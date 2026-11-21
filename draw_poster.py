"""Draw AURMARA - The Harbour of Golden Stairs (poster v7).

From the v6 poster that jumped to 70.10%: same warm coastal town, grand
staircase, cafe terrace, small golden clock tower. Four small touches
only: (1) fine paint grain over the sky and sea, (2) warm bunting flags
strung across the cafe terrace, (3) two extra sailboats plus small birds
in the sky, (4) a longer sun reflection path on the sea. No composition
change, no clock tower change, no name shadow, no new subtitle, no dense
town. Drawn with Pillow at build time; main.py only copies it.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
OUT = "/home/hatch/workspace/poster-v7-build/poster.png"
random.seed(20261121)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def blend(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_band(img, y0, y1, stops):
    """Paint a vertical gradient between (pos 0..1, rgb) stops."""
    d = ImageDraw.Draw(img)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                tt = (t - p0) / max(1e-6, p1 - p0)
                d.line([(0, y), (W, y)], fill=blend(c0, c1, tt))
                break


def lettered(d, cx, y, s, font, fill, spacing=6, shadow=None):
    widths = [d.textlength(ch, font=font) for ch in s]
    total = sum(widths) + spacing * (len(s) - 1)
    x = cx - total / 2
    for ch, wch in zip(s, widths):
        if shadow:
            d.text((x + shadow[0], y + shadow[1]), ch, font=font, fill=shadow[2])
        d.text((x, y), ch, font=font, fill=fill)
        x += wch + spacing


def paint_sky(img):
    sky_band(img, 0, 560, [
        (0.0, (28, 52, 96)),
        (0.35, (78, 92, 134)),
        (0.55, (232, 130, 58)),
        (0.75, (250, 184, 96)),
        (1.0, (253, 218, 155)),
    ])


def paint_sea(img):
    sky_band(img, 560, 800, [
        (0.0, (250, 196, 120)),
        (0.15, (56, 138, 150)),
        (0.6, (30, 104, 122)),
        (1.0, (22, 82, 100)),
    ])


def paint_terrace(img):
    sky_band(img, 800, 1024, [
        (0.0, (232, 196, 148)),
        (1.0, (198, 152, 104)),
    ])


def paint_grain(d):
    # v7 touch 1: fine paint grain over sky and sea, warm light speckle.
    for _ in range(2600):
        x = random.randint(0, W - 1)
        y = random.randint(0, 799)
        warm = random.random() < 0.5
        col = (255, 226, 170, 26) if warm else (20, 30, 60, 22)
        d.ellipse([x, y, x + 1, y + 1], fill=col)
    # a few soft brush dabs in the sky
    for _ in range(60):
        x = random.randint(40, W - 40)
        y = random.randint(60, 500)
        r = random.randint(6, 18)
        col = (255, 210, 140, 14) if random.random() < 0.6 else (90, 70, 110, 12)
        d.ellipse([x - r, y - r // 2, x + r, y + r // 2], fill=col)


def paint_sun(d, sun_c):
    # stronger glow halos around the sun
    for r, a in [(230, 55), (185, 75), (140, 110)]:
        d.ellipse([sun_c[0] - r, sun_c[1] - r, sun_c[0] + r, sun_c[1] + r],
                  fill=(255, 214, 130, a))
    d.ellipse([sun_c[0] - 78, sun_c[1] - 78, sun_c[0] + 78, sun_c[1] + 78],
              fill=(255, 233, 168, 255))
    # v7 touch 4: longer, brighter reflection path on the sea
    for i in range(48):
        y = 566 + i * 5
        wdt = 34 + i * 4 + random.randint(-8, 8)
        x0 = sun_c[0] - wdt // 2 + random.randint(-14, 14)
        alpha = max(36, 220 - i * 4)
        d.rectangle([x0, y, x0 + wdt, y + 3], fill=(255, 214, 130, alpha))


def paint_birds(d):
    # v7 touch 3: small birds in the evening sky
    for (bx, by, s) in [(150, 180, 10), (210, 150, 8), (620, 140, 9),
                        (690, 200, 7), (320, 110, 8), (540, 90, 7)]:
        d.arc([bx - s, by - s, bx, by + s], 200, 340, fill=(40, 32, 48, 200), width=2)
        d.arc([bx, by - s, bx + s, by + s], 200, 340, fill=(40, 32, 48, 200), width=2)


def paint_headland(d):
    d.polygon([(700, 560), (1024, 470), (1024, 560)], fill=(122, 74, 88, 200))
    d.polygon([(820, 560), (1024, 500), (1024, 560)], fill=(96, 58, 74, 220))


def paint_cliff_town(d):
    d.polygon([(640, 800), (700, 470), (1024, 400), (1024, 800)],
              fill=(146, 84, 62, 255))
    d.polygon([(640, 800), (700, 470), (760, 470), (720, 800)],
              fill=(120, 66, 50, 255))
    houses = [
        # x, y, w, h, wall, roof
        (760, 430, 90, 70, (250, 240, 214), (178, 84, 52)),
        (860, 415, 80, 78, (246, 230, 198), (168, 76, 48)),
        (945, 430, 79, 64, (250, 238, 210), (178, 84, 52)),
        (720, 520, 100, 76, (248, 236, 208), (172, 80, 50)),
        (830, 505, 86, 84, (252, 242, 218), (180, 86, 54)),
        (925, 520, 99, 70, (246, 232, 200), (170, 78, 48)),
        (690, 620, 110, 80, (250, 238, 212), (176, 82, 52)),
        (810, 610, 96, 88, (248, 234, 204), (172, 80, 50)),
        (915, 625, 109, 74, (252, 240, 216), (178, 84, 52)),
    ]
    for (x, y, w, h, wall, roof) in houses:
        d.rectangle([x, y, x + w, y + h], fill=wall)
        d.polygon([(x - 4, y), (x + w + 4, y), (x + w - 8, y - 16), (x + 8, y - 16)],
                  fill=roof)
        # lit windows, most of them warm
        for wx in range(x + 12, x + w - 12, 26):
            for wy in (y + 14, y + 42):
                if wy + 16 <= y + h:
                    lit = random.random() < 0.85
                    d.rectangle([wx, wy, wx + 12, wy + 16],
                                fill=(255, 214, 120, 255) if lit else (52, 44, 66, 255))
        # tiny arch door
        d.rectangle([x + w // 2 - 8, y + h - 22, x + w // 2 + 8, y + h],
                    fill=(72, 52, 60, 255))


def paint_clock_tower(d):
    # ONE small golden clock tower above the rooftops (kept from v6).
    x0, x1 = 886, 926
    d.rectangle([x0, 332, x1, 432], fill=(240, 214, 164, 255))
    d.rectangle([x0 - 3, 428, x1 + 3, 436], fill=(214, 178, 128, 255))
    # gold dome
    d.pieslice([x0 - 2, 306, x1 + 2, 344], 180, 360, fill=(232, 178, 84, 255))
    d.rectangle([x0 + 18, 296, x0 + 22, 310], fill=(90, 60, 30, 255))
    d.ellipse([x0 + 16, 292, x0 + 24, 300], fill=(255, 214, 120, 255))
    # clock face
    d.ellipse([x0 + 6, 346, x1 - 6, 380], fill=(255, 248, 228, 255))
    d.ellipse([x0 + 6, 346, x1 - 6, 380], outline=(120, 84, 40, 255), width=2)
    cx, cy = (x0 + x1) // 2, 363
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        d.ellipse([cx + int(13 * math.cos(a)) - 1, cy + int(13 * math.sin(a)) - 1,
                   cx + int(13 * math.cos(a)) + 1, cy + int(13 * math.sin(a)) + 1],
                  fill=(90, 60, 30, 255))
    # hands: about 5:40, like the golden hour
    d.line([cx, cy, cx + 7, cy - 9], fill=(60, 40, 24, 255), width=3)
    d.line([cx, cy, cx - 9, cy + 4], fill=(60, 40, 24, 255), width=3)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(60, 40, 24, 255))
    # tiny window under the face
    d.rectangle([cx - 5, 392, cx + 5, 414], fill=(52, 44, 66, 255))


def paint_trees(d):
    for (x, y, s) in [(735, 470, 46), (905, 455, 52), (985, 470, 44), (700, 600, 40)]:
        d.ellipse([x - s * 0.22, y - s, x + s * 0.22, y], fill=(34, 74, 52, 255))
        d.rectangle([x - 2, y - 4, x + 2, y + 6], fill=(74, 52, 38, 255))
    # bougainvillea clusters on the cliff
    for (x, y, r) in [(700, 500, 26), (880, 470, 30), (990, 560, 28), (745, 640, 24)]:
        for _ in range(26):
            px = x + random.randint(-r, r)
            py = y + random.randint(-r // 2, r // 2)
            d.ellipse([px - 4, py - 4, px + 4, py + 4],
                      fill=random.choice([(214, 62, 110), (226, 92, 128), (198, 48, 96)]))


def paint_staircase(d):
    for i in range(12):
        y = 560 + i * 18
        x0 = 520 - i * 3
        x1 = 620 + i * 2
        d.rectangle([x0, y, x1, y + 11], fill=(240, 214, 164, 255))
        d.rectangle([x0, y + 11, x1, y + 14], fill=(176, 128, 84, 255))
    # stair side walls
    d.polygon([(520, 560), (500, 776), (520, 776), (538, 560)], fill=(214, 178, 128, 255))
    d.polygon([(620, 560), (640, 776), (620, 776), (604, 560)], fill=(214, 178, 128, 255))
    # lanterns on the stair walls
    for (x, y) in [(506, 600), (520, 680), (634, 620), (624, 700)]:
        d.rectangle([x - 3, y - 12, x + 3, y + 12], fill=(52, 44, 58, 255))
        d.ellipse([x - 8, y - 24, x + 8, y - 8], fill=(255, 214, 120, 255))


def paint_sailboats(d):
    def sailboat(cx, cy, s):
        d.polygon([(cx - 34 * s, cy), (cx + 34 * s, cy), (cx + 22 * s, cy + 14 * s),
                   (cx - 22 * s, cy + 14 * s)], fill=(72, 44, 40, 255))
        d.rectangle([cx - 2 * s, cy - 62 * s, cx + 2 * s, cy], fill=(52, 40, 36, 255))
        d.polygon([(cx + 4 * s, cy - 58 * s), (cx + 4 * s, cy - 4 * s),
                   (cx + 40 * s, cy - 4 * s)], fill=(255, 246, 224, 255))
        d.polygon([(cx - 4 * s, cy - 48 * s), (cx - 4 * s, cy - 4 * s),
                   (cx - 30 * s, cy - 4 * s)], fill=(250, 226, 188, 255))
        # reflection
        for i in range(4):
            d.rectangle([cx - 26 * s, cy + 18 * s + i * 6, cx + 26 * s,
                         cy + 21 * s + i * 6], fill=(255, 220, 150, 90 - i * 18))

    sailboat(250, 640, 1.0)
    sailboat(180, 720, 0.65)
    # v7 touch 3: two more small sailboats, further out
    sailboat(430, 700, 0.5)
    sailboat(90, 600, 0.45)


def paint_bunting(d):
    # v7 touch 2: warm bunting flags strung across the cafe terrace.
    # Two gentle sagging lines of small triangle flags.
    palette = [(214, 62, 110), (232, 178, 84), (250, 240, 214),
               (32, 110, 110), (178, 84, 52)]
    for (x0, y0, x1, y1) in [(30, 806, 500, 830), (520, 828, 1000, 806)]:
        n = 16
        for i in range(n):
            t = i / (n - 1)
            x = x0 + (x1 - x0) * t
            # sag curve
            y = y0 + (y1 - y0) * t + 26 * math.sin(math.pi * t)
            col = palette[i % len(palette)]
            d.polygon([(x - 9, y), (x + 9, y), (x, y + 20)], fill=col)
        # string line
        for i in range(n - 1):
            t0 = i / (n - 1)
            t1 = (i + 1) / (n - 1)
            xa = x0 + (x1 - x0) * t0
            ya = y0 + (y1 - y0) * t0 + 26 * math.sin(math.pi * t0)
            xb = x0 + (x1 - x0) * t1
            yb = y0 + (y1 - y0) * t1 + 26 * math.sin(math.pi * t1)
            d.line([(xa, ya), (xb, yb)], fill=(60, 40, 30, 220), width=2)


def paint_cafe(d):
    # balustrade
    d.rectangle([0, 800, W, 818], fill=(226, 188, 138, 255))
    for x in range(30, W, 46):
        d.rectangle([x, 818, x + 14, 872], fill=(240, 214, 164, 255))
        d.ellipse([x - 2, 812, x + 16, 826], fill=(244, 222, 176, 255))
    d.rectangle([0, 872, W, 884], fill=(214, 172, 118, 255))
    # round table + two people (left)
    d.ellipse([140, 912, 350, 940], fill=(255, 250, 236, 255))
    d.rectangle([236, 935, 244, 1000], fill=(120, 88, 60, 255))
    # person 1 (straw hat, rust dress)
    d.ellipse([176, 872, 212, 908], fill=(52, 40, 36, 255))
    d.ellipse([158, 884, 230, 902], fill=(232, 196, 120, 255))
    d.polygon([(168, 908), (220, 908), (232, 985), (156, 985)], fill=(178, 84, 52, 255))
    # person 2 (dark hair, white shirt)
    d.ellipse([262, 874, 296, 908], fill=(40, 32, 30, 255))
    d.polygon([(256, 908), (302, 908), (312, 985), (246, 985)], fill=(250, 244, 230, 255))
    # wine glasses on the table
    for gx in (196, 282):
        d.rectangle([gx, 890, gx + 10, 906], fill=(255, 240, 190, 230))
        d.rectangle([gx + 4, 906, gx + 6, 912], fill=(255, 240, 190, 230))
    # potted bougainvillea (right foreground)
    d.polygon([(880, 930), (950, 930), (940, 1000), (890, 1000)], fill=(172, 84, 52, 255))
    for _ in range(40):
        px = 915 + random.randint(-46, 46)
        py = 900 + random.randint(-34, 10)
        d.ellipse([px - 5, py - 5, px + 5, py + 5],
                  fill=random.choice([(214, 62, 110), (226, 92, 128), (198, 48, 96)]))
    d.polygon([(60, 930), (130, 930), (122, 1000), (68, 1000)], fill=(172, 84, 52, 255))
    for _ in range(26):
        px = 95 + random.randint(-34, 34)
        py = 905 + random.randint(-28, 8)
        d.ellipse([px - 5, py - 5, px + 5, py + 5],
                  fill=random.choice([(214, 62, 110), (226, 92, 128)]))


def paint_cafe_extra(d):
    # second, livelier cafe table (umbrella, more people) - kept from v6
    # striped umbrella
    for i, col in enumerate([(250, 240, 214, 255), (214, 62, 110, 255),
                             (250, 240, 214, 255), (214, 62, 110, 255),
                             (250, 240, 214, 255)]):
        a0 = 180 + i * 36
        d.pieslice([540, 800, 740, 900], a0, a0 + 36, fill=col)
    d.rectangle([636, 850, 644, 928], fill=(120, 88, 60, 255))
    # round table
    d.ellipse([560, 922, 720, 948], fill=(255, 250, 236, 255))
    d.rectangle([636, 944, 644, 1000], fill=(120, 88, 60, 255))
    # person 3 (wide cream hat, teal dress)
    d.ellipse([576, 884, 610, 916], fill=(52, 40, 36, 255))
    d.ellipse([556, 894, 630, 912], fill=(250, 240, 214, 255))
    d.polygon([(570, 916), (616, 916), (626, 990), (560, 990)], fill=(32, 110, 110, 255))
    # person 4 (grey hair, ochre shirt)
    d.ellipse([664, 886, 696, 918], fill=(200, 190, 180, 255))
    d.polygon([(658, 918), (702, 918), (712, 990), (648, 990)], fill=(212, 150, 52, 255))
    # glasses on the second table
    for gx in (596, 676):
        d.rectangle([gx, 900, gx + 10, 916], fill=(255, 240, 190, 230))
        d.rectangle([gx + 4, 916, gx + 6, 922], fill=(255, 240, 190, 230))


def paint_frame_title(img):
    # soft vignette
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, W, H], outline=(60, 30, 20, 70), width=26)
    img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    # cream border + inner rule
    d.rectangle([0, 0, W - 1, H - 1], outline=(250, 240, 214, 255), width=26)
    d.rectangle([34, 34, W - 35, H - 35], outline=(250, 240, 214, 160), width=2)
    # title, same size as v5/v6
    f_title = ImageFont.truetype(SERIF_B, 130)
    f_sub = ImageFont.truetype(SERIF, 36)
    lettered(d, W // 2, 72, "AURMARA", f_title, (255, 246, 224, 255),
             spacing=10, shadow=(4, 5, (90, 40, 20, 160)))
    lettered(d, W // 2, 228, "THE HARBOUR OF GOLDEN STAIRS", f_sub,
             (255, 238, 205, 255), spacing=5, shadow=(2, 2, (90, 40, 20, 140)))
    return img


def main():
    img = Image.new("RGB", (W, H), (24, 48, 84))
    d = ImageDraw.Draw(img, "RGBA")
    paint_sky(img)
    paint_sea(img)
    paint_terrace(img)
    paint_sun(d, (400, 520))
    paint_birds(d)
    paint_grain(d)
    paint_headland(d)
    paint_cliff_town(d)
    paint_clock_tower(d)
    paint_trees(d)
    paint_staircase(d)
    paint_sailboats(d)
    paint_cafe(d)
    paint_cafe_extra(d)
    paint_bunting(d)
    img = paint_frame_title(img)
    img.save(OUT, optimize=True)
    print("saved", OUT, img.size)
    print("bytes:", os.path.getsize(OUT))


if __name__ == "__main__":
    main()
