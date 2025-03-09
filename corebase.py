from abc import ABC, abstractmethod
import random

# Stack to handle spell and ability resolution
class Stack:
    def __init__(self):
        self.stack = []

    def add(self, item):
        """Add an item to the stack (spells, abilities, permanents entering)."""
        print(f"Added {item.name} to the stack.")
        self.stack.append(item)

    def resolve_top(self):
        """Resolve the top item of the stack (Last In, First Out)."""
        if self.stack:
            item = self.stack.pop()
            print(f"Resolving {item.name}...")
            item.resolve()
        else:
            print("The stack is empty.")

    def resolve_all(self):
        """Resolve everything on the stack in order."""
        while self.stack:
            self.resolve_top()

# Base Card Class
class Card(ABC):
    def __init__(self, name, material_cost, owner):
        self.name = name
        self.material_cost = material_cost
        self.owner = owner  # The player who owns the card
        self.controller = owner  # The player currently controlling the card
        self.abilities = {}  # Dictionary for triggered abilities

    @abstractmethod
    def play(self, game_stack):
        """Defines how a card is played"""
        pass

    def trigger_ability(self, event, *args):
        """Triggers an ability based on an event."""
        if event in self.abilities:
            self.abilities[event](*args)

# Player Class
