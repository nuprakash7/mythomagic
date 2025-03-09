
from permanentsbase import Permanent

# Creatures
class Creature(Permanent):
    def __init__(self, name, mana_cost, power, toughness, owner, keywords=None):
        super().__init__(name, mana_cost)
        self.power = power
        self.toughness = toughness
        self.keywords = keywords if keywords else set()
        self.summoning_sick = True  # Prevents attacking the turn it enters unless it has Haste

    def resolve(self):
        """Handles entering the battlefield"""
        self.summoning_sick = True
        self.trigger_ability("on_enter")

    def attack(self, player):
        """Declares this creature as an attacker"""
        if "Defender" in self.keywords:
            print(f"{self.name} has Defender and cannot attack!")
            return
        
        if self.summoning_sick and "Haste" not in self.keywords:
            print(f"{self.name} is summoning sick and cannot attack!")
            return

        print(f"{self.name} is attacking {player.name}.")
        self.trigger_ability("on_attack")
        if "Vigilance" not in self.keywords:
            self.tap()  # Does not tap if it has Vigilance

    def block(self, attacker):
        """Blocks an attacking creature"""
        if "Flying" in attacker.keywords and "Flying" not in self.keywords and "Reach" not in self.keywords:
            print(f"{self.name} cannot block {attacker.name} because it has Flying.")
            return

        if "Menace" in attacker.keywords:
            print(f"{attacker.name} has Menace and must be blocked by at least two creatures.")
            return

        print(f"{self.name} is blocking {attacker.name}.")
        self.trigger_ability("on_block", attacker)

    def assign_combat_damage(self, blockers):
        """Handles combat damage assignment, including First Strike, Double Strike, Trample, and Deathtouch"""
        total_block_power = sum(b.power for b in blockers)

        # First Strike / Double Strike Damage Step
        if "First Strike" in self.keywords or "Double Strike" in self.keywords:
            for blocker in blockers:
                if "Deathtouch" in self.keywords:
                    blocker.destroy()
                else:
                    blocker.take_damage(self.power)
                if blocker.toughness <= 0:
                    blockers.remove(blocker)

        # Regular Damage Step
        if "Double Strike" in self.keywords or "First Strike" not in self.keywords:
            for blocker in blockers:
                if "Deathtouch" in self.keywords:
                    blocker.destroy()
                else:
                    blocker.take_damage(self.power)

        # Trample Damage
        if "Trample" in self.keywords and total_block_power < self.power:
            trample_damage = self.power - total_block_power
            return trample_damage  # Excess damage to player
        return 0

    def take_damage(self, damage):
        """Creature takes damage, considering Indestructible, Lifelink, and Deathtouch"""
        if "Indestructible" in self.keywords:
            print(f"{self.name} is Indestructible and takes no lethal damage!")
            return

        self.toughness -= damage

        if "Lifelink" in self.keywords:
            print(f"{self.name} has Lifelink! Controller gains {damage} life.")

        if self.toughness <= 0:
            self.trigger_ability("on_destroy")
            print(f"{self.name} is destroyed!")

    



