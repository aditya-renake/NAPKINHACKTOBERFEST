"""Local Open-Weight Vision Model Engine for Napkin2Code.

Interfaces with Ollama running locally on the user's machine to perform
multimodal sketch-to-code generation and physical-annotation iterative updates.
"""

import re
import requests
from typing import Optional, Dict, Any, Tuple
from PIL import Image

from core.image_processor import image_to_base64
from engine.prompts import (
    INITIAL_SKETCH_SYSTEM_PROMPT,
    INITIAL_SKETCH_USER_PROMPT,
    ITERATIVE_EDIT_SYSTEM_PROMPT,
    build_iterative_user_prompt,
)

DEFAULT_OLLAMA_HOST = "http://localhost:11434"
SUPPORTED_MODELS = [
    "moondream",
    "llama3.2-vision:11b",
    "llama3.2-vision:latest",
    "llava:7b",
    "llava:latest",
    "qwen2-vl:7b",
]


def check_ollama_status(host: str = DEFAULT_OLLAMA_HOST) -> Tuple[bool, list[str]]:
    """Check if local Ollama daemon is running and list available models."""
    try:
        resp = requests.get(f"{host}/api/tags", timeout=1.5)
        if resp.status_code == 200:
            models_data = resp.json().get("models", [])
            model_names = [m.get("name", "") for m in models_data]
            return True, model_names
        return False, []
    except Exception:
        return False, []


