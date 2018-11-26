import websocket
import json
import pyttsx3 as pyttsx
import time
from markov import MarkovGenerator
from ESIConnection import ESI

MGenerator = MarkovGenerator()
esi = ESI()

engine = pyttsx.init()

try:
	import thread
except ImportError:
	import _thread as thread


def get_attacker_info(message_json):
	n_attackers = 0
	damageSum = 0
	for attacker in message_json.get("attackers"):
		n_attackers += 1
		damageSum += attacker.get("damage_done")
	info = {
		"numberOfAttackers": n_attackers,
		"totalDamage": damageSum
	}
	return info


def on_message(ws, message):
	# Print message and parse JSON
	# print(message)
	messageJSON = json.loads(message)
	victimOBJ = messageJSON.get("victim")

	# Get attacker info
	attackerInfo = get_attacker_info(messageJSON)
	numberOfAttackers = attackerInfo["numberOfAttackers"]
	totalDamage = attackerInfo["totalDamage"]
	victimNumber = victimOBJ.get("character_id")
	victimName = esi.get_character_name(victimNumber)
	victimAlliance = victimOBJ.get("alliance_id")
	if victimAlliance == None:
		victimAlliance = "Unknown Alliance"
	enemyAlliance = messageJSON.get("attackers")[0].get("alliance_id")
	if enemyAlliance == None:
		victimAlliance = "Unknown Alliance"
	solarSystem = messageJSON.get("solar_system_id")
	print(victimNumber)

	# Generate message
	generated_message = MGenerator.generate_death()
	generated_message = generated_message.replace("{Victim}", str(victimName))
	generated_message = generated_message.replace("{Alliance}", str(victimAlliance))
	generated_message = generated_message.replace("{Region}", str(solarSystem))
	if numberOfAttackers > 1:
		generated_message = generated_message.replace("{N_Enemies}", str(numberOfAttackers))
	else:
		generated_message = generated_message.replace("{N_Enemies} enemies", f"{str(numberOfAttackers)} enemy")
	generated_message = generated_message.replace("{Enemy_Alliance}", str(enemyAlliance))
	generated_message = generated_message.replace("{Damage}", str(totalDamage))
	# generated_message = generated_message.replace("None", "Unknown Victim")
	print(generated_message)

	# Say message
	engine.say(generated_message)
	engine.runAndWait()


def on_error(ws, error):
	print(error)


def on_close(ws):
	print("Connection closed.")


def on_open(ws):
	def run(*args):
		ws.send('{"action": "sub", "channel": "killstream"}')
		print("Sending request...")
		time.sleep(1)
		print("Request sent. Start listening...\n\n>>\n")


	thread.start_new_thread(run, ())


if __name__ == "__main__":
	# websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://zkillboard.com:2096",
								on_message=on_message,
								on_error=on_error,
								on_close=on_close)
	ws.on_open = on_open
	ws.run_forever()
