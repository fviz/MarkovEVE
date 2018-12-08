from pythonosc import  osc_message_builder
from pythonosc import udp_client
import argparse
import time
import random


class SoundPlayer:

	def __init__(self):
		parser = argparse.ArgumentParser()
		parser.add_argument("--ip",
							default="127.0.0.1",
							help="The IP of the OSC server.")
		parser.add_argument("--port",
							default=8000,
							help="The port of the OSC server.")
		args = parser.parse_args()

		self.client = udp_client.SimpleUDPClient(args.ip, args.port)


	def send_message(self, destination, n_attackers):

		amount = n_attackers + random.randrange(1, 4)
		print(f"Attackers: {n_attackers}. Amount: {amount}.")
		for x in range(amount):
			self.client.send_message(f"/{destination}", "1")
			r_wait = random.randrange(200, 2000)
			time.sleep(r_wait / 1000)
			print(r_wait / 1000)
