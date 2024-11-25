from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/fila", response_model=list[schemas.ClienteResponse])
def listar_fila(db: Session = Depends(get_db)):
    fila = crud.listar_fila(db)
    return fila


@app.get("/fila/{id}", response_model=schemas.ClienteResponse)
def get_cliente(id: int, db: Session = Depends(get_db)):
    cliente = crud.buscar_por_id(db, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@app.post("/fila", response_model=schemas.ClienteResponse)
def adicionar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    if cliente.tipo_atendimento != "N" and cliente.tipo_atendimento != "P":
        raise HTTPException(status_code=400, detail="Tipo de atendimento inválido")
    if len(cliente.nome) > 20:
        raise HTTPException(
            status_code=400,
            detail="Nome muito longo, o nome deve conter no máximo 20 caracteres",
        )
    novo_cliente = crud.adicionar_cliente(db, cliente.nome, cliente.tipo_atendimento)
    return novo_cliente


@app.put("/fila")
def atualizar_fila(db: Session = Depends(get_db)):
    crud.atualizar_fila(db)
    return {"message": "Fila atualizada"}


@app.delete("/fila/{id}")
def remover_cliente(id: int, db: Session = Depends(get_db)):
    if not crud.remover_cliente(db, id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"message": "Cliente removido"}
