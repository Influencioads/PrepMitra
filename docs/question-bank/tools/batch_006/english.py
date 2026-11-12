"""Writes batches/parts/BATCH_006_ENG.json: the 150 English Language questions of BATCH_006.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000 to BATCH_005, and the grammar rules, idioms and words tested are ones not tested in those batches (where
a grammar area was already covered, it is tested here through a different rule or a context-based item). Run from
anywhere:

    python docs/question-bank/tools/batch_006/english.py

Structural checks (quota per topic and difficulty, subtopics, ID range, passage length, set sizes, option count, cloze
blank numbering, 'No error' / 'No replacement' placement, para-jumble option validity, RC option-length spread,
repeated stems, passage titles and passage themes against all earlier English files, answer-key balance) and the one
computable answer (the capture-recapture estimate in RC 4) are asserted before anything is written. Option letters are
never named in solutions (except the fixed parts A/B/C of Error Detection), so option order can be changed safely.
"""

import json
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
FIRST_ID = 754
FIRST_STIM = 6001
EARLIER = ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json", "parts/BATCH_002_ENG.json",
           "parts/BATCH_003_ENG.json", "parts/BATCH_004_ENG.json", "parts/BATCH_005_ENG.json")

QS = []


def Q(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, why, seconds,
      stim=None, pos=None, shortcut=None):
    assert len(options) == 4 and answer in LETTERS, text
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
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True,
                         "review_status": "Pending Human Review",
                         "verified_by": ["ai:author-solve", "ai:independent-check"], "verified_at": TODAY},
    }
    QS.append(out)


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

# ---------------------------------------------------------------- RC 1 (Basic, 4)
P1 = stim("Warning before the strike", (
    "Lightning kills more people in India each year than most other natural hazards, yet it rarely makes headlines. "
    "Unlike a cyclone or a flood, which can be tracked for days, a lightning strike is over in a fraction of a "
    "second, and its victims are usually scattered: a farmer in a field, a herder on a hillside, a group sheltering "
    "under a tree.\n\n"
    "Most of these deaths happen in rural areas during the pre-monsoon and monsoon months, when thunderstorms build "
    "up quickly in the afternoon. People working outdoors are the most exposed. Many of them believe that a tall tree "
    "offers safety from the rain, but a lone tree is in fact one of the most dangerous places to stand, because "
    "lightning tends to strike the highest point in an open area.\n\n"
    "In recent years, weather scientists have set up networks of sensors that detect the electrical activity of a "
    "storm as it forms. This allows them to issue warnings for a particular district from about thirty minutes to a "
    "few hours in advance. Several states now send these alerts as text messages, and free mobile apps show whether a "
    "storm is approaching the user's location.\n\n"
    "A warning, however, is useful only if people know what to do with it. Officials therefore combine the alerts "
    "with simple advice. People caught outdoors should move into a solid building or a closed vehicle. If no shelter "
    "is near, they should keep away from trees, poles and water, and crouch low with their feet together rather than "
    "lie flat on the ground. They should also wait for about half an hour after the last thunder before going out "
    "again.\n\n"
    "Experts say that awareness campaigns in schools and village meetings have already helped to reduce deaths in "
    "some districts. Their aim is modest but important: to turn a few minutes of warning into a few minutes of safe "
    "action."))

Q(RC, "Factual", B,
  "According to the passage, why does lightning rarely make headlines?",
  ["It kills far fewer people than cyclones and floods do.",
   "Each strike is over in an instant and its victims are scattered.",
   "Most strikes happen at night when nobody is reporting.",
   "Weather offices do not record deaths caused by lightning."], "B",
  "Locating a stated reason",
  "Paragraph 1 contrasts lightning with cyclones and floods, which 'can be tracked for days': a strike 'is over in a "
  "fraction of a second, and its victims are usually scattered'.",
  ["Find 'rarely makes headlines' in paragraph 1", "The next sentence gives the reason",
   "Over in a fraction of a second + scattered victims"],
  "'Kills far fewer people' contradicts the first sentence, which says lightning kills more than most other hazards. "
  "The passage says storms build up in the afternoon, not at night. Nothing is said about weather offices failing to "
  "record deaths.", 40, P1, 1)

Q(RC, "Factual", B,
  "Why, according to the passage, is a lone tree a dangerous place to stand during a thunderstorm?",
  ["Its branches may break and fall in the strong wind.",
   "Rainwater collects around its roots and conducts current.",
   "Lightning tends to strike the highest point in open ground.",
   "Animals and insects gather under it to shelter from rain."], "C",
  "Locating a stated reason",
  "Paragraph 2: a lone tree is one of the most dangerous places to stand 'because lightning tends to strike the "
  "highest point in an open area'.",
  ["Find 'a lone tree' in paragraph 2", "Reason after 'because'", "Highest point in an open area"],
  "Falling branches, water around the roots and sheltering animals are never mentioned; they are guesses from "
  "general knowledge, not reasons given in the passage.", 40, P1, 2)

