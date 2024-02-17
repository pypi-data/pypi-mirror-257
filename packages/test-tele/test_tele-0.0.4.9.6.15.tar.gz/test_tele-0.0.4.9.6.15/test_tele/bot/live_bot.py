"""A bot to control settings for telethon bot live mode."""

import re
import time
import yaml
import logging

from telethon import events, Button

from test_tele import config
from test_tele.bot.bot_header import *
from test_tele.bot.utils import (
    admin_protect,
    registered_user,
    display_forwards,
    get_args,
    get_command_prefix,
    get_command_suffix,
    remove_source,
    query # query db_helper
)
from test_tele.config import CONFIG, write_config
from test_tele.config_bot import BOT_CONFIG, UserBot, write_bot_config
from test_tele.plugin_models import Style
from test_tele.plugins import TgcfMessage

from telethon import errors
from telethon.tl.functions.messages import (
    SetInlineBotResultsRequest, SendMultiMediaRequest, SetTypingRequest,
    UploadMediaRequest
)
from telethon.tl.types import (
    InputBotInlineResult, InputPhoto, InputMediaPhoto, InputSingleMedia, InputDocument,
    InputMediaPhotoExternal, InputMediaDocument, InputMediaDocumentExternal, SendMessageUploadDocumentAction,
    InputBotInlineMessageMediaAuto, InputWebDocument, SendMessageUploadPhotoAction
)


@admin_protect
async def forward_command_handler(event):
    """Handle the `/forward` command."""
    notes = """The `/forward` command allows you to add a new forward.
    Example: suppose you want to forward from a to (b and c)

    ```/forward source: a
    dest: [b,c]
    ```

    a,b,c are chat ids
    """.replace("    ", "")

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n{display_forwards(config.CONFIG.forwards)}")

        parsed_args = yaml.safe_load(args)
        forward = config.Forward(**parsed_args)
        try:
            remove_source(forward.source, config.CONFIG.forwards)
        except:
            pass
        CONFIG.forwards.append(forward)
        config.from_to, config.reply_to = await config.load_from_to(event.client, config.CONFIG.forwards)

        await event.respond("Success")
        write_config(config.CONFIG)
    except ValueError as err:
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


@admin_protect
async def remove_command_handler(event):
    """Handle the /remove command."""
    notes = """The `/remove` command allows you to remove a source from forwarding.
    Example: Suppose you want to remove the channel with id -100, then run

    `/remove source: -100`

    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n{display_forwards(config.CONFIG.forwards)}")

        parsed_args = yaml.safe_load(args)
        source_to_remove = parsed_args.get("source")
        CONFIG.forwards = remove_source(source_to_remove, config.CONFIG.forwards)
        config.from_to, config.reply_to = await config.load_from_to(event.client, config.CONFIG.forwards)

        await event.respond("Success")
        write_config(config.CONFIG)
    except ValueError as err:
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


@admin_protect
async def style_command_handler(event):
    """Handle the /style command"""
    notes = """This command is used to set the style of the messages to be forwarded.

    Example: `/style bold`

    Options are preserve,normal,bold,italics,code, strike

    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n")
        _valid = [item.value for item in Style]
        if args not in _valid:
            raise ValueError(f"Invalid style. Choose from {_valid}")
        CONFIG.plugins.fmt.style = args
        await event.respond("Success")
        write_config(CONFIG)
    except ValueError as err:
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


# =================================================


@admin_protect
async def respond_command_handler(event):
    """Handle the /reply command handler"""
    
    try:
        args = get_args(event.message.text)
        if not args:
            return

        tm = TgcfMessage(event.message)
        
        matches = re.match(r'(\d+)\s(.+)', args, re.DOTALL)
        id_user = matches.group(1)
        isi_pesan = matches.group(2)

        tm.text = f'Admin says: "{isi_pesan}"'
        await start_sending(int(id_user), tm)

    except Exception as err:
        logging.error(err)
    finally:
        raise events.StopPropagation


