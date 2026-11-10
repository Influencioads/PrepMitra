"""Writes the three fragment files of Banking and Financial Awareness topic package 3 (batches 008, 009 and 010):

    batches/parts/frag/BATCH_008_BFA_pkg3.json   (63 questions, BANK_BFA_001540 - 001602)
    batches/parts/frag/BATCH_009_BFA_pkg3.json   (65 questions, BANK_BFA_001737 - 001801)
    batches/parts/frag/BATCH_010_BFA_pkg3.json   (63 questions, BANK_BFA_001938 - 002000)

Topics: Payment Banks, Small Finance Banks, Financial Markets, Money Market, Capital Market, Insurance, Mutual Funds,
Budget and Economic Survey, Government Financial Schemes, RBI Circulars and Regulatory Updates.

Structure follows tools/batch_006/banking.py. Every fact is backed by a fact_check whose source was opened on
2026-11-06 (HTML pages fetched with a plain client and read; PDFs downloaded and their text extracted), or, where only
search results stated it (no block was worked around), by search results, in which case the question carries
web:search-confirmed. Only the rules in force on 2026-11-06 are tested (SEBI's revised mutual fund categorisation of
26 February 2026, the current RBI money market directions, etc.); a proposal or draft is named as such. Questions on a
dated event or a value that can change carry current_affairs with the date stated by the source. Every computable
answer is re-derived below with assertions; the per-batch quota per (topic, difficulty), the ID ranges and the key
balance are checked against batches/plans/packages/BFA_pkg3.json before anything is written. All earlier questions of
these topics (BATCH_000 sample and the BATCH_001-007 Banking parts, including the final BATCH_007 part) were read
first; their facts are not repeated. ai:independent-check is added only to questions in
INDEPENDENT, which a separate fresh solver answered blind (stem and options only) and matched with confidence.

    python tools/packages/BFA_pkg3.py      (run from anywhere)
"""

import json
import random
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"      # verified_at / created_at, as the brief fixes
CHECKED = "2026-11-06"    # the day the sources were actually opened
REVIEW_BY = "2027-05-05"
LETTERS = "ABCD"
BF = "Banking and Financial Awareness"
SECONDS = {"Basic": 20, "Intermediate": 30, "Advanced": 60}
PKG = json.loads((ROOT / "batches" / "plans" / "packages" / "BFA_pkg3.json").read_text(encoding="utf-8"))
BATCHES = ("008", "009", "010")

_rng = random.Random(2026110603)
_keys = {b: Counter() for b in BATCHES}
QS = {b: [] for b in BATCHES}

# Question IDs that a separate fresh solver answered blind (stem and options only) and matched with high confidence.
# 97 questions (every second question of each fragment) were given to a separate fresh solver, key-free. It matched
# 93; the 4 misses were low-confidence guesses on 2026 RBI facts (keys re-checked against RBI pages, unchanged).
# The 52 high-confidence matches are tagged; no tagged question was changed afterwards.
INDEPENDENT = {"BANK_BFA_001540", "BANK_BFA_001542", "BANK_BFA_001546", "BANK_BFA_001548", "BANK_BFA_001550",
    "BANK_BFA_001552", "BANK_BFA_001554", "BANK_BFA_001556", "BANK_BFA_001558", "BANK_BFA_001562",
    "BANK_BFA_001570", "BANK_BFA_001572", "BANK_BFA_001574", "BANK_BFA_001576", "BANK_BFA_001580",
    "BANK_BFA_001584", "BANK_BFA_001586", "BANK_BFA_001588", "BANK_BFA_001590", "BANK_BFA_001592",
    "BANK_BFA_001594", "BANK_BFA_001737", "BANK_BFA_001739", "BANK_BFA_001743", "BANK_BFA_001745",
    "BANK_BFA_001747", "BANK_BFA_001749", "BANK_BFA_001753", "BANK_BFA_001755", "BANK_BFA_001759",
    "BANK_BFA_001761", "BANK_BFA_001767", "BANK_BFA_001781", "BANK_BFA_001783", "BANK_BFA_001785",
    "BANK_BFA_001791", "BANK_BFA_001942", "BANK_BFA_001944", "BANK_BFA_001948", "BANK_BFA_001950",
    "BANK_BFA_001952", "BANK_BFA_001954", "BANK_BFA_001956", "BANK_BFA_001968", "BANK_BFA_001972",
    "BANK_BFA_001976", "BANK_BFA_001982", "BANK_BFA_001984", "BANK_BFA_001986", "BANK_BFA_001990",
    "BANK_BFA_001992", "BANK_BFA_002000"}

# URLs confirmed only through search results.
SEARCH_ONLY = set()


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": CHECKED}


def ca(event_date, review_by=REVIEW_BY):
    return {"event_date": event_date, "review_by": review_by}


def Q(b, topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, facts, why,
      seconds=None, computed=False, current=None, shortcut=None):
    """Adds one question to batch b. With answer=None, options[0] is the correct text and it is placed at the
    least-used key of that batch so far (random tie-break, fixed seed)."""
    assert b in BATCHES
    assert len(options) == 4 and len(set(options)) == 4, text
    assert facts and why and steps, text
    keys = _keys[b]
    if answer is None:
        low = min(keys[k] for k in LETTERS)
        pos = LETTERS.index(_rng.choice([k for k in LETTERS if keys[k] == low]))
        correct, wrongs = options[0], list(options[1:])
        options = wrongs[:pos] + [correct] + wrongs[pos:]
        answer = LETTERS[pos]
    assert answer in LETTERS
    keys[answer] += 1
    QS[b].append({
        "exam_mappings": default_mappings(BF, difficulty),
        "subject": BF, "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_type": "MCQ", "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds or (90 if computed and difficulty == "Advanced" else SECONDS[difficulty]),
        "_current": current, "_computed": computed, "_facts": facts,
    })


# ============================================================================================ sources
# All opened on 2026-11-06 unless added to SEARCH_ONLY.
SEBI_MFCAT = "https://www.sebi.gov.in/sebi_data/attachdocs/feb-2026/1772079826878.pdf"   # SEBI circular 26 Feb 2026
RBI_CD = "https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12108"             # CD Directions, 2021
RBI_CP = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12592&Mode=0"          # CP and NCD Directions, 2024
BUDGET = "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf"  # PIB Budget compendium

BUD = ca("2026-02-01")        # Union Budget 2026-27 presented
MFC = ca("2026-02-26")        # SEBI revised MF categorisation circular

# ============================================================================================ Mutual Funds
T = "Mutual Funds"
Q("008", T, "Types", "Basic",
  "Under SEBI's mutual fund categorisation of February 2026, what is the minimum equity allocation of a Flexi Cap Fund, "
  "which invests dynamically across large, mid and small caps?",
  ["65% of total assets, with no minimum for any market-cap segment", "75% of total assets, with 25% in each segment",
   "80% of total assets, in not more than 30 stocks", "95% of total assets, tracking an index"],
  concept="Flexi Cap Fund",
  explanation="A Flexi Cap Fund must keep at least 65% of total assets in equity and equity-related instruments and is "
              "free to move across market capitalisations. Multi Cap funds need 75% with 25% in each segment; Focused "
              "funds hold at most 30 stocks with 80% in equity; index funds hold 95% in index securities.",
  steps=["Flexi Cap: ≥ 65% equity; no segment floors"],
  why="The other allocations belong to the Multi Cap, Focused and index fund categories.",
  current=MFC,
  facts=[fact("Flexi Cap Fund: Minimum Investment in equity & equity related instruments - 65% of total assets; An open "
              "ended dynamic equity scheme investing across large cap, mid cap, small cap stocks", SEBI_MFCAT)])
Q("008", T, "Types", "Basic",
  "Under SEBI's revised categorisation of mutual fund schemes (February 2026), what must a Large & Mid Cap Fund invest "
  "in?",
  ["At least 35% each in large cap and mid cap companies", "At least 80% in large cap companies",
   "At least 65% in mid cap companies", "At least 25% each in large, mid and small cap companies"],
  concept="Large & Mid Cap Fund",
  explanation="A Large & Mid Cap Fund must invest at least 35% of total assets in equity of large cap companies and at "
              "least 35% in mid cap companies. 80% in large caps is the Large Cap Fund rule, 65% in mid caps the Mid "
              "Cap Fund rule, and 25% each in three segments the Multi Cap Fund rule.",
  steps=["Large & Mid Cap: ≥ 35% large + ≥ 35% mid"],
  why="The other options describe the Large Cap, Mid Cap and Multi Cap categories.",
  current=MFC,
  facts=[fact("Large & Mid Cap Fund: Minimum investment in equity & equity related instruments of large cap companies - "
              "35% of total assets; Minimum investment in equity & equity related instruments of mid cap stocks - 35% of "
              "total assets", SEBI_MFCAT)])
Q("008", T, "Types", "Intermediate",
  "Under SEBI's mutual fund categorisation circular of 26 February 2026, may a fund house offer both a Value Fund and a "
  "Contra Fund?",
  ["Yes, provided the portfolio overlap between the two schemes is not more than 50%",
   "No, a fund house may offer only one of the two",
   "Yes, without any restriction, as they follow different strategies",
   "Yes, provided the two schemes hold no common stock at all"],
  concept="Value and Contra funds",
  explanation="Under the 2017 framework a fund house could offer either a value fund or a contra fund. The 2026 circular "
              "permits both, subject to the portfolio overlap between the two schemes not exceeding 50%. Overlap is "
              "computed quarterly as the average of daily overlap values.",
  steps=["Both allowed", "Condition: overlap ≤ 50%"],
  why="The either/or rule was the old position; the permission is conditional, and the condition is a 50% overlap cap, "
      "not zero overlap.",
  current=MFC,
  facts=[fact("Mutual Funds shall be permitted to offer both Value and Contra funds subject to the condition that scheme "
              "portfolio overlap between the two schemes shall not be more than 50%", SEBI_MFCAT),
         fact("The overlap condition shall be computed on a quarterly basis using the daily portfolio overlap values "
              "i.e. the average of daily portfolio overlap values over a quarter", SEBI_MFCAT)])

# Portfolio overlap: sum over common scrips of min(weight in A, weight in B)
wa = {"P": 18, "Q": 12, "R": 25, "S": 10, "T": 35}
wb = {"P": 30, "Q": 20, "R": 5, "U": 25, "V": 20}
assert sum(wa.values()) == 100 and sum(wb.values()) == 100
overlap = sum(min(wa[s], wb[s]) for s in wa if s in wb)
wrong_max = sum(max(wa[s], wb[s]) for s in wa if s in wb)
assert overlap == 35 and wrong_max == 75
Q("008", T, "Types", "Advanced",
  "Under SEBI's February 2026 categorisation, four open-ended hybrid schemes (none uses arbitrage) hold the following "
  "shares of total assets in equity and debt: P – equity 20%, debt 80%; Q – equity 50%, debt 50%; R – equity 72%, debt "
  "28%; S – equity 85%, debt 15%. Which classification is correct?",
  ["P Conservative Hybrid; Q Balanced Hybrid; R Aggressive Hybrid; S fits none of the three",
   "P Conservative Hybrid; Q Aggressive Hybrid; R Balanced Hybrid; S Aggressive Hybrid",
   "P Balanced Hybrid; Q Balanced Hybrid; R Aggressive Hybrid; S Aggressive Hybrid",
   "P Conservative Hybrid; Q Balanced Hybrid; R Aggressive Hybrid; S Aggressive Hybrid"],
  concept="Hybrid fund categories",
  explanation="Conservative Hybrid: equity 10–25%, debt 75–90% (P). Balanced Hybrid: equity and debt each 40–60%, no "
              "arbitrage (Q). Aggressive Hybrid: equity 65–80%, debt 20–35% (R). S, with 85% equity and 15% debt, "
              "exceeds the aggressive hybrid equity ceiling of 80% and is below its debt floor, so it fits none of "
              "the three.",
  steps=["P: 20/80 → Conservative", "Q: 50/50 → Balanced", "R: 72/28 → Aggressive", "S: 85/15 → outside 65–80"],
  why="S cannot be an Aggressive Hybrid (equity cap 80%); P is below the balanced range; Q is not aggressive.",
  computed=True, current=MFC,
  facts=[fact("Conservative Hybrid Fund: equity between 10% and 25%; debt between 75% and 90%. Balanced Hybrid Fund: "
              "equity between 40% and 60%; debt between 40% and 60%; no arbitrage. Aggressive Hybrid Fund: equity between "
              "65% and 80%; debt between 20% 35%", SEBI_MFCAT)])
for _e, _lo, _hi in ((20, 10, 25), (50, 40, 60), (72, 65, 80)):
    assert _lo <= _e <= _hi
assert not (65 <= 85 <= 80)
assert 18 + 12 + 25 == 55

Q("009", T, "Types", "Basic",
  "Under SEBI's framework of February 2026, Life Cycle Funds (target-maturity, glide-path funds) may be launched with "
  "what tenure?",
  ["Minimum 5 years and maximum 30 years, in multiples of 5 years",
   "Minimum 3 years and maximum 25 years, of any length",
   "Minimum 1 year and maximum 10 years, in multiples of 1 year", "Exactly 20 years"],
  concept="Life Cycle Funds",
  explanation="Life Cycle Funds are open-ended funds with a target maturity that follow a glide path across equity, "
              "debt, InvITs, ETCDs and gold/silver ETFs. They may be launched for 5 to 30 years, in multiples of 5 "
              "years, and a mutual fund may have at most 6 such funds open for subscription at a time. The maturity year "
              "appears in the name, e.g. Life Cycle Fund 2055.",
  steps=["Tenure 5–30 years", "Multiples of 5", "Max 6 open for subscription"],
  why="The other tenures do not match the circular.",
  current=MFC,
  facts=[fact("Mutual Fund may launch Life Cycle Funds with a minimum tenure of 5 years and a maximum tenure of 30 years. "
              "Such fund may be launched for tenures in multiple of 5 years and a maximum of 6 funds by a Mutual Fund "
              "can be active for subscription at any given point in time", SEBI_MFCAT)])
Q("009", T, "Types", "Intermediate",
  "Which of the following is a rule for Life Cycle Funds under SEBI's February 2026 framework?",
  ["The maturity year must appear in the scheme name, and a fund with less than one year to maturity may be merged with "
   "the nearest-maturity Life Cycle Fund with unitholders' positive consent",
   "They must invest only in equity until the last year before maturity",
   "They are closed-ended and listed on stock exchanges",
   "They must follow the benchmark of a Large Cap Fund"],
  concept="Life Cycle Fund structure",
  explanation="Life Cycle Funds are open-ended, target-maturity funds following a glide path across equity, debt, "
              "InvITs, ETCDs and gold/silver ETFs. The name must carry the maturity date (e.g. Life Cycle Fund 2055); "
              "when a fund has less than one year left it may be merged with the nearest-maturity fund with positive "
              "unitholder consent; and they follow the benchmark framework of Multi Asset Allocation Funds.",
  steps=["Name carries maturity year", "< 1 year left → merger with consent", "Benchmark as Multi Asset Allocation"],
  why="They hold a glide-path mix, not only equity; they are open-ended; the benchmark is the multi-asset one.",
  current=MFC,
  facts=[fact("as each fund reaches less than 1 year to maturity, such fund may be merged with nearest maturity Life Cycle "
              "Fund with positive consent from the unitholders", SEBI_MFCAT),
         fact("Life Cycle Funds shall follow benchmark framework as prescribed for Multi Asset Allocation Fund. Life Cycle "
              "Funds shall include the maturity date in the nomenclature of the scheme, for e.g. Life Cycle Fund 2055",
              SEBI_MFCAT)])
Q("009", T, "Types", "Intermediate",
  "Under SEBI's February 2026 categorisation, what restriction applies to the debt portion of an Arbitrage Fund?",
  ["Debt exposure is limited to government securities with maturity under one year and repo of government bonds; no "
   "InvITs are permitted", "It may hold only AA+ and above corporate bonds of any maturity",
   "It may hold up to 35% in credit risk bonds", "It must hold only overnight securities"],
  concept="Arbitrage Fund characteristics",
  explanation="An Arbitrage Fund must invest at least 65% in equity and equity-related instruments following an "
              "arbitrage strategy. Its debt exposure is limited to G-secs with maturity of less than one year and repo of "
              "government bonds, and it cannot invest in InvITs.",
  steps=["Equity ≥ 65% (arbitrage)", "Debt: G-secs < 1 year + G-sec repo only", "No InvITs"],
  why="Corporate bonds, credit-risk paper and an overnight-only rule are not the prescribed limits.",
  current=MFC,
  facts=[fact("Arbitrage Fund: Minimum investment in equity & equity related instruments - 65% of total assets ... "
              "Exposure in debt instruments shall be limited to government securities with maturity less than 1 year as "
              "well as repo of government bonds only ... No investment in InvITs permitted", SEBI_MFCAT)])
Q("009", T, "Types", "Intermediate",
  "SEBI's revised list of debt fund categories (February 2026) includes an 'Ultra Short to Short Term Fund'. What "
  "Macaulay duration must its portfolio have?",
  ["Between 6 months and 12 months", "Between 3 months and 6 months", "Between 1 year and 3 years",
   "Up to 91 days, by residual maturity"],
  concept="Debt fund duration buckets",
  explanation="The revised table has an Ultra Short Term Fund (portfolio Macaulay duration 3–6 months), an Ultra Short "
              "to Short Term Fund (6–12 months) and a Short Term Fund (1–3 years). A Liquid Fund is defined by "
              "maturity of up to 91 days, not by duration.",
  steps=["3–6 m: Ultra Short Term", "6–12 m: Ultra Short to Short Term", "1–3 y: Short Term"],
  why="3–6 months and 1–3 years are the neighbouring categories; up to 91 days is the liquid fund rule.",
  current=MFC,
  facts=[fact("Ultra Short to Short Term Fund: Investment in Debt & Money Market instruments such that the Macaulay "
              "duration of the portfolio is between 6 months to 12 months", SEBI_MFCAT),
         fact("Ultra Short Term Fund: Macaulay duration of the portfolio is between 3 months to 6 months; Short Term "
              "Fund: between 1 year to 3 years", SEBI_MFCAT)])

limit, start_ov = 50, 74
excess = start_ov - limit
y1 = start_ov - 0.35 * excess
y2 = y1 - 0.35 * excess
y3 = y2 - 0.30 * excess
assert excess == 24 and abs(y1 - 65.6) < 1e-9 and abs(y2 - 57.2) < 1e-9 and abs(y3 - 50) < 1e-9
Q("009", T, "Types", "Advanced",
  "An existing thematic equity fund's portfolio overlaps 74% with the fund house's other equity schemes (other than "
  "its large cap scheme) on the date of SEBI's February 2026 circular. Following SEBI's suggested three-year glide "
  "path to the 50% overlap limit, to what level should the overlap be brought by the end of Year 2?",
  ["57.2%", "65.6%", "62.0%", "50.0%"],
  concept="Glide path for sectoral/thematic overlap",
  explanation="The excess over the 50% limit is 74 − 50 = 24 percentage points. The glide path realigns 35% of the "
              "excess in Year 1, a further 35% in Year 2 and the remaining 30% in Year 3. By the end of Year 2, "
              "70% of 24 = 16.8 points has been removed: 74 − 16.8 = 57.2%. Schemes still above the limit after three "
              "years must be merged.",
  steps=["Excess = 24", "Year 1: −8.4 → 65.6%", "Year 2: −8.4 → 57.2%", "Year 3: −7.2 → 50%"],
  why="65.6% is the Year 1 level; 62% assumes equal cuts of 12 points a year; 50% is the Year 3 level.",
  computed=True, current=MFC,
  facts=[fact("For any scheme offering in sectoral/thematic equity category, Mutual Funds shall ensure that no more than "
              "50% of the schemes portfolios would overlap with other equity schemes in sectoral/thematic category and "
              "other equity schemes categories except for large cap scheme", SEBI_MFCAT),
         fact("Glide path: Year 1 - 35% of the excess overlap; Year 2 - Additional 35%; Year 3 - Remaining 30%; "
              "existing schemes to comply within 3 years, failing which they shall be mandatorily merged", SEBI_MFCAT)])
assert 74 - 12 == 62

Q("010", T, "Types", "Basic",
  "Under SEBI's mutual fund categorisation (February 2026), what minimum share of its total assets must an index fund "
  "or ETF invest in the securities of the index it tracks?",
  ["95%", "80%", "65%", "100%"],
  concept="Passive schemes",
  explanation="Index funds and ETFs, grouped under 'Other Schemes', must invest at least 95% of total assets in the "
              "securities of the index being replicated or tracked. Fund of funds must likewise put at least 95% in the "
              "underlying fund.",
  steps=["Index fund / ETF ≥ 95% in index securities"],
  why="80% and 65% are minimums for active equity categories; 100% is not required.",
  current=MFC,
  facts=[fact("Index Funds/ ETFs: Minimum investment in securities of a particular index (which is being replicated/ "
              "tracked) - 95% of total assets", SEBI_MFCAT)])
Q("010", T, "Types", "Intermediate",
  "SEBI's February 2026 categorisation introduced sectoral debt funds, which must invest at least 80% in AA+ and above "
  "rated debt of a particular sector. In which of the following sectors is such a fund NOT permitted?",
  ["Telecommunications", "Housing", "Energy", "Real Estate"],
  concept="Sectoral debt funds",
  explanation="Sectoral debt funds may be launched only in Financial Services, Energy, Infrastructure, Housing and Real "
              "Estate, and only where enough investment-grade paper of that sector is available. Telecommunications is "
              "not on the list.",
  steps=["Permitted: Financial Services, Energy, Infrastructure, Housing, Real Estate"],
  why="Housing, Energy and Real Estate are all on the permitted list.",
  current=MFC,
  facts=[fact("Sectoral Fund (debt): Minimum investment in debt & debt related instruments of a particular sector across "
              "duration (only in AA+ and above rated corporate bonds) - 80% of total assets. Sectoral Debt Funds may be "
              "launched in following sectors: Financial Services, Energy, Infrastructure, Housing, Real Estate",
              SEBI_MFCAT)])
Q("010", T, "Types", "Intermediate",
  "An Overnight Fund invests in securities maturing in one day. Under SEBI's February 2026 categorisation, what "
  "exception is allowed?",
  ["Up to 5% of net assets may be placed in G-secs or T-bills with residual maturity of up to 30 days, for use as "
   "margin and collateral",
   "Up to 10% of net assets may be placed in commercial paper of up to 91 days for higher yield",
   "Up to 20% of net assets may be held in liquid fund units",
   "Up to 5% of net assets may be invested in listed equity for liquidity"],
  concept="Overnight Fund characteristics",
  explanation="Overnight funds may deploy not more than 5% of net assets in G-secs and/or T-bills with residual "
              "maturity of up to 30 days, only to place them as margin and collateral for certain transactions.",
  steps=["Overnight securities (1 day) + up to 5% in G-sec/T-bill ≤ 30 days for margin"],
  why="CP, liquid fund units and equity are not permitted under this exception.",
  current=MFC,
  facts=[fact("Overnight funds can deploy, not exceeding, 5% of the net assets of the scheme in G-secs and/or T-bills "
              "with a residual maturity of upto 30 days for the purpose of placing the same as margin and collateral "
              "for certain transactions", SEBI_MFCAT)])

eq, debt, gold = 45, 45, 10
assert 35 <= eq <= 50 and 25 <= debt <= 50 and 0 <= gold <= 10 and eq + debt + gold == 100
for e_, d_, g_ in ((55, 40, 5), (40, 48, 12), (50, 20, 30)):
    assert e_ + d_ + g_ == 100 and not (35 <= e_ <= 50 and 25 <= d_ <= 50 and g_ <= 10)
Q("010", T, "Types", "Advanced",
  "A Life Cycle Fund launched with a 20-year maturity now has 4 years left to maturity and holds no arbitrage "
  "positions. Which allocation complies with the glide path in SEBI's February 2026 framework?",
  ["Equity 45%, debt 45%, gold/silver ETFs 10%", "Equity 55%, debt 40%, gold/silver ETFs 5%",
   "Equity 40%, debt 48%, gold/silver ETFs 12%", "Equity 50%, debt 20%, gold/silver ETFs 30%"],
  concept="Life Cycle Fund glide path",
  explanation="With 3–5 years to maturity, a Life Cycle Fund must hold 35–50% in equity, 25–50% in debt and 0–10% in "
              "gold/silver ETFs, ETCDs and InvITs. Only 45/45/10 meets all three ranges.",
  steps=["3–5 years left: equity 35–50, debt 25–50, others 0–10", "Check each option"],
  why="55% equity exceeds 50%; 12% in gold/silver exceeds 10%; 20% debt is below 25% and 30% in gold exceeds 10%.",
  computed=True, current=MFC,
  facts=[fact("For Life Cycle Funds with maturity of 20 years: 3-5 Years to maturity - Investment in Equity 35-50%; "
              "Debt 25-50%; Gold/Silver ETFs/ETCDs/InvITs 0-10%", SEBI_MFCAT)])

# ============================================================================================ Money Market
T = "Money Market"
ST = "Instruments: T-bills, CP, CD, call money"
MMO = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63933"     # Money Market Operations, 5 Nov 2026
TB_NOV4 = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63918"  # T-bill full auction result 4 Nov 2026

Q("008", T, ST, "Basic",
  "Under RBI's Certificate of Deposit Directions, 2021, on what basis are CDs issued?",
  ["T+1, where T is the date on which the offer period for the CD issue closes", "T+4, where T is the deal date",
   "T+0 only, on the date of the board resolution", "T+7, where T is the date of application to RBI"],
  concept="Issuance of CDs",
  explanation="CDs are issued on a T+1 basis, T being the date of closure of the offer period. (Primary CP and NCD "
              "issues, by contrast, may settle up to T+4 working days.) CDs are in demat form only.",
  steps=["CD issue: T+1 from offer closure"],
  why="T+4 is the CP/NCD primary settlement limit; the other bases are not in the Directions.",
  facts=[fact("CDs shall be issued on a T+1 basis where T represents the date of closure of the offer period for issuance "
              "of the CDs", RBI_CD)])
Q("008", T, ST, "Basic",
  "How may commercial paper (CP) be priced at issue under RBI's Directions of 2024?",
  ["Only at a discount to face value", "At a discount or with a fixed coupon", "Only with a floating coupon linked to "
   "the repo rate", "At par, with interest paid on maturity"],
  concept="Discount instruments",
  explanation="CPs shall be issued at a discount to the face value. Short-term NCDs, in contrast, may be issued at a "
              "discount or with a fixed or floating coupon.",
  steps=["CP → discount only", "NCD (≤ 1 year) → discount, fixed or floating coupon"],
  why="Coupon-bearing issue (fixed or floating) is allowed for NCDs, not CPs; CP is not issued at par with interest.",
  facts=[fact("CPs shall be issued at a discount to the face value. NCDs shall be issued at a discount to the face value "
              "or with fixed or floating rate coupon", RBI_CP)])
Q("008", T, ST, "Intermediate",
  "In any primary issuance of commercial paper or short-term NCDs, what is the limit on subscription by individuals "
  "under RBI's 2024 Directions?",
  ["All individuals together, including HUFs, may not take more than 25% of the amount issued",
   "Individuals cannot subscribe at all", "Each individual may take up to ₹5 lakh only",
   "Individuals together may take up to 50% of the amount issued"],
  concept="Retail participation in CP/NCD",
  explanation="All residents (and non-residents to the extent FEMA permits) may invest in CPs and NCDs, but total "
              "subscription by all individuals, including Hindu Undivided Families, in a primary issuance cannot exceed "
              "25% of the total amount issued. ₹5 lakh is the minimum denomination, not a cap.",
  steps=["Individuals + HUFs ≤ 25% of the issue"],
  why="Individuals are not barred; ₹5 lakh is the minimum denomination; 50% is not the limit.",
  facts=[fact("Total subscription by all individuals, including Hindu Undivided Families, in any primary issuance of CPs "
              "or NCDs shall not exceed 25 per cent of the total amount issued", RBI_CP)])
Q("008", T, ST, "Intermediate",
  "A company defaults on the redemption of its commercial paper. What must it do under RBI's 2024 Directions?",
  ["Inform the IPA before 5:00 pm on the day of default and publicly disseminate the default, e.g. on its website",
   "Inform RBI within 30 days and nothing more", "Roll the CP over automatically for one month",
   "Inform only the credit rating agency at its next review"],
  concept="Default in CP",
  explanation="An issuer that defaults on a coupon or redemption of a CP/NCD must inform the IPA before 5:00 pm on the "
              "date of default (and the debenture trustee for NCDs) and publicly disseminate the default. The IPA reports "
              "it on CCIL's F-TRAC platform by 5:30 pm, and the issuer cannot issue CPs/NCDs until it repays or six "
              "months pass.",
  steps=["Inform IPA before 5 pm", "Public dissemination", "IPA reports on F-TRAC by 5:30 pm"],
  why="Automatic rollover is not allowed, and RBI-only or rating-agency-only intimation is not the rule.",
  facts=[fact("The issuer who has defaulted on the repayment of a coupon/redemption, partially or in full, of a CP and/or "
              "NCD shall inform the details of any default in payments related to a CP/NCD to the IPA before 5:00 pm on "
              "the date of the default ... Information about any default in payments related a CP/NCD shall be publicly "
              "disseminated (e.g., through its website) by the issuer", RBI_CP)])
Q("008", T, ST, "Intermediate",
  "Under RBI's 2024 Directions, within what time must a primary issuance of commercial paper be settled, i.e. funds paid "
  "to the issuer and CPs issued to investors?",
  ["Within T+4 working days of the deal date", "On the same day (T+0) only", "Within T+1 working day of the deal "
   "date", "Within 15 days of the board resolution"],
  concept="Primary settlement of CP/NCD",
  explanation="Primary issuances of CPs and NCDs, including both payment of funds and issue of the instruments, must be "
              "settled within T+4 working days, where T is the date on which the trade details including price are "
              "agreed. Secondary OTC trades settle T+0 or T+1, and CDs are issued on a T+1 basis.",
  steps=["Primary CP/NCD: ≤ T+4", "Secondary OTC: T+0 or T+1"],
  why="T+0/T+1 is the secondary-market settlement cycle; T+1 applies to CD issuance; the board resolution is not the "
      "reference date.",
  facts=[fact("The primary issuances of CPs and NCDs ... shall be settled within a period not exceeding T+4 working days, "
              "where T represents the deal date", RBI_CP),
         fact("The settlement cycle for OTC trades in CPs and NCDs shall be either T+0 or T+1", RBI_CP)])
Q("008", T, ST, "Intermediate",
  "Which of the following is NOT permitted while issuing commercial paper under RBI's 2024 Directions?",
  ["Issuing the CP with a call or put option", "Credit enhancement by a bank through a stand-by facility",
   "Issuing the CP in dematerialised form", "Appointing a scheduled commercial bank as Issuing and Paying Agent"],
  concept="CP issuance conditions",
  explanation="Issuance of a CP/NCD with options (call/put) is not permitted, and it cannot be underwritten or "
              "co-accepted. Banks and AIFIs may provide credit enhancement such as stand-by assistance; CPs must be in "
              "demat form; and an IPA, which must be a scheduled commercial bank, is required for each issue.",
  steps=["Options, underwriting, co-acceptance → barred", "Demat, IPA, credit enhancement → required/allowed"],
  why="Credit enhancement is allowed; demat form and an SCB as IPA are mandatory.",
  facts=[fact("Issuance of a CP/NCD with options (call/put) is not permitted. Issuance of a CP/NCD is not permitted to be "
              "underwritten or co-accepted", RBI_CP),
         fact("Issuing and Paying Agent (IPA) means a Scheduled Commercial Bank undertaking duties and responsibilities "
              "specified under paragraph 7(a) of these Directions", RBI_CP)])

