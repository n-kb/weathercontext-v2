import os
import datetime as dt
from city import City
from stream import sendTweet

def tweetCity():

    # Gets the current time
    now = dt.datetime.utcnow()
    current_hour = now.hour

    if current_hour == 11:
        city = City("Berlin", "4563", "Berlin-Mitte", "de")
        sendTweet(city)
#    elif current_hour == 15:
#        city = City("Paris", "11249", "Orly", "fr")
#        sendTweet(city)
#    elif current_hour == 19:
#        city = City("London", "1859", "Hampstead", "en")
#        sendTweet(city)

    return "OK"


if __name__ == "__main__":
    tweetCity()