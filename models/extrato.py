from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from database import Base
from datetime import datetime,UTC


class Extrato(Base):

    __tablename__ = "Extrato"

    id : Mapped[int] = mapped_column(primary_key= True, autoincrement= True, index= True)
    user_id : Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete= "CASCADE"))
    bank : Mapped[str] = mapped_column(String)
    name : Mapped[str] = mapped_column(String)
    created_at : Mapped[datetime] = mapped_column(default= datetime.now(UTC))

    usuario = relationship("Usuario", back_populates="extratos")
    transacao = relationship('Transacoes', back_populates = 'extratos', cascade = "all, delete")