iss = 600
assert iss * 25 / 100 == 150
Q("008", T, ST, "Advanced",
  "A company with an 'A2+' rating plans a ₹600 crore CP issue of 120 days. 2,400 individuals want to subscribe "
  "₹10 lakh each, and an NBFC (a related party of the company) wants ₹100 crore. Applying RBI's 2024 Directions, which "
  "statement is correct?",
  ["Individuals can be allotted at most ₹150 crore in all, and the related NBFC cannot invest at all",
   "Individuals can be allotted the full ₹240 crore, and the NBFC can take ₹100 crore",
   "Individuals can be allotted at most ₹150 crore, and the NBFC can take ₹100 crore",
   "The issue cannot be made, as an 'A2+' rating is below the minimum"],
  concept="Investor limits in CP",
  explanation="Individuals (including HUFs) may take at most 25% of a primary issue: 25% × 600 = ₹150 crore, so the "
              "₹240 crore of demand (2,400 × ₹10 lakh) cannot be met in full. No person, resident or non-resident, may "
              "invest in CPs/NCDs issued by related parties. 'A2+' is above the minimum rating of A3, so the issue is "
              "allowed.",
  steps=["Individual cap = 0.25 × 600 = ₹150 crore", "Related-party investment barred", "A2+ ≥ A3 → eligible"],
  why="₹240 crore exceeds the 25% cap; the related NBFC is barred; A2+ is better than the A3 minimum.",
  computed=True,
  facts=[fact("Total subscription by all individuals, including Hindu Undivided Families, in any primary issuance of CPs "
              "or NCDs shall not exceed 25 per cent of the total amount issued", RBI_CP),
         fact("No person, resident or non-resident, can invest in CPs and NCDs issued by related parties either in the "
              "primary or through the secondary market", RBI_CP),
         fact("The minimum credit rating ... for the issuance of CPs and NCDs shall be 'A3'", RBI_CP)])
assert 2400 * 10 / 100 == 240

import datetime as _dt
cp_issue = _dt.date(2027, 1, 4)
ncd_issue = _dt.date(2027, 1, 4)
cp_bb = cp_issue + _dt.timedelta(days=7)
ncd_bb = ncd_issue + _dt.timedelta(days=90)
assert cp_bb == _dt.date(2027, 1, 11) and ncd_bb == _dt.date(2027, 4, 4)
Q("008", T, ST, "Advanced",
  "Consider the following statements about RBI's 2024 Directions on CPs and short-term NCDs:\n"
  "I. The issuer must make funds for redemption available to the IPA by 3:00 pm on the redemption date.\n"
  "II. The debenture trustee reports outstanding NCDs and defaults to RBI quarterly, within 15 days of the quarter's "
  "end.\n"
  "III. Depositories report CP and NCD holdings to RBI only once a quarter.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Repayment and reporting in CP/NCD markets",
  explanation="I is correct: redemption funds must reach the IPA by 3:00 pm on the redemption date, and repayment is "
              "routed through the IPA. II is correct: the debenture trustee reports quarterly, within 15 days of the end "
              "of the quarter. III is wrong: depositories report fortnightly (on the 15th and the last day of the "
              "month).",
  steps=["I ✓", "II ✓", "III ✗ (fortnightly)"],
  why="Any option containing III is wrong.",
  facts=[fact("The issuer shall make the funds for redemption available to the IPA by 3:00 P.M. on the redemption date",
              RBI_CP),
         fact("The Debenture Trustee shall report the details of the outstanding amount of NCDs and the particulars of "
              "default in repayment of NCD, at quarterly intervals (within 15 days from the end of the quarter)", RBI_CP),
         fact("The depositories shall report to the Reserve Bank, the details of the CPs and NCDs held with them ... at "
              "fortnightly intervals (on the 15th day and on the last day of the month)", RBI_CP)])

d_def = _dt.date(2027, 2, 10)
d_full = _dt.date(2027, 5, 20)
six_m = _dt.date(2027, 8, 10)
assert min(d_full, six_m) == _dt.date(2027, 5, 20)
Q("008", T, ST, "Advanced",
  "A company defaults on a CP redemption on 10 February 2027 and repays the defaulted amount in full on 20 May 2027. "
  "Under RBI's 2024 Directions, from when can it issue CPs or NCDs again?",
  ["From 20 May 2027, the date of full repayment, as that is earlier than six months after the default",
   "From 10 August 2027, six months after the default, irrespective of repayment",
   "Only after one year from the date of default",
   "Only after a fresh rating of A1+ is obtained"],
  concept="Bar on issuance after default",
  explanation="After a default, the issuer cannot issue CPs or NCDs till full repayment of the defaulted obligation or "
              "six months after the date of default, whichever is earlier. Full repayment (20 May 2027) comes before "
              "10 August 2027, so the bar lifts on 20 May 2027. The default must also be reported to the IPA before "
              "5 pm on the day of default and publicly disseminated.",
  steps=["Six months after 10 Feb 2027 = 10 Aug 2027", "Full repayment = 20 May 2027", "Earlier = 20 May 2027"],
  why="The six-month date applies only if repayment is later; there is no one-year bar or A1+ requirement.",
  computed=True,
  facts=[fact("In the event of default of a CP / NCD, the issuer shall not be allowed to issue CPs or NCDs till full "
              "repayment of the defaulted obligation or six months after the date of default, whichever is earlier",
              RBI_CP)])

Q("009", T, ST, "Basic",
  "Under RBI's directions, during what hours may primary issuance and secondary trading in Certificates of Deposit "
  "take place?",
  ["9:00 am to 5:00 pm on a business day", "9:00 am to 7:00 pm on a business day", "10:00 am to 3:30 pm on a business "
   "day", "Round the clock, all days"],
  concept="Market timings for CDs and CPs",
  explanation="Primary issuance and secondary trading of CDs (and of CPs/NCDs) take place between 9:00 am and 5:00 pm "
              "on a business day, or as RBI specifies. 9 am to 7 pm is the call money market window.",
  steps=["CD/CP market hours: 9 am – 5 pm"],
  why="9 am–7 pm is for call money; the others are not RBI's timings.",
  facts=[fact("Primary issuance and secondary market trading hours shall be between 9:00 AM and 5:00 PM on a business day "
              "or as specified by the Reserve Bank from time to time", RBI_CD)])
Q("009", T, ST, "Basic",
  "Which of the following may issue commercial paper under RBI's 2024 Directions, provided their fund-based facilities "
  "are standard?",
  ["InvITs and REITs", "Individuals", "Hindu Undivided Families", "Partnership firms of any size"],
  concept="Eligible CP issuers",
  explanation="Companies, NBFCs (including HFCs), InvITs and REITs, AIFIs and other bodies corporate with net worth of "
              "₹100 crore that may lawfully issue debt can issue CPs; co-operative societies and LLPs with net worth of "
              "₹100 crore may also issue. Individuals, HUFs and ordinary partnership firms cannot.",
  steps=["Issuers: companies, NBFCs/HFCs, InvITs, REITs, AIFIs, others as specified"],
  why="Individuals, HUFs and ordinary partnership firms are not eligible issuers.",
  facts=[fact("CPs and NCDs may be issued by the following entities subject to the condition that all fund-based "
              "facilities availed, if any, by the issuer from banks/ AIFIs / NBFCs are classified as Standard at the time "
              "of issue: Companies; NBFCs, including Housing Finance Companies (HFCs); InvITs and REITs; All India "
              "Financial Institutions (AIFIs)", RBI_CP)])
Q("009", T, ST, "Intermediate",
  "Which of the following entities is eligible to issue commercial paper under RBI's 2024 Directions?",
  ["A limited liability partnership with a net worth of ₹120 crore whose bank loans are all standard",
   "A co-operative society with a net worth of ₹80 crore", "A company whose working capital loan from a bank is an NPA",
   "A limited liability partnership with a net worth of ₹60 crore"],
  concept="Eligible CP issuers",
  explanation="Companies, NBFCs (including HFCs), InvITs, REITs, AIFIs and other permitted bodies corporate can issue "
              "CPs. Co-operative societies and LLPs can issue CPs only if their net worth is at least ₹100 crore. Every "
              "issuer's fund-based facilities from banks, AIFIs and NBFCs must be standard at the time of issue.",
  steps=["LLP/co-op: net worth ≥ ₹100 crore", "All issuers: fund-based facilities standard"],
  why="₹80 crore and ₹60 crore are below the ₹100 crore floor; an NPA account disqualifies a company.",
  facts=[fact("Co-operative societies and limited liability partnerships with a minimum net-worth of ₹100 crore, may also "
              "issue CPs under these Directions, subject to the condition that all fund-based facilities availed, if "
              "any, by the issuer from banks/ AIFIs / NBFCs are classified as Standard at the time of issue", RBI_CP)])

ov = {"call": 14431.90, "triparty": 572289.15, "market_repo": 195543.41, "corp_repo": 7492.65}
tot = sum(ov.values())
assert abs(tot - 789757.11) < 0.01
sh_tri = 100 * ov["triparty"] / tot
sh_call = 100 * ov["call"] / tot
assert round(sh_tri, 1) == 72.5 and round(sh_call, 1) == 1.8
Q("009", T, ST, "Advanced",
  "RBI's money market data for 5 November 2026 show overnight volumes (₹ crore, one leg) of: call money 14,431.90 "
  "(weighted average rate 5.63%), triparty repo 5,72,289.15 (5.53%), market repo 1,95,543.41 (5.61%) and repo in "
  "corporate bonds 7,492.65 (5.71%). Which statement is correct?",
  ["Triparty repo made up about 72.5% of the overnight volume, while call money made up under 2%",
   "Call money was the largest segment, at about 72.5% of the overnight volume",
   "Market repo made up about half of the overnight volume",
   "The segment with the highest rate also had the highest volume"],
  concept="Composition of the overnight money market",
  explanation="Total overnight volume = 14,431.90 + 5,72,289.15 + 1,95,543.41 + 7,492.65 = ₹7,89,757.11 crore. "
              "Triparty repo is 5,72,289.15 ÷ 7,89,757.11 ≈ 72.5%; call money is about 1.8%; market repo about 24.8%. "
              "The highest rate (5.71%, corporate bond repo) belongs to the smallest segment.",
  steps=["Total = 7,89,757.11", "Triparty share ≈ 72.5%", "Call share ≈ 1.8%"],
  why="Call money is the smallest overnight segment; market repo is about a quarter, not half; corporate bond repo has "
      "the highest rate but the smallest volume.",
  computed=True, current=ca("2026-11-05"),
  facts=[fact("Money Market Operations as on November 05, 2026: Call Money 14,431.90 (5.63); Triparty Repo 5,72,289.15 "
              "(5.53); Market Repo 1,95,543.41 (5.61); Repo in Corporate Bond 7,492.65 (5.71); Overnight total "
              "7,89,757.11 (5.55)", MMO)])
assert round(100 * ov["market_repo"] / tot, 1) == 24.8

bc91 = 20465.330 / 8000
bc364 = 18875.000 / 7000
assert round(bc91, 2) == 2.56 and round(bc364, 2) == 2.70
Q("009", T, ST, "Advanced",
  "In RBI's Treasury Bill auction of 4 November 2026, competitive bids worth ₹20,465.33 crore were received against a "
  "notified ₹8,000 crore for the 91-day bill, and ₹18,875 crore against ₹7,000 crore for the 364-day bill. The cut-off "
  "yields were 5.8970% and 6.6485%. Which statement is correct?",
  ["The 364-day bill had the higher bid-cover ratio (about 2.70 against 2.56) and the higher cut-off yield",
   "The 91-day bill had the higher bid-cover ratio (about 2.70 against 2.56)",
   "Both bills had the same bid-cover ratio of about 2.6",
   "The 364-day bill had the lower cut-off yield, as it was more heavily bid"],
  concept="Reading a T-bill auction result",
  explanation="Bid-cover ratio = competitive bids received ÷ notified amount. 91-day: 20,465.33 ÷ 8,000 ≈ 2.56. "
              "364-day: 18,875 ÷ 7,000 ≈ 2.70. The 364-day cut-off yield (6.6485%) was also higher than the 91-day "
              "yield (5.8970%), as is usual for the longer tenor.",
  steps=["91-day: 20,465.33/8,000 = 2.56", "364-day: 18,875/7,000 = 2.70", "6.6485% > 5.8970%"],
  why="The ratios are swapped in the second option and not equal; the 364-day yield was higher, not lower.",
  computed=True, current=ca("2026-11-04"),
  facts=[fact("91-Day: notified 8,000; competitive bids received 20,465.330; cut-off price 98.5511 (YTM 5.8970%). 364-Day: "
              "notified 7,000; competitive bids received 18,875.000; cut-off price 93.7820 (YTM 6.6485%)", TB_NOV4)])

Q("010", T, ST, "Basic",
  "What grace period is allowed for repayment of a Certificate of Deposit on maturity under RBI's CD Directions, 2021?",
  ["No grace period", "3 working days", "7 days", "One month"],
  concept="Repayment of CDs",
  explanation="There is no grace period for repayment of CDs; the same applies to CPs and short-term NCDs under the 2024 "
              "Directions.",
  steps=["CD/CP/NCD repayment → no grace period"],
  why="No grace period of any length is provided.",
  facts=[fact("There will be no grace period for repayment of CDs", RBI_CD),
         fact("There will be no grace period for repayment of CPs/NCDs", RBI_CP)])
Q("010", T, ST, "Basic",
  "Under RBI's 2024 Directions on Commercial Paper and NCDs, who can act as the Issuing and Paying Agent (IPA) for an "
  "issue?",
  ["A scheduled commercial bank", "A SEBI-registered stock broker", "A credit rating agency",
   "Any NBFC with a net worth of ₹100 crore"],
  concept="Role of the IPA",
  explanation="An IPA must be appointed for each CP and NCD issue, and the IPA must be a scheduled commercial bank. "
              "Subscriptions are routed through the IPA, which verifies documents, issues an IPA certificate and reports "
              "primary issuances on CCIL's F-TRAC platform by 5:30 pm.",
  steps=["IPA = scheduled commercial bank; one per issue"],
  why="Brokers, rating agencies and NBFCs cannot act as IPA.",
  facts=[fact("Issuing and Paying Agent (IPA) means a Scheduled Commercial Bank undertaking duties and responsibilities "
              "specified under paragraph 7(a) of these Directions", RBI_CP),
         fact("An IPA shall be appointed for each issuance of a CP and an NCD ... The subscription to the primary issue "
              "of a CP/NCD shall be routed through the IPA", RBI_CP)])
Q("010", T, ST, "Basic",
  "Who may invest in Certificates of Deposit under RBI's Certificate of Deposit Directions, 2021?",
  ["All persons resident in India", "Only banks and mutual funds", "Residents and non-residents alike, without limit",
   "Only corporates and institutions, not individuals"],
  concept="Eligible investors in CDs",
  explanation="CDs may be issued to all persons resident in India, including individuals. The Directions do not list "
              "non-residents as eligible investors.",
  steps=["CD investors: all residents"],
  why="Investors are not limited to banks, mutual funds or institutions; non-residents are not covered.",
  facts=[fact("CDs may be issued to all persons resident in India", RBI_CD)])
Q("010", T, ST, "Intermediate",
  "Funds raised through commercial paper are normally meant for current assets and operating expenses. What must the "
  "issuer do regarding end-use under RBI's 2024 Directions?",
  ["Disclose the end-use in the offer document and give the IPA a CEO/CFO certificate on use of proceeds within 3 "
   "months of issue or on maturity, whichever is earlier",
   "Obtain RBI's prior approval for any use other than working capital",
   "Submit an auditor's certificate to SEBI within one year",
   "Nothing, as CP is unsecured and end-use is not monitored"],
  concept="End-use of CP proceeds",
  explanation="End-use must be disclosed in the offer document (with the exact purpose if it is not current assets or "
              "operating expenses). The issuer gives the IPA a CEO/CFO certificate that proceeds were used as disclosed, "
              "within 3 months of issue or on maturity, whichever is earlier.",
  steps=["Disclose end-use", "CEO/CFO certificate → IPA within 3 months or on maturity (earlier)"],
  why="No RBI approval, SEBI certificate or exemption from monitoring is provided for.",
  facts=[fact("The issuer shall submit a certificate from the Chief Executive Officer/Chief Financial Officer (CEO/CFO) to "
              "the IPAs concerned that the proceeds of CPs and NCDs have been used for the disclosed purposes ... The "
              "certificate shall be provided to the IPA within 3 months of the issue of CP/NCD or on maturity of the "
              "issue, whichever is earlier", RBI_CP)])
Q("010", T, ST, "Intermediate",
  "How are secondary market trades in CPs and CDs to be reported under RBI's directions?",
  ["By each counterparty on CCIL's F-TRAC platform, with time stamp, within 15 minutes of execution",
   "By the issuer to RBI at the end of each fortnight", "By the stock exchange to SEBI on T+1",
   "By the IPA to FIMMDA by 5:30 pm on the trade date"],
  concept="Trade reporting in the money market",
  explanation="All OTC and exchange secondary trades in CPs/NCDs and CDs must be reported with time stamp within "
              "15 minutes of execution (when price is agreed) on F-TRAC, CCIL's trade repository, by each counterparty. "
              "Primary issuance and buybacks are reported by 5:30 pm on the day; depositories report holdings to RBI "
              "fortnightly.",
  steps=["Secondary trades → F-TRAC, 15 minutes, both counterparties"],
  why="Fortnightly reports are made by depositories; 5:30 pm applies to primary issues and buybacks; FIMMDA and "
      "SEBI are not the reporting channels.",
  facts=[fact("All secondary market transactions in CPs and NCDs ... shall be reported with time stamp within 15 minutes "
              "of execution ... on the F-TRAC platform by each counterparty to the transaction", RBI_CP),
         fact("All secondary market transactions executed in OTC market and/or on the recognised stock exchanges in CDs "
              "shall be reported, with time stamp, within 15 minutes of execution ... on the F-TRAC platform by each "
              "counterparty", RBI_CD)])

cd_issue = _dt.date(2026, 12, 1)
assert cd_issue + _dt.timedelta(days=7) == _dt.date(2026, 12, 8)
Q("010", T, ST, "Advanced",
  "A bank issued a 180-day CD on 1 December 2026 and wants to buy back part of it. Consider:\n"
  "I. It may make the buyback offer from 8 December 2026, seven days after issue.\n"
  "II. It may buy back only from the investors it chooses, at face value.\n"
  "III. The CDs bought back are extinguished, and the buyback is reported on F-TRAC by 5:30 pm that day.\n"
  "Which of the above is/are correct under RBI's CD Directions, 2021?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Buyback of CDs",
  explanation="Buyback is allowed only 7 days after issue (1 Dec + 7 = 8 Dec 2026), so I is correct. The offer must go to "
              "all investors in that issue on identical terms at the prevailing market price, so II is wrong. CDs "
              "bought back are extinguished and the issuer reports the buyback on F-TRAC by 5:30 pm, so III is correct.",
  steps=["I: issue + 7 days → correct", "II: all investors, market price → wrong", "III: extinguished, F-TRAC 5:30 pm → "
         "correct"],
  why="Any option containing II is wrong.",
  computed=True,
  facts=[fact("Buyback of CDs can be made only 7 days after the date of issue of the CD; the buyback offer shall be made "
              "to all investors in a particular CD issue on identical terms and conditions; buyback of CDs shall be at "
              "the prevailing market price; CDs bought back, partially or in full, shall be extinguished", RBI_CD),
         fact("Details of the buyback of a CD shall be reported by the issuer on the F-TRAC platform by 5.30 PM on the day "
              "of buyback", RBI_CD)])
Q("010", T, ST, "Advanced",
  "Consider the following statements about RBI's 2024 Directions on CPs and short-term NCDs:\n"
  "I. Non-bank entities, including corporates, may give an unconditional and irrevocable guarantee to enhance the "
  "credit of CPs issued by a group entity, with disclosures.\n"
  "II. Secondary OTC trades in NCDs may be settled bilaterally, but OTC trades in CPs must settle on a DvP basis "
  "through a clearing corporation or other RBI-approved mechanism.\n"
  "III. A debenture trustee must be appointed for every CP issue.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Credit enhancement and settlement of CP/NCD",
  explanation="I is correct: non-bank entities may guarantee CPs/NCDs of group entities. II is correct: OTC CP trades "
              "settle DvP through a clearing corporation (or approved mechanism), whereas NCD trades may also be settled "
              "bilaterally. III is wrong: a debenture trustee is required for each NCD issue, not for CPs.",
  steps=["I ✓ (group guarantee)", "II ✓ (CP DvP; NCD may be bilateral)", "III ✗ (trustee only for NCDs)"],
  why="Options with III are wrong, since a debenture trustee is an NCD requirement only.",
  facts=[fact("Non-bank entities (including corporates) may provide unconditional and irrevocable guarantee for credit "
              "enhancement of CPs and NCDs issued by a group entity subject to making appropriate disclosures", RBI_CP),
         fact("All OTC secondary market transactions in CPs ... shall be settled on a DvP basis through the clearing "
              "corporation of any recognised stock exchange, or any other mechanism approved by the Reserve Bank. All OTC "
              "secondary market transactions in NCDs ... shall be settled bilaterally, or on a DvP basis", RBI_CP),
         fact("An IPA shall be appointed for each issuance of a CP and an NCD. A Debenture Trustee shall also be "
              "appointed for each issuance of an NCD", RBI_CP)])

# ============================================================================================ Budget and Economic Survey
T = "Budget and Economic Survey"
UB, ESH, FT = "Union Budget highlights", "Economic Survey highlights", "Fiscal terms"
ES_PRINT = "https://theprint.in/economy/economic-survey-2025-26-the-top-10-takeaways-for-india/2839818"
ESD = ca("2026-01-29")       # Economic Survey 2025-26 tabled

Q("008", T, UB, "Basic",
  "The Union Budget 2026-27 raised the Securities Transaction Tax (STT) on options premium to:",
  ["0.15%, from 0.1%", "0.05%, from 0.02%", "0.125%, from 0.1%", "0.25%, from 0.15%"],
  concept="STT changes in Budget 2026-27",
  explanation="STT on options premium and on exercise of options was raised to 0.15%, from 0.1% and 0.125% "
              "respectively. STT on futures was raised to 0.05% from 0.02%.",
  steps=["Options premium: 0.1% → 0.15%", "Exercise of options: 0.125% → 0.15%", "Futures: 0.02% → 0.05%"],
  why="0.05% from 0.02% is the futures change; 0.125% was the old rate on exercise; 0.25% is not a Budget rate.",
  current=BUD,
  facts=[fact("STT on Futures to be raised to 0.05 percent from present 0.02 percent. STT on options premium and exercise "
              "of options to be raised to 0.15 percent from the present rate of 0.1 percent and 0.125 percent "
              "respectively", BUDGET)])
Q("008", T, UB, "Basic",
  "As recommended by the Sixteenth Finance Commission, how much did the Union Budget 2026-27 provide to the States as "
  "Finance Commission grants for 2026-27?",
  ["₹1.4 lakh crore", "₹15.26 lakh crore", "₹4.93 lakh crore", "₹2.0 lakh crore"],
  concept="Finance Commission grants",
  explanation="The Government provided ₹1.4 lakh crore to the States for FY 2026-27 as Finance Commission grants, "
              "including grants to rural and urban local bodies and for disaster management. Tax devolution is "
              "separately ₹15.26 lakh crore.",
  steps=["FC grants 2026-27 = ₹1.4 lakh crore"],
  why="₹15.26 lakh crore is tax devolution; ₹4.93 lakh crore is grants for creation of capital assets; ₹2.0 lakh crore "
      "is the SASCI outlay.",
  current=BUD,
  facts=[fact("As recommended by the Commission, I have provided ₹1.4 lakh crore to the States for the FY 2026-27 as "
              "Finance Commission Grants. These include Rural and Urban Local Body and Disaster Management Grants",
              BUDGET)])
Q("008", T, UB, "Basic",
  "For long-term energy security, what outlay did the Union Budget 2026-27 announce over the next five years for Carbon "
  "Capture, Utilization and Storage (CCUS) technologies?",
  ["₹20,000 crore", "₹10,000 crore", "₹40,000 crore", "₹5,000 crore"],
  concept="Budget 2026-27: energy security",
  explanation="Under 'Ensuring long term energy security and stability', the Budget announced ₹20,000 crore over five "
              "years for CCUS technologies.",
  steps=["CCUS: ₹20,000 crore over 5 years"],
  why="₹10,000 crore is the Biopharma SHAKTI / container manufacturing figure; ₹40,000 crore is the ECMS outlay; "
      "₹5,000 crore is per City Economic Region.",
  current=BUD,
  facts=[fact("An outlay of ₹20,000 crore over the next 5 years, announced for Carbon Capture Utilization and Storage "
              "(CCUS) technologies", BUDGET)])
Q("008", T, ESH, "Basic",
  "According to the Economic Survey 2025-26, what was India's average headline CPI inflation between April and "
  "December 2025?",
  ["1.7 per cent", "3.4 per cent", "4.0 per cent", "5.2 per cent"],
  concept="Inflation in the Economic Survey 2025-26",
  explanation="The Survey reported average headline CPI inflation of just 1.7% for April–December 2025, which summaries "
              "described as the lowest for that period since the CPI series began, helped by falling food prices.",
  steps=["Apr–Dec 2025 average CPI = 1.7%"],
  why="The other figures are not the Survey's number for that period.",
  current=ESD,
  facts=[fact("average headline Consumer Price Index (CPI) inflation between April and December 2025 was just 1.7 "
              "percent", ES_PRINT)])

Q("008", T, UB, "Intermediate",
  "What did the Union Budget 2026-27 propose about Minimum Alternate Tax (MAT)?",
  ["MAT to become a final tax at 14% (down from 15%), with no further MAT credit accumulating from 1 April 2026",
   "MAT to be abolished for all companies from 1 April 2026",
   "MAT rate to be raised to 18.5% to curb tax avoidance",
   "MAT credit to be allowed in full against tax under the new regime"],
  concept="MAT reform",
  explanation="MAT is to be made a final tax at 14% (against the current 15%), with no further credit accumulation from "
              "1 April 2026. Brought-forward MAT credit up to 31 March 2026 can be set off only by companies in the new "
              "regime, up to one-fourth of the tax liability.",
  steps=["MAT = final tax @14%", "No credit accrual from 1-4-2026", "Old credit: new regime only, ≤ 1/4 of liability"],
  why="MAT is not abolished (only non-residents on presumptive tax are exempted); the rate is cut, not raised; credit "
      "set-off is limited to one-fourth.",
  current=BUD,
  facts=[fact("MAT is proposed to be made final tax. There will be no further credit accumulation from 1st April 2026. "
              "The rate of final tax to be reduced to 14 percent from the current MAT rate of 15 percent", BUDGET),
         fact("Set-off using available MAT credit to be allowed to an extent of 1/4th of the tax liability in the new "
              "regime", BUDGET)])
Q("008", T, UB, "Intermediate",
  "To rationalise penalty and prosecution, the Union Budget 2026-27 proposed to reduce the pre-payment required "
  "(while a tax dispute is pending) from 20 per cent to:",
  ["10 per cent, calculated only on the core tax demand", "15 per cent of the total demand including interest",
   "5 per cent of the core tax demand", "Nil for all taxpayers"],
  concept="Direct tax dispute reforms",
  explanation="The quantum of pre-payment is to be reduced from 20% to 10%, calculated only on the core tax demand. "
              "Assessment and penalty proceedings are also to be integrated through a common order.",
  steps=["Pre-payment: 20% → 10% of core tax demand"],
  why="The other rates and bases are not the Budget proposal.",
  current=BUD,
  facts=[fact("The quantum of pre-payment will be reduced from 20 percent to 10 percent, calculated only on core tax "
              "demand", BUDGET)])
Q("008", T, ESH, "Intermediate",
  "The Economic Survey 2025-26 credited low inflation partly to food and fuel prices. Roughly what share of the CPI "
  "basket do food and fuel together account for, as cited in reports on the Survey?",
  ["52.7 per cent", "29.2 per cent", "45.9 per cent", "68.0 per cent"],
  concept="CPI basket and the Economic Survey",
  explanation="Reports on the Survey noted that food and fuel together account for 52.7% of the CPI basket, so the sharp "
              "fall in food prices pulled average headline CPI inflation down to 1.7% in April–December 2025.",
  steps=["Food + fuel ≈ 52.7% of CPI basket"],
  why="The other shares are not the figure cited.",
  current=ESD,
  facts=[fact("together account for 52.7 percent of the CPI basket (food and fuel)", ES_PRINT)])

gross, net = 17.2, 11.7
assert round(gross - net, 1) == 5.5 and round(100 * net / gross) == 68
Q("008", T, FT, "Advanced",
  "The Union Budget 2026-27 estimates gross market borrowings of ₹17.2 lakh crore and net market borrowings from dated "
  "securities of ₹11.7 lakh crore. Which statement is correct?",
  ["About ₹5.5 lakh crore of gross borrowing goes to repay maturing debt, so net borrowing is about 68% of gross",
   "About ₹5.5 lakh crore is borrowed from small savings, so market borrowing is 68% of the fiscal deficit",
   "Net borrowing exceeds gross borrowing by ₹5.5 lakh crore because of buybacks",
   "About ₹28.9 lakh crore is raised in all from the market, the sum of the two figures"],
  concept="Gross versus net market borrowing",
  explanation="Gross market borrowing is the total raised through dated securities; net borrowing deducts repayments "
              "of maturing securities (and similar adjustments). 17.2 − 11.7 = ₹5.5 lakh crore goes to repayments; "
              "11.7 ÷ 17.2 ≈ 68%. Only net borrowing finances the fiscal deficit; the balance comes from small savings "
              "and other sources.",
  steps=["Gross − net = 17.2 − 11.7 = 5.5", "Net/gross = 11.7/17.2 ≈ 68%"],
  why="Small savings finance the fiscal deficit beyond net borrowing, not the gross–net gap; net cannot exceed gross; "
      "the two figures overlap and cannot be added.",
  computed=True, current=BUD,
  facts=[fact("The net market borrowings from dated securities are estimated at ₹11.7 lakh crore. The balance financing "
              "is expected to come from small savings and other sources. The gross market borrowings are estimated at "
              "₹17.2 lakh crore", BUDGET)])

fut, prem = 50_00_000, 2_00_000
old_stt = fut * 0.02 / 100 + prem * 0.1 / 100
new_stt = fut * 0.05 / 100 + prem * 0.15 / 100
assert round(old_stt) == 1200 and round(new_stt) == 2800 and round(new_stt - old_stt) == 1600
Q("008", T, UB, "Advanced",
  "A trader sells futures worth ₹50 lakh and sells options with a total premium of ₹2 lakh. Using the STT rates on "
  "futures and on options premium before and after the Union Budget 2026-27, by how much does his STT on these trades "
  "rise?",
  ["₹1,600 (from ₹1,200 to ₹2,800)", "₹1,500 (from ₹1,000 to ₹2,500)", "₹1,700 (from ₹1,250 to ₹2,950)",
   "₹3,000 (from ₹2,000 to ₹5,000)"],
  concept="Computing STT after the Budget",
  explanation="Futures: 0.02% of ₹50 lakh = ₹1,000 before, 0.05% = ₹2,500 after. Options premium: 0.1% of ₹2 lakh = "
              "₹200 before, 0.15% = ₹300 after. Total ₹1,200 → ₹2,800, a rise of ₹1,600.",
  steps=["Futures: 1,000 → 2,500", "Options premium: 200 → 300", "Total: 1,200 → 2,800 (+1,600)"],
  why="₹1,500 ignores the options leg; ₹1,700 applies 0.125% as the old premium rate; ₹3,000 uses wrong bases.",
  computed=True, current=BUD,
  facts=[fact("STT on Futures to be raised to 0.05 percent from present 0.02 percent. STT on options premium and exercise "
              "of options to be raised to 0.15 percent from the present rate of 0.1 percent and 0.125 percent "
              "respectively", BUDGET)])
assert round(fut * 0.02 / 100 + prem * 0.125 / 100) == 1250

Q("009", T, UB, "Basic",
  "The Coastal Cargo Promotion Scheme announced in the Union Budget 2026-27 aims to raise the share of inland "
  "waterways and coastal shipping in cargo movement from 6% to what level by 2047?",
  ["12%", "10%", "18%", "25%"],
  concept="Budget 2026-27: logistics",
  explanation="The scheme incentivises a modal shift from rail and road to raise the share of inland waterways and "
              "coastal shipping from 6% to 12% by 2047. The Budget also proposed 20 new National Waterways over five "
              "years, starting with NW-5 in Odisha.",
  steps=["6% → 12% by 2047"],
  why="The other targets are not in the Budget.",
  current=BUD,
  facts=[fact("A Coastal Cargo Promotion Scheme to be launched for incentivising a modal shift from rail and road, to "
              "increase the share of inland waterways and coastal shipping from 6% to 12 % by 2047", BUDGET)])
