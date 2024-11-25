from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(20), nullable=False)
    tipo_atendimento = Column(String(1), nullable=False)  # 'N' ou 'P'
    posicao = Column(Integer, nullable=False)
    atendido = Column(Boolean, default=False)
    data_chegada = Column(DateTime(timezone=True), server_default=func.now())
