"""
this module is to prompt user inputting choice, allowing to download weather data from DB,
or update weather data from DB. Also, allowing user to input year range to generate the
box plot, or input a month and a year to generate a line plot.
"""
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations
import datetime


class WeatherProcessor:
    """
    this class is to interact with user, to prompt user inputting choice
    and generate box plots and line plot according user choices of inputting a year range
    or a specific month from a specific year.
    """

    @staticmethod
    def download_or_update_database():
        """
        this class is to allow user to download or update their database
        :return: print the message to show the user if the data base has been downloaded or updated
        """
        user_choice = input('please select a choice to input. "d" or "D" to download a full set of '
                            'weather data, "u"or "U" to update the weather data according to the current date: ')
        while not (user_choice.lower() == 'd' or user_choice.lower() == 'u'):
            user_choice = input('please select a choice to input. "d" or "D" to download a full set of '
                                'weather data, "u"or "U" to update the weather data according to the current date: ')

        iso_time_format = '%Y-%m-%d'
        current_time = datetime.datetime.now().strftime(iso_time_format)
        return_message = ''
        if user_choice.lower() == 'd':
            my_scraper = WeatherScraper()
            years = range(1996, current_time[:4] + 1)
            for year in years:
                my_scraper.start_scraping('', year)
            mydb = DBOperations('weather.sqlite')
            mydb.initialize_db()
            mydb.purge_data()
            mydb.save_data(my_scraper.weather)
            return_message = 'your database has been downloaded!'
        elif user_choice.lower() == 'u':
            my_scraper = WeatherScraper()
            db_latest_date = ''  # 数据库里最新信息 怎么get????????
            years = range(db_latest_date[:4], current_time[:4] + 1)
            for year in years:
                my_scraper.start_scraping('', year)
            mydb = DBOperations('weather.sqlite')
            mydb.initialize_db()
            mydb.purge_data()
            mydb.save_data(my_scraper.weather)
            return_message = 'your database has been updated!'

        print(return_message)

    @staticmethod
    def box_plot():
        """
        this class to allow users to generate box plots for a year range
        :return:
        """
        print("please input two separated years to generate a year range.(example: 2015 2018)")
        years = list(map(int, input("please input now: ").split()))
        my_plot = PlotOperations()
        print(my_plot.generate_box_plot(years[0], years[1]))

    @staticmethod
    def line_plot():
        """
        this class is to allow a user to generate a line plot for a specific month from one year
        :return:
        """
        print("please input a specific month followed by a specific year,"
              " to generate a year range.(example: 3 2018)")
        nums = list(map(int, input("please input now: ").split()))
        my_plot = PlotOperations()
        print(my_plot.generate_line_plot(nums[0], nums[1]))

if __name__ == '__main__':
    WeatherProcessor.download_or_update_database()
    WeatherProcessor.box_plot()
    WeatherProcessor.line_plot()

