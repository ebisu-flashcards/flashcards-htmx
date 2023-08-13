from typing import Dict
from abc import ABC, abstractmethod
import random

from jinja2 import Template


class Algorithm(ABC):

    def buttons(self):
        return {
            "correct": "var(--success)",
            "wrong": "var(--danger)",
        }

    @abstractmethod
    def next_card(self, deck, schemas):
        ...

    @abstractmethod
    def process_result(self, deck, card_id, card_type, result):
        ...


class Random(Algorithm):
    
    def next_card(self, deck, schemas):
        card_id, card_data = random.choice(list(deck["cards"].items()))
        card_schema = schemas[card_data["schema"]]
        card_type, card = random.choice(list(card_schema["cards"].items()))
        question = Template(card["question"]).render(**card_data)
        answer = Template(card["answer"]).render(**card_data)
        return card_id, card_type, question, answer

    def process_result(self, deck, card_id, card_type, result):
        pass


class HardestFirst(Algorithm):

    def buttons(self):
        return {
            "correct": "var(--success)",
            "wrong": "var(--danger)",
        }
    
    def next_card(self, deck, schemas):
        print(schemas)

        card_id, card_data = random.choice(list(deck["cards"].items()))
        card_schema = schemas[card_data["schema"]]
        card_type, card = random.choice(list(card_schema["cards"].items()))
        question = Template(card["question"]).render(**card_data)
        answer = Template(card["answer"]).render(**card_data)
        return card_id, card_type, question, answer
    
    def process_result(self, deck, card_id, card_type, result):
        card_data = deck["cards"][card_id]
        if result == "correct":
            card_data["reviews"][card_type] = card_data["reviews"].get(card_type, 0) + 1
        else:
            reviews = []
            for card_data in deck["cards"].values():
                reviews += card_data.get("reviews", {}).values()
            card_data["reviews"][card_type] = max(min(reviews or []) - 1, 0)

        reviews = []
        for card_data in deck["cards"].values():
            reviews += card_data.get("reviews", {}).values()
        print(card_data["preview"], "storing", card_data["reviews"][card_type] , "values: ", reviews)


ALGORITHMS: Dict[str, Algorithm] = {
    "Random": Random(),
    "HardestFirst": HardestFirst(),
}