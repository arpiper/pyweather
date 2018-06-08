import sys
import os
import argparse
import requests

# set path to the local directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather import OpenWeatherMap
from weather import CityWeather
import config 

def main(args):
    city = config.CITY
    country = config.COUNTRY
    units = config.UNITS
    if args['city']:
        city = args['city']
    if args['units']:
        units = args['units']
    api = OpenWeatherMap(key=config.KEY, city=city, units=units)
    w = CityWeather(city=city, api=api)
    w.getCurrentWeather()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--city', help='City name or id')
    ap.add_argument('-u', '--units', help='Temperature units: metric | imperial')
    args = vars(ap.parse_args())
    main(args)
