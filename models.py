from sqlalchemy import Column, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
