
# ================================================================ Principles of Inheritance and Variation (7 / 10 / 7)
C12_PI = lambda s: ref(12, PIV, s)

add(PIV, "Linkage and crossing over", "Basic", "direct",
    "Alfred Sturtevant used the frequency of recombination between gene pairs on the same chromosome to 'map' "
    "their positions. According to NCERT, such genetic maps are used today:",
    P("Extensively, as a starting point in the sequencing of whole genomes, as was done in the Human Genome "
      "Sequencing Project",
      ["Only to predict the sex of the offspring in Drosophila", "To count the number of chromosomes in a "
       "karyotype", "Only to identify the dominant allele of each gene pair"], "B"),
    "Use of genetic maps",
    "NCERT: Sturtevant used the frequency of recombination between gene pairs on the same chromosome as a measure "
    "of the distance between genes and 'mapped' their position on the chromosome. Today genetic maps are "
    "extensively used as a starting point in the sequencing of whole genomes, as was done in the case of the Human "
    "Genome Sequencing Project.",
    ["Recombination frequency → distance between genes", "Genetic map of gene positions", "Starting point for "
     "whole-genome sequencing (HGP)"],
    C12_PI("chromosomal theory of inheritance: linkage and recombination"),
    why="A map of gene positions is not used to predict sex, count chromosomes or decide dominance.",
    seconds=25)

