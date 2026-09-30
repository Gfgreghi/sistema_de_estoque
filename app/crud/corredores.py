from fastapi import HTTPException
from sqlalchemy import and_, or_
from app.schemas.update import CorredorUpdateSchema
from app.schemas.entry import CorredorSchema, ItemCorredorSchema
from app.api.dependencies import SessionDep
from app.models import Corredor, ItemCorredor, Item
#criar corredor
def create(Corredor_scema: CorredorSchema,session: SessionDep) -> Corredor:
    corredor = session.query(Corredor).filter(and_(Corredor_scema.coluna==Corredor.coluna,Corredor_scema.linha==Corredor.linha)).first()
    if corredor:
        raise HTTPException(status_code=400,detail="corredor ja existente na posição")
    novo_corredor = Corredor(Corredor_scema.nome,Corredor_scema.categoria,Corredor_scema.coluna,Corredor_scema.linha)
    session.add(novo_corredor)
    session.commit()
    return novo_corredor
#ver corredor
def read(id_corredor: int, session: SessionDep) -> Corredor:
    corredor = session.query(Corredor).filter(id_corredor==Corredor.id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não encontrado")
    return corredor
#editar corredor
def update(corridor_id,corredor_update_schema: CorredorUpdateSchema, session: SessionDep) -> dict:
    corredor = session.query(Corredor).filter(Corredor.id==corridor_id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor inexistente")
    atualizacao_corredor = corredor_update_schema.model_dump(exclude_unset=True)
    campos_alterados = []
    for campo, valor in atualizacao_corredor.items():
        setattr(corredor, campo, valor)
        campos_alterados.append(campo)
    session.commit()
    session.refresh(corredor)
    return {
        "campos_alterados": campos_alterados,
        "id_corredor": corredor.id,
        "corredor": corredor
    }
#apagar corredor
def delete(corridor_id: int, session: SessionDep):
    corredor = session.query(Corredor).filter(corridor_id==Corredor.id).first()
    if not corredor:
        raise HTTPException(status_code=400,detail="corredor não existe")
    session.delete(corredor)
    session.commit()
    return corredor
#adcionar item ao corredor
def add_item(id_corridor: int,item_corredor_schema: ItemCorredorSchema,session: SessionDep):
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
    return novo_item_corredor