"""hungarian_parser.py — Parse text into logical relations via Hungarian case algebra.

Uses Hungarian's agglutinative case system to expose grammatical relations
as explicit logical connectives. Each case suffix IS a logical relation.

Supports two modes:
  1. Direct Hungarian parsing (suffix → case → logic)
  2. English text annotation (grammatical role → Hungarian case → logic)

Usage:
  python3 hungarian_parser.py --text "A kutya üldözi a macskát." --lang hu
  python3 hungarian_parser.py --text "The dog chases the cat." --lang en
"""

import re, sys, json
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════
# Hungarian Case Inventory (22 cases, each → logical relation)
# ═══════════════════════════════════════════════════════════════

CASE_MAP = {
    "∅":     ("NOM", "subject/agent"),
    "-t":    ("ACC", "object/patient"),
    "-nak":  ("DAT", "recipient/purpose → caused_by"),
    "-nek":  ("DAT", "recipient/purpose → caused_by"),
    "-val":  ("INS", "instrument → via/using"),
    "-vel":  ("INS", "instrument → via/using"),
    "-stul": ("COM", "together → conjoined_with"),
    "-stül": ("COM", "together → conjoined_with"),
    "-ért":  ("CAU", "cause/reason → because_of"),
    "-vá":   ("TRA", "transformation → results_in"),
    "-vé":   ("TRA", "transformation → results_in"),
    "-ig":   ("TER", "limit → up_to"),
    "-ba":   ("ILL", "into → specializes_to"),
    "-be":   ("ILL", "into → specializes_to"),
    "-ban":  ("INE", "in → context_of"),
    "-ben":  ("INE", "in → context_of"),
    "-ból":  ("ELA", "out_of → derived_from"),
    "-ből":  ("ELA", "out_of → derived_from"),
    "-hoz":  ("ALL", "toward → targets"),
    "-hez":  ("ALL", "toward → targets"),
    "-höz":  ("ALL", "toward → targets"),
    "-nál":  ("ADE", "at → relative_to"),
    "-nél":  ("ADE", "at → relative_to"),
    "-tól":  ("ABL", "from → originates_in"),
    "-től":  ("ABL", "from → originates_in"),
    "-n":    ("SUP", "on → topic_of"),
    "-on":   ("SUP", "on → topic_of"),
    "-en":   ("SUP", "on → topic_of"),
    "-ön":   ("SUP", "on → topic_of"),
    "-ról":  ("DEL", "about → references"),
    "-ről":  ("DEL", "about → references"),
    "-ra":   ("SUB", "onto → purpose"),
    "-re":   ("SUB", "onto → purpose"),
    "-kor":  ("TEM", "at_time → when"),
    "-ként": ("SOC", "as → in_role_of"),
    "-nként":("DIST", "per → distributively"),
    "-ul":   ("ESS", "as → essentially"),
    "-ül":   ("ESS", "as → essentially"),
    "-lag":  ("MOD", "-wise → modally"),
    "-leg":  ("MOD", "-wise → modally"),
    "-képp": ("CAS", "as → casewise"),
    "-képpen":("CAS","as → casewise"),
}

# Reverse: case_name → suffix
CASE_BY_NAME = {v[0]: k for k, v in CASE_MAP.items()}

# Hungarian suffixes in order of agglutination (longest first for matching)
HUN_SUFFIX_PATTERN = "|".join(sorted(
    [k for k in CASE_MAP if k != "∅"],
    key=len, reverse=True
))

# ═══════════════════════════════════════════════════════════════
# Hungarian Verb Conjugation → Logical Modes
# ═══════════════════════════════════════════════════════════════

DEFINITE_ENDINGS = {
    "om", "od", "ja", "juk", "játok", "ják",
    "öm", "öd", "i", "ük", "itek", "ik",
}

INDEFINITE_ENDINGS = {
    "ok", "sz", "", "unk", "tok", "nak",
    "ek", "öl", "unk", "ötök", "ök",
}