_n_f = 24
_n_m = _n_f - 1
_sperm = sorted({(_n_f - 2) // 2 + 1, (_n_f - 2) // 2})
assert (_n_m, _sperm) == (23, [11, 12])

add(PIV, "Sex determination", "Basic", "numerical",
    "In a grasshopper species, the somatic cells of the female have 24 chromosomes. Sex is determined by the XO "
    "mechanism. How many chromosomes are present in a somatic cell of the male, and in the two kinds of sperm it "
    "produces?",
    P("23; sperms with 12 and with 11 chromosomes",
      ["24; sperms with 12 and with 12 chromosomes", "23; all sperms with 12 chromosomes",
       "22; sperms with 11 and with 11 chromosomes"], "D"),
    "XO type of sex determination",
    "In the XO type (grasshopper), females have a pair of X chromosomes and males have only one X besides the "
    "autosomes. Female: 22 autosomes + XX = 24, so the male has 22 + X = 23. In meiosis, each sperm receives 11 "
    "autosomes; half the sperms also receive the X (12 chromosomes) and half do not (11 chromosomes).",
    ["Female 24 = 22A + XX", "Male = 22A + X = 23", "Sperms: 11A + X = 12, or 11A = 11"],
    C12_PI("sex determination"),
    why="24 would give the male two sex chromosomes (not XO); 'all 12' forgets the sperms without an X; 22 removes "
        "the X altogether.",
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "assertion_reason",
    ar("In phenylketonuria, phenylpyruvic acid and other derivatives of phenylalanine are excreted through urine.",
       "These derivatives are poorly absorbed by the kidney."),
    AR("A"),
    "Why phenylpyruvic acid appears in urine",
    "NCERT: in phenylketonuria the affected individual lacks an enzyme that converts phenylalanine into tyrosine, "
    "so phenylalanine accumulates and is converted into phenylpyruvic acid and other derivatives. Their accumulation "
    "in the brain causes mental retardation. They are also excreted through urine because of their poor absorption "
    "by the kidney. R is the reason NCERT gives for A.",
    ["A: true", "R: true (poor absorption by the kidney)", "R is the stated cause of A"],
    C12_PI("genetic disorders: Mendelian disorders (phenylketonuria)"),
    seconds=30)

add(PIV, "Mendelian inheritance", "Basic", "statement_pair",
    sp("During Mendel's investigations into inheritance patterns, statistical analysis and mathematical logic were "
       "applied to problems in biology for the first time.",
       "The confirmation of Mendel's inferences from experiments on successive generations of his test plants "
       "showed that his results pointed to general rules of inheritance rather than unsubstantiated ideas."),
    SP("A"),
    "What made Mendel's work scientific",
    "NCERT: it was during Mendel's investigations into inheritance patterns that, for the first time, statistical "
    "analysis and mathematical logic were applied to problems in biology (Statement I true). His experiments had a "
    "large sampling size, and the confirmation of his inferences from experiments on successive generations of his "
    "test plants proved that his results pointed to general rules of inheritance rather than unsubstantiated ideas "
    "(Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_PI("Mendel's laws of inheritance"),
    seconds=30)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Among the seven pairs of contrasting traits studied by Mendel in pea, which option gives the recessive traits "
    "for pod shape and pod colour, respectively?",
    P("Constricted and yellow", ["Inflated and green", "Constricted and green", "Inflated and yellow"], "B"),
    "Mendel's contrasting traits in pea",
    "In NCERT's table of the seven characters, pod shape is inflated (dominant) or constricted (recessive), and pod "
    "colour is green (dominant) or yellow (recessive). Note the trap: for pod colour green is dominant, whereas for "
    "seed colour yellow is dominant.",
    ["Pod shape: inflated > constricted", "Pod colour: green > yellow", "Recessive: constricted, yellow"],
    C12_PI("inheritance of one gene"),
    why="Inflated and green are the dominant traits; 'constricted and green' and 'inflated and yellow' each pair one "
        "dominant trait with one recessive trait.",
    seconds=25)

add(PIV, "Mendelian inheritance", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Phenotype", "Genotype", "Homozygous", "Monohybrid cross"],
       ["A cross between parents that differ in one character", "Having two identical alleles of a gene, as TT or tt",
        "Observable expression of a character, such as tall or dwarf", "Genetic constitution, such as TT, Tt or tt"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("II,IV,III,I")], "D"),
    "Basic terms of Mendelian genetics",
    "Phenotype is the observable expression of a character (tall, dwarf) (A-III); genotype is the genetic make-up "
    "(TT, Tt, tt) (B-IV); a homozygous individual has two identical alleles, TT or tt (C-II); a monohybrid cross "
    "involves parents differing in one character, such as Mendel's tall × dwarf cross (D-I).",
    ["A → III", "B → IV", "C → II", "D → I"],
    C12_PI("inheritance of one gene"),
    why="The other codes swap phenotype with genotype, homozygous with monohybrid cross, or phenotype with "
        "homozygous.",
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "Which of the following is described in NCERT as a feature of individuals with Down's syndrome?",
    P("Retarded physical, psychomotor and mental development",
      ["Development of breasts (gynaecomastia) in an individual with overall masculine development",
       "Rudimentary ovaries in a sterile female", "Non-stop bleeding from a simple cut"], "C"),
    "Features of Down's syndrome",
    "NCERT: Down's syndrome is caused by an additional copy of chromosome 21. The affected individual is short "
    "statured with a small round head, furrowed tongue and partially open mouth; the palm is broad with a "
    "characteristic palm crease; and physical, psychomotor and mental development is retarded.",
    ["Trisomy 21", "Physical features listed in NCERT", "Physical, psychomotor and mental development retarded"],
    C12_PI("genetic disorders: chromosomal disorders"),
    why="Gynaecomastia belongs to Klinefelter's syndrome, rudimentary ovaries to Turner's syndrome and non-stop "
        "bleeding to haemophilia.",
    seconds=25)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "match_list",
    ml(("fertilisation event", "result"),
       ["An egg with 22 autosomes + XX fertilised by a sperm with 22 autosomes + Y",
        "An egg with 22 autosomes and no sex chromosome fertilised by a sperm with 22 autosomes + X",
        "An egg with 23 autosomes (an extra chromosome 21) + X fertilised by a sperm with 22 autosomes + Y",
        "An egg with 22 autosomes + X fertilised by a sperm with 22 autosomes + Y"],
       ["Normal male (46, XY)", "Male with Down's syndrome (47 chromosomes)", "Turner's syndrome (45, X0)",
        "Klinefelter's syndrome (47, XXY)"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,III,I,II"), mc("II,III,IV,I")], "B"),
    "Aneuploid gametes and the resulting disorders",
    "Failure of segregation of chromatids (aneuploidy) can give eggs with an extra or a missing chromosome. "
    "A: 44 + XXY = 47, Klinefelter's syndrome (IV). B: 44 + X = 45, X0, Turner's syndrome (III). C: an extra "
    "chromosome 21 gives trisomy 21 with XY, a male with Down's syndrome, 47 chromosomes (II). D: normal gametes "
    "give 46, XY (I).",
    ["Count autosomes and sex chromosomes in the zygote", "XXY → Klinefelter's; X0 → Turner's",
     "Trisomy 21 → Down's; 44 + XY → normal male"],
    C12_PI("genetic disorders: chromosomal disorders; mutation (aneuploidy)"),
    why="The other codes swap Klinefelter's with Turner's, Down's with the normal male, or Down's with "
        "Klinefelter's.",
    seconds=50)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "assertion_reason",
    ar("A man with blood group O cannot be the biological father of a child with blood group AB.",
       "The allele i is dominant over both Iᴬ and Iᴮ."),
    AR("C"),
    "ABO alleles and paternity",
    "A child with blood group AB (IᴬIᴮ) must receive Iᴬ from one parent and Iᴮ from the other. A man with blood "
    "group O is ii and can pass on only i, so he cannot be the father: A is true. R is false: Iᴬ and Iᴮ are "
    "co-dominant with each other and both are dominant over i; i is recessive and produces no sugar.",
    ["AB child = IᴬIᴮ", "O father = ii → can give only i", "i is recessive, not dominant → R false"],
    C12_PI("inheritance of one gene: co-dominance and multiple alleles"),
    seconds=35)

