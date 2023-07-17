from abc import ABC
import math

SECONDS_IN_DAY = 60 * 60 * 24

class Environment(ABC):
    time: int
    temperature: int # in degrees celsius
    moisture: int
    soil_quality: int
    light: int

    def __init__(self, temperature, moisture, soil_quality, light):
        self.time = 0
        self.temperature = temperature
        self.moisture = moisture
        self.soil_quality = soil_quality
        self.light = light

    def __str__(self):
        return f"(Env)\ntime: {self.time}s\ntemp: {self.temperature}*C\nmoisture: {self.moisture}\nlight: {self.light}"

    def update(self):
        """
        Changes the internal values of the environment, should be based on time.
        """
        raise NotImplementedError()

    def pass_time(self, duration=1):
        self.time += duration
        self.update()

    def get_water(self, amount):
        if self.moisture >= amount:
            self.moisture -= amount
        else:
            amount = self.moisture
            self.moisture = 0
        return amount

    def dry(self):
        return self.moisture < 50

    def soaked(self):
        return self.moisture > 1500

    def light_level(self):
        return self.light

class EdenEnvironment(Environment):
    def __init__(self):
        initial_temp = self.temperature_func(0)
        super().__init__(initial_temp, self.moisture_func(0, initial_temp), None, self.light_func(0))

    def shift_time(self, time) -> float:
        """
        Map from time range to [0, 2pi)
        """
        return 2 * math.pi * (time / SECONDS_IN_DAY)

    def temperature_func(self, time: int) -> int:
        return 6 * math.sin(self.shift_time(time) - math.pi / 2) + 22

    def moisture_func(self, time: int, temperature: int) -> int:
        return int(max(0.0, 200 * math.cos(self.shift_time(time)) - temperature + 225))

    def light_func(self, time: int) -> int:
        return int(215 * math.exp(-math.sin((self.shift_time(time) + math.pi) / 2)**2))

    def update(self):
        self.temperature = self.temperature_func(self.time)
        self.moisture = self.moisture_func(self.time, self.temperature)
        self.light = self.light_func(self.time)

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    env = EdenEnvironment()
    num_days = 1
    time = list(range(60 * 60 * 24 * num_days))
    temp = list(map(env.temperature_func, time))
    moisture = list(map(env.moisture_func, time, temp))

    plt.plot(time, moisture)
    plt.show()
