import environ

# Initialize environment variables
env = environ.Env()
# Read .env file
environ.Env.read_env('.env')

# Access the OpenAI API key
OPENAI_API_KEY = env("OPENAI_API_KEY")
