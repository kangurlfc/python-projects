import re
import requests
import sys
import tabulate


class City:
    def __init__(self) -> None:
        self.inp = input("City: ").strip().lower().capitalize().replace(' ', '_')

    def __str__(self) -> str:
        ...

    def get_wiki(self):
        # This function ensures the inputs are redirected to the correct Wikipedia page in case of ambiguity.

        response = requests.get("https://en.wikipedia.org/w/rest.php/v1/page/" + self.inp)
        o = response.json()
        return requests.get(
            "https://en.wikipedia.org/" + o["redirect_target"]).json() if "redirect_target" in o else o

    def get_coordinates(self):
        if matches := re.search(
                r"\{\{coord\|((?:\d{1,2}\|){3}[NS])\|(\d{1,3}\|(?:\d{1,2}\|){2}[EW])", self.get_wiki()["source"], re.I):
            return matches.group(1, 2)

    def get_latitude(self):
        degrees, minutes, seconds, card = self.get_coordinates()[0].split('|')
        return f"{degrees}º{minutes}'{seconds}\"{card}"

    def get_longitude(self):
        degrees, minutes, seconds, card = self.get_coordinates()[1].split('|')
        return f"{degrees}º{minutes}'{seconds}\"{card}"

    def get_country(self):
        with open('countries.txt', 'r') as file:
            countries = file.readlines()
        if matches := re.search(r"^\{\{Short description(.+)}}", self.get_wiki()["source"], re.I):
            for country in countries:
                if country.strip().replace('\\n', '') in matches.group(1):
                    return country


def main():

    city = City()
    print(city.get_country())


if __name__ == "__main__":
    main()
