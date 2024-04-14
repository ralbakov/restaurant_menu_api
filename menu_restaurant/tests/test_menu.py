from httpx import AsyncClient

from ..tests.reverse import reverse

save_data = {}


async def test_get_empty_menus(ac_client: AsyncClient):
    """Тестирует пустой список меню."""

    response = await ac_client.get(
        reverse('Просматривает список меню')
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


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


async def test_get_menus(ac_client: AsyncClient):
    """Тестирует непустой список меню."""

    response = await ac_client.get(
        reverse('Просматривает список меню')
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data != []


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
    assert data['id'] == f'{target_menu_id}'


async def test_update_menu(ac_client: AsyncClient):
    """Тестирует обновление меню."""

    target_menu_id = save_data['id']
    response = await ac_client.patch(
        reverse('Обновляет меню',
                **{'target_menu_id': target_menu_id}),
        json={
            'title': 'My updated menu 1',
            'description': 'My updated menu description 1'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My updated menu 1'
    assert data['description'] == 'My updated menu description 1'
    assert data['id'] == f'{target_menu_id}'


async def test_delete_menu(ac_client: AsyncClient):
    """Тестирует удаление меню."""

    target_menu_id = save_data['id']
    response = await ac_client.delete(
        reverse('Удаляет меню',
                **{'target_menu_id': target_menu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


async def test_get_menu_deleted(ac_client: AsyncClient):
    """Тестирует просмотр удаленного меню."""

    target_menu_id = save_data['id']
    response = await ac_client.get(
        reverse('Просматривает определенное меню',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 404, response.text
    assert response.json()['detail'] == 'menu not found'
