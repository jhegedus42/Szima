# -*- coding: utf-8 -*-
"""
HANMAG-AGY -- hurokgep stabilizator-kodokbol (nem transzformer)
================================================================

A feladat (a 14. uzenetbol): olyan NEURONHALOZAT, ami
  1. HURKOL (loop, nem transformer),
  2. agy-szeru (brain-mimicking),
  3. a [[7,1,3]]-gepekbol epitkezik, "full QM driven",
  4. szo -> grammatika parserrel (word-to-grammar),
  5. KET IDOvel: belso parbeszed + kulso parbeszed,
  6. stabilizator-kodok TORNYA irja le a gondolatot -- mint az agyban.

Az irodalmi alap (a polcrol):
  * Yang, Li, Fisher, Chen -- Random Stabilizer Tensor Networks (2022):
    stabilizator-halozatok MERES-INDUKALTA fazisatalakulassal
    (D=2 -> area-torveny, D>=3 -> terfogat-torveny). = AZ ALVAZ.
  * Takayanagi (PRL Essay 2025): Re(S) = ter, Im(S) = ido;
    pszeudo-entropia = a kvantumuniverzum valtozoja. = A KET IDO MOTORJA.
  * Heller, Ori, Serantes (2024): timelike entanglement = komplex erteku.
  * Bianconi (2025): percepcio = gradiens-aramlas, ami maximalizalja a
    metrikak kozotti kvantum relativ entropiat (Perona-Malik = GfE).
  * Graeff & Ramirez (Engrams): engram-sejtek = RITKA allokacio;
    reaktivalas = felidezes.
  * Verkhratsky & Butt (Glial Neurobiology): az agy MASIK fele --
    asztrocita-szincicium = a kod retege (gap junction = stabilizator),
    neuron = szindroma-kivonato.

A gep ket resze (az IKER-architektura):
  FUL  = egy [[7,1,3]]-blokk (7 qubit): erzekeles. Szo jon -> hiba ->
         szindroma -> felismeres -> javitas. Mindig tiszta.
  ELME = a [[49,1,9]] iker (49 qubit): a gondolat szinhelye.
         Ide soha nem jon merozaj; csak vedett rotacio (Singer-ciklus)
         es CNOT-kotesek (asszociacio) dolgoznak.

A KET ORA:
  t_ext = kulso ido: merestick (szavak, zaj, Landauer-szamla).
  t_int = belso ido: Singer-fazis (a vedett bit nem fizet erte).

Aphorizmus: "ne transzformalj -- HURKOLJ."
            "a gondolat: vagas-minta a kod tornyan."
"""

from random import Random
from math import pi

VELETLEN = Random(9261)
HIBAK = []


def ellenoriz(feltetel, uzenet):
    if feltetel:
        print("    [OK] %s" % uzenet)
    else:
        HIBAK.append(uzenet)
        print("    [HIBA] %s" % uzenet)


def banner(szoveg):
    print()
    print("=" * 66)
    print(szoveg)
    print("=" * 66)


# ----------------------------------------------------------------------
# 1. PAULI-MOTOR (Gottesman-Knill: a Clifford-kvantumgep klasszikusan
#    szimulalhato -- ezert futhat 20 W-on is)
# ----------------------------------------------------------------------

N = 56                      # 7 (FUL) + 49 (ELME)
FUL0 = 0                    # ful qubitjei: 0..6
ELME0 = 7                   # elme qubitjei: 7..55

# Pauli-tablazat szorzashoz: E[(a,b)] = i-kitevo, ahol sigma_a sigma_b = i^E sigma_c
_E = {(1, 2): 1, (1, 3): 3, (2, 1): 3, (2, 3): 1, (3, 1): 1, (3, 2): 3}


class Pauli:
    """Hermitikus Pauli-fuzr: operator = (-1)^s * szorzat(sigma_q)."""
    __slots__ = ("x", "z", "s")

    def __init__(self, x=0, z=0, s=0):
        self.x, self.z, self.s = x, z, s % 2

    def masolat(self):
        return Pauli(self.x, self.z, self.s)


