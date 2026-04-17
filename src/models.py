"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class Activity(BaseModel):
    """Activity model"""
    name: str
    description: str
    schedule: str
    max_participants: int
    participants: List[EmailStr] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu"]
            }
        }


class ActivityResponse(Activity):
    """Activity response model with ID"""
    id: Optional[str] = Field(None, alias="_id")

    class Config:
        populate_by_name = True


class Participant(BaseModel):
    """Participant model"""
    email: EmailStr
    name: str
    grade: Optional[str] = None
    activities: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "email": "michael@mergington.edu",
                "name": "Michael Johnson",
                "grade": "10",
                "activities": ["Chess Club", "Programming Class"]
            }
        }


class ParticipantResponse(Participant):
    """Participant response model with ID"""
    id: Optional[str] = Field(None, alias="_id")

    class Config:
        populate_by_name = True


class SignupRequest(BaseModel):
    """Request model for activity signup"""
    email: EmailStr


class SignupResponse(BaseModel):
    """Response model for signup"""
    message: str
    activity: str
    email: str
