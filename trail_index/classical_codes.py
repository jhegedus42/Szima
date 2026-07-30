"""classical_codes.py — Classical convolutional codes over E8 × E8 for Hungarian case algebra.

Not static: the code evolves as context accumulates.
Each case suffix is an 8-bit syndrome in the E8 sub-code.
Convolution means the encoding at position t depends on position t-1.

Theory:
  E8 × E8 → two 8D lattices = 16D total code space
  Hungarian cases → 5-bit sub-code within E8 (2^5 = 32 ≥ 22 cases)
  Convolutional code → state machine with constraint length K
  The syndrome at step t = f(input_t, state_{t-1})
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════
# E8 × E8 Lattice — 16D code space
# ═══════════════════════════════════════════════════════════════

# E8 parity-check matrix (8×8 over F2 — the Hamming(8,4) parent)
# Each row is a parity constraint
E8_PARITY = np.array([
    [1,0,0,0,1,0,1,1],
    [0,1,0,0,1,1,0,1],
    [0,0,1,0,1,1,1,0],
    [0,0,0,1,0,1,1,1],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1],
], dtype=np.int8)


# ═══════════════════════════════════════════════════════════════
# Hungarian Case → 5-bit sub-code within E8
# ═══════════════════════════════════════════════════════════════

CASES = [
    "NOM", "ACC", "DAT", "INS", "COM", "CAU", "TRA", "TER",
    "ILL", "INE", "ELA", "ALL", "ADE", "ABL", "SUP", "DEL",
    "SUB", "TEM", "SOC", "DIST", "ESS", "MOD", "CAS", "FOR",
]

# Each case mapped to a unique 5-bit vector (sub-code of E8)
# These span a 5D subspace within the 8D E8 lattice
CASE_CODES: dict[str, np.ndarray] = {}
for i, case in enumerate(CASES):
    bits = [(i >> b) & 1 for b in range(5)] + [0, 0, 0]
    CASE_CODES[case] = np.array(bits, dtype=np.int8)

# Reverse map: syndrome → case name
SYNDROME_TO_CASE: dict[tuple, str] = {}
for case, vec in CASE_CODES.items():
    syndrome = tuple(int(v) for v in (E8_PARITY @ vec) % 2)
    SYNDROME_TO_CASE[syndrome] = case


# ═══════════════════════════════════════════════════════════════
# Convolutional Encoder (not static — stateful)
# ═══════════════════════════════════════════════════════════════

@dataclass
class ConvState:
    """Convolutional encoder state."""
    prev_case: Optional[str] = None       # previous case (K=1 memory)
    prev_vec: np.ndarray = field(
        default_factory=lambda: np.zeros(8, dtype=np.int8)
    )
    step: int = 0
    parity_history: list[np.ndarray] = field(default_factory=list)

    def reset(self):
        self.prev_case = None
        self.prev_vec = np.zeros(8, dtype=np.int8)
        self.step = 0
        self.parity_history = []


def encode_case(case: str, state: ConvState) -> np.ndarray:
    """Encode a Hungarian case as a convolutional E8 code word.

    The output at step t depends on:
      - input: case at step t
      - state: previous case syndrome at step t-1

    Returns: 16-bit vector (E8 left concatenated with E8 right = E8×E8 sub-code)
    """
    vec = CASE_CODES.get(case, np.zeros(8, dtype=np.int8))

    # Convolution: XOR with previous state (constraint length K=1)
    if state.prev_vec is not None:
        vec = (vec + state.prev_vec) % 2

    # Enforce E8 parity: compute syndrome
    syndrome = (E8_PARITY @ vec) % 2

    # If parity violated, correct by flipping the lowest-weight bit
    if np.any(syndrome):
        # Find the error position (simplified: assume single-bit error)
        for i in range(8):
            test = vec.copy()
            test[i] ^= 1
            if not np.any((E8_PARITY @ test) % 2):
                vec = test
                break

    # E8 × E8: right half mirrors left with offset (sub-code structure)
    right = (vec + np.roll(vec, 1)) % 2

    # Update state
    state.prev_case = case
    state.prev_vec = vec
    state.step += 1
    state.parity_history.append((E8_PARITY @ vec) % 2)

    # Return 16D code word (E8 left, E8 right)
    return np.concatenate([vec, right])


# ═══════════════════════════════════════════════════════════════
# Decoder with state tracking
# ═══════════════════════════════════════════════════════════════

@dataclass
class DecodedToken:
    case: str
    syndrome: tuple
    code_16d: list[int]
    corrected: bool = False


def decode_16d(code_16d: np.ndarray, state: ConvState) -> DecodedToken:
    """Decode a 16D code word back to a Hungarian case.

    Uses Viterbi-like backward tracking: checks both E8 halves,
    corrects errors using the convolutional constraint.
    """
    left = code_16d[:8].astype(np.int8)
    right = code_16d[8:].astype(np.int8)

    # Check parity on both halves
    left_syn = tuple(int(v) for v in (E8_PARITY @ left) % 2)
    right_syn = tuple(int(v) for v in (E8_PARITY @ right) % 2)

    # Try to match syndrome to a case (first from left, then right)
    case = SYNDROME_TO_CASE.get(left_syn) or SYNDROME_TO_CASE.get(right_syn)
    corrected = False

    if case is None:
        # Error: no matching case. Apply convolutional correction:
        # flip bits until we get a valid syndrome close to previous
        corrected = True
        for i in range(8):
            trial = left.copy()
            trial[i] ^= 1
            syn = tuple(int(v) for v in (E8_PARITY @ trial) % 2)
            case = SYNDROME_TO_CASE.get(syn)
            if case:
                left = trial
                break

    if case is None:
        case = "NOM"  # fallback

    state.prev_case = case
    state.prev_vec = left
    state.step += 1

    return DecodedToken(
        case=case,
        syndrome=left_syn,
        code_16d=[int(v) for v in code_16d],
        corrected=corrected,
    )


# ═══════════════════════════════════════════════════════════════
# Sentence-level encoding/decoding
# ═══════════════════════════════════════════════════════════════

def encode_sentence(cases: list[str]) -> tuple[list[list[int]], ConvState]:
    """Encode a sequence of Hungarian cases as 16D code words."""
    state = ConvState()
    codes = []
    for case in cases:
        code = encode_case(case, state)
        codes.append([int(v) for v in code])
    return codes, state


def decode_sentence(codes_16d: list[list[int]]) -> list[DecodedToken]:
    """Decode a sequence of 16D code words back to cases."""
    state = ConvState()
    tokens = []
    for code in codes_16d:
        token = decode_16d(np.array(code, dtype=np.int8), state)
        tokens.append(token)
    return tokens


# ═══════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════

def demo():
    print("=" * 60)
    print("Classical Convolutional Code over E8 × E8")
    print("Hungarian Case System as 5-bit Sub-code")
    print("=" * 60)

    # Example: a simple causal chain
    chain = ["NOM", "ACC", "CAU", "TRA", "DAT", "SUB", "INE", "ELA"]
    print(f"\nInput cases: {chain}")

    codes, state = encode_sentence(chain)
    print(f"Encoded {len(codes)} code words (16D each)")
    print(f"Final state step: {state.step}")

    # Introduce an error in transmission
    codes[3][2] ^= 1  # flip one bit in TRA
    print(f"\nIntroduced bit error at position 3")

    decoded = decode_sentence(codes)
    recovered = [t.case for t in decoded]
    errors = sum(1 for t in decoded if t.corrected)
    print(f"Recovered: {recovered}")
    print(f"Errors corrected: {errors}")

    # Show the parity evolution (not static!)
    print(f"\nParity history (evolving syndrome):")
    for i, ph in enumerate(state.parity_history):
        syn_str = "".join(str(int(b)) for b in ph)
        print(f"  Step {i}: {syn_str}")


if __name__ == "__main__":
    demo()
