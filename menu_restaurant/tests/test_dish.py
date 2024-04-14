from httpx import AsyncClient

from ..tests.reverse import reverse

save_data = {}


async def test_create_menu(ac_client: AsyncClient):
    """Тестирует создание меню."""

    response = await ac_client.post(
        reverse('Создает меню'),
        json={
            'title': 'My menu 1',
            'description': 'My menu description 1'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    save_data['id'] = data['id']
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    assert data['id'] == save_data['id']


async def test_create_submenu(ac_client: AsyncClient):
    """Тестирует создание субменю."""

    target_menu_id = save_data['id']
    response = await ac_client.post(
        reverse('Создает подменю',
                **{'target_menu_id': target_menu_id}),
        json={
            'title': 'My submenu 1',
            'description': 'My submenu description 1'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    save_data['sub_id'] = data['id']
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'
    assert data['id'] == save_data['sub_id']


async def test_get_empty_dishes(ac_client: AsyncClient):
    """Тестирует просмотр пустых блюд (когда еще нет блюд)."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.get(
        reverse('Просматривает список блюд',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


async def test_create_dish(ac_client: AsyncClient):
    """Тестирует создание блюда."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.post(
        reverse('Создает блюдо',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
        json={
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    save_data['dis_id'] = data['id']
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'
    assert data['id'] == save_data['dis_id']


async def test_get_dishes(ac_client: AsyncClient):
    """Тестирует просмотр, когда список блюд непустой."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.get(
        reverse('Просматривает список блюд',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}
                ),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data != []


async def test_get_dish(ac_client: AsyncClient):
    """Тестирует просмотр блюда."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    target_dish_id = save_data['dis_id']
    response = await ac_client.get(
        reverse('Просматривает определенное блюдо',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id,
                   'target_dish_id': target_dish_id}
                )
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'
    assert data['id'] == target_dish_id


async def test_update_dish(ac_client: AsyncClient):
    """Тестирует обновление блюда."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    target_dish_id = save_data['dis_id']
    response = await ac_client.patch(
        reverse('Обновляет блюдо',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id,
                   'target_dish_id': target_dish_id}
                ),
        json={
            'title': 'My updated dish 1',
            'description': 'My updated dish description 1',
            'price': '14.50'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My updated dish 1'
    assert data['description'] == 'My updated dish description 1'
    assert data['price'] == '14.50'
    assert data['id'] == target_dish_id


async def test_delete_dish(ac_client: AsyncClient):
    """Тестирует удаление блюда."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    target_dish_id = save_data['dis_id']
    response = await ac_client.delete(
        reverse('Удаляет блюдо',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id,
                   'target_dish_id': target_dish_id}
                ),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


async def test_get_dish_deleted(ac_client: AsyncClient):
    """Тестирует просмотр удаленного блюда."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    target_dish_id = save_data['dis_id']
    response = await ac_client.get(
        reverse('Просматривает определенное блюдо',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id,
                   'target_dish_id': target_dish_id}
                ),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 404, response.text
    assert response.json()['detail'] == 'dish not found'


async def test_delete_submenu(ac_client: AsyncClient):
    """Тестирует удаление субменю."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.delete(
        reverse('Удаляет подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}
                ),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


async def test_delete_menu(ac_client: AsyncClient):
    """Тестирует удаление меню."""

    target_menu_id = save_data['id']
    response = await ac_client.delete(
        reverse('Удаляет меню',
                **{'target_menu_id': target_menu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
