
from fastapi import APIRouter, Depends, HTTPException
from app.models import Usuario, Item, Corredor, ItemCorredor
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.schemas.entry import ItemSchema, CorredorSchema, ItemCorredorSchema
from app.schemas.update import ItemUpdateSchema, CorredorUpdateSchema
from app.schemas.response import (
    ResponseCorredorSchema, 
    ResponseItemSchema, 
    ResponseCorredorUpdateSchema, 
    ResponseItemUpdateSchema
    )
from app.api.dependencies import get_db, verify_token
storage_router = APIRouter(prefix="/storage",tags=["storage"],dependencies=[Depends(verify_token())])

@storage_router.get("/")
async def storage():
    return{
        "mensagem": "bem vindo a rota de armazenamento"
    }
#visualizar corredor
@storage_router.get("/corridor/{id_corredor}",response_model=ResponseCorredorSchema)
async def visualizar_corredor(id_corredor: int, session: Session = Depends(get_db)):
    corredor = session.query(Corredor).filter(id_corredor==Corredor.id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não encontrado")
    return corredor
#criar corredor
@storage_router.post("/corridor")
async def criar_corredor(corredor_schema: CorredorSchema,session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="Não autorizado")
    corredor = session.query(Corredor).filter(or_(and_(Corredor.coluna==corredor_schema.coluna,Corredor.linha==corredor_schema.linha),Corredor.nome==corredor_schema.nome)).first()
    if corredor:
        raise HTTPException(status_code=400,detail=f"um corredor de id {corredor.id} já existe nessa posição ")
    novo_corredor = Corredor(corredor_schema.nome,corredor_schema.categoria,corredor_schema.coluna,corredor_schema.linha)
    session.add(novo_corredor)
    session.commit()
    return {
        "mensagem":f"corredor {novo_corredor.nome} criado com sucesso",
        "corredor_id": novo_corredor.id
    }
#editar corredor
@storage_router.patch("/corridor/{id_corredor}",response_model=ResponseCorredorUpdateSchema)
async def editar_corredor(id_corredor: int,corredor_update_schema: CorredorUpdateSchema, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="não autorizado")
    corredor = session.query(Corredor).filter(Corredor.id==id_corredor).first()
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
#adcionar item ao corredor
@storage_router.post("/corridor/{id_corridor}")
async def adcionar_ao_corredor(id_corridor: int,item_corredor_schema: ItemCorredorSchema,session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    corredor = session.query(Corredor).filter(Corredor.id == id_corridor).first()
    item = session.query(Item).filter(Item.id==item_corredor_schema.item_id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não existe")
    if not item:
        raise HTTPException(status_code=400,detail="item não cadastrado")
    item_corredor = session.query(ItemCorredor).filter(and_(item_corredor_schema.item_id==ItemCorredor.item_id,id_corridor==ItemCorredor.corredor_id)).first()
    if item_corredor:
        raise HTTPException(status_code=400,detail="ja existe esse item nesse corredor")
    novo_item_corredor = ItemCorredor(item_id=item_corredor_schema.item_id,corredor_id=id_corridor,quantidade=item_corredor_schema.quantidade)
    session.add(novo_item_corredor)
    session.commit()
#apagar corredor
@storage_router.delete("/corridor/{id_corredor}")
async def deletar_corredor(id_corredor: int, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="Não Autorizado")
    corredor = session.query(Corredor).filter(id_corredor==Corredor.id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não existe")
    session.delete(corredor)
    session.commit()
"""
Endpoints de item
"""
#cadastrar item manualmente
@storage_router.post("/item/",response_model=ResponseItemSchema)
async def cadastrar_item(item_schema: ItemSchema, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    if not usuario.admin:
        raise  HTTPException(status_code=401,detail="Não autorizado")
    item = session.query(Item).filter(item_schema.bar_code==Item.bar_code).first()
    if item:
        raise HTTPException(status_code=400,detail="o Item ja esta cadastrado")
    novo_item = Item(nome=item_schema.nome,barcode=item_schema.bar_code,quantidade=item_schema.quantidade,preco=item_schema.preco)
    session.add(novo_item)
    session.commit()
    return novo_item
#cadastrar item via barcode
@storage_router.post("/item/barcode/{codigo_de_barras}")
async def cadastrar_via_barcode(codigo_de_barras: int, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    pass
#editar informações de item
@storage_router.patch("/item/{item_id}",response_model=ResponseItemUpdateSchema)
async def editar_item(item_id: int,item_update_schema: ItemUpdateSchema,session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="não autorizado")
    item = session.query(Item).filter(Item.id==item_id).first()
    if not item:
        raise HTTPException(status_code=400,detail="item não cadastrado")
    atualizacao_item = item_update_schema.model_dump(exclude_unset=True)
    campos_alterados = []
    for campo, valor in atualizacao_item.items():
        setattr(item, campo, valor)
        campos_alterados.append(campo)
    session.commit()
    session.refresh(item)
    return{
        "mensagem": f"informações do item {item.id} alterado com sucesso",
        "campos_alterados": campos_alterados,
        "corredor": item
    }
#deletar cadastro de item
@storage_router.delete("/item/{item_id}",response_model=ItemSchema)
async def deletar_item(item_id: int,session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="Não Autorizado")
    item = session.query(Item).filter(item_id==Item.id).first()
    if not item:
        raise HTTPException(status_code=400,detail="item_não_cadastrado")
    session.delete(item)
    session.commit()
    return {
        "item removido": item
    }
#visualizar item
@storage_router.get("/item/{item_id}",response_model=ResponseItemSchema)
async def visualizar_item(item_id: int, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token())):
    item = session.query(Item).filter(item_id==Item.id).first()
    if not item:
        raise HTTPException(status_code=400,detail="item não cadastrado")
    return item
#visualizar itens de um corredor

