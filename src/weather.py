import requests
import sys
import datetime

DEG = u'\N{DEGREE SIGN}'

class CityWeather:
    city = None
    temp = None
    api = None
    weather = None
    forecast = {}
    sunrise = 0
    sunset = 0
    units = 'F'
    date = None

    def __init__(self, city, api, **kwargs):
        # set variables
        self.city = city
        self.api = api
        self.date = datetime.datetime.now()
        if 'units' in kwargs.keys():
            if kwargs['units'] == 'metric':
                self.units = 'C'
        # get the weather info from the given api.
        self.updateForecast()
        self.updateCurrentWeather()


    def getForecast(self):
        return self.forecast

    def getCurrentWeather(self):
        return self.weather

    def updateForecast(self):
        forecast = self.api.getForecast()
        if len(forecast['days']) > 0:
            self.forecast = forecast

    def updateCurrentWeather(self):
        weather = self.api.getWeather()
        if len(weather) > 0:
            self.weather = weather
            self.temp = f"{int(weather['main']['temp'])}{DEG} {self.units}"
            s = datetime.datetime.fromtimestamp(weather['sys']['sunrise'])
            self.sunrise = f'{s.hour}:{s.minute}'
            if s.minute < 10:
                self.sunrise = f'{s.hour}:0{s.minute}'
            s = datetime.datetime.fromtimestamp(weather['sys']['sunset'])
            self.sunset = f'{s.hour}:{s.minute}'
            if s.minute < 10:
                self.sunset = f'{s.hour}:0{s.minute}'

    def updateData(self):
        self.updateForecast()
        self.updateCurrentWeather()

    def formatWeather(self, output='dzen'):
        date = f"{self.city}\n{self.date:%A, %B %d}"
        temps = f"{self.temp}"
        return f"{date}\n{temps}"

    def formatForecast(self, output='dzen'):
        strings = []
        i = 0
        for key,day in self.forecast['days'].items():
            d = datetime.datetime.strptime(day['date'], '%Y-%m-%d')
            line = f"{d:%A, %b %d}\n" \
                f"High: {day['high']:.0f}{DEG} {self.units} " \
                f"Low: {day['low']:.0f}{DEG} {self.units}\n" \
                f"{day['conditions']['description'].upper()}\n"
            strings.append(line)
            i += 1
        return '\n'.join(strings)

    def gtkWeatherString(self):
        date = f"<span font='16'>{self.weather['name']}\n{self.date.strftime('%A, %B %d')}</span>"
        temps = f"<span font='24'>{self.temp}</span>"
        return f"{date}\n{temps}\n"

    def gtkForecastString(self):
        string = []
        for key,day in self.forecast['days'].items():
            temps = f"<span>High: {day['high']:.0f}{DEG} - Low: {day['low']:.0f}{DEG}</span>"
            conditions = f"<span>{day['conditions']['description'].upper()}</span>"
            d = datetime.datetime.strptime(day['date'].split(' ')[0], '%Y-%m-%d')
            date = f"<span>{d.strftime('%A, %b %d')}</span>"
            string.append(f"{date}\n{temps}\n{conditions}\n")
        return '\n'.join(string)


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
            if key in ['weather', 'main', 'id', 'wind', 'name', 'coord', 'sys']:
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
                    'date': hour['dt_txt'].split(' ')[0],
                }
        d = str(datetime.datetime.now().day)
        if d in data['days'].keys():
            del data['days'][d]
        return data