async def start_command_handler(event):
    """Handle the /start command"""
    event = event.message
    chat_id = event.chat_id

    try:
        if not query.read_datas('users', None, 'chat_id = %s', [chat_id]):
            user = await event.client.get_entity(chat_id)
            query.create_data(
                'users', 
                ['chat_id', 'username', 'firstname', 'is_subscriber', 'is_full_subscriber', 'is_block'], 
                [chat_id, user.username, user.first_name, 0, 0, 0]
            )
            query.create_data(
                'settings',
                ['lang', 'def_inline', 'caption', 'keyboard', 'chat_id'],
                ['en', 'Gelbooru', 1, 1, chat_id]
            )

        await event.respond(BOT_CONFIG.bot_messages.start)
    except Exception as e:
        pass
    finally:
        raise events.StopPropagation


async def help_command_handler(event):
    """Handle the /help command."""
    await event.respond(BOT_CONFIG.bot_messages.bot_help)


async def report_command_handler(event):
    """Handle the /report command"""
    notes = """The command `/report` allows you to send a message to the bot Admin.

    Command: `/report`
    Usage: MESSAGE..

    **Example**
    `/report Bot is not responding. Not sure if you received this or not.. lol`
    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n")
        
        tm = TgcfMessage(event.message)
        tm.text = f"**-= New Message =-**\nfrom: `{tm.message.chat_id}`\n———————————\n" + args
        tm.text += f"\n———————————\n#report"

        admin = query.read_datas('admins', ['chat_id'], "role = 'admin'")
        if admin:
            await start_sending(admin[0][0], tm)
            await event.respond("We have received your message. Please wait while the Admin attempts to fix it")
        
    except ValueError as err:
        await event.respond(str(err))
    finally:
        raise events.StopPropagation


async def setting_command_handler(event):
    """Handle the /setting command"""
    notes = """**SETTINGS**

    Command: `/report`
    Usage: MESSAGE..

    **Example**
    `/report Bot is not responding. Not sure if you received this or not.. lol`
    """.replace(
        "    ", ""
    )
    
    try:
        pass
    except:
        pass
    finally:
        raise events.StopPropagation


@registered_user
async def get_id_command_handler(event, is_premium:bool = False):
    """Handle the /id command"""

    try:
        args = get_args(event.message.text)

        if not args and CONFIG.login.user_type == 1:
            tm = TgcfMessage(event.message)
            tm.text = ""
            i = 0

            async for dialog in event.client.iter_dialogs():
                if dialog.is_channel:
                    i += 1
                    if i <= 80:
                        ch_id = f"`{str(dialog.id)}`"
                        ch_name = str(dialog.name).replace("`", "'")
                        tm.text += ch_id + " 👉 " + ch_name + "\n"
                    else:
                        await start_sending(tm.message.chat_id, tm)
                        tm.text = ""
                        i = 0
            
            await start_sending(tm.message.chat_id, tm)

        message = await event.message.get_reply_message()
        await event.respond(f"```{message.stringify()}```")

    except Exception as err:
        logging.error(err)
        message = await event.message.get_reply_message()
        await event.respond(f"```{message.stringify()}```")

    finally:
        raise events.StopPropagation


@registered_user
async def get_message_command_handler(event, is_premium:bool = False):
    """Handle the command /get"""
    notes = """The command `/get` is used to retrieve messages from a public channel or group even if forwarding is not allowed.

    Command: `/get`
    Usage: LINK..
    Note: copy the message link from the public channel or group, and paste it here as argument
    
    **Example** 
    `/get https://t.me/username/post_id`
    """.replace("    ", "")

    try:
        args = get_args(event.message.text)

        if not args:
            raise ValueError(f"{notes}\n")

        pattern = r'(t.me/(c/)?|)(-?\w+)/(\d+)'
        match = re.search(pattern, args)

        tm = TgcfMessage(event.message)

        if match:
            entity = str(match.group(3))
            ids = int(match.group(4))
            chat = await get_entity(event, entity)

            if chat is None:
                raise ValueError("Unable to get post")

            message = await event.client.get_messages(chat, ids=ids)            
            tm.text = message.message
            caption = tm.text + f"\n\n👉 {BOT_CONFIG.bot_name} 👈"

            if message.grouped_id is not None and message.media:
                from test_tele.live_pyrogram import BOT as app
                await app.copy_media_group(
                    tm.message.chat_id, 
                    chat.username, 
                    message.id, 
                    disable_notification=True,
                    captions=caption, 
                )
            elif message.grouped_id is None and message.media:
                from test_tele.live_pyrogram import BOT as app
                await app.copy_message(
                    tm.message.chat_id, 
                    chat.username, 
                    message.id, 
                    disable_notification=True,
                    caption=caption, 
                )

    except ValueError as err:
        await event.respond(str(err))

    except Exception as err:
        await event.respond("Something's wrong! Please report it to the bot Admin")
        logging.error(err, exc_info=True)

    finally:
        raise events.StopPropagation


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
            ids = message.id
            message.text += f"\n\n👉 {BOT_CONFIG.bot_name} 👈 | `t.me/{username}/{ids}`"
            return await event.client.send_message(event.message.chat_id, message, buttons=[
                                Button.inline('◀️', f'gtp_{username}_{ids}'),
                                Button.inline('▶️', f'gtn_{username}_{ids}')
                            ])
        return

    except Exception as err:
        logging.error(err)
    finally:
        raise events.StopPropagation


@registered_user
async def callback_get_message(event, is_premium:bool = False):
    """Handle callback for get messages"""
    try:
        pattern = r'gt(?:p|n)_(\w+)_(\d+)'
        text = event.data.decode('utf-8')
        match = re.match(pattern, text)
        id_post = 2

        if match:
            ent_chnl = match.group(1)
            id_post = int(match.group(2))

            if text.startswith("gtp_"):
                id_post -= 1
                message = await loop_message(event, ent_chnl, id_post, False)
            if text.startswith("gtn_"):
                id_post += 1
                message = await loop_message(event, ent_chnl, id_post)

            id_msg = message.id
            msg_text = message.text + f"\n\n👉 {BOT_CONFIG.bot_name} 👈 | `t.me/{ent_chnl}/{id_msg}`"
            return await event.edit(text=msg_text, file=message.media, buttons=[
                                Button.inline('◀️', f'gtp_{ent_chnl}_{id_msg}'),
                                Button.inline('▶️', f'gtn_{ent_chnl}_{id_msg}')
                            ])

    except Exception as err:
        logging.error(err)

    finally:
        raise events.StopPropagation


@registered_user
async def get_images_from_inline(event, is_premium:bool = False):
    event = event.message
    query = event.text
    start = time.time()

    if not is_premium:
        return

    n = 10
    part = 0
    await event.client(SetTypingRequest(event.input_chat, SendMessageUploadPhotoAction(0)))

    query, mode, keywords = await check_prefix(query)

    limit: int = mode.get('limit', 30)
    offset: int = mode.get('offset', 0)
    as_file = mode.get('file', False)

    logging.warning("lama proses gambar: %s", round(time.time(), 2) - start)
    lists = await get_images_dict(query, keywords, offset)

    if not lists:
        return

    try:
        for chunk in (lists[i:i + n] for i in range(0, limit, n)):
            try:
                max_slice = limit - part
                img_lists = await get_images_list(query, chunk, max_slice)
                logging.warning(f"ini img_lists : {img_lists}")
                images = await upload_images_to_tele(as_file, event, img_lists)
                logging.warning(f"ini images : {images}")
                if not images or part >= 30:
                    break
                    
            except errors.MultiError as e:
                logging.warning("UploadMedia returned one or more errors")
                logging.error(f"{e.exceptions}, {e.results}, {e.requests}")
                if not any(e.results):
                    logging.exception("All UploadMedia requests failed")
                    return
                images = filter(None, e.results)

            if as_file:
                images = [InputSingleMedia(InputMediaDocument(InputDocument(img.document.id, img.document.access_hash, b'')), '') for img in images]
            else:
                images = [InputSingleMedia(InputMediaPhoto(InputPhoto(img.photo.id, img.photo.access_hash, b'')), '') for img in images]
            try:
                await event.client(SendMultiMediaRequest(event.input_chat, images))
                part += len(images)
            except (errors.UserIsBlockedError, errors.RPCError):  # TODO: add other relevant errors
                logging.exception("Failed to send multimedia")
        
        logging.warning("lama seluruh proses : %s", round(time.time(), 2) - start)

    except Exception as err:
        logging.error(err)

    finally:
        raise events.StopPropagation


def get_events(val): # tambah argumen
    logging.info(f"Command prefix is . for userbot and / for bot")
    _ = get_command_prefix(val)
    u = get_command_suffix(val)
    command_events = {
        "start": (start_command_handler, events.NewMessage(pattern=f"{_}start{u}")),
        "forward": (forward_command_handler, events.NewMessage(pattern=f"{_}forward")),
        "remove": (remove_command_handler, events.NewMessage(pattern=f"{_}remove")),
        "style": (style_command_handler, events.NewMessage(pattern=f"{_}style")),
        "help": (help_command_handler, events.NewMessage(pattern=f"{_}help{u}")),
        "get_id": (get_id_command_handler, events.NewMessage(pattern=f"{_}id{u}")),
    }
    if val == 0: # bot
        khusus_bot= {
            "report": (report_command_handler, events.NewMessage(pattern=f"{_}report")),
            "reply": (respond_command_handler, events.NewMessage(pattern=f"{_}reply")),
            "get_post": (get_message_command_handler, events.NewMessage(pattern=f"{_}get")),
            "get_images": (get_images_from_inline, events.NewMessage(pattern=r".(?:px|rp)")),
            "adv_get_post": (advanced_get_message_handler, events.NewMessage(pattern=r'(?:https?://)?(?:t.me\/|@)(\w+)')),
            "cb_get_post": (callback_get_message, events.CallbackQuery(pattern=r'gt(?:p|n)_')),
        }
        command_events.update(khusus_bot)

    return command_events

# PYROGRAM ==================================================

from pyrogram import filters, enums
from pyrogram.types import InlineQuery, CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import (InlineQueryHandler, CallbackQueryHandler, MessageHandler)

from test_tele.features.pyrogram.pixiv import inline_pixiv, get_px_file
from test_tele.features.pyrogram.gelbooru import inline_gelbooru, get_gb_file
from test_tele.features.pyrogram.manga import inline_mangapark, check_inline_query_type
from test_tele.features.pyrogram.realperson import inline_realperson, get_nude_file
from test_tele.features.pyrogram.furry import inline_furry, get_fur_file

# Inline 
async def inline_handler(app, inline_query: InlineQuery):
    """Handle inline query search"""
    query_handlers = {
        '/': check_inline_query_type,
        '.md': inline_mangapark,
        '.px': inline_pixiv,
        '.rp': inline_realperson,
        '.fur': inline_furry
        # '.2d': inline_vanillarock
    }

    for query_prefix, handler in query_handlers.items():
        if inline_query.query.lower().startswith(query_prefix):
            await handler(app, inline_query)
            break
    else:
        await inline_gelbooru(app, inline_query)

# Callback button
async def callback_query_handler(app, callback_query: CallbackQuery):
    """Get callback query from inline keyboard"""
    handlers = {
        "md": None,
        "gb": get_gb_file,
        "px": get_px_file,
        "rp": get_nude_file,
        "fur": get_fur_file
        # "2d": get_vr_file
    }

    for prefix, handler in handlers.items():
        if callback_query.data.startswith(prefix):
            image_file = await handler(callback_query.data.replace(f"{prefix} ", ''))
            if callback_query.data.startswith("md"):
                await app.send_photo(callback_query.from_user.id, image_file)
            else:
                await app.send_document(callback_query.from_user.id, image_file)
            break
    else:
        pass

# Incoming message containing command /sauce 
async def sauce_command_handler(app, message: Message):
    """Handles the /sauce command."""
    notes = """The command /sauce is used to search for the source or origin of the image being replied to.

    Command: `/sauce`
    Note: reply to message with media (preferably 2D/anime picture)
    """.replace("    ", "")

    try:
        if message.text == "/sauce" and not message.reply_to_message_id:
            raise ValueError(f"{notes}\n")
        
        if message.text == "/sauce":
            replied_msg = await app.get_messages(
                message.chat.id, message.reply_to_message_id
            )
            file_bytes = await download_media_bytes(app, replied_msg)
            resp = await search_images(file_bytes, command=True)
            
            author = f"[{resp[0]['author']}]({resp[0]['author_url']})" if resp[0]['author'] and resp[0]['author_url'] else 'Unknown'
            msg_to_send = (
                f"**[{resp[0]['title']}]({resp[0]['url']})**\n"
                f"Author: {author}\n"
            ) if resp else "Sorry, no matches were found"

            await send_response(msg_to_send, message, resp)
        elif message.photo and not message.outgoing:
            if message.media_group_id:
                msg_list = await message.get_media_group()
                for per_msg in msg_list:
                    file_bytes = await download_media_bytes(app, per_msg)
                    resp = await search_images(file_bytes)
                    if resp:
                        msg_to_send = (
                            "The full version is found in :\n"
                            f"{resp[0]['title']}\n"
                            "Initiating synchronization, Please wait..\n"
                        )
                        msg = await send_response(msg_to_send, message, resp)
                    # do something about ex-hent to telegraph here
            else:
                file_bytes = await download_media_bytes(app, message)
                resp = await search_images(file_bytes)
                if resp:
                    msg_to_send = (
                        "The full version is found in :\n"
                        f"{resp[0]['title']}\n"
                        "Initiating synchronization, Please wait..\n"
                    )
                    msg = await send_response(msg_to_send, message, resp)
                # do something about ex-hent to telegraph here

    except ValueError as err:
        await app.send_message(message.from_user.id, str(err))

    except Exception as err:
        logging.error(err, exc_info=True)
    finally:
        raise message.stop_propagation()


async def send_response(msg_to_send, message: Message, resp = None) -> Message:
    """Sends the response message with formatted text and reply markup."""

    reply_markup = await get_reply_markup(resp)
    sent_msg = await message.reply(
        msg_to_send,
        disable_web_page_preview=True,
        disable_notification=True,
        reply_to_message_id=message.id,
        reply_markup=reply_markup,
    )
    return sent_msg


async def get_reply_markup(results: list):
    """Returns an InlineKeyboardMarkup object based on the given URL."""
    buttons = []
    supported_url = ['pixiv']

    if results:
        for i, res in enumerate(results):
            buttons.append(
                [
                    InlineKeyboardButton(res['category'], url=res['url'])
                ]
            )
            if res['category'].lower() in supported_url:
                if 'pixiv' in res['category'].lower():
                    id_author = res['author_url'].replace("https://www.pixiv.net/users/", "")
                    id_art = res['url'].replace("https://www.pixiv.net/artworks/", "")
                    buttons[i].insert(0, InlineKeyboardButton("👤🔄", switch_inline_query_current_chat=f".px id:{id_author}"))
                    buttons[i].insert(2, InlineKeyboardButton("🔗🔄", switch_inline_query_current_chat=f".px {id_art}"))

        return InlineKeyboardMarkup(buttons)
    return None




def get_handlers():
    cb_for_image = r"(?:md|gb|px|rp|fur|2d)"
    filter_for_image_search = filters.command("sauce") | (filters.photo | filters.media_group) & filters.incoming & filters.private
    pyrogram_handler = {
        "inline_query": InlineQueryHandler(inline_handler),
        "callback_query": CallbackQueryHandler(callback_query_handler, filters.regex(cb_for_image)),
        "image_search": MessageHandler(sauce_command_handler, filter_for_image_search)
    }

    return pyrogram_handler
