# -*- coding: utf-8 -*-
"""Cek glyph mana yang TIDAK ada di sebuah font (tanpa fontTools).

Cara kerja: render tiap char ke bitmap kecil, bandingkan MD5-nya dengan render
U+10FFFD (codepoint private-use yang dijamin tidak ada di font) -> kalau hash-nya
sama, artinya font merender notdef/tofu, jadi glyph itu TIDAK tersedia.

Pakai sebelum render dokumen panjang, supaya tidak dapat kotak-kotak di tengah halaman.

    python3 font_glyph_check.py Kalam-Regular.ttf
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = os.path.expanduser("~/.hermes/assets/fonts")
DEFAULT_CHARS = "→↳×±•–—""≈°%&/:;()[]{}<>"


def sig(font, ch, size=40):
    im = Image.new("L", (90, 76), 0)
    ImageDraw.Draw(im).text((6, 6), ch, font=font, fill=255)
    return hashlib.md5(im.tobytes()).hexdigest()


def check(path, chars=DEFAULT_CHARS):
    font = ImageFont.truetype(path, 40)
    notdef = sig(font, "\U0010FFFD")
    missing = [c for c in chars if sig(font, c) == notdef]
    return missing


if __name__ == "__main__":
    args = sys.argv[1:] or ["Kalam-Regular.ttf", "Kalam-Bold.ttf"]
    for a in args:
        p = a if os.path.isabs(a) else os.path.join(FONT_DIR, a)
        if not os.path.exists(p):
            print(f"{a}: TIDAK ADA (cek nama file / unduh ulang)")
            continue
        miss = check(p)
        print(f"{os.path.basename(p)}: missing = {''.join(miss) if miss else '(semua ada)'}")
