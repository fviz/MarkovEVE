import pyttsx3 as pyttsx


class VoiceEngine:

	def __init__(self):
		self.engine = pyttsx.init()


	def say(self, content):
		print(content)
		self.engine.say(content)
		if self.engine.isBusy() is True:
			self.engine.runAndWait()


engine = VoiceEngine()
