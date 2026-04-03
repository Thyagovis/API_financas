from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from controllers import user, extrato, transacao

# Importando os models
from models.user import Usuario
from models.extrato import Extrato
from models.transacao import Transacoes


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(extrato.router)
app.include_router(transacao.router)