Q("009", T, UB, "Basic",
  "Under the Union Budget 2026-27 proposals, up to when can a taxpayer revise an income tax return?",
  ["Up to 31 March, on payment of a nominal fee, instead of 31 December", "Up to 31 December, as before, without any "
   "fee", "Up to 30 September of the next year, with a 10% fee", "Up to 31 July of the next year"],
  concept="Return revision timeline",
  explanation="The time available for revising returns is proposed to be extended from 31 December to up to 31 March, "
              "with payment of a nominal fee. The timeline for filing returns is also to be staggered.",
  steps=["Revision deadline: 31 Dec → 31 Mar (nominal fee)"],
  why="31 December was the earlier deadline; the other dates are not in the Budget.",
  current=BUD,
  facts=[fact("Extend time available for revising returns from 31st December to upto 31st March with payment of nominal "
              "fees", BUDGET)])
Q("009", T, UB, "Intermediate",
  "To reduce litigation, the Union Budget 2026-27 proposed that taxpayers may update their returns even after "
  "reassessment proceedings have started. On what condition?",
  ["Paying tax at an additional 10 percentage points over the rate applicable for that year",
   "Paying a flat penalty of ₹1 lakh", "Only if the reassessment notice is withdrawn first",
   "Paying 100% of the tax as additional income tax"],
  concept="Updated returns during reassessment",
  explanation="Taxpayers will be allowed to update returns even after reassessment has been initiated, at an "
              "additional 10 percent tax rate over and above the rate applicable for the relevant year. Paying 100% of "
              "the tax as additional income tax is the condition for immunity in cases of misreporting.",
  steps=["Updated return after reassessment → applicable rate + 10%"],
  why="There is no flat ₹1 lakh penalty or need to withdraw the notice; 100% additional tax is the misreporting "
      "immunity condition.",
  current=BUD,
  facts=[fact("Taxpayers will be allowed to update their returns even after reassessment proceedings have been "
              "initiated, at an additional 10 percent tax rate over and above the rate applicable for the relevant "
              "year", BUDGET)])
Q("009", T, UB, "Intermediate",
  "What did the Union Budget 2026-27 propose about Income Computation and Disclosure Standards (ICDS)?",
  ["A joint committee of MCA and CBDT to fold ICDS requirements into Ind AS, with separate ICDS-based accounting done "
   "away with from tax year 2027-28",
   "Making ICDS mandatory for all companies from 1 April 2026",
   "Replacing Ind AS with ICDS for listed companies",
   "Extending ICDS to individuals with business income above ₹50 lakh"],
  concept="Tax administration in Budget 2026-27",
  explanation="The Budget proposed a Joint Committee of the Ministry of Corporate Affairs and CBDT to incorporate ICDS "
              "requirements into Ind AS itself, so that separate ICDS-based accounting ends from tax year 2027-28.",
  steps=["MCA–CBDT committee → ICDS inside Ind AS → no separate ICDS accounting from TY 2027-28"],
  why="The Budget removes, rather than extends, separate ICDS accounting.",
  current=BUD,
  facts=[fact("A Joint Committee of Ministry of Corporate Affairs and Central Board of Direct Taxes to be constituted for "
              "incorporating the requirements of Income Computation and Disclosure Standards (ICDS) in the Indian "
              "Accounting Standards (IndAS) itself. Separate accounting requirement based on ICDS will be done away with "
              "from the tax year 2027-28", BUDGET)])
assert 4.2 <= 11.21 / 2.63 < 4.3
Q("009", T, UB, "Intermediate",
  "The Electronics Components Manufacturing Scheme (ECMS) was launched in April 2025. What did the Union Budget "
  "2026-27 do to its outlay?",
  ["Raised it to ₹40,000 crore from ₹22,919 crore", "Raised it to ₹22,919 crore from ₹10,000 crore",
   "Merged it into India Semiconductor Mission 2.0 with no separate outlay", "Cut it to ₹20,000 crore"],
  concept="Manufacturing schemes in Budget 2026-27",
  explanation="ECMS, launched in April 2025 with ₹22,919 crore, had its outlay raised to ₹40,000 crore to capitalise on "
              "momentum. ISM 2.0 was announced separately.",
  steps=["ECMS: ₹22,919 crore → ₹40,000 crore"],
  why="The other figures and the merger are not in the Budget.",
  current=BUD,
  facts=[fact("The Electronics Components Manufacturing Scheme, launched in April 2025 has an outlay of ₹22,919 crore. The "
              "Union Budget 2026-27 proposes to increase the outlay to ₹40,000 crore", BUDGET)])

liab, credit = 80, 30
setoff = min(credit, liab / 4)
assert setoff == 20 and liab - setoff == 60 and credit - setoff == 10
Q("009", T, UB, "Advanced",
  "A company that has moved to the new tax regime has a tax liability of ₹80 lakh for tax year 2026-27 and "
  "brought-forward MAT credit of ₹30 lakh accumulated till 31 March 2026. Under the Union Budget 2026-27 proposal, how "
  "much credit can it set off this year?",
  ["₹20 lakh, paying ₹60 lakh and carrying ₹10 lakh of credit forward", "₹30 lakh, paying ₹50 lakh",
   "Nil, because MAT credit lapses from 1 April 2026", "₹26.7 lakh, one-third of the liability"],
  concept="MAT credit set-off",
  explanation="Brought-forward MAT credit can be used only by companies in the new regime, and only up to one-fourth "
              "of the tax liability: ¼ × 80 = ₹20 lakh. The company pays 80 − 20 = ₹60 lakh, and ₹10 lakh of credit "
              "remains for later years.",
  steps=["Cap = 80/4 = 20", "Set-off = min(30, 20) = 20", "Payable 60; credit left 10"],
  why="Full set-off ignores the one-fourth cap; old credit does not lapse; the cap is one-fourth, not one-third.",
  computed=True, current=BUD,
  facts=[fact("Set-off of brought forward MAT credit to be allowed to companies only in the new regime. Set-off using "
              "available MAT credit to be allowed to an extent of 1/4th of the tax liability in the new regime ... The "
              "brought forward MAT credit of taxpayers accumulated till 31st March 2026, will continue to be available "
              "to them for set-off as above", BUDGET)])

dev_be, dev_re, gtr = 15.26, 13.93, 44.04
assert round(dev_be - dev_re, 2) == 1.33 and round(100 * (dev_be - dev_re) / dev_re, 1) == 9.5
assert round(100 * dev_be / gtr, 1) == 34.7
Q("009", T, FT, "Advanced",
  "In BE 2026-27, tax devolution to the States is ₹15.26 lakh crore (₹13.93 lakh crore in RE 2025-26) and the Centre's "
  "gross tax revenue (GTR) is ₹44.04 lakh crore, while the States' share has been retained at 41% of the divisible "
  "pool. Which statement is correct?",
  ["Devolution grows about 9.5% and is only about 35% of GTR, because cesses, surcharges and collection costs are "
   "outside the divisible pool",
   "Devolution grows about 9.5% and is exactly 41% of GTR",
   "Devolution grows about 13.3% and is about 41% of GTR",
   "Devolution falls, since the 41% share applies only to direct taxes"],
  concept="Divisible pool versus gross tax revenue",
  explanation="Growth: (15.26 − 13.93) ÷ 13.93 ≈ 9.5% (₹1.33 lakh crore more). Share of GTR: 15.26 ÷ 44.04 ≈ 34.7%. "
              "The 41% applies to the divisible pool, which excludes cesses and surcharges (and cost of collection), so "
              "devolution is a smaller share of gross tax revenue.",
  steps=["(15.26 − 13.93)/13.93 ≈ 9.5%", "15.26/44.04 ≈ 34.7%", "41% is of the divisible pool, not GTR"],
  why="41% is not applied to GTR; 13.3% misreads the ₹1.33 lakh crore increase; devolution rises and covers all "
      "shareable taxes.",
  computed=True, current=BUD,
  facts=[fact("In BE 2026-27, tax devolution to the States is estimated at ₹15.26 lakh crore compared to ₹13.93 lakh "
              "crore in RE 2025-26 ... ₹1.33 lakh crore more than tax devolution of RE 2025-26", BUDGET),
         fact("In BE 2026-27, Gross Tax Revenue (GTR) is estimated at ₹44.04 lakh crore ... SFC has recommended for "
              "retaining the share of devolution to the States at 41 per cent of divisible pool", BUDGET)])

Q("010", T, UB, "Basic",
  "Under the Union Budget 2026-27, what tax benefit is offered to a foreign company that provides cloud services to "
  "customers globally using data centre services from India?",
  ["A tax holiday till 2047", "A concessional tax rate of 15% till 2035", "Exemption from GST on exports",
   "A 100% deduction for 10 years"],
  concept="Attracting data centre investment",
  explanation="Any foreign company providing cloud services to customers globally using data centre services from "
              "India is to get a tax holiday till 2047. If the Indian data centre provider is a related entity, a safe "
              "harbour of 15% on cost applies.",
  steps=["Foreign cloud provider using Indian data centres → tax holiday till 2047"],
  why="15% is the safe harbour on cost for a related data-centre entity, not a tax rate; the other benefits are not in "
      "the Budget.",
  current=BUD,
  facts=[fact("Any foreign company that provides cloud services to customers globally by using data centre services from "
              "India to be provided Tax holiday till 2047", BUDGET)])
Q("010", T, UB, "Basic",
  "To help small businesses, artisans and start-ups export through e-commerce, the Union Budget 2026-27 proposed to:",
  ["Remove the ₹10 lakh per consignment value cap on courier exports", "Raise the courier export cap from ₹5 lakh to "
   "₹10 lakh", "Exempt courier exports from GST", "Set up a ₹10,000 crore export credit fund for courier exports"],
  concept="Budget 2026-27: export facilitation",
  explanation="The Budget proposed complete removal of the current value cap of ₹10 lakh per consignment on courier "
              "exports.",
  steps=["Courier exports: ₹10 lakh cap removed"],
  why="The cap was removed, not raised; GST exemption and an export credit fund were not proposed.",
  current=BUD,
  facts=[fact("Complete removal of the current value cap of ₹10 lakh per consignment on courier exports-supports "
              "aspirations of India's small businesses, artisans and start-ups to access global markets through "
              "e-commerce", BUDGET)])
Q("010", T, UB, "Intermediate",
  "What relief did the Union Budget 2026-27 propose for non-disclosure of foreign assets other than immovable property?",
  ["Immunity from prosecution where the aggregate value is less than ₹20 lakh, with retrospective effect from "
   "1 October 2024", "Immunity from tax where the value is less than ₹50 lakh, from 1 April 2026",
   "Waiver of all penalties for assets disclosed by 31 March 2027", "Immunity from prosecution for all such assets, "
   "whatever their value"],
  concept="Decriminalisation under the Income-tax Act",
  explanation="Non-disclosure of non-immovable foreign assets with aggregate value below ₹20 lakh is to get immunity "
              "from prosecution, retrospectively from 1.10.2024. Separately, a one-time six-month foreign asset "
              "disclosure scheme was proposed for small taxpayers.",
  steps=["Non-immovable foreign assets < ₹20 lakh → no prosecution (from 1-10-2024)"],
  why="The relief is from prosecution, not tax; the threshold is ₹20 lakh; it is not unlimited.",
  current=BUD,
  facts=[fact("Non-disclosure of non-immovable foreign assets with aggregate value less than 20 lakh rupees to be "
              "provided with immunity from prosecution with retrospective effect from 1.10.2024", BUDGET)])
Q("010", T, UB, "Intermediate",
  "The Union Budget 2026-27 offered non-residents a safe harbour for component warehousing in a bonded warehouse. On "
  "what basis, and with what resulting tax?",
  ["Profit margin of 2% of invoice value, giving tax of about 0.7%", "Profit margin of 15% on cost, giving tax of "
   "about 5%", "Profit margin of 15.5%, giving tax of about 4%", "Profit margin of 5% of invoice value, giving tax of "
   "about 2%"],
  concept="Safe harbour rules in Budget 2026-27",
  explanation="Non-residents get a safe harbour for component warehousing in a bonded warehouse at a profit margin of "
              "2% of invoice value; the resulting tax of about 0.7% is far lower than in competing jurisdictions. 15% on "
              "cost is the safe harbour for related-entity data centre services; 15.5% is the common margin for IT "
              "services.",
  steps=["Component warehousing: 2% of invoice → tax ≈ 0.7%"],
  why="15% on cost and 15.5% belong to other safe harbours; 5% is not the margin.",
  current=BUD,
  facts=[fact("A safe harbour to non-residents for component warehousing in a bonded warehouse at a profit margin of 2 "
              "percent of the invoice value. The resultant tax of about 0.7 percent will be much lower than in "
              "competing jurisdictions", BUDGET)])
Q("010", T, UB, "Intermediate",
  "Which customs measures for trusted traders did the Union Budget 2026-27 propose?",
  ["Duty deferral for Tier 2 and Tier 3 Authorised Economic Operators raised from 15 to 30 days, and validity of "
   "customs advance rulings extended from 3 to 5 years",
   "Duty deferral for all importers raised from 30 to 60 days, and advance rulings made valid for 10 years",
   "Abolition of the AEO programme and its replacement by a risk-based audit",
   "Duty deferral for Tier 1 AEOs raised from 7 to 15 days"],
  concept="Trust-based customs",
  explanation="The duty deferral period for Tier 2 and Tier 3 AEOs is to go up from 15 to 30 days (and be extended to "
              "eligible manufacturer-importers), and the validity of advance rulings binding on Customs from 3 to 5 "
              "years.",
  steps=["AEO Tier 2/3 deferral: 15 → 30 days", "Advance ruling validity: 3 → 5 years"],
  why="The other periods and the abolition of AEO are not in the Budget.",
  current=BUD,
  facts=[fact("Duty deferral period for Tier 2 and Tier 3 Authorised Economic Operators, known as AEOs, to be enhanced "
              "from 15 days to 30 days ... Validity period of advance ruling, binding on Customs, to be extended from the "
              "present 3 years to 5 years", BUDGET)])
Q("010", T, ESH, "Intermediate",
  "According to the Economic Survey 2025-26, what were India's total exports of goods and services in FY25?",
  ["A record $825.3 billion, up 6.1% year-on-year", "$437.4 billion, up 2.4% year-on-year",
   "$1 trillion, up 10% year-on-year", "$778.2 billion, flat year-on-year"],
  concept="External sector in the Economic Survey",
  explanation="Total exports (merchandise and services) reached a record $825.3 billion in FY25, growing 6.1% "
              "year-on-year; the Budget's Macro-economic Framework Statement cites the same total.",
  steps=["FY25 total exports = $825.3 bn (+6.1%)"],
  why="The other figures are not the Survey's total-exports number.",
  current=ESD,
  facts=[fact("India's total exports reached a record $825.3 billion in FY25, growing 6.1 percent year-on-year",
              ES_PRINT),
         fact("India's total exports (merchandise and services) reached USD 825.3 billion in FY25", BUDGET)])
Q("010", T, UB, "Intermediate",
  "What change did the Union Budget 2026-27 propose to the TCS rate on the sale of overseas tour programme packages?",
  ["A single rate of 2%, replacing the 5% and 20% rates, without any threshold", "A cut from 20% to 10% for all "
   "packages", "Abolition of TCS on tour packages up to ₹7 lakh", "An increase to 20% for all packages"],
  concept="TCS rationalisation",
  explanation="TCS on overseas tour programme packages is to be reduced from the current 5% and 20% to 2%, without any "
              "stipulation of amount. TCS on LRS remittances for education and medical purposes was separately cut from "
              "5% to 2%.",
  steps=["Tour packages: 5%/20% → 2% flat"],
  why="The 10% cut, a ₹7 lakh exemption and an increase are not the Budget proposal.",
  current=BUD,
  facts=[fact("The Overseas tour program package is reduced from the current 5 percent and 20 percent to 2 percent "
              "without any stipulation of amount", BUDGET)])

ec26, ec27 = 15.48, 17.15
g = 100 * (ec27 - ec26) / ec26
assert round(ec27 - ec26, 2) == 1.67 and round(g, 1) == 10.8
Q("010", T, FT, "Advanced",
  "The Economic Survey 2025-26 put the Centre's effective capital expenditure for FY26 at ₹15.48 lakh crore, and the "
  "Budget estimates it at ₹17.15 lakh crore (4.4% of GDP) for FY27, made up of capital expenditure of ₹12.22 lakh crore "
  "and grants for creation of capital assets of ₹4.93 lakh crore. Which statement is correct?",
  ["Effective capex is budgeted to grow by about 10.8%, and grants for capital assets make up about 29% of it",
   "Effective capex is budgeted to grow by about 1.67%, and grants make up about 40% of it",
   "Effective capex is budgeted to fall, because grants are revenue expenditure",
   "Effective capex equals capital expenditure minus grants for capital assets"],
  concept="Effective capital expenditure",
  explanation="Effective capex = capital expenditure + grants-in-aid for creation of capital assets = 12.22 + 4.93 = "
              "₹17.15 lakh crore. Growth over FY26: (17.15 − 15.48) ÷ 15.48 ≈ 10.8%. Share of grants: 4.93 ÷ 17.15 "
              "≈ 28.7%.",
  steps=["17.15 − 15.48 = 1.67 → 1.67/15.48 ≈ 10.8%", "4.93/17.15 ≈ 28.7%"],
  why="1.67 is the increase in lakh crore, not per cent; effective capex rises; grants are added, not subtracted.",
  computed=True, current=BUD,
  facts=[fact("Effective capital expenditure in FY26 stands at Rs 15.48 lakh crore", ES_PRINT),
         fact("The effective capital expenditure of Union Government in FY 2026-27 estimated at ₹17.15 lakh crore, that is "
              "4.4% of GDP; includes GoI's capital expenditure (₹12.22 lakh crore) and grants-in-aid to States (₹4.93 "
              "lakh crore) for creation of capital assets", BUDGET)])
assert round(12.22 + 4.93, 2) == 17.15 and round(100 * 4.93 / 17.15) == 29

add_inc, rate = 10, 30
tax_upd = add_inc * (rate + 10) / 100
assert tax_upd == 4
Q("010", T, UB, "Advanced",
  "Reassessment has been started against a taxpayer for a year in which his income was taxable at 30%. He now wants to "
  "update his return to show ₹10 lakh of omitted income. Under the Union Budget 2026-27 proposal (ignoring cess, "
  "surcharge and interest), what tax does he pay on it?",
  ["₹4 lakh, i.e. 30% plus an additional 10 percentage points", "₹3 lakh, at the applicable 30% only",
   "₹6 lakh, i.e. 30% plus 100% of that tax as additional tax", "₹3.3 lakh, i.e. 30% plus 10% of the tax"],
  concept="Updated return after reassessment",
  explanation="Returns can be updated even after reassessment starts, at an additional 10 percent tax rate over and "
              "above the applicable rate: 30% + 10% = 40% of ₹10 lakh = ₹4 lakh.",
  steps=["Rate = 30 + 10 = 40%", "Tax = 0.40 × 10 lakh = ₹4 lakh"],
  why="₹3 lakh omits the additional rate; ₹6 lakh applies the misreporting-immunity condition (100% additional tax); "
      "₹3.3 lakh reads the 10% as a surcharge on tax instead of extra rate points.",
  computed=True, current=BUD,
  facts=[fact("Taxpayers allowed to update their returns even after reassessment proceedings have been initiated to "
              "reduce litigations, at an additional 10 percent tax rate over and above the rate applicable for the "
              "relevant year", BUDGET)])

tax_mis = 6
assert tax_mis + 1.0 * tax_mis == 12
Q("010", T, UB, "Advanced",
  "Consider the following statements on the penalty and prosecution proposals of the Union Budget 2026-27:\n"
  "I. Immunity from penalty and prosecution, available for under-reporting, is extended to misreporting of income, on "
  "payment of 100% of the tax amount as additional income tax over the tax and interest due.\n"
  "II. Assessment and penalty proceedings are to be integrated through a common order.\n"
  "III. Non-production of books of account is made a cognizable offence.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Penalty and prosecution reforms",
  explanation="I is correct: misreporting cases can get immunity by paying 100% of the tax as additional income tax "
              "(so a ₹6 lakh tax on misreported income means ₹12 lakh plus interest). II is correct. III is wrong: "
              "non-production of books of account and documents is to be decriminalised.",
  steps=["I ✓", "II ✓", "III ✗ (decriminalised)"],
  why="Any option with III is wrong.",
  current=BUD,
  facts=[fact("The Budget proposes to extend the provisions for immunity from penalty and prosecution in the cases of "
              "under reporting, to misreporting as well. Taxpayer will need to pay 100 percent of the tax amount as an "
              "additional income tax over and above the tax and interest due", BUDGET),
         fact("Assessment & penalty proceedings will be integrated by way of a common order for both ... Non-production "
              "of books of account and documents ... will be decriminalised", BUDGET)])

# ============================================================================================ Government Financial Schemes
T = "Government Financial Schemes"
PM4, CG = "PMMY, PMSBY, PMJJBY, APY", "Credit guarantee schemes"
D_APY = "https://financialservices.gov.in/atal-pension-yojana-apy"
D_PMMY = "https://financialservices.gov.in/pradhan-mantri-mudra-yojana-pmmy"
D_PMJJBY = "https://financialservices.gov.in/pmjjby"
D_PMSBY = "https://financialservices.gov.in/pmsby"
CGS1 = ("https://www.cgtmse.in/Default/ViewFile/?id=1743176302611_CGTMSE%20-%20Scheme%20Document%20CGS%20I_updated"
        "%20as%20on%20Apr%201%202025.pdf&path=Page")    # CGS-I scheme document, updated as on 1 April 2025
SVANIDHI = "https://www.tribuneindia.com/news/business/cabinet-approves-restructuring-extension-of-pm-svanidhi-scheme-till-2030"
SVA = ca("2025-08-27")       # Cabinet approval of restructured PM SVANidhi

Q("008", T, PM4, "Basic",
  "Of the PMJJBY annual premium of ₹436 collected from a new subscriber, how much is the insurance premium payable to "
  "the insurer?",
  ["₹395", "₹436", "₹342", "₹330"],
  concept="Appropriation of PMJJBY premium",
  explanation="For the full annual premium of ₹436: ₹395 goes to LIC/the insurer as insurance premium, ₹30 is commission "
              "to BCs/agents (new enrolments only) and ₹11 is administrative expenses to the participating bank.",
  steps=["436 = 395 (insurer) + 30 (BC/agent) + 11 (bank)"],
  why="₹436 is the gross premium; ₹342 is the pro-rata premium for September–November enrolment; ₹330 is not a figure "
      "in the scheme.",
  facts=[fact("Appropriation of Premium where Full Annual Premium of Rs.436/- collected: (1) Insurance Premium to LIC/ "
              "Insurance Company Rs.395/- (2) Commission payable to Business Correspondents, agents, etc. (For new "
              "enrolments only) Rs.30/- (3) Administrative Expenses payable to participating Banks Rs.11/-", D_PMJJBY)])
assert 395 + 30 + 11 == 436
Q("008", T, PM4, "Basic",
  "Under the PM SVANidhi scheme for street vendors, as restructured by the Union Cabinet in August 2025, what are the "
  "loan amounts of the three tranches?",
  ["₹15,000, ₹25,000 and ₹50,000", "₹10,000, ₹20,000 and ₹50,000", "₹15,000, ₹30,000 and ₹75,000",
   "₹25,000, ₹50,000 and ₹1,00,000"],
  concept="PM SVANidhi loan tranches",
  explanation="The restructuring raised the first tranche to ₹15,000 (from ₹10,000) and the second to ₹25,000 (from "
              "₹20,000); the third tranche stays at ₹50,000.",
  steps=["1st: 10k → 15k", "2nd: 20k → 25k", "3rd: 50k (unchanged)"],
  why="₹10,000/₹20,000/₹50,000 were the earlier amounts; the other sets are not the scheme's.",
  current=SVA,
  facts=[fact("Loan tranches: first raised to Rs. 15,000 from Rs. 10,000; second raised to Rs. 25,000 from Rs. 20,000; "
              "third unchanged at Rs. 50,000", SVANIDHI)])
Q("008", T, CG, "Basic",
  "Under CGTMSE's Credit Guarantee Scheme (CGS-I), what is the maximum extent of guarantee cover on a credit facility "
  "of up to ₹5 lakh to a micro enterprise?",
  ["85%", "75%", "90%", "100%"],
  concept="CGTMSE coverage for micro enterprises",
  explanation="For guarantees approved on or after 1 April 2025, micro enterprises get 85% cover on credit facilities "
              "up to ₹5 lakh and 75% above ₹5 lakh. Women entrepreneurs get 90%.",
  steps=["Micro, ≤ ₹5 lakh → 85%"],
  why="75% applies to micro loans above ₹5 lakh and to 'all other' borrowers; 90% is for women entrepreneurs; 100% "
      "is not offered.",
  facts=[fact("The Extent of Guarantee Coverage: Micro Enterprises - Upto ₹5 lakh: 85%; Above ₹5 lakh: 75%", CGS1)])
Q("008", T, CG, "Intermediate",
  "Under CGTMSE's CGS-I, what is the maximum credit facility per borrower that each type of lending institution can "
  "get guaranteed?",
  ["₹10 crore for public sector, private sector and foreign banks; ₹200 lakh for SFBs, RRBs and co-operative "
   "banks; ₹50 lakh for microfinance institutions",
   "₹10 crore for all lending institutions alike",
   "₹5 crore for banks; ₹1 crore for RRBs; ₹10 lakh for MFIs",
   "₹200 lakh for public sector banks; ₹10 crore for private and foreign banks"],
  concept="Ceilings by type of Member Lending Institution",
  explanation="CGS-I covers credit facilities not exceeding ₹10 crore from public sector, private sector and foreign "
              "banks and select FIs; ₹200 lakh from SFBs, RRBs, State Financial Institutions and urban/state/district "
              "co-operative banks; and ₹50 lakh from microfinance institutions.",
  steps=["SCBs/select FIs: ₹10 crore", "SFBs, RRBs, SFCs, co-op banks: ₹2 crore", "MFIs: ₹50 lakh"],
  why="The ceiling differs by type of lender; the other figures are not in the scheme.",
  facts=[fact("credit facility (i) not exceeding ₹10 crore (Public Sector Banks, Private Sector Banks, Foreign Banks, "
              "select Financial Institutions); (ii) not exceeding ₹200 lakh (Small Finance Banks (SFBs), Regional Rural "
              "Banks, State Financial Institutions and Scheduled Urban Co-operative Banks ...); (iii) not exceeding "
              "₹50 lakh (Microfinance Institutions)", CGS1)])
Q("008", T, PM4, "Intermediate",
  "What did the Union Cabinet's restructuring of PM SVANidhi in August 2025 provide for street vendors who repay the "
  "second loan, and up to when was the lending period extended?",
  ["A UPI-linked RuPay credit card for personal and business needs; lending extended to 31 March 2030",
   "A third loan of ₹1 lakh without guarantee; lending extended to 31 December 2027",
   "An interest-free overdraft of ₹10,000; lending extended to 31 March 2028",
   "A free accident insurance cover of ₹2 lakh; lending extended to 31 March 2035"],
  concept="Restructured PM SVANidhi",
  explanation="Vendors who repay the second loan get a UPI-linked RuPay credit card for personal and business needs. "
              "The lending period was extended from 31 December 2024 to 31 March 2030, with an outlay of ₹7,332 crore.",
  steps=["Repay 2nd loan → UPI-linked RuPay credit card", "Lending till 31-3-2030"],
  why="The other benefits and dates are not part of the restructured scheme.",
  current=SVA,
  facts=[fact("UPI-linked RuPay Credit Card: introduced for vendors who successfully repay their second loan, for "
              "personal and business needs; lending period extended from December 31, 2024 to March 31, 2030",
              SVANIDHI)])
Q("008", T, CG, "Intermediate",
  "Under CGTMSE's CGS-I, a lending institution can invoke the guarantee only after a lock-in period. What is it?",
  ["18 months (9 months for guarantees up to ₹10 lakh with tenure up to 36 months), from the later of the last "
   "disbursement and the guarantee start date",
   "12 months from the date of sanction, for all guarantees", "36 months from the guarantee start date",
   "90 days from the date the account turns NPA"],
  concept="Lock-in period for claims",
  explanation="The lock-in period is 18 months, or 9 months for guarantees up to ₹10 lakh with tenure up to 36 months "
              "(from 15 December 2023), counted from the date of last disbursement or the guarantee start date, "
              "whichever is later. Claims must be lodged within 3 years of the NPA date or the end of lock-in, whichever "
              "is later.",
  steps=["Lock-in 18 m (9 m for ≤ ₹10 lakh, tenure ≤ 36 m)", "From later of last disbursement / guarantee start"],
  why="The other periods are not the scheme's lock-in; 90 days relates to NPA classification, not lock-in.",
  facts=[fact("The lock-in period of 18 months for guarantee (or 9 months for guarantee upto ₹10 lakh with tenure upto 36 "
              "months wef December 15, 2023) from either the date of last disbursement of the loan to the borrower or "
              "the guarantee start date in respect of credit facility to the borrower, whichever is later, has lapsed",
              CGS1)])

loan_def, cover = 32, 0.75
guar = loan_def * cover
first, second = 0.75 * guar, 0.25 * guar
assert guar == 24 and first == 18 and second == 6
Q("008", T, CG, "Advanced",
  "A small enterprise (in the 'all other' category, outside any ICDD) defaults on a CGTMSE-covered term loan of ₹45 "
  "lakh, and the amount in default is ₹32 lakh. The bank has initiated recovery and lodges an eligible claim. How will "
  "CGTMSE settle it under CGS-I?",
  ["₹18 lakh within 30 days as first instalment; the balance ₹6 lakh after 3 years from the first settlement or after "
   "OTS, whichever is earlier",
   "₹24 lakh in one instalment within 30 days",
   "₹24 lakh within 30 days and ₹8 lakh after recovery proceedings end",
   "₹18 lakh within 90 days and nothing more"],
  concept="Claim settlement under CGS-I",
  explanation="'All other' borrowers get 75% cover: 0.75 × 32 = ₹24 lakh guaranteed. CGTMSE pays 75% of the guaranteed "
              "amount (₹18 lakh) within 30 days of an eligible claim, and the balance 25% (₹6 lakh) can be claimed after "
              "3 years from the first settlement or OTS, whichever is earlier. Recoveries must first be credited to "
              "CGTMSE before the second claim.",
  steps=["Guaranteed = 75% × 32 = 24", "1st instalment = 75% × 24 = 18 (within 30 days)", "2nd = 6 (after 3 yrs/OTS)"],
  why="₹24 lakh in one go ignores the two-instalment rule; ₹8 lakh covers the uncovered portion; the timing in the "
      "last option is wrong.",
  computed=True,
  facts=[fact("All other category of borrowers 75%", CGS1),
         fact("The Trust shall pay 75 per cent of the guaranteed amount on preferring of eligible claim by the lending "
              "institution, within 30 days ... The claim for balance 25 per cent of the guaranteed amount can be lodged "
              "after the completion of 3 years from the settlement of first claim or OTS (after the receipt of full and "
              "final OTS amount) whichever is earlier", CGS1)])

d8 = 8
two = 0.75 * d8
single = 0.60 * d8
assert two == 6 and abs(single - 4.8) < 1e-9
Q("008", T, CG, "Advanced",
  "A micro enterprise's CGTMSE-covered loan of ₹9 lakh turns NPA with ₹8 lakh in default. As the amount is within the "
  "₹10 lakh threshold, the bank waives legal action and opts for single-instalment settlement. What can it claim, "
  "compared with the normal two-instalment route?",
  ["₹4.8 lakh at once (cover cut from 75% to 60%), against ₹6 lakh in two instalments",
   "₹6 lakh at once, the same as in two instalments",
   "₹6.8 lakh at once (85% cover), against ₹6 lakh in two instalments",
   "₹3.6 lakh at once (45% cover), against ₹4.5 lakh in two instalments"],
  concept="Single-instalment option where legal action is waived",
  explanation="A micro enterprise loan above ₹5 lakh has 75% cover: 0.75 × 8 = ₹6 lakh, paid as ₹4.5 lakh + ₹1.5 lakh "
              "under the two-instalment route. Where legal action is waived (claims lodged from 1 April 2023 up to "
              "₹10 lakh), the bank may take a single instalment with cover reduced by 15 points: 60% × 8 = ₹4.8 lakh.",
  steps=["Cover = 75% (micro, > ₹5 lakh)", "Two instalments: 6.0 lakh", "Single: (75 − 15)% × 8 = 4.8 lakh"],
  why="Single settlement is not at full cover; 85% applies only to loans up to ₹5 lakh; 45% wrongly halves the cover.",
  computed=True,
  facts=[fact("Micro Enterprises - Upto ₹5 lakh: 85%; Above ₹5 lakh: 75%", CGS1),
         fact("In respect of claims lodged on or after April 01, 2023, the threshold for waiver of legal action has been "
              "increased to ₹10,00,000/-", CGS1),
         fact("Option 1: Single instalment of claim settlement with reduced extent of guarantee by 15%. Eg: in respect of "
              "extent of coverage of 75%, reduced coverage would be 60%", CGS1)])

