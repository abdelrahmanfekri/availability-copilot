from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Dict
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import ast
import openai
import os

from dotenv import load_dotenv
load_dotenv()

motor_client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
database = motor_client["availability_calendar"]

def get_database() -> AsyncIOMotorDatabase:
    return database


def get_completion(prompt, model="gpt-4-turbo", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

def get_object_id(tutor_id: str) -> ObjectId:
    return ObjectId(tutor_id)


def get_availability_list(content: str) -> list:
    prompt = """
    You are a calender co-pilot,
    Your task is extract availability from the text delimited by ####.
    The response should be a list of dictionaries with the keys "day" and "from" and "to"
    You should always understand the intend of the user and provide the availability in a structured format.
    Don't output anything else other than the list of dictionaries.
    Example [{"day": "Monday", "from": "7pm", "to": "8pm"}, {"day": "Monday", "from": "1pm", "to": "3pm"}]
    the day should always be day of the week
    Ex: Friday, Monday, Tuesday, Wednesday, Thursday, Saturday, Sunday
    from: should always be in 12 hour format
    to: should always be in 12 hour format

    the weekends is Friday, Saturday.
    Example:
    Availability Input: I am available between 1pm and 4pm on weekends, after 7 pm to midnight on
    Monday and Wednesday, and after 9pm otherwise

    output:
    [{"day": "Friday", "from": "1pm", "to": "4pm"}, {"day": "Saturday", "from": "1pm", "to": "4pm"}, {"day": "Monday", "from": "7pm", "to": "12am"}, {"day": "Wednesday", "from": "7pm", "to": "12am"}, {"day": "Tuesday", "from": "9pm", "to": "12am"}, {"day": "Thursday", "from": "9pm", "to": "12am"}, {"day": "Sunday", "from": "9pm", "to": "12am"}]

    Availability Input: ####
    """ + content + "####"
    respond = get_completion(prompt)
    try:
        lst_respond = ast.literal_eval(respond)
        if not isinstance(lst_respond, list):
            raise ValueError("Can't parse the availability")
        return lst_respond
    except Exception as e:
        raise ValueError("Can't parse the availability")
            
        
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TutorRequest(BaseModel):
    username: str

@app.post("/create-tutor")
async def create_tutor(tutor: TutorRequest, database: AsyncIOMotorDatabase = Depends(get_database)):
    username = tutor.username
    tutor = await database["tutors_profile"].insert_one({"username": username, "availability": []})
    return {"id": str(tutor.inserted_id), "username": username , "availability": []}

class AvailabilityRequest(BaseModel):
    content: str

@app.post("/availability", response_model=List[Dict[str,str]])
async def availability(request: AvailabilityRequest):
    try:
        return get_availability_list(request.content)
    except Exception as e:
        return {"error": str(e)}

class AvailabilityRequest(BaseModel):
    availability: List[Dict[str,str]] = []

@app.post("/save/{tutor_id}")
async def save_availability(availability: AvailabilityRequest, tutor_id: ObjectId = Depends(get_object_id), database: AsyncIOMotorDatabase = Depends(get_database)):
    await database["tutors_profile"].update_one({"_id": tutor_id}, {"$set":{"availability": availability.availability}})
    print(availability.availability)
    return {"message": "Availability saved successfully"}

@app.get("/get/{tutor_id}")
async def get_availability(tutor_id: ObjectId = Depends(get_object_id) , database: AsyncIOMotorDatabase = Depends(get_database)):
    availability = await database["tutors_profile"].find_one({"_id": tutor_id})
    return {"availability": availability["availability"]}

