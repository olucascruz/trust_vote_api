import json
import uuid
from datetime import datetime
from http import HTTPStatus

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from trust_vote_api.schemas import (
    BlockSchema,
    CandidateSchema,
    ElectionSchema,
    UserSchema,
    VoteSchema,
)

app = FastAPI()
url_base = 'http://localhost:8080/api'

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

blockchains = {
    'users': 1,
    'elections': 2,
    'candidates': 3,
    'users_elections': 4,
    'votes': 5,
}


@app.post('/blockchain/', status_code=HTTPStatus.CREATED)
async def create_blockchains():
    blockchains = []
    async with httpx.AsyncClient() as client:
        try:
            for _ in range(4):
                response = await client.post(
                    f'{url_base}/blockchain/init?difficulty=2'
                )
                blockchains.append({
                    'status_code': response.status_code,
                    'response_body': response.json(),
                })
            response = await client.post(
                f'{url_base}/blockchain/init?difficulty=3'
            )
            blockchains.append({
                'status_code': response.status_code,
                'response_body': response.json(),
            })
            return blockchains
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f'Erro ao criar blockchains: {e}'
            )


async def add_block_content(id_blockchain, new_data, error_message='Erro'):
    data = {'blockchainID': id_blockchain, 'blockData': new_data}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f'{url_base}/blockchain/block', json=data
            )
            return {
                'status_code': response.status_code,
                'response_body': response.json(),
            }
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f'{error_message}: {e}'
            )


async def get_block_content(Schema, response_body_blocks) -> list:
    blocks = []
    for block in response_body_blocks:
        print(type(block))
        block_schema = BlockSchema(**block)

        blocks.append(block_schema)

    block_content = []
    for block_data in blocks:
        try:
            # Verifica se a string não está vazia
            if block_data.data.strip():
                # *
                dict_data = json.loads(block_data.data)
                dict_data = json.loads(dict_data)

                schema = Schema(**dict_data)
                block_content.append(schema)
            else:
                print('A string de dados está vazia.')
        except Exception as ex:
            print(ex)
            continue

        return block_content


async def get_blocks_by_blockchain_id(blockchain_id, error_message='Erro'):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f'{url_base}/blockchain/blocks?blockchainId={blockchain_id}'
            )
            print(response)
            return {
                'status_code': response.status_code,
                'response_body': response.json(),
            }
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f'{error_message}: {e}'
            )


# About users
@app.post('/user', status_code=HTTPStatus.CREATED)
async def create_user(user: UserSchema):
    user.id = uuid.uuid4()
    user.create_at = datetime.now()
    user.modificated_at = None
    user.deleted = False

    new_user = user.model_dump_json()
    return await add_block_content(
        blockchains.get('users'),
        new_user,
        error_message='Erro ao criar usuário',
    )


@app.put('/user/', status_code=HTTPStatus.CREATED)
def update_user(user: UserSchema):
    pass


@app.delete('/user/', status_code=HTTPStatus.CREATED)
def delete_user():
    pass


@app.get('/users/', status_code=HTTPStatus.OK)
async def get_users():
    response = await get_blocks_by_blockchain_id(
        blockchains.get('users'), 'Error ao buscar usuários'
    )
    return response


@app.get('/user', status_code=HTTPStatus.OK)
async def get_user(id: int):
    response = await get_users()
    blocks_users = response['response_body']

    users = await get_block_content(UserSchema, blocks_users)

    for user in users:
        if id == user.id:
            return {
                'status_code': response['status_code'],
                'response_body': user,
            }

    return HTTPException(status_code=404, detail='Usuário não encontrado')


# About votes
@app.post('/vote/', status_code=HTTPStatus.CREATED)
async def create_vote(vote: VoteSchema):
    new_vote = vote.model_dump_json()
    return await add_block_content(
        blockchains.get('votes'), new_vote, error_message='Erro ao criar voto'
    )


@app.get('/vote/', status_code=HTTPStatus.OK)
async def get_vote():
    response = await get_blocks_by_blockchain_id(
        blockchains.get('votes'), 'Erro ao buscar votes'
    )

    return response


# About elections


@app.get('/election/', status_code=HTTPStatus.OK)
async def get_elections():
    response = await get_blocks_by_blockchain_id(
        blockchains.get('elections'), 'Erro ao buscar eleições'
    )
    return response


@app.post('/election/', status_code=HTTPStatus.CREATED)
async def create_election(election: ElectionSchema):
    new_election = election.model_dump_json()
    return await add_block_content(
        blockchains.get('votes'),
        new_election,
        error_message='Erro ao criar eleição',
    )


@app.put('/election/', status_code=HTTPStatus.CREATED)
def update_election():
    pass


# About candidates
@app.get('/candidates/', status_code=HTTPStatus.OK)
async def get_canditates():
    response = await get_blocks_by_blockchain_id(
        blockchains.get('candidates'), 'Erro ao buscar eleições'
    )

    return response


@app.get('/candidate/', status_code=HTTPStatus.OK)
async def get_canditate():
    response = await get_blocks_by_blockchain_id(
        blockchains.get('candidates'), 'Erro ao buscar eleições'
    )
    blocks_candidates = response['response_body']

    candidates = await get_block_content(CandidateSchema, blocks_candidates)

    for candidate in candidates:
        if id == candidate.id:
            return {
                'status_code': response['status_code'],
                'response_body': candidate,
            }

    return HTTPException(status_code=404, detail='Usuário não encontrado')

    return response


@app.post('/candidate/', status_code=HTTPStatus.CREATED)
async def create_candidate(candidate: CandidateSchema):
    new_candidate = candidate.model_dump_json()
    return await add_block_content(
        blockchains.get('votes'),
        new_candidate,
        error_message='Erro ao criar voto',
    )