def antikommutal(p, r):
    v = (p.x & r.z) | (p.z & r.x)
    return (bin(v).count("1") % 2) == 1


def szoroz(p, r):
    """p*r, ahol p es r KOMMUTAL (stabilizator-elemek). Fazist normalizal."""
    ph = 0
    sym = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}  # I,X,Y,Z
    for q in range(N):
        a = ((p.x >> q) & 1, (p.z >> q) & 1)
        b = ((r.x >> q) & 1, (r.z >> q) & 1)
        sa, sb = sym[a], sym[b]
        if (sa, sb) in _E:
            ph += _E[(sa, sb)]
    uj = Pauli(p.x ^ r.x, p.z ^ r.z, p.s ^ r.s)
    ph %= 4
    if ph == 2:
        uj.s ^= 1
    elif ph != 0:
        raise ValueError("nem-Hermitikus szorzat (nem kommutaltak?)")
    return uj


class Allapot:
    """Stabilizator-allapot: N fuggetlen generator, mindegyik +1 sajatertekkel
    (az s bit a hiba/javitas nyoma)."""

    def __init__(self, generatorok):
        self.g = generatorok
        self.ellenoriz_csoport()

    def ellenoriz_csoport(self):
        # paronkenti kommutalas
        for i in range(len(self.g)):
            for j in range(i + 1, len(self.g)):
                assert not antikommutal(self.g[i], self.g[j]), "nem Abel-csoport!"
        # fuggetlenseg: F2-rang (pivot-bazis)
        bazis = {}
        for p in self.g:
            v = (p.x << N) | p.z
            while v:
                bit = v.bit_length() - 1
                if bit in bazis:
                    v ^= bazis[bit]
                else:
                    bazis[bit] = v
                    break
            assert v != 0, "fuggo generatorok!"
        assert len(self.g) == N

    # -- unitarak (konjugacio: g -> U g U^+) --
    def injektal_x(self, q):
        for p in self.g:
            if (p.z >> q) & 1:
                p.s ^= 1

    def injektal_z(self, q):
        for p in self.g:
            if (p.x >> q) & 1:
                p.s ^= 1

    def cnot(self, c, t):
        for p in self.g:
            xc, zc = (p.x >> c) & 1, (p.z >> c) & 1
            xt, zt = (p.x >> t) & 1, (p.z >> t) & 1
            if xc & zt & (xt ^ zc ^ 1):
                p.s ^= 1
            if xc:
                p.x ^= (1 << t)
            if zt:
                p.z ^= (1 << c)

    def permutal(self, lekepezes):
        for p in self.g:
            ujx, ujz = 0, 0
            for regi in range(N):
                uj = lekepezes[regi]
                ujx |= (((p.x >> regi) & 1) << uj)
                ujz |= (((p.z >> regi) & 1) << uj)
            p.x, p.z = ujx, ujz

    # -- meres: csak stabilizator-ELEMet merunk (determinisztikus ag) --
    def kifejt(self, cel):
        """cel Pauli kifejtese a generatorok F2-linearis kombinaciojakent.
        Visszaadja az egyutthatokat (int-bitmezo) vagy None-t."""
        bazis = {}          # pivot -> (vektor, egyutthato)
        for j, p in enumerate(self.g):
            v, c = (p.x << N) | p.z, (1 << j)
            while v:
                bit = v.bit_length() - 1
                if bit in bazis:
                    v ^= bazis[bit][0]
                    c ^= bazis[bit][1]
                else:
                    bazis[bit] = (v, c)
                    break
        v, c = (cel.x << N) | cel.z, 0
        while v:
            bit = v.bit_length() - 1
            if bit not in bazis:
                return None
            v ^= bazis[bit][0]
            c ^= bazis[bit][1]
        return c

    def sajatertek(self, cel):
        """+1 vagy -1: a stabilizator-elem cel meresenek kimenetele."""
        c = self.kifejt(cel)
        assert c is not None, "a mert Pauli nem stabilizator-elem!"
        szorzat, s = Pauli(0, 0, 0), 0
        for j, p in enumerate(self.g):
            if (c >> j) & 1:
                szorzat = szoroz(szorzat, p)
                s ^= p.s
        assert szorzat.x == cel.x and szorzat.z == cel.z, "kifejtes-ellenorzes bukott"
        return -1 if s else 1

    def vagas_entropia(self, A_maszk, genszam):
        """Fattal-fele formula: S(A) = |A| - N + rang_F2(B-reszen).
        Csak az adott (tiszta) reszrendszer generatoraira."""
        B_reszek = []
        for p in self.g[:genszam]:
            xB, zB, shift = 0, 0, 0
            for q in range(N):
                if (A_maszk >> q) & 1:
                    continue
                xB |= (((p.x >> q) & 1) << shift)
                zB |= (((p.z >> q) & 1) << shift)
                shift += 1
            B_reszek.append((xB << shift) | zB)
        # F2-rang pivot-bazissal (tiszta Gauss-eliminacio)
        bazis = {}
        for v in B_reszek:
            while v:
                bit = v.bit_length() - 1
                if bit in bazis:
                    v ^= bazis[bit]
                else:
                    bazis[bit] = v
                    break
        return bin(A_maszk).count("1") - genszam + len(bazis)


