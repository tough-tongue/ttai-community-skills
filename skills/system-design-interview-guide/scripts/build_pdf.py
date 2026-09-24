#!/usr/bin/env python3
"""Build a styled A4 PDF from a study-guide markdown file.

Pipeline: pandoc (TOC + cover) -> strip pandoc title header -> headless Chrome print
-> contact sheet PNG for layout QA. Diagrams must already be rendered to PNG next to
the markdown (see render_diagrams.sh); image paths in the markdown are relative.

Usage:
  build_pdf.py guide.md --title "Designing X" --subtitle "..." \
      --meta "Difficulty=Medium" --meta "Primary source=..." \
      --out outputs/Designing_X.pdf [--first-break "part-1-the-problem"]

--first-break: id of the first H1 that should start on a fresh page after the
"How to use" intro (pandoc slugifies headings: lowercase, spaces->hyphens).
Defaults to the first H1 whose text starts with "Part 1".
"""
import argparse, glob, html, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")


def find_chrome():
    """$CHROME_PATH, else the first Chrome/Chromium found on PATH or in /Applications."""
    if os.environ.get("CHROME_PATH"):
        return os.environ["CHROME_PATH"]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    for path in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                 "/Applications/Chromium.app/Contents/MacOS/Chromium"):
        if os.path.exists(path):
            return path
    sys.exit("Chrome/Chromium not found; set CHROME_PATH")


CHROME = find_chrome()

ap = argparse.ArgumentParser()
ap.add_argument("markdown")
ap.add_argument("--title", required=True)
ap.add_argument("--subtitle", default="")
ap.add_argument("--meta", action="append", default=[], help="Label=Value, repeatable")
ap.add_argument("--out", required=True)
ap.add_argument("--first-break", default=None)
ap.add_argument("--no-contact-sheet", action="store_true")
a = ap.parse_args()

md = os.path.abspath(a.markdown)
workdir = os.path.dirname(md)
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)

# --- cover -------------------------------------------------------------------
rows = "\n".join(
    f"    <b>{html.escape(k.strip())}:</b> {v.strip()}<br/>"
    for k, v in (m.split("=", 1) for m in a.meta)
)
cover = (open(os.path.join(ASSETS, "cover_template.html")).read()
         .replace("{{TITLE}}", html.escape(a.title))
         .replace("{{SUBTITLE}}", html.escape(a.subtitle))
         .replace("{{META_ROWS}}", rows))
open(os.path.join(workdir, "_cover.html"), "w").write(cover)

# --- pandoc ------------------------------------------------------------------
body = os.path.join(workdir, "_body.html")
subprocess.run(["pandoc", md, "-f", "markdown+pipe_tables", "-t", "html5", "--standalone",
                "--toc", "--toc-depth=2", "--css", os.path.join(ASSETS, "style.css"),
                "--metadata", f"title={a.title}", "-B", os.path.join(workdir, "_cover.html"),
                "-o", body], check=True, cwd=workdir)

h = open(body).read()
h = re.sub(r'<header id="title-block-header">.*?</header>', "", h, flags=re.S)
# inline the stylesheet so the HTML is self-contained
css = open(os.path.join(ASSETS, "style.css")).read()
h = re.sub(r'<link rel="stylesheet" href="[^"]*style.css"\s*/?>', f"<style>{css}</style>", h)
# first real Part starts on a fresh page
fb = a.first_break
if not fb:
    m = re.search(r'<h1 id="(part-1[^"]*)">', h)
    fb = m.group(1) if m else None
if fb:
    h = h.replace(f'<h1 id="{fb}">', f'<h1 id="{fb}" style="page-break-before:always">', 1)
final_html = os.path.join(workdir, "_final.html")
open(final_html, "w").write(h)

# --- chrome ------------------------------------------------------------------
out = os.path.abspath(a.out)
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
                "--no-pdf-header-footer", f"--print-to-pdf={out}", f"file://{final_html}"],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
pages = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout
pages = re.search(r"Pages:\s+(\d+)", pages).group(1)
print(f"PDF: {out} ({pages} pages)")

# --- contact sheet -----------------------------------------------------------
if not a.no_contact_sheet:
    from PIL import Image
    sheet = os.path.join(workdir, "_sheet")
    os.makedirs(sheet, exist_ok=True)
    for f in glob.glob(os.path.join(sheet, "*.png")):
        os.remove(f)
    subprocess.run(["pdftoppm", "-r", "28", "-png", out, os.path.join(sheet, "p")], check=True)
    ims = [Image.open(f) for f in sorted(glob.glob(os.path.join(sheet, "p-*.png")))]
    w, hh = ims[0].size
    cols = 7
    rows_n = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * (w + 6), rows_n * (hh + 6)), "#888")
    for i, im in enumerate(ims):
        S.paste(im, ((i % cols) * (w + 6) + 3, (i // cols) * (hh + 6) + 3))
    cs = os.path.join(workdir, "contact_sheet.png")
    S.save(cs)
    print(f"Contact sheet: {cs}  <- view this before presenting")
