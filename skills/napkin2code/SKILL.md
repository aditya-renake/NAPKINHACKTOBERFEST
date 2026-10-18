---
name: napkin2code
description: Converts physical hand-drawn paper sketches, wireframes, and whiteboard drawings into responsive HTML with Tailwind CSS, and supports iterative physical red-pen annotations.
version: 1.0.0
author: Napkin2Code Team
license: MIT
metadata:
  model_compatibility:
    - moondream
    - llama3.2-vision:11b
    - qwen2-vl:7b
    - llava:7b
  inference_engine: ollama
  category: frontend-engineering
---

# Napkin2Code: Agent Skill

An open-source agent skill adhering to the [Agent Skills Open Standard](https://agentskills.io/specification). This skill equips AI agent harnesses with the ability to interpret real-world hand-drawn wireframes and physical red-pen code modifications.

## Capabilities

1. **Initial Sketch to Code**: Ingests an image of a physical drawing (via base64 or file path) and synthesizes clean HTML5 with Tailwind CSS.
2. **Physical Iterative Refactoring**: Ingests an existing HTML snippet along with a newly annotated drawing (containing handwritten arrows, labels, or strikethroughs) and merges the changes into the HTML code.
3. **Local Privacy**: Runs 100% locally through Ollama with open-weight vision models (Moondream 2 or Llama 3.2 Vision).

## Usage via CLI / Python

```python
from PIL import Image
from engine.vision_engine import generate_code_from_sketch

# 1. Initial Generation from Sketch
sketch_img = Image.open("path/to/paper_sketch.png")
html_code, is_live, status = generate_code_from_sketch(
    image=sketch_img,
    model="moondream"
)

# 2. Iterative Update with Physical Red-Pen Annotations
annotated_img = Image.open("path/to/annotated_sketch.png")
updated_html, is_live, status = generate_code_from_sketch(
    image=annotated_img,
    model="moondream",
    existing_html=html_code
)
```

## Input Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `image` | `PIL.Image` | Yes | Captured snapshot of physical sketch or whiteboard. |
| `model` | `str` | No | Vision model name in Ollama (default: `moondream`). |
| `existing_html` | `str` | No | Existing HTML codebase to update (triggers Iterative Edit mode). |

## Output

Returns a tuple: `(html_code: str, is_live_model_used: bool, status_message: str)`.
