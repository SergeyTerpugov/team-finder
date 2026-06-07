import io
import os
import random

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from constants import constants_users as constant


def generate_avatar(instance):
    bg_color = random.choice(constant.AVATARS_COLORS)

    letter = instance.name[0].upper() if instance.name else instance.email[0].upper()

    img = Image.new('RGB', (constant.SIZE_AVATAR, constant.SIZE_AVATAR), bg_color)

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_from_static, constant.SIZE_FONT)
    bbox = draw.textbbox(constant.BBOX, letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (constant.SIZE_AVATAR - text_width) / 2 - bbox[0]
    y = (constant.SIZE_AVATAR - text_height) / 2 - bbox[1]
    draw.text((x, y), letter, fill=constant.AVATAR_LETTER_COLOR, font=font)

    buffer = io.BytesIO()
    img.save(buffer, format=constant.IMAGE_FORMAT)

    return ContentFile(buffer.getvalue(), f"avatar_{instance.email}.png")
