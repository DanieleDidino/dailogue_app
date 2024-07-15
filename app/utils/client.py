import environ
from openai import OpenAI

from utils.config import OPENAI_API_KEY


def initialize_openai_client():
    # OpenAI API key
    api_key = OPENAI_API_KEY

    if not api_key:
        raise ValueError(
            "No API key found. Please set a OPENAI_API_KEY in the .env file."
        )

    return OpenAI(api_key=api_key)
