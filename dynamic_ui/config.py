from dotenv import load_dotenv
import os

load_dotenv()

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "qwen/qwen3-235b-a22b-2507"
#MODEL_NAME = "google/gemini-2.5-flash-lite"
#MODEL_NAME = "openai/gpt-4.1"