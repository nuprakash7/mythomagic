from creature import Creature
from preists import Priest
from enchantments import Enchantment
from artifacts import Artifact  
from corebase import Stack
import random

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = []
        self.creatures = []  # List of creatures
        self.priests = []    # List of priest-type cards
        self.enchantments = []  # List of enchantments
        self.artifacts = []   # List of artifacts
        self.graveyard = []
        self.material_pool = {"W": 0, "F": 0, "B": 0, "G": 0}  # Wood, Fire, Blood, Gold
        self.health = 20

    def play_card(self, card, game_stack):
        """Play a card from hand onto the battlefield or stack."""
        generic_cost = card.material_cost.get("X", 0)  # Generic cost
        available_generic = sum(self.material_pool.values())  # Sum of all available materials
        
        if card in self.hand and all(self.material_pool.get(mat, 0) >= cost for mat, cost in card.material_cost.items() if mat != "X") and available_generic >= generic_cost:
            for mat, cost in card.material_cost.items():
                if mat != "X":
                    self.material_pool[mat] -= cost

            remaining_generic = generic_cost
            for mat in self.material_pool:
                if remaining_generic > 0:
                    deduction = min(self.material_pool[mat], remaining_generic)
                    self.material_pool[mat] -= deduction
                    remaining_generic -= deduction

            self.hand.remove(card)

            # Place the card in the correct board section
            if isinstance(card, Creature):
                self.creatures.append(card)
            elif isinstance(card, Priest):  
                self.priests.append(card)
            elif isinstance(card, Enchantment):
                self.enchantments.append(card)
            elif isinstance(card, Artifact):
                self.artifacts.append(card)
            else:
                game_stack.add(card)  # If it's a spell, put it on the stack

            print(f"{self.name} plays {card.name}.")
        else:
            print(f"{self.name} cannot play {card.name} due to insufficient materials.")

    def untap_all(self):
        """Untap all permanents on the battlefield."""
        for permanent in self.creatures + self.priests + self.enchantments + self.artifacts:
            permanent.untap()
        print(f"{self.name} untaps all their permanents.")

    def take_damage(self, damage):
        """Reduce player health."""
        self.health -= damage
        print(f"{self.name} takes {damage} damage! Remaining health: {self.health}")
        if self.health <= 0:
            print(f"{self.name} has lost the game!")


