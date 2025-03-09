from corebase import Card

class Permanent(Card):
    def __init__(self, name, material_cost, owner, keywords=None):
        super().__init__(name, material_cost, owner)
        self.tapped = False
        self.keywords = keywords if keywords else set()
        self.zone = "battlefield"  # Track where the card is
        
    def tap(self):
        if not self.tapped:
            self.tapped = True
            print(f"{self.name} is now tapped.")
            self.trigger_ability("on_tap")
        else:
            print(f"{self.name} is already tapped.")

    def untap(self):
        self.tapped = False
        print(f"{self.name} is now untapped.")
        self.trigger_ability("on_untap")

    def resolve(self):
        """When a permanent resolves, it enters the battlefield."""
        print(f"{self.name} enters the battlefield.")
        self.trigger_ability("on_enter")
        self.zone = "battlefield"

    def play(self, game_stack):
        """Permanents go on the stack before resolving and entering the battlefield."""
        game_stack.add(self)
    
    def can_be_targeted(self, spell):
        """Checks if a permanent can be targeted by a spell, considering Hexproof and Ward"""
        if "Hexproof" in self.keywords and spell.owner.opponent:
            print(f"{self.name} has Hexproof and cannot be targeted by opponent's spells!")
            return False
        return True
    
    def move_to_graveyard(self):
        """Moves the permanent to the graveyard."""
        print(f"{self.name} goes to the graveyard.")
        self.zone = "graveyard"
        self.trigger_ability("on_graveyard")

    def move_to_exile(self):
        """Moves the permanent to exile."""
        print(f"{self.name} is exiled.")
        self.zone = "exile"
        self.trigger_ability("on_exile")

    def add_activated_ability(self, ability_name, ability_function, condition_function=None):
        """Adds an activated ability with an optional condition function."""
        self.activated_abilities[ability_name] = (ability_function, condition_function)

    def activate_ability(self, ability_name, *args):
        """Activates a specified ability of the permanent if conditions are met."""
        if ability_name in self.activated_abilities:
            ability_function, condition_function = self.activated_abilities[ability_name]
            if condition_function is None or condition_function():
                print(f"{self.name} activates {ability_name}.")
                ability_function(*args)
            else:
                print(f"{self.name} cannot activate {ability_name} due to unmet conditions.")
        else:
            print(f"{self.name} does not have the ability {ability_name}.")


