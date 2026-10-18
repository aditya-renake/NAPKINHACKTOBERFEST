"""Image Preprocessor for Napkin2Code.

Enhances real-world webcam snapshots of paper napkins, whiteboards,
and notebook pages so that ink/pencil strokes stand out with maximum contrast
for local open-weight vision models.
"""

import io
import base64
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont


def enhance_sketch(
    image: Image.Image,
    contrast: float = 1.8,
    sharpness: float = 2.0,
    brightness: float = 1.05,
    auto_contrast: bool = True
) -> Image.Image:
    """Enhance paper sketch to reduce background noise, shadow, and boost ink lines."""
    # Convert to RGB if not already
    img = image.convert("RGB")
    
    # Auto contrast / level adjustment
    if auto_contrast:
        try:
            from PIL import ImageOps
            img = ImageOps.autocontrast(img, cutoff=2)
        except Exception:
            pass

    # Brightness adjustment
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)

    # Sharpness adjustment
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness)

    # Contrast adjustment
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)

    return img


def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Convert PIL image to base64 encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def generate_mock_sketch(annotated: bool = False) -> Image.Image:
    """Generates a synthetic hand-drawn napkin sketch for instant offline demo testing."""
    width, height = 700, 500
    # Creamy napkin paper color with slight texture
    img = Image.new("RGB", (width, height), color=(248, 246, 238))
    draw = ImageDraw.Draw(img)

    # Draw napkin border folds
    draw.rectangle([10, 10, width - 10, height - 10], outline=(225, 220, 205), width=2)
    
    # Blue ballpoint ink color
    ink_color = (25, 45, 90)

    # Main Card container
    draw.rounded_rectangle([70, 50, 630, 440], radius=15, outline=ink_color, width=4)

    # Header / Title sketch
    draw.rectangle([110, 80, 320, 110], outline=ink_color, width=2)
    draw.text((120, 85), "Product Launch Card", fill=ink_color)

    # Image placeholder with an X
    draw.rounded_rectangle([110, 130, 320, 300], radius=8, outline=ink_color, width=3)
    draw.line([110, 130, 320, 300], fill=ink_color, width=2)
    draw.line([110, 300, 320, 130], fill=ink_color, width=2)
    draw.text((170, 205), "[ Photo ]", fill=ink_color)

    # Description lines
    draw.line([360, 140, 590, 140], fill=ink_color, width=3)
    draw.line([360, 170, 570, 170], fill=ink_color, width=3)
    draw.line([360, 200, 520, 200], fill=ink_color, width=3)
    draw.text((360, 220), "Price: $49.00", fill=ink_color)

    # CTA Button
    draw.rounded_rectangle([360, 260, 550, 310], radius=10, fill=(35, 75, 140), outline=ink_color, width=3)
    draw.text((410, 275), "BUY NOW", fill=(255, 255, 255))

    # Features list
    draw.text((120, 340), "* Free 2-day delivery", fill=ink_color)
    draw.text((120, 370), "* 30-day money back guarantee", fill=ink_color)
    draw.text((120, 400), "* Open-source hardware", fill=ink_color)

    if annotated:
        # RED PEN ANNOTATIONS FOR ITERATIVE EDITING
        red_ink = (210, 25, 30)

        # Arrow pointing to the top right with Dark Mode note
        draw.arc([480, 50, 580, 120], start=180, end=350, fill=red_ink, width=4)
        draw.polygon([(580, 85), (595, 80), (585, 95)], fill=red_ink)
        draw.text((450, 40), "+ Add Dark Mode Switch", fill=red_ink)

        # Arrow pointing to price with Discount note
        draw.line([500, 225, 590, 225], fill=red_ink, width=3)
        draw.polygon([(490, 225), (505, 218), (505, 232)], fill=red_ink)
        draw.text((530, 235), "50% OFF badge!", fill=red_ink)

        # Star rating addition under the image
        draw.text((115, 312), "★★★★★ (128 reviews)", fill=red_ink)

    return img
