from permanentsbase import Permanent

# Enchantments
class Enchantment(Permanent):
    def resolve(self):
        """Enchantments resolve and enter the battlefield."""
        print(f"{self.name} (Enchantment) enters the battlefield and affects the game.")