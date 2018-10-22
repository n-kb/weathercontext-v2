import sys
sys.path.insert(0, '../src/')
from city import City
from stream import *

def test_citiesList():
    city = City("Paris", "11249", "ORLY", "fr")
    city.defaultGraph()
    assert ("température moyenne" in city.title)

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

def test_plama():
	city_name, station_id, station_name, lang = getCityFromString("Palma de mallorca bitte")
	assert (city_name == "Palma de Mallorca" and lang == "de" and station_id == "3918")

def test_warsaw():
	city_name, station_id, station_name, lang = getCityFromString("Varsovie please")
	assert (city_name == "Varsovie" and lang == "en" and station_id == "209")

def test_koeln():
	city_name, station_id, station_name, lang = getCityFromString("Köln")
	assert (city_name == "Köln" and lang == "de" and station_id == "4298")