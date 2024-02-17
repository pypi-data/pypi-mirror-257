from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from .model import HonorWinOrLooseDetail


def draw(info: HonorWinOrLooseDetail, honor_name: str):
    header = ["全分段", "1350", "高星局", "顶端局"]
    data = [info.banRate, info.pickRate, info.bpRate, info.winRate]
    row_names = [honor_name, "禁用率%", "出场率%", "禁选率%", "胜率%"]
    img = Image.new("RGB", (750, 500), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("msyh.ttc", size=22)
    for i in range(6):
        draw.line((0, 100 * i, 750, 100 * i), fill="black")
    for i in range(6):
        draw.line((150 * i, 0, 150 * i, 500), fill="black")
    for i, name in enumerate(row_names):
        bbox = draw.textbbox((0, 0), name, font=font)
        draw.text(
            (
                75 - (bbox[2] - bbox[0]) / 2 - bbox[0],
                50 + i * 100 - (bbox[3] - bbox[1]) / 2 - bbox[1],
            ),
            name,
            fill=0,
            font=font,
        )
    for i, name in enumerate(header):
        bbox = draw.textbbox((0, 0), name, font=font)
        draw.text(
            (
                225 + i * 150 - (bbox[2] - bbox[0]) / 2 - bbox[0],
                50 - (bbox[3] - bbox[1]) / 2 - bbox[1],
            ),
            name,
            fill=0,
            font=font,
        )
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            if value != "":
                bbox = draw.textbbox((0, 0), value, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                draw.text(
                    (
                        150 + j * 150 + (150 - text_width) / 2 - bbox[0],
                        100 + i * 100 + (100 - text_height) / 2 - bbox[1],
                    ),
                    value,
                    fill=0,
                    font=font,
                )
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    return img_buffer.getvalue()