sr, disc = 0.55, 0.30
fee = 30_00_000 * sr * (1 - disc) / 100
assert round(fee) == 11550
Q("008", T, CG, "Advanced",
  "A woman entrepreneur running a ZED-certified unit in an Aspirational District gets a ₹30 lakh CGTMSE-covered loan "
  "from a bank charged the standard fee rate. The standard Annual Guarantee Fee for the above ₹10–50 lakh slab is 0.55% "
  "and each of the three categories (social, geographic, MSE status) earns a 10% concession, subject to a maximum of "
  "30%. What is the first-year fee?",
  ["₹11,550 (0.385%)", "₹16,500 (0.55%)", "₹14,850 (0.495%)", "₹9,900 (0.33%)"],
  concept="AGF concessions",
  explanation="Women entrepreneurs (social), Aspirational Districts (geographic) and ZED-certified MSEs (MSE status) "
              "each get 10% relief, and a borrower in all three gets the maximum 30%. Rate = 0.55% × 0.70 = 0.385%; "
              "fee = 0.385% × ₹30 lakh = ₹11,550 (first year on the guaranteed amount).",
  steps=["Concession = 10 + 10 + 10 = 30% (max)", "Rate = 0.55 × 0.7 = 0.385%", "Fee = 0.00385 × 30,00,000 = 11,550"],
  why="₹16,500 ignores concessions; ₹14,850 gives only one 10% concession; ₹9,900 deducts 40%.",
  computed=True,
  facts=[fact("Slab Above 10-50 lakh: Standard Rate 0.55", CGS1),
         fact("Women/SC/ST/PwD/Agniveers/Transgender Entrepreneur; NER .../ Aspirational District / ICDD; ZED Certified: "
              "Relaxation/Concession in Rate 10% 10% 10% ... shall be eligible for maximum discount of 30%", CGS1)])
assert round(30_00_000 * 0.55 * 0.9 / 100) == 14850 and round(30_00_000 * 0.55 * 0.6 / 100) == 9900

Q("009", T, PM4, "Basic",
  "According to the Department of Financial Services, how many loan accounts had been sanctioned under PMMY from its "
  "launch to 28 February 2025?",
  ["52.07 crore", "7.47 crore", "59.09 crore", "33.19 crore"],
  concept="PMMY progress",
  explanation="DFS reported 52.07 crore accounts sanctioned under PMMY, with ₹33.19 lakh crore sanctioned and ₹32.40 lakh "
              "crore disbursed, as on 28 February 2025.",
  steps=["PMMY accounts (to 28-2-2025) = 52.07 crore"],
  why="7.47 crore is the APY subscriber count on the same date; 59.09 crore is the PMJDY account count of August 2026; "
      "33.19 is the amount sanctioned in lakh crore.",
  facts=[fact("Progress under MUDRA (as on 28.02.2025 since launch of scheme) Total accounts sanctioned : 52.07 crore "
              "Total Sanctioned Amount : Rs. 33.19 lakh crore", D_PMMY),
         fact("Progress under Atal Pension Yojana (as on 28.02.2025) Total subscribers: 7.47 crore", D_APY)])
Q("009", T, PM4, "Basic",
  "What total outlay did the Union Cabinet approve in August 2025 for the restructured PM SVANidhi scheme, and how "
  "many street vendors is it expected to benefit?",
  ["₹7,332 crore; about 1.15 crore vendors, including 50 lakh new beneficiaries",
   "₹5,000 crore; about 50 lakh vendors", "₹13,797 crore; about 68 lakh vendors",
   "₹10,000 crore; about 2 crore vendors"],
  concept="PM SVANidhi outlay",
  explanation="The restructured scheme has an outlay of ₹7,332 crore and aims to benefit about 1.15 crore street "
              "vendors, including 50 lakh new beneficiaries. ₹13,797 crore was the value of loans disbursed to 68 lakh "
              "vendors up to July 2025.",
  steps=["Outlay ₹7,332 crore; 1.15 crore vendors (50 lakh new)"],
  why="₹13,797 crore and 68 lakh are the earlier disbursement figures; the others are not the Cabinet's figures.",
  current=SVA,
  facts=[fact("Financial outlay: Rs. 7,332 crore. Beneficiaries: About 1.15 crore street vendors, including 50 lakh new "
              "beneficiaries", SVANIDHI)])
Q("009", T, CG, "Basic",
  "Under CGTMSE's CGS-I, what concession in the Annual Guarantee Fee is given to women, SC/ST, PwD, Agniveer and "
  "transgender entrepreneurs?",
  ["10%", "25%", "50%", "No concession; only higher cover"],
  concept="AGF concession for target groups",
  explanation="These target groups get a 10% discount on the guarantee fee. Similar 10% concessions are given for "
              "geographic categories (NER, J&K, Ladakh up to ₹50 lakh, Aspirational Districts, ICDDs) and for "
              "ZED-certified MSEs, subject to a maximum total of 30%.",
  steps=["Social category concession = 10% of the fee rate"],
  why="25% and 50% are not the concession; the groups get both higher cover and a fee concession.",
  facts=[fact("Women entrepreneurs/ SC/ST/ Person with disability (PwD) / Transgender Entrepreneur would be given the "
              "discount of 10%. Guarantee to the MSEs promoted by Agniveers shall also carry 10% relaxation in Annual "
              "Guarantee Fee", CGS1)])
Q("009", T, CG, "Basic",
  "What is the maximum extent of CGTMSE guarantee cover for an MSE located in the North East Region or the UTs of "
  "Jammu & Kashmir and Ladakh?",
  ["80%", "75%", "90%", "95%"],
  concept="Regional coverage under CGS-I",
  explanation="MSEs located in the North East Region and the UTs of J&K and Ladakh get 80% cover (75% applies to 'all "
              "other' borrowers). An MSE in an RBI-identified credit deficient district gets 5 points more.",
  steps=["NER / J&K / Ladakh → 80%"],
  why="75% is the 'all other' rate; 90% is for women entrepreneurs; 95% applies only with the ICDD addition to 90%.",
  facts=[fact("MSEs located in North East Region, UT of Jammu & Kashmir & UT of Ladakh 80%", CGS1)])
Q("009", T, CG, "Intermediate",
  "Under CGTMSE's CGS-I, for claims lodged on or after 1 April 2023, up to what outstanding amount may a lending "
  "institution waive the initiation of legal proceedings before invoking the guarantee?",
  ["₹10 lakh", "₹50,000", "₹1 lakh", "₹5 lakh"],
  concept="Waiver of legal action",
  explanation="Initiation of legal proceedings is normally a pre-condition for a claim. The waiver threshold rose from "
              "₹50,000 (2018) to ₹1 lakh (October 2021), ₹5 lakh (January 2023) and ₹10 lakh for claims lodged on or "
              "after 1 April 2023.",
  steps=["2018: ₹50,000 → 2021: ₹1 lakh → Jan 2023: ₹5 lakh → Apr 2023: ₹10 lakh"],
  why="₹50,000, ₹1 lakh and ₹5 lakh were earlier thresholds.",
  facts=[fact("In respect of claims lodged on or after April 01, 2023, the threshold for waiver of legal action has been "
              "increased to ₹10,00,000/-", CGS1)])
Q("009", T, CG, "Intermediate",
  "Which of the following is a condition under CGTMSE's CGS-I?",
  ["Credit facilities above ₹50 lakh must be internally rated by the lending institution and be of investment grade",
   "Every guaranteed loan must be backed by collateral of at least 25%",
   "New lending institutions get a 10% fee discount in their first year",
   "Claims are allowed even if the account is classified as a wilful default"],
  concept="CGS-I conditions",
  explanation="All proposals above ₹50 lakh must be internally rated by the MLI and be investment grade. Loans are "
              "collateral-free (a hybrid model covers only the unsecured part); newly registered MLIs are placed at a "
              "70% risk premium for at least a year; and fraud/wilful-default accounts are ineligible for claims.",
  steps=["> ₹50 lakh → internal rating, investment grade"],
  why="CGS-I covers collateral-free credit; new MLIs pay a 70% risk premium, not a discount; wilful-default accounts "
      "cannot claim.",
  facts=[fact("All proposals for sanction of guarantee approvals for credit facilities above ₹50 lakh will have to be "
              "rated internally by the MLI and should be of investment grade", CGS1),
         fact("MLIs newly registered/which do not have sufficient history of transactions under CGTMSE will be placed at "
              "70% risk premium for a period of atleast 1 year", CGS1),
         fact("The accounts classified by the Lending Institution as Fraud / Willful defaulter / Non-Co-operative "
              "borrower shall not be considered eligible for Claim Settlement", CGS1)])

g_amt = 1_50_00_000
fee_w = g_amt * 0.85 * 0.90 / 100
assert round(fee_w) == 114750
Q("009", T, CG, "Advanced",
  "A bank charged CGTMSE's standard fee rate obtains a guarantee of ₹1.5 crore for a women-owned small enterprise. The "
  "standard Annual Guarantee Fee for the above ₹1–2 crore slab is 0.85% a year. What is the first-year fee, and on "
  "what amount is the fee charged in later years?",
  ["₹1,14,750 (0.765%); later years on the outstanding amount", "₹1,27,500 (0.85%); later years on the original "
   "guaranteed amount", "₹1,14,750 (0.765%); later years on the original guaranteed amount", "₹1,02,000 (0.68%); later "
   "years on the outstanding amount"],
  concept="Computing CGTMSE's Annual Guarantee Fee",
  explanation="Women entrepreneurs get a 10% concession: 0.85% × 0.9 = 0.765%. First-year fee = 0.765% × ₹1.5 crore = "
              "₹1,14,750, charged on the guaranteed amount. From the second year the AGF is charged on the outstanding "
              "amount (for term loans, as on 31 December).",
  steps=["Rate = 0.85 × 0.9 = 0.765%", "Fee = 0.00765 × 1.5 crore = ₹1,14,750", "Later: on outstanding"],
  why="₹1,27,500 ignores the concession; later fees are on the outstanding, not the original amount; ₹1,02,000 "
      "deducts 20%.",
  computed=True,
  facts=[fact("Slab Above 1-2 crore: Standard Rate 0.85 ... AGF will be charged on the guaranteed amount for the first "
              "year and on the outstanding amount for the remaining tenure of the credit facility", CGS1),
         fact("Women entrepreneurs/ SC/ST/ Person with disability (PwD) / Transgender Entrepreneur would be given the "
              "discount of 10%", CGS1)])
assert round(g_amt * 0.85 / 100) == 127500 and round(g_amt * 0.85 * 0.8 / 100) == 102000
Q("009", T, PM4, "Advanced",
  "Consider the following statements about the restructured PM SVANidhi scheme approved in August 2025:\n"
  "I. Coverage is to be extended beyond statutory towns to census towns and peri-urban areas in a phased manner.\n"
  "II. The Department of Financial Services is responsible for access to loans and credit cards through banks and "
  "financial institutions, along with MoHUA.\n"
  "III. The third loan tranche was raised to ₹75,000.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Features of restructured PM SVANidhi",
  explanation="I is correct: coverage extends to census towns and peri-urban areas in phases. II is correct: MoHUA and "
              "DFS share responsibility, with DFS handling loans and credit cards. III is wrong: the third tranche stays "
              "at ₹50,000; only the first two were raised (to ₹15,000 and ₹25,000).",
  steps=["I ✓", "II ✓", "III ✗ (third tranche unchanged at ₹50,000)"],
  why="Any option containing III is wrong.",
  current=SVA,
  facts=[fact("Coverage expansion: extended beyond statutory towns to census towns and peri-urban areas, in a phased "
              "manner", SVANIDHI),
         fact("The Ministry of Housing & Urban Affairs (MoHUA) and the Department of Financial Services (DFS) share "
              "responsibility. DFS handles access to loans and credit cards through banks and financial institutions",
              SVANIDHI),
         fact("Third tranche: unchanged at Rs. 50,000", SVANIDHI)])

Q("010", T, PM4, "Basic",
  "Does Pradhan Mantri Suraksha Bima Yojana (PMSBY) reimburse hospitalisation expenses after an accident?",
  ["No; it pays only for accidental death or specified disability", "Yes, up to ₹1 lakh", "Yes, up to ₹2 lakh",
   "Yes, but only for road accidents"],
  concept="Scope of PMSBY",
  explanation="PMSBY is a one-year personal accident cover paying ₹2 lakh for accidental death or total permanent "
              "disability and ₹1 lakh for specified partial disability. It does not reimburse hospitalisation "
              "expenses.",
  steps=["PMSBY: death/disability benefit only; no hospitalisation reimbursement"],
  why="₹1 lakh and ₹2 lakh are disability/death benefits, not hospitalisation cover; there is no road-accident-only "
      "reimbursement.",
  facts=[fact("Is there any provision for reimbursement of hospitalisation expenses following accident resulting in death "
              "or disablement? No", D_PMSBY)])
Q("010", T, CG, "Basic",
  "What does the 'Hybrid / Partial Collateral Security' product of CGTMSE allow?",
  ["The lender may take collateral for part of the loan and cover the unsecured part under CGS-I, up to ₹10 crore",
   "The lender may take third-party guarantees for the whole loan and still get CGTMSE cover",
   "The borrower may pledge mutual fund units instead of paying the guarantee fee",
   "CGTMSE and NCGTC may jointly guarantee the same loan"],
  concept="Hybrid security model",
  explanation="Under the hybrid model, MLIs may obtain collateral for part of the credit and get the remaining unsecured "
              "part (up to a maximum of ₹10 crore) covered by CGTMSE, which has a notional second charge on the "
              "collateral. Credit already covered through NCGTC is not eligible.",
  steps=["Secured part: collateral", "Unsecured part (≤ ₹10 crore): CGTMSE cover"],
  why="Third-party guarantees make a loan ineligible; there is no fee-for-pledge option; NCGTC-covered credit is "
      "excluded.",
  facts=[fact("'Hybrid Security' product has been introduced where the MLIs will be allowed to obtain collateral security "
              "for a part of the credit facility, whereas the remaining unsecured part of the credit facility, upto a "
              "maximum of ₹ 10 crore, can be covered under CGS-I. CGTMSE will, however, have notional second charge on "
              "the collateral security", CGS1)])
Q("010", T, CG, "Intermediate",
  "For how long does a CGTMSE guarantee cover a borrower who has been given only working capital facilities?",
  ["For a block of 5 years, which can be renewed, with no overall cap on the coverage period",
   "For 18 months, the lock-in period, and then it ends",
   "For 10 years, and it cannot be renewed",
   "Only for one year at a time, like the annual fee"],
  concept="Tenure of guarantee for working capital",
  explanation="For term credit the cover runs through the agreed tenure; where working capital alone is given, cover is "
              "for 5 years or a block of 5 years. It can be renewed after the initial block, and there is no maximum "
              "coverage period for working capital accounts.",
  steps=["WC only → 5-year blocks, renewable, no overall cap"],
  why="18 months is the lock-in for claims; 10 years and one year are not the scheme's periods.",
  facts=[fact("Where working capital alone is extended to the eligible borrower, the guarantee cover shall be for a period "
              "of 5 years or a block of 5 years ... Guarantee for working capital account can be renewed after "
              "completion of initial 5 years block coverage. There is no maximum guarantee coverage period cap for "
              "working capital account", CGS1)])
Q("010", T, CG, "Intermediate",
  "What happens under CGTMSE's CGS-I if a lending institution does not pay the annual guarantee fee demanded for a "
  "covered loan by the due date (normally 30 March)?",
  ["The Trust's liability for that credit facility lapses; revival may be sought within the next financial year with "
   "penal interest", "The fee is simply recovered from the claim amount later", "The cover continues, but the fee "
   "doubles", "The borrower's account is automatically classified as NPA"],
  concept="Non-payment of AGF",
  explanation="If the annual fee is not paid in time, the Trust's liability for that credit facility lapses. A request "
              "for revival must be made within the next financial year, the account must be standard, and dues are "
              "charged with penal interest at 4% over Bank Rate and an additional risk premium.",
  steps=["Non-payment → guarantee lapses", "Revival: next FY, standard account, penal interest"],
  why="The fee is not netted from claims, does not just double, and has no effect on the borrower's asset "
      "classification.",
  facts=[fact("AGF so demanded would be paid by the MLIs on or before 30th March each year ... in the event of non-payment "
              "of annual service / guarantee fee within the stipulated time ... liability of the Trust to guarantee such "
              "credit facility would lapse", CGS1),
         fact("Request for revival of account will have to be submitted within next financial year ... Any fee due by "
              "the MLI ... will be demanded along with penal interest (@ 4% over Bank Rate, per annum)", CGS1)])
Q("010", T, CG, "Intermediate",
  "Which of the following credit facilities is NOT eligible for cover under CGTMSE's CGS-I?",
  ["A loan already covered for guarantee through NCGTC Ltd", "A collateral-free term loan to a micro enterprise in "
   "retail trade", "A collateral-free loan to an educational/training institution set up as an MSE", "A working "
   "capital limit given without collateral to a small manufacturing unit"],
  concept="Ineligible facilities",
  explanation="A credit facility already guaranteed through NCGTC (or whose risk is covered by DICGC, RBI, the "
              "Government or an insurer, to that extent) cannot be covered. Retail and wholesale trade and "
              "educational/training institutions have been made eligible activities.",
  steps=["Already covered by NCGTC → excluded"],
  why="Trading and educational/training institutions are eligible; collateral-free working capital is the core of "
      "the scheme.",
  facts=[fact("Any Credit facility shall not be eligible to covered under the Scheme if the said credit facility has been "
              "covered for guarantee through NCGTC Ltd", CGS1),
         fact("Trading (Retail / Wholesale Trade) has been made eligible activity under CGTMSE for all MLIs (including "
              "RRBs) ... Educational / Training Institution also made eligible activity", CGS1)])

fees_prev = 40
cap = 2 * fees_prev
assert cap == 80 and 95 - cap == 15
Q("010", T, CG, "Advanced",
  "In FY 2026-27 a lending institution remitted ₹40 crore to CGTMSE as fees and recoveries. In FY 2027-28 it lodges "
  "eligible claims of ₹95 crore. Applying the payout cap in CGS-I, what happens?",
  ["Claims up to ₹80 crore are settled; ₹15 crore of claims are kept suspended until the payout is within the cap",
   "All ₹95 crore is settled, as each claim is eligible", "Only ₹40 crore is settled and the rest rejected",
   "Claims up to ₹60 crore (1.5 times) are settled; ₹35 crore is rejected"],
  concept="Claim payout cap",
  explanation="Claims of an MLI are settled up to 2 times the fees (including recoveries) it remitted in the previous "
              "financial year: 2 × 40 = ₹80 crore. Claims beyond that (₹95 − 80 = ₹15 crore) are suspended, not "
              "rejected, until the payout is brought within the cap.",
  steps=["Cap = 2 × 40 = 80", "Excess = 95 − 80 = 15 → suspended"],
  why="The cap is 2 times, not 1 or 1.5 times, and the excess is suspended rather than rejected; all claims cannot be "
      "paid at once.",
  computed=True,
  facts=[fact("Claims of the respective MLI will be settled to the extent of 2 times of the fee including recovery "
              "remitted during the previous financial year. Any claim lodged / received exceeding 2 times of the total "
              "fee including recovery remitted by MLI will be suspended till such time the position is remedied", CGS1)])

import datetime as _dt2
last_disb = _dt2.date(2026, 1, 20)
lock_end = _dt2.date(2027, 7, 20)          # 18 months after last disbursement
npa = _dt2.date(2026, 11, 15)
deadline = _dt2.date(max(npa, lock_end).year + 3, max(npa, lock_end).month, max(npa, lock_end).day)
assert max(npa, lock_end) == lock_end and deadline == _dt2.date(2030, 7, 20)
Q("010", T, CG, "Advanced",
  "A ₹25 lakh CGTMSE-covered term loan (tenure 5 years) was last disbursed on 20 January 2026, which is later than the "
  "guarantee start date. It turns NPA on 15 November 2026. The account is not a fraud or wilful default, and recovery "
  "proceedings have begun. When can the bank lodge a claim, and by when must it do so?",
  ["From 20 July 2027, after the 18-month lock-in; within 3 years of that date, i.e. by 20 July 2030",
   "Immediately on 15 November 2026; within 3 years, i.e. by 15 November 2029",
   "From 20 October 2026, after a 9-month lock-in; by 20 October 2029",
   "From 15 November 2027, one year after NPA; by 15 November 2028"],
  concept="Timing of a CGTMSE claim",
  explanation="The lock-in is 18 months from the later of last disbursement and guarantee start: 20 Jan 2026 + 18 months "
              "= 20 July 2027 (the 9-month lock-in applies only to guarantees up to ₹10 lakh with tenure up to 36 "
              "months). The claim must be made within 3 years of the NPA date or the end of lock-in, whichever is later: "
              "20 July 2027 + 3 years = 20 July 2030.",
  steps=["Lock-in ends 20-7-2027 (18 m)", "Later of NPA (15-11-2026) and lock-in end = 20-7-2027",
         "Deadline = 20-7-2030"],
  why="A claim cannot be lodged during lock-in; the 9-month lock-in does not apply to a ₹25 lakh, 5-year loan; the "
      "one-year option has no basis in the scheme.",
  computed=True,
  facts=[fact("The lending institution may invoke the guarantee in respect of credit facility within a maximum period of "
              "3 years from the NPA date or lock-in period whichever is later", CGS1),
         fact("The lock-in period of 18 months for guarantee (or 9 months for guarantee upto ₹10 lakh with tenure upto 36 "
              "months wef December 15, 2023) from either the date of last disbursement of the loan to the borrower or "
              "the guarantee start date ... whichever is later, has lapsed", CGS1)])

Q("008", "Government Financial Schemes", "Credit guarantee schemes", "Advanced",
  "Consider the following conditions for settlement of claims under CGTMSE's CGS-I:\n"
  "I. Accounts classified by the lender as fraud, wilful defaulter or non-co-operative borrower are not eligible.\n"
  "II. An account that slips into NPA within 90 days of the material date (the date the guarantee fee is paid) is not "
  "eligible.\n"
  "III. The guarantee may be invoked up to five years after the NPA date.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Claim eligibility under CGS-I",
  explanation="I and II are correct. III is wrong: the guarantee must be invoked within a maximum of 3 years from the NPA "
              "date or the end of the lock-in period, whichever is later.",
  steps=["I ✓", "II ✓", "III ✗ (3 years)"],
  why="Any option with III is wrong.",
  facts=[fact("The accounts classified by the Lending Institution as Fraud / Willful defaulter / Non-Co-operative borrower "
              "shall not be considered eligible for Claim Settlement ... The account slipping into NPA within 90 days from "
              "the material date shall not be considered eligible for Claim Settlement", CGS1),
         fact("The lending institution may invoke the guarantee in respect of credit facility within a maximum period of 3 "
              "years from the NPA date or lock-in period whichever is later", CGS1)])

# ============================================================================================ RBI Circulars
T = "RBI Circulars and Regulatory Updates"
RD = "Recent RBI directions"
_N = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id={}&Mode=0"
_P = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid={}"
N_CRR99, N_PENAL, N_SLFPD, N_CASS = _N.format(13736), _N.format(13728), _N.format(13726), _N.format(13717)
N_KYCSFB, N_NSM, N_SCST, N_MISC = _N.format(13700), _N.format(13723), _N.format(13716), _N.format(13731)
N_NOV, N_FEMA, N_DELHI = _N.format(13706), _N.format(13714), _N.format(13746)
P_DRP, P_RBL, P_DC, P_OMC = _P.format(63743), _P.format(63820), _P.format(63862), _P.format(63784)
P_BOARD, P_RATES, P_SFS, P_CVA = _P.format(63892), _P.format(63894), _P.format(63873), _P.format(63749)
P_PSL, P_NBFC = _P.format(63925), _P.format(63773)

Q("008", T, RD, "Basic",
  "By a circular of 9 October 2026, RBI raised the minimum CRR that scheduled banks must maintain on every day of a "
  "reporting fortnight to what share of the required CRR?",
  ["99 per cent, from 90 per cent", "100 per cent, from 95 per cent", "95 per cent, from 90 per cent",
   "90 per cent, from 70 per cent"],
  concept="Daily minimum CRR maintenance",
  explanation="Banks must keep the fortnightly average CRR at the prescribed level, with a daily floor. Reviewing "
              "liquidity conditions, RBI raised the daily minimum from 90% to 99% of the requirement, effective from the "
              "fortnight beginning 16 October 2026.",
  steps=["Daily floor: 90% → 99% of required CRR (from fortnight beginning 16-10-2026)"],
  why="The other pairs are not the figures in the circular.",
  current=ca("2026-10-09"),
  facts=[fact("it has been decided to increase the minimum daily maintenance of the CRR from 90 per cent of the "
              "requirement to 99 per cent effective from the fortnight beginning October 16, 2026", N_CRR99)])
Q("008", T, RD, "Intermediate",
  "After the Bank Rate was raised to 5.75% on 7 October 2026, what penal interest rates apply to shortfalls in CRR and "
  "SLR requirements?",
  ["8.75% or 10.75% (Bank Rate plus 3 or 5 percentage points, depending on the duration of the shortfall)",
   "8.50% or 10.50% (Bank Rate plus 3 or 5 percentage points)", "5.75% flat, equal to the Bank Rate",
   "7.75% or 9.75% (Bank Rate plus 2 or 4 percentage points)"],
  concept="Penal interest linked to the Bank Rate",
  explanation="Penal rates on reserve shortfalls are Bank Rate + 3 percentage points or Bank Rate + 5 percentage points, "
              "depending on how long the shortfall lasts. With the Bank Rate at 5.75%, they are 8.75% and 10.75% (they "
              "were 8.50% and 10.50% when the Bank Rate was 5.50%).",
  steps=["5.75 + 3 = 8.75%", "5.75 + 5 = 10.75%"],
  why="8.50%/10.50% were the rates before the change; the flat and +2/+4 options misstate the formula.",
  current=ca("2026-10-07"),
  facts=[fact("the Bank Rate is revised upwards by 25 basis points from 5.50 per cent to 5.75 per cent ... Penal interest "
              "rates on shortfalls in reserve requirements: Bank Rate plus 3.0 percentage points (8.75 per cent) or Bank "
              "Rate plus 5.0 percentage points (10.75 per cent)", N_PENAL)])
Q("008", T, RD, "Intermediate",
  "In its Statement on Developmental and Regulatory Policies of 7 October 2026, what did RBI announce for the Account "
  "Aggregator (AA) framework?",
  ["Interoperability among NBFC-AAs, and inclusion of bank deposit information in depositories' Consolidated Account "
   "Statement through AAs, both by 31 December 2026",
   "Merger of all NBFC-AAs into a single entity run by NPCI",
   "Mandatory linking of every bank account to an AA by 31 March 2027",
   "Permission for AAs to lend directly to customers using the data they hold"],
  concept="Account Aggregator measures",
  explanation="RBI decided to implement interoperability among NBFC-AAs so customers can fetch and share data from "
              "different Financial Information Providers through any AA of their choice, and to let SEBI-regulated "
              "depositories show bank deposit information in the CAS through AAs. Both are expected by 31 December "
              "2026.",
  steps=["AA interoperability", "Bank deposits in CAS via AAs", "Target: 31-12-2026"],
  why="No merger, mandatory linking or lending by AAs was announced.",
  current=ca("2026-10-07"),
  facts=[fact("it has been decided to implement interoperability among NBFC-Account Aggregators (NBFC-AA) ... Depositories "
              "regulated by the Securities and Exchange Board of India are being facilitated to include information "
              "related to bank deposit accounts in their Consolidated Account Statement (CAS) through the NBFC-AAs ... "
              "expected to be implemented by December 31, 2026", P_DRP)])
Q("008", T, RD, "Intermediate",
  "In October 2026, RBI sanctioned the amalgamation of the Indian branches of Emirates NBD Bank P.J.S.C. with which "
  "Indian bank, and from when?",
  ["RBL Bank Limited, effective 1 December 2026", "Yes Bank Limited, effective 1 November 2026",
   "IDBI Bank Limited, effective 1 January 2027", "Federal Bank Limited, effective 16 October 2026"],
  concept="Bank amalgamation under the BR Act",
  explanation="RBI sanctioned the scheme under Section 44A(4) of the Banking Regulation Act, 1949. From 1 December 2026 "
              "all Indian branches of Emirates NBD Bank function as branches of RBL Bank Limited.",
  steps=["Emirates NBD (India branches) → RBL Bank; effective 1-12-2026; Sec 44A(4)"],
  why="The other banks and dates are not those in RBI's press release.",
  current=ca("2026-10-16"),
  facts=[fact("The Reserve Bank of India has sanctioned the Scheme of Amalgamation of Indian branches of Emirates NBD Bank "
              "P.J.S.C. (Transferor Bank) with RBL Bank Limited (Transferee Bank) ... under sub-section (4) of Section "
              "44A of the Banking Regulation Act, 1949. The effective date of the amalgamation shall be December 01, "
              "2026", P_RBL)])
Q("008", T, RD, "Intermediate",
  "After the UT of Ladakh notified five new districts (Sham, Nubra, Changthang, Zanskar and Drass), which bank did RBI "
  "assign lead bank responsibility for all of them, in August 2026?",
  ["State Bank of India", "Jammu & Kashmir Bank", "Punjab National Bank", "Bank of Baroda"],
  concept="Lead Bank Scheme",
  explanation="By its circular of 10 August 2026, RBI designated State Bank of India as lead bank for all five new "
              "districts, with new district working codes; lead banks of the other districts of Ladakh are unchanged.",
  steps=["5 new Ladakh districts → SBI"],
  why="The other banks were not assigned these districts.",
  current=ca("2026-08-10"),
  facts=[fact("The Administration of Union Territory (UT) of Ladakh has notified formation of five new districts, viz., "
              "Sham, Nubra, Changthang, Zanskar and Drass ... Lead Bank Responsibility assigned to: State Bank of India "
              "(all five)", "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13675&Mode=0")])

req = 10_000
floor99 = 0.99 * req
days = [10_150, 9_950, 9_880, 10_100] + [10_000] * 10
assert floor99 == 9_900 and sum(days) / 14 >= req and min(days) < floor99
assert abs(sum(days) / 14 - 10_005.714) < 0.01
Q("008", T, RD, "Advanced",
  "A bank's required CRR for the fortnight beginning 16 October 2026 is ₹10,000 crore. Its daily CRR balances are "
  "₹10,150 crore, ₹9,950 crore, ₹9,880 crore and ₹10,100 crore on the first four days and ₹10,000 crore on each of the "
  "other ten days. Which statement is correct under RBI's circular of 9 October 2026?",
  ["The fortnightly average (about ₹10,006 crore) is adequate, but the ₹9,880 crore day breaches the daily floor of "
   "₹9,900 crore", "The bank complies fully, since the daily floor is ₹9,000 crore",
   "The bank fails because its balance fell below ₹10,000 crore on two days",
   "The bank fails because the fortnightly average is below ₹10,000 crore"],
  concept="Average and daily CRR requirements",
  explanation="The average must be at least the required CRR, and every day's balance at least 99% of it. Average = "
              "(10,150 + 9,950 + 9,880 + 10,100 + 10 × 10,000) ÷ 14 ≈ ₹10,006 crore, which is adequate. Daily floor = "
              "0.99 × 10,000 = ₹9,900 crore; the ₹9,880 crore day falls short, while ₹9,950 crore is within the floor.",
  steps=["Average ≈ 10,005.7 ≥ 10,000 ✓", "Floor = 9,900", "9,880 < 9,900 ✗"],
  why="₹9,000 crore was the floor under the old 90% rule; balances between 99% and 100% on a day are allowed; the "
      "average is above the requirement.",
  computed=True, current=ca("2026-10-09"),
  facts=[fact("The scheduled banks are allowed to maintain minimum Cash Reserve Ratio (CRR) of not less than 90 percent of "
              "the required CRR on all days during the reporting fortnight, in such a manner that the average of CRR "
              "maintained daily shall not be less than the CRR prescribed ... decided to increase the minimum daily "
              "maintenance of the CRR from 90 per cent of the requirement to 99 per cent effective from the fortnight "
              "beginning October 16, 2026", N_CRR99)])
