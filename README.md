# Rest API приложение для работы с меню ресторана

## Стек

API - FlaskAPI  \
ORM - sqlalchemy  \
БД - PostgreSQL  \
Тестирование - pytest  \
DevOps - Docker \
Cache - Redis

## Копирование репозитория

```bash
git clone https://github.com/ralbakov/restaurant_menu_api.git
```

```text
После завершения клонирования репозитория, необходимо перейти в папку "restaurant_menu_api".
Для этого в терминале выполните нижеуказанную команду:
```

```bash
cd restaurant_menu_api
```

## Запуск

### Основное приложение

```text
Находясь в папке "restaurant_menu_api", в командной строке выполните команду:
docker-compose -f prod.yml up
```

### Тестирование приложения

```text
Находясь в папке "restaurant_menu_api", в командной строке выполните команду:
docker-compose -f test.yml up
```