Q(RC, "Factual", B,
  "Which of the following is NOT part of the advice given to people caught outdoors in a thunderstorm?",
  ["Lie flat on the ground until the storm passes.",
   "Move into a solid building or a closed vehicle.",
   "Keep away from trees, poles and water.",
   "Wait about half an hour after the last thunder."], "A",
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 4 advises shelter in a solid building or closed vehicle, keeping away from trees, poles and water, "
  "crouching low with feet together 'rather than lie flat on the ground', and waiting half an hour after the last "
  "thunder. Lying flat is the one thing it tells people not to do.",
  ["Building or closed vehicle: stated", "Away from trees, poles and water: stated",
   "Half an hour after the last thunder: stated", "Lying flat: advised against"],
  "Shelter in a building or vehicle, keeping away from trees and water, and waiting half an hour are all stated in "
  "paragraph 4, so none of them can be the answer.", 45, P1, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'exposed' as used in the passage ('People working "
  "outdoors are the most exposed')?",
  ["revealed", "experienced", "unprotected", "displayed"], "C",
  "Vocabulary in context: exposed (to a danger) = left without protection from it",
  "People in the open fields have nothing between them and the storm. 'Exposed' here means unprotected from the "
  "danger of lightning.",
  ["Context: people outdoors during thunderstorms", "They lack shelter from the danger", "'unprotected'"],
  "'Revealed' and 'displayed' are the senses of 'exposed' used for secrets or objects put on show. 'Experienced' "
  "has nothing to do with lacking protection.", 30, P1, 4)

# ---------------------------------------------------------------- RC 2 (Basic, 4)
P2 = stim("Money you can feel", (
    "For most people, telling one currency note from another takes only a glance. For the millions of Indians who "
    "are blind or have poor eyesight, it can be a daily struggle, and a mistake can be costly: a shopkeeper might hand "
    "back a ten-rupee note in place of a hundred, and the customer would never know.\n\n"
    "Banknote designers try to help in several ways. Notes of different values are made in different sizes, so that "
    "a person can compare their length and width with the fingers. Many notes also carry marks printed in raised "
    "ink, such as small lines or shapes near the edge, which can be felt by touch. The large numerals and strong "
    "colours used on new notes are meant to help people whose sight is weak but not entirely lost.\n\n"
    "These features do not always work as intended. When a new series of notes is introduced, older notes of the "
    "same value may stay in use for years, so people have to learn two sets of sizes. Raised printing tends to wear "
    "away as a note passes from hand to hand, and a note that has been folded, crumpled or soaked may be hard to read "
    "by touch at all. Some notes of neighbouring values are also so close in size that the difference is difficult "
    "to feel.\n\n"
    "Technology now offers another aid. Mobile phone apps can identify a note when it is held in front of the camera "
    "and announce its value aloud, and some work even without an internet connection. Users say the apps are "
    "helpful, but they also point out that pulling out a phone for every transaction is slow, and not everyone owns "
    "a smartphone.\n\n"
    "Organisations that work with the visually impaired argue that the best solution is a mix: notes designed with "
    "touch in mind from the very start, coins that are easy to tell apart, and apps for those who want them. Money, "
    "they say, should be usable by everyone who earns it."))

Q(RC, "Factual", B,
  "How, according to the passage, do notes of different sizes help a person who cannot see them?",
  ["Shopkeepers are required to count them out aloud.",
   "Larger notes make a louder sound when they are shaken.",
   "Smaller notes are printed in brighter, stronger colours.",
   "The person can compare their length and width by touch."], "D",
  "Locating a stated purpose",
  "Paragraph 2: notes of different values are made in different sizes 'so that a person can compare their length "
  "and width with the fingers'.",
  ["Find 'different sizes' in paragraph 2", "Purpose after 'so that'", "Compare length and width by touch"],
  "Sound and a duty on shopkeepers are never mentioned. Strong colours are mentioned, but for people with weak "
  "sight, and they are not linked to the size of the note.", 40, P2, 1)

Q(RC, "Factual", B,
  "Which of the following is NOT given in the passage as a reason why the touch features of notes do not always "
  "work?",
  ["Old and new notes of one value may circulate together.",
   "Raised printing wears away as notes change hands.",
   "Some neighbouring values are very close in size.",
   "Raised marks are printed only on high-value notes."], "D",
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 3 gives three problems: old and new series in use together, raised printing that wears away (or notes "
  "that are crumpled or soaked), and neighbouring values that are close in size. It never says raised marks appear "
  "only on high-value notes.",
  ["Two series in use: stated", "Raised printing wears away: stated", "Close sizes: stated",
   "Marks only on high-value notes: not in the passage"],
  "The two series in circulation, worn raised printing and close sizes are all stated in paragraph 3, so none of "
  "them can be the answer.", 45, P2, 2)

Q(RC, "Factual", B,
  "What drawback of note-reading mobile apps do users point out?",
  ["They work only when there is an internet connection.",
   "They often announce the wrong value for older notes.",
   "Using a phone for every payment is slow, and not all own one.",
   "They are sold at a price that most users cannot afford."], "C",
  "Locating a stated drawback",
  "Paragraph 4: users 'point out that pulling out a phone for every transaction is slow, and not everyone owns a "
  "smartphone'.",
  ["Find 'point out' in paragraph 4", "Two drawbacks: slow, and not everyone owns a smartphone",
   "Match the option that states both"],
  "The passage says some apps work 'even without an internet connection', which rules out the first option. Wrong "
  "values and a high price are never mentioned.", 40, P2, 3)

Q(RC, "Tone and title", B,
  "Which of the following is the most suitable title for the passage?",
  ["Making Money Usable for All", "How Banks Catch Fake Notes", "The History of Indian Coins",
   "Why Cash Is Disappearing"], "A",
  "Title: the idea that runs through every paragraph",
  "Every paragraph deals with how people who cannot see well identify money: the problem, design features, their "
  "limits, apps and a mixed solution. The last line says money 'should be usable by everyone who earns it'.",
  ["Para 1: the problem for blind people", "Paras 2–4: features, their limits, apps",
   "Para 5: money usable by everyone"],
  "Fake notes and the decline of cash are not discussed. Coins are mentioned only once, in passing, and the passage "
  "has no history.", 35, P2, 4)

# ---------------------------------------------------------------- RC 3 (Basic 3 + Intermediate 2)
P3 = stim("A number with a past", (
    "When a person stops using a mobile number, it does not disappear. After a period of inactivity, telecom "
    "operators may deactivate the connection and, some months later, issue the same number to a new customer. "
    "Numbers are a limited resource, and recycling them is a normal practice around the world. In an age of digital "
    "banking, however, it has created an unexpected risk.\n\n"
    "Most bank accounts today are linked to a mobile number. The bank sends one-time passwords, transaction alerts "
    "and balance messages to that number, and many apps use it to identify the customer. If the old owner of a "
    "number forgets to update the bank, those messages may now reach a stranger. In the worst cases, a person who "
    "receives someone else's one-time passwords and has a few other details can reset passwords or approve "
    "payments.\n\n"
    "The problem usually arises from neglect rather than crime. People change numbers when they move to a new city, "
    "switch operators or let a second SIM card lapse, and updating every bank, insurer and government service is "
    "tedious. Elderly customers and those who rarely use their accounts are especially likely to overlook it.\n\n"
    "Banks and regulators have responded in several ways. Some banks now check whether a registered number has "
    "recently changed hands and ask the customer to confirm it before sending sensitive messages. Customers are "
    "urged to update their contact details whenever they give up a number, and to read alerts carefully, since an "
    "unfamiliar message may be the first sign that their details are out of date.\n\n"
    "The episode is a reminder that security depends not only on strong technology but also on the ordinary links "
    "between a person and their accounts. A mobile number feels permanent to the person who uses it. To the network, "
    "it is merely on loan."))

Q(RC, "Factual", B,
  "According to the passage, what may telecom operators do with a number that has been inactive for some time?",
  ["Sell it back to the bank to which it was linked",
   "Deactivate it and later issue it to a new customer",
   "Keep it blocked permanently for security reasons",
   "Transfer it automatically to the owner's new phone"], "B",
  "Locating a stated fact",
  "Paragraph 1: 'telecom operators may deactivate the connection and, some months later, issue the same number to a "
  "new customer'.",
  ["Find 'After a period of inactivity' in paragraph 1", "Deactivate, then reissue to someone new",
   "Match the option"],
  "Selling numbers to banks and automatic transfer are never mentioned. Permanent blocking contradicts the statement "
  "that recycling numbers is normal practice.", 40, P3, 1)

Q(RC, "Factual", B,
  "Which customers, according to the passage, are especially likely to forget to update their mobile number with "
  "the bank?",
  ["Young people who change phones every year",
   "Customers who bank only at a branch counter",
   "Elderly people and those who rarely use their accounts",
   "Business owners who hold accounts in many banks"], "C",
  "Locating a stated fact",
  "Paragraph 3: 'Elderly customers and those who rarely use their accounts are especially likely to overlook it.'",
  ["Find 'especially likely' in paragraph 3", "Two groups: elderly customers, rare users", "Match the option"],
  "Young people, branch-only customers and business owners are not singled out anywhere in the passage.",
  40, P3, 2)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'tedious' as used in the passage ('updating every bank, "
  "insurer and government service is tedious')?",
  ["dangerous", "costly", "tiresome", "illegal"], "C",
  "Vocabulary in context: tedious = long, dull and tiring",
  "Contacting every bank, insurer and government office one by one is a dull, drawn-out chore. 'Tedious' means "
  "tiresome.",
  ["Context: updating many organisations one by one", "A dull, time-consuming chore", "'tiresome'"],
  "Nothing in the sentence suggests that updating details is dangerous, expensive or against the law; the point is "
  "that it is a boring chore people put off.", 30, P3, 3)

Q(RC, "Inference", I,
  "What does the author mean by saying that the problem 'usually arises from neglect rather than crime'?",
  ["Most cases begin with people forgetting to update details, not with a fraud plan.",
   "Banks neglect their duty to customers far more often than criminals do.",
   "Fraud with recycled numbers is rare because the police act quickly on it.",
   "Customers who lose money this way are usually to blame and get no refund."], "A",
  "Inference: what a contrast ('neglect rather than crime') says about causes",
  "The sentences that follow explain the 'neglect': people change numbers and do not update every bank because it is "
  "tedious. So the usual starting point is forgetfulness by the old owner, not a deliberate scheme by criminals.",
  ["The next sentences describe people failing to update details", "'neglect' = forgetting to update",
   "Most cases start with forgetfulness, not a fraud plan"],
  "The passage blames customers' forgetfulness, not banks, for the neglect. Police action is never mentioned. "
  "Blame and refunds are not discussed; the point is about how the problem starts.", 50, P3, 4)

Q(RC, "Tone and title", I,
  "What does the author suggest by the closing line, 'To the network, it is merely on loan'?",
  ["Customers must pay a monthly fee to keep using their numbers.",
   "A number belongs to the network and may pass to someone else.",
   "Banks lend money only to customers with a registered number.",
   "Telecom operators may withdraw a number if a loan is unpaid."], "B",
  "Inference: the meaning of a closing metaphor",
  "Something on loan is used for a while and then returned. The author contrasts how permanent a number feels to its "
  "user with the network's view: the number is only borrowed and can be reissued to a new customer, as paragraph 1 "
  "describes.",
  ["'feels permanent to the person' vs 'on loan' to the network", "On loan = borrowed for a time, then reused",
   "Links back to recycling in paragraph 1"],
  "The other options take 'loan' literally as money or fees, which the passage never connects with mobile numbers.",
  45, P3, 5)

# ---------------------------------------------------------------- RC 4 (Intermediate, 6)
P4 = stim("Counting what hides", (
    "Counting tigers sounds simple until one tries it. The animals are shy, mostly active at night and spread across "
    "thick forest, so a direct head-count is impossible. For decades, Indian forest departments relied instead on "
    "pugmarks, the footprints that tigers leave on soft ground. Staff would trace the prints and try to tell "
    "individuals apart by their shape and size.\n\n"
    "The method had obvious weaknesses. Prints change with the softness of the soil and the speed of the animal, and "
    "experts often disagreed over whether two prints came from one tiger or two. Critics argued that the counts "
    "tended to rise whenever officials were under pressure to show success.\n\n"
    "Today the main tool is the camera trap: a weatherproof camera fixed to a tree, which takes a picture whenever an "
    "animal passes in front of it. Because the pattern of stripes on every tiger is unique, like a human fingerprint, "
    "a computer can match photographs and recognise individuals. Thousands of cameras are placed across a reserve for "
    "several weeks, and the results are analysed using a method known as capture-recapture.\n\n"
    "The logic of capture-recapture is easiest to see with a simple example. Suppose cameras photograph forty "
    "different tigers in the first fortnight, and in the second fortnight they photograph forty again, of which "
    "twenty were already seen. Since half of the second sample had been 'captured' earlier, statisticians reason that "
    "the first sample probably represented about half the population, which is therefore around eighty. Real surveys "
    "use far more complex models, but the principle is the same.\n\n"
    "Camera traps have drawbacks too. They are expensive, they can be stolen or damaged by elephants, and they work "
    "poorly for animals without distinctive markings. For such species, researchers increasingly turn to DNA "
    "extracted from droppings, which can identify individuals without the animal ever being seen.\n\n"
    "What these methods share is a shift from guesswork to evidence that others can check. A count that can be "
    "repeated and verified, even if imperfect, is worth more than a confident figure that no one can test."))


def capture_recapture(first, second, recaptured):
    """Lincoln-Petersen estimate used in the passage: N = n1 * n2 / m."""
    return first * second // recaptured


assert capture_recapture(40, 40, 20) == 80          # the passage's own example
RC4_ESTIMATE = capture_recapture(40, 40, 10)        # question 4 below
assert RC4_ESTIMATE == 160

Q(RC, "Factual", I,
  "Why, according to the passage, is a direct head-count of tigers impossible?",
  ["Tigers are shy, mostly active at night and spread over thick forest.",
   "Forest departments are not allowed to enter the core of a reserve.",
   "Tigers move between reserves so often that they are counted twice.",
   "Most reserves are too small to hold enough tigers to be counted."], "A",
  "Locating a stated reason",
  "Paragraph 1: 'The animals are shy, mostly active at night and spread across thick forest, so a direct head-count "
  "is impossible.'",
  ["Find 'head-count' in paragraph 1", "Reason before 'so'", "Shy, nocturnal, spread over thick forest"],
  "Restricted entry, movement between reserves and small reserves are never given as reasons; they are plausible "
  "guesses from outside the passage.", 40, P4, 1)

Q(RC, "Factual", I,
  "Which of the following is given in the passage as a weakness of the pugmark method?",
  ["Tigers avoid walking on the soft ground where prints form.",
   "Prints vary with soil and speed, so experts disagreed on them.",
   "Tracing prints needed costly equipment that often broke down.",
   "Prints were washed away before staff could reach the forest."], "B",
  "Locating a stated weakness",
  "Paragraph 2: 'Prints change with the softness of the soil and the speed of the animal, and experts often "
  "disagreed over whether two prints came from one tiger or two.'",
  ["Find 'weaknesses' in paragraph 2", "Prints change with soil and speed", "Experts disagreed"],
  "Paragraph 1 says tigers do leave prints on soft ground, so avoiding it is wrong. Costly equipment is a drawback "
  "of camera traps, not pugmarks. Washed-away prints are never mentioned.", 40, P4, 2)

Q(RC, "Inference", I,
  "What does the critics' argument in paragraph 2 suggest about the old tiger counts?",
  ["They were always lower than the true number of tigers.",
   "They were produced by computers that matched footprints.",
   "They may have reflected officials' wishes more than evidence.",
   "They were checked every year by independent experts."], "C",
  "Inference: what an observed pattern implies",
  "If counts rose 'whenever officials were under pressure to show success', the numbers moved with the officials' "
  "needs, not only with the tigers. The critics were suggesting that the counts could be shaped by what officials "
  "wanted to report.",
  ["Pattern: counts rose when officials needed success", "The figure followed the pressure, not the forest",
   "Counts may have reflected wishes rather than evidence"],
  "'Always lower' runs against the critics' point that counts tended to rise. Computers matching footprints mixes up "
  "the two methods. Independent yearly checks contradict the final paragraph, which praises the new methods because "
  "they can be checked.", 50, P4, 3)

Q(RC, "Inference", I,
  "Using the reasoning of the example in paragraph 4, what would be the estimated population if the cameras "
  "photographed forty tigers in each fortnight but only ten of the second forty had already been seen?",
  ["about forty", "about eighty", "about one hundred and twenty", "about one hundred and sixty"], "D",
  "Inference: applying the capture-recapture logic to new figures",
  f"Ten of forty is one quarter, so the first sample of forty is taken to be about one quarter of the population: "
  f"40 × 4 = {RC4_ESTIMATE}. (Estimate = first sample × second sample ÷ recaptured = 40 × 40 ÷ 10.)",
  ["Share of the second sample already seen: 10 of 40 = one quarter",
   "So the first sample (40) is about one quarter of the population",
   f"Population ≈ 40 × 4 = {RC4_ESTIMATE}"],
  "About eighty is the passage's own answer for twenty recaptures, not ten. About forty would mean every tiger was "
  "seen in the first fortnight. About one hundred and twenty does not follow from any of the figures; fewer "
  "recaptures mean a larger population, here four times the first sample.", 60, P4, 4,
  shortcut="Estimate = (first count × second count) ÷ number seen in both = 40 × 40 ÷ 10 = 160")

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'distinctive' as used in the passage ('they work "
  "poorly for animals without distinctive markings')?",
  ["brightly coloured", "permanently fixed", "easily told apart", "widely admired"], "C",
  "Vocabulary in context: distinctive = marking out one individual from others",
  "Camera traps work for tigers because each stripe pattern is unique, so individuals can be recognised. Animals "
  "without such markings cannot be told apart in photographs. 'Distinctive' therefore means easily told apart.",
  ["Contrast with tigers' unique stripes", "Purpose of markings here: to recognise individuals",
   "'easily told apart'"],
  "'Brightly coloured' confuses being noticeable with being individually recognisable. 'Permanently fixed' and "
  "'widely admired' have nothing to do with telling one animal from another.", 35, P4, 5)

Q(RC, "Tone and title", I,
  "Which of the following best states the main idea of the passage?",
  ["Camera traps have made tiger counts perfectly accurate.",
   "Pugmarks remain the cheapest and best way to count tigers.",
   "Counts that others can check are worth more than confident guesses.",
   "DNA from droppings will soon replace every other counting method."], "C",
  "Main idea: the author's conclusion in the last paragraph",
  "The passage moves from pugmarks to camera traps and DNA, and ends: 'A count that can be repeated and verified, "
  "even if imperfect, is worth more than a confident figure that no one can test.'",
  ["Paras 1–2: pugmarks and their weaknesses", "Paras 3–5: camera traps, capture-recapture, DNA",
   "Para 6: verifiable evidence beats confident guesses"],
  "'Perfectly accurate' contradicts 'even if imperfect' and the drawbacks in paragraph 5. The passage criticises "
  "pugmarks. DNA is offered for animals without markings, not as a replacement for every method.", 45, P4, 6)

# ---------------------------------------------------------------- RC 5 (Intermediate 2 + Advanced 4)
P5 = stim("The trouble with rent control", (
    "Few policies are as popular with voters, or as unpopular with economists, as rent control. When a city caps the "
    "rent that landlords may charge, tenants who already have homes are protected from sudden increases, and "
    "families who might otherwise be forced to move can stay near their schools and jobs. The appeal is easy to "
    "understand, especially in cities where rents have risen far faster than wages.\n\n"
    "The difficulty lies in what happens next. If the permitted rent is well below what the market would bear, "
    "owning a flat to let becomes less rewarding. Some landlords sell their properties, others convert them into "
    "offices or holiday lets, and many simply leave flats empty rather than accept a low rent from a tenant they "
    "cannot easily remove. Builders, expecting controlled returns, put up fewer new rental homes. Over time, the "
    "supply of housing available for rent shrinks.\n\n"
    "Those who already hold controlled tenancies benefit, often for decades. Newcomers to the city, who are "
    "frequently young and poor, find fewer homes on offer and may end up paying more in the uncontrolled part of the "
    "market or making informal payments to secure a flat. The policy thus divides tenants into insiders and "
    "outsiders, and the outsiders are not always better off than they would have been without it.\n\n"
    "Maintenance suffers as well. A landlord who cannot raise the rent has little reason to repair a leaking roof, "
    "and tenants who fear losing a cheap flat are reluctant to complain. In some old city centres, buildings under "
    "long-standing rent control have decayed to the point of danger.\n\n"
    "None of this means that tenants should be left at the mercy of the market. Many economists favour other "
    "remedies: allowing more homes to be built, offering housing allowances to poor families, or limiting how "
    "sharply rents may rise within an existing lease while letting them reset between tenants. Such measures are "
    "less eye-catching than a rent freeze, but they aim at the cause of high rents, a shortage of homes, rather than "
    "at its symptom."))

Q(RC, "Factual", I,
  "According to the passage, why do builders put up fewer new rental homes under rent control?",
  ["They expect the returns on such homes to be held down.",
   "They are legally barred from building rental housing.",
   "They cannot find tenants willing to live in new flats.",
   "They prefer to build schools and offices for the city."], "A",
  "Locating a stated reason",
  "Paragraph 2: 'Builders, expecting controlled returns, put up fewer new rental homes.'",
  ["Find 'Builders' in paragraph 2", "Reason: 'expecting controlled returns'", "Returns held down by the cap"],
  "No legal bar is mentioned. A shortage of tenants contradicts the passage, which describes newcomers struggling to "
  "find homes. Converting flats to offices is something some landlords do, not the builders' reason.", 40, P5, 1)

Q(RC, "Factual", I,
  "What, according to the passage, do many landlords do rather than accept a low rent from a tenant they cannot "
  "easily remove?",
  ["They raise the rent quietly without telling the city.",
   "They leave their flats standing empty.",
   "They move into the flats themselves.",
   "They hand the flats over to the city council."], "B",
  "Locating a stated fact",
  "Paragraph 2: 'many simply leave flats empty rather than accept a low rent from a tenant they cannot easily "
  "remove'.",
  ["Find 'rather than accept a low rent' in paragraph 2", "Action: leave flats empty", "Match the option"],
  "Raising rents secretly, moving in and handing flats to the council are not mentioned. The other actions the "
  "passage names are selling and converting to offices or holiday lets.", 35, P5, 2)

Q(RC, "Inference", A,
  "What does the author imply by describing rent control as dividing tenants into 'insiders and outsiders'?",
  ["Tenants in the city centre pay more than those in the suburbs.",
   "Insiders who complain about repairs are evicted and become outsiders.",
   "Landlords favour tenants from inside the city over migrants from outside.",
   "Existing tenants gain, while newcomers may face fewer homes and higher costs."], "D",
  "Inference: who gains and who loses from a policy",
  "Paragraph 3 says those who hold controlled tenancies benefit 'often for decades', while newcomers find fewer "
  "homes and may pay more or make informal payments. The 'insiders' are existing tenants; the 'outsiders' are "
  "newcomers who bear the cost.",
  ["Insiders: existing controlled tenancies (benefit)", "Outsiders: newcomers (fewer homes, higher costs)",
   "The policy's gains and losses fall on different groups"],
  "The passage does not compare centre and suburbs, does not describe landlords choosing locals over migrants, and "
  "never says complaining tenants are evicted; it says tenants are reluctant to complain.", 55, P5, 3)

Q(RC, "Vocabulary in context", A,
  "What does the phrase 'left at the mercy of the market' mean as used in the passage?",
  ["given generous help by local traders",
   "allowed to bargain freely for better homes",
   "left unprotected from whatever rents the market sets",
   "forced to sell their homes at low prices"], "C",
  "Vocabulary in context: at the mercy of = without any protection against",
  "Having listed the harms of rent control, the author says this does not mean tenants should be left with no "
  "protection at all against market rents, and goes on to suggest other remedies. 'At the mercy of' means in the "
  "power of, unprotected from.",
  ["'None of this means ...' = the author still wants tenants protected", "At the mercy of = powerless against",
   "'left unprotected from whatever rents the market sets'"],
  "'Generous help' takes 'mercy' in its everyday sense of kindness. 'Bargain freely' turns the phrase into a "
  "benefit. 'Forced to sell their homes' confuses tenants with owners.", 40, P5, 4)

Q(RC, "Tone and title", A,
  "Which of the following best describes the author's attitude towards rent control?",
  ["enthusiastic, urging every city to adopt it at once",
   "indifferent, treating housing as a purely private matter",
   "critical of its effects, but sympathetic to tenants' needs",
   "hostile to tenants, whom it blames for high rents"], "C",
  "Tone: weigh criticism against the author's stated concern",
  "The author lists the policy's harms (fewer homes, insiders and outsiders, poor maintenance) but begins by "
  "explaining its appeal and ends by insisting that tenants should not be left at the mercy of the market, proposing "
  "other remedies.",
  ["Paras 2–4: harms of rent control (critical)", "Para 1: its appeal is 'easy to understand'",
   "Para 5: tenants still need protection (sympathetic)"],
  "'Enthusiastic' contradicts the long list of harms. 'Indifferent' is wrong because the author proposes remedies. "
  "'Hostile to tenants' is wrong because the author blames a shortage of homes, not tenants, for high rents.",
  45, P5, 5)

Q(RC, "Inference", A,
  "According to the author, how do the remedies favoured by many economists differ from a rent freeze?",
  ["They help landlords rather than tenants.",
   "They take effect faster than a freeze.",
   "They tackle the shortage of homes behind high rents.",
   "They cost the government nothing at all."], "C",
  "Inference: the contrast drawn in the final sentence",
  "The last sentence says such measures 'aim at the cause of high rents, a shortage of homes, rather than at its "
  "symptom'. A rent freeze treats the symptom (high rents); the remedies address the cause.",
  ["Final sentence: cause vs symptom", "Cause = a shortage of homes", "The remedies aim at that cause"],
  "Housing allowances for poor families and limits within a lease help tenants. Speed is not discussed, and housing "
  "allowances clearly cost the government money.", 45, P5, 6)

# ---------------------------------------------------------------- RC 6 (Advanced, 6)
P6 = stim("The month you were born", (
    "In many sports academies, a curious pattern appears when the players' birth dates are listed. Far more of them "
    "are born in the months just after the cut-off date used to group children by age than in the months just "
    "before it. The pattern has been found in football, cricket and ice hockey across several countries, and "
    "psychologists call it the relative age effect.\n\n"
    "The explanation lies in the way children are sorted. If teams are formed by calendar year, a child born in "
    "January and one born in December of the same year play in the same age group, although the first is almost a "
    "year older. At the age of eight or nine, eleven months can make a large difference to height, strength and "
    "coordination. The older child is more likely to stand out in a trial, be picked for a better team and receive "
    "more coaching, which widens the gap still further. What began as an accident of the calendar is gradually "
    "mistaken for talent.\n\n"
    "The effect does not stop at sport. Studies in several countries have found that, on average, the youngest "
    "children in a school class score slightly lower in early tests and are more often judged to have learning or "
    "behavioural difficulties. Much of this gap narrows as children grow older, but decisions taken early, such as "
    "placement in a slower stream, can have lasting consequences.\n\n"
    "Curiously, the advantage is sometimes reversed at the highest level. A few studies suggest that among the "
    "relatively young players who do reach professional sport, a larger share go on to long careers, perhaps because "
    "they had to develop skill and resilience to compete with bigger rivals.\n\n"
    "Remedies are simple in principle. Selectors can be shown each child's age in months and asked to judge "
    "performance against it; some academies have experimented with rotating the cut-off date each year, or with "
    "grouping children by physical development rather than birth date. None of these removes the effect entirely, "
    "but each reduces the chance that a selector confuses being older with being better."))

Q(RC, "Inference", A,
  "Which of the following best describes the process explained in paragraph 2?",
  ["A small early advantage grows because it attracts more opportunities.",
   "Talent shown at eight or nine years predicts adult success exactly.",
   "Children born in December train harder to make up for their age.",
   "Coaches deliberately choose older children to win junior matches."], "A",
  "Inference: identifying a self-reinforcing process",
  "The older child stands out, is picked for a better team and gets more coaching, 'which widens the gap still "
  "further'. A small head start produces chances that make it larger: a self-reinforcing advantage.",
  ["Start: up to eleven months' physical head start", "Result: selection, better team, more coaching",
   "'widens the gap still further' = the advantage feeds itself"],
  "The passage says the early edge is 'mistaken for talent', not that it predicts adult success. Harder training by "
  "younger children appears only as a guess about professionals in paragraph 4. Nothing says coaches act "
  "deliberately; the point is that they confuse age with ability.", 55, P6, 1)

Q(RC, "Inference", A,
  "Why does the author say that 'an accident of the calendar is gradually mistaken for talent'?",
  ["Parents falsify birth dates so that their children seem talented.",
   "Children born in some months are genetically more gifted at sport.",
   "Academies change their calendars so that talented players fit in.",
   "Selectors read the physical edge of being older as natural ability."], "D",
  "Inference: interpreting a key sentence from its context",
  "Being born just after the cut-off is chance (an 'accident of the calendar'). The extra size and strength it gives "
  "is judged in trials as talent, and further coaching then makes the gap look like real ability.",
  ["'accident of the calendar' = the chance of birth month", "Its effect: greater height, strength, coordination",
   "Selectors take that edge for talent"],
  "Genetic gifts contradict the passage's explanation, which is relative age, not birth month as such. Academies "
  "changing calendars and parents falsifying dates are never mentioned.", 50, P6, 2)

Q(RC, "Factual", A,
  "What do a few studies suggest about relatively young players who reach professional sport?",
  ["They usually retire early because of injuries.",
   "They are paid less than players born earlier.",
   "A larger share of them go on to long careers.",
   "Most of them were born just after the cut-off."], "C",
  "Locating a stated finding",
  "Paragraph 4: 'among the relatively young players who do reach professional sport, a larger share go on to long "
  "careers'.",
  ["Find 'reversed at the highest level' in paragraph 4", "Finding: a larger share have long careers",
   "Match the option"],
  "Early retirement and lower pay are not mentioned. 'Born just after the cut-off' describes the relatively old "
  "players, the opposite group.", 40, P6, 3)

Q(RC, "Inference", A,
  "A cricket academy groups boys by calendar year of birth. Which change would the author most likely support?",
  ["Selecting only boys born between January and March",
   "Holding trials only for boys taller than a fixed height",
   "Judging each boy's performance against his age in months",
   "Excluding boys born in December from the selection trials"], "C",
  "Inference: applying the author's remedies to a new case",
  "The last paragraph proposes showing selectors 'each child's age in months' and asking them to judge performance "
  "against it, so that being older is not confused with being better.",
  ["Problem: older boys in the group look better", "Author's remedy: judge performance against age in months",
   "Match the option"],
  "Selecting only early-born boys, a height bar and excluding December boys would all strengthen the bias against "
  "younger or smaller children, which the author wants to reduce.", 50, P6, 4)

Q(RC, "Vocabulary in context", A,
  "What does the word 'stream' mean as used in the passage ('decisions taken early, such as placement in a slower "
  "stream, can have lasting consequences')?",
  ["a small river running through a valley", "a steady line of thought or argument",
   "a continuous flow of data online", "a group of pupils taught by ability"], "D",
  "Vocabulary in context: stream (in schools) = a class or group of pupils of similar ability",
  "The sentence is about decisions taken in school for children judged to be weaker. Being placed in a 'slower "
  "stream' means being put in a group of pupils taught at a slower pace according to ability.",
  ["Context: school decisions about young pupils", "'slower' describes the pace of teaching",
   "'a group of pupils taught by ability'"],
  "A river, a flow of data and a line of thought are other senses of 'stream' that make no sense with "
  "'placement in a slower ...' in a school.", 40, P6, 5)

Q(RC, "Tone and title", A,
  "Which of the following is the most suitable title for the passage?",
  ["Older Is Not Always Better", "How to Build a Cricket Academy", "The Science of Children's Sleep",
   "Why Talent Is Inherited"], "A",
  "Title: the central idea of the whole passage",
  "The passage shows how being older within an age group is mistaken for being better, in sport and in school, and "
  "ends with remedies that reduce 'the chance that a selector confuses being older with being better'.",
  ["Paras 1–3: older children are taken to be more able", "Para 4: the effect can even reverse",
   "Para 5: stop confusing older with better"],
  "'How to Build a Cricket Academy' is too narrow. Sleep is never discussed. 'Why Talent Is Inherited' contradicts "
  "the passage, which explains the pattern by age, not inheritance.", 40, P6, 6)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic 3 + Intermediate 2)
C1 = stim("The many lives of bamboo", (
    "Bamboo is often called a tree, but it is in fact a giant grass, and one of the fastest-growing plants on earth. "
    "Some species can grow (1) ______ a metre in a single day, and a new clump can be harvested within a few years, "
    "far sooner than most timber trees.\n\n"
    "For centuries, rural communities in India's north-east have used bamboo for almost everything: houses, bridges, "
    "baskets, water pipes and even food, since its young shoots are cooked and eaten as a (2) ______. Because the "
    "plant regrows from its roots after cutting, a well-managed grove can supply material year after year without "
    "being (3) ______.\n\n"
    "Bamboo's strength surprises many people. Weight for weight, some species are remarkably strong when pulled, "
    "which is why builders in parts of Asia still use bamboo poles for scaffolding on tall buildings. It is also light "
    "and (4) ______, so it bends in strong winds rather than snapping.\n\n"
    "The plant does have limits. Untreated bamboo is easily attacked by insects and fungi, and it can rot within a "
    "few years if it is left in damp conditions. Simple treatments with salt solutions can extend its life many times "
    "over, but they are not yet widely (5) ______ by village craftsmen, many of whom have never been shown how to use "
    "them. Supporters argue that with better treatment and design, bamboo could replace some of the cement and steel "
    "used in rural housing, cutting both costs and the pollution that comes from making those materials."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["hardly", "nearly", "seldom", "never"], "B",
  "Cloze: the word must agree with 'one of the fastest-growing plants'",
  "The sentence illustrates how fast bamboo grows, so it must describe a large amount: some species grow nearly a "
  "metre in a day.",
  ["Claim just made: one of the fastest-growing plants", "The example must show great speed",
   "'grow nearly a metre in a single day'"],
  "'Hardly a metre' would play down the growth and clash with 'fastest-growing'. 'Seldom' and 'never' do not fit "
  "before a quantity and would contradict the claim.", 30, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["medicine", "fuel", "delicacy", "decoration"], "C",
  "Cloze: 'cooked and eaten as a ...' needs a kind of food",
  "The list ends with 'even food', and the shoots are 'cooked and eaten'. Something cooked and eaten as a special "
  "food is a delicacy.",
  ["Clue: 'even food'", "Clue: 'cooked and eaten'", "'delicacy'"],
  "Fuel and decoration are not eaten. 'Medicine' does not answer 'even food', the item the sentence is "
  "explaining.", 30, C1, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["harvested", "exhausted", "planted", "watered"], "B",
  "Cloze: 'regrows from its roots' means the supply is not used up",
  "Because bamboo regrows after cutting, a grove can be cut year after year without being used up: without being "
  "exhausted.",
  ["Cause: the plant regrows from its roots", "Result: a lasting supply", "'without being exhausted'"],
  "'Without being harvested' contradicts 'supply material year after year', which requires cutting. 'Planted' and "
  "'watered' do not express the idea of a supply that lasts.", 35, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["rigid", "brittle", "heavy", "flexible"], "D",
  "Cloze: 'so it bends ... rather than snapping' explains the blank",
  "Something that bends instead of breaking is flexible.",
  ["Result clause: bends rather than snapping", "Quality needed: able to bend", "'flexible'"],
  "'Rigid' and 'brittle' describe materials that do not bend and are likely to snap. 'Heavy' contradicts 'light' "
  "earlier in the same sentence.", 30, C1, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["adopted", "opposed", "abandoned", "criticised"], "A",
  "Cloze: the reason given after the blank decides the word",
  "The treatments work, but craftsmen 'have never been shown how to use them'. So the treatments are not yet widely "
  "taken up: not yet widely adopted.",
  ["'but they are not yet widely ___'", "Reason: craftsmen have never been shown how to use them",
   "Not yet taken up = 'not yet widely adopted'"],
  "Craftsmen who have never been shown a method cannot have 'opposed', 'abandoned' or 'criticised' it widely; those "
  "words also do not follow from a lack of training.", 35, C1, 5)

# ---------------------------------------------------------------- Cloze 2 (Intermediate, 6)
C2 = stim("The real cost of free returns", (
    "Online shoppers have come to expect that anything they buy can be sent back free of charge. For retailers, "
    "generous return policies are a powerful way to (1) ______ customers who would otherwise hesitate to buy clothes "
    "or shoes they cannot try on. A buyer who knows she can return a dress is far more likely to order it, and "
    "perhaps to order two sizes at once.\n\n"
    "The convenience, however, comes at a price that the shopper rarely sees. Every returned parcel must be "
    "collected, transported back to a warehouse, inspected and repackaged before it can be sold again. For "
    "low-priced goods, these steps can cost more than the item itself, so many returns are never put back on sale at "
    "all; they are sold off cheaply in bulk or simply (2) ______.\n\n"
    "Returns also add to (3) ______. A parcel that travels to the customer and back again doubles the delivery "
    "journey, and the packaging used for it is often thrown away. Some estimates suggest that a significant share of "
    "everything bought online is returned, and the share is highest for (4) ______, where fit is hard to judge on a "
    "screen.\n\n"
    "Retailers have begun to look for ways to reduce returns without losing customers. Better size charts, "
    "photographs taken from several angles and reviews that mention whether an item runs small or large all help "
    "buyers choose correctly the first time. A few companies have started to charge a small fee for returns, or to "
    "offer a discount to shoppers who (5) ______ to keep an item they are unsure about.\n\n"
    "The broader lesson is that 'free' is seldom truly free. When a service costs the customer nothing, its cost is "
    "usually (6) ______ somewhere else, whether in higher prices, lower wages along the delivery chain, or a heavier "
    "burden on the environment."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["deter", "penalise", "attract", "refund"], "C",
  "Cloze: the purpose of a generous return policy",
  "Customers who would otherwise hesitate are won over by the promise of free returns. The policy is a way to "
  "attract them.",
  ["Customers 'would otherwise hesitate'", "The policy removes their hesitation", "'attract'"],
  "'Deter' and 'penalise' are the opposite of a 'powerful way' to win hesitant buyers. 'Refund customers' does not "
  "explain why they would now buy.", 35, C2, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["displayed", "delivered", "upgraded", "discarded"], "D",
  "Cloze: what happens to returns that are 'never put back on sale'",
  "Goods that are never sold again are either sold off cheaply in bulk or simply thrown away: discarded.",
  ["Clue: 'never put back on sale at all'", "First outcome: sold off cheaply in bulk",
   "Second outcome: thrown away = 'discarded'"],
  "'Displayed' and 'delivered' contradict 'never put back on sale'. 'Upgraded' would add cost to goods whose return "
  "already costs more than they are worth.", 35, C2, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["pollution", "loyalty", "savings", "accuracy"], "A",
  "Cloze: the sentences after the blank explain it",
  "The paragraph describes doubled delivery journeys and packaging that is thrown away, both of which harm the "
  "environment. Returns add to pollution.",
  ["Next sentence: doubled journeys, wasted packaging", "Both are environmental harms", "'pollution'"],
  "'Loyalty', 'savings' and 'accuracy' are benefits, which do not match the costs described next and the passage's "
  "point that the convenience 'comes at a price'.", 35, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["groceries", "clothing", "medicines", "books"], "B",
  "Cloze: 'where fit is hard to judge on a screen'",
  "Fit matters for things that are worn. Paragraph 1 also mentions clothes and shoes that buyers 'cannot try on'. "
  "The share of returns is highest for clothing.",
  ["Clue: 'where fit is hard to judge'", "Para 1: clothes and shoes buyers cannot try on", "'clothing'"],
  "Groceries, medicines and books do not have a 'fit' to judge, so the clue after the blank does not apply to "
  "them.", 35, C2, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["refuse", "forget", "agree", "hesitate"], "C",
  "Cloze: a discount rewards the behaviour the retailer wants",
  "Retailers want fewer returns, so they reward shoppers who choose to keep an item: shoppers who agree to keep it.",
  ["Aim: reduce returns", "A discount rewards keeping the item", "'shoppers who agree to keep an item'"],
  "Retailers would not reward shoppers who 'refuse' or 'hesitate' to keep an item, since that leads to returns. "
  "'Forget to keep' is meaningless here.", 35, C2, 5)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=6), ["avoided", "reduced", "cancelled", "borne"], "D",
  "Cloze: collocation 'a cost is borne (by someone)'",
  "If a service is free to the customer, someone else still pays: the cost is borne (carried) elsewhere, as the "
  "list of higher prices, lower wages and environmental burden shows.",
  ["'free is seldom truly free'", "The cost still falls on someone else", "'its cost is usually borne somewhere else'"],
  "'Avoided', 'cancelled' and 'reduced' would mean the cost disappears or shrinks, contradicting 'free is seldom "
  "truly free' and the list of places where it shows up.", 35, C2, 6)

# ---------------------------------------------------------------- Cloze 3 (Intermediate 1 + Advanced 4; error-based)
C3 = stim("When rates rise, bonds fall", (
    "A government bond is a promise to pay its holder a fixed amount of interest every year and to return the "
    "original sum when the bond matures. Because the interest is fixed when the bond is issued, the bond's market "
    "price must **(1) adjust** whenever interest rates in the economy change.\n\n"
    "Suppose a bond pays seven per cent a year, and soon afterwards new bonds are issued paying eight per cent. No "
    "investor will now pay full price for the old bond when a new one offers more, so the old bond's price must "
    "**(2) rise** until its fixed payments give a buyer roughly the same return as the new bonds. The opposite "
    "happens when rates fall: older bonds, paying more than new ones, become more **(3) attractive**, and their "
    "prices go up.\n\n"
    "This is why bond prices and interest rates are said to be **(4) directly** related. The effect is strongest for "
    "bonds that have many years left to run, because their fixed payments stretch far into the future, so a change "
    "in rates affects a larger stream of income.\n\n"
    "The relationship matters well beyond the bond market. Banks hold large amounts of government bonds, and a sharp "
    "rise in interest rates can reduce the value of these holdings and **(5) strengthen** their balance sheets. "
    "Investors and regulators therefore watch the expected path of interest rates closely, since even a small change "
    "can shift the value of portfolios worth billions. For an ordinary saver, the lesson is simpler: a bond held "
    "until it matures returns its full original sum, but one sold earlier may fetch less than was paid for it."))

Q(CL, "Error-based cloze", I,
  ERR_STEM.format(n=1, ctx="Because the interest is fixed when the bond is issued, the bond's market price must "
                           "adjust whenever interest rates in the economy change"),
  ["remain", "vanish", "double", NR], "D",
  "Error-based cloze: the 'Because' clause explains why the price must change",
  "The interest payment cannot change, so when rates in the economy move, the only thing that can change is the "
  "bond's price. The price must adjust. 'Adjust' is correct.",
  ["Fixed interest cannot move", "So the price has to change when rates change", "'adjust' fits: no replacement"],
  "'Remain' says the price stays the same, the opposite of what the passage goes on to describe. 'Vanish' and "
  "'double' are extreme changes that the passage never describes.", 40, C3, 1)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=2, ctx="No investor will now pay full price for the old bond when a new one offers more, so the "
                           "old bond's price must rise"),
  ["double", "fall", "stabilise", NR], "B",
  "Error-based cloze: follow the logic of 'No investor will now pay full price'",
  "If nobody will pay full price for the old bond, its price has to come down until its fixed seven per cent gives "
  "a buyer about the same return as a new eight per cent bond. The price must fall, not rise.",
  ["Nobody will pay full price for the old bond", "So its price must go down", "Replace 'rise' with 'fall'"],
  "'Double' and 'rise' move the price the wrong way. 'Stabilise' ignores the need for the price to drop. 'Rise' "
  "is wrong, so 'No replacement required' does not apply.", 45, C3, 2)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=3, ctx="older bonds, paying more than new ones, become more attractive, and their prices go up"),
  ["risky", "volatile", "obscure", NR], "D",
  "Error-based cloze: the participle phrase gives the reason",
  "When rates fall, older bonds pay more than new ones, so investors want them more. Being more attractive, their "
  "prices go up. 'Attractive' is correct.",
  ["Older bonds now pay more than new ones", "Investors prefer them", "'attractive' fits: no replacement"],
  "Nothing in the sentence makes old bonds 'risky', 'volatile' or 'obscure'; none of these would explain why "
  "their prices go up. 'Attractive' is correct, so a replacement would spoil the sentence.", 45, C3, 3)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=4, ctx="This is why bond prices and interest rates are said to be directly related"),
  ["closely", "loosely", "inversely", NR], "C",
  "Error-based cloze: 'This is why' sums up the two examples",
  "Paragraph 2 shows that when rates rise, prices fall, and when rates fall, prices rise. Two quantities that move "
  "in opposite directions are inversely related.",
  ["Rates up → prices down; rates down → prices up", "Opposite movement = inverse relation",
   "Replace 'directly' with 'inversely'"],
  "'Closely' and 'loosely' describe how strong the link is, not its direction, so they miss the opposite movement "
  "the paragraph has just shown. 'Directly' says they move together, so 'No replacement required' does not apply.",
  45, C3, 4)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=5, ctx="a sharp rise in interest rates can reduce the value of these holdings and strengthen "
                           "their balance sheets"),
  ["weaken", "diversify", "publish", NR], "A",
  "Error-based cloze: a loss in the value of assets harms the balance sheet",
  "When rates rise, the bonds that banks hold lose value. Losing value on assets weakens a balance sheet; it cannot "
  "strengthen it.",
  ["Rates rise → bond prices fall", "Banks' bond holdings lose value", "Replace 'strengthen' with 'weaken'"],
  "'Diversify' and 'publish' have no link with a fall in the value of holdings. 'Strengthen' contradicts 'reduce "
  "the value', so 'No replacement required' does not apply.", 45, C3, 5)

