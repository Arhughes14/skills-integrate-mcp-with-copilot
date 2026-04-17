"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Uses MongoDB for persistent data storage.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from datetime import datetime
from bson.objectid import ObjectId

from database import connect_db, close_db, get_db
from models import Activity, ActivityResponse, SignupRequest, SignupResponse
from config import ACTIVITIES_COLLECTION

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


# Startup and shutdown events
@app.on_event("startup")
async def startup():
    """Initialize database connection on application startup."""
    await connect_db()
    print("Application startup complete")


@app.on_event("shutdown")
async def shutdown():
    """Close database connection on application shutdown."""
    await close_db()
    print("Application shutdown complete")


# Legacy in-memory activity database (for reference, kept but not used)
activities_legacy = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
async def get_activities():
    """Get all activities from the database."""
    db = get_db()
    activities_collection = db[ACTIVITIES_COLLECTION]
    
    # Fetch all activities from MongoDB
    cursor = activities_collection.find()
    activities = []
    async for activity in cursor:
        # Convert ObjectId to string for JSON serialization
        activity["_id"] = str(activity["_id"])
        activities.append(activity)
    
    return activities


@app.post("/activities/{activity_name}/signup")
async def signup_for_activity(activity_name: str, signup_request: SignupRequest):
    """Sign up a student for an activity"""
    email = signup_request.email
    db = get_db()
    activities_collection = db[ACTIVITIES_COLLECTION]
    
    # Validate activity exists
    activity = await activities_collection.find_one({"name": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Validate student is not already signed up
    if email in activity.get("participants", []):
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )
    
    # Validate capacity hasn't been reached
    current_participants = len(activity.get("participants", []))
    if current_participants >= activity.get("max_participants", 0):
        raise HTTPException(
            status_code=400,
            detail="Activity is at maximum capacity"
        )
    
    # Add student to the activity
    result = await activities_collection.update_one(
        {"name": activity_name},
        {
            "$push": {"participants": email},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to register for activity")
    
    return SignupResponse(
        message=f"Successfully signed up {email} for {activity_name}",
        activity=activity_name,
        email=email
    )


@app.delete("/activities/{activity_name}/unregister")
async def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    db = get_db()
    activities_collection = db[ACTIVITIES_COLLECTION]
    
    # Validate activity exists
    activity = await activities_collection.find_one({"name": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Validate student is signed up
    if email not in activity.get("participants", []):
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )
    
    # Remove student from the activity
    result = await activities_collection.update_one(
        {"name": activity_name},
        {
            "$pull": {"participants": email},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to unregister from activity")
    
    return {"message": f"Unregistered {email} from {activity_name}"}
