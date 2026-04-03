from pydantic import BaseModel
from datetime import datetime

class UsuarioOut(BaseModel):

    nome : str
    email : str
    created_at : datetime