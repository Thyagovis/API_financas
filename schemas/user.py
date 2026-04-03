from pydantic import BaseModel, EmailStr

class UsuarioIn(BaseModel):

    nome : str
    email : EmailStr
    password : str