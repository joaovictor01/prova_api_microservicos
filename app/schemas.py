from pydantic import BaseModel, Field
from datetime import datetime


class ClienteBase(BaseModel):
    nome: str = Field(..., max_length=20)
    tipo_atendimento: str = Field(..., pattern="^[NP]$")


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(BaseModel):
    id: int
    nome: str
    tipo_atendimento: str
    posicao: int
    atendido: bool
    data_chegada: datetime

    class Config:
        orm_mode = True
