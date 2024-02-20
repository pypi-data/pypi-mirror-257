class SimulationParameters:
    """
    Holds the parameters required to setup and run a molecular dynamics simulation.

    Attributes:
        temperature (float): The temperature at which to perform the simulation, in Kelvin.
        pressure (float): The pressure at which to perform the simulation, in bar.
        timestep (float): The timestep of the simulation, in femtoseconds.
        duration (float): The total duration of the simulation, in nanoseconds.
        output_frequency (int): The frequency at which to output data, in steps.
    """

    def __init__(self, temperature: float, pressure: float, timestep: float, duration: float, output_frequency: int):
        """
        Initializes the simulation parameters with the provided values.

        Parameters:
            temperature (float): The simulation temperature in Kelvin.
            pressure (float): The simulation pressure in bar.
            timestep (float): The simulation timestep in femtoseconds.
            duration (float): The total duration of the simulation in nanoseconds.
            output_frequency (int): The number of steps between data outputs.
        """
        self.temperature = temperature
        self.pressure = pressure
        self.timestep = timestep
        self.duration = duration
        self.output_frequency = output_frequency

    def __repr__(self):
        """
        Returns a string representation of the simulation parameters.

        Returns:
            str: A string representation of the SimulationParameters object.
        """
        return (f"SimulationParameters(temperature={self.temperature}, pressure={self.pressure}, "
                f"timestep={self.timestep}, duration={self.duration}, output_frequency={self.output_frequency})")
