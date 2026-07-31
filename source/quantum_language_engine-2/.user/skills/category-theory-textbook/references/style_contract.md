# Style Contract

## Reference Source

- **Type**: Uploaded artifact (PDF)
- **Artifact**: "Category Theory" by Steve Awodey (Oxford Logic Guides 49, Oxford University Press, 2006)
- **Pages**: 269
- **Reference File Type**: PDF

## Typography System

### Reference Fonts (extracted via fitz)
The book uses the standard Computer Modern font family (classic LaTeX):

| Font ID | Family | Usage |
|---------|--------|-------|
| CMR10, CMR9, CMR7, CMR5, CMR12 | Computer Modern Roman | Body text, headings |
| CMTI9, CMTI10, CMTI12 | Computer Modern Text Italic | Emphasis, theorem statements |
| CMBX10, CMBX12, CMBX7 | Computer Modern Bold Extended | Section headings, definition/theorem labels |
| CMMI10, CMMI7 | Computer Modern Math Italic | Mathematical variables |
| CMSY10, CMSY9, CMSY7 | Computer Modern Math Symbols | Mathematical symbols |
| CMEX10 | Computer Modern Math Extension | Large delimiters, summation |
| LINE10 | Line font (for diagrams) | Commutative diagram arrows |
| MSBM10 | AMS Blackboard Bold | Blackboard bold symbols |

### Typography Characteristics
- **Style**: Classical academic mathematical typesetting (LaTeX/TeX)
- **Body**: Serif, 10pt, justified text
- **Heading hierarchy**: Bold extended for chapter/section, roman for subsection
- **Math mode**: Inline math within body text; display math centered with equation numbers
- **Emphasis**: Italic for defined terms, theorem statements, and emphasis
- **Small caps**: Used in running headers (e.g., "CATEGORIES", "EXAMPLES OF CATEGORIES")

### Font Strategy for CJK Content
- When content includes CJK characters, use Latin Modern (LM Roman, LM Sans, LM Mono) for Latin text and Noto Serif CJK or Source Han Serif for CJK text
- Latin Modern is the OpenType successor to Computer Modern and preserves the same visual character
- Maintain the same typographic hierarchy: serif body, bold sans for headings, italic for emphasis
- Apply one consistent font strategy across all document elements

## Color Palette

