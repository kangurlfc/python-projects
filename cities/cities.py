import re
import requests
from tabulate import tabulate


class City:
    def __init__(self, city: str = None) -> None:
        self.inp = (city or input("City: ")).strip().lower().capitalize().replace(' ', '_')
        if not self.inp.replace('_', '').isalpha():
            raise ValueError("Enter a valid city")

    def __str__(self):
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
    def get_wiki(self) -> dict:
        # This function ensures the inputs are redirected to the correct Wikipedia page in case of ambiguity.

        response = requests.get("https://en.wikipedia.org/w/rest.php/v1/page/" + self.inp)
        o = response.json()
        return requests.get(
            "https://en.wikipedia.org/" + o["redirect_target"]).json() if "redirect_target" in o else o

    @property
    def coordinates(self) -> tuple:
        if matches := re.search(
                r"\{\{coord\|((?:\d{1,2}\|){3}[NS])\|(\d{1,3}\|(?:\d{1,2}\|){2}[EW])", self.get_wiki["source"], re.I):
            return matches.group(1, 2)
        else:
            raise ValueError("Invalid city or coordinates unavailable")

    @property
    def population(self) -> str:
        if matches := re.search(
                r"\|\s*population(?:_blank1|_total|_urban)?\s*=\s*(?:{{\w+}} )?([\d,]+(?:\s?[\d,]+)*)",
                self.get_wiki["source"], re.I):
            return matches.group(1)
        else:
            return "n/a"

    @property
    def input_coord(self) -> tuple:
        latitude = self.coordinates[0].replace('|', '.', 1).split('|')[0]
        longitude = self.coordinates[1].replace('|', '.', 1).split('|')[0]
        return (latitude if 'N' in self.coordinates[0] else -float(latitude),
                longitude if 'E' in self.coordinates[1] else -float(longitude))

    @property
    def latitude(self) -> str:
        degrees, minutes, seconds, card = self.coordinates[0].split('|')
        return f"{degrees}º{minutes}'{seconds}\"{card}"

    @property
    def longitude(self) -> str:
        degrees, minutes, seconds, card = self.coordinates[1].split('|')
        return f"{degrees}º{minutes}'{seconds}\"{card}"

    @property
    def country(self) -> str:
        with open('countries.txt', 'r') as file:
            countries = file.readlines()
        if matches := re.search(r"^\{\{Short description(.+)}}", self.get_wiki["source"], re.I):
            for country in countries:
                if country.strip() in matches.group(1):
                    return country.strip()
        else:
            raise ValueError("Enter a valid city")

    @property
    def temperature(self) -> str:
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.input_coord[0]}&"
                                f"longitude={self.input_coord[1]}&current_weather=true")
        o = response.json()
        return f"{o['current_weather']['temperature']}°C"

    @property
    def windspeed(self) -> str:
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.input_coord[0]}&"
                                f"longitude={self.input_coord[1]}&current_weather=true")
        o = response.json()
        return f"{o['current_weather']['windspeed']} km/h"

    @property
    def datetime(self) -> str:
        response = requests.get(
            f"http://api.geonames.org/timezoneJSON?lat={self.input_coord[0]}"
            f"&lng={self.input_coord[1]}&username=demo_1892")
        o = response.json()
        return o['time']


def main():
    all_data = []
    add_more = True
    while add_more:
        city = City()
        city_data = city.__str__()
        all_data.append(city_data)
        print(tabulate(all_data, headers="keys", tablefmt="grid", showindex='always'))
        add_more = another_city()


def another_city():
    while True:
        q1 = input("Would you like to add another city? ").lower().strip()
        if q1 in ['y', 'yes']:
            return True
        elif q1 in ['n', 'no']:
            return False


if __name__ == "__main__":
    main()
