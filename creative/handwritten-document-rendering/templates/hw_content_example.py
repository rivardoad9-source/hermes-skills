# -*- coding: utf-8 -*-
"""Contoh struktur konten + cara panggil build(). Copy lalu ganti isinya.

    python3 hw_content_tugas.py     -> ~/tugas/page_tugas_1..N.png + <out_pdf>
"""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.hermes/skills/creative/handwritten-document-rendering/scripts"))
from hw_engine import build

ITEMS = []


def add(kind, txt, indent=0):
    ITEMS.append((kind, txt, indent))


# --- judul: garis bawah otomatis ---
add("h1", "SOAL 1", 0)
add("h2", "a. Subjudul bagian", 0)

# --- list bernomor / bullet; "->" jadi panah tangan ---
add("num", "1. Integritas -> auditor harus jujur dan tidak menyembunyikan temuan penting.", 1)
add("bul", "Safeguards: rotasi partner dan anggota tim audit.", 1)

# --- paragraf ---
add("p", "Paragraf pembuka ditulis mengalir tanpa indentasi.", 0)

# --- baris angka: pakai '|' supaya angka rata kanan di kolom ---
add("f", "Saldo menurut bank|Rp205.595.500", 1)
add("f", "Ditambah: deposit in transit|Rp30.000.000", 1)
add("f", "kesalahan bank|Rp900.000", 2)          # indent 2 = sub-item
add("f", "= saldo disesuaikan|Rp220.445.500", 1)
add("blank", "", 0)                              # baris kosong

# --- teks kecil (catatan kaki / nomor halaman manual) ---
add("s", "Catatan: angka ini contoh, ganti sesuai data.", 0)

if __name__ == "__main__":
    out_dir = os.path.expanduser("~/tugas")
    pdf = os.path.join(out_dir, "Contoh_Tulisan_Tangan.pdf")
    pages, pdf = build(ITEMS, pdf, tag="tugas_", out_dir=out_dir)
    print("pages:", len(pages), "->", pdf)
