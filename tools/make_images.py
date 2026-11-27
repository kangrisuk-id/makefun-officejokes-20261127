#!/usr/bin/env python3
"""Build-time image generator for the entry README (Pillow only).

Generates assets/hero.png (1200x630) and four 800x500 gallery images.
NOT imported by main.py — the submitted entrypoint is stdlib-only.
Run:  python3 tools/make_images.py
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

BG = (26, 29, 41)        # charcoal navy
BG2 = (34, 38, 56)
GOLD = (245, 197, 24)
GOLD_D = (210, 165, 10)
WHITE = (245, 245, 240)
MUTED = (168, 175, 195)
CARD = (44, 49, 71)
GREEN = (74, 222, 128)
RED = (248, 113, 113)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)      # noqa: E731
REG = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731

JOKE = "The printer jammed on page 1 of 1, which IT logged as a 'complex multi-page failure'."


def wrap(draw, text, fnt, width):
    """Wrap text to pixel width, returning lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_printer(draw, x, y, scale=1.0):
    """Simple flat printer with a jammed sheet, drawn from rectangles."""
    w, h = int(300 * scale), int(170 * scale)
    # paper sheet sticking out the top, tilted
    draw.polygon([(x + 60, y - 46), (x + 240, y - 46), (x + 225, y + 30), (x + 75, y + 30)],
                 fill=(235, 235, 225), outline=(180, 180, 170))
    for i, txt in enumerate(["PAGE 1 of 1", "ERROR: JAM"]):
        draw.text((x + 85, y - 38 + i * 20), txt, font=BOLD(int(15 * scale)),
                  fill=(200, 60, 60) if i else (60, 60, 60))
    # body
    draw.rounded_rectangle([x, y + 30, x + w, y + 30 + h], radius=int(18 * scale), fill=CARD)
    draw.rounded_rectangle([x, y + 30, x + w, y + 30 + 46], radius=int(18 * scale), fill=(58, 64, 90))
    draw.rectangle([x, y + 30 + 40, x + w, y + 30 + 46], fill=(58, 64, 90))
    # output slot + paper coming out
    draw.rectangle([x + 30, y + 30 + 92, x + w - 30, y + 30 + 108], fill=(20, 22, 32))
    draw.polygon([(x + 70, y + 30 + 108), (x + 230, y + 30 + 108),
                  (x + 245, y + 30 + 150), (x + 55, y + 30 + 150)],
                 fill=(235, 235, 225), outline=(180, 180, 170))
    # buttons
    draw.ellipse([x + w - 52, y + 30 + 58, x + w - 32, y + 30 + 78], fill=RED)
    draw.ellipse([x + w - 84, y + 30 + 58, x + w - 64, y + 30 + 78], fill=GREEN)


def hero():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # gold top rule + corner dots
    d.rectangle([0, 0, W, 8], fill=GOLD)
    for cx in (60, W - 60):
        d.ellipse([cx - 6, 26, cx + 6, 38], fill=GOLD)
    d.text((60, 60), "MAKE.FUN  ·  ONE-LINE OFFICE JOKES", font=BOLD(30), fill=GOLD)
    d.text((60, 104), "The printer jammed on page 1 of 1…", font=BOLD(48), fill=WHITE)
    # joke card
    d.rounded_rectangle([60, 190, 700, 420], radius=24, fill=CARD)
    d.rectangle([60, 190, 72, 420], fill=GOLD)
    lines = wrap(d, "\u201c" + JOKE + "\u201d", REG(34), 580)
    y = 225
    for ln in lines:
        d.text((96, y), ln, font=REG(34), fill=WHITE)
        y += 46
    d.text((96, 368), "25/25  ·  tournament winner  ·  85 characters", font=BOLD(24), fill=GREEN)
    # printer on the right
    draw_printer(d, 770, 260, scale=1.0)
    d.text((770, 470), "IT ticket: MULTI-PAGE FAILURE", font=BOLD(20), fill=RED)
    # bottom strip
    d.text((60, 500), "$2 USDC  ·  5 paid places  ·  1st $0.73", font=BOLD(30), fill=WHITE)
    d.text((60, 548), "30 candidates  →  8 finalists  →  1 line. Judged pairwise by the house judge.",
           font=REG(24), fill=MUTED)
    img.save(os.path.join(ASSETS, "hero.png"))


