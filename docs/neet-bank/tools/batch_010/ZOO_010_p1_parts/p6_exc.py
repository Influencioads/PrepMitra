

# ================================================================ Excretory Products and their Elimination (B4 I5 A4)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Urine formation", "Basic", "direct",
  "Which part of the nephron reabsorbs nearly all of the essential nutrients and 70–80 per cent of the electrolytes "
  "and water of the filtrate?",
  ["Distal convoluted tubule", "Proximal convoluted tubule", "Ascending limb of Henle's loop", "Collecting duct"],
  "B",
  "Reabsorption in the PCT",
  "NCERT: the PCT is lined by simple cuboidal brush border epithelium, which increases the surface area for "
  "reabsorption. Nearly all of the essential nutrients, and 70–80 per cent of electrolytes and water, are reabsorbed "
  "by this segment.",
  ["Maximum reabsorption, incl. nearly all nutrients → PCT"],
  R_EXC("function of the tubules"),
  why_others_wrong="A carries out conditional reabsorption of Na⁺ and water; C is impermeable to water; D reabsorbs "
                   "large amounts of water mainly to concentrate urine.",
  seconds=25)

Z(EXC, "Nephron structure", "Basic", "statement_pair",
  sp("The kidneys are situated close to the dorsal inner wall of the abdominal cavity.",
     "Each ureter carries urine from a kidney directly into the urethra."),
  STATEMENT_PAIR, "C",
  "Organs of the human excretory system",
  "NCERT: the kidneys are reddish-brown, bean-shaped structures situated between the levels of the last thoracic and "
  "third lumbar vertebra close to the dorsal inner wall of the abdominal cavity. The ureters open into the urinary "
  "bladder, which stores urine until it is released through the urethra.",
  ["Statement I → true", "Statement II → false: ureters open into the urinary bladder"],
  R_EXC("human excretory system"),
  why_others_wrong="A and D accept that the ureters lead straight to the urethra; B rejects the true Statement I.",
  seconds=25)

Z(EXC, "Urine formation", "Basic", "assertion_reason",
  ar("The urine of a healthy adult human is slightly acidic.",
     "On an average, 25–30 g of urea is excreted out per day."),
  ASSERTION_REASON, "B",
  "Characteristics of urine",
  "NCERT: the urine formed is a light yellow coloured watery fluid which is slightly acidic (pH 6.0) and has a "
  "characteristic odour; on an average, 25–30 g of urea is excreted out per day. Both are true, but the daily amount "
  "of urea is a separate fact and does not explain the pH of urine.",
  ["A → true (pH about 6.0)", "R → true (25–30 g urea/day)", "R does not explain A"],
  R_EXC("micturition"),
  why_others_wrong="A forges a link NCERT does not make; C and D reject true statements.",
  seconds=25)

Z(EXC, "Urine formation", "Basic", "direct",
  "Conditional reabsorption of Na⁺ and water takes place in which part of the nephron?",
  ["Proximal convoluted tubule", "Descending limb of Henle's loop", "Collecting duct",
   "Distal convoluted tubule"], "D",
  "Functions of the DCT",
  "NCERT: in the DCT, conditional reabsorption of Na⁺ and water takes place. The DCT is also capable of reabsorption "
  "of HCO₃⁻ and selective secretion of hydrogen and potassium ions and NH₃ to maintain the pH and sodium–potassium "
  "balance in blood.",
  ["Conditional reabsorption of Na⁺ and water → DCT"],
  R_EXC("function of the tubules"),
  why_others_wrong="A reabsorbs nutrients, electrolytes and water in bulk; B is permeable to water but almost "
                   "impermeable to electrolytes; C is the site of large-scale water reabsorption for concentrated urine.",
  seconds=25)

_gfr = 125  # mL per minute
_day = _gfr * 60 * 24 / 1000  # litres per day
assert _day == 180 and _day / 3 == 60 and _day / 5 == 36 and _day / 24 / 3 == 2.5 and _day / 3000 == 0.06
Z(EXC, "Urine formation", "Intermediate", "numerical",
  "A person has 5 L of blood, of which 3 L is plasma, and a glomerular filtration rate (GFR) of 125 mL per minute. "
  "In one day, the kidneys filter a volume equal to the person's whole plasma volume about how many times?",
  ["60", "36", "2.5", "0.06"], "A",
  "Scale of glomerular filtration",
  "NCERT: a GFR of 125 mL per minute means about 180 litres of filtrate per day. Filtration takes place from the "
  "plasma (blood cells and plasma proteins stay behind), so the daily filtrate is compared with the plasma volume.",
  ["Filtrate per day = 125 mL/min × 1440 min = 180,000 mL = 180 L", "Plasma = 3 L",
   "180 / 3 = 60 times"],
  R_EXC("urine formation – glomerular filtration"),
  shortcut="NCERT's 180 L/day ÷ 3 L = 60.",
  why_others_wrong="B divides by the whole blood volume; C gives the number per hour; D divides litres by "
                   "millilitres.",
  seconds=60, verified_by=RECOMPUTED)

