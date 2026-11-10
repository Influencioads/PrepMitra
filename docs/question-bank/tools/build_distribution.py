"""Builds the PrepMitra banking question-bank plan from one taxonomy.

Writes taxonomy.json (subject -> topic -> subtopics, with exact target counts per difficulty) and
02_SYLLABUS_AND_DISTRIBUTION.md. Counts are allocated with the largest-remainder method so that every subject total
and every difficulty total is exact (10,000 = 3,000 Basic + 4,000 Intermediate + 3,000 Advanced).

Topic weights are relative frequencies estimated from the official section sizes and published shift-wise exam
analyses (see 03_SOURCES.md). They are a plan, not a measurement; re-run after changing a weight.

    python docs/question-bank/tools/build_distribution.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIFFS = {"Basic": 30, "Intermediate": 40, "Advanced": 30}

# subject -> (id prefix, target, [(topic, weight, [subtopics], note)])
TAXONOMY = {
    "Quantitative Aptitude": ("QUANT", 2000, [
        ("Simplification", 6, ["BODMAS", "Fractions and decimals", "Surds and indices", "Square and cube roots"], ""),
        ("Approximation", 6, ["Percentage approximation", "Root approximation", "Mixed approximation"], ""),
        ("Number Series", 7, ["Missing number series", "Pattern: differences", "Pattern: multiply-add", "Pattern: squares and cubes"], ""),
        ("Wrong Number Series", 3, ["Find the wrong term"], "Added: frequent in IBPS/SBI prelims"),
        ("Quadratic Equations", 5, ["Relation between roots", "Linear vs quadratic"], "Added: a staple of PO and RRB prelims"),
        ("Number System", 2.5, ["Divisibility", "HCF and LCM", "Remainders", "Unit digit"], ""),
        ("Percentage", 3.5, ["Basic percentage", "Successive change", "Population and depreciation", "Income and expenditure"], ""),
        ("Ratio and Proportion", 3, ["Basic ratio", "Proportion", "Ages via ratio", "Coins and salary share"], ""),
        ("Problems on Ages", 2, ["Present and future ages", "Ratio-based ages"], "Added: regular arithmetic word problem"),
        ("Average", 2.5, ["Simple average", "Replacement", "Weighted average"], ""),
        ("Profit and Loss", 3.5, ["Cost and selling price", "Marked price", "Dishonest dealer", "Successive transactions"], ""),
        ("Discount", 2, ["Single discount", "Successive discounts", "Discount with profit"], ""),
        ("Simple Interest", 2, ["Basic SI", "SI with changing rates"], ""),
        ("Compound Interest", 3, ["Annual compounding", "Half-yearly and quarterly", "CI vs SI difference", "Instalments"], ""),
        ("Partnership", 2.5, ["Simple partnership", "Compound partnership", "Working partner"], ""),
        ("Mixture and Alligation", 3, ["Alligation rule", "Replacement of mixture", "Mixing solutions"], ""),
        ("Time and Work", 3, ["Work efficiency", "Work and wages", "Alternate days", "Men-women-children"], ""),
        ("Pipes and Cisterns", 2, ["Inlet and outlet", "Leak problems"], ""),
        ("Speed, Time and Distance", 3, ["Average speed", "Relative speed", "Meeting and overtaking"], ""),
        ("Boats and Streams", 2, ["Upstream and downstream", "Speed of stream"], ""),
        ("Problems on Trains", 2, ["Crossing a pole or platform", "Trains crossing each other"], ""),
        ("Mensuration", 3, ["2D areas and perimeters", "3D volume and surface area", "Cylinder, cone and sphere"], ""),
        ("Probability", 3, ["Coins and dice", "Cards", "Balls from bags"], ""),
        ("Permutation and Combination", 2, ["Arrangements", "Selections", "Word arrangements"], ""),
        ("Tabular DI", 5, ["Single table", "Table with percentages"], ""),
        ("Bar Graph DI", 4, ["Simple bar", "Stacked or grouped bar"], ""),
        ("Pie Chart DI", 4, ["Degree-based", "Percentage-based", "Two pie charts"], ""),
        ("Line Graph DI", 3.5, ["Single line", "Multiple lines"], ""),
        ("Caselet DI", 5, ["Paragraph data", "Caselet with table"], ""),
        ("Missing DI", 3, ["Table with missing values"], ""),
        ("Quantity Comparison", 4, ["Quantity I vs II", "Arithmetic-based comparison"], ""),
        ("Data Sufficiency (Quant)", 2.5, ["Two-statement", "Three-statement"], "Added: appears in PO mains DA&I"),
    ]),
    "Reasoning Ability": ("REAS", 2000, [
        ("Linear Seating Arrangement", 5.5, ["Single row, facing north/south", "Double row", "Unknown number of persons"], ""),
        ("Circular Seating Arrangement", 5.5, ["Facing centre", "Facing inside and outside", "Square and rectangular tables"], ""),
        ("Floor-Based Puzzles", 6, ["Floor and flat", "Floor with attribute"], ""),
        ("Box-Based Puzzles", 5, ["Stacked boxes", "Boxes with weights or colours"], ""),
        ("Month and Date-Based Puzzles", 5, ["Month-based", "Date-based", "Year-based"], ""),
        ("Puzzles (Other)", 3, ["Designation", "Comparison and ordering", "Day-based"], "Covers puzzles that are not seating, floor, box or calendar"),
        ("Syllogism", 7, ["Two-statement", "Only a few / Only", "Possibility cases"], ""),
        ("Inequality", 7, ["Direct inequality", "Coded inequality"], ""),
        ("Blood Relations", 4, ["Direct relation", "Coded blood relation", "Family puzzle"], ""),
        ("Direction Sense", 4, ["Distance and direction", "Point-to-point", "Shadow-based"], ""),
        ("Coding and Decoding", 5.5, ["Letter coding", "Sentence/word coding", "Number coding"], ""),
        ("Alphanumeric Series", 3.5, ["Position-based", "Symbol and number series"], ""),
        ("Alphabet Test", 2.5, ["Letter position", "Word formation", "Pairs of letters"], ""),
        ("Number Series (Reasoning)", 2, ["Number-based digit operations", "Three-digit number questions"], "Digit-operation questions; arithmetic series sit in Quant"),
        ("Ranking and Order", 2.5, ["Position in a row", "Comparison of heights/weights"], ""),
        ("Input and Output", 3.5, ["Word rearrangement", "Number rearrangement", "Mixed machine"], ""),
        ("Data Sufficiency", 3.5, ["Two-statement", "Three-statement"], ""),
        ("Statement and Assumptions", 2.5, ["Implicit assumptions"], "Logical reasoning"),
        ("Statement and Conclusions", 2.5, ["Valid conclusions", "Inferences"], "Logical reasoning"),
        ("Cause and Effect", 2, ["Independent causes", "Common cause"], "Logical reasoning"),
        ("Critical Reasoning", 4.5, ["Strengthen and weaken", "Course of action", "Inference from a passage"], "Logical reasoning; heavier in PO mains"),
    ]),
    "English Language": ("ENG", 1500, [
        ("Reading Comprehension", 20, ["Factual", "Inference", "Tone and title", "Vocabulary in context"], ""),
        ("Cloze Test", 12, ["Single-blank cloze", "Error-based cloze"], ""),
        ("Error Detection", 10, ["Part-wise error", "Error-free sentence"], ""),
        ("Sentence Improvement", 5, ["Bold-part improvement"], ""),
        ("Phrase Replacement", 3, ["Replace the phrase"], ""),
        ("Sentence Correction", 3, ["Correct sentence", "Grammatically incorrect sentence"], ""),
        ("Para Jumbles", 6, ["Five-sentence jumble", "Fixed sentence"], ""),
        ("Sentence Rearrangement", 2, ["Word/phrase rearrangement within a sentence"], ""),
        ("Fill in the Blanks", 8, ["Single blank", "Double blank", "Phrase fillers"], ""),
        ("Word Usage", 3, ["Correct usage of a word", "Word swap"], ""),
        ("Vocabulary", 3, ["Contextual meaning", "Word pairs"], ""),
        ("Synonyms", 3, ["Contextual synonym"], ""),
        ("Antonyms", 2.5, ["Contextual antonym"], ""),
        ("Idioms and Phrases", 3, ["Meaning of idiom", "Idiom in context"], ""),
        ("One-Word Substitution", 2, ["Single word for a phrase"], ""),
        ("Active and Passive Voice", 1.5, ["Voice conversion"], "Rare in current patterns; kept low"),
        ("Direct and Indirect Speech", 1.5, ["Narration change"], "Rare in current patterns; kept low"),
        ("Subject-Verb Agreement", 2, ["Agreement rules"], "Grammar"),
        ("Tenses", 2, ["Sequence of tenses", "Perfect tenses"], "Grammar"),
        ("Articles", 1.5, ["Definite and indefinite"], "Grammar"),
        ("Prepositions", 2, ["Fixed prepositions", "Phrasal verbs"], "Grammar"),
        ("Connectors", 3, ["Sentence connectors", "Starters and linkers"], ""),
    ]),
    "General Awareness and Current Affairs": ("GA", 1500, [
        ("National Current Affairs", 12, ["Government decisions", "States and UTs", "Defence"], "Current affairs: 6-8 month window"),
        ("International Current Affairs", 10, ["Bilateral relations", "Global events"], "Current affairs"),
        ("Government Schemes", 11, ["Central schemes", "Scheme launches and changes"], ""),
        ("Important Appointments", 8, ["Banking and finance heads", "International bodies"], "Current affairs"),
        ("Awards and Honours", 7, ["National awards", "International awards"], "Current affairs"),
        ("Sports", 7, ["Tournaments and winners", "Venues and records"], "Current affairs"),
        ("Summits and Conferences", 5, ["G20, BRICS, SCO and others", "Hosting countries"], "Current affairs"),
        ("Important Days", 4, ["Days and themes"], ""),
        ("Books and Authors", 3, ["Recent books"], "Current affairs"),
        ("National and International Organizations", 8, ["Headquarters and heads", "Membership"], ""),
        ("Important Reports and Indexes", 7, ["Publishing body", "India's rank"], ""),
        ("Economic Affairs", 9, ["GDP and growth projections", "Inflation data", "Fiscal data",
                                 "Monetary policy decisions"], "Current affairs"),
        ("Government Policies", 5, ["Policy changes", "Regulatory reforms"], ""),
        ("Business and Corporate News", 5, ["Mergers and acquisitions", "Corporate partnerships"], "Current affairs"),
        ("Static Awareness", 7, ["Capitals and currencies", "National parks and dams", "Indian states facts"], "Added: common in RRB GA"),
    ]),
    "Banking and Financial Awareness": ("BFA", 2000, [
        ("Banking Fundamentals", 6, ["Types of accounts", "Types of banks", "Cheques and instruments"], ""),
        ("History of Banking in India", 3, ["Nationalisation", "Mergers and consolidation", "Committees"], ""),
        ("Reserve Bank of India", 4, ["Establishment and structure", "Governors and leadership"], ""),
        ("RBI Functions", 4, ["Issuer of currency", "Banker to government", "Regulator and supervisor"], ""),
        ("Monetary Policy", 5, ["MPC structure", "Policy stance", "Transmission"], ""),
        ("Repo Rate", 2.5, ["Repo and policy corridor"], "Current values change: needs review_by date"),
        ("Reverse Repo Rate", 1.5, ["Reverse repo and SDF"], ""),
        ("CRR", 2, ["CRR concept", "CRR value"], ""),
        ("SLR", 2, ["SLR concept", "SLR value"], ""),
        ("Bank Rate", 1.5, ["Bank rate and MSF"], ""),
        ("Inflation", 3, ["CPI and WPI", "Inflation targeting"], ""),
        ("NPA", 4, ["Classification", "Resolution and IBC", "SARFAESI"], ""),
        ("Basel Norms", 4, ["Capital adequacy", "LCR and NSFR", "Leverage ratio"], ""),
        ("Financial Inclusion", 4, ["PMJDY and allied schemes", "Business correspondents"], ""),
        ("Priority Sector Lending", 3.5, ["Targets and sub-targets", "PSLCs"], ""),
        ("RBI Integrated Ombudsman Scheme", 3, ["Scope and grounds", "Process and limits"], ""),
        ("Digital Banking", 4, ["Mobile and internet banking", "Digital lending", "CBDC (e-rupee)"], ""),
        ("UPI", 3.5, ["Features", "UPI Lite and international"], ""),
        ("NEFT", 2, ["Settlement and timings"], ""),
        ("RTGS", 2, ["Limits and timings"], ""),
        ("IMPS", 1.5, ["Limits and features"], ""),
        ("NPCI", 3, ["Products: NACH, AePS, RuPay, FASTag"], ""),
        ("Payment Banks", 2, ["Permitted activities", "Deposit limit"], ""),
        ("Small Finance Banks", 2, ["Licensing norms", "PSL targets"], ""),
        ("Financial Markets", 3, ["Structure and regulators"], ""),
        ("Money Market", 3, ["Instruments: T-bills, CP, CD, call money"], ""),
        ("Capital Market", 3.5, ["Primary and secondary market", "SEBI", "Indices"], ""),
        ("Insurance", 3, ["IRDAI", "Life and general insurance", "Government insurance schemes"], ""),
        ("Mutual Funds", 2.5, ["Types", "NAV and SIP", "AMFI"], ""),
        ("Budget and Economic Survey", 4, ["Union Budget highlights", "Economic Survey highlights", "Fiscal terms"], "Current affairs"),
        ("Government Financial Schemes", 4, ["PMMY, PMSBY, PMJJBY, APY", "Credit guarantee schemes"], ""),
        ("RBI Circulars and Regulatory Updates", 4, ["Recent RBI directions"], "Added: IBPS PO 2026 Mains names RBI circulars explicitly"),
    ]),
    "Computer Knowledge": ("COMP", 1000, [
        ("Computer Fundamentals", 9, ["Generations and history", "Number systems", "Types of computers"], ""),
        ("Hardware", 7, ["CPU and components", "Motherboard and ports"], ""),
        ("Software", 7, ["System and application software", "Licensing", "Programming languages"], ""),
        ("Operating Systems", 8, ["Functions", "Windows and Linux basics", "File systems"], ""),
        ("Input and Output Devices", 6, ["Input devices", "Output devices"], ""),
        ("Memory", 8, ["Primary memory", "Secondary storage", "Cache and units"], ""),
        ("Internet", 8, ["Web basics", "Protocols", "Email"], ""),
        ("Networking", 9, ["Topologies", "OSI and TCP/IP", "Devices"], ""),
        ("Cybersecurity", 10, ["Malware", "Phishing and social engineering", "Encryption and authentication"], ""),
        ("Database Fundamentals", 7, ["DBMS concepts", "Keys", "SQL basics"], ""),
        ("MS Office", 10, ["MS Word", "MS Excel", "MS PowerPoint", "Shortcuts"], ""),
        ("Digital Payments", 4, ["Payment technology", "Card security"], "Technical side; banking side sits in BFA"),
        ("Computer Abbreviations", 7, ["Common abbreviations"], ""),
    ]),
}


def largest_remainder(total: int, weights: dict) -> dict:
    s = sum(weights.values())
    raw = {k: total * w / s for k, w in weights.items()}
    out = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[: total - sum(out.values())]:
        out[k] += 1
    return out


def exam_stages_by_subject() -> dict:
    """Which exam stages test each subject, read from the official patterns."""
    patterns = json.loads((ROOT / "exam_patterns.json").read_text(encoding="utf-8"))
    out: dict = {}
    for exam in patterns["exams"]:
        for stage in exam["stages"]:
            for sec in stage["sections"]:
                for subj in sec["subjects"]:
                    out.setdefault(subj, []).append(f'{exam["exam_id"]}:{stage["stage"]}')
    return {k: sorted(set(v)) for k, v in out.items()}


def build():
    applicability = exam_stages_by_subject()
    subjects, rows = [], []
    for subject, (prefix, target, topics) in TAXONOMY.items():
        weights = {t[0]: t[1] for t in topics}
        per_diff = largest_remainder(target, DIFFS)  # subject totals are multiples of 10, so this is exact 30/40/30
        by_diff = {d: largest_remainder(n, weights) for d, n in per_diff.items()}
        out_topics = []
        for name, _, subtopics, note in topics:
            counts = {d: by_diff[d][name] for d in DIFFS}
            out_topics.append({"topic": name, "subtopics": subtopics, "note": note,
                               "target": sum(counts.values()), "by_difficulty": counts})
            rows.append((subject, name, counts))
        subjects.append({"subject": subject, "id_prefix": f"BANK_{prefix}_", "target": target,
                         "by_difficulty": per_diff, "tested_in": applicability.get(subject, []),
                         "topics": out_topics})

    grand = {d: sum(r[2][d] for r in rows) for d in DIFFS}
    assert sum(grand.values()) == 10000 and grand == {"Basic": 3000, "Intermediate": 4000, "Advanced": 3000}, grand
    (ROOT / "taxonomy.json").write_text(json.dumps({"total": 10000, "by_difficulty": grand, "subjects": subjects},
                                                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md = ["# Banking Syllabus and 10,000-Question Distribution", "",
          "Generated by `tools/build_distribution.py` from `taxonomy.json`; edit the weights there, not this file.",
          "", "Difficulty split is 30 / 40 / 30 inside every subject, so the grand totals are exactly "
          "3,000 Basic, 4,000 Intermediate and 3,000 Advanced.", "",
          "## Summary", "", "| Subject | Basic | Intermediate | Advanced | Total | Tested in (exam:stage) |",
          "|---|---:|---:|---:|---:|---|"]
    for s in subjects:
        d = s["by_difficulty"]
        md.append(f'| {s["subject"]} | {d["Basic"]:,} | {d["Intermediate"]:,} | {d["Advanced"]:,} | '
                  f'{s["target"]:,} | {", ".join(s["tested_in"])} |')
    md.append(f'| **Total** | **{grand["Basic"]:,}** | **{grand["Intermediate"]:,}** | **{grand["Advanced"]:,}** '
              f'| **10,000** | |')
    for s in subjects:
        md += ["", f'## {s["subject"]} ({s["target"]:,})', "",
               "| Topic | Subtopics | Basic | Inter. | Adv. | Total | Note |", "|---|---|---:|---:|---:|---:|---|"]
        for t in s["topics"]:
            c = t["by_difficulty"]
            md.append(f'| {t["topic"]} | {"; ".join(t["subtopics"])} | {c["Basic"]} | {c["Intermediate"]} | '
                      f'{c["Advanced"]} | {t["target"]} | {t["note"]} |')
    (ROOT / "02_SYLLABUS_AND_DISTRIBUTION.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("subjects:", {s["subject"]: s["target"] for s in subjects}, "difficulty:", grand)


if __name__ == "__main__":
    build()
