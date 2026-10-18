"""Napkin2Code - Prompt Engineering Module.

Optimized prompt templates for small vision language models (Moondream2 / Llama 3.2 Vision).
"""

INITIAL_SYSTEM_PROMPT = """You are an expert Frontend Architect and UI/UX Designer.
Your task is to examine hand-drawn paper/napkin sketches and convert them into beautiful, modern, responsive, and interactive web applications.

Rules for your output:
1. Generate a single, complete, fully working HTML file (starting with <!DOCTYPE html> and ending with </html>).
2. Use Tailwind CSS via CDN: <script src="https://cdn.tailwindcss.com"></script>.
3. Include icons where appropriate using FontAwesome CDN:
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
4. Make UI elements INTERACTIVE using lightweight Vanilla JavaScript:
   - Buttons should perform realistic actions (e.g., open modals, toggle counters, change states, show toast alerts).
   - Forms should have client-side submit handling (e.g. show success alert or state update).
   - Toggles (like Dark Mode, Tabs, or Accordions) must function when clicked.
5. High Aesthetic Standards:
   - Use clean shadows, subtle borders, rounded corners (e.g. rounded-xl), modern typography (Inter/sans-serif), and aesthetic color palettes (slate, indigo, emerald, violet).
   - Responsive layout using flexbox or grid.
6. STRICT OUTPUT CONSTRAINT: Return ONLY valid HTML code. Do NOT include markdown code blocks like ```html ... ```, and do NOT include any introductory or concluding conversational text.
"""

INITIAL_USER_PROMPT = """Analyze this hand-drawn UI sketch carefully.
Identify all drawn layout structures, navigation bars, headers, cards, buttons, text fields, lists, checkboxes, and interactive elements.
Transform this sketch into a production-grade, interactive web interface using Tailwind CSS.
Remember: Output ONLY the complete HTML document, no markdown wrappers, no conversational filler."""

ITERATIVE_EDIT_PROMPT_TEMPLATE = """You are an expert Frontend Developer modifying an existing web application based on a physical hand-drawn revision.

Here is the CURRENT HTML of the application:
```html
{current_html}
```

The user has now provided a new photo of their sketch with physical handwritten revisions (arrows, handwritten text, crossed out sections, newly drawn widgets, or sticky notes).

Your Task:
1. Carefully inspect the physical annotations and notes drawn on the paper sketch.
2. Determine what elements were added, modified, repositioned, or crossed out.
3. Apply these exact updates to the CURRENT HTML code while strictly preserving existing functionality, structure, and styling.
4. Make any newly requested elements fully interactive with Vanilla JavaScript.
5. Return the COMPLETE updated HTML file from <!DOCTYPE html> to </html>.
6. STRICT OUTPUT CONSTRAINT: Return ONLY the raw HTML document. No markdown code blocks, no conversational preamble or postscript.
"""

# Aliases for compatibility across engine imports
INITIAL_SKETCH_SYSTEM_PROMPT = INITIAL_SYSTEM_PROMPT
INITIAL_SKETCH_USER_PROMPT = INITIAL_USER_PROMPT
ITERATIVE_EDIT_SYSTEM_PROMPT = ITERATIVE_EDIT_PROMPT_TEMPLATE


def build_initial_prompt(user_instructions: str = "") -> str:
    """Build the prompt for initial sketch-to-code generation."""
    if user_instructions.strip():
        return f"{INITIAL_USER_PROMPT}\n\nAdditional User Guidance:\n{user_instructions.strip()}"
    return INITIAL_USER_PROMPT


def build_iterative_prompt(current_html: str, user_notes: str = "") -> str:
    """Build the prompt for iterative physical pen/annotation editing."""
    prompt = ITERATIVE_EDIT_PROMPT_TEMPLATE.format(current_html=current_html.strip())
    if user_notes.strip():
        prompt += f"\n\nAdditional User Notes:\n{user_notes.strip()}"
    return prompt


def build_iterative_user_prompt(existing_html: str, user_notes: str = "") -> str:
    """Alias for build_iterative_prompt."""
    return build_iterative_prompt(existing_html, user_notes)
