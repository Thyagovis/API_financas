from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import engine, Base
from controllers import user, extrato, transacao, auth

# Importando os models
from models.user import Usuario
from models.extrato import Extrato
from models.transacao import Transacoes

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  # React/Vite
    "http://127.0.0.1:3000",
    # adicione aqui seu domínio depois (produção)
]



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
app.include_router(auth.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # quem pode acessar
    allow_credentials=True,       # cookies / auth
    allow_methods=["*"],          # GET, POST, PUT...
    allow_headers=["*"],          # headers liberados
)