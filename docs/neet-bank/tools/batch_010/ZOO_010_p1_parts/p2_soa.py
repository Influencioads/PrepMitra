

# ================================================================ Structural Organisation in Animals (B4 I5 A4)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "In the brain of the frog, the fore-brain includes the olfactory lobes, the paired cerebral hemispheres and an "
  "unpaired:",
  ["Optic lobe", "Diencephalon", "Cerebellum", "Medulla oblongata"], "B",
  "Divisions of the frog brain",
  "NCERT: the frog brain is divided into fore-brain, mid-brain and hind-brain. The fore-brain includes the olfactory "
  "lobes, the paired cerebral hemispheres and the unpaired diencephalon. The mid-brain is characterised by a pair of "
  "optic lobes; the hind-brain consists of the cerebellum and the medulla oblongata.",
  ["Fore-brain → olfactory lobes + paired cerebral hemispheres + unpaired diencephalon"],
  R_SOA("frogs – neural system"),
  why_others_wrong="A belongs to the mid-brain (and is paired); C and D form the hind-brain.",
  seconds=25)

Z(SOA, "Animal tissues", "Basic", "statement_pair",
  sp("Smooth muscle fibres are held together by cell junctions and are bundled together in a connective tissue "
     "sheath.",
     "The walls of blood vessels contain smooth muscle tissue."),
  STATEMENT_PAIR, "A",
  "Smooth muscle",
  "NCERT: the smooth muscle fibres taper at both ends (fusiform) and do not show striations. Cell junctions hold them "
  "together and they are bundled together in a connective tissue sheath. The wall of internal organs such as the "
  "blood vessels, stomach and intestine contains this type of muscle tissue.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("animal tissues – muscle tissue"),
  why_others_wrong="B, C and D reject at least one of two correct NCERT statements.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Basic", "assertion_reason",
  ar("In the frog, fats are emulsified in the duodenum.",
     "The duodenum receives bile from the gall bladder through a common bile duct, and bile emulsifies fat."),
  ASSERTION_REASON, "A",
  "Fat digestion in the frog",
  "NCERT: the duodenum receives bile from the gall bladder and pancreatic juices from the pancreas through a common "
  "bile duct. Bile emulsifies fat and pancreatic juices digest carbohydrates and proteins. Fat is emulsified in the "
  "duodenum precisely because bile arrives there – R explains A.",
  ["A → true", "R → true", "Bile reaches the duodenum and emulsifies fat → R explains A"],
  R_SOA("frogs – digestive system"),
  why_others_wrong="B misses the direct link; C and D reject statements that NCERT makes.",
  seconds=30)

Z(SOA, "Animal tissues", "Basic", "match_list",
  ml(("cell", "tissue in which NCERT describes it"), ["Mast cells", "Chondrocytes", "Osteocytes", "Neuroglia"],
     ["Neural tissue", "Bone", "Areolar tissue", "Cartilage"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "II", "IV", "I"),
                                            M("III", "IV", "I", "II")], "C"), "C",
  "Cells of different tissues",
  "NCERT: areolar tissue contains fibroblasts, macrophages and mast cells; cartilage cells (chondrocytes) are enclosed "
  "in small cavities within the matrix; bone cells (osteocytes) lie in spaces called lacunae; neuroglial cells protect "
  "and support the neurons of neural tissue.",
  ["Mast cells → areolar tissue (III)", "Chondrocytes → cartilage (IV)", "Osteocytes → bone (II)",
   "Neuroglia → neural tissue (I)"],
  R_SOA("animal tissues – connective tissue; neural tissue"),
  why_others_wrong="A swaps areolar tissue and cartilage; B swaps cartilage and bone; D swaps bone and neural tissue.",
  seconds=30)

_opts = ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a) and (d) only", "(a), (b) and (d) only"]
Z(SOA, "Frog: morphology and anatomy", "Intermediate", "multi_statement",
  ms("Which of the following statements about the lungs and heart of the frog are correct, according to NCERT?",
     ["The lungs are a pair of elongated, pink-coloured, sac-like structures in the upper part of the trunk region "
      "(thorax).",
      "The heart is a muscular structure situated in the upper part of the body cavity.",
      "The heart has two atria and two ventricles.",
      "The ventricle opens into a sac-like conus arteriosus on the ventral side of the heart.",
      "The sinus venosus joins the left atrium."]),
  _opts, "D",
  "Lungs and heart of the frog",
  "NCERT: the lungs are a pair of elongated, pink-coloured sac-like structures in the upper part of the trunk region "
  "(thorax). The heart is a muscular structure in the upper part of the body cavity with three chambers – two atria "
  "and one ventricle. A triangular sinus venosus joins the RIGHT atrium, and the ventricle opens into a sac-like "
  "conus arteriosus on the ventral side of the heart.",
  ["(a) true", "(b) true", "(c) false – one ventricle", "(d) true", "(e) false – sinus venosus joins the right atrium"],
  R_SOA("frogs – respiratory and circulatory systems"),
  why_others_wrong="A includes (c); B includes (e); C leaves out the correct (b).",
  seconds=50)
