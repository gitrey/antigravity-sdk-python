from utils import get_client

client = get_client()

interaction_id = "ChBkYzFmZjdhMWE2MDY0ZWY1EAgaAzM3NioEbWFpbg"
res = client.interactions.get(id=interaction_id)

print("--- MODEL DUMP ---")
import pprint
pprint.pprint(res.model_dump())


