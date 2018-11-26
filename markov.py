import markovify


class MarkovGenerator:

	def __init__(self):
		with open("deaths.txt") as deathFile:
			self.deathsSource = deathFile.read()
			# TODO: Try state_size = 2
			self.deathsModel = markovify.Text(self.deathsSource)

	def generate_death(self):
		generatedDeath = self.deathsModel.make_short_sentence(120)
