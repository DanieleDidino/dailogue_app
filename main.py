# import environ
# from openai import OpenAI
from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID
from pathlib import Path

from utils.client import initialize_openai_client
from utils.openai_config import OpenAIModels
from utils.models import TextModel, MessageUpdateRequest
from utils.prompts import create_dynamic_prompt
from utils.request_handler import handle_request


app = FastAPI()

# OpenAI API key & client
#env = environ.Env()
#environ.Env.read_env()
#OPENAI_API_KEY = env("OPENAI_API_KEY")
#client = OpenAI(api_key=OPENAI_API_KEY) # Initialize OpenAI client
client = initialize_openai_client()

# LLM_MODEL  = "gpt-3.5-turbo" # OR "gpt-4"
# TEMPERATURE = 0 # LLM temperature
# EMB_MODEL = "text-embedding-3-small" # Embedding model
LLM_MODEL  = OpenAIModels.GPT3_TURBO
TEMPERATURE = 0 # LLM temperature
EMB_MODEL = OpenAIModels.TEXT_EMB_3_SMALL # Embedding model

# Path to embedding database
FOLDER = "./data_synthetic" # folder wiht generated synthetic data
PATH_EMB_DB = Path(FOLDER, "embeddings.db")

# Number of example to use as few-shots in the prompt
NUM_EXAMPLES_TO_SELECT = 5

# Initializes "messages", i.e., an empty list used to store instances of TextModel
messages: List[TextModel] = []

@app.get("/")
async def root():
    return {"message": "Welcome to D-AI-logue API!"}


@app.get("/api/messages/")
async def get_messages():
    return messages


# Transform text
@app.post("/api/messages/", response_model=TextModel)
async def transform_message(text_model: TextModel):
    try:
        # Generate prompt
        prompt = create_dynamic_prompt(
            user_text=text_model.original_text,
            path_emb=PATH_EMB_DB,
            emb_model=EMB_MODEL,
            client=client,
            num_examples=NUM_EXAMPLES_TO_SELECT)
        text_model.prompt = prompt

        # Generate tranformed text using LLM from OpenAI API
        transformed_text, _ = handle_request(
            prompt=text_model.prompt,
            client=client,
            model=LLM_MODEL,
            temperature=TEMPERATURE
        )
        text_model.transformed_text = transformed_text

        messages.append(text_model)

        return {
            "id": text_model.id,
            "original_text": text_model.original_text,
            "prompt": text_model.prompt,
            "transformed_text": text_model.transformed_text,
            }
    
    # If something goes wrong, return a 500 error and a message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/messages/{message_id}")
async def delete_message(message_id: UUID):
    for message in messages:
        if message.id == message_id:
            messages.remove(message)
            return
    raise HTTPException(
        status_code=404,
        detail=f"message with id: {message_id} does not exist"
    )


@app.put("/api/messages/{message_id}")
async def update_message(message_update: MessageUpdateRequest, message_id: UUID):
    for message in messages:
        if message.id == message_id:
            if message_update.original_text is not None:
                message.original_text = message_update.original_text
            if message_update.prompt is not None:
                message.prompt = message_update.prompt
            if message_update.transformed_text is not None:
                message.transformed_text = message_update.transformed_text
            return
    raise HTTPException(
        status_code=404,
        detail=f"message with id: {message_id} does not exist"
    )
