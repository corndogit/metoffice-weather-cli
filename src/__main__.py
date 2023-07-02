import argparse
import sys
import weather


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="weather-cli",
        description="A CLI tool for fetching the weather"
    )
    parser.add_argument('-c', '--config',
                        action='store_true',
                        help="Configures the .env file"
                        )
    parser.add_argument('-s', '--search',
                        action='store',
                        nargs=1,
                        metavar='location',
                        help="Fetch and print the weather given the name of a city or town"
                        )
    parser.add_argument('-g', '--geocode',
                        action='store',
                        nargs=1,
                        metavar='location',
                        help="Fetch and print the latitude and longitude coordinates of a city or town"
                        )
    parser.add_argument('-w', '--weather',
                        action='store',
                        nargs=2,
                        type=float,
                        metavar=('latitude', 'longitude'),
                        help="Fetch and print the weather at a set of latitude and longitude coordinates.",
                        )

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
