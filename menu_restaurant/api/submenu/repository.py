from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.database.confdb import get_db
from menu_restaurant.database.models import Submenus
from menu_restaurant.database.schemas import SubmenusCreate, SubmenusUpdate


class SubmenuRepository:
    '''Репозиторий для работы с базой данных подменю'''

    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session = session
        self.model = Submenus

    async def check_exist(self, target_menu_id: str, data: SubmenusCreate | SubmenusUpdate) -> Submenus | None:
        '''Проверяет наличие подменю с переданными названием в базе данных'''
        result = await self.session.execute(
            select(self.model).where(
                self.model.target_menu_id == target_menu_id,
                self.model.title == data.title)
        )
        if result.one_or_none() is not None:
            raise ValueError('submenu with title alredy exist ')
        return None

    async def create(self, target_menu_id: str, data: SubmenusCreate) -> Submenus:
        '''Создает подменю'''
        await self.check_exist(target_menu_id, data)
        result = self.model(target_menu_id=target_menu_id, **data.model_dump())
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def read(self, target_submenu_id: str) -> Submenus:
        '''Получает подменю'''
        result = await self.session.get(self.model, target_submenu_id)
        if result is None:
            raise AttributeError('submenu not found')
        return result

    async def update(self, target_menu_id: str, target_submenu_id: str, data: SubmenusUpdate) -> Submenus:
        '''Обновляет подменю'''
        result = await self.read(target_submenu_id)
        await self.check_exist(target_menu_id, data)
        result.title = data.title
        result.description = data.description
        self.session.add(result)
        await self.session.merge(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def delete(self, target_submenu_id: str) -> None:
        '''Удаляет подменю'''
        result = await self.read(target_submenu_id)
        await self.session.delete(result)
        await self.session.commit()

    async def read_all(self, target_menu_id: str) -> list[Submenus] | list[None]:
        '''Получает все подменю'''
        result = await self.session.execute(select(self.model).where(self.model.target_menu_id == target_menu_id))
        return result.all()
