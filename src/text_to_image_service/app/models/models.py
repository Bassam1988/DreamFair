# myapp/models.py
from ..database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone


class Text2ImageOperation(Base):
    __tablename__ = 'text2image_operation'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference = Column(String(50))
    script_text = Column(String(10000))
    created_date = Column(DateTime, default=datetime.now())
    images = relationship(
        "Text2ImageOperationImage", back_populates="text2image_operation")


class Text2ImageOperationImage(Base):
    __tablename__ = 'text2image_operation_image'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text2image_operation_id = Column(UUID, ForeignKey(
        'text2image_operation.id'), nullable=False)
    text2image_operation = relationship(
        "Text2ImageOperation", back_populates="images")
    scene_text = Column(String(10000))
    order = Column(Integer)
    url = Column(String(250))
    created_date = Column(DateTime, default=datetime.now())


class OperationErrors(Base):
    __tablename__ = 'operation_error'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference = Column(String(50))
    script_text = Column(String(10000))
    error = Column(String(25000))
    created_date = Column(DateTime, default=datetime.now())
