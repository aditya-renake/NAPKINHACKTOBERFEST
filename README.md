# 📸 Napkin2Code: Physical Sketch to Live Software
### *MLH Open Source AI Hackathon — Hacktoberfest Hack Day, Pune*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-indigo.svg)](https://www.python.org/)
[![Local AI: Ollama](https://img.shields.io/badge/AI-100%25%20Local%20(Ollama)-emerald.svg)](https://ollama.com/)
[![Vision Model: Google Gemma 4](https://img.shields.io/badge/Model-Google%20Gemma%204%20(E2B%2FE4B)-blue.svg)](https://ollama.com/library/gemma4)
[![Vision Model: Moondream2](https://img.shields.io/badge/Model-Moondream2%20(1.86B)-purple.svg)](https://github.com/vikhyat/moondream)
[![Zero Cloud APIs](https://img.shields.io/badge/Cloud%20APIs-%240.00%20Zero-green.svg)](#)

> **Tagline:** Turn rough hand-drawn paper sketches and cafe napkins into working, interactive web applications in seconds using 100% local, open-weight vision AI. Zero cloud APIs, zero cost, 100% private.

---

## 🌟 1. Overview & Core Innovation

Commercial AI code generators (like Vercel v0, Bolt, or tldraw Make Real) are:
1. **Expensive and Closed-Source**: Rely on costly proprietary cloud APIs (OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet).
2. **Cloud-Dependent**: If the venue Wi-Fi drops, they stop working completely.
3. **Screen-Bound**: They require digital drawing tablets or uploading PNG screenshots.

### Our Solution: Napkin2Code
**Napkin2Code** bridges the **physical world and digital software**:
- **Physical First**: Grab any real pen and paper, a cafe napkin, or a whiteboard in the room. Draw a rough UI layout.
- **Webcam Capture**: Hold the paper up to your laptop webcam.
- **Local Open-Weight AI**: Powered by local Small Vision Models (**Google Gemma 4 E2B/E4B**, **Moondream 2**, or **Llama 3.2 Vision** via **Ollama**) to parse ink strokes and generate responsive HTML with Tailwind CSS.
- **Interactive Live App**: A working, clickable application renders in real-time right beside your camera feed.

### 🚀 The "Secret Weapon" Feature: Physical Iterative Editing
Unlike one-shot generators, **you can iterate with a real pen**:
1. Draw a basic UI $\rightarrow$ Hold to webcam $\rightarrow$ Live app appears.
2. Grab your red pen, draw an arrow pointing to a button, and write: `"+ Add Dark Mode toggle and star ratings ⭐"` or cross an element out.
3. Hold it back up to the webcam and click **"Apply Physical Handwritten Edits"**.
4. The local AI reads the **current code** + **your handwritten physical annotations** and updates the live website in real time!

---

## 🏗️ 2. System Architecture

```mermaid
flowchart LR
    A["Real Paper / Napkin Sketch"] -->|Webcam Snapshot| B["Image Preprocessor (Ink Contrast Boost)"]
    B --> C["Local Vision Engine (Ollama: Moondream / Llama 3.2 Vision)"]
    
    subgraph "Stateful Iteration Loop"
        C -->|Initial Sketch| D["HTML + Tailwind CSS Generator"]
        D --> E["Active App State (Code in Memory)"]
        E -->|Current Code + New Annotated Sketch| C
        C -->|Physical Edit / Diff| F["Intelligent Code Updater"]
        F --> E
    end
    
    E --> G["Interactive Live Preview (Clickable iframe)"]
    E --> H["1-Click Code Export (.html)"]
```

---

## 👥 3. Project Structure

```text
HackToberFest/
├── app.py                      # Flagship Streamlit split-screen UI & state manager
├── requirements.txt            # Python dependencies (Streamlit, Ollama, Pillow, NumPy)
├── LICENSE                     # Standard MIT License
├── PROJECT_PLAN.md             # Hack Day division of labor & timeline
├── core/
│   ├── __init__.py
│   └── image_processing.py     # Shadow/lighting normalization, ink enhancement & image encoding
├── engine/
│   ├── __init__.py
│   ├── prompts.py              # Vision model prompt templates (Initial & Iterative)
│   └── vision_ai.py            # Ollama client, model validation & fallback engine
├── assets/
│   ├── generate_samples.py     # Script to generate sample paper sketches
│   └── samples/
│       ├── sample_product_card.png          # Base eCommerce sketch
│       └── sample_product_card_iterated.png # Revised sketch with red pen scribbles
└── tests/
    ├── test_image_processing.py # Unittest suite for image pipeline
    └── test_vision_ai.py        # Unittest suite for HTML sanitizer & prompts
```

---

## ⚡ 4. Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) (Free, open-source local inference engine)

### 2. Install & Start Ollama
```bash
# On macOS:
brew install ollama

# Start the Ollama server:
ollama serve
```

### 3. Pull the Small Vision Model
```bash
# Google Gemma 4 on-device multimodal model (E2B / 128K context):
ollama pull gemma4:e2b

# Ultra-fast & lightweight (1.8GB, runs smoothly on any CPU/GPU):
ollama pull moondream

# Or for deep reasoning:
ollama pull llama3.2-vision:11b
```

### 4. Clone & Run Napkin2Code
```bash
git clone https://github.com/aditya-renake/NAPKINHACKTOBERFEST.git
cd NAPKINHACKTOBERFEST

# Create virtual environment & install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 5. Testing & Verification

Run the test suite:
```bash
python -m unittest discover tests
```

---

## 🧠 6. Open-Weight Model Citations & Architecture

Napkin2Code is strictly compliant with open-source and hackathon guidelines:

| Pipeline Stage | Model | License | Description |
|---|---|---|---|
| **Vision (Direct / Multimodal)** | `gemma4:e2b` / `gemma4:e4b` | Gemma Terms of Use | Google DeepMind frontier on-device multimodal model (128K context) |
| **Vision (Lightweight Fast)** | `moondream2` (1.86B) | Apache 2.0 | Ultra-fast Small Vision Model running smoothly on any CPU/GPU |
| **Vision (Deep Reasoning)** | `llama3.2-vision:11b` | Llama 3.2 Community | High-accuracy layout and fine handwriting recognition |
| **Two-Stage Coder Engine** | `qwen2.5-coder:7b` | Apache 2.0 | Specialized code synthesis model converting UI JSON specs into HTML5/Tailwind |
| **Local Inference Server** | `ollama` | MIT License | 100% open-source local LLM/VLM runner (`localhost:11434`) |

- **Zero Proprietary Cloud APIs**: No OpenAI, Anthropic, or proprietary cloud endpoints are required or used.

---

## 🏗️ 7. Project Structure & Architecture

For detailed development specs, prompt strategies, and pipeline architecture:
- See [`PROJECT_PLAN.md`](PROJECT_PLAN.md) and [`PLAN.md`](PLAN.md).
- See Agent Skill standard definition in [`skills/napkin2code/SKILL.md`](skills/napkin2code/SKILL.md).

---

## 🎤 8. The 2-Minute Demo Script for Judges

1. **The Hook (15 seconds)**:  
   *"Judges, tools like Vercel v0 and OpenAI charge $20/month and require constant internet connection to turn digital mockups into code. We asked: Why can't a developer or student sketch on a real coffee napkin with zero Wi-Fi and watch it turn into real software on their laptop for free?"*

2. **The First Live Action (30 seconds)**:  
   *(Hold up a piece of paper with a hand-drawn product card: title, image placeholder, and 'Buy Now' button)*  
   *"Watch this: We hold this rough sketch to our laptop webcam. Click 'Compile Sketch'."*  
   *(In seconds, the live interactive website pops up on screen with working buttons, counters, and Tailwind CSS)*

3. **The 'Mind-Blowing' Iteration Moment (45 seconds)**:  
   *(Pick up a red marker pen live in front of the judges)*  
   *"Now, what if the client wants changes? Instead of retyping code, watch me draw a physical arrow pointing to the button and write: '+ Add Dark Mode toggle and 20% OFF Sale badge'."*  
   *(Hold paper back up to webcam $\rightarrow$ Click 'Merge Physical Handwritten Edits')*  
   *(The live app refreshes with a working dark mode toggle and sale badge!)*

4. **The Open-Source Impact (30 seconds)**:  
   *"This runs on 100% open-weight AI (Google Gemma 4 / Moondream 2 / Qwen 2.5 Coder) using Ollama on our local machine. It uses zero cloud APIs, costs $0, preserves 100% privacy, and works completely offline. The code is public under the MIT license."*

---

## 📜 9. License

This project is licensed under the [MIT License](LICENSE).

