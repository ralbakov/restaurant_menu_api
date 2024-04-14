from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.database.confdb import get_db
from menu_restaurant.database.models import Dishes, Submenus
from menu_restaurant.database.schemas import DishesCreate, DishesUpdate


class DishRepository:
    '''Репозиторий для работы с базой данных блюда'''

    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session = session
        self.model = Dishes
        self.submenu = Submenus

    async def check_exist(self,
                          target_menu_id: str,
                          target_submenu_id: str,
                          data: DishesCreate | DishesUpdate) -> Dishes | None:
        '''Проверяет наличие блюда с переданными названием в базе данных'''
        result = await self.session.execute(
            select(self.model).join(self.submenu).where(
                self.submenu.id == target_submenu_id,
                self.submenu.target_menu_id == target_menu_id,
                self.model.title == data.title)
        )
        if result.one_or_none() is not None:
            raise ValueError('dish with title alredy exist ')
        return None

    async def create(self, target_menu_id: str, target_submenu_id: str, data: DishesCreate) -> Dishes:
        '''Создает блюда'''
        await self.check_exist(target_menu_id, target_submenu_id, data)
        result = self.model(target_submenu_id=target_submenu_id, **data.model_dump())
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def read(self, target_dish_id: str) -> Dishes:
        '''Получает блюда'''
        result = await self.session.get(self.model, target_dish_id)
        if result is None:
            raise AttributeError('dish not found')
        return result

    async def update(self,
                     target_menu_id: str,
                     target_submenu_id: str,
                     target_dish_id: str,
                     data: DishesUpdate) -> Dishes:
        '''Обновляет блюда'''
        result = await self.read(target_dish_id)
        await self.check_exist(target_menu_id, target_submenu_id, data)
        result.title = data.title
        result.description = data.description
        result.price = data.price
        self.session.add(result)
        await self.session.merge(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def delete(self, target_dish_id: str) -> None:
        '''Удаляет блюда'''
        result = await self.read(target_dish_id)
        await self.session.delete(result)
        await self.session.commit()

    async def read_all(self, target_menu_id: str, target_submenu_id: str) -> list[Dishes] | list[None]:
        '''Получает все блюда'''
        result = await self.session.execute(
            select(self.model).where(
                self.model.target_submenu_id == target_submenu_id,
                self.submenu.target_menu_id == target_menu_id)
        )
        return result.all()
