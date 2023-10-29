import logging
import json
import os
import pymongo
import certifi

from fastapi import APIRouter, Form, HTTPException, Header
from typing import Annotated, Union

from ..settings.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

mongo_connection = Config.get_mongodb_connection


def process(data):
    pass


@router.post("/write_to_mongo",tags=["mongo_db"])
def write_to_mongo(email_id: Annotated[Union[str, None], Header()], data: str =Form(...)) -> str:
    """
    Writes data to mongo db
    :param email_id:
    :param data:
    :return:
    """
    # data = process(data)
    if len(data) != 50:
        raise HTTPException(status_code=400, detail="Data is not correct")
    else:
        try:
            client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
            db = client["mindful_ai"]
            collection = db["responses"]
            if email_id in collection.distinct("email_id"):
                collection.update_one({"email_id": email_id}, {"$set": {"data": data}})
            else:
                collection.insert_one({"email_id": email_id, "data": data})
            logger.info("Data written to mongo db")
            return (json.dumps({"status": "success"}))
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")

@router.post("/read_from_mongo",tags=["mongo_db"])
def read_from_mongo(email_id: Annotated[Union[str, None], Header()]) -> str:
    """
    Reads data from mongo db
    :param email_id:
    :return:
    """
    try:
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client["mindful_ai"]
        collection = db["responses"]
        data = collection.find_one({"email_id": email_id})
        logger.info("Data read from mongo db")
        return (json.dumps({"status": "success", "data": data["data"]}))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/update_mongo",tags=["mongo_db"])
def update_mongo(email_id: Annotated[Union[str, None], Header()], data: str =Form(...)) -> str:
    """
    Updates data in mongo db for the particular email id
    :param email_id:
    :param data:
    :return:
    """
    if len(data) != 50:
        raise HTTPException(status_code=400, detail="Data is not correct")
    else:
        try:
            client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
            db = client["mindful_ai"]
            collection = db["responses"]
            collection.update_one({"email_id": email_id}, {"$set": {"data": data}})
            logger.info("Data updated in mongo db")
            return (json.dumps({"status": "success"}))
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/delete_from_mongo",tags=["mongo_db"])
def delete_from_mongo(email_id: Annotated[Union[str, None], Header()]) -> str:
    """
    Deletes data from mongo db
    :param email_id:
    :return:
    """
    try:
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client["mindful_ai"]
        collection = db["responses"]
        collection.delete_one({"email_id": email_id})
        logger.info("Data deleted from mongo db")
        return (json.dumps({"status": "success"}))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/get_all_chat_for_email")
def get_chat(email_id: Annotated[Union[str, None], Header()]) -> str:
    """
    Gets all the chat for the email id
    :param email_id:
    :return:
    """
    try:
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client["mindful_ai"]
        collection = db["chats"]
        data = collection.find({"email_id": email_id})
        logger.info("Data read from mongo db")
        return (json.dumps({"status": "success", "data": data}))

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/get_emails")
def get_emails() -> str:
    """
    Gets all the emails
    :return:
    """
    try:
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client["mindful_ai"]
        collection = db["responses"]
        data = collection.distinct("email_id")
        logger.info("Data read from mongo db")
        return (json.dumps({"status": "success", "data": data}))

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/add_personal_information_by_email")
def personal_information_by_email(email_id: Annotated[Union[str, None], Header()], first_name: str =Form(...), last_name: str =Form(...),gender: str =Form(...), age: int =Form(...), marital_status: bool =Form(...), employment_status: bool =Form(...), education: bool =Form(...)) -> str:
    """
    post all the personal information by email
    :param email_id:
    :return:
    """
    try:
        data = {
            "email_id": email_id,
            "First Name": first_name,
            "Last Name": last_name,
            "Age": age,
            "Gender": gender,
            "Marital Status": marital_status,
            "Employment Status": employment_status,
            "Education": education,
        }
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client["mindful_ai"]
        collection = db["personal_information"]
        if email_id in collection.distinct("email_id"):
            collection.update_one({"email_id": email_id}, {"$set": data})
        else:

            collection.insert_one(data)
        logger.info("Data written to mongo db")
        return (json.dumps({"status": "success"}))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")


@router.post("/get_personal_information_by_email")
def get_personal_information_by_email(email_id: Annotated[Union[str, None], Header()]) -> str:
    """
    Gets all the personal information by email
    :param email_id:
    :return:
    """
    try:
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client["mindful_ai"]
        collection = db["personal_information"]
        data = collection.find_one({"email_id": email_id})
        logger.info("Data read from mongo db")
        return (json.dumps({"status": "success", "data": data}))

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")