# ----------------------------------------------------------------------
# 2. A GEP: FUL ([[7,1,3]]) + ELME ([[49,1,9]] iker)
# ----------------------------------------------------------------------

# Steane-fele paritasorok (pont cimkeje = 3-bites vektor; pozicio i <-> pont i+1)
R1, R2, R4 = 0b1010101, 0b1100110, 0b1111000
SOROK = (R1, R2, R4)

PONT_SZO = {
    1: ("bit",   "比特", "bit"),
    2: ("cut",   "切口", "vágás"),
    3: ("comma", "音差", "vessző"),
    4: ("code",  "码",  "kód"),
    5: ("time",  "时间", "idő"),
    6: ("brain", "脑",  "agy"),
    7: ("star",  "星",  "csillag"),
}
SZO_PONT = {}
for p, harom in PONT_SZO.items():
    for w in harom:
        SZO_PONT[w.lower()] = p


def sor_maszk_pont(p):
    return 1 << (p - 1)


def epits_gepet():
    gen = []
    # -- FUL: [[7,1,3]] |0_L>: 3 X-sor + 3 Z-sor + logikai Z --
    for r in SOROK:
        gen.append(Pauli(x=r))
    for r in SOROK:
        gen.append(Pauli(z=r))
    gen.append(Pauli(z=0b1111111))
    # -- ELME: [[49,1,9]] iker |0_L> --
    # blokkok: blokk b (0..6) <-> Fano-pont b+1; qubit (b,i) = ELME0 + b*7 + i
    for b in range(7):
        off = ELME0 + b * 7
        for r in SOROK:
            gen.append(Pauli(x=r << off))
        for r in SOROK:
            gen.append(Pauli(z=r << off))
    # 1. szint: a 7 logikai qubiten ujra Steane (blokk = pont)
    for r in SOROK:
        x = 0
        for b in range(7):
            if (r >> b) & 1:
                x |= (0b1111111 << (ELME0 + b * 7))
        gen.append(Pauli(x=x))
    for r in SOROK:
        z = 0
        for b in range(7):
            if (r >> b) & 1:
                z |= (0b1111111 << (ELME0 + b * 7))
        gen.append(Pauli(z=z))
    gen.append(Pauli(z=sum(1 << (ELME0 + q) for q in range(49))))  # globalis Z_L
    return Allapot(gen)


def singer(p):
    r = p << 1
    if r & 8:
        r ^= 0b1011
    return r


