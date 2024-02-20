from abc import ABC, abstractmethod
from protkit.structure.protein import Protein
from protkit.util.simulation_parameters import SimulationParameters
from protkit.util.trajectory import Trajectory


class MolecularDynamicsEngine(ABC):
    """
    The MDSimulator abstract base class defines the interface for a molecular dynamics (MD) simulator.

    Molecular dynamics simulations are computational methods used to simulate the physical movements
    of atoms and molecules. They are essential for understanding the structure, dynamics, and
    thermodynamics of biological macromolecules such as proteins.

    Implementations of this class should provide mechanisms to set up, run, and analyze the
    molecular dynamics simulations for given protein structures.
    """

    def __init__(self):
        pass


    @abstractmethod
    def simulate(self, protein: Protein, parameters: SimulationParameters) -> Trajectory:
        """
        Runs a molecular dynamics simulation on the given protein with the specified parameters.

        Parameters:
            protein (Protein): The protein object to simulate.
            parameters (SimulationParameters): The parameters specifying how the simulation should be conducted.

        Returns:
            Trajectory: A trajectory object that has been subject to the MD simulation,
                     with updated coordinates and properties reflecting the simulation outcome.
        """
        trajectory = Trajectory()
        return trajectory
