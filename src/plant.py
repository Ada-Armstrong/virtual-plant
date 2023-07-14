from abc import ABC


class PlantComponent(ABC):
    """
    Represents a part of the plant, for example a stem or leaf.
    """
    age: int
    size: int
    growth_factor: int

    def __init__(self, growth_factor):
        self.age = 0
        self.size = 1
        self.growth_factor = growth_factor

    def sun_exposure(self):
        raise NotImplementedError()

    def get_water(self):
        raise NotImplementedError()

    def grow(self, sugar_amount: int):
        self.size += sugar_amount*self.growth_factor

class Seed(PlantComponent):
    """
    It's a sneed.
    """
    def __init__(self):
        seed_growth_factor = 5
        super().__init__(seed_growth_factor)

    def sun_exposure(self):
        return 3

    def get_water(self):
        return 3

class PlantModel(ABC):
    """
    An abstract base class that represents the interface for a plant.
    """
    sugar: int
    water: int
    age: int
    components: list[PlantComponent]

    def __init__(self):
        self.sugar = 0
        self.water = 0
        self.age = 0
        self.components = []

    def add_water(self, amount: int):
        self.water += amount

    def get_water(self):
        for component in self.components:
            self.add_water(component.get_water())

    def sun_exposure(self):
        exposure = 0
        for component in self.components:
            exposure += component.sun_exposure()
        return exposure

    def photosynthesize(self):
        sunlight_threshold: int = 5
        sunlight_burn_threshold: int = 10
        water_threshold: int = 5

        sunlight = self.sun_exposure()
        burnt = sunlight > sunlight_threshold

        if burnt:
            water_threshold *= 2

        if sunlight > sunlight_threshold and self.water > water_threshold:
            self.sugar += 5
            self.water -= water_threshold

    def grow(self):
        sugar_per_component = self.sugar / len(self.components)
        for component in self.components:
            component.grow(sugar_per_component)

