import os
import textwrap

from dotenv import load_dotenv, find_dotenv


class Configurator:
    def __init__(self):
        self.env_exists = load_dotenv()
        self.geocode_auth = os.getenv('GEOCODE_AUTH') if self.env_exists else None
        self.datahub_api_key = os.getenv('DATAHUB_API_KEY') if self.env_exists else None
        self.datahub_secret = os.getenv('DATAHUB_SECRET') if self.env_exists else None

    def initial_setup(self):
        """
        Takes 3 inputs from stdin for the geocode.xyz auth token, Met Office Weather DataHub API key and secret,
        which is then written out to a new .env file to use with the program.
        """
        self.geocode_auth = input("Please enter your geocode.xyz auth token: ")
        self.datahub_api_key = input("Please enter your Met Office Weather DataHub API key: ")
        self.datahub_secret = input("Please enter your Met Office Weather DataHub API secret: ")
        self.generate_dotenv()

    def generate_dotenv(self):
        mode = 'w'
        if find_dotenv() == '':
            mode = 'x'
        with open('./.env', mode) as file:
            file.write(textwrap.dedent(f"""\
            GEOCODE_AUTH={self.geocode_auth}
            DATAHUB_API_KEY={self.datahub_api_key}
            DATAHUB_SECRET={self.datahub_secret}
            """))
            print(f"Saved dotenv file at {os.getcwd()}/.env")


if __name__ == '__main__':
    configurator = Configurator()
    configurator.initial_setup()
