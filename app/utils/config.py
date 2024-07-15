import environ
import os

# Initialize environment variables
env = environ.Env()


# Check for the presence of an environment variable first, then read .env file for local development
if os.getenv("OPENAI_API_KEY"):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
else:
    # Initialize environment variables
    environ.Env.read_env('.env')
    OPENAI_API_KEY = env("OPENAI_API_KEY")
