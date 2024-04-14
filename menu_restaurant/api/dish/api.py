from fastapi import APIRouter, Depends, HTTPException

from menu_restaurant.database.schemas import Dishes, DishesCreate, DishesUpdate

from ..dish.service import DishService

dish_router = APIRouter(prefix=('/api/v1/menus'
                                '/{target_menu_id}'
                                '/submenus/{target_submenu_id}/dishes'))


@dish_router.get('',
                 name='Просматривает список блюд',
                 status_code=200,
                 response_model=list[Dishes],
                 tags=['Dish']
                 )
async def get_all_dish(target_menu_id: str,
                       target_submenu_id: str,
                       service: DishService = Depends()
                       ):
    return await service.read_all(target_menu_id, target_submenu_id)


@dish_router.post('',
                  name='Создает блюдо',
                  status_code=201,
                  response_model=Dishes,
                  tags=['Dish']
                  )
async def post_dish(target_menu_id: str,
                    target_submenu_id: str,
                    data: DishesCreate,
                    service: DishService = Depends()
                    ):
    try:
        return await service.create(target_menu_id, target_submenu_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@dish_router.get('/{target_dish_id}',
                 name='Просматривает определенное блюдо',
                 status_code=200,
                 response_model=Dishes,
                 tags=['Dish']
                 )
async def get_dish(target_menu_id: str,
                   target_submenu_id: str,
                   target_dish_id: str,
                   service: DishService = Depends()
                   ):
    try:
        return await service.read(target_menu_id, target_submenu_id, target_dish_id)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@dish_router.patch('/{target_dish_id}',
                   name='Обновляет блюдо',
                   response_model=Dishes,
                   tags=['Dish']
                   )
async def patch_dish(target_menu_id: str,
                     target_submenu_id: str,
                     target_dish_id: str,
                     data: DishesUpdate,
                     service: DishService = Depends()
                     ):
    try:
        return await service.update(target_menu_id, target_submenu_id, target_dish_id, data)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@dish_router.delete('/{target_dish_id}',
                    name='Удаляет блюдо',
                    tags=['Dish']
                    )
async def delete_dish(target_menu_id: str,
                      target_submenu_id: str,
                      target_dish_id: str,
                      service: DishService = Depends()
                      ):
    try:
        return await service.delete(target_menu_id, target_submenu_id, target_dish_id)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
