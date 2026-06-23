from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
import random

# Initialize the application
app = FastAPI(
    title="Cowrywise Learning API",
    description="Mini-projects covering GET routes, POST requests, and Pydantic validation.",
    version="1.0.0"
)

# ---------------------------------------------------------
# Mini-Project 1: "Hello FastAPI"
# ---------------------------------------------------------

@app.get("/")
async def root_route():
    """Returns a simple welcome message."""
    return {"message": "Welcome to the Cowrywise FastAPI Learning Project!"}


@app.get("/greet/{name}")
async def greet_route(name: str):
    """Takes a user's name as a path parameter and returns a personalized greeting."""
    return {"message": f"Hello, {name}! Welcome to the API."}


@app.get("/time")
async def time_route():
    """Returns the server's current date and time."""
    return {"server_time": datetime.now().isoformat()}


# Hardcoded list of quotes
quotes_list = [
    "The best way to predict the future is to invent it.",
    "Code is like humor. When you have to explain it, it’s bad.",
    "First, solve the problem. Then, write the code.",
    "Make it work, make it right, make it fast.",
    "Simplicity is the soul of efficiency."
]

@app.get("/quote")
async def quote_route(index: int | None = Query(default=None, description="Optional index of the quote to fetch")):
    """
    Returns a random quote. 
    Stretch Goal: If an 'index' query parameter is provided, returns that specific quote.
    """
    if index is not None:
        # Basic safeguard to prevent an out-of-range error
        if 0 <= index < len(quotes_list):
            return {"quote": quotes_list[index]}
        return {"error": "Index out of range. Please choose a number between 0 and 4."}
    
    return {"quote": random.choice(quotes_list)}


# ---------------------------------------------------------
# Mini-Project 2: Contact Form API
# ---------------------------------------------------------
class ContactMessage(BaseModel):
    name: str
    # Stretch Goal: Use EmailStr for automatic validation
    email: EmailStr 
    # Stretch Goal: Enforce a minimum length of 10 characters
    message: str = Field(..., min_length=10, description="Your message (min 10 characters)")
    # Optional field with a default value
    subject: str = Field(default="General Inquiry")


@app.post("/contact")
async def submission_route(contact: ContactMessage):
    """
    Accepts a structured JSON payload, validates it via Pydantic, 
    and returns a success message.
    """
    return {
        "status": "success",
        "info": f"Message received from {contact.name}.",
        # Returning the validated data to prove it worked
        "data_received": contact.model_dump() 
    }