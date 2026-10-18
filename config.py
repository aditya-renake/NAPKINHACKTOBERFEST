"""Single place for model names and settings."""
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

PROVIDER = "gemini"
GEMINI_MODEL = "models/gemma-4-26b-a4b-it"

# Optional local Ollama fallback models
VISION_MODEL = "gemma3:4b"
CODE_MODEL = "qwen2.5-coder:7b"
TEMPERATURE = 0.2
MAX_IMAGE_SIDE = 1024
