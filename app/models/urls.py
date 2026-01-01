from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Model


class Url(Model):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    url: Mapped[str] = mapped_column(String(255))
    short_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
