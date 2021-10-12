# "Журнал погоды"

## Используемые технологии
![](https://img.shields.io/badge/Python3-mediumblue) ![](https://img.shields.io/badge/Django-purple) ![](https://img.shields.io/badge/DRF-Lime) ![](https://img.shields.io/badge/Celery-gold) ![](https://img.shields.io/badge/Docker-red)


## Описание проекта
Сервис предназначен для ведения журнала метеонаблюдений и предоставления информации клиентам сервиса.  
Для актуализации архива погоды сервис каждые 30 минут осуществляет опрос двух внешних API [openweathermap.org](https://openweathermap.org/), [www.weatherbit.io](https://www.weatherbit.io), предоставляющих последнюю доступную информацию о погоде в запрошенных городах.  
Список городов для которых ведется журнал метеонаблюдений определятся перечнем внесенным в базу данных проекта. Список городов может быть изменен через административную панель Django-проекта.  
Клиентам сервиса при обращении к эндпоиту ```http://<you_host>/api/v1/weather/``` возвращаются данные содержащие
* название города,
* географические широта и долгота города,
* температура,
* дата и время наблюдения,
* источник информации о погоде.

### Запросы к API "Журнала погоды"
Данные отправляемые клиенту при обращении к эндпоиту ```http://<you_host>/api/v1/weather/``` имеют следующую структуру:
```json
{
    "count": 26,
    "next": "http://<you_host>/api/v1/weather/?page=2&source=openweathermap",
    "previous": null,
    "results": [
        {
            "city_name": "Moscow",
            "longitude": 37.606667,
            "latitude": 55.761665,
            "temperature": 12.3,
            "datetime": "2021-10-12T13:02:34+03:00",
            "source": "openweathermap"
        },
        ...
    ]
}
```
При обращении к ```http://<you_host>/api/v1/weather/``` могут быть указаны несколько необязательныx параметров:

Параметр запроса | Признак фильтрации | Допустимые значения
--- | --- | --- 
`source` | источники данных о погоде | `openweathermap`, `weatherbit`
`city_name` | города |  Названия городов на транслите. Например: `sochi`.
`datetime_after` | начальные дата и время метеонаблюдений | Например: `2021-10-09` или `2021-10-09T14:01`
`datetime_before` | конечные дата и время метеонаблюдений | Например: `2021-10-12` или `2021-10-12T22:01` 
`page` | номер страницы результата | Целое число

Пример запроса: `http://<your_host>/api/v1/weather/?source=openweathermap&city_name=Sochi&city_name=Moscow&datetime_after=2021-10-12T13:44`

### Добавление городов в БД
Для внесения городов в базу данных необходимо указать следующие данные:  
* ID города;
* название города;
* географические широта и долгота;
* часовой пояс.

Все перечисленные параметры должны быть взяты из файлов доступных для скачивания по ссылкам:  
* https://www.weatherbit.io/static/exports/stations_current.csv.gz;
* http://bulk.openweathermap.org/sample/city.list.json.gz.

## Как развернуть
Для развертывания проекта описанным ниже способом на базе Linux должны быть установлены и включены утилиты docker и docker-compose. Для развертывания на базе Windows10 должны быть установлены запущены WSL2 и Docker-desktop.

1. Склонируйте репозиторий: ```https://github.com/palmage/api_weather```.
2. В корневую директорию добавьте файл ```.env``` и заполните его следующими переменными окружения:
```PowerShell
DJANGO_SECRET_KEY='<your_django_secret_key>'
KEY_WEATHERBIT = '<your_key_for_openweathermap.org>'
KEY_OPENWEATHERMAP = '<your_key_for_www.weatherbit.io>'
```  
*с целью демонстрации проекта заполненный файл .env умышлено сохранен в публичном доступе

3. Из корневой директории проекта выполните команду ```sudo docker-compose up --build```.  
4. Примените миграции: ```sudo docker-compose exec web python manage.py migrate --noinput```.  
5. Для наполнения БД начальными данными выполните команды:

``` PowerShell
sudo docker-compose exec web python manage.py loaddata dump.json
```  
6. Создайте суперпользователя: ```sudo docker-compose exec web python manage.py createsuperuser```. После развертывания проекта сайт администратора будет доступен по адресу: http://<your_host>/admin/.  
