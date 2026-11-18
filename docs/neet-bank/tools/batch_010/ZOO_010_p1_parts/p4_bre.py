

# ================================================================ Breathing and Exchange of Gases (B3 I5 A3)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Regulation and disorders", "Basic", "direct",
  "According to NCERT, the role of oxygen in the regulation of the respiratory rhythm is:",
  ["Quite insignificant", "The main stimulus that activates the respiratory rhythm centre",
   "Exerted mainly through the pneumotaxic centre", "Exerted mainly through the chemosensitive area"], "A",
  "Chemical regulation of respiration",
  "NCERT: a chemosensitive area adjacent to the rhythm centre is highly sensitive to CO₂ and hydrogen ions; receptors "
  "associated with the aortic arch and carotid artery also recognise changes in CO₂ and H⁺ concentration. The role of "
  "oxygen in the regulation of the respiratory rhythm is quite insignificant.",
  ["Main chemical signals → CO₂ and H⁺", "O₂ → quite insignificant"],
  R_BRE("regulation of respiration"),
  why_others_wrong="B, C and D give oxygen a major regulatory role; the chemosensitive area responds to CO₂ and H⁺, "
                   "and the pneumotaxic centre moderates the rhythm centre.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Basic", "statement_pair",
  sp("In humans, the alveoli are the primary sites of exchange of gases.",
     "The partial pressure of CO₂ in deoxygenated blood is about 45 mm Hg."),
  STATEMENT_PAIR, "A",
  "Site of exchange and a partial pressure value",
  "NCERT: alveoli are the primary sites of exchange of gases; exchange also occurs between blood and tissues. In "
  "NCERT's table of partial pressures, deoxygenated blood has pO₂ about 40 mm Hg and pCO₂ about 45 mm Hg.",
  ["Statement I → true", "Statement II → true"],
  R_BRE("exchange of gases"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=25)

Z(BRE, "Respiratory system", "Basic", "match_list",
  ml(("animal group", "means of gas exchange given in NCERT"),
     ["Insects", "Aquatic arthropods and molluscs", "Birds", "Coelenterates"],
     ["Gills", "Lungs", "Simple diffusion over the entire body surface", "A network of tubes (tracheal tubes)"]),
  match_options(M("IV", "I", "II", "III"), [M("I", "IV", "II", "III"), M("IV", "I", "III", "II"),
                                            M("IV", "II", "I", "III")], "C"), "C",
  "Respiratory organs in different animals",
  "NCERT: lower invertebrates like sponges, coelenterates and flatworms exchange O₂ with CO₂ by simple diffusion over "
  "their entire body surface. Insects have a network of tubes (tracheal tubes). Special vascularised structures called "
  "gills are used by most aquatic arthropods and molluscs. Reptiles, birds and mammals respire through lungs.",
  ["Insects → IV", "Aquatic arthropods and molluscs → I", "Birds → II", "Coelenterates → III"],
  R_BRE("respiratory organs"),
  why_others_wrong="A swaps the insects and aquatic arthropods; B swaps birds and coelenterates; D swaps gills and "
                   "lungs.",
  seconds=30)

_tv, _irv, _erv, _rv = 500, 3000, 1000, 1200
_vc = _tv + _irv + _erv
assert _vc == 4500 and round(100 * _tv / _vc, 1) == 11.1
assert round(100 * _tv / (_vc + _rv), 1) == 8.8 and round(100 * _tv / (_tv + _irv), 1) == 14.3
assert round(100 * _tv / (_tv + _erv), 1) == 33.3
Z(BRE, "Respiratory volumes", "Intermediate", "numerical",
  "Spirometry of a healthy adult gives a tidal volume of 500 mL, an inspiratory reserve volume of 3000 mL, an "
  "expiratory reserve volume of 1000 mL and a residual volume of 1200 mL. During quiet breathing, what percentage of "
  "his vital capacity is used in each breath (take one breath as the tidal volume)?",
  ["8.8%", "11.1%", "14.3%", "33.3%"], "B",
  "Tidal volume as a part of vital capacity",
  "NCERT: vital capacity is the maximum volume of air a person can breathe in after a forced expiration, i.e. "
  "ERV + TV + IRV. It does not include the residual volume. Here VC = 1000 + 500 + 3000 = 4500 mL, and the tidal "
  "volume is 500/4500 × 100 ≈ 11.1% of it.",
  ["VC = ERV + TV + IRV = 1000 + 500 + 3000 = 4500 mL", "TV / VC = 500 / 4500", "≈ 11.1%"],
  R_BRE("respiratory volumes and capacities"),
  shortcut="VC is 9 tidal volumes here, so one breath is 1/9 ≈ 11.1% of it.",
  why_others_wrong="A divides by the total lung capacity (adds the residual volume); C divides by the inspiratory "
                   "capacity (TV + IRV); D divides by the expiratory capacity (TV + ERV).",
  seconds=60, verified_by=RECOMPUTED)

