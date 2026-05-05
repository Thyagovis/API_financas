from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db

from dependencies.auth import get_current_user
from services.transacao import Transacao

router = APIRouter(prefix= "/transacao")

@router.get('/user/me')
async def read_transacoes_by_user_id(user_id : int = Depends(get_current_user), db : AsyncSession = Depends(get_db)):

    result = await Transacao.ler_transacoes_usuario(user_id, db)

    if result == "USUARIO_SEM_EXTRATOS":

        raise HTTPException(
            status_code= 404,
            detail= "Extratos do cliente nao foram encontrados"
        )
    
    return result



@router.get("/user/me/pagamentos/")
async def read_pagamentos_by_user_id(user_id : int = Depends(get_current_user), db : AsyncSession = Depends(get_db)):

    result = await Transacao.ler_pagamentos_usuario(user_id, db)

    if result == "USUARIO_SEM_EXTRATOS":

        raise HTTPException(
            status_code= 404,
            detail= "Extratos do cliente nao foram encontrados"
        )
    
    return result



@router.get("/user/me/pagamentos/mesal/")
async def read_pagamentos_mensal(user_id : int = Depends(get_current_user), db : AsyncSession = Depends(get_db)):

    result = await Transacao.ler_pagamentos_mensais_usuario(user_id, db)

    if result == "USUARIO_SEM_EXTRATOS":

        raise HTTPException(
            status_code= 404,
            detail= "Extratos do cliente nao foram encontrados"
        )

    return result

    