add(PIV, "Sex determination", "Intermediate", "statement_pair",
    sp("In both the XO and the XY types of sex determination, the males produce two different kinds of sperms with "
       "respect to the sex chromosomes.",
       "In the ZW type of sex determination seen in birds, it is the male that produces two different kinds of "
       "gametes."),
    SP("C"),
    "Male and female heterogamety",
    "In the XO type (grasshopper), males produce sperms with an X and sperms without it; in the XY type (Drosophila, "
    "humans), males produce X-bearing and Y-bearing sperms. In both, the male is heterogametic (Statement I true). "
    "In birds the female is heterogametic (ZW) and produces two kinds of eggs, Z-bearing and W-bearing, while the "
    "male (ZZ) produces one kind of sperm (Statement II false).",
    ["XO and XY: male heterogamety → I true", "ZW: female heterogamety → II false"],
    C12_PI("sex determination"),
    seconds=35)

_f3_dwarf = F(2, 3) * F(1, 4)
assert _f3_dwarf == F(1, 6)

add(PIV, "Mendelian inheritance", "Intermediate", "numerical",
    "True-breeding tall (TT) and dwarf (tt) pea plants are crossed and the F1 is self-pollinated. All the tall F2 "
    "plants are then self-pollinated, each tall plant contributing an equal number of progeny. What fraction of the "
    "F3 progeny raised from them will be dwarf?",
    P("1/6", ["1/4", "1/3", "1/8"], "C"),
    "Selfing the dominant class of F2",
    "Tall F2 plants are TT and Tt in the ratio 1 : 2, i.e. 1/3 TT and 2/3 Tt. TT plants give only tall progeny; Tt "
    "plants give 1/4 dwarf. Fraction dwarf in F3 = 2/3 × 1/4 = 1/6.",
    ["Tall F2: 1/3 TT, 2/3 Tt", "Dwarf only from Tt: 1/4 of its progeny", "2/3 × 1/4 = 1/6"],
    C12_PI("inheritance of one gene"),
    why="1/4 assumes every tall F2 plant is Tt; 1/3 is the fraction of tall F2 plants that are TT; 1/8 wrongly "
        "takes half the tall plants as Tt.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Linkage and crossing over", "Intermediate", "multi_statement",
    ms("Which of the following statements linking Mendel's laws with the behaviour of chromosomes are correct?",
       ["Segregation of the two alleles of a gene can be explained by the separation of the pair of homologous "
        "chromosomes carrying them during gamete formation.",
        "Independent assortment of two genes can be explained by the independent segregation of two different "
        "pairs of chromosomes carrying them.",
        "Two genes that are very tightly linked on the same chromosome do not assort independently, and parental "
        "combinations predominate among the progeny.",
        "A gamete receives both chromosomes of each homologous pair.",
        "The law of independent assortment applies to every pair of genes, whatever their location."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "D"),
    "Chromosomal basis of Mendel's laws",
    "Sutton and Boveri argued that the pairing and separation of a pair of chromosomes would lead to the "
    "segregation of the pair of factors they carried (a). In NCERT's comparison of chromosomes and genes, "
    "independent pairs segregate independently of each other, which explains independent assortment (b). Morgan "
    "found that genes on the same chromosome, especially tightly linked ones, give mostly parental combinations, so "
    "they do not assort independently (c). Only one chromosome of each pair goes to a gamete (d false), and linkage "
    "shows that independent assortment does not apply to every gene pair (e false).",
    ["(a) segregation ↔ homologues separating", "(b) assortment ↔ independent pairs", "(c) linkage exception",
     "(d), (e) false"],
    C12_PI("chromosomal theory of inheritance; linkage and recombination"),
    why="Options with (d) or (e) include a false statement; '(b), (c) and (d)' also leaves out (a).",
    seconds=50)

add(PIV, "Sex-linked inheritance", "Intermediate", "multi_statement",
    ms("A woman with normal vision is heterozygous (a carrier) for red-green colour blindness. Which of the "
       "following statements are correct?",
       ["Her vision is normal because the effect of the recessive allele is suppressed by her matching dominant "
        "normal allele.",
        "Each of her sons has a 50 per cent chance of being colour blind.",
        "She may have received the allele for colour blindness from either her mother or her father.",
        "All her daughters will necessarily be carriers.",
        "Her father must be colour blind."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "b", "e"], ["c", "d", "e"]], "B"),
    "A carrier of colour blindness",
    "Colour blindness is a sex-linked recessive disorder due to a mutation in a gene on the X chromosome. NCERT: "
    "the son of a woman who carries the gene has a 50 per cent chance of being colour blind; the mother is not "
    "herself colour blind because the gene is recessive, its effect being suppressed by her matching dominant "
    "normal gene (a, b). She has two X chromosomes, one from each parent, so the allele could have come from "
    "either a carrier mother or a colour-blind father (c), and her father need not be colour blind (e false). Each "
    "daughter receives one of her two X chromosomes, so a daughter is not necessarily a carrier (d false).",
    ["Recessive allele masked → normal vision (a)", "Son: 50% chance (b)", "Allele from either parent (c)",
     "(d), (e) need not be true"],
    C12_PI("sex-linked inheritance: colour blindness"),
    why="(d) ignores that each daughter has a 1/2 chance of receiving the normal X; (e) ignores a carrier mother as "
        "the source.",
    seconds=50)

