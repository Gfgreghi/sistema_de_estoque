from fastapi import HTTPException
from app.schemas.update import UsuarioUpdateSchema
from app.schemas.entry import ItemSchema
from app.api.dependencies import SessionDep
from app.models import Item, ItemCorredor
#criar item
def create(item_schema: ItemSchema,session: SessionDep) -> Item:
    item = session.query(Item).filter(item_schema.bar_code==Item.bar_code).first()
    if item:
        raise HTTPException(status_code=400,detail="o Item ja esta cadastrado")
    novo_item = Item(nome=item_schema.nome,barcode=item_schema.bar_code,quantidade=item_schema.quantidade,preco=item_schema.preco)
    session.add(novo_item)
    session.commit()
    return novo_item
#ver item
def read(item_id: int,session: SessionDep) -> Item:
    item = session.query(Item).filter(item_id==Item.id).first()
    if not item:
        raise HTTPException(status_code=400,detail="item não cadastrado")
    return item
#editar item
def update(item_id:int, item_update_schema: UsuarioUpdateSchema,session: SessionDep) -> dict:
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
    return {
        "item": item, 
        "campos_alterados": campos_alterados
            }
#apagar item
def delete(item_id: int, session: SessionDep):
    item = session.query(Item).filter(item_id==Item.id).first()
    if not item:
        raise HTTPException(status_code=400,detail="item_não_cadastrado")
    session.delete(item)
    session.commit()
    return item#visualizar itens de um corredor
