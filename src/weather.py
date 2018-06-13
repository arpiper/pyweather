import requests
import sys

class CityWeather:
    city = None
    temp = None
    api = None
    forecast = []

    def __init__(self, city, api):
        self.city = city
        self.api = api

    def getForecast(self):
        return self.api.getForecast()

    def getCurrentWeather(self):
        return self.api.getWeather()


class OpenWeatherMap:
    APPID = None
    key = None
    base = 'http://api.openweathermap.org/data/2.5/'
    units = 'imperial' # default to fahrenheit
    mode = 'json'
    city = None
    city_id = None

    def __init__(self, key, **kwargs):
        self.key = key
        self.APPID = f'APPID={key}'
        if 'city_id' in kwargs.keys():
            self.city_id = kwargs['city_id']
        elif 'city' in kwargs.keys():
            self.city = kwargs['city']
        else:
            sys.exit('city or city_id are required arguments')
        if 'units' in kwargs.keys():
            self.units = kwargs['units']

    def weather(self):
        if self.city_id:
            q = f'id={self.city_id}'
        else:
            q = f'q={self.city}'
        return f'{self.base}weather?{q}&mode={self.mode}&units={self.units}&{self.APPID}'

    def forecast(self):
        if self.city_id:
            q = f'id={self.city_id}'
        else:
            q = f'q={self.city}'
        return f'{self.base}forecast?{q}&mode={self.mode}&units={self.units}&{self.APPID}'

    def getWeather(self):
        res = requests.get(self.weather())
        data = {}
        for key,value in res.json().items():
            if key in ['weather', 'main', 'id', 'wind', 'name', 'coord',]:
                data[key] = value
        return data

    def getForecast(self):
        res = requests.get(self.forecast()).json()
        data = {
            'city': res['city'],
            'days': {},
        }
        for hour in res['list']:
            day = hour['dt_txt'].split(' ')[0].split('-')[2]
            if day in data['days'].keys():
                if data['days'][day]['high'] < hour['main']['temp_max']:
                    data['days'][day]['high'] = hour['main']['temp_max']
                if data['days'][day]['low'] > hour['main']['temp_min']:
                    data['days'][day]['low'] = hour['main']['temp_min']
            else:
                data['days'][day] = {
                    'high': hour['main']['temp_max'],
                    'low': hour['main']['temp_min'],
                    'humidity': hour['main']['humidity'],
                    'pressure': hour['main']['pressure'],
                    'conditions': hour['weather'][0],
                    'date': hour['dt_txt'],
                }
        return data
