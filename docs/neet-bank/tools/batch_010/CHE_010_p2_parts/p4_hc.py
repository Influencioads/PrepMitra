
# ================================================================ Hydrocarbons (2416-2431)
# 2416: C6H6 + SO3 (oleum) -> C6H5SO3H; 7.8 g benzene
M_bz = mm(C=6, H=6)
M_bsa = mm(C=6, H=6, S=1, O=3)
assert (M_bz, M_bsa) == (78, 158)
m_2416 = F(78, 10) / M_bz * M_bsa
assert m_2416 == F(158, 10)
v_2416 = "15.8 g"
assert F(1, 10) * mm(S=1, O=3) == 8 and F(1, 10) * mm(C=6, H=6, S=2, O=6) == F(238, 10)
# 2421: BrCH2CH2Br + Zn -> CH2=CH2 + ZnBr2; 18.8 g
M_dbe = mm(C=2, H=4, Br=2)
assert M_dbe == 188
V_2421 = F(188, 10) / M_dbe * F(224, 10)
assert V_2421 == F(224, 100)
v_2421 = "2.24 L"
# 2422: 0.10 mol CH4 -> 0.05 mol CH3Cl + 0.05 mol CH2Cl2; one HCl per H replaced
n_hcl = F(5, 100) * 1 + F(5, 100) * 2
assert n_hcl == F(15, 100)
v_2422 = "0.15 mol"
# 2427: 4.2 g propene -> 2-bromopropane (Markovnikov) -> Wurtz -> 2,3-dimethylbutane (C6H14)
n_prop = F(42, 10) / mm(C=3, H=6)
m_2427 = n_prop / 2 * mm(C=6, H=14)
assert n_prop == F(1, 10) and m_2427 == F(43, 10)
v_2427 = "2,3-Dimethylbutane, 4.3 g"
# 2428: alkenes giving the same product with HBr with and without peroxide = symmetrical alkenes
sym_2428 = {"ethene": True, "propene": False, "but-1-ene": False, "but-2-ene": True, "2-methylpropene": False,
            "cyclohexene": True, "2,3-dimethylbut-2-ene": True}
v_2428 = str(sum(sym_2428.values()))
assert v_2428 == "4"

