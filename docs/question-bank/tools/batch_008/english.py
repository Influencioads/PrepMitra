"""Writes batches/parts/BATCH_008_ENG.json: the 149 English Language questions of BATCH_008.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000 to BATCH_007, and the grammar rules, idioms and words tested are ones not tested in those batches (where
a grammar area was already covered, it is tested here through a different rule or a context-based item). Run from
anywhere:

    python docs/question-bank/tools/batch_008/english.py

Structural checks (quota per topic and difficulty, subtopics, ID range, passage length, set sizes, option count, cloze
blank numbering, 'No error' / 'No replacement' / 'No swap' placement, para-jumble option validity, RC option-length
spread, repeated stems, passage titles and passage themes against all earlier English files, keyed words and bold
words against all earlier English files, answer-key balance) and the computable answers (the chit-fund pool in RC 3
and the trader's cash need in RC 5) are asserted before anything is written. Option letters are never named in
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
FIRST_ID = 1054
FIRST_STIM = 8001
EARLIER = ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json", "parts/BATCH_002_ENG.json",
           "parts/BATCH_003_ENG.json", "parts/BATCH_004_ENG.json", "parts/BATCH_005_ENG.json",
           "parts/BATCH_006_ENG.json", "parts/BATCH_007_ENG.json")

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
P1 = stim("Glasses for working hands", (
    "Somewhere in their forties, most people notice a small but annoying change. The print in the newspaper seems "
    "smaller than it used to be, and they begin to hold their phones further away to read a message. This is "
    "presbyopia, the gradual loss of the eye's ability to focus on nearby objects. It is not a disease. It happens to "
    "almost everyone with age, because the lens inside the eye slowly becomes less flexible.\n\n"
    "For an office worker in a city, the remedy is simple: a visit to an optician and a pair of reading glasses. For "
    "many people in villages and small towns, however, the change can quietly damage their livelihood. A tailor who "
    "cannot see the eye of a needle, a weaver who can no longer follow a fine pattern, or a farmer who cannot sort "
    "seeds may work more slowly and earn less, often in the very years when their skills are at their best.\n\n"
    "What makes this loss especially sad is how easily it can be prevented. Simple reading glasses are among the "
    "cheapest of all medical aids. In most cases a trained health worker with a basic reading chart can find the "
    "right strength in a few minutes.\n\n"
    "The difficulty lies in reaching people. Many have never had their eyes tested, and some believe that weak near "
    "vision is simply a part of growing old that must be accepted. Others worry that glasses will make their eyes "
    "lazy, or feel embarrassed to wear them in front of their neighbours.\n\n"
    "Several voluntary groups now hold eye camps at weekly markets and village fairs, where people can try on "
    "glasses and take home a pair that suits them. Organisers say the reaction is often the same. A woman threads a "
    "needle at the first attempt, or an old shopkeeper reads his account book without squinting, and then laughs in "
    "surprise. For a small cost, years of good work are given back."))

Q(RC, "Factual", B,
  "According to the passage, what causes presbyopia?",
  ["Reading on mobile phones for many hours a day",
   "The lens inside the eye becoming less flexible with age",
   "An infection that spreads in crowded villages",
   "A poor diet in the years before middle age"], 1,
  "Locating a stated cause",
  "Paragraph 1: presbyopia 'happens to almost everyone with age, because the lens inside the eye slowly becomes "
  "less flexible.'",
  ["Find 'presbyopia' in paragraph 1", "Look for 'because'", "The lens becomes less flexible with age"],
  "Holding a phone further away is a sign of presbyopia, not its cause. The passage says it 'is not a disease', so "
  "an infection is wrong. Diet is never mentioned.", 35, P1, 1)

Q(RC, "Factual", B,
  "Which of the following workers is NOT mentioned in the passage as being affected by weak near vision?",
  ["A tailor threading a needle",
   "A weaver following a fine pattern",
   "A farmer sorting seeds",
   "A driver reading road signs"], 3,
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 2 names a tailor, a weaver and a farmer who sorts seeds. A driver is never mentioned; reading distant "
  "road signs is not even a near-vision task.",
  ["Tailor: stated", "Weaver: stated", "Farmer sorting seeds: stated", "Driver: not in the passage"],
  "The tailor, the weaver and the farmer are all named in paragraph 2, so none of them can be the answer.",
  35, P1, 2)

Q(RC, "Factual", B,
  "According to the passage, which of the following is one reason why some people do not get reading glasses?",
  ["They believe weak near vision must simply be accepted in old age.",
   "Reading glasses are among the costliest medical aids available.",
   "Only doctors in large cities are allowed to test eyesight.",
   "Glasses cannot be worn by people who work outdoors."], 0,
  "Locating a stated reason",
  "Paragraph 4: 'some believe that weak near vision is simply a part of growing old that must be accepted.' Others "
  "fear lazy eyes or feel embarrassed.",
  ["Find 'The difficulty lies in reaching people'", "Reasons listed: belief, worry, embarrassment",
   "Belief that it must be accepted"],
  "Paragraph 3 calls glasses 'among the cheapest of all medical aids', the opposite of costliest. It says a trained "
  "health worker can test eyes, so doctors are not required. Outdoor work is never mentioned.", 40, P1, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'remedy' as used in the passage ('For an office worker "
  "in a city, the remedy is simple')?",
  ["solution", "danger", "price", "habit"], 0,
  "Vocabulary in context: remedy = a way of putting a problem right",
  "The sentence goes on to name what fixes the problem: a visit to an optician and reading glasses. A remedy is a "
  "cure or solution.",
  ["Context: a visit to an optician and a pair of glasses", "These put the problem right", "'solution'"],
  "'Danger' and 'habit' do not describe a fix. 'Price' is about cost; the sentence names what to do, not what it "
  "costs.", 30, P1, 4)

Q(RC, "Inference", B,
  "What does the author mean by the closing words 'years of good work are given back'?",
  ["People get back the money they spent on eye camps.",
   "Workers can go on using their skills well for many more years.",
   "Old people are given back the jobs they had lost.",
   "Glasses make people feel younger than they really are."], 1,
  "Inference: the meaning of a summing-up phrase",
  "Paragraph 2 says weak near vision makes skilled workers slow down 'in the very years when their skills are at "
  "their best'. Cheap glasses let them see well again, so they can keep working well for years.",
  ["Problem: skilled people lose working years", "Glasses restore near vision", "So those working years return"],
  "No refund of money is mentioned. Nobody is said to have lost a job and got it back. Feeling younger is not "
  "suggested; the phrase is about work.", 40, P1, 5)

Q(RC, "Tone and title", B,
  "Which of the following is the most suitable title for the passage?",
  ["Seeing Clearly, Working Longer", "Diseases of the Ageing Eye", "The Rising Cost of Spectacles",
   "City Opticians and Their Customers"], 0,
  "Title: the idea that runs through every paragraph",
  "The passage explains a normal change in near vision, shows how it harms the work of village craftspeople and "
  "farmers, and describes how cheap glasses restore their working lives.",
  ["Para 1: near vision weakens with age", "Paras 2-4: the effect on work and why people go without glasses",
   "Para 5: glasses give working years back"],
  "Presbyopia is 'not a disease'. The passage says glasses are cheap, not costly. City opticians appear in one "
  "sentence only.", 35, P1, 6)

# ---------------------------------------------------------------- RC 2 (Basic 2 + Intermediate 4)
P2 = stim("Paths that walkers choose", (
    "Walk through almost any park or college campus and you will find them: narrow strips of bare earth cutting "
    "across the grass, often running at an angle between two paved paths. Nobody planned them. They were made by "
    "thousands of people who decided, one step at a time, that the official route was too long. Planners call them "
    "'desire lines' or 'desire paths'.\n\n"
    "Such paths appear for a simple reason. Most people, when they are in a hurry, take the shortest route they can "
    "see. If a paved path turns a corner at a right angle, walkers will cut the corner. Once a few have done so, the "
    "grass wears thin, a faint line becomes visible, and others follow it, so that within weeks the faint track "
    "becomes a clear one.\n\n"
    "For a long time, the usual response was to fight the walkers. Park managers put up fences, planted hedges or "
    "added signs asking people to keep off the grass. These measures rarely worked for long. A fence would be "
    "stepped over or a gap would be pushed through a hedge, and the path would reappear a little further along.\n\n"
    "Some planners now take the opposite view. Instead of treating desire paths as damage, they treat them as "
    "information. A path worn across a lawn shows exactly where people want to go, which is something no drawing "
    "can predict with certainty. Some have even suggested waiting until a new campus has been in use for a few "
    "months before laying its walkways, so that the paved paths can follow the tracks that appear.\n\n"
    "The idea reaches beyond parks. Designers of websites, offices and public services face the same question: "
    "should people be made to follow the route that was planned for them, or should the route be redrawn to follow "
    "people? Desire paths suggest that when many people keep ignoring a design, the fault may lie with the design "
    "rather than with the people."))

Q(RC, "Factual", B,
  "According to the passage, why do desire paths appear?",
  ["Park managers mark them out for walkers in a hurry.",
   "People in a hurry take the shortest route they can see.",
   "Grass does not grow well near paved paths.",
   "Children are told to play away from the paved paths."], 1,
  "Locating a stated reason",
  "Paragraph 2: 'Most people, when they are in a hurry, take the shortest route they can see.' Cutting corners wears "
  "the grass into a path.",
  ["Find 'Such paths appear for a simple reason'", "Next sentence gives the reason", "Shortest visible route"],
  "Paragraph 1 says 'Nobody planned them', so managers did not mark them. Poor grass and children's play are never "
  "mentioned.", 35, P2, 1)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'faint' as used in the passage ('a faint line becomes "
  "visible')?",
  ["barely noticeable", "very wide", "freshly paved", "carefully planned"], 0,
  "Vocabulary in context: faint = weak, only just able to be seen",
  "The line is faint at first and 'within weeks the faint track becomes a clear one'. The contrast with 'clear' "
  "shows that faint means only just visible.",
  ["Contrast: faint track → clear one", "Faint = not yet clear", "'barely noticeable'"],
  "A path worn by feet is not 'freshly paved' or 'carefully planned' (nobody planned it). 'Very wide' contradicts "
  "the narrow strips described in paragraph 1.", 30, P2, 2)

Q(RC, "Factual", I,
  "Which of the following is NOT mentioned in the passage as a way in which park managers tried to stop walkers?",
  ["Putting up fences", "Planting hedges", "Adding keep-off-the-grass signs", "Posting guards to fine walkers"], 3,
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 3 lists fences, hedges and signs asking people to keep off the grass. Guards and fines are never "
  "mentioned.",
  ["Fences: stated", "Hedges: stated", "Signs: stated", "Guards and fines: not in the passage"],
  "Fences, hedges and signs are all stated in paragraph 3, so none of them can be the answer.", 35, P2, 3)

Q(RC, "Inference", I,
  "What do the planners mentioned in paragraph 4 mean when they treat desire paths 'as information'?",
  ["The paths show where people actually want to walk, which helps in planning routes.",
   "The paths are recorded so that walkers who damage the grass can be identified.",
   "The paths prove that most visitors cannot read the signs in the park.",
   "The paths tell managers how many people visit the park each day."], 0,
  "Inference: the meaning of a phrase from the sentence that follows it",
  "The next sentence explains: 'A path worn across a lawn shows exactly where people want to go.' Planners use this "
  "to decide where the paved paths should run.",
  ["'treat them as information' is explained next", "Paths show where people want to go",
   "Used to plan walkways"],
  "Identifying walkers, people's reading ability and visitor counts are never discussed; the passage uses the paths "
  "to learn where people want to go.", 45, P2, 4)

Q(RC, "Inference", I,
  "With which of the following statements would the author most probably agree?",
  ["Walkers who cut across lawns should be made to pay for the damage.",
   "When many users keep ignoring a design, the design should be reconsidered.",
   "Paved paths should never be built in parks or college campuses.",
   "Signs and fences are the best way to protect a well-designed park."], 1,
  "Inference: identifying the author's view from the conclusion",
  "The last paragraph says that when many people keep ignoring a design, 'the fault may lie with the design rather "
  "than with the people'. The author favours redrawing routes to follow people.",
  ["Para 4: paths treated as useful information", "Para 5: fault may lie with the design",
   "So: reconsider the design"],
  "The author never suggests fining walkers. Paved paths are not rejected, only placed where people walk. Paragraph 3 "
  "says fences and signs 'rarely worked for long'.", 45, P2, 5)

Q(RC, "Tone and title", I,
  "Which of the following best describes the author's attitude to desire paths?",
  ["angry at the people who damage public lawns",
   "open to learning from them when planning routes",
   "indifferent to how parks and campuses are planned",
   "sad that old gardens are disappearing from cities"], 1,
  "Tone: the author's attitude, judged from the conclusion",
  "The author presents desire paths as useful information and ends by suggesting that designs may need to follow "
  "people. The attitude is open and appreciative.",
  ["Desire paths = information, not damage", "Conclusion: redraw routes to follow people",
   "Attitude: open to learning from them"],
  "The author does not blame walkers, so 'angry' is wrong. A writer who discusses planning in detail is not "
  "indifferent. Disappearing gardens are never mentioned.", 40, P2, 6)

# ---------------------------------------------------------------- RC 3 (Intermediate, 6)
P3 = stim("The pot that is auctioned", (
    "In many Indian towns, long before banks reached every street, families saved and borrowed through the chit fund. "
    "The idea is simple. Suppose twenty people agree to pay one thousand rupees each month for twenty months. Every "
    "month, the whole pool collected from the members goes to one member, so that by the end, every member has "
    "received the pool once.\n\n"
    "Who gets the money first? In most chit funds, members who need cash urgently bid for it. The pool goes to the "
    "member who is willing to give up the largest amount, called the discount. That discount, after the organiser's "
    "fee is deducted, is shared among the other members as a kind of dividend, which reduces what each of them pays "
    "that month. A member who takes the pool early therefore receives less than he will eventually pay in, while a "
    "member who waits until the end receives the full pool after paying less than his full share in most months.\n\n"
    "In effect, the chit fund is both a savings scheme and a loan. Early takers borrow from the group and pay for it "
    "through the discount; late takers save and are rewarded for their patience. Because members often know one "
    "another, the group can judge who is likely to keep paying, something a distant bank cannot easily do.\n\n"
    "The arrangement has obvious risks. A member who takes the pool early may stop paying once he has the money. A "
    "dishonest organiser may disappear with the collections. For this reason, chit funds in India are regulated by "
    "law, and registered funds must follow rules on how they are run. Unregistered schemes, however, continue to "
    "operate in many places, and from time to time some of them collapse, leaving members with heavy losses.\n\n"
    "Supporters argue that, when it is run honestly, the chit fund offers something that formal finance often does "
    "not: credit that is quick, flexible and decided by people who know the borrower. Critics reply that the same "
    "informality that makes it useful also makes it dangerous."))

MEMBERS, MONTHLY = 20, 1000
POOL = MEMBERS * MONTHLY
assert POOL == 20000
Q(RC, "Factual", I,
  "In the example in the first paragraph, how much is the full monthly pool, before any discount is deducted?",
  ["₹1,000", "₹20,000", "₹4,00,000", "₹19,000"], 1,
  "Reading a worked example: pool = number of members × monthly payment",
  "Twenty members each pay ₹1,000 a month, so the pool collected every month is 20 × ₹1,000 = ₹20,000, and the whole "
  "pool goes to one member.",
  ["Members: 20", "Each pays ₹1,000 a month", "Pool = 20 × 1,000 = ₹20,000"],
  "₹1,000 is one member's monthly payment. ₹4,00,000 is the total paid over all twenty months. ₹19,000 leaves out one "
  "member's payment for no reason the passage gives.", 40, P3, 1)

Q(RC, "Factual", I,
  "According to the passage, how is it decided in most chit funds who receives the pool in a given month?",
  ["The organiser chooses the member he trusts most.",
   "Members bid, and the one willing to give up the most gets it.",
   "Names are drawn by lottery at a monthly meeting.",
   "The oldest member always receives it first."], 1,
  "Locating a stated procedure",
  "Paragraph 2: members who need cash 'bid for it. The pool goes to the member who is willing to give up the largest "
  "amount, called the discount.'",
  ["Find 'Who gets the money first?'", "Members bid", "Largest discount wins the pool"],
  "The organiser's choice, a lottery and age are never given as the method in most chit funds.", 40, P3, 2)

Q(RC, "Inference", I,
  "Why does the passage say that a member who takes the pool early is, in effect, paying for a loan?",
  ["He must pay the organiser's fee twice over.",
   "He receives less than he will pay in over the months.",
   "He has to pay interest to a bank on the amount.",
   "He is not allowed to take part in later auctions."], 1,
  "Inference: linking the mechanism to the 'savings and loan' idea",
  "The early taker gives up a discount, so the pool he gets is smaller than the total he will contribute. That "
  "difference is the cost of getting the money early, like interest on a loan.",
  ["Early taker accepts a discount", "Receives less than he pays in", "The gap is the price of early money"],
  "No double fee or bank interest is mentioned. The passage never says early takers are barred from later auctions; "
  "each member simply receives the pool once.", 45, P3, 3)

Q(RC, "Inference", I,
  "What advantage of the chit fund over a distant bank does the passage point out?",
  ["Members know one another and can judge who is likely to keep paying.",
   "It is never affected by dishonest organisers or defaulting members.",
   "It pays a fixed rate of interest that is guaranteed by law.",
   "Its members do not need to pay anything until they receive the pool."], 0,
  "Inference: identifying a stated contrast",
  "Paragraph 3: 'Because members often know one another, the group can judge who is likely to keep paying, something "
  "a distant bank cannot easily do.'",
  ["Find 'a distant bank' in paragraph 3", "Members know one another", "They can judge who will keep paying"],
  "Paragraph 4 describes dishonest organisers and defaults, so 'never affected' is false. No guaranteed interest is "
  "mentioned. Every member pays each month from the start.", 40, P3, 4)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'collapse' as used in the passage ('from time to time "
  "some of them collapse, leaving members with heavy losses')?",
  ["fail suddenly", "grow quickly", "merge together", "close for a holiday"], 0,
  "Vocabulary in context: collapse = fail suddenly and completely",
  "A scheme that leaves its members 'with heavy losses' has failed. 'Collapse' here means fail suddenly.",
  ["Result: heavy losses for members", "The scheme has failed", "'fail suddenly'"],
  "Growing, merging or closing for a holiday would not leave members with heavy losses.", 30, P3, 5)

Q(RC, "Tone and title", I,
  "Which of the following best states the main idea of the passage?",
  ["Chit funds combine saving and borrowing in a way that is useful but risky.",
   "Chit funds should be banned because unregistered schemes often collapse.",
   "Banks have now replaced chit funds in every Indian town.",
   "Members who wait until the end of a chit fund always lose money."], 0,
  "Main idea: balance the mechanism, the benefits and the risks",
  "The passage explains how a chit fund works, shows that it is both a savings scheme and a loan, describes its "
  "risks and ends with the views of supporters and critics.",
  ["Paras 1-2: how it works", "Para 3: saving plus borrowing; local knowledge", "Paras 4-5: risks and the debate"],
  "The passage never calls for a ban. It says unregistered schemes 'continue to operate', so banks have not replaced "
  "them. Paragraph 2 says late takers are 'rewarded for their patience'.", 45, P3, 6)

# ---------------------------------------------------------------- RC 4 (Intermediate 2 + Advanced 3)
P4 = stim("When a fine becomes a fee", (
    "A group of day-care centres had a familiar problem: some parents arrived late to collect their children, so "
    "that teachers had to stay on after closing time. The solution seemed obvious. Introduce a small fine for every "
    "late pick-up, and parents would surely become more punctual.\n\n"
    "When economists studied what happened after such a fine was introduced at a number of day-care centres in "
    "Israel, they found the opposite. The number of late arrivals rose and settled at a higher level than before. "
    "More surprising still, when the fine was later withdrawn, lateness did not fall back to its old level.\n\n"
    "The researchers offered an explanation that has since become well known. Before the fine, a parent who came "
    "late felt that he was imposing on a teacher's goodwill, and that sense of guilt kept most parents on time. The "
    "fine changed how the situation was understood. Lateness was no longer a favour taken from a teacher but a "
    "service that could be bought, and a modest price for an extra half-hour seemed reasonable to many parents. Once "
    "the moral question had been turned into a commercial one, removing the price did not turn it back.\n\n"
    "The lesson is not that penalties never work. A fine large enough to hurt will usually change behaviour, and "
    "many rules depend on penalties to be obeyed at all. The point is narrower: when people already behave well out "
    "of duty, pride or a sense of fairness, a small payment can weaken those motives instead of adding to them. "
    "Psychologists sometimes describe this as money 'crowding out' other reasons for acting.\n\n"
    "The same risk may appear elsewhere. A small reward for volunteering, for instance, could make the work feel "
    "like a poorly paid job rather than a good deed. Policy makers who reach for fines and rewards, therefore, need "
    "to ask not only how large an incentive should be, but also what message it sends about the behaviour it is "
    "meant to change."))

Q(RC, "Factual", I,
  "According to the passage, what happened when the fine for late pick-up was withdrawn?",
  ["Lateness quickly fell back to its old level.",
   "Lateness did not fall back to its old level.",
   "Parents began to arrive earlier than before.",
   "The day-care centres stopped staying open late."], 1,
  "Locating a stated result",
  "Paragraph 2: 'when the fine was later withdrawn, lateness did not fall back to its old level.'",
  ["Find 'withdrawn' in paragraph 2", "Lateness stayed high", "Did not return to the old level"],
  "Falling back quickly is the opposite of what the passage says. Earlier arrivals and changed opening hours are "
  "never mentioned.", 35, P4, 1)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to 'imposing on' as used in the passage ('he was imposing on a "
  "teacher's goodwill')?",
  ["taking unfair advantage of", "giving official orders to", "adding a heavy tax to", "praising in front of"], 0,
  "Vocabulary in context: impose on someone = take unfair advantage of their kindness",
  "A late parent made a teacher stay on unpaid, relying on her kindness. That is taking unfair advantage of her "
  "goodwill, which is why the parent felt guilty.",
  ["Context: teacher stays late out of goodwill", "The parent feels guilty", "'taking unfair advantage of'"],
  "A parent does not order a teacher, tax her goodwill or praise it; none of these would cause the guilt the "
  "passage describes.", 35, P4, 2)

Q(RC, "Inference", A,
  "According to the researchers' explanation, why did late arrivals increase after the fine was introduced?",
  ["The fine was too large for most parents to pay, so they stopped caring.",
   "Teachers began to leave earlier, so more parents were counted as late.",
   "The fine turned lateness into a service that could be bought, easing parents' guilt.",
   "Parents who paid the fine were allowed to collect their children at any time."], 2,
  "Inference: following the causal chain in an explanation",
  "Before the fine, guilt about imposing on teachers kept parents punctual. The fine made lateness 'a service that "
  "could be bought', and a modest price seemed reasonable, so the guilt that had kept parents on time disappeared.",
  ["Before: guilt kept parents on time", "Fine: lateness became something one could buy",
   "Guilt gone, price small → more lateness"],
  "The passage calls the fine 'modest', not too large. Teachers leaving early and unlimited collection times are "
  "never mentioned.", 50, P4, 3)

Q(RC, "Inference", A,
  "With which of the following statements would the author most probably agree?",
  ["Penalties of any size never change the way people behave.",
   "A small payment can weaken good behaviour that rests on a sense of duty.",
   "Volunteers always do better work when they are paid a small amount.",
   "Day-care centres should keep their teachers on duty until every child is collected."], 1,
  "Inference: distinguishing the author's narrow claim from an overstatement",
  "Paragraph 4 says 'The lesson is not that penalties never work', and that 'when people already behave well out of "
  "duty, pride or a sense of fairness, a small payment can weaken those motives'.",
  ["Author rejects 'penalties never work'", "Narrow point: small payments can crowd out duty",
   "Matches the statement about weakening good behaviour"],
  "The author says large fines usually work, so 'never change' is wrong. Paragraph 5 suggests a small reward could "
  "harm volunteering, the opposite of 'always do better'. Teachers' duty hours are not the author's argument.",
  50, P4, 4)

Q(RC, "Tone and title", A,
  "Which of the following is the most suitable title for the passage?",
  ["When a Price Replaces a Duty", "Why Parents Are Always Late", "The Failure of All Penalties",
   "How Day-Care Centres Make Money"], 0,
  "Title: the central idea, not the example used to illustrate it",
  "The day-care study is the example; the central idea is that a small fine or payment can replace a moral duty with "
  "a commercial deal and so backfire.",
  ["Example: day-care fines", "Explanation: lateness became something one could buy",
   "General lesson: money can crowd out duty"],
  "The passage is not about why parents are late in general. It says penalties do not always fail. Earning money for "
  "day-care centres is not discussed.", 40, P4, 5)

# ---------------------------------------------------------------- RC 5 (Advanced, 4)
P5 = stim("Profitable but out of cash", (
    "Ask a shopkeeper whether his business is doing well, and he will probably answer in terms of profit: how much "
    "more he sells his goods for than he paid for them. Yet a surprising number of firms that earn a profit on paper "
    "close down because they run out of cash. To understand how, it helps to separate two ideas that are easily "
    "confused.\n\n"
    "Profit measures whether a sale earns more than it costs. Cash measures whether there is money in the bank today "
    "to pay the bills that are due today. The two can drift far apart because they move at different times. A "
    "wholesaler may pay his supplier on delivery, store the goods for a month, and then sell them to retailers who "
    "are allowed sixty days to pay. For three months, the money he has spent is tied up in stock and in amounts owed "
    "to him. The sale may be profitable, but in the meantime he must still pay rent, wages and electricity.\n\n"
    "Growth makes the problem worse rather than better. Consider a trader who buys goods for ₹80,000 and sells them "
    "for ₹1,00,000 on two months' credit. Each such order earns ₹20,000 of profit, but it also locks up ₹80,000 until "
    "the buyer pays. If the trader doubles the number of such orders, his expected profit doubles, but so does the "
    "cash he must find in advance. A firm that grows faster than its cash can support may collapse at the very "
    "moment its order book looks healthiest.\n\n"
    "This is why lenders look closely at the working-capital cycle, the time between paying for inputs and receiving "
    "cash from customers. Shortening it, by collecting dues faster, holding less stock or negotiating longer credit "
    "from suppliers, frees cash without any change in profit. Banks offer overdrafts and short-term loans to bridge "
    "the gap, but these carry interest and are best arranged before a crisis arrives, not after.\n\n"
    "An old business saying puts the point bluntly: turnover is vanity, profit is sanity, but cash is king. A "
    "business can survive for a while without profit; it cannot survive for long without cash."))

COST, SALE = 80000, 100000
assert SALE - COST == 20000
CASH_NEEDED_DOUBLED = 2 * COST
assert CASH_NEEDED_DOUBLED == 160000
Q(RC, "Factual", A,
  "In the trader's example, if he doubles the number of orders, how much cash must he find in advance to pay for "
  "the goods?",
  ["₹40,000", "₹1,60,000", "₹2,00,000", "₹80,000"], 1,
  "Applying a worked example: cash locked up = purchase cost per order × number of orders",
  "Each order locks up the ₹80,000 paid for the goods until the buyer pays. Doubling the orders doubles this: "
  "2 × ₹80,000 = ₹1,60,000. The passage says the cash he must find in advance doubles along with profit.",
  ["Cash locked per order = purchase cost = ₹80,000", "Orders doubled → × 2", "2 × 80,000 = ₹1,60,000"],
  "₹40,000 is the doubled profit, not the cash needed. ₹2,00,000 is the doubled sale value, which he receives later. "
  "₹80,000 is the need for a single order, before doubling.", 50, P5, 1)

Q(RC, "Inference", A,
  "Why, according to the passage, can a fast-growing firm collapse just when its order book looks healthiest?",
  ["Larger orders always earn a smaller profit per sale.",
   "Each extra order locks up more cash before customers pay.",
   "Banks refuse to lend to firms whose sales are growing.",
   "Suppliers raise their prices when a firm buys more."], 1,
  "Inference: the mechanism behind a paradox",
  "Every order requires paying for goods in advance while the buyer pays later. More orders mean more cash tied up, "
  "so a firm can run out of cash even though each order is profitable.",
  ["Paying first, being paid later", "More orders → more cash tied up", "Cash runs out despite profits"],
  "The passage says profit doubles with orders, so profit per sale does not shrink. Banks are said to offer "
  "overdrafts, not refuse them. Supplier price rises are never mentioned.", 50, P5, 2)

Q(RC, "Inference", A,
  "Which of the following would free cash for the trader without changing his profit, according to the passage?",
  ["Persuading his suppliers to allow him longer credit",
   "Raising his selling price by ten per cent",
   "Selling more goods on the same credit terms",
   "Paying his suppliers earlier to win their goodwill"], 0,
  "Inference: applying the listed remedies to a new case",
  "Paragraph 4 lists ways to shorten the working-capital cycle 'without any change in profit', including "
  "'negotiating longer credit from suppliers'. Paying later keeps cash with the trader longer.",
  ["Remedies: collect faster, hold less stock, longer supplier credit", "Longer supplier credit = pay later",
   "Cash freed, profit unchanged"],
  "Raising prices changes profit. Selling more on the same terms locks up more cash. Paying suppliers earlier "
  "lengthens the cycle and uses up cash.", 50, P5, 3)

Q(RC, "Tone and title", A,
  "Which of the following is the most suitable title for the passage?",
  ["Why Profitable Firms Can Still Run Out of Money", "How to Raise Prices Without Losing Customers",
   "The Vanity of Large Businesses", "Banks That Refuse to Lend to Traders"], 0,
  "Title: the question the whole passage answers",
  "The passage opens with firms that are profitable on paper but close for lack of cash, explains why profit and "
  "cash differ, shows how growth worsens the gap and ends with 'cash is king'.",
  ["Opening puzzle: profitable firms closing", "Body: profit vs cash, growth, working capital",
   "Conclusion: cash is king"],
  "Pricing is not discussed. 'Vanity' appears only in the saying, about turnover, not about large businesses. Banks "
  "are described as offering loans, not refusing them.", 45, P5, 4)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic 5 + Intermediate 1)
C1 = stim("Walls that give", (
    "On a busy road in some Indian cities, you may come across an unusual wall. Rows of hooks and hangers are fixed "
    "to it, and on them hang shirts, sweaters, blankets and children's clothes. A painted sign above them carries a "
    "simple (1) ______: 'Leave what you do not need; take what you need.'\n\n"
    "These 'walls of kindness' are usually started by a few residents or a local group. The rules are few. Anyone who "
    "has clean clothes that they no longer wear can hang them up, and anyone who needs them can take them, without "
    "asking (2) ______ and without having to explain why. There is no counter, no form to fill in and no one keeping "
    "(3) ______ of who gives and who takes.\n\n"
    "Supporters say this is exactly what makes the idea work. Many people who badly need a warm blanket in winter "
    "feel (4) ______ to stand in a queue and ask for charity. At the wall, they can choose quietly, like any other "
    "passer-by. Donors, for their part, find it easier to give when they can simply stop on their way to work.\n\n"
    "The walls are not free of problems. Some fill up with torn or dirty clothes that nobody can use, and in the "
    "rainy season, clothes left in the open can be (5) ______ within days. Volunteers who look after the walls often "
    "sort the clothes every evening and take the unusable ones away.\n\n"
    "Still, the idea has spread, and some groups have added shelves for books, toys and shoes. A wall, after all, is "
    "usually built to keep people apart. These walls do the (6) ______: they bring together people who might "
    "otherwise never meet."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["message", "price", "complaint", "warning"], 0,
  "Cloze: what a sign 'carries' when it states an idea",
  "The sign states the idea of the wall: leave what you do not need, take what you need. A sign that carries such "
  "words carries a message.",
  ["Words on the sign: an invitation to give and take", "A sign carries a message", "'message'"],
  "The wall is free, so a 'price' does not fit. The words are not a 'complaint'. They invite people rather than warn "
  "them of danger, so 'warning' does not fit.", 25, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["permission", "directions", "the weather", "a loan"], 0,
  "Cloze: taking freely, without anyone's approval",
  "Anyone who needs the clothes can simply take them, without asking anyone for permission and without explaining "
  "why.",
  ["'take them, without asking ___'", "Taking freely = no approval needed", "'permission'"],
  "Asking 'directions', 'the weather' or 'a loan' has nothing to do with taking clothes from a wall.", 25, C1, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["records", "quiet", "promises", "secrets"], 0,
  "Cloze: the fixed phrase 'keep records of'",
  "Along with 'no counter' and 'no form to fill in', the sentence says nobody notes down who gives and who takes: no "
  "one is keeping records of it.",
  ["List: no counter, no form, no one keeping ___", "'___ of who gives and who takes'", "'keeping records of'"],
  "'Keeping quiet of', 'keeping promises of' and 'keeping secrets of' who gives and who takes are not idiomatic and "
  "do not continue the list of missing paperwork.", 30, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["ashamed", "eager", "proud", "lucky"], 0,
  "Cloze: the feeling the wall helps people avoid",
  "At the wall, needy people can 'choose quietly, like any other passer-by'. This helps because many feel ashamed to "
  "queue up and ask for charity.",
  ["Contrast: queueing for charity vs choosing quietly", "Queueing for charity is embarrassing for many",
   "'ashamed'"],
  "If people felt 'eager', 'proud' or 'lucky' to queue for charity, the quiet wall would not be what makes the idea "
  "work.", 25, C1, 4)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=5), ["ruined", "ironed", "sold", "folded"], 0,
  "Cloze: a problem caused by rain",
  "The paragraph lists problems. Clothes left in the open during the rainy season get wet and dirty and become "
  "useless: they are ruined.",
  ["Context: problems with the walls", "Clothes left out in the rain", "'ruined'"],
  "Ironing and folding are improvements, not problems. Nothing on the wall is sold.", 25, C1, 5)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=6), ["opposite", "same", "impossible", "repairs"], 0,
  "Cloze: a contrast with what walls usually do",
  "A wall is 'usually built to keep people apart'. These walls bring people together, which is the opposite.",
  ["Usual walls: keep people apart", "These walls: bring people together", "'do the opposite'"],
  "'Do the same' would mean these walls also keep people apart. 'Do the impossible' and 'do the repairs' do not set "
  "up the contrast that follows the colon.", 25, C1, 6)

# ---------------------------------------------------------------- Cloze 2 (Intermediate, 6)
C2 = stim("The mark that will not wash off", (
    "At every election in India, a voter who has cast her vote leaves the polling station with a small dark line on "
    "her left forefinger. It is drawn by a polling official with a special ink, and fingers are checked before anyone "
    "is allowed to vote. The mark is a simple but effective (1) ______ against fraud: anyone who tries to vote a "
    "second time can be spotted at once, because a finger that already carries the mark gives the game away.\n\n"
    "The ink owes its staying power to silver nitrate. When it is applied to the skin and (2) ______ to light, the "
    "chemical reacts with the outer layer of the skin and leaves a stain that cannot be removed with soap, oil or "
    "ordinary cleaning liquids. The mark does not wash away; it (3) ______ only slowly, as old skin cells are "
    "naturally shed and replaced by new ones, a process that usually takes some weeks.\n\n"
    "For decades, the ink used in Indian elections has been made by a public-sector company in Karnataka, which also "
    "supplies it to a number of other countries for their elections. The exact formula is closely (4) ______, and "
    "each batch is tested for quality before it is (5) ______ to polling stations across the country.\n\n"
    "Critics sometimes point out that, in an age of electronic voter lists and photo identity cards, such an "
    "old-fashioned method seems (6) ______. Election officials reply that its strength lies precisely in its "
    "simplicity. It needs no electricity, no network connection and no special training. A glance at a voter's finger "
    "is enough to tell whether she has already voted."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["safeguard", "invitation", "reward", "excuse"], 0,
  "Cloze: 'a ___ against fraud' needs a word meaning protection",
  "The mark lets officials spot anyone who tries to vote twice, so it protects the election against fraud: it is a "
  "safeguard.",
  ["'a simple but effective ___ against fraud'", "It catches people who try to vote twice", "'safeguard'"],
  "An 'invitation', a 'reward' or an 'excuse' against fraud makes no sense; the mark prevents fraud.", 30, C2, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["exposed", "opposed", "composed", "disposed"], 0,
  "Cloze: confusable '-posed' words; exposed to light = left open to light",
  "The ink reacts once it is on the skin and left in light. The phrase is 'exposed to light'.",
  ["'applied to the skin and ___ to light'", "Light acts on the chemical", "'exposed'"],
  "'Opposed to' means against; 'composed' means made up of or calm; 'disposed to' means inclined to. None describes "
  "ink being left in light.", 30, C2, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["fades", "spreads", "darkens", "multiplies"], 0,
  "Cloze: 'does not wash away; it ___ only slowly' describes gradual disappearance",
  "The mark disappears gradually as old skin cells are shed. Something that disappears gradually fades.",
  ["Contrast: does not wash away", "Gradual loss as skin is replaced", "'fades'"],
  "'Spreads', 'darkens' and 'multiplies' describe the mark growing or strengthening, which does not fit skin being "
  "shed and replaced.", 30, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["guarded", "published", "ignored", "borrowed"], 0,
  "Cloze: 'closely guarded' (kept secret) is a fixed collocation for a formula or secret",
  "A formula made by only one supplier for decades is kept secret: it is 'closely guarded'.",
  ["'The exact formula is closely ___'", "One maker, a secret formula", "'guarded'"],
  "'Closely published' is self-contradictory. 'Closely ignored' and 'closely borrowed' are not idiomatic and do not "
  "fit a valued formula.", 30, C2, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["dispatched", "withheld", "subjected", "borrowed"], 0,
  "Cloze: sending goods 'to polling stations'",
  "After testing, each batch is sent out to polling stations: it is dispatched to them.",
  ["Order: tested, then sent", "'___ to polling stations'", "'dispatched'"],
  "'Withheld' means kept back, the opposite of supplying. 'Subjected to' means made to undergo, and ink is not "
  "'borrowed' to polling stations; neither describes sending supplies.", 30, C2, 5)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=6), ["outdated", "futuristic", "compulsory", "invisible"], 0,
  "Cloze: what critics would say about an 'old-fashioned method' in a digital age",
  "Critics contrast the ink with electronic lists and photo cards, suggesting it belongs to the past: it seems "
  "outdated. The officials' reply defends its simplicity.",
  ["Contrast: electronic lists vs an old-fashioned ink", "Critics' charge: it belongs to the past", "'outdated'"],
  "'Futuristic' contradicts 'old-fashioned'. 'Compulsory' is not a criticism linked to modern technology. The mark is "
  "plainly visible, so 'invisible' is wrong.", 30, C2, 6)

# ---------------------------------------------------------------- Cloze 3 (Intermediate 3 + Advanced 2)
C3 = stim("The money left on the card", (
    "A gift card seems like the perfect present. The buyer does not have to guess the receiver's taste, and the "
    "receiver can choose whatever she likes. For the shops that sell them, however, gift cards have an added "
    "(1) ______ that is rarely advertised: part of the money loaded on them is never spent.\n\n"
    "Some cards are lost in drawers, some are forgotten, and many are used for a purchase that leaves a balance too "
    "(2) ______ to bother with. In the retail trade, this unspent money is known as 'breakage'. Because the shop has "
    "already received the full amount when the card was sold, every rupee that is never used is, in effect, pure "
    "(3) ______.\n\n"
    "Shops also gain in less obvious ways. A customer with a card worth one thousand rupees often spends more than "
    "that amount, paying the difference from her own pocket. And the money from cards sold before a festival stays "
    "with the seller for weeks or months before any goods are handed over, which amounts to an interest-free loan "
    "from the buyer.\n\n"
    "Consumer groups argue that expiry dates make the problem worse, since a card that (4) ______ after a year turns "
    "forgetfulness into a direct gain for the seller. In several countries, rules now limit how soon a gift card may "
    "expire or say how unused balances must be treated. The rules differ widely, however, and they are often "
    "(5) ______ by buyers who never read the fine print.\n\n"
    "None of this means that gift cards are a bad idea. It does mean that the most useful thing a giver can do, after "
    "handing over the card, is to remind the receiver to use it before the money quietly disappears."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["advantage", "drawback", "weakness", "nuisance"], 0,
  "Cloze: 'For the shops ..., however' sets up a benefit to sellers",
  "Money that is paid for but never spent is a gain for the shop. Gift cards therefore have an added advantage for "
  "sellers, one that is 'rarely advertised'.",
  ["Unspent money stays with the shop", "That is a gain for the seller", "'advantage'"],
  "'Drawback', 'weakness' and 'nuisance' describe disadvantages, but the colon introduces a gain for shops.", 30, C3, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["small", "large", "valuable", "generous"], 0,
  "Cloze: 'too ___ to bother with'",
  "People do not bother with a leftover balance because it is too small to be worth the trouble.",
  ["Pattern: too + adjective + to bother with", "A balance not worth the effort", "'small'"],
  "A 'large', 'valuable' or 'generous' balance is exactly what people would bother to spend.", 30, C3, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["profit", "loss", "debt", "tax"], 0,
  "Cloze: money received for which nothing is ever given",
  "The shop has been paid in full, and if the card is never used it hands over no goods. That money is pure profit.",
  ["Shop already paid in full", "No goods handed over for unused money", "'pure profit'"],
  "For the shop this money is a gain, not a 'loss'. It is not a 'debt' or a 'tax', which the shop would owe to "
  "someone.", 30, C3, 3)

Q(CL, "Single-blank cloze", A, CLOZE_STEM.format(n=4), ["expires", "matures", "multiplies", "reopens"], 0,
  "Cloze: 'expiry dates' in the same sentence decide the verb",
  "The sentence is about expiry dates: a card that expires after a year cannot be used after that, so a forgotten "
  "balance becomes the seller's gain.",
  ["Topic: expiry dates", "A card that stops being valid after a year", "'expires'"],
  "'Matures' is used for deposits or bonds that become payable, which would help the holder. 'Multiplies' and "
  "'reopens' do not turn forgetfulness into a gain for the seller.", 35, C3, 4)

Q(CL, "Single-blank cloze", A, CLOZE_STEM.format(n=5), ["overlooked", "overseen", "overstated", "overtaken"], 0,
  "Cloze: confusable 'over-' verbs; overlook = fail to notice",
  "Buyers 'who never read the fine print' fail to notice the rules: the rules are overlooked by them.",
  ["Clue: buyers never read the fine print", "Rules go unnoticed", "'overlooked'"],
  "'Overseen' means supervised, which buyers do not do. 'Overstated' means exaggerated and 'overtaken' means passed; "
  "neither fits people who do not read the rules.", 35, C3, 5)

# ---------------------------------------------------------------- Cloze 4 (Advanced, 6; error-based)
C4 = stim("Paying for power in advance", (
    "For decades, electricity in most Indian homes has been paid for after it is used. A meter reader visits, a bill "
    "arrives weeks later, and the household pays, or **(1) delays**, as its finances allow. Prepaid smart meters "
    "reverse this order. Like a mobile phone, the meter must be recharged before power can be used, and the balance "
    "falls as electricity is consumed.\n\n"
    "Distribution companies see clear advantages. A large share of their losses comes from bills that are paid late "
    "or never paid at all, and from errors in reading meters by hand. A prepaid meter **(2) widens** both gaps: the "
    "money arrives in advance, and readings are sent automatically. Supporters add that customers benefit too, since "
    "they can track their daily use on a phone and are no longer **(3) surprised** by a large bill at the end of a "
    "hot summer month.\n\n"
    "The concerns are mostly about poorer households. A family that runs out of balance late at night may find its "
    "power cut before it can recharge, which is a serious matter during a heatwave or when a child is unwell. For "
    "this reason, many prepaid systems offer a small emergency credit, send repeated alerts as the balance runs low "
    "and avoid **(4) restoring** supply at night or on holidays.\n\n"
    "There is also a question of trust. When a new meter shows higher readings than the old one, customers often "
    "suspect that it is faulty, even when the old meter was simply **(5) overstating** their use. Utilities that "
    "install meters without explaining how they work have faced protests in several places.\n\n"
    "The technology itself is neither good nor bad. Whether prepaid meters help or hurt depends on how carefully they "
    "are **(6) introduced**: with clear information, a fair grace period and a quick way to settle complaints, or "
    "with none of these."))

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=1, ctx="a bill arrives weeks later, and the household pays, or delays, as its finances allow"),
  ["doubles", "receives", "earns", NR], 3,
  "Error-based cloze: under post-paid billing, a household short of money pays late",
  "With a bill paid after use, a household pays when it can, or puts off paying 'as its finances allow'. 'Delays' "
  "fits, and it also explains the late payments mentioned in paragraph 2.",
  ["Post-paid: bill comes after use", "'as its finances allow' → pay now or later", "'delays' fits: no replacement"],
  "A household does not 'double', 'receive' or 'earn' a bill as its finances allow; these do not describe a choice "
  "about paying.", 45, C4, 1, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=2, ctx="A prepaid meter widens both gaps: the money arrives in advance, and readings are sent "
                           "automatically"),
  ["closes", "hides", "creates", NR], 0,
  "Error-based cloze: the explanation after the colon shows both problems are solved",
  "Money arriving in advance ends late payment, and automatic readings end reading errors. The meter closes both "
  "gaps; 'widens' says the opposite.",
  ["Gap 1: late or unpaid bills → money now comes in advance", "Gap 2: reading errors → readings automatic",
   "Replace 'widens' with 'closes'"],
  "'Hides' and 'creates' do not match the solutions listed after the colon. 'Widens' contradicts them, so 'No "
  "replacement required' does not apply.", 45, C4, 2, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=3, ctx="they can track their daily use on a phone and are no longer surprised by a large bill at "
                           "the end of a hot summer month"),
  ["pleased", "protected", "informed", NR], 3,
  "Error-based cloze: tracking daily use removes the shock of a large bill",
  "Customers who see their use every day know what they are spending, so a big bill no longer comes as a shock: they "
  "are 'no longer surprised'. The word is correct.",
  ["Daily tracking → customers know their use", "A large bill is no longer unexpected",
   "'surprised' fits: no replacement"],
  "'No longer pleased by a large bill' and 'no longer informed by a large bill' do not describe a benefit of "
  "tracking. 'No longer protected by a large bill' is meaningless.", 45, C4, 3, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=4, ctx="many prepaid systems offer a small emergency credit, send repeated alerts as the balance "
                           "runs low and avoid restoring supply at night or on holidays"),
  ["cutting off", "measuring", "billing", NR], 0,
  "Error-based cloze: the safeguards protect families from losing power at a bad time",
  "The concern is power being cut late at night. To protect families, systems avoid cutting off supply at night or "
  "on holidays. Avoiding 'restoring' supply would make things worse.",
  ["Concern: power cut at night before recharge", "Safeguards: credit, alerts, no night cuts",
   "Replace 'restoring' with 'cutting off'"],
  "Avoiding 'measuring' or 'billing' supply at night does not address the danger described. 'Restoring' reverses "
  "the safeguard, so 'No replacement required' does not apply.", 50, C4, 4, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=5, ctx="When a new meter shows higher readings than the old one, customers often suspect that it "
                           "is faulty, even when the old meter was simply overstating their use"),
  ["understating", "displaying", "doubling", NR], 0,
  "Error-based cloze: higher new readings are explained by an old meter that recorded too little",
  "If the new meter reads higher and is accurate, the old one must have been recording less than the real use: it "
  "was understating it. An old meter that overstated use would have shown higher readings, not lower.",
  ["New reading higher than old", "New meter accurate → old meter read too low", "Replace 'overstating' with "
   "'understating'"],
  "'Displaying' and 'doubling' do not explain why the old readings were lower. 'Overstating' gives the reverse "
  "logic, so 'No replacement required' does not apply.", 50, C4, 5, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=6, ctx="Whether prepaid meters help or hurt depends on how carefully they are introduced"),
  ["abandoned", "disconnected", "forgotten", NR], 3,
  "Error-based cloze: the colon lists features of a careful roll-out",
  "Clear information, a grace period and quick complaint handling describe how the meters are brought in. "
  "'Introduced' is correct.",
  ["After the colon: information, grace period, complaints", "These describe a roll-out",
   "'introduced' fits: no replacement"],
  "Meters that are 'abandoned', 'disconnected' or 'forgotten' are not being rolled out with information and a grace "
  "period.", 40, C4, 6, order=LAST_FIXED)

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


# ---- Basic (6)
ed("Part-wise error", B, "May I lend your pen", "for a minute?", "Mine has run out of ink.", "A",
   "Lend = give for a time; borrow = take for a time",
   "The speaker wants to take and use someone else's pen for a minute, so the verb is 'borrow': 'May I borrow your "
   "pen for a minute?' One lends something to another person.",
   ["The speaker will take the pen", "Taking for a time = borrow", "'lend' → 'borrow': error in part A"],
   "Part B is a correct time phrase. Part C correctly gives the reason. A has an error, so 'No error' is wrong.", 25)

ed("Part-wise error", B, "An one-day workshop", "was organised", "for new account holders.", "A",
   "'A' or 'an' depends on the first sound: 'one' begins with a 'w' sound, so it takes 'a'",
   "'One' is pronounced with a consonant sound /w/, so the article is 'a': 'A one-day workshop was organised ...'.",
   ["First sound of 'one': /w/ (a consonant sound)", "Consonant sound → 'a'", "'An one-day' → 'A one-day': error in "
    "part A"],
   "Part B is a correct singular passive verb. Part C is a correct purpose phrase. A has an error, so 'No error' is "
   "wrong.", 25)

ed("Part-wise error", B, "Before filing his return,", "he took", "some useful advise from a tax consultant.", "C",
   "Advice (noun, the 'c' form) vs advise (verb, the 's' form)",
   "After 'some useful', a noun is needed. The noun is 'advice'; 'advise' is the verb ('to advise someone'). Correct: "
   "'he took some useful advice from a tax consultant.'",
   ["'some useful ___' needs a noun", "Noun: advice; verb: advise", "'advise' → 'advice': error in part C"],
   "Part A is a correct participle phrase. Part B is a correct past tense. C has an error, so 'No error' is wrong.",
   25)

ed("Part-wise error", B, "At the staff meeting,", "the news of the merger", "were announced by the chairman.", "C",
   "'News' looks plural but is an uncountable noun and takes a singular verb",
   "'News' is singular in meaning and grammar: 'the news of the merger was announced by the chairman.'",
   ["Subject: 'the news' (uncountable)", "Uncountable noun → singular verb", "'were announced' → 'was announced': "
    "error in part C"],
   "Part A is a correct place phrase. Part B is a correct subject; 'of the merger' does not change its number. C has "
   "an error, so 'No error' is wrong.", 30)

ed("Part-wise error", B, "Two masked men", "robbed fifty thousand rupees", "from the cash van.", "B",
   "Rob a person or place (of something); steal a thing (from someone)",
   "The object here is the money, the thing taken, so the verb is 'steal': 'Two masked men stole fifty thousand "
   "rupees from the cash van.' One robs a van or a bank, not the money.",
   ["Object: fifty thousand rupees (the thing taken)", "Thing taken → steal", "'robbed' → 'stole': error in part B"],
   "Part A is a correct subject. Part C correctly uses 'from' with the place the money was taken from. B has an "
   "error, so 'No error' is wrong.", 30)

ed("Error-free sentence", B, "The customer to whom", "the cheque was issued", "has not yet deposited it.", "D",
   "'Whom' as the object of a preposition ('to whom'); present perfect with 'not yet'",
   "'To whom' is correct because 'whom' is the object of 'to' (the cheque was issued to him). 'Has not yet deposited "
   "it' agrees with the singular 'The customer' and uses the present perfect with 'yet'.",
   ["Part A: preposition + whom: correct", "Part B: passive 'was issued': correct",
    "Part C: singular subject, 'has not yet deposited': correct", "No error"],
   "A, B and C are each correct as shown in the steps.", 30)

# ---- Intermediate (4)
ed("Part-wise error", I, "Afraid of losing his job,", "the junior clerk dare not to complain",
   "about his long hours.", "B",
   "'Dare not' used as a modal takes a bare infinitive (dare not complain), like 'must not' or 'need not'",
   "In the negative modal form, 'dare' has no '-s' and is followed directly by the base verb: 'the junior clerk dare "
   "not complain'. (As a main verb the pattern is 'does not dare (to) complain'.) 'Dare not to complain' mixes the "
   "two.",
   ["'dare not' = modal form", "Modal + bare infinitive", "'dare not to complain' → 'dare not complain': error in "
    "part B"],
   "Part A is a correct adjective phrase with 'of' + -ing. Part C is a correct prepositional phrase. B has an error, "
   "so 'No error' is wrong.", 40)

ed("Part-wise error", I, "Once the auditors", "finish to check the vouchers,", "the branch can close its books.", "B",
   "'Finish' takes a gerund (-ing form) as its object, never a to-infinitive",
   "'Finish' is followed by the -ing form: 'Once the auditors finish checking the vouchers, the branch can close its "
   "books.'",
   ["Verb: finish", "Pattern: finish + -ing", "'finish to check' → 'finish checking': error in part B"],
   "Part A is a correct start to a time clause; the present tense 'finish' is right for a future time after 'once'. "
   "Part C is a correct main clause. B has an error, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "After a two-month inquiry,", "the clerk who forged the signatures",
   "has been charged of cheating.", "C",
   "Fixed preposition: charged WITH an offence (but accused OF an offence)",
   "The verb 'charge' in the legal sense takes 'with': 'the clerk ... has been charged with cheating.' 'Of' belongs "
   "with 'accused'.",
   ["Verb: charge (legally)", "Fixed pairing: charged with", "'charged of' → 'charged with': error in part C"],
   "Part A is a correct time phrase. Part B is a correct subject with a relative clause. C has an error, so 'No "
   "error' is wrong.", 35)

ed("Error-free sentence", I, "The premises of the old branch", "are being converted", "into a training centre.", "D",
   "'Premises' (a building and its land) is always plural in form and takes a plural verb",
   "'Premises' in this sense has no singular form and takes a plural verb, so 'The premises ... are being converted' "
   "is correct. 'Converted into' is the right preposition.",
   ["Part A: 'premises' = the building and its grounds", "Part B: plural verb 'are being converted': correct",
    "Part C: 'converted into': correct", "No error"],
   "A, B and C are each correct as shown in the steps. 'Is being converted' would be wrong, because 'premises' takes "
   "a plural verb.", 35)

# ---- Advanced (5)
ed("Part-wise error", A, "Despite the bank cut its rates twice,", "demand for home loans",
   "remained weak through the year.", "A",
   "'Despite' is a preposition: it takes a noun or -ing form, not a full clause",
   "A full clause ('the bank cut its rates') cannot follow 'despite'. Correct forms: 'Despite the bank's cutting its "
   "rates twice', 'Despite two rate cuts by the bank', or 'Although the bank cut its rates twice, ...'.",
   ["'Despite' = preposition", "A preposition cannot take a clause with a finite verb",
    "'Despite the bank cut' → 'Although the bank cut': error in part A"],
   "Part B is a correct subject. Part C is a correct verb with an adjective complement. A has an error, so 'No "
   "error' is wrong.", 45)

ed("Part-wise error", A, "The borrower did not repay the loan,", "nor he replied", "to any of the bank's notices.", "B",
   "After 'nor' introducing a clause, the auxiliary comes before the subject (inversion)",
   "'Nor' at the start of a clause works like a negative adverb, so the subject and auxiliary are inverted: '..., nor "
   "did he reply to any of the bank's notices.'",
   ["'nor' begins a new clause", "Inversion: nor + auxiliary + subject + base verb", "'nor he replied' → 'nor did he "
    "reply': error in part B"],
   "Part A is a correct negative clause. Part C correctly uses 'reply to'. B has an error, so 'No error' is wrong.", 45)

ed("Error-free sentence", A, "Little did the clerk realise", "that the customer he had helped",
   "was the bank's new chairman.", "D",
   "Inversion after the negative adverb 'Little' (= not at all); past perfect for the earlier action",
   "'Little did the clerk realise' correctly inverts the auxiliary 'did' and the subject after 'Little' used in a "
   "negative sense. 'He had helped' is correctly earlier than 'realise', and 'was' agrees with 'the customer'.",
   ["Part A: Little + did + subject + base verb: correct", "Part B: past perfect for the earlier action: correct",
    "Part C: singular 'was' with 'the customer': correct", "No error"],
   "A, B and C are each correct as shown in the steps. 'Little the clerk realised' would be the error, not the "
   "inverted form.", 45)

ed("Part-wise error", A, "The new app is both faster", "and it is easier to use", "than the old one.", "B",
   "Correlative 'both ... and' must join items of the same grammatical type (parallelism)",
   "'Both' comes before an adjective ('faster'), so 'and' must also be followed by an adjective: 'The new app is both "
   "faster and easier to use than the old one.' 'And it is easier' adds a whole clause.",
   ["'both' + adjective (faster)", "'and' + must match: adjective (easier)", "'and it is easier' → 'and easier': "
    "error in part B"],
   "Part A correctly places 'both' before the first adjective. Part C completes the comparison correctly. B has an "
   "error, so 'No error' is wrong.", 45)

ed("Part-wise error", A, "The auditors found that the manager had approved", "large loans to two firms",
   "which his brother was a director.", "C",
   "In a relative clause, the preposition needed by the verb or noun cannot be dropped (a director OF which)",
   "His brother was a director 'of' the firms, so the relative clause needs 'of which': '... large loans to two firms "
   "of which his brother was a director.'",
   ["Underlying idea: his brother was a director OF the firms", "Relative pronoun keeps the preposition",
    "'which his brother' → 'of which his brother': error in part C"],
   "Part A correctly uses the past perfect after 'found'. Part B is a correct object phrase. C has an error, so 'No "
   "error' is wrong.", 45)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", B,
  SI_STEM + "The tea in the canteen was **very hot to drink**, so he waited for it to cool.",
  ["too hot to drink", "very hot for drinking", "so hot to drink", NI], 0,
  "'Too + adjective + to-infinitive' shows that something is more than is acceptable for the action",
  "The tea was hotter than he could drink, so he waited. Excess that prevents an action is shown by 'too ... to': "
  "'The tea ... was too hot to drink.'",
  ["Meaning: hot enough to stop him drinking", "Pattern: too + adjective + to-infinitive", "'too hot to drink'"],
  "'Very hot for drinking' and 'so hot to drink' do not express excess correctly ('so' needs 'that': so hot that he "
  "could not drink it). The original uses 'very', so 'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "**The both brothers** run the family's grain shop together.",
  ["Both the brothers", "The both of brothers", "Both brother", NI], 0,
  "'Both' comes before the article: both the + plural noun (never 'the both')",
  "'Both' is placed before 'the', not after it: 'Both the brothers (or Both brothers) run the family's grain shop "
  "together.'",
  ["Word order: both + the + noun", "'the both' is wrong", "'Both the brothers'"],
  "'The both of brothers' keeps the wrong order and adds 'of' without a pronoun. 'Both brother' needs a plural noun. "
  "The original puts 'the' before 'both', so 'No improvement required' is wrong.", 30, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "Ramesh visited the branch **for withdrawing** money from his pension account.",
  ["to withdraw", "for to withdraw", "for withdraw", NI], 0,
  "A person's purpose in doing something is expressed by the to-infinitive (infinitive of purpose)",
  "Ramesh's purpose in visiting the branch is shown with 'to': 'Ramesh visited the branch to withdraw money from his "
  "pension account.' ('For + -ing' describes what a thing is used for, as in 'a form for withdrawing money'.)",
  ["The phrase gives Ramesh's purpose", "Purpose of an action → to-infinitive", "'to withdraw'"],
  "'For to withdraw' and 'for withdraw' are ungrammatical. 'For withdrawing' describes the use of a thing, not a "
  "person's purpose, so 'No improvement required' is wrong.", 30, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "Customers should **pay attention towards** the fine print before signing a loan agreement.",
  ["pay attention to", "pay attention at", "pay attention on", NI], 0,
  "Fixed collocation: pay attention to (something)",
  "The noun 'attention' with 'pay' takes 'to': 'Customers should pay attention to the fine print ...'.",
  ["Collocation: pay attention", "Fixed preposition: to", "'pay attention to'"],
  "'At' and 'on' are not used after 'pay attention', and 'towards' is not standard here either, so 'No improvement "
  "required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "The new branch is **twice as larger as** the old one.",
  ["twice as large as", "twice larger as", "two times as larger than", NI], 0,
  "Multiplier comparisons use 'as + base adjective + as' (twice as large as)",
  "In 'as ... as' comparisons the adjective stays in its base form, with the multiplier in front: 'The new branch is "
  "twice as large as the old one.'",
  ["Pattern: multiplier + as + adjective + as", "Base form inside 'as ... as'", "'twice as large as'"],
  "'Twice larger as' mixes a comparative with 'as'. 'Two times as larger than' mixes both patterns. The original "
  "uses a comparative inside 'as ... as', so 'No improvement required' is wrong.", 30, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "After paying the school fees, I **have no any money** left for this month.",
  ["have no money", "have any no money", "have not no money", NI], 0,
  "'No' and 'any' are not used together; use 'no + noun' or 'not ... any + noun'",
  "'No' already makes the sentence negative, so 'any' cannot follow it: 'I have no money left' (or 'I do not have "
  "any money left').",
  ["'no' is a negative determiner", "'no any' doubles the determiner", "'have no money'"],
  "'Any no money' is ungrammatical, and 'not no money' is a double negative. The original combines 'no' and 'any', "
  "so 'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "She **would rather walk** to the branch than wait for the bus in the heat.",
  ["would rather walking", "would rather to walk", "had rather to walk", NI], 3,
  "'Would rather' + bare infinitive (... than + bare infinitive) for a preference",
  "'Would rather' is followed by the base form of the verb, and so is 'than': 'She would rather walk to the branch "
  "than wait for the bus in the heat.' The sentence is correct.",
  ["Expression of preference: would rather", "Followed by the base verb: walk", "'than wait' matches: correct"],
  "'Would rather walking' uses an -ing form, and 'would rather to walk' and 'had rather to walk' add 'to'; all three "
  "break the pattern.", 30, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "**Unlike the old branch**, the new branch's vault has two separate locks.",
  ["Unlike the old branch's vault", "Unlike in the old branch's", "Unlike with the old branch", NI], 0,
  "'Unlike' must compare like with like: the thing after 'unlike' must be the same kind of thing as the subject",
  "The subject is 'the new branch's vault', so it must be compared with a vault, not with a branch: 'Unlike the old "
  "branch's vault, the new branch's vault has two separate locks.'",
  ["Subject compared: the new branch's vault", "'Unlike the old branch' compares a vault with a branch",
   "Compare vault with vault: 'Unlike the old branch's vault'"],
  "'Unlike in the old branch's' leaves the possessive without a noun, and 'Unlike with the old branch' adds a "
  "preposition and still compares a branch with a vault. The original is a faulty comparison, so 'No improvement "
  "required' is wrong.", 45, order=LAST_FIXED)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", B,
  PR_STEM + "It took the old clerk almost a month to **get on** his fever.",
  ["get over", "get off", "get by", NR], 0,
  "Phrasal verb: get over (an illness or a shock) = recover from it",
  "Recovering from a fever is 'getting over' it: 'It took the old clerk almost a month to get over his fever.'",
  ["Meaning needed: recover from", "Phrasal verb: get over", "'get over'"],
  "'Get off' means leave a vehicle or escape punishment. 'Get by' means manage with little. 'Get on' means board or "
  "make progress; none means recover, so 'No replacement required' does not apply.", 25, order=LAST_FIXED)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The branch manager **dealt in** the customer's complaint within a day.",
  ["dealt with", "dealt by", "dealt at", NR], 0,
  "Deal with = handle or take action on; deal in = trade in (goods)",
  "A manager who handles a complaint 'deals with' it: 'The branch manager dealt with the customer's complaint within "
  "a day.' 'Deal in' is used for trading, as in 'He deals in spices'.",
  ["Meaning needed: handled the complaint", "Deal with = handle", "'dealt with'"],
  "'Dealt by' and 'dealt at' are not idiomatic. 'Dealt in' means traded in, which does not fit a complaint, so 'No "
  "replacement required' does not apply.", 30, order=LAST_FIXED)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", I, SC_OK,
  ["Him and me went to the branch together.",
   "He and me went to the branch together.",
   "Me and him went to the branch together.",
   "He and I went to the branch together."], 3,
  "Pronouns in a compound subject take the subject form (I, he), not the object form (me, him)",
  "Both pronouns are the subject of 'went', so both take the subject case: 'He and I went to the branch together.' "
  "Test each pronoun alone: 'He went', 'I went'.",
  ["Test alone: 'Him went' ✗, 'He went' ✓", "Test alone: 'Me went' ✗, 'I went' ✓", "'He and I went': correct"],
  "The others use the object forms 'him' or 'me' as subjects, which fails the test of saying each pronoun alone with "
  "'went'.", 30)

Q(SC, "Correct sentence", A, SC_OK,
  ["Give the form to whomever asks for it.",
   "Give the form to whoever asks for it.",
   "Give the form to anyone whom asks for it.",
   "Give the form to whoever ask for it."], 1,
  "The case of 'who(ever)' depends on its role inside its own clause, not on the preposition before the clause",
  "The whole clause 'whoever asks for it' is the object of 'to', but inside the clause 'whoever' is the subject of "
  "'asks', so the subject form is needed: 'Give the form to whoever asks for it.' The verb is singular.",
  ["Clause: '___ asks for it'", "Role inside the clause: subject of 'asks' → whoever",
   "'whoever asks' (singular verb): correct"],
  "'Whomever asks' and 'whom asks' use the object form as the subject of 'asks'. 'Whoever ask' does not agree: "
  "'whoever' takes a singular verb.", 45)

Q(SC, "Grammatically incorrect sentence", A, SC_BAD,
  ["The scissors on the table are blunt.",
   "A pair of scissors is lying on the table.",
   "These spectacles need new lenses.",
   "A new pair of spectacles were bought for the old clerk."], 3,
  "Plural-only nouns (scissors, spectacles) take plural verbs, but 'a pair of' + such a noun takes a singular verb",
  "When 'pair' is the head of the subject, the verb agrees with 'pair', which is singular: 'A pair of new spectacles "
  "was bought for the old clerk.'",
  ["'The scissors ... are': plural noun, plural verb: correct", "'A pair ... is': head 'pair', singular: correct",
   "'These spectacles need': plural: correct", "'A new pair ... were': head 'pair' is singular: incorrect"],
  "The other three follow the rule: plural verbs with 'scissors' and 'spectacles' on their own, and a singular verb "
  "after 'a pair of'.", 40)

Q(SC, "Grammatically incorrect sentence", A, SC_BAD,
  ["She resembles her mother in looks.",
   "The committee discussed the proposal at length.",
   "He married a doctor from Pune.",
   "The new clerk resembles to the old one in his habits."], 3,
  "Some verbs take a direct object with no preposition: resemble, discuss, marry",
  "'Resemble' is transitive and takes its object directly: 'The new clerk resembles the old one in his habits.' "
  "Adding 'to' is an error.",
  ["'resembles her mother': correct", "'discussed the proposal': correct", "'married a doctor': correct",
   "'resembles to the old one': extra preposition: incorrect"],
  "The other three use 'resemble', 'discuss' and 'marry' with a direct object, which is correct.", 35)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) Within minutes, a dozen passengers climbed down and began to push the bus from behind.\n"
  "(B) The village bus coughed, shuddered and stopped dead in the middle of a muddy road.\n"
  "(C) The driver tried the starter again and again, but the engine would not catch.\n"
  "(D) With a roar, the engine came to life, and a loud cheer went up from the roadside.\n"
  "(E) After a hundred metres of pushing, the driver let the clutch out with a jerk.",
  ["BCAED", "BACED", "CBAED", "BCADE"], 0,
  "Para jumble: breakdown → failed restart → passengers push → driver's action → success",
  "B describes the breakdown. C: the starter fails. A: passengers push. E: after pushing, the driver lets the "
  "clutch out. D: the engine roars to life.",
  ["Opener: B (the bus stops)", "B → C: the starter fails", "C → A: passengers push",
   "A → E (after pushing) → D (engine starts): BCAED"],
  "BACED has passengers pushing before anyone has tried the starter. CBAED has the driver trying to restart before "
  "the bus has stopped. BCADE has the engine start before the push-start that causes it.", 35)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) Planting a sapling properly takes only a few minutes.\n"
  "(P) First, dig a pit about twice as wide as the ball of soil around the sapling's roots.\n"
  "(Q) Place the sapling in the pit, fill the space around it with soil and press it down gently.\n"
  "(R) Finally, water it well and put a small fence around it to keep goats away.\n"
  "(S) Then loosen the soil at the bottom of the pit so that the roots can spread easily.",
  ["PSQR", "PQSR", "SPQR", "PSRQ"], 0,
  "Fixed opener; process words 'First', 'Then' and 'Finally', and the logic of each step",
  "P ('First') digs the pit. S ('Then') loosens its bottom. Q places the sapling and fills the pit. R ('Finally') "
  "waters and fences it.",
  ["(1) → P: 'First', dig", "P → S: 'Then', loosen the bottom of the pit", "S → Q: place the sapling",
   "Q → R: 'Finally': PSQR"],
  "PQSR loosens the bottom of the pit after the sapling is already in it. SPQR loosens a pit that has not been dug. "
  "PSRQ waters and fences before the sapling is planted.", 35)

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) Years later, she received a letter from Delhi signed 'Your student, Dr Rekha'.\n"
  "(B) Every evening, after her own school work, Kamla taught three village girls to read under the street lamp.\n"
  "(C) One of them, Rekha, was so eager that she began borrowing Kamla's old textbooks.\n"
  "(D) Rekha won the scholarship and went on to study medicine in the city.\n"
  "(E) Kamla gave her the books and helped her prepare for a scholarship examination.",
  ["BCEDA", "BECDA", "CBEDA", "BCDEA"], 0,
  "Para jumble: named opener → one pupil ('One of them') → help → result → years later",
  "B introduces Kamla and the three girls. C: one of them, Rekha, borrows books. E: Kamla helps her prepare. D: Rekha "
  "wins the scholarship. A ('Years later') closes with the letter.",
  ["Opener: B", "B → C: 'One of them'", "C → E: Kamla gives her the books",
   "E → D (wins the scholarship) → A ('Years later'): BCEDA"],
  "BECDA gives 'her' the books before Rekha is introduced. CBEDA opens with 'One of them' before the girls are "
  "mentioned. BCDEA has Rekha win the scholarship before preparing for it.", 35)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) Every Saturday morning, the residents of Shanti Nagar clean their colony together.\n"
  "(P) The volunteers first gather at the community hall, where gloves and bags are handed out.\n"
  "(Q) Once the bags are full, they are taken to the collection point at the end of the lane.\n"
  "(R) They then split into small groups, each of which takes one street.\n"
  "(S) By ten o'clock the work is done, and everyone shares tea and biscuits at the hall.",
  ["PRQS", "RPQS", "PQRS", "PRSQ"], 0,
  "Fixed opener; time order marked by 'first', 'then', 'Once the bags are full' and 'By ten o'clock'",
  "P ('first') gathers the volunteers and hands out bags. R ('then') splits them into groups. Q ('Once the bags are "
  "full') takes the bags away. S ('By ten o'clock') ends the work.",
  ["(1) → P: 'first' gather", "P → R: 'then' split into groups", "R → Q: full bags taken away",
   "Q → S: work done by ten: PRQS"],
  "RPQS splits 'They' into groups before they have gathered. PQRS fills the bags before the groups start work. PRSQ "
  "ends the work and serves tea before the bags are taken away.", 35)

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) When milk is heated, a thin layer of cream and proteins forms on its surface.\n"
  "(B) Anyone who has boiled milk knows how suddenly it can rise and spill over the edge of the pan.\n"
  "(C) Steam bubbles rising from below are trapped under this layer, which swells upward.\n"
  "(D) Stirring the milk or blowing on it breaks the layer and lets the steam escape.\n"
  "(E) This is why a cook watching a pan of milk keeps a spoon close at hand.",
  ["BACDE", "BCADE", "BADCE", "BACED"], 0,
  "Para jumble: familiar experience → cause (layer) → effect (trapped steam) → remedy → practical conclusion",
  "B states the familiar problem. A explains the layer that forms. C: steam is trapped under 'this layer'. D: "
  "stirring breaks it. E ('This is why ... a spoon') draws the practical conclusion from D.",
  ["Opener: B (the familiar problem)", "B → A: a layer forms", "A → C: 'this layer' traps steam",
   "C → D (stirring breaks it) → E (spoon at hand): BACDE"],
  "BCADE mentions 'this layer' before the layer is described. BADCE breaks the layer before explaining what it "
  "traps. BACED explains the spoon before saying that stirring helps.", 40)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Designers noticed that once people had their cash, many walked away and left their cards behind.\n"
  "(B) Early cash machines handed over the money first and returned the card afterwards.\n"
  "(C) The reason is simple: the person's goal was the cash, and once a goal is reached, attention moves on.\n"
  "(D) Most machines now return the card before the cash, so that the goal cannot be reached until the card is "
  "safely back.\n"
  "(E) The same principle is now applied elsewhere, by arranging tasks so that the step people tend to forget comes "
  "before the one they care about.",
  ["BACDE", "ABCDE", "BACED", "BCADE"], 0,
  "Para jumble: old design → problem → reason ('The reason is simple') → solution → wider use ('The same principle')",
  "B describes the old order. A gives the problem it caused. C explains why. D gives the redesign. E ('The same "
  "principle') extends the idea.",
  ["Opener: B (the old design)", "B → A: cards left behind", "A → C: 'The reason is simple'",
   "C → D (redesign) → E ('The same principle'): BACDE"],
  "ABCDE opens with the problem before the old design that caused it. BACED applies 'the same principle' before the "
  "principle (card first) is described. BCADE gives 'The reason' before the problem it explains.", 50)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) A passenger who books a train ticket when all berths are taken is given a waitlist number.\n"
  "(P) As other passengers cancel their bookings, the berths they release are allotted to those on the list, in "
  "order.\n"
  "(Q) Some hours before departure, when the final chart is prepared, she can see whether her ticket has been "
  "confirmed.\n"
  "(R) Her number therefore moves up the list each time a confirmed ticket is cancelled.\n"
  "(S) If it is still on the waitlist at that point, an online ticket is cancelled automatically and the fare "
  "refunded.",
  ["PRQS", "RPQS", "PQRS", "PRSQ"], 0,
  "Fixed opener; 'therefore', 'when the final chart is prepared' and 'at that point' as links",
  "P explains how cancelled berths go to the list. R ('therefore') draws the consequence for her number. Q gives the "
  "moment of the final chart. S ('at that point') says what happens if the ticket is still waitlisted.",
  ["(1) → P: how the list works", "P → R: 'therefore' her number moves up", "R → Q: the final chart",
   "Q → S: 'at that point': PRQS"],
  "RPQS uses 'therefore' before the rule it depends on. PQRS has her number moving up after the final chart. PRSQ "
  "uses 'at that point' before the chart is mentioned.", 50)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) For a small group of goods, however, a higher price can make them more desirable.\n"
  "(B) Ordinarily, when the price of a product rises, people buy less of it.\n"
  "(C) Luxury watches and designer handbags are often cited as Veblen goods, since part of their appeal lies in "
  "showing that the owner can afford them.\n"
  "(D) The economist Thorstein Veblen, who wrote about 'conspicuous consumption', gave his name to such goods.\n"
  "(E) For sellers of such status symbols, cutting prices can therefore be risky, since a cheaper item may lose "
  "the very exclusiveness buyers were paying for.",
  ["BADCE", "BACDE", "ABDCE", "BADEC"], 0,
  "Para jumble: general rule → exception ('however') → name ('such goods') → examples ('Veblen goods') → "
  "consequence ('therefore')",
  "B states the normal rule. A ('however') gives the exception. D names such goods after Veblen. C gives examples of "
  "'Veblen goods' whose appeal is showing wealth. E ('such status symbols', 'therefore') draws the consequence from C.",
  ["Opener: B (the normal rule)", "B → A: 'however', the exception", "A → D: Veblen gave his name to 'such goods'",
   "D → C ('Veblen goods' examples) → E ('therefore'): BADCE"],
  "BACDE calls the watches 'Veblen goods' before Veblen is introduced. ABDCE opens with 'however', which needs a rule "
  "before it. BADEC refers to 'such status symbols' and draws the 'therefore' conclusion before C explains that "
  "these goods show the owner can afford them.", 60)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) Safety measures do not always reduce accidents as much as engineers expect.\n"
  "(P) The reason, some researchers argue, is that people adjust their behaviour to the level of risk they feel.\n"
  "(Q) A driver who feels safer in a car with better brakes, for instance, may drive a little faster or follow the "
  "car ahead more closely.\n"
  "(R) In such a case, part of the benefit of the better brakes is used up by riskier driving.\n"
  "(S) This does not mean that safety measures are useless, only that their effect on behaviour must be counted "
  "along with their effect on equipment.",
  ["PQRS", "QPRS", "PRQS", "PQSR"], 0,
  "Fixed opener; general explanation → example ('for instance') → consequence ('In such a case') → qualification",
  "P gives the reason for (1). Q is an example ('for instance') of adjusting behaviour. R ('In such a case ... the "
  "better brakes') draws the result of the example. S qualifies the whole argument.",
  ["(1) → P: 'The reason'", "P → Q: 'for instance', the brakes example", "Q → R: 'In such a case', the brakes",
   "R → S: 'This does not mean ...': PQRS"],
  "QPRS gives the example before the claim it illustrates. PRQS mentions 'the better brakes' before the brakes are "
  "introduced. PQSR puts the qualification before the consequence it qualifies, leaving 'In such a case' cut off "
  "from its example.", 60)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) As a result, the cost of a concert, relative to the cost of manufactured goods, keeps climbing.\n"
  "(B) A string quartet written two centuries ago still needs four musicians and roughly the same playing time "
  "today.\n"
  "(C) Economists call this Baumol's cost disease, and it helps explain why services such as education and health "
  "care tend to grow more expensive over time.\n"
  "(D) Over the same period, the number of workers needed to make a shirt or a car has fallen sharply.\n"
  "(E) Yet musicians' wages have risen along with those in factories, because orchestras must pay enough to stop "
  "players leaving for other work.",
  ["BDEAC", "DBEAC", "BDAEC", "ABDEC"], 0,
  "Para jumble: example → contrast ('Over the same period') → twist ('Yet') → result ('As a result') → name",
  "B gives the unchanged quartet. D ('Over the same period') contrasts factory productivity. E ('Yet') says wages "
  "rose anyway. A ('As a result') gives the rising cost of concerts. C names the effect and widens it.",
  ["Opener: B (the quartet)", "B → D: 'Over the same period' factories improved", "D → E: 'Yet' wages rose",
   "E → A ('As a result') → C (the name): BDEAC"],
  "DBEAC opens with 'Over the same period' before any period is given. BDAEC puts the result before the rise in "
  "wages that causes it. ABDEC opens with 'As a result' before anything has been described.", 60)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) In 2003, a photographer put thousands of aerial pictures of the California coastline online to record "
  "coastal erosion.\n"
  "(P) One of them happened to show the clifftop house of the singer Barbra Streisand, who sued to have it "
  "removed.\n"
  "(Q) Until then, the picture had been downloaded only a handful of times.\n"
  "(R) Within a month of the case becoming public, however, hundreds of thousands of people had visited the site "
  "to look at it.\n"
  "(S) The attempt to hide the picture had made it famous, and such backfiring efforts to suppress information are "
  "now known as the Streisand effect.",
  ["PQRS", "QPRS", "PRQS", "PQSR"], 0,
  "Fixed opener; 'One of them', 'Until then', 'however' and the summing-up sentence as links",
  "P picks out one picture and the lawsuit. Q ('Until then') gives the few downloads before the case. R ('however') "
  "contrasts the huge interest after it. S sums up and names the effect.",
  ["(1) → P: 'One of them' (the pictures)", "P → Q: 'Until then' (the lawsuit)",
   "Q → R: 'however', hundreds of thousands", "R → S: the attempt backfired: PQRS"],
  "QPRS says 'Until then' before anything has happened to mark 'then'. PRQS puts the contrast word 'however' before "
  "the handful of downloads it contrasts with. PQSR names the effect before the surge in visits that shows it.", 60)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", B,
  SR_STEM + "(P) a cup of tea and a chair\n(Q) offered the tired farmer\n(R) the kind shopkeeper\n"
  "(S) as soon as he walked in",
  ["RQPS", "RPQS", "QRPS", "PRQS"], 0,
  "Subject + verb + indirect object + direct object + time clause",
  "'The kind shopkeeper offered the tired farmer a cup of tea and a chair as soon as he walked in.' Subject (R), verb "
  "with the person (Q), the things offered (P), time clause (S).",
  ["Subject: R", "Verb + person: Q", "Things offered P, then time S → RQPS"],
  "RPQS puts the objects between the subject and its verb. QRPS opens with a verb and no subject. PRQS opens with "
  "the objects and leaves the verb without its subject before it.", 30)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) that the fraud\n(Q) it was\n(R) came to light\n(S) only after the audit",
  ["QSPR", "SQRP", "PRQS", "QSRP"], 0,
  "Cleft sentence for emphasis: It was + focus + that + rest of the clause",
  "'It was only after the audit that the fraud came to light.' 'It was' (Q) + the emphasised phrase (S) + 'that the "
  "fraud' (P) + 'came to light' (R).",
  ["Frame: It was ... that ...", "Focus: only after the audit (S)", "Rest: that the fraud (P) came to light (R) → "
   "QSPR"],
  "SQRP gives 'Only after the audit it was came to light', which has no clear subject. PRQS separates the cleft "
  "frame from its focus. QSRP gives 'only after the audit came to light that the fraud', leaving 'the fraud' "
  "without a verb.", 35)

Q(SR, "Word/phrase rearrangement within a sentence", A,
  SR_STEM + "(P) is not more branches\n(Q) what the bank needs\n(R) but better-trained staff\n"
  "(S) to win back its customers",
  ["QSPR", "QRPS", "PQSR", "RQSP"], 0,
  "Pseudo-cleft: What-clause as subject + is + 'not X but Y'",
  "'What the bank needs to win back its customers is not more branches but better-trained staff.' The what-clause "
  "(Q + S) is the subject, 'is not more branches' (P) follows, and 'but better-trained staff' (R) completes the "
  "contrast.",
  ["Subject: 'what the bank needs' (Q) + purpose (S)", "Verb + first item: P", "'not ... but' completed by R → QSPR"],
  "QRPS puts 'but better-trained staff' before 'not more branches'. PQSR opens with a verb that has no subject. RQSP "
  "opens with 'but', which needs a 'not' before it.", 40)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The old bridge is no longer ______, so heavy lorries have been told to use the new road.",
  ["safe", "famous", "visible", "empty"], 0,
  "Single blank: the result clause ('so ...') decides the word",
  "Lorries are sent another way because the bridge cannot bear their weight any more: it is no longer safe.",
  ["Result: lorries must use the new road", "Reason: the bridge is risky", "'safe'"],
  "A bridge being no longer 'famous', 'visible' or 'empty' gives no reason to keep heavy lorries off it.", 20)

Q(FB, "Single blank", B,
  FB1 + "The farmers were ______ to see the first rain clouds after three months of drought.",
  ["relieved", "annoyed", "ashamed", "bored"], 0,
  "Single blank: the feeling that follows the end of a long worry",
  "After three months of drought, the first rain clouds end a long worry, so the farmers feel relieved.",
  ["Clue: rain after a long drought", "A worry is ending", "'relieved'"],
  "Farmers would not be 'annoyed', 'ashamed' or 'bored' to see rain after a drought.", 20)

Q(FB, "Double blank", B,
  FB2 + "The shop was ______ with customers on the eve of Diwali, so the owner had to ______ two extra helpers.",
  ["packed, hire", "empty, hire", "packed, dismiss", "quiet, appoint"], 0,
  "Double blank: a crowded shop needs more staff",
  "On a festival eve the shop is full of customers, so the owner needs more help: 'packed' and 'hire'.",
  ["Blank 1: festival eve → full of customers → packed", "'so' → more help needed", "Blank 2: hire"],
  "An 'empty' or 'quiet' shop would not need extra helpers. A packed shop would not lead the owner to 'dismiss' "
  "helpers.", 25)

Q(FB, "Phrase fillers", B,
  FBP + "The candle ______ when a gust of wind blew in through the open window.",
  ["went out", "went up", "went by", "went over"], 0,
  "Phrasal verb: go out = stop burning (a fire, a light or a candle)",
  "A gust of wind puts out a candle's flame: the candle 'went out'.",
  ["Cause: a gust of wind", "Effect on a flame: it stops burning", "'went out'"],
  "'Went up' means rose or caught fire suddenly. 'Went by' means passed. 'Went over' means examined. None means "
  "stopped burning.", 20)

Q(FB, "Single blank", B,
  FB1 + "Please speak ______; the baby is sleeping in the next room.",
  ["softly", "loudly", "rudely", "angrily"], 0,
  "Single blank: the reason after the semicolon decides the word",
  "A sleeping baby should not be woken, so people should speak quietly: softly.",
  ["Reason: a baby is sleeping nearby", "Speak without noise", "'softly'"],
  "Speaking 'loudly' would wake the baby. 'Rudely' and 'angrily' describe manner, not volume, and do not follow "
  "from the reason given.", 20)

Q(FB, "Single blank", I,
  FB1 + "The three small cooperatives decided to ______ their savings to build a shared cold store.",
  ["pool", "squander", "conceal", "divide"], 0,
  "Single blank: 'shared' shows the money is brought together",
  "To build one shared store, the cooperatives put their savings together into a common fund: they pool them.",
  ["Clue: a shared cold store", "Money combined from three groups", "'pool'"],
  "'Squander' (waste) and 'conceal' (hide) would not build anything. 'Divide' is the opposite of combining.", 25)

Q(FB, "Double blank", I,
  FB2 + "The ______ of the new metro line has ______ traffic on the main road, and buses now take half the time.",
  ["opening, eased", "opening, blocked", "delay, eased", "cost, reduced"], 0,
  "Double blank: the result clause (buses take half the time) decides both words",
  "Buses are faster because there is less traffic. That follows from the metro line opening and drawing travellers "
  "away: the opening has 'eased' traffic.",
  ["Result: buses take half the time", "So traffic has become lighter → eased", "Cause: the metro line has opened"],
  "Traffic that was 'blocked' would slow the buses. A 'delay' in the metro could not ease traffic. 'Cost' cannot "
  "reduce traffic.", 30)

Q(FB, "Phrase fillers", I,
  FBP + "Despite weeks of protests, the management refused to ______ on its decision to close the branch.",
  ["back down", "back up", "back in", "back onto"], 0,
  "Phrasal verb: back down (on) = withdraw a demand or decision under pressure",
  "Protests are pressure to change the decision. The management refused to give way: it would not 'back down' on "
  "its decision.",
  ["Context: weeks of protests (pressure)", "Refused to give way", "'back down'"],
  "'Back up' means support or make a copy. 'Back in' and 'back onto' describe moving a vehicle backwards. None means "
  "give way under pressure.", 25)

Q(FB, "Single blank", I,
  FB1 + "His ______ handwriting made the amount on the cheque impossible to read.",
  ["illegible", "ineligible", "eligible", "legible"], 0,
  "Confusable words: legible / illegible (readable / unreadable) vs eligible / ineligible (qualified / not qualified)",
  "Handwriting that cannot be read is 'illegible'.",
  ["Clue: impossible to read", "Unreadable writing → illegible", "'illegible'"],
  "'Legible' means readable, the opposite. 'Eligible' and 'ineligible' are about meeting conditions, not about "
  "writing.", 25)

Q(FB, "Single blank", A,
  FB1 + "Once a bustling port, the town is now ______, its warehouses empty and its streets silent.",
  ["desolate", "teeming", "burgeoning", "opulent"], 0,
  "Single blank: 'Once ... now' contrast, with the description after the comma",
  "Empty warehouses and silent streets describe a lonely, abandoned place: the town is now 'desolate'.",
  ["Contrast: once bustling → now the opposite", "Clue: empty, silent", "'desolate'"],
  "'Teeming' (crowded) and 'burgeoning' (growing fast) describe a busy town. 'Opulent' (rich and lavish) does not "
  "fit empty warehouses.", 30)

Q(FB, "Double blank", A,
  FB2 + "Far from ______ the dispute, the chairman's ______ remarks only made both sides more bitter.",
  ["settling, intemperate", "settling, conciliatory", "inflaming, intemperate", "ending, soothing"], 0,
  "Double blank: 'Far from X, ... only Y' means the opposite of X happened",
  "Making both sides more bitter is the opposite of settling a dispute, so blank 1 is 'settling'. Remarks that make "
  "people bitter are harsh and unrestrained: 'intemperate'.",
  ["'Far from ___' + result: more bitterness", "Blank 1: the opposite of the result → settling",
   "Blank 2: remarks that cause bitterness → intemperate"],
  "'Conciliatory' and 'soothing' remarks would not make both sides more bitter. 'Far from inflaming' contradicts a "
  "result that is itself inflaming.", 40)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Word swap", B,
  WS_STEM + "The **(A) letter** posted the **(B) clerk** in the **(C) red** box near the **(D) branch**.",
  ["A-B", "C-D", "B-D", "No swap required"], 0,
  "Word swap: check who can perform each action",
  "A letter cannot post anything. Swapping A and B gives: 'The clerk posted the letter in the red box near the "
  "branch.'",
  ["'The letter posted' is impossible", "The clerk is the one who posts", "Swap A and B"],
  "C-D gives 'the branch box near the red', which is meaningless. B-D leaves the letter as the one posting. The "
  "sentence clearly needs a swap.", 25, order=FIXED)

Q(WU, "Correct usage of a word", I,
  "In which of the following sentences is the word 'complement' used correctly?",
  ["The manager paid her a complement on her neat handwriting.",
   "The spicy chutney is a perfect complement to the plain rice.",
   "Every customer received a complement calendar at the new year.",
   "He complemented the cashier on her quick service."], 1,
  "Complement (something that completes or goes well with) vs compliment (praise; complimentary = free)",
  "A chutney that goes well with plain rice completes the meal: it is a 'complement' to it.",
  ["Praise for handwriting → 'compliment'", "Chutney that goes well with rice → 'complement': correct",
   "A free calendar → 'complimentary'", "Praised the cashier → 'complimented'"],
  "The other three are about praise or something given free, which needs 'compliment' or 'complimentary'.", 30)

Q(WU, "Correct usage of a word", I,
  "In which of the following sentences is the word 'precede' used correctly?",
  ["After the speech, the guests will precede to the dining hall.",
   "A short prayer will precede the opening of the new branch.",
   "The case cannot precede until all the documents are filed.",
   "Please precede with your complaint; I am listening."], 1,
  "Precede (come before) vs proceed (go forward, continue)",
  "'Precede' means come before. A prayer that comes before the opening 'precedes' it.",
  ["Guests going on to the hall → 'proceed'", "Prayer before the opening → 'precede': correct",
   "A case moving forward → 'proceed'", "Continue with a complaint → 'proceed'"],
  "The other three describe going forward or continuing, which needs 'proceed'.", 30)

Q(WU, "Word swap", I,
  WS_STEM + "When **(A) demand** for onions fell short of **(B) supply**, their **(C) prices** rose sharply and "
  "**(D) traders** began to hoard them.",
  ["C-D", "A-B", "A-C", "No swap required"], 1,
  "Word swap: test the sentence against the law of demand and supply",
  "Prices rise when supply falls short of demand, not the other way round. Swapping A and B gives: 'When supply of "
  "onions fell short of demand, their prices rose sharply and traders began to hoard them.'",
  ["Demand below supply → prices would fall", "Supply below demand → prices rise", "Swap A and B"],
  "C-D makes the traders rise and the prices hoard. A-C gives 'When prices for onions fell short of supply, their "
  "demand rose', which no longer explains the hoarding. The original reverses the economics, so a swap is needed.",
  35, order=FIXED)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'noisome' used correctly?",
  ["The noisome children in the next room kept the clerk awake.",
   "A noisome smell rose from the blocked drain behind the market.",
   "The festival was noisome, full of music and drums.",
   "The noisome crowd cheered loudly when the result was announced."], 1,
  "Noisome = very unpleasant or offensive, especially in smell (not 'noisy')",
  "'Noisome' has nothing to do with noise; it means foul or offensive. A smell from a blocked drain is noisome.",
  ["Children keeping someone awake → 'noisy'", "Foul smell from a drain → 'noisome': correct",
   "Festival with music and drums → 'noisy'", "Crowd cheering loudly → 'noisy'"],
  "The other three use 'noisome' as if it meant noisy, which is a common mistake.", 35)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'streamlined' as used in the sentence:\n"
  "'The new software has streamlined the loan approval process, cutting the time taken from two weeks to three "
  "days.'",
  ["made simpler and more efficient", "made longer and stricter", "made more expensive", "stopped for a time"], 0,
  "Streamline = make a process simpler and more efficient",
  "The process now takes three days instead of two weeks. Making a process quicker by removing unnecessary steps is "
  "'streamlining' it.",
  ["Clue: two weeks cut to three days", "Faster, simpler process", "'made simpler and more efficient'"],
  "'Made longer and stricter' contradicts the shorter time. Cost and stopping the process are not suggested.", 25)

Q(VO, "Word pairs", I, "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Diligent – Industrious", "Hostile – Friendly", "Scarce – Abundant", "Timid – Bold"], 0,
  "Word pairs: identify synonyms and antonyms",
  "'Diligent' and 'industrious' both mean hard-working and careful. The other pairs are opposites.",
  ["Diligent = industrious (hard-working)", "Hostile ≠ friendly", "Scarce ≠ abundant", "Timid ≠ bold"],
  "The other three pairs are opposites, not synonyms.", 25)

Q(VO, "Contextual meaning", A,
  "Choose the meaning of the word 'specious' as used in the sentence:\n"
  "'The auditor rejected the manager's specious argument that the missing cash had simply been miscounted.'",
  ["seemingly reasonable but actually false", "detailed and well supported", "angry and abusive",
   "honest but confused"], 0,
  "Specious = appearing right or reasonable on the surface but actually wrong",
  "The manager's claim sounded possible (a miscount), but the auditor saw through it and rejected it. An argument "
  "that looks plausible but is false is 'specious'.",
  ["The argument sounded possible", "The auditor rejected it as false", "'seemingly reasonable but actually false'"],
  "'Detailed and well supported' would not be rejected. 'Angry and abusive' and 'honest but confused' do not mean "
  "specious.", 30)

Q(VO, "Word pairs", A, "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Obdurate – Stubborn", "Garrulous – Taciturn", "Mendacious – Untruthful", "Penurious – Destitute"], 1,
  "Word pairs: identify synonyms and antonyms",
  "'Garrulous' means excessively talkative; 'taciturn' means saying very little. They are opposites. The other "
  "pairs are synonyms.",
  ["Obdurate = stubborn", "Garrulous (very talkative) ≠ taciturn (silent)", "Mendacious = untruthful",
   "Penurious = destitute (very poor)"],
  "The other three pairs are synonyms, not opposites.", 35)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", B,
  SY_STEM + "Rani was **delighted** to hear that she had passed the clerk's examination.",
  ["pleased", "worried", "surprised", "tired"], 0,
  "Delighted = very pleased",
  "Passing an examination is good news, and 'delighted' means very pleased.",
  ["Context: good news", "'delighted' = very happy", "Closest: 'pleased'"],
  "'Worried' and 'tired' do not describe joy. 'Surprised' describes an unexpected event, not happiness.", 20)

Q(SY, "Contextual synonym", I,
  SY_STEM + "At the press meeting, the minister **reiterated** his promise to repair the flood-damaged roads before "
  "the monsoon.",
  ["repeated", "withdrew", "doubted", "forgot"], 0,
  "Reiterate = say again, repeat",
  "A promise that is 'reiterated' is made again, usually for emphasis: it is repeated.",
  ["'re-' = again", "'reiterate' = say again", "Closest: 'repeated'"],
  "'Withdrew' and 'forgot' are the opposite of stating a promise again. 'Doubted' does not describe what the "
  "minister did with his own promise.", 25)

Q(SY, "Contextual synonym", A,
  SY_STEM + "A **perspicacious** investor, she sold her shares months before the market crashed.",
  ["shrewd", "reckless", "wealthy", "lucky"], 0,
  "Perspicacious = quick to notice and understand things; shrewd",
  "Selling months before a crash shows that she saw the danger clearly before others did. 'Perspicacious' means "
  "having sharp insight: shrewd.",
  ["Context: sold well before the crash", "She understood the risk early", "Closest: 'shrewd'"],
  "'Reckless' is the opposite. 'Wealthy' describes money, not judgement. 'Lucky' implies chance, whereas the word "
  "describes insight.", 30)

Q(SY, "Contextual synonym", A,
  SY_STEM + "The **recalcitrant** borrower ignored every notice and refused to meet the recovery officer.",
  ["uncooperative", "bankrupt", "forgetful", "apologetic"], 0,
  "Recalcitrant = stubbornly refusing to obey or cooperate",
  "Ignoring every notice and refusing to meet the officer shows a stubborn refusal to cooperate: the borrower is "
  "uncooperative.",
  ["Context: ignored notices, refused to meet", "Deliberate refusal to cooperate", "Closest: 'uncooperative'"],
  "'Bankrupt' describes finances, not attitude. 'Forgetful' suggests accident, not refusal. 'Apologetic' is the "
  "opposite of his behaviour.", 30)

Q(SY, "Contextual synonym", A,
  SY_STEM + "Thanks to a **munificent** donation from a former student, the village school built a new library.",
  ["generous", "secret", "modest", "late"], 0,
  "Munificent = very generous, especially with money",
  "A donation large enough to build a library is very generous: 'munificent'.",
  ["Context: a donation that built a library", "Large, giving gift", "Closest: 'generous'"],
  "'Modest' suggests a small gift, the opposite. 'Secret' and 'late' do not describe the size or spirit of a gift.",
  30)

Q(SY, "Contextual synonym", A,
  SY_STEM + "The **obsequious** clerk agreed with everything the visiting director said and laughed at all his "
  "jokes.",
  ["servile", "rude", "honest", "sleepy"], 0,
  "Obsequious = too eager to please or obey; servile",
  "Agreeing with everything a senior person says and laughing at all his jokes shows excessive eagerness to please: "
  "the clerk is servile.",
  ["Context: agrees with everything, laughs at every joke", "Excessive eagerness to please", "Closest: 'servile'"],
  "'Rude' is the opposite. 'Honest' and 'sleepy' do not describe flattering a superior.", 30)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The water in the village pond is so **shallow** in summer that children can walk across it.",
  ["deep", "muddy", "cold", "clean"], 0,
  "Shallow = not deep; antonym: deep",
  "Water that children can walk across is not deep. The opposite of 'shallow' is 'deep'.",
  ["'shallow' = of little depth", "Opposite: 'deep'"],
  "'Muddy', 'cold' and 'clean' describe the water's condition or temperature, not its depth.", 20)

Q(AN, "Contextual antonym", B,
  AN_STEM + "Snow is **rare** in this coastal town, so the children have never built a snowman.",
  ["common", "heavy", "cold", "late"], 0,
  "Rare = not happening often; antonym: common",
  "Something that seldom happens is 'rare'; the opposite is 'common' (happening often).",
  ["'rare' = seldom found or seen", "Opposite: 'common'"],
  "'Heavy', 'cold' and 'late' describe amount, temperature and timing, not how often snow falls.", 20)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The bank has put up a **conspicuous** sign at the gate so that no one can miss the new timings.",
  ["unobtrusive", "prominent", "striking", "official"], 0,
  "Conspicuous = easily seen, attracting notice; antonym: unobtrusive",
  "A sign that 'no one can miss' is conspicuous. The opposite is 'unobtrusive' (not easily noticed).",
  ["'conspicuous' = clearly visible", "Opposite: not noticeable → 'unobtrusive'"],
  "'Prominent' and 'striking' are close in meaning to 'conspicuous'. 'Official' describes who put the sign up.", 25)

Q(AN, "Contextual antonym", A,
  AN_STEM + "The **intrepid** reporter travelled alone into the flood zone to file her story.",
  ["timid", "fearless", "careless", "famous"], 0,
  "Intrepid = fearless, adventurous; antonym: timid",
  "Going alone into a flood zone shows courage. 'Intrepid' means fearless; its opposite is 'timid' (easily "
  "frightened).",
  ["'intrepid' = fearless", "Opposite: easily frightened → 'timid'"],
  "'Fearless' is a synonym. 'Careless' and 'famous' do not describe the lack of courage.", 25)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"

Q(ID, "Meaning of idiom", B,
  "Choose the meaning of the idiom 'to see eye to eye'.",
  ["to agree fully with someone", "to stare at someone angrily", "to meet someone face to face",
   "to have one's eyesight tested"], 0,
  "Idiom: see eye to eye = agree, have the same opinion",
  "People who 'see eye to eye' share the same view. For example: 'The two partners rarely see eye to eye on how to "
  "spend the profits.'",
  ["Literal: looking at each other", "Idiomatic: sharing the same view", "'to agree fully with someone'"],
  "Staring angrily, meeting face to face and an eye test read the words literally; none means agreeing.", 20)

Q(ID, "Idiom in context", B,
  "Choose the meaning of the idiom in bold.\n"
  "The contractor finished painting the new branch **at the eleventh hour**, just before the opening ceremony "
  "began.",
  ["at the last possible moment", "at eleven o'clock at night", "after a delay of eleven days",
   "much earlier than planned"], 0,
  "Idiom: at the eleventh hour = at the latest possible time",
  "Finishing 'just before the opening ceremony began' means finishing at the very last moment.",
  ["Clue: just before the ceremony", "Very late, but still in time", "'at the last possible moment'"],
  "'Eleven o'clock' and 'eleven days' read the idiom literally. 'Much earlier than planned' contradicts 'just "
  "before'.", 20)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "Searching the old record room for the missing file turned out to be **a wild goose chase**; it had been sent to "
  "the head office years earlier.",
  ["a pointless search for something that is not there", "an exciting race against time",
   "a careful and successful inspection", "a pleasant trip away from work"], 0,
  "Idiom: a wild goose chase = a hopeless search or pursuit",
  "The file was never in the record room, so searching there could not succeed. Such a hopeless search is a wild "
  "goose chase.",
  ["Clue: the file had been sent elsewhere", "The search could not succeed", "'a pointless search'"],
  "The search was neither exciting, successful nor pleasant; the sentence stresses that it was useless.", 25)

Q(ID, "Meaning of idiom", I,
  "Choose the meaning of the idiom 'to add fuel to the fire'.",
  ["to make a bad situation worse", "to give workers fresh energy", "to settle a quarrel quickly",
   "to waste money on unnecessary things"], 0,
  "Idiom: add fuel to the fire = make an angry or difficult situation worse",
  "Fuel makes a fire burn more fiercely; doing something that inflames an already tense situation 'adds fuel to the "
  "fire'. For example: 'His rude reply only added fuel to the fire.'",
  ["Fuel makes a fire stronger", "Idiomatic: makes trouble worse", "'to make a bad situation worse'"],
  "Giving energy, settling a quarrel and wasting money are not what the idiom means; settling a quarrel is nearly "
  "the opposite.", 25)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "The two largest shareholders took **the lion's share** of the profits, leaving little for the rest.",
  ["the largest part", "a fair part", "a hidden part", "the smallest part"], 0,
  "Idiom: the lion's share = the largest part of something",
  "'Leaving little for the rest' shows that the two shareholders took most of the profits: the lion's share.",
  ["Clue: little left for the others", "They took most of it", "'the largest part'"],
  "'A fair part' and 'the smallest part' contradict 'leaving little for the rest'. Nothing suggests the share was "
  "hidden.", 20)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", I, OW_STEM + "A person authorised to act or vote on behalf of another",
  ["proxy", "mentor", "rival", "heir"], 0,
  "One-word substitution: roles and representatives",
  "A 'proxy' is a person given authority to act or vote for someone else, as at a company meeting.",
  ["Key idea: acts or votes for another person", "Word: proxy"],
  "A 'mentor' is an experienced adviser, a 'rival' a competitor and an 'heir' a person who inherits property.", 25)

Q(OW, "Single word for a phrase", A, OW_STEM + "A person who pretends to be ill in order to avoid work or duty",
  ["malingerer", "hypochondriac", "invalid", "sluggard"], 0,
  "One-word substitution: pretending versus believing",
  "A 'malingerer' pretends to be ill, or exaggerates an illness, to escape work or duty.",
  ["Key idea: pretends to be ill", "Purpose: to avoid work", "Word: malingerer"],
  "A 'hypochondriac' truly believes he is ill without cause; he is not pretending. An 'invalid' is a person who "
  "really is ill or disabled. A 'sluggard' is lazy but does not pretend to be ill.", 30)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", B, AP_STEM + "The children did not break the window.",
  ["The window was not broken by the children.",
   "The window is not broken by the children.",
   "The window was not break by the children.",
   "The window had not been broken by the children."], 0,
  "Simple past negative active (did not + verb) → was/were not + past participle",
  "The object 'the window' becomes the subject. 'Did not break' (simple past) becomes 'was not broken'.",
  ["New subject: the window (singular)", "Simple past passive negative: was not + broken", "Agent: by the children"],
  "'Is not broken' changes the tense to the present. 'Was not break' uses the base form instead of the participle. "
  "'Had not been broken' is past perfect.", 25)

Q(AP, "Voice conversion", I, AP_STEM + "The guard made the visitors wait outside the strongroom.",
  ["The visitors were made to wait outside the strongroom by the guard.",
   "The visitors were made wait outside the strongroom by the guard.",
   "The visitors had been made to wait outside the strongroom by the guard.",
   "The visitors were making to wait outside the strongroom by the guard."], 0,
  "'Make + object + bare infinitive' in the active becomes 'be made + to-infinitive' in the passive",
  "In the active, 'make' takes a bare infinitive (made the visitors wait). In the passive, 'to' comes back: 'The "
  "visitors were made to wait outside the strongroom by the guard.'",
  ["New subject: the visitors", "Simple past passive: were made", "'to' returns in the passive: made to wait"],
  "'Were made wait' leaves out the 'to' that the passive needs. 'Had been made' changes the tense. 'Were making to "
  "wait' is not a passive form.", 30)

Q(AP, "Voice conversion", A, AP_STEM + "I remember my father taking me to the bank for the first time.",
  ["I remember being taken to the bank for the first time by my father.",
   "I remember having taken to the bank for the first time by my father.",
   "I am remembered being taken to the bank for the first time by my father.",
   "I remember my father being taken to the bank for the first time."], 0,
  "Passive gerund: being + past participle",
  "The gerund clause 'my father taking me' is made passive: 'me' becomes the understood subject and the gerund "
  "becomes 'being taken': 'I remember being taken to the bank for the first time by my father.' The main verb "
  "'remember' stays active.",
  ["Main clause 'I remember' stays the same", "Gerund 'taking me' → passive gerund 'being taken'",
   "Agent: by my father"],
  "'Having taken' is an active perfect gerund. 'I am remembered' wrongly makes the main verb passive. 'My father "
  "being taken' reverses who took whom.", 40)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", B, DS_STEM + "Ravi said, \"I am going to the market.\"",
  ["Ravi said that he was going to the market.",
   "Ravi said that I was going to the market.",
   "Ravi told that he was going to the market.",
   "Ravi said that he had been going to the market."], 0,
  "Past reporting verb: present continuous → past continuous; 'I' → 'he'",
  "With 'said', 'am going' becomes 'was going', and 'I' becomes 'he': 'Ravi said that he was going to the market.'",
  ["Reporting verb: 'said' (past)", "'am going' → 'was going'", "'I' → 'he'"],
  "'Said that I' keeps the first person. 'Told that' needs an object ('told me that'). 'Had been going' backshifts "
  "too far.", 25)

Q(DS, "Narration change", I, DS_STEM + "The manager said to the staff, \"Good morning!\"",
  ["The manager wished the staff good morning.",
   "The manager said to the staff that good morning.",
   "The manager told the staff that it was a good morning.",
   "The manager exclaimed to the staff that good morning."], 0,
  "Greetings are reported with a suitable verb such as 'wish' or 'greet', not with 'that'",
  "A greeting is not a statement, so it cannot follow 'that'. It is reported as 'The manager wished the staff good "
  "morning.'",
  ["'Good morning!' is a greeting", "Reporting verb for greetings: wished / greeted", "'wished the staff good "
   "morning'"],
  "'Said ... that good morning' and 'exclaimed ... that good morning' put a greeting in a 'that' clause with no verb. "
  "'That it was a good morning' turns the greeting into a remark about the weather.", 30)

Q(DS, "Narration change", A,
  DS_STEM + "She said, \"If I had known about the strike, I would have taken a taxi.\"",
  ["She said that if she had known about the strike, she would have taken a taxi.",
   "She said that if she had had known about the strike, she would have had taken a taxi.",
   "She said that if she knew about the strike, she would take a taxi.",
   "She said that if she had known about the strike, she will have taken a taxi."], 0,
  "Past perfect and 'would have + past participle' (third conditional) do not change in reported speech",
  "The past perfect cannot be shifted further back, and 'would have taken' stays the same. Only the pronoun "
  "changes: 'She said that if she had known about the strike, she would have taken a taxi.'",
  ["Third conditional: had known / would have taken", "No further backshift is possible",
   "'I' → 'she' only"],
  "'Had had known' and 'would have had taken' are not English verb forms. 'Knew ... would take' changes the meaning "
  "to a present unreal condition. 'Will have taken' wrongly changes 'would' to 'will'.", 40)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", B, SV_STEM + "Here ______ the files you asked for.",
  ["are", "is", "was", "has"], 0,
  "After 'Here' or 'There' at the start, the verb agrees with the noun subject that follows it",
  "The real subject is 'the files', which is plural, so the verb is plural: 'Here are the files you asked for.'",
  ["'Here' is not the subject", "Subject after the verb: 'the files' (plural)", "Plural verb: 'are'"],
  "'Is', 'was' and 'has' are singular and do not agree with 'the files'; 'has' also gives no meaning here.", 20)

Q(SV, "Agreement rules", I,
  SV_STEM + "A series of thefts from the lockers ______ forced the bank to install new cameras.",
  ["has", "have", "were", "are"], 0,
  "'A series of + plural noun' takes a singular verb, because the head noun is 'series'",
  "The head of the subject is 'a series' (one sequence), so the verb is singular: 'A series of thefts ... has forced "
  "the bank to install new cameras.'",
  ["Head noun: 'a series' (singular)", "'of thefts' does not change the number", "Present perfect, singular: 'has'"],
  "'Have' agrees wrongly with 'thefts'. 'Were' and 'are' cannot be followed by 'forced' to give an active verb and "
  "are plural.", 30)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Sequence of tenses", I, TE_STEM + "This cake ______ wonderful; may I have the recipe?",
  ["tastes", "is tasting", "has been tasting", "was tasting"], 0,
  "State verbs of the senses (taste, smell, look, sound) used with an adjective take simple tenses, not continuous",
  "'Taste' here describes a quality of the cake (a state), followed by the adjective 'wonderful', so the simple "
  "present is used: 'This cake tastes wonderful.'",
  ["'taste' + adjective = a state, not an action", "State verbs avoid continuous forms", "Simple present: 'tastes'"],
  "'Is tasting' and 'has been tasting' wrongly use continuous forms for a state. 'Was tasting' is past and also "
  "continuous, which clashes with 'may I have the recipe?' now.", 25)

Q(TE, "Sequence of tenses", A,
  TE_STEM + "I ______ leave the office when the manager called me back for an urgent meeting.",
  ["was about to", "am about to", "will be about to", "have been about to"], 0,
  "'Was about to + verb ... when + past simple' = an action on the point of happening when something interrupted it",
  "The interruption ('the manager called me back') is in the past, so the planned action just before it is "
  "expressed by 'was about to': 'I was about to leave the office when the manager called me back ...'.",
  ["Interrupting event: past simple 'called'", "Action on the point of happening at that moment",
   "'was about to leave'"],
  "'Am about to' and 'will be about to' are present and future and clash with 'called'. 'Have been about to' is not "
  "used for a single past moment.", 30)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", I,
  AR_STEM + "______ Taj Mahal was built by ______ Mughal emperor Shah Jahan.",
  ["The, the", "A, the", "No article, a", "The, a"], 0,
  "'The' with the names of certain famous buildings, and with a title + name when the title identifies the person",
  "'The Taj Mahal' is the fixed name of the monument. 'The Mughal emperor Shah Jahan' refers to one particular, "
  "identified emperor, so it also takes 'the'.",
  ["Monument name: the Taj Mahal", "Identified person with a descriptive title: the Mughal emperor",
   "'The, the'"],
  "'A Taj Mahal' would suggest one of many. 'Taj Mahal' without 'the' drops the article that is part of the name. "
  "'A Mughal emperor Shah Jahan' uses 'a' for a person who is already named and identified.", 30)

Q(AR, "Definite and indefinite", A,
  AR_STEM + "Known for his plays and poems, Ravi is often called ______ Kalidasa of our district.",
  ["the", "a", "an", "no article"], 0,
  "A proper noun used as a common noun (one who is like a famous person) takes 'the' when a phrase identifies the "
  "one meant",
  "Ravi is being compared with Kalidasa, the great poet. 'Of our district' makes the reference unique: the one person "
  "in the district who is like Kalidasa. So it is 'the Kalidasa of our district'.",
  ["Kalidasa used as a common noun: a great poet like Kalidasa", "'of our district' identifies the unique one",
   "Unique, identified → 'the'"],
  "'A Kalidasa of our district' clashes with the identifying phrase, which marks one particular person. 'An' does not "
  "fit the consonant sound /k/. With no article, the sentence would call Ravi the actual poet Kalidasa.", 35)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", B, PP_STEM + "The little boy is afraid ______ the dark.",
  ["of", "from", "with", "at"], 0,
  "Fixed preposition: 'afraid of'",
  "The adjective 'afraid' takes 'of': 'The little boy is afraid of the dark.'",
  ["Adjective: afraid", "Fixed pairing: afraid of", "'of'"],
  "'Afraid from', 'afraid with' and 'afraid at' are not used.", 20)

Q(PP, "Fixed prepositions", B, PP_STEM + "The branch is closed ______ Sundays and public holidays.",
  ["on", "in", "at", "by"], 0,
  "Prepositions of time: 'on' with days and dates",
  "Days of the week take 'on': 'The branch is closed on Sundays and public holidays.'",
  ["Time word: Sundays (days)", "Days → 'on'", "'on'"],
  "'In' is used with months, years and parts of the day, 'at' with clock times, and 'by' means no later than. None "
  "is used with days in this sense.", 20)

Q(PP, "Fixed prepositions", A,
  PP_STEM + "The management finally acceded ______ the union's demand for a five-day week.",
  ["to", "with", "for", "on"], 0,
  "Fixed preposition: accede to (a request or demand) = agree to it",
  "To accept a demand after resisting it is to 'accede to' it: 'The management finally acceded to the union's "
  "demand ...'.",
  ["Verb: accede (agree)", "Fixed pairing: accede to", "'to'"],
  "'Accede with', 'accede for' and 'accede on' are not used.", 25)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"
CN_STEM = "Choose the connector that best fills the blank.\n"

Q(CN, "Sentence connectors", B,
  CN_STEM + "He was very tired, ______ he kept working until the last customer had left.",
  ["yet", "so", "because", "or"], 0,
  "'Yet' = but still; it joins two facts that contrast",
  "Being tired would make one stop, but he kept working. The contrast is shown by 'yet'.",
  ["Clause 1: very tired", "Clause 2: kept working (unexpected)", "Contrast → 'yet'"],
  "'So' would make tiredness the reason he kept working. 'Because' makes keeping on working the reason for being "
  "tired, which reverses the logic. 'Or' offers an alternative.", 20)

Q(CN, "Sentence connectors", B,
  CN_STEM + "______ he was ill, he could not attend the meeting.",
  ["Since", "Although", "Unless", "Until"], 0,
  "'Since' (= because) introduces a reason",
  "His illness is the reason he could not attend. 'Since' introduces a reason: 'Since he was ill, he could not "
  "attend the meeting.'",
  ["Clause 1: he was ill (cause)", "Clause 2: could not attend (result)", "Reason → 'Since'"],
  "'Although' signals a contrast that is not there. 'Unless' makes illness a condition for attending. 'Until' is "
  "about time and does not fit 'could not attend'.", 20)

Q(CN, "Sentence connectors", I,
  CN_STEM + "The rural branches cut their staff costs last year; ______, the urban branches brought down their rent "
  "bills.",
  ["similarly", "nevertheless", "otherwise", "consequently"], 0,
  "'Similarly' links two actions of the same kind",
  "Both groups of branches reduced a cost: one cut staff costs, the other rent. Parallel actions are linked by "
  "'similarly'.",
  ["Action 1: rural branches cut costs", "Action 2: urban branches cut costs too", "Same kind → 'similarly'"],
  "'Nevertheless' signals a contrast that is not there. 'Otherwise' means 'if not'. 'Consequently' would make the "
  "urban rent cuts a result of the rural staff cuts, which the sentence does not suggest.", 25)

Q(CN, "Starters and linkers", I,
  "Combine the two sentences into one without changing the meaning, and choose the correct combined sentence.\n"
  "He is very rich. He is not happy.",
  ["For all his wealth, he is not happy.", "Because of his wealth, he is not happy.",
   "Owing to his wealth, he is not happy.", "In addition to his wealth, he is not happy."], 0,
  "'For all' (= in spite of) introduces a concession",
  "The two sentences contrast: he is rich, but still not happy. 'For all his wealth' means 'in spite of his wealth', "
  "keeping the contrast.",
  ["Relation: rich, yet not happy (contrast)", "Concessive phrase needed", "'For all his wealth, ...'"],
  "'Because of' and 'Owing to' make his wealth the cause of his unhappiness, which changes the meaning. 'In addition "
  "to' adds rather than contrasts.", 30)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

# questions whose key was also recomputed by this script
RECOMPUTED = {(P3, 1), (P5, 1)}
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


for seed in range(8008, 12000):
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

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_008_plan.json").read_text(encoding="utf-8"))
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

# no reused stem or passage title across the earlier English files (BATCH_000 to BATCH_007)
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
# BATCH_007 for this batch.
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

# earlier-key / bold-word repeat scan: no word, idiom or phrase keyed or tested in BATCH_000 to BATCH_007 is keyed or
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
    "batch_id": "BATCH_008",
    "created_at": TODAY,
    "notes": "BATCH_008 English Language part: 149 original questions (BANK_ENG_001054 to BANK_ENG_001202). Five "
             "reading passages (27 questions) and four cloze passages (23 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 to BATCH_007; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules, words and idioms not tested in earlier batches "
             "(checked by the builder against all earlier keyed and bold words). Each answer was set by the author "
             "and re-solved in a separate blind pass by fresh checkers without the key; the chit-fund pool (RC 3) "
             "and the trader's cash need (RC 5) are also recomputed by the builder. Pending human review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_008_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))}, seed {seed})")
