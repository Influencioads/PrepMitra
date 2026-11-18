
# ================================================================ Neural Control and Coordination (4/6/4)
Z(NCC, "Nervous system divisions", B, D,
  "Which of the following parts of the human brain belongs to the hindbrain but is NOT a part of the brain stem?",
  "Hindbrain versus brain stem",
  "NCERT: the hindbrain comprises the pons, cerebellum and medulla oblongata. The midbrain, pons and medulla "
  "oblongata together form the brain stem. The cerebellum is therefore in the hindbrain but outside the brain "
  "stem.",
  ["Hindbrain = pons + cerebellum + medulla oblongata", "Brain stem = midbrain + pons + medulla oblongata",
   "Common to the hindbrain only: cerebellum"],
  "Central Neural System",
  at="A", correct="Cerebellum",
  wrong=["Pons", "Medulla oblongata", "Corpora quadrigemina"],
  why="The pons and the medulla oblongata are in the hindbrain and are also parts of the brain stem; the corpora "
      "quadrigemina are on the dorsal side of the midbrain, so they are in the brain stem but not in the "
      "hindbrain.", secs=25)

Z(NCC, "Neuron and nerves", B, D,
  "NCERT classifies neurons into multipolar, bipolar and unipolar types. On what basis is this classification "
  "made?",
  "Types of neurons",
  "NCERT: based on the number of axon and dendrites, the neurons are divided into three types: multipolar (one "
  "axon and two or more dendrites), bipolar (one axon and one dendrite) and unipolar (cell body with one axon "
  "only).",
  ["Multipolar: 1 axon, 2 or more dendrites", "Bipolar: 1 axon, 1 dendrite", "Unipolar: cell body with 1 axon only",
   "-> basis = number of axon and dendrites"],
  "Neuron as Structural and Functional Unit of Neural System",
  at="C", correct="The number of axon and dendrites",
  wrong=["Whether the axon is myelinated or unmyelinated", "The direction in which the neuron carries impulses",
         "The number of synaptic knobs at the end of the axon"],
  why="Myelination is the basis for classing nerve fibres (myelinated and unmyelinated), not neurons into "
      "multipolar, bipolar and unipolar; direction of conduction is the basis for afferent and efferent fibres; "
      "NCERT does not class neurons by the number of synaptic knobs.", secs=25)

Z(NCC, "Neuron and nerves", B, STP,
  SP("Like the cell body, the dendrites of a neuron contain Nissl's granules.",
     "The axon of a neuron transmits nerve impulses towards the cell body."),
  "Dendrites and axon compared",
  "NCERT: short fibres which branch repeatedly and project out of the cell body also contain Nissl's granules "
  "and are called dendrites; these fibres transmit impulses towards the cell body. The axon is a long fibre that "
  "transmits nerve impulses away from the cell body to a synapse or to a neuromuscular junction.",
  ["Statement I: true - dendrites also contain Nissl's granules",
   "Statement II: false - the axon carries impulses away from the cell body"],
  "Neuron as Structural and Functional Unit of Neural System", ans="C",
  why="Statement II gives the dendrites' direction of conduction to the axon, so options calling it true are "
      "wrong; Statement I is NCERT's description of dendrites, so options calling it false are wrong.", secs=30)

Z(NCC, "Nervous system divisions", B, ASR,
  AR("The human brain is well protected.",
     "The brain is enclosed in the skull, and inside the skull it is covered by the cranial meninges."),
  "Protection of the brain",
  "NCERT: the human brain is well protected by the skull. Inside the skull, the brain is covered by cranial "
  "meninges consisting of an outer layer called dura mater, a very thin middle layer called arachnoid and an inner "
  "layer (which is in contact with the brain tissue) called pia mater. The skull and the meninges are the very "
  "structures that protect it, so R explains A.",
  ["A: true", "R: true - skull and cranial meninges", "R is the reason A holds"],
  "Central Neural System", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; R names the coverings that "
      "give the protection stated in A, so it is the correct explanation.", secs=25)

