import datetime
import motor.motor_asyncio
from configs import Config
from typing import Optional, Union


class Database:
    def __init__(self, uri: str, database_name: str):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id: int) -> dict:
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            apply_caption=True,
            upload_as_doc=False,
            thumbnail=None,
            caption=None
        )

    async def add_user(self, id: int) -> None:
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id: int) -> bool:
        user = await self.col.find_one({'id': id})
        return bool(user)

    async def total_users_count(self) -> int:
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self) -> motor.motor_asyncio.AsyncIOMotorCursor:
        return self.col.find({})

    async def delete_user(self, user_id: int) -> None:
        await self.col.delete_many({'id': user_id})

    async def set_apply_caption(self, id: int, apply_caption: bool) -> None:
        await self.col.update_one({'id': id}, {'$set': {'apply_caption': apply_caption}})

    async def get_apply_caption(self, id: int) -> bool:
        user = await self.col.find_one({'id': id})
        return user.get('apply_caption', True)

    async def set_upload_as_doc(self, id: int, upload_as_doc: bool) -> None:
        await self.col.update_one({'id': id}, {'$set': {'upload_as_doc': upload_as_doc}})

    async def get_upload_as_doc(self, id: int) -> bool:
        user = await self.col.find_one({'id': id})
        return user.get('upload_as_doc', False)

    async def set_thumbnail(self, id: int, thumbnail: Optional[str]) -> None:
        await self.col.update_one({'id': id}, {'$set': {'thumbnail': thumbnail}})

    async def get_thumbnail(self, id: int) -> Optional[str]:
        user = await self.col.find_one({'id': id})
        return user.get('thumbnail', None)

    async def set_caption(self, id: int, caption: Optional[str]) -> None:
        await self.col.update_one({'id': id}, {'$set': {'caption': caption}})

    async def get_caption(self, id: int) -> Optional[str]:
        user = await self.col.find_one({'id': id})
        return user.get('caption', None)

    async def get_user_data(self, id: int) -> Union[dict, None]:
        user = await self.col.find_one({'id': id})
        return user or None


db = Database(Config.MONGODB_URI, "Rename-Bot")
        
