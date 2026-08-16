# -*- coding: utf-8 -*-
"""
HANMAG-TORONY -- a jelentes tornya: haromszintes hurok-agy
============================================================

A 15. uzenetbol: "we need to have some hierarchy of these, no?
coz we need to be able to represent all sorts of meaning."

Igen. A torony (ez a gep):
  0. szint: FUL       [[7,1,3]]    -- betuk/szavak (erzekeles)
  1. szint: 7 x ELME  [[49,1,9]]   -- gondolatok (mondatok)
  2. szint: NARRATIVA [[343,1,27]] -- tortenet (7 gondolat osszekotve)

A hierarchia harom ajandeka:
  1. KAPACITAS: a stabilizator-allapotter merete:
     log2(#allapot) = n + Szumma_k log2(2^k + 1)
     ful ~= 36 bit, elme ~= 1275 bit (~egy bekezdes),
     narrativa ~= 59340 bit (~egy novella). [Clifford-szektor]
  2. BEAGYAZOTT ORAK: minden szinten kulon t_ext / t_int --
     az agy ritmushierarchiaja (gamma C theta C alfa).
  3. KOMPOZICIONALITAS: jelentes = rekurziv kotes (Tomasello:
     a nyelvtan is igy epul -- konstrukciok tornya).

Aphorizma: "a jelentes a vagasokban lakik; a logikai bit az 'en'."
           "a torony nem magasabb -- MELYEBB."
"""

from random import Random
from math import pi, log2

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
# 1. PAULI-MOTOR (N = 350: 7 ful + 343 narrativa)
# ----------------------------------------------------------------------

N = 350
FUL0 = 0                     # ful: 0..6
TOR0 = 7                     # narrativa: 7..349
# qubit-index: (elme m, blokk b, pozicio i) -> TOR0 + m*49 + b*7 + i

_E = {(1, 2): 1, (1, 3): 3, (2, 1): 3, (2, 3): 1, (3, 1): 1, (3, 2): 3}
_SYM = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}


class Pauli:
    __slots__ = ("x", "z", "s")

    def __init__(self, x=0, z=0, s=0):
        self.x, self.z, self.s = x, z, s % 2


def antikommutal(p, r):
    return (bin((p.x & r.z) | (p.z & r.x)).count("1") % 2) == 1


def szoroz(p, r):
    """p*r, ahol p es r KOMMUTAL. Fazist (-1)^s-be normalizal."""
    ph = 0
    for q in range(N):
        a = ((p.x >> q) & 1, (p.z >> q) & 1)
        b = ((r.x >> q) & 1, (r.z >> q) & 1)
        sa, sb = _SYM[a], _SYM[b]
        if (sa, sb) in _E:
            ph += _E[(sa, sb)]
    uj = Pauli(p.x ^ r.x, p.z ^ r.z, p.s ^ r.s)
    ph %= 4
    if ph == 2:
        uj.s ^= 1
    elif ph != 0:
        raise ValueError("nem-Hermitikus szorzat")
    return uj


def rang_f2(vektorok):
    bazis = {}
    for v in vektorok:
        while v:
            bit = v.bit_length() - 1
            if bit in bazis:
                v ^= bazis[bit]
            else:
                bazis[bit] = v
                break
    return len(bazis)


