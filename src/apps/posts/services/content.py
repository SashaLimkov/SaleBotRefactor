import math

from PIL import Image, ImageFont, ImageDraw
import random

from apps.posts.models import Content


def create_content(file_name: str, file: bytes, type_content: int, to: str, to_id: int) -> Content:
    """Создает объект контента"""
    if to == 'compilation':
        content = Content.objects.create(type=type_content, compilation_id=to_id)
    elif to == 'final_compilation':
        content = Content.objects.create(type=type_content, final_compilation_id=to_id)
    else:
        content = Content.objects.create(type=type_content, post_id=to_id)
    content.file.save(file_name, file)
    content.save()
    return content


def update_or_create_content(file_name: str, file: bytes, type_content: int, to: str, to_id: int) -> Content:
    """Обновляет объект контента"""
    if to == 'compilation':
        content = Content.objects.update_or_create(compilation_id=to_id,
                                                   defaults={'type': type_content})
        print(content)
    elif to == 'final_compilation':
        content = Content.objects.update_or_create(final_compilation_id=to_id,
                                                   defaults={'type': type_content})
    else:
        content = Content.objects.update_or_create(post_id=to_id,
                                                   defaults={'type': type_content})
    content[0].file.save(file_name, file)
    content[0].save()
    return content


def watermark(img_post, img_wm, position, t_wm=" "):
    try:
        img_post_p = Image.open(img_post)
    except:
        return img_post
    if position == "center":
        pos = 1
    elif position == "fill":
        pos = 0
    else:
        return img_post
    if img_wm:
        img_wm = Image.open(img_wm)
        position = pos
        if position == 1:
            img_wm = img_wm.resize((img_post_p.size[0] // 2, img_post_p.size[1] // 2))
            if img_wm.mode != "RGBA":
                alpha = Image.new("L", img_wm.size, 255)
                img_wm.putalpha(alpha)

            paste_mask = img_wm.split()[3].point(lambda i: i * 45 / 100.0)
            img_post_p.paste(
                img_wm,
                (img_post_p.size[0] // 3, img_post_p.size[1] // 3),
                mask=paste_mask,
            )
        elif position == 2:
            img_wm = img_wm.resize((img_post_p.size[1] // 6, img_post_p.size[1] // 6))
            if img_wm.mode != "RGBA":
                alpha = Image.new("L", img_wm.size, 255)
                img_wm.putalpha(alpha)

            paste_mask = img_wm.split()[3].point(lambda i: i * 45 / 100.0)
            for x in range(5):
                for y in range(5):
                    img_post_p.paste(
                        img_wm,
                        (img_post_p.size[0] - x * 250, img_post_p.size[1] - y * 250),
                        mask=paste_mask,
                    )
    else:
        width, height = img_post_p.size
        message_length = len(t_wm)
        opacity = int(256 * 0.3)
        angle = math.degrees(math.atan(height / width))
        if pos == 1:
            FONT_RATIO = 2
            DIAGONAL_PERCENTAGE = 0.7
            diagonal_length = int(math.sqrt((width ** 2) + (height ** 2)))
            diagonal_to_use = diagonal_length * DIAGONAL_PERCENTAGE
            font_size = int(diagonal_to_use / (message_length / FONT_RATIO))
            font = ImageFont.truetype("static/fonts/bookmanoldstyle.ttf", font_size)
            mark_width, mark_height = font.getsize(t_wm)
            watermark = Image.new("RGBA", (mark_width, mark_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            draw.text((0, 0), text=t_wm, font=font, fill=(0, 0, 0, opacity))
            watermark = watermark.rotate(angle, expand=True)
            wx, wy = watermark.size
            px = int((width - wx) / 2)
            py = int((height - wy) / 2)
            img_post_p.paste(watermark, (px, py, px + wx, py + wy), watermark)
        else:
            font_size = 70
            font = ImageFont.truetype("static/fonts/bookmanoldstyle.ttf", font_size)
            mark_width, mark_height = font.getsize(t_wm)
            watermark = Image.new("RGBA", (mark_width, mark_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            draw.text((0, 0), text=t_wm, font=font, fill=(0, 0, 0, opacity))
            watermark = watermark.rotate(angle, expand=True)
            wx, wy = watermark.size
            for x in range(4):
                for y in range(4):
                    px = int(width - x * 450) - 250
                    py = int(height - y * 550) - 150
                    img_post_p.paste(watermark, (px, py, px + wx, py + wy), watermark)

    file_name, file_format = img_post.split("/")[-1].split('.')
    path = f'{file_name}_{random.randint(100000, 9999999)}.{file_format}'
    img_post_p.save(path)
    return path
