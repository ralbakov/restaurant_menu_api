import typing

from menu_restaurant.main import app


def reverse(name: str, **path_params: typing.Any) -> str:
    """Функция для возврата пути 'endpoint'"""

    return app.url_path_for(name, **path_params)