_snap = {"RR x rr": Counter({"pink": 4}), "Rr x Rr": Counter({"red": 1, "pink": 2, "white": 1}),
         "Rr x rr": Counter({"pink": 2, "white": 2}), "Rr x RR": Counter({"red": 2, "pink": 2})}
_col = {"RR": "red", "Rr": "pink", "rr": "white"}
for _k, _v in _snap.items():
    _a, _b = _k.split(" x ")
    _got = Counter(_col["".join(sorted(x + y))] for x in _a for y in _b)
    assert _got == _v, (_k, _got)

add(PIV, "Incomplete and co-dominance", "Intermediate", "match_list",
    "In snapdragon, flower colour shows incomplete dominance: RR is red, Rr is pink and rr is white.\n\n" +
    ml(("cross", "flower colours among the progeny"),
       ["RR × rr", "Rr × Rr", "Rr × rr", "Rr × RR"],
       ["1 red : 1 pink", "All pink", "1 pink : 1 white", "1 red : 2 pink : 1 white"]),
    M(mc("II,IV,III,I"), [mc("II,IV,I,III"), mc("IV,II,III,I"), mc("II,III,IV,I")], "D"),
    "Crosses under incomplete dominance",
    "With incomplete dominance every genotype has its own phenotype, so phenotypic ratios equal genotypic ratios. "
    "RR × rr gives only Rr: all pink (A-II). Rr × Rr gives RR : Rr : rr = 1 : 2 : 1, i.e. 1 red : 2 pink : 1 white "
    "(B-IV). Rr × rr gives Rr : rr = 1 pink : 1 white (C-III). Rr × RR gives RR : Rr = 1 red : 1 pink (D-I).",
    ["Phenotype ratio = genotype ratio", "Work each cross with gametes", "A-II, B-IV, C-III, D-I"],
    C12_PI("inheritance of one gene: incomplete dominance"),
    why="The other codes swap the two back-crosses (with RR and with rr) or the F1 cross with the F2 cross.",
    seconds=50, verified_by=RECOMPUTED)

