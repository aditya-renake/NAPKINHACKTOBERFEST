"""
Napkin2Code - Vision AI Engine
Communicates with Ollama local vision models (Gemma 4, Moondream, Llama 3.2 Vision),
handles image inputs, parses output code, and provides a mock/demo fallback.
"""

import json
import re
import time
import requests
from typing import Optional, Dict, Any, List, Tuple
from PIL import Image
import ollama

from core.image_processing import image_to_base64, image_to_bytes
from engine.prompts import (
    INITIAL_SYSTEM_PROMPT,
    build_initial_prompt,
    build_iterative_prompt,
)

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_VISION_MODELS = [
    "gemma4:e2b",
    "gemma4:e4b",
    "gemma4:latest",
    "moondream",
    "llama3.2-vision:11b",
    "llama3.2-vision",
    "llava",
    "bakllava",
]


def check_ollama_status(base_url: str = OLLAMA_BASE_URL) -> Dict[str, Any]:
    """Check if the local Ollama daemon is reachable and list downloaded models."""
    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=2.0)
        if resp.status_code == 200:
            models_data = resp.json().get("models", [])
            model_names = [m.get("name", "") for m in models_data]
            return {
                "online": True,
                "models": model_names,
                "message": f"Connected to Ollama ({len(model_names)} models found)"
            }
        return {"online": False, "models": [], "message": f"Ollama returned HTTP {resp.status_code}"}
    except Exception as e:
        return {"online": False, "models": [], "message": f"Ollama not running: {str(e)}"}