Z(BRE, "Respiratory system", "Intermediate", "assertion_reason",
  ar("The larynx is called the sound box.",
     "During swallowing, the glottis can be covered by the epiglottis, which prevents the entry of food into the "
     "larynx."),
  ASSERTION_REASON, "B",
  "Larynx and epiglottis",
  "NCERT: the larynx is a cartilaginous box which helps in sound production and hence is called the sound box. "
  "NCERT also states that during swallowing the glottis can be covered by a thin, elastic, cartilaginous flap, the "
  "epiglottis, to prevent the entry of food into the larynx. The name 'sound box' comes from the role in sound "
  "production; closing the glottis during swallowing is an unrelated function.",
  ["A → true (helps in sound production)", "R → true (epiglottis guards the glottis)",
   "R concerns swallowing, not sound production → R does not explain A"],
  R_BRE("human respiratory system"),
  why_others_wrong="A links an unrelated protective function to the name; C and D reject true statements.",
  seconds=30)

_opts = ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b) and (c) only", "(a), (c), (d) and (e) only"]
Z(BRE, "Mechanism of breathing", "Intermediate", "multi_statement",
  ms("Which of the following take place during a normal inspiration in a human, according to NCERT?",
     ["The diaphragm contracts, increasing the volume of the thoracic chamber in the antero-posterior axis.",
      "The external inter-costal muscles contract and lift up the ribs and the sternum.",
      "The volume of the thoracic chamber increases in the dorso-ventral axis.",
      "The intra-pulmonary pressure becomes greater than the atmospheric pressure.",
      "The diaphragm relaxes and returns to its normal position."]),
  _opts, "C",
  "Events of inspiration",
  "NCERT: inspiration is initiated by contraction of the diaphragm, which increases the thoracic volume in the "
  "antero-posterior axis. Contraction of the external inter-costal muscles lifts up the ribs and the sternum, "
  "increasing the volume in the dorso-ventral axis. The overall increase in thoracic volume increases pulmonary "
  "volume, so the intra-pulmonary pressure falls BELOW atmospheric pressure and air moves in. Relaxation of the "
  "diaphragm belongs to expiration.",
  ["(a) true", "(b) true", "(c) true", "(d) false – pressure falls below atmospheric", "(e) false – that is "
   "expiration"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A and D include (d); B includes (e) and drops (a).",
  seconds=45)
ms_check("abc", _opts, "C")

Z(BRE, "Exchange and transport of gases", "Intermediate", "statement_pair",
  sp("The diffusion membrane in the lungs is made of only two layers: the squamous epithelium of the alveoli and the "
     "endothelium of the alveolar capillaries.",
     "The total thickness of the diffusion membrane is much less than a millimetre."),
  STATEMENT_PAIR, "D",
  "The diffusion membrane",
  "NCERT: the diffusion membrane is made up of three major layers – the thin squamous epithelium of the alveoli, the "
  "endothelium of the alveolar capillaries and the basement substance (composed of a thin basement membrane "
  "supporting the squamous epithelium and that surrounding the single-layer endothelial cells) between them. Its "
  "total thickness is much less than a millimetre, which favours diffusion.",
  ["Statement I → false (three layers – the basement substance is left out)", "Statement II → true"],
  R_BRE("exchange of gases"),
  why_others_wrong="A and C accept a two-layered membrane; B rejects the true Statement II.",
  seconds=35)

Z(BRE, "Respiratory system", "Intermediate", "direct",
  "Which of the following parts of the human respiratory tract is NOT among those that NCERT describes as supported "
  "by incomplete cartilaginous rings?",
  ["Trachea", "Primary bronchi", "Tertiary bronchi", "Terminal bronchioles"], "D",
  "Cartilaginous support of the airways",
  "NCERT: the trachea, the primary, secondary and tertiary bronchi, and the initial bronchioles are supported by "
  "incomplete cartilaginous rings. Repeated divisions of the tertiary bronchi end in very thin terminal bronchioles, "
  "which are not in this list.",
  ["Supported → trachea, primary, secondary, tertiary bronchi, initial bronchioles",
   "Terminal bronchioles → not listed"],
  R_BRE("human respiratory system"),
  why_others_wrong="A, B and C are all named by NCERT as supported by incomplete cartilaginous rings.",
  seconds=30)

_opts = ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only", "(a), (b), (c) and (d) only"]
Z(BRE, "Exchange and transport of gases", "Advanced", "multi_statement",
  ms("Using NCERT's table of partial pressures (in mm Hg) of O₂ and CO₂, which of the following comparisons are "
     "correct?",
     ["The pO₂ of alveolar air is lower than that of atmospheric air.",
      "The pCO₂ of alveolar air is higher than that of atmospheric air.",
      "The pO₂ of alveolar air is higher than that of oxygenated blood.",
      "The pCO₂ of alveolar air is equal to that of oxygenated blood.",
      "The pCO₂ of the tissues is lower than that of deoxygenated blood."]),
  _opts, "D",
  "Reading the table of partial pressures",
  "NCERT's values (O₂, CO₂): atmospheric air 159, 0.3; alveoli 104, 40; deoxygenated blood 40, 45; oxygenated blood "
  "95, 40; tissues 40, 45. So alveolar pO₂ (104) < atmospheric (159); alveolar pCO₂ (40) > atmospheric (0.3); "
  "alveolar pO₂ (104) > oxygenated blood (95); alveolar pCO₂ (40) = oxygenated blood (40); tissue pCO₂ (45) = "
  "deoxygenated blood (45), not lower.",
  ["(a) 104 < 159 → true", "(b) 40 > 0.3 → true", "(c) 104 > 95 → true", "(d) 40 = 40 → true",
   "(e) 45 = 45 → false"],
  R_BRE("exchange of gases – Table: partial pressures of oxygen and carbon dioxide"),
  why_others_wrong="A leaves out the correct (d); B and C include (e).",
  seconds=60)
ms_check("abcd", _opts, "D")

Z(BRE, "Mechanism of breathing", "Advanced", "assertion_reason",
  ar("Additional muscles in the abdomen can increase the strength of expiration.",
     "Normal (quiet) expiration is brought about by the contraction of the diaphragm."),
  ASSERTION_REASON, "C",
  "Normal and forceful expiration",
  "NCERT: we have the ability to increase the strength of inspiration and expiration with the help of additional "
  "muscles in the abdomen – A is true. Normal expiration takes place when the diaphragm and the inter-costal muscles "
  "RELAX, returning the diaphragm and sternum to their normal positions and reducing the thoracic volume; contraction "
  "of the diaphragm initiates inspiration. R is false.",
  ["A → true", "Diaphragm contraction → inspiration", "Diaphragm relaxation → expiration", "R → false"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A and B accept that diaphragm contraction causes expiration; D rejects NCERT's statement about "
                   "the abdominal muscles.",
  seconds=40)

Z(BRE, "Exchange and transport of gases", "Advanced", "direct",
  "A sample has a pO₂ of about 40 mm Hg and a pCO₂ of about 45 mm Hg. Using only NCERT's table of partial pressures, "
  "the sample could be:",
  ["Alveolar air or oxygenated blood", "Deoxygenated blood or the tissues", "Atmospheric air",
   "Oxygenated blood only"], "B",
  "Identifying a sample from partial pressures",
  "NCERT's table gives pO₂ 40 and pCO₂ 45 mm Hg for BOTH deoxygenated blood and the tissues, so the table alone "
  "cannot tell these two apart. Alveolar air (104, 40), oxygenated blood (95, 40) and atmospheric air (159, 0.3) do "
  "not match.",
  ["Deoxygenated blood → 40, 45", "Tissues → 40, 45", "Both match → either is possible"],
  R_BRE("exchange of gases – Table: partial pressures of oxygen and carbon dioxide"),
  why_others_wrong="A, C and D name samples whose pO₂ is far higher (95–159 mm Hg) and pCO₂ lower (0.3–40 mm Hg).",
  seconds=40)
