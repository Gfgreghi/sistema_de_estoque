from fastapi import APIRouter, HTTPException
import app.crud.itens as itens
from app.api.dependencies import UsuarioDep, SessionDep
from app.schemas.entry import ItemSchema
from app.schemas.update import ItemUpdateSchema
from app.schemas.response import ResponseItemSchema, ResponseItemUpdateSchema

item_router = APIRouter(prefix="/item",tags=["item"])
#cadastrar item manualmente
@item_router.post("/item/",response_model=ResponseItemSchema)
async def cadastrar_item(item_schema: ItemSchema, session: SessionDep,usuario: UsuarioDep):
    item = itens.create(item_schema,session)
    return item
#editar informações de item
@item_router.patch("/item/{item_id}",response_model=ResponseItemUpdateSchema)
async def editar_item(item_id: int,item_update_schema: ItemUpdateSchema,session: SessionDep,usuario: UsuarioDep):
    item_update = itens.update(item_id,item_update_schema,session)
    item = item_update["item"]
    return{
        "mensagem": f"informações do item {item.id} alterado com sucesso",
        "campos_alterados": item_update["campos_alterados"],
        "corredor": item
    }
#deletar cadastro de item
@item_router.delete("/item/{item_id}",response_model=ItemSchema)
async def deletar_item(item_id: int,session: SessionDep,usuario: UsuarioDep):
    item = itens.delete(item_id,session)
    return {
        "item removido": item
    }
#visualizar item
@item_router.get("/item/{item_id}",response_model=ResponseItemSchema)
async def visualizar_item(item_id: int, session: SessionDep,usuario: UsuarioDep):
    itens.read(item_id,session)
