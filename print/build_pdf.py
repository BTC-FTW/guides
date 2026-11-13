#!/usr/bin/env python3
"""Build the print version of the seed recovery procedure.

Renders PART 1 and PART 2 from their Markdown sources into one A4 PDF, so the
printed copy can never drift from the published text. Only the small Markdown
subset used by those two files is supported.

Needs Google Chrome (headless) for the HTML to PDF step. No other packages.

    python3 print/build_pdf.py
"""

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SOURCES = [
    REPO / "bitcoin-seed-recovery" / "SLIP39-Recovery-Card.md",
    REPO / "bitcoin-seed-recovery" / "Passphrase-And-Verification.md",
]
OUTPUT = HERE / "seed-recovery-procedure.pdf"
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]

CSS = """
@page {
  size: A4;
  margin: 13mm 15mm 15mm 15mm;
  @bottom-left  { content: "Seed recovery procedure, contains no secrets";
                  font: 8pt "Helvetica Neue", Arial, sans-serif; color: #666; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages);
                  font: 8pt "Helvetica Neue", Arial, sans-serif; color: #666; }
}
html { font: 9.9pt/1.31 "Helvetica Neue", Helvetica, Arial, sans-serif; color: #000; }
body { margin: 0; }
h1 { font-size: 17pt; margin: 0 0 8pt; padding-bottom: 4pt; border-bottom: 2pt solid #000; }
h2 { font-size: 12.5pt; margin: 11pt 0 5pt; padding-top: 4pt; border-top: 0.75pt solid #999; }
h3 { font-size: 11pt; margin: 10pt 0 4pt; }
h1, h2, h3, p.step { break-after: avoid; }
p { margin: 0 0 6pt; }
ul, ol { margin: 0 0 6pt; padding-left: 16pt; }
li { margin: 0 0 2pt; }
li > ul { margin: 2pt 0 0; }
code, pre { font-family: Menlo, "DejaVu Sans Mono", monospace; }
code { font-size: 9.3pt; background: #eee; padding: 0 2pt; border-radius: 2pt; }
pre {
  font-size: 9.6pt; line-height: 1.36; background: #eee; border: 0.75pt solid #888;
  padding: 4pt 7pt; margin: 2pt 0 6pt; white-space: pre-wrap; overflow-wrap: anywhere;
  break-inside: avoid;
}
pre.fillin { line-height: 2.1; background: #fff; }
pre code { background: none; padding: 0; font-size: inherit; }
.badge {
  font: bold 7.5pt "Helvetica Neue", Arial, sans-serif; letter-spacing: 0.3pt;
  border: 0.75pt solid #000; border-radius: 2pt; padding: 0 3pt; white-space: nowrap;
}
blockquote {
  margin: 3pt 0 7pt; padding: 4pt 8pt; border: 1.2pt solid #000; background: #fff6e0;
  break-inside: avoid;
}
blockquote p:last-child { margin-bottom: 0; }
table { border-collapse: collapse; width: 100%; margin: 2pt 0 8pt; break-inside: avoid; }
th, td { border: 0.75pt solid #888; padding: 2.5pt 5pt; text-align: left; vertical-align: top; }
th { background: #ddd; }
td code { white-space: nowrap; }
.part-break { break-before: page; }
"""


def inline(text):
    """Render inline Markdown: code spans, bold, italic, links."""
    spans = []

    def stash(match):
        content = match.group(1)
        if content == "[ONE LINE]":
            spans.append('<span class="badge">ONE LINE</span>')
        else:
            spans.append("<code>" + html.escape(content, quote=False) + "</code>")
        return "\x00%d\x00" % (len(spans) - 1)

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    # Links are shown as their text only: nothing on paper is clickable.
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"<strong>\1</strong>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


LIST_ITEM = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def render_list(lines):
    """Render a (possibly nested) list from its raw lines."""
    first = LIST_ITEM.match(lines[0])
    indent = len(first.group(1))
    tag = "ol" if first.group(2)[0].isdigit() else "ul"
    items = []
    for line in lines:
        m = LIST_ITEM.match(line)
        if m and len(m.group(1)) == indent:
            items.append([m.group(3)])
        else:
            items[-1].append(line)
    out = ["<%s>" % tag]
    for item in items:
        text, nested = [item[0]], []
        for line in item[1:]:
            if nested or (LIST_ITEM.match(line) and len(LIST_ITEM.match(line).group(1)) > indent):
                nested.append(line)
            else:
                text.append(line.strip())
        body = inline(" ".join(text))
        if nested:
            body += render_list(nested)
        out.append("<li>" + body + "</li>")
    out.append("</%s>" % tag)
    return "".join(out)


