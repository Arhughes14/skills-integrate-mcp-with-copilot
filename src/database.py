"""
Database connection and utilities for MongoDB.
"""

import motor.motor_asyncio
from typing import Optional
from config import MONGODB_URL, DATABASE_NAME

# Global database client and db instance
client: Optional[motor.motor_asyncio.AsyncClient] = None
db = None


async def connect_db():
    """
    Connect to MongoDB database.
    Call this on application startup.
    """
    global client, db
    client = motor.motor_asyncio.AsyncClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    # Test the connection
    try:
        await client.admin.command('ping')
        print(f"Successfully connected to MongoDB database: {DATABASE_NAME}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


async def close_db():
    """
    Close the MongoDB database connection.
    Call this on application shutdown.
    """
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_db():
    """
    Get the database instance.
    """
    if db is None:
        raise RuntimeError("Database not connected. Call connect_db() first.")
    return db
