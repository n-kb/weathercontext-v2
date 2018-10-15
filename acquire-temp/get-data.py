import MySQLdb
import requests, json, os, math, time
import datetime as dt
import urllib.parse as urlparse
import peewee
import pandas as pd
from peewee import *

if 'CLEARDB_DATABASE_URL' not in os.environ:
    from playhouse.sqlite_ext import SqliteExtDatabase
    db = SqliteExtDatabase('weather.db')

else:
    PROD = True
    url = urlparse.urlparse(os.environ['CLEARDB_DATABASE_URL'])
    db = peewee.MySQLDatabase(url.path[1:], host=url.hostname, user=url.username, passwd=url.password)

class BaseModel(Model):
    class Meta:
        database = db

class CityTemp(BaseModel):
    id = IntegerField(index=True, primary_key=True)
    station_id = IntegerField()
    city = CharField()
    temp = FloatField()
    date = DateTimeField()

db.connect()
db.create_tables([CityTemp], safe=True)

cities = pd.read_csv("data/cities.csv")

for index, city in cities.iterrows():
    url = "http://api.openweathermap.org/data/2.5/weather?q=%s,%s&APPID=%s" % (city["City"], city["Country"], os.environ["OWMKEY"])
    r = requests.get(url)
    time.sleep(.5)
    json_data = json.loads(r.text)
    temp = json_data["main"]["temp"] - 272.15

    CityTemp.create(
        city = city["City"],
        station_id = city["station_id"].split(",")[0].replace("(",""),
        date = dt.datetime.now(),
        temp = temp
    )
    print ("\033[92mInserted data for %s.\033[0m" % city["City"])
