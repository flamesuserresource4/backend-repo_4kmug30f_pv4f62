"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --------------------------------------------------
# Expense Tracker Schemas
# Each class below becomes its own collection using the lowercase
# class name. For example: Expense -> "expense", Category -> "category".
# --------------------------------------------------

class Category(BaseModel):
    name: str = Field(..., description="Category name, e.g., Groceries, Rent")
    color: str = Field("#6366F1", description="Hex color for UI tags")

class Expense(BaseModel):
    title: str = Field(..., description="Short description, e.g., Coffee at Starbucks")
    amount: float = Field(..., gt=0, description="Positive amount in the selected currency")
    category: str = Field(..., description="Category name (reference to Category.name)")
    date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="When the expense occurred")
    notes: Optional[str] = Field(None, description="Optional notes")

class Budget(BaseModel):
    category: str = Field(..., description="Category this budget applies to")
    limit: float = Field(..., gt=0, description="Spending limit for the period")
    period: str = Field("monthly", description="Budget period: daily/weekly/monthly/quarterly/yearly")

# Example schemas kept for reference (not used by the app directly)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True

# Note: The Flames database viewer can read these schemas from GET /schema
# for validation and quick CRUD management.
