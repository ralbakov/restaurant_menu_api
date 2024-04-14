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


async def test_get_empty_submenus(ac_client: AsyncClient):
    """Тестирует пустой список субменю."""

    target_menu_id = save_data['id']
    response = await ac_client.get(
        reverse('Просматривает список подменю',
                **{'target_menu_id': target_menu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


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


async def test_get_submenus(ac_client: AsyncClient):
    """Тестирует непустой список субменю."""

    target_menu_id = save_data['id']
    response = await ac_client.get(
        reverse('Просматривает список подменю',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data != []


async def test_get_one_submenu(ac_client: AsyncClient):
    """Тестирует просмотр субменю."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.get(
        reverse('Просматривает определенное подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'
    assert data['id'] == target_submenu_id


async def test_update_submenu(ac_client: AsyncClient):
    """Тестирует обновление субменю."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.patch(
        reverse('Обновляет подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
        json={
            'title': 'My updated submenu 1',
            'description': 'My updated submenu description 1'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My updated submenu 1'
    assert data['description'] == 'My updated submenu description 1'
    assert data['id'] == target_submenu_id


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


async def test_get_submenu_deleted(ac_client: AsyncClient):
    """Тестирует просмотр удаленного субменю."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = await ac_client.get(
        reverse('Просматривает определенное подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 404, response.text
    assert response.json()['detail'] == 'submenu not found'


async def test_delete_menu(ac_client: AsyncClient):
    """Тестирует удаление меню."""

    target_menu_id = save_data['id']
    response = await ac_client.delete(
        reverse('Удаляет меню',
                **{'target_menu_id': target_menu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
