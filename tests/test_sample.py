import sys, io
sys.path.insert(0, 'src/')
from city import City
from stream import *

def test_citiesList():
  city = City("Paris", "11249", "ORLY", "fr")
  city.defaultGraph()
  assert ("température moyenne" in city.comment)

def test_Paris():
  city_name, station_id, station_name, lang = getCityFromString("Paris steup")
  assert (city_name == "Paris" and lang == "fr" and station_name == "'ORLY'")

def test_paris():
  city_name, station_id, station_name, lang = getCityFromString("paris")
  assert (city_name == "Paris" and lang == "fr" and station_name == "'ORLY'")

def test_paris_de():
  city_name, station_id, station_name, lang = getCityFromString("Paris bitte")
  assert (city_name == "Paris" and lang == "de" and station_name == "'ORLY'")

def test_varsovie():
  city_name, station_id, station_name, lang = getCityFromString("Varsovie")
  assert (city_name == "Varsovie" and lang == "fr" and station_id == "209")
  city = City(city_name, station_id, station_name, lang)
  img = city.defaultGraph()
  with open("tests/varsovie.png", "wb") as f: 
    f.write(img.read()) 
    f.close()

def test_berlin():
  city_name, station_id, station_name, lang = getCityFromString("Berlin")
  assert (city_name == "Berlin" and lang == "de" and station_id == "4563")
  city = City(city_name, station_id, station_name, lang)
  img = city.defaultGraph()
  with open("tests/berlin.png", "wb") as f: 
    f.write(img.read()) 
    f.close()

def test_zarago():
  city_name, station_id, station_name, lang = getCityFromString("Zaragoza please")
  assert (city_name == "Zaragoza" and lang == "en" and station_id == "238")
  city = City(city_name, station_id, station_name, lang)
  img = city.defaultGraph()
  with open("tests/zaragoza.png", "wb") as f: 
    f.write(img.read()) 
    f.close()

def test_plama():
  city_name, station_id, station_name, lang = getCityFromString("Palma de mallorca bitte")
  assert (city_name == "Palma de Mallorca" and lang == "de" and station_id == "3918")
  city = City(city_name, station_id, station_name, lang)
  img = city.defaultGraph()
  with open("tests/parlma.png", "wb") as f: 
    f.write(img.read()) 
    f.close()

def test_warsaw():
  city_name, station_id, station_name, lang = getCityFromString("Varsovie please")
  assert (city_name == "Varsovie" and lang == "en" and station_id == "209")

def test_koeln():
  city_name, station_id, station_name, lang = getCityFromString("Köln")
  assert (city_name == "Köln" and lang == "de" and station_id == "4298")
  city = City(city_name, station_id, station_name, lang)
  img = city.defaultGraph()
  with open("tests/cologne.png", "wb") as f: 
    f.write(img.read()) 
    f.close()