from permanentsbase import Permanent

class Priest(Permanent):
    def __init__(self, name, owner, primary_material, secondary_material=None):
        super().__init__(name, material_cost=0)
        self.primary_material = primary_material
        self.secondary_material = secondary_material
        
        self.abilities["on_tap"] = self.produce_material
    
    def produce_material(self):
        if not self.tapped:
            self.tapped = True
            self.owner.gain_material(self.primary_material, 1)
            print(f"{self.name} taps to produce 1 {self.primary_material}.")
            
            if self.secondary_material:
                self.owner.gain_material(self.secondary_material, 1)
                print(f"{self.name} also produces 1 {self.secondary_material}.")
        else:
            print(f"{self.name} is already tapped.")
    
    def resolve(self):
        print(f"{self.name} enters the battlefield.")