VERB_PERSON = {
    "om": "1SG", "od": "2SG", "ja": "3SG",
    "juk": "1PL", "játok": "2PL", "ják": "3PL",
    "öm": "1SG", "öd": "2SG", "i": "3SG",
    "ük": "1PL", "itek": "2PL", "ik": "3PL",
    "ok": "1SG", "sz": "2SG", "": "3SG",
    "unk": "1PL", "tok": "2PL", "nak": "3PL",
    "ek": "1SG", "öl": "2SG",
    "ötök": "2PL", "ök": "1SG",
}


# ═══════════════════════════════════════════════════════════════
# Data Structures
# ═══════════════════════════════════════════════════════════════

@dataclass
class CaseMarked:
    stem: str
    case: str          # case name (NOM, ACC, etc.)
    suffix: str        # actual suffix string
    role: str          # logical role description

@dataclass
class LogicalRelation:
    subject: str
    verb: str
    object: str
    cases: dict[str, str] = field(default_factory=dict)  # case → noun
    certainty: float = 1.0
    mode: str = "definite"  # definite | indefinite → R | I1

@dataclass
class HungarianParse:
    words: list[CaseMarked]
    verb: Optional[str]
    definiteness: Optional[bool]
    relations: list[LogicalRelation]


# ═══════════════════════════════════════════════════════════════
# Hungarian Parser
# ═══════════════════════════════════════════════════════════════

HUN_SUFFIX_RE = re.compile(f"({HUN_SUFFIX_PATTERN})$")

def parse_hungarian_word(word: str) -> CaseMarked:
    """Decompose a Hungarian word into stem + case suffix."""
    m = HUN_SUFFIX_RE.search(word)
    if m:
        suffix = m.group(1)
        stem = word[:m.start()]
        case_name, role = CASE_MAP.get(suffix, ("UNK", "unknown"))
        return CaseMarked(stem, case_name, suffix, role)
    return CaseMarked(word, "NOM", "∅", "subject/agent — unmarked")


def detect_verb_conjugation(verb: str) -> tuple[Optional[str], Optional[bool]]:
    """Detect person and definiteness from verb ending."""
    for ending in DEFINITE_ENDINGS:
        if verb.endswith(ending):
            person = VERB_PERSON.get(ending, "3SG")
            return person, True  # definite
    for ending in INDEFINITE_ENDINGS:
        if ending and verb.endswith(ending):
            person = VERB_PERSON.get(ending, "3SG")
            return person, False  # indefinite
        if not ending:
            # zero ending = 3SG indefinite
            return "3SG", False
    return None, None


def parse_hungarian_sentence(text: str) -> HungarianParse:
    """Parse a Hungarian sentence into case-marked words and relations."""
    words = text.strip().rstrip(".!?").split()
    parsed_words = []
    verb = None
    definiteness = None

    for w in words:
        cw = parse_hungarian_word(w)
        person, def_ = detect_verb_conjugation(w)
        if person is not None:
            verb = cw.stem
            definiteness = def_
        parsed_words.append(cw)

    # Build relations from case-marked words
    relations = []
    subjects = [w for w in parsed_words if w.case == "NOM" and w != verb]
    objects = [w for w in parsed_words if w.case == "ACC"]

    for subj in subjects or [parsed_words[0]]:
        for obj in objects or [CaseMarked("∅", "ACC", "-t", "unspecified object")]:
            cases = {}
            for w in parsed_words:
                if w.case not in ("NOM", "ACC"):
                    cases[w.case] = w.stem
            rel = LogicalRelation(
                subject=subj.stem,
                verb=verb or "(copula)",
                object=obj.stem,
                cases=cases,
                mode="definite" if definiteness else "indefinite",
            )
            relations.append(rel)

    return HungarianParse(parsed_words, verb, definiteness, relations)


# ═══════════════════════════════════════════════════════════════
# English → Hungarian Case Annotation
# ═══════════════════════════════════════════════════════════════

# English grammatical role → Hungarian case mapping
EN_ROLE_TO_CASE = {
    "subject": "NOM",
    "object": "ACC",
    "indirect_object": "DAT",
    "instrument": "INS",
    "cause": "CAU",
    "result": "TRA",
    "location": "INE",
    "source": "ELA",
    "goal": "ALL",
    "purpose": "SUB",
    "topic": "DEL",
    "time": "TEM",
    "limit": "TER",
    "manner": "MOD",
}

