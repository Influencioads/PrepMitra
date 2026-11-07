"""Writes batches/parts/BATCH_003_ENG.json: the 150 English Language questions of BATCH_003.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000, BATCH_001 and BATCH_002, and the grammar rules, idioms and words tested are ones not tested in those
batches. Run from anywhere:

    python docs/question-bank/tools/batch_003/english.py

Structural checks (quota per topic and difficulty, subtopics, ID range, passage length, set sizes, option count, cloze
blank numbering, 'No error' / 'No replacement' placement, para-jumble option validity, repeated stems against all
earlier English files, answer-key balance) are asserted before anything is written.
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
FIRST_ID = 304
FIRST_STIM = 3001
EARLIER = ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json", "parts/BATCH_002_ENG.json")

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

# ---------------------------------------------------------------- RC 1 (Basic, 5)
P1 = stim("Seeds that farmers keep", (
    "In many Indian villages, farmers once kept a portion of every harvest aside as seed for the next season. "
    "Grandmothers stored grain in earthen pots sealed with mud and ash, and families exchanged seeds at weddings and "
    "fairs. Over time, this practice faded. High-yielding hybrid seeds, sold in bright packets in the market town, "
    "promised bigger harvests, and many farmers stopped saving their own.\n\n"
    "The new seeds did raise yields, especially where water and fertiliser were plentiful. But they came with a "
    "catch. Hybrid seeds do not breed true, so a farmer who saves them finds that the next crop is weaker and uneven. "
    "He must therefore buy fresh seed every year, often on credit, and the cost rises with each season. In a dry year, "
    "when the crop fails, the farmer is left with a loan and nothing to show for it.\n\n"
    "Community seed banks are an attempt to bring back the old habit in an organised form. A group of farmers, often "
    "led by women, collects seeds of local varieties, cleans and dries them, and stores them in a common room. A "
    "member who borrows a kilogram of seed at sowing time returns two kilograms after the harvest, so the stock grows "
    "from year to year. Records are kept in a simple register, and the seeds are tested for germination before they "
    "are lent.\n\n"
    "The local varieties held in these banks may not match hybrids in a good year, but many of them tolerate drought, "
    "pests and poor soil far better. For a small farmer who cannot afford irrigation, a crop that yields a little less "
    "but rarely fails completely can be the wiser choice. Seed banks also preserve varieties that might otherwise "
    "disappear forever, along with the knowledge of how to grow and cook them.\n\n"
    "Seed banks are not a rejection of modern science. Several of them work with agricultural universities to improve "
    "local varieties without losing their toughness. Their real value lies in giving farmers a choice: to buy seed "
    "when it suits them, and to rely on their own when it does not."))

Q(RC, "Factual", B,
  "According to the passage, why must a farmer who grows hybrid seeds buy fresh seed every year?",
  ["Government rules do not allow farmers to save hybrid seed.",
   "Hybrid seed cannot be stored in earthen pots.",
   "Seed saved from a hybrid crop gives a weaker and uneven crop.",
   "Seed shops refuse to buy back unused hybrid seed."], "C",
  "Locating a stated reason",
  "Paragraph 2 says hybrid seeds 'do not breed true, so a farmer who saves them finds that the next crop is weaker "
  "and uneven. He must therefore buy fresh seed every year.'",
  ["Find 'buy fresh seed every year' in paragraph 2", "Read the sentence before it: the cause",
   "Saved hybrid seed gives a weaker, uneven crop: option C"],
  "No rule (A), storage problem (B) or buy-back by shops (D) is mentioned. The earthen pots belong to the old "
  "practice of saving local seed.", 50, P1, 1)

Q(RC, "Factual", B,
  "How, according to the passage, does the stock of a community seed bank grow from year to year?",
  ["Each member who borrows seed returns twice the quantity after the harvest.",
   "The government adds fresh seed to the bank every season.",
   "Agricultural universities donate hybrid seed to the bank.",
   "Members buy seed in the market town and deposit it in the bank."], "A",
  "Locating a stated mechanism",
  "Paragraph 3 says a member who borrows a kilogram at sowing time 'returns two kilograms after the harvest, so the "
  "stock grows from year to year'.",
  ["Find 'the stock grows' in paragraph 3", "Mechanism: borrow one kilogram, return two", "Option A"],
  "Government additions (B) are not mentioned. The universities help improve local varieties; they do not donate "
  "hybrid seed (C). Buying seed in the market (D) is what seed banks help farmers avoid.", 50, P1, 2)

Q(RC, "Factual", B,
  "Which of the following is NOT mentioned in the passage as part of the way a seed bank works?",
  ["Seeds are cleaned and dried before storage.",
   "Members pay a yearly fee in cash to the group.",
   "Records are kept in a simple register.",
   "Seeds are tested for germination before they are lent."], "B",
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 3 mentions cleaning and drying (A), a simple register (C) and germination tests (D). No cash fee is "
  "mentioned; members repay in seed, not money.",
  ["Paragraph 3: cleans and dries (A), register (C), germination test (D)",
   "Repayment is in seed: two kilograms for one", "A cash fee is not mentioned: B"],
  "A, C and D are all stated in paragraph 3, so none of them can be the 'NOT mentioned' answer.", 50, P1, 3)

Q(RC, "Inference", B,
  "Why, according to the passage, might a small farmer without irrigation prefer local varieties to hybrids?",
  ["Local varieties always give higher yields than hybrids.",
   "Local varieties are sold at a higher price in the market town.",
   "Hybrid seeds cannot be grown without the help of a university.",
   "Local varieties yield a little less but rarely fail completely in hard conditions."], "D",
  "Inference: weighing yield against risk",
  "Paragraph 4 says local varieties 'may not match hybrids in a good year' but tolerate drought, pests and poor soil. "
  "For a farmer without irrigation, a crop that 'rarely fails completely can be the wiser choice'.",
  ["Farmer's situation: no irrigation, so drought is a real risk",
   "Local varieties: slightly lower yield, much lower risk of total failure", "Option D"],
  "A contradicts the passage, which admits local varieties may yield less in a good year. Market prices (B) are not "
  "discussed. C is not stated; universities work with seed banks but hybrids do not need them.", 55, P1, 4)

Q(RC, "Tone and title", B,
  "Which of the following is the most suitable title for the passage?",
  ["Why Hybrid Seeds Should Be Banned", "The Science of Plant Breeding",
   "Wedding Customs of Rural India", "Seed Banks: Giving Farmers a Choice"], "D",
  "A title must cover the main idea of the whole passage",
  "The passage traces the decline of seed saving, the drawbacks of relying only on bought hybrid seed, how community "
  "seed banks work and why they matter. Its last sentence names their value: giving farmers a choice.",
  ["Paras 1–2: old habit lost; problems with depending on hybrids",
   "Paras 3–4: how seed banks work and why local varieties help",
   "Para 5: seed banks give farmers a choice: D"],
  "A goes too far: the passage says seed banks are 'not a rejection of modern science'. B is far wider than the "
  "passage. C picks up one detail from the first paragraph.", 45, P1, 5)

# ---------------------------------------------------------------- RC 2 (Basic, 4)
P2 = stim("Pumps that run on sunshine", (
    "For decades, farmers in many parts of India have watered their fields with pumps run on diesel or on grid "
    "electricity. Diesel is expensive and its price keeps changing, while the power supplied to farms often arrives "
    "for only a few hours a day, sometimes in the middle of the night. A farmer may have to walk to his field at two "
    "in the morning simply because that is when the current comes.\n\n"
    "Solar pumps offer a way out of this daily struggle. Panels set up beside the field run the pump during daylight, "
    "when the farmer is already at work, and the fuel, sunlight, costs nothing. Once the pump is installed, the cost of "
    "running it is very low, and there is no smoke or noise. Government schemes now meet a large part of the purchase "
    "price, which has brought these pumps within the reach of many small farmers.\n\n"
    "The benefits, however, come with a risk. Because water from a solar pump is almost free, a farmer has little "
    "reason to use it carefully. In areas where groundwater levels are already falling, free pumping could drain "
    "aquifers even faster, leaving everyone with deeper and drier wells. Experts therefore suggest that solar pumps "
    "should be combined with drip irrigation, which delivers water directly to the roots of plants and wastes very "
    "little.\n\n"
    "Another idea being tried in some states is to connect solar pumps to the electricity grid. On days when the "
    "farmer does not need to irrigate, the power from his panels flows into the grid, and he is paid for it. This "
    "turns the sun into a second crop. It also gives the farmer a reason to save water, since every unit of power he "
    "does not use for pumping can be sold.\n\n"
    "Solar pumps alone will not solve the problems of Indian agriculture. Used wisely, though, they can cut costs, free "
    "farmers from night-time irrigation and, if the incentives are right, help protect the water on which every farm "
    "depends."))

Q(RC, "Factual", B,
  "According to the passage, why might a farmer have to go to his field at two in the morning?",
  ["Diesel is cheaper at night.",
   "Electricity for farms is often supplied only at certain hours, sometimes at night.",
   "Solar panels work best before sunrise.",
   "Drip irrigation must be done when it is cool."], "B",
  "Locating a stated reason",
  "Paragraph 1 says farm power 'often arrives for only a few hours a day, sometimes in the middle of the night', so "
  "the farmer goes at two in the morning 'because that is when the current comes'.",
  ["Find 'two in the morning' in paragraph 1", "Reason: that is when the current comes", "Option B"],
  "A: the passage says diesel is expensive and its price keeps changing, not that it is cheaper at night. C is "
  "absurd: solar panels need daylight. D is not mentioned.", 45, P2, 1)

Q(RC, "Factual", B,
  "What risk of solar pumps does the passage point out?",
  ["The panels are easily stolen from the fields.",
   "The pumps make a great deal of noise.",
   "Government schemes may stop paying for them.",
   "Because pumping costs almost nothing, farmers may overuse groundwater."], "D",
  "Locating a stated drawback",
  "Paragraph 3 says that because water from a solar pump is almost free, a farmer has little reason to use it "
  "carefully, and free pumping could drain aquifers faster.",
  ["Find 'risk' in paragraph 3", "Cause: water is almost free", "Effect: overuse of groundwater: D"],
  "Theft (A) and the end of government schemes (C) are not mentioned. B contradicts paragraph 2, which says the "
  "pumps make no smoke or noise.", 45, P2, 2)

Q(RC, "Inference", B,
  "How, according to the passage, does connecting solar pumps to the grid encourage farmers to save water?",
  ["Power the farmer does not use for pumping can be sold, so saving water earns him money.",
   "The grid company limits the amount of water each farmer may pump.",
   "Grid-connected pumps cannot run for more than a few hours a day.",
   "Farmers who join the grid must also install drip irrigation."], "A",
  "Inference: following an incentive",
  "Paragraph 4 says the farmer is paid for the power his panels send to the grid, and 'every unit of power he does "
  "not use for pumping can be sold'. Pumping less water therefore earns him more.",
  ["Grid link: unused solar power is sold", "Less pumping → more power to sell → more income",
   "So the farmer gains by saving water: A"],
  "B, C and D describe limits or conditions that the passage never mentions. The incentive works through payment, "
  "not through rules.", 55, P2, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'drain' as used in the passage ('free pumping could drain "
  "aquifers even faster')?",
  ["fill", "clean", "empty", "measure"], "C",
  "Vocabulary in context: drain = use up, empty",
  "The sentence says overuse could leave 'deeper and drier wells'. Pumping out underground water faster than it is "
  "replaced empties the aquifers.",
  ["Context: groundwater levels already falling", "Result: deeper and drier wells",
   "So 'drain' means empty or use up"],
  "'Fill' is the opposite. 'Clean' and 'measure' do not explain why wells would become deeper and drier.", 35, P2, 4)

# ---------------------------------------------------------------- RC 3 (Intermediate, 5)
P3 = stim("Forests that face the sea", (
    "Along much of India's coastline, a strip of dense, tangled forest grows where the land meets the sea. Mangroves, "
    "trees that can survive in salty water and are flooded twice a day by the tide, were long regarded as wasteland. "
    "They were cleared to make room for ports, prawn farms, salt pans and housing, and few people mourned their "
    "loss.\n\n"
    "That view has changed, largely because of what happens when a cyclone strikes. A belt of mangroves acts like a "
    "natural breakwater. Its roots, which rise out of the mud in thick clusters, slow down the waves and trap the "
    "sediment the water carries, so that the surge reaching the villages behind is weaker and lower. Studies after "
    "major cyclones on the eastern coast found that villages sheltered by healthy mangroves generally suffered less "
    "damage than nearby villages whose forests had been cleared, although the size of the effect depended on the "
    "width of the forest and the strength of the storm.\n\n"
    "Mangroves are also nurseries for the sea. Many fish, crabs and prawns spend their early lives among the roots, "
    "where they are protected from larger predators, before moving out into open water. Fishing communities that "
    "depend on these catches therefore have a direct stake in the forest's health. In addition, mangrove soils store "
    "large amounts of carbon, which would be released into the air if the forests were destroyed.\n\n"
    "Restoring mangroves, however, is more difficult than simply planting saplings. Many past planting drives failed "
    "because the young trees were placed where the tide did not reach them properly, or because the species chosen "
    "did not suit the site. The most successful projects have begun by restoring the natural flow of tidal water and "
    "have involved local communities, who know the coast and have a reason to protect what grows on it.\n\n"
    "None of this means that mangroves can replace sea walls, cyclone shelters or early-warning systems. It does mean "
    "that a forest once dismissed as useless may be among the cheapest and most lasting forms of coastal protection "
    "available, provided that it is allowed to grow where nature intended."))

Q(RC, "Factual", I,
  "According to the passage, how does a belt of mangroves reduce the damage caused by a cyclone?",
  ["It warns villagers in advance that a storm is approaching.",
   "It stores carbon that would otherwise make storms stronger.",
   "Its roots slow the waves and trap sediment, so the surge reaching villages is weaker and lower.",
   "It provides timber for building stronger houses."], "C",
  "Locating a stated mechanism",
  "Paragraph 2 says the roots 'slow down the waves and trap the sediment the water carries, so that the surge reaching "
  "the villages behind is weaker and lower'.",
  ["Find 'natural breakwater' in paragraph 2", "Mechanism: roots slow waves and trap sediment",
   "Result: weaker, lower surge: C"],
  "A: early warning is something mangroves cannot replace, according to the last paragraph. B: carbon storage is a "
  "separate benefit and is not linked to storm strength. D: timber is never mentioned.", 50, P3, 1)

Q(RC, "Inference", I,
  "The clause 'although the size of the effect depended on the width of the forest and the strength of the storm' "
  "suggests that",
  ["the protection mangroves give is real but varies, and is not unlimited",
   "mangroves give no protection against strong storms",
   "only very wide forests should be protected",
   "the studies after the cyclones were unreliable"], "A",
  "Inference: the purpose of a qualifying clause",
  "The main clause reports a benefit (less damage behind healthy mangroves); the 'although' clause qualifies it: how "
  "much protection a forest gives depends on its width and the storm's strength. The benefit is real but varies.",
  ["Main claim: mangrove villages generally suffered less damage",
   "'although' adds a limit, not a denial", "So the protection is real but variable: A"],
  "B turns a limit into a denial and contradicts 'generally suffered less damage'. C is a policy the passage never "
  "proposes. D questions the studies, which the author relies on.", 55, P3, 2)

Q(RC, "Factual", I,
  "Which of the following is NOT mentioned in the passage as a benefit of mangroves?",
  ["Sheltering young fish, crabs and prawns", "Storing carbon in their soils",
   "Reducing the force of storm surges", "Providing timber for coastal housing"], "D",
  "Factual (NOT) question",
  "The passage names three benefits: protection from surges (paragraph 2), nurseries for marine life and carbon "
  "storage (paragraph 3). Housing appears only as one of the reasons mangroves were cleared, not as a benefit.",
  ["Para 2: weaker surges (C)", "Para 3: young fish, crabs, prawns (A); carbon (B)",
   "Housing is a reason for clearing them, not a benefit: D"],
  "A, B and C are each stated as benefits, so none of them is the 'NOT mentioned' answer.", 50, P3, 3)

Q(RC, "Inference", I,
  "What can be inferred from the passage about successful mangrove restoration?",
  ["It depends mainly on planting as many saplings as possible.",
   "It depends on suitable tidal conditions and the involvement of local people more than on the number of saplings.",
   "It can be achieved quickly by choosing a single fast-growing species everywhere.",
   "It is no longer necessary, because sea walls give better protection."], "B",
  "Inference from contrasting failures and successes",
  "Paragraph 4 says past drives failed when trees were planted where the tide did not reach them or the wrong species "
  "was chosen, while the best projects restored tidal flow and involved local communities. Success therefore turns on "
  "site conditions and people, not on sapling numbers.",
  ["Failures: wrong place for the tide, wrong species", "Successes: tidal flow restored, local people involved",
   "Conclusion: conditions and community matter more than numbers: B"],
  "A is what the passage says is not enough ('more difficult than simply planting saplings'). C contradicts the "
  "failure caused by species that did not suit the site. D contradicts the last paragraph, which values mangroves "
  "alongside sea walls.", 55, P3, 4)

Q(RC, "Tone and title", I,
  "Which of the following best describes the author's attitude towards mangroves as a form of coastal protection?",
  ["Dismissive", "Uncritically enthusiastic", "Appreciative but measured", "Indifferent"], "C",
  "Tone: look for praise together with limits",
  "The author praises mangroves as among the cheapest and most lasting forms of protection, but also says they cannot "
  "replace sea walls or early warnings, that their effect varies and that restoration is hard. That is appreciation "
  "with clear limits.",
  ["Positive: 'natural breakwater', 'cheapest and most lasting'",
   "Limits: effect varies; cannot replace sea walls; restoration difficult",
   "Positive but balanced: C"],
  "'Dismissive' is the old view the author rejects. 'Uncritically enthusiastic' ignores the stated limits. "
  "'Indifferent' does not fit a passage that argues a case.", 45, P3, 5)

# ---------------------------------------------------------------- RC 4 (Intermediate, 4)
P4 = stim("The humble city bus", (
    "When Indian cities talk about public transport, the conversation usually turns to metro rail. Gleaming new lines "
    "are inaugurated with ceremony, and their stations become landmarks. The city bus, by comparison, receives little "
    "attention. Yet in most cities buses carry far more passengers than the metro does, and they reach neighbourhoods "
    "that no rail line will ever serve.\n\n"
    "The neglect shows. In many cities, the number of buses has not kept pace with the population, so waits are long "
    "and vehicles are packed at peak hours. Buses share crowded roads with cars and two-wheelers and move at a crawl, "
    "which pushes anyone who can afford a vehicle to buy one. More vehicles mean more congestion, which slows the "
    "buses further, and the cycle repeats.\n\n"
    "Breaking this cycle does not require costly technology. A dedicated lane, painted and enforced, can let a bus "
    "move faster than the cars beside it. Reliable timetables, displayed at stops and on phones, allow commuters to "
    "plan their journeys instead of waiting anxiously. Low, level boarding helps the elderly, people with disabilities "
    "and parents with small children. None of these measures costs more than a fraction of a single kilometre of "
    "metro line.\n\n"
    "The obstacle is less money than priority. A bus lane takes road space away from private cars, and car owners, "
    "though fewer in number than bus passengers, tend to be more influential. Officials who would happily cut the "
    "ribbon on a new flyover hesitate to anger motorists by narrowing a road to make room for buses.\n\n"
    "Cities that have made buses work, in India and abroad, share one feature: their leaders treated the bus as the "
    "backbone of the transport system rather than as a service for those with no other choice. Metro lines have their "
    "place, but a city that wants to move most of its people quickly and cheaply will have to start with the vehicle "
    "that already carries them."))

Q(RC, "Factual", I,
  "According to the passage, how do buses compare with the metro in most Indian cities?",
  ["Buses carry far more passengers and reach neighbourhoods that rail lines will never serve.",
   "Buses are faster than the metro at peak hours.",
   "Buses receive more public attention than the metro.",
   "Buses cost more to run per kilometre than the metro."], "A",
  "Locating a stated comparison",
  "Paragraph 1 says that 'in most cities buses carry far more passengers than the metro does, and they reach "
  "neighbourhoods that no rail line will ever serve'.",
  ["Find the comparison in paragraph 1 ('Yet in most cities ...')", "Two points: more passengers, wider reach",
   "Option A"],
  "B contradicts paragraph 2: buses 'move at a crawl'. C reverses paragraph 1: buses receive 'little attention'. D: "
  "the passage compares the cost of bus measures with metro construction, not running costs per kilometre.",
  50, P4, 1)

Q(RC, "Inference", I,
  "What does 'the cycle' in 'and the cycle repeats' (paragraph 2) refer to?",
  ["The daily timetable of buses on a route",
   "The rise and fall of fares every year",
   "Commuters switching between buses and bicycles",
   "Slow buses push people to buy vehicles, which adds to congestion and slows buses further"], "D",
  "Inference: identify what a summarising phrase refers to",
  "The sentences before it describe a loop: buses crawl → people who can afford it buy vehicles → more vehicles mean "
  "more congestion → buses slow down further. 'The cycle' is this self-reinforcing loop.",
  ["Trace paragraph 2: slow buses → more private vehicles", "More vehicles → more congestion → slower buses",
   "The loop returns to its start: D"],
  "A, B and C name cycles the paragraph never describes; fares and bicycles are not mentioned.", 50, P4, 2)

Q(RC, "Inference", I,
  "According to the author, what is the main obstacle to improving bus services?",
  ["The high cost of the technology needed",
   "Officials' reluctance to take road space from car owners, who are more influential",
   "A shortage of trained bus drivers",
   "Passengers' dislike of fixed timetables"], "B",
  "Inference: the author's stated main obstacle",
  "Paragraph 4 begins: 'The obstacle is less money than priority.' Bus lanes take space from cars, and car owners are "
  "more influential, so officials hesitate to anger them.",
  ["Key sentence: 'The obstacle is less money than priority'",
   "Bus lanes take road space from cars", "Influential motorists → officials hesitate: B"],
  "A contradicts paragraph 3, which says the measures do not need costly technology. C is never mentioned. D "
  "contradicts paragraph 3, which presents reliable timetables as a help to commuters.", 50, P4, 3)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'backbone' as used in the passage ('treated the bus as "
  "the backbone of the transport system')?",
  ["afterthought", "rival", "mainstay", "luxury"], "C",
  "Vocabulary in context: figurative 'backbone'",
  "The backbone is the part that supports everything else. Treating the bus as the backbone, 'rather than as a service "
  "for those with no other choice', means treating it as the main support of the system: its mainstay.",
  ["Contrast: backbone vs 'a service for those with no other choice'", "So backbone = the main support",
   "'mainstay'"],
  "'Afterthought' is close to the opposite. 'Rival' and 'luxury' do not fit a system's central support.", 40, P4, 4)

# ---------------------------------------------------------------- RC 5 (Advanced, 6)
P5 = stim("When the number becomes the goal", (
    "A principle familiar to economists and administrators holds that when a measure becomes a target, it ceases to "
    "be a good measure. The idea sounds paradoxical, but examples are easy to find. A hospital judged by how quickly it "
    "discharges patients may send people home before they are ready, only to see them readmitted a week later. A "
    "school rewarded for its pass rate may quietly discourage weaker students from sitting the examination. In each "
    "case the number improves while the thing it was meant to reflect stays the same or gets worse.\n\n"
    "The reason is not that people are dishonest, though some are. It is that any single figure captures only part of "
    "what we care about. A pass rate tells us something about learning, but not everything; a discharge time tells us "
    "something about efficiency, but nothing about recovery. As long as nobody is paid or punished according to the "
    "figure, it remains a fair, if partial, signal. Once careers depend on it, effort flows towards whatever moves the "
    "number most cheaply, and the gap between the figure and the reality it was meant to track widens.\n\n"
    "Banking offers its own illustrations. A branch given a target for opening new accounts may open thousands that "
    "are never used. A loan officer assessed on the volume of credit disbursed has little reason to dwell on whether "
    "the borrowers can repay, since the disbursement is counted today and any default arrives, if at all, years later "
    "and on someone else's watch.\n\n"
    "None of this is an argument against measurement. An organisation that measures nothing cannot tell success from "
    "failure, and the absence of targets usually means that decisions are driven by habit or by whoever speaks "
    "loudest. The lesson is rather that numbers should be treated as instruments, not idols. Good practice includes "
    "using several indicators at once, so that gaming one shows up as a decline in another; changing targets from time "
    "to time before they can be learned and exploited; and, above all, pairing figures with judgement, exercised by "
    "people who understand the work well enough to notice when a number has stopped telling the truth.\n\n"
    "The most dangerous moment, paradoxically, is when a measure appears to be working best. A figure that rises "
    "steadily, year after year, may be a sign of genuine progress, or a sign that people have simply become skilled at "
    "producing it."))

Q(RC, "Inference", A,
  "The examples of the hospital and the school in the first paragraph are used mainly to show that",
  ["a figure can improve even while the outcome it is meant to reflect stays the same or worsens",
   "hospitals and schools are run less efficiently than banks",
   "most administrators deliberately falsify their records",
   "discharge times and pass rates should never be measured"], "A",
  "Inference: the function of examples",
  "Both examples end the same way: the number (discharge speed, pass rate) improves, but the real goal (recovery, "
  "learning) does not. The paragraph's last sentence states this directly.",
  ["Hospital: faster discharges, but readmissions", "School: higher pass rate, but weaker students kept out",
   "Shared point (last sentence of para 1): A"],
  "B makes a comparison the passage never makes. C contradicts paragraph 2: 'The reason is not that people are "
  "dishonest'. D contradicts paragraph 4: 'None of this is an argument against measurement'.", 60, P5, 1)

Q(RC, "Factual", A,
  "According to the passage, why does a figure become less reliable once careers depend on it?",
  ["People stop recording it accurately because it is tedious to collect.",
   "It becomes too expensive for the organisation to measure.",
   "Dishonest people are attracted to jobs that carry targets.",
   "Effort shifts to whatever moves the figure most cheaply, so the figure drifts away from the reality it tracked."],
  "D",
  "Locating the author's explanation",
  "Paragraph 2: 'Once careers depend on it, effort flows towards whatever moves the number most cheaply, and the gap "
  "between the figure and the reality it was meant to track widens.'",
  ["Find 'Once careers depend on it' in paragraph 2", "Mechanism: effort goes to the cheapest way of moving the number",
   "Result: figure and reality drift apart: D"],
  "A and B give reasons the passage never mentions. C contradicts the author, who says the reason is 'not that people "
  "are dishonest'.", 60, P5, 2)

Q(RC, "Inference", A,
  "The phrase 'on someone else's watch', used about a loan officer, suggests that",
  ["loan officers are usually transferred before they are trained",
   "defaults are recorded by a different department of the bank",
   "a bad loan's cost is likely to surface after the officer who made it has moved on, so he does not bear it",
   "borrowers deliberately delay repayment until the officer retires"], "C",
  "Inference: meaning of an idiom in context",
  "'On someone else's watch' means during another person's period of responsibility. The disbursement is credited to "
  "the officer today, while any default comes years later, when someone else is in charge, so the officer has little "
  "reason to worry about repayment.",
  ["Idiom: 'on X's watch' = while X is responsible", "Disbursement counted now; default arrives later",
   "So the cost falls on a successor: C"],
  "A and D invent motives and events. B takes 'someone else' too literally; the point is about timing and "
  "responsibility, not departments.", 60, P5, 3)

Q(RC, "Inference", A,
  "With which of the following statements would the author most likely agree?",
  ["Using several indicators together, interpreted by people who understand the work, reduces the risk of gaming.",
   "Organisations would be better off without any targets at all.",
   "A figure that rises steadily every year can safely be taken as proof of progress.",
   "Gaming of targets happens mainly because employees are dishonest."], "A",
  "Inference: the author's recommendations",
  "Paragraph 4 recommends using several indicators at once, 'so that gaming one shows up as a decline in another', "
  "and pairing figures with the judgement of people who understand the work. Option A combines the two.",
  ["Para 4 lists remedies: several indicators; changing targets; judgement",
   "Option A restates two of them"],
  "B contradicts 'None of this is an argument against measurement'. C contradicts the last paragraph, which warns that "
  "a steadily rising figure may reflect skill at producing it. D contradicts 'The reason is not that people are "
  "dishonest'.", 60, P5, 4)

Q(RC, "Vocabulary in context", A,
  "In the sentence 'numbers should be treated as instruments, not idols', the word 'idols' most nearly means",
  ["tools to be used with care", "rough estimates", "temporary fashions", "objects of unquestioning reverence"], "D",
  "Vocabulary in context: figurative 'idols' contrasted with 'instruments'",
  "An instrument is a tool we use and judge; an idol is something worshipped without question. The author warns "
  "against treating numbers as beyond question.",
  ["Contrast pair: instruments (tools) vs idols", "Idol = object of worship",
   "Figurative meaning: something revered without question: D"],
  "A describes 'instruments', the opposite side of the contrast. B and C do not capture the sense of uncritical "
  "devotion.", 45, P5, 5)

Q(RC, "Tone and title", A,
  "Which of the following best describes the author's attitude towards numerical targets?",
  ["Wholly opposed to the use of targets",
   "Uncritically enthusiastic about measurement",
   "Supportive of measurement but wary of treating any single figure as the goal",
   "Indifferent to how organisations are assessed"], "C",
  "Tone: a balanced position stated in the fourth paragraph",
  "The author defends measurement ('An organisation that measures nothing cannot tell success from failure') while "
  "warning, throughout, against making one figure the goal. That is support with caution.",
  ["For measurement: para 4, first two sentences", "Against single-figure targets: paras 1–3 and 5",
   "Balanced: C"],
  "A ignores the defence of measurement. B ignores the passage's many warnings. D does not fit a passage that argues "
  "a definite case.", 50, P5, 6)

# ---------------------------------------------------------------- RC 6 (Advanced, 5)
P6 = stim("The case for keeping cash", (
    "Over the past decade, digital payments in India have grown at a pace few predicted. A vegetable seller with a "
    "printed QR code can now accept money from a stranger in seconds, and many urban consumers go days without touching "
    "a banknote. It is tempting to conclude that cash is a relic, and that the sooner it disappears the better. Such a "
    "conclusion would be premature.\n\n"
    "Cash has qualities that digital money, for all its convenience, does not fully replicate. It works without a "
    "network, a battery or a bank account, which matters in a flood, a power failure or a remote village with patchy "
    "signal. It settles a transaction finally and instantly: once a note changes hands, there is no server to fail and "
    "no payment to reverse. And it offers a degree of privacy that many people value for reasons that have nothing to "
    "do with wrongdoing, such as an elderly widow who prefers that her relatives not see every rupee she spends.\n\n"
    "The usual objections to cash are real but often overstated. It is true that cash can be used to evade tax and "
    "hide illegal income. Yet large-scale evasion increasingly relies on sophisticated devices, such as shell "
    "companies and inflated invoices, rather than suitcases of notes, and digital systems carry risks of their own, "
    "from fraud to outages. A payment system that depends on a single technology is efficient only for as long as that "
    "technology works.\n\n"
    "There is also a question of fairness. Those most comfortable with digital payments tend to be young, urban and "
    "literate; those most reliant on cash tend to be older, poorer or rural. A shop that refuses notes, or a public "
    "service that can be paid for only through an app, shifts the burden of adjustment onto the people least able to "
    "bear it.\n\n"
    "None of this is an argument for resisting digital payments, whose benefits in speed, record-keeping and reach are "
    "considerable. It is an argument for coexistence. A sensible policy would continue to encourage digital "
    "transactions while ensuring that cash remains widely accepted, easy to obtain and genuinely usable. The goal "
    "should be a society in which people choose digital payments because they are better, not because they have been "
    "left with no alternative."))

Q(RC, "Factual", A,
  "Which of the following is NOT mentioned in the passage as a quality of cash?",
  ["It works without a network, a battery or a bank account.",
   "It settles a transaction finally and instantly.",
   "It offers a degree of privacy.",
   "It earns interest for as long as it is held."], "D",
  "Factual (NOT) question",
  "Paragraph 2 lists three qualities: it works without network, battery or account (A); it settles finally and "
  "instantly (B); it offers privacy (C). Earning interest is not mentioned, and notes held as cash earn none.",
  ["Para 2, quality 1: no network needed (A)", "Quality 2: final, instant settlement (B)",
   "Quality 3: privacy (C)", "Interest is not mentioned: D"],
  "A, B and C are all stated in paragraph 2, so none of them can be the 'NOT mentioned' answer.", 50, P6, 1)

Q(RC, "Inference", A,
  "The statement 'A payment system that depends on a single technology is efficient only for as long as that "
  "technology works' implies that",
  ["keeping more than one means of payment makes the system more resilient to failures",
   "digital payments are less efficient than cash in normal times",
   "technology should be removed from payment systems altogether",
   "outages in digital payment systems happen every day"], "A",
  "Inference: unstated implication of a general statement",
  "If a system that relies on one technology fails whenever that technology fails, then keeping an alternative, such "
  "as cash, protects the system during outages. The statement argues for having more than one way to pay.",
  ["Claim: single-technology dependence is fragile", "Implication: alternatives provide a back-up",
   "Fits the passage's call for coexistence: A"],
  "B contradicts the passage, which praises the speed of digital payments. C goes far beyond it; the author wants "
  "coexistence, not removal. D exaggerates; the passage mentions outages only as one risk.", 60, P6, 2)

Q(RC, "Inference", A,
  "How does the author deal with the argument that cash helps people evade tax?",
  ["The author rejects it as entirely false.",
   "The author treats it as a decisive reason to abolish cash.",
   "The author accepts that it has some truth but argues that it is often overstated.",
   "The author does not mention it at all."], "C",
  "Inference: the author's treatment of a counter-argument",
  "Paragraph 3 begins 'The usual objections to cash are real but often overstated', concedes 'It is true that cash "
  "can be used to evade tax', and then argues that large-scale evasion increasingly uses other devices.",
  ["Concession: 'real' and 'It is true that ...'", "Limitation: 'often overstated'; evasion uses shell companies",
   "Partial acceptance: C"],
  "A ignores the concession. B is the opposite of the author's conclusion. D is wrong: paragraph 3 discusses the "
  "point directly.", 55, P6, 3)

Q(RC, "Inference", A,
  "According to the passage, why can a policy that pushes everyone towards digital payments be unfair?",
  ["It raises the prices that urban consumers pay.",
   "It harms shopkeepers more than it harms customers.",
   "Young people find digital payments difficult to use.",
   "It puts the burden of adjusting on older, poorer and rural people, who rely most on cash."], "D",
  "Inference: following the fairness argument",
  "Paragraph 4 contrasts the young, urban and literate, who are comfortable with digital payments, with the older, "
  "poorer or rural, who rely on cash. Refusing cash 'shifts the burden of adjustment onto the people least able to "
  "bear it'.",
  ["Para 4: two groups with different comfort levels", "Cash-only refusals burden the second group",
   "Option D"],
  "A and B are not mentioned. C reverses the passage, which says the young are the most comfortable with digital "
  "payments.", 55, P6, 4)

Q(RC, "Tone and title", A,
  "Which of the following is the most appropriate title for the passage?",
  ["Cash and Digital Payments: The Case for Coexistence", "Why Cash Must Replace Digital Payments",
   "The History of the Banknote in India", "How QR Codes Changed Street Vending"], "A",
  "A title must match the author's conclusion and cover the whole passage",
  "The passage defends the qualities of cash, weighs the objections and ends: 'It is an argument for coexistence.' "
  "Option A captures both the topic and the conclusion.",
  ["Final paragraph: not against digital payments; 'an argument for coexistence'",
   "Body: the qualities of cash, objections, fairness", "Option A"],
  "B reverses the author's position, which welcomes digital payments. C is not discussed. D picks up one example "
  "from the first paragraph.", 50, P6, 5)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic 4 + Intermediate 1)
C1 = stim("Gardens on the roof", (
    "In crowded Indian cities, where every square metre of land is expensive, a quiet green (1) ______ is taking place "
    "on rooftops. Families who once used their terraces only for drying clothes are now growing tomatoes, chillies, "
    "spinach and herbs in pots, old buckets and grow bags. What began as a hobby for a few retired people has "
    "(2) ______ among young professionals, many of whom say that tending plants helps them relax after a long day at "
    "a screen.\n\n"
    "The benefits go beyond the kitchen. A terrace covered with plants absorbs some of the sun's heat, so the rooms "
    "below stay a little cooler in summer. Kitchen waste, instead of being thrown away, can be turned into compost and "
    "returned to the soil, which (3) ______ the amount of garbage a household sends to the landfill. Children who help "
    "with the watering learn where vegetables come from.\n\n"
    "Rooftop farming does have its limits. A roof must be strong enough to bear the weight of wet soil, and water must "
    "be drained carefully so that it does not (4) ______ into the building. Beginners often lose their first plants "
    "to pests or to too much water. Most gardeners, however, learn quickly, and local groups on social media share "
    "tips, seeds and even surplus harvests.\n\n"
    "No one expects rooftops to feed a city. But a family that grows even a part of its own vegetables learns how much "
    "effort goes into producing food and tends to waste less of it. In that sense, the small garden on the terrace may "
    "(5) ______ a lesson far larger than its size."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["silence", "revolution", "dispute", "decline"], "B",
  "Cloze: the paragraph describes a spreading new trend",
  "The paragraph describes many families turning their terraces into gardens. A widespread change that happens without "
  "noise is a 'quiet green revolution'.",
  ["The sentences after the blank describe a growing change", "'quiet ... revolution' = a big change without fuss",
   "'revolution'"],
  "'Silence' and 'dispute' do not describe a change that is 'taking place'. 'Decline' contradicts the growth of the "
  "hobby described next.", 35, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["caught on", "given up", "died out", "set off"], "A",
  "Cloze: phrasal verb 'catch on' = become popular",
  "A hobby that began with a few retired people and is now taken up by young professionals has become popular among "
  "them: it has 'caught on'.",
  ["Contrast: began with a few retired people → now young professionals", "Meaning needed: become popular",
   "'caught on among young professionals'"],
  "'Given up' and 'died out' mean the opposite. 'Set off' means started a journey or triggered something and does not "
  "fit 'among young professionals'.", 35, C1, 2)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=3), ["increases", "doubles", "reduces", "hides"], "C",
  "Cloze: effect of composting on household garbage",
  "Waste that is composted instead of thrown away no longer goes to the landfill, so composting reduces the amount of "
  "garbage a household sends there.",
  ["'instead of being thrown away' → less waste leaves the house", "So the amount sent to landfill falls",
   "'reduces'"],
  "'Increases' and 'doubles' reverse the effect. 'Hides' suggests the garbage still exists but is concealed, which is "
  "not what composting does.", 35, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["fly", "climb", "jump", "seep"], "D",
  "Cloze: verb for water slowly passing through a surface",
  "Badly drained water on a roof can slowly pass through cracks into the rooms below. The verb for this is 'seep'.",
  ["Subject: water on the roof", "Danger: it passes slowly through into the building", "'seep into the building'"],
  "Water does not 'fly', 'climb' or 'jump' into a building; none of these describes slow leakage.", 35, C1, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["lose", "deny", "carry", "waste"], "C",
  "Cloze: 'carry a lesson' = contain or convey a lesson",
  "The last paragraph says a family learns about the effort behind food and wastes less. The small garden therefore "
  "carries (conveys) a lesson larger than itself.",
  ["Preceding sentence: the family learns something important", "The garden conveys that lesson",
   "'may carry a lesson'"],
  "'Lose', 'deny' and 'waste' a lesson all mean the lesson is missed, which contradicts the sentence before it.",
  40, C1, 5)

# ---------------------------------------------------------------- Cloze 2 (Intermediate, 5)
C2 = stim("Bring your own bottle", (
    "A walk through any city market shows how much of what we buy comes wrapped in plastic. Shampoo arrives in "
    "sachets, rice in printed bags and detergent in pouches that are used once and thrown away. Most of this packaging "
    "is (1) ______ to recycle, either because it is made of several layers fused together or because it is too small "
    "and dirty to be worth collecting. Much of it ends up in drains, rivers and landfills.\n\n"
    "A small but growing number of shops are trying a different approach. Customers bring their own bottles and "
    "containers and refill them from large dispensers, paying only for the product, not for the packaging. Some shops "
    "weigh the empty container at the counter and (2) ______ its weight from the total, so that nobody pays for glass "
    "or steel. Others lend sturdy containers for a small deposit that is returned when the container is brought "
    "back.\n\n"
    "The model has obvious appeal, but it faces real (3) ______. Shoppers are used to the convenience of picking a "
    "packet off the shelf, and carrying containers requires planning. Hygiene rules for loose food are strict, and "
    "dispensers must be cleaned regularly. Above all, refill shops are too few to make a difference on their own; a "
    "family that has to cross the city to refill a bottle of oil will soon (4) ______ to sachets.\n\n"
    "Larger change will probably depend on manufacturers and big retailers. If major brands offered refill stations in "
    "ordinary supermarkets, and if rules required companies to take responsibility for the packaging they put on the "
    "market, the economics would shift quickly. Until then, the refill shop is less a solution than a (5) ______: "
    "proof that buying without throwing away is possible, and a reminder of how far we still have to go."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["designed", "easy", "difficult", "cheap"], "C",
  "Cloze: the 'because' clauses explain the blank",
  "The packaging is hard to recycle 'because it is made of several layers fused together or because it is too small "
  "and dirty to be worth collecting'. Both reasons are problems, so 'difficult' fits.",
  ["Read the 'either because ... or because' reasons", "Both describe obstacles to recycling",
   "'difficult to recycle'"],
  "'Easy' and 'cheap' contradict the reasons and the next sentence (it ends up in drains and rivers). 'Designed to "
  "recycle' is ungrammatical here and would also contradict the reasons.", 40, C2, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["add", "deduct", "measure", "hide"], "B",
  "Cloze: 'from the total' with the purpose 'so that nobody pays for glass or steel'",
  "To make sure customers do not pay for their own container, the shop takes its weight away from the total: it "
  "deducts the weight.",
  ["Purpose: nobody pays for the container", "So its weight must be taken off the total",
   "'deduct ... from the total'"],
  "'Add' would make customers pay for the container. 'Measure' and 'hide' do not go with 'from the total' and do not "
  "achieve the stated purpose.", 40, C2, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["rewards", "profits", "customers", "obstacles"], "D",
  "Cloze: 'but' introduces the difficulties listed next",
  "After 'The model has obvious appeal, but ...', the paragraph lists problems: habits of convenience, strict hygiene "
  "rules and too few shops. These are obstacles.",
  ["'but' contrasts with 'obvious appeal'", "Following sentences list difficulties", "'real obstacles'"],
  "'Rewards' and 'profits' are positives and remove the contrast. 'Faces real customers' does not introduce the list "
  "of difficulties that follows.", 40, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["revert", "refer", "react", "relate"], "A",
  "Cloze: 'revert to' = go back to an earlier habit",
  "A family that finds refilling too inconvenient will go back to its old habit of buying sachets. 'Revert to' means "
  "return to a previous state or practice.",
  ["Situation: refilling means crossing the city", "Likely result: going back to sachets",
   "'revert to sachets'"],
  "'Refer to', 'react to' and 'relate to' are all grammatical with 'to' but do not mean going back to an old habit.",
  40, C2, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["failure", "nuisance", "demonstration", "secret"], "C",
  "Cloze: the words after the colon define the blank",
  "After the colon, the refill shop is called 'proof that buying without throwing away is possible'. Something that "
  "proves a thing possible is a demonstration.",
  ["Read after the colon: 'proof that ... is possible'", "Proof that something can be done = a demonstration",
   "'less a solution than a demonstration'"],
  "'Failure' and 'nuisance' contradict 'proof that ... is possible'. A 'secret' cannot serve as public proof or a "
  "reminder.", 40, C2, 5)

# ---------------------------------------------------------------- Cloze 3 (Intermediate 2 + Advanced 3; error-based)
C3 = stim("Insuring against the sky", (
    "Every farmer knows that a single failed monsoon can **(1) wipe** out a year's income. Crop insurance is meant to "
    "soften such blows, but traditional policies have often disappointed farmers. To settle a claim, an official must "
    "visit the field and **(2) ignore** the loss, a process that is slow, costly and open to dispute. By the time the "
    "money arrives, the farmer may already have sold his cattle or borrowed at high interest to survive.\n\n"
    "Weather-index insurance takes a different route. Instead of measuring the damage in each field, it pays out "
    "automatically when an objective index, such as the rainfall recorded at a nearby weather station, crosses an "
    "agreed limit. If rainfall during the growing season falls below the threshold, every insured farmer in the area "
    "receives a payment, whether or not an inspector has visited. Because no field visits are needed, claims can be "
    "settled quickly and administrative costs stay **(3) high**.\n\n"
    "The approach has a weakness, which experts call basis risk: the gap between what the index records and what a "
    "particular farmer actually suffers. A weather station ten kilometres away may record adequate rain while a "
    "farmer's own field remains dry, or a crop may be destroyed by pests in a year when rainfall is perfectly normal. "
    "In such cases the farmer suffers a loss but receives nothing, and his trust in insurance is **(4) strengthened**."
    "\n\n"
    "Denser networks of weather stations and satellite data can narrow this gap, though they cannot close it entirely. "
    "Many specialists therefore see index insurance not as a replacement for traditional cover but as a "
    "**(5) substitute** for it: a quick, cheap first payment that keeps a household afloat, while losses that the index "
    "misses are handled in other ways."))

Q(CL, "Error-based cloze", I,
  ERR_STEM.format(n=1, ctx="a single failed monsoon can wipe out a year's income"),
  ["clear", "rub", "sweep", NR], "D",
  "Error-based cloze: the phrasal verb 'wipe out' = destroy completely",
  "'Wipe out' means destroy or remove completely, and a failed monsoon can destroy a whole year's income. The word is "
  "correct as it stands.",
  ["Meaning needed: completely destroy the year's income", "'wipe out' has exactly this meaning",
   "No replacement required"],
  "'Clear out', 'rub out' and 'sweep out' mean emptying or erasing something physically and do not describe the loss "
  "of income.", 40, C3, 1)

Q(CL, "Error-based cloze", I,
  ERR_STEM.format(n=2, ctx="an official must visit the field and ignore the loss, a process that is slow, costly and "
                           "open to dispute"),
  ["assess", "overlook", "inflate", NR], "A",
  "Error-based cloze: what an official visits a field to do",
  "To settle a claim, the official must measure, or assess, the loss. An official who 'ignores' the loss could not "
  "settle a claim, and the next paragraph contrasts this with 'measuring the damage in each field'.",
  ["Purpose of the visit: to settle a claim", "That requires judging the size of the loss",
   "Next paragraph confirms: 'measuring the damage': replace with 'assess'"],
  "'Overlook' repeats the error of 'ignore'. 'Inflate' means exaggerate, which is not the official's task. 'Ignore' "
  "is wrong, so 'No replacement required' does not apply.", 45, C3, 2)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=3, ctx="Because no field visits are needed, claims can be settled quickly and administrative "
                           "costs stay high"),
  ["rising", "heavy", "low", NR], "C",
  "Error-based cloze: follow the cause ('Because no field visits are needed')",
  "Field visits make traditional claims 'slow, costly'. Removing them makes settlement quick and keeps administrative "
  "costs low. 'High' contradicts the cause given in the same sentence.",
  ["Cause: no field visits", "Effects: quick settlement and smaller costs", "Replace 'high' with 'low'"],
  "'Rising' and 'heavy' repeat the error of 'high'. 'High' is wrong, so 'No replacement required' does not apply.",
  50, C3, 3)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=4, ctx="the farmer suffers a loss but receives nothing, and his trust in insurance is "
                           "strengthened"),
  ["deepened", "weakened", "confirmed", NR], "B",
  "Error-based cloze: effect of an unpaid loss on trust",
  "A farmer who suffers a loss and receives no payment loses faith in insurance. His trust is weakened, not "
  "strengthened.",
  ["Situation: real loss, no payout", "Natural effect: less trust", "Replace 'strengthened' with 'weakened'"],
  "'Deepened' and 'confirmed' repeat the error by making trust grow. 'Strengthened' is wrong, so 'No replacement "
  "required' does not apply.", 50, C3, 4)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=5, ctx="not as a replacement for traditional cover but as a substitute for it"),
  ["alternative", "complement", "compliment", NR], "B",
  "Error-based cloze: 'not X but Y' needs Y to differ from X; complement vs compliment",
  "'Not as a replacement ... but as a substitute' says the same thing twice, so 'substitute' is wrong. The colon "
  "explains that index insurance gives a quick first payment while other losses are 'handled in other ways': it works "
  "alongside traditional cover, completing it. That is a 'complement' (something that completes).",
  ["'not a replacement but a ___' → the blank must mean something other than a replacement",
   "After the colon: index insurance plus other cover together", "'complement' (completes), not 'compliment' (praise)"],
  "'Alternative' means the same as replacement, like 'substitute'. 'Compliment' means an expression of praise, a "
  "different word. 'Substitute' is wrong, so 'No replacement required' does not apply. (The preposition 'for it' would "
  "become 'to it' with 'complement'.)", 55, C3, 5)

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


# ---- Basic (7)
ed("Part-wise error", B, "The bank sent me", "all the informations", "I needed to open an account.", "B",
   "'Information' is uncountable and has no plural form",
   "'Information' is an uncountable noun, so it never takes '-s': 'all the information I needed'.",
   ["Noun in part B: 'information' (uncountable)", "Uncountable nouns have no plural",
    "'informations' → 'information': error in part B"],
   "Part A is a correct subject, verb and indirect object. Part C is a correct relative clause. B has an error, so 'No "
   "error' is wrong.", 30)

ed("Part-wise error", B, "The farmer told us", "that his cattle", "was grazing near the river.", "C",
   "'Cattle' is a plural noun and takes a plural verb",
   "'Cattle' has no singular form and is always plural: 'his cattle were grazing near the river'.",
   ["Subject of the 'that' clause: 'his cattle'", "'Cattle' is always plural",
    "'was grazing' → 'were grazing': error in part C"],
   "Part A is a correct past-tense reporting clause. Part B correctly introduces the clause. C has an error, so 'No "
   "error' is wrong.", 30)

ed("Part-wise error", B, "Please return back", "the signed form", "by Friday.", "A",
   "Redundancy: 'return' already means 'give or come back'",
   "'Return' means 'give back', so 'return back' says the same thing twice. The correct form is 'Please return the "
   "signed form by Friday.'",
   ["Meaning of 'return': give back", "'back' repeats that meaning",
    "Drop 'back': error in part A"],
   "Part B is a correct object and part C a correct time phrase. A has an error, so 'No error' is wrong.", 25)

ed("Part-wise error", B, "During the year-end closing,", "she is used", "to work late hours.", "C",
   "'Be/get used to' + gerund ('to' is a preposition here)",
   "In 'be used to' (be accustomed to), 'to' is a preposition, so it is followed by a noun or an -ing form: 'she is "
   "used to working late hours'. ('Used to work', with no 'be', means a past habit that has stopped.)",
   ["Expression: 'be used to' = be accustomed to", "'to' is a preposition → -ing form",
    "'to work' → 'to working': error in part C"],
   "Part A is a correct time phrase. Part B ('is used') is a correct form of the expression. C has an error, so "
   "'No error' is wrong.", 35)

ed("Error-free sentence", B, "The bank has revised its rates", "on all fixed deposits", "with effect from Monday.", "D",
   "Checking a correct sentence part by part",
   "The sentence is correct. 'Its' is the possessive (no apostrophe), the present perfect 'has revised' suits a recent "
   "change with a present result, 'rates on deposits' is the standard collocation and 'with effect from' is the correct "
   "fixed phrase.",
   ["Part A: 'has revised its rates': correct possessive and tense",
    "Part B: 'rates on all fixed deposits': correct", "Part C: 'with effect from Monday': correct",
    "No error: option D"],
   "Each of parts A, B and C is correct, as shown in the steps, so none of them is the answer.", 30)

ed("Part-wise error", B, "The canteen orders three dozens", "bananas every morning", "for the staff.", "A",
   "'Dozen' after a number takes no '-s'",
   "When 'dozen' follows a number, it stays singular: 'three dozen bananas'. ('Dozens of' is used only without a "
   "number, meaning 'many'.)",
   ["Number + dozen: 'three dozen'", "No plural '-s' after a number",
    "'three dozens' → 'three dozen': error in part A"],
   "Part B ('bananas every morning') and part C ('for the staff') are correct. A has an error, so 'No error' is "
   "wrong.", 30)

ed("Part-wise error", B, "The cash van", "reached to the branch", "just after ten.", "B",
   "'Reach' (arrive at) takes a direct object, with no 'to'",
   "'Reach' meaning 'arrive at' is transitive: 'The cash van reached the branch just after ten.' 'Reached to' is "
   "wrong.",
   ["Verb in part B: 'reached' (arrive at)", "It takes a direct object without a preposition",
    "Drop 'to': error in part B"],
   "Part A is a correct subject and part C a correct time phrase. B has an error, so 'No error' is wrong.", 25)

# ---- Intermediate (9)
ed("Part-wise error", I, "The salary of a clerk", "is lower than", "a branch manager.", "C",
   "Compare like with like: salary with salary, not salary with a person",
   "The sentence compares a clerk's salary with a branch manager (a person). It should compare salary with salary: "
   "'lower than that of a branch manager' (or 'than a branch manager's').",
   ["What is being compared? 'The salary of a clerk'", "It must be compared with another salary",
    "'than a branch manager' → 'than that of a branch manager': error in part C"],
   "Part A is a correct subject and part B a correct comparative. C has an error, so 'No error' is wrong.", 40)

ed("Part-wise error", I, "Prices of vegetables", "have raised sharply", "since the floods.", "B",
   "Rise (intransitive: rise – rose – risen) vs raise (transitive: raise – raised – raised)",
   "Prices go up by themselves; nothing is being lifted by someone. The intransitive verb 'rise' is needed: 'Prices "
   "have risen sharply.'",
   ["Is there an object after the verb? No", "No object → intransitive 'rise'",
    "Past participle of 'rise' is 'risen': error in part B"],
   "Part A is a correct plural subject and part C a correct 'since' phrase with the present perfect. B has an error, so "
   "'No error' is wrong.", 35)

ed("Part-wise error", I, "Beside his salary,", "he earns a small income", "from his farm.", "A",
   "Besides (in addition to) vs beside (next to)",
   "The meaning is 'in addition to his salary', which needs 'Besides'. 'Beside' means 'next to', which makes no sense "
   "with a salary.",
   ["Meaning needed: in addition to", "'Besides' = in addition to; 'beside' = next to",
    "'Beside' → 'Besides': error in part A"],
   "Part B is a correct main clause and part C a correct source phrase. A has an error, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "By evening the cashier was", "so tired to count", "the remaining notes.", "B",
   "'Too + adjective + to-infinitive' vs 'so + adjective + that-clause'",
   "'So tired to count' mixes two patterns. The correct forms are 'too tired to count the remaining notes' or 'so tired "
   "that he could not count the remaining notes'.",
   ["Pattern 1: too + adjective + to-infinitive", "Pattern 2: so + adjective + that-clause",
    "'so tired to count' mixes them: error in part B"],
   "Part A is a correct clause opening and part C a correct object. B has an error, so 'No error' is wrong.", 40)

ed("Part-wise error", I, "Although the loan was approved in March, but", "the money was released",
   "only in June.", "A",
   "'Although' and 'but' are not used together in one sentence",
   "'Although' already links the two clauses with a contrast, so adding 'but' is a double connector. Correct: "
   "'Although the loan was approved in March, the money was released only in June' (or 'The loan was approved in "
   "March, but ...'). Both connectors sit in part A.",
   ["Part A contains two connectors: 'Although' and 'but'", "Only one may be used",
    "Drop one of them: error in part A"],
   "Part B is a correct passive verb phrase and part C a correct time phrase. A has an error, so 'No error' is "
   "wrong.", 35)

ed("Part-wise error", I, "The officer explained me", "the terms of the loan", "in simple words.", "A",
   "'Explain something to someone' (not 'explain someone something')",
   "'Explain' cannot take the person as a direct object. The correct form is 'The officer explained the terms of the "
   "loan to me in simple words.'",
   ["Verb: 'explain'", "Pattern: explain + thing + to + person", "'explained me' is wrong: error in part A"],
   "Parts B and C are correct as phrases; the error lies in the verb pattern in A. So 'No error' is wrong.", 35)

ed("Part-wise error", I, "When have you submitted", "the documents for", "the home loan?", "A",
   "'When' asks about a definite past time, so it takes the simple past, not the present perfect",
   "A question with 'When' points to a specific time in the past, which needs the simple past: 'When did you submit the "
   "documents for the home loan?'",
   ["Question word: 'When' (definite time)", "Definite past time → simple past",
    "'When have you submitted' → 'When did you submit': error in part A"],
   "Parts B and C are correct. The error is the tense in A, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "I will call you", "as soon as the cheque", "will be cleared.", "C",
   "Time clauses ('as soon as', 'when', 'after') use the present tense for a future meaning",
   "In a time clause introduced by 'as soon as', the present tense is used even for a future event: 'as soon as the "
   "cheque is cleared'. 'Will' belongs only in the main clause.",
   ["Main clause: 'I will call you' (future, correct)", "Time clause with 'as soon as' → present tense",
    "'will be cleared' → 'is cleared': error in part C"],
   "Part A correctly uses 'will' in the main clause and part B correctly introduces the time clause. C has an error, so "
   "'No error' is wrong.", 35)

ed("Error-free sentence", I, "The committee's recommendations", "have been accepted", "by the board in full.", "D",
   "Checking a correct sentence: plural subject, present perfect passive, agent",
   "The sentence is correct. The subject 'recommendations' is plural, so 'have been accepted' agrees; the possessive "
   "'committee's' is correctly formed; and 'by the board in full' is a correct agent phrase.",
   ["Part A: plural head noun 'recommendations'", "Part B: plural verb 'have been accepted': agrees",
    "Part C: agent and adverbial: correct", "No error: option D"],
   "Each of parts A, B and C is correct, as shown in the steps, so none of them is the answer.", 35)

# ---- Advanced (5)
ed("Part-wise error", A, "The committee recommended", "simplifying the forms, cutting the fees",
   "and that branches should open on Sundays.", "C",
   "Parallel structure: items in a list must have the same grammatical form",
   "The list after 'recommended' begins with two gerund phrases ('simplifying ...', 'cutting ...'), so the third item "
   "must also be a gerund phrase: 'and opening branches on Sundays'. Switching to a 'that' clause breaks the "
   "parallelism.",
   ["Item 1: 'simplifying the forms' (gerund)", "Item 2: 'cutting the fees' (gerund)",
    "Item 3: 'that branches should open' (clause): not parallel, error in part C"],
   "Part A is a correct subject and verb, and part B lists two correct parallel gerunds. C has an error, so 'No error' "
   "is wrong.", 45)

ed("Part-wise error", A, "Of the two brothers who run the firm,", "Arun, who is elder than Vikram,",
   "looks after the accounts.", "B",
   "'Elder' is not followed by 'than'; use 'older than'",
   "'Elder' is used before a noun ('my elder brother') or as 'the elder of the two', but not with 'than'. The "
   "comparative with 'than' is 'older': 'Arun, who is older than Vikram, ...'.",
   ["Comparison with 'than' in part B", "'elder' cannot take 'than'",
    "'elder than' → 'older than': error in part B"],
   "Part A is a correct introductory phrase and part C a correct main verb that agrees with 'Arun'. B has an error, so "
   "'No error' is wrong.", 40)

ed("Part-wise error", A, "The recovery team has worked", "very hardly this quarter", "to bring down overdue loans.",
   "B",
   "Hard (adverb: with great effort) vs hardly (adverb: almost not)",
   "'Hard' is itself an adverb meaning 'with great effort'. 'Hardly' means 'almost not', so 'worked very hardly' would "
   "say the team barely worked, which contradicts the purpose clause. Correct: 'has worked very hard this quarter'.",
   ["Intended meaning: worked with great effort", "Adverb for that meaning: 'hard'",
    "'very hardly' → 'very hard': error in part B"],
   "Part A is a correct subject and present perfect, and part C a correct purpose clause. B has an error, so 'No "
   "error' is wrong.", 40)

ed("Error-free sentence", A, "So severe was the drought", "that the bank rescheduled", "all crop loans in the district.",
   "D",
   "Inversion after 'So + adjective' at the start of a sentence",
   "When 'So + adjective' opens a sentence, the verb comes before the subject: 'So severe was the drought that ...'. The "
   "result clause 'that the bank rescheduled all crop loans' is also correct. The sentence has no error.",
   ["Part A: 'So severe was the drought': correct inversion",
    "Part B: 'that' introduces the result; past tense matches", "Part C: correct object and place phrase",
    "No error: option D"],
   "Each of parts A, B and C is correct, as shown in the steps, so none of them is the answer. The inversion in A "
   "is required, not an error.", 45)

ed("Part-wise error", A, "A great deal of applications", "were rejected", "because of missing documents.", "A",
   "'A great deal of' goes with uncountable nouns; countable plurals take 'a great many' or 'a large number of'",
   "'Applications' is a countable plural, so 'a great deal of applications' is wrong. Correct: 'A great many "
   "applications were rejected' or 'A large number of applications were rejected'.",
   ["Noun: 'applications' (countable, plural)", "'A great deal of' is only for uncountable nouns (a great deal of time)",
    "Use 'A great many' / 'A large number of': error in part A"],
   "Part B ('were rejected') correctly agrees with the plural 'applications'. Part C is a correct reason phrase. A has "
   "an error, so 'No error' is wrong.", 40)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", B,
  SI_STEM + "She **is working in this branch since** 2019.",
  ["has been working in this branch since", "was working in this branch since", "is working in this branch from", NI],
  "A",
  "Present perfect continuous for an action that began in the past and continues now ('since + point of time')",
  "The work began in 2019 and still continues. An action running from a past point up to now takes the present perfect "
  "continuous: 'She has been working in this branch since 2019.'",
  ["Time marker: 'since 2019' (starting point in the past)", "The action continues now",
   "Present perfect continuous: 'has been working'"],
  "'Was working' suggests the work is over. 'Is working ... from' keeps the wrong present continuous. The original "
  "uses the present continuous with 'since', so 'No improvement required' is wrong.", 30)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "**Let he** handle the cash counter today.",
  ["Let his", "Let him", "Let he will", NI], "B",
  "'Let' is followed by an object pronoun and a bare infinitive",
  "'Let' takes an object, so the pronoun must be in the object form: 'Let him handle the cash counter today.'",
  ["'Let' + object + base verb", "Object form of 'he' is 'him'", "'Let him'"],
  "'His' is a possessive and 'Let he will' adds a modal after 'let'; both are ungrammatical. The original uses the "
  "subject form 'he', so 'No improvement required' is wrong.", 25)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "The heritage museum next to the head office **is worth to visit** on a weekend.",
  ["is worthy to visiting", "is worth for visiting", "is worth visiting", NI], "C",
  "'Worth' + gerund (never 'worth to' + verb)",
  "The adjective 'worth' is followed by an -ing form: 'The museum is worth visiting.' 'Worth to visit' is not used.",
  ["Expression: 'be worth'", "It takes a gerund", "'is worth visiting'"],
  "'Worthy to visiting' mixes 'worthy' with a preposition and a gerund. 'Worth for visiting' adds an unnecessary "
  "preposition. The to-infinitive in the original is wrong after 'worth', so 'No improvement required' does not "
  "apply.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "During the training, the new recruits **were made to sit** through a three-hour session on fraud "
  "prevention.",
  ["were made sit", "were made sitting", "had made to sit", NI], "D",
  "Causative 'make': bare infinitive in the active, to-infinitive in the passive",
  "In the active, 'make' takes a bare infinitive ('They made the recruits sit'). In the passive, 'to' returns: 'The "
  "recruits were made to sit'. The sentence is already correct.",
  ["Voice: passive ('were made')", "Passive of 'make someone do' → 'be made to do'",
   "'were made to sit' is correct: no improvement"],
  "'Were made sit' drops the 'to' that the passive needs. 'Were made sitting' uses the wrong verb form. 'Had made to "
  "sit' turns the passive into an incorrect active form with no object.", 35)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", B,
  PR_STEM + "The bank promised to **look after** the customer's complaint and reply within a week.",
  ["look into", "look up", "look down on", NR], "A",
  "Phrasal verbs with 'look': look into = investigate",
  "A complaint is investigated before the bank replies. 'Look into' means investigate; 'look after' means take care "
  "of a person or thing.",
  ["Context: a complaint to be examined before replying", "Meaning needed: investigate", "'look into'"],
  "'Look up' means search for information in a book or list. 'Look down on' means regard as inferior. The original "
  "'look after' (take care of) does not suit a complaint, so 'No replacement required' is wrong.", 30)

Q(PR, "Replace the phrase", I,
  PR_STEM + "A few large defaults **accounted by** most of the bank's losses last year.",
  ["accounted to", "accounted for", "were accounted", NR], "B",
  "'Account for' = make up, form (a proportion of)",
  "The defaults made up most of the losses. The phrasal verb is 'account for': 'A few large defaults accounted for most "
  "of the bank's losses.'",
  ["Meaning needed: formed, made up", "Phrasal verb: 'account for'", "'accounted for'"],
  "'Accounted to' means reported to someone. 'Were accounted' is an incomplete passive that makes no sense here. "
  "'Accounted by' is wrong, so 'No replacement required' does not apply.", 35)

Q(PR, "Replace the phrase", I,
  PR_STEM + "When his father retired, Ravi **took after** the family's grain business.",
  ["took up with", "took off", "took over", NR], "C",
  "Phrasal verbs with 'take': take over = assume control of",
  "When the father retired, Ravi assumed control of the business: he 'took over' the family's grain business. 'Take "
  "after' means to resemble a parent.",
  ["Context: father retires; son steps in", "Meaning needed: assume control", "'took over'"],
  "'Took up with' means began to associate with someone. 'Took off' means departed or became successful and cannot "
  "take this object. 'Took after' (resembled) is wrong here, so 'No replacement required' does not apply.", 35)

Q(PR, "Replace the phrase", A,
  PR_STEM + "Despite heavy publicity, the new deposit scheme **fell short of** the bank's targets.",
  ["fell short from", "fell shortly of", "fell short to", NR], "D",
  "Fixed expression: 'fall short of' = fail to reach",
  "'Fall short of a target' means fail to reach it, which fits 'Despite heavy publicity'. The phrase is already "
  "correct.",
  ["'Despite' signals a disappointing result", "'fall short of' = fail to reach", "Correct as it stands"],
  "'Fell short from' and 'fell short to' use the wrong preposition. 'Fell shortly of' wrongly turns 'short' into the "
  "adverb 'shortly' (soon).", 35)

Q(PR, "Replace the phrase", A,
  PR_STEM + "The success of the merger **hinges in** the approval of the regulator.",
  ["hinges at", "hinges on", "is hinging to", NR], "B",
  "Fixed preposition: 'hinge on' (or 'hinge upon') = depend entirely on",
  "'Hinge on' means depend entirely on. The merger's success depends on the regulator's approval: 'The success of the "
  "merger hinges on the approval of the regulator.'",
  ["Meaning: depends entirely on", "Fixed preposition with 'hinge': 'on'", "'hinges on'"],
  "'Hinges at' and 'is hinging to' use the wrong prepositions, and the continuous form is not used for this state. "
  "'Hinges in' is wrong, so 'No replacement required' does not apply.", 35)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", I, "Four question tags were used at a branch counter. " + SC_OK,
  ["She is coming to the meeting, isn't it?",
   "You will sign the form today, won't you?",
   "He hardly ever pays late, doesn't he?",
   "Let us begin the meeting, won't we?"], "B",
  "Question tags: same auxiliary and pronoun as the statement, with the opposite polarity",
  "A positive statement takes a negative tag with the same auxiliary and a matching pronoun: 'You will ..., won't "
  "you?'",
  ["A: 'She is ...' → tag 'isn't she?', not 'isn't it?'",
   "B: 'You will ...' → 'won't you?': correct",
   "C: 'hardly ever' is negative → positive tag 'does he?'",
   "D: 'Let us ...' → 'shall we?'"],
  "A uses 'it' instead of the subject pronoun 'she'. C needs a positive tag because 'hardly' makes the statement "
  "negative. D: the tag for 'Let us' is 'shall we?'.", 40)

Q(SC, "Grammatically incorrect sentence", I, SC_BAD,
  ["The scissors on the counter are blunt.",
   "A pair of new spectacles costs a lot these days.",
   "His trousers is torn at the knee.",
   "The goods were delivered to the warehouse on time."], "C",
  "Nouns that exist only in the plural (trousers, scissors, goods) take plural verbs; 'a pair of' takes a singular verb",
  "'Trousers' is a plural-only noun, so the verb must be plural: 'His trousers are torn at the knee.'",
  ["A: 'scissors ... are': correct", "B: 'A pair ... costs': the head noun 'pair' is singular, correct",
   "C: 'trousers is': incorrect", "D: 'goods were': correct"],
  "A, B and D are correct. In B the verb agrees with 'pair', which is singular.", 35)

Q(SC, "Correct sentence", A, SC_OK,
  ["The new system is as efficient, if not more efficient than, the old one.",
   "The new system is as efficient as, if not more efficient, the old one.",
   "The new system is as efficient, if not more, than the old one.",
   "The new system is as efficient as, if not more efficient than, the old one."], "D",
  "Double comparison: each part ('as ... as' and 'more ... than') must be complete",
  "Remove the bracketed phrase and the sentence must still work, and the bracketed phrase must also be complete on its "
  "own. Only D passes both tests: 'as efficient as the old one' and 'more efficient than the old one'.",
  ["Test 1 (remove 'if not ...'): 'as efficient as the old one' needs the second 'as'",
   "Test 2: 'more efficient than the old one' needs 'than'", "Only D has both: correct"],
  "A drops the second 'as'. B drops 'than'. C drops both the second 'as' and the adjective after 'more', leaving 'as "
  "efficient ... than'.", 45)

Q(SC, "Grammatically incorrect sentence", A,
  "Which of the following sentences is INCORRECT because of a faulty comparison?",
  ["The Pune branch earns more than any branch of the bank.",
   "The Pune branch earns more than any other branch of the bank.",
   "The Pune branch earns more than any branch of the rival bank.",
   "No other branch of the bank earns as much as the Pune branch."], "A",
  "Comparison within the same group needs 'any other'",
  "The Pune branch is itself a branch of the bank, so 'more than any branch of the bank' compares it with itself as "
  "well. Within the same group, the comparison must be 'than any other branch'.",
  ["A: Pune branch is one of 'the bank's' branches → needs 'any other': incorrect",
   "B: 'any other branch of the bank': correct",
   "C: rival bank's branches are a different group, so 'any' is correct",
   "D: positive-degree form 'No other ... as much as': correct"],
  "B, C and D are correct. C is correct without 'other' because the Pune branch does not belong to the rival bank.",
  45)

Q(SC, "Grammatically incorrect sentence", A, SC_BAD,
  ["Should you need any help, please call the branch.",
   "Had the auditors not raised the alarm, the fraud would have gone unnoticed.",
   "Did the bank know the borrower's history, it would have refused the loan.",
   "Were the rupee to weaken further, imports would become costlier."], "C",
  "Inverted conditionals are formed only with 'should', 'had' and 'were', never with 'did'",
  "A conditional can drop 'if' and invert only with 'should', 'had' or 'were'. 'Did the bank know ...' cannot replace "
  "'If the bank had known ...'. Correct: 'Had the bank known the borrower's history, it would have refused the loan.'",
  ["A: 'Should you need ...' = If you need: correct", "B: 'Had the auditors not raised ...': correct",
   "C: 'Did the bank know ...': not a possible inversion; incorrect",
   "D: 'Were the rupee to weaken ...': correct"],
  "A, B and D use the three accepted inversions (should, had, were) correctly.", 45)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) The next morning, he took the bag to the bank and handed it to the manager.\n"
  "(B) While locking up his shop one evening, Ravi noticed a cloth bag lying near the steps.\n"
  "(C) Inside it he found a passbook and a bundle of cash.\n"
  "(D) The manager traced the owner, an old farmer, who had dropped it on his way home.\n"
  "(E) Since the bank had already closed for the day, he kept the bag safely overnight.",
  ["BCADE", "BACED", "CBEAD", "BCEAD"], "D",
  "Para jumble: named opener, then discovery, decision, action and outcome",
  "B introduces Ravi and the bag. C ('Inside it') opens the bag and finds a passbook, which links it to the bank. E "
  "explains why he waited ('the bank had already closed'). A follows with 'The next morning'. D, the manager tracing "
  "the owner, comes last.",
  ["Opener: B (names Ravi; others use 'he' or 'it')", "B → C: 'Inside it' = the bag",
   "C → E: the passbook points to the bank, which is closed", "E → A ('The next morning') → D: BCEAD"],
  "BCADE has the bank closing after he has already handed the bag over. BACED takes the bag to the bank before he "
  "knows what is inside. CBEAD opens with 'Inside it' before any bag is mentioned.", 50)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) Last month, the bank introduced a token system at its busiest branch.\n"
  "(P) Each customer now collects a numbered token at the entrance.\n"
  "(Q) When the number is displayed on a screen, the customer goes to the counter shown beside it.\n"
  "(R) Until then, he can sit and wait instead of standing in a queue.\n"
  "(S) Customers say the new system has made their visits far less tiring.",
  ["PQRS", "PRQS", "QPRS", "PQSR"], "A",
  "Fixed opener; process order and the time reference 'Until then'",
  "P describes the first step (collecting a token). Q describes when the customer goes to the counter. R ('Until "
  "then') refers back to Q's moment, the number being displayed. S gives the customers' verdict.",
  ["(1) → P: first step of the new system", "P → Q: what happens to the token number",
   "Q → R: 'Until then' = until the number is displayed", "S: overall result: PQRS"],
  "PRQS puts 'Until then' before any moment has been mentioned. QPRS describes the number being displayed before "
  "customers collect tokens. PQSR gives the verdict before finishing the description.", 45)

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) He decided to stay ashore and persuaded his neighbours to do the same.\n"
  "(B) By noon, the storm had struck the coast with great force.\n"
  "(C) Murugan, a fisherman, had always set out to sea before dawn.\n"
  "(D) Several boats from other villages, whose crews had not received the warning, were badly damaged.\n"
  "(E) One morning, however, a message on his phone warned of a sudden storm.",
  ["CAEBD", "ECABD", "CEBAD", "CEABD"], "D",
  "Para jumble: habit → change ('however') → decision → event → consequence",
  "C introduces Murugan and his habit. E ('One morning, however') breaks the habit with a warning. A gives his "
  "decision. B ('By noon') reports the storm, and D contrasts the fate of crews who had no warning.",
  ["Opener: C (names Murugan)", "C → E: 'however' contrasts with his usual habit",
   "E → A: his response to the warning", "A → B ('By noon') → D (consequence): CEABD"],
  "CAEBD has him stay ashore before any warning arrives. ECABD opens with 'his phone' before Murugan is named. CEBAD "
  "has the storm strike before he decides to stay ashore.", 50)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Many patients, however, distrust them, assuming that a lower price means lower quality.\n"
  "(B) If that trust is built, families could save a large share of what they spend on medicines.\n"
  "(C) Generic medicines contain the same active ingredients as branded ones but are sold under their chemical "
  "names.\n"
  "(D) Because they do not carry the cost of advertising, they are often far cheaper.\n"
  "(E) Doctors and pharmacists can help overcome this doubt by explaining that generics must meet the same quality "
  "standards.",
  ["CADEB", "DCAEB", "CDAEB", "CDEAB"], "C",
  "Para jumble: definition → advantage → objection ('however') → remedy → result",
  "C defines generic medicines. D gives their advantage (cheaper). A ('however') raises the patients' doubt about a "
  "low price. E offers the remedy for 'this doubt'. B ('If that trust is built') states the result.",
  ["Opener: C (defines the subject)", "C → D: 'they' = generics; why they are cheaper",
   "D → A: low price → distrust ('however')", "A → E ('this doubt') → B ('that trust'): CDAEB"],
  "CADEB raises distrust of a low price before the low price is mentioned. DCAEB opens with 'they' before generics are "
  "introduced. CDEAB mentions 'this doubt' before the doubt is described.", 60)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) Television news in India is now often accompanied by a sign-language interpreter in a corner of the "
  "screen.\n"
  "(P) This shortage is the main reason why many channels still offer no interpretation at all.\n"
  "(Q) For millions of people with hearing loss, that small window is the only way to follow the news as it "
  "happens.\n"
  "(R) Expanding training courses would therefore benefit not only viewers but also schools, hospitals and courts.\n"
  "(S) Trained interpreters, however, remain scarce, and the few who exist are in heavy demand.",
  ["QPSR", "SPQR", "QSRP", "QSPR"], "D",
  "Fixed opener; demonstratives ('that small window', 'This shortage') and 'therefore' as links",
  "Q explains why the interpreter's window in (1) matters. S ('however') introduces the scarcity of interpreters. P "
  "('This shortage') refers to S. R ('therefore') draws the conclusion: train more interpreters.",
  ["(1) → Q: 'that small window' = the interpreter's corner", "Q → S: 'however', interpreters are scarce",
   "S → P: 'This shortage' refers to S", "P → R: 'therefore' concludes: QSPR"],
  "QPSR mentions 'This shortage' before any shortage is stated. SPQR uses 'however' with nothing to contrast and "
  "moves the window's importance after the shortage. QSRP draws the conclusion before P completes the problem.", 60)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Bananas meant for distant markets are therefore harvested while still green and hard.\n"
  "(B) A ripe banana bruises easily and spoils within a few days.\n"
  "(C) Near the market, they are placed in ripening rooms where a small dose of ethylene gas starts the process "
  "evenly.\n"
  "(D) This gas is produced naturally by the fruit itself, so the method adds nothing foreign to it.\n"
  "(E) The fruit that reaches the shop is thus ripe, unbruised and ready to eat.",
  ["BACDE", "BCADE", "ABCDE", "BACED"], "A",
  "Para jumble: problem → solution ('therefore') → next step → explanation → result ('thus')",
  "B states the problem (ripe bananas spoil). A ('therefore') gives the solution: pick them green. C describes ripening "
  "near the market. D ('This gas') explains C's ethylene. E ('thus') states the result.",
  ["Opener: B (the problem)", "B → A: 'therefore' follows from the problem",
   "A → C: 'they' = the green bananas", "C → D ('This gas') → E ('thus'): BACDE"],
  "BCADE ripens the bananas before they are harvested. ABCDE opens with 'therefore' with nothing before it. BACED "
  "separates 'This gas' (D) from the gas it refers to in C.", 55)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) Thousands of palm-leaf manuscripts lie in temples, monasteries and private homes across India.\n"
  "(P) Besides helping distant scholars, this means the fragile originals need to be handled far less often.\n"
  "(Q) Digitisation projects now photograph each leaf at high resolution before it is too late.\n"
  "(R) Many of them are crumbling because of heat, humidity and insects.\n"
  "(S) The images are then stored online, where scholars anywhere can study them.",
  ["RSQP", "QRSP", "RQPS", "RQSP"], "D",
  "Fixed opener; problem, response, next step ('then') and added benefit ('Besides')",
  "R describes the manuscripts' decay ('Many of them'). Q gives the response ('before it is too late'). S ('then') is "
  "the next step: storing the images online for scholars. P ('Besides helping distant scholars') adds a second "
  "benefit, so it must follow S.",
  ["(1) → R: 'them' = the manuscripts", "R → Q: 'before it is too late' answers the decay",
   "Q → S: 'The images ... then'", "S → P: 'Besides helping distant scholars' refers to S: RQSP"],
  "RSQP mentions 'The images' before any photographs are taken. QRSP puts the urgency ('too late') before the decay "
  "that explains it. RQPS refers to 'helping distant scholars' before scholars are mentioned.", 55)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) These are small warehouses, closed to walk-in shoppers, from which riders collect orders.\n"
  "(B) Quick-commerce apps promise to deliver groceries within minutes of an order.\n"
  "(C) To keep that promise, they rely on a network of so-called dark stores.\n"
  "(D) Critics, however, worry about the pressure such tight deadlines place on riders on busy roads.\n"
  "(E) Because each store serves only a few square kilometres, a rider rarely has far to travel.",
  ["BACED", "BCAED", "CBAED", "BCDAE"], "B",
  "Para jumble: claim → method → definition → how it works → criticism",
  "B states the promise. C ('that promise') introduces dark stores. A ('These are') defines them. E explains why "
  "delivery is quick. D ('however') raises the critics' concern about deadlines.",
  ["Opener: B (the apps' promise)", "B → C: 'that promise'", "C → A: 'These' = dark stores",
   "A → E (how they speed delivery) → D (criticism): BCAED"],
  "BACED uses 'These' before dark stores are named. CBAED opens with 'that promise' before the promise is made. BCDAE "
  "puts the criticism between the term and its definition, so 'These' would wrongly point to the critics' "
  "deadlines.", 55)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) In some villages, the panchayat now paints its annual budget on a wall in the main square.\n"
  "(P) Residents have begun to ask why a drain listed as complete has not been built.\n"
  "(Q) Transparency, it seems, works best when information is placed where people already gather.\n"
  "(R) Anyone passing by can see how much was allotted for roads, drains and the school.\n"
  "(S) Such questions were rare when the figures were kept in a register in the panchayat office.",
  ["RSPQ", "PRSQ", "RPQS", "RPSQ"], "D",
  "Fixed opener; effect, contrast with the past ('Such questions') and general conclusion",
  "R explains what the painted budget shows. P describes the result: residents ask questions. S ('Such questions') "
  "refers to P and contrasts with the past. Q draws the general lesson.",
  ["(1) → R: what the wall shows passers-by", "R → P: residents use that information to ask questions",
   "P → S: 'Such questions' refers to P", "Q: general conclusion last: RPSQ"],
  "RSPQ uses 'Such questions' before any question is asked. PRSQ has residents asking about the drain before the "
  "figures are described. RPQS draws the conclusion before S completes the contrast.", 55)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) Evidence from the market for investment products suggests otherwise.\n"
  "(B) Their money stays in a savings account, earning less than it could, not because they prefer it there but "
  "because deciding feels too hard.\n"
  "(C) It might seem that more choice must always leave consumers better off.\n"
  "(D) Simplifying the menu, by offering a few clearly explained products, may therefore help more people than adding "
  "yet another scheme.\n"
  "(E) Faced with dozens of almost identical mutual fund schemes, many first-time investors simply do nothing.",
  ["CEABD", "CAEBD", "ACEBD", "CAEDB"], "B",
  "Para jumble: common belief → 'suggests otherwise' → evidence → its consequence → conclusion ('therefore')",
  "C states the common belief. A ('suggests otherwise') challenges it. E gives the evidence. B ('Their money') "
  "describes what happens to those investors. D ('therefore') draws the conclusion.",
  ["Opener: C (the belief to be challenged)", "C → A: 'otherwise' needs a claim before it",
   "A → E: the evidence itself", "E → B ('Their' = first-time investors) → D ('therefore'): CAEBD"],
  "CEABD gives the evidence before saying it contradicts anything, leaving 'otherwise' after the evidence. ACEBD opens "
  "with 'otherwise' with nothing to contradict. CAEDB draws the conclusion before B finishes the evidence, leaving "
  "'Their money' without a clear referent.", 70)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) Antibiotics are among the most valuable medicines ever discovered.\n"
  "(P) If this continues, infections that are easily treated today could once again become deadly.\n"
  "(Q) Each such useless dose gives bacteria another chance to develop resistance.\n"
  "(R) A cold, for instance, is caused by a virus, against which an antibiotic is useless.\n"
  "(S) Their very success, however, has encouraged careless use, from self-medication for common colds to routine use "
  "on poultry farms.",
  ["SQRP", "RSQP", "SRPQ", "SRQP"], "D",
  "Fixed opener; 'however', 'for instance', 'such' and 'this' as links",
  "S ('Their very success, however') turns from (1)'s praise to careless use. R ('for instance') explains why using "
  "antibiotics for colds is useless. Q ('Each such useless dose') refers to R. P ('If this continues') gives the "
  "danger.",
  ["(1) → S: 'Their' = antibiotics; 'however' contrasts with (1)", "S → R: 'for instance' expands the colds example",
   "R → Q: 'such useless dose' refers to R's 'useless'", "Q → P: 'If this continues': SRQP"],
  "SQRP says 'such useless dose' before R explains why the dose is useless. RSQP opens with an example before the "
  "careless use it illustrates. SRPQ warns 'If this continues' before Q states the mechanism.", 70)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) Loading a single ship could take a week, and theft and damage were common.\n"
  "(B) Because every container has the same dimensions, cranes, trucks and trains everywhere can handle it without "
  "unpacking the goods inside.\n"
  "(C) The standard steel container changed all this.\n"
  "(D) Until the middle of the twentieth century, cargo was loaded onto ships piece by piece, in sacks, barrels and "
  "crates.\n"
  "(E) The resulting fall in shipping costs is one reason why a shirt sold in one country is so often made in "
  "another.",
  ["DCABE", "ADCBE", "DACEB", "DACBE"], "D",
  "Para jumble: old situation → its problems → turning point ('all this') → how it works → result",
  "D describes the old method. A adds its problems. C ('changed all this') refers to D and A. B explains how the "
  "container works. E ('The resulting fall') states the result of B.",
  ["Opener: D (time marker 'Until ...')", "D → A: problems of loading piece by piece",
   "A → C: 'all this' = the old method and its problems", "C → B (how) → E ('resulting'): DACBE"],
  "DCABE says the container 'changed all this' before the problems are described. ADCBE begins with a ship's loading "
  "time before the old method is introduced. DACEB states the result before explaining how the container works.", 65)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", B,
  SR_STEM + "(P) a new ATM\n(Q) has installed\n(R) the bank\n(S) near the bus stand",
  ["PQRS", "RPQS", "QRPS", "RQPS"], "D",
  "Subject + verb + object + place",
  "'The bank has installed a new ATM near the bus stand.' The subject (R) comes first, then the verb (Q), the object "
  "(P) and the place (S).",
  ["Subject: R ('the bank')", "Verb: Q ('has installed')", "Object: P; place: S: RQPS"],
  "PQRS would make the ATM install the bank. RPQS puts the object between the subject and the verb. QRPS starts with "
  "the verb.", 30)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) which had been pending for months\n(Q) was finally approved\n(R) the farmers' request for a new "
  "branch\n(S) after the minister's visit",
  ["RPQS", "RQPS", "PRQS", "RPSQ"], "A",
  "Noun + relative clause before the main verb; time phrase last",
  "'The farmers' request for a new branch, which had been pending for months, was finally approved after the "
  "minister's visit.' The relative clause (P) must follow 'request' (R), and the main verb (Q) follows the whole "
  "subject.",
  ["Subject noun: R", "Relative clause describing it: P", "Main verb: Q; time: S: RPQS"],
  "RQPS separates 'which' from 'request' so that it seems to refer to the approval. PRQS opens with 'which'. RPSQ puts "
  "the time phrase between the subject and its verb.", 40)

Q(SR, "Word/phrase rearrangement within a sentence", A,
  SR_STEM + "(P) that the board had no choice\n(Q) seek fresh capital from the government\n"
  "(R) so heavy were the losses\n(S) but to",
  ["RSPQ", "RPQS", "PRSQ", "RPSQ"], "D",
  "Inverted 'So + adjective + verb + subject ... that'; 'no choice but to + verb'",
  "'So heavy were the losses that the board had no choice but to seek fresh capital from the government.' R opens with "
  "the inverted 'So ... were the losses', P gives the result clause, and 'no choice' is completed by 'but to' (S) and "
  "the verb phrase (Q).",
  ["Opener: R ('So heavy were the losses')", "Result clause: P ('that the board had no choice')",
   "'no choice but to' + verb: S then Q: RPSQ"],
  "RSPQ and RPQS break the fixed phrase 'no choice but to seek'. PRSQ opens with 'that', leaving the 'So' clause in "
  "the middle.", 45)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The customer was ______ when the cashier returned the extra money she had paid by mistake.",
  ["annoyed", "grateful", "careless", "absent"], "B",
  "Single blank: the reaction to a kind act",
  "The cashier honestly returned money paid by mistake. The natural reaction is thankfulness: she was 'grateful'.",
  ["Event: extra money returned", "Reaction to an honest favour: thankful", "'grateful'"],
  "'Annoyed' does not fit a helpful act. 'Careless' and 'absent' do not describe a reaction to what happened.", 25)

Q(FB, "Single blank", B,
  FB1 + "The bank will ______ a penalty if the borrower misses three instalments in a row.",
  ["impose", "oppose", "propose", "expose"], "A",
  "Confusable words: impose (enforce a charge or rule) vs oppose, propose, expose",
  "A bank enforces a penalty on a borrower who misses payments: it 'imposes' a penalty.",
  ["Collocation: impose a penalty / fine / tax", "Context: consequence of missed instalments", "'impose'"],
  "'Oppose' (resist), 'propose' (suggest) and 'expose' (reveal) do not describe enforcing a charge.", 25)

Q(FB, "Double blank", B,
  FB2 + "The branch was ______ for repairs, so customers were ______ to the branch across the road.",
  ["opened, directed", "closed, directed", "closed, prevented", "crowded, invited"], "B",
  "Double blank: cause and result joined by 'so'",
  "Repairs mean the branch was closed, so customers were sent (directed) to another branch.",
  ["Blank 1: a branch under repair is 'closed'", "Blank 2: customers sent elsewhere → 'directed'", "Option B"],
  "'Opened ... for repairs' does not explain why customers went elsewhere. 'Prevented to' is not the right pattern "
  "('prevented from'). 'Crowded ... invited' breaks the cause and result.", 30)

Q(FB, "Phrase fillers", B,
  FBP + "The new manager is easy to ______; within a week, the whole staff liked him.",
  ["get along with", "get away with", "get over with", "get through with"], "A",
  "Phrasal verb: get along with = have a friendly relationship with",
  "The staff liked him within a week, so he was easy to have a friendly relationship with: 'easy to get along with'.",
  ["Clue: 'the whole staff liked him'", "Meaning needed: be on good terms with", "'get along with'"],
  "'Get away with' means escape punishment. 'Get over with' means finish something unpleasant. 'Get through with' "
  "means complete a task. None describes a friendly relationship.", 30)

Q(FB, "Single blank", I,
  FB1 + "The merger talks reached a ______ when neither bank would agree on who should lead the combined entity.",
  ["consensus", "milestone", "conclusion", "deadlock"], "D",
  "Single blank: 'neither ... would agree' signals a standstill",
  "When neither side will give way, talks cannot move forward: they reach a deadlock.",
  ["Clue: 'neither bank would agree'", "Result: no progress", "'deadlock'"],
  "'Consensus' (agreement) is the opposite. 'Milestone' suggests progress. 'Reached a conclusion' would mean the talks "
  "were settled, which contradicts the disagreement.", 30)

Q(FB, "Double blank", I,
  FB2 + "The scheme was ______ in theory, but poor ______ meant that few farmers ever benefited from it.",
  ["flawed, planning", "sound, implementation", "sound, intentions", "popular, weather"], "B",
  "Double blank: 'in theory ... but' contrasts design with execution",
  "'In theory ... but' sets good design against bad execution: the scheme was sound in theory, but poor "
  "implementation kept the benefits from reaching farmers.",
  ["Blank 1: positive, because 'but' introduces a problem → 'sound'",
   "Blank 2: the practical failure → 'implementation'", "Option B"],
  "A: 'flawed in theory' removes the contrast with 'but'. C: 'poor intentions' contradicts a scheme that was sound. "
  "D: 'poor weather' does not contrast with 'in theory', and 'popular in theory' is odd.", 35)

Q(FB, "Phrase fillers", I,
  FBP + "With costs rising and deposits falling, the bank had no choice but to ______ its plans for rural expansion.",
  ["scale back", "scale up", "back up", "draw up"], "A",
  "Phrasal verb: scale back = reduce in size or extent",
  "Rising costs and falling deposits force a bank to cut its plans: it must 'scale back' its expansion.",
  ["Situation: financial pressure", "'had no choice but to' → an unwelcome cut", "'scale back'"],
  "'Scale up' (enlarge) contradicts the pressure. 'Back up' (support) and 'draw up' (prepare a plan) do not express "
  "a forced reduction.", 30)

Q(FB, "Single blank", A,
  FB1 + "The bank's accounts were so ______ that even the auditors could not tell where the money had gone.",
  ["lucid", "opaque", "meticulous", "prudent"], "B",
  "Single blank: 'so ... that' result",
  "The result is that even auditors could not trace the money, so the accounts must have been hard to understand: "
  "'opaque' (not transparent, unclear).",
  ["Result: auditors could not trace the money", "Cause: accounts were unclear", "'opaque'"],
  "'Lucid' (clear), 'meticulous' (very careful) and 'prudent' (sensible) would make the money easier to trace, not "
  "harder.", 35)

Q(FB, "Single blank", A,
  FB1 + "His ______ stance in the negotiations, refusing to concede even minor points, eventually drove the investors "
  "away.",
  ["accommodating", "pliant", "genial", "intransigent"], "D",
  "Single blank: the participle phrase defines the blank",
  "'Refusing to concede even minor points' describes someone who will not compromise: 'intransigent'.",
  ["Definition clue: 'refusing to concede even minor points'", "Unwilling to compromise = intransigent",
   "Result 'drove the investors away' confirms a negative quality"],
  "'Accommodating' and 'pliant' mean willing to adjust, the opposite. 'Genial' (friendly) does not describe refusing "
  "to concede.", 35)

Q(FB, "Double blank", A,
  FB2 + "Instead of ______ the crisis, the hasty measures only ______ public panic, and depositors queued outside "
  "branches the next morning.",
  ["defusing, fuelled", "worsening, calmed", "defusing, eased", "ignoring, prevented"], "A",
  "Double blank: 'Instead of' contrasts the intended effect with the actual one",
  "The measures were meant to calm the crisis but did the opposite, as the queues show. 'Instead of defusing the "
  "crisis, the hasty measures only fuelled public panic.'",
  ["Result clue: depositors queued the next morning → panic grew", "Blank 2: 'fuelled' (increased)",
   "Blank 1: the opposite, the intended effect → 'defusing'"],
  "B reverses both words and contradicts the queues. C ('eased panic') contradicts the queues and removes the "
  "contrast. D ('prevented panic') also contradicts the queues.", 40)

Q(FB, "Phrase fillers", A,
  FBP + "The bank's new chairman has promised to ______ the culture of aggressive sales targets that led to "
  "mis-selling.",
  ["root for", "bring about", "root out", "set up"], "C",
  "Phrasal verb: root out = find and remove completely",
  "A culture that led to mis-selling is something to be eliminated. 'Root out' means find and remove completely.",
  ["Object: a harmful culture", "Promise: get rid of it", "'root out'"],
  "'Root for' means support or cheer on. 'Bring about' (cause to happen) and 'set up' (establish) would create the "
  "culture, not end it.", 35)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Word swap", I,
  WS_STEM + "The **(A) receipt** counted the **(B) notes** twice before handing them to the **(C) customer**, who "
  "signed the **(D) teller**.",
  ["A-B", "A-D", "B-C", "No swap required"], "B",
  "Word swap: check who can perform each action",
  "A receipt cannot count notes, and a customer does not sign a teller. Swapping A and D gives: 'The teller counted "
  "the notes twice before handing them to the customer, who signed the receipt.'",
  ["'The receipt counted' is meaningless → A is misplaced", "'signed the teller' is meaningless → D is misplaced",
   "Swap A and D"],
  "A-B gives 'The notes counted the receipt'. B-C gives 'counted the customer twice before handing them to the "
  "notes'. The sentence clearly needs a swap.", 35)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'proscribe' used correctly?",
  ["The doctor proscribed rest and plenty of fluids for a week.",
   "Students must read the proscribed textbooks before the examination.",
   "The law proscribes the sale of tobacco products to minors.",
   "The bank has proscribed a new format for loan applications."], "C",
  "Proscribe (forbid, ban) vs prescribe (recommend, lay down as a rule)",
  "'Proscribe' means forbid by law. 'The law proscribes the sale of tobacco products to minors' means the law bans "
  "it, which is correct.",
  ["A: a doctor recommends rest → 'prescribed'", "B: textbooks laid down for a course → 'prescribed'",
   "C: the law forbids a sale → 'proscribes': correct", "D: a format laid down → 'prescribed'"],
  "A, B and D all need 'prescribe', meaning recommend or lay down; using 'proscribe' would mean the rest, textbooks "
  "and format were banned.", 40)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'dormant' as used in the sentence:\n"
  "'The bank wrote to her about her dormant account, which had seen no transactions for over two years.'",
  ["overdrawn", "inactive", "jointly held", "newly opened"], "B",
  "Dormant = inactive, not in use for a period",
  "The sentence explains the word: the account 'had seen no transactions for over two years'. A dormant account is an "
  "inactive one.",
  ["Clue: no transactions for over two years", "'dormant' = inactive"],
  "'Overdrawn' (more taken out than deposited), 'jointly held' and 'newly opened' all describe something other than a "
  "lack of activity.", 25)

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'stringent' as used in the sentence:\n"
  "'After a string of defaults, the regulator introduced stringent norms for lending to property developers.'",
  ["strict", "lenient", "vague", "temporary"], "A",
  "Stringent = strict, severe",
  "A regulator reacting to a string of defaults tightens the rules: 'stringent norms' are strict ones.",
  ["Context: response to many defaults", "Likely response: tougher rules", "'stringent' = strict"],
  "'Lenient' is the opposite. 'Vague' and 'temporary' do not describe a tougher response to defaults.", 30)

Q(VO, "Word pairs", A, "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Obdurate – Pliant", "Garrulous – Taciturn", "Ephemeral – Transient", "Munificent – Miserly"], "C",
  "Advanced vocabulary: synonym and antonym pairs",
  "'Ephemeral' and 'transient' both mean lasting only a short time. The other three pairs are opposites.",
  ["Obdurate (stubborn) ≠ pliant (easily bent)", "Garrulous (very talkative) ≠ taciturn (saying little)",
   "Ephemeral = transient (short-lived)", "Munificent (very generous) ≠ miserly"],
  "A, B and D are pairs of opposites, not synonyms.", 35)

Q(VO, "Word pairs", A, "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Assiduous – Diligent", "Mendacious – Untruthful", "Inimical – Hostile", "Laconic – Verbose"], "D",
  "Advanced vocabulary: synonym and antonym pairs",
  "'Laconic' means using very few words; 'verbose' means using too many. They are opposites. The other pairs are "
  "synonyms.",
  ["Assiduous = diligent (hard-working)", "Mendacious = untruthful", "Inimical = hostile",
   "Laconic ≠ verbose"],
  "A, B and C are pairs of synonyms, not opposites.", 35)

Q(VO, "Contextual meaning", A,
  "Choose the meaning of the word 'sanguine' as used in the sentence:\n"
  "'Despite the slowdown, the chairman remained sanguine about the bank's prospects for the coming year.'",
  ["gloomy", "optimistic", "indifferent", "secretive"], "B",
  "Sanguine = cheerfully hopeful, optimistic",
  "'Despite the slowdown' sets up a contrast: the economy is weak, yet the chairman stays hopeful. 'Sanguine' means "
  "optimistic.",
  ["'Despite' signals an attitude that runs against the bad news", "Hopeful in spite of a slowdown",
   "'sanguine' = optimistic"],
  "'Gloomy' is the opposite and removes the contrast with 'Despite'. 'Indifferent' and 'secretive' do not describe a "
  "view of the bank's prospects.", 30)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", B,
  SY_STEM + "The bank will **commence** its annual audit next Monday.",
  ["postpone", "begin", "complete", "cancel"], "B",
  "Commence = begin",
  "To 'commence' something is to begin it; the audit will begin next Monday.",
  ["'commence' = start, begin"],
  "'Postpone' and 'cancel' mean the audit will not start then. 'Complete' refers to the end, not the start.", 20)

Q(SY, "Contextual synonym", B,
  SY_STEM + "Clean drinking water is **vital** for the health of the village.",
  ["harmful", "optional", "essential", "costly"], "C",
  "Vital = absolutely necessary",
  "Clean water is absolutely necessary for health. 'Vital' means essential.",
  ["'vital' = necessary for life or success", "Closest: 'essential'"],
  "'Harmful' and 'optional' contradict the meaning. 'Costly' describes price, not necessity.", 20)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The inspector will **scrutinise** every loan file before the audit report is finalised.",
  ["approve", "ignore", "sign", "examine closely"], "D",
  "Scrutinise = examine closely and thoroughly",
  "Before a report is finalised, an inspector checks each file carefully. 'Scrutinise' means examine closely.",
  ["Context: checking before finalising a report", "'scrutinise' = examine in detail"],
  "'Approve' and 'sign' are actions after checking, not the checking itself. 'Ignore' is the opposite.", 25)

Q(SY, "Contextual synonym", A,
  SY_STEM + "Updating KYC details online will **obviate** the need for most customers to visit the branch.",
  ["remove", "create", "highlight", "delay"], "A",
  "Obviate = remove (a need or difficulty), make unnecessary",
  "If KYC can be updated online, customers no longer need to visit the branch. 'Obviate the need' means remove the "
  "need.",
  ["Context: online updating replaces a branch visit", "So the need for a visit disappears",
   "'obviate' = remove, make unnecessary"],
  "'Create' is the opposite. 'Highlight' and 'delay' the need do not fit the effect of an online option.", 30)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The bank offers **temporary** jobs to students during the festive season.",
  ["short", "permanent", "seasonal", "brief"], "B",
  "Temporary = lasting for a limited time; antonym: permanent",
  "A 'temporary' job lasts only for a limited period. The opposite is 'permanent'.",
  ["'temporary' = for a limited time", "Opposite = lasting indefinitely: 'permanent'"],
  "'Short', 'seasonal' and 'brief' are all close in meaning to 'temporary'.", 20)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The company plans to **expand** its operations in rural areas next year.",
  ["grow", "extend", "reduce", "widen"], "C",
  "Expand = make larger; antonym: reduce",
  "To 'expand' operations is to enlarge them. The opposite is to 'reduce' them.",
  ["'expand' = enlarge", "Opposite = make smaller: 'reduce'"],
  "'Grow', 'extend' and 'widen' are all similar in meaning to 'expand'.", 20)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The cashier quickly identified the five-hundred-rupee note as **genuine**.",
  ["counterfeit", "authentic", "real", "valid"], "A",
  "Genuine = real, not fake; antonym: counterfeit",
  "A 'genuine' note is real. The opposite is a 'counterfeit' (fake) note.",
  ["'genuine' = real", "Opposite = fake: 'counterfeit'"],
  "'Authentic', 'real' and 'valid' are all similar in meaning to 'genuine'.", 20)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The witness gave a **candid** account of what had happened at the counter.",
  ["frank", "honest", "open", "evasive"], "D",
  "Candid = frank and truthful; antonym: evasive",
  "A 'candid' account is frank and holds nothing back. The opposite is an 'evasive' account, one that avoids giving "
  "direct answers.",
  ["'candid' = frank, open", "Opposite = avoiding the truth: 'evasive'"],
  "'Frank', 'honest' and 'open' are all similar in meaning to 'candid'.", 25)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The fresh capital is expected to **augment** the bank's lending capacity.",
  ["increase", "diminish", "boost", "strengthen"], "B",
  "Augment = increase; antonym: diminish",
  "To 'augment' is to make larger or add to. The opposite is to 'diminish', to make smaller.",
  ["'augment' = increase", "Opposite = make smaller: 'diminish'"],
  "'Increase', 'boost' and 'strengthen' are all similar in meaning to 'augment'.", 25)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"

Q(ID, "Meaning of idiom", B,
  "Choose the meaning of the idiom 'the tip of the iceberg'.",
  ["a small, visible part of a much larger problem", "the most dangerous part of a journey",
   "a cold and unfriendly welcome", "the final stage of a task"], "A",
  "Idiom: the tip of the iceberg",
  "Only a small part of an iceberg shows above the water. The idiom means a small, visible part of a much bigger "
  "problem. For example: 'The frauds detected so far may be just the tip of the iceberg.'",
  ["Image: most of an iceberg is hidden under water", "Meaning: a small visible part of a larger problem"],
  "B, C and D take one word of the image ('tip' or 'ice') literally and have no link with the idiom's meaning.", 25)

Q(ID, "Idiom in context", B,
  "Choose the meaning of the idiom in bold.\n"
  "The security guard was dismissed for **turning a blind eye** to the thefts from the staff lockers.",
  ["reporting promptly", "being unable to see clearly", "deliberately ignoring", "investigating carefully"], "C",
  "Idiom: turn a blind eye (to) = pretend not to notice",
  "The guard was dismissed because he knew about the thefts but deliberately ignored them.",
  ["Context: a guard dismissed over thefts", "Idiom: pretend not to see something wrong"],
  "'Reporting promptly' and 'investigating carefully' would not lead to dismissal. 'Being unable to see clearly' takes "
  "the idiom literally.", 25)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "The new flyover, built at great cost but hardly used by anyone, has become a **white elephant**.",
  ["a symbol of national pride", "a rare and beautiful object",
   "a project that is completed ahead of time", "a costly possession that is of little use"], "D",
  "Idiom: white elephant = something costly to build or keep but of little use",
  "The flyover cost a great deal but is hardly used: it is a costly thing of little use, a 'white elephant'.",
  ["Context: great cost, little use", "Idiom: expensive but useless"],
  "'A symbol of national pride' and 'a rare and beautiful object' miss the idea of uselessness. 'Completed ahead of "
  "time' has no link with the idiom.", 25)

Q(ID, "Meaning of idiom", I,
  "Choose the meaning of the idiom 'to be in the red'.",
  ["to be very angry", "to be in debt or making a loss", "to be in danger of an accident", "to be embarrassed"],
  "B",
  "Idiom: in the red = owing money, making a loss (from losses once written in red ink)",
  "A business that is 'in the red' is losing money or is in debt. Its opposite is 'in the black'.",
  ["Origin: losses were entered in red ink", "Meaning: in debt, making a loss"],
  "A and D link red with anger or embarrassment, and C with danger, but the idiom refers only to finances.", 25)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "Stop **beating about the bush** and tell us plainly whether the loan has been approved.",
  ["avoiding the main point", "working very hard", "making a loud noise", "wasting money"], "A",
  "Idiom: beat about (or around) the bush = avoid coming to the point",
  "The speaker wants a plain answer, so the listener has been avoiding the main point.",
  ["Clue: 'tell us plainly'", "So the person has been talking around the point"],
  "'Working very hard', 'making a loud noise' and 'wasting money' do not contrast with telling something plainly.",
  25)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "Everyone agreed that the regional head's bullying should be reported, but nobody was willing to **bell the cat**.",
  ["share the credit", "keep a secret", "take the risk of confronting a powerful person", "make a hasty decision"],
  "C",
  "Idiom: bell the cat = take on a dangerous task on behalf of a group",
  "Everyone wanted the bullying reported, but reporting a powerful boss is risky. Nobody would take that risk: nobody "
  "would 'bell the cat'.",
  ["Context: all agree on an action against a powerful person", "'but nobody was willing' → the action is risky",
   "Idiom: take the risky step for the group"],
  "'Share the credit' and 'make a hasty decision' do not fit. 'Keep a secret' is the opposite of reporting.", 30)

Q(ID, "Idiom in context", A,
  "Choose the meaning of the phrase in bold.\n"
  "The bank won the long court case, but it was a **Pyrrhic victory**: the legal costs were greater than the amount it "
  "recovered.",
  ["a victory won by cheating", "an easy and unexpected victory",
   "a victory that brings fame but no money", "a victory won at so great a cost that it is hardly worth winning"], "D",
  "Phrase: Pyrrhic victory = a win that costs the winner almost as much as, or more than, a defeat",
  "The explanation after the colon makes the meaning clear: the bank spent more on legal costs than it recovered, so "
  "the win was not worth its cost.",
  ["Explanation after the colon: costs exceeded the gain", "A win not worth its price = Pyrrhic victory"],
  "Nothing suggests cheating (A) or an easy win (B). C is wrong because the problem is the cost, not a lack of "
  "money from fame.", 30)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", I,
  OW_STEM + "A temporary suspension of an activity or of an obligation, such as the repayment of loans",
  ["embargo", "moratorium", "sanction", "amnesty"], "B",
  "One-word substitution: finance and law terms",
  "A 'moratorium' is a temporary suspension of an activity or obligation, for example a moratorium on loan "
  "repayments.",
  ["Key ideas: temporary + suspension of an obligation", "Word: moratorium"],
  "An 'embargo' is an official ban, usually on trade. A 'sanction' is a penalty or an official permission. An "
  "'amnesty' is an official pardon.", 25)

Q(OW, "Single word for a phrase", I,
  OW_STEM + "The dishonest taking of money that has been placed in one's care",
  ["extortion", "bribery", "embezzlement", "forgery"], "C",
  "One-word substitution: financial wrongdoing",
  "'Embezzlement' is the theft of money by someone who has been trusted to look after it, such as an employee or "
  "official.",
  ["Key ideas: money entrusted to the person + dishonestly taken", "Word: embezzlement"],
  "'Extortion' is obtaining money by threats. 'Bribery' is offering money to influence someone. 'Forgery' is making a "
  "false copy of a document or signature.", 25)

Q(OW, "Single word for a phrase", A,
  OW_STEM + "A position that requires little or no work but gives the holder a salary or status",
  ["sinecure", "tenure", "stipend", "prerogative"], "A",
  "One-word substitution: positions and payments",
  "A 'sinecure' is a post that brings pay or status without real duties.",
  ["Key ideas: little or no work + salary or status", "Word: sinecure"],
  "'Tenure' is the period for which a post is held. A 'stipend' is a fixed allowance, such as an apprentice's pay. A "
  "'prerogative' is a special right or privilege.", 30)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", B, AP_STEM + "The clerk is counting the cash.",
  ["The cash is counted by the clerk.", "The cash was being counted by the clerk.",
   "The cash is being counted by the clerk.", "The cash has been counted by the clerk."], "C",
  "Present continuous active → is/are being + past participle",
  "'Is counting' becomes 'is being counted'; the object 'the cash' becomes the subject and 'the clerk' the agent.",
  ["Object 'the cash' → subject", "is + V-ing → is being + V3", "Agent: 'by the clerk'"],
  "A changes the tense to present simple. B changes it to past continuous. D changes it to present perfect.", 25)

Q(AP, "Voice conversion", A, AP_STEM + "People say that the bank is planning a merger.",
  ["The bank is said to plan a merger.", "The bank was said to be planning a merger.",
   "It is said that the bank was planning a merger.", "The bank is said to be planning a merger."], "D",
  "Passive of reporting verbs: subject + is said + to be + -ing for an action in progress",
  "'People say that the bank is planning ...' becomes 'The bank is said to be planning a merger.' The present 'is "
  "said' matches 'say', and the continuous infinitive 'to be planning' matches 'is planning'.",
  ["Reporting verb 'say' (present) → 'is said'", "Subject of the 'that' clause → subject of the sentence",
   "'is planning' (in progress) → 'to be planning'"],
  "A uses the simple infinitive 'to plan', which loses the sense of an action in progress. B changes 'say' to the past "
  "'was said'. C wrongly changes 'is planning' to 'was planning'.", 40)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", B, DS_STEM + "He asked me, \"Where do you work?\"",
  ["He asked me where did I work.", "He asked me where I worked.",
   "He asked me where do I work.", "He asked me that where I worked."], "B",
  "Wh-question in reported speech: statement word order + backshift, no 'that'",
  "A reported wh-question keeps the question word, uses statement order (subject before verb) and moves the tense "
  "back: 'He asked me where I worked.'",
  ["Keep the question word 'where'", "Statement order: 'I worked' (no 'did' or 'do')",
   "Present 'do you work' → past 'I worked'"],
  "A and C keep question order ('did I work', 'do I work'). D adds 'that' before the question word.", 30)

Q(DS, "Narration change", I, DS_STEM + "The manager said, \"What a careful worker she is!\"",
  ["The manager exclaimed that she was a very careful worker.",
   "The manager said what a careful worker was she.",
   "The manager exclaimed that what a careful worker she is.",
   "The manager asked what a careful worker she was."], "A",
  "Exclamatory sentence in reported speech: 'exclaimed that' + statement form + backshift",
  "An exclamation is reported with a verb such as 'exclaimed', and the exclamation becomes a statement: 'What a "
  "careful worker she is!' → 'that she was a very careful worker'.",
  ["Exclamation → reporting verb 'exclaimed'", "'What a ...!' → statement with 'very'",
   "Backshift: 'is' → 'was'"],
  "B inverts the verb ('was she') as if it were a question. C keeps 'what' after 'that' and does not backshift. D "
  "uses 'asked', but the original is an exclamation, not a question.", 35)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", B,
  SV_STEM + "Ten kilometres ______ a long distance to walk to the nearest bank branch.",
  ["are", "is", "were", "have been"], "B",
  "A plural amount of distance, money or time seen as one quantity takes a singular verb",
  "'Ten kilometres' is treated here as a single distance, not ten separate kilometres, so the verb is singular: 'Ten "
  "kilometres is a long distance.'",
  ["Is the subject one amount or separate items? One distance", "Single quantity → singular verb",
   "Present general statement → 'is'"],
  "'Are', 'were' and 'have been' are plural and treat the distance as separate kilometres, against the singular "
  "complement 'a long distance'.", 25)

Q(SV, "Agreement rules", I,
  SV_STEM + "Opening new branches in remote hill districts ______ proved far more expensive than the bank expected.",
  ["has", "have", "are", "were"], "A",
  "A gerund phrase used as the subject is singular, whatever plural noun it contains",
  "The subject is the activity 'Opening new branches ...', a gerund phrase, which takes a singular verb. 'Branches' is "
  "only the object of 'opening'. So: 'Opening new branches ... has proved far more expensive.'",
  ["Subject: the gerund phrase 'Opening new branches in remote hill districts'",
   "A gerund subject is singular ('branches' is the object of 'opening')", "Singular present perfect: 'has proved'"],
  "'Have' wrongly agrees with 'branches'. 'Are proved' and 'were proved' are plural passive forms that also change "
  "the meaning to 'were shown to be'.", 30)

Q(SV, "Agreement rules", I,
  SV_STEM + "None of the stolen money ______ been recovered so far.",
  ["have", "are", "has", "were"], "C",
  "'None of' + uncountable noun takes a singular verb",
  "'Money' is uncountable, so 'none of the stolen money' is singular: 'None of the stolen money has been recovered.'",
  ["Noun after 'none of': 'money' (uncountable)", "Uncountable → singular verb",
   "With 'so far' → present perfect: 'has been'"],
  "'Have' and 'were' are plural forms. 'Are been' is ungrammatical. An uncountable noun after 'none of' takes a "
  "singular verb.", 30)

Q(SV, "Agreement rules", A,
  SV_STEM + "Two-thirds of the farmland in the district ______ irrigated by canals.",
  ["are", "were", "have", "is"], "D",
  "Fractions and percentages agree with the noun after 'of'",
  "With a fraction, the verb agrees with the noun that follows 'of'. 'Farmland' is uncountable and singular, so the "
  "verb is singular: 'Two-thirds of the farmland is irrigated.'",
  ["Fraction subject: 'Two-thirds of ...'", "Noun after 'of': 'farmland' (uncountable)",
   "Singular verb, present passive: 'is irrigated'"],
  "'Are' and 'were' wrongly agree with the plural-looking 'two-thirds'. 'Have irrigated' would make the farmland the "
  "doer of the irrigation.", 35)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Sequence of tenses", I,
  TE_STEM + "While the clerk ______ the cash, the power suddenly went off.",
  ["was counting", "counted", "had counted", "is counting"], "A",
  "Past continuous for an action in progress interrupted by a short past event",
  "The counting was in progress when the power failure (a sudden, short event) happened. The longer background action "
  "takes the past continuous: 'While the clerk was counting the cash, the power went off.'",
  ["Short event: 'the power suddenly went off' (simple past)",
   "Background action in progress at that moment", "Past continuous: 'was counting'"],
  "'Counted' and 'had counted' present the counting as completed, which clashes with 'While'. 'Is counting' is present "
  "and does not match 'went off'.", 30)

Q(TE, "Perfect tenses", A,
  TE_STEM + "If he had accepted the transfer last year, he ______ a branch manager now.",
  ["would have been", "would be", "will be", "had been"], "B",
  "Mixed conditional: past condition (had + V3) with a present result (would + base verb)",
  "The condition is past ('had accepted ... last year') but the result is about the present ('now'). This mixed "
  "conditional uses 'would be' in the result clause: 'he would be a branch manager now'.",
  ["Condition: past perfect ('had accepted last year')", "Result time: 'now' (present)",
   "Present unreal result: 'would be'"],
  "'Would have been' refers to the past and clashes with 'now'. 'Will be' is used for real future conditions. 'Had "
  "been' cannot stand in the result clause.", 40)

Q(TE, "Perfect tenses", A,
  TE_STEM + "This is the third time this month that the bank's server ______ down.",
  ["went", "goes", "has gone", "had gone"], "C",
  "'This is the first/second/third time (that) ...' takes the present perfect",
  "After 'This is the third time that ...', the clause counts experiences up to now and takes the present perfect: "
  "'the server has gone down'.",
  ["Pattern: This is the [ordinal] time that ...", "Experience counted up to now → present perfect",
   "'has gone down'"],
  "'Went' (simple past) and 'goes' (simple present) do not follow this pattern. 'Had gone' is past perfect and needs "
  "a past reference point, which clashes with 'This is'.", 35)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", B,
  AR_STEM + "Her son has ______ MBA from ______ university in Pune.",
  ["a, an", "an, an", "an, a", "a, a"], "C",
  "'A' or 'an' depends on the first sound, not the first letter",
  "'MBA' is read 'em-bee-ay' and begins with a vowel sound, so it takes 'an'. 'University' begins with a 'yoo' "
  "(consonant) sound, so it takes 'a'.",
  ["'MBA' → first sound 'em' (vowel sound) → 'an'", "'university' → first sound 'yoo' (consonant sound) → 'a'",
   "Option C: an, a"],
  "A reverses the two articles. B uses 'an' before 'university'. D uses 'a' before 'MBA'.", 25)

Q(AR, "Definite and indefinite", I,
  AR_STEM + "The members elected her ______ chairperson of the cooperative bank.",
  ["a", "an", "the", "No article"], "D",
  "No article before a title held by one person, used as a complement after 'elect', 'appoint' or 'make'",
  "When a unique post is the complement of 'elect', 'appoint' or 'make', it takes no article: 'They elected her "
  "chairperson.'",
  ["Verb: 'elected' + object + post", "The post is unique (one chairperson)", "No article"],
  "'A' and 'an' would suggest one of several chairpersons. 'An' is also wrong before the consonant sound of "
  "'chairperson'. 'The' is not used before a title in this position.", 30)

Q(AR, "Definite and indefinite", A,
  AR_STEM + "Most of ______ lunch that we were served at ______ staff canteen yesterday was cold.",
  ["no article, the", "the, the", "a, a", "the, no article"], "B",
  "Meals normally take no article, but take 'the' when a particular meal is specified",
  "'Lunch' in general takes no article ('We had lunch'). Here a relative clause ('that we were served ... yesterday') "
  "picks out one particular lunch, so it takes 'the'; 'most of' also needs a determiner before a noun. 'Staff "
  "canteen' is a particular canteen known to the speakers, so it also takes 'the'.",
  ["Blank 1: a specific meal, defined by the relative clause → 'the lunch'",
   "Blank 2: a particular, known canteen → 'the staff canteen'", "Option B"],
  "A applies the general no-article rule for meals although this lunch is specified. C uses 'a', which cannot follow "
  "'Most of' and does not fit a specific, known canteen. D leaves the singular countable noun 'canteen' without any "
  "article.", 35)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", B, PP_STEM + "Her daughter is married ______ a doctor who works in Chennai.",
  ["with", "to", "by", "for"], "B",
  "Fixed preposition: 'married to' someone",
  "The adjective 'married' takes 'to': 'She is married to a doctor.'",
  ["Pattern: be married to + person"],
  "'Married with' is not standard for a spouse. 'Married by' names the person who conducted the ceremony. 'Married "
  "for' is used with a period of time ('married for ten years').", 20)

Q(PP, "Fixed prepositions", I,
  PP_STEM + "The new scheme is aimed ______ helping first-time women entrepreneurs.",
  ["for", "to", "at", "on"], "C",
  "Fixed preposition: 'aimed at' (+ noun or -ing form)",
  "'Aim' in the sense of 'intend for a purpose' takes 'at': 'The scheme is aimed at helping first-time women "
  "entrepreneurs.'",
  ["Expression: be aimed at", "Followed by a gerund: 'at helping'"],
  "'Aimed for', 'aimed to helping' and 'aimed on' are not the standard pattern; 'aimed to' would need a base verb "
  "('aimed to help'), not 'helping'.", 25)

Q(PP, "Fixed prepositions", A,
  PP_STEM + "A stable and predictable policy environment is conducive ______ long-term investment.",
  ["for", "with", "towards", "to"], "D",
  "Fixed preposition: 'conducive to' = making something likely to happen",
  "The adjective 'conducive' takes 'to': 'conducive to long-term investment'.",
  ["Adjective: 'conducive'", "Fixed pairing: 'conducive to'"],
  "'Conducive for', 'conducive with' and 'conducive towards' are not the standard collocation.", 25)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"

Q(CN, "Sentence connectors", B,
  "Choose the connector that best fills the blank.\n"
  "______ it was raining heavily, all the staff reached the branch on time.",
  ["Because", "Although", "Unless", "So"], "B",
  "Contrast connector 'Although' for an unexpected result",
  "Heavy rain would normally delay people, yet everyone was on time. 'Although' introduces a fact that contrasts with "
  "the main clause.",
  ["Clause 1: heavy rain (an obstacle)", "Clause 2: everyone on time (unexpected)", "Contrast → 'Although'"],
  "'Because' would make the rain the reason for punctuality. 'Unless' sets a condition. 'So' cannot open a clause "
  "that is joined to a following main clause like this.", 25)

Q(CN, "Sentence connectors", I,
  "Choose the connector that best fills the blank.\n"
  "Deposits in the bank's urban branches rose by ten per cent, ______ those in its rural branches fell slightly.",
  ["whereas", "because", "so that", "unless"], "A",
  "'Whereas' compares two contrasting facts",
  "The sentence sets two facts side by side: urban deposits rose; rural deposits fell. 'Whereas' links two "
  "contrasting statements of this kind.",
  ["Clause 1: urban deposits rose", "Clause 2: rural deposits fell", "Side-by-side contrast → 'whereas'"],
  "'Because' would make one change the cause of the other. 'So that' expresses purpose and 'unless' a condition; "
  "neither fits two facts being compared.", 30)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_003_plan.json").read_text(encoding="utf-8"))
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
            assert f" {bold} " in q["question_text"].replace("'", " ").replace(",", " "), (q["question_id"], bold)
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
    assert len({o["text"] for o in q["options"]}) == 4, q["question_id"]

# no reused stem or passage title across the earlier English files
earlier, titles = set(), set()
for f in EARLIER:
    data = json.loads((ROOT / "batches" / f).read_text(encoding="utf-8"))
    for q in data["questions"]:
        if q["subject"] == EN:
            earlier.add(q["question_text"].strip().lower())
    titles |= {s["title"].lower() for s in data.get("stimuli", []) if s["stimulus_id"].startswith("STIM_ENG")}
for s in STIMULI:
    assert s["title"].lower() not in titles, s["title"]
for q in QS:
    if q.get("stimulus_id") is None and q["topic"] not in (SC, WU, VO):  # shared fixed stems are allowed there
        assert q["question_text"].strip().lower() not in earlier, q["question_id"]
stems = [q["question_text"] for q in QS if q.get("stimulus_id") is None and q["topic"] not in (SC, WU, VO)]
assert len(stems) == len(set(stems)), "repeated stem inside this batch"

keys = Counter(q["correct_answer"] for q in QS)
assert max(keys.values()) <= 0.28 * len(QS) and min(keys.values()) >= 0.22 * len(QS), keys

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_003",
    "created_at": TODAY,
    "notes": "BATCH_003 English Language part: 150 original questions (BANK_ENG_000304 to BANK_ENG_000453). Six "
             "reading passages (29 questions) and three cloze passages (15 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 to BATCH_002; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules, words and idioms not tested in earlier batches. "
             "Each answer was set by the author and re-solved in a separate blind pass without the key. Pending human "
             "review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_003_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))})")