QUESTIONS += [
    N(T_HC, "Electrophilic substitution", "Basic",
      "7.8 g of benzene is heated with fuming sulphuric acid (oleum) and is converted completely into "
      "benzenesulphonic acid, C₆H₅SO₃H. The mass of benzenesulphonic acid formed is (C = 12, H = 1, S = 32, O = 16):",
      ["8.0 g", v_2416, "7.8 g", "23.8 g"], "B", v_2416,
      "Sulphonation of benzene",
      "Benzene reacts with fuming sulphuric acid to give benzenesulphonic acid: C₆H₆ + SO₃ (H₂SO₄) → C₆H₅SO₃H. "
      "One mole of benzene gives one mole of product.",
      ["Benzene: 7.8 / 78 = 0.10 mol", "C₆H₅SO₃H: M = 158 g mol⁻¹", "Mass = 0.10 × 158 = 15.8 g"],
      why_others_wrong="8.0 g is the mass of SO₃ used; 7.8 g simply repeats the mass of benzene; 23.8 g is for a "
                       "disulphonic acid, C₆H₄(SO₃H)₂.",
      ncert=f"{NC11}, 'Hydrocarbons', electrophilic substitution reactions: sulphonation", seconds=40),

    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "In the free radical chlorination of methane in light, which of the following is a chain propagation step?",
      ["Cl₂ → Cl• + Cl•", "Cl• + Cl• → Cl₂", "CH₃• + CH₃• → CH₃–CH₃", "CH₄ + Cl• → CH₃• + HCl"], "D",
      "Mechanism of halogenation of alkanes",
      "Initiation: homolysis of Cl₂ by light. Propagation: a chlorine radical abstracts H from methane to give a "
      "methyl radical and HCl; the methyl radical then reacts with Cl₂ to give CH₃Cl and a new chlorine radical. "
      "Termination: two radicals combine.",
      ["Cl₂ → 2Cl•: initiation", "CH₄ + Cl• → CH₃• + HCl: propagation (radical in, radical out)",
       "Radical + radical → molecule: termination"],
      why_others_wrong="Homolysis of Cl₂ starts the chain (initiation); Cl• + Cl• and CH₃• + CH₃• consume radicals "
                       "without forming new ones, so they end the chain (termination).",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: halogenation mechanism", seconds=30),

    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "An aqueous solution of sodium propanoate, CH₃CH₂COONa, is electrolysed by Kolbe's electrolytic method. The "
      "hydrocarbon formed at the anode is:",
      ["Ethane", "Propane", "Butane", "Hexane"], "C",
      "Kolbe's electrolytic method",
      "In Kolbe's electrolysis 2RCOONa + 2H₂O → R–R + 2CO₂ + H₂ + 2NaOH. The alkyl groups of two carboxylate ions "
      "join after losing CO₂. With R = C₂H₅, the product is C₂H₅–C₂H₅, butane.",
      ["R = CH₃CH₂–", "R–R = CH₃CH₂–CH₂CH₃ = butane"],
      why_others_wrong="Ethane is formed from sodium ethanoate; propane would need the carboxyl carbon to stay in "
                       "the chain; hexane would need two propyl groups.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes from carboxylic acids", seconds=30),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "assertion_reason",
      *ar("Ozonolysis is used to locate the position of the double bond in an alkene.", True,
          "On ozonolysis followed by treatment with zinc and water, the alkene is cleaved at the double bond, and "
          "each carbon that was part of the double bond becomes the carbon of a C=O group in the products.", True,
          explains=True),
      "Ozonolysis as a structural tool",
      "Because the molecule is cut exactly at the C=C bond and both doubly bonded carbons end up as carbonyl "
      "carbons, identifying the carbonyl products tells where the double bond was. R is the reason for A.",
      ["Alkene + O₃ → ozonide; Zn/H₂O → two carbonyl compounds",
       "Carbonyl carbons = former doubly bonded carbons → position of C=C"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: ozonolysis", seconds=35),

    Q(T_HC, "Alkynes", "Basic", "statement_pair",
      *sp("Ethyne adds one molecule of HBr to give bromoethene, which adds a second molecule of HBr to give "
          "1,1-dibromoethane.", True,
          "Propyne, on hydration with dilute H₂SO₄ in the presence of Hg²⁺ ions, gives propanal.", False),
      "Addition reactions of alkynes",
      "HBr adds to ethyne first to give CH₂=CHBr; the second addition follows Markovnikov's rule, putting Br on the "
      "carbon that already carries Br: CH₃CHBr₂ (1,1-dibromoethane). Hydration of propyne also follows Markovnikov's "
      "rule: the enol CH₃C(OH)=CH₂ changes into propanone, not propanal.",
      ["Statement I: true", "Statement II: false; propyne → propanone"],
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: addition of hydrogen halides and water", seconds=40),

    N(T_HC, "Alkenes: addition and ozonolysis", "Intermediate",
      "18.8 g of 1,2-dibromoethane is heated with zinc dust and is converted completely into ethene. The volume of "
      "ethene formed, measured at STP, is (C = 12, H = 1, Br = 80; molar volume at STP = 22.4 L mol⁻¹):",
      ["1.12 L", "4.48 L", "0.224 L", v_2421], "D", v_2421,
      "Dehalogenation of vicinal dihalides",
      "Vicinal dihalides lose both halogen atoms on heating with zinc: BrCH₂–CH₂Br + Zn → CH₂=CH₂ + ZnBr₂. One "
      "mole of dihalide gives one mole of ethene.",
      ["BrCH₂CH₂Br: M = 188 g mol⁻¹ → 18.8 / 188 = 0.10 mol", "Ethene: 0.10 mol × 22.4 = 2.24 L"],
      why_others_wrong="4.48 L assumes two moles of gas per mole of dihalide; 1.12 L halves the moles; 0.224 L "
                       "misplaces the decimal (0.01 mol).",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes from vicinal dihalides", seconds=45),

    N(T_HC, "Alkanes and conformations", "Intermediate",
      "0.10 mol of methane is chlorinated in diffused sunlight, and the methane is converted completely into an "
      "equimolar mixture of CH₃Cl and CH₂Cl₂ only. The amount of HCl formed is:",
      ["0.10 mol", v_2422, "0.20 mol", "0.30 mol"], "B", v_2422,
      "Stoichiometry of free radical substitution",
      "Each hydrogen atom replaced by chlorine gives one molecule of HCl: CH₄ + Cl₂ → CH₃Cl + HCl and "
      "CH₄ + 2Cl₂ → CH₂Cl₂ + 2HCl.",
      ["Equimolar: 0.05 mol CH₃Cl + 0.05 mol CH₂Cl₂", "HCl = 0.05 × 1 + 0.05 × 2 = 0.15 mol"],
      why_others_wrong="0.10 mol counts one HCl per methane; 0.20 mol counts two for every methane; 0.30 mol counts "
                       "the chlorine atoms used (0.15 mol Cl₂ = 0.30 mol Cl) instead of the HCl formed.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: substitution reactions (halogenation)", seconds=50),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "statement_pair",
      *sp("With chlorine in the presence of ultraviolet light, benzene gives hexachlorobenzene, C₆Cl₆, by "
          "substitution.", False,
          "With an excess of chlorine in the presence of anhydrous AlCl₃ in the dark, benzene can be converted into "
          "hexachlorobenzene.", True),
      "Substitution versus addition in benzene",
      "In UV light benzene adds three molecules of chlorine to give benzene hexachloride, C₆H₆Cl₆ (an addition "
      "product), not hexachlorobenzene. With a Lewis acid and an excess of the electrophilic reagent, substitution "
      "continues until all six hydrogens are replaced: C₆H₆ + 6Cl₂ → C₆Cl₆ + 6HCl.",
      ["Statement I: false; UV light → C₆H₆Cl₆ by addition",
       "Statement II: true; excess Cl₂ / anhydrous AlCl₃ → C₆Cl₆ by substitution"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: chemical properties", seconds=45),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "match_list",
      *ml("Match the conversion in List-I with the catalyst or conditions used for it in List-II.",
          ["Hydrogenation of an alkene to an alkane", "Partial hydrogenation of an alkyne to a cis-alkene",
           "Hydration of ethyne to ethanal", "Conversion of n-hexane into benzene"],
          ["Hg²⁺ ions in dilute H₂SO₄ at 333 K", "Cr₂O₃ supported on alumina at 773 K and 10–20 atm",
           "Palladium on charcoal partly deactivated with quinoline", "Finely divided Pt, Pd or Ni"],
          "IV III I II", ["III IV I II", "IV III II I", "I III IV II"], "C"),
      "Catalysts in hydrocarbon reactions",
      "Alkenes and alkynes are hydrogenated completely over finely divided Pt, Pd or Ni; Lindlar's catalyst (Pd on "
      "charcoal deactivated with quinoline) stops the reduction of an alkyne at the cis-alkene; alkynes are hydrated "
      "with Hg²⁺/dilute H₂SO₄ at 333 K; n-hexane is aromatised over Cr₂O₃ (or V₂O₅, Mo₂O₃) on alumina at 773 K.",
      ["A → IV", "B → III", "C → I", "D → II"],
      why_others_wrong="Codes that swap the two palladium/nickel catalysts would reduce an alkyne fully or stop an "
                       "alkene reaction; codes that swap hydration and aromatisation mix up the mercury catalyst with "
                       "the oxide catalyst.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation and properties of alkanes, alkenes and alkynes", seconds=50),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "multi_statement",
      *ms("Which of the following statements about substituents on a benzene ring in electrophilic substitution are "
          "correct?",
          [("The –COOR group is meta directing.", True),
           ("The –NHCOCH₃ group is ortho and para directing.", True),
           ("The –SO₃H group is ortho and para directing.", False),
           ("The –CN group deactivates the benzene ring.", True),
           ("The –Br group activates the benzene ring.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "b", "d", "e"]], "D"),
      "Directive influence of functional groups",
      "Ortho/para directors: –OH, –NH₂, –NHR, –NHCOCH₃, –OCH₃, –CH₃ and halogens. Meta directors (deactivating): "
      "–NO₂, –CN, –CHO, –COR, –COOH, –COOR, –SO₃H. Halogens are ortho/para directing but deactivate the ring because "
      "of their strong −I effect.",
      ["(a) true", "(b) true", "(c) false: –SO₃H is meta directing", "(d) true", "(e) false: halogens deactivate"],
      why_others_wrong="Options with (c) treat –SO₃H as an electron-releasing group; options with (e) confuse the "
                       "ortho/para direction of halogens with activation.",
      ncert=f"{NC11}, 'Hydrocarbons', directive influence of a functional group in monosubstituted benzene",
      seconds=60),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "assertion_reason",
      *ar("The peroxide effect is not observed when HCl adds to propene.", True,
          "The H–Cl bond is weaker than the H–Br bond, so HCl is readily cleaved by free radicals.", False),
      "Why only HBr shows the peroxide effect",
      "NCERT explains that the H–Cl bond (430.5 kJ mol⁻¹) is stronger than the H–Br bond (363.7 kJ mol⁻¹) and is "
      "not cleaved by the free radicals formed from the peroxide. So A is true and R, which reverses the bond "
      "strengths, is false.",
      ["A: true", "R: false; H–Cl is stronger than H–Br"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: anti-Markovnikov addition (peroxide effect)", seconds=40),

    N(T_HC, "Alkenes: addition and ozonolysis", "Advanced",
      "4.2 g of propene is treated with HBr in the absence of peroxide, and the product is heated with sodium in dry "
      "ether. Assuming every step is complete, the final hydrocarbon and its mass are (C = 12, H = 1, Br = 80):",
      ["n-Hexane, 4.3 g", v_2427, "2,3-Dimethylbutane, 8.6 g", "n-Hexane, 8.6 g"], "B", v_2427,
      "Markovnikov addition followed by the Wurtz reaction",
      "Without peroxide, HBr adds by Markovnikov's rule to give 2-bromopropane. In the Wurtz reaction two "
      "isopropyl groups join: (CH₃)₂CH–CH(CH₃)₂, 2,3-dimethylbutane. Two moles of alkyl halide give one mole of "
      "alkane.",
      ["Propene: 4.2 / 42 = 0.10 mol → 0.10 mol (CH₃)₂CHBr",
       "Wurtz: 0.10 mol RBr → 0.05 mol R–R", "C₆H₁₄: 0.05 × 86 = 4.3 g of 2,3-dimethylbutane"],
      why_others_wrong="n-Hexane would come from 1-bromopropane (peroxide addition); 8.6 g forgets that two "
                       "molecules of alkyl halide give one molecule of alkane.",
      ncert=f"{NC11}, 'Hydrocarbons', Markovnikov rule; Wurtz reaction", seconds=80),

    N(T_HC, "Alkenes: addition and ozonolysis", "Advanced",
      "HBr is added to each of the following alkenes, once in the absence and once in the presence of benzoyl "
      "peroxide. For how many of them is the main product the same in both cases?\n"
      "Ethene, propene, but-1-ene, but-2-ene, 2-methylpropene, cyclohexene, 2,3-dimethylbut-2-ene",
      ["1", "2", "3", v_2428], "D", v_2428,
      "Peroxide effect matters only for unsymmetrical alkenes",
      "Markovnikov and anti-Markovnikov additions give different products only when the two doubly bonded carbons "
      "are differently substituted. For a symmetrical alkene, Br goes to an equivalent carbon either way.",
      ["Symmetrical: ethene, but-2-ene, cyclohexene, 2,3-dimethylbut-2-ene → same product (4)",
       "Unsymmetrical: propene, but-1-ene, 2-methylpropene → different products"],
      why_others_wrong="Lower counts usually leave out cyclohexene or 2,3-dimethylbut-2-ene, whose doubly bonded "
                       "carbons are equivalent even though the molecules are not straight chains.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: addition of hydrogen halides", seconds=60),

    Q(T_HC, "Electrophilic substitution", "Advanced", "direct",
      "m-Bromonitrobenzene is to be prepared from benzene as the main product, using Br₂/FeBr₃ and a mixture of "
      "concentrated HNO₃ and H₂SO₄. The correct sequence is:",
      ["Nitration first, then bromination", "Bromination first, then nitration",
       "Either order, as both give the same main product", "Both reagents together in a single step"], "A",
      "Using directive influence in synthesis",
      "The –NO₂ group is meta directing, so brominating nitrobenzene puts Br at the meta position. Bromine is "
      "ortho/para directing, so nitrating bromobenzene would give mainly o- and p-bromonitrobenzene.",
      ["C₆H₆ → (HNO₃/H₂SO₄) C₆H₅NO₂", "C₆H₅NO₂ → (Br₂/FeBr₃) m-BrC₆H₄NO₂"],
      why_others_wrong="Bromination first gives ortho and para products; the order matters because the first group "
                       "directs the second; a one-step mixture gives no control over position.",
      ncert=f"{NC11}, 'Hydrocarbons', directive influence of a functional group in monosubstituted benzene",
      seconds=50),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "match_list",
      *ml("Each alkene in List-I is hydrated with water in the presence of an acid. Match it with its main product "
          "in List-II.",
          ["Propene", "2-Methylpropene", "But-1-ene", "Ethene"],
          ["Ethanol", "Butan-2-ol", "Propan-2-ol", "2-Methylpropan-2-ol"],
          "III IV II I", ["III IV I II", "IV III II I", "II IV III I"], "D"),
      "Markovnikov addition of water",
      "Acid-catalysed hydration goes through the more stable carbocation, so the –OH ends up on the more "
      "substituted carbon of the double bond (Markovnikov's rule).",
      ["Propene → (CH₃)₂CH⁺ → propan-2-ol", "2-Methylpropene → (CH₃)₃C⁺ → 2-methylpropan-2-ol",
       "But-1-ene → CH₃CH₂CH⁺CH₃ → butan-2-ol", "Ethene → ethanol"],
      why_others_wrong="The other codes give an alcohol whose carbon skeleton differs from that of the alkene (for "
                       "example ethene → butan-2-ol or propene → 2-methylpropan-2-ol); the trap in this set is "
                       "but-1-ene, which gives butan-2-ol, not butan-1-ol.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: addition of water", seconds=50),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "multi_statement",
      *ms("Which of the following statements about the addition of HBr to propene are correct?",
          [("In the absence of peroxide, the first step is the attack of H⁺, an electrophile, on the double bond.",
            True),
           ("Protonation at C-1 gives a secondary carbocation, which is formed in preference to the primary one.",
            True),
           ("In the second step, Br⁻ attacks the carbocation.", True),
           ("In the presence of a peroxide, a bromine free radical adds first to C-1, giving the more stable "
            "secondary free radical.", True),
           ("The addition in the presence of a peroxide proceeds through a carbocation intermediate.", False)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "A"),
      "Mechanisms of Markovnikov and anti-Markovnikov addition",
      "Ionic addition: H⁺ adds to C-1 to give the 2° carbocation CH₃CH⁺CH₃, which Br⁻ attacks → 2-bromopropane. "
      "Peroxide addition is a free radical chain: Br• adds to C-1, giving the 2° radical CH₃ĊHCH₂Br, which takes "
      "H from HBr → 1-bromopropane. No carbocation is involved in the peroxide reaction.",
      ["(a), (b), (c) true: ionic mechanism", "(d) true: free radical mechanism", "(e) false"],
      why_others_wrong="(a), (b) and (c) only misses the radical step; options with (e) attribute a carbocation to "
                       "the free radical pathway.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: mechanism of addition of HBr", seconds=75),
]
