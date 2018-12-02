import websocket
import json
import pyttsx3 as pyttsx
import time
from markov import MarkovGenerator
from ESIConnection import ESI
from tts import engine
from DebugMessages import debugMessages
import sys


MGenerator = MarkovGenerator()
esi = ESI()

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
	if victimNumber is None:
		victimName = "Unknown Victim"
	else:
		victimName = esi.get_name(victimNumber)
	victimAlliance = victimOBJ.get("alliance_id") 							# TODO: Victim Alliance name
	if victimAlliance is None:
		victimAllianceName = "Unknown Alliance"
	else:
		victimAllianceName = esi.get_name(victimAlliance)
	enemyAlliance = messageJSON.get("attackers")[0].get("alliance_id")		# TODO: Enemy Alliance name
	if enemyAlliance is None:
		enemyAllianceName = "Unknown Alliance"
	else:
		enemyAllianceName = esi.get_name(enemyAlliance)
	victimCorporation = victimOBJ.get("corporation_id")
	enemyCorporation = messageJSON.get("attackers")[0].get("corporation_id")
	if victimCorporation is None:
		victimCorporationName = "Unknown Corporation"
	else:
		victimCorporationName = esi.get_name(victimCorporation)
	enemyCorporation = messageJSON.get("attackers")[0].get("corporation_id")		# TODO: Enemy Alliance name
	if enemyCorporation is None:
		enemyCorporationName = "Unknown Corporation"
	else:
		enemyCorporationName = esi.get_name(enemyCorporation)
	solarSystem = messageJSON.get("solar_system_id")
	solarSystemName = esi.get_name(solarSystem)

	# Generate message
	generated_message = MGenerator.generate_death()
	generated_message = generated_message.replace("{Victim}", str(victimName))
	generated_message = generated_message.replace("{Alliance}", str(victimAllianceName))
	generated_message = generated_message.replace("{System}", str(solarSystemName))
	if numberOfAttackers > 1:
		generated_message = generated_message.replace("{N_Enemies}", str(numberOfAttackers))
	else:
		generated_message = generated_message.replace("{N_Enemies} enemies", f"{str(numberOfAttackers)} enemy")
	generated_message = generated_message.replace("{Enemy_Alliance}", str(enemyAllianceName))
	generated_message = generated_message.replace("{Damage}", str(totalDamage))
	generated_message = generated_message.replace("{Victim_Alliance}", str(victimAllianceName))
	generated_message = generated_message.replace("{Enemy_Corporation}", str(enemyCorporationName))
	generated_message = generated_message.replace("{Victim_Corporation}", str(victimCorporationName))

	# Say message
	engine.say(generated_message)


def on_error(ws, error):
	print("Error: " + str(error))


def on_close(ws):
	print("Connection closed.")


def on_open(ws):
	def run(*args):
		ws.send('{"action": "sub", "channel": "killstream"}')
		print(debugMessages["websocket_sending_request"])
		print(debugMessages["done"])
		print(debugMessages["websocket_start_listening"])


	thread.start_new_thread(run, ())


if __name__ == "__main__":
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://zkillboard.com:2096",
								on_message=on_message,
								on_error=on_error,
								on_close=on_close)
	ws.on_open = on_open
	ws.run_forever()
