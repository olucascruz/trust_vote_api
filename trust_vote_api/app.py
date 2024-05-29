import json
import uuid
from datetime import datetime
from http import HTTPStatus

import httpx
from fastapi import FastAPI, HTTPException, Response
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


@app.get('/blockchain/', status_code=HTTPStatus.OK)
async def load_blockchains():
    endpoint = '/blockchain/block/persistence/load'

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(f'{url_base}{endpoint}')
            return response
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f'Erro ao carregar blokcchains: {e}'
            )


async def add_block_content(id_blockchain, new_data, error_message='Erro'):
    endpoint = '/blockchain/block'
    data = {'blockchainID': id_blockchain, 'blockData': new_data}
    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(
                f'{url_base}{endpoint}', json=data
            )
            return response
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


async def get_blocks_by_blockchain_id(
    blockchain_id: int, error_message: str = 'Erro'
) -> Response:
    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(
                f'{url_base}/blockchain/blocks?blockchainId={blockchain_id}'
            )

            return response

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f'{error_message}: {e}'
            )


@app.post('/login', status_code=HTTPStatus.OK)
async def login(user_credential: dict):
    print(user_credential)
    response = await get_users()
    block_users = json.loads(response.body.decode())
    users = await get_block_content(UserSchema, block_users)
    for _user in users:
        print(_user)
        if _user.email == user_credential.email:
            if _user.password == user_credential.password:
                return Response(
                    content={_user.id, _user.name},
                    status_code=response.status_code,
                    media_type='application/json',
                )
    return HTTPException(status_code=404, detail=f'{"Erro credenciais"}')


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
async def get_users() -> Response:
    response = await get_blocks_by_blockchain_id(
        blockchains.get('users'), 'Error ao buscar usuários'
    )
    return response


@app.get('/user', status_code=HTTPStatus.OK)
async def get_user(id: uuid.UUID):
    response: Response = await get_users()
    blocks_users = json.loads(response.content.decode())

    users: list[UserSchema] = await get_block_content(UserSchema, blocks_users)

    for user in users:
        if id == user.id:
            return Response(
                content=user.model_dump_json(),
                status_code=response.status_code,
                media_type='application/json',
            )

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
    response: Response = await get_blocks_by_blockchain_id(
        blockchains.get('votes'), 'Erro ao buscar votos'
    )

    return response


# About elections


@app.get('/election/', status_code=HTTPStatus.OK)
async def get_elections(id: int = None):
    response: Response = await get_blocks_by_blockchain_id(
        blockchains.get('elections'), 'Erro ao buscar eleições'
    )

    blocks_elections = json.loads(response.content.decode())
    elections: list[ElectionSchema] = await get_block_content(
        ElectionSchema, blocks_elections
    )

    if id is None:
        return Response(
            status_code=HTTPStatus.OK,
            content=str(elections),
            media_type='application/json',
        )
    for election in elections:
        if election.id == id:
            return Response(
                status_code=HTTPStatus.OK,
                content=election.model_dump_json(),
                media_type='application/json',
            )
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Eleição não encontrada'
    )


@app.get('/election/', status_code=HTTPStatus.OK)
async def get_all_elections():
    response: Response = await get_blocks_by_blockchain_id(
        blockchains.get('elections'), 'Erro ao buscar eleições'
    )

    blocks_elections = json.loads(response.content.decode())
    elections = await get_block_content(ElectionSchema, blocks_elections)

    return Response(
        status_code=HTTPStatus.OK,
        content=elections,
        media_type='application/json',
    )


@app.post('/election/', status_code=HTTPStatus.CREATED)
async def create_election(election: ElectionSchema):
    new_election = election.model_dump_json()
    return await add_block_content(
        blockchains.get('elections'),
        new_election,
        error_message='Erro ao criar eleição',
    )


@app.put('/election/', status_code=HTTPStatus.CREATED)
def update_election():
    pass


@app.post('/election/add_user')
async def add_user_to_election(election_id: int, user_id: int):
    add_block_content()


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


@app.post('/candidate/', status_code=HTTPStatus.CREATED)
async def create_candidate(candidate: CandidateSchema):
    new_candidate = candidate.model_dump_json()
    return await add_block_content(
        blockchains.get('candidates'),
        new_candidate,
        error_message='Erro ao criar voto',
    )
