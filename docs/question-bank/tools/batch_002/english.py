"""Writes batches/parts/BATCH_002_ENG.json: the 150 English Language questions of BATCH_002.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000 and BATCH_001. Run from anywhere:

    python docs/question-bank/tools/batch_002/english.py

Structural checks (quota per topic and difficulty, subtopics, passage length, set sizes, option count, cloze blank
numbering, para-jumble option validity, answer-key balance) are asserted before anything is written.
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
FIRST_ID = 154
FIRST_STIM = 2001

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
P1 = stim("The return of millets", (
    "Not long ago, millets such as ragi, jowar and bajra were dismissed in many Indian homes as 'poor man's food'. "
    "Rice and wheat, supported by assured government procurement and subsidised distribution, gradually took their "
    "place on the plate, and the area under millets shrank steadily over several decades. Today, however, these "
    "hardy grains are enjoying a revival, and the reasons are as much about health and climate as about taste.\n\n"
    "Nutritionists point out that millets are rich in fibre, iron and calcium, and that they release sugar into the "
    "blood more slowly than polished rice. For a country with a rising number of people living with diabetes, this "
    "matters a great deal. Farmers, for their part, value millets because they grow on poor soils and need far less "
    "water than paddy. In regions where the monsoon is becoming less predictable, a crop that survives a dry spell "
    "can be the difference between a modest income and none at all.\n\n"
    "The revival has not been easy, though. Millets are harder to process than rice or wheat; the small grains must "
    "be cleaned, de-husked and sometimes soaked before they can be cooked, and many villages lack the machines to do "
    "this. City consumers who are willing to pay more for millet biscuits and breakfast cereals often have little "
    "idea how to cook the grain itself. As a result, a large share of the price paid in a supermarket goes to "
    "processors and brands rather than to the farmer.\n\n"
    "If the revival is to last, it will need more than enthusiasm. Small processing units close to the farms, fair "
    "procurement prices and recipes that suit modern kitchens could together turn a passing trend into a lasting "
    "change in what the country grows and eats. The humble millet, in short, deserves to be treated not as a fashion "
    "but as a foundation."))

Q(RC, "Factual", B,
  "According to the passage, why did rice and wheat gradually replace millets on Indian plates?",
  ["Millets were banned from village markets.",
   "Rice and wheat were backed by assured procurement and subsidised distribution.",
   "Farmers found that millets needed too much water.",
   "Millets could not be grown on poor soils."], "B",
  "Locating a stated reason",
  "The first paragraph says rice and wheat, 'supported by assured government procurement and subsidised "
  "distribution', gradually took the place of millets.",
  ["Find the sentence about rice and wheat in paragraph 1",
   "The reason given is government support: procurement and subsidised distribution", "Option B restates it"],
  "A: no ban is mentioned. C and D reverse the passage, which says millets need far less water than paddy and grow "
  "on poor soils.", 60, P1, 1)

Q(RC, "Factual", B,
  "Which of the following is NOT mentioned in the passage as an advantage of millets?",
  ["They are rich in fibre, iron and calcium.",
   "They release sugar into the blood more slowly than polished rice.",
   "They grow on poor soils and need far less water than paddy.",
   "They fetch farmers a higher share of the supermarket price than rice does."], "D",
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 2 lists the nutritional and farming advantages in A, B and C. Paragraph 3 says the opposite of D: a "
  "large share of the supermarket price goes to processors and brands rather than to the farmer.",
  ["Paragraph 2: fibre, iron, calcium (A); slow sugar release (B); poor soils, less water (C)",
   "Paragraph 3: most of the retail price does not reach the farmer", "So D is not an advantage stated: answer D"],
  "A, B and C are all stated as advantages in paragraph 2, so none of them can be the 'NOT mentioned' answer.",
  60, P1, 2)

Q(RC, "Inference", B,
  "Why, according to the passage, does a large share of the price paid for millet products not reach the farmer?",
  ["Farmers sell their grain directly to city consumers.",
   "The government fixes a very low retail price for millet products.",
   "Processing is difficult, and much of the value is captured by processors and brands.",
   "Millets spoil quickly and must be sold cheaply."], "C",
  "Linking a result ('As a result') to the reasons before it",
  "Paragraph 3 explains that millets are hard to process, villages lack machines and city buyers purchase processed "
  "goods such as biscuits. 'As a result', the money goes to processors and brands. Option C joins these points.",
  ["Find 'As a result' in paragraph 3 and read the sentences before it",
   "Causes: hard processing, no village machines, buyers want processed products",
   "Effect: value goes to processors and brands: option C"],
  "A contradicts the passage: the sale is through supermarkets and brands, not direct. B (government retail price) "
  "and D (quick spoilage) are never mentioned.", 60, P1, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is most similar in meaning to the word 'hardy' as used in the passage ('these hardy "
  "grains')?",
  ["robust", "fragile", "expensive", "tasty"], "A",
  "Vocabulary in context: hardy = able to survive difficult conditions",
  "The passage says millets grow on poor soils, need little water and survive dry spells. A 'hardy' crop is tough "
  "and able to withstand hard conditions, so 'robust' is closest.",
  ["Look for clues: poor soils, little water, survives a dry spell", "These describe toughness",
   "'robust' fits"],
  "'Fragile' is the opposite. 'Expensive' and 'tasty' are not suggested by the passage's description of how millets "
  "grow.", 40, P1, 4)

# ---------------------------------------------------------------- RC 2 (Basic 3 + Intermediate 2)
P2 = stim("The library that listened", (
    "For years, the district library in a small town in central India was a quiet, dusty building visited mainly by "
    "retired men reading the morning newspapers. Its shelves held old textbooks, its fans rarely worked, and its "
    "timings, ten in the morning to five in the evening, suited almost no one who had a job or attended college. "
    "Many residents assumed it would simply close one day without anyone noticing.\n\n"
    "That changed when a new librarian decided to ask people what they actually wanted. The answers surprised her. "
    "Students preparing for competitive examinations wanted a quiet place to study and access to recent guidebooks "
    "they could not afford to buy. Young mothers wanted a corner where their children could read picture books. "
    "Daily-wage workers wanted help filling in online forms for government schemes. None of them had ever been asked "
    "before.\n\n"
    "With a modest grant from the municipality and donations from local shops, the library extended its hours into "
    "the evening, set up a reading room for aspirants and installed four computers with an internet connection. "
    "Volunteers, many of them former students, offered to help visitors with forms and applications. Within two "
    "years, daily footfall rose from about thirty to more than four hundred, and a waiting list formed for seats in "
    "the reading room.\n\n"
    "The story is not unique. Across the country, libraries that were once written off are finding new life by "
    "becoming community spaces rather than mere storehouses of books. Their success suggests a simple lesson that "
    "applies well beyond libraries: public institutions decline not only when they lack money but when they stop "
    "listening to the people they are meant to serve."))

Q(RC, "Factual", B,
  "According to the passage, why did the library's old timings suit almost no one?",
  ["They clashed with the hours of people who had jobs or attended college.",
   "The library opened only on weekends.",
   "The building had no electricity in the evening.",
   "The librarian was often absent."], "A",
  "Locating a stated fact",
  "Paragraph 1 says the timings, ten to five, 'suited almost no one who had a job or attended college': these people "
  "were busy during exactly those hours.",
  ["Find 'timings' in paragraph 1", "Ten to five overlaps with working and college hours", "Option A"],
  "B, C and D are never mentioned. The passage mentions fans that rarely worked, not a lack of electricity, and says "
  "nothing about the old librarian's attendance.", 50, P2, 1)

Q(RC, "Factual", B,
  "Which of the following was NOT one of the changes made by the library?",
  ["Extending its hours into the evening", "Setting up a reading room for aspirants",
   "Installing computers with an internet connection", "Charging a membership fee to cover its costs"], "D",
  "Factual (NOT) question",
  "Paragraph 3 lists the changes: longer hours, a reading room and four computers with internet. The money came from "
  "a municipal grant and shop donations; no membership fee is mentioned.",
  ["List the changes in paragraph 3: hours, reading room, computers", "Funding: grant and donations",
   "A membership fee is not mentioned: D"],
  "A, B and C are all named in paragraph 3 as changes the library made.", 50, P2, 2)

Q(RC, "Factual", B,
  "What did the daily-wage workers want from the library?",
  ["Picture books for their children", "Help filling in online forms for government schemes",
   "Recent guidebooks for examinations", "A quiet place to study"], "B",
  "Matching each group to its stated need",
  "Paragraph 2 says daily-wage workers 'wanted help filling in online forms for government schemes'.",
  ["Paragraph 2 lists three groups and their needs", "Daily-wage workers → help with online forms",
   "Option B"],
  "A is what young mothers wanted. C and D are what students preparing for examinations wanted.", 45, P2, 3)

Q(RC, "Inference", I,
  "Which of the following does the passage suggest was the main reason for the library's revival?",
  ["A large grant from the state government", "The supply of free newspapers to all visitors",
   "The librarian asked people what they needed and the library responded to those needs",
   "The closure of other libraries in the district"], "C",
  "Inference: identify the turning point and the author's own conclusion",
  "Paragraph 2 says things 'changed when a new librarian decided to ask people what they actually wanted', and every "
  "change in paragraph 3 answers one of those wants. The final sentence makes listening the key lesson.",
  ["Turning point: the librarian asks people what they want",
   "Changes made match the needs people expressed", "Conclusion: institutions decline when they stop listening",
   "So listening and responding drove the revival: C"],
  "A: the grant was 'modest' and came from the municipality, not the state. B: newspapers belong to the old, "
  "declining library. D: no other library closure is mentioned.", 60, P2, 4)

Q(RC, "Tone and title", I,
  "Which of the following best expresses the central lesson the author draws from the story?",
  ["Libraries should replace books with computers.",
   "Small towns no longer need public libraries.",
   "Volunteers can run public institutions without any funding.",
   "Public institutions thrive when they listen and respond to the people they serve."], "D",
  "Main idea: the lesson is stated in the concluding sentence",
  "The last sentence says public institutions decline 'when they stop listening to the people they are meant to "
  "serve'. The positive form of this lesson is option D.",
  ["Read the final paragraph: 'a simple lesson that applies well beyond libraries'",
   "Lesson: institutions decline when they stop listening", "Positive restatement: D"],
  "A: computers were only one change; books remained. B is contradicted by the rise in footfall. C ignores the "
  "municipal grant and shop donations.", 60, P2, 5)

# ---------------------------------------------------------------- RC 3 (Intermediate, 6)
P3 = stim("Keeping it fresh", (
    "India is among the world's largest producers of fruits and vegetables, yet a significant share of what its "
    "farmers grow never reaches a consumer. Tomatoes split in the back of overloaded trucks, bananas ripen too early "
    "in hot warehouses, and leafy vegetables wilt while waiting for a buyer at a crowded market yard. Estimates of "
    "post-harvest loss vary, but even conservative figures suggest that the value lost every year is enormous.\n\n"
    "The missing link is the cold chain: the unbroken sequence of pre-cooling, refrigerated storage and refrigerated "
    "transport that keeps perishable produce fresh from the farm gate to the retail shelf. A chain, as the name "
    "suggests, is only as useful as its weakest link. A cold store in a city is of little help if the produce has "
    "already spent eight hours in the sun on its way there. Much of the existing cold storage capacity, moreover, is "
    "concentrated in a few states and built for a single crop, the potato, which leaves growers of other perishables "
    "with few options.\n\n"
    "Building more warehouses is therefore not the whole answer. What farmers need most is small pre-cooling and "
    "storage units close to where crops are harvested, along with refrigerated vehicles that can carry produce to "
    "distant markets. Such units are expensive to run on unreliable grid power, which is why solar-powered cold rooms "
    "that can be shared by a village have attracted attention. Farmer producer organisations, which pool the output "
    "of many small growers, are better placed than individual farmers to fill such facilities and to bargain with "
    "buyers.\n\n"
    "Storage alone, however, does not guarantee a better price. A farmer who can hold back his tomatoes for two weeks "
    "gains only if he knows where and when prices will rise, and has the means to reach that market. Information, "
    "finance and logistics must therefore advance together. When they do, a cold chain does more than prevent waste: "
    "it gives the grower the one thing he has rarely had, the freedom to choose when to sell."))

Q(RC, "Factual", I,
  "According to the passage, why is much of the existing cold storage of limited use to many growers?",
  ["It is located only near ports.",
   "It is concentrated in a few states and built mainly for potatoes.",
   "It is too cheap to be maintained properly.",
   "It is reserved for produce meant for export."], "B",
  "Locating a stated fact",
  "Paragraph 2 says existing capacity 'is concentrated in a few states and built for a single crop, the potato, "
  "which leaves growers of other perishables with few options'.",
  ["Find 'existing cold storage capacity' in paragraph 2", "Two limits: few states, one crop (potato)",
   "Option B states both"],
  "Ports (A), low cost (C) and export (D) are not mentioned anywhere in the passage.", 60, P3, 1)

Q(RC, "Inference", I,
  "The statement 'A chain ... is only as useful as its weakest link' is used in the passage to suggest that",
  ["a single gap in the sequence can undo the benefit of all the other links",
   "cold stores in cities are unnecessary",
   "refrigerated trucks are the most important part of the chain",
   "farmers should avoid selling in distant markets"], "A",
  "Inference: understand the purpose of an image by reading the example that follows it",
  "The very next sentence gives the example: a city cold store is of little help if the produce has already spent "
  "eight hours in the sun. One broken link (no pre-cooling or cool transport) wastes the rest.",
  ["Read the example after the image", "Good storage at the end cannot save produce damaged earlier",
   "So one weak link spoils the whole chain: A"],
  "B overstates: the passage says a city store is of little help only when earlier links fail. C picks one link as "
  "most important, which the image denies. D contradicts the passage, which wants produce carried to distant "
  "markets.", 60, P3, 2)

Q(RC, "Factual", I,
  "Why, according to the passage, are farmer producer organisations well placed to use cold-chain facilities?",
  ["They receive free electricity from the grid.",
   "They own most of the cold stores in cities.",
   "They are allowed to fix retail prices.",
   "They pool the output of many growers, so they can fill facilities and bargain with buyers."], "D",
  "Locating a stated reason",
  "Paragraph 3 says these organisations 'pool the output of many small growers' and are therefore 'better placed "
  "than individual farmers to fill such facilities and to bargain with buyers'.",
  ["Find 'Farmer producer organisations' in paragraph 3", "Reason: pooling output",
   "Benefits: filling facilities, bargaining: D"],
  "A contradicts the passage, which calls grid power unreliable and costly. B and C are never mentioned.",
  60, P3, 3)

Q(RC, "Inference", I,
  "Which of the following can be inferred about a farmer who has access to storage but no information about "
  "markets?",
  ["He can safely ignore price movements.",
   "He will always earn more than a farmer without storage.",
   "He may gain little from storage, since he cannot tell when or where to sell profitably.",
   "He will no longer need any finance."], "C",
  "Inference from a conditional statement ('gains only if ...')",
  "Paragraph 4 says a farmer who holds back his produce 'gains only if he knows where and when prices will rise'. "
  "Without that knowledge, storage by itself may bring little benefit.",
  ["Key sentence: 'Storage alone ... does not guarantee a better price'",
   "Condition for gain: knowing where and when prices rise",
   "No information → the condition fails → little gain: C"],
  "A and B contradict 'gains only if he knows'. D contradicts the passage, which says information, finance and "
  "logistics must advance together.", 60, P3, 4)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'conservative' as used in the passage ('even "
  "conservative figures suggest')?",
  ["traditional", "cautious", "political", "exaggerated"], "B",
  "Vocabulary in context: a word with several meanings",
  "'Conservative figures' are deliberately low, cautious estimates. 'Even' cautious figures show a large loss, so "
  "the true loss may be larger still. 'Cautious' fits.",
  ["Context: estimates of loss vary", "'even conservative figures' = even the lowest, most careful estimates",
   "Meaning here: cautious"],
  "'Traditional' and 'political' are other senses of 'conservative' that do not fit figures. 'Exaggerated' is the "
  "opposite of the meaning here.", 45, P3, 5)

Q(RC, "Tone and title", I,
  "Which of the following is the most appropriate title for the passage?",
  ["Potatoes and the Politics of Storage", "Why Farmers Should Sell Early",
   "Solar Power in Rural India", "Keeping It Fresh: Why the Cold Chain Needs More Than Cold Stores"], "D",
  "A title must cover the whole passage",
  "The passage describes post-harvest loss, explains the cold chain, argues that small local units matter more than "
  "big warehouses and adds that information and finance are also needed. Option D captures the topic and the "
  "argument.",
  ["Para 1: losses; para 2: the cold chain and its gaps",
   "Para 3: more warehouses are not enough; para 4: information and finance too",
   "D covers all of this"],
  "A and C each pick up a single detail. B contradicts the conclusion, which values the freedom to choose when to "
  "sell.", 60, P3, 6)

# ---------------------------------------------------------------- RC 4 (Intermediate, 4)
P4 = stim("The missing middle", (
    "India's health financing has long had an odd shape. The poorest households are covered, at least on paper, by "
    "government-funded insurance schemes, while salaried employees in the formal sector usually receive a policy "
    "from their employer. Between these two groups lies a large population of shopkeepers, small traders, "
    "self-employed professionals and informal workers who are too well-off to qualify for free schemes but not "
    "well-off enough to feel that they can afford private cover. Policy researchers call them the 'missing "
    "middle'.\n\n"
    "For these households, a single hospital admission can wipe out years of savings. Yet many of them do not buy "
    "insurance even when a suitable policy is available at a modest premium. The reasons are partly financial and "
    "partly psychological. A premium is a certain cost paid today, while an illness is an uncertain event that may "
    "never happen, and people tend to give more weight to the first than to the second. Some also see an unused "
    "policy as money wasted, much as one might regret buying an umbrella in a year without rain. Others simply "
    "distrust insurers, having heard stories of claims rejected on technical grounds.\n\n"
    "Insurers have responded with cheaper products, shorter forms and cashless treatment at network hospitals, but "
    "take-up has risen only slowly. Experience from other countries suggests that what works best is a combination of "
    "measures: making enrolment simple, perhaps through a bank account or a mobile app; pooling small buyers into "
    "groups so that premiums fall; and settling claims quickly and transparently so that trust can be built over "
    "time.\n\n"
    "None of these steps is dramatic. Together, however, they address the real obstacle, which is less the price of a "
    "policy than the belief that it will be there when needed. A household that has seen a neighbour's claim paid "
    "without fuss is far more likely to buy a policy than one that has only seen an advertisement."))

Q(RC, "Factual", I,
  "Who, according to the passage, make up the 'missing middle'?",
  ["Households too well-off for free schemes but not confident that they can afford private cover",
   "Salaried employees of large firms in the formal sector",
   "The poorest households in villages",
   "Households covered by both government and employer insurance"], "A",
  "Locating a definition",
  "Paragraph 1 defines the group as those 'too well-off to qualify for free schemes but not well-off enough to feel "
  "that they can afford private cover'.",
  ["Find the term 'missing middle' at the end of paragraph 1", "Read the sentence before it: the definition",
   "Option A restates it"],
  "B and C are the two groups on either side of the missing middle, both of which have some cover. D describes no "
  "group in the passage.", 50, P4, 1)

Q(RC, "Inference", I,
  "The comparison with 'buying an umbrella in a year without rain' is meant to illustrate",
  ["that insurance premiums rise in bad years",
   "the feeling that a policy which is never claimed has been a waste of money",
   "that insurers reject claims on technical grounds",
   "that households should save instead of buying insurance"], "B",
  "Inference: the purpose of an analogy",
  "The sentence says some people 'see an unused policy as money wasted, much as one might regret buying an umbrella "
  "in a year without rain'. An unused umbrella, like an unclaimed policy, feels wasted, even though it was sensible "
  "protection.",
  ["Read the full sentence containing the analogy", "Unused umbrella ↔ unused policy",
   "Shared feeling: regret over money 'wasted': B"],
  "A: premiums are not discussed. C is a separate reason given in the next sentence. D is not the author's advice; "
  "the passage argues for more insurance.", 60, P4, 2)

Q(RC, "Factual", I,
  "Which of the following is NOT among the measures that, according to the passage, have worked best in other "
  "countries?",
  ["Making enrolment simple through a bank account or a mobile app",
   "Pooling small buyers into groups so that premiums fall",
   "Making insurance compulsory for all self-employed people",
   "Settling claims quickly and transparently"], "C",
  "Factual (NOT) question",
  "Paragraph 3 lists three measures: simple enrolment, pooling buyers into groups and quick, transparent claim "
  "settlement. Compulsion is never mentioned.",
  ["Find 'Experience from other countries' in paragraph 3", "Three measures follow the colon",
   "Compulsory insurance is not among them: C"],
  "A, B and D are the three measures listed in paragraph 3.", 50, P4, 3)

Q(RC, "Inference", I,
  "According to the author, the main obstacle to insurance take-up among these households is",
  ["the high price of premiums", "a shortage of network hospitals", "long and complicated forms",
   "doubt that the policy will actually pay out when it is needed"], "D",
  "Identifying the author's main claim ('the real obstacle')",
  "Paragraph 4 says the real obstacle 'is less the price of a policy than the belief that it will be there when "
  "needed'. The example of a neighbour's claim being paid shows that trust is what matters.",
  ["Find 'the real obstacle' in paragraph 4",
   "'less the price ... than the belief that it will be there when needed'",
   "So the obstacle is doubt about payment: D"],
  "A is explicitly ranked below trust ('less the price'). B and C are mentioned only as problems insurers have "
  "already addressed, without much effect.", 60, P4, 4)

# ---------------------------------------------------------------- RC 5 (Advanced, 4)
P5 = stim("The power of the default", (
    "Economics textbooks once assumed that people, given the right information, would make the choices that best "
    "served their long-term interests. If saving for retirement was sensible, rational workers would save. Decades "
    "of evidence have complicated that picture. People procrastinate, are swayed by how options are presented and, "
    "above all, tend to stick with whatever happens if they do nothing. This last tendency, the power of the "
    "default, has become one of the most studied ideas in public policy.\n\n"
    "Consider a pension scheme in which employees must fill in a form to join. Many who intend to enrol never get "
    "round to it, not because they have weighed the scheme and rejected it but because the form sits on a desk for "
    "months. Reverse the arrangement, so that employees are enrolled automatically unless they choose to opt out, and "
    "participation typically rises sharply, even though the scheme itself has not changed in the slightest. Nobody "
    "is forced to save; the path of least resistance has merely been redrawn.\n\n"
    "Supporters of such 'nudges' argue that they preserve freedom while correcting predictable lapses. Critics are "
    "less comfortable. A default, they point out, is never neutral: someone must choose it, and that someone may have "
    "interests of their own. A default contribution rate set too low may leave workers falsely reassured that they "
    "are saving enough; a default investment fund chosen for the provider's convenience may serve the provider "
    "better than the saver. There is also the question of consent. A choice that people make only because they did "
    "not notice they were making it is a curious kind of choice.\n\n"
    "The sensible conclusion is not to abandon defaults, which are unavoidable in any case, since every form must "
    "begin somewhere, but to design them with care and disclose them openly. If inertia is going to decide outcomes "
    "for millions of people, those who set the starting point bear a responsibility that is easy to underestimate "
    "precisely because it is so quiet."))

Q(RC, "Inference", A,
  "Why, according to the passage, does automatic enrolment raise participation even though the scheme is "
  "unchanged?",
  ["Workers are legally barred from leaving the scheme.",
   "Automatic enrolment comes with a higher rate of return.",
   "Many people who intend to join never act, and automatic enrolment turns their inaction into saving.",
   "Most non-participants had rejected the scheme after careful thought."], "C",
  "Inference: connect the example to the general tendency (inertia)",
  "Paragraph 2 says many who intend to enrol never do so because the form sits on a desk, not because they reject "
  "the scheme. When enrolment is automatic, the same inaction keeps them in. People 'stick with whatever happens if "
  "they do nothing'.",
  ["Paragraph 1: people stick with the default", "Paragraph 2: non-joiners are procrastinators, not rejecters",
   "Automatic enrolment makes doing nothing = saving: C"],
  "A contradicts 'unless they choose to opt out' and 'Nobody is forced to save'. B contradicts 'the scheme itself has "
  "not changed'. D is the opposite of what the passage says ('not because they have weighed the scheme and rejected "
  "it').", 75, P5, 1)

Q(RC, "Inference", A,
  "Which of the following statements would the critics mentioned in the passage most likely agree with?",
  ["Defaults should be banned from all public schemes.",
   "Whoever sets a default can shape outcomes in ways that may not serve the saver.",
   "Nudges take away workers' freedom to leave a scheme.",
   "People always make rational choices when they are given enough information."], "B",
  "Inference: extend a viewpoint without overstating it",
  "The critics say a default 'is never neutral: someone must choose it, and that someone may have interests of "
  "their own', and give examples of low contribution rates and provider-friendly funds. Option B summarises this "
  "concern.",
  ["Locate the critics' view in paragraph 3", "Core concern: the person who sets the default may not act for the saver",
   "Option B matches"],
  "A is too extreme; the critics question defaults but never call for a ban, and the author notes defaults are "
  "unavoidable. C misstates the scheme: workers can opt out. D is the old textbook assumption that the passage says "
  "has been 'complicated'.", 75, P5, 2)

Q(RC, "Tone and title", A,
  "The author's attitude towards defaults is best described as",
  ["cautiously accepting: defaults are unavoidable, but they must be designed carefully and disclosed",
   "enthusiastic and uncritical", "dismissive and hostile", "indifferent and detached"], "A",
  "Author's attitude: read the concluding paragraph",
  "The author rejects abandoning defaults ('unavoidable in any case') but insists they be designed 'with care' and "
  "disclosed 'openly', stressing the responsibility of those who set them. That is cautious acceptance.",
  ["Para 2 presents the benefit of defaults; para 3 presents the critics' concerns",
   "Para 4: keep defaults but design and disclose them carefully", "So: cautious acceptance: A"],
  "B ignores the author's warnings about responsibility. C ignores the author's view that defaults are unavoidable "
  "and useful. D does not fit an author who draws a firm conclusion and speaks of responsibility.", 60, P5, 3)

Q(RC, "Inference", A,
  "What does the author mean by saying that the responsibility of those who set defaults is 'easy to underestimate "
  "precisely because it is so quiet'?",
  ["The officials who set defaults rarely speak in public.",
   "Defaults affect only a small number of people.",
   "Pension providers deliberately hide their fees from savers.",
   "Defaults work unnoticed, so their large influence on outcomes is seldom recognised."], "D",
  "Inference: interpret figurative language in context",
  "A default decides outcomes for millions of people who simply do nothing; no one notices a decision being made. "
  "Because its influence is silent, people underestimate how much power the person who sets it holds.",
  ["Preceding clause: inertia decides outcomes 'for millions of people'",
   "'Quiet' = operating without notice", "Large influence + no notice = easily underestimated: D"],
  "A takes 'quiet' literally. B contradicts 'millions of people'. C introduces fees, which the passage never "
  "mentions.", 60, P5, 4)

# ---------------------------------------------------------------- RC 6 (Intermediate 1 + Advanced 3)
P6 = stim("A net or a hammock", (
    "Deposit insurance is one of the quiet foundations of modern banking. By promising that ordinary depositors will "
    "get their money back, up to a fixed limit, even if their bank fails, it removes the main reason for a bank run: "
    "the fear that those who wait in the queue will be left with nothing. A rumour that might once have emptied a "
    "sound bank in an afternoon now does far less damage, because small savers know their deposits are safe.\n\n"
    "Yet the same protection creates a subtler problem, which economists call moral hazard. When people are shielded "
    "from the consequences of a risk, they tend to take less care to avoid it. An insured depositor has little reason "
    "to ask whether her bank lends prudently, and a bank that knows its depositors will not desert it may be tempted "
    "to chase high returns through risky loans. The guarantee that prevents panic can thus weaken the discipline that "
    "would otherwise keep banks careful.\n\n"
    "Policymakers have tried to strike a balance. Coverage is usually capped, so that large depositors, who are "
    "better able to monitor a bank, still bear some risk. Banks pay premiums for the insurance, and some systems "
    "charge higher premiums to riskier banks, much as a careless driver pays more for motor insurance. Above all, "
    "deposit insurance is paired with regulation and supervision: if depositors no longer watch the banks closely, "
    "someone else must.\n\n"
    "The arrangement is therefore less a single safety net than a bargain. Society agrees to protect small savers "
    "from the failure of institutions they cannot be expected to understand; in return, banks accept rules on "
    "capital, liquidity and lending that limit their freedom to gamble with insured money. When either side of that "
    "bargain weakens, when coverage expands without matching supervision or when supervisors grow complacent, the "
    "safety net can quietly turn into a hammock."))

Q(RC, "Factual", I,
  "According to the passage, how does deposit insurance prevent bank runs?",
  ["It reassures small savers that their deposits are safe even if the bank fails, so they have no reason to rush "
   "to withdraw.",
   "It forbids depositors to withdraw money during a crisis.",
   "It guarantees depositors a higher rate of interest.",
   "It makes large depositors bear the entire risk of failure."], "A",
  "Locating a stated mechanism",
  "Paragraph 1 says insurance removes 'the main reason for a bank run: the fear that those who wait in the queue will "
  "be left with nothing', because small savers know their deposits are safe.",
  ["Cause of a run: fear that latecomers lose everything", "Insurance removes that fear",
   "So savers do not rush: A"],
  "B and C are never mentioned. D distorts paragraph 3: large depositors bear 'some' risk because coverage is "
  "capped, not the entire risk.", 50, P6, 1)

Q(RC, "Inference", A,
  "Which of the following is an example of moral hazard as the passage describes it?",
  ["A false rumour makes depositors queue outside a sound bank.",
   "A large depositor moves money out of a bank whose lending looks risky.",
   "A bank expands risky, high-return lending because it knows its insured depositors will not withdraw.",
   "A regulator raises the capital that banks must hold."], "C",
  "Applying a defined concept to a new case",
  "Moral hazard is taking less care because one is shielded from the consequences. Paragraph 2 says a bank that knows "
  "its depositors will not desert it 'may be tempted to chase high returns through risky loans'. Option C is that "
  "behaviour.",
  ["Definition: protection from a risk → less care to avoid it",
   "Who is protected? Depositors (insured) and so, indirectly, the bank's funding",
   "Option C shows the bank taking more risk because of that protection"],
  "A describes the panic that insurance prevents, not moral hazard. B shows market discipline, the opposite of moral "
  "hazard. D is a regulatory response to moral hazard.", 70, P6, 2)

Q(RC, "Inference", A,
  "According to the passage, why is deposit insurance coverage usually capped?",
  ["To make sure the insurer never runs out of funds",
   "So that large depositors, who can monitor banks better, still bear some risk",
   "To discourage wealthy people from saving in banks",
   "Because small savers do not need protection"], "B",
  "Answer from the passage's stated reason, not from outside knowledge",
  "Paragraph 3 gives the reason directly: coverage is capped 'so that large depositors, who are better able to "
  "monitor a bank, still bear some risk'. Their exposure keeps some market discipline alive.",
  ["Find 'Coverage is usually capped' in paragraph 3", "Read the 'so that' clause: the stated purpose",
   "Option B restates it"],
  "A may be true in the real world but is not the reason the passage gives. C misreads the purpose. D contradicts "
  "the passage, whose whole point is protecting small savers.", 60, P6, 3)

Q(RC, "Inference", A,
  "What does the author suggest by saying that the safety net can 'quietly turn into a hammock'?",
  ["Deposit insurance will eventually be withdrawn.",
   "Banks will become too small to fail.",
   "Depositors will stop earning interest on their savings.",
   "A protection meant to catch failures can instead encourage complacency and comfortable risk-taking."], "D",
  "Interpreting a concluding metaphor",
  "A safety net catches someone who falls; a hammock is something one lies back in comfortably. If supervision "
  "weakens, insurance stops being an emergency protection and becomes a comfort that lets banks and supervisors "
  "relax and take risks: the moral hazard of paragraph 2.",
  ["Net = catches failures; hammock = encourages relaxing",
   "The sentence names the conditions: coverage without supervision, complacent supervisors",
   "So protection turns into complacency: D"],
  "A, B and C read meanings into the metaphor that the passage never discusses (withdrawal of insurance, bank size, "
  "interest).", 60, P6, 4)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic, 5)
C1 = stim("The bicycle comes back", (
    "In many Indian cities, the bicycle was once the most common way to get to work. Mill workers, clerks and "
    "students rode to their (1) ______ every morning, and a bicycle was a prized possession that was passed down from "
    "parent to child. As incomes rose, however, the scooter and the car gradually (2) ______ it, and the cycle came "
    "to be seen as a sign of poverty rather than of good sense.\n\n"
    "Today, as traffic jams grow longer and the air in many cities becomes harder to breathe, planners are taking a "
    "fresh look at this simple machine. A bicycle produces no fumes, takes up little road space and costs almost "
    "nothing to run. Regular cycling also keeps the rider fit, which is a real (3) ______ at a time when lifestyle "
    "diseases are rising.\n\n"
    "The main obstacle is safety. Few people are willing to ride alongside speeding buses and trucks, and most roads "
    "offer no separate space for cyclists. Where cities have built protected cycle lanes and secure parking, the "
    "number of riders has (4) ______ quickly. Some cities have also introduced public bicycle-sharing schemes, under "
    "which a cycle can be hired at one station and returned at another for a small fee.\n\n"
    "Such schemes work best when they are (5) ______ to bus and metro stations, so that a commuter can ride the first "
    "and last kilometre of the journey. The bicycle will not replace the bus or the train, but it can make them far "
    "more useful. A city that makes room for cyclists, in short, makes room for everyone."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["vehicles", "destinations", "journeys", "accidents"], "B",
  "Cloze: what one rides 'to'",
  "Workers and students rode their bicycles to the places they had to reach every morning: their destinations "
  "(factories, offices, colleges).",
  ["The verb is 'rode to their ___'", "One rides to a place", "'destinations' is the only place word"],
  "One does not ride 'to' one's vehicles, journeys or accidents; none of these is a place reached every morning.",
  35, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["rescued", "repaired", "rented", "replaced"], "D",
  "Cloze: the contrast set up by 'however'",
  "The bicycle was once the most common vehicle; 'however', as incomes rose, scooters and cars took its place and it "
  "came to be seen as a sign of poverty. 'Replaced' expresses this.",
  ["'However' signals a change from the bicycle's earlier popularity",
   "Scooters and cars took its place", "'gradually replaced it'"],
  "'Rescued' and 'repaired' would be positive actions on the bicycle, which do not explain its fall in status. "
  "'Rented' makes no sense with scooters and cars as the subject.", 35, C1, 2)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=3), ["advantage", "burden", "expense", "risk"], "A",
  "Cloze: tone of the paragraph (benefits of cycling)",
  "The paragraph lists the bicycle's benefits: no fumes, little road space, low cost. Keeping riders fit when "
  "lifestyle diseases are rising is another benefit, so 'advantage' fits.",
  ["The paragraph lists positives", "Fitness during a rise in lifestyle diseases is a positive",
   "'a real advantage'"],
  "'Burden', 'expense' and 'risk' are negatives and contradict the list of benefits.", 35, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["fallen", "stopped", "risen", "frozen"], "C",
  "Cloze: cause and effect",
  "Safety is the main obstacle. Where cities removed it with protected lanes and parking, more people started "
  "cycling: the number of riders 'has risen quickly'.",
  ["Obstacle: lack of safety", "Protected lanes and parking remove the obstacle",
   "Result: more riders: 'risen'"],
  "'Fallen' reverses the effect of safer roads. 'Stopped' and 'frozen' do not go with 'quickly' and make no sense "
  "as a result of better facilities.", 35, C1, 4)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=5), ["opposed", "unknown", "linked", "closed"], "C",
  "Cloze: 'so that' gives the purpose",
  "Sharing schemes help a commuter ride 'the first and last kilometre' to and from a bus or metro station. That works "
  "only if the cycle stations are linked to bus and metro stations.",
  ["Purpose clause: 'so that a commuter can ride the first and last kilometre'",
   "The cycle must connect with the bus or metro", "'linked to'"],
  "'Opposed to', 'unknown to' and 'closed to' would all prevent commuters from using the bicycles with buses and "
  "trains, defeating the purpose stated after 'so that'.", 35, C1, 5)

# ---------------------------------------------------------------- Cloze 2 (Basic 3 + Intermediate 2)
C2 = stim("Weavers on the web", (
    "For generations, handloom weavers in India sold their saris and fabrics through middlemen who bought cheaply in "
    "the village and sold at a large profit in the city. The weaver, who might spend weeks on a single piece, rarely "
    "knew what the final buyer paid for it. Online marketplaces and social media have begun to (1) ______ this "
    "pattern. A weaver with a smartphone can now photograph her work, describe how it was made and sell it directly "
    "to a customer hundreds of kilometres away.\n\n"
    "The benefits can be (2) ______. Weavers who sell directly report earning noticeably more per piece, and some "
    "have built a loyal following among buyers who value the story behind each product. Customers, for their part, "
    "gain access to genuine handwoven goods instead of cheaper machine-made (3) ______ that are often passed off as "
    "handloom.\n\n"
    "Selling online, however, brings new demands. Photographs must be clear, descriptions accurate and parcels packed "
    "so that delicate fabric is not damaged. Payments, returns and customer queries must be handled promptly, and a "
    "single bad review can (4) ______ sales for weeks. Many weavers, especially older ones, find these tasks "
    "daunting and continue to depend on intermediaries.\n\n"
    "Weavers' cooperatives and a few non-profit groups are trying to meet this need by offering training in "
    "photography, digital payments and basic bookkeeping, and by handling packing and dispatch collectively. Their "
    "experience suggests that technology works best when it is (5) ______ by support on the ground. A website can "
    "open a door, but someone still has to help the weaver walk through it."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["change", "repeat", "protect", "admire"], "A",
  "Cloze: the new development contrasts with the old pattern",
  "The old pattern was selling through middlemen. Online selling lets weavers sell directly, so it has begun to "
  "change that pattern.",
  ["Old pattern: middlemen take the profit", "New: weavers sell directly online",
   "Online selling changes the pattern: 'change'"],
  "'Repeat' and 'protect' would keep the middleman system, which the next sentence shows is being bypassed. "
  "'Admire' makes no sense with 'this pattern' here.", 35, C2, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["negligible", "substantial", "imaginary", "harmful"], "B",
  "Cloze: the sentences that follow decide the word",
  "The next sentences describe clear gains: noticeably higher earnings, loyal buyers and genuine goods for customers. "
  "So the benefits are 'substantial'.",
  ["Read ahead: 'earning noticeably more per piece', 'a loyal following'",
   "These are large, real gains", "'substantial'"],
  "'Negligible' and 'imaginary' deny the gains that follow. 'Harmful' contradicts the word 'benefits'.", 35, C2, 2)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=3), ["machines", "originals", "weavers", "imitations"], "D",
  "Cloze: contrast between genuine and fake goods",
  "Customers get 'genuine handwoven goods instead of cheaper machine-made imitations that are often passed off as "
  "handloom'. Something 'passed off' as handloom is an imitation.",
  ["Contrast: genuine handwoven vs ___", "'passed off as handloom' = pretending to be handloom",
   "So the word is 'imitations'"],
  "'Machines' are not sold as fabric. 'Originals' contradicts 'passed off as'. 'Weavers' are people, not goods.",
  35, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["boost", "double", "hurt", "fix"], "C",
  "Cloze: the paragraph lists difficulties",
  "The paragraph describes the demands and risks of selling online. A single bad review is one such risk: it can "
  "hurt sales for weeks.",
  ["Paragraph tone: 'brings new demands', 'daunting'", "A bad review has a negative effect",
   "'hurt sales for weeks'"],
  "'Boost' and 'double' are positive effects, which a bad review does not cause. 'Fix sales for weeks' is "
  "meaningless here.", 40, C2, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["replaced", "backed", "opposed", "delayed"], "B",
  "Cloze: the closing image explains the blank",
  "Cooperatives give training and handle packing alongside online selling. The lesson is that technology works best "
  "when it is backed (supported) by help on the ground, which the final sentence repeats: a website opens a door, "
  "but someone must help the weaver through it.",
  ["Cooperatives add human support to the technology", "Technology + support together work best",
   "'backed by support on the ground'"],
  "'Replaced by support' would remove the technology, but the final sentence keeps the website. 'Opposed' and "
  "'delayed' contradict the cooperatives' helpful role.", 40, C2, 5)

# ---------------------------------------------------------------- Cloze 3 (Intermediate, 5)
C3 = stim("Learning by doing", (
    "Every year, millions of young Indians finish school or college with a certificate but little idea of how a "
    "workplace actually functions. Employers, in turn, complain that graduates lack practical skills and must be "
    "trained almost from scratch. Apprenticeships, in which a young person learns a trade by working under "
    "experienced staff while earning a stipend, offer a way to (1) ______ young people with real experience before "
    "they enter the job market.\n\n"
    "The idea is old. Carpenters, goldsmiths and tailors have always learned by watching and assisting a master. What "
    "is new is the attempt to make apprenticeships a formal (2) ______ to employment across industries, from retail "
    "and hospitality to banking and manufacturing. For the apprentice, the arrangement offers income, experience and "
    "a credential that employers recognise. For the firm, it offers a chance to train future staff in its own methods "
    "and to judge their ability before making a permanent offer.\n\n"
    "Yet the numbers remain modest compared with the size of the workforce. Small firms, which employ most workers, "
    "often find the paperwork (3) ______ and fear that an apprentice will leave as soon as the training is complete. "
    "Some larger firms, meanwhile, have been accused of using apprentices as cheap labour, assigning them routine "
    "tasks that teach them little.\n\n"
    "Making the system work will require simpler rules, so that a small workshop can take on an apprentice without "
    "hiring a consultant, and closer (4) ______ of what apprentices actually learn. Industry bodies can help by "
    "designing short, practical courses and by certifying skills in a way that is recognised across firms. An "
    "apprenticeship that ends with a certificate no one trusts is little better than a degree no one values. If these "
    "conditions are met, apprenticeships could become one of the most (5) ______ routes into work for young people "
    "who want to learn by doing."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["deprive", "provide", "threaten", "charge"], "B",
  "Cloze: verb pattern 'provide someone with something'",
  "Apprenticeships give young people practical experience, which they otherwise lack. 'Provide young people with "
  "real experience' fits both the meaning and the preposition 'with'.",
  ["Problem in the paragraph: graduates lack practical skills", "Apprenticeships solve it by giving experience",
   "Pattern: provide + person + with + thing"],
  "'Deprive' means the opposite and takes 'of'. 'Threaten young people with experience' and 'charge young people "
  "with experience' are illogical here.", 40, C3, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["pathway", "barrier", "substitute", "obstacle"], "A",
  "Cloze: noun + 'to employment'",
  "The paragraph presents apprenticeships as a route into jobs: income, a recognised credential and a chance of a "
  "permanent offer. 'A formal pathway to employment' fits.",
  ["Apprenticeships lead to jobs (permanent offer)", "The noun must mean a route",
   "'pathway to employment'"],
  "'Barrier' and 'obstacle' would mean apprenticeships block jobs, which contradicts the paragraph. 'Substitute' "
  "takes 'for' and would mean apprenticeships replace employment.", 40, C3, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["rewarding", "simple", "optional", "burdensome"], "D",
  "Cloze: a reason for low uptake by small firms",
  "The paragraph explains why numbers stay modest. Small firms find the paperwork burdensome; the last paragraph "
  "confirms this by calling for simpler rules so a workshop need not hire a consultant.",
  ["Paragraph topic: why few firms take apprentices", "Paperwork must be a deterrent",
   "Confirmed later: 'simpler rules ... without hiring a consultant': 'burdensome'"],
  "'Rewarding' and 'simple' would encourage firms, not deter them. 'Optional' paperwork would not be a problem "
  "either.", 40, C3, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["neglect", "imitation", "monitoring", "celebration"], "C",
  "Cloze: a remedy for the problem described earlier",
  "Paragraph 3 says some firms use apprentices as cheap labour on tasks that teach little. The remedy is closer "
  "monitoring of what apprentices actually learn.",
  ["Problem: apprentices learn little in some firms", "Remedy: check what they learn",
   "'closer monitoring of what apprentices actually learn'"],
  "'Closer neglect' is self-contradictory and would worsen the problem. 'Imitation' and 'celebration' of what "
  "apprentices learn do not address it.", 40, C3, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["neglected", "costly", "uncertain", "promising"], "D",
  "Cloze: 'If these conditions are met' signals a positive outcome",
  "The sentence describes what happens once the problems are fixed, so the outcome must be positive: apprenticeships "
  "could become one of the most promising routes into work.",
  ["Condition: the fixes in this paragraph are made", "Outcome must be good", "'most promising routes'"],
  "'Neglected', 'costly' and 'uncertain' are negative outcomes, which do not follow from meeting the conditions.",
  40, C3, 5)

# ---------------------------------------------------------------- Cloze 4 (Intermediate 3 + Advanced 1)
C4 = stim("Too many visitors", (
    "Every summer, the roads leading to popular hill towns fill with cars, and towns built for a few thousand "
    "residents find themselves hosting many times that number of visitors. Hotels are booked out, water tankers run "
    "day and night, and garbage piles up faster than the local body can (1) ______ it. What was once a quiet retreat "
    "begins to resemble the crowded city the tourists came to escape.\n\n"
    "Tourism is, of course, a vital source of income for these regions, where farming is difficult and industry "
    "scarce. The problem is not tourism itself but its (2) ______: too many visitors arriving in the same few weeks, "
    "staying in the same few places and making demands that fragile mountain slopes cannot bear. Unplanned "
    "construction of hotels on steep slopes has made some towns more (3) ______ to landslides, and the loss of forest "
    "cover has worsened the damage caused by heavy rain.\n\n"
    "Some local governments have begun to experiment with limits. A few have introduced permits for vehicles entering "
    "ecologically sensitive areas, while others charge a small green fee whose proceeds are spent on waste "
    "management. Promoting lesser-known destinations and off-season travel can also spread visitors more evenly "
    "through the year.\n\n"
    "Such measures are rarely popular at first. Hotel owners worry about losing business, and visitors resent paying "
    "for what was once free. But the alternative is a slow decline in which the very beauty that draws tourists is "
    "(4) ______ by their numbers. A hill town that protects its forests, water and slopes is not turning tourists "
    "away; it is making sure there will still be something worth visiting in twenty years."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["clear", "count", "produce", "admire"], "A",
  "Cloze: the job a local body does with garbage",
  "Garbage 'piles up faster than the local body can clear it': the municipality removes garbage, and crowds create it "
  "faster than it can be removed.",
  ["Problem: garbage piling up", "The local body's role: removing it", "'clear it'"],
  "A local body does not 'produce' or 'admire' garbage. 'Count it' does not explain why garbage piles up.",
  40, C4, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["absence", "concentration", "cost", "taxation"], "B",
  "Cloze: the explanation after the colon defines the word",
  "After the colon, the passage explains the problem: too many visitors in the same few weeks and the same few "
  "places. That is the concentration of tourism in time and space.",
  ["Read after the colon: 'same few weeks', 'same few places'", "Crowding in time and place = concentration",
   "'its concentration'"],
  "'Absence' contradicts the crowds. 'Cost' and 'taxation' are not what the colon goes on to describe.", 45, C4, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["immune", "resistant", "vulnerable", "indifferent"], "C",
  "Cloze: 'more ___ to landslides' after unplanned construction",
  "Building hotels on steep slopes weakens them, so towns become more vulnerable (exposed) to landslides. The next "
  "clause about worsened damage confirms the negative effect.",
  ["Unplanned construction on slopes is harmful", "Harm → greater exposure to landslides",
   "'more vulnerable to landslides'"],
  "'Immune' and 'resistant' reverse the effect of unplanned building. 'Indifferent to landslides' describes an "
  "attitude, which a town cannot have.", 40, C4, 3)

Q(CL, "Single-blank cloze", A, CLOZE_STEM.format(n=4), ["sustained", "magnified", "showcased", "eroded"], "D",
  "Cloze: 'a slow decline in which ...' requires a word of gradual damage",
  "The alternative to limits is 'a slow decline', in which the beauty that draws tourists is gradually worn away by "
  "crowds. 'Eroded' means worn away little by little and matches 'slow decline'.",
  ["Frame: 'a slow decline in which the very beauty ... is ___ by their numbers'",
   "Decline → the beauty is being lost", "Gradual loss → 'eroded'"],
  "'Sustained', 'magnified' and 'showcased' all mean the beauty is kept or increased, which contradicts 'a slow "
  "decline' and the irony in 'the very beauty that draws tourists'.", 50, C4, 4)

# ---------------------------------------------------------------- Cloze 5 (Advanced, 4; error-based)
C5 = stim("What your deposit really earns", (
    "For millions of households, a fixed deposit is the simplest way to save. The interest rate printed on the "
    "deposit receipt, however, can be **(1) misleading**. What matters to a saver is not the nominal rate but the real "
    "rate: the return left after inflation has been taken into account. If a deposit earns seven per cent a year "
    "while prices rise by six per cent, the saver's purchasing power grows by only about one per cent, and if "
    "inflation **(2) falls** above the deposit rate, the saver is in effect becoming poorer every year even as the "
    "balance on paper keeps rising.\n\n"
    "This distinction matters most for those who depend on interest income, such as retired people. When inflation "
    "is high and deposit rates lag behind, they face an uncomfortable choice: accept a **(3) gain** in their real "
    "income or move their savings into riskier assets in search of higher returns. Many choose the second path "
    "without fully understanding the risks, which is one reason why the mis-selling of complex products tends to rise "
    "when real rates are **(4) generous**.\n\n"
    "Tax adds another layer. Interest on deposits is generally taxed as income, so the post-tax real return can be "
    "lower still, or even negative for savers in higher tax brackets. A saver who looks only at the headline rate "
    "may therefore greatly overestimate how much her money is really earning.\n\n"
    "None of this means that deposits are a poor choice; they remain safe, liquid and easy to understand. It does "
    "mean that savers should judge them by the right yardstick. The question to ask is not 'How much interest will I "
    "get?' but 'How much more will my money be able to buy at the end of the year?'"))

Q(CL, "Error-based cloze", A, ERR_STEM.format(n=1, ctx="The interest rate printed on the deposit receipt, however, can be misleading"), ["accurate", "reassuring", "transparent", NR], "D",
  "Error-based cloze: 'however' and the next sentence show the bold word is right",
  "The printed rate 'can be misleading' because, as the next sentence says, what matters is the real rate after "
  "inflation. A saver who sees only the nominal rate is misled. The word is correct as it stands.",
  ["'however' contrasts the simple deposit with a hidden catch",
   "Next sentence: nominal rate ≠ real rate", "So the printed rate can mislead: no replacement needed"],
  "'Accurate', 'reassuring' and 'transparent' remove the contrast signalled by 'however' and contradict the "
  "passage's point that the printed rate hides the effect of inflation.", 50, C5, 1)

Q(CL, "Error-based cloze", A, ERR_STEM.format(n=2, ctx="if inflation falls above the deposit rate, the saver is in effect becoming poorer every year"), ["drops", "rises", "rising", NR], "B",
  "Error-based cloze: meaning and collocation ('rise above')",
  "The saver becomes poorer when inflation goes higher than the deposit rate. Inflation 'rises above' the deposit "
  "rate; 'falls above' is self-contradictory.",
  ["Condition for becoming poorer: inflation > deposit rate", "Movement upward past a level: 'rises above'",
   "Finite verb needed after 'if inflation': 'rises'"],
  "'Drops' repeats the error of 'falls'. 'Rising' is a participle and cannot be the main verb of the 'if' clause. "
  "'Falls' is wrong, so 'No replacement required' does not apply.", 50, C5, 2)

Q(CL, "Error-based cloze", A, ERR_STEM.format(n=3, ctx="they face an uncomfortable choice: accept a gain in their real income or move their savings into riskier assets"), ["rise", "boost", "decline", NR], "C",
  "Error-based cloze: an 'uncomfortable choice' must involve a loss",
  "When inflation is above deposit rates, savers relying on interest lose purchasing power. Their uncomfortable "
  "choice is to accept a decline in real income or take on risk. 'Gain' makes the choice comfortable, so it is "
  "wrong.",
  ["Context: inflation high, deposit rates lag behind → real income falls",
   "'uncomfortable choice' between two bad options", "Replace 'gain' with 'decline'"],
  "'Rise' and 'boost' repeat the error of 'gain'. 'Gain' itself is wrong, so 'No replacement required' does not "
  "apply.", 50, C5, 3)

Q(CL, "Error-based cloze", A, ERR_STEM.format(n=4, ctx="the mis-selling of complex products tends to rise when real rates are generous"), ["low", "high", "attractive", NR], "A",
  "Error-based cloze: link the effect back to its cause",
  "Savers move into risky products when deposits fail to beat inflation, i.e. when real rates are low. So mis-selling "
  "rises when real rates are low, not 'generous'.",
  ["Cause of risk-taking in this paragraph: deposits lag behind inflation", "That means real rates are low",
   "Replace 'generous' with 'low'"],
  "'High' and 'attractive' repeat the error: with good real returns, savers would have no reason to chase risk. "
  "'Generous' is wrong, so 'No replacement required' does not apply.", 55, C5, 4)

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


ed("Part-wise error", B, "Both the branch manager", "as well as the cashier", "attended the training session.", "B",
   "'Both' pairs with 'and', not 'as well as'",
   "The correlative is 'both ... and': 'Both the branch manager and the cashier attended the training session.' "
   "'Both ... as well as' is incorrect.",
   ["Spot the correlative opener 'Both' in part A", "Its partner must be 'and'",
    "'as well as' → 'and': error in part B"],
   "Part A is a correct subject opener and part C has a correct past-tense verb with its object. Since B has an "
   "error, 'No error' is wrong.", 30)

ed("Part-wise error", B, "We discussed about", "the new crop loan scheme", "at yesterday's meeting.", "A",
   "'Discuss' is a transitive verb and takes a direct object (no 'about')",
   "One 'discusses something', not 'discusses about something'. The correct form is 'We discussed the new crop loan "
   "scheme at yesterday's meeting.'",
   ["Check the verb in part A: 'discussed'", "'Discuss' takes a direct object", "Remove 'about': error in part A"],
   "Part B is a correct noun phrase and part C a correct time phrase. A has an error, so 'No error' is wrong.", 30)

ed("Part-wise error", B, "This year the bank has recruited", "less officers than", "it did last year.", "B",
   "'Fewer' with countable plural nouns; 'less' with uncountable nouns",
   "'Officers' can be counted, so the sentence needs 'fewer officers than it did last year'. 'Less' is used with "
   "uncountable nouns such as 'less money'.",
   ["Noun after the quantifier: 'officers' (countable, plural)", "Countable plural → 'fewer'",
    "'less officers' → 'fewer officers': error in part B"],
   "Part A uses the present perfect correctly with 'This year' (a period not yet over). Part C correctly uses 'did' "
   "to stand for 'recruited'. B has an error, so 'No error' is wrong.", 30)

ed("Part-wise error", B, "The agent who cheated", "the villagers has been arrested,", "and the police has filed a case.",
   "C",
   "'Police' is a plural noun and takes a plural verb",
   "'Police' is always treated as plural: 'the police have filed a case'. The singular 'has' is wrong.",
   ["Part B: 'The agent ... has been arrested': singular subject, singular verb, correct",
    "Part C: subject 'the police' is plural", "'has filed' → 'have filed': error in part C"],
   "Part A correctly uses 'who' for a person. In part B, 'has' agrees with 'The agent', not with 'villagers'. C has "
   "an error, so 'No error' is wrong.", 35)

ed("Error-free sentence", B, "Would you mind waiting", "for a few minutes while", "I check your account details?", "D",
   "'Mind' takes a gerund; 'while' + present simple for a simultaneous action",
   "The sentence is correct. 'Would you mind' is followed by the gerund 'waiting', 'for a few minutes' is a correct "
   "duration phrase, and 'while I check' correctly uses the present simple for an action happening at the same time.",
   ["Part A: 'mind' + -ing form: correct", "Part B: 'for' + period of time; 'while' as a linker: correct",
    "Part C: present simple after 'while': correct", "No error: option D"],
   "Each of parts A, B and C is correct, as shown in the steps, so none of them is the answer.", 30)

ed("Part-wise error", I, "If the borrower would have", "submitted the documents on time,",
   "his loan would have been approved.", "A",
   "Third conditional: 'If' + past perfect, main clause 'would have' + past participle",
   "In a past unreal condition, 'would have' belongs only in the main clause. The 'if' clause takes the past "
   "perfect: 'If the borrower had submitted the documents on time, his loan would have been approved.'",
   ["Main clause (part C) uses 'would have been approved': third conditional",
    "The 'if' clause must use the past perfect", "'would have' → 'had': error in part A"],
   "Part B is the correct continuation once A is fixed, and part C is the correct main clause of a third "
   "conditional. A has an error, so 'No error' is wrong.", 40)

ed("Part-wise error", I, "The new manager is looking forward", "to meet the members of",
   "the local self-help groups.", "B",
   "'Look forward to' + gerund ('to' is a preposition here)",
   "In 'look forward to', 'to' is a preposition, so it is followed by the -ing form: 'looking forward to meeting the "
   "members'.",
   ["Phrase: 'look forward to'", "'to' here is a preposition, not part of an infinitive",
    "Preposition + gerund: 'to meeting': error in part B"],
   "Part A correctly uses the present continuous. Part C is a correct noun phrase. B has an error, so 'No error' is "
   "wrong.", 35)

ed("Part-wise error", I, "Two employees of the branch", "have been suspended after being",
   "accused for forging signatures.", "C",
   "Fixed preposition: 'accused of' (not 'for')",
   "The verb 'accuse' takes 'of': 'accused of forging signatures'. ('Charged with' and 'blamed for' are different "
   "verbs.)",
   ["Find the verb + preposition pair: 'accused for'", "Correct pairing: accuse someone of something",
    "'for' → 'of': error in part C"],
   "Part A is a correct plural subject and part B a correct passive with a plural verb and 'after being'. C has an "
   "error, so 'No error' is wrong.", 35)

ed("Part-wise error", A, "Many a customer", "have complained about", "the long queues at the branch.", "B",
   "'Many a' + singular noun takes a singular verb",
   "Although 'many a customer' refers to many people, grammatically it is singular: 'Many a customer has complained "
   "about the long queues.'",
   ["Subject: 'Many a customer'", "'Many a' is always followed by a singular noun and a singular verb",
    "'have' → 'has': error in part B"],
   "Part A is the correct form of the subject ('many a' + singular). Part C is a correct prepositional phrase. B has "
   "an error, so 'No error' is wrong.", 40)

ed("Part-wise error", A, "The officer whom we thought", "was responsible for the delay",
   "turned out to be on leave that week.", "A",
   "Who vs whom: the pronoun is the subject of 'was', so it must be 'who'",
   "Remove the inserted 'we thought': 'The officer who was responsible for the delay'. The pronoun is the subject of "
   "'was', so 'who' is required: 'The officer who we thought was responsible ...'.",
   ["Test by removing 'we thought'", "The pronoun becomes the subject of 'was responsible'",
    "Subject form: 'who', not 'whom': error in part A"],
   "Part B correctly continues the relative clause with 'was', and part C is a correct main verb phrase. A has an "
   "error, so 'No error' is wrong.", 45)

ed("Part-wise error", A, "The more carefully a bank checks", "a borrower's credit history,",
   "lesser is the chance of a default.", "C",
   "Comparative correlative: 'The more ..., the + comparative ...'",
   "A sentence beginning 'The more ...' must continue with 'the' + comparative in the second half: 'the smaller the "
   "chance of a default' (or 'the less likely a default'). 'Lesser is the chance' breaks the pattern, and 'lesser' is "
   "not used for amounts or chances in this way.",
   ["Part A opens the pattern 'The more ...'", "Second half must be 'the + comparative': 'the smaller the chance'",
    "'lesser is the chance' is wrong: error in part C"],
   "Part A correctly uses 'The more carefully' and part B is a correct object phrase. C has an error, so 'No error' "
   "is wrong.", 45)

ed("Part-wise error", A, "The board has approved", "the proposal, but neither the chief executive",
   "or the finance head has signed it yet.", "C",
   "Correlative pair: 'neither ... nor'",
   "'Neither' must be paired with 'nor': 'neither the chief executive nor the finance head has signed it yet'. The "
   "singular verb 'has' is correct because both subjects are singular.",
   ["Part B contains 'neither'", "Its partner must be 'nor', not 'or'",
    "'or' → 'nor': error in part C (the verb 'has' is fine)"],
   "Part A uses a correct present perfect. Part B correctly opens the correlative. C has an error, so 'No error' is "
   "wrong.", 40)

ed("Error-free sentence", A, "Not until the audit was completed", "did the board realise",
   "how large the losses were.", "D",
   "Inversion after a negative opening ('Not until ...' + auxiliary + subject); embedded question in statement order",
   "The sentence is correct. A sentence starting with 'Not until ...' inverts the main clause ('did the board "
   "realise'), and the embedded question 'how large the losses were' correctly keeps statement word order.",
   ["Part A: 'Not until' + a complete time clause: correct",
    "Part B: inversion 'did the board realise': correct after 'Not until'",
    "Part C: embedded question in statement order ('the losses were'): correct", "No error: option D"],
   "A is a correct time clause, B shows the required inversion, and C correctly avoids question order ('how large "
   "were the losses') inside a statement. None of them contains an error.", 45)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", B,
  SI_STEM + "Most young customers **prefer using the app than visiting** the branch.",
  ["prefer to using the app than visiting", "prefer using the app to visiting",
   "are preferring using the app than visiting", NI], "B",
  "'Prefer A to B' (not 'prefer A than B')",
  "With 'prefer' + gerund, the thing preferred is compared using 'to': 'prefer using the app to visiting the "
  "branch'.",
  ["The comparison word after 'prefer' is 'to', not 'than'", "Keep both gerunds parallel: using ... visiting",
   "'prefer using the app to visiting'"],
  "A puts 'to' in the wrong place and keeps 'than'. C keeps 'than' and wrongly uses 'prefer' in the continuous form "
  "for a general preference. The original uses 'than', so 'No improvement required' is wrong.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "The new clerk **cannot cope up with** the pressure of the month-end closing.",
  ["cannot cope with", "cannot cope up to", "cannot coping up with", NI], "A",
  "'Cope with' (no 'up')",
  "The verb is 'cope with': 'The new clerk cannot cope with the pressure.' 'Cope up with' is a common error.",
  ["The phrasal verb is 'cope with'", "Remove the extra 'up'", "'cannot cope with'"],
  "B keeps 'up' and uses the wrong preposition. C keeps 'up' and uses '-ing' after 'cannot'. The original is wrong, "
  "so 'No improvement required' does not apply.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "It is two years **since he has joined** the bank as a probationary officer.",
  ["since he had joined", "since he joined", "for he joined", NI], "B",
  "'It is + period + since + simple past'",
  "In the pattern 'It is two years since ...', the 'since' clause names a past event and takes the simple past: 'It "
  "is two years since he joined the bank.'",
  ["Pattern: It is [period] since [past event]", "The past event takes the simple past", "'since he joined'"],
  "A uses the past perfect, which needs another past reference point. C replaces 'since' with 'for', which cannot "
  "introduce a clause here. The present perfect in the original is wrong, so 'No improvement required' does not "
  "apply.", 35)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "Looking at the long queue today, I wish I **had applied** for the online account last year.",
  ["applied", "have applied", "would apply", NI], "D",
  "'Wish' + past perfect for a regret about the past",
  "The regret concerns a past action ('last year'), so 'wish' takes the past perfect: 'I wish I had applied ...'. "
  "The sentence is already correct.",
  ["Time of the wished-for action: last year (past)", "Regret about the past: wish + past perfect",
   "'had applied' is correct: no improvement"],
  "'Applied' (simple past) after 'wish' expresses a present wish, which clashes with 'last year'. 'Have applied' "
  "and 'would apply' are not used after 'wish' for a past regret.", 35)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "She **has been knowing** the branch manager for more than ten years.",
  ["is knowing", "knows", "has known", NI], "C",
  "Stative verbs ('know') are not used in continuous forms",
  "'Know' describes a state, not an action, so it does not take the continuous. With 'for more than ten years', the "
  "present perfect is needed: 'She has known the branch manager for more than ten years.'",
  ["'know' is a stative verb: no -ing form", "Duration up to now ('for ... years') → present perfect",
   "'has known'"],
  "'Is knowing' is a continuous form of a stative verb. 'Knows' (present simple) does not go with 'for more than ten "
  "years'. The original is wrong, so 'No improvement required' does not apply.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "It is getting late, so we **had better to leave** before the roads are flooded.",
  ["had better to leaving", "would better leave", "had better leave", NI], "C",
  "'Had better' + bare infinitive (no 'to')",
  "'Had better' is followed by the base form of the verb without 'to': 'we had better leave before the roads are "
  "flooded'.",
  ["'had better' works like a modal", "Modal + base form, no 'to'", "'had better leave'"],
  "A adds 'to' and an -ing form. 'Would better' is not an English expression. The original wrongly uses 'to', so 'No "
  "improvement required' does not apply.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "The auditor **suggested him to check** all the vouchers again.",
  ["suggested him for checking", "suggested that he should check", "suggested to him to check", NI], "B",
  "'Suggest' does not take object + to-infinitive; use a 'that' clause",
  "'Suggest' cannot be followed by 'him to check'. The standard pattern is a 'that' clause: 'The auditor suggested "
  "that he should check all the vouchers again.'",
  ["'suggest + object + to-infinitive' is not standard", "Use 'suggest that + subject + should + verb'",
   "'suggested that he should check'"],
  "'Suggested him for checking' and 'suggested to him to check' are both unidiomatic. The original is wrong, so 'No "
  "improvement required' does not apply.", 35)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "She is one of those officers **who has always refused** to cut corners.",
  ["who have always refused", "which has always refused", "who is always refusing", NI], "A",
  "In 'one of those + plural noun + who', the relative pronoun refers to the plural noun",
  "The relative clause describes 'those officers' (the group that refuses to cut corners); she is one of them. "
  "'Who' therefore takes a plural verb: 'one of those officers who have always refused'.",
  ["Antecedent of 'who': 'those officers' (plural)", "Plural antecedent → plural verb 'have'",
   "'who have always refused'"],
  "B uses 'which' for people and keeps the singular verb. C keeps the singular verb and changes the meaning to an "
  "ongoing action. The original is wrong, so 'No improvement required' does not apply.", 45)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "**Had the bank informed earlier**, it could have blocked the stolen card at once.",
  ["If the bank had informed earlier", "Had the bank being informed earlier", "Had the bank been informed earlier",
   NI], "C",
  "Inverted third conditional with a passive verb ('Had + subject + been + V3')",
  "The bank did not inform anyone; it should have been informed. The passive is needed, and the inverted conditional "
  "is 'Had + subject + been + past participle': 'Had the bank been informed earlier, it could have blocked the "
  "card.'",
  ["Who informs whom? The customer informs the bank, so the bank is the receiver: passive",
   "Inverted third conditional: Had + subject + past participle", "Passive: 'Had the bank been informed'"],
  "A keeps the active 'had informed', which leaves 'inform' without an object and wrongly makes the bank the "
  "informer. B uses 'being' instead of 'been'. The original is wrong, so 'No improvement required' does not "
  "apply.", 45)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", I,
  PR_STEM + "The manager **called off** the review meeting because half the members were absent.",
  ["called on", "called for", "called in", NR], "D",
  "Phrasal verbs with 'call': call off = cancel",
  "Half the members were absent, so the meeting was cancelled. 'Called off' means cancelled, which fits exactly.",
  ["Context: too few members present", "Logical action: cancel the meeting", "'called off' = cancelled: correct"],
  "'Called on' means visited or asked to speak. 'Called for' means demanded. 'Called in' means summoned someone. "
  "None fits a meeting cancelled for lack of members.", 30)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The board **turned off** the expansion proposal because it was too costly.",
  ["turned up", "turned down", "turned over", NR], "B",
  "Phrasal verbs with 'turn': turn down = reject",
  "A proposal that is too costly is rejected. 'Turn down' means reject; 'turn off' means switch off (a device).",
  ["Context: the proposal is too costly", "Needed meaning: reject", "'turned down'"],
  "'Turned up' means appeared or increased. 'Turned over' means handed over or flipped. The original 'turned off' "
  "is wrong, so 'No replacement required' does not apply.", 30)

Q(PR, "Replace the phrase", A,
  PR_STEM + "**In lieu of** the festival, the branch will remain closed on Thursday.",
  ["On account of", "In spite of", "In place of", NR], "A",
  "'In lieu of' = instead of; 'on account of' = because of",
  "The festival is the reason the branch will close, so a phrase meaning 'because of' is needed: 'On account of the "
  "festival, the branch will remain closed.' 'In lieu of' means 'instead of', which makes no sense here.",
  ["Relation between festival and closure: cause", "'In lieu of' means 'instead of': wrong",
   "Cause phrase: 'On account of'"],
  "'In spite of' expresses contrast, not cause. 'In place of' means the same as 'in lieu of'. The original is "
  "wrong, so 'No replacement required' does not apply.", 40)

Q(PR, "Replace the phrase", A,
  PR_STEM + "The minister's claim **was on contrary to** the data released by her own ministry.",
  ["was contrary with", "were contrary to", "ran contrary to", NR], "C",
  "Fixed expression: 'run contrary to' / 'be contrary to'",
  "The idiom is 'contrary to' with no 'on': 'The minister's claim ran contrary to the data.' 'Ran contrary to' means "
  "went against.",
  ["Remove 'on': the phrase is 'contrary to'", "Subject 'claim' is singular", "'ran contrary to' fits"],
  "A uses the wrong preposition 'with'. B uses the plural 'were' with the singular subject 'claim'. The original "
  "'was on contrary to' is wrong, so 'No replacement required' does not apply.", 40)

Q(PR, "Replace the phrase", A,
  PR_STEM + "Most retired depositors **are averse from** taking risks with their savings.",
  ["are adverse to", "are averse to", "are averse for", NR], "B",
  "'Averse to' = opposed to, unwilling; 'adverse' = harmful, unfavourable",
  "People who dislike risk are 'averse to' it: 'Most retired depositors are averse to taking risks.' The preposition "
  "is 'to'.",
  ["Meaning needed: unwilling, opposed", "Word: 'averse' (not 'adverse')", "Preposition: 'to'"],
  "'Adverse' means harmful ('adverse effects') and does not describe a person's attitude. 'Averse for' uses the "
  "wrong preposition. The original is wrong, so 'No replacement required' does not apply.", 40)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", B, "A customer is comparing a bank's new mobile app with its old one. " + SC_OK,
  ["This app is more faster than the old one.", "This app is faster than the old one.",
   "This app is most faster than the old one.", "This app is fastest than the old one."], "B",
  "Comparative degree: one-syllable adjectives add -er; no 'more' or 'most' with it",
  "Comparing two things needs the comparative 'faster', and 'than' follows the comparative. 'More faster' is a "
  "double comparative.",
  ["Two things compared → comparative degree", "'fast' → 'faster' (no 'more')", "Option B"],
  "A and C add 'more' or 'most' to a form that is already comparative. D uses the superlative with 'than'.", 25)

Q(SC, "Grammatically incorrect sentence", B, "Four remarks were overheard at a branch counter. " + SC_BAD,
  ["I don't know anything about the new scheme.", "She hardly ever visits the branch.",
   "He can't hardly read the small print on the form.", "We have never missed a payment."], "C",
  "Double negatives: 'hardly' is already negative",
  "'Hardly' has a negative meaning, so it cannot be combined with 'can't'. The correct form is 'He can hardly read "
  "the small print.'",
  ["A: 'don't ... anything': one negative, correct", "B: 'hardly ever': correct",
   "C: 'can't hardly': double negative, incorrect", "D: 'never': one negative, correct"],
  "A, B and D each contain only one negative and are correct.", 30)

Q(SC, "Correct sentence", B, "Which of the following requests from a colleague is grammatically correct?",
  ["Please keep this matter between you and I.", "Please keep this matter between you and myself.",
   "Please keep this matter between I and you.", "Please keep this matter between you and me."], "D",
  "A pronoun after a preposition takes the object form",
  "'Between' is a preposition, so the pronouns after it must be object forms: 'between you and me'.",
  ["'between' is a preposition", "Object pronoun needed: 'me', not 'I'", "Option D"],
  "A and C use the subject pronoun 'I' after a preposition. B uses the reflexive 'myself', which needs a matching "
  "subject ('I ... myself') and is wrong here.", 25)

Q(SC, "Correct sentence", I, SC_OK,
  ["The clerk admitted making an error in the ledger.", "The clerk admitted to make an error in the ledger.",
   "The clerk admitted of making an error in the ledger.", "The clerk admitted to have made an error in the ledger."],
  "A",
  "'Admit' + gerund (or 'admit to' + gerund); never 'admit' + to-infinitive",
  "'Admit' is followed by a gerund: 'admitted making an error'. ('Admitted to making' is also correct, but it is not "
  "among the options.)",
  ["'admit' takes the -ing form", "A: 'admitted making': correct",
   "B and D: 'to' + infinitive after 'admit': wrong", "C: 'admit of' means 'allow' and does not fit"],
  "B and D use a to-infinitive after 'admit', which is incorrect. C uses 'admit of', which means 'leave room for' "
  "('The facts admit of no doubt') and cannot be used for confessing.", 35)

Q(SC, "Grammatically incorrect sentence", I, SC_BAD,
  ["The scheme will benefit farmers as well as traders.", "Hardly anyone attended the meeting.",
   "The manager made him to sign the register again.", "She is the more capable of the two officers."], "C",
  "Causative 'make' + object + bare infinitive (in the active voice)",
  "In the active voice, 'make someone do something' takes the base form without 'to': 'The manager made him sign "
  "the register again.'",
  ["A: 'as well as' joins two nouns: correct", "B: 'Hardly anyone': correct",
   "C: 'made him to sign': 'to' must be dropped, incorrect",
   "D: comparative 'the more capable of the two': correct"],
  "A, B and D are correct. D in particular rightly uses the comparative for two people.", 35)

Q(SC, "Correct sentence", A, SC_OK,
  ["The files have laid untouched on the shelf for months.", "The files have lain untouched on the shelf for months.",
   "The files have lied untouched on the shelf for months.", "The files have layed untouched on the shelf for months."],
  "B",
  "Lie (rest) – lay – lain vs lay (put) – laid – laid",
  "The files are resting, so the verb is intransitive 'lie', whose past participle is 'lain': 'The files have lain "
  "untouched for months.'",
  ["Are the files resting or putting something? Resting → 'lie'",
   "Forms of 'lie' (rest): lie, lay, lain", "Present perfect: 'have lain'"],
  "A uses 'laid', the participle of 'lay' (to put), which needs an object. C uses 'lied', which belongs to 'lie' "
  "meaning to tell an untruth. D 'layed' is not a standard form.", 40)

Q(SC, "Grammatically incorrect sentence", A, SC_BAD,
  ["Were the bank to raise its rates, many borrowers would protest.",
   "Not only did sales fall, but costs also rose.",
   "Having been warned twice, the clerk was finally suspended.",
   "Write down the reference number lest you should not forget it."], "D",
  "'Lest' already means 'so that ... not'; it is not followed by another negative",
  "'Lest' carries the negative meaning, so 'lest you should not forget' is a double negative and says the opposite "
  "of what is meant. The correct form is 'lest you should forget it' (or 'lest you forget it').",
  ["A: inverted conditional 'Were the bank to ...': correct",
   "B: 'Not only did ... but ... also': correct",
   "C: participle phrase whose doer is 'the clerk', the subject: correct",
   "D: 'lest ... should not': double negative, incorrect"],
  "A, B and C are correct. C is not a dangling modifier: the clerk is the one who was warned.", 45)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) With the loan, she bought a second-hand sewing machine.\n"
  "(B) Meena had always wanted to start a tailoring business from her home.\n"
  "(C) Within a year, she had repaid the loan and hired two assistants.\n"
  "(D) But she did not have enough money to buy a machine.\n"
  "(E) So she approached her self-help group for a small loan.",
  ["BDEAC", "BEDAC", "DBEAC", "BDAEC"], "A",
  "Para jumble: named opener, then problem, solution, action and result",
  "B introduces Meena and her wish. D gives the problem ('But ... not enough money'). E gives her response ('So she "
  "approached ...'). A uses 'the loan', so it follows E. C ('Within a year') closes the story.",
  ["Opener: B (names Meena; the others use 'she')", "B → D: 'But' introduces the obstacle",
   "D → E: 'So' gives the response", "E → A: 'the loan' refers to E's loan; C last: BDEAC"],
  "BEDAC has her seek a loan before the money problem is stated. DBEAC opens with 'But she' before Meena is named. "
  "BDAEC has her use 'the loan' before asking for it.", 50)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) The town's weekly market is held every Sunday near the bus stand.\n"
  "(P) Farmers from nearby villages arrive early with vegetables, grain and milk.\n"
  "(Q) By eight in the morning, the ground is crowded with buyers.\n"
  "(R) By noon, most of the stock has been sold and the stalls begin to close.\n"
  "(S) The farmers then use their earnings to buy seeds and household goods before heading home.",
  ["PRQS", "QPRS", "PQRS", "PQSR"], "C",
  "Fixed opener; follow the time sequence (early → eight o'clock → noon → then)",
  "The sentences follow the market day: farmers arrive early (P), buyers crowd in by eight (Q), stock is sold by "
  "noon (R), and the farmers then spend their earnings (S).",
  ["(1) → P: sellers arrive first", "Q: 'By eight in the morning'", "R: 'By noon'",
   "S: 'then use their earnings' after selling: PQRS"],
  "PRQS puts noon before eight o'clock. QPRS has buyers crowding the ground before the sellers arrive. PQSR has "
  "farmers spending earnings before the stock is sold.", 45)

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) Last year, the school installed solar panels on its roof with help from the panchayat.\n"
  "(B) The money saved on electricity bills is now being used to buy books for the library.\n"
  "(C) A village school often lost power for hours during the afternoon.\n"
  "(D) The panels now supply most of the school's electricity during the day.\n"
  "(E) As a result, teachers found it hard to use the computers donated by a local firm.",
  ["CAEDB", "CEADB", "ECADB", "CEABD"], "B",
  "Para jumble: problem → its effect → solution → result → further benefit",
  "C introduces the school and the power cuts. E states the effect ('As a result'). A gives the solution (solar "
  "panels). D describes what 'the panels' now do. B mentions money saved, which follows from D.",
  ["Opener: C ('A village school')", "C → E: 'As a result' follows the power cuts",
   "A introduces the panels; D refers to 'The panels'", "B (savings) follows D: CEADB"],
  "CAEDB puts the solution before the effect of the problem, so 'As a result' follows the solar panels. ECADB opens "
  "with 'As a result'. CEABD mentions savings before saying the panels supply the electricity.", 55)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) Earlier, passengers had to stand in long queues at the station to buy a railway ticket.\n"
  "(P) They are still used by passengers who are not comfortable with smartphones.\n"
  "(Q) Later, computerised reservation counters made it possible to book a ticket for any train from any major "
  "station.\n"
  "(R) Even so, the counters have not disappeared completely.\n"
  "(S) Today, most tickets are booked online in a few minutes.",
  ["SQRP", "QRSP", "QSPR", "QSRP"], "D",
  "Time markers (Earlier → Later → Today) and the pronoun 'They'",
  "The paragraph moves through time: queues earlier (1), computerised counters later (Q), online booking today (S). "
  "R ('Even so') contrasts with S, and P ('They') refers to 'the counters' in R.",
  ["(1) 'Earlier' → Q 'Later' → S 'Today'", "R: 'Even so' contrasts with online booking",
   "P: 'They' = the counters in R: QSRP"],
  "SQRP puts 'Today' before 'Later'. QRSP says counters have not disappeared before online booking is mentioned. "
  "QSPR makes 'They' refer to tickets.", 50)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Manufacturers argue that unauthorised repairs could compromise safety and void warranties.\n"
  "(B) Campaigners, however, say such claims are often used to protect profitable service monopolies.\n"
  "(C) When a smartphone or a tractor breaks down, its owner is often forced to go back to the company that made "
  "it.\n"
  "(D) This is because spare parts, manuals and diagnostic software are not available to independent repairers.\n"
  "(E) A growing 'right to repair' movement wants these restrictions removed.",
  ["CEDAB", "ECDAB", "CDEAB", "CDAEB"], "C",
  "Para jumble: situation → cause ('This is because') → movement → objection → reply",
  "C states the situation. D explains it ('This is because ...'). E introduces the movement against 'these "
  "restrictions'. A gives the manufacturers' objection, and B replies to 'such claims' with 'however'.",
  ["Opener: C (general situation)", "D explains C", "E: 'these restrictions' = the restrictions in D",
   "A (objection) → B ('such claims', 'however'): CDEAB"],
  "CEDAB mentions 'these restrictions' before they are described. ECDAB opens with 'these restrictions'. CDAEB puts "
  "the manufacturers' reply before the movement they are replying to.", 60)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) Hospitals in many cities are turning to telemedicine to reach patients in remote areas.\n"
  "(P) A doctor in the city can then examine the reports, speak to the patient on a video call and prescribe "
  "treatment.\n"
  "(Q) Under this arrangement, a health worker at a village centre records the patient's symptoms and basic test "
  "results.\n"
  "(R) This saves the patient a long and expensive journey.\n"
  "(S) It cannot, however, replace a physical examination when a serious condition is suspected.",
  ["QPRS", "PQRS", "QRPS", "QPSR"], "A",
  "Process order ('then') and a final limitation ('however')",
  "Q explains the arrangement (a health worker records details). P follows with 'then' (the doctor examines the "
  "reports). R gives the benefit, and S ends with the limitation.",
  ["(1) → Q: 'this arrangement' = telemedicine", "Q → P: the doctor examines the reports Q mentions",
   "R: benefit; S: 'however' limitation: QPRS"],
  "PQRS has the doctor examine 'the reports' before they are recorded. QRPS states the benefit before describing the "
  "consultation. QPSR gives the limitation before the benefit, leaving 'This saves ...' with an unclear referent.", 55)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) Instead, they reduce the quantity in each pack while keeping the price unchanged.\n"
  "(B) When the cost of raw materials rises, companies selling packaged goods face a dilemma.\n"
  "(C) Economists call this practice 'shrinkflation'.\n"
  "(D) Raising prices openly risks driving away customers who watch price tags closely.\n"
  "(E) Shrinkflation often goes unnoticed, because shoppers check prices far more often than pack sizes.",
  ["BADCE", "BDACE", "BDAEC", "DBACE"], "B",
  "Para jumble: dilemma → rejected option → 'Instead' → name → consequence of the named practice",
  "B states the dilemma. D gives the rejected option (raising prices). A begins 'Instead', so it follows D. C names "
  "'this practice' (A's). E uses the term 'Shrinkflation', so it must come after C defines it.",
  ["Opener: B (sets up the dilemma)", "D → A: 'Instead' needs an option to replace",
   "C names A's practice", "E uses the name, so it comes after C: BDACE"],
  "BADCE puts 'Instead' before the option it replaces. BDAEC uses the term 'Shrinkflation' before it is introduced. "
  "DBACE begins with the rejected option before the dilemma is set up.", 70)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) For most of history, a trader's reputation in the marketplace travelled by word of mouth.\n"
  "(P) That very scale, however, has made ratings an attractive target for manipulation.\n"
  "(Q) Online ratings promised to scale up this ancient mechanism to millions of buyers and sellers.\n"
  "(R) Fake reviews, bought in bulk, can now lift an indifferent product above an excellent one.\n"
  "(S) A trader who cheated one customer would soon find that others had heard about it.",
  ["QSPR", "SPQR", "SQRP", "SQPR"], "D",
  "Fixed opener; 'this ancient mechanism' and 'That very scale' as links",
  "S illustrates word of mouth from (1). Q calls it 'this ancient mechanism' and introduces online ratings. P "
  "('That very scale') refers to Q's 'millions'. R gives the result of the manipulation in P.",
  ["(1) → S: an example of word of mouth", "S → Q: 'this ancient mechanism' = word of mouth",
   "Q → P: 'That very scale' = millions of buyers and sellers", "P → R: manipulation → fake reviews: SQPR"],
  "QSPR moves to online ratings and then back to the old marketplace example. SPQR mentions 'That very scale' before "
  "any scale is described. SQRP gives the fake-review result before the manipulation that explains it.", 70)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) Supporters point to trials in which output held steady even as working hours fell.\n"
  "(B) Sceptics reply that the firms in these trials volunteered and were therefore likely to succeed.\n"
  "(C) The idea of a four-day working week has moved from the fringes to mainstream debate.\n"
  "(D) Whether such results would hold across an entire economy therefore remains an open question.\n"
  "(E) Employees in these trials also reported less stress and fewer sick days.",
  ["CAEBD", "CABED", "CEABD", "CAEDB"], "A",
  "Para jumble: topic → supporters' evidence → added evidence → objection → conclusion",
  "C introduces the debate. A gives the supporters' evidence (trials). E adds to it ('also', 'these trials'). B "
  "gives the sceptics' reply. D draws the conclusion ('therefore') from the doubt raised in B.",
  ["Opener: C", "A introduces 'trials'; E ('these trials ... also') extends A",
   "B: sceptics' reply to the evidence", "D: 'therefore' concludes from B: CAEBD"],
  "CABED separates E from the supporters' evidence and puts it after the sceptics' reply. CEABD mentions 'these "
  "trials' before any trial is introduced. CAEDB draws the conclusion before the doubt that justifies it.", 70)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) A city's informal settlements are often described only in terms of what they lack.\n"
  "(P) Yet many of them are also dense networks of small enterprises, from tailoring units to recycling workshops.\n"
  "(Q) Treating these areas solely as problems to be cleared can therefore destroy livelihoods along with shacks.\n"
  "(R) By contrast, upgrading them in place, with water, drainage and secure tenure, tends to preserve those "
  "networks.\n"
  "(S) Residents typically live close to where they work, often in the same building.",
  ["PQSR", "SPQR", "PSQR", "RPSQ"], "C",
  "Fixed opener; 'Yet' contrasts with (1), 'therefore' and 'By contrast' order the argument",
  "P contrasts with (1) ('Yet ... also'). S adds detail about those enterprises (people live where they work). Q "
  "draws the consequence ('therefore') of clearing such areas. R offers the alternative ('By contrast').",
  ["(1) → P: 'Yet' answers 'only in terms of what they lack'", "P → S: detail about the work networks",
   "Q: 'therefore' follows from P and S", "R: 'By contrast' answers Q: PSQR"],
  "PQSR draws the conclusion (Q) before S finishes the evidence. SPQR describes residents' work before the "
  "enterprises are introduced. RPSQ offers the contrast before there is anything to contrast with.", 70)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", B,
  SR_STEM + "(P) to all account holders\n(Q) the bank sent\n(R) about the new service charges\n(S) a text message",
  ["QSPR", "SQPR", "QPRS", "PQSR"], "A",
  "Subject + verb + direct object, then the prepositional phrases",
  "'The bank sent a text message to all account holders about the new service charges.' The verb 'sent' (Q) is "
  "followed by its object 'a text message' (S), then 'to whom' (P) and 'about what' (R).",
  ["Subject + verb: Q ('the bank sent')", "Direct object follows the verb: S",
   "Then the recipients (P) and the topic (R): QSPR"],
  "SQPR places the object before the subject and verb. QPRS separates 'sent' from its object and leaves 'a text "
  "message' dangling at the end. PQSR begins with a prepositional phrase that cannot open this sentence.", 35)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) the farmers who had\n(Q) lost their crops to the floods\n(R) were given\n"
  "(S) interest-free loans by the cooperative",
  ["PRQS", "QPRS", "PQRS", "PQSR"], "C",
  "Relative clause completed before the main verb; passive verb + object + agent",
  "'The farmers who had lost their crops to the floods were given interest-free loans by the cooperative.' The "
  "relative clause (P + Q) must be complete before the main verb 'were given' (R).",
  ["P ends with 'who had', which needs a past participle: Q ('lost ...')",
   "Then the main verb R ('were given')", "Then what was given and by whom: S: PQRS"],
  "PRQS gives 'who had were given', which is ungrammatical. QPRS cannot start with 'lost'. PQSR puts the object "
  "before the verb.", 40)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The new mobile app makes it ______ for customers to check their balance at any time.",
  ["easy", "easily", "ease", "easiness"], "A",
  "'Make it + adjective + for + person + to-infinitive'",
  "In 'makes it ___ for customers to check', 'it' is the object and the blank is its complement, which must be an "
  "adjective: 'makes it easy'.",
  ["Pattern: make + it + adjective + to-infinitive", "Adjective needed", "'easy'"],
  "'Easily' is an adverb, and 'ease' and 'easiness' are nouns; none can be the complement of 'it' in this "
  "pattern.", 25)

Q(FB, "Double blank", B,
  FB2 + "The bank ______ the customer's request and ______ a duplicate passbook within a week.",
  ["rejected, issued", "accepted, issued", "accepted, cancelled", "ignored, printed"], "B",
  "Double blank: both words must agree in meaning",
  "The sentence describes a request being met: the bank accepted the request and issued a duplicate passbook.",
  ["The 'and' joins two actions in the same direction", "Request met → accepted + issued", "Option B"],
  "A and D pair a refusal or neglect of the request with a helpful action, which is contradictory. C pairs accepting "
  "the request with cancelling the passbook, which defeats the request.", 30)

Q(FB, "Single blank", I,
  FB1 + "Despite repeated reminders from the branch, the borrower remained ______ and made no effort to repay the "
  "loan.",
  ["prompt", "grateful", "indifferent", "punctual"], "C",
  "Single blank: 'Despite' signals that the borrower did not respond",
  "Repeated reminders produced no response, so the borrower was unconcerned: 'indifferent'.",
  ["'Despite repeated reminders' → the reminders had no effect", "'made no effort' confirms lack of concern",
   "'indifferent'"],
  "'Prompt' and 'punctual' contradict 'made no effort to repay'. 'Grateful' does not fit the lack of response.", 30)

Q(FB, "Double blank", I,
  FB2 + "The audit ______ several lapses in record-keeping, but the inspector found no ______ of fraud.",
  ["concealed, evidence", "revealed, absence", "praised, sign", "revealed, evidence"], "D",
  "Double blank: 'but' contrasts lapses with the absence of fraud",
  "An audit reveals (brings to light) lapses. 'But' introduces a contrast: there were lapses, yet no evidence of "
  "fraud.",
  ["Blank 1: what an audit does with lapses → 'revealed'",
   "Blank 2: 'no ___ of fraud' → 'evidence'", "Option D"],
  "A: an audit does not conceal lapses. B: 'found no absence of fraud' would mean fraud was present, which clashes "
  "with 'but'. C: an audit does not praise lapses.", 35)

Q(FB, "Phrase fillers", I,
  FBP + "The road project was abandoned ______ funds, and the half-built bridge still stands unused.",
  ["for want of", "in want for", "by want of", "on want of"], "A",
  "Fixed phrase: 'for want of' = because of a lack of",
  "The project stopped because there was not enough money. The fixed phrase is 'for want of funds'.",
  ["Meaning needed: because of a lack of", "Fixed phrase: 'for want of'"],
  "'In want for', 'by want of' and 'on want of' are not English phrases.", 30)

Q(FB, "Double blank", A,
  FB2 + "The regulator's response was ______: instead of addressing the root cause of the losses, it merely ______ "
  "the symptoms.",
  ["thorough, treated", "superficial, treated", "superficial, ignored", "delayed, cured"], "B",
  "Double blank: the colon explains the first word; 'merely' limits the second",
  "The colon explains the response: it dealt only with symptoms, not causes. That is a 'superficial' response that "
  "'merely treated the symptoms'.",
  ["After the colon: root cause ignored, symptoms handled → superficial",
   "'merely ___ the symptoms' → it did deal with them, but only them → 'treated'", "Option B"],
  "A: 'thorough' contradicts ignoring the root cause. C: 'merely ignored the symptoms' makes no sense; if it ignored "
  "both causes and symptoms, 'merely' has no point. D: 'cured' is too strong for a response criticised as "
  "inadequate, and 'delayed' is not what the colon explains.", 45)

Q(FB, "Single blank", A,
  FB1 + "His explanation for the missing funds was so ______ that even his closest colleagues found it hard to "
  "believe.",
  ["cogent", "lucid", "candid", "far-fetched"], "D",
  "Single blank: 'so ... that' result clause",
  "The result is that even his friends could not believe it, so the explanation must have been unlikely or "
  "improbable: 'far-fetched'.",
  ["Result: 'even his closest colleagues found it hard to believe'",
   "Cause must be a quality that makes something unbelievable", "'far-fetched'"],
  "'Cogent' (convincing), 'lucid' (clear) and 'candid' (frank) are qualities that would make an explanation easier "
  "to believe, not harder.", 35)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'affect' used correctly?",
  ["The strike will effect the bank's operations in the district.",
   "The rate cut had no affect on deposits.",
   "The new rule will affect all current account holders.",
   "The affect of the rate cut was felt within a month."], "C",
  "Affect (verb: to influence) vs effect (noun: result)",
  "'Affect' is normally a verb meaning 'to influence'. In C it is used as a verb: 'The new rule will affect all "
  "current account holders.'",
  ["A uses 'effect' as a verb meaning 'influence': wrong (it should be 'affect')",
   "B and D use 'affect' as a noun meaning 'result': wrong (it should be 'effect')",
   "C uses 'affect' as a verb: correct"],
  "A should read 'will affect the bank's operations'. B should read 'no effect on deposits'. D should read 'The "
  "effect of the rate cut'.", 30)

Q(WU, "Word swap", I,
  WS_STEM + "The **(A) deposit** asked the cashier to **(B) customer** the cheque **(C) into** his savings **(D) "
  "account**.",
  ["A-B", "A-C", "B-D", "No swap required"], "A",
  "Word swap: check each bold word in its slot",
  "A customer asks a cashier to deposit a cheque. Swapping A and B gives: 'The customer asked the cashier to deposit "
  "the cheque into his savings account.'",
  ["'The deposit asked the cashier' makes no sense", "'to customer the cheque' makes no sense",
   "Swap A and B; 'into' and 'account' are already correct"],
  "A-C gives 'The into asked the cashier'. B-D gives 'to account the cheque into his savings customer'. The sentence "
  "clearly needs a swap.", 35)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'discreet' used correctly?",
  ["The data were divided into four discreet categories.",
   "Each instalment is a discreet payment recorded separately.",
   "The two accounts are kept in discreet ledgers.",
   "The manager made a discreet inquiry about the borrower's other debts."], "D",
  "Discreet (careful, tactful, not drawing attention) vs discrete (separate, distinct)",
  "'Discreet' means careful and tactful so as not to cause embarrassment. A quiet, tactful inquiry about someone's "
  "debts is a 'discreet inquiry'.",
  ["A, B and C all mean 'separate' or 'distinct': they need 'discrete'",
   "D means a careful, tactful inquiry: 'discreet' is correct"],
  "A ('discrete categories'), B ('a discrete payment') and C ('discrete ledgers') need 'discrete', meaning "
  "separate.", 35)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'flout' used correctly?",
  ["The company was fined for flouting the safety rules at its plant.",
   "He liked to flout his new car in front of his neighbours.",
   "The winners flouted their trophy at the parade.",
   "She flouted her knowledge of tax law at every meeting."], "A",
  "Flout (openly disobey a rule) vs flaunt (show off)",
  "'Flout' means to break or openly disregard a rule. A company fined for ignoring safety rules has 'flouted' them.",
  ["A: openly breaking rules → 'flout': correct",
   "B, C and D describe showing off → they need 'flaunt'"],
  "B ('flaunt his new car'), C ('flaunted their trophy') and D ('flaunted her knowledge') confuse 'flout' with "
  "'flaunt'.", 35)

Q(WU, "Word swap", A,
  WS_STEM + "The **(A) committee** decided to keep the policy rate unchanged because **(B) target** had not yet "
  "**(C) eased** to its **(D) inflation**.",
  ["A-B", "A-D", "B-D", "No swap required"], "C",
  "Word swap: subject–object logic in the 'because' clause",
  "It is inflation that eases towards a target, not a target that eases to its inflation. Swapping B and D gives: "
  "'... because inflation had not yet eased to its target.'",
  ["'committee decided' and 'eased' are correct in place",
   "'target had not yet eased to its inflation' reverses the logic",
   "Swap B and D: 'inflation had not yet eased to its target'"],
  "A-B gives 'The target decided', which is meaningless. A-D gives 'The inflation decided ... to its committee'. "
  "The sentence needs a swap, so 'No swap required' is wrong.", 45)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'lapsed' as used in the sentence:\n"
  "'His insurance policy lapsed because he forgot to pay the premium for three months.'",
  ["was renewed", "ceased to be valid", "was transferred", "doubled in value"], "B",
  "Lapse (of a policy or right) = come to an end through neglect",
  "A policy whose premium is not paid stops being in force. 'Lapsed' means it ceased to be valid.",
  ["Cause: premium unpaid for three months", "Result for a policy: it ends", "'ceased to be valid'"],
  "'Was renewed' and 'doubled in value' are the opposite of what non-payment causes. 'Was transferred' has no link "
  "with missing premiums.", 25)

Q(VO, "Word pairs", B,
  "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Ample – Plentiful", "Scarce – Abundant", "Hasty – Careful", "Rigid – Flexible"], "A",
  "Word pairs: identify synonyms and antonyms",
  "'Ample' and 'plentiful' both mean more than enough. The other three pairs are opposites.",
  ["Ample = plentiful (synonyms)", "Scarce ≠ abundant", "Hasty ≠ careful", "Rigid ≠ flexible"],
  "B, C and D are pairs of opposites, not synonyms.", 25)

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'lax' as used in the sentence:\n"
  "'The inspection report was scathing about the branch's lax control over cash in the vault.'",
  ["strict", "costly", "loose and careless", "secret"], "C",
  "Lax = not strict or careful enough",
  "A 'scathing' (severely critical) report criticises weak control. 'Lax control' is loose, careless control.",
  ["Context: the report is 'scathing' (harshly critical)", "So the control must have been poor",
   "'lax' = loose and careless"],
  "'Strict' is the opposite and would not draw harsh criticism. 'Costly' and 'secret' do not describe a weakness "
  "in control.", 30)

Q(VO, "Word pairs", A,
  "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Venal – Corrupt", "Recalcitrant – Defiant", "Diffident – Shy", "Parsimonious – Lavish"], "D",
  "Advanced vocabulary: synonym and antonym pairs",
  "'Parsimonious' means extremely unwilling to spend money; 'lavish' means spending generously. They are opposites. "
  "The other pairs are synonyms.",
  ["Venal = corrupt (open to bribery)", "Recalcitrant = defiant (resisting authority)",
   "Diffident = shy (lacking self-confidence)", "Parsimonious ≠ lavish"],
  "A, B and C are pairs of synonyms, not opposites.", 35)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", B,
  SY_STEM + "The branch manager sent a **brief** reply to the customer's long letter of complaint.",
  ["short", "rude", "detailed", "delayed"], "A",
  "Brief = short",
  "A 'brief' reply is a short one; the contrast with the customer's 'long letter' confirms the meaning.",
  ["Contrast clue: 'long letter'", "'brief' = short"],
  "'Detailed' is close to the opposite. 'Rude' and 'delayed' describe tone and timing, not length.", 20)

Q(SY, "Contextual synonym", B,
  SY_STEM + "The cashier **verified** the signature on the cheque before paying out the amount.",
  ["ignored", "checked", "copied", "forged"], "B",
  "Verify = check that something is true or genuine",
  "Before paying, a cashier makes sure the signature is genuine: he checks it.",
  ["Context: a precaution before payment", "'verify' = check, confirm"],
  "'Ignored' is the opposite of a precaution. 'Copied' and 'forged' describe fraud, not verification.", 20)

Q(SY, "Contextual synonym", B,
  SY_STEM + "The minister **lauded** the bank staff for keeping branches open during the floods.",
  ["criticised", "ignored", "praised", "doubted"], "C",
  "Laud = praise",
  "Keeping branches open during floods deserves praise; 'lauded' means praised highly.",
  ["Context: staff did something commendable", "'lauded' = praised"],
  "'Criticised' is the opposite. 'Ignored' and 'doubted' do not fit a reaction to commendable work.", 20)

Q(SY, "Contextual synonym", B,
  SY_STEM + "Customers were asked to **retain** the receipt until the amount was credited to their account.",
  ["discard", "sign", "copy", "keep"], "D",
  "Retain = keep",
  "The receipt is proof until the money is credited, so customers must keep it. 'Retain' means keep.",
  ["Context: receipt needed until the credit appears", "'retain' = keep"],
  "'Discard' is the opposite. 'Sign' and 'copy' are different actions and do not mean holding on to something.", 20)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The new chairman is known for his **pragmatic** approach: he prefers workable solutions to grand "
  "theories.",
  ["practical", "idealistic", "careless", "cautious"], "A",
  "Pragmatic = dealing with things in a practical, realistic way",
  "The sentence explains the word: he prefers workable solutions to grand theories. That is a practical approach.",
  ["Explanation after the colon: workable solutions over theories", "'pragmatic' = practical"],
  "'Idealistic' is nearly the opposite (theories over practice). 'Careless' and 'cautious' are not suggested by the "
  "explanation.", 25)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The scheme was launched with great fanfare, but its impact on rural unemployment has been "
  "**negligible**.",
  ["insignificant", "immense", "harmful", "lasting"], "A",
  "Negligible = so small as not to matter",
  "'With great fanfare, but ...' sets up a contrast: big publicity, tiny impact. 'Negligible' means insignificant.",
  ["'but' contrasts the grand launch with the result", "Result must be small", "'insignificant'"],
  "'Immense' and 'lasting' remove the contrast. 'Harmful' changes the meaning from small to damaging.", 25)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The board's decision to **defer** the dividend until the next quarter surprised shareholders.",
  ["increase", "announce", "cancel", "postpone"], "D",
  "Defer = put off to a later time",
  "'Until the next quarter' shows the dividend is not being dropped but moved to a later date: 'postpone'.",
  ["Clue: 'until the next quarter'", "Moved to a later date = postponed", "'defer' = postpone"],
  "'Cancel' would not fit 'until the next quarter'. 'Increase' and 'announce' do not mean delaying.", 25)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The manager was **reluctant** to approve the loan without any collateral.",
  ["unwilling", "eager", "hesitant", "afraid"], "B",
  "Reluctant = unwilling; antonym: eager",
  "'Reluctant' means unwilling or hesitant. Its opposite is 'eager'.",
  ["'reluctant' = unwilling", "Opposite = eager"],
  "'Unwilling' and 'hesitant' are synonyms of 'reluctant'. 'Afraid' is close in feeling, not opposite.", 20)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The company's profits have shown a **steady** rise over the last five years.",
  ["constant", "gradual", "regular", "erratic"], "D",
  "Steady = regular, even; antonym: erratic (irregular, unpredictable)",
  "A 'steady' rise is even and regular. The opposite is an 'erratic' pattern, irregular and unpredictable.",
  ["'steady' = even, regular", "Opposite = irregular, unpredictable: 'erratic'"],
  "'Constant', 'gradual' and 'regular' are all close in meaning to 'steady'.", 25)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The new manager's **transparent** style of working quickly won the trust of the staff.",
  ["secretive", "open", "clear", "honest"], "A",
  "Transparent (of conduct) = open, nothing hidden; antonym: secretive",
  "A 'transparent' style is open, with nothing hidden, which is why it earned trust. The opposite is 'secretive'.",
  ["'transparent' here = open about decisions", "Opposite = secretive"],
  "'Open', 'clear' and 'honest' are all similar to 'transparent' in this sense.", 25)

Q(AN, "Contextual antonym", I,
  AN_STEM + "Asked about the rise in bad loans, the official gave only a **vague** answer.",
  ["unclear", "brief", "polite", "precise"], "D",
  "Vague = not clear or definite; antonym: precise",
  "A 'vague' answer lacks detail and clarity. The opposite is a 'precise' answer.",
  ["'vague' = unclear, not specific", "Opposite = exact, specific: 'precise'"],
  "'Unclear' is a synonym. 'Brief' and 'polite' describe length and manner, not clarity.", 25)

Q(AN, "Contextual antonym", A,
  AN_STEM + "The chairman's **conciliatory** remarks helped ease the tension between the management and the union.",
  ["soothing", "apologetic", "provocative", "diplomatic"], "C",
  "Conciliatory = intended to calm anger or make peace; antonym: provocative",
  "'Conciliatory' remarks are meant to pacify, which is why they 'helped ease the tension'. The opposite is "
  "'provocative', meaning likely to cause anger.",
  ["'conciliatory' = peace-making (confirmed by 'helped ease the tension')",
   "Opposite = causing anger: 'provocative'"],
  "'Soothing', 'apologetic' and 'diplomatic' are all close in meaning to 'conciliatory'.", 30)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"

Q(ID, "Meaning of idiom", I,
  "Choose the meaning of the idiom 'to keep one's head above water'.",
  ["to swim well in deep water", "to be very proud of oneself",
   "to manage to survive, especially in financial difficulty", "to take a very big risk"], "C",
  "Idiom: keep one's head above water",
  "The idiom means to just about manage to survive a difficult situation, usually a financial one. For example, "
  "'With sales down, the shop is barely keeping its head above water.'",
  ["Image: a person struggling not to sink", "Meaning: to survive, just about, in difficulty"],
  "'To swim well' takes the idiom literally. 'To be very proud' and 'to take a big risk' have no link with it.", 25)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "After losing its two biggest clients, the small trading firm was **on its last legs**.",
  ["about to collapse", "growing rapidly", "moving to a new office", "looking for a merger partner"], "A",
  "Idiom: on its last legs = close to failure or the end",
  "Losing its two biggest clients has left the firm close to failing: 'on its last legs'.",
  ["Context: the firm has lost its biggest clients", "Idiom: near the end, about to fail"],
  "'Growing rapidly' contradicts the context. 'Moving office' and 'looking for a merger' are not meanings of the "
  "idiom.", 25)

Q(ID, "Idiom in context", A,
  "Choose the meaning of the idiom in bold.\n"
  "The claim that the deficit would be met without any new taxes was taken **with a pinch of salt** by most "
  "economists.",
  ["with complete trust", "with some doubt", "with open anger", "with amusement"], "B",
  "Idiom: take something with a pinch of salt = not believe it fully",
  "Economists were sceptical that the deficit could be met without new taxes, so they did not fully believe the "
  "claim.",
  ["Context: an optimistic fiscal claim", "Idiom: accept with reservations, doubt"],
  "'With complete trust' is the opposite. 'Open anger' and 'amusement' are reactions the idiom does not express.",
  30)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", B, OW_STEM + "A person who lends money at very high rates of interest",
  ["debtor", "usurer", "auditor", "philanthropist"], "B",
  "One-word substitution: lending terms",
  "A 'usurer' lends money at excessively high interest ('usury').",
  ["Key idea: lending + excessive interest", "Word: usurer"],
  "A 'debtor' owes money. An 'auditor' examines accounts. A 'philanthropist' gives money to good causes.", 20)

Q(OW, "Single word for a phrase", I, OW_STEM + "A list of items to be discussed at a meeting",
  ["minutes", "memo", "quorum", "agenda"], "D",
  "One-word substitution: meeting terms",
  "The 'agenda' is the list of items to be discussed at a meeting.",
  ["Before the meeting: list of topics = agenda"],
  "'Minutes' are the written record of what was said after the meeting. A 'memo' is a short note. A 'quorum' is the "
  "minimum number of members needed for a valid meeting.", 20)

Q(OW, "Single word for a phrase", A, OW_STEM + "A speech delivered without any preparation",
  ["extempore", "verbatim", "soliloquy", "rhetoric"], "A",
  "One-word substitution: speech terms",
  "An 'extempore' speech is delivered on the spot, without preparation.",
  ["Key words: 'without preparation'", "Word: extempore"],
  "'Verbatim' means word for word. A 'soliloquy' is speaking one's thoughts aloud when alone, especially in a play. "
  "'Rhetoric' is the art of persuasive speaking.", 25)

Q(OW, "Single word for a phrase", A, OW_STEM + "The study of the origin and history of words",
  ["entomology", "philology", "etymology", "lexicography"], "C",
  "One-word substitution: fields of study",
  "'Etymology' is the study of where words come from and how their forms and meanings have changed.",
  ["Key words: origin and history of words", "Word: etymology"],
  "'Entomology' is the study of insects. 'Philology' is the broader study of language in historical texts. "
  "'Lexicography' is the compiling of dictionaries.", 25)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", B, AP_STEM + "The bank will open a new branch in our village next month.",
  ["A new branch would be opened in our village by the bank next month.",
   "A new branch is opened in our village by the bank next month.",
   "A new branch will be opened in our village by the bank next month.",
   "A new branch will be open in our village by the bank next month."], "C",
  "Simple future active → will be + past participle",
  "'Will open' becomes 'will be opened', the object 'a new branch' becomes the subject, and 'the bank' becomes the "
  "agent.",
  ["Object 'a new branch' → subject", "will + V1 → will be + V3", "Agent: 'by the bank'"],
  "A changes 'will' to 'would'. B changes the tense to present. D uses the adjective 'open' instead of the past "
  "participle 'opened'.", 25)

Q(AP, "Voice conversion", I, AP_STEM + "Do not touch the electric panel.",
  ["Let the electric panel not be touched.", "The electric panel is not touched.",
   "Let not the electric panel touched.", "The electric panel should not touching."], "A",
  "Passive of a negative command: Let + object + not + be + past participle",
  "An imperative becomes passive with 'Let': 'Let the electric panel not be touched.'",
  ["Imperative → passive with 'Let'", "Object 'the electric panel' after 'Let'",
   "Negative: 'not be touched'"],
  "B turns the command into a statement of fact. C leaves out 'be'. D is ungrammatical ('should not touching').", 30)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", B, DS_STEM + "The customer said, \"I want to close my account.\"",
  ["The customer said that he wants to close his account.",
   "The customer said that I wanted to close my account.",
   "The customer told that he wanted to close his account.",
   "The customer said that he wanted to close his account."], "D",
  "Statement in reported speech: past reporting verb → backshift; first person → third person",
  "After 'said', the present 'want' moves back to 'wanted', and 'I/my' become 'he/his': 'The customer said that he "
  "wanted to close his account.'",
  ["Reporting verb 'said' is past → 'want' → 'wanted'", "'I' → 'he', 'my' → 'his'",
   "'said that' needs no object"],
  "A keeps the present 'wants'. B keeps the first person 'I' and 'my'. C uses 'told' without an object ('told "
  "someone').", 30)

Q(DS, "Narration change", I, DS_STEM + "The clerk asked me, \"Have you brought your passbook?\"",
  ["The clerk asked me had I brought my passbook.",
   "The clerk asked me whether I had brought my passbook.",
   "The clerk asked me whether I have brought my passbook.",
   "The clerk asked me that whether I had brought my passbook."], "B",
  "Yes/no question in reported speech: 'whether/if' + statement order + backshift",
  "A yes/no question is reported with 'whether' (or 'if'), in statement order, with the present perfect moved back "
  "to the past perfect: 'whether I had brought my passbook'.",
  ["Yes/no question → 'whether'", "Statement order: 'I had brought'",
   "Present perfect → past perfect; 'you/your' → 'I/my'"],
  "A keeps question order. C does not backshift the tense. D adds 'that' before 'whether'.", 35)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", I,
  SV_STEM + "The quality of the new currency notes ______ much better than that of the old ones.",
  ["are", "is", "have been", "were"], "B",
  "The verb agrees with the head noun, not with a noun in the 'of' phrase",
  "The subject is 'quality' (singular); 'of the new currency notes' only describes it. So the verb is 'is'.",
  ["Head noun: 'quality'", "'of the new currency notes' is a modifier", "Singular subject → 'is'"],
  "'Are', 'have been' and 'were' are plural and wrongly agree with 'notes'.", 25)

Q(SV, "Agreement rules", A,
  SV_STEM + "Bread and butter ______ his usual breakfast before he leaves for the branch.",
  ["are", "have been", "were", "is"], "D",
  "Two nouns joined by 'and' that form a single idea take a singular verb",
  "'Bread and butter' here is one dish, a single idea, so it takes a singular verb: 'Bread and butter is his usual "
  "breakfast.' The singular complement 'his usual breakfast' confirms this.",
  ["Do the two nouns name one item or two? One dish", "Single idea → singular verb",
   "Present habit ('leaves') → 'is'"],
  "'Are', 'have been' and 'were' are plural, which would treat bread and butter as two separate items, against the "
  "singular 'his usual breakfast'.", 35)

Q(SV, "Agreement rules", A,
  SV_STEM + "Not only the manager but also the clerks ______ responsible for the shortfall in the cash.",
  ["is", "was", "are", "has been"], "C",
  "'Not only ... but also': the verb agrees with the nearer subject",
  "With 'not only X but also Y', the verb agrees with Y, the subject nearer to it. Y is 'the clerks' (plural), so the "
  "verb is 'are'.",
  ["Correlative: not only ... but also", "Nearer subject: 'the clerks' (plural)", "Plural verb: 'are'"],
  "'Is', 'was' and 'has been' are singular and wrongly agree with 'the manager'.", 35)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Perfect tenses", B,
  TE_STEM + "The manager ______ just ______ the meeting, so you can see him now.",
  ["has, finished", "had, finished", "is, finishing", "was, finished"], "A",
  "Present perfect with 'just' for a recently completed action that matters now",
  "The meeting ended a moment ago and the result is relevant now ('you can see him now'), so the present perfect is "
  "used: 'has just finished'.",
  ["Clue: 'just' + present result 'you can see him now'", "Recent completed action → present perfect",
   "'has just finished'"],
  "'Had finished' is past perfect and needs a past reference point. 'Is just finishing' means it is not yet over, "
  "so he could not be seen now. 'Was just finished' is a passive form and does not fit.", 25)

Q(TE, "Sequence of tenses", I,
  TE_STEM + "Our teacher told us that the earth ______ round the sun once a year.",
  ["went", "goes", "had gone", "would go"], "B",
  "Sequence of tenses: a universal truth stays in the present even after a past reporting verb",
  "Normally a past reporting verb ('told') moves the verb back. A universal or scientific truth is an exception and "
  "keeps the present tense: 'the earth goes round the sun'.",
  ["Reporting verb 'told' is past", "But the reported fact is a permanent truth",
   "Universal truth → present simple: 'goes'"],
  "'Went', 'had gone' and 'would go' backshift a permanent truth, which makes it sound as if it were true only in "
  "the past or in the future.", 30)

Q(TE, "Perfect tenses", A,
  TE_STEM + "He ______ for the bank for ten years when he was promoted to branch manager.",
  ["has been working", "was working", "had been working", "is working"], "C",
  "Past perfect continuous: an action continuing up to a point in the past",
  "The ten years of work continued up to a past event (his promotion). An action lasting until a past point takes "
  "the past perfect continuous: 'had been working for ten years when he was promoted'.",
  ["Past reference point: 'when he was promoted'", "Duration up to that point: 'for ten years'",
   "Past perfect continuous: 'had been working'"],
  "'Has been working' and 'is working' are present forms that clash with 'was promoted'. 'Was working' does not "
  "express a duration up to a past point with 'for ten years'.", 35)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", B, AR_STEM + "______ sun rises in the east and sets in the west.",
  ["A", "An", "The", "No article"], "C",
  "'The' with things that are unique (the sun, the moon, the earth)",
  "There is only one sun, so it takes the definite article: 'The sun rises in the east.'",
  ["'sun' names a unique object", "Unique objects take 'the'"],
  "'A' and 'An' suggest one of many suns. A singular countable noun like 'sun' cannot stand without an article "
  "here.", 20)

Q(AR, "Definite and indefinite", I, AR_STEM + "______ rich are not always happier than ______ poor.",
  ["A, a", "The, the", "The, a", "No article, no article"], "B",
  "'The' + adjective to refer to a whole class of people (the rich, the poor)",
  "'The rich' and 'the poor' mean rich people and poor people as a class. This pattern needs 'the' + adjective, and "
  "the plural verb 'are' confirms it.",
  ["Adjectives used as plural nouns for a class of people", "Pattern: the + adjective", "'The rich ... the poor'"],
  "'A rich' or 'a poor' cannot stand alone as nouns. Without an article, 'rich' and 'poor' cannot act as subjects "
  "or objects here. C mixes the forms.", 30)

Q(AR, "Definite and indefinite", A, AR_STEM + "______ Ganga is ______ holy river for millions of people.",
  ["A, the", "The, the", "No article, a", "The, a"], "D",
  "'The' before names of rivers; 'a' for one member of a class",
  "Names of rivers take 'the' ('the Ganga'). The second blank describes the river as one of the class of holy "
  "rivers, so it takes 'a': 'a holy river'.",
  ["Rivers take the definite article: 'The Ganga'", "'holy river' classifies it → indefinite 'a'",
   "Option D"],
  "A puts 'a' before a river's name. B ('the holy river') would mean the only holy river, which is not intended. C "
  "omits 'the' before the river's name.", 30)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", B, PP_STEM + "Ever since she was a child, she has been fond ______ reading.",
  ["with", "for", "about", "of"], "D",
  "Fixed preposition: 'fond of'",
  "The adjective 'fond' takes 'of': 'fond of reading'.",
  ["Adjective: 'fond'", "Fixed pairing: 'fond of'"],
  "'Fond with', 'fond for' and 'fond about' are not standard English.", 20)

Q(PP, "Phrasal verbs", I,
  PP_STEM + "The bank plans to ______ its old core-banking software over the next two years and move to a new "
  "system.",
  ["phase out", "phase in", "bring up", "set off"], "A",
  "Phrasal verb 'phase out' = stop using something gradually",
  "The bank is moving to a new system, so the old software will be gradually withdrawn: 'phase out'.",
  ["Context: replacing old software with a new system over two years", "Gradual withdrawal = 'phase out'"],
  "'Phase in' means introduce gradually, which suits the new system, not the old one. 'Bring up' (raise a topic) and "
  "'set off' (start a journey, trigger) do not fit.", 30)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"

Q(CN, "Sentence connectors", I,
  "Choose the connector that best fills the blank.\n"
  "______ the new queue-management software was installed, complaints about waiting time have fallen sharply.",
  ["Even though", "Ever since", "Unless", "So that"], "B",
  "Time connector 'ever since' + present perfect in the main clause",
  "The fall in complaints has continued from the time the software was installed. 'Ever since' marks the starting "
  "point, and the present perfect 'have fallen' confirms a period running up to now.",
  ["Relation: the second event follows from and continues after the first", "Main clause: present perfect",
   "Connector: 'Ever since'"],
  "'Even though' sets up a contrast, but better software reducing complaints is expected, not surprising. 'Unless' "
  "(condition) and 'So that' (purpose) do not fit the relationship.", 30)

Q(CN, "Sentence connectors", A,
  "Choose the connector that best fills the blank.\n"
  "The bank's profits fell this year because of higher provisions. ______, its asset quality improved, with bad loans "
  "at their lowest level in a decade.",
  ["Consequently", "Similarly", "Nonetheless", "Hence"], "C",
  "Concession connector: a positive point despite a negative one",
  "Sentence 1 is negative (profits fell); sentence 2 is positive (asset quality improved). 'Nonetheless' introduces "
  "a point that holds in spite of the earlier one.",
  ["Sentence 1: negative", "Sentence 2: positive", "Contrast/concession → 'Nonetheless'"],
  "'Consequently' and 'Hence' would make better asset quality a result of falling profits, which is not the logic. "
  "'Similarly' signals a point of the same kind, but the second point is the opposite in tone.", 35)

Q(CN, "Starters and linkers", A,
  "Combine the two sentences into one, starting with 'Provided that'.\n"
  "The borrower repays this loan on time. He will get a lower interest rate on his next loan.",
  ["Provided that the borrower will repay this loan on time, he gets a lower interest rate on his next loan.",
   "Provided that the borrower repays this loan on time, but he will get a lower interest rate on his next loan.",
   "Provided that repaying this loan on time, the borrower will get a lower interest rate on his next loan.",
   "Provided that the borrower repays this loan on time, he will get a lower interest rate on his next loan."], "D",
  "'Provided that' introduces a condition: present simple in the condition, 'will' in the result",
  "'Provided that' works like 'if': the condition uses the present simple ('repays') and the result uses 'will' ('he "
  "will get').",
  ["'Provided that' = on condition that", "Condition clause: present simple 'repays'",
   "Result clause: 'will get', with no extra connector"],
  "A uses 'will' in the condition clause and the present in the result. B adds 'but', which wrongly joins a "
  "condition to its result. C puts a participle after 'Provided that', which needs a full clause.", 40)

Q(CN, "Sentence connectors", A,
  "Choose the connector that best fills the blank.\n"
  "The scheme was meant to help small farmers; ______, most of its benefits went to large landowners.",
  ["in practice", "accordingly", "likewise", "for instance"], "A",
  "Contrast between intention and outcome: 'in practice'",
  "The first clause states the intention; the second states what actually happened, which was different. 'In "
  "practice' introduces the real outcome as against the plan.",
  ["Clause 1: what the scheme was meant to do", "Clause 2: what actually happened (the opposite)",
   "Connector of reality vs intention: 'in practice'"],
  "'Accordingly' would make the outcome follow from the intention. 'Likewise' signals similarity. 'For instance' "
  "introduces an example, but clause 2 is not an example of clause 1.", 35)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_002_plan.json").read_text(encoding="utf-8"))
eng = next(s for s in plan["subjects"] if s["subject"] == EN)
have = Counter((q["topic"], q["difficulty"]) for q in QS)
for t in eng["topics"]:
    for d, n in t["quota"].items():
        assert have[(t["topic"], d)] == n, (t["topic"], d, have[(t["topic"], d)], n)
    for q in QS:
        if q["topic"] == t["topic"]:
            assert q["subtopic"] in t["subtopics"], (q["topic"], q["subtopic"])
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
        # the number of blanks / bold words in the passage equals the number of questions on it
        size = sum(1 for x in QS if x.get("stimulus_id") == q["stimulus_id"])
        assert f"({size + 1})" not in content, q["stimulus_id"]
    if q["topic"] == ED:
        assert q["options"][3]["text"] == "No error"
    if q["topic"] in (SI, PR) or (q["topic"] == CL and q["subtopic"] == "Error-based cloze"):
        assert q["options"][3]["text"] in (NI, NR), q["question_id"]
    if q["topic"] in (PJ, SR):
        # every option is a permutation of the sentence labels shown in the stem
        labels = sorted(q["options"][0]["text"])
        assert all(sorted(o["text"]) == labels and len(set(o["text"])) == len(labels) for o in q["options"])
        for lab in labels:
            assert f"({lab})" in q["question_text"], (q["question_id"], lab)
    assert len({o["text"] for o in q["options"]}) == 4, q["question_id"]

# no reused stem across the earlier English files
earlier = set()
for f in ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json"):
    for q in json.loads((ROOT / "batches" / f).read_text(encoding="utf-8"))["questions"]:
        if q["subject"] == EN:
            earlier.add(q["question_text"].strip().lower())
for q in QS:
    if q.get("stimulus_id") is None and q["topic"] not in (SC, WU, VO):  # shared fixed stems are allowed there
        assert q["question_text"].strip().lower() not in earlier, q["question_id"]

keys = Counter(q["correct_answer"] for q in QS)
assert max(keys.values()) <= 0.28 * len(QS) and min(keys.values()) >= 0.22 * len(QS), keys

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_002",
    "created_at": TODAY,
    "notes": "BATCH_002 English Language part: 150 original questions (BANK_ENG_000154 to BANK_ENG_000303). Six "
             "reading passages (27 questions) and five cloze passages (23 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 or BATCH_001; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules not tested in earlier batches. Each answer was "
             "set by the author and re-solved in a separate pass without the key. Pending human review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_002_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))})")
