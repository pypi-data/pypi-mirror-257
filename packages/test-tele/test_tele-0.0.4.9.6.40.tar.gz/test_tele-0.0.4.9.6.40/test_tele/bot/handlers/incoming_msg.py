import re
import time
import asyncio
import logging

from telethon import events, Button, errors
from telethon.tl.functions.messages import SendMultiMediaRequest, SetTypingRequest, UploadMediaRequest
from telethon.tl.types import (
    InputPhoto, InputMediaPhoto, 
    InputSingleMedia, InputDocument, 
    InputMediaDocument, SendMessageUploadPhotoAction,
    InputMediaPhotoExternal, InputMediaDocumentExternal,
    InputReplyToMessage
)
from pyrogram import filters
from pyrogram.types import Message, InputMediaPhoto
from pyrogram.handlers import (MessageHandler, EditedMessageHandler)
from pyrogram.enums import MessageEntityType

from test_tele.bot.utils import registered_user, query
from test_tele.bot.bot_header import loop_message
from test_tele.config_bot import BOT_CONFIG
from test_tele.plugins import TgcfMessage
from test_tele.features.extractors import gallery_dl, download_from_url, images_in_folder


# Helper for image grabber
        
async def check_prefix(query):
    from test_tele.features.extractors.utils import clean_up_tags

    if query.startswith('.px'):
        from test_tele.features.extractors.pixiv import PIXIV_MODE
        mode, keywords = await clean_up_tags('no_inline ' + query, PIXIV_MODE, '.px')
    elif query.startswith('.rp'):
        from test_tele.features.extractors.realperson import get_nude_list
        mode, keywords = await clean_up_tags('no_inline ' + query, [], '.rp')

    return query, mode, keywords


async def get_images_dict(query, keywords, offset):
    if query.startswith('.px'):
        from test_tele.features.extractors.pixiv import get_pixiv_list
        lists = await get_pixiv_list(keywords, offset)
    elif query.startswith('.rp'):
        from test_tele.features.extractors.realperson import get_nude_list
        lists = await get_nude_list(keywords, offset)
    return lists


async def get_images_list(query, chunk, max_slice):
    if query.startswith('.px'):
        img_lists = [lists['img_urls']['img_original'] for lists in chunk[:max_slice]]
    elif query.startswith('.rp'):
        img_lists = [lists['img_url'] for lists in chunk[:max_slice]]
    return img_lists


async def upload_image(img, as_file, event):
    ttl = 86000
    try:
        if as_file:
            media_request = await event.client(
                UploadMediaRequest(event.input_chat, InputMediaDocumentExternal(img, ttl_seconds=ttl))
            )
        else:
            media_request = await event.client(
                UploadMediaRequest(event.input_chat, InputMediaPhotoExternal(img, ttl_seconds=ttl))
            )
        return media_request
    except errors.FloodWaitError as e:
        time.sleep(e.seconds)
    except:
        return None


@registered_user
async def get_images_from_inline(event, is_premium:bool = False):
    event = event.message
    query = event.text

    if not is_premium:
        return

    n = 10
    part = 0
    await event.client(SetTypingRequest(event.input_chat, SendMessageUploadPhotoAction(0)))
    query, mode, keywords = await check_prefix(query)

    limit: int = mode.get('limit', 30)
    offset: int = mode.get('offset', 0)
    as_file = mode.get('file', False)

    lists = await get_images_dict(query, keywords, offset)

    if not lists:
        return

    try:
        for chunk in (lists[i:i + n] for i in range(0, limit, n)):
            max_slice = limit - part
            img_lists = await get_images_list(query, chunk, max_slice)
            if not img_lists or part >= 30:
                break
            tasks = [upload_image(img, as_file, event) for img in img_lists]
            results = await asyncio.gather(*tasks)
            images = [result for result in results if result is not None]
            if not images:
                continue

            if as_file:
                images = [InputSingleMedia(InputMediaDocument(InputDocument(img.document.id, img.document.access_hash, b'')), '') for img in images]
            else:
                images = [InputSingleMedia(InputMediaPhoto(InputPhoto(img.photo.id, img.photo.access_hash, b'')), '') for img in images]
            try:
                await event.client(
                    SendMultiMediaRequest(event.input_chat, images, silent=True, background=True, reply_to=InputReplyToMessage(event.id))
                )
                part += len(images)
            except errors.FloodWaitError as e:
                time.sleep(e.seconds)
            except (errors.UserIsBlockedError, errors.RPCError):  # TODO: add other relevant errors
                logging.exception("Failed to send multimedia")
        
    except Exception as err:
        logging.error(err)

    finally:
        raise events.StopPropagation


# Helper for save links

