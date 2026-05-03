from schemas.auth import AuthIn
from models.user import Usuario
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import verify_password

class Auth:

    async def Login(user : AuthIn, db : AsyncSession):

        result = await db.execute(
            select(Usuario)
            .where(Usuario.email == user.gmail)
        )

        result = result.scalar_one_or_none()

        if result == None:

            return "EMAIL_NAO_ENCONTRADO"

        correct_pass = verify_password(user.password, result.password)
        print(correct_pass)    
        if correct_pass:

            return result
        
        else:

            return 'SENHA_INCORRETA'
