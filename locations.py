from permanentsbase import Permanent

# Locations (alternative to Planeswalkers)
class Location(Permanent):
    def __init__(self, name, material_cost, loyalty, owner):
        super().__init__(name, material_cost)
        self.loyalty = loyalty

    def activate_ability(self, ability):
        print(f"{self.name} activates ability: {ability}")
        self.trigger_ability("on_activate_ability", ability)

    def resolve(self):
        """Locations resolve and enter the battlefield."""
        print(f"{self.name} enters with {self.loyalty} loyalty.")

