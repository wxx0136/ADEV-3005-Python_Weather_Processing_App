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

        :return:
        """
        user_choice = input('please select a choice to input. "d" or "D" to download a full set of '
                            'weather data, "u"or "U" to update the weather data according to the current date')
        iso_time_format = '%Y-%m-%d'
        current_time = datetime.datetime.now().strftime(iso_time_format)
        if user_choice.lower() == 'd':
            my_scraper = WeatherScraper()
            years = range(1996, current_time[:4] + 1)
            for year in years:
                my_scraper.start_scraping('', year)
            mydb = DBOperations('weather.sqlite')
            mydb.initialize_db()
            mydb.purge_data()
            mydb.save_data(my_scraper.weather)
        elif user_choice.lower() == 'u':
            my_scraper = WeatherScraper()
            db_latest_date = ''
            years = range(db_latest_date[:4], current_time[:4] + 1)
            for year in years:
                my_scraper.start_scraping('', year)
            mydb = DBOperations('weather.sqlite')
            mydb.initialize_db()
            mydb.purge_data()
            mydb.save_data(my_scraper.weather)
        else:
            print("please make your choice from options.please select a choice to input. ")
