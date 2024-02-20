import os
import json

# all country info
from pkg_resources import resource_filename


def get_all_cities():
    with open(
        resource_filename(__name__, "py_countries_states_cities_database/cities.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_states():
    with open(
        resource_filename(__name__, "py_countries_states_cities_database/states.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries():
    with open(
        resource_filename(
            __name__, "py_countries_states_cities_database/countries.json"
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_sub_regions():
    with open(
        resource_filename(
            __name__, "py_countries_states_cities_database/subregions.json"
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_regions():
    with open(
        resource_filename(__name__, "py_countries_states_cities_database/regions.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_and_cities_nested():
    with open(
        resource_filename(
            __name__, "py_countries_states_cities_database/countries+cities.json"
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_and_states_nested():
    with open(
        resource_filename(
            __name__, "py_countries_states_cities_database/countries+states.json"
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_states_and_cities_nested():
    with open(
        resource_filename(
            __name__, "py_countries_states_cities_database/states+cities.json"
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_states_and_cities_nested():
    with open(
        resource_filename(
            __name__,
            "py_countries_states_cities_database/countries+states+cities.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)
