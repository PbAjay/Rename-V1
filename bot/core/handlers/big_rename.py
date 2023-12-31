import traceback
from typing import Union
from bot.client import Client
from pyrogram import raw, utils
from pyrogram.types import Message
from configs import Config
from bot.core.utils.rm import rm_dir
from bot.core.fixes import fix_thumbnail
from bot.core.db.database import db
from bot.core.file_info import get_thumb_file_id, get_media_mime_type


async def handle_big_rename(
    c: Client,
    m: Message,
    file_id: Union[raw.types.InputFileBig, raw.types.InputFile],
    file_name: str,
    editable: Message,
    file_type: str
) -> None:
    await editable.edit("Sending to you ...")
    upload_as_doc = await db.get_upload_as_doc(m.from_user.id)

    if not upload_as_doc and file_type == "video":
        ttl_seconds = None
        supports_streaming = m.reply_to_message.video.supports_streaming or None
        duration = m.reply_to_message.video.duration or 0
        width = m.reply_to_message.video.width or 0
        height = m.reply_to_message.video.height or 0
        mime_type = m.reply_to_message.video.mime_type or "video/mp4"
        _f_thumb = m.reply_to_message.video.thumbs[0] if m.reply_to_message.video.thumbs else None
        _db_thumb = await db.get_thumbnail(m.from_user.id)
        thumbnail_file_id = _db_thumb or (_f_thumb.file_id if _f_thumb else None)

        if thumbnail_file_id:
            await editable.edit("Fetching Thumbnail ...")
            thumb_path = await c.download_media(
                thumbnail_file_id, f"{Config.DOWNLOAD_DIR}/{m.from_user.id}/{m.message_id}/"
            )

            if _db_thumb:
                thumb_path = await fix_thumbnail(thumb_path)

            thumb = await c.save_file(path=thumb_path)
        else:
            thumb = None

        media = raw.types.InputMediaUploadedDocument(
            mime_type=mime_type,
            file=file_id,
            ttl_seconds=ttl_seconds,
            thumb=thumb,
            attributes=[
                raw.types.DocumentAttributeVideo(
                    supports_streaming=supports_streaming,
                    duration=duration,
                    w=width,
                    h=height
                ),
                raw.types.DocumentAttributeFilename(file_name=file_name)
            ]
        )
    # ... (similar adjustments for audio and document cases)

    try:
        r = await c.send(
            raw.functions.messages.SendMedia(
                peer=await c.resolve_peer(m.chat.id),
                media=media,
                silent=None,
                reply_to_msg_id=None,
                random_id=c.rnd_id(),
                schedule_date=None,
                reply_markup=await reply_markup.write(c) if reply_markup else None,
                **await utils.parse_text_entities(c, caption, parse_mode, None)
            )
        )
        await rm_dir(f"{Config.DOWNLOAD_DIR}/{m.from_user.id}/{m.message_id}/")
    except Exception as _err:
        Config.LOGGER.getLogger(__name__).error(_err)
        Config.LOGGER.getLogger(__name__).info(traceback.format_exc())
    else:
        await editable.edit("Uploaded Successfully!")
        
