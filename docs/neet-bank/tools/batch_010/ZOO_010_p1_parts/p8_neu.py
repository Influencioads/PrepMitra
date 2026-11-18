

# ================================================================ Neural Control and Coordination (B4 I5 A4)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The whole complex of nerves, fibres, ganglia and plexuses by which impulses travel from the CNS to the viscera "
  "and from the viscera to the CNS is the visceral nervous system. According to NCERT, it is a part of the:",
  ["Central neural system", "Spinal cord", "Peripheral neural system", "Forebrain"],
  "C",
  "Divisions of the human neural system",
  "NCERT: the human neural system is divided into the central neural system (brain and spinal cord) and the "
  "peripheral neural system (all the nerves associated with the CNS). The visceral nervous system is the part of the "
  "peripheral nervous system that comprises the whole complex of nerves, fibres, ganglia and plexuses by which "
  "impulses travel from the CNS to the viscera and from the viscera to the CNS.",
  ["CNS → brain + spinal cord", "Visceral nervous system → nerves, fibres, ganglia, plexuses → PNS"],
  R_NEU("human neural system"),
  why_others_wrong="A, B and D name the CNS or parts of it, whereas nerves, ganglia and plexuses outside the brain "
                   "and spinal cord form the PNS.",
  seconds=25)

Z(NEU, "Neuron and nerves", "Basic", "statement_pair",
  sp("In a myelinated nerve fibre, the myelin sheath around the axon is formed by Schwann cells.",
     "The gaps between two adjacent myelin sheaths are called nodes of Ranvier."),
  STATEMENT_PAIR, "A",
  "Myelinated nerve fibres",
  "NCERT: the myelinated nerve fibres are enveloped with Schwann cells, which form a myelin sheath around the axon. "
  "The gaps between two adjacent myelin sheaths are called nodes of Ranvier. Myelinated fibres are found in spinal "
  "and cranial nerves.",
  ["Statement I → true", "Statement II → true"],
  R_NEU("structure of neuron"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=25)

Z(NEU, "Nervous system divisions", "Basic", "assertion_reason",
  ar("The cerebral cortex is referred to as the grey matter.",
     "The cerebral cortex contains motor areas, sensory areas and large regions that are neither clearly sensory nor "
     "motor in function."),
  ASSERTION_REASON, "B",
  "Cerebral cortex",
  "NCERT: the layer of cells covering the cerebral hemisphere is the cerebral cortex; it is referred to as the grey "
  "matter due to its greyish appearance, the neuron cell bodies being concentrated there. NCERT also states that the "
  "cortex contains motor areas, sensory areas and association areas. The kinds of functional areas present have "
  "nothing to do with the grey colour, so R does not explain A.",
  ["A → true (concentrated cell bodies give a grey look)", "R → true (functional areas)",
   "Functional areas do not explain the colour → R does not explain A"],
  R_NEU("central neural system – forebrain"),
  why_others_wrong="A gives a functional reason for a structural feature; C and D reject true statements.",
  seconds=30)

Z(NEU, "Neuron and nerves", "Basic", "match_list",
  ml(("structure", "description in NCERT"), ["Cerebral aqueduct", "Arachnoid", "Nissl's granules", "Dendrites"],
     ["Short fibres that branch repeatedly and transmit impulses towards the cell body",
      "Very thin middle layer of the cranial meninges",
      "Granular bodies in the cytoplasm of the cell body and dendrites",
      "Canal that passes through the midbrain"]),
  match_options(M("IV", "II", "III", "I"), [M("II", "IV", "III", "I"), M("IV", "II", "I", "III"),
                                            M("IV", "III", "II", "I")], "B"), "B",
  "Structures of the neural system",
  "NCERT: a canal called the cerebral aqueduct passes through the midbrain; the cranial meninges are an outer dura "
  "mater, a very thin middle arachnoid and an inner pia mater; the cell body and dendrites contain certain granular "
  "bodies called Nissl's granules; dendrites are short fibres which branch repeatedly, project out of the cell body "
  "and transmit impulses towards the cell body.",
  ["Cerebral aqueduct → IV", "Arachnoid → II", "Nissl's granules → III", "Dendrites → I"],
  R_NEU("structure of neuron; central neural system"),
  why_others_wrong="A swaps the cerebral aqueduct and the arachnoid; C swaps Nissl's granules and dendrites; D swaps "
                   "the arachnoid and Nissl's granules.",
  seconds=35)

_opts = ["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only"]
Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "multi_statement",
  ms("A stimulus applied at a site on a polarised axonal membrane makes the membrane at that site freely permeable "
     "to Na⁺. Which of the following statements about that site, shortly afterwards, are correct according to NCERT?",
     ["Na⁺ rushes in rapidly.",
      "The inner surface of the membrane becomes positively charged with respect to the outer surface.",
      "The membrane at the site is said to be depolarised.",
      "The electrical potential difference across the membrane at the site is the action potential, which is termed "
      "a nerve impulse.",
      "The resting potential can never be restored at this site."]),
  _opts, "C",
  "Generation of an action potential",
  "NCERT: when a stimulus is applied at a site on the polarised membrane, the membrane there becomes freely permeable "
  "to Na⁺, leading to a rapid influx of Na⁺ followed by the reversal of polarity – the outer surface becomes "
  "negatively charged and the inner positively charged. The polarity is reversed and the membrane is depolarised; "
  "the potential difference at the site is called the action potential, which is in fact termed a nerve impulse. The "
  "rise in Na⁺ permeability is extremely short-lived; it is quickly followed by a rise in K⁺ permeability, and K⁺ "
  "diffuses outside, restoring the resting potential.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – K⁺ outflow restores the resting potential"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A and D include (e); B leaves out the Na⁺ influx in (a).",
  seconds=50)