Z(NCC, "Nervous system divisions", I, MAT,
  ML(("function", "part of the brain mainly involved"),
     ["Control of body temperature and of the urge for eating and drinking",
      "Control of gastric secretions",
      "Fibre tracts that interconnect different regions of the brain",
      "Regulation of sexual behaviour and motivation, along with the hypothalamus"],
     ["Pons", "Limbic system", "Hypothalamus", "Medulla oblongata"]),
  "Localisation of brain functions",
  "NCERT: the hypothalamus contains a number of centres which control body temperature and the urge for eating "
  "and drinking. The medulla contains centres which control respiration, cardiovascular reflexes and gastric "
  "secretions. The pons consists of fibre tracts that interconnect different regions of the brain. The limbic "
  "system, along with the hypothalamus, is involved in the regulation of sexual behaviour, expression of emotional "
  "reactions and motivation.",
  ["A -> hypothalamus (III)", "B -> medulla oblongata (IV)", "C -> pons (I)", "D -> limbic system (II)"],
  "Central Neural System",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="Giving temperature control to the medulla and gastric secretions to the hypothalamus reverses them; the pons, "
      "not the medulla, consists of interconnecting fibre tracts; and sexual behaviour and motivation are limbic "
      "functions, while temperature and the urge for eating and drinking are hypothalamic centres.", secs=50)

Z(NCC, "Neuron and nerves", I, MUL,
  MS("Which of the following statements correctly describe the axon of a neuron, as given in NCERT?",
     ["It is a long fibre whose distal end is branched.",
      "Each of its branches terminates as a bulb-like structure called the synaptic knob.",
      "It transmits nerve impulses towards the cell body.",
      "Axons are of two types, myelinated and non-myelinated.",
      "It transmits nerve impulses to a synapse or to a neuromuscular junction."]),
  "Structure and role of the axon",
  "NCERT: the axon is a long fibre, the distal end of which is branched. Each branch terminates as a bulb-like "
  "structure called the synaptic knob, which possesses synaptic vesicles containing neurotransmitters. Axons "
  "transmit nerve impulses away from the cell body to a synapse or to a neuromuscular junction. There are two "
  "types of axons, namely myelinated and non-myelinated. Conduction towards the cell body is the role of the "
  "dendrites.",
  ["(a) true", "(b) true", "(c) false - that is the dendrites", "(d) true", "(e) true"],
  "Neuron as Structural and Functional Unit of Neural System",
  at="D", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b) and (c) only", "(a), (b), (c), (d) and (e)", "(b), (d) and (e) only"],
  why="(c) describes dendrites, so every option containing (c) is wrong; '(b), (d) and (e) only' leaves out (a), "
      "NCERT's description of the axon as a long fibre with a branched distal end.", secs=50)

Z(NCC, "Nervous system divisions", I, D,
  "According to NCERT, which of the following is among the functions controlled by the human brain?",
  "Functions of the brain",
  "NCERT lists that the brain controls the voluntary movements, balance of the body, functioning of vital "
  "involuntary organs (e.g. lungs, heart, kidneys, etc.), thermoregulation, hunger and thirst, circadian (24-hour) "
  "rhythms of our body, activities of several endocrine glands and human behaviour. It is also the site for "
  "processing of vision, hearing, speech, memory, intelligence, emotions and thoughts.",
  ["Brain = 'command and control system'", "Controls voluntary AND vital involuntary organs (lungs, heart, kidneys)"],
  "Central Neural System",
  at="B", correct="The functioning of vital involuntary organs such as the lungs, heart and kidneys",
  wrong=["Only voluntary movements; involuntary organs are controlled by the spinal cord alone",
         "Only the processing of vision and hearing; memory and emotions are handled by the PNS",
         "Only the activities of endocrine glands, not human behaviour"],
  why="NCERT names both voluntary movements and the functioning of vital involuntary organs as brain functions, "
      "puts memory and emotions among processes of the brain (the PNS carries impulses, it does not process them), "
      "and lists human behaviour as well as endocrine activity.", secs=35)

