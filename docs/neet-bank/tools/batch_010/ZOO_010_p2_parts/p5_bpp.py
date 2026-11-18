

# ================================================================ Biotechnology: Principles and Processes (6/8/6)
HIND_II_YEAR = 1963 + 5
assert HIND_II_YEAR == 1968
Z(BPP, "Restriction enzymes", B, NUM,
  "In 1963, two enzymes responsible for restricting the growth of bacteriophage in Escherichia coli were isolated. "
  "According to NCERT, the first restriction endonuclease whose functioning depended on a specific DNA nucleotide "
  "sequence, Hind II, was isolated and characterised five years later. In which year was this?",
  "History of restriction enzymes",
  "NCERT: in the year 1963, the two enzymes responsible for restricting the growth of bacteriophage in E. coli were "
  "isolated - one added methyl groups to DNA, the other cut DNA (restriction endonuclease). The first restriction "
  "endonuclease, Hind II, whose functioning depended on a specific DNA nucleotide sequence, was isolated and "
  "characterised five years later.",
  ["1963 + 5 = 1968"],
  "Tools of Recombinant DNA Technology",
  at="A", correct="1968",
  wrong=["1958", "1972", "1963"],
  why="1958 subtracts the five years instead of adding them; 1972 is the year Cohen and Boyer made the first "
      "recombinant DNA; 1963 is the year of the first two restriction-related enzymes.", secs=20, vb=RECOMPUTED)

Z(BPP, "PCR and gel electrophoresis", B, ASR,
  AR("A thermostable DNA polymerase is used in the polymerase chain reaction (PCR).",
     "This thermostable DNA polymerase is isolated from the bacterium Thermus aquaticus."),
  "Thermostable DNA polymerase: use and source",
  "NCERT: the repeated amplification in PCR is achieved by the use of a thermostable DNA polymerase (isolated from a "
  "bacterium, Thermus aquaticus), which remains active during the high temperature induced denaturation of "
  "double-stranded DNA. Both statements are true, but the name of the bacterium the enzyme comes from does not "
  "explain why a thermostable enzyme is needed; the reason is that it must stay active at the high temperature used "
  "for denaturation.",
  ["A: true", "R: true", "R gives the source, not the reason (stability at denaturation temperature)"],
  "Processes of Recombinant DNA Technology", ans="B",
  why="The source organism is not the reason for using a heat-stable enzyme, so 'R is the correct explanation' is "
      "wrong; both are NCERT statements, so options calling either false are wrong.", secs=30)

Z(BPP, "PCR and gel electrophoresis", B, STP,
  SP("During the isolation of DNA from a fungus, the cells are broken open by treating them with chitinase.",
     "During the isolation of DNA from bacteria, the cells are broken open by treating them with cellulase."),
  "Enzymes used to break open cells",
  "NCERT: DNA is enclosed within membranes, so the cell has to be broken open to release DNA along with other "
  "macromolecules. This is done by treating the bacterial cells, plant cells or fungus with enzymes such as "
  "lysozyme (bacteria), cellulase (plant cells) and chitinase (fungus).",
  ["Fungus -> chitinase: Statement I true", "Bacteria -> lysozyme (cellulase is for plant cells): Statement II false"],
  "Processes of Recombinant DNA Technology", ans="C",
  why="Statement II names the plant-cell enzyme for bacteria (lysozyme is used), so options calling it true are "
      "wrong; Statement I is correct, so 'both false' and 'Statement I false' are wrong.", secs=25)

Z(BPP, "Cloning vectors", B, D,
  "The plasmid of Agrobacterium tumefaciens that has been modified into a cloning vector is called the Ti plasmid. "
  "According to NCERT, 'Ti' stands for:",
  "Ti plasmid",
  "NCERT: the tumor inducing (Ti) plasmid of Agrobacterium tumefaciens has now been modified into a cloning vector "
  "which is no more pathogenic to the plants but is still able to use the mechanisms to deliver genes of our "
  "interest into a variety of plants. Agrobacterium is a pathogen of several dicot plants and delivers T-DNA that "
  "transforms normal plant cells into tumour cells.",
  ["Ti = tumour (tumor) inducing"],
  "Tools of Recombinant DNA Technology",
  at="D", correct="Tumour inducing",
  wrong=["Tetracycline inactivating", "Transfer initiating", "Thermus-isolated"],
  why="Tetracycline resistance is a pBR322 marker, not the meaning of 'Ti'; 'transfer initiating' and "
      "'Thermus-isolated' are not NCERT terms.", secs=20)

