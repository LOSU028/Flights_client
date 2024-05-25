from pydantic import BaseModel, Field

class Flight(BaseModel):
    airline: str = Field(...)
    from_: str = Field(..., alias="from")
    to: str = Field(...)
    day: int = Field(...)
    month: int = Field(...)
    year: int = Field(...)
    duration: int = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    stay: str = Field(...)
    connection: bool = Field(...)
    wait: int = Field(...)
    ticket: str = Field(...)
    checked_bags: int = Field(...)
    carry_on: bool = Field(...)
    
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "airline": "Cathay Pacific",
                "from": "JFK",
                "to": "SJC",
                "day": 2,
                "month": 3,
                "year": 2022,
                "duration": 333,
                "age": 8,
                "gender": "female",
                "reason": "On vacation/Pleasure",
                "stay": "Hotel",
                "connection": True,
                "wait": 409,
                "ticket": "First Class",
                "checked_bags": 2,
                "carry_on": True
            }
        }
