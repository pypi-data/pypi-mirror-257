import re
import asyncio
from typing import TYPE_CHECKING
from telethon.tl import types

from pyrogram.types import Message
from test_tele.utils import start_sending

if TYPE_CHECKING:
    from test_tele.plugins import TgcfMessage

timeout = 60
proxies = None
web_pattern = r'([-\w]+)\.[a-z]{2,3}\/'
cookies = "ipb_session_id=99588dfea429026c8abb2dc5dba908a8; ipb_member_id=7096096; ipb_pass_hash=c8a343f74141f88a715eee04d96ef5eb"
saucenao_api = "6c2e6af3fa0b1b76971067efb5ab633c5c3ec2bf"

## Helper function for get_message
    
async def get_entity(event, entity):
    """Get chat entity from entity parameter"""
    if entity.isdigit() or entity.startswith("-"):
        chat = types.PeerChannel(int(entity))
    else:
        try:
            chat = await event.client.get_entity(entity)
        except Exception as e:
            chat = await event.client.get_entity(types.PeerChat(int(entity)))

    return chat


async def loop_message(event, chat, ids: int, next=True):
    """Loop channel posts to get message"""
    skip = 20
    tries = 0
    while True:
        if ids > 0 and tries <= skip:
            message = await event.client.get_messages(chat, ids=ids)
            tries += 1
            if not message:
                if next:
                    ids += 1
                    continue
                else:
                    ids -= 1
                    continue
            else:
                if hasattr(message, 'message'):
                    if message.media and not (message.sticker or message.voice or message.web_preview):
                        return message
                ids = ids + 1 if next else ids - 1
        else:
            return


# Download media in message and store it as byte
        
async def download_media_bytes(app, message: Message):
    """Downloads media from a message and returns its bytes."""

    file = await app.download_media(message, in_memory=True)
    return bytes(file.getbuffer())

# Helper for reverse image search

async def saucenao_image_search(file_path, url:str = None) -> list:
    """Image search using saucenao"""
    from PicImageSearch import SauceNAO

    ehentai = SauceNAO(api_key=saucenao_api, numres=3, minsim=80)
    resp = await ehentai.search(url=url, file=file_path)
    
    results = []
    seen_categories = set()

    if resp.status_code == 200:
        for selected in (i for i in resp.raw if i.title and i.url and i.similarity > 80):
            match = re.search(web_pattern, selected.url)
            if match:
                category = match.group(1).capitalize()
                if category in seen_categories:
                    continue
                seen_categories.add(category)
            else:
                category = 'Unknown'

            my_dict = {
                "title": selected.title,
                "url": selected.url,
                "category": category,
                "author": selected.author,
                "author_url": selected.author_url,
            }
            results.append(my_dict)

        return results
    else:
        return await ascii_image_search(file_path, url)


async def ascii_image_search(file_path, url:str = None) -> list:
    """Image search using ASCII2D"""
    from PicImageSearch import Ascii2D

    ascii2d = Ascii2D(proxies=proxies)
    resp = await ascii2d.search(url=url, file=file_path)
    
    results = []
    seen_categories = set()

    for selected in (i for i in resp.raw if (i.title or i.url_list) and i.url):
        match = re.search(web_pattern, selected.url)
        if match:
            category = match.group(1).capitalize()
            if category in seen_categories:
                continue
            seen_categories.add(category)
        else:
            category = 'Unknown'

        my_dict = {
            "title": selected.title,
            "url": selected.url,
            "category": category,
            "author": selected.author,
            "author_url": selected.author_url,
        }
        results.append(my_dict)

    return results


async def ehentai_image_search(file_path, url:str = None) -> list:
    """Image search using e-hentai"""
    from PicImageSearch import EHentai, Network

    ehentai = EHentai(proxies=proxies, cookies=cookies, timeout=timeout)
    resp = await ehentai.search(url=url, file=file_path)
    
    results = []
    seen_categories = set()

    for selected in (i for i in resp.raw if i.title and i.url):
        match = re.search(web_pattern, selected.url)
        if match:
            category = match.group(1).capitalize()
            if category in seen_categories:
                continue
            seen_categories.add(category)
        else:
            category = 'Unknown'

        my_dict = {
            "title": selected.title,
            "url": selected.url,
            "category": category
        }
        results.append(my_dict)

    return results


async def search_images(file_path, url:str = None, command: bool = False) -> list:
    """Global function for search images"""

    if command:
        resp_ascii, resp_ehentai = await asyncio.gather(
            saucenao_image_search(file_path, url), 
            ehentai_image_search(file_path, url)
        )
        resp = resp_ascii + resp_ehentai
    else:
        resp = await ehentai_image_search(file_path, url)

    return resp

