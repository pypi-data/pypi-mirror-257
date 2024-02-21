import numpy as np

class NewtonianGrav:
    def __init__(self) -> None:
        self.G = np.float64(6.67430e-11)
        self.Earth_mass = np.float256(5.98e24)
        self.Earth_radius = np.float256(6.37e6)
    def attraction_force(self, mass_1: np.float256, mass_2: np.float256, radius: np.float256):
        return self.G * (mass_1 * mass_2) / radius**2
    def acceleration(self, center_mass: np.float256, radius: np.float256):
        return self.G * center_mass / radius**2
    def escape_velocity(self, center_mass: np.float256, radius: np.float256):
        return np.sqrt(2 * self.G * center_mass / radius)
    def orbital_velocity(self, center_mass: np.float256, radius: np.float256):
        return np.sqrt(self.G * center_mass / radius)
    def gravitational_potential_energy(self, mass_1: np.float256, mass_2: np.float256, radius: np.float256):
        return -self.G * (mass_1 * mass_2) / radius
    def gravitational_kinetic_energy(self, mass_1: np.float256, mass_2: np.float256, radius: np.float256):
        return 1/2 * self.G * mass_1 * mass_2 / radius
    def gravitational_potential(self, mass: np.float256, radius: np.float256):
        return -self.G * mass / radius