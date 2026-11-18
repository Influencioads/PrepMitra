
# ================================================================ Biotechnology: Principles and Processes (5/7/5)
Z(BPP, "Restriction enzymes", B, D,
  "According to NCERT, genetic engineering refers to:",
  "Meaning of genetic engineering",
  "NCERT: the two core techniques that enabled the birth of modern biotechnology are genetic engineering and "
  "bioprocess engineering. Genetic engineering: techniques to alter the chemistry of genetic material (DNA and RNA), "
  "to introduce these into host organisms and thus change the phenotype of the host organism.",
  ["Alter the chemistry of DNA/RNA", "Introduce it into a host organism", "-> change the host's phenotype"],
  "Principles of Biotechnology",
  at="B", correct="Techniques to alter the chemistry of genetic material (DNA and RNA), introduce it into host "
                  "organisms and thus change the phenotype of the host",
  wrong=["Maintenance of a sterile ambience to grow only the desired microbe on a large scale",
         "Separation and purification of a product before it is marketed",
         "Traditional hybridisation of plants and animals to combine desirable characters"],
  why="A sterile ambience for large-scale culture is bioprocess engineering; separation and purification is "
      "downstream processing; traditional hybridisation is what genetic engineering improves upon, since it often "
      "carries undesirable genes along with the desired ones.", secs=25)

Z(BPP, "Restriction enzymes", B, D,
  "In its account of the principles of biotechnology, NCERT contrasts asexual and sexual reproduction. Which "
  "statement gives this contrast correctly?",
  "Asexual versus sexual reproduction",
  "NCERT: you have learnt that asexual reproduction preserves the genetic information, while sexual reproduction "
  "permits variation. Traditional hybridisation procedures used in plant and animal breeding very often lead to "
  "inclusion and multiplication of undesirable genes along with the desired genes; genetic engineering allows only "
  "the desired genes to be introduced.",
  ["Asexual reproduction -> preserves genetic information", "Sexual reproduction -> permits variation"],
  "Principles of Biotechnology",
  at="A", correct="Asexual reproduction preserves the genetic information, while sexual reproduction permits "
                  "variation",
  wrong=["Asexual reproduction permits variation, while sexual reproduction preserves the genetic information",
         "Both asexual and sexual reproduction only preserve the genetic information",
         "Both asexual and sexual reproduction always introduce undesirable genes"],
  why="The second option reverses NCERT's contrast; sexual reproduction permits variation, so it does not only "
      "preserve information; and the inclusion of undesirable genes is NCERT's criticism of traditional "
      "hybridisation, not a property of all reproduction.", secs=25)

Z(BPP, "Bioreactors and downstream processing", B, STP,
  SP("The cells harbouring cloned genes of interest may be grown on a small scale in the laboratory.",
     "Such cultures may be used for extracting the desired protein and then purifying it by using different "
     "separation techniques."),
  "Obtaining the foreign gene product",
  "NCERT: the cells harbouring cloned genes of interest may be grown on a small scale in the laboratory. The "
  "cultures may be used for extracting the desired protein and then purifying it by using different separation "
  "techniques. The cells can also be multiplied in a continuous culture system or in bioreactors for large-scale "
  "production.",
  ["Statement I: true", "Statement II: true"],
  "Obtaining the Foreign Gene Product", ans="A",
  why="Both statements are NCERT's own, so every option calling either of them false is wrong.", secs=25)

Z(BPP, "PCR and gel electrophoresis", B, ASR,
  AR("During the isolation of DNA, the preparation is treated with ribonuclease.",
     "Purified DNA ultimately precipitates after the addition of chilled ethanol and can be seen as a collection "
     "of fine threads in the suspension."),
  "Steps in DNA isolation",
  "NCERT: when the cell is broken open, RNA is released along with DNA; RNA can be removed by treatment with "
  "ribonuclease, whereas proteins can be removed by treatment with protease. Other molecules can be removed by "
  "appropriate treatments, and purified DNA ultimately precipitates out after the addition of chilled ethanol. "
  "Both statements are true, but the precipitation by ethanol is a later step and is not why ribonuclease is used.",
  ["A: true - ribonuclease removes RNA", "R: true - chilled ethanol precipitates DNA",
   "R does not explain the use of ribonuclease"],
  "Isolation of the Genetic Material (DNA)", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; ribonuclease is used because "
      "RNA must be removed, which R does not say, so R is not the explanation.", secs=30)

