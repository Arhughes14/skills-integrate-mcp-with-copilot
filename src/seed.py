"""
Database seeding script to populate initial activities data.
"""

import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncClient
from config import MONGODB_URL, DATABASE_NAME, ACTIVITIES_COLLECTION


async def seed_activities():
    """Seed the database with initial activities data."""
    
    client = AsyncClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        # Check if activities already exist
        count = await db[ACTIVITIES_COLLECTION].count_documents({})
        if count > 0:
            print(f"Database already contains {count} activities. Skipping seed.")
            return
        
        # Initial activities data
        activities_data = [
            {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Programming Class",
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Gym Class",
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Soccer Team",
                "description": "Join the school soccer team and compete in matches",
                "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 22,
                "participants": ["liam@mergington.edu", "noah@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Basketball Team",
                "description": "Practice and play basketball with the school team",
                "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 15,
                "participants": ["ava@mergington.edu", "mia@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Art Club",
                "description": "Explore your creativity through painting and drawing",
                "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 15,
                "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Drama Club",
                "description": "Act, direct, and produce plays and performances",
                "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                "max_participants": 20,
                "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Math Club",
                "description": "Solve challenging problems and participate in math competitions",
                "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
                "max_participants": 10,
                "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Debate Team",
                "description": "Develop public speaking and argumentation skills",
                "schedule": "Fridays, 4:00 PM - 5:30 PM",
                "max_participants": 12,
                "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        # Insert activities into database
        result = await db[ACTIVITIES_COLLECTION].insert_many(activities_data)
        print(f"Successfully seeded {len(result.inserted_ids)} activities into the database")
        
        # Create index on activity name for faster lookups
        await db[ACTIVITIES_COLLECTION].create_index("name", unique=True)
        print("Created unique index on activity name")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        raise
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_activities())
