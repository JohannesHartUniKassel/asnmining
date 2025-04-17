import requests
from resources import RIPE_COUNTRY_RESOURCE_LIST_URL


def load_country_data(country: str) -> dict:
    resp = requests.get(RIPE_COUNTRY_RESOURCE_LIST_URL.format(country)).json()
    return resp['data']['resources']['asn']

def load_multiple_country_data(countries: list) -> dict:
    country_asns_ripe = dict()
    for country in countries:
        print("Downloading country {} info...".format(country))
        country_asns_ripe[country] = load_country_data(country)
    return {key: value for key, value in sorted(country_asns_ripe.items(), key=lambda item: item[1], reverse=True)}