ms_check("abcd", _opts, "C")

_items = {"Voluntary movements": True, "Balance of the body": True, "Thermoregulation": True,
          "Hunger and thirst": True, "Circadian (24-hour) rhythms of the body": True,
          "Processing of vision and hearing": True, "Ultrafiltration of blood": False,
          "Production of red blood cells": False}
_opts = ["3", "4", "5", "6"]
Z(NEU, "Nervous system divisions", "Intermediate", "direct",
  "NCERT lists the functions that the human brain controls or for which it is the site of processing. How many of "
  "the following are in that list?\n\n" + "; ".join(_items),
  _opts, "D",
  "Functions of the brain",
  "NCERT: the brain is the central information processing organ and acts as the command and control system. It "
  "controls voluntary movements, balance of the body, functioning of vital involuntary organs (e.g. lungs, heart, "
  "kidneys), thermoregulation, hunger and thirst, circadian (24-hour) rhythms, activities of several endocrine glands "
  "and human behaviour. It is also the site for processing of vision, hearing, speech, memory, intelligence, emotions "
  "and thoughts. Ultrafiltration of blood takes place in the glomeruli of the kidney, and RBCs are produced in the "
  "red bone marrow.",
  ["In NCERT's list → voluntary movements, balance, thermoregulation, hunger and thirst, circadian rhythms, "
   "vision and hearing = 6", "Not in the list → ultrafiltration, RBC production"],
  R_NEU("central neural system – human brain"),
  why_others_wrong="A, B and C leave out functions NCERT lists, most often thermoregulation or the circadian rhythms.",
  seconds=45)
count_check(_items, _opts, "D")

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "assertion_reason",
  ar("In a resting neuron, the fluid outside the axon contains a high concentration of Na⁺ and a low concentration "
     "of K⁺.",
     "The sodium-potassium pump transports 3 Na⁺ outwards for 2 K⁺ into the cell."),
  ASSERTION_REASON, "A",
  "Ionic gradients across the resting axonal membrane",
  "NCERT: the axoplasm contains a high concentration of K⁺ and negatively charged proteins and a low concentration of "
  "Na⁺, while the fluid outside the axon contains a low concentration of K⁺ and a high concentration of Na⁺. NCERT "
  "states that these ionic gradients across the resting membrane are maintained by the active transport of ions by "
  "the sodium-potassium pump, which transports 3 Na⁺ outwards for 2 K⁺ into the cell. R therefore explains A.",
  ["A → true", "R → true", "NCERT: the pump maintains these ionic gradients → R explains A"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="B ignores NCERT's statement that the pump maintains the gradients; C and D reject true "
                   "statements.",
  seconds=35)

