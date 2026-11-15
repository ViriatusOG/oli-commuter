#!/usr/bin/env python3
"""Draw the launcher icons for "Next Elizabeth line".

No image libraries needed: the roundel is drawn with signed-distance maths and
written out as PNG with stdlib zlib.  Run it again any time you want to change
the mark, then rebuild:

    python3 make-icons.py && ./build.sh

It writes, for every density Android asks for:
  * mipmap-*/ic_launcher.png          the squarish icon (legacy launchers)
  * mipmap-*/ic_launcher_round.png    the same mark in a circle
  * mipmap-*/ic_launcher_foreground.png  adaptive-icon foreground, on clear
  * drawable-*/splash.png                the launch screen
and sets the adaptive background colour to Elizabeth line purple.
"""
import math
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "android", "app", "src", "main", "res")

PURPLE = (0x66, 0x00, 0xCC)
WHITE = (255, 255, 255)

DENSITIES = {  # res folder -> icon size in px
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}
ADAPTIVE = {   # 108dp canvas per density
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432,
}
# Supersampling is what makes small icons smooth, but it is pure Python maths per
# pixel: big launch screens would take minutes. Fewer samples where the picture is
# already hundreds of pixels across.
def supersample(w, h):
    m = max(w, h)
    return 4 if m <= 480 else (2 if m <= 900 else 1)


def sdf_rounded_rect(px, py, hw, hh, r):
    dx = abs(px) - (hw - r)
    dy = abs(py) - (hh - r)
    return math.hypot(max(dx, 0.0), max(dy, 0.0)) + min(max(dx, dy), 0.0) - r


def alpha(distance, edge=1.0):
    """1 inside the shape, 0 outside, soft over `edge` pixels."""
    return max(0.0, min(1.0, 0.5 - distance / edge))


def mark_alpha(px, py, ring_r, ring_t, bar_w, bar_h, bar_r, edge):
    ring = alpha(abs(math.hypot(px, py) - ring_r) - ring_t / 2.0, edge)
    bar = alpha(sdf_rounded_rect(px, py, bar_w / 2.0, bar_h / 2.0, bar_r), edge)
    return max(ring, bar)


