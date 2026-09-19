from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, Item, Estoque
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from schemas import ItemSchema, CorredorSchema, ResponseCorredorSchema, CorredorUpdateSchema, ResponseCorredorUpdateSchema
from dependencies import get_db, verify_token
storage_router = APIRouter(prefix="/storage",tags=["storage"],dependencies=[Depends(verify_token)])

@storage_router.get("/")
async def storage():
    return{
        "mensagem": "bem vindo a rota de armazenamento"
    }
#visualizar corredor
@storage_router.get("/corridor/{id_corredor}",response_model=ResponseCorredorSchema)
async def visualizar_corredor(id_corredor: int, session: Session = Depends(get_db)):
    corredor = session.query(Estoque).filter(id_corredor==Estoque.id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não encontrado")
    return corredor
#criar corredor
@storage_router.post("/corridor")
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
@storage_router.patch("/corridor/{id_corredor}",response_model=ResponseCorredorUpdateSchema)
async def editar_corredor(id_corredor: int,corredor_update_schema: CorredorUpdateSchema, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token)):
    """
    edita informações de um corredor especifico com base no id do mesmo
    """
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="não autorizado")
    corredor = session.query(Estoque).filter(Estoque.id==id_corredor).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor inexistente")
    atualizacao_corredor = corredor_update_schema.model_dump(exclude_unset=True)
    campos_alterados = []
    for campo, valor in atualizacao_corredor.items():
        setattr(corredor, campo, valor)
        campos_alterados.append(campo)
    session.commit()
    session.refresh(corredor)
    return{
        "mensagem": f"Corredor {corredor.id} alterado com sucesso",
        "campos_alterados": campos_alterados,
        "corredor": corredor
    }
#apagar corredor
@storage_router.delete("/corridor/{id_corredor}")
async def deletar_corredor(id_corredor: int, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="Não Autorizado")
    corredor = session.query(Estoque).filter(id_corredor==Estoque.id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não existe")
    session.delete(corredor)
    session.commit()
"""
Endpoints de item
"""