# =====================================================================================================================
# ERROR DETECTION
# =====================================================================================================================
ED = "Error Detection"
ED_STEM = ("Read the sentence to find out whether there is any grammatical or idiomatic error in it. The error, if "
           "any, will be in one part of the sentence. Choose that part as the answer. If there is no error, choose "
           "'No error'.\n")


def ed(sub, diff, a, b, c, answer, concept, explanation, steps, why, seconds=35):
    text = f"{ED_STEM}{a} (A) / {b} (B) / {c} (C) / No error (D)"
    Q(ED, sub, diff, text, [a, b, c, "No error"], answer, concept, explanation, steps, why, seconds)


# ---- Basic (5)
ed("Part-wise error", B, "The new bank and it's customers", "have both benefited", "from the faster software.", "A",
   "'Its' (possessive: belonging to it) vs 'it's' (short for 'it is' or 'it has')",
   "The customers belong to the bank, so the possessive 'its' is needed: 'The new bank and its customers have both "
   "benefited ...'. 'It's' means 'it is' or 'it has', which makes no sense here.",
   ["Test: 'The new bank and it is customers' is meaningless", "Possession → 'its' (no apostrophe)",
    "'it's' → 'its': error in part A"],
   "Part B's plural verb agrees with the compound subject 'the bank and its customers'. Part C is correct. A has an "
   "error, so 'No error' is wrong.", 30)

