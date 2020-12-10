"""
The entrance of this App.
"""
import logging

from weather_processor import WeatherProcessor


def main():
    """
    The entrance of this App.
    :return:
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s  %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S +0000',
                        filename='error_handler.log',
                        filemode='a')

    my_wp = WeatherProcessor()
    my_wp.exe_welcome()


if __name__ == '__main__':
    main()
