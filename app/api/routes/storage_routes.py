from sqlalchemy import and_, or_
from fastapi import APIRouter, HTTPException, Depends
from app.models import Corredor
import app.crud.corredores as corredores
from app.api.dependencies import UsuarioDep, SessionDep,verify_token, require_permission
from app.schemas.entry import CorredorSchema, ItemCorredorSchema
from app.schemas.update import CorredorUpdateSchema
from app.schemas.response import ResponseCorredorSchema, ResponseCorredorUpdateSchema 

storage_router = APIRouter(prefix="/storage",tags=["storage"],dependencies=[Depends(verify_token)])

@storage_router.get("/")
async def storage():
    return{
        "mensagem": "bem vindo a rota de armazenamento"
    }
#visualizar corredor
@storage_router.get("/corridor/{id_corredor}",response_model=ResponseCorredorSchema)
async def visualizar_corredor(id_corredor: int, session: SessionDep,usuario: UsuarioDep):
    require_permission(usuario.role,"view_corridor",session)
    corredor = corredores.read(id_corredor,session)
    return corredor
#criar corredor
@storage_router.post("/corridor")
async def criar_corredor(corredor_schema: CorredorSchema,session: SessionDep,usuario: UsuarioDep):
    require_permission(usuario.role,"create_corridor",session)
    novo_corredor = corredores.create(corredor_schema,session)
    return {
        "mensagem":f"corredor {novo_corredor.nome} criado com sucesso",
        "corredor_id": novo_corredor.id
    }
#editar corredor
@storage_router.patch("/corridor/{id_corredor}",response_model=ResponseCorredorUpdateSchema)
async def editar_corredor(id_corredor: int,corredor_update_schema: CorredorUpdateSchema, session: SessionDep,usuario: UsuarioDep):
    require_permission(usuario.role,"edit_corridor",session)
    novo_corredor: list = corredores.update(id_corredor,corredor_update_schema,session)
    corredor: Corredor = novo_corredor[1]

    return{
        "mensagem": f"Corredor {corredor.id} alterado com sucesso",
        "campos_alterados": novo_corredor[0],
        "corredor": corredor
    }
#adcionar item ao corredor
@storage_router.post("/corridor/{id_corridor}")
async def adcionar_ao_corredor(id_corridor: int,item_corredor_schema: ItemCorredorSchema,session: SessionDep,usuario: UsuarioDep):
    require_permission(usuario.role,"adcionar_ao_corredor",session)
    item_corredor = corredores.add_item(id_corridor,item_corredor_schema,session)
    return {
        "mensagem": f"item de id {item_corredor.id} adcionado com sucesso ao corredor de id {id_corridor}"
    }
#apagar corredor
@storage_router.delete("/corridor/{id_corredor}")
async def deletar_corredor(id_corredor: int, session: SessionDep,usuario: UsuarioDep):
    require_permission(usuario.role,"delete_corridor",session)
    corredor_apagado  =  corredores.delete(id_corredor, session)
    return {
        "mensagem": f"corredor de id {id_corredor} apagado com sucesso",
        "corredor": corredor_apagado
    }