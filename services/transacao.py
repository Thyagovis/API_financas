from schemas.transacao import TransacaoIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from models.transacao import Transacoes
from fastapi import UploadFile

import io
import re
from ofxparse import OfxParser

from models.transacao import Transacoes
from models.extrato import Extrato

class Transacao():


    #func auxiliar para Extrato.adicionar_extrato
    async def registrar_transacoes(extrato_id: int, file : UploadFile, db : AsyncSession):

        def limpar_ofx(text: str) -> str:
            text = re.sub(r"<NAME>\s*</NAME>", "<NAME>Sem descricao</NAME>", text)
            return text

        contents = await file.read()
        text = contents.decode("latin-1")
        text = limpar_ofx(text)
        ofx = OfxParser.parse(io.StringIO(text))



        transacoes = ofx.account.statement.transactions



        for transacao in transacoes:

            transacao_query = Transacoes(
                extrato_id = extrato_id,
                transaction_id = transacao.id,
                valor = transacao.amount,
                desc =  (
                    getattr(transacao, "name", None)
                    or getattr(transacao, "memo", None)
                    or getattr(transacao, "payee", None)
                    or "Sem descrição"
                ),
                tipo = transacao.type,
                date = transacao.date
            )

            db.add(transacao_query)


    
    async def ler_transacoes_usuario(user_id : int, db : AsyncSession):

        extratos_id = await db.execute(select(Extrato.id).where(Extrato.user_id == user_id))
        extratos_id = extratos_id.scalars().all()
        all_transacoes = []

        if extratos_id == []:

            return "USUARIO_SEM_EXTRATOS"

        for id in extratos_id:

            result = await db.execute(select(Transacoes).where(Transacoes.extrato_id == id))

            all_transacoes.append(result.scalars().all())


        return all_transacoes



    async def ler_pagamentos_usuario(user_id : int, db : AsyncSession):

        extratos_id = await db.execute(select(Extrato.id).where(Extrato.user_id == user_id))
        extratos_id = extratos_id.scalars().all()
        transacoes = []
        total_gasto = 0

        if extratos_id == []:

            return "USUARIO_SEM_EXTRATOS"
        
        for id in extratos_id:

            result_transacao = await db.execute(select(Transacoes).where(Transacoes.extrato_id == id, Transacoes.tipo == "payment"))
            gastos = await db.execute(select(Transacoes.valor).where(Transacoes.extrato_id == id, Transacoes.tipo == "payment"))

            result_transacao = result_transacao.scalars().all()
            gastos = gastos.scalars().all()

            total_gasto += sum(gastos)
            transacoes.extend(result_transacao)

        return {
            "total_gasto" : total_gasto,
            "transacoes" : transacoes
        }



    async def ler_pagamentos_mensais_usuario(user_id : int, db : AsyncSession):


        extratos_id = await db.execute(select(Extrato.id).where(Extrato.user_id == user_id))
        extratos_id = extratos_id.scalars().all()

        all_meses = []
        all_valores = []
        meses_valores = {}

        if extratos_id == []:

            return "USUARIO_SEM_EXTRATOS"

        for id in extratos_id:

            meses = await db.execute(
                
                select(func.strftime("%m/%Y", Transacoes.date))
                .distinct()
                .where(Transacoes.extrato_id == id, Transacoes.tipo == "payment")
                .order_by(Transacoes.date)
            )

            valores = await db.execute(
                select(func.strftime("%m/%Y", Transacoes.date).label('mes'), Transacoes.valor)
                .where(Transacoes.extrato_id == id, Transacoes.tipo == "payment")
            )

            for row in valores:

                all_valores.append({"mes": row.mes, "valor": row.valor})


            all_meses.extend(meses.scalars().all())

        for mes in all_meses:

            meses_valores[mes] = 0

        for row in all_valores:

            meses_valores[row["mes"]] += row['valor']


        return meses_valores
         

         