class Allapot:
    def __init__(self, generatorok):
        self.g = generatorok
        self.ellenoriz_csoport()

    def ellenoriz_csoport(self):
        for i in range(len(self.g)):
            for j in range(i + 1, len(self.g)):
                assert not antikommutal(self.g[i], self.g[j]), "nem Abel-csoport!"
        vekt = [((p.x << N) | p.z) for p in self.g]
        assert rang_f2(vekt) == len(self.g) == N, "fuggo generatorok!"

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

    def permutal_map(self, mozgasok):
        # teljes permutacio: ami nincs mozgatva, az marad (identity a tobbi qubiten)
        teljes = list(range(N))
        for regi, uj in mozgasok:
            teljes[regi] = uj
        for p in self.g:
            ujx, ujz = 0, 0
            for regi in range(N):
                uj = teljes[regi]
                ujx |= (((p.x >> regi) & 1) << uj)
                ujz |= (((p.z >> regi) & 1) << uj)
            p.x, p.z = ujx, ujz

    def sajatertek(self, cel):
        """cel stabilizator-elem meresenek determinisztikus kimenetele.
        Csak a cel TAMOGATASAN BELULI generatorok kellenek (itt biztonsagos:
        a ful- es torony-generatorok tamogatasa diszjunkt)."""
        tam = cel.x | cel.z
        jeloltek = [p for p in self.g if ((p.x | p.z) & ~tam) == 0]
        bazis = {}
        for p in jeloltek:
            v = (p.x << N) | p.z
            lanc = [p]
            while v:
                bit = v.bit_length() - 1
                if bit in bazis:
                    v ^= bazis[bit][0]
                    lanc = lanc + bazis[bit][1]
                else:
                    bazis[bit] = (v, lanc)
                    break
        v = (cel.x << N) | cel.z
        lanc = []
        while v:
            bit = v.bit_length() - 1
            if bit not in bazis:
                raise ValueError("a mert Pauli nem stabilizator-elem!")
            v ^= bazis[bit][0]
            lanc = lanc + bazis[bit][1]
        szorzat, s = Pauli(0, 0, 0), 0
        for p in lanc:
            szorzat = szoroz(szorzat, p)
            s ^= p.s
        assert szorzat.x == cel.x and szorzat.z == cel.z
        return -1 if s else 1

    def vagas_entropia(self, A_maszk, genek):
        """S(A) = |A| - N + rang_F2(B-resz)  (Fattal; a genek tiszta allapotot
        stabilizalnak a vizsgalt N qubiten)."""
        n_sub = len(genek)
        B_reszek = []
        for p in genek:
            xB, zB, shift = 0, 0, 0
            for q in range(N):
                if (A_maszk >> q) & 1:
                    continue
                if (TOR0 <= q):
                    xB |= (((p.x >> q) & 1) << shift)
                    zB |= (((p.z >> q) & 1) << shift)
                    shift += 1
            B_reszek.append((xB << shift) | zB)
        return bin(A_maszk).count("1") - n_sub + rang_f2(B_reszek)


# ----------------------------------------------------------------------
# 2. A TORONY FELEPITESE
# ----------------------------------------------------------------------

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


def qbit(m, b, i):
    return TOR0 + m * 49 + b * 7 + i


def epits_tornyot():
    gen = []
    # -- FUL --
    for r in SOROK:
        gen.append(Pauli(x=r))
    for r in SOROK:
        gen.append(Pauli(z=r))
    gen.append(Pauli(z=0b1111111))
    # -- 7 ELME: mindegyik [[49,1,9]] --
    for m in range(7):
        for b in range(7):
            off = qbit(m, b, 0)
            for r in SOROK:
                gen.append(Pauli(x=r << off))
            for r in SOROK:
                gen.append(Pauli(z=r << off))
        for r in SOROK:                      # elme szint-1 stabilizatorai
            x = 0
            for b in range(7):
                if (r >> b) & 1:
                    x |= (0b1111111 << qbit(m, b, 0))
            gen.append(Pauli(x=x))
        for r in SOROK:
            z = 0
            for b in range(7):
                if (r >> b) & 1:
                    z |= (0b1111111 << qbit(m, b, 0))
            gen.append(Pauli(z=z))
    # FIGYELEM: az elmek logikai Z-je NEM generator -- az a szint-2 kod
    # osszefonodasa (igy lesz S(elme) = 1 ebit a tobbi elmevel).
    # -- NARRATIVA szint-2: a 7 elme logikai qubiten ujra Steane --
    for r in SOROK:
        x = 0
        for m in range(7):
            if (r >> m) & 1:
                for b in range(7):
                    x |= (0b1111111 << qbit(m, b, 0))
        gen.append(Pauli(x=x))
    for r in SOROK:
        z = 0
        for m in range(7):
            if (r >> m) & 1:
                for b in range(7):
                    z |= (0b1111111 << qbit(m, b, 0))
        gen.append(Pauli(z=z))
    z = 0                                      # globalis logikai Z (az "en")
    for m in range(7):
        for b in range(7):
            z |= (0b1111111 << qbit(m, b, 0))
    gen.append(Pauli(z=z))
    return Allapot(gen)


