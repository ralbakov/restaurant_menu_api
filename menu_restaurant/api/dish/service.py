from fastapi import Depends

from menu_restaurant.api.dish.repository import DishRepository
from menu_restaurant.database.models import Dishes
from menu_restaurant.database.redis_tools import RedisCache
from menu_restaurant.database.schemas import DishesCreate, DishesUpdate


class DishService:
    '''Сервисный слой для работы с репозиторием и кэшем блюда'''

    def __init__(self, cache: RedisCache = Depends(), crud_db: DishRepository = Depends()) -> None:
        self.crud_db = crud_db
        self.cache = cache

    async def create(self, target_menu_id: str, target_submenu_id: str, data: DishesCreate) -> Dishes:
        result = await self.crud_db.create(target_menu_id, target_submenu_id, data)
        await self.cache.set_dish_cache(target_menu_id=target_menu_id,
                                        target_submenu_id=target_submenu_id,
                                        target_dish_id=str(result.id),
                                        dish=result)
        return result

    async def update(self,
                     target_menu_id: str,
                     target_submenu_id: str,
                     target_dish_id: str,
                     data: DishesUpdate) -> Dishes | None:
        result = await self.crud_db.update(target_menu_id, target_submenu_id, target_dish_id, data)
        await self.cache.update_dish_cache(target_submenu_id=target_submenu_id,
                                           target_dish_id=target_dish_id,
                                           dish=result)
        return result

    async def delete(self, target_menu_id: str, target_submenu_id: str, target_dish_id: str) -> None:
        await self.crud_db.delete(target_dish_id)
        await self.cache.delete_dish_cache(target_menu_id, target_submenu_id, target_dish_id)

    async def read(self, target_menu_id: str, target_submenu_id: str, target_dish_id: str) -> Dishes:
        if target_dish_id in await self.cache.get_all_keys_dishes(target_submenu_id):
            result = await self.cache.get_dish_cache(target_submenu_id, target_dish_id)
            return result
        result = await self.crud_db.read(target_dish_id)
        await self.cache.set_dish_cache(target_menu_id=target_menu_id,
                                        target_submenu_id=target_submenu_id,
                                        target_dish_id=str(result.id),
                                        dish=result)
        return result

    async def read_all(self, target_menu_id: str, target_submenu_id: str) -> list[Dishes] | list[None]:
        result = await self.cache.get_all_dish_cache(target_submenu_id)
        if result is not None:
            return result
        result = await self.crud_db.read_all(target_menu_id, target_submenu_id)
        return result
