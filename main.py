#!/usr/bin/env python3
import os

from fastapi import FastAPI
from pymongo import MongoClient

from routes import router as book_router


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'iteso')

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]
    create_indexes()
    print(f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Bye bye...!!")

def create_indexes():
    flight_collection = app.database['flights']
    flight_collection.create_index([("from", 1)])
    flight_collection.create_index([("to", 1)])
    flight_collection.create_index([("age", 1)])

app.include_router(book_router, tags=["flights"], prefix="/flight")