def singer(p):
    r = p << 1
    if r & 8:
        r ^= 0b1011
    return r


def blokk_rotacio(m):
    """Singer-ciklus a blokkokon az m-edik elmen belul (szint-1 automorfizmus)."""
    lek = []
    for b in range(7):
        for i in range(7):
            lek.append((qbit(m, b, i), qbit(m, singer(b + 1) - 1, i)))
    return lek


def elme_rotacio():
    """Singer-ciklus a 7 elmen (szint-2 automorfizmus) -- a narrativa oraja."""
    lek = []
    for m in range(7):
        for b in range(7):
            for i in range(7):
                lek.append((qbit(m, b, i), qbit(singer(m + 1) - 1, b, i)))
    return lek


# ----------------------------------------------------------------------
# 3. A HAROMSZINTES AGY
# ----------------------------------------------------------------------

class ToronyAgy:
    def __init__(self):
        self.allapot = epits_tornyot()
        self.t_ext = 0          # kulso ido: mert szavak
        self.t_int1 = 0         # belso ido-1: blokk-rotaciok (a gondolat ritmusa)
        self.t_int2 = 0         # belso ido-2: elme-rotaciok (a tortenet ritmusa)
        self.engramok = []
        self.elozo_kotes = None
        self.aktualis_elme = 0

    def hall(self, szo, zaj=False):
        p = SZO_PONT[szo.lower()]
        q = FUL0 + (p - 1)
        self.allapot.injektal_x(q)
        zaj_p = None
        if zaj:
            zaj_p = VELETLEN.choice([x for x in range(1, 8) if x != p])
            self.allapot.injektal_z(FUL0 + (zaj_p - 1))
        sz = 0
        for j in range(3, 6):
            if self.allapot.sajatertek(self.allapot.g[j]) == -1:
                sz |= (1 << (j - 3))
        szx = 0
        for j in range(0, 3):
            if self.allapot.sajatertek(self.allapot.g[j]) == -1:
                szx |= (1 << j)
        if sz:
            self.allapot.injektal_x(FUL0 + (sz - 1))
        if szx:
            self.allapot.injektal_z(FUL0 + (szx - 1))
        self.t_ext += 1
        return p, sz, zaj_p

    def gondol(self, blokk, pont):
        m = self.aktualis_elme
        if self.elozo_kotes is not None:
            b0, p0 = self.elozo_kotes
            self.allapot.cnot(qbit(m, b0 - 1, p0 - 1), qbit(m, blokk - 1, pont - 1))
        self.elozo_kotes = (blokk, pont)
        self.allapot.permutal_map(blokk_rotacio(m))   # belso tick-1
        self.t_int1 += 1

    def elme_signatura(self, m):
        sor = []
        narrativa_genek = self.allapot.g[7:]
        for b in range(7):
            A = sum(1 << qbit(m, b, i) for i in range(7))
            sor.append(self.allapot.vagas_entropia(A, narrativa_genek))
        return tuple(sor)

    def narrativa_signatura(self):
        sor = []
        narrativa_genek = self.allapot.g[7:]
        for m in range(7):
            A = sum(1 << qbit(m, b, i) for b in range(7) for i in range(7))
            sor.append(self.allapot.vagas_entropia(A, narrativa_genek))
        return tuple(sor)

    def lezar_mondat(self, szavak, tema):
        """A mondat lezarul: a tema bekotodik a NARRATIVABA (szint-2 CNOT),
        az elme engramma allokalodik, es a torony orai tickelnek."""
        m = self.aktualis_elme
        if m > 0:
            elozo_tema = self.engramok[-1]["tema"]
            self.allapot.cnot(qbit(m - 1, 0, elozo_tema - 1), qbit(m, 0, tema - 1))
        sig = self.elme_signatura(m)
        self.engramok.append({
            "elme": m + 1, "szavak": list(szavak), "tema": tema,
            "signatura": sig, "t_ext": self.t_ext, "t_int1": self.t_int1,
        })
        self.elozo_kotes = None
        self.aktualis_elme += 1
        self.allapot.permutal_map(elme_rotacio())     # belso tick-2
        self.t_int2 += 1
        return sig

    def felidez(self, cue):
        return [e for e in self.engramok if cue.lower() in [w.lower() for w in e["szavak"]]]