ed("Part-wise error", B, "All the money changers at the airport", "must comply to", "the new rules on foreign "
   "currency.", "B",
   "Fixed preposition: 'comply with' (a rule, order or request)",
   "The verb 'comply' takes 'with': 'must comply with the new rules on foreign currency'.",
   ["Verb: comply (obey a rule)", "Fixed pairing: comply with", "'comply to' → 'comply with': error in part B"],
   "Part A is a correct plural subject. Part C is a correct object phrase. B has an error, so 'No error' is wrong.",
   30)

ed("Part-wise error", B, "Most of customers", "who visited the branch today", "came to update their passbooks.",
   "A",
   "'Most' + noun in general ('most customers'), or 'most of' + a determiner + noun ('most of the customers')",
   "'Of' after 'most' needs a determiner such as 'the', 'these' or 'our' before the noun: 'Most of the customers who "
   "visited the branch today ...' (or simply 'Most customers ...').",
   ["'most of' must be followed by the/these/my etc.", "'Most of customers' lacks a determiner",
    "Correct: 'Most of the customers': error in part A"],
   "Part B is a correct relative clause. Part C ('came to update their passbooks') is correct. A has an error, so "
   "'No error' is wrong.", 30)

ed("Part-wise error", B, "The new clerk don't know", "how to use", "the note-counting machine yet.", "A",
   "A third-person singular subject takes 'does', not 'do', in negatives and questions",
   "'The new clerk' is third person singular, so the auxiliary must be 'does': 'The new clerk doesn't (does not) "
   "know how to use the note-counting machine yet.'",
   ["Subject: 'The new clerk' (he/she)", "Third person singular → 'does not'", "'don't' → 'doesn't': error in part A"],
   "Part B ('how to use') is a correct infinitive phrase. Part C correctly places 'yet' at the end of a negative "
   "sentence. A has an error, so 'No error' is wrong.", 25)

ed("Error-free sentence", B, "The guard switched off the lights", "and locked the main door", "before going home.",
   "D",
   "Phrasal verb 'switch off', parallel past verbs, and preposition + gerund",
   "'Switched off the lights and locked the main door' joins two past-tense verbs with 'and'. 'Before going home' "
   "correctly uses a gerund after the preposition 'before'.",
   ["Part A: 'switched off' + object: correct", "Part B: 'locked' matches 'switched' (both simple past)",
    "Part C: 'before' + -ing: correct", "No error"],
   "A, B and C are each correct as shown in the steps. Changing C to 'before go home' or B to 'lock' would create an "
   "error.", 30)

# ---- Intermediate (6)
ed("Part-wise error", I, "This criteria was used", "to select the branches", "for the new pilot scheme.", "A",
   "Greek-origin plurals: one criterion, two criteria (like phenomenon – phenomena)",
   "'Criteria' is the plural of 'criterion'. With 'This' and 'was', a singular is meant: 'This criterion was used "
   "...'. (For the plural: 'These criteria were used ...'.)",
   ["'This' and 'was' are singular", "Singular of 'criteria' = 'criterion'",
    "'This criteria' → 'This criterion': error in part A"],
   "Part B is a correct infinitive of purpose. Part C is a correct prepositional phrase. A has an error, so 'No "
   "error' is wrong.", 35)

ed("Part-wise error", I, "The branch manager finally", "got the customer sign", "the revised loan agreement.", "B",
   "Causative 'get': get + person + to-infinitive (unlike 'make' and 'let', which take a bare infinitive)",
   "'Get someone to do something' means persuade them to do it. The 'to' cannot be dropped: 'finally got the "
   "customer to sign the revised loan agreement'.",
   ["Causative verb: 'got'", "Pattern: get + person + to + verb", "'got the customer sign' → 'got the customer to "
    "sign': error in part B"],
   "Part A is a correct subject with an adverb. Part C is a correct object. B has an error, so 'No error' is "
   "wrong.", 35)

ed("Part-wise error", I, "My colleague did not attend", "the training in Pune,", "and so did I.", "C",
   "Agreeing with a negative statement: 'neither/nor + auxiliary + subject', not 'so + auxiliary + subject'",
   "'So did I' agrees with a positive statement ('He attended, and so did I'). After a negative ('did not attend'), "
   "agreement is 'and neither did I' (or 'nor did I').",
   ["First clause is negative: 'did not attend'", "Negative agreement → 'neither did I'",
    "'and so did I' → 'and neither did I': error in part C"],
   "Part A correctly uses 'did not' + base verb. Part B is a correct place phrase. C has an error, so 'No error' is "
   "wrong.", 35)

ed("Part-wise error", I, "Visitors are prohibited", "to enter the strongroom", "without a senior officer.", "B",
   "'Prohibit' takes 'from' + -ing: prohibit someone from doing something",
   "The pattern is 'prohibit + person + from + -ing'; in the passive, 'be prohibited from + -ing': 'Visitors are "
   "prohibited from entering the strongroom without a senior officer.'",
   ["Verb: prohibit (forbid by rule)", "Pattern: prohibited from + -ing",
    "'to enter' → 'from entering': error in part B"],
   "Part A is a correct passive. Part C is a correct phrase. B has an error, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "Either of the three cashiers", "can open the vault", "in the manager's absence.", "A",
   "'Either' and 'neither' refer to one of two; for three or more, use 'any (one) of' or 'none of'",
   "'Either of' is used when there are exactly two. With three cashiers the sentence needs 'Any of the three cashiers "
   "can open the vault ...' (or 'Any one of').",
   ["Number of people: three", "'Either' = one of two only", "'Either of the three' → 'Any of the three': error in "
    "part A"],
   "Part B correctly uses the modal 'can' + base verb. Part C is a correct phrase. A has an error, so 'No error' is "
   "wrong.", 40)

ed("Part-wise error", I, "The two first chapters of the manual", "explain the rules", "for opening new accounts.",
   "A",
   "Order of numbers: ordinal before cardinal ('the first two', 'the last three'), not 'the two first'",
   "When an ordinal (first, last, next) and a cardinal (two, three) come together, the ordinal comes first: 'The first "
   "two chapters of the manual explain the rules ...'.",
   ["Ordinal: 'first'; cardinal: 'two'", "Order: the + ordinal + cardinal + noun",
    "'The two first chapters' → 'The first two chapters': error in part A"],
   "Part B's plural verb agrees with 'chapters'. Part C is a correct phrase. A has an error, so 'No error' is "
   "wrong.", 35)

# ---- Advanced (4)
ed("Part-wise error", A, "After the firm collapsed,", "he not only lost his job", "but also his life's savings.", "B",
   "Correlative conjunctions ('not only ... but also') must be followed by the same kind of element",
   "'But also' is followed by a noun phrase ('his life's savings'), so 'not only' must be too: 'he lost not only his "
   "job but also his life's savings'. As written, 'not only' comes before the verb 'lost' while 'but also' comes "
   "before a noun, which breaks the parallel.",
   ["'but also' + noun phrase", "So 'not only' + noun phrase", "'not only lost his job' → 'lost not only his job': "
    "error in part B"],
   "Part A is a correct time clause. Part C is the correct second half of the pair; the faulty placement is in B. B "
   "has an error, so 'No error' is wrong.", 45)

ed("Part-wise error", A, "The village where the bank's founder", "was born in", "now has a branch of its own.", "B",
   "A relative adverb ('where', 'when') already contains the preposition; 'where ... in' repeats it",
   "'Where' means 'in which', so adding 'in' at the end of the clause says 'in' twice. Correct: 'The village where the "
   "bank's founder was born now has a branch of its own' (or 'The village in which ... was born', or 'The village "
   "that ... was born in').",
   ["'where' = 'in which'", "'where ... was born in' repeats the preposition",
    "Drop 'in': 'was born': error in part B"],
   "Part A correctly uses 'where' for a place. Part C's singular verb 'has' agrees with 'The village'. B has an "
   "error, so 'No error' is wrong.", 45)

ed("Part-wise error", A, "I clearly remember to lock", "the vault last night,", "so the key must be in the drawer.",
   "A",
   "'Remember + -ing' (recall a past action) vs 'remember + to-infinitive' (not forget a duty)",
   "The speaker is recalling an action already done 'last night', which needs 'remember + -ing': 'I clearly remember "
   "locking the vault last night'. 'Remember to lock' means not forgetting to do it in the future.",
   ["'last night' → the action is in the past", "Recalling a past action → remember + -ing",
    "'remember to lock' → 'remember locking': error in part A"],
   "Part B is a correct object and time phrase. Part C correctly uses 'must be' for a deduction about the present. "
   "A has an error of meaning, so 'No error' is wrong.", 45)

ed("Error-free sentence", A, "Were the bank to raise its lending rate again,", "many small borrowers",
   "would find it hard to repay.", "D",
   "Inverted conditional with 'Were + subject + to-infinitive' (= If the bank were to raise ...)",
   "'Were the bank to raise' is the formal, inverted form of 'If the bank were to raise', used for an unlikely future "
   "event. The main clause correctly uses 'would + base verb'.",
   ["Part A: inversion with 'Were ... to': correct", "Part B: plural subject: correct",
    "Part C: 'would find' for the hypothetical result: correct", "No error"],
   "A, B and C are each correct as shown in the steps. 'Was the bank to raise' or 'will find' would create an "
   "error.", 45)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", I,
  SI_STEM + "After the twelve-hour audit, the cashier did not **feel like to cook** dinner.",
  ["feel like cooking", "feel to cook", "feel like cook", NI], "A",
  "'Feel like' (= want) is followed by a noun or a gerund",
  "'Like' in 'feel like' is a preposition, so the verb after it takes the -ing form: 'the cashier did not feel like "
  "cooking dinner'.",
  ["'feel like' = want, be in the mood for", "'like' is a preposition here", "Preposition + gerund: 'feel like "
   "cooking'"],
  "'Feel to cook' drops 'like' and changes the meaning. 'Feel like cook' uses a base verb after a preposition. The "
  "original uses a to-infinitive after 'like', so 'No improvement required' is wrong.", 30)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "You **need not bring** your passbook yesterday; the bank had already updated your entries online.",
  ["must not have brought", "did not need bringing", "need not have brought", NI], "C",
  "'Need not have + past participle' for something done in the past that turned out to be unnecessary",
  "The customer brought the passbook yesterday, but it was not needed because the entries were already updated. A "
  "past action that was unnecessary is expressed by 'need not have + past participle': 'You need not have brought "
  "your passbook yesterday'.",
  ["Time: 'yesterday' (past)", "The action happened but was unnecessary",
   "'need not have brought'"],
  "'Must not have brought' is a deduction that he did not bring it, which changes the meaning. 'Did not need "
  "bringing' is ungrammatical with a person as subject. 'Need not bring' refers to the present or future, so 'No "
  "improvement required' is wrong.", 40)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "The committee has recommended **that the scheme be extended** to all rural branches.",
  ["that the scheme to be extended", "that the scheme should extended", "that the scheme be extend", NI], "D",
  "Mandative subjunctive: verbs like recommend, insist and demand + 'that' + subject + base form (or 'should' + base "
  "form)",
  "After 'recommend that', the verb in the 'that' clause takes the base form: 'that the scheme be extended'. 'That the "
  "scheme should be extended' would also be correct, but the sentence as written is already correct.",
  ["'recommended that' → subjunctive", "Passive subjunctive: be + past participle", "The bold part is correct"],
  "'That the scheme to be extended' has no finite verb. 'Should extended' drops 'be'. 'Be extend' uses the base form "
  "instead of the participle.", 40)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "Fifteen tonnes of grain was **a too heavy load** for the old lorry to carry up the hill.",
  ["too heavy a load", "a so heavy load", "too much heavy a load", NI], "A",
  "Word order with 'too/so/as/how' + adjective + a/an + noun",
  "When 'too' (or 'so', 'as', 'how') qualifies an adjective before a singular noun, the order is too + adjective + "
  "a + noun: 'too heavy a load'.",
  ["'too' + adjective before 'a/an' + noun", "Order: too heavy a load", "'too heavy a load'"],
  "'A so heavy load' uses the wrong order with 'so' ('so heavy a load' would be needed). 'Too much heavy' is wrong "
  "because 'much' does not qualify a plain adjective. The original 'a too heavy load' has the wrong order, so 'No "
  "improvement required' is wrong.", 40)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", B,
  PR_STEM + "The ATM near the market **ran away of** cash by noon on the day before the festival.",
  ["ran out of", "ran into", "ran off with", NR], "A",
  "Phrasal verbs with 'run': run out of = use up all of something",
  "When a machine has no cash left, it has 'run out of' cash: 'The ATM ... ran out of cash by noon'.",
  ["Meaning needed: had no cash left", "Phrasal verb: run out of", "'ran out of'"],
  "'Ran into' means met by chance or collided with. 'Ran off with' means stole and escaped. The original 'ran away "
  "of' is not a phrasal verb, so 'No replacement required' does not apply.", 25)

Q(PR, "Replace the phrase", B,
  PR_STEM + "The bank has **set up** a help desk in the village to explain the new pension scheme.",
  ["set off", "set aside", "set back", NR], "D",
  "Phrasal verbs with 'set': set up = establish, arrange",
  "To 'set up' a help desk is to establish it. The sentence is correct.",
  ["Object: a help desk", "Meaning needed: established", "'set up' is correct"],
  "'Set off' means start a journey or trigger something. 'Set aside' means keep for later use. 'Set back' means "
  "delay. None means established.", 25)

Q(PR, "Replace the phrase", I,
  PR_STEM + "Please **bear on** me for a few minutes while I check your loan file.",
  ["bear up", "bear with", "bear out", NR], "B",
  "Phrasal verb: bear with (someone) = be patient with someone",
  "The speaker asks the customer to be patient while he checks the file. The phrasal verb for this is 'bear with': "
  "'Please bear with me for a few minutes'.",
  ["Meaning needed: be patient with me", "Phrasal verb: bear with", "'bear with'"],
  "'Bear up' means stay cheerful in difficulty. 'Bear out' means confirm (as in 'the facts bear out his claim'). "
  "'Bear on' means relate to and does not take a person in this sense, so 'No replacement required' does not "
  "apply.", 30)

Q(PR, "Replace the phrase", A,
  PR_STEM + "The union and the management have been **on loggerheads** over the new transfer policy for months.",
  ["at loggerheads", "in loggerheads", "under loggerheads", NR], "A",
  "Fixed expression: 'at loggerheads (with someone / over something)' = in strong disagreement",
  "Two sides in a long, bitter disagreement are 'at loggerheads'. The fixed expression always takes 'at'.",
  ["Meaning: in strong disagreement", "Fixed form: at loggerheads", "'at loggerheads'"],
  "'In loggerheads' and 'under loggerheads' are not idiomatic. The original 'on loggerheads' is not the fixed form, "
  "so 'No replacement required' does not apply.", 30)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", B, SC_OK,
  ["This is the most worst flood the town has seen.",
   "His handwriting is badder than his brother's.",
   "The second road is more worse than the first.",
   "This year's harvest was worse than last year's."], "D",
  "Irregular comparison: bad – worse – worst (never 'more worse', 'most worst' or 'badder')",
  "'Bad' has irregular forms: 'worse' (comparative) and 'worst' (superlative). 'This year's harvest was worse than "
  "last year's' uses the comparative correctly.",
  ["'most worst' → 'worst' (double superlative)", "'badder' → 'worse'",
   "'more worse' → 'worse' (double comparative)", "'was worse than': correct"],
  "The other three add 'more' or 'most' to a form that is already comparative or superlative, or invent the "
  "regular form 'badder'.", 30)

Q(SC, "Grammatically incorrect sentence", B, SC_BAD,
  ["He always reaches the branch before nine.",
   "She comes always late to the Monday meeting.",
   "They are usually busy on the first of the month.",
   "We have never missed a monthly deadline."], "B",
  "Position of frequency adverbs (always, usually, never): before the main verb, after 'be' and after the first "
  "auxiliary",
  "Frequency adverbs go before a main verb: 'She always comes late to the Monday meeting.' 'Comes always' puts the "
  "adverb after the main verb, which is wrong.",
  ["'always reaches': before the main verb: correct", "'comes always': after the main verb: incorrect",
   "'are usually': after 'be': correct", "'have never missed': after the auxiliary: correct"],
  "The other three place the adverb correctly: before a main verb, after 'be', or after an auxiliary.", 30)

Q(SC, "Correct sentence", B, SC_OK,
  ["The meeting is in Monday at ten in the morning.",
   "The meeting is on Monday in ten in the morning.",
   "The meeting is at Monday on ten in the morning.",
   "The meeting is on Monday at ten in the morning."], "D",
  "Prepositions of time: 'on' + day or date, 'at' + clock time, 'in' + part of the day, month or year",
  "Days take 'on' ('on Monday'), clock times take 'at' ('at ten') and parts of the day take 'in' ('in the "
  "morning'). Only one option uses all three correctly.",
  ["Day → on Monday", "Clock time → at ten", "Part of the day → in the morning"],
  "The others use 'in Monday', 'at Monday', 'on ten' or 'in ten', each of which breaks the rule for days or clock "
  "times.", 30)

Q(SC, "Correct sentence", I, SC_OK,
  ["Ramesh is a friend of me from college.",
   "Ramesh is a my friend from college.",
   "Ramesh is one my friend from college.",
   "Ramesh is a friend of mine from college."], "D",
  "Double possessive: a/an/this + noun + of + possessive pronoun (a friend of mine, a colleague of hers)",
  "'A' and 'my' cannot stand together before a noun. To say 'one of my friends' with 'a', English uses 'a friend of "
  "mine', with the possessive pronoun 'mine'.",
  ["'a friend of me' → object pronoun is wrong here", "'a my friend' → two determiners",
   "'one my friend' → 'of' missing", "'a friend of mine': correct"],
  "The others use the object pronoun 'me', put 'a' and 'my' together, or drop the 'of' that 'one of my friends' "
  "needs.", 35)

Q(SC, "Grammatically incorrect sentence", I, SC_BAD,
  ["The lady has two step-daughters and a son.",
   "Both her sons-in-law work in the same bank.",
   "The commanders-in-chief of the three services met today.",
   "Two passer-bys stopped to help the injured guard."], "D",
  "Plural of compound nouns: the main noun takes the plural (passers-by, sons-in-law, commanders-in-chief)",
  "In a compound such as 'passer-by', the main word is 'passer' (the person), so it takes the '-s': 'passers-by'. "
  "'Passer-bys' puts the plural on the wrong part.",
  ["'passer-bys' → 'passers-by': incorrect", "'sons-in-law': plural on 'son': correct",
   "'commanders-in-chief': plural on 'commander': correct", "'step-daughters': plural on 'daughter': correct"],
  "The other three put the plural on the main noun of the compound, which is correct.", 35)

Q(SC, "Correct sentence", I, SC_OK,
  ["He went to the bank for withdrawing some cash.",
   "He went to the bank for to withdraw some cash.",
   "He went to the bank to withdraw some cash.",
   "He went to the bank for withdraw some cash."], "C",
  "Purpose of a person's action: to-infinitive (not 'for + -ing')",
  "To say why someone did something, English uses the to-infinitive: 'He went to the bank to withdraw some cash.' "
  "'For + -ing' describes what a thing is used for ('a machine for counting notes'), not a person's purpose.",
  ["Purpose of going to the bank → to-infinitive", "'for withdrawing' describes a tool's use, not a purpose",
   "'to withdraw': correct"],
  "The others use 'for + -ing', 'for to' or 'for' + base verb, none of which expresses a person's purpose.", 35)

Q(SC, "Grammatically incorrect sentence", A, SC_BAD,
  ["The accident was happened near the toll plaza.",
   "The meeting was postponed because of the strike.",
   "The new branch was opened by the local MLA.",
   "The parcel was delivered to the wrong address."], "A",
  "Intransitive verbs (happen, occur, arrive, die) have no object and therefore no passive form",
  "'Happen' cannot take an object, so it cannot be made passive. The correct sentence is 'The accident happened near "
  "the toll plaza.'",
  ["'was happened': passive of an intransitive verb: incorrect", "'was postponed': transitive, passive: correct",
   "'was opened by': transitive, passive: correct", "'was delivered to': transitive, passive: correct"],
  "Postpone, open and deliver are transitive verbs, so their passives are correct.", 35)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) Every night, after his last trip, he sat under the streetlight near the depot with his books.\n"
  "(B) Suresh worked as a conductor on a city bus, but he dreamt of becoming a teacher.\n"
  "(C) Last month, the former conductor of route 21 took charge of his first class.\n"
  "(D) His regular passengers soon noticed and began lending him their old guidebooks.\n"
  "(E) Three years later, he passed the teachers' eligibility test on his second attempt.",
  ["BDAEC", "BADEC", "ABDEC", "BAEDC"], "B",
  "Para jumble: named opener, then time order (dream → effort → help → success → result)",
  "B introduces Suresh and his dream. A ('he', 'every night') shows his effort. D ('noticed') refers to his studying "
  "under the streetlight. E ('Three years later') gives the exam result, and C ('Last month') the present outcome.",
  ["Opener: B (names Suresh)", "B → A: his nightly study", "A → D: passengers notice the study",
   "D → E → C: exam passed, then his first class: BADEC"],
  "BDAEC has passengers 'notice' before there is anything to notice. ABDEC opens with 'he' before Suresh is named. "
  "BAEDC has passengers lend guidebooks after he has already passed the test.", 45)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) Every morning at eight, two students of a village school read the rain gauge in the playground.\n"
  "(P) They then chalk the figure on a board beside the school gate.\n"
  "(Q) Encouraged by this interest, the school now keeps ten years of readings in a register that anyone may "
  "consult.\n"
  "(R) Farmers passing by soon began to check the board before deciding when to sow.\n"
  "(S) A few of them even come back in the evening to ask how much rain fell in the same week last year.",
  ["PRSQ", "PSRQ", "RPSQ", "PRQS"], "A",
  "Fixed opener; 'They then', 'the board', 'A few of them' and 'this interest' as links",
  "P ('They then') continues the students' routine. R ('the board') tells how farmers use the board. S ('A few of "
  "them') refers to the farmers. Q ('this interest') sums up the farmers' interest and gives the school's response.",
  ["(1) → P: students chalk the reading", "P → R: farmers check 'the board'", "R → S: 'A few of them' = farmers",
   "S → Q: 'this interest' leads to the register: PRSQ"],
  "PSRQ uses 'A few of them' before the farmers are mentioned. RPSQ has farmers check 'the board' before it is "
  "introduced. PRQS gives the school's response before the evening visits that show the interest.", 45)

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) For two years the plants bore nothing, and even Raghu began to have doubts.\n"
  "(B) Today, several of the neighbours who once laughed buy saplings from him.\n"
  "(C) Neighbours laughed when Raghu pulled out his cotton plants and set up concrete poles across his field.\n"
  "(D) In the third summer, however, the poles were heavy with bright pink fruit.\n"
  "(E) The poles, he explained, were to support dragon fruit, a cactus that needs little water.",
  ["CAEDB", "ECADB", "CEDAB", "CEADB"], "D",
  "Para jumble: setting → explanation → setback → turning point ('however') → present result",
  "C introduces Raghu and the strange poles. E ('The poles, he explained') explains them. A gives the two barren "
  "years. D ('In the third summer, however') is the turning point. B ('Today') gives the result.",
  ["Opener: C (names Raghu)", "C → E: the poles explained", "E → A: two years with no fruit",
   "A → D ('however', third summer) → B ('Today'): CEADB"],
  "CAEDB mentions 'the plants' before E says what was planted. ECADB opens with 'he' and 'The poles' before Raghu "
  "is introduced. CEDAB puts the third-summer harvest before the first two barren years.", 45)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Over time, only the debased coins remained in circulation.\n"
  "(B) In the past, coins were made of gold or silver, and their value depended on the metal they contained.\n"
  "(C) People naturally spent the debased coins and hoarded the full-weight ones.\n"
  "(D) When a ruler issued new coins with less precious metal but the same face value as the old ones, the two kinds "
  "circulated side by side.\n"
  "(E) This tendency, summed up as 'bad money drives out good', is known as Gresham's law.",
  ["BCDAE", "BDCAE", "DBCAE", "BDACE"], "B",
  "Para jumble: background → event → behaviour → result → name of the principle ('This tendency')",
  "B gives the background (value from metal). D describes the debasement and two kinds of coin. C ('the debased "
  "coins') gives people's behaviour. A ('Over time') states the result. E ('This tendency') names it.",
  ["Opener: B (general background)", "B → D: debased coins appear", "D → C: people spend bad, hoard good",
   "C → A ('Over time') → E ('This tendency'): BDCAE"],
  "BCDAE mentions 'the debased coins' before D introduces them. DBCAE opens with an event before the background "
  "that explains why less metal matters. BDACE gives the result before the behaviour that causes it.", 55)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) When enough people in a community are vaccinated against a contagious disease, even those who are not "
  "vaccinated gain some protection.\n"
  "(P) A newborn baby or a patient undergoing cancer treatment, for instance, may be unable to take certain "
  "vaccines.\n"
  "(Q) This is because the infection finds too few unprotected people to pass through, and its spread slows or "
  "stops.\n"
  "(R) Such protection matters most for people who cannot be vaccinated themselves.\n"
  "(S) Their safety therefore depends on the choices made by those around them.",
  ["QPRS", "RPQS", "QRSP", "QRPS"], "D",
  "Fixed opener; 'This is because', 'Such protection', 'for instance' and 'Their safety' as links",
  "Q ('This is because') explains the protection in (1). R ('Such protection') says who needs it most. P ('for "
  "instance') gives examples of such people. S ('Their safety') concludes about them.",
  ["(1) → Q: the reason for the protection", "Q → R: 'Such protection' matters most for some",
   "R → P: examples ('for instance')", "P → S: 'Their safety': QRPS"],
  "QPRS gives examples before saying what they are examples of. RPQS separates 'This is because' from the claim in "
  "(1) that it explains. QRSP uses 'Their' before the people it refers to have been described.", 55)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Engineers solve the problem by leaving small gaps, called expansion joints, at regular intervals along "
  "the structure.\n"
  "(B) If a long concrete bridge were built as one solid piece, this movement would set up huge stresses.\n"
  "(C) Like most materials, concrete expands slightly in summer heat and contracts in winter cold.\n"
  "(D) Over time, these stresses could crack the deck or push the supports out of line.\n"
  "(E) Drivers often feel these joints as a gentle bump at regular points on a flyover.",
  ["CDBAE", "BCDAE", "CBADE", "CBDAE"], "D",
  "Para jumble: fact → problem ('this movement') → consequence ('these stresses') → solution → everyday sign",
  "C states the fact of expansion. B ('this movement') shows the problem it causes. D ('these stresses') gives the "
  "damage. A ('the problem') gives the solution. E ('these joints') links it to everyday experience.",
  ["Opener: C (the basic fact)", "C → B: 'this movement' = expansion and contraction",
   "B → D: 'these stresses'", "D → A ('the problem') → E ('these joints'): CBDAE"],
  "CDBAE mentions 'these stresses' before any stress is introduced. BCDAE opens with 'this movement' before the "
  "movement is described. CBADE solves the problem before its consequences are stated and leaves 'these stresses' "
  "after the solution.", 55)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) In many villages, a common pasture is open to every family's cattle.\n"
  "(P) Each family therefore has a reason to add one more animal, even when the land is already overgrazed.\n"
  "(Q) The cost of the damage to the grass, by contrast, is shared among all the families.\n"
  "(R) The benefit of grazing an extra cow, however, goes wholly to the family that owns it.\n"
  "(S) When every family reasons in this way, the pasture is ruined for all.",
  ["RQPS", "QRPS", "RPQS", "PRQS"], "A",
  "Fixed opener; 'however', 'by contrast', 'therefore' and 'in this way' as links",
  "R ('however') contrasts the shared pasture with a private benefit. Q ('by contrast') sets the shared cost against "
  "that benefit. P ('therefore') draws the family's conclusion. S ('in this way') shows the result when all do it.",
  ["(1) → R: shared land, but private benefit", "R → Q: 'by contrast', the cost is shared",
   "Q → P: 'therefore' each family adds an animal", "P → S: 'in this way': RQPS"],
  "QRPS states the cost 'by contrast' before the benefit it is contrasted with. RPQS draws the conclusion "
  "('therefore') before the shared cost that completes the reason. PRQS starts with 'therefore' before any reason is "
  "given.", 55)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) To prevent such a spiral, stock exchanges use circuit breakers.\n"
  "(B) When prices fall sharply, frightened investors often rush to sell, pushing prices down even further.\n"
  "(C) These rules halt trading for a fixed period once an index falls by a set percentage in a day.\n"
  "(D) The pause gives investors time to absorb the news and think before they act.\n"
  "(E) Critics argue, however, that the prospect of a halt can itself cause panic, as traders hurry to sell before "
  "the market closes.",
  ["BCADE", "BACDE", "ABCDE", "BADCE"], "B",
  "Para jumble: problem → solution ('such a spiral') → how it works ('These rules') → benefit ('The pause') → "
  "criticism ('however')",
  "B describes the falling spiral. A ('such a spiral') introduces circuit breakers. C ('These rules') explains them. "
  "D ('The pause') gives the benefit. E ('however') gives the critics' view.",
  ["Opener: B (the problem)", "B → A: 'such a spiral'", "A → C: 'These rules' = circuit breakers",
   "C → D ('The pause') → E ('however'): BACDE"],
  "BCADE uses 'These rules' before any rule is named. ABCDE opens with 'such a spiral' before the spiral is "
  "described. BADCE mentions 'The pause' before C explains that trading is halted.", 55)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) Suppose a skilled lawyer can also type faster than her assistant.\n"
  "(P) Every hour she spends typing is an hour taken away from legal work that earns far more.\n"
  "(Q) Even so, it makes sense for her to leave the typing to the assistant.\n"
  "(R) Economists use the same reasoning, called comparative advantage, to explain why countries trade.\n"
  "(S) Both of them gain when each concentrates on the work at which they are relatively better.",
  ["PQSR", "QSPR", "QPSR", "QPRS"], "C",
  "Fixed opener; 'Even so', the reason, the conclusion about 'both of them', then the general principle",
  "Q ('Even so') gives the surprising conclusion despite (1). P explains why: her time is worth more at legal work. "
  "S ('Both of them') states the gain for lawyer and assistant. R ('the same reasoning') extends it to countries.",
  ["(1) → Q: 'Even so' = despite being faster", "Q → P: the reason (cost of her hour)",
   "P → S: both gain", "S → R: 'the same reasoning' for countries: QPSR"],
  "PQSR separates 'Even so' from the fact in (1) that it answers. QSPR states the shared gain before the reason "
  "for the arrangement. QPRS extends the reasoning to countries before finishing the lawyer's case.", 55)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", B,
  SR_STEM + "(P) did not\n(Q) the customer\n(R) sign the cheque\n(S) because he had forgotten his glasses",
  ["QRPS", "RQPS", "PQSR", "QPRS"], "D",
  "Subject + auxiliary + 'not' + base verb + object, then the reason clause",
  "'The customer did not sign the cheque because he had forgotten his glasses.' Subject (Q), negative auxiliary (P), "
  "base verb + object (R), reason (S).",
  ["Subject: Q", "Negative auxiliary: P ('did not')", "Verb + object: R; reason: S → QPRS"],
  "QRPS puts the verb before 'did not'. PQSR opens with 'did not' before any subject. RQPS opens with a verb "
  "phrase.", 30)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) than the lights went out\n(Q) no sooner had\n(R) begun his speech\n(S) the chairman",
  ["QSRP", "SQRP", "QRSP", "QSPR"], "A",
  "Inversion after 'No sooner': 'No sooner had + subject + past participle ... than ...'",
  "'No sooner had the chairman begun his speech than the lights went out.' 'No sooner had' (Q) is followed by the "
  "subject (S) and the participle (R); the 'than' clause (P) comes last.",
  ["Opening: Q ('No sooner had')", "Subject + participle: S + R", "'than' clause: P → QSRP"],
  "SQRP puts the subject before 'No sooner had'. QRSP puts the participle before the subject. QSPR puts the 'than' "
  "clause before the chairman has begun anything.", 35)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) the small firm would have\n(Q) were it not for\n(R) lost its biggest contract\n"
  "(S) the bank's timely loan",
  ["QPSR", "QSPR", "SQPR", "QSRP"], "B",
  "Inverted conditional: 'Were it not for + noun, ... would have + past participle'",
  "'Were it not for the bank's timely loan, the small firm would have lost its biggest contract.' 'Were it not for' "
  "(Q) takes a noun phrase (S); the main clause follows (P + R).",
  ["Condition: Q + S ('Were it not for the bank's timely loan')", "Main clause: P ('the small firm would have')",
   "Participle + object: R → QSPR"],
  "QPSR puts the main clause between 'Were it not for' and its noun. SQPR opens with a noun phrase that has no "
  "verb. QSRP puts 'lost its biggest contract' before its subject and auxiliary.", 40)

Q(SR, "Word/phrase rearrangement within a sentence", A,
  SR_STEM + "(P) as to approve\n(Q) have the directors been so willing\n(R) rarely\n(S) a loan without any collateral",
  ["QRPS", "RPQS", "RQPS", "RQSP"], "C",
  "Inversion after 'Rarely' (auxiliary before subject) + 'so ... as to + infinitive'",
  "'Rarely have the directors been so willing as to approve a loan without any collateral.' 'Rarely' (R) needs "
  "inversion (Q); 'so willing' is completed by 'as to approve' (P), whose object follows (S).",
  ["Opening negative adverb: R", "Inverted clause: Q ('have the directors been so willing')",
   "'so ... as to' + verb: P; object: S → RQPS"],
  "QRPS places 'rarely' in the middle, where the inversion has no trigger. RPQS puts 'as to approve' before 'so "
  "willing'. RQSP separates 'as to approve' from 'so willing' and leaves it without an object.", 40)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The lecture on tax rules was so ______ that half the trainees were yawning within ten minutes.",
  ["lively", "tedious", "useful", "brief"], "B",
  "Single blank: the 'so ... that' result decides the word",
  "Trainees yawning within ten minutes shows the lecture was dull and tiring: 'tedious'.",
  ["Result: trainees yawning within minutes", "Quality needed: dull, tiring", "'tedious'"],
  "A 'lively' or 'useful' lecture would not make people yawn. 'Brief' does not explain yawning within ten "
  "minutes.", 25)

Q(FB, "Single blank", B,
  FB1 + "The old cashier's honesty is beyond ______; in forty years, not a single rupee has gone missing at his "
  "counter.",
  ["repair", "reach", "reproach", "return"], "C",
  "Fixed phrase: beyond reproach = so good that no one could find fault",
  "Forty years without a rupee going missing shows that no one can find fault with his honesty: it is 'beyond "
  "reproach'.",
  ["Evidence: forty years, nothing missing", "Meaning needed: faultless", "'beyond reproach'"],
  "'Beyond repair' means too damaged to fix. 'Beyond reach' means out of reach. 'Beyond return' is not an idiom. "
  "None describes faultless honesty.", 25)

Q(FB, "Double blank", B,
  FB2 + "The ______ of the new bridge has been delayed because the contractor has not yet ______ the steel.",
  ["construction, received", "destruction, received", "construction, refused", "opening, returned"], "A",
  "Double blank: a delay caused by a missing material",
  "Building (construction) cannot go on without steel. The delay is explained by steel that has not yet arrived: "
  "'has not yet received the steel'.",
  ["Blank 1: a new bridge is being built → construction", "Blank 2: the steel has not arrived → received",
   "'construction, received'"],
  "'Destruction' makes no sense for a new bridge. 'Has not yet refused the steel' gives no reason for delay. "
  "'Opening' and 'returned' do not link the delay to missing steel.", 30)

Q(FB, "Phrase fillers", B,
  FBP + "Volunteers were asked to ______ the leaflets about the free health camp to every house in the lane.",
  ["hand down", "hand out", "hand in", "hand back"], "B",
  "Phrasal verbs with 'hand': hand out = distribute to many people",
  "Giving a leaflet to every house in the lane is distributing it: 'hand out the leaflets'.",
  ["Object: leaflets", "Receivers: every house (many people)", "'hand out'"],
  "'Hand down' means pass to a younger generation. 'Hand in' means submit to an authority. 'Hand back' means "
  "return. None means distribute.", 25)

Q(FB, "Single blank", I,
  FB1 + "The new penalty rules are ______: they apply only to loans taken after 1 April, not to older ones.",
  ["retrospective", "prospective", "perspective", "provisional"], "B",
  "Prospective (applying to the future) vs retrospective (applying to the past)",
  "Rules that apply only from a date onwards, and not to earlier loans, take effect for the future: they are "
  "'prospective'.",
  ["Clue: only loans taken after 1 April", "Not older loans → forward-looking", "'prospective'"],
  "'Retrospective' is the opposite (applying to the past). 'Perspective' is a noun meaning point of view. "
  "'Provisional' (temporary) does not match the explanation after the colon.", 30)

Q(FB, "Single blank", I,
  FB1 + "When reporters asked about the missing funds, the official remained ______, saying only that an inquiry "
  "was under way.",
  ["outspoken", "light-hearted", "tight-lipped", "long-winded"], "C",
  "Single blank: the participle phrase defines the word",
  "Saying 'only that an inquiry was under way' means refusing to give details: being 'tight-lipped'.",
  ["Clue: 'saying only that ...'", "Meaning needed: unwilling to say much", "'tight-lipped'"],
  "'Outspoken' and 'long-winded' describe someone who says a lot. 'Light-hearted' (cheerful) does not fit a "
  "refusal to talk about missing funds.", 30)

Q(FB, "Double blank", I,
  FB2 + "The ______ rise in onion prices, which doubled in a fortnight, ______ the government to ban exports.",
  ["gradual, prompted", "steep, prompted", "steep, prevented", "modest, forced"], "B",
  "Double blank: a relative clause defines the first word; the result decides the second",
  "Prices that double in a fortnight show a 'steep' rise. A steep rise would push (prompt) the government to act by "
  "banning exports.",
  ["Blank 1: doubled in a fortnight → steep", "Blank 2: led the government to act → prompted",
   "'steep, prompted'"],
  "'Gradual' and 'modest' contradict doubling in a fortnight. 'Prevented the government to ban' is both illogical "
  "and ungrammatical ('prevent from').", 30)

Q(FB, "Double blank", I,
  FB2 + "Although the inquiry ______ the manager of any wrongdoing, the ______ of the scandal stayed with him for "
  "years.",
  ["cleared, stigma", "accused, stigma", "cleared, glory", "convicted, shame"], "A",
  "Double blank: 'Although' sets an official result against a lasting effect",
  "'Clear someone of wrongdoing' means declare them innocent. 'Although' introduces a contrast: even so, the shame "
  "or 'stigma' of the scandal stayed with him.",
  ["Blank 1: '___ him of any wrongdoing' → cleared", "'Although' → the bad effect lasted anyway",
   "Blank 2: stigma"],
  "'Accused of wrongdoing' removes the contrast with a lasting stigma. 'Glory' does not come from a scandal. "
  "'Convicted ... shame' removes the contrast that 'Although' requires.", 35)

Q(FB, "Phrase fillers", I,
  FBP + "The new disclosure rules are expected to ______ the practice of hiding fees in the fine print.",
  ["make way for", "put an end to", "come up with", "fall in with"], "B",
  "Phrase meaning: put an end to = stop completely",
  "Disclosure rules are meant to stop a bad practice. 'Put an end to' means stop it.",
  ["Object: a bad practice (hiding fees)", "Purpose of disclosure rules: stop it", "'put an end to'"],
  "'Make way for' means allow something to replace you. 'Come up with' means think of. 'Fall in with' means agree "
  "to. None means stop.", 30)

Q(FB, "Single blank", A,
  FB1 + "The minister's ______ reply, a single sentence that answered none of the questions, angered the "
  "opposition benches.",
  ["curt", "effusive", "exhaustive", "eloquent"], "A",
  "Single blank: the appositive ('a single sentence that answered none of the questions') defines the word",
  "A reply of one sentence that answers nothing and angers listeners is rudely short: 'curt'.",
  ["Description: one sentence, answered nothing", "Effect: angered the opposition", "'curt' (rudely brief)"],
  "'Effusive' (gushing) and 'exhaustive' (complete) contradict 'a single sentence'. 'Eloquent' (fluent and "
  "persuasive) would not anger listeners by answering nothing.", 35)

Q(FB, "Single blank", A,
  FB1 + "Far from being ______, the cost overrun was the predictable result of years of poor planning.",
  ["avoidable", "deliberate", "negligible", "unforeseeable"], "D",
  "Single blank: 'Far from being X' denies X; the rest of the sentence states the opposite",
  "The sentence says the overrun was 'predictable'. 'Far from being' must therefore deny the opposite quality: it "
  "was far from being 'unforeseeable'.",
  ["'Far from being X' = not at all X", "The sentence says: predictable", "X = the opposite: 'unforeseeable'"],
  "'Avoidable' contradicts the point: a result of poor planning could have been avoided. 'Deliberate' and "
  "'negligible' are not opposites of 'predictable', so 'far from being' would not set up the contrast.", 40)

Q(FB, "Double blank", A,
  FB2 + "The committee's report ______ the bank's management for its weak controls but stopped short of ______ any "
  "individual officer.",
  ["praised, naming", "censured, naming", "censured, praising", "exonerated, blaming"], "B",
  "Double blank: 'but stopped short of' marks a step that was not taken",
  "A report on weak controls criticises the management: it 'censured' them. 'Stopped short of' means it did not go "
  "further, that is, it did not name any officer.",
  ["Blank 1: weak controls → criticised (censured)", "'stopped short of' = did not go as far as",
   "Blank 2: the further step = naming individuals"],
  "Reports do not 'praise' weak controls. 'Stopped short of praising' is not a further step after censure. "
  "'Exonerated' (cleared) clashes with 'weak controls'.", 40)

Q(FB, "Double blank", A,
  FB2 + "A ______ of cheap credit, kept going for too long, can ______ asset bubbles that end in painful crashes.",
  ["dearth, inflate", "glut, inflate", "glut, deflate", "shortage, prevent"], "B",
  "Double blank: cause (plenty of credit) and effect (bubbles) must match",
  "Bubbles grow when money is plentiful. A 'glut' (excess) of cheap credit can 'inflate' (blow up) asset bubbles.",
  ["Cheap credit kept going too long → an excess (glut)", "Bubbles are blown up → inflate",
   "'glut, inflate'"],
  "'Dearth' and 'shortage' mean too little credit, which does not create bubbles. 'Deflate' bubbles contradicts "
  "'end in painful crashes'.", 40)

Q(FB, "Phrase fillers", A,
  FBP + "When the auditors began asking awkward questions, the finance head tried to ______ by blaming a junior "
  "clerk.",
  ["steal the show", "toe the line", "bite the dust", "pass the buck"], "D",
  "Idiomatic phrase: pass the buck = shift responsibility onto someone else",
  "Blaming a junior clerk to avoid answering the auditors is shifting the responsibility: 'pass the buck'.",
  ["Action: blaming a junior clerk", "Purpose: escaping responsibility", "'pass the buck'"],
  "'Steal the show' means attract the most attention. 'Toe the line' means obey the rules. 'Bite the dust' means "
  "fail or die. None means shifting blame.", 35)

Q(FB, "Phrase fillers", A,
  FBP + "The two banks' merger plans have been put ______ since the regulator raised objections to the deal.",
  ["in the pipeline", "above board", "on the back burner", "in the offing"], "C",
  "Idiomatic phrase: on the back burner = set aside for later, given low priority",
  "After the regulator's objections, the plans are not being pursued for now: they have been 'put on the back "
  "burner'.",
  ["Event: regulator's objections", "Effect: the plans are set aside", "'on the back burner'"],
  "'In the pipeline' and 'in the offing' mean about to happen, the opposite of being shelved. 'Above board' means "
  "honest and open. Also, only 'on the back burner' fits after 'put'.", 35)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'quiet' used correctly?",
  ["The new branch is quiet close to the bus stand.",
   "She has quiet a lot of work this week.",
   "The banking hall was quiet after the lunch rush.",
   "The loan amount was quiet large for a farmer."], "C",
  "Quiet (adjective: making little noise) vs quite (adverb: fairly, completely)",
  "'Quiet' means making little noise. A banking hall after the lunch rush has few people and little noise.",
  ["'quiet close' → 'quite close' (fairly)", "'quiet a lot' → 'quite a lot'",
   "'was quiet' (little noise): correct", "'quiet large' → 'quite large'"],
  "The other three need the adverb 'quite' (fairly, rather) before an adjective or 'a lot'.", 25)

