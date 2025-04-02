from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Ingredient:
    quantity: str
    unit: str
    name: str

@dataclass
class IngredientsAll:
    name: str
    ingredients: List[Ingredient]

@dataclass
class Root:
    name: str
    category: str
    tags: List[str]
    preparation_time_minutes: str
    baking_time_minutes: str
    baking_temperature_celcius: str
    cooking_time_minutes: str
    portion: str
    source: str
    ingredients_all: List[IngredientsAll]
    steps: List[str]
    hint: str
