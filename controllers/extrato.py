from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from dependencies.auth import get_current_user
from services.extrato import Extratos
from schemas.extrato import ExtratoIn
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix= "/extrato")


@router.post("/add")
async def create_extrato(banco : str = Form(...),  file : UploadFile = File(...),user_id : int = Depends(get_current_user), db : AsyncSession = Depends(get_db)):

    result = await Extratos.adicionar_extrato(user_id , banco, file, db)

    if result == "USUARIO_NAO_ENCONTRADO":

        raise HTTPException(
            status_code= 404,
            detail= "Usuario não encontrado"
        )
    
    if result == "IMPOSSIVEL_REGISTRAR_EXTRATO":
    
        raise HTTPException(
            status_code= 500,
            detail= "Impossivel registrar extrato"
        )

    return result



@router.get("/user/me")
async def read_all_extratos_user(user_id : int = Depends(get_current_user), db : AsyncSession = Depends(get_db)):

    result = await Extratos.ler_extratos_user(id, db)

    if result == "USUARIO_SEM_EXTRATOS":

        raise HTTPException(
            status_code= 404,
            detail= "Usuario nao possui extratos registrados"
        )
    
    return result



@router.delete("/delete/me")
async def delete_extrato(user_id : int = Depends(get_current_user), db : AsyncSession = Depends(get_db)):

    result = await Extratos.remover_extrato(id, db)

    if result == "EXTRATO_NAO_ENCONTRADO":

        raise HTTPException(
            status_code = 404,
            detail = "Extrato nao encontrado"
        )

    return result