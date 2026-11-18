
# ================================================================ Molecular Basis of Inheritance (7 / 10 / 8)
C12_MB = lambda s: ref(12, MBI, s)

add(MBI, "Replication", "Basic", "direct",
    "The scheme of DNA replication in which each strand of the double helix acts as a template for the synthesis "
    "of a new complementary strand was proposed by:",
    P("Watson and Crick themselves", ["Meselson and Stahl", "Taylor and colleagues", "Hershey and Chase"], "A"),
    "Proposal and proof of semiconservative replication",
    "NCERT: while proposing the double helix structure, Watson and Crick also proposed a scheme for replication: "
    "the two strands separate and each acts as a template for a new complementary strand, so that each daughter "
    "molecule has one parental and one new strand (semiconservative). Meselson and Stahl (1958) later proved it "
    "experimentally in E. coli, and Taylor and colleagues showed it for chromosomes of Vicia faba.",
    ["Proposed: Watson and Crick", "Proved in E. coli: Meselson and Stahl", "Shown in chromosomes: Taylor"],
    C12_MB("replication: the experimental proof"),
    why="Meselson and Stahl and Taylor provided experimental proof; Hershey and Chase showed that DNA is the "
        "genetic material.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "According to NCERT, a nucleotide has three components. They are:",
    P("A nitrogenous base, a pentose sugar and a phosphate group",
      ["A nitrogenous base, a hexose sugar and a phosphate group", "A nitrogenous base, a pentose sugar and an "
       "amino acid", "Two nitrogenous bases joined by hydrogen bonds and a phosphate group"], "D"),
    "Components of a nucleotide",
    "NCERT: a nucleotide has three components: a nitrogenous base, a pentose sugar (ribose in RNA, deoxyribose in "
    "DNA) and a phosphate group. A base linked to the sugar is a nucleoside; adding a phosphate at the 5'-OH gives "
    "a nucleotide.",
    ["Base + pentose = nucleoside", "Nucleoside + phosphate = nucleotide"],
    C12_MB("structure of polynucleotide chain"),
    why="The sugar is a pentose, not a hexose; amino acids are not part of nucleotides; hydrogen-bonded base pairs "
        "belong to the double helix, not to a single nucleotide.",
    seconds=20)

add(MBI, "Transcription", "Basic", "assertion_reason",
    ar("The base sequence of an mRNA is the same as that of the coding strand of its gene, except that the mRNA "
       "has uracil in place of thymine.",
       "The mRNA is synthesised complementary to the template strand, and the template strand is itself "
       "complementary to the coding strand."),
    AR("A"),
    "Why mRNA matches the coding strand",
    "NCERT: in a transcription unit, the strand with 3'→5' polarity acts as the template, and the other strand, "
    "with 5'→3' polarity, has the same sequence as the RNA (except thymine at the place of uracil) and is called "
    "the coding strand. The RNA is built by complementary base pairing on the template; since the coding strand "
    "is also complementary to the template, the RNA and the coding strand carry the same sequence, with U in RNA "
    "where DNA has T. R is the direct cause of A.",
    ["RNA = complement of template", "Coding strand = complement of template", "So RNA = coding strand (U for T)"],
    C12_MB("transcription: transcription unit"),
    seconds=30)

add(MBI, "DNA as genetic material", "Basic", "statement_pair",
    sp("RNA, being a catalyst as well as genetic material, was reactive and hence unstable.",
       "DNA has evolved from RNA with chemical modifications that make it more stable."),
    SP("A"),
    "From the RNA world to DNA",
    "NCERT (RNA world): RNA was the first genetic material and used to act both as genetic material and as a "
    "catalyst. But RNA, being a catalyst, was reactive and hence unstable (Statement I true). Therefore DNA has "
    "evolved from RNA with chemical modifications that make it more stable; being double stranded, with a "
    "complementary strand, DNA further resists changes by evolving a process of repair (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_MB("RNA world"),
    seconds=30)

