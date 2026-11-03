import { liveCatalog } from '../api/live';
import type { Question, QuestionOption, QuestionTranslation } from '../types/core';

const opts = (id: string, texts: string[]): QuestionOption[] =>
  texts.map((text, i) => ({ id: `${id}-${String.fromCharCode(97 + i)}`, text }));

/** Builds an option-based question; `correct` uses option letters (a, b, c, d). */
function mcq(
  q: Omit<Question, 'options' | 'correctOptionIds'> & { options: string[]; correct: string[] },
): Question {
  const { options, correct, ...rest } = q;
  return { ...rest, options: opts(q.id, options), correctOptionIds: correct.map((c) => `${q.id}-${c}`) };
}

/**
 * Demo question bank. In production questions are AI-generated, verified by a
 * second model plus code checks, and stored per language (MVP doc §6.1).
 */
const BASE_BANK: Question[] = [
  // ---------------- Quantitative aptitude ----------------
  mcq({
    id: 'q-quant-1', subject: 'quant', topic: 'Compound Interest', type: 'single', difficulty: 'Moderate',
    text: 'A sum of money becomes ₹1,331 in 3 years at 10% per annum compound interest. What is the principal?',
    options: ['₹900', '₹1,000', '₹1,100', '₹1,210'], correct: ['b'],
    explanation: 'Amount = P(1.1)³ = 1.331P. So 1.331P = 1331, giving P = ₹1,000.',
    shortcut: 'Recognise 1331 = 11³. With r = 10%, the multiplier is (11/10)³, so P = 10³ = 1000.',
    expectedTimeSec: 45,
    translations: {
      hi: {
        text: 'कोई धनराशि 10% वार्षिक चक्रवृद्धि ब्याज पर 3 वर्ष में ₹1,331 हो जाती है। मूलधन क्या है?',
        options: ['₹900', '₹1,000', '₹1,100', '₹1,210'],
      },
    },
  }),
  mcq({
    id: 'q-quant-2', subject: 'quant', topic: 'Profit and Loss', type: 'single', difficulty: 'Easy',
    text: 'If the cost price of 12 pens equals the selling price of 10 pens, what is the profit percentage?',
    options: ['16.67%', '20%', '18%', '25%'], correct: ['b'],
    explanation: 'Let CP of 1 pen = ₹1. CP of 12 = ₹12 = SP of 10, so SP of 1 = ₹1.2. Profit = 20%.',
    shortcut: 'Profit % = (difference ÷ goods sold) × 100 = (12 − 10) ÷ 10 × 100 = 20%.',
    expectedTimeSec: 30,
    translations: {
      hi: { text: 'यदि 12 पेनों का क्रय मूल्य 10 पेनों के विक्रय मूल्य के बराबर है, तो लाभ प्रतिशत क्या है?', options: ['16.67%', '20%', '18%', '25%'] },
    },
  }),
  mcq({
    id: 'q-quant-3', subject: 'quant', topic: 'Time Speed Distance', type: 'single', difficulty: 'Easy',
    text: 'A train 240 m long passes a pole in 12 seconds. What is its speed in km/h?',
    options: ['60', '72', '80', '84'], correct: ['b'],
    explanation: 'Speed = 240 ÷ 12 = 20 m/s. Convert: 20 × 18/5 = 72 km/h.',
    shortcut: 'Multiply m/s by 3.6 to get km/h: 20 × 3.6 = 72.',
    expectedTimeSec: 30,
  }),
  mcq({
    id: 'q-quant-4', subject: 'quant', topic: 'Percentages', type: 'single', difficulty: 'Easy',
    text: 'What is 35% of 640?',
    options: ['214', '224', '234', '244'], correct: ['b'],
    explanation: '10% of 640 = 64, so 30% = 192 and 5% = 32. Total = 224.',
    shortcut: 'Split 35% into 25% + 10%: 160 + 64 = 224.',
    expectedTimeSec: 20,
  }),
  mcq({
    id: 'q-quant-5', subject: 'quant', topic: 'Time and Work', type: 'single', difficulty: 'Moderate',
    text: 'A can finish a job in 12 days and B in 18 days. Working together, in how many days will they finish it?',
    options: ['6.6 days', '7.2 days', '7.5 days', '8 days'], correct: ['b'],
    explanation: 'Combined rate = 1/12 + 1/18 = 5/36 per day. Time = 36/5 = 7.2 days.',
    shortcut: 'Use product ÷ sum: (12 × 18) ÷ (12 + 18) = 216 ÷ 30 = 7.2 days.',
    expectedTimeSec: 40,
  }),
  mcq({
    id: 'q-quant-6', subject: 'quant', topic: 'Averages', type: 'single', difficulty: 'Moderate',
    text: 'The average of 5 numbers is 28. If one number is excluded, the average becomes 25. What is the excluded number?',
    options: ['36', '38', '40', '42'], correct: ['c'],
    explanation: 'Sum of 5 = 140. Sum of 4 = 100. Excluded number = 140 − 100 = 40.',
    shortcut: 'Excluded = new avg + (count × change) = 25 + 5 × 3 = 40.',
    expectedTimeSec: 35,
  }),
  {
    id: 'q-quant-7', subject: 'quant', topic: 'Ratio and Proportion', type: 'numeric', difficulty: 'Moderate',
    text: '₹7,200 is divided among A, B and C in the ratio 2 : 3 : 4. How much (in ₹) does C receive? Enter a number.',
    correctNumeric: 3200, tolerance: 0,
    explanation: 'Total parts = 9. One part = 7200 ÷ 9 = 800. C gets 4 × 800 = ₹3,200.',
    shortcut: 'C’s share = 4/9 of 7200; 7200 ÷ 9 = 800 is a clean division, so multiply by 4.',
    expectedTimeSec: 40,
  },
  mcq({
    id: 'q-quant-8', subject: 'quant', topic: 'Number System', type: 'multiple', difficulty: 'Moderate',
    text: 'Which of the following numbers are divisible by both 3 and 4? (Select all that apply)',
    options: ['132', '246', '312', '458'], correct: ['a', 'c'],
    explanation: 'Divisible by 12 means divisible by 3 (digit sum) and 4 (last two digits). 132: sum 6, 32 ÷ 4 ✓. 312: sum 6, 12 ÷ 4 ✓. 246: 46 not divisible by 4. 458: sum 17 ✗.',
    shortcut: 'Check the last two digits for 4 first — it eliminates options fastest.',
    expectedTimeSec: 45,
  }),

  // ---------------- Reasoning ----------------
  mcq({
    id: 'q-reas-1', subject: 'reasoning', topic: 'Number Series', type: 'single', difficulty: 'Easy',
    text: 'Find the next number in the series: 2, 6, 12, 20, 30, ?',
    options: ['40', '42', '44', '36'], correct: ['b'],
    explanation: 'Differences are 4, 6, 8, 10, so the next difference is 12: 30 + 12 = 42.',
    shortcut: 'Terms are n(n+1): 1×2, 2×3, 3×4… so the 6th term is 6×7 = 42.',
    expectedTimeSec: 25,
    translations: { hi: { text: 'श्रृंखला में अगली संख्या ज्ञात कीजिए: 2, 6, 12, 20, 30, ?', options: ['40', '42', '44', '36'] } },
  }),
  mcq({
    id: 'q-reas-2', subject: 'reasoning', topic: 'Coding-Decoding', type: 'single', difficulty: 'Moderate',
    text: 'If CAT is coded as 3120 and DOG is coded as 4157, how is BAT coded?',
    options: ['2120', '2210', '3120', '2130'], correct: ['a'],
    explanation: 'Each letter is replaced by its alphabet position: C=3, A=1, T=20. So B=2, A=1, T=20 → 2120.',
    shortcut: 'BAT differs from CAT only in the first letter (C→B), so change 3 to 2.',
    expectedTimeSec: 30,
  }),
  mcq({
    id: 'q-reas-3', subject: 'reasoning', topic: 'Blood Relations', type: 'single', difficulty: 'Moderate',
    text: 'Pointing to a man, Riya says, “He is the son of my grandfather’s only son.” How is the man related to Riya?',
    options: ['Cousin', 'Brother', 'Uncle', 'Father'], correct: ['b'],
    explanation: 'Her grandfather’s only son is her father. The father’s son is her brother.',
    shortcut: '“Only son” of grandfather (paternal) collapses to “father” — resolve from the far end.',
    expectedTimeSec: 30,
  }),
  mcq({
    id: 'q-reas-4', subject: 'reasoning', topic: 'Direction Sense', type: 'single', difficulty: 'Easy',
    text: 'Aman walks 5 km north, turns right and walks 3 km, then turns right again and walks 5 km. How far is he from the start?',
    options: ['3 km', '5 km', '8 km', '13 km'], correct: ['a'],
    explanation: 'North 5, east 3, south 5. He ends 3 km east of the starting point.',
    shortcut: 'Equal north and south legs cancel; only the 3 km east leg remains.',
    expectedTimeSec: 25,
  }),
  mcq({
    id: 'q-reas-5', subject: 'reasoning', topic: 'Syllogism', type: 'single', difficulty: 'Moderate',
    text: 'Statements: All pens are books. Some books are bags. Conclusions: I. Some pens are bags. II. Some bags are books.',
    options: ['Only I follows', 'Only II follows', 'Both follow', 'Neither follows'], correct: ['b'],
    explanation: '“Some books are bags” converts to “Some bags are books” (II follows). Pens and bags have no definite link, so I does not follow.',
    shortcut: 'A “some” statement always converts; a link through a “some” middle term never gives a definite conclusion.',
    expectedTimeSec: 40,
  }),
  mcq({
    id: 'q-reas-6', subject: 'reasoning', topic: 'Analogy', type: 'single', difficulty: 'Easy',
    text: 'Doctor : Hospital :: Teacher : ?',
    options: ['Student', 'School', 'Book', 'Classroom board'], correct: ['b'],
    explanation: 'A doctor works in a hospital; a teacher works in a school.',
    shortcut: 'Name the relationship in words (“works in”) before scanning options.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-reas-7', subject: 'reasoning', topic: 'Seating Arrangement', type: 'single', difficulty: 'Hard',
    text: 'Five friends P, Q, R, S and T sit in a row facing north. R is in the middle. P is at the left end. T is to the immediate right of R. Q is not next to P. Who sits second from the left?',
    options: ['Q', 'S', 'T', 'R'], correct: ['b'],
    explanation: 'Positions 1–5: P at 1, R at 3, T at 4. Q and S fill 2 and 5; Q cannot be next to P, so Q is at 5 and S at 2.',
    shortcut: 'Place fixed people first (ends and middle), then apply the negative clue last.',
    expectedTimeSec: 60,
  }),
  mcq({
    id: 'q-reas-8', subject: 'reasoning', topic: 'Odd One Out', type: 'multiple', difficulty: 'Moderate',
    text: 'Which of the following numbers are prime? (Select all that apply)',
    options: ['51', '53', '57', '59'], correct: ['b', 'd'],
    explanation: '51 = 3 × 17 and 57 = 3 × 19 are composite. 53 and 59 are prime.',
    shortcut: 'Check digit sums: 5+1 = 6 and 5+7 = 12 are divisible by 3, so 51 and 57 fall away instantly.',
    expectedTimeSec: 35,
  }),

  // ---------------- English ----------------
  mcq({
    id: 'q-eng-1', subject: 'english', topic: 'Antonyms', type: 'single', difficulty: 'Easy',
    text: 'Choose the word most nearly OPPOSITE in meaning to “SCARCE”.',
    options: ['Rare', 'Abundant', 'Limited', 'Meagre'], correct: ['b'],
    explanation: 'Scarce means insufficient; abundant means plentiful.',
    shortcut: 'Eliminate synonyms first — rare, limited and meagre all mean “not enough”.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-eng-2', subject: 'english', topic: 'Error Spotting', type: 'single', difficulty: 'Moderate',
    text: 'Identify the part with an error: “Neither the manager (A) / nor his assistants (B) / was present (C) / at the meeting. (D)”',
    options: ['A', 'B', 'C', 'D'], correct: ['c'],
    explanation: 'With “neither…nor”, the verb agrees with the nearer subject. “Assistants” is plural, so it should be “were present”.',
    shortcut: 'For either/neither…or/nor, look only at the subject closest to the verb.',
    expectedTimeSec: 35,
  }),
  mcq({
    id: 'q-eng-3', subject: 'english', topic: 'Fill in the Blanks', type: 'single', difficulty: 'Easy',
    text: 'The committee will ______ its decision after reviewing all the applications.',
    options: ['announce', 'announcing', 'announced', 'announces'], correct: ['a'],
    explanation: 'After the modal “will”, the base form of the verb is used: “will announce”.',
    shortcut: 'Modal verbs (will, can, should) are always followed by the base form.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-eng-4', subject: 'english', topic: 'Idioms and Phrases', type: 'single', difficulty: 'Moderate',
    text: 'Choose the meaning of the idiom “to burn the midnight oil”.',
    options: ['To waste resources', 'To work late into the night', 'To start a conflict', 'To celebrate late'], correct: ['b'],
    explanation: 'The idiom means to study or work late at night.',
    shortcut: 'Picture the literal image (an oil lamp lit at midnight) to recall the meaning.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-eng-5', subject: 'english', topic: 'Synonyms', type: 'single', difficulty: 'Moderate',
    text: 'Choose the word closest in meaning to “METICULOUS”.',
    options: ['Careless', 'Thorough', 'Hasty', 'Generous'], correct: ['b'],
    explanation: 'Meticulous means showing great attention to detail — thorough.',
    shortcut: 'Careless and hasty are antonyms; remove them and choose between the remaining two.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-eng-6', subject: 'english', topic: 'Reading Comprehension', type: 'single', difficulty: 'Hard',
    text: 'Passage: “Digital payments in India grew rapidly after 2016, but trust remains uneven: first-time users often abandon a transaction after a single failure.” Which inference is best supported?',
    options: [
      'Digital payments declined after 2016',
      'Reliability affects whether new users keep using digital payments',
      'All users distrust digital payments',
      'Failures happen only to first-time users',
    ],
    correct: ['b'],
    explanation: 'The passage links a single failure with abandonment among first-time users, so reliability influences adoption. Other options overgeneralise or contradict the text.',
    shortcut: 'Reject options with absolute words (“all”, “only”) unless the passage uses them.',
    expectedTimeSec: 60,
  }),
  mcq({
    id: 'q-eng-7', subject: 'english', topic: 'Sentence Improvement', type: 'single', difficulty: 'Moderate',
    text: 'Improve the phrase in brackets: “He is senior [than me] by two years.”',
    options: ['to me', 'from me', 'over me', 'No improvement'], correct: ['a'],
    explanation: 'Latin comparatives such as senior, junior, superior and prior take “to”, not “than”.',
    shortcut: 'Memorise the “-ior + to” rule: senior to, junior to, superior to.',
    expectedTimeSec: 20,
  }),

  // ---------------- General awareness ----------------
  mcq({
    id: 'q-ga-1', subject: 'general-awareness', topic: 'Indian Polity', type: 'single', difficulty: 'Easy',
    text: 'Who is known as the principal architect of the Indian Constitution?',
    options: ['Jawaharlal Nehru', 'B. R. Ambedkar', 'Rajendra Prasad', 'Sardar Patel'], correct: ['b'],
    explanation: 'Dr. B. R. Ambedkar chaired the Drafting Committee of the Constituent Assembly.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-ga-2', subject: 'general-awareness', topic: 'Geography', type: 'single', difficulty: 'Moderate',
    text: 'Which river is known as the “Dakshin Ganga” (Ganga of the South)?',
    options: ['Krishna', 'Kaveri', 'Godavari', 'Narmada'], correct: ['c'],
    explanation: 'The Godavari is the longest river in peninsular India and is called the Dakshin Ganga.',
    shortcut: 'Longest peninsular river ↔ largest comparison (Ganga) — Godavari.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-ga-3', subject: 'general-awareness', topic: 'Economy', type: 'single', difficulty: 'Moderate',
    text: 'The repo rate in India is set by which body?',
    options: ['Ministry of Finance', 'SEBI', 'Monetary Policy Committee of the RBI', 'NITI Aayog'], correct: ['c'],
    explanation: 'The six-member Monetary Policy Committee of the Reserve Bank of India decides the policy repo rate.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-ga-4', subject: 'general-awareness', topic: 'Science', type: 'single', difficulty: 'Easy',
    text: 'Which vitamin is produced in the human skin on exposure to sunlight?',
    options: ['Vitamin A', 'Vitamin B12', 'Vitamin C', 'Vitamin D'], correct: ['d'],
    explanation: 'UVB rays help the skin synthesise Vitamin D from cholesterol derivatives.',
    expectedTimeSec: 10,
  }),
  mcq({
    id: 'q-ga-5', subject: 'general-awareness', topic: 'History', type: 'single', difficulty: 'Moderate',
    text: 'The Dandi March of 1930 was launched to protest against which tax?',
    options: ['Land revenue', 'Salt tax', 'Income tax', 'Cotton duty'], correct: ['b'],
    explanation: 'Gandhi led the Salt March from Sabarmati to Dandi to break the British salt law.',
    expectedTimeSec: 10,
  }),
  mcq({
    id: 'q-ga-6', subject: 'general-awareness', topic: 'Railways', type: 'single', difficulty: 'Moderate',
    text: 'Which Indian state has the longest railway route length?',
    options: ['Maharashtra', 'Uttar Pradesh', 'Rajasthan', 'Gujarat'], correct: ['b'],
    explanation: 'Uttar Pradesh has the largest railway network by route length among Indian states.',
    expectedTimeSec: 15,
  }),

  // ---------------- General studies (UPSC) ----------------
  mcq({
    id: 'q-gs-1', subject: 'general-studies', topic: 'Indian Polity', type: 'single', difficulty: 'Moderate',
    text: 'Which Article of the Indian Constitution deals with the Right to Constitutional Remedies?',
    options: ['Article 19', 'Article 21', 'Article 32', 'Article 44'], correct: ['c'],
    explanation: 'Article 32 allows citizens to move the Supreme Court for enforcement of Fundamental Rights; Ambedkar called it the “heart and soul” of the Constitution.',
    shortcut: 'Remember 32 with “writs” — the five writs flow from Articles 32 and 226.',
    expectedTimeSec: 30,
  }),
  mcq({
    id: 'q-gs-2', subject: 'general-studies', topic: 'Environment', type: 'single', difficulty: 'Hard',
    text: 'Consider the statements: 1. Wetlands act as carbon sinks. 2. The Ramsar Convention is a treaty for the conservation of wetlands. Which is/are correct?',
    options: ['1 only', '2 only', 'Both 1 and 2', 'Neither 1 nor 2'], correct: ['c'],
    explanation: 'Wetlands such as peatlands store large amounts of carbon, and the Ramsar Convention (1971) is the treaty on wetland conservation.',
    shortcut: 'If you are sure of one statement, eliminate the two options that contradict it before deciding the other.',
    expectedTimeSec: 45,
  }),
  mcq({
    id: 'q-gs-3', subject: 'general-studies', topic: 'Modern History', type: 'single', difficulty: 'Moderate',
    text: 'The Indian National Congress session at which the “Purna Swaraj” resolution was adopted was held at:',
    options: ['Calcutta', 'Lahore', 'Karachi', 'Lucknow'], correct: ['b'],
    explanation: 'The Lahore session of December 1929, presided over by Jawaharlal Nehru, adopted Purna Swaraj.',
    expectedTimeSec: 25,
  }),
  mcq({
    id: 'q-gs-4', subject: 'general-studies', topic: 'Economy', type: 'single', difficulty: 'Hard',
    text: 'An increase in the Cash Reserve Ratio (CRR) by the central bank will most likely:',
    options: ['Increase money supply', 'Reduce the lending capacity of banks', 'Lower inflation expectations immediately to zero', 'Increase government borrowing'], correct: ['b'],
    explanation: 'A higher CRR means banks must park more deposits with the RBI, leaving less money available to lend.',
    shortcut: 'Any rise in a reserve requirement → less money with banks → tighter liquidity.',
    expectedTimeSec: 35,
  }),
  mcq({
    id: 'q-gs-5', subject: 'general-studies', topic: 'Geography', type: 'single', difficulty: 'Moderate',
    text: 'Which of the following is a cold ocean current?',
    options: ['Gulf Stream', 'Kuroshio Current', 'Labrador Current', 'Brazil Current'], correct: ['c'],
    explanation: 'The Labrador Current flows south from the Arctic along Canada’s coast and is cold. The others are warm currents.',
    expectedTimeSec: 25,
  }),
  mcq({
    id: 'q-gs-6', subject: 'general-studies', topic: 'Science & Technology', type: 'single', difficulty: 'Moderate',
    text: 'CRISPR-Cas9 technology is primarily associated with:',
    options: ['Quantum computing', 'Gene editing', 'Satellite navigation', 'Battery storage'], correct: ['b'],
    explanation: 'CRISPR-Cas9 is a genome editing tool that cuts DNA at targeted locations.',
    expectedTimeSec: 15,
  }),

  // ---------------- Computer science ----------------
  mcq({
    id: 'q-cs-1', subject: 'computer-science', topic: 'Data Structures', type: 'single', difficulty: 'Easy',
    text: 'What is the worst-case time complexity of searching in a balanced binary search tree with n nodes?',
    options: ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'], correct: ['b'],
    explanation: 'A balanced BST has height O(log n), and search follows one root-to-leaf path.',
    expectedTimeSec: 20,
  }),
  mcq({
    id: 'q-cs-2', subject: 'computer-science', topic: 'Operating Systems', type: 'multiple', difficulty: 'Moderate',
    text: 'Which of the following are necessary conditions for deadlock? (Select all that apply)',
    options: ['Mutual exclusion', 'Preemption', 'Hold and wait', 'Circular wait'], correct: ['a', 'c', 'd'],
    explanation: 'Coffman conditions: mutual exclusion, hold and wait, no preemption and circular wait. Preemption itself prevents deadlock.',
    shortcut: 'Remember “MHNC” — Mutual exclusion, Hold & wait, No preemption, Circular wait.',
    expectedTimeSec: 45,
  }),
  {
    id: 'q-cs-3', subject: 'computer-science', topic: 'Algorithms', type: 'numeric', difficulty: 'Moderate',
    text: 'How many comparisons does binary search make in the worst case on a sorted array of 1,024 elements? Enter an integer.',
    correctNumeric: 11, tolerance: 0,
    explanation: 'Worst case is ⌊log₂ n⌋ + 1 = 10 + 1 = 11 comparisons for n = 1024.',
    shortcut: '1024 = 2¹⁰, so the answer is 10 + 1.',
    expectedTimeSec: 40,
  },
  mcq({
    id: 'q-cs-4', subject: 'computer-science', topic: 'DBMS', type: 'single', difficulty: 'Moderate',
    text: 'A relation is in BCNF if, for every non-trivial functional dependency X → Y:',
    options: ['Y is a prime attribute', 'X is a super key', 'X is a foreign key', 'Y is part of a candidate key'], correct: ['b'],
    explanation: 'BCNF requires the determinant X of every non-trivial FD to be a super key.',
    expectedTimeSec: 30,
  }),
  mcq({
    id: 'q-cs-5', subject: 'computer-science', topic: 'Computer Networks', type: 'single', difficulty: 'Easy',
    text: 'Which layer of the OSI model is responsible for routing packets between networks?',
    options: ['Data link', 'Network', 'Transport', 'Session'], correct: ['b'],
    explanation: 'The network layer (Layer 3) handles logical addressing and routing, e.g. IP.',
    expectedTimeSec: 15,
  }),
  mcq({
    id: 'q-cs-6', subject: 'computer-science', topic: 'Programming Logic', type: 'single', difficulty: 'Easy',
    text: 'How many times does the loop body run? for (i = 1; i <= 20; i = i * 2)',
    options: ['4', '5', '10', '20'], correct: ['b'],
    explanation: 'i takes the values 1, 2, 4, 8, 16 — five iterations. The next value, 32, exceeds 20.',
    shortcut: 'Count powers of two up to the limit: 2⁰ to 2⁴ → 5.',
    expectedTimeSec: 20,
  }),
  mcq({
    id: 'q-cs-7', subject: 'computer-science', topic: 'Theory of Computation', type: 'single', difficulty: 'Hard',
    text: 'Which of the following languages is NOT regular?',
    options: ['Strings over {a,b} with an even number of a’s', 'aⁿbⁿ for n ≥ 0', 'Strings ending in “ab”', 'All strings over {a,b}'], correct: ['b'],
    explanation: 'aⁿbⁿ requires counting an unbounded number of a’s, which a finite automaton cannot do (pumping lemma).',
    shortcut: 'If recognising the language needs unbounded counting/matching, it is not regular.',
    expectedTimeSec: 40,
  }),

  // ---------------- Electronics ----------------
  mcq({
    id: 'q-ece-1', subject: 'electronics', topic: 'Signals and Systems', type: 'single', difficulty: 'Easy',
    text: 'The Nyquist sampling rate for a signal band-limited to 4 kHz is:',
    options: ['4 kHz', '8 kHz', '2 kHz', '16 kHz'], correct: ['b'],
    explanation: 'Nyquist rate = 2 × maximum frequency = 8 kHz.',
    expectedTimeSec: 15,
  }),
  {
    id: 'q-ece-2', subject: 'electronics', topic: 'Network Theory', type: 'numeric', difficulty: 'Moderate',
    text: 'Two resistors of 6 Ω and 3 Ω are connected in parallel. What is the equivalent resistance in ohms?',
    correctNumeric: 2, tolerance: 0.01,
    explanation: 'R = (6 × 3) ÷ (6 + 3) = 18 ÷ 9 = 2 Ω.',
    shortcut: 'Product over sum for two parallel resistors.',
    expectedTimeSec: 25,
  },
  mcq({
    id: 'q-ece-3', subject: 'electronics', topic: 'Digital Electronics', type: 'multiple', difficulty: 'Moderate',
    text: 'Which of the following gates are universal gates? (Select all that apply)',
    options: ['AND', 'NAND', 'NOR', 'XOR'], correct: ['b', 'c'],
    explanation: 'NAND and NOR can each implement any Boolean function on their own.',
    expectedTimeSec: 20,
  }),
  mcq({
    id: 'q-ece-4', subject: 'electronics', topic: 'Analog Circuits', type: 'single', difficulty: 'Moderate',
    text: 'An ideal operational amplifier has:',
    options: ['Zero input impedance', 'Infinite open-loop gain', 'Infinite output impedance', 'Limited bandwidth'], correct: ['b'],
    explanation: 'Ideal op-amps have infinite open-loop gain, infinite input impedance and zero output impedance.',
    expectedTimeSec: 20,
  }),
  mcq({
    id: 'q-ece-5', subject: 'electronics', topic: 'Communication', type: 'single', difficulty: 'Hard',
    text: 'In AM, if the modulation index is 1 and carrier power is 100 W, the total transmitted power is:',
    options: ['100 W', '125 W', '150 W', '200 W'], correct: ['c'],
    explanation: 'Pt = Pc(1 + m²/2) = 100 × 1.5 = 150 W.',
    shortcut: 'For m = 1, sidebands add exactly 50% of the carrier power.',
    expectedTimeSec: 35,
  }),

  // ---------------- Data interpretation / DILR ----------------
  mcq({
    id: 'q-di-1', subject: 'data-interpretation', topic: 'Data Interpretation', type: 'single', difficulty: 'Moderate',
    text: 'A company’s revenue was ₹200 crore in 2023 and ₹250 crore in 2024. What is the percentage growth?',
    options: ['20%', '25%', '30%', '50%'], correct: ['b'],
    explanation: 'Growth = (250 − 200) ÷ 200 × 100 = 25%.',
    shortcut: '50 on a base of 200 is one quarter → 25%.',
    expectedTimeSec: 20,
  }),
  {
    id: 'q-di-2', subject: 'data-interpretation', topic: 'Data Interpretation', type: 'numeric', difficulty: 'Moderate',
    text: 'In a class of 60 students, 40% play cricket, 25% play football and 10% play both. How many students play neither? Enter a number.',
    correctNumeric: 27, tolerance: 0,
    explanation: 'Play at least one = 40% + 25% − 10% = 55% = 33 students. Neither = 60 − 33 = 27.',
    shortcut: 'Work in percentages until the last step: 100 − 55 = 45% of 60 = 27.',
    expectedTimeSec: 45,
  },
  mcq({
    id: 'q-di-3', subject: 'data-interpretation', topic: 'Logical Reasoning', type: 'single', difficulty: 'Hard',
    text: 'Four teams play each other once in a league. A win gives 2 points, a draw 1 and a loss 0. What is the maximum total points that can be scored by all teams together?',
    options: ['6', '8', '12', '16'], correct: ['c'],
    explanation: 'There are C(4,2) = 6 matches and every match distributes exactly 2 points, so the total is always 12.',
    shortcut: 'With 2-1-0 scoring, total points = 2 × number of matches regardless of results.',
    expectedTimeSec: 45,
  }),
  mcq({
    id: 'q-di-4', subject: 'data-interpretation', topic: 'Data Interpretation', type: 'single', difficulty: 'Moderate',
    text: 'Sales (in units) for Q1–Q4 were 120, 150, 180 and 150. What is the average quarterly sales figure?',
    options: ['145', '150', '155', '160'], correct: ['b'],
    explanation: 'Total = 600 units across 4 quarters → average 150.',
    shortcut: 'Assume 150 as the mean; deviations −30, 0, +30, 0 sum to zero.',
    expectedTimeSec: 20,
  }),
  {
    id: 'q-di-5', subject: 'data-interpretation', topic: 'Logical Reasoning', type: 'numeric', difficulty: 'Hard',
    text: 'In how many ways can 3 different books be arranged on a shelf from a set of 5 different books? Enter a number.',
    correctNumeric: 60, tolerance: 0,
    explanation: 'Permutations ⁵P₃ = 5 × 4 × 3 = 60.',
    shortcut: 'Arrangement = order matters → multiply the top three descending numbers.',
    expectedTimeSec: 30,
  },
];

