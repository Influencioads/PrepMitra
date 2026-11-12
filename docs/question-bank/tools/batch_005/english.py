"""Writes batches/parts/BATCH_005_ENG.json: the 150 English Language questions of BATCH_005.

All passages, sentences and items are original PrepMitra content. Passage themes were chosen to avoid every theme used
in BATCH_000 to BATCH_004, and the grammar rules, idioms and words tested are ones not tested in those batches (where
a grammar area was already covered, it is tested here through a different rule or a context-based item). Run from
anywhere:

    python docs/question-bank/tools/batch_005/english.py

Structural checks (quota per topic and difficulty, subtopics, ID range, passage length, set sizes, option count, cloze
blank numbering, 'No error' / 'No replacement' placement, para-jumble option validity, RC option-length spread,
repeated stems and passage titles against all earlier English files, answer-key balance) are asserted before anything
is written.
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
FIRST_ID = 604
FIRST_STIM = 5001
EARLIER = ("BATCH_000_sample.json", "parts/BATCH_001_ENG.json", "parts/BATCH_002_ENG.json",
           "parts/BATCH_003_ENG.json", "parts/BATCH_004_ENG.json")

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
P1 = stim("The lunch-box relay", (
    "Every working day in some large Indian cities, thousands of home-cooked lunches travel from kitchens in the "
    "suburbs to offices in the business district, and the empty boxes return home the same evening. The service is "
    "run not by a technology company but by a network of carriers, most of whom have little formal schooling. Yet the "
    "boxes almost never go missing.\n\n"
    "The secret lies in a simple system. Each box is marked with a short code of letters, numbers and colours painted "
    "on its lid. The code shows the station where the box is collected, the station where it is to be delivered, and "
    "the building and floor of the office. Carriers do not need to read addresses; they need only to recognise the "
    "marks. At every major station, boxes are sorted by code and handed from one team to the next, much like a baton "
    "in a relay race.\n\n"
    "Timing is just as important as sorting. The carriers depend on local trains, which run to a fixed timetable, and "
    "each team knows exactly which train it must catch. A delay of even a few minutes at one point can upset the whole "
    "chain, so carriers take great pride in being punctual. Many of them work in the same area for years and come to "
    "know their customers by sight.\n\n"
    "The system has drawn visitors from business schools and large companies, who come to study how such reliability "
    "is achieved without computers. What they often find is that the strength of the network lies less in its tools "
    "than in its people: a shared sense of duty, clear roles and a habit of helping a team-mate who falls behind.\n\n"
    "The service has had to adapt in recent years. Some customers now book through mobile apps, and food-delivery "
    "companies offer competition. Even so, many families still prefer to send food from their own kitchens, and the "
    "painted code on the lid continues to do its quiet work."))

Q(RC, "Factual", B,
  "According to the passage, what information does the code painted on each lunch box show?",
  ["The name of the cook and the time at which the food was made",
   "The price of the meal and the telephone number of the customer",
   "The collection station, the delivery station and the office location",
   "The name of the carrier and the number of the train he must take"], "C",
  "Locating a stated fact",
  "Paragraph 2 says the code 'shows the station where the box is collected, the station where it is to be delivered, "
  "and the building and floor of the office'.",
  ["Find 'The code shows' in paragraph 2", "Three items: collection station, delivery station, building and floor",
   "Option C"],
  "A, B and D list details the passage never says are in the code. D is tempting because trains are mentioned in "
  "paragraph 3, but the code describes the box's route, not the carrier or his train.", 45, P1, 1)

Q(RC, "Inference", B,
  "Why does the author compare the handling of the boxes to 'a baton in a relay race'?",
  ["Boxes are passed from one team to the next at each major station.",
   "Carriers often have to run hard to catch their trains on time.",
   "Teams compete with one another to deliver their boxes first.",
   "Each carrier takes his boxes the whole way from home to office."], "A",
  "Inference: what a comparison refers to",
  "The comparison comes right after the statement that boxes 'are sorted by code and handed from one team to the "
  "next'. In a relay race the baton is passed from one runner to the next; the boxes pass from team to team in the "
  "same way.",
  ["Read the clause the comparison is attached to", "Boxes are handed from one team to the next",
   "A baton passes from runner to runner: option A"],
  "B picks up the idea of running, but the comparison is attached to the handing over, not to catching trains. C "
  "invents a competition the passage never mentions. D contradicts the idea of passing the boxes on.", 45, P1, 2)

Q(RC, "Factual", B,
  "What do visitors from business schools and companies often find when they study the network?",
  ["Its success rests mainly on modern computers and tracking tools.",
   "Its strength lies more in its people and their habits than in tools.",
   "Its carriers are paid far more than most office workers in the city.",
   "It works only because local trains in the city are never late."], "B",
  "Locating a stated finding",
  "Paragraph 4 says visitors 'often find ... that the strength of the network lies less in its tools than in its "
  "people: a shared sense of duty, clear roles and a habit of helping a team-mate'.",
  ["Find 'What they often find' in paragraph 4", "Strength lies 'less in its tools than in its people'",
   "Option B"],
  "A contradicts 'without computers'. C is never mentioned. D goes too far: trains run to a timetable, but the "
  "passage says a delay can upset the chain, so it does not claim trains are never late.", 45, P1, 3)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'upset' as used in the passage ('A delay of even a few "
  "minutes at one point can upset the whole chain')?",
  ["sadden", "annoy", "disrupt", "worry"], "C",
  "Vocabulary in context: upset (a plan or system) = disturb its normal working",
  "A delay at one point throws the rest of the timetable out of order. 'Upset' here means disturb or disrupt the "
  "smooth working of the chain.",
  ["Subject: a delay; object: the whole chain (of hand-overs)", "Effect: the chain stops working smoothly",
   "'disrupt'"],
  "'Sadden', 'annoy' and 'worry' are the emotional senses of 'upset', used of people's feelings. A chain of "
  "deliveries has no feelings; a delay throws it out of order.", 35, P1, 4)

# ---------------------------------------------------------------- RC 2 (Basic 3 + Intermediate 2)
P2 = stim("The sleepy classroom", (
    "Teachers of early-morning classes know the scene well: rows of students yawning, heads resting on hands, eyes "
    "struggling to stay open. It is tempting to blame late-night phone use, and screens certainly play a part. But "
    "sleep scientists point to a deeper cause. During the teenage years, the body clock shifts, so that adolescents "
    "naturally begin to feel sleepy later at night than younger children or adults do. A fifteen-year-old who is sent "
    "to bed at nine may simply lie awake.\n\n"
    "This shift would matter little if teenagers could also wake later. Instead, many schools begin their day early, "
    "and long journeys mean that some students leave home before sunrise. The result is a steady loss of sleep through "
    "the week, which students try to recover by sleeping late on Saturdays and Sundays. Researchers call this pattern 'social jet "
    "lag', because the body is pushed back and forth as if it were crossing time zones every weekend.\n\n"
    "The costs go beyond yawning. Students who sleep too little find it harder to concentrate and to remember what "
    "they have learnt, and they are more likely to feel irritable or low. Tired teenagers are also more prone to "
    "accidents, especially on two-wheelers.\n\n"
    "A few schools in different countries have experimented with starting classes later in the morning, often by "
    "thirty to sixty minutes. Studies of such schools have generally found that students sleep longer, attend more "
    "regularly and arrive less tired, though the effect on examination results varies. The change is not easy to "
    "make: bus routes must be rearranged, parents' working hours must be considered, and sports and other activities "
    "may be pushed into the evening.\n\n"
    "Sleep experts do not claim that a later bell will solve every problem. Their point is narrower but important. A "
    "sleepy teenager is not necessarily lazy; he or she may be fighting biology. Schools that take this into account "
    "may find that the same lessons, taught an hour later, are better received."))

Q(RC, "Factual", B,
  "According to sleep scientists, what is the deeper cause of teenagers' sleepiness in early-morning classes?",
  ["Heavy meals eaten late in the evening just before going to bed",
   "Classrooms that are too warm and poorly lit early in the morning",
   "Homework that keeps most of them working until after midnight",
   "A shift in the body clock that delays their sleepiness at night"], "D",
  "Locating a stated cause",
  "Paragraph 1: 'sleep scientists point to a deeper cause. During the teenage years, the body clock shifts, so that "
  "adolescents naturally begin to feel sleepy later at night'.",
  ["Find 'a deeper cause' in paragraph 1", "Next sentence: the body clock shifts", "Option D"],
  "Meals (A), classrooms (B) and homework (C) are never mentioned. The only other cause named, phone use, is "
  "described as playing a part but not as the deeper cause.", 45, P2, 1)

Q(RC, "Factual", B,
  "Why do researchers call the pattern described in paragraph 2 'social jet lag'?",
  ["Students travel very long distances to reach their schools each day.",
   "Shifting sleep between weekdays and weekends is like crossing time zones.",
   "Teenagers stay up late talking to friends who live in other countries.",
   "School timetables in many places are set by the clocks of other nations."], "B",
  "Locating a stated reason",
  "Paragraph 2 explains the name: 'because the body is pushed back and forth as if it were crossing time zones every "
  "weekend' (short sleep on weekdays, long sleep on Sundays).",
  ["Find 'social jet lag' in paragraph 2", "Reason given: the body is pushed back and forth as if crossing time zones",
   "Option B"],
  "A picks up 'long journeys' but that is not the reason for the name. C and D are not mentioned.", 45, P2, 2)

Q(RC, "Vocabulary in context", B,
  "Which of the following is closest in meaning to the word 'prone' as used in the passage ('Tired teenagers are also "
  "more prone to accidents')?",
  ["lying face down", "protected from", "liable to suffer", "responsible for"], "C",
  "Vocabulary in context: prone to = likely to suffer from",
  "The sentence lists another cost of too little sleep. 'More prone to accidents' means more likely to have "
  "accidents.",
  ["Context: costs of lack of sleep", "'prone to' + something bad = likely to suffer it", "'liable to suffer'"],
  "'Lying face down' is the physical sense of 'prone', which does not take 'to accidents'. 'Protected from' is the "
  "opposite. 'Responsible for' would blame the teenagers for causing accidents, which the sentence does not say.",
  35, P2, 3)

Q(RC, "Inference", I,
  "Which of the following can be inferred from the passage about starting school later in the morning?",
  ["It guarantees better examination results for every student.",
   "It brings clear benefits but also some practical difficulties.",
   "It has been rejected by most sleep experts as impractical.",
   "It matters only for students who use their phones at night."], "B",
  "Inference: weighing benefits and costs stated in one paragraph",
  "Paragraph 4 lists benefits (longer sleep, better attendance, less tiredness) and then says 'The change is not easy "
  "to make', listing bus routes, parents' hours and activities. Both sides are stated.",
  ["Benefits: students sleep longer, attend more, arrive less tired", "Costs: bus routes, parents' hours, activities",
   "Both together: option B"],
  "A contradicts 'the effect on examination results varies'. C contradicts the experts' support in paragraph 5. D "
  "ignores the passage's main point that the cause is biological, not phone use.", 50, P2, 4)

Q(RC, "Tone and title", I,
  "Which of the following best describes the author's attitude towards sleepy teenagers?",
  ["critical, blaming them for wasting their nights on screens",
   "indifferent, treating their sleep as a private family matter",
   "alarmed, predicting a collapse in school standards",
   "understanding, seeing their tiredness as partly biological"], "D",
  "Tone: read the author's own conclusion",
  "The last paragraph says 'A sleepy teenager is not necessarily lazy; he or she may be fighting biology', and "
  "suggests schools take this into account. That is an understanding, sympathetic attitude.",
  ["Key line: 'not necessarily lazy ... fighting biology'", "The author defends rather than blames",
   "Option D"],
  "A contradicts the author, who says screens 'play a part' but points to a deeper cause. B is wrong because the "
  "author discusses what schools should do. C exaggerates: no collapse of standards is predicted.", 45, P2, 5)

# ---------------------------------------------------------------- RC 3 (Intermediate, 6)
P3 = stim("The magic of ninety-nine", (
    "Walk into almost any shop and you will see prices such as ₹199, ₹499 or ₹9,999. Few sellers choose these numbers "
    "by accident. A price that ends just below a round figure is known as a 'charm price', and retailers have used it "
    "for more than a century in the belief that it makes goods seem cheaper than they are.\n\n"
    "The belief is not entirely mistaken. Researchers who have studied shoppers' behaviour suggest that people tend to "
    "read a price from left to right and give most weight to the first digit. A price of ₹499 is therefore registered "
    "as 'four hundred and something' rather than as almost five hundred. The saving of a single rupee is trivial, but "
    "the impression of a lower price category can be strong, especially when a shopper is in a hurry or comparing "
    "many items at once.\n\n"
    "Charm prices also carry a message. Shoppers have learnt to associate them with discounts and bargains, so a price "
    "ending in 99 can signal value even when no discount is being offered. For the same reason, sellers of luxury "
    "goods often avoid them. A jeweller or a high-end restaurant is more likely to quote a round ₹5,000, which "
    "suggests quality and confidence rather than a hunt for bargains.\n\n"
    "The effect has limits. When buyers think carefully, as they do before purchasing a house or a car, the pull of "
    "the first digit weakens. Some studies have found little or no effect for certain products, and the results vary "
    "from one market to another. In addition, as digital payments replace cash, the practical nuisance of receiving "
    "small change has disappeared, which may alter how shoppers respond to odd prices.\n\n"
    "Still, the persistence of the ninety-nine suggests that sellers find it useful. It is a reminder that a price is "
    "not just a number but a piece of communication, and that buyers, however rational they believe themselves to be, "
    "read more into it than arithmetic alone would justify."))

Q(RC, "Factual", I,
  "According to the passage, why may a price of ₹499 seem much lower than ₹500 to a shopper?",
  ["Shoppers give the most weight to the first digit that they read.",
   "Shoppers carefully work out the value of saving a single rupee.",
   "Shops usually round such prices down further at the billing counter.",
   "Odd prices are printed in smaller type on most shop price tags."], "A",
  "Locating a stated explanation",
  "Paragraph 2: people 'read a price from left to right and give most weight to the first digit', so ₹499 is "
  "registered as 'four hundred and something'.",
  ["Find the explanation in paragraph 2", "Most weight on the first digit (4, not 5)", "Option A"],
  "B contradicts the passage, which calls the one-rupee saving 'trivial'. C and D are not mentioned.", 45, P3, 1)

Q(RC, "Inference", I,
  "Why, according to the passage, do sellers of luxury goods often avoid charm prices?",
  ["Luxury buyers always pay by card and dislike odd amounts.",
   "Charm prices suggest bargains rather than quality and confidence.",
   "The law requires costly items to be sold at round prices.",
   "Luxury goods are too expensive for the first-digit effect to work."], "B",
  "Inference: 'For the same reason' links back to the message charm prices carry",
  "Paragraph 3 says charm prices signal discounts and bargains, and 'For the same reason, sellers of luxury goods "
  "often avoid them'; a round price 'suggests quality and confidence rather than a hunt for bargains'.",
  ["Charm price = signal of a bargain", "Luxury sellers want to signal quality instead",
   "So they avoid charm prices: option B"],
  "A and C are never mentioned. D is plausible on its face but is not the reason given; the passage links the "
  "weakening of the first-digit effect to careful thinking, not to high prices as such.", 50, P3, 2)

Q(RC, "Factual", I,
  "In which situation does the passage say that the pull of the first digit weakens?",
  ["When the shop is offering a genuine discount on the item",
   "When buyers are in a hurry and comparing many items",
   "When buyers think carefully before a major purchase",
   "When the price is quoted as a round figure"], "C",
  "Locating a stated condition",
  "Paragraph 4: 'When buyers think carefully, as they do before purchasing a house or a car, the pull of the first "
  "digit weakens.'",
  ["Find 'weakens' in paragraph 4", "Condition: careful thinking before a big purchase", "Option C"],
  "B is the opposite: paragraph 2 says the effect is strong when shoppers are in a hurry. A and D are not given as "
  "conditions that weaken the effect.", 40, P3, 3)

Q(RC, "Inference", I,
  "What change does the author connect with the spread of digital payments?",
  ["Shoppers paying by phone may stop noticing the first digit.",
   "Card fees may push sellers towards round prices on all goods.",
   "Odd prices may soon be barred for payments made through apps.",
   "With no coins to handle, reactions to odd prices could shift."], "D",
  "Inference: reading a cautious claim exactly",
  "Paragraph 4: 'as digital payments replace cash, the practical nuisance of receiving small change has disappeared, "
  "which may alter how shoppers respond to odd prices.'",
  ["Find 'digital payments' in paragraph 4", "Effect: the nuisance of small change has gone",
   "Possible result: responses to odd prices may change: option D"],
  "A, B and C are cautious-sounding guesses that the passage never makes: it links digital payments only to the "
  "disappearance of the small-change nuisance, not to the first digit, card fees or any ban.", 45, P3, 4)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'persistence' as used in the passage ('the persistence "
  "of the ninety-nine suggests that sellers find it useful')?",
  ["sudden return", "gradual decline", "continued existence", "stubborn insistence"], "C",
  "Vocabulary in context: persistence (of a practice) = its continuing to exist",
  "The charm price has been used 'for more than a century' and is still everywhere. Its persistence is its continued "
  "existence over a long time, which suggests sellers find it useful.",
  ["Context: a pricing habit used for over a century", "'persistence' = continuing to exist",
   "'continued existence'"],
  "'Sudden return' and 'gradual decline' contradict a practice that has never gone away. 'Stubborn insistence' is "
  "the sense used of a person who keeps demanding something, not of a pricing habit.", 40, P3, 5)

Q(RC, "Tone and title", I,
  "Which of the following best states the main idea of the passage?",
  ["Prices carry messages that sway buyers beyond simple arithmetic.",
   "Charm prices fool every shopper and ought to be banned by law.",
   "Luxury sellers earn more than shops that rely on odd prices.",
   "Digital payments have made the psychology of pricing irrelevant."], "A",
  "Main idea: the author's conclusion in the last paragraph",
  "The passage explains how charm prices work, what they signal and where the effect weakens, and concludes that 'a "
  "price is not just a number but a piece of communication' that buyers read more into than arithmetic justifies.",
  ["Paras 1–3: how and why charm prices work", "Para 4: limits of the effect",
   "Para 5: a price is communication: option A"],
  "B overstates ('every shopper') and invents a call for a ban. C is never compared. D contradicts the passage, which "
  "says digital payments 'may alter' responses, not that pricing psychology no longer matters.", 45, P3, 6)

# ---------------------------------------------------------------- RC 4 (Intermediate, 6)
P4 = stim("A garden plant gone wild", (
    "In the nineteenth century, a flowering shrub from Central and South America was brought to India as an "
    "ornamental plant for gardens. Its small, bright flowers made it popular, and it was later planted along fences "
    "and railway lines as a hedge. Today that shrub, lantana, covers vast areas of Indian forests, and ecologists "
    "count it among the most troublesome invasive plants in the country.\n\n"
    "Lantana spreads with remarkable ease. Birds eat its berries and scatter the seeds widely, and the plant grows "
    "quickly in open, disturbed ground, such as the edges of roads or patches cleared by fire. Once established, it "
    "forms dense thickets that shade out the grasses and young trees beneath. Because most animals avoid eating its "
    "leaves, which are toxic to livestock, there is little to keep it in check.\n\n"
    "The consequences reach well beyond the plants it smothers. Grazing animals such as deer find less to eat where "
    "lantana dominates, and the predators that depend on them may follow them elsewhere. Villagers who once collected "
    "fodder, fuel and medicinal herbs from the forest floor find these resources harder to reach. The thickets can "
    "also feed forest fires, since the dry stems burn readily.\n\n"
    "Removing lantana has proved difficult. Cutting it back without digging out the roots often leads to vigorous "
    "regrowth, and cleared ground is quickly reinvaded unless native grasses are planted at once. Some forest "
    "departments have therefore adopted a method in which each plant is uprooted at the base and the area is restored "
    "with local species, but the work is slow and labour-intensive.\n\n"
    "A few communities have found an unexpected use for the plant. Its tough, flexible stems can be woven into "
    "furniture and baskets, and craftspeople trained in this work earn an income while helping to clear the forest. "
    "Such efforts cannot remove lantana on their own, given the scale of the problem, but they turn a burden into a "
    "modest resource and give local people a reason to keep up the fight."))

Q(RC, "Factual", I,
  "Why, according to the passage, was lantana first brought to India?",
  ["To feed cattle during the dry months", "To provide stems for weaving furniture",
   "To decorate gardens with its bright flowers", "To shield railway lines from forest fires"], "C",
  "Locating a stated fact",
  "Paragraph 1: the shrub 'was brought to India as an ornamental plant for gardens', and 'Its small, bright flowers "
  "made it popular'.",
  ["Find 'brought to India' in paragraph 1", "Purpose: an ornamental plant for gardens", "Option C"],
  "A contradicts the passage: the leaves are toxic to livestock. B describes a much later use found by a few "
  "communities. D twists the later hedge planting along railway lines; the passage links the stems to feeding fires, "
  "not preventing them.", 40, P4, 1)

Q(RC, "Factual", I,
  "Which of the following is NOT given in the passage as a reason why lantana spreads so easily?",
  ["Birds eat its berries and scatter the seeds widely.",
   "It grows quickly in open and disturbed ground.",
   "Most animals avoid eating its toxic leaves.",
   "Its roots release chemicals that kill nearby plants."], "D",
  "Factual (NOT) question: eliminate every option the passage states",
  "Paragraph 2 gives three reasons: birds scatter the seeds, it grows fast in disturbed ground, and animals avoid its "
  "toxic leaves so nothing keeps it in check. Chemicals from the roots are never mentioned.",
  ["Birds scatter seeds: stated (A)", "Fast growth in disturbed ground: stated (B)",
   "Animals avoid the leaves: stated (C)", "Root chemicals: not in the passage: D"],
  "A, B and C are all stated in paragraph 2, so none of them can be the answer. D may sound scientific, but the "
  "question asks what the passage gives, and it does not mention root chemicals.", 45, P4, 2)

Q(RC, "Inference", I,
  "Why, according to the passage, may predators leave areas where lantana dominates?",
  ["Their prey, such as deer, find less to eat there and move away.",
   "The toxic leaves poison the predators that pass through the thickets.",
   "Villagers clearing the thickets drive the predators out of the area.",
   "Fires that start in lantana patches destroy the predators' dens."], "A",
  "Inference: following a chain of cause and effect",
  "Paragraph 3: deer 'find less to eat where lantana dominates, and the predators that depend on them may follow them "
  "elsewhere'. The predators move because their prey moves.",
  ["Lantana → less food for deer", "Deer move elsewhere", "Predators that depend on deer follow: option A"],
  "B wrongly applies the toxicity to predators; the passage says the leaves are toxic to livestock that might eat "
  "them. C and D are not given as reasons for predators leaving.", 45, P4, 3)

Q(RC, "Inference", I,
  "What does the passage suggest about cutting lantana back without digging out its roots?",
  ["It is the quickest way to get rid of the plant for good.",
   "It often lets the problem return, sometimes more strongly.",
   "It is the method most forest departments now recommend.",
   "It allows native grasses to spread back on their own."], "B",
  "Inference: reading the meaning of 'vigorous regrowth'",
  "Paragraph 4: 'Cutting it back without digging out the roots often leads to vigorous regrowth.' Vigorous regrowth "
  "means the plant comes back strongly, so the problem returns.",
  ["Find 'without digging out the roots' in paragraph 4", "Result: vigorous (strong) regrowth",
   "The problem returns: option B"],
  "A contradicts the regrowth. C is wrong: departments have adopted uprooting at the base instead. D contradicts the "
  "statement that cleared ground is quickly reinvaded unless native grasses are planted.", 45, P4, 4)

Q(RC, "Vocabulary in context", I,
  "Which of the following is closest in meaning to the word 'smothers' as used in the passage ('The consequences "
  "reach well beyond the plants it smothers')?",
  ["shelters", "overwhelms by covering", "feeds upon", "replaces gradually"], "B",
  "Vocabulary in context: smother = cover something so completely that it cannot live or grow",
  "Paragraph 2 says lantana forms dense thickets that 'shade out the grasses and young trees beneath'. The plants it "
  "smothers are the ones it covers and kills in this way.",
  ["Link back: thickets that shade out grasses and young trees", "'smother' = cover and stifle",
   "'overwhelms by covering'"],
  "'Shelters' turns covering into protection, the opposite of the effect described. 'Feeds upon' wrongly makes "
  "lantana a parasite. 'Replaces gradually' misses the idea of covering and stifling.", 40, P4, 5)

Q(RC, "Tone and title", I,
  "How does the author view the communities that make furniture and baskets from lantana?",
  ["Their work will soon remove lantana from Indian forests altogether.",
   "Their work wastes effort that should go into proper removal.",
   "Their work is a useful but limited response to a large problem.",
   "Their work harms the forest by encouraging people to plant lantana."], "C",
  "Author's view: a balanced 'cannot ... but ...' judgement",
  "The last paragraph says 'Such efforts cannot remove lantana on their own, given the scale of the problem, but they "
  "turn a burden into a modest resource and give local people a reason to keep up the fight.'",
  ["Limitation: cannot remove lantana on their own", "Value: a modest resource and a reason to keep fighting",
   "Useful but limited: option C"],
  "A contradicts 'cannot remove lantana on their own'. B and D are criticisms the author never makes; the author "
  "presents the work positively.", 45, P4, 6)

# ---------------------------------------------------------------- RC 5 (Advanced, 4)
P5 = stim("Money already spent", (
    "Suppose you have paid in advance for a concert ticket, and on the evening of the show you feel unwell and the "
    "rain is pouring down. Many people would go anyway, reasoning that they cannot let the money go to waste. Yet the "
    "money is gone whether they go or not. The only question that remains is whether the evening will be better spent "
    "at the concert or at home. Economists call money that has already been spent and cannot be recovered a 'sunk "
    "cost', and they argue that it should play no part in decisions about the future.\n\n"
    "The advice is simple to state and remarkably hard to follow. People dislike admitting that an earlier choice was "
    "a mistake, and abandoning a project can feel like confirming that the resources put into it were wasted. So they "
    "continue, sometimes adding more money in the hope of rescuing what has already been spent. Psychologists have "
    "found this tendency in individuals, in companies and in governments, and it tends to grow stronger when the "
    "person who made the original decision is also the one deciding whether to continue.\n\n"
    "Large organisations offer the most expensive examples. A half-built project may consume further funds for years "
    "because stopping it would mean writing off the amount already invested and accepting blame for the original "
    "plan. Officials may describe the extra spending as 'protecting the investment', a phrase that quietly shifts "
    "attention from future returns to past costs.\n\n"
    "Not every decision to persist is irrational, however. Sometimes the money already spent has bought something of "
    "real value, such as a nearly finished building, a skilled team or knowledge gained through trial and error, that "
    "makes completing the project cheaper than starting something new. In such cases, continuing is justified not by "
    "the past spending itself but by what it has produced. The difficulty lies in telling the two situations apart "
    "honestly.\n\n"
    "Some institutions try to do this by separating roles: the people who review a troubled project are not the ones "
    "who proposed it. Others set conditions in advance, agreeing at the outset on the point at which a venture will "
    "be abandoned. Neither method is foolproof, but both rest on the same insight: the past should inform our "
    "judgement of the future, not hold it hostage."))

Q(RC, "Inference", A,
  "According to the passage, which of the following people is most likely to be caught in the sunk-cost trap?",
  ["An outside reviewer asked to assess a project for the first time",
   "A manager deciding whether to continue a project he once proposed",
   "An investor who agreed in advance on when to abandon a venture",
   "A buyer who has not yet paid anything for the item in question"], "B",
  "Inference: applying the condition under which the tendency grows stronger",
  "Paragraph 2: the tendency 'tends to grow stronger when the person who made the original decision is also the one "
  "deciding whether to continue'. The manager who proposed the project fits exactly.",
  ["Condition: the original decision-maker also decides whether to continue", "Manager who proposed it: fits",
   "Option B"],
  "A and C describe the two safeguards in paragraph 5 (separate reviewers, conditions set in advance), which reduce "
  "the trap. D has no sunk cost at all, since nothing has been spent.", 60, P5, 1)

Q(RC, "Inference", A,
  "What is the author's view of the phrase 'protecting the investment' as officials use it?",
  ["It accurately describes the real purpose of most extra spending.",
   "It is the technical term that economists use for sunk costs.",
   "It subtly moves attention from future returns to past spending.",
   "It is used only by private companies and never by governments."], "C",
  "Inference: the author's comment on a quoted phrase",
  "Paragraph 3 calls it 'a phrase that quietly shifts attention from future returns to past costs'. The author sees "
  "it as a subtle distortion, not an accurate description.",
  ["Find the phrase in paragraph 3", "Author's comment: it 'quietly shifts attention' to past costs",
   "Option C"],
  "A contradicts the author's critical comment. B confuses it with 'sunk cost', the economists' term in paragraph 1. "
  "D is unsupported; officials of 'large organisations' generally are meant, and governments are named in "
  "paragraph 2.", 55, P5, 2)

Q(RC, "Inference", A,
  "Which of the following would the author regard as a justified reason for continuing a project?",
  ["Going on because so much has already been spent on it",
   "Going on so that the planner escapes blame for the plan",
   "Going on because stopping would admit the plan was wrong",
   "Going on because finishing now costs less than starting anew"], "D",
  "Inference: distinguishing what past spending produced from the spending itself",
  "Paragraph 4: continuing is justified 'not by the past spending itself but by what it has produced', for example a "
  "nearly finished building 'that makes completing the project cheaper than starting something new'.",
  ["Justified: what the spending produced lowers the cost of finishing", "Not justified: the spending itself, blame, "
   "pride", "Option D"],
  "A is the sunk-cost reasoning the passage rejects. B and C are the motives of avoiding blame and not admitting a "
  "mistake, which paragraphs 2 and 3 describe as the cause of the trap.", 60, P5, 3)

Q(RC, "Vocabulary in context", A,
  "What does the author mean by saying that the past should not 'hold it hostage' (the judgement of the future)?",
  ["The past should not keep our judgement captive and dictate its choices.",
   "The past should not shield our judgement from outside dangers.",
   "The past should not make our judgement of the future more predictable.",
   "The past should not delay our judgement until a price has been paid."], "A",
  "Figurative language: to hold something hostage = to keep it captive and control what it can do",
  "A hostage is held captive and forced to act on the captor's terms. The author means past spending should inform "
  "decisions but must not control them, which is the sunk-cost trap the passage describes.",
  ["Literal: a captor controls a hostage", "Figurative: past costs controlling future decisions",
   "Contrast with 'inform': option A"],
  "B reverses the image: a hostage-taker does not protect. C has no link with the image. D takes the ransom idea "
  "literally and misses the point about control.", 50, P5, 4)

# ---------------------------------------------------------------- RC 6 (Advanced, 4)
P6 = stim("The pull of the crowd", (
    "A telephone is useless to the first person who owns one; its value comes entirely from the number of other "
    "people one can call. Economists call this a 'network effect': a product or service becomes more valuable to each "
    "user as more people use it. Messaging apps, online marketplaces and even languages share this property, and it "
    "shapes competition in ways that ordinary products do not.\n\n"
    "When network effects are strong, early leads tend to grow. A marketplace with many sellers attracts more buyers, "
    "whose presence draws still more sellers. A rival with a better design may struggle to break in, because a "
    "customer who switches gives up access to everyone who stays behind. Markets of this kind often tip towards one "
    "or two dominant firms, not necessarily because those firms offer the best product but because they reached a "
    "large size first.\n\n"
    "For users, the outcome is mixed. A single dominant network is convenient: everyone can reach everyone else, and "
    "there is no need to juggle several accounts. But a firm that knows its customers cannot easily leave has less "
    "reason to keep prices low or to listen to complaints. It may raise the fees it charges to sellers, change its "
    "rules without warning or neglect the privacy of its users, confident that few will walk away.\n\n"
    "Regulators have experimented with several responses. One is to require 'interoperability', so that the users of "
    "one service can communicate or trade with the users of another, much as subscribers of different mobile "
    "operators can call one another. Another is to let users carry their data, such as contacts or ratings, when "
    "they move to a competitor, which lowers the cost of switching. A third is to build a shared platform on which "
    "many firms compete, so that the network itself belongs to no single company.\n\n"
    "None of these remedies is free of difficulty. Interoperability can be technically complex and may weaken "
    "security if it is designed carelessly, and forcing a network open may reduce the reward for building one in the "
    "first place. The challenge is to keep the benefits of a large network, which are real, while preventing its "
    "owner from turning those benefits into a toll that users have no choice but to pay."))

Q(RC, "Inference", A,
  "Why, according to the passage, may a rival with a better design fail to win customers from a dominant network?",
  ["Customers who switch lose access to everyone who stays on the larger network.",
   "Better-designed services usually cost far more than the market leader's.",
   "Regulators often bar new firms from entering markets that have tipped.",
   "Users rarely notice any difference in design between rival services."], "A",
  "Inference: the cost of switching in a network market",
  "Paragraph 2: a better-designed rival 'may struggle to break in, because a customer who switches gives up access to "
  "everyone who stays behind'. The value of the network, not the design, keeps customers in place.",
  ["Find 'A rival with a better design' in paragraph 2", "Reason: switching means losing everyone who stays",
   "Option A"],
  "B and D are never stated. C contradicts the passage, where regulators try to make switching easier, not to keep "
  "rivals out.", 55, P6, 1)

Q(RC, "Inference", A,
  "Which of the following is the closest example of a 'network effect' as the passage defines it?",
  ["A bakery's bread improves after it installs a modern oven.",
   "A shop lowers its prices because it buys its flour in bulk.",
   "A video-calling app grows more useful as more relatives join it.",
   "A car becomes cheaper to run when the price of fuel falls."], "C",
  "Applying a defined term to a new case",
  "A network effect exists when 'a product or service becomes more valuable to each user as more people use it'. A "
  "video-calling app is worth more to each user as more of the people he wants to call join it.",
  ["Definition: value to each user rises with the number of users", "Test each option against it",
   "Only the video-calling app fits: option C"],
  "A is an improvement in the product itself. B is a cost saving from buying in bulk (economies of scale), which "
  "lowers the price but does not make the product more valuable as more people use it. D is a change in running "
  "costs. None depends on the number of other users.", 55, P6, 2)

Q(RC, "Tone and title", A,
  "Which of the following best describes the author's attitude towards dominant networks?",
  ["admiring, since dominance proves that the best product has won",
   "hostile, since large networks bring users no real benefit",
   "indifferent, since users can always move to a rival",
   "balanced, valuing their convenience but wary of their power"], "D",
  "Tone: weighing the author's praise and criticism",
  "The author calls the outcome for users 'mixed': a dominant network is 'convenient', and its benefits 'are real', "
  "but a firm whose customers cannot leave may raise fees, change rules or neglect privacy.",
  ["Praise: convenient; benefits 'are real'", "Concern: power over customers who cannot leave",
   "Balanced: option D"],
  "A contradicts 'not necessarily because those firms offer the best product'. B contradicts 'which are real'. C "
  "contradicts the point that customers 'cannot easily leave'.", 50, P6, 3)

Q(RC, "Factual", A,
  "According to the passage, how does letting users carry their data to a competitor help them?",
  ["It makes the dominant network's own services more secure.",
   "It lowers the cost to users of switching to a rival service.",
   "It allows regulators to fix the fees charged to sellers.",
   "It ensures that the network belongs to no single company."], "B",
  "Locating a stated effect",
  "Paragraph 4: letting users carry their data, such as contacts or ratings, to a competitor 'lowers the cost of "
  "switching'.",
  ["Find 'carry their data' in paragraph 4", "Stated effect: lowers the cost of switching", "Option B"],
  "A reverses the passage, which warns that careless interoperability may weaken security. C is not mentioned. D "
  "describes the third remedy, a shared platform, not data portability.", 50, P6, 4)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used: '{ctx}'. Choose the word that should "
            "replace it to make the sentence grammatically correct and meaningful. If the word is correct as it "
            "stands, choose 'No replacement required'.")
NR = "No replacement required"

# ---------------------------------------------------------------- Cloze 1 (Basic, 6)
C1 = stim("Keepers of the light", (
    "For centuries, lighthouses have warned ships away from rocks and shallow water. Before modern navigation "
    "equipment, a sailor approaching the coast at night (1) ______ on these lights to know where he was. Each "
    "lighthouse flashes in its own pattern, so that an experienced crew can tell one from another.\n\n"
    "Running a lighthouse was once a demanding job. Keepers lived at the station with their families, often on a "
    "lonely headland or a small island. They climbed the tower every evening to light the lamp, cleaned the glass so "
    "that the beam would not be (2) ______, and kept watch through the night. In stormy weather, they could not leave "
    "their post even for a short while.\n\n"
    "Over the last few decades, most lighthouses have been (3) ______. Electric lamps now switch on by themselves at "
    "dusk, and faults are reported to a distant control room. Satellite navigation has also made the lights far less "
    "(4) ______ than they once were. As a result, the old job of the keeper has almost disappeared.\n\n"
    "The towers themselves, however, have found new life. Several have been opened to visitors, who climb the narrow "
    "stairs to enjoy the view and learn about the history of the coast. Small museums explain how the great lenses "
    "work and how the keepers lived. For many coastal towns, the lighthouse has become a (5) ______ that draws "
    "tourists and their money.\n\n"
    "Sailors still value the lights, too. Electronic systems can fail, and a captain who sees a familiar beam in the "
    "darkness knows at once whether his instruments are telling him the (6) ______."))

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=1), ["insisted", "depended", "commented", "operated"], "B",
  "Cloze: verb + 'on' that means rely on",
  "Without modern equipment, the lights were the sailor's only guide, so he depended on them to know his position. "
  "'Depend on' means rely on.",
  ["Context: no modern navigation equipment", "The sailor needed the lights to know where he was",
   "'depended on'"],
  "'Insisted on' means demanded firmly. 'Commented on' means remarked about. 'Operated on' is used of surgery. None "
  "means relied on.", 30, C1, 1)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=2), ["brightened", "measured", "painted", "dimmed"], "D",
  "Cloze: the purpose of cleaning the glass",
  "Dirty glass makes a beam weaker. Keepers cleaned it so that the beam would not be dimmed (made less bright).",
  ["Action: cleaning the glass", "Purpose: keep the beam strong", "'so that ... would not be dimmed'"],
  "'Brightened' would make the sentence say they cleaned the glass so that the beam would not become brighter, "
  "which is illogical. 'Measured' and 'painted' do not describe what dirt does to a beam.", 30, C1, 2)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=3), ["automated", "abandoned", "demolished", "repainted"], "A",
  "Cloze: the next sentence explains the blank",
  "The next sentence says lamps 'switch on by themselves' and faults are reported to a distant control room. The "
  "lighthouses now run by machine: they have been automated.",
  ["Next sentence: lamps switch on by themselves", "Working without people = automated", "'automated'"],
  "'Abandoned' and 'demolished' contradict the lamps that still switch on every evening. 'Repainted' has nothing to "
  "do with lamps working on their own.", 30, C1, 3)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=4), ["visible", "colourful", "essential", "expensive"], "C",
  "Cloze: what satellite navigation changed",
  "Ships can now find their position by satellite, so they need the lights less. The lights have become less "
  "essential (necessary) than they once were.",
  ["Cause: satellite navigation", "Effect: ships rely less on the lights", "'far less essential'"],
  "Satellite navigation does not make the lights less 'visible' or less 'colourful'. 'Less expensive' has no link "
  "with satellite navigation and does not explain why the keeper's job disappeared.", 30, C1, 4)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=5), ["burden", "showpiece", "warning", "barrier"], "B",
  "Cloze: 'that draws tourists'",
  "The paragraph describes towers opened to visitors, with views and museums. Something a town proudly displays and "
  "that draws tourists and their money is a showpiece.",
  ["Clue: 'draws tourists and their money'", "Paragraph: towers opened to visitors, museums", "'showpiece'"],
  "'Burden' and 'barrier' are the opposite of something that brings visitors and money. A 'warning' does not draw "
  "tourists; it keeps people away.", 30, C1, 5)

Q(CL, "Single-blank cloze", B, CLOZE_STEM.format(n=6), ["time", "story", "news", "truth"], "D",
  "Cloze: fixed expression 'tell (someone) the truth'",
  "Electronic systems can fail. Seeing a familiar beam lets the captain check at once whether his instruments are "
  "correct, that is, whether they are telling him the truth.",
  ["Context: instruments may fail", "The beam lets him check whether they are right",
   "'telling him the truth'"],
  "'Telling him the time', 'the story' and 'the news' do not express whether the instruments are correct.",
  30, C1, 6)

# ---------------------------------------------------------------- Cloze 2 (Intermediate, 6)
C2 = stim("Mushrooms from straw", (
    "Every year, after the paddy harvest, farmers in parts of northern India are left with mountains of straw. With "
    "little time before the next crop must be sown, many set the fields on fire, sending thick smoke across the "
    "region. The practice is (1) ______ by law in many places, yet it continues because the alternatives seem costly "
    "or slow.\n\n"
    "One alternative turns the problem into a (2) ______. Paddy straw, when chopped, soaked and packed into beds, makes "
    "an excellent base for growing certain varieties of mushroom. A small shed, some plastic sheeting and a few weeks "
    "of care are enough to produce a crop that can be sold in nearby towns. The leftover material, rich in organic "
    "matter, can then be (3) ______ to the fields as manure, improving the soil that produced the straw in the first "
    "place.\n\n"
    "The idea is not new, but it has spread slowly. Mushrooms are delicate and spoil within days, so growers need "
    "quick access to buyers. Many farmers also lack the knowledge needed to keep the beds free of disease. Where "
    "cooperatives have stepped in to provide (4) ______ and to collect the produce, the results have been "
    "encouraging, and some women's groups now earn a steady income from their mushroom sheds.\n\n"
    "Mushroom growing cannot, of course, use all the straw that a region produces. It is one of several (5) ______, "
    "along with machines that mix the straw into the soil and plants that turn it into fuel. Together, such measures "
    "can reduce burning, but only if farmers find them practical and (6) ______. A ban that offers no workable "
    "alternative is likely to be ignored, however strictly it is worded."))

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=1), ["encouraged", "permitted", "prohibited", "rewarded"], "C",
  "Cloze: 'yet it continues' signals that the practice is forbidden",
  "'Yet it continues' shows a contrast: the practice goes on in spite of the law. So the law forbids it: it is "
  "prohibited. The last paragraph's mention of 'a ban' confirms this.",
  ["'by law ... yet it continues' = contrast", "The law must be against the practice", "'prohibited'"],
  "'Encouraged', 'permitted' and 'rewarded' remove the contrast with 'yet it continues' and clash with the 'ban' in "
  "the last paragraph.", 35, C2, 1)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=2), ["resource", "burden", "hazard", "dispute"], "A",
  "Cloze: 'turns the problem into ...' needs something useful",
  "The paragraph shows straw being used to grow a saleable crop and then as manure. The problem becomes something "
  "useful: a resource.",
  ["'turns the problem into' → the opposite of a problem", "Following sentences: straw grows mushrooms and manure",
   "'resource'"],
  "'Burden', 'hazard' and 'dispute' are themselves problems, so turning a problem into one of them makes no sense "
  "with the useful outcomes that follow.", 35, C2, 2)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=3), ["restricted", "confined", "exported", "returned"], "D",
  "Cloze: verb + 'to the fields as manure'",
  "The leftover material goes back to the fields where the straw came from, 'improving the soil that produced the "
  "straw in the first place'. It is returned to the fields.",
  ["Pattern: be ___ to the fields as manure", "Clue: the soil that produced the straw", "'returned'"],
  "'Restricted to' and 'confined to' mean limited to, which does not describe using the material as manure. "
  "'Exported to the fields' is not idiomatic; export means send to another country.", 35, C2, 3)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=4), ["tractors", "training", "fertiliser", "land"], "B",
  "Cloze: the cooperatives answer the two difficulties just named",
  "The two difficulties are quick access to buyers and a lack of the knowledge needed to keep beds free of disease. "
  "Cooperatives 'collect the produce' (buyers) and provide training (knowledge).",
  ["Difficulty 1: access to buyers → cooperatives collect the produce",
   "Difficulty 2: lack of knowledge → cooperatives provide training", "'training'"],
  "Tractors, fertiliser and land are not among the difficulties described; the passage says a small shed and some "
  "sheeting are enough.", 35, C2, 4)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=5), ["problems", "causes", "solutions", "crops"], "C",
  "Cloze: 'one of several ___, along with machines ... and plants ...'",
  "Mushroom growing, straw-mixing machines and fuel plants are all ways of dealing with the straw instead of burning "
  "it. They are solutions.",
  ["Items grouped together: mushrooms, machines, fuel plants", "All are alternatives to burning",
   "'solutions'"],
  "They are not 'problems' or 'causes' of burning; the next sentence says they can reduce it. 'Crops' does not "
  "describe machines or fuel plants.", 35, C2, 5)

Q(CL, "Single-blank cloze", I, CLOZE_STEM.format(n=6), ["affordable", "fashionable", "compulsory", "complicated"],
  "A",
  "Cloze: paired adjectives with 'practical and ___'",
  "Paragraph 1 says burning continues 'because the alternatives seem costly or slow'. Farmers will adopt the "
  "alternatives only if they are practical and affordable, answering the 'slow' and 'costly' objections.",
  ["Para 1: alternatives seem costly or slow", "Measures work only if they meet these objections",
   "'practical and affordable'"],
  "'Fashionable' is irrelevant to farmers' choices. 'Compulsory' clashes with 'if farmers find them'. "
  "'Complicated' would be a reason not to adopt them.", 35, C2, 6)

# ---------------------------------------------------------------- Cloze 3 (Intermediate 1 + Advanced 5; error-based)
C3 = stim("Gold in the vault", (
    "Long after the world abandoned the gold standard, central banks continue to hold large stocks of gold. To some "
    "observers this seems **(1) reasonable**: gold pays no interest, costs money to store and guard, and its price can "
    "swing sharply from one year to the next. Why should a modern central bank keep so much of its reserves in a metal "
    "that earns nothing?\n\n"
    "Part of the answer lies in trust. Unlike a government bond, gold is not anyone's promise to pay, so it cannot be "
    "**(2) defaulted** on, and if it is stored at home it cannot be frozen by a foreign government. In times of "
    "crisis, when confidence in currencies and financial institutions weakens, gold has tended to hold its value or "
    "even rise, which makes it a **(3) risky** hedge against turmoil.\n\n"
    "Gold also helps central banks **(4) concentrate** their reserves. A reserve portfolio made up mainly of assets in "
    "a single foreign currency leaves a country exposed to that currency's ups and downs; adding gold spreads the "
    "risk. In recent years, several central banks in emerging economies have been **(5) reducing** their gold "
    "holdings steadily, partly for this reason and partly to lessen their dependence on any one country's financial "
    "system.\n\n"
    "The case is not without critics. They point out that the price of gold is driven largely by sentiment, and that "
    "money tied up in the metal could instead earn interest in bonds. Holding some gold, they concede, may be prudent, "
    "but holding a great deal of it amounts to **(6) costly** insurance whose benefits are hard to measure."))

Q(CL, "Error-based cloze", I,
  ERR_STEM.format(n=1, ctx="To some observers this seems reasonable: gold pays no interest, costs money to store and "
                           "guard"),
  ["curious", "prudent", "natural", NR], "A",
  "Error-based cloze: the colon introduces reasons why the practice looks strange",
  "After the colon, the passage lists gold's drawbacks (no interest, storage costs, price swings) and then asks why a "
  "central bank should keep so much of it. These reasons make the practice seem strange, not reasonable. 'Curious' "
  "(odd, puzzling) fits.",
  ["After the colon: drawbacks of holding gold", "Followed by the puzzled question 'Why should ...?'",
   "Replace 'reasonable' with 'curious'"],
  "'Prudent' and 'natural' would, like 'reasonable', present the practice as sensible, which contradicts the list of "
  "drawbacks and the question. 'Reasonable' is wrong, so 'No replacement required' does not apply.", 40, C3, 1)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=2, ctx="gold is not anyone's promise to pay, so it cannot be defaulted on"),
  ["repaid", "guaranteed", "traded", NR], "D",
  "Error-based cloze: 'default on' = fail to repay a debt",
  "A bond is a promise to pay, and the borrower can default on it (fail to pay). Gold is no one's promise, so no one "
  "can default on it. 'Defaulted' is correct.",
  ["Contrast: bond (a promise to pay) vs gold (no promise)", "A promise can be broken = defaulted on",
   "'cannot be defaulted on' fits: no replacement"],
  "'Cannot be repaid on' and 'cannot be guaranteed on' are not idiomatic and lose the contrast with a broken "
  "promise. 'Cannot be traded on' is false and has nothing to do with the 'promise to pay'.", 50, C3, 2)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=3, ctx="gold has tended to hold its value or even rise, which makes it a risky hedge against "
                           "turmoil"),
  ["costly", "dependable", "temporary", NR], "B",
  "Error-based cloze: 'which makes it ...' must follow from the good behaviour just described",
  "An asset that holds its value or rises when confidence falls is good protection in a crisis. That makes it a "
  "dependable hedge, not a 'risky' one.",
  ["Gold holds or gains value in crises", "Therefore it is a good hedge", "Replace 'risky' with 'dependable'"],
  "'Costly' is a drawback (raised by the critics later), not something that follows from gold holding its value. "
  "'Temporary' has no support in the sentence. 'Risky' contradicts the clause before it, so 'No replacement "
  "required' does not apply.", 45, C3, 3)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=4, ctx="Gold also helps central banks concentrate their reserves ... adding gold spreads the "
                           "risk"),
  ["liquidate", "value", "diversify", NR], "C",
  "Error-based cloze: the next sentences describe spreading risk",
  "The paragraph explains that holding mainly one currency is risky and that 'adding gold spreads the risk'. "
  "Spreading reserves across different assets is diversifying them; 'concentrate' says the opposite.",
  ["Problem: reserves mainly in one currency", "Solution: adding gold spreads the risk",
   "Replace 'concentrate' with 'diversify'"],
  "'Liquidate' (turn into cash, sell off) has nothing to do with spreading risk across assets. 'Value' their reserves "
  "does not match 'adding gold spreads the risk'. 'Concentrate' is wrong, so 'No replacement required' does not "
  "apply.", 45, C3, 4)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=5, ctx="several central banks in emerging economies have been reducing their gold holdings "
                           "steadily, partly for this reason and partly to lessen their dependence"),
  ["auditing", "increasing", "insuring", NR], "B",
  "Error-based cloze: 'for this reason' points back to the benefit of adding gold",
  "'This reason' is that adding gold spreads risk, and lessening dependence on one country's financial system also "
  "calls for more gold, not less. Banks acting for these reasons would be increasing their holdings.",
  ["'for this reason' = adding gold spreads the risk", "Lessening dependence on one country → hold more gold",
   "Replace 'reducing' with 'increasing'"],
  "'Auditing' and 'insuring' their holdings are not actions that spread risk or lessen dependence, and 'steadily' "
  "fits a change in size, not an audit. 'Reducing' contradicts both reasons given, so 'No replacement required' does "
  "not apply.", 50, C3, 5)

Q(CL, "Error-based cloze", A,
  ERR_STEM.format(n=6, ctx="holding a great deal of it amounts to costly insurance whose benefits are hard to "
                           "measure"),
  ["cheap", "reliable", "compulsory", NR], "D",
  "Error-based cloze: the critics' objection decides the word",
  "The critics argue that money in gold earns no interest and could earn interest in bonds. Their point, introduced "
  "by 'but' after the concession 'may be prudent', is that holding a great deal of gold amounts to costly insurance. "
  "'Costly' is correct.",
  ["Critics: gold earns nothing; bonds earn interest", "'but holding a great deal' = an objection",
   "'costly' fits: no replacement"],
  "'Cheap' and 'reliable' would turn the critics' objection into praise. 'Compulsory' is false: no one forces central "
  "banks to hold gold.", 50, C3, 6)

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


# ---- Basic (4)
ed("Part-wise error", B, "The bank has launched", "a three-years savings plan", "for school students.", "B",
   "A number + noun used as a compound adjective before another noun stays singular",
   "When a number and a noun together describe another noun, the noun is singular and the two are hyphenated: 'a "
   "three-year savings plan', just as we say 'a ten-rupee note' and 'a five-day week'.",
   ["'three-years' describes the noun 'plan'", "Compound adjective → singular 'year'",
    "'a three-years' → 'a three-year': error in part B"],
   "Part A uses the present perfect correctly. Part C ('for school students') is correct. B has an error, so 'No "
   "error' is wrong.", 30)

ed("Part-wise error", B, "The branch who opened", "near the bus stand last month", "is already crowded.", "A",
   "Relative pronouns: 'who' for people, 'which' or 'that' for things",
   "A branch is a place, not a person, so the relative pronoun must be 'which' or 'that': 'The branch which (or that) "
   "opened near the bus stand last month is already crowded.'",
   ["Antecedent: 'The branch' (a thing)", "Thing → 'which' or 'that'", "'who' → 'which': error in part A"],
   "Part B is a correct place-and-time phrase. Part C has a singular verb agreeing with 'branch'. A has an error, so "
   "'No error' is wrong.", 30)

ed("Part-wise error", B, "On pension day,", "the waiting hall is not", "enough large for all the customers.", "C",
   "'Enough' comes after an adjective or adverb but before a noun",
   "With an adjective, 'enough' follows it: 'large enough', 'big enough'. ('Enough' comes before a noun: 'enough "
   "chairs'.) Correct: 'the waiting hall is not large enough for all the customers'.",
   ["'large' is an adjective", "Adjective + enough", "'enough large' → 'large enough': error in part C"],
   "Part A is a correct time phrase. Part B ('the waiting hall is not') is correct. C has an error, so 'No error' "
   "is wrong.", 30)

ed("Error-free sentence", B, "Hardly anyone", "turned up at the meeting", "because of the heavy rain.", "D",
   "'Hardly anyone' (= almost nobody) is correct; no extra negative is needed",
   "'Hardly anyone turned up' means almost nobody came. 'Hardly' is already negative, and the sentence correctly uses "
   "a positive verb with it. 'Turn up' (arrive) and 'because of' + noun are also correct.",
   ["Part A: 'Hardly anyone' = almost nobody", "Part B: 'turned up at' = arrived at, simple past",
    "Part C: 'because of' + noun phrase", "No error: option D"],
   "A, B and C are each correct as shown in the steps. Changing A to 'Hardly no one' would create a double "
   "negative.", 30)

# ---- Intermediate (3)
ed("Part-wise error", I, "Of the two plans", "presented to the board,", "the second was clearly the best.", "C",
   "When exactly two things are compared, the comparative ('better') is used, not the superlative ('best')",
   "The superlative is for three or more. With 'Of the two plans', the correct form is 'the second was clearly the "
   "better'.",
   ["'Of the two plans' → exactly two items", "Two items → comparative", "'the best' → 'the better': error in part C"],
   "Parts A and B correctly introduce the two plans. C has an error, so 'No error' is wrong.", 35)

ed("Part-wise error", I, "These kind of errors", "are common among", "new clerks in their first month.", "A",
   "'Kind', 'sort' and 'type' agree with the demonstrative: 'this kind of', 'these kinds of'",
   "'Kind' is singular, so it takes 'this': 'This kind of error is common ...'. For the plural, both words change: "
   "'These kinds of errors are common ...'. 'These kind of' mixes a plural demonstrative with a singular noun.",
   ["'These' is plural; 'kind' is singular", "They must agree: 'these kinds of errors'",
    "Error in part A"],
   "Part B's plural verb 'are' agrees with the intended plural subject. Part C is a correct phrase. A has an error, "
   "so 'No error' is wrong.", 35)

ed("Part-wise error", I, "The awareness camp was a failure,", "as a few villagers", "turned up to listen.", "B",
   "'A few' (= some, a small but useful number) vs 'few' (= hardly any, not enough)",
   "The camp failed because almost nobody came. That negative idea needs 'few' (or 'very few'): 'as few villagers "
   "turned up to listen'. 'A few villagers' sounds positive and does not explain a failure.",
   ["Result: the camp was a failure", "Cause must be negative: hardly any villagers came",
    "'a few' → 'few': error in part B"],
   "Part A is correct. Part C ('turned up to listen') is correct. B has an error of meaning, so 'No error' is "
   "wrong.", 40)

# ---- Advanced (6)
ed("Part-wise error", A, "On his doctor's advice,", "he stopped to eat sweets", "after his fiftieth birthday.", "B",
   "'Stop + -ing' (give up an activity) vs 'stop + to-infinitive' (pause in order to do something)",
   "The doctor advised him to give up sweets, so he stopped eating them. 'He stopped to eat sweets' means he paused "
   "something else in order to eat sweets, the opposite of the advice.",
   ["Context: doctor's advice → give up sweets", "Give up = stop + -ing",
    "'stopped to eat' → 'stopped eating': error in part B"],
   "Part A is a correct phrase. Part C ('after his fiftieth birthday') is correct. B is grammatical on its own but "
   "wrong in meaning, so 'No error' is wrong.", 45)

ed("Part-wise error", A, "The regional office has not yet decided", "if or not the branch", "will open on the "
   "second Saturday.", "B",
   "'Whether or not' (or 'whether ... or not'); 'if' cannot be followed directly by 'or not'",
   "'If' and 'whether' can both introduce an indirect question ('has not decided if the branch will open'), but only "
   "'whether' can be followed immediately by 'or not': 'has not yet decided whether or not the branch will open on "
   "the second Saturday'.",
   ["Indirect yes/no question after 'decided'", "'or not' placed straight after the conjunction",
    "Only 'whether or not' is possible: 'if or not' → 'whether or not': error in part B"],
   "Part A correctly uses the present perfect with 'not yet'. Part C correctly uses 'will' inside the indirect "
   "question. B has an error, so 'No error' is wrong.", 40)

ed("Part-wise error", A, "The night guard", "noticed an asleep man", "lying on the bench outside the ATM.", "B",
   "Some adjectives beginning with 'a-' (asleep, alive, afraid, alone) are used only after a verb, not before a noun",
   "We can say 'the man was asleep' but not 'an asleep man'. Before the noun we need 'a sleeping man': 'The night "
   "guard noticed a sleeping man lying on the bench outside the ATM.'",
   ["'asleep' is a predicative-only adjective", "Before a noun → 'sleeping'",
    "'an asleep man' → 'a sleeping man': error in part B"],
   "Part A is a correct subject. Part C ('lying on the bench ...') is a correct participle phrase. B has an error, so "
   "'No error' is wrong.", 40)

ed("Error-free sentence", A, "Not a single complaint", "has been received", "since the new system was introduced.",
   "D",
   "'Not a single' + singular noun takes a singular verb; present perfect with 'since' + a past point",
   "'Not a single complaint' is singular, so 'has been received' is correct. The present perfect suits a period "
   "lasting up to now, and 'since' is followed by the simple past of the starting event ('was introduced').",
   ["Part A: singular subject 'complaint'", "Part B: singular present perfect passive: correct",
    "Part C: 'since' + simple past starting point: correct", "No error: option D"],
   "A, B and C are each correct as shown in the steps. 'Have been received' would wrongly treat the subject as "
   "plural.", 45)

ed("Part-wise error", A, "In the strongroom,", "the three senior cashiers", "each has a separate locker.", "C",
   "When 'each' comes after a plural subject, the verb agrees with the plural subject",
   "'Each' at the start of a subject ('Each cashier has') takes a singular verb, but here the subject is 'the three "
   "senior cashiers' and 'each' follows it, so the verb is plural: 'the three senior cashiers each have a separate "
   "locker'.",
   ["Subject: 'the three senior cashiers' (plural)", "'each' after the subject does not change its number",
    "'each has' → 'each have': error in part C"],
   "Part A is a correct place phrase and part B a correct plural subject. C has an error, so 'No error' is wrong.",
   45)

ed("Part-wise error", A, "Being a public holiday,", "the branch remained closed", "and its ATM ran out of cash.",
   "A",
   "An introductory participle phrase must refer to the subject of the main clause; otherwise use an absolute "
   "phrase with its own subject ('It being ...')",
   "As written, 'Being a public holiday' describes 'the branch', as if the branch were a holiday. The day needs its "
   "own subject: 'It being a public holiday, the branch remained closed ...' (or 'As it was a public holiday, ...').",
   ["Who or what was 'a public holiday'? The day, not the branch", "Subject of the main clause: 'the branch'",
    "Add a subject: 'It being a public holiday': error in part A"],
   "Part B is a correct main clause. Part C correctly joins a second clause. A has an error, so 'No error' is "
   "wrong.", 45)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", B,
  SI_STEM + "**Why you did not inform** the bank as soon as your card was stolen?",
  ["Why did you not inform", "Why you had not informed", "Why did you not informed", NI], "A",
  "Direct questions use question word order: question word + auxiliary + subject + base verb",
  "A direct question needs the auxiliary before the subject: 'Why did you not inform the bank ...?' (or 'Why didn't "
  "you inform ...?'). Statement order ('you did not') is used only in indirect questions.",
  ["The sentence ends with '?' → direct question", "Order: Why + did + you + not + base verb",
   "'Why did you not inform'"],
  "'Why you had not informed' keeps statement order and changes the tense. 'Why did you not informed' uses a past "
  "form after 'did'. The original keeps statement order, so 'No improvement required' is wrong.", 25)

Q(SI, "Bold-part improvement", B,
  SI_STEM + "**Instead of to wait** in the long queue, she paid the bill on the bank's app.",
  ["Instead to wait", "Instead of wait", "Instead of waiting", NI], "C",
  "A preposition ('of' in 'instead of') is followed by a gerund (-ing form)",
  "'Instead of' ends in the preposition 'of', and a verb after a preposition takes the -ing form: 'Instead of "
  "waiting in the long queue, she paid the bill on the app.'",
  ["'instead of' ends in a preposition", "Preposition + gerund", "'Instead of waiting'"],
  "'Instead to wait' drops the needed 'of'. 'Instead of wait' uses the base form after a preposition. The original "
  "uses a to-infinitive after 'of', so 'No improvement required' is wrong.", 25)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "The roads are full of puddles this morning; it **must rain** heavily last night.",
  ["must be raining", "must have rained", "should rain", NI], "B",
  "Modal of deduction about the past: must have + past participle",
  "The puddles are evidence from which the speaker concludes something about last night. A confident conclusion "
  "about the past is 'must have + past participle': 'it must have rained heavily last night'.",
  ["Evidence now: puddles", "Conclusion about a past event: 'last night'", "Past deduction → 'must have rained'"],
  "'Must be raining' is a deduction about the present. 'Should rain' expresses expectation or advice about the "
  "future. 'Must rain' cannot refer to last night, so 'No improvement required' is wrong.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "**Supposing if you lose** your debit card, what will you do first?",
  ["Supposing you lose", "Supposing if you will lose", "Suppose if you lost", NI], "A",
  "Redundancy: 'supposing' already means 'if', so the two are not used together",
  "'Supposing' (like 'suppose' and 'if') introduces a condition by itself. Using it with 'if' doubles the "
  "conjunction. Correct: 'Supposing you lose your debit card, what will you do first?'.",
  ["'Supposing' = 'if'", "Using both repeats the conjunction", "'Supposing you lose'"],
  "'Supposing if you will lose' keeps the doubled conjunction and adds 'will' in the condition. 'Suppose if you "
  "lost' keeps 'if' and changes the tense. The original doubles the conjunction, so 'No improvement required' is "
  "wrong.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "**As far as the home loan**, the bank will decide on your application next week.",
  ["As far as the home loan goes on", "So far as the home loan", "As far as the home loan is concerned", NI],
  "C",
  "The fixed expression is 'as far as X is concerned' (or 'as far as X goes')",
  "'As far as' introduces a clause and needs a verb: 'As far as the home loan is concerned, the bank will decide on "
  "your application next week.' Without 'is concerned' the phrase is incomplete.",
  ["'As far as' + subject needs a verb", "Fixed completion: 'is concerned'",
   "'As far as the home loan is concerned'"],
  "'Goes on' is not the fixed completion. 'So far as the home loan' is incomplete in the same way as the original. "
  "The original is incomplete, so 'No improvement required' is wrong.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "I **have gone** to the bank's head office in Mumbai twice, so I know the way.",
  ["had gone", "have been", "was going", NI], "B",
  "'Have been to' (visited and returned) vs 'have gone to' (went and is still there or on the way)",
  "The speaker visited the head office and came back, which is why he can say he knows the way. A completed visit "
  "is 'have been to': 'I have been to the bank's head office in Mumbai twice.' 'Have gone' would mean he is there now, "
  "and it cannot be repeated 'twice'.",
  ["Experience of visiting and returning", "'twice' = repeated completed visits", "'have been to'"],
  "'Had gone' places the visits before another past event that is not mentioned. 'Was going' describes an action in "
  "progress, which clashes with 'twice'. 'Have gone' implies he is still there, so 'No improvement required' is "
  "wrong.", 30)

Q(SI, "Bold-part improvement", I,
  SI_STEM + "**On no account should customers share** their OTP with anyone who calls them.",
  ["On no account customers should share", "On no account should customers sharing",
   "In no account should customers share", NI], "D",
  "Negative adverbial phrase at the start ('On no account') + inversion (auxiliary before subject)",
  "When a negative phrase such as 'On no account' begins a sentence, the auxiliary comes before the subject: 'On no "
  "account should customers share their OTP ...'. The sentence is already correct.",
  ["Opening: 'On no account' (negative)", "Inversion: should + customers + base verb",
   "The bold part is correct"],
  "'On no account customers should share' lacks the required inversion. 'Should customers sharing' uses an -ing form "
  "after a modal. 'In no account' is not the fixed phrase.", 30)

Q(SI, "Bold-part improvement", A,
  SI_STEM + "The proposal to close the rural branches **was objected by** the employees' union.",
  ["was objected on by", "was objected to by", "objected by", NI], "B",
  "Prepositional verbs keep their preposition in the passive: 'object to' → 'was objected to'",
  "The active is 'The union objected to the proposal'. In the passive, the preposition stays with the verb: 'The "
  "proposal ... was objected to by the employees' union.'",
  ["Active: 'object to' + object", "Passive: was + objected + to", "Agent: 'by the union' → 'was objected to by'"],
  "'Objected on' uses the wrong preposition. 'Objected by' makes the proposal the one objecting. The original drops "
  "'to', so 'No improvement required' is wrong.", 35)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", B,
  PR_STEM + "The fire brigade **put off** the fire in the market within an hour.",
  ["put up", "put away", "put out", NR], "C",
  "Phrasal verbs with 'put': put out = extinguish (a fire or light)",
  "Firefighters extinguish a fire: they 'put it out'. 'Put off' means postpone.",
  ["Object: a fire", "Meaning needed: extinguish", "'put out'"],
  "'Put up' means build, display or accommodate. 'Put away' means store something in its place. The original 'put "
  "off' means postpone, so 'No replacement required' does not apply.", 25)

Q(PR, "Replace the phrase", B,
  PR_STEM + "The bank's founder **passed out** peacefully last year at the age of ninety-two.",
  ["passed away", "passed by", "passed over", NR], "A",
  "Phrasal verbs with 'pass': pass away = die (a polite expression)",
  "'At the age of ninety-two' and 'peacefully' show that the founder died. The polite phrasal verb for dying is "
  "'pass away'. 'Pass out' means faint (or, in some varieties, graduate).",
  ["Context: an old man, 'peacefully', 'last year'", "Meaning needed: died", "'passed away'"],
  "'Passed by' means went past. 'Passed over' means ignored someone, for example for promotion. The original 'passed "
  "out' (fainted) does not fit, so 'No replacement required' does not apply.", 25)

Q(PR, "Replace the phrase", B,
  PR_STEM + "The new clerk quickly **picked up** the basics of the core-banking software.",
  ["picked on", "picked out", "picked off", NR], "D",
  "Phrasal verbs with 'pick': pick up = learn (a skill) without formal study",
  "To 'pick up' a skill is to learn it easily through practice. The new clerk learnt the basics of the software "
  "quickly, so the sentence is correct.",
  ["Object: the basics of the software", "Meaning needed: learnt", "'picked up' is correct"],
  "'Picked on' means treated someone unfairly. 'Picked out' means chose or recognised. 'Picked off' means shot or "
  "removed one by one. None means learnt.", 25)

Q(PR, "Replace the phrase", I,
  PR_STEM + "Rumours about the cooperative bank's losses **gave rise for** panic among its depositors.",
  ["gave rise to", "gave raise to", "gave rise of", NR], "A",
  "Fixed expression: 'give rise to' = cause",
  "To 'give rise to' something is to cause it: 'Rumours ... gave rise to panic among its depositors.' The expression "
  "always takes 'to'.",
  ["Meaning: caused panic", "Fixed expression: give rise to", "'gave rise to'"],
  "'Gave raise to' confuses the noun 'rise' with the verb 'raise'. 'Gave rise of' uses the wrong preposition. The "
  "original uses 'for', so 'No replacement required' does not apply.", 30)

Q(PR, "Replace the phrase", I,
  PR_STEM + "The fraud **came into light** only when the auditors checked the old vouchers.",
  ["came to light", "came in light", "came at light", NR], "A",
  "Fixed expression: 'come to light' = become known",
  "Hidden facts 'come to light' when they are discovered: 'The fraud came to light only when the auditors checked "
  "the old vouchers.'",
  ["Meaning: became known", "Fixed expression: come to light", "'came to light'"],
  "'Came in light' and 'came at light' are not idiomatic. The original 'came into light' is not the fixed form, so "
  "'No replacement required' does not apply.", 30)

Q(PR, "Replace the phrase", I,
  PR_STEM + "With two colleagues on leave, the clerk could not **keep up to** the growing pile of applications.",
  ["keep up on", "keep up with", "keep off", NR], "B",
  "Phrasal verb: keep up with = manage to deal with something at the rate it arrives",
  "The pile of applications grows faster than the clerk can handle it: he cannot 'keep up with' it. The phrasal verb "
  "takes 'with'.",
  ["Context: work arriving faster than it can be done", "Phrasal verb: keep up with", "'keep up with'"],
  "'Keep up on' is not the standard pattern here. 'Keep off' means stay away from. The original uses 'to', so 'No "
  "replacement required' does not apply.", 30)

Q(PR, "Replace the phrase", A,
  PR_STEM + "Several directors **took exception at** the chairman's remarks about the staff union.",
  ["took exception on", "took exception to", "made exception to", NR], "B",
  "Fixed expression: 'take exception to' = object to; be offended by",
  "To 'take exception to' something is to object to it or be offended by it: 'Several directors took exception to "
  "the chairman's remarks.' The expression takes 'to'.",
  ["Meaning: objected to, were offended by", "Fixed form: take exception to", "'took exception to'"],
  "'Took exception on' uses the wrong preposition. 'Made exception to' is not idiomatic ('make an exception' means "
  "not apply a rule in one case). The original uses 'at', so 'No replacement required' does not apply.", 35)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"
SC_OK = "Which of the following sentences is grammatically correct?"
SC_BAD = "Which of the following sentences is grammatically INCORRECT?"

Q(SC, "Correct sentence", B, SC_OK,
  ["The customers were boring by the long wait at the counter.",
   "The training lecture was so bored that many of us fell asleep.",
   "I was very interesting in the bank's new savings scheme.",
   "The results of the customer survey were surprising to everyone."], "D",
  "-ing adjectives describe what causes a feeling; -ed adjectives describe the person who has the feeling",
  "Something that causes surprise is 'surprising'; a person who feels it is 'surprised'. 'The results ... were "
  "surprising to everyone' is correct.",
  ["A: customers felt boredom → 'bored by'", "B: the lecture caused boredom → 'boring'",
   "C: the speaker felt interest → 'interested in'", "D: the results caused surprise → 'surprising': correct"],
  "A and C use the -ing form for people who feel something. B uses the -ed form for the thing that causes the "
  "feeling.", 30)

Q(SC, "Grammatically incorrect sentence", B, SC_BAD,
  ["The children's section of the library opens at ten.",
   "The two clerks' desks were moved to the new floor.",
   "The mens' hostel is just behind the bank.",
   "The women's group meets every Friday evening."], "C",
  "Possessive of irregular plurals (men, women, children): add 's",
  "'Men' is already plural and does not end in -s, so its possessive is 'men's', like 'women's' and 'children's'. "
  "'Mens'' is wrong. Regular plurals ending in -s take only an apostrophe: 'the two clerks' desks'.",
  ["A: children → children's: correct", "B: clerks (regular plural) → clerks': correct",
   "C: men → men's, not mens': incorrect", "D: women → women's: correct"],
  "A, B and D form the possessive correctly, so none of them is the incorrect sentence.", 30)

Q(SC, "Correct sentence", I, SC_OK,
  ["You need not to bring your passbook tomorrow.",
   "You need not bring your passbook tomorrow.",
   "He dare not to question the manager's order.",
   "They ought submit the form by Friday."], "B",
  "Modal 'need not' and 'dare not' take a bare infinitive; 'ought' takes 'to'",
  "Used as modals in the negative, 'need' and 'dare' are followed by the base verb without 'to': 'You need not "
  "bring ...', 'He dare not question ...'. 'Ought', by contrast, always takes 'to': 'They ought to submit ...'.",
  ["A: 'need not to bring' → 'need not bring'", "B: correct",
   "C: 'dare not to question' → 'dare not question'", "D: 'ought submit' → 'ought to submit'"],
  "A and C add 'to' after modal 'need not' and 'dare not'. D drops the 'to' that 'ought' requires.", 35)

Q(SC, "Grammatically incorrect sentence", I, SC_BAD,
  ["New tea stalls have sprang up all round the new branch.",
   "The old cotton shirt has shrunk in the wash.",
   "The guard has drunk three cups of tea since midnight.",
   "The bell had already rung when we reached the hall."], "A",
  "Past participles of irregular verbs: spring – sprang – sprung; shrink – shrank – shrunk; drink – drank – drunk; "
  "ring – rang – rung",
  "After 'has' or 'have', the past participle is needed. 'Sprang' is the simple past of 'spring'; the participle is 'sprung': "
  "'New tea stalls have sprung up all round the new branch.' (To 'spring up' is to appear suddenly.)",
  ["A: 'have sprang' → 'have sprung': incorrect", "B: 'has shrunk': correct participle",
   "C: 'has drunk': correct participle", "D: 'had rung': correct participle"],
  "B, C and D all use the correct past participle after 'has', 'have' or 'had'.", 35)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) A volunteer took her to the help desk, where her name was announced on the loudspeaker.\n"
  "(B) At the crowded village fair, six-year-old Priya let go of her mother's hand to look at a toy stall.\n"
  "(C) Within ten minutes, her worried mother came running to the desk.\n"
  "(D) When she turned around, her mother was nowhere to be seen, and she began to cry.\n"
  "(E) Since that day, Priya has never let go of her mother's hand in a crowd.",
  ["BADCE", "DBACE", "BDCAE", "BDACE"], "D",
  "Para jumble: named opener, then time order (lost → found → lesson)",
  "B introduces Priya and how she let go. D ('When she turned around') shows she was lost. A gives the help desk "
  "announcement. C ('to the desk') shows the mother arriving. E gives the lasting lesson.",
  ["Opener: B (names Priya)", "B → D: she turns round and her mother is gone",
   "D → A: a volunteer helps; A → C: mother comes 'to the desk'", "C → E: lesson: BDACE"],
  "BADCE brings in the volunteer before Priya is lost. DBACE opens with 'she' before Priya is named. BDCAE has the "
  "mother come 'to the desk' before anyone has gone to it.", 45)

Q(PJ, "Five-sentence jumble", B,
  PJ5 + "(A) The report showed that his field had plenty of phosphorus but was short of zinc.\n"
  "(B) His costs fell, and his wheat yield was the best in five years.\n"
  "(C) For years, Ramesh had used the same amount of fertiliser on his field every season.\n"
  "(D) Following its advice, he cut back on one fertiliser and added a small dose of zinc.\n"
  "(E) Last year, an agriculture officer persuaded him to get his soil tested.",
  ["CEADB", "CAEDB", "ECADB", "CEDAB"], "A",
  "Para jumble: old habit → change → finding → action → result",
  "C names Ramesh and his old habit. E ('Last year', 'him') introduces the soil test. A gives 'The report'. D "
  "('Following its advice') acts on the report. B gives the result.",
  ["Opener: C (names Ramesh)", "C → E: the soil test is suggested", "E → A: 'The report' of that test",
   "A → D ('its advice') → B (result): CEADB"],
  "CAEDB mentions 'The report' before any test. ECADB opens with 'him' before Ramesh is named. CEDAB follows "
  "advice before the report that gives it.", 45)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) Last winter, the residents of our lane decided to start a weekly cleanliness drive.\n"
  "(P) On the first Sunday, only five people turned up with brooms and bags.\n"
  "(Q) Encouraged by the change, more families joined in over the following weeks.\n"
  "(R) Still, by noon they had cleared the rubbish from the whole lane.\n"
  "(S) Today, the lane is one of the cleanest in the town, and the drive has spread to nearby streets.",
  ["PQRS", "RPQS", "PRSQ", "PRQS"], "D",
  "Fixed opener; time order and the contrast word 'Still'",
  "P gives the small start on the first Sunday. R ('Still') contrasts the small number with what they achieved. Q "
  "('Encouraged by the change') follows the cleaned lane. S ('Today') gives the present result.",
  ["(1) → P: first Sunday", "P → R: 'Still' = in spite of only five people",
   "R → Q: the cleaned lane encourages others", "Q → S: 'Today': PRQS"],
  "PQRS places 'the change' before any change has been made. RPQS opens with 'Still' and 'they' before anyone is "
  "mentioned. PRSQ jumps to 'Today' and then back to the following weeks.", 45)

Q(PJ, "Fixed sentence", B,
  PJF + "(1) Hospitals often run short of blood during the summer months.\n"
  "(P) Donors at these camps are given a card that reminds them when they can donate again.\n"
  "(Q) One reason is that many regular donors, often college students, are away on holiday.\n"
  "(R) Helped by this reminder, many first-time donors go on to give blood regularly.\n"
  "(S) To fill this gap, some hospitals organise donation camps in offices and housing societies.",
  ["SQPR", "QPSR", "QSRP", "QSPR"], "D",
  "Fixed opener; 'One reason', 'this gap', 'these camps' and 'this reminder' as links",
  "Q gives a reason for the shortage in (1). S ('this gap') introduces the camps. P ('these camps') describes the "
  "reminder card. R ('this reminder') gives the result.",
  ["(1) → Q: 'One reason' for the shortage", "Q → S: 'this gap' = the shortage",
   "S → P: 'these camps'", "P → R: 'this reminder' = the card: QSPR"],
  "SQPR answers 'this gap' before the reason is given. QPSR mentions 'these camps' before any camp. QSRP uses 'this "
  "reminder' before the reminder card is described.", 45)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Modern buildings, with their smooth walls and sealed windows, offer few such spaces.\n"
  "(B) House sparrows were once found in almost every Indian home and courtyard.\n"
  "(C) In many cities, however, their numbers appear to have fallen sharply over the past few decades.\n"
  "(D) Bird experts suggest that one reason is the loss of nesting sites, since sparrows nest in holes and gaps in "
  "old walls and roofs.\n"
  "(E) Some residents have responded by putting up wooden nest boxes on their balconies, and in places the birds have "
  "returned.",
  ["BDCAE", "BCADE", "CBDAE", "BCDAE"], "D",
  "Para jumble: past → change ('however') → reason → elaboration ('such spaces') → response",
  "B describes the past. C ('however', 'their numbers') reports the decline. D gives a reason: loss of nesting "
  "sites. A ('such spaces') explains why modern buildings lack them. E gives the response.",
  ["Opener: B (names the sparrows)", "B → C: 'however' marks the decline",
   "C → D: 'one reason' for the decline", "D → A: 'such spaces' = holes and gaps; A → E: BCDAE"],
  "BDCAE gives a reason before the decline it explains. BCADE uses 'such spaces' before holes and gaps are "
  "mentioned. CBDAE opens with 'their numbers' before sparrows are named.", 55)

Q(PJ, "Fixed sentence", I,
  PJF + "(1) Most households own a drill that is used for only a few minutes in its entire life.\n"
  "(P) Members pay a small annual fee and can borrow a drill, a ladder or a sewing machine for a few days at a time.\n"
  "(Q) Such waste has led some neighbourhoods to set up 'tool libraries'.\n"
  "(R) Besides saving money, the arrangement reduces the number of rarely used goods that are made and later thrown "
  "away.\n"
  "(S) The same is true of ladders, large cooking pots for family functions and many other items.",
  ["QSPR", "SQPR", "SPQR", "SQRP"], "B",
  "Fixed opener; 'The same is true of', 'Such waste', 'Members' and 'the arrangement' as links",
  "S extends the point of (1) to other items. Q ('Such waste') introduces tool libraries. P ('Members') explains how "
  "they work. R ('the arrangement') adds the wider benefit.",
  ["(1) → S: 'The same is true of' other items", "S → Q: 'Such waste' sums up (1) and S",
   "Q → P: how a tool library works", "P → R: further benefit: SQPR"],
  "QSPR separates 'The same is true of' from the drill example it extends. SPQR describes members before any library "
  "is mentioned. SQRP gives the benefit of 'the arrangement' before the arrangement is explained.", 55)

Q(PJ, "Five-sentence jumble", I,
  PJ5 + "(A) Airlines know from experience that a certain share of passengers with tickets will not turn up.\n"
  "(B) Occasionally, however, more passengers arrive than there are seats.\n"
  "(C) To avoid flying with empty seats, they sell more tickets than the aircraft can hold.\n"
  "(D) In such cases, the airline asks for volunteers to take a later flight in return for compensation.\n"
  "(E) Most of the time, the passengers who do not turn up balance the extra sales, and every seat is filled.",
  ["ACEBD", "ACBED", "CAEBD", "ACEDB"], "A",
  "Para jumble: fact → practice → usual result → exception ('however') → how the exception is handled",
  "A states the known fact. C ('they') describes overbooking. E gives the usual outcome. B ('however') gives the "
  "exception. D ('In such cases') explains what happens then.",
  ["Opener: A (names airlines)", "A → C: 'they' = airlines; overbooking",
   "C → E: usual result", "E → B ('however') → D ('In such cases'): ACEBD"],
  "ACBED gives the exception before the usual result it contrasts with. CAEBD opens with 'they'. ACEDB places 'In "
  "such cases' before the cases (B) are described.", 55)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) When the use of a resource becomes more efficient, one might expect total consumption of it to fall.\n"
  "(B) The economist William Stanley Jevons noticed this in the nineteenth century, when more efficient steam engines "
  "were followed by a rise, not a fall, in Britain's use of coal.\n"
  "(C) Yet the opposite can happen: cheaper use encourages people to use more of it, sometimes so much more that "
  "total consumption rises.\n"
  "(D) Gains in efficiency, these cases suggest, are not by themselves a guarantee of conservation.\n"
  "(E) Today, some economists warn that fuel-efficient cars may similarly encourage people to drive longer "
  "distances.",
  ["ABCED", "ACEBD", "CABED", "ACBED"], "D",
  "Para jumble: expectation → 'Yet' the opposite → historical case ('this') → modern case ('similarly') → "
  "conclusion ('these cases')",
  "A states the expectation. C ('Yet the opposite') states the paradox. B ('noticed this') gives the historical "
  "example. E ('similarly', 'Today') gives a modern one. D ('these cases') draws the conclusion from both.",
  ["Opener: A (the expectation)", "A → C: 'Yet the opposite can happen'",
   "C → B: 'this' = the opposite effect", "B → E ('similarly') → D ('these cases'): ACBED"],
  "ABCED has Jevons notice 'this' before the paradox is stated. ACEBD gives the modern 'similarly' example before "
  "the case it is similar to. CABED opens with 'Yet'.", 70)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) In trials of new medicines, some patients are given a dummy pill that contains no active ingredient.\n"
  "(P) Surprisingly, many of these patients report that they feel better.\n"
  "(Q) This improvement, known as the placebo effect, shows how strongly expectation can shape the experience of "
  "illness.\n"
  "(R) It is also why a new drug is judged not by whether patients improve, but by whether they improve more than "
  "those given the dummy.\n"
  "(S) They are not told this, and in the best-designed trials neither are their doctors.",
  ["PSQR", "SQPR", "SPQR", "PQSR"], "C",
  "Fixed opener; 'They are not told this', 'these patients', 'This improvement' and 'also' as links",
  "S ('They are not told this') continues (1): the patients given the dummy are not told what it is. P ('these "
  "patients', 'Surprisingly') reports that they feel better all the same. Q ('This improvement') names the effect. "
  "R ('also') gives a further consequence for drug trials.",
  ["(1) → S: 'They' = the patients given the dummy; 'this' = that the pill is a dummy",
   "S → P: 'Surprisingly', these patients feel better",
   "P → Q: 'This improvement' must follow P directly", "Q → R: 'also why': SPQR"],
  "PSQR separates 'This improvement' (Q) from the improvement in P. SQPR uses 'This improvement' before any "
  "improvement is mentioned. PQSR puts 'They are not told this' after Q has "
  "moved on to the general effect, where 'They' and 'this' no longer have a clear referent.", 70)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) During the Second World War, analysts studied the bombers that returned from missions to decide where to "
  "add armour.\n"
  "(B) The statistician Abraham Wald pointed out the flaw in this reasoning.\n"
  "(C) The returning planes were full of bullet holes in the wings and the body, so the first instinct was to "
  "strengthen those areas.\n"
  "(D) The planes in front of them, he noted, were only the ones that had survived; those hit in the engines had not "
  "come back at all.\n"
  "(E) Armour, he argued, belonged where the returning planes showed no damage.",
  ["ACBDE", "ABCDE", "ACDBE", "CABDE"], "A",
  "Para jumble: situation → first instinct → 'this reasoning' challenged → why ('he noted') → conclusion",
  "A sets the scene. C gives the obvious reasoning. B ('this reasoning') introduces Wald's objection. D ('he noted') "
  "explains the flaw. E ('he argued') gives his conclusion.",
  ["Opener: A (the analysts' task)", "A → C: the first instinct", "C → B: 'this reasoning' = C's instinct",
   "B → D ('he' = Wald) → E: ACBDE"],
  "ABCDE calls the reasoning flawed before it has been stated. ACDBE uses 'he noted' before Wald is named. CABDE "
  "opens with 'The returning planes' before any planes are introduced.", 70)

Q(PJ, "Fixed sentence", A,
  PJF + "(1) Linguists estimate that a large share of the world's languages may fall silent by the end of this "
  "century.\n"
  "(P) Once the last fluent speakers die, much of this knowledge disappears with them.\n"
  "(Q) A language usually dies not because it is banned, but because parents stop passing it on to their children.\n"
  "(R) With each language lost in this way goes a store of knowledge about local plants, weather and history that "
  "was never written down.\n"
  "(S) They do so, often, in the belief that a dominant language will offer their children better prospects.",
  ["QRSP", "SQRP", "QSPR", "QSRP"], "D",
  "Fixed opener; 'They do so', 'in this way' and 'this knowledge' as links",
  "Q explains how languages die. S ('They do so') gives the parents' reason. R ('lost in this way') states what is "
  "lost. P ('this knowledge') explains when it disappears.",
  ["(1) → Q: how a language dies", "Q → S: 'They' = parents; 'do so' = stop passing it on",
   "S → R: 'in this way' = the process in Q and S", "R → P: 'this knowledge': QSRP"],
  "QRSP separates 'They do so' (S) from the parents in Q. SQRP opens with 'They do so' before anyone has done "
  "anything. QSPR uses 'this knowledge' before R mentions the knowledge.", 70)

Q(PJ, "Five-sentence jumble", A,
  PJ5 + "(A) A country that discovers a large oil or gas field might seem certain to grow richer.\n"
  "(B) As foreign buyers pay for the fuel, the country's currency tends to rise in value.\n"
  "(C) Economists call this pattern 'Dutch disease', after the experience of the Netherlands following the discovery "
  "of a large gas field in 1959.\n"
  "(D) A stronger currency, however, makes the country's other exports dearer abroad, and its factories may lose "
  "customers.\n"
  "(E) Yet the windfall can harm other parts of its economy.",
  ["AEBDC", "ABEDC", "AEDBC", "EABDC"], "A",
  "Para jumble: expectation → 'Yet' → mechanism (step 1 → step 2) → name of the pattern",
  "A states the expectation. E ('Yet', 'the windfall') introduces the harm. B explains the first step (currency "
  "rises). D ('A stronger currency') gives the second step. C ('this pattern') names it.",
  ["Opener: A (the discovery)", "A → E: 'Yet the windfall' (the oil or gas wealth)",
   "E → B → D: currency rises, then a stronger currency hurts exports", "D → C: 'this pattern': AEBDC"],
  "ABEDC explains the mechanism before E announces the harm, leaving 'Yet' after an explanation. AEDBC uses 'A "
  "stronger currency' before B says the currency rises. EABDC opens with 'Yet'.", 70)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) has decided to waive\n(Q) the processing fee on loans\n(R) the cooperative bank\n"
  "(S) taken by women entrepreneurs this year",
  ["RQSP", "RPQS", "QSRP", "RPSQ"], "B",
  "Subject + verb + object, with a participle phrase directly after the noun it describes",
  "'The cooperative bank has decided to waive the processing fee on loans taken by women entrepreneurs this year.' "
  "Subject (R), verb (P), object (Q), and S describes 'loans', so it follows Q.",
  ["Subject: R", "Verb: P ('has decided to waive')", "Object: Q; S describes 'loans': RPQS"],
  "RQSP puts the object before the verb. QSRP opens with the object, leaving 'the cooperative bank has decided' "
  "unconnected. RPSQ makes 'taken by women entrepreneurs' describe nothing before it.", 35)

Q(SR, "Word/phrase rearrangement within a sentence", I,
  SR_STEM + "(P) that the customer realised\n(Q) it was not until\n(R) she checked her statement\n"
  "(S) that her card had been misused",
  ["QPRS", "RQPS", "QRSP", "QRPS"], "D",
  "Cleft structure 'It was not until X that Y'",
  "'It was not until she checked her statement that the customer realised that her card had been misused.' The "
  "frame is 'It was not until' (Q) + time clause (R) + 'that' + main clause (P), followed by what she realised (S).",
  ["Frame: Q + R ('It was not until she checked her statement')", "'that' + main clause: P",
   "Object of 'realised': S → QRPS"],
  "QPRS puts 'that the customer realised' straight after 'until'. RQPS opens with 'she checked her statement' before "
  "the frame. QRSP makes the card's misuse the main clause and leaves 'that the customer realised' unfinished.", 40)

Q(SR, "Word/phrase rearrangement within a sentence", A,
  SR_STEM + "(P) did the authorities\n(Q) only when the river\n(R) order the evacuation\n(S) crossed the danger mark",
  ["QSPR", "QPSR", "SQPR", "QSRP"], "A",
  "Inversion after 'Only when' + clause: 'Only when X happened did + subject + base verb'",
  "'Only when the river crossed the danger mark did the authorities order the evacuation.' The 'only when' clause "
  "(Q + S) comes first; the main clause is inverted (P), followed by the base verb (R).",
  ["Opening clause: Q + S ('Only when the river crossed the danger mark')",
   "Inverted main clause: P ('did the authorities')", "Base verb + object: R → QSPR"],
  "QPSR breaks up the 'only when' clause. SQPR opens with a verb phrase. QSRP puts the verb before its subject "
  "'the authorities'.", 40)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", B,
  FB1 + "The doctor advised him to ______ from oily food for a few weeks after the operation.",
  ["avoid", "refuse", "abstain", "prevent"], "C",
  "Single blank: the verb must fit both the meaning and the preposition 'from'",
  "The doctor wants him to keep away from oily food. 'Abstain from' means choose not to have something, and it takes "
  "'from': 'to abstain from oily food'.",
  ["Meaning needed: keep away from", "The blank is followed by 'from'", "'abstain from'"],
  "'Avoid' has the right meaning but takes a direct object, not 'from' ('avoid oily food'). 'Refuse from' and "
  "'prevent from' (without an object) are not standard here.", 25)

Q(FB, "Double blank", B,
  FB2 + "The road was so ______ after the heavy rain that the bus had to move very ______.",
  ["dry, fast", "smooth, carefully", "slippery, fast", "slippery, slowly"], "D",
  "Double blank: 'so ... that' links a condition to its result",
  "Heavy rain makes a road slippery, and on a slippery road a bus has to move slowly.",
  ["Cause: heavy rain → slippery road", "Result after 'so ... that': careful, slow driving",
   "'slippery, slowly'"],
  "'Dry' contradicts the heavy rain. A 'smooth' road gives no reason to move carefully. 'Slippery, fast' breaks the "
  "cause-and-result link.", 25)

Q(FB, "Single blank", I,
  FB1 + "The committee's report was ______; it covered every aspect of the problem in great detail.",
  ["comprehensible", "comprehensive", "cursory", "concise"], "B",
  "Comprehensive (covering everything) vs comprehensible (understandable)",
  "The clause after the semicolon explains the blank: the report 'covered every aspect ... in great detail'. That "
  "is what 'comprehensive' means.",
  ["Clue: 'covered every aspect ... in great detail'", "Meaning needed: complete, thorough", "'comprehensive'"],
  "'Comprehensible' (easy to understand) is a look-alike with a different meaning. 'Cursory' (hasty) and 'concise' "
  "(brief) contradict 'in great detail'.", 30)

Q(FB, "Double blank", I,
  FB2 + "The minister's promise to ______ corruption sounded ______, since he had protected corrupt officials in the "
  "past.",
  ["encourage, sincere", "tolerate, hollow", "eradicate, hollow", "eradicate, convincing"], "C",
  "Double blank: a promise that his past record contradicts",
  "A minister promises to wipe out (eradicate) corruption, but his record of protecting corrupt officials makes the "
  "promise sound empty: hollow.",
  ["Blank 1: what a minister would promise to do to corruption → eradicate",
   "'since he had protected corrupt officials' → the promise lacks credibility", "Blank 2: hollow"],
  "No minister promises to 'encourage' or 'tolerate' corruption. 'Convincing' clashes with the reason given after "
  "'since'.", 35)

Q(FB, "Phrase fillers", I,
  FBP + "Before the audit, the bank wants to ______ fake and duplicate accounts from its records.",
  ["weed out", "bring about", "set off", "hold back"], "A",
  "Phrasal verb: weed out = remove unwanted members from a group",
  "Fake and duplicate accounts are unwanted items to be found and removed from the records, just as weeds are pulled "
  "out of a garden: 'weed out'.",
  ["Object: fake and duplicate accounts", "Meaning needed: find and remove", "'weed out'"],
  "'Bring about' means cause. 'Set off' means start a journey or trigger. 'Hold back' means restrain. None means "
  "remove from records.", 30)

Q(FB, "Single blank", A,
  FB1 + "His ______ manner (he never once raised his voice, even when the customers shouted at him) calmed the "
  "angry crowd.",
  ["irascible", "impetuous", "imperturbable", "obsequious"], "C",
  "Single blank: the bracketed description defines the word",
  "A person who never raises his voice even when shouted at is calm and impossible to upset: 'imperturbable'. Such a "
  "manner would calm a crowd.",
  ["Description: stays calm under provocation", "Effect: calms the crowd", "'imperturbable'"],
  "'Irascible' means easily angered and 'impetuous' means acting rashly, the opposite of the description. "
  "'Obsequious' (too eager to please) does not match never raising one's voice under pressure.", 35)

Q(FB, "Double blank", A,
  FB2 + "The board's decision, though ______ at the time, was later ______ when the market collapsed exactly as the "
  "chairman had predicted.",
  ["applauded, vindicated", "derided, vindicated", "derided, refuted", "praised, discredited"], "B",
  "Double blank: 'though' sets the first reaction against the later judgement",
  "Events proved the chairman right, so the decision was later shown to be correct: 'vindicated'. 'Though' needs the "
  "first reaction to be the opposite: the decision was mocked, 'derided', at the time.",
  ["Later: the market collapsed as predicted → the decision was proved right (vindicated)",
   "'though' → the earlier reaction was negative (derided)", "'derided, vindicated'"],
  "'Applauded, vindicated' loses the contrast that 'though' requires. 'Refuted' and 'discredited' contradict the "
  "prediction coming true.", 40)

Q(FB, "Phrase fillers", A,
  FBP + "The government is trying to ______ the fiscal deficit without cutting spending on welfare schemes.",
  ["egg on", "play up", "bank on", "rein in"], "D",
  "Phrasal verb: rein in = bring under control, restrain",
  "A government tries to control or reduce its deficit. To 'rein in' something is to restrain it, like pulling the "
  "reins of a horse.",
  ["Object: the fiscal deficit (something to be controlled)", "Meaning needed: restrain, reduce", "'rein in'"],
  "'Egg on' means urge someone to do something. 'Play up' means exaggerate. 'Bank on' means rely on. None means "
  "control a deficit.", 35)

Q(FB, "Single blank", A,
  FB1 + "The company's ______ approach to compliance, fixing problems only after the regulator had found them, "
  "eventually cost it its licence.",
  ["proactive", "exhaustive", "punctilious", "reactive"], "D",
  "Single blank: the participle phrase defines the word",
  "Fixing problems only after someone else finds them is acting in response to events rather than in advance: a "
  "'reactive' approach.",
  ["Description: fixing problems only after they are found", "Responding, not anticipating", "'reactive'"],
  "'Proactive' is the opposite (acting in advance). 'Exhaustive' and 'punctilious' (very thorough, very careful) "
  "contradict the careless approach that cost the licence.", 35)

Q(FB, "Double blank", A,
  FB2 + "The senior partner's ______ advice, offered only after long reflection, was in sharp contrast to the ______ "
  "suggestions of the younger staff, who wanted to act at once.",
  ["considered, impetuous", "hasty, impetuous", "considered, deliberate", "rash, measured"], "A",
  "Double blank: 'in sharp contrast' requires opposite qualities, each defined by its own phrase",
  "Advice 'offered only after long reflection' is 'considered'. Suggestions from people who 'wanted to act at once' "
  "are 'impetuous' (rash). The two are opposites, as 'in sharp contrast' requires.",
  ["Blank 1: after long reflection → considered", "Blank 2: wanting to act at once → impetuous",
   "Contrast confirmed: 'considered, impetuous'"],
  "'Hasty, impetuous' removes the contrast and contradicts 'long reflection'. 'Considered, deliberate' also removes "
  "the contrast. 'Rash, measured' reverses the two descriptions.", 40)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"
WS_STEM = ("In the sentence below, four words are in bold. Two of them may need to be interchanged to make the "
           "sentence meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n")

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'loose' used correctly?",
  ["Do not loose your passbook; a new one takes a week.",
   "If you loose the receipt, you cannot claim a refund.",
   "He was afraid that he would loose his job.",
   "The handle on the cash drawer has come loose."], "D",
  "Loose (adjective: not firmly fixed) vs lose (verb: be unable to find; fail to keep)",
  "'Loose' is an adjective meaning not tight or not firmly attached. A handle that 'has come loose' is no longer "
  "firmly fixed.",
  ["A: misplace the passbook → 'lose'", "B: misplace the receipt → 'lose'",
   "C: fail to keep his job → 'lose'", "D: not firmly fixed → 'loose': correct"],
  "A, B and C all need the verb 'lose' (misplace, fail to keep). 'Loose' is not a verb in these senses.", 25)

Q(WU, "Word swap", B,
  WS_STEM + "The **(A) farmer** ploughed his **(B) tractor** with a new **(C) field** before the **(D) monsoon**.",
  ["B-C", "A-B", "C-D", "No swap required"], "A",
  "Word swap: check what can be ploughed and what one ploughs with",
  "One ploughs a field with a tractor, not a tractor with a field. Swapping B and C gives: 'The farmer ploughed his "
  "field with a new tractor before the monsoon.'",
  ["'ploughed his tractor' is meaningless", "'with a new field' is meaningless", "Swap B and C"],
  "A-B gives 'The tractor ploughed his farmer'. C-D gives 'with a new monsoon before the field'. The sentence clearly "
  "needs a swap.", 30)

Q(WU, "Correct usage of a word", B,
  "In which of the following sentences is the word 'adapt' used correctly?",
  ["The couple decided to adapt a baby girl from the orphanage.",
   "The board voted to adapt the new policy at once.",
   "It took the new clerk a month to adapt to the night shift.",
   "Many villagers have now adapted digital payments."], "C",
  "Adapt (adjust to new conditions) vs adopt (take up, accept, or legally take a child as one's own)",
  "To 'adapt to' something is to adjust to new conditions. A clerk getting used to the night shift adapts to it.",
  ["A: take a child as one's own → 'adopt'", "B: accept a policy → 'adopt'",
   "C: adjust to new conditions → 'adapt to': correct", "D: take up a new practice → 'adopted'"],
  "A, B and D describe taking something up or accepting it, which is 'adopt'.", 30)

Q(WU, "Word swap", I,
  WS_STEM + "The **(A) interest** on the loan was **(B) calculated** at a fixed **(C) rate**, so the **(D) borrower** "
  "knew in advance how much he would pay.",
  ["A-C", "B-D", "A-D", "No swap required"], "D",
  "Word swap: test each bold word in its own slot before swapping",
  "Interest is calculated at a rate, and the borrower knows in advance what he will pay. Every bold word fits its "
  "place, so no swap is needed.",
  ["'The interest ... was calculated': correct", "'at a fixed rate': correct", "'the borrower knew': correct",
   "No swap required"],
  "A-C gives 'The rate on the loan was calculated at a fixed interest', which garbles the meaning. B-D and A-D "
  "produce nonsense ('The borrower ... was interest').", 35)

Q(WU, "Correct usage of a word", I,
  "In which of the following sentences is the word 'assure' (or 'assured') used correctly?",
  ["Please assure that all the doors are locked before you leave.",
   "The manager assured the customers that their deposits were safe.",
   "He assured his car against theft and fire.",
   "She assured that the form was complete before submitting it."], "B",
  "Assure (tell someone confidently to remove doubt) vs ensure (make certain) vs insure (protect with insurance)",
  "'Assure' takes a person as its object: you assure someone that something is true. 'The manager assured the "
  "customers that their deposits were safe' is correct.",
  ["A: make certain → 'ensure that'", "B: told the customers confidently → 'assured': correct",
   "C: protect with insurance → 'insured'", "D: made certain → 'ensured'"],
  "A and D need 'ensure' (make certain), and C needs 'insure' (cover with insurance). None of them has a person "
  "being told something to remove doubt.", 35)

Q(WU, "Correct usage of a word", A,
  "In which of the following sentences is the word 'fortuitous' used correctly?",
  ["We were fortuitous to get the last two seats on the bus.",
   "The fortuitous planning of the event impressed every guest.",
   "Their meeting at the airport was entirely fortuitous; neither knew the other was travelling.",
   "He worked fortuitously through the night to finish the audit."], "C",
  "Fortuitous = happening by chance, not by design",
  "A meeting that neither person expected or arranged happened by chance: it was 'fortuitous'.",
  ["A: describes people as lucky → 'fortunate'", "B: planning cannot happen by chance",
   "C: an unplanned chance meeting → 'fortuitous': correct", "D: working hard through the night is deliberate"],
  "A uses it of people (it describes events). B contradicts 'planning'. D applies it to deliberate effort.", 40)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", B,
  "Choose the meaning of the word 'tally' as used in the sentence:\n"
  "'At the end of the day, the cashier must tally the cash in the drawer with the figures in the ledger.'",
  ["count roughly", "hide safely", "hand over", "match and check"], "D",
  "Tally (verb) = check that two sets of figures agree",
  "The cashier compares the cash with the ledger to make sure the two agree. To 'tally' one with the other is to "
  "match and check them.",
  ["Two things compared: cash and ledger figures", "Purpose: make sure they agree", "'match and check'"],
  "'Count roughly' contradicts the exactness of a daily check. 'Hide safely' and 'hand over' do not involve comparing "
  "the cash with the ledger.", 25)

Q(VO, "Contextual meaning", I,
  "Choose the meaning of the word 'deter' as used in the sentence:\n"
  "'The new reporting rule is expected to deter people from keeping large amounts of unaccounted cash at home.'",
  ["discourage", "encourage", "permit", "remind"], "A",
  "Deter = discourage someone from doing something, usually through fear of consequences",
  "A rule that makes people report their cash is meant to make keeping unaccounted cash less attractive. 'Deter "
  "from' means discourage from.",
  ["Pattern: deter + person + from + -ing", "Purpose of the rule: fewer people keeping unaccounted cash",
   "'discourage'"],
  "'Encourage' is the opposite. 'Permit' and 'remind' do not fit 'from keeping' and do not describe the aim of the "
  "rule.", 25)

Q(VO, "Word pairs", I, "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Garrulous – Reticent", "Opaque – Lucid", "Frugal – Thrifty", "Diligent – Indolent"], "C",
  "Word pairs: identify synonyms and antonyms",
  "'Frugal' and 'thrifty' both mean careful with money and avoiding waste. The other pairs are opposites.",
  ["Garrulous (talkative) ≠ reticent (reserved)", "Opaque (unclear) ≠ lucid (clear)",
   "Frugal = thrifty (economical)", "Diligent (hard-working) ≠ indolent (lazy)"],
  "A, B and D are pairs of opposites, not synonyms.", 30)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", I,
  SY_STEM + "Before the merger, the bank raised fresh equity to **bolster** its capital base.",
  ["reveal", "strengthen", "reduce", "value"], "B",
  "Bolster = support, strengthen",
  "Raising fresh equity adds to the bank's capital, making its capital base stronger. 'Bolster' means strengthen or "
  "support.",
  ["Context: raising fresh equity adds capital", "'bolster' = strengthen", "Closest: 'strengthen'"],
  "'Reduce' is the opposite. 'Reveal' and 'value' do not describe what new equity does to the capital base.", 25)

Q(SY, "Contextual synonym", A,
  SY_STEM + "The minister's **sanctimonious** lecture on thrift annoyed voters who knew of his lavish lifestyle.",
  ["sincere", "sensible", "sympathetic", "self-righteous"], "D",
  "Sanctimonious = making a show of being morally better than others",
  "A minister who lectures others on thrift while living lavishly is acting morally superior without practising what "
  "he preaches. 'Sanctimonious' means self-righteous in this way.",
  ["Context: preaching thrift while living lavishly", "Annoyance at the moral superiority",
   "Closest: 'self-righteous'"],
  "'Sincere' contradicts his hypocrisy. 'Sensible' and 'sympathetic' would not annoy voters and miss the idea of "
  "moral superiority.", 30)

Q(AN, "Contextual antonym", B,
  AN_STEM + "The branch was **crowded** on the first working day of the month, when pensions are paid.",
  ["packed", "busy", "deserted", "full"], "C",
  "Crowded = full of people; antonym: deserted",
  "A 'crowded' branch is full of people. The opposite is 'deserted', with nobody there.",
  ["'crowded' = full of people", "Opposite = empty of people: 'deserted'"],
  "'Packed', 'busy' and 'full' are all close in meaning to 'crowded'.", 20)

Q(AN, "Contextual antonym", I,
  AN_STEM + "The officer gave a **concise** summary of the new rules at the start of the meeting.",
  ["long-winded", "brief", "crisp", "short"], "A",
  "Concise = giving much information in few words; antonym: long-winded",
  "A 'concise' summary is short and to the point. The opposite is 'long-winded', using far more words than needed.",
  ["'concise' = brief and clear", "Opposite = wordy, tediously long: 'long-winded'"],
  "'Brief', 'crisp' and 'short' are all close in meaning to 'concise'.", 25)

Q(AN, "Contextual antonym", A,
  AN_STEM + "The auditor was praised for her **scrupulous** attention to every entry in the accounts.",
  ["meticulous", "slipshod", "thorough", "painstaking"], "B",
  "Scrupulous = extremely careful and thorough; antonym: slipshod",
  "'Scrupulous' attention leaves nothing unchecked. The opposite is 'slipshod', careless and sloppy.",
  ["'scrupulous' = very careful", "Opposite = careless: 'slipshod'"],
  "'Meticulous', 'thorough' and 'painstaking' are all close in meaning to 'scrupulous'.", 25)

Q(AN, "Contextual antonym", A,
  AN_STEM + "The new chairman's **magnanimous** decision to forgive his former critics surprised everyone.",
  ["generous", "noble", "big-hearted", "petty"], "D",
  "Magnanimous = generous in forgiving, free from resentment; antonym: petty",
  "Forgiving one's critics is a 'magnanimous' act. The opposite is 'petty', small-minded and unwilling to let go of "
  "minor grievances.",
  ["'magnanimous' = generous-spirited", "Opposite = small-minded: 'petty'"],
  "'Generous', 'noble' and 'big-hearted' are all close in meaning to 'magnanimous'.", 25)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"

Q(ID, "Meaning of idiom", B,
  "Choose the meaning of the idiom 'to break the ice'.",
  ["to ease the first awkwardness when people meet", "to break a promise", "to cool down an angry person",
   "to start a quarrel"], "A",
  "Idiom: break the ice = say or do something to relieve tension when people first meet",
  "To 'break the ice' is to make people feel more relaxed at the start of a meeting. For example: 'The trainer broke "
  "the ice by asking each new recruit about his home town.'",
  ["Image: breaking a frozen surface so movement can begin", "Meaning: ease the first awkwardness"],
  "B, C and D take the image of ice loosely. None captures the idea of putting people at ease when they first "
  "meet.", 20)

Q(ID, "Idiom in context", I,
  "Choose the meaning of the idiom in bold.\n"
  "With the year-end audit and two staff vacancies, the new branch manager **has his hands full**.",
  ["is very generous", "has stolen something", "is extremely busy", "is fully in control"], "C",
  "Idiom: have one's hands full = be very busy, with as much as one can manage",
  "An audit and two vacancies leave the manager with as much work as he can handle: he 'has his hands full'.",
  ["Context: audit + two vacancies = heavy workload", "Idiom: very busy"],
  "'Very generous' and 'has stolen something' read the image of full hands literally. 'Fully in control' misses the "
  "sense of being overloaded.", 25)

Q(ID, "Meaning of idiom", A,
  "Choose the meaning of the idiom 'to throw the baby out with the bathwater'.",
  ["to punish a child too harshly", "to waste water carelessly",
   "to blame others for one's own mistake",
   "to discard something valuable while getting rid of something unwanted"], "D",
  "Idiom: throw the baby out with the bathwater = reject the good along with the bad",
  "When people reject a whole plan or system because of one flaw, losing its useful parts too, they 'throw the baby "
  "out with the bathwater'. For example: 'Scrapping the whole scheme over a few billing errors would be throwing the "
  "baby out with the bathwater.'",
  ["Image: the baby (valuable) and the dirty water (unwanted)", "Meaning: losing the good while removing the bad"],
  "A and B take the image literally. C describes shifting blame, which the idiom does not mean.", 25)

Q(ID, "Idiom in context", A,
  "Choose the meaning of the idiom in bold.\n"
  "By refusing to sell through online stores because it disliked their fees, the company was **cutting off its nose "
  "to spite its face**.",
  ["cutting its costs sensibly", "harming itself out of anger at others",
   "changing its brand image", "punishing its dishonest staff"], "B",
  "Idiom: cut off one's nose to spite one's face = harm oneself in trying to hurt or punish someone else",
  "To show displeasure at the stores' fees, the company gave up the sales it could have made through them. It hurt "
  "itself more than it hurt the stores.",
  ["Context: refusing a sales channel out of annoyance", "Effect: the company loses sales",
   "Idiom: self-harm driven by spite"],
  "'Cutting its costs sensibly' misses the self-harm. 'Changing its brand image' takes 'face' loosely. 'Punishing "
  "its dishonest staff' has no link with the context.", 30)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", B,
  OW_STEM + "A place where coins and currency notes are officially made",
  ["treasury", "vault", "mint", "mine"], "C",
  "One-word substitution: money terms",
  "A 'mint' is a place where a government makes its coins (and, in some countries, notes).",
  ["Key idea: where money is made", "Word: mint"],
  "A 'treasury' manages or stores public money. A 'vault' is a secure room for keeping valuables. A 'mine' is where "
  "minerals are dug out.", 20)

Q(OW, "Single word for a phrase", B,
  OW_STEM + "A person who is travelling on foot, especially in a town",
  ["pedestrian", "passenger", "pilgrim", "commuter"], "A",
  "One-word substitution: travellers",
  "A 'pedestrian' is a person walking, especially along a road or street.",
  ["Key idea: travelling on foot", "Word: pedestrian"],
  "A 'passenger' travels in a vehicle driven by someone else. A 'pilgrim' travels to a holy place. A 'commuter' "
  "travels regularly between home and work, usually by vehicle.", 20)

Q(OW, "Single word for a phrase", I,
  OW_STEM + "Government by a small group of powerful people",
  ["monarchy", "democracy", "anarchy", "oligarchy"], "D",
  "One-word substitution: forms of government",
  "An 'oligarchy' is a system in which power rests with a small group of people (from Greek 'oligoi', few).",
  ["Key idea: rule by a few", "Word: oligarchy"],
  "A 'monarchy' is rule by a king or queen. A 'democracy' is rule by the people. 'Anarchy' is the absence of "
  "government.", 20)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", I, AP_STEM + "Did the regional manager approve your transfer?",
  ["Did your transfer approved by the regional manager?",
   "Was your transfer approved by the regional manager?",
   "Has your transfer been approved by the regional manager?",
   "Was your transfer being approved by the regional manager?"], "B",
  "Passive of a simple past 'Did' question: Was/Were + object + past participle + by + agent?",
  "In the passive, 'did ... approve' becomes 'was ... approved', and the question order is kept by putting 'Was' "
  "first: 'Was your transfer approved by the regional manager?'",
  ["Tense: simple past", "Passive: was + past participle", "Question order: Was + subject + approved ...?"],
  "A keeps 'Did', which cannot form a passive. C changes the tense to the present perfect. D changes it to the past "
  "continuous.", 30)

Q(AP, "Voice conversion", A, AP_STEM + "Nobody has ever seen him lose his temper.",
  ["He has never been seen lose his temper.",
   "He has ever been seen to lose his temper by nobody.",
   "He has never been seen to lose his temper.",
   "His temper has never been seen to lose by anybody."], "C",
  "Passive of 'see + object + bare infinitive': the infinitive takes 'to' in the passive; 'nobody ... ever' becomes "
  "'never'",
  "The object 'him' becomes the subject 'He'. 'Has seen' becomes 'has been seen', and the bare infinitive 'lose' "
  "becomes 'to lose'. The negative agent 'Nobody' is dropped and its negation moves to the verb: 'never'.",
  ["Subject: He", "'Nobody has ever seen' → 'has never been seen'", "Bare infinitive → 'to lose'"],
  "A keeps the bare infinitive, which is not used after a passive 'seen'. B keeps 'by nobody', which is "
  "ungrammatical with 'ever'. D makes 'his temper' the thing that loses, which changes the meaning.", 40)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", I,
  DS_STEM + "(Reported a week later) She said, \"I have to finish the audit report today.\"",
  ["She said that she had to finish the audit report that day.",
   "She said that she has to finish the audit report today.",
   "She said that I had to finish the audit report that day.",
   "She said that she had to finished the audit report that day."], "A",
  "Reported statement: 'have to' → 'had to'; first person → third person; 'today' → 'that day'",
  "With a past reporting verb, 'have to' is backshifted to 'had to', 'I' becomes 'she', and 'today' becomes 'that "
  "day': 'She said that she had to finish the audit report that day.'",
  ["'I' → 'she'", "'have to' → 'had to'", "'today' → 'that day'"],
  "B keeps the present tense and 'today', which cannot be right when the words are reported a week later. C keeps "
  "'I'. D puts a past form ('finished') after 'to'.", 30)

Q(DS, "Narration change", A, DS_STEM + "He said to me, \"Congratulations! You have passed the examination.\"",
  ["He congratulated me that I have passed the examination.",
   "He said me congratulations for passing the examination.",
   "He congratulated to me for I had passed the examination.",
   "He congratulated me on having passed the examination."], "D",
  "Reporting greetings and wishes: 'Congratulations!' → 'congratulated + object + on + -ing'",
  "An expression such as 'Congratulations!' is reported with the verb 'congratulate', which takes 'on' + a noun or "
  "-ing form: 'He congratulated me on having passed the examination.' The perfect gerund shows that the passing came "
  "first.",
  ["'Congratulations!' → 'congratulated me'", "Pattern: congratulate + person + on + -ing",
   "'You have passed' → 'on having passed'"],
  "A uses a 'that' clause after 'congratulated' and keeps 'have'. B uses 'said me'. C uses 'to me' and 'for I had', "
  "neither of which fits 'congratulate'.", 40)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", B, SV_STEM + "A lot of the money collected for the flood victims ______ been misused.",
  ["have", "are", "has", "were"], "C",
  "'A lot of' takes its number from the noun that follows: uncountable noun → singular verb",
  "'A lot of' can go with plural or uncountable nouns; the verb agrees with that noun. 'Money' is uncountable, so "
  "the verb is singular: 'A lot of the money ... has been misused.'",
  ["Noun after 'a lot of': 'money' (uncountable)", "Uncountable → singular verb", "'has been misused'"],
  "'Have' and 'were' are plural. 'Are been' is not a verb form.", 25)

Q(SV, "Agreement rules", B, SV_STEM + "One of the ATMs near the railway station ______ out of order since Monday.",
  ["has been", "have been", "are", "were"], "A",
  "'One of the + plural noun' takes a singular verb, because the subject is 'one'",
  "The subject is 'One', not 'ATMs', so the verb is singular. 'Since Monday' needs the present perfect: 'One of the "
  "ATMs ... has been out of order since Monday.'",
  ["Subject: 'One' (singular)", "'since Monday' → present perfect", "'has been'"],
  "'Have been' is plural. 'Are' and 'were' are plural and also do not go with 'since Monday'.", 25)

Q(SV, "Agreement rules", I, SV_STEM + "The majority of the bank's depositors in this town ______ senior citizens.",
  ["is", "are", "has", "was"], "B",
  "'The majority of' + plural noun takes a plural verb",
  "When 'the majority of' is followed by a plural noun ('depositors'), the verb is plural: 'The majority of the "
  "bank's depositors ... are senior citizens.' The plural complement 'senior citizens' confirms this.",
  ["Noun after 'the majority of': 'depositors' (plural)", "Plural → plural verb", "'are'"],
  "'Is', 'has' and 'was' are singular. ('Has senior citizens' also makes no sense.)", 30)

Q(SV, "Agreement rules", A, SV_STEM + "The main cause of the delays at the counters ______ the frequent server "
  "failures.",
  ["were", "are", "have been", "was"], "D",
  "With a linking verb, the verb agrees with the subject before it, not with the complement after it",
  "The subject is 'The main cause' (singular); 'of the delays' and the complement 'the frequent server failures' do "
  "not change it. So the verb is singular: 'The main cause of the delays ... was the frequent server failures.'",
  ["Subject: 'The main cause' (singular head noun)", "Ignore 'of the delays' and the plural complement",
   "Singular verb: 'was'"],
  "'Were', 'are' and 'have been' are plural, agreeing wrongly with 'delays' or 'failures'.", 35)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Sequence of tenses", B, TE_STEM + "Look at those dark clouds over the hills! It ______ rain.",
  ["is going to", "rains", "rained", "has rained"], "A",
  "'Be going to' for a prediction based on present evidence",
  "The dark clouds are present evidence that rain is about to come. A prediction based on what we can see now is "
  "expressed with 'be going to': 'It is going to rain.'",
  ["Evidence now: dark clouds", "Prediction about the near future", "'is going to rain'"],
  "'Rains' is the simple present for habits or facts. 'Rained' and 'has rained' refer to the past, which clashes with "
  "clouds that have not yet produced rain.", 20)

Q(TE, "Perfect tenses", I,
  TE_STEM + "I ______ three loan reports since this morning, and I am now working on the fourth.",
  ["have been writing", "have written", "wrote", "had written"], "B",
  "Present perfect (not continuous) for a number of completed actions up to now",
  "'Three reports' are finished and counted, and the period ('since this morning') runs up to now. A count of "
  "completed actions takes the present perfect simple: 'I have written three loan reports.'",
  ["'since this morning' → a period up to now", "'three reports' = completed and counted",
   "Present perfect simple: 'have written'"],
  "'Have been writing' focuses on an ongoing activity and is not used with a number of completed items. 'Wrote' "
  "cannot go with 'since this morning'. 'Had written' places the action before another past moment.", 30)

Q(TE, "Sequence of tenses", I,
  TE_STEM + "The new branch, which ______ in March, finally opened in June after several delays.",
  ["is opening", "will open", "was to open", "has opened"], "C",
  "'Was/were to + base verb' for a plan in the past (future in the past), often one that did not happen as planned",
  "The opening was planned for March but happened in June. Speaking from a past viewpoint about a planned event, we "
  "use 'was to open' (= was scheduled to open).",
  ["The narrative is in the past ('finally opened in June')", "March was the planned date",
   "Future in the past: 'was to open'"],
  "'Is opening' and 'will open' are present and future forms that clash with the past narrative. 'Has opened' "
  "cannot go with the past date 'in March' or with 'finally opened in June'.", 35)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", B, AR_STEM + "The new clerk earns twenty-five thousand rupees ______ month.",
  ["the", "an", "no article", "a"], "D",
  "'A' or 'an' meaning 'per' with rates (a month, an hour, twice a day)",
  "With amounts and rates, 'a' (or 'an' before a vowel sound) means 'each' or 'per': 'twenty-five thousand rupees a "
  "month'.",
  ["Pattern: amount + a/an + unit of time", "'month' begins with a consonant sound → 'a'", "'a month'"],
  "'The month' would refer to one particular month. 'An' is used before a vowel sound. With no article, 'rupees "
  "month' is ungrammatical.", 20)

Q(AR, "Definite and indefinite", I,
  AR_STEM + "The children go to ______ school by bus, but yesterday their parents went to ______ school to meet the "
  "principal.",
  ["no article, the", "the, the", "the, no article", "no article, no article"], "A",
  "No article with school, church, college or prison used for their main purpose; 'the' when the building is visited "
  "for another reason",
  "Children go to school as pupils, so no article is used. The parents went to the building only to meet the "
  "principal, not as pupils, so it is 'the school'.",
  ["Blank 1: children go as pupils → no article", "Blank 2: parents visit the building → 'the'",
   "Option A"],
  "B and C put 'the' before the children's 'school'. C and D drop the 'the' needed for the parents' visit to the "
  "building.", 30)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", I,
  PP_STEM + "The rules adopted at the general meeting are binding ______ all members of the society.",
  ["to", "on", "for", "with"], "B",
  "Fixed preposition: 'binding on' (or 'binding upon') = must be obeyed by",
  "A rule that members must obey is 'binding on' them: 'The rules ... are binding on all members of the society.'",
  ["Adjective: 'binding' (must be obeyed)", "Fixed pairing: 'binding on/upon'"],
  "'Binding to', 'binding for' and 'binding with' are not the standard pattern.", 25)

Q(PP, "Phrasal verbs", I,
  PP_STEM + "Before signing the report, the audit team will ______ the accounts of the last three years.",
  ["go off", "go by", "go through", "go after"], "C",
  "Phrasal verb: go through = examine carefully",
  "An audit team examines accounts in detail before signing its report. To 'go through' documents is to examine them "
  "carefully.",
  ["Object: the accounts", "Meaning needed: examine in detail", "'go through'"],
  "'Go off' means explode, ring or go bad. 'Go by' means pass (of time) or follow. 'Go after' means chase.", 25)

Q(PP, "Fixed prepositions", A,
  PP_STEM + "The release of the second instalment of the loan is contingent ______ the completion of the first floor.",
  ["on", "of", "with", "to"], "A",
  "Fixed preposition: 'contingent on' (or 'upon') = depending on a condition",
  "The second instalment will be released only if the first floor is completed. 'Contingent' takes 'on' or 'upon': "
  "'contingent on the completion of the first floor'.",
  ["Adjective: 'contingent' (dependent on a condition)", "Fixed pairing: 'contingent on/upon'"],
  "'Contingent of' is a noun use (a group, as in 'a contingent of soldiers'). 'Contingent with' and 'contingent to' "
  "are not standard.", 30)

Q(PP, "Phrasal verbs", A,
  PP_STEM + "No apology from the bank could ______ the loss of trust caused by the fraud.",
  ["make off with", "make out", "make over", "make up for"], "D",
  "Phrasal verb: make up for = compensate for something lost or bad",
  "An apology would be an attempt to compensate for the damage done to trust. 'Make up for' means compensate for.",
  ["Object: the loss of trust", "Meaning needed: compensate for", "'make up for'"],
  "'Make off with' means steal and run away. 'Make out' means manage to see or understand. 'Make over' means "
  "transfer or remodel.", 30)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"

Q(CN, "Sentence connectors", B,
  "Choose the connector that best fills the blank.\n"
  "He missed the first bus to the branch ______ he woke up late.",
  ["although", "because", "unless", "so"], "B",
  "'Because' introduces a reason",
  "Waking up late is the reason he missed the bus. 'Because' introduces a reason clause.",
  ["Clause 1: missed the bus (result)", "Clause 2: woke up late (cause)", "Cause → 'because'"],
  "'Although' signals contrast and 'unless' a condition. 'So' introduces a result, which would make missing the bus "
  "the cause of waking late.", 20)

Q(CN, "Sentence connectors", B,
  "Choose the connector that best fills the blank.\n"
  "You cannot withdraw cash from the ATM ______ you enter the correct PIN.",
  ["because", "while", "unless", "if"], "C",
  "'Unless' = except if",
  "Entering the correct PIN is the condition without which no cash can be withdrawn. 'You cannot withdraw cash "
  "unless you enter the correct PIN' means you can withdraw only if you enter it.",
  ["Main clause: negative ('cannot withdraw')", "The only exception: entering the correct PIN",
   "'unless'"],
  "'If' would say that entering the correct PIN stops the withdrawal. 'Because' gives the PIN as the reason for "
  "failure. 'While' only links the two in time.", 20)

Q(CN, "Sentence connectors", B,
  "Choose the connector that best fills the blank.\n"
  "______ standing in the long queue, he paid the electricity bill on his phone.",
  ["Instead of", "In spite of", "Because of", "In addition to"], "A",
  "'Instead of' + -ing = in place of doing something",
  "He paid on his phone in place of standing in the queue. 'Instead of' shows that one action replaces the other.",
  ["Two ways of paying: queue or phone", "He chose the phone in place of the queue", "'Instead of'"],
  "'In spite of' suggests he stood in the queue and still paid by phone, which is illogical. 'Because of' makes "
  "standing in the queue the reason. 'In addition to' says he did both.", 25)

Q(CN, "Starters and linkers", I,
  "Combine the two sentences into one without changing the meaning, and choose the option that correctly begins the "
  "combined sentence.\n"
  "You must submit the claim form by Friday. Otherwise, your claim will be rejected.",
  ["Unless you do not submit the claim form by Friday,", "If you submit the claim form by Friday,",
   "Until you submit the claim form by Friday,", "Unless you submit the claim form by Friday,"], "D",
  "'Otherwise' (= if not) becomes 'Unless' (= if ... not) in a combined sentence",
  "'Submit by Friday; otherwise your claim will be rejected' means 'If you do not submit by Friday, your claim will "
  "be rejected', which is 'Unless you submit the claim form by Friday, your claim will be rejected.'",
  ["'Otherwise' = if you do not do this", "'if ... not' = 'unless'", "'Unless you submit the claim form by Friday, ...'"],
  "A adds 'not' after 'unless', giving a double negative. B reverses the meaning: submitting on time would lead to "
  "rejection. C ('Until') does not express a condition.", 35)

Q(CN, "Sentence connectors", I,
  "Choose the connector that best fills the blank.\n"
  "The bank's engineers spent the night repairing the main server. ______, customers were asked to use the branch "
  "counters for urgent payments.",
  ["Therefore", "Meanwhile", "Nevertheless", "Besides"], "B",
  "'Meanwhile' = during the same period of time",
  "While the server was being repaired, customers were sent to the counters. 'Meanwhile' links two things happening "
  "during the same time.",
  ["Event 1: engineers repairing the server", "Event 2: customers using counters during that time",
   "Same period → 'Meanwhile'"],
  "'Therefore' would make the repair the reason for the request, which hides the link in time; the cause is the "
  "server failure, not the repair. 'Nevertheless' signals contrast. 'Besides' adds a further point.", 30)

Q(CN, "Sentence connectors", A,
  "Choose the connector that best fills the blank.\n"
  "______ the new scheme is well funded, it will fail if the branch staff are not trained to explain it.",
  ["Only if", "As long as", "Even if", "Since"], "C",
  "'Even if' = whether or not this is true, the result does not change",
  "Good funding does not prevent failure when staff are untrained. 'Even if' concedes the funding while saying the "
  "outcome is still failure.",
  ["Clause 1: a favourable condition (well funded)", "Clause 2: failure still possible",
   "Concession → 'Even if'"],
  "'Only if' and 'As long as' would make funding the condition for failure, which is illogical. 'Since' would give "
  "funding as the reason for failure.", 30)

Q(CN, "Starters and linkers", A,
  "Combine the two sentences into one without changing the meaning, and choose the option that correctly begins the "
  "combined sentence.\n"
  "The bank lowered its service charges. It also extended its working hours.",
  ["In addition to lowering its service charges,", "In addition to lower its service charges,",
   "Besides it lowered its service charges,", "Apart to lowering its service charges,"], "A",
  "'In addition to' / 'besides' / 'apart from' are prepositions and take a noun or -ing form",
  "'In addition to' ends in the preposition 'to', so it is followed by a gerund: 'In addition to lowering its "
  "service charges, the bank extended its working hours.'",
  ["Relation: addition (two improvements)", "'In addition to' + -ing",
   "'In addition to lowering its service charges, ...'"],
  "B uses a base verb after the preposition 'to'. C uses 'Besides' (a preposition here) before a full clause. D "
  "uses 'Apart to' instead of 'Apart from'.", 35)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_005_plan.json").read_text(encoding="utf-8"))
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
    assert len({o["text"] for o in q["options"]}) == 4, q["question_id"]

# no reused stem or passage title across the earlier English files (BATCH_000 to BATCH_004)
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
# against 'A net or a hammock' (6 of 12 keywords shared), while unrelated passages share at most 3.
STOP = set("about after again against among because before being between bring could every first found great large "
           "later might money other people place price prices still their there these thing those three through "
           "under until where which while whose would years often never since cannot always".split())


def theme_words(text):
    words = [w.strip(".,;:'\"()!?*-\u2014\u2013").lower() for w in text.split()]
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
    "batch_id": "BATCH_005",
    "created_at": TODAY,
    "notes": "BATCH_005 English Language part: 150 original questions (BANK_ENG_000604 to BANK_ENG_000753). Six "
             "reading passages (29 questions) and three cloze passages (18 blanks, one set error-based), all written "
             "for PrepMitra on themes not used in BATCH_000 to BATCH_004; the rest are standalone grammar, "
             "vocabulary and sentence-ordering items testing rules, words and idioms not tested in earlier batches. "
             "Each answer was set by the author and re-solved in a separate blind pass by fresh checkers without the "
             "key. Pending human review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_005_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))})")
