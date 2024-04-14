from fastapi import APIRouter, Depends, HTTPException

from menu_restaurant.database.schemas import Submenus, SubmenusCreate, SubmenusUpdate

from ..submenu.service import SubmenuService

submenu_router = APIRouter(prefix=('/api/v1/menus'
                                   '/{target_menu_id}/submenus'))


@submenu_router.get('',
                    name='Просматривает список подменю',
                    status_code=200,
                    response_model=list[Submenus],
                    tags=['Submenu']
                    )
async def get_all_submenu(target_menu_id: str,
                          service: SubmenuService = Depends()
                          ):
    return await service.read_all(target_menu_id)


@submenu_router.post('',
                     name='Создает подменю',
                     status_code=201,
                     response_model=Submenus,
                     tags=['Submenu']
                     )
async def post_submenu(target_menu_id: str,
                       data: SubmenusCreate,
                       service: SubmenuService = Depends()
                       ):
    try:
        return await service.create(target_menu_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@submenu_router.get('/{target_submenu_id}',
                    name='Просматривает определенное подменю',
                    status_code=200,
                    response_model=Submenus,
                    tags=['Submenu']
                    )
async def get_submenu(target_menu_id: str,
                      target_submenu_id: str,
                      service: SubmenuService = Depends()
                      ):
    try:
        return await service.read(target_menu_id, target_submenu_id)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@submenu_router.patch('/{target_submenu_id}',
                      name='Обновляет подменю',
                      response_model=Submenus,
                      tags=['Submenu']
                      )
async def patch_submenu(target_menu_id: str,
                        target_submenu_id: str,
                        data: SubmenusUpdate,
                        service: SubmenuService = Depends()
                        ):
    try:
        return await service.update(target_menu_id, target_submenu_id, data)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@submenu_router.delete('/{target_submenu_id}',
                       name='Удаляет подменю', tags=['Submenu'])
async def delete_submenu(target_menu_id: str,
                         target_submenu_id: str,
                         service: SubmenuService = Depends()
                         ):
    try:
        return await service.delete(target_menu_id, target_submenu_id)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
