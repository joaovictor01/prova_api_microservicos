from sqlalchemy.orm import Session
from .models import Cliente


def listar_fila(db: Session):
    # return db.query(Cliente).filter_by(atendido=False).order_by(Cliente.posicao).all()
    return (
        db.query(Cliente)
        .filter_by(atendido=False)
        .order_by(Cliente.tipo_atendimento.desc(), Cliente.posicao)
        .all()
    )


def buscar_por_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def adicionar_cliente(db: Session, nome: str, tipo_atendimento: str):
    posicao = db.query(Cliente).filter_by(atendido=False).count() + 1
    cliente = Cliente(nome=nome, tipo_atendimento=tipo_atendimento, posicao=posicao)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def atualizar_fila(db: Session):
    fila = listar_fila(db)
    for cliente in fila:
        cliente.posicao -= 1
        if cliente.posicao == 0:
            cliente.atendido = True
    db.commit()


def remover_cliente(db: Session, cliente_id: int):
    cliente = buscar_por_id(db, cliente_id)
    if cliente:
        db.delete(cliente)
        db.commit()
        return True
    return False
