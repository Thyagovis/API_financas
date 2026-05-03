from schemas.user import UsuarioIn

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from models.user import Usuario
from core.security import hash_password




class Usuarios:

    async def adicionar_usuario(usuario : UsuarioIn, db : AsyncSession):

        user = Usuario(
            nome = usuario.nome,
            email = usuario.email,
            password = hash_password(usuario.password)
        )

        try:

            db.add(user)
            await db.commit()
            await db.refresh(user)

            return user
        
        except IntegrityError:

            await db.rollback()
            raise ValueError("Email já cadastrado!")
        
    

    async def ler_usuario_id(id : int, db : AsyncSession):

        result = await db.execute(
            select(Usuario).where(Usuario.id == id)
        )

        result = result.scalar_one_or_none()
        
        if result == None:

            return 'USUARIO_NAO_ENCONTRADO'

        return result
    


    async def delete_user_by_id(id : int, db : AsyncSession):

        user = await Usuarios.ler_usuario_id(id, db)

        if user == "USUARIO_NAO_ENCONTRADO":

            return user
        
        result = await db.delete(user)

        await db.commit()
        return "USUARIO_DELETADO"
    
        

