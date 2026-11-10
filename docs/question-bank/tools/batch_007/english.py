"""Writes batches/parts/BATCH_007_ENG.json: the 150 English Language questions of BATCH_007.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000 to BATCH_006, and the grammar rules, idioms and words tested are ones not tested in those batches (where
a grammar area was already covered, it is tested here through a different rule or a context-based item). Run from
anywhere:

    python docs/question-bank/tools/batch_007/english.py

Structural checks (quota per topic and difficulty, subtopics, ID range, passage length, set sizes, option count, cloze
blank numbering, 'No error' / 'No replacement' / 'No swap' placement, para-jumble option validity, RC option-length
spread, repeated stems, passage titles and passage themes against all earlier English files, answer-key balance) and
the computable answers (the loan-recovery figures in RC 6) are asserted before anything is written. Option letters are
never named in solutions (except the fixed parts A/B/C of Error Detection), and solutions never refer to an option by
its position, so the script places the correct option itself (seeded shuffle) to keep the answer keys balanced.
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
FIRST_ID = 904
FIRST_STIM = 7001
EARLIER = ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json", "parts/BATCH_002_ENG.json",
           "parts/BATCH_003_ENG.json", "parts/BATCH_004_ENG.json", "parts/BATCH_005_ENG.json",
           "parts/BATCH_006_ENG.json")

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
P1 = stim("A station for the village", (
    "In a small town on the edge of a dry district, a radio station broadcasts from two rooms above a grocery shop. "
    "Its signal reaches only about fifteen kilometres, and most of its presenters are farmers, housewives and "
    "students who had never spoken into a microphone before. This is community radio: a low-power station run by and "
    "for the people of a small area.\n\n"
    "Unlike large commercial channels, which try to attract as many listeners as possible across a city or a state, "
    "a community station serves a few villages and speaks in their own dialect. Its programmes are shaped by local "
    "needs. A typical day might include a talk by an agriculture officer on pest control, a call-in show on a new "
    "pension scheme, folk songs recorded at a wedding and the prices of vegetables at the nearest market.\n\n"
    "Supporters say that the greatest strength of such stations is trust. Listeners recognise the voices on air; the "
    "person reading out a weather warning may be a neighbour's daughter. During floods and heavy storms, when mobile "
    "networks often fail, community stations have kept villages informed about rising water levels, safe shelters "
    "and relief camps.\n\n"
    "Running a station, however, is not easy. Most are operated by schools, colleges or voluntary organisations with "
    "little money. They cannot depend on advertising, since local businesses are small and the stations are allowed "
    "to broadcast only a limited amount of it. Equipment breaks down, trained volunteers move away to cities, and "
    "licences take a long time to obtain.\n\n"
    "Many stations have survived by involving their listeners. Villagers donate small sums, women's groups produce "
    "their own programmes, and young people learn to record and edit on cheap phones. As one station manager put it, "
    "the station does not belong to its staff; it belongs to the people who keep switching it on."))

Q(RC, "Factual", B,
  "According to the passage, who are most of the presenters at the station described in the first paragraph?",
  ["Trained broadcasters hired from the nearest city",
   "Local people who had never used a microphone before",
   "Agriculture officers posted in the district",
   "Owners of the shops in the town market"], 1,
  "Locating a stated detail",
  "Paragraph 1: 'most of its presenters are farmers, housewives and students who had never spoken into a microphone "
  "before'.",
  ["Find 'presenters' in paragraph 1", "Farmers, housewives and students", "They had never spoken into a microphone"],
  "Trained broadcasters from a city are the opposite of what is described. An agriculture officer gives one talk in "
  "paragraph 2 but is not a regular presenter. The station sits above a grocery shop, but shop owners are not named "
  "as presenters.", 35, P1, 1)

Q(RC, "Factual", B,
  "How, according to the passage, does a community station differ from a large commercial channel?",
  ["It plays only music and carries no talk shows.",
   "It broadcasts across a whole state in one language.",
   "It serves a few villages and uses their own dialect.",
   "It is run by the government and needs no licence."], 2,
  "Locating a stated contrast",
  "Paragraph 2: commercial channels try to reach as many listeners as possible across a city or state, while 'a "
  "community station serves a few villages and speaks in their own dialect'.",
  ["Find 'Unlike large commercial channels' in paragraph 2", "Commercial: as many listeners as possible",
   "Community: a few villages, their own dialect"],
  "Paragraph 2 lists talks and call-in shows, so 'only music' is wrong. Broadcasting across a state describes the "
  "commercial channels. Paragraph 4 says stations are run by schools, colleges and voluntary groups and that licences "
  "take time to obtain.", 40, P1, 2)

Q(RC, "Factual", B,
  "Why, according to the passage, have community stations been especially useful during floods and storms?",
  ["They kept villages informed when mobile networks failed.",
   "They raised money to rebuild houses after the floods.",
   "They sent their volunteers to rescue stranded families.",
   "They moved their studios to the relief camps."], 0,
  "Locating a stated reason",
  "Paragraph 3: 'During floods and heavy storms, when mobile networks often fail, community stations have kept "
  "villages informed about rising water levels, safe shelters and relief camps.'",
  ["Find 'floods' in paragraph 3", "Mobile networks often fail", "Stations kept villages informed"],
  "Raising money, rescuing families and moving studios are never mentioned. The passage says the stations gave "
  "information, not that they did relief work.", 35, P1, 3)

Q(RC, "Factual", B,
  "Which of the following is NOT mentioned in the passage as a difficulty in running a community station?",
  ["Most stations have very little money.",
   "Trained volunteers move away to cities.",
   "Programmes in local dialects are not permitted.",
   "Only a limited amount of advertising is allowed."], 2,
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 4 lists little money, limited advertising, equipment that breaks down, volunteers who move away and "
  "slow licences. Far from being forbidden, local dialects are a feature of these stations (paragraph 2).",
  ["Little money: stated", "Volunteers move away: stated", "Limited advertising: stated",
   "Dialects forbidden: contradicted by paragraph 2"],
  "Little money, volunteers leaving and the limit on advertising are all stated in paragraph 4, so none of them can "
  "be the answer.", 45, P1, 4)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'shaped' as used in the passage ('Its programmes are "
  "shaped by local needs')?",
  ["influenced", "shortened", "hidden", "repeated"], 0,
  "Vocabulary in context: shaped by = formed or decided by",
  "The next sentence lists programmes chosen for local people: pest control, a pension scheme, local songs and "
  "market prices. Local needs decide what is broadcast, so 'shaped' means influenced or determined.",
  ["Context: the programmes listed all answer local needs", "Local needs decide the content", "'influenced'"],
  "'Shortened', 'hidden' and 'repeated' say nothing about local needs deciding what goes on air.", 30, P1, 5)

Q(RC, "Tone and title", B,
  "Which of the following is the most suitable title for the passage?",
  ["A Voice for the Village", "The Decline of Radio", "How to Become a Radio Star", "Advertising in Small Towns"], 0,
  "Title: the idea that runs through every paragraph",
  "Every paragraph is about small stations run by and for local people: what they are, what they broadcast, why "
  "villagers trust them, their difficulties and how listeners keep them going.",
  ["Paras 1-2: local stations for local people", "Paras 3-4: trust and difficulties",
   "Para 5: the station belongs to its listeners"],
  "The passage does not say radio is declining. Becoming a star is never discussed. Advertising appears in a single "
  "sentence as one difficulty, so it is too narrow for a title.", 35, P1, 6)

# ---------------------------------------------------------------- RC 2 (Basic 3 + Intermediate 3)
P2 = stim("Driving blind in the fog", (
    "Every winter, large parts of northern India disappear under a thick blanket of fog. For railway passengers, the "
    "season brings a familiar frustration: trains that run hours, sometimes a whole day, behind schedule. Passengers "
    "often blame poor planning, but the main cause is simple. A driver who cannot see the signal ahead cannot safely "
    "run his train at full speed.\n\n"
    "Railway signals work much like traffic lights. A red light tells the driver to stop, while yellow and green "
    "lights tell him how much of the line ahead is clear. In good weather a driver can see a signal from a long "
    "distance and adjust his speed calmly. In dense fog, visibility may fall to a few metres, so he may not spot a "
    "red signal until it is too late. A heavy train needs a long distance to halt even after the brakes are applied. "
    "Rules therefore require trains to slow down sharply when the fog is thick.\n\n"
    "Technology has eased the problem without removing it. Many locomotives now carry a small device that uses "
    "satellite positioning to tell the driver how far away the next signal is, and sounds an alert as the train "
    "approaches it. Drivers say this removes much of the guesswork. Some routes are also being fitted with systems "
    "that can apply the brakes automatically if a train passes a red signal or goes faster than the safe speed.\n\n"
    "Even so, delays cannot be avoided entirely. One late train holds up the trains behind it on a busy line, and the "
    "effect spreads across the network. Railways therefore cancel or shorten some services in the foggiest weeks, so "
    "that the remaining trains can run closer to time.\n\n"
    "For passengers, the practical lesson is to check the running status of a train before leaving home. For the "
    "railways, the challenge is to make winter travel safe first and punctual second, in that order."))

Q(RC, "Factual", B,
  "According to the passage, what is the main reason why trains run late in thick fog?",
  ["Fog damages the electric lines that run the trains.",
   "Drivers cannot see signals, so trains must slow down.",
   "Passengers take longer to board in the cold weather.",
   "Railway staff are on leave during the winter season."], 1,
  "Locating a stated cause",
  "Paragraph 1: 'A driver who cannot see the signal ahead cannot safely run his train at full speed.' Paragraph 2 "
  "adds that rules require trains to slow down sharply in thick fog.",
  ["Find 'the main cause' in paragraph 1", "Driver cannot see the signal ahead", "So trains slow down"],
  "Damaged lines, slow boarding and staff on leave are never mentioned. The passage also rejects 'poor planning' as "
  "the main cause.", 35, P2, 1)

Q(RC, "Factual", B,
  "Why, according to the passage, is it dangerous for a driver to spot a red signal late?",
  ["The signal may change back to green at any moment.",
   "A heavy train needs a long distance to stop after braking.",
   "Other drivers cannot see his train's headlights.",
   "The brakes of most trains do not work in cold weather."], 1,
  "Locating a stated reason",
  "Paragraph 2: a driver 'may not spot a red signal until it is too late. A heavy train needs a long distance to "
  "halt even after the brakes are applied.'",
  ["Find 'too late' in paragraph 2", "Next sentence gives the reason", "Long stopping distance"],
  "Signals changing back, headlights and brakes failing in the cold are never mentioned in the passage.",
  35, P2, 2)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'eased' as used in the passage ('Technology has eased "
  "the problem without removing it')?",
  ["solved", "reduced", "created", "hidden"], 1,
  "Vocabulary in context: ease a problem = make it less severe",
  "The words 'without removing it' show that the problem still exists but is smaller. To ease a problem is to make "
  "it less serious: to reduce it.",
  ["Clue: 'without removing it'", "The problem remains but is smaller", "'reduced'"],
  "'Solved' contradicts 'without removing it'. 'Created' is the opposite of what the device does. 'Hidden' does not "
  "describe making a problem smaller.", 30, P2, 3)

Q(RC, "Inference", I,
  "Why do railways cancel or shorten some services in the foggiest weeks?",
  ["Running fewer trains means delays spread less, so the rest run closer to time.",
   "Passengers do not wish to travel during the coldest weeks of the winter.",
   "Satellite devices cannot be fitted to all the locomotives in time for winter.",
   "Shorter routes are cheaper to run when ticket sales fall in bad weather."], 0,
  "Inference: linking a stated action to the cause given just before it",
  "Paragraph 4 explains that one late train holds up the trains behind it and the effect spreads. Running fewer "
  "trains reduces this knock-on effect, 'so that the remaining trains can run closer to time'.",
  ["Problem: one late train delays those behind it", "Fewer trains = less knock-on delay",
   "Purpose stated: remaining trains run closer to time"],
  "Passengers' wishes, a shortage of devices and falling ticket sales are not given as reasons; the passage links the "
  "cuts only to the spread of delays.", 45, P2, 4)

Q(RC, "Inference", I,
  "What does the last sentence of the passage ('safe first and punctual second, in that order') imply?",
  ["Punctuality matters more to passengers than safety does.",
   "Trains should be cancelled whenever there is any fog.",
   "Delays are acceptable if they are needed to keep trains safe.",
   "Safety devices have already made fog delays a thing of the past."], 2,
  "Inference: the meaning of an order of priorities",
  "Putting safety first and punctuality second 'in that order' means that when the two clash, safety wins: trains "
  "may run late so that they run safely.",
  ["Two goals: safety and punctuality", "'In that order': safety comes first",
   "So some delay is acceptable for safety"],
  "'Punctuality matters more' reverses the order. Cancelling trains whenever there is any fog goes far beyond the "
  "passage. Paragraph 4 says delays cannot be avoided entirely, so they are not a thing of the past.",
  45, P2, 5)

Q(RC, "Tone and title", I,
  "Which of the following best describes the tone of the passage?",
  ["angry and accusing", "explanatory and practical", "humorous and light-hearted", "gloomy and hopeless"], 1,
  "Tone: how the author treats the subject",
  "The author explains how signals work, why fog slows trains and what technology does, and ends with practical "
  "advice for passengers. The writing is calm and informative.",
  ["Explains causes (signals, stopping distance)", "Describes solutions and their limits",
   "Ends with practical advice"],
  "The author defends the railways against the charge of poor planning, so the tone is not accusing. There are no "
  "jokes. Describing devices that remove much of the guesswork is not hopeless.", 35, P2, 6)

# ---------------------------------------------------------------- RC 3 (Intermediate, 6)
P3 = stim("Money that crosses borders", (
    "Every month, millions of Indians working abroad, in the Gulf, in Europe, in North America and elsewhere, send "
    "part of their earnings home. These transfers, known as remittances, have made India the largest recipient of "
    "such money in the world. For many families, the monthly transfer from a son or a husband abroad pays for food, "
    "school fees and medical bills, and over the years it has built houses, shops and small businesses.\n\n"
    "Economists value remittances for reasons that go beyond the family budget. Unlike foreign investment, which may "
    "leave a country quickly when conditions turn bad, remittances tend to be steady, and they often rise when the "
    "home country faces a disaster, because workers abroad send more to help relatives in trouble. They also bring in "
    "foreign currency without creating any debt that must later be repaid.\n\n"
    "The benefits, however, come with costs. Sending small sums across borders has long been expensive: once fees and "
    "the margin on the exchange rate are added, a worker may lose a noticeable share of what he sends. Many migrants "
    "also borrow heavily to pay recruitment agents before they leave, and spend their first years abroad simply "
    "clearing that debt. At home, families that depend on a single overseas earner are exposed if he loses his job or "
    "falls ill.\n\n"
    "Some researchers worry about a subtler effect. Where remittances are large, they argue, young people may come to "
    "see migration as the only route to a good life, and invest little effort in local work or study. Others reply "
    "that the money often pays for the education that makes the next generation more productive.\n\n"
    "Policy has focused on making transfers cheaper and safer. Digital channels have cut fees, and banks have been "
    "encouraged to offer accounts and investment products tailored to migrants and their families. The larger "
    "challenge is to turn money that is spent mainly on daily needs into savings and investment that can outlast the "
    "worker's years abroad."))

Q(RC, "Factual", I,
  "Why, according to the passage, are remittances considered more dependable than foreign investment?",
  ["They are steady and often rise when the home country faces a disaster.",
   "They are guaranteed by the governments of the countries that send them.",
   "They are always spent on houses and businesses rather than daily needs.",
   "They are sent through banks, which cannot move money out of the country."], 0,
  "Locating a stated contrast",
  "Paragraph 2: foreign investment 'may leave a country quickly when conditions turn bad', whereas remittances 'tend "
  "to be steady, and they often rise when the home country faces a disaster'.",
  ["Find 'Unlike foreign investment' in paragraph 2", "Investment may leave quickly",
   "Remittances: steady, often rise in a disaster"],
  "No guarantee by foreign governments is mentioned. The last paragraph says remittances are spent mainly on daily "
  "needs, which contradicts 'always spent on houses'. Banks being unable to move money is never stated.",
  45, P3, 1)

Q(RC, "Factual", I,
  "Which of the following is NOT mentioned in the passage as a cost or risk linked to remittances?",
  ["Fees and exchange-rate margins on small transfers",
   "Debts taken to pay recruitment agents before leaving",
   "Families depending on a single overseas earner",
   "A stronger rupee that hurts the country's exporters"], 3,
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 3 lists fees and exchange margins, debts to recruitment agents and the exposure of families relying on "
  "one earner. The effect of remittances on the rupee or on exporters is never discussed.",
  ["Fees and margins: stated", "Recruitment debts: stated", "Single earner: stated",
   "Stronger rupee and exporters: not in the passage"],
  "Fees, recruitment debts and dependence on one earner are all stated in paragraph 3, so none of them can be the "
  "answer.", 45, P3, 2)

Q(RC, "Inference", I,
  "What does the phrase 'without creating any debt that must later be repaid' suggest about some other sources of "
  "foreign currency?",
  ["They are not allowed to enter the country at all.",
   "They come as loans that the country must pay back.",
   "They are always smaller than the money migrants send.",
   "They are spent only by the government, not by families."], 1,
  "Inference: what a contrast implies about the thing it is contrasted with",
  "Praising remittances for bringing in foreign currency 'without creating any debt' implies that other ways of "
  "getting foreign currency, such as borrowing abroad, do create debt that must be repaid.",
  ["Remittances: currency with no debt", "The contrast implies others bring debt", "Other sources = loans to repay"],
  "Nothing suggests other sources are banned, always smaller, or used only by the government; the phrase is about "
  "debt, not size or who spends the money.", 45, P3, 3)

Q(RC, "Inference", I,
  "On which point do the researchers mentioned in paragraph 4 disagree?",
  ["Whether remittances discourage effort or fund a more productive next generation",
   "Whether migrants should pay recruitment agents before they leave the country",
   "Whether digital channels have really cut the fees charged on transfers",
   "Whether young people should study abroad or in their home towns"], 0,
  "Inference: identifying the issue in a two-sided debate",
  "One group argues that large remittances may lead young people to invest little effort in local work or study; "
  "the other replies that the money often pays for education that makes the next generation more productive. The "
  "dispute is about the effect of remittances on young people's effort and productivity.",
  ["View 1: remittances weaken effort at home", "View 2: remittances pay for education",
   "Issue: effect on the next generation's productivity"],
  "Recruitment agents and digital fees appear in other paragraphs and are not debated. Studying abroad versus at "
  "home is not what either side discusses.", 50, P3, 4)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'tailored' as used in the passage ('accounts and "
  "investment products tailored to migrants and their families')?",
  ["stitched", "designed to suit", "sold cheaply", "restricted"], 1,
  "Vocabulary in context: tailored to = made to fit particular needs",
  "Banks are encouraged to offer products made for the particular needs of migrants. Like clothes cut to fit one "
  "person, the products are designed to suit them.",
  ["Context: banks offering products for a group", "Made to fit that group's needs", "'designed to suit'"],
  "'Stitched' is the literal tailor's sense and does not apply to accounts. 'Sold cheaply' and 'restricted' are not "
  "meanings of 'tailored'.", 35, P3, 5)

Q(RC, "Tone and title", I,
  "Which of the following best states the main idea of the passage?",
  ["Remittances do more harm than good and should be discouraged.",
   "Remittances help families and the economy but carry costs and need better use.",
   "Recruitment agents are the main reason why Indians go abroad to work.",
   "Digital channels have solved every problem linked to sending money home."], 1,
  "Main idea: balance the benefits, the costs and the conclusion",
  "The passage describes the benefits (family income, steady foreign currency), the costs (fees, debts, dependence), "
  "a debate, and ends by calling for cheaper transfers and for turning the money into lasting savings.",
  ["Paras 1-2: benefits", "Paras 3-4: costs and a debate", "Para 5: cheaper transfers, better use of the money"],
  "The passage never calls for remittances to be discouraged. Recruitment agents are one cost among several. The "
  "last paragraph says a 'larger challenge' remains, so not every problem is solved.", 45, P3, 6)

# ---------------------------------------------------------------- RC 4 (Intermediate, 6)
P4 = stim("Pooling the milk", (
    "Twice a day, in thousands of Indian villages, a small queue forms outside a room with a tin roof. Farmers, many "
    "of them women, arrive carrying steel cans of milk from one or two buffaloes or cows. Each can is weighed, a "
    "small sample is tested for fat content, and within minutes the farmer receives a slip showing what she will be "
    "paid. This is the village collection centre of a dairy cooperative, and it is the first link in a chain that "
    "ends in packets of milk, butter and cheese on shop shelves hundreds of kilometres away.\n\n"
    "Before cooperatives spread, a small producer had little choice but to sell to a private trader. With only a few "
    "litres to sell and no way of storing milk, which spoils within hours in the heat, she accepted whatever price "
    "the trader offered. Traders often paid late, cheated on measurement, or lent money on terms that tied the farmer "
    "to them for years.\n\n"
    "The cooperative changed the balance of power by pooling the milk of many small producers. Together they could "
    "afford chilling plants, trucks and processing units, and could sell in distant cities where prices were higher. "
    "Because the members owned the organisation, its surplus returned to them, often as a bonus at the end of the "
    "year. Testing every sample also meant that the price depended on quality rather than on the trader's mood, so "
    "farmers had a reason to feed and care for their animals better.\n\n"
    "The model is not free of problems. In some places, cooperatives have been captured by local politicians who use "
    "them to reward their supporters, and elections to their boards are bitterly fought. Private dairies, which now "
    "compete for the same milk, sometimes offer higher prices in good seasons, tempting members to sell outside.\n\n"
    "Still, the basic idea has proved remarkably durable: when many small sellers act together, they can win terms "
    "that none of them could obtain alone."))

Q(RC, "Factual", I,
  "Why, according to the passage, did small producers accept whatever price a private trader offered?",
  ["They had little milk to sell and no way to stop it spoiling.",
   "The government fixed the price that traders had to pay.",
   "Traders always paid in advance for a whole year's milk.",
   "They preferred traders to the cooperative's testing system."], 0,
  "Locating a stated reason",
  "Paragraph 2: 'With only a few litres to sell and no way of storing milk, which spoils within hours in the heat, "
  "she accepted whatever price the trader offered.'",
  ["Find 'whatever price' in paragraph 2", "Reason 1: only a few litres", "Reason 2: milk spoils, no storage"],
  "A government-fixed price is never mentioned. Traders 'often paid late', the opposite of paying in advance. The "
  "cooperative did not yet exist in the period described, so farmers could not prefer traders to it.", 40, P4, 1)

Q(RC, "Factual", I,
  "According to the passage, how did testing every sample of milk benefit farmers?",
  ["It allowed them to sell their milk without weighing it.",
   "It made the price depend on quality, rewarding better care of animals.",
   "It let them keep their milk fresh for several days longer.",
   "It removed the need for chilling plants and trucks."], 1,
  "Locating a stated effect",
  "Paragraph 3: testing 'meant that the price depended on quality rather than on the trader's mood, so farmers had a "
  "reason to feed and care for their animals better'.",
  ["Find 'Testing every sample' in paragraph 3", "Price depends on quality", "Reason to care for animals better"],
  "Paragraph 1 says each can is weighed as well as tested. Testing does not keep milk fresh. Chilling plants and "
  "trucks are listed as things the pooled cooperative could afford, not things testing replaced.", 40, P4, 2)

Q(RC, "Inference", I,
  "The statement that the cooperative 'changed the balance of power' implies that earlier",
  ["farmers and traders bargained as equals",
   "traders had the stronger hand in dealing with farmers",
   "the government controlled the sale of all milk",
   "farmers refused to sell milk to anyone outside the village"], 1,
  "Inference: what a change implies about the situation before it",
  "Paragraph 2 shows traders setting prices, paying late, cheating on measurement and tying farmers to them with "
  "loans. If the cooperative changed the balance of power, power earlier lay with the traders.",
  ["Para 2: traders set prices, cheated, tied farmers down", "'Changed the balance' = shifted power",
   "Earlier, the traders were stronger"],
  "'Bargained as equals' contradicts paragraph 2. Government control and a refusal to sell outside the village are "
  "never mentioned.", 45, P4, 3)

Q(RC, "Inference", I,
  "What does the passage suggest about why elections to cooperative boards are 'bitterly fought'?",
  ["Board members must pay for the chilling plants themselves.",
   "Control of a cooperative can bring power to reward supporters.",
   "Private dairies choose the members of the boards.",
   "Only women are allowed to vote in the elections."], 1,
  "Inference: connecting two parts of the same sentence",
  "The same sentence says cooperatives have been 'captured by local politicians who use them to reward their "
  "supporters'. A board that can hand out favours is a prize worth fighting for.",
  ["Politicians capture cooperatives", "They use them to reward supporters", "So board seats are worth fighting for"],
  "Paying for plants, private dairies choosing boards and women-only voting are not in the passage; the passage links "
  "the fights only to political capture.", 45, P4, 4)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'captured' as used in the passage ('cooperatives have "
  "been captured by local politicians')?",
  ["taken control of", "arrested", "photographed", "won in a battle"], 0,
  "Vocabulary in context: capture (an organisation) = take control of it for one's own purposes",
  "The politicians 'use them to reward their supporters', which shows that they control the cooperatives. To capture "
  "an organisation here is to take control of it.",
  ["Context: politicians use cooperatives to reward supporters", "They have gained control of them",
   "'taken control of'"],
  "'Arrested' and 'photographed' are literal senses of 'capture' that cannot apply to an organisation. 'Won in a "
  "battle' suggests fighting with weapons, while the passage describes political control.", 35, P4, 5)

Q(RC, "Tone and title", I,
  "Which of the following is the most suitable title for the passage?",
  ["Strength in Numbers", "How to Test Milk for Fat", "Why Private Dairies Pay More", "The Village Trader's Story"],
  0,
  "Title: the central idea, stated in the last paragraph",
  "The passage ends: 'when many small sellers act together, they can win terms that none of them could obtain "
  "alone.' Small producers gaining strength by joining together is captured by 'Strength in Numbers'.",
  ["Para 3: pooling gives small producers power", "Para 5: acting together wins better terms",
   "'Strength in Numbers'"],
  "Testing milk is one detail. Private dairies paying more is mentioned once, and only in good seasons. The trader "
  "appears only in paragraph 2 as the problem the cooperative solved.", 40, P4, 6)

# ---------------------------------------------------------------- RC 5 (Advanced, 6)
P5 = stim("When winning means losing", (
    "Imagine a jar of coins put up for auction in a classroom. Nobody knows exactly how much money it contains, so "
    "each student makes a guess and bids accordingly. Some guesses are too low and some too high, and if the class is "
    "large, the average guess may be quite close to the true value. Yet the student who wins the auction is, almost "
    "by definition, the one whose guess was the most optimistic. Experiments of this kind repeatedly find that the "
    "winner pays more than the jar is worth.\n\n"
    "Economists call this the winner's curse. It arises whenever many bidders compete for an item whose true value is "
    "the same for all of them but uncertain to each, such as the right to drill for oil in a particular field, a "
    "licence to use a band of radio frequencies, or a company that has been put up for sale. Every bidder's estimate "
    "contains some error. Winning therefore tells a bidder something unwelcome: that everyone else valued the prize "
    "less highly, and so her own estimate was probably too high.\n\n"
    "The lesson for a careful bidder is counter-intuitive. Rather than bidding what she believes the item is worth, "
    "she should bid somewhat less, and shade her bid further as the number of rivals grows, because the more bidders "
    "there are, the more extreme the most optimistic estimate is likely to be. A bidder who ignores this may win "
    "often and still lose money.\n\n"
    "The curse is not inevitable. Experienced bidders in industries with frequent auctions learn to discount their "
    "own enthusiasm, and the designers of an auction can reduce the problem by releasing more information about the "
    "item, which narrows the spread of estimates. Where bidders are inexperienced, or where pride and publicity "
    "reward winning for its own sake, the curse tends to bite hardest.\n\n"
    "The idea reaches well beyond auctions. A company that wins a fierce bidding war to take over a rival, a city "
    "that outbids others to host a costly sporting event, even a buyer who beats a crowd of others to a house, may "
    "each discover that the victory was the most expensive part of the deal."))

Q(RC, "Inference", A,
  "Why, according to the reasoning of the passage, is winning an auction 'unwelcome' news for a bidder?",
  ["It shows that the seller has hidden important facts about the item.",
   "It means she must now pay fees to the people who organised the sale.",
   "It reveals that all the rivals valued the item lower than she did.",
   "It proves that her rivals deliberately bid low to trick her."], 2,
  "Inference: following the author's chain of reasoning",
  "Paragraph 2: winning tells a bidder 'that everyone else valued the prize less highly, and so her own estimate was "
  "probably too high'. Since all estimates contain error, being the highest suggests hers had the biggest upward "
  "error.",
  ["All estimates contain error", "Winner = highest estimate", "So her estimate was probably too high"],
  "Hidden facts, organisers' fees and deliberate tricks by rivals are not part of the argument; the curse arises even "
  "when everyone bids honestly on the same uncertain value.", 55, P5, 1)

Q(RC, "Inference", A,
  "According to the passage, how should a careful bidder change her bid as the number of rival bidders increases?",
  ["Raise it, because more rivals mean she is less likely to win.",
   "Lower it further, because the top estimate grows more extreme.",
   "Keep it fixed at her best guess of what the item is worth.",
   "Withdraw from the auction once there are more than a few rivals."], 1,
  "Inference: applying the stated rule and its reason",
  "Paragraph 3: she should 'shade her bid further as the number of rivals grows, because the more bidders there are, "
  "the more extreme the most optimistic estimate is likely to be'.",
  ["More bidders → more extreme highest estimate", "Winning then signals a bigger overestimate",
   "So lower the bid further"],
  "Raising the bid is the instinct the passage warns against. Bidding her best guess is what the passage says she "
  "should not do ('Rather than bidding what she believes the item is worth'). Withdrawing is never advised.",
  55, P5, 2)

Q(RC, "Inference", A,
  "In which of the following situations is the winner's curse, as defined in the passage, LEAST likely to arise?",
  ["Oil companies bidding for the right to drill in an unexplored field",
   "Telecom firms bidding for a licence to use a band of frequencies",
   "Investors bidding for a company whose future profits are uncertain",
   "A collector bidding for a painting she wants for her own home"], 3,
  "Inference: applying a definition to new cases",
  "The curse needs an item whose value is the same for all bidders but uncertain to each. A painting bought for one's "
  "own wall is worth different amounts to different people, and the collector knows what it is worth to her, so "
  "winning does not reveal that she overestimated a common value.",
  ["Condition 1: value the same for all bidders", "Condition 2: that value uncertain to each",
   "Personal taste fails both conditions"],
  "The oil field, the frequency licence and the company are the passage's own examples of a common but uncertain "
  "value, so the curse is likely in each of them.", 60, P5, 3)

Q(RC, "Inference", A,
  "Why, according to the passage, does releasing more information about an item reduce the winner's curse?",
  ["It narrows the spread of estimates, so the highest is nearer the truth.",
   "It persuades inexperienced bidders to stay away from the auction.",
   "It allows the seller to set a higher minimum price for the item.",
   "It makes pride and publicity less important to the bidders."], 0,
  "Inference: explaining why a remedy works",
  "Paragraph 4 says more information 'narrows the spread of estimates'. If estimates are bunched closer together, "
  "the most optimistic one is not far above the true value, so the winner overpays by less.",
  ["More information → estimates closer together", "Highest estimate less extreme",
   "Smaller overpayment by the winner"],
  "Keeping bidders away, raising the minimum price and reducing pride are not effects the passage attributes to more "
  "information.", 55, P5, 4)

Q(RC, "Vocabulary in context", A,
  "Which of the following is closest in meaning to the word 'shade' as used in the passage ('shade her bid further "
  "as the number of rivals grows')?",
  ["hide from view", "reduce slightly", "keep it safe", "make darker"], 1,
  "Vocabulary in context: shade (a figure) = adjust it slightly, here downwards",
  "The sentence tells the bidder to bid 'somewhat less' than her estimate, and to do so 'further' when there are "
  "more rivals. To shade a bid here is to lower it a little.",
  ["Context: 'bid somewhat less'", "'shade further' = lower it more", "'reduce slightly'"],
  "'Hide from view', 'keep it safe' and 'make darker' are other senses of 'shade' that do not fit a number "
  "being adjusted.", 40, P5, 5)

Q(RC, "Tone and title", A,
  "Which of the following best describes the author's approach in the passage?",
  ["Analytical, explaining a counter-intuitive risk and how to guard against it",
   "Nostalgic, recalling a classroom game that the author once enjoyed",
   "Sarcastic, mocking companies that lose money in takeover battles",
   "Alarmist, demanding that governments stop selling licences by auction"], 0,
  "Tone: identify the purpose and manner of the whole passage",
  "The author uses an experiment to explain a concept, gives its conditions and a remedy, and applies it to other "
  "situations. This is a calm, analytical explanation of a counter-intuitive risk.",
  ["Example → concept → advice → remedies → wider uses", "Calm, reasoned explanation",
   "'counter-intuitive' is the author's own word"],
  "The classroom jar is a thought experiment, not a memory. Takeovers are mentioned without mockery. The author says "
  "the curse 'is not inevitable' and never calls for auctions to be stopped.", 45, P5, 6)

# ---------------------------------------------------------------- RC 6 (Advanced, 6)
P6 = stim("When the totals mislead", (
    "A regional manager comparing two branches of a bank looks at a single figure: the share of loans repaid on time. "
    "The town branch recovers 88 per cent of its loans, the hill branch only 79 per cent. The conclusion seems "
    "obvious, and the hill branch is told to learn from its neighbour.\n\n"
    "A closer look tells a different story. Each branch makes two kinds of loans: crop loans to small farmers, which "
    "are riskier because they depend on the weather, and salary loans to government employees, which are almost "
    "always repaid. Of the hill branch's 100 loans, 80 are crop loans, of which 60 were repaid, and 20 are salary "
    "loans, of which 19 were repaid. The town branch made only 20 crop loans, recovering 14, and 80 salary loans, "
    "recovering 74.\n\n"
    "Now compare like with like. On crop loans, the hill branch recovers 75 per cent and the town branch 70 per cent. "
    "On salary loans, the hill branch recovers 95 per cent and the town branch 92.5 per cent. The hill branch does "
    "better in both categories, yet worse overall. It is not a weaker lender; it simply makes far more of the "
    "difficult loans.\n\n"
    "This reversal is known as Simpson's paradox. It appears whenever the groups being compared differ in their mix "
    "of some factor that strongly affects the outcome. A hospital that treats the most serious cases can show a "
    "higher death rate than others even if it treats every type of patient better; a school that admits weaker "
    "students can post lower pass rates while adding more to each student's learning.\n\n"
    "The paradox does not mean that totals are useless, nor that a breakdown always gives the truer picture. "
    "Splitting data by the wrong factor can create misleading patterns of its own. What it demands is a question "
    "before every comparison: are these groups really alike in the ways that matter? A manager who asked it might "
    "reward the hill branch for taking on the farmers whom others avoid, rather than scold it for the arithmetic that "
    "follows."))

# the figures in the passage, checked
HILL = {"crop": (80, 60), "salary": (20, 19)}
TOWN = {"crop": (20, 14), "salary": (80, 74)}


def pct(repaid, made):
    return Fraction(100 * repaid, made)


def overall(branch):
    return pct(sum(r for _, r in branch.values()), sum(m for m, _ in branch.values()))


assert overall(HILL) == 79 and overall(TOWN) == 88
assert pct(*HILL["crop"][::-1]) == 75 and pct(*TOWN["crop"][::-1]) == 70
assert pct(*HILL["salary"][::-1]) == 95 and pct(*TOWN["salary"][::-1]) == Fraction(185, 2)   # 92.5
assert all(pct(*HILL[k][::-1]) > pct(*TOWN[k][::-1]) for k in HILL) and overall(HILL) < overall(TOWN)
# question 2: the town branch makes 20 more crop loans and recovers 14 of them
TOWN_MORE = {"crop": (40, 28), "salary": (80, 74)}
RC6_Q2 = overall(TOWN_MORE)
assert RC6_Q2 == 85
TOWN_CROP_RATE, TOWN_SALARY_RATE = 70, 92.5
SIMPLE_AVG = (TOWN_CROP_RATE + TOWN_SALARY_RATE) / 2               # wrong method behind 'about 81 per cent'
assert SIMPLE_AVG == 81.25
FORGOT_REPAID = Fraction(100 * (14 + 74), 120)                      # wrong method behind 'about 73 per cent'
assert round(float(FORGOT_REPAID)) == 73
# question 1 distractor check: if the hill branch had the town branch's loan mix but its own rates
HILL_WITH_TOWN_MIX = Fraction(20 * 75 + 80 * 95, 100)
assert HILL_WITH_TOWN_MIX == 91 and HILL_WITH_TOWN_MIX > overall(TOWN)

Q(RC, "Inference", A,
  "Why, according to the passage, does the hill branch's overall recovery rate look worse than the town branch's?",
  ["It recovers a smaller share of both crop loans and salary loans.",
   "Most of its loans are crop loans, which are repaid less often.",
   "It made far fewer loans in total than the town branch did.",
   "Its salary loans go to employees who are rarely paid on time."], 1,
  "Inference: explaining a reversal by the mix of groups",
  "Both branches made 100 loans. The hill branch does better in each category (75% vs 70%, 95% vs 92.5%), but 80 of "
  f"its 100 loans are risky crop loans, against only 20 at the town branch. Given the town branch's mix, its own "
  f"rates would give {HILL_WITH_TOWN_MIX}%, above the town branch's 88%.",
  ["Both branches: 100 loans each", "Hill is better in each category",
   "Hill's mix: 80 crop loans vs town's 20", "The mix, not skill, drags its total down"],
  "The hill branch recovers a larger share in both categories, not a smaller one. Both branches made 100 loans. "
  "Salary loans are described as 'almost always repaid', and the hill branch recovers 19 of 20.", 60, P6, 1)

Q(RC, "Inference", A,
  "Suppose the town branch made 20 more crop loans and recovered 14 of them, with its salary loans unchanged. What "
  "would its overall recovery rate then be?",
  ["88 per cent", "85 per cent", "about 81 per cent", "about 73 per cent"], 1,
  "Inference: recomputing an overall rate after the mix changes",
  f"Crop loans become 20 + 20 = 40, with 14 + 14 = 28 repaid; salary loans stay at 80 with 74 repaid. Overall: "
  f"(28 + 74) ÷ (40 + 80) = 102 ÷ 120 = {RC6_Q2} per cent. Adding more risky loans pulls the total down even though "
  f"the crop-loan rate (70%) is unchanged.",
  ["Crop: 40 loans, 28 repaid", "Salary: 80 loans, 74 repaid", f"102 ÷ 120 = {RC6_Q2}%"],
  f"88 per cent ignores the new loans. About 81 per cent is the simple average of the two category rates "
  f"(({TOWN_CROP_RATE} + {TOWN_SALARY_RATE}) ÷ 2 = {SIMPLE_AVG}), which ignores how many loans fall in each. About "
  f"73 per cent counts the 20 new loans but forgets the 14 that were repaid ((14 + 74) ÷ 120).", 75, P6, 2,
  shortcut="Overall rate = total repaid ÷ total loans = (28 + 74) ÷ 120 = 85%")

Q(RC, "Inference", A,
  "The example of the hospital in paragraph 4 is used to show that",
  ["hospitals should refuse the most serious cases to protect their records",
   "a raw comparison can make those who take the hardest cases look worse",
   "death rates are a poor measure of a hospital's work in every situation",
   "patients should always choose the hospital with the lowest death rate"], 1,
  "Inference: the purpose of an example",
  "Like the hill branch, a hospital that takes the most serious cases can do better with every type of patient yet "
  "show a worse overall figure. The example shows that raw totals can penalise those who take on the hardest cases.",
  ["Hill branch: hardest loans, worse total", "Hospital: hardest patients, worse total",
   "Same lesson: raw totals can mislead"],
  "The author does not recommend refusing serious cases; the last line praises taking on hard cases. Paragraph 5 "
  "says totals are not useless, so 'in every situation' goes too far. Choosing the lowest death rate is exactly the "
  "mistake the example warns against.", 55, P6, 3)

Q(RC, "Inference", A,
  "What does the author mean by saying that 'Splitting data by the wrong factor can create misleading patterns of "
  "its own'?",
  ["A breakdown is useful only if it is by a factor that really affects the outcome.",
   "Totals should never be broken down, because breakdowns always mislead.",
   "Every comparison of branches should be split into as many groups as possible.",
   "Simpson's paradox appears only when data are split into exactly two groups."], 0,
  "Inference: reading a qualification of the main argument",
  "The author warns against treating any breakdown as automatically truer. The useful question is whether the groups "
  "differ 'in the ways that matter', so a breakdown helps only when it is by a factor that genuinely affects the "
  "result.",
  ["Breakdowns are not automatically truer", "The wrong factor can mislead too",
   "Split by factors that matter"],
  "'Never be broken down' contradicts the whole branch example. 'As many groups as possible' ignores the warning "
  "about the wrong factor. The number of groups is not the author's point.", 55, P6, 4)

Q(RC, "Vocabulary in context", A,
  "Which of the following is closest in meaning to the word 'post' as used in the passage ('a school that admits "
  "weaker students can post lower pass rates')?",
  ["mail", "record", "appoint", "display on a wall"], 1,
  "Vocabulary in context: post (results, figures) = record or report them",
  "A school does not mail or appoint its pass rates; it records and reports them. 'Post lower pass rates' means "
  "show lower pass rates in its results.",
  ["Object: pass rates (figures)", "Figures are recorded or reported", "'record'"],
  "'Mail', 'appoint' and 'display on a wall' are other senses of 'post' that do not fit figures a school achieves.",
  40, P6, 5)

Q(RC, "Tone and title", A,
  "Which of the following best expresses the central lesson of the passage?",
  ["Compare groups only after checking that they are alike in what matters.",
   "Branches that lend to farmers should be closed to protect the bank.",
   "Overall figures are always more reliable than detailed breakdowns.",
   "Hospitals and schools should be judged by the same rules as banks."], 0,
  "Main idea: the question the author says every comparison demands",
  "The passage ends with the question that the paradox demands: 'are these groups really alike in the ways that "
  "matter?' Its lesson is to check that groups are alike before comparing their totals.",
  ["Branch example: totals mislead", "Paradox explained with other cases",
   "Last paragraph: ask whether the groups are alike"],
  "The author praises lending to farmers. The passage shows how totals can mislead, so they are not 'always more "
  "reliable'. Hospitals and schools are examples, not the subject of a recommendation.", 45, P6, 6)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic, 6)
C1 = stim("The pot that keeps water cool", (
    "In many Indian homes, a round earthen pot still sits in a corner of the kitchen, (1) ______ with drinking "
    "water. Even on the hottest summer afternoon, the water inside stays pleasantly cool, although the pot uses no "
    "electricity at all and costs only a small sum at the local market.\n\n"
    "The secret lies in the clay. Baked clay is full of tiny holes, so a little water slowly (2) ______ through the "
    "walls of the pot to its outer surface. There it evaporates, and evaporation carries heat away from the pot, "
    "just as sweat cools our skin on a hot day. The drier and (3) ______ the air, the faster the water evaporates and "
    "the cooler the pot becomes. In humid coastal weather, when the air is already full of moisture, the effect is "
    "much (4) ______.\n\n"
    "Potters say that a new pot works best after it has been soaked and used for a few days. They also advise "
    "keeping it in a shady, airy place, and (5) ______ it regularly so that its tiny holes are not blocked by dust "
    "and by the salts left behind by the water.\n\n"
    "In recent years, the earthen pot has found new admirers. Some families who own refrigerators still prefer it, "
    "because its water is cool without being icy and is gentler on the throat. Designers have used the same "
    "principle to build simple clay coolers for vegetables, which help small farmers and vendors keep their produce "
    "fresh for a few extra days. An old object, it seems, still has something to (6) ______ to a modern world that "
    "is worried about rising temperatures and electricity bills."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["filled", "emptied", "painted", "broken"], 0,
  "Cloze: 'with drinking water' needs a word meaning 'containing'",
  "The pot holds drinking water that 'stays pleasantly cool', so it is filled with water.",
  ["Phrase: '___ with drinking water'", "The next sentence: the water inside stays cool", "'filled'"],
  "A pot 'emptied with water' or 'broken with water' makes no sense, and an emptied or broken pot could not keep "
  "water cool. 'Painted with drinking water' is meaningless.", 25, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["trickles", "leaps", "burns", "freezes"], 0,
  "Cloze: slow movement of water through tiny holes",
  "Water that passes slowly, a little at a time, through the tiny holes in clay 'trickles' through the walls.",
  ["Clue: 'tiny holes', 'slowly', 'a little water'", "Slow movement of a small amount of liquid", "'trickles'"],
  "Water does not 'leap' or 'burn' through clay. 'Freezes' contradicts the hot weather and the evaporation in the "
  "next sentence.", 25, C1, 2)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=3), ["colder", "wetter", "warmer", "darker"], 2,
  "Cloze: conditions that speed up evaporation",
  "Water evaporates faster in dry, warm air. The sentence pairs 'drier' with a second quality that helps "
  "evaporation: 'warmer'. It also fits the opening point that the pot works on the hottest afternoons.",
  ["Pairing: 'The drier and ___ the air'", "Evaporation is faster in warm air", "'warmer'"],
  "'Wetter' contradicts 'drier' and the next sentence, which says humid air weakens the effect. Colder air slows "
  "evaporation. 'Darker' has nothing to do with evaporation.", 30, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["stronger", "weaker", "faster", "louder"], 1,
  "Cloze: humid air slows evaporation, so the cooling is less",
  "Air 'already full of moisture' takes up water slowly, so less evaporation happens and the pot cools less. The "
  "effect is much weaker.",
  ["Clue: air already full of moisture", "Less evaporation → less cooling", "'weaker'"],
  "'Stronger' and 'faster' reverse the effect of humid air described in the passage. 'Louder' does not describe "
  "cooling.", 25, C1, 4)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=5), ["painting", "heating", "cleaning", "covering"], 2,
  "Cloze: the purpose clause after the blank decides the word",
  "The pot must be treated 'so that its tiny holes are not blocked by dust and ... salts'. Removing dust and salts "
  "means cleaning it regularly.",
  ["Purpose: keep the holes free of dust and salts", "Action that removes dirt", "'cleaning'"],
  "Painting or covering the pot would block its holes, the opposite of the purpose. Heating it does not remove dust "
  "or salts.", 25, C1, 5)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=6), ["offer", "fear", "hide", "refuse"], 0,
  "Cloze: 'have something to ___ to someone' = have something useful to give",
  "An old object that saves electricity and keeps things cool can offer a lesson to a world worried about heat and "
  "power bills: it still has something to offer to it.",
  ["Structure: 'something to ___ to a modern world'", "The pot has something useful to give", "'offer'"],
  "'Fear to a modern world' and 'hide to a modern world' are ungrammatical. 'Something to refuse to a modern world' "
  "contradicts the praise of the pot in the paragraph.", 25, C1, 6)

# ---------------------------------------------------------------- Cloze 2 (Basic 1 + Intermediate 5)
C2 = stim("The vanishing scavengers", (
    "Not long ago, vultures were a common sight in India, circling high above towns or crowding around the body of a "
    "dead cow at the edge of a village. Then, within roughly a decade from the 1990s, the numbers of several species "
    "(1) ______ by more than ninety per cent, one of the fastest declines of any bird ever recorded.\n\n"
    "For years the cause remained a (2) ______. Scientists suspected disease or poisoning, but the answer turned out "
    "to be a common painkiller given to cattle. Vultures that fed on the bodies of animals treated shortly before "
    "death absorbed the drug, which (3) ______ their kidneys. Because a single carcass can feed dozens of birds, even "
    "a small share of treated animals was enough to kill vast numbers of them.\n\n"
    "The loss was not only an ecological one. Vultures had quietly performed a public service, stripping a carcass to "
    "the bone within hours. Without them, carcasses lay rotting for days, and the number of stray dogs feeding on "
    "them rose. More dogs meant more dog bites and more cases of rabies, a disease that is almost always (4) ______ "
    "once its symptoms appear.\n\n"
    "The veterinary use of the drug was banned, and breeding centres were set up to raise vultures in captivity and "
    "later release them into the wild. Progress has been slow, partly because vultures breed slowly, (5) ______ only "
    "one egg a year, and partly because some other painkillers that harm them remain in use.\n\n"
    "The story is a reminder that the value of a species is not always obvious until it is gone. Animals that seem "
    "(6) ______, even unpleasant, may be holding up parts of the system on which human health depends."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["rose", "fell", "settled", "doubled"], 1,
  "Cloze: 'one of the fastest declines' decides the direction",
  "The sentence ends by calling this 'one of the fastest declines of any bird', so the numbers fell by more than "
  "ninety per cent.",
  ["Clue: 'one of the fastest declines'", "A decline = a fall", "'fell'"],
  "'Rose' and 'doubled' are increases, which contradict 'declines'. 'Settled by more than ninety per cent' is "
  "meaningless.", 25, C2, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["certainty", "mystery", "celebration", "decision"], 1,
  "Cloze: 'For years' and 'Scientists suspected' show the cause was unknown",
  "Scientists only 'suspected' causes until 'the answer turned out to be' a painkiller. Something unexplained for "
  "years is a mystery.",
  ["'For years the cause remained a ___'", "Scientists suspected, then found 'the answer'", "'mystery'"],
  "'Certainty' contradicts the guessing that followed. 'Celebration' and 'decision' do not describe an unknown "
  "cause.", 30, C2, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["cleaned", "strengthened", "damaged", "cooled"], 2,
  "Cloze: the drug killed the birds, so it harmed an organ",
  "The next sentence says the drug was 'enough to kill vast numbers' of vultures. A drug that kills by acting on "
  "the kidneys damaged them.",
  ["Effect of the drug: deaths", "It acted on the kidneys", "'damaged'"],
  "'Cleaned', 'strengthened' and 'cooled' describe harmless or helpful effects, which cannot explain mass deaths.",
  30, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["curable", "mild", "fatal", "rare"], 2,
  "Cloze: the word must make rabies a reason for concern",
  "The paragraph lists harms that followed the loss of vultures. Rabies is a serious harm because, once symptoms "
  "appear, it almost always kills: it is fatal.",
  ["Context: harms caused by more dogs", "Rabies once symptoms appear", "'fatal'"],
  "'Curable' and 'mild' would make rabies a small matter, which does not fit a list of serious harms. 'Rare' "
  "contradicts 'more cases of rabies'.", 30, C2, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["eating", "laying", "hiding", "selling"], 1,
  "Cloze: the participle phrase explains 'breed slowly'",
  "Vultures breed slowly because each pair produces only one egg a year, that is, they lay only one egg a year.",
  ["Claim: vultures breed slowly", "Explanation: only one egg a year", "'laying'"],
  "'Eating', 'hiding' and 'selling' one egg a year do not explain slow breeding, and birds do not sell eggs.",
  30, C2, 5)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=6), ["precious", "worthless", "beautiful", "endangered"], 1,
  "Cloze: 'seem ___, even unpleasant' is contrasted with real value",
  "The passage says a species' value 'is not always obvious'. Animals that seem of no value, even unpleasant, may "
  "in fact be important: they seem worthless.",
  ["'value ... not always obvious'", "'seem ___, even unpleasant' → seem to have no value", "'worthless'"],
  "'Precious' and 'beautiful' would mean the value is already obvious, and do not build up to 'even unpleasant'. "
  "'Endangered' is about numbers, not about how valuable an animal seems.", 35, C2, 6)

# ---------------------------------------------------------------- Cloze 3 (Advanced, 6; error-based)
C3 = stim("The trap of the minimum due", (
    "Every credit card statement shows two figures that matter: the total amount due, and a much smaller 'minimum "
    "amount due', usually a small percentage of the balance. Paying the minimum keeps the account in good standing "
    "and **(1) avoids** a late-payment fee. Many cardholders therefore treat it as the amount they owe. That is an "
    "expensive mistake.\n\n"
    "Any part of the balance that is not paid by the due date begins to attract interest, often at rates of thirty "
    "to forty per cent a year, far **(2) lower** than the rate on almost any other kind of borrowing. Worse, on many "
    "cards the interest-free period on new purchases is lost as long as an old balance is carried forward, so even "
    "fresh spending starts attracting interest from the day it is made. A cardholder who pays only the minimum each "
    "month may find, after a year of steady payments, that the balance has barely **(3) fallen**.\n\n"
    "The design is not accidental. Card issuers earn much of their income from customers who **(4) clear** their "
    "balances from month to month, and a low minimum makes this easy to do. In the United States, for example, card "
    "statements must show how long it would take to repay the balance through minimum payments alone, and how much "
    "would be paid in total along the way; the figures are often **(5) sobering**.\n\n"
    "The remedy is simple to state, if not always to follow: treat the card as a convenient way to pay, not as a "
    "source of credit, and settle the full amount every month. A cardholder who cannot do so is, in effect, "
    "borrowing at one of the highest rates on offer, and would usually be better off **(6) increasing** the card "
    "balance with a cheaper personal loan."))

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=1, ctx="Paying the minimum keeps the account in good standing and avoids a late-payment fee"),
  ["incurs", "doubles", "waives", NR], 3,
  "Error-based cloze: the 'and' clause must state a benefit, like 'good standing'",
  "Paying at least the minimum keeps the account in good standing and so escapes the fee charged for late payment. "
  "'Avoids' is correct; it also explains why many people think the minimum is enough.",
  ["First benefit: account in good standing", "Second benefit: no late-payment fee", "'avoids' fits: no replacement"],
  "'Incurs' (brings on) and 'doubles' turn the benefit into a penalty. 'Waives' is what a bank does, not what a "
  "payment does.", 45, C3, 1, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=2, ctx="often at rates of thirty to forty per cent a year, far lower than the rate on almost any "
                           "other kind of borrowing"),
  ["higher", "safer", "fairer", NR], 0,
  "Error-based cloze: thirty to forty per cent a year is a very high rate",
  "Rates of thirty to forty per cent are far above those on home, car or personal loans. The last paragraph ('one "
  "of the highest rates on offer') confirms that card interest is far higher, not lower.",
  ["30-40% a year is very high", "Last paragraph: 'one of the highest rates on offer'", "Replace 'lower' with 'higher'"],
  "'Safer' and 'fairer' do not compare the cost of borrowing. 'Lower' contradicts the figures and the last "
  "paragraph, so 'No replacement required' does not apply.", 45, C3, 2, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=3, ctx="may find, after a year of steady payments, that the balance has barely fallen"),
  ["doubled", "vanished", "risen", NR], 3,
  "Error-based cloze: the surprise is that steady payments hardly reduce the balance",
  "Because most of each minimum payment goes on interest, a year of steady payments reduces the balance only a "
  "little: it has 'barely fallen'. 'Fallen' is correct.",
  ["Steady payments → one expects the balance to fall", "High interest eats most of each payment",
   "'barely fallen' fits: no replacement"],
  "'Barely doubled' and 'barely vanished' are contradictory phrases. 'Barely risen' implies the balance was expected "
  "to rise, which makes no sense after a year of payments.", 45, C3, 3, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=4, ctx="Card issuers earn much of their income from customers who clear their balances from month "
                           "to month, and a low minimum makes this easy to do"),
  ["roll over", "check", "close", NR], 0,
  "Error-based cloze: issuers earn interest only on unpaid balances",
  "Interest is charged on balances that are not paid off. Issuers earn from customers who roll over (carry "
  "forward) their balances from month to month, and a low minimum makes this easy. Customers who clear their "
  "balances pay no interest.",
  ["Interest comes from unpaid balances", "A low minimum lets people leave balances unpaid",
   "Replace 'clear' with 'roll over'"],
  "'Check their balances' does not produce interest income. 'Close their balances from month to month' is "
  "meaningless. 'Clear' reverses the logic, so 'No replacement required' does not apply.", 50, C3, 4,
  order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=5, ctx="how long it would take to repay the balance through minimum payments alone, and how much "
                           "would be paid in total along the way; the figures are often sobering"),
  ["reassuring", "trivial", "cheerful", NR], 3,
  "Error-based cloze: the figures reveal a long, costly repayment",
  "Repaying through minimum payments alone takes years and costs far more than the original balance. Figures that "
  "make people think seriously about a danger are 'sobering'. The word is correct.",
  ["Minimum payments → very long, very costly repayment", "Such figures shock people into caution",
   "'sobering' fits: no replacement"],
  "'Reassuring', 'trivial' and 'cheerful' contradict the passage's warning that paying only the minimum is 'an "
  "expensive mistake'.", 45, C3, 5, order=LAST_FIXED)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=6, ctx="would usually be better off increasing the card balance with a cheaper personal loan"),
  ["replacing", "ignoring", "doubling", NR], 0,
  "Error-based cloze: a cheaper loan should take the place of the costly card debt",
  "A cardholder paying one of the highest rates would be better off paying off the card with a cheaper loan: "
  "replacing the card balance with a personal loan. 'Increasing' the costly balance makes no sense.",
  ["Card debt is very expensive", "A cheaper loan can pay it off", "Replace 'increasing' with 'replacing'"],
  "'Ignoring' and 'doubling' the card balance would make matters worse. 'Increasing' contradicts 'better off', so "
  "'No replacement required' does not apply.", 45, C3, 6, order=LAST_FIXED)

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


# ---- Basic (2)
ed("Part-wise error", B, "My elder brother he", "works as a clerk", "in a cooperative bank.", "A",
   "A clause has one subject; a pronoun does not repeat a noun subject that has just been named",
   "'My elder brother' is already the subject of 'works'. Adding 'he' gives the verb two subjects. Correct: 'My elder "
   "brother works as a clerk in a cooperative bank.'",
   ["Subject: 'My elder brother'", "'he' repeats the same subject", "Drop 'he': error in part A"],
   "Part B has a singular verb that agrees with 'brother'. Part C is a correct place phrase. A has an error, so 'No "
   "error' is wrong.", 25)

ed("Part-wise error", B, "All the members of the society", "are agree with", "the new timings of the branch.", "B",
   "'Agree' is a verb, not an adjective, so it is not used after 'am/is/are'",
   "'Agree' is a full verb: 'All the members agree with the new timings'. 'Are agree' wrongly adds the verb 'be' "
   "before it, as if 'agree' were an adjective like 'happy'.",
   ["'agree' is a verb", "A verb does not need 'are' before it", "'are agree with' → 'agree with': error in part B"],
   "Part A is a correct plural subject. Part C is a correct object phrase. B has an error, so 'No error' is wrong.",
   25)

# ---- Intermediate (8)
ed("Part-wise error", I, "One or two customers", "has complained about", "the noise from the new generator.", "B",
   "'One or two' + plural noun takes a plural verb (unlike 'more than one' + singular noun)",
   "'One or two customers' means a few customers; the noun is plural and so is the verb: 'One or two customers have "
   "complained about the noise ...'.",
   ["Subject: 'One or two customers' (plural noun)", "Plural noun → plural verb", "'has complained' → 'have "
    "complained': error in part B"],
   "Part A correctly uses the plural noun 'customers' after 'one or two'. Part C is a correct object phrase. B has an "
   "error, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "Fifty new staffs", "have been recruited", "for the bank's rural branches.", "A",
   "'Staff' (the people who work for an organisation) is a collective noun with no '-s' plural in this sense",
   "'Staff' already refers to a group of employees, so it does not take '-s' when counting people: 'Fifty new staff "
   "(or staff members) have been recruited ...'.",
   ["'staff' = the employees as a group", "No '-s' plural for people", "'Fifty new staffs' → 'Fifty new staff "
    "members': error in part A"],
   "Part B's plural verb suits a subject of fifty people. Part C is a correct prepositional phrase. A has an error, so "
   "'No error' is wrong.", 35)

ed("Part-wise error", I, "The cashier absented", "from the office for two days", "without informing the manager.",
   "A",
   "'Absent' as a verb is reflexive: absent oneself (from a place)",
   "The verb 'absent' needs a reflexive pronoun: 'The cashier absented himself from the office for two days ...'. "
   "Without 'himself', the verb has no object.",
   ["Verb: 'absent' (stay away)", "Pattern: absent + oneself + from", "'absented' → 'absented himself': error in "
    "part A"],
   "Part B correctly uses 'from' for the place and 'for' for the period. Part C is a correct gerund phrase after "
   "'without'. A has an error, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "Every member of the society", "must abide to", "the rules framed by its board.", "B",
   "Fixed preposition: abide by (a rule, decision or agreement) = obey it",
   "The phrasal verb meaning 'obey' is 'abide by': 'Every member of the society must abide by the rules framed by its "
   "board.'",
   ["Meaning: obey the rules", "Fixed form: abide by", "'abide to' → 'abide by': error in part B"],
   "Part A is a correct singular subject. Part C is a correct object with a participle phrase. B has an error, so "
   "'No error' is wrong.", 30)

ed("Part-wise error", I, "The new software", "is capable to handle", "ten thousand transactions a minute.", "B",
   "'Capable' takes 'of' + -ing (capable of doing), not a to-infinitive",
   "The adjective 'capable' is followed by 'of' and a gerund: 'The new software is capable of handling ten thousand "
   "transactions a minute.' (Compare 'able to handle'.)",
   ["Adjective: 'capable'", "Pattern: capable of + -ing", "'capable to handle' → 'capable of handling': error in part B"],
   "Part A is a correct subject. Part C is a correct object with a rate ('a minute'). B has an error, so 'No "
   "error' is wrong.", 35)

ed("Part-wise error", I, "All applicants must submit", "the signed forms", "till the fifteenth of this month.", "C",
   "'By' marks a deadline (no later than); 'till/until' marks how long a situation continues",
   "Submitting a form is a single action that must happen no later than a date, so the preposition is 'by': '... "
   "must submit the signed forms by the fifteenth of this month.' 'Till' would suggest that applicants keep "
   "submitting until that date.",
   ["Action: submit (a single act)", "A deadline → 'by'", "'till the fifteenth' → 'by the fifteenth': error in part C"],
   "Part A correctly uses 'must' + base verb. Part B is a correct object. C has an error, so 'No error' is wrong.",
   35)

ed("Part-wise error", I, "The power supply to the branch", "was cut off", "during three hours this morning.", "C",
   "'For' + a length of time (for three hours); 'during' + a named period or event (during the night, during the "
   "meeting)",
   "'Three hours' measures how long the cut lasted, which needs 'for': 'was cut off for three hours this morning'. "
   "'During' is used with a period named as a whole, such as 'during the morning'.",
   ["'three hours' = a length of time", "Length of time → 'for'", "'during three hours' → 'for three hours': error "
    "in part C"],
   "Part A is a correct subject. Part B is a correct passive of the phrasal verb 'cut off'. C has an error, so 'No "
   "error' is wrong.", 35)

ed("Error-free sentence", I, "Having been warned twice by the auditors,", "the clerk now checks every voucher",
   "before filing it.", "D",
   "Perfect passive participle ('Having been + past participle') whose subject is the subject of the main clause",
   "The clerk was warned (passive) before he began checking. 'Having been warned twice by the auditors' correctly "
   "refers to 'the clerk', the subject of the main clause. 'Before filing it' correctly uses a gerund after the "
   "preposition 'before'.",
   ["Part A: perfect passive participle, doer of 'warned' = auditors: correct",
    "Part B: its subject 'the clerk' is the one who was warned: correct", "Part C: 'before' + -ing: correct",
    "No error"],
   "A, B and C are each correct as shown in the steps. The participle does not dangle, because the clerk is the one "
   "who was warned.", 40)

# ---- Advanced (3)
ed("Part-wise error", A, "When I met him in 2020,", "he told me that he had left", "the bank three years ago.", "C",
   "'Ago' counts back from now; to count back from a past point, use 'before' or 'earlier'",
   "He left the bank three years before 2020, not three years before today. Seen from a past moment, the right word "
   "is 'before' or 'earlier': '... he had left the bank three years before (or earlier).'",
   ["Reference point: 2020, in the past", "'ago' measures back from the present", "'three years ago' → 'three years "
    "before': error in part C"],
   "Part A is a correct past time clause. Part B correctly uses the past perfect for the earlier action. C has an "
   "error, so 'No error' is wrong.", 45)

ed("Part-wise error", A, "Many first-time borrowers are unsure", "if to choose a fixed rate", "or a floating one.",
   "B",
   "Before a to-infinitive, only 'whether' can introduce the choice ('whether to'); 'if to' is never used",
   "A yes/no or either/or choice followed by an infinitive must begin with 'whether': 'Many first-time borrowers are "
   "unsure whether to choose a fixed rate or a floating one.' 'If' can introduce a full clause ('unsure if they "
   "should choose ...') but never a bare to-infinitive.",
   ["Choice expressed with a to-infinitive: '___ to choose'", "Only 'whether' + to-infinitive is possible",
    "'if to choose' → 'whether to choose': error in part B"],
   "Part A is a correct subject and adjective. Part C correctly completes the choice with 'or a floating one'. B has "
   "an error, so 'No error' is wrong.", 45)

ed("Part-wise error", A, "The officer said that if the documents were in order", "that the loan would be released",
   "within a week of the visit.", "B",
   "A reported clause takes one 'that'; it is not repeated after an inserted 'if' clause",
   "'Said that' already introduces the reported clause. The 'if' clause is inserted inside it, so the main part "
   "continues without a second 'that': 'The officer said that if the documents were in order, the loan would be "
   "released within a week of the visit.'",
   ["'said that' introduces the reported clause", "'if the documents were in order' is inserted inside it",
    "The second 'that' repeats the first: error in part B"],
   "Part A correctly backshifts to 'were' after 'said'. Part C is a correct time phrase. B has an error, so 'No "
   "error' is wrong.", 45)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", B,
  SI_STEM + "After three attempts, the shopkeeper finally **succeeded to get** a loan for his new shop.",
  ["succeeded in getting", "succeeded for getting", "succeeded getting", NI], 0,
  "'Succeed' takes 'in' + -ing (succeed in doing something)",
  "The verb 'succeed' is followed by 'in' and a gerund: 'the shopkeeper finally succeeded in getting a loan'.",
  ["Verb: succeed", "Pattern: succeed in + -ing", "'succeeded in getting'"],
  "'Succeeded for getting' uses the wrong preposition. 'Succeeded getting' leaves out the preposition. The original "
  "uses a to-infinitive, so 'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "Do you **know to operate** the new cash-counting machine?",
  ["know operating", "know how to operate", "know for operating", NI], 1,
  "'Know' + a question word + to-infinitive (know how to do something), not 'know' + to-infinitive",
  "To talk about having a skill, English uses 'know how to': 'Do you know how to operate the new cash-counting "
  "machine?'",
  ["Meaning: have the skill", "Pattern: know how to + verb", "'know how to operate'"],
  "'Know operating' and 'know for operating' are not used for a skill. The original leaves out 'how', so 'No "
  "improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "Ramesh is **taller from his brother** by almost five centimetres.",
  ["more taller than his brother", "tallest than his brother", "taller than his brother", NI], 2,
  "A comparative adjective is followed by 'than', not 'from'",
  "Comparisons with a comparative adjective use 'than': 'Ramesh is taller than his brother by almost five "
  "centimetres.'",
  ["Comparative: 'taller'", "Comparative + than", "'taller than his brother'"],
  "'More taller' adds 'more' to a form that is already comparative. 'Tallest than' uses a superlative with 'than'. "
  "The original uses 'from', so 'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "The news of her promotion **made her happily** for the whole week.",
  ["made her happy", "made happily her", "made her to be happily", NI], 0,
  "'Make + object + adjective': the adjective describes the object (made her happy)",
  "After 'make + object', the word that describes the object's state is an adjective, not an adverb: 'The news of "
  "her promotion made her happy for the whole week.'",
  ["Pattern: make + object + complement", "The complement describes 'her' → adjective", "'made her happy'"],
  "'Made happily her' and 'made her to be happily' keep the adverb and break the word order. The original uses the "
  "adverb 'happily', so 'No improvement required' is wrong.", 25, order=LAST_FIXED)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "The bank auctioned **a wooden large old cabinet** from its record room.",
  ["an old wooden large cabinet", "a large old wooden cabinet", "a wooden old large cabinet", NI], 1,
  "Order of adjectives before a noun: opinion, size, age, shape, colour, origin, material, purpose",
  "Size comes before age, and age before material: 'a large (size) old (age) wooden (material) cabinet'.",
  ["Size: large", "Age: old", "Material: wooden (closest to the noun)"],
  "The other orders put size after age or material before age, which breaks the normal order. The original puts "
  "the material first, so 'No improvement required' is wrong.", 35, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "**All what the auditor said** about the branch turned out to be true.",
  ["That all the auditor said", "All those the auditor said", "All that the auditor said", NI], 2,
  "After 'all' (and 'everything', 'anything'), the relative pronoun is 'that', not 'what'",
  "'What' already means 'the thing that', so it cannot follow 'all'. The correct form is 'All that the auditor said "
  "about the branch turned out to be true.'",
  ["'what' = 'the thing that'", "'all what' doubles the idea", "'all that' + clause"],
  "'That all the auditor said' turns the subject into a 'that' clause with no meaning. 'All those the auditor said' "
  "uses a plural pronoun with no noun for things said. 'All what' is wrong, so 'No improvement required' is "
  "wrong.", 40, order=LAST_FIXED)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "**The manager being on leave**, the meeting was postponed to Friday.",
  ["Being on leave", "The manager was on leave", "The manager having on leave", NI], 3,
  "Absolute phrase: a noun + participle phrase with its own subject, linked loosely to the main clause",
  "'The manager being on leave' has its own subject ('the manager'), so it does not need to share the subject of "
  "the main clause. It means 'Because the manager was on leave'. The sentence is correct.",
  ["The phrase has its own subject: 'the manager'", "Absolute phrase = 'because the manager was on leave'",
   "No improvement required"],
  "'Being on leave' without a subject would dangle, making the meeting the one on leave. 'The manager was on leave, "
  "the meeting was postponed' joins two clauses with only a comma. 'Having on leave' drops the verb 'been'.", 45,
  order=LAST_FIXED)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", I,
  PR_STEM + "The staff protest over the new shift timings **petered off** after the first week.",
  ["petered out", "petered down", "petered away", NR], 0,
  "Phrasal verb: peter out = gradually become weaker and then stop",
  "A protest that slowly lost strength and ended 'petered out'. 'Peter' is used only in this phrasal verb.",
  ["Meaning needed: faded away gradually", "Fixed form: peter out", "'petered out'"],
  "'Petered down', 'petered away' and 'petered off' are not idiomatic; the verb is used only with 'out', so 'No "
  "replacement required' does not apply.", 30, order=LAST_FIXED)

Q(PR, "Replace the phrase", A,
  PR_STEM + "**On the wake of** the fraud, the bank introduced a second signature for large withdrawals.",
  ["At the wake of", "In the wake of", "By the wake of", NR], 1,
  "Fixed expression: in the wake of = following, as a result of",
  "The bank acted after, and because of, the fraud. The fixed expression for this is 'in the wake of'.",
  ["Meaning: following, as a result of", "Fixed form: in the wake of", "'In the wake of'"],
  "'At', 'by' and 'on' are not used in this expression, so 'No replacement required' does not apply.", 30,
  order=LAST_FIXED)

Q(PR, "Replace the phrase", A,
  PR_STEM + "The officials behind the land scam will soon be **brought on book**.",
  ["brought by book", "brought in book", "brought to book", NR], 2,
  "Fixed expression: bring someone to book = punish them or make them answer for their actions",
  "Officials behind a scam who will be made to answer for it are 'brought to book'.",
  ["Meaning: made to answer for wrongdoing", "Fixed form: bring to book", "'brought to book'"],
  "'By book', 'in book' and 'on book' are not idiomatic, so 'No replacement required' does not apply.", 30,
  order=LAST_FIXED)

Q(PR, "Replace the phrase", A,
  PR_STEM + "Analysts expect the effect of the one-time tax refund on spending to **wear off** within a few months.",
  ["wear out", "wear on", "wear down", NR], 3,
  "Phrasal verbs with 'wear': wear off = gradually disappear (an effect, a feeling)",
  "The boost to spending from a one-time refund fades over time: it 'wears off'. The sentence is correct.",
  ["Subject: the effect of a refund", "Meaning needed: fade gradually", "'wear off' is correct"],
  "'Wear out' means become useless through long use (shoes, machines). 'Wear on' means pass slowly (as the day wore "
  "on). 'Wear down' means weaken someone's resistance. None means fade.", 30, order=LAST_FIXED)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", B, SC_OK,
  ["My uncle is engineer in a steel plant.",
   "My uncle is an engineer in steel plant.",
   "My uncle is a engineer in a steel plant.",
   "My uncle is an engineer in a steel plant."], 3,
  "A singular countable noun needs an article (a/an/the) or another determiner",
  "'Engineer' and 'plant' are singular countable nouns, so each needs an article. 'Engineer' begins with a vowel "
  "sound, so it takes 'an'.",
  ["'is engineer' → article missing", "'in steel plant' → article missing", "'a engineer' → 'an' before a vowel "
   "sound", "'an engineer in a steel plant': correct"],
  "The others leave out an article before 'engineer' or 'plant', or use 'a' before a vowel sound.", 25)

Q(SC, "Grammatically incorrect sentence", B, SC_BAD,
  ["We usually go shopping on Sunday evenings.",
   "He went for a walk after dinner.",
   "They went for shopping in the new mall.",
   "She goes swimming every morning."], 2,
  "'Go + -ing' for activities (go shopping, go swimming); 'go for + noun' (go for a walk)",
  "Activities such as shopping and swimming follow 'go' directly: 'They went shopping in the new mall.' 'Go for' is "
  "used with a noun such as 'a walk' or 'a swim'.",
  ["'go shopping': correct", "'went for a walk': noun after 'for': correct",
   "'went for shopping': 'for' + -ing activity: incorrect", "'goes swimming': correct"],
  "The other three follow the rule: 'go' + -ing activity, or 'go for' + a noun.", 25)

Q(SC, "Correct sentence", I, SC_OK,
  ["When I was a child, I would own a bicycle.",
   "When I was a child, I used to own a bicycle.",
   "When I was a child, I was used to own a bicycle.",
   "When I was a child, I use to own a bicycle."], 1,
  "'Used to' for past states and habits; 'would' only for repeated past actions, not states such as own, have, live",
  "Owning a bicycle is a state, not a repeated action, so 'would' cannot be used. 'Used to own' describes a past "
  "state that no longer exists.",
  ["'own' = a state", "'would' is for repeated actions → wrong here", "'was used to' = be accustomed to (+ -ing)",
   "'use to' needs '-d' in a positive sentence; 'used to own': correct"],
  "'Would own' uses 'would' with a state verb. 'Was used to own' confuses 'used to' with 'be used to' (be "
  "accustomed to). 'Use to own' drops the '-d'.", 35)

Q(SC, "Grammatically incorrect sentence", A, SC_BAD,
  ["Here comes the cashier with the keys.",
   "Here he comes with the keys.",
   "There goes the last bus to the depot.",
   "Here comes he with the keys."], 3,
  "After 'Here' or 'There' at the start, a noun subject follows the verb, but a pronoun subject comes before it",
  "With a noun subject, the verb comes first ('Here comes the cashier'). With a pronoun subject, there is no "
  "inversion: 'Here he comes', not 'Here comes he'.",
  ["'Here comes the cashier': noun subject, inverted: correct", "'Here he comes': pronoun, not inverted: correct",
   "'There goes the last bus': noun subject, inverted: correct", "'Here comes he': pronoun inverted: incorrect"],
  "The other three follow the rule: the noun subjects follow the verb and the pronoun 'he' comes before it.", 40)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) He watered the saplings every evening for years, even after his eyesight began to fail.\n"
  "(B) The neighbours laughed and asked why a man of his age was planting trees he would never see bear fruit.\n"
  "(C) At seventy, Hari Prasad dug ten pits behind his house and planted a mango sapling in each.\n"
  "(D) Last summer, his grandchildren picked the first full crop and shared it with the whole lane.\n"
  "(E) \"These trees are not for me,\" he replied, \"but for the children who will play under them.\"",
  ["CBEAD", "CEBAD", "BCEAD", "CBEDA"], 0,
  "Para jumble: named opener → reaction → reply → years of care → result",
  "C introduces Hari Prasad and the saplings. B gives the neighbours' question. E is his reply ('he replied'). A "
  "describes years of watering. D ('Last summer') gives the result.",
  ["Opener: C (names Hari Prasad)", "C → B: neighbours ask why", "B → E: 'he replied'",
   "E → A (years of watering) → D (first crop): CBEAD"],
  "CEBAD puts his reply before the question it answers. BCEAD opens with the neighbours laughing before anyone is "
  "introduced. CBEDA has the crop picked before the years of watering that produced it.", 40)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) The women of the Lakshmi self-help group meet on the first Sunday of every month under the banyan "
  "tree.\n"
  "(P) The treasurer counts the money and enters every amount in the group's register.\n"
  "(Q) Members who need a loan then explain their reasons, and the group decides together whom to lend to.\n"
  "(R) Each member first hands over her monthly saving of two hundred rupees to the treasurer.\n"
  "(S) Once the loans are agreed, the meeting closes with a reminder of the date for repayment.",
  ["RPQS", "RQPS", "PRQS", "RPSQ"], 0,
  "Fixed opener; process order marked by 'first', 'the money', 'then' and 'Once the loans are agreed'",
  "R ('first') begins the meeting with savings handed to the treasurer. P ('counts the money') follows. Q ('then') "
  "turns to loans. S ('Once the loans are agreed') closes the meeting.",
  ["(1) → R: savings handed over 'first'", "R → P: the treasurer counts 'the money'",
   "P → Q: 'then' loans are discussed", "Q → S: meeting closes: RPQS"],
  "RQPS discusses loans before the money is counted. PRQS counts 'the money' before any is handed over. RPSQ closes "
  "the meeting once loans are agreed before any loan is discussed.", 40)

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) The next week, the railway office received a letter of thanks, with the money for the ticket enclosed.\n"
  "(B) In a trembling voice, she explained that her purse, with the ticket inside, had been stolen at the station.\n"
  "(C) An elderly woman boarded the night train to Nagpur clutching a small cloth bag.\n"
  "(D) When the ticket examiner came round, she searched the bag in vain.\n"
  "(E) Seeing her distress, the examiner wrote out a fresh ticket and did not charge her a fine.",
  ["CDBEA", "CBDEA", "DCBEA", "CDBAE"], 0,
  "Para jumble: named opener → problem → explanation → response → later result",
  "C introduces the woman and her bag. D: she searches the bag in vain. B explains why (the purse was stolen). E: "
  "the examiner's kind response. A ('The next week') gives the result.",
  ["Opener: C", "C → D: 'the bag' searched in vain", "D → B: she explains the theft",
   "B → E ('her distress') → A ('The next week'): CDBEA"],
  "CBDEA has her explain the theft before the examiner arrives to ask for the ticket. DCBEA opens with 'she' before "
  "the woman is introduced. CDBAE puts the thank-you letter before the kindness it thanks.", 40)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) To reach them, a shopper must walk past long aisles of biscuits, snacks and soaps.\n"
  "(B) Milk, bread and eggs are among the items most households buy several times a week.\n"
  "(C) Many supermarkets therefore place them at the far end of the store.\n"
  "(D) Along the way, many shoppers pick up things they had not planned to buy.\n"
  "(E) A layout that looks inconvenient is, for the store, a carefully designed route to higher sales.",
  ["BCADE", "BACDE", "CBADE", "BCDAE"], 0,
  "Para jumble: fact → decision ('therefore') → consequence ('To reach them') → effect ('Along the way') → "
  "conclusion",
  "B gives the fact that these items are bought often. C ('therefore') gives the store's decision. A ('To reach "
  "them') describes the walk. D ('Along the way') gives what happens on it. E sums up the purpose.",
  ["Opener: B (the basic fact)", "B → C: 'therefore' placed at the far end", "C → A: 'To reach them'",
   "A → D ('Along the way') → E (conclusion): BCADE"],
  "BACDE has shoppers walking 'to reach them' before the store places them anywhere. CBADE opens with 'therefore' "
  "and 'them' before the items are named. BCDAE puts 'Along the way' before the walk is described.", 50)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) When a customer deposits a cheque drawn on another bank, the money does not reach her account at once.\n"
  "(P) Her bank first sends an image of the cheque through the clearing system to the bank on which it is drawn.\n"
  "(Q) If everything is in order, it confirms the payment; if not, the cheque is returned unpaid.\n"
  "(R) That bank checks whether the signature is genuine and whether the account holds enough money.\n"
  "(S) Only after this confirmation does her bank credit the amount to her account.",
  ["PRQS", "PQRS", "RPQS", "PRSQ"], 0,
  "Fixed opener; process order: 'first', 'That bank', 'If everything is in order', 'Only after this confirmation'",
  "P ('first') sends the cheque to the paying bank. R ('That bank') checks it. Q ('it confirms') gives the paying "
  "bank's decision. S ('Only after this confirmation') completes the process.",
  ["(1) → P: her bank 'first' sends the image", "P → R: 'That bank' checks", "R → Q: it confirms or returns",
   "Q → S: 'this confirmation' → credit: PRQS"],
  "PQRS has the payment confirmed before anything is checked. RPQS opens with 'That bank' before any other bank is "
  "mentioned. PRSQ refers to 'this confirmation' before the confirmation is described.", 50)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Ride-hailing apps do the same thing openly, raising fares when many riders want cars at once.\n"
  "(B) A street vendor who sells umbrellas often raises his price the moment the rain begins.\n"
  "(C) Supporters say that higher fares draw more drivers onto the roads, so that more riders get a car.\n"
  "(D) Critics reply that the rise falls hardest on people who have no other way to get home.\n"
  "(E) Buyers grumble, but they pay, because an umbrella is worth more to them in a downpour.",
  ["BEACD", "BAECD", "ABECD", "BEADC"], 0,
  "Para jumble: familiar example → its explanation → the same idea elsewhere ('the same thing') → defence → reply",
  "B gives the umbrella seller's price rise. E explains why buyers pay. A ('the same thing') extends the idea to "
  "ride-hailing apps. C gives the supporters' case and D the critics' reply.",
  ["Opener: B (the umbrella example)", "B → E: why buyers pay", "E → A: apps do 'the same thing'",
   "A → C (supporters) → D (critics 'reply'): BEACD"],
  "BAECD leaves the umbrella buyers' reaction until after the apps, breaking the example in two. ABECD opens with "
  "'the same thing' before anything has been described. BEADC puts the critics' reply before the supporters' "
  "argument.", 50)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) This counter-intuitive result, in which an extra road slows a network down, is known as Braess's "
  "paradox.\n"
  "(B) So many drivers took it that the roads leading to it became jammed, and average journeys grew longer.\n"
  "(C) City planners once built a road linking two congested highways, expecting it to spread traffic more "
  "evenly.\n"
  "(D) Some cities have since improved traffic flow by closing roads rather than building them.\n"
  "(E) The new link, however, appeared to offer every driver a shortcut.",
  ["CEBAD", "CBEAD", "ECBAD", "CEABD"], 0,
  "Para jumble: expectation → 'however' → consequence → name of the result ('This counter-intuitive result') → "
  "practical lesson",
  "C gives the plan and its expectation. E ('however') turns to what drivers saw. B ('took it') gives the jam. A "
  "('This counter-intuitive result') names it. D ('since') draws a practical lesson.",
  ["Opener: C (the plan)", "C → E: 'however', a shortcut for every driver", "E → B: so many took it",
   "B → A ('This ... result') → D ('since'): CEBAD"],
  "CBEAD has drivers take 'it' in a jam before the shortcut is explained. ECBAD opens with 'however' and 'The new "
  "link' before the road is introduced. CEABD names the result before the jam that is the result.", 60)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) In a market for second-hand cars, the seller usually knows far more about a car's condition than the "
  "buyer does.\n"
  "(P) Such a price is too low for the owner of a well-kept car but generous for the owner of a bad one.\n"
  "(Q) As they leave, the average quality of the cars on sale falls, and buyers lower their offers still further.\n"
  "(R) Unable to tell a sound car from a faulty one, buyers offer only an average price for any car.\n"
  "(S) Owners of good cars, unable to get a fair price, begin to withdraw from the market.",
  ["RPSQ", "RSPQ", "PRSQ", "RPQS"], 0,
  "Fixed opener; 'Such a price', 'Owners of good cars' and 'As they leave' as links",
  "R draws the consequence of (1): buyers offer an average price. P ('Such a price') explains who gains and who "
  "loses. S: owners of good cars withdraw. Q ('As they leave') gives the result, a falling average quality.",
  ["(1) → R: buyers cannot tell, so they offer an average price", "R → P: 'Such a price' is too low for good cars",
   "P → S: good owners withdraw", "S → Q: 'As they leave': RPSQ"],
  "RSPQ has owners withdraw before 'Such a price' explains why. PRSQ refers to 'Such a price' before any price is "
  "mentioned. RPQS uses 'As they leave' before anyone has begun to leave.", 60)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", B,
  SR_STEM + "(P) walked five kilometres\n(Q) the old farmer\n(R) to open a savings account\n(S) to the bank",
  ["QPSR", "QPRS", "PQSR", "QSRP"], 0,
  "Subject + verb + distance + destination ('to the bank') + purpose ('to open ...')",
  "'The old farmer walked five kilometres to the bank to open a savings account.' Subject (Q), verb and distance "
  "(P), destination (S), purpose (R).",
  ["Subject: Q", "Verb + distance: P", "Destination S, then purpose R → QPSR"],
  "QPRS gives 'open a savings account to the bank', which is not idiomatic. PQSR opens with a verb before its "
  "subject. QSRP puts 'to the bank' between the subject and its verb.", 30)

Q(SR, "Word/phrase rearrangement within a sentence", B,
  SR_STEM + "(P) too heavy\n(Q) the box of coins was\n(R) to lift\n(S) for the young clerk",
  ["QPSR", "QRPS", "QSPR", "PQRS"], 0,
  "'too + adjective + for + person + to-infinitive'",
  "'The box of coins was too heavy for the young clerk to lift.' After 'too heavy' (P), 'for the young clerk' (S) "
  "names who cannot lift it, and 'to lift' (R) completes the pattern.",
  ["Subject + verb: Q", "'too heavy': P", "'for the young clerk' S + 'to lift' R → QPSR"],
  "QRPS puts 'to lift' before 'too heavy'. QSPR puts 'for the young clerk' before 'too heavy'. PQRS opens with "
  "'too heavy' before the subject.", 30)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) please call\n(Q) should you need\n(R) the branch helpline\n(S) any help with the form",
  ["QSPR", "QPSR", "QSRP", "SQPR"], 0,
  "Inverted conditional with 'Should' (= If you need ...), then the main clause",
  "'Should you need any help with the form, please call the branch helpline.' 'Should you need' (Q) takes its "
  "object (S); the main clause (P + R) follows.",
  ["Condition: Q + S ('Should you need any help with the form')", "Main clause: P ('please call')",
   "Object of 'call': R → QSPR"],
  "QPSR puts 'please call' between 'need' and its object. QSRP puts the object of 'call' before the verb. SQPR "
  "opens with a noun phrase that has no verb.", 35)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The doctor told the old man to take his medicine ______, twice a day without missing a single dose.",
  ["rarely", "regularly", "secretly", "carelessly"], 1,
  "Single blank: the phrase after the comma defines the word",
  "'Twice a day without missing a single dose' describes taking medicine at fixed times without fail: regularly.",
  ["Clue: twice a day, never missing a dose", "Meaning: at fixed, steady intervals", "'regularly'"],
  "'Rarely' and 'carelessly' contradict 'without missing a single dose'. 'Secretly' has nothing to do with how "
  "often the medicine is taken.", 20)

Q(FB, "Double blank", B,
  FB2 + "The shopkeeper ______ the price of the rice because the customer ______ to buy ten bags at once.",
  ["raised, refused", "reduced, agreed", "reduced, refused", "hid, agreed"], 1,
  "Double blank: a bulk purchase earns a discount",
  "A customer who agrees to buy ten bags at once is usually given a lower price. The shopkeeper reduced the price "
  "because the customer agreed to buy in bulk.",
  ["Blank 2: buying ten bags at once → agreed", "A big order earns a discount", "Blank 1: reduced"],
  "Raising the price because a customer refused to buy is illogical. Reducing it because the customer refused gives "
  "no reason for a discount. 'Hid the price' makes no sense.", 25)

Q(FB, "Phrase fillers", B,
  FBP + "Whenever Meena comes across a new word in the newspaper, she ______ in her dictionary.",
  ["looks it up", "looks after it", "looks down on it", "looks forward to it"], 0,
  "Phrasal verb: look (something) up = search for information in a book or list",
  "Finding the meaning of a new word in a dictionary is 'looking it up'.",
  ["Object: a new word", "Action: find its meaning in a dictionary", "'looks it up'"],
  "'Look after' means take care of. 'Look down on' means think oneself better than. 'Look forward to' means wait "
  "eagerly for. None means search in a dictionary.", 25)

Q(FB, "Single blank", I,
  FB1 + "The two witnesses' accounts were so ______ that the inspector could not decide which of them to believe.",
  ["consistent", "contradictory", "detailed", "brief"], 1,
  "Single blank: the 'so ... that' result decides the word",
  "The inspector cannot decide whom to believe because the accounts disagree with each other: they are "
  "contradictory.",
  ["Result: cannot decide which account to believe", "Cause: the accounts disagree", "'contradictory'"],
  "Consistent accounts agree, so there would be nothing to decide between. 'Detailed' and 'brief' describe length, "
  "which does not explain the inspector's difficulty.", 30)

Q(FB, "Single blank", I,
  FB1 + "The landslide left the hill village ______ for three days, with no road or telephone link to the outside "
  "world.",
  ["congested", "prosperous", "isolated", "illuminated"], 2,
  "Single blank: the phrase after the comma defines the word",
  "A village with 'no road or telephone link to the outside world' is cut off from others: it is isolated.",
  ["Clue: no road or telephone link", "Meaning: cut off from others", "'isolated'"],
  "'Congested' (crowded with traffic) contradicts having no road. 'Prosperous' and 'illuminated' do not describe "
  "being cut off by a landslide.", 30)

Q(FB, "Single blank", I,
  FB1 + "On the advice of his ______, the accused chose not to answer any questions until the hearing.",
  ["council", "counsel", "consul", "console"], 1,
  "Confusable words: counsel (a lawyer; advice) vs council (an elected body) vs consul (a diplomat) vs console "
  "(comfort; a control panel)",
  "An accused person is advised by his lawyer, who is called his 'counsel'.",
  ["Who advises an accused person? His lawyer", "Lawyer = 'counsel'", "'counsel'"],
  "A 'council' is an elected or advisory body, a 'consul' is a diplomat posted abroad, and a 'console' is a control "
  "panel (or, as a verb, to comfort). None is an accused person's lawyer.", 30)

Q(FB, "Double blank", I,
  FB2 + "The new manager's ______ style, in which he sought every clerk's opinion before deciding, quickly won him "
  "the ______ of the staff.",
  ["autocratic, trust", "consultative, trust", "consultative, hostility", "arbitrary, respect"], 1,
  "Double blank: a relative clause defines the first word; the result decides the second",
  "Seeking everyone's opinion before deciding is a 'consultative' style. Such a style would earn the staff's "
  "'trust'.",
  ["Blank 1: sought every clerk's opinion → consultative", "Blank 2: a good style 'won him' something positive",
   "'consultative, trust'"],
  "'Autocratic' and 'arbitrary' (deciding alone or without reason) contradict asking everyone's opinion. "
  "'Consultative ... hostility' does not fit 'won him'.", 35)

Q(FB, "Double blank", I,
  FB2 + "Vegetable prices ______ after the floods cut off supplies, but they returned to normal once the roads were "
  "______.",
  ["soared, reopened", "slumped, reopened", "soared, blocked", "steadied, closed"], 0,
  "Double blank: cause and effect on both sides of 'but'",
  "When supplies are cut off, prices shoot up: they 'soared'. Prices return to normal when supplies resume, that is, "
  "when the roads are 'reopened'.",
  ["Blank 1: supplies cut off → prices soared", "'but ... returned to normal' → supplies came back",
   "Blank 2: roads reopened"],
  "'Slumped' (fell) does not follow from cut supplies. Prices would not return to normal once roads were 'blocked' "
  "or 'closed'.", 30)

Q(FB, "Double blank", I,
  FB2 + "The neighbour's evidence ______ the accused's claim that he was at home that night, and the court ______ "
  "him of the charge.",
  ["corroborated, acquitted", "contradicted, acquitted", "corroborated, convicted", "refuted, cleared"], 0,
  "Double blank: supporting evidence leads to a verdict of not guilty",
  "Evidence that 'corroborated' (confirmed) his alibi supports his innocence, so the court 'acquitted' him (found "
  "him not guilty).",
  ["Blank 1: evidence confirming the alibi → corroborated", "Supported alibi → not guilty",
   "Blank 2: acquitted (of the charge)"],
  "Evidence that 'contradicted' or 'refuted' the alibi would not lead to an acquittal or clearing. 'Convicted him "
  "of the charge' clashes with evidence that supported him.", 35)

Q(FB, "Phrase fillers", I,
  FBP + "The rumour that the bank was about to close ______ to be completely false.",
  ["turned up", "turned out", "turned in", "turned over"], 1,
  "Phrasal verbs with 'turn': turn out (to be) = prove to be in the end",
  "A rumour that is shown in the end to be false 'turned out to be' false.",
  ["Pattern: ___ to be completely false", "Meaning: proved to be in the end", "'turned out'"],
  "'Turned up' means arrived or appeared. 'Turned in' means handed over or went to bed. 'Turned over' means flipped "
  "or handed control. None is followed by 'to be' in this sense.", 25)

Q(FB, "Phrase fillers", I,
  FBP + "Doctors were not sure that the injured guard would ______ after the accident, but he is now back at work.",
  ["pull off", "pull through", "pull over", "pull out"], 1,
  "Phrasal verbs with 'pull': pull through = recover from a serious illness or injury",
  "The guard survived a serious injury and is back at work: he 'pulled through'.",
  ["Context: doctors unsure he would survive", "He is now back at work", "'pull through'"],
  "'Pull off' means succeed in something difficult. 'Pull over' means bring a vehicle to the side of the road. 'Pull "
  "out' means withdraw. None means recover.", 25)

Q(FB, "Single blank", A,
  FB1 + "The committee's ______ report, crammed with jargon and sentences that ran on for half a page, defeated even "
  "its most patient readers.",
  ["lucid", "terse", "turgid", "pithy"], 2,
  "Single blank: the participle phrase defines the word",
  "Writing 'crammed with jargon' and with very long sentences is pompous and hard to follow: 'turgid'.",
  ["Clue: jargon, sentences half a page long", "Effect: defeated patient readers", "'turgid' (overblown, hard to "
   "read)"],
  "'Lucid' means clear. 'Terse' and 'pithy' mean short and to the point, the opposite of sentences half a page "
  "long.", 35)

Q(FB, "Double blank", A,
  FB2 + "The once-______ start-up, which investors had valued at several billion dollars, is now ______, its "
  "founders accused of inflating its sales.",
  ["vaunted, thriving", "obscure, moribund", "vaunted, moribund", "humble, flourishing"], 2,
  "Double blank: 'once' and 'now' set a past high against a present low",
  "A firm valued at billions was once highly praised: 'vaunted'. With its founders accused of inflating sales, it is "
  "now close to collapse: 'moribund'.",
  ["'once-___' + valued at billions → vaunted (much praised)", "'now ___' + accused of fraud → moribund (dying)",
   "'vaunted, moribund'"],
  "'Thriving' and 'flourishing' do not fit a firm whose founders face fraud charges. 'Obscure' and 'humble' "
  "contradict a valuation of billions.", 40)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Correct usage of a word", I,
  "In which of the following sentences is the word 'imminent' used correctly?",
  ["He is an imminent economist who has advised three finance ministers.",
   "With dark clouds gathering over the hills, heavy rain seemed imminent.",
   "The bank's imminent founder was honoured with a statue in the town square.",
   "She played an imminent part in setting up the village cooperative."], 1,
  "Imminent (about to happen) vs eminent (famous and respected) vs prominent (important, noticeable)",
  "'Imminent' describes something about to happen. Rain that is about to fall when dark clouds gather is imminent.",
  ["A famous economist → 'eminent'", "Rain about to fall → 'imminent': correct",
   "A respected founder → 'eminent'", "An important part → 'prominent'"],
  "The other three describe people or roles that are famous or important, which needs 'eminent' or 'prominent', not "
  "'imminent'.", 30)

Q(WU, "Word swap", I,
  WS_STEM + "The **(A) auditor** found that the **(B) ledger** had copied the figures wrongly into the **(C) clerk**, "
  "so the **(D) report** was delayed.",
  ["A-D", "B-C", "A-B", "No swap required"], 1,
  "Word swap: check who can perform each action",
  "A ledger cannot copy figures, and figures are not copied into a clerk. Swapping B and C gives: 'The auditor found "
  "that the clerk had copied the figures wrongly into the ledger, so the report was delayed.'",
  ["'the ledger had copied' is impossible", "'into the clerk' is impossible", "Swap B and C"],
  "A-D gives 'The report found ... so the auditor was delayed', and the ledger still copies figures into a clerk. "
  "A-B gives 'The ledger found that the auditor had copied ... into the clerk'. The sentence clearly needs a swap.",
  35, order=FIXED)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'enervated' used correctly?",
  ["The coach's rousing speech enervated the team, and they won easily.",
   "Weeks of extreme heat enervated the workers, who could barely lift their tools.",
   "The good news enervated the staff, who cheered and danced in the hall.",
   "A strong cup of tea always enervates me before a long day at the counter."], 1,
  "Enervate = drain of energy, weaken (often misused as if it meant 'energise')",
  "'Enervate' means to weaken or exhaust. Heat that leaves workers barely able to lift their tools has enervated "
  "them.",
  ["A rousing speech that leads to a win → 'energised', not 'enervated'",
   "Heat that exhausts workers → 'enervated': correct", "Good news that makes people cheer → 'energised'",
   "Tea before a long day → 'energises' or 'revives'"],
  "The other three use 'enervate' as if it meant 'fill with energy', the opposite of its real meaning.", 35)

Q(WU, "Word swap", A,
  WS_STEM + "The **(A) lender** charged the **(B) borrower** a higher **(C) collateral** because he could not offer "
  "any **(D) interest rate**.",
  ["A-B", "C-D", "B-D", "No swap required"], 1,
  "Word swap: test each bold word in its slot using banking logic",
  "A lender charges an interest rate and asks for collateral as security. A borrower who cannot offer collateral is "
  "charged a higher interest rate. Swapping C and D gives: 'The lender charged the borrower a higher interest rate "
  "because he could not offer any collateral.'",
  ["Collateral is offered, not charged", "An interest rate is charged, not offered", "Swap C and D"],
  "A-B makes the borrower charge the lender and still has collateral being charged. B-D gives 'charged the interest "
  "rate a higher collateral', which is meaningless. The sentence clearly needs a swap.", 40, order=FIXED)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'vacate' as used in the sentence:\n"
  "'The tenants were asked to vacate the flat by the end of the month so that repairs could begin.'",
  ["rent", "leave", "clean", "decorate"], 1,
  "Vacate = leave a place empty, move out of it",
  "Repairs can begin only when nobody is living in the flat. To 'vacate' it is to move out and leave it empty.",
  ["Purpose: so that repairs could begin", "The flat must be empty", "'leave'"],
  "'Rent', 'clean' and 'decorate' do not empty the flat, which is what the repairs need.", 20)

Q(VO, "Word pairs", I, "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Lethargic – Energetic", "Benign – Harmless", "Arrogant – Humble", "Shallow – Profound"], 1,
  "Word pairs: identify synonyms and antonyms",
  "'Benign' means gentle and not harmful, so it is close in meaning to 'harmless'. The other pairs are opposites.",
  ["Lethargic (sluggish) ≠ energetic", "Benign = harmless", "Arrogant (proud) ≠ humble",
   "Shallow ≠ profound (deep)"],
  "The other three pairs are opposites, not synonyms.", 30)

Q(VO, "Contextual meaning", A,
  "Choose the meaning of the word 'pecuniary' as used in the sentence:\n"
  "'The officer was charged with using his position to obtain a pecuniary advantage for his brother's firm.'",
  ["political", "financial", "legal", "personal"], 1,
  "Pecuniary = relating to money",
  "Using a public position to gain something for a relative's firm is usually about money. 'Pecuniary' (from Latin "
  "'pecunia', money) means financial.",
  ["Context: an advantage for a business firm", "'pecuniary' = of money", "'financial'"],
  "'Political', 'legal' and 'personal' are other kinds of advantage; none is the meaning of 'pecuniary'.", 30)

Q(VO, "Word pairs", A, "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Pliable – Malleable", "Furtive – Stealthy", "Ebullient – Morose", "Erudite – Learned"], 2,
  "Word pairs: identify synonyms and antonyms",
  "'Ebullient' means cheerful and full of energy; 'morose' means gloomy and sullen. They are opposites. The other "
  "pairs are synonyms.",
  ["Pliable = malleable (easily bent or influenced)", "Furtive = stealthy (secretive)",
   "Ebullient (bubbling with cheer) ≠ morose (gloomy)", "Erudite = learned (scholarly)"],
  "The other three pairs are synonyms, not opposites.", 35)

Q(VO, "Contextual meaning", A,
  "Choose the meaning of the word 'desultory' as used in the sentence:\n"
  "'After a desultory search lasting barely ten minutes, the clerk declared that the file had been lost.'",
  ["thorough", "half-hearted", "secret", "urgent"], 1,
  "Desultory = lacking a plan, purpose or enthusiasm; half-hearted",
  "A search lasting 'barely ten minutes' before giving up was done without real effort: it was half-hearted.",
  ["Clue: barely ten minutes, then gave up", "Little effort or method", "'half-hearted'"],
  "'Thorough' is the opposite. 'Secret' and 'urgent' are not suggested by a short search followed by giving up.", 30)

Q(VO, "Word pairs", A, "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Prodigal – Economical", "Recondite – Obscure", "Fecund – Barren", "Adroit – Clumsy"], 1,
  "Word pairs: identify synonyms and antonyms",
  "'Recondite' means little known or hard to understand, which is close to 'obscure'. The other pairs are "
  "opposites.",
  ["Prodigal (wasteful) ≠ economical", "Recondite = obscure", "Fecund (fertile) ≠ barren",
   "Adroit (skilful) ≠ clumsy"],
  "The other three pairs are opposites, not synonyms.", 35)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", B,
  SY_STEM + "The branch manager always keeps his desk **tidy**, with every file in its proper place.",
  ["neat", "empty", "wooden", "crowded"], 0,
  "Tidy = neat and in order",
  "A desk with 'every file in its proper place' is neat and orderly.",
  ["Context: every file in its proper place", "'tidy' = orderly", "Closest: 'neat'"],
  "'Empty' contradicts the files on the desk. 'Crowded' suggests clutter. 'Wooden' describes the material, not the "
  "order.", 20)

Q(SY, "Contextual synonym", B,
  SY_STEM + "There has been a **rapid** rise in the number of people paying their bills by phone.",
  ["slight", "fast", "costly", "planned"], 1,
  "Rapid = happening quickly",
  "A 'rapid' rise is one that happens quickly: a fast rise.",
  ["Context: a rise in numbers", "'rapid' = quick", "Closest: 'fast'"],
  "'Slight' describes a small rise, not a quick one. 'Costly' and 'planned' do not describe speed.", 20)

Q(SY, "Contextual synonym", B,
  SY_STEM + "Workers handling **hazardous** chemicals at the factory must wear gloves and masks.",
  ["expensive", "foreign", "dangerous", "liquid"], 2,
  "Hazardous = risky, dangerous",
  "Chemicals that require gloves and masks are risky to handle: they are dangerous.",
  ["Clue: gloves and masks needed", "'hazardous' = involving danger", "Closest: 'dangerous'"],
  "'Expensive', 'foreign' and 'liquid' describe price, origin and form, not the danger that calls for protection.",
  20)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The family's savings began to **dwindle** after two bad harvests in a row.",
  ["shrink", "multiply", "stabilise", "circulate"], 0,
  "Dwindle = become gradually smaller",
  "After two bad harvests, the family must live on its savings, which gradually become smaller: they shrink.",
  ["Context: two bad harvests", "Savings are used up gradually", "Closest: 'shrink'"],
  "'Multiply' is the opposite. 'Stabilise' means stop changing. 'Circulate' means move around, not get smaller.", 25)

Q(SY, "Contextual synonym", I,
  SY_STEM + "The clerk gave a **plausible** explanation for the shortage, and the manager accepted it.",
  ["lengthy", "believable", "rude", "written"], 1,
  "Plausible = reasonable and likely to be true",
  "The manager accepted the explanation because it seemed reasonable and likely to be true: believable.",
  ["Clue: the manager accepted it", "'plausible' = seemingly true", "Closest: 'believable'"],
  "'Lengthy', 'rude' and 'written' describe length, manner or form, not whether the explanation could be believed.",
  25)

Q(SY, "Contextual synonym", A,
  SY_STEM + "Shareholders were angered by the board's **pusillanimous** response to the fraud: a mild warning to the "
  "officers involved.",
  ["decisive", "cowardly", "generous", "hasty"], 1,
  "Pusillanimous = lacking courage, timid",
  "Answering a fraud with only 'a mild warning' shows a lack of courage to act firmly. 'Pusillanimous' means "
  "cowardly.",
  ["Context: a fraud met with a mild warning", "The board lacked the courage to act", "Closest: 'cowardly'"],
  "'Decisive' is the opposite. 'Generous' and 'hasty' do not capture a fearful, weak response.", 30)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The path to the old temple is so **narrow** that two people cannot walk side by side.",
  ["steep", "wide", "short", "rough"], 1,
  "Narrow = small from side to side; antonym: wide",
  "A path too narrow for two people side by side is small in width. The opposite is 'wide'.",
  ["'narrow' = small in width", "Opposite: 'wide'"],
  "'Steep', 'short' and 'rough' describe slope, length and surface, not width.", 20)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The branch moved out of the **dilapidated** old building, whose roof leaked every monsoon.",
  ["crumbling", "run-down", "well-maintained", "ruined"], 2,
  "Dilapidated = in a bad condition because of age or neglect; antonym: well-maintained",
  "A building whose roof leaks every monsoon is falling apart from neglect. The opposite of 'dilapidated' is "
  "'well-maintained'.",
  ["'dilapidated' = falling to pieces through neglect", "Opposite: kept in good condition: 'well-maintained'"],
  "'Crumbling', 'run-down' and 'ruined' are all close in meaning to 'dilapidated'.", 25)

Q(AN, "Contextual antonym", I,
  AN_STEM + "A **prolific** writer, she published three novels and dozens of articles every year.",
  ["productive", "inventive", "unproductive", "famous"], 2,
  "Prolific = producing a great deal of work; antonym: unproductive",
  "Three novels and dozens of articles a year show great output. The opposite of 'prolific' is 'unproductive'.",
  ["'prolific' = producing much", "Opposite: producing little: 'unproductive'"],
  "'Productive' is a synonym. 'Inventive' and 'famous' describe originality and fame, not the amount produced.", 25)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "Losing the government contract proved **a blessing in disguise**: it forced the firm to find new customers "
  "abroad.",
  ["a misfortune that later proves useful", "a gift that is given secretly", "a sign of trouble to come",
   "a reward for honest work"], 0,
  "Idiom: a blessing in disguise = something that seems bad at first but turns out to be good",
  "Losing the contract seemed bad, but it pushed the firm to find customers abroad, which helped it. It was a "
  "blessing in disguise.",
  ["Event: loss of a contract (bad)", "Result: new customers abroad (good)", "Bad at first, good in the end"],
  "A secret gift reads 'disguise' literally. A sign of trouble reverses the meaning. Nothing in the sentence is a "
  "reward for honest work.", 25)

Q(ID, "Meaning of idiom", A,
  "Choose the meaning of the idiom 'to rest on one's laurels'.",
  ["to take a holiday after a period of hard work", "to be content with past success and stop trying",
   "to praise others for what they have achieved", "to retire from a job with full honours"], 1,
  "Idiom: rest on one's laurels = rely on past achievements instead of continuing to work",
  "Laurels were a symbol of victory. Someone who 'rests on his laurels' is satisfied with what he has already won and "
  "makes no further effort. For example: 'After last year's record profits, the bank cannot afford to rest on its "
  "laurels.'",
  ["Laurels = symbol of past victory", "Resting on them = making no further effort"],
  "A holiday after hard work is earned rest, not complacency. Praising others and retiring with honours are not what "
  "the idiom means.", 25)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", B, OW_STEM + "A person who cannot read or write",
  ["ignorant", "illiterate", "innocent", "amateur"], 1,
  "One-word substitution: education and ability",
  "An 'illiterate' person is one who cannot read or write.",
  ["Key idea: unable to read or write", "Word: illiterate"],
  "'Ignorant' means lacking knowledge in general. 'Innocent' means not guilty. An 'amateur' does something without "
  "being paid for it.", 20)

Q(OW, "Single word for a phrase", I,
  OW_STEM + "A document sent by a seller listing the goods supplied and the amount the buyer must pay",
  ["receipt", "voucher", "invoice", "ledger"], 2,
  "One-word substitution: business documents",
  "An 'invoice' lists the goods or services supplied and asks the buyer for payment.",
  ["Key idea: list of goods + amount to be paid", "Word: invoice"],
  "A 'receipt' confirms that payment has already been made. A 'voucher' is a document that can be exchanged for "
  "goods or that supports an entry in the accounts. A 'ledger' is a book of accounts.", 25)

Q(OW, "Single word for a phrase", A, OW_STEM + "A person who is very hard to please and attentive to small details",
  ["gregarious", "fastidious", "ambivalent", "complacent"], 1,
  "One-word substitution: personality types",
  "A 'fastidious' person is very particular, demands that everything be exactly right and is hard to please.",
  ["Key idea: hard to please, fussy about details", "Word: fastidious"],
  "'Gregarious' means fond of company. 'Ambivalent' means having mixed feelings. 'Complacent' means too satisfied "
  "with oneself to see a need for improvement.", 25)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", B, AP_STEM + "The postman delivers the letters every morning.",
  ["The letters were delivered by the postman every morning.",
   "The letters are delivered by the postman every morning.",
   "The letters are being delivered by the postman every morning.",
   "The letters is delivered by the postman every morning."], 1,
  "Simple present active → am/is/are + past participle",
  "The object 'the letters' becomes the subject. 'Delivers' (simple present) becomes 'are delivered' (plural "
  "subject), and the agent follows 'by'.",
  ["New subject: the letters (plural)", "Simple present passive: are + delivered", "Agent: by the postman"],
  "'Were delivered' changes the tense to the past. 'Are being delivered' is present continuous. 'Is delivered' does "
  "not agree with the plural 'letters'.", 25)

Q(AP, "Voice conversion", I, AP_STEM + "The bank gave him a loan of two lakh rupees.",
  ["He was given a loan of two lakh rupees by the bank.",
   "He has been given a loan of two lakh rupees by the bank.",
   "He was gave a loan of two lakh rupees by the bank.",
   "A loan of two lakh rupees was given by him to the bank."], 0,
  "Verbs with two objects: the indirect object (the person) can become the passive subject",
  "'Gave' has two objects: 'him' (the person) and 'a loan'. Making the person the subject gives 'He was given a loan "
  "of two lakh rupees by the bank.' The simple past stays simple past.",
  ["Indirect object 'him' → subject 'He'", "Simple past passive: was + given", "Direct object 'a loan' stays after "
   "the verb"],
  "'Has been given' changes the tense. 'Was gave' uses the past tense instead of the participle. 'Given by him to "
  "the bank' reverses who gave the loan to whom.", 30)

Q(AP, "Voice conversion", A, AP_STEM + "The contractors will have completed the new branch building by June.",
  ["The new branch building will be completed by the contractors by June.",
   "The new branch building would have been completed by the contractors by June.",
   "The new branch building will have completed by the contractors by June.",
   "The new branch building will have been completed by the contractors by June."], 3,
  "Future perfect active (will have + past participle) → will have been + past participle",
  "'Will have completed' is future perfect. Its passive keeps 'will have' and adds 'been' before the participle: "
  "'will have been completed'. 'By June' stays at the end.",
  ["New subject: the new branch building", "Future perfect passive: will have been + completed",
   "Agent: by the contractors; time: by June"],
  "'Will be completed' changes the tense to simple future. 'Would have been completed' is conditional. 'Will have "
  "completed' drops 'been' and is not passive.", 35)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", B, DS_STEM + "Meena says, \"I am tired of waiting in this queue.\"",
  ["Meena said that she was tired of waiting in that queue.",
   "Meena says that she is tired of waiting in this queue.",
   "Meena says that she was tired of waiting in that queue.",
   "Meena says that I am tired of waiting in this queue."], 1,
  "A reporting verb in the present tense ('says') does not change the tense of the reported words",
  "With 'says' (present), the tense stays as it is: 'am' remains 'is' after the pronoun change. 'I' becomes 'she'. "
  "She is still in the queue as she speaks, so 'this' can stay.",
  ["Reporting verb: 'says' (present) → no backshift", "'I am' → 'she is'", "'Meena says that she is tired ...'"],
  "'Said ... was' changes the reporting verb itself. 'Says ... was' backshifts after a present reporting verb. 'Says "
  "that I am' keeps the first person.", 25)

Q(DS, "Narration change", I,
  DS_STEM + "(Reported the next day) The clerk said, \"I can open the locker now.\"",
  ["The clerk said that he can open the locker then.",
   "The clerk said that he could open the locker now.",
   "The clerk told that he could open the locker then.",
   "The clerk said that he could open the locker then."], 3,
  "Backshift of modals (can → could) and time words (now → then) with a past reporting verb",
  "'Said' is past, so 'can' becomes 'could'. Reported the next day, 'now' becomes 'then'. 'I' becomes 'he'.",
  ["Past reporting verb → 'can' → 'could'", "Reported later → 'now' → 'then'", "'said that he could open the "
   "locker then'"],
  "'He can open ... then' keeps 'can'. 'Could open ... now' keeps 'now', which no longer fits a day later. 'Told "
  "that' needs an object ('told me that').", 30)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", I, SV_STEM + "Nobody except the two guards ______ allowed into the strongroom after dark.",
  ["are", "were", "is", "have"], 2,
  "A phrase beginning with 'except' (or 'but', meaning except) does not change the number of the subject",
  "The subject is 'Nobody', which is singular. 'Except the two guards' is an added phrase and does not make the "
  "subject plural: 'Nobody except the two guards is allowed ...'.",
  ["Subject: 'Nobody' (singular)", "'except the two guards' does not change it", "Present passive: 'is allowed'"],
  "'Are' and 'were' agree wrongly with 'guards'. 'Have allowed' would be active and needs a plural subject.", 30)

Q(SV, "Agreement rules", A,
  SV_STEM + "Suresh is the only one of the cashiers who ______ never made a single error in ten years.",
  ["have", "has", "are", "were"], 1,
  "'The only one of the + plural noun + who': the relative pronoun refers to 'the only one', so the verb is singular",
  "Only Suresh has never made an error, so 'who' refers to 'the only one' (Suresh), not to 'the cashiers'. The verb "
  "is singular: 'who has never made a single error'. (Compare 'one of those cashiers who have ...', where 'who' "
  "refers to the plural noun.)",
  ["Antecedent of 'who': 'the only one' (Suresh)", "Singular antecedent → singular verb",
   "Present perfect with 'never ... in ten years': 'has'"],
  "'Have' agrees wrongly with 'cashiers'. 'Are' and 'were' cannot be followed by 'made' to give the active present "
  "perfect.", 40)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Sequence of tenses", B, TE_STEM + "Listen! Someone ______ at the main door of the branch.",
  ["knocks", "is knocking", "knocked", "has knocked"], 1,
  "Present continuous for an action happening at the moment of speaking",
  "'Listen!' shows the action is going on right now, so the present continuous is needed: 'Someone is knocking at "
  "the main door.'",
  ["Signal: 'Listen!'", "Action happening now", "Present continuous: 'is knocking'"],
  "'Knocks' describes a habit. 'Knocked' is past. 'Has knocked' presents a completed action, which does not fit "
  "'Listen!'.", 20)

Q(TE, "Perfect tenses", I,
  TE_STEM + "\"Why are your hands so black with grease?\" \"I ______ the old generator all morning.\"",
  ["am repairing", "have been repairing", "had repaired", "repair"], 1,
  "Present perfect continuous for a recent, continuing activity whose result is visible now",
  "The greasy hands (present result) come from an activity that has been going on through the morning. This needs "
  "the present perfect continuous: 'I have been repairing the old generator all morning.'",
  ["Present evidence: greasy hands", "Activity over a period up to now: 'all morning'", "'have been repairing'"],
  "'Am repairing ... all morning' cannot take a duration up to now. 'Had repaired' refers to a time before another "
  "past event. 'Repair' describes a habit.", 30)

Q(TE, "Sequence of tenses", A,
  TE_STEM + "If the clerk were not so careless, he ______ the wrong account number yesterday.",
  ["would not enter", "would not have entered", "had not entered", "will not have entered"], 1,
  "Mixed conditional: a present unreal condition (were) with a past result (would have + past participle)",
  "'If the clerk were not so careless' describes his general, present character. 'Yesterday' puts the result in the "
  "past, so the main clause needs 'would have + past participle': 'he would not have entered the wrong account "
  "number yesterday'.",
  ["Condition: present, unreal ('were not so careless')", "Result: past ('yesterday')",
   "'would not have entered'"],
  "'Would not enter' describes a present or future result, which clashes with 'yesterday'. 'Had not entered' is the "
  "form of an 'if' clause, not a result. 'Will not have entered' is a real future form.", 40)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", B,
  AR_STEM + "______ patience is essential for anyone who deals with customers all day.",
  ["The", "A", "An", "No article"], 3,
  "Abstract nouns used in a general sense take no article",
  "'Patience' here means patience in general, not a particular patience, so it takes no article: 'Patience is "
  "essential for anyone who deals with customers all day.'",
  ["Noun: 'patience' (abstract, uncountable)", "Used in a general sense", "No article"],
  "'The patience' would refer to a particular patience already mentioned. 'A' and 'an' are not used with an "
  "uncountable abstract noun in this sense.", 20)

Q(AR, "Definite and indefinite", A,
  AR_STEM + "Many historians believe that ______ printing press did more to spread literacy than any other "
  "invention.",
  ["a", "the", "an", "no article"], 1,
  "Generic 'the' + singular countable noun to refer to an invention or type as a whole",
  "The sentence is about the printing press as an invention, not about one particular machine. A whole class or "
  "invention is referred to with 'the' + singular noun: 'the printing press'.",
  ["The noun names an invention as a whole", "Generic reference → 'the' + singular", "'the printing press'"],
  "'A printing press' would mean any single machine, which cannot have spread literacy more than other inventions. "
  "'An' does not fit the consonant sound of 'printing'. A singular countable noun cannot stand without an article.",
  35)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", B, PP_STEM + "She is very interested ______ learning how the share market works.",
  ["on", "at", "for", "in"], 3,
  "Fixed preposition: 'interested in'",
  "The adjective 'interested' takes 'in': 'She is very interested in learning how the share market works.'",
  ["Adjective: interested", "Fixed pairing: interested in", "'in'"],
  "'Interested on', 'interested at' and 'interested for' are not used.", 20)

Q(PP, "Fixed prepositions", B, PP_STEM + "This small town is famous ______ its handmade brass lamps.",
  ["by", "for", "with", "about"], 1,
  "Fixed preposition: 'famous for' (the thing that makes a place or person well known)",
  "A town that is well known because of its brass lamps is 'famous for' them.",
  ["Adjective: famous", "Reason it is known: its brass lamps", "'famous for'"],
  "'Famous by', 'famous with' and 'famous about' are not used for the reason something is well known.", 20)

Q(PP, "Fixed prepositions", I,
  PP_STEM + "Under the agreement, the courier company is liable ______ any loss of documents in transit.",
  ["for", "of", "with", "at"], 0,
  "Fixed preposition: 'liable for' = legally responsible for",
  "A company that must pay for documents lost in transit is legally responsible for the loss: 'liable for any loss'.",
  ["Meaning: legally responsible", "Fixed pairing: liable for", "'for'"],
  "'Liable of', 'liable with' and 'liable at' are not used. ('Liable to' means likely to or subject to, as in "
  "'liable to a fine', which is a different sense.)", 25)

Q(PP, "Phrasal verbs", I,
  PP_STEM + "Before the promotion interview, she decided to ______ her knowledge of foreign exchange rules.",
  ["brush up on", "brush off", "brush aside", "brush past"], 0,
  "Phrasal verb: brush up (on) = refresh one's knowledge of something learnt earlier",
  "Before an interview, a candidate refreshes what she already knows: she 'brushes up on' her knowledge.",
  ["Context: preparing for an interview", "Refresh earlier knowledge", "'brush up on'"],
  "'Brush off' and 'brush aside' mean dismiss or ignore. 'Brush past' means move quickly past someone, touching "
  "them. None means refresh knowledge.", 25)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"
CN_STEM = "Choose the connector that best fills the blank.\n"

Q(CN, "Sentence connectors", B, CN_STEM + "Leave now, ______ you will miss the last bus to the village.",
  ["or", "and", "but", "so"], 0,
  "'Or' after an instruction = otherwise (introduces what will happen if the instruction is not followed)",
  "Missing the bus is what happens if you do not leave now. 'Or' introduces this result: 'Leave now, or you will "
  "miss the last bus.'",
  ["Instruction: leave now", "Consequence of not leaving: miss the bus", "'or' (= otherwise)"],
  "'And' would mean that leaving now makes you miss the bus. 'But' signals a contrast that is not there. 'So' would "
  "make missing the bus the result of leaving.", 20)

Q(CN, "Sentence connectors", I,
  CN_STEM + "______ the new bridge over the river is open, villagers can reach the town in twenty minutes.",
  ["Even though", "Now that", "Unless", "In case"], 1,
  "'Now that' = because (something new) is now the case",
  "The bridge has just opened, and because of this the journey is now short. 'Now that' introduces a new situation "
  "as the reason.",
  ["Clause 1: the bridge is now open (new situation)", "Clause 2: a shorter journey (result)", "'Now that'"],
  "'Even though' signals a contrast. 'Unless' makes the open bridge a condition that blocks the result. 'In case' "
  "expresses a precaution.", 25)

Q(CN, "Sentence connectors", I,
  CN_STEM + "______ you pay in cash or by card, you will get a printed receipt for the bill.",
  ["Either", "Whether", "Unless", "Although"], 1,
  "'Whether ... or' = it makes no difference which (of the alternatives)",
  "The receipt is given in both cases, cash or card. 'Whether you pay in cash or by card' means 'it does not matter "
  "which'.",
  ["Two alternatives: cash, card", "Same result in both cases", "'Whether ... or'"],
  "'Either ... or' cannot begin a clause that leads into a main clause this way. 'Unless' makes no sense with two "
  "alternatives. 'Although' signals a contrast, but getting a receipt does not contrast with paying.", 30)

Q(CN, "Starters and linkers", A,
  "Combine the two sentences into one without changing the meaning, and choose the option that correctly begins the "
  "combined sentence.\n"
  "The bank cut its fees. It wanted to attract more young customers.",
  ["With a view to attract more young customers,", "In view of attracting more young customers,",
   "With a view to attracting more young customers,", "With a view of attract more young customers,"], 2,
  "'With a view to' (= with the aim of) is followed by a gerund, because 'to' here is a preposition",
  "'It wanted to attract more young customers' gives the bank's aim. 'With a view to attracting more young customers, the bank cut its "
  "fees.' The 'to' in 'with a view to' is a preposition, so the verb after it takes the -ing form.",
  ["Relation: 'It wanted to ...' is the purpose", "Purpose phrase: 'with a view to'", "Preposition 'to' + -ing: "
   "'attracting'"],
  "'With a view to attract' uses a base verb after the preposition 'to'. 'In view of' means 'considering', not 'with "
  "the aim of'. 'With a view of attract' changes the preposition and uses a base verb.", 35)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

# questions whose key was also recomputed by this script
RECOMPUTED = {(P6, 2)}
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


for seed in range(7007, 9000):
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

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_007_plan.json").read_text(encoding="utf-8"))
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

# no reused stem or passage title across the earlier English files (BATCH_000 to BATCH_006)
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
# BATCH_006 for this batch.
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
    "batch_id": "BATCH_007",
    "created_at": TODAY,
    "notes": "BATCH_007 English Language part: 150 original questions (BANK_ENG_000904 to BANK_ENG_001053). Six "
             "reading passages (36 questions) and three cloze passages (18 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 to BATCH_006; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules, words and idioms not tested in earlier batches. "
             "Each answer was set by the author and re-solved in a separate blind pass by fresh checkers without the "
             "key; the two loan-recovery figures in RC 6 are also recomputed by the builder. Pending human review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_007_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))}, seed {seed})")
