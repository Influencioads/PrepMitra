# Source Research Report (NEET UG)

Research date: **16 November 2026**. Official sources are authoritative. Coaching sites were used only to find the
official documents, never for questions, answers or the pattern.

## A. Official documents (primary)

| Document | URL | What was used |
|---|---|---|
| NTA Information Bulletin NEET (UG)-2026 | https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602231394640855.pdf (linked from https://neet.nta.nic.in/document/information-bulletin-english/) | Chapter 4: pattern, marking, mode, duration, mediums |
| NMC public notice and Syllabus for NEET (UG)-2026 (22 Dec 2025), NTA copy | https://nta.ac.in/Download/Notice/Notice_20260108180635.pdf | Every unit and subtopic in `taxonomy.json`. Also listed at https://neet.nta.nic.in/document/syllabus-for-neet-ug-2026-examination/ and https://www.nmc.org.in/neet/neet-ug/ |
| NTA FAQs on the NEET (UG)-2026 re-examination | https://nta.ac.in/Download/Notice/Notice_20260516152301.pdf | Re-exam date and timing (context only) |

## B. Reference for facts and methods

- **NCERT textbooks, Class 11 and 12** (Physics, Chemistry, Biology; rationalised editions) at https://ncert.nic.in/textbook.php.
  Biology answers cite the NCERT chapter in `solution.ncert_reference` so a reviewer can check them.
- Physical constants used in numericals are stated in the question (for example g = 10 m/s², 2.303RT/F = 0.059 V), as
  NEET papers do.

## C. Secondary (used only to locate official files)

| Page | Used for |
|---|---|
| https://news.careers360.com/neet-ug-2026-syllabus-out-nmc-finalised-no-chapters-removed-in-physics-chemistry-biology-download-pdf-link-mbbs-nta-exam-date | Confirmed that the NMC released the 2026 syllabus with no chapters removed; the unit list was then read from the official PDF |

## D. Previous-year papers and coaching content: copyright position

- **Coaching question banks are not used.** Allen, Aakash, PW, Embibe, Testbook, Careers360, Shiksha and similar sites
  own their questions, and their terms forbid scraping. Copying them would expose PrepMitra to takedown and copyright
  claims, so this bank does not scrape, copy or paraphrase them.
- **Official NEET papers** are published by NTA, which holds the copyright (Indian Copyright Act, government work).
  There are only about 180 to 200 questions a year, so 10 years give roughly 2,000, far short of 10,000. They are
  not used unless PrepMitra gets written permission from NTA. The schema has `Official PYQ` and `Licensed` source
  types for that case; the validator then requires a source URL and a licence note.
- **Therefore every question is `Original`**: written for the NMC 2026 syllabus and the NTA pattern. No question claims
  to have appeared in a NEET paper.

## E. What could not be verified

- The NMC syllabus PDF is partly a scanned image. Its text was read from the PDF's text layer. A few words in it are
  garbled (for example "insect (Frog)" in Biology Unit 2), and the taxonomy uses the plain meaning.
- Topic weights in `taxonomy.json` are planning estimates, not counts from official papers.
- Placing a topic in Botany or Zoology follows the usual split of the printed paper by NCERT chapter. The bulletin itself
  only says "Biology: 90".
