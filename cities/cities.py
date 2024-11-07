import re
import requests
import tabulate


class City:
    def __init__(self) -> None:
        self.inp = input("City: ").strip().lower().capitalize().replace(' ', '_')
        # maybe i should let the user pass in an argument as well

    def __str__(self):
        # this would print every attribute
        ...

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

    @property
    def population(self) -> str:
        if matches := re.search(
                r"\|\s*population(?:(?:_blank1)|(?:_total)|(?:_urban)?)\s*=\s*(?:{{\w+}} )?([\d, ]+)", self.get_wiki["source"], re.I):
            # kraków? munich glasgow perth
            return matches.group(1)

    @property
    def input_coord(self) -> tuple:
        latitude = self.coordinates[0].replace('|', '.', 1).split('|')[0]
        longitude = self.coordinates[1].replace('|', '.', 1).split('|')[0]
        return latitude, longitude

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

    city = City()
    print(city.population)


if __name__ == "__main__":
    main()