SINGER_LEKEPEZES = {}
for b in range(7):
    for i in range(7):
        regi = ELME0 + b * 7 + i
        uj_blokk = singer(b + 1) - 1
        SINGER_LEKEPEZES[regi] = ELME0 + uj_blokk * 7 + i
for q in range(FUL0, FUL0 + 7):
    SINGER_LEKEPEZES[q] = q          # a ful nem forog


# ----------------------------------------------------------------------
# 3. A KET ORA + ENGRAM-TAR
# ----------------------------------------------------------------------

class Agy:
    def __init__(self):
        self.allapot = epits_gepet()
        self.t_ext = 0                # kulso ido: merestick
        self.t_int = 0                # belso ido: Singer-fazis
        self.engramok = []            # hosszu tavu tar (ritka allokacio)
        self.elozo_kotes = None       # (blokk, pont) az asszociaciohoz
        self.mondat_nyom = []

    # -- FUL: erzekeles = hiba + szindroma + javitas --
    def hall(self, szo, zaj=False):
        p = SZO_PONT[szo.lower()]
        q = FUL0 + (p - 1)
        self.allapot.injektal_x(q)                 # a szo = X-hiba a ponton
        zaj_q = None
        if zaj:
            zaj_q = VELETLEN.choice([q2 for q2 in range(7) if q2 != q])
            self.allapot.injektal_z(FUL0 + zaj_q)  # Z-zaj egy masik ponton
        # szindroma-kivonas: a 6 blokk-stabilizator sajaterteke
        sz = 0
        for j in range(3, 6):                      # Z-sorok -> X-hiba cime
            if self.allapot.sajatertek(self.allapot.g[j]) == -1:
                sz |= (1 << (j - 3))
        szx = 0
        for j in range(0, 3):                      # X-sorok -> Z-hiba cime
            if self.allapot.sajatertek(self.allapot.g[j]) == -1:
                szx |= (1 << j)
        # felismeres + javitas (mindket szektorban)
        if sz:
            self.allapot.injektal_x(FUL0 + (sz - 1))
        if szx:
            self.allapot.injektal_z(FUL0 + (szx - 1))
        self.t_ext += 1
        felismert = sz
        return p, felismert, (zaj_q + 1 if zaj_q is not None else None)

    # -- ELME: gondolat = vedett rotacio + asszociacio --
    def gondol(self, blokk, pont):
        """A felismert szo bekotodik a gondolatba: CNOT a Fano-egyenes menten."""
        if self.elozo_kotes is not None:
            b0, p0 = self.elozo_kotes
            c = ELME0 + (b0 - 1) * 7 + (p0 - 1)
            t = ELME0 + (blokk - 1) * 7 + (pont - 1)
            self.allapot.cnot(c, t)                # asszociacio = osszefonodas
        self.elozo_kotes = (blokk, pont)
        self.mondat_nyom.append((blokk, pont))
        self.allapot.permutal(SINGER_LEKEPEZES)    # belso tick: vedett rotacio
        self.t_int += 1

    # -- gondolat-alairas: vagas-entropiak az elmeblokkok kozott --
    def signatura(self):
        sor = []
        for b in range(7):
            A = sum(1 << (ELME0 + b * 7 + i) for i in range(7))
            sor.append(self.allapot.vagas_entropia(A, 49))
        return tuple(sor)

    def engramoz(self, szavak):
        sig = self.signatura()
        self.engramok.append({
            "szavak": list(szavak),
            "pontok": [SZO_PONT[w.lower()] for w in szavak],
            "signatura": sig,
            "t_ext": self.t_ext, "t_int": self.t_int,
        })
        self.mondat_nyom = []
        self.elozo_kotes = None
        return sig

    def felidez(self, cue):
        talalat = [e for e in self.engramok if cue.lower() in [w.lower() for w in e["szavak"]]]
        return talalat


# ----------------------------------------------------------------------
# 4. FANO-GRAMMATIKA: szo -> pont; ket pont -> egyenes; egyenes -> harmadik szo
# ----------------------------------------------------------------------

