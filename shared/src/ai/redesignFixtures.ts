/* Generated from backend/app/services/ai_features (cheat_codes, lessons, teach_back, archetype) for mock mode.
   Answers are included here only because the mock API marks drills locally. Regenerate if the backend content changes. */
/* eslint-disable */
export const MOCK_CHEAT_CODES = [
 {
  "id": "ci-1331",
  "topic": "Compound interest",
  "title": "×1.331 for 10% CI, 3 yrs",
  "saves_seconds": 40,
  "trick": "1.1³ = 1.331. Multiply the principal once — no year-by-year.",
  "example": "₹8,000 at 10% CI for 3 years: 8,000 × 1.331 = ₹10,648.",
  "trap": "Only for 10% compounded annually. Half-yearly at 10% is 5% for 6 periods — 1.05⁶, not 1.331.",
  "exams": [
   "SSC CGL",
   "IBPS PO",
   "SBI PO"
  ],
  "drill": [
   {
    "text": "Amount on ₹5,000 at 10% p.a. compound interest for 3 years?",
    "options": [
     {
      "key": "A",
      "text": "₹6,500"
     },
     {
      "key": "B",
      "text": "₹6,655"
     },
     {
      "key": "C",
      "text": "₹6,600"
     },
     {
      "key": "D",
      "text": "₹6,750"
     }
    ],
    "answer": "B",
    "explanation": "5,000 × 1.331 = 6,655."
   },
   {
    "text": "Compound interest on ₹10,000 at 10% p.a. for 3 years?",
    "options": [
     {
      "key": "A",
      "text": "₹3,000"
     },
     {
      "key": "B",
      "text": "₹3,100"
     },
     {
      "key": "C",
      "text": "₹3,310"
     },
     {
      "key": "D",
      "text": "₹3,331"
     }
    ],
    "answer": "C",
    "explanation": "10,000 × 1.331 = 13,310, so CI = 3,310."
   },
   {
    "text": "₹2,000 at 10% p.a. compounded annually amounts to what after 3 years?",
    "options": [
     {
      "key": "A",
      "text": "₹2,662"
     },
     {
      "key": "B",
      "text": "₹2,600"
     },
     {
      "key": "C",
      "text": "₹2,620"
     },
     {
      "key": "D",
      "text": "₹2,731"
     }
    ],
    "answer": "A",
    "explanation": "2,000 × 1.331 = 2,662."
   }
  ]
 },
 {
  "id": "ci-si-2yr",
  "topic": "Compound interest",
  "title": "CI − SI for 2 years = P(r/100)²",
  "saves_seconds": 35,
  "trick": "The difference is just interest on the first year's interest.",
  "example": "P = ₹5,000, r = 10%: 5,000 × (0.1)² = ₹50.",
  "trap": "Only for exactly 2 years. For 3 years use P(r/100)² × (3 + r/100).",
  "exams": [
   "SSC CGL",
   "IBPS PO"
  ],
  "drill": [
   {
    "text": "CI − SI on ₹8,000 at 5% for 2 years?",
    "options": [
     {
      "key": "A",
      "text": "₹20"
     },
     {
      "key": "B",
      "text": "₹40"
     },
     {
      "key": "C",
      "text": "₹10"
     },
     {
      "key": "D",
      "text": "₹80"
     }
    ],
    "answer": "A",
    "explanation": "8,000 × 0.05² = 20."
   },
   {
    "text": "CI − SI on ₹12,000 at 10% for 2 years?",
    "options": [
     {
      "key": "A",
      "text": "₹100"
     },
     {
      "key": "B",
      "text": "₹120"
     },
     {
      "key": "C",
      "text": "₹144"
     },
     {
      "key": "D",
      "text": "₹240"
     }
    ],
    "answer": "B",
    "explanation": "12,000 × 0.1² = 120."
   },
   {
    "text": "CI − SI for 2 years at 20% is ₹160. The principal is:",
    "options": [
     {
      "key": "A",
      "text": "₹3,200"
     },
     {
      "key": "B",
      "text": "₹4,000"
     },
     {
      "key": "C",
      "text": "₹800"
     },
     {
      "key": "D",
      "text": "₹1,600"
     }
    ],
    "answer": "B",
    "explanation": "P × 0.04 = 160, so P = 4,000."
   }
  ]
 },
 {
  "id": "x-percent-of-y",
  "topic": "Percentages",
  "title": "x% of y = y% of x",
  "saves_seconds": 20,
  "trick": "Swap the two numbers when one side is friendlier.",
  "example": "16% of 25 = 25% of 16 = 4.",
  "trap": "If neither side is friendly (say 37% of 83), swapping saves nothing — approximate instead.",
  "exams": [
   "SSC CHSL",
   "IBPS Clerk"
  ],
  "drill": [
   {
    "text": "8% of 50 = ?",
    "options": [
     {
      "key": "A",
      "text": "4"
     },
     {
      "key": "B",
      "text": "40"
     },
     {
      "key": "C",
      "text": "0.4"
     },
     {
      "key": "D",
      "text": "5"
     }
    ],
    "answer": "A",
    "explanation": "50% of 8 = 4."
   },
   {
    "text": "24% of 25 = ?",
    "options": [
     {
      "key": "A",
      "text": "5"
     },
     {
      "key": "B",
      "text": "6"
     },
     {
      "key": "C",
      "text": "8"
     },
     {
      "key": "D",
      "text": "12"
     }
    ],
    "answer": "B",
    "explanation": "25% of 24 = 6."
   },
   {
    "text": "36% of 75 = ?",
    "options": [
     {
      "key": "A",
      "text": "24"
     },
     {
      "key": "B",
      "text": "25"
     },
     {
      "key": "C",
      "text": "27"
     },
     {
      "key": "D",
      "text": "30"
     }
    ],
    "answer": "C",
    "explanation": "75% of 36 = 27."
   }
  ]
 },
 {
  "id": "two-changes",
  "topic": "Percentages",
  "title": "Two changes: a + b + ab/100",
  "saves_seconds": 30,
  "trick": "Net % change of two successive changes, in one line.",
  "example": "+20% then −10%: 20 − 10 + (20 × −10)/100 = +8%.",
  "trap": "Keep the signs inside ab/100. For three changes apply it twice — never just add all three.",
  "exams": [
   "SSC CGL",
   "IBPS PO",
   "SBI Clerk"
  ],
  "drill": [
   {
    "text": "Price up 10%, then up 10%. Net change?",
    "options": [
     {
      "key": "A",
      "text": "+20%"
     },
     {
      "key": "B",
      "text": "+21%"
     },
     {
      "key": "C",
      "text": "+19%"
     },
     {
      "key": "D",
      "text": "+22%"
     }
    ],
    "answer": "B",
    "explanation": "10 + 10 + 100/100 = 21."
   },
   {
    "text": "Price up 25%, then down 20%. Net change?",
    "options": [
     {
      "key": "A",
      "text": "+5%"
     },
     {
      "key": "B",
      "text": "0%"
     },
     {
      "key": "C",
      "text": "−5%"
     },
     {
      "key": "D",
      "text": "+2%"
     }
    ],
    "answer": "B",
    "explanation": "25 − 20 − 500/100 = 0."
   },
   {
    "text": "Salary down 10%, then up 20%. Net change?",
    "options": [
     {
      "key": "A",
      "text": "+10%"
     },
     {
      "key": "B",
      "text": "+8%"
     },
     {
      "key": "C",
      "text": "+12%"
     },
     {
      "key": "D",
      "text": "−8%"
     }
    ],
    "answer": "B",
    "explanation": "−10 + 20 − 200/100 = 8."
   }
  ]
 },
 {
  "id": "together-ab",
  "topic": "Time & work",
  "title": "Together = ab / (a + b)",
  "saves_seconds": 30,
  "trick": "Two workers, days a and b: product over sum.",
  "example": "A takes 12 days, B takes 18: 216 ÷ 30 = 7.2 days together.",
  "trap": "Only two workers at constant speed. Three workers, or someone leaving midway — switch to LCM units.",
  "exams": [
   "SSC CGL",
   "SSC CHSL"
  ],
  "drill": [
   {
    "text": "A: 10 days, B: 15 days. Together?",
    "options": [
     {
      "key": "A",
      "text": "5 days"
     },
     {
      "key": "B",
      "text": "6 days"
     },
     {
      "key": "C",
      "text": "12.5 days"
     },
     {
      "key": "D",
      "text": "7 days"
     }
    ],
    "answer": "B",
    "explanation": "150 ÷ 25 = 6."
   },
   {
    "text": "A: 20 days, B: 30 days. Together?",
    "options": [
     {
      "key": "A",
      "text": "12 days"
     },
     {
      "key": "B",
      "text": "25 days"
     },
     {
      "key": "C",
      "text": "10 days"
     },
     {
      "key": "D",
      "text": "15 days"
     }
    ],
    "answer": "A",
    "explanation": "600 ÷ 50 = 12."
   },
   {
    "text": "A: 6 days, B: 12 days. Together?",
    "options": [
     {
      "key": "A",
      "text": "9 days"
     },
     {
      "key": "B",
      "text": "3 days"
     },
     {
      "key": "C",
      "text": "4 days"
     },
     {
      "key": "D",
      "text": "5 days"
     }
    ],
    "answer": "C",
    "explanation": "72 ÷ 18 = 4."
   }
  ]
 },
 {
  "id": "lcm-work",
  "topic": "Time & work",
  "title": "Total work = LCM of the days",
  "saves_seconds": 45,
  "trick": "Make work a whole number of units. Rates become integers.",
  "example": "A 10 days, B 15: work = 30 units; A = 3/day, B = 2/day; together 30 ÷ 5 = 6 days.",
  "trap": "If speeds come as a ratio (\"A is twice as fast as B\"), take units from the ratio, not the LCM.",
  "exams": [
   "SSC CGL",
   "IBPS PO",
   "SBI PO"
  ],
  "drill": [
   {
    "text": "A: 12 days, B: 18 days, C: 36 days. All together?",
    "options": [
     {
      "key": "A",
      "text": "6 days"
     },
     {
      "key": "B",
      "text": "8 days"
     },
     {
      "key": "C",
      "text": "9 days"
     },
     {
      "key": "D",
      "text": "4 days"
     }
    ],
    "answer": "A",
    "explanation": "Work 36: rates 3 + 2 + 1 = 6, so 6 days."
   },
   {
    "text": "A: 8 days, B: 12 days. A works 2 days alone, then B finishes. B takes?",
    "options": [
     {
      "key": "A",
      "text": "8 days"
     },
     {
      "key": "B",
      "text": "9 days"
     },
     {
      "key": "C",
      "text": "6 days"
     },
     {
      "key": "D",
      "text": "10 days"
     }
    ],
    "answer": "B",
    "explanation": "Work 24: A does 3 × 2 = 6, left 18, B at 2/day = 9 days."
   },
   {
    "text": "A and B together: 10 days. A alone: 15 days. B alone?",
    "options": [
     {
      "key": "A",
      "text": "25 days"
     },
     {
      "key": "B",
      "text": "30 days"
     },
     {
      "key": "C",
      "text": "20 days"
     },
     {
      "key": "D",
      "text": "35 days"
     }
    ],
    "answer": "B",
    "explanation": "Work 30: A+B = 3, A = 2, B = 1/day, so 30 days."
   }
  ]
 },
 {
  "id": "unit-digit",
  "topic": "DI",
  "title": "Unit-digit check",
  "saves_seconds": 25,
  "trick": "Multiply only the last digits. Kill options with the wrong ending.",
  "example": "347 × 28: 7 × 8 = 56 → ends in 6. Of 9,712 / 9,716 / 9,718, only 9,716 survives.",
  "trap": "If two options end in the same digit, follow up with a digit-sum (casting out nines) check.",
  "exams": [
   "SSC CGL",
   "IBPS PO",
   "IBPS Clerk"
  ],
  "drill": [
   {
    "text": "413 × 27 = ?",
    "options": [
     {
      "key": "A",
      "text": "11,149"
     },
     {
      "key": "B",
      "text": "11,151"
     },
     {
      "key": "C",
      "text": "11,153"
     },
     {
      "key": "D",
      "text": "11,157"
     }
    ],
    "answer": "B",
    "explanation": "3 × 7 = 21 → ends in 1. Only 11,151."
   },
   {
    "text": "268 × 34 = ?",
    "options": [
     {
      "key": "A",
      "text": "9,110"
     },
     {
      "key": "B",
      "text": "9,114"
     },
     {
      "key": "C",
      "text": "9,112"
     },
     {
      "key": "D",
      "text": "9,118"
     }
    ],
    "answer": "C",
    "explanation": "8 × 4 = 32 → ends in 2. Only 9,112."
   },
   {
    "text": "159 × 47 = ?",
    "options": [
     {
      "key": "A",
      "text": "7,473"
     },
     {
      "key": "B",
      "text": "7,475"
     },
     {
      "key": "C",
      "text": "7,477"
     },
     {
      "key": "D",
      "text": "7,471"
     }
    ],
    "answer": "A",
    "explanation": "9 × 7 = 63 → ends in 3. Only 7,473."
   }
  ]
 },
 {
  "id": "round-two-figures",
  "topic": "DI",
  "title": "Round to 2 figures when options are far apart",
  "saves_seconds": 50,
  "trick": "Options 10%+ apart? Round both numbers and divide in your head.",
  "example": "4,872 ÷ 19.6 ≈ 4,900 ÷ 20 = 245 (exact: 248.6).",
  "trap": "If options sit within 5% of each other, compute exactly — rounding can pick the wrong one.",
  "exams": [
   "IBPS PO",
   "SBI PO",
   "SSC CGL"
  ],
  "drill": [
   {
    "text": "Approximately 6,018 ÷ 29.8 = ?",
    "options": [
     {
      "key": "A",
      "text": "150"
     },
     {
      "key": "B",
      "text": "200"
     },
     {
      "key": "C",
      "text": "250"
     },
     {
      "key": "D",
      "text": "300"
     }
    ],
    "answer": "B",
    "explanation": "6,000 ÷ 30 = 200."
   },
   {
    "text": "Approximately 39.7% of 1,206 = ?",
    "options": [
     {
      "key": "A",
      "text": "360"
     },
     {
      "key": "B",
      "text": "420"
     },
     {
      "key": "C",
      "text": "480"
     },
     {
      "key": "D",
      "text": "540"
     }
    ],
    "answer": "C",
    "explanation": "40% of 1,200 = 480."
   },
   {
    "text": "Approximately 2,987 × 0.51 = ?",
    "options": [
     {
      "key": "A",
      "text": "1,200"
     },
     {
      "key": "B",
      "text": "1,500"
     },
     {
      "key": "C",
      "text": "1,800"
     },
     {
      "key": "D",
      "text": "2,100"
     }
    ],
    "answer": "B",
    "explanation": "3,000 × 0.5 = 1,500."
   }
  ]
 },
 {
  "id": "pin-one-both-cases",
  "topic": "Seating puzzles",
  "title": "Pin one, then draw both cases",
  "saves_seconds": 60,
  "trick": "Start from the clue that fixes a seat. Draw Case 1 and Case 2 side by side.",
  "example": "\"A sits at the extreme left; B is second to the right of A\" → A = 1, B = 3. Every later clue now has an anchor.",
  "trap": "If two clues still leave 4+ cases open, skip the puzzle and come back. It is a time sink.",
  "exams": [
   "IBPS PO",
   "SBI PO",
   "IBPS Clerk"
  ],
  "drill": [
   {
    "text": "Five in a row facing north. P is at the extreme left, Q is second to the right of P. Q's seat number from the left?",
    "options": [
     {
      "key": "A",
      "text": "2"
     },
     {
      "key": "B",
      "text": "3"
     },
     {
      "key": "C",
      "text": "4"
     },
     {
      "key": "D",
      "text": "5"
     }
    ],
    "answer": "B",
    "explanation": "P = 1, so Q = 3."
   },
   {
    "text": "Six around a circle facing the centre. A is 2nd to the right of D. Counting from D, which way do you go?",
    "options": [
     {
      "key": "A",
      "text": "Clockwise"
     },
     {
      "key": "B",
      "text": "Anticlockwise"
     },
     {
      "key": "C",
      "text": "Either"
     },
     {
      "key": "D",
      "text": "Cannot say"
     }
    ],
    "answer": "B",
    "explanation": "Facing the centre, right is anticlockwise."
   },
   {
    "text": "Which clue should you place first?",
    "options": [
     {
      "key": "A",
      "text": "C is not next to D"
     },
     {
      "key": "B",
      "text": "B sits between A and D"
     },
     {
      "key": "C",
      "text": "A sits at an extreme end"
     },
     {
      "key": "D",
      "text": "E is opposite B"
     }
    ],
    "answer": "C",
    "explanation": "A clue that fixes a seat is the anchor."
   }
  ]
 },
 {
  "id": "some-all-some",
  "topic": "Syllogism",
  "title": "Some + All = Some",
  "saves_seconds": 20,
  "trick": "Some A are B + All B are C → Some A are C. The middle term carries it.",
  "example": "Some pens are books. All books are bags. ⇒ Some pens are bags.",
  "trap": "\"All A are B\" + \"Some B are C\" gives NO definite link between A and C — only a possibility.",
  "exams": [
   "IBPS PO",
   "SBI Clerk"
  ],
  "drill": [
   {
    "text": "Some cats are dogs. All dogs are birds. Conclusion: Some cats are birds.",
    "options": [
     {
      "key": "A",
      "text": "Follows"
     },
     {
      "key": "B",
      "text": "Does not follow"
     },
     {
      "key": "C",
      "text": "Only a possibility"
     },
     {
      "key": "D",
      "text": "Cannot say"
     }
    ],
    "answer": "A",
    "explanation": "Some + All = Some."
   },
   {
    "text": "All roses are flowers. Some flowers are red. Conclusion: Some roses are red.",
    "options": [
     {
      "key": "A",
      "text": "Follows"
     },
     {
      "key": "B",
      "text": "Does not follow"
     },
     {
      "key": "C",
      "text": "Definitely false"
     },
     {
      "key": "D",
      "text": "Always true"
     }
    ],
    "answer": "B",
    "explanation": "All + Some gives no definite conclusion."
   },
   {
    "text": "Some pens are books. All books are bags. Conclusion: All pens are bags.",
    "options": [
     {
      "key": "A",
      "text": "Follows"
     },
     {
      "key": "B",
      "text": "Does not follow"
     },
     {
      "key": "C",
      "text": "Always true"
     },
     {
      "key": "D",
      "text": "Partly follows"
     }
    ],
    "answer": "B",
    "explanation": "Only Some pens are bags follows."
   }
  ]
 },
 {
  "id": "cross-out-of",
  "topic": "English",
  "title": "Cross out \"of the …\" to find the subject",
  "saves_seconds": 15,
  "trick": "Strike the phrase after \"of\". The verb agrees with what is left.",
  "example": "\"One of the boys were absent\" → One … was absent.",
  "trap": "\"A number of\" takes a plural verb; \"The number of\" takes a singular one. The strike-out rule does not apply.",
  "exams": [
   "SSC CGL",
   "IBPS PO",
   "SBI Clerk"
  ],
  "drill": [
   {
    "text": "Each of the students ___ a book.",
    "options": [
     {
      "key": "A",
      "text": "have"
     },
     {
      "key": "B",
      "text": "has"
     },
     {
      "key": "C",
      "text": "are having"
     },
     {
      "key": "D",
      "text": "were having"
     }
    ],
    "answer": "B",
    "explanation": "Each … has."
   },
   {
    "text": "The quality of the mangoes ___ poor.",
    "options": [
     {
      "key": "A",
      "text": "was"
     },
     {
      "key": "B",
      "text": "were"
     },
     {
      "key": "C",
      "text": "are"
     },
     {
      "key": "D",
      "text": "have been"
     }
    ],
    "answer": "A",
    "explanation": "Quality … was."
   },
   {
    "text": "A number of students ___ absent today.",
    "options": [
     {
      "key": "A",
      "text": "is"
     },
     {
      "key": "B",
      "text": "was"
     },
     {
      "key": "C",
      "text": "are"
     },
     {
      "key": "D",
      "text": "has been"
     }
    ],
    "answer": "C",
    "explanation": "\"A number of\" takes a plural verb."
   }
  ]
 },
 {
  "id": "stem-first-scan",
  "topic": "Reading",
  "title": "Stem-first scan",
  "saves_seconds": 20,
  "trick": "On any question over two lines, read the last sentence (the ask) first, then the data.",
  "example": "\"…How long will it take to cross a 360 m platform?\" Read that first: you need time, so look for speed and total distance.",
  "trap": "On one-line questions the ask is already in front of you — just read normally.",
  "exams": [
   "IBPS PO",
   "SBI PO",
   "SSC CGL"
  ],
  "drill": [
   {
    "text": "A word problem is four lines long. What do you read first?",
    "options": [
     {
      "key": "A",
      "text": "The first number"
     },
     {
      "key": "B",
      "text": "The last sentence"
     },
     {
      "key": "C",
      "text": "The options"
     },
     {
      "key": "D",
      "text": "The units"
     }
    ],
    "answer": "B",
    "explanation": "The last sentence tells you what to find."
   },
   {
    "text": "\"…What is the ratio of their present ages?\" Which quantity must your answer be?",
    "options": [
     {
      "key": "A",
      "text": "A ratio"
     },
     {
      "key": "B",
      "text": "An age in years"
     },
     {
      "key": "C",
      "text": "A difference"
     },
     {
      "key": "D",
      "text": "A sum"
     }
    ],
    "answer": "A",
    "explanation": "The ask is a ratio."
   },
   {
    "text": "When is stem-first scanning not needed?",
    "options": [
     {
      "key": "A",
      "text": "DI sets"
     },
     {
      "key": "B",
      "text": "Long word problems"
     },
     {
      "key": "C",
      "text": "One-line questions"
     },
     {
      "key": "D",
      "text": "Caselets"
     }
    ],
    "answer": "C",
    "explanation": "Short questions show the ask at once."
   }
  ]
 },
 {
  "id": "elimination",
  "topic": "Exam strategy",
  "title": "Eliminate two, then guess",
  "saves_seconds": 15,
  "trick": "Cross out two options before any guess. A blind guess with 5 options is worth 0 marks on average.",
  "example": "With 3 options left: +1 × 1/3 − 0.25 × 2/3 = +1/6 mark per guess on average.",
  "trap": "If you cannot remove even one option, skip — guessing costs time and gains nothing.",
  "exams": [
   "IBPS PO",
   "SBI PO",
   "SSC CGL"
  ],
  "drill": [
   {
    "text": "5 options, −0.25 per wrong. Expected marks of a blind guess?",
    "options": [
     {
      "key": "A",
      "text": "+0.2"
     },
     {
      "key": "B",
      "text": "0"
     },
     {
      "key": "C",
      "text": "−0.05"
     },
     {
      "key": "D",
      "text": "+0.25"
     }
    ],
    "answer": "B",
    "explanation": "1/5 − 0.25 × 4/5 = 0."
   },
   {
    "text": "3 options left, −0.25 per wrong. Expected marks of a guess?",
    "options": [
     {
      "key": "A",
      "text": "0"
     },
     {
      "key": "B",
      "text": "+1/6"
     },
     {
      "key": "C",
      "text": "+1/3"
     },
     {
      "key": "D",
      "text": "−1/6"
     }
    ],
    "answer": "B",
    "explanation": "1/3 − 0.25 × 2/3 = 1/6."
   },
   {
    "text": "You cannot rule out any option. Best move?",
    "options": [
     {
      "key": "A",
      "text": "Guess A"
     },
     {
      "key": "B",
      "text": "Skip"
     },
     {
      "key": "C",
      "text": "Guess the longest"
     },
     {
      "key": "D",
      "text": "Guess C"
     }
    ],
    "answer": "B",
    "explanation": "A blind guess is worth 0 and costs time."
   }
  ]
 }
] as const;

