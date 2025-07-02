# config.py
import os
from dotenv import load_dotenv

# Load from .env (only needed for local dev)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing from environment")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is missing from environment")

# # Optional debug output
# print(f"🔑 Loaded OpenAI key (first 5 chars): {OPENAI_API_KEY[:5]}...")