class Game:
    def __init__(self, players):
        self.players = players
        self.stack = Stack()
        self.turn = 0  # Index of the active player

    def start_game(self):
        """Start the game by shuffling decks and drawing starting hands."""
        for player in self.players:
            random.shuffle(player.deck)
            for _ in range(7):
                player.draw_card()
        print("Game has started!")
        self.start_turn()

    def start_turn(self):
        """Handles the beginning of a player's turn."""
        active_player = self.players[self.turn]
        print(f"It is now {active_player.name}'s turn.")
        
        self.untap_phase()
        self.upkeep_phase()
        self.draw_phase()
        self.main_phase()
        self.combat_phase()
        self.main_phase()
        self.end_step()
        
        if not self.check_winner():
            self.next_turn()

    def untap_phase(self):
        """Untap all permanents of the active player."""
        active_player = self.players[self.turn]
        active_player.untap_all()
        print(f"{active_player.name} untaps their permanents.")

    def upkeep_phase(self):
        """Handle upkeep triggers and allow only instants or flash spells."""
        active_player = self.players[self.turn]
        print(f"{active_player.name} is in their upkeep phase.")

        while True:
            print("\nUpkeep Phase: Choose an action:")
            print("1. Cast an instant or flash spell")
            print("2. Pass to Draw Phase")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.cast_spell_phase(active_player, allowed_types=["Instant", "Flash"])
            elif choice == "2":
                break
            else:
                print("Invalid choice. Try again.")

    def draw_phase(self):
        """Active player draws a card and can cast instants or flash spells."""
        active_player = self.players[self.turn]
        active_player.draw_card()
        print(f"{active_player.name} draws a card.")

        while True:
            print("\nDraw Phase: Choose an action:")
            print("1. Cast an instant or flash spell")
            print("2. Pass to Main Phase")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.cast_spell_phase(active_player, allowed_types=["Instant", "Flash"])
            elif choice == "2":
                break
            else:
                print("Invalid choice. Try again.")

    def main_phase(self):
        """Handles the active player's main phase where they can cast all spells."""
        active_player = self.players[self.turn]
        print(f"{active_player.name} is in their main phase.")

        while True:
            print("\nMain Phase: Choose an action:")
            print("1. Cast a spell")
            print("2. Pass to Combat Phase")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.cast_spell_phase(active_player, allowed_types=["Instant", "Flash", "Sorcery", "Creature", "Enchantment", "Artifact", "Planeswalker"])
            elif choice == "2":
                break
            else:
                print("Invalid choice. Try again.")

    def end_step(self):
        """Handles the end step, allowing only instants or flash spells."""
        active_player = self.players[self.turn]
        print(f"{active_player.name} is in their end step.")

        while True:
            print("\nEnd Step: Choose an action:")
            print("1. Cast an instant or flash spell")
            print("2. Pass to next turn")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.cast_spell_phase(active_player, allowed_types=["Instant", "Flash"])
            elif choice == "2":
                break
            else:
                print("Invalid choice. Try again.")

    def cast_spell_phase(self, active_player, allowed_types):
        """Allows the player to cast only valid spells for the current phase."""
        valid_cards = [card for card in active_player.hand if card.type in allowed_types]

        if not valid_cards:
            print(f"You have no {', '.join(allowed_types)} spells to cast.")
            return

        print("\nYour Hand:")
        for i, card in enumerate(valid_cards):
            print(f"{i}: {card.name} - Type: {card.type}, Cost: {card.material_cost}")

        choice = input("Enter the number of the card to cast, or press Enter to cancel: ")

        if choice.isdigit():
            index = int(choice)
            if 0 <= index < len(valid_cards):
                card = valid_cards[index]
                active_player.play_card(card, self.stack)
            else:
                print("Invalid selection.")
        else:
            print("Cancelled spell casting.")

        # Allow the player to play spells or abilities

    def combat_phase(self):
        active_player = self.players[self.turn]
        print(f"{active_player.name} enters the combat phase.")

        while True:
            print("\nCombat Phase: Choose an action:")
            print("1. Cast an instant or flash spell")
            print("2. Declare attackers")
            print("3. Pass to Main Phase 2")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.cast_spell_phase(active_player, allowed_types=["Instant", "Flash"])
            elif choice == "2":
                if not active_player.creatures:
                    print(f"{active_player.name} has no creatures to attack with.")
                    return

                attackers = []
                print("Choose attackers (enter indices separated by space, or press enter to skip):")
                for i, creature in enumerate(active_player.creatures):
                    print(f"{i}: {creature.name} ({creature.power}/{creature.toughness})")

                selected_attackers = input().split()#change later for UI integration
                if selected_attackers:
                    target_player = self.choose_defender(active_player)
                    for index in selected_attackers:
                        if index.isdigit():
                            index = int(index)
                            if 0 <= index < len(active_player.creatures):
                                creature = active_player.creatures[index]
                                creature.attack(target_player)
                                attackers.append(creature)

                # Step 2: Declare Blockers
                if not attackers:
                    print(f"{active_player.name} chose not to attack.")
                    return

                blockers = {}
                for defender in self.players:
                    if defender == active_player:
                        continue

                    print(f"{defender.name}, choose blockers for each attacker.")
                    for attacker in attackers:
                        print(f"{attacker.name} is attacking.")
                        available_blockers = [creature for creature in defender.creatures if not creature.summoning_sick]
                        if not available_blockers:
                            print(f"{defender.name} has no creatures to block with.")
                            continue

                        print("Choose blockers (enter indices separated by space, or press enter to skip):")
                        for i, creature in enumerate(available_blockers):
                            print(f"{i}: {creature.name} ({creature.power}/{creature.toughness})")

                        selected_blockers = input().split()
                        if selected_blockers:
                            blockers[attacker] = []
                            for index in selected_blockers:
                                if index.isdigit():
                                    index = int(index)
                                    if 0 <= index < len(available_blockers):
                                        blocker = available_blockers[index]
                                        blocker.block(attacker)
                                        blockers[attacker].append(blocker)

                # Step 3: Assign Combat Damage
                for attacker in attackers:
                    if attacker in blockers:
                        damage_to_player = attacker.assign_combat_damage(blockers[attacker])
                        if damage_to_player > 0:
                            target_player.take_damage(damage_to_player)
                    else:
                        print(f"{attacker.name} deals {attacker.power} damage to {target_player.name}!")
                        target_player.take_damage(attacker.power)
            else:
                break


   
        """Handles the end step and cleanup phase."""
        active_player = self.players[self.turn]
        active_player.trigger_ability("on_end_step")
        print(f"{active_player.name} is in their end step.")

    def next_turn(self):
        """Proceed to the next player's turn."""
        self.turn = (self.turn + 1) % len(self.players)
        self.start_turn()

    def resolve_stack(self):
        """Resolve everything on the stack."""
        print("Resolving the stack...")
        self.stack.resolve_all()

    def check_winner(self):
        """Check if a player has won the game."""
        alive_players = [p for p in self.players if p.health > 0]
        if len(alive_players) == 1:
            print(f"{alive_players[0].name} wins the game!")
            return True
        return False