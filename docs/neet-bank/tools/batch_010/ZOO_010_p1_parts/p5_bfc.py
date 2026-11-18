

# ================================================================ Body Fluids and Circulation (B4 I6 A4)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Human heart", "Basic", "statement_pair",
  sp("In the human heart, the atria are two relatively small upper chambers and the ventricles are two larger lower "
     "chambers.",
     "The right and left atria are separated by a thick-walled, fibrous inter-atrial septum."),
  STATEMENT_PAIR, "C",
  "Chambers and septa of the human heart",
  "NCERT: the heart has four chambers – two relatively small upper chambers called atria and two larger lower "
  "chambers called ventricles. A thin, muscular wall called the inter-atrial septum separates the right and left "
  "atria; it is the inter-ventricular septum that is thick-walled, and the atrio-ventricular septum that is a thick "
  "fibrous tissue.",
  ["Statement I → true", "Statement II → false: the inter-atrial septum is thin and muscular"],
  R_BFC("circulatory pathways – human circulatory system"),
  why_others_wrong="A and D accept a thick, fibrous inter-atrial septum; B rejects the true Statement I.",
  seconds=30)

Z(BFC, "Human heart", "Basic", "direct",
  "In the human heart, the atrium and the ventricle of the same side are separated by a thick fibrous tissue called "
  "the:",
  ["Inter-atrial septum", "Inter-ventricular septum", "Pericardium", "Atrio-ventricular septum"], "D",
  "Septa of the heart",
  "NCERT: the atrium and the ventricle of the same side are separated by a thick fibrous tissue called the "
  "atrio-ventricular septum; each of these septa has an opening that connects the two chambers of the same side. "
  "The inter-atrial septum (thin, muscular) separates the two atria and the inter-ventricular septum (thick-walled) "
  "separates the two ventricles. The pericardium is the double-walled membranous bag around the heart.",
  ["Atrium ↔ ventricle of the same side → atrio-ventricular septum"],
  R_BFC("circulatory pathways – human circulatory system"),
  why_others_wrong="A separates the two atria and B the two ventricles; C is the protective covering of the heart.",
  seconds=20)

