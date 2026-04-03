from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas.extrato import ExtratoIn
from models.extrato import Extrato

from services.user import Usuarios
from services.transacao import Transacao



class Extratos():

    async def adicionar_extrato(user_id_pr : int, banco : str, extrato : UploadFile, db : AsyncSession):

        user_id = await Usuarios.ler_usuario_id(user_id_pr, db)

        if not user_id:

            return "USUARIO_NAO_ENCONTRADO"

        extrato_query = Extrato(
            user_id = user_id_pr,
            bank = banco,
            name = extrato.filename
        )

        try:

            db.add(extrato_query)
            await db.commit()
            await Transacao.registrar_transacoes(extrato_query.id, extrato, db)
            await db.commit()
            await db.refresh(extrato_query)

            return extrato_query
        
        except IntegrityError:

            await db.rollback()
            return "IMPOSSIVEL_REGISTRAR_EXTRATO"
        
    

    async def ler_extrato_id(id : int, db : AsyncSession):
        
        result = await db.execute(
            select(Extrato).where(Extrato.id == id)
        )

        return result.scalar_one_or_none()
    


    async def ler_extratos_user(user_id : int, db : AsyncSession):

        result = await db.execute(
            select(Extrato).where(Extrato.user_id == user_id)
        )

        if not result:

            return "USUARIO_SEM_EXTRATOS"

        return result.scalars().all()
    


    async def remover_extrato(id : int, db : AsyncSession):

        extrato = await Extratos.ler_extrato_id(id, db)

        if not extrato:

            return "EXTRATO_NAO_ENCONTRADO"
        
        result = await db.delete(extrato)

        await db.commit()

        return result