def clean_extracted_html(raw_response: str) -> str:
    """Extract and sanitize raw HTML code from LLM output."""
    text = raw_response.strip()

    # Case 1: Markdown code block ```html ... ```
    match = re.search(r"```(?:html)?\s*(<!DOCTYPE[\s\S]*?</html>)\s*```", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Case 2: Any code block ``` ... ```
    match = re.search(r"```(?:html)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        candidate = match.group(1).strip()
        if "<!DOCTYPE" in candidate.upper() or "<html" in candidate.lower():
            return candidate

    # Case 3: Raw HTML starting with <!DOCTYPE and ending with </html>
    match = re.search(r"(<!DOCTYPE[\s\S]*?</html>)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Case 4: Raw HTML starting with <html and ending with </html>
    match = re.search(r"(<html[\s\S]*?</html>)", text, re.IGNORECASE)
    if match:
        return "<!DOCTYPE html>\n" + match.group(1).strip()

    # Case 5: Partial HTML: if it contains tags, wrap in standard boilerplate
    if "<body" in text or "<div" in text:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Napkin2Code App</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-50 min-h-screen text-slate-800 p-6 flex flex-col items-center justify-center font-sans">
{text}
<script>
  if (window.lucide) {{ lucide.createIcons(); }}
</script>
</body>
</html>"""

    # If completely empty or non-HTML, return fallback
    return get_fallback_html("Could not generate valid HTML from sketch. Please try again with clear pen strokes.")


def get_fallback_html(message: str = "Demo Sketch Output") -> str:
    """Return a polished fallback interactive mockup for offline demo testing."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Napkin2Code - Live Application</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    @keyframes pulse-subtle {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.02); }} }}
    .btn-hover:hover {{ transform: translateY(-1px); }}
  </style>
</head>
<body class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 min-h-screen text-slate-100 p-6 flex flex-col items-center justify-center font-sans">
  <div class="max-w-md w-full bg-slate-800/90 border border-slate-700/60 rounded-2xl p-6 shadow-2xl backdrop-blur-xl transition-all">
    <!-- Header -->
    <div class="flex items-center justify-between pb-4 border-b border-slate-700">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center border border-indigo-500/30">
          <i data-lucide="sparkles" class="w-5 h-5"></i>
        </div>
        <div>
          <h2 class="font-bold text-lg text-white">Napkin2Code App</h2>
          <p class="text-xs text-indigo-400 font-medium">✨ Generated from Physical Sketch</p>
        </div>
      </div>
      <button id="themeToggle" class="p-2 rounded-lg bg-slate-700/50 hover:bg-slate-700 text-slate-300 transition">
        <i data-lucide="moon" class="w-4 h-4"></i>
      </button>
    </div>

    <!-- Product / Card Body -->
    <div class="mt-6 space-y-4">
      <div class="w-full h-44 rounded-xl bg-gradient-to-tr from-indigo-500/30 to-purple-500/20 border border-indigo-500/20 flex flex-col items-center justify-center p-4 text-center">
        <i data-lucide="image" class="w-10 h-10 text-indigo-300 mb-2"></i>
        <span class="text-sm font-semibold text-slate-200">Hand-Drawn Sketch Layout</span>
        <span class="text-xs text-slate-400 mt-1 max-w-xs">{message}</span>
      </div>

      <div class="flex items-center justify-between pt-1">
        <div>
          <h3 class="font-bold text-white text-base">Interactive Product Item</h3>
          <p class="text-xs text-slate-400">100% Local Vision AI Compilation</p>
        </div>
        <span class="text-indigo-400 font-bold text-lg">$24.00</span>
      </div>

      <!-- Rating Demo -->
      <div class="flex items-center space-x-1 text-amber-400" id="starRating">
        <i data-lucide="star" class="w-4 h-4 fill-amber-400"></i>
        <i data-lucide="star" class="w-4 h-4 fill-amber-400"></i>
        <i data-lucide="star" class="w-4 h-4 fill-amber-400"></i>
        <i data-lucide="star" class="w-4 h-4 fill-amber-400"></i>
        <i data-lucide="star" class="w-4 h-4 text-slate-600"></i>
        <span class="text-xs text-slate-400 ml-2">(4.8 / 5.0)</span>
      </div>

      <!-- Interactive Counter -->
      <div class="flex items-center justify-between bg-slate-900/60 p-3 rounded-xl border border-slate-700/40">
        <span class="text-xs font-medium text-slate-300">Quantity</span>
        <div class="flex items-center space-x-3">
          <button id="qtyMinus" class="w-7 h-7 rounded-lg bg-slate-800 text-slate-200 hover:bg-slate-700 flex items-center justify-center font-bold text-sm">-</button>
          <span id="qtyVal" class="text-sm font-bold text-white px-1">1</span>
          <button id="qtyPlus" class="w-7 h-7 rounded-lg bg-slate-800 text-slate-200 hover:bg-slate-700 flex items-center justify-center font-bold text-sm">+</button>
        </div>
      </div>

      <!-- Action Button -->
      <button id="checkoutBtn" class="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-medium rounded-xl shadow-lg shadow-indigo-600/30 transition btn-hover flex items-center justify-center space-x-2">
        <i data-lucide="shopping-cart" class="w-4 h-4"></i>
        <span>Purchase Now</span>
      </button>

      <div id="toast" class="hidden text-xs text-emerald-400 bg-emerald-950/50 border border-emerald-800/60 p-2.5 rounded-lg text-center transition">
        🎉 Item added to cart! Hand-drawn UI is live.
      </div>
    </div>
  </div>

  <script>
    // Initialize Lucide Icons
    if (window.lucide) {{ lucide.createIcons(); }}

    // Quantity Counter Logic
    let qty = 1;
    const qtyVal = document.getElementById('qtyVal');
    document.getElementById('qtyPlus')?.addEventListener('click', () => {{
      qty++;
      qtyVal.textContent = qty;
    }});
    document.getElementById('qtyMinus')?.addEventListener('click', () => {{
      if (qty > 1) {{ qty--; qtyVal.textContent = qty; }}
    }});

    // Checkout Notification
    document.getElementById('checkoutBtn')?.addEventListener('click', () => {{
      const toast = document.getElementById('toast');
      toast.classList.remove('hidden');
      setTimeout(() => toast.classList.add('hidden'), 3000);
    }});
  </script>
</body>
</html>"""


def resolve_vision_model(requested_model: str, available_models: List[str]) -> Tuple[str, bool, Optional[str]]:
    """
    Match requested model against available Ollama models.
    Returns: (model_to_use, is_exact_match, notice_message)
    """
    if not available_models:
        return requested_model, False, None

    # Exact match
    if requested_model in available_models:
        return requested_model, True, None

    # Prefix/tag match (e.g. 'moondream' -> 'moondream:latest')
    for m in available_models:
        base = m.split(":")[0]
        if requested_model.lower() == base.lower():
            return m, True, None

    # Substring match
    for m in available_models:
        if requested_model.lower() in m.lower():
            return m, True, None

    # Fallback to an available vision model in Ollama if requested model is not downloaded
    preferred = ["gemma4", "moondream", "llama3.2-vision", "llava", "qwen"]
    for pref in preferred:
        for m in available_models:
            if pref in m.lower():
                notice = f"Model '{requested_model}' not found in Ollama. Using installed '{m}'."
                return m, False, notice

    # Fallback to first available model
    notice = f"Model '{requested_model}' not found in Ollama. Using installed '{available_models[0]}'."
    return available_models[0], False, notice


def generate_code_from_sketch(
    image: Image.Image,
    model_name: str = "moondream",
    user_guidance: str = "",
    base_url: str = OLLAMA_BASE_URL,
    mock_fallback: bool = True,
) -> Dict[str, Any]:
    """
    Generate initial HTML code from a hand-drawn paper sketch.
    Returns dict with status, html_code, elapsed_time, and model used.
    """
    start_time = time.time()
    b64_image = image_to_base64(image)
    prompt = build_initial_prompt(user_guidance)

    # Check if Ollama is accessible
    status = check_ollama_status(base_url)
    available_models = status.get("models", [])

    if not status["online"] and mock_fallback:
        elapsed = time.time() - start_time
        return {
            "success": True,
            "mock": True,
            "html": get_fallback_html("Demo Mode: Ollama offline. Showing live mock preview."),
            "model": f"{model_name} (Mock Fallback)",
            "elapsed_seconds": round(elapsed, 2),
            "message": "Generated using Demo Mode (Ollama offline). Start Ollama for real vision inference."
        }

    actual_model, is_exact, notice = resolve_vision_model(model_name, available_models)

    try:
        client = ollama.Client(host=base_url)
        response = client.chat(
            model=actual_model,
            messages=[
                {"role": "system", "content": INITIAL_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompt,
                    "images": [b64_image],
                },
            ],
            options={"temperature": 0.2},
        )
        raw_text = response.get("message", {}).get("content", "")
        cleaned_html = clean_extracted_html(raw_text)
        elapsed = time.time() - start_time

        display_model = actual_model if is_exact else f"{actual_model} (auto-fallback from {model_name})"
        msg = "HTML successfully compiled from sketch!"
        if notice:
            msg = f"{notice} HTML compiled!"

        return {
            "success": True,
            "mock": False,
            "html": cleaned_html,
            "raw_text": raw_text,
            "model": display_model,
            "elapsed_seconds": round(elapsed, 2),
            "message": msg
        }
    except Exception as e:
        elapsed = time.time() - start_time
        err_msg = str(e)
        if "not found" in err_msg.lower() or "404" in err_msg:
            hint = f"Model '{actual_model}' not found in Ollama. Run: `ollama pull {actual_model}`"
        else:
            hint = err_msg

        if mock_fallback:
            return {
                "success": True,
                "mock": True,
                "html": get_fallback_html(f"Fallback active: {hint}"),
                "model": f"{model_name} (Fallback)",
                "elapsed_seconds": round(elapsed, 2),
                "message": f"Ollama error: {hint}. Rendered fallback preview."
            }
        return {
            "success": False,
            "mock": False,
            "html": "",
            "error": hint,
            "elapsed_seconds": round(elapsed, 2),
            "message": f"Vision AI failed: {hint}"
        }


def iterate_code_from_sketch(
    new_annotated_image: Image.Image,
    current_html: str,
    user_notes: str = "",
    model_name: str = "moondream",
    base_url: str = OLLAMA_BASE_URL,
    mock_fallback: bool = True,
) -> Dict[str, Any]:
    """
    Perform physical iterative editing: merge handwritten updates from new sketch into current HTML.
    """
    start_time = time.time()
    b64_image = image_to_base64(new_annotated_image)
    prompt = build_iterative_prompt(current_html=current_html, user_notes=user_notes)

    status = check_ollama_status(base_url)
    available_models = status.get("models", [])

    if not status["online"] and mock_fallback:
        elapsed = time.time() - start_time
        # Mock modification: add a dark mode badge & reviews into current HTML
        modified_html = current_html
        if "Physical Revision" not in modified_html:
            modified_html = modified_html.replace(
                "<!-- Product / Card Body -->",
                """<!-- Physical Revision: Injected Dark Mode & Verified Badge -->
    <div class="mb-3 px-3 py-1.5 rounded-lg bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-xs flex items-center justify-between">
      <span>✏️ Physical Iteration Applied</span>
      <span class="font-bold">v2.0 Revision</span>
    </div>
    <!-- Product / Card Body -->"""
            )
        return {
            "success": True,
            "mock": True,
            "html": modified_html,
            "model": f"{model_name} (Mock Revision)",
            "elapsed_seconds": round(elapsed, 2),
            "message": "Physical scribbles applied via Demo Mode! (Ollama offline)"
        }

    actual_model, is_exact, notice = resolve_vision_model(model_name, available_models)

    try:
        client = ollama.Client(host=base_url)
        response = client.chat(
            model=actual_model,
            messages=[
                {"role": "system", "content": INITIAL_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompt,
                    "images": [b64_image],
                },
            ],
            options={"temperature": 0.2},
        )
        raw_text = response.get("message", {}).get("content", "")
        cleaned_html = clean_extracted_html(raw_text)
        elapsed = time.time() - start_time

        display_model = actual_model if is_exact else f"{actual_model} (auto-fallback from {model_name})"
        msg = "Physical handwritten revisions successfully merged into code!"
        if notice:
            msg = f"{notice} Revisions merged!"

        return {
            "success": True,
            "mock": False,
            "html": cleaned_html,
            "raw_text": raw_text,
            "model": display_model,
            "elapsed_seconds": round(elapsed, 2),
            "message": msg
        }
    except Exception as e:
        elapsed = time.time() - start_time
        err_msg = str(e)
        if "not found" in err_msg.lower() or "404" in err_msg:
            hint = f"Model '{actual_model}' not found in Ollama. Run: `ollama pull {actual_model}`"
        else:
            hint = err_msg

        if mock_fallback:
            return {
                "success": True,
                "mock": True,
                "html": current_html,
                "model": f"{model_name} (Fallback)",
                "elapsed_seconds": round(elapsed, 2),
                "message": f"Ollama error: {hint}"
            }
        return {
            "success": False,
            "mock": False,
            "html": "",
            "error": hint,
            "elapsed_seconds": round(elapsed, 2),
            "message": f"Iterative edit failed: {hint}"
        }


# --- Multi-Stage Pipeline Helpers (Spec & Annotation Extraction) ---

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
        import config
        from engine import prompts
        vision_model = getattr(config, "VISION_MODEL", "moondream")
        temperature = getattr(config, "TEMPERATURE", 0.2)
        resp = ollama.chat(
            model=vision_model,
            messages=[{"role": "user", "content": prompts.SPEC_PROMPT, "images": [image_bytes]}],
            format="json",
            options={"temperature": temperature},
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
        import config
        from engine import prompts
        vision_model = getattr(config, "VISION_MODEL", "moondream")
        temperature = getattr(config, "TEMPERATURE", 0.2)
        resp = ollama.chat(
            model=vision_model,
            messages=[{"role": "user", "content": prompts.ANNOTATION_PROMPT, "images": [image_bytes]}],
            options={"temperature": temperature},
        )
        content = resp["message"]["content"].strip()
        if content.upper() == "NONE" or not content:
            return ""
        return content
    except Exception as e:
        raise RuntimeError(f"Failed to extract annotations from sketch: {e}") from e

