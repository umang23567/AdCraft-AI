from PIL import Image, ImageDraw, ImageFont, ImageColor
import textwrap
import numpy as np

def center_crop(image, size=(1080, 1080)):
    width, height = image.size
    new_width, new_height = size
    if width < new_width or height < new_height:
        scale = max(new_width / width, new_height / height)
        image = image.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)
        width, height = image.size
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    return image.crop((left, top, left + new_width, top + new_height))

def gen_solid_bg(color):
    color = ImageColor.getrgb(color)
    return Image.new("RGB", (1080, 1080), color)

def gen_grad_bg(start_color, end_color, direction):
    start_color = ImageColor.getrgb(start_color)
    end_color = ImageColor.getrgb(end_color)
    img = Image.new("RGB", (1080, 1080))
    draw = ImageDraw.Draw(img)
    for y in range(1080):
        for x in range(1080):
            ratio = {
                "Vertical": y / 1080,
                "Horizontal": x / 1080,
                "Diagonal": (x + y) / (2 * 1080)
            }.get(direction, 0)
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.point((x, y), fill=(r, g, b))
    return img

def process_bg(img):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    elif not isinstance(img, Image.Image):
        img = Image.open(img)
    return center_crop(img).convert("RGB")

def wrap_text_by_width(text, font, max_pixel_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if font.getlength(test_line) <= max_pixel_width:
            line = test_line
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def measure_block_height(text, font, max_pixel_width, line_spacing=15, block_spacing=30):
    if not text:
        return 0
    lines = wrap_text_by_width(text, font, max_pixel_width)
    return sum(font.getbbox(line)[3] - font.getbbox(line)[1] + line_spacing for line in lines) - line_spacing + block_spacing

def draw_text_block(draw, text, font, max_pixel_width, y_offset, img_width, margin=50, fill=(0, 0, 0), center_align=False, line_spacing=15, block_spacing=30):
    if not text:
        return y_offset
    lines = wrap_text_by_width(text, font, max_pixel_width)
    for line in lines:
        line_width = font.getlength(line)
        x = (img_width - line_width) // 2 if center_align else margin
        draw.text((x, y_offset), line, font=font, fill=fill)
        y_offset += font.getbbox(line)[3] - font.getbbox(line)[1] + line_spacing
    return y_offset + block_spacing

def get_fitting_font_size(text_blocks, font_path, max_width, max_height, max_font_size=60, min_font_size=20, step=2, line_spacing=15, block_spacing=30):
    for size in range(max_font_size, min_font_size - 1, -step):
        total_height = 0
        for text, is_subhead in text_blocks:
            font = ImageFont.truetype(font_path, size if not is_subhead else int(size * 1.2))
            lines = wrap_text_by_width(text, font, max_width)
            if not lines:
                continue
            block_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] + line_spacing for line in lines) - line_spacing + block_spacing
            total_height += block_height
        if total_height <= max_height:
            return size
    return min_font_size

from PIL import Image, ImageDraw, ImageFont, ImageColor
import textwrap
import numpy as np

def overlay_txt(ad, img, fill, font_path,
                spacing_above_middle=-10, spacing_below_middle=30,
                contact_spacing=5):
    
    fill = ImageColor.getrgb(fill)

    # Extract ad fields
    company_name = ad.get("company_name", "")
    headline = ad.get("headline", "")
    text = ad.get("text", "")
    call_to_action = ad.get("call_to_action", "")
    hashtags = " ".join(ad.get("hashtags", []))
    location = ad.get("location", "")
    phone = ad.get("phone", "")
    email = ad.get("email", "")
    website = ad.get("website", "")

    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size

    # Fonts
    company_font = ImageFont.truetype(font_path, size=50)
    headline_font = ImageFont.truetype(font_path, size=70)
    body_font = ImageFont.truetype(font_path, size=45)  # slightly smaller
    fixed_small_font = ImageFont.truetype(font_path, size=40)
    contact_font = ImageFont.truetype(font_path, size=28)

    margin = 50
    bottom_margin = 40
    line_spacing = 10
    block_spacing = 25

    def wrap_text(text, font, max_pixel_width):
        words = text.split()
        lines, line = [], ""
        for word in words:
            test_line = f"{line} {word}".strip()
            if font.getlength(test_line) <= max_pixel_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def measure_block_height(text, font, max_pixel_width, spacing=line_spacing):
        if not text:
            return 0
        lines = wrap_text(text, font, max_pixel_width)
        return sum(font.getbbox(line)[3] - font.getbbox(line)[1] + spacing for line in lines) - spacing + block_spacing

    def draw_text_block(text, font, max_pixel_width, y_offset,
                        center_align=False, spacing=line_spacing):
        if not text:
            return y_offset
        lines = wrap_text(text, font, max_pixel_width)
        for line in lines:
            line_width = font.getlength(line)
            draw_x = (img_width - line_width) // 2 if center_align else margin
            line_height = font.getbbox(line)[3] - font.getbbox(line)[1]
            draw.text((draw_x, y_offset), line, font=font, fill=fill)
            y_offset += line_height + spacing
        return y_offset + block_spacing

    max_width = img_width - 2 * margin

    # 1. Top - Company Name
    y_top = draw_text_block(company_name, company_font, max_width, margin, center_align=False)

    # 2. Bottom - Contact Info
    contact_blocks = [
        ("We are located at " + location, contact_font),
        ("Contact us at " + phone + " or " + email, contact_font),
        ("Visit us: " + website, contact_font),
    ]
    contact_height = sum(
        measure_block_height(text, font, max_width, spacing=contact_spacing)
        for text, font in contact_blocks
    )

    # 3. Middle Block - Headline + Body + CTA + Hashtags
    middle_blocks = [
        (headline, headline_font),
        (text, body_font),
        (call_to_action, fixed_small_font),
        (hashtags, fixed_small_font),
    ]
    middle_height = sum(
        measure_block_height(text, font, max_width)
        for text, font in middle_blocks
    )

    # 4. Y Start for Middle Block
    y_middle_start = y_top + spacing_above_middle + \
        (img_height - y_top - contact_height - bottom_margin -
         spacing_above_middle - spacing_below_middle - middle_height) // 2

    # 5. Draw Middle
    y_middle = y_middle_start
    for text, font in middle_blocks:
        y_middle = draw_text_block(text, font, max_width, y_middle, center_align=True)

    # 6. Draw Contact Info at Bottom
    y_contact = img_height - contact_height - bottom_margin
    for text, font in contact_blocks:
        y_contact = draw_text_block(text, font, max_width, y_contact, center_align=False, spacing=contact_spacing)

    return img
