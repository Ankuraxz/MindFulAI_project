import logging
import json
import os
import requests
import joblib
import pandas as pd
import pymongo
import certifi

from fastapi import APIRouter, Form, HTTPException, Header
from typing import Optional, Annotated, Union

from ..settings.config import Config

from langchain.prompts import PromptTemplate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
model = joblib.load(open('data/modelnew.pkl', 'rb'))


openai_llm_chat = Config.get_openai_chat_connection
mongo_connection = Config.get_mongodb_connection

def predict(data : str) -> int:
    """
    Predicts based on data responses typeform
    :param data in stringformat:
    :return:
    """

    if len(data) != 50:
        raise HTTPException(status_code=400, detail="Data is not correct")
    else:
        dfx = []
        for ix in data:
            dfx.append(int(ix))
        print(dfx)
        df = pd.DataFrame(dfx)
        df = df.T
        return (model.predict(df)[0])


def interpret_prediction(prediction: int) -> str:
    """
    Interprets prediction
    :param prediction:
    :return:
    """
    if prediction == 0:
        return (json.dumps({
            "Conscientiousness": "High",
            "Openness to Experience": "High",
            "Agreeableness": "High",
            "Emotional Stability": "Low",
            "Extraversion": "Neutral"
        }))

    elif prediction == 1:
        return (json.dumps({
            "Conscientiousness": "Low",
            "Openness to Experience": "Low",
            "Agreeableness": "Low",
            "Emotional Stability": "High",
            "Extraversion": "Low"
        }))

    elif prediction == 2:
        return (json.dumps({
            "Conscientiousness": "High",
            "Openness to Experience": "Low",
            "Agreeableness": "Neutral",
            "Emotional Stability": "Low",
            "Extraversion": "Low"
        }))

    elif prediction == 3:
        return (json.dumps({
            "Conscientiousness": "Neutral",
            "Openness to Experience": "High",
            "Agreeableness": "Low",
            "Emotional Stability": "High",
            "Extraversion": "High"
        }))

    elif prediction == 4:
        return (json.dumps({
            "Conscientiousness": "High",
            "Openness to Experience": "Neutral",
            "Agreeableness": "High",
            "Emotional Stability": "Low",
            "Extraversion": "High"
        }))

def get_data_from_mongo(email_id: str) -> str:
    """
    Gets data from mongo db
    :param email_id:
    :return:
    """
    try:
        logger.info(f"Connecting to MongoDB")
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client['mindful_ai']
        collection = db['responses']
        data = collection.find_one({"email_id": email_id})
        # print(data)
        return str(data['data'])
    except Exception as e:
        logger.error(f"An Exception Occurred while connecting to MongoDB --> {e}")
        raise Exception(f"An Exception Occurred while connecting to MongoDB --> {e}")


def get_personal_information_by_email(email_id: str) -> str:
    """
    Gets personal information by email id
    :param email_id:
    :return:
    """
    try:
        logger.info(f"Connecting to MongoDB")
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client['mindful_ai']
        collection = db["personal_information"]
        data = collection.find_one({"email_id": email_id})
        del data["_id"]
        return json.dumps(data)

    except Exception as e:
        logger.error(f"An Exception Occurred while connecting to MongoDB --> {e}")
        raise Exception(f"An Exception Occurred while connecting to MongoDB --> {e}")

def save_chat(email_id: str, history: str, inference: str) -> str:
    """
    Saves chat to MongoDB
    :param email_id:
    :param history:
    :param inference:
    :return:
    """
    try:
        logger.info(f"Connecting to MongoDB")
        client = pymongo.MongoClient(os.environ.get('MONGO_URI'),ssl=True,tlsCAFile=certifi.where())
        db = client['mindful_ai']
        collection = db['chats']
        collection.insert_one({"email_id": email_id, "history": history, "inference": inference})
        return (json.dumps({"status": "success"}))
    except Exception as e:
        logger.error(f"An Exception Occurred while connecting to MongoDB --> {e}")
        raise Exception(f"An Exception Occurred while connecting to MongoDB --> {e}")






@router.post("/chat",tags=["ai"])
async def chat(email_id: Annotated[Union[str, None], Header()], message: str = Form(...), history: list = Form(...)):
    """
    Chat with the AI to know about personality
    :header: user_email
    :param: message
    :param: history
    :return: message, reply
    """

    if history is None:
        history = []

    data = get_data_from_mongo(email_id)
    if data is None:
        return {"response": "No data found for this email id", "history": history, "stop": True}
    prediction = predict(data)
    if prediction is None:
        return {"response": "No data found for this email id", "history": history, "stop": True}
    inference = interpret_prediction(prediction)

    personal_info = get_personal_information_by_email(email_id)
    if personal_info is None:
        personal_info= "No personal information found for this email id"

    if "STOP" in message or "Stop" in message or "stop" in message:
        save_chat(email_id, json.dumps(history), inference)
        return {"response": "STOPPING CHAT ", "history": history, "stop": True}


    template = """
    CONTEXT: You are an AI-based Mental Health Chatbot. You will be provided a personality report containing personality traits like Conscientiousness, Openness to Experience, Agreeableness, Emotional Stability, Extraversion. A user with personal information {personal_info} will be chatting with you to know more about their personality, and may ask related questions. Politely answer them. Here is the history of chat {history}, now the customer is saying {message}. Please respond to the customer in a polite manner. In case there is no history of chat, just respond to the customer's current message.
    Personality Report: {inference}
    TASK: Based on the personality report, answer the user's questions politely and explain their personality briefly if asked. You can also ask the user questions if you need more information about their personality.
    ANSWER: Respond in a few lines and be polite. If you don't know the answer, you can say "I don't know." If you want to stop the chat, you can say "STOP."
    SUB_TASKS: Help the user learn more about their personality, answer their questions, address their doubts as a friend, and provide information about their mental well-being. Offer support and guidance for improving mental health.
    RESPONSE CONSTRAINT: DO NOT OUTPUT HISTORY OF CHAT, JUST OUTPUT RESPONSE TO THE CUSTOMER IN CONCISE WAY, PREFERABLY BULLET POINTS.

    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | openai_llm_chat

    response = chain.invoke({"personal_info":personal_info,"history": json.dumps(history), "inference": inference, "message": message})

    if "STOP" in response or "Stop" in response or "stop" in response or "STOPPING CHAT" in response or "Stopping Chat" in response or "stopping chat" in response:
        return {"response": response, "history": history, "stop": True}
    else:
        history.append({"message":message,"response":response})
        return {"response": response, "history": history, "stop": False}