Z(BPP, "Cloning vectors", B, D,
  "The E. coli cloning vector pBR322 shown in NCERT carries two genes that are used as selectable markers. These "
  "genes give resistance to:",
  "Selectable markers of pBR322",
  "NCERT: the figure of pBR322 shows the restriction sites, ori, and the antibiotic resistance genes ampR and tetR "
  "(resistance to ampicillin and tetracycline); rop codes for proteins involved in the replication of the plasmid. "
  "Foreign DNA ligated at the BamHI site of the tetracycline resistance gene, for example, inactivates that gene "
  "while ampicillin resistance remains.",
  ["pBR322 markers: ampR and tetR", "= ampicillin and tetracycline"],
  "Cloning Vectors",
  at="C", correct="Ampicillin and tetracycline",
  wrong=["Ampicillin and kanamycin", "Chloramphenicol and kanamycin", "Tetracycline and chloramphenicol"],
  why="Chloramphenicol and kanamycin are other antibiotics whose resistance genes NCERT calls useful selectable "
      "markers for E. coli in general, but pBR322 carries ampR and tetR.", secs=25)

Z(BPP, "Restriction enzymes", I, MAT,
  ML(("organism or body", "connection with biotechnology described in NCERT"),
     ["Escherichia coli RY 13", "Thermus aquaticus", "Agrobacterium tumefaciens",
      "European Federation of Biotechnology"],
     ["Source of the thermostable DNA polymerase used in PCR",
      "Strain from which the restriction enzyme EcoRI was isolated",
      "Gave a definition of biotechnology covering both traditional and modern molecular biotechnology",
      "Its T-DNA transforms normal plant cells into tumour cells"]),
  "Organisms and bodies in biotechnology",
  "NCERT: in EcoRI, the letters come from the genus Escherichia, species coli and strain RY 13. PCR uses a "
  "thermostable DNA polymerase isolated from the bacterium Thermus aquaticus. Agrobacterium tumefaciens delivers a "
  "piece of DNA known as T-DNA that transforms normal plant cells into tumour cells. The European Federation of "
  "Biotechnology (EFB) has given a definition of biotechnology that encompasses both traditional view and modern "
  "molecular biotechnology.",
  ["A -> II", "B -> I", "C -> IV", "D -> III"],
  "Principles of Biotechnology; Restriction Enzymes; Cloning Vectors; Amplification of Gene of Interest using PCR",
  at="D", match=({"A": "II", "B": "I", "C": "IV", "D": "III"},
                 [{"A": "I", "B": "II", "C": "IV", "D": "III"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="EcoRI, not the PCR polymerase, comes from E. coli RY 13; the T-DNA belongs to Agrobacterium, which did not "
      "define biotechnology; and Thermus aquaticus is the polymerase source, not a plant pathogen.", secs=45)

Z(BPP, "Cloning vectors", I, MUL,
  MS("Which of the following statements about alien DNA moved into a host organism are correct, according to "
     "NCERT?",
     ["In most cases, alien DNA moved into an organism would not be able to multiply in the progeny cells.",
      "When it gets integrated into the genome of the recipient, it may multiply and be inherited along with the "
      "host DNA.",
      "It can also be replicated if it is linked to an origin of replication (ori).",
      "The ori is also responsible for controlling the copy number of the linked DNA.",
      "Alien DNA always multiplies in the host on its own, without integration or an ori."]),
  "Maintaining alien DNA in a host",
  "NCERT: in a majority of cases, the alien piece of DNA would not be able to multiply itself in the progeny cells "
  "of the organism. But when it gets integrated into the genome of the recipient, it may multiply and be inherited "
  "along with the host DNA, because it has become part of a chromosome, which has the ability to replicate. The "
  "alien DNA is linked with the origin of replication, a sequence from where replication starts; the ori is also "
  "responsible for controlling the copy number of the linked DNA.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - needs integration or an ori"],
  "Principles of Biotechnology; Cloning Vectors",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(b), (c) and (e) only", "(a) and (e) only"],
  why="(e) contradicts NCERT's point that alien DNA usually cannot multiply by itself, so every option with (e) is "
      "wrong; (a)-(d) are all NCERT statements.", secs=45)

Z(BPP, "Competent hosts and transformation", I, D,
  "Which pairing of a vector and the kind of cell into which NCERT says it is used to deliver genes is correct?",
  "Vectors for plants and animals",
  "NCERT: Agrobacterium tumefaciens, a pathogen of several dicot plants, delivers T-DNA into plant cells; its Ti "
  "plasmid has been modified into a cloning vector which is no more pathogenic to the plants but is still able to "
  "deliver genes of our interest into a variety of plants. Similarly, retroviruses have been disarmed and are now "
  "used to deliver desirable genes into animal cells. pBR322 is an E. coli cloning vector.",
  ["Ti plasmid (disarmed) -> plant cells", "Retrovirus (disarmed) -> animal cells", "pBR322 -> E. coli"],
  "Cloning Vectors",
  at="A", correct="Disarmed retroviruses – animal cells; modified Ti plasmid – plant cells",
  wrong=["Disarmed retroviruses – plant cells; modified Ti plasmid – animal cells",
         "Disarmed retroviruses – bacterial cells; pBR322 – plant cells",
         "Modified Ti plasmid – fungal cells; bacteriophage – animal cells"],
  why="The second option swaps the two vectors; pBR322 is an E. coli vector and retroviruses are used for animal "
      "cells, not bacteria; and NCERT uses the Ti plasmid for plants, not fungi, with bacteriophages as vectors for "
      "bacteria.", secs=35)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("Each restriction endonuclease recognises a specific palindromic nucleotide sequence in the DNA.",
     "The more than 900 restriction enzymes known today, isolated from over 230 strains of bacteria, all recognise "
     "the same recognition sequence."),
  "Specificity of restriction enzymes",
  "NCERT: today we know more than 900 restriction enzymes that have been isolated from over 230 strains of bacteria, "
  "each of which recognises DIFFERENT recognition sequences. Every restriction endonuclease recognises a specific "
  "palindromic nucleotide sequence in the DNA. A is true; R is false.",
  ["A: true", "R: false - each recognises a different sequence"],
  "Restriction Enzymes", ans="C",
  why="R contradicts NCERT's statement that the enzymes recognise different sequences, so options treating R as "
      "true are wrong; A is NCERT's statement, so 'A is false' is wrong.", secs=30)

Z(BPP, "Cloning vectors", I, STP,
  SP("In pBR322, the rop gene codes for the proteins involved in the replication of the plasmid.",
     "In pBR322, the recognition site for PvuI lies within the tetracycline resistance gene."),
  "Map of pBR322",
  "NCERT (pBR322 figure): rop codes for the proteins involved in the replication of the plasmid. The PstI and PvuI "
  "sites lie in the ampicillin resistance gene (ampR), while the BamHI and SalI sites lie in the tetracycline "
  "resistance gene (tetR).",
  ["Statement I: true", "Statement II: false - PvuI site is in ampR"],
  "Cloning Vectors", ans="C",
  why="Statement II places the PvuI site in the wrong resistance gene, so options calling it true are wrong; "
      "Statement I is NCERT's description of rop, so options calling it false are wrong.", secs=35)

Z(BPP, "Bioreactors and downstream processing", I, ASR,
  AR("A stirred-tank bioreactor is usually cylindrical or has a curved base.",
     "This shape facilitates the mixing of the reactor contents."),
  "Shape of stirred-tank bioreactors",
  "NCERT: the most commonly used bioreactors are of the stirring type. A stirred-tank reactor is usually cylindrical "
  "or with a curved base to facilitate the mixing of the reactor contents; the stirrer facilitates even mixing and "
  "oxygen availability throughout the bioreactor. NCERT gives mixing as the purpose of the shape, so R explains A.",
  ["A: true", "R: true", "NCERT: shape is 'to facilitate the mixing' -> R explains A"],
  "Bioreactors", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; NCERT states the shape is "
      "meant to facilitate mixing, so R is the explanation.", secs=30)

Z(BPP, "Competent hosts and transformation", I, STP,
  SP("Agrobacterium tumefaciens is a pathogen of several monocot plants.",
     "In animals, retroviruses have the ability to transform cancerous cells back into normal cells."),
  "Natural gene-transfer agents",
  "NCERT: Agrobacterium tumefaciens is a pathogen of several DICOT plants; it delivers T-DNA that transforms normal "
  "plant cells into tumours. Retroviruses in animals have the ability to transform NORMAL cells into CANCEROUS "
  "cells. Both statements reverse NCERT's description.",
  ["Statement I: false - dicot plants", "Statement II: false - normal cells into cancerous cells"],
  "Cloning Vectors", ans="B",
  why="Statement I names the wrong plant group and Statement II reverses the direction of transformation, so every "
      "option calling either statement true is wrong.", secs=35)

Z(BPP, "Bioreactors and downstream processing", A, MUL,
  MS("Which of the following statements about the processing of a biotechnological product after biosynthesis are "
     "correct?",
     ["Separation and purification of the product are collectively referred to as downstream processing.",
      "The product has to be formulated with suitable preservatives.",
      "In the case of drugs, the formulation has to undergo thorough clinical trials.",
      "Strict quality control testing for each product is required.",
      "Downstream processing and quality control testing are the same for every product."]),
  "Downstream processing",
  "NCERT: after completion of the biosynthetic stage, the product has to be subjected through a series of processes "
  "before it is ready for marketing. The processes include separation and purification, collectively referred to "
  "as downstream processing. The product has to be formulated with suitable preservatives; such formulation has to "
  "undergo thorough clinical trials as in the case of drugs. Strict quality control testing for each product is "
  "also required. The downstream processing and quality control testing vary from product to product.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - vary from product to product"],
  "Downstream Processing",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (e) only", "(c), (d) and (e) only"],
  why="(e) contradicts NCERT, which says these steps vary from product to product, so every option with (e) is "
      "wrong; (a)-(d) are all NCERT statements.", secs=45)