ms_check("abd", _opts, "D")

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "According to NCERT, glandular epithelium is formed when some of the cells of which kinds of epithelium become "
  "specialised for secretion?",
  ["Squamous or compound epithelium", "Columnar or cuboidal epithelium", "Squamous epithelium only",
   "Compound epithelium only"], "B",
  "Origin of glandular epithelium",
  "NCERT: some of the columnar or cuboidal cells get specialised for secretion and are called glandular epithelium. "
  "Such glands may be unicellular (goblet cells of the alimentary canal) or multicellular (salivary gland). Squamous "
  "epithelium forms a diffusion boundary, and compound epithelium has only a limited role in secretion.",
  ["Glandular epithelium ← specialised columnar or cuboidal cells"],
  R_SOA("animal tissues – epithelial tissue"),
  why_others_wrong="A, C and D name squamous or compound epithelium, which NCERT describes as a diffusion boundary or "
                   "as protective, not as the source of glandular cells.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "statement_pair",
  sp("In the male frog, the cloaca is used to pass faecal matter, urine and sperms to the exterior.",
     "In the female frog, the oviducts arising from the ovaries open into the cloaca separately."),
  STATEMENT_PAIR, "A",
  "Cloaca and genital ducts of the frog",
  "NCERT: the cloaca is a small, median chamber that is used to pass faecal matter, urine and sperms to the exterior "
  "(male). In the female, the ovaries have no functional connection with the kidneys, and a pair of oviducts arising "
  "from the ovaries opens into the cloaca separately.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("frogs – reproductive system"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "assertion_reason",
  ar("The lymph of the frog differs from its blood in lacking RBCs.",
     "The RBCs of the frog are nucleated and contain a red-coloured pigment, haemoglobin."),
  ASSERTION_REASON, "B",
  "Blood and lymph of the frog",
  "NCERT: the lymph is different from blood – it lacks a few proteins and the RBCs. Separately, NCERT states that the "
  "frog's RBCs are nucleated and contain the red pigment haemoglobin. Whether RBCs have a nucleus has nothing to do "
  "with their absence from lymph, so R does not explain A.",
  ["A → true", "R → true", "A nucleus in the RBC is unrelated to the RBC's absence from lymph → R does not explain A"],
  R_SOA("frogs – circulatory system"),
  why_others_wrong="A forges a link NCERT does not make; C and D reject true statements.",
  seconds=35)

Z(SOA, "Animal tissues", "Intermediate", "match_list",
  ml(("structure", "description in NCERT"), ["Goblet cell", "Salivary gland", "Ciliated epithelium",
                                             "Compound epithelium"],
     ["Main function is protection against chemical and mechanical stresses",
      "Unicellular glandular epithelium",
      "Moves particles or mucus in a specific direction",
      "Multicellular gland"]),
  match_options(M("II", "IV", "III", "I"), [M("IV", "II", "III", "I"), M("II", "IV", "I", "III"),
                                            M("II", "III", "IV", "I")], "D"), "D",
  "Glandular, ciliated and compound epithelia",
  "NCERT: glandular epithelium may be unicellular, consisting of isolated glandular cells (goblet cells of the "
  "alimentary canal), or multicellular, consisting of clusters of cells (salivary gland). Ciliated epithelium moves "
  "particles or mucus in a specific direction. The main function of compound epithelium is protection against "
  "chemical and mechanical stresses.",
  ["Goblet cell → II", "Salivary gland → IV", "Ciliated epithelium → III", "Compound epithelium → I"],
  R_SOA("animal tissues – epithelial tissue"),
  why_others_wrong="A swaps the unicellular and multicellular glands; B swaps the ciliated and compound epithelia; C "
                   "swaps the salivary gland and ciliated epithelium.",
  seconds=40)

