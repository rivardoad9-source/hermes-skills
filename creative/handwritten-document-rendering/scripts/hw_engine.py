# -*- coding: utf-8 -*-
"""Renderer halaman bergaya tulisan tangan (pulpen, kertas bergaris) -> PNG + PDF.

Cara pakai:
    from hw_engine import build
    ITEMS = [("h1", "SOAL 1", 0), ("p", "Isi paragraf ...", 0),
             ("f", "Saldo menurut bank|Rp205.595.500", 1), ("blank", "", 0)]
    pages, pdf = build(ITEMS, os.path.expanduser("~/tugas/Keluar.pdf"), tag="tugas_")

kind: h1 (judul + garis bawah) | h2 (subjudul bold) | num | bul | p | f (baris angka) | blank | s (kecil)
- "label|Rp123"  -> angka rata kanan di kolom AMT_X  (pakai ini, jangan padding spasi manual)
- token "->"     -> digambar jadi panah tangan (font handwriting tidak punya glyph panah)
- indent        -> level indentasi (0,1,2 ... = kelipatan 52 px)

Font: unduh ke ~/.hermes/assets/fonts (Kalam-Regular/-Bold/-Light adalah default paling natural).
"""
import os, random
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = os.path.expanduser("~/.hermes/assets/fonts")
OUT_DIR = os.path.expanduser("~/tugas")
SEED = 20261001

W, H = 1654, 2339            # A4 @ 200 dpi
ML, MR, MT, MB = 168, 138, 176, 150
RULE_GAP = 52
INK = (34, 33, 40)
BIC = Image.Resampling.BICUBIC
AMT_X = ML + 980             # kolom angka (rata kanan di kolom ini)

random.seed(SEED)


def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BODY_V = [F("Kalam-Regular.ttf", s) for s in (30, 31, 32, 32)]
BODY_L = F("Kalam-Light.ttf", 31)
HEAD = F("Kalam-Bold.ttf", 37)
SUB = F("Kalam-Bold.ttf", 32)
SMALL = F("Kalam-Regular.ttf", 27)
STYLE = {"h1": HEAD, "h2": SUB, "num": None, "bul": None, "p": None, "f": None, "s": SMALL}


def paper():
    img = Image.new("RGB", (W, H), (253, 250, 242))
    n = Image.effect_noise((W, H), 7).convert("L")
    img = Image.blend(img, Image.merge("RGB", (n, n, n)), 0.05)
    d = ImageDraw.Draw(img, "RGBA")
    y = MT - RULE_GAP + 12
    while y < H - MB + RULE_GAP:
        val = random.randint(196, 212)
        sl = random.uniform(-0.9, 0.9)
        d.line([(ML - 46, y), (W - MR + 40, y + sl)], fill=(val, val + 2, val - 6, 145), width=1)
        y += RULE_GAP
    d.line([(ML - 46, MT - 70), (ML - 46, H - MB + 40)], fill=(216, 198, 198, 110), width=2)
    # gradasi cahaya + vignette halus (kesan difoto/scan)
    grad = Image.linear_gradient("L").resize((W, H)).rotate(90, expand=True)
    g = Image.new("L", (W, H))
    g.paste(grad, (0, 0))
    g = g.point(lambda v: 226 + int(v * 0.11))
    solid = Image.new("RGB", (W, H), (250, 247, 238))
    img = Image.composite(img, solid, g)
    dd = ImageDraw.Draw(img, "RGBA")
    for _ in range(7):                    # bintik kertas
        x, y2 = random.randint(ML, W - MR), random.randint(MT, H - MB)
        r = random.choice([1, 1, 2])
        dd.ellipse([x, y2, x + r, y2 + r], fill=(150, 145, 135, random.randint(25, 55)))
    return img


def draw_word(layer, text, x, y, font, size_var=3):
    if size_var and random.random() < 0.12:
        font = BODY_L if random.random() < 0.5 else BODY_V[-1]
    w = int(font.getlength(text)) + 20
    asc, desc = font.getmetrics()
    tile = Image.new("RGBA", (w, asc + desc + 18), (0, 0, 0, 0))
    ink = (INK[0] + random.randint(-7, 9), INK[1] + random.randint(-7, 9), INK[2] + random.randint(-5, 14))
    a = random.randint(228, 255)
    d = ImageDraw.Draw(tile)
    d.text((9, 9), text, font=font, fill=ink + (a,))
    if random.random() < 0.22:                      # tekanan pulpen lebih kuat
        d.text((10, 9), text, font=font, fill=ink + (a - 30,))
    sc = random.uniform(0.955, 1.045)               # variasi lebar huruf
    tile = tile.resize((max(1, int(tile.width * sc)), tile.height), resample=BIC)
    tile = tile.rotate(random.uniform(-0.8, 0.8), resample=BIC, expand=True)
    layer.alpha_composite(tile, (int(x + random.uniform(-1.6, 1.6)),
                                 int(y + random.uniform(-1.8, 1.8))))
    return sc