add(MBI, "Replication", "Basic", "match_list",
    ml(("enzyme or catalyst", "role"),
       ["DNA-dependent DNA polymerase", "DNA ligase", "DNA-dependent RNA polymerase",
        "23S rRNA in bacteria (ribozyme)"],
       ["Joins the discontinuously synthesised fragments", "Forms peptide bonds during translation",
        "Synthesises RNA on a DNA template", "Polymerises deoxyribonucleotides on a DNA template"]),
    M(mc("IV,I,III,II"), [mc("III,I,IV,II"), mc("IV,II,III,I"), mc("I,IV,III,II")], "C"),
    "Enzymes of replication, transcription and translation",
    "DNA-dependent DNA polymerases polymerise deoxyribonucleotides using a DNA template (A-IV). The discontinuously "
    "synthesised fragments of the lagging strand are later joined by DNA ligase (B-I). Transcription is catalysed "
    "by DNA-dependent RNA polymerase (C-III). In bacteria, 23S rRNA acts as the enzyme (ribozyme) for peptide bond "
    "formation (D-II).",
    ["A → IV", "B → I", "C → III", "D → II"],
    C12_MB("replication: the machinery and the enzymes; transcription; translation"),
    why="The other codes swap DNA and RNA polymerase, ligase with the ribozyme, or the polymerase with ligase.",
    seconds=35)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "The pentose sugar present in the nucleotides of DNA is:",
    P("2'-deoxyribose", ["Ribose", "Glucose", "3'-deoxyribose"], "B"),
    "Sugar of DNA",
    "NCERT: the pentose sugar is ribose in RNA and 2'-deoxyribose in DNA, which is why the nucleic acids are "
    "named ribonucleic acid and deoxyribonucleic acid. RNA retains a 2'-OH group on every nucleotide, which makes "
    "it labile; DNA lacks it.",
    ["RNA: ribose", "DNA: 2'-deoxyribose (no 2'-OH)"],
    C12_MB("structure of polynucleotide chain"),
    why="Ribose is the sugar of RNA, glucose is a hexose, and the missing oxygen in DNA's sugar is at the 2' "
        "carbon, not the 3' carbon.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Basic", "multi_statement",
    ms("Which of the following nitrogenous bases are pyrimidines?",
       ["Cytosine", "Thymine", "Uracil", "Adenine", "Guanine"]),
    MS(["a", "b", "c"], [["a", "d", "e"], ["d", "e"], ["a", "b", "d"]], "D"),
    "Purines and pyrimidines",
    "NCERT: nitrogenous bases are of two types, purines (adenine and guanine) and pyrimidines (cytosine, uracil "
    "and thymine). Cytosine is common to DNA and RNA; thymine is present in DNA and uracil in RNA.",
    ["Purines: A, G", "Pyrimidines: C, T, U"],
    C12_MB("structure of polynucleotide chain"),
    why="Adenine and guanine are purines, so options with (d) or (e) are wrong.",
    seconds=25)

