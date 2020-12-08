import calendar
import urllib.request
from html.parser import HTMLParser
from datetime import date


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

    def handle_data(self, data: str):
        if self.reading_temp_flag:
            if data not in ['LegendM', 'LegendE', ' ', 'LegendT', 'LegendCarer', 'E']:
                # if data == 'E':
                #     self.data = self.data[:-1]
                # if data == 'M':
                #     self.data += '' + ','
                # else:
                self.data += data.strip() + ','

    def handle_endtag(self, tag):
        if tag == 'td':
            self.reading_temp_flag = False

    def get_data(self):
        return self.data

    def start_scraping(self, url: str, year: int) -> None:
        for i in range(1, 13):
            self.get_weather_dict(year, i)

    def get_weather_dict(self, year: int, month: int) -> dict:
        print('Scraping data of year:{0}, month:{1}'.format(year, month))
        days_of_current_month = calendar.monthrange(year, month)[1]
        # Get raw info from HTML parse
        url = ("http://climate.weather.gc.ca/"
               + "climate_data/daily_data_e.html"
               + "?StationID=27174"
               + "&timeframe=2&StartYear=1840"
               + "&EndYear=" + str(year)
               + "&Day=1&Year=" + str(year)
               + "&Month=" + str(month) + "#")

        new_scraper = WeatherScraper()
        with urllib.request.urlopen(url) as response:
            html = str(response.read())
        new_scraper.feed(html)

        result = new_scraper.get_data().split(',')

        # print('debug: result')
        # count = 0
        # for r in result:
        #     print(str(r) + ',', end='')
        #     count += 1
        #     if count == 11:
        #         print()
        #         count = 0
        # print()

        # Convert raw info to weather list.
        # From the website, each row has 11 column, and the last 4 lines are useless(sum, avg, xtrm, summary)
        columns = 11

        # print(datetime.date.today().day)
        if date.today().year == year and date.today().month == month:
            rows = date.today().day
        else:
            rows = days_of_current_month
        result_grouping = [result[i:i + columns] for i in
                           range(0, rows * columns, columns)]
        daily_temps_list = []
        for item in result_grouping:
            if len(item) >= 3:
                my_dict = {"Max": str(item[0]), "Min": str(item[1]), "Mean": str(item[2])}
                daily_temps_list.append(my_dict)

        # print('debug: daily_temps_list')
        # for item in daily_temps_list:
        #     print(str(item))

        # Zip weather list items with the date
        day = 1
        month_dict = {}
        for item in daily_temps_list:
            # Get the days of that month
            if day <= days_of_current_month:
                str_day = ('0' + str(day)) if day < 10 else str(day)
                str_month = ('0' + str(month)) if month < 10 else str(month)
                data_key = str(year) + '-' + str_month + '-' + str_day
                # exclude today's or yesterday's blank data
                if item['Max'] != '' and item['Min'] != '' and item['Mean'] != '':
                    month_dict[data_key] = item
                    self.weather[data_key] = item
            day += 1

        # print('debug: month_dict')
        # for key, value in month_dict.items():
        #     print(key + ':' + str(value))

        return month_dict


if __name__ == '__main__':
    my_scraper = WeatherScraper()
    my_scraper.get_weather_dict(2020, 12)
    for key, value in my_scraper.weather.items():
        print(key + ': ' + str(value))
