"""LLM abstraction routing between Gemini API (Gemma 4) and local Ollama."""
import time
import config

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

try:
    import ollama
except ImportError:
    ollama = None


def _get_gemini_client():
    if genai is None:
        raise RuntimeError("google-genai package is not installed.")
    return genai.Client()


def generate_text(prompt: str, system: str | None = None) -> str:
    """Generate text completion from prompt and optional system instructions."""
    full_prompt = f"{system}\n\n{prompt}".strip() if system else prompt.strip()

    if config.PROVIDER == "gemini":
        last_err = None
        for attempt in range(2):
            try:
                client = _get_gemini_client()
                try:
                    cfg = types.GenerateContentConfig(temperature=config.TEMPERATURE)
                except Exception:
                    cfg = None
                res = client.models.generate_content(
                    model=config.GEMINI_MODEL,
                    contents=full_prompt,
                    config=cfg,
                )
                if not res.text:
                    raise RuntimeError("Gemini returned an empty response.")
                return res.text
            except Exception as e:
                last_err = e
                if attempt == 0:
                    time.sleep(1)
        raise RuntimeError(f"Gemini text generation failed: {type(last_err).__name__} - {str(last_err)}")

    elif config.PROVIDER == "ollama":
        if ollama is None:
            raise RuntimeError("ollama package is not installed.")
        try:
            resp = ollama.chat(
                model=config.CODE_MODEL,
                messages=[{"role": "user", "content": full_prompt}],
                options={"temperature": config.TEMPERATURE},
            )
            return resp["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Ollama text generation failed: {e}") from e

    else:
        raise RuntimeError(f"Unknown PROVIDER: {config.PROVIDER}")


def generate_vision(prompt: str, image_bytes: bytes) -> str:
    """Generate response from multimodal model given image bytes and prompt."""
    if config.PROVIDER == "gemini":
        last_err = None
        for attempt in range(2):
            try:
                client = _get_gemini_client()
                try:
                    cfg = types.GenerateContentConfig(temperature=config.TEMPERATURE)
                except Exception:
                    cfg = None
                mime_type = "image/png" if image_bytes.startswith(b"\x89PNG") else "image/jpeg"
                contents = [
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    prompt,
                ]
                res = client.models.generate_content(
                    model=config.GEMINI_MODEL,
                    contents=contents,
                    config=cfg,
                )
                if not res.text:
                    raise RuntimeError("Gemini vision returned an empty response.")
                return res.text
            except Exception as e:
                last_err = e
                if attempt == 0:
                    time.sleep(1)
        raise RuntimeError(f"Gemini vision generation failed: {type(last_err).__name__} - {str(last_err)}")

    elif config.PROVIDER == "ollama":
        if ollama is None:
            raise RuntimeError("ollama package is not installed.")
        try:
            resp = ollama.chat(
                model=config.VISION_MODEL,
                messages=[{"role": "user", "content": prompt, "images": [image_bytes]}],
                options={"temperature": config.TEMPERATURE},
            )
            return resp["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Ollama vision generation failed: {e}") from e

    else:
        raise RuntimeError(f"Unknown PROVIDER: {config.PROVIDER}")
