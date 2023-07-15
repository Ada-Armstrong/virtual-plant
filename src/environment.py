from abc import ABC

class Environment(ABC):
	time: int
	temperature: int
	moisture: int
	soil_quality: int
	light: int

	def __init__(self, temperature, moisture, soil_quality, light):
		self.time = 0
		self.temperature = temperature
		self.moisture = moisture
		self.soil_quality = soil_quality
		self.light = light

	def pass_time(self, duration):
		self.time += duration

	def get_water(self, amount):
		if self.moisture >= amount:
			self.moisture -= amount
		else:
			amount = self.moisture
			self.moisture = 0
		return amount

	def dry(self):
		return self.moisture < 10

	def soaked(self):
		return self.moisture > 100

	def light_level(self):
		return self.light