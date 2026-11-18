# Batch 8 summary (17 Nov 2026)

**1,000 original questions**, `NEET_PHY/CHE/BOT/ZOO_001751` to `_002000`, written as 8 topic packages
(`tools/batch_008/*.py`) and merged into `BATCH_008.json`. The bank now holds **8,000 of 10,000**.

- **Difficulty:** 300 Basic / 397 Intermediate / 303 Advanced, exactly as planned per topic.
- **Formats:** 245 numerical, 232 direct, 138 multi-statement, 137 statement pair, 136 assertion-reason, 112 match the list.
- **Answer keys:** A 253, B 246, C 253, D 248.
- **Validator:** 0 errors and 0 warnings for the sample and Batches 1–8 together (8,000 questions).

## Verification

- **289 answers** are recomputed by an `assert` in the builders.
- **All 1,000** were answered blind with no key. 999 matched first time; the one disagreement (`BOT_001928`, an
  assertion-reason item where R only partly explained A) was rewritten.
- **17 questions were changed** and all 17 matched on a blind re-check:
  - **Outside the strict NMC wording (6):** two Carnot engine / COP questions in Physics; in Chemistry, astatine's
    radioactivity, a match list of single-element properties (gallium's melting point), actinoid contraction, and
    lanthanoid hardness and tarnishing.
  - **NCERT lines that are wrong in reality (5):** ctenophores as radially symmetrical, hexokinase acting on fructose,
    every parietal ovary becoming two-chambered, the white-light fringe next to the centre being red, recombination
    changing a single gene's allele frequency.
  - **Inferences or knowledge NCERT does not give (5):** somatostatin loss causing gigantism, more enzyme raising Vmax,
    Penicillium's class, a conditional-probability Hardy-Weinberg step, and an ambiguous work-energy assertion.
  - **Arguable assertion-reason key (1):** `BOT_001928`.
- All 1,000 are `Pending Human Review`.

## For a teacher to check first

- **`ZOO_001880`** (pars intermedia lesion affects MSH) rests on facts already asked as recall items; only the set-up is new.
- **`CHE_001962`, `CHE_001970`** rely on recalled NCERT pKa / pKb orders; the keys depend only on the order.
- **`CHE_001899`** treats two esters as metamers; NCERT shows metamerism only with ethers.
- **Physics logic-gate and Experimental Skills items** still cite the NMC syllabus, as the rationalised NCERT dropped them.
