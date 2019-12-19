import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import ConnectionPatch
import matplotlib.font_manager as font_manager
import matplotlib.ticker as mticker
import datetime as dt
from scipy.interpolate import interp1d
import matplotlib.dates as mdates
from colour import Color
import random, os, io
import urllib.parse as urlparse
import peewee
from peewee import *
from functools import reduce
from texts import texts

class City:
    
    days_to_show = 7
    
    colors = {"purple": "#a02073",
            "yellow": "#dbb64b",
            "lightblue": "#67c7d3",
            "darkblue": "#2d616f",
            "red": "#eb3721"}
    
    font_color = "#676767"
    sans_fontfile = 'fonts/LiberationSans-Regular.ttf'
    serif_fontfile = 'fonts/VeraSerif.ttf'
    title_font = {'fontproperties': font_manager.FontProperties(fname=serif_fontfile, size=15)
                  ,'color': font_color
                 }
    comment_font = {'fontproperties': font_manager.FontProperties(fname=sans_fontfile, size=14)
                  ,'color': font_color
                  , 'weight': 'bold'
                 }
    label_font = {'fontproperties': font_manager.FontProperties(fname=sans_fontfile, size=10)
                 ,'color': font_color
                 }

    label_font_strong = {'fontproperties': font_manager.FontProperties(fname=sans_fontfile, size=10)
                 ,'color': colors["red"]
                 , 'weight': 'bold'
                 }
    expl_sentences = {'fontproperties': font_manager.FontProperties(fname=sans_fontfile, size=9)
                 ,'color': "white"
                 , 'weight': 'normal'
                 }
    label_current = {'fontproperties': font_manager.FontProperties(fname=sans_fontfile, size=12)
                 ,'color': colors["red"]
                 , 'weight': 'bold'
                 }
    
    label_current_small = {'fontproperties': font_manager.FontProperties(fname=sans_fontfile, size=10)
                 ,'color': colors["darkblue"]
                 }

    smaller_font = {'fontproperties': font_manager.FontProperties(fname=sans_fontfile, size=9)
                    ,'color': font_color
                    , 'weight': 'bold'}
    

    
    def __init__(self, name, code, station_name, lang):
        self.name = name
        self.code = code
        self.lang = lang
        if (self.lang == ""):
          self.lang = "en"
        self.absolute_min = 99
        self.station_name = station_name.title()
        self.makeFilename()
        
    def makeFilename(self):
        zeroes = ""
        for a in range(0, 6 - len(self.code)):
            zeroes += "0"
        self.filename = "TG_STAID%s%s.txt" % (zeroes, self.code)
        
    def loadTempFile(self):
        self.df = pd.read_csv("data/ECA_blend_tg/" + self.filename, sep=","
                              , header=15
                              , skipinitialspace=True
                              , parse_dates = ["DATE"]
                              , infer_datetime_format = True)
        # Keep only valid values
        self.df = self.df.loc[self.df["Q_TG"] == 0]
        self.df = self.df.reset_index(drop=True)
        # Transforms values to °C
        self.df["TG"] = self.df["TG"] / 10
        # Gets series start year
        self.first_year = self.df["DATE"][0].year
    
    def defaultGraph(self):
        self.blankGraph()
        self.getValuesForLastWeek()
        self.makeAnnotations()
        self.addTitle()
        
        ## Reduces size of plot to allow for text
        plt.subplots_adjust(top=0.84, bottom=0.10)

        # Saves images to string
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)

        plt.close()

        return img_data
    
    def addTitle(self):
        comment = texts[self.lang]["comment"] % (self.name, self.current_values[0])
        
        hot_or_warm = texts[self.lang]["warm"]
        if self.current_values[0] > 25:
            hot_or_warm = texts[self.lang]["hot"]
        diff = self.current_values[0] - self.avg_values[0]
        
        if diff > 8:
            comment += texts[self.lang]["extremely hot"] % hot_or_warm
        elif diff > 5:
            comment += texts[self.lang]["very hot"] % hot_or_warm
        elif diff > 2:
            comment += texts[self.lang]["pretty hot"] % hot_or_warm
        elif diff > -2:
            comment += texts[self.lang]["average"]
        elif diff > -5:
            comment += texts[self.lang]["pretty cold"]
        else:
            comment += texts[self.lang]["very cold"]
        
        begin_end = texts[self.lang]["early"]
        if dt.datetime.now().day > 20:
            begin_end = texts[self.lang]["late"]
        elif dt.datetime.now().day > 10:
            begin_end = texts[self.lang]["mid"]
        
        comment += texts[self.lang]["for month"] % (begin_end, texts[self.lang][dt.datetime.now().strftime("%b")])

        # Text "Pretty worm for mid december"
        plt.annotate(comment,
             xy=(pd.to_datetime('today') - pd.Timedelta('%d hours' % ((int(self.days_to_show) * 24) / 2 - 12)), self.current_values[0] - .1),
             xytext=(pd.to_datetime('today') - pd.Timedelta('%d hours' % ((int(self.days_to_show) * 24) / 2 - 12)), self.absolute_min + 1),
             horizontalalignment='center',
             verticalalignment='center',
             bbox=dict(facecolor="white", edgecolor=self.colors["yellow"], alpha=1),
             **self.comment_font
            )
        
        self.comment = comment

        title = texts[self.lang]["title"] % self.name

        plt.figtext(.05,.9,title, **self.title_font)
    
    def makeAnnotations(self):
        # Last available temperature
        todays_text = "%.1f°C" % self.current_values[0]
        plt.annotate(todays_text,
             xy=(pd.to_datetime('today'), self.current_values[0]),
             xytext=(pd.to_datetime('today') + pd.Timedelta('3 hours'), self.current_values[0]),
             horizontalalignment='left',
             verticalalignment='center',
             **self.label_current
            )
        
        # Sentence for half
        plt.annotate(texts[self.lang]["annotate_half"] % (self.first_year),
             xy=(pd.to_datetime('today') - pd.Timedelta('%d hours' % (int(self.days_to_show) * 24 - 36)), self.avg_values[-1]),
             xytext=(pd.to_datetime('today') - pd.Timedelta('%d hours' % (int(self.days_to_show) * 24 - 36)), self.avg_values[-1]),
             bbox=dict(facecolor='white', edgecolor='none', alpha=0),
             horizontalalignment='left',
             verticalalignment='center',
             **self.expl_sentences
            )

        # Sentence for 90p
        plt.annotate(texts[self.lang]["annotate_90"],
             xy=(pd.to_datetime('today') - pd.Timedelta('%d hours' % (int(self.days_to_show) * 24 - 36)), self.lower_90_values[-1]),
             xytext=(pd.to_datetime('today') - pd.Timedelta('%d hours' % (int(self.days_to_show) * 24 - 36)), self.lower_90_values[-1]),
             bbox=dict(facecolor=self.colors["lightblue"], edgecolor='none', alpha=.7),
             horizontalalignment='left',
             verticalalignment='center',
             **self.expl_sentences
            )

        # Last 50p upper temperature
        todays_text = "%.1f°C" % self.upper_50_values[0]
        plt.annotate(todays_text,
             xy=(pd.to_datetime('today'), self.upper_50_values[0]),
             xytext=(pd.to_datetime('today') + pd.Timedelta('3 hours'), self.upper_50_values[0]),
             horizontalalignment='left',
             verticalalignment='center',
             **self.label_current_small
            )

        # Last 50p lower temperature
        todays_text = "%.1f°C" % self.lower_50_values[0]
        plt.annotate(todays_text,
             xy=(pd.to_datetime('today'), self.lower_50_values[0]),
             xytext=(pd.to_datetime('today') + pd.Timedelta('3 hours'), self.lower_50_values[0]),
             horizontalalignment='left',
             verticalalignment='center',
             **self.label_current_small
            )
        
        # Line label averages
        # plt.annotate(texts[self.lang]["annotate_avg"] % (self.first_year, self.station_name),
        #      xy=(pd.to_datetime('today') - pd.Timedelta('%d days' % (int(self.days_to_show) - 1)), self.avg_values[-1]),
        #      xytext=(pd.to_datetime('today') - pd.Timedelta('%d days' % (int(self.days_to_show) - 1)), self.avg_values[-1] - 2),
        #      bbox=dict(facecolor='white', edgecolor='none', alpha=.7),
        #      horizontalalignment='left',
        #      verticalalignment='center',
        #      **self.label_avg
        #     )
        
        # Checks the height of the last current temp in order to position the current temp label
        offset = 2
        if self.current_values[0] >= max(self.current_values) - 1:
            offset = -1
        
        # Line label "Average daily temp for the last 7 days"
        plt.annotate(texts[self.lang]["annotate_lastweek"],
             xy=(pd.to_datetime('today'), self.current_values[0]),
             xytext=(pd.to_datetime('today'), self.current_values[0] + offset),
             bbox=dict(facecolor='white', edgecolor='none', alpha=.7),
             horizontalalignment='right',
             verticalalignment='center',
             **self.label_current
            )
        
        ## Adds source
        plt.figtext(.05, .03, texts[self.lang]["source"] + ": ECA&D, openweathermap. Last updated %s UTC" % self.lastUpdated, **self.smaller_font)
        
        # Formats x axis
        xfmt = mdates.DateFormatter('%d %B')
        self.ax.xaxis.set_major_formatter(xfmt)

    def getCurrentYearsValues(self):
        self.current_values = []
        
        cityTemp = self.dbInit()
        now = dt.datetime.now()
        lastWeek = now - dt.timedelta(self.days_to_show)
        citytemps = cityTemp.select(cityTemp.date, cityTemp.temp).where(cityTemp.date >= lastWeek).where(cityTemp.station_id == self.code)
        self.lastUpdated = citytemps[-1].date
        for day_num in range(0, self.days_to_show):
            daily_temps = citytemps.where(cityTemp.date >= now - dt.timedelta(day_num + 1)).where(cityTemp.date < now - dt.timedelta(day_num))
            daily_temps = list(map(lambda x: x.temp, list(daily_temps)))
            if len(daily_temps) > 0:
                daily_avg = reduce(lambda x, y: x + y, daily_temps) / len(daily_temps)
            else:
                daily_avg = np.nan
            self.current_values.append(daily_avg)
    
    def getValuesForLastWeek(self):
        today = pd.to_datetime('today')
        days = []
        self.lower_90_values = []
        self.upper_90_values = []
        self.lower_50_values = []
        self.upper_50_values = []
        self.avg_values = []
        self.max_values = []
        self.getCurrentYearsValues()
        
        for day in range(0,self.days_to_show):
            day = today - pd.Timedelta(str(day) + ' days')
            days.append(day)
            lower_90, upper_90, lower_50, upper_50, avg_value, max_value = self.getValuesForDay(day)
            self.lower_90_values.append(lower_90)
            self.upper_90_values.append(upper_90)
            self.lower_50_values.append(lower_50)
            self.upper_50_values.append(upper_50)
            self.avg_values.append(avg_value)
            self.max_values.append(max_value)
            
        # Checks for and plots records
        for day in range(0,self.days_to_show):
            if self.current_values[day] > self.max_values[day]:
                plt.annotate(texts[self.lang]["record"] + "!\n▼",
                     xy=(days[day], self.current_values[day]),
                     xytext=(days[day], self.current_values[day] + .9),
                     horizontalalignment='center',
                     verticalalignment='center',
                     **self.label_current_small
                    )
        
        # Fill area for 90% of the days
        self.ax.fill_between(days, self.lower_90_values, self.upper_90_values, color=self.colors["lightblue"], alpha=1)

        # Fill area for 50% of the days
        self.ax.fill_between(days, self.lower_50_values, self.upper_50_values, color=self.colors["darkblue"], alpha=1)
        self.ax.plot(days, self.lower_50_values, lw=1, color="white", alpha=.7)
        self.ax.plot(days, self.upper_50_values, lw=1, color="white", alpha=.7)

        # Plots the averages
        # self.ax.plot(days, self.avg_values, lw=1, color="white", alpha=.5)
        
        # Plots the current week
        self.ax.plot(days, self.current_values, lw=2.5, color="white", marker="o")
        self.ax.plot(days, self.current_values, lw=1, color=self.colors["red"], marker="o")
    
    def getValuesForDay(self, day):
        self.loadTempFile()
        
        day_values = self.df.loc[(self.df["DATE"].dt.month == day.month) & (self.df["DATE"].dt.day == day.day)]
        # Computes 20th century average
        day_values_20c = day_values.loc[day_values["DATE"].dt.year < 2000]
        avg_20c = day_values_20c["TG"].mean()
        lower_90 = day_values_20c["TG"].quantile(0.05)
        lower_50 = day_values_20c["TG"].quantile(0.25)
        upper_50 = day_values_20c["TG"].quantile(0.75)
        upper_90 = day_values_20c["TG"].quantile(0.95)
        
        # Plots the historical values
        for index, row in day_values.iterrows():
            # Checks for min
            if row["TG"] < self.absolute_min:
              self.absolute_min = row["TG"]
            color = Color(self.colors["darkblue"]).rgb
            self.ax.plot(day, row["TG"], lw=.5, color=color, alpha=0,  marker="o")
        
        return lower_90, upper_90, lower_50, upper_50, avg_20c, day_values["TG"].max()
    
    def blankGraph(self):
        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 6))
        ## Adds a horizontal line under the title
        con = ConnectionPatch(xyA=(.05,.88), xyB=(.95,.88), coordsA="figure fraction", coordsB="figure fraction",
                              axesA=None, axesB=None, color=self.font_color, lw=.1)
        self.ax.add_artist(con)

        # Removes top and right axes
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        ## Sets axes color
        self.ax.spines['bottom'].set_color(self.font_color)
        self.ax.spines['left'].set_color(self.font_color)
        self.ax.tick_params(axis='x', colors=self.font_color)
        self.ax.tick_params(axis='y', colors=self.font_color)
        self.ax.yaxis.label.set_color(self.font_color)
        self.ax.xaxis.label.set_color(self.font_color)

        # Sets labels fonts for axes
        for label in self.ax.get_xticklabels():
            label.set_fontproperties(font_manager.FontProperties(fname=self.sans_fontfile))
            label.set_fontsize(9)
        for label in self.ax.get_yticklabels():
            label.set_fontproperties(font_manager.FontProperties(fname=self.sans_fontfile))
            label.set_fontsize(9)

        # Set units for yaxis
        self.ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d°C'))

        self.ax.margins(x=0)
    
    def dbInit(self):
        if 'CLEARDB_DATABASE_URL' in os.environ:
            url = urlparse.urlparse(os.environ['CLEARDB_DATABASE_URL'])
        else:
            url = urlparse.urlparse(clear_db)
        
        db = peewee.MySQLDatabase(url.path[1:], host=url.hostname, user=url.username, passwd=url.password)

        class BaseModel(Model):
            class Meta:
                database = db

        class CityTemp(BaseModel):
            id = PrimaryKeyField()
            station_id = IntegerField()
            city = CharField()
            temp = FloatField()
            date = DateTimeField()

        db.connect()

        return CityTemp