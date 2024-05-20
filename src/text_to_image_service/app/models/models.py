# myapp/models.py
from ..database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone


class Text2TextOperation(Base):
    __tablename__ = 'text2text_operation'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference = Column(String(50))
    original_text = Column(String(10000))
    generated_text = Column(String(10000))
    generated_script = Column(String(10000))
    created_date = Column(DateTime, default=datetime.now(timezone.utc))
    storyboards = relationship(
        "Text2TextOperationStoryboard", back_populates="text2text_operation")


class Text2TextOperationStoryboard(Base):
    __tablename__ = 'text2text_operation_storyboard'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text2text_operation_id = Column(UUID, ForeignKey(
        'text2text_operation.id'), nullable=False)
    text2text_operation = relationship(
        "Text2TextOperation", back_populates="storyboards")
    generated_text = Column(String(10000))
    order = Column(Integer)
