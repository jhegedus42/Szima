# Structure Contract

## Document Section Hierarchy

### Front Matter (Roman numeral pagination: i, ii, iii, ...)
1. **Cover page** — Blue background, gold text, title, author, series, crest, publisher
2. **Series page** — "OXFORD LOGIC GUIDES" centered in small caps, series editors listed
3. **Series listing page** — Available books in the series with italic titles
4. **Title page** — Title, author, affiliation, publisher, year
5. **Copyright page** — Publisher details, ISBN, rights, printing data
6. **Dedication page** (optional) — "in memoriam" or similar dedication
7. **Preface** — "PREFACE" heading, personal first-person introduction by the author. Should discuss: motivation for writing, intended audience, prerequisite level, pedagogical approach, topics covered and not covered, acknowledgments. Typically 2-3 pages. Must end with author name, location, and date right-aligned in italic.
8. **Table of Contents** — Chapter and section listings WITH page numbers. Front matter entries also listed.

### Body (Chapters, Arabic pagination: 1, 2, 3, ...)
Each chapter follows this pattern:

```
[Verso page: "This page intentionally left blank" (if needed for recto opening)]

Chapter N (centered, large font)
CHAPTER TITLE (small caps, centered)

N.1 Section Title (bold)
[Body text with inline math and display math]

N.2 Section Title
...

N.K Exercises (last section)
[Numbered exercise list]
```

#### Chapter Opening
- Chapter opens on recto (right/odd) page when possible
- Chapter number centered, large font
- Chapter title in small caps, centered below number
- NO header on chapter opening page
- NO italic summary box at chapter start — begin directly with first section
- First section heading appears below chapter title on same page

#### Section Numbering
- Format: `Chapter.Section` (e.g., 1.1, 1.2, 2.1)
- Sections are the main organizational unit
- No subsections in the reference (flat structure under chapters)

#### Content Elements Within Sections
- **Definitions**: Bold label "Definition X.Y." — defines key terms. Body in roman. Defined term in bold at first occurrence.
- **Theorems**: Bold label "Theorem X.Y." — major results. Statement body in ITALIC.
- **Propositions**: Bold label "Proposition X.Y." — intermediate results. Statement body in ITALIC.
- **Corollaries**: Bold label "Corollary X.Y." — consequences. Statement body in ITALIC.
- **Lemmas**: Bold label "Lemma X.Y." — stepping stones. Statement body in ITALIC.
- **Proofs**: Labeled "Proof." in italic, followed by proof text in roman, ending with qed symbol (□).
- **Remarks**: Bold label "Remark X.Y." — additional notes. Body in roman.
- **Warnings**: Bold + italic label "Warning X.Y." — cautionary notes. Body in roman.
- **Examples**: Introduced with numbering (1., 2., 3.) or inline. Body in roman.
- **Diagrams**: Commutative diagrams illustrating categorical constructions. Inline, centered, no captions.

#### Exercise Sections
- Titled "Exercises" (bold section heading)
- Appear at end of each chapter
- Numbered sequentially (1., 2., 3., ...)
- Mix of computational and proof-based problems
- Approximately 6-10 exercises per chapter
- Each exercise should be substantive — not trivial one-liners

### Back Matter
1. **References/Bibliography** — Full academic citations. Numbered or alphabetical. Contains cited works and recommended further reading.
2. **Index** — Alphabetical two-column index with page references

## Numbering Systems

### Definition/Theorem/Proposition Numbering
- Sequential within each chapter
- Format: `Chapter.SequentialNumber`
- Examples: Definition 1.1, Theorem 1.6, Proposition 2.6, Definition 2.19

### Equation Numbering
- Sequential within each chapter
- Format: `(Chapter.Number)`
- Right-aligned in display math

### Page Numbering
- Front matter: Roman numerals (i, ii, iii, ...)
- Body: Arabic numerals (1, 2, 3, ...)
- Back matter: Continues body numbering

### Cross-References
- Internal references to sections: "Section 1.8", "Section 2.2"
- Internal references to equations: "(1.1)", "(2.3)"
- Internal references to definitions/theorems: "Definition 1.1", "Theorem 1.6"
- Forward references: "will be introduced in Section 1.8"
- Named references: "Cayley's theorem", "the Yoneda Lemma"

## Diagram and Figure Conventions

