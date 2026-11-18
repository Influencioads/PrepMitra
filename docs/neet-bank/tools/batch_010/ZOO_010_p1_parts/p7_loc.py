

# ================================================================ Locomotion and Movement (B4 I5 A4)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Muscle contraction", "Basic", "direct",
  "Each meromyosin of a thick filament has a globular head with a short arm and a tail. NCERT calls the tail the:",
  ["Heavy meromyosin (HMM)", "Tropomyosin", "Light meromyosin (LMM)", "Troponin"], "C",
  "Structure of meromyosin",
  "NCERT: each myosin (thick) filament is a polymerised protein of many monomeric proteins called meromyosins. Each "
  "meromyosin has two important parts – a globular head with a short arm, called heavy meromyosin (HMM), and a tail, "
  "called light meromyosin (LMM). Tropomyosin and troponin are proteins of the thin (actin) filament.",
  ["Head + short arm → HMM", "Tail → LMM"],
  R_LOC("structure of contractile proteins"),
  why_others_wrong="A is the head with its short arm; B and D belong to the actin filament.",
  seconds=25)

Z(LOC, "Muscle contraction", "Basic", "statement_pair",
  sp("The light bands of a myofibril contain actin and are called I-bands or isotropic bands.",
     "The dark bands of a myofibril contain myosin and are called A-bands or anisotropic bands."),
  STATEMENT_PAIR, "A",
  "Bands of a myofibril",
  "NCERT: each myofibril has alternate dark and light bands. The light bands contain actin and are called I-band or "
  "isotropic band, whereas the dark band, called 'A' or anisotropic band, contains myosin.",
  ["Statement I → true", "Statement II → true"],
  R_LOC("skeletal muscle"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=25)

Z(LOC, "Skeletal system", "Basic", "assertion_reason",
  ar("Each rib is called bicephalic.",
     "The first seven pairs of ribs are called true ribs."),
  ASSERTION_REASON, "B",
  "Ribs",
  "NCERT: each rib is a thin flat bone connected dorsally to the vertebral column and ventrally to the sternum; it has "
  "two articulation surfaces on its dorsal end and is hence called bicephalic. NCERT also states that the first seven "
  "pairs are true ribs, attached dorsally to the thoracic vertebrae and ventrally to the sternum. The ventral "
  "attachment of the true ribs has nothing to do with the two dorsal articulation surfaces that make every rib "
  "bicephalic.",
  ["A → true (two dorsal articulation surfaces)", "R → true", "R concerns ventral attachment → does not explain A"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="A links two unrelated features of ribs; C and D reject true statements.",
  seconds=30)

Z(LOC, "Skeletal system", "Basic", "match_list",
  ml(("bone", "description in NCERT"), ["Clavicle", "Femur", "Patella", "Hyoid"],
     ["Single U-shaped bone present at the base of the buccal cavity", "Cup-shaped bone that covers the knee "
      "ventrally", "Longest bone of the body", "Long slender bone with two curvatures, commonly called the collar "
      "bone"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Identifying individual bones",
  "NCERT: each clavicle is a long slender bone with two curvatures, commonly called the collar bone; the femur (thigh "
  "bone) is the longest bone of the body; the patella is a cup-shaped bone that covers the knee ventrally (knee cap); "
  "a single U-shaped bone called the hyoid is present at the base of the buccal cavity.",
  ["Clavicle → IV", "Femur → III", "Patella → II", "Hyoid → I"],
  R_LOC("skeletal system"),
  why_others_wrong="A swaps the clavicle and the femur; B swaps the femur and the patella; C swaps the patella and "
                   "the hyoid.",
  seconds=30)

_limbs, _pectoral, _pelvic = 4 * 30, 2 * 2, 2
_appendicular = _limbs + _pectoral + _pelvic
_phalanges = 4 * 14
assert _appendicular == 126 and _appendicular - _phalanges == 70
assert _limbs - _phalanges == 64 and (_limbs + _pectoral + 6) - _phalanges == 74
Z(LOC, "Skeletal system", "Intermediate", "numerical",
  "Each upper limb and each lower limb has 30 bones, of which 14 are phalanges. Each half of the pectoral girdle has "
  "a clavicle and a scapula, and the pelvic girdle consists of two coxal bones. How many bones of the appendicular "
  "skeleton (limbs plus girdles) are NOT phalanges?",
  ["56", "70", "64", "74"], "B",
  "Counting bones of the appendicular skeleton",
  "NCERT: the appendicular skeleton is made of the bones of the limbs along with their girdles. Four limbs × 30 = "
  "120 bones; pectoral girdle 2 × 2 = 4; pelvic girdle = 2 coxal bones. Total = 126. Phalanges = 4 × 14 = 56. "
  "Non-phalangeal bones = 126 − 56 = 70.",
  ["Limbs = 4 × 30 = 120", "Girdles = 4 + 2 = 6", "Appendicular = 126", "Phalanges = 4 × 14 = 56",
   "126 − 56 = 70"],
  R_LOC("skeletal system – appendicular skeleton"),
  why_others_wrong="A is the number of phalanges itself; C forgets the girdles; D counts each coxal bone as its three "
                   "fused bones (ilium, ischium, pubis).",
  seconds=70, verified_by=RECOMPUTED)

_opts = ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only", "(a), (b), (c) and (d) only"]
Z(LOC, "Skeletal system", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human skull are correct, according to NCERT?",
     ["The cranium is made of 8 bones that form a hard protective outer covering for the brain.",
      "The facial region is made up of 14 skeletal elements which form the front part of the skull.",
      "The hyoid, a single U-shaped bone at the base of the buccal cavity, is included in the skull.",
      "The skull articulates with the vertebral column with the help of two occipital condyles (dicondylic skull).",
      "Each middle ear contains two tiny bones, the ear ossicles."]),
  _opts, "D",
  "The human skull",
  "NCERT: the skull is composed of cranial and facial bones totalling 22 – the cranium has 8 bones and the facial "
  "region 14 skeletal elements. A single U-shaped hyoid at the base of the buccal cavity is also included in the "
  "skull. Each middle ear contains THREE tiny bones – malleus, incus and stapes – collectively called ear ossicles. "
  "The skull articulates with the superior region of the vertebral column with the help of two occipital condyles "
  "(dicondylic skull).",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – three ossicles in each middle ear"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="A leaves out the correct (d); B and C include (e).",
  seconds=50)
ms_check("abcd", _opts, "D")

Z(LOC, "Muscle contraction", "Intermediate", "assertion_reason",
  ar("During muscle contraction, the Z-lines of a sarcomere are pulled closer to each other.",
     "The myosin cross bridges pull the attached actin filaments towards the centre of the A-band, and the Z-lines "
     "are attached to these actin filaments."),
  ASSERTION_REASON, "A",
  "Sliding filament mechanism",
  "NCERT: the myosin head binds to the exposed active sites on actin to form a cross bridge, which pulls the attached "
  "actin filaments towards the centre of the 'A' band. The 'Z' line attached to these actins is also pulled inwards, "
  "thereby causing a shortening of the sarcomere, i.e. contraction. R is the mechanism by which the Z-lines come "
  "closer – it explains A.",
  ["A → true", "R → true", "Actins pulled to the A-band centre drag the Z-lines with them → R explains A"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="B misses the direct cause; C and D reject statements that NCERT makes.",
  seconds=35)

Z(LOC, "Skeletal system", "Intermediate", "statement_pair",
  sp("The number of cervical vertebrae is seven in almost all mammals, including human beings.",
     "The vertebral column is dorsally placed and extends from the base of the skull."),
  STATEMENT_PAIR, "A",
  "The vertebral column",
  "NCERT: the vertebral column is formed by 26 serially arranged units called vertebrae and is dorsally placed. It "
  "extends from the base of the skull and constitutes the main framework of the trunk. The number of cervical "
  "vertebrae is seven in almost all mammals including human beings.",
  ["Statement I → true", "Statement II → true"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=30)

Z(LOC, "Joints", "Intermediate", "match_list",
  ml(("structure", "what articulates with it"), ["Glenoid cavity", "Acetabulum", "Acromion", "Occipital condyles"],
     ["Clavicle", "Atlas (first vertebra)", "Head of the humerus", "Thigh bone (femur)"]),
  match_options(M("III", "IV", "I", "II"), [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"),
                                            M("I", "IV", "III", "II")], "C"), "C",
  "Articulations of the skeleton",
  "NCERT: below the acromion of the scapula is a depression called the glenoid cavity, which articulates with the "
  "head of the humerus to form the shoulder joint; the clavicle articulates with the acromion. At the point of "
  "fusion of the ilium, ischium and pubis is a cavity called the acetabulum, to which the thigh bone articulates. The "
  "first vertebra, the atlas, articulates with the occipital condyles of the skull.",
  ["Glenoid cavity → humerus (III)", "Acetabulum → femur (IV)", "Acromion → clavicle (I)",
   "Occipital condyles → atlas (II)"],
  R_LOC("skeletal system – appendicular and axial skeleton"),
  why_others_wrong="A swaps the glenoid cavity and the acetabulum; B swaps the acromion and the occipital condyles; D "
                   "swaps the glenoid cavity and the acromion.",
  seconds=45)

_items = {"Knee joint": True, "Joint between the humerus and the pectoral girdle": True,
          "Joint between the atlas and the axis": True, "Joint between the carpals": True,
          "Joint between the carpal and the metacarpal of the thumb": True,
          "Joints between adjacent vertebrae": False, "Sutures between the flat bones of the skull": False}
_opts = ["4", "5", "6", "7"]
Z(LOC, "Joints", "Advanced", "direct",
  "How many of the following are synovial joints, according to NCERT?\n\n" + "; ".join(_items),
  _opts, "B",
  "Fibrous, cartilaginous and synovial joints",
  "NCERT: synovial joints have a fluid-filled synovial cavity between the articulating surfaces. Examples: ball and "
  "socket (humerus and pectoral girdle), hinge (knee), pivot (atlas and axis), gliding (between the carpals) and "
  "saddle (carpal and metacarpal of the thumb). The joint between adjacent vertebrae is cartilaginous, and the "
  "sutures of the cranium are fibrous joints.",
  ["Synovial → knee, shoulder, atlas–axis, carpals, thumb = 5", "Cartilaginous → adjacent vertebrae",
   "Fibrous → skull sutures"],
  R_LOC("joints"),
  why_others_wrong="A misses one synovial joint; C counts the vertebral joints; D counts every joint listed.",
  seconds=50)
count_check(_items, _opts, "B")

_opts = ["(a), (c) and (e) only", "(c), (d) and (e) only", "(a), (b) and (e) only", "(a), (b), (c) and (e) only"]
Z(LOC, "Skeletal system", "Advanced", "multi_statement",
  ms("Which of the following bones are present as a pair (one on each side of the body), rather than as a single "
     "median bone?",
     ["Clavicle", "Sternum", "Patella", "Hyoid", "Scapula"]),
  _opts, "A",
  "Paired and median bones",
  "NCERT: each half of the pectoral girdle consists of a clavicle and a scapula, so both are paired; each lower limb "
  "has a patella, so there are two. The sternum is a flat bone on the ventral midline of the thorax, and the hyoid is "
  "a single U-shaped bone at the base of the buccal cavity – both are single median bones.",
  ["(a) paired – one clavicle in each half of the pectoral girdle", "(b) single – ventral midline",
   "(c) paired – one in each lower limb", "(d) single – U-shaped bone", "(e) paired"],
  R_LOC("skeletal system"),
  why_others_wrong="B includes the hyoid and drops the clavicle; C and D include the sternum.",
  seconds=45)
ms_check("ace", _opts, "A")

Z(LOC, "Muscle contraction", "Advanced", "assertion_reason",
  ar("White muscle fibres depend on anaerobic processes for energy.",
     "White muscle fibres contain plenty of mitochondria."),
  ASSERTION_REASON, "C",
  "Red and white muscle fibres",
  "NCERT: some muscles possess very little myoglobin and appear pale or whitish – the white fibres. The number of "
  "mitochondria is also few in them, but the amount of sarcoplasmic reticulum is high, and they depend on anaerobic "
  "processes for energy. Plenty of mitochondria is a feature of red (aerobic) fibres. A is true, R is false.",
  ["A → true", "R → false (white fibres have few mitochondria)"],
  R_LOC("skeletal muscle – red and white fibres"),
  why_others_wrong="A and B accept many mitochondria in white fibres; D rejects the true A.",
  seconds=35)

Z(LOC, "Skeletal system", "Advanced", "statement_pair",
  sp("The 8th, 9th and 10th pairs of ribs do not articulate directly with the sternum but join the seventh rib with "
     "the help of hyaline cartilage.",
     "The 11th and 12th pairs of ribs are not connected dorsally to the vertebral column."),
  STATEMENT_PAIR, "C",
  "True, false and floating ribs",
  "NCERT: there are 12 pairs of ribs, each connected dorsally to the vertebral column. The first seven pairs are true "
  "ribs. The 8th, 9th and 10th pairs do not articulate directly with the sternum but join the seventh rib with the "
  "help of hyaline cartilage – the vertebrochondral (false) ribs. The last two pairs (11th and 12th) are not "
  "connected VENTRALLY and are therefore called floating ribs; dorsally they are attached to the vertebral column "
  "like every other rib.",
  ["Statement I → true", "Statement II → false: floating ribs are free ventrally, not dorsally"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="A and D accept that floating ribs are free dorsally; B rejects the true Statement I.",
  seconds=40)
