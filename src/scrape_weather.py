import calendar
import urllib.request
from html.parser import HTMLParser


class WeatherScraper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.weather = {}
        self.data = ''
        self.reading_temp_flag = False

    def error(self, message):
        print("<Error>:", message)

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.reading_temp_flag = True

    def handle_data(self, data):
        if self.reading_temp_flag:
            if data not in ['LegendM', 'LegendE', ' ', 'LegendT', 'LegendCarer']:
                if data == 'E':
                    self.data = self.data[:-1]
                self.data += data.strip() + ','

    def handle_endtag(self, tag):
        if tag == 'td':
            self.reading_temp_flag = False

    def get_data(self):
        return self.data

    def start_scraping(self, url: str, year: int):
        print('we never use this ', url)
        for i in range(1, 12):
            self.get_weather_dict(year, i)

    def get_weather_dict(self, year: int, month: int):
        # Get raw info from HTML parse
        url = ("http://climate.weather.gc.ca/"
               + "climate_data/daily_data_e.html"
               + "?StationID=27174"
               + "&timeframe=2&StartYear=1840"
               + "&EndYear=" + str(year)
               + "&Day=1&Year=" + str(year)
               + "&Month=" + str(month) + "#")
        with urllib.request.urlopen(url) as response:
            html = str(response.read())
            self.feed(html)
        result = self.get_data().split(',')

        # print('debug: result')
        # print(str(result))

        # Convert raw info to weather list.
        # From the website, each row has 11 column, and the last 4 lines are useless(sum, avg, xtrm, summary)
        column = 11
        result_grouping = [result[i:i + column] for i in
                           range(0, len(result) - len(result) % column - column * 4, column)]
        daily_temps_list = []
        for item in result_grouping:
            my_dict = {"Max": str(item[0]), "Min": str(item[1]), "Mean": str(item[2])}
            daily_temps_list.append(my_dict)

        # print('debug: daily_temps_list')
        # print(str(daily_temps_list))

        # Zip weather list items with the date
        day = 1
        for item in daily_temps_list:
            # Get the days of that month
            if day <= calendar.monthrange(year, month)[1]:
                str_day = ('0' + str(day)) if day < 10 else str(day)
                str_month = ('0' + str(month)) if month < 10 else str(month)
                data_key = str(year) + '-' + str_month + '-' + str_day
                self.weather[data_key] = item
                day += 1

        # print('debug: weather_dict')
        # print(str(self.weather))


if __name__ == '__main__':
    myws = WeatherScraper()
    myws.get_weather_dict(2020, 12)
    print(str(myws.weather))