_opts = ["(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
Z(SOA, "Frog: morphology and anatomy", "Advanced", "multi_statement",
  ms("A frog swallows an insect. Which of the following statements about what happens to the insect are correct, "
     "according to NCERT?",
     ["It is captured by the bilobed tongue.",
      "In the stomach, it is digested by the action of HCl and gastric juices.",
      "The partially digested food (chyme) passes from the stomach into the duodenum.",
      "Its fats are emulsified by pancreatic juice.",
      "Its final digestion takes place in the rectum."]),
  _opts, "B",
  "Path of digestion in the frog",
  "NCERT: food is captured by the bilobed tongue; digestion takes place by the action of HCl and gastric juices "
  "secreted from the walls of the stomach; partially digested food called chyme passes from the stomach to the "
  "duodenum. Bile (not pancreatic juice) emulsifies fat, pancreatic juices digest carbohydrates and proteins, and "
  "the final digestion takes place in the intestine. The rectum only passes undigested solid waste to the cloaca.",
  ["(a) true", "(b) true", "(c) true", "(d) false – bile emulsifies fat", "(e) false – final digestion is in the "
   "intestine"],
  R_SOA("frogs – digestive system"),
  why_others_wrong="A includes (d); C and D include (e) and drop correct statements.",
  seconds=60)
ms_check("abc", _opts, "B")

_items = {"Tip of the nose": True, "Outer ear joints": True, "Between adjacent bones of the vertebral column": True,
          "Limbs": True, "Hands": True, "Walls of the stomach": False, "Walls of blood vessels": False,
          "Air sacs of the lungs": False}
_opts = ["2", "3", "4", "5"]
Z(SOA, "Animal tissues", "Advanced", "direct",
  "NCERT lists the sites where cartilage is present in the body of an adult human. How many of the following sites "
  "are in that list?\n\n" + "; ".join(_items),
  _opts, "D",
  "Sites of cartilage in adults",
  "NCERT: most of the cartilages in vertebrate embryos are replaced by bones in adults. Cartilage is present in our "
  "body at the tip of the nose, outer ear joints, between adjacent bones of the vertebral column, limbs and hands in "
  "adults. The walls of the stomach and of blood vessels contain smooth muscle, and the air sacs of the lungs are "
  "made of squamous epithelium.",
  ["Listed → tip of nose, outer ear joints, between vertebrae, limbs, hands = 5",
   "Not listed → stomach wall, blood-vessel walls, air sacs"],
  R_SOA("animal tissues – connective tissue (cartilage)"),
  why_others_wrong="A, B and C leave out some of NCERT's listed sites, usually the limbs and hands.",
  seconds=50)
count_check(_items, _opts, "D")

Z(SOA, "Frog: morphology and anatomy", "Advanced", "assertion_reason",
  ar("In the frog, the renal portal system carries blood from the intestine to the liver.",
     "Frogs have special venous connections between the liver and the intestine as well as between the kidney and "
     "the lower parts of the body."),
  ASSERTION_REASON, "D",
  "Portal systems of the frog",
  "NCERT: special venous connections between the liver and intestine, and between the kidney and lower parts of the "
  "body, are present in frogs. The former is the hepatic portal system and the latter the renal portal system. So R "
  "is true, but A is false: blood from the intestine to the liver travels in the HEPATIC portal system.",
  ["R → true (two portal connections)", "Liver–intestine → hepatic portal system",
   "Kidney–lower body → renal portal system", "A → false"],
  R_SOA("frogs – circulatory system"),
  why_others_wrong="A and B accept the mislabelled portal system; C rejects NCERT's true statement R.",
  seconds=40)

Z(SOA, "Animal tissues", "Advanced", "statement_pair",
  sp("Of the three types of muscle tissue, skeletal muscle is the one closely attached to skeletal bones.",
     "Both smooth muscle fibres and cardiac muscle fibres show striations."),
  STATEMENT_PAIR, "C",
  "Comparing the three types of muscle tissue",
  "NCERT: skeletal muscle tissue is closely attached to skeletal bones (e.g. the biceps), and its fibres are striated. "
  "Smooth muscle fibres do not show striations; cardiac muscle is striated. Statement II is therefore false because "
  "of smooth muscle.",
  ["Statement I → true", "Statement II → false: smooth muscle is non-striated"],
  R_SOA("animal tissues – muscle tissue"),
  why_others_wrong="A and D accept striated smooth muscle; B rejects the true Statement I.",
  seconds=35)
