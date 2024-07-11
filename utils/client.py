import environ
from openai import OpenAI


def initialize_openai_client():
    # OpenAI API key
    env = environ.Env()
    environ.Env.read_env()
    api_key = env("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "No API key found. Please set a OPENAI_API_KEY in the .env file."
        )

    return OpenAI(api_key=api_key)
