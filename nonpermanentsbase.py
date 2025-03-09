from abc import abstractmethod
from corebase import Card

class NonPermanent(Card):
    @abstractmethod
    def resolve(self):
        """Effect of the card when played"""
        pass

class Instant(NonPermanent):
    def resolve(self):
        print(f"{self.name} (Instant) resolves immediately.")
        self.trigger_ability("on_resolve")

    def play(self, game_stack):
        game_stack.add(self)

class Sorcery(NonPermanent):
    def resolve(self):
        print(f"{self.name} (Sorcery) resolves but can only be played on your turn.")
        self.trigger_ability("on_resolve")

    def play(self, game_stack):
        game_stack.add(self)