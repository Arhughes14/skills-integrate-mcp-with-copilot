# MongoDB Integration Setup Guide

This feature integrates MongoDB as the persistent database backend, replacing the in-memory data storage.

## What Changed

### New Files Created
- `src/config.py` - Configuration management and environment variables
- `src/database.py` - MongoDB connection setup and management
- `src/models.py` - Pydantic models for validation and serialization
- `src/seed.py` - Database seeding script for initial data
- `.env.example` - Environment variable template
- `.env` - Local environment configuration (for development)

### Files Updated
- `requirements.txt` - Added MongoDB drivers (pymongo, motor) and dependencies
- `src/app.py` - Converted from in-memory to async MongoDB-backed routes

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB

**Option A: Using Docker (Recommended)**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Option B: Local MongoDB installation**
Make sure MongoDB is running on `localhost:27017`

### 3. Seed the Database
Run the seed script to populate initial activities:
```bash
cd src
python seed.py
```

You should see output like:
```
Successfully seeded 9 activities into the database
Created unique index on activity name
```

### 4. Run the Application
```bash
cd src
python -m uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## Database Features

- **Persistent Storage**: All data survives application restarts
- **Automatic Indexing**: Unique index on activity names for performance
- **Timestamps**: All activities track `created_at` and `updated_at`
- **Async Operations**: Uses Motor for non-blocking database calls
- **Capacity Tracking**: Enforces maximum participant limits

## API Changes

The API endpoints remain the same, but now support:
- Query parameter for signup: `/activities/{activity_name}/signup?email=...` (GET) or POST with JSON body
- Persistent participant registration
- Real-time data updates

### Example Signup (POST)
```bash
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "student@mergington.edu"}'
```

## Configuration

Edit `.env` to customize:
- `MONGODB_URL` - MongoDB connection string
- `DATABASE_NAME` - Database name in MongoDB
- `DEBUG` - Enable/disable debug mode

## Verification

To verify the setup:
1. Access the API at `http://localhost:8000`
2. View activities: `GET http://localhost:8000/activities`
3. MongoDB should contain a `mergington_high_school` database with an `activities` collection