# ----------------------------------------------------------------------
# 4. KISERLETEK
# ----------------------------------------------------------------------

def kiserlet_epites():
    banner("1. A TORONY ALL (onellenorzes)")
    a = ToronyAgy()
    ellenoriz(len(a.allapot.g) == 350, "350 fuggetlen stabilizator (7 + 343)")
    sig = a.narrativa_signatura()
    ellenoriz(sig == (1,) * 7, "friss narrativa: minden elme-vagas = 1 ebit %s" % (sig,))
    return a


def kiserlet_jelentester():
    banner("2. JELENES-TER: mennyi jelentes fer bele? (Clifford-szektor)")
    def allapotter_bit(n):
        return n + sum(log2((1 << k) + 1) for k in range(1, n + 1))
    abc = log2(22)
    print("    0. szint  FUL [[7,1,3]]:    64 szindroma, 22 betu (tiszta + 21 suly-1)")
    print("       -> %.2f bit / betu; allapotter = %.1f bit" % (abc, allapotter_bit(7)))
    print("    1. szint  ELME [[49,1,9]]:  allapotter = %.1f bit  (~egy bekezdes)"
          % allapotter_bit(49))
    print("    2. szint  NARRATIVA [[343,1,27]]: allapotter = %.1f bit (~egy novella)"
          % allapotter_bit(343))
    print("    -- de: a VEDETT logikai qubit minden szinten 1.")
    print("       a jelentes a vagasokban lakik; a logikai bit az 'en'.")


def kiserlet_tortenet(a):
    banner("3. A TORTENET FUT: 7 mondat -> 7 elme -> 1 narrativa")
    tortenet = [
        (["bit",   "brain", "star"],  False),
        (["code",  "time",  "bit"],   False),
        (["comma", "time",  "brain"], True),     # zajos!
        (["cut",   "code",  "brain"], False),
        (["star",  "cut",   "time"],  False),
        (["code",  "comma", "star"],  False),
        (["bit",   "brain", "star"],  False),    # a tortenet visszater a magjahoz
    ]
    for k, (szavak, zaj) in enumerate(tortenet, start=1):
        print("  >> %d. mondat (elme %d): %s%s"
              % (k, k, " ".join(szavak), "   [ZAJ!]" if zaj else ""))
        for j, szo in enumerate(szavak, start=1):
            p, felismert, zaj_p = a.hall(szo, zaj=(zaj and j == 1))
            a.gondol(blokk=j, pont=p)
            zajtxt = ("  (Z-zaj @%d javítva)" % zaj_p) if zaj_p else ""
            print("     [t_ext=%2d | t_int1=%2d | t_int2=%d] %-6s szindroma=%d%s"
                  % (a.t_ext, a.t_int1, a.t_int2, szo, felismert, zajtxt))
        tema = SZO_PONT[szavak[0].lower()]       # konvencio: tema = elso szo pontja
        sig = a.lezar_mondat(szavak, tema)
        print("     ENGRAM #%d allokalva (elme %d, tema=%d %s): blokk-vagasok %s"
              % (k, k, tema, PONT_SZO[tema][0], sig))
    print()
    nsig = a.narrativa_signatura()
    print("    NARRATIVA-signatura (7 elme-vagas): %s  (osszesen %d ebit)"
          % (nsig, sum(nsig)))
    print("    a tortenet visszatert a magjahoz: a 7. mondat = az 1. mondat")
    return nsig