Z(BFC, "Circulatory disorders", "Basic", "direct",
  "According to NCERT, coronary artery disease (CAD) is often referred to as:",
  ["Atherosclerosis", "Angina", "Heart failure", "Hypertension"], "A",
  "Coronary artery disease",
  "NCERT: coronary artery disease, often referred to as atherosclerosis, affects the vessels that supply blood to the "
  "heart muscle. It is caused by deposits of calcium, fat, cholesterol and fibrous tissues, which make the lumen of "
  "the arteries narrower. Angina, heart failure and hypertension are described as separate disorders.",
  ["CAD ↔ atherosclerosis"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="B is acute chest pain when not enough O₂ reaches the heart muscle; C is ineffective pumping; D is "
                   "blood pressure persistently above normal.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "assertion_reason",
  ar("Neutrophils are phagocytic cells.",
     "Neutrophils are the most abundant cells (60–65 per cent) of the total WBCs."),
  ASSERTION_REASON, "B",
  "Neutrophils",
  "NCERT: neutrophils are the most abundant cells (60–65 per cent) of the total WBCs; neutrophils and monocytes "
  "(6–8 per cent) are phagocytic cells which destroy foreign organisms entering the body. Both statements are true, "
  "but being numerous is not why a cell is phagocytic – monocytes are phagocytic too while forming only 6–8 per cent. "
  "R does not explain A.",
  ["A → true", "R → true", "Abundance ≠ phagocytic ability (monocytes are few yet phagocytic) → R does not explain A"],
  R_BFC("blood – formed elements"),
  why_others_wrong="A links a count to a function; C and D reject true statements.",
  seconds=30)

_rbc_per_mm3, _blood_mm3, _life = 4.8e6, 5 * 1e6, 120
_total = _rbc_per_mm3 * _blood_mm3
_per_day = _total / _life
assert abs(_total - 2.4e13) < 1e9 and abs(_per_day - 2.0e11) < 1e7
assert abs(_rbc_per_mm3 * 5 * 1e3 / _life - 2.0e8) < 1e4 and abs(_per_day / 24 - 8.3e9) < 0.05e9
Z(BFC, "Blood and blood groups", "Intermediate", "numerical",
  "A man has 5 L of blood containing 4.8 million RBCs per mm³. RBCs have an average life span of 120 days. Assuming "
  "that his RBC count stays constant and that every RBC lives exactly 120 days, about how many RBCs are destroyed "
  "(and replaced) in his body each day? (Take 1 L = 10⁶ mm³.)",
  ["2.0 × 10⁸", "8.3 × 10⁹", "2.0 × 10¹¹", "2.4 × 10¹³"], "C",
  "Life span of RBCs",
  "NCERT: RBCs have an average life span of 120 days, after which they are destroyed in the spleen (graveyard of "
  "RBCs). With a constant count, the number destroyed each day equals the total number divided by the life span.",
  ["Blood volume = 5 L = 5 × 10⁶ mm³", "Total RBCs = 4.8 × 10⁶ × 5 × 10⁶ = 2.4 × 10¹³",
   "Per day = 2.4 × 10¹³ / 120 = 2.0 × 10¹¹"],
  R_BFC("blood – formed elements (erythrocytes)"),
  shortcut="4.8 × 5 = 24, and 24/120 = 0.2; powers: 10⁶ × 10⁶ = 10¹² → 0.2 × 10¹² = 2 × 10¹¹.",
  why_others_wrong="A takes 1 L as 1000 mm³; B gives the number per hour; D is the total number of RBCs, not the "
                   "number per day.",
  seconds=75, verified_by=RECOMPUTED)

Z(BFC, "Circulatory disorders", "Intermediate", "statement_pair",
  sp("Heart failure is sometimes called congestive heart failure because congestion of the lungs is one of its main "
     "symptoms.",
     "Cardiac arrest is the condition in which the heart muscle is suddenly damaged by an inadequate blood supply."),
  STATEMENT_PAIR, "C",
  "Heart failure, cardiac arrest and heart attack",
  "NCERT: heart failure means the state of the heart when it is not pumping blood effectively enough to meet the "
  "needs of the body; it is sometimes called congestive heart failure because congestion of the lungs is one of its "
  "main symptoms. Heart failure is not the same as cardiac arrest (when the heart stops beating) or a heart attack "
  "(when the heart muscle is suddenly damaged by an inadequate blood supply). Statement II describes a heart attack.",
  ["Statement I → true", "Statement II → false: that is a heart attack, not cardiac arrest"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="A and D accept the definition of heart attack as cardiac arrest; B rejects the true Statement I.",
  seconds=35)

Z(BFC, "Coagulation and lymph", "Intermediate", "assertion_reason",
  ar("Interstitial (tissue) fluid lacks the larger proteins and most of the formed elements of blood.",
     "Interstitial fluid has a mineral distribution different from that of plasma."),
  ASSERTION_REASON, "C",
  "Composition of interstitial fluid",
  "NCERT: as blood passes through the capillaries in tissues, some water along with many small water-soluble "
  "substances moves out into the spaces between the cells, leaving the larger proteins and most of the formed "
  "elements in the blood vessels. This interstitial fluid has the SAME mineral distribution as that in plasma. So A "
  "is true but R is false.",
  ["A → true", "R → false (same mineral distribution as plasma)"],
  R_BFC("lymph (tissue fluid)"),
  why_others_wrong="A and B accept a false R; D rejects the true A.",
  seconds=35)

_opts = ["(a), (b), (c) and (e) only", "(a), (b) and (c) only", "(a) and (d) only", "(b), (c) and (d) only"]
Z(BFC, "Double circulation and regulation", "Intermediate", "multi_statement",
  ms("Which of the following statements about the hepatic portal system and the coronary system are correct, "
     "according to NCERT?",
     ["The hepatic portal vein carries blood from the intestine to the liver before it is delivered to the systemic "
      "circulation.",
      "The hepatic portal system is a unique vascular connection between the digestive tract and the liver.",
      "The coronary system circulates blood exclusively to and from the cardiac musculature.",
      "The hepatic portal vein carries blood from the liver to the intestine.",
      "The coronary system is a part of the pulmonary circulation."]),
  _opts, "B",
  "Special vascular connections",
  "NCERT: a unique vascular connection exists between the digestive tract and liver, called the hepatic portal "
  "system; the hepatic portal vein carries blood from the intestine to the liver before it is delivered to the "
  "systemic circulation. A special coronary system of blood vessels is present in our body exclusively for the "
  "circulation of blood to and from the cardiac musculature. Pulmonary circulation is the path between the right "
  "ventricle, the lungs and the left atrium.",
  ["(a) true", "(b) true", "(c) true", "(d) false – direction reversed", "(e) false – it serves the heart muscle, not "
   "the lungs"],
  R_BFC("double circulation"),
  why_others_wrong="A includes (e); C and D include the reversed direction in (d).",
  seconds=45)
ms_check("abc", _opts, "B")

Z(BFC, "Blood and blood groups", "Intermediate", "direct",
  "Which of the following leucocytes is phagocytic but is NOT a granulocyte?",
  ["Monocyte", "Neutrophil", "Lymphocyte", "Basophil"], "A",
  "Granulocytes, agranulocytes and phagocytes",
  "NCERT: neutrophils, eosinophils and basophils are granulocytes; lymphocytes and monocytes are agranulocytes. "
  "Neutrophils and monocytes are phagocytic cells. The only cell that is both phagocytic and an agranulocyte is the "
  "monocyte.",
  ["Phagocytic → neutrophils, monocytes", "Agranulocytes → lymphocytes, monocytes", "Common to both → monocyte"],
  R_BFC("blood – formed elements (leucocytes)"),
  why_others_wrong="B is phagocytic but a granulocyte; C is an agranulocyte but responsible for immune responses, not "
                   "described as phagocytic; D is a granulocyte that secretes histamine, serotonin and heparin.",
  seconds=35)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "match_list",
  ml(("event", "record of it"),
     ["Closure of the tricuspid and bicuspid valves", "Closure of the semilunar valves",
      "Depolarisation of the atria", "Return of the ventricles from the excited to the normal state"],
     ["T-wave of the ECG", "P-wave of the ECG", "Second heart sound, 'dub'", "First heart sound, 'lub'"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("III", "IV", "I", "II")], "D"), "D",
  "Heart sounds and ECG waves",
  "NCERT: the first heart sound (lub) is associated with the closure of the tricuspid and bicuspid valves, and the "
  "second (dub) with the closure of the semilunar valves. In the ECG, the P-wave represents the electrical "
  "excitation (depolarisation) of the atria, and the T-wave represents the return of the ventricles from the excited "
  "to the normal state (repolarisation).",
  ["AV valves close → lub (IV)", "Semilunar valves close → dub (III)", "Atrial depolarisation → P (II)",
   "Ventricular repolarisation → T (I)"],
  R_BFC("cardiac cycle; electrocardiograph (ECG)"),
  why_others_wrong="A swaps the two heart sounds; B swaps the P- and T-waves; C swaps both pairs.",
  seconds=40)

Z(BFC, "Double circulation and regulation", "Advanced", "direct",
  "An RBC enters the right atrium through the vena cava and travels by the shortest route until it leaves the heart "
  "in the aorta. In which order does it pass the valves of the heart?",
  ["Bicuspid → semilunar valve of the pulmonary artery → tricuspid → semilunar valve of the aorta",
   "Tricuspid → semilunar valve of the pulmonary artery → bicuspid → semilunar valve of the aorta",
   "Tricuspid → bicuspid → semilunar valve of the pulmonary artery → semilunar valve of the aorta",
   "Semilunar valve of the pulmonary artery → tricuspid → semilunar valve of the aorta → bicuspid"], "B",
  "Valves met in double circulation",
  "Right atrium → (tricuspid valve) → right ventricle → (semilunar valve) → pulmonary artery → lungs → pulmonary "
  "veins → left atrium → (bicuspid/mitral valve) → left ventricle → (semilunar valve) → aorta. NCERT: the tricuspid "
  "valve guards the opening between the right atrium and right ventricle, the bicuspid between the left atrium and "
  "left ventricle, and semilunar valves guard the openings of the right and left ventricles into the pulmonary artery "
  "and the aorta.",
  ["RA → tricuspid → RV", "RV → semilunar → pulmonary artery → lungs", "Pulmonary veins → LA → bicuspid → LV",
   "LV → semilunar → aorta"],
  R_BFC("human circulatory system; double circulation"),
  why_others_wrong="A starts on the left side; C skips the pulmonary circuit between the two atrio-ventricular "
                   "valves; D puts a semilunar valve before the tricuspid.",
  seconds=50)

Z(BFC, "Cardiac cycle and ECG", "Advanced", "assertion_reason",
  ar("In a standard ECG, the QRS complex represents the contraction of the atria.",
     "The contraction of the ventricles starts shortly after Q and marks the beginning of the systole."),
  ASSERTION_REASON, "D",
  "Meaning of the QRS complex",
  "NCERT: the P-wave represents depolarisation of the atria, which leads to the contraction of both the atria. The "
  "QRS complex represents the depolarisation of the ventricles, which initiates ventricular contraction; the "
  "contraction starts shortly after Q and marks the beginning of the systole. A is false; R is true.",
  ["QRS → ventricular depolarisation (not atrial)", "A → false", "R → true"],
  R_BFC("electrocardiograph (ECG)"),
  why_others_wrong="A and B accept a false A; C rejects the true R.",
  seconds=35)

Z(BFC, "Double circulation and regulation", "Advanced", "statement_pair",
  sp("In fishes, the heart pumps out oxygenated blood, which then goes to the gills.",
     "In birds and mammals, the oxygenated and deoxygenated blood received by the left and right atria respectively "
     "pass on to the ventricles of the same sides."),
  STATEMENT_PAIR, "D",
  "Single and double circulation",
  "NCERT: in fishes the heart pumps out deoxygenated blood, which is oxygenated by the gills and supplied to the body "
  "parts, from where deoxygenated blood is carried back to the heart (single circulation). In birds and mammals, "
  "oxygenated and deoxygenated blood received by the left and right atria respectively pass on to the ventricles of "
  "the same sides; the ventricles pump it out without any mixing (double circulation).",
  ["Statement I → false (fish heart pumps deoxygenated blood)", "Statement II → true"],
  R_BFC("circulatory pathways"),
  why_others_wrong="A and C accept that the fish heart pumps oxygenated blood; B rejects the true Statement II.",
  seconds=40)

_hr, _sv = 75, 70
assert 60 / _hr == 0.8 and _hr * _sv == 5250 and 2 * _hr == 150 and 2 * _hr * _sv == 10500
_opts = ["(a), (b), (c) and (d) only", "(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"]
Z(BFC, "Cardiac cycle and ECG", "Advanced", "multi_statement",
  ms("A person's heart beats 75 times per minute, and each ventricle pumps out 70 mL of blood in each cardiac cycle. "
     "Which of the following statements are correct?",
     ["The duration of each cardiac cycle is 0.8 s.",
      "His cardiac output is 5250 mL per minute.",
      "His heart produces 150 prominent heart sounds ('lub' and 'dub') per minute.",
      "His left ventricle pumps out 70 mL of blood into the aorta in each cardiac cycle.",
      "His two ventricles together pump out a total of 5250 mL of blood per minute."]),
  _opts, "A",
  "Stroke volume, cardiac output and heart sounds",
  "NCERT: the stroke volume is the volume of blood pumped out by each ventricle during a cardiac cycle (about 70 mL), "
  "and cardiac output = stroke volume × heart rate is the volume pumped out by EACH ventricle per minute. Two "
  "prominent sounds (lub and dub) are produced in each cycle. Here: cycle = 60/75 = 0.8 s; cardiac output = 70 × 75 = "
  "5250 mL/min; sounds = 2 × 75 = 150 per minute; the two ventricles together pump 2 × 5250 = 10500 mL/min.",
  ["(a) 60/75 = 0.8 s → true", "(b) 70 × 75 = 5250 mL/min → true", "(c) 2 × 75 = 150 → true",
   "(d) stroke volume of each ventricle → true", "(e) both ventricles → 10500 mL/min → false"],
  R_BFC("cardiac cycle"),
  why_others_wrong="B and D include (e), which forgets that cardiac output is per ventricle; C leaves out the correct "
                   "(a).",
  seconds=75)
ms_check("abcd", _opts, "A")
