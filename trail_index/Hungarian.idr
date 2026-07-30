module Hungarian

||| Hungarian case suffixes as logical relation markers.
||| Each case encodes a distinct grammatical → logical role.
public export
data Case = Nom | Acc | Dat | Ins | Com | Cau | Tra | Ter
          | Ill | Ine | Ela | All | Ade | Abl | Sup | Del | Sub
          | Tem | Soc | Dist | Ess | For | Mod | Cas

public export
Show Case where
  show Nom  = "∅";   show Acc  = "-t";   show Dat  = "-nak"
  show Ins  = "-val"; show Com  = "-stul"; show Cau  = "-ért"
  show Tra  = "-vá";  show Ter  = "-ig";   show Ill  = "-ba"
  show Ine  = "-ban"; show Ela  = "-ból";  show All  = "-hoz"
  show Ade  = "-nál"; show Abl  = "-tól";  show Sup  = "-n"
  show Del  = "-ról"; show Sub  = "-ra";   show Tem  = "-kor"
  show Soc  = "-ként"; show Dist = "-nként"; show Ess = "-ul"
  show For  = "-ért"; show Mod  = "-lag";  show Cas  = "-képp"

||| Each case maps to a logical relation.
||| This IS the grammar → logic bridge.
public export
data CaseLogic : Case -> Type where

  -- Core grammatical roles
  NomLogic  : CaseLogic Nom      -- subject / agent-of
  AccLogic  : CaseLogic Acc      -- object / patient-of

  -- Causal relations (matches Triggers from Ontology)
  CauLogic  : CaseLogic Cau      -- cause → because-of
  DatLogic  : CaseLogic Dat      -- recipient → caused-by

  -- Transformative relations (matches Resolves from Ontology)
  TraLogic  : CaseLogic Tra      -- transformation → results-in

  -- Spatial → logical mappings
  IllLogic  : CaseLogic Ill      -- into → becomes / specializes-to
  IneLogic  : CaseLogic Ine      -- in → context-of
  ElaLogic  : CaseLogic Ela      -- out-of → derived-from
  AllLogic  : CaseLogic All      -- toward → targets / implies
  SubLogic  : CaseLogic Sub      -- onto → applies-to / purpose

  -- Instrumental
  InsLogic  : CaseLogic Ins      -- with → via / using / by-means-of
  ComLogic  : CaseLogic Com      -- together-with → conjoined-with

  -- Relational
  AdeLogic  : CaseLogic Ade      -- at → relative-to / compared-to
  AblLogic  : CaseLogic Abl      -- from → originates-in / source-of
  DelLogic  : CaseLogic Del      -- about → topic-of / references
  SupLogic  : CaseLogic Sup      -- on → surface / topically

  -- Temporal
  TemLogic  : CaseLogic Tem      -- at-time → when

  -- Limit / boundary
  TerLogic  : CaseLogic Ter      -- until → up-to / bounded-by

  -- Predicative
  EssLogic  : CaseLogic Ess      -- as → in-role-of
  SocLogic  : CaseLogic Soc      -- as → in-capacity-of

||| Agglutination: a stem with a suffix stack.
||| The stack builds compositionally, like logical formulas.
public export
data Word : Type where
  Bare  : String -> Word
  Suffix : Word -> Case -> Word

||| A proposition in Hungarian case logic.
||| Case marks the logical role of each concept in the relation.
public export
data CaseProp : Type where
  MkCaseProp : (subject : String) -> (verb : String) 
            -> (object : String) -> (cases : List (Case, String))
            -> CaseProp

||| Convert Hungarian case structure to OctonionLogic truth mode.
||| Causative cases → Causal mode (I1).
||| Transformative cases → Deductive mode (I2).
||| Others map to the appropriate octonion dimension.
public export
caseToMode : Case -> OctVal
caseToMode Nom = R       -- definite truth
caseToMode Acc = R       -- definite truth
caseToMode Cau = I1      -- causal
caseToMode Tra = I2      -- deductive
caseToMode Dat = I3      -- hypothetical (purpose)
caseToMode Sub = I4      -- temporal (goal-oriented)
caseToMode Ela = I5      -- modal (origin/possibility)
caseToMode Ill = I6      -- deontic (becoming)
caseToMode Ine = I7      -- epistemic (context)
caseToMode _   = R