def extract_html_code(raw_text: str) -> str:
    """Extract clean HTML code block from LLM output."""
    # Look for ```html ... ``` block
    pattern = r"```(?:html)?\s*(<!DOCTYPE html[\s\S]*?|<html[\s\S]*?)```"
    match = re.search(pattern, raw_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Fallback to general ``` codeblock
    code_pattern = r"```(?:html)?\s*([\s\S]*?)```"
    match = re.search(code_pattern, raw_text)
    if match:
        extracted = match.group(1).strip()
        if "<html" in extracted.lower() or "<div" in extracted.lower():
            return extracted

    # If raw text contains HTML tags directly
    if "<html" in raw_text.lower() or "<!doctype html" in raw_text.lower():
        return raw_text.strip()

    # Wrap bare HTML snippet into full HTML template
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Napkin2Code Prototype</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 flex items-center justify-center min-h-screen p-4">
  <div class="max-w-2xl w-full">
    {raw_text}
  </div>
</body>
</html>"""


def get_demo_fallback_code(is_annotated: bool = False) -> str:
    """Provides high-fidelity pre-compiled demo code if Ollama is not active."""
    if not is_annotated:
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Launch Card - Napkin2Code</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-100 flex items-center justify-center min-h-screen p-6 font-sans">
  <div class="bg-white rounded-2xl shadow-xl border border-slate-200 max-w-md w-full overflow-hidden hover:shadow-2xl transition duration-300">
    <div class="p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Product Launch Card</h2>
        <span class="px-3 py-1 text-xs font-semibold bg-blue-100 text-blue-700 rounded-full">New Release</span>
      </div>

      <!-- Image Area -->
      <div class="bg-gradient-to-tr from-blue-600 to-indigo-700 rounded-xl h-52 flex flex-col items-center justify-center text-white p-4 shadow-inner">
        <i class="fa-solid fa-microchip text-5xl mb-2 opacity-90"></i>
        <span class="text-sm font-medium tracking-wide">Next-Gen Hardware Edition</span>
      </div>

      <!-- Description & Pricing -->
      <div class="mt-6 flex items-baseline justify-between">
        <div>
          <span class="text-3xl font-extrabold text-slate-900">$49.00</span>
          <span class="text-xs text-slate-500 font-medium ml-1">one-time payment</span>
        </div>
        <button id="buyBtn" onclick="handleBuy()" class="bg-blue-600 hover:bg-blue-700 active:scale-95 text-white font-semibold px-6 py-2.5 rounded-xl shadow-md transition duration-150 flex items-center gap-2">
          <span>BUY NOW</span>
          <i class="fa-solid fa-arrow-right text-xs"></i>
        </button>
      </div>

      <!-- Feature Bullets -->
      <div class="mt-6 pt-5 border-t border-slate-100 space-y-3">
        <div class="flex items-center text-sm text-slate-600">
          <i class="fa-solid fa-truck-fast text-emerald-500 mr-3"></i>
          <span>Free 2-day express global delivery</span>
        </div>
        <div class="flex items-center text-sm text-slate-600">
          <i class="fa-solid fa-shield-halved text-emerald-500 mr-3"></i>
          <span>30-day no-questions-asked refund</span>
        </div>
        <div class="flex items-center text-sm text-slate-600">
          <i class="fa-solid fa-code text-emerald-500 mr-3"></i>
          <span>100% Open-source hardware & firmware</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    function handleBuy() {
      const btn = document.getElementById('buyBtn');
      btn.innerHTML = '<i class="fa-solid fa-check"></i> Added!';
      btn.classList.replace('bg-blue-600', 'bg-emerald-600');
      setTimeout(() => {
        btn.innerHTML = '<span>BUY NOW</span> <i class="fa-solid fa-arrow-right text-xs"></i>';
        btn.classList.replace('bg-emerald-600', 'bg-blue-600');
      }, 2000);
    }
  </script>
</body>
</html>"""
    else:
        # Annotated version with Dark Mode Toggle, Star Ratings, and 50% OFF Badge!
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Launch Card (Iterative Edit) - Napkin2Code</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script>
    tailwind.config = {
      darkMode: 'class',
    }
  </script>
</head>
<body id="bodyRoot" class="bg-slate-100 dark:bg-slate-900 transition-colors duration-300 flex items-center justify-center min-h-screen p-6 font-sans">
  <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-xl dark:shadow-indigo-500/10 border border-slate-200 dark:border-slate-700 max-w-md w-full overflow-hidden transition-all duration-300">
    <div class="p-6">
      
      <!-- Top Bar with Added Dark Mode Switch -->
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-2xl font-bold text-slate-800 dark:text-white tracking-tight">Product Launch Card</h2>
          <span class="inline-block px-2.5 py-0.5 text-xs font-bold bg-rose-100 text-rose-700 dark:bg-rose-900/60 dark:text-rose-300 rounded-md mt-1 animate-pulse">
            🔥 50% OFF FLASH SALE
          </span>
        </div>
        
        <!-- Physical Red-Pen Annotation 1: Dark Mode Toggle -->
        <button id="themeToggle" onclick="toggleTheme()" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-yellow-400 hover:scale-110 transition shadow-sm" title="Toggle Dark Mode">
          <i id="themeIcon" class="fa-solid fa-moon"></i>
        </button>
      </div>

      <!-- Image Area -->
      <div class="relative bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-600 rounded-xl h-52 flex flex-col items-center justify-center text-white p-4 shadow-lg overflow-hidden">
        <i class="fa-solid fa-microchip text-5xl mb-2 opacity-95 drop-shadow-md"></i>
        <span class="text-sm font-semibold tracking-wide">Next-Gen Cyberpunk Edition</span>
        <div class="absolute top-3 right-3 bg-red-500 text-white text-xs font-extrabold px-2.5 py-1 rounded-full uppercase tracking-wider shadow">
          Limited
        </div>
      </div>

      <!-- Physical Red-Pen Annotation 2: Star Ratings -->
      <div class="mt-4 flex items-center justify-between">
        <div class="flex items-center gap-1.5 text-amber-400 text-sm">
          <i class="fa-solid fa-star"></i>
          <i class="fa-solid fa-star"></i>
          <i class="fa-solid fa-star"></i>
          <i class="fa-solid fa-star"></i>
          <i class="fa-solid fa-star"></i>
          <span class="text-xs font-semibold text-slate-500 dark:text-slate-400 ml-1">(128 reviews)</span>
        </div>
        <span class="text-xs font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50 px-2 py-0.5 rounded">
          ✓ Verified In-Stock
        </span>
      </div>

      <!-- Description & Pricing -->
      <div class="mt-5 flex items-baseline justify-between">
        <div>
          <span class="text-3xl font-extrabold text-slate-900 dark:text-white">$24.50</span>
          <span class="text-sm text-slate-400 line-through ml-1.5">$49.00</span>
        </div>
        <button id="buyBtn" onclick="handleBuy()" class="bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 active:scale-95 text-white font-semibold px-6 py-2.5 rounded-xl shadow-md transition duration-150 flex items-center gap-2">
          <span>CLAIM DEAL</span>
          <i class="fa-solid fa-bolt text-xs"></i>
        </button>
      </div>

      <!-- Feature Bullets -->
      <div class="mt-6 pt-5 border-t border-slate-100 dark:border-slate-700 space-y-3">
        <div class="flex items-center text-sm text-slate-600 dark:text-slate-300">
          <i class="fa-solid fa-truck-fast text-indigo-500 mr-3"></i>
          <span>Free 2-day express global delivery</span>
        </div>
        <div class="flex items-center text-sm text-slate-600 dark:text-slate-300">
          <i class="fa-solid fa-shield-halved text-indigo-500 mr-3"></i>
          <span>30-day money-back guarantee</span>
        </div>
        <div class="flex items-center text-sm text-slate-600 dark:text-slate-300">
          <i class="fa-solid fa-code text-indigo-500 mr-3"></i>
          <span>100% Open-source hardware & firmware</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    let isDark = false;
    function toggleTheme() {
      isDark = !isDark;
      const html = document.documentElement;
      const icon = document.getElementById('themeIcon');
      if (isDark) {
        html.classList.add('dark');
        icon.classList.replace('fa-moon', 'fa-sun');
      } else {
        html.classList.remove('dark');
        icon.classList.replace('fa-sun', 'fa-moon');
      }
    }

    function handleBuy() {
      const btn = document.getElementById('buyBtn');
      btn.innerHTML = '<i class="fa-solid fa-check"></i> Deal Claimed!';
      btn.classList.replace('bg-indigo-600', 'bg-emerald-600');
      setTimeout(() => {
        btn.innerHTML = '<span>CLAIM DEAL</span> <i class="fa-solid fa-bolt text-xs"></i>';
        btn.classList.replace('bg-emerald-600', 'bg-indigo-600');
      }, 2000);
    }
  </script>
</body>
</html>"""


def generate_code_from_sketch(
    image: Image.Image,
    model: str = "moondream",
    existing_html: Optional[str] = None,
    host: str = DEFAULT_OLLAMA_HOST,
    timeout: int = 120
) -> Tuple[str, bool, str]:
    """Generates HTML code from a sketch image using local Ollama vision model.

    Returns:
        (html_code, is_live_model_used, status_message)
    """
    is_ollama_up, available_models = check_ollama_status(host)

    # Convert image to base64
    b64_image = image_to_base64(image)

    # Determine prompt mode
    is_iteration = bool(existing_html and len(existing_html.strip()) > 50)
    system_prompt = ITERATIVE_EDIT_SYSTEM_PROMPT if is_iteration else INITIAL_SKETCH_SYSTEM_PROMPT
    user_prompt = build_iterative_user_prompt(existing_html) if is_iteration else INITIAL_SKETCH_USER_PROMPT

    if not is_ollama_up:
        # Graceful fallback to verified prototype code
        demo_code = get_demo_fallback_code(is_annotated=is_iteration)
        msg = f"Ollama is not running on {host}. Loaded verified offline demonstration code."
        return demo_code, False, msg

    # Check if requested model or any vision model is available
    matched_model = None
    for m in [model, "moondream", "llama3.2-vision:11b", "llama3.2-vision", "llava"]:
        for avail in available_models:
            if m.lower() in avail.lower():
                matched_model = avail
                break
        if matched_model:
            break

    if not matched_model:
        demo_code = get_demo_fallback_code(is_annotated=is_iteration)
        msg = f"Model '{model}' not found in Ollama tags. Available: {available_models}. Loaded verified offline code."
        return demo_code, False, msg

    # Call Ollama API
    payload = {
        "model": matched_model,
        "prompt": f"{system_prompt}\n\n{user_prompt}",
        "images": [b64_image],
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
        }
    }

    try:
        resp = requests.post(f"{host}/api/generate", json=payload, timeout=timeout)
        if resp.status_code == 200:
            result = resp.json()
            raw_response = result.get("response", "")
            clean_html = extract_html_code(raw_response)
            msg = f"Generated successfully using local model '{matched_model}' via Ollama!"
            return clean_html, True, msg
        else:
            demo_code = get_demo_fallback_code(is_annotated=is_iteration)
            return demo_code, False, f"Ollama HTTP error {resp.status_code}. Fallback loaded."
    except Exception as e:
        demo_code = get_demo_fallback_code(is_annotated=is_iteration)
        return demo_code, False, f"Ollama inference exception: {e}. Fallback loaded."