Z(BPP, "Cloning vectors", B, D,
  "According to NCERT, scientists learnt how to deliver genes to transform eukaryotic cells (and force them to do "
  "what is wanted) from:",
  "Lessons from pathogens for gene delivery",
  "NCERT: we have learnt a lesson or two from bacteria and viruses, which have known for ages how to deliver genes "
  "to transform eukaryotic cells and force them to do what the bacteria or viruses want. Agrobacterium "
  "tumefaciens delivers T-DNA into dicot plant cells, and retroviruses can transform normal animal cells into "
  "cancerous cells; both have been disarmed and used as vectors.",
  ["Gene delivery learnt from bacteria and viruses (pathogens of eukaryotes)"],
  "Tools of Recombinant DNA Technology",
  at="B", correct="Bacteria and viruses, which have known for ages how to deliver genes to transform eukaryotic cells",
  wrong=["Fungi that break down plant cell walls with chitinase", "Chemical carcinogens present in tobacco smoke",
         "Thermophilic bacteria such as Thermus aquaticus"],
  why="NCERT credits pathogenic bacteria (Agrobacterium) and viruses (retroviruses) for the art of gene delivery; "
      "chitinase is used to break fungal cells, carcinogens cause cancer, and Thermus aquaticus is the source of the "
      "PCR polymerase.", secs=25)

Z(BPP, "Restriction enzymes", B, MUL,
  MS("Which of the following are nucleases, as described in NCERT?",
     ["Exonucleases", "Endonucleases", "Restriction enzymes", "DNA ligase", "Thermostable DNA polymerase"]),
  "Nucleases",
  "NCERT: restriction enzymes belong to a larger class of enzymes called nucleases. These are of two kinds: "
  "exonucleases, which remove nucleotides from the ends of the DNA, and endonucleases, which make cuts at specific "
  "positions within the DNA. DNA ligase joins DNA fragments and DNA polymerase synthesises DNA; neither is a "
  "nuclease.",
  ["Nucleases: exonucleases, endonucleases (restriction enzymes belong here)",
   "DNA ligase: joins; DNA polymerase: synthesises"],
  "Tools of Recombinant DNA Technology",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only"],
  why="Restriction enzymes are nucleases, so '(a) and (b) only' is incomplete; DNA ligase and DNA polymerase build "
      "or join DNA rather than cut it, so options with (d) or (e) are wrong.", secs=35)

EC_SITES = 3
EC_BONDS, EC_FRAGS = 2 * EC_SITES, EC_SITES
assert (EC_BONDS, EC_FRAGS) == (6, 3)
Z(BPP, "Restriction enzymes", I, NUM,
  "A circular plasmid has three recognition sites for EcoRI. It is digested completely with EcoRI, which, at each "
  "recognition site, cuts each of the two strands of the double helix once in its sugar-phosphate backbone. How "
  "many phosphodiester bonds are broken in all, and how many DNA fragments are obtained?",
  "Counting cuts made by a restriction enzyme",
  "NCERT: once a restriction endonuclease finds its specific recognition sequence, it binds to the DNA and cuts each "
  "of the two strands of the double helix at specific points in their sugar-phosphate backbones. So each site "
  "breaks 2 phosphodiester bonds. A circular DNA cut at n sites gives n fragments (a linear DNA would give n + 1).",
  ["Bonds broken = 2 per site x 3 sites = 6", "Circular DNA with 3 cuts -> 3 fragments"],
  "Processes of Recombinant DNA Technology",
  at="C", correct="6 bonds; 3 fragments",
  wrong=["3 bonds; 3 fragments", "6 bonds; 4 fragments", "3 bonds; 4 fragments"],
  why="'3 bonds' counts only one strand per site, although both strands are cut; '4 fragments' applies the rule for "
      "a linear DNA (n + 1) to a circular plasmid.", secs=60, vb=RECOMPUTED)

