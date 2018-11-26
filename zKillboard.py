import websocket
import json

try:
	import thread
except ImportError:
	import _thread as thread
import time


def on_message(ws, message):
	print(message)
	messageJSON = json.loads(message)
	damageSum  = 0
	numberOfAttackers = 0
	for attacker in messageJSON.get("attackers"):
		numberOfAttackers += 1
		damageSum += attacker.get("damage_done")

	victim = messageJSON.get("victim").get("character_id")
	print(f"Attackers: {numberOfAttackers} – Total damage: {damageSum} – Victim: {victim}")


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
