from fastapi import Depends

from menu_restaurant.api.menu.repository import MenuRepository
from menu_restaurant.database.models import Menus
from menu_restaurant.database.redis_tools import RedisCache
from menu_restaurant.database.schemas import MenusCreate, MenusUpdate


class MenuService:
    '''Сервисный слой для работы с репозиторием и кэшем меню'''

    def __init__(self, cache: RedisCache = Depends(), crud_db: MenuRepository = Depends()) -> None:
        self.crud_db = crud_db
        self.cache = cache

    async def create(self, data: MenusCreate) -> Menus:
        result = await self.crud_db.create(data)
        await self.cache.set_menu_cache(target_menu_id=str(result.id), menu=result)
        return result

    async def update(self, target_menu_id: str, data: MenusUpdate) -> Menus:
        result = await self.crud_db.update(target_menu_id, data)
        await self.cache.update_menu_cache(target_menu_id=target_menu_id, menu=result)
        return result

    async def delete(self, target_menu_id: str) -> None:
        await self.crud_db.delete(target_menu_id)
        await self.cache.delete_menu_cache(target_menu_id)

    async def read(self, target_menu_id: str) -> Menus | AttributeError:
        if target_menu_id in await self.cache.get_all_keys_menu():
            result = await self.cache.get_menu_cache(target_menu_id)
            return result
        result = await self.crud_db.read(target_menu_id)
        await self.cache.set_menu_cache(target_menu_id=str(result.id), menu=result)
        return result

    async def read_all(self) -> list[Menus] | list[None]:
        result = await self.cache.get_all_menu_cache()
        if result is not None:
            return result
        result = await self.crud_db.read_all()
        return result
