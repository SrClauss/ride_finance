from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- Schemas de Token ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# --- Schemas de Usuário ---
# Schema para criar um novo usuário (recebido pela API)
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, description="Username com pelo menos 3 caracteres")
    password: str = Field(..., min_length=6, description="Senha com pelo menos 6 caracteres")
    email: EmailStr
    full_name: str = Field(..., min_length=2)
    phone: str = Field(..., min_length=10)


# Schema para o login do usuário
class UserLogin(BaseModel):
    username: str
    password: str


# Schema base para dados do usuário (usado para compor outros schemas)
class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Schema para os dados do usuário que são retornados pela API (seguro, sem senha)
class User(UserBase):
    is_paid: bool
    plan_status: str
    trial_ends_at: Optional[datetime] = None
    payment_status: Optional[str] = None
    payment_method: Optional[str] = None


# --- Schemas de Categoria ---
class CategoryBase(BaseModel):
    name: str
    type: str  # 'income' or 'expense'
    icon: Optional[str] = None
    color: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    is_default: bool

    model_config = ConfigDict(from_attributes=True)


# --- Schemas de Transação ---
class TransactionBase(BaseModel):
    amount: Decimal = Field(..., max_digits=10, decimal_places=2)
    description: Optional[str] = None
    type: str  # 'income' or 'expense'
    source: Optional[str] = None
    date: datetime
    category_id: int


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Schemas de Sessão de Trabalho ---
class WorkSessionBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    total_minutes: Optional[int] = None
    date: str  # Formato YYYY-MM-DD


class WorkSessionCreate(WorkSessionBase):
    pass


class WorkSession(WorkSessionBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Schemas de Meta ---
class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: str  # 'daily', 'weekly', etc.
    category: str  # 'income', 'hours', etc.
    target: Decimal = Field(..., max_digits=10, decimal_places=2)
    current: Optional[Decimal] = Field(Decimal('0'), max_digits=10, decimal_places=2)
    deadline: str  # ISO date string
    priority: str = "medium"
    is_active: bool = True
    is_completed: bool = False


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
        
        
# (Adicione estas classes ao final do arquivo app/models/schemas.py)

# --- Schemas de Perfil Abrangente ---

class ProfileStats(BaseModel):
    total_trips: int
    total_earnings: Decimal
    total_expenses: Decimal
    net_profit: Decimal
    total_hours: int
    average_per_trip: Decimal
    average_per_hour: Decimal
    best_month_earnings: Decimal
    monthly_average_earnings: Decimal

class MonthlyPerformance(BaseModel):
    month: str
    income: Decimal
    expenses: Decimal
    profit: Decimal
    trips: int

class PlatformBreakdown(BaseModel):
    name: str
    earnings: Decimal
    trips: int
    percentage: float

class Achievement(BaseModel):
    id: int
    title: str
    description: str
    achieved: bool
    date: Optional[datetime] = None
    progress: float
    goal: int

class ActivityDay(BaseModel):
    date: str

class ProfileComprehensive(BaseModel):
    personal_info: User
    stats: ProfileStats
    monthly_performance: List[MonthlyPerformance]
    platform_breakdown: List[PlatformBreakdown]
    achievements: List[Achievement]
    # Adicionaremos o 'activity_calendar' diretamente no endpoint por simplicidade