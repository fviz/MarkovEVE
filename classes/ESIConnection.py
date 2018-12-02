from esipy import EsiClient
from esipy import EsiApp
from esipy import EsiSecurity
from esipy import App
from classes.DebugMessages import debugMessages
from classes.tts import engine


class ESI:

	def __init__(self):
		engine.say(debugMessages["esi_connecting"])
		self.esi_app = EsiApp()
		self.app = self.esi_app.get_latest_swagger

		self.security = EsiSecurity(
			redirect_uri="http://localhost/callback/",
			client_id="5cc3f56b88364587b5b25aeb0299cdd1",
			secret_key="HX9ed1EYpPQj1bnCklcWFXAborUvXXEpv8BQdEcg",
			headers={'User-Agent': 'PythonProject'},
		)

		self.app = App.create(url="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")

		self.client = EsiClient(
			retry_requests=True,
			raw_body_only=False
		)
		engine.say(debugMessages["done"])

	def get_name(self, request_id):
		get_character_name_operation = self.app.op['post_universe_names'](
			ids=[str(request_id)]
		)

		response = self.client.request(get_character_name_operation)
		return response.data[0]["name"]