def render_table(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    head, body = rows[0], rows[2:]
    out = ["<table><tr>"] + ["<th>%s</th>" % inline(c) for c in head] + ["</tr>"]
    for row in body:
        out += ["<tr>"] + ["<td>%s</td>" % inline(c) for c in row] + ["</tr>"]
    out.append("</table>")
    return "".join(out)


def render(md):
    """Render a Markdown document to an HTML fragment."""
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped == "---":
            i += 1
        elif stripped.startswith("```"):
            j = i + 1
            while not lines[j].strip().startswith("```"):
                j += 1
            code = "\n".join(lines[i + 1:j])
            cls = ' class="fillin"' if "____" in code else ""
            out.append("<pre%s><code>%s</code></pre>" % (cls, html.escape(code, quote=False)))
            i = j + 1
        elif re.match(r"^#{1,3} ", line):
            level = len(line) - len(line.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (level, inline(line[level:].strip()), level))
            i += 1
        elif stripped.startswith(">"):
            j = i
            while j < len(lines) and lines[j].strip().startswith(">"):
                j += 1
            inner = "\n".join(re.sub(r"^\s*> ?", "", l) for l in lines[i:j])
            out.append("<blockquote>%s</blockquote>" % render(inner))
            i = j
        elif stripped.startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            out.append(render_table(lines[i:j]))
            i = j
        elif LIST_ITEM.match(line):
            j = i + 1
            while j < len(lines) and lines[j].strip() and (
                LIST_ITEM.match(lines[j]) or lines[j].startswith(" ")
            ):
                j += 1
            out.append(render_list(lines[i:j]))
            i = j
        else:
            j = i
            while j < len(lines) and lines[j].strip() and not re.match(
                r"^(#{1,3} |```|>|\||---$)", lines[j].strip()
            ) and not LIST_ITEM.match(lines[j]):
                j += 1
            text = " ".join(l.strip() for l in lines[i:j])
            # Step labels, lead-ins ending in ":" and any paragraph directly
            # above a code box stay on the page of what follows.
            k = j
            while k < len(lines) and not lines[k].strip():
                k += 1
            above_code = k < len(lines) and lines[k].strip().startswith("```")
            keep = (re.match(r"^\*\*[A-Z]\d+\.\*\*", text) or text.endswith(":")
                    or above_code)
            cls = ' class="step"' if keep else ""
            out.append("<p%s>%s</p>" % (cls, inline(text)))
            i = j
    return "\n".join(out)


def find_chrome():
    for candidate in CHROME_CANDIDATES:
        path = candidate if Path(candidate).is_file() else shutil.which(candidate)
        if path:
            return path
    sys.exit("Google Chrome or Chromium not found.")


def main():
    parts = [render(p.read_text(encoding="utf-8")) for p in SOURCES]
    body = '\n<div class="part-break"></div>\n'.join(parts)
    page = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>Seed Recovery Procedure</title><style>%s</style></head>"
        "<body>%s</body></html>" % (CSS, body)
    )
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "procedure.html"
        src.write_text(page, encoding="utf-8")
        subprocess.run(
            [
                find_chrome(),
                "--headless=new",
                "--disable-gpu",
                "--no-first-run",
                "--user-data-dir=" + str(Path(tmp) / "profile"),
                "--no-pdf-header-footer",
                "--print-to-pdf=" + str(OUTPUT),
                src.as_uri(),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    # Chrome stamps the exact build time. Round it to 12:00 UTC, like the
    # commit dates in this repository, so the file shows no time of day.
    # The replacement keeps the byte length, so the PDF offsets stay valid.
    pdf = OUTPUT.read_bytes()
    pdf = re.sub(
        rb"/(CreationDate|ModDate) \(D:(\d{8})\d{6}",
        rb"/\1 (D:\g<2>120000",
        pdf,
    )
    OUTPUT.write_bytes(pdf)
    print("Wrote", OUTPUT.relative_to(REPO))


if __name__ == "__main__":
    main()