Z(NEU, "Nervous system divisions", "Intermediate", "statement_pair",
  sp("The hypothalamus is the major coordinating centre for sensory and motor signalling.",
     "The cerebrum wraps around a structure called the thalamus."),
  STATEMENT_PAIR, "D",
  "Thalamus and hypothalamus",
  "NCERT: the cerebrum wraps around a structure called the thalamus, which is a major coordinating centre for "
  "sensory and motor signalling. The hypothalamus lies at the base of the thalamus and contains centres that control "
  "body temperature and the urge for eating and drinking, as well as neurosecretory cells. Statement I gives the "
  "thalamus's role to the hypothalamus.",
  ["Statement I → false (that is the thalamus)", "Statement II → true"],
  R_NEU("central neural system – forebrain"),
  why_others_wrong="A and C accept the hypothalamus as the sensory–motor coordinating centre; B rejects the true "
                   "Statement II.",
  seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "match_list",
  ml(("event in impulse transmission", "where it takes place"),
     ["Synaptic vesicles fuse with the membrane and release neurotransmitters",
      "Neurotransmitters bind to specific receptors and ion channels open",
      "Released neurotransmitters cross the fluid-filled space between the two neurons",
      "Electric current flows directly from one neuron into the other"],
     ["Electrical synapse", "Post-synaptic membrane", "Synaptic cleft",
      "Plasma membrane of the synaptic knob (pre-synaptic membrane)"]),
  match_options(M("IV", "II", "III", "I"), [M("II", "IV", "III", "I"), M("IV", "III", "II", "I"),
                                            M("IV", "II", "I", "III")], "C"), "C",
  "Steps of synaptic transmission",
  "NCERT: when an impulse arrives at the axon terminal, it stimulates the movement of synaptic vesicles towards the "
  "membrane, where they fuse with the plasma membrane and release their neurotransmitters into the synaptic cleft "
  "(the fluid-filled space separating the pre- and post-synaptic membranes of a chemical synapse). The released "
  "neurotransmitters bind to their specific receptors present on the post-synaptic membrane, and ion channels open. "
  "At electrical synapses the membranes are in very close proximity and electric current can flow directly from one "
  "neuron into the other.",
  ["Vesicle fusion → pre-synaptic membrane (IV)", "Receptor binding → post-synaptic membrane (II)",
   "Crossing the gap → synaptic cleft (III)", "Direct current flow → electrical synapse (I)"],
  R_NEU("transmission of impulses"),
  why_others_wrong="A swaps the pre- and post-synaptic membranes; B swaps receptor binding and the synaptic cleft; D "
                   "swaps the synaptic cleft and the electrical synapse.",
  seconds=45)