export const MOCK_LESSONS = [
 {
  "id": "circular-seating",
  "subject": "Reasoning",
  "topic": "Circular seating arrangement",
  "question": {
   "style": "IBPS PO style",
   "text": "Six friends A, B, C, D, E and F sit around a circular table, all facing the centre.",
   "clues": [
    "A is 2nd to the right of D",
    "B sits between A and D",
    "E sits opposite B",
    "C is not a neighbour of D"
   ]
  },
  "steps": [
   {
    "title": "Read & draw the table",
    "lines": [
     "Draw a circle with 6 seats.",
     "Everyone faces the centre."
    ],
    "trap": "Facing outside flips left and right. Check the first line every time.",
    "diagram": {
     "seats": 6
    }
   },
   {
    "title": "Fix an anchor",
    "lines": [
     "Put D at the top seat.",
     "Every other clue is counted from D."
    ],
    "trap": "Do not start from a clue with \"not\" — it fixes nothing.",
    "diagram": {
     "seats": 6,
     "placed": {
      "0": "D"
     }
    }
   },
   {
    "title": "Second to the right",
    "lines": [
     "A is 2nd to the RIGHT of D.",
     "Right = anticlockwise. Count 1, 2 from D. That is A."
    ],
    "trap": "Counting clockwise puts A in E's seat.",
    "diagram": {
     "seats": 6,
     "placed": {
      "0": "D",
      "4": "A"
     },
     "arrow": [
      0,
      4
     ]
    }
   },
   {
    "title": "Sitting between",
    "lines": [
     "B sits between A and D.",
     "Only one seat lies between them: B takes it."
    ],
    "trap": "\"Between\" means the seat directly between, not anywhere on that side.",
    "diagram": {
     "seats": 6,
     "placed": {
      "0": "D",
      "5": "B",
      "4": "A"
     }
    }
   },
   {
    "title": "Opposite = 3 seats away",
    "lines": [
     "E sits opposite B.",
     "With 6 seats, opposite is 3 seats away."
    ],
    "trap": "With 8 seats, opposite is 4 away. Count the seats first.",
    "diagram": {
     "seats": 6,
     "placed": {
      "0": "D",
      "5": "B",
      "4": "A",
      "2": "E"
     }
    }
   },
   {
    "title": "Eliminate & finish",
    "lines": [
     "C is not a neighbour of D, so C cannot sit next to D.",
     "C takes the seat next to E; F sits next to D."
    ],
    "trap": "Read every \"not\" clue last — it only removes options.",
    "diagram": {
     "seats": 6,
     "placed": {
      "0": "D",
      "5": "B",
      "4": "A",
      "2": "E",
      "3": "C",
      "1": "F"
     }
    }
   }
  ],
  "check": [
   {
    "text": "Who sits immediately to the LEFT of E?",
    "options": [
     {
      "key": "A",
      "text": "C"
     },
     {
      "key": "B",
      "text": "F"
     },
     {
      "key": "C",
      "text": "A"
     },
     {
      "key": "D",
      "text": "B"
     }
    ],
    "answer": "A",
    "explanation": "Left = clockwise when facing the centre. The next seat clockwise from E is C."
   },
   {
    "text": "Who sits opposite A?",
    "options": [
     {
      "key": "A",
      "text": "F"
     },
     {
      "key": "B",
      "text": "C"
     },
     {
      "key": "C",
      "text": "D"
     },
     {
      "key": "D",
      "text": "E"
     }
    ],
    "answer": "A",
    "explanation": "A and F are 3 seats apart."
   }
  ]
 },
 {
  "id": "trains-platform",
  "subject": "Quant",
  "topic": "Trains crossing a platform",
  "question": {
   "style": "SSC CGL style",
   "text": "A train 240 m long passes a pole in 16 seconds. How long will it take to cross a 360 m platform?",
   "clues": [
    "Train length 240 m",
    "Pole: 16 s",
    "Platform 360 m"
   ]
  },
  "steps": [
   {
    "title": "What does a pole mean?",
    "lines": [
     "Passing a pole, the train covers only its own length.",
     "Distance = 240 m."
    ],
    "trap": "A pole has no length — do not add anything."
   },
   {
    "title": "Find the speed",
    "lines": [
     "Speed = 240 ÷ 16 = 15 m/s."
    ],
    "trap": "Keep metres and seconds; convert to km/h only if the options ask."
   },
   {
    "title": "Platform distance",
    "lines": [
     "Crossing a platform: train + platform.",
     "240 + 360 = 600 m."
    ],
    "trap": "Using 360 m alone gives 24 s — the most chosen wrong option."
   },
   {
    "title": "Time = distance ÷ speed",
    "lines": [
     "600 ÷ 15 = 40 seconds."
    ],
    "trap": "Check: 15 × 40 = 600."
   }
  ],
  "check": [
   {
    "text": "A 150 m train passes a pole in 10 s. Its speed?",
    "options": [
     {
      "key": "A",
      "text": "15 m/s"
     },
     {
      "key": "B",
      "text": "10 m/s"
     },
     {
      "key": "C",
      "text": "25 m/s"
     },
     {
      "key": "D",
      "text": "1.5 m/s"
     }
    ],
    "answer": "A",
    "explanation": "150 ÷ 10 = 15."
   },
   {
    "text": "Same train, 300 m platform. Time to cross?",
    "options": [
     {
      "key": "A",
      "text": "20 s"
     },
     {
      "key": "B",
      "text": "30 s"
     },
     {
      "key": "C",
      "text": "45 s"
     },
     {
      "key": "D",
      "text": "25 s"
     }
    ],
    "answer": "B",
    "explanation": "(150 + 300) ÷ 15 = 30."
   }
  ]
 },
 {
  "id": "syllogism-basics",
  "subject": "Reasoning",
  "topic": "Syllogism: All and Some",
  "question": {
   "style": "IBPS PO style",
   "text": "All A are B. Some B are C. Can we say: Some A are C?",
   "clues": [
    "All A are B",
    "Some B are C"
   ]
  },
  "steps": [
   {
    "title": "Draw the first statement",
    "lines": [
     "All A are B: draw A fully inside B."
    ],
    "trap": "Do not draw A and B as equal circles."
   },
   {
    "title": "Add the second",
    "lines": [
     "Some B are C: C overlaps B somewhere."
    ],
    "trap": "\"Some\" does not say where the overlap is."
   },
   {
    "title": "Try to break it",
    "lines": [
     "Can C overlap B only outside A? Yes.",
     "Then no A is C."
    ],
    "trap": "If one valid drawing breaks the conclusion, it does not follow."
   },
   {
    "title": "Conclude",
    "lines": [
     "Some A are C does NOT follow.",
     "It is only a possibility."
    ],
    "trap": "Only \"always true\" conclusions follow."
   }
  ],
  "check": [
   {
    "text": "Some cats are dogs. All dogs are birds. Some cats are birds?",
    "options": [
     {
      "key": "A",
      "text": "Follows"
     },
     {
      "key": "B",
      "text": "Does not follow"
     },
     {
      "key": "C",
      "text": "Possibility only"
     },
     {
      "key": "D",
      "text": "Cannot say"
     }
    ],
    "answer": "A",
    "explanation": "Some + All = Some."
   },
   {
    "text": "All pens are books. Some books are red. Some pens are red?",
    "options": [
     {
      "key": "A",
      "text": "Follows"
     },
     {
      "key": "B",
      "text": "Does not follow"
     },
     {
      "key": "C",
      "text": "Always true"
     },
     {
      "key": "D",
      "text": "Definitely false"
     }
    ],
    "answer": "B",
    "explanation": "All + Some gives no definite link."
   }
  ]
 }
] as const;