### Commutative Diagrams
- Objects as single letters (A, B, C, ...) in math italic
- Arrows with or without labels
- Proper arrow rendering (→, ←, ↓, ↑, and diagonal arrows)
- No figure numbers or captions (diagrams are inline)
- Common patterns:
  - Triangle diagrams: A → B → C with A → C (composition)
  - Square diagrams: Commutative squares with four objects
  - Chain diagrams: Longer sequences of objects and arrows
  - Diagrams with named functors: F, G, U between categories

### Diagram Placement
- Centered on page
- Inline with text (not floating figures)
- No captions or figure numbers
- Surrounded by explanatory text
- Use proper arrow characters or rendering, NOT ASCII art approximations

## Mathematical Notation Conventions

### Categories
- Boldface for named categories: **Sets**, **Pos**, **Groups**, **Cat**, **Top**, **Rel**, **Mon**, **Graph**
- Objects: Italic capitals (A, B, C)
- Arrows/morphisms: Italic lowercase (f, g, h)
- Composition: g ∘ f (small circle operator)
- Identity: 1_A
- Opposite category: C^op
- Product category: C × D
- Slice category: C/C
- Coslice category: C/C

### Functors
- Boldface or uppercase italic (F, G, U)
- Category of categories: **Cat**
- Forgetful functor: U
- Free functor: F
- Identity functor: 1_C

### Natural Transformations
- Greek letters (α, β, η, ε)
- Vertical composition: β ∘ α
- Horizontal composition: β * α

### Special Objects and Constructions
- Terminal object: 1
- Initial object: 0
- Product: A × B with projections p1, p2
- Coproduct: A + B with injections q1, q2
- Exponential: B^A or B^A
- Equalizer: eq(f, g)
- Coequalizer: coequalizer(f, g)
- Pullback: A ×_C B
- Pushout: A +_C B

## Table of Contents Structure

```
Contents
Preface ........................................................ vi

1  Categories .................................................. 1
   1.1  Introduction .......................................... 1
   1.2  Functions of sets ..................................... 3
   1.3  Definition of a category .............................. 4
   1.4  Examples of categories ................................ 5
   1.5  Isomorphisms .......................................... 11
   1.6  Constructions on categories ........................... 13
   1.7  Free categories ....................................... 16
   1.8  Foundations: large, small, and locally small ......... 21
   1.9  Exercises ............................................. 23

2  Abstract structures ......................................... 25
   ...

References ................................................... 249
Index ........................................................ 251
```

## Index Structure

- Two-column format
- Alphabetical ordering
- Main entries in regular weight
- Sub-entries indented
- Page numbers: italic for definition pages, regular for references
- Cross-references: "see", "see also", "contd."
- Mathematical symbols indexed at start (0, 1, 2, 3, ...)
- Named categories indexed: **Sets**, **Pos**, **Cat**, etc.

## Content Depth and Expansion Guidance

The reference is 269 pages. When generating content, aim for comparable depth:

- **Each chapter**: 15-30 pages of body content (excluding exercises)
- **Each section**: 3-8 pages with multiple examples and detailed proofs
- **Definitions**: Include full formal definitions with numbered conditions
- **Examples**: Multiple concrete examples per concept (3-5 minimum), fully worked out
- **Proofs**: Complete rigorous proofs, not sketches (unless marked as such)
- **Diagrams**: Include commutative diagrams at every opportunity where they aid understanding
- **Exercises**: 6-10 per chapter, substantive — mix of verification, construction, and proof problems
- **Remarks**: Add contextual remarks connecting to applications and other areas

### Pedagogical Content Flow Pattern
Each section follows a consistent pattern:
1. **Introduction/motivation** — Why the concept matters, what problem it solves
2. **Formal definition** — Complete definition with numbered conditions
3. **Concrete examples** — 3-5 fully worked out examples (numbered 1., 2., 3., ...)
4. **Propositions and theorems** — Key properties and results with ITALIC statement text
5. **Proofs** — Rigorous proofs, often with commutative diagrams
6. **Remarks** — Additional context, connections, and cautions
7. **Exercises** — Practice problems at chapter end

### Preface Content Requirements
The preface must be written in first person by the author and should include:
- Motivation for the book (why another textbook on this topic?)
- Description of the intended audience and prerequisites
- Discussion of the pedagogical approach
- Overview of topics covered
- Mention of topics deliberately excluded
- Personal acknowledgments to colleagues, students, mentors
- Author name, location, and date at the end (right-aligned, italic)
