from fastapi import Depends

from menu_restaurant.api.submenu.repository import SubmenuRepository
from menu_restaurant.database.models import Submenus
from menu_restaurant.database.redis_tools import RedisCache
from menu_restaurant.database.schemas import SubmenusCreate, SubmenusUpdate


class SubmenuService:
    '''Сервисный слой для работы с репозиторием и кэшем подменю'''

    def __init__(self, cache: RedisCache = Depends(), crud_db: SubmenuRepository = Depends()) -> None:
        self.crud_db = crud_db
        self.cache = cache

    async def create(self, target_menu_id: str, data: SubmenusCreate) -> Submenus:
        result = await self.crud_db.create(target_menu_id, data)
        await self.cache.set_submenu_cache(target_menu_id=target_menu_id,
                                           target_submenu_id=str(result.id),
                                           submenu=result)
        return result

    async def update(self, target_menu_id: str, target_submenu_id: str, data: SubmenusUpdate) -> Submenus | None:
        result = await self.crud_db.update(target_menu_id, target_submenu_id, data)
        await self.cache.update_submenu_cache(target_menu_id=target_menu_id,
                                              target_submenu_id=target_submenu_id,
                                              submenu=result)
        return result

    async def delete(self, target_menu_id: str, target_submenu_id: str) -> None:
        await self.crud_db.delete(target_submenu_id)
        await self.cache.delete_submenu_cache(target_menu_id, target_submenu_id)

    async def read(self, target_menu_id: str, target_submenu_id: str) -> Submenus:
        if target_submenu_id in await self.cache.get_all_keys_submenu(target_menu_id):
            result = await self.cache.get_submenu_cache(target_menu_id, target_submenu_id)
            return result
        result = await self.crud_db.read(target_submenu_id)
        await self.cache.set_submenu_cache(target_menu_id=target_menu_id,
                                           target_submenu_id=target_submenu_id,
                                           submenu=result)
        return result

    async def read_all(self, target_menu_id) -> list[Submenus] | list[None]:
        result = await self.cache.get_all_submenu_cache(target_menu_id)
        if result is not None:
            return result
        result = await self.crud_db.read_all(target_menu_id)
        return result
