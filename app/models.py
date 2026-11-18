
from sqlalchemy import Column, Integer, String, Float, DateTime, func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )



class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)

    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)

    type = Column(String(20), nullable=False)

    result = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"Calculation(id={self.id}, a={self.a}, "
            f"b={self.b}, type='{self.type}', "
            f"result={self.result})"
        )