def kiserlet_harom_ora(a, nsig):
    banner("4. HAROM ORA -- a beagyazott ket-ido (az agy ritmushierarchiaja)")
    S = sum(nsig)
    print("    t_ext  (kulso: merestick)       = %d" % a.t_ext)
    print("    t_int1 (belso-1: blokk/Singer)  = %d  (mod 7: %d) -- gondolat-ritmus"
          % (a.t_int1, a.t_int1 % 7))
    print("    t_int2 (belso-2: elme/Singer)   = %d  (mod 7: %d) -- tortenet-ritmus"
          % (a.t_int2, a.t_int2 % 7))
    print("    pszeudo-entropia RIME: S ~= %d + i*2pi*(%d/7) + i*2pi*(%d/7)"
          % (S, a.t_int1 % 7, a.t_int2 % 7))
    print("    -- gamma C theta C alfa: a torony orai nem ugyanazt mutatjak,")
    print("       es nem is kell; a vedett bit egyikert sem fizet.")
    print()
    print("    FELIDEZES-KASZKAD (cue='brain'):")
    for e in a.felidez("brain"):
        print("      elme %d: %s  (tema=%d, t_ext=%d)"
              % (e["elme"], " ".join(e["szavak"]), e["tema"], e["t_ext"]))


def kiserlet_itelet(a):
    banner("5. ITELET -- a hierarchia ara es ajandeka")
    ellenoriz(len(HIBAK) == 0, "onellenorzes tiszta (350 generator, szindroma-cimek, vagasok)")
    print("""
    A HIERARCHIA AJANDEKA (most fut):
      [x] KOMPOZICIO: szo -> gondolat -> tortenet; a Fano-grammatika minden
          szinten ugyanaz (onhasonlo torony)
      [x] HAROM ORA: t_ext / t_int1 / t_int2 -- beagyazott belso idok
      [x] KAPACITAS: 36 bit -> 1275 bit -> 59340 bit (Clifford-szektor)
      [x] AZ 'EN' VEDVE: a globalis logikai Z egyetlen qubit -- a 343 qubit
          forgataga korulotte; a jelentes a vagasokban, nem a bitben

    NYITOTT VESSZOK:
      ( ) FOKOZATOS jelentes: a stabilizator-vilag diszkret; a homalyos,
          folytonos jelentes = kevert allapotok + magic (a klasszikus iker dolga)
      ( ) TANULAS: a kotesek most konvenciok; Hebb = az RSTN-koteserosseg
      ( ) MELYEBB TORONY: [[2401,1,81]] = a vilagmodell szintje (4 ora...)
      ( ) GLIA: tobb ilyen torony osszekapcsolasa = a tarsadalom
    """)


def main():
    print("HANMAG-TORONY -- a jelentes tornya (haromszintes hurok-agy)")
    print("aforizma: a torony nem magasabb -- MELYEBB.")
    a = kiserlet_epites()
    kiserlet_jelentester()
    nsig = kiserlet_tortenet(a)
    kiserlet_harom_ora(a, nsig)
    kiserlet_itelet(a)
    if HIBAK:
        print("TORONY-HIBA: %d ellentmondas" % len(HIBAK))
    else:
        print("TORONY ELLENORIZVE -- a jelentesnek helye van.")


if __name__ == "__main__":
    main()
