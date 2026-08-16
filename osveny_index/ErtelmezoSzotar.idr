module ErtelmezoSzotar

-- ═══════════════════════════════════════════════════════════════
-- ÉRTELMEZŐ SZÓTÁR — minden szó és toldalék ADATTÍPUS
-- ═══════════════════════════════════════════════════════════════
-- ELV: minden magyar szó nevesített Fonetika-érték, tisztán
-- Hang-konstruktorokból. NINCS String a magban — csak a Show-ban.
--
-- A TOLDALÉKOK is típusok. Az agglutináció = list-összefűzés:
--   ragoz szHaz ragBan = ház + ban = házban
--
-- Az ÉKSZ-definíció: „Az X olyan Y, amely Z."
--   X = szócím | Y = genus (nem-fogalom) | Z = differentia
--   A Z ragjai Fillmore-szerepeket adnak (mélyeset-slotok).
-- ═══════════════════════════════════════════════════════════════

import Fonetika
import MagyarNyelvtan

%default total

-- ─── 0. RÖVIDÍTÉSEK ──────────────────────────────────────

MH : Maganhangzo -> Hang
MH = MaganhangzoHang

MS : Massalhangzo -> Hang
MS = MassalhangzoHang

DG : Digraf -> Hang
DG = DigrafHang

-- ─── 1. A TOLDALÉKOK MINT TÍPUSOK ─────────────────────────
-- Minden rag = Hang-konstruktorok listája + az esete.

public export
record Rag where
  constructor RagK
  ragFonetika : Fonetika
  ragEset     : Esetrag

-- fő esetragok (Kiefer 18 közül a leggyakoribbak):
public export ragBan : Rag   -- -ban inessivus
ragBan = RagK [MS Mb, MH Va, MS Mn] InessivusE

public export ragBen : Rag   -- -ben inessivus
ragBen = RagK [MS Mb, MH Ve, MS Mn] InessivusE

public export ragBa : Rag    -- -ba illativus
ragBa = RagK [MS Mb, MH Va] IllativusE

public export ragBe : Rag    -- -be illativus
ragBe = RagK [MS Mb, MH Ve] IllativusE

public export ragBol : Rag   -- -ból elativus
ragBol = RagK [MS Mb, MH Voo, MS Ml] ElativusE

public export ragBolMagas : Rag -- -ből elativus
ragBolMagas = RagK [MS Mb, MH Voe, MS Ml] ElativusE

public export ragNak : Rag   -- -nak dativus
ragNak = RagK [MS Mn, MH Va, MS Mk] DativusE

public export ragNek : Rag   -- -nek dativus
ragNek = RagK [MS Mn, MH Ve, MS Mk] DativusE

public export ragVal : Rag   -- -val instrumentalis
ragVal = RagK [MS Mv, MH Va, MS Ml] InstrumentalisE

public export ragVel : Rag   -- -vel instrumentalis
ragVel = RagK [MS Mv, MH Ve, MS Ml] InstrumentalisE

public export ragRa : Rag    -- -ra sublativus
ragRa = RagK [MS Mr, MH Va] SublativusE

public export ragRe : Rag    -- -re sublativus
ragRe = RagK [MS Mr, MH Ve] SublativusE

public export ragEr : Rag    -- -ért causalis
ragEr = RagK [MS Voe ... ]