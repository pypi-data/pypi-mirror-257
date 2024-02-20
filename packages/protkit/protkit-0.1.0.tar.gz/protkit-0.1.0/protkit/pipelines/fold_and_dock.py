from protkit.structure.protein import Protein
from protkit.seq.sequence import Sequence

from protkit.pipelines.pipeline import Pipeline

from protkit.tasks.dock_engine import DockEngine
from protkit.tasks.sequence_to_structure import SequenceToStructure


class FoldAndDock:
    def __init__(self, dock_engine: DockEngine, folder: SequenceToStructure):
        self.dock_engine = dock_engine
        self.folder = folder

    def fold_and_dock(self, antigen: Protein, antibody: Sequence) -> Protein:
        antibody_structure = self.folder.fold_monomer(antibody)
        complex_structure: Protein = self.dock_engine.blind_dock(antigen, antibody_structure)
        print("fold and dock 1")
        return complex_structure

class FoldAndDock2(Pipeline):
    def __init__(self, dock_engine: DockEngine, folder: SequenceToStructure):
        # super().__init__(dock_engine, folder)
        self.dock_engine = dock_engine
        self.folder = folder

    def fit(self, *args):
        antibody_structure = self.folder.fold_monomer(args[1])
        complex_structure: Protein = self.dock_engine.blind_dock(args[0], antibody_structure)
        print("fold and dock 2")
        return complex_structure