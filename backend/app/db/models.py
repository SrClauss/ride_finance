from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone = Column(String)
    is_paid = Column(Boolean, default=False)
    payment_id = Column(String)
    payment_method = Column(String)
    payment_status = Column(String, default="pending")
    subscription_type = Column(String, default="monthly")
    trial_ends_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = relationship("Category", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    work_sessions = relationship("WorkSession", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    settings = relationship("Setting", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    icon = Column(String)
    color = Column(String)
    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String)
    type = Column(String, nullable=False)
    source = Column(String)
    external_id = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    total_minutes = Column(Integer)
    date = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="work_sessions")


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    type = Column(String, nullable=False)  # 'daily', 'weekly', etc.
    category = Column(String, nullable=False)  # 'income', 'hours', etc.
    target = Column(DECIMAL(10, 2), nullable=False)
    current = Column(DECIMAL(10, 2), default=0)
    deadline = Column(String, nullable=False)
    priority = Column(String, default="medium")
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="goals")


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String, nullable=False)
    value = Column(JSON)

    user = relationship("User", back_populates="settings")