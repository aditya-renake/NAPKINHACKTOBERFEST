# AGENTS.md — Rules for any AI coding agent working in this repo

Read this file and PLAN.md BEFORE writing any code.

## Project
Napkin2Code: photo of a hand-drawn UI sketch -> live HTML/Tailwind app, using ONLY local open-weight models through Ollama. Hackathon project (MLH Open Source AI). Time is very limited: keep everything simple.

## Hard rules
1. NO cloud AI APIs (no OpenAI, Gemini, Anthropic, HuggingFace Inference). All AI calls go through the `ollama` Python package to localhost.
2. Model names live ONLY in `config.py`. Never hardcode a model name anywhere else. Never invent model names.
3. Allowed dependencies: streamlit, ollama, pillow (see requirements.txt). Do not add others without being asked.
4. No Docker, no database, no extra frameworks, no async code, no classes unless needed.
5. Only create or edit the file(s) the user names. Do not rewrite other files. Do NOT modify `engine/prompts.py` once the user says it is tuned.
6. Keep the function signatures in PLAN.md exactly as written. Other files depend on them.
7. Every Ollama call must be wrapped in try/except and raise `RuntimeError` with a readable message.
8. Python 3.10+. Add short docstrings. No long explanations in code comments.
9. If something is unclear, ask. Do not guess library APIs: use the snippet below.

## Correct Ollama usage (do not deviate)
```python
import ollama
resp = ollama.chat(
    model=VISION_MODEL,
    messages=[{"role": "user", "content": PROMPT, "images": [image_bytes]}],
    format="json",            # only for JSON outputs
    options={"temperature": 0.2},
)
text = resp["message"]["content"]
```

## Streamlit usage
- Camera: `st.camera_input(...)` returns an UploadedFile; use `.getvalue()` for bytes.
- Upload: `st.file_uploader(..., type=["png","jpg","jpeg"])`.
- Live preview: `import streamlit.components.v1 as components; components.html(html, height=650, scrolling=True)`.
- State: `st.session_state["html"]`.