Z(BPP, "Cloning vectors", I, D,
  "A researcher cuts a vector and a source DNA with the same restriction enzyme, EcoRI, and mixes the two, but "
  "forgets to add DNA ligase. Following NCERT's account, which of the following is expected?",
  "Role of DNA ligase",
  "NCERT: restriction enzymes cut each strand a little away from the centre of the palindrome, leaving overhanging "
  "stretches (sticky ends). These form hydrogen bonds with their complementary cut counterparts, and this "
  "stickiness facilitates the action of the enzyme DNA ligase, which joins the ends. Only after the cut gene and "
  "the cut vector are mixed and ligase is added does this result in recombinant DNA.",
  ["Same enzyme -> matching sticky ends -> hydrogen bonding", "Joining into recombinant DNA needs DNA ligase"],
  "Processes of Recombinant DNA Technology",
  at="A",
  correct="The sticky ends can pair by hydrogen bonds, but without ligase the gene is not joined to the vector to "
          "give a recombinant DNA",
  wrong=["A recombinant DNA forms normally, because sticky ends are joined covalently on their own",
         "EcoRI itself joins the cut ends, so ligase is not needed",
         "The ends cannot pair at all, because sticky ends never form hydrogen bonds"],
  why="Sticky ends only hydrogen-bond; joining needs ligase, so the first two options are wrong; NCERT states that "
      "sticky ends do form hydrogen bonds with their counterparts, so the last option is wrong.", secs=45)

Z(BPP, "PCR and gel electrophoresis", I, ASR,
  AR("Agarose gel electrophoresis separates DNA fragments according to their size.",
     "In an agarose gel, the larger DNA fragments move faster and farther than the smaller ones."),
  "Separation by size in agarose gel",
  "NCERT: the cut fragments of DNA are separated by gel electrophoresis; the DNA fragments separate (resolve) "
  "according to their size through the sieving effect provided by the agarose gel. Hence, the smaller the "
  "fragment size, the farther it moves. So A is true and R reverses the direction of the size effect.",
  ["A: true", "R: false - smaller fragments move farther"],
  "Processes of Recombinant DNA Technology", ans="C",
  why="R contradicts NCERT's 'the smaller the fragment size, the farther it moves', so options with R true are wrong; "
      "A is NCERT's statement, so 'A is false' is wrong.", secs=30)

Z(BPP, "Bioreactors and downstream processing", I, STP,
  SP("When a piece of alien DNA is inserted into a cloning vector and transferred into a bacterial, plant or animal "
     "cell, the alien DNA gets multiplied.",
     "Since the ultimate aim is usually to produce a desirable protein, the recombinant DNA has to be expressed, and "
     "the foreign gene gets expressed under appropriate conditions."),
  "Obtaining the foreign gene product",
  "NCERT (Obtaining the Foreign Gene Product): when you insert a piece of alien DNA into a cloning vector and "
  "transfer it into a bacterial, plant or animal cell, the alien DNA gets multiplied. In almost all recombinant "
  "technologies, the ultimate aim is to produce a desirable protein. Hence, there is a need for the recombinant DNA "
  "to be expressed. The foreign gene gets expressed under appropriate conditions.",
  ["Statement I: true", "Statement II: true"],
  "Processes of Recombinant DNA Technology", ans="A",
  why="Both statements are NCERT's own, so every option with a false statement is wrong.", secs=30)

