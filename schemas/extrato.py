from pydantic import BaseModel

class ExtratoIn(BaseModel):

    user_id : int
    name : str
