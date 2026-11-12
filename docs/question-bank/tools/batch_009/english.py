"""Writes batches/parts/BATCH_009_ENG.json: the 149 English Language questions of BATCH_009.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000 to BATCH_008 (passages and para-jumble topics), and the grammar rules, idioms and words tested are ones not
tested in those batches. Run from anywhere:

    python docs/question-bank/tools/batch_009/english.py

Structural checks (quota per topic and difficulty, subtopics, ID range, passage length, set sizes, option count, cloze
blank numbering, 'No error' / 'No replacement' / 'No swap' placement, para-jumble option validity, RC option-length
spread, repeated stems, passage titles and passage themes against all earlier English files, keyed words and bold
words against all earlier English files, answer-key balance) and the computable answers (the sari discount in RC 3
and the guarantor's liability in RC 4) are asserted before anything is written. Option letters are never named in
solutions (except the fixed parts A/B/C of Error Detection), and solutions never refer to an option by its position,
so the script places the correct option itself (seeded shuffle) to keep the answer keys balanced.
"""

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
EN = "English Language"
LETTERS = "ABCD"
FIRST_ID = 1203
FIRST_STIM = 9001
EARLIER = ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json", "parts/BATCH_002_ENG.json",
           "parts/BATCH_003_ENG.json", "parts/BATCH_004_ENG.json", "parts/BATCH_005_ENG.json",
           "parts/BATCH_006_ENG.json", "parts/BATCH_007_ENG.json", "parts/BATCH_008_ENG.json")

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
                         "verified_by": ["ai:author-solve", "ai:independent-check"], "verified_at": TODAY},
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
P1 = stim("A bite in the dark", (
    "Every year, thousands of people in rural India die after being bitten by snakes, and many more are left with "
    "damaged limbs. Most of the victims are farmers and farm workers, bitten while cutting crops, walking along field "
    "bunds at night or sleeping on the floor of their huts. The monsoon months, when rain floods the burrows of rats "
    "and drives out the snakes that hunt them, are the most dangerous.\n\n"
    "Doctors say that most of these deaths can be prevented. An effective medicine, antivenom, has been available for "
    "decades and is produced in India. It works best when it is given early, ideally within a few hours of the bite. "
    "The tragedy is that many victims never reach a hospital in time.\n\n"
    "One reason is distance. A village may be an hour or more from the nearest health centre that stocks antivenom. "
    "Another is belief. Many families first take the victim to a local healer, who may cut the wound, apply herbs or "
    "tie a tight cloth above the bite. Precious hours are lost, and some of these treatments cause harm of their "
    "own.\n\n"
    "Health workers are trying to change this through simple advice. A person who has been bitten should stay calm "
    "and keep the bitten limb still, because movement helps the venom spread through the body. Rings and bangles "
    "should be removed before the limb swells. The victim should be carried, not made to walk, to a hospital as "
    "quickly as possible. Trying to suck out the venom or cutting the wound does no good.\n\n"
    "Prevention matters too. Wearing boots in the fields, carrying a torch at night and sleeping on a raised cot "
    "rather than on the floor greatly reduce the risk. These are small habits, but in a country where snakes and "
    "people share the same fields, they can be the difference between life and death."))

Q(RC, "Factual", B,
  "According to the passage, when is the danger of snakebite the greatest?",
  ["During the monsoon, when rain floods the burrows of rats",
   "During the winter, when farmers sleep indoors",
   "During the summer, when village wells run dry",
   "During the harvest festival, when crowds gather"], 0,
  "Locating a stated fact",
  "Paragraph 1: 'The monsoon months, when rain floods the burrows of rats and drives out the snakes that hunt them, "
  "are the most dangerous.'",
  ["Find 'the most dangerous' in paragraph 1", "It refers to the monsoon months", "Reason: flooded rat burrows"],
  "Winter, summer and festivals are never mentioned as dangerous times; the passage names only the monsoon months.",
  35, P1, 1)

Q(RC, "Factual", B,
  "According to the passage, when does antivenom work best?",
  ["When it is given early, within a few hours of the bite",
   "When it is mixed with herbs by a local healer",
   "When it is given only after the limb has swollen",
   "When it is taken regularly before going to the fields"], 0,
  "Locating a stated fact",
  "Paragraph 2: antivenom 'works best when it is given early, ideally within a few hours of the bite.'",
  ["Find 'antivenom' in paragraph 2", "Read the sentence after it", "Given early, within a few hours"],
  "Herbs are mentioned only as a healer's treatment that wastes time. Waiting for swelling contradicts 'given "
  "early'. Taking it before going to the fields is never suggested.", 35, P1, 2)

Q(RC, "Factual", B,
  "Which of the following is NOT advised in the passage for a person who has been bitten by a snake?",
  ["Keeping the bitten limb still",
   "Removing rings and bangles before the limb swells",
   "Being carried to a hospital as quickly as possible",
   "Sucking the venom out of the wound"], 3,
  "Factual (NOT) question: eliminate every option the passage advises",
  "Paragraph 4 advises keeping the limb still, removing rings and bangles and carrying the victim to hospital. It "
  "says that trying to suck out the venom 'does no good'.",
  ["Limb still: advised", "Rings and bangles removed: advised", "Carried to hospital: advised",
   "Sucking out venom: 'does no good'"],
  "Keeping the limb still, removing rings and bangles and carrying the victim to hospital are all advised in "
  "paragraph 4, so none of them can be the answer.", 40, P1, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'Precious' as used in the passage ('Precious hours are "
  "lost')?",
  ["valuable", "needless", "peaceful", "ordinary"], 0,
  "Vocabulary in context: precious = of great value, not to be wasted",
  "Antivenom works best within a few hours, so every hour after a bite is of great value. Hours spent at a healer's "
  "are 'precious' hours lost: valuable time.",
  ["Context: antivenom works best within a few hours", "So each hour matters greatly", "'valuable'"],
  "The hours are badly needed, not 'needless', and 'peaceful' and 'ordinary' say nothing about their importance.",
  30, P1, 4)

Q(RC, "Inference", B,
  "Why, according to the passage, should a snakebite victim be carried rather than made to walk?",
  ["Walking moves the limb, which helps the venom spread.",
   "Walking makes the victim reach the hospital too late at night.",
   "Hospitals do not admit patients who arrive on foot.",
   "Carrying the victim keeps the wound clean of mud."], 0,
  "Inference: linking two pieces of advice in the same paragraph",
  "Paragraph 4 says the bitten limb should be kept still 'because movement helps the venom spread'. Walking would "
  "move the limb, so the victim should be carried.",
  ["Advice: keep the bitten limb still", "Reason: movement spreads the venom", "Walking = movement → carry the "
   "victim"],
  "Time of night and hospital rules are never mentioned. Mud and clean wounds are not discussed; the reason given "
  "is that movement spreads the venom.", 40, P1, 5)

Q(RC, "Tone and title", B,
  "Which of the following is the most suitable title for the passage?",
  ["Saving Lives After a Snakebite", "The Snakes of India's Forests", "Village Healers and Their Herbs",
   "How Antivenom Is Manufactured"], 0,
  "Title: the idea that runs through every paragraph",
  "The passage describes snakebite deaths, says most can be prevented, explains why victims reach hospital late, "
  "gives first-aid advice and ends with prevention. Its concern throughout is saving lives.",
  ["Para 1: the scale of the problem", "Paras 2-4: deaths are preventable; delays and advice",
   "Para 5: prevention: 'the difference between life and death'"],
  "The passage is about bites in farms and villages, not forest snakes. Healers appear in one paragraph only. How "
  "antivenom is made is never described.", 35, P1, 6)

# ---------------------------------------------------------------- RC 2 (Basic 4 + Intermediate 2)
P2 = stim("Homes without an address", (
    "Ask for directions in many Indian towns and you will hear something like this: 'Go past the temple, turn left "
    "at the big neem tree, and ask for the house with the blue gate behind the flour mill.' For the people who live "
    "there, such directions work well enough. For anyone else, they can be a puzzle.\n\n"
    "Millions of homes have no precise address. Streets may have no names, house numbers may be missing or follow no "
    "order, and the same name may be shared by two or three lanes. Local residents rarely notice the problem, "
    "because they know their neighbourhood by heart. It becomes serious only when a stranger must find a particular "
    "door quickly.\n\n"
    "An ambulance driver is the most obvious example. Every minute he spends asking shopkeepers for directions is a "
    "minute lost for the patient. Fire engines and police vans face the same difficulty. Delivery companies also "
    "lose money: a parcel that cannot be delivered must be carried back, stored and sent out again, and some of that "
    "cost is passed on to customers.\n\n"
    "The lack of an address can also shut people out. Opening a bank account, getting a gas connection or applying "
    "for a loan usually requires proof of where one lives. A family in an unnamed lane may find it hard to supply "
    "such proof, even if it has lived there for twenty years.\n\n"
    "Several solutions are being tried. Some towns are naming streets and fixing number plates on every building. "
    "Others are testing digital codes that identify a small square of land from map coordinates, so that any "
    "location can be described by a short string of letters and numbers, even where there are no street names at "
    "all. Such codes do not depend on local knowledge, but they work only if people know their own code and the "
    "services that need it can read it.\n\n"
    "An address, in short, is more than a line on an envelope. It is a way of being found."))

Q(RC, "Factual", B,
  "According to the passage, why do local residents rarely notice that their homes lack a proper address?",
  ["They know their neighbourhood by heart.",
   "They seldom receive any letters or parcels.",
   "Their town has already named all its streets.",
   "They always travel with a local guide."], 0,
  "Locating a stated reason",
  "Paragraph 2: 'Local residents rarely notice the problem, because they know their neighbourhood by heart.'",
  ["Find 'rarely notice' in paragraph 2", "Read the 'because' clause", "They know the area by heart"],
  "Receiving few letters and travelling with guides are never mentioned. If the streets were already named, there "
  "would be no problem to notice.", 35, P2, 1)

Q(RC, "Factual", B,
  "According to the passage, how does a parcel that cannot be delivered affect customers?",
  ["Part of the cost of returning and resending it is passed on to them.",
   "They must collect it themselves from the nearest police station.",
   "They are fined by the delivery company for a wrong address.",
   "They receive the parcel free of charge the next time."], 0,
  "Locating a stated consequence",
  "Paragraph 3: the parcel 'must be carried back, stored and sent out again, and some of that cost is passed on to "
  "customers.'",
  ["Find 'parcel' in paragraph 3", "Costs: carried back, stored, sent again", "Some cost is passed on to customers"],
  "Collecting parcels from a police station, fines and free delivery are not mentioned anywhere in the passage.",
  35, P2, 2)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'obvious' as used in the passage ('An ambulance driver "
  "is the most obvious example')?",
  ["clear", "hidden", "unusual", "recent"], 0,
  "Vocabulary in context: obvious = easily seen or understood",
  "The ambulance driver is the example that comes to mind first and is easiest to see, because a delay can cost a "
  "life. 'Most obvious' means clearest.",
  ["Context: delay costs a patient's life", "Easiest example to see", "'clear'"],
  "'Hidden' is the opposite of obvious. 'Unusual' and 'recent' do not describe how easy the example is to see.",
  30, P2, 3)

Q(RC, "Factual", B,
  "Which of the following is NOT mentioned in the passage as something that usually requires proof of where one "
  "lives?",
  ["Opening a bank account", "Getting a gas connection", "Applying for a loan", "Booking a bus ticket"], 3,
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 4 lists opening a bank account, getting a gas connection and applying for a loan. Booking a bus ticket "
  "is never mentioned.",
  ["Bank account: stated", "Gas connection: stated", "Loan: stated", "Bus ticket: not in the passage"],
  "The bank account, the gas connection and the loan are all named in paragraph 4, so none of them can be the "
  "answer.", 35, P2, 4)

Q(RC, "Inference", I,
  "What does the passage suggest is the main limitation of the digital location codes?",
  ["They are useful only if residents know their codes and services can read them.",
   "They cannot describe places where streets have no names.",
   "They depend entirely on the knowledge of local shopkeepers.",
   "They are too long for most people to write on an envelope."], 0,
  "Inference: a limitation stated with 'but'",
  "Paragraph 5: the codes 'do not depend on local knowledge, but they work only if people know their own code and "
  "the services that need it can read it.' The condition after 'but' is their limitation.",
  ["Strength: no need for local knowledge", "'but' introduces the limitation", "Residents and services must both "
   "use the code"],
  "The codes work 'even where there are no street names' and 'do not depend on local knowledge', so two options "
  "contradict the passage. The codes are called 'a short string', so length is not a problem.", 45, P2, 5)

Q(RC, "Inference", I,
  "What does the author mean by the closing words 'It is a way of being found'?",
  ["An address lets services and institutions reach and recognise a person.",
   "An address helps lost travellers find their way back home.",
   "An address shows how long a family has lived in a town.",
   "An address allows the police to track people who move often."], 0,
  "Inference: the meaning of a summing-up sentence",
  "The passage shows that without an address, ambulances, fire engines and deliveries cannot find a home, and "
  "families cannot prove where they live to banks or gas agencies. Being 'found' means being reached and "
  "recognised by such services.",
  ["Paras 3-4: emergency services, deliveries, banks", "All need to locate or recognise a home",
   "'Being found' = being reachable and recognised"],
  "The passage is about others finding a home, not travellers finding their way. An address does not show how long "
  "a family has lived somewhere (paragraph 4 makes the opposite point). Tracking people is never discussed.",
  45, P2, 6)

# ---------------------------------------------------------------- RC 3 (Intermediate, 6)
MARKED, SALE = 6000, 4500
CUT_PCT = (MARKED - SALE) * 100 // MARKED
assert (MARKED - SALE) * 100 % MARKED == 0 and CUT_PCT == 25
WRONG_BASE_PCT = round((MARKED - SALE) * 100 / SALE)        # 33: the trap of dividing by the sale price
assert WRONG_BASE_PCT == 33

P3 = stim("The first number in the room", (
    "In a well-known kind of experiment, people are asked to write down the last two digits of their phone number "
    "and then to say how much they would pay for an ordinary item, such as a box of chocolates or a cordless mouse. "
    "The digits have nothing to do with the item, and everyone knows it. Yet, again and again, those whose digits "
    "are high offer noticeably more than those whose digits are low. A number that should carry no weight has "
    "quietly pulled their judgement towards itself.\n\n"
    "Psychologists call this anchoring. When we must estimate a value we are unsure of, we tend to start from "
    "whatever figure is in front of us and adjust from there, usually not far enough. The first number becomes an "
    "anchor, and our final answer stays within reach of its chain.\n\n"
    f"Sellers have long understood this. A shop that marks a sari at ₹{MARKED:,} and then 'reduces' it to "
    f"₹{SALE:,} is not only offering a discount; it is fixing ₹{MARKED:,} in the buyer's mind as the true value, so "
    f"that ₹{SALE:,} feels like a gain, whatever the sari is really worth. In negotiations, too, the side that names "
    "the first figure often gains an advantage, because the discussion that follows tends to circle around it. A "
    "seller who opens high, within reason, usually settles higher than one who opens modestly.\n\n"
    "Experts are not immune. In studies, experienced professionals asked to value a house or to fix a penalty have "
    "been swayed by figures they had been told were arbitrary. Knowing about the bias does not remove it, though it "
    "can weaken it.\n\n"
    "The most practical defence is to set one's own anchor before hearing anyone else's. A buyer who has checked "
    "prices in three shops, or a borrower who has worked out what monthly instalment she can afford before visiting "
    "a lender, enters the conversation with a figure of her own. The other side's anchor still pulls, but now it "
    "pulls against something."))

Q(RC, "Inference", I,
  "What do the phone-number experiments described in the passage show?",
  ["An unrelated number can influence how much people are willing to pay.",
   "People with high phone numbers usually have more money to spend.",
   "Most buyers can judge the true value of an ordinary item easily.",
   "People refuse to state a price when they are unsure of an item's value."], 0,
  "Inference: the point an example is meant to prove",
  "The digits 'have nothing to do with the item', yet people with high digits offer more. A number that 'should "
  "carry no weight' pulls their judgement towards itself.",
  ["The digits are irrelevant to the item", "Yet high digits → higher offers", "An irrelevant number sways the "
   "price people offer"],
  "The passage never links phone numbers to wealth; the digits are random. If buyers could judge value easily, the "
  "digits would not sway them. People do state prices in the experiment.", 45, P3, 1)

Q(RC, "Factual", I,
  f"In the sari example, the discount (the marked price minus the sale price) is what percentage of the marked "
  f"price of ₹{MARKED:,}?",
  [f"{CUT_PCT}%", f"{WRONG_BASE_PCT}%", "20%", "75%"], 0,
  "Percentage reduction = (marked price − sale price) ÷ marked price × 100",
  f"The reduction is ₹{MARKED:,} − ₹{SALE:,} = ₹{MARKED - SALE:,}. As a share of the marked price: "
  f"{MARKED - SALE:,} ÷ {MARKED:,} × 100 = {CUT_PCT}%.",
  [f"Reduction = {MARKED:,} − {SALE:,} = {MARKED - SALE:,}", f"Base = marked price {MARKED:,}",
   f"{MARKED - SALE:,} ÷ {MARKED:,} = 1/4 = {CUT_PCT}%"],
  f"{WRONG_BASE_PCT}% divides the reduction by the sale price instead of the marked price. 20% has no basis in the "
  f"figures. 75% is the sale price as a share of the marked price, not the discount.", 45, P3, 2,
  shortcut=f"{MARKED - SALE:,} is one quarter of {MARKED:,}, so the cut is {CUT_PCT}%.")

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'arbitrary' as used in the passage ('figures they had "
  "been told were arbitrary')?",
  ["chosen at random", "carefully calculated", "officially approved", "widely published"], 0,
  "Vocabulary in context: arbitrary = based on chance or whim, not on reason",
  "The point of the studies is that the figures had no real basis, yet they still swayed experts. 'Arbitrary' "
  "figures are ones chosen at random.",
  ["Context: figures that should not matter", "Yet they swayed experts", "'chosen at random'"],
  "If the figures were 'carefully calculated' or 'officially approved', being swayed by them would not show a "
  "bias. 'Widely published' says nothing about whether they had any basis.", 35, P3, 3)

Q(RC, "Inference", I,
  "According to the passage, why does a seller who opens high usually settle at a higher price?",
  ["The bargaining that follows tends to stay close to the first figure named.",
   "Buyers trust sellers who ask for more than the item is worth.",
   "A high opening figure shows that the seller has many other buyers.",
   "Buyers are not allowed to name a figure of their own."], 0,
  "Inference: applying the idea of an anchor to bargaining",
  "Paragraph 3: the side that names the first figure gains, 'because the discussion that follows tends to circle "
  "around it.' A high first figure keeps the final price high.",
  ["First figure = anchor", "Discussion circles around it", "High anchor → higher settlement"],
  "Trust, other buyers and rules against buyers' figures are never mentioned. In fact, paragraph 5 advises buyers "
  "to bring a figure of their own.", 40, P3, 4)

Q(RC, "Inference", I,
  "With which of the following statements would the author most probably agree?",
  ["Preparing a figure of one's own weakens, but does not cancel, the pull of an anchor.",
   "Experts are completely protected from anchoring by their long experience.",
   "Once people learn about anchoring, it no longer affects their judgement.",
   "Buyers should always let the seller name the first price."], 0,
  "Inference: the author's position, drawn from the last two paragraphs",
  "Paragraph 4: knowing about the bias 'does not remove it, though it can weaken it.' Paragraph 5: with a figure of "
  "one's own, the other side's anchor 'still pulls, but now it pulls against something.'",
  ["Para 4: the bias can be weakened, not removed", "Para 5: one's own figure resists the pull",
   "The pull remains, but it is reduced"],
  "'Experts are not immune', so they are not completely protected. Knowing about the bias 'does not remove it'. "
  "Letting the seller go first would hand him the anchor, the opposite of the author's advice.", 45, P3, 5)

Q(RC, "Tone and title", I,
  "Which of the following is the most suitable title for the passage?",
  ["The Pull of the First Number", "Why Discounts Are Always Genuine", "How Experts Value Houses",
   "Phone Numbers and Personal Wealth"], 0,
  "Title: the central idea of the whole passage",
  "Every paragraph is about how a first figure pulls later judgements towards it: in experiments, in shops, in "
  "negotiations, among experts, and how to resist it.",
  ["Para 1-2: anchoring explained", "Para 3-4: shops, bargaining, experts", "Para 5: defence against the anchor"],
  "The passage suggests discounts can mislead, not that they are always genuine. House valuation is one example "
  "in one sentence. Phone numbers are a random input, not a measure of wealth.", 35, P3, 6)

# ---------------------------------------------------------------- RC 4 (Intermediate 1 + Advanced 4)
LOAN, REPAID, INT_DUE = 500000, 200000, 30000
GUAR_DUE = LOAN - REPAID + INT_DUE
assert GUAR_DUE == 330000


def inr(n):
    """Indian digit grouping: 330000 -> 3,30,000."""
    s = str(n)
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


assert inr(LOAN) == "5,00,000" and inr(GUAR_DUE) == "3,30,000"

P4 = stim("The signature that binds", (
    "Few documents are signed as casually, or regretted as deeply, as a loan guarantee. A friend or relative needs a "
    "loan, the bank asks for a guarantor, and someone close to the borrower signs, often at the branch counter and "
    "often without reading the agreement. To the guarantor it feels like an act of friendship, a formality that "
    "costs nothing. It is, in fact, a promise to repay someone else's debt.\n\n"
    "The promise is not a weak one. In India, as in many other countries, the law treats a guarantor's liability as "
    "co-extensive with that of the borrower. If the borrower defaults, the lender is generally free to demand the "
    "money from the guarantor without first suing the borrower or selling his property. Suppose a man borrows "
    f"₹{inr(LOAN)}, repays ₹{inr(REPAID)} of the principal and then stops paying, leaving ₹{inr(INT_DUE)} of "
    f"interest unpaid. The bank may ask his guarantor for ₹{inr(GUAR_DUE)}, together with any further interest and "
    "charges it is entitled to recover.\n\n"
    "The consequences reach beyond money. A default by the borrower can be reported against the guarantor as well, "
    "and a person who has guaranteed one large loan may find banks reluctant to lend to her, because part of her "
    "capacity to borrow is already spoken for. In this sense a guarantee is a latent debt: it does not appear in "
    "one's own accounts, but it can surface at any time.\n\n"
    "Why, then, do so many people sign? Partly because refusing feels like an insult to the borrower. Partly because "
    "the risk seems remote: the borrower is a cousin with a steady job, or a friend whose business is doing well. "
    "Guarantees, however, are asked for precisely because lenders are not sure that the loan will be repaid.\n\n"
    "None of this means that one should never stand guarantee. It means that a guarantee deserves the same scrutiny "
    "as a loan of one's own. A careful guarantor reads the agreement, asks how the borrower plans to repay, keeps "
    "track of whether instalments are being paid, and signs only for an amount she could afford to lose."))

Q(RC, "Factual", I,
  "According to the passage, what may a lender generally do if the borrower defaults?",
  ["Demand the money from the guarantor without first suing the borrower.",
   "Approach the guarantor only after selling all of the borrower's property.",
   "Recover from the guarantor only the interest, not the principal.",
   "Cancel the guarantee and write off the whole of the loan."], 0,
  "Locating a stated fact",
  "Paragraph 2: 'the lender is generally free to demand the money from the guarantor without first suing the "
  "borrower or selling his property.'",
  ["Find 'If the borrower defaults' in paragraph 2", "Lender may go straight to the guarantor",
   "No need to sue the borrower first"],
  "Selling the borrower's property first is exactly what the lender need not do. The example makes the guarantor "
  "liable for principal and interest. Writing off the loan is never mentioned.", 40, P4, 1)

Q(RC, "Factual", A,
  "In the example in paragraph 2, if no further interest or charges are added, how much can the bank ask the "
  "guarantor to pay?",
  [f"₹{inr(GUAR_DUE)}", f"₹{inr(LOAN - REPAID)}", f"₹{inr(LOAN + INT_DUE)}", f"₹{inr(REPAID + INT_DUE)}"], 0,
  "Guarantor's liability = unpaid principal + unpaid interest (co-extensive with the borrower's)",
  f"Unpaid principal = ₹{inr(LOAN)} − ₹{inr(REPAID)} = ₹{inr(LOAN - REPAID)}. Adding the unpaid interest of "
  f"₹{inr(INT_DUE)} gives ₹{inr(GUAR_DUE)}, the figure the passage states.",
  [f"Unpaid principal: {inr(LOAN)} − {inr(REPAID)} = {inr(LOAN - REPAID)}", f"Add unpaid interest {inr(INT_DUE)}",
   f"Total: {inr(GUAR_DUE)}"],
  f"₹{inr(LOAN - REPAID)} leaves out the unpaid interest. ₹{inr(LOAN + INT_DUE)} ignores the "
  f"₹{inr(REPAID)} already repaid. ₹{inr(REPAID + INT_DUE)} adds the repaid amount instead of the unpaid one.",
  50, P4, 2)

Q(RC, "Inference", A,
  "What does the author imply by saying that part of a guarantor's 'capacity to borrow is already spoken for'?",
  ["Lenders treat the guarantee as a possible claim on her ability to repay her own loans.",
   "She has already borrowed money from the same bank for her own needs.",
   "She has promised in writing never to take out a loan of her own.",
   "The borrower has the right to use her savings without asking her."], 0,
  "Inference: the meaning of a figurative phrase in its context",
  "The sentence explains why banks are reluctant to lend to a guarantor. Since she may have to pay the guaranteed "
  "loan, banks count part of her repaying ability as already committed. The next sentence calls the guarantee 'a "
  "latent debt'.",
  ["Context: banks reluctant to lend to a guarantor", "Reason: she may have to pay the guaranteed loan",
   "Part of her repaying ability is already committed"],
  "Nothing says she has borrowed for herself or promised never to borrow. The borrower gets no right to her "
  "savings; the risk is that the lender may claim from her.", 50, P4, 3)

Q(RC, "Vocabulary in context", A,
  "Which of the following is closest in meaning to the word 'latent' as used in the passage ('a guarantee is a "
  "latent debt')?",
  ["present but not yet visible", "already fully repaid", "openly acknowledged", "legally invalid"], 0,
  "Vocabulary in context: latent = existing but hidden or not yet active",
  "The passage explains the word itself: the guarantee 'does not appear in one's own accounts, but it can surface "
  "at any time.' It is a debt that exists but is not yet visible.",
  ["Gloss after the colon: does not appear ... can surface", "Exists but hidden", "'present but not yet visible'"],
  "A debt that can 'surface at any time' is not 'already fully repaid', and one that 'does not appear' is not "
  "'openly acknowledged'. The passage stresses that the guarantee is binding, not 'legally invalid'.", 40, P4, 4)

Q(RC, "Tone and title", A,
  "Which of the following best describes the author's attitude towards standing guarantee for a loan?",
  ["Cautionary: it is not forbidden, but it should be weighed like one's own loan.",
   "Approving: it is a harmless act of friendship that costs nothing at all.",
   "Hostile: no sensible person should ever sign a guarantee for anyone.",
   "Indifferent: the risks are too small to deserve any real attention."], 0,
  "Tone: read the conclusion, where the author states a position",
  "The final paragraph says: 'None of this means that one should never stand guarantee. It means that a guarantee "
  "deserves the same scrutiny as a loan of one's own.' This is a warning, not a ban.",
  ["Paras 1-4: the hidden risks of guaranteeing", "Para 5: not 'never', but careful scrutiny",
   "Attitude: cautionary"],
  "The author calls the 'costs nothing' view a mistake, so the attitude is not approving. 'None of this means that "
  "one should never stand guarantee' rules out hostility. Spending a whole passage on the risks rules out "
  "indifference.", 45, P4, 5)

# ---------------------------------------------------------------- RC 5 (Advanced, 5)
P5 = stim("Each generation's normal", (
    "Ask an elderly fisherman on almost any Indian coast about the sea of his youth, and he will describe catches "
    "that sound like exaggerations: nets so heavy that three men struggled to haul them in, fish as long as a man's "
    "arm, sharks seen close to the shore. Ask his grandson, who fishes the same waters today, and he will describe a "
    "good day that his grandfather would have called a poor one. Yet the grandson does not feel that anything has "
    "been lost. The sea he knows is the only sea he has known.\n\n"
    "The fisheries scientist Daniel Pauly gave this pattern a name in the 1990s: the shifting baseline. Each "
    "generation, he argued, takes the state of the world it first encounters as normal, and measures decline only "
    "from that point. Losses that happened before its time are invisible to it. Over several generations, a "
    "resource can be reduced to a fraction of its former abundance without any single generation witnessing a "
    "dramatic collapse.\n\n"
    "The idea reaches well beyond fishing. City dwellers who grew up under a hazy sky may regard a few clear days as "
    "unusually good rather than as what the sky once was. Birdwatchers who began counting a species when it was "
    "already scarce may record no fall at all. Even official targets can be affected: a plan to 'restore' a river to "
    "its condition of thirty years ago may aim at a state that was itself badly degraded.\n\n"
    "The difficulty is partly one of evidence. Older conditions were seldom measured with the care that today's "
    "surveys demand, and memories, as critics rightly point out, can be selective or romantic. An old man's "
    "recollection of giant fish is not data. But dismissing such accounts altogether carries its own risk, since it "
    "leaves the most recent, and most depleted, state as the only one that counts.\n\n"
    "Researchers have therefore turned to unconventional sources: old photographs of fishermen posing with their "
    "catch, market records, colonial gazetteers, even the menus of restaurants. None of these is precise, but "
    "together they can show the direction and rough size of a change that no living observer can see in full.\n\n"
    "The lesson is not that the past was always better. It is that our sense of what is normal is borrowed from a "
    "short span of experience, and that a society which wishes to protect what remains must first find out what "
    "has already gone."))

Q(RC, "Inference", A,
  "Why, according to the passage, does the young fisherman not feel that anything has been lost?",
  ["He judges the sea by the state in which he first came to know it.",
   "His catches are in fact larger than his grandfather's ever were.",
   "He does not believe his grandfather's stories about the past.",
   "He has moved to waters that were never fished in the past."], 0,
  "Inference: applying the 'shifting baseline' to the opening example",
  "'The sea he knows is the only sea he has known.' Paragraph 2 explains: each generation 'takes the state of the "
  "world it first encounters as normal'. The grandson's normal is already a depleted sea.",
  ["Para 1: the grandson's good day = the grandfather's poor day", "Para 2: each generation's first view = normal",
   "So the loss is invisible to him"],
  "His catches are smaller, not larger. The passage never says he disbelieves his grandfather; the point is that he "
  "has no memory of the earlier sea. He fishes 'the same waters'.", 50, P5, 1)

Q(RC, "Inference", A,
  "What does the example of the plan to 'restore' a river (paragraph 3) illustrate?",
  ["Targets for recovery may themselves be set from an already degraded state.",
   "Rivers recover faster than fisheries once pollution has been stopped.",
   "Official plans are usually based on very old and accurate records.",
   "Thirty years is long enough to measure any change in the natural world."], 0,
  "Inference: the purpose of an example",
  "The plan aims at the river's condition thirty years ago, but that condition 'was itself badly degraded'. The "
  "target is fixed from a baseline that had already shifted.",
  ["Restore to: the state of thirty years ago", "That state was already degraded",
   "The baseline problem affects official targets too"],
  "The speed of recovery is not discussed, and the passage says older conditions were 'seldom measured with the "
  "care' surveys now demand, so old records are not called accurate. The example suggests thirty years is too short "
  "a window, not long enough.", 50, P5, 2)

Q(RC, "Inference", A,
  "Which of the following best describes the author's view of the old fishermen's memories?",
  ["They are not data, but they should be weighed rather than dismissed.",
   "They are exaggerations that researchers should simply ignore.",
   "They are more reliable than any modern scientific survey.",
   "They are the only evidence of past conditions that survives."], 0,
  "Inference: a balanced position stated with 'But'",
  "Paragraph 4 concedes that 'An old man's recollection of giant fish is not data', but warns that 'dismissing such "
  "accounts altogether carries its own risk'. The author wants them treated with care, not thrown out.",
  ["Concession: memories can be selective, not data", "'But' dismissing them is risky",
   "Position: weigh them, do not ignore them"],
  "The author warns against ignoring them and does not rank them above surveys. Paragraph 5 lists other sources "
  "(photographs, market records, gazetteers, menus), so they are not the only evidence.", 50, P5, 3)

Q(RC, "Vocabulary in context", A,
  "Which of the following is closest in meaning to the word 'depleted' as used in the passage ('the most recent, "
  "and most depleted, state')?",
  ["greatly reduced", "carefully recorded", "recently restored", "widely admired"], 0,
  "Vocabulary in context: depleted = reduced in quantity, used up",
  "The passage describes a resource reduced generation after generation, so the most recent state is the one with "
  "the least left: the most depleted, or most greatly reduced.",
  ["Theme: steady decline over generations", "Latest state = lowest point", "'greatly reduced'"],
  "Nothing in the passage suggests the latest state is restored or admired. 'Carefully recorded' is about "
  "measurement, while the word describes how much of the resource is left.", 40, P5, 4)

Q(RC, "Tone and title", A,
  "Which of the following is the most suitable title for the passage?",
  ["The Normal That Keeps Moving", "Why Old Fishermen Exaggerate", "The Golden Age of Indian Fisheries",
   "How Surveys Replaced Memory"], 0,
  "Title: the central idea, not one example or a claim the author rejects",
  "The passage explains how each generation's idea of 'normal' shifts downward, hiding long-term losses, and how "
  "researchers try to recover older baselines.",
  ["Central idea: the shifting baseline", "Examples: fishing, skies, birds, rivers",
   "Conclusion: our sense of normal comes from a short span"],
  "The author does not say the fishermen exaggerate, and says 'The lesson is not that the past was always better', "
  "which rules out a golden-age title. Surveys have not replaced memory; the author wants both, plus other "
  "sources.", 40, P5, 5)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic 4 + Intermediate 1)
C1 = stim("A string with an edge", (
    "On festival days in many towns, the sky fills with kites, and on the rooftops below, children and adults battle "
    "to cut one another's strings. To win these contests, many fliers use a string coated with powdered glass. Such a "
    "string can (1) ______ through a rival's thread in seconds, and the winner's shout of triumph rings across the "
    "lanes.\n\n"
    "The same sharpness makes it dangerous. Every season, thousands of birds, especially pigeons and black kites, "
    "fly into loose strings that hang from trees, poles and wires, and many of them die of their (2) ______. Strings "
    "stretched across roads have also cut the necks of people riding two-wheelers, sometimes fatally.\n\n"
    "Several states have banned glass-coated string, and some cities have gone further, banning strings made of "
    "nylon and other synthetic materials, which do not snap easily. Yet the ban is hard to (3) ______. The string is "
    "cheap, it is sold quietly from small shops and homes, and demand rises sharply in the few days before the "
    "festival, when the police have many other duties.\n\n"
    "Volunteers have stepped in where the law falls short. In some cities, groups set up bird-rescue camps where "
    "vets stitch the wounds of injured birds and release them once they have healed. Others go from roof to roof "
    "after the festival, collecting the tangled string that would otherwise (4) ______ hanging from trees and wires "
    "for months.\n\n"
    "Many riders now fix a thin metal rod in front of the handlebar of their scooters, which catches any string "
    "before it reaches the rider's neck. Such rods help, but doctors and police (5) ______ that the safest solution "
    "is a simple one: fly kites with plain cotton thread, which breaks long before it can wound."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["slice", "melt", "wander", "float"], 0,
  "Cloze: what a sharp string does to another thread",
  "A glass-coated string is sharp and is used to cut a rival's thread quickly. A sharp edge 'slices through' a "
  "thread.",
  ["Purpose: to cut one another's strings", "Glass coating = sharp edge", "'slice through'"],
  "Strings do not 'melt', 'wander' or 'float' through a thread, and none of these would let the flier win by "
  "cutting.", 25, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["injuries", "songs", "nests", "colours"], 0,
  "Cloze: the cause of death after being caught in a sharp string",
  "The paragraph is about the danger of the sharp string. Birds caught in it are cut and many 'die of their "
  "injuries'.",
  ["Topic: 'The same sharpness makes it dangerous'", "Birds are cut by the string", "'die of their injuries'"],
  "Birds do not die of their 'songs', 'nests' or 'colours'; none of these is caused by a sharp string.", 25, C1, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["enforce", "admire", "describe", "repeat"], 0,
  "Cloze: the sentences after 'Yet' explain the difficulty",
  "The string is cheap, sold quietly and in high demand while the police are busy. These are reasons why a ban is "
  "hard to put into effect: hard to 'enforce'.",
  ["'Yet' = despite the ban", "Reasons: cheap, sold quietly, police busy", "Hard to make the ban work → 'enforce'"],
  "Nothing about the cheap, quietly sold string makes a ban hard to 'admire', 'describe' or 'repeat'; the reasons "
  "listed are all about making the ban work.", 30, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["remain", "vanish", "travel", "shrink"], 0,
  "Cloze: what uncollected string would do",
  "Volunteers collect the string because otherwise it would stay where it is: it would 'remain hanging from trees "
  "and wires for months'.",
  ["'would otherwise ___ hanging ... for months'", "Uncollected string stays put", "'remain'"],
  "If the string would 'vanish', there would be no need to collect it. 'Travel hanging' and 'shrink hanging' make "
  "no sense with 'for months'.", 25, C1, 4)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=5), ["insist", "deny", "forget", "regret"], 0,
  "Cloze: experts stating a firm opinion",
  "Doctors and police strongly hold the view that cotton thread is the safest solution. They 'insist that' it is "
  "so.",
  ["'Such rods help, but ...'", "Experts firmly recommend cotton thread", "'insist that'"],
  "'Deny that the safest solution is ...' would reject the advice that the sentence goes on to give. 'Forget' and "
  "'regret' do not fit people recommending a solution.", 25, C1, 5)

# ---------------------------------------------------------------- Cloze 2 (Intermediate, 5)
C2 = stim("The case for the roundabout", (
    "At a busy crossroads controlled by traffic lights, drivers spend much of their time waiting. Even when no "
    "vehicle is coming from any other direction, a red light holds them back until it (1) ______. A well-designed "
    "roundabout works differently. Vehicles entering it give way to the traffic already circling and then move on as "
    "soon as there is a gap, so that at quiet hours almost nobody has to stop at all.\n\n"
    "Safety experts value roundabouts for a further reason. At an ordinary crossing, the most serious crashes are "
    "side-on or head-on collisions between vehicles moving at speed. A roundabout (2) ______ such crashes almost "
    "impossible: all traffic moves in one direction, and the curve forces drivers to slow down. Accidents still "
    "happen, but they tend to be minor scrapes rather than deadly impacts.\n\n"
    "Roundabouts are not a cure for every junction, however. When traffic is very heavy on one road and light on the "
    "others, the busy stream may never leave a gap, and vehicles on the quieter roads can wait for a long time. Large "
    "roundabouts can also be hard for pedestrians and cyclists to (3) ______, since there is no pause in the flow of "
    "vehicles. In many cities, such circles have been fitted with traffic lights for the rush hours, which "
    "(4) ______ much of their advantage.\n\n"
    "Much also depends on drivers. A roundabout works only if those entering it actually give way. Where drivers "
    "push in regardless, the circle quickly becomes a knot of vehicles, each blocking the next. Engineers therefore "
    "stress that good design must be (5) ______ by clear signs, road markings and the steady enforcement of one "
    "simple rule: give way to the traffic already on the circle."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["changes", "dims", "fails", "glows"], 0,
  "Cloze: what releases drivers waiting at a red light",
  "Drivers wait at a red light even when the road is empty; they can move only when the light turns green, that is, "
  "when it 'changes'.",
  ["'a red light holds them back until it ___'", "Drivers go when the light turns green", "'changes'"],
  "A light that 'dims' or 'glows' is still red. A light that 'fails' is a fault, not the normal event drivers wait "
  "for.", 30, C2, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["makes", "takes", "gives", "holds"], 0,
  "Cloze: verb + object + adjective ('make something impossible')",
  "The pattern 'make + object + adjective' means cause it to become so: a roundabout 'makes such crashes almost "
  "impossible', because all traffic moves one way.",
  ["Pattern: ___ such crashes almost impossible", "make + object + adjective", "'makes'"],
  "'Takes', 'gives' and 'holds' are not used with an object followed by an adjective to mean 'cause to become'.",
  30, C2, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["cross", "see", "clean", "light"], 0,
  "Cloze: the reason clause decides the word",
  "'Since there is no pause in the flow of vehicles', people on foot or on cycles find large roundabouts hard to get "
  "across: hard to 'cross'.",
  ["Reason: no pause in the flow of vehicles", "A continuous flow blocks those trying to get across", "'cross'"],
  "A continuous flow of vehicles does not make a roundabout hard to 'see', 'clean' or 'light'; it makes it hard to "
  "cross.", 30, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["cancels", "doubles", "explains", "reveals"], 0,
  "Cloze: the effect of adding traffic lights to a roundabout",
  "The roundabout's advantage is that vehicles need not wait for a light. Fitting lights brings the waiting back, "
  "which 'cancels much of their advantage'.",
  ["Advantage of a roundabout: no waiting at lights", "Adding lights brings back waiting", "'cancels'"],
  "Adding lights does not 'double' the advantage; it removes it. 'Explains' and 'reveals' do not fit an action that "
  "takes something away.", 30, C2, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["supported", "replaced", "delayed", "hidden"], 0,
  "Cloze: design needs help from signs and enforcement",
  "The paragraph says a roundabout works only if drivers give way, so design alone is not enough. It must be "
  "'supported by' signs, markings and enforcement.",
  ["Design alone fails if drivers push in", "Signs and enforcement add to the design", "'supported by'"],
  "Engineers would not want good design 'replaced', 'delayed' or 'hidden'; the signs and enforcement are meant to "
  "work along with it.", 30, C2, 5)

# ---------------------------------------------------------------- Cloze 3 (Intermediate 2 + Advanced 4; error-based)
C3 = stim("Holes that come back", (
    "Every monsoon, the roads of many Indian cities break out in potholes. They appear so **(1) regularly** that "
    "many residents treat them as a season of their own, like the rains that bring them. Yet potholes are not an act "
    "of nature. Engineers say that most of them can be traced to two causes: water and poor construction.\n\n"
    "A road surface is meant to shed rain into the drains along its edges. When the surface is laid without the "
    "proper slope, or when the drains are **(2) cleared**, water stands on the road and slowly seeps into small "
    "cracks. Heavy vehicles passing over the weakened patch press the water down and force it out again, loosening "
    "the stones beneath. Within days a crack can **(3) shrink** into a hole deep enough to throw a rider off a "
    "scooter.\n\n"
    "The usual response makes matters worse. Crews arrive after the rains, shovel loose material into the hole and "
    "press it down with a roller or even with their feet. Such patches are cheap and quick, but they rarely bond "
    "with the old surface, and the next heavy shower washes them out. The city then pays for the same hole again and "
    "again, a cycle that some critics believe is **(4) convenient** for contractors.\n\n"
    "Better methods exist. A pothole can be cut into a neat rectangle, cleaned, dried and filled with material that "
    "is pressed down in thin layers, so that the repair **(5) crumbles** for years. Some cities also write a defect "
    "liability period into road contracts, under which the contractor must repair, at his own cost, any damage that "
    "appears within a fixed number of years. Where such clauses are **(6) ignored**, contractors have a reason to "
    "build well the first time.\n\n"
    "Residents can help too. Several cities now allow people to photograph a pothole and report it through an app, "
    "and some publish how quickly each complaint is closed. Records of this kind make it harder for the same hole to "
    "be patched, forgotten and paid for, year after year."))

Q(CL, "Error-based cloze", I,
  ERR_STEM.format(n=1, ctx="They appear so regularly that many residents treat them as a season of their own"),
  ["rarely", "quietly", "cheaply", NR], 3,
  "Error-based cloze: 'so ... that' result must match the cause",
  "People treat potholes 'as a season of their own' because they come back every monsoon, i.e. they appear "
  "regularly. 'Regularly' fits.",
  ["Result: treated like a season", "A season comes back every year", "'regularly' fits → no replacement"],
  "If potholes appeared 'rarely', no one would treat them as a season. 'Quietly' and 'cheaply' do not explain the "
  "comparison with a season.", 35, C3, 1, order=LAST_FIXED)

Q(CL, "Error-based cloze", I,
  ERR_STEM.format(n=2, ctx="when the surface is laid without the proper slope, or when the drains are cleared, "
                          "water stands on the road"),
  ["blocked", "repaired", "numbered", NR], 0,
  "Error-based cloze: cause and effect must agree",
  "Water stands on the road when it cannot run off into the drains. Cleared drains would carry water away; drains "
  "that are 'blocked' make it stand.",
  ["Effect: water stands on the road", "Cause must stop drainage", "'cleared' → 'blocked'"],
  "'Repaired' drains would work better, not cause standing water. 'Numbered' has nothing to do with drainage. "
  "'Cleared' gives the opposite cause, so the word must be replaced.", 35, C3, 2, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=3, ctx="Within days a crack can shrink into a hole deep enough to throw a rider off a scooter"),
  ["widen", "harden", "dry", NR], 0,
  "Error-based cloze: a small crack becoming a deep hole",
  "A small crack that turns into a deep hole grows larger; it does not get smaller. The verb must be 'widen "
  "into'.",
  ["Start: small crack", "End: hole deep enough to throw a rider", "Growth → 'widen'"],
  "A crack does not 'harden' or 'dry' into a deep hole; neither describes growth. 'Shrink' contradicts the change "
  "from crack to hole.", 40, C3, 3, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=4, ctx="The city then pays for the same hole again and again, a cycle that some critics believe "
                          "is convenient for contractors"),
  ["costly", "harmful", "unknown", NR], 3,
  "Error-based cloze: read the critics' suspicion from the context",
  "Each time a patch washes out, the city pays again, and contractors earn again. Critics suspect the cycle suits "
  "contractors: it is 'convenient' for them. The word fits.",
  ["The city pays repeatedly", "Contractors are paid repeatedly", "The cycle suits them → 'convenient' is correct"],
  "The city, not the contractor, bears the cost, so 'costly' and 'harmful' for contractors miss the critics' point. "
  "'Unknown' makes no sense of a cycle the critics have noticed.", 40, C3, 4, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=5, ctx="filled with material that is pressed down in thin layers, so that the repair crumbles "
                          "for years"),
  ["lasts", "sinks", "bends", NR], 0,
  "Error-based cloze: the purpose of a better method",
  "The paragraph describes 'better methods'. Their purpose is a repair that holds 'for years': one that 'lasts'.",
  ["'Better methods exist'", "'so that' gives the purpose", "'crumbles' → 'lasts'"],
  "A repair that 'sinks' or 'bends' for years is a failed repair, not the aim of a better method. 'Crumbles' is "
  "the opposite of the purpose, so it must be replaced.", 40, C3, 5, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=6, ctx="Where such clauses are ignored, contractors have a reason to build well the first time"),
  ["enforced", "forgotten", "hidden", NR], 0,
  "Error-based cloze: a contract clause gives an incentive only if it is applied",
  "A contractor who must repair damage at his own cost has a reason to build well, but only where the clause is "
  "actually applied, i.e. 'enforced'.",
  ["Clause: contractor pays for later damage", "Incentive works only if the clause is applied", "'ignored' → "
   "'enforced'"],
  "Clauses that are 'forgotten' or 'hidden' give no incentive, just like ignored ones. 'Ignored' contradicts the "
  "result 'have a reason to build well'.", 40, C3, 6, order=LAST_FIXED)

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


# ---- Basic (4)
ed("Part-wise error", B, "Sunil is best player", "in our office", "cricket team.", "A",
   "A superlative adjective before a noun takes 'the'",
   "'Best' is a superlative and picks out one player from the team, so it needs 'the': 'Sunil is the best player in "
   "our office cricket team.'",
   ["'best' = superlative", "Superlative + noun → 'the'", "'is best player' → 'is the best player': error in part "
    "A"],
   "Part B is a correct place phrase. Part C correctly completes the noun phrase. A has an error, so 'No error' is "
   "wrong.", 25)

ed("Part-wise error", B, "When I was six,", "my grandfather learnt me", "how to ride a bicycle.", "B",
   "Learn = gain knowledge yourself; teach = give knowledge to someone else",
   "The grandfather gave the skill to the child, so the verb is 'teach': 'my grandfather taught me how to ride a "
   "bicycle.' One learns from someone; one teaches someone.",
   ["Who gives the skill? The grandfather", "Giving knowledge = teach", "'learnt me' → 'taught me': error in part B"],
   "Part A is a correct time clause. Part C ('how to ride a bicycle') correctly follows 'taught me'. B has an error, "
   "so 'No error' is wrong.", 25)

ed("Part-wise error", B, "After the long meeting,", "all the members went", "to home early.", "C",
   "'Home' after verbs of motion (go, come, return) takes no preposition",
   "'Home' here works as an adverb of place, so no 'to' is used: 'all the members went home early.'",
   ["Verb of motion: went", "go/come/return + home (no 'to')", "'to home' → 'home': error in part C"],
   "Part A is a correct time phrase. Part B has a correct subject and past tense. C has an error, so 'No error' is "
   "wrong.", 25)

ed("Error-free sentence", B, "Ravi, who lives next door,", "teaches mathematics", "at a college in the town.", "D",
   "Error-free sentence: check the relative clause, agreement and prepositions",
   "'Who lives next door' correctly describes Ravi and is set off by commas. 'Ravi ... teaches' is singular and "
   "agrees. 'Mathematics' is the subject taught, and 'at a college in the town' is correct.",
   ["'who lives' agrees with Ravi", "'Ravi teaches': singular verb", "'at a college in the town': correct"],
   "No part contains an error: the relative clause, the verb and the place phrase are all correct.", 25)

# ---- Intermediate (8)
ed("Part-wise error", I, "The train from Delhi", "arrived lately", "because of the thick fog.", "B",
   "Late (adverb) = after the expected time; lately = recently",
   "The train came after its expected time, which is 'late': 'The train from Delhi arrived late because of the thick "
   "fog.' 'Lately' means 'recently', as in 'I have not seen him lately.'",
   ["Meaning: after the scheduled time", "Adverb 'late', not 'lately' (recently)", "'arrived lately' → 'arrived "
    "late': error in part B"],
   "Part A is a correct subject. Part C correctly gives the reason. B has an error, so 'No error' is wrong.", 30)

ed("Part-wise error", I, "Most people in this town", "feel that the new mall", "is too much expensive.", "C",
   "'Too' + adjective is strengthened by 'much' placed before it: 'much too expensive', never 'too much expensive'",
   "'Too much' is used before nouns ('too much noise'). Before an adjective, the intensifier comes first: 'is much "
   "too expensive'.",
   ["'expensive' is an adjective", "Adjective → 'much too' + adjective", "'too much expensive' → 'much too "
    "expensive': error in part C"],
   "Part A is a correct subject phrase. Part B correctly introduces the clause. C has an error, so 'No error' is "
   "wrong.", 30)

ed("Part-wise error", I, "Before he moved to the village,", "the old man divided his savings",
   "equally among his two sons.", "C",
   "'Between' is used for two people or things; 'among' for more than two",
   "There are only two sons, so the savings are divided 'between' them: 'equally between his two sons.'",
   ["Number of sons: two", "Two → between; more than two → among", "'among his two sons' → 'between his two sons': "
    "error in part C"],
   "Part A is a correct time clause. Part B is a correct main clause. C has an error, so 'No error' is wrong.", 30)

ed("Part-wise error", I, "The flood victims were deprived from", "food and clean water", "for nearly three days.",
   "A",
   "Fixed preposition: deprive someone of something",
   "The verb 'deprive' takes 'of': 'The flood victims were deprived of food and clean water for nearly three days.'",
   ["Verb: deprive(d)", "Fixed pairing: deprived of", "'deprived from' → 'deprived of': error in part A"],
   "Part B is a correct object. Part C is a correct duration phrase. A has an error, so 'No error' is wrong.", 30)

ed("Part-wise error", I, "The new water filter consists from", "three layers of sand,", "gravel and charcoal.", "A",
   "Fixed preposition: consist of (be made up of)",
   "'Consist' takes 'of' when it lists parts: 'The new water filter consists of three layers of sand, gravel and "
   "charcoal.'",
   ["Verb: consist(s)", "Made up of → 'consist of'", "'consists from' → 'consists of': error in part A"],
   "Part B and part C correctly list the materials. A has an error, so 'No error' is wrong.", 30)

ed("Part-wise error", I, "The courier could not lift", "the parcel alone", "because it was such heavy.", "C",
   "'So' goes before an adjective alone; 'such' goes before a noun phrase (such a heavy parcel)",
   "'Heavy' is an adjective with no noun after it, so the intensifier is 'so': 'because it was so heavy.' 'Such' "
   "would need a noun: 'such a heavy parcel'.",
   ["After 'such': a noun phrase is needed", "Here only an adjective follows", "'such heavy' → 'so heavy': error in "
    "part C"],
   "Part A has a correct modal and verb. Part B is a correct object and adverb. C has an error, so 'No error' is "
   "wrong.", 30)

ed("Part-wise error", I, "Members are requested", "to refrain to smoke", "inside the reading room.", "B",
   "Fixed preposition: refrain from + -ing",
   "'Refrain' is followed by 'from' and a gerund: 'Members are requested to refrain from smoking inside the reading "
   "room.'",
   ["Verb: refrain", "Pattern: refrain from + -ing", "'to refrain to smoke' → 'to refrain from smoking': error in "
    "part B"],
   "Part A is a correct passive request. Part C is a correct place phrase. B has an error, so 'No error' is wrong.",
   30)

ed("Error-free sentence", I, "Whether he comes or not,", "the meeting will begin", "at ten sharp.", "D",
   "Error-free sentence: 'whether ... or not' clause + future in the main clause",
   "'Whether he comes or not' is a correct concessive clause, with the present tense for a future event. 'The "
   "meeting will begin at ten sharp' is a correct main clause.",
   ["'Whether ... or not': correct", "Present 'comes' in the subordinate clause, future 'will begin' in the main "
    "clause", "'at ten sharp': correct"],
   "No part has an error: the clause, the tenses and the time phrase are all correct.", 30)

# ---- Advanced (7)
ed("Part-wise error", A, "The leaking roof of the warehouse", "needs to repair", "before the monsoon arrives.", "B",
   "When the subject receives the action, 'need' takes a passive infinitive (needs to be repaired) or a gerund "
   "(needs repairing)",
   "The roof cannot repair anything; it is to be repaired. So the infinitive must be passive: 'needs to be repaired' "
   "(or 'needs repairing').",
   ["Subject 'the roof' receives the action", "Passive needed: to be repaired", "'needs to repair' → 'needs to be "
    "repaired': error in part B"],
   "Part A is a correct subject. Part C correctly uses the present tense in a time clause about the future. B has an "
   "error, so 'No error' is wrong.", 35)

ed("Part-wise error", A, "Having found cheaper software,", "the firm decided",
   "to dispense of its old accountant's services.", "C",
   "Fixed preposition: dispense with = do without, get rid of",
   "To stop using someone's services is to 'dispense with' them: 'the firm decided to dispense with its old "
   "accountant's services.'",
   ["Meaning: stop using, do without", "Fixed pairing: dispense with", "'dispense of' → 'dispense with': error in "
    "part C"],
   "Part A is a correct participle phrase whose subject is the firm. Part B is a correct main clause. C has an "
   "error, so 'No error' is wrong.", 35)

ed("Part-wise error", A, "The old farmer refused to part from", "the wooden plough",
   "that his father had made for him.", "A",
   "Part with = give up possession of a thing; part from = leave a person",
   "A plough is a thing he refuses to give up, so the phrase is 'part with': 'The old farmer refused to part with "
   "the wooden plough ...'. 'Part from' is used for leaving a person ('parted from his friends').",
   ["Object: a plough (a thing)", "Give up a thing → part with", "'part from' → 'part with': error in part A"],
   "Part B is a correct object. Part C correctly uses the past perfect for the earlier action. A has an error, so "
   "'No error' is wrong.", 35)

ed("Part-wise error", A, "He is an alumni", "of the same college", "where his father studied.", "A",
   "Alumnus (one person) / alumni (plural)",
   "'Alumni' is the plural of 'alumnus'. One person is 'an alumnus': 'He is an alumnus of the same college where his "
   "father studied.'",
   ["Subject: one person ('He')", "Singular: alumnus; plural: alumni", "'an alumni' → 'an alumnus': error in part A"],
   "Part B is a correct prepositional phrase. Part C is a correct relative clause. A has an error, so 'No error' is "
   "wrong.", 35)

ed("Part-wise error", A, "Watching the old craftsman at work,", "we could not but to admire",
   "the patience in his hands.", "B",
   "'Cannot but' (= cannot help) is followed by the bare infinitive, without 'to'",
   "'Cannot but' means 'cannot do anything except', and takes the bare infinitive: 'we could not but admire the "
   "patience in his hands.'",
   ["Expression: could not but", "Followed by bare infinitive", "'not but to admire' → 'not but admire': error in "
    "part B"],
   "Part A is a correct participle phrase with 'we' as its subject. Part C is a correct object. B has an error, so "
   "'No error' is wrong.", 40)

ed("Error-free sentence", A, "I have yet to receive", "a reply from the head office", "about my transfer request.",
   "D",
   "Error-free sentence: 'have yet to + verb' = have not done so far",
   "'I have yet to receive a reply' correctly means 'I have not received a reply so far'. 'From the head office' and "
   "'about my transfer request' are correct.",
   ["'have yet to receive': correct idiom", "'a reply from ...': correct", "'about my transfer request': correct"],
   "No part has an error. 'Have yet to' may look odd, but it is standard English.", 35)

ed("Error-free sentence", A, "Barely a month after it opened,", "the new branch had signed up",
   "over a thousand customers.", "D",
   "Error-free sentence: past perfect for a result reached by a past point in time",
   "'Barely a month after it opened' fixes a past point. By then the branch 'had signed up' over a thousand "
   "customers: the past perfect is correct. 'Over a thousand customers' is a correct plural object.",
   ["Past reference point: a month after opening", "Result completed by then: past perfect", "No agreement or "
    "preposition errors"],
   "No part has an error: 'barely' does not need inversion here because it modifies the time phrase, not the verb.",
   35)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", B,
  SI_STEM + "**Each students** of the class must bring a photograph for the identity card.",
  ["Each student", "Each of student", "Every students", NI], 0,
  "'Each' and 'every' are followed by a singular noun",
  "'Each' refers to members one at a time and takes a singular noun: 'Each student of the class must bring a "
  "photograph ...'.",
  ["Determiner: each", "each + singular noun", "'Each student'"],
  "'Each of student' needs 'the' and a plural (each of the students). 'Every students' repeats the same mistake. The "
  "original uses a plural noun, so 'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "It is getting dark; please **open the light** in the corridor.",
  ["switch on the light", "open on the light", "start the light", NI], 0,
  "Lights and fans are switched (or turned) on and off, not opened",
  "'Open' is used for doors, windows and boxes. A light is 'switched on': 'please switch on the light in the "
  "corridor.'",
  ["Object: a light", "Verb for lights: switch on / turn on", "'switch on the light'"],
  "'Open on the light' and 'start the light' are not used in English. 'Open the light' is a common error, so 'No "
  "improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "The other boys **were laughing on him** because he had fallen into the puddle.",
  ["were laughing at him", "were laughing to him", "were laughing over him", NI], 0,
  "Fixed preposition: laugh at (someone) = mock or find funny",
  "To make fun of someone is to 'laugh at' him: 'The other boys were laughing at him because he had fallen into the "
  "puddle.'",
  ["Verb: laugh", "Mocking someone → laugh at", "'were laughing at him'"],
  "'Laughing to him' and 'laughing over him' are not idiomatic for mocking someone. 'Laughing on him' is wrong, so "
  "'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "Because the chief guest was unwell, the annual function was **postponed for next week**.",
  ["postponed to next week", "postponed in next week", "postponed by next week", NI], 0,
  "Postpone something to (or until) a later time",
  "When an event is moved to a later date, it is 'postponed to' that date: 'the annual function was postponed to "
  "next week.'",
  ["Verb: postpone (move later)", "The new time is introduced by 'to' (or 'until')", "'postponed to next week'"],
  "'Postponed in next week' and 'postponed by next week' do not name the new date correctly ('by' would give the "
  "length of a delay, as in 'postponed by a week'). 'Postponed for next week' is not idiomatic, so 'No improvement "
  "required' is wrong.", 30, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "Nobody in the office knows **the reason of his sudden resignation**.",
  ["the reason for his sudden resignation", "the reason about his sudden resignation",
   "the reason to his sudden resignation", NI], 0,
  "Fixed preposition: reason for (something)",
  "The noun 'reason' takes 'for': 'Nobody in the office knows the reason for his sudden resignation.'",
  ["Noun: reason", "Fixed pairing: reason for", "'the reason for his sudden resignation'"],
  "'Reason about' and 'reason to' are not used with a noun in this sense. 'Reason of' is wrong, so 'No improvement "
  "required' is wrong.", 30, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "You **ought to inform** me yesterday that the branch would be closed today.",
  ["ought to have informed", "ought to be informing", "ought to informed", NI], 0,
  "'Ought to have + past participle' = a past duty that was not carried out",
  "The duty belonged to yesterday and was not done (the speaker was not told). A past unfulfilled duty is "
  "expressed by 'ought to have + past participle': 'You ought to have informed me yesterday ...'.",
  ["Time: yesterday (past)", "The duty was not carried out", "'ought to have informed'"],
  "'Ought to be informing' refers to the present or future and clashes with 'yesterday'. 'Ought to informed' "
  "puts a past form after 'to'. 'Ought to inform' cannot refer to yesterday, so 'No improvement required' is "
  "wrong.", 35, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "**What with the rain and the traffic**, we reached the station only a minute before the train left.",
  ["Because with the rain and the traffic", "What for the rain and the traffic", "Due with the rain and the traffic",
   NI], 3,
  "'What with A and B' = because of A and B (usually several troublesome causes)",
  "'What with the rain and the traffic' is a correct idiom giving two reasons for the late arrival. The sentence is "
  "correct as it stands.",
  ["Idiom: what with X and Y = because of X and Y", "Two causes: rain, traffic", "Correct as written"],
  "'Because with', 'What for' and 'Due with' are not English expressions. The bold part is a correct idiom, so no "
  "change is needed.", 35, order=LAST_FIXED)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", B,
  PR_STEM + "Please **fill on** this form in capital letters and sign it at the bottom.",
  ["fill in", "fill at", "fill by", NR], 0,
  "Phrasal verb: fill in (a form) = write the required details in it",
  "Writing details into a form is 'filling it in': 'Please fill in this form in capital letters ...'.",
  ["Object: a form", "Phrasal verb: fill in", "'fill in'"],
  "'Fill at' and 'fill by' are not phrasal verbs. 'Fill on' is wrong, so 'No replacement required' does not apply.",
  25, order=LAST_FIXED)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The unsafe old building was **pulled up** last year, and a park now stands in its place.",
  ["pulled down", "pulled over", "pulled through", NR], 0,
  "Phrasal verb: pull down (a building) = demolish it",
  "A building that is removed so that a park can take its place is demolished, i.e. 'pulled down'.",
  ["Meaning needed: demolished", "Phrasal verb: pull down", "'pulled down'"],
  "'Pull over' is what a vehicle does to stop at the side of a road. 'Pull through' means recover from an illness. "
  "'Pull up' means stop a vehicle or remove a plant; none means demolish, so 'No replacement required' does not "
  "apply.", 30, order=LAST_FIXED)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The thief **made off by** the cash box while the shopkeeper was busy with a customer.",
  ["made off with", "made up with", "made out of", NR], 0,
  "Phrasal verb: make off with (something) = steal it and run away",
  "A thief who runs away with stolen goods 'makes off with' them: 'The thief made off with the cash box ...'.",
  ["Meaning: escaped carrying the cash box", "Phrasal verb: make off with", "'made off with'"],
  "'Made up with' means became friends again after a quarrel. 'Made out of' describes material. 'Made off by' is "
  "not idiomatic, so 'No replacement required' does not apply.", 30, order=LAST_FIXED)

Q(PR, "Replace the phrase", A,
  PR_STEM + "Worried about panic, the minister tried to **play up** the crisis, calling it a minor issue that would "
  "soon pass.",
  ["play down", "play along", "play out", NR], 0,
  "Play down = make something seem less important; play up = make it seem more important",
  "Calling the crisis 'a minor issue' makes it seem smaller, which is 'playing it down'. 'Play up' would mean "
  "exaggerating it, the opposite of what the minister did.",
  ["Clue: 'calling it a minor issue'", "Making something seem smaller = play down", "'play down'"],
  "'Play along' means pretend to agree. 'Play out' means happen or unfold. 'Play up' gives the opposite meaning, so "
  "'No replacement required' does not apply.", 35, order=LAST_FIXED)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", B, SC_OK,
  ["Please wait me at the school gate.",
   "Please wait for me at the school gate.",
   "Please wait to me at the school gate.",
   "Please wait at me at the school gate."], 1,
  "Fixed preposition: wait for (someone or something)",
  "The verb 'wait' takes 'for' before the person or thing waited for: 'Please wait for me at the school gate.'",
  ["Verb: wait", "Person waited for → 'wait for'", "'wait for me': correct"],
  "The other sentences drop the preposition or use 'to' or 'at', none of which is used with 'wait' in this sense.",
  25)

Q(SC, "Grammatically incorrect sentence", I, SC_BAD,
  ["He did nothing but complained about the food all evening.",
   "She could do nothing but wait for the next bus.",
   "There was nothing to do but sit and wait.",
   "All he did was complain about the food."], 0,
  "'Do nothing but' is followed by the bare infinitive",
  "After 'did nothing but', the verb takes its base form: 'He did nothing but complain about the food all "
  "evening.' 'Complained' is wrong.",
  ["Pattern: do nothing but + base verb", "'complained' is past tense → error", "Correct: 'did nothing but "
   "complain'"],
  "The other three are correct: 'could do nothing but wait' and 'nothing to do but sit' use the base form, and 'All "
  "he did was complain' also takes the base form after 'did ... was'.", 35)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) On his last day, he found the whole village waiting for him outside the post office.\n"
  "(B) For thirty-two years, Hariram had delivered letters on foot to the scattered hamlets around Sonpur.\n"
  "(C) In all that time, he had not missed a single day, not even during the great flood.\n"
  "(D) Young men and women to whom he had once brought their exam results now handed him a garland and a new "
  "bicycle.\n"
  "(E) When the news came that he was to retire, people began to realise how much they would miss him.",
  ["BCEAD", "CBEAD", "BCADE", "BCEDA"], 0,
  "Para jumble: introduction → 'all that time' → news of retirement → last day → farewell gift",
  "B introduces Hariram and his thirty-two years. C ('In all that time') refers back to those years. E brings the "
  "news of his retirement. A describes his last day, and D the gift the villagers gave him that day.",
  ["Opener: B (who he is, how long he served)", "B → C: 'all that time' = the thirty-two years",
   "C → E: news of retirement", "E → A (last day) → D (the gift): BCEAD"],
  "CBEAD opens with 'In all that time', which has nothing to refer to. BCADE puts the news of his retirement after "
  "his last day. BCEDA has the gift handed over before the village gathers on his last day.", 40)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) When a highway bypass is built around a small town, the town's shopkeepers often protest.\n"
  "(P) Yet some towns find that, once the heavy lorries are gone, their markets become pleasanter places to shop, "
  "and local customers return.\n"
  "(Q) Once the bypass opens, these vehicles no longer pass through the town at all.\n"
  "(R) Their fear is easy to understand.\n"
  "(S) Many of their customers are travellers whose buses, cars and lorries stop on the main road for tea, food "
  "or fuel.",
  ["RSQP", "RQSP", "SRQP", "RSPQ"], 0,
  "Fixed opener; 'their fear' → reason → consequence → 'Yet' contrast",
  "R ('Their fear') refers to the protest in (1). S explains the fear: many customers are passing travellers. Q "
  "('these vehicles') shows they will stop coming. P ('Yet') gives the surprising other side.",
  ["(1) → R: 'Their fear' = the protest", "R → S: why they fear", "S → Q: 'these vehicles' stop coming",
   "Q → P: 'Yet' the unexpected benefit: RSQP"],
  "RQSP puts 'these vehicles' before any vehicles are mentioned. SRQP separates 'Their fear' from the protest it "
  "refers to. RSPQ gives the 'Yet' contrast before the loss of travellers it contrasts with.", 40)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) When an onion is cut, its damaged cells release substances that mix and form an irritating gas.\n"
  "(B) Anyone who has chopped onions knows that the job can bring tears to the eyes.\n"
  "(C) The eyes respond by producing tears to wash the irritant away.\n"
  "(D) This gas drifts upward and, on reaching the eyes, stings them.\n"
  "(E) Chilling an onion before cutting it slows this process, which is why some cooks keep onions in the "
  "refrigerator.",
  ["BADCE", "BDACE", "ABDCE", "BADEC"], 0,
  "Para jumble: common experience → cause → spread → body's response → practical tip",
  "B states the familiar experience. A explains what happens when the onion is cut. D ('This gas') follows the gas "
  "to the eyes. C gives the eyes' response. E offers a remedy based on the process.",
  ["Opener: B (the everyday experience)", "B → A: cutting releases a gas", "A → D: 'This gas' reaches the eyes",
   "D → C: tears → E: the remedy: BADCE"],
  "BDACE uses 'This gas' before any gas is mentioned. ABDCE puts the general experience in the middle of the "
  "explanation. BADEC gives the remedy before explaining that the eyes water.", 40)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) A fixed deposit can usually be closed before it matures.\n"
  "(P) A depositor who may need money at short notice can therefore split her savings into several smaller "
  "deposits.\n"
  "(Q) Doing so, however, comes at a price.\n"
  "(R) That way, she can break only one of them in an emergency and let the others earn their full interest.\n"
  "(S) The bank usually pays a lower rate on the money withdrawn early, and may also charge a small penalty.",
  ["QSPR", "QPSR", "SQPR", "QSRP"], 0,
  "Fixed opener; 'Doing so' → the cost → 'therefore' → 'That way'",
  "Q ('Doing so') refers to closing the deposit early. S describes the price: a lower rate and a penalty. P "
  "('therefore') gives the sensible response. R ('That way') explains how splitting helps.",
  ["(1) → Q: 'Doing so' = closing early", "Q → S: the price paid", "S → P: 'therefore' split the savings",
   "P → R: 'That way': QSPR"],
  "QPSR gives the advice before the cost that makes it necessary. SQPR describes the price before 'Doing so ... "
  "comes at a price' introduces it. QSRP uses 'That way' and 'them' before the smaller deposits are mentioned.", 40)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) To correct this, an extra day, 29 February, is added to the calendar every fourth year.\n"
  "(B) The Earth takes about 365 and a quarter days to go once round the Sun.\n"
  "(C) Without this adjustment, the seasons would slowly drift away from their usual months.\n"
  "(D) Over four years, this shortfall adds up to roughly one whole day.\n"
  "(E) A calendar of exactly 365 days therefore falls behind by about a quarter of a day each year.",
  ["BEDAC", "BDEAC", "EBDAC", "BEDCA"], 0,
  "Para jumble: fact → consequence → accumulation → correction → why it matters",
  "B gives the length of the Earth's year. E ('therefore') shows a 365-day calendar falls behind. D ('this "
  "shortfall') adds it up over four years. A ('To correct this') adds the leap day. C ('this adjustment') says what "
  "would happen without it.",
  ["Opener: B (the basic fact)", "B → E: 'therefore' the calendar falls behind", "E → D: 'this shortfall' adds up",
   "D → A: the correction → C: 'Without this adjustment': BEDAC"],
  "BDEAC uses 'this shortfall' before the shortfall is described. EBDAC opens with 'therefore', which needs a fact "
  "before it. BEDCA mentions 'this adjustment' before the adjustment is introduced.", 40)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) Mohan had saved for two years to buy a second-hand bicycle.\n"
  "(P) When he came out with a box of sweets for his mother, the bicycle was gone.\n"
  "(Q) Two days later, a constable knocked at his door with the bicycle, which had been found abandoned near the "
  "railway station.\n"
  "(R) On the very first day, he rode it to the market and parked it outside a sweet shop.\n"
  "(S) He searched the nearby lanes until dark and then reported the theft at the police station.",
  ["RPSQ", "RSPQ", "PRSQ", "RPQS"], 0,
  "Fixed opener; narrative order: ride → theft → search and report → recovery",
  "R: on the first day he parks the bicycle outside a sweet shop. P: he comes out to find it gone. S: he searches "
  "and reports the theft. Q: two days later the police return it.",
  ["(1) → R: the first ride", "R → P: the bicycle is gone", "P → S: search and report",
   "S → Q: 'Two days later' it is returned: RPSQ"],
  "RSPQ reports a theft before the bicycle is missing. PRSQ has him coming out of the shop before he has parked "
  "there. RPQS returns the bicycle before the theft has been reported.", 40)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) Critics reply that such a charge would fall hardest on poorer drivers, who may have no other way to "
  "reach work.\n"
  "(B) This is because a car entering a crowded road at rush hour slows every other vehicle on it, yet its driver "
  "pays nothing for that delay.\n"
  "(C) Economists have long argued that drivers should pay for the congestion they cause.\n"
  "(D) Supporters answer that the money raised could be spent on better buses, which poorer commuters use most.\n"
  "(E) A fee for entering the busiest areas at peak hours would make drivers weigh that cost, and some would "
  "travel earlier, later or by bus.",
  ["CBEAD", "CEBAD", "BCEAD", "CBEDA"], 0,
  "Argument structure: claim → reason → proposal → objection → reply",
  "C states the economists' claim. B ('This is because') gives the reason. E proposes a fee that makes drivers weigh "
  "'that cost'. A ('such a charge') is the critics' objection. D is the supporters' reply to it.",
  ["Opener: C (the claim)", "C → B: 'This is because' explains it", "B → E: the fee weighs 'that cost'",
   "E → A (objection) → D (reply): CBEAD"],
  "CEBAD proposes the fee before explaining the cost it is meant to price. BCEAD opens with 'This is because', "
  "which needs a claim before it. CBEDA has supporters answering an objection that has not yet been raised.", 50)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) Economists distinguish between a risk and an uncertainty.\n"
  "(P) Such cases are much harder to insure, and markets often deal with them by spreading bets or by avoiding them "
  "altogether.\n"
  "(Q) Insurers can price such situations, because past experience gives them a reliable guide to the future.\n"
  "(R) An uncertainty, by contrast, is one in which even the chances cannot be calculated, such as whether an "
  "untried technology will succeed.\n"
  "(S) A risk is a situation in which the possible outcomes and their chances are known, as when a fair die is "
  "rolled.",
  ["SQRP", "SRQP", "RSQP", "SQPR"], 0,
  "Fixed opener; define the first term → its consequence → contrast → its consequence",
  "S defines a risk. Q ('such situations') says insurers can price risks. R ('by contrast') defines an uncertainty. "
  "P ('Such cases') says uncertainties are hard to insure.",
  ["(1) → S: define risk", "S → Q: insurers can price risks", "Q → R: 'by contrast', uncertainty",
   "R → P: 'Such cases' = uncertainties: SQRP"],
  "SRQP makes Q's 'such situations' refer to uncertainties, which cannot be priced. RSQP gives 'by contrast' before "
  "the term it contrasts with. SQPR makes P's 'Such cases' refer to risks, which the passage says can be insured.",
  50)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) As the days shorten in autumn, however, the tree stops making chlorophyll, and what remains breaks "
  "down.\n"
  "(B) The reds, by contrast, are newly made in autumn, which is why their brightness varies from year to year with "
  "the weather.\n"
  "(C) Leaves are green because they contain chlorophyll, which plants use to make food from sunlight.\n"
  "(D) With the green gone, those hidden yellows and oranges show through.\n"
  "(E) The leaves also contain yellow and orange pigments, but all summer these are masked by the green.",
  ["CEADB", "CAEDB", "ECADB", "CEABD"], 0,
  "Para jumble: why green → hidden colours → loss of green → colours revealed → contrast with reds",
  "C explains the green colour. E ('also') adds the hidden yellows and oranges. A describes the loss of chlorophyll "
  "in autumn. D ('With the green gone') shows the hidden colours appearing. B ('by contrast') explains the reds, "
  "which were not hidden.",
  ["Opener: C (why leaves are green)", "C → E: 'also' other pigments, masked", "E → A: chlorophyll breaks down",
   "A → D: hidden colours show → B: reds by contrast: CEADB"],
  "CAEDB puts 'however' (autumn) straight after the plain fact about chlorophyll, with no summer state to "
  "contrast with, and removes the green before the hidden pigments are introduced. ECADB opens with 'also', which needs an "
  "earlier statement. CEABD puts the contrast with reds before the yellows and oranges have appeared.", 50)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", B,
  SR_STEM + "(P) who sells vegetables\n(Q) the woman\n(R) is my neighbour's mother\n(S) from a cart at the corner of our lane",
  ["QPSR", "QRPS", "PQSR", "QSPR"], 0,
  "Subject + relative clause (with its place phrase) + main verb",
  "'The woman who sells vegetables from a cart at the corner of our lane is my neighbour's mother.' Subject (Q), relative clause "
  "(P) with its place phrase (S), then the main verb and complement (R).",
  ["Subject: Q", "Relative clause: P + S", "Main verb: R → QPSR"],
  "QRPS separates 'who sells vegetables' from 'the woman' and leaves the place phrase dangling at the end. PQSR "
  "opens with a relative clause that has no noun before it. QSPR gives 'the woman from a cart at the corner of our "
  "lane', cutting the place phrase off from 'sells vegetables'.", 30)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) the more\n(Q) you practise\n(R) you will become\n(S) the more confident",
  ["PQSR", "PSQR", "SRPQ", "PRSQ"], 0,
  "Double comparative: The more + clause, the more + adjective + clause",
  "'The more you practise, the more confident you will become.' The first half is 'the more' (P) + 'you practise' "
  "(Q); the second is 'the more confident' (S) + 'you will become' (R).",
  ["Frame: The more ..., the more ...", "First half: P + Q", "Second half: S + R → PQSR"],
  "PSQR gives 'The more the more confident', which breaks the frame. SRPQ makes no sense as a statement. PRSQ "
  "gives 'The more you will become the more confident you practise', which reverses cause and result.", 35)

Q(SR, "Word/phrase rearrangement within a sentence", A,
  SR_STEM + "(P) can the city\n(Q) only by\n(R) hope to reduce its traffic jams\n(S) improving its bus service",
  ["QSPR", "PRQS", "QPSR", "SQPR"], 0,
  "Inversion after a fronted 'only by + -ing' phrase: Only by ... can + subject + verb",
  "'Only by improving its bus service can the city hope to reduce its traffic jams.' The fronted phrase (Q + S) is "
  "followed by the inverted 'can the city' (P) and the rest of the verb (R).",
  ["Fronted phrase: 'Only by' (Q) + 'improving its bus service' (S)", "Inversion: 'can the city' (P)",
   "Rest of the verb: R → QSPR"],
  "PRQS opens with an inverted question form and leaves 'only by improving' hanging at the end. QPSR splits 'only "
  "by' from 'improving'. SQPR puts 'improving its bus service' before 'only by'.", 40)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The baby was so ______ after the long bus journey that she fell asleep in her mother's arms.",
  ["drowsy", "cheerful", "curious", "restless"], 0,
  "Single blank: the result clause ('so ... that she fell asleep') decides the word",
  "Falling asleep follows feeling sleepy. 'Drowsy' means sleepy.",
  ["Result: she fell asleep", "Cause: she was sleepy", "'drowsy'"],
  "Being 'cheerful' or 'curious' does not lead to falling asleep, and 'restless' suggests the opposite.", 20)

Q(FB, "Single blank", B,
  FB1 + "Please ______ your seat belt; the plane is about to land.",
  ["fasten", "loosen", "lift", "fold"], 0,
  "Single blank: the fixed collocation 'fasten a seat belt'",
  "Before landing, passengers are asked to buckle their seat belts: 'fasten your seat belt'.",
  ["Context: the plane is about to land", "Safety step: buckle the belt", "'fasten'"],
  "'Loosen' is the opposite of what is needed for landing. Seat belts are not 'lifted' or 'folded'.", 20)

Q(FB, "Single blank", B,
  FB1 + "The village well had ______ up during the long, hot summer, so the women had to fetch water from the river.",
  ["dried", "filled", "opened", "cooled"], 0,
  "Single blank: the phrasal verb 'dry up' and the result clause",
  "Water had to be fetched from the river because the well had no water left: it had 'dried up' in the heat.",
  ["Result: water fetched from the river", "Cause: no water in the well", "'dried up'"],
  "A well that had 'filled up' would remove the need to go to the river. 'Opened up' and 'cooled up' do not "
  "explain the lack of water.", 20)

Q(FB, "Double blank", B,
  FB2 + "The tailor ______ the trousers by two inches because they were too ______ for the boy.",
  ["shortened, long", "lengthened, long", "shortened, short", "stitched, expensive"], 0,
  "Double blank: both words must agree with each other",
  "Trousers that are too long for the boy are made shorter: the tailor 'shortened' them because they were too "
  "'long'.",
  ["Problem: too long", "Fix: make them shorter", "'shortened, long'"],
  "Lengthening long trousers or shortening short ones makes the problem worse. Stitching cannot fix a price.", 25)

Q(FB, "Phrase fillers", B,
  FBP + "The teacher asked the students to ______ the new words in their notebooks.",
  ["write down", "give up", "call off", "run over"], 0,
  "Phrase fillers: write down = record in writing",
  "Students record new words in notebooks: they 'write them down'.",
  ["Place: in their notebooks", "Action: record in writing", "'write down'"],
  "'Give up' (stop), 'call off' (cancel) and 'run over' (knock down with a vehicle) make no sense with notebooks.",
  20)

Q(FB, "Phrase fillers", B,
  FBP + "The fire alarm ______ suddenly in the middle of the night, and everyone rushed out of the building.",
  ["went off", "went over", "went by", "went down"], 0,
  "Phrase fillers: go off (of an alarm) = start ringing",
  "An alarm that starts ringing 'goes off', which is why everyone rushed out.",
  ["Subject: a fire alarm", "Result: everyone rushed out", "Alarm starts ringing → 'went off'"],
  "'Went over' (examined), 'went by' (passed) and 'went down' (fell or sank) do not describe an alarm ringing.", 20)

Q(FB, "Single blank", I,
  FB1 + "The rumours about the minister's health proved ______; he was back at work the very next day.",
  ["unfounded", "accurate", "contagious", "permanent"], 0,
  "Single blank: the clause after the semicolon gives the evidence",
  "If he was back at work the next day, the rumours that he was ill had no basis: they proved 'unfounded'.",
  ["Evidence: back at work next day", "So the rumours were false", "'unfounded'"],
  "If the rumours were 'accurate', he would not be back at work. Rumours are not 'contagious' or 'permanent' in "
  "any sense that fits the evidence.", 25)

Q(FB, "Double blank", I,
  FB2 + "The two neighbours have not been on ______ terms since their quarrel over the boundary wall, and they now "
  "______ each other in the street.",
  ["speaking, ignore", "talking, greet", "equal, help", "easy, follow"], 0,
  "Double blank: the idiom 'on speaking terms' and a consistent second word",
  "'Not on speaking terms' means not talking to each other after a quarrel; such neighbours 'ignore' each other.",
  ["Idiom: on speaking terms", "After a quarrel: not speaking", "So they 'ignore' each other"],
  "'Talking terms' is not idiomatic, and greeting each other contradicts the quarrel. 'Help' and 'follow' do not "
  "fit people who have fallen out.", 30)

Q(FB, "Phrase fillers", I,
  FBP + "Having been cheated once, the old man now tries to ______ anyone who promises to double his money.",
  ["steer clear of", "look up to", "catch up with", "run short of"], 0,
  "Phrase fillers: steer clear of = deliberately avoid",
  "A man cheated before would avoid anyone making the same kind of promise: he 'steers clear of' them.",
  ["Past: cheated once", "Now: avoids such people", "'steer clear of'"],
  "'Look up to' (admire) and 'catch up with' (reach) contradict his caution. 'Run short of' is used for supplies, "
  "not people.", 30)

Q(FB, "Single blank", A,
  FB1 + "Her ______ remarks, always delivered with a perfectly straight face, left the audience unsure whether she "
  "was joking.",
  ["deadpan", "effusive", "rambling", "tearful"], 0,
  "Single blank: the description 'with a perfectly straight face' defines the word",
  "Humour delivered without any expression, so that listeners cannot tell whether it is a joke, is 'deadpan'.",
  ["Clue: straight face, unsure if joking", "Expressionless humour", "'deadpan'"],
  "'Effusive' remarks are full of open feeling, the opposite of a straight face. 'Rambling' describes length, not "
  "expression. 'Tearful' does not fit joking.", 30)

Q(FB, "Single blank", A,
  FB1 + "The minister's ______ promise to build a bridge, repeated at every election for twenty years, has become "
  "a local joke.",
  ["perennial", "solitary", "sudden", "sincere"], 0,
  "Single blank: 'repeated at every election for twenty years' points to something constantly recurring",
  "A promise that keeps coming back year after year is 'perennial' (lasting or recurring for a very long time).",
  ["Clue: repeated for twenty years", "Constantly recurring", "'perennial'"],
  "A promise repeated for twenty years is neither 'solitary' (single) nor 'sudden'. A 'sincere' promise kept "
  "unfulfilled for twenty years would hardly become a joke.", 30)

Q(FB, "Double blank", A,
  FB2 + "The film's ______ plot, full of improbable twists and half-explained flashbacks, ______ even its most "
  "loyal fans.",
  ["convoluted, bewildered", "lucid, bored", "predictable, surprised", "gripping, disappointed"], 0,
  "Double blank: the description in the middle decides both words",
  "A plot full of twists and half-explained flashbacks is 'convoluted' (complicated and hard to follow), and it "
  "would 'bewilder' (confuse) even loyal fans.",
  ["Clue: improbable twists, half-explained flashbacks", "Plot: convoluted", "Effect: bewildered"],
  "A plot full of twists is neither 'lucid' (clear) nor 'predictable'. A 'gripping' plot would not disappoint its "
  "most loyal fans in this context.", 40)

Q(FB, "Phrase fillers", A,
  FBP + "After five years of losses, the founder finally decided to ______ and sell the company to a larger rival.",
  ["cut his losses", "turn the tables", "hold his horses", "steal the show"], 0,
  "Phrase fillers: cut one's losses = abandon a failing venture before losing more",
  "After five years of losses, selling the business stops the losses from growing: he 'cut his losses'.",
  ["Context: five years of losses", "Action: sell to stop further loss", "'cut his losses'"],
  "'Turn the tables' means reverse a situation in one's favour, which selling up is not. 'Hold his horses' means "
  "wait, and 'steal the show' means attract the most attention.", 35)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'breathe' used correctly?",
  ["Take a deep breathe before you dive into the water.",
   "The doctor asked the old man to breathe slowly and deeply.",
   "She was out of breathe after climbing the stairs.",
   "He held his breathe for a full minute under water."], 1,
  "Breathe (verb, to take air in and out) vs breath (noun, the air taken in)",
  "'Breathe' is a verb. 'To breathe slowly' uses it correctly as a verb after 'to'.",
  ["'a deep ___' needs a noun → breath", "'to breathe slowly' → verb: correct", "'out of ___' needs a noun → "
   "breath", "'held his ___' needs a noun → breath"],
  "The other three need the noun 'breath': a deep breath, out of breath, held his breath.", 25)

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'personnel' used correctly?",
  ["This is only my personnel opinion, not the company's.",
   "All personnel must wear identity badges inside the factory.",
   "She keeps her personnel diary locked in a drawer.",
   "He took a personnel interest in the new trainee's progress."], 1,
  "Personnel (noun, the people employed in an organisation) vs personal (adjective, one's own, private)",
  "'Personnel' means the staff of an organisation. 'All personnel must wear identity badges' uses it correctly.",
  ["'my ___ opinion' → personal", "'All ___ must wear badges' = all staff → personnel: correct",
   "'her ___ diary' → personal", "'a ___ interest' → personal"],
  "The other three need the adjective 'personal' (one's own): personal opinion, personal diary, personal interest.",
  25)

Q(WU, "Word swap", B,
  WS_STEM + "The hungry **(A) bone** chewed the **(B) dog** that the **(C) butcher** had thrown into the "
  "**(D) street**.",
  ["C-D", "A-B", "B-C", "No swap required"], 1,
  "Word swap: check who can perform each action",
  "A bone cannot chew anything. Swapping A and B gives: 'The hungry dog chewed the bone that the butcher had thrown "
  "into the street.'",
  ["'The hungry bone chewed' is impossible", "The dog is the one that chews", "Swap A and B"],
  "C-D gives 'the street had thrown into the butcher', which is absurd. B-C gives 'chewed the butcher', which leaves "
  "the bone as the one chewing. The sentence clearly needs a swap.", 25, order=FIXED)

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'dessert' used correctly?",
  ["The camel caravan crossed the dessert in three days.",
   "We had mango ice cream for dessert after dinner.",
   "The soldier was punished for trying to dessert his post.",
   "After the floods, the village looked dessert and empty."], 1,
  "Dessert (sweet dish after a meal) vs desert (dry land; or, as a verb, to abandon)",
  "'Dessert' is the sweet course at the end of a meal. 'Mango ice cream for dessert after dinner' uses it "
  "correctly.",
  ["Dry land crossed by camels → desert", "Sweet course after dinner → dessert: correct",
   "Abandon one's post → desert (verb)", "Empty, abandoned-looking → deserted"],
  "The camel sentence needs 'desert' (dry land), the soldier sentence the verb 'desert' (abandon), and the village "
  "sentence 'deserted'.", 25)

Q(WU, "Correct usage of a word", I,
  "In which of the following sentences is the word 'morale' used correctly?",
  ["The story has a clear morale: honesty is always rewarded.",
   "The surprise bonus lifted the morale of the tired staff.",
   "He is a man of high morale principles.",
   "It is our morale duty to help the flood victims."], 1,
  "Morale (spirit and confidence of a group) vs moral (a lesson; or, as an adjective, concerning right and wrong)",
  "'Morale' means the confidence and spirit of a group. A bonus that cheers tired staff 'lifts their morale'.",
  ["Lesson of a story → moral", "Spirit of the staff → morale: correct", "Principles of right and wrong → moral",
   "Duty of conscience → moral"],
  "The other three need 'moral': the moral of a story, moral principles, a moral duty.", 30)

Q(WU, "Correct usage of a word", I,
  "In which of the following sentences is the word 'allusion' used correctly?",
  ["The magician created the allusion of a table floating in the air.",
   "Her speech contained an allusion to the Salt March of 1930.",
   "He was under the allusion that the loan would be forgiven.",
   "In the desert heat, the travellers saw an allusion of water."], 1,
  "Allusion (an indirect reference to something) vs illusion (a false idea or a deceptive appearance)",
  "An 'allusion' is a passing or indirect reference. A speech that refers to the Salt March contains an "
  "allusion to it.",
  ["Magic trick that deceives the eye → illusion", "Indirect reference in a speech → allusion: correct",
   "A false belief → under the illusion", "Water that is not really there → illusion"],
  "The magic trick, the false belief and the imagined water are all deceptions, which need 'illusion'.", 30)

Q(WU, "Word swap", I,
  WS_STEM + "The **(A) heavy** rain **(B) flooded** the low-lying **(C) fields** and **(D) washed** away the young "
  "crops.",
  ["A-C", "B-D", "A-B", "No swap required"], 3,
  "Word swap: test each pair, and choose 'No swap' when the sentence already makes sense",
  "Heavy rain flooding low-lying fields and washing away young crops is perfectly sensible. No words need to be "
  "interchanged.",
  ["'heavy rain': sensible", "'flooded the low-lying fields': sensible", "'washed away the young crops': sensible"],
  "A-C gives 'the fields rain ... heavy', B-D gives 'washed the fields and flooded away the crops', and A-B gives "
  "'the flooded rain heavy'; each makes the sentence worse.", 30, order=FIXED)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'reimburse' as used in the sentence:\n"
  "'The company will reimburse the travel expenses of all candidates called for the interview.'",
  ["pay back", "reduce", "check", "refuse"], 0,
  "Reimburse = repay money that someone has spent",
  "Candidates pay their own fares to attend, and the company later returns that money to them: it reimburses "
  "them.",
  ["Candidates spend on travel", "The company returns the money", "'pay back'"],
  "'Reduce' and 'check' do not mean returning money. 'Refuse' is the opposite of the company's promise.", 20)

Q(VO, "Word pairs", I, "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Tenacious – Persistent", "Placid – Agitated", "Sparse – Dense", "Feasible – Impracticable"], 0,
  "Word pairs: identify synonyms and antonyms",
  "'Tenacious' and 'persistent' both mean holding on firmly and not giving up. The other pairs are opposites.",
  ["Tenacious = persistent", "Placid (calm) ≠ agitated", "Sparse (thinly spread) ≠ dense",
   "Feasible (possible) ≠ impracticable"],
  "The other three pairs are opposites, not synonyms.", 25)

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'unprecedented' as used in the sentence:\n"
  "'The cyclone caused unprecedented damage; nothing like it had been seen on this coast for a hundred years.'",
  ["never known or done before", "expected and planned for", "small and easily repaired", "caused deliberately"], 0,
  "Unprecedented = without any earlier example",
  "The clause after the semicolon explains it: nothing like it had been seen in a hundred years. Damage with no "
  "earlier parallel is 'unprecedented'.",
  ["Clue: nothing like it in a hundred years", "No earlier example", "'never known or done before'"],
  "'Expected and planned for' and 'small and easily repaired' contradict the clue. Nothing suggests the cyclone's "
  "damage was 'caused deliberately'.", 25)

Q(VO, "Word pairs", I, "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Ponder – Contemplate", "Zenith – Nadir", "Lament – Mourn", "Abate – Subside"], 1,
  "Word pairs: identify synonyms and antonyms",
  "'Zenith' is the highest point and 'nadir' the lowest point. They are opposites. The other pairs are synonyms.",
  ["Ponder = contemplate (think deeply)", "Zenith (highest point) ≠ nadir (lowest point)",
   "Lament = mourn (grieve)", "Abate = subside (become less)"],
  "The other three pairs are synonyms, not opposites.", 25)

Q(VO, "Contextual meaning", A,
  "Choose the meaning of the word 'insouciant' as used in the sentence:\n"
  "'As the losses mounted month after month, the owner's insouciant attitude astonished his accountants.'",
  ["carelessly unconcerned", "deeply anxious", "angrily defensive", "quietly ashamed"], 0,
  "Insouciant = showing a casual lack of concern",
  "The accountants are astonished because the owner does not seem worried at all while losses mount. His attitude "
  "is 'insouciant': casually unconcerned.",
  ["Situation: mounting losses", "Accountants astonished → owner not worried", "'carelessly unconcerned'"],
  "If he were 'deeply anxious' or 'quietly ashamed', his reaction would be normal and would not astonish anyone. "
  "Nothing suggests he was 'angrily defensive'.", 30)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", I,
  SY_STEM + "Landslides and heavy rain **impeded** the rescue work in the hills for two days.",
  ["hindered", "assisted", "announced", "inspected"], 0,
  "Impede = obstruct or slow down",
  "Landslides and heavy rain make rescue work harder and slower: they 'impede' or 'hinder' it.",
  ["Context: landslides and rain vs rescue work", "Effect: slowed and obstructed", "Closest: 'hindered'"],
  "'Assisted' is the opposite. Landslides do not 'announce' or 'inspect' work.", 25)

Q(SY, "Contextual synonym", I,
  SY_STEM + "She sat on the steps for an hour, **pensive**, wondering whether to accept the transfer.",
  ["thoughtful", "cheerful", "careless", "sleepy"], 0,
  "Pensive = deep in serious thought",
  "Someone sitting for an hour wondering about a decision is lost in thought: 'pensive' or 'thoughtful'.",
  ["Context: wondering whether to accept", "Deep in thought", "Closest: 'thoughtful'"],
  "'Cheerful', 'careless' and 'sleepy' do not describe someone weighing a decision.", 25)

Q(SY, "Contextual synonym", A,
  SY_STEM + "The critic's **trenchant** review exposed every weakness in the play's script and acting.",
  ["cutting", "flattering", "lengthy", "confused"], 0,
  "Trenchant = vigorous and sharply incisive",
  "A review that exposes every weakness is sharp and forceful: 'trenchant', or 'cutting'.",
  ["Context: exposes every weakness", "Sharp, forceful criticism", "Closest: 'cutting'"],
  "A 'flattering' review would hide weaknesses. 'Lengthy' refers to length, not sharpness. A 'confused' review "
  "could not expose every weakness clearly.", 30)

Q(SY, "Contextual synonym", A,
  SY_STEM + "The company's **profligate** spending on parties and foreign trips soon emptied its reserves.",
  ["extravagant", "careful", "secret", "modest"], 0,
  "Profligate = recklessly wasteful",
  "Spending on parties and trips that empties a company's reserves is recklessly wasteful: 'profligate', or "
  "'extravagant'.",
  ["Context: parties, trips, empty reserves", "Wasteful spending", "Closest: 'extravagant'"],
  "'Careful' and 'modest' spending would not empty the reserves. 'Secret' says nothing about how much was spent.",
  30)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The new bridge is **sturdy** enough to carry heavily loaded lorries.",
  ["flimsy", "strong", "long", "costly"], 0,
  "Sturdy = strong and solidly built; opposite: flimsy",
  "A bridge that can carry loaded lorries is strong. The opposite of 'sturdy' is 'flimsy' (weak, easily broken).",
  ["'sturdy' = strong, solid", "Opposite: weak, easily broken", "'flimsy'"],
  "'Strong' is a synonym, not an opposite. 'Long' and 'costly' describe size and price, not strength.", 20)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The **vigilant** guard noticed the stranger loitering near the gate long before he tried to climb it.",
  ["inattentive", "watchful", "armed", "elderly"], 0,
  "Vigilant = keeping careful watch; opposite: inattentive",
  "The guard noticed the stranger early because he was watching carefully. The opposite of 'vigilant' is "
  "'inattentive' (not paying attention).",
  ["'vigilant' = alert, watchful", "Opposite: not paying attention", "'inattentive'"],
  "'Watchful' is a synonym. 'Armed' and 'elderly' describe the guard in other ways, not his attention.", 25)

Q(AN, "Contextual antonym", A,
  AN_STEM + "The young founder's **audacious** plan to take on the market leader in its home city surprised "
  "investors.",
  ["timorous", "daring", "costly", "secret"], 0,
  "Audacious = boldly daring; opposite: timorous",
  "Taking on the market leader in its home city is a bold, risky move. The opposite of 'audacious' is 'timorous' "
  "(timid, lacking courage).",
  ["'audacious' = bold, daring", "Opposite: fearful, timid", "'timorous'"],
  "'Daring' is a synonym. 'Costly' and 'secret' describe other features of a plan, not its boldness.", 30)

Q(AN, "Contextual antonym", A,
  AN_STEM + "Known for his **pugnacious** manner, the union leader picked a fight with almost everyone at the "
  "meeting.",
  ["peaceable", "aggressive", "talkative", "wealthy"], 0,
  "Pugnacious = eager to quarrel or fight; opposite: peaceable",
  "A man who picks a fight with almost everyone is quarrelsome: 'pugnacious'. The opposite is 'peaceable' (inclined "
  "to avoid conflict).",
  ["'pugnacious' = quarrelsome", "Opposite: avoiding conflict", "'peaceable'"],
  "'Aggressive' is a synonym. 'Talkative' and 'wealthy' have nothing to do with quarrelling.", 30)

Q(AN, "Contextual antonym", A,
  AN_STEM + "The **abstemious** old monk ate a single plain meal a day and never touched sweets.",
  ["gluttonous", "frugal", "devout", "silent"], 0,
  "Abstemious = sparing in eating and drinking; opposite: gluttonous",
  "Eating one plain meal a day and avoiding sweets is self-denying: 'abstemious'. The opposite is 'gluttonous' "
  "(eating far too much).",
  ["'abstemious' = sparing with food", "Opposite: eating greedily", "'gluttonous'"],
  "'Frugal' is close in meaning, not opposite. 'Devout' and 'silent' describe religion and speech, not eating.", 30)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"
ID_STEM = "Choose the option that best expresses the meaning of the idiom in bold.\n"

Q(ID, "Meaning of idiom", B, "Choose the meaning of the idiom 'to pull someone's leg'.",
  ["to tease someone playfully", "to hurt someone deliberately", "to help someone walk",
   "to stop someone from leaving"], 0,
  "Idiom: pull someone's leg = joke with someone by telling them something untrue",
  "To 'pull someone's leg' is to tease them in fun, for example by pretending something false is true.",
  ["Not literal", "Meaning: tease in fun", "'to tease someone playfully'"],
  "The idiom has nothing to do with hurting, helping someone walk or stopping them leaving; these read it "
  "literally.", 20)

Q(ID, "Idiom in context", B,
  ID_STEM + "After walking home in the rain, Grandfather felt **under the weather** for a few days.",
  ["slightly unwell", "very cheerful", "extremely busy", "short of money"], 0,
  "Idiom: under the weather = slightly ill",
  "After getting wet in the rain, Grandfather was a little ill for a few days: he felt 'under the weather'.",
  ["Context: walked home in the rain", "Result: a few days of feeling poorly", "'slightly unwell'"],
  "Getting wet does not make one 'very cheerful', 'extremely busy' or 'short of money'; the idiom refers to "
  "health.", 20)

Q(ID, "Meaning of idiom", I, "Choose the meaning of the idiom 'a storm in a teacup'.",
  ["great anger or worry about a very small matter", "a sudden change in the weather",
   "a serious problem that is hidden from view", "a quarrel that lasts for many years"], 0,
  "Idiom: a storm in a teacup = a big fuss over something trivial",
  "A storm inside a teacup is tiny; the idiom describes a lot of excitement or anger about something unimportant.",
  ["Storm = fuss", "Teacup = tiny matter", "'great anger or worry about a very small matter'"],
  "The idiom is not about weather. A hidden serious problem is the opposite of a trivial one, and the idiom says "
  "nothing about a long-lasting quarrel.", 25)

Q(ID, "Idiom in context", A,
  ID_STEM + "Having resigned publicly and sold his house in the city, he had **burnt his boats**; there was no way "
  "back to his old job.",
  ["made it impossible to return to his former position", "lost all his savings in a bad deal",
   "worked very hard to finish a task", "travelled abroad in search of work"], 0,
  "Idiom: burn one's boats = take an action that makes retreat impossible",
  "The clause after the semicolon explains it: 'there was no way back'. By resigning publicly and selling his house, "
  "he had cut off any return.",
  ["Actions: public resignation, house sold", "Result: no way back", "'made it impossible to return ...'"],
  "Losing savings, working hard and travelling abroad are not suggested; the context stresses only that he could "
  "not go back.", 30)

Q(ID, "Meaning of idiom", A, "Choose the meaning of the idiom 'Achilles' heel'.",
  ["a small but serious weakness in someone otherwise strong", "an injury that heals very slowly",
   "a habit of running away from danger", "a reward given for great courage"], 0,
  "Idiom: Achilles' heel = a weak point that can lead to downfall",
  "In Greek legend, Achilles could be wounded only in his heel. The idiom means a single vulnerable point in a "
  "person or thing that is otherwise strong.",
  ["Origin: Achilles, vulnerable only at the heel", "Meaning: one fatal weakness",
   "'a small but serious weakness ...'"],
  "The idiom is not about slow healing, running away or a reward; those read the words literally or invent a "
  "meaning.", 30)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", B, OW_STEM + "Able to speak two languages fluently",
  ["bilingual", "eloquent", "articulate", "literate"], 0,
  "One-word substitution: bi- (two) + lingual (of language)",
  "'Bilingual' means able to speak two languages fluently.",
  ["'bi-' = two", "'lingual' = of language", "'bilingual'"],
  "'Eloquent' and 'articulate' mean able to express oneself well, in any number of languages. 'Literate' "
  "means able to read and write.", 20)

Q(OW, "Single word for a phrase", I, OW_STEM + "An abnormal and extreme fear of heights",
  ["acrophobia", "claustrophobia", "hydrophobia", "xenophobia"], 0,
  "One-word substitution: acro- (height) + phobia (fear)",
  "'Acrophobia' is an extreme fear of heights.",
  ["'acro-' = height, top", "'phobia' = fear", "'acrophobia'"],
  "'Claustrophobia' is fear of closed spaces, 'hydrophobia' fear of water, and 'xenophobia' fear or dislike of "
  "foreigners.", 20)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", I, AP_STEM + "The members elected him secretary of the club.",
  ["He was elected secretary of the club by the members.",
   "Secretary of the club was elected him by the members.",
   "He has been elected secretary of the club by the members.",
   "He was elected by secretary of the club the members."], 0,
  "Passive of a verb with an object and an object complement (elect, make, appoint + object + title)",
  "The object 'him' becomes the subject 'He'. The complement 'secretary of the club' stays after the verb. The tense "
  "is past simple: 'He was elected secretary of the club by the members.'",
  ["Object 'him' → subject 'He'", "Past simple → was + elected", "Complement stays after the verb"],
  "Making 'Secretary' the subject turns the complement into the subject wrongly. 'Has been elected' changes the "
  "tense. 'He was elected by secretary of the club the members' scrambles the agent and the complement.", 30)

Q(AP, "Voice conversion", A, AP_STEM + "One should keep one's promises.",
  ["Promises should be kept.", "Promises should have been kept.", "One's promises should keep.",
   "Promises are being kept by one."], 0,
  "Passive with a modal (should + be + past participle); a general 'one' as subject is dropped",
  "The object 'promises' becomes the subject. 'Should keep' becomes 'should be kept'. The general agent 'one' is "
  "left out: 'Promises should be kept.'",
  ["Object → subject: promises", "should + be + kept", "Drop the general agent 'by one'"],
  "'Should have been kept' changes the time to the past. 'One's promises should keep' is active and changes the "
  "meaning. 'Are being kept by one' loses 'should' and keeps an awkward general agent.", 30)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", B, DS_STEM + 'She said, "I bought this saree yesterday."',
  ["She said that she had bought that saree the previous day.",
   "She said that she bought this saree yesterday.",
   "She said that I had bought that saree the previous day.",
   "She said that she has bought that saree the day before."], 0,
  "Reported statement: past simple → past perfect; this → that; yesterday → the previous day",
  "With a past reporting verb, 'bought' moves back to 'had bought', 'I' becomes 'she', 'this' becomes 'that' and "
  "'yesterday' becomes 'the previous day'.",
  ["Pronoun: I → she", "Tense: bought → had bought", "this → that; yesterday → the previous day"],
  "Keeping 'this' and 'yesterday' ignores the change of time and place. 'I had bought' keeps the wrong pronoun. "
  "'Has bought' is present perfect, which does not follow 'said'.", 30)

Q(DS, "Narration change", I, DS_STEM + 'He said to me, "Will you lend me your bicycle for an hour?"',
  ["He asked me if I would lend him my bicycle for an hour.",
   "He asked me will I lend him my bicycle for an hour.",
   "He told me that I will lend him my bicycle for an hour.",
   "He asked me if I would lend me his bicycle for an hour."], 0,
  "Reported yes/no question (a request): asked + if/whether + statement order; will → would",
  "A yes/no question is reported with 'asked' and 'if' (or 'whether') in statement order. 'Will' becomes 'would'; "
  "'you' → 'I', 'me' → 'him', 'your' → 'my'.",
  ["'said to' + question → asked", "if + statement order: if I would lend", "Pronouns: me → him, your → my"],
  "'Will I lend' keeps question order and the present 'will'. 'Told me that I will lend' turns the request into a "
  "statement. 'Lend me his bicycle' gets both pronouns wrong.", 30)

Q(DS, "Narration change", A, DS_STEM + 'She said, "Alas! I have lost my purse."',
  ["She exclaimed sorrowfully that she had lost her purse.",
   "She said alas that she had lost her purse.",
   "She exclaimed sorrowfully that she has lost my purse.",
   "She exclaimed with joy that she had lost her purse."], 0,
  "Reported exclamation: the interjection becomes a reporting verb + adverb ('exclaimed sorrowfully'); present "
  "perfect → past perfect",
  "'Alas' expresses sorrow, so the reporting verb becomes 'exclaimed sorrowfully' (or 'exclaimed with sorrow'). "
  "'Have lost' → 'had lost', 'I' → 'she', 'my' → 'her'.",
  ["'Alas!' → exclaimed sorrowfully", "have lost → had lost", "I → she; my → her"],
  "Keeping 'alas' inside the reported clause is wrong. 'Has lost my purse' keeps the wrong tense and pronoun. "
  "'With joy' gets the feeling wrong: 'alas' expresses sorrow.", 35)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", B, SV_STEM + "Ravi and his sister ______ to school by bus every day.",
  ["go", "goes", "is going", "has gone"], 0,
  "Two subjects joined by 'and' take a plural verb",
  "'Ravi and his sister' are two people, so the verb is plural. 'Every day' calls for the simple present: 'go'.",
  ["Subject: Ravi + his sister (plural)", "Habit ('every day') → simple present", "Plural simple present: 'go'"],
  "'Goes', 'is going' and 'has gone' are singular forms, and the last two also do not express a daily habit.", 20)

Q(SV, "Agreement rules", I, SV_STEM + "Measles ______ a contagious disease that spreads quickly among children.",
  ["is", "are", "were", "have been"], 0,
  "Names of diseases ending in -s (measles, mumps, rabies) are singular",
  "'Measles' is the name of one disease and takes a singular verb: 'Measles is a contagious disease ...'.",
  ["Subject: measles (one disease)", "Singular despite the -s", "Present fact → 'is'"],
  "'Are', 'were' and 'have been' are plural forms, and 'were' also puts a general fact in the past.", 25)

Q(SV, "Agreement rules", A, SV_STEM + "The rest of the mangoes ______ rotten, so the shopkeeper threw them away.",
  ["were", "was", "has been", "is"], 0,
  "'The rest of', like 'half of' and 'most of', agrees with the noun after 'of'",
  "'The rest of the mangoes' refers to many mangoes, so the verb is plural. The story is in the past ('threw'), so "
  "it is 'were'.",
  ["Noun after 'of': mangoes (plural)", "Plural verb needed", "Past, to match 'threw' → 'were'"],
  "'Was', 'has been' and 'is' are singular; 'the rest of' + a singular noun ('the rest of the cake') would take "
  "them, but mangoes are plural.", 30)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Perfect tenses", B, TE_STEM + "I ______ never ______ a tiger in the wild, though I have visited many forests.",
  ["have, seen", "had, saw", "have, saw", "did, seen"], 0,
  "Present perfect (have + past participle) for life experience up to now, often with 'never' or 'ever'",
  "The speaker is describing experience up to the present ('though I have visited many forests'), so the present "
  "perfect is used: 'I have never seen a tiger in the wild.'",
  ["Time: whole life up to now", "Present perfect: have + past participle", "'have, seen'"],
  "'Had' moves the time to before some past moment. 'Have saw' uses the past tense instead of the participle. 'Did "
  "seen' mixes the auxiliary 'did' with a participle.", 20)

Q(TE, "Perfect tenses", I, TE_STEM + "Her eyes were red and she looked exhausted because she ______ all night.",
  ["had been studying", "has been studying", "is studying", "was studied"], 0,
  "Past perfect continuous: an activity that continued up to a past moment and explains a past result",
  "The red eyes and tiredness are a past result ('looked'). The activity that went on before it and caused it is in "
  "the past perfect continuous: 'because she had been studying all night.'",
  ["Past result: she looked exhausted", "Earlier, continuing activity: studying all night",
   "Past perfect continuous: 'had been studying'"],
  "'Has been studying' is tied to the present and clashes with 'looked'. 'Is studying' is present. 'Was studied' is "
  "passive and makes no sense.", 30)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", I, AR_STEM + "______ Indian Ocean lies to the south of ______ India.",
  ["The, no article", "No article, the", "The, the", "An, no article"], 0,
  "'The' with the names of oceans and seas; no article with the names of most countries",
  "Oceans take 'the': 'the Indian Ocean'. Most country names take no article: 'India'. So: 'The Indian Ocean lies "
  "to the south of India.'",
  ["Ocean name → the", "Country name (single word) → no article", "'The, no article'"],
  "'No article, the' reverses the rule. 'The, the' wrongly puts 'the' before India. 'An Indian Ocean' would suggest "
  "one of several Indian oceans.", 25)

Q(AR, "Definite and indefinite", A, AR_STEM + "______ Japanese are known all over the world for their politeness.",
  ["The", "A", "An", "No article"], 0,
  "'The' + a nationality adjective ending in -ese, -ch, -sh or -ss refers to the whole people",
  "Nationality words such as Japanese, Chinese, French and Swiss do not add -s in the plural. To refer to the people "
  "as a whole, they take 'the': 'The Japanese are known ... for their politeness.'",
  ["'Japanese' as a people", "Nationality in -ese: 'the' + adjective = the whole people", "'The'"],
  "'A' and 'an' are singular and clash with 'are' and 'their'. Without an article, 'Japanese' would be read as the "
  "language or an adjective missing its noun.", 30)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", I, PP_STEM + "The new science teacher is very popular ______ her students.",
  ["with", "by", "to", "for"], 0,
  "Fixed preposition: popular with (a group of people)",
  "A person liked by a group is 'popular with' that group: 'The new science teacher is very popular with her "
  "students.'",
  ["Adjective: popular", "Fixed pairing: popular with", "'with'"],
  "'Popular by', 'popular to' and 'popular for' (the last is used for the reason, as in 'popular for her "
  "patience') do not fit before the people who like her.", 25)

Q(PP, "Phrasal verbs", A, PP_STEM + "The two brothers fell ______ over the division of their father's land and "
  "have not spoken since.",
  ["out", "off", "through", "back"], 0,
  "Phrasal verb: fall out (with someone) = quarrel and stop being friendly",
  "The brothers quarrelled about the land and stopped speaking. To quarrel in this way is to 'fall out'.",
  ["Context: dispute over land, not speaking since", "Meaning: quarrel", "'fell out'"],
  "'Fall off' means decrease or drop from something. 'Fall through' means fail to happen (a plan). 'Fall back' "
  "means retreat. None means to quarrel.", 30)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"
CN_STEM = "Choose the connector that best fills the blank.\n"

Q(CN, "Sentence connectors", B, CN_STEM + "The chemist's shop was closed, ______ we went to the one across the road.",
  ["so", "but", "because", "unless"], 0,
  "'So' introduces a result",
  "Going to another shop is the result of the first shop being closed: 'The chemist's shop was closed, so we went to "
  "the one across the road.'",
  ["Clause 1: shop closed (cause)", "Clause 2: went elsewhere (result)", "Result → 'so'"],
  "'But' signals a contrast that is not there. 'Because' would make going across the road the reason the shop was "
  "closed. 'Unless' sets a condition that makes no sense.", 20)

Q(CN, "Sentence connectors", B, CN_STEM + "She studied very hard for the test, ______ she did not get the marks she "
  "had hoped for.",
  ["but", "so", "because", "unless"], 0,
  "'But' joins two facts that contrast",
  "Studying hard should bring good marks, yet she did not get them. The unexpected result is introduced by 'but'.",
  ["Clause 1: studied hard", "Clause 2: did not get the marks (unexpected)", "Contrast → 'but'"],
  "'So' would make hard work the cause of low marks. 'Because' reverses the logic. 'Unless' sets a condition that "
  "does not fit.", 20)

Q(CN, "Sentence connectors", B, CN_STEM + "Please wait here ______ I come back with the tickets.",
  ["until", "unless", "although", "because"], 0,
  "'Until' = up to the time when",
  "The listener is to wait up to the moment the speaker returns: 'Please wait here until I come back with the "
  "tickets.'",
  ["Action: wait", "End point: my return", "'until'"],
  "'Unless' makes waiting depend on a condition that makes no sense. 'Although' and 'because' signal contrast and "
  "reason, which do not fit.", 20)

Q(CN, "Sentence connectors", I,
  CN_STEM + "A landslide had blocked the main road; ______, the buses were sent through the next valley.",
  ["hence", "besides", "likewise", "nevertheless"], 0,
  "'Hence' introduces a consequence",
  "Sending the buses by another route is a result of the main road being blocked, so the linker is 'hence' (= for "
  "this reason).",
  ["Clause 1: road blocked (cause)", "Clause 2: buses diverted (result)", "Result → 'hence'"],
  "'Besides' adds a further point. 'Likewise' signals a similar action. 'Nevertheless' signals a contrast; none of "
  "these shows a result.", 25)

Q(CN, "Starters and linkers", I,
  "Combine the two sentences into one without changing the meaning, and choose the correct combined sentence.\n"
  "You can pay now. You can pay on delivery.",
  ["You can pay either now or on delivery.", "You can pay neither now nor on delivery.",
   "You can pay both now and on delivery.", "You can either pay now nor on delivery."], 0,
  "'Either ... or' joins two alternatives",
  "The two sentences give two choices of when to pay. Alternatives are joined by 'either ... or': 'You can pay either "
  "now or on delivery.'",
  ["Relation: two alternatives", "Correlative: either ... or", "'You can pay either now or on delivery.'"],
  "'Neither ... nor' denies both choices. 'Both ... and' means paying twice. 'Either ... nor' mixes two "
  "correlatives.", 30)

Q(CN, "Starters and linkers", A,
  "Choose the option that best fills the blank.\n"
  "______ as it may seem, the cheaper option often costs more in the long run.",
  ["Strange", "So strange", "Too strange", "Very strange"], 0,
  "Concessive pattern: adjective + as + subject + verb (= although it may seem strange)",
  "'Strange as it may seem' means 'although it may seem strange'. Only the bare adjective fits this pattern.",
  ["Pattern: Adjective + as + it may seem", "Meaning: although it may seem ...", "'Strange'"],
  "'So', 'too' and 'very' cannot stand before the adjective in this concessive pattern.", 30)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

# questions whose key was also recomputed by this script
RECOMPUTED = {(P3, 2), (P4, 2)}
for q in QS:
    if (q.get("stimulus_id"), q.get("set_position")) in RECOMPUTED:
        q["verification"]["verified_by"] = ["ai:author-solve", "script:recompute", "ai:independent-check"]

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


for seed in range(9009, 14000):
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

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_009_plan.json").read_text(encoding="utf-8"))
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

# no reused stem or passage title across the earlier English files (BATCH_000 to BATCH_008)
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
# BATCH_008 for this batch.
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

# earlier-key / bold-word repeat scan: no word, idiom or phrase keyed or tested in BATCH_000 to BATCH_008 is keyed or
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
    "batch_id": "BATCH_009",
    "created_at": TODAY,
    "notes": "BATCH_009 English Language part: 149 original questions (BANK_ENG_001203 to BANK_ENG_001351). Five "
             "reading passages (28 questions) and three cloze passages (16 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 to BATCH_008; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules, words and idioms not tested in earlier batches "
             "(checked by the builder against all earlier keyed and bold words). Each answer was set by the author "
             "and re-solved in a separate blind pass by fresh checkers without the key; the sari discount (RC 3) "
             "and the guarantor's liability (RC 4) are also recomputed by the builder. Pending human review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_009_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))}, seed {seed})")
