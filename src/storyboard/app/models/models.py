# myapp/models.py
from ..database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  # Specific to PostgreSQL
import uuid


class ScriptStyle(Base):
    __tablename__ = 'script_styles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)
    code_name = Column(String(20), unique=True)
    projects = relationship("Project", back_populates="script_style")


class StoryBoardStyle(Base):
    __tablename__ = 'storyboard_styles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)
    code_name = Column(String(20), unique=True)
    projects = relationship("Project", back_populates="storyboard_style")


class VideoDuration(Base):
    __tablename__ = 'video_durations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)
    code_name = Column(String(20), unique=True)
    projects = relationship("Project", back_populates="video_duration")


class AspectRatio(Base):
    __tablename__ = 'aspect_ratios'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)
    code_name = Column(String(20), unique=True)
    projects = relationship("Project", back_populates="aspect_ratio")


class BoardsPerMin(Base):
    __tablename__ = 'boards_per_mins'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)
    count = Column(Integer, unique=True)
    code_name = Column(String(20), unique=True)
    projects = relationship("Project", back_populates="boards_per_min")


class Project(Base):
    __tablename__ = 'projects'

    # Use UUID as primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(150))
    synopsis = Column(String(2500))
    script = Column(String(2500))
    script_style_id = Column(UUID, ForeignKey('script_styles.id'))
    script_style = relationship("ScriptStyle", back_populates="projects")
    storyboard_style_id = Column(UUID, ForeignKey(
        'storyboard_styles.id'))
    storyboard_style = relationship(
        "StoryBoardStyle", back_populates="projects")
    video_duration_id = Column(UUID, ForeignKey(
        'video_durations.id'))
    video_duration = relationship("VideoDuration", back_populates="projects")
    aspect_ratio_id = Column(UUID, ForeignKey(
        'aspect_ratios.id'))
    aspect_ratio = relationship("AspectRatio", back_populates="projects")
    boards_per_min_id = Column(UUID, ForeignKey(
        'boards_per_mins.id'))
    boards_per_min = relationship("BoardsPerMin", back_populates="projects")
    storyboards = relationship("Storyboard", back_populates="project")


class Storyboard(Base):
    __tablename__ = 'storyboards'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID, ForeignKey('projects.id'), nullable=False)
    project = relationship("Project", back_populates="storyboards")
    name = Column(String(150))
    image = Column(String(2500))
    scene_description = Column(String(2500))