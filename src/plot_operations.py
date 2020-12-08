"""
this module plots the weather  data fetched from database
include methods:
generate_box_plot is to draw box plot from year to year
generate_line_plot is to draw line plot from a specific month from a chosen year
"""
from requests import get
import matplotlib.pyplot as plt
from dateutil import parser
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from common import is_number


class PlotOperations:
    """
    this class is to box plot and line plot
    weather mean temperatures of year to year or specific month respectively
    """

    def __init__(self):
        self.box_plot_path_saving_dict = {}
        self.line_plot_path_saving_dict = {}

    # fetched_list_format = [
    #     (366, '2020-01-01', 'StationID=27174', -12.3, -3.5, -7.9),
    #     (367, '2020-01-02', 'StationID=27174', -8.2, -6.0, -7.1),
    #     (368, '2020-01-03', 'StationID=27174', -6.8, -1.0, -3.9)
    # ]

    def generate_box_plot(self, start_year: int, end_year: int) -> dict:
        """
        :param end_year: starting year for box plotting
        :param start_year: ending year for line plotting
        :return: returns the generated box plot images' saving paths class instance
        """

        my_db = DBOperations('weather.sqlite')

        years = range(start_year, end_year + 1)
        monthly_weather_data = {}

        for year in years:
            months = range(1, 13)
            yearly_data = []
            for month in months:
                monthly_list = my_db.fetch_data(year, month)
                if month not in monthly_weather_data:
                    monthly_weather_data[month] = []
                for item in monthly_list:
                    if is_number(item[5]):
                        monthly_weather_data[month].append(float(item[5]))
        # format: [1:[Jan temps],2:[Feb temps],..,12:[Dec temps]]
        plot_title = 'Monthly Temperature Distribution for:' + str(start_year) + ' to ' + str(end_year)

        print(monthly_weather_data)
        plt.boxplot(monthly_weather_data.values(), sym="o", whis=1.5)
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')
        plt.title(plot_title)
        save_path = './images/boxplot-'+str(start_year)+'_to_'+str(end_year)+'.jpg'
        plt.savefig(save_path)
        self.box_plot_path_saving_dict[str(start_year) + '-' + str(end_year)] = save_path
        plt.show()

        return self.box_plot_path_saving_dict

    def generate_line_plot(self, specific_month: int, specific_year: int) -> dict:
        """
        :param specific_month: the chosen month for line plotting
        :param specific_year: the chosen year for line plotting
        :return: returns the generated line plot images' saving paths class instance
        """
        my_db = DBOperations('weather.sqlite')
        specific_month_data = []
        specific_timestamp = []
        monthly_list = my_db.fetch_data(specific_year, specific_month)
        for item in monthly_list:
            if is_number(item[5]):
                specific_month_data.append(float(item[5]))
                specific_timestamp.append(float(item[1][-2:]))
        print(specific_year, '-', specific_month, ':', specific_month_data)

        plt.plot(specific_timestamp, specific_month_data)
        plt.xlabel('Day')
        plt.ylabel('Temperature (Celsius)')
        plot_title = 'Daily Temperature Distribution for:' + str(specific_year) + ' - ' + str(specific_month)
        plt.title(plot_title)
        save_path = './images/' + str(specific_year) + '-' + str(specific_month) + '.jpg'
        plt.savefig(save_path)
        self.line_plot_path_saving_dict[str(specific_year) + '-' + str(specific_month)] = save_path
        plt.show()

        return self.line_plot_path_saving_dict


if __name__ == '__main__':
    my_scraper = WeatherScraper()
    my_scraper.start_scraping('', 2018)
    my_scraper.start_scraping('', 2019)
    my_scraper.start_scraping('', 2020)

    mydb = DBOperations('weather.sqlite')
    mydb.initialize_db()
    mydb.purge_data()
    mydb.save_data(my_scraper.weather)

    my_plot = PlotOperations()
    print(my_plot.generate_box_plot(2018, 2020))
    print(my_plot.generate_line_plot(3, 2018))