Z(NCC, "Nerve impulse generation and conduction", I, ASR,
  AR("Within a fraction of a second after a site on an axon is stimulated, the resting potential is restored at "
     "that site.",
     "The rise in Na⁺ permeability at the site is extremely short-lived and is quickly followed by a rise in "
     "permeability to K⁺, so that K⁺ diffuses to the outside of the membrane."),
  "Restoring the resting potential",
  "NCERT: the rise in the stimulus-induced permeability to Na⁺ is extremely short-lived. It is quickly followed by "
  "a rise in permeability to K⁺. Within a fraction of a second, K⁺ diffuses outside the membrane and restores "
  "the resting potential of the membrane at the site of excitation, and the fibre becomes once more responsive to "
  "further stimulation. The events in R are what restore the resting potential, so R explains A.",
  ["A: true", "R: true", "Short-lived Na⁺ rise + K⁺ outflow -> resting potential restored"],
  "Generation and Conduction of Nerve Impulse", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; NCERT presents the outward "
      "diffusion of K⁺ after the brief Na⁺ rise as the process that restores the resting potential, so R "
      "explains A.", secs=40)

Z(NCC, "Nervous system divisions", I, STP,
  SP("The cerebral hemispheres are connected by a tract of nerve fibres called the corpus callosum, and the "
     "cerebrum wraps around the thalamus.",
     "The midbrain is located between the thalamus/hypothalamus of the forebrain and the medulla oblongata, with "
     "no other part of the hindbrain in between."),
  "Position of brain parts",
  "NCERT: the cerebral hemispheres are connected by a tract of nerve fibres called the corpus callosum, and the "
  "cerebrum wraps around a structure called the thalamus. The midbrain is located between the thalamus/"
  "hypothalamus of the forebrain and the pons of the hindbrain; the medulla lies below the pons and is connected "
  "to the spinal cord.",
  ["Statement I: true", "Statement II: false - the midbrain borders the pons, not the medulla directly"],
  "Central Neural System", ans="C",
  why="Statement II replaces the pons with the medulla oblongata, so options calling it true are wrong; Statement "
      "I is NCERT's description of the cerebrum.", secs=40)

Z(NCC, "Nerve impulse generation and conduction", I, D,
  "At a chemical synapse, neurotransmitters bind to their specific receptors on the post-synaptic membrane. What, "
  "according to NCERT, is the immediate result of this binding?",
  "Post-synaptic events",
  "NCERT: the released neurotransmitters bind to their specific receptors present on the post-synaptic membrane. "
  "This binding opens ion channels, allowing the entry of ions which can generate a new potential in the "
  "post-synaptic neuron. The new potential developed may be either excitatory or inhibitory.",
  ["Binding to receptors -> ion channels open", "Ions enter -> new potential (excitatory or inhibitory)"],
  "Transmission of Impulses",
  at="D", correct="Ion channels open, allowing entry of ions that can generate a new potential in the "
                  "post-synaptic neuron",
  wrong=["Synaptic vesicles of the post-synaptic neuron fuse with its membrane",
         "Electrical current flows directly from the pre-synaptic into the post-synaptic neuron",
         "The post-synaptic membrane becomes permanently impermeable to all ions"],
  why="Synaptic vesicles are in the pre-synaptic knob, not the post-synaptic neuron; direct current flow happens "
      "at electrical synapses, which have no neurotransmitters; and the binding opens channels rather than closing "
      "the membrane to all ions.", secs=35)

Z(NCC, "Nerve impulse generation and conduction", A, MUL,
  MS("An axon is at rest. Which of the following are TRUE of it, according to NCERT?",
     ["The axonal membrane is nearly impermeable to Na⁺.",
      "The axonal membrane is impermeable to the negatively charged proteins present in the axoplasm.",
      "The outer surface of the axonal membrane is negatively charged.",
      "The concentration of K⁺ is higher in the axoplasm than in the fluid outside.",
      "The membrane is in a depolarised state."]),
  "The resting axonal membrane",
  "NCERT: when a neuron is not conducting any impulse, i.e. resting, the axonal membrane is comparatively more "
  "permeable to K⁺ and nearly impermeable to Na⁺; it is also impermeable to the negatively charged proteins "
  "present in the axoplasm. The axoplasm contains a high concentration of K⁺ and negatively charged proteins and a "
  "low concentration of Na⁺. The outer surface carries a positive charge and the inner surface a negative charge, "
  "so the membrane is POLARISED; a depolarised membrane is found only at a stimulated site.",
  ["(a) true", "(b) true", "(c) false - outer surface positive", "(d) true", "(e) false - polarised, not "
   "depolarised"],
  "Generation and Conduction of Nerve Impulse",
  at="A", correct="(a), (b) and (d) only",
  wrong=["(a), (c) and (e) only", "(a), (b), (d) and (e) only", "(b), (c) and (d) only"],
  why="(c) reverses the resting charges and (e) describes a stimulated site, so options with either are wrong; "
      "the remaining statements (a), (b) and (d) are all NCERT facts about the resting state.", secs=60)

