from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.database.confdb import get_db
from menu_restaurant.database.models import Menus
from menu_restaurant.database.schemas import MenusCreate, MenusUpdate


class MenuRepository:
    '''Репозиторий для работы с базой данных меню'''

    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session = session
        self.model = Menus

    async def check_exist(self, data: MenusCreate | MenusUpdate) -> None:
        '''Проверяет наличие меню с переданными названием в базе данных'''
        result = await self.session.execute(select(self.model).where(self.model.title == data.title))
        if result.one_or_none() is not None:
            raise ValueError('menu with title alredy exist ')
        return None

    async def create(self, data: MenusCreate) -> Menus:
        '''Создает меню'''
        await self.check_exist(data)
        result = self.model(**data.model_dump())
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def read(self, target_menu_id: str) -> Menus:
        '''Получает меню'''
        result = await self.session.get(self.model, target_menu_id)
        if result is None:
            raise AttributeError('menu not found')
        return result

    async def update(self, target_menu_id: str, data: MenusUpdate) -> Menus:
        '''Обновляет меню'''
        result = await self.read(target_menu_id)
        await self.check_exist(data)
        result.title = data.title
        result.description = data.description
        self.session.add(result)
        await self.session.merge(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def delete(self, target_menu_id: str) -> None:
        '''Удаляет меню'''
        result = await self.read(target_menu_id)
        await self.session.delete(result)
        await self.session.commit()

    async def read_all(self) -> list[Menus] | list[None]:
        '''Получает все меню'''
        result = await self.session.execute(select(self.model))
        return result.all()