add(PIV, "Sex determination", "Intermediate", "assertion_reason",
    ar("In humans, the female produces two kinds of eggs, X-bearing and Y-bearing.",
       "Human females are homogametic, with two X chromosomes."),
    AR("D"),
    "Homogametic human female",
    "Human females have a pair of X chromosomes (XX), so every egg receives an X besides 22 autosomes; there are "
    "no Y-bearing eggs (A false). R is true: having two sex chromosomes of the same type, the female is "
    "homogametic. It is the male (XY) that produces two kinds of sperms, X-bearing and Y-bearing, so the sex of the "
    "child is decided by the sperm.",
    ["Female XX → all eggs carry X → A false", "R: true (homogametic female)"],
    C12_PI("sex determination: sex determination in humans"),
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "statement_pair",
    sp("α-Thalassemia is observed due to mutation or deletion of one or more of the four genes HBA1 and HBA2 "
       "(two on chromosome 16 from each parent); the more genes affected, the fewer α-globin molecules are "
       "produced.",
       "β-Thalassemia is controlled by a single gene, HBB, on chromosome 11 of each parent and occurs due to "
       "mutation of one or both the genes."),
    SP("A"),
    "Genetic basis of α- and β-thalassemia",
    "NCERT: α-thalassemia is controlled by two closely linked genes, HBA1 and HBA2, on chromosome 16 of each "
    "parent, and is observed due to mutation or deletion of one or more of the four genes; the more genes "
    "affected, the less α-globin is produced (Statement I true). β-Thalassemia is controlled by a single gene, "
    "HBB, on chromosome 11 of each parent and occurs due to mutation of one or both the genes (Statement II true).",
    ["α: HBA1 + HBA2 on chr 16 × 2 parents = 4 genes", "β: HBB on chr 11 × 2 parents = 2 genes", "Both true"],
    C12_PI("genetic disorders: Mendelian disorders (thalassemia)"),
    seconds=40)

add(PIV, "Sex determination", "Intermediate", "direct",
    "Henking traced a specific nuclear structure through spermatogenesis in a few insects and named it the 'X "
    "body'. What did further investigations by other scientists conclude about it?",
    P("The 'X body' was in fact a chromosome, which is why it was given the name X chromosome",
      ["The 'X body' was a cytoplasmic granule unrelated to sex", "The 'X body' was the nucleolus of the "
       "spermatocyte", "The 'X body' was a Y chromosome that had lost its genes"], "A"),
    "From Henking's X body to the X chromosome",
    "NCERT: Henking (1891) observed that 50 per cent of the sperm received the X body after spermatogenesis and "
    "the other 50 per cent did not, but he could not explain its significance. Further investigations by other "
    "scientists led to the conclusion that the 'X body' was in fact a chromosome, and that is why it was given the "
    "name X chromosome.",
    ["Henking: 'X body', significance unexplained", "Later work: it is a chromosome", "Hence 'X chromosome'"],
    C12_PI("sex determination"),
    why="The structure was shown to be a chromosome, not a cytoplasmic granule, a nucleolus or a Y chromosome.",
    seconds=25)

