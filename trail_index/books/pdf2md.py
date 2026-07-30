"""pdf2md.py — Convert PDF to structured markdown using PyMuPDF.
Usage: python3 pdf2md.py <input.pdf> [output.md]

Preserves: headings, paragraphs, code blocks, lists.
Extracts: code snippets, type signatures, definitions.
"""

import sys, re, pathlib
import fitz


def is_heading(text: str, font_size: float, base_size: float) -> bool:
    ratio = font_size / base_size if base_size > 0 else 1
    return ratio > 1.15 or (text.strip().isupper() and len(text) < 80)


def is_code(text: str) -> bool:
    code_patterns = [
        r'^  [a-z]', r'^data\s', r'^module\s', r'^import\s', r'^public\s',
        r'^export\s', r'^record\s', r'^interface\s', r'^\w+\s*:', r'^\w+\s*=',
        r'^\| ', r'^>>=', r'^->', r'=>', r'::', r'->\s',
    ]
    return any(re.match(p, text) for p in code_patterns)


def is_list_item(text: str) -> bool:
    return bool(re.match(r'^\s*[-*\d+.]\s', text))


def pdf_to_markdown(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    output = []
    base_font_size = 11

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        prev_y = 0
        prev_was_code = False

        for block in blocks:
            if block["type"] != 0:  # 0 = text block
                continue

            text = ""
            font_sizes = []
            for line in block["lines"]:
                for span in line["spans"]:
                    text += span["text"]
                    font_sizes.append(span["size"])
                text += "\n"

            text = text.strip()
            if not text:
                continue

            avg_font = sum(font_sizes) / len(font_sizes) if font_sizes else base_font_size
            bbox = block["bbox"]
            y_pos = bbox[1]

            is_code_block = is_code(text) and not is_heading(text, avg_font, base_font_size)
            is_h = is_heading(text, avg_font, base_font_size)
            is_li = is_list_item(text)

            # Spacing between blocks
            if prev_y > 0 and y_pos - prev_y > 15:
                output.append("")

            if is_h:
                level = min(6, max(1, int(6 - avg_font / base_font_size * 2)))
                output.append(f"{'#' * level} {text}")
            elif is_code_block and not prev_was_code:
                language = "idris" if any(kw in text for kw in ["module", "data ", "import ", "public ", "record "]) else ""
                output.append(f"```{language}")
                output.append(text)
                output.append("```")
            elif is_code_block:
                output.append(text)
                output.append("```")
            elif is_li:
                output.append(text)
            else:
                output.append(text)

            prev_y = bbox[3]
            prev_was_code = is_code_block

        if page_num < len(doc) - 1:
            output.append("\n---\n")

    doc.close()
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pdf_path = sys.argv[1]
    md_path = sys.argv[2] if len(sys.argv) > 2 else str(pathlib.Path(pdf_path).with_suffix(".md"))

    print(f"Converting: {pdf_path} → {md_path}")
    md = pdf_to_markdown(pdf_path)
    pathlib.Path(md_path).write_text(md)
    print(f"Done. {len(md)} chars written.")


if __name__ == "__main__":
    main()
