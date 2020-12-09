import sys

from db_operations import DBOperations
from scrape_weather import WeatherScraper
from datetime import date
from common import is_int


class WeatherProcessor:
    def __init__(self):
        self.my_db = DBOperations('weather.sqlite')
        self.my_db.initialize_db()
        self.cut_off = '*****************************************************************************************'
        self.invalid_input_str = 'Sorry, your input is not validated, please try again.'

    def exe_welcome(self):
        print(self.cut_off)
        print('Welcome to Weather Scraper App!')
        print('Here are following year weather data in the database:')
        # TODO: print the years in the database

        self.exe_menu_0()

    def exe_menu_0(self):
        print(self.cut_off)
        print('What do you want to do?')
        menu = {
            '1': 'Fetch all new data from the website.',
            '2': 'Update data between today and the latest date in the database.',
            '3': 'Generate a plot.',
            '4': 'Exit.'
        }
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])

        while True:
            selection = input('Please input the number of the options[1,2,3,4]: ')

            if selection == '1':
                self.exe_menu_0_1()
            elif selection == '2':
                self.exe_menu_0_2()
            elif selection == '3':
                self.exe_menu_0_3()
            elif selection == '4':
                sys.exit()
            else:
                print(self.invalid_input_str)

    def exe_menu_0_1(self):
        print(self.cut_off)
        print('Are you sure you want to fetch all new data from the website?')

        while True:
            selection = input('It will take several minutes [Y/N] :').lower()

            if selection == 'y':
                self.exe_menu_0_1_1()
            elif selection == 'n':
                self.exe_menu_0()
            else:
                print(self.invalid_input_str)

    def exe_menu_0_1_1(self):
        print(self.cut_off)
        print('Fetching all new data from the website. It will take several minutes...')
        self.renew_all_data()

    def exe_menu_0_2(self):
        print(self.cut_off)
        print('The last day in the database is: [{0}]'.format(self.my_db.fetch_last_one()[0][0]))
        print('Fetching the missing data from the website...')
        self.fill_missing_data()
        self.exe_menu_0()

    def exe_menu_0_3(self):
        print(self.cut_off)
        print('What the kind of plots you want?')

        menu = {
            '1': 'Generate a BOX PLOT between a year range.',
            '2': 'Generate a LINE PLOT for an assigned month.',
            '3': 'Return to main menu.',
            '4': 'Exit.'
        }
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])

        while True:
            selection = input('Please input the number of the options[1,2,3,4]: ')

            if selection == '1':
                self.exe_menu_0_3_1()
            elif selection == '2':
                self.exe_menu_0_3_2()
            elif selection == '3':
                self.exe_menu_0_3_3()
            elif selection == '4':
                sys.exit()
            else:
                print(self.invalid_input_str)

    def exe_menu_0_3_1(self):
        print(self.cut_off)
        print('You are trying to generate a BOX PLOT between a year range:')
        start_year_input_flag = True
        end_year_input_flag = True
        start_year = 0
        end_year = 0

        while start_year_input_flag:
            year_input = input('Enter the start year[between 1996-2020, c for Cancel]: ')
            if is_int(year_input) and 1996 <= int(year_input) <= date.today().year:
                start_year = int(year_input)
                start_year_input_flag = False
            elif year_input == 'c':
                self.exe_menu_0_3()
            else:
                print(self.invalid_input_str)

        while end_year_input_flag:
            year_input = input('Enter the end year[between 1996-2020, c for Cancel]: ')
            if is_int(year_input) and 1996 <= int(year_input) <= date.today().year:
                end_year = int(year_input)
                end_year_input_flag = False
            elif year_input == 'c':
                self.exe_menu_0_3()
            else:
                print(self.invalid_input_str)

        if start_year > end_year:
            start_year, end_year = end_year, start_year

        print('Generate a BOX PLOT between years[{0}-{1}]...'.format(start_year, end_year))
        self.generate_box_plot()
        self.exe_menu_0_3()

    def generate_box_plot(self):
        pass

    def renew_all_data(self):
        my_scraper = WeatherScraper()
        my_scraper.scrape_now_to_earliest_month_weather()
        self.my_db.save_data(my_scraper.weather)

    def fill_missing_data(self):
        # TODO: fill missing data from today to the latest day in the database
        pass


if __name__ == '__main__':
    my_wp = WeatherProcessor()
    my_wp.exe_menu_0_3_1()
