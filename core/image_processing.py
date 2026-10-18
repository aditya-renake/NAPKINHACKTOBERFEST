"""
Napkin2Code - Core Image Processing Module
Enhances contrast, removes glare, and sharpens ink strokes from paper/napkin webcam captures.
"""

import io
import base64
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np


def _to_rgb(image: Image.Image) -> Image.Image:
    """Convert an image to RGB, compositing transparency onto white paper."""
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA") or "transparency" in image.info:
        rgba = image.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        return Image.alpha_composite(background, rgba).convert("RGB")
    return image.convert("RGB")


def _normalize_lighting(image: Image.Image) -> Image.Image:
    """Reduce broad shadows and brightness variations without discarding ink color."""
    rgb = np.asarray(image, dtype=np.float32)
    luminance = np.asarray(image.convert("L"), dtype=np.float32)
    blur_radius = max(8, min(image.size) * 0.05)
    background = np.asarray(
        Image.fromarray(luminance.astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(radius=blur_radius)
        ),
        dtype=np.float32,
    )

    paper_level = float(np.percentile(background, 75))
    correction = paper_level / np.maximum(background, 1.0)
    correction = np.clip(correction, 0.65, 1.5)
    corrected = np.clip(rgb * correction[:, :, np.newaxis], 0, 255).astype(np.uint8)
    return Image.fromarray(corrected)


def enhance_sketch(
    image: Image.Image,
    contrast_factor: float = 1.8,
    sharpness_factor: float = 2.0,
    brightness_factor: float = 1.05,
    auto_levels: bool = True,
    normalize_lighting: bool = True,
) -> Image.Image:
    """
    Enhance paper sketch readability for vision models:
    - Reduces broad shadows and uneven lighting
    - Boosts ink stroke contrast
    - Sharpens faint pencil/pen edges while preserving colored annotations
    """
    image = _to_rgb(image)

    if normalize_lighting:
        image = _normalize_lighting(image)

    if auto_levels:
        ycbcr = image.convert("YCbCr")
        luminance, chroma_blue, chroma_red = ycbcr.split()
        luminance = ImageOps.autocontrast(luminance, cutoff=1)
        image = Image.merge("YCbCr", (luminance, chroma_blue, chroma_red)).convert("RGB")

    if brightness_factor != 1.0:
        image = ImageEnhance.Brightness(image).enhance(brightness_factor)

    if contrast_factor != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast_factor)

    if sharpness_factor != 1.0:
        image = ImageEnhance.Sharpness(image).enhance(sharpness_factor)

    return image


def image_to_base64(image: Image.Image, format: str = "JPEG") -> str:
    """Convert a PIL Image to a Base64-encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format=format, quality=90)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def image_to_bytes(image: Image.Image, format: str = "JPEG") -> bytes:
    """Convert a PIL Image to raw bytes."""
    buffered = io.BytesIO()
    image.save(buffered, format=format, quality=90)
    return buffered.getvalue()


def load_image_from_bytes(data: bytes) -> Image.Image:
    """Load a PIL Image from raw bytes."""
    with Image.open(io.BytesIO(data)) as image:
        return _to_rgb(image)


def enhance(image_bytes: bytes) -> bytes:
    """Enhance sketch photo: autocontrast, contrast, sharpness, and resize."""
    image = load_image_from_bytes(image_bytes)
    image = enhance_sketch(image)

    max_side = 1024
    try:
        import config
        max_side = getattr(config, "MAX_IMAGE_SIDE", 1024)
    except Exception:
        pass

    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    return image_to_bytes(image)