Z(BPP, "Competent hosts and transformation", I, MAT,
  ML(("step in recombinant DNA work", "agent used"),
     ["Breaking open bacterial cells to release DNA", "Precipitating the purified DNA",
      "Joining the gene of interest to the cut vector", "Making bacterial cells competent to take up DNA"],
     ["DNA ligase", "Chilled ethanol", "A divalent cation such as calcium", "Lysozyme"]),
  "Agents used at different steps",
  "NCERT: bacterial cells are broken open with lysozyme; purified DNA ultimately precipitates out after the addition "
  "of chilled ethanol; the cut gene of interest and the cut vector are mixed and ligase is added to give recombinant "
  "DNA; bacterial cells are made competent by treating them with a specific concentration of a divalent cation, "
  "such as calcium.",
  ["A -> IV", "B -> II", "C -> I", "D -> III"],
  "Processes of Recombinant DNA Technology; Tools of Recombinant DNA Technology",
  at="D", match=({"A": "IV", "B": "II", "C": "I", "D": "III"},
                 [{"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="Calcium makes cells competent but does not lyse them, so swapping A and D is wrong; ethanol precipitates DNA "
      "and ligase joins it, so swapping B and C is wrong; the last code mismatches every step.", secs=45)

Z(BPP, "Competent hosts and transformation", I, MUL,
  MS("Which of the following statements are true for BOTH micro-injection and biolistics (gene gun), as described "
     "in NCERT?",
     ["Neither uses a 'disarmed pathogen' vector.",
      "Both are methods of introducing recombinant DNA into host cells.",
      "NCERT describes both as methods for animal cells.",
      "Both use micro-particles of gold or tungsten coated with DNA.",
      "In both, the recombinant DNA is injected directly into the nucleus."]),
  "Micro-injection and biolistics compared",
  "NCERT: in micro-injection, recombinant DNA is directly injected into the nucleus of an animal cell. In another "
  "method, suitable for plants, cells are bombarded with high velocity micro-particles of gold or tungsten coated "
  "with DNA (biolistics or gene gun). The last method uses 'disarmed pathogen' vectors. So both micro-injection and "
  "biolistics introduce rDNA without a pathogen vector; they differ in cell type and procedure.",
  ["(a), (b): true for both", "(c): biolistics is for plants", "(d): only biolistics", "(e): only micro-injection"],
  "Processes of Recombinant DNA Technology",
  at="B", correct="(a) and (b) only",
  wrong=["(a), (b) and (c) only", "(b) and (d) only", "(a), (b) and (e) only"],
  why="Biolistics is described as suitable for plants, uses metal micro-particles and does not inject into the "
      "nucleus, while micro-injection uses no particles; so (c), (d) and (e) each hold for only one method.",
  secs=50)

Z(BPP, "PCR and gel electrophoresis", I, D,
  "In NCERT's procedure for isolating DNA, which pair of enzymes is used to REMOVE contaminating macromolecules "
  "from the DNA preparation, rather than to break open the cells?",
  "Purifying DNA",
  "NCERT: the cell is broken open with enzymes such as lysozyme (bacteria), cellulase (plant cells) and chitinase "
  "(fungus). Genes are located on long DNA molecules intertwined with proteins such as histones; RNA can be removed "
  "by treatment with ribonuclease, whereas proteins can be removed by treatment with protease. Other molecules are "
  "removed by appropriate treatments, and purified DNA is precipitated with chilled ethanol.",
  ["Break open cells: lysozyme, cellulase, chitinase", "Remove RNA: ribonuclease; remove proteins: protease"],
  "Processes of Recombinant DNA Technology",
  at="C", correct="Ribonuclease and protease",
  wrong=["Lysozyme and cellulase", "Chitinase and protease", "Ribonuclease and lysozyme"],
  why="Lysozyme, cellulase and chitinase are used to break open bacterial, plant and fungal cells respectively, so "
      "any pair containing one of them is wrong.", secs=30)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("A restriction endonuclease cuts only one of the two strands of DNA at its recognition site.",
     "Once a restriction endonuclease finds its specific recognition sequence, it binds to the DNA."),
  "Action of a restriction endonuclease",
  "NCERT: each restriction endonuclease functions by 'inspecting' the length of a DNA sequence. Once it finds its "
  "specific recognition sequence, it will bind to the DNA and cut each of the two strands of the double helix at "
  "specific points in their sugar-phosphate backbones. So A is false (both strands are cut) and R is true.",
  ["A: false - both strands are cut", "R: true"],
  "Tools of Recombinant DNA Technology", ans="D",
  why="A contradicts NCERT, which says each of the two strands is cut, so all options with A true are wrong; R is "
      "NCERT's statement, so 'A is false but R is true' is correct.", secs=30)

Z(BPP, "Restriction enzymes", A, D,
  "Starting from a bacterial culture, a researcher isolates DNA, cuts it and joins the gene of interest to a vector "
  "following NCERT's procedure. Which option lists the enzymes in the order in which they are used?",
  "Order of enzymes in recombinant DNA work",
  "NCERT: the bacterial cell is first broken open (lysozyme); RNA is removed by ribonuclease (and proteins by "
  "protease) so that the DNA is pure, because DNA must be free from other macromolecules before it can be cut; the "
  "pure DNA is then cut with a restriction enzyme; finally the cut gene of interest and the cut vector are mixed and "
  "DNA ligase is added to give recombinant DNA.",
  ["Lyse cells: lysozyme", "Purify: ribonuclease", "Cut: restriction endonuclease", "Join: DNA ligase"],
  "Processes of Recombinant DNA Technology",
  at="B", correct="Lysozyme -> ribonuclease -> restriction endonuclease -> DNA ligase",
  wrong=["Ribonuclease -> lysozyme -> DNA ligase -> restriction endonuclease",
         "Lysozyme -> restriction endonuclease -> ribonuclease -> DNA ligase",
         "Lysozyme -> ribonuclease -> DNA ligase -> restriction endonuclease"],
  why="The cells must be opened before the DNA can be purified; DNA must be pure before it is cut, so cutting cannot "
      "precede ribonuclease treatment; and the fragments must be cut before ligase can join them.", secs=50)

Z(BPP, "PCR and gel electrophoresis", A, D,
  "In an agarose gel electrophoresis, a student wrongly connects the power supply so that the electrode at the end "
  "of the gel nearer the wells is the POSITIVE electrode (anode). Following NCERT, what will happen to the DNA "
  "loaded in the wells?",
  "Direction of DNA movement in a gel",
  "NCERT: DNA is a negatively charged molecule; hence it moves towards the anode (positive electrode) under an "
  "electric field through the agarose matrix, the fragments separating by size through the sieving effect of the "
  "gel. If the anode is placed at the well end, the DNA will move towards it, i.e. out of the wells away from the "
  "gel, so it will not be resolved in the gel.",
  ["DNA is negatively charged -> moves to the anode", "Anode at the well end -> DNA leaves the wells away from the gel"],
  "Processes of Recombinant DNA Technology",
  at="A",
  correct="The DNA moves towards the electrode next to the wells, away from the gel, so no fragments are resolved in "
          "the gel",
  wrong=["The fragments separate normally, since separation depends only on size",
         "The larger fragments now move farther into the gel than the smaller ones",
         "The DNA stays in the wells, because DNA carries no charge"],
  why="Movement direction depends on DNA's negative charge, so it cannot separate normally with reversed electrodes; "
      "reversing polarity does not reverse the size order inside the gel; DNA is negatively charged, not neutral.",
  secs=50)

Z(BPP, "PCR and gel electrophoresis", A, MUL,
  MS("A researcher amplifies a gene by PCR and then clones it in E. coli. Which of the following statements are "
     "correct according to NCERT?",
     ["The amplified fragment can be used to ligate with a vector for further cloning.",
      "The DNA polymerase used is thermostable, so it remains active during the high temperature of denaturation.",
      "The PCR has to be carried out inside a living host cell.",
      "The primers are small, chemically synthesised oligonucleotides complementary to regions of the template DNA.",
      "The recombinant DNA is introduced into E. coli cells that have been made competent, for example by calcium "
      "treatment followed by heat shock."]),
  "From PCR to cloning",
  "NCERT: in PCR, multiple copies of the gene (or DNA) of interest are synthesised in vitro using two sets of primers "
  "(small chemically synthesised oligonucleotides complementary to regions of the DNA) and DNA polymerase; a "
  "thermostable DNA polymerase (from Thermus aquaticus) remains active during high-temperature denaturation. The "
  "amplified fragment, if desired, can now be used to ligate with a vector for further cloning. The recombinant DNA "
  "is put into competent host cells, e.g. E. coli treated with calcium and given a heat shock.",
  ["(a), (b), (d), (e): true", "(c): false - PCR is done in vitro"],
  "Processes of Recombinant DNA Technology; Tools of Recombinant DNA Technology",
  at="D", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b) and (d) only", "(a), (b), (c) and (d) only", "(b), (c), (d) and (e) only"],
  why="PCR synthesises DNA in vitro, so any option with (c) is wrong; '(a), (b) and (d) only' leaves out the "
      "transformation of competent E. coli, which is how the recombinant DNA enters the host.", secs=60)

Z(BPP, "Cloning vectors", A, STP,
  SP("As used for gene transfer, both the Ti plasmid of Agrobacterium tumefaciens and the retroviruses are in a "
     "disarmed (non-pathogenic) form.",
     "Agrobacterium tumefaciens delivers a piece of DNA (T-DNA) that transforms normal plant cells into tumour cells, "
     "which then produce the chemicals required by the pathogen."),
  "Disarmed pathogen vectors",
  "NCERT: Agrobacterium tumefaciens, a pathogen of several dicot plants, is able to deliver a piece of DNA known as "
  "T-DNA to transform normal plant cells into a tumor and direct these tumor cells to produce the chemicals "
  "required by the pathogen. The tumor inducing (Ti) plasmid has now been modified into a cloning vector which is no "
  "more pathogenic to the plants. Similarly, retroviruses have also been disarmed and are now used to deliver "
  "desirable genes into animal cells.",
  ["Statement I: true (modified Ti plasmid; disarmed retroviruses)", "Statement II: true (wild Agrobacterium)"],
  "Tools of Recombinant DNA Technology", ans="A",
  why="Statement II describes the natural pathogen and Statement I the vectors derived from it; both match NCERT, so "
      "every option with a false statement is wrong.", secs=45)

Z(BPP, "Bioreactors and downstream processing", A, D,
  "An aerobic microbial culture growing in a simple stirred-tank bioreactor is limited by the supply of oxygen. "
  "Which design described in NCERT would most directly improve oxygen transfer to the cells?",
  "Sparged stirred-tank bioreactor",
  "NCERT: the most commonly used bioreactors are of the stirring type. The stirrer facilitates even mixing and "
  "oxygen availability throughout the bioreactor. In a sparged stirred-tank bioreactor, sterile air bubbles are "
  "sparged through the culture; sparging greatly increases the area for oxygen transfer. The foam control system "
  "and sampling ports serve other purposes.",
  ["Sparging sterile air bubbles -> greatly increased area for oxygen transfer"],
  "Processes of Recombinant DNA Technology",
  at="C", correct="A sparged stirred-tank bioreactor, through which sterile air bubbles are sparged",
  wrong=["Adding a foam control system", "Withdrawing more samples through the sampling ports",
         "Shifting the culture to a small-volume laboratory flask"],
  why="Foam control and sampling ports do not increase oxygen transfer; small-volume cultures cannot yield "
      "appreciable quantities of product and do not solve the oxygen limitation.", secs=40)

Z(BPP, "Restriction enzymes", A, D,
  "Which of the following steps in recombinant DNA technology does NOT need a restriction enzyme?",
  "Where restriction enzymes are and are not used",
  "NCERT: restriction enzymes are used to cut the source DNA to release the gene of interest and to cut the vector, "
  "creating matching sticky ends; a vector with a single recognition site is opened (linearised) at that site for "
  "the insert. PCR amplifies a gene in vitro using two sets of primers, DNA polymerase, nucleotides and the template "
  "DNA; no restriction enzyme is needed for amplification.",
  ["Cutting gene, cutting vector, opening the cloning site -> restriction enzyme",
   "PCR amplification -> primers + thermostable DNA polymerase only"],
  "Processes of Recombinant DNA Technology",
  at="D", correct="Amplifying the gene of interest by PCR",
  wrong=["Cutting out the gene of interest from the source DNA",
         "Creating sticky ends on the vector so that the gene can be inserted",
         "Opening a circular plasmid at its single cloning site"],
  why="Each of the other steps is a cut made at a specific recognition sequence, which is exactly what a restriction "
      "endonuclease does.", secs=35)
