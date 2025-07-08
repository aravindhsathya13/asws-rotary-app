"""
models.py: Data models for Rotary Club Anniversary Management System
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Member:
    """Data class for club members"""
    id: Optional[int]
    name: str
    phone: str
    birthday: str  # Format: DD-MM
    wedding_anniversary: Optional[str]  # Format: DD-MM
    spouse_name: Optional[str]
    email: Optional[str]
    title: Optional[str] = None
    relationship_status: Optional[str] = None
