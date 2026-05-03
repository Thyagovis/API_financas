from fastapi import APIRouter, status,HTTPException, Response, Depends
from schemas.auth import AuthIn
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.auth import Auth
from core.security import create_acess_token


router = APIRouter(prefix='/auth')

@router.post('/', status_code= status.HTTP_200_OK,)
async def login(user: AuthIn, response : Response, db : AsyncSession = Depends(get_db)):

    result =  await Auth.Login(user, db)

    if result == 'EMAIL_NAO_ENCONTRADO':

        raise HTTPException(
            status_code= 404,
            detail= 'Usuario não encontrado'
        )
    
    if result == 'SENHA_INCORRETA':

        raise HTTPException(
            status_code= 401,
            detail= 'Senha incorreta'
        )
    
    token = create_acess_token(result.id)

    print(result.id)
    
    response.set_cookie(
        key= 'access_token',
        value = token,
        httponly= True,
        secure= True,
        samesite= 'none',
        path= '/',
        domain=None
    )
    
    return {'message' : 'Login realizado com sucesso'}