Q("008", T, RD, "Advanced",
  "RBI's circular of 26 October 2026 reassigned lead bank responsibility after the reorganisation of districts in the "
  "NCT of Delhi. Consider:\n"
  "I. Three new districts (Old Delhi, Central North and Outer North) were formed, and Shahdara district ceased to "
  "exist.\n"
  "II. Lead bank responsibility for Central district moved from Canara Bank to State Bank of India.\n"
  "III. Bank of Baroda, earlier lead bank of Shahdara, was made lead bank of Old Delhi.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Lead Bank Scheme",
  explanation="I is correct: the Delhi government's notification of 25 December 2025 formed three new districts and "
              "abolished Shahdara. II is correct: Central moved from Canara Bank to SBI (Northwest moved from PNB to "
              "Union Bank of India). III is wrong: Bank of Baroda's responsibility for Shahdara was revoked, and Old Delhi "
              "went to Canara Bank (Central North to SBI, Outer North to PNB).",
  steps=["I ✓", "II ✓", "III ✗ (Old Delhi → Canara Bank)"],
  why="Any option with III is wrong.",
  current=ca("2026-10-26"),
  facts=[fact("three new districts, viz., Old Delhi, Central North and Outer North have been formed and Shahdara district "
              "has ceased to exist ... Old Delhi: Canara Bank; Central North: State Bank of India; Outer North: Punjab "
              "National Bank ... Central: Canara Bank → State Bank of India; Northwest: Punjab National Bank → Union Bank "
              "of India ... Shahdara: Bank of Baroda stands revoked", N_DELHI)])

Q("009", T, RD, "Basic",
  "On 25 October 2026 the Prime Minister inaugurated RBI's new Data Centre and Cybersecurity Training Institute. Where "
  "are they located?",
  ["Bhubaneswar, Odisha", "Hyderabad, Telangana", "Navi Mumbai, Maharashtra", "Gandhinagar, Gujarat"],
  concept="RBI infrastructure",
  explanation="The Data Centre and Cybersecurity Training Institute are in Bhubaneswar. The Data Centre will house RBI's "
              "mission-critical systems including RTGS and NEFT, and the Institute will build expertise in "
              "cybersecurity, AI and emerging technologies.",
  steps=["Bhubaneswar: Data Centre (RTGS, NEFT) + Cybersecurity Training Institute"],
  why="The other cities are not where these facilities were set up.",
  current=ca("2026-10-25"),
  facts=[fact("The Hon'ble Prime Minister of India, Shri Narendra Modi, today inaugurated the Reserve Bank of India's "
              "newly established Data Centre and Cybersecurity Training Institute in Bhubaneswar, Odisha ... the new Data "
              "Centre will house RBI's mission-critical systems, including RTGS and NEFT", P_DC)])
Q("009", T, RD, "Basic",
  "Besides reviewing economic conditions, the activities of which RBI subsidiary did the 625th meeting of RBI's Central "
  "Board (30 October 2026) review?",
  ["Deposit Insurance and Credit Guarantee Corporation (DICGC)", "National Housing Bank",
   "Bharatiya Reserve Bank Note Mudran Ltd", "Reserve Bank Information Technology Pvt Ltd"],
  concept="RBI Central Board",
  explanation="The 625th meeting, held in Mumbai under Governor Sanjay Malhotra, reviewed the activities of DICGC and of "
              "select Central Office departments, and the Board took the Integrity Pledge for Vigilance Awareness Week "
              "2026.",
  steps=["625th Board meeting → reviewed DICGC"],
  why="The other subsidiaries were not named in the press release.",
  current=ca("2026-10-30"),
  facts=[fact("The Board reviewed the activities of Deposit Insurance and Credit Guarantee Corporation and activities of "
              "select Central Office Departments of the Bank", P_BOARD)])
Q("009", T, RD, "Basic",
  "Under RBI's Master Direction on Note Sorting Machines (October 2026), when is a banknote 'fit' for recycling?",
  ["When it is genuine, clean enough for its denomination to be readily ascertained, and passes every fitness "
   "parameter", "When it passes at least seven of the ten fitness parameters",
   "When it is genuine, whatever its physical condition", "When it belongs to any series ever issued by RBI"],
  concept="Fit and unfit notes",
  explanation="A fit note is genuine and sufficiently clean for its denomination to be readily ascertained. Each "
              "fitness parameter (soiling, limpness, dog-ears, tears, holes, stains, graffiti, folds, decolouration, "
              "repair) is evaluated individually, and a note must pass all of them. Notes of a phased-out series are "
              "unfit.",
  steps=["Genuine + clean + passes all parameters → fit"],
  why="Passing some parameters is not enough; condition matters; phased-out series are unfit.",
  current=ca("2026-10-02"),
  facts=[fact("A fit note is a note that is genuine, sufficiently clean to allow its denomination to be readily "
              "ascertained and thus suitable for recycling. An unfit note is a note that is not suitable for recycling "
              "because of its physical condition or belongs to a series that has been phased out ... A note must pass "
              "all the fitness parameters to be considered fit for recycling", N_NSM)])
Q("009", T, RD, "Intermediate",
  "On 10 October 2026, RBI opened a special window from 12 October 2026 for which entities, and for what?",
  ["The three public sector oil marketing companies (IOCL, HPCL and BPCL), to meet their entire daily dollar "
   "requirements through sale of USD by RBI via designated banks",
   "All exporters, to sell dollars to RBI at a fixed rate",
   "Public sector banks, to borrow dollars from RBI for FCNR(B) redemptions",
   "State governments, to borrow against their gold reserves"],
  concept="Forex market measures",
  explanation="RBI decided to meet the entire daily dollar requirements of Indian Oil, HPCL and BPCL by selling USD to "
              "them through designated banks, from 12 October 2026 until further notice. This takes their large demand "
              "out of the market.",
  steps=["Who: IOCL, HPCL, BPCL", "What: RBI sells USD through designated banks", "From 12-10-2026"],
  why="The window is for the three PSU OMCs' dollar purchases, not exporters, banks or States.",
  current=ca("2026-10-10"),
  facts=[fact("Reserve Bank of India has decided to open a special window to meet the entire daily dollar requirements of "
              "three public sector oil marketing companies (OMCs), viz. Indian Oil Corporation Limited, Hindustan "
              "Petroleum Corporation Limited and Bharat Petroleum Corporation Limited ... The facility will come in "
              "effect from October 12, 2026", P_OMC)])
Q("009", T, RD, "Intermediate",
  "Under RBI's circular of 2 September 2026, how often and by when must regulated entities report the relief measures "
  "they extend in areas affected by natural calamities?",
  ["Half-yearly through the CIMS portal, within 30 days of the half-year's end (by 30 October and 30 April)",
   "Monthly, by the 7th of the next month, by e-mail", "Quarterly, within 15 days, through SLBCs",
   "Annually, with the audited balance sheet"],
  concept="Natural calamity relief reporting",
  explanation="The revised framework (effective 1 July 2026) requires REs to submit relief-measure data on the CIMS "
              "portal half-yearly, within 30 days of each half-year: by 30 October for the half-year to 30 September and "
              "by 30 April for the half-year to 31 March.",
  steps=["Half-yearly; CIMS; 30 days → 30 Oct / 30 Apr"],
  why="Monthly, quarterly and annual reporting are not what the circular prescribes.",
  current=ca("2026-09-02"),
  facts=[fact("REs to submit data relating to relief measures extended in areas affected by natural calamities through the "
              "CIMS portal on a half-yearly basis ... The return shall be submitted within 30 days from the end of each "
              "half-year, i.e., by October 30 for the half-year ending September 30, and by April 30 for the half-year "
              "ending March 31", "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13692&Mode=0")])
Q("009", T, RD, "Intermediate",
  "After the MPC's decision of 7 October 2026, at what rate does RBI provide the Standing Liquidity Facility "
  "(collateralised liquidity support) to Primary Dealers?",
  ["At the revised repo rate of 5.50%", "At the MSF rate of 5.75%", "At the SDF rate of 5.25%",
   "At the Bank Rate plus 1%"],
  concept="Standing Liquidity Facility for PDs",
  explanation="The MPC raised the policy repo rate by 25 basis points from 5.25% to 5.50%. The SLF to Primary Dealers is "
              "available at the repo rate, i.e. 5.50%, with immediate effect.",
  steps=["SLF for PDs = repo rate = 5.50%"],
  why="MSF and SDF rates and Bank Rate + 1% are not the SLF rate.",
  current=ca("2026-10-07"),
  facts=[fact("decided by the Monetary Policy Committee (MPC) to increase the policy repo rate under the Liquidity "
              "Adjustment Facility (LAF) by 25 basis points from 5.25 per cent to 5.50 per cent ... the Standing "
              "Liquidity Facility provided to Primary Dealers (PDs) ... would be available at the revised repo rate of "
              "5.50 per cent", N_SLFPD)])

walr_f, wadt_f, walr_o, wadt_o = 8.51, 5.61, 8.96, 6.55
assert round((walr_f - wadt_f) * 100) == 290 and round((walr_o - wadt_o) * 100) == 241
assert round((8.61 - 8.55) * 100) == 6
Q("009", T, RD, "Advanced",
  "RBI's data of 30 October 2026 show, for September 2026, WALR on fresh rupee loans of 8.51% and on outstanding loans "
  "of 8.96%, and WADTDR on fresh term deposits of 5.61% and on outstanding term deposits of 6.55%. The 1-year median "
  "MCLR was 8.55% in October against 8.61% in September. Which statement is correct?",
  ["The spread on fresh business (about 290 bps) was wider than on outstanding business (about 241 bps), and MCLR "
   "fell by 6 bps",
   "The spread on outstanding business (about 290 bps) was wider than on fresh business (about 241 bps)",
   "Both spreads were about 241 bps, and MCLR rose by 6 bps",
   "The fresh-loan WALR was above the outstanding WALR, showing rising lending rates"],
  concept="Reading lending and deposit rate data",
  explanation="Fresh spread = 8.51 − 5.61 = 2.90 percentage points (290 bps); outstanding spread = 8.96 − 6.55 = 2.41 "
              "(241 bps). MCLR fell from 8.61% to 8.55% (6 bps). Fresh-loan WALR (8.51%) was below the outstanding WALR "
              "(8.96%).",
  steps=["Fresh: 8.51 − 5.61 = 2.90", "Outstanding: 8.96 − 6.55 = 2.41", "MCLR: −6 bps"],
  why="The spreads are swapped or equated in the other options; MCLR fell; fresh WALR was lower, not higher.",
  computed=True, current=ca("2026-10-30"),
  facts=[fact("The WALR on outstanding rupee loans of SCBs remained unchanged at 8.96 per cent in September 2026 ... The "
              "WALR on fresh rupee loans of SCBs declined to 8.51 per cent ... 1-Year median MCLR of SCBs declined to 8.55 "
              "per cent in October 2026 from 8.61 per cent in September 2026 ... WADTDR on outstanding rupee term "
              "deposits ... 6.55 per cent ... WADTDR on fresh rupee term deposits of SCBs declined to 5.61 per cent",
              P_RATES)])
Q("009", T, RD, "Advanced",
  "Consider the following statements about RBI's Commercial Banks – Credit Valuation Adjustment (CVA) Framework "
  "Directions, 2026:\n"
  "I. They were finalised on 7 October 2026 after a draft of 7 August 2026.\n"
  "II. Eligible banks may choose a simpler approach to the CVA capital charge.\n"
  "III. They took effect immediately on issue.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="CVA risk capital",
  explanation="CVA risk is the risk of loss from changes in the counterparty credit spread on derivatives. The draft of "
              "7 August 2026 was finalised on 7 October 2026 with revisions such as letting eligible banks choose a "
              "simpler approach, more risk-sensitive supervisory risk weights and clearer recognition of CVA hedges. "
              "The Directions come into effect on 1 April 2027, so III is wrong.",
  steps=["I ✓", "II ✓", "III ✗ (effective 1-4-2027)"],
  why="Any option with III is wrong.",
  current=ca("2026-10-07"),
  facts=[fact("The Reserve Bank of India had issued draft Directions on the 'Credit Valuation Adjustment (CVA) Framework' "
              "on August 7, 2026 ... Key revisions included: (i) allowing eligible banks to choose a simpler approach ... "
              "the Reserve Bank has today released the ... Directions, 2026 ... These instructions will come into effect "
              "from April 1, 2027", P_CVA)])
Q("009", T, RD, "Advanced",
  "On 5 November 2026 RBI released drafts consolidating its priority sector lending (PSL) instructions. Consider:\n"
  "I. Separate draft Directions were issued for commercial banks, small finance banks, local area banks, regional rural "
  "banks and urban co-operative banks.\n"
  "II. Comments were invited up to 26 November 2026.\n"
  "III. The consolidated Directions replaced the existing PSL instructions with immediate effect.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Consolidation of PSL instructions (draft)",
  explanation="RBI placed five draft 'Priority Sector Lending – Targets and Classification' Directions, one for each "
              "type of regulated entity, for comments up to 26 November 2026. They are drafts: the existing PSL "
              "instructions continue until final Directions are issued, after which instructions not included will be "
              "repealed separately.",
  steps=["I ✓ (five RE-wise drafts)", "II ✓", "III ✗ (drafts only)"],
  why="Any option with III is wrong, since these are only drafts.",
  current=ca("2026-11-05"),
  facts=[fact("the following draft Directions are being placed on the website for public comments: Reserve Bank of India "
              "(Commercial Banks / Small Finance Banks / Local Area Banks / Regional Rural Banks / Urban Co-operative "
              "Banks – Priority Sector Lending – Targets and Classification) Directions, 2026 ... comments / feedback may "
              "be submitted on or before November 26, 2026", P_PSL)])
Q("009", T, RD, "Advanced",
  "In June 2026 RBI gave temporary relief to attract fresh non-resident deposits. By amendments of August–September "
  "2026, the end date of these measures was advanced from 30 September 2026 to 31 August 2026. Consider:\n"
  "I. Fresh FCNR(B) deposits of 3–5 years and NRE term deposits of 3 years or more were exempt from CRR and SLR.\n"
  "II. The interest rate ceiling on fresh FCNR(B) deposits of 3–5 years was temporarily withdrawn.\n"
  "III. The relief covered NRE savings deposits of any tenor.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Relief measures for non-resident deposits",
  explanation="I is correct: fresh FCNR(B) deposits of 3–5 years (from 8 June) and NRE term deposits of 3 years or more "
              "(from 19 June) were exempted from CRR/SLR, and advances against them were excluded from ANBC. II is "
              "correct: the interest ceiling on such FCNR(B) deposits was temporarily withdrawn. All these ended on "
              "31 August 2026 instead of 30 September. III is wrong: only NRE term deposits of 3 years or more were "
              "covered.",
  steps=["I ✓", "II ✓", "III ✗ (NRE term ≥ 3 years only)"],
  why="Any option containing III is wrong.",
  current=ca("2026-08-25"),
  facts=[fact("exemption from CRR and SLR maintenance have been provided to fresh FCNR(B) deposits of minimum tenor of three "
              "years and maximum tenor of five years and fresh Non-Resident (External) Rupee (NRE) term deposits of tenor "
              "of three years or more ... it has been decided to amend the date 'September 30, 2026' to the date 'August "
              "31, 2026'", "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13680&Mode=0"),
         fact("temporary withdrawal of the interest rate ceiling on fresh FCNR(B) deposits of 3-5 year tenors ... for the "
              "period until September 30, 2026 ... amend ... to 'August 31, 2026'", "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13685&Mode=0")])

Q("010", T, RD, "Basic",
  "At the 36th Conference of State Finance Secretaries held at RBI on 27 October 2026, what did the Governor urge the "
  "States to use for Direct Benefit Transfers?",
  ["Programmable Central Bank Digital Currency (P-CBDC)", "Pre-paid gift cards", "Cheques routed through CTS",
   "Treasury Bills"],
  concept="RBI and State finances",
  explanation="The Governor urged States to onboard the Unified Lending Interface (ULI), use programmable CBDC for DBT and "
              "make effective use of the SLBC forum. He released a booklet, 'Compendium on Cash and Debt Management for "
              "State Governments'.",
  steps=["DBT → programmable CBDC; credit → ULI"],
  why="The other instruments were not suggested.",
  current=ca("2026-10-27"),
  facts=[fact("The Governor urged the States to onboard onto the Unified Lending Interface (ULI) and utilise Programmable "
              "Central Bank Digital Currency (P-CBDC) for Direct Benefit Transfers (DBT) ... the Governor released a "
              "Booklet titled 'Compendium on Cash and Debt Management for State Governments'", P_SFS)])
Q("010", T, RD, "Basic",
  "Under its review of circulars issued under FEMA since June 2000, how many circulars that had ceased to be operative "
  "did RBI withdraw by its circular of 8 September 2026?",
  ["Seven", "Twelve", "Twenty-five", "Sixty-four"],
  concept="Rationalisation of FEMA circulars",
  explanation="RBI is comprehensively reviewing A.P. (DIR Series) circulars issued since 1 June 2000. On 8 September 2026 "
              "it withdrew seven circulars (mostly on ECB policy and rupee borrowing) that had become inoperative owing to "
              "amendments, redundancy, overlap or supersession.",
  steps=["8-9-2026: 7 FEMA circulars withdrawn"],
  why="The other numbers are not those in the circular.",
  current=ca("2026-09-08"),
  facts=[fact("a comprehensive review of circulars issued since June 01, 2000, is underway ... seven circulars as listed at "
              "Annex, that have ceased to be operative owing to subsequent regulatory amendments, redundancy, overlap or "
              "supersession by newer directives, are being withdrawn", "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13696&Mode=0")])
Q("010", T, RD, "Basic",
  "Under which provision did RBI cancel the Certificates of Registration of 13 NBFCs, as announced on 9 October 2026?",
  ["Section 45-IA(6) of the RBI Act, 1934", "Section 22 of the Banking Regulation Act, 1949",
   "Section 35A of the Banking Regulation Act, 1949", "Section 11 of the SEBI Act, 1992"],
  concept="Regulation of NBFCs",
  explanation="NBFCs are registered under Section 45-IA of the RBI Act, and Section 45-IA(6) empowers RBI to cancel a "
              "Certificate of Registration. Section 22 of the BR Act governs bank licences.",
  steps=["NBFC CoR cancellation → RBI Act s. 45-IA(6)"],
  why="Section 22 (licensing) and 35A (directions) of the BR Act apply to banks; SEBI Act s. 11 is SEBI's power.",
  current=ca("2026-10-09"),
  facts=[fact("The Reserve Bank of India, in exercise of powers conferred on it under Section 45-IA (6) of the Reserve Bank "
              "of India Act, 1934, has cancelled the Certificate of Registration of the following companies", P_NBFC)])
Q("010", T, RD, "Basic",
  "According to RBI data released on 30 October 2026, what was the 1-year median MCLR of scheduled commercial banks in "
  "October 2026?",
  ["8.55%", "8.96%", "8.51%", "6.55%"],
  concept="Lending rate data",
  explanation="The 1-year median MCLR declined to 8.55% in October 2026 from 8.61% in September. 8.96% and 8.51% are the "
              "WALRs on outstanding and fresh loans, and 6.55% the WADTDR on outstanding deposits (September 2026).",
  steps=["1-year median MCLR (Oct 2026) = 8.55%"],
  why="The other figures are different rates in the same release.",
  current=ca("2026-10-30"),
  facts=[fact("1-Year median Marginal Cost of Funds based Lending Rate (MCLR) of SCBs declined to 8.55 per cent in October "
              "2026 from 8.61 per cent in September 2026", P_RATES)])
Q("010", T, RD, "Intermediate",
  "By Amendment Directions of 7 October 2026, effective 1 April 2027, RBI deleted which section of the Commercial Banks "
  "– Miscellaneous Directions, 2025?",
  ["The sub-section on deferment of option premium", "The sub-section on penal charges on loans",
   "The sub-section on unclaimed deposits", "The sub-section on safe deposit lockers"],
  concept="Housekeeping amendments",
  explanation="Consequent to the Forthcoming Instructions Amendment Directions, 2026, Sub-section D of Chapter IV "
              "(paragraph 38) on deferment of option premium is deleted from 1 April 2027.",
  steps=["Deleted: Ch. IV, Sub-section D (deferment of option premium), from 1-4-2027"],
  why="The other subjects were not touched by this amendment.",
  current=ca("2026-10-07"),
  facts=[fact("Please refer to Sub-section D of Chapter IV of the Reserve Bank of India (Commercial Banks - Miscellaneous) "
              "Directions, 2025 on deferment of option premium ... These Amendment Directions shall come into effect from "
              "April 1, 2027 ... Sub-section D of Chapter IV (Paragraph 38) shall be deleted", N_MISC)])
Q("010", T, RD, "Intermediate",
  "Under the FEMA (Export and Import of Goods and Services) (Amendment) Regulations notified on 22 September 2026, who "
  "handles export, import and merchanting trade transactions undertaken before 1 October 2026 that earlier needed RBI "
  "approval?",
  ["Authorised Dealers", "The Directorate General of Foreign Trade", "RBI's Regional Offices", "Customs authorities"],
  concept="Delegation to Authorised Dealers",
  explanation="A new regulation 20 empowers Authorised Dealers to handle transactions related to export and import of "
              "goods and services and merchanting trade undertaken before 1 October 2026 that required RBI approval under "
              "the 2015 regulations and the old Master Directions. Exporters on the Caution List as on 30 September 2026 "
              "stay governed by the earlier orders.",
  steps=["Pre-1-10-2026 cases needing RBI approval → Authorised Dealers"],
  why="DGFT, customs and RBI's Regional Offices are not given this power.",
  current=ca("2026-09-22"),
  facts=[fact("20. Powers to Authorised Dealers: Authorised Dealers shall handle transactions related to the export and "
              "import of goods and services, as well as merchanting trade, undertaken prior to October 01, 2026, which "
              "hitherto required approval of the Reserve Bank of India", N_FEMA)])

short, rate, ndays = 50_00_00_000, 8.75, 1
pen = short * rate / 100 * ndays / 365
assert round(pen) == 119863
Q("010", T, RD, "Advanced",
  "A bank's CRR falls short by ₹50 crore for one day in November 2026, and the shortfall attracts penal interest at "
  "Bank Rate plus 3 percentage points. With the Bank Rate as revised on 7 October 2026, what is the penal interest for "
  "that day (365-day basis, approx.)?",
  ["₹1.20 lakh (at 8.75%)", "₹1.16 lakh (at 8.50%)", "₹1.47 lakh (at 10.75%)", "₹0.79 lakh (at 5.75%)"],
  concept="Penal interest on reserve shortfall",
  explanation="Bank Rate = 5.75%, so the penal rate is 8.75%. Interest = ₹50 crore × 8.75% × 1/365 ≈ ₹1,19,863, i.e. "
              "about ₹1.20 lakh.",
  steps=["Rate = 5.75 + 3 = 8.75%", "50,00,00,000 × 0.0875 / 365 ≈ 1,19,863"],
  why="8.50% is the pre-hike rate; 10.75% is the higher (Bank Rate + 5) rate for prolonged shortfalls; 5.75% is the "
      "Bank Rate itself.",
  computed=True, current=ca("2026-10-07"),
  facts=[fact("the Bank Rate is revised upwards by 25 basis points from 5.50 per cent to 5.75 per cent ... Bank Rate plus "
              "3.0 percentage points (8.75 per cent) or Bank Rate plus 5.0 percentage points (10.75 per cent)",
              N_PENAL)])
assert round(short * 0.085 / 365 / 1000) == 116 and round(short * 0.1075 / 365 / 1000) == 147 \
    and round(short * 0.0575 / 365 / 1000) == 79
Q("010", T, RD, "Advanced",
  "By a circular of 2 September 2026 on Rupee accounts of non-resident banks, RBI dispensed with certain reporting by "
  "AD Category-I banks. Consider:\n"
  "I. Furnishing an annual list of offices maintaining Rupee accounts of non-resident banks, by 15 January.\n"
  "II. Reporting temporary overdrawals by overseas branches/correspondents beyond permissible limits that are not "
  "adjusted within five days.\n"
  "III. Maintaining Rupee accounts of non-resident banks at all.\n"
  "Which of the above were dispensed with?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="FEMA reporting rationalisation",
  explanation="RBI dispensed, with immediate effect, with the two reporting requirements in the 2003 circular: the "
              "annual list of offices maintaining such accounts (due before 15 January) and reports of temporary "
              "overdrawals not adjusted within five days. Banks may continue to maintain these Rupee accounts; only the "
              "reporting was removed.",
  steps=["I ✓ dispensed", "II ✓ dispensed", "III ✗ accounts continue"],
  why="Any option with III is wrong: the accounts themselves were not abolished.",
  current=ca("2026-09-02"),
  facts=[fact("Furnish an up-to-date list of all its offices/branches maintaining Rupee accounts of non-resident banks, as "
              "at the end of December each year before 15th January of the following year ... and Report temporary "
              "overdrawals by overseas branches/ correspondents over permissible limit, if not adjusted within five days "
              "... it has been decided to dispense with the above reporting requirements with immediate effect",
              "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13693&Mode=0")])

# ============================================================================================ Payment Banks
T = "Payment Banks"
PA, DL = "Permitted activities", "Deposit limit"
PB_MISC = "https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13087"   # PB Miscellaneous Directions, 2025 (upd 1 Oct 2026)
PB_DIG = "https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13101"    # PB Digital Banking Channels Authorisation Directions
P_PAYTM = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63751"

Q("008", T, PA, "Basic",
  "In October 2026 RBI announced that Paytm Payments Bank Limited had been excluded from which schedule?",
  ["The Second Schedule to the Reserve Bank of India Act, 1934", "The Third Schedule to the Banking Regulation Act, "
   "1949", "The First Schedule to the SEBI Act, 1992", "The Schedule to the Payment and Settlement Systems Act, 2007"],
  concept="Scheduled banks",
  explanation="Banks included in the Second Schedule to the RBI Act, 1934 are 'scheduled banks'. Paytm Payments Bank was "
              "excluded from it by a notification dated 31 July 2026, published in the Gazette on 7 September 2026; RBI "
              "announced this on 7 October 2026.",
  steps=["Scheduled status ↔ Second Schedule, RBI Act 1934 → Paytm PB excluded"],
  why="Scheduled bank status comes only from the Second Schedule to the RBI Act.",
  current=ca("2026-10-07"),
  facts=[fact("Paytm Payments Bank Limited has been excluded from the Second Schedule to the Reserve Bank of India Act, "
              "1934 vide Notification DoR.LIC.No.S3674/16.13.215/2026-27 dated July 31, 2026 and published in the Gazette "
              "of India (Part III - Section 4) dated September 07, 2026", P_PAYTM)])
Q("008", T, PA, "Intermediate",
  "Under RBI's Payments Banks – Digital Banking Channels Authorisation Directions, 2025, how does a payments bank start "
  "a 'view only' internet or mobile banking facility, compared with a 'transactional' facility?",
  ["View-only: with Board approval, intimating RBI within 30 days with a GAICA report; transactional: only with RBI's "
   "prior approval", "Both need RBI's prior approval", "Neither needs any approval or intimation",
   "View-only needs RBI's prior approval; transactional needs only Board approval"],
  concept="Digital banking channels",
  explanation="Banks with CBS and IPv6-enabled public-facing IT may offer view-only facilities, intimating RBI's "
              "Department of Regulation through PRAVAAH within thirty days of the Board-approved decision, along with a "
              "Gap Assessment and Internal Controls Adequacy (GAICA) report. A transactional facility needs RBI's prior "
              "approval.",
  steps=["View only → intimation (30 days, GAICA)", "Transactional → prior approval"],
  why="The two facilities are treated differently; the last option reverses them.",
  facts=[fact("The banks commencing view only digital banking channel(s) ... shall intimate the Department of Regulation, "
              "Reserve Bank of India (through the PRAVAAH portal) along with a copy of the 'Gap Assessment and Internal "
              "Controls Adequacy' (GAICA) report ... within thirty days from the decision to launch the facility with the "
              "approval of bank board", PB_DIG),
         fact("Banks shall require prior approval of the Reserve Bank for launching transactional banking facility",
              PB_DIG)])

Q("009", T, DL, "Basic",
  "Which kinds of deposits may a payments bank accept under RBI's Payments Banks – Miscellaneous Directions, 2025?",
  ["Only demand deposits, i.e. current and savings deposits", "Savings, current and fixed deposits up to ₹2 lakh",
   "Only fixed deposits of up to one year", "Recurring deposits only"],
  concept="Deposit products of payments banks",
  explanation="Payments banks may undertake only restricted activities such as accepting demand deposits — current and "
              "savings bank deposits. They cannot accept term deposits, and the ₹2 lakh end-of-day cap per individual "
              "applies.",
  steps=["PB deposits = current + savings only"],
  why="Fixed and recurring deposits are term deposits, which payments banks cannot accept.",
  facts=[fact("PBs may undertake only certain restricted activities such as acceptance of demand deposits, i.e., current "
              "deposits, and savings bank deposits", PB_MISC)])
Q("009", T, PA, "Basic",
  "A payments bank offers 'view only' mobile banking. Which service can it provide through it?",
  ["Balance enquiry and account statement download", "Funds transfer to another bank", "Applying for and receiving "
   "a loan", "Bill payments from the account"],
  concept="View only banking facility",
  explanation="A view-only facility offers only services that do not alter the customer's assets or liabilities, such as "
              "balance enquiry, balance viewing and statement download. Fund transfers and other facilities that move "
              "funds or create liability need a transactional facility.",
  steps=["View only = no change in assets/liabilities"],
  why="Fund transfers, loans and bill payments move funds or create liabilities.",
  facts=[fact("View Only Banking Facility – A feature of digital banking channels which only allows banking services that "
              "do not alter the asset or liability of the customer viz. balance enquiry, balance viewing, account "
              "statement download, etc. ... Loans, funds transfers, and other such facilities ... cannot be provided by "
              "banks having view only facility", PB_DIG)])
Q("009", T, PA, "Intermediate",
  "Which of the following is NOT among the eligibility criteria for a payments bank to get RBI's approval for a "
  "transactional internet/mobile banking facility?",
  ["A minimum of five years of profitable operations", "Core Banking Solution and IPv6-enabled public-facing IT "
   "infrastructure", "Compliance with the minimum regulatory CRAR", "A GAICA report certified by a CERT-In empanelled "
   "auditor"],
  concept="Transactional digital banking",
  explanation="The criteria include CBS and IPv6 readiness, compliance with minimum CRAR, minimum capital/net worth as per "
              "licensing norms, adequate financial and technical capability, and a satisfactory compliance record shown "
              "by a GAICA report certified by CERT-In empanelled auditors. A five-year profit record is not a criterion.",
  steps=["CBS + IPv6; CRAR; net worth; capability; GAICA (CERT-In auditor)"],
  why="The other three are listed criteria.",
  facts=[fact("Implementation of CBS and public facing IT infrastructure being enabled to handle IPv6 traffic. Compliance "
              "with minimum regulatory CRAR requirement. Minimum paid up capital/Net worth as per the applicable licensing "
              "requirement ... A GAICA Report ... certified by (third party) CERT-In empaneled auditor(s)", PB_DIG)])

Q("009", T, PA, "Advanced",
  "A company has fund-based and non-fund-based facilities of ₹12 crore from the banking system and wants a current "
  "account with a payments bank. Under the current account rules in RBI's Payments Banks – Miscellaneous Directions, "
  "2025 (as updated), what can the payments bank offer?",
  ["Only a collection account, whose credits must be remitted within two working days to the designated cash credit, "
   "overdraft or current account", "A normal current account without restriction",
   "Nothing, as payments banks cannot open current accounts", "A current account, provided the balance stays below ₹2 lakh"],
  concept="Current accounts and collection accounts",
  explanation="A bank may maintain a current account without restriction only where the banking system's aggregate "
              "exposure to the customer is below ₹10 crore. At ₹10 crore or more, only a collection account is allowed; "
              "funds credited must be remitted within two working days to the designated CC/OD/current account (after "
              "statutory dues and dues to the bank). ₹12 crore ≥ ₹10 crore, so only a collection account.",
  steps=["Exposure 12 ≥ 10 crore → collection account only", "Remit credits within 2 working days"],
  why="₹12 crore exceeds the threshold; payments banks can open current accounts; the ₹2 lakh cap concerns individuals.",
  computed=True,
  facts=[fact("A bank may maintain current account without any restriction in case of customers where the aggregate "
              "exposure of the banking system to the customer is less than ₹10 crore ... A bank may maintain only "
              "collection accounts in case of customers to whom the exposure of the banking system is ₹10 crore or more",
              PB_MISC),
         fact("Funds credited into a collection account shall be remitted within two working days of receipt of such funds "
              "to a Cash Credit Account (CC), current account, or Overdraft Account (OD) ... designated by the borrower",
              PB_MISC)])
assert 12 >= 10

import datetime as _dt3
obs = _dt3.date(2026, 11, 10)
notify_by = _dt3.date(2026, 12, 10)
done_by = _dt3.date(2027, 2, 10)
assert notify_by.month == obs.month + 1 and done_by.month == 2
Q("009", T, PA, "Advanced",
  "On 10 November 2026 a payments bank finds that the banking system's exposure to a customer holding an ordinary current "
  "account with it has risen to ₹10.5 crore. Under RBI's Payments Banks – Miscellaneous Directions, 2025, what must it "
  "do?",
  ["Notify the customer by 10 December 2026 that the account must be converted to a collection account or closed, and "
   "complete this by 10 February 2027", "Close the account the same day", "Nothing until the next half-yearly review",
   "Convert the account into a savings account within a week"],
  concept="Compliance monitoring of current accounts",
  explanation="Banks must monitor accounts at least once every half-year. When a customer becomes ineligible because "
              "exposure has reached ₹10 crore, the bank must notify the customer promptly and within one month that the "
              "account must be converted to a collection account or closed, and complete the conversion or closure within "
              "three months of observing the ineligibility.",
  steps=["Observed 10-11-2026", "Notify ≤ 1 month → by 10-12-2026", "Convert/close ≤ 3 months → by 10-2-2027"],
  why="Immediate closure is not required; waiting for the review or converting to savings is not the rule.",
  computed=True,
  facts=[fact("the bank shall notify the customer(s) concerned promptly, and in any case within one month from the date of "
              "observing such ineligibility, that the account must either be converted to a collection account or "
              "closed. The conversion or closure process ... shall be completed within three months of observing such "
              "ineligibility", PB_MISC),
         fact("all banks shall monitor accounts maintained with them on a regular basis, and in any case at least once "
              "every half-year", PB_MISC)])

Q("010", T, PA, "Basic",
  "From when did RBI's Payments Banks – Digital Banking Channels Authorisation Directions, 2025 come into effect?",
  ["1 January 2026", "28 November 2025", "1 April 2026", "1 October 2026"],
  concept="Digital banking directions for payments banks",
  explanation="The Directions, issued on 28 November 2025 as part of RBI's consolidation, came into effect on 1 January "
              "2026. They govern internet and mobile banking (view-only and transactional) by payments banks.",
  steps=["Issued 28-11-2025; effective 1-1-2026"],
  why="28 November 2025 is the issue date; the other dates are not the effective date.",
  facts=[fact("These Directions shall come into effect from January 01, 2026. The provisions of these Directions shall be "
              "applicable to Payments Banks", PB_DIG)])
Q("010", T, PA, "Intermediate",
  "For applying the ₹10 crore exposure threshold in RBI's current account rules (as in the Payments Banks – "
  "Miscellaneous Directions), which lenders make up the 'banking system'?",
  ["Commercial banks (including SFBs, LABs and RRBs, but excluding payments banks), urban co-operative banks and rural "
   "co-operative banks", "All banks including payments banks, and all NBFCs",
   "Only scheduled commercial banks", "Banks and AIFIs only"],
  concept="Definition of banking system exposure",
  explanation="'Banking System' covers commercial banks (including SFBs, LABs and RRBs but excluding payments banks), "
              "urban co-operative banks and rural co-operative banks (state and central co-operative banks). Payments "
              "banks are excluded because they do not lend.",
  steps=["Include: commercial banks (SFB, LAB, RRB), UCBs, StCBs/CCBs", "Exclude: payments banks, NBFCs"],
  why="NBFCs and AIFIs are outside the definition; payments banks are expressly excluded; co-operative banks are "
      "included.",
  facts=[fact("'Banking System' for the purpose of this Chapter shall include Commercial Banks (including Small Finance "
              "Banks, Local Area Banks, and Regional Rural Banks, but excluding Payments Banks), Urban Co-operative Banks "
              "and Rural Co-operative Banks (State Co-operative Banks and Central Co-operative Banks)", PB_MISC)])
Q("010", T, PA, "Intermediate",
  "Which of the following accounts is exempt from the 'collection account only' restriction for customers with banking "
  "system exposure of ₹10 crore or more?",
  ["An account opened as required under FEMA", "Any account of a listed company", "An account with a balance below ₹2 "
   "lakh", "An account opened before 2020"],
  concept="Exemptions from current account restrictions",
  explanation="Exempt accounts include accounts under FEMA, accounts or transactions stipulated by a statute or by a "
              "financial sector regulator or government, and accounts of regulated entities used for their regulated "
              "activities. Listing, a small balance or account age do not exempt an account.",
  steps=["Exempt: FEMA accounts; statute/regulator-mandated; REs' regulated-activity accounts"],
  why="The other conditions are not exemptions.",
  facts=[fact("The restrictions placed in terms of paragraph 55C ... shall not be applicable to the accounts mentioned "
              "below: (1) Accounts opened as per the provisions of Foreign Exchange Management Act, 1999 (FEMA) ... (2) "
              "Specific accounts or transactions which are stipulated under a statute or a specific instruction of a "
              "financial sector regulator ... (3) Accounts of entities regulated by a financial sector regulator, used "
              "for the purpose of carrying out their regulated activities", PB_MISC)])

cr, tax, due = 50, 2, 3
remit = cr - tax - due
assert remit == 45
Q("010", T, PA, "Advanced",
  "A collection account of a large borrower with a payments bank receives ₹50 lakh on a Monday. ₹2 lakh of TDS/taxes "
  "and ₹3 lakh of charges due to the payments bank are payable from it. Under RBI's rules, what must the payments bank "
  "do?",
  ["Debit the ₹5 lakh of statutory and own dues and remit ₹45 lakh to the designated account within two working days",
   "Remit the full ₹50 lakh at once and recover dues separately", "Hold the ₹50 lakh until month-end",
   "Remit ₹45 lakh within seven working days"],
  concept="Operation of collection accounts",
  explanation="Funds credited to a collection account must be remitted within two working days to the designated "
              "CC/OD/current account. Statutory dues such as taxes, and dues to the bank maintaining the account, may be "
              "debited first: 50 − 2 − 3 = ₹45 lakh.",
  steps=["Allowed debits: 2 + 3 = 5", "Remit 45 within 2 working days"],
  why="The permitted debits need not be recovered separately; holding funds or a seven-day window breaks the rule.",
  computed=True,
  facts=[fact("Funds credited into a collection account shall be remitted within two working days of receipt of such funds "
              "to a Cash Credit Account (CC), current account, or Overdraft Account (OD) ... Provided that statutory dues "
              "such as taxes, and dues, if any, to the bank maintaining the collection account may be debited before "
              "remitting the funds", PB_MISC)])


# ============================================================================================ Small Finance Banks
T = "Small Finance Banks"
LN, PS = "Licensing norms", "PSL targets"
SFB25 = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13135"   # SFB Licensing Guidelines, 2025

Q("008", T, LN, "Basic",
  "What must a small finance bank include in its name under the RBI (Small Finance Banks – Licensing) Guidelines, 2025?",
  ["The words 'Small Finance Bank'", "The word 'Limited' only", "The name of its promoter group",
   "The words 'Payments Bank'"],
  concept="Name of an SFB",
  explanation="An SFB must use the words 'Small Finance Bank' in its name to distinguish it from other banks.",
  steps=["Name must contain 'Small Finance Bank'"],
  why="The other options are not the requirement.",
  facts=[fact("The small finance bank will be required to use the words “Small Finance Bank” in its name in "
              "order to differentiate it from other banks", SFB25)])
Q("008", T, LN, "Basic",
  "According to RBI's Small Finance Banks – Licensing Guidelines, 2025, small finance banks are set up to further "
  "financial inclusion mainly through:",
  ["Savings vehicles for unserved and underserved people, and credit to small businesses, small and marginal farmers, "
   "micro and small industries and the unorganised sector, through high technology–low cost operations",
   "Large-ticket corporate lending and investment banking",
   "Payments and remittances only, without any lending",
   "Financing of infrastructure projects through long-term bonds"],
  concept="Objectives of SFBs",
  explanation="SFBs aim at (i) savings vehicles primarily for unserved and underserved sections and (ii) credit to small "
              "business units, small and marginal farmers, micro and small industries and other unorganised entities, "
              "through high technology–low cost operations.",
  steps=["Savings for underserved + small-ticket credit, low-cost technology"],
  why="Corporate/infrastructure finance is not their objective; payments-only is the payments bank model.",
  facts=[fact("The objectives of setting up of small finance banks will be for furthering financial inclusion by (i) "
              "provision of savings vehicles primarily to unserved and underserved sections of the population, and (ii) "
              "supply of credit to small business units; small and marginal farmers; micro and small industries; and "
              "other unorganised sector entities, through high technology-low cost operations", SFB25)])
Q("008", T, PS, "Intermediate",
  "A newly licensed small finance bank commences business in October. Under the SFB Licensing Guidelines, 2025, how is "
  "its first priority sector target set?",
  ["On its first audited balance sheet as on 31 March, applying to the following year; it cannot sell PSL Certificates "
   "in the intervening period", "On its opening balance sheet, applying from day one",
   "At 40% of ANBC for the first three years", "It has no PSL target for the first five years"],
  concept="First PSL target of an SFB",
  explanation="The first audited balance sheet as on 31 March after commencement forms the basis of the first PSL target, "
              "for the subsequent financial year. In the intervening period (commencement to that 31 March) the SFB is "
              "not allowed to sell PSLCs.",
  steps=["Basis: first audited 31 March balance sheet", "Target applies next FY", "No PSLC sale in between"],
  why="There is no day-one target, no 40% transitional rate and no five-year holiday.",
  facts=[fact("The first audited balance sheet as on March 31st, post commencement of operations of the small finance bank, "
              "would form the basis for the first PSL target for the bank (for the subsequent financial year). During the "
              "'intervening period' ... the small finance banks are not allowed to sell Priority Sector Lending "
              "Certificates", SFB25)])
Q("008", T, LN, "Intermediate",
  "What capital adequacy requirement applies to small finance banks under the SFB Licensing Guidelines, 2025?",
  ["CRAR of at least 15% on a continuous basis, Tier I at least 7.5% of RWAs, and Tier II capped at 100% of Tier I",
   "CRAR of 9%, as for other commercial banks", "CRAR of 12%, with no separate Tier I floor",
   "CRAR of 15%, with Tier II capped at 50% of Tier I"],
  concept="Capital adequacy of SFBs",
  explanation="SFBs must maintain minimum CRAR of 15% of RWAs continuously; Tier I capital must be at least 7.5% of "
              "RWAs; Tier II is limited to 100% of Tier I.",
  steps=["CRAR ≥ 15%", "Tier I ≥ 7.5%", "Tier II ≤ Tier I"],
  why="9% and 12% are not the SFB requirement; the Tier II cap is 100% of Tier I, not 50%.",
  facts=[fact("The small finance bank shall be required to maintain a minimum capital adequacy ratio of 15 per cent of its "
              "risk weighted assets (RWA) on a continuous basis ... Tier I capital should be at least 7.5 per cent of "
              "RWAs. Tier II capital should be limited to a maximum of 100 per cent of total Tier I capital", SFB25)])

rwa, t1, t2 = 8000, 560, 700
t2e = min(t2, t1)
crar = 100 * (t1 + t2e) / rwa
assert t2e == 560 and crar == 14 and 100 * t1 / rwa == 7
Q("008", T, LN, "Advanced",
  "A small finance bank has risk-weighted assets of ₹8,000 crore, Tier I capital of ₹560 crore and Tier II capital of "
  "₹700 crore. Applying the SFB capital norms, which statement is correct?",
  ["Eligible Tier II is capped at ₹560 crore, so CRAR is 14% and Tier I is 7%; both requirements are breached",
   "CRAR is 15.75%, so the bank complies", "CRAR is 15.75% but Tier I at 7% is short",
   "CRAR is 14% but Tier I at 7% meets the 7% floor"],
  concept="Applying Tier I/Tier II limits",
  explanation="Tier II counts only up to 100% of Tier I: min(700, 560) = 560. CRAR = (560 + 560) ÷ 8,000 = 14% < 15%. "
              "Tier I ratio = 560 ÷ 8,000 = 7% < 7.5%. Both are breached.",
  steps=["Eligible T2 = 560", "CRAR = 1,120/8,000 = 14%", "T1 = 7% < 7.5%"],
  why="15.75% ignores the Tier II cap; the Tier I floor is 7.5%, not 7%.",
  computed=True,
  facts=[fact("minimum capital adequacy ratio of 15 per cent ... Tier I capital should be at least 7.5 per cent of RWAs. "
              "Tier II capital should be limited to a maximum of 100 per cent of total Tier I capital", SFB25)])
assert 100 * (560 + 700) / 8000 == 15.75
Q("008", T, LN, "Advanced",
  "An NBFC that has secured borrowings backed by a floating charge on its assets converts into a small finance bank. "
  "Consider:\n"
  "I. SFBs are precluded from creating floating charges on their assets.\n"
  "II. The existing floating-charge borrowings may be grandfathered till maturity.\n"
  "III. The assets under such a charge carry no extra risk weight.\n"
  "Which of the above is/are correct under the SFB Licensing Guidelines, 2025?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Floating charges on conversion",
  explanation="SFBs cannot create floating charges. For a converting NBFC/MFI, such borrowings on the balance sheet on "
              "conversion day are grandfathered till maturity, but an additional 25% risk weight is imposed on the "
              "assets on which the charge/lien was created. So III is wrong.",
  steps=["I ✓", "II ✓", "III ✗ (+25% risk weight)"],
  why="Any option with III is wrong.",
  facts=[fact("SFBs are precluded from creating floating charge on their assets. For such NBFCs / MFIs ... if they have "
              "created floating charges on their assets for secured borrowings ... RBI will permit grandfathering of such "
              "borrowings till their maturity. An additional risk weight of 25 per cent will be imposed on the assets on "
              "which charge / lien has been created by the converting entity", SFB25)])

Q("009", T, LN, "Basic",
  "Under the SFB Licensing Guidelines, 2025, proposals from which of the following will NOT be entertained for setting up "
  "a small finance bank?",
  ["Alternative Investment Funds (AIFs)", "Resident professionals with 10 years' senior experience in banking and "
   "finance", "Resident-controlled NBFCs with a five-year track record", "Resident-controlled microfinance institutions "
   "with a five-year track record"],
  concept="Ineligible promoters",
  explanation="Proposals from AIFs will not be entertained, nor from government-owned entities, large industrial houses, "
              "state financial corporations and some others. Resident professionals, NBFCs and MFIs meeting the "
              "criteria are eligible.",
  steps=["AIFs → not entertained"],
  why="The other three are eligible categories.",
  facts=[fact("The proposals from Alternative Investment Funds (AIFs) will also not be entertained", SFB25)])
Q("009", T, LN, "Intermediate",
  "Which statement on voting rights and share acquisition applies to small finance banks under the SFB Licensing "
  "Guidelines, 2025?",
  ["A shareholder's voting rights are capped at 26%, and acquiring 5% or more needs RBI's prior approval",
   "Voting rights are capped at 10%, and acquiring 1% needs RBI's approval",
   "There is no cap on voting rights for SFBs", "Acquisition of up to 25% needs no approval"],
  concept="Voting rights in private banks and SFBs",
  explanation="Under Section 12(2) of the BR Act read with RBI's 2016 notification, any shareholder's voting rights in a "
              "private sector bank are capped at 26%, and under Section 12B acquiring 5% or more of paid-up capital or "
              "voting rights needs RBI's prior approval. Both apply to SFBs.",
  steps=["Voting cap 26%", "≥ 5% acquisition → RBI approval"],
  why="The other caps and thresholds are not those in the BR Act.",
  facts=[fact("any shareholder's voting rights in private sector banks are currently capped at 26 per cent ... any "
              "acquisition of 5 per cent or more of paid-up share capital in a private sector bank or voting rights "
              "therein will require prior approval of RBI. These provisions will apply to the small finance banks also",
              SFB25)])

Q("010", T, LN, "Basic",
  "Under the SFB Licensing Guidelines, 2025, can different promoter groups form a joint venture to set up a small "
  "finance bank?",
  ["No, joint ventures by different promoter groups are not permitted", "Yes, if each holds at least 26%",
   "Yes, with RBI's prior approval", "Yes, but only between NBFCs"],
  concept="Eligible promoters",
  explanation="Individuals/professionals may apply singly or jointly, but joint ventures by different promoter groups "
              "for setting up SFBs are not permitted.",
  steps=["JV of promoter groups → not allowed"],
  why="No exception exists for JVs.",
  facts=[fact("However, joint ventures by different promoter groups for the purpose of setting up small finance banks "
              "would not be permitted", SFB25)])
Q("010", T, LN, "Basic",
  "An SFB must open at least 25% of its banking outlets in unbanked rural centres within a year. How is an 'unbanked "
  "rural centre' defined by population in the SFB Licensing Guidelines, 2025?",
  ["Population up to 9,999 as per the latest census", "Population up to 4,999", "Population up to 49,999",
   "Population up to 99,999"],
  concept="Rural centres",
  explanation="Rural centres are those with population up to 9,999 as per the latest census; 10,000–49,999 is "
              "semi-urban.",
  steps=["Rural = population ≤ 9,999"],
  why="The other cut-offs do not define rural centres.",
  facts=[fact("it is required to open at least 25 per cent of its banking outlets in unbanked rural centres (population "
              "upto 9,999 as per the latest census) within one year from the date of commencement of operations",
              SFB25)])
Q("010", T, LN, "Intermediate",
  "Promoters want to hold their small finance bank through an intermediate company. Under the SFB Licensing Guidelines, "
  "2025, what must that structure be?",
  ["An intermediate company must be a Non-Operative Financial Holding Company (NOFHC); a holding company without an "
   "NOFHC must be registered as an NBFC-CIC", "Any private company may act as the holding company",
   "The holding company must be listed within three years", "The SFB itself must hold the promoters' other businesses as "
   "subsidiaries"],
  concept="Corporate structure of SFBs",
  explanation="The SFB may be standalone or under a holding company. An intermediate company between the bank and its "
              "promoting entity must be an NOFHC; if a holding company structure without an NOFHC is chosen, the holding "
              "company must be registered with RBI as an NBFC-CIC. SFBs cannot set up subsidiaries.",
  steps=["Intermediate → NOFHC", "Holding co. without NOFHC → NBFC-CIC"],
  why="Any company will not do; listing of the holding company is not required; SFBs cannot have subsidiaries.",
  facts=[fact("if there is an intermediate company between the small finance bank and its promoting entity, it should be a "
              "Non-Operative Financial Holding Company (NOFHC). If the promoters desire to set up the small finance bank "
              "under a holding company structure, without an NOFHC, the holding company / the promoting entity shall be "
              "registered as an NBFC–CIC with the Reserve Bank", SFB25)])

loans = {"A": [12, 8], "B": [30], "C": [20], "D": [10, 10, 10], "E": [24]}
small = sum(sum(v) for v in loans.values() if sum(v) <= 25)
total = sum(sum(v) for v in loans.values())
assert total == 124 and small == 64 and round(100 * small / total, 1) == 51.6
Q("010", T, LN, "Advanced",
  "A small finance bank's loan book (₹ lakh) has five borrowers: A – two loans of 12 and 8; B – one loan of 30; C – one "
  "loan of 20; D – three loans of 10 each; E – one loan of 24. At least 50% of the portfolio must be loans of up to ₹25 "
  "lakh, applied borrower-wise. What is the position?",
  ["Borrowers A, C and E qualify (₹64 lakh of ₹124 lakh, about 51.6%), so the norm is met",
   "All loans except B's qualify (₹94 lakh, about 75.8%)", "Only C and E qualify (₹44 lakh, about 35.5%), so it fails",
   "Every loan is below ₹25 lakh except B's, so the share is 100% less B"],
  concept="₹25 lakh norm, borrower-wise",
  explanation="The ₹25 lakh limit is borrower-wise, and the whole portfolio counts. Borrower totals: A 20, B 30, C 20, "
              "D 30, E 24. Qualifying: A, C, E = 64 of 124 ≈ 51.6% ≥ 50%. D's three loans of 10 each total 30 and do "
              "not qualify.",
  steps=["Totals: A 20, B 30, C 20, D 30, E 24", "≤ 25: A, C, E = 64", "64/124 ≈ 51.6%"],
  why="Counting D loan-by-loan ignores the borrower-wise rule; excluding A also misapplies it.",
  computed=True,
  facts=[fact("at least 50 per cent of its loan portfolio should constitute loans and advances of up to ₹ 25 lakh on an "
              "ongoing basis ... the entire loan portfolio of the bank ... would be considered ... Further, the criteria "
              "of upper limit of ₹ 25 lakh shall be borrower wise", SFB25)])
assert round(100 * 94 / 124, 1) == 75.8 and round(100 * 44 / 124, 1) == 35.5
Q("010", T, LN, "Advanced",
  "Consider the following about the ring-fencing of a promoter's other businesses under the SFB Licensing Guidelines, "
  "2025:\n"
  "I. The promoter's other financial and non-financial activities must be kept distinctly ring-fenced from the banking "
  "business.\n"
  "II. Sharing infrastructure of the promoter group is allowed under an agreement on an arm's length basis, with "
  "firewalls, customer confidentiality and risk mitigation.\n"
  "III. Entities under an NOFHC may undertake activities that the SFB itself is not permitted to do.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Ring-fencing and group activities",
  explanation="I and II are correct: other businesses must be ring-fenced, but infrastructure may be shared at arm's "
              "length with firewalls. III is wrong: activities not permitted to the bank are not permitted to the group "
              "entities under the NOFHC either.",
  steps=["I ✓", "II ✓", "III ✗"],
  why="Any option with III is wrong.",
  facts=[fact("The other financial and non-financial services activities of the promoters, if any, should be kept distinctly "
              "ring-fenced and not comingled with the banking business. Explanation: Ring fencing does not restrict "
              "arrangements for sharing of infrastructure ... if such arrangement is entered into on an arm's length "
              "basis, suitable firewalls are built in, customer confidentiality maintained", SFB25),
         fact("the activities not permitted to the bank would also not be permitted to the group i.e. entities under the "
              "NOFHC would not be permitted to engage in activities that the bank is not permitted to engage in", SFB25)])

# ============================================================================================ Financial Markets
T = "Financial Markets"
SR = "Structure and regulators"
_PR = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid={}"
P_OMO, P_OMOR, P_SWITCH, P_FRB, P_SGB = (_PR.format(63779), _PR.format(63796), _PR.format(63806), _PR.format(63883),
                                         _PR.format(63897))
P_AA = _PR.format(63743)

Q("008", T, SR, "Basic",
  "Which of the following is listed as an All India Financial Institution (AIFI) in RBI's Commercial Paper and NCD "
  "Directions, 2024?",
  ["National Bank for Financing Infrastructure and Development (NaBFID)", "Life Insurance Corporation of India",
   "Power Finance Corporation", "Housing and Urban Development Corporation"],
  concept="All India Financial Institutions",
  explanation="The Directions define AIFIs as EXIM Bank, NABARD, National Housing Bank, SIDBI and NaBFID. LIC is an "
              "insurer, and PFC and HUDCO are NBFCs.",
  steps=["AIFIs: EXIM, NABARD, NHB, SIDBI, NaBFID"],
  why="LIC, PFC and HUDCO are not AIFIs.",
  facts=[fact("All India Financial Institution (AIFI) shall include: (a) Export Import Bank of India, (b) National Bank for "
              "Agriculture and Rural Development, (c) National Housing Bank, (d) Small Industries Development Bank of "
              "India and (e) National Bank for Financing Infrastructure and Development", RBI_CP)])
Q("008", T, SR, "Basic",
  "On 9 October 2026, after reviewing liquidity conditions, RBI announced an OMO sale of government securities worth "
  "₹25,000 crore. What is the effect of an OMO sale on banking system liquidity?",
  ["It absorbs liquidity, as buyers pay RBI for the securities", "It injects liquidity, as RBI pays the buyers",
   "It has no effect, as it only changes ownership among banks", "It raises the CRR automatically"],
  concept="Open market operations",
  explanation="In an OMO sale RBI sells G-secs; buyers pay from their accounts, so reserves move to RBI and liquidity is "
              "absorbed. The 13 October 2026 auction offered six securities (2030–2034 maturities) through a "
              "multi-security, multiple-price auction.",
  steps=["OMO sale → funds flow to RBI → liquidity absorbed"],
  why="OMO purchases inject liquidity; a sale is not neutral; CRR is set separately.",
  current=ca("2026-10-09"),
  facts=[fact("On a review of current and evolving liquidity conditions, the Reserve Bank has decided to conduct an OMO "
              "sale auction of Government of India securities for an aggregate amount of ₹25,000 crore on October 13, "
              "2026, through multi-security auction using the multiple price method", P_OMO)])
Q("008", T, SR, "Intermediate",
  "On 19 October 2026 the Government ran a switch auction of ₹20,000 crore, exchanging securities maturing in 2027–2029 "
  "for securities maturing between 2033 and 2060. What is the main purpose of such a switch?",
  ["To ease near-term redemption pressure by lengthening the maturity profile of debt", "To raise fresh borrowing of "
   "₹20,000 crore", "To inject liquidity into the banking system", "To convert dated securities into Treasury Bills"],
  concept="Conversion/switch of G-secs",
  explanation="A switch exchanges existing (source) securities for other (destination) securities without fresh "
              "borrowing. Replacing 2027–2029 papers with 2033–2060 papers spreads redemptions and lengthens the debt's "
              "maturity, reducing rollover risk.",
  steps=["Source: short-dated → destination: long-dated", "No fresh money; maturity profile lengthened"],
  why="A switch raises no fresh money, is not a liquidity operation, and does not create T-bills.",
  current=ca("2026-10-14"),
  facts=[fact("Government of India announces the conversion/switch of its securities through auction for an aggregate "
              "amount of ₹20,000 crore (face value) ... Source Securities 8.26% GS 2027 ... 6.79% GS 2029; Destination "
              "Securities 7.19% GS 2060 ... 7.57% GS 2033", P_SWITCH)])

acc = {"7.88% GS 2030": 2820, "6.10% GS 2031": 8430, "7.95% GS 2032": 1600, "7.26% GS 2033": 2735,
       "7.18% GS 2033": 9415}
assert sum(acc.values()) == 25000 and max(acc, key=acc.get) == "7.18% GS 2033"
assert round(100 * 9415 / 25000, 1) == 37.7
Q("008", T, SR, "Advanced",
  "In RBI's OMO sale of 13 October 2026 (aggregate ₹25,000 crore, no security-wise notified amount), RBI accepted ₹2,820 "
  "crore of 7.88% GS 2030, ₹8,430 crore of 6.10% GS 2031, ₹1,600 crore of 7.95% GS 2032, ₹2,735 crore of 7.26% GS 2033, "
  "₹9,415 crore of 7.18% GS 2033 and none of 7.10% GS 2034. Which statement is correct?",
  ["The full ₹25,000 crore was sold, and 7.18% GS 2033 alone made up about 37.7% of it",
   "Only ₹22,000 crore was sold, as one security got no bids accepted",
   "6.10% GS 2031 made up the largest share, about 37.7%",
   "Each security was sold in equal amounts of about ₹4,167 crore"],
  concept="Reading an OMO auction result",
  explanation="2,820 + 8,430 + 1,600 + 2,735 + 9,415 = 25,000, so the full amount was sold. The largest share was 7.18% "
              "GS 2033: 9,415 ÷ 25,000 ≈ 37.7%. Since there was no security-wise notified amount, RBI could sell nothing "
              "of 7.10% GS 2034.",
  steps=["Sum = 25,000", "Largest: 9,415 → 37.7%"],
  why="The total is 25,000, not 22,000; 6.10% GS 2031 (8,430) was second; amounts were unequal.",
  computed=True, current=ca("2026-10-13"),
  facts=[fact("OMO Sale held on Oct 13, 2026: Total amount (Face Value) accepted by RBI (₹ in crore): 7.88% GS 2030 2,820; "
              "6.10% GS 2031 8,430; 7.95% GS 2032 1,600; 7.26% GS 2033 2,735; 7.18% GS 2033 9,415; 7.10% GS 2034 -",
              P_OMOR)])

cpn, spread = 7.26, 0.98
base = round(cpn - spread, 2)
assert base == 6.28
Q("008", T, SR, "Advanced",
  "RBI announced that Floating Rate Bond 2034 will pay 7.26% a year for the half year 30 October 2026 to 29 April 2027. "
  "The coupon equals a base rate plus a fixed spread of 0.98%. What base rate does this imply, and how is it set?",
  ["6.28%: the average of the weighted average yields of the last three 182-day T-bill auctions before the rate-fixing "
   "day", "6.28%: the repo rate on the rate-fixing day", "8.24%: the 10-year G-sec yield plus spread",
   "7.26%: the average 364-day T-bill cut-off yield"],
  concept="Floating Rate Bonds",
  explanation="Base rate = coupon − spread = 7.26 − 0.98 = 6.28%. For FRB 2034 the base is the average of the WAY of the "
              "last three 182-day T-bill auctions from the rate-fixing day, and the coupon resets every half-year.",
  steps=["Base = 7.26 − 0.98 = 6.28%", "Base = avg WAY of last three 182-day T-bill auctions"],
  why="The repo rate, 10-year yield and 364-day bill are not the reference; 8.24% adds instead of subtracts.",
  computed=True, current=ca("2026-10-29"),
  facts=[fact("The rate of interest on Government of India Floating Rate Bond 2034 (FRB 2034) applicable for the half year "
              "October 30, 2026 to April 29, 2027 shall be 7.26 per cent per annum ... base rate equivalent to the "
              "average of the Weighted Average Yield (WAY) of last three auctions ... of 182 Day T-Bills, plus a fixed "
              "spread (0.98 per cent)", P_FRB)])

Q("009", T, SR, "Basic",
  "When may a holder of a Sovereign Gold Bond seek premature redemption?",
  ["After the fifth year from the date of issue, on the dates on which interest is payable", "At any time after one "
   "year", "Only on final maturity after eight years", "After three years, on any business day"],
  concept="Sovereign Gold Bonds",
  explanation="Premature redemption may be permitted after the fifth year from the issue date, on interest payment dates. "
              "For example, SGB 2021-22 Series VII, issued on 2 November 2021, became eligible on 2 November 2026.",
  steps=["Premature redemption: after year 5, on interest dates"],
  why="One year and three years are too early; it need not wait for final maturity.",
  current=ca("2026-10-30"),
  facts=[fact("premature redemption of Gold Bond may be permitted after fifth year from the date of issue of such Gold Bond "
              "on the date on which interest is payable", P_SGB)])
Q("009", T, SR, "Basic",
  "Account Aggregators (AAs), which let customers share financial information between providers with consent, are "
  "registered and regulated in India as:",
  ["NBFCs regulated by RBI (NBFC-AAs)", "Depositories regulated by SEBI", "Insurance intermediaries regulated by IRDAI",
   "Payment system operators regulated by NPCI"],
  concept="Regulatory structure",
  explanation="AAs are a category of RBI-regulated NBFC (NBFC-AA). RBI's October 2026 statement provided for "
              "interoperability among NBFC-AAs and let SEBI-regulated depositories include bank deposit data in their "
              "Consolidated Account Statement through AAs.",
  steps=["AA = NBFC-AA under RBI"],
  why="Depositories are SEBI-regulated but are not AAs; IRDAI and NPCI do not regulate AAs.",
  current=ca("2026-10-07"),
  facts=[fact("it has been decided to implement interoperability among NBFC-Account Aggregators (NBFC-AA) ... Depositories "
              "regulated by the Securities and Exchange Board of India are being facilitated to include information "
              "related to bank deposit accounts in their Consolidated Account Statement (CAS) through the NBFC-AAs",
              P_AA)])
Q("009", T, SR, "Basic",
  "On which RBI platform do eligible participants submit bids in OMO auctions and G-sec switch auctions?",
  ["E-Kuber, RBI's Core Banking Solution", "NDS-OM", "CROMS", "SWIFT"],
  concept="Auction infrastructure",
  explanation="Bids for OMO sale/purchase and switch auctions are submitted electronically on E-Kuber, RBI's Core Banking "
              "Solution; physical bids are accepted only on system failure. NDS-OM is for secondary G-sec trading and "
              "CROMS for repo.",
  steps=["Auctions → E-Kuber"],
  why="NDS-OM and CROMS are trading platforms; SWIFT is a messaging network.",
  current=ca("2026-10-09"),
  facts=[fact("Eligible participants should submit their bids in electronic format on the Reserve Bank of India Core Banking "
              "Solution (E-Kuber) system between 9:30 am and 10:30 am on October 13, 2026", P_OMO)])
Q("009", T, SR, "Intermediate",
  "How is the redemption price of a Sovereign Gold Bond fixed?",
  ["On the simple average of the closing price of 999-purity gold for the previous three business days, as published "
   "by the India Bullion and Jewellers Association (IBJA)", "On RBI's reference rate for gold on the redemption day",
   "On the issue price plus accrued interest", "On the London Bullion Market price converted at the RBI reference rate"],
  concept="SGB redemption price",
  explanation="The redemption price is the simple average of IBJA's closing price of 999 gold for the three business days "
              "before redemption. For the premature redemption due on 2 November 2026 (SGB 2021-22 Series VII), it was "
              "₹14,167 per unit, based on 28–30 October 2026.",
  steps=["Average of IBJA 999 closing price, previous 3 business days"],
  why="RBI reference rates, issue price plus interest and LBMA prices are not used.",
  current=ca("2026-10-30"),
  facts=[fact("the redemption price of SGB shall be based on simple average of closing price of gold of 999 purity of "
              "previous three business days from the date of redemption, as published by the India Bullion and Jewellers "
              "Association Ltd (IBJA)", P_SGB)])
Q("009", T, SR, "Intermediate",
  "RBI's OMO sale of 13 October 2026 and the G-sec switch of 19 October 2026 were both conducted as 'multiple price' "
  "auctions. What does this mean?",
  ["Each successful bid is accepted at its own quoted price", "All successful bids are accepted at a single cut-off "
   "price", "Prices are fixed in advance by RBI", "Only non-competitive bids are accepted"],
  concept="Multiple-price auctions",
  explanation="In a multiple-price auction successful bidders pay (or receive) their own quoted prices. In a uniform-price "
              "auction all successful bids are settled at the single cut-off price.",
  steps=["Multiple price → own quoted price"],
  why="A single cut-off price describes uniform-price auctions; prices are not pre-fixed.",
  current=ca("2026-10-14"),
  facts=[fact("The auction will be a multiple-price based auction, i.e., successful bids will get accepted at their "
              "respective quoted prices for the source and destination securities", P_SWITCH)])

units, price = 40, 14167
assert units * price == 566680
Q("009", T, SR, "Advanced",
  "An investor holds 40 units of SGB 2021-22 Series VII (issued 2 November 2021) and opts for premature redemption on "
  "2 November 2026, when the redemption price is ₹14,167 per unit. Which statement is correct?",
  ["She receives ₹5,66,680; the redemption is allowed as five years from issue have passed and it falls on an interest "
   "date", "She receives ₹5,66,680, but only after final maturity in 2029",
   "She cannot redeem before eight years", "She receives ₹14,167 in all, as the price is per holding"],
  concept="SGB premature redemption",
  explanation="Premature redemption is allowed after the fifth year on interest dates; 2 November 2026 is such a date for "
              "this tranche. Proceeds = 40 × ₹14,167 = ₹5,66,680.",
  steps=["Eligible: 5 years from 2-11-2021", "40 × 14,167 = 5,66,680"],
  why="Payment is on the premature redemption date; eight years is the full tenor; the price is per unit.",
  computed=True, current=ca("2026-10-30"),
  facts=[fact("SGB 2021-22 Series VII - Issue date November 02, 2021 ... the due date of premature redemption of the above "
              "tranche shall be on November 02, 2026 ... the redemption price ... shall be ₹14,167/- per unit of SGB",
              P_SGB)])

src = [2000, 3000, 3000, 4000, 4000, 4000]
assert sum(src) == 20000 and max(src) == 4000
Q("009", T, SR, "Advanced",
  "In the switch auction of 19 October 2026, the source securities were 8.26% GS 2027 (₹2,000 crore), 7.17% GS 2028 "
  "(₹3,000 crore), 7.06% GS 2028 (₹3,000 crore), 7.26% GS 2029, 6.03% GS 2029 and 6.79% GS 2029 (₹4,000 crore each), "
  "and the longest destination was 7.19% GS 2060. Which statement is correct?",
  ["2029 maturities made up ₹12,000 crore, or 60% of the ₹20,000 crore, and the auction raised no fresh cash for the "
   "Government", "2028 maturities made up the largest block, ₹12,000 crore", "The auction raised ₹20,000 crore of "
   "fresh borrowing", "Settlement was on the auction date itself (T+0)"],
  concept="Analysing a switch auction",
  explanation="2029 papers: 3 × 4,000 = ₹12,000 crore = 60% of 20,000; 2028 papers total ₹6,000 crore. A switch exchanges "
              "one security for another, so no fresh money is raised. The auction on 19 October settled on 21 October "
              "2026.",
  steps=["2029: 12,000 (60%)", "2028: 6,000", "No fresh cash; settlement 21-10-2026"],
  why="2028 papers total 6,000; a switch is not fresh borrowing; settlement was two days later.",
  computed=True, current=ca("2026-10-14"),
  facts=[fact("conversion/switch of its securities through auction for an aggregate amount of ₹20,000 crore (face value) "
              "... 8.26% GS 2027 2,000; 7.17% GS 2028 3,000; 7.06% GS 2028 3,000; 7.26% GS 2029 4,000; 6.03% GS 2029 4,000; "
              "6.79% GS 2029 4,000 ... settlement will take place on October 21, 2026", P_SWITCH)])

Q("010", T, SR, "Basic",
  "RBI's current-account rules list four 'financial sector regulators'. Which are they?",
  ["RBI, SEBI, IRDAI and PFRDA", "RBI, SEBI, IRDAI and IBBI", "RBI, SEBI, NABARD and NHB", "RBI, SEBI, IFSCA and "
   "CCI"],
  concept="Financial sector regulators",
  explanation="For these rules, 'financial sector regulator' means the Reserve Bank of India, the Securities and Exchange "
              "Board of India, the Insurance Regulatory and Development Authority of India and the Pension Fund "
              "Regulatory and Development Authority.",
  steps=["RBI + SEBI + IRDAI + PFRDA"],
  why="IBBI, NABARD, NHB, IFSCA and CCI are not in this definition.",
  facts=[fact("'Financial sector regulator' for the purpose of this Chapter refers to the Reserve Bank of India (RBI), the "
              "Securities and Exchange Board of India (SEBI), the Insurance Regulatory and Development Authority of India "
              "(IRDAI) and the Pension Fund Regulatory and Development Authority (PFRDA)", PB_MISC)])
Q("010", T, SR, "Intermediate",
  "Among its measures to leverage TReDS, the Union Budget 2026-27 proposed introducing TReDS receivables as what kind of "
  "instrument, to develop a secondary market?",
  ["Asset-backed securities", "Certificates of Deposit", "Sovereign Green Bonds", "Commercial Paper"],
  concept="Securitisation of trade receivables",
  explanation="The Budget proposed to introduce TReDS receivables as asset-backed securities, helping develop a secondary "
              "market and improve liquidity and settlement, besides linking GeM with TReDS and a CGTMSE guarantee for "
              "invoice discounting.",
  steps=["TReDS receivables → ABS → secondary market"],
  why="CDs, green bonds and CP are different instruments.",
  current=BUD,
  facts=[fact("introduce TReDS receivables as asset-backed securities, helping develop a secondary market, enhancing "
              "liquidity and settlement of transactions", BUDGET)])
Q("010", T, SR, "Intermediate",
  "To recycle real estate assets of Central Public Sector Enterprises, the Union Budget 2026-27 proposed to set up:",
  ["Dedicated Real Estate Investment Trusts (REITs)", "A National Land Bank Corporation", "Infrastructure Debt Funds "
   "under NBFC route", "A sovereign wealth fund for CPSE land"],
  concept="Asset monetisation through REITs",
  explanation="The Budget proposed to accelerate recycling of significant CPSE real estate assets through dedicated REITs.",
  steps=["CPSE real estate → dedicated REITs"],
  why="The other vehicles were not proposed.",
  current=BUD,
  facts=[fact("Government to accelerate recycling of significant real estate assets of CPSEs through the setting up of "
              "dedicated REITs", BUDGET)])

# ============================================================================================ Capital Market
T = "Capital Market"
PS_, SE, IX = "Primary and secondary market", "SEBI", "Indices"
_SD = "https://www.sebi.gov.in/sebi_data/attachdocs/{}.pdf"
S_IGP, S_FPIKYC, S_BOE = _SD.format("nov-2026/1793796577714"), _SD.format("oct-2026/1793361131985"), \
    _SD.format("oct-2026/1793190911537")
S_WA, S_CHD, S_DNVS = _SD.format("oct-2026/1792675550417"), _SD.format("oct-2026/1791211079880"), \
    _SD.format("oct-2026/1790853960291")
S_MUST, S_SPM, S_CAS = _SD.format("oct-2026/1791210984403"), _SD.format("sep-2026/1789649899889"), \
    _SD.format("sep-2026/1788448619635")
S_CYB, S_PROI, S_BRD = _SD.format("sep-2026/1788856724844"), _SD.format("aug-2026/1786716712210"), \
    _SD.format("sep-2026/1790259036651")
S_HBS = _SD.format("aug-2026/1786977098058")
BRD = ca("2026-09-24")

Q("008", T, SE, "Basic",
  "SEBI opened a Local Office in Chandigarh on 5 October 2026. Which areas does it cover?",
  ["Punjab, Haryana and the UT of Chandigarh, under SEBI's Northern Regional Office, New Delhi",
   "Himachal Pradesh and Jammu & Kashmir only", "All of North India, reporting directly to SEBI's head office",
   "Punjab only, under the Western Regional Office"],
  concept="SEBI's regional structure",
  explanation="The Chandigarh Local Office covers Punjab, Haryana and the UT of Chandigarh and works under the Northern "
              "Regional Office at New Delhi. It helps redress investor grievances, spreads investor education and "
              "engages with issuers including SMEs, social stock exchanges and municipal and corporate bonds.",
  steps=["Chandigarh LO → Punjab, Haryana, Chandigarh; under NRO Delhi"],
  why="The other jurisdictions and reporting lines are not those announced.",
  current=ca("2026-10-05"),
  facts=[fact("The Chandigarh Local Office will cover the States of Punjab and Haryana and the Union Territory of "
              "Chandigarh. It will function under the administrative control and jurisdiction of SEBI's Northern Regional "
              "Office at New Delhi", S_CHD)])
Q("008", T, SE, "Intermediate",
  "In its caution of October 2026 about stock tips in invitation-only WhatsApp groups, SEBI described 'astroturfing'. "
  "What is it?",
  ["Members acting with the operators post false profit claims and praise to create a false impression of genuine "
   "support", "Front-running of client orders by brokers", "Splitting large orders to avoid disclosure",
   "Spreading rumours to depress a stock's price"],
  concept="Investor protection",
  explanation="Unregistered operators pose as experts, often from overseas numbers, and share buy/sell calls. Members "
              "acting in concert post false profit claims and praise; this astroturfing creates a false impression of "
              "genuine support. SEBI advised investors to avoid such groups and deal only with registered "
              "intermediaries.",
  steps=["Astroturfing = planted praise/profit claims to fake genuine support"],
  why="The other options describe different market abuses.",
  current=ca("2026-10-22"),
  facts=[fact("To make these calls look credible, certain members, acting in concert with the operators, post false claims "
              "of profit and praise the 'expert'. This practice, known as astroturfing, creates a false impression of "
              "genuine support", S_WA)])
Q("008", T, SE, "Intermediate",
  "How did SEBI change the periodicity of KYC review for Foreign Portfolio Investors in October 2026?",
  ["From one year to two years and from three years to eight years, effective 1 December 2026; SWAGAT-FI FPIs stay at "
   "10 years", "From one year to three years for all FPIs", "KYC review was abolished for all FPIs",
   "From three years to five years for all FPIs, effective 1 April 2027"],
  concept="Ease of compliance for FPIs",
  explanation="FPIs earlier faced KYC review annually or every three years depending on category. The new periods are two "
              "years and eight years respectively; SWAGAT-FI FPIs remain at 10 years, and GS-FPI relaxations continue. "
              "The circular takes effect on 1 December 2026.",
  steps=["1 → 2 years", "3 → 8 years", "SWAGAT-FI: 10 years"],
  why="The other periods and dates are not those in SEBI's circular.",
  current=ca("2026-10-30"),
  facts=[fact("The revised framework increases the periodicity from one year to two years and from three years to eight "
              "years. In case of SWAGAT-FI FPIs, the periodicity of KYC review will remain unchanged at 10 years ... The "
              "provisions of the circular shall come into effect from December 01, 2026", S_FPIKYC)])
Q("008", T, SE, "Advanced",
  "SEBI's Board approved the SEBI (Settlement of Administrative and Civil Proceedings) Regulations, 2026 on 24 September "
  "2026. Under the approved formula, Settlement Amount = Base Amount × (S + R + G + A − M) + Legal Costs. Consider:\n"
  "I. Wrongful gains are excluded from the Base Amount and disgorged separately.\n"
  "II. 'G' is the gravity factor and 'M' the mitigating factors.\n"
  "III. The Base Amount is linked to the maximum penalty for the violation.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Settlement formula (Board-approved)",
  explanation="The Base Amount is linked to the minimum penalty under securities laws, with multipliers by type of "
              "applicant (so III is wrong). S is stage of proceedings, R the regulatory action factor, G gravity, A "
              "aggravating and M mitigating factors. Wrongful gains, losses avoided or caused are not in the Base Amount "
              "and are disgorged separately, removing double counting.",
  steps=["I ✓", "II ✓", "III ✗ (minimum penalty)"],
  why="Any option with III is wrong.",
  current=BRD,
  facts=[fact("Settlement Amount = Base Amount × (S + R + G + A - M) + Legal Costs. Base Amount (BA) linked to minimum "
              "penalty provided for the violation under securities laws ... 'G' the gravity factor ... 'A' the "
              "aggravating factors and 'M' the mitigating factors ... Wrongful gains ... will not be considered while "
              "determining the Base Amount. Such amounts, where quantified, will be disgorged separately", S_BRD)])

gain, yrs = 50, 2
assert gain * 0.09 * yrs == 9
Q("008", T, SE, "Advanced",
  "Under the settlement framework approved by SEBI's Board in September 2026, an entity in proceedings pending before the "
  "Board files a settlement application two years after the violation, which yielded a quantified wrongful gain of ₹50 "
  "lakh. What interest is charged on the disgorgement amount?",
  ["₹9 lakh (9% a year, simple, from violation to filing)", "₹12 lakh (12% a year)", "₹9.405 lakh (9% compounded "
   "annually)", "Nil, as disgorgement carries no interest"],
  concept="Interest on disgorgement",
  explanation="For proceedings pending before the Board, interest is 9% a year from the date of violation to the date of "
              "filing the settlement application, with no interest on interest: 50 × 9% × 2 = ₹9 lakh. The 12% rate "
              "applies only after a final order in other matters.",
  steps=["50 × 0.09 × 2 = 9"],
  why="12% applies after a final order; no compounding; interest is charged.",
  computed=True, current=BRD,
  facts=[fact("Interest on the disgorgement amount will now be charged at 9% per annum from the date of the violation till "
              "the date of filing of the settlement application for proceedings pending before the Board ... at 12% per "
              "annum thereafter till the filing ... Further, no interest will be charged on interest", S_BRD)])
assert round(50 * (1.09 ** 2 - 1), 3) == 9.405

Q("009", T, SE, "Basic",
  "What is SEBI's 'Cyber Suraksha Portal', launched in August 2026?",
  ["A central hub where securities market participants can access cybersecurity circulars, vulnerability warnings "
   "and incident insights", "A portal for investors to file complaints against brokers", "A trading platform for "
   "government securities", "A database of unregistered investment advisers"],
  concept="SEBI cyber security initiative",
  explanation="The Cyber Suraksha Portal is a centralised hub for the securities market to share cybersecurity knowledge; "
              "participants can directly access the latest circulars, vulnerability warnings and incident insights. "
              "Investor complaints go to SCORES.",
  steps=["Cyber Suraksha = cybersecurity information hub"],
  why="Complaints go to SCORES; the others are not its function.",
  current=ca("2026-08-24"),
  facts=[fact("SEBI has launched the Cyber Suraksha Portal. This platform provides a comprehensive, centralized hub for the "
              "securities market to share crucial knowledge and disseminate information regarding cyber security ... "
              "the latest cybersecurity circulars, vulnerability warnings and incident insights", S_CYB)])
Q("009", T, SE, "Basic",
  "What is the 'MUST' initiative that SEBI rolled out in October 2026?",
  ["Mentoring of University/College Students by Trainers, for financial literacy on campuses",
   "Market Utility for Settlement and Trading", "Mutual fund Unit Subscription Tracker",
   "Monitoring of Unregistered Stock Tipsters"],
  concept="Investor education",
  explanation="Under MUST, faculty, staff or senior students are trained and certified as Partner Trainers by SEBI, "
              "market partners and NISM to teach basic financial literacy, informed investing and fraud prevention on "
              "campus. It was launched with the 'Samajh Se Investing Simple' campaign under Project Jagrook.",
  steps=["MUST = Mentoring of University/College Students by Trainers"],
  why="The other expansions are invented.",
  current=ca("2026-10-05"),
  facts=[fact("SEBI rolled out the 'Mentoring of University/College Students by Trainers (MUST)' initiative to strengthen "
              "financial literacy and awareness about the securities market among students", S_MUST)])
Q("009", T, SE, "Intermediate",
  "In September 2026 SEBI extended the 'Samuhik Prativedan Manch' to clearing members who are also stock brokers. What "
  "is it?",
  ["A common reporting platform, so compliance reports are submitted once instead of separately to every exchange and "
   "clearing corporation", "A grievance redress forum for investors", "A common KYC registry for FPIs",
   "A platform for social stock exchange listings"],
  concept="Ease of compliance for intermediaries",
  explanation="Introduced for stock brokers on 18 July 2025, the platform lets intermediaries registered with several "
              "exchanges submit compliance reports once. Phase 1 for clearing members (from 30 September 2026) covers 14 "
              "reports, about 60% of their reporting; around 1,066 CMs benefit.",
  steps=["One submission consumed by all exchanges/CCs", "Phase 1: 14 reports (≈60%) from 30-9-2026"],
  why="It is not a grievance, KYC or social stock exchange platform.",
  current=ca("2026-09-17"),
  facts=[fact("Samuhik Prativedan Manch, a technology based common reporting platform for stock brokers ... SEBI ... is now "
              "extending the Samuhik Prativedan Manch to members of the Clearing Corporations (CCs), who are also stock "
              "brokers ... The first phase ... with effect from September 30, 2026 wherein submission of 14 compliance "
              "reports (approximately 60% of their reporting requirements) would be operationalised", S_SPM)])
Q("009", T, PS_, "Intermediate",
  "SEBI introduced a Closing Auction Session (CAS) in the equity cash segment from 3 August 2026. Why did SEBI announce "
  "in September 2026 that it would review a related methodology?",
  ["Because the CAS closing price is also the basis for settlement prices of derivative contracts on expiry, and "
   "stakeholders raised concerns about this", "Because CAS replaced the pre-open session", "Because CAS was withdrawn "
   "after one month", "Because the CAS price was used to fix IPO prices"],
  concept="Closing price discovery",
  explanation="CAS, introduced by a circular of 16 January 2026 and effective 3 August 2026, determines closing prices of "
              "securities, and that closing price is the basis for settlement prices of derivatives on expiry. After "
              "feedback during the first month, SEBI said it might propose changes to the settlement price methodology "
              "through a consultation paper.",
  steps=["CAS → closing price → derivative settlement price", "Feedback → review of settlement methodology"],
  why="CAS did not replace the pre-open session, was not withdrawn and is unrelated to IPO pricing.",
  current=ca("2026-09-03"),
  facts=[fact("SEBI, vide circular dated January 16, 2026, had introduced the Closing Auction Session (CAS) in the Equity "
              "Cash Segment with effect from August 3, 2026 ... the closing price determined through CAS also serves as a "
              "basis for determination of settlement prices for derivative contracts on expiry ... SEBI may be proposing "
              "certain changes in the methodology for determination of settlement prices", S_CAS)])
Q("009", T, SE, "Intermediate",
  "SEBI revamped its Document Number Verification System in 2026. What does a successful verification confirm?",
  ["That a letter with those details was issued by SEBI, but not the correctness of its contents",
   "That the letter's contents have been approved by SEBI's Board", "That the recipient is SEBI-registered",
   "That the matter in the letter has been settled"],
  concept="Fighting fake SEBI communications",
  explanation="The recipient enters the outward number, the issuing official's name, date, subject matter (now mandatory) "
              "and recipient's name. A match confirms that the letter was issued by SEBI; it does not verify the "
              "contents.",
  steps=["Verifies issuance, not contents"],
  why="The system does not approve contents, registration status or settlements.",
  current=ca("2026-10-01"),
  facts=[fact("the 'Document Number Verification System' has now been modified to include the 'Subject Matter' of a SEBI "
              "letter as one of the mandatory fields ... the recipient ... could verify whether such letter was issued by "
              "SEBI ... Such verification does not constitute a verification of the contents of that letter", S_DNVS)])
Q("009", T, PS_, "Intermediate",
  "In November 2026 SEBI constituted a Working Group to review the Innovators Growth Platform (IGP). Under which "
  "regulations is the IGP governed, and what is a key aim of the review?",
  ["The SEBI (ICDR) Regulations, 2018; to see whether the IGP suits research-stage, pre-revenue, IP-led and deep-tech "
   "enterprises", "The SEBI (Mutual Funds) Regulations, 2026; to create new fund categories",
   "The SEBI (LODR) Regulations, 2015; to delist small companies", "The Companies Act, 2013; to merge the IGP with the "
   "SME platform"],
  concept="Listing of innovation-led companies",
  explanation="The IGP framework sits in the SEBI (Issue of Capital and Disclosure Requirements) Regulations, 2018. The "
              "Working Group will examine the IGP's suitability for research-stage, pre-revenue, IP-led and deep-tech "
              "firms, the IGP investor framework, listing and capital raising, post-listing rules and migration to the "
              "main board.",
  steps=["IGP → ICDR Regulations, 2018", "Review for deep-tech/research-stage firms"],
  why="The other regulations do not govern the IGP.",
  current=ca("2026-11-04"),
  facts=[fact("SEBI has constituted a Working Group to undertake a comprehensive review of the regulatory framework "
              "governing the IGP under the SEBI (Issue of Capital and Disclosure Requirements) Regulations, 2018 ... "
              "Examine the suitability of the IGP framework for research-stage, pre-revenue, IP-led, deep-tech and other "
              "innovation- and technology-intensive enterprises", S_IGP)])
Q("009", T, SE, "Intermediate",
  "What does the MoU signed by SEBI and the Bank of England in October 2026 concern?",
  ["Cooperation and information exchange on SEBI-recognised clearing corporations, letting the BoE rely on SEBI's "
   "supervision of these central counterparties", "Listing of Indian companies on the London Stock Exchange",
   "A currency swap between RBI and the BoE", "Joint regulation of Indian mutual funds in the UK"],
  concept="Cross-border regulatory cooperation",
  explanation="The MoU covers cooperation regarding central counterparties and sets up a framework for the BoE to place "
              "reliance on SEBI's regulation and supervision of SEBI-recognised clearing corporations, facilitating "
              "international clearing while safeguarding UK financial stability.",
  steps=["SEBI–BoE MoU → CCPs; BoE relies on SEBI supervision"],
  why="It is not about listings, currency swaps or mutual funds.",
  current=ca("2026-10-28"),
  facts=[fact("SEBI and the Bank of England (BoE) have signed a Memorandum of Understanding (MoU) concerning cooperation and "
              "the exchange of information in relation to SEBI-recognised Clearing Corporations (CCs) ... establishes a "
              "framework for BoE to place reliance on SEBI's regulatory and supervisory activities", S_BOE)])
Q("009", T, SE, "Intermediate",
  "Under the Common Advertisement Code for specified SEBI-regulated entities approved by SEBI's Board on 24 September "
  "2026, which statement is correct?",
  ["Mandatory prior approval of advertisements is dropped except for celebrity endorsements, with post-issuance "
   "reporting within three working days", "Celebrity endorsements are banned for all regulated entities",
   "Every advertisement needs prior approval from SEBI", "The code applies only to mutual funds"],
  concept="Advertising by regulated entities (Board-approved)",
  explanation="The code covers stock brokers, DPs, investment advisers, research analysts, online bond platforms, "
              "portfolio managers and mutual funds/AMCs. Celebrity promotion at brand level is allowed with prior "
              "approval and safeguards; other prior approvals are dropped, but advertisements must be reported within "
              "three working days of issue.",
  steps=["No prior approval (except celebrity)", "Report within 3 working days"],
  why="Celebrities are permitted with approval; prior approval is not universal; the code covers several entity types.",
  current=BRD,
  facts=[fact("Use of celebrities for brand-level/entity-level promotion has been permitted for regulated entities, subject "
              "to prior approval and safeguards. Obtaining mandatory prior approval (except for advertisements containing "
              "celebrity endorsements) has been done away with. However, post-issuance reporting will be required within "
              "three (3) working days", S_BRD)])

Q("009", T, SE, "Advanced",
  "Under the Portfolio Managers Route for Investing in Mutual Fund units (PRIM) approved by SEBI's Board in September "
  "2026, which arrangement complies?",
  ["Client ticket ₹30 lakh; fixed fee 0.8% of AUM; 20% invested in schemes of the PM's group AMC",
   "Client ticket ₹20 lakh; fixed fee 0.8%; 10% in group AMC schemes",
   "Client ticket ₹30 lakh; fixed fee 1.5%; 10% in group AMC schemes",
   "Client ticket ₹30 lakh; fixed fee 0.8%; 40% in group AMC schemes"],
  concept="PRIM conditions (Board-approved)",
  explanation="PRIM lets portfolio managers invest clients' money in direct plans of mutual funds (including ETFs, index "
              "funds and SIFs) with a minimum ticket of ₹25 lakh, a fixed management fee capped at 1% of AUM and a "
              "prudential cap of 25% in schemes of affiliated/group AMCs. Only the first option meets all three.",
  steps=["Ticket ≥ 25 lakh", "Fee ≤ 1%", "Group AMC ≤ 25%"],
  why="₹20 lakh is below the minimum ticket; 1.5% exceeds the fee cap; 40% exceeds the 25% group cap.",
  computed=True, current=BRD,
  facts=[fact("Minimum Ticket Size INR 25 lakh ... Prudential cap of 25% on investments in schemes of affiliated/group/ "
              "associate AMCs. Fixed management fee capped at a maximum of 1% of the client's AUM", S_BRD)])
sa = 40
assert sa * 1.2 == 48
Q("009", T, SE, "Advanced",
  "Under the Settlement Regulations, 2026 approved by SEBI's Board, an entity whose settlement application was rejected "
  "under the 2018 Regulations uses the one-time window for a proceeding still pending before the Board. If the "
  "settlement amount computed is ₹40 lakh, what must it pay, and within what window must it apply?",
  ["₹48 lakh (an additional 20%), within 90 days of the new Regulations commencing", "₹40 lakh, within 60 days",
   "₹44 lakh (an additional 10%), within 30 days", "₹80 lakh (double), within one year"],
  concept="One-time settlement window (Board-approved)",
  explanation="A one-time 90-day window from commencement is open to entities that did not apply earlier or whose "
              "applications were rejected, withdrawn or returned under the 2018 Regulations, for specified proceedings "
              "pending before the Board, with an additional 20% settlement amount: 40 × 1.2 = ₹48 lakh.",
  steps=["40 × 1.20 = 48", "Window: 90 days from commencement"],
  why="The other amounts and windows misstate the surcharge and timing.",
  computed=True, current=BRD,
  facts=[fact("One-time window of 90 days from commencement of the Settlement Regulations, 2026 available to entities who "
              "either did not apply earlier or whose applications were rejected, withdrawn or returned under the 2018 "
              "Regulations ... subject to payment of an additional 20 % settlement amount", S_BRD)])
Q("009", T, SE, "Advanced",
  "Consider the following features of the SEBI Settlement Regulations, 2026, as approved by SEBI's Board:\n"
  "I. Before a show cause notice, SEBI may issue a settlement notice giving 60 days to apply.\n"
  "II. The time to file a settlement application after a show cause notice rises from 60 to 90 days.\n"
  "III. A fast-track route is available where the settlement amount does not exceed ₹1 crore.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Access to settlement (Board-approved)",
  explanation="I is correct (a 'Wells notice' type settlement notice, not issued where prosecution or an interim order is "
              "contemplated). II is correct. III is wrong: the monetary fast-track threshold is a settlement amount not "
              "exceeding ₹10 lakh.",
  steps=["I ✓", "II ✓", "III ✗ (₹10 lakh)"],
  why="Any option with III is wrong.",
  current=BRD,
  facts=[fact("Before issuance of a show cause notice, SEBI will issue a settlement notice giving 60 days to file a "
              "settlement application ... The period for filing a settlement application after service of a show cause "
              "notice increased from 60 days to 90 days ... A monetary threshold (settlement amount does not exceed ₹10 "
              "lakh) ... based fast-track settlement route introduced", S_BRD)])

Q("010", T, SE, "Basic",
  "Which department of SEBI prepares the annual Handbook of Statistics, whose 2025-26 (21st) edition was released in "
  "August 2026?",
  ["Department of Economic and Policy Analysis (DEPA)", "Investment Management Department", "Market Regulation "
   "Department", "Office of Investor Assistance and Education"],
  concept="SEBI publications",
  explanation="The Handbook of Statistics, a single-stop source of time-series data on the Indian securities market, is "
              "prepared every year by SEBI's DEPA. The 2025-26 edition has 153 tables (85 annual and 68 "
              "quarterly/monthly).",
  steps=["HBS → DEPA; 2025-26: 21st edition, 153 tables"],
  why="The other departments do not prepare the HBS.",
  current=ca("2026-08-17"),
  facts=[fact("The HBS is prepared and published every year by the Department of Economic and Policy Analysis (DEPA) of "
              "SEBI ... The HBS 2025-26, consists of 85 annual series tables and 68 quarterly/monthly series tables, "
              "totalling to 153 tables", S_HBS)])
Q("010", T, SE, "Basic",
  "What was the theme of World Investor Week 2026, observed in India from 5 to 11 October 2026?",
  ["Samajh Se Investing Simple", "Invest Smart, Invest Safe", "Digital Rupee for All", "Saving for Viksit Bharat"],
  concept="Investor awareness",
  explanation="The 10th edition of World Investor Week, held under IOSCO's aegis, was observed in India on the theme "
              "'Samajh Se Investing Simple', and SEBI launched a campaign of that name under Project Jagrook at Panjab "
              "University, Chandigarh.",
  steps=["WIW 2026 theme: Samajh Se Investing Simple"],
  why="The other phrases were not the theme.",
  current=ca("2026-10-05"),
  facts=[fact("The 10th edition of WIW, organised annually under the aegis of the International Organization of Securities "
              "Commissions (IOSCO), is being observed in India from October 05 to 11, 2026 on the theme 'Samajh Se "
              "Investing Simple'", S_MUST)])
