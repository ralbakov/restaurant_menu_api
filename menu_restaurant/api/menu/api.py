from fastapi import APIRouter, Depends, HTTPException

from menu_restaurant.database.schemas import Menus, MenusCreate, MenusUpdate

from ..menu.service import MenuService

menu_router = APIRouter(prefix='/api/v1/menus')


@menu_router.post('',
                  status_code=201,
                  name='Создает меню',
                  response_model=Menus,
                  tags=['Menu'],
                  )
async def post_menu(data: MenusCreate, service: MenuService = Depends()):
    try:
        return await service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@menu_router.get('',
                 name='Просматривает список меню',
                 response_model=list[Menus],
                 status_code=200,
                 tags=['Menu']
                 )
async def get_all_menu(service: MenuService = Depends()):
    return await service.read_all()


@menu_router.get('/{target_menu_id}',
                 name='Просматривает определенное меню',
                 response_model=Menus,
                 status_code=200,
                 tags=['Menu']
                 )
async def get_menu(target_menu_id: str, service: MenuService = Depends()):
    try:
        return await service.read(target_menu_id)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@menu_router.patch('/{target_menu_id}',
                   name='Обновляет меню',
                   response_model=Menus,
                   status_code=200,
                   tags=['Menu']
                   )
async def patch_menu(target_menu_id: str, data: MenusUpdate, service: MenuService = Depends()):
    try:
        return await service.update(target_menu_id, data)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@menu_router.delete('/{target_menu_id}',
                    name='Удаляет меню',
                    response_model=None,
                    status_code=200,
                    tags=['Menu']
                    )
async def delete_menu(target_menu_id: str, service: MenuService = Depends()):
    try:
        return await service.delete(target_menu_id)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
