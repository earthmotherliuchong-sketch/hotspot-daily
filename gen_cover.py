#!/usr/bin/env python3
"""Generate og-cover.png for the hotspot daily report."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630

# Warm gradient background (dark red to warm orange)
img = Image.new('RGB', (W, H), '#1a1a2e')
draw = ImageDraw.Draw(img)

# Create gradient
for y in range(H):
    r = int(26 + (180 - 26) * y / H)
    g = int(26 + (60 - 26) * y / H)
    b = int(46 + (50 - 46) * y / H)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Add decorative circles
for cx, cy, radius, alpha in [(100, 500, 200, 15), (1050, 80, 150, 20), (600, 320, 300, 8)]:
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=(255, 140, 60, alpha))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

# Try to load fonts
font_paths = [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/Library/Fonts/Arial Unicode.ttf',
]

def get_font(size):
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()

font_title = get_font(52)
font_sub = get_font(28)
font_date = get_font(36)

# Title
title = "热点流量日报"
subtitle = "装修建材 · 环保材料 · 暖通空调 · 节能环保"
date_text = "2026-08-13"

# Draw title
bbox = draw.textbbox((0, 0), title, font=font_title)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) / 2, 180), title, fill='white', font=font_title)

# Draw subtitle
bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
sw = bbox2[2] - bbox2[0]
draw.text(((W - sw) / 2, 270), subtitle, fill=(255, 200, 150), font=font_sub)

# Draw date
bbox3 = draw.textbbox((0, 0), date_text, font=font_date)
dw = bbox3[2] - bbox3[0]
draw.text(((W - dw) / 2, 350), date_text, fill=(255, 230, 200), font=font_date)

# Draw decorative line
draw.line([(300, 430), (900, 430)], fill=(255, 140, 60), width=3)

# Footer text
footer = "每日精选高流量话题 · 筛选行业关联内容"
font_footer = get_font(22)
bbox4 = draw.textbbox((0, 0), footer, font=font_footer)
fw = bbox4[2] - bbox4[0]
draw.text(((W - fw) / 2, 470), footer, fill=(200, 180, 160), font=font_footer)

# Tags
tags = ["#社会热点", "#行业资讯", "#技术趋势", "#国际视野", "#流量钩子"]
font_tag = get_font(18)
x_start = 250
for i, tag in enumerate(tags):
    bbox5 = draw.textbbox((0, 0), tag, font=font_tag)
    tw5 = bbox5[2] - bbox5[0]
    draw.text((x_start + i * 150, 530), tag, fill=(255, 160, 100), font=font_tag)

img.save('/Users/liuchong/WorkBuddy/自动化任务/hotspot-daily/og-cover.png', 'PNG')
print("og-cover.png generated successfully")
