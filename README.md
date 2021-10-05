# web-backend
## Запуск тестов:

Из корневой папки проекта выполняем команду
1) для юнит-тестов
```./manage.py test points/unit_tests/```
  
2) для интеграционных 
```./manage.py test points/integration_tests/```
  

## Добавляение данных для GraphQL
Чтобы прротестировать работу эндпоинтов GraphQL можно заполнить таблицу данными с помощью 

```./manage.py loaddata models.json```
