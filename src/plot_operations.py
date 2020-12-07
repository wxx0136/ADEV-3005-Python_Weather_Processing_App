from requests import get
import matplotlib.pyplot as plt
from dateutil import parser
# from db_operations import DBOperations
from scrape_weather import WeatherScraper
from common import is_number


class PlotOperations:
    """
    plot weather details
    """

    # weather_data[0].append(my_dict[calendar.xxx]['mean'])
    # my_dict = {
    #     '2020-12-01': {'Max': '1.3', 'Min': '-9.4', 'Mean': '-4.0'},
    #     '2020-12-02': {'Max': '4.0', 'Min': '-6.8', 'Mean': '-1.4'},
    #     '2020-12-03': {'Max': '3.3', 'Min': '-8.4', 'Mean': '-2.5'},
    #     '2020-12-04': {'Max': '1.6', 'Min': '-10.6', 'Mean': '-4.5'}
    #     }

    # my_list = [
    #     (366, '2020-01-01', 'StationID=27174', -12.3, -3.5, -7.9),
    #     (367, '2020-01-02', 'StationID=27174', -8.2, -6.0, -7.1),
    #     (368, '2020-01-03', 'StationID=27174', -6.8, -1.0, -3.9)
    # ]
    @staticmethod
    def generate_box_plot(start_year: int, end_year: int):
        my_scraper = WeatherScraper()
        years = range(start_year, end_year + 1)
        years_weather_data = {}

        for year in years:
            months = range(1, 13)
            yearly_data = []
            current_year = ''
            for month in months:
                monthly_dict = my_scraper.get_weather_dict(year, month)
                monthly_mean_temp = []
                for key, value in monthly_dict.items():
                    if is_number(value['Mean']):
                        monthly_mean_temp.append(float(value['Mean']))
                        current_year = key[:4]
                yearly_data.append(monthly_mean_temp)
            years_weather_data.update({current_year: yearly_data})
        # format: {2019:[[Jan],2:[Feb],..,12:[Dec]], 2020: [[Jan],...12:[Dec]]}

        for key, value in years_weather_data.items():
            print(key, value)
            plt.boxplot(value, sym="o", whis=1.5)
            plt.show()

        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    @staticmethod
    def generate_line_plot(specific_month: int, specific_year: int):
        my_scraper = WeatherScraper()
        specific_month_data = []
        specific_timestamp = []
        monthly_dict = my_scraper.get_weather_dict(specific_year, specific_month)
        for k, v in monthly_dict.items():
            if is_number(v['Mean']):
                specific_month_data.append(float(v['Mean']))
                specific_timestamp.append(float(k[-2:]))
        print(specific_year, '-', specific_month, ':', specific_month_data)

        plt.plot(specific_timestamp, specific_month_data)
        plt.show()


if __name__ == '__main__':
    PlotOperations.generate_box_plot(2018, 2019)
    PlotOperations.generate_line_plot(3, 2018)
