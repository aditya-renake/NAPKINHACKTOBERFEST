"""Single place for model names and settings. Verify tags with `ollama list`."""

VISION_MODEL = "gemma3:4b"          # multimodal; swap for a Gemma 4 vision tag if available
CODE_MODEL = "qwen2.5-coder:7b"     # use qwen2.5-coder:3b on slow laptops
TEMPERATURE = 0.2
MAX_IMAGE_SIDE = 1024