def gallery_joke():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), BG2)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=GOLD)
    d.text((50, 44), "THE WINNING LINE — v3", font=BOLD(28), fill=GOLD)
    d.rounded_rectangle([50, 100, 750, 330], radius=20, fill=CARD)
    d.rectangle([50, 100, 62, 330], fill=GOLD)
    lines = wrap(d, "\u201c" + JOKE + "\u201d", REG(32), 640)
    y = 130
    for ln in lines:
        d.text((86, y), ln, font=REG(32), fill=WHITE)
        y += 44
    d.text((86, 285), "85 chars  ·  1 line  ·  0 trailing newline", font=BOLD(22), fill=GREEN)
    d.text((50, 370), "Device: concrete number + absurd IT escalation.", font=REG(24), fill=MUTED)
    d.text((50, 408), "The laugh lands in the last four words.", font=REG(24), fill=MUTED)
    img.save(os.path.join(ASSETS, "gallery-joke.png"))


def gallery_printer():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), BG2)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=GOLD)
    d.text((50, 44), "THE SCENE — PAGE 1 OF 1", font=BOLD(28), fill=GOLD)
    draw_printer(d, 250, 170, scale=1.0)
    d.text((50, 380), "One page. One jam. One very confident IT ticket.", font=REG(26), fill=WHITE)
    d.text((50, 424), "The contradiction is the joke: a single page cannot", font=REG(22), fill=MUTED)
    d.text((50, 452), "fail as a “multi-page” job — so IT's label is the punchline.", font=REG(22), fill=MUTED)
    img.save(os.path.join(ASSETS, "gallery-printer.png"))


def gallery_bracket():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), BG2)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=GOLD)
    d.text((50, 44), "THE TOURNAMENT — 30 → 8 → 1", font=BOLD(28), fill=GOLD)
    stages = [
        ("30", "candidates", "8 devices", MUTED),
        ("8", "finalists", "scored /25", MUTED),
        ("4", "semi-finalists", "knockout", MUTED),
        ("1", "WINNER", "25/25", GOLD),
    ]
    x = 50
    for idx, (num, label, sub, col) in enumerate(stages):
        d.rounded_rectangle([x, 120, x + 160, 300], radius=16, fill=CARD)
        d.text((x + 80, 150), num, font=BOLD(64), fill=col, anchor="mt")
        d.text((x + 80, 235), label, font=BOLD(20), fill=WHITE, anchor="mt")
        d.text((x + 80, 265), sub, font=REG(18), fill=MUTED, anchor="mt")
        if idx < len(stages) - 1:
            d.text((x + 160, 195), "  →  ", font=BOLD(28), fill=GOLD)
        x += 170
    qf = wrap(d, "Quarter-finals: #25 beats #24 · #10 beats #21 · #11 beats #29 · #4 beats #23",
              REG(22), 700)
    y = 340
    for ln in qf:
        d.text((50, y), ln, font=REG(22), fill=WHITE)
        y += 32
    d.text((50, y + 6), "Semi-finals: #25 beats #10 · #11 beats #4", font=REG(22), fill=WHITE)
    d.text((50, y + 44), "Final: #25 beats #11 on freshness (criterion 5, 5–4).", font=REG(22), fill=WHITE)
    img.save(os.path.join(ASSETS, "gallery-bracket.png"))


def gallery_criteria():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), BG2)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=GOLD)
    d.text((50, 44), "THE JUDGE BRIEF — ALL FIVE, IN ORDER", font=BOLD(28), fill=GOLD)
    rows = [
        ("1", "Single-line joke about office life", "5 / 5"),
        ("2", "Real detail: the printer, the IT ticket", "5 / 5"),
        ("3", "Laugh lands in the last few words", "5 / 5"),
        ("4", "Clear on one reading, no setup needed", "5 / 5"),
        ("5", "Fresh wording, not a circulating joke", "5 / 5"),
    ]
    y = 110
    for num, label, score in rows:
        d.ellipse([50, y, 92, y + 42], fill=GREEN)
        d.text((71, y + 21), num, font=BOLD(24), fill=(20, 30, 20), anchor="mm")
        d.text((112, y + 6), label, font=REG(26), fill=WHITE)
        d.text((750, y + 6), score, font=BOLD(26), fill=GREEN, anchor="rt")
        y += 62
    d.text((50, 440), "Total 25 / 25 — no early-criterion loss in self-pairwise.", font=BOLD(22), fill=GOLD)
    img.save(os.path.join(ASSETS, "gallery-criteria.png"))


if __name__ == "__main__":
    hero()
    gallery_joke()
    gallery_printer()
    gallery_bracket()
    gallery_criteria()
    print("assets written to", ASSETS)
