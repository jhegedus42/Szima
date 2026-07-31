---
name: category-theory-textbook
description: Create academic mathematical textbooks, lecture notes, and educational materials in the classical LaTeX academic style. Use when the agent needs to produce structured mathematical documents featuring definitions, theorems, proofs, commutative diagrams, examples, and exercises. Applies to tasks involving category theory, abstract algebra, topology, logic, type theory, or any graduate-level mathematics exposition requiring rigorous theorem-proof formatting, numbered mathematical environments, and diagram-heavy academic presentation. Supports PDF and DOCX output.
---

# Category Theory Textbook Skill

## Reference Information

- **Reference source type**: Uploaded artifact (PDF)
- **Reference artifact**: "Category Theory" by Steve Awodey (Oxford Logic Guides 49, Oxford University Press, 2006)
- **Reference File Type**: PDF
- **Style contract**: See [references/style_contract.md](references/style_contract.md)
- **Structure contract**: See [references/structure_contract.md](references/structure_contract.md)

## Style Summary

This skill produces documents in the classical LaTeX academic mathematical style:

- **Fonts**: Computer Modern family (serif body, bold sans headings, italic emphasis). For non-LaTeX output, substitute with Latin Modern or New Computer Modern to preserve the visual character.
- **Layout**: Single column, generous margins (~1 inch), justified text, first-line paragraph indent
- **Color**: Pure monochrome interior — black text on white ONLY. Cover uses deep blue (#002147) + gold (#C5A000).
- **Headers**: Section title in small caps (even pages, centered), chapter title in small caps (odd pages, centered). Page numbers on outer margins.
- **Math**: Inline math in body text; display math centered with right-aligned equation numbers

Read the full style contract for typography details, CJK font strategy, and cover design.

## CRITICAL Style Rules (Must Follow)

These rules are derived from direct comparison with the reference. Violations produce visibly wrong output.

1. **NO colored text, NO colored backgrounds, NO colored borders in body content** — pure black on white throughout
2. **NO colored border boxes** for definitions, theorems, propositions, examples, or proofs. Use simple bold inline labels:
   - Correct: `Definition 1.1. A category consists of...`
   - Correct: `Theorem 1.6. Every category C...` (statement in italic)
   - Correct: `Proof. Define...` (ends with □)
   - WRONG: Any box, shaded background, left border, or colored label
3. **Theorem/Proposition/Corollary/Lemma statements in ITALIC** — distinguishes them from surrounding text
4. **NO chapter-opening summary boxes** — chapters begin directly with the first section
5. **NO bullet points for main exposition** — use prose paragraphs, numbered conditions, or numbered examples
6. **Proofs end with QED** — the hollow square symbol □
7. **Running headers centered in small caps** — not left-aligned, not gray
8. **Commutative diagrams with proper arrows** — use proper arrow rendering (→, ←, ↗, etc.), NOT ASCII art or text approximations
9. **Definitions: defined term in bold** at first occurrence within the definition
10. **Named categories in boldface**: **Sets**, **Pos**, **Groups**, **Cat**, **Top**, **Rel**, **Mon**

## Structure Summary

### Section Hierarchy

```
Front Matter: Cover > Series > Series Listing > Title > Copyright > Dedication > Preface > TOC
Body: Chapter > Section > Content
Back Matter: References > Index
```

### Mathematical Environments (numbered Chapter.Sequential)

| Environment | Label Style | Body Style | End Marker |
|-------------|-------------|------------|------------|
| Definition | Bold "Definition X.Y." | Roman; term bold | None |
| Theorem | Bold "Theorem X.Y." | Italic | None |
| Proposition | Bold "Proposition X.Y." | Italic | None |
| Corollary | Bold "Corollary X.Y." | Italic | None |
| Lemma | Bold "Lemma X.Y." | Italic | None |
| Proof | Italic "Proof." | Roman | QED symbol □ |
| Remark | Bold "Remark X.Y." | Roman | None |
| Warning | Bold + italic "Warning X.Y." | Roman | None |
| Example | Numbered (1., 2., 3.) | Roman | None |

### Content Flow per Chapter
1. Motivation/introduction
2. Formal definition (numbered conditions)
3. Concrete examples (numbered 1., 2., 3. — fully worked out)
4. Propositions and theorems (with proofs)
5. Remarks and connections
6. Exercises (collected at chapter end)

### Diagram Conventions
- Commutative diagrams: centered, inline with text, no captions
- Objects: single italic capitals (A, B, C)
- Arrows: labeled morphisms, composition g ∘ f
- Named categories in bold: **Sets**, **Pos**, **Groups**, **Cat**
- Render with proper arrow characters, NOT ASCII approximations

Read the full structure contract for numbering systems, notation conventions, TOC/index formatting, and content depth guidance.

## Output Policy

### Supported Outputs
- **PDF** — Primary output; preserves the LaTeX-typeset academic appearance
- **DOCX** — Editable document format
- **PPTX** — Not applicable for this textbook format

### Default Output
- If user does not specify: **PDF** (the reference is a native PDF with LaTeX typesetting)
- If user requests an editable document: **DOCX**

## Font Handling

- **Primary language**: English (Latin script)
- **Reference fonts**: Computer Modern (CMR, CMBX, CMTI, CMMI, CMSY, CMEX)
- **Typography family**: Classical LaTeX serif system
- **For CJK content**: Use Latin Modern for Latin text + Noto Serif CJK for CJK text. Latin Modern is metrically compatible with Computer Modern.
- **Document components**: Apply one consistent font strategy across all elements — body text, headings, math environments, captions, headers, footers, cover text, and index

## Page Break Rules

- Chapter opens on a new recto (odd/right) page when possible
- Preceding verso may display "This page intentionally left blank" if needed
- Section starts on same page (no forced page break)
- Display math may break across pages
- Exercises section starts on same page as preceding content or new page if needed
- References begin on new page
- Index begins on new page

## Cover Design Rules

- Deep solid Oxford blue (#002147) background
- Gold/yellow (#C5A000) text throughout
- Series name at top in small caps: "OXFORD LOGIC GUIDES • N"
- Title in large serif
- Horizontal rule separator
- Author name in small caps
- Publisher crest centered
- Publisher name at bottom in small caps
- NO beige/tan. NO modern geometric decorations. NO diamond shapes.

## Content Depth Guidance

The reference is 269 pages. Generated content must be comparably deep:
- Each chapter: 15-30 pages body content + exercises
- Each section: 3-8 pages with multiple examples and detailed proofs
- Definitions: full formal with numbered conditions
- Examples: 3-5 fully worked out concrete examples per concept
- Proofs: complete rigorous proofs (not sketches unless marked)
- Diagrams: include at every opportunity
- Exercises: 6-10 per chapter, substantive
- Preface: personal, first-person, 2-3 pages with acknowledgments

## Key Style Rules Checklist

1. **No colored text in body** — pure black on white
2. **No bullet points for main exposition** — prose, numbered conditions, or numbered examples
3. **Theorem statements in italic**
4. **Proofs end with qed** — □
5. **Running headers centered in small caps**
6. **Equation numbers right-aligned** — format (Chapter.Number)
7. **Definition terms in bold** — at first definition occurrence
8. **Generous whitespace around display math**
9. **Diagrams inline with proper arrows** — not floating, no captions
10. **Preface: personal first-person** with author signature block at end
11. **Named categories boldface**: **Sets**, **Pos**, **Groups**, **Cat**, **Top**
12. **Page numbers on outer margins** (left on even, right on odd)
13. **Front matter**: Roman numerals; **Body**: Arabic numerals
14. **References/Bibliography** section at end before index
15. **Two-column index** with italic page numbers for definitions
