"""Stage 2: coder model. Reads text only, outputs HTML."""
import json
import re
import ollama
import config
from engine import prompts


def extract_html(text: str) -> str:
    """Pull the <!DOCTYPE html>...</html> block out of model text; strip code fences."""
    content = text.strip()

    doc_pattern = re.compile(r"(<!DOCTYPE\s+html.*?>[\s\S]*?<\/html>)", re.IGNORECASE)
    match = doc_pattern.search(content)
    if match:
        return match.group(1).strip()

    html_pattern = re.compile(r"(<html.*?>[\s\S]*?<\/html>)", re.IGNORECASE)
    match = html_pattern.search(content)
    if match:
        return "<!DOCTYPE html>\n" + match.group(1).strip()

    fence_pattern = re.compile(r"```(?:html)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
    match = fence_pattern.search(content)
    if match:
        return match.group(1).strip()

    return content


def spec_to_html(spec: dict) -> str:
    """Generate HTML5 code from UI spec dict."""
    try:
        spec_text = json.dumps(spec, indent=2)
        resp = ollama.chat(
            model=config.CODE_MODEL,
            messages=[
                {"role": "system", "content": prompts.CODE_SYSTEM_PROMPT},
                {"role": "user", "content": prompts.GENERATE_PROMPT.format(spec=spec_text)},
            ],
            options={"temperature": config.TEMPERATURE},
        )
        content = resp["message"]["content"]
        html = extract_html(content)
        if not html:
            raise ValueError("Empty HTML output received from model")
        return html
    except Exception as e:
        raise RuntimeError(f"Failed to generate HTML from spec: {e}") from e


def edit_html(html: str, instruction: str) -> str:
    """Update existing HTML code based on handwritten annotations or instruction."""
    try:
        resp = ollama.chat(
            model=config.CODE_MODEL,
            messages=[
                {"role": "system", "content": prompts.CODE_SYSTEM_PROMPT},
                {"role": "user", "content": prompts.EDIT_PROMPT.format(html=html, instruction=instruction)},
            ],
            options={"temperature": config.TEMPERATURE},
        )
        content = resp["message"]["content"]
        updated_html = extract_html(content)
        if not updated_html:
            raise ValueError("Empty HTML output received from model during edit")
        return updated_html
    except Exception as e:
        raise RuntimeError(f"Failed to edit HTML with instruction: {e}") from e