_glucose_g_per_L = 100 / 1000 * 10  # 100 mg per 100 mL = 1 g per L
_filtered = _day * _glucose_g_per_L
assert _glucose_g_per_L == 1 and _filtered == 180
Z(EXC, "Urine formation", "Intermediate", "numerical",
  "A healthy person has a plasma glucose concentration of 100 mg per 100 mL and a GFR of 125 mL per minute. Glucose "
  "passes freely into the glomerular filtrate, and the person's urine contains no glucose. About how much glucose do "
  "the renal tubules reabsorb in one day?",
  ["1.8 g", "125 g", "0 g", "180 g"], "D",
  "Filtered load and reabsorption of glucose",
  "NCERT: almost all constituents of the plasma except the proteins pass into the filtrate, and substances like "
  "glucose are reabsorbed actively by the tubules (glucose in urine, glycosuria, indicates diabetes mellitus). If none "
  "appears in the urine, all the glucose filtered must have been reabsorbed.",
  ["Filtrate per day = 125 × 1440 mL = 180 L", "Glucose = 100 mg/100 mL = 1 g/L",
   "Filtered = 180 L × 1 g/L = 180 g", "Urine glucose = 0 → reabsorbed = 180 g"],
  R_EXC("urine formation – reabsorption"),
  shortcut="180 L/day × 1 g/L = 180 g, all of it reabsorbed.",
  why_others_wrong="A uses the daily urine volume instead of the filtrate; B mixes up the GFR value with grams; C "
                   "assumes glucose is not filtered at all.",
  seconds=70, verified_by=RECOMPUTED)