Z(BPP, "PCR and gel electrophoresis", A, D,
  "During the isolation of DNA, how many of the following are used to BREAK OPEN the cells (rather than for a later "
  "step)?\n\nLysozyme, ribonuclease, cellulase, protease, chitinase, chilled ethanol",
  "Breaking open cells to release DNA",
  "NCERT: to obtain DNA free from other macromolecules, the cells are broken open by treating bacterial cells, "
  "plant cells or fungal cells with enzymes such as lysozyme (bacteria), cellulase (plant cells) and chitinase "
  "(fungus). RNA is then removed by ribonuclease and proteins by protease, and purified DNA precipitates on "
  "addition of chilled ethanol.",
  ["Break open cells: lysozyme, cellulase, chitinase = 3",
   "Later steps: ribonuclease (RNA), protease (proteins), chilled ethanol (precipitation)"],
  "Isolation of the Genetic Material (DNA)",
  at="B", correct="Three",
  wrong=["Two", "Four", "Five"],
  why="Two leaves out one of the three cell-wall-degrading enzymes (often chitinase for fungi); four or five add "
      "ribonuclease, protease or chilled ethanol, which act after the cells have been opened.", secs=40)

Z(BPP, "Cloning vectors", A, ASR,
  AR("Selecting recombinants by the insertional inactivation of β-galactosidase is less cumbersome than selecting "
     "them by the inactivation of an antibiotic resistance gene.",
     "In this method, colonies that carry the recombinant DNA give a blue colour with the chromogenic substrate."),
  "Insertional inactivation of β-galactosidase",
  "NCERT: selection of recombinants due to inactivation of antibiotics is a cumbersome procedure because it requires "
  "simultaneous plating on two plates having different antibiotics; alternative markers differentiate recombinants "
  "on the basis of their ability to produce colour in the presence of a chromogenic substrate. Presence of a "
  "chromogenic substrate gives blue coloured colonies if the plasmid in the bacteria does NOT have an insert; "
  "presence of an insert results in insertional inactivation of β-galactosidase, and the colonies do not produce "
  "any colour. So A is true and R is false.",
  ["A: true - one plate, colour-based", "R: false - recombinants give no colour; non-recombinants are blue"],
  "Cloning Vectors", ans="C",
  why="R reverses which colonies turn blue, so options treating R as true are wrong; A is NCERT's comparison of the "
      "two selection methods, so 'A is false' is wrong.", secs=40)

