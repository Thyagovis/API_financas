from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Date
from core.database import Base
from datetime import date

class Transacoes(Base):

    __tablename__ = "Transacoes"

    id : Mapped[int] = mapped_column(primary_key= True, autoincrement= True, index= True)
    extrato_id : Mapped[int] = mapped_column(ForeignKey("Extrato.id", ondelete= "CASCADE"))
    transaction_id : Mapped[str] = mapped_column(nullable= False, unique= True)
    valor : Mapped[float] = mapped_column(Float, nullable= False)
    desc : Mapped[str] = mapped_column(String)
    tipo : Mapped[str] = mapped_column(String)
    date : Mapped[date] = mapped_column(Date)

    extratos = relationship("Extrato", back_populates= "transacao") 