# English prepositions → Hungarian case mapping
EN_PREP_TO_CASE = {
    "by": "INS", "with": "INS", "via": "INS",
    "to": "ALL", "toward": "ALL",
    "from": "ELA", "out_of": "ELA",
    "in": "INE", "inside": "INE",
    "into": "ILL",
    "on": "SUP", "upon": "SUP",
    "about": "DEL", "regarding": "DEL",
    "for": "CAU", "because_of": "CAU",
    "as": "ESS", "as_a": "ESS",
    "until": "TER",
    "at": "ADE",
}

EN_PREP_RE = re.compile(
    r"\b(" + "|".join(sorted(EN_PREP_TO_CASE, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)


def annotate_english(text: str) -> list[LogicalRelation]:
    """Annotate English text with Hungarian case roles."""
    tokens = text.split()
    relations = []
    current_subj = None
    current_obj = None
    current_verb = None
    current_cases = {}
    i = 0

    while i < len(tokens):
        t = tokens[i]
        # Simple subject-verb-object heuristic
        if i == 0:
            current_subj = t
        elif re.match(r'^[a-z]+(s|es|ed|ing)$', t) and t not in EN_PREP_TO_CASE:
            current_verb = t
        else:
            # Check for prepositional phrases
            m = EN_PREP_RE.match(t)
            if m:
                prep = m.group(1).lower()
                case = EN_PREP_TO_CASE.get(prep)
                if case and i + 1 < len(tokens):
                    current_cases[case] = tokens[i + 1]
                    i += 1
            elif current_obj is None and current_verb:
                current_obj = t

        # Form relation when we have subject + verb
        if current_subj and current_verb and i + 1 >= len(tokens):
            if current_obj is None:
                current_obj = "∅"
            rel = LogicalRelation(
                subject=current_subj,
                verb=current_verb,
                object=current_obj,
                cases=dict(current_cases),
                mode="definite",
            )
            relations.append(rel)

        i += 1

    return relations


# ═══════════════════════════════════════════════════════════════
# Export: Hungarian case algebra → JSON for Reader agents
# ═══════════════════════════════════════════════════════════════

def relations_to_json(relations: list[LogicalRelation]) -> str:
    """Serialize logical relations to JSON for the Reader pipeline."""
    output = []
    for r in relations:
        entry = {
            "subject": r.subject,
            "verb": r.verb,
            "object": r.object,
            "cases": r.cases,
            "mode": "R" if r.mode == "definite" else "I1",
            "certainty": r.certainty,
        }
        output.append(entry)
    return json.dumps(output, indent=2, ensure_ascii=False)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Parse text via Hungarian case algebra")
    parser.add_argument("--text", required=True, help="Text to parse (Hungarian or English)")
    parser.add_argument("--lang", choices=["hu", "en"], default="hu",
                        help="Language of input (hu=Hungarian, en=English)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.lang == "hu":
        result = parse_hungarian_sentence(args.text)
        if args.json:
            print(relations_to_json(result.relations))
        else:
            print(f"Verb: {result.verb} (definite={result.definiteness})")
            print("Words:")
            for w in result.words:
                print(f"  {w.stem:<12} → case={w.case:<5} suffix={w.suffix:<6} role={w.role}")
            print("\nRelations:")
            for r in result.relations:
                print(f"  {r.subject} {r.verb} {r.object} [mode={r.mode}]")
                for case, noun in r.cases.items():
                    h_case = CASE_BY_NAME.get(case, case)
                    print(f"    {h_case:<6} ({case:<4}) → {noun}")
    else:
        relations = annotate_english(args.text)
        if args.json:
            print(relations_to_json(relations))
        else:
            print("English → Hungarian case annotation:")
            for r in relations:
                print(f"  {r.subject} {r.verb} {r.object}")
                for case, noun in r.cases.items():
                    h_case = CASE_BY_NAME.get(case, case)
                    print(f"    [{case}] {h_case} → {noun}")


if __name__ == "__main__":
    main()
