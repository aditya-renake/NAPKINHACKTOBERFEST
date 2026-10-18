"""
Unit tests for vision AI response parsing and HTML extraction.
"""
import unittest
from engine.vision_ai import clean_extracted_html, get_fallback_html, check_ollama_status


class TestVisionAI(unittest.TestCase):
    def test_clean_extracted_html_markdown_fence(self):
        raw = """Here is your generated code:
```html
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body><h1>Hello World</h1></body>
</html>
```
Hope you like it!"""
        cleaned = clean_extracted_html(raw)
        self.assertTrue(cleaned.startswith("<!DOCTYPE html>"))
        self.assertTrue(cleaned.endswith("</html>"))
        self.assertIn("<h1>Hello World</h1>", cleaned)
        self.assertNotIn("Here is your generated code:", cleaned)

    def test_clean_extracted_html_raw_tags(self):
        raw = """<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body><button>Click</button></body>
</html>"""
        cleaned = clean_extracted_html(raw)
        self.assertEqual(cleaned, raw)

    def test_clean_extracted_html_snippet_wrapper(self):
        raw = """<div class="p-4 bg-white rounded shadow"><button>Button</button></div>"""
        cleaned = clean_extracted_html(raw)
        self.assertIn("<!DOCTYPE html>", cleaned)
        self.assertIn("cdn.tailwindcss.com", cleaned)
        self.assertIn("<button>Button</button>", cleaned)

    def test_resolve_vision_model_exact_and_fallback(self):
        from engine.vision_ai import resolve_vision_model

        # Case 1: Exact match
        model, exact, notice = resolve_vision_model("moondream:latest", ["moondream:latest"])
        self.assertEqual(model, "moondream:latest")
        self.assertTrue(exact)
        self.assertIsNone(notice)

        # Case 2: Base tag match
        model, exact, notice = resolve_vision_model("moondream", ["moondream:latest"])
        self.assertEqual(model, "moondream:latest")
        self.assertTrue(exact)

        # Case 3: Missing model falling back to available vision model
        model, exact, notice = resolve_vision_model("llama3.2-vision", ["moondream:latest"])
        self.assertEqual(model, "moondream:latest")
        self.assertFalse(exact)
        self.assertIn("not found in Ollama", notice)


if __name__ == "__main__":
    unittest.main()