/**
 * Hindi versions of the bilingual questions. As in real CBT exams, the English
 * language section stays English-only. Options are in the same order as English.
 */
const HI: Record<string, QuestionTranslation> = {
  'q-quant-1': { text: 'कोई धनराशि 10% वार्षिक चक्रवृद्धि ब्याज पर 3 वर्ष में ₹1,331 हो जाती है। मूलधन क्या है?', options: ['₹900', '₹1,000', '₹1,100', '₹1,210'] },
  'q-quant-2': { text: 'यदि 12 पेनों का क्रय मूल्य 10 पेनों के विक्रय मूल्य के बराबर है, तो लाभ प्रतिशत क्या है?', options: ['16.67%', '20%', '18%', '25%'] },
  'q-quant-3': { text: '240 मीटर लंबी एक ट्रेन एक खंभे को 12 सेकंड में पार करती है। ट्रेन की चाल किमी/घंटा में क्या है?', options: ['60', '72', '80', '84'] },
  'q-quant-4': { text: '640 का 35% कितना है?', options: ['214', '224', '234', '244'] },
  'q-quant-5': { text: 'A किसी काम को 12 दिनों में और B उसी काम को 18 दिनों में पूरा कर सकता है। दोनों मिलकर काम कितने दिनों में पूरा करेंगे?', options: ['6.6 दिन', '7.2 दिन', '7.5 दिन', '8 दिन'] },
  'q-quant-6': { text: '5 संख्याओं का औसत 28 है। यदि एक संख्या हटा दी जाए, तो औसत 25 हो जाता है। हटाई गई संख्या क्या है?', options: ['36', '38', '40', '42'] },
  'q-quant-7': { text: '₹7,200 को A, B और C में 2 : 3 : 4 के अनुपात में बाँटा जाता है। C को कितने रुपये (₹) मिलते हैं? एक संख्या दर्ज करें।' },
  'q-quant-8': { text: 'निम्नलिखित में से कौन-सी संख्याएँ 3 और 4 दोनों से विभाज्य हैं? (सभी सही विकल्प चुनें)', options: ['132', '246', '312', '458'] },
  'q-reas-1': { text: 'श्रृंखला में अगली संख्या ज्ञात कीजिए: 2, 6, 12, 20, 30, ?', options: ['40', '42', '44', '36'] },
  'q-reas-2': { text: 'यदि CAT को 3120 और DOG को 4157 के रूप में कोडित किया जाता है, तो BAT को कैसे कोडित किया जाएगा?', options: ['2120', '2210', '3120', '2130'] },
  'q-reas-3': { text: 'एक व्यक्ति की ओर इशारा करते हुए रिया कहती है, “यह मेरे दादाजी के इकलौते बेटे का बेटा है।” वह व्यक्ति रिया से कैसे संबंधित है?', options: ['चचेरा भाई', 'भाई', 'चाचा', 'पिता'] },
  'q-reas-4': { text: 'अमन 5 किमी उत्तर की ओर चलता है, दाएँ मुड़कर 3 किमी चलता है, फिर दोबारा दाएँ मुड़कर 5 किमी चलता है। वह आरंभिक बिंदु से कितनी दूर है?', options: ['3 किमी', '5 किमी', '8 किमी', '13 किमी'] },
  'q-reas-5': { text: 'कथन: सभी पेन किताबें हैं। कुछ किताबें बैग हैं। निष्कर्ष: I. कुछ पेन बैग हैं। II. कुछ बैग किताबें हैं।', options: ['केवल I अनुसरण करता है', 'केवल II अनुसरण करता है', 'दोनों अनुसरण करते हैं', 'कोई भी अनुसरण नहीं करता'] },
  'q-reas-6': { text: 'डॉक्टर : अस्पताल :: शिक्षक : ?', options: ['छात्र', 'विद्यालय', 'पुस्तक', 'कक्षा का बोर्ड'] },
  'q-reas-7': { text: 'पाँच मित्र P, Q, R, S और T उत्तर की ओर मुख करके एक पंक्ति में बैठे हैं। R बीच में है। P बाएँ छोर पर है। T, R के ठीक दाएँ है। Q, P के बगल में नहीं है। बाएँ से दूसरे स्थान पर कौन बैठा है?', options: ['Q', 'S', 'T', 'R'] },
  'q-reas-8': { text: 'निम्नलिखित में से कौन-सी संख्याएँ अभाज्य (prime) हैं? (सभी सही विकल्प चुनें)', options: ['51', '53', '57', '59'] },
  'q-ga-1': { text: 'भारतीय संविधान के मुख्य वास्तुकार के रूप में किसे जाना जाता है?', options: ['जवाहरलाल नेहरू', 'बी. आर. आंबेडकर', 'राजेंद्र प्रसाद', 'सरदार पटेल'] },
  'q-ga-2': { text: 'किस नदी को “दक्षिण गंगा” कहा जाता है?', options: ['कृष्णा', 'कावेरी', 'गोदावरी', 'नर्मदा'] },
  'q-ga-3': { text: 'भारत में रेपो दर किसके द्वारा निर्धारित की जाती है?', options: ['वित्त मंत्रालय', 'सेबी', 'भारतीय रिज़र्व बैंक की मौद्रिक नीति समिति', 'नीति आयोग'] },
  'q-ga-4': { text: 'सूर्य के प्रकाश के संपर्क में आने पर मानव त्वचा में कौन-सा विटामिन बनता है?', options: ['विटामिन A', 'विटामिन B12', 'विटामिन C', 'विटामिन D'] },
  'q-ga-5': { text: '1930 का दांडी मार्च किस कर के विरोध में शुरू किया गया था?', options: ['भू-राजस्व', 'नमक कर', 'आयकर', 'कपास शुल्क'] },
  'q-ga-6': { text: 'रेलवे मार्ग की लंबाई के आधार पर भारत का कौन-सा राज्य सबसे बड़ा है?', options: ['महाराष्ट्र', 'उत्तर प्रदेश', 'राजस्थान', 'गुजरात'] },
  'q-gs-1': { text: 'भारतीय संविधान का कौन-सा अनुच्छेद संवैधानिक उपचारों के अधिकार से संबंधित है?', options: ['अनुच्छेद 19', 'अनुच्छेद 21', 'अनुच्छेद 32', 'अनुच्छेद 44'] },
  'q-gs-2': { text: 'निम्नलिखित कथनों पर विचार कीजिए: 1. आर्द्रभूमियाँ कार्बन सिंक के रूप में कार्य करती हैं। 2. रामसर अभिसमय आर्द्रभूमियों के संरक्षण की संधि है। कौन-सा/से कथन सही है/हैं?', options: ['केवल 1', 'केवल 2', '1 और 2 दोनों', 'न तो 1, न ही 2'] },
  'q-gs-3': { text: 'भारतीय राष्ट्रीय कांग्रेस का वह अधिवेशन, जिसमें “पूर्ण स्वराज” का प्रस्ताव पारित हुआ, कहाँ हुआ था?', options: ['कलकत्ता', 'लाहौर', 'कराची', 'लखनऊ'] },
  'q-gs-4': { text: 'केंद्रीय बैंक द्वारा नकद आरक्षित अनुपात (CRR) बढ़ाने का सबसे संभावित प्रभाव क्या होगा?', options: ['मुद्रा आपूर्ति बढ़ेगी', 'बैंकों की ऋण देने की क्षमता घटेगी', 'मुद्रास्फीति की अपेक्षाएँ तुरंत शून्य हो जाएँगी', 'सरकारी उधारी बढ़ेगी'] },
  'q-gs-5': { text: 'निम्नलिखित में से कौन-सी एक ठंडी महासागरीय धारा है?', options: ['गल्फ स्ट्रीम', 'क्यूरोशियो धारा', 'लैब्राडोर धारा', 'ब्राज़ील धारा'] },
  'q-gs-6': { text: 'CRISPR-Cas9 तकनीक मुख्य रूप से किससे संबंधित है?', options: ['क्वांटम कंप्यूटिंग', 'जीन संपादन', 'उपग्रह नेविगेशन', 'बैटरी भंडारण'] },
  'q-cs-1': { text: 'n नोड वाले संतुलित बाइनरी सर्च ट्री में खोज की सबसे खराब स्थिति (worst case) में समय जटिलता क्या है?', options: ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'] },
  'q-cs-2': { text: 'निम्नलिखित में से कौन-सी डेडलॉक की आवश्यक शर्तें हैं? (सभी सही विकल्प चुनें)', options: ['परस्पर अपवर्जन (Mutual exclusion)', 'प्रीएम्प्शन (Preemption)', 'होल्ड एंड वेट (Hold and wait)', 'वृत्ताकार प्रतीक्षा (Circular wait)'] },
  'q-cs-3': { text: '1,024 तत्वों वाले क्रमबद्ध ऐरे पर बाइनरी सर्च सबसे खराब स्थिति में कितनी तुलनाएँ करता है? एक पूर्णांक दर्ज करें।' },
  'q-cs-4': { text: 'कोई संबंध (relation) BCNF में तब होता है, जब प्रत्येक गैर-तुच्छ फंक्शनल डिपेंडेंसी X → Y के लिए:', options: ['Y एक प्राइम एट्रिब्यूट हो', 'X एक सुपर की हो', 'X एक फॉरेन की हो', 'Y किसी कैंडिडेट की का भाग हो'] },
  'q-cs-5': { text: 'OSI मॉडल की कौन-सी परत नेटवर्कों के बीच पैकेट रूटिंग के लिए ज़िम्मेदार है?', options: ['डेटा लिंक', 'नेटवर्क', 'ट्रांसपोर्ट', 'सेशन'] },
  'q-cs-6': { text: 'लूप की बॉडी कितनी बार चलेगी? for (i = 1; i <= 20; i = i * 2)', options: ['4', '5', '10', '20'] },
  'q-cs-7': { text: 'निम्नलिखित में से कौन-सी भाषा रेगुलर (regular) नहीं है?', options: ['{a,b} पर ऐसी स्ट्रिंग जिनमें a की संख्या सम हो', 'n ≥ 0 के लिए aⁿbⁿ', '“ab” पर समाप्त होने वाली स्ट्रिंग', '{a,b} पर सभी स्ट्रिंग'] },
  'q-di-1': { text: 'किसी कंपनी का राजस्व 2023 में ₹200 करोड़ और 2024 में ₹250 करोड़ था। प्रतिशत वृद्धि कितनी है?', options: ['20%', '25%', '30%', '50%'] },
  'q-di-2': { text: '60 छात्रों की एक कक्षा में 40% क्रिकेट, 25% फुटबॉल और 10% दोनों खेलते हैं। कितने छात्र दोनों में से कोई खेल नहीं खेलते? एक संख्या दर्ज करें।' },
  'q-di-3': { text: 'एक लीग में चार टीमें एक-दूसरे से एक बार खेलती हैं। जीत पर 2 अंक, ड्रॉ पर 1 और हार पर 0 अंक मिलते हैं। सभी टीमें मिलकर अधिकतम कुल कितने अंक प्राप्त कर सकती हैं?', options: ['6', '8', '12', '16'] },
  'q-di-4': { text: 'Q1–Q4 में बिक्री (इकाइयों में) 120, 150, 180 और 150 थी। औसत तिमाही बिक्री कितनी है?', options: ['145', '150', '155', '160'] },
  'q-di-5': { text: '5 अलग-अलग पुस्तकों में से 3 अलग-अलग पुस्तकों को एक शेल्फ पर कितने तरीकों से व्यवस्थित किया जा सकता है? एक संख्या दर्ज करें।' },
};

const BILINGUAL_SUBJECTS = new Set(['quant', 'reasoning', 'general-awareness', 'general-studies', 'data-interpretation', 'computer-science']);

export const QUESTION_BANK: Question[] = BASE_BANK.map((q) =>
  HI[q.id] && BILINGUAL_SUBJECTS.has(q.subject) ? { ...q, translations: { ...q.translations, hi: HI[q.id] } } : q,
);

export const getQuestionById = (id: string): Question | undefined => liveCatalog.question(id) ?? QUESTION_BANK.find((q) => q.id === id);
