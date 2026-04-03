from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

from services.transacao import Transacao

router = APIRouter(prefix= "/transacao")

@router.get('/user/{id}')
async def read_transacoes_by_user_id(id : int, db : AsyncSession = Depends(get_db)):

    result = await Transacao.ler_transacoes_usuario(id, db)

    if result == "USUARIO_SEM_EXTRATOS":

        raise HTTPException(
            status_code= 404,
            detail= "Extratos do cliente nao foram encontrados"
        )
    
    return result



@router.get("/user/{id}/pagamentos/")
async def read_pagamentos_by_user_id(id : int, db : AsyncSession = Depends(get_db)):

    result = await Transacao.ler_pagamentos_usuario(id, db)

    if result == "USUARIO_SEM_EXTRATOS":

        raise HTTPException(
            status_code= 404,
            detail= "Extratos do cliente nao foram encontrados"
        )
    
    return result



@router.get("/user/{id}/pagamentos/mesal/")
async def read_pagamentos_mensal(id : int, db : AsyncSession = Depends(get_db)):

    result = await Transacao.ler_pagamentos_mensais_usuario(id, db)

    if result == "USUARIO_SEM_EXTRATOS":

        raise HTTPException(
            status_code= 404,
            detail= "Extratos do cliente nao foram encontrados"
        )

    return result

    