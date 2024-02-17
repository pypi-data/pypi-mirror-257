import json

# all country info
import os


def get_all_cities():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/cities.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_states():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/states.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/countries.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_sub_regions():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/subregions.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_regions():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/regions.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_and_cities_nested():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/countries+cities.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_and_states_nested():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/countries+states.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_states_and_cities_nested():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/states+cities.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_states_and_cities_nested():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../py_countries_states_cities_database/countries+states+cities.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)
