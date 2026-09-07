import json
from pathlib import Path


COUNTRIES_PATH = Path(__file__).resolve().parent.parent / "data" / "countries.json"

with COUNTRIES_PATH.open(encoding="utf-8") as countries_file:
    country_data = json.load(countries_file)

COUNTRIES = tuple(sorted(country_data["countries"].values(), key=str.casefold))
COUNTRY_NAMES = frozenset(COUNTRIES)
