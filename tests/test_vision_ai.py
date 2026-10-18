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

    def test_get_fallback_html(self):
        fallback = get_fallback_html("Custom Test Message")
        self.assertIn("<!DOCTYPE html>", fallback)
        self.assertIn("cdn.tailwindcss.com", fallback)
        self.assertIn("Custom Test Message", fallback)


if __name__ == "__main__":
    unittest.main()
