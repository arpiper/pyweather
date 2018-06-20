import sys
import os
import argparse
import requests

import tkinter as tk

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# set path to the local directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather import OpenWeatherMap
from weather import CityWeather
from window import WeatherWindow
import config 

DEG = u'\N{DEGREE SIGN}'

def main(args):
    city = config.CITY
    country = config.COUNTRY
    units = config.UNITS
    if args['city']:
        city = args['city']
    if args['units']:
        units = args['units']
    api = OpenWeatherMap(key=config.KEY, city=city, units=units)
    w = CityWeather(city=city, api=api, units=units)
    if args['window']:
        cw = w.getCurrentWeather()
        f = w.getForecast()
        win = WeatherWindow(title=f"{f['city']['name']} Weather Forecast")
        # mvoed thses two lines into window class.
        #win.connect('destroy', Gtk.main_quit)
        win.setData(current=cw, forecast=f)
        win.show_all()
        win.showWindow()
    else:
        cw = w.getCurrentWeather()
        print(f"{w.temp} - {w.sunset}")
        title = '^pa(;-150)Weather Forecast'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-w', '--window', action='store_true', help='Show weather data in a popup window')
    ap.add_argument('-l', '--cli', action='store_true', help='Print Current weather conditions. Default output mode.')
    ap.add_argument('-C', '--city', help='City name or id')
    ap.add_argument('-u', '--units', help='Temperature units: metric | imperial')
    ap.add_argument('-bg', '--background', help='background color of the popup window')
    ap.add_argument('-fg', '--foreground', help='foreground color of the popup window')
    args = vars(ap.parse_args())
    main(args)
