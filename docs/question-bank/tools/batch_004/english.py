"""Writes batches/parts/BATCH_004_ENG.json: the 150 English Language questions of BATCH_004.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000 to BATCH_003, and the grammar rules, idioms and words tested are ones not tested in those batches. Run
from anywhere:

    python docs/question-bank/tools/batch_004/english.py

Structural checks (quota per topic and difficulty, subtopics, ID range, passage length, set sizes, option count, cloze
blank numbering, 'No error' / 'No replacement' placement, para-jumble option validity, repeated stems and passage
titles against all earlier English files, answer-key balance) are asserted before anything is written.
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
FIRST_ID = 454
FIRST_STIM = 4001
EARLIER = ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json", "parts/BATCH_002_ENG.json",
           "parts/BATCH_003_ENG.json")

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
P1 = stim("Bees on the farm", (
    "Most farmers think of bees, if they think of them at all, as insects that sting. Yet a large share of the fruits, "
    "vegetables and oilseeds grown in India depends on bees and other insects to carry pollen from one flower to "
    "another. Without this service, which nature provides free of charge, many plants would produce fewer and smaller "
    "fruits, or none at all.\n\n"
    "In recent years, beekeepers and scientists have noticed that wild bees are becoming harder to find in many farming "
    "areas. The reasons are not fully understood, but the loss of hedges and wild plants at the edges of fields, and "
    "the careless spraying of pesticides at times when bees are active, are thought to play a large part. A field that "
    "is sprayed in the middle of a sunny morning may lose its visiting bees in a single day.\n\n"
    "Some farmers have responded by keeping bees themselves. A few wooden boxes placed at the edge of a mustard or "
    "sunflower field can raise the yield of the crop, and the honey and wax they produce can be sold for extra income. "
    "Training in beekeeping is offered by agricultural universities and voluntary groups, and the cost of starting is "
    "modest compared with most other farm businesses. Women in several villages have formed groups that manage the "
    "boxes together and share the earnings.\n\n"
    "Beekeeping is not without difficulties. The bees must be moved or fed when flowers are scarce, the boxes must be "
    "checked regularly for disease, and the honey market is crowded with cheap, adulterated products that pull down the "
    "price for genuine producers. A beekeeper who cannot prove the purity of her honey may find it hard to earn a fair "
    "price.\n\n"
    "Still, the lesson of the bee box is a useful one. A farm is not a factory that runs on seeds, water and fertiliser "
    "alone. It depends on living helpers that ask for little except flowers and a little care, and a farmer who looks "
    "after them is also looking after the harvest."))

Q(RC, "Factual", B,
  "According to the passage, what service do bees provide to crops?",
  ["They feed on the pests that attack fruit and vegetable crops.",
   "They improve the quality of the soil in which the plants grow.",
   "They carry pollen between flowers, which helps the plants produce fruit.",
   "They shade young plants from the strong heat of the sun."], "C",
  "Locating a stated fact",
  "Paragraph 1 says crops depend on bees 'to carry pollen from one flower to another', and that without this service "
  "many plants would produce fewer and smaller fruits, or none at all.",
  ["Find the service in paragraph 1", "Bees carry pollen between flowers", "Without it, fewer fruits: option C"],
  "Eating pests (A), improving soil (B) and shading plants (D) are never mentioned as things bees do.", 45, P1, 1)

Q(RC, "Factual", B,
  "Which of the following does the passage mention as a likely reason why wild bees are becoming harder to find?",
  ["Spraying pesticides at times when bees are active",
   "Farmers harvesting too much honey from wild hives",
   "Unusually cold winters in farming areas",
   "Too many bee boxes placed at the edges of fields"], "A",
  "Locating a stated cause",
  "Paragraph 2 names two likely reasons: the loss of hedges and wild plants at field edges, and 'the careless spraying "
  "of pesticides at times when bees are active'.",
  ["Find 'wild bees are becoming harder to find' in paragraph 2", "Reasons given: loss of hedges; careless spraying",
   "Option A matches the second reason"],
  "B and C are not mentioned. D reverses the passage: bee boxes are a response by farmers, not a cause of the "
  "decline.", 45, P1, 2)

Q(RC, "Inference", B,
  "Why, according to the passage, may a beekeeper find it hard to earn a fair price for her honey?",
  ["Universities buy most of the honey from beekeepers at a fixed, very low price.",
   "Most people in India prefer sugar to honey and buy very little of it.",
   "Honey spoils quickly in hot weather and cannot be stored for long.",
   "Fake honey drags prices down, and she may be unable to show that hers is pure."], "D",
  "Inference: linking two sentences in the same paragraph",
  "Paragraph 4 says cheap, adulterated products 'pull down the price for genuine producers', and a beekeeper 'who "
  "cannot prove the purity of her honey may find it hard to earn a fair price'.",
  ["Problem 1: cheap, adulterated honey lowers prices", "Problem 2: genuine producers must prove purity",
   "Together: option D"],
  "A, B and C are not stated anywhere. Universities offer training, not a market for honey.", 50, P1, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'modest' as used in the passage ('the cost of starting is "
  "modest compared with most other farm businesses')?",
  ["shy", "small", "enormous", "boastful"], "B",
  "Vocabulary in context: modest (of an amount) = not large",
  "The sentence compares the cost of starting beekeeping with that of other farm businesses and presents it as an "
  "advantage. Here 'modest' describes an amount, so it means small or moderate.",
  ["'modest' here describes a cost, not a person", "Presented as an advantage → the cost is low", "'small'"],
  "'Shy' is a meaning of 'modest' only when it describes a person. 'Enormous' is the opposite. 'Boastful' is the "
  "opposite of the personal sense of 'modest'.", 35, P1, 4)

Q(RC, "Tone and title", B,
  "Which of the following is the most suitable title for the passage?",
  ["Bees: The Farmer's Unpaid Helpers", "How to Make Honey at Home",
   "The Dangers of Bee Stings", "Why Pesticides Must Be Banned"], "A",
  "A title must cover the main idea of the whole passage",
  "The passage explains how much crops depend on bees, why wild bees are declining, how keeping bees helps farmers "
  "and what difficulties it brings, ending with the idea that bees are 'living helpers that ask for little'.",
  ["Para 1: bees pollinate crops for free", "Paras 2–4: decline of wild bees; beekeeping and its problems",
   "Para 5: bees as helpers of the farm: option A"],
  "B is not discussed. C picks up only the opening remark about stings. D goes beyond the passage, which criticises "
  "careless spraying but never calls for a ban.", 45, P1, 5)

# ---------------------------------------------------------------- RC 2 (Basic, 5)
P2 = stim("Grandparents go online", (
    "When Kamala Devi, a retired schoolteacher of sixty-eight, received a smartphone from her son, she kept it in its "
    "box for three months. She was afraid of pressing the wrong button and losing money, and she did not want to keep "
    "asking her busy grandchildren for help. Her story is common. Millions of older Indians now own smartphones, but "
    "many use them only to receive calls.\n\n"
    "This matters more than it might seem. Pensions are credited to bank accounts, electricity bills and medical "
    "appointments are increasingly handled through apps, and family news is shared in video calls and messages. An "
    "older person who cannot use these services must depend on others for tasks that she once managed alone. For "
    "many, the loss of independence is harder to bear than the inconvenience.\n\n"
    "Some cities and towns now run free classes for senior citizens, often held in community halls and parks. "
    "Volunteers, many of them college students, sit with small groups and go through one task at a time: making a "
    "video call, reading a message, booking a doctor's appointment. Learners are also shown how to enlarge the text on "
    "the screen and how to type by speaking, which helps those with weak eyesight or unsteady hands. The classes move "
    "slowly, and nobody is laughed at for asking the same question twice.\n\n"
    "Kamala Devi joined such a class last year. Within a few weeks she was sending voice messages to her sister in "
    "another state, and she now pays her own electricity bill from her phone. What helped her most, she says, was not "
    "the technology itself but the patience of the young volunteer who taught her. 'At home, everyone was in a "
    "hurry,' she explains. 'Here, I was allowed to be slow.'\n\n"
    "The volunteers say they learn as much as they teach. Many had never spent long hours with anyone of their "
    "grandparents' age, and they discover stories, advice and humour they had not expected. A class meant to close a "
    "digital gap, it turns out, can close other gaps too."))

Q(RC, "Factual", B,
  "Why did Kamala Devi keep her new smartphone in its box for three months?",
  ["The phone did not work properly in her area, where the signal was weak.",
   "She feared losing money by a wrong press and did not want to trouble her grandchildren.",
   "Her son had asked her not to use it until he could show her how.",
   "She could not afford to pay the monthly charges for a connection."], "B",
  "Locating a stated reason",
  "Paragraph 1 gives two reasons: she 'was afraid of pressing the wrong button and losing money', and she 'did not "
  "want to keep asking her busy grandchildren for help'.",
  ["Find 'kept it in its box' in paragraph 1", "Read the next sentence: fear of losing money; not wanting to trouble "
   "her grandchildren", "Option B"],
  "A, C and D are not mentioned. The passage gives only the two reasons in option B.", 45, P2, 1)

Q(RC, "Factual", B,
  "Which of the following is NOT mentioned in the passage as something taught in the classes?",
  ["Making a video call", "Booking a doctor's appointment",
   "Enlarging the text on the screen", "Opening a new bank account"], "D",
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 3 lists making a video call, reading a message and booking a doctor's appointment, and adds enlarging the "
  "text and typing by speaking. Opening a bank account is not mentioned.",
  ["Paragraph 3: video call (A), doctor's appointment (B)", "Also: enlarging the text (C), typing by speaking",
   "Opening a bank account is not listed: D"],
  "A, B and C are all stated in paragraph 3, so none of them can be the 'NOT mentioned' answer. Bank accounts appear "
  "only in paragraph 2, where pensions are credited to them.", 45, P2, 2)

Q(RC, "Factual", B,
  "According to Kamala Devi, what helped her most in learning to use her phone?",
  ["The patience of the young volunteer who taught her",
   "The low price of the phone",
   "The printed instruction book that came with the phone",
   "Her grandchildren's help at home"], "A",
  "Locating a stated opinion",
  "Paragraph 4 says what helped her most 'was not the technology itself but the patience of the young volunteer who "
  "taught her'.",
  ["Find 'What helped her most' in paragraph 4", "Answer given: the volunteer's patience", "Option A"],
  "B and C are never mentioned. D contradicts the passage: at home 'everyone was in a hurry', and she did not want to "
  "keep asking her grandchildren.", 40, P2, 3)

Q(RC, "Inference", B,
  "What does the author suggest by saying that such a class 'can close other gaps too'?",
  ["The classes also help older people save money on their bills.",
   "The classes bring young and old people closer to each other.",
   "The classes reduce the gap between rich and poor towns.",
   "The classes close the gap between what phones cost and what people earn."], "B",
  "Inference: what a closing remark refers to",
  "The sentence before it says the young volunteers had rarely spent time with people of their grandparents' age and "
  "discover 'stories, advice and humour' they had not expected. The other gap closed is the one between generations.",
  ["Context: volunteers learn from the elderly learners", "Gap besides the digital one: between generations",
   "Option B"],
  "Money saved (A), rich and poor towns (C) and the cost of phones (D) are not discussed in the last paragraph.",
  50, P2, 4)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'bear' as used in the passage ('the loss of independence "
  "is harder to bear than the inconvenience')?",
  ["carry", "tolerate", "produce", "hold up"], "B",
  "Vocabulary in context: bear = endure, put up with",
  "Something 'hard to bear' is hard to endure or put up with. The passage says losing independence is harder to "
  "tolerate than the inconvenience itself.",
  ["Context: a painful experience", "'hard to bear' = hard to endure", "'tolerate'"],
  "'Carry' and 'hold up' are physical senses of 'bear', and 'produce' is the sense in 'bear fruit'. None fits a "
  "feeling that is hard to put up with.", 35, P2, 5)

# ---------------------------------------------------------------- RC 3 (Intermediate, 6)
P3 = stim("The cost of noise", (
    "Ask residents of an Indian city what troubles them most, and they will probably mention traffic, dust or the price "
    "of housing. Noise is rarely near the top of the list. People have come to accept the blare of horns, the roar of "
    "generators and the loudspeakers of weddings and festivals as part of urban life, as unavoidable as the weather. "
    "Yet a growing body of research suggests that this acceptance comes at a price.\n\n"
    "Noise does more than irritate. Long exposure to loud traffic at night disturbs sleep even when the sleeper does "
    "not fully wake, and poor sleep over months and years has been linked to high blood pressure and heart disease. "
    "Studies of schoolchildren in noisy neighbourhoods have found that they tend to score lower on reading tests than "
    "children in quieter areas, possibly because constant noise makes it harder to concentrate and to hear the teacher "
    "clearly. Workers exposed to loud machinery without protection may slowly lose part of their hearing without "
    "noticing until the damage is done.\n\n"
    "India has had rules on noise for more than two decades. They set limits for different zones, with the strictest "
    "applying to areas around hospitals, schools and courts, and they restrict the use of loudspeakers late at night. "
    "The difficulty lies in enforcement. Measuring noise requires equipment and trained staff, offenders are many and "
    "scattered, and a police officer who stops a wedding procession for being too loud can expect little thanks from "
    "anyone.\n\n"
    "Some cities have tried a different approach. Instead of relying only on fines, they have run campaigns against "
    "needless honking, installed displays at busy junctions showing the noise level as it happens, and declared "
    "'silent zones' where horns are banned. In one experiment, signals at a junction were set to stay red longer "
    "whenever drivers honked continuously, so that honking only prolonged their own wait.\n\n"
    "None of these measures will make a city quiet. But they treat noise as what it is: a form of pollution with real "
    "effects on health and learning, not merely a nuisance to be shrugged off. The first step towards a quieter city "
    "may simply be to stop regarding noise as normal."))

Q(RC, "Factual", I,
  "According to the passage, how can traffic noise at night harm a person's health even if it does not fully wake "
  "him?",
  ["It disturbs his sleep, and poor sleep over years is linked to high blood pressure and heart disease.",
   "It damages his hearing, and hearing loss over years is linked to heart disease.",
   "It lowers his concentration, and he scores worse on reading tests the next day.",
   "It forces him to take sleeping pills, which over time raise his blood pressure."], "A",
  "Locating a stated chain of cause and effect",
  "Paragraph 2: noise 'disturbs sleep even when the sleeper does not fully wake', and 'poor sleep over months and "
  "years has been linked to high blood pressure and heart disease'.",
  ["Find 'does not fully wake' in paragraph 2", "Noise → disturbed sleep → (over years) blood pressure, heart disease",
   "Option A"],
  "B confuses this with the workers exposed to loud machinery, who lose hearing slowly. C refers to schoolchildren, "
  "not night-time sleep; no link between hearing loss and heart disease is made. D (sleeping pills) is never "
  "mentioned.", 50, P3, 1)

Q(RC, "Factual", I,
  "Which of the following is NOT mentioned in the passage as a step some cities have taken against noise?",
  ["Campaigns against needless honking", "Displays at junctions showing the noise level",
   "Banning all wedding processions", "Zones where horns are banned"], "C",
  "Factual (NOT) question",
  "Paragraph 4 lists campaigns against honking, displays at junctions and silent zones. Wedding processions appear "
  "only in paragraph 3, as an example of why enforcement is unpopular; no city is said to have banned them.",
  ["Para 4: campaigns (A), displays (B), silent zones (D)", "Weddings appear only in para 3, not as a measure",
   "Option C"],
  "A, B and D are each stated in paragraph 4, so none of them is the 'NOT mentioned' answer.", 50, P3, 2)

Q(RC, "Inference", I,
  "What was the purpose of setting the signals to stay red longer when drivers honked continuously?",
  ["To give pedestrians more time to cross the road safely at busy hours",
   "To measure how loud the junction became at different hours of the day",
   "To identify drivers who honked so that they could be fined later",
   "To make honking prolong the drivers' own wait, so that they would stop"], "D",
  "Inference: the logic of an incentive",
  "Honking was meant to hurry the traffic, but under this experiment it 'only prolonged their own wait'. The design "
  "turns honking into something that costs the honker, giving drivers a reason to stop.",
  ["Effect of honking under the experiment: a longer red light", "So honking defeats its own purpose",
   "Aim: discourage honking: D"],
  "A, B and C give purposes the passage never mentions. No fines are linked to this experiment; it works by delay, "
  "not by penalty.", 55, P3, 3)

Q(RC, "Inference", I,
  "Why does the author mention a police officer who stops a wedding procession?",
  ["To show that weddings are the main source of noise in Indian cities",
   "To illustrate that enforcing noise rules is socially unpopular as well as difficult",
   "To suggest that the police should stop all processions",
   "To argue that noise rules do not apply to weddings"], "B",
  "Inference: the purpose of an example",
  "The example comes in a list of reasons why 'the difficulty lies in enforcement'. An officer who acts 'can expect "
  "little thanks from anyone', showing that enforcement meets public resentment.",
  ["Topic sentence: 'The difficulty lies in enforcement'", "Example: an officer who acts gets 'little thanks'",
   "So enforcement is unpopular: B"],
  "A overstates: weddings are one source among several. C and D are claims the author never makes.", 55, P3, 4)

Q(RC, "Tone and title", I,
  "Which of the following best describes the author's attitude towards the way city residents treat noise?",
  ["Approving", "Amused", "Critical", "Indifferent"], "C",
  "Tone: identify the author's judgement",
  "The author says that accepting noise 'comes at a price', that noise is 'a form of pollution ... not merely a "
  "nuisance to be shrugged off', and that we must 'stop regarding noise as normal'. The author disapproves of this "
  "acceptance.",
  ["Opening: acceptance 'comes at a price'", "Closing: stop regarding noise as normal",
   "The author disapproves: critical"],
  "'Approving' is the opposite. 'Amused' does not fit a passage about health damage. 'Indifferent' does not fit an "
  "author arguing for change.", 45, P3, 5)

Q(RC, "Vocabulary in context", I,
  "What does the phrase 'shrugged off' mean as used in the passage ('not merely a nuisance to be shrugged off')?",
  ["dismissed as unimportant", "measured carefully", "protested against loudly", "removed quickly"], "A",
  "Vocabulary in context: shrug off = treat as not worth worrying about",
  "The author contrasts treating noise as real pollution with treating it as a mere nuisance. To 'shrug off' "
  "something is to dismiss it as unimportant.",
  ["Contrast: 'pollution with real effects' vs 'a nuisance to be shrugged off'",
   "Shrugging = showing you do not care", "'dismissed as unimportant'"],
  "'Measured carefully' and 'protested against loudly' are the opposite of shrugging something off. 'Removed "
  "quickly' would mean the problem was solved, which is not the sense.", 40, P3, 6)

# ---------------------------------------------------------------- RC 4 (Intermediate, 6)
P4 = stim("Water that never arrives", (
    "A city's water supply is usually judged by how much water it can draw from rivers, lakes and wells. Far less "
    "attention goes to what happens to that water after it leaves the treatment plant. In many Indian cities, a large "
    "share of the water that is pumped and treated never reaches a paying customer. Engineers call this 'non-revenue "
    "water', and in some cities it is estimated to be close to half of the total supply.\n\n"
    "Part of the loss is physical. Old pipes crack, joints loosen and valves fail, and because most of the network "
    "lies underground, a leak can run for months before anyone notices. Part of it is commercial: water that does "
    "reach homes but is never billed, because meters are missing or broken, connections are illegal or records are "
    "out of date. Either way, the city pays to pump and clean water for which it earns nothing.\n\n"
    "The consequences are felt by everyone. Because so much water is lost, supply is often rationed to a few hours a "
    "day. When the pipes are empty, the pressure inside them falls, and dirty water from the surrounding soil can be "
    "drawn in through the same cracks through which clean water escapes. Families respond by installing storage tanks "
    "and private pumps, which pull water unevenly and leave households at the end of the line with even less.\n\n"
    "Reducing these losses is less glamorous than building a new dam or laying a pipeline from a distant river, and it "
    "rarely features in election speeches. It involves dividing the network into small zones, measuring how much "
    "water enters each, finding and repairing leaks block by block, and fixing meters and billing records. The work "
    "is slow and its results are invisible to the public. Yet every litre saved in this way is a litre that need not "
    "be found elsewhere, and it is usually far cheaper than a litre drawn from a new source.\n\n"
    "A city that cannot account for its water may not need more of it as urgently as it thinks. It may first need to "
    "stop losing what it already has."))

Q(RC, "Factual", I,
  "What does the term 'non-revenue water' refer to, according to the passage?",
  ["Water supplied free of charge to poor households",
   "Water drawn from rivers and lakes rather than wells",
   "Water that is pumped and treated but never reaches a paying customer",
   "Water that is too dirty to be sold"], "C",
  "Locating a definition",
  "Paragraph 1 defines it: 'a large share of the water that is pumped and treated never reaches a paying customer. "
  "Engineers call this \"non-revenue water\"'.",
  ["Find the quoted term in paragraph 1", "Read the sentence just before it", "Option C"],
  "A and D are not mentioned. B confuses the sources of water with what happens to it after treatment.", 45, P4, 1)

Q(RC, "Factual", I,
  "Which of the following is an example of what the passage calls a 'commercial' loss?",
  ["A cracked pipe that leaks underground for months",
   "Water that reaches a home through a broken meter and is never billed",
   "A valve that fails at the treatment plant",
   "Water lost when a storage tank overflows"], "B",
  "Applying a definition given in the passage",
  "Paragraph 2 contrasts physical losses (cracks, loose joints, failed valves) with commercial losses: 'water that does "
  "reach homes but is never billed, because meters are missing or broken ...'.",
  ["Physical loss: water escapes from the network", "Commercial loss: water is delivered but not billed",
   "Broken meter, no bill: option B"],
  "A and C are physical losses named in paragraph 2. D (overflowing tanks) is not mentioned as a loss of either "
  "kind.", 50, P4, 2)

Q(RC, "Inference", I,
  "Why, according to the passage, can rationing water to a few hours a day make it unsafe to drink?",
  ["People store water in tanks for so long that it becomes stale and unsafe.",
   "The treatment plant has less time to clean the water when supply is rationed.",
   "Private pumps add rust and chemicals to the water as they pull it unevenly.",
   "With little pressure in empty pipes, polluted groundwater can seep in through leaks."], "D",
  "Inference: following a stated mechanism",
  "Paragraph 3: 'When the pipes are empty, the pressure inside them falls, and dirty water from the surrounding soil "
  "can be drawn in through the same cracks through which clean water escapes.'",
  ["Rationing → pipes empty for most of the day", "Empty pipes → low pressure",
   "Low pressure → dirty water drawn in through cracks: D"],
  "A, B and C give reasons the passage never mentions. Private pumps are said to pull water unevenly, not to add "
  "chemicals.", 50, P4, 3)

Q(RC, "Inference", I,
  "Why does the author describe the work of reducing water losses as 'less glamorous' than building a new dam?",
  ["It is slow, its results are invisible, and it brings little political credit.",
   "It costs far more than building a new dam and gives poorer results.",
   "It does not save any water, since leaks reappear as soon as they are fixed.",
   "It can be carried out only by foreign engineers with costly equipment."], "A",
  "Inference: understanding a contrast",
  "Paragraph 4 says the work 'rarely features in election speeches' and that it 'is slow and its results are invisible "
  "to the public'. A new dam, by contrast, is visible and wins attention.",
  ["Not in election speeches → little political credit", "Slow; results invisible to the public",
   "Hence 'less glamorous': A"],
  "B contradicts the passage, which says a saved litre is 'usually far cheaper'. C contradicts 'every litre saved'. D "
  "is never mentioned.", 55, P4, 4)

Q(RC, "Inference", I,
  "Which of the following can be inferred from the last paragraph?",
  ["Cities should stop building treatment plants altogether.",
   "A city should cut the water it loses before rushing to find new sources.",
   "Cities already have more water than they can use.",
   "Water losses cannot be measured accurately."], "B",
  "Inference: the author's conclusion",
  "The last paragraph says a city 'may not need more of it as urgently as it thinks' and 'may first need to stop "
  "losing what it already has'. The priority is to reduce losses before seeking new supply.",
  ["Key words: 'may first need to stop losing'", "'first' sets a priority, not a ban on new sources",
   "Option B"],
  "A and C go far beyond the cautious 'may' in the paragraph. D contradicts paragraph 4, which describes measuring "
  "how much water enters each zone.", 50, P4, 5)

Q(RC, "Tone and title", I,
  "Which of the following is the most suitable title for the passage?",
  ["The Water Cities Lose Before It Reaches Homes", "Why India Needs More Dams",
   "How to Install a Storage Tank", "The History of Water Meters"], "A",
  "A title must cover the main idea of the whole passage",
  "The passage defines water lost after treatment, explains its causes and consequences, and argues that reducing "
  "these losses should come first. Only option A covers this.",
  ["Para 1: water lost after treatment", "Paras 2–3: causes and consequences",
   "Paras 4–5: reduce losses before seeking new water: A"],
  "B contradicts the author's argument. C and D pick up minor details (tanks, meters) from single paragraphs.",
  45, P4, 6)

# ---------------------------------------------------------------- RC 5 (Advanced, 5)
P5 = stim("The right to fail", (
    "Every economy that wants enterprise must decide what to do with those who try and fail. For much of history, the "
    "answer was harsh. Debtors who could not pay were imprisoned, their property seized and their names published as "
    "a warning to others. The assumption behind such treatment was that failure was a moral lapse, and that the "
    "prospect of disgrace would make borrowers more careful.\n\n"
    "Modern insolvency law rests on a different premise. Most businesses fail not because their owners are dishonest "
    "but because markets change, customers disappear or a promising idea turns out to be ahead of, or behind, its "
    "time. If the penalty for such failure is ruin for life, the rational response is not greater care but greater "
    "timidity. Talented people will avoid starting firms, and those who do start them will cling to a sinking venture "
    "for too long, hoping to avoid the stigma of closure, while its assets lose value and its debts mount.\n\n"
    "A well-designed system therefore tries to achieve two things at once. It must allow a failing firm to be resolved "
    "quickly, so that whatever value remains, in machines, buildings, a brand or a skilled workforce, can be sold or "
    "put to better use before it decays. And it must allow an honest entrepreneur, once the process is over, to start "
    "again without carrying the old debts for the rest of her life. The first goal protects creditors; the second "
    "protects the willingness to take risks on which economic growth depends.\n\n"
    "The two goals are not always in harmony. Creditors who expect to recover little may be reluctant to lend at all, "
    "or may lend only at higher rates and against heavy collateral, which hurts precisely the small firms the system "
    "is meant to encourage. A discharge granted too easily, on the other hand, invites abuse by borrowers who take "
    "money with no intention of repaying it. The skill lies in separating misfortune from fraud, and that requires "
    "courts and tribunals with the time and expertise to examine each case on its merits.\n\n"
    "Where the balance is struck well, failure becomes what it ought to be in a dynamic economy: an expensive lesson "
    "rather than a life sentence."))

Q(RC, "Inference", A,
  "According to the passage, what is the likely effect of making the penalty for business failure 'ruin for life'?",
  ["Entrepreneurs become more careful and fewer firms fail.",
   "Talented people avoid starting firms, and owners keep failing firms going for too long.",
   "Creditors recover more of their money from failed firms.",
   "Courts are able to separate misfortune from fraud more easily."], "B",
  "Inference: the author's argument against the old premise",
  "Paragraph 2 says the rational response to lifelong ruin 'is not greater care but greater timidity': talented "
  "people avoid starting firms, and those who start them 'cling to a sinking venture for too long' while assets lose "
  "value.",
  ["Old assumption: disgrace → more care", "Author's claim: harsh penalty → timidity, not care",
   "Two effects: fewer start-ups; failing firms kept alive too long: B"],
  "A is the old assumption the author rejects. C is the opposite: assets lose value while owners cling on. D is about "
  "the skill of tribunals, not the effect of harsh penalties.", 60, P5, 1)

Q(RC, "Factual", A,
  "Which two goals, according to the passage, should a well-designed insolvency system try to achieve at once?",
  ["Punishing dishonest borrowers and publishing their names",
   "Lowering interest rates and reducing collateral requirements",
   "Resolving failing firms quickly, and letting honest entrepreneurs make a fresh start",
   "Keeping every failing firm alive and protecting its workforce"], "C",
  "Locating a stated pair of goals",
  "Paragraph 3: the system 'must allow a failing firm to be resolved quickly' and 'must allow an honest entrepreneur "
  "... to start again without carrying the old debts'.",
  ["Find 'two things at once' in paragraph 3", "Goal 1: quick resolution; goal 2: a fresh start",
   "Option C"],
  "A describes the harsh historical approach. B names possible side effects discussed in paragraph 4, not goals. D "
  "contradicts the aim of resolving failing firms quickly.", 55, P5, 2)

Q(RC, "Inference", A,
  "Why, according to the passage, are the two goals 'not always in harmony'?",
  ["Generous discharge always leads borrowers to take loans with no intention of repaying them.",
   "Small firms no longer need loans once business failure is forgiven by the courts.",
   "Quick resolution always destroys the value of a failed firm's assets.",
   "Debt relief that is too generous can cut creditors' recoveries and make credit costlier for small firms."], "D",
  "Inference: identifying a trade-off",
  "Paragraph 4 explains the tension: creditors who expect to recover little lend less, or at higher rates and against "
  "heavy collateral, which 'hurts precisely the small firms the system is meant to encourage'; yet a discharge that is "
  "too easy invites abuse. Protecting debtors too generously works against creditors and, through them, against "
  "small borrowers.",
  ["Fresh start made too generous → creditors recover less",
   "Creditors then lend less, at higher rates, against heavy collateral → small firms hurt",
   "This is the conflict between the goals: D"],
  "A overstates the passage, which says easy discharge 'invites abuse', not that it always leads to fraud. B is "
  "not stated. C contradicts paragraph 3, where quick resolution is meant to preserve value 'before it "
  "decays'.", 65, P5, 3)

Q(RC, "Vocabulary in context", A,
  "Which of the following is closest in meaning to the word 'premise' as used in the passage ('Modern insolvency law "
  "rests on a different premise')?",
  ["building", "promise", "assumption", "conclusion"], "C",
  "Vocabulary in context: premise = a basic idea on which an argument rests",
  "The previous paragraph described the old 'assumption' that failure was a moral lapse. Modern law 'rests on a "
  "different premise': a different underlying assumption, namely that most failure is not dishonest.",
  ["Parallel: 'The assumption behind such treatment ...' → 'a different premise'",
   "'rests on' = is based on", "'premise' = assumption"],
  "'Building' confuses 'premise' with 'premises' (a building or site). 'Promise' only looks similar. A 'conclusion' "
  "is what an argument reaches, not what it rests on.", 40, P5, 4)

Q(RC, "Tone and title", A,
  "Which of the following is the most suitable title for the passage?",
  ["Failing Well: Why Insolvency Law Matters for Enterprise",
   "The Prisons Where Debtors Were Once Held",
   "How Banks Decide on Collateral",
   "Why Fraud Is Increasing Among Small Firms"], "A",
  "A title must cover the main idea of the whole passage",
  "The passage contrasts the old punishment of failure with modern insolvency law, sets out the two goals of a good "
  "system and the balance between them, and ends with failure as 'an expensive lesson rather than a life sentence'.",
  ["Para 1: harsh treatment of debtors in the past", "Paras 2–4: modern premise, goals and trade-off",
   "Para 5: failure as a lesson, not a sentence: A"],
  "B covers only the first paragraph. C picks up one detail from paragraph 4. D makes a claim the passage never "
  "makes.", 50, P5, 5)

# ---------------------------------------------------------------- RC 6 (Advanced, 4)
P6 = stim("Justice in one's own language", (
    "A villager who goes to court in India may find that the most important document in his case, the judgment, is "
    "written in a language he cannot read. In the higher courts, proceedings and judgments are largely in English, a "
    "language that only a small fraction of the population speaks with ease. Litigants must rely on lawyers to explain "
    "what has been decided about their own land, liberty or livelihood, and something is often lost, or added, in the "
    "explanation.\n\n"
    "The argument for change rests on a simple principle: law that binds people should be intelligible to them. A "
    "citizen who cannot understand why a court ruled against him is less likely to accept the ruling as fair, and less "
    "able to judge whether an appeal is worthwhile. Justice, in this view, must not only be done and be seen to be "
    "done; it must also be understood.\n\n"
    "Recent efforts to translate judgments into Indian languages, often with the help of software, are a step in this "
    "direction. Yet the translation of legal texts is unusually demanding. Legal terms carry precise meanings built up "
    "over decades of precedent, and a translation that is fluent but slightly inexact can mislead more dangerously than "
    "an awkward literal one. A word that suggests 'may' where the original says 'shall' can change a party's "
    "obligations entirely. For this reason, such translations are generally offered as an aid to understanding, while "
    "the English original remains the authoritative version.\n\n"
    "Critics point out that this arrangement, however sensible, preserves the very hierarchy it is meant to soften: "
    "the version that counts is still the one most citizens cannot read. Supporters reply that perfection should not "
    "be the enemy of progress. A careful translation, checked by people who know both the law and the language, may "
    "not carry legal authority, but it gives the litigant something he did not have before: the ability to read, in "
    "his own words, the reasons for a decision that shapes his life."))

Q(RC, "Inference", A,
  "The example of 'may' and 'shall' is used in the passage to show that",
  ["software cannot translate any legal text",
   "a fluent translation that is slightly inexact can change a party's legal obligations",
   "English legal terms have no equivalents in Indian languages",
   "judges should avoid using the word 'shall'"], "B",
  "Inference: the purpose of an example",
  "The example follows the claim that 'a translation that is fluent but slightly inexact can mislead more "
  "dangerously than an awkward literal one'. Replacing 'shall' (an obligation) with 'may' (a permission) changes what "
  "a party must do.",
  ["Claim: small inexactness can mislead dangerously", "Example: 'may' for 'shall' changes obligations",
   "Option B"],
  "A overstates: the passage says translation is demanding, not impossible. C is not claimed. D draws a lesson the "
  "passage never draws.", 55, P6, 1)

Q(RC, "Inference", A,
  "What do the critics mean when they say that the arrangement 'preserves the very hierarchy it is meant to soften'?",
  ["Translations will be available only to litigants who can afford them.",
   "Lawyers will lose their role in explaining judgments to their clients.",
   "Only the English version stays authoritative, though most citizens cannot read it.",
   "Courts in different states will begin to follow different versions of the law."], "C",
  "Inference: interpreting a critical claim",
  "The critics' own explanation follows the colon: 'the version that counts is still the one most citizens cannot "
  "read'. The ranking of English above Indian languages, which translation was meant to soften, remains.",
  ["Read after the colon", "Authoritative version = English", "So English still outranks the translation: C"],
  "A, B and D are not mentioned. The hierarchy is between languages, not between rich and poor litigants, lawyers or "
  "states.", 60, P6, 2)

Q(RC, "Inference", A,
  "By saying that 'perfection should not be the enemy of progress', the supporters argue that",
  ["translations should carry the same legal authority as the English original",
   "judgments should in future be written only in Indian languages",
   "software will soon be able to produce perfect legal translations",
   "an imperfect translation is still better than none at all"],
  "D",
  "Inference: the meaning of a maxim in context",
  "The supporters admit the translation 'may not carry legal authority', but say it still gives the litigant 'the "
  "ability to read, in his own words, the reasons for a decision'. An imperfect step is better than none.",
  ["The maxim: do not reject an improvement because it is imperfect", "Imperfection admitted: no legal authority",
   "Gain claimed: the litigant can read the reasons: D"],
  "A and B are changes the supporters do not propose; they accept that the English original remains authoritative. C "
  "is a prediction the passage never makes.", 55, P6, 3)

Q(RC, "Vocabulary in context", A,
  "Which of the following is closest in meaning to the word 'intelligible' as used in the passage ('law that binds "
  "people should be intelligible to them')?",
  ["clever", "understandable", "binding", "lengthy"], "B",
  "Vocabulary in context: intelligible = able to be understood",
  "The next sentences speak of a citizen who 'cannot understand' a ruling and say justice 'must also be understood'. "
  "'Intelligible' means understandable.",
  ["Context: citizens who cannot understand rulings", "'intelligible' = capable of being understood",
   "'understandable'"],
  "'Clever' is the meaning of 'intelligent', a different word. 'Binding' repeats 'law that binds'. 'Lengthy' has no "
  "connection with the sense.", 35, P6, 4)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic, 5)
C1 = stim("Learning to float", (
    "In many parts of rural India, children grow up close to water: village ponds, rivers, canals and, during the "
    "monsoon, flooded fields. Yet very few of them are ever taught to swim. Drowning is among the leading causes of "
    "death of young children in many countries, and India is no (1) ______. Most of these deaths happen quietly, close "
    "to home, often when an adult has looked away for only a few minutes.\n\n"
    "Some voluntary groups have begun to teach swimming in a simple, low-cost way. Classes are held in shallow, "
    "fenced-off parts of ponds, and trainers use empty plastic bottles and old tyre tubes to help children (2) ______ "
    "while they learn. Children are first taught to stay calm in the water and to lie on their backs, since panic is "
    "often more dangerous than the water itself. Only then do they learn to move towards the bank.\n\n"
    "Parents were (3) ______ at first. Many believed that a child who could swim would be tempted to go into deep "
    "water alone. Trainers answered this fear by teaching water safety along with swimming: never to swim without an "
    "adult nearby, to stay away from fast-flowing rivers, and to throw a rope or a bottle rather than jump in to "
    "(4) ______ a friend who is in trouble.\n\n"
    "Another simple measure is supervision. In some villages, mothers take turns to look after young children in a "
    "crèche during the busiest working hours, so that toddlers are not left (5) ______ near water while adults are in "
    "the fields. Together, these steps cost very little, yet they can save lives that are too often lost for lack of "
    "a few hours of training and a watchful eye."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["expression", "exception", "excuse", "exclusion"], "B",
  "Cloze: fixed expression 'be no exception' = be like the others",
  "The sentence says drowning is a leading cause of child deaths in many countries and that India is like them. "
  "'India is no exception' means India too has this problem.",
  ["First half: many countries have this problem", "Second half: India is the same",
   "Fixed expression: 'no exception'"],
  "'No expression', 'no excuse' and 'no exclusion' do not form a meaningful phrase that says India is like the other "
  "countries.", 35, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["sink", "shout", "float", "sleep"], "C",
  "Cloze: what bottles and tyre tubes do for a learner",
  "Empty bottles and tyre tubes are light and full of air. They help a learner stay on the surface of the water, "
  "that is, float.",
  ["Objects: empty bottles, tyre tubes (full of air)", "Purpose: keep the child on the surface", "'float'"],
  "'Sink' is the opposite of what these aids do. 'Shout' and 'sleep' have nothing to do with learning to swim.",
  35, C1, 2)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=3), ["delighted", "careless", "grateful", "hesitant"], "D",
  "Cloze: the next sentence explains the parents' attitude",
  "The next sentence says many parents feared that a child who could swim would go into deep water alone. Parents "
  "with this fear were unwilling or unsure at first: hesitant.",
  ["Next sentence: parents' fear", "'at first' → their attitude later changed", "'hesitant'"],
  "'Delighted' and 'grateful' contradict the fear described next. 'Careless' does not fit parents worried about "
  "their children's safety.", 35, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["rescue", "scold", "follow", "race"], "A",
  "Cloze: the purpose of jumping in after a friend in trouble",
  "A child might jump in to save a friend who is in trouble in the water. Trainers teach them to throw a rope or "
  "bottle instead. The verb is 'rescue'.",
  ["Situation: a friend in trouble in the water", "Natural purpose of jumping in: to save him", "'rescue'"],
  "Nobody jumps into water to 'scold', 'follow' or 'race' a friend who is in trouble.", 35, C1, 4)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=5), ["unknown", "unattended", "untidy", "unhappy"], "B",
  "Cloze: 'left ______ near water' while adults are away",
  "The crèche exists so that toddlers are not left without anyone watching them while adults work. 'Unattended' "
  "means without supervision.",
  ["Purpose of the crèche: someone looks after the children", "Danger avoided: no adult watching",
   "'left unattended'"],
  "'Unknown', 'untidy' and 'unhappy' do not describe the danger that supervision removes.", 35, C1, 5)

# ---------------------------------------------------------------- Cloze 2 (Intermediate 4 + Advanced 1)
C2 = stim("Reading the label", (
    "Walk down the aisle of any supermarket and you will find packets covered in cheerful promises: 'natural', "
    "'light', 'rich in fibre', 'no added sugar'. Such words are designed to catch the eye, but they reveal little about "
    "what is actually inside. The information that matters is usually printed in small type on the back of the pack, "
    "and few shoppers take the trouble to read it.\n\n"
    "A food label, read carefully, can be surprisingly (1) ______. The list of ingredients is arranged in order of "
    "weight, so if sugar or oil appears near the top, the product contains more of it than of anything listed below. "
    "The nutrition table shows the amount of energy, fat, sugar and salt in every hundred grams, which allows two "
    "products to be (2) ______ fairly even when their packs are of different sizes. A biscuit sold as a healthy choice "
    "may, on inspection, contain as much sugar as an ordinary cream biscuit.\n\n"
    "Manufacturers, however, have learned to (3) ______ these rules. Sugar may be split into several forms, such as "
    "glucose, invert syrup and malt extract, so that none of them appears high in the list on its own. Serving sizes "
    "may be set unrealistically small, making the figures per serving look modest. A drink labelled 'no added sugar' "
    "may still be heavily sweetened with fruit concentrate.\n\n"
    "For these reasons, many nutrition experts favour simple warnings on the front of the pack, such as a symbol "
    "showing that a product is high in salt or sugar. Such labels can be understood at a glance, even by a shopper in "
    "a hurry or one who does not read well. The industry has generally (4) ______ them, arguing that they unfairly "
    "brand foods as unhealthy. Evidence from countries that have adopted them suggests that they do change what people "
    "buy, and that manufacturers often respond by quietly (5) ______ their recipes to contain less salt and sugar, a "
    "change that benefits even those customers who never read the label."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["misleading", "decorative", "informative", "expensive"],
  "C",
  "Cloze: the sentences after the blank show what a label reveals",
  "The rest of the paragraph explains what a careful reader can learn from the ingredient list and the nutrition "
  "table, even that a 'healthy' biscuit is as sugary as a cream biscuit. Read carefully, a label is informative.",
  ["Following sentences: what the label tells you", "Contrast with the front-of-pack slogans that 'reveal little'",
   "'surprisingly informative'"],
  "'Misleading' contradicts the paragraph, which shows the back label revealing the truth. 'Decorative' and "
  "'expensive' have nothing to do with reading a label carefully.", 40, C2, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["compared", "combined", "consumed", "concealed"], "A",
  "Cloze: the purpose of figures per hundred grams",
  "Because the figures are given for the same quantity (one hundred grams), two products in packs of different sizes "
  "can be compared fairly.",
  ["Same base quantity for every product", "'even when their packs are of different sizes'",
   "Purpose: a fair comparison → 'compared'"],
  "'Combined', 'consumed' and 'concealed' do not go with 'fairly even when their packs are of different sizes'.",
  40, C2, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["abide by", "write down", "get around", "look up"], "C",
  "Cloze: 'however' and the examples of tricks that follow",
  "The paragraph lists tricks that keep the rules technically satisfied while hiding the truth: splitting sugar into "
  "several names, tiny serving sizes, fruit concentrate in 'no added sugar' drinks. Manufacturers have learned to get "
  "around (evade) the rules.",
  ["'however' contrasts with the honest reading of labels", "Examples: ways of evading the rules",
   "'get around these rules'"],
  "'Abide by' (obey) contradicts the tricks described. 'Write down' and 'look up' do not describe what manufacturers "
  "do with the rules.", 45, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["welcomed", "printed", "invented", "resisted"], "D",
  "Cloze: 'arguing that they unfairly brand foods' shows opposition",
  "An industry that argues the warnings 'unfairly brand foods as unhealthy' is opposing them. It has resisted them.",
  ["Reason given by the industry: the labels are unfair", "So the industry opposes them", "'resisted'"],
  "'Welcomed' contradicts the complaint. 'Printed' and 'invented' do not fit an industry that argues against the "
  "labels; the experts, not the industry, favour them.", 40, C2, 4)

Q(CL, "Single-blank cloze", A, CLOZE_STEM.format(n=5), ["advertising", "reformulating", "publicising", "patenting"],
  "B",
  "Cloze: 'quietly ______ their recipes to contain less salt and sugar'",
  "To make recipes 'contain less salt and sugar' is to change their composition: to reformulate them. 'Quietly' fits "
  "a change made without announcement.",
  ["Object: recipes; result: less salt and sugar", "Changing a recipe's make-up = reformulating",
   "'quietly' = without publicity, which also rules out advertising and publicising"],
  "'Advertising' and 'publicising' contradict 'quietly' and do not change what the recipe contains. 'Patenting' a "
  "recipe protects it legally but does not reduce its salt or sugar.", 45, C2, 5)

# ---------------------------------------------------------------- Cloze 3 (Advanced 6; error-based)
C3 = stim("The case for the index fund", (
    "An investor who buys shares through a mutual fund usually pays a professional manager to pick the companies most "
    "likely to do well. It seems a **(1) sensible** arrangement: experts with research teams should be able to beat "
    "ordinary savers. Yet study after study, in many countries, has found that most actively managed funds fail to "
    "outperform the market index they are measured against, especially over long periods and once their fees are "
    "**(2) ignored**.\n\n"
    "The reason is partly arithmetic. The market as a whole is made up of all investors together, so before costs the "
    "average actively managed rupee must earn roughly the market return. After fees, which can amount to a couple of "
    "per cent a year, the average active investor must therefore do **(3) better** than the market. A few managers will "
    "beat it in any given year, but picking them in advance has proved remarkably difficult, and past winners often "
    "become future laggards.\n\n"
    "An index fund takes the opposite approach. Instead of trying to pick winners, it simply buys all the shares in an "
    "index, such as the fifty largest companies on an exchange, in the same proportions. Because it needs no research "
    "team and trades rarely, its costs are a **(4) fraction** of those of an active fund. Over twenty or thirty years, "
    "that difference, compounded, can add up to a substantial sum.\n\n"
    "Index funds are not without **(5) merits**. An investor who owns the whole market owns its weaker companies along "
    "with its stronger ones, and has no protection when the market as a whole falls. Some critics also argue that if "
    "everyone invested passively, nobody would be left to study companies and set prices sensibly. For the ordinary "
    "saver, however, such concerns are remote. The more immediate danger is paying high fees for skill that may not "
    "exist, and the humble index fund offers a cheap and **(6) opaque** way to avoid it."))

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=1, ctx="It seems a sensible arrangement: experts with research teams should be able to beat "
                           "ordinary savers"),
  ["senseless", "sensitive", "sensational", NR], "D",
  "Error-based cloze: 'It seems ...' introduces a view the author then questions",
  "The sentence states the common view: paying experts seems reasonable, because experts 'should be able to beat "
  "ordinary savers'. 'Sensible' (reasonable) is correct. The 'Yet' in the next sentence questions this view, which "
  "only works if the arrangement first seems sensible.",
  ["'It seems ...' + the expert's advantage = a reasonable-looking arrangement", "'Yet' then challenges it",
   "'sensible' fits: no replacement"],
  "'Senseless' contradicts the reason after the colon. 'Sensitive' (easily affected) and 'sensational' (causing "
  "excitement) are look-alike words with the wrong meaning.", 45, C3, 1)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=2, ctx="most actively managed funds fail to outperform the market index ... once their fees are "
                           "ignored"),
  ["deducted", "overlooked", "waived", NR], "A",
  "Error-based cloze: fees make returns worse only when they are taken into account",
  "Funds fall behind the index 'once their fees are' taken out of their returns. Ignoring the fees would make the "
  "funds look better, not worse, so 'ignored' reverses the logic. The correct word is 'deducted'.",
  ["Fees reduce what the investor actually earns", "Funds fail to beat the index after fees are subtracted",
   "Replace 'ignored' with 'deducted'"],
  "'Overlooked' repeats the error of 'ignored'. 'Waived' means the fees are not charged at all, which would help the "
  "funds. 'Ignored' is wrong, so 'No replacement required' does not apply.", 50, C3, 2)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=3, ctx="After fees ... the average active investor must therefore do better than the market"),
  ["well", "worse", "best", NR], "B",
  "Error-based cloze: follow the arithmetic of the paragraph",
  "Before costs, the average active rupee earns roughly the market return. Subtracting fees of a couple of per cent "
  "must leave the average active investor behind the market: he does worse, not better.",
  ["Before fees: about the market return", "After fees: market return minus fees", "So: 'worse than the market'"],
  "'Well than' and 'best than' are ungrammatical with 'than'. 'Better' reverses the arithmetic, so 'No replacement "
  "required' does not apply.", 50, C3, 3)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=4, ctx="Because it needs no research team and trades rarely, its costs are a fraction of those of "
                           "an active fund"),
  ["multiple", "double", "fragment", NR], "D",
  "Error-based cloze: 'a fraction of' = a small part of",
  "An index fund needs no research team and trades rarely, so its costs are much lower than an active fund's: 'a "
  "fraction of' them. The word is correct.",
  ["Cause: no research team, little trading", "Effect: much lower costs", "'a fraction of' fits: no replacement"],
  "'A multiple of' and 'double' would make the index fund more expensive, contradicting the cause. 'A fragment of' is "
  "used for pieces of objects or texts, not for comparing costs.", 45, C3, 4)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=5, ctx="Index funds are not without merits. An investor who owns the whole market owns its "
                           "weaker companies"),
  ["virtues", "rewards", "drawbacks", NR], "C",
  "Error-based cloze: the sentences that follow decide the word",
  "The paragraph goes on to list weaknesses: owning weak companies, no protection when the market falls, the "
  "critics' worry about pricing. 'Not without drawbacks' introduces such a list; 'not without merits' would introduce "
  "advantages.",
  ["Following sentences: problems with index funds", "'not without ___' + a list of problems",
   "Replace 'merits' with 'drawbacks'"],
  "'Virtues' and 'rewards' repeat the error of 'merits'. 'Merits' is wrong, so 'No replacement required' does not "
  "apply.", 50, C3, 5)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=6, ctx="the humble index fund offers a cheap and opaque way to avoid it"),
  ["obscure", "simple", "costly", NR], "B",
  "Error-based cloze: the closing praise must match the passage",
  "The passage presents the index fund as straightforward: it 'simply buys all the shares in an index'. Calling the "
  "way 'opaque' (hard to understand) contradicts this and sits oddly beside 'cheap' as praise. 'Simple' fits.",
  ["The sentence praises the index fund", "Paragraph 3: it 'simply buys all the shares'",
   "Replace 'opaque' with 'simple'"],
  "'Obscure' repeats the error of 'opaque'. 'Costly' contradicts 'cheap' and the low costs of paragraph 3. 'Opaque' is "
  "wrong, so 'No replacement required' does not apply.", 45, C3, 6)

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


# ---- Basic (3)
ed("Part-wise error", B, "There is many reasons", "why customers prefer", "the new branch.", "A",
   "After 'there', the verb agrees with the noun that follows it",
   "In a 'there is / there are' sentence, the real subject comes after the verb. Here it is 'many reasons', which is "
   "plural, so the verb must be 'are': 'There are many reasons why customers prefer the new branch.'",
   ["Real subject: 'many reasons' (plural)", "'There' + plural subject → 'are'",
    "'There is' → 'There are': error in part A"],
   "Part B ('why customers prefer') and part C ('the new branch') are correct. A has an error, so 'No error' is "
   "wrong.", 30)

ed("Part-wise error", B, "The new clerk", "can able to handle", "the cash counter alone.", "B",
   "'Can' and 'be able to' express the same ability and are not combined",
   "'Can' is a modal verb followed by a base verb; 'able' is an adjective used with 'be'. They cannot be joined. "
   "Correct: 'The new clerk can handle ...' or 'The new clerk is able to handle ...'.",
   ["'can' + base verb, or 'is able to' + base verb", "'can able to' mixes the two",
    "Error in part B"],
   "Part A is a correct subject and part C a correct object and adverb. B has an error, so 'No error' is wrong.", 30)

ed("Part-wise error", B, "In the first week of a new job,", "almost every trainee", "does a few mistakes.", "C",
   "Collocation: we 'make' a mistake, not 'do' a mistake",
   "The noun 'mistake' collocates with 'make': 'almost every trainee makes a few mistakes'. 'Do a mistake' is not "
   "standard English.",
   ["Noun: 'mistakes'", "Fixed verb: 'make a mistake'", "'does' → 'makes': error in part C"],
   "Part A is a correct time phrase. Part B ('almost every trainee') is a correct singular subject. C has an error, "
   "so 'No error' is wrong.", 30)

# ---- Intermediate (7)
ed("Part-wise error", I, "After the complaint,", "the regional manager ordered for", "an inquiry into the delay.", "B",
   "'Order' (command that something be done) takes a direct object, with no 'for'",
   "To 'order an inquiry' is to command that one be held; the verb takes its object directly: 'the regional manager "
   "ordered an inquiry into the delay'. 'Order for' is not standard.",
   ["Verb: 'ordered' (commanded)", "It takes a direct object: 'ordered an inquiry'",
    "Drop 'for': error in part B"],
   "Part A is a correct time phrase. Part C ('an inquiry into the delay') uses the correct preposition 'into'. B has "
   "an error, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "The sweets that the customer", "brought for the staff", "tasted deliciously.", "C",
   "Linking (sense) verbs such as taste, smell, look and sound take an adjective, not an adverb",
   "'Tasted' here describes the sweets, not the way they performed an action, so it is a linking verb and needs an "
   "adjective: 'The sweets ... tasted delicious.'",
   ["Verb: 'tasted' = had a certain taste (linking verb)", "Linking verb + adjective",
    "'deliciously' → 'delicious': error in part C"],
   "Part A is a correct subject with a relative clause and part B completes it correctly. C has an error, so 'No "
   "error' is wrong.", 35)

ed("Part-wise error", I, "Could you please tell me", "where is the nearest ATM", "of your bank?", "B",
   "An embedded (indirect) question uses statement word order",
   "When a question is placed inside another sentence ('Could you tell me ...'), its subject comes before the verb: "
   "'where the nearest ATM of your bank is'. 'Where is the nearest ATM' keeps the order of a direct question.",
   ["Main question: 'Could you please tell me ...?'", "Embedded question → subject + verb order",
    "'where is the nearest ATM' → 'where the nearest ATM ... is': error in part B"],
   "Part A is a correct polite request. Part C ('of your bank?') is correct. B has an error, so 'No error' is "
   "wrong.", 35)

ed("Part-wise error", I, "I had my passbook update", "at the kiosk near the entrance", "before meeting the manager.",
   "A",
   "Causative 'have': have + object + past participle",
   "To say that someone else did the action for you, use 'have something done': 'I had my passbook updated'. The "
   "base form 'update' is wrong after the object here.",
   ["Pattern: have + object + past participle", "The passbook was updated (by the kiosk)",
    "'update' → 'updated': error in part A"],
   "Part B is a correct place phrase. Part C ('before meeting') correctly uses a gerund after a preposition. A has an "
   "error, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "The bank will not release", "the gold ornaments until", "the borrower does not repay the "
   "loan.", "C",
   "'Until' already marks the point at which a negative situation ends; it is not followed by another 'not'",
   "The meaning is: the ornaments stay with the bank up to the moment the loan is repaid. 'Until' + positive verb "
   "expresses this: 'until the borrower repays the loan'. Adding 'not' turns the sentence into nonsense.",
   ["Main clause is already negative: 'will not release'", "'until' + positive clause marks when that ends",
    "'does not repay' → 'repays': error in part C"],
   "Part A correctly uses 'will' in the main clause. Part B is correct. C has an error, so 'No error' is wrong.", 40)

ed("Part-wise error", I, "The home loan which I applied for it", "last month", "has finally been sanctioned.", "A",
   "A relative clause does not repeat its antecedent with a pronoun",
   "'Which' already stands for 'the home loan' as the object of 'applied for'. Adding 'it' repeats the object: 'The "
   "home loan which I applied for last month has finally been sanctioned.'",
   ["'which' = the home loan (object of 'applied for')", "'it' repeats the same object",
    "Drop 'it': error in part A"],
   "Part B is a correct time phrase. Part C correctly uses the present perfect passive with a singular subject. A has "
   "an error, so 'No error' is wrong.", 35)

ed("Error-free sentence", I, "The portraits of the bank's founders", "were hung in the main hall",
   "on the day of the centenary.", "D",
   "Hang – hung – hung (objects) vs hang – hanged – hanged (execution)",
   "Pictures and other objects are 'hung'; 'hanged' is used only for putting a person to death. 'The portraits ... "
   "were hung in the main hall' is correct, and the plural subject agrees with 'were'.",
   ["Part A: plural subject 'portraits'", "Part B: 'were hung': plural verb, correct past participle for objects",
    "Part C: correct time phrase", "No error: option D"],
   "A, B and C are each correct as shown in the steps. 'Hanged' would be wrong here, so B is not an error.", 35)

# ---- Advanced (2)
ed("Part-wise error", A, "Along the back wall of the strongroom", "stands two rows of steel lockers",
   "that are rented to customers.", "B",
   "With an inverted sentence (place phrase + verb + subject), the verb agrees with the subject that follows it",
   "The sentence opens with a place phrase, so the subject comes after the verb. The subject is 'two rows of steel "
   "lockers' (head noun 'rows', plural), so the verb must be plural: 'Along the back wall ... stand two rows of steel "
   "lockers'.",
   ["Opening place phrase → subject follows the verb", "Subject: 'two rows' (plural)",
    "'stands' → 'stand': error in part B"],
   "Part A is a correct opening phrase; 'strongroom' is not the subject. Part C ('that are rented') correctly agrees "
   "with 'lockers'. B has an error, so 'No error' is wrong.", 45)

ed("Error-free sentence", A, "It was the cashier,", "not the two managers, who was", "blamed for the shortfall in the "
   "vault.", "D",
   "In a cleft sentence ('It was X who ...'), the verb after 'who' agrees with X; a 'not ...' phrase in between does "
   "not change it",
   "The sentence highlights 'the cashier': 'It was the cashier who was blamed.' The phrase 'not the two managers' is "
   "a parenthetical contrast, so 'who' still refers to 'the cashier', which is singular. 'Who was' is correct.",
   ["Cleft structure: It was [the cashier] who ...", "'not the two managers' is a contrast set off by commas",
    "'who' = the cashier (singular) → 'was'", "No error: option D"],
   "Part A is a correct cleft opening. Part B is correct because 'who' refers to the cashier, not the managers. Part "
   "C is a correct passive complement. So none of them has an error.", 45)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", B,
  SI_STEM + "The branch remains open **between 10 a.m. to 4 p.m.** on weekdays.",
  ["from 10 a.m. and 4 p.m.", "between 10 a.m. and 4 p.m.", "between 10 a.m. till 4 p.m.", NI], "B",
  "Paired prepositions: 'between ... and', 'from ... to'",
  "'Between' pairs with 'and': 'between 10 a.m. and 4 p.m.'. ('From 10 a.m. to 4 p.m.' would also be correct, but it "
  "is not offered.)",
  ["'between' → 'and'", "'from' → 'to' (or 'till')", "Only 'between 10 a.m. and 4 p.m.' is correctly paired"],
  "'From ... and' and 'between ... till' mix the two pairs. The original 'between ... to' is also mixed, so 'No "
  "improvement required' is wrong.", 25)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "**My colleague and myself will attend** the training programme in Chennai.",
  ["Myself and my colleague will attend", "Me and my colleague will attend", "My colleague and I will attend", NI],
  "C",
  "Subject pronoun 'I' (not 'myself' or 'me') in a compound subject",
  "The pronoun is part of the subject, so it takes the subject form 'I'. A reflexive pronoun ('myself') is used only "
  "when it refers back to a subject already in the sentence. Courtesy also places 'I' last: 'My colleague and I'.",
  ["Test: drop 'My colleague and' → 'I will attend', not 'myself will attend'", "Subject form: 'I'",
   "'My colleague and I will attend'"],
  "'Myself' cannot act as a subject. 'Me' is an object pronoun. The original uses 'myself' as a subject, so 'No "
  "improvement required' is wrong.", 25)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "I **wish you will get** the loan you have applied for.",
  ["hope you will get", "wish you would got", "wish you get", NI], "A",
  "'Hope' for something possible in the future; 'wish' for unreal or regretted situations",
  "Getting the loan is a real possibility, and the speaker wants it to happen. That is expressed with 'hope' + "
  "'will': 'I hope you will get the loan.' 'Wish' + 'will' is not standard.",
  ["The outcome is still possible", "Wanting a possible outcome → 'hope'", "'I hope you will get the loan'"],
  "'Wish you would got' adds a past form after 'would'. 'Wish you get' is not standard. The original 'wish ... "
  "will' is wrong, so 'No improvement required' does not apply.", 30)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "All staff members **are suppose to** wear their identity cards inside the branch.",
  ["are supposing to", "were suppose to", "are supposed to", NI], "C",
  "'Be supposed to' (= be expected or required to) always uses the past participle 'supposed'",
  "The expression is 'be supposed to': 'All staff members are supposed to wear their identity cards.' The '-d' is "
  "often missed because it is not heard in speech.",
  ["Fixed expression: be + supposed + to", "Present, plural subject: 'are supposed to'"],
  "'Are supposing to' changes the meaning to 'imagining'. 'Were suppose to' still lacks the '-d' and changes the "
  "tense. The original lacks the '-d', so 'No improvement required' is wrong.", 25)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "The new mobile app is **very better than** the old one.",
  ["more better than", "much better than", "very good than", NI], "B",
  "Comparatives are strengthened with 'much' or 'far', not 'very'",
  "'Very' goes with the positive degree ('very good'); a comparative ('better') is intensified with 'much', 'far' or "
  "'a lot': 'much better than the old one'.",
  ["'better' is already comparative", "Intensifier for a comparative: 'much'", "'much better than'"],
  "'More better' is a double comparative. 'Very good than' cannot take 'than'. The original 'very better' is wrong, "
  "so 'No improvement required' does not apply.", 25)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "The children **enjoyed themselves** at the bank's annual staff picnic.",
  ["enjoyed", "enjoyed themself", "were enjoyed", NI], "D",
  "'Enjoy' needs an object; when there is no other object, a reflexive pronoun is used",
  "'Enjoy' is transitive: we enjoy something, or enjoy ourselves. 'The children enjoyed themselves at the picnic' is "
  "correct.",
  ["'enjoy' must take an object", "No other object here → reflexive 'themselves'", "Correct as it stands"],
  "'Enjoyed' alone leaves the verb without an object. 'Themself' does not match the plural 'children'. 'Were "
  "enjoyed' would mean someone enjoyed the children.", 25)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "When the manager slipped on the wet floor, the trainees **could not help to laugh**.",
  ["could not help laughing", "could not help but laughing", "could not helped laughing", NI], "A",
  "'Cannot help' (= cannot stop oneself) + gerund",
  "In the sense 'be unable to stop oneself', 'help' is followed by an -ing form: 'the trainees could not help "
  "laughing'. ('Could not help but laugh', with a base verb, is also used, but it is not offered.)",
  ["Expression: 'cannot help' = cannot avoid", "It takes a gerund", "'could not help laughing'"],
  "'Help but laughing' puts an -ing form after 'but', which needs a base verb. 'Could not helped' puts a past form "
  "after 'could'. The to-infinitive in the original is wrong, so 'No improvement required' does not apply.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "She has been handling the bank's foreign exchange desk **for last five years**.",
  ["since last five years", "for the last five years", "from last five years", NI], "B",
  "'For the last/past + period': the article is required",
  "A period counted back from now is 'the last five years' or 'the past five years'; the definite article is needed. "
  "With a period of time, 'for' is used: 'for the last five years'.",
  ["Period of time → 'for'", "'last five years' needs 'the'", "'for the last five years'"],
  "'Since' needs a point of time, not a period. 'From last five years' is not standard. The original drops 'the', so "
  "'No improvement required' is wrong.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "The farmer could not repay even the interest, **let alone of the principal**.",
  ["leave alone of the principal", "let alone for the principal", "let alone the principal", NI], "C",
  "'Let alone' (= and certainly not) is followed by the same kind of element as the one it is compared with",
  "'Let alone' links 'the interest' with 'the principal', both objects of 'repay'. The second item takes the same "
  "form as the first, with no added preposition: 'could not repay even the interest, let alone the principal'.",
  ["First item: 'the interest' (object of 'repay')", "Second item must match: 'the principal'",
   "No preposition after 'let alone'"],
  "'Leave alone of' and 'let alone for' add a preposition that the object of 'repay' cannot take. The original adds "
  "'of', so 'No improvement required' is wrong.", 35)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "The new scheme has been so designed **that to benefit** first-time borrowers.",
  ["as to benefit", "so that benefit", "that benefiting", NI], "A",
  "'So + adjective/participle + as to + infinitive' expresses purpose or result",
  "'So designed as to benefit' means designed in such a way that it benefits. After 'so' + participle, an infinitive "
  "is introduced by 'as to'; 'that' must be followed by a full clause ('so designed that it benefits').",
  ["'so designed' + infinitive → 'as to benefit'", "'so ... that' would need a subject and verb",
   "'has been so designed as to benefit'"],
  "'So that benefit' and 'that benefiting' have no subject and finite verb after 'that'. The original 'that to "
  "benefit' mixes the two patterns, so 'No improvement required' is wrong.", 40)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "**Such was the demand for the bonds that** the issue was closed within an hour.",
  ["Such was the demand for the bonds as", "So was the demand for the bonds that",
   "Such the demand for the bonds was that", NI], "D",
  "Inverted 'Such + be + subject + that' for emphasis on degree",
  "'Such was the demand ... that the issue was closed within an hour' is an emphatic inversion of 'The demand was "
  "such that ...'. 'Such' comes first, then the verb 'was', then the subject, then the 'that' clause of result.",
  ["Normal order: The demand was such that ...", "Emphatic inversion: Such was the demand ... that ...",
   "Correct as it stands"],
  "'Such ... as' introduces a comparison or example, not a result clause. 'So was the demand' needs an adjective "
  "after 'so' ('So great was the demand'). 'Such the demand ... was' breaks the inversion.", 40)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "**But for he had warned us in time**, we would have lost all our savings.",
  ["But for his timely warning", "But for he warned us in time", "But for that he had warned us in time", NI], "A",
  "'But for' (= if it had not been for) is followed by a noun phrase, not a clause",
  "'But for' works like a preposition and takes a noun phrase: 'But for his timely warning, we would have lost all "
  "our savings.' A full clause such as 'he had warned us' cannot follow it.",
  ["'But for' = without / if not for", "It takes a noun phrase", "'But for his timely warning'"],
  "'But for he warned' and 'But for that he had warned' place a clause after 'but for'. The original does the same, "
  "so 'No improvement required' is wrong.", 40)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "The branch's real problem is **not so much a lack of staff but** a lack of training.",
  ["not so much a lack of staff than", "not so much a lack of staff as", "not as much a lack of staff but", NI], "B",
  "Correlative pair: 'not so much X as Y' (= Y rather than X)",
  "The fixed pattern is 'not so much ... as ...': 'not so much a lack of staff as a lack of training'. 'But' and "
  "'than' do not complete it.",
  ["Pattern: not so much X as Y", "X = a lack of staff; Y = a lack of training", "'... as' completes the pair"],
  "'Than' and 'but' do not complete 'not so much'. The original uses 'but', so 'No improvement required' is wrong.",
  40)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", B,
  PR_STEM + "After hours of argument, the union finally **gave up to** the management's demand.",
  ["gave in to", "gave out to", "gave away to", NR], "A",
  "Phrasal verbs with 'give': give in (to) = yield, stop resisting",
  "After resisting for hours, the union yielded to the demand. 'Give in to' means stop opposing and accept. 'Give "
  "up' means stop trying, and does not take 'to' in this sense.",
  ["Context: resistance ends, demand accepted", "Meaning needed: yield", "'gave in to'"],
  "'Gave out' means ran out or distributed. 'Gave away' means gave freely or revealed. Neither means yield. The "
  "original 'gave up to' is wrong, so 'No replacement required' does not apply.", 30)

Q(PR, "Replace the phrase", B,
  PR_STEM + "The old photocopier **broke out** again in the middle of the month-end rush.",
  ["broke up", "broke in", "broke down", NR], "C",
  "Phrasal verbs with 'break': break down = stop working (of a machine)",
  "A machine that stops working 'breaks down'. 'Break out' is used for fires, wars and diseases that start "
  "suddenly.",
  ["Subject: a machine", "Meaning needed: stopped working", "'broke down'"],
  "'Broke up' means split apart or ended a relationship. 'Broke in' means entered by force. The original 'broke "
  "out' is wrong for a machine, so 'No replacement required' does not apply.", 30)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The merger has **brought about** major changes in the way the two banks work.",
  ["brought up", "brought out", "brought off", NR], "D",
  "Phrasal verbs with 'bring': bring about = cause to happen",
  "A merger causes changes. 'Bring about' means cause something to happen, so the sentence is correct.",
  ["Subject: the merger; object: major changes", "Meaning needed: caused", "'brought about' is correct"],
  "'Brought up' means raised (a topic or a child). 'Brought out' means published or revealed. 'Brought off' means "
  "achieved something difficult. None means 'caused'.", 30)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The clerk could not **make up** the faded handwriting on the old cheque.",
  ["make over", "make out", "make for", NR], "B",
  "Phrasal verbs with 'make': make out = manage to read, see or hear",
  "Faded handwriting is hard to read. 'Make out' means manage to read or see something with difficulty.",
  ["Object: faded handwriting", "Meaning needed: read with difficulty", "'make out'"],
  "'Make over' means transfer ownership or remodel. 'Make for' means move towards. 'Make up' means invent or form. "
  "The original is wrong, so 'No replacement required' does not apply.", 35)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", B, "A customer is asking a colleague for a short-term favour. " + SC_OK,
  ["Can you borrow me five hundred rupees till Friday?",
   "Could you lend me five hundred rupees till Friday?",
   "Can I lend five hundred rupees from you till Friday?",
   "Could you borrow five hundred rupees to me till Friday?"], "B",
  "Lend (give for a time) vs borrow (take for a time)",
  "The person who gives money for a time 'lends' it; the person who receives it 'borrows' it. Asking someone to give "
  "you money: 'Could you lend me ...?' (or 'Can I borrow ... from you?').",
  ["A: 'borrow me' wrongly uses 'borrow' for giving", "B: 'lend me': correct",
   "C: 'lend ... from you' wrongly uses 'lend' for receiving", "D: 'borrow ... to me' reverses the verbs"],
  "A, C and D each use 'lend' where 'borrow' is needed or the reverse.", 30)

Q(SC, "Grammatically incorrect sentence", I, SC_BAD,
  ["The bank decided to extend the deadline.",
   "The officer refused to sign the form.",
   "The spokesperson avoided to give a clear answer.",
   "The branch hopes to reopen next week."], "C",
  "Verbs followed by a gerund (avoid) vs verbs followed by a to-infinitive (decide, refuse, hope)",
  "'Avoid' is followed by an -ing form: 'The spokesperson avoided giving a clear answer.' 'Decide', 'refuse' and "
  "'hope' take a to-infinitive.",
  ["A: 'decided to extend': correct", "B: 'refused to sign': correct",
   "C: 'avoided to give' → 'avoided giving': incorrect", "D: 'hopes to reopen': correct"],
  "A, B and D are correct because 'decide', 'refuse' and 'hope' take a to-infinitive.", 35)

Q(SC, "Correct sentence", I, SC_OK,
  ["More than one customer have complained about the new charges.",
   "More than one customers has complained about the new charges.",
   "More than one customers have complained about the new charges.",
   "More than one customer has complained about the new charges."], "D",
  "'More than one' + singular noun takes a singular verb",
  "Although the meaning is plural, 'more than one' is followed by a singular noun and a singular verb: 'More than one "
  "customer has complained.'",
  ["Noun after 'more than one': singular ('customer')", "Verb agrees with the singular noun: 'has'",
   "Only D has both"],
  "A uses a plural verb. B and C use a plural noun after 'more than one'.", 35)

Q(SC, "Grammatically incorrect sentence", A, SC_BAD,
  ["Of the two offers, the latter seemed more attractive.",
   "Of rice, wheat and millets, the latter needs the least water.",
   "Of the bus and the train, the former is cheaper on this route.",
   "Of the three candidates, the last one was the most experienced."], "B",
  "'The former' and 'the latter' refer to one of exactly two items",
  "'Latter' means the second of two. With three items (rice, wheat and millets), the right word is 'the last' (or the "
  "item should be named): 'Of rice, wheat and millets, the last needs the least water.'",
  ["A: two offers → 'the latter': correct", "B: three crops → 'the latter': incorrect",
   "C: two items → 'the former': correct", "D: three candidates → 'the last': correct"],
  "A and C use 'former/latter' with exactly two items. D correctly uses 'the last' with three.", 40)

Q(SC, "Correct sentence", A, SC_OK,
  ["Every one of the applicants was interviewed twice.",
   "Every of the applicants was interviewed twice.",
   "Every one of the applicant was interviewed twice.",
   "Each applicants was interviewed twice."], "A",
  "'Every' cannot be followed directly by 'of'; use 'every one of' + plural noun + singular verb",
  "'Every' is a determiner and must be followed by a noun or by 'one'. 'Every one of the applicants' takes a plural "
  "noun after 'of' and a singular verb, because the subject is 'one'.",
  ["'every of' is impossible → 'every one of'", "'one of the' + plural noun ('applicants')",
   "Subject 'one' → singular 'was'"],
  "B uses 'every of'. C uses a singular noun after 'one of the'. D puts the plural 'applicants' after 'each', which "
  "needs a singular noun.", 40)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Volunteers then collect these dishes in insulated boxes soon after the kitchens close.\n"
  "(B) Every night, restaurants and wedding halls in large cities throw away food that was cooked but never served.\n"
  "(C) Some cities now have groups that try to rescue this food instead.\n"
  "(D) Within an hour, it is served at shelters and night schools to people who might otherwise go hungry.\n"
  "(E) They first persuade kitchens to set aside unserved dishes rather than throw them out.",
  ["BECAD", "BCAED", "BCEAD", "CBEAD"], "C",
  "Para jumble: problem → response → first step → next step ('then') → result",
  "B states the problem (cooked food thrown away). C ('this food') introduces groups that rescue it. E ('They first') "
  "describes their first step. A ('then', 'these dishes') follows. D ('Within an hour') gives the result.",
  ["Opener: B (the problem)", "B → C: 'this food' = the unserved food",
   "C → E: 'They' = the groups; 'first' step", "E → A ('then') → D ('Within an hour'): BCEAD"],
  "BECAD makes 'They' in E refer to the restaurants, who would not persuade themselves. BCAED puts the collection "
  "('then') before the first step. CBEAD opens with 'this food' before any food is mentioned.", 55)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) In some forest stretches, sensors have now been installed that detect large animals near the line.\n"
  "(B) Elephants often cross railway lines that run through forests, especially at night.\n"
  "(C) A train moving at full speed cannot stop in time, and collisions have killed many of them.\n"
  "(D) The alert reaches the driver early enough for him to slow down, giving the animals time to move away.\n"
  "(E) When a herd is detected, these sensors send an alert to approaching trains.",
  ["BCAED", "BACED", "BCEAD", "CBAED"], "A",
  "Para jumble: situation → danger → solution → how it works → result",
  "B introduces elephants crossing railway lines. C ('many of them') states the danger. A introduces sensors. E "
  "('these sensors') explains what they do. D ('The alert') gives the result.",
  ["Opener: B (names the elephants)", "B → C: 'them' = elephants; the problem",
   "C → A: the response (sensors)", "A → E ('these sensors') → D ('The alert'): BCAED"],
  "BACED offers the solution before the problem is stated. BCEAD uses 'these sensors' before sensors are introduced. "
  "CBAED opens with 'many of them' before the elephants are named.", 55)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) Every year, thousands of two-wheeler riders in India die in road accidents.\n"
  "(P) Many of these deaths, doctors say, are caused by head injuries.\n"
  "(Q) Yet many riders wear one only when they expect to see a traffic policeman, or strap it so loosely that it flies "
  "off in a crash.\n"
  "(R) A good helmet, worn properly, greatly reduces the risk of such injuries.\n"
  "(S) A helmet, in other words, protects only those who wear it as if their life depended on it, because it does.",
  ["PQRS", "RPQS", "PRSQ", "PRQS"], "D",
  "Fixed opener; 'these deaths', 'such injuries', 'one' and 'in other words' as links",
  "P ('these deaths') follows the deaths in (1) and names head injuries. R ('such injuries') introduces the helmet. "
  "Q ('Yet', 'wear one') contrasts with proper use. S ('in other words') sums up.",
  ["(1) → P: 'these deaths'", "P → R: 'such injuries' = head injuries",
   "R → Q: 'one' = a helmet; 'Yet' contrasts with 'worn properly'", "Q → S: conclusion: PRQS"],
  "PQRS uses 'wear one' before any helmet is mentioned. RPQS uses 'such injuries' before injuries are mentioned. "
  "PRSQ sums up 'in other words' before Q describes how riders misuse helmets.", 55)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) But if every household cuts its spending at the same time, shops sell less, firms cut jobs and incomes "
  "fall.\n"
  "(B) For a single family facing uncertain times, saving more is plainly sensible.\n"
  "(C) Economists call this outcome the paradox of thrift: what is prudent for one may be harmful for all.\n"
  "(D) Their attempt to save more may therefore leave them no richer than before, because their incomes have "
  "shrunk.\n"
  "(E) This is one reason why governments often raise their own spending in a downturn, when private spending is "
  "weak.",
  ["BACDE", "BADCE", "ABDCE", "BDACE"], "B",
  "Para jumble: individual case → 'But' all together → consequence → named idea → policy implication",
  "B gives the individual view. A ('But if every household ...') turns to everyone saving at once. D ('Their "
  "attempt', 'therefore') draws the consequence for those households. C ('this outcome') names it. E ('This is one "
  "reason') gives the policy response.",
  ["Opener: B (one family)", "B → A: 'But' turns from one family to every household",
   "A → D: 'Their' = the households; 'therefore' = consequence", "D → C ('this outcome') → E: BADCE"],
  "BACDE places C between A and D, so 'Their attempt' in D would refer to the economists. ABDCE opens with 'But'. "
  "BDACE draws the consequence ('therefore', 'incomes have shrunk') before A explains why incomes fall.", 70)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) In many towns, the months in which ice-cream sales rise are also the months in which more people "
  "drown.\n"
  "(P) That factor is hot weather, which sends more people to buy ice cream and, separately, more people to swim in "
  "rivers and lakes.\n"
  "(Q) Nobody seriously believes that eating ice cream makes people drown.\n"
  "(R) Mistaking such a coincidence for a cause can lead to policies that are useless, or worse.\n"
  "(S) Rather, both rise together because both depend on a third factor.",
  ["QPSR", "SPQR", "QSPR", "QSRP"], "C",
  "Fixed opener; 'Rather' needs a denial before it; 'That factor' needs a factor before it",
  "Q denies the absurd causal reading. S ('Rather') gives the real explanation, a third factor. P ('That factor') "
  "names it. R draws the general lesson about mistaking coincidence for cause.",
  ["(1) → Q: rejects the idea that ice cream causes drowning", "Q → S: 'Rather' corrects the rejected idea",
   "S → P: 'That factor' = the third factor", "P → R: general lesson: QSPR"],
  "QPSR uses 'That factor' before any factor is mentioned. SPQR opens with 'Rather' when nothing has been denied. "
  "QSRP puts the lesson between S and P, leaving 'That factor' far from its referent.", 70)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) For most Indian families, gold is not only an ornament but also a store of savings.\n"
  "(P) With such a mark, a family that sells or pledges its jewellery years later can expect a fair value for it.\n"
  "(Q) Yet a buyer can rarely tell, just by looking, whether a necklace is as pure as the jeweller claims.\n"
  "(R) Under the system, each piece is tested independently and stamped with a mark that certifies its purity.\n"
  "(S) This is the gap that hallmarking was introduced to close.",
  ["QSRP", "QRSP", "SQRP", "QSPR"], "A",
  "Fixed opener; 'Yet', 'This is the gap', 'Under the system' and 'such a mark' as links",
  "Q ('Yet') raises the problem: buyers cannot judge purity. S ('This is the gap') names hallmarking as the answer. R "
  "('Under the system') explains how it works. P ('such a mark') gives the benefit.",
  ["(1) → Q: 'Yet' contrasts gold's value with the buyer's uncertainty", "Q → S: 'the gap' = Q's problem",
   "S → R: 'the system' = hallmarking", "R → P: 'such a mark' = the certifying mark: QSRP"],
  "QRSP mentions 'the system' before hallmarking is named. SQRP opens with 'This is the gap' before any gap is "
  "described. QSPR uses 'such a mark' before the mark is described.", 70)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", B,
  SR_STEM + "(P) the lost passbook\n(Q) handed over\n(R) to the branch manager\n(S) the honest watchman",
  ["PQSR", "SPQR", "QSPR", "SQPR"], "D",
  "Subject + verb + object + 'to' phrase",
  "'The honest watchman handed over the lost passbook to the branch manager.' The subject (S) comes first, then the "
  "verb (Q), the object (P) and the receiver (R).",
  ["Subject: S ('the honest watchman')", "Verb: Q ('handed over')", "Object: P; receiver: R: SQPR"],
  "PQSR would make the passbook hand over the watchman. SPQR puts the object between the subject and the verb. QSPR "
  "starts with the verb.", 30)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) that the branch would remain\n(Q) the notice on the door\n(R) closed until Monday\n(S) said",
  ["SQPR", "QSPR", "QSRP", "PRQS"], "B",
  "Subject + reporting verb + 'that' clause (subject + verb + complement)",
  "'The notice on the door said that the branch would remain closed until Monday.' Subject (Q), verb (S), then the "
  "reported clause: P ('that the branch would remain') completed by R ('closed until Monday').",
  ["Subject: Q", "Reporting verb: S ('said')", "'that' clause: P + R: QSPR"],
  "SQPR starts with the verb. QSRP separates 'remain' from its complement and leaves 'closed until Monday' before "
  "'that'. PRQS puts the reported clause before its subject and verb without the punctuation such an order needs.",
  35)

Q(SR, "Word/phrase rearrangement within a sentence", A,
  SR_STEM + "(P) that the cheque\n(Q) little did\n(R) the shopkeeper suspect\n(S) had been forged",
  ["RQPS", "QPRS", "QRPS", "QRSP"], "C",
  "Inversion after a negative adverb at the start: 'Little did + subject + base verb'",
  "'Little did the shopkeeper suspect that the cheque had been forged.' 'Little did' (Q) needs the subject and base "
  "verb next (R), then the 'that' clause (P) completed by its verb (S).",
  ["Opener: Q ('Little did')", "Inverted subject + verb: R ('the shopkeeper suspect')",
   "'that' clause: P + S: QRPS"],
  "RQPS places 'little did' after the subject and verb. QPRS puts the 'that' clause before the subject. QRSP puts "
  "'had been forged' before its subject 'the cheque'.", 40)

Q(SR, "Word/phrase rearrangement within a sentence", A,
  SR_STEM + "(P) what matters\n(Q) is not how much you earn\n(R) most to a lender\n(S) but how regularly you repay",
  ["PRQS", "PQRS", "RPQS", "PQSR"], "A",
  "A 'what' clause as subject; 'not X but Y' after the main verb",
  "'What matters most to a lender is not how much you earn but how regularly you repay.' The subject is the clause "
  "'What matters most to a lender' (P + R), the verb is 'is' (Q), and 'not ... but ...' is completed by S.",
  ["Subject clause: P + R ('What matters most to a lender')", "Verb + first item: Q ('is not how much you earn')",
   "Second item: S ('but how regularly you repay'): PRQS"],
  "PQRS and PQSR separate 'matters' from 'most to a lender'. RPQS opens with 'most to a lender', which cannot begin "
  "the sentence.", 40)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The shopkeeper was ______ five thousand rupees for selling adulterated cooking oil.",
  ["praised", "promoted", "thanked", "fined"], "D",
  "Single blank: the verb that takes an amount of money as a penalty",
  "Selling adulterated oil is an offence, and an amount of money follows the verb. A penalty in money is a fine: "
  "'was fined five thousand rupees'.",
  ["Offence: selling adulterated oil", "Verb + amount of money as punishment", "'fined'"],
  "'Praised', 'promoted' and 'thanked' do not fit an offence and cannot take an amount of money as their object.",
  20)

Q(FB, "Single blank", B,
  FB1 + "Never share your PIN with anyone; it must be kept ______ at all times.",
  ["visible", "public", "famous", "confidential"], "D",
  "Single blank: the clause before the semicolon explains the blank",
  "A PIN that must never be shared has to be kept secret. 'Confidential' means meant to be kept secret.",
  ["Clue: 'Never share your PIN'", "Meaning needed: secret", "'confidential'"],
  "'Visible', 'public' and 'famous' all suggest that others know the PIN, the opposite of what is needed.", 20)

Q(FB, "Double blank", B,
  FB2 + "The bridge was ______ by the floods, so the bus had to take a much ______ route to the town.",
  ["damaged, longer", "repaired, shorter", "built, direct", "opened, quicker"], "A",
  "Double blank: cause and result joined by 'so'",
  "Floods damage bridges. With the bridge out of use, the bus had to go round another way, which is longer.",
  ["Blank 1: what floods do to a bridge → 'damaged'", "'so' → the bus could not use the bridge",
   "Blank 2: a detour is longer → 'longer'"],
  "Floods do not repair, build or open bridges, and a usable bridge would not force the bus onto another route.", 30)

Q(FB, "Phrase fillers", B,
  FBP + "After playing, the children were asked to ______ their toys in the cupboard.",
  ["give in", "run into", "put away", "take after"], "C",
  "Phrasal verb: put away = put something back in its proper place",
  "After playing, toys are put back where they belong: the children 'put away' their toys in the cupboard.",
  ["Context: tidying up after play", "Meaning needed: put back in place", "'put away'"],
  "'Give in' means yield. 'Run into' means meet by chance or collide with. 'Take after' means resemble a parent.",
  25)

Q(FB, "Single blank", I,
  FB1 + "His ______ remarks about the new clerk's accent offended several colleagues at the meeting.",
  ["tactful", "timely", "tactless", "tentative"], "C",
  "Single blank: the result ('offended several colleagues') decides the word",
  "Remarks about someone's accent that offend others show a lack of sensitivity. 'Tactless' means without "
  "consideration for others' feelings.",
  ["Result: colleagues were offended", "Remarks lacked sensitivity", "'tactless'"],
  "'Tactful' is the opposite and would not offend. 'Timely' and 'tentative' do not explain why the remarks "
  "offended.", 25)

Q(FB, "Single blank", I,
  FB1 + "The company's claim to be 'eco-friendly' turned out to be ______; its factory was still dumping waste into "
  "the river.",
  ["spurious", "genuine", "modest", "accurate"], "A",
  "Single blank: the clause after the semicolon shows the claim was false",
  "A company dumping waste into a river is not eco-friendly, so its claim was false. 'Spurious' means false or fake, "
  "though made to look genuine.",
  ["Evidence: still dumping waste", "So the claim was false", "'spurious'"],
  "'Genuine' and 'accurate' contradict the evidence. 'Modest' does not describe a claim proved false.", 25)

Q(FB, "Single blank", I,
  FB1 + "The relief kits were distributed ______: some families received three, while others on the same street got "
  "none.",
  ["fairly", "promptly", "generously", "haphazardly"], "D",
  "Single blank: the example after the colon defines the word",
  "Some families got three kits and their neighbours none: the distribution followed no order or plan. "
  "'Haphazardly' means without order or planning.",
  ["Evidence: very unequal shares on the same street", "Distribution without a plan", "'haphazardly'"],
  "'Fairly' contradicts the uneven shares. 'Promptly' (quickly) and 'generously' do not explain why some got nothing.",
  25)

Q(FB, "Double blank", I,
  FB2 + "The witness's account was so ______ that the police found it hard to ______ the sequence of events.",
  ["precise, recall", "confused, reconstruct", "clear, follow", "coherent, understand"], "B",
  "Double blank: 'so ... that' – the quality of the account must explain the difficulty",
  "The police had difficulty working out the order of events, so the account must have been unclear: 'so confused "
  "that the police found it hard to reconstruct the sequence of events'.",
  ["'so ... that ... hard to' → the account caused difficulty", "Blank 1: a quality that causes difficulty → "
   "'confused'", "Blank 2: what police do with events → 'reconstruct'"],
  "A precise, clear or coherent account would make the events easy, not hard, to recall, follow or understand.", 35)

Q(FB, "Double blank", I,
  FB2 + "Though ______ in its aims, the housing scheme proved ______ in its execution, and few of the promised homes "
  "were ever built.",
  ["noble, impressive", "narrow, successful", "laudable, flawed", "vague, flawless"], "C",
  "Double blank: 'Though' sets a good aim against a poor result",
  "The result ('few of the promised homes were ever built') shows the execution was poor. 'Though' needs a contrast, "
  "so the aims were good: 'laudable in its aims, flawed in its execution'.",
  ["Result clue: few homes built → execution poor → 'flawed'", "'Though' → contrast → aims good → 'laudable'",
   "Option C"],
  "'Impressive', 'successful' and 'flawless' execution all contradict 'few of the promised homes were ever built'.",
  35)

Q(FB, "Phrase fillers", I,
  FBP + "Investigators finally ______ the missing funds: a clerk had been quietly diverting small sums for months.",
  ["got by", "got away with", "got on with", "got to the bottom of"], "D",
  "Idiomatic phrase: get to the bottom of = discover the real cause or truth of",
  "The words after the colon give the truth that the investigators discovered. To 'get to the bottom of' something "
  "is to find out its real cause.",
  ["After the colon: the explanation discovered", "Meaning needed: found the truth about", "'got to the bottom of'"],
  "'Got by' means managed to survive. 'Got away with' means escaped punishment for, which describes the clerk, not "
  "the investigators. 'Got on with' means continued doing.", 30)

Q(FB, "Phrase fillers", I,
  FBP + "With the promotion exam only a month away, Ravi decided to ______ and study every evening after work.",
  ["back down", "break down", "bog down", "buckle down"], "D",
  "Phrasal verb: buckle down = start working seriously and with determination",
  "An exam a month away is a reason to start working hard. 'Buckle down' means begin to work seriously.",
  ["Context: exam approaching; studying every evening", "Meaning needed: start working hard", "'buckle down'"],
  "'Back down' means withdraw from a position. 'Break down' means stop working or lose control of one's feelings. "
  "'Bog down' means get stuck and cannot be used without an object here.", 30)

Q(FB, "Single blank", A,
  FB1 + "Critics dismissed the committee's report as ______, saying it merely repeated well-worn truisms in "
  "long-winded language without offering a single fresh idea.",
  ["incisive", "seminal", "cogent", "platitudinous"], "D",
  "Single blank: the participle phrase defines the word",
  "A report that 'merely repeated well-worn truisms' with no fresh idea is full of platitudes: it is "
  "'platitudinous' (dull, stale and obvious).",
  ["Clue: 'well-worn truisms', 'without a single fresh idea'", "A platitude = an overused, obvious remark",
   "'platitudinous'"],
  "'Incisive' (sharp and clear), 'seminal' (highly original and influential) and 'cogent' (convincing) are words of "
  "praise that contradict 'dismissed'.", 35)

Q(FB, "Double blank", A,
  FB2 + "The auditor's ______ eye for detail meant that not even the smallest ______ in the accounts escaped her "
  "notice.",
  ["meticulous, discrepancy", "cursory, discrepancy", "meticulous, accuracy", "casual, error"], "A",
  "Double blank: the result must match the quality; collocation 'discrepancy in the accounts'",
  "'Not even the smallest ... escaped her notice' shows extreme care, so the eye was 'meticulous'. What an auditor "
  "notices in accounts is a mismatch: a 'discrepancy'.",
  ["Result: nothing escaped her → very careful → 'meticulous'",
   "What an auditor catches: a mismatch → 'discrepancy'", "Option A"],
  "'Cursory' and 'casual' mean careless, contradicting the result. 'Accuracy' is not something that 'escapes' an "
  "auditor's notice as a fault.", 35)

Q(FB, "Phrase fillers", A,
  FBP + "Rather than ______ the growing rift between the two directors, the chairman decided to confront it openly at "
  "the next board meeting.",
  ["iron out", "thrash out", "paper over", "weigh in"], "C",
  "Phrasal verb: paper over = hide a problem instead of dealing with it",
  "'Rather than ... confront it openly' sets up a contrast with concealment. To 'paper over' a rift is to hide it "
  "without solving it.",
  ["Contrast: X vs 'confront it openly'", "X must mean hide or avoid", "'paper over'"],
  "'Iron out' and 'thrash out' mean resolve or discuss thoroughly, which do not contrast with confronting the "
  "problem. 'Weigh in' (join a discussion) does not take an object like this.", 35)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'stationary' used correctly?",
  ["She bought some stationary for the new office.",
   "The traffic remained stationary for over an hour.",
   "The bank's stationary budget has been cut this year.",
   "Pens and files are sold at the stationary shop."], "B",
  "Stationary (not moving) vs stationery (paper, pens and office supplies)",
  "'Stationary' is an adjective meaning not moving. Traffic that does not move for an hour is stationary.",
  ["A: office supplies → 'stationery'", "B: traffic not moving → 'stationary': correct",
   "C: budget for office supplies → 'stationery'", "D: shop selling pens and files → 'stationery'"],
  "A, C and D all refer to paper, pens and office supplies, which is 'stationery' (spelt with -ery).", 30)

Q(WU, "Word swap", I,
  WS_STEM + "The **(A) loan** sanctioned the **(B) manager** after checking the farmer's **(C) land** records and "
  "**(D) income** proof.",
  ["A-C", "C-D", "A-B", "No swap required"], "C",
  "Word swap: check who can perform each action",
  "A loan cannot sanction anything, and a manager is not sanctioned. Swapping A and B gives: 'The manager sanctioned "
  "the loan after checking the farmer's land records and income proof.'",
  ["'The loan sanctioned' is meaningless → A is misplaced", "The doer must be a person: the manager (B)",
   "Swap A and B"],
  "A-C gives 'The land sanctioned the manager'. C-D gives 'income records and land proof' and leaves 'The loan "
  "sanctioned the manager'. The sentence clearly needs a swap.", 35)

Q(WU, "Correct usage of a word", I,
  "In which of the following sentences is the word 'credulous' used correctly?",
  ["The court accepted the witness's credulous account.",
   "The bank's credulous balance sheet reassured investors.",
   "Her story was so credulous that everyone believed it.",
   "The credulous villagers believed the agent's promise to double their money in a month."], "D",
  "Credulous (too ready to believe things) vs credible (believable)",
  "'Credulous' describes a person who believes things too easily. Villagers who believed a promise to double their "
  "money in a month were credulous.",
  ["A: an account that can be believed → 'credible'", "B: a balance sheet that inspires trust → 'credible'",
   "C: a believable story → 'credible'", "D: people who believe too easily → 'credulous': correct"],
  "A, B and C describe accounts, documents or stories that are believable, which is 'credible'. 'Credulous' can only "
  "describe the person doing the believing.", 35)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'abeyance' as used in the sentence:\n"
  "'The construction of the new branch building has been held in abeyance until the land dispute is settled.'",
  ["temporary suspension", "full progress", "public view", "legal ownership"], "A",
  "Abeyance (in 'held in abeyance') = a state of temporary suspension",
  "Construction cannot go on while the land dispute is unsettled; it is paused until then. 'In abeyance' means "
  "temporarily suspended.",
  ["Clue: 'until the land dispute is settled'", "Work is paused for a time", "'abeyance' = temporary suspension"],
  "'Full progress' contradicts 'until the dispute is settled'. 'Public view' and 'legal ownership' do not describe "
  "the state of the construction work.", 30)

Q(VO, "Word pairs", A, "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Querulous – Peevish", "Truculent – Docile", "Bellicose – Belligerent", "Insipid – Bland"], "B",
  "Advanced vocabulary: synonym and antonym pairs",
  "'Truculent' means eager to argue or fight; 'docile' means quiet and easily controlled. They are opposites. The "
  "other pairs are synonyms.",
  ["Querulous = peevish (complaining, irritable)", "Truculent (aggressive) ≠ docile (submissive)",
   "Bellicose = belligerent (warlike)", "Insipid = bland (lacking flavour or interest)"],
  "A, C and D are pairs of synonyms, not opposites.", 35)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", B,
  SY_STEM + "The security guard stayed **alert** throughout the night shift.",
  ["sleepy", "careless", "watchful", "tired"], "C",
  "Alert = watchful, quick to notice danger",
  "A guard who stays 'alert' keeps watch and notices anything unusual. The closest word is 'watchful'.",
  ["'alert' = fully aware and ready", "Closest: 'watchful'"],
  "'Sleepy', 'careless' and 'tired' are close to the opposite of 'alert'.", 20)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The new rules will **curtail** the powers of loan recovery agents.",
  ["extend", "explain", "transfer", "restrict"], "D",
  "Curtail = reduce, restrict",
  "To 'curtail' powers is to cut them back or limit them. The closest word is 'restrict'.",
  ["'curtail' = cut short, reduce", "Closest: 'restrict'"],
  "'Extend' is the opposite. 'Explain' and 'transfer' powers do not mean reduce them.", 25)

Q(SY, "Contextual synonym", A,
  SY_STEM + "The government announced measures to **ameliorate** the condition of debt-ridden weavers.",
  ["improve", "worsen", "examine", "publicise"], "A",
  "Ameliorate = make a bad situation better",
  "Measures for debt-ridden weavers are meant to make their condition better. 'Ameliorate' means improve.",
  ["Context: help for people in difficulty", "'ameliorate' = make better", "Closest: 'improve'"],
  "'Worsen' is the opposite. 'Examine' and 'publicise' describe actions that do not themselves make the condition "
  "better.", 25)

Q(SY, "Contextual synonym", A,
  SY_STEM + "The annual report seemed designed to **obfuscate** the true extent of the bank's losses.",
  ["clarify", "exaggerate", "celebrate", "obscure"], "D",
  "Obfuscate = make unclear or hard to understand",
  "A report 'designed to obfuscate' the losses makes their true size hard to see. 'Obfuscate' means obscure or "
  "confuse.",
  ["Context: hiding the true extent of losses", "'obfuscate' = make unclear", "Closest: 'obscure'"],
  "'Clarify' is the opposite. 'Exaggerate' would make the losses look bigger, not unclear. 'Celebrate' does not fit "
  "losses.", 30)

Q(SY, "Contextual synonym", A,
  SY_STEM + "An **inveterate** gambler, he lost all his savings within a year of retiring.",
  ["occasional", "reformed", "reluctant", "habitual"], "D",
  "Inveterate = having a long-established habit that is unlikely to change",
  "An 'inveterate' gambler gambles by long habit, which explains why he lost all his savings. The closest word is "
  "'habitual'.",
  ["Context: lost everything through gambling", "'inveterate' = firmly established by habit",
   "Closest: 'habitual'"],
  "'Occasional' and 'reluctant' suggest he rarely or unwillingly gambled. 'Reformed' means he had given it up.", 30)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The museum displays **ancient** coins found in the region.",
  ["old", "antique", "modern", "historic"], "C",
  "Ancient = belonging to the distant past; antonym: modern",
  "'Ancient' coins come from the distant past. The opposite is 'modern', belonging to the present time.",
  ["'ancient' = very old", "Opposite = of the present: 'modern'"],
  "'Old', 'antique' and 'historic' are all close in meaning to 'ancient'.", 20)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The **benevolent** landlord waived the rent for the flood-hit tenants.",
  ["kind", "generous", "charitable", "malevolent"], "D",
  "Benevolent = kind and well-meaning; antonym: malevolent",
  "A 'benevolent' landlord wishes others well, as waiving the rent shows. The opposite is 'malevolent', wishing harm "
  "to others.",
  ["'benevolent' = well-wishing, kind", "Opposite = wishing harm: 'malevolent'"],
  "'Kind', 'generous' and 'charitable' are all close in meaning to 'benevolent'.", 25)

Q(AN, "Contextual antonym", A,
  AN_STEM + "The **acrimonious** meeting between the union and the management ended without any agreement.",
  ["amicable", "bitter", "hostile", "rancorous"], "A",
  "Acrimonious = angry and bitter; antonym: amicable",
  "An 'acrimonious' meeting is full of bitterness and anger. The opposite is 'amicable', friendly and peaceful.",
  ["'acrimonious' = bitter, angry", "Opposite = friendly: 'amicable'"],
  "'Bitter', 'hostile' and 'rancorous' are all close in meaning to 'acrimonious'.", 25)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"

Q(ID, "Meaning of idiom", B,
  "Choose the meaning of the idiom 'once in a blue moon'.",
  ["very often", "very rarely", "at midnight", "on festival days"], "B",
  "Idiom: once in a blue moon = very rarely",
  "A 'blue moon' is a rare event, so something that happens 'once in a blue moon' happens very rarely. For example: "
  "'He visits the branch once in a blue moon.'",
  ["Image: a rare sight", "Meaning: very rarely"],
  "'Very often' is the opposite. 'At midnight' and 'on festival days' take the image of the moon literally.", 20)

Q(ID, "Meaning of idiom", B,
  "Choose the meaning of the idiom 'to let the cat out of the bag'.",
  ["to reveal a secret, often by mistake", "to set someone free", "to create confusion", "to escape from danger"],
  "A",
  "Idiom: let the cat out of the bag = reveal a secret",
  "To 'let the cat out of the bag' is to reveal something that was meant to be kept secret, often carelessly. For "
  "example: 'He let the cat out of the bag about the surprise party.'",
  ["Something hidden is let out", "Meaning: reveal a secret"],
  "B, C and D take the image of releasing a cat literally or loosely and miss the idea of a secret.", 20)

Q(ID, "Idiom in context", B,
  "Choose the meaning of the idiom in bold.\n"
  "For Meena, who had worked in a bank for ten years, the clerical exam was **a piece of cake**.",
  ["a reward", "a small portion", "very easy", "very tiring"], "C",
  "Idiom: a piece of cake = something very easy",
  "With ten years of bank experience, Meena found the clerical exam very easy: 'a piece of cake'.",
  ["Context: long experience → the exam is easy", "Idiom: something very easy"],
  "'A reward' and 'a small portion' take the words literally. 'Very tiring' contradicts the idea that her experience "
  "made it easy.", 20)

Q(ID, "Idiom in context", B,
  "Choose the meaning of the idiom in bold.\n"
  "When the trainee said that the branch's real problem was poor planning, not a lack of staff, she **hit the nail on "
  "the head**.",
  ["made a careless remark", "hurt someone's feelings", "worked very hard", "described the problem exactly"], "D",
  "Idiom: hit the nail on the head = say exactly the right thing",
  "The trainee identified the real cause of the problem precisely. To 'hit the nail on the head' is to describe "
  "something exactly right.",
  ["Context: identifying the real problem", "Idiom: be exactly right"],
  "'A careless remark' is the opposite. 'Hurt someone's feelings' and 'worked very hard' do not fit naming the real "
  "cause of a problem.", 25)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "After the regulator rejected its proposal, the bank had to **go back to the drawing board**.",
  ["start planning again from the beginning", "hire a new architect", "appeal against the decision",
   "give up the idea for ever"], "A",
  "Idiom: go back to the drawing board = start again after a plan has failed",
  "Once its proposal was rejected, the bank had to prepare a new plan from the start.",
  ["Context: a plan rejected", "Idiom: begin planning again"],
  "'Hire a new architect' takes the image literally. 'Appeal against the decision' and 'give up the idea for ever' "
  "are different responses that the idiom does not express.", 25)

Q(ID, "Meaning of idiom", I,
  "Choose the meaning of the idiom 'a red herring'.",
  ["an embarrassing mistake", "a costly gift", "something that distracts attention from the real issue",
   "a sign of danger"], "C",
  "Idiom: a red herring = a misleading clue or a distraction",
  "A 'red herring' is something that draws attention away from the real issue. For example: 'The complaint about "
  "the parking fee was a red herring; the real dispute was over pay.'",
  ["Meaning: a distraction or false lead"],
  "A links 'red' with embarrassment and D with danger; B has no link with the idiom. None captures the idea of a "
  "distraction.", 25)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", B,
  OW_STEM + "A person who does not believe that God exists",
  ["agnostic", "pilgrim", "heretic", "atheist"], "D",
  "One-word substitution: beliefs",
  "An 'atheist' is a person who does not believe that God exists.",
  ["Key idea: denies that God exists", "Word: atheist"],
  "An 'agnostic' holds that it cannot be known whether God exists. A 'pilgrim' travels to a holy place. A 'heretic' "
  "holds beliefs contrary to accepted religious teaching.", 20)

Q(OW, "Single word for a phrase", I,
  OW_STEM + "A list of the books and articles referred to in a piece of writing",
  ["biography", "anthology", "bibliography", "glossary"], "C",
  "One-word substitution: books and writing",
  "A 'bibliography' lists the books and articles a writer has used or referred to.",
  ["Key ideas: list + books referred to", "Word: bibliography"],
  "A 'biography' is an account of a person's life. An 'anthology' is a collection of writings by different authors. "
  "A 'glossary' is a list of difficult words with their meanings.", 25)

Q(OW, "Single word for a phrase", I,
  OW_STEM + "A formal written request, usually signed by many people, appealing to an authority for some action",
  ["petition", "manifesto", "affidavit", "ultimatum"], "A",
  "One-word substitution: formal documents",
  "A 'petition' is a formal written request, typically signed by many people, asking an authority to act.",
  ["Key ideas: written request + many signatures + to an authority", "Word: petition"],
  "A 'manifesto' is a public statement of a party's aims. An 'affidavit' is a written statement sworn on oath by one "
  "person. An 'ultimatum' is a final demand backed by a threat.", 25)

Q(OW, "Single word for a phrase", A,
  OW_STEM + "A person who has an excessive interest in or admiration of himself or herself",
  ["misanthrope", "altruist", "egalitarian", "narcissist"], "D",
  "One-word substitution: personality types",
  "A 'narcissist' is excessively absorbed in and admiring of himself or herself, after Narcissus, who fell in love "
  "with his own reflection.",
  ["Key idea: excessive self-admiration", "Word: narcissist"],
  "A 'misanthrope' dislikes people in general. An 'altruist' puts others' welfare first. An 'egalitarian' believes "
  "all people are equal.", 25)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", I, AP_STEM + "Please submit the form at counter 3.",
  ["The form is requested to be submitted at counter 3.", "You are requested to submit the form at counter 3.",
   "The form is submitted by you at counter 3, please.", "You were requested to submit the form at counter 3."],
  "B",
  "Passive of a polite request: 'Please + verb' → 'You are requested to + verb'",
  "A request beginning with 'Please' is turned into the passive with 'You are requested to ...': 'You are requested "
  "to submit the form at counter 3.' The present tense keeps the request current.",
  ["'Please' signals a request", "Passive form: You are requested to + base verb", "Present tense: 'are requested'"],
  "A makes the form the thing that is requested, which is illogical. C turns the request into a statement of fact. D "
  "changes the tense to the past.", 30)

Q(AP, "Voice conversion", A, AP_STEM + "The manager wants someone to check these files.",
  ["The manager wants these files to check.", "These files are wanted to check by the manager.",
   "The manager wants these files to be checked.", "The manager is wanted to have these files checked."], "C",
  "Passive infinitive after 'want': want + object + to be + past participle",
  "Only the infinitive clause is passive: 'someone to check these files' becomes 'these files to be checked'. The "
  "indefinite agent 'someone' is dropped. 'The manager wants' stays active.",
  ["Main verb 'wants' stays active", "'someone to check these files' → 'these files to be checked'",
   "Drop the indefinite agent"],
  "A keeps the active infinitive 'to check', which wrongly suggests the files will do the checking. B makes the files "
  "the object of 'want' and garbles the infinitive. D makes the manager the one who is wanted.", 40)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", B, DS_STEM + "He said, \"I will come here tomorrow.\"",
  ["He said that he will come here tomorrow.", "He said that he would come there the next day.",
   "He said that I would come there the next day.", "He said that he will come there the next day."], "B",
  "Reported statement: backshift (will → would), pronoun change and change of place and time words",
  "With a past reporting verb, 'will' becomes 'would', 'I' becomes 'he', 'here' becomes 'there' and 'tomorrow' "
  "becomes 'the next day': 'He said that he would come there the next day.'",
  ["'I' → 'he'", "'will' → 'would'", "'here' → 'there'; 'tomorrow' → 'the next day'"],
  "A changes neither the tense nor the place and time words. C keeps 'I'. D keeps 'will'.", 30)

Q(DS, "Narration change", A,
  DS_STEM + "The old man said to me, \"Please help me cross the road; my eyesight is poor.\"",
  ["The old man said me to help him cross the road as his eyesight is poor.",
   "The old man requested me that please help him cross the road because my eyesight was poor.",
   "The old man told me to please help me cross the road as his eyesight had been poor.",
   "The old man requested me to help him cross the road as his eyesight was poor."], "D",
  "Mixed sentence (request + statement): 'requested + object + to-infinitive', then a linking word and backshift",
  "The request ('Please help me') becomes 'requested me to help him'; 'please' is dropped. The statement ('my "
  "eyesight is poor') is joined with 'as' and backshifted: 'as his eyesight was poor'.",
  ["Request: 'said to me, \"Please ...\"' → 'requested me to ...'", "'me' (speaker) → 'him'",
   "Statement joined with 'as': 'is' → 'was'; 'my' → 'his'"],
  "A uses 'said me' and keeps 'is'. B keeps 'please' after 'that' and does not change 'my'. C keeps 'please', uses "
  "'me' for the old man and wrongly changes 'is' to 'had been'.", 45)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", B, SV_STEM + "Everyone in the branch ______ about the new working hours.",
  ["know", "are knowing", "have known", "knows"], "D",
  "Indefinite pronouns (everyone, everybody, someone, nobody) take a singular verb",
  "'Everyone' refers to all the people but is grammatically singular, so it takes a singular verb: 'Everyone in the "
  "branch knows about the new working hours.'",
  ["Subject: 'Everyone' (singular)", "'in the branch' does not change the number", "Singular present: 'knows'"],
  "'Know' and 'have known' are plural forms. 'Are knowing' is plural and also uses the stative verb 'know' in the "
  "continuous form.", 20)

Q(SV, "Agreement rules", I,
  SV_STEM + "'The Arabian Nights' ______ a collection of tales that has been translated into many languages.",
  ["are", "were", "is", "have been"], "C",
  "The title of a single work takes a singular verb, even if the title is plural in form",
  "'The Arabian Nights' is the name of one book, so it takes a singular verb: \"'The Arabian Nights' is a collection "
  "of tales.\" The singular 'a collection' and 'has been translated' confirm this.",
  ["Subject: the title of one book", "One work → singular verb", "Present: 'is'"],
  "'Are', 'were' and 'have been' are plural forms that treat the title as several nights.", 30)

Q(SV, "Agreement rules", I,
  SV_STEM + "The secretary and treasurer of the cooperative society, Mr Rao, ______ submitted the annual accounts.",
  ["has", "have", "are", "were"], "A",
  "Two titles joined by 'and' with one article refer to one person and take a singular verb",
  "'The secretary and treasurer' has one article, so it names one person who holds both posts; the name 'Mr Rao' "
  "confirms this. A single person takes a singular verb: 'has submitted'.",
  ["One article ('The') before both titles → one person", "Confirmed by 'Mr Rao'",
   "Singular present perfect: 'has submitted'"],
  "'Have' treats the subject as two people. 'Are submitted' and 'were submitted' are plural passive forms that would "
  "make Mr Rao the thing submitted.", 30)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Sequence of tenses", B,
  TE_STEM + "Mr Iyer usually ______ to the branch by bus, but today he has come by car.",
  ["is going", "has gone", "went", "goes"], "D",
  "Simple present for a habit ('usually')",
  "'Usually' describes a regular habit, which takes the simple present: 'Mr Iyer usually goes to the branch by bus.' "
  "The 'but today' clause contrasts today with the habit.",
  ["Time word: 'usually' (habit)", "Habit → simple present", "Third person singular: 'goes'"],
  "'Is going' describes something happening now, not a habit. 'Has gone' and 'went' do not express a regular habit "
  "with 'usually'.", 25)

Q(TE, "Sequence of tenses", I,
  TE_STEM + "We ______ the new branch next Monday; the invitations have already been sent.",
  ["are opening", "opened", "had opened", "have opened"], "A",
  "Present continuous for a future arrangement that has already been fixed",
  "An event planned for 'next Monday', with invitations already sent, is a fixed arrangement. The present continuous "
  "expresses such arrangements: 'We are opening the new branch next Monday.'",
  ["Time: 'next Monday' (future)", "Arrangement already made (invitations sent)", "Present continuous: 'are opening'"],
  "'Opened', 'had opened' and 'have opened' are past or perfect forms that clash with 'next Monday'.", 30)

Q(TE, "Sequence of tenses", I,
  TE_STEM + "Please don't call me at nine tomorrow morning; I ______ the branch's cash with the auditors then.",
  ["have checked", "had been checking", "will be checking", "checked"], "C",
  "Future continuous for an action that will be in progress at a definite future time",
  "At nine tomorrow morning the checking will be going on. An action in progress at a future moment takes the future "
  "continuous: 'I will be checking the branch's cash then.'",
  ["Time: 'at nine tomorrow morning ... then' (a future moment)", "Action in progress at that moment",
   "Future continuous: 'will be checking'"],
  "'Have checked', 'had been checking' and 'checked' are present-perfect or past forms that clash with 'tomorrow'.",
  30)

Q(TE, "Perfect tenses", A,
  TE_STEM + "I ______ to visit the branch yesterday, but a sudden meeting kept me at the office.",
  ["have intended", "had intended", "intend", "will intend"], "B",
  "Past perfect of verbs like 'intend', 'hope', 'mean' and 'plan' for an intention that was not carried out",
  "The intention existed before the meeting got in the way, and it was not fulfilled. 'Had intended' expresses an "
  "earlier plan that did not happen: 'I had intended to visit the branch yesterday, but ...'.",
  ["Time: 'yesterday' (past)", "The plan existed before the meeting and failed",
   "Unfulfilled past intention: 'had intended'"],
  "'Have intended' (present perfect) cannot be used with 'yesterday'. 'Intend' and 'will intend' are present and "
  "future forms that clash with the past time.", 35)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", I,
  AR_STEM + "______ Mount Everest lies in ______ Himalayas.",
  ["The, the", "No article, the", "The, no article", "No article, no article"], "B",
  "No article before names of single mountains; 'the' before mountain ranges",
  "Names of individual peaks take no article ('Mount Everest', 'Kanchenjunga'). Mountain ranges, which are plural "
  "names, take 'the' ('the Himalayas', 'the Alps').",
  ["Blank 1: a single peak → no article", "Blank 2: a mountain range → 'the'", "Option B"],
  "A puts 'the' before a single peak. C drops 'the' before the range. D drops it as well.", 25)

Q(AR, "Definite and indefinite", A,
  AR_STEM + "She plays ______ violin in the evenings and teaches ______ music at a school on weekdays.",
  ["the, the", "a, the", "the, no article", "no article, the"], "C",
  "'The' with musical instruments after 'play'; no article with uncountable subjects in general (music, history)",
  "We 'play the violin' (an instrument in general). 'Music' as a subject in general is an uncountable noun and takes "
  "no article: 'teaches music'.",
  ["Blank 1: play + instrument → 'the violin'", "Blank 2: music as a subject in general → no article",
   "Option C"],
  "A and B put 'the' before 'music' in its general sense. B also uses 'a violin', and D drops 'the' before the "
  "instrument.", 30)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", B, PP_STEM + "Several clerks were absent ______ the meeting because of the strike.",
  ["in", "at", "from", "of"], "C",
  "Fixed preposition: 'absent from'",
  "The adjective 'absent' takes 'from': 'Several clerks were absent from the meeting.'",
  ["Pattern: be absent from + place or event"],
  "'Absent in', 'absent at' and 'absent of' are not the standard pattern.", 20)

Q(PP, "Fixed prepositions", I,
  PP_STEM + "The revised service charges apply ______ all savings accounts opened after 1 April.",
  ["on", "for", "with", "to"], "D",
  "Fixed preposition: a rule 'applies to' the people or things it covers",
  "When a rule or charge covers something, it 'applies to' it: 'The revised charges apply to all savings accounts.' "
  "('Apply for' means make a formal request, as in 'apply for a loan'.)",
  ["Meaning: the charges cover these accounts", "Pattern: apply to + what is covered", "'apply to'"],
  "'Apply on' and 'apply with' are not standard here. 'Apply for' means request something, which accounts cannot "
  "do.", 25)

Q(PP, "Phrasal verbs", A,
  PP_STEM + "When the shop stayed closed for months during the floods, the family had to ______ its small savings.",
  ["fall back on", "fall out with", "fall in with", "fall through"], "A",
  "Phrasal verb: fall back on = use something kept in reserve when other things fail",
  "With no income from the shop, the family had to use its savings as a reserve. To 'fall back on' something is to "
  "rely on it when other resources fail.",
  ["Context: income stopped", "Meaning needed: rely on a reserve", "'fall back on'"],
  "'Fall out with' means quarrel with. 'Fall in with' means agree to or join. 'Fall through' means fail to happen and "
  "takes no object.", 30)

Q(PP, "Fixed prepositions", A,
  PP_STEM + "Ignoring the auditor's repeated warnings was tantamount ______ inviting a fraud.",
  ["to", "with", "for", "as"], "A",
  "Fixed preposition: 'tantamount to' = equivalent in effect to",
  "The adjective 'tantamount' takes 'to': 'Ignoring the warnings was tantamount to inviting a fraud.'",
  ["Adjective: 'tantamount' (= as good as)", "Fixed pairing: 'tantamount to'"],
  "'Tantamount with', 'tantamount for' and 'tantamount as' are not standard.", 25)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"

Q(CN, "Sentence connectors", B,
  "Choose the connector that best fills the blank.\n"
  "He saved a part of his salary every month ______ he could buy a bicycle for his son.",
  ["although", "unless", "so that", "because of"], "C",
  "'So that' introduces a purpose",
  "Buying a bicycle is the purpose of saving every month. 'So that' introduces a purpose clause.",
  ["Clause 1: saving every month", "Clause 2: buying a bicycle (the aim)", "Purpose → 'so that'"],
  "'Although' signals contrast and 'unless' a condition. 'Because of' must be followed by a noun, not a clause.", 25)

Q(CN, "Sentence connectors", I,
  "Choose the connector that best fills the blank.\n"
  "The new scheme is cheap to run. ______, it reaches families that banks have long ignored.",
  ["Nevertheless", "Moreover", "Instead", "Otherwise"], "B",
  "Additive connector 'Moreover' adds a further point in the same direction",
  "Both sentences praise the scheme: it is cheap, and it also reaches neglected families. 'Moreover' adds a second "
  "point supporting the first.",
  ["Sentence 1: advantage (cheap)", "Sentence 2: another advantage (wide reach)", "Addition → 'Moreover'"],
  "'Nevertheless' signals contrast, but the two points agree. 'Instead' signals replacement. 'Otherwise' introduces "
  "what would happen if the first statement were not true.", 30)

Q(CN, "Sentence connectors", I,
  "Choose the connector that best fills the blank.\n"
  "Keep a copy of the payment receipt ______ the amount is not credited to your account.",
  ["unless", "even though", "so that", "in case"], "D",
  "'In case' = as a precaution against a possible event",
  "Keeping a copy of the receipt is a precaution: the amount might not be credited. 'In case' introduces the "
  "possible problem the precaution guards against.",
  ["Main clause: a precaution (keep a copy)", "Subordinate clause: a possible problem",
   "Precaution against a possibility → 'in case'"],
  "'Unless' would mean keep a copy only if the amount is credited, which is illogical. 'Even though' treats the "
  "failure as a fact. 'So that' would make the failure the aim.", 30)

Q(CN, "Sentence connectors", I,
  "Choose the connector that best fills the blank.\n"
  "The new manager did not reduce the staff's workload; ______, he added two new weekly reports to their duties.",
  ["on the contrary", "similarly", "as a result", "likewise"], "A",
  "'On the contrary' follows a negative statement and introduces the opposite of what was denied",
  "The first clause denies that the workload was reduced; the second says it was actually increased. 'On the "
  "contrary' introduces a statement that is the opposite of the one just denied.",
  ["Clause 1: workload not reduced (denial)", "Clause 2: workload increased (the opposite)",
   "→ 'on the contrary'"],
  "'Similarly' and 'likewise' signal a comparison between like things. 'As a result' would make the extra reports a "
  "consequence of not reducing the workload.", 30)

Q(CN, "Starters and linkers", A,
  "Combine the two sentences into one without changing the meaning, and choose the option that correctly begins the "
  "combined sentence.\n"
  "The project was well planned. It failed because the funds ran out.",
  ["Though was the project well planned,", "Well planned though the project was,",
   "Well planned despite the project was,", "As though the project was well planned,"], "B",
  "Concessive inversion: adjective/participle + 'though' (or 'as') + subject + verb",
  "'Well planned though the project was, it failed because the funds ran out' means 'Although the project was well "
  "planned, it failed ...'. The complement moves to the front, followed by 'though', the subject and the verb.",
  ["Relation: contrast (good plan, yet failure)", "Fronted form: complement + though + subject + verb",
   "'Well planned though the project was, it failed ...'"],
  "A inverts the verb after 'though', which is not allowed. C uses 'despite' before a clause. D's 'As though' means "
  "'as if', which changes the meaning.", 40)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_004_plan.json").read_text(encoding="utf-8"))
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
            assert f" {bold} " in q["question_text"].replace("'", " ").replace(",", " ").replace(".", " "), \
                (q["question_id"], bold)
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
    "batch_id": "BATCH_004",
    "created_at": TODAY,
    "notes": "BATCH_004 English Language part: 150 original questions (BANK_ENG_000454 to BANK_ENG_000603). Six "
             "reading passages (31 questions) and three cloze passages (16 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 to BATCH_003; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules, words and idioms not tested in earlier batches. "
             "Each answer was set by the author and re-solved in a separate blind pass without the key. Pending human "
             "review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_004_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))})")
