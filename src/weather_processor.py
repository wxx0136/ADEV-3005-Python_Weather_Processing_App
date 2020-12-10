"""
There is one class in this module.

Class WeatherProcessor presents the user with a menu of choices when the program starts.
"""
import sys

from db_operations import DBOperations
from plot_operations import PlotOperations
from scrape_weather import WeatherScraper
from datetime import date
from common import is_int


class WeatherProcessor:
    def __init__(self):
        self.my_db = DBOperations('weather.sqlite')
        self.my_db.initialize_db()
        self.cut_off = '****************************************************************************'
        self.invalid_input_str = 'Sorry, your input is not validated, please try again.'

    def exe_welcome(self):
        """
        Welcome menu.
        :return:
        """
        print(self.cut_off)
        print('Welcome to Weather Scraper App!')
        print('There are weather data between [{0}] and [{1}] in the database.'.format(
            self.my_db.fetch_earliest_one()[0][0], self.my_db.fetch_last_one()[0][0]))

        self.exe_menu_0()

    def exe_menu_0(self):
        """
        Main menu.
        :return:
        """
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
        """
        Fetch all new data menu:
        :return:
        """
        print(self.cut_off)
        print('Are you sure you want to fetch all new data from the website?')

        while True:
            selection = input('It will take several minutes [Y/N] :').lower()

            if selection == 'y':
                self.exe_menu_0_1_1()
                self.exe_menu_0()
            elif selection == 'n':
                self.exe_menu_0()
            else:
                print(self.invalid_input_str)

    def exe_menu_0_1_1(self):
        """
        Processing of fetching all new data.
        :return:
        """
        print(self.cut_off)
        print('Fetching all new data from the website. It will take several minutes...')
        self.renew_all_data()

    def exe_menu_0_2(self):
        """
        Fetch the gap data menu.
        :return:
        """
        print(self.cut_off)
        print('The last day in the database is: [{0}]'.format(self.my_db.fetch_last_one()[0][0]))
        print('Today is: [{0}]'.format(date.today()))
        print('Fetching the missing data from the website...')
        self.fill_missing_data()
        self.exe_menu_0()

    def exe_menu_0_3(self):
        """
        Plot menu.
        :return:
        """
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
                self.exe_menu_0()
            elif selection == '4':
                sys.exit()
            else:
                print(self.invalid_input_str)

    def exe_menu_0_3_1(self):
        """
        Box plot menu.
        :return:
        """
        print(self.cut_off)
        print('You are trying to generate a BOX PLOT between a year range:')
        start_year_input_flag = True
        end_year_input_flag = True
        start_year = 0
        end_year = 0

        while start_year_input_flag:
            year_input = input('Enter the start year[from 1996 to now, c for Cancel]: ').lower()
            if is_int(year_input) and 1996 <= int(year_input) <= date.today().year:
                start_year = int(year_input)
                start_year_input_flag = False
            elif year_input == 'c':
                self.exe_menu_0_3()
            else:
                print(self.invalid_input_str)

        while end_year_input_flag:
            year_input = input('Enter the end year[from 1996 to now, c for Cancel]: ').lower()
            if is_int(year_input) and 1996 <= int(year_input) <= date.today().year:
                end_year = int(year_input)
                end_year_input_flag = False
            elif year_input == 'c':
                self.exe_menu_0_3()
            else:
                print(self.invalid_input_str)

        if start_year > end_year:
            start_year, end_year = end_year, start_year

        self.generate_box_plot(start_year, end_year)
        self.exe_menu_0_3()

    def exe_menu_0_3_2(self):
        """
        Line plot menu.
        :return:
        """
        print(self.cut_off)
        print('You are trying to generate a LINE PLOT for a specific month:')
        year_input_flag = True
        month_input_flag = True
        specific_year = 0
        specific_month = 0

        while year_input_flag:
            year_input = input('Enter the year[from 1996 to now, c for Cancel]: ').lower()
            if is_int(year_input) and 1996 <= int(year_input) <= date.today().year:
                specific_year = int(year_input)
                year_input_flag = False
            elif year_input == 'c':
                self.exe_menu_0_3()
            else:
                print(self.invalid_input_str)

        while month_input_flag:
            month_input = input('Enter the month[1-12, c for Cancel]: ').lower()
            if is_int(month_input) and 1 <= int(month_input) <= 12:
                specific_month = int(month_input)
                month_input_flag = False
            elif month_input == 'c':
                self.exe_menu_0_3()
            else:
                print(self.invalid_input_str)

        self.generate_line_plot(specific_year, specific_month)
        self.exe_menu_0_3()

    def renew_all_data(self):
        """
        Fetch all new data from website and cover the database.
        :return:
        """
        my_scraper = WeatherScraper()
        my_scraper.scrape_now_to_earliest_month_weather()
        self.my_db.purge_data()
        self.my_db.save_data(my_scraper.weather)

    def fill_missing_data(self):
        """
        Fetch the gap data from now to the last one in the database and just insert these data.
        :return:
        """
        last_one_date = self.my_db.fetch_last_one()[0][0]
        last_one_year = int(last_one_date[:4])
        last_one_month = int(last_one_date[5:7])

        year = date.today().year
        month = date.today().month
        my_scraper = WeatherScraper()

        if last_one_year == year and last_one_month == month:
            my_scraper.scrape_month_weather(year, month)
        while last_one_year != year and last_one_month != month:
            my_scraper.scrape_month_weather(year, month)
            month -= 1
            if month == 0:
                year -= 1
                month = 12

        self.my_db.save_data(my_scraper.weather)

    def generate_box_plot(self, start_year: int, end_year: int) -> None:
        """
        Generate a box plot for a year range.
        :param start_year:
        :param end_year:
        :return:
        """
        start_year_data = self.my_db.fetch_data(start_year)
        end_year_data = self.my_db.fetch_data(end_year)
        if not start_year_data:
            print('Warning: there is no data of year[{0}] in the database. Please update first.'.format(start_year))
        elif not end_year_data:
            print('Warning: there is no data of year[{0}] in the database. Please update first.'.format(end_year_data))
        else:
            my_plot = PlotOperations()
            my_plot.generate_box_plot(start_year, end_year)

    def generate_line_plot(self, specific_year: int, specific_month: int) -> None:
        """
        Generate a line plot for a month.
        :param specific_year:
        :param specific_month:
        :return:
        """
        month_data = self.my_db.fetch_data(specific_year, specific_month)
        if not month_data:
            print('Warning: there is no data of [{0}-{1}] in the database. Please update first.'.format(specific_year,
                                                                                                        specific_month))
        else:
            my_plot = PlotOperations()
            my_plot.generate_line_plot(specific_year, specific_month)


if __name__ == '__main__':
    my_wp = WeatherProcessor()
    my_wp.exe_welcome()