export const MOCK_TEACH_CONCEPTS = [
 {
  "id": "syllogism-all-some",
  "topic": "Syllogism",
  "board": [
   "All A are B.",
   "Some B are C."
  ],
  "ask": "Can we say: Some A are C?",
  "diagram": "venn-all-some",
  "rounds": [
   {
    "kind": "Conclusion check",
    "mood": "curious",
    "chotu": "Bhaiya, A sits inside B, and B touches C… so some A must be C, na? Looks obvious to me!",
    "coach_hint": "Ask yourself: is it ALWAYS true, or just possible? Only \"always\" follows.",
    "keywords": [
     "draw",
     "outside",
     "not follow",
     "doesn't follow",
     "does not follow",
     "possib",
     "always"
    ],
    "options": [
     {
      "key": "A",
      "text": "Yes, it follows. A is inside B and C touches B, so A and C have to meet somewhere.",
      "scores": {
       "clarity": 6,
       "correctness": 0,
       "examples": 2
      },
      "note": "Chotu agrees — but you taught him the classic trap. C can touch B away from A.",
      "good": false
     },
     {
      "key": "B",
      "text": "Draw it. Put A fully inside B. C can overlap only the part of B outside A — so no A has to be C. It does not follow.",
      "scores": {
       "clarity": 9,
       "correctness": 10,
       "examples": 9
      },
      "note": "Spot on. You showed one drawing that breaks the conclusion — that is the proof.",
      "good": true
     },
     {
      "key": "C",
      "text": "No conclusion — the middle term B is not distributed in either statement.",
      "scores": {
       "clarity": 5,
       "correctness": 8,
       "examples": 2
      },
      "note": "Correct, but Chotu does not know what \"distributed\" means. Show him with a drawing.",
      "good": true
     }
    ]
   },
   {
    "kind": "Possibility",
    "mood": "confused",
    "chotu": "Okay, it doesn't follow. But then is \"Some A are C\" false? Should I mark it wrong?",
    "coach_hint": "Not following is different from being false. Can it be true in some drawing?",
    "keywords": [
     "possib",
     "can be",
     "may be",
     "might",
     "either",
     "both",
     "draw"
    ],
    "options": [
     {
      "key": "A",
      "text": "Yes, it is false. If it does not follow, it is wrong.",
      "scores": {
       "clarity": 6,
       "correctness": 0,
       "examples": 0
      },
      "note": "Careful — \"does not follow\" is not \"false\". It can still be true in another drawing.",
      "good": false
     },
     {
      "key": "B",
      "text": "Not false — it is a possibility. Draw C over A too and it becomes true. Exams ask this as \"Some A being C is a possibility\".",
      "scores": {
       "clarity": 9,
       "correctness": 10,
       "examples": 8
      },
      "note": "Great. Two drawings, two outcomes — so it is only a possibility.",
      "good": true
     },
     {
      "key": "C",
      "text": "We cannot say anything about A and C at all.",
      "scores": {
       "clarity": 6,
       "correctness": 6,
       "examples": 0
      },
      "note": "Half right. We can say it is possible. Show him a drawing where it is true.",
      "good": false
     }
    ]
   },
   {
    "kind": "Flip it",
    "mood": "testing",
    "chotu": "What if it said \"Some A are B. All B are C.\" Now does Some A are C follow?",
    "coach_hint": "Some + All = Some. The middle term carries it.",
    "keywords": [
     "follow",
     "some + all",
     "inside",
     "all b",
     "carries",
     "draw"
    ],
    "options": [
     {
      "key": "A",
      "text": "Yes. The part of A inside B is also inside C, because all of B is inside C. So some A are C.",
      "scores": {
       "clarity": 9,
       "correctness": 10,
       "examples": 8
      },
      "note": "Exactly — Some + All = Some. You traced the overlap through B.",
      "good": true
     },
     {
      "key": "B",
      "text": "No, same as before — it never follows.",
      "scores": {
       "clarity": 5,
       "correctness": 0,
       "examples": 0
      },
      "note": "Order matters. With \"All B are C\", every bit of B sits inside C.",
      "good": false
     },
     {
      "key": "C",
      "text": "Only a possibility.",
      "scores": {
       "clarity": 5,
       "correctness": 3,
       "examples": 0
      },
      "note": "Draw it: the A-and-B overlap is inside B, and B is inside C. It is definite.",
      "good": false
     }
    ]
   }
  ]
 },
 {
  "id": "right-anticlockwise",
  "topic": "Circular seating",
  "board": [
   "Six people sit around a table,",
   "facing the centre."
  ],
  "ask": "Is \"right\" clockwise or anticlockwise?",
  "diagram": "circle-6",
  "rounds": [
   {
    "kind": "Direction",
    "mood": "curious",
    "chotu": "Right is always clockwise na? Like a clock goes to the right?",
    "coach_hint": "Sit at the table yourself. Which way does your right hand point?",
    "keywords": [
     "anticlockwise",
     "anti-clockwise",
     "counter",
     "facing",
     "centre",
     "center",
     "hand"
    ],
    "options": [
     {
      "key": "A",
      "text": "Yes, right is clockwise always.",
      "scores": {
       "clarity": 6,
       "correctness": 0,
       "examples": 0
      },
      "note": "That is true only when people face outside.",
      "good": false
     },
     {
      "key": "B",
      "text": "Facing the centre, your right hand points anticlockwise. So right = anticlockwise, left = clockwise.",
      "scores": {
       "clarity": 9,
       "correctness": 10,
       "examples": 7
      },
      "note": "Clear and correct. The \"sit at the table\" picture makes it stick.",
      "good": true
     },
     {
      "key": "C",
      "text": "It depends on the question.",
      "scores": {
       "clarity": 4,
       "correctness": 5,
       "examples": 0
      },
      "note": "True but vague. Say what it depends on: facing in or out.",
      "good": false
     }
    ]
   },
   {
    "kind": "Facing outside",
    "mood": "confused",
    "chotu": "And if they face outside, everything flips?",
    "coach_hint": "Turn around in your chair. What happens to your right hand?",
    "keywords": [
     "flip",
     "clockwise",
     "reverse",
     "opposite",
     "turn"
    ],
    "options": [
     {
      "key": "A",
      "text": "Yes. Facing outside, right = clockwise and left = anticlockwise.",
      "scores": {
       "clarity": 9,
       "correctness": 10,
       "examples": 5
      },
      "note": "Correct. Add an example and Chotu will never forget it.",
      "good": true
     },
     {
      "key": "B",
      "text": "No, it stays the same.",
      "scores": {
       "clarity": 5,
       "correctness": 0,
       "examples": 0
      },
      "note": "Turn around and check — your right hand now points the other way.",
      "good": false
     },
     {
      "key": "C",
      "text": "Only left flips.",
      "scores": {
       "clarity": 4,
       "correctness": 0,
       "examples": 0
      },
      "note": "Both flip together.",
      "good": false
     }
    ]
   },
   {
    "kind": "Count it",
    "mood": "testing",
    "chotu": "D is at the top, facing the centre. Who is 2nd to the right of D if seats go D, F, E, C, A, B clockwise?",
    "coach_hint": "Right = anticlockwise. Count two seats that way.",
    "keywords": [
     "a",
     "anticlockwise",
     "count",
     "two"
    ],
    "options": [
     {
      "key": "A",
      "text": "E — count two clockwise.",
      "scores": {
       "clarity": 6,
       "correctness": 0,
       "examples": 4
      },
      "note": "That is 2nd to the left.",
      "good": false
     },
     {
      "key": "B",
      "text": "A — right is anticlockwise, so count B (1), A (2).",
      "scores": {
       "clarity": 9,
       "correctness": 10,
       "examples": 9
      },
      "note": "Perfect, and you showed the counting.",
      "good": true
     },
     {
      "key": "C",
      "text": "B",
      "scores": {
       "clarity": 3,
       "correctness": 0,
       "examples": 0
      },
      "note": "B is only 1st to the right.",
      "good": false
     }
    ]
   }
  ]
 }
] as const;

