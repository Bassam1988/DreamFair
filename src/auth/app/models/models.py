# myapp/models.py
from ..database import Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  # Specific to PostgreSQL
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = 'users'

    # Use UUID as primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(255))  # Added password column
    roles = relationship('Role', secondary='user_roles',
                         back_populates="users")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)
    users = relationship('User', secondary='user_roles',
                         back_populates="roles")


class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    role_id = Column(UUID, ForeignKey('roles.id'), primary_key=True)
