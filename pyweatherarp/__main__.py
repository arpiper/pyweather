import sys
import os
import argparse
import requests
import configparser
from xdg.BaseDirectory import *

# set path to the local directory
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather import OpenWeatherMap
from weather import CityWeather
from window import WeatherWindow

def main():
    # parse any command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-w', '--window', action='store_true', help='Show weather data in a popup window')
    ap.add_argument('-l', '--cli', action='store_true', help='Print Current weather conditions. Default output mode.')
    ap.add_argument('-C', '--city', help='City name or id')
    ap.add_argument('-u', '--units', help='Temperature units: metric | imperial')
    ap.add_argument('-bg', '--background', help='background color of the popup window')
    ap.add_argument('-fg', '--foreground', help='foreground color of the popup window')
    args = vars(ap.parse_args())

    # Read the config file and parse the defaults
    cfg_dir = save_config_path('pyweatherarp')
    config = configparser.ConfigParser()
    # read the included default configuration file
    config.read('config')
    # read the user created configuration file. Should be in $XDG_CONFIG_HOME/pyweatherarp
    config.read(f'{cfg_dir}/config')

    city = config['SETTINGS']['CITY']
    country = config['SETTINGS']['COUNTRY']
    units = config['SETTINGS']['UNITS']
    key = config['API']['key']

    if args['city']:
        city = args['city']
    if args['units']:
        units = args['units']

    api = OpenWeatherMap(key=key, city=city, units=units)
    w = CityWeather(city=city, api=api, units=units)
    if args['window']:
        win = WeatherWindow(title=f"{w.city} Weather Forecast")
        win.setData(current=w.getWeatherStrings(), forecast=w.getForecastStrings())
        win.drawGrid()
        win.showWindow()
    else:
        cw = w.getCurrentWeather()
        print(f"{w.temp} - \uf051 {w.sunset['hm']}")
        title = '^pa(;-150)Weather Forecast'


if __name__ == '__main__':
    main()