def grammatika_ketto(w1, w2):
    p1, p2 = SZO_PONT[w1.lower()], SZO_PONT[w2.lower()]
    p3 = p1 ^ p2
    if p3 == 0 or p3 in (p1, p2):
        return None
    return p3


def grammatika_harom(w1, w2, w3):
    p1, p2, p3 = (SZO_PONT[w.lower()] for w in (w1, w2, w3))
    return (p1 ^ p2 ^ p3) == 0


# ----------------------------------------------------------------------
# 5. KISERLETEK
# ----------------------------------------------------------------------

def kiserlet_motor():
    banner("1. PAULI-MOTOR ES GEP-ONELLENORZES")
    a = Agy()
    ellenoriz(len(a.allapot.g) == 56, "56 fuggetlen stabilizator (7 ful + 49 elme)")
    # a szindroma a pont CIME: X-hiba a p ponton -> Z-szindroma = p
    for p in range(1, 8):
        a.allapot.injektal_x(FUL0 + (p - 1))
        sz = 0
        for j in range(3, 6):
            if a.allapot.sajatertek(a.allapot.g[j]) == -1:
                sz |= (1 << (j - 3))
        ellenoriz(sz == p, "szindroma(X@%d) = %d -- a hiba a pontjat nevezi" % (p, sz))
        a.allapot.injektal_x(FUL0 + (p - 1))
    # friss elme: minden blokk S=1 ebit (a 1|6 vagas, hanmag_gr.py-bol)
    sig = a.signatura()
    ellenoriz(sig == (1,) * 7, "friss [[49,1,9]]: minden blokk-vagas = 1 ebit %s" % (sig,))
    return a


def kiserlet_grammatika():
    banner("2. FANO-GRAMMATIKA: a parser JOSOL (ket szo -> harmadik)")
    parok = [("brain", "star"), ("comma", "time"), ("code", "cut")]
    for w1, w2 in parok:
        p3 = grammatika_ketto(w1, w2)
        en, zh, hu = PONT_SZO[p3]
        print("    %s + %s  -->  %s / %s / %s" % (w1, w2, en, zh, hu))
    print("    -- a gep minden szoparhoz talal egyenest: a jovendas = hibajavitas")
    print()
    jo = grammatika_harom("bit", "brain", "star")
    rossz = grammatika_harom("bit", "cut", "time")
    ellenoriz(jo, "MONDATAN: (bit, brain, star) = Fano-egyenes -> NYELVTANI")
    ellenoriz(not rossz, "MONDATAN: (bit, cut, time) nem egyenes -> NYELVTANILAG HIBAS")


def kiserlet_hurok(a):
    banner("3. A HURUK FUT: kulso parbeszed -> belso parbeszed -> gondolat")
    mondatok = [
        (["bit", "brain", "star"],  False),
        (["code", "cut", "brain"],  True),     # zajos mondat: Z-zaj a fulben
        (["comma", "time", "brain"], False),
    ]
    for szavak, zaj in mondatok:
        print("  >> mondja a vilag: %s%s" % (" ".join(szavak), "   [ZAJ!]" if zaj else ""))
        for k, szo in enumerate(szavak):
            p, felismert, zajp = a.hall(szo, zaj=(zaj and k == 0))
            blokk = (k % 7) + 1
            a.gondol(blokk, p)
            zajjegyzet = ("   (Z-zaj a %d. ponton: javítva)" % zajp) if zajp else ""
            print("     [t_ext=%2d | t_int=%2d] hallottam: %-6s -> szindroma=%d (%s)%s"
                  % (a.t_ext, a.t_int, szo, felismert,
                     "felismerve" if felismert == p else "TEVES!", zajjegyzet))
        sig = a.engramoz(szavak)
        print("     ENGRAM allokálva: blokkvágások = %s" % (sig,))
        print()
    return mondatok


