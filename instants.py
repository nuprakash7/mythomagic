from nonpermanentsbase import NonPermanent


class Instant(NonPermanent):
    def resolve(self):
        print(f"{self.name} (Instant) resolves immediately.")
        self.trigger_ability("on_resolve")

    def play(self, game_stack):
        game_stack.add(self)