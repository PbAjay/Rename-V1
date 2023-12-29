from configs import Config
from bot.client import Client
from pyrogram.types import Message
from bot.core.db.database import db
from typing import Optional, Union


async def handle_not_big(
    c: Client,
    m: Message,
    file_id: str,
    file_name: str,
    editable: Message,
    upload_mode: str = "document",
    thumb: Optional[str] = None,
) -> None:
    reply_markup = m.reply_to_message.reply_markup if m.reply_to_message.reply_markup else None
    _db_caption = await db.get_caption(m.from_user.id)
    apply_caption = await db.get_apply_caption(m.from_user.id)

    if (not _db_caption) and (apply_caption is True):
        caption = m.reply_to_message.caption.markdown if m.reply_to_message.caption else "**Developer: @AbirHasan2005**"
    elif _db_caption and (apply_caption is True):
        caption = _db_caption
    else:
        caption = ""

    parse_mode = "Markdown"
    
    if thumb:
        _thumb = await c.download_media(thumb, f"{Config.DOWNLOAD_DIR}/{m.from_user.id}/{m.message_id}/")
    else:
        _thumb = None

    upload_as_doc = await db.get_upload_as_doc(m.from_user.id)

    if (upload_as_doc is False) and (upload_mode == "video"):
        performer: Optional[str] = None
        title: Optional[str] = None
        duration: int = m.reply_to_message.video.duration if m.reply_to_message.video.duration else 0
        width: int = m.reply_to_message.video.width if m.reply_to_message.video.width else 0
        height: int = m.reply_to_message.video.height if m.reply_to_message.video.height else 0
    elif (upload_as_doc is False) and (upload_mode == "audio"):
        width: Optional[int] = None
        height: Optional[int] = None
        duration: Optional[int] = m.reply_to_message.audio.duration if m.reply_to_message.audio.duration else None
        performer: Optional[str] = m.reply_to_message.audio.performer if m.reply_to_message.audio.performer else None
        title: Optional[str] = m.reply_to_message.audio.title if m.reply_to_message.audio.title else None
    else:
        duration: Optional[int] = None
        width: Optional[int] = None
        height: Optional[int] = None
        performer: Optional[str] = None
        title: Optional[str] = None

    await c.normal_rename(
        file_id,
        file_name,
        editable,
        m.chat.id,
        upload_mode,
        _thumb,
        caption,
        parse_mode,
        reply_markup=reply_markup,
        duration=duration,
        width=width,
        height=height,
        performer=performer,
        title=title
        )
    
