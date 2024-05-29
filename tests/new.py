from fastapi.testclient import TestClient

from trust_vote_api.app import app

client = TestClient(app)

endpoint = '/users'

response = client.get(endpoint)
print('Response', response)
