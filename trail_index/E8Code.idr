module E8Code

||| E8 lattice coordinates as an 8-tuple of integers.
public export
record E8Vec where
  constructor MKE8
  c1 : Int; c2 : Int; c3 : Int; c4 : Int
  c5 : Int; c6 : Int; c7 : Int; c8 : Int

||| Clifford algebra Cl(8) blade indexed by 8-bit mask.
||| ab = a·b + a∧b → inner product = overlap (redundant), outer = novelty.
public export
data Blade : Int -> Type where
  S  : Blade 0
  E1 : Blade 1;  E2 : Blade 2;  E3 : Blade 4;  E4 : Blade 8
  E5 : Blade 16; E6 : Blade 32; E7 : Blade 64; E8 : Blade 128

||| A concept/relationship embedded in E8 with Cl(8) decomposition.
public export
record CodeWord where
  constructor MkCW
  label : String
  embed : E8Vec
  inner : Int      -- Cl(8) inner component (scalar + symmetric)
  outer : Int      -- Cl(8) outer component (bivector + higher)

||| Does B have high overlap with A? If so → redundant, drop B.
public export
overlapThreshold : Double
overlapThreshold = 0.8

||| Decision after comparing two code words.
public export
data DropOrKeep = DropB | KeepBoth

||| Redundancy decision based on overlap.
public export
decide : Double -> DropOrKeep
decide o = if o > overlapThreshold then DropB else KeepBoth

||| Geometric product computes overlap from two code words.
||| High overlap → concept is redundant.
public export
overlap : CodeWord -> CodeWord -> Double
overlap a b =
  let dot = a.inner * b.inner + a.outer * b.outer
      na  = a.inner * a.inner + a.outer * a.outer
      nb  = b.inner * b.inner + b.outer * b.outer
  in cast dot / cast (na + nb + 1)
