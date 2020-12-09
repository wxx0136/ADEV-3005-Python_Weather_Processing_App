"""
    There is one classes in this module.

    Class DBOperations is an sqlite database operation.
        __init__: build a new database connection
        connection_closed: close this database connection
        table_init: create a new table in the database
        insert_dictionary: insert an assigned dictionary to the table
        print_all: print out the data currently in the database
"""

import sqlite3
from common import is_number

from scrape_weather import WeatherScraper


class DBOperations:
    """ create this database context manager """

    def __init__(self, path: str):
        """ build a new database connection """
        self.db_name = path
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ close this database connection """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def initialize_db(self):
        """ create a 'samples' table in the database """
        # self.cursor.execute("drop table %s;" % name)
        with DBOperations(self.db_name) as DBCM:
            sql_initialize_db = """create table if not exists samples (id integer primary key autoincrement not null,
                                        sample_date text not null UNIQUE,
                                        location text not null default %s,
                                        min_temp real not null,
                                        max_temp real not null,
                                        avg_temp real not null); """ % "'StationID=27174'"
            DBCM.execute(sql_initialize_db)

    def save_data(self, data_source: dict):
        """
        receive a dictionary of dictionaries and correctly insert the data into the DB
        :param data_source:
        :return: none
        """
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

        with DBOperations(self.db_name) as DBCM:
            sql_save_data = """INSERT OR IGNORE INTO samples (sample_date,max_temp,min_temp,avg_temp) VALUES (?,?,?,
            ?); """
            for list_item in new_list:
                DBCM.execute(sql_save_data, list_item)
        print('Database updated.')

    def fetch_data(self, year: int, month: int = 0) -> list:
        if month == 0:
            month_str = ''
        elif month < 10:
            month_str = '0' + str(month)
        else:
            month_str = str(month)

        with DBOperations(self.db_name) as DBCM:
            sql_fetch_year_date = f"""SELECT * FROM samples WHERE sample_date LIKE '{year}-{month_str}%';"""
            DBCM.execute(sql_fetch_year_date)
            fetch_weather = DBCM.fetchall()
        return fetch_weather

    def fetch_earliest_one(self) -> list:
        with DBOperations(self.db_name) as DBCM:
            sql_fetch_last_one = """SELECT min(sample_date) FROM samples;"""
            DBCM.execute(sql_fetch_last_one)
            fetch_weather = DBCM.fetchall()
        return fetch_weather

    def fetch_last_one(self) -> list:
        with DBOperations(self.db_name) as DBCM:
            sql_fetch_last_one = """SELECT max(sample_date) FROM samples;"""
            DBCM.execute(sql_fetch_last_one)
            fetch_weather = DBCM.fetchall()
        return fetch_weather

    def purge_data(self):
        print('Purging all the data from the database... ')
        with DBOperations(self.db_name) as DBCM:
            sql_purge_data_1 = """DELETE FROM samples;"""
            sql_purge_data_2 = """DELETE FROM sqlite_sequence WHERE name = 'samples';"""
            DBCM.execute(sql_purge_data_1)
            DBCM.execute(sql_purge_data_2)


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