add(MBI, "Lac operon", "Intermediate", "direct",
    "A mutant E. coli has an altered operator to which the lac repressor can no longer bind; its i, z, y and a "
    "genes and its promoter are normal. Glucose is absent. What happens in this mutant?",
    P("The z, y and a genes are transcribed even when lactose is absent",
      ["The z, y and a genes are never transcribed, even when lactose is present",
       "The z, y and a genes are transcribed only when lactose is present, as in the wild type",
       "Only the i gene is transcribed, and the repressor accumulates in the cell"], "C"),
    "Role of the operator in negative regulation",
    "In the lac operon, the repressor (from the i gene) binds to the operator and prevents RNA polymerase from "
    "transcribing the structural genes; the inducer acts by inactivating the repressor. If the repressor cannot "
    "bind the operator, nothing blocks RNA polymerase, so the polycistronic z-y-a mRNA is made whether or not "
    "lactose is present: the operon is expressed all the time.",
    ["Repressor must bind operator to switch the operon off", "Operator cannot bind repressor → never switched "
     "off", "z, y, a transcribed even without lactose"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="Nothing stops transcription in this mutant, so it cannot be 'never' or 'only with lactose'; the i gene is "
        "transcribed in the wild type too and its product simply cannot act here.",
    seconds=45)

add(MBI, "Lac operon", "Intermediate", "assertion_reason",
    ar("When the lac operon is switched on, the z, y and a genes are transcribed together.",
       "In the lac operon, a polycistronic structural gene is regulated by a common promoter and regulatory genes."),
    AR("A"),
    "Polycistronic organisation of the lac operon",
    "NCERT: in bacteria, the arrangement in which a polycistronic structural gene is regulated by a common promoter "
    "and regulatory genes is called an operon. The lac operon's structural genes z, y and a share one promoter and "
    "operator, so when the repressor is removed by the inducer, RNA polymerase transcribes them as one "
    "polycistronic mRNA. R explains A.",
    ["One promoter for z, y, a", "Polycistronic transcript", "R explains A"],
    C12_MB("regulation of gene expression: the lac operon"),
    seconds=35)

_phx = 5386
assert 2 * _phx == 10772

add(MBI, "DNA and RNA structure", "Intermediate", "statement_pair",
    sp("Because the bases pair in a complementary way, if the sequence of bases in one strand of a DNA double "
       "helix is known, the sequence in the other strand can be predicted.",
       "A circular double-stranded DNA molecule of 5386 base pairs has 10,772 phosphodiester linkages in all."),
    SP("A"),
    "Complementarity and counting linkages",
    "NCERT: base pairing confers a very unique property on the polynucleotide chains: they are complementary, so "
    "if the sequence of one strand is known, the other can be predicted (Statement I true). In a circular strand "
    "of n nucleotides there are n phosphodiester linkages (a linear strand has n − 1). Two strands of 5386 "
    "nucleotides each: 2 × 5386 = 10,772 (Statement II true).",
    ["Statement I: true", "Circular strand: n linkages", "2 × 5386 = 10,772 → Statement II true"],
    C12_MB("structure of polynucleotide chain"),
    seconds=50, verified_by=RECOMPUTED)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "multi_statement",
    ms("Which of the following statements about the significance and findings of the Human Genome Project are "
       "correct according to NCERT?",
       ["Knowledge about the effects of DNA variations among individuals can lead to revolutionising the ways to "
        "diagnose, treat and someday prevent thousands of disorders that affect human beings.",
        "Learning about non-human organisms' DNA sequences can lead to an understanding of their natural "
        "capabilities that can be applied to challenges in health care, agriculture, energy production and "
        "environmental remediation.",
        "Since less than 2 per cent of the genome codes for proteins, the remaining DNA has been shown to have no "
        "role at all.",
        "The human genome contains about 80,000 genes.",
        "The functions of all the discovered human genes are now known."]),
    MS(["a", "b"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d"]], "D"),
    "Why the Human Genome Project matters",
    "NCERT: knowledge about the effects of DNA variations among individuals can revolutionise the ways to "
    "diagnose, treat and someday prevent thousands of disorders (a); learning about the DNA of non-human "
    "organisms can lead to an understanding of their natural capabilities, applicable to health care, "
    "agriculture, energy production and environmental remediation (b). Repetitive sequences, though thought to "
    "have no direct coding function, shed light on chromosome structure, dynamics and evolution (c false). The "
    "genome has about 30,000 genes, not 80,000 (d false), and functions are unknown for over 50 per cent of the "
    "discovered genes (e false).",
    ["(a), (b): NCERT's significance of HGP", "(c), (d), (e): contradict NCERT's salient features"],
    C12_MB("human genome project: goals, methodologies and salient features"),
    why="Every other option includes at least one false statement.",
    seconds=55)

add(MBI, "DNA as genetic material", "Intermediate", "match_list",
    ml(("experiment", "label used"),
       ["Hershey and Chase: labelling the DNA of bacteriophages",
        "Hershey and Chase: labelling the protein coat of bacteriophages",
        "Meselson and Stahl: replication in E. coli",
        "Taylor and colleagues: replication in chromosomes of Vicia faba"],
       ["Radioactive thymidine", "¹⁵NH₄Cl as the only nitrogen source", "Radioactive sulphur",
        "Radioactive phosphorus"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,III,I,II"), mc("II,III,IV,I")], "A"),
    "Labels used in classic experiments",
    "DNA contains phosphorus but not sulphur, and protein contains sulphur but not phosphorus, so Hershey and Chase "
    "labelled phage DNA with radioactive phosphorus (A-IV) and the protein coat with radioactive sulphur (B-III). "
    "Meselson and Stahl grew E. coli on ¹⁵NH₄Cl as the only nitrogen source to make heavy DNA (C-II). Taylor and "
    "colleagues used radioactive thymidine on Vicia faba to detect the distribution of newly synthesised DNA in "
    "chromosomes (D-I).",
    ["P in DNA, S in protein", "Heavy nitrogen for density separation", "Radioactive thymidine for chromosomes"],
    C12_MB("the search for genetic material; replication: the experimental proof"),
    why="The other codes swap the two Hershey–Chase labels or the two replication experiments.",
    seconds=40)

add(MBI, "DNA as genetic material", "Intermediate", "direct",
    "In a variation of Griffith's experiment, mice are injected with a mixture of heat-killed S strain and "
    "heat-killed R strain Streptococcus pneumoniae. What is expected?",
    P("The mice live, because no living bacteria are present to be transformed or to multiply",
      ["The mice die, because the R strain is transformed by the S strain",
       "The mice die, because heat-killed S strain bacteria alone are virulent",
       "The mice live, but living S strain bacteria are recovered from them"], "C"),
    "Transformation needs living recipient cells",
    "NCERT (Griffith): live S strain kills mice; live R strain and heat-killed S strain alone do not. Only when "
    "heat-killed S was mixed with live R did the mice die, because the living R bacteria were transformed into "
    "virulent S bacteria. With both strains heat-killed, there are no living cells to be transformed or to cause "
    "infection, so the mice survive and no living bacteria can be recovered.",
    ["Heat-killed S alone: mice live", "Transformation needs living R cells", "Both killed → mice live"],
    C12_MB("the search for genetic material: transforming principle"),
    why="Dead R cells cannot be transformed; heat-killed S alone is not virulent; and no living S cells can be "
        "recovered without living bacteria.",
    seconds=40)

add(MBI, "Transcription", "Intermediate", "multi_statement",
    ms("The template strand of a short stretch of a structural gene reads 3'-TACGAT-5'. Which of the following "
       "statements are correct?",
       ["The mRNA transcribed from it reads 5'-AUGCUA-3'.",
        "The coding strand reads 5'-ATGCTA-3'.",
        "The first codon of the mRNA is the initiation codon AUG.",
        "The mRNA contains thymine at two positions.",
        "The RNA is polymerised in the 3'→5' direction."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Reading template and coding strands",
    "RNA is complementary and antiparallel to the template: template 3'-TACGAT-5' gives mRNA 5'-AUGCUA-3' (a). The "
    "coding strand has the same sequence as the mRNA with T for U: 5'-ATGCTA-3' (b). The first codon AUG is the "
    "initiation codon (c). RNA has uracil, not thymine (d false), and all nucleic acid polymerases add "
    "nucleotides in the 5'→3' direction (e false).",
    ["Template 3'-TAC GAT-5' → mRNA 5'-AUG CUA-3'", "Coding strand = mRNA with T for U", "(d), (e) false"],
    C12_MB("transcription: transcription unit"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (e)' also omits (a).",
    seconds=50)

add(MBI, "Transcription", "Intermediate", "statement_pair",
    sp("In eukaryotes, RNA polymerase I transcribes the rRNAs 28S, 18S and 5.8S, whereas RNA polymerase III "
       "transcribes the 5S rRNA.",
       "In eukaryotes, the heterogeneous nuclear RNA, the precursor of mRNA, is transcribed by RNA polymerase III."),
    SP("C"),
    "Division of labour among eukaryotic RNA polymerases",
    "NCERT: in eukaryotes there are at least three RNA polymerases in the nucleus. RNA polymerase I transcribes "
    "rRNAs (28S, 18S and 5.8S); RNA polymerase III transcribes tRNA, 5S rRNA and snRNAs (Statement I true); RNA "
    "polymerase II transcribes the precursor of mRNA, hnRNA (Statement II false).",
    ["Pol I: 28S, 18S, 5.8S rRNA", "Pol II: hnRNA", "Pol III: tRNA, 5S rRNA, snRNA"],
    C12_MB("transcription: transcription unit and gene"),
    seconds=35)

add(MBI, "Transcription", "Intermediate", "assertion_reason",
    ar("In bacteria, the mRNA does not require any processing to become active.",
       "Bacterial structural genes are split genes, with coding sequences interrupted by introns."),
    AR("C"),
    "Bacterial versus eukaryotic genes",
    "NCERT: in bacteria the mRNA does not require any processing to become active, and since transcription and "
    "translation occur in the same compartment, translation can begin before the mRNA is fully transcribed (A "
    "true). Split genes, with exons interrupted by introns, are a feature of eukaryotes; their hnRNA must be "
    "spliced. Bacterial genes are not split, so R is false.",
    ["A: true", "Split genes → eukaryotes", "R: false"],
    C12_MB("transcription: transcription unit and gene; processing of hnRNA"),
    seconds=30)

_strand = {"A": 30, "T": 20, "G": 15, "C": 35}
_g_ds = F(_strand["G"] + _strand["C"], 2)
assert _g_ds == 25

add(MBI, "DNA and RNA structure", "Intermediate", "direct",
    "One strand of a double-stranded DNA molecule has the base composition A 30 per cent, T 20 per cent, G 15 per "
    "cent and C 35 per cent. What percentage of all the bases in the double-stranded molecule is guanine?",
    P("25 per cent", ["15 per cent", "35 per cent", "50 per cent"], "D"),
    "Base composition of a double helix from one strand",
    "Each G in one strand pairs with a C in the other. The complementary strand therefore has G = 35 per cent "
    "(opposite the C of the first strand). Total G = (15 + 35)/2 = 25 per cent of the bases of the double "
    "helix. Check with Chargaff's rule: then C = 25, and A = T = (30 + 20)/2 = 25 per cent each.",
    ["Strand 1: G 15, C 35 → strand 2: G 35", "Average over two strands: (15 + 35)/2 = 25%"],
    C12_MB("structure of polynucleotide chain: double helix and Chargaff's rule"),
    why="15 per cent is the G of one strand only; 35 per cent is the G of the other strand only; 50 per cent is "
        "G + C, not G alone.",
    seconds=50, verified_by=RECOMPUTED)

add(MBI, "Lac operon", "Advanced", "match_list",
    ml(("E. coli strain (glucose absent)", "behaviour of the lac operon"),
       ["Wild type", "Mutant whose operator cannot bind the repressor",
        "Mutant whose repressor binds the operator but cannot interact with the inducer",
        "Mutant lacking the lac promoter"],
       ["Expressed only when lactose is present", "Expressed even when lactose is absent",
        "Not expressed even when lactose is present, because the repressor stays bound",
        "Not expressed, because RNA polymerase has no binding site"]),
    M(mc("I,II,III,IV"), [mc("I,III,II,IV"), mc("II,I,III,IV"), mc("I,II,IV,III")], "B"),
    "Predicting lac operon behaviour in mutants",
    "Wild type: the repressor blocks the operator; lactose (inducer) inactivates it, so the operon is inducible "
    "(A-I). If the operator cannot bind the repressor, nothing blocks RNA polymerase and the genes are expressed "
    "even without lactose (B-II). If the repressor cannot interact with the inducer, it stays bound to the "
    "operator even when lactose is present (C-III). The promoter provides the binding site for RNA polymerase; "
    "without it, transcription cannot start (D-IV).",
    ["Inducer inactivates repressor", "Operator must bind repressor to switch off", "Promoter is needed to start"],
    C12_MB("regulation of gene expression: the lac operon; transcription unit"),
    why="The other codes swap the inducible and constitutive states, or the two non-expressing mutants, whose "
        "causes differ.",
    seconds=70)

add(MBI, "Genetic code and translation", "Advanced", "multi_statement",
    "The coding strand of a short gene reads 5'-ATGGCATTCTAA-3'. Use: AUG = methionine, GCA = alanine, "
    "UUC = phenylalanine, UUU = phenylalanine, UAA = stop.\n\n" +
    ms("Which of the following statements are correct?",
       ["The mRNA reads 5'-AUGGCAUUCUAA-3'.",
        "The polypeptide formed is methionine–alanine–phenylalanine.",
        "Deleting the fifth base of the gene would leave the amino acid sequence unchanged.",
        "Changing the ninth base of the coding strand from C to T would not change the polypeptide.",
        "The template strand, written 5'→3', reads 5'-ATGGCATTCTAA-3'."]),
    MS(["a", "b", "d"], [["a", "b", "c", "d"], ["a", "d", "e"], ["b", "c", "e"]], "A"),
    "Codons, mutations and the degenerate code",
    "mRNA = coding strand with U for T: AUG GCA UUC UAA (a): Met–Ala–Phe, then stop (b). Deleting the fifth base "
    "(C) gives AUG GAU UCU AA…: the reading frame shifts and the amino acids after the first change (c false). C→T "
    "at the ninth base turns UUC into UUU, which also codes for phenylalanine, since the code is degenerate (d). "
    "The sequence in (e) is the coding strand; the template, written 5'→3', is 5'-TTAGAATGCCAT-3' (e false).",
    ["mRNA: AUG GCA UUC UAA", "Met–Ala–Phe", "Deletion → frameshift", "UUC → UUU: same amino acid"],
    C12_MB("genetic code; mutations and genetic code; translation"),
    why="(c) ignores the frameshift caused by a single-base deletion; (e) gives the coding strand, not the "
        "template.",
    seconds=90)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "assertion_reason",
    ar("DNA fingerprinting uses repetitive (satellite) DNA rather than the protein-coding sequences.",
       "Satellite DNA sequences show a high degree of polymorphism among individuals."),
    AR("A"),
    "Why satellite DNA is used in fingerprinting",
    "NCERT: DNA fingerprinting involves identifying differences in some specific regions of the DNA sequence "
    "called repetitive DNA. Satellite DNA sequences normally do not code for any proteins, but they form a large "
    "portion of the human genome and show a high degree of polymorphism, which forms the basis of DNA "
    "fingerprinting. Since 99.9 per cent of the bases are the same in all people, it is the highly polymorphic "
    "regions that can tell individuals apart: R explains A.",
    ["Goal: tell individuals apart", "Need highly variable DNA", "Satellite DNA is highly polymorphic → R explains "
     "A"],
    C12_MB("DNA fingerprinting"),
    seconds=40)

_mols = [("H", "H")]
for _gen in range(1, 6):
    _mols = [m for (a, b) in _mols for m in ((a, "L"), (b, "L"))]
    assert sum(1 for m in _mols if "H" in m) == 2 and ("H", "H") not in _mols

add(MBI, "Replication", "Advanced", "statement_pair",
    "One DNA molecule of E. coli fully labelled with ¹⁵N (both strands heavy) replicates semiconservatively for "
    "several generations in a medium containing only ¹⁴NH₄Cl.\n\n" +
    sp("After any number of generations (one or more), exactly two of the descendant molecules are hybrid "
       "(¹⁵N/¹⁴N), and all the others are light.",
       "Heavy (¹⁵N/¹⁵N) DNA reappears after the third generation in the ¹⁴N medium."),
    SP("C"),
    "Fate of parental strands in semiconservative replication",
    "In semiconservative replication the two parental heavy strands are never broken or lost; in each generation "
    "each one is paired with a new light strand. So after every generation exactly two molecules are hybrid and "
    "the rest are ¹⁴N/¹⁴N (Statement I true): e.g. 2 of 4 after two generations, 2 of 8 after three. A heavy/heavy "
    "molecule needs two ¹⁵N strands together, which cannot form in a medium supplying only ¹⁴N (Statement II "
    "false).",
    ["Two parental strands persist, each in a hybrid", "Hybrid count stays 2; light molecules increase",
     "No new ¹⁵N strands → no heavy DNA"],
    C12_MB("replication: the experimental proof"),
    seconds=60, verified_by=RECOMPUTED)

_aa = 150
assert 3 * _aa + 3 == 453 and _aa - 1 == 149

add(MBI, "Genetic code and translation", "Advanced", "direct",
    "A polypeptide of 150 amino acids is translated from an mRNA. What is the minimum length of the mRNA region "
    "from the first base of the start codon to the last base of the stop codon, and how many peptide bonds does "
    "the polypeptide contain?",
    P("453 nucleotides; 149 peptide bonds",
      ["450 nucleotides; 150 peptide bonds", "453 nucleotides; 150 peptide bonds", "450 nucleotides; 149 peptide "
       "bonds"], "C"),
    "Codons, stop codon and peptide bonds",
    "Each amino acid needs one triplet codon (the start codon AUG codes for the first methionine): 150 × 3 = 450 "
    "nucleotides. The stop codon codes for no amino acid but is part of the reading frame: + 3 = 453. A linear "
    "chain of n amino acids has n − 1 peptide bonds: 149.",
    ["150 codons × 3 = 450", "+ stop codon 3 = 453", "Peptide bonds = 150 − 1 = 149"],
    C12_MB("genetic code; translation"),
    why="450 forgets the stop codon; 150 peptide bonds counts one bond per amino acid instead of n − 1.",
    seconds=50, verified_by=RECOMPUTED)

add(MBI, "DNA as genetic material", "Advanced", "multi_statement",
    ms("Suppose Hershey and Chase had used bacteriophages labelled with both radioactive phosphorus (in DNA) and "
       "radioactive sulphur (in protein) to infect bacteria, followed by blending and centrifugation. Which "
       "results are expected?",
       ["The bacterial cells in the pellet would carry radioactive phosphorus.",
        "Radioactive sulphur would be found mainly in the supernatant.",
        "Blending would separate the viral coats from the bacteria.",
        "Radioactive sulphur would be found inside the bacterial cells.",
        "The result would show that protein is the genetic material."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "d", "e"], ["b", "c", "e"]], "D"),
    "Predicting a double-label Hershey–Chase experiment",
    "Only phage DNA enters the bacterium; the protein coat stays outside. Blending removes the viral coats from "
    "the bacteria (c), and centrifugation separates the light viral particles (supernatant, carrying ³⁵S protein) "
    "from the heavier bacteria (pellet, carrying ³²P DNA) (a, b). Sulphur-labelled protein does not enter (d "
    "false), so the result shows that DNA, not protein, is the genetic material (e false).",
    ["DNA (³²P) enters → pellet", "Protein coat (³⁵S) stays out → supernatant", "DNA is the genetic material"],
    C12_MB("the search for genetic material"),
    why="Options with (d) or (e) contradict the experiment's key finding that protein does not enter the cell.",
    seconds=60)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "match_list",
    ml(("change in DNA or in the cell cycle", "consequence"),
       ["A mutation in non-coding repetitive DNA that does not affect reproductive ability",
        "Change of the sixth codon of the β-globin gene from GAG to GUG",
        "Insertion of a single base within the coding region of a gene",
        "Failure of cell division after DNA replication"],
       ["Polyploidy", "Shift of the reading frame from the point of insertion",
        "Glutamic acid replaced by valine in the β-globin chain", "Accumulation over generations, giving DNA "
        "polymorphism"]),
    M(mc("IV,III,II,I"), [mc("IV,II,III,I"), mc("I,III,II,IV"), mc("III,IV,II,I")], "D"),
    "Consequences of changes in DNA",
    "Mutations in non-coding DNA may have no immediate effect on reproductive ability, so they accumulate "
    "generation after generation, one cause of DNA polymorphism (A-IV). GAG→GUG at the sixth codon of β-globin "
    "replaces glutamic acid by valine, causing sickle-cell anaemia (B-III). A single-base insertion shifts the "
    "reading frame (C-II). NCERT: a failure in cell division after DNA replication results in polyploidy (D-I).",
    ["A → IV", "B → III", "C → II", "D → I"],
    C12_MB("DNA fingerprinting; mutations and genetic code; replication"),
    why="The other codes swap the substitution with the frameshift, or polyploidy with polymorphism.",
    seconds=55)

add(MBI, "Replication", "Advanced", "multi_statement",
    ms("Which of the following statements about events at a replication fork are correct?",
       ["On the template strand with 3'→5' polarity, the new strand is synthesised continuously.",
        "On the template strand with 5'→3' polarity, the new strand is synthesised discontinuously.",
        "The discontinuously synthesised fragments are later joined by DNA ligase.",
        "DNA polymerase can initiate replication at any random place in the DNA.",
        "The new strands are polymerised in the 3'→5' direction."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Continuous and discontinuous synthesis",
    "NCERT: DNA-dependent DNA polymerases catalyse polymerisation only in the 5'→3' direction. Consequently, on "
    "the template with 3'→5' polarity replication is continuous (a), while on the template with 5'→3' polarity it "
    "is discontinuous (b); the fragments are joined by DNA ligase (c). Replication does not start randomly: it "
    "begins at a definite region, the origin of replication (d false). Polymerisation is 5'→3', not 3'→5' (e "
    "false).",
    ["5'→3' polymerisation only", "3'→5' template: continuous; 5'→3' template: discontinuous", "Ligase joins "
     "fragments; start at origin"],
    C12_MB("replication: the machinery and the enzymes"),
    why="Options with (d) or (e) contain a false statement.",
    seconds=50)
