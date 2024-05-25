#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Dict, Union
from pydantic import BaseModel


from model import Flight

router = APIRouter()


@router.post("/", response_description="Post a new flight", status_code=status.HTTP_201_CREATED, response_model=Flight)
def create_flight(request: Request, flight: Flight = Body(...)):
    flight_dict = flight.dict()
    new_flight = request.app.database["flights"].insert_one(flight_dict)
    created_flight = request.app.database["flights"].find_one({"_id": new_flight.inserted_id})
    
    if created_flight:
        created_flight["_id"] = str(created_flight["_id"])
        created_flight["from"] = created_flight.pop("from_")
        return created_flight
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create flight")



    

@router.get("/", response_description="Get all flights", response_model=List[Flight])
async def list_flights(request: Request, age: int = 0, limit: int = 0):
    flights = list(request.app.database["flights"].find({"age": {"$gte": age}}).limit(limit))
    ##print(flights)
    for flight in flights:
        flight["_id"] = str(flight["_id"])
    return flights

@router.get("/busiest_airports", response_description="Get the busiest airports", response_model=List[Dict[str, Union[str, int]]])
async def get_busiest_airports(request: Request, num_airports: int = 10):
    pipeline = [
        {
            "$facet": {
                "departures": [
                    {
                        "$group": {
                            "_id": "$from",
                            "total_passengers": { "$sum": 1 }
                        }
                    }
                ],
                "arrivals": [
                    {
                        "$group": {
                            "_id": "$to",
                            "total_passengers": { "$sum": 1 }
                        }
                    }
                ]
            }
        },
        {
            "$project": {
                "traffic": { "$concatArrays": ["$departures", "$arrivals"] }
            }
        },
        {
            "$unwind": {
                "path": "$traffic",
                "includeArrayIndex": "index"
            }
        },
        {
            "$group": {
                "_id": "$traffic._id",
                "total_passengers": { "$sum": "$traffic.total_passengers" }
            }
        },
        {
            "$sort": {"total_passengers": -1}
        },
        {
            "$limit": num_airports
        }
    ]

    cursor = request.app.database["flights"].aggregate(pipeline)
    busiest_airports = list(cursor)

    return busiest_airports

@router.get("/busiest_airports/months", response_description="Get the busiest months from an airport", response_model=List[Dict[str, Union[str, int]]])
async def get_busiest_airport_months(request: Request, airport_code: str, num_months: int = 10):
    pipeline = [
        {
            "$match": {
                "$or": [
                    { "from": airport_code },
                    { "to": airport_code }
                ]
            }
        },
        {
            "$group": {
                "_id": "$month",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": num_months
        }
    ]

    cursor = request.app.database["flights"].aggregate(pipeline)
    busiest_months = list(cursor)

    return busiest_months

@router.get("/most_active_months", response_description="Get the most active months for an airline at an airport", response_model=List[Dict[str, Union[str, int]]])
async def get_most_active_months(request: Request, airport_code: str, airline_name: str):
    pipeline = [
        {
            "$match": {
                "from": airport_code,
                "airline": airline_name
            }
        },
        {
            "$group": {
                "_id": "$month",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        }
    ]

    cursor = request.app.database["flights"].aggregate(pipeline)
    most_active_months = list(cursor)

    return most_active_months

@router.get("/vacation_months", response_description="Get the vacation months for an airport", response_model=List[Dict[str, Union[str, int]]])
async def get_vacation_months(request: Request, airport_code: str):
    pipeline = [
        {
            "$match": {
                "$or": [
                    { "from": airport_code },
                    { "to": airport_code }
                ],
                "reason": "On vacation/Pleasure"
            }
        },
        {
            "$group": {
                "_id": "$month",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        }
    ]

    cursor = request.app.database["flights"].aggregate(pipeline)
    vacation_months = list(cursor)

    return vacation_months
