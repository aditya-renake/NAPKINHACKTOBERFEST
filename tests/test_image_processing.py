"""
Unit tests for image processing pipeline.
"""
import unittest
from PIL import Image
import numpy as np
from core.image_processing import (
    enhance_sketch,
    image_to_base64,
    image_to_bytes,
    load_image_from_bytes,
)


class TestImageProcessing(unittest.TestCase):
    def test_enhance_sketch_dimensions_and_mode(self):
        img = Image.new("RGB", (200, 200), color=(250, 245, 240))
        enhanced = enhance_sketch(img, contrast_factor=1.5, sharpness_factor=1.5)
        self.assertEqual(enhanced.size, (200, 200))
        self.assertEqual(enhanced.mode, "RGB")

    def test_enhance_sketch_reduces_uneven_lighting(self):
        pixels = np.zeros((128, 256, 3), dtype=np.uint8)
        for x in range(256):
            pixels[:, x] = (170 + x // 4,) * 3
        pixels[48:80, 96:160] = (25, 45, 90)
        img = Image.fromarray(pixels)

        enhanced = enhance_sketch(
            img,
            contrast_factor=1.0,
            sharpness_factor=1.0,
            brightness_factor=1.0,
            auto_levels=False,
        )
        enhanced_pixels = np.asarray(enhanced)
        original_background = pixels[10:30, :, 0]
        enhanced_background = enhanced_pixels[10:30, :, 0]

        self.assertLess(float(enhanced_background.std()), float(original_background.std()))
        self.assertLess(float(enhanced_pixels[60, 120].mean()), float(enhanced_pixels[20, 120].mean()))
        self.assertGreater(
            int(enhanced_pixels[60, 120, 2]),
            int(enhanced_pixels[60, 120, 0]),
        )

    def test_image_to_base64_and_bytes(self):
        img = Image.new("RGB", (100, 100), color=(255, 255, 255))
        b64_str = image_to_base64(img)
        self.assertIsInstance(b64_str, str)
        self.assertTrue(len(b64_str) > 0)

        raw_bytes = image_to_bytes(img)
        self.assertIsInstance(raw_bytes, bytes)
        self.assertTrue(len(raw_bytes) > 0)

        reloaded = load_image_from_bytes(raw_bytes)
        self.assertEqual(reloaded.size, (100, 100))
        self.assertEqual(reloaded.mode, "RGB")

    def test_load_image_composites_transparency_onto_white(self):
        img = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        img.putpixel((5, 5), (20, 40, 80, 255))

        reloaded = load_image_from_bytes(image_to_bytes(img, format="PNG"))

        self.assertEqual(reloaded.mode, "RGB")
        self.assertEqual(reloaded.getpixel((0, 0)), (255, 255, 255))
        self.assertEqual(reloaded.getpixel((5, 5)), (20, 40, 80))


if __name__ == "__main__":
    unittest.main()
