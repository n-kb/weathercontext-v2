from twitter import *
import pandas as pd
from texts import texts
from city import City
import os, requests, json

cities = pd.read_csv("data/cities.csv")
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

def sendTweet(city, username = None, reply_to = None):

    # List of image ids
    img_ids = []

    imagedata = city.defaultGraph().read()
    status_text = city.comment

    if username == None:
        status_text = title
    else:
        status_text = texts[lang]["answer"] % (username, city.name)

    auth = OAuth(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_SECRET"], os.environ["TWITTER_KEY"], os.environ["TWITTER_SECRET"])

    # Authenticate to twitter
    t = Twitter(auth=auth)

    if imagedata is not None:
        t_upload = Twitter(domain='upload.twitter.com', auth=auth)

        # Sends image to twitter
        img_ids.append(t_upload.media.upload(media=imagedata)["media_id_string"])

    img_ids = ",".join(img_ids)

    # Tweets
    t.statuses.update(status=status_text, media_ids=img_ids, in_reply_to_status_id=reply_to)

if __name__ == "__main__":
    auth = OAuth(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_SECRET"], os.environ["TWITTER_KEY"], os.environ["TWITTER_SECRET"])

    # Authentifies with Twitter
    t = Twitter(auth=auth)

    # And with twitter stream
    twitter_stream = TwitterStream(auth=auth, domain='stream.twitter.com')

    # And with twitter upload 
    t_upload = Twitter(domain='upload.twitter.com', auth=auth)

    # Gets only the mentions to the account
    iterator = twitter_stream.statuses.filter(track="@weathercontext")

    for msg in iterator:

        # Gets some data from the tweet
        username = msg["user"]["screen_name"]
        status_id = msg["id_str"]
        tweet_contents = msg["text"]

        # Parses the city
        city_name, station_id, station_name, lang = getCityFromString(tweet_contents.replace("@weathercontext", ""))

        if city_name == None:
            # Does nothing
            print("Ignoring %s..." % username)
        else:
            city = City(city_name, station_id, station_name, lang)
            sendTweet(city, username, status_id)
            print("Tweeting to %s..." % username)