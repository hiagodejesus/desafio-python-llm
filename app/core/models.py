from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base


class Classifications(Base):
    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    confidence = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Classification(id={self.id}, category={self.category}, tags={self.tags}, confidence={self.confidence})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "tags": self.tags or [],
        }
