from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base
from datetime import datetime,UTC

class Usuario(Base):

    __tablename__ = "usuarios"

    id : Mapped[int] = mapped_column(primary_key= True, index = True, autoincrement= True)
    nome : Mapped[str] = mapped_column(String, nullable= False)
    email: Mapped[str] = mapped_column(String, nullable= False, unique= True)
    password : Mapped[str] = mapped_column(String, nullable= False)
    created_at : Mapped[datetime] = mapped_column(default= datetime.now(UTC))

    extratos = relationship(
        "Extrato",
        back_populates="usuario",
        cascade="all, delete"
    )