# PLAN.md — Napkin2Code spec (source of truth)

## Flow
1. Image (webcam or upload) -> `core.image_processing.enhance` -> bytes
2. GENERATE: `engine.vision_ai.sketch_to_spec(bytes)` -> dict spec -> `engine.codegen.spec_to_html(spec)` -> html str
3. ITERATE: `engine.vision_ai.extract_annotations(bytes)` -> str instruction -> `engine.codegen.edit_html(html, instruction)` -> html str
4. `app.py` shows html in an iframe, a code tab, and a download button.

## Two-stage design (important)
- Vision model ONLY describes what it sees (JSON, or handwritten notes as text).
- Coder model ONLY writes/edits HTML from text. It never sees images.

## Function contracts (do not change signatures)
| File | Function | Returns |
|---|---|---|
| core/image_processing.py | `enhance(image_bytes: bytes) -> bytes` | JPEG bytes, autocontrast + sharpen, longest side <= 1024 |
| engine/vision_ai.py | `sketch_to_spec(image_bytes: bytes) -> dict` | spec dict (schema below) |
| engine/vision_ai.py | `extract_annotations(image_bytes: bytes) -> str` | handwritten instruction text, "" if none |
| engine/codegen.py | `spec_to_html(spec: dict) -> str` | one complete HTML5 file |
| engine/codegen.py | `edit_html(html: str, instruction: str) -> str` | full updated HTML file |
| engine/codegen.py | `extract_html(text: str) -> str` | HTML block pulled from model text |

## Spec schema
```json
{
  "title": "string",
  "elements": [
    {"type": "button|input|image|text|list|nav|card", "label": "string", "position": "top|middle|bottom|left|right"}
  ]
}
```

## Output HTML rules
Single file, HTML5, Tailwind via CDN `<script src="https://cdn.tailwindcss.com"></script>`, vanilla JS only, no external images (use colored placeholder boxes).

## Build order
1. config.py, core/image_processing.py
2. engine/vision_ai.py (+ prompts)
3. engine/codegen.py
4. test_pipeline.py  <- tune prompts here with real photos in samples/
5. app.py
6. Iterate mode, offline polish, README

## Status checklist
- [x] image_processing
- [x] vision_ai
- [x] codegen
- [ ] test_pipeline passes on 3/4 samples (awaiting sample sketch images)
- [x] app.py generate flow
- [x] iterate flow
- [x] README with model cards + licenses
- [ ] repo public, MIT license, submitted
