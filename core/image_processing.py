"""Image cleanup before sending to the vision model."""
import io
from PIL import Image, ImageEnhance, ImageOps
import config


def enhance(image_bytes: bytes) -> bytes:
    """Enhance sketch photo: autocontrast, contrast, sharpness, and resize."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = ImageOps.autocontrast(image)
    image = ImageEnhance.Contrast(image).enhance(1.5)
    image = ImageEnhance.Sharpness(image).enhance(2.0)

    image.thumbnail((config.MAX_IMAGE_SIDE, config.MAX_IMAGE_SIDE), Image.Resampling.LANCZOS)

    out = io.BytesIO()
    image.save(out, format="JPEG", quality=90)
    return out.getvalue()