def draw_arrow(layer, x, y):
    d = ImageDraw.Draw(layer, "RGBA")
    ln = random.randint(26, 34)
    y1 = y + random.uniform(-2, 2)
    y2 = y1 + random.uniform(-2, 2)
    a = INK + (random.randint(235, 255),)
    d.line([(x, y1), (x + ln, y2)], fill=a, width=2)
    d.line([(x + ln - 12, y2 - 6), (x + ln, y2)], fill=a, width=2)
    d.line([(x + ln - 12, y2 + 6), (x + ln, y2)], fill=a, width=2)
    return ln


ARROW_W = 34


def wrap(txt, indent, font, amt=None):
    """bila amt (string) diberikan, teks kiri + angka rata kanan di kolom AMT_X"""
    lh = int(sum(font.getmetrics()) * 1.10) + 6
    x0 = ML + indent * 52
    space = font.getlength(" ")
    lines, cur, x = [], [], x0
    limit = (AMT_X - 30) - x0 if amt else (W - MR)
    for wd in txt.split(" "):
        wl = ARROW_W if wd == "->" else font.getlength(wd)
        if cur and x + wl > limit:
            lines.append((x0, cur))
            cur, x = [], x0
        cur.append(wd)
        x += wl + space
    if cur:
        lines.append((x0, cur))
    return lh, lines


def render_page(items, state, pageno):
    base = paper()
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = MT
    n = len(items)
    while state["i"] < n:
        kind, raw, indent = items[state["i"]]
        if kind == "blank":
            y += int(RULE_GAP * 0.72)
            state["i"] += 1
            continue
        font = STYLE[kind] if kind in ("h1", "h2", "s") else random.choice(BODY_V)
        txt, amt = raw, None
        if "|" in raw:
            txt, amt = raw.split("|", 1)
            txt, amt = txt.rstrip(), amt.strip()
        lh, lines = wrap(txt, indent, font, amt)
        need = lh * len(lines) + (10 if kind == "h1" else 4)
        if y + need > H - MB and y > MT + 20:        # jangan potong item di tengah halaman
            break
        if kind == "h1":
            d = ImageDraw.Draw(layer, "RGBA")
            wdt = int(font.getlength(txt))
            d.line([(ML - 2, y + lh - 11), (ML + wdt + 8, y + lh - 15)], fill=INK + (210,), width=2)
        drift = random.uniform(-5.0, 5.0)            # goyangan baseline per baris
        rate = random.uniform(-0.010, 0.010)
        for (x0, words) in lines:
            x = x0
            for wd in words:
                yy = y + drift + rate * (x - x0)
                if wd == "->":
                    ln = draw_arrow(layer, x, yy + int(font.size * 0.60))
                    x += ln + random.uniform(6, 12)
                else:
                    sc = draw_word(layer, wd, x, yy, font)
                    x += font.getlength(wd) * sc + font.getlength(" ") * random.uniform(0.78, 1.22)
            if amt and (x0, words) == lines[-1]:
                aw = font.getlength(amt)
                draw_word(layer, amt, AMT_X - aw - 6, y + drift, font)
            y += lh
        state["i"] += 1
    d = ImageDraw.Draw(layer, "RGBA")
    d.text((W - MR - 44, H - MB + 40), str(pageno), font=SMALL, fill=INK + (215,))
    tilt = random.uniform(-0.55, 0.55)               # halaman tidak 100% tegak
    layer = layer.rotate(tilt, resample=BIC, center=(W // 2, H // 2))
    out = base.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB")


def build(items, out_pdf, tag="", out_dir=None):
    out_dir = out_dir or OUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    state = {"i": 0}
    pages = []
    while state["i"] < len(items) and len(pages) < 60:
        pg = render_page(items, state, len(pages) + 1)
        pg.save(os.path.join(out_dir, f"page_{tag}{len(pages)+1}.png"))
        pages.append(pg)
    pages[0].save(out_pdf, save_all=True, append_images=pages[1:], resolution=200.0)
    return pages, out_pdf
