# Context for my weather

## Rationale

I wanted to know how abnormal the current temperature was, based on 20th-century averages, so I built this dogbot, which does just that. A [first version](https://github.com/n-kb/weathercontext) used reanalysis data ; I wanted to switch to station data for easier comparison.

## Usage

Tweet to @weathercontext with the name of the city you want temperature context for. The dogbot answers in either French, English or German. If no language is specified, the dogbot answers in the language spoken by the majority of the inhabitants of the city if it happens to be one of the three mentioned above (defaults to English otherwise). 

Some keywords, such as asking for the city in a different language, lets you change the dogbot's language.

Examples of requests:

- _"Paris"_ ➡️ Shows temperature in _Paris_, in _French_
- "_Paris, doggy_" ➡️ Shows temperatures in Paris, in _English_
- _"Berlin mon chien"_ ➡️ Shows temperature in _Berlin_, in _French_
- "_Wrocław_" ➡️ Shows temperatures in _Wrocław_, in _English_
- "_Breslau_" ➡️ Shows temperatures in _Wrocław_, in _German_

## Coverage

78 cities are covered. From North to South:

- Helsinki
- Tallinn
- Stockholm
- Gothenburg
- Riga
- Edinburgh
- Copenhagen
- Malmö
- Vilnius
- Belfast
- Leeds
- Hamburg
- Szczecin
- Liverpool
- Sheffield
- Dublin
- Bremen
- Nottingham
- Leicester
- Berlin
- Birmingham
- Amsterdam
- Hanover
- Warsaw
- Utrecht
- The Hague
- Münster
- Rotterdam
- Dortmund
- London
- Bochum
- Essen
- Duisburg
- Leipzig
- Wuppertal
- Düsseldorf
- Wrocław
- Dresden
- Cologne
- Bonn
- Frankfurt
- Prague
- Kraków
- Mannheim
- Nuremberg
- Karlsruhe
- Paris
- Stuttgart
- Vienna
- Munich
- Budapest
- Iasi
- Cluj-Napoca
- Zagreb
- Lyon
- Milan
- Galati
- Bologna
- Bucharest
- Craiova
- Constanța
- Nice
- Toulouse
- Marseille
- Bilbao
- Rome
- Zaragoza
- Madrid
- Palma de Mallorca
- Valencia
- Lisbon
- Alicante
- Murcia
- Athens
- Córdoba
- Seville
- Málaga
- Las Palmas

## Data

Historical data comes from European Climate Assessment & Dataset (ECA&D), who very nicely put [datasets of daily weather data](https://www.ecad.eu//dailydata/index.php) online.

Data for the current week comes from [openweathermap](http://openweathermap.org).

Data for the current week shows average temperature over a 24-hour period based on hourly data. If you ask for data at 15:00, for instance, the mean temperature for the day will be the average of the hourly values between 15:00 on the previous day and 15:00 on the current day. Do note that this is not the same methodology as the ECA&D dataset mentioned above, which uses midnight-to-midnight means.

## Localization

## References

Klein Tank, A.M.G. and Coauthors, 2002. _Daily dataset of 20th-century surface air temperature and precipitation series for the European Climate Assessment._ Int. J. of Climatol., 22, 1441-1453. Data and metadata available at http://www.ecad.eu