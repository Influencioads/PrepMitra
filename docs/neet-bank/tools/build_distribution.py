"""Builds the PrepMitra NEET (UG) question-bank plan from one taxonomy.

Writes taxonomy.json (subject -> topic -> subtopics, with exact target counts per difficulty) and
02_SYLLABUS_AND_DISTRIBUTION.md. Counts use the largest-remainder method so every subject total and every difficulty
total is exact (10,000 = 3,000 Basic + 4,000 Intermediate + 3,000 Advanced; 2,500 per paper section).

Topics and subtopics follow the NMC "Syllabus for NEET (UG)-2026" (public notice of 22 Dec 2025) unit by unit; nothing
outside it is planned. Biology is split into Botany and Zoology the way the printed NEET paper splits its 90 Biology
questions (45 + 45), following the NCERT chapter each topic comes from.

Topic weights are relative frequencies ESTIMATED from unit size and how often a unit has carried questions in past
papers. They are a plan, not a measurement; change a weight and re-run.

    python docs/neet-bank/tools/build_distribution.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIFFS = {"Basic": 30, "Intermediate": 40, "Advanced": 30}

# subject -> (id prefix, section key, target, [(topic, NMC unit, weight, [subtopics])])
TAXONOMY = {
    "Physics": ("PHY", "physics", 2500, [
        ("Physics and Measurement", "Physics 1", 2, ["Units and SI system", "Least count and significant figures",
                                                     "Errors in measurement", "Dimensional analysis"]),
        ("Kinematics", "Physics 2", 4, ["Motion in a straight line", "Graphs of motion", "Vectors",
                                        "Relative velocity", "Projectile motion", "Uniform circular motion"]),
        ("Laws of Motion", "Physics 3", 4, ["Newton's laws and impulse", "Conservation of linear momentum",
                                            "Equilibrium of concurrent forces", "Friction",
                                            "Circular motion: level and banked roads"]),
        ("Work, Energy and Power", "Physics 4", 3.5, ["Work by constant and variable force", "Work-energy theorem",
                                                      "Power", "Spring potential energy", "Motion in a vertical circle",
                                                      "Collisions"]),
        ("Rotational Motion", "Physics 5", 4, ["Centre of mass", "Torque and angular momentum",
                                               "Moment of inertia and axis theorems", "Rigid-body rotation",
                                               "Equilibrium of rigid bodies"]),
        ("Gravitation", "Physics 6", 3, ["Law of gravitation", "Variation of g", "Kepler's laws",
                                         "Gravitational potential and energy", "Escape and orbital velocity",
                                         "Satellite energy and period"]),
        ("Properties of Solids and Liquids", "Physics 7", 5, ["Elasticity and moduli", "Fluid pressure and Pascal's law",
                                                              "Viscosity and Stokes' law", "Bernoulli's principle",
                                                              "Surface tension and capillarity",
                                                              "Thermal expansion and calorimetry", "Heat transfer"]),
        ("Thermodynamics", "Physics 8", 3, ["Zeroth and first law", "Isothermal and adiabatic processes",
                                            "Second law, reversible and irreversible processes"]),
        ("Kinetic Theory of Gases", "Physics 9", 2, ["Ideal gas equation", "Pressure and rms speed",
                                                     "Degrees of freedom and equipartition", "Mean free path"]),
        ("Oscillations and Waves", "Physics 10", 4.5, ["SHM equation and phase", "Spring and pendulum oscillations",
                                                       "Energy in SHM", "Progressive waves and wave speed",
                                                       "Superposition and standing waves", "Organ pipes and beats"]),
        ("Electrostatics", "Physics 11", 6, ["Coulomb's law and superposition", "Electric field and dipole",
                                             "Gauss's law", "Electric potential and energy",
                                             "Capacitors and dielectrics"]),
        ("Current Electricity", "Physics 12", 6, ["Drift velocity and Ohm's law", "Resistivity and temperature",
                                                  "Combination of resistors", "Cells, emf and internal resistance",
                                                  "Kirchhoff's laws", "Wheatstone and metre bridge"]),
        ("Magnetic Effects of Current and Magnetism", "Physics 13", 6, ["Biot-Savart law", "Ampere's law",
                                                                        "Force on charges and conductors",
                                                                        "Torque on loop and galvanometer",
                                                                        "Magnetic dipole and bar magnet",
                                                                        "Magnetic materials"]),
        ("Electromagnetic Induction and Alternating Currents", "Physics 14", 4.5, [
            "Faraday's and Lenz's laws", "Self and mutual inductance", "AC: rms, reactance and impedance",
            "LCR resonance and power", "AC generator and transformer"]),
        ("Electromagnetic Waves", "Physics 15", 1.5, ["Displacement current", "EM wave properties",
                                                      "EM spectrum and uses"]),
        ("Optics", "Physics 16", 7, ["Mirrors", "Refraction and lenses", "Total internal reflection", "Prism",
                                     "Optical instruments", "Huygens' principle and interference",
                                     "Diffraction", "Polarisation"]),
        ("Dual Nature of Matter and Radiation", "Physics 17", 3, ["Photoelectric effect", "Einstein's equation",
                                                                  "de Broglie wavelength"]),
        ("Atoms and Nuclei", "Physics 18", 4, ["Rutherford scattering", "Bohr model and hydrogen spectrum",
                                               "Nuclear size and mass defect", "Binding energy", "Fission and fusion"]),
        ("Electronic Devices", "Physics 19", 4.5, ["Semiconductors", "p-n junction diode and rectifier",
                                                   "LED, photodiode and solar cell", "Zener diode", "Logic gates"]),
        ("Experimental Skills", "Physics 20", 2.5, ["Vernier calipers and screw gauge", "Mechanics experiments",
                                                    "Thermal and fluid experiments", "Electrical experiments",
                                                    "Optics experiments"]),
    ]),
    "Chemistry": ("CHE", "chemistry", 2500, [
        ("Some Basic Concepts in Chemistry", "Chemistry 1", 3, ["Laws of chemical combination", "Mole concept",
                                                                "Empirical and molecular formulae", "Stoichiometry"]),
        ("Atomic Structure", "Chemistry 2", 4, ["Bohr model and hydrogen spectrum", "Dual nature and uncertainty",
                                                "Quantum numbers and orbitals", "Electronic configuration"]),
        ("Chemical Bonding and Molecular Structure", "Chemistry 3", 6, ["Ionic bonding and lattice enthalpy",
                                                                        "Fajans' rule and dipole moment",
                                                                        "VSEPR shapes", "Hybridisation and resonance",
                                                                        "Molecular orbital theory",
                                                                        "Hydrogen and metallic bonding"]),
        ("Chemical Thermodynamics", "Chemistry 4", 4, ["First law, work and enthalpy", "Hess's law and enthalpies",
                                                       "Entropy and Gibbs energy", "Gibbs energy and K"]),
        ("Solutions", "Chemistry 5", 3.5, ["Concentration terms", "Raoult's law and ideal solutions",
                                           "Colligative properties", "van't Hoff factor"]),
        ("Equilibrium", "Chemistry 6", 5.5, ["Physical equilibria and Henry's law", "Kp, Kc and Le Chatelier",
                                             "Acids, bases and pH", "Hydrolysis and buffers", "Solubility product"]),
        ("Redox Reactions and Electrochemistry", "Chemistry 7", 4.5, ["Oxidation number and balancing",
                                                                      "Conductance and Kohlrausch's law",
                                                                      "Electrode potential and cells",
                                                                      "Nernst equation and Gibbs energy",
                                                                      "Batteries and fuel cells"]),
        ("Chemical Kinetics", "Chemistry 8", 3.5, ["Rate law and order", "Zero and first order reactions",
                                                   "Half-life", "Arrhenius equation and activation energy"]),
        ("Classification of Elements and Periodicity in Properties", "Chemistry 9", 3, [
            "Modern periodic table", "Atomic and ionic radii", "Ionisation and electron gain enthalpy",
            "Valence and reactivity"]),
        ("p-Block Elements", "Chemistry 10", 4, ["Group 13 and 14 trends", "Group 15 and 16 trends",
                                                 "Group 17 and 18 trends", "Anomalous first element"]),
        ("d- and f-Block Elements", "Chemistry 11", 4, ["Transition element trends", "Magnetic and colour properties",
                                                        "K2Cr2O7 and KMnO4", "Lanthanoids and actinoids"]),
        ("Coordination Compounds", "Chemistry 12", 5, ["Werner's theory and ligands", "IUPAC nomenclature",
                                                       "Isomerism", "Valence bond theory", "Crystal field theory",
                                                       "Applications"]),
        ("Purification and Characterisation of Organic Compounds", "Chemistry 13", 2, [
            "Purification methods", "Qualitative analysis", "Quantitative analysis and formulae"]),
        ("Some Basic Principles of Organic Chemistry", "Chemistry 14", 6, ["Hybridisation and functional groups",
                                                                           "IUPAC nomenclature", "Isomerism",
                                                                           "Reactive intermediates",
                                                                           "Electronic effects",
                                                                           "Types of organic reactions"]),
        ("Hydrocarbons", "Chemistry 15", 5, ["Alkanes and conformations", "Alkenes: addition and ozonolysis",
                                             "Alkynes", "Benzene and aromaticity", "Electrophilic substitution"]),
        ("Organic Compounds Containing Halogens", "Chemistry 16", 3.5, ["C-X bond and preparation",
                                                                        "SN1 and SN2", "Polyhalogen compounds"]),
        ("Organic Compounds Containing Oxygen", "Chemistry 17", 6, ["Alcohols", "Phenols", "Ethers",
                                                                    "Aldehydes and ketones", "Carboxylic acids"]),
        ("Organic Compounds Containing Nitrogen", "Chemistry 18", 3.5, ["Amines: basicity and identification",
                                                                        "Diazonium salts"]),
        ("Biomolecules (Chemistry)", "Chemistry 19", 3.5, ["Carbohydrates", "Amino acids and proteins", "Vitamins",
                                                           "Nucleic acids", "Hormones"]),
        ("Principles Related to Practical Chemistry", "Chemistry 20", 3, ["Detection of elements and functional groups",
                                                                          "Preparations", "Titrimetric analysis",
                                                                          "Qualitative salt analysis",
                                                                          "Thermochemistry and kinetics experiments"]),
    ]),
    "Botany": ("BOT", "botany", 2500, [
        ("The Living World and Classification", "Biology 1", 5, ["What is living", "Taxonomy and hierarchy",
                                                                 "Binomial nomenclature", "Five kingdom classification",
                                                                 "Monera, Protista and Fungi",
                                                                 "Lichens, viruses and viroids"]),
        ("Plant Kingdom", "Biology 1", 5, ["Algae", "Bryophytes", "Pteridophytes", "Gymnosperms"]),
        ("Morphology of Flowering Plants", "Biology 2", 5, ["Root, stem and leaf", "Inflorescence", "Flower",
                                                            "Fruit and seed", "Plant families"]),
        ("Anatomy of Flowering Plants", "Biology 2", 4, ["Plant tissues", "Tissue systems",
                                                         "Dicot and monocot anatomy"]),
        ("Cell: The Unit of Life", "Biology 3", 5, ["Cell theory", "Prokaryotic cell", "Cell envelope and membrane",
                                                    "Endomembrane system", "Mitochondria, plastids and ribosomes",
                                                    "Cytoskeleton, cilia and centrioles", "Nucleus"]),
        ("Cell Cycle and Cell Division", "Biology 3", 4, ["Cell cycle phases", "Mitosis", "Meiosis",
                                                          "Significance"]),
        ("Photosynthesis", "Biology 4", 4.5, ["Site and pigments", "Light reactions and photophosphorylation",
                                              "Chemiosmosis", "Calvin cycle and C4 pathway", "Photorespiration",
                                              "Limiting factors"]),
        ("Respiration in Plants", "Biology 4", 3.5, ["Glycolysis and fermentation", "TCA cycle",
                                                     "Electron transport system", "ATP yield and amphibolic pathway",
                                                     "Respiratory quotient"]),
        ("Plant Growth and Development", "Biology 4", 3.5, ["Germination and growth phases", "Growth rate",
                                                            "Differentiation and redifferentiation",
                                                            "Plant growth regulators"]),
        ("Sexual Reproduction in Flowering Plants", "Biology 6", 6, ["Microsporogenesis and male gametophyte",
                                                                     "Megasporogenesis and embryo sac", "Pollination",
                                                                     "Outbreeding devices and pollen-pistil interaction",
                                                                     "Double fertilisation", "Endosperm and embryo",
                                                                     "Apomixis, parthenocarpy and polyembryony"]),
        ("Principles of Inheritance and Variation", "Biology 7", 7, ["Mendelian inheritance",
                                                                     "Incomplete and co-dominance",
                                                                     "Multiple alleles and pleiotropy",
                                                                     "Polygenic inheritance", "Linkage and crossing over",
                                                                     "Sex determination", "Sex-linked inheritance",
                                                                     "Mendelian and chromosomal disorders"]),
        ("Molecular Basis of Inheritance", "Biology 7", 7, ["DNA as genetic material", "DNA and RNA structure",
                                                            "DNA packaging", "Replication", "Transcription",
                                                            "Genetic code and translation", "Lac operon",
                                                            "Human genome project and DNA fingerprinting"]),
        ("Microbes in Human Welfare", "Biology 8", 2.5, ["Household and industrial products", "Sewage treatment",
                                                         "Biogas", "Biocontrol agents and biofertilisers"]),
        ("Organisms and Populations", "Biology 10", 4, ["Population attributes", "Population growth",
                                                        "Population interactions"]),
        ("Ecosystem", "Biology 10", 3.5, ["Structure and components", "Productivity and decomposition",
                                          "Energy flow", "Ecological pyramids"]),
        ("Biodiversity and Conservation", "Biology 10", 3.5, ["Patterns of biodiversity", "Importance and loss",
                                                              "Hotspots and Red Data Book",
                                                              "In situ and ex situ conservation"]),
    ]),
    "Zoology": ("ZOO", "zoology", 2500, [
        ("Animal Kingdom", "Biology 1", 5.5, ["Basis of classification", "Non-chordate phyla", "Chordate classes"]),
        ("Structural Organisation in Animals", "Biology 2", 4, ["Animal tissues", "Frog: morphology and anatomy"]),
        ("Biomolecules", "Biology 3", 5, ["Proteins and amino acids", "Carbohydrates and lipids", "Nucleic acids",
                                          "Enzymes: properties and action", "Enzyme classification"]),
        ("Breathing and Exchange of Gases", "Biology 5", 3.5, ["Respiratory system", "Mechanism of breathing",
                                                               "Respiratory volumes", "Exchange and transport of gases",
                                                               "Regulation and disorders"]),
        ("Body Fluids and Circulation", "Biology 5", 4.5, ["Blood and blood groups", "Coagulation and lymph",
                                                           "Human heart", "Cardiac cycle and ECG",
                                                           "Double circulation and regulation",
                                                           "Circulatory disorders"]),
        ("Excretory Products and their Elimination", "Biology 5", 4, ["Modes of excretion", "Nephron structure",
                                                                      "Urine formation", "Regulation of kidney function",
                                                                      "Disorders and dialysis"]),
        ("Locomotion and Movement", "Biology 5", 4, ["Types of movement", "Muscle contraction", "Skeletal system",
                                                     "Joints", "Muscular and skeletal disorders"]),
        ("Neural Control and Coordination", "Biology 5", 3.5, ["Neuron and nerves", "Nervous system divisions",
                                                               "Nerve impulse generation and conduction"]),
        ("Chemical Coordination and Integration", "Biology 5", 4.5, ["Hypothalamus and pituitary",
                                                                     "Thyroid, parathyroid and pineal",
                                                                     "Adrenal, pancreas and gonads",
                                                                     "Mechanism of hormone action",
                                                                     "Hormonal disorders"]),
        ("Human Reproduction", "Biology 6", 6, ["Male and female reproductive systems", "Gametogenesis",
                                                "Menstrual cycle", "Fertilisation and implantation",
                                                "Pregnancy, parturition and lactation"]),
        ("Reproductive Health", "Biology 6", 4, ["STDs and their prevention", "Contraception", "MTP and amniocentesis",
                                                 "Infertility and ART"]),
        ("Evolution", "Biology 7", 5, ["Origin of life", "Evidences of evolution", "Darwinism and modern synthesis",
                                       "Natural selection", "Gene flow, drift and Hardy-Weinberg",
                                       "Adaptive radiation", "Human evolution"]),
        ("Human Health and Disease", "Biology 8", 6, ["Pathogens and diseases", "Immunity and vaccines", "Cancer",
                                                      "HIV and AIDS", "Drug and alcohol abuse"]),
        ("Biotechnology: Principles and Processes", "Biology 9", 5, ["Restriction enzymes", "Cloning vectors",
                                                                     "Competent hosts and transformation",
                                                                     "PCR and gel electrophoresis",
                                                                     "Bioreactors and downstream processing"]),
        ("Biotechnology and its Applications", "Biology 9", 4.5, ["Bt crops and RNAi", "Human insulin",
                                                                  "Gene therapy", "Transgenic animals",
                                                                  "Biosafety, biopiracy and patents"]),
    ]),
}

# NCERT content that the NMC 2026 syllabus does NOT list. Do not write questions on these.
EXCLUDED = {
    "Physics": ["Communication systems", "Earth's magnetism and magnetic elements"],
    "Chemistry": ["States of matter (gas laws as a chapter)", "s-Block elements", "Hydrogen", "Metallurgy",
                  "Surface chemistry (except preparing sols, a listed experiment)", "Polymers",
                  "Chemistry in everyday life", "Environmental chemistry", "Solid state"],
    "Botany": ["Transport in plants", "Mineral nutrition", "Strategies for enhancement in food production",
               "Environmental issues", "Nutrient cycling", "Ecological succession"],
    "Zoology": ["Digestion and absorption", "Sense organs and reflex action", "Animal husbandry and plant breeding"],
}


def largest_remainder(total: int, weights: dict) -> dict:
    s = sum(weights.values())
    raw = {k: total * w / s for k, w in weights.items()}
    out = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[: total - sum(out.values())]:
        out[k] += 1
    return out


def build() -> dict:
    total = sum(t[2] for t in TAXONOMY.values())
    by_diff = largest_remainder(total, DIFFS)
    subjects = []
    for name, (prefix, section, target, topics) in TAXONOMY.items():
        sdiff = largest_remainder(target, DIFFS)
        counts = largest_remainder(target, {t[0]: t[2] for t in topics})
        # difficulty per topic: allocate each difficulty column over topics so column totals are exact
        cols = {d: largest_remainder(n, counts) for d, n in sdiff.items()}
        # fix row sums (a topic's three cells must add up to its count) by moving units between topics in a column
        for t in topics:
            row = sum(cols[d][t[0]] for d in DIFFS)
            assert abs(row - counts[t[0]]) <= 2, (t[0], row, counts[t[0]])
        rows = {t[0]: {d: cols[d][t[0]] for d in DIFFS} for t in topics}
        for topic, row in rows.items():
            counts[topic] = sum(row.values())
        assert sum(counts.values()) == target
        subjects.append({
            "subject": name, "id_prefix": f"NEET_{prefix}_", "section_key": section, "target": target,
            "by_difficulty": sdiff,
            "topics": [{"topic": t[0], "nmc_unit": t[1], "subtopics": t[3], "target": counts[t[0]],
                        "by_difficulty": rows[t[0]]} for t in topics],
            "not_in_syllabus": EXCLUDED[name],
        })
    assert sum(s["target"] for s in subjects) == total
    assert {d: sum(s["by_difficulty"][d] for s in subjects) for d in DIFFS} == by_diff
    return {"total": total, "by_difficulty": by_diff, "syllabus": "NMC Syllabus for NEET (UG)-2026", "subjects": subjects}


def markdown(tax: dict) -> str:
    lines = ["# NEET (UG) Syllabus and Distribution", "",
             "Generated by `tools/build_distribution.py` from the NMC *Syllabus for NEET (UG)-2026* (22 Dec 2025). "
             "Do not edit by hand.", "",
             f"**Total: {tax['total']:,}** = " + " / ".join(f"{n:,} {d}" for d, n in tax["by_difficulty"].items()) + ".",
             "", "Topic weights are planning estimates, not measured counts from past papers.", "",
             "| Subject | Paper section | Questions | Basic | Intermediate | Advanced |", "|---|---|---:|---:|---:|---:|"]
    for s in tax["subjects"]:
        d = s["by_difficulty"]
        lines.append(f"| {s['subject']} | `{s['section_key']}` | {s['target']:,} | {d['Basic']} | {d['Intermediate']} "
                     f"| {d['Advanced']} |")
    for s in tax["subjects"]:
        lines += ["", f"## {s['subject']} ({s['target']:,})", "",
                  "| Topic | NMC unit | Subtopics | Total | Basic | Inter. | Adv. |", "|---|---|---|---:|---:|---:|---:|"]
        for t in s["topics"]:
            d = t["by_difficulty"]
            lines.append(f"| {t['topic']} | {t['nmc_unit']} | {'; '.join(t['subtopics'])} | {t['target']} "
                         f"| {d['Basic']} | {d['Intermediate']} | {d['Advanced']} |")
        lines += ["", "**Not in the 2026 syllabus (no questions):** " + "; ".join(s["not_in_syllabus"]) + "."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    tax = build()
    (ROOT / "taxonomy.json").write_text(json.dumps(tax, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "02_SYLLABUS_AND_DISTRIBUTION.md").write_text(markdown(tax), encoding="utf-8")
    print({s["subject"]: s["target"] for s in tax["subjects"]}, tax["by_difficulty"])