- **Interior**: STRICTLY black text on white background — NO colors anywhere in body content
- **Cover**: Deep Oxford blue (#002147) background with gold/yellow (#C5A000) text
- **No colored accents** in body content — pure monochrome throughout
- **No colored border boxes** for definitions, theorems, propositions, examples, or any other environment
- **No background colors** of any kind on interior pages

## Page Layout

- **Single column** layout throughout
- **Page size**: Standard academic book format (approximately 6 x 9 inches / 152 x 229 mm)
- **Margins**: ~1 inch on all sides (LaTeX standard book class: \oddsidemargin, \evensidemargin, \textwidth, \textheight)
- **Line spacing**: Slightly greater than single (LaTeX \baselinestretch ~1.2)
- **Paragraph indent**: First line indent for body paragraphs (no vertical spacing between paragraphs)
- **No bullet points** for main mathematical exposition — use prose, numbered conditions, or numbered examples

## Running Headers and Footers

- **Even pages**: Page number on the LEFT margin; Section title in small caps CENTERED
- **Odd pages**: Chapter title in small caps CENTERED; Page number on the RIGHT margin
- **Chapter opening pages**: No header; page number may be at bottom center or absent
- **No footers** on most pages except page numbers as described above
- **Front matter**: Page numbers in Roman numerals, positioned same as body

## Mathematical Content Styling

### Display Math
- Centered on page
- Equation numbers right-aligned in parentheses: (1.1), (1.2), etc.
- Numbered sequentially within chapters

### Commutative Diagrams
- Properly rendered with arrow fonts (LINE10 or TikZ/xymatrix-quality arrows)
- Objects labeled with letters (A, B, C, etc.) in math italic
- Arrows with labels above/below in math mode
- No colored fills or complex graphical elements
- Centered inline with text, NOT as floating figures
- No captions or figure numbers on diagrams
- Triangle diagrams, square diagrams, and chain sequences all properly arrow-rendered

### Theorem Environments — CRITICAL: NO BOXES, NO COLORS

All theorem environments use SIMPLE BOLD INLINE LABELS followed by text. NO background colors. NO border boxes. NO colored borders.

| Environment | Label Style | Body Style | End Marker |
|-------------|-------------|------------|------------|
| Definition | **Bold** "Definition X.Y." | Roman text; defined term in bold | None |
| Theorem | **Bold** "Theorem X.Y." | Statement in *italic* | None |
| Proposition | **Bold** "Proposition X.Y." | Statement in *italic* | None |
| Corollary | **Bold** "Corollary X.Y." | Statement in *italic* | None |
| Lemma | **Bold** "Lemma X.Y." | Statement in *italic* | None |
| Proof | *Italic* "Proof." | Roman text | QED symbol (□) at end |
| Remark | **Bold** "Remark X.Y." | Roman text | None |
| Warning | **Bold** + *italic* "Warning X.Y." | Roman text | None |
| Example | Numbered (1., 2., 3.) or inline | Roman text | None |

Example of correct styling:
```
Definition 1.1. A category consists of the following data: ...

Theorem 1.6. Every category C with a set of arrows is isomorphic to one
in which the objects are sets and the arrows are functions.

Proof. (sketch) Define the Cayley representation ...
                                         (end of proof)  □

Warning 1.5. Note the two different levels of isomorphisms ...
```

## Cover Design

- **Background**: Dark solid Oxford blue (#002147)
- **Series name** at top: "OXFORD LOGIC GUIDES • 49" in gold small caps
- **Title** in large serif gold text: "Category Theory"
- **Horizontal rule** separator (thin gold line)
- **Author name**: "STEVE AWODEY" in gold small caps
- **Publisher crest/logo** centered (Oxford crest)
- **Publisher name** at bottom: "OXFORD SCIENCE PUBLICATIONS" in gold small caps
- NO beige/tan cover. NO modern geometric decorations. NO diamond shapes.

## Front Matter Pages

1. **Series page** (ii): "OXFORD LOGIC GUIDES" centered in small caps, "Series Editors" in italic, names listed
2. **Series listing page** (iii): "Available books in the series:" with numbered list, titles in italic
3. **Title page** (iv): Title in large serif, author in small caps, affiliation in italic, publisher and year at bottom
4. **Copyright page** (v): Publisher info, ISBN, printing data, copyright notice
5. **Dedication page** (optional): "in memoriam" in italic, name centered — or similar dedication
6. **Preface** (vii+): "PREFACE" heading centered in small caps, body text follows. Written in first person by the author. Personal, discussing motivation, audience, acknowledgments. Page numbers in Roman numerals.
7. **Table of Contents**: "CONTENTS" centered in small caps. Chapter numbers bold, section numbers not bold, page numbers right-aligned. Front matter entries (Preface) also listed with page numbers.

## Back Matter

- **References/Bibliography**: Full citations in standard academic format, numbered or alphabetical
- **Index**: Two-column layout, alphabetical with sub-entries
- Page numbers in index: italicized for definition pages, regular for references
- Cross-references with "see", "see also", "contd."
- Mathematical symbols indexed at start (0, 1, 2, 3, ...)

## Visual Density and Rhythm

- Moderate density: generous whitespace around display math and diagrams
- Clear visual separation between sections via bold headings
- Theorem/proof blocks create rhythmic alternation between definitions and exposition
- Diagrams appear frequently (every 3-5 pages) to illustrate categorical concepts
- Exercises collected at end of each chapter
- Body text: prose paragraphs with first-line indent, NOT bullet-point lists
- NO chapter-opening summary boxes — chapters begin directly with first section content
