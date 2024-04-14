from httpx import AsyncClient

from ..tests.reverse import reverse

save_data = {}


async def test_create_menu(ac_client: AsyncClient):
    """Тестирует создание меню."""

    response = await ac_client.post(
        url=reverse('Создает меню'),
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


async def test_create_dish_first(ac_client: AsyncClient):
    """Тестирует создание 1-го блюда."""

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


async def test_create_dish_second(ac_client: AsyncClient):
    """Тестирует создание 2-го блюда."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.post(
        reverse('Создает блюдо',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
        json={
            'title': 'My dish 2',
            'description': 'My dish description 2',
            'price': '13.50'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    save_data['dis_id'] = data['id']
    assert data['title'] == 'My dish 2'
    assert data['description'] == 'My dish description 2'
    assert data['price'] == '13.50'
    assert data['id'] == save_data['dis_id']


async def test_get_submenu_dish_count(ac_client: AsyncClient):
    """Тестирует просмотр определенного меню с количеством субменю и блюд."""

    target_menu_id = save_data['id']
    response = await ac_client.get(
        reverse('Просматривает определенное меню',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == target_menu_id
    assert data['submenus_count'] == 1
    assert data['dishes_count'] == 2
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'


async def test_get_dish_count(ac_client: AsyncClient):
    """Тестирует просмотр определенного субменю с количеством блюд."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.get(
        reverse('Просматривает определенное подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == target_submenu_id
    assert data['dishes_count'] == 2


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


async def test_get_submenus(ac_client: AsyncClient):
    """Тестирует список субменю."""

    target_menu_id = save_data['id']
    response = await ac_client.get(
        reverse('Просматривает список подменю',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


async def test_get_empty_dishes(ac_client: AsyncClient):
    """Тестирует просмотр списка блюд."""

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
    assert data == []


async def test_get_one_menu(ac_client: AsyncClient):
    """Тестирует просмотр меню."""

    target_menu_id = save_data['id']
    response = await ac_client.get(
        reverse('Просматривает определенное меню',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    assert data['id'] == target_menu_id


async def test_delete_menu(ac_client: AsyncClient):
    """Тестирует удаление меню."""

    target_menu_id = save_data['id']
    response = await ac_client.delete(
        reverse('Удаляет меню',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


async def test_get_empty_menus(ac_client: AsyncClient):
    """Тестирует пустой список меню."""

    response = await ac_client.get(
        reverse('Просматривает список меню'),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []
