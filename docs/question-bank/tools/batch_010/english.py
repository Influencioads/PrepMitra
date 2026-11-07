"""Writes batches/parts/BATCH_010_ENG.json: the 149 English Language questions of BATCH_010.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000 to BATCH_009 (passages and para-jumble topics), and the grammar rules, idioms and words tested are ones not
tested in those batches. Run from anywhere:

    python docs/question-bank/tools/batch_010/english.py

Structural checks (quota per topic and difficulty, subtopics, ID range, passage length, set sizes, option count, cloze
blank numbering, 'No error' / 'No replacement' / 'No swap' placement, para-jumble option validity, RC option-length
spread, repeated stems, passage titles and passage themes against all earlier English files, keyed words and bold
words against all earlier English files, answer-key balance) and the computable answers (the calibration check in
RC 3, the screening-test arithmetic in RC 6 and the popcorn prices in Cloze 3) are asserted before anything is
written. Option letters are never named in solutions (except the fixed parts A/B/C of Error Detection), and solutions
never refer to an option by its position, so the script places the correct option itself (seeded shuffle) to keep the
answer keys balanced.
"""

import json
import random
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
EN = "English Language"
LETTERS = "ABCD"
FIRST_ID = 1352
FIRST_STIM = 10001
EARLIER = ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json", "parts/BATCH_002_ENG.json",
           "parts/BATCH_003_ENG.json", "parts/BATCH_004_ENG.json", "parts/BATCH_005_ENG.json",
           "parts/BATCH_006_ENG.json", "parts/BATCH_007_ENG.json", "parts/BATCH_008_ENG.json",
           "parts/BATCH_009_ENG.json")

QS = []
FREE, LAST_FIXED, FIXED = "free", "last_fixed", "fixed"   # how the options may be reordered


def Q(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, why, seconds,
      stim=None, pos=None, shortcut=None, order=FREE):
    """answer is the 0-based index of the correct option in `options` (letters are assigned at the end)."""
    assert len(options) == 4 and 0 <= answer < 4, text
    assert why, text
    out = {
        "question_id": None,
        "exam_mappings": default_mappings(EN, difficulty),
        "subject": EN, "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_type": "MCQ", "language": "en",
    }
    if stim:
        out |= {"stimulus_id": stim, "set_position": pos}
    out |= {
        "question_text": text,
        "options": list(options),
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why, "final_answer": None},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True,
                         "review_status": "Pending Human Review",
                         "verified_by": ["ai:author-solve"], "verified_at": TODAY},
        "_order": order,
    }
    QS.append(out)
    return out


STIMULI = []


def stim(title, content, kind="passage"):
    sid = f"STIM_ENG_{FIRST_STIM + len(STIMULI):06d}"
    STIMULI.append({"stimulus_id": sid, "type": kind, "title": title, "content": content})
    return sid


RC, CL = "Reading Comprehension", "Cloze Test"
B, I, A = "Basic", "Intermediate", "Advanced"

# =====================================================================================================================
# READING COMPREHENSION
# =====================================================================================================================

# ---------------------------------------------------------------- RC 1 (Basic, 6)
P1 = stim("A pinch of iodine", (
    "For most of us, salt is just salt: something we add to food without a second thought. Yet the packet in an "
    "Indian kitchen today usually carries a small word printed on it: 'iodised'. Behind that word lies one of the "
    "cheapest and most successful public health measures ever attempted.\n\n"
    "The human body needs only a tiny amount of iodine, but it cannot do without it. The thyroid gland in the neck "
    "uses iodine to make hormones that control growth and the development of the brain. When the diet lacks iodine, "
    "the gland swells, producing a visible lump in the neck known as goitre. The hidden damage is worse. A mother who "
    "lacks iodine during pregnancy may give birth to a child whose mental development is permanently held back.\n\n"
    "Iodine deficiency is common in hilly regions and in areas prone to floods, where rain and rivers have washed "
    "much of the iodine out of the soil. Crops grown in such soil contain little of it, and so do the people who eat "
    "them. For generations, whole villages in the Himalayan foothills were known for the number of people with "
    "swollen necks.\n\n"
    "The solution that health experts settled on was simple. Instead of asking people to change their diet, they "
    "decided to add a little iodine to something everybody already eats every day. Salt was the ideal choice. Rich "
    "and poor alike consume it, in roughly similar amounts, and adding iodine to it costs only a few paise per "
    "kilogram. India launched a national programme against goitre in the 1960s, and over the following decades "
    "iodised salt became the norm in most households.\n\n"
    "The work is not finished, however. Some families still buy cheap loose salt from small producers who do not add "
    "iodine to it. Iodine can also be lost from salt that is stored carelessly. Damp air, heat and sunlight all cause "
    "it to escape, so a packet left open near the stove may slowly lose much of its value.\n\n"
    "The advice to households is therefore easy to follow: buy salt that is labelled 'iodised' and keep it in a "
    "closed, dry container away from the stove. It is a small habit, but it protects the most valuable thing a child "
    "carries into the world: a healthy mind."))

Q(RC, "Factual", B,
  "According to the passage, what does the thyroid gland use iodine for?",
  ["To make hormones that control growth and brain development",
   "To remove salt that the body does not need",
   "To protect the neck from damp air and heat",
   "To help the stomach digest crops grown in hilly areas"], 0,
  "Locating a stated fact",
  "Paragraph 2: 'The thyroid gland in the neck uses iodine to make hormones that control growth and the development "
  "of the brain.'",
  ["Find 'thyroid gland' in paragraph 2", "Read what it uses iodine for", "Hormones for growth and the brain"],
  "Removing extra salt, guarding against damp and heat, and digesting crops are never given as the gland's work; "
  "damp air and heat are mentioned only as causes of iodine loss from stored salt.", 35, P1, 1)

Q(RC, "Factual", B,
  "Why, according to the passage, is iodine deficiency common in hilly and flood-prone areas?",
  ["Rain and rivers have washed much of the iodine out of the soil.",
   "People in these areas do not like the taste of salt.",
   "Salt cannot be carried to these areas during the rains.",
   "The water in these areas destroys iodine in the body."], 0,
  "Locating a stated cause",
  "Paragraph 3: in such areas 'rain and rivers have washed much of the iodine out of the soil', so crops, and the "
  "people who eat them, get little iodine.",
  ["Find 'hilly regions' in paragraph 3", "Cause: iodine washed out of the soil", "Crops and people get little"],
  "The passage never says these people dislike salt, that salt cannot reach them, or that their water destroys "
  "iodine in the body.", 35, P1, 2)

Q(RC, "Factual", B,
  "Which of the following is NOT given in the passage as a reason why salt was chosen to carry iodine?",
  ["Rich and poor alike consume it.",
   "People eat it in roughly similar amounts.",
   "Adding iodine to it costs very little.",
   "It keeps its iodine for years even if left open."], 3,
  "Factual (NOT) question: eliminate every reason the passage gives",
  "Paragraph 4 gives three reasons: rich and poor eat salt, in roughly similar amounts, and iodising it costs only a "
  "few paise per kilogram. Paragraph 5 says the opposite of the last statement: iodine escapes from salt that is "
  "stored carelessly.",
  ["Rich and poor consume it: stated", "Similar amounts: stated", "Low cost: stated",
   "Keeps iodine when left open: contradicted in paragraph 5"],
  "Eating by rich and poor alike, similar amounts and low cost are all stated in paragraph 4, so none of them can "
  "be the answer.", 40, P1, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'norm' as used in the passage ('iodised salt became the "
  "norm in most households')?",
  ["the usual practice", "a rare luxury", "a strict rule", "a costly mistake"], 0,
  "Vocabulary in context: norm = what is usual or standard",
  "Over the decades iodised salt came to be used in most homes; it became the ordinary, expected thing, i.e. 'the "
  "usual practice'.",
  ["Context: 'in most households'", "Something most people do = usual", "'the usual practice'"],
  "Something found in most households is not 'a rare luxury'. No law is mentioned, so 'a strict rule' goes too far. "
  "The passage praises iodised salt, so 'a costly mistake' contradicts it.", 30, P1, 4)

Q(RC, "Inference", B,
  "Why does the passage advise keeping salt away from the stove?",
  ["Heat causes the iodine in the salt to escape.",
   "Salt near the stove attracts insects.",
   "The stove makes the salt taste bitter.",
   "Salt near the stove is easily spilt into food."], 0,
  "Inference: linking the advice to the reason given earlier",
  "Paragraph 5 says that damp air, heat and sunlight cause iodine to escape, so a packet left near the stove loses "
  "its value. The advice in the last paragraph follows from this.",
  ["Advice: keep salt away from the stove", "Earlier reason: heat makes iodine escape", "So heat must be avoided"],
  "Insects, taste and spilling are never mentioned; the only reason the passage gives is the loss of iodine.",
  35, P1, 5)

Q(RC, "Tone and title", B,
  "Which of the following is the most suitable title for the passage?",
  ["A Small Addition with a Big Benefit", "How Salt Is Made from Sea Water", "The Villages of the Himalayas",
   "Why Doctors Tell Us to Eat Less Salt"], 0,
  "Title: the idea that runs through the whole passage",
  "The passage explains why the body needs iodine, why salt was chosen to carry it, and how households can keep "
  "its benefit. A tiny addition to salt protects health: 'A Small Addition with a Big Benefit'.",
  ["Paras 1-3: iodine and the harm its lack causes", "Para 4: adding it to salt", "Paras 5-6: keeping its value"],
  "How salt is made is never described. Himalayan villages appear in one sentence only. The passage is not about "
  "eating less salt.", 35, P1, 6)

# ---------------------------------------------------------------- RC 2 (Basic 5 + Intermediate 1)
P2 = stim("Money nobody claims", (
    "Somewhere in the records of almost every Indian bank lies money that nobody seems to own. A savings account "
    "opened for a scholarship and then forgotten, a fixed deposit made by a grandfather who never told anyone about "
    "it, a salary account left behind when its holder moved to another city: such balances add up, across the "
    "country, to many thousands of crores of rupees.\n\n"
    "Money becomes unclaimed for ordinary reasons. People change jobs and towns and open new accounts without closing "
    "the old ones. Small balances seem too trivial to bother about. Most often, an account holder dies and the family "
    "simply does not know that the account exists. The passbook may lie in a trunk for years, or there may be no "
    "passbook at all.\n\n"
    "Banks do not keep this money for themselves. When an account has seen no transaction by its holder for a long "
    "time, the bank marks it as inactive and tries to reach the customer. If the deposit remains unclaimed for ten "
    "years, the bank transfers it to a fund maintained by the Reserve Bank of India. The money still belongs to the "
    "depositor. If the rightful owner or the legal heirs come forward, even many years later, the bank must pay it "
    "back.\n\n"
    "Claiming it, however, can be a tiring process. Heirs who were never named in the bank's records may have to "
    "produce a death certificate, proof of their relationship and sometimes papers from a court, which can take "
    "months to obtain.\n\n"
    "Much of this trouble can be avoided by one simple step: nomination. When opening an account or making a "
    "deposit, a customer can name a person, the nominee, to whom the bank will pay the money after the customer's "
    "death. Where a nominee is registered, the bank can usually settle the claim quickly and with far less "
    "paperwork. Yet many people leave the nomination form blank, either because they do not understand it or because "
    "they find it uncomfortable to think about death.\n\n"
    "The Reserve Bank has also set up a website on which people can search for unclaimed deposits held in their own "
    "names or in the names of family members. Still, the surest protection lies at home: keep a list of all your "
    "accounts, tell your family where the list is kept, and register a nominee for every one of them."))

Q(RC, "Factual", B,
  "Which of the following is NOT mentioned in the passage as a reason why money in bank accounts goes unclaimed?",
  ["People open new accounts in new towns without closing the old ones.",
   "Some balances are too small to seem worth claiming.",
   "The family of a dead account holder does not know the account exists.",
   "Banks refuse to let customers close their old accounts."], 3,
  "Factual (NOT) question: eliminate every reason the passage gives",
  "Paragraph 2 gives three reasons: people move and open new accounts, small balances seem trivial, and families "
  "do not know about a dead relative's account. Nothing is said about banks refusing to close accounts.",
  ["Moving without closing old accounts: stated", "Small balances seem trivial: stated",
   "Family unaware after a death: stated", "Banks refusing closure: not mentioned"],
  "Moving towns, trivial balances and unaware families are all named in paragraph 2, so none of them can be the "
  "answer.", 40, P2, 1)

Q(RC, "Factual", B,
  "According to the passage, what happens to a deposit that remains unclaimed for ten years?",
  ["The bank transfers it to a fund maintained by the Reserve Bank of India.",
   "The bank adds it to its own profits for that year.",
   "The government spends it on new branches in villages.",
   "The money is divided among the bank's other customers."], 0,
  "Locating a stated fact",
  "Paragraph 3: 'If the deposit remains unclaimed for ten years, the bank transfers it to a fund maintained by the "
  "Reserve Bank of India.'",
  ["Find 'ten years' in paragraph 3", "Read what the bank does", "Transfer to an RBI fund"],
  "The passage says banks do not keep the money, so it is not added to profits. Spending on new branches and "
  "sharing among other customers are never mentioned.", 35, P2, 2)

Q(RC, "Inference", B,
  "What can be understood from the passage about money that has been moved to the Reserve Bank's fund?",
  ["The owner or the legal heirs can still claim it, even years later.",
   "It can never be returned once it has been moved.",
   "It can be returned only if it is claimed within a month.",
   "Only the Reserve Bank can decide whom to give it to."], 0,
  "Inference from a stated fact",
  "Paragraph 3 says, right after describing the transfer, that 'The money still belongs to the depositor' and that "
  "the bank must pay it back if the owner or heirs come forward 'even many years later'.",
  ["Transfer to the fund: paragraph 3", "'The money still belongs to the depositor'",
   "Can be claimed 'even many years later'"],
  "'Never returned' and 'only within a month' contradict 'even many years later'. The passage says the bank must "
  "pay the rightful owner, not that the Reserve Bank chooses whom to pay.", 40, P2, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'trivial' as used in the passage ('Small balances seem "
  "too trivial to bother about')?",
  ["unimportant", "dangerous", "valuable", "complicated"], 0,
  "Vocabulary in context: trivial = of little importance",
  "People do not bother about small balances because the amounts seem too small to matter, i.e. 'unimportant'.",
  ["Context: small balances", "Not worth bothering about", "'unimportant'"],
  "A small balance is not 'dangerous'. 'Valuable' is the opposite of the sense. 'Complicated' does not explain why "
  "people would ignore a small sum.", 30, P2, 4)

Q(RC, "Factual", B,
  "According to the passage, how does registering a nominee help the family?",
  ["The bank can usually settle the claim quickly and with far less paperwork.",
   "The bank pays the family a higher rate of interest on the deposit.",
   "The family no longer has to pay any tax on the money.",
   "The account can never become inactive after a nominee is named."], 0,
  "Locating a stated fact",
  "Paragraph 5: 'Where a nominee is registered, the bank can usually settle the claim quickly and with far less "
  "paperwork.'",
  ["Find 'nominee' in paragraph 5", "Read what happens where one is registered", "Quick settlement, less paperwork"],
  "Higher interest, freedom from tax and accounts that never become inactive are not mentioned anywhere in the "
  "passage.", 35, P2, 5)

Q(RC, "Tone and title", I,
  "Which of the following best states the main purpose of the passage?",
  ["To explain why bank deposits go unclaimed and how families can avoid the problem",
   "To criticise banks for hiding unclaimed money from their customers",
   "To persuade people to keep their savings at home instead of in banks",
   "To describe how the Reserve Bank of India invests the money it receives"], 0,
  "Main purpose: what the passage as a whole sets out to do",
  "The passage describes how money becomes unclaimed, what banks do with it, why claiming it is hard, and how "
  "nomination, the search website and a list of accounts can prevent the problem. It explains and advises.",
  ["Paras 1-2: how money becomes unclaimed", "Paras 3-4: what happens to it; claims are tiring",
   "Paras 5-6: nomination and other remedies"],
  "The passage says banks do not keep the money and must pay it back, so it does not accuse them. It never advises "
  "keeping savings at home. How the Reserve Bank invests the fund is not discussed.", 40, P2, 6)

# ---------------------------------------------------------------- RC 3 (Intermediate, 6)
P3 = stim("What seventy per cent means", (
    "When the weather report says that there is a seventy per cent chance of rain tomorrow, what exactly is it "
    "promising? Surveys in several countries have found that people read such forecasts in surprisingly different "
    "ways. Some believe that it will rain for seventy per cent of the day. Others think that rain will fall over "
    "seventy per cent of the area. A good number simply round the figure up and treat it as a promise of rain.\n\n"
    "None of these readings is correct. The figure means that, at any given spot in the forecast area, there is a "
    "seven-in-ten chance of at least some measurable rain during the period. Put another way, if the same forecast "
    "were issued on a hundred days with similar conditions, rain would be expected on about seventy of them, and on "
    "the other thirty it would stay dry.\n\n"
    "Where does such a number come from? The atmosphere is so sensitive that a tiny error in today's measurements "
    "can grow into a large error in tomorrow's forecast. Forecasters therefore often run their computer models many "
    "times, each time starting from slightly different conditions. If most of these runs produce rain at a place, "
    "the chance of rain there is high; if only a few do, it is low.\n\n"
    "This has an uncomfortable consequence for forecasters. A dry day after a forecast of seventy per cent does not "
    "prove that the forecast was wrong; three days in ten are expected to be dry. Yet people tend to remember such "
    "days as failures. The fair way to judge a forecaster is over many forecasts: of all the days for which she "
    "predicted a seventy per cent chance, did it actually rain on roughly seventy per cent? A forecaster whose "
    "figures pass this test is said to be well calibrated, even if she is sometimes 'wrong' on a particular day.\n\n"
    "A probability is also more useful than a plain yes or no, because different people can act on it differently. "
    "A family planning an outdoor wedding, for whom rain would be a disaster, may hire a tent even when the chance "
    "is only thirty per cent. A farmer deciding whether to spray his crop, which a shower would wash off, may wait "
    "unless the chance is very low. The same forecast, rightly understood, leads sensible people to different "
    "decisions."))

# The calibration question: each forecaster said 'seventy per cent' on 40 days; only one record matches 70%.
CAL_OPTS = ["rain fell on 28 of the 40 days", "rain fell on 40 of the 40 days", "rain fell on 12 of the 40 days",
            "rain fell on 20 of the 40 days"]
CAL_OK = [k for k in CAL_OPTS if Fraction(int(k.split()[3]), int(k.split()[6])) == Fraction(70, 100)]
assert CAL_OK == [CAL_OPTS[0]]

Q(RC, "Factual", I,
  "According to the passage, what does a forecast of 'a seventy per cent chance of rain' actually mean?",
  ["At any spot in the area there is a seven-in-ten chance of some measurable rain.",
   "Rain will fall for about seventy per cent of the hours in the day.",
   "Rain will fall over about seventy per cent of the forecast area.",
   "Rain is certain, and it will be heavier than on an ordinary day."], 0,
  "Locating the stated definition and rejecting the common misreadings",
  "Paragraph 2: 'at any given spot in the forecast area, there is a seven-in-ten chance of at least some measurable "
  "rain during the period.'",
  ["Paragraph 1 lists the common misreadings", "Paragraph 2: 'None of these readings is correct'",
   "Correct meaning: seven-in-ten chance at any spot"],
  "Seventy per cent of the day, seventy per cent of the area and a promise of rain are exactly the misreadings that "
  "paragraph 2 rejects.", 40, P3, 1)

Q(RC, "Inference", I,
  "Why, according to the passage, do forecasters run their computer models many times?",
  ["Their starting measurements are never perfect, so they test many slightly different starts.",
   "Computers often break down, so each run has to be repeated to get any result at all.",
   "Each run covers only one town, so many runs are needed to cover a whole country.",
   "People do not trust a single run, so repeated runs are made to persuade the public."], 0,
  "Inference: the reason stated in the same paragraph",
  "Paragraph 3: the atmosphere is so sensitive that 'a tiny error in today's measurements can grow into a large "
  "error'. Forecasters 'therefore' run the models many times from slightly different conditions, and the share of "
  "runs that give rain sets the chance.",
  ["Problem: small errors grow", "'Therefore': many runs from slightly different starts",
   "Share of rainy runs → chance of rain"],
  "Breakdowns, one-town coverage and persuading the public are never mentioned; the passage links repeated runs to "
  "the growth of small errors.", 45, P3, 2)

Q(RC, "Inference", I,
  "Four forecasters each predicted 'a seventy per cent chance of rain' on 40 days. Going by the test described in "
  "the passage, whose record shows that he or she is well calibrated?",
  ["The one for whose forecasts " + k for k in CAL_OPTS], 0,
  "Applying the calibration test: the share of rainy days should match the forecast figure",
  "A well-calibrated forecaster's seventy per cent days should turn out rainy about seventy per cent of the time. "
  "Seventy per cent of 40 days = 28 days, so the record '28 of the 40 days' passes the test.",
  ["Test: share of rainy days ≈ forecast figure", "70% of 40 = 28", "28 of 40 matches"],
  "Rain on all 40 days (100%) means the figure was too low, 12 of 40 is 30% and 20 of 40 is 50%; none of these "
  "matches seventy per cent. Rain on every day may feel like success, but the passage judges the match between the "
  "figure and the outcome.", 60, P3, 3, shortcut="0.7 × 40 = 28")

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'sensitive' as used in the passage ('The atmosphere is "
  "so sensitive that a tiny error ... can grow into a large error')?",
  ["easily affected by small changes", "likely to be hurt by criticism", "kept secret from the public",
   "able to detect faint sounds"], 0,
  "Vocabulary in context: one word, several senses; the clause after 'so ... that' fixes the sense",
  "The atmosphere is called sensitive because a tiny difference in the starting measurements can produce a large "
  "difference later. In this sense, 'sensitive' means easily affected by small changes.",
  ["'so sensitive that a tiny error can grow'", "Small cause, large effect", "'easily affected by small changes'"],
  "'Hurt by criticism' and 'kept secret' are other senses of 'sensitive' that do not suit the atmosphere. 'Able to "
  "detect faint sounds' describes an instrument or an ear, not the weather.", 35, P3, 4)

Q(RC, "Inference", I,
  "Why might the family planning a wedding and the farmer in the last paragraph act differently on the same "
  "forecast?",
  ["Rain would ruin the wedding, while for the farmer it would only waste one spraying.",
   "The family trusts weather forecasts, while the farmer does not believe them at all.",
   "The family receives a different forecast from the one the farmer receives.",
   "The farmer wants his crop to be washed by the rain before he sprays it."], 0,
  "Inference: decisions depend on the cost of being caught by rain, not on the forecast alone",
  "For the family, rain would be 'a disaster', so even a thirty per cent chance justifies a tent. For the farmer, a "
  "shower would only wash off the spray, so he can wait for a day when the chance is very low. The cost of each "
  "mistake differs.",
  ["Wedding: rain = disaster → act even at 30%", "Farmer: rain wastes the spray → spray only when the chance is "
   "low", "Same forecast, different costs → different decisions"],
  "The passage says both act on 'the same forecast', so a different forecast or distrust is not the reason. The "
  "farmer wants to avoid rain washing off the spray, not to have the crop washed.", 45, P3, 5)

Q(RC, "Tone and title", I,
  "Which of the following is the most suitable title for the passage?",
  ["Reading the Odds in a Weather Forecast", "Why the Monsoon Arrives Late", "Weddings in the Rainy Season",
   "How Computers Replaced Weather Stations"], 0,
  "Title: the idea that runs through every paragraph",
  "The passage explains what a percentage chance of rain means, where it comes from, how forecasters should be "
  "judged and how people can use it. Its subject is understanding the probability in a forecast.",
  ["Paras 1-2: what the figure means", "Para 3: where it comes from", "Paras 4-5: judging and using it"],
  "The monsoon is never discussed. The wedding is one example in the last paragraph. Computers are mentioned only "
  "as tools for running models, not as replacing weather stations.", 35, P3, 6)

# ---------------------------------------------------------------- RC 4 (Intermediate, 6)
P4 = stim("Why the work always takes longer", (
    "Almost everyone has had the experience. A report that was supposed to take a weekend takes a fortnight; a "
    "kitchen that was to be rebuilt in a month is still full of dust after three. Large projects show the same "
    "pattern on a grander scale. Flyovers, metro lines and new airports routinely open years after their promised "
    "dates and at costs well above their original budgets.\n\n"
    "Psychologists have a name for this tendency: the planning fallacy. It describes our habit of underestimating "
    "how long our own tasks will take, even when we know that similar tasks in the past took longer than planned. In "
    "one well-known study, students were asked to estimate when they would finish their final-year thesis, and also "
    "to give a 'worst-case' estimate in case everything went badly. On average, they took longer than even their "
    "worst-case estimate.\n\n"
    "Why do people who are otherwise sensible keep making the same mistake? Part of the answer lies in how we plan. "
    "When we think about a task, we picture the particular steps it requires and imagine them going roughly as "
    "intended. This is called taking the 'inside view'. What we leave out are the many things that are not part of "
    "the plan at all: an illness, a delayed supplier, a sudden demand from the boss. Each of these is unlikely on its "
    "own, but over a long project it is almost certain that some of them will happen.\n\n"
    "Memory makes matters worse. When a past project overran, we tend to explain the delay as a special case (the "
    "rains came early, a key worker resigned) rather than as a sign of how projects usually go. Having explained the "
    "delay away, we expect the next project to run smoothly.\n\n"
    "The most effective remedy is to take the 'outside view'. Instead of starting from the details of the plan, a "
    "planner first asks how long similar projects actually took, and then adjusts that figure for anything that "
    "makes the present case genuinely different. Some governments now require planners of large public works to "
    "compare their estimates with the record of comparable projects before a budget is approved.\n\n"
    "Curiously, people are often better at predicting how long other people's tasks will take than their own. Asked "
    "about a colleague's project, we naturally think of the colleague's past record; asked about our own, we think "
    "of our plan. The best forecast for one's own work may come from imagining that it belongs to someone else."))

Q(RC, "Factual", I,
  "What did the study of students' final-year theses described in the passage find?",
  ["On average, they finished later than their own estimate for things going badly.",
   "Most students finished well before the dates they had first estimated.",
   "Students who gave worst-case estimates always finished on time.",
   "The students' estimates were accurate, but their teachers' were not."], 0,
  "Locating a stated finding",
  "Paragraph 2: 'On average, they took longer than even their worst-case estimate.'",
  ["Find 'thesis' in paragraph 2", "Read the result", "Longer than even the worst case"],
  "Finishing early, always finishing on time and accurate estimates all contradict the finding; teachers' estimates "
  "are not mentioned.", 40, P4, 1)

Q(RC, "Inference", I,
  "According to the passage, what does taking the 'inside view' of a task involve?",
  ["Imagining one's own planned steps working out more or less as expected",
   "Asking how long similar projects carried out by others actually took",
   "Adding a fixed margin of extra time to every estimate one makes",
   "Discussing the plan with colleagues before deciding on a date"], 0,
  "Understanding a term defined in the passage",
  "Paragraph 3: 'we picture the particular steps it requires and imagine them going roughly as intended. This is "
  "called taking the \"inside view\".'",
  ["Find 'inside view' in paragraph 3", "It is defined by the sentence before it", "Picturing one's own steps going "
   "to plan"],
  "Checking how long similar projects took is the 'outside view' of paragraph 5. Adding a margin and consulting "
  "colleagues are not what the passage calls the inside view.", 40, P4, 2)

Q(RC, "Inference", I,
  "Why, according to the passage, are unplanned events such as an illness or a delayed supplier so damaging to "
  "estimates?",
  ["Any one of them is improbable, but on a long job a few are bound to occur.",
   "They happen only on large public projects, which planners cannot control.",
   "Each of them is very likely to happen on every single day of a project.",
   "Planners include them in their plans, which makes the plans too long."], 0,
  "Inference: the reasoning in paragraph 3",
  "The passage says each such event 'is unlikely on its own, but over a long project it is almost certain that "
  "some of them will happen'. Because the inside view leaves them out, the estimate is too short.",
  ["Unplanned events are left out of the plan", "Each is unlikely, but together they are near-certain",
   "So estimates that ignore them are too short"],
  "The passage gives everyday examples, so they are not limited to public projects. It calls each event unlikely, "
  "not likely every day. The problem is that planners leave such events out, not that they include them.",
  45, P4, 3)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'routinely' as used in the passage ('new airports "
  "routinely open years after their promised dates')?",
  ["regularly, as a matter of course", "suddenly, without any warning", "rarely, only in special cases",
   "deliberately, in order to save money"], 0,
  "Vocabulary in context: routinely = as a normal, regular occurrence",
  "The passage says large projects show 'the same pattern', so late openings are the normal state of affairs: they "
  "happen regularly, as a matter of course.",
  ["Context: 'the same pattern on a grander scale'", "Late openings are usual", "'regularly, as a matter of "
   "course'"],
  "'Rarely' is the opposite of the sense. Nothing suggests the delays are sudden or deliberate; the passage treats "
  "them as a common pattern.", 30, P4, 4)

Q(RC, "Inference", I,
  "Which of the following is an example of the 'outside view' as the passage describes it?",
  ["A builder checks how long the last ten school buildings in the district really took before quoting a date.",
   "A builder lists every step of the new building and adds up the time each step should take.",
   "A builder promises an early date because his workers are more skilled than those of his rivals.",
   "A builder ignores his past delays because each had a special cause, such as early rains."], 0,
  "Applying a concept: the outside view starts from the record of similar projects",
  "Paragraph 5: the planner 'first asks how long similar projects actually took'. Checking the actual time taken by "
  "ten similar school buildings is exactly this.",
  ["Outside view: start from how long similar projects took", "Ten past school buildings = similar projects",
   "Then adjust for real differences"],
  "Listing the steps is the inside view. Trusting one's own workers' skill also starts from the details of the "
  "present case. Explaining away past delays as special cases is the error described in paragraph 4.", 45, P4, 5)

Q(RC, "Inference", I,
  "What does the author suggest in the last paragraph?",
  ["Picturing one's own task as someone else's may give a truer estimate.",
   "People should ask their colleagues to do their own work for them.",
   "Colleagues' tasks always take longer to finish than one's own tasks.",
   "One should never try to estimate how long one's own work will take."], 0,
  "Inference: the conclusion the author draws",
  "When we judge others' tasks we think of their past record (the outside view), not their plan. So imagining our "
  "own task as someone else's may push us to use the record too: 'The best forecast ... may come from imagining "
  "that it belongs to someone else.'",
  ["Others' tasks → we think of their record", "Own task → we think of our plan",
   "So treat one's own task as another's"],
  "The author suggests imagining, not handing the work to colleagues. Nothing says colleagues' tasks take longer. "
  "The author wants better estimates, not no estimates.", 40, P4, 6)

# ---------------------------------------------------------------- RC 5 (Intermediate 1 + Advanced 5)
P5 = stim("The pull of the average", (
    "Many years ago, a psychologist was telling a group of flight instructors that praise teaches better than "
    "punishment. One of the instructors objected. In his experience, he said, when he praised a trainee pilot for an "
    "unusually smooth landing, the next landing was usually worse; when he shouted at a trainee after a rough one, "
    "the next was usually better. Praise, he concluded, made pilots careless, and criticism made them try harder.\n\n"
    "His observation was accurate, but his conclusion was not. Any skill performed again and again varies from one "
    "attempt to the next. Part of the variation reflects real ability, and part is simply luck: a gust of wind, a "
    "moment's distraction. An unusually good landing is likely to have been helped by good luck as well as skill, "
    "and luck does not repeat on demand. The next landing will therefore tend to be closer to the trainee's normal "
    "standard, that is, worse, whatever the instructor says. In the same way, an unusually bad landing is likely to "
    "be followed by a better one. Statisticians call this pattern regression to the mean.\n\n"
    "The instructor had been fooled because his words always came at the extremes. He praised only after the best "
    "landings and shouted only after the worst, so the natural movement back towards the average looked like the "
    "effect of his words.\n\n"
    "The same trap appears in many places. Patients tend to visit a doctor when their symptoms are at their worst, "
    "and many would improve in the following days even if they did nothing; whatever remedy they took gets the "
    "credit. A school that gives extra coaching to the students who did worst in one test will usually find that "
    "their next scores rise, even if the coaching is useless. A city that installs speed cameras at the junctions "
    "with the most accidents last year will probably see accidents there fall, partly because last year's figures "
    "were unusually high.\n\n"
    "None of this means that coaching, medicines or speed cameras do not work. It means that a simple before-and-"
    "after comparison cannot tell us whether they do. To judge the true effect, we need a comparison group: similar "
    "patients who did not take the remedy, or similar junctions, chosen in the same way, where no cameras were "
    "installed. Only the difference between the two groups shows what the measure itself achieved."))

Q(RC, "Factual", I,
  "What did the flight instructor conclude from his experience?",
  ["Praise led to carelessness, while shouting pushed pilots to greater effort.",
   "Praise and criticism had no effect at all on how pilots landed.",
   "Pilots landed better on calm days than on windy ones.",
   "Trainee pilots needed more hours of practice before flying alone."], 0,
  "Locating a stated conclusion",
  "Paragraph 1: 'Praise, he concluded, made pilots careless, and criticism made them try harder.'",
  ["Find 'concluded' in paragraph 1", "Read his conclusion", "Praise → careless; criticism → try harder"],
  "That praise and criticism had no effect is the psychologist's explanation, not the instructor's belief. Wind and "
  "practice hours are not part of his conclusion.", 35, P5, 1)

Q(RC, "Inference", A,
  "Why, according to the passage, was the instructor misled?",
  ["His praise and criticism came only after extreme landings, so the usual drift back to normal looked like their "
   "effect.",
   "He praised the trainees too often, so they stopped paying attention to anything he said.",
   "He remembered the rough landings more clearly than the smooth ones, so he misjudged his trainees.",
   "His trainees practised in very different weather, so their landings could not be compared."], 0,
  "Inference: identifying the cause of a mistaken conclusion",
  "Paragraph 3: 'his words always came at the extremes ... so the natural movement back towards the average looked "
  "like the effect of his words.' Extreme landings are partly luck, so the next one tends to be more ordinary "
  "whatever he says.",
  ["Feedback only after the best and worst landings", "Next landing drifts back to normal anyway",
   "The drift was mistaken for the effect of the feedback"],
  "Praising too often contradicts 'praised only after the best landings'. Selective memory and weather differences "
  "are not the explanation the passage gives.", 50, P5, 2)

Q(RC, "Inference", A,
  "Which of the following is the best example of regression to the mean as the passage describes it?",
  ["A batsman whose average is 40 scores a career-best 180, and then scores 45 in his next innings.",
   "A batsman who practises harder every season raises his average from 30 to 45 over five years.",
   "A batsman scores less and less every season as an old knee injury slowly gets worse.",
   "A batsman scores exactly his average of 40 in every one of his twenty innings."], 0,
  "Applying a concept: an extreme result followed by one closer to the usual level",
  "A career-best 180 is an extreme result, helped by luck as well as skill. The next score, 45, falls back close to "
  "his normal average of 40, without any change in ability. That is regression to the mean.",
  ["Extreme result: 180 against an average of 40", "Next result: 45, near the average",
   "No change in ability needed → regression to the mean"],
  "Steady improvement through practice and a steady decline through injury are real changes in ability, not a "
  "drift back after an extreme. Scoring exactly 40 every time shows no extreme result at all.", 50, P5, 3)

Q(RC, "Inference", A,
  "What does the author imply about the city that installed speed cameras at its most dangerous junctions?",
  ["A fall in accidents there does not, by itself, show how much the cameras helped.",
   "The cameras were useless and the money should have been spent elsewhere.",
   "Accidents at those junctions will certainly rise again once the cameras are removed.",
   "The city chose the junctions wrongly, because last year's figures were false."], 0,
  "Inference: the author's qualified position",
  "Paragraph 4 says accidents will 'probably' fall 'partly because last year's figures were unusually high'. "
  "Paragraph 5 adds that this does not mean cameras do not work, only that a before-and-after comparison cannot "
  "tell us; comparable junctions without cameras are needed.",
  ["Junctions chosen at an extreme year", "Some fall would happen anyway", "Need a comparison group to measure the "
   "real effect"],
  "The author says plainly that this does not mean cameras do not work. Nothing predicts what happens when cameras "
  "are removed. Last year's figures were unusually high, not false.", 50, P5, 4)

Q(RC, "Vocabulary in context", A,
  "As used in the passage ('luck does not repeat on demand'), the phrase 'on demand' means",
  ["whenever it is wanted", "at a high price", "after a long delay", "under a legal order"], 0,
  "Vocabulary in context: on demand = as soon as or whenever it is asked for",
  "Good luck helped the smooth landing, but the trainee cannot call it up again whenever he wants it; luck does not "
  "come back 'on demand'.",
  ["Context: luck helped one landing", "It cannot be produced again at will", "'whenever it is wanted'"],
  "'At a high price' and 'under a legal order' are senses linked to demand in trade and law, not here. 'After a "
  "long delay' says nothing about luck being available at will.", 35, P5, 5)

Q(RC, "Tone and title", A,
  "Which of the following best describes the tone of the passage?",
  ["explanatory and cautionary", "angry and accusing", "humorous and light-hearted", "sentimental and nostalgic"],
  0,
  "Tone: how the author treats the subject",
  "The author explains a statistical pattern with examples and warns readers not to trust simple before-and-after "
  "comparisons. That is explanatory and cautionary.",
  ["Explains: luck, extremes, regression to the mean", "Warns: before-and-after comparisons mislead",
   "→ explanatory and cautionary"],
  "The author does not attack the instructor or anyone else, so the tone is not angry. The subject is treated "
  "seriously, not as a joke, and there is no longing for the past.", 35, P5, 6)

# ---------------------------------------------------------------- RC 6 (Advanced, 4)
POP, ILL_RATE = 100000, Fraction(1, 1000)
SENS, FALSE_POS = Fraction(99, 100), Fraction(5, 100)
ILL = POP * ILL_RATE
TRUE_POS = ILL * SENS
FALSE_POS_N = (POP - ILL) * FALSE_POS
assert (ILL, TRUE_POS, POP - ILL, FALSE_POS_N, TRUE_POS + FALSE_POS_N) == (100, 99, 99900, 4995, 5094)
assert TRUE_POS / (TRUE_POS + FALSE_POS_N) < Fraction(2, 100)
assert 19 < (TRUE_POS / (TRUE_POS + FALSE_POS_N)) / ILL_RATE < 20          # 'nearly twenty-fold'
# the question: same test, but the disease affects 1 in 100
ILL2 = POP * Fraction(1, 100)
SHARE2 = ILL2 * SENS / (ILL2 * SENS + (POP - ILL2) * FALSE_POS)
assert (ILL2 * SENS, (POP - ILL2) * FALSE_POS) == (990, 4950) and SHARE2 == Fraction(1, 6)

P6 = stim("A positive result", (
    "Suppose a disease affects one person in every thousand, and a screening test for it is quite accurate: it "
    "correctly detects 99 of every 100 people who have the disease, but it also wrongly flags 5 of every 100 healthy "
    "people. A man takes the test and the result is positive. How worried should he be?\n\n"
    "Most people, including many doctors when they are asked such questions, guess that he very probably has the "
    "disease, perhaps with a chance of 95 per cent. The real answer is surprisingly different. Imagine that 1,00,000 "
    "people are tested. About 100 of them have the disease, and the test flags 99 of these. Of the remaining 99,900 "
    "healthy people, 5 in every 100, or 4,995, are also flagged. Altogether, 5,094 people test positive, and only 99 "
    "of them are actually ill. A positive result therefore means a chance of fewer than 2 in 100 that the man has the "
    "disease.\n\n"
    "The mistake people make is to ignore how rare the disease is to begin with, a figure statisticians call the "
    "base rate. Because healthy people vastly outnumber sick ones, even a small error rate among the healthy produces "
    "far more false alarms than there are true cases. The test's accuracy, quoted on its own, hides this.\n\n"
    "This does not make screening useless. A positive result raises the man's chance of being ill from 1 in 1,000 to "
    "nearly 2 in 100, a nearly twenty-fold increase, which is good reason for a second, more precise test. What it "
    "does mean is that the first result should be treated as a reason for further checks, not as a diagnosis. It "
    "also explains why doctors are often cautious about testing large numbers of people for rare conditions: the "
    "anxiety, cost and sometimes risky follow-up procedures suffered by the many healthy people who are wrongly "
    "flagged can outweigh the benefit to the few who are truly ill.\n\n"
    "The same reasoning applies far beyond medicine. A fraud-detection system at a bank, an airport scanner or any "
    "filter that hunts for rare problems among millions of ordinary cases will, unless it is extraordinarily "
    "precise, raise far more false alarms than real ones."))

Q(RC, "Inference", A,
  "According to the passage, why do most of the positive results in the example come from healthy people?",
  ["Healthy people so outnumber sick ones that a small error rate among them yields many false alarms.",
   "The test is much better at detecting the disease in healthy people than in sick ones.",
   "Most people who take the test have already been told by a doctor that they are ill.",
   "The disease often disappears on its own between the test and the result."], 0,
  "Inference: the base-rate reasoning in paragraph 3",
  "There are 99,900 healthy people and only 100 sick ones. Flagging just 5 in 100 healthy people gives 4,995 false "
  "alarms, far more than the 99 true cases. Paragraph 3 states this reason.",
  ["Healthy: 99,900; sick: 100", "5% of 99,900 = 4,995 false alarms vs 99 true cases",
   "Rarity of the disease → most positives are false"],
  "The test detects 99 of every 100 sick people; it does not 'detect the disease' in healthy people better. Prior "
  "diagnosis and recovery between test and result are never mentioned.", 50, P6, 1)

Q(RC, "Inference", A,
  "Suppose the same test (detecting 99 of every 100 sick people and wrongly flagging 5 of every 100 healthy people) "
  "were used for a disease that affects 1 person in every 100. Using the method of the passage, roughly what share "
  "of the people who test positive would actually be ill?",
  ["about 1 in 6", "about 99 in 100", "about 1 in 50", "about 95 in 100"], 0,
  "Applying the passage's method (count people, not percentages) to a new base rate",
  "Out of 1,00,000 people, 1,000 are ill and the test flags 990 of them. Of the 99,000 healthy people, 5 in 100 = "
  "4,950 are flagged. Positives = 990 + 4,950 = 5,940, of whom 990 are ill: 990/5,940 = 1/6.",
  ["Ill: 1% of 1,00,000 = 1,000 → 990 flagged", "Healthy: 99,000 → 5% = 4,950 flagged",
   "Share ill = 990 / (990 + 4,950) = 990/5,940 = 1/6"],
  "'About 99 in 100' and 'about 95 in 100' confuse the test's accuracy with the chance that a positive person is "
  "ill, the very error the passage warns against. 'About 1 in 50' is the passage's own answer for the rarer "
  "disease, before the base rate was changed.", 90, P6, 2, shortcut="Positives ≈ 990 true + 4,950 false; 990 is one "
  "sixth of 5,940")

Q(RC, "Inference", A,
  "According to the author, how should a first positive result from such a screening test be treated?",
  ["As a reason for a second, more precise test rather than as a diagnosis",
   "As proof that the person certainly has the disease and needs treatment",
   "As a meaningless result, since the test cannot be trusted at all",
   "As a sign that the screening test should be stopped for everyone"], 0,
  "Inference: the author's conclusion in paragraph 4",
  "Paragraph 4: 'the first result should be treated as a reason for further checks, not as a diagnosis', since it "
  "raises the chance of illness nearly twenty-fold and justifies 'a second, more precise test'.",
  ["Positive result raises the chance nearly twenty-fold", "But the chance is still under 2 in 100",
   "→ further checks, not a diagnosis"],
  "Treating the result as proof is the mistake the passage corrects. Calling it meaningless or stopping screening "
  "contradicts 'This does not make screening useless'.", 45, P6, 3)

Q(RC, "Vocabulary in context", A,
  "Which of the following is closest in meaning to the word 'outweigh' as used in the passage ('can outweigh the "
  "benefit to the few who are truly ill')?",
  ["be greater than", "be equal to", "be hidden by", "be paid for by"], 0,
  "Vocabulary in context: outweigh = be greater or more important than",
  "The author explains why doctors are cautious: the harm done to many wrongly flagged healthy people can be "
  "greater than the good done to the few sick ones. To 'outweigh' is to be greater than.",
  ["Two things compared: harm to many vs benefit to few", "The harm can be larger", "'be greater than'"],
  "'Be equal to' would give doctors no reason for caution. 'Be hidden by' and 'be paid for by' do not express a "
  "comparison of size.", 30, P6, 4)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic, 6)
C1 = stim("Twenty seconds at the tap", (
    "Washing hands with soap is one of the simplest ways to stay healthy. Doctors say that the habit can "
    "(1) ______ many common illnesses, such as diarrhoea and colds, which spread when germs travel from dirty hands "
    "to the mouth, nose or eyes.\n\n"
    "Many people believe that rinsing their hands with water is enough. It is not. Germs (2) ______ to the natural "
    "oils on our skin, and water alone slides over these oils without removing them. Soap breaks up the oil, so that "
    "the germs can be washed away.\n\n"
    "How we wash also matters. Hands should be rubbed together with soap for at least twenty seconds, which is about "
    "as long as it takes to hum a short song twice. The backs of the hands, the spaces between the fingers and the "
    "area under the nails are easily (3) ______, and germs often hide there.\n\n"
    "The most important moments to wash are before eating, before cooking or feeding a child, and after using the "
    "toilet. Health workers in many villages now teach children to (4) ______ these moments with simple rhymes and "
    "with pictures painted on school walls.\n\n"
    "Some schools have gone further. They have built long rows of taps near the dining area, so that a whole class "
    "can wash at once before the midday meal. Teachers report that children who once (5) ______ the task now rush to "
    "the taps, and that fewer pupils stay at home because of stomach infections.\n\n"
    "The habit costs very little. A bar of soap is cheap, and where running water is not (6) ______, a simple tap "
    "made from a hanging plastic bottle can be enough. It is hard to think of any other medicine that does so much "
    "good for so little money."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["prevent", "cause", "enjoy", "measure"], 0,
  "Cloze: the effect of a healthy habit on illness",
  "The passage praises handwashing as a way 'to stay healthy'. A healthy habit stops illnesses from happening: it "
  "can 'prevent' them.",
  ["'one of the simplest ways to stay healthy'", "So the habit stops illness", "'prevent'"],
  "A habit that keeps people healthy does not 'cause' illness. Illnesses are not 'enjoyed', and 'measure' says "
  "nothing about keeping them away.", 20, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["stick", "speak", "travel", "point"], 0,
  "Cloze: why water alone does not remove germs",
  "Water slides over the oils 'without removing them', so the germs stay held by the oils. Germs 'stick to' the "
  "oils on the skin.",
  ["Water alone fails", "Because germs are held by the skin's oils", "'stick to'"],
  "Germs do not 'speak' or 'point' to oils. 'Travel to the oils' does not explain why water fails to remove them.",
  20, C1, 2)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=3), ["missed", "painted", "praised", "borrowed"], 0,
  "Cloze: the parts of the hand that are overlooked",
  "The backs of the hands, the spaces between the fingers and the area under the nails are places people forget to "
  "wash, which is why 'germs often hide there'. They are easily 'missed'.",
  ["'germs often hide there'", "These places are not washed properly", "'easily missed'"],
  "Hands are not 'painted', 'praised' or 'borrowed' while washing; none of these explains why germs hide there.",
  20, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["remember", "forget", "count", "hide"], 0,
  "Cloze: the purpose of rhymes and pictures",
  "Rhymes and pictures on school walls are memory aids. They help children 'remember' the moments when they must "
  "wash their hands.",
  ["Tools: rhymes and pictures", "Purpose: keep the moments in mind", "'remember'"],
  "Health workers would not teach children to 'forget' or 'hide' the moments. 'Count' the moments does not suit "
  "rhymes meant to build a habit.", 20, C1, 4)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=5), ["avoided", "invented", "ordered", "enjoyed"], 0,
  "Cloze: 'once ... now' signals a change of behaviour",
  "'Children who once ___ the task now rush to the taps' contrasts their past and present attitudes. Children who "
  "now rush to wash once kept away from it: they 'avoided' the task.",
  ["'once' vs 'now' = contrast", "Now: rush to the taps", "Before: kept away → 'avoided'"],
  "If they had 'enjoyed' the task, there would be no change to report. Children did not 'invent' or 'order' "
  "handwashing.", 20, C1, 5)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=6), ["available", "heavy", "noisy", "silent"], 0,
  "Cloze: when a substitute tap is needed",
  "A tap made from a hanging bottle is a substitute used where there is no running water: where it is not "
  "'available'.",
  ["Substitute: a bottle tap", "Needed where running water cannot be had", "'not available'"],
  "Whether water is 'heavy', 'noisy' or 'silent' has nothing to do with needing a bottle tap.", 20, C1, 6)

# ---------------------------------------------------------------- Cloze 2 (Intermediate, 5)
C2 = stim("One clock for a wide country", (
    "All of India runs on a single clock. Indian Standard Time, five and a half hours ahead of Greenwich, is based "
    "on a line of longitude that (1) ______ near Mirzapur in Uttar Pradesh, roughly in the middle of the country. "
    "Whether one lives in Kutch or in Arunachal Pradesh, the clock on the wall shows the same time.\n\n"
    "The country, however, is wide. From its western edge to its eastern edge it stretches across nearly thirty "
    "degrees of longitude, and the sun rises almost two hours earlier in the far east than in the far west. In the "
    "north-east, summer dawn can break before four in the morning, and by the time offices and schools open by the "
    "clock, several hours of daylight have already been (2) ______. In the evening, the sun sets early, and homes "
    "and offices must switch on their lights, which adds to the demand for electricity.\n\n"
    "For this reason, there have long been calls for a second time zone for the north-eastern states. Supporters "
    "point out that the tea gardens of Assam have, since colonial days, followed their own local clock, set about an "
    "hour ahead of Indian Standard Time, so that work can begin soon after sunrise. They argue that a separate zone "
    "would let people make better use of daylight and would (3) ______ electricity.\n\n"
    "Opponents are not convinced. They fear that two time zones would cause confusion in railway and airline "
    "timetables, where a mistake about the time can have serious (4) ______. Some also argue that a single clock is "
    "a symbol of national unity.\n\n"
    "Between these positions lies a middle course that has attracted growing attention: keep one time zone, but "
    "allow states in the east to (5) ______ their office and school hours, opening and closing earlier than the rest "
    "of the country. Such a change would capture much of the benefit of a new zone without redrawing the national "
    "clock."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["passes", "begins", "stops", "settles"], 0,
  "Cloze: how a line of longitude relates to a place",
  "A line of longitude runs from pole to pole, so it does not begin or stop at a town; it 'passes' near it. IST is "
  "based on the line that passes near Mirzapur.",
  ["Line of longitude: runs north-south across the whole globe", "It crosses places, it does not end in them",
   "'passes near Mirzapur'"],
  "A line of longitude neither 'begins' nor 'stops' near a town, and lines do not 'settle'. Only 'passes' describes "
  "a line running past a place.", 30, C2, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["wasted", "saved", "earned", "stored"], 0,
  "Cloze: the cost of opening late by the sun's clock",
  "Dawn breaks before four, but offices open hours later by the clock, so those early hours of daylight go unused. "
  "They have been 'wasted', which is the problem the paragraph describes.",
  ["Dawn before 4 a.m.", "Offices open hours later", "Daylight goes unused → 'wasted'"],
  "Daylight that passes before work starts is not 'saved', 'earned' or 'stored'; each of these turns the problem "
  "into a benefit, while the paragraph is listing costs.", 30, C2, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["save", "consume", "waste", "measure"], 0,
  "Cloze: the benefit claimed by supporters",
  "Paragraph 2 said early sunsets add to the demand for electricity. Supporters argue that a separate zone would "
  "make better use of daylight and so reduce that demand: it would 'save' electricity.",
  ["Problem: early sunset → more electricity for lights", "Supporters' remedy: separate zone", "Benefit: 'save "
   "electricity'"],
  "'Consume' and 'waste' would make the supporters argue against their own proposal. 'Measure' electricity is not "
  "a benefit of a time zone.", 30, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["consequences", "rewards", "intentions", "origins"], 0,
  "Cloze: what follows from a mistake in a timetable",
  "Opponents fear confusion in railway and airline timetables, where a mistake about the time can lead to serious "
  "results such as missed connections or accidents. Results of an action are its 'consequences'.",
  ["Context: opponents' fear", "A timetable mistake → serious results", "'serious consequences'"],
  "A mistake does not have serious 'rewards'. 'Intentions' and 'origins' come before an action, not after it, so "
  "they cannot express the danger the opponents fear.", 30, C2, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["advance", "postpone", "abolish", "conceal"], 0,
  "Cloze: the phrase after the blank explains it",
  "The words that follow, 'opening and closing earlier than the rest of the country', show that the hours would be "
  "moved earlier. To move a time earlier is to 'advance' it.",
  ["Explanation: 'opening and closing earlier'", "Moving hours earlier", "'advance'"],
  "'Postpone' would move the hours later, the opposite of 'earlier'. Offices cannot 'abolish' or 'conceal' their "
  "hours and still open earlier.", 30, C2, 5)

# ---------------------------------------------------------------- Cloze 3 (Advanced, 6; error-based)
SMALL, LARGE, MEDIUM = 150, 300, 280
assert LARGE == 2 * SMALL and LARGE - MEDIUM == 20 and SMALL < MEDIUM < LARGE

C3 = stim("The tub nobody buys", (
    f"A cinema sells popcorn in two sizes: a small tub for ₹{SMALL} and a large one for ₹{LARGE}. Most customers, "
    "unwilling to pay double, choose the small tub. Then the cinema adds a third option, a medium tub for "
    f"₹{MEDIUM}. Hardly anyone buys it, yet sales of the large tub **(1) plummet**.\n\n"
    "The medium tub, it turns out, was never meant to be sold. Its job is to make the large tub look like a bargain: "
    "for only twenty rupees more than the medium, the customer gets far more popcorn. Marketers call such an option "
    "a decoy, and the pattern it creates is known as the decoy effect. The decoy works because people rarely judge "
    "prices in **(2) isolation**. Faced with a single price, most of us have little idea whether it is fair. Faced "
    "with two options that are easy to compare, we seize on the comparison and let it guide the choice. The decoy is "
    "therefore designed to be clearly **(3) superior** to the option the seller wants to sell, yet only slightly "
    "cheaper than it, so that the target option wins the comparison.\n\n"
    "Subscription offers often use the same trick. A magazine that offers a digital edition for ₹1,000 a year, a "
    "print edition for ₹2,500, and print and digital together, also for ₹2,500, is not being generous by "
    "**(4) accident**. Few readers want the print edition alone, but its presence makes the combined offer look like "
    "a free gift, and the combined offer is what the publisher hoped to sell all along.\n\n"
    "Critics argue that decoys **(5) honour** a quirk of the mind rather than serve the customer. Defenders reply "
    "that no one is forced to buy anything, and that the decoy merely highlights a deal that genuinely is good "
    "value. The truth probably lies between the two. A decoy does not deceive in the way a false label does; every "
    "price on the board is real. But it does **(6) steer** choices in a direction the seller has chosen, and a buyer "
    "who knows the trick is better placed to ask a simple question: would I still want this option if the decoy "
    "were not there?"))

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=1, ctx="Hardly anyone buys it, yet sales of the large tub plummet"),
  ["soar", "stagnate", "vanish", NR], 0,
  "Error-based cloze: the rest of the passage shows what the decoy does to the target option",
  "The passage explains that the medium tub exists 'to make the large tub look like a bargain'. Its effect is that "
  "more people buy the large tub, so its sales rise sharply: they 'soar'. 'Plummet' (fall steeply) says the "
  "opposite.",
  ["Purpose of the medium tub: make the large tub look like a bargain", "So large-tub sales rise",
   "'plummet' → 'soar'"],
  "'Stagnate' and 'vanish' would mean the decoy failed, yet the passage presents it as a working trick. "
  "'Plummet' contradicts the purpose of the decoy, so it cannot stay.", 40, C3, 1, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=2, ctx="The decoy works because people rarely judge prices in isolation"),
  ["comparison", "haste", "silence", NR], 3,
  "Error-based cloze: the next two sentences explain the bold word",
  "The passage goes on to say that with a single price we cannot tell whether it is fair, but with two options we "
  "'seize on the comparison'. So people rarely judge a price on its own, 'in isolation'. The word is correct.",
  ["Single price: we cannot judge it", "Two options: we compare", "Rarely judged alone → 'isolation' fits"],
  "'In comparison' reverses the point: the passage says people almost always compare. 'Haste' and 'silence' have "
  "nothing to do with how prices are judged.", 40, C3, 2, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=3, ctx="The decoy is therefore designed to be clearly superior to the option the seller wants "
                         "to sell, yet only slightly cheaper than it"),
  ["inferior", "identical", "unrelated", NR], 0,
  "Error-based cloze: checking the bold word against the example",
  f"The medium tub (₹{MEDIUM}) gives far less popcorn than the large one (₹{LARGE}) for only twenty rupees less: it "
  "is clearly worse value, i.e. 'inferior' to the target option. A decoy that was 'superior' would win the "
  "comparison itself.",
  ["Example: medium = much less popcorn, only ₹20 cheaper", "So it is clearly worse than the large tub",
   "'superior' → 'inferior'"],
  "An 'identical' option could not be both identical and cheaper, and an 'unrelated' option could not be compared "
  "at all. 'Superior' contradicts the example, so a replacement is needed.", 45, C3, 3, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=4, ctx="is not being generous by accident"),
  ["force", "habit", "law", NR], 3,
  "Error-based cloze: 'not ... by accident' = deliberately",
  "The next sentence explains that the print-only option is there so that the combined offer looks like a free "
  "gift, which is 'what the publisher hoped to sell all along'. The apparent generosity is deliberate, i.e. not 'by "
  "accident'. The word is correct.",
  ["Following sentence: the publisher planned it", "Planned = not accidental", "'by accident' fits"],
  "'Not generous by force' or 'by law' suggests the publisher was compelled, and 'by habit' suggests routine; the "
  "passage is about a deliberate design.", 40, C3, 4, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=5, ctx="Critics argue that decoys honour a quirk of the mind rather than serve the customer"),
  ["exploit", "conceal", "cure", NR], 0,
  "Error-based cloze: what critics would say a decoy does to a weakness",
  "Critics object that decoys take unfair advantage of a quirk in how people judge prices, instead of serving the "
  "customer. To take unfair advantage of something is to 'exploit' it. 'Honour' (respect) is not a criticism.",
  ["Speakers: critics", "Charge: taking advantage of a mental quirk", "'honour' → 'exploit'"],
  "Critics would not say decoys 'conceal' or 'cure' the quirk; decoys depend on it. 'Honour' turns the criticism "
  "into praise, so it must be replaced.", 40, C3, 5, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=6, ctx="But it does steer choices in a direction the seller has chosen"),
  ["halt", "ignore", "record", NR], 3,
  "Error-based cloze: a decoy guides choices without forcing them",
  "A decoy pushes buyers towards the option the seller prefers, while leaving them free to choose. To guide "
  "something in a chosen direction is to 'steer' it. The word is correct.",
  ["Decoy: guides buyers to the target option", "'in a direction the seller has chosen'", "'steer' fits"],
  "A decoy does not 'halt' or 'ignore' choices, and 'record choices in a direction' makes no sense. Only 'steer' "
  "goes with 'in a direction'.", 40, C3, 6, order=LAST_FIXED)

# =====================================================================================================================
# ERROR DETECTION
# =====================================================================================================================
ED = "Error Detection"
ED_STEM = ("Read the sentence to find out whether there is any grammatical or idiomatic error in it. The error, if "
           "any, will be in one part of the sentence. Choose that part as the answer. If there is no error, choose "
           "'No error'.\n")


def ed(sub, diff, a, b, c, answer, concept, explanation, steps, why, seconds=35):
    text = f"{ED_STEM}{a} (A) / {b} (B) / {c} (C) / No error (D)"
    Q(ED, sub, diff, text, [a, b, c, "No error"], LETTERS.index(answer), concept, explanation, steps, why, seconds,
      order=FIXED)


# ---- Basic (3)
ed("Part-wise error", B, "My younger sister is", "more cleverer than", "all her classmates.", "B",
   "Double comparative: a comparative adjective is formed either with -er or with 'more', never both",
   "'Cleverer' is already comparative, so adding 'more' doubles the comparison. Correct: 'My younger sister is "
   "cleverer than all her classmates.'",
   ["'clever' → comparative 'cleverer'", "'more' + 'cleverer' = double comparative", "Error in part B"],
   "Part A is a correct subject and verb. Part C ('than all her classmates') correctly completes the comparison. B "
   "has an error, so 'No error' is wrong.", 25)

ed("Part-wise error", B, "The teacher said us", "to keep our bags", "outside the laboratory.", "A",
   "'Say' does not take a person as its direct object; 'tell' does (tell someone to do something)",
   "We 'tell' someone to do something, or 'say' something 'to' someone. Correct: 'The teacher told us to keep our "
   "bags outside the laboratory.'",
   ["Verb + person + to-infinitive (an instruction)", "'say' cannot be followed directly by 'us'",
    "'said us' → 'told us': error in part A"],
   "Part B ('to keep our bags') correctly gives the instruction, and part C is a correct place phrase. A has an "
   "error, so 'No error' is wrong.", 25)

ed("Error-free sentence", B, "The shepherd counted", "his sheep carefully", "before closing the gate.", "D",
   "Error-free sentence: 'sheep' has the same form in the singular and the plural",
   "'Sheep' does not add -s in the plural, so 'his sheep' is correct for a whole flock. 'Counted ... carefully' and "
   "'before closing the gate' are also correct.",
   ["'sheep' plural = sheep (not 'sheeps')", "'counted his sheep carefully': correct", "'before closing the gate': "
    "correct"],
   "Part B only looks wrong to a reader who expects 'sheeps'; parts A and C have no error either, so 'No error' is "
   "the answer.", 25)

# ---- Intermediate (7)
ed("Part-wise error", I, "Every evening, the old man sat", "by the window and", "heard to the news on the radio.",
   "C",
   "Hear vs listen: 'listen to' means to pay attention to a sound; 'hear' takes no 'to'",
   "Paying attention to the news every evening is 'listening to' it. 'Heard to' is wrong. Correct: '... and "
   "listened to the news on the radio.'",
   ["Deliberate attention to a sound → listen to", "'hear' never takes 'to'", "'heard to' → 'listened to': error "
    "in part C"],
   "Part A (time phrase, subject and verb) and part B ('by the window and') are correct. C has an error, so 'No "
   "error' is wrong.")

ed("Part-wise error", I, "Our school team won the visitors", "by three goals to one", "in the final match.", "A",
   "Win vs beat: one wins a match, a game or a prize; one beats an opponent",
   "The visitors are the opponents, so the verb must be 'beat': 'Our school team beat the visitors by three goals "
   "to one ...'. One could say 'won the match', but not 'won the visitors'.",
   ["Object of the verb: the visitors (opponents)", "Opponent → beat; match/prize → win",
    "'won the visitors' → 'beat the visitors': error in part A"],
   "Part B ('by three goals to one') and part C ('in the final match') are correct. A has an error, so 'No error' "
   "is wrong.")

ed("Part-wise error", I, "This small car is very economic", "because it uses", "very little petrol.", "A",
   "Economic (relating to the economy) vs economical (giving good value, not wasteful)",
   "A car that uses very little petrol saves money: it is 'economical'. 'Economic' means 'relating to the economy', "
   "as in 'economic growth'.",
   ["Meaning needed: cheap to run, not wasteful", "That is 'economical'", "'very economic' → 'very economical': "
    "error in part A"],
   "Part B ('because it uses') and part C ('very little petrol') are correct. A has an error, so 'No error' is "
   "wrong.")

ed("Part-wise error", I, "Hearing the doorbell,", "she quickly wore her coat", "and ran down the stairs.", "B",
   "Wear (be dressed in: a state) vs put on (the action of dressing)",
   "Grabbing a coat and getting into it is an action done 'quickly': she 'put on' her coat. 'Wear' describes "
   "having clothes on, not the act of dressing.",
   ["'quickly' marks an action", "Action of dressing → put on", "'wore her coat' → 'put on her coat': error in "
    "part B"],
   "Part A is a correct participle phrase with 'she' as its subject. Part C is correct. B has an error, so 'No "
   "error' is wrong.")

ed("Part-wise error", I, "We had expected the repairs to be cheap,", "but in the end they",
   "costed us twelve thousand rupees.", "C",
   "'Cost' (to have a price) has the same form in the past tense: cost, cost, cost",
   "The past tense of 'cost' in the sense of having a price is 'cost': 'they cost us twelve thousand rupees'. "
   "('Costed' is used only for working out a cost, as in 'The plan was costed by the engineers'.)",
   ["Meaning: had a price of", "Past tense: cost (not costed)", "'costed us' → 'cost us': error in part C"],
   "Part A ('had expected ... to be cheap') and part B ('but in the end they') are correct. C has an error, so 'No "
   "error' is wrong.")

ed("Part-wise error", I, "After a six-hour journey", "over mountain roads, the bus", "finally arrived to the village.",
   "C",
   "'Arrive' takes 'at' (a point or building) or 'in' (a town, village or country), never 'to'",
   "One arrives 'in' a town or village and 'at' a station or building. 'Arrived to' is wrong: '... the bus finally "
   "arrived in the village.'",
   ["Verb: arrive", "arrive in (village, town) / arrive at (station, building)", "'arrived to' → 'arrived in': "
    "error in part C"],
   "Part A and part B ('over mountain roads, the bus') are correct. C has an error, so 'No error' is wrong.")

ed("Error-free sentence", I, "On reaching the hospital,", "we learnt that the doctor", "had already left for the day.",
   "D",
   "Error-free sentence: a participle phrase must refer to the subject of the main clause; past perfect for the "
   "earlier action",
   "'On reaching the hospital' refers to 'we', the subject of the main clause, so the phrase is correctly attached. "
   "The doctor's leaving happened before 'we learnt', so 'had already left' is correct.",
   ["Who reached? 'we' = subject of the main clause: correct", "Earlier past action: 'had already left': correct",
    "No error"],
   "The opening phrase is not dangling, since its subject is 'we'. 'Learnt' and 'had already left' are in the right "
   "order of time. No part has an error.")

# ---- Advanced (3)
ed("Part-wise error", A, "After the conference,", "the delegates returned", "to their respectable hotels.", "C",
   "Respective (belonging to each one separately) vs respectable (deserving respect; decent)",
   "Each delegate went back to his or her own hotel: 'their respective hotels'. 'Respectable hotels' would comment "
   "on the hotels' reputation, which is not the sense.",
   ["Sense: each to his or her own hotel", "That is 'respective'", "'respectable' → 'respective': error in part C"],
   "Part A (time phrase) and part B ('the delegates returned') are correct. C has an error, so 'No error' is "
   "wrong.", 40)

ed("Part-wise error", A, "The old poet's childish delight", "in birdsong and falling rain",
   "charmed everyone who met him.", "A",
   "Childish (silly, immature: a criticism) vs childlike (having a child's innocence and freshness: praise)",
   "The delight 'charmed everyone', so the author is praising the poet's innocent sense of wonder. That is "
   "'childlike delight'. 'Childish' is used to criticise immature behaviour.",
   ["Context: the delight charmed everyone (praise)", "Innocent wonder → childlike; immaturity → childish",
    "'childish' → 'childlike': error in part A"],
   "Part B ('in birdsong and falling rain') correctly follows 'delight', and part C is correct. A has an error, so "
   "'No error' is wrong.", 40)

ed("Error-free sentence", A, "His efforts notwithstanding,", "the project could not be", "completed on time.", "D",
   "Error-free sentence: 'notwithstanding' (= in spite of) may stand after its noun",
   "'Notwithstanding' can come before or after the noun it governs: 'notwithstanding his efforts' or 'his efforts "
   "notwithstanding'. 'Could not be completed' is a correct passive. The sentence means that the project was "
   "late in spite of his efforts.",
   ["'His efforts notwithstanding' = in spite of his efforts: correct", "'could not be completed': correct "
    "passive", "No error"],
   "The position of 'notwithstanding' may look odd, but it is correct. Parts B and C form a correct passive. No "
   "part has an error.", 40)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", B,
  SI_STEM + "Although she has lived in Paris for only a year, she speaks French **very fluent**.",
  ["very fluently", "very fluency", "much fluent", NI], 0,
  "An adverb, not an adjective, describes how an action is done",
  "'Fluent' is an adjective; it describes the action 'speaks', so the adverb 'fluently' is needed: 'she speaks "
  "French very fluently'.",
  ["Word described: the verb 'speaks'", "Verb → adverb", "'very fluently'"],
  "'Very fluency' puts a noun where a modifier is needed. 'Much fluent' keeps the adjective. The original uses an "
  "adjective for a verb, so 'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "The lecture went on for three hours, and most of the students **felt boring**.",
  ["felt bored", "felt boringly", "were feeling boring", NI], 0,
  "-ed adjectives describe how a person feels; -ing adjectives describe what causes the feeling",
  "The students had the feeling, so they 'felt bored'. The lecture was 'boring' because it caused that feeling.",
  ["Who has the feeling? The students", "Feeling → -ed adjective", "'felt bored'"],
  "'Felt boringly' uses an adverb after a linking verb. 'Were feeling boring' still says the students caused "
  "boredom. 'Felt boring' is wrong, so 'No improvement required' does not apply.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "Your handwriting is very **similar with** your brother's.",
  ["similar to", "similar from", "similar than", NI], 0,
  "Fixed preposition: similar to",
  "The adjective 'similar' is followed by 'to': 'Your handwriting is very similar to your brother's.'",
  ["Adjective: similar", "Fixed pairing: similar to", "'similar to'"],
  "'Similar from' confuses it with 'different from', and 'similar than' with comparatives. 'Similar with' is not "
  "standard, so 'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "I don't eat meat, and my sister **does not eat it too**.",
  ["does not eat it either", "does not eat it also", "does not eat it neither", NI], 0,
  "'Too' and 'also' are used in positive statements; 'either' adds a negative statement to another",
  "The added statement is negative ('does not eat it'), so it ends with 'either': 'my sister does not eat it "
  "either'.",
  ["Second clause is negative", "Negative addition → either", "'does not eat it either'"],
  "'Also' has the same problem as 'too'. 'Does not ... neither' is a double negative. The original uses 'too' with "
  "a negative, so 'No improvement required' is wrong.", 30, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "After retiring from the army, he **went on becoming** one of the most successful farmers in the "
  "district.",
  ["went on to become", "went on to becoming", "went on become", NI], 0,
  "'Go on to do' = do something next, after something else; 'go on doing' = continue doing the same thing",
  "Becoming a farmer was the next stage of his life after the army, not something he kept doing before. So the "
  "pattern is 'went on to become'.",
  ["Sense: a new stage after retiring", "Next stage → go on + to-infinitive", "'went on to become'"],
  "'Went on to becoming' mixes the two patterns, and 'went on become' drops 'to'. 'Went on becoming' would mean he "
  "continued becoming a farmer, which makes no sense, so 'No improvement required' is wrong.", 35,
  order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "Many economists believe that a gradual reform **is more preferable to** a sudden one.",
  ["is preferable to", "is more preferable than", "is preferable than", NI], 0,
  "'Preferable' already means 'better' or 'more desirable', so it does not take 'more'; it is followed by 'to'",
  "'Preferable' contains the idea of comparison, so 'more preferable' is redundant. The pattern is 'preferable "
  "to': 'a gradual reform is preferable to a sudden one'.",
  ["'preferable' = more desirable", "No 'more' before it", "Pattern: preferable to → 'is preferable to'"],
  "'More preferable than' keeps the redundant 'more' and adds the wrong preposition. 'Preferable than' uses the "
  "wrong preposition. The original is redundant, so 'No improvement required' is wrong.", 35, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "We **regret informing** you that your application for the post of librarian has not been accepted.",
  ["regret to inform", "regret to informing", "are regretting to inform", NI], 0,
  "'Regret to do' = be sorry about what one is about to say or do (formal announcements); 'regret doing' = be sorry "
  "for something already done",
  "The writer is sorry about the news being given now, in this letter. That sense takes the to-infinitive: 'We "
  "regret to inform you ...'. 'Regret informing' would mean being sorry for having informed someone earlier.",
  ["Sense: sorry about what we are now telling you", "Act happening now → regret + to-infinitive",
   "'regret to inform'"],
  "'Regret to informing' mixes the two patterns. 'Are regretting to inform' puts a verb of feeling in the "
  "continuous form. 'Regret informing' gives the wrong meaning, so 'No improvement required' is wrong.", 35,
  order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "**Try as he might**, the old man could not loosen the rusty bolt.",
  ["Trying as he might", "Try as might he", "As he might try", NI], 3,
  "Concessive inversion: verb (base form) + as + subject + might = however hard he tried",
  "'Try as he might' is a fixed concessive pattern meaning 'however hard he tried'. It is correct as it stands.",
  ["Pattern: Verb + as + subject + might/may", "Meaning: however hard he tried", "Correct → no improvement"],
  "'Trying as he might' breaks the fixed pattern, 'Try as might he' inverts the wrong words, and 'As he might try' "
  "loses the concessive meaning.", 35, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "Accepting the job in Delhi would **mean to leave** my parents alone in the village.",
  ["mean leaving", "mean to leaving", "meant to leave", NI], 0,
  "'Mean doing' = involve or result in; 'mean to do' = intend to do",
  "The sentence says what accepting the job would involve: leaving the parents alone. For this sense 'mean' takes "
  "the -ing form: 'would mean leaving my parents alone'.",
  ["Subject: accepting the job (a thing, not a person)", "Sense: involve, result in → mean + -ing",
   "'mean leaving'"],
  "'Mean to leave' would mean 'intend to leave', which a job cannot do. 'Mean to leaving' mixes the patterns. "
  "'Meant to leave' clashes with 'would', so 'No improvement required' is wrong.", 35, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "Before leaving for the city, he gave his younger brother **the few rupees** he had saved.",
  ["the little rupees", "a little rupees", "few of rupees", NI], 3,
  "'The few' + plural countable noun = all of a small number (here, all the rupees he had saved)",
  "'Rupees' is countable, so 'few' is right, and 'the few rupees he had saved' means all of the small number of "
  "rupees he had. The phrase is correct.",
  ["'rupees' is countable → few", "'the few ... he had saved' = all of a small number", "Correct → no improvement"],
  "'Little' goes with uncountable nouns, so 'the little rupees' and 'a little rupees' are wrong. 'Few of rupees' "
  "needs 'the' before the noun.", 35, order=LAST_FIXED)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", B,
  PR_STEM + "The plane **took up** an hour late because of the fog.",
  ["took off", "took over", "took in", NR], 0,
  "Phrasal verb: take off = (of an aircraft) leave the ground",
  "A plane leaving the ground 'takes off': 'The plane took off an hour late because of the fog.'",
  ["Subject: the plane", "Leaving the ground → take off", "'took off'"],
  "'Took over' means took control, and 'took in' means received or deceived. 'Took up' (started a hobby or used "
  "space) is wrong here, so 'No replacement required' does not apply.", 25, order=LAST_FIXED)

Q(PR, "Replace the phrase", B,
  PR_STEM + "Thieves **broke from** the shop last night and stole two laptops.",
  ["broke into", "broke up", "broke down", NR], 0,
  "Phrasal verb: break into (a building) = enter it by force",
  "The thieves forced their way into the shop to steal the laptops: they 'broke into' it.",
  ["Thieves + a shop + stealing", "Forced entry → break into", "'broke into'"],
  "'Broke up' means ended or separated, and 'broke down' means stopped working. 'Broke from' is not the phrase for "
  "a forced entry, so 'No replacement required' does not apply.", 25, order=LAST_FIXED)

Q(PR, "Replace the phrase", B,
  PR_STEM + "While shopping in the market, I **ran across** my old school teacher.",
  ["ran over", "ran through", "ran off", NR], 3,
  "Phrasal verb: run across (someone) = meet by chance",
  "Meeting a teacher unexpectedly while shopping is 'running across' him or her. The phrase is correct.",
  ["Situation: an unplanned meeting", "run across = meet by chance", "Correct → no replacement"],
  "'Ran over' means hit with a vehicle, 'ran through' means rehearsed or pierced, and 'ran off' means escaped; "
  "none describes a chance meeting.", 25, order=LAST_FIXED)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The witness's story did not **add on**; the times he gave did not match the bus timetable.",
  ["add up", "add in", "add to", NR], 0,
  "Phrasal verb: add up (informal) = make sense; be consistent",
  "The witness's times clashed with the timetable, so his story did not make sense: it did not 'add up'.",
  ["Clue: times did not match the timetable", "Story not consistent → did not add up", "'add up'"],
  "'Add in' means include, and 'add to' needs an object (add to something). 'Add on' means attach an extra part, "
  "so 'No replacement required' does not apply.", 30, order=LAST_FIXED)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The opposition tried hard to **pick holes on** the government's new housing plan.",
  ["pick holes in", "pick holes at", "pick holes from", NR], 0,
  "Idiom: pick holes in (something) = find faults in it",
  "Looking for faults in a plan is 'picking holes in' it: 'The opposition tried hard to pick holes in the "
  "government's new housing plan.'",
  ["Sense: find faults", "Fixed phrase: pick holes in", "'pick holes in'"],
  "'At' and 'from' are not used in this phrase, and neither is 'on', so 'No replacement required' does not apply.",
  30, order=LAST_FIXED)

Q(PR, "Replace the phrase", A,
  PR_STEM + "The company tried to **hush away** the scandal, but a junior employee leaked the documents to the "
  "press.",
  ["hush up", "hush down", "hush off", NR], 0,
  "Phrasal verb: hush up = keep something secret, especially something discreditable",
  "The company wanted to stop the scandal from becoming known; the leak defeated that aim. Keeping a scandal "
  "secret is 'hushing it up'.",
  ["Clue: the documents were leaked despite the company", "Keeping a scandal quiet → hush up", "'hush up'"],
  "'Hush down' and 'hush off' are not English phrasal verbs, and neither is 'hush away', so 'No replacement "
  "required' does not apply.", 30, order=LAST_FIXED)

Q(PR, "Replace the phrase", A,
  PR_STEM + "The dam was completed **in the teeth of** fierce opposition from the villages that it would flood.",
  ["in the jaws of", "on the teeth of", "at the teeth of", NR], 3,
  "Idiom: in the teeth of = in spite of (strong opposition or difficulty)",
  "The dam was built despite fierce opposition. 'In the teeth of' means exactly this, so the phrase is correct.",
  ["Sense: despite fierce opposition", "Idiom: in the teeth of", "Correct → no replacement"],
  "'In the jaws of' means close to (danger or death), as in 'in the jaws of death'. 'On the teeth of' and 'at the "
  "teeth of' are not idioms.", 30, order=LAST_FIXED)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", B, SC_OK,
  ["There are too many cars on this narrow road.",
   "There are too much cars on this narrow road.",
   "There are too more cars on this narrow road.",
   "There is too many cars on this narrow road."], 0,
  "'Many' with countable plural nouns; 'much' with uncountable nouns; verb agrees with the plural noun",
  "'Cars' is a countable plural, so it takes 'many' and the plural verb 'are': 'There are too many cars on this "
  "narrow road.'",
  ["'cars' = countable plural", "countable plural → too many", "plural noun → 'There are'"],
  "'Too much cars' uses 'much' with a countable noun, 'too more' is not English, and 'There is ... cars' does not "
  "agree with the plural noun.", 25)

Q(SC, "Grammatically incorrect sentence", I, SC_BAD,
  ["A large amount of people gathered outside the stadium.",
   "A large amount of money was spent on the new stadium.",
   "A large number of people gathered outside the stadium.",
   "Only a small amount of sugar is needed for this recipe."], 0,
  "'Amount of' goes with uncountable nouns; 'number of' with countable plurals",
  "'People' is countable, so it takes 'a large number of'. 'A large amount of people' is incorrect.",
  ["'people' = countable → number of", "'money', 'sugar' = uncountable → amount of",
   "Only the people-with-'amount' sentence is wrong"],
  "'Amount of money' and 'amount of sugar' correctly pair 'amount' with uncountable nouns, and 'number of people' "
  "correctly pairs 'number' with a countable plural.", 30)

Q(SC, "Correct sentence", I, SC_OK,
  ["I want you to come early tomorrow.",
   "I want that you come early tomorrow.",
   "I want that you should come early tomorrow.",
   "I want you come early tomorrow."], 0,
  "'Want' takes object + to-infinitive, not a that-clause",
  "The pattern is 'want + someone + to do something': 'I want you to come early tomorrow.'",
  ["Verb: want", "Pattern: want + object + to-infinitive", "'I want you to come early tomorrow.'"],
  "'Want' is not followed by a that-clause, with or without 'should'. 'Want you come' leaves out the 'to' of the "
  "infinitive.", 25)

Q(SC, "Grammatically incorrect sentence", A, SC_BAD,
  ["Almost each passenger on the night bus was asleep.",
   "Almost every passenger on the night bus was asleep.",
   "Each passenger on the night bus was given a blanket.",
   "Nearly every seat on the night bus was taken."], 0,
  "'Almost' and 'nearly' combine with 'every', not with 'each'",
  "'Each' picks out members one by one and cannot be modified by 'almost'; 'every' sees the group as a whole and "
  "can. So 'Almost each passenger ...' is incorrect; it should be 'Almost every passenger ...'.",
  ["'almost/nearly' + every: correct", "'almost/nearly' + each: incorrect", "The 'almost each' sentence is wrong"],
  "'Almost every passenger' and 'Nearly every seat' use 'every' correctly, and 'Each passenger was given a "
  "blanket' uses 'each' without 'almost', which is correct.", 35)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) So the puppy stayed, and the children named him Bholu and took turns to share their lunch with him.\n"
  "(B) One rainy morning, a thin, shivering puppy was found sitting at the gate of our village school.\n"
  "(C) The headmistress at first wanted to send him away, as she was worried that he might bite.\n"
  "(D) Today Bholu sleeps outside the staffroom and barks loudly whenever a stranger comes near the school.\n"
  "(E) But when she saw how gently he played with the youngest pupils, she changed her mind.",
  ["BCEAD", "BACED", "BCAED", "CBEAD"], 0,
  "Para jumble: arrival → first reaction → change of mind → result ('So') → present day",
  "B introduces the puppy. C gives the headmistress's first reaction. E ('But when she saw ...') reverses it. A "
  "('So the puppy stayed') is the result of her change of mind. D ('Today') ends the story.",
  ["Opener: B (the puppy arrives)", "B → C: her first reaction ('at first')", "C → E: 'But ... she changed her "
   "mind'", "E → A ('So the puppy stayed') → D ('Today'): BCEAD"],
  "BACED says 'So the puppy stayed' before any question of sending him away has arisen. BCAED puts A between the "
  "headmistress's doubt and her change of mind, so 'So' has no reason before it. CBEAD opens with 'him', who has "
  "not yet been introduced.", 35)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) Making a cup of masala tea is easier than many people think.\n"
  "(P) Then add the tea leaves and let them boil for a minute, until the water turns dark.\n"
  "(Q) Finally, strain the tea into cups and serve it hot.\n"
  "(R) First, bring a cup of water to the boil with some crushed ginger and a few cardamoms.\n"
  "(S) After that, pour in the milk and sugar and let the mixture come to the boil once more.",
  ["RPSQ", "RSPQ", "PRSQ", "RPQS"], 0,
  "Process jumble: sequence words (First, Then, After that, Finally) and the logic of the steps",
  "R ('First') starts with boiling water and spices. P ('Then') adds tea leaves to the water. S ('After that') "
  "adds milk and sugar. Q ('Finally') strains and serves.",
  ["(1) → R: 'First'", "R → P: 'Then' add tea leaves to the water", "P → S: 'After that' milk and sugar",
   "S → Q: 'Finally' strain and serve: RPSQ"],
  "RSPQ adds milk before the tea leaves, yet P speaks of 'the water' turning dark. PRSQ starts with 'Then'. RPQS "
  "serves the tea before the milk and sugar are added.", 30)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) At sea level, water boils at 100 °C, and no amount of extra heat can make it hotter while it stays "
  "liquid in an open pan.\n"
  "(B) Food that would take an hour to cook in an open pot can therefore be ready in a fraction of that time.\n"
  "(C) A pressure cooker gets round this limit by sealing the pot so that the steam cannot escape.\n"
  "(D) The trapped steam raises the pressure inside, and at this higher pressure water boils only at around "
  "120 °C.\n"
  "(E) Cooks in hill towns value the device even more, because at high altitude water boils below 100 °C and food "
  "in an open pan cooks very slowly.",
  ["ACDBE", "ACBDE", "CDABE", "ACDEB"], 0,
  "Para jumble: the limit → how the cooker gets round it → the mechanism → the result → a further use",
  "A states the limit of an open pan. C ('this limit') shows how the cooker gets round it. D explains how sealing "
  "raises the boiling point. B ('therefore') gives the result: faster cooking. E adds why hill cooks value it even "
  "more.",
  ["Opener: A (the boiling-point limit)", "A → C: 'this limit'", "C → D: trapped steam → higher pressure → hotter "
   "water", "D → B ('therefore' faster) → E ('even more'): ACDBE"],
  "ACBDE gives the result ('therefore') before the higher temperature that causes it. CDABE opens with 'this "
  "limit', which has nothing to refer to. ACDEB places 'therefore' after E, so it would wrongly follow from the "
  "hill-town point instead of from D.", 45)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) During a storm, we always see the flash of lightning before we hear the thunder, although both are "
  "produced at the same moment.\n"
  "(P) Light travels so fast that the flash reaches us almost instantly.\n"
  "(Q) Sound, by contrast, covers only about a third of a kilometre every second.\n"
  "(R) The reason is the great difference between the speeds of light and sound.\n"
  "(S) By counting the seconds between the flash and the bang and dividing by three, one can therefore estimate "
  "roughly how many kilometres away the storm is.",
  ["RPQS", "RQPS", "PQRS", "RPSQ"], 0,
  "Fixed opener; 'The reason' → light → 'by contrast' sound → 'therefore' practical use",
  "R ('The reason') explains the puzzle in (1). P describes light, and Q ('by contrast') describes sound. S "
  "('therefore') uses the third-of-a-kilometre figure from Q to estimate distance.",
  ["(1) → R: 'The reason' for the puzzle", "R → P: light", "P → Q: 'Sound, by contrast'",
   "Q → S: 'dividing by three' uses Q's figure: RPQS"],
  "RQPS puts 'by contrast' before the thing it contrasts with. PQRS gives the details before 'The reason' "
  "introduces them. RPSQ divides by three before the speed of sound (a third of a kilometre a second) is given.",
  40)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) that he fell asleep\n(Q) the night watchman was\n(R) in his chair within minutes.\n(S) so tired",
  ["QSPR", "QPSR", "SQPR", "QSRP"], 0,
  "'So + adjective + that' (result clause)",
  "'The night watchman was so tired that he fell asleep in his chair within minutes.' Subject and verb (Q), 'so "
  "tired' (S), the result clause (P) and the place and time phrase that ends the sentence (R).",
  ["Subject + verb: Q", "so + adjective: S", "that-clause: P, completed by R (ends with the full stop)"],
  "QPSR separates 'so tired' from 'was'. SQPR opens with 'so tired', which has no verb before it. QSRP puts 'in his "
  "chair within minutes.' (which ends with the full stop) before the result clause.", 30)

Q(SR, "Word/phrase rearrangement within a sentence", A,
  SR_STEM + "(P) much as\n(Q) I cannot support\n(R) I admire my uncle's courage,\n(S) his plan to sell the land.",
  ["PRQS", "RPQS", "PQRS", "QPSR"], 0,
  "Concessive 'much as' (= although ... very much) + main clause",
  "'Much as I admire my uncle's courage, I cannot support his plan to sell the land.' The concessive clause (P + R) "
  "comes first, then the main clause (Q + S), which ends with the full stop.",
  ["Concessive clause: much as (P) + I admire my uncle's courage, (R)", "Main clause: I cannot support (Q) + his "
   "plan to sell the land. (S)", "→ PRQS"],
  "RPQS puts 'much as' after the clause it belongs to. PQRS gives 'Much as I cannot support', which reverses the "
  "logic and leaves 'I admire ...' hanging. QPSR splits 'I cannot support' from its object.", 35)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The medicine tasted so ______ that the little boy spat it out.",
  ["bitter", "sweet", "fresh", "mild"], 0,
  "Single blank: the result clause ('so ... that he spat it out') decides the word",
  "A child spits out medicine that tastes unpleasant. 'Bitter' gives that unpleasant taste.",
  ["Result: he spat it out", "Cause: an unpleasant taste", "'bitter'"],
  "A 'sweet', 'fresh' or 'mild' taste would not make the boy spit the medicine out.", 20)

Q(FB, "Double blank", B,
  FB2 + "The shopkeeper ______ the boy for the broken glass and asked him to ______ for it.",
  ["blamed, pay", "praised, pay", "blamed, wait", "thanked, ask"], 0,
  "Double blank: both words must fit the situation of a broken glass",
  "The shopkeeper holds the boy responsible for breaking the glass ('blamed') and wants the cost covered ('pay for "
  "it').",
  ["Broken glass → the boy is held responsible: blamed", "'asked him to ___ for it' → pay for it",
   "'blamed, pay'"],
  "No one is 'praised' or 'thanked' for breaking a glass. 'Wait for it' does not suit a shopkeeper's demand after "
  "damage.", 25)

Q(FB, "Single blank", I,
  FB1 + "Unlike her evasive colleagues, the witness was ______: she answered every question directly and hid "
  "nothing.",
  ["forthright", "devious", "hesitant", "cunning"], 0,
  "Single blank: 'Unlike' signals a contrast, and the colon gives the definition",
  "She answered directly and hid nothing, the opposite of her evasive colleagues. Someone who speaks plainly and "
  "openly is 'forthright'.",
  ["'Unlike her evasive colleagues' → the opposite of evasive", "Colon: answered directly, hid nothing",
   "'forthright'"],
  "'Devious' and 'cunning' describe someone who hides the truth, like the colleagues. 'Hesitant' does not fit "
  "someone who answered every question directly.", 25)

Q(FB, "Single blank", I,
  FB1 + "The new parking fee was deeply ______ by small traders, who held protests in every market.",
  ["resented", "welcomed", "admired", "ignored"], 0,
  "Single blank: the traders' reaction ('held protests') decides the word",
  "People who protest in every market feel bitter about the fee. To feel bitter at something unfair is to 'resent' "
  "it: the fee was deeply 'resented'.",
  ["Reaction: protests everywhere", "Feeling: bitterness at unfair treatment", "'resented'"],
  "Traders who 'welcomed' or 'admired' the fee would not protest, and a fee that was 'ignored' would not cause "
  "protests in every market.", 25)

Q(FB, "Double blank", I,
  FB2 + "The ______ child refused to share his toys and ______ for hours whenever he did not get his way.",
  ["spoilt, sulked", "generous, sulked", "spoilt, laughed", "obedient, smiled"], 0,
  "Double blank: both words must describe a child who refuses to share",
  "A child who will not share and is unhappy whenever he does not get his way is 'spoilt', and he 'sulked' (was "
  "silently bad-tempered) for hours.",
  ["Refuses to share, wants his way → spoilt", "Reaction to not getting his way → sulked", "'spoilt, sulked'"],
  "A 'generous' or 'obedient' child would not refuse to share. A child who does not get his way does not usually "
  "'laugh' or 'smile' for hours.", 30)

Q(FB, "Double blank", I,
  FB2 + "The ______ of the old fort, once the pride of the kingdom, are now ______ with creepers and wild grass.",
  ["ruins, overgrown", "plans, overgrown", "ruins, decorated", "owners, covered"], 0,
  "Double blank: 'once the pride of the kingdom' and 'now' signal decay",
  "What remains of a fort that was 'once' the pride of a kingdom is its 'ruins', and neglected ruins become 'overgrown with "
  "creepers and wild grass'.",
  ["'once ... now' → decline", "What remains of a fort → ruins", "Covered by plants → overgrown"],
  "'Plans' cannot be overgrown with grass, and 'owners' cannot be covered with creepers. Creepers and wild grass "
  "are a sign of neglect, not 'decoration'.", 30)

Q(FB, "Phrase fillers", I,
  FBP + "After the accident on the bridge, traffic in both directions ______ for nearly three hours.",
  ["came to a standstill", "came of age", "came to terms", "came into its own"], 0,
  "Phrase filler: come to a standstill = stop moving completely",
  "An accident on a bridge blocks the road, so the traffic stops completely for hours: it 'came to a standstill'.",
  ["Cause: accident on the bridge", "Effect: no movement for hours", "'came to a standstill'"],
  "'Came of age' means became adult or mature, 'came to terms' means accepted something painful, and 'came into "
  "its own' means began to show its value; none describes traffic stopping.", 30)

Q(FB, "Phrase fillers", I,
  FBP + "Every month, she ______ a small part of her salary for her daughter's education.",
  ["sets aside", "sets off", "sets out", "sets about"], 0,
  "Phrase filler: set aside = save or keep for a particular purpose",
  "Keeping part of one's salary for a particular purpose, here a daughter's education, is 'setting it aside'.",
  ["Purpose: the daughter's education", "Keeping money for a purpose → set aside", "'sets aside'"],
  "'Sets off' means starts a journey or causes, 'sets out' means begins a journey or explains, and 'sets about' "
  "means begins a task; none means saving money.", 25)

Q(FB, "Single blank", I,
  FB1 + "Even as a child, she showed a remarkable ______ for languages, picking up Tamil, Bengali and Marathi from "
  "her neighbours.",
  ["flair", "aversion", "contempt", "indifference"], 0,
  "Single blank: the participle phrase ('picking up three languages') shows natural talent",
  "A child who picks up three languages from her neighbours has a natural talent for them. 'Flair' means a natural "
  "ability: 'a remarkable flair for languages'.",
  ["Evidence: learnt three languages easily", "Natural talent", "'flair'"],
  "'Aversion', 'contempt' and 'indifference' all suggest dislike or lack of interest, which contradicts her easy "
  "learning.", 25)

Q(FB, "Single blank", A,
  FB1 + "The professor's lectures were so ______ that only a handful of students could follow his arguments.",
  ["abstruse", "lucid", "succinct", "trite"], 0,
  "Single blank: 'so ... that only a handful could follow' points to difficulty",
  "Lectures that almost nobody can follow are hard to understand. 'Abstruse' means difficult to understand, "
  "obscure.",
  ["Result: very few could follow", "Cause: hard to understand", "'abstruse'"],
  "'Lucid' (clear) and 'succinct' (brief and clear) would make the lectures easy to follow. 'Trite' (overused, "
  "unoriginal) ideas are easy to follow too.", 30)

Q(FB, "Double blank", A,
  FB2 + "The ______ critic found fault with every scene, yet even he ______ that the lead actor was superb.",
  ["captious, conceded", "captious, denied", "lenient, conceded", "indulgent, doubted"], 0,
  "Double blank: the first word fits 'found fault with every scene'; 'yet even he' signals a reluctant admission",
  "A critic who finds fault with everything is 'captious'. 'Yet even he' shows that, against his habit, he admitted "
  "something good: he 'conceded' that the actor was superb.",
  ["Fault-finding → captious", "'yet even he' → reluctant admission", "'captious, conceded'"],
  "'Denied' cancels the contrast set up by 'yet even he'. 'Lenient' and 'indulgent' critics do not find fault with "
  "every scene, and 'doubted' does not fit 'yet even he'.", 35)

Q(FB, "Phrase fillers", A,
  FBP + "The young batsman's century in his first match proved to be ______; he did not score another fifty all "
  "season.",
  ["a flash in the pan", "a red herring", "a dark horse", "the order of the day"], 0,
  "Phrase filler: a flash in the pan = a sudden success that is not repeated",
  "One century followed by no other fifty all season is a single success that was never repeated: 'a flash in the "
  "pan'.",
  ["Clue after the semicolon: no repeat all season", "One-off success", "'a flash in the pan'"],
  "'A red herring' distracts from the real issue, 'a dark horse' is a little-known competitor who surprises "
  "everyone (a person, not a century), and 'the order of the day' is something common.", 30)

Q(FB, "Single blank", A,
  FB1 + "Rather than face the questions directly, the spokesperson gave ______ answers that committed the ministry "
  "to nothing.",
  ["equivocal", "unequivocal", "categorical", "emphatic"], 0,
  "Single blank: avoiding direct answers and committing to nothing = deliberately vague",
  "Answers that dodge the questions and commit to nothing are open to more than one reading, deliberately: "
  "'equivocal'.",
  ["'Rather than face the questions directly'", "'committed the ministry to nothing'", "Deliberately vague → "
   "'equivocal'"],
  "'Unequivocal', 'categorical' and 'emphatic' answers are clear and firm, the opposite of answers that commit to "
  "nothing.", 30)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'accept' used correctly?",
  ["Everyone accept Ravi came to the party.",
   "Please accept my apologies for the delay.",
   "All the shops are open accept the chemist's.",
   "He works every day accept Sunday."], 1,
  "Accept (verb: to receive or agree to) vs except (preposition: leaving out)",
  "'Accept' is a verb meaning to receive willingly. 'Please accept my apologies' uses it correctly.",
  ["'Everyone ___ Ravi' = leaving out Ravi → except", "'accept my apologies' = receive → correct",
   "'open ___ the chemist's' = leaving out → except", "'every day ___ Sunday' = leaving out → except"],
  "The other three need 'except' (leaving out): everyone except Ravi, open except the chemist's, every day except "
  "Sunday.", 25)

Q(WU, "Word swap", B,
  WS_STEM + "The **(A) teacher** asked the **(B) blackboard** to clean the **(C) monitor** before the **(D) class** "
  "began.",
  ["B-C", "A-C", "A-D", "No swap required"], 0,
  "Word swap: who can be asked, and what can be cleaned",
  "A blackboard cannot be asked to do anything, and a class monitor is not what gets cleaned. Swapping B and C "
  "gives 'The teacher asked the monitor to clean the blackboard before the class began.'",
  ["'asked the blackboard' makes no sense", "'clean the monitor' should be 'clean the blackboard'", "Swap B and C"],
  "A-C gives 'The monitor asked the blackboard to clean the teacher', and A-D gives 'The class asked the "
  "blackboard ...'; both remain absurd. The sentence as given makes no sense, so a swap is required.", 25,
  order=LAST_FIXED)

Q(WU, "Correct usage of a word", I,
  "In which of the following sentences is the word 'ingenious' used correctly?",
  ["The boy's ingenious answer showed that he was simply honest and innocent.",
   "Using an old bicycle wheel, the farmer built an ingenious device for lifting water.",
   "It would be ingenious of us to pretend that the scheme has no flaws.",
   "She was so ingenious that she believed every stranger's story."], 1,
  "Ingenious (clever and inventive) vs ingenuous (innocent, trusting) vs disingenuous (insincere)",
  "'Ingenious' means clever and inventive. A water-lifting device made from an old bicycle wheel is an inventive "
  "solution, so 'ingenious' fits.",
  ["Honest and innocent → ingenuous", "Clever device from a bicycle wheel → ingenious: correct",
   "Pretending insincerely → disingenuous", "Believing every story → ingenuous (naive)"],
  "The honest-and-innocent answer and the trusting woman need 'ingenuous'; pretending the scheme has no flaws "
  "would be 'disingenuous'.", 30)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'officious' used correctly?",
  ["The officious letter from the ministry carried the government's seal.",
   "An officious clerk insisted on checking every visitor's bag, though no one had asked him to.",
   "The results will be declared on the board's officious website next week.",
   "He remained officious and silent throughout the meeting, giving no opinion."], 1,
  "Officious (too eager to give orders or interfere) vs official (authorised; of an office)",
  "'Officious' describes someone who interferes or asserts authority without being asked. A clerk who checks every "
  "bag when nobody asked him to is officious.",
  ["Letter with a government seal → official", "Interfering without being asked → officious: correct",
   "The board's website → official", "Silent, giving no opinion → not officious (the opposite)"],
  "The letter and the website need 'official'. A man who stays silent and offers nothing is the opposite of "
  "officious.", 35)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'scarce' as used in the sentence:\n"
  "'During the long drought, drinking water became so scarce that tankers were sent to the village every day.'",
  ["in short supply", "dirty", "costly", "plentiful"], 0,
  "Scarce = not enough to meet the need",
  "A drought dries up wells, and tankers had to bring water every day, so there was not enough of it: water was "
  "'in short supply'.",
  ["Cause: long drought", "Result: tankers needed daily", "'in short supply'"],
  "Dirty or costly water would not by itself need daily tankers in a drought, and 'plentiful' is the opposite.", 20)

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'vacant' as used in the sentence:\n"
  "'Three teachers' posts in the village school have been vacant since March, so the other teachers take extra "
  "classes.'",
  ["unfilled", "temporary", "well paid", "newly created"], 0,
  "Vacant (of a job or seat) = not filled",
  "The other teachers take extra classes because no one holds those three posts: they are 'unfilled'.",
  ["Clue: others take extra classes", "No one in the posts", "'unfilled'"],
  "Temporary, well-paid or newly created posts could still be filled; only 'unfilled' explains the extra classes.",
  20)

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'hoard' as used in the sentence:\n"
  "'Fearing a shortage, some traders began to hoard sugar instead of selling it.'",
  ["store up and hold back", "sell cheaply", "throw away", "weigh carefully"], 0,
  "Hoard = collect and keep a large store of something, often secretly",
  "'Instead of selling it' shows that the traders kept the sugar back. Storing goods in expectation of a shortage "
  "is hoarding: 'store up and hold back'.",
  ["'instead of selling it'", "They kept it back, fearing a shortage", "'store up and hold back'"],
  "'Sell cheaply' contradicts 'instead of selling it'. Traders fearing a shortage would not throw sugar away, and "
  "'weigh carefully' does not oppose selling.", 20)

Q(VO, "Word pairs", B, "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Ascend – Descend", "Brave – Courageous", "Rapid – Swift", "Wealthy – Rich"], 0,
  "Word pairs: identify antonyms and synonyms",
  "'Ascend' means go up and 'descend' means go down, so they are opposites. The other pairs are synonyms.",
  ["Ascend (go up) ≠ descend (go down)", "Brave = courageous", "Rapid = swift", "Wealthy = rich"],
  "The other three pairs are synonyms, not opposites.", 20)

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'cryptic' as used in the sentence:\n"
  "'The minister's cryptic reply, \"Wait and see what the river brings\", left the reporters guessing about his "
  "plans.'",
  ["having a hidden or puzzling meaning", "rude and angry", "long and detailed", "clear and direct"], 0,
  "Cryptic = with a meaning that is hidden or hard to work out",
  "The reply left reporters 'guessing about his plans', so its meaning was not plain. A remark with a hidden or "
  "puzzling meaning is 'cryptic'.",
  ["Reply: a riddle-like sentence", "Effect: reporters left guessing", "'having a hidden or puzzling meaning'"],
  "Nothing suggests anger, and a one-line reply is not 'long and detailed'. 'Clear and direct' is the opposite; a "
  "clear reply would not leave reporters guessing.", 25)

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'mundane' as used in the sentence:\n"
  "'After years of adventure at sea, the retired captain found the mundane routine of village life hard to bear.'",
  ["ordinary and dull", "strange and exciting", "dangerous", "holy"], 0,
  "Mundane = ordinary, lacking interest or excitement",
  "The captain is contrasting village life with 'years of adventure'. A routine he finds 'hard to bear' after "
  "adventure is ordinary and dull.",
  ["Contrast: adventure at sea vs village routine", "Hard to bear → lacking excitement", "'ordinary and dull'"],
  "'Strange and exciting' and 'dangerous' would suit the life at sea, not the village routine. 'Holy' is not "
  "suggested by the context.", 25)

Q(VO, "Word pairs", I, "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Arduous – Laborious", "Humble – Arrogant", "Swift – Sluggish", "Fertile – Barren"], 0,
  "Word pairs: identify synonyms and antonyms",
  "'Arduous' and 'laborious' both mean needing great effort. The other pairs are opposites.",
  ["Arduous = laborious (needing much effort)", "Humble ≠ arrogant", "Swift ≠ sluggish", "Fertile ≠ barren"],
  "The other three pairs are opposites, not synonyms.", 25)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", B,
  SY_STEM + "After walking all day in the hot sun, the **weary** travellers sat down under a tree.",
  ["tired", "cheerful", "careless", "foreign"], 0,
  "Weary = very tired",
  "People who have walked all day in the hot sun and sit down to rest are worn out: 'weary' means 'tired'.",
  ["Context: walked all day in the sun, then sat down", "State: worn out", "Closest: 'tired'"],
  "Nothing suggests the travellers were 'cheerful', 'careless' or 'foreign'; the context is about exhaustion.", 20)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The **dexterous** potter shaped a perfect jar on the wheel in under a minute.",
  ["skilful", "clumsy", "elderly", "patient"], 0,
  "Dexterous = skilful, especially with the hands",
  "Shaping a perfect jar in under a minute shows great skill with the hands: the potter is 'skilful'.",
  ["Context: perfect jar in under a minute", "Quality: skill with the hands", "Closest: 'skilful'"],
  "'Clumsy' is the opposite. Nothing about age is said, and a potter who works in under a minute is fast rather "
  "than 'patient'.", 25)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The **ominous** silence in the forest made the villagers fear that a tiger was nearby.",
  ["threatening", "pleasant", "noisy", "ancient"], 0,
  "Ominous = suggesting that something bad is going to happen",
  "The silence made the villagers fear a tiger, so it seemed to warn of danger. That is 'threatening'.",
  ["Effect: villagers feared a tiger", "Silence that warns of danger", "Closest: 'threatening'"],
  "A silence that causes fear is not 'pleasant', and a silence cannot be 'noisy'. 'Ancient' has nothing to do with "
  "fear.", 25)

Q(SY, "Contextual synonym", I,
  SY_STEM + "Many offices have stopped using fax machines, which are now largely **obsolete**.",
  ["outmoded", "expensive", "novel", "fragile"], 0,
  "Obsolete = out of date; no longer used",
  "Offices 'have stopped using' fax machines because newer methods have replaced them, so the machines are out "
  "of date: 'outmoded'.",
  ["Clue: offices have stopped using them", "Replaced by newer methods = out of date", "Closest: 'outmoded'"],
  "Cost and fragility are not mentioned as reasons, and 'novel' (new) contradicts offices giving them up.", 25)

Q(SY, "Contextual synonym", A,
  SY_STEM + "The **surreptitious** glances that the clerk kept casting at the open safe made the guard suspicious.",
  ["furtive", "candid", "admiring", "indifferent"], 0,
  "Surreptitious = done secretly, so as not to be noticed",
  "The glances made the guard suspicious because they were secret and sly. 'Furtive' means secretive and sly, "
  "trying to avoid notice.",
  ["Effect: the guard became suspicious", "Glances meant not to be noticed", "Closest: 'furtive'"],
  "'Candid' (open) is the opposite. 'Admiring' and 'indifferent' do not explain why the guard grew suspicious.", 30)

Q(AN, "Contextual antonym", I,
  AN_STEM + "Though eighty, my grandfather is still **robust** and walks five kilometres every morning.",
  ["frail", "healthy", "cheerful", "tall"], 0,
  "Robust = strong and healthy; opposite: frail (weak and delicate)",
  "A man of eighty who walks five kilometres every day is strong and healthy, i.e. 'robust'. The opposite is "
  "'frail'.",
  ["Context: walks 5 km daily at eighty", "robust = strong and healthy", "Opposite: 'frail'"],
  "'Healthy' is close to a synonym. 'Cheerful' and 'tall' are not related to strength.", 25)

Q(AN, "Contextual antonym", I,
  AN_STEM + "Relations between the two firms were **cordial** for years, until a dispute over a contract soured "
  "them.",
  ["hostile", "friendly", "courteous", "lengthy"], 0,
  "Cordial = warm and friendly; opposite: hostile (unfriendly, antagonistic)",
  "The relations were warm and friendly until a dispute 'soured them'. The opposite of 'cordial' is 'hostile'.",
  ["Before the dispute: cordial", "cordial = warm and friendly", "Opposite: 'hostile'"],
  "'Friendly' and 'courteous' are close to synonyms. 'Lengthy' describes duration, not the warmth of relations.",
  25)

Q(AN, "Contextual antonym", A,
  AN_STEM + "Even when the crowd began shouting, the **phlegmatic** umpire calmly checked the replay before giving "
  "his decision.",
  ["excitable", "unhurried", "impartial", "experienced"], 0,
  "Phlegmatic = calm and not easily excited; opposite: excitable",
  "The umpire stayed calm while the crowd shouted, which is what 'phlegmatic' means. The opposite is 'excitable'.",
  ["Context: calm despite a shouting crowd", "phlegmatic = unemotional, calm", "Opposite: 'excitable'"],
  "'Unhurried' is close to the meaning, not opposite. 'Impartial' and 'experienced' describe other qualities of an "
  "umpire.", 30)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"
ID_STEM = "Choose the option that best expresses the meaning of the idiom in bold.\n"

Q(ID, "Meaning of idiom", B, "Choose the meaning of the idiom 'to cry over spilt milk'.",
  ["to regret something that has already happened and cannot be changed", "to waste food carelessly",
   "to complain about small household expenses", "to weep at a sad story"], 0,
  "Idiom: cry over spilt milk = be upset about something that cannot be undone",
  "Milk that has been spilt cannot be put back. To 'cry over spilt milk' is to waste time regretting something that "
  "cannot be changed.",
  ["Not literal", "Spilt milk = something done that cannot be undone", "Meaning: useless regret"],
  "The idiom is not about wasting food, household expenses or sad stories; these read it literally.", 20)

Q(ID, "Idiom in context", I,
  ID_STEM + "The landlord had already raised the rent twice that year, so his demand for an extra month's deposit "
  "was **the last straw**, and the tenants moved out.",
  ["the final problem in a series that makes a situation unbearable", "a small and harmless request",
   "the first sign of a coming quarrel", "a generous offer that was refused"], 0,
  "Idiom: the last straw = the last of a series of troubles, after which one cannot bear any more",
  "After two rent increases, one more demand was too much, and the tenants left. That final demand was 'the last "
  "straw'.",
  ["Earlier troubles: two rent rises", "One more demand → tenants leave", "Meaning: the final, unbearable problem"],
  "The demand came after earlier troubles, so it was not the 'first sign'. It drove the tenants away, so it was "
  "neither 'harmless' nor 'generous'.", 25)

Q(ID, "Meaning of idiom", A, "Choose the meaning of the idiom 'Hobson's choice'.",
  ["a situation in which there is only one option, so no real choice", "a choice made after careful thought",
   "a choice between two equally good options", "a choice that is made for someone by a friend"], 0,
  "Idiom: Hobson's choice = take what is offered or nothing",
  "The phrase comes from a stable-keeper who let customers take only the horse nearest the door, or none at all. A "
  "'Hobson's choice' is therefore no real choice.",
  ["Origin: take this one or none", "Only one option available", "Meaning: no real choice"],
  "'Careful thought', 'two equally good options' and a choice made by a friend all assume a real choice exists, "
  "which is exactly what the idiom denies.", 25)

Q(ID, "Idiom in context", A,
  ID_STEM + "After months of publicity, the much-awaited film festival turned out to be **a damp squib**: half the "
  "films never arrived and the halls were empty.",
  ["a disappointing failure", "a surprising success", "a quiet celebration", "an expensive luxury"], 0,
  "Idiom: a damp squib = something expected to be impressive that turns out to be a disappointment",
  "A squib is a small firework; a damp one fails to go off. After 'months of publicity', a festival with missing "
  "films and empty halls was a disappointing failure.",
  ["High expectation: months of publicity", "Outcome: films missing, halls empty", "Meaning: a disappointing "
   "failure"],
  "Empty halls rule out 'a surprising success'. A festival is not described as 'quiet', and cost is never "
  "mentioned.", 30)

Q(ID, "Idiom in context", A,
  ID_STEM + "Asked whether he supported the new tax, the MLA chose to **sit on the fence**, saying that both sides "
  "had valid points.",
  ["avoid taking either side", "strongly oppose the tax", "change his mind suddenly", "take a short break"], 0,
  "Idiom: sit on the fence = avoid committing oneself to either side",
  "By saying that 'both sides had valid points', the MLA avoided supporting or opposing the tax: he sat on the "
  "fence.",
  ["Clue: 'both sides had valid points'", "No clear position", "Meaning: avoid taking either side"],
  "Strong opposition is a clear position, the opposite of the idiom. Nothing suggests a sudden change of mind or a "
  "break.", 30)

Q(ID, "Meaning of idiom", A, "Choose the meaning of the idiom 'to carry coals to Newcastle'.",
  ["to supply something to a place or person that already has plenty of it",
   "to do hard physical work for very little pay",
   "to travel a long distance for an important purpose",
   "to bring bad news to someone who is far away"], 0,
  "Idiom: carry coals to Newcastle = do something pointless because what is brought is already plentiful there",
  "Newcastle in England was a great coal-mining town. Carrying coal there was pointless. The idiom means supplying "
  "something to a place that already has plenty of it.",
  ["Newcastle: a coal-mining centre", "Bringing coal there is pointless", "Meaning: supplying what is already "
   "plentiful"],
  "The idiom has nothing to do with low pay, long journeys or bad news; these read 'carrying coal' literally.", 30)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", B, OW_STEM + "A large building in which aircraft are kept and repaired",
  ["hangar", "hanger", "harbour", "garage"], 0,
  "One-word substitution: hangar (aircraft shed); do not confuse with hanger (for clothes)",
  "A 'hangar' is a large building where aircraft are housed and serviced.",
  ["Aircraft + large building", "'hangar'", "Spelling: -ar, not -er"],
  "A 'hanger' holds clothes, a 'harbour' shelters ships, and a 'garage' is for cars.", 20)

Q(OW, "Single word for a phrase", I, OW_STEM + "A person who walks while asleep",
  ["somnambulist", "insomniac", "ventriloquist", "hypochondriac"], 0,
  "One-word substitution: somn- (sleep) + ambul- (walk)",
  "'Somnambulist' (from Latin somnus, sleep, and ambulare, to walk) means a sleepwalker.",
  ["'somn-' = sleep", "'ambul-' = walk", "'somnambulist'"],
  "An 'insomniac' cannot sleep, a 'ventriloquist' makes his voice seem to come from elsewhere, and a "
  "'hypochondriac' constantly fears being ill.", 20)

Q(OW, "Single word for a phrase", A,
  OW_STEM + "A person who dislikes and distrusts other people and avoids their company",
  ["misanthrope", "philanthropist", "misogynist", "ascetic"], 0,
  "One-word substitution: mis- (hatred) + anthrop- (humankind)",
  "A 'misanthrope' dislikes humankind in general and avoids other people.",
  ["'mis-' = hatred", "'anthrop-' = humankind", "'misanthrope'"],
  "A 'philanthropist' loves people and helps them, a 'misogynist' dislikes women in particular, and an 'ascetic' "
  "gives up comforts for spiritual reasons, not out of dislike of people.", 25)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", B, AP_STEM + "We can solve this problem easily.",
  ["This problem can be solved easily.", "This problem can solved easily.", "This problem could be solve easily.",
   "This problem can be solving easily."], 0,
  "Passive with a modal: modal + be + past participle",
  "The object 'this problem' becomes the subject; 'can solve' becomes 'can be solved'. 'By us' may be left out "
  "because it adds nothing.",
  ["Object → subject: this problem", "can + be + past participle → can be solved", "'This problem can be solved "
   "easily.'"],
  "'Can solved' leaves out 'be'; 'could be solve' changes the modal and uses the base form; 'can be solving' uses "
  "the -ing form instead of the past participle.", 25)

Q(AP, "Voice conversion", I, AP_STEM + "It is time to close the shop.",
  ["It is time for the shop to be closed.", "It is time for the shop to close.",
   "It is time to be closed the shop.", "The shop is time to be closed."], 0,
  "Passive of 'It is time + to-infinitive': It is time for + object + to be + past participle",
  "The object of 'to close' is 'the shop'. In the passive, the infinitive becomes 'to be closed' and the shop is "
  "brought in with 'for': 'It is time for the shop to be closed.'",
  ["Infinitive with object: to close the shop", "Passive infinitive: to be closed", "'It is time for the shop to "
   "be closed.'"],
  "'For the shop to close' keeps an active infinitive (the shop closes itself). 'To be closed the shop' leaves the "
  "object after a passive verb. 'The shop is time ...' makes no sense.", 30)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", I, DS_STEM + 'He said to me, "Thank you for your help."',
  ["He thanked me for my help.", "He said me thank you for my help.", "He thanked to me for his help.",
   "He told me that thank you for his help."], 0,
  "Reporting thanks: 'said ... \"Thank you\"' becomes 'thanked'; pronouns change to suit the speaker and listener",
  "Words of thanks are reported with the verb 'thank'. 'Your help' (the listener's help) becomes 'my help' when "
  "the listener ('me') reports it: 'He thanked me for my help.'",
  ["Reporting verb: thanked", "'your help' → listener = me → 'my help'", "'He thanked me for my help.'"],
  "'Said me' is wrong ('say' does not take a person as object). 'Thanked to me' adds a wrong 'to', and 'his help' "
  "changes whose help it was. 'Told me that thank you' keeps the direct words inside a that-clause.", 30)

Q(DS, "Narration change", A,
  DS_STEM + 'She said to him, "You look tired. Why don\'t you rest for a while?"',
  ["She told him that he looked tired and suggested that he should rest for a while.",
   "She told him that he looks tired and asked why don't you rest for a while.",
   "She told him that he looked tired and suggested him to rest for a while.",
   "She said him that he looked tired and suggested that he should rest for a while."], 0,
  "Mixed narration: a statement (told ... that) + a suggestion ('Why don't you ...?' → suggested that ... should)",
  "'You look tired' is a statement: 'told him that he looked tired' (tense backshifted). 'Why don't you rest?' is "
  "a suggestion, not a real question, so it is reported with 'suggested that he should rest'.",
  ["Statement → told him that he looked tired", "'Why don't you ...?' = suggestion → suggested that he should ...",
   "Join the two with 'and'"],
  "Keeping 'looks' and 'why don't you' copies the direct words. 'Suggested him to rest' is wrong: 'suggest' takes "
  "a that-clause or -ing, not object + infinitive. 'Said him' is wrong ('say' needs 'to').", 40)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", B, SV_STEM + "The goods ______ loaded onto the lorry late last night.",
  ["were", "was", "is", "has"], 0,
  "'Goods' (merchandise) is always plural and takes a plural verb",
  "'Goods' has no singular form in this sense and is treated as plural; the time is past ('last night'): 'The goods "
  "were loaded ...'.",
  ["Subject: goods (plural only)", "Time: last night → past", "'were'"],
  "'Was' and 'is' are singular, and 'is' is also present. 'Has loaded' would make the goods do the loading.", 20)

Q(SV, "Agreement rules", I, SV_STEM + "The United States ______ a federal system of government.",
  ["has", "have", "are having", "were having"], 0,
  "A country's name that is plural in form takes a singular verb",
  "'The United States' names one country, so it takes a singular verb: 'The United States has a federal system of "
  "government.'",
  ["Subject: one country, plural in form", "Treated as singular", "'has'"],
  "'Have', 'are having' and 'were having' treat the country as plural; the last two also use 'have' (possess) in a "
  "continuous form.", 25)

Q(SV, "Agreement rules", A,
  SV_STEM + "All the riches of the old merchant ______ not able to buy him a single night of peaceful sleep.",
  ["were", "was", "is", "has"], 0,
  "'Riches' (wealth) is a plural noun and takes a plural verb",
  "'Riches' has no singular in this sense and is always plural, so the verb is plural; the story is in the past: "
  "'All the riches ... were not able to buy him ...'.",
  ["Subject: riches (plural only)", "'of the old merchant' does not change the number", "'were'"],
  "'Was' and 'is' treat 'riches' as singular. 'Has not able' is not a correct verb form.", 30)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Perfect tenses", B,
  TE_STEM + "So far this season, our school team ______ four matches and lost none.",
  ["has won", "had won", "wins", "is winning"], 0,
  "Present perfect with 'so far': a period that runs up to now",
  "'So far this season' covers the time from the start of the season up to now, which calls for the present "
  "perfect: 'has won four matches and (has) lost none'.",
  ["Time marker: so far (up to now)", "Present perfect: has + past participle", "'has won'"],
  "'Had won' needs a later past moment to refer to. 'Wins' and 'is winning' cannot count matches already played "
  "up to now.", 20)

Q(TE, "Perfect tenses", I,
  TE_STEM + "The window is still open and the jewellery box is empty; the thief seems ______ through the window.",
  ["to have escaped", "to escape", "escaping", "to be escaped"], 0,
  "Perfect infinitive (to have + past participle) for an action earlier than the main verb",
  "The seeming is present ('seems'), but the escape happened earlier. An earlier action after 'seem' takes the "
  "perfect infinitive: 'the thief seems to have escaped through the window.'",
  ["Main verb: seems (now)", "Escape: earlier", "Earlier action → perfect infinitive: 'to have escaped'"],
  "'To escape' would describe a present or habitual action. 'Seems escaping' is not standard, and 'to be escaped' "
  "is a wrong passive.", 30)

Q(TE, "Sequence of tenses", A,
  TE_STEM + "Yesterday morning, she assured her manager that by six o'clock that evening she ______ the report.",
  ["would have finished", "will have finished", "has finished", "had been finishing"], 0,
  "Sequence of tenses: future perfect seen from the past = would have + past participle",
  "Her promise was made in the past ('assured', 'yesterday morning') about a time that is also past now (six "
  "o'clock that evening). 'Will have finished' moves back to 'would have finished'.",
  ["Reporting verb: assured (past)", "Future perfect from a past viewpoint", "'would have finished'"],
  "'Will have finished' ignores the past reporting verb, and six o'clock yesterday is no longer in the future. 'Has "
  "finished' and 'had been finishing' do not express a promise about a deadline.", 35)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", B, AR_STEM + "Meena is ______ only daughter of her parents.",
  ["the", "a", "an", "no article"], 0,
  "'The' before 'only' when it picks out a single, particular person or thing",
  "'Only daughter' names the one and only daughter, so the definite article is needed: 'Meena is the only daughter "
  "of her parents.'",
  ["'only' = the single one", "A particular, unique person → the", "'the'"],
  "'A' and 'an' would suggest one of several, which contradicts 'only'. Without an article the noun phrase is "
  "incomplete.", 20)

Q(AR, "Definite and indefinite", I,
  AR_STEM + "______ Andaman and Nicobar Islands lie in ______ Bay of Bengal.",
  ["The, the", "No article, the", "The, no article", "An, the"], 0,
  "'The' with groups of islands and with bays named 'the Bay of ...'",
  "A group of islands takes 'the' (the Andaman and Nicobar Islands), and so does a bay named with 'of' (the Bay of "
  "Bengal).",
  ["Group of islands → the", "'Bay of ...' → the", "'The, the'"],
  "Dropping either 'the' breaks one of the two rules. 'An' is singular and cannot go with 'Islands'.", 25)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", I,
  PP_STEM + "The old soldier is blind ______ one eye but still reads the newspaper every morning.",
  ["in", "at", "from", "by"], 0,
  "Fixed preposition: blind in (one eye)",
  "Loss of sight in one eye is expressed as 'blind in one eye'.",
  ["Adjective: blind", "Part affected: one eye", "'blind in one eye'"],
  "'Blind at', 'blind from' and 'blind by' one eye are not used; 'blind to' means unwilling to notice something.",
  25)

Q(PP, "Phrasal verbs", A,
  PP_STEM + "By selling two of their goats, the family managed to ______ hunger until the next harvest.",
  ["stave off", "make off", "set off", "lay off"], 0,
  "Phrasal verb: stave off = keep something bad away for a time",
  "Selling the goats gave the family money for food, which kept hunger away until the harvest. To keep a danger at "
  "bay for a while is to 'stave it off'.",
  ["Action: sold goats for money", "Result: hunger kept away for a time", "'stave off'"],
  "'Make off' means run away, 'set off' means start a journey or cause (an alarm), and 'lay off' means dismiss "
  "workers; none means keeping hunger away.", 30)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"
CN_STEM = "Choose the connector that best fills the blank.\n"

Q(CN, "Sentence connectors", B, CN_STEM + "______ the bell rang, the children ran out of the classroom.",
  ["As soon as", "Unless", "Although", "So that"], 0,
  "'As soon as' = immediately after",
  "The children ran out immediately after the bell rang: 'As soon as the bell rang, the children ran out of the "
  "classroom.'",
  ["Event 1: the bell rang", "Event 2 follows at once: the children ran out", "'As soon as'"],
  "'Unless' sets a condition that does not fit a past event, 'Although' signals a contrast that is not there, and "
  "'So that' would make the bell ring for the purpose of the children running out.", 20)

Q(CN, "Starters and linkers", I,
  CN_STEM + "The scholarship is open only to first-time students; ______, anyone who has already earned a degree "
  "cannot apply.",
  ["in other words", "on the other hand", "even so", "by contrast"], 0,
  "'In other words' introduces a restatement of the same point",
  "'Open only to first-time students' and 'anyone who already has a degree cannot apply' say the same thing in two "
  "ways. A restatement is introduced by 'in other words'.",
  ["Clause 1: only first-time students", "Clause 2: graduates cannot apply (same rule)", "Restatement → 'in other "
   "words'"],
  "'On the other hand' and 'by contrast' signal a contrast, and 'even so' signals a surprising contrast; the "
  "second clause does not contrast with the first.", 25)

Q(CN, "Starters and linkers", A,
  CN_STEM + "The new rules will add to the paperwork of small lenders. ______, they will give depositors far better "
  "protection.",
  ["Be that as it may", "Inasmuch as", "Lest", "So long as"], 0,
  "'Be that as it may' = even though that is true (accepting a point, then moving to a stronger one)",
  "The opening sentence admits a drawback (more paperwork); the next gives an outweighing benefit. 'Be that as it "
  "may' accepts the first point and turns to the second.",
  ["Sentence 1: a drawback admitted", "Sentence 2: a benefit that outweighs it", "Concession → 'Be that as it may'"],
  "'Inasmuch as' (= because), 'Lest' (= for fear that) and 'So long as' (= provided that) introduce clauses, and "
  "none of them can open a full sentence that answers a drawback.", 30)
# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

# questions whose key was also recomputed by this script
RECOMPUTED = {(P3, 3), (P6, 2)}
# Every question was re-solved from a key-free dump by fresh checker agents (blind pass). Questions listed in
# NOT_BLIND_CONFIRMED (none at present) would keep only the author's own re-check.
NOT_BLIND_CONFIRMED = set()
for q in QS:
    vb = ["ai:author-solve"]
    if (q.get("stimulus_id"), q.get("set_position")) in RECOMPUTED:
        vb.append("script:recompute")
    vb.append("ai:self-recheck" if q["question_id"] in NOT_BLIND_CONFIRMED else "ai:independent-check")
    q["verification"]["verified_by"] = vb

# solutions must not point at an option by letter or position, because the script reorders options
POSITIONAL = re.compile(r"\b(the )?(first|second|third|fourth|last) (option|sentence|choice|pair|answer)\b|"
                        r"\b[Oo]ption [A-D]\b|\b(The|the) (first|second|third|fourth) (one|three|two)\b")
for q in QS:
    sol = q["solution"]
    prose = " ".join([sol["explanation"], sol["why_others_wrong"]] + sol["steps"])
    if q["_order"] != FIXED:
        assert not POSITIONAL.search(prose), (q["question_id"], POSITIONAL.search(prose).group(0))


def arrange(seed):
    """Place each correct option with a seeded shuffle; FIXED keeps the order, LAST_FIXED keeps option D in place."""
    rng = random.Random(seed)
    placed = []
    for q in QS:
        opts, ans = q["options"], q["correct_answer"]
        if q["_order"] == FIXED:
            perm = [0, 1, 2, 3]
        elif q["_order"] == LAST_FIXED:
            head = [0, 1, 2]
            rng.shuffle(head)
            perm = head + [3]
        else:
            perm = [0, 1, 2, 3]
            rng.shuffle(perm)
        placed.append(([opts[k] for k in perm], perm.index(ans)))
    return placed


for seed in range(10010, 15000):
    placed = arrange(seed)
    keys = Counter(LETTERS[a] for _, a in placed)
    # balanced overall, and no letter more than three times in a row
    run_ok = all(len(set(LETTERS[a] for _, a in placed[i:i + 4])) > 1 for i in range(len(placed) - 3))
    if max(keys.values()) <= 0.26 * len(QS) and min(keys.values()) >= 0.24 * len(QS) and run_ok:
        break
else:
    raise SystemExit("no balanced arrangement found")
for q, (opts, a) in zip(QS, placed):
    q["options"] = [{"key": LETTERS[i], "text": t} for i, t in enumerate(opts)]
    q["correct_answer"] = LETTERS[a]
    q["solution"]["final_answer"] = f"Option {LETTERS[a]}: {opts[a]}"
    del q["_order"]

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_010_plan.json").read_text(encoding="utf-8"))
eng = next(s for s in plan["subjects"] if s["subject"] == EN)
have = Counter((q["topic"], q["difficulty"]) for q in QS)
for t in eng["topics"]:
    for d, n in t["quota"].items():
        assert have[(t["topic"], d)] == n, (t["topic"], d, have[(t["topic"], d)], n)
    for q in QS:
        if q["topic"] == t["topic"]:
            assert q["subtopic"] in t["subtopics"], (q["topic"], q["subtopic"])
assert {q["topic"] for q in QS} <= {t["topic"] for t in eng["topics"]}
assert len(QS) == eng["total"] == 149
assert Counter(q["difficulty"] for q in QS) == Counter(eng["by_difficulty"])
assert QS[0]["question_id"] == eng["question_ids"][0] and QS[-1]["question_id"] == eng["question_ids"][1]
assert STIMULI[0]["stimulus_id"] == eng["stimulus_id_start"]

for s in STIMULI:
    words = len(s["content"].replace("*", "").split())
    assert 250 <= words <= 450, (s["stimulus_id"], words)
    members = [q for q in QS if q.get("stimulus_id") == s["stimulus_id"]]
    assert 3 <= len(members) <= 6, (s["stimulus_id"], len(members))
    assert [q["set_position"] for q in members] == list(range(1, len(members) + 1))
for q in QS:
    if q["topic"] == CL:
        n = q["set_position"]
        content = next(s["content"] for s in STIMULI if s["stimulus_id"] == q["stimulus_id"])
        assert f"({n})" in content and f"({n})" in q["question_text"], q["question_id"]
        size = sum(1 for x in QS if x.get("stimulus_id") == q["stimulus_id"])
        assert f"({size + 1})" not in content, q["stimulus_id"]
        if q["subtopic"] == "Error-based cloze":
            # the bold word quoted in the stem is the bold word in the passage
            bold = content.split(f"**({n}) ")[1].split("**")[0]
            assert f" {bold} " in q["question_text"].replace("'", " ").replace(",", " ").replace(".", " ").replace(":", " "), \
                (q["question_id"], bold)
    if q["topic"] == RC:
        # keep RC options similar in length so the key does not stand out
        lens = [len(o["text"]) for o in q["options"]]
        key_len = lens[LETTERS.index(q["correct_answer"])]
        assert key_len <= 1.35 * max(x for i, x in enumerate(lens) if LETTERS[i] != q["correct_answer"]), \
            (q["question_id"], lens)
    if q["topic"] == ED:
        assert q["options"][3]["text"] == "No error"
        assert (q["subtopic"] == "Error-free sentence") == (q["correct_answer"] == "D"), q["question_id"]
    if q["topic"] in (SI, PR) or (q["topic"] == CL and q["subtopic"] == "Error-based cloze"):
        assert q["options"][3]["text"] in (NI, NR), q["question_id"]
    if q["topic"] in (PJ, SR):
        labels = sorted(q["options"][0]["text"])
        assert all(sorted(o["text"]) == labels and len(set(o["text"])) == len(labels) for o in q["options"])
        for lab in labels:
            assert f"({lab})" in q["question_text"], (q["question_id"], lab)
    if q["topic"] == WU and q["subtopic"] == "Word swap":
        assert q["options"][3]["text"] == "No swap required", q["question_id"]
    assert len({o["text"] for o in q["options"]}) == 4, q["question_id"]
    # option letters are never named in the solution text, so option order can change without breaking it
    sol = q["solution"]
    prose = " ".join([sol["explanation"], sol["why_others_wrong"]] + sol["steps"])
    if q["topic"] != ED:
        for lab in LETTERS:
            assert f"Option {lab}" not in prose and f"option {lab}" not in prose, (q["question_id"], lab)

# no reused stem or passage title across the earlier English files (BATCH_000 to BATCH_009)
earlier, titles = set(), set()
EARLIER_DATA = [json.loads((ROOT / "batches" / f).read_text(encoding="utf-8")) for f in EARLIER]
for data in EARLIER_DATA:
    for q in data["questions"]:
        if q["subject"] == EN:
            earlier.add(q["question_text"].strip().lower())
    titles |= {s["title"].lower() for s in data.get("stimuli", []) if s["stimulus_id"].startswith("STIM_ENG")}
for s in STIMULI:
    assert s["title"].lower() not in titles, s["title"]

# theme check: a passage's keywords (words of 5+ letters used 2+ times, minus common words) must not largely coincide
# with those of any earlier English passage. Calibrated on BATCH_000-004: it rejects a deposit-insurance passage
# against 'A net or a hammock' (6 of 12 keywords shared), while unrelated passages share at most 3. Extended to
# BATCH_009 for this batch.
STOP = set("about after again against among because before being between bring could every first found great large "
           "later might money other people place price prices still their there these thing those three through "
           "under until where which while whose would years often never since cannot always".split())


def theme_words(text):
    words = [w.strip(".,;:'\"()!?*-—–").lower() for w in text.split()]
    counts = Counter(w for w in words if len(w) >= 5 and w.isalpha() and w not in STOP)
    return {w for w, n in counts.items() if n >= 2}


earlier_themes = {}
for data in EARLIER_DATA:
    for st in data.get("stimuli", []):
        if st["stimulus_id"].startswith("STIM_ENG"):
            earlier_themes[st["title"]] = theme_words(st["content"])
for s in STIMULI:
    mine = theme_words(s["content"])
    for title, theirs in earlier_themes.items():
        shared = mine & theirs
        assert len(shared) < 4 and len(shared) < 0.4 * len(mine), (s["title"], title, sorted(shared))
for q in QS:
    if q.get("stimulus_id") is None and q["topic"] not in (SC, WU, VO):  # shared fixed stems are allowed there
        assert q["question_text"].strip().lower() not in earlier, q["question_id"]
stems = [q["question_text"] for q in QS if q.get("stimulus_id") is None and q["topic"] not in (SC, WU, VO)]
assert len(stems) == len(set(stems)), "repeated stem inside this batch"

# earlier-key / bold-word repeat scan: no word, idiom or phrase keyed or tested in BATCH_000 to BATCH_009 is keyed or
# tested again. Covers the keys of the vocabulary-type topics, the bold words of Synonyms / Antonyms / Idioms /
# Phrase Replacement, the quoted word of Word Usage / Vocabulary / idiom-meaning stems and RC vocabulary-in-context.
KEYED_TOPICS = {SY, AN, VO, OW, ID, FB, PR}
BOLD_TOPICS = {SY, AN, ID, PR}
SKIP_KEYS = {NI.lower(), NR.lower(), "no swap required", "no error"}


def tested_words(q):
    """(keyed texts, tested words) of one question, lower-cased."""
    text = q["question_text"]
    keyed, tested = set(), set()
    if q["topic"] in KEYED_TOPICS:
        key = q["correct_answer"]
        opts = q["options"]
        k = next(o["text"] for o in opts if o["key"] == key) if isinstance(key, str) else opts[key]
        if k.lower() not in SKIP_KEYS:
            keyed.add(k.lower().strip())
    if q["topic"] in BOLD_TOPICS:
        tested |= {m.lower().strip() for m in re.findall(r"\*\*(.+?)\*\*", text)}
    if q["topic"] in (WU, VO, ID) or q.get("subtopic") == "Vocabulary in context":
        m = re.search(r"(?:the word|the idiom|to) '([^']+)'", text) or re.search(r"the word '([^']+)'", text)
        if m and q["topic"] != VO:
            tested.add(m.group(1).lower())
        if q["topic"] == VO:
            m2 = re.search(r"the word '([^']+)'", text)
            if m2:
                tested.add(m2.group(1).lower())
    return keyed, tested


earlier_keyed, earlier_tested = set(), set()
for data in EARLIER_DATA:
    for q in data["questions"]:
        if q["subject"] == EN:
            k, t = tested_words(q)
            earlier_keyed |= k
            earlier_tested |= t
for q in QS:
    k, t = tested_words(q)
    for w in k:
        assert w not in earlier_keyed and w not in earlier_tested, (q["question_id"], "key repeats", w)
    for w in t:
        assert w not in earlier_tested and w not in earlier_keyed, (q["question_id"], "tested word repeats", w)

keys = Counter(q["correct_answer"] for q in QS)
assert max(keys.values()) <= 0.28 * len(QS) and min(keys.values()) >= 0.22 * len(QS), keys

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_010",
    "created_at": TODAY,
    "notes": "BATCH_010 English Language part: 149 original questions (BANK_ENG_001352 to BANK_ENG_001500). Six "
             "reading passages (34 questions) and three cloze passages (17 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 to BATCH_009; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules, words and idioms not tested in earlier batches "
             "(checked by the builder against all earlier keyed and bold words). Each answer was set by the author "
             "and re-solved in a separate blind pass by fresh checkers without the key; the calibration record (RC 3) "
             "and the screening-test share (RC 6) are also recomputed by the builder. Pending human review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_010_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))}, seed {seed})")
