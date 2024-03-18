import environ
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID
from utils import get_responses_from_llm, return_category_sentence
from models import TextModel, MessageUpdateRequest

app = FastAPI()

LLM_MODEL  = "gpt-3.5-turbo" # OR "gpt-4"
TEMPERATURE = 0 # LLM temperature

# OpenAI API key & client
env = environ.Env()
environ.Env.read_env()
OPENAI_API_KEY = env("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) # Initialize OpenAI client

messages: List[TextModel] = []

@app.get("/")
async def root():
    return {"message": "Welcome to D-AI-logue API!"}


@app.get("/api/messages/")
async def get_messages():
    return messages


# Classify and Transform text
@app.post("/api/messages/")
async def clf_transform_message(text_model: TextModel):
    try:
        clf_text, transformed_text, _ = get_responses_from_llm(
            user_text=text_model.original_text,
            api_client=client,
            llm_model=LLM_MODEL,
            temperature=TEMPERATURE
        )

        # Extract the sentences and the corresponding category from the original text
        # (done using the output from OpenAI API)
        sentences, categories = return_category_sentence(clf_text)

        text_model.raw_output = clf_text
        text_model.splitted_text = sentences
        text_model.communication_style = categories
        text_model.transformed_text = transformed_text # TODO: merge the text into a coherent paragraph

        messages.append(text_model)

        return {
            "id": text_model.id,
            "original_text": text_model.original_text,
            "raw_output": text_model.raw_output,
            "splitted_text": text_model.splitted_text,
            "communication_style": text_model.communication_style,
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
            if message_update.raw_output is not None:
                message.raw_output = message_update.raw_output
            if message_update.splitted_text is not None:
                message.splitted_text = message_update.splitted_text
            if message_update.communication_style is not None:
                message.communication_style = message_update.communication_style
            if message_update.transformed_text is not None:
                message.transformed_text = message_update.transformed_text
            return
    raise HTTPException(
        status_code=404,
        detail=f"message with id: {message_id} does not exist"
    )