Z(BPP, "Cloning vectors", A, STP,
  SP("The first recombinant DNA was constructed by linking a gene encoding antibiotic resistance with a native "
     "plasmid of Escherichia coli.",
     "Plasmid DNA acts as a vector to transfer the piece of DNA attached to it into the host organism."),
  "The first recombinant DNA",
  "NCERT: the construction of the first recombinant DNA emerged from the possibility of linking a gene encoding "
  "antibiotic resistance with a native plasmid (autonomously replicating circular extra-chromosomal DNA) of "
  "Salmonella typhimurium. Stanley Cohen and Herbert Boyer accomplished this in 1972. Plasmid DNA acts as a vector "
  "to transfer the piece of DNA attached to it into the host organism.",
  ["Statement I: false - native plasmid of Salmonella typhimurium", "Statement II: true"],
  "Principles of Biotechnology", ans="D",
  why="Statement I replaces Salmonella typhimurium with E. coli, so options calling it true are wrong; Statement II "
      "is NCERT's description of plasmid vectors, so options calling it false are wrong.", secs=40)

Z(BPP, "Competent hosts and transformation", A, MAT,
  ML(("term", "meaning, as used in NCERT"),
     ["Recombinant protein", "Competent host", "Elution", "Spooling"],
     ["Removing the fine threads of precipitated DNA from the suspension",
      "Extraction of DNA from the piece of gel cut out with its band",
      "Protein made when a protein-encoding gene is expressed in a heterologous host",
      "A bacterial cell made capable of taking up DNA, for example by treatment with a divalent cation"]),
  "Terms of recombinant DNA work",
  "NCERT: if any protein-encoding gene is expressed in a heterologous host, it is called a recombinant protein. "
  "Bacterial cells are made 'competent' to take up DNA by treating them with a specific concentration of a "
  "divalent cation, such as calcium. Separated DNA bands are cut out from the agarose gel and extracted from the "
  "gel piece; this step is known as elution. Purified DNA precipitating after chilled ethanol can be removed by "
  "spooling.",
  ["A -> III", "B -> IV", "C -> II", "D -> I"],
  "Isolation of the Genetic Material (DNA); Separation and Isolation of DNA Fragments; Insertion of Recombinant DNA "
  "into the Host Cell/Organism; Obtaining the Foreign Gene Product",
  at="A", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="A competent host is a cell able to take up DNA, not the protein it makes; elution extracts DNA from the gel, "
      "whereas spooling removes DNA threads from the ethanol suspension, so swapping C and D is wrong; elution is "
      "not a way of making cells competent.", secs=45)