_rf = F(20, 100)
_ab_gamete = (1 - _rf) / 2
assert _ab_gamete ** 2 == F(16, 100) and (_rf / 2) ** 2 == F(1, 100)

add(PIV, "Linkage and crossing over", "Advanced", "numerical",
    "Genes A and B lie on the same chromosome, and the frequency of recombination between them is 20 per cent. A "
    "plant that received AB from one parent and ab from the other is self-pollinated. Assume the same "
    "recombination frequency in male and female gamete formation. What percentage of the progeny is expected to "
    "be aabb?",
    P("16 per cent", ["1 per cent", "4 per cent", "6.25 per cent"], "B"),
    "Gamete frequencies of a linked dihybrid",
    "With AB/ab and 20 per cent recombination, the gametes are parental AB 40 per cent and ab 40 per cent, and "
    "recombinant Ab 10 per cent and aB 10 per cent. An aabb plant needs an ab gamete from each parent: "
    "0.40 × 0.40 = 0.16, i.e. 16 per cent.",
    ["Parental gametes: (100 − 20)/2 = 40% each", "Recombinant gametes: 10% each", "aabb = 0.4 × 0.4 = 16%"],
    C12_PI("chromosomal theory of inheritance: linkage and recombination"),
    why="1 per cent would apply if ab were a recombinant gamete (parents Ab/aB); 4 per cent squares the "
        "recombination frequency; 6.25 per cent (1/16) assumes independent assortment.",
    seconds=90, verified_by=RECOMPUTED)

_dark = Counter()
for _alleles in product((0, 1), repeat=6):         # each of six alleles in AaBbCc x AaBbCc dominant or not
    _dark[sum(_alleles)] += F(1, 64)
assert _dark[5] + _dark[6] == F(7, 64) and _dark[4] == F(15, 64)

add(PIV, "Polygenic inheritance", "Advanced", "numerical",
    "Suppose a polygenic trait is controlled by three genes A, B and C, and each dominant allele adds an equal "
    "amount to the phenotype. Plants AABBcc and aabbCC are crossed, and the F1 is self-pollinated. What fraction "
    "of the F2 will show a phenotype beyond (more extreme than) that of the parent with more dominant alleles?",
    P("7/64", ["1/64", "15/64", "11/32"], "C"),
    "Polygenic F2 can exceed the parental range",
    "The parents have 4 (AABBcc) and 2 (aabbCC) dominant alleles. The F1 is AaBbCc (3 dominant alleles). In its "
    "F2, the number of dominant alleles ranges from 0 to 6, with frequencies 1, 6, 15, 20, 15, 6, 1 (out of 64). "
    "More than 4 dominant alleles: 6/64 (five) + 1/64 (six) = 7/64.",
    ["Parents: 4 and 2 dominant alleles", "F2 classes 0–6: 1 : 6 : 15 : 20 : 15 : 6 : 1 (/64)", "Five or six: "
     "(6 + 1)/64 = 7/64"],
    C12_PI("polygenic inheritance"),
    why="1/64 counts only AABBCC; 15/64 is the class equal to the darker parent; 11/32 (22/64) includes that "
        "equal class as well.",
    seconds=100, verified_by=RECOMPUTED)

assert F(1, 2) * F(1, 2) == F(1, 4)

