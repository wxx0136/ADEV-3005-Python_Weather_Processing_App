import calendar
import urllib.request
from html.parser import HTMLParser


class WeatherScraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = ''
        self.reading_temp_flag = False
        self.element_counter = 0

    def error(self, message):
        print("<Error>:", message)

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.reading_temp_flag = True

    def handle_data(self, data):
        if self.reading_temp_flag:
            if not data in ['LegendM', 'LegendE', ' ', 'LegendT']:
                if data == 'E':
                    self.data = self.data[:-1]
                self.data += data.strip() + ','

    def handle_endtag(self, tag):
        if tag == 'td':
            self.reading_temp_flag = False

    def get_data(self):
        return self.data


def get_weather_dict(year: int, month: int) -> dict:
    # Get raw info from HTML parse
    url = ("http://climate.weather.gc.ca/"
           + "climate_data/daily_data_e.html"
           + "?StationID=27174"
           + "&timeframe=2&StartYear=1840"
           + "&EndYear=" + str(year)
           + "&Day=1&Year=" + str(year)
           + "&Month=" + str(month) + "#")
    my_scraper = WeatherScraper()
    with urllib.request.urlopen(url) as response:
        html = str(response.read())
        my_scraper.feed(html)
    result = my_scraper.get_data().split(',')

    print('debug: result')
    print(str(result))

    # Convert raw info to weather list
    step = 11
    daily_temps_list = []
    for item in [result[i:i + step] for i in range(0, len(result), step)]:
        my_dict = {"Max": str(item[0]), "Min": str(item[1]), "Mean": str(item[2])}
        daily_temps_list.append(my_dict)

    print('debug: daily_temps_list')
    print(str(daily_temps_list))

    # Zip weather list items with the date
    weather_dict = {}
    day = 1
    for item in daily_temps_list:
        if day <= calendar.monthrange(year, month)[1]:
            if day < 10:
                data_day = '0' + str(day)
            else:
                data_day = str(day)
            data_key = str(year) + '-' + str(month) + '-' + data_day
            weather_dict[data_key] = item
            day += 1

    print('debug: weather_dict')
    print(str(weather_dict))

    return weather_dict


if __name__ == '__main__':
    print(str(get_weather_dict(2018, 2)))
