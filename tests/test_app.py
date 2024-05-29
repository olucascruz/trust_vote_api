from http import HTTPStatus

from fastapi.testclient import TestClient

from trust_vote_api.app import app

client = TestClient(app)


# def test_create_blockchains():
#     endpoint = '/blockchain'
#     # Fazer a chamada para criar o blockchain
#     response = client.post(endpoint)

#     # Verificar se o blockchain foi criado com sucesso
#     assert response.status_code == HTTPStatus.CREATED

#     # Extrair os dados da resposta JSON
#     data = response.json()

#     # Verificar se a criação dos blockchains foi bem-sucedida
#     blockchains = data
#     number_blockchains = 5
#     # Verificar se foram criados 5 blockchains
#     assert len(blockchains) == number_blockchains
#     for blockchain in blockchains:
#         assert 'status_code' in blockchain
#         assert 'response_body' in blockchain


# def test_create_user():
#     endpoint = '/user'
#     user_data = {
#         'name': 'John Doe',
#         'email': 'john@example.com',
#         'password': 'secretpassword',
#         'phone': '95846512',
#     }

#     response = client.post(endpoint, json=user_data)
#     # Assert
#     assert response.status_code == HTTPStatus.CREATED
#     assert 'status_code' in response.json()
#     assert 'response_body' in response.json()


# def test_load_blockchains():
#     endpoint = '/blockchain'

#     response = client.get(endpoint).json()

#     print(response)
#     # Assert
#     number_expect_blockchains = 5
#     assert len(response['response_body']) == number_expect_blockchains
#     assert 'status_code' in response
#     assert 'response_body' in response
#     assert response['status_code'] == HTTPStatus.OK


# def test_create_election():
#     endpoint = '/election'

#     election_data = {
#         'name': 'bolos',
#         'type': 'Público',
#     }
#     response = client.post(endpoint, json=election_data)
#     # Assert
#     assert response.status_code == HTTPStatus.CREATED


# def test_create_candidate():
#     endpoint = '/candidate'
#     candidate_data = {
#         'id': 1,
#         'election': 45,
#         'name': 'John Doe',
#     }

#     response = client.post(endpoint, json=candidate_data)
#     # Assert
#     assert response.status_code == HTTPStatus.CREATED
#     assert 'status_code' in response.json()
#     assert 'response_body' in response.json()


# def test_create_vote():
#     endpoint = '/vote'
#     vote_date = {
#         'candidate': 1,
#         'voter': 1,
#         'location': 'Lirio do vale',
#         'at': str(datetime.now()),
#     }

#     response = client.post(endpoint, json=vote_date)
#     # Assert
#     assert response.status_code == HTTPStatus.CREATED
#     assert 'status_code' in response.json()
#     assert 'response_body' in response.json()


def test_get_users():
    endpoint = '/users'

    response = client.get(endpoint)
    print('Response', response)

    # Assert
    assert response.status_code == HTTPStatus.OK


def test_get_user():
    endpoint = '/user?id=dfe7fcc2-a285-41d7-936b-52f025c26a41'

    response = client.get(endpoint)

    print(response.content)
    # Assert
    assert response.status_code == HTTPStatus.OK


# def test_get_election_with_id():
#     endpoint = '/election?id=45'

#     response = client.get(endpoint)
#     # Assert
#     assert response.status_code == HTTPStatus.OK


# def test_get_election():
#     endpoint = '/election'

#     response = client.get(endpoint)
#     # Assert
#     assert response.status_code == HTTPStatus.OK


# def test_login():
#     endpoint = '/log'

#     user = {
#         'email': 'email',
#         'password': 'senha',
#     }
#     response = client.post(endpoint, json=user)
#     # Assert
#     assert response.status_code == HTTPStatus.OK
