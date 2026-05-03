from pydantic import BaseModel

class AuthIn(BaseModel):

    gmail : str
    password : str