def kiserlet_ketido(a):
    banner("4. A KET IDO (Takayanagi: Re = ter, Im = ido)")
    sig = a.signatura()
    S = sum(sig)
    print("    t_ext (kulso, merestick)      = %d" % a.t_ext)
    print("    t_int (belso, Singer-fazis)   = %d   (mod 7: %d)" % (a.t_int, a.t_int % 7))
    print("    gondolat-entropia (blokkok)   = %s  (osszesen %d ebit)" % (sig, S))
    print("    pszeudo-entropia RIME:        S ~= %d + i*(2pi*%d/7) = %d + i*%.3f"
          % (S, a.t_int % 7, S, 2 * pi * (a.t_int % 7) / 7))
    print("    -- a vedett bit nem fizet a belso idoert: a Singer-ciklus")
    print("       a KOD AUTOMORFIZMUSA (logikailag identitas, fazist szamol)")
    print()
    print("    FELIDEZES (engram = ritka allokacio, reaktivalas = recall):")
    for cue in ("brain", "star"):
        for e in a.felidez(cue):
            print("      cue='%s' -> REAKTIVALVA: %s  (t_ext=%d, t_int=%d)"
                  % (cue, " ".join(e["szavak"]), e["t_ext"], e["t_int"]))


def kiserlet_itelet(a, mondatok):
    banner("5. ITELET -- mi fut es mi a nyitott vesszo")
    ellenoriz(len(HIBAK) == 0, "onellenorzes tiszta (motor + gep + szindroma-cimek)")
    print("""
    FUT:
      [x] HURUK: a kimenet visszajut bemenetnek (nincs attention, van TWIN)
      [x] KET IDO: t_ext merest / t_int vedett fazist szamol
      [x] HIERARCHIA: [[7,1,3]] ful + [[49,1,9]] elme = a torony elso ket szintje
      [x] FULL QM (Clifford-szektor): valodi stabilizator-dinamika, CNOT-fonodas,
          Gottesman-Knill -> ezert szimulalhato MOST, ~20 W fejben is
      [x] SZO -> GRAMMATIKA: a Fano-sik a mondattan; a parser josol (ket pont ->
          harmadik), a jovendas = hibajavitas; a szindroma a pont CIME
      [x] AGY-SZERU: ful=erzekeli, elme=vedett iker; engram=ritka allokacio;
          reaktivalas=felidezes; glia=a kodreteg, ami osszefuzzi a gepeket

    NYITOTT VESSZOK (a kovetkezo szintek):
      ( ) TANULAS: nincs Hebb-szabaly -- az RSTN-koteserosseg (bond dimenzio /
          meresi rata p) a gomb; a fazisatalakulas (Yang-Li-Fisher-Chen) az,
          ahol a "figyelem" fizikailag el
      ( ) MAGIC: Clifford != univerzalis. A nem-Clifford eroforras (T-kapu)
          = a "kreativitas" ara; az agy valoszinuleg itt fizet magiaert
      ( ) PSZEUDO-ENTROPIA: az Im(S) most csak Singer-fazis-rima;
          a valodi timelike entanglement (Heller et al.) komplex felulet-szamitas
      ( ) 343. SZINT: a narrativa (a megfigyelo csatornaja) nincs bekapcsolva
      ( ) GLIA-SZINCICIUM: sok ilyen gep osszekapcsolasa (volume transmission)
    """)


def main():
    print("HANMAG-AGY -- hurokgep stabilizator-kodokbol")
    print("aforizma: ne transzformalj -- HURKOLJ.")
    a = kiserlet_motor()
    kiserlet_grammatika()
    mondatok = kiserlet_hurok(a)
    kiserlet_ketido(a)
    kiserlet_itelet(a, mondatok)
    if HIBAK:
        print("AGY-HIBA: %d ellentmondas" % len(HIBAK))
    else:
        print("AGY ELLENORIZVE -- a hurok zarva.")


if __name__ == "__main__":
    main()