def draw_splash(w, h, logo_scale=0.34):
    """A purple launch screen with the roundel centred.

    The background is a solid fill, so instead of computing every pixel the rows
    are written out as whole purple stretches and only the roundel's bounding
    box is drawn pixel by pixel: a 1280x1920 screen comes out in well under a
    second."""
    ss = supersample(w, h)
    cw, ch = w * ss, h * ss
    cx, cy = cw / 2.0, ch / 2.0
    unit = min(cw, ch)
    ring_r = unit * 0.5 * logo_scale
    ring_t = ring_r * 0.30
    bar_w = ring_r * 2.05
    bar_h = ring_r * 0.40
    bar_r = bar_h / 2.0
    edge = 1.0
    pad = 2 * ss
    half = max(bar_w, 2 * ring_r) / 2.0
    bx0 = max(0, int((cx - half) // ss) - pad)
    bx1 = min(w, int((cx + half) // ss) + pad)
    by0 = max(0, int((cy - ring_r) // ss) - pad)
    by1 = min(h, int((cy + ring_r) // ss) + pad)
    purple = bytes(PURPLE + (255,))

    out = bytearray()
    for y in range(h):
        out.append(0)  # filter: none
        if not (by0 <= y < by1):
            out.extend(purple * w)
            continue
        py = y * ss + ss / 2.0 - cy
        out.extend(purple * bx0)
        for x in range(bx0, bx1):
            px = x * ss + ss / 2.0 - cx
            rs = gs = bs = al = 0.0
            for dy in range(ss):
                for dx in range(ss):
                    m = mark_alpha(px + dx, py + dy, ring_r, ring_t, bar_w, bar_h, bar_r, edge)
                    rs += (PURPLE[0] + (WHITE[0] - PURPLE[0]) * m) * m
                    gs += (PURPLE[1] + (WHITE[1] - PURPLE[1]) * m) * m
                    bs += (PURPLE[2] + (WHITE[2] - PURPLE[2]) * m) * m
                    al += m
            if al == 0:
                out.extend(purple)
            else:
                out.extend((round(rs / al), round(gs / al), round(bs / al), round(al / (ss * ss))))
        out.extend(purple * (w - bx1))
    return out


def draw_rect(w, h, shape, logo_scale, transparent_bg):
    """shape: 'fill' | 'square' | 'circle' | 'none' (clear background)."""
    if shape == "fill":
        return draw_splash(w, h)
    ss = supersample(w, h)
    canvas_w, canvas_h = w * ss, h * ss
    unit = min(canvas_w, canvas_h)
    cx, cy = canvas_w / 2.0, canvas_h / 2.0
    # the roundel: a ring with a bar through it, the way TfL draws it
    ring_r = unit * 0.5 * logo_scale
    ring_t = ring_r * 0.30
    bar_w = ring_r * 2.05
    bar_h = ring_r * 0.40
    bar_r = bar_h / 2.0
    bg_r = unit * 0.16 if shape == "square" else unit  # corner radius

    edge = 1.0

    rows = []
    for iy in range(canvas_h):
        py = iy + 0.5 - cy
        row = []
        for ix in range(canvas_w):
            px = ix + 0.5 - cx
            # background
            if shape == "none":
                bg = 0.0
            elif shape == "fill":
                bg = 1.0
            elif shape == "circle":
                bg = alpha(math.hypot(px, py) - unit / 2.0, edge)
            else:
                bg = alpha(sdf_rounded_rect(px, py, canvas_w / 2.0, canvas_h / 2.0, bg_r), edge)
            # roundel
            ring = alpha(abs(math.hypot(px, py) - ring_r) - ring_t / 2.0, edge)
            bar = alpha(sdf_rounded_rect(px, py, bar_w / 2.0, bar_h / 2.0, bar_r), edge)
            mark = max(ring, bar)
            # the white mark only shows where there is something under it, unless
            # we are drawing the clear adaptive-icon foreground
            mark = mark if transparent_bg else min(mark, bg)
            a = max(bg, mark)
            if a <= 0.0:
                row.append((0, 0, 0, 0))
                continue
            mix = mark / a
            r = round(PURPLE[0] * (1 - mix) + WHITE[0] * mix)
            g = round(PURPLE[1] * (1 - mix) + WHITE[1] * mix)
            b = round(PURPLE[2] * (1 - mix) + WHITE[2] * mix)
            row.append((r, g, b, round(a * 255)))
        rows.append(row)

    # average the supersampled block down to the requested size
    out = bytearray()
    for y in range(h):
        out.append(0)  # filter: none
        for x in range(w):
            rs = gs = bs = al = 0.0
            for dy in range(ss):
                for dx in range(ss):
                    r, g, b, a = rows[y * ss + dy][x * ss + dx]
                    rs += r * a
                    gs += g * a
                    bs += b * a
                    al += a
            if al == 0:
                out.extend((0, 0, 0, 0))
            else:
                out.extend((round(rs / al), round(gs / al), round(bs / al), round(al / (ss * ss))))
    return out


def draw(size, shape, logo_scale, transparent_bg):
    return draw_rect(size, size, shape, logo_scale, transparent_bg)


def write_png(path, size, raw):
    return write_png_rect(path, size, size, raw)


def write_png_rect(path, w, h, raw):
    flat = zlib.compress(bytes(raw), 9)
    head = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head) + chunk(b"IDAT", flat) + chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)
    return os.path.getsize(path)


# the launch screen, in the shapes Android asks for (w, h) per density
SPLASH = {
    "drawable": (480, 320),
    "drawable-port-mdpi": (320, 480),
    "drawable-port-hdpi": (480, 800),
    "drawable-port-xhdpi": (720, 1280),
    "drawable-port-xxhdpi": (960, 1600),
    "drawable-port-xxxhdpi": (1280, 1920),
    "drawable-land-mdpi": (480, 320),
    "drawable-land-hdpi": (800, 480),
    "drawable-land-xhdpi": (1280, 720),
    "drawable-land-xxhdpi": (1600, 960),
    "drawable-land-xxxhdpi": (1920, 1280),
}


def write_splashes():
    for folder, dims in SPLASH.items():
        w, h = (dims, dims) if isinstance(dims, int) else dims
        d = os.path.join(RES, folder)
        os.makedirs(d, exist_ok=True)
        write_png_rect(os.path.join(d, "splash.png"), w, h, draw_rect(w, h, "fill", 0.34, False))


def main():
    for folder, size in DENSITIES.items():
        d = os.path.join(RES, folder)
        os.makedirs(d, exist_ok=True)
        write_png(os.path.join(d, "ic_launcher.png"), size, draw(size, "square", 0.74, False))
        write_png(os.path.join(d, "ic_launcher_round.png"), size, draw(size, "circle", 0.80, False))
    for folder, size in ADAPTIVE.items():
        d = os.path.join(RES, folder)
        os.makedirs(d, exist_ok=True)
        # 66 % of the adaptive canvas, so launchers can crop a circle or a blob
        write_png(os.path.join(d, "ic_launcher_foreground.png"), size, draw(size, "none", 0.66, True))
    colours = os.path.join(RES, "values")
    os.makedirs(colours, exist_ok=True)
    with open(os.path.join(colours, "ic_launcher_background.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#6600CC</color>\n</resources>\n')
    write_splashes()
    print("icons and launch screens written to", RES)


if __name__ == "__main__":
    main()
