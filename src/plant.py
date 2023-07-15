from abc import ABC

# light level is in the range 0 - 255
MIN_LIGHT_AMT = 0
LOW_LIGHT_AMT = 50
HIGH_LIGHT_AMT = 200
MAX_LIGHT_AMT = 255

class PlantComponent(ABC):
    """
    Represents a part of the plant, for example a stem or leaf.
    """
    MAX_HEALTH: int = 100
    MAX_SIZE: int = 50

    def __init__(self, environment, growth_factor, water_absorbtion, light_absorbtion):
        self.sugar: int = 0
        self.water: int = 0
        self.age: int = 0
        self.size: int = 1
        self.env = environment
        self.health: int = self.MAX_HEALTH
        self.growth_factor: int = growth_factor

        self.water_absorbtion: int = water_absorbtion

        self.light_absorbtion: int = light_absorbtion
        self.low_light_threshold: int = max(MIN_LIGHT_AMT, LOW_LIGHT_AMT - light_absorbtion)
        self.high_light_threshold: int = min(MAX_LIGHT_AMT, HIGH_LIGHT_AMT - light_absorbtion)

    def alive(self) -> bool:
        """
        Return whether the plant is alive.
        """
        return self.health > 0

    def take_damage(self, dmg: int = 1):
        """
        Apply damage to the component.
        """
        self.health -= dmg

    def sun_damage(self) -> bool:
        """
        Return whether the component should take damage due to over or under exposure to sun.
        Apply the damage as well.
        """
        light_level = self.env.light_level()

        if self.low_light_threshold > light_level or self.high_light_threshold < light_level:
            self.take_damage(1)
            return True
        return False

    def water_damage(self):
        """
        Return whether the component should take damage due to over or under exposure to water.
        Apply the damage as well.
        """
        if (self.env.dry() and self.dry()) or (self.env.soaked and self.soaked()):
            self.take_damage(1)
            return True
        return False

    def stress(self):
        """
        Apply environmental stress to the plant.
        """
        self.sun_damage()
        self.water_damage()

    def sun_exposure(self) -> int:
        """
        Return the amount of sun the component is exposed to.
        """
        light_level = self.env.light_level()
        exposure = min(self.light_absorbtion, light_level)

        return exposure

    def get_water(self):
        """
        Extract water from the environment. Take damage if too dry or too hydrated.
        """
        water = self.env.get_water(self.water_absorbtion)
        self.water += water

        return self.water

    def heal(self):
        """
        Consume sugar to heal.
        """
        while self.health < self.MAX_HEALTH and self.sugar > 0:
            self.sugar -= 1
            self.health += 1

    def grow(self):
        """
        Consume sugar to grow.
        """
        if self.size < self.MAX_SIZE:
            self.size += self.sugar * self.growth_factor
            self.sugar -= 1

    def feed(self):
        """
        Consume sugar to heal and grow.
        """
        self.heal()
        self.grow()

    def dry(self) -> bool:
        """
        Return True if the component is considered dry, generally low on water.
        """
        raise NotImplementedError()

    def soaked(self) -> bool:
        """
        Return True if the component is considered soaked, generally too much water.
        """
        raise NotImplementedError()

    def photosynthesize(self):
        """
        Produces sugar in the component by converting water and light.
        """
        if self.water > 0 and self.sun_exposure():
            self.water -= 1
            self.sugar += 1

class Seed(PlantComponent):
    """
    It's a sneed.
    """
    def __init__(self, environment):
        seed_growth_factor = 5
        water_absorbtion = 5
        light_absorbtion = 5
        super().__init__(environment, seed_growth_factor, water_absorbtion, light_absorbtion)

    def dry(self) -> bool:
        return self.water < 1

    def soaked(self) -> bool:
        return self.water > 100

class PlantModel(ABC):
    """
    An abstract base class that represents the interface for a plant.
    """
    age: int
    components: list[PlantComponent]

    def __init__(self):
        self.age = 0
        self.components = []

    def get_water(self) -> int:
        """
        Return the total amount of water stored in the plant.
        """
        water = 0
        for component in self.components:
            water += component.get_water()
        return water

    def sun_exposure(self) -> int:
        """
        Return the total amount of sun exposure.
        """
        exposure = 0
        for component in self.components:
            exposure += component.sun_exposure()
        return exposure

    def grow(self):
        sugar_per_component = self.sugar / len(self.components)
        for component in self.components:
            component.grow(sugar_per_component)

