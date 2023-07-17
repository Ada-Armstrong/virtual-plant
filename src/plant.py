from abc import ABC
import math
from utils import ValueRange

# light level is in the range 0 - 255
MIN_LIGHT_AMT = 0
LOW_LIGHT_AMT = 50
HIGH_LIGHT_AMT = 200
MAX_LIGHT_AMT = 255

class PlantComponent(ABC):
    """
    Represents a part of the plant, for example a stem or leaf.
    """
    MAX_HEALTH: float = 1000.0
    MAX_SIZE: float = 100.0

    def __init__(self,
                 name,
                 parent,
                 environment,
                 growth_factor,
                 water_absorbtion,
                 light_range,
                 synthesis_rate):
        self.name: str = name
        self.parent = parent
        self.sugar: float = 5.0
        self.water: float = 10.0
        self.age: int = 0
        self.size: float = 1.0
        self.env = environment
        self.health: float = self.MAX_HEALTH
        self.growth_factor: float = growth_factor

        self.water_absorbtion: float = water_absorbtion
        self.light_range = light_range
        self.synthesis_rate = synthesis_rate

        self.can_add_component = True
        self.stats = {"sugar": [], "water": [], "health": [], "size": []}

    def __str__(self):
        return f"{self.name}(sugar: {self.sugar}, water: {self.water}, age: {self.age}, size: {self.size}, health: {self.health})"

    def store_stats(self):
        self.stats["sugar"].append(self.sugar)
        self.stats["water"].append(self.water)
        self.stats["health"].append(self.health)
        self.stats["size"].append(self.size)

    def alive(self) -> bool:
        """
        Return whether the plant is alive.
        """
        return self.health > 0

    def take_damage(self, dmg: float = 0.1):
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

        if light_level not in self.light_range:
            self.take_damage(0.2)
            return True
        return False

    def water_damage(self):
        """
        Return whether the component should take damage due to over or under exposure to water.
        Apply the damage as well.
        """
        if (self.env.dry() and self.dry()) or (self.env.soaked() and self.soaked()):
            self.take_damage(0.1)
            return True
        return False

    def stress(self):
        """
        Apply environmental stress to the plant.
        """
        self.sun_damage()
        self.water_damage()

    def sun_exposure(self) -> bool:
        """
        Return True if the component is exposed to enough sun for photosynthesis.
        """
        light_level = self.env.light_level()

        return light_level > 100

    def water_capacity(self) -> float:
        return 2.0 * self.size

    def get_water(self) -> int:
        """
        Extract water from the environment.
        """
        extract = min(self.water_absorbtion, self.water_capacity() - self.water)
        water = self.env.get_water(extract)
        self.water += water

        return self.water

    def heal(self):
        """
        Consume sugar to heal.
        """
        heal_amt = 1.0
        sugar_amt = 1.0

        while self.health < self.MAX_HEALTH - heal_amt and self.sugar > sugar_amt:
            self.sugar -= sugar_amt
            self.health = min(self.MAX_HEALTH, self.health + heal_amt)

    def grow(self):
        """
        Consume sugar to grow.
        """
        required_sugar = 0.5 * self.size**1.1
        build_component_sugar = 3.0 * self.MAX_SIZE

        if self.size < self.MAX_SIZE and self.sugar > required_sugar:
            self.sugar -= required_sugar
            self.size = min(self.MAX_SIZE, self.size + self.growth_factor)
        elif (self.can_add_component
              and self.size >= 0.75 * self.MAX_SIZE
              and self.sugar > build_component_sugar):
            self.can_add_component = False
            self.sugar -= build_component_sugar
            self.grow_component()

    def grow_component(self):
        """
        Add a new component.
        """
        raise NotImplementedError()

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

    def damp(self) -> bool:
        """
        Return True if the component is considered damp, generally medium on water.
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
        maximum_sugar = self.size * 10

        if self.damp() and self.sun_exposure() and self.sugar < maximum_sugar:
            self.water -= self.synthesis_rate * 1.0
            self.sugar += self.synthesis_rate * 1.0

class Seed(PlantComponent):
    """
    It's a sneed.
    """
    def __init__(self, parent, environment):
        growth_factor = 1.5
        water_absorbtion = 0.6
        super().__init__(name="Seed",
                         parent=parent,
                         environment=environment,
                         growth_factor=growth_factor,
                         water_absorbtion=water_absorbtion,
                         light_range=ValueRange(30, 205),
                         synthesis_rate=1.1)

    def grow_component(self):
        self.parent.components.append(Root(self.parent, self.env))

    def dry(self) -> bool:
        return self.water < 0.05 * self.water_capacity()

    def damp(self) -> bool:
        return self.water > 0.45 * self.water_capacity()

    def soaked(self) -> bool:
        return self.water > 0.9 * self.water_capacity()

class Root(PlantComponent):
    """
    It's a root.
    """
    def __init__(self, parent, environment):
        growth_factor = 0.5
        water_absorbtion = 1.5
        super().__init__(name="Root",
                         parent=parent,
                         environment=environment,
                         growth_factor=growth_factor,
                         water_absorbtion=water_absorbtion,
                         light_range=ValueRange(30, 220),
                         synthesis_rate=0.1)

    def grow_component(self):
        pass

    def dry(self) -> bool:
        return self.water < 0.1 * self.water_capacity()

    def damp(self) -> bool:
        return self.water > 0.5 * self.water_capacity()

    def soaked(self) -> bool:
        return self.water > 0.9 * self.water_capacity()

class PlantModel(ABC):
    """
    An abstract base class that represents the interface for a plant.
    """
    age: int
    components: list[PlantComponent]

    def __init__(self, name, env):
        self.name = name
        self.env = env
        self.age = 0
        self.components = []

    def __str__(self):
        indent = "    "
        return f"{self.name}(age: {self.age})\n" + "\n".join([indent + str(comp) for comp in self.components])

    def alive(self) -> bool:
        """
        Returns True if the plant is alive.
        """
        return any(comp.alive() for comp in self.components)

    def get_water(self) -> float:
        """
        Extract water from the environment.
        Return the total amount of water stored in the plant.
        """
        water = 0.0
        for component in self.components:
            water += component.get_water()
        return water

    def total_sugar(self) -> float:
        """
        Return the total amount of sugar stored in the plant.
        """
        sugar = 0.0
        for component in self.components:
            sugar += component.sugar
        return sugar

    def feed(self):
        for component in self.components:
            component.feed()

    def stress(self):
        for component in self.components:
            component.stress()

    def photosynthesize(self):
        for component in self.components:
            component.photosynthesize()

    def update(self):
        self.get_water()
        self.photosynthesize()
        self.feed()
        self.stress()

    def pass_time(self, duration=1):
        self.age += duration
        for component in self.components:
            component.age += duration
        self.update()

    def store_stats(self):
        for component in self.components:
            component.store_stats()

class SimplePlant(PlantModel):
    def __init__(self, env):
        super().__init__("Simple Plant", env)
        self.components.append(Seed(self, env))

