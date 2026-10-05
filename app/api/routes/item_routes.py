from fastapi import APIRouter, HTTPException
import app.crud.itens as itens
from app.api.dependencies import UsuarioDep, SessionDep, require_permission
from app.schemas.entry import ItemSchema
from app.schemas.update import ItemUpdateSchema
from app.schemas.response import ResponseItemSchema, ResponseItemUpdateSchema

item_router = APIRouter(prefix="/item",tags=["item"])
#cadastrar item manualmente
@item_router.post("/item/",response_model=ResponseItemSchema)
async def cadastrar_item(item_schema: ItemSchema, session: SessionDep,usuario: UsuarioDep):
    require_permission(usuario.id,"create_item",session)
    item = itens.create(item_schema,session)
    return item
#editar informações de item
@item_router.patch("/item/{item_id}")
async def editar_item(item_id: int,item_update_schema: ItemUpdateSchema,session: SessionDep,usuario: UsuarioDep):
    require_permission(usuario.id,"edit_item",session)
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
    require_permission(usuario.id,"delete_item",session)
    item = itens.delete(item_id,session)
    return {
        "item removido": item
    }
#visualizar item
@item_router.get("/item/{item_id}",response_model=ResponseItemSchema)
async def visualizar_item(item_id: int, session: SessionDep,usuario: UsuarioDep):
    require_permission(usuario.id,"view_item",session)
    item = itens.read(item_id,session)
    return item