_opts = ["(a), (b), (c) and (d) only", "(a), (b), (d) and (e) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
Z(NEU, "Nervous system divisions", "Advanced", "multi_statement",
  ms("Which of the following statements about the human hindbrain are correct, according to NCERT?",
     ["It comprises the pons, the cerebellum and the medulla (medulla oblongata).",
      "The pons consists of fibre tracts that interconnect different regions of the brain.",
      "It contains the corpora quadrigemina.",
      "The medulla of the brain is connected to the spinal cord.",
      "The cerebellum has a very convoluted surface, which provides additional space for many more neurons."]),
  _opts, "B",
  "Structure of the hindbrain",
  "NCERT: the hindbrain comprises the pons, cerebellum and medulla (also called the medulla oblongata). The pons "
  "consists of fibre tracts that interconnect different regions of the brain. The cerebellum has a very convoluted "
  "surface in order to provide the additional space for many more neurons. The medulla of the brain is connected to "
  "the spinal cord. The corpora quadrigemina are four round swellings on the dorsal portion of the midbrain.",
  ["(a) true", "(b) true", "(c) false – corpora quadrigemina are in the midbrain", "(d) true", "(e) true"],
  R_NEU("central neural system – hindbrain"),
  why_others_wrong="A and C include (c); D leaves out the correct (b).",
  seconds=50)
ms_check("abde", _opts, "B")

Z(NEU, "Neuron and nerves", "Advanced", "assertion_reason",
  ar("Afferent nerve fibres carry regulatory impulses from the CNS to the muscles.",
     "Efferent nerve fibres transmit regulatory impulses from the CNS to the concerned peripheral tissues and "
     "organs."),
  ASSERTION_REASON, "D",
  "Afferent and efferent fibres",
  "NCERT: the nerve fibres of the PNS are of two types – afferent fibres transmit impulses from tissues/organs to the "
  "CNS, and efferent fibres transmit regulatory impulses from the CNS to the concerned peripheral tissues/organs. A "
  "describes efferent fibres but names them afferent, so A is false; R is true.",
  ["Afferent → towards the CNS", "Efferent → away from the CNS", "A → false", "R → true"],
  R_NEU("human neural system"),
  why_others_wrong="A and B accept the reversed direction for afferent fibres; C rejects the true R.",
  seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "statement_pair",
  sp("In the resting state, the axonal membrane is impermeable to the negatively charged proteins present in the "
     "axoplasm.",
     "In the resting state, the outer surface of the axonal membrane possesses a negative charge, while its inner "
     "surface is positively charged."),
  STATEMENT_PAIR, "C",
  "The polarised membrane",
  "NCERT: the axonal membrane is comparatively more permeable to K⁺ and nearly impermeable to Na⁺; similarly, the "
  "membrane is impermeable to the negatively charged proteins present in the axoplasm. In the resting state, the "
  "outer surface of the axonal membrane possesses a POSITIVE charge while its inner surface becomes negatively "
  "charged – it is polarised. The charges in Statement II describe a depolarised site, not a resting one.",
  ["Statement I → true", "Statement II → false: at rest the outside is positive and the inside negative"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A and D accept the reversed resting charges; B rejects the true Statement I.",
  seconds=35)

Z(NEU, "Nervous system divisions", "Advanced", "match_list",
  ml(("effect of damage", "structure most likely damaged"),
     ["Loss of communication between the two cerebral hemispheres",
      "Disturbed control of body temperature and of the urge for eating and drinking",
      "Failure of the centres that control respiration, cardiovascular reflexes and gastric secretions",
      "Disturbed regulation of sexual behaviour and of emotional reactions such as excitement, pleasure, rage and "
      "fear, together with the hypothalamus"],
     ["Limbic system (amygdala and hippocampus)", "Medulla oblongata", "Hypothalamus", "Corpus callosum"]),
  match_options(M("IV", "III", "II", "I"), [M("IV", "I", "II", "III"), M("III", "IV", "II", "I"),
                                            M("IV", "II", "III", "I")], "D"), "D",
  "Functions localised to brain regions",
  "NCERT: the two cerebral hemispheres are connected by a tract of nerve fibres, the corpus callosum. The "
  "hypothalamus contains centres which control body temperature and the urge for eating and drinking. The medulla "
  "contains centres which control respiration, cardiovascular reflexes and gastric secretions. The limbic system "
  "(with the amygdala and hippocampus), along with the hypothalamus, is involved in the regulation of sexual "
  "behaviour and the expression of emotional reactions.",
  ["A → corpus callosum (IV)", "B → hypothalamus (III)", "C → medulla (II)", "D → limbic system (I)"],
  R_NEU("central neural system – forebrain and hindbrain"),
  why_others_wrong="A swaps the hypothalamus and the limbic system; B swaps the corpus callosum and the hypothalamus; "
                   "C swaps the hypothalamus and the medulla.",
  seconds=55)