add(PIV, "Sex-linked inheritance", "Advanced", "multi_statement",
    ms("A man with normal colour vision and blood group AB marries a colour-blind woman with blood group O. "
       "Which of the following statements about their children are correct?",
       ["All their sons will be colour blind.",
        "None of their children will have blood group O or blood group AB.",
        "All their daughters will have normal vision but will be carriers of colour blindness.",
        "The probability that their first child is a colour-blind son with blood group A is 1/4.",
        "Half of their daughters will be colour blind."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "A"),
    "Combining an X-linked and an autosomal gene",
    "Colour vision: mother XᶜXᶜ, father XY (normal). Every son gets Xᶜ from his mother and Y from his father: "
    "colour blind (a). Every daughter gets Xᶜ from her mother and the normal X from her father: normal vision, "
    "carrier (c), so no daughter is colour blind (e false). Blood group: IᴬIᴮ × ii gives Iᴬi (A) or Iᴮi (B), each "
    "1/2, never O or AB (b). First child a son (1/2, and then certainly colour blind) with blood group A (1/2): "
    "1/2 × 1/2 = 1/4 (d).",
    ["Sons: all colour blind; daughters: all carriers", "Blood groups: A or B, 1/2 each",
     "P(colour-blind son with A) = 1/2 × 1/2 = 1/4"],
    C12_PI("sex-linked inheritance; co-dominance and multiple alleles"),
    why="'(a), (b) and (c) only' leaves out the true probability in (d); options with (e) are wrong because every "
        "daughter receives the father's normal X.",
    seconds=90, verified_by=RECOMPUTED)

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "assertion_reason",
    ar("Among the children of a man of genotype Iᴬi and a woman of genotype Iᴮi, all four blood groups, A, B, AB "
       "and O, are expected in equal proportions.",
       "Each parent forms its two kinds of gametes in equal numbers; Iᴬ and Iᴮ are co-dominant while both are "
       "dominant over i, so the four equally likely genotypes IᴬIᴮ, Iᴬi, Iᴮi and ii each give a different blood "
       "group."),
    AR("A"),
    "All four ABO phenotypes from one couple",
    "Gametes: Iᴬ and i (1/2 each) from the father, Iᴮ and i (1/2 each) from the mother. The four combinations "
    "IᴬIᴮ, Iᴬi, Iᴮi and ii are each 1/4. Because of co-dominance (IᴬIᴮ → AB) and the recessiveness of i "
    "(Iᴬi → A, Iᴮi → B, ii → O), each genotype gives a different phenotype, so the four blood groups appear in a "
    "1 : 1 : 1 : 1 ratio. R is exactly the reason for A.",
    ["Gametes 1 : 1 from each parent", "Four genotypes, 1/4 each", "Each genotype → a distinct blood group"],
    C12_PI("inheritance of one gene: co-dominance and multiple alleles"),
    seconds=50)

add(PIV, "Sex-linked inheritance", "Advanced", "direct",
    "A couple with normal colour vision has a son with Klinefelter's syndrome (XXY) who is red-green colour blind. "
    "Assuming no new mutation, which explanation fits these facts?",
    P("The mother is a carrier, and an egg carrying two X chromosomes, both with the colour-blindness allele, was "
      "fertilised by a Y-bearing sperm",
      ["A sperm carrying both the X and the Y chromosome of the father fertilised a normal egg carrying the "
       "colour-blindness allele",
       "An egg with no sex chromosome was fertilised by a sperm carrying both the X and the Y chromosome of the "
       "father",
       "The father is a carrier of colour blindness and passed the allele to his son on the Y chromosome"], "B"),
    "Tracing an extra X chromosome with an X-linked marker",
    "Colour blindness is X-linked recessive, so an XXY son is colour blind only if both his X chromosomes carry "
    "the allele. The father has normal vision, so his X carries the normal allele; any X from him would make the "
    "son see normally. Both X chromosomes must therefore come from the mother, who must be a carrier (she sees "
    "normally); her egg had two X chromosomes (failure of segregation, aneuploidy) and was fertilised by a "
    "Y-bearing sperm.",
    ["Son needs the allele on both X chromosomes", "Father's X is normal → neither X came from him",
     "Both X from a carrier mother + Y from father"],
    C12_PI("sex-linked inheritance; chromosomal disorders"),
    why="Any option in which the son receives his father's X gives him a normal allele; a male cannot be a "
        "carrier, and the gene is not on the Y chromosome.",
    seconds=90)

