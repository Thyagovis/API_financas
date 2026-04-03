from pydantic import BaseModel
from datetime import datetime

class TransacaoIn(BaseModel):

    extrato_id : int
    transaction_id : int
    valor : float
    desc : str
    tipo : str
    date : datetime