Q(WU, "Word swap", I,
  WS_STEM + "The **(A) premium** paid the **(B) policyholder** on time, so the **(C) insurer** settled the "
  "**(D) claim** quickly.",
  ["A-B", "C-D", "B-C", "No swap required"], "A",
  "Word swap: check who can perform each action",
  "A policyholder pays a premium; a premium cannot pay anyone. Swapping A and B gives: 'The policyholder paid the "
  "premium on time, so the insurer settled the claim quickly.'",
  ["'The premium paid the policyholder' is meaningless", "Swap A and B", "The rest fits: the insurer settles the "
   "claim"],
  "C-D gives 'the claim settled the insurer'. B-C gives 'The premium paid the insurer ... the policyholder settled "
  "the claim', which still has a premium paying someone. The sentence clearly needs a swap.", 30)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'mitigate' used correctly?",
  ["The high fees will mitigate against small investors joining the scheme.",
   "Planting trees along the river helped to mitigate the damage from floods.",
   "The two brothers decided to mitigate their dispute in court.",
   "She tried to mitigate her friend into lending her the money."], "B",
  "Mitigate (make less severe) vs militate (against) (work against, make less likely)",
  "To 'mitigate' damage is to make it less severe. Trees along a river reduce flood damage, so they help to mitigate "
  "it.",
  ["'mitigate against' → 'militate against' (work against)", "'mitigate the damage' = reduce it: correct",
   "'mitigate their dispute in court' → 'litigate' (go to court)", "'mitigate her friend into' → 'persuade'"],
  "The first confuses 'mitigate' with 'militate'. The third confuses it with 'litigate'. The fourth uses it as if it "
  "meant 'persuade'.", 35)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'venal' used correctly?",
  ["The doctor said the cut was venal and would heal in a week.",
   "He made a venal error in the ledger, which was easily corrected.",
   "The venal officer would approve any file for a suitable bribe.",
   "Her venal face showed how little she had slept."], "C",
  "Venal (open to bribery, corrupt) vs venial (minor, pardonable) vs venous (of the veins)",
  "'Venal' describes a person who can be bribed. An officer who approves any file for a bribe is venal.",
  ["A minor cut → not 'venal' (it has nothing to do with bribery)", "A small, forgivable error → 'venial'",
   "An officer open to bribes → 'venal': correct", "A tired face → 'pale' or 'drawn', not 'venal'"],
  "The second confuses 'venal' with 'venial' (pardonable). The first and fourth use it for things that have nothing "
  "to do with corruption.", 35)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'infer' used correctly?",
  ["Are you inferring that I took the money from the drawer?",
   "His tone inferred that he was unhappy with the decision.",
   "The report infers that the bank's losses will rise next year.",
   "From his silence, the manager inferred that the clerk knew more."], "D",
  "Infer (the listener draws a conclusion) vs imply (the speaker or evidence suggests something)",
  "To 'infer' is to reach a conclusion from evidence. The manager drew a conclusion from the clerk's silence, so he "
  "'inferred' it.",
  ["Speaker hinting → 'implying'", "Listener concluding from silence → 'inferred': correct",
   "A report suggesting → 'implies'", "A tone suggesting → 'implied'"],
  "In the other three, the subject (a speaker, a report, a tone) suggests something, which is 'imply', not "
  "'infer'.", 35)

Q(WU, "Word swap", A,
  WS_STEM + "Higher **(A) interest rates** make **(B) borrowing** costlier and **(C) saving** more **(D) "
  "attractive**.",
  ["B-C", "A-B", "A-D", "No swap required"], "D",
  "Word swap: test each bold word in its slot using economic logic",
  "When interest rates rise, loans cost more (borrowing becomes costlier) and deposits earn more (saving becomes "
  "more attractive). Every word fits its place.",
  ["Higher rates → loans cost more: 'borrowing costlier'", "Higher rates → deposits earn more: 'saving more "
   "attractive'", "No swap required"],
  "B-C gives 'make saving costlier and borrowing more attractive', which reverses the effect of higher rates. A-B "
  "and A-D produce nonsense ('Higher borrowing make interest rates costlier').", 40)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'levy' as used in the sentence:\n"
  "'The bank will levy a small charge on every cash deposit above ten lakh rupees in a month.'",
  ["impose", "waive", "refund", "reduce"], "A",
  "Levy (verb) = impose a tax, fee or charge",
  "The bank will put a charge on large cash deposits. To 'levy' a charge is to impose it.",
  ["Subject: the bank; object: a small charge", "Meaning: put a charge on", "'impose'"],
  "'Waive', 'refund' and 'reduce' all lighten or remove the charge; to levy it is to put it on.", 20)

Q(VO, "Word pairs", B, "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Rigid – Flexible", "Feeble – Weak", "Hostile – Friendly", "Scarce – Abundant"], "B",
  "Word pairs: identify synonyms and antonyms",
  "'Feeble' and 'weak' both mean lacking strength. The other pairs are opposites.",
  ["Rigid (stiff) ≠ flexible (bendable)", "Feeble = weak", "Hostile (unfriendly) ≠ friendly",
   "Scarce (in short supply) ≠ abundant (plentiful)"],
  "The other three pairs are opposites, not synonyms.", 25)

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'inundated' as used in the sentence:\n"
  "'After the bank announced free locker rents for a year, the branch was inundated with applications.'",
  ["refused", "overwhelmed", "delayed", "examined"], "B",
  "Inundated = flooded, overwhelmed (with more than can be handled)",
  "A popular free offer brings far more applications than usual. The branch was flooded or overwhelmed with them.",
  ["Cause: an attractive free offer", "Effect: a huge number of applications", "'overwhelmed'"],
  "'Refused', 'delayed' and 'examined' describe what the branch might do with applications, not the flood of "
  "applications arriving.", 25)

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'anomalies' as used in the sentence:\n"
  "'The year-end audit brought to light several anomalies in the branch's cash records.'",
  ["improvements", "agreements", "irregularities", "summaries"], "C",
  "Anomaly = something that departs from what is normal or expected",
  "Audits 'bring to light' problems. Entries in cash records that do not fit the normal pattern are irregularities.",
  ["Context: an audit 'brought to light' (uncovered) something", "Things an audit uncovers: departures from the "
   "norm", "'irregularities'"],
  "'Improvements', 'agreements' and 'summaries' are not things an audit uncovers as problems; 'brought to light' "
  "suggests something wrong.", 25)

Q(VO, "Word pairs", I, "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Obstinate – Stubborn", "Ardent – Fervent", "Opulent – Impoverished", "Tranquil – Serene"], "C",
  "Word pairs: identify synonyms and antonyms",
  "'Opulent' means very wealthy and luxurious; 'impoverished' means very poor. They are opposites. The other pairs "
  "are synonyms.",
  ["Obstinate = stubborn", "Ardent = fervent (passionate)", "Opulent (rich) ≠ impoverished (poor)",
   "Tranquil = serene (calm)"],
  "The other three pairs are synonyms, not opposites.", 30)

Q(VO, "Contextual meaning", A,
  "Choose the meaning of the word 'salutary' as used in the sentence:\n"
  "'The heavy fine imposed on one careless lender had a salutary effect: the others quickly tightened their "
  "checks.'",
  ["ceremonial", "harmful", "temporary", "beneficial"], "D",
  "Salutary = producing a good effect, often through an unpleasant experience",
  "One lender's fine led the others to improve their checks. The effect was good (beneficial), even though it came "
  "from a penalty.",
  ["Event: a heavy fine on one lender", "Result: others tightened their checks (an improvement)", "'beneficial'"],
  "'Harmful' contradicts the improvement that followed. 'Temporary' is not supported. 'Ceremonial' confuses "
  "'salutary' with 'salute'.", 30)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", B,
  SY_STEM + "The new clerk was **courteous** to every customer, even to those who were rude to him.",
  ["polite", "strict", "nervous", "careless"], "A",
  "Courteous = polite and respectful",
  "Being courteous even to rude customers means being polite and respectful to them.",
  ["Context: kind behaviour even to rude people", "'courteous' = polite", "Closest: 'polite'"],
  "'Strict', 'nervous' and 'careless' do not describe respectful behaviour towards customers.", 20)

Q(SY, "Contextual synonym", I,
  SY_STEM + "Lending to small traders has proved surprisingly **lucrative** for the cooperative bank.",
  ["risky", "profitable", "tiresome", "popular"], "B",
  "Lucrative = producing a lot of money, profitable",
  "A line of lending that is 'lucrative' brings in good profits.",
  ["Context: a bank's lending business", "'lucrative' = making money", "Closest: 'profitable'"],
  "'Risky' and 'tiresome' describe drawbacks. 'Popular' describes demand, not profit.", 25)

Q(SY, "Contextual synonym", I,
  SY_STEM + "Facing heavy losses, the airline **jettisoned** its plan to fly to three new cities.",
  ["announced", "abandoned", "postponed", "expanded"], "B",
  "Jettison = throw away, abandon (a plan or an idea)",
  "Heavy losses forced the airline to drop its expansion plan altogether: it 'jettisoned' (abandoned) it.",
  ["Context: heavy losses", "Action on a costly plan: drop it", "Closest: 'abandoned'"],
  "'Postponed' means delayed, not dropped. 'Announced' and 'expanded' do not fit a company cutting back because of "
  "losses.", 25)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The audience remained **apathetic** throughout the minister's speech on rural credit.",
  ["indifferent", "uninterested", "enthusiastic", "listless"], "C",
  "Apathetic = showing no interest or enthusiasm; antonym: enthusiastic",
  "An 'apathetic' audience shows no interest. The opposite is an 'enthusiastic' one.",
  ["'apathetic' = without interest or feeling", "Opposite: full of interest and eagerness"],
  "'Indifferent', 'uninterested' and 'listless' are all close in meaning to 'apathetic'.", 25)

Q(AN, "Contextual antonym", A,
  AN_STEM + "The businessman's **ostentatious** wedding, with its gold-plated invitations, drew wide criticism.",
  ["showy", "lavish", "flamboyant", "understated"], "D",
  "Ostentatious = designed to impress by showing off wealth; antonym: understated",
  "Gold-plated invitations show a wish to display wealth. The opposite of such a showy event is an 'understated' one, "
  "simple and modest in style.",
  ["'ostentatious' = showy, meant to impress", "Opposite: restrained, modest: 'understated'"],
  "'Showy', 'lavish' and 'flamboyant' are all close in meaning to 'ostentatious'.", 25)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"

Q(ID, "Meaning of idiom", B,
  "Choose the meaning of the idiom 'to call it a day'.",
  ["to stop working for the time being", "to give a day a special name", "to telephone someone daily",
   "to postpone a meeting to the next day"], "A",
  "Idiom: call it a day = decide to stop doing something, especially work, for now",
  "To 'call it a day' is to stop working and go home. For example: 'After clearing the last cheque, the clerks "
  "called it a day.'",
  ["Image: declaring the day's work over", "Meaning: stop working for now"],
  "Naming a day and telephoning daily read the words literally. Postponing a meeting is a different idea: the "
  "idiom means stopping, not rescheduling.", 20)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "Ravi had agreed to invest in his friend's shop, but he **got cold feet** when he saw the rent agreement.",
  ["fell ill suddenly", "became too nervous to go ahead", "lost his temper", "got a better offer"], "B",
  "Idiom: get cold feet = become nervous and withdraw from a plan",
  "Ravi had agreed to invest, but the rent agreement made him lose his nerve: he 'got cold feet' and hesitated to go "
  "ahead.",
  ["Context: agreed, then hesitated on seeing the terms", "Idiom: lose one's nerve before acting"],
  "'Fell ill' takes 'cold feet' literally. 'Lost his temper' and 'got a better offer' are not what the idiom means.",
  25)

Q(ID, "Meaning of idiom", A,
  "Choose the meaning of the idiom 'to steal someone's thunder'.",
  ["to frighten someone with a loud noise", "to borrow money without repaying it",
   "to take credit or attention meant for someone else", "to make someone lose an argument"], "C",
  "Idiom: steal someone's thunder = take the attention or praise that another person expected",
  "If a colleague announces your idea at a meeting just before you do, he 'steals your thunder': he gets the "
  "attention that should have been yours.",
  ["Image: taking another's dramatic effect", "Meaning: taking credit or attention meant for another"],
  "A loud noise reads 'thunder' literally. Unpaid borrowing and losing an argument are not what the idiom means.",
  25)

Q(ID, "Idiom in context", A,
  "Choose the meaning of the idiom in bold.\n"
  "When three of its largest borrowers defaulted in one quarter, the small lender's owners **saw the writing on the "
  "wall** and began looking for a buyer.",
  ["read the terms of the loan agreements carefully", "decided to take the defaulters to court",
   "noticed that someone had damaged their office", "recognised the signs of coming failure"], "D",
  "Idiom: see the writing on the wall = recognise clear signs that something bad, such as failure, is coming",
  "Three large defaults in one quarter were a clear warning. The owners understood that the business was heading for "
  "failure and prepared to sell it.",
  ["Context: heavy defaults, then looking for a buyer", "Idiom: recognise signs of approaching failure"],
  "Reading loan terms and damaged walls take the image literally. Going to court is not suggested by 'began looking "
  "for a buyer'.", 30)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", B,
  OW_STEM + "A place where old public records and historical documents are kept",
  ["museum", "archives", "library", "gallery"], "B",
  "One-word substitution: places for keeping things",
  "'Archives' is the place where historical records and documents are stored.",
  ["Key idea: old records and documents", "Word: archives"],
  "A 'museum' displays objects, a 'library' lends books, and a 'gallery' displays works of art.", 20)

Q(OW, "Single word for a phrase", I,
  OW_STEM + "The practice of those in power giving jobs or favours to their relatives",
  ["nepotism", "favouritism", "patronage", "bribery"], "A",
  "One-word substitution: misuse of power",
  "'Nepotism' is favouring relatives (from Latin 'nepos', nephew or grandson), especially by giving them jobs.",
  ["Key idea: favours to relatives", "Word: nepotism"],
  "'Favouritism' is unfair preference for anyone, not specifically relatives. 'Patronage' is support given by a "
  "patron. 'Bribery' is paying someone to act dishonestly.", 25)

Q(OW, "Single word for a phrase", A,
  OW_STEM + "A person who falsely claims to have special knowledge or skill",
  ["connoisseur", "novice", "charlatan", "sycophant"], "C",
  "One-word substitution: types of people",
  "A 'charlatan' is a fraud who pretends to have knowledge or skill, such as a fake doctor.",
  ["Key idea: false claim to expertise", "Word: charlatan"],
  "A 'connoisseur' is a genuine expert in matters of taste. A 'novice' is a beginner who makes no false claim. A "
  "'sycophant' flatters powerful people.", 25)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", B, AP_STEM + "The bank has issued new debit cards to all its customers.",
  ["New debit cards were issued to all its customers by the bank.",
   "New debit cards have issued to all its customers by the bank.",
   "New debit cards have been issued to all its customers by the bank.",
   "New debit cards had been issued to all its customers by the bank."], "C",
  "Present perfect active (has/have + past participle) → has/have been + past participle",
  "The object 'new debit cards' becomes the subject. 'Has issued' becomes 'have been issued' (plural subject), and "
  "the agent follows 'by'.",
  ["New subject: new debit cards (plural)", "Present perfect passive: have been + issued", "Agent: by the bank"],
  "'Were issued' changes the tense to the simple past. 'Have issued' drops 'been' and is not passive. 'Had been "
  "issued' changes the tense to the past perfect.", 25)