Q("010", T, SE, "Intermediate",
  "In August 2026 SEBI released a consultation paper on KYC for individual Persons Resident Outside India (NRIs, OCIs and "
  "foreign nationals). Which of the following was among its proposals?",
  ["Removing the need for physical presence in India for PROI clients from FATF-compliant countries completing KYC "
   "digitally", "Barring PROIs from investing through more than one intermediary", "Making KYC valid for only one year "
   "for PROIs", "Requiring PROIs to open accounts only through Indian embassies"],
  concept="KYC for non-resident investors (proposal)",
  explanation="The proposals (not yet final) include dispensing with physical presence for PROIs from FATF-compliant "
              "countries, relying on KYC by entities of other financial sector regulators, mandatory email IDs, a wider "
              "list of certifying officials, portability of KYC across intermediaries and safeguards for video "
              "verification.",
  steps=["Proposal: digital KYC without physical presence (FATF-compliant countries)"],
  why="The other options run against the proposals, which aim to ease onboarding.",
  current=ca("2026-08-14"),
  facts=[fact("Eliminate the requirement of physical presence in India for PROI clients from FATF-compliant countries, to "
              "complete their KYC through digital mode ... Permit PROI client's KYC records to be portable across "
              "intermediaries in securities market", S_PROI)])
Q("010", T, SE, "Advanced",
  "The new Portfolio Managers Regulations approved by SEBI's Board in September 2026 introduce Independent Fund Managers "
  "(IFMs). Consider:\n"
  "I. The registered portfolio manager bears full responsibility and liability for an IFM's activities.\n"
  "II. Fees are paid directly to the registered portfolio manager.\n"
  "III. An IFM may operate under several portfolio managers at the same time.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="Independent Fund Managers (Board-approved)",
  explanation="I and II are correct; orders also flow through the PM's infrastructure and clients get an exit option if "
              "an IFM leaves. III is wrong: one PM may affiliate with several IFMs, but an IFM can operate under only one "
              "PM at a time. APMI keeps a central database of IFMs.",
  steps=["I ✓", "II ✓", "III ✗ (one PM at a time)"],
  why="Any option with III is wrong.",
  current=BRD,
  facts=[fact("Registered Portfolio Manager will have full responsibility and liability for all activities of IFM ... Fees "
              "will be paid directly to the registered portfolio manager ... One Portfolio Manager may affiliate with "
              "several IFMs while one IFM would only be able to operate under one PM at a time", S_BRD)])

pg0, pg1, w0, w1 = 70, 33, 19486, 11308
assert round(100 * (pg0 - pg1) / pg0) == 53 and round(100 * (w0 - w1) / w0) == 42
Q("010", T, SE, "Advanced",
  "SEBI said its rewritten Portfolio Managers Regulations shrink from 70 pages to 33, and from 19,486 words to 11,308, "
  "with provisos cut from 47 to 4. Which statement is correct?",
  ["Pages fall by about 53% and words by about 42%", "Pages fall by about 47% and words by about 58%",
   "Pages and words both fall by about 53%", "Pages fall by about 37% and words by about 8,178%"],
  concept="Regulatory simplification",
  explanation="Pages: (70 − 33) ÷ 70 ≈ 52.9% ≈ 53%. Words: (19,486 − 11,308) ÷ 19,486 = 8,178 ÷ 19,486 ≈ 42%.",
  steps=["(70 − 33)/70 ≈ 53%", "8,178/19,486 ≈ 42%"],
  why="47% and 58% are the complements; the two reductions differ; 8,178 is the absolute word cut, not a percentage.",
  computed=True, current=BRD,
  facts=[fact("The exercise has resulted in a 53% reduction in the size of the regulations from 70 pages to 33 pages. The "
              "word count has been reduced by approximately 42%, from 19,486 words ... to 11,308 words ... the number of "
              "provisos have been reduced from 47 to 4", S_BRD)])
fee_l, ord_y, post_y = 20, 3, 1
assert round(fee_l * (0.09 * ord_y + 0.12 * post_y), 2) == 7.8
Q("010", T, SE, "Advanced",
  "Under the settlement framework approved by SEBI's Board in September 2026, a wrongful gain of ₹20 lakh is quantified "
  "in a matter not pending before the Board. A final order comes 3 years after the violation, and a settlement "
  "application is filed 1 year after that order. What interest is payable on the disgorgement amount?",
  ["₹7.8 lakh (9% for 3 years plus 12% for 1 year, simple)", "₹7.2 lakh (9% for 4 years)",
   "₹9.6 lakh (12% for 4 years)", "₹5.4 lakh (9% for 3 years only)"],
  concept="Interest on disgorgement in other matters",
  explanation="For other matters: 9% a year from violation to final order, then 12% a year until the settlement "
              "application, with no interest on interest. 20 × 9% × 3 = 5.4; 20 × 12% × 1 = 2.4; total ₹7.8 lakh.",
  steps=["20 × 0.09 × 3 = 5.4", "20 × 0.12 × 1 = 2.4", "Total 7.8"],
  why="The other options apply one rate throughout or ignore the post-order period.",
  computed=True, current=BRD,
  facts=[fact("For other matters, the interest will be charged at 9% per annum from the date of the violation till the "
              "date of final order and at 12% per annum thereafter till the filing of the settlement application. "
              "Further, no interest will be charged on interest", S_BRD)])

# ============================================================================================ Insurance
T = "Insurance"
IR, GI = "IRDAI", "Government insurance schemes"
IRDAI_ST = "https://www.majmudarindia.com/wp-content/uploads/2026-08-17_IRDAI-share-transfer-regulatory-changes-update.pdf"
IRA = ca("2026-07-30")     # IRDAI (Registration, Capital Structure, Transfer of Shares and Amalgamation) Amendment Regs

Q("008", T, IR, "Basic",
  "Under the IRDAI amendment regulations notified on 30 July 2026, who may use words such as 'insurance', 'insurer' or "
  "'assurance' in its name?",
  ["Only persons carrying on insurance business in India; existing insurers without such a word must add one within "
   "12 months", "Any company registered with the Registrar of Companies", "Only public sector insurers",
   "Any company with IRDAI's no-objection, whatever its business"],
  concept="Names of insurers",
  explanation="No person other than one carrying on insurance business in India may use 'insurance', 'insurer', "
              "'assurance', 're-insurance', 'insurance company' or derivatives in its name. Existing insurers lacking such "
              "a word must change their name within twelve months of 30 July 2026, after an IRDAI no-objection "
              "certificate.",
  steps=["Insurance words reserved for insurers", "Existing insurers: add a word within 12 months"],
  why="The restriction is not limited to public sector insurers, and other companies cannot use the words.",
  current=IRA,
  facts=[fact("no person other than a person carrying on insurance business in India can use 'insurance,' 'insurer,' "
              "'assurance,' 're-insurance', 'insurance company' or derivatives in its name ... This should be done twelve "
              "(12) months from July 30, 2026", IRDAI_ST)])
Q("008", T, IR, "Intermediate",
  "Under IRDAI's amended share-transfer rules of July 2026, a transferee's acquisition in an insurer needs IRDAI's prior "
  "approval when:",
  ["Its holding crosses 5%; or, if already above 5%, crosses 10%, 25%, 50% or 75%; or it becomes the single largest "
   "shareholder", "Every additional 5% block is acquired, whatever the holding", "Its holding crosses 26% only",
   "Only when it acquires control (above 50%)"],
  concept="Approval thresholds for share transfers",
  explanation="Approval is needed if a transferee holding 5% or less is likely to exceed 5%; if one holding more than 5% "
              "is likely to cross 10%, 25%, 50% or 75%; or if it is likely to become the single largest shareholder. "
              "Earlier, approval was needed for every 5% block.",
  steps=["Cross 5%", "Then cross 10/25/50/75%", "Or become single largest shareholder"],
  why="The 5%-block rule is the old regime; 26% or control alone are not the triggers.",
  current=IRA,
  facts=[fact("prior IRDAI approval is required ... (A) if the transferee holds 5% or less before the transfer and is likely "
              "to exceed 5% thereafter; (B) if the transferee holds more than 5% before the transfer and the "
              "shareholding post transfer is likely to exceed 10%, 25%, 50% or 75%; or (C) if the shareholder is likely "
              "to become the single largest shareholder ... Under the previous regime, approval was required for every "
              "transfer in blocks of 5%", IRDAI_ST)])
Q("008", T, IR, "Intermediate",
  "Under IRDAI's July 2026 amendments, a shareholder transferring shares of an insurer needs prior approval when the "
  "nominal value transferred in a financial year exceeds what share of the insurer's paid-up equity capital?",
  ["5% (earlier 1%)", "1% (unchanged)", "10% (earlier 5%)", "26% (earlier 10%)"],
  concept="Transferor-side threshold",
  explanation="Prior approval is required where the nominal value of shares intended to be transferred by any person, "
              "group or body corporate under the same management, jointly or severally, exceeds 5% of paid-up equity "
              "capital in a financial year; the earlier threshold was 1%. This implements the Sabka Bima Sabki Raksha "
              "Act, 2025.",
  steps=["Transferor threshold: 1% → 5% of paid-up capital per FY"],
  why="The other pairs do not match the amendment.",
  current=IRA,
  facts=[fact("where the nominal value of shares intended to be transferred by any individual, firm, group, constituents of "
              "a group, or body corporate under the same management, jointly or severally, exceeds 5% (previously 1%) of "
              "the insurer's paid-up equity capital in a financial year", IRDAI_ST)])
Q("008", T, GI, "Intermediate",
  "How does the Department of Financial Services define an 'accident' for Pradhan Mantri Suraksha Bima Yojana (PMSBY)?",
  ["A sudden, unforeseen and involuntary event caused by external, violent and visible means",
   "Any event causing hospitalisation for more than 24 hours", "Any death other than natural death",
   "Any injury at the workplace"],
  concept="Accident under PMSBY",
  explanation="PMSBY defines an accident as a sudden, unforeseen and involuntary event caused by external, violent and "
              "visible means. Only death or specified disability from such an accident is covered.",
  steps=["Sudden + unforeseen + involuntary + external, violent, visible means"],
  why="The other definitions are broader or different from the scheme's.",
  facts=[fact("Accident means a sudden, unforeseen and involuntary event caused by external, violent and visible means",
              D_PMSBY)])
Q("008", T, GI, "Intermediate",
  "Can a Non-Resident Indian join Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)?",
  ["Yes, through an eligible account with a bank branch in India; any claim is paid to the nominee only in Indian "
   "currency", "No, the scheme is only for residents", "Yes, and the claim can be paid in the currency of residence",
   "Only if the NRI returns to India within a year"],
  concept="NRIs under PMJJBY",
  explanation="Any NRI with an eligible bank account in a branch in India can buy PMJJBY cover, subject to the scheme's "
              "terms; claims are paid to the beneficiary/nominee only in Indian rupees.",
  steps=["NRI + Indian bank account → eligible", "Claim paid in INR"],
  why="NRIs are not barred, and claims are not paid in foreign currency.",
  facts=[fact("Any NRI having an eligible bank account with a bank branch located in India is eligible for purchase of "
              "PMJJBY cover ... However, in case a claim arises, the claim benefit will be paid to the beneficiary/ "
              "nominee only in Indian currency", D_PMJJBY)])
Q("008", T, IR, "Advanced",
  "Under IRDAI's share-transfer thresholds of July 2026, which of these acquisitions of an insurer's shares needs IRDAI's "
  "prior approval on the basis of the transferee's holding?\n"
  "P. 3% → 4.5%\nQ. 6% → 9%\nR. 22% → 27%\nS. 12% → 18%, making it the single largest shareholder",
  ["R and S only", "Q, R and S", "P and R only", "S only"],
  concept="Applying approval thresholds",
  explanation="P stays at or below 5%: no approval. Q (above 5%) stays below 10%: no approval. R crosses 25%: approval "
              "needed. S crosses no marker (10% is already passed), but becomes the single largest shareholder: approval "
              "needed. So R and S.",
  steps=["P: ≤ 5% ✗", "Q: 6→9, no marker ✗", "R: crosses 25% ✓", "S: single largest ✓"],
  why="Q crosses no marker; P stays within 5%.",
  computed=True, current=IRA,
  facts=[fact("(A) if the transferee holds 5% or less before the transfer and is likely to exceed 5% thereafter; (B) if the "
              "transferee holds more than 5% before the transfer and the shareholding post transfer is likely to exceed "
              "10%, 25%, 50% or 75%; or (C) if the shareholder is likely to become the single largest shareholder",
              IRDAI_ST)])

Q("009", T, GI, "Basic",
  "Can all holders of a joint bank account join PMJJBY through that account?",
  ["Yes, each holder who meets the eligibility and pays the premium can join", "No, only the first holder can join",
   "No, joint accounts are not eligible", "Only if all holders are of the same age"],
  concept="PMJJBY eligibility",
  explanation="In a joint account, all holders can join PMJJBY if each satisfies the eligibility criteria (age 18–50 at "
              "entry) and pays the appropriate premium.",
  steps=["Joint account → every eligible holder may join"],
  why="The scheme does not limit cover to the first holder or exclude joint accounts.",
  facts=[fact("In case of a joint account, all holders of the said account can join the scheme provided they satisfy its "
              "eligibility criteria and pay the appropriate premium", D_PMJJBY)])
Q("009", T, GI, "Intermediate",
  "For claims under PMSBY, how must an accident be documented, according to the Department of Financial Services?",
  ["Road, rail and similar vehicular accidents, drowning and deaths involving crime must be reported to police; cases "
   "like snake bite or a fall from a tree must be supported by immediate hospital records",
   "A police FIR is required for every claim", "No documents are needed; the bank's certificate is enough",
   "Only a death certificate is needed in all cases"],
  concept="PMSBY claim documentation",
  explanation="Accidents such as road, rail and vehicular accidents, drowning and crime-related deaths must be reported to "
              "the police; for events like snake bite or a fall from a tree, the cause must be supported by immediate "
              "hospital records.",
  steps=["Vehicular/drowning/crime → police report", "Snake bite/fall → hospital record"],
  why="The requirement varies with the type of accident; documentation is necessary.",
  facts=[fact("In case of incidents like road, rail and similar vehicular accidents, drowning, death involving any crime etc, "
              "the accident should be reported to police. In case of incidents like snake bite, fall from tree etc, the "
              "cause should be supported by immediate hospital record", D_PMSBY)])
Q("009", T, IR, "Intermediate",
  "What did the IRDAI (Insurance Intermediaries) (Amendment) Regulations, 2026 change for corporate agents?",
  ["Registration becomes perpetual (no three-yearly renewal) subject to annual fees and compliance; existing agents must "
   "upgrade by 31 January 2027", "Corporate agents must renew registration every year",
   "Corporate agents were abolished in favour of brokers", "Registration is valid for ten years"],
  concept="Corporate agents",
  explanation="Corporate agent registrations are now permanent if annual fees and compliances are maintained, instead of "
              "renewal every three years. Existing agents must upgrade by 31 January 2027 (or 31 March 2027 with a late "
              "fee). From 1 January 2027 every policy must be linked to the person who solicited it.",
  steps=["Perpetual registration", "Upgrade by 31-1-2027", "Policies linked to solicitor from 1-1-2027"],
  why="The other options misstate the change.",
  current=IRA,
  facts=[fact("corporate agent registrations are now permanent provided annual fees and compliances are maintained. "
              "Previously, they had to be renewed every three (3) years. Existing corporate agents must upgrade to the new "
              "perpetual registration by January 31, 2027 (or by March 31, 2027, with a late fee) ... starting January 1, "
              "2027, every policy must be officially linked to the specific person who solicited the insurance policy",
              IRDAI_ST)])

Q("009", T, GI, "Advanced",
  "Meena, 32, enrols in PMJJBY for the first time in January through a bank agent. Using the DFS schedule, what premium "
  "does she pay, and how much of it goes to the insurer as insurance premium?",
  ["₹228, of which ₹206 goes to the insurer", "₹436, of which ₹395 goes to the insurer",
   "₹342, of which ₹309 goes to the insurer", "₹114, of which ₹103 goes to the insurer"],
  concept="Pro-rata PMJJBY premium",
  explanation="For enrolment in December, January or February (third quarter of the June–May cover), the pro-rata premium "
              "is ₹228. It is split as ₹206 to the insurer, ₹15 commission to the BC/agent and ₹7 administrative "
              "expenses to the bank.",
  steps=["Dec–Feb enrolment → ₹228", "228 = 206 + 15 + 7"],
  why="₹436 is for June–August, ₹342 for September–November and ₹114 for March–May.",
  computed=True,
  facts=[fact("c) For enrolment in December, January and February – pro rata premium of Rs. 228/- is payable", D_PMJJBY),
         fact("Rs.228/- collected in the 3rd quarter of risk period: Insurance Premium to LIC/ Insurance Company Rs.206/-; "
              "Commission ... Rs.15/-; Administrative Expenses ... Rs.7/-", D_PMJJBY)])
assert 206 + 15 + 7 == 228
Q("009", T, GI, "Advanced",
  "Consider the following statements about PMSBY claims, based on the Department of Financial Services' FAQs:\n"
  "I. A disability claim is credited to the bank account of the insured subscriber.\n"
  "II. If no nominee was registered, the death claim can be filed by the legal heirs.\n"
  "III. If the insured is missing, the claim is paid after seven years even without evidence of an accident.\n"
  "Which of the above is/are correct?",
  ["I and II only", "II and III only", "I and III only", "I, II and III"],
  concept="PMSBY claim settlement",
  explanation="Disability claims go to the insured's account; death claims go to the nominee/appointee or, if there is no "
              "nomination, the legal heirs. PMSBY covers deaths due to accident confirmed by documentary evidence only, "
              "so III is wrong.",
  steps=["I ✓", "II ✓", "III ✗ (accident death must be documented)"],
  why="Any option with III is wrong.",
  facts=[fact("Disability claim will be credited in the bank account of the insured bank account holder / subscriber. "
              "Death claim will be remitted to the bank account of the nominee / legal heir(s) ... claim can be filed by "
              "the nominee/appointee ... or by the legal heir/s in case there is no nomination", D_PMSBY),
         fact("PMSBY covers deaths due to accident as confirmed by documentary evidence only", D_PMSBY)])

Q("010", T, GI, "Basic",
  "Which bank account holders are NOT eligible to subscribe to PMJJBY and PMSBY?",
  ["Institutional account holders", "Joint account holders", "NRIs with an eligible account in India",
   "Post Office savings account holders"],
  concept="Eligibility for the Suraksha schemes",
  explanation="All bank account holders other than institutional account holders may subscribe. Joint holders, NRIs with "
              "an eligible Indian account and Post Office account holders can join.",
  steps=["Institutional accounts → not eligible"],
  why="The other three are eligible.",
  facts=[fact("All bank account holders other than institutional account holders are eligible for subscribing to PMSBY "
              "scheme", D_PMSBY),
         fact("All bank account holders other than institutional account holders are eligible for subscribing to PMJJBY "
              "scheme", D_PMJJBY)])
Q("010", T, GI, "Basic",
  "When does the risk cover begin for a person joining PMSBY after the start of the June–May cover year?",
  ["From the date the premium is auto-debited from the account", "From 1 June of that year", "After a 30-day lien "
   "period", "From the next 1 June"],
  concept="Commencement of PMSBY cover",
  explanation="New entrants can join any time by paying the annual premium through auto-debit; risk cover starts from the "
              "date of auto-debit. (The 30-day lien period applies to PMJJBY for non-accidental death, not PMSBY.)",
  steps=["PMSBY cover starts on auto-debit date"],
  why="Cover is not backdated to 1 June or deferred; the lien period belongs to PMJJBY.",
  facts=[fact("new eligible entrants can also join in future years on payment of premium through auto-debit. However, risk "
              "cover would start from the date of auto debit of premium from the subscriber's account", D_PMSBY)])
Q("010", T, GI, "Intermediate",
  "A person who left PMJJBY rejoins in a later year by paying the appropriate premium. What applies to the cover?",
  ["Death other than by accident in the first 30 days after re-enrolment is not covered", "Full cover from day one, "
   "as he was a past member", "Only accidental death is covered for the first year", "He cannot rejoin once he has left"],
  concept="Lien period on re-joining PMJJBY",
  explanation="Members who exit may rejoin later by paying the appropriate premium, but, as for new members, death due to "
              "any cause other than accident during the first 30 days from enrolment is not covered.",
  steps=["Rejoin allowed", "30-day lien for non-accidental death"],
  why="Past membership does not waive the lien; the restriction lasts 30 days, not a year; rejoining is allowed.",
  facts=[fact("Individuals who exit the scheme at any point may re-join the scheme in future years by paying the appropriate "
              "premium ... However, for such subscribers, insurance benefit shall not be available for death (due to any "
              "cause other than accident) occurring during the first 30 days from the date of enrolment", D_PMJJBY)])
Q("010", T, IR, "Intermediate",
  "By how much did IRDAI's July 2026 amendments reduce the processing fee for a share-transfer application where the "
  "transfer exceeds 50% of an insurer's paid-up equity capital?",
  ["From ₹50 lakh to ₹10 lakh", "From ₹1 crore to ₹50 lakh", "From ₹10 lakh to ₹5 lakh", "It was abolished"],
  concept="IRDAI processing fees",
  explanation="The fee for share-transfer applications exceeding 50% of paid-up equity was cut from ₹50,00,000 to "
              "₹10,00,000. A flat ₹10 lakh fee per entity also applies to amalgamation applications.",
  steps=["₹50 lakh → ₹10 lakh"],
  why="The other figures are not those in the amendment.",
  current=IRA,
  facts=[fact("the IRDAI's processing fee for share transfer applications in cases where the transfer of shareholding "
              "exceeds 50% of the paid-up equity capital of the insurer has been reduced from INR5,000,000 ... to "
              "INR1,000,000", IRDAI_ST)])
Q("010", T, IR, "Intermediate",
  "After IRDAI's July 2026 amendments, how are share transfers of listed insurance companies treated?",
  ["The separate regulation for listed insurers was omitted, so listed and unlisted insurers follow a single approval "
   "track", "Listed insurers no longer need any approval for share transfers", "Only SEBI approves transfers in listed "
   "insurers", "Listed insurers need approval for every transfer above 1%"],
  concept="Unified approval track",
  explanation="Regulation 25 of the 2024 regulations, which governed share transfers of listed insurers, was omitted in its "
              "entirety, placing listed and unlisted insurers on a single approval track under the new thresholds.",
  steps=["Regulation 25 omitted → one track for listed and unlisted"],
  why="Approval requirements remain; IRDAI, not SEBI, approves; the 1% threshold is gone.",
  current=IRA,
  facts=[fact("Regulation 25 of the Principal Regulations (that governed the transfer of shares of listed insurance "
              "companies) has been omitted in its entirety, placing listed and unlisted insurers on a single approval "
              "track", IRDAI_ST)])
Q("010", T, GI, "Intermediate",
  "How is the PMSBY premium of ₹20 per member appropriated, according to the Department of Financial Services?",
  ["₹20 goes to the insurer, which pays ₹1 commission to BCs/agents (new enrolments) and ₹1 administrative expense to "
   "the bank", "₹18 to the insurer and ₹2 to the bank", "₹20 to the bank, which pays the insurer later",
   "₹15 to the insurer, ₹3 to agents and ₹2 to the bank"],
  concept="Appropriation of PMSBY premium",
  explanation="The full ₹20 is insurance premium payable to the insurer; out of it the insurer pays Re 1 per member as "
              "commission to BCs/agents (new enrolments only) and Re 1 per member per year as administrative expenses to "
              "the participating bank.",
  steps=["Insurer gets 20; pays 1 (BC) + 1 (bank)"],
  why="The other splits do not match the FAQ.",
  facts=[fact("Insurance Premium payable to Insurance Company: Rs. 20/- per annum per member. Commission payable to Business "
              "Correspondents, agents, etc. by the insurer: Re.1/- per member (for new enrolments only). Administrative "
              "expenses payable to participating Bank by insurer: Re.1/- per annum per member", D_PMSBY)])
Q("010", T, IR, "Advanced",
  "Under IRDAI's July 2026 amendments, which of these holding companies may amalgamate into the insurer it holds?\n"
  "P. Holds 60% of the insurer; has no other business; consideration in equity shares.\n"
  "Q. Holds 60% of the insurer; also runs a software business.\n"
  "R. Holds 45% of the insurer; has no other business.\n"
  "S. Holds 70% of the insurer; has no other business; consideration partly in cash.",
  ["P only", "P and S only", "P and R only", "P, Q and S"],
  concept="Amalgamation of a non-insurance entity into an insurer",
  explanation="A non-insurance transferor may amalgamate with the insurer if it holds more than 50% of the insurer's "
              "paid-up equity and has no other non-insurance business, and only equity may be paid as consideration. Q "
              "has another business, R holds only 45%, and S proposes cash; only P qualifies.",
  steps=["> 50% ✓, no other business ✓, equity only ✓ → P"],
  why="Q, R and S each fail one condition.",
  computed=True, current=IRA,
  facts=[fact("permit a non-insurance business entity/ transferor to amalgamate with the transferee insurer, provided that "
              "the transferor holds more than 50% of the paid-up equity capital of the transferee insurer and has no "
              "other non-insurance business ... other than equity, no other form of payment is allowed as consideration",
              IRDAI_ST)])
Q("010", T, IR, "Advanced",
  "An insurer makes a rights issue. Shareholder X, holding 8%, does not subscribe and is diluted to 6.5%. How do IRDAI's "
  "July 2026 amendments treat this?",
  ["The fall in X's holding from non-subscription is treated as shares intended to be transferred, so the transferor "
   "thresholds must be checked", "It is ignored, since X sold nothing", "It needs SEBI's approval, not IRDAI's",
   "X must buy back shares to restore 8%"],
  concept="Passive dilution as deemed transfer",
  explanation="A decrease in a shareholder's holding due to non-subscription on a pro-rata basis in a fresh equity issue "
              "is treated as shares intended to be transferred. Here 1.5% of capital is deemed transferred; it is within "
              "the 5% per-year transferor threshold, but the rule means every existing holder's position must be "
              "modelled.",
  steps=["Dilution 8 → 6.5 = 1.5% deemed transfer", "Compare with 5% per FY threshold"],
  why="The dilution is not ignored; SEBI does not approve; no buy-back obligation exists.",
  computed=True, current=IRA,
  facts=[fact("a decrease in a shareholder's shareholding pursuant to non-subscription on a pro-rata basis in a fresh "
              "issuance of equity shares is also treated as shares intended to be transferred", IRDAI_ST)])
assert round(8 - 6.5, 1) == 1.5 < 5
Q("010", T, GI, "Advanced",
  "Consider the following statements about PMSBY, based on the Department of Financial Services' FAQs:\n"
  "I. Death of the insured by murder is covered.\n"
  "II. A partial disability without irrecoverable loss of sight of an eye or use of a hand or foot gets ₹50,000.\n"
  "III. A PMSBY cover is in addition to any other insurance cover the subscriber has.\n"
  "Which of the above is/are correct?",
  ["I and III only", "I and II only", "II and III only", "I, II and III"],
  concept="Scope of PMSBY",
  explanation="I is correct: death by murder is covered (suicide is not). II is wrong: no benefit is payable for partial "
              "disability without such irrecoverable loss. III is correct: PMSBY cover is in addition to "
              "other insurance.",
  steps=["I ✓", "II ✗ (no benefit)", "III ✓"],
  why="Any option with II is wrong.",
  facts=[fact("While death due to suicide is not covered, that from murder is covered ... What benefit will be payable if a "
              "person suffers partial disability without irrecoverable loss of sight of one eye or loss of use of one "
              "hand or foot? No benefit will be payable ... Will this cover be in addition to cover under any other insurance "
              "scheme the subscriber may be covered under? Yes", D_PMSBY)])

# ============================================================================================ checks and output
TOPIC_ORDER = PKG["topics"]
written = []
for b in BATCHES:
    spec = PKG["batches"][b]
    qs = sorted(QS[b], key=lambda q: TOPIC_ORDER.index(q["topic"]))       # stable: keeps authoring order in a topic
    planned = Counter({(t["topic"], d): n for t in spec["topics"] for d, n in t["quota"].items() if n})
    have = Counter((q["topic"], q["difficulty"]) for q in qs)
    assert have == planned, (b, sorted(set(have.items()) ^ set(planned.items())))
    subs = {t["topic"]: set(t["subtopics"]) for t in spec["topics"]}
    assert all(q["subtopic"] in subs[q["topic"]] for q in qs), [(q["topic"], q["subtopic"]) for q in qs
                                                                if q["subtopic"] not in subs[q["topic"]]]
    assert len(qs) == spec["count"]
    assert Counter(q["difficulty"] for q in qs) == Counter(spec["by_difficulty"])
    lo, hi = spec["question_ids"]
    first = int(lo.split("_")[-1])
    assert int(hi.split("_")[-1]) - first + 1 == len(qs)
    keys = _keys[b]
    assert max(keys.values()) - min(keys.values()) <= 2, (b, keys)
    out_qs = []
    for n, q in enumerate(qs):
        qid = f"BANK_BFA_{first + n:06d}"
        facts, computed, current = q.pop("_facts"), q.pop("_computed"), q.pop("_current")
        urls = {f["source_url"] for f in facts}
        web = (["web:fact-check"] if urls - SEARCH_ONLY else []) + (["web:search-confirmed"] if urls & SEARCH_ONLY
                                                                     else [])
        rec = {"question_id": qid, **q}
        if current:
            assert current["event_date"] <= CHECKED, (qid, current)
            rec_items = list(rec.items())
            idx = [k for k, _ in rec_items].index("suggested_time_seconds") + 1
            rec = dict(rec_items[:idx] + [("current_affairs", current)] + rec_items[idx:])
        rec["source"] = {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                         "original_exam_year": None, "license_note": None}
        rec["verification"] = {"answer_verified": True, "solution_verified": True,
                               "review_status": "Pending Human Review",
                               "verified_by": ["ai:author-solve", *web] + (["script:recompute"] if computed else [])
                               + (["ai:independent-check"] if qid in INDEPENDENT else []),
                               "verified_at": TODAY, "fact_checks": facts}
        out_qs.append(rec)
    assert out_qs[0]["question_id"] == lo and out_qs[-1]["question_id"] == hi
    assert all(q.get("current_affairs") for q in out_qs if q["topic"] == "Budget and Economic Survey")
    assert len({q["question_text"] for q in out_qs}) == len(out_qs)
    written.append((b, spec, out_qs))

allq = [q for _, _, qs in written for q in qs]
assert len({q["question_text"] for q in allq}) == len(allq) == PKG["total"]
assert INDEPENDENT <= {q["question_id"] for q in allq}

for b, spec, qs in written:
    frag = {
        "schema_version": "1.0",
        "batch_id": spec["batch_id"],
        "created_at": TODAY,
        "notes": (f"{spec['batch_id']} Banking and Financial Awareness, topic package 3 (payments banks, SFBs, financial, "
                  f"money and capital markets, insurance, mutual funds, Budget/Economic Survey, government financial "
                  f"schemes, RBI circulars): {len(qs)} original questions, {spec['question_ids'][0]} to "
                  f"{spec['question_ids'][1]}. Built by tools/packages/BFA_pkg3.py from sources opened on 2026-11-06 "
                  "(RBI directions, notifications and press releases; SEBI circulars and press releases; CGTMSE scheme "
                  "document; DFS scheme pages; PIB Budget compendium; named news and law-firm pages). Only rules in force "
                  "are tested; Board-approved or draft items are framed as such. Computed answers are re-derived with "
                  "asserts. Facts tested in BATCH_000-BATCH_007 Banking parts are not repeated."),
        "stimuli": [],
        "questions": qs,
    }
    out = ROOT / spec["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.name}: {len(qs)} questions; keys {dict(sorted(_keys[b].items()))}; "
          f"current_affairs {sum('current_affairs' in q for q in qs)}; "
          f"independent {sum(q['question_id'] in INDEPENDENT for q in qs)}")

# @@END@@
