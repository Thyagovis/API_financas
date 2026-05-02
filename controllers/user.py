from fastapi import APIRouter, Depends, status, HTTPException
from database import get_db
from schemas.user import UsuarioIn
from views.user import UsuarioOut
from sqlalchemy.ext.asyncio import AsyncSession
from services.user import Usuarios

router = APIRouter(prefix= "/users")


@router.post("/add", status_code= status.HTTP_201_CREATED, response_model= UsuarioOut)
async def create_user(usuario : UsuarioIn, db : AsyncSession = Depends(get_db)):

    return await Usuarios.adicionar_usuario(usuario, db)



@router.get("/{id}", status_code= status.HTTP_200_OK, response_model= UsuarioOut)
async def read_user_by_id(id : int, db : AsyncSession = Depends(get_db)):

    response = await Usuarios.ler_usuario_id(id, db)

    if response == 'USUARIO_NAO_ENCONTRADO':

        raise HTTPException(
            status_code= 404,
            detail= 'Usuario não encontrado'
        )

    return response



@router.delete("/delete/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_user(id : int, db : AsyncSession = Depends(get_db)):

    result = await Usuarios.delete_user_by_id(id, db)

    if result == "USUARIO_NAO_ENCONTRADO":

        raise HTTPException(
            status_code= 404,
            detail = "Usuario não encontrado"
        )
    
    return result



    