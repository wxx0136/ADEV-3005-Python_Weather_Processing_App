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

    def __init__(self):
        # user's database action choice: download full set or update
        self.database_choice = ''
        # user's plotting choice: box plot a year range or just line-plot one specific month
        self.plot_choice = ''

    def interact_with_user(self):
        """
        this class is to allow user to download or update their database
        :return: print the message to show the user if the data base has been downloaded or updated
        """
        self.database_choice = input('please input: "D" or "d" to download full DB, or input  '
                                     '"U"or "u" to update DB:  ')
        while not (
                self.database_choice.lower() == 'd' or self.database_choice.lower() == 'u' or self.database_choice.lower() == 'b' or self.database_choice.lower() == 'l'):
            self.database_choice = input('please input. "d" or "D" to download DB, "u"or "U" to update DB: ')

        iso_time_format = '%Y-%m-%d'
        current_time = datetime.datetime.now().strftime(iso_time_format)

        if self.database_choice.lower() == 'd':
            my_scraper = WeatherScraper()
            years = range(1996, int(current_time[:4]) + 1)
            for year in years:
                my_scraper.start_scraping('', year)
            mydb = DBOperations('weather.sqlite')
            mydb.initialize_db()
            mydb.purge_data()
            mydb.save_data(my_scraper.weather)
            print('your database has been downloaded!')

            self.plot_choice = input('please input "B" or "b" to draw box plots for a year range, or input '
                                     '"L" or "l" to draw a line plot for a selected month and year: ')
            if self.plot_choice.lower() == 'b':
                self.box_plot()

            elif self.plot_choice.lower() == 'l':
                self.line_plot()

        elif self.database_choice.lower() == 'u':
            my_scraper = WeatherScraper()
            mydb = DBOperations('weather.sqlite')
            db_latest_date = mydb.fetch_last_one()[0][1]

            if db_latest_date < current_time:  # compare 2 dates with ASCII value
                print('the latest date in database is ', db_latest_date, 'starting to update...')
                db_latest_year = int(db_latest_date[:4])
                db_latest_month = int(db_latest_date[5:7])
                db_latest_day = int(db_latest_date[-2:])
                current_year = int(current_time[:4])
                current_month = int(current_time[5:7])
                current_day = int(current_time[-2:])
                if db_latest_year < current_year:
                    for year in range(db_latest_year, current_year + 1):
                        my_scraper.start_scraping('', year)
                    mydb.initialize_db()
                    mydb.purge_data()
                    mydb.save_data(my_scraper.weather)
                elif db_latest_year == current_year and db_latest_month < current_month:
                    my_scraper.start_scraping('', current_year)
                    mydb.initialize_db()
                    mydb.purge_data()
                    mydb.save_data(my_scraper.weather)
                elif db_latest_year == current_year and db_latest_month == current_month and db_latest_day < current_day:
                    my_scraper.start_scraping('', current_year)
                    mydb.initialize_db()
                    mydb.purge_data()
                    mydb.save_data(my_scraper.weather)
                print('your database has been updated!')
            elif db_latest_date == current_time:
                print('No need to update, your database is already up to date!')
            self.plot_choice = input('please input "B" or "b" to draw box plots for a year range, or input '
                                     '"L" or "l" to draw a line plot for a selected month and year: ')
            if self.plot_choice.lower() == 'b':
                self.box_plot()

            elif self.plot_choice.lower() == 'l':
                self.line_plot()

    def box_plot(self):
        print("please input two separated years to generate a year range.(example: 2015 2018)")
        years = list(map(int, input("please input now: ").split()))
        my_plot = PlotOperations()
        print(my_plot.generate_box_plot(years[0], years[1]))
        print('the mean temperature from ' + str(years[0]) + 'to' + str(
            years[1]) + 'has been plotted')

    def line_plot(self):
        print("please input a specific month followed by a specific year,"
              " to generate a year range.(example: 2018 3)")
        nums = list(map(int, input("please input now: ").split()))
        my_plot = PlotOperations()
        print(my_plot.generate_line_plot(nums[0], nums[1]))
        print('the mean temperature of ' + str(nums[0]) + '-' + str(nums[1]) + 'has been plotted')


if __name__ == '__main__':
    my_weather_processor = WeatherProcessor()
    my_weather_processor.interact_with_user()
