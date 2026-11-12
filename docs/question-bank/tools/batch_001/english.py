"""Writes batches/parts/BATCH_001_ENG.json: the 150 English Language questions of BATCH_001.

All passages, sentences and items are original PrepMitra content. Run from anywhere:

    python docs/question-bank/tools/batch_001/english.py

Structural checks (quota per topic and difficulty, passage length, set sizes, option count, answer-key balance) are
asserted before anything is written.
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
FIRST_ID = 4
FIRST_STIM = 2

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

# =====================================================================================================================
# READING COMPREHENSION
# =====================================================================================================================

# ---------------------------------------------------------------- RC 1 (Basic, 5)
P1 = stim("The bank at the village shop", (
    "In many Indian villages, the nearest bank branch is still several kilometres away, and a trip to it can cost a "
    "farmer or a daily-wage worker a full day's earnings. To bridge this gap, banks appoint business correspondents: "
    "local shopkeepers, retired teachers or members of self-help groups who are trained to offer basic banking "
    "services from their own premises. Equipped with a biometric device and a small terminal, a correspondent can "
    "open a savings account, accept deposits, pay out small withdrawals and help villagers receive government "
    "benefits directly in their accounts.\n\n"
    "The model has clear advantages. Because the correspondent is a familiar face, people who once felt nervous about "
    "entering a bank are more willing to save. Transactions happen close to home and at hours that suit working "
    "people, often in the evening after work in the fields is over. For the bank, the cost of serving a customer "
    "through a correspondent is a fraction of the cost of running a full branch.\n\n"
    "The arrangement is not without problems, however. Correspondents earn a commission on each transaction, and in "
    "areas where transactions are few and small, the income may not be enough to keep them interested. Network "
    "failures can leave a customer waiting for hours, and when the cash at the counter runs short, withdrawals are "
    "delayed. Some customers also complain that they do not receive a printed receipt and therefore cannot check "
    "whether their money has been recorded correctly.\n\n"
    "Experts argue that the solution lies in better pay for correspondents, reliable connectivity and simple ways for "
    "customers to verify every transaction on their phones. If these gaps are filled, the village shop may become as "
    "trusted as the bank itself."))

Q(RC, "Factual", "Basic",
  "According to the passage, which of the following is NOT mentioned as a service offered by a business "
  "correspondent?",
  ["Opening a savings account", "Accepting deposits", "Sanctioning crop loans",
   "Helping villagers receive government benefits"], "C",
  "Factual (NOT) question: eliminate every option the passage states",
  "The first paragraph lists the correspondent's services: opening savings accounts, accepting deposits, paying "
  "small withdrawals and helping villagers receive government benefits. Sanctioning crop loans is never mentioned.",
  ["Locate the list of services in paragraph 1",
   "Tick off the options found there: account opening, deposits, government benefits",
   "Crop loans do not appear anywhere in the passage, so C is the answer"],
  "A, B and D are all named in the first paragraph as services a correspondent provides, so they cannot be the "
  "'NOT mentioned' answer.", 60, P1, 1)

Q(RC, "Factual", "Basic",
  "Why, according to the passage, are villagers more willing to save through a business correspondent?",
  ["Correspondents pay a higher rate of interest than bank branches.",
   "The correspondent is a familiar person, which reduces their nervousness.",
   "Government benefits can be received only through correspondents.",
   "Correspondents do not charge the bank any commission."], "B",
  "Locating a stated reason",
  "Paragraph 2 says that because the correspondent is a familiar face, people who once felt nervous about entering "
  "a bank are more willing to save.",
  ["Find the sentence about willingness to save: paragraph 2, sentence 2",
   "The reason given is familiarity, which removes nervousness",
   "Option B restates this"],
  "A: interest rates are never compared. C: the passage says correspondents help people receive benefits, not that "
  "this is the only channel. D: the passage says correspondents earn a commission on each transaction.", 60, P1, 2)

Q(RC, "Factual", "Basic",
  "Which of the following problems with the correspondent model is/are mentioned in the passage?\n"
  "(i) Low commission income in areas with few transactions\n"
  "(ii) Delays caused by network failures\n"
  "(iii) Correspondents refusing to serve elderly customers",
  ["Only (ii)", "Only (i) and (iii)", "All of (i), (ii) and (iii)", "Only (i) and (ii)"], "D",
  "Checking each statement against the passage",
  "Paragraph 3 mentions low commission income where transactions are few and small, and network failures that "
  "leave customers waiting. Nothing is said about correspondents refusing elderly customers.",
  ["(i): 'the income may not be enough to keep them interested': mentioned",
   "(ii): 'Network failures can leave a customer waiting for hours': mentioned",
   "(iii): not mentioned anywhere", "So only (i) and (ii): option D"],
  "A leaves out (i), which is clearly stated. B and C include (iii), which the passage never mentions.", 60, P1, 3)

Q(RC, "Vocabulary in context", "Basic",
  "Which of the following is most similar in meaning to the word 'bridge' as used in the passage ('To bridge this "
  "gap')?",
  ["close", "ignore", "widen", "measure"], "A",
  "Vocabulary in context: 'bridge a gap' means to reduce or close a gap",
  "Banks appoint correspondents to remove the distance between villagers and banking services. To 'bridge a gap' "
  "is to close it, so 'close' fits.",
  ["Read the sentence: the gap is the distance between villages and bank branches",
   "Correspondents are appointed to remove that distance", "'Bridge' here means close"],
  "'Ignore' and 'widen' are opposite to what the correspondents are meant to do. 'Measure' does not remove the gap "
  "at all.", 45, P1, 4)

Q(RC, "Tone and title", "Basic",
  "Which of the following best describes the author's view of the business correspondent model?",
  ["It has failed and should be replaced by more bank branches.",
   "It is perfect and needs no change.",
   "It is useful, but its shortcomings must be fixed for it to succeed fully.",
   "It benefits banks but offers nothing to villagers."], "C",
  "Author's overall view: weigh the advantages against the problems the passage lists",
  "The author lists clear advantages (paragraph 2), then real problems (paragraph 3), and ends by saying that if "
  "these gaps are filled the village shop may become as trusted as the bank. That is a balanced, positive-but-"
  "conditional view.",
  ["Paragraph 2: advantages for villagers and banks", "Paragraph 3: problems",
   "Paragraph 4: solutions, with a hopeful conclusion", "So the model is useful but needs fixing: C"],
  "A: the author never says the model failed or calls for more branches. B: paragraph 3 lists problems. D: "
  "paragraph 2 lists clear benefits to villagers.", 60, P1, 5)

# ---------------------------------------------------------------- RC 2 (Basic, 4)
P2 = stim("Saving the rain", (
    "Every monsoon, many Indian cities face a strange contradiction. Streets flood after a few hours of heavy rain, "
    "yet a few months later the same neighbourhoods queue up for water tankers. The reason is simple: most of the "
    "rain that falls on roofs, roads and paved courtyards runs straight into drains and is lost, while the "
    "groundwater that residents depend on in summer keeps falling year after year.\n\n"
    "Rainwater harvesting offers a low-cost way out of this cycle. In its simplest form, water from a rooftop is led "
    "through pipes into a filter and then into a storage tank or a recharge pit. Water stored in a tank can be used "
    "for washing and gardening, while water sent into a recharge pit seeps into the ground and gradually raises the "
    "water table. A house with a roof of a hundred square metres in a city that receives moderate rainfall can "
    "capture tens of thousands of litres in a single season.\n\n"
    "Several city governments have made rainwater harvesting compulsory for new buildings, but enforcement has been "
    "uneven. In many cases, structures are built only to obtain an approval certificate and are never cleaned or "
    "maintained afterwards. A recharge pit clogged with silt does little more than collect mosquitoes.\n\n"
    "The lesson from places where the practice has worked is that rules alone are not enough. Where resident "
    "associations take charge of maintenance, and where people can see the water level in their own borewells "
    "rising, harvesting becomes a habit rather than a formality. Public awareness, in short, matters as much as "
    "public regulation."))

Q(RC, "Factual", "Basic",
  "According to the passage, what happens to most of the rain that falls on roofs, roads and paved courtyards in "
  "cities?",
  ["It is stored in public tanks.", "It recharges the groundwater.", "It evaporates before it reaches the ground.",
   "It runs into drains and is lost."], "D",
  "Locating a stated fact",
  "The first paragraph says most of this rain 'runs straight into drains and is lost'.",
  ["Find the sentence beginning 'The reason is simple' in paragraph 1",
   "It says the rain runs into drains and is lost", "Option D matches"],
  "A and B describe what harvesting could achieve, not what happens now; the passage says groundwater keeps falling. "
  "C (evaporation) is not mentioned.", 60, P2, 1)

Q(RC, "Factual", "Basic",
  "According to the passage, water collected in a storage tank can be used for",
  ["washing and gardening", "drinking without any treatment", "cooling industrial machines",
   "supplying water tankers"], "A",
  "Locating a stated fact",
  "Paragraph 2 says water stored in a tank 'can be used for washing and gardening'.",
  ["Find the sentence about the storage tank in paragraph 2", "It names washing and gardening",
   "Option A matches"],
  "Drinking without treatment, industrial cooling and supplying tankers are not mentioned as uses of stored water.",
  60, P2, 2)

Q(RC, "Inference", "Basic",
  "What can be inferred about harvesting structures that are built 'only to obtain an approval certificate'?",
  ["They usually capture more water than is required.",
   "They are maintained by resident associations.",
   "They are often neglected and so stop working effectively.",
   "They are exempt from the city's rules."], "C",
  "Inference from the surrounding sentences",
  "The passage says such structures 'are never cleaned or maintained afterwards' and that a pit clogged with silt "
  "'does little more than collect mosquitoes'. So they are neglected and become ineffective.",
  ["Read the sentence and the one after it in paragraph 3",
   "Never cleaned or maintained + clogged pit collects mosquitoes = neglect leads to failure",
   "Option C captures this"],
  "A has no support. B is the opposite: resident associations appear in paragraph 4 as the remedy. D contradicts "
  "the passage, since the certificate is obtained precisely to satisfy the rules.", 60, P2, 3)

Q(RC, "Tone and title", "Basic",
  "Which of the following is the most suitable title for the passage?",
  ["Why Cities Flood Every Monsoon",
   "Harvesting the Rain: Why Rules Need Public Participation",
   "The Engineering of Recharge Pits",
   "Water Tankers and Urban Supply"], "B",
  "A title must cover the whole passage, not one detail",
  "The passage introduces the problem, explains rainwater harvesting, shows that compulsory rules have been poorly "
  "enforced and concludes that public involvement matters as much as regulation. Option B covers all of this.",
  ["Para 1: the problem; para 2: the solution; para 3: weak enforcement; para 4: people must take part",
   "The title must mention harvesting and the role of the public", "Only B does both"],
  "A covers only the first paragraph. C focuses on one technical detail. D picks up a passing reference to tankers.",
  60, P2, 4)

# ---------------------------------------------------------------- RC 3 (Intermediate, 6)
P3 = stim("The weakest link in digital payments", (
    "Over the past decade, the technology behind digital payments has become remarkably secure. Transactions are "
    "encrypted, devices are bound to specific phone numbers, and a payment cannot usually be completed without a PIN "
    "or a one-time password known only to the customer. Ironically, it is this very strength that has shifted the "
    "attention of fraudsters away from the system and towards its users. Rather than break the code, they persuade "
    "the customer to open the door.\n\n"
    "The methods are varied but follow a common script. A caller claims to be from the bank's 'security team' and "
    "warns that the customer's account will be frozen unless a document is updated immediately. A message offers a "
    "refund for a failed delivery, and a link leads to a page that looks exactly like the customer's banking app. In "
    "each case, the victim is rushed, frightened or flattered into sharing a code or approving a request that moves "
    "money out of the account. Because the customer has technically authorised the payment, recovering the money is "
    "often difficult.\n\n"
    "Banks have responded with warnings printed on statements, pop-up alerts in apps and cooling-off periods for new "
    "payees. Some have begun to use software that flags unusual behaviour, such as a large transfer to a new "
    "beneficiary minutes after a long phone call. These measures help, but they cannot entirely replace the judgement "
    "of the customer. A warning that appears on every screen soon becomes invisible.\n\n"
    "The more durable defence may be cultural rather than technical. Just as people learned over generations not to "
    "hand over their house keys to a stranger at the door, they will need to learn that no genuine bank official "
    "will ever ask for a PIN. Until that instinct becomes second nature, the security of the system will be only as "
    "strong as the caution of its least careful user."))

Q(RC, "Factual", "Intermediate",
  "According to the passage, why have fraudsters shifted their attention from the payment system to its users?",
  ["The technology has become so secure that deceiving users is easier than breaking it.",
   "Users are legally responsible for every failed transaction.",
   "Banks have stopped using one-time passwords.",
   "Encryption prevents users from reporting fraud."], "A",
  "Cause and effect stated in the passage",
  "Paragraph 1 says it is 'this very strength' of the technology that shifted fraudsters' attention to users: "
  "'Rather than break the code, they persuade the customer to open the door.'",
  ["Locate 'Ironically, it is this very strength...' in paragraph 1",
   "'This very strength' = the security of the technology",
   "So fraudsters find it easier to deceive users than to break the system: option A"],
  "B: legal responsibility for failed transactions is not discussed. C contradicts the passage, which says payments "
  "usually need a PIN or OTP. D: encryption is mentioned only as a security feature.", 70, P3, 1)

Q(RC, "Factual", "Intermediate",
  "According to the passage, why is it often difficult to recover money lost in such frauds?",
  ["The fraudsters usually operate from other countries.",
   "The customer has technically authorised the payment.",
   "Banks do not keep records of such transactions.",
   "The money is always withdrawn as cash immediately."], "B",
  "Locating a stated reason",
  "The last sentence of paragraph 2 says: 'Because the customer has technically authorised the payment, recovering "
  "the money is often difficult.'",
  ["Find the word 'recovering' in paragraph 2", "The reason given is that the customer technically authorised it",
   "Option B matches"],
  "A, C and D introduce reasons the passage never mentions.", 65, P3, 2)

Q(RC, "Inference", "Intermediate",
  "What does the author mean by the statement 'A warning that appears on every screen soon becomes invisible'?",
  ["Warnings are printed in a font too small to read.",
   "Banks withdraw warnings after a short period.",
   "Fraudsters hide warnings using malicious software.",
   "Users stop noticing warnings that are repeated too often."], "D",
  "Interpreting a figurative statement",
  "The warning does not literally disappear; seeing it everywhere makes users stop paying attention to it. That is "
  "why, the author says, banks' measures cannot replace the customer's own judgement.",
  ["The sentence is figurative: 'invisible' means 'unnoticed'",
   "'On every screen' points to over-repetition",
   "Repetition leads to users ignoring it: option D"],
  "A, B and C read 'invisible' literally and add details (font size, withdrawal of warnings, malware) that the "
  "passage does not mention.", 70, P3, 3)

Q(RC, "Inference", "Intermediate",
  "Which of the following can be inferred from the passage?",
  ["Software that flags unusual behaviour has eliminated payment fraud.",
   "Most digital payments today can be made without a PIN.",
   "The author believes customer awareness is at least as important as technical safeguards.",
   "Banks have been unwilling to warn customers about fraud."], "C",
  "Inference consistent with the whole passage",
  "The author says banks' measures 'help, but they cannot entirely replace the judgement of the customer', and "
  "calls the cultural defence 'more durable'. So the author values customer awareness at least as much as technical "
  "safeguards.",
  ["Paragraph 3: technical measures help but cannot replace judgement",
   "Paragraph 4: the more durable defence is cultural",
   "Option C follows; check that the others contradict the passage"],
  "A: the passage says such measures 'help', not that they eliminate fraud. B contradicts paragraph 1. D "
  "contradicts paragraph 3, which lists the warnings banks give.", 75, P3, 4)

Q(RC, "Vocabulary in context", "Intermediate",
  "Which of the following is most nearly OPPOSITE in meaning to the word 'durable' as used in the passage?",
  ["permanent", "robust", "short-lived", "enduring"], "C",
  "Vocabulary in context: 'durable' means long-lasting",
  "'The more durable defence' is a defence that lasts longer. The opposite is 'short-lived'.",
  ["Meaning of 'durable' in the sentence: lasting, able to hold over time",
   "Look for the option that means 'not lasting'", "'Short-lived' is the opposite"],
  "'Permanent', 'robust' and 'enduring' are all close in meaning to 'durable', not opposite.", 45, P3, 5)

Q(RC, "Tone and title", "Intermediate",
  "The tone of the passage is best described as",
  ["alarmist and accusatory", "analytical and cautionary", "indifferent and casual", "celebratory and optimistic"],
  "B",
  "Identifying tone from word choice and structure",
  "The author explains why fraud has shifted to users, examines the banks' responses and warns readers that "
  "security depends on the caution of users. That is analytical and cautionary.",
  ["The passage explains causes and evaluates measures: analytical",
   "It ends with a warning about the 'least careful user': cautionary",
   "No blame, panic, indifference or celebration"],
  "A: the author blames neither banks nor customers and does not exaggerate. C: the author is clearly concerned. "
  "D: the passage praises the technology only to explain the shift of fraud to users.", 60, P3, 6)

# ---------------------------------------------------------------- RC 4 (Intermediate, 6)
P4 = stim("Work without a workplace", (
    "A delivery rider in a large Indian city may work for three platforms in a single day, switching apps depending "
    "on which offers the better rate at that hour. He has no manager he has ever met, no fixed hours and no office. "
    "To the platforms, he is not an employee but a 'partner', an independent contractor who chooses when and how much "
    "to work. To many economists, he represents one of the fastest-growing segments of the urban labour force.\n\n"
    "The flexibility of gig work is real, and many workers value it. Students fit deliveries around classes; "
    "homemakers drive cabs during school hours; people between jobs earn an income while they search. For workers "
    "with few formal qualifications, platforms have lowered the barriers to entry that once kept them out of steady "
    "earnings.\n\n"
    "But flexibility has a cost that is easy to overlook in good times. A gig worker who falls ill earns nothing until "
    "he recovers. He has no provident fund, no gratuity and, in most cases, no health insurance beyond what he buys "
    "himself. Because his income is spread across several platforms, none of them considers itself responsible for "
    "his welfare. An accident on the road can wipe out months of savings.\n\n"
    "Recent labour codes have, for the first time, recognised gig and platform workers as a distinct category and "
    "provided for social security schemes funded partly by contributions from aggregators. The idea is sound, but its "
    "success will depend on details that are still being worked out: how contributions are calculated when a worker "
    "serves several platforms, how benefits travel with him when he switches apps, and how a worker with no employer "
    "proves his eligibility. A safety net, after all, is useful only if those who fall can actually land in it."))

Q(RC, "Factual", "Intermediate",
  "Which of the following is NOT cited in the passage as an example of how people use the flexibility of gig work?",
  ["Students fitting deliveries around their classes", "Homemakers driving cabs during school hours",
   "People earning an income while they look for a job", "Retired employees supplementing their pensions"], "D",
  "Factual (NOT) question",
  "Paragraph 2 gives three examples: students, homemakers and people between jobs. Retired employees are not "
  "mentioned.",
  ["Find the examples in paragraph 2", "Match A, B and C to the three examples",
   "Retired employees do not appear: option D"],
  "A, B and C are the three examples listed in paragraph 2, so they cannot be the answer.", 65, P4, 1)

Q(RC, "Inference", "Intermediate",
  "Why, according to the passage, does no single platform consider itself responsible for a gig worker's welfare?",
  ["The worker's income is spread across several platforms.",
   "Platforms are not registered in India.",
   "Gig workers refuse to sign contracts with platforms.",
   "The law forbids platforms from offering insurance."], "A",
  "Cause stated in the passage",
  "Paragraph 3 says: 'Because his income is spread across several platforms, none of them considers itself "
  "responsible for his welfare.'",
  ["Locate 'responsible for his welfare' in paragraph 3", "The reason is the spread of income across platforms",
   "Option A"],
  "B, C and D introduce facts the passage never states; D also contradicts paragraph 4, where aggregators are asked "
  "to contribute to social security.", 65, P4, 2)

Q(RC, "Inference", "Intermediate",
  "The phrase 'a cost that is easy to overlook in good times' suggests that",
  ["gig work becomes more expensive for customers during festivals",
   "the lack of protection becomes apparent only when the worker falls ill or meets with an accident",
   "platforms raise their commissions when demand is high",
   "workers save too much money when their income is high"], "B",
  "Inference from the sentences that follow a claim",
  "The sentences after the phrase describe illness, no provident fund or insurance, and accidents wiping out "
  "savings. The 'cost' of flexibility is the absence of protection, which shows only when something goes wrong.",
  ["'Good times' = when the worker is healthy and earning",
   "The examples that follow are illness and accidents",
   "So the cost is hidden until misfortune strikes: option B"],
  "A and C talk about prices and commissions, which the passage does not discuss. D reverses the point: the "
  "passage says an accident can wipe out savings.", 70, P4, 3)

Q(RC, "Factual", "Intermediate",
  "According to the passage, which of the following aspects of the new social security provisions is still being "
  "worked out?",
  ["Whether gig workers should be recognised as a separate category",
   "Whether aggregators should contribute at all",
   "How contributions are to be calculated for a worker who serves several platforms",
   "Whether students should be allowed to take up gig work"], "C",
  "Locating a detail in a list",
  "The last paragraph lists three unresolved details: calculating contributions for a worker serving several "
  "platforms, carrying benefits across apps and proving eligibility without an employer.",
  ["Find 'details that are still being worked out' in paragraph 4",
   "The first detail listed is how contributions are calculated across platforms", "Option C"],
  "A and B are already settled: the codes have recognised gig workers and provided for aggregator contributions. "
  "D is not discussed.", 70, P4, 4)

Q(RC, "Vocabulary in context", "Intermediate",
  "Which of the following is most similar in meaning to the word 'distinct' as used in the passage ('as a distinct "
  "category')?",
  ["vague", "famous", "temporary", "separate"], "D",
  "Vocabulary in context",
  "The labour codes recognised gig workers as a category of their own, different from employees. 'Distinct' here "
  "means separate.",
  ["Context: gig workers were recognised 'for the first time' as their own category",
   "So 'distinct' = separate, different from others", "Option D"],
  "'Vague' is nearly the opposite of 'distinct'. 'Famous' and 'temporary' do not fit the meaning of a legal "
  "category.", 45, P4, 5)

Q(RC, "Tone and title", "Intermediate",
  "Which of the following best expresses the central idea of the passage?",
  ["Gig work offers real flexibility, but workers need a social safety net that actually works for them.",
   "Gig work should be banned because it offers no security.",
   "Platforms are the main cause of unemployment in cities.",
   "Recent labour codes have fully solved the problems of gig workers."], "A",
  "Central idea: balance all paragraphs",
  "The passage grants that flexibility is real and valued, describes the missing protections and welcomes the new "
  "codes while warning that the details must work. Option A captures this balance.",
  ["Para 2: flexibility is valuable; para 3: protections are missing",
   "Para 4: new codes are sound, but details decide success", "So A"],
  "B is too extreme; the author values flexibility. C is never claimed. D contradicts paragraph 4, which says the "
  "details are still being worked out.", 70, P4, 6)

# ---------------------------------------------------------------- RC 5 (Advanced, 5)
P5 = stim("The colour of money", (
    "Few labels have spread through financial markets as quickly as 'green'. Bonds that fund solar parks, loans "
    "linked to emission targets and funds that screen out polluting companies have multiplied, and banks now compete "
    "to announce ever larger commitments to sustainable finance. For a planet that needs vast sums to decarbonise, "
    "the enthusiasm is welcome. The difficulty is that enthusiasm is cheaper than accountability.\n\n"
    "A label is only as meaningful as the standard behind it, and for years the standards were largely written by "
    "those who used them. A company could issue a 'sustainability-linked' bond whose targets it was already on course "
    "to meet, or a fund could call itself green while holding the shares of firms whose principal business was "
    "extracting coal, provided those firms had published a transition plan. None of this was necessarily dishonest; "
    "much of it was simply vague. But vagueness has a way of favouring the issuer over the investor, and a market in "
    "which every product can claim virtue soon becomes one in which none can be trusted.\n\n"
    "Regulators have begun to respond with taxonomies that define which activities qualify as sustainable and "
    "disclosure rules that require firms to back their claims with data. Critics complain that these rules add "
    "paperwork, and that a rigid definition may exclude genuinely useful projects that do not fit neatly into any "
    "category. The objection is not frivolous. A cement plant that halves its emissions does more for the climate "
    "than a solar firm that merely exists, yet only the latter may qualify for the label.\n\n"
    "The answer is unlikely to lie in abandoning standards, but in making them measure change rather than identity. "
    "Investors should ask not whether a firm looks green today but whether it is becoming less brown, and at what "
    "pace. Money, after all, has no colour; it is what money does that the label ought to describe."))

Q(RC, "Inference", "Advanced",
  "The statement 'enthusiasm is cheaper than accountability' most nearly implies that",
  ["green projects cost less to build than conventional projects",
   "it is easier to announce sustainable commitments than to be held answerable for meeting them",
   "investors are unwilling to pay for independent audits",
   "regulators charge high fees for green certification"], "B",
  "Interpreting a figurative claim in context",
  "The sentence follows the description of banks competing to announce ever larger commitments. 'Cheaper' is "
  "figurative: announcing is easy, while being held to account for results is costly and demanding. The next "
  "paragraph develops exactly this gap between labels and standards.",
  ["Context: banks 'compete to announce' commitments", "'Cheaper' = easier, costing less effort",
   "Accountability = being answerable for results", "So announcing is easier than delivering: option B"],
  "A reads 'cheaper' literally as project cost. C and D bring in audits and certification fees, which the passage "
  "never mentions.", 80, P5, 1)

Q(RC, "Inference", "Advanced",
  "Which of the following can be inferred about the early standards for green finance described in the second "
  "paragraph?",
  ["Since they were framed largely by the issuers themselves, they tended to be loose in ways that favoured issuers.",
   "They were mostly drafted by independent climate scientists.",
   "They were deliberately designed to defraud investors.",
   "They excluded all coal-related companies from green funds."], "A",
  "Inference that stays within the author's claims",
  "The standards were 'largely written by those who used them', allowed easy targets and coal holdings, and were "
  "'simply vague'; vagueness 'has a way of favouring the issuer over the investor'. Option A combines these points.",
  ["Who wrote the standards? Those who used them (issuers)", "What were they like? Vague, permissive",
   "Whom did vagueness favour? The issuer", "So A; check that C overstates and D contradicts"],
  "B contradicts 'written by those who used them'. C overstates: the author says 'None of this was necessarily "
  "dishonest'. D contradicts the example of a green fund holding coal firms.", 85, P5, 2)

Q(RC, "Inference", "Advanced",
  "The author uses the example of the cement plant and the solar firm mainly to show that",
  ["cement production is more harmful to the climate than solar power",
   "solar firms should not receive green finance at all",
   "regulators favour heavy industry over renewable energy",
   "a definition based on the type of activity may reward identity rather than an actual cut in emissions"], "D",
  "Purpose of an example",
  "The example comes right after the critics' point that rigid definitions can exclude useful projects. A cement "
  "plant halving its emissions helps the climate more, yet only the solar firm 'may qualify for the label'. The "
  "author's conclusion that standards should 'measure change rather than identity' confirms the purpose.",
  ["Locate the example: paragraph 3, after 'The objection is not frivolous'",
   "Contrast: real emission cut (cement) vs merely being a solar firm",
   "Link to paragraph 4: 'measure change rather than identity'", "So D"],
  "A is a factual comparison the example does not aim at. B goes too far; the author does not oppose financing "
  "solar firms. C reverses the point: under current definitions, the solar firm qualifies and the cement plant may "
  "not.", 85, P5, 3)

Q(RC, "Tone and title", "Advanced",
  "The author's attitude towards the critics of the new regulations can best be described as",
  ["dismissive", "hostile", "partly sympathetic", "wholly supportive"], "C",
  "Tone towards a viewpoint: look for concessions and limits",
  "The author concedes 'The objection is not frivolous' and gives an example supporting it, but then says the "
  "answer is not to abandon standards but to redesign them. That is partial agreement: partly sympathetic.",
  ["Concession: 'The objection is not frivolous' plus a supporting example",
   "Limit: 'The answer is unlikely to lie in abandoning standards'",
   "Agreement with reservations = partly sympathetic"],
  "A and B are ruled out by the explicit concession. D overstates: the author does not accept the critics' "
  "complaint about paperwork and keeps the case for standards.", 75, P5, 4)

Q(RC, "Vocabulary in context", "Advanced",
  "The word 'frivolous' as used in the passage ('The objection is not frivolous') is closest in meaning to",
  ["trivial", "serious", "dishonest", "complex"], "A",
  "Vocabulary in context: frivolous = lacking serious purpose or value",
  "'Not frivolous' means the objection deserves to be taken seriously. So 'frivolous' itself means trivial.",
  ["The author supports the objection with an example, so 'not frivolous' = worth taking seriously",
   "Remove the 'not': frivolous = trivial"],
  "'Serious' is the opposite of 'frivolous'; it is the meaning of 'not frivolous'. 'Dishonest' and 'complex' are "
  "unrelated in meaning.", 50, P5, 5)

# ---------------------------------------------------------------- RC 6 (Advanced, 4)
P6 = stim("A dividend that must be earned", (
    "Demographers speak of a 'dividend' when a country's working-age population grows faster than the number of "
    "children and elderly people who depend on it. With more earners for every dependant, savings rise, investment "
    "becomes easier to finance and growth can accelerate. Several East Asian economies rode such a wave in the late "
    "twentieth century, and India, with a median age still below thirty, is often said to be riding one now.\n\n"
    "The metaphor, however, is misleading in one important respect. A dividend is something a shareholder receives "
    "simply for owning a share; it requires no further effort. The demographic dividend is nothing of the kind. A "
    "large cohort of young people becomes an asset only if they are healthy, educated and absorbed into productive "
    "work. If they are not, the same cohort becomes a burden: a generation of under-employed adults who save little, "
    "pay little tax and grow old without the savings to support themselves.\n\n"
    "The East Asian economies that benefited did not merely possess young populations; they invested heavily in "
    "schooling, moved workers out of low-productivity farming into manufacturing, and drew women into the paid "
    "workforce in large numbers. The last point is often neglected. A country in which a large share of working-age "
    "women do not participate in paid work is, in effect, collecting only part of its dividend, however favourable "
    "its age structure may appear.\n\n"
    "The window does not stay open indefinitely. As fertility falls, the working-age share eventually peaks and "
    "begins to decline, and the country must then support a growing elderly population. A nation that has not grown "
    "rich by then may find that it has grown old first. The question for policymakers, therefore, is not whether the "
    "dividend exists but whether the conditions to collect it are being created quickly enough."))

Q(RC, "Inference", "Advanced",
  "According to the author, the term 'dividend' is misleading because",
  ["India's working-age population has already begun to shrink",
   "dividends are usually paid only to elderly shareholders",
   "unlike a financial dividend, the demographic benefit does not come automatically but depends on deliberate "
   "investment",
   "East Asian economies gained nothing from their young populations"], "C",
  "Understanding an argument about a metaphor",
  "A shareholder's dividend 'requires no further effort', but a young population becomes an asset 'only if they "
  "are healthy, educated and absorbed into productive work'. The benefit has to be earned through investment.",
  ["Paragraph 2 explains the misleading respect",
   "Financial dividend: no effort needed; demographic dividend: needs health, education and jobs", "So C"],
  "A contradicts paragraph 1 (India is said to be riding the wave now). B is a distortion of what a dividend is. D "
  "contradicts paragraph 3, which says the East Asian economies benefited.", 80, P6, 1)

Q(RC, "Inference", "Advanced",
  "Which of the following statements would the author most likely agree with?",
  ["A young population by itself guarantees rapid economic growth.",
   "Countries should try to raise fertility so that the demographic window stays open.",
   "Investment in schooling matters less than the size of the working-age population.",
   "Low participation of women in paid work reduces the benefit a country can draw from a favourable age "
   "structure."], "D",
  "Agree/disagree inference",
  "Paragraph 3 says a country where many working-age women do not do paid work is 'collecting only part of its "
  "dividend, however favourable its age structure may appear'. That is option D.",
  ["Test each option against the passage",
   "A contradicts the central claim that the dividend must be earned",
   "B: the author never proposes raising fertility",
   "C reverses paragraph 3, which stresses schooling", "D restates paragraph 3"],
  "A, B and C are each contradicted by, or absent from, the passage, as shown in the steps.", 85, P6, 2)

Q(RC, "Inference", "Advanced",
  "The phrase 'may find that it has grown old first' suggests that",
  ["the country's elderly population may become large before the country is prosperous enough to support it",
   "the country will age faster than every other country in the world",
   "older citizens will be forced to keep working after retirement",
   "the demographic window will reopen once the population ages"], "A",
  "Interpreting a phrase from its sentence",
  "The full sentence is 'A nation that has not grown rich by then may find that it has grown old first'. 'First' "
  "means before growing rich: ageing arrives before prosperity.",
  ["Read the whole sentence: 'not grown rich by then ... grown old first'",
   "'First' = before becoming rich", "So the elderly burden arrives before the wealth to bear it: option A"],
  "B makes an unsupported comparison with all countries. C is not mentioned. D contradicts 'The window does not "
  "stay open indefinitely'.", 75, P6, 3)

Q(RC, "Tone and title", "Advanced",
  "Which of the following titles best captures the main argument of the passage?",
  ["India's Ageing Crisis",
   "The Demographic Dividend: An Opportunity, Not an Entitlement",
   "How East Asia Industrialised",
   "Falling Fertility and Its Causes"], "B",
  "Title = main argument, not a supporting detail",
  "The author's main argument is that a young population is a benefit only if a country creates the conditions to "
  "collect it, and must do so before the window closes. 'An Opportunity, Not an Entitlement' expresses that.",
  ["Main claim (para 2): the dividend must be earned",
   "Support (para 3): East Asia earned it; women's participation matters",
   "Urgency (para 4): the window closes", "Option B captures the argument"],
  "A: the passage says India is young now; ageing is a future risk. C is one supporting example. D: the causes of "
  "falling fertility are not discussed.", 70, P6, 4)

# =====================================================================================================================
# CLOZE TEST
# =====================================================================================================================
CLOZE_STEM = "In the passage, a word is missing at the blank numbered ({n}). Choose the word that best fits the blank."
ERR_STEM = ("In the passage, the word in bold numbered ({n}) may be wrongly used. Choose the word that should replace "
            "it to make the sentence grammatically correct and meaningful. If the word is correct as it stands, "
            "choose 'No replacement required'.")

# ---------------------------------------------------------------- Cloze 1 (Basic, 6)
C1 = stim("Learning to save early", (
    "Financial habits, like most habits, are formed early. A child who receives a small allowance and is encouraged "
    "to keep part of it aside learns a lesson that no textbook can (1) ______: that money spent today is money that "
    "cannot be spent tomorrow. Unfortunately, many young adults enter their first job without ever having (2) ______ "
    "a budget, and the arrival of a regular salary, together with easy access to credit cards and instant loans, can "
    "quickly lead to debt.\n\n"
    "Schools and banks can play a useful role here. Several banks now run programmes in which students open a savings "
    "account, (3) ______ small amounts every month and track how interest makes their balance grow. Such exercises "
    "turn an abstract idea into something the student can see and measure. Teachers report that students who take "
    "part are more (4) ______ about comparing prices and less likely to buy things on impulse.\n\n"
    "Parents, too, have a part to play. Children learn more from what they see than from what they are told, and a "
    "household in which expenses are discussed openly gives them a realistic picture of how money is earned and used. "
    "Talking about money need not be (5) ______; it can be as ordinary as discussing the weather.\n\n"
    "The aim is not to make children anxious about money but to make them confident with it. A young person who "
    "understands saving, borrowing and interest is far better (6) ______ to make the large financial decisions that "
    "adult life brings."))

Q(CL, "Single-blank cloze", "Basic", CLOZE_STEM.format(n=1), ["teach", "learn", "forget", "borrow"], "A",
  "Cloze: meaning of the sentence decides the word",
  "The child 'learns a lesson that no textbook can teach': a textbook is something that teaches, so 'teach' "
  "completes the idea that this lesson is learned from experience.",
  ["Subject of the blank: 'no textbook'", "What does a textbook do with a lesson? It teaches it",
   "'no textbook can teach' fits"],
  "A textbook cannot 'learn', 'forget' or 'borrow' a lesson; these verbs do not suit a book as subject.", 40, C1, 1)

Q(CL, "Single-blank cloze", "Basic", CLOZE_STEM.format(n=2), ["earned", "prepared", "borrowed", "refused"], "B",
  "Cloze: collocation ('prepare a budget')",
  "Young adults start work 'without ever having prepared a budget', which explains why a salary and easy credit lead "
  "them into debt. 'Prepare a budget' is the standard collocation.",
  ["The sentence explains why young earners fall into debt", "They lack practice in planning money",
   "'prepared a budget' expresses this"],
  "One does not 'earn', 'borrow' or 'refuse' a budget in this sense; none of these explains the slide into debt.",
  40, C1, 2)

Q(CL, "Single-blank cloze", "Basic", CLOZE_STEM.format(n=3), ["withdraw", "waste", "deposit", "lend"], "C",
  "Cloze: logical sequence of actions",
  "Students open an account, deposit small amounts every month and watch interest make the balance grow. Only "
  "regular deposits make the balance grow.",
  ["Result in the sentence: the balance grows", "Monthly action that makes a balance grow: depositing",
   "'deposit' fits"],
  "'Withdraw' and 'waste' would shrink the balance. Students do not 'lend' amounts into their own savings "
  "account.", 40, C1, 3)

Q(CL, "Single-blank cloze", "Basic", CLOZE_STEM.format(n=4), ["careless", "famous", "angry", "careful"], "D",
  "Cloze: positive outcome signalled by the context",
  "The sentence reports a good result: students become more careful about comparing prices and less likely to buy "
  "on impulse. 'Careful' matches 'less likely to buy things on impulse'.",
  ["The second half of the sentence is positive: less impulse buying",
   "The first half must also be positive", "'more careful about comparing prices'"],
  "'Careless' contradicts the positive result. 'Famous' and 'angry' make no sense with 'about comparing prices'.",
  40, C1, 4)

Q(CL, "Single-blank cloze", "Basic", CLOZE_STEM.format(n=5), ["awkward", "routine", "common", "casual"], "A",
  "Cloze: contrast marked by 'need not be ... ; it can be as ordinary as...'",
  "The sentence contrasts what talking about money is feared to be with what it can be: ordinary. The contrasting "
  "word is 'awkward'.",
  ["Structure: 'need not be X; it can be as ordinary as...'", "X must be the opposite of ordinary and easy",
   "'awkward' fits"],
  "'Routine', 'common' and 'casual' all mean much the same as 'ordinary', so they destroy the contrast.", 40, C1, 5)

Q(CL, "Single-blank cloze", "Basic", CLOZE_STEM.format(n=6), ["equip", "equipped", "equipping", "equipment"], "B",
  "Cloze: grammar ('be + better + past participle + to')",
  "'Is far better equipped to make decisions' uses the past participle 'equipped' after 'is ... better'. It means "
  "better prepared.",
  ["Pattern: 'is (far) better ___ to make'", "A past participle used as an adjective is needed: equipped",
   "'is far better equipped to make' is correct"],
  "'Equip' (base form) and 'equipping' (present participle) do not fit after 'is better'. 'Equipment' is a noun.",
  35, C1, 6)

# ---------------------------------------------------------------- Cloze 2 (Intermediate, 4)
C2 = stim("The second life of batteries", (
    "As electric vehicles move from novelty to the mainstream, a question that once seemed distant is becoming "
    "urgent: what happens to their batteries when they wear out? A typical vehicle battery is considered unfit for "
    "driving once its capacity falls to about seventy or eighty per cent of the original, but that does not mean it "
    "is (1) ______. Such a battery can still store a great deal of energy, and a growing number of firms are giving "
    "it a second life as stationary storage for solar panels, telecom towers and small shops.\n\n"
    "When even this second life ends, the battery must be recycled. Lithium, cobalt and nickel are expensive to mine "
    "and are concentrated in a handful of countries, so recovering them from old cells reduces both costs and (2) "
    "______ on imports. Recycling, however, is technically demanding. Batteries differ widely in design, and "
    "dismantling them safely requires skilled labour and careful handling of materials that can catch fire.\n\n"
    "At present, a large share of used batteries in many developing countries passes through informal dealers who "
    "extract the most valuable parts and (3) ______ the rest, often in ways that pollute soil and water. Bringing "
    "these dealers into the formal system, rather than simply banning them, may be the most practical way forward.\n\n"
    "Policy can help by making manufacturers responsible for collecting the batteries they sell and by setting "
    "minimum recovery targets. If the rules are clear and enforced, the battery that leaves a car may become not a "
    "waste problem but a (4) ______ of raw material for the next generation of vehicles."))

Q(CL, "Single-blank cloze", "Intermediate", CLOZE_STEM.format(n=1), ["valuable", "charged", "useless", "expensive"],
  "C",
  "Cloze: contrast with 'but' and the sentence that follows",
  "The battery is unfit for driving, 'but that does not mean it is useless': the next sentence says it can still "
  "store a great deal of energy and be given a second life.",
  ["'but that does not mean it is ___' denies a negative conclusion",
   "The next sentence shows the battery still has a use", "So the denied word is 'useless'"],
  "'Valuable' would make the sentence say the battery is not valuable, contradicting the next sentence. 'Charged' "
  "and 'expensive' do not follow from being unfit for driving.", 45, C2, 1)

Q(CL, "Single-blank cloze", "Intermediate", CLOZE_STEM.format(n=2),
  ["emphasis", "insistence", "interest", "dependence"], "D",
  "Cloze: collocation ('dependence on imports')",
  "The metals are concentrated in a handful of countries, so recovering them reduces costs and the country's "
  "dependence on imports. 'Dependence on' is the fixed collocation.",
  ["Context: metals come from a few countries, i.e. through imports",
   "Recycling reduces the need to import", "'dependence on imports' fits in meaning and preposition"],
  "'Emphasis on imports', 'insistence on imports' and 'interest on imports' make no sense here: recycling metals "
  "does not reduce any of them.", 45, C2, 2)

Q(CL, "Single-blank cloze", "Intermediate", CLOZE_STEM.format(n=3), ["preserve", "dump", "polish", "insure"], "B",
  "Cloze: action that explains the pollution that follows",
  "Informal dealers take the valuable parts and dump the rest, 'often in ways that pollute soil and water'. Only "
  "dumping explains the pollution.",
  ["The phrase after the blank: 'in ways that pollute soil and water'",
   "What would dealers do with parts they do not want? Throw them away", "'dump' fits"],
  "'Preserve', 'polish' and 'insure' are careful handling, which cannot pollute soil and water.", 45, C2, 3)

Q(CL, "Single-blank cloze", "Intermediate", CLOZE_STEM.format(n=4), ["source", "shortage", "burden", "lack"], "A",
  "Cloze: contrast 'not a waste problem but a ___'",
  "The sentence contrasts a waste problem with something positive: a source of raw material for new vehicles.",
  ["Structure: 'not X but Y' where X is negative", "Y must be positive and fit 'of raw material'",
   "'a source of raw material' fits"],
  "'Shortage' and 'lack' of raw material would be problems, not the positive opposite. 'Burden' repeats the idea "
  "of a problem.", 45, C2, 4)

# ---------------------------------------------------------------- Cloze 3 (Intermediate 3 + Advanced 1)
C3 = stim("When credit becomes a trap", (
    "Microfinance began with a simple and powerful insight: poor households, especially women, are reliable borrowers "
    "when loans are small, repayments are frequent and borrowers in a group (1) ______ for one another. For two "
    "decades, the model brought formal credit to millions who had previously depended on moneylenders charging "
    "ruinous rates.\n\n"
    "Success, however, brought its own risks. As lenders multiplied and competed for the same customers, some "
    "borrowers took loans from several institutions at once, using one loan to repay another. Because no single "
    "lender could see the full picture, a household's total debt could grow well beyond what its income could (2) "
    "______. When a crop failed or a family member fell ill, repayments stopped, and the stress spread quickly "
    "through entire villages. Some families sold their livestock, and others went back to the very moneylenders "
    "that microfinance had been meant to replace.\n\n"
    "The lesson was not that small loans are harmful but that lending without information is. Credit bureaus now "
    "record microfinance loans, and regulators have introduced limits linking a household's total repayment "
    "obligations to its income. These rules aim to (3) ______ the kind of over-lending that had turned a tool of "
    "empowerment into a source of distress.\n\n"
    "Yet rules can only do so much. Responsible lending also depends on loan officers who are judged by the quality "
    "of the loans they make, not merely by how many they disburse. An institution that rewards its staff only for "
    "volume will always find ways around a ceiling. In finance, as elsewhere, incentives tend to (4) ______ "
    "intentions."))

Q(CL, "Single-blank cloze", "Intermediate", CLOZE_STEM.format(n=1), ["argue", "vouch", "compete", "apologise"], "B",
  "Cloze: group lending and the phrasal verb 'vouch for'",
  "In group lending, members guarantee each other's repayment. 'Vouch for' means to guarantee or answer for "
  "someone, which explains why such borrowers are reliable.",
  ["The sentence lists conditions that make borrowers reliable",
   "Group members standing guarantee for each other is one such condition", "'vouch for one another' fits"],
  "'Argue for' and 'compete for' one another do not make borrowers more reliable. 'Apologise for one another' is "
  "illogical here.", 45, C3, 1)

Q(CL, "Single-blank cloze", "Intermediate", CLOZE_STEM.format(n=2), ["earn", "waste", "support", "spend"], "C",
  "Cloze: what income does to debt ('support' = sustain, service)",
  "Total debt grew 'well beyond what its income could support', i.e. beyond the level the household's income could "
  "service. The next sentence (repayments stopped) confirms the overload.",
  ["The subject is 'its income'; the object is the debt",
   "Income either can or cannot sustain a level of debt", "'support' fits"],
  "Income does not 'earn', 'waste' or 'spend' debt; with 'income' as subject these verbs make no sense.",
  45, C3, 2)

Q(CL, "Single-blank cloze", "Intermediate", CLOZE_STEM.format(n=3), ["encourage", "reward", "ignore", "curb"], "D",
  "Cloze: purpose of a regulation",
  "Credit bureaus and repayment limits are meant to restrain over-lending, which had caused distress. 'Curb' means "
  "to restrain or control.",
  ["The rules respond to over-lending that caused distress", "Their aim must be to restrain it",
   "'curb' fits"],
  "'Encourage' and 'reward' over-lending contradict the purpose of the rules. 'Ignore' makes the rules pointless.",
  40, C3, 3)

Q(CL, "Single-blank cloze", "Advanced", CLOZE_STEM.format(n=4), ["override", "follow", "reflect", "obey"], "A",
  "Cloze: concluding generalisation drawn from the paragraph",
  "The paragraph says an institution that rewards volume 'will always find ways around a ceiling', whatever the "
  "rules intend. The generalisation is that incentives override intentions: what people are rewarded for wins over "
  "what they mean to do.",
  ["Paragraph point: good rules are defeated by bad incentives",
   "The last sentence generalises: incentives beat intentions", "'override' expresses this"],
  "'Follow', 'obey' and 'reflect' make incentives subordinate to, or consistent with, intentions, which reverses "
  "the paragraph's point.", 50, C3, 4)

# ---------------------------------------------------------------- Cloze 4 (Advanced, 5; error-based)
C4 = stim("Cities that cool themselves", (
    "On a summer afternoon, the centre of a large city can be several degrees hotter than the farmland around it. "
    "This 'urban heat island' is no mystery. Concrete and asphalt absorb sunlight during the day and release it "
    "slowly at night, while the trees and open soil that would otherwise **(1) aggravate** the heat have been paved "
    "over. Air conditioners, which pump hot air out of buildings and into the streets, make the problem **(2) "
    "better**.\n\n"
    "The consequences are not merely uncomfortable. Prolonged heat raises the risk of illness among the elderly and "
    "outdoor workers, **(3) elevates** labour productivity and pushes up demand for electricity at the very hours when "
    "grids are most strained. In a warming climate, heat is fast becoming one of the most serious, if least **(4) "
    "visible**, threats to urban life.\n\n"
    "Fortunately, many of the remedies are simple. Roofs painted in reflective white can lower indoor temperatures "
    "noticeably; trees planted along streets provide shade and cool the air through evaporation; and water bodies "
    "that were filled in for construction can be restored. Some cities have drawn up 'heat action plans' that combine "
    "such measures with early warnings and changes in working hours during heatwaves.\n\n"
    "What these plans require is not exotic technology but **(5) occasional** attention. A tree planted this year "
    "will cast useful shade only after several years of care, and a white roof must be repainted as it fades. Cooling "
    "a city, in other words, is less a single project than a habit of maintenance."))

NR = "No replacement required"
Q(CL, "Error-based cloze", "Advanced", ERR_STEM.format(n=1), ["moderate", "intensify", "trap", NR], "A",
  "Error-based cloze: the bold word must fit the logic of the sentence",
  "The sentence says heat builds up because the trees and soil that would otherwise reduce it have been paved over. "
  "'Aggravate' (make worse) reverses this; 'moderate' (make less extreme) is correct.",
  ["Logic: paving over trees and soil makes the city hotter",
   "So trees and soil must have reduced the heat", "'aggravate' is wrong; replace with 'moderate'"],
  "'Intensify' and 'trap' repeat the error of 'aggravate': they make trees the cause of heat. The original word is "
  "wrong, so 'No replacement required' does not apply.", 55, C4, 1)

Q(CL, "Error-based cloze", "Advanced", ERR_STEM.format(n=2), ["worst", "well", "worse", NR], "C",
  "Error-based cloze: meaning plus the comparative form after 'make the problem'",
  "Air conditioners pump hot air into the streets, so they make the heat problem worse, not 'better'. After "
  "'make the problem', the comparative adjective 'worse' is required.",
  ["Effect of pumping hot air into streets: more heat", "So the problem becomes worse",
   "Comparative needed: 'worse' (not the superlative 'worst' or the adverb 'well')"],
  "'Worst' is a superlative and needs 'the' and a comparison set. 'Well' is an adverb/adjective that does not fit "
  "the meaning. 'Better' itself is wrong, so 'No replacement required' does not apply.", 50, C4, 2)

Q(CL, "Error-based cloze", "Advanced", ERR_STEM.format(n=3), ["enhances", "reduces", "elevating", NR], "B",
  "Error-based cloze: a list of harmful consequences",
  "The sentence lists the harms of prolonged heat: illness, lower labour productivity and higher electricity "
  "demand. Heat 'reduces' productivity; 'elevates' wrongly makes it a benefit.",
  ["The sentence opens 'The consequences are not merely uncomfortable': it lists harms",
   "Heat lowers the output of workers", "Replace 'elevates' with 'reduces' (same tense and number as 'raises' and "
   "'pushes')"],
  "'Enhances' has the same wrong meaning as 'elevates'. 'Elevating' is both wrong in meaning and breaks the "
  "parallel verbs 'raises ... pushes'.", 55, C4, 3)

Q(CL, "Error-based cloze", "Advanced", ERR_STEM.format(n=4), ["invisible", "visibly", "visibility", NR], "D",
  "Error-based cloze: 'if least ...' concession is correct as written",
  "'One of the most serious, if least visible, threats' means serious though not easily seen. Heat is invisible "
  "compared with floods or fires, so 'visible' is correct as written.",
  ["'If' here means 'though': serious though least visible", "The adjective 'visible' is grammatical after 'least'",
   "The meaning is sound, so no replacement is needed"],
  "'Least invisible' is a confusing double negative that would make heat an obvious threat, which is not the point. "
  "'Visibly' is an adverb and 'visibility' a noun; neither can modify 'threats' here. Since 'visible' is already "
  "correct, no replacement is needed.", 50, C4, 4)

Q(CL, "Error-based cloze", "Advanced", ERR_STEM.format(n=5), ["sustained", "sporadic", "momentary", NR], "A",
  "Error-based cloze: the following sentences decide the word",
  "The next sentences say a tree needs several years of care and a roof must be repainted as it fades: cooling a "
  "city is 'a habit of maintenance'. That calls for 'sustained' attention, not 'occasional' attention.",
  ["Read what follows: years of care, repainting, 'a habit of maintenance'",
   "These describe continuous effort", "Replace 'occasional' with 'sustained'"],
  "'Sporadic' and 'momentary' mean the same kind of irregular or brief attention as 'occasional', so they keep the "
  "error. 'Occasional' is wrong, so 'No replacement required' does not apply.", 55, C4, 5)

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


ed("Part-wise error", "Basic", "Each of the new trainees", "have been assigned", "to a rural branch this year.", "B",
   "'Each of + plural noun' takes a singular verb",
   "'Each' is the subject, and it is singular; 'of the new trainees' only describes it. So the verb must be 'has been "
   "assigned', not 'have been assigned'.",
   ["Find the true subject: 'Each' (not 'trainees')", "'Each' is singular, so the verb must be singular",
    "'have been assigned' → 'has been assigned': error in part B"],
   "Part A is a correct subject phrase and part C is a correct adverbial phrase. Since B has an error, 'No error' is "
   "wrong.", 30)

ed("Part-wise error", "Basic", "He did not knew", "that the branch", "would remain closed on Saturday.", "A",
   "After the auxiliary 'did', the main verb takes the base form",
   "'Did not' must be followed by the base form of the verb: 'did not know', not 'did not knew'.",
   ["Locate the auxiliary 'did' in part A", "Rule: do/does/did + base form",
    "'knew' → 'know': error in part A"],
   "Part B is a correct 'that' clause opener, and 'would remain' in part C correctly follows the past reporting "
   "verb. Part A has an error, so 'No error' is wrong.", 30)

ed("Error-free sentence", "Basic", "The cashier counted the notes", "carefully before",
   "handing them over to the customer.", "D",
   "Checking each part: verb form, adverb placement, gerund after a preposition",
   "The sentence is correct. 'Counted' is a correct past tense, 'carefully' correctly modifies 'counted', and "
   "'before' (a preposition here) is correctly followed by the gerund 'handing'.",
   ["Part A: subject + past tense + object: correct", "Part B: adverb + 'before': correct",
    "Part C: 'before handing them over': preposition + gerund, correct", "No error: option D"],
   "Each of parts A, B and C is grammatically correct, as shown in the steps, so none of them is the answer.", 30)

ed("Part-wise error", "Basic", "She has been working", "in this bank", "since five years.", "C",
   "'Since' takes a point of time; 'for' takes a period of time",
   "'Five years' is a period, so it needs 'for': 'for five years'. 'Since' is used with a point in time, such as "
   "'since 2021'.",
   ["Part C has a time expression: 'five years'", "It is a period, not a starting point",
    "'since five years' → 'for five years': error in part C"],
   "'Has been working' (part A) is the correct present perfect continuous with a duration, and part B is correct. "
   "Part C has an error, so 'No error' is wrong.", 30)

ed("Part-wise error", "Basic", "One of my friend", "has opened a savings account", "in a public sector bank.", "A",
   "'One of' is followed by a plural noun",
   "'One of' picks one member of a group, so the noun after it must be plural: 'one of my friends'.",
   ["Locate 'One of my friend' in part A", "Rule: one of + plural noun (+ singular verb)",
    "'friend' → 'friends': error in part A"],
   "'Has opened' in part B correctly agrees with the singular subject 'One'. Part C is correct. Part A has the error, "
   "so 'No error' is wrong.", 30)

ed("Part-wise error", "Intermediate", "The committee has submitted", "its report, which recommend",
   "stricter norms for digital lenders.", "B",
   "In a relative clause, the verb agrees with the antecedent of 'which'",
   "'Which' refers to 'its report', which is singular. So the verb must be 'recommends', not 'recommend'.",
   ["Identify the antecedent of 'which': 'report' (singular)",
    "The verb in the relative clause must agree with it: 'recommends'", "Error in part B"],
   "Part A is correct: 'committee' acting as one body takes 'has' and 'its'. Part C is correct. Part B has the error, "
   "so 'No error' is wrong.", 35)

ed("Part-wise error", "Intermediate", "No sooner had the auditors", "arrived at the branch",
   "when the manager produced the ledgers.", "C",
   "'No sooner' pairs with 'than', not 'when'",
   "The correlative is 'No sooner ... than'. Part C uses 'when', which belongs with 'hardly' or 'scarcely'. It "
   "should read 'than the manager produced the ledgers'.",
   ["Part A starts with 'No sooner had ...' (correct inversion)",
    "Its partner word must be 'than'", "'when' in part C → 'than': error in part C"],
   "Part A has the correct inversion 'No sooner had the auditors' and part B the correct past participle. Part C "
   "has the error, so 'No error' is wrong.", 40)

ed("Part-wise error", "Intermediate", "The number of customers using", "mobile banking apps have",
   "risen sharply over the last year.", "B",
   "'The number of' takes a singular verb; 'a number of' takes a plural verb",
   "The subject is 'The number', a single quantity, so the verb must be 'has risen', not 'have risen'.",
   ["Head of the subject: 'The number' (singular)",
    "'of customers using mobile banking apps' only describes it",
    "'have' → 'has': error in part B"],
   "Part A is a correct subject phrase. Part C, 'risen sharply', is correct with 'has'. Part B has the error, so 'No "
   "error' is wrong.", 35)

ed("Part-wise error", "Intermediate", "Unless the borrower does not repay", "the overdue amount by Friday,",
   "the bank will initiate recovery proceedings.", "A",
   "'Unless' already means 'if not'; it is not followed by another 'not'",
   "'Unless the borrower does not repay' is a double negative meaning 'if the borrower does not not repay'. It should "
   "be 'Unless the borrower repays' (or 'If the borrower does not repay').",
   ["'Unless' = 'if ... not'", "Adding 'does not' creates a double negative and reverses the meaning",
    "Error in part A"],
   "Part B is correct, and part C correctly uses the future in the main clause of a first conditional. Part A has "
   "the error, so 'No error' is wrong.", 35)

ed("Error-free sentence", "Intermediate", "The new policy, along with its detailed guidelines,",
   "has been published", "on the bank's official website.", "D",
   "'Along with', 'as well as', 'together with' do not change the number of the subject",
   "The subject is 'The new policy' (singular); 'along with its detailed guidelines' is a parenthetical addition. "
   "So the singular 'has been published' is correct, and 'published on the website' is idiomatic. The sentence has "
   "no error.",
   ["Subject: 'The new policy' (singular); ignore 'along with ...'", "'has been published' agrees: correct",
    "'on the bank's official website' is correct", "No error: option D"],
   "A student who counts the guidelines as part of the subject may wrongly pick part B; parts A and C are also "
   "correct, so only 'No error' fits.", 35)

ed("Part-wise error", "Intermediate", "Neither of the two proposals", "submitted by the consultants",
   "were acceptable to the board.", "C",
   "'Neither of + plural noun' takes a singular verb",
   "'Neither' (not one of the two) is the subject and is singular. The verb must be 'was acceptable', not 'were'.",
   ["Subject: 'Neither' (singular)", "'of the two proposals submitted by the consultants' describes it",
    "'were' → 'was': error in part C"],
   "Part A is the correct form 'Neither of the two' and part B is a correct participle phrase. Part C has the "
   "error, so 'No error' is wrong.", 35)

ed("Part-wise error", "Advanced", "Scarcely a week passes", "without some new scheme being announced",
   "for farmers who's crops have failed.", "C",
   "'Whose' (possessive relative) vs 'who's' (who is / who has)",
   "The relative pronoun must show possession: the crops belong to the farmers. 'Who's' means 'who is' or 'who has', "
   "so it should be 'whose crops have failed'.",
   ["Test 'who's' by expanding it: 'who is crops' / 'who has crops' make no sense",
    "Possession is needed: 'whose'", "Error in part C"],
   "Part A ('Scarcely a week passes') and part B ('without ... being announced') are correct idioms. Part C has the "
   "error, so 'No error' is wrong.", 40)

ed("Part-wise error", "Advanced", "The chairman, as well as the directors,", "were present at the meeting",
   "where the merger was finally approved.", "B",
   "With 'as well as', the verb agrees with the first subject",
   "The subject is 'The chairman' (singular); 'as well as the directors' is parenthetical. The verb must be 'was "
   "present', not 'were'.",
   ["First subject: 'The chairman' (singular)", "'as well as the directors' does not make it plural",
    "'were' → 'was': error in part B"],
   "Part A is correctly punctuated with commas around the parenthetical phrase, and part C is correct. Part B has "
   "the error, so 'No error' is wrong.", 40)

ed("Part-wise error", "Advanced", "It is high time the government takes", "concrete steps to curb",
   "the misuse of farm loan waivers.", "A",
   "'It is high time' + subject + past (subjunctive) form",
   "'It is (high) time' is followed by the simple past to show that the action is overdue: 'It is high time the "
   "government took concrete steps'.",
   ["Identify the structure 'It is high time + clause'", "Rule: the verb in the clause takes the past form",
    "'takes' → 'took': error in part A"],
   "Parts B and C ('concrete steps to curb the misuse of ...') are correct. Part A has the error, so 'No error' is "
   "wrong.", 40)

ed("Error-free sentence", "Advanced", "Not only did the bank reduce its lending rate,", "but it also waived",
   "the processing fee for first-time borrowers.", "D",
   "'Not only' at the start needs inversion; it pairs with 'but ... also'",
   "The sentence is correct. 'Not only' at the start correctly triggers inversion ('did the bank reduce'), and the "
   "second clause correctly uses 'but it also waived'. The fee phrase is correct.",
   ["Part A: 'Not only did the bank reduce' = auxiliary + subject + base verb: correct",
    "Part B: 'but it also waived' = correct partner of 'not only'",
    "Part C: correct noun phrase", "No error: option D"],
   "Students often expect 'not only' to need 'but also' together and mark part B, but 'but it also' is standard. "
   "Part A's inversion is required, not an error. Part C is correct.", 40)

ed("Part-wise error", "Advanced", "The reason he was denied the loan", "was because his credit score",
   "had fallen below the bank's cut-off.", "B",
   "'The reason ... is/was that', not 'is/was because' (redundancy)",
   "'Reason' already means cause, so 'the reason ... was because' says the cause twice. The standard form is 'The "
   "reason he was denied the loan was that his credit score had fallen...'.",
   ["Subject 'The reason ...' + 'was' needs a noun clause as complement", "Use 'that', not 'because'",
    "Error in part B"],
   "Part A is correct (the relative 'that/why' may be omitted after 'reason'). Part C correctly uses the past perfect "
   "for the earlier event. Part B has the error, so 'No error' is wrong.", 40)

# =====================================================================================================================
# SENTENCE IMPROVEMENT
# =====================================================================================================================
SI = "Sentence Improvement"
SI_STEM = ("Which of the following phrases should replace the phrase in bold to make the sentence grammatically "
           "correct? If the sentence is correct as it is, choose 'No improvement required'.\n")
NI = "No improvement required"

Q(SI, "Bold-part improvement", "Basic",
  SI_STEM + "The bank **has opened two new branches last month** in the district.",
  ["opened two new branches last month", "had opened two new branches last month",
   "has been opening two new branches last month", NI], "A",
  "Present perfect is not used with a finished past time ('last month')",
  "'Last month' is a definite past time, so the simple past is required: 'The bank opened two new branches last "
  "month'.",
  ["Spot the time marker: 'last month' (finished past)", "Present perfect cannot take a finished past time marker",
   "Use the simple past: 'opened'"],
  "'Had opened' (past perfect) needs another past action to precede. 'Has been opening' is still a present "
  "perfect form and clashes with 'last month'. The original is wrong, so 'No improvement required' does not "
  "apply.", 30)

Q(SI, "Bold-part improvement", "Basic",
  SI_STEM + "He is **senior than** me by three years in the bank.",
  ["seniors to", "senior to", "senior from", NI], "B",
  "Latin comparatives (senior, junior, superior, inferior, prior) take 'to', not 'than'",
  "'Senior' is a Latin comparative and is followed by 'to': 'He is senior to me by three years'.",
  ["Identify 'senior' as a Latin comparative", "Rule: such words take 'to'", "'senior than' → 'senior to'"],
  "'Seniors' is a plural noun and cannot follow 'He is' here. 'Senior from' is not idiomatic. The original 'senior "
  "than' is wrong, so 'No improvement required' does not apply.", 30)

Q(SI, "Bold-part improvement", "Intermediate",
  SI_STEM + "The loan was sanctioned **despite of his poor credit history**.",
  ["in spite his poor credit history", "despite to his poor credit history", "despite his poor credit history", NI],
  "C",
  "'Despite' takes no preposition; 'in spite' needs 'of'",
  "'Despite' is itself a preposition and is followed directly by a noun phrase: 'despite his poor credit history'. "
  "The alternative is 'in spite of'.",
  ["'Despite of' is a mixing of 'despite' and 'in spite of'", "Remove 'of': 'despite his poor credit history'"],
  "'In spite his' drops the necessary 'of'. 'Despite to' adds a wrong preposition. The original is wrong, so 'No "
  "improvement required' does not apply.", 30)

Q(SI, "Bold-part improvement", "Intermediate",
  SI_STEM + "**Having finished the audit, the report was submitted** to the head office on Monday.",
  ["Having finished the audit, the team submitted the report",
   "Having been finished the audit, the report was submitted",
   "Having finished the audit, the report has submitted", NI], "A",
  "Dangling participle: the subject of the main clause must be the doer of the participle",
  "'Having finished the audit' must describe who finished it. In the original, the subject is 'the report', which "
  "cannot finish an audit. Making 'the team' the subject fixes the sentence.",
  ["Ask who finished the audit: a person or team, not the report",
   "The main clause must begin with that doer", "Option A: 'the team submitted the report'"],
  "B keeps 'the report' as the doer and adds an ungrammatical 'Having been finished the audit'. C still has the "
  "report doing the action and wrongly uses an active 'has submitted'. The original dangles, so 'No improvement "
  "required' does not apply.", 40)

Q(SI, "Bold-part improvement", "Intermediate",
  SI_STEM + "I would rather you **do not disclose** your PIN to anyone, even to a family member.",
  ["will not disclose", "had not disclosed", "did not disclose", NI], "C",
  "'Would rather' + subject + past form for a present or future preference",
  "When 'would rather' introduces a different subject, the verb takes the simple past even though the meaning is "
  "present or future: 'I would rather you did not disclose your PIN'.",
  ["Structure: I would rather + you + verb", "Rule: use the past simple for present/future meaning",
   "'do not disclose' → 'did not disclose'"],
  "'Will not disclose' breaks the rule. 'Had not disclosed' is used for regrets about the past, not for advice "
  "about the future. The original is wrong, so 'No improvement required' does not apply.", 40)

Q(SI, "Bold-part improvement", "Advanced",
  SI_STEM + "The committee, **comprising of five senior economists**, submitted its report to the governor.",
  ["comprises five senior economists", "comprising five senior economists", "comprised from five senior economists",
   NI], "B",
  "'Comprise' is followed directly by its object; 'comprising of' is incorrect ('consisting of' is the "
  "alternative)",
  "'Comprise' means 'consist of', so it takes no 'of': 'The committee, comprising five senior economists, "
  "submitted...'.",
  ["'Comprise' already contains the idea of 'of'", "Drop 'of': 'comprising five senior economists'"],
  "A creates a second finite verb inside the commas ('comprises ... submitted'), which is ungrammatical. C "
  "('comprised from') is not idiomatic. The original 'comprising of' is wrong, so 'No improvement required' does "
  "not apply.", 40)

Q(SI, "Bold-part improvement", "Advanced",
  SI_STEM + "**Scarcely had the rate cut been announced when** bond yields began to fall.",
  ["Scarcely had the rate cut been announced than", "Scarcely the rate cut had been announced when",
   "Scarcely had the rate cut announced when", NI], "D",
  "'Scarcely/Hardly ... when' with inversion; passive 'had been announced'",
  "The sentence is correct. 'Scarcely' at the start needs inversion ('had the rate cut been announced'), its "
  "partner is 'when', and a rate cut is announced by someone, so the passive is right.",
  ["Inversion after 'Scarcely': had + subject + been + past participle: present",
   "Partner word: 'when' (not 'than'): present", "Passive needed: present", "No improvement required"],
  "A uses 'than', which pairs with 'no sooner', not 'scarcely'. B drops the required inversion. C makes the rate "
  "cut announce something (active voice), which is illogical.", 40)

# =====================================================================================================================
# PHRASE REPLACEMENT
# =====================================================================================================================
PR = "Phrase Replacement"
PR_STEM = ("Which of the following should replace the phrase in bold to make the sentence grammatically and "
           "contextually correct? If no replacement is needed, choose 'No replacement required'.\n")

Q(PR, "Replace the phrase", "Basic",
  PR_STEM + "The customer **insisted to meet** the branch manager personally.",
  ["insisted for meeting", "insisted on meeting", "insisted at meeting", NR], "B",
  "'Insist' takes the preposition 'on' followed by a gerund",
  "The fixed pattern is 'insist on + -ing': 'The customer insisted on meeting the branch manager'.",
  ["'Insist' does not take a to-infinitive", "Pattern: insist on + gerund", "'insisted on meeting'"],
  "'For' and 'at' are the wrong prepositions after 'insist'. The original 'insisted to meet' is wrong, so 'No "
  "replacement required' does not apply.", 30)

Q(PR, "Replace the phrase", "Intermediate",
  PR_STEM + "The bank decided to **do away from** the minimum balance requirement for student accounts.",
  ["do away with", "do off with", "do away by", NR], "A",
  "Phrasal verb 'do away with' = abolish, get rid of",
  "The bank is abolishing the requirement. The phrasal verb for this is 'do away with'.",
  ["Meaning needed: abolish the requirement", "Phrasal verb: 'do away with'"],
  "'Do off with' and 'do away by' are not English phrasal verbs. The original 'do away from' is wrong, so 'No "
  "replacement required' does not apply.", 30)

Q(PR, "Replace the phrase", "Intermediate",
  PR_STEM + "The two banks have agreed to **work in tandem** to expand ATM coverage in remote areas.",
  ["work in tandom", "work on tandem", "working in tandem", NR], "D",
  "Idiom 'in tandem' = together, side by side; 'agree to' + base verb",
  "'Agreed to work in tandem' is correct: 'agree to' takes the base form, and 'in tandem' means working together. "
  "No replacement is needed.",
  ["'agreed to' + base verb 'work': correct", "'in tandem' is the correct idiom and spelling",
   "So no replacement is required"],
  "A misspells 'tandem'. B uses the wrong preposition ('on'). C gives 'agreed to working', which is wrong because "
  "the 'to' here is part of the infinitive.", 30)

Q(PR, "Replace the phrase", "Advanced",
  PR_STEM + "The minister said that the new rules would **come into force with immediate effect from** next month.",
  ["come in force with immediate effect from", "came into force with immediate effect from", "come into force from",
   NR], "C",
  "Logical consistency: 'with immediate effect' cannot apply to a future date",
  "'With immediate effect' means starting now, which contradicts 'from next month'. Removing it gives 'would come "
  "into force from next month', which is grammatical and logical.",
  ["Check meaning: 'immediate' vs 'next month' clash", "Remove 'with immediate effect'",
   "'would come into force from next month' is correct"],
  "A keeps the contradiction and also changes the idiom to 'in force'. B keeps the contradiction and puts a past "
  "form after 'would'. The original is self-contradictory, so 'No replacement required' does not apply.", 45)

# =====================================================================================================================
# SENTENCE CORRECTION
# =====================================================================================================================
SC = "Sentence Correction"

Q(SC, "Correct sentence", "Basic",
  "Which of the following sentences is grammatically correct?",
  ["The furnitures in the new branch are expensive.", "The furniture in the new branch is expensive.",
   "The furniture in the new branch are expensive.", "The furnitures in the new branch is expensive."], "B",
  "'Furniture' is an uncountable noun: no plural form, singular verb",
  "'Furniture' has no plural ('furnitures' is wrong) and takes a singular verb. Only 'The furniture ... is "
  "expensive' is correct.",
  ["'Furniture' is uncountable: remove options with 'furnitures' (A, D)",
   "Uncountable nouns take a singular verb: 'is', not 'are' (removes C)", "Option B"],
  "A and D use the non-existent plural 'furnitures'. C uses the plural verb 'are' with an uncountable noun.", 30)

Q(SC, "Grammatically incorrect sentence", "Intermediate",
  "Which of the following sentences is grammatically INCORRECT?",
  ["Neither of the answers is correct.", "The scissors are on the table.",
   "Ten kilometres is a long distance to walk.", "Mathematics are my favourite subject."], "D",
  "Nouns ending in -s that take a singular verb (subjects like mathematics, economics)",
  "Names of subjects such as 'mathematics' are singular in meaning and take a singular verb: 'Mathematics is my "
  "favourite subject'. The other three sentences are correct.",
  ["A: 'Neither of + plural' takes a singular verb: 'is' is correct",
   "B: 'scissors' is always plural: 'are' is correct",
   "C: a distance treated as one amount takes a singular verb: correct",
   "D: 'Mathematics' needs 'is': incorrect"],
  "A, B and C are all correct for the reasons given in the steps, so they are not the incorrect sentence.", 40)

Q(SC, "Correct sentence", "Intermediate",
  "Which of the following sentences is grammatically correct?",
  ["If he apply today, he will get the loan by Monday.", "If he applies today, he will get the loan by Monday.",
   "If he applied today, he will get the loan by Monday.", "If he had applied today, he will get the loan by Monday."],
  "B",
  "First conditional: If + simple present, ... will + base verb",
  "A real, possible future condition uses the simple present in the if-clause and 'will' in the main clause: 'If he "
  "applies today, he will get the loan by Monday'.",
  ["The main clause uses 'will get': first conditional",
   "The if-clause therefore needs the simple present, third person: 'applies'", "Option B"],
  "A lacks the third-person '-s'. C mixes a second-conditional if-clause with 'will'. D mixes a third-conditional "
  "if-clause with 'will', and 'had applied today' is illogical.", 35)

Q(SC, "Grammatically incorrect sentence", "Advanced",
  "Which of the following sentences is grammatically INCORRECT?",
  ["Only after the inquiry the bank suspended the officer.",
   "Seldom have we seen such strong demand for gold loans.",
   "No sooner did the market open than prices crashed.",
   "Not until the audit was complete did the board approve the accounts."], "A",
  "Inversion after restrictive or negative openers (only after, seldom, no sooner, not until)",
  "When a sentence begins with 'Only after ...', the main clause must be inverted: 'Only after the inquiry did the "
  "bank suspend the officer'. Option A lacks the inversion.",
  ["Each option opens with a restrictive or negative adverbial", "Each such opener requires auxiliary + subject",
   "B, C and D invert correctly ('have we', 'did the market', 'did the board')",
   "A does not ('the bank suspended'): incorrect"],
  "B, C and D all use correct inversion and correct partner words ('No sooner ... than'), so they are correct "
  "sentences.", 45)

# =====================================================================================================================
# PARA JUMBLES
# =====================================================================================================================
PJ = "Para Jumbles"
PJ5 = ("Rearrange the following five sentences (A), (B), (C), (D) and (E) to form a meaningful paragraph. Then "
       "choose the correct order.\n")
PJF = ("Sentence (1) is fixed as the first sentence. Rearrange sentences P, Q, R and S that follow it to form a "
       "meaningful paragraph, and choose the correct order.\n")

Q(PJ, "Five-sentence jumble", "Basic",
  PJ5 + "(A) Within minutes, the helpline blocked the card and registered a complaint.\n"
  "(B) Rohan realised that his debit card had not come out of the ATM.\n"
  "(C) A week later, a new card arrived at his home by post.\n"
  "(D) Worried, he immediately called the helpline number printed on the machine.\n"
  "(E) He had collected his cash but had forgotten to take the card back.",
  ["BDEAC", "EBDAC", "BEDAC", "BEADC"], "C",
  "Para jumble: opener with a named person, then pronouns and time markers",
  "B introduces Rohan and the problem. E explains it ('He had collected his cash ...'). D shows his reaction (called "
  "the helpline), A follows ('Within minutes, the helpline ...') and C closes the story ('A week later').",
  ["Opener: B (names Rohan; E and D use 'he')", "E explains B, so B-E",
   "D (calls helpline) must precede A (helpline acts)", "C ('A week later') is last: B-E-D-A-C"],
  "BDEAC puts the explanation after he has already called. EBDAC opens with 'He' before Rohan is named. BEADC has "
  "the helpline act before he calls it.", 60)

Q(PJ, "Fixed sentence", "Basic",
  PJF + "(1) Small savings schemes run by the post office remain popular in rural India.\n"
  "(P) They offer a guaranteed return backed by the government.\n"
  "(Q) This makes them attractive to people who cannot afford to take risks.\n"
  "(R) Moreover, a post office is often closer than the nearest bank branch.\n"
  "(S) As a result, many villagers prefer to keep their savings there.",
  ["PRQS", "QPRS", "RPQS", "PQRS"], "D",
  "Fixed opener; link pronouns ('They', 'This') and connectors ('Moreover', 'As a result')",
  "P gives the first reason ('They' = the schemes). Q comments on it ('This' = the guaranteed return). R adds a "
  "second reason with 'Moreover'. S states the result.",
  ["(1) → P: 'They' refers to the schemes", "P → Q: 'This' refers to the guaranteed return",
   "R: 'Moreover' adds a further reason", "S: 'As a result' concludes: PQRS"],
  "PRQS separates Q from the guarantee it refers to. QPRS and RPQS start with 'This' or 'Moreover' before any "
  "reason has been given.", 60)

Q(PJ, "Five-sentence jumble", "Basic",
  PJ5 + "(A) However, a survey a year later found that fewer than half the saplings had survived.\n"
  "(B) Last monsoon, the town council organised a drive to plant ten thousand saplings.\n"
  "(C) Most of the rest had died because no one had been given the task of watering them.\n"
  "(D) Hundreds of volunteers, including schoolchildren, took part with great enthusiasm.\n"
  "(E) This year, the council has therefore assigned each sapling to a local family.",
  ["BDACE", "BADCE", "DBACE", "BDCAE"], "A",
  "Chronology plus connectors ('However', 'the rest', 'therefore')",
  "B starts the story (the drive). D describes the drive. A turns ('However') to the survey. C explains the deaths "
  "('the rest' = those that did not survive). E gives the council's response ('therefore').",
  ["Opener: B (sets time and event)", "D describes participation in that drive",
   "A ('However ... fewer than half survived') → C ('Most of the rest had died')",
   "E ('therefore') is the solution: BDACE"],
  "BADCE puts the survey before the drive is described and splits A from C. DBACE starts with volunteers before the "
  "drive is introduced. BDCAE puts 'the rest' before we know that only some saplings survived.", 60)

Q(PJ, "Five-sentence jumble", "Intermediate",
  PJ5 + "(A) When prices rise persistently, the central bank usually responds by raising its policy rate.\n"
  "(B) Higher borrowing costs discourage households and firms from taking fresh loans.\n"
  "(C) Raise rates too far, though, and the economy may slow more sharply than intended.\n"
  "(D) With less borrowing, overall demand cools and price pressures ease over time.\n"
  "(E) The art of monetary policy therefore lies in judging how much tightening is enough.",
  ["ADBCE", "ABDCE", "ABCDE", "ACBDE"], "B",
  "Cause-and-effect chain followed by a caveat and a conclusion",
  "A: inflation leads to a rate hike. B: higher rates reduce borrowing. D: less borrowing cools demand. C: the "
  "caveat ('though') about raising too far. E: the conclusion ('therefore').",
  ["A is the opener (sets up the situation)", "B follows the rate hike; D needs 'less borrowing' from B",
   "C ('though') qualifies the whole mechanism", "E concludes: ABDCE"],
  "ADBCE puts the effect of less borrowing before borrowing falls. ABCDE inserts the caveat in the middle of the "
  "chain. ACBDE states the caveat before the mechanism.", 70)

Q(PJ, "Fixed sentence", "Intermediate",
  PJF + "(1) Many young graduates today prefer to start their own ventures rather than seek salaried jobs.\n"
  "(P) Yet most new ventures fail within their first few years.\n"
  "(Q) Easy access to digital tools has made it cheaper than ever to launch a business.\n"
  "(R) The reasons are rarely a lack of ideas; more often, the founders run out of working capital.\n"
  "(S) Mentoring and patient credit could therefore improve their chances of survival considerably.",
  ["PRQS", "QRPS", "QPRS", "PQRS"], "C",
  "Fixed opener; explanation, contrast, reasons, solution",
  "Q explains why graduates choose ventures. P turns ('Yet') to failure. R gives the reasons for failure. S offers "
  "the solution ('therefore'), which answers R's point about working capital.",
  ["(1) → Q: why starting ventures is attractive", "P: 'Yet' introduces the contrast (failure)",
   "R: 'The reasons' = reasons for the failure in P", "S: solution: QPRS"],
  "PRQS and PQRS put Q (why launching is easy) after the failures, breaking the link between R's reasons and S's "
  "solution or between P and R. QRPS gives 'The reasons' before any failure is mentioned.", 70)

Q(PJ, "Five-sentence jumble", "Intermediate",
  PJ5 + "(A) Before it arrived, sending money to a friend usually meant knowing their account number and the "
  "branch's IFSC code.\n"
  "(B) The Unified Payments Interface changed the way Indians move money.\n"
  "(C) Now a phone number or a QR code is enough, and the transfer is completed in seconds.\n"
  "(D) Its simplicity has drawn in even small vendors who had never accepted cards.\n"
  "(E) As a result, a tea stall today may record more digital transactions in a day than a large shop did a decade "
  "ago.",
  ["BCADE", "ABCDE", "BADCE", "BACDE"], "D",
  "Before/now contrast, then consequence",
  "B introduces UPI. A describes the situation before it ('Before it arrived'). C describes now. D refers to 'its "
  "simplicity', just shown in C. E gives the result.",
  ["Opener: B (names UPI; A and D use 'it'/'its')", "A ('Before') → C ('Now') is a natural pair",
   "D ('Its simplicity') follows the description of simplicity in C", "E ('As a result') ends: BACDE"],
  "BCADE puts 'Now' before 'Before'. ABCDE starts with 'it' before UPI is named. BADCE mentions simplicity before "
  "it has been described.", 70)

Q(PJ, "Fixed sentence", "Intermediate",
  PJF + "(1) Credit scores were designed to help lenders judge risk quickly.\n"
  "(P) A first-time borrower therefore has no score at all.\n"
  "(Q) But a score can be built only from a record of past borrowing.\n"
  "(R) Ironically, this means that the people who most need a first loan find it hardest to get one.\n"
  "(S) Some lenders now use alternative data, such as rent and utility payments, to fill this gap.",
  ["QPRS", "QRPS", "PQRS", "RQPS"], "A",
  "Logical chain: limitation → consequence → irony → solution",
  "Q states the limitation ('But'). P draws the consequence ('therefore'). R comments on it ('this means'). S gives "
  "the remedy for 'this gap'.",
  ["(1) → Q: 'But' introduces the limitation", "P's 'therefore' follows directly from Q",
   "R's 'this' refers to P's no-score borrower", "S closes with the remedy: QPRS"],
  "QRPS puts R's 'this means' before P, so 'this' has nothing to refer to. PQRS and RQPS start with a consequence "
  "before its cause.", 70)

Q(PJ, "Five-sentence jumble", "Advanced",
  PJ5 + "(A) Critics counter that such a payment would strain public finances and might weaken the incentive to "
  "work.\n"
  "(B) The idea of a universal basic income, a regular cash payment to every citizen with no conditions attached, "
  "has gained fresh attention.\n"
  "(C) Supporters argue that it would simplify a tangle of overlapping welfare schemes and reduce leakages.\n"
  "(D) Evidence from pilot projects, though limited, suggests that the second fear may be exaggerated.\n"
  "(E) Recipients in several trials continued to work, and some used the money to start small businesses.",
  ["BACDE", "BCDAE", "BCADE", "BADCE"], "C",
  "Argument structure: idea → for → against → evidence on one objection",
  "B defines the idea. C gives the supporters' view. A gives the critics' counter ('counter' needs a prior "
  "argument). D refers to 'the second fear' (weakened incentive to work, from A). E gives the evidence.",
  ["Opener: B (defines the idea)", "'Critics counter' needs an argument first: C before A",
   "D's 'second fear' points to A's second concern", "E supports D: BCADE"],
  "BACDE and BADCE put the critics' counter before the supporters' argument. BCDAE mentions 'the second fear' "
  "before any fears are stated.", 85)

Q(PJ, "Five-sentence jumble", "Advanced",
  PJ5 + "(A) Larger balance sheets, it was argued, would allow the merged banks to finance big infrastructure "
  "projects.\n"
  "(B) Over the past decade, several public sector banks have been merged into fewer, larger entities.\n"
  "(C) The gains, however, have been slower to materialise than the promises suggested.\n"
  "(D) Integrating different technology systems and work cultures has proved to be a lengthy exercise.\n"
  "(E) The rationale was that scale would bring efficiency and greater lending capacity.",
  ["BAECD", "BEACD", "BECAD", "EBACD"], "B",
  "Event → rationale → elaboration → reality check → explanation",
  "B states the event (mergers). E gives the rationale. A elaborates one argued benefit ('it was argued'). C turns "
  "('however') to the slow gains. D explains why.",
  ["Opener: B", "E ('The rationale') explains why the mergers were done",
   "A develops the rationale; C ('however') contrasts it with results", "D explains C: BEACD"],
  "BAECD gives a specific argument before the general rationale. BECAD puts the turn ('however') before the "
  "argument is complete. EBACD has 'The rationale' before the event it explains.", 85)

Q(PJ, "Fixed sentence", "Advanced",
  "Sentence (5) is fixed as the last sentence. Rearrange sentences P, Q, R and S that come before it to form a "
  "meaningful paragraph, and choose the correct order.\n"
  "(P) Over time, however, some forest departments began to treat these communities as partners.\n"
  "(Q) For decades, forest policy treated villagers living near protected areas as a threat to the forest.\n"
  "(R) Where villagers were given such a role, along with a share of the income from forest produce, illegal "
  "felling fell sharply.\n"
  "(S) Their access to grazing land and firewood was restricted, often with little consultation.\n"
  "(5) The forest, it turned out, was safest in the hands of those who depended on it.",
  ["QSRP", "SQPR", "QPSR", "QSPR"], "D",
  "Fixed closing sentence; past policy → its effect → turn → result → conclusion",
  "Q opens with the old policy. S describes it ('Their' = the villagers). P turns ('however') to partnership. R "
  "reports the result ('such a role' = partners). The fixed conclusion follows.",
  ["Opener: Q ('For decades')", "S's 'Their' refers to the villagers in Q",
   "P ('however') must follow the old policy; R's 'such a role' refers to P's partners",
   "R leads into (5): QSPR"],
  "QSRP puts 'such a role' before the role is mentioned. SQPR starts with 'Their' before the villagers are "
  "introduced. QPSR places the restrictions after the turn to partnership.", 85)

# =====================================================================================================================
# SENTENCE REARRANGEMENT
# =====================================================================================================================
SR = "Sentence Rearrangement"
SR_STEM = ("Rearrange the following parts (P), (Q), (R) and (S) to form a meaningful and grammatically correct "
           "sentence.\n")

Q(SR, "Word/phrase rearrangement within a sentence", "Basic",
  SR_STEM + "(P) who had lost her passbook\n(Q) the elderly woman\n(R) was issued a new one\n(S) within a day",
  ["QRPS", "QPRS", "PQRS", "RQPS"], "B",
  "Relative clause directly after its noun; 'one' needs an earlier referent",
  "'The elderly woman who had lost her passbook was issued a new one within a day.' The relative clause P must "
  "follow 'woman', and 'a new one' (R) needs 'passbook' before it.",
  ["Subject: Q ('the elderly woman')", "P ('who had lost her passbook') must follow its noun",
   "R ('was issued a new one') refers back to the passbook", "S ends the sentence: QPRS"],
  "QRPS separates the relative clause from its noun and puts 'one' before 'passbook'. PQRS and RQPS cannot begin a "
  "sentence sensibly.", 35)

Q(SR, "Word/phrase rearrangement within a sentence", "Intermediate",
  SR_STEM + "(P) the regulator has asked banks\n(Q) that are not\n(R) to stop charging penalties on loans\n"
  "(S) linked to any specific default",
  ["PQSR", "RPQS", "PRQS", "PSQR"], "C",
  "'Ask + object + to-infinitive'; the relative clause follows the noun it describes",
  "'The regulator has asked banks to stop charging penalties on loans that are not linked to any specific "
  "default.' 'Asked banks' takes the infinitive R; 'that are not linked ...' (Q + S) describes 'penalties on "
  "loans'.",
  ["Start: P (subject + verb + object)", "'asked banks' + 'to stop ...' (R)",
   "Q + S form one relative clause: 'that are not linked to any specific default'", "PRQS"],
  "PQSR makes banks, not penalties, 'not linked to any default', which is nonsensical. RPQS and PSQR do not form a "
  "grammatical sentence.", 45)

Q(SR, "Word/phrase rearrangement within a sentence", "Advanced",
  SR_STEM + "(P) but it has also\n(Q) not only has the bank\n(R) passed the benefit on to existing borrowers\n"
  "(S) cut its lending rate",
  ["QRPS", "SQPR", "PSQR", "QSPR"], "D",
  "'Not only + inversion ..., but ... also'; a definite noun ('the benefit') needs a referent",
  "'Not only has the bank cut its lending rate, but it has also passed the benefit on to existing borrowers.' The "
  "benefit is the rate cut, so S must come before R.",
  ["Opener: Q ('Not only has the bank' with inversion)", "Q + S: 'cut its lending rate'",
   "P + R: 'but it has also passed the benefit on ...'", "'the benefit' refers to the rate cut: QSPR"],
  "QRPS mentions 'the benefit' before the rate cut that creates it. SQPR and PSQR break the 'not only ... but also' "
  "frame.", 50)

# =====================================================================================================================
# FILL IN THE BLANKS
# =====================================================================================================================
FB = "Fill in the Blanks"
FB1 = "Choose the word that best fills the blank.\n"
FB2 = "Choose the pair of words that best fills the blanks.\n"
FBP = "Choose the phrase that best fills the blank.\n"

Q(FB, "Single blank", "Basic",
  FB1 + "The branch will remain ______ on the second and fourth Saturdays of every month.",
  ["closed", "close", "closing", "closure"], "A",
  "'Remain' + adjective (subject complement)",
  "'Remain' is a linking verb and takes an adjective: 'remain closed'. 'Closed' is the adjective describing a branch "
  "that is not open.",
  ["'remain' is a linking verb like 'be'", "It needs an adjective complement", "'closed' fits"],
  "'Close' as an adjective means near ('remain close to'), which does not fit. 'Closing' suggests an ongoing action, "
  "and 'closure' is a noun.", 25)

Q(FB, "Single blank", "Basic",
  FB1 + "The farmer could not repay the loan ______ the failure of his crop.",
  ["because", "due", "owing to", "despite"], "C",
  "Prepositions of cause: 'owing to', 'because of'",
  "A noun phrase ('the failure of his crop') follows the blank, so a prepositional phrase of cause is needed: "
  "'owing to the failure of his crop'.",
  ["What follows the blank: a noun phrase", "Cause is needed: owing to / because of",
   "Only 'owing to' is among the options"],
  "'Because' alone needs a clause or 'of'. 'Due' alone needs 'to'. 'Despite' expresses contrast, which reverses the "
  "meaning.", 25)

Q(FB, "Double blank", "Basic",
  FB2 + "The auditor was ______ by the number of errors in the ledger and ______ a detailed inquiry.",
  ["surprising, recommending", "surprise, recommends", "surprised, recommending", "surprised, recommended"], "D",
  "-ed adjective for feelings; parallel verbs joined by 'and'",
  "A person feels 'surprised' (by something). 'And' joins two past-tense actions of the auditor: 'was surprised ... "
  "and recommended'.",
  ["Blank 1: the auditor's feeling = 'surprised'", "Blank 2: parallel with 'was': past tense 'recommended'",
   "Option D"],
  "'Surprising' describes the cause, not the person. 'Surprise ... recommends' breaks both grammar and tense. "
  "'Surprised, recommending' breaks the parallel structure after 'and'.", 30)

Q(FB, "Phrase fillers", "Basic",
  FBP + "After months of negotiation, the two companies finally ______ an agreement on the merger.",
  ["reached to", "arrived at", "arrived on", "came at"], "B",
  "Collocation: 'arrive at / reach / come to an agreement'",
  "One 'arrives at' an agreement (or 'reaches' an agreement without 'to'). 'Arrived at an agreement' is correct.",
  ["Check each preposition with 'agreement'", "'arrive at an agreement' is standard", "Option B"],
  "'Reach' is transitive and takes no 'to'. 'Arrived on' and 'came at' are not idiomatic with 'agreement' (the "
  "idiom is 'came to an agreement').", 25)

Q(FB, "Single blank", "Intermediate",
  FB1 + "The finance minister said that the deficit target, though ambitious, was ______ if spending was kept in "
  "check.",
  ["attainable", "elusive", "impossible", "unthinkable"], "A",
  "Concession ('though ambitious') plus a condition that makes success possible",
  "'Though ambitious' concedes that the target is hard; 'if spending was kept in check' gives the condition for "
  "success. So the target was attainable.",
  ["'though ambitious' = hard but not impossible", "'if spending was kept in check' = a condition for success",
   "'attainable' fits"],
  "'Elusive', 'impossible' and 'unthinkable' all say the target cannot be reached, which clashes with the "
  "condition for success.", 35)

Q(FB, "Double blank", "Intermediate",
  FB2 + "The new rules are meant to ______ small investors from mis-selling, but critics fear they will merely "
  "______ the paperwork without improving outcomes.",
  ["expose, increase", "shield, reduce", "protect, increase", "guard, simplify"], "C",
  "Purpose vs criticism signalled by 'but ... fear ... merely'",
  "Rules are 'meant to protect investors from mis-selling'. Critics 'fear' an undesirable result: the rules will "
  "merely increase paperwork.",
  ["Blank 1: purpose of investor rules: protect/shield/guard (not expose)",
   "Blank 2: something critics fear: increase (not reduce or simplify)", "Only 'protect, increase' fits both"],
  "'Expose' reverses the purpose. 'Reduce' and 'simplify' paperwork would not be a fear. 'Guard from' is also less "
  "idiomatic than 'guard against'.", 40)

Q(FB, "Double blank", "Intermediate",
  FB2 + "Although the company's revenue rose ______, its profits ______ because of rising input costs.",
  ["steadily, soared", "sharply, declined", "marginally, surged", "sharply, multiplied"], "B",
  "'Although' needs contrast between the clauses",
  "'Although' signals contrast: revenue went up, but profits went down because of rising costs. 'Sharply, "
  "declined' gives that contrast.",
  ["Rising input costs reduce profits", "So blank 2 must be a fall: 'declined'",
   "Blank 1 is a rise: 'sharply' fits", "Option B"],
  "'Soared', 'surged' and 'multiplied' all show profits rising, which removes the contrast required by "
  "'although' and contradicts 'rising input costs'.", 35)

Q(FB, "Phrase fillers", "Intermediate",
  FBP + "The bank had to ______ its plan to open fifty new branches when the economy slowed down.",
  ["put up", "put on", "put across", "put off"], "D",
  "Phrasal verbs with 'put': put off = postpone",
  "When the economy slowed, the bank had to postpone its expansion plan. 'Put off' means postpone.",
  ["Meaning needed: delay the plan because of the slowdown", "'put off' = postpone", "Option D"],
  "'Put up' means to build or to offer, 'put on' means to wear or stage, and 'put across' means to communicate "
  "an idea. None means postpone.", 30)

Q(FB, "Single blank", "Intermediate",
  FB1 + "The governor's remarks were deliberately ______, leaving markets unsure whether a rate cut was coming.",
  ["explicit", "emphatic", "ambiguous", "transparent"], "C",
  "Result clause decides the word ('leaving markets unsure')",
  "The remarks left markets unsure, so they must have been open to more than one interpretation: ambiguous.",
  ["Result: markets are unsure", "Cause must be unclear remarks", "'ambiguous' fits"],
  "'Explicit', 'emphatic' and 'transparent' describe clear, forceful statements, which would remove uncertainty.",
  35)

Q(FB, "Single blank", "Advanced",
  FB1 + "The auditor's report was so ______ that even the bank's harshest critics could find little to dispute in "
  "it.",
  ["cursory", "rigorous", "perfunctory", "superficial"], "B",
  "'So ... that' result clause: the quality must explain why critics found little to dispute",
  "Critics could find little to dispute because the report was thorough and exacting: rigorous.",
  ["Result: even harsh critics could not fault it", "Cause: a thorough report", "'rigorous' fits"],
  "'Cursory', 'perfunctory' and 'superficial' all mean hasty or shallow, which would invite criticism rather than "
  "silence it.", 35)

Q(FB, "Double blank", "Advanced",
  FB2 + "The government's attempt to ______ the slowdown with a stimulus package was criticised as ______, since "
  "the measures were too small to make any real difference.",
  ["counter, token", "worsen, generous", "counter, lavish", "ignore, excessive"], "A",
  "Purpose of a stimulus; criticism explained by 'too small'",
  "A stimulus aims to counter a slowdown. It was criticised as 'token' (symbolic, minimal) because the measures "
  "were too small.",
  ["Blank 1: a stimulus fights a slowdown: 'counter'",
   "Blank 2: criticism because measures were too small: 'token'", "Option A"],
  "'Worsen' and 'ignore' are not the aim of a stimulus. 'Generous', 'lavish' and 'excessive' contradict 'too small'.",
  40)

Q(FB, "Double blank", "Advanced",
  FB2 + "Far from being ______ by the setback, the young entrepreneur ______ her business model and returned with "
  "a stronger proposal.",
  ["elated, refined", "encouraged, abandoned", "daunted, refined", "daunted, ignored"], "C",
  "'Far from being X' denies X; the second blank must lead to 'a stronger proposal'",
  "'Far from being daunted' (discouraged) by the setback, she improved (refined) her model and came back stronger.",
  ["Blank 1: a natural reaction to a setback that she did NOT have: 'daunted'",
   "Blank 2: an action that produces a stronger proposal: 'refined'", "Option C"],
  "'Elated' is not a likely reaction to a setback, so denying it says nothing. 'Encouraged by the setback' is "
  "illogical. 'Ignored' her model does not explain the stronger proposal.", 40)

Q(FB, "Phrase fillers", "Advanced",
  FBP + "With inflation proving more stubborn than expected, the central bank is unlikely to ______ its tight "
  "stance any time soon.",
  ["come up with", "fall back upon", "look up to", "move away from"], "D",
  "Phrase meaning: the bank will not abandon its tight stance while inflation persists",
  "Stubborn inflation means the bank will keep policy tight, i.e. it is unlikely to move away from (abandon) its "
  "tight stance.",
  ["Stubborn inflation → keep policy tight", "'unlikely to ___ its tight stance' needs 'abandon'",
   "'move away from' fits"],
  "'Come up with' means to produce an idea; the stance already exists. 'Fall back upon' means to rely on as a "
  "reserve. 'Look up to' means to admire.", 35)

# =====================================================================================================================
# WORD USAGE
# =====================================================================================================================
WU = "Word Usage"

Q(WU, "Correct usage of a word", "Basic",
  "In which of the following sentences is the word 'principal' used correctly?",
  ["The bank follows a strict principal of confidentiality.",
   "The principal reason for the delay was a network outage.",
   "He refused to compromise his principals.",
   "The principal of fair lending must be respected."], "B",
  "Principal (main; head; sum lent) vs principle (rule, belief)",
  "'Principal' as an adjective means main or most important: 'the principal reason'. A rule or belief is a "
  "'principle'.",
  ["A, C and D refer to rules or beliefs: they need 'principle(s)'",
   "B uses 'principal' to mean 'main': correct"],
  "A ('principle of confidentiality'), C ('his principles') and D ('principle of fair lending') all need "
  "'principle'.", 30)

Q(WU, "Word swap", "Intermediate",
  "In the sentence below, four words are in bold. Two of them may need to be interchanged to make the sentence "
  "meaningful. Choose the correct swap; if no swap is needed, choose 'No swap required'.\n"
  "A weaker **(A) deficit** makes imports more expensive and can widen the current account **(B) rupee**, unless "
  "**(C) exports** rise fast enough to **(D) offset** the effect.",
  ["A-C", "A-B", "B-D", "No swap required"], "B",
  "Word swap: check each bold word in its slot",
  "A currency weakens, and a deficit widens. Swapping A and B gives: 'A weaker rupee makes imports more expensive "
  "and can widen the current account deficit, unless exports rise fast enough to offset the effect.'",
  ["'A weaker deficit' and 'current account rupee' make no sense",
   "Swap them: 'weaker rupee', 'current account deficit'",
   "'exports' and 'offset' are already correct"],
  "A-C gives 'A weaker exports' and 'current account rupee'. B-D gives 'the current account offset' and 'to "
  "rupee the effect'. The sentence clearly needs a swap.", 40)

Q(WU, "Correct usage of a word", "Intermediate",
  "In which of the following sentences is the word 'elicit' used correctly?",
  ["Selling counterfeit goods is an elicit trade.", "The bank elicited the loan to the farmer.",
   "The survey was designed to elicit honest responses from customers.",
   "He elicited from the meeting before it ended."], "C",
  "Elicit (verb: draw out a response) vs illicit (adjective: illegal)",
  "'Elicit' is a verb meaning to draw out or evoke a response or information: 'to elicit honest responses'.",
  ["A needs 'illicit' (illegal)", "B needs a verb like 'sanctioned'", "D needs a verb like 'exited' or 'withdrew'",
   "C uses 'elicit' correctly"],
  "A confuses 'elicit' with 'illicit'. B and D use 'elicit' where 'sanctioned' and 'withdrew' are meant.", 35)

Q(WU, "Correct usage of a word", "Advanced",
  "In which of the following sentences is the word 'tenuous' used correctly?",
  ["She kept a tenuous grip on the rope and climbed with great confidence.",
   "Its tenuous profits made it the strongest lender in the region.",
   "He delivered a tenuous speech that lasted three hours.",
   "The link between the two events is tenuous at best, so the inquiry found no evidence of collusion."], "D",
  "Tenuous = very weak or slight (of a connection, argument or hold)",
  "A 'tenuous link' is a very weak connection, which fits an inquiry finding no evidence of collusion.",
  ["Meaning: very weak or slight", "D: weak link → no evidence: consistent",
   "A: a weak grip clashes with 'great confidence'", "B and C: 'tenuous' does not suit profits that make a bank "
   "strongest, or a long speech"],
  "A contradicts itself (weak grip, great confidence). B: weak profits cannot make a bank the strongest. C: a "
  "speech is not described as tenuous because of its length.", 40)

# =====================================================================================================================
# VOCABULARY
# =====================================================================================================================
VO = "Vocabulary"

Q(VO, "Contextual meaning", "Basic",
  "Choose the meaning of the word 'waived' as used in the sentence:\n"
  "'The bank waived the late fee because the delay was caused by its own server failure.'",
  ["chose not to demand", "charged in full", "doubled", "postponed"], "A",
  "Waive = refrain from insisting on a right or claim",
  "The delay was the bank's own fault, so it gave up its claim to the late fee. 'Waived' means chose not to demand "
  "it.",
  ["Context: the bank caused the delay", "Fair action: not charging the fee", "'waived' = chose not to demand"],
  "'Charged in full' and 'doubled' are the opposite of what the context suggests. 'Postponed' means delayed, not "
  "given up.", 25)

Q(VO, "Word pairs", "Intermediate",
  "Which of the following pairs consists of words that are OPPOSITE in meaning?",
  ["Frugal – Thrifty", "Prudent – Reckless", "Candid – Frank", "Lucid – Clear"], "B",
  "Word pairs: identify synonyms and antonyms",
  "'Prudent' means careful and sensible; 'reckless' means careless of consequences. They are opposites. The other "
  "pairs are synonyms.",
  ["Frugal = thrifty (synonyms)", "Prudent ≠ reckless (antonyms)", "Candid = frank (synonyms)",
   "Lucid = clear (synonyms)"],
  "A, C and D are pairs of synonyms, not opposites.", 30)

Q(VO, "Contextual meaning", "Intermediate",
  "Choose the meaning of the word 'placate' as used in the sentence:\n"
  "'The minister's announcement was seen as an attempt to placate farmers angered by the fall in crop prices.'",
  ["provoke", "mislead", "pacify", "ignore"], "C",
  "Placate = make someone less angry",
  "The farmers are angry; an attempt to placate them is an attempt to calm or pacify them.",
  ["Context: farmers are angry", "A minister's announcement aims to calm them", "'placate' = pacify"],
  "'Provoke' is the opposite. 'Mislead' and 'ignore' do not mean calming someone's anger.", 25)

Q(VO, "Word pairs", "Advanced",
  "Which of the following pairs consists of words that are SIMILAR in meaning?",
  ["Obdurate – Pliant", "Laconic – Verbose", "Ephemeral – Enduring", "Sagacious – Astute"], "D",
  "Advanced vocabulary: synonym and antonym pairs",
  "'Sagacious' and 'astute' both mean shrewd and wise in judgement. The other pairs are opposites.",
  ["Obdurate (stubborn) ≠ pliant (easily influenced)", "Laconic (using few words) ≠ verbose (wordy)",
   "Ephemeral (short-lived) ≠ enduring", "Sagacious = astute (both: shrewd, wise)"],
  "A, B and C are antonym pairs, not synonyms.", 30)

# =====================================================================================================================
# SYNONYMS / ANTONYMS
# =====================================================================================================================
SY, AN = "Synonyms", "Antonyms"
SY_STEM = "Choose the word most similar in meaning to the word in bold as used in the sentence.\n"
AN_STEM = "Choose the word most opposite in meaning to the word in bold as used in the sentence.\n"

Q(SY, "Contextual synonym", "Basic",
  SY_STEM + "The bank took **prompt** action on the customer's complaint and refunded the amount the same day.",
  ["quick", "delayed", "partial", "careless"], "A",
  "Prompt = done without delay",
  "The refund came the same day, so the action was quick. 'Prompt' means quick, without delay.",
  ["Context clue: 'the same day'", "'prompt' = quick"],
  "'Delayed' is the opposite. 'Partial' and 'careless' do not mean quick and are not suggested by a same-day "
  "refund.", 20)

Q(SY, "Contextual synonym", "Intermediate",
  SY_STEM + "The new posting policy is likely to **exacerbate** the shortage of skilled staff in rural branches.",
  ["relieve", "reveal", "ignore", "worsen"], "D",
  "Exacerbate = make a problem worse",
  "To 'exacerbate' a shortage is to make it worse.",
  ["'exacerbate' + a problem (shortage)", "Meaning: make worse", "'worsen'"],
  "'Relieve' is the opposite. 'Reveal' and 'ignore' do not mean making a problem worse.", 25)

Q(SY, "Contextual synonym", "Intermediate",
  SY_STEM + "Despite two failed product launches, the start-up's founders remained **resilient** and kept "
  "working on a third.",
  ["tough", "timid", "rigid", "careless"], "A",
  "Resilient = able to recover quickly from setbacks; tough",
  "They kept working after two failures, which shows the ability to withstand and recover from setbacks: tough.",
  ["Context: despite failures, they kept working", "That shows toughness", "'tough' is closest"],
  "'Timid' (fearful) is nearly the opposite. 'Rigid' means inflexible, unlike resilience. 'Careless' is unrelated.",
  25)

Q(SY, "Contextual synonym", "Advanced",
  SY_STEM + "The minister's **perfunctory** visit to the flood-hit district, lasting barely twenty minutes, drew "
  "sharp criticism.",
  ["thorough", "prolonged", "sympathetic", "cursory"], "D",
  "Perfunctory = done as a routine duty with minimal effort or care",
  "A visit of barely twenty minutes that drew criticism was a hasty formality: perfunctory, i.e. cursory.",
  ["Context: 'barely twenty minutes', 'sharp criticism'", "'perfunctory' = hasty, minimal",
   "'cursory' has the same meaning"],
  "'Thorough' and 'prolonged' are nearly opposite. 'Sympathetic' would not attract criticism.", 30)

Q(AN, "Contextual antonym", "Basic",
  AN_STEM + "The rules for opening a basic savings account are quite **lenient**, so most people can open one "
  "easily.",
  ["mild", "flexible", "strict", "tolerant"], "C",
  "Lenient = not strict, tolerant",
  "'Lenient' rules are easy-going. The opposite is 'strict'.",
  ["'lenient' = permissive, not strict", "Opposite: 'strict'"],
  "'Mild', 'flexible' and 'tolerant' are close to 'lenient' in meaning, not opposite.", 20)

Q(AN, "Contextual antonym", "Intermediate",
  AN_STEM + "The bank's **meagre** profits this year worried its shareholders.",
  ["scanty", "abundant", "modest", "limited"], "B",
  "Meagre = small in quantity, inadequate",
  "'Meagre' means very small or insufficient. The opposite is 'abundant' (plentiful).",
  ["'meagre' = scanty, insufficient", "Opposite: plentiful = 'abundant'"],
  "'Scanty', 'modest' and 'limited' all suggest smallness, close to 'meagre'.", 25)

Q(AN, "Contextual antonym", "Advanced",
  AN_STEM + "His **affable** manner made him popular with the customers who visited the branch.",
  ["cordial", "genial", "surly", "amiable"], "C",
  "Affable = friendly and easy to talk to",
  "'Affable' means friendly and pleasant. 'Surly' means bad-tempered and unfriendly, its opposite.",
  ["'affable' = friendly, pleasant", "Opposite: rude, unfriendly = 'surly'"],
  "'Cordial', 'genial' and 'amiable' are all synonyms of 'affable'.", 25)

# =====================================================================================================================
# IDIOMS AND PHRASES
# =====================================================================================================================
ID = "Idioms and Phrases"

Q(ID, "Meaning of idiom", "Basic",
  "Choose the meaning of the idiom 'a drop in the ocean'.",
  ["a sudden fall in prices", "a serious mistake", "a rare opportunity",
   "a very small amount compared with what is needed"], "D",
  "Idiom: a drop in the ocean",
  "'A drop in the ocean' means an amount so small that it makes almost no difference to what is needed. For "
  "example, 'The relief fund was a drop in the ocean compared with the losses.'",
  ["Picture a single drop compared with an ocean", "Meaning: tiny relative to the need"],
  "'A sudden fall in prices' takes 'drop' literally. 'A serious mistake' and 'a rare opportunity' have no link with "
  "the idiom.", 20)

Q(ID, "Idiom in context", "Intermediate",
  "Choose the meaning of the idiom in bold.\n"
  "With the deadline approaching, the audit team had to **burn the midnight oil** all week.",
  ["waste the bank's resources", "work late into the night", "quarrel among themselves", "give up the task"], "B",
  "Idiom: burn the midnight oil",
  "To 'burn the midnight oil' is to work or study late into the night. The approaching deadline explains why the "
  "team had to do so.",
  ["Idiom origin: working by lamplight at midnight", "Context: a deadline is approaching",
   "Meaning: work late into the night"],
  "'Waste resources' takes 'burn' literally. 'Quarrel' and 'give up' contradict the effort the deadline demands.", 25)

Q(ID, "Meaning of idiom", "Intermediate",
  "Choose the meaning of the idiom 'to bite the bullet'.",
  ["to make oneself do something difficult or unpleasant that cannot be avoided", "to speak rudely to someone",
   "to act without thinking", "to avoid responsibility"], "A",
  "Idiom: bite the bullet",
  "'To bite the bullet' means to force oneself to face or do something unpleasant that is unavoidable. For "
  "example, 'The bank bit the bullet and wrote off the bad loans.'",
  ["The idiom refers to enduring pain bravely", "Meaning: accept an unpleasant necessity"],
  "'Speaking rudely' and 'acting without thinking' are unrelated. 'Avoiding responsibility' is the opposite of "
  "facing it.", 25)

Q(ID, "Idiom in context", "Advanced",
  "Choose the meaning of the idiom in bold.\n"
  "After five years of mounting losses, the board decided to **throw in the towel** on its loss-making insurance "
  "subsidiary.",
  ["invest more money", "clean up the accounts", "hand over control temporarily", "admit defeat and give up"], "D",
  "Idiom: throw in the towel",
  "To 'throw in the towel' is to admit defeat and stop trying. After five years of losses, the board gave up on the "
  "subsidiary.",
  ["Context: five years of losses", "Idiom from boxing: throwing in the towel ends the fight",
   "Meaning: admit defeat and give up"],
  "'Invest more money' is the opposite. 'Clean up the accounts' takes 'towel' literally. 'Hand over control "
  "temporarily' implies continued involvement, not giving up.", 30)

# =====================================================================================================================
# ONE-WORD SUBSTITUTION
# =====================================================================================================================
OW = "One-Word Substitution"
OW_STEM = "Choose the one word that can be substituted for the given group of words.\n"

Q(OW, "Single word for a phrase", "Basic", OW_STEM + "A person or firm that is unable to pay its debts",
  ["solvent", "creditor", "insolvent", "benefactor"], "C",
  "One-word substitution: financial terms",
  "'Insolvent' describes a person or firm unable to pay its debts.",
  ["Meaning: cannot pay debts", "Word: insolvent"],
  "'Solvent' means able to pay debts (the opposite). A 'creditor' is one to whom money is owed. A 'benefactor' gives "
  "help or money.", 20)

Q(OW, "Single word for a phrase", "Intermediate", OW_STEM + "Government by the wealthy",
  ["autocracy", "plutocracy", "bureaucracy", "theocracy"], "B",
  "One-word substitution: forms of government (-cracy = rule)",
  "'Plutocracy' (from Greek 'ploutos', wealth) is government by the wealthy.",
  ["Root 'pluto-' = wealth", "'plutocracy' = rule by the rich"],
  "'Autocracy' is rule by one person, 'bureaucracy' is rule by officials, and 'theocracy' is rule by religious "
  "authority.", 20)

Q(OW, "Single word for a phrase", "Advanced", OW_STEM + "A solution or remedy for all difficulties or diseases",
  ["panacea", "placebo", "antidote", "catalyst"], "A",
  "One-word substitution: remedies",
  "A 'panacea' (from Greek 'pan', all) is a supposed cure for all ills or problems.",
  ["Key words: 'for all'", "Root 'pan-' = all", "'panacea'"],
  "A 'placebo' has no real medical effect. An 'antidote' counters a particular poison. A 'catalyst' speeds up a "
  "change. None is a remedy for all difficulties.", 20)

# =====================================================================================================================
# ACTIVE AND PASSIVE VOICE
# =====================================================================================================================
AP = "Active and Passive Voice"
AP_STEM = "Choose the option that correctly expresses the given sentence in passive voice.\n"

Q(AP, "Voice conversion", "Basic", AP_STEM + "The manager approved the loan application.",
  ["The loan application is approved by the manager.", "The loan application had been approved by the manager.",
   "The loan application was being approved by the manager.", "The loan application was approved by the manager."],
  "D",
  "Simple past active → was/were + past participle",
  "The active verb 'approved' is simple past. In the passive, the object becomes the subject and the verb becomes "
  "'was approved': 'The loan application was approved by the manager.'",
  ["Object 'the loan application' becomes the subject", "Simple past → was + past participle",
   "Agent: 'by the manager'"],
  "A changes the tense to present. B changes it to past perfect. C changes it to past continuous.", 25)

Q(AP, "Voice conversion", "Intermediate", AP_STEM + "Who has signed this cheque?",
  ["By whom has this cheque been signed?", "By whom this cheque has been signed?", "By whom was this cheque signed?",
   "By whom had this cheque been signed?"], "A",
  "Passive of a 'who' question: Who → By whom; present perfect → has been + past participle; keep question order",
  "'Who' becomes 'By whom', the tense stays present perfect ('has been signed'), and the question keeps the "
  "auxiliary before the subject: 'By whom has this cheque been signed?'",
  ["'Who' → 'By whom'", "Present perfect active → 'has been signed'",
   "Question order: auxiliary 'has' before 'this cheque'"],
  "B uses statement order in a question. C changes the tense to simple past. D changes it to past perfect.", 30)

Q(AP, "Voice conversion", "Advanced", AP_STEM + "Someone must have leaked the report before the board meeting.",
  ["The report must be leaked before the board meeting.",
   "The report must had been leaked before the board meeting.",
   "The report must have been leaked before the board meeting.",
   "The report must have leaked by someone before the board meeting."], "C",
  "Modal perfect active (must have + V3) → must have been + V3; an indefinite agent is dropped",
  "'Must have leaked' becomes 'must have been leaked'. The vague agent 'someone' is normally omitted.",
  ["Object 'the report' becomes the subject", "must have + V3 → must have been + V3",
   "Omit 'by someone'"],
  "A changes the meaning to a present or future obligation. B uses 'had' after a modal, which is ungrammatical. D "
  "keeps an active form ('must have leaked') with 'by someone', which is wrong.", 35)

# =====================================================================================================================
# DIRECT AND INDIRECT SPEECH
# =====================================================================================================================
DS = "Direct and Indirect Speech"
DS_STEM = "Choose the option that correctly expresses the given sentence in indirect (reported) speech.\n"

Q(DS, "Narration change", "Basic", DS_STEM + "The manager said to me, \"Submit the form by Monday.\"",
  ["The manager said me to submit the form by Monday.", "The manager told me that submit the form by Monday.",
   "The manager told to me submit the form by Monday.", "The manager told me to submit the form by Monday."], "D",
  "Imperative sentences: said to → told/asked/ordered + object + to-infinitive",
  "A command is reported with 'told' (or 'asked') + object + to-infinitive: 'The manager told me to submit the form "
  "by Monday.'",
  ["The direct speech is an order (imperative)", "'said to me' → 'told me'", "Imperative → 'to submit'"],
  "A: 'said' cannot take a personal object without 'to'. B: 'that' cannot introduce an imperative. C: 'told to me' "
  "is wrong, and the infinitive marker 'to' is missing before 'submit'.", 30)

Q(DS, "Narration change", "Intermediate",
  DS_STEM + "She said, \"I have been waiting for the loan approval since Monday.\"",
  ["She said that she has been waiting for the loan approval since Monday.",
   "She said that she had been waiting for the loan approval since Monday.",
   "She said that I had been waiting for the loan approval since Monday.",
   "She said that she was waiting for the loan approval since Monday."], "B",
  "Backshift with a past reporting verb: present perfect continuous → past perfect continuous; pronoun change",
  "The reporting verb 'said' is past, so 'have been waiting' becomes 'had been waiting', and 'I' becomes 'she'.",
  ["Reporting verb in the past: backshift tenses", "'have been waiting' → 'had been waiting'",
   "'I' → 'she'"],
  "A does not backshift the tense. C does not change the pronoun. D uses past continuous, which does not fit the "
  "duration expressed by 'since Monday'.", 35)

Q(DS, "Narration change", "Advanced", DS_STEM + "The officer said, \"Let us review the documents once again.\"",
  ["The officer told that let us review the documents once again.",
   "The officer suggested to review the documents once again.",
   "The officer suggested that they should review the documents once again.",
   "The officer ordered them to review the documents once again."], "C",
  "'Let us' (proposal) → suggested/proposed that + subject + should + verb",
  "'Let us' expresses a proposal, so the reporting verb is 'suggested' or 'proposed', followed by 'that they "
  "should review'.",
  ["'Let us ...' = a suggestion that includes the speaker", "Reporting verb: suggested/proposed",
   "Structure: suggested that + they + should + base verb"],
  "A keeps 'let us' and uses 'told that' without an object. B: 'suggest' is not followed by a to-infinitive in "
  "standard English. D turns a suggestion into an order and drops the speaker's inclusion.", 40)

# =====================================================================================================================
# SUBJECT-VERB AGREEMENT
# =====================================================================================================================
SV = "Subject-Verb Agreement"
SV_STEM = "Choose the verb form that correctly fills the blank.\n"

Q(SV, "Agreement rules", "Basic",
  SV_STEM + "Every customer and every employee ______ required to follow the new security protocol.",
  ["is", "are", "were", "have"], "A",
  "Two singular subjects joined by 'and', each preceded by 'every' or 'each', take a singular verb",
  "When 'every' (or 'each') precedes nouns joined by 'and', each noun is considered separately, so the verb is "
  "singular: 'is required'.",
  ["Subjects: 'Every customer and every employee'", "'Every' makes each one singular",
   "Singular present verb: 'is'"],
  "'Are' and 'were' are plural. 'Have required' would make customers do the requiring, which changes the meaning, "
  "and it is still plural.", 25)

Q(SV, "Agreement rules", "Intermediate",
  SV_STEM + "A large number of applications ______ been received for the post of probationary officer.",
  ["has", "have", "is", "was"], "B",
  "'A number of' (= many) takes a plural verb; 'The number of' takes a singular verb",
  "'A large number of applications' means many applications, so the verb is plural: 'have been received'.",
  ["'A number of' = many → plural", "'been received' needs 'have' or 'has'", "Plural: 'have'"],
  "'Has' is singular (that would suit 'The number of'). 'Is been' and 'was been' are ungrammatical.", 25)

Q(SV, "Agreement rules", "Advanced",
  SV_STEM + "The committee ______ divided in their opinions about the proposed merger.",
  ["is", "has", "was being", "are"], "D",
  "Collective noun acting as individuals takes a plural verb (signalled by 'their opinions')",
  "The members of the committee hold different opinions, so the collective noun is used in a plural sense. The "
  "plural pronoun 'their' confirms this: 'The committee are divided in their opinions.'",
  ["Is the committee acting as one unit or as individuals? Individuals (divided opinions)",
   "'their' is plural, so the verb must be plural", "'are'"],
  "'Is' and 'has' are singular and clash with 'their'. 'Was being divided' is singular and changes the meaning to "
  "an ongoing action.", 35)

# =====================================================================================================================
# TENSES
# =====================================================================================================================
TE = "Tenses"
TE_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(TE, "Perfect tenses", "Basic", TE_STEM + "When I reached the station, the train ______ already ______.",
  ["has, left", "was, leaving", "had, left", "did, leave"], "C",
  "Past perfect for the earlier of two past actions",
  "Two past actions: the train leaving happened before I reached. The earlier action takes the past perfect: 'had "
  "already left'.",
  ["Later past action: 'I reached' (simple past)", "Earlier past action: the train's departure",
   "Past perfect: 'had left'"],
  "'Has left' is present perfect and does not fit a past narrative. 'Was leaving' does not express completion "
  "before arrival and 'already' does not suit it. 'Did already leave' is not standard.", 25)

Q(TE, "Sequence of tenses", "Intermediate",
  TE_STEM + "The officer told us that the branch ______ on the following day for an audit.",
  ["will remain closed", "would remain closed", "remains closed", "has remained closed"], "B",
  "Sequence of tenses: a past reporting verb takes a past form in the subordinate clause (will → would)",
  "The main verb 'told' is past, so a future idea in the 'that' clause takes 'would': 'would remain closed on the "
  "following day'.",
  ["Main clause verb: 'told' (past)", "Future idea in the reported clause: will → would",
   "'the following day' confirms reported speech"],
  "'Will remain', 'remains' and 'has remained' are present-based forms that break the sequence of tenses after "
  "'told'.", 30)

Q(TE, "Perfect tenses", "Advanced",
  TE_STEM + "By the end of this financial year, the bank ______ more than five hundred new ATMs.",
  ["will have installed", "will install", "would install", "has installed"], "A",
  "Future perfect: an action completed before a point in the future ('by the end of ...')",
  "'By the end of this financial year' marks a future deadline before which the action will be complete, so the "
  "future perfect 'will have installed' is needed.",
  ["Time marker: 'By the end of this financial year' (future point)",
   "Completion before that point → future perfect", "'will have installed'"],
  "'Will install' does not show completion by the deadline. 'Would install' is conditional or past-future. 'Has "
  "installed' is present perfect and cannot refer to a future point.", 30)

# =====================================================================================================================
# ARTICLES
# =====================================================================================================================
AR = "Articles"
AR_STEM = "Choose the option that correctly fills the blank(s).\n"

Q(AR, "Definite and indefinite", "Basic",
  AR_STEM + "She waited for ______ hour before her token number was called.",
  ["a", "an", "the", "no article"], "B",
  "'An' before a vowel sound (silent 'h')",
  "The 'h' in 'hour' is silent, so the word begins with a vowel sound. The indefinite article is 'an': 'an hour'.",
  ["The sentence refers to any one hour: indefinite article", "'hour' starts with a vowel sound",
   "So 'an'"],
  "'A' is used before consonant sounds. 'The' would point to a specific hour already known, which the sentence "
  "does not do. A singular countable noun cannot stand without an article here.", 20)

Q(AR, "Definite and indefinite", "Intermediate",
  AR_STEM + "______ unemployment rate in urban areas fell slightly in the last quarter.",
  ["A", "An", "The", "no article"], "C",
  "'The' with a noun made specific by a following phrase",
  "The phrase 'in urban areas' and the time 'last quarter' identify one particular rate, so the definite article "
  "is needed: 'The unemployment rate in urban areas fell...'.",
  ["The noun is 'rate', a singular countable noun", "It is made specific by 'in urban areas'",
   "Specific → 'The'"],
  "'A' and 'An' would refer to an unspecified rate, which does not fit a specific statistic. A singular countable "
  "noun like 'rate' cannot be used without an article here.", 25)

Q(AR, "Definite and indefinite", "Advanced",
  AR_STEM + "He is ______ European by birth but has lived in India for ______ decade.",
  ["a, a", "an, a", "an, the", "a, the"], "A",
  "Article choice depends on sound, not spelling: 'European' begins with a 'y' sound",
  "'European' is pronounced with an initial 'yoo' (consonant) sound, so it takes 'a'. 'Decade' is any period of "
  "ten years, so it also takes 'a': 'a European ... for a decade'.",
  ["'European' starts with the consonant sound /j/: 'a'",
   "'decade' starts with a consonant sound and is not specific: 'a'", "Option A"],
  "'An European' is a common error caused by the spelling 'Eu'. 'For the decade' would need a specific decade "
  "already mentioned.", 30)

# =====================================================================================================================
# PREPOSITIONS
# =====================================================================================================================
PP = "Prepositions"
PP_STEM = "Choose the option that correctly fills the blank.\n"

Q(PP, "Fixed prepositions", "Basic",
  PP_STEM + "She is very good ______ explaining complex financial products to customers.",
  ["in", "on", "for", "at"], "D",
  "Fixed preposition: 'good at' (skill)",
  "To express skill in an activity, English uses 'good at': 'good at explaining'.",
  ["The sentence describes a skill", "'good at' + noun/gerund expresses skill", "'at'"],
  "'Good in' and 'good on' are not standard for skills. 'Good for' means beneficial to ('good for health').", 20)

Q(PP, "Phrasal verbs", "Intermediate",
  PP_STEM + "The bank has decided to ______ a special drive to recover overdue loans.",
  ["carry away", "carry over", "carry off", "carry out"], "D",
  "Phrasal verb 'carry out' = conduct, perform",
  "A drive is conducted or performed, so the phrasal verb is 'carry out a special drive'.",
  ["Meaning needed: conduct a drive", "'carry out' = conduct, perform"],
  "'Carry away' means to excite or remove. 'Carry over' means to postpone or transfer to a later period. 'Carry off' "
  "means to win or handle something successfully.", 25)

Q(PP, "Fixed prepositions", "Advanced",
  PP_STEM + "The new disclosure guidelines are ______ keeping with the bank's commitment to transparency.",
  ["in", "with", "at", "on"], "A",
  "Fixed phrase: 'in keeping with' = consistent with",
  "The fixed phrase is 'in keeping with', meaning consistent with or appropriate to.",
  ["Recognise the fixed phrase '___ keeping with'", "'in keeping with' = consistent with"],
  "'With keeping with', 'at keeping with' and 'on keeping with' are not English phrases.", 25)

# =====================================================================================================================
# CONNECTORS
# =====================================================================================================================
CN = "Connectors"

Q(CN, "Sentence connectors", "Basic",
  "Choose the connector that best fills the blank.\n"
  "The bank cut the interest rate on its fixed deposits. ______, many customers moved their savings to other "
  "banks.",
  ["Nevertheless", "On the contrary", "As a result", "In contrast"], "C",
  "Connectors of result vs contrast",
  "A lower deposit rate leads customers to move their money elsewhere. The second sentence is a consequence of the "
  "first, so 'As a result' fits.",
  ["Relation between the sentences: cause → effect", "Connector of result: 'As a result'"],
  "'Nevertheless', 'On the contrary' and 'In contrast' signal contrast, but customers leaving after a rate cut is an "
  "expected result, not a contrast.", 25)

Q(CN, "Starters and linkers", "Intermediate",
  "Combine the two sentences into one, starting with 'Despite'.\n"
  "The branch was short-staffed. It cleared all pending applications on time.",
  ["Despite the branch was short-staffed, it cleared all pending applications on time.",
   "Despite being short-staffed, the branch cleared all pending applications on time.",
   "Despite of being short-staffed, the branch cleared all pending applications on time.",
   "Despite being short-staffed, all pending applications were cleared by the branch on time."], "B",
  "'Despite' + noun/gerund (not a clause); the subject of the main clause must be the doer of the gerund",
  "'Despite' is a preposition, so it takes a gerund phrase: 'Despite being short-staffed'. The main clause must "
  "begin with 'the branch', the one that was short-staffed.",
  ["'Despite' + gerund: 'Despite being short-staffed'",
   "The doer of 'being short-staffed' is the branch", "So the main clause starts with 'the branch'"],
  "A puts a full clause after 'despite'. C adds a wrong 'of'. D makes the applications the subject, so they seem "
  "to be short-staffed (dangling modifier).", 40)

Q(CN, "Sentence connectors", "Intermediate",
  "Choose the connector that best fills the blank.\n"
  "The new mobile app is easy to use; ______, it has been criticised for its weak security features.",
  ["therefore", "moreover", "consequently", "however"], "D",
  "Contrast connector after a semicolon",
  "The first clause praises the app; the second criticises it. That is a contrast, so 'however' fits.",
  ["Clause 1: positive (easy to use)", "Clause 2: negative (criticised)", "Contrast → 'however'"],
  "'Therefore' and 'consequently' show result: being easy to use does not cause criticism of security. "
  "'Moreover' adds a point in the same direction.", 30)

Q(CN, "Sentence connectors", "Advanced",
  "Choose the connector that best fills the blank.\n"
  "The regulator relaxed the provisioning norms for stressed loans; ______, banks would have had to set aside far "
  "larger sums and cut their lending.",
  ["otherwise", "whereas", "hence", "likewise"], "A",
  "'Otherwise' = if this had not happened (introduces the alternative outcome)",
  "The second clause ('would have had to') describes what would have happened without the relaxation. 'Otherwise' "
  "introduces exactly this unreal alternative.",
  ["Clause 2 uses 'would have had to': an unreal past outcome",
   "It describes what would have happened if the norms had not been relaxed", "Connector: 'otherwise'"],
  "'Hence' would make larger provisions a result of the relaxation, which is the reverse. 'Whereas' and 'likewise' "
  "do not introduce an alternative outcome and leave the conditional 'would have had' unexplained.", 40)

# =====================================================================================================================
# ASSEMBLY AND CHECKS
# =====================================================================================================================
for i, q in enumerate(QS):
    q["question_id"] = f"BANK_ENG_{FIRST_ID + i:06d}"

plan = json.loads((ROOT / "batches" / "plans" / "BATCH_001_plan.json").read_text(encoding="utf-8"))
eng = next(s for s in plan["subjects"] if s["subject"] == EN)
have = Counter((q["topic"], q["difficulty"]) for q in QS)
for t in eng["topics"]:
    for d, n in t["quota"].items():
        assert have[(t["topic"], d)] == n, (t["topic"], d, have[(t["topic"], d)], n)
    for q in QS:
        if q["topic"] == t["topic"]:
            assert q["subtopic"] in t["subtopics"], (q["topic"], q["subtopic"])
assert len(QS) == eng["total"] == 150
assert QS[-1]["question_id"] == eng["question_ids"][1]
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
    if q["topic"] == ED:
        assert q["options"][3]["text"] == "No error"
    assert len({o["text"] for o in q["options"]}) == 4, q["question_id"]

keys = Counter(q["correct_answer"] for q in QS)
assert max(keys.values()) <= 0.28 * len(QS) and min(keys.values()) >= 0.22 * len(QS), keys

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_001",
    "created_at": TODAY,
    "notes": "BATCH_001 English Language part: 150 original questions (BANK_ENG_000004 to BANK_ENG_000153). Six "
             "reading passages (30 questions) and four cloze passages (19 blanks), all written for PrepMitra; the "
             "rest are standalone grammar, vocabulary and sentence-ordering items. Each answer was set by the author "
             "and re-solved in a separate pass without the key. Pending human review.",
    "stimuli": STIMULI,
    "questions": QS,
}
out = ROOT / "batches" / "parts" / "BATCH_001_ENG.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(QS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(keys.items()))})")