Q(AP, "Voice conversion", I,
  AP_STEM + "The engineers were repairing the main server when the power failed.",
  ["The main server was repaired by the engineers when the power failed.",
   "The main server had been repaired by the engineers when the power failed.",
   "The main server was being repaired by the engineers when the power failed.",
   "The main server was repairing by the engineers when the power failed."], "C",
  "Past continuous active (was/were + -ing) → was/were being + past participle",
  "'Were repairing' describes an action in progress. Its passive keeps the continuous form: 'was being repaired'. "
  "The 'when' clause is not changed.",
  ["New subject: the main server (singular)", "Past continuous passive: was being + repaired",
   "Keep 'when the power failed' unchanged"],
  "'Was repaired' loses the sense of an action in progress. 'Had been repaired' says the repair was already over. "
  "'Was repairing' is active in form and makes the server the one doing the repair.", 30)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", I, DS_STEM + "The visitor said to me, \"May I use your phone for a minute?\"",
  ["The visitor asked me if he might use my phone for a minute.",
   "The visitor asked me that may he use my phone for a minute.",
   "The visitor told me if he may use your phone for a minute.",
   "The visitor asked me whether might he use my phone for a minute."], "A",
  "Reported yes/no question with 'may': asked + if/whether + statement order; 'may' → 'might'",
  "A yes/no question is reported with 'asked (me) if/whether', followed by statement word order. 'May' is "
  "backshifted to 'might', 'I' becomes 'he' and 'your' becomes 'my'.",
  ["'said to me' + question → 'asked me'", "'if' + statement order: 'he might use'", "'your phone' → 'my phone'"],
  "The second uses 'that' with question order. The third uses 'told', keeps 'may' and 'your'. The fourth keeps "
  "question order ('might he use') after 'whether'.", 30)

Q(DS, "Narration change", A, DS_STEM + "He said to me, \"Don't wait for me if I am late.\"",
  ["He told me not to wait for him if he was late.",
   "He told me to not wait for me if I was late.",
   "He said me not to wait for him if he is late.",
   "He told me that don't wait for him if he was late."], "A",
  "Negative command → told + object + not + to-infinitive; the 'if' clause is backshifted and its pronouns change",
  "'Don't wait' becomes 'not to wait' after 'told me'. In the 'if' clause, 'I am' becomes 'he was', and 'for me' "
  "becomes 'for him'.",
  ["'said to me' + command → 'told me'", "'Don't wait' → 'not to wait'", "'for me ... I am late' → 'for him ... he "
   "was late'"],
  "The second keeps 'for me' and 'I'. The third uses 'said me' and keeps 'is'. The fourth keeps the imperative "
  "'don't wait' after 'that'.", 35)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", B, SV_STEM + "After the bus accident, the injured ______ taken to the district hospital.",
  ["was", "were", "has", "is"], "B",
  "'The + adjective' (the injured, the poor, the elderly) refers to a group of people and takes a plural verb",
  "'The injured' means 'the injured people', which is plural. So the verb is plural: 'the injured were taken to the "
  "district hospital'.",
  ["Subject: 'the injured' = injured people", "Plural subject → plural verb", "Past passive: 'were taken'"],
  "'Was' and 'is' are singular. 'Has taken' would be active and make the injured the ones doing the taking.", 25)

Q(SV, "Agreement rules", I, SV_STEM + "What these small borrowers need most ______ timely credit, not another loan waiver.",
  ["are", "have been", "were", "is"], "D",
  "A 'what' clause used as the subject is normally singular",
  "The subject is the whole clause 'What these small borrowers need most', which is treated as singular even though "
  "it contains the plural noun 'borrowers': 'What these small borrowers need most is timely credit ...'.",
  ["Subject: the clause 'What these small borrowers need most'", "A clause as subject → singular verb",
   "Present tense to match 'need': 'is'"],
  "'Are', 'have been' and 'were' are plural, agreeing wrongly with 'borrowers' inside the clause.", 30)

Q(SV, "Agreement rules", A, SV_STEM + "It is I who ______ to blame for the delay in sending the statements.",
  ["is", "are", "am", "be"], "C",
  "In 'It is I/you/we who ...', the verb after 'who' agrees with the pronoun before it",
  "'Who' refers back to 'I', so the verb takes the form that goes with 'I': 'It is I who am to blame'.",
  ["Antecedent of 'who': 'I'", "Verb agrees with 'I' → 'am'", "'It is I who am to blame'"],
  "'Is' agrees wrongly with 'It'. 'Are' does not agree with 'I'. 'Be' is not a finite form.", 30)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Sequence of tenses", B, TE_STEM + "According to the timetable, the first train to Pune ______ at 5.40 "
  "tomorrow morning.",
  ["leaves", "left", "has left", "had left"], "A",
  "Simple present for a future event fixed by a timetable",
  "Events fixed by an official timetable or schedule take the simple present even when they are in the future: 'the "
  "first train to Pune leaves at 5.40 tomorrow morning'.",
  ["'According to the timetable' → a scheduled event", "Future time: 'tomorrow morning'",
   "Timetable future → simple present: 'leaves'"],
  "'Left', 'has left' and 'had left' are past or perfect forms that clash with 'tomorrow morning'.", 20)

Q(TE, "Sequence of tenses", B, TE_STEM + "If I ______ a car, I would drive to the branch every day.",
  ["have", "had", "will have", "would have"], "B",
  "Second conditional: If + simple past, ... would + base verb (an unreal or unlikely present situation)",
  "The speaker does not have a car; the situation is imagined. The 'if' clause takes the simple past ('had') and the "
  "main clause 'would + base verb'.",
  ["Main clause: 'would drive' → second conditional", "Imagined present situation", "'If I had a car'"],
  "'Have' gives a first conditional, which needs 'will drive'. 'Will have' and 'would have' are not used in the 'if' "
  "clause here.", 25)

Q(TE, "Perfect tenses", I,
  TE_STEM + "By next March, she ______ at this branch for ten years.",
  ["will be working", "has been working", "will have been working", "would work"], "C",
  "Future perfect continuous: an action continuing up to a point in the future, with its duration",
  "'By next March' fixes a future point, and 'for ten years' gives the length of an action continuing up to it. This "
  "needs 'will have been working'.",
  ["Future point: 'By next March'", "Duration up to that point: 'for ten years'", "'will have been working'"],
  "'Will be working' describes an action in progress at a future time but cannot measure duration up to it. 'Has "
  "been working' is anchored to now, not to next March. 'Would work' is conditional.", 30)

Q(TE, "Perfect tenses", A,
  TE_STEM + "It was the first time that Mohan ______ a loan, so he read every clause of the agreement twice.",
  ["has taken", "had taken", "took", "was taking"], "B",
  "'It was the first/second time (that) ...' takes the past perfect",
  "Just as 'It is the first time' takes the present perfect, 'It was the first time' (a past frame) takes the past "
  "perfect: 'It was the first time that Mohan had taken a loan'.",
  ["Frame: 'It was the first time' (past)", "Past frame → past perfect", "'had taken'"],
  "'Has taken' belongs with 'It is the first time'. 'Took' and 'was taking' are not used after 'It was the first time "
  "that' in standard grammar.", 30)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", B,
  AR_STEM + "Both cashiers at the counter were wearing ______ same blue uniform.",
  ["a", "an", "the", "no article"], "C",
  "'The' is always used with 'same'",
  "'Same' points to one particular thing that is shared, so it always takes 'the': 'the same blue uniform'.",
  ["Word before the noun: 'same'", "'same' always takes 'the'", "'the same blue uniform'"],
  "'A same' and 'an same' are never used. Without an article, 'wearing same blue uniform' is ungrammatical.", 20)

Q(AR, "Definite and indefinite", I,
  AR_STEM + "What ______ lovely weather we are having! And what ______ beautiful garden the bank has planted!",
  ["a, a", "the, the", "a, no article", "no article, a"], "D",
  "Exclamations with 'What': 'What a/an + singular countable noun!' but 'What + uncountable or plural noun!'",
  "'Weather' is uncountable, so it takes no article: 'What lovely weather!'. 'Garden' is singular and countable, so "
  "it takes 'a': 'What a beautiful garden!'.",
  ["Blank 1: 'weather' is uncountable → no article", "Blank 2: 'garden' is singular countable → 'a'",
   "'no article, a'"],
  "'A lovely weather' treats an uncountable noun as countable. Dropping 'a' before 'beautiful garden' is wrong. "
  "'The' is not used in 'What ...!' exclamations.", 30)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", B,
  PP_STEM + "During the festival season, the rural branch is always short ______ staff.",
  ["in", "from", "with", "of"], "D",
  "Fixed preposition: 'short of' = not having enough of something",
  "A branch that does not have enough staff is 'short of staff'. The adjective 'short' in this sense takes 'of'.",
  ["Meaning: not having enough staff", "Fixed pairing: short of", "'of'"],
  "'Short in', 'short with' and 'short from' are not used for lacking something. ('Short with someone' means "
  "rude or impatient to them, which does not fit staff.)", 20)

Q(PP, "Fixed prepositions", I,
  PP_STEM + "The education loan is repayable ______ sixty equal monthly instalments after the course ends.",
  ["on", "in", "by", "with"], "B",
  "Fixed preposition: repay or pay 'in' instalments",
  "A sum paid in parts is paid 'in instalments': 'repayable in sixty equal monthly instalments'.",
  ["Noun: instalments (the parts of the payment)", "Fixed pairing: in instalments", "'in'"],
  "'On', 'by' and 'with' are not used with 'instalments' in this sense.", 25)

Q(PP, "Phrasal verbs", I,
  PP_STEM + "When the highway project ended, the contractor had to ______ fifty temporary workers.",
  ["lay off", "lay down", "lay out", "lay by"], "A",
  "Phrasal verb: lay off = dismiss workers because there is no more work for them",
  "When a project ends, workers hired for it lose their jobs. An employer who dismisses workers for lack of work "
  "'lays them off'.",
  ["Event: the project ended", "Object: temporary workers", "'lay off'"],
  "'Lay down' means put down or establish (rules). 'Lay out' means arrange or spend. 'Lay by' means save for later. "
  "None means dismiss workers.", 25)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"

Q(CN, "Sentence connectors", I,
  "Choose the connector that best fills the blank.\n"
  "______ most of its borrowers are farmers, the cooperative bank's fortunes depend heavily on the monsoon.",
  ["Even though", "So that", "Unless", "Given that"], "D",
  "'Given that' = considering the fact that (introduces a reason)",
  "The bank depends on the monsoon because its borrowers are farmers. 'Given that' introduces this known fact as the "
  "reason.",
  ["Clause 1: most borrowers are farmers (a fact)", "Clause 2: the bank depends on the monsoon (a result)",
   "Reason → 'Given that'"],
  "'Even though' signals a contrast that is not there. 'Unless' makes the fact a condition. 'So that' gives a "
  "purpose.", 30)

Q(CN, "Sentence connectors", I,
  "Choose the connector that best fills the blank.\n"
  "You may keep the locker ______ you pay the annual rent on time.",
  ["unless", "even though", "so that", "as long as"], "D",
  "'As long as' = on condition that",
  "Keeping the locker depends on paying the rent on time. 'As long as' introduces this condition.",
  ["Permission: keep the locker", "Condition: pay the rent on time", "'as long as'"],
  "'Even though' signals contrast. 'So that' gives a purpose. 'Unless' would mean you may keep the locker only if you "
  "do not pay on time.", 25)

Q(CN, "Sentence connectors", A,
  "Choose the connector that best fills the blank.\n"
  "______ carefully the bank checks its documents, a few clever forgeries will always slip through.",
  ["Moreover", "Whatever", "Although", "However"], "D",
  "'However + adjective/adverb' = no matter how",
  "'However carefully the bank checks' means 'no matter how carefully it checks'. The result (forgeries slip through) "
  "happens whatever the degree of care.",
  ["Blank is followed by an adverb: 'carefully'", "Meaning needed: no matter how", "'However carefully ...'"],
  "'Moreover' adds a point and cannot be followed by an adverb this way. 'Whatever' goes with a noun ('whatever "
  "checks'). 'Although carefully the bank checks' is ungrammatical.", 35)

Q(CN, "Starters and linkers", A,
  "Combine the two sentences into one without changing the meaning, and choose the option that correctly begins the "
  "combined sentence.\n"
  "The officer checked all the documents. Then she approved the loan.",
  ["Having checked all the documents,", "Checked all the documents,", "Having been checked all the documents,",
   "After checked all the documents,"], "A",
  "Perfect participle ('Having + past participle') for the earlier of two actions by the same subject",
  "The officer did both actions, one after the other. 'Having checked all the documents, she approved the loan' "
  "shows that the checking was completed first.",
  ["Same subject for both actions: the officer", "Earlier action → 'Having + past participle'",
   "'Having checked all the documents, she approved the loan.'"],
  "'Checked all the documents' and 'After checked' are not complete participle forms. 'Having been checked' is "
  "passive and would describe the officer as the one checked.", 35)

Q(CN, "Sentence connectors", A,
  "Choose the word that best fills the blank.\n"
  "______ than cut jobs during the slowdown, the company reduced the salaries of its top managers.",
  ["Instead", "Other", "Better", "Rather"], "D",
  "'Rather than' = instead of; it can begin a sentence and be followed by a base verb",
  "The company chose one action in place of another. 'Rather than cut jobs, the company reduced ...' expresses this "
  "preference.",
  ["Two alternatives: cutting jobs or cutting top salaries", "Blank + 'than' = in place of",
   "'Rather than cut jobs, ...'"],
  "'Instead' takes 'of', not 'than' ('Instead of cutting jobs'). 'Better than' and 'Other than' change the meaning "
  "and do not express a choice of one action over another.", 30)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_006_plan.json").read_text(encoding="utf-8"))
eng = next(s for s in plan["subjects"] if s["subject"] == EN)
have = Counter((q["topic"], q["difficulty"]) for q in QS)
for t in eng["topics"]:
    for d, n in t["quota"].items():
        assert have[(t["topic"], d)] == n, (t["topic"], d, have[(t["topic"], d)], n)
    for q in QS:
        if q["topic"] == t["topic"]:
            assert q["subtopic"] in t["subtopics"], (q["topic"], q["subtopic"])
assert {q["topic"] for q in QS} <= {t["topic"] for t in eng["topics"]}
assert len(QS) == eng["total"] == 150
assert QS[0]["question_id"] == eng["question_ids"][0] and QS[-1]["question_id"] == eng["question_ids"][1]
assert STIMULI[0]["stimulus_id"] == eng["stimulus_id_start"]

for s in STIMULI:
    words = len(s["content"].replace("*", "").split())
    assert 250 <= words <= 450, (s["stimulus_id"], words)
    members = [q for q in QS if q.get("stimulus_id") == s["stimulus_id"]]
    assert 4 <= len(members) <= 6, (s["stimulus_id"], len(members))
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

# no reused stem or passage title across the earlier English files (BATCH_000 to BATCH_005)
earlier, titles = set(), set()
for f in EARLIER:
    data = json.loads((ROOT / "batches" / f).read_text(encoding="utf-8"))
    for q in data["questions"]:
        if q["subject"] == EN:
            earlier.add(q["question_text"].strip().lower())
    titles |= {s["title"].lower() for s in data.get("stimuli", []) if s["stimulus_id"].startswith("STIM_ENG")}
for s in STIMULI:
    assert s["title"].lower() not in titles, s["title"]

# theme check: a passage's keywords (words of 5+ letters used 2+ times, minus common words) must not largely coincide
# with those of any earlier English passage. Calibrated on BATCH_000-004: it rejects a deposit-insurance passage
# against 'A net or a hammock' (6 of 12 keywords shared), while unrelated passages share at most 3. Extended to
# BATCH_005 for this batch.
STOP = set("about after again against among because before being between bring could every first found great large "
           "later might money other people place price prices still their there these thing those three through "
           "under until where which while whose would years often never since cannot always".split())


def theme_words(text):
    words = [w.strip(".,;:'\"()!?*-—–").lower() for w in text.split()]
    counts = Counter(w for w in words if len(w) >= 5 and w.isalpha() and w not in STOP)
    return {w for w, n in counts.items() if n >= 2}


earlier_themes = {}
for f in EARLIER:
    for st in json.loads((ROOT / "batches" / f).read_text(encoding="utf-8")).get("stimuli", []):
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

keys = Counter(q["correct_answer"] for q in QS)
assert max(keys.values()) <= 0.28 * len(QS) and min(keys.values()) >= 0.22 * len(QS), keys

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_006",
    "created_at": TODAY,
    "notes": "BATCH_006 English Language part: 150 original questions (BANK_ENG_000754 to BANK_ENG_000903). Six "
             "reading passages (31 questions) and three cloze passages (16 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 to BATCH_005; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules, words and idioms not tested in earlier batches. "
             "Each answer was set by the author and re-solved in a separate blind pass by fresh checkers without the "
             "key. Pending human review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_006_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))})")
