from abc import ABC, abstractmethod

class Stats(ABC):
    def __init__(self):
        self._residue_scores = []
        self._residue_likelihoods = []

    @property
    @abstractmethod
    def residue_scores(self):
        pass

    @residue_scores.setter
    @abstractmethod
    def residue_scores(self, value):
        pass

    @property
    @abstractmethod
    def residue_likelihoods(self):
        pass

    @residue_likelihoods.setter
    @abstractmethod
    def residue_likelihoods(self, value):
        pass