export const MOCK_PERSONA_TYPES = [
 {
  "key": "fast_guesser",
  "name": "The Fast Guesser",
  "tagline": "quick hands, loose aim",
  "icon": "zap",
  "description": "Moves fast and attempts nearly everything, but commits before the question is fully read. Marks leak through negative marking, not through lack of knowledge.",
  "signals": [
   "Many answers locked in under 15 seconds",
   "Very high attempts, middling accuracy",
   "Wrong answers cluster in long questions"
  ],
  "shape": {
   "speed": 92,
   "accuracy": 55,
   "risk": 95,
   "stamina": 70,
   "recovery": 50,
   "consistency": 60
  }
 },
 {
  "key": "perfectionist",
  "name": "The Perfectionist",
  "tagline": "right answers, too few of them",
  "icon": "target",
  "description": "Rarely wrong, but attempts too few questions. Marks are lost to the clock and to questions left blank that you could have solved.",
  "signals": [
   "Accuracy well above average",
   "Low attempt count",
   "Many questions skipped near the end"
  ],
  "shape": {
   "speed": 25,
   "accuracy": 90,
   "risk": 40,
   "stamina": 60,
   "recovery": 78,
   "consistency": 75
  }
 },
 {
  "key": "section_hopper",
  "name": "The Section Hopper",
  "tagline": "everywhere at once",
  "icon": "shuffle",
  "description": "Jumps between sections and questions without a fixed order. Time leaks in the switching, and scores swing from mock to mock.",
  "signals": [
   "Score swings between mocks",
   "Time spread unevenly across sections",
   "Questions revisited often"
  ],
  "shape": {
   "speed": 60,
   "accuracy": 65,
   "risk": 70,
   "stamina": 55,
   "recovery": 55,
   "consistency": 35
  }
 },
 {
  "key": "late_bloomer",
  "name": "The Late Bloomer",
  "tagline": "slow start, strong finish",
  "icon": "sunrise",
  "description": "Starts cautiously and loses easy marks early, then finds rhythm in the second half. The first ten minutes decide the score.",
  "signals": [
   "Accuracy rises through the paper",
   "Slow on the first questions",
   "Strong last 15 minutes"
  ],
  "shape": {
   "speed": 40,
   "accuracy": 65,
   "risk": 60,
   "stamina": 88,
   "recovery": 70,
   "consistency": 55
  }
 },
 {
  "key": "steady_climber",
  "name": "The Steady Climber",
  "tagline": "calm, even, improving",
  "icon": "trending-up",
  "description": "Balanced speed and accuracy, and scores that climb mock by mock. The next marks come from topic depth, not exam habits.",
  "signals": [
   "Scores rise steadily",
   "Accuracy holds all paper long",
   "Recovers well after mistakes"
  ],
  "shape": {
   "speed": 58,
   "accuracy": 76,
   "risk": 70,
   "stamina": 76,
   "recovery": 76,
   "consistency": 85
  }
 },
 {
  "key": "overthinker",
  "name": "The Overthinker",
  "tagline": "second-guesses the right answer",
  "icon": "help-circle",
  "description": "Knows the method but spends too long checking, and changes right answers to wrong ones. Time, not knowledge, caps the score.",
  "signals": [
   "Long time per question",
   "Good accuracy on attempted questions",
   "Weak final minutes"
  ],
  "shape": {
   "speed": 15,
   "accuracy": 80,
   "risk": 50,
   "stamina": 45,
   "recovery": 65,
   "consistency": 65
  }
 }
] as const;

export const MOCK_PERSONA_PLANS = {
 "fast_guesser": [
  {
   "title": "Read the ask before the data",
   "code_id": "stem-first-scan",
   "body": "Any question over two lines: read the last sentence first, then the numbers. In drills you get a 20-second minimum on these."
  },
  {
   "title": "Eliminate two, then guess",
   "code_id": "elimination",
   "body": "With 3 options left, a guess is worth +1/6 of a mark on average. With 5 left it is worth 0. Never guess before you cross two out."
  },
  {
   "title": "Three-second answer check",
   "code_id": "unit-digit",
   "body": "Before you lock a quick Quant answer, check the unit digit. It catches most rushed slips and costs about three seconds."
  }
 ],
 "perfectionist": [
  {
   "title": "Two-pass the paper",
   "code_id": "round-two-figures",
   "body": "First pass: only questions you can finish in 45 seconds. Second pass: the rest. Never sit on one question for two minutes in the first pass."
  },
  {
   "title": "Approximate when options are far apart",
   "code_id": "round-two-figures",
   "body": "If options are 10% or more apart, round and divide in your head. Exact working is wasted time."
  },
  {
   "title": "Attempt target per section",
   "code_id": "elimination",
   "body": "Set an attempt target before each section and track it. Accuracy above 85% means you can afford more attempts."
  }
 ],
 "section_hopper": [
  {
   "title": "Fix a section order",
   "code_id": "pin-one-both-cases",
   "body": "Decide the order before the mock and keep it for five mocks. Change only one thing at a time."
  },
  {
   "title": "Skip, don't hop",
   "code_id": "elimination",
   "body": "If a question is not clear in 20 seconds, mark it and move on. Come back only after the section is done."
  },
  {
   "title": "Check before you switch",
   "code_id": "unit-digit",
   "body": "Before leaving a section, spend 30 seconds checking marked answers with the unit digit."
  }
 ],
 "late_bloomer": [
  {
   "title": "Warm up before the mock",
   "code_id": "x-percent-of-y",
   "body": "Do five quick calculation questions just before you start. Your first section then gets your real speed."
  },
  {
   "title": "Start with your best section",
   "code_id": "round-two-figures",
   "body": "Open with the section where you are most accurate to build momentum."
  },
  {
   "title": "Bank time early",
   "code_id": "together-ab",
   "body": "Use one-line formulas on standard questions in the first half so the end is not rushed."
  }
 ],
 "steady_climber": [
  {
   "title": "Go deep on one weak topic a week",
   "code_id": "lcm-work",
   "body": "Your habits are sound. Pick the weakest topic and do one focused drill set each day."
  },
  {
   "title": "Learn the shortcut for each topic",
   "code_id": "ci-1331",
   "body": "Every topic has one shortcut worth knowing. Unlock them in Cheat codes."
  },
  {
   "title": "Raise the attempt target slowly",
   "code_id": "elimination",
   "body": "Add two attempts per section per mock while accuracy stays above 75%."
  }
 ],
 "overthinker": [
  {
   "title": "One check, then lock",
   "code_id": "unit-digit",
   "body": "Allow yourself exactly one quick check (unit digit or units). Then lock and move on."
  },
  {
   "title": "90-second ceiling",
   "code_id": "round-two-figures",
   "body": "If a question passes 90 seconds, mark it and skip. Come back only if time is left."
  },
  {
   "title": "Trust the first clean answer",
   "code_id": "elimination",
   "body": "Change an answer only if you find a definite error, not a feeling."
  }
 ]
} as const;

