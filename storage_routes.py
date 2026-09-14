from fastapi import APIRouter

storage_router = APIRouter(prefix="/storage",tags=["storage"])

@storage_router.get("/")
async def storage():
    return{
        "mensagem": "bem vindo a rota de armazenamento"
    }