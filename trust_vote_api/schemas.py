import uuid
from typing import Optional

from pydantic import BaseModel


class ElectionSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    type: str
    start_at: Optional[str] = None
    end_at: Optional[str] = None


class UserElectionSchema(BaseModel):
    user: int
    election: int


class UserSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    email: str
    password: str
    phone: str
    create_at: Optional[str] = None
    modified_at: Optional[str] = None
    deleted: Optional[bool] = None


class CandidateSchema(BaseModel):
    id: Optional[int]
    election: int
    name: str


class VoteSchema(BaseModel):
    candidate: int
    voter: int
    location: str
    at: str


class BlockSchema(BaseModel):
    index: int
    timestamp: int
    hash: str
    previousHash: Optional[str]
    data: str
