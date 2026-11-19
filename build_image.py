#!/usr/bin/env python3
"""Draw the news-image-20261119 artwork: a one-page newspaper front page
summing up Thursday 19 November 2026 in four stories.

Stories (all first reported / developed on 19 Nov 2026, sources: BBC,
Reuters, AP, The Guardian):
  1. Grand Theft Auto VI begins its global rollout; after a 13-year wait,
     Vice City returns as the launch starts worldwide.
  2. US-Iran exchange of fire widens across the Gulf: Iran hits a US base
     in Kuwait and strikes Bahrain again; the US sends a third carrier.
  3. Trump, Xi and Putin are to hold trilateral talks in Shenzhen during
     the APEC summit.
  4. NASA's Voyager 1 reaches one light-day from Earth, nearly 50 years
     after launch; NASA confirms the milestone on 19 November.
Ticker: EU proposes a 45bn euro Ukraine loan; Fed minutes point to
further rate hikes.

Drawn flat at 3x supersampling (3072x3072) and downscaled to 1024x1024.
Run: python3 build_image.py  ->  writes entry.png next to this script.
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 3  # supersampling factor
W, H = 1024, 1024

PAPER = (246, 241, 227)
NAVY = (22, 35, 63)
NAVY_LIGHT = (46, 64, 87)
GOLD = (217, 164, 65)
INK = (30, 30, 34)
GREY = (90, 100, 114)
WHITE = (255, 255, 255)
RED = (176, 58, 46)
TEAL = (23, 126, 118)
TEAL_DARK = (16, 90, 86)
SKY_PALE = (207, 232, 228)
GREEN = (118, 185, 0)
GREEN_DARK = (30, 122, 52)
ORANGE = (255, 140, 60)
SUNSET_PINK = (238, 130, 150)
PURPLE = (120, 80, 150)
PURPLE_DARK = (70, 50, 110)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * S)


def X(v):
    return v * S


def box(d, x0, y0, x1, y1, fill):
    d.rectangle([X(x0), X(y0), X(x1), X(y1)], fill=fill)


def rbox(d, x0, y0, x1, y1, r, fill):
    d.rounded_rectangle([X(x0), X(y0), X(x1), X(y1)], radius=X(r), fill=fill)


def poly(d, pts, fill):
    d.polygon([(X(x), X(y)) for x, y in pts], fill=fill)


def line(d, pts, fill, width=1):
    d.line([(X(x), X(y)) for x, y in pts], fill=fill, width=X(width))


def ell(d, x0, y0, x1, y1, fill):
    d.ellipse([X(x0), X(y0), X(x1), X(y1)], fill=fill)


def text(d, x, y, s, f, fill, anchor="la"):
    d.text((X(x), X(y)), s, font=f, fill=fill, anchor=anchor)


def draw_tracked(d, cx, y, s, path, size, fill, tracking=3):
    """Centred text with letter-spacing (tracking in 1024-space px)."""
    f = font(path, size)
    widths = [d.textlength(ch, font=f) // S for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        d.text((X(x), X(y)), ch, font=f, fill=fill)
        x += w + tracking


def wrap(d, s, path, size, max_w):
    """Greedy word wrap; returns list of lines fitting max_w (1024-space)."""
    f = font(path, size)
    words = s.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) / S <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(cx, cy, r_out, r_in, fill, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
box(d, 0, 0, W, 132, NAVY)
draw_tracked(d, W // 2, 22, "THE WORLD IN ONE PICTURE", FONT_BOLD, 25, GOLD, tracking=6)
f_date = font(FONT_BOLD, 54)
d.text((X(W // 2), X(56)), "THURSDAY 19 NOVEMBER 2026", font=f_date, fill=WHITE, anchor="ma")
box(d, 0, 128, W, 132, GOLD)

# ---------------------------------------------------------------- kicker
draw_tracked(d, W // 2, 146, "FOUR STORIES THAT DEFINED THE DAY", FONT_BOLD, 24, NAVY, tracking=4)

# ---------------------------------------------------------------- panels
PANELS = [
    # (x, y, headline, sub, draw_fn)
    (28, 188, "GTA VI ROLLS OUT WORLDWIDE",
     "Vice City returns after 13 years"),
    (528, 188, "IRAN HITS US BASE IN KUWAIT",
     "Bahrain hit again; third carrier sent"),
    (28, 568, "TRUMP, XI AND PUTIN TO MEET",
     "Trilateral talks in Shenzhen at APEC"),
    (528, 568, "VOYAGER 1, ONE LIGHT-DAY OUT",
     "NASA probe's milestone after 50 years"),
]
PW, PH, ILL_H = 468, 360, 200



def draw_gta(d, x0, y0):
    # Vice City sunset: orange -> pink -> purple bands, big sun
    box(d, x0, y0, x0 + PW, y0 + 62, (255, 166, 77))
    box(d, x0, y0 + 62, x0 + PW, y0 + 112, SUNSET_PINK)
    box(d, x0, y0 + 112, x0 + PW, y0 + 160, PURPLE)
    box(d, x0, y0 + 160, x0 + PW, y0 + ILL_H, PURPLE_DARK)
    # sun with VI on it
    sx, sy = x0 + 234, y0 + 72
    ell(d, sx - 40, sy - 40, sx + 40, sy + 40, (255, 220, 120))
    ell(d, sx - 28, sy - 28, sx + 28, sy + 28, (255, 236, 170))
    f_vi = font(FONT_BOLD, 40)
    d.text((X(sx), X(sy - 4)), "VI", font=f_vi, fill=(90, 50, 110), anchor="ma")
    # skyline silhouettes along the bottom
    for bx, bw, bh in [(0, 46, 52), (52, 34, 78), (92, 58, 44), (156, 30, 66),
                       (192, 52, 40), (330, 40, 58), (376, 30, 84), (412, 56, 48)]:
        box(d, x0 + bx, y0 + 200 - bh, x0 + bx + bw, y0 + 200, (40, 28, 70))
    # lit windows on the skyline
    for wx, wy in [(12, 158), (30, 172), (64, 140), (104, 168), (122, 156),
                   (166, 150), (204, 172), (342, 156), (386, 132), (424, 162)]:
        box(d, x0 + wx, y0 + wy, x0 + wx + 7, y0 + wy + 9, GOLD)
    # palm trees, left and right: trunk leaning out, fronds drooping down
    for px, lean in [(60, 1), (420, -1)]:
        tx, ty = x0 + px, y0 + 200
        line(d, [(tx, ty), (tx + lean * 14, ty - 62)], (60, 40, 26), 7)
        cx, cy = tx + lean * 14, ty - 62
        for dx, dy in [(-30, -16), (-16, -22), (0, -24), (16, -22), (30, -16)]:
            mx, my = cx + lean * dx * 0.6, cy + dy * 0.6
            ex, ey = cx + lean * dx, cy + dy + 14
            line(d, [(cx, cy), (mx, my), (ex, ey)], (30, 122, 52), 4)
    # OUT NOW tag, top-right
    rbox(d, x0 + 316, y0 + 14, x0 + 456, y0 + 48, 8, RED)
    f_tag = font(FONT_BOLD, 18)
    d.text((X(x0 + 386), X(y0 + 19)), "OUT NOW", font=f_tag, fill=WHITE, anchor="ma")


def draw_gulf(d, x0, y0):
    # night sky over the Gulf, stars, dark sea
    box(d, x0, y0, x0 + PW, y0 + 130, (10, 20, 46))
    for sx, sy, r in [(40, 24, 2), (120, 44, 2), (210, 18, 3), (300, 30, 2),
                      (380, 52, 2), (440, 20, 2), (70, 80, 2), (250, 70, 2),
                      (420, 90, 3), (330, 12, 2), (160, 100, 2)]:
        ell(d, x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r, (200, 205, 220))
    # crescent moon, top-left
    ell(d, x0 + 24, y0 + 14, x0 + 52, y0 + 42, (240, 238, 220))
    ell(d, x0 + 34, y0 + 12, x0 + 58, y0 + 40, (10, 20, 46))
    box(d, x0, y0 + 130, x0 + PW, y0 + ILL_H, (18, 64, 86))
    for wy in (150, 172, 192):
        for wx in range(0, PW, 52):
            d.arc([X(x0 + wx), X(y0 + wy), X(x0 + wx + 40), X(y0 + wy + 18)],
                  start=180, end=360, fill=(120, 170, 185), width=X(3))
    # aircraft carrier, centre
    hx0, hx1 = x0 + 90, x0 + 380
    poly(d, [(hx0, y0 + 166), (hx1, y0 + 166), (hx1 - 20, y0 + 192),
             (hx0 + 20, y0 + 192)], (90, 92, 96))
    box(d, hx0 + 8, y0 + 160, hx1 - 8, y0 + 168, (60, 62, 66))
    # island tower + mast
    box(d, x0 + 296, y0 + 132, x0 + 326, y0 + 162, (70, 72, 76))
    line(d, [(x0 + 311, y0 + 132), (x0 + 311, y0 + 112)], (70, 72, 76), 4)
    ell(d, x0 + 308, y0 + 108, x0 + 314, y0 + 114, RED)
    # two missile trails arcing down from the top-right
    for (mx0, my0, mx1, my1) in [(430, 8, 330, 96), (452, 34, 372, 108)]:
        line(d, [(x0 + mx0, y0 + my0), (x0 + mx1, y0 + my1)], (255, 176, 66), 4)
        ell(d, x0 + mx1 - 5, y0 + my1 - 5, x0 + mx1 + 5, y0 + my1 + 5, (255, 120, 40))
    # interception burst above the carrier deck
    bx, by = x0 + 250, y0 + 96
    ell(d, bx - 22, by - 22, bx + 22, by + 22, (255, 176, 66))
    ell(d, bx - 12, by - 12, bx + 12, by + 12, (255, 224, 150))
    poly(d, star(bx, by, 26, 10, (255, 140, 0)), (255, 140, 0))


def draw_summit(d, x0, y0):
    box(d, x0, y0, x0 + PW, y0 + ILL_H, (220, 233, 245))
    # Shenzhen towers in the background
    for tx, tw, th in [(16, 44, 96), (72, 30, 128), (112, 52, 80),
                       (340, 40, 110), (392, 34, 72), (436, 26, 96)]:
        box(d, x0 + tx, y0 + 178 - th, x0 + tx + tw, y0 + 178, NAVY_LIGHT)
    for wx, wy in [(28, 96), (44, 116), (82, 70), (126, 112), (352, 84), (404, 116)]:
        box(d, x0 + wx, y0 + wy, x0 + wx + 7, y0 + wy + 9, GOLD)
    box(d, x0, y0 + 178, x0 + PW, y0 + ILL_H, (232, 220, 192))
    # red carpet strip along the bottom
    box(d, x0, y0 + 186, x0 + PW, y0 + ILL_H, RED)
    box(d, x0, y0 + 186, x0 + PW, y0 + 190, GOLD)
    # flag poles
    for px in (52, 204, 356):
        line(d, [(x0 + px, y0 + 22), (x0 + px, y0 + 186)], (60, 60, 66), 4)
        ell(d, x0 + px - 5, y0 + 14, x0 + px + 5, y0 + 24, GOLD)
    # US flag
    fx, fy = x0 + 56, y0 + 26
    for i in range(7):
        box(d, fx, fy + i * 9, fx + 96, fy + i * 9 + 9,
            RED if i % 2 == 0 else WHITE)
    box(d, fx, fy, fx + 40, fy + 36, (30, 50, 110))
    for r in range(3):
        for c in range(4):
            ell(d, fx + 5 + c * 9, fy + 5 + r * 11, fx + 10 + c * 9, fy + 10 + r * 11, WHITE)
    # China flag
    fx = x0 + 208
    box(d, fx, fy, fx + 96, fy + 63, (222, 41, 16))
    poly(d, star(fx + 20, fy + 18, 12, 5, GOLD), GOLD)
    for sx, sy in [(44, 10), (52, 20), (52, 32), (44, 42)]:
        poly(d, star(fx + sx, fy + sy, 5, 2, GOLD), GOLD)
    # Russia flag
    fx = x0 + 360
    box(d, fx, fy, fx + 96, fy + 21, WHITE)
    box(d, fx, fy + 21, fx + 96, fy + 42, (0, 57, 166))
    box(d, fx, fy + 42, fx + 96, fy + 63, (213, 0, 50))


def draw_voyager(d, x0, y0):
    # deep space, starfield
    box(d, x0, y0, x0 + PW, y0 + ILL_H, (8, 10, 24))
    for sx, sy, r in [(36, 30, 2), (90, 66, 2), (150, 22, 3), (210, 90, 2),
                      (260, 40, 2), (330, 26, 3), (400, 70, 2), (446, 30, 2),
                      (60, 120, 2), (180, 150, 2), (300, 130, 3), (420, 150, 2),
                      (120, 176, 2), (240, 176, 2), (380, 182, 2)]:
        ell(d, x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r, WHITE)
    # Earth, small, bottom-left
    ex, ey = x0 + 74, y0 + 158
    ell(d, ex - 30, ey - 30, ex + 30, ey + 30, (46, 110, 200))
    ell(d, ex - 18, ey - 8, ex + 2, ey + 6, (60, 160, 90))
    ell(d, ex + 4, ey + 8, ex + 18, ey + 20, (60, 160, 90))
    d.arc([X(ex - 30), X(ey - 30), X(ex + 30), X(ey + 30)], start=200, end=340,
          fill=(200, 220, 245), width=X(3))
    # Voyager probe: gold body, white dish, boom antenna
    bx0, by0, bx1, by1 = x0 + 268, y0 + 66, x0 + 336, y0 + 118
    rbox(d, bx0, by0, bx1, by1, 8, (201, 162, 39))
    box(d, bx0 + 12, by0 + 12, bx1 - 12, by1 - 12, (150, 116, 28))
    # dish: white half-ellipse (parabola) opening to the upper right
    d.pieslice([X(x0 + 330), X(y0 + 52), X(x0 + 396), X(y0 + 118)],
               start=270, end=90, fill=WHITE)
    d.arc([X(x0 + 330), X(y0 + 52), X(x0 + 396), X(y0 + 118)], start=270, end=90,
          fill=(180, 184, 190), width=X(3))
    line(d, [(x0 + 336, y0 + 92), (x0 + 363, y0 + 85)], (180, 184, 190), 4)
    # boom antenna to the lower left
    line(d, [(x0 + 268, y0 + 100), (x0 + 210, y0 + 132)], (180, 184, 190), 4)
    ell(d, x0 + 204, y0 + 126, x0 + 216, y0 + 138, GOLD)
    # signal arcs beaming from the dish toward Earth
    for r in (66, 92, 118):
        d.arc([X(x0 + 363 - r), X(y0 + 85 - r), X(x0 + 363 + r), X(y0 + 85 + r)],
              start=150, end=250, fill=(140, 200, 235), width=X(3))
    # ONE LIGHT-DAY tag, top-right
    rbox(d, x0 + 296, y0 + 14, x0 + 456, y0 + 48, 8, NAVY)
    f_tag = font(FONT_BOLD, 18)
    d.text((X(x0 + 376), X(y0 + 19)), "1 LIGHT-DAY", font=f_tag, fill=WHITE, anchor="ma")



DRAW = [draw_gta, draw_gulf, draw_summit, draw_voyager]

for (px, py, headline, sub), draw_fn in zip(PANELS, DRAW):
    box(d, px, py, px + PW, py + PH, WHITE)
    d.rectangle([X(px), X(py), X(px + PW), X(py + PH)], outline=NAVY, width=X(2))
    draw_fn(d, px + 2, py + 2)
    # headline + sub (panel interior is 360 tall: illustration 200,
    # up to 2 headline lines + up to 2 sub lines must fit below it)
    f_head = font(FONT_BOLD, 36)
    head_lines = wrap(d, headline, FONT_BOLD, 36, PW - 36)
    hy = py + ILL_H + 14
    for ln in head_lines:
        d.text((X(px + 18), X(hy)), ln, font=f_head, fill=NAVY)
        hy += 40
    f_sub = font(FONT_REG, 22)
    for ln in wrap(d, sub, FONT_REG, 22, PW - 36):
        d.text((X(px + 18), X(hy + 4)), ln, font=f_sub, fill=GREY)
        hy += 27

# ---------------------------------------------------------------- footer
box(d, 28, 930, W - 28, 932, (200, 190, 160))
f_tick = font(FONT_BOLD, 20)
d.text((X(W // 2), X(938)),
       "ALSO: EU proposes \u20ac45bn Ukraine loan \u00b7 Fed minutes point to more rate hikes",
       font=f_tick, fill=NAVY, anchor="ma")
f_src = font(FONT_REG, 21)
d.text((X(W // 2), X(964)), "Sources: BBC \u00b7 Reuters \u00b7 AP \u00b7 The Guardian  \u2014  as reported on 19 November 2026",
       font=f_src, fill=GREY, anchor="ma")

out = img.resize((W, H), Image.LANCZOS)
out.save("entry.png", optimize=True)
print("wrote entry.png", out.size, len(open("entry.png", "rb").read()), "bytes")