async def find_links(text):
    link_pattern = r'((?:t.me/|@)[_0-9a-zA-Z/]+)'

    links = []
    for link in re.findall(link_pattern, text):
        link_type = 'sticker' if 'addstickers' in link else 'addlist' if 'addlist' in link else 'channel'
        links.append((link, link_type))
    return links


async def save_links(links):
    for link, link_type in links:
        link: str = link.replace("@", "t.me/")
        if link_type == 'channel':
            if link.endswith("bot") or link.endswith("Bot"):
                continue
            tme, url, *id = link.split("/")
            link = f"{tme}/{url}"
        link = "https://" + link
        if not query.read_datas('links', None, 'url = %s', [link]):
            query.create_data('links', ['url', 'type'], [link, link_type])


async def get_links(event):
    links = await find_links(event.text)
    if links:
        await save_links(links)

    try:
        for entity in event.entities:
            if entity.type == MessageEntityType.TEXT_LINK:
                links = await find_links(entity.url)
                await save_links(links)
    except:
        pass


async def incoming_message_handler(app, message: Message):
    """Handle spesific incoming message"""
    try:
        if message.text:
            # grab links
            await get_links(message)
        elif message.sticker:
            # logging.warning("ya ini sticker")
            link = await find_links(f"t.me/addstickers/{message.sticker.set_name}")
            await save_links(link)
            
    except Exception as err:
        logging.error(err, exc_info=True)
    

async def edited_message_handler(app, message: Message):
    """Handle spesific edited message"""
    try:
        if message.text:
            await get_links(message)
            
    except Exception as err:
        logging.error(err, exc_info=True)


@registered_user
async def advanced_get_message_handler(event, is_premium:bool = False):
    """Handle new incoming post link message"""
    try:
        pattern = r'(?:t\.me/|@)(\w+)(?:/(\d+))?' 
        if match := re.search(pattern, event.message.text):
            entity, ids = match.groups()
            ids = int(ids) if ids else 2
        else:
            return

        if entity in ('addstickers', 'proxy', 'addlist'):
            return

        # username = await get_entity(event, entity)
        username = entity
        message = await loop_message(event, username, ids)

        if message:
            tm = TgcfMessage(message)
            message.text = tm.text + f"\n\n👉 {BOT_CONFIG.bot_name} 👈 | `t.me/{username}/{tm.message.id}`"
            return await event.client.send_message(
                event.message.chat_id, 
                message, 
                reply_to=event.message.id, 
                buttons=[
                    Button.inline('◀️', f'gtp_{username}_{tm.message.id}'),
                    Button.inline('▶️', f'gtn_{username}_{tm.message.id}')
                ]
            )
        return

    except Exception as err:
        logging.error(err)
    finally:
        raise events.StopPropagation


@registered_user
async def download_media_url_handler(event, is_premium: bool=False):
    """Handle if incoming message is a url"""
    # pattern = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', event.message.text)
    pattern = r'(https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)'
    web_pattern = r'https?:\/\/([\.\w]+)\.[a-z]{2,4}\/'

    match = re.search(pattern, event.message.text)
    if not match:
        return
    
    gallery_dl_result = await gallery_dl(match.group(1), force_kill=10)
    lists = []
    category = ''
    for elemen in gallery_dl_result:
        if elemen[0] == 3:
            my_dict = {
                'user_id': event.message.chat_id,
                'index': str(elemen[2]['num']),
                'img_url': elemen[1],
                'extension': elemen[2]['extension'],
                'category': elemen[2]['category']
            }
            category = elemen[2]['category']
            lists.append(my_dict)
    await download_from_url(lists)
    media_lists = await images_in_folder(f'temps/{event.message.chat_id}/{category}')
    await event.message.client.send_file(event.message.chat_id, media_lists, reply_to=event.message.id, silent=True, background=True)


def get_incoming_msg_handlers_telethon(val) -> dict:
    """Get only incoming message handlers for telethon"""
    incoming_msg_handlers = {}
    if val == 0: # bot
        incoming_msg_handlers_for_bot = {
            "adv_get_post": (advanced_get_message_handler, events.NewMessage(pattern=r'(?:https?://)?(?:t.me\/|@)(\w+)')),
            "download_media": (download_media_url_handler, events.NewMessage(pattern=r'(?:https?://)')),
            "get_images": (get_images_from_inline, events.NewMessage(pattern=r".(?:px|rp)"))
        }
        incoming_msg_handlers.update(incoming_msg_handlers_for_bot)

    return incoming_msg_handlers


def get_incoming_msg_handlers_pyrogram() -> dict:
    """Get only incoming message handlers for pyrogram"""
    pyrogram_incoming_msg_handler = {
        "in_message": MessageHandler(incoming_message_handler, filters.text | filters.sticker),
        "update_message": EditedMessageHandler(edited_message_handler, filters.text)
    }

    return pyrogram_incoming_msg_handler