_opts = ["(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(a) and (c) only"]
Z(EXC, "Regulation of kidney function", "Intermediate", "multi_statement",
  ms("Which of the following can lead to an increase in blood pressure and GFR, according to NCERT?",
     ["Angiotensin II, being a powerful vasoconstrictor",
      "ADH, through its constrictory effects on blood vessels",
      "Aldosterone, which causes reabsorption of Na⁺ and water from the distal parts of the tubule",
      "Atrial natriuretic factor (ANF)",
      "Dilation of blood vessels (vasodilation)"]),
  _opts, "B",
  "Hormones raising blood pressure and GFR",
  "NCERT: angiotensin II, a powerful vasoconstrictor, increases the glomerular blood pressure and thereby GFR; ADH's "
  "constrictory effect on blood vessels increases blood pressure, which can increase glomerular blood flow and GFR; "
  "aldosterone causes reabsorption of Na⁺ and water from the distal parts of the tubule, which also leads to an "
  "increase in blood pressure and GFR. ANF causes vasodilation and decreases blood pressure, acting as a check on "
  "the renin–angiotensin mechanism.",
  ["(a) raises", "(b) raises", "(c) raises", "(d) lowers", "(e) lowers"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A includes ANF; C includes ANF and vasodilation; D leaves out ADH.",
  seconds=50)
ms_check("abc", _opts, "B")

Z(EXC, "Nephron structure", "Intermediate", "assertion_reason",
  ar("In cortical nephrons, the loop of Henle is too short and extends only very little into the medulla.",
     "The vasa recta is well developed in cortical nephrons."),
  ASSERTION_REASON, "C",
  "Cortical and juxtamedullary nephrons",
  "NCERT: in the majority of nephrons the loop of Henle is too short and extends only very little into the medulla; "
  "these are cortical nephrons. In some nephrons the loop is very long and runs deep into the medulla – the "
  "juxtamedullary nephrons. The vasa recta is absent or highly reduced in cortical nephrons. So A is true and R is "
  "false.",
  ["A → true", "R → false (vasa recta absent or highly reduced in cortical nephrons)"],
  R_EXC("human excretory system – nephron"),
  why_others_wrong="A and B accept a well-developed vasa recta in cortical nephrons; D rejects the true A.",
  seconds=35)

Z(EXC, "Urine formation", "Intermediate", "statement_pair",
  sp("The counter-current mechanism helps to maintain an increasing osmolarity towards the inner medullary "
     "interstitium, from about 300 mOsmol L⁻¹ in the cortex to about 1200 mOsmol L⁻¹ in the inner medulla.",
     "This gradient is mainly caused by NaCl and urea."),
  STATEMENT_PAIR, "A",
  "Medullary osmolarity gradient",
  "NCERT: the proximity between Henle's loop and the vasa recta, and the counter current in them, help in "
  "maintaining an increasing osmolarity towards the inner medullary interstitium, i.e. from 300 mOsmol L⁻¹ in the "
  "cortex to about 1200 mOsmol L⁻¹ in the inner medulla. This gradient is mainly caused by NaCl and urea.",
  ["Statement I → true", "Statement II → true"],
  R_EXC("mechanism of concentration of the filtrate"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=35)

_opts = ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (b), (c) and (e) only", "(a), (c) and (e) only"]
Z(EXC, "Urine formation", "Advanced", "multi_statement",
  ms("Trace a molecule of water from the blood in a glomerulus until it is either reabsorbed or reaches the urine. "
     "Which of the following statements are correct according to NCERT?",
     ["It leaves the glomerular blood across the endothelium of the glomerular blood vessels, the basement membrane "
      "and the epithelium of Bowman's capsule.",
      "In the initial segments of the nephron, it can be reabsorbed passively.",
      "It can leave the filtrate in the descending limb of Henle's loop.",
      "It can leave the filtrate in the ascending limb of Henle's loop.",
      "Large amounts of it can be reabsorbed from the collecting duct."]),
  _opts, "C",
  "Handling of water along the nephron",
  "NCERT: filtration takes place through the endothelium of the glomerular blood vessels, the epithelium of Bowman's "
  "capsule and a basement membrane between them. Reabsorption of water is passive in the initial segments of the "
  "nephron. The descending limb of Henle's loop is permeable to water but almost impermeable to electrolytes; the "
  "ascending limb is impermeable to water. Large amounts of water can be reabsorbed from the collecting duct to "
  "produce concentrated urine.",
  ["(a) true", "(b) true", "(c) true", "(d) false – ascending limb impermeable to water", "(e) true"],
  R_EXC("urine formation; function of the tubules"),
  why_others_wrong="A and B include (d); D leaves out the correct (b).",
  seconds=60)
ms_check("abce", _opts, "C")

_items = {"Reptiles": True, "Birds": True, "Land snails": True, "Marine fishes": False, "Mammals": False,
          "Aquatic amphibians": False, "Bony fishes": False, "Terrestrial amphibians": False}
_opts = ["3", "4", "5", "6"]
Z(EXC, "Modes of excretion", "Advanced", "direct",
  "How many of the following groups does NCERT describe as excreting their nitrogenous wastes mainly as uric acid "
  "(uricotelic)?\n\n" + ", ".join(_items),
  _opts, "A",
  "Ammonotelic, ureotelic and uricotelic animals",
  "NCERT: many bony fishes, aquatic amphibians and aquatic insects are ammonotelic; mammals, many terrestrial "
  "amphibians and marine fishes are ureotelic; reptiles, birds, land snails and insects are uricotelic. From the "
  "list, reptiles, birds and land snails are uricotelic.",
  ["Uricotelic → reptiles, birds, land snails = 3", "Ureotelic → marine fishes, mammals, terrestrial amphibians",
   "Ammonotelic → aquatic amphibians, bony fishes"],
  R_EXC("introduction – modes of excretion"),
  why_others_wrong="B, C and D add ureotelic or ammonotelic groups – often the terrestrial amphibians, which are "
                   "ureotelic.",
  seconds=45)
count_check(_items, _opts, "A")

Z(EXC, "Urine formation", "Advanced", "assertion_reason",
  ar("In a healthy person, the urine contains every constituent of the glomerular filtrate in the same proportion as "
     "the filtrate.",
     "Nearly 99 per cent of the filtrate has to be reabsorbed by the renal tubules."),
  ASSERTION_REASON, "D",
  "Selective reabsorption",
  "NCERT: comparing the filtrate formed per day (180 L) with the urine released (1.5 L) shows that nearly 99 per cent "
  "of the filtrate has to be reabsorbed by the renal tubules. Reabsorption is selective – glucose, amino acids and Na⁺ "
  "are reabsorbed actively, nitrogenous wastes passively – and substances like H⁺, K⁺ and ammonia are secreted. So the "
  "urine does not have the same proportions as the filtrate; A is false and R is true.",
  ["R → true (≈99% reabsorbed)", "Selective reabsorption and secretion change the proportions", "A → false"],
  R_EXC("urine formation – reabsorption and secretion"),
  why_others_wrong="A and B accept a false A; C rejects NCERT's true statement R.",
  seconds=40)

Z(EXC, "Regulation of kidney function", "Advanced", "statement_pair",
  sp("Both atrial natriuretic factor (ANF) and the renin–angiotensin mechanism tend to raise the blood pressure.",
     "ANF can cause vasodilation and thereby decrease the blood pressure, acting as a check on the renin–angiotensin "
     "mechanism."),
  STATEMENT_PAIR, "D",
  "ANF versus the renin–angiotensin mechanism",
  "NCERT: an increase in blood flow to the atria of the heart can cause the release of ANF. ANF can cause "
  "vasodilation (dilation of blood vessels) and thereby decrease the blood pressure; the ANF mechanism therefore acts "
  "as a check on the renin–angiotensin mechanism, which raises blood pressure. Statement I is false because ANF "
  "lowers blood pressure.",
  ["Statement I → false", "Statement II → true"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A and C accept that ANF raises blood pressure; B rejects the true Statement II.",
  seconds=35)
