from permanentsbase import Permanent

# Artifacts

class Artifact(Permanent):
    def resolve(self):
        """Artifacts resolve and enter the battlefield."""
        print(f"{self.name} (Artifact) enters the battlefield with special effects.")