from twitter import *
import pandas as pd
import os, requests, json

cities = pd.read_csv("../data/cities.csv")
cities.fillna("", inplace = True)
please_words = {
    "en": ["please", "pls"],
    "fr": ["stp", "svp", "plaît", "steup"],
    "de": ["bitte"]
}

def getCityFromString(s):
    words = s.split(" ")
    lang = None
    city_name = None
    station = None

    for word in words:
        # Checks the word against list of magic words
        if lang == None:
            for lang_list, wordlist in please_words.items():
                for keyword in wordlist:
                    if word.lower() == keyword.lower():
                        lang = lang_list

    # Checks the cities against the phrase
    for index, city in cities.iterrows():
        if city["City"].lower() in s.lower():
            city_name = city["City"]
            station = city["station_id"]
            if lang == None:
                lang = city["lang"]
            break
        elif city["de"].lower() in s.lower() and city["de"] != "":
            city_name = city["de"]
            station = city["station_id"]
            if lang == None:
                lang = "de"
            break
        elif city["fr"].lower() in s.lower() and city["fr"] != "":
            city_name = city["fr"]
            station = city["station_id"]
            if lang == None:
                lang = "fr"
            break

    if station:
        station_id = station.split(",")[0].replace("(","")
        station_name = station.split(",")[1].replace(")","").replace("(","").strip()
    else:
        station_id = None
        station_name = None

    if lang == None:
        lang = "en"

    return city_name, station_id, station_name, lang