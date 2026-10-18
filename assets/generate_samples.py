"""
Generate sample hand-drawn napkin/sketch mockups for quick testing and judge demos.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets/samples", exist_ok=True)

def create_paper_texture(width=700, height=700, bg_color=(248, 246, 240)):
    """Create a realistic notebook/paper texture."""
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Add subtle grid lines like a graph notebook
    grid_color = (230, 235, 245)
    for x in range(0, width, 25):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 25):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    return img, draw

def draw_hand_line(draw, points, color=(40, 50, 70), width=3):
    """Draw a slightly wobbly hand-drawn line."""
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

def draw_hand_rect(draw, x1, y1, x2, y2, color=(40, 50, 70), width=3):
    """Draw a hand-drawn rectangle."""
    draw_hand_line(draw, [(x1, y1), (x2+2, y1-1), (x2, y2+2), (x1-1, y2), (x1, y1)], color=color, width=width)

def generate_samples():
    # 1. Base Product Card Sketch
    img1, draw1 = create_paper_texture()
    ink_color = (35, 45, 60)

    # Outer Card box
    draw_hand_rect(draw1, 120, 100, 580, 600, color=ink_color, width=4)

    # Header / Logo
    draw1.text((150, 120), "[*] RetroStore UI", fill=ink_color)

    # Image placeholder box with cross
    draw_hand_rect(draw1, 160, 160, 540, 360, color=ink_color, width=3)
    draw1.line([(160, 160), (540, 360)], fill=(150, 160, 180), width=2)
    draw1.line([(160, 360), (540, 160)], fill=(150, 160, 180), width=2)
    draw1.text((310, 250), "[ IMAGE ]", fill=(100, 110, 130))

    # Product Title & Price
    draw1.text((160, 385), "Vintage 35mm Film Camera", fill=ink_color)
    draw1.text((160, 420), "$ 45.00  |  In Stock", fill=(60, 70, 90))

    # Star rating sketch
    draw1.text((160, 455), "★ ★ ★ ★ ☆ (4.2)", fill=(180, 140, 20))

    # Quantity Selector
    draw_hand_rect(draw1, 160, 495, 270, 540, color=ink_color, width=2)
    draw1.text((175, 510), " -  1  + ", fill=ink_color)

    # Buy Button
    draw_hand_rect(draw1, 300, 490, 540, 545, color=ink_color, width=4)
    draw1.text((360, 508), ">> BUY NOW <<", fill=ink_color)

    img1.save("assets/samples/sample_product_card.png")
    print("Saved sample_product_card.png")

    # 2. Iterated Sketch with Red Pen Scribbles
    img2, draw2 = create_paper_texture()
    # Draw original elements
    draw_hand_rect(draw2, 120, 100, 580, 600, color=ink_color, width=4)
    draw2.text((150, 120), "[*] RetroStore UI", fill=ink_color)
    draw_hand_rect(draw2, 160, 160, 540, 360, color=ink_color, width=3)
    draw2.line([(160, 160), (540, 360)], fill=(150, 160, 180), width=2)
    draw2.line([(160, 360), (540, 160)], fill=(150, 160, 180), width=2)
    draw2.text((310, 250), "[ IMAGE ]", fill=(100, 110, 130))
    draw2.text((160, 385), "Vintage 35mm Film Camera", fill=ink_color)
    draw2.text((160, 420), "$ 45.00  |  In Stock", fill=(60, 70, 90))
    draw2.text((160, 455), "★ ★ ★ ★ ☆ (4.2)", fill=(180, 140, 20))
    draw_hand_rect(draw2, 160, 495, 270, 540, color=ink_color, width=2)
    draw2.text((175, 510), " -  1  + ", fill=ink_color)
    draw_hand_rect(draw2, 300, 490, 540, 545, color=ink_color, width=4)
    draw2.text((360, 508), ">> BUY NOW <<", fill=ink_color)

    # RED PEN PHYSICAL ANNOTATIONS:
    red_ink = (210, 35, 45)
    # Dark mode toggle annotation top right
    draw_hand_line(draw2, [(470, 130), (530, 130), (530, 110)], color=red_ink, width=3)
    draw2.text((360, 70), "arrow -> + Add Dark Mode Toggle (Moon icon)", fill=red_ink)
    draw_hand_line(draw2, [(440, 90), (510, 120)], color=red_ink, width=2)

    # Scribble over price with discount
    draw2.line([(160, 430), (220, 430)], fill=red_ink, width=3)
    draw2.text((230, 420), "$35.00 (20% OFF SALE!)", fill=red_ink)

    # Sticky Note / Arrow at bottom
    draw_hand_rect(draw2, 280, 555, 560, 595, color=red_ink, width=2)
    draw2.text((290, 568), "+ Add 'Free Express Shipping' Badge", fill=red_ink)

    img2.save("assets/samples/sample_product_card_iterated.png")
    print("Saved sample_product_card_iterated.png")

if __name__ == "__main__":
    generate_samples()
