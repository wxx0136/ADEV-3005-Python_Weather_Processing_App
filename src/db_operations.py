"""
    There are one classes in this module.

    Class DBOperations is an sqlite database operation.
        __init__: build a new database connection
        connection_closed: close this database connection
        table_init: create a new table in the database
        insert_dictionary: insert an assigned dictionary to the table
        print_all: print out the data currently in the database
"""

import sqlite3


class DBOperations:
    """ create this database context manager """

    def __init__(self, name: str):
        """ build a new database connection """

        self.db_name = name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def connection_closed(self):
        """ close this database connection """

        self.cursor.close()
        self.conn.close()

    def table_init(self, name: str):
        """ create a new table in the database """

        # self.cursor.execute("drop table %s;" % name)
        sql = """create table if not exists %s (id integer primary key autoincrement not null,
                                    sample_date text not null,
                                    location text not null default %s,
                                    min_temp real not null,
                                    max_temp real not null,
                                    avg_temp real not null); """ % (name, "'Winnipeg, MB'")
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_dictionary(self, table: str, input_dict: dict):
        """
        receive a dictionary of dictionaries and correctly insert the data into the DB
        :param table:
        :param input_dict:
        :return: none
        """

        new_list = []
        for key, value in input_dict.items():
            new_row = [key]
            for nest_key, nest_value in value.items():
                new_row.append(nest_value)
            new_list.append(tuple(new_row))

        # values = ', '.join(map(str, tuple(new_list)))
        # sql = """INSERT INTO %s """ % table_name + """(date,max_temp,min_temp,avg_temp) VALUES {}""".format(values)
        # print("SQL for insert_dictionary function: ", sql)
        # self.cursor.execute(sql)
        # self.conn.commit()

        for item in new_list:
            sql = """INSERT INTO %s """ % table + """(sample_date,max_temp,min_temp,avg_temp) VALUES (?,?,?,?)"""
            self.cursor.execute(sql, item)
        self.conn.commit()

    def print_all(self, table: str):
        """ print out the data currently in the database. """
        sql = """select * from %s;""" % table
        self.cursor.execute(sql)
        print("Current data in this database: ", self.cursor.fetchall())
        self.conn.commit()


if __name__ == '__main__':
    my_db_name = 'weather.sqlite'
    my_table_name = 'samples'
    db = DBOperations(my_db_name)

    db.table_init(my_table_name)

    weather = {
        "2018-06-01": {"Max": 12.0, "Min": 5.6, "Mean": 7.1},
        "2018-06-02": {"Max": 22.2, "Min": 11.1, "Mean": 15.5},
        "2018-06-03": {"Max": 31.3, "Min": 29.9, "Mean": 30.0}
    }
    db.insert_dictionary(my_table_name, weather)

    db.print_all(my_table_name)

    db.connection_closed()
