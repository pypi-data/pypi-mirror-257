from protkit.properties.interaction import Interface
from protkit.structure.protein import Protein
from protkit.structure.antibody import Antibody
from protkit.util.stats import Stats


class Paratope:
    def __init__(self, antibody: Antibody):
        self.antibody = antibody
        self.interface = None
        self.prediction = {}

    def identify_from_interface(self, antigen: Protein, cut_off_distance=4.5):
        # Create an Interface object
        self.interface = Interface(self.antibody, antigen, cut_off_distance)
        interface = self.interface

        return interface

    def predict(self, tool_name):

        # Stats object returned by tool
        # TODO: Impliment way to get stats object from tool
        stats = Stats()

        self.prediction[tool_name] = stats

