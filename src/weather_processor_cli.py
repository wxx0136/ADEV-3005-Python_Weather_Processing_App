import sys

from db_operations import DBOperations


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
        menu_0 = {
            '1': 'Fetch all new data from the website.',
            '2': 'Update data between today and the latest date in the database.',
            '3': 'Generate a plot.',
            '4': 'Exit.'
        }
        options = menu_0.keys()
        for entry in options:
            print(entry, menu_0[entry])

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
        pass


if __name__ == '__main__':
    my_wp = WeatherProcessor()
    my_wp.exe_welcome()



