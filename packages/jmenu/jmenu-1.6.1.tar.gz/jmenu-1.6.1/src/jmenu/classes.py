"""
Contains dataclasses jmenu uses to manage data.
This file can be imported and exposes the following classes:

    * MenuItem
    * Restaurant
    * Marker

The following collections are use-case specific to the University of Oulu:

    * MARKERS
    * RESTAURANTS
    * SKIPPED_ITEMS
"""

from typing import NamedTuple
from collections.abc import Iterable, Mapping


class MenuItem(NamedTuple):
    """Dataclass for single menu items and their properties

    Attributes:
        name (str):
            name of the dish
        diets ([str]):
            list of allergen markers

    Methods:
        diets_to_string: returns the list of diets as a joined string.
    """

    name: str
    diets: Iterable[str]

    def diets_to_string(self) -> str:
        """Returns the diets associated with this MenuItem as spaced string."""
        return " ".join(self.diets)


class Restaurant(NamedTuple):
    """Dataclass for relevant restaurant information

    Attributes:
        name (str):
            name of the restaurant
        client_id (int):
            internal jamix identifier used for restaurant providers
        kitchen_id (int):
            internal jamix identifier used to assign menu content
        menu_type (int):
            internal jamix identifier used to classify menus based on content
        relevant_menus ([str]):
            menu names used for filtering out desserts etc.
    """

    name: str
    client_id: int
    kitchen_id: int
    menu_type: int
    relevant_menus: Iterable[str]


class Marker(NamedTuple):
    """Dataclass for allergen information markings

    Attributes:
        letters (str):
            allergen markings
        explanation (dict):
            extended information about the marker, in lang_code: explanation pairs.


    Methods:
        get_explanation(lang: str): returns the explanation string for this Marker. Defaults to english.
    """

    letters: str
    explanation: Mapping

    def get_explanation(self, lang_code: str = "en"):
        "Returns the explanation in the language specified by lang_code. Defaults to english."
        exp = self.explanation.get(lang_code)
        return exp if exp is not None else f"No explanation available for '{lang_code}'"


# TODO: Remove extra space when the API response is fixed
SKIPPED_ITEMS = [
    "proteiinilisäke",
    "Täysjyväriisi",
    "Lämmin kasvislisäke",
    "Höyryperunat",
    "Tumma pasta",
    "Meillä tehty perunamuusi",
    "Mashed Potatoes",
    "Dark Pasta",
    "Whole Grain Rice",
    "Hot Vegetable  Side",  # note the extra space
]

RESTAURANTS = [
    Restaurant("Foobar", 93077, 49, 84, ["Foobar Salad and soup", "Foobar Rohee"]),
    Restaurant("Foodoo", 93077, 48, 89, ["Foodoo Salad and soup", "Foodoo Reilu"]),
    Restaurant("Kastari", 95663, 5, 2, ["Ruokalista"]),
    Restaurant("Kylymä", 93077, 48, 92, ["Kylymä Rohee"]),
    Restaurant("Mara", 93077, 49, 111, ["Salad and soup", "Ravintola Mara"]),
    Restaurant("Napa", 93077, 48, 79, ["Napa Rohee"]),
]

MARKERS = [
    Marker("G", {"fi": "Gluteeniton", "en": "Gluten-free"}),
    Marker("M", {"fi": "Maidoton", "en": "Milk-free"}),
    Marker("L", {"fi": "Laktoositon", "en": "Lactose-free"}),
    Marker("SO", {"fi": "Sisältää soijaa", "en": "Contains soy"}),
    Marker("SE", {"fi": "Sisältää selleriä", "en": "Includes cellery"}),
    Marker("MU", {"fi": "Munaton", "en": "Egg-free"}),
    Marker(
        "[S], *",
        {
            "fi": "Kelan korkeakouluruokailunsuosituksen mukainen",
            "en": "Matches recommendation standards provided by KELA",
        },
    ),
    Marker("SIN", {"fi": "Sisältää sinappia", "en": "Contains mustard"}),
    Marker("<3", {"fi": "Sydänmerkki", "en": "Better choice indicator"}),
    Marker("VEG", {"fi": "Vegaani", "en": "Vegan"}),
]