Z(NCC, "Neuron and nerves", A, MAT,
  ML(("feature", "neural structure"),
     ["Has one axon and one dendrite",
      "Gap between two adjacent myelin sheaths",
      "Enclosed by a Schwann cell that does not form a myelin sheath around the axon",
      "Granular bodies present in the cell body and dendrites"],
     ["Unmyelinated nerve fibre", "Nissl's granules", "Bipolar neuron", "Node of Ranvier"]),
  "Neuron and nerve-fibre features",
  "NCERT: bipolar neurons have one axon and one dendrite (found in the retina). In myelinated fibres, the gaps "
  "between two adjacent myelin sheaths are called nodes of Ranvier. An unmyelinated nerve fibre is enclosed by a "
  "Schwann cell that does not form a myelin sheath around the axon. Nissl's granules are certain granular bodies "
  "in the cytoplasm of the cell body, also present in the dendrites.",
  ["A -> bipolar neuron (III)", "B -> node of Ranvier (IV)", "C -> unmyelinated fibre (I)",
   "D -> Nissl's granules (II)"],
  "Neuron as Structural and Functional Unit of Neural System",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="A node of Ranvier is a gap between myelin sheaths, not a fibre wrapped by a non-myelinating Schwann cell; "
      "Nissl's granules are granular bodies, not a type of neuron; and a bipolar neuron is a neuron, not an "
      "unmyelinated fibre.", secs=50)

Z(NCC, "Nerve impulse generation and conduction", A, ASR,
  AR("An electrical synapse can transmit an impulse even though no neurotransmitter is released across it.",
     "At an electrical synapse, the pre- and post-synaptic membranes are separated by a fluid-filled synaptic "
     "cleft."),
  "Electrical versus chemical synapse",
  "NCERT: at electrical synapses, the membranes of pre- and post-synaptic neurons are in very close proximity, and "
  "electrical current can flow directly from one neuron into the other across these synapses. Neurotransmitters "
  "are involved only at chemical synapses, where the membranes are separated by a fluid-filled space called the "
  "synaptic cleft. A is true; R wrongly gives the electrical synapse the cleft of a chemical synapse.",
  ["A: true - current flows directly", "R: false - the synaptic cleft belongs to a chemical synapse"],
  "Transmission of Impulses", ans="C",
  why="R is false, so options treating both statements as true are wrong; A is true because current passes "
      "directly between the closely apposed membranes, so 'A is false' is wrong.", secs=40)

Z(NCC, "Nervous system divisions", A, D,
  "How many of the following structures of the human brain belong to the MIDBRAIN or the HINDBRAIN (i.e. not "
  "to the forebrain)?\n\nCerebrum, thalamus, corpora quadrigemina, pons, hypothalamus, cerebral aqueduct, "
  "cerebellum, hippocampus",
  "Divisions of the brain",
  "NCERT: the forebrain consists of the cerebrum, thalamus and hypothalamus; the hippocampus is one of the deep "
  "structures that, with the inner parts of the cerebral hemispheres, form the limbic system of the forebrain. "
  "The midbrain has the cerebral aqueduct passing through it and the corpora quadrigemina on its dorsal side. The "
  "hindbrain comprises the pons, cerebellum and medulla oblongata.",
  ["Forebrain: cerebrum, thalamus, hypothalamus, hippocampus (4)",
   "Midbrain: corpora quadrigemina, cerebral aqueduct (2)", "Hindbrain: pons, cerebellum (2)",
   "Midbrain + hindbrain = 4"],
  "Central Neural System",
  at="B", correct="Four",
  wrong=["Three", "Five", "Six"],
  why="Three misses one of the four (usually the cerebral aqueduct, which is a canal in the midbrain); five counts "
      "the hippocampus or the hypothalamus outside the forebrain; six also puts the thalamus outside it.",
  secs=60)
