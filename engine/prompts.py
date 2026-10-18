"""All prompt text lives here."""

SPEC_PROMPT = """You are looking at a hand-drawn UI wireframe on paper.
Return ONLY valid JSON in this exact shape:
{"title": "short page title",
 "elements": [{"type": "button|input|image|text|list|nav|card", "label": "text written on or near it", "position": "top|middle|bottom|left|right"}]}
Rules: describe only what is actually drawn, in top-to-bottom order. Do not invent elements. Ignore handwritten notes in a different color or marked with arrows; those are edit instructions."""

ANNOTATION_PROMPT = """Look at this image of a UI sketch. Find ONLY the handwritten edit instructions
(notes starting with '+', arrows with text, crossed-out items). Reply with plain text, one instruction per line.
If there are none, reply with exactly: NONE"""

CODE_SYSTEM_PROMPT = """You are a front-end generator. Output ONLY one complete HTML5 file and nothing else.
Rules: use Tailwind via <script src="https://cdn.tailwindcss.com"></script>; vanilla JS only for interactivity;
no external images (use colored placeholder boxes); make buttons and inputs actually work; modern clean design.
No markdown, no code fences, no explanation."""

GENERATE_PROMPT = "Build a responsive web page from this UI spec:\n{spec}"

EDIT_PROMPT = """Here is the current HTML file:
{html}

Apply ONLY this change and keep everything else identical:
{instruction}

Return the COMPLETE updated HTML file, not a diff."""