_tc = {"unlinked": F(1, 4), "coupling RF 20%": (1 - F(20, 100)) / 2, "repulsion RF 20%": F(20, 100) / 2,
       "complete linkage": F(1, 2)}
assert list(_tc.values()) == [F(1, 4), F(2, 5), F(1, 10), F(1, 2)]

add(PIV, "Linkage and crossing over", "Advanced", "match_list",
    "Each dihybrid in List-I is test-crossed with aabb.\n\n" +
    ml(("dihybrid test-crossed with aabb", "expected fraction of aabb progeny"),
       ["AaBb, with the two genes on different chromosomes",
        "A dihybrid that received AB from one parent and ab from the other, with 20 per cent recombination",
        "A dihybrid that received Ab from one parent and aB from the other, with 20 per cent recombination",
        "A dihybrid that received AB from one parent and ab from the other, with genes so tightly linked that no "
        "recombination occurs"],
       ["1/2", "1/4", "1/10", "2/5"]),
    M(mc("II,IV,III,I"), [mc("II,III,IV,I"), mc("I,IV,III,II"), mc("II,IV,I,III")], "C"),
    "Test-cross outcomes with and without linkage",
    "In a test cross, the fraction of aabb progeny equals the fraction of ab gametes of the dihybrid. Independent "
    "genes: 1/4 (A-II). AB/ab with 20 per cent recombination: ab is parental, (1 − 0.2)/2 = 0.4 = 2/5 (B-IV). "
    "Ab/aB with 20 per cent recombination: ab is recombinant, 0.2/2 = 0.1 = 1/10 (C-III). Complete linkage of "
    "AB/ab: only AB and ab gametes, 1/2 (D-I).",
    ["aabb fraction = ab gamete fraction", "Parental class: (1 − RF)/2; recombinant: RF/2",
     "A-II, B-IV, C-III, D-I"],
    C12_PI("chromosomal theory of inheritance: linkage and recombination"),
    why="The other codes confuse the coupling (AB/ab) and repulsion (Ab/aB) arrangements, or treat complete "
        "linkage as independent assortment.",
    seconds=100, verified_by=RECOMPUTED)

_chicken = 78
assert _chicken // 2 == 39 and _chicken - 2 == 76

add(PIV, "Sex determination", "Advanced", "multi_statement",
    ms("In a bird species, the somatic cells of both sexes have 78 chromosomes. Which of the following statements "
       "are correct?",
       ["The hen produces two kinds of eggs, each with 39 chromosomes: one kind carries a Z chromosome and the "
        "other a W chromosome.",
        "The cock produces only one kind of sperm with respect to the sex chromosomes.",
        "The sex of a chick is decided by the kind of egg that is fertilised.",
        "The somatic cells of the hen have 77 chromosomes, because she has only one Z chromosome.",
        "Each sperm of the cock carries 38 autosomes and a W chromosome."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
    "Female heterogamety in birds",
    "In birds the female is ZW and the male ZZ, so both sexes have the same number of chromosomes, 76 autosomes + "
    "2 sex chromosomes = 78 (d false). The hen gives eggs with 38 autosomes + Z or 38 autosomes + W, 39 each (a). "
    "The cock gives only sperms with 38 autosomes + Z (b); it has no W (e false). Since the egg type varies and "
    "the sperm does not, the egg decides the sex of the chick (c).",
    ["Hen ZW, cock ZZ: 78 in both", "Eggs: 38 + Z or 38 + W", "Sperms: 38 + Z only → egg decides sex"],
    C12_PI("sex determination"),
    why="(d) treats the ZW female like an XO male; (e) gives the male a W chromosome, which only females carry.",
    seconds=60, verified_by=RECOMPUTED)
