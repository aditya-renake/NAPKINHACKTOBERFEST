"""Stage 1: vision model. Reads images, outputs text/JSON only."""
import json
import ollama
import config
from engine import prompts


def _clean_json_str(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def sketch_to_spec(image_bytes: bytes) -> dict:
    """Return the UI spec dict. Raise RuntimeError on failure or invalid JSON."""
    try:
        resp = ollama.chat(
            model=config.VISION_MODEL,
            messages=[{"role": "user", "content": prompts.SPEC_PROMPT, "images": [image_bytes]}],
            format="json",
            options={"temperature": config.TEMPERATURE},
        )
        content = resp["message"]["content"]
        spec = json.loads(_clean_json_str(content))
        if not isinstance(spec, dict):
            raise ValueError("Expected JSON object for spec")
        return spec
    except Exception as e:
        raise RuntimeError(f"Failed to generate UI spec from sketch: {e}") from e


def extract_annotations(image_bytes: bytes) -> str:
    """Return handwritten edit instructions as text, or '' if NONE."""
    try:
        resp = ollama.chat(
            model=config.VISION_MODEL,
            messages=[{"role": "user", "content": prompts.ANNOTATION_PROMPT, "images": [image_bytes]}],
            options={"temperature": config.TEMPERATURE},
        )
        content = resp["message"]["content"].strip()
        if content.upper() == "NONE" or not content:
            return ""
        return content
    except Exception as e:
        raise RuntimeError(f"Failed to extract annotations from sketch: {e}") from e
