import requests
import sys
import datetime
import fontawesome as fa

DEG = u'\N{DEGREE SIGN}'
ICON = {
    '01d': u"\uf00d",
    '01n': u"\uf02e",
    '02d': u"\uf00c",
    '02n': u"\uf083",
    '03d': u"\uf041",
    '03n': u"\uf041",
    '04d': u"\uf013",
    '04n': u"\uf013",
    '09d': u"\uf019",
    '09n': u"\uf019",
    '10d': u"\uf008",
    '10n': u"\uf028",
    '11d': u"\uf01e",
    '11n': u"\uf01e",
    '13d': u"\uf01b",
    '13n': u"\uf01b",
    '50d': u"\uf014",
    '50n': u"\uf014",
}


class CityWeather:
    city = None
    temp = None
    api = None
    weather = None
    forecast = {}
    sunrise = {}
    sunset = {}
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
            self.sunrise = {
                'hm': f'{s.hour}:{s.minute}',
                'utc': weather['sys']['sunrise'],
            }
            if s.minute < 10:
                self.sunrise['hm'] = f'{s.hour}:0{s.minute}'
            s = datetime.datetime.fromtimestamp(weather['sys']['sunset'])
            self.sunset = {
                'hm': f'{s.hour}:{s.minute}',
                'utc': weather['sys']['sunset'],
            }
            if s.minute < 10:
                self.sunset['hm'] = f'{s.hour}:0{s.minute}'

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
        for key, day in self.forecast['days'].items():
            d = datetime.datetime.strptime(day['date'], '%Y-%m-%d')
            line = f"{d:%A, %b %d}\n" \
                f"High: {day['high']:.0f}{DEG} {self.units} " \
                f"Low: {day['low']:.0f}{DEG} {self.units}\n" \
                f"{day['conditions']['description'].upper()}\n"
            strings.append(line)
            i += 1
        return '\n'.join(strings)

    def getWeatherStrings(self):
        strings = {
            'city': self.city,
            'date': self.date.strftime('%a, %b %d'),
            'temp': self.temp,
        }
        if self.date.timestamp() < self.sunset['utc']:
            strings['sun'] = self.sunset['hm']
        else:
            strings['sun'] = self.sunrise['hm']
        return strings

    def getForecastStrings(self):
        strings = {}
        for key,day in self.forecast['days'].items():
            d = datetime.datetime.strptime(day['date'].split(' ')[0], '%Y-%m-%d')
            strings[d.day] = {
                'date': d.strftime('%A - %d'),
                'temps': f"High: {day['high']:.0f}{DEG} {self.units} - Low: {day['low']:.0f}{DEG} {self.units}",
                'cond': day['conditions']['description'].upper(),
                'icon': day['icon'],
            }
        return strings


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
                    'icon': ICON[hour['weather'][0]['icon']],
                }
        d = str(datetime.datetime.now().day)
        if d in data['days'].keys():
            del data['days'][d]
        data['days'] = {k:data['days'][k] for k in data['days'] if int(k) > int(d) and int(k) <= int(d)+3}
        return data

