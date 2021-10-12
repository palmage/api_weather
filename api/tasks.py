from api_weather.celery import app

from .service import get_weather


@app.task
def update_weather():
    get_weather()
