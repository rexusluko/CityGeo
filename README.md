# Первоначальные настройки
Создать .env файл в корневой директории проекта с содержимым
```
POSTGRES_DB = example_db
POSTGRES_USER = example_user
POSTGRES_PASSWORD = example_password
GRAPHHOPPER_KEY = example_key
```
# Запуск приложения
С помощью консоли перейти в корневую директорию и выполнить
```
docker-compose up
```
После этого нужно подключиться к контейнеру и выполнить команду для создания администратора
```
docker exec -it {container_id} python citygeo/manage.py createsuperuser
```
Документация находится по адресу
```
http://127.0.0.1:8000/api/docs/
```