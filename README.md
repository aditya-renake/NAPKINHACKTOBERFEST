# Napkin2Code

Turn a hand-drawn paper sketch into a working web app, using 100% local open-weight AI. No cloud APIs, no cost, fully private.

> Built for the MLH Open Source AI Hackathon (Hacktoberfest Hack Day, Pune).

## Demo
_(add GIF / screenshots here)_

## The problem
Most AI website builders rely on expensive, proprietary cloud APIs, require constant internet connectivity, and only accept digital wireframes or text prompts. Napkin2Code makes web prototyping tactile, private, and free by turning real hand-drawn paper sketches directly into interactive HTML/Tailwind web apps using open-weight models on your local machine.

## How it works
1. Photograph a sketch with your webcam or upload a photo.
2. A local vision model analyzes the sketch and describes the UI elements as a JSON spec.
3. A local coder model converts the spec into a responsive, single-file HTML5 app styled with Tailwind CSS.
4. Draw notes, arrows, or edit instructions on the paper and re-photograph it to iterate.

## Models (all open-weight, run locally via Ollama)
| Role | Model | License | Model card |
|---|---|---|---|
| Vision | `gemma3:4b` | Gemma Terms of Use | [google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it) |
| Code | `qwen2.5-coder:7b` | Apache 2.0 | [Qwen/Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct) |

## Setup
```bash
# 1. Install Ollama from https://ollama.com and make sure it is running
ollama pull gemma3:4b
ollama pull qwen2.5-coder:7b

# 2. Install dependencies
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

## Project structure
See `PLAN.md`.

## License
MIT, see `LICENSE`.
