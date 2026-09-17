from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, Item, Estoque
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from schemas import ItemSchema, CorredorSchema, ResponseCorredor
from dependencies import get_db, verify_token
storage_router = APIRouter(prefix="/storage",tags=["storage"],dependencies=[Depends(verify_token)])

@storage_router.get("/")
async def storage():
    return{
        "mensagem": "bem vindo a rota de armazenamento"
    }
#criar corredor
@storage_router.post("/corridor/create")
async def criar_corredor(corredor_schema: CorredorSchema,session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="Não autorizado")
    corredor = session.query(Estoque).filter(or_(and_(Estoque.coluna==corredor_schema.coluna,Estoque.linha==corredor_schema.linha),Estoque.nome==corredor_schema.nome)).first()
    if corredor:
        raise HTTPException(status_code=400,detail=f"um corredor de id {corredor.id} já existe nessa posição ")
    novo_corredor = Estoque(corredor_schema.nome,corredor_schema.categoria,corredor_schema.coluna,corredor_schema.linha)
    session.add(novo_corredor)
    session.commit()
    return {
        "mensagem":f"corredor {novo_corredor.nome} criado com sucesso",
        "corredor_id": novo_corredor.id
    }
#editar corredor
@storage_router.post("/corridor/{id_corredor}/edit")
async def editar_corredor(id_corredor: int, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="não autorizado")
    corredor = session.query(Estoque).filter(Estoque.id==id_corredor).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor inexistente")
    
#apagar corredor
@storage_router.post("/corridor/{id_corredor}/delete")
async def deletar_corredor(id_corredor: int, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="Não Autorizado")
    corredor = session.query(Estoque).filter(id_corredor==Estoque.id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não existe")
    session.delete(corredor)
    session.commit()
#visualizar corredor
@storage_router.get("/corridor/{id_corredor}/view",response_model=ResponseCorredor)
async def visualizar_corredor(id_corredor: int, session: Session = Depends(get_db)):
    corredor = session.query(Estoque).filter(id_corredor==Estoque.id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não encontrado")
    return corredor
"""
Endpoints de item
"""