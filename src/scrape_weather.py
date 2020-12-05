import re
import urllib.request
from html.parser import HTMLParser


class WeatherScraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = ''
        self.readingFlag = False
        self.element_counter = 0

    def error(self, message):
        print("<Error>:", message)

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.readingFlag = True
            print(self.element_counter)
            if self.element_counter == 10:
                self.element_counter = 0

    def handle_data(self, data):
        if self.readingFlag:
            if self.element_counter < 3:
                self.data += data + ','
            self.element_counter += 1

    def handle_endtag(self, tag):
        if tag == 'td':
            self.readingFlag = False


    def cleanse(self):
        """ Remove all the space/blank """
        self.data = re.sub('\s+', ' ', self.data)

    def get_data(self):
        self.cleanse()
        return self.data


def my_filter():
    wScraper = WeatherScraper()
    url_example = 'http://www.weather.com.cn/html/weather/101210501.shtml'
    url = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5'
    with urllib.request.urlopen(
            url) as response:
        html = str(response.read())
        wScraper.feed(html)
    weather = wScraper.get_data()
    # weather = weather.split()
    return weather


if __name__ == '__main__':
    print(my_filter())
