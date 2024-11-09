import re
import requests
from tabulate import tabulate


class CityApi:
    # This class gets data via APIs
    @staticmethod
    def get_wiki_data(city: str) -> dict:
        # This function gets data and redirects to the correct Wikipedia page in case of ambiguity.
        response = requests.get("https://en.wikipedia.org/w/rest.php/v1/page/" + city)
        if response.status_code == 200:
            o = response.json()
            if "redirect_target" in o:
                response = requests.get("https://en.wikipedia.org/" + o["redirect_target"])
            return response.json()
        else:
            raise Exception("Failed to retrieve data")

    @staticmethod
    def get_meteo(latitude: float, longitude: float):
        # Gets meteorological data of a location based on latitude nad longitude
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
                                f"&current_weather=true")
        return response.json()

    @staticmethod
    def get_datetime(latitude: float, longitude: float):
        # Gets gets current date and time of a location based on latitude nad longitude
        response = requests.get(
            f"http://api.geonames.org/timezoneJSON?lat={latitude}&lng={longitude}&username=demo_1892")
        return response.json()


class City:
    COUNTRIES = set(line.strip() for line in open('countries.txt'))

    def __init__(self, city: str | None = None) -> None:
        self.inp = (city or input("City: ")).strip().lower().capitalize().replace(' ', '_')
        if not self.inp.replace('_', '').isalpha():
            raise ValueError("Enter a valid city")

        self.wiki = CityApi.get_wiki_data(self.inp)

        if self.input_coord != 'n/a':
            self.meteo = CityApi.get_meteo(self.input_coord[0], self.input_coord[1])
        else:
            self.meteo = 'n/a'

        if self.input_coord != 'n/a':
            self.get_datetime = CityApi.get_datetime(self.input_coord[0], self.input_coord[1])
        else:
            self.get_datetime = 'n/a'

    def __str__(self) -> dict:
        # Returns a dictionary of acquired data
        table = {
            "City": self.inp.replace('_', ' ').title(),
            "Country": self.country,
            "Latitude": self.latitude,
            "Longitude": self.longitude,
            "Population": self.population,
            "Local date & time": self.datetime,
            "Temperature": self.temperature,
            "Windspeed": self.windspeed
        }
        return table

    @property
    def coordinates(self) -> tuple | str:
        # Gets coordinates of a location from Wikipedia
        if matches := re.search(
                r"\{\{coord\|((?:\d{1,2}\|){3}[NS])\|(\d{1,3}\|(?:\d{1,2}\|){2}[EW])", self.wiki["source"], re.I):
            return matches.group(1, 2)
        else:
            return "n/a"

    @property
    def population(self) -> int | str:
        # Gets population of a city from Wikipedia
        if matches := re.search(
                r"\|\s*population(?:_blank1|_total|_urban)?\s*=\s*(?:{{\w+}} )?([\d,]+(?:\s?[\d,]+)*)",
                self.wiki["source"], re.I):
            return f"{int(matches.group(1).replace(',', '').replace(' ', '')):,d}"
        else:
            return "n/a"

    @property
    def input_coord(self) -> tuple | str:
        # Converts fetched coordinates to a format used by other APIs
        if self.coordinates != 'n/a':
            latitude = self.coordinates[0].replace('|', '.', 1).split('|')[0]
            longitude = self.coordinates[1].replace('|', '.', 1).split('|')[0]
            return (latitude if 'N' in self.coordinates[0] else -float(latitude),
                    longitude if 'E' in self.coordinates[1] else -float(longitude))
        else:
            return 'n/a'

    @property
    def latitude(self) -> str:
        # Outputs latitude based on coordinates
        if self.coordinates != 'n/a':
            degrees, minutes, seconds, card = self.coordinates[0].split('|')
            return f"{degrees}º{minutes}'{seconds}\"{card}"
        else:
            return 'n/a'

    @property
    def longitude(self) -> str:
        # Outputs longitude based on coordinates
        if self.coordinates != 'n/a':
            degrees, minutes, seconds, card = self.coordinates[1].split('|')
            return f"{degrees}º{minutes}'{seconds}\"{card}"
        else:
            return 'n/a'

    @property
    def country(self) -> str | None:
        # Outputs the country by comparing a full list of countries to see if any of them appear in the Wiki description
        if matches := re.search(r"^\{\{Short description(.+)}}", self.wiki["source"], re.I):
            for country in City.COUNTRIES:
                if country in matches.group(1):
                    return country
        else:
            raise KeyError("Enter a valid city")
        return None

    @property
    def temperature(self) -> str:
        # Outputs temperature based on coordinates
        if isinstance(self.meteo, dict) and 'current_weather' in self.meteo:
            return f"{self.meteo['current_weather']['temperature']}°C"
        else:
            return 'n/a'

    @property
    def windspeed(self) -> str:
        # Outputs wind speed based on coordinates
        if isinstance(self.meteo, dict) and 'current_weather' in self.meteo:
            return f"{self.meteo['current_weather']['windspeed']} km/h"
        else:
            return 'n/a'

    @property
    def datetime(self) -> str:
        # Outputs date and time based on coordinates
        if isinstance(self.get_datetime, dict) and 'time' in self.get_datetime:
            return self.get_datetime['time']
        else:
            return 'n/a'


def main():
    all_data = []
    add_more = True
    while add_more:
        city = City()
        city_data = city.__str__()
        all_data.append(city_data)
        table = tabulate(all_data, headers="keys", tablefmt="grid", showindex=range(1, len(all_data) + 1))
        print(table)
        add_more = another_city(table)


def another_city(t) -> bool:
    while True:
        q1 = input("Would you like to add another city? ").lower().strip()
        if q1 in ['y', 'yes']:
            return True
        elif q1 in ['n', 'no']:
            save(t)
            return False


def save(t: str) -> None:
    while True:
        q2 = input("Do you want to save the table? ").lower().strip()
        if q2 in ['y', 'yes']:
            with open('cities.txt', 'w', encoding='utf-8') as f:
                f.write(t)
            print("Table saved")
            return
        elif q2 in ['n', 'no']:
            return


if __name__ == "__main__":
    main()
