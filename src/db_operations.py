"""
There is one classes in this module.

Class DBOperations is an sqlite database operation.
"""
import sqlite3
import logging

from common import is_number
from scrape_weather import WeatherScraper


class DBOperations:
    """
    Use the Python sqlite3 module to store the weather data in an SQLite database in the specified format.
    """

    def __init__(self, path: str):
        """
        Build a new database connection.
        """
        self.db_name = path
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.logger = logging.getLogger()

    def __enter__(self):
        """
        Create a database context manager.
        :return:
        """
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the database connection.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def initialize_db(self):
        """
        Create a table if it not exists.
        :return:
        """
        try:
            with DBOperations(self.db_name) as cursor:
                sql_initialize_db = """create table if not exists samples (
                                            id integer primary key autoincrement not null,
                                            sample_date text not null UNIQUE,
                                            location text not null default %s,
                                            min_temp real not null,
                                            max_temp real not null,
                                            avg_temp real not null); """ % "'StationID=27174'"
                cursor.execute(sql_initialize_db)
        except Exception as e:
            self.logger.error(e)

    def save_data(self, data_source: dict):
        """
        Save new data to the DB, if it doesn't already exist (i.e. No duplicate data)
        :param data_source:
        :return: none
        """
        try:
            print('Database is updating...')
            new_list = []
            for k, v in data_source.items():
                new_row = [k]
                for nest_key, nest_value in v.items():
                    # If it's 'M', insert a '' into database.
                    if is_number(nest_value):
                        new_row.append(nest_value)
                    else:
                        new_row.append('')
                new_list.append(tuple(new_row))

            with DBOperations(self.db_name) as cursor:
                sql_save_data = """INSERT OR IGNORE INTO samples (sample_date,max_temp,min_temp,avg_temp) VALUES (?,?,?,
                ?); """
                for list_item in new_list:
                    cursor.execute(sql_save_data, list_item)
            print('Database updated.')
        except Exception as e:
            self.logger.error(e)

    def fetch_data(self, year: int, month: int = 0) -> list:
        """
        Fetch the requested data for plotting.
        :param year:
        :param month:
        :return:
        """
        try:
            if month == 0:
                month_str = ''
            elif month < 10:
                month_str = '0' + str(month)
            else:
                month_str = str(month)

            with DBOperations(self.db_name) as cursor:
                sql_fetch_year_date = f"""SELECT * FROM samples WHERE sample_date LIKE '{year}-{month_str}%';"""
                cursor.execute(sql_fetch_year_date)
                fetch_weather = cursor.fetchall()
            return fetch_weather
        except Exception as e:
            self.logger.error(e)

    def fetch_earliest_one(self) -> list:
        """
        Fetch the earliest date in the database.
        :return:
        """
        try:
            with DBOperations(self.db_name) as cursor:
                sql_fetch_last_one = """SELECT min(sample_date) FROM samples;"""
                cursor.execute(sql_fetch_last_one)
                fetch_weather = cursor.fetchall()
            return fetch_weather
        except Exception as e:
            self.logger.error(e)

    def fetch_last_one(self) -> list:
        """
        Fetch the latest data in the database.
        :return:
        """
        try:
            with DBOperations(self.db_name) as cursor:
                sql_fetch_last_one = """SELECT max(sample_date) FROM samples;"""
                cursor.execute(sql_fetch_last_one)
                fetch_weather = cursor.fetchall()
            return fetch_weather
        except Exception as e:
            self.logger.error(e)

    def purge_data(self):
        """
        Delete all the data from the DB for when the program fetches all new weather data.
        :return:
        """
        try:
            print('Purging all the data from the database... ')
            with DBOperations(self.db_name) as cursor:
                sql_purge_data_1 = """DELETE FROM samples;"""
                sql_purge_data_2 = """DELETE FROM sqlite_sequence WHERE name = 'samples';"""
                cursor.execute(sql_purge_data_1)
                cursor.execute(sql_purge_data_2)
        except Exception as e:
            self.logger.error(e)


if __name__ == '__main__':
    mydb = DBOperations('weather.sqlite')
    mydb.initialize_db()

    my_scraper = WeatherScraper()
    my_scraper.scrape_month_weather(2020, 12)
    my_scraper.scrape_now_to_earliest_month_weather(1998, 5)

    mydb.purge_data()
    mydb.save_data(my_scraper.weather)
    for key, value in my_scraper.weather.items():
        print(key + ': ' + str(value))

    print('years data')
    for item in mydb.fetch_data(1996):
        print(item)

    print('month data')
    for item in mydb.fetch_data(2020, 12):
        print(item)

    print('the last one in the database')
    print(mydb.fetch_last_one())
