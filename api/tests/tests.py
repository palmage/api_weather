from django.core.management import call_command
from django.test import Client, TestCase


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'api/tests/testdata.json')
        cls.guest_client = Client()

    def test_get_weather(self):
        '''Эндпоинт /api/v1/weather/ доступен любому пользователю'''
        response = URLTests.guest_client.get('/api/v1/weather/')
        self.assertEqual(
            response.status_code, 200,
            'Эндпоинт /api/v1/weather/ не доступен'
        )
        response = URLTests.guest_client.get(
            '/api/v1/weather/?page=1&city_name=Sochi&city_name=Moscow'
            '&datetime_after=2021-10-05 14:01&datetime_before=2021-10-05 23:00'
        )
        self.assertEqual(
            response.status_code, 200,
            'Эндпоинт c параметрами '
            '/api/v1/weather/?city_name=Sochi&city_name=Moscow'
            '&datetime_after=2021-10-05 14:01&datetime_before=2021-10-05 23:00'
            'не доступен'
        )


class ListWeatherWiewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'api/tests/testdata.json')
        cls.guest_client = Client()

    def test_data(self):
        '''Ресурс /api/v1/weather/ имеет правильную схему данных'''
        response = ListWeatherWiewTests.guest_client.get('/api/v1/weather/')
        data = response.data
        self.assertTrue(
            data.__contains__('results'),
            'Response.data \'/api/v1/weather/\' не содержит атрибута results'
        )
        self.assertIsInstance(
            data['results'], list,
            'results должен быть экземпляром list'
        )
        weathes_attributes = {
            'city_name': "Novosibirsk",
            'longitude': 82.934441,
            'latitude': 55.041111,
            'temperature': -1.2,
            'datetime': "2021-10-06T22:22:00+03:00",
            'source': "openweathermap"
        }
        weather = data['results'][0]
        for attribute, value in weathes_attributes.items():
            with self.subTest(attribute=attribute):
                self.assertTrue(
                    weather.get(attribute, False),
                    f'В экзкмплярах списка resualts \'/api/v1/weather/\' '
                    f'отсутствует атрибут {attribute}'
                )
                self.assertEqual(
                    value, weather[attribute],
                    f'Атрибут {attribute}, для последней записи '
                    'принимает неверное значение'
                )

    def test_pagination(self):
        '''Пагинация /api/v1/weather/ работает корректно'''
        attributes = {
            'count': 41,
            'next': 'http://testserver/api/v1/weather/?page=2',
            'previous': None,
        }
        response = ListWeatherWiewTests.guest_client.get('/api/v1/weather/')
        data = response.data
        for attribute, value in attributes.items():
            with self.subTest(attribute=attribute):
                self.assertTrue(
                    data.__contains__(attribute),
                    f'Response.data \'/api/v1/weather/\' '
                    f'не содержит атрибута {attribute}'
                )
                self.assertEqual(
                    value, data[attribute],
                    f'Атриббут {attribute} принимает неверное значение'
                )
        self.assertEqual(
            len(data['results']), 20,
            'Проверте коректность работы пагинатора'
        )
        response = ListWeatherWiewTests.guest_client.get(
            '/api/v1/weather/?page=3'
        )
        self.assertEqual(
            len(response.data['results']), 1,
            'Проверте коректность работы пагинатора'
        )

    def test_sort(self):
        response = ListWeatherWiewTests.guest_client.get('/api/v1/weather/')
        previous_datetime = '3000-10-06T22:22:00+03:00'
        for current_weather in response.data['results']:
            self.assertTrue(
                current_weather['datetime'] <= previous_datetime,
                'Убедитесь, что список погоды отсортированн по дате'
            )
            previous_datetime = current_weather['datetime']

    def test_filters(self):
        response = ListWeatherWiewTests.guest_client.get(
            '/api/v1/weather/?city_name=Sochi&city_name=Moscow'
            '&datetime_after=2021-10-05 14:01&datetime_before=2021-10-05 23:00'
        )
        for current_weather in response.data['results']:
            self.assertTrue(
                '2021-10-05T14:01+03:00' <= current_weather['datetime'] <= '2021-10-05T23:00+03:00',
                'Убедитесь, что фильтрация по дате работает'
            )
            self.assertIn(
                current_weather['city_name'], ('Moscow', 'Sochi'),
                'Убедитесь, что фильтрация по городам работает'
            )
        response = ListWeatherWiewTests.guest_client.get(
            '/api/v1/weather/?source=openweathermap'
        )
        for current_weather in response.data['results']:
            self.assertEqual(
                current_weather['source'], 'openweathermap',
                'Убедитесь, что фильтрация по источнуку '
                'данных о погоде работает'
            )
