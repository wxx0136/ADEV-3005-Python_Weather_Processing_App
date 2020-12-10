"""
The entrance of this App.
"""

from weather_processor import WeatherProcessor


def main():
    """
    The entrance of this App.
    :return:
    """
    my_wp = WeatherProcessor()
    my_wp.exe_welcome()


if __name__ == '__main__':
    main()
