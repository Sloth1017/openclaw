"""
Resume PDF generator — converts Polinger resume markdown to PDF with correct alignment.
Usage: python3 generate_pdf.py <input.md> <output.pdf>
"""

import sys
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ── Colours ──────────────────────────────────────────────────────────────────
BLACK  = (30,  30,  30)
GREY   = (100, 100, 100)
RULE   = (187, 187, 187)

# ── Layout constants (mm) ────────────────────────────────────────────────────
PAGE_W        = 210
PAGE_H        = 297
MARGIN_L      = 18
MARGIN_R      = 18
MARGIN_T      = 16
MARGIN_B      = 16
CONTENT_W     = PAGE_W - MARGIN_L - MARGIN_R

NAME_SIZE     = 22
CONTACT_SIZE  = 8.5
SECTION_SIZE  = 9
JOB_SIZE      = 9.5
META_SIZE     = 8.5
BODY_SIZE     = 8.5

BULLET        = "\u2022"
BULLET_INDENT = 4    # mm from left margin to bullet
FONT_DIR      = "/usr/share/fonts/truetype/dejavu"


class ResumePDF(FPDF):

    FONT = "DejaVu"

    def header(self): pass
    def footer(self): pass

    def rgb(self, t):
        self.set_text_color(*t)

    def rule(self, thickness=0.5):
        self.set_draw_color(*RULE)
        self.set_line_width(thickness)
        self.line(MARGIN_L, self.get_y(), PAGE_W - MARGIN_R, self.get_y())

    def vspace(self, mm):
        self.ln(mm)

    # ── Name + contact ────────────────────────────────────────────────────────

    def name_line(self, text):
        self.set_font(self.FONT, "B", NAME_SIZE)
        self.rgb(BLACK)
        self.cell(CONTENT_W, 10, text,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def contact_line(self, text):
        self.set_font(self.FONT, "", CONTACT_SIZE)
        self.rgb(GREY)
        self.cell(CONTENT_W, 5, text,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.vspace(1)
        self.rule(0.75)

    # ── Section heading ───────────────────────────────────────────────────────

    def section_heading(self, text):
        self.vspace(4)
        self.rule(0.5)
        self.vspace(3)
        self.set_font(self.FONT, "B", SECTION_SIZE)
        self.rgb(BLACK)
        self.cell(CONTENT_W, 5, text.upper(),
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.vspace(1)

    # ── Job title + meta ──────────────────────────────────────────────────────

    def job_title(self, title):
        self.vspace(3)
        self.set_font(self.FONT, "B", JOB_SIZE)
        self.rgb(BLACK)
        self.multi_cell(CONTENT_W, 5, title,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def job_meta(self, meta):
        self.set_font(self.FONT, "", META_SIZE)
        self.rgb(GREY)
        self.cell(CONTENT_W, 4.5, meta,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.vspace(1)

    # ── Bullet point (wrapped lines align with first line text) ───────────────

    def bullet_point(self, text):
        self.set_font(self.FONT, "", BODY_SIZE)
        self.rgb(BLACK)

        bullet_str = BULLET + "  "
        bullet_w   = self.get_string_width(bullet_str)
        x0         = MARGIN_L + BULLET_INDENT
        text_x     = x0 + bullet_w
        text_w     = CONTENT_W - BULLET_INDENT - bullet_w

        # Word-wrap manually so we control the x position of every line
        words  = text.split()
        lines  = []
        cur    = []
        for word in words:
            test = " ".join(cur + [word])
            if self.get_string_width(test) <= text_w:
                cur.append(word)
            else:
                if cur:
                    lines.append(" ".join(cur))
                cur = [word]
        if cur:
            lines.append(" ".join(cur))

        y0 = self.get_y()

        # Bullet symbol on first line
        self.set_xy(x0, y0)
        self.cell(bullet_w, 4.5, bullet_str,
                  new_x=XPos.RIGHT, new_y=YPos.TOP)

        # Text lines — all starting at text_x
        for i, line in enumerate(lines):
            if i == 0:
                self.set_xy(text_x, y0)
            else:
                self.set_xy(text_x, self.get_y())
            self.cell(text_w, 4.5, line,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.vspace(0.5)

    # ── Body text (summary paragraph) ────────────────────────────────────────

    def body_text(self, text):
        self.set_font(self.FONT, "", BODY_SIZE)
        self.rgb(BLACK)
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, 5, text,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ── Simple line (education, certs, skills) ────────────────────────────────

    def simple_line(self, text):
        self.set_font(self.FONT, "", BODY_SIZE)
        self.rgb(BLACK)
        self.set_x(MARGIN_L)
        self.multi_cell(CONTENT_W, 5, text,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# ── Markdown parser ───────────────────────────────────────────────────────────

def parse_md(path):
    with open(path) as f:
        lines = [l.rstrip() for l in f.readlines()]

    sections = []
    current  = None

    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            sections.append({"type": "name", "text": line[2:].strip()})

        elif "|" in line and not line.startswith("#") and not line.startswith("-") and current is None:
            sections.append({"type": "contact", "text": line.strip()})

        elif line.startswith("## "):
            current = {"type": "section", "title": line[3:].strip(), "items": []}
            sections.append(current)

        elif line.startswith("### "):
            if current:
                current["items"].append({"type": "job", "title": line[4:].strip(), "bullets": []})

        elif line.startswith("- ") and current:
            text = line[2:].strip()
            if current["items"] and current["items"][-1]["type"] == "job":
                current["items"][-1]["bullets"].append(text)
            else:
                current["items"].append({"type": "bullet", "text": text})

        elif line and not line.startswith("#") and not line.startswith("-") and not line.startswith("---"):
            if current:
                current["items"].append({"type": "text", "text": line.strip()})

    return sections


# ── PDF builder ───────────────────────────────────────────────────────────────

def build_pdf(sections, out_path):
    pdf = ResumePDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(MARGIN_L, MARGIN_T, MARGIN_R)
    pdf.set_auto_page_break(True, MARGIN_B)
    pdf.add_font("DejaVu",  style="",  fname=f"{FONT_DIR}/DejaVuSans.ttf")
    pdf.add_font("DejaVu",  style="B", fname=f"{FONT_DIR}/DejaVuSans-Bold.ttf")
    pdf.add_page()

    for item in sections:
        t = item["type"]

        if t == "name":
            pdf.name_line(item["text"])

        elif t == "contact":
            pdf.contact_line(item["text"])

        elif t == "section":
            pdf.section_heading(item["title"])
            for si in item["items"]:
                if si["type"] == "job":
                    parts = [p.strip() for p in si["title"].split("|")]
                    title = parts[0]
                    meta  = "  \u00b7  ".join(parts[1:]) if len(parts) > 1 else ""
                    pdf.job_title(title)
                    if meta:
                        pdf.job_meta(meta)
                    for b in si["bullets"]:
                        pdf.bullet_point(b)
                elif si["type"] == "text":
                    pdf.body_text(si["text"])
                elif si["type"] == "bullet":
                    pdf.bullet_point(si["text"])

    pdf.output(out_path)
    print(f"\u2713 Written: {out_path}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate_pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    sections = parse_md(sys.argv[1])
    build_pdf(sections, sys.argv[2])
