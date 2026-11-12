"""Writes batches/parts/BATCH_010_COMP.json: the 99 Computer Knowledge questions of BATCH_010 (the final Computer batch).

BATCH_010 builds applied scenarios around six shared stimuli (the 16-bit status word of a note-sorting machine, a
teaching accumulator processor running a small program, overnight batch jobs on an end-of-day server, a DNS lookup
made by a branch PC, a Cheques table for SQL and an Excel gold-loan register). Every computable answer is re-derived
below with assertions before the file is written: bit-field extraction, octal form and 16-bit rotation, base
comparison, an accumulator-machine simulation (PC, stored result, memory accesses), non-preemptive and preemptive
priority scheduling, DNS TTL expiry, set-associative mapping, TLB effective access time, cache hit ratio, a printer
page bitmap, stop-and-wait efficiency, IPv4 fragment offsets, a toy RSA private exponent, SQL in sqlite3 (MIN,
UPDATE row count, INTERSECT, <> with NULL, > ALL, LAG) and Excel PROPER / EOMONTH / HLOOKUP / DATEDIF. The plan quota
per (topic, difficulty), subtopics, the ID range, stimulus IDs and the answer-key balance are also asserted. If any
assertion fails, nothing is written.

    python tools/batch_010/computer.py      (run from docs/question-bank)
"""

import datetime as dt
import json
import random
import sqlite3
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
LETTERS = "ABCD"
CK = "Computer Knowledge"
FIRST_ID = 902
SELF = "ai:self-recheck"
REC = "script:recompute"
IND = "ai:independent-check"
SC = "web:search-confirmed"
# A separate fresh subagent answered every question from a key-free dump (made in the author's scratchpad).
# BLIND_DONE is switched on only after that check; IDs it did not match are listed in BLIND_MISMATCH and do not get
# ai:independent-check.
BLIND_DONE = True
BLIND_MISMATCH = set()

_rng = random.Random(20261105 + 10)
_keys = Counter()
questions = []
stimuli = []
_stim_no = [0]


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


def ordered(correct, distractors, fmt=str):
    """Numeric options in ascending order; returns (option texts, answer letter)."""
    vals = sorted([correct] + list(distractors))
    assert len(set(vals)) == 4, vals
    return [fmt(v) for v in vals], LETTERS[vals.index(correct)]


def new_stim(kind, title, content, solution):
    _stim_no[0] += 1
    sid = f"STIM_COMP_010{_stim_no[0]:03d}"
    stimuli.append({"stimulus_id": sid, "type": kind, "title": title, "content": content, "solution": solution})
    return sid


def Q(topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, wrong, seconds=30,
      shortcut=None, computed=False, facts=None, web="web:fact-check", stim=None, pos=None):
    """Adds one question. With answer=None, options[0] is the correct text and it is placed at the least-used key
    so far (random tie-break, fixed seed). Ordered options (numbers) pass an explicit answer letter."""
    assert len(options) == 4 and len(set(options)) == 4, text
    if answer is None:
        low = min(_keys[k] for k in LETTERS)
        p = LETTERS.index(_rng.choice([k for k in LETTERS if _keys[k] == low]))
        correct, wrongs = options[0], list(options[1:])
        options = wrongs[:p] + [correct] + wrongs[p:]
        answer = LETTERS[p]
    assert answer in LETTERS
    _keys[answer] += 1
    qid = f"BANK_COMP_{FIRST_ID + len(questions):06d}"
    vb = ([REC] if computed else []) + [SELF]
    if BLIND_DONE and qid not in BLIND_MISMATCH:
        vb.append(IND)
    v = {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
         "verified_by": vb, "verified_at": TODAY}
    if facts:
        vb.append(web)
        v["fact_checks"] = facts
    q = {
        "question_id": qid,
        "exam_mappings": default_mappings(CK, difficulty),
        "subject": CK, "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_type": "MCQ", "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": wrong,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": v,
    }
    if stim:
        q["stimulus_id"] = stim
        q["set_position"] = pos
    questions.append(q)


# ---------------------------------------------------------------- verification of computable answers
# 1. Status word of a note-sorting machine: 16-bit word 0x9C5A
W = 0x9C5A
WBIN = format(W, "016b")
assert WBIN == "1001110001011010"
MODE = (W >> 13) & 0b111
COUNT = (W >> 5) & 0xFF
ERR = W & 0b11111
assert (MODE, COUNT, ERR) == (4, 226, 26), (MODE, COUNT, ERR)
assert (MODE << 13) | (COUNT << 5) | ERR == W
assert W == 40026 and oct(W) == "0o116132"
ROTL4 = ((W << 4) | (W >> 12)) & 0xFFFF
assert ROTL4 == 0xC5A9
assert (W << 4) & 0xFFFF == 0xC5A0 and W >> 4 == 0x09C5 and ((W >> 4) | (W << 12)) & 0xFFFF == 0xA9C5
# wrong readings used as distractors
assert (W >> 5) & 0xFF != (W >> 4) & 0xFF and (W >> 4) & 0xFF == 0xC5 == 197 and W & 0xFF == 90
assert int("116132", 8) == 40026 and int("9C5A", 16) == 40026
assert format(0b1001110001011010, "o") == "116132"

# Base comparison
assert int("3E", 16) == 62 and int("75", 8) == 61 and int("111111", 2) == 63
assert int("17", 8) == 15

# 2. Accumulator machine
MEM0 = {200: 45, 201: 60, 202: 0}
PROG = {100: ("LOAD", 200), 101: ("SUB", 201), 102: ("JUMPNEG", 106), 103: ("LOAD", 200), 104: ("STORE", 202),
        105: ("HALT", None), 106: ("LOAD", 201), 107: ("STORE", 202), 108: ("HALT", None)}


def run(mem):
    mem = dict(mem)
    pc, acc, fetches, data, trace, pc_after = 100, 0, 0, 0, [], {}
    while True:
        op, adr = PROG[pc]
        fetches += 1
        here = pc
        pc += 1
        trace.append(here)
        if op == "LOAD":
            acc = mem[adr]
            data += 1
        elif op == "SUB":
            acc -= mem[adr]
            data += 1
        elif op == "STORE":
            mem[adr] = acc
            data += 1
        elif op == "JUMPNEG":
            if acc < 0:
                pc = adr
        elif op == "HALT":
            pc_after[here] = pc
            return mem, acc, fetches, data, trace, pc_after
        pc_after[here] = pc


M1, ACC1, F1, D1, T1, PCA = run(MEM0)
assert M1[202] == 60 and T1 == [100, 101, 102, 106, 107, 108] and PCA[102] == 106 and PCA[101] == 102
assert F1 == 6 and D1 == 4 and F1 + D1 == 10
M2, _, F2, D2, T2, _ = run({200: 75, 201: 60, 202: 0})
assert M2[202] == 75 and T2 == [100, 101, 102, 103, 104, 105] and 75 - 60 == 15

# 3. Overnight batch jobs: (name, arrival, burst, priority) - smaller number = higher priority
JOBS = [("J1", 0, 8, 3), ("J2", 1, 4, 1), ("J3", 2, 9, 4), ("J4", 3, 5, 2)]


def np_priority(jobs):
    t, done, order, fin = 0, set(), [], {}
    while len(done) < len(jobs):
        ready = [j for j in jobs if j[0] not in done and j[1] <= t]
        if not ready:
            t = min(j[1] for j in jobs if j[0] not in done)
            continue
        j = min(ready, key=lambda x: (x[3], x[1]))
        t += j[2]
        fin[j[0]] = t
        done.add(j[0])
        order.append(j[0])
    return order, fin


def p_priority(jobs):
    rem = {j[0]: j[2] for j in jobs}
    t, fin = 0, {}
    while rem:
        ready = [j for j in jobs if j[0] in rem and j[1] <= t]
        j = min(ready, key=lambda x: (x[3], x[1]))
        rem[j[0]] -= 1
        t += 1
        if rem[j[0]] == 0:
            del rem[j[0]]
            fin[j[0]] = t
    return fin


ORDER, FIN = np_priority(JOBS)
assert ORDER == ["J1", "J2", "J4", "J3"] and FIN == {"J1": 8, "J2": 12, "J4": 17, "J3": 26}
TAT = {j[0]: FIN[j[0]] - j[1] for j in JOBS}
assert sum(TAT.values()) / 4 == 14.25
assert sum(FIN.values()) / 4 == 15.75  # completion times averaged without subtracting arrival
WAIT_NP = {j[0]: TAT[j[0]] - j[2] for j in JOBS}
assert sum(WAIT_NP.values()) / 4 == 7.75
FINP = p_priority(JOBS)
assert FINP == {"J2": 5, "J4": 10, "J1": 17, "J3": 26}
WAIT_P = {j[0]: FINP[j[0]] - j[1] - j[2] for j in JOBS}
assert WAIT_P == {"J1": 9, "J2": 0, "J3": 15, "J4": 2} and sum(WAIT_P.values()) / 4 == 6.5
assert sum(FINP[j[0]] - j[1] for j in JOBS) / 4 == 13.0

# 4. DNS TTL: cached at 10:00:00 with TTL 300 s
assert (dt.datetime(2026, 11, 5, 10, 0, 0) + dt.timedelta(seconds=300)).strftime("%H:%M:%S") == "10:05:00"
assert ".".join(reversed("203.0.113.25".split("."))) + ".in-addr.arpa" == "25.113.0.203.in-addr.arpa"

# 5. Memory
assert (2000 - 150) / 2000 * 100 == 92.5
SETS = 256 // 4
assert SETS == 64 and 1000 % SETS == 40 and 1000 % 256 == 232 and 1000 // 64 == 15
EAT = 0.8 * (10 + 100) + 0.2 * (10 + 100 + 100)
assert round(EAT, 6) == 130 and 0.8 * 100 + 0.2 * 200 == 120 and 0.8 * 110 + 0.2 * 110 == 110
# printer page bitmap: 8 x 10 inch at 600 dpi, 1 bit per dot
DOTS = (8 * 600) * (10 * 600)
assert DOTS == 28_800_000 and DOTS // 8 == 3_600_000 and DOTS * 3 == 86_400_000

# 6. Networking: stop-and-wait, fragmentation
TF = 1000 * 8 / 1e6 * 1000  # ms
assert TF == 8 and TF / (TF + 2 * 4) == 0.5 and round(TF / (TF + 4) * 100, 1) == 66.7
DATA = 4000 - 20
PER = (1500 - 20) // 8 * 8
assert PER == 1480
frags, off = [], 0
while off < DATA:
    size = min(PER, DATA - off)
    frags.append((off // 8, size))
    off += size
assert frags == [(0, 1480), (185, 1480), (370, 1020)]

# 7. RSA toy example
P_, Q_, E_ = 3, 11, 3
N_, PHI = P_ * Q_, (P_ - 1) * (Q_ - 1)
D_ = next(d for d in range(1, PHI) if d * E_ % PHI == 1)
assert (N_, PHI, D_) == (33, 20, 7) and pow(pow(4, E_, N_), D_, N_) == 4
assert next(d for d in range(1, 32) if d * E_ % 32 == 1) == 11  # using n - 1 = 32 instead of phi gives 11

# 8. SQL: Cheques table
CHQ = [("C101", "A1", 25000, "Cleared", "2026-11-02"), ("C102", "A2", 48000, "Returned", "2026-11-02"),
       ("C103", "A1", 12000, "Pending", "2026-11-03"), ("C104", "A3", 75000, "Cleared", "2026-11-03"),
       ("C105", "A2", 30000, "Cleared", "2026-11-04"), ("C106", "A4", 9000, "Returned", "2026-11-04"),
       ("C107", "A3", 60000, None, "2026-11-04"), ("C108", "A1", 40000, "Pending", "2026-11-05")]
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Cheques (chq_no TEXT PRIMARY KEY, acc_no TEXT, amount INTEGER, status TEXT, "
           "presented_on TEXT)")
db.executemany("INSERT INTO Cheques VALUES (?, ?, ?, ?, ?)", CHQ)


def col(sql):
    return [r[0] for r in db.execute(sql)]


assert col("SELECT MIN(amount) FROM Cheques WHERE status = 'Returned'") == [9000]
assert col("SELECT MIN(amount) FROM Cheques") == [9000]
assert col("SELECT acc_no FROM Cheques WHERE status = 'Cleared' INTERSECT "
           "SELECT acc_no FROM Cheques WHERE status = 'Returned'") == ["A2"]
assert col("SELECT COUNT(*) FROM Cheques WHERE status <> 'Cleared'") == [4]
assert col("SELECT COUNT(*) FROM Cheques WHERE status IS NOT 'Cleared'") == [5]
# > ALL (not supported by SQLite): checked in Python, and equal to > MAX for a non-empty, NULL-free subquery
_ret = [r[2] for r in CHQ if r[3] == "Returned"]
ALL_ROWS = [r[0] for r in CHQ if all(r[2] > x for x in _ret)]
assert ALL_ROWS == ["C104", "C107"] and ALL_ROWS == col(
    "SELECT chq_no FROM Cheques WHERE amount > (SELECT MAX(amount) FROM Cheques WHERE status = 'Returned') "
    "ORDER BY chq_no")
assert [r[0] for r in CHQ if any(r[2] > x for x in _ret)] == ["C101", "C102", "C103", "C104", "C105", "C107",
                                                               "C108"]
LAG = dict(db.execute("SELECT chq_no, amount - LAG(amount) OVER (PARTITION BY acc_no ORDER BY presented_on, "
                      "chq_no) FROM Cheques").fetchall())
assert LAG["C108"] == 28000 and LAG["C101"] is None and LAG["C103"] == -13000
cur = db.execute("UPDATE Cheques SET status = 'Cleared' WHERE status = 'Pending'")
assert cur.rowcount == 2
db.rollback()

# 9. Excel gold-loan register
GL = [("asha MENON", "Pune", dt.date(2026, 8, 14), 40, 22),
      ("anil d'cruz", "Delhi", dt.date(2026, 8, 31), 18, 18),
      ("RAVI shankar", "Agra", dt.date(2026, 9, 10), 25, 20),
      ("meena iyer", "Pune", dt.date(2026, 9, 30), 32, 24),
      ("john mathew", "Delhi", dt.date(2026, 10, 19), 12, 22),
      ("farah khan", "Agra", dt.date(2026, 11, 5), 50, 18)]
RATE = {18: 4800, 20: 5300, 22: 5900, 24: 6400}


def proper(s):
    out, prev_letter = [], False
    for ch in s:
        out.append(ch.upper() if not prev_letter else ch.lower()) if ch.isalpha() else out.append(ch)
        prev_letter = ch.isalpha()
    return "".join(out)


assert proper("2-way street") == "2-Way Street"  # Microsoft's own example
assert proper(GL[1][0]) == "Anil D'Cruz"


def eomonth(d, m):
    y, mo = d.year + (d.month - 1 + m) // 12, (d.month - 1 + m) % 12 + 1
    return dt.date(y + mo // 12, mo % 12 + 1, 1) - dt.timedelta(days=1)


assert eomonth(dt.date(2011, 1, 1), 1) == dt.date(2011, 2, 28) and eomonth(dt.date(2011, 1, 1), -3) == \
    dt.date(2010, 10, 31)  # Microsoft's own examples
assert eomonth(GL[0][2], 3) == dt.date(2026, 11, 30) and eomonth(GL[0][2], 2) == dt.date(2026, 10, 31)
assert GL[2][3] * RATE[GL[2][4]] == 132500 and GL[2][3] * RATE[22] == 147500 and GL[2][3] * RATE[18] == 120000


def datedif_m(a, b):
    return (b.year - a.year) * 12 + b.month - a.month - (1 if b.day < a.day else 0)


assert datedif_m(GL[0][2], GL[5][2]) == 2 and (GL[5][2] - GL[0][2]).days == 83 and GL[5][2].month - \
    GL[0][2].month == 3

# ---------------------------------------------------------------- fact-check sources
# Pages opened on 2026-11-05 (web:fact-check)
WIKI_NAPIER = "https://en.wikipedia.org/wiki/Napier%27s_bones"
CENSUS_UNIVAC = ("https://www.census.gov/about/history/bureau-history/census-innovations/technology/univac-i.html")
WIKI_PARAM = "https://en.wikipedia.org/wiki/PARAM"
CERN_WEB = "https://home.cern/science/computing/the-birth-of-the-web/short-history-web/"
DARPA_ARPANET = "https://www.darpa.mil/news/features/arpanet"
GOOGLE_REFINE = "https://support.google.com/websearch/answer/2466433"
RFC1035 = "https://www.rfc-editor.org/rfc/rfc1035"
RFC3596 = "https://www.rfc-editor.org/rfc/rfc3596"
RFC9110 = "https://www.rfc-editor.org/rfc/rfc9110.html"
RFC791 = "https://www.rfc-editor.org/rfc/rfc791"
RFC6335 = "https://www.rfc-editor.org/rfc/rfc6335"
RFC2104 = "https://www.rfc-editor.org/rfc/rfc2104"
RFC8446 = "https://www.rfc-editor.org/rfc/rfc8446"
MDN_SETCOOKIE = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie"
WIKI_MODES = "https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation"
NIST_80038A = "https://csrc.nist.gov/pubs/sp/800/38/a/final"
OWASP_CLICK = "https://community.owasp.org/attacks/Clickjacking"
GNU_WHY_AGPL = "https://www.gnu.org/licenses/why-affero-gpl.html"
LIBREOFFICE = "https://www.libreoffice.org/discover/libreoffice/"
MAN_TOUCH = "https://man7.org/linux/man-pages/man1/touch.1.html"
MAN_INODE = "https://man7.org/linux/man-pages/man7/inode.7.html"
MAN_CHOWN = "https://man7.org/linux/man-pages/man1/chown.1.html"
MAN_WC = "https://man7.org/linux/man-pages/man1/wc.1.html"
MS_GPT = "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-and-gpt-faq"
MS_WIN_KEYS = ("https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-"
               "cb9706c75eec")
MS_WORD_KEYS = ("https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-"
                "f762f663ceb2")
MS_EXCEL_KEYS = ("https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-"
                 "9b7213f0040f")
MS_PPT_KEYS = ("https://support.microsoft.com/en-us/office/use-keyboard-shortcuts-to-create-powerpoint-"
               "presentations-ebb3d20e-dcd4-444f-a38e-bb5c5ed180f4")
MS_PROPER = "https://support.microsoft.com/en-us/office/proper-function-52a5a283-e8b2-49be-8506-b2887b889f94"
MS_EOMONTH = "https://support.microsoft.com/en-us/excel/functions/eomonth-function"
MS_HLOOKUP = "https://support.microsoft.com/en-us/office/hlookup-function-a3034eec-b719-4ba3-bb65-e1ad662ed95f"
MS_DATEDIF = "https://support.microsoft.com/en-us/office/datedif-function-25dba1a4-2812-480b-84dd-8b32a451b35c"
IEEE_OUI = "https://standards.ieee.org/products-programs/regauth/oui/"
ICANN_WHAT = "https://www.icann.org/resources/pages/what-2012-02-25-en"
IBM_EBCDIC = "https://www.ibm.com/docs/SSDTBM_3.2.0/com.ibm.gddm.v3r2.adms700/adms7a05158.htm"
RBI_NEFT_FAQ = "https://www.rbi.org.in/Scripts/FAQView.aspx?Id=60"
RBI_PPS = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=11969"
RBI_CHEQUE_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=3878"
RBI_PPI_FAQ = "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=2812"

# ================================================================ 1. Computer Fundamentals (3 / 6 / 1)
T = "Computer Fundamentals"
S_WORD = new_stim(
    "input_output", "Status word of a note-sorting machine",
    "A currency note-sorting machine in a cash-processing centre reports its state to the controller as one 16-bit "
    "status word, shown in hexadecimal. The bits are numbered 15 (leftmost) to 0 (rightmost):\n\n"
    "| Bits | Field | Meaning |\n|---|---|---|\n| 15-13 | Mode | 3-bit operating mode |\n"
    "| 12-5 | Count | 8-bit unsigned number of notes in the current bundle |\n| 4-0 | Error | 5-bit error code |\n\n"
    "The status word received at 10:42 is **9C5A** (hexadecimal).",
    "9C5A = 1001 1100 0101 1010 in binary. Mode = bits 15-13 = 100 = 4; Count = bits 12-5 = 1110 0010 = 226; "
    "Error = bits 4-0 = 11010 = 26. As an unsigned number the word is 40,026, which is 116132 in octal. Rotating "
    "the word left by 4 bits moves the leading hex digit 9 to the end: C5A9.")
o, a = ordered(W, [W - 0x2000, W + 0x300, W - 144], fmt=lambda v: f"{v:,}")
Q(T, "Number systems", "Intermediate",
  "Refer to the note-sorting machine. What is the status word 9C5A when it is read as one unsigned decimal "
  "number?", o, a,
  concept="Hexadecimal to decimal conversion",
  explanation="Multiply each hex digit by its place value (powers of 16): 9 x 4096 + 12 x 256 + 5 x 16 + 10 x 1 = "
              "36,864 + 3,072 + 80 + 10 = 40,026.",
  steps=["9 x 16^3 = 36,864", "C = 12; 12 x 16^2 = 3,072", "5 x 16 = 80", "A = 10", "Sum = 40,026"],
  shortcut="Work left to right: ((9 x 16 + 12) x 16 + 5) x 16 + 10 = 40,026.",
  wrong="The other values come from slips in the place values or in the values of the letter digits C and A.",
  seconds=60, computed=True, stim=S_WORD, pos=1)
assert 9 * 4096 + 12 * 256 + 5 * 16 + 10 == W
o, a = ordered(COUNT, [197, 90, 113], fmt=str)
Q(T, "Number systems", "Intermediate",
  "Refer to the note-sorting machine. How many notes does the Count field (bits 12-5) report?", o, a,
  concept="Extracting a bit field",
  explanation="9C5A = 1001 1100 0101 1010. Bits 15-13 are 100 (Mode) and bits 4-0 are 11010 (Error); the eight "
              "bits in between, bits 12 to 5, are 1110 0010 = 128 + 64 + 32 + 2 = 226. (In code: (word >> 5) AND "
              "FF.)",
  steps=["Binary: 1001 1100 0101 1010", "Shift right by 5 (drop the Error bits): 100 1110 0010",
         "Keep the low 8 bits: 1110 0010", "= 226"],
  wrong="197 is C5, the middle two hex digits, which do not line up with bits 12-5. 90 is 5A, the lowest byte. "
        "113 is the field taken one place too far left (bits 13-6).", seconds=75, computed=True, stim=S_WORD, pos=2)
assert (W >> 6) & 0xFF == 113
o = ["116132", "116232", "470550", "9C5A"]
Q(T, "Number systems", "Intermediate",
  "Refer to the note-sorting machine. A legacy log prints the status word in octal (base 8). What does it print "
  "for 9C5A?", o,
  concept="Hexadecimal to octal through binary",
  explanation="Write the word in binary and regroup into 3-bit groups from the right: 1 001 110 001 011 010 -> 1 1 "
              "6 1 3 2 = 116132 (octal). Check: 1 x 32768 + 1 x 4096 + 6 x 512 + 1 x 64 + 3 x 8 + 2 = 40,026.",
  steps=["9C5A = 1001 1100 0101 1010", "Group in threes from the right: 1 001 110 001 011 010",
         "Digits: 1 1 6 1 3 2", "Octal 116132"],
  shortcut="Hex -> binary -> octal by regrouping 4-bit groups into 3-bit groups.",
  wrong="116232 misreads one group (001 as 010). 470550 groups the bits in threes from the LEFT instead of the right. "
        "9C5A is the hexadecimal form, and C and A are not octal digits.", seconds=75, computed=True,
  stim=S_WORD, pos=3)
assert int("116232", 8) != W and "".join(str(int(WBIN[i:i + 3], 2)) for i in range(0, 16, 3)) == "470550"
o = ["C5A9", "C5A0", "09C5", "A9C5"]
Q(T, "Number systems", "Advanced",
  "Refer to the note-sorting machine. The controller ROTATES the 16-bit word 9C5A LEFT by 4 bit positions (a "
  "circular shift: bits leaving on the left re-enter on the right). What is the result in hexadecimal?", o,
  concept="Circular (rotate) shift versus logical shift",
  explanation="Rotating a 16-bit word left by 4 bits moves each hex digit one place left, and the leading digit 9 "
              "wraps round to the right end: 9C5A -> C5A9. A logical left shift would instead fill the right end "
              "with zeros (C5A0).",
  steps=["4 bits = 1 hex digit", "Digits move one place left: C 5 A _", "The 9 that left on the left re-enters: C5A9"],
  shortcut="Rotate by 4 bits = rotate the hex digits by one place.",
  wrong="C5A0 is a logical left shift (zeros enter). 09C5 is a logical right shift by 4. A9C5 is a rotation to the "
        "RIGHT by 4 bits.", seconds=60, computed=True, stim=S_WORD, pos=4)
Q(T, "Number systems", "Basic",
  "A value is written in octal (base 8) as 17. What is its value in decimal?", ["15", "17", "8", "23"],
  concept="Octal to decimal",
  explanation="In base 8 the place values are 8 and 1: 1 x 8 + 7 x 1 = 15.",
  steps=["17 (octal) = 1 x 8 + 7", "= 15"],
  wrong="17 reads the digits as if they were decimal. 8 just adds the digits 1 + 7. 23 uses 16 as the place value "
        "of the first digit (that would be hexadecimal 17).", seconds=15, computed=True)
assert int("17", 8) == 15 and int("17", 16) == 23
o = ["(111111) base 2", "(3E) base 16", "(75) base 8", "(60) base 10"]
Q(T, "Number systems", "Intermediate",
  "A test asks which of these four values is the LARGEST. Which one is it?", o,
  concept="Comparing numbers written in different bases",
  explanation="Convert all to decimal: (111111)2 = 63, (3E)16 = 3 x 16 + 14 = 62, (75)8 = 7 x 8 + 5 = 61 and "
              "(60)10 = 60. The largest is (111111)2 = 63.",
  steps=["111111 (2) = 64 - 1 = 63", "3E (16) = 62", "75 (8) = 61", "60 (10) = 60"],
  shortcut="Six binary 1s = 2^6 - 1 = 63.",
  wrong="3E is 62, 75 octal is 61 and 60 decimal is 60, all smaller than 63.", seconds=45, computed=True)
Q(T, "Generations and history", "Basic",
  "In 1617 the Scottish mathematician John Napier published a manually operated calculating aid made of numbered "
  "rods, used to work out products and quotients. What is this device called?",
  ["Napier's bones", "Pascaline", "Difference Engine", "Abacus"],
  concept="Early calculating devices",
  explanation="Napier's bones are a set of numbered rods laid side by side so that multiplication can be done by "
              "adding the digits shown, and division by repeated steps. Napier published them in 1617.",
  steps=["John Napier, 1617, rods for products and quotients -> Napier's bones"],
  wrong="The Pascaline was Blaise Pascal's geared adding machine (1640s). The Difference Engine was Charles "
        "Babbage's design for tabulating polynomials. The abacus is an ancient bead frame, not Napier's invention.",
  seconds=15,
  facts=[fact("Napier's bones is a manually operated calculating device created by John Napier of Merchiston for "
              "the calculation of products and quotients; Napier published his version in 1617.", WIKI_NAPIER)])
Q(T, "Types of computers", "Basic",
  "The PCs, ATMs and mobile phones used by a bank all represent data as discrete binary values (0s and 1s) and "
  "process them by counting rather than by measuring a continuous quantity. On the basis of how they work, such "
  "computers are classified as:",
  ["Digital computers", "Analog computers", "Hybrid computers", "Optical computers"],
  concept="Classification by working principle",
  explanation="Computers are classified as analog (measure continuously varying quantities), digital (work with "
              "discrete digits, in practice binary) or hybrid (combine both). Everyday PCs, ATMs and phones are "
              "digital computers.",
  steps=["Discrete 0s and 1s, counting -> digital"],
  wrong="Analog computers measure continuous quantities such as voltage. Hybrid computers combine analog and digital "
        "parts. Optical computing is a research area, not the class of these devices.", seconds=15)
Q(T, "Generations and history", "Intermediate",
  "The US Census Bureau signed a contract for a computer in March 1951 and held its dedication ceremony in June "
  "1951; the Bureau describes it as the first successful civilian computer. Which computer was it?",
  ["UNIVAC I", "ENIAC", "EDSAC", "IBM 701"],
  concept="First-generation commercial computers",
  explanation="UNIVAC I (Universal Automatic Computer), built by the company of J. Presper Eckert and John Mauchly, "
              "went to the US Census Bureau in 1951 and became the first successful civilian (commercial) computer "
              "in the United States. Like other first-generation machines it used vacuum tubes.",
  steps=["Census Bureau, 1951, first successful civilian computer -> UNIVAC I"],
  wrong="ENIAC (1945) was built for the US Army's ballistics work. EDSAC (1949) was a stored-program computer at "
        "Cambridge University. The IBM 701 was IBM's first commercial scientific computer, not the Census Bureau's "
        "1951 machine.", seconds=20,
  facts=[fact("The Census Bureau signed a contract for UNIVAC I on 31 March 1951, held a dedication in June 1951 "
              "and calls it the first successful civilian computer.", CENSUS_UNIVAC)])
Q(T, "Types of computers", "Intermediate",
  "Which machine, built from scratch by C-DAC and delivered in 1991, was the first of the PARAM series and is "
  "remembered as India's first indigenous supercomputer?",
  ["PARAM 8000", "PARAM Padma", "PARAM Yuva", "PARAM Siddhi-AI"],
  concept="Supercomputers in India",
  explanation="C-DAC was set up in 1988 to build an indigenous supercomputer. The PARAM 8000, a parallel machine "
              "built from transputers, was delivered in 1991 and was the first machine of the PARAM series.",
  steps=["First PARAM, 1991 -> PARAM 8000"],
  wrong="PARAM Padma (2002), PARAM Yuva and PARAM Siddhi-AI are later machines of the series.", seconds=20,
  facts=[fact("Wikipedia's PARAM article: the PARAM 8000 was the first machine in the series and was built from "
              "scratch; a 64-node machine was delivered in August 1991; its cited C-DAC item says this gave India "
              "her first indigenous supercomputer in 1991.", WIKI_PARAM)])

# ================================================================ 2. Hardware (2 / 2 / 3)
T = "Hardware"
S_CPU = new_stim(
    "input_output", "Program on a teaching accumulator processor",
    "A bank's IT training lab uses a simple processor with one register for data, the accumulator (ACC), and a "
    "program counter (PC) that always holds the address of the NEXT instruction to fetch. Each instruction occupies "
    "one memory word and is fetched with ONE memory access. LOAD, SUB and STORE each make ONE further memory access "
    "for their data; JUMPNEG and HALT make none.\n\n"
    "| Address | Instruction | Meaning |\n|---|---|---|\n| 100 | LOAD 200 | ACC <- contents of address 200 |\n"
    "| 101 | SUB 201 | ACC <- ACC - contents of address 201 |\n"
    "| 102 | JUMPNEG 106 | If ACC < 0, continue at address 106 |\n| 103 | LOAD 200 | ACC <- contents of 200 |\n"
    "| 104 | STORE 202 | Contents of 202 <- ACC |\n| 105 | HALT | Stop |\n| 106 | LOAD 201 | ACC <- contents of 201 |\n"
    "| 107 | STORE 202 | Contents of 202 <- ACC |\n| 108 | HALT | Stop |\n\n"
    "Before the run, address 200 holds 45, address 201 holds 60 and address 202 holds 0. Execution starts at 100.",
    "45 - 60 = -15 is negative, so the jump is taken: the instructions run are 100, 101, 102, 106, 107 and 108, and "
    "60 is stored in 202. The program stores the larger of the two numbers. Memory accesses = 6 instruction fetches + "
    "4 data accesses (LOAD, SUB, LOAD, STORE) = 10.")
o, a = ordered(PCA[102], [103, 102, 107], fmt=str)
Q(T, "CPU and components", "Intermediate",
  "Refer to the accumulator processor. What does the program counter hold immediately after the JUMPNEG "
  "instruction at address 102 has finished executing?", o, a,
  concept="Program counter and conditional jumps",
  explanation="During the fetch of the instruction at 102 the PC is advanced to 103. ACC holds 45 - 60 = -15, which "
              "is negative, so JUMPNEG overwrites the PC with its target 106. The next instruction fetched is "
              "therefore at 106.",
  steps=["After fetch: PC = 103", "ACC = -15 < 0 -> jump taken", "PC <- 106"],
  wrong="103 would be the PC if the jump were not taken. 102 is the address of the jump itself. 107 is one "
        "instruction too far: the PC points to the next instruction to fetch, which is 106.", seconds=45,
  computed=True, stim=S_CPU, pos=1)
o, a = ordered(M1[202], [-15, 45, 15], fmt=str)
Q(T, "CPU and components", "Advanced",
  "Refer to the accumulator processor. When the program halts, what value is stored at address 202?", o, a,
  concept="Tracing a machine-level program",
  explanation="LOAD 200 puts 45 in ACC; SUB 201 makes it 45 - 60 = -15; the result is negative, so control jumps "
              "to 106, where LOAD 201 puts 60 in ACC and STORE 202 writes 60 to address 202. The program stores the "
              "larger of the two numbers.",
  steps=["ACC = 45", "ACC = 45 - 60 = -15", "Negative -> jump to 106", "ACC = 60", "M[202] = 60"],
  wrong="-15 is the difference, which is never stored. 45 would be stored only if the jump were not taken. 15 is "
        "the size of the difference.", seconds=60, computed=True, stim=S_CPU, pos=2)
o, a = ordered(F1 + D1, [6, 4, 9], fmt=str)
Q(T, "CPU and components", "Advanced",
  "Refer to the accumulator processor. Counting both instruction fetches and data accesses, how many memory "
  "accesses does the whole run make, up to and including the HALT that stops it?", o, a,
  concept="Instruction cycle: fetch and operand accesses",
  explanation="Six instructions run (100, 101, 102, 106, 107, 108), each needing one fetch = 6 accesses. Of these, "
              "LOAD 200, SUB 201, LOAD 201 and STORE 202 each make one data access = 4. Total = 10.",
  steps=["Instructions executed: 100, 101, 102, 106, 107, 108 = 6 fetches",
         "Data accesses: LOAD, SUB, LOAD, STORE = 4", "Total = 10"],
  wrong="6 counts only the fetches and 4 only the data accesses. 9 forgets the fetch of the final HALT.",
  seconds=75, computed=True, stim=S_CPU, pos=3)
o = ["75, because the program now reloads 75 and stores it", "15, the difference 75 - 60",
     "60, because address 201 is always stored", "0, because the program halts before any STORE"]
Q(T, "CPU and components", "Advanced",
  "Refer to the accumulator processor. If address 200 held 75 instead of 45 (address 201 still holds 60), what "
  "would address 202 hold when the program halts?", o,
  concept="Tracing the not-taken branch",
  explanation="75 - 60 = 15 is not negative, so JUMPNEG does not jump. Execution continues at 103: LOAD 200 puts 75 "
              "back into ACC, STORE 202 writes 75 and HALT at 105 stops the run. In both cases the program stores "
              "the larger of the two numbers.",
  steps=["ACC = 75 - 60 = 15 (not negative)", "No jump: 103 LOAD 200 -> ACC = 75", "104 STORE 202 -> 75",
         "105 HALT"],
  wrong="15 would be stored only if there were no LOAD at 103 to reload the original value. 60 is stored only on "
        "the jump path. A STORE does run (at 104) before the HALT.", seconds=60, computed=True, stim=S_CPU, pos=4)
assert M2[202] == 75
Q(T, "Motherboard and ports", "Basic",
  "An old dot-matrix printer in a branch has a wide 25-pin connector and was designed for the PC port that sends "
  "8 bits at a time over separate wires, often called the LPT port. Which port is this?",
  ["Parallel port", "Serial (COM) port", "PS/2 port", "HDMI port"],
  concept="Legacy PC ports",
  explanation="The parallel (LPT, Centronics) port sends the 8 bits of a byte simultaneously over 8 data wires and "
              "was the standard printer port before USB. A serial (COM) port sends bits one after another.",
  steps=["8 bits at a time, printer, LPT -> parallel port"],
  wrong="A serial port sends one bit at a time. PS/2 is a small round port for keyboards and mice. HDMI carries "
        "digital video and audio.", seconds=15)
Q(T, "Motherboard and ports", "Basic",
  "A technician building desktops for a bank buys a cabinet, a power supply and a motherboard that all follow the "
  "same standard, so that the board's mounting holes, rear connector panel and power connectors fit together. "
  "What is this standard size and layout of a motherboard called?",
  ["Form factor (for example ATX)", "Chipset", "Socket type", "Bus width"],
  concept="Motherboard form factors",
  explanation="A form factor such as ATX, micro-ATX or mini-ITX fixes the board's dimensions, mounting-hole "
              "positions, rear I/O panel position and power connectors, so that compatible cases and power supplies "
              "fit.",
  steps=["Physical size and layout standard -> form factor"],
  wrong="The chipset controls data flow between components. The socket type decides which processors fit. Bus "
        "width is the number of bits a bus carries at once.", seconds=20)
Q(T, "CPU and components", "Intermediate",
  "To make a trading-desk PC faster, a technician sets its processor to run above the clock speed at which the "
  "manufacturer rated it, which increases heat and can make the system unstable. What is this practice called?",
  ["Overclocking", "Thermal throttling", "Hyper-threading", "Pipelining"],
  concept="Clock speed and overclocking",
  explanation="Overclocking runs a component such as the CPU or RAM above its rated clock frequency to gain speed, "
              "at the cost of more heat, more power use and possible instability.",
  steps=["Above rated clock speed -> overclocking"],
  wrong="Thermal throttling is the opposite: the processor lowers its own speed when it gets too hot. "
        "Hyper-threading runs two threads per core. Pipelining overlaps the stages of several instructions.",
  seconds=20)

# ================================================================ 3. Software (1 / 2 / 3)
T = "Software"
Q(T, "Licensing", "Basic",
  "A small branch office wants a word processor, spreadsheet and presentation program that can be used legally "
  "at no cost and whose source code anyone may study and improve. Which suite fits this need?",
  ["LibreOffice (free and open-source software)", "Microsoft 365 (subscription software)",
   "A 30-day trial version of a paid office suite (shareware)", "A cracked copy of a paid office suite"],
  concept="Free and open-source software",
  explanation="LibreOffice is free and open-source software: it costs nothing and its source code can be studied "
              "and improved by anyone. It includes Writer (word processor), Calc (spreadsheet) and Impress "
              "(presentations).",
  steps=["No cost + source open to study and improve -> open-source suite such as LibreOffice"],
  wrong="Microsoft 365 is proprietary and paid by subscription. A trial version must be bought after the trial. "
        "A cracked copy is pirated software and illegal.", seconds=20,
  facts=[fact("LibreOffice describes itself as free and open source software, so anyone can study how it works and "
              "add improvements; it includes Writer, Calc and Impress.", LIBREOFFICE)])
Q(T, "Licensing", "Intermediate",
  "A bank pays a fixed fee every year for each officer who uses an analytics tool. If the bank stops paying, the "
  "officers lose the right to use it, but while it pays it always gets the latest version. What type of licence "
  "is this?",
  ["Subscription licence", "Perpetual licence", "Freeware licence", "Public domain dedication"],
  concept="Software licensing models",
  explanation="Under a subscription licence the customer pays a recurring (monthly or yearly) fee for the right to "
              "use the software, usually with updates included; the right ends when the payments stop.",
  steps=["Recurring fee + rights end when payment stops -> subscription"],
  wrong="A perpetual licence is paid for once and the bought version may be used for ever. Freeware costs nothing. "
        "Public domain software has no copyright restrictions at all.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "A trainee says, 'I programmed the branch's web page in HTML.' His trainer points out that HTML is not a "
  "programming language. Why?",
  ["HTML is a markup language: its tags describe the structure of content, and it has no variables, conditions or "
   "loops of its own",
   "HTML can only be run after it is compiled into machine code by the browser's compiler",
   "HTML is an assembly language for the browser's processor",
   "HTML is a database query language like SQL"],
  concept="Markup languages versus programming languages",
  explanation="HTML (HyperText Markup Language) marks up content with tags such as <h1>, <p> and <table> to show "
              "its structure. It cannot by itself make decisions, repeat steps or calculate; logic on a web page "
              "comes from a programming language such as JavaScript.",
  steps=["HTML = HyperText Markup Language", "Tags describe structure; no logic of its own"],
  wrong="Browsers parse HTML; they do not compile it into machine code. HTML is not an assembly language. It is "
        "not a query language either.", seconds=30)
o = ["500 with pass by value; 600 with pass by reference", "600 with pass by value; 500 with pass by reference",
     "500 in both cases", "600 in both cases"]
Q(T, "Programming languages", "Advanced",
  "Consider this pseudocode:\n\nprocedure addBonus(x)\n    x = x + 100\nend procedure\n\nb = 500\naddBonus(b)\n"
  "print b\n\nWhat is printed if the parameter is passed BY VALUE, and what if it is passed BY REFERENCE?", o,
  concept="Parameter passing: by value and by reference",
  explanation="With pass by value, x is a separate copy of b; changing x to 600 does not affect b, so 500 is "
              "printed. With pass by reference, x is another name for b itself, so the change makes b = 600 and 600 "
              "is printed.",
  steps=["By value: x is a copy -> b stays 500", "By reference: x refers to b -> b becomes 600"],
  wrong="The second option swaps the two mechanisms. The last two options ignore the difference between a copy and "
        "a reference.", seconds=45, computed=True)
_b = 500
_x = _b
_x += 100
assert _b == 500 and _x == 600
o = ["The condition is simply false and no division is performed, because count != 0 is false and AND stops there",
     "The program crashes with a division-by-zero error",
     "The condition is true, because total / 0 is treated as infinity",
     "The compiler rejects the statement because it may divide by zero"]
Q(T, "Programming languages", "Advanced",
  "In a language that uses short-circuit evaluation for AND, a program runs:\n\nif count != 0 AND total / count > "
  "1000 then\n    print \"High average\"\nend if\n\nwith count = 0 and total = 50000. What happens?", o,
  concept="Short-circuit evaluation",
  explanation="With short-circuit AND, the right-hand operand is evaluated only when the left-hand operand is true. "
              "Here count != 0 is false, so the whole condition is false and total / count is never computed; "
              "nothing is printed and no error occurs. This is why the zero check is written first.",
  steps=["Left operand: count != 0 -> false", "AND with false is false -> stop", "Division never runs"],
  wrong="A crash would happen only if both operands were always evaluated. Division by zero is not treated as "
        "infinity in integer arithmetic, and it is never reached here. A compiler cannot know the run-time value of "
        "count, so it does not reject the statement.", seconds=45)
Q(T, "Licensing", "Advanced",
  "A fintech company modifies an open-source loan-calculator program licensed under the GNU Affero GPL (AGPL) and "
  "runs it on its own server, where customers use it through a web browser; the company never hands out copies of "
  "the program. What does the AGPL require?",
  ["Users who interact with the modified program over the network must be able to get its modified source code",
   "Nothing, because the program is never distributed as a copy",
   "Only the original author's copyright notice must be kept, as with the MIT licence",
   "The company must pay a royalty to the Free Software Foundation"],
  concept="Copyleft licences and network use",
  explanation="Ordinary GPL obligations are triggered by distributing copies, so a program that only runs on a "
              "server escapes them. The AGPL closes this gap: if you run a modified version on a server and let "
              "users interact with it there, the server must also let them download the corresponding source code.",
  steps=["Modified AGPL program + users interact over a network", "-> offer them the modified source"],
  wrong="'Nothing' describes the plain GPL server loophole that the AGPL was written to close. Keeping only a "
        "copyright notice is the permissive MIT model. Free-software licences do not charge royalties.", seconds=40,
  facts=[fact("The FSF explains that the AGPL adds one requirement to GPLv3: if you run a modified program on a "
              "server and let other users communicate with it there, your server must also allow them to download "
              "the source code of the modified version.", GNU_WHY_AGPL)])

# ================================================================ 4. Operating Systems (3 / 4 / 3)
T = "Operating Systems"
S_JOBS = new_stim(
    "data_table", "Overnight batch jobs on an end-of-day server",
    "A bank's end-of-day (EOD) server has one CPU and runs four batch jobs. Times are in minutes after the batch "
    "window opens. A SMALLER priority number means a HIGHER priority. A job's turnaround time = completion time - "
    "arrival time; its waiting time = turnaround time - burst time. Ignore context-switch time.\n\n"
    "| Job | Task | Arrival time | CPU burst | Priority |\n|---|---|---|---|---|\n"
    "| J1 | Interest posting | 0 | 8 | 3 |\n| J2 | ATM cash reconciliation | 1 | 4 | 1 |\n"
    "| J3 | Statement generation | 2 | 9 | 4 |\n| J4 | Loan EMI debit | 3 | 5 | 2 |",
    "Non-preemptive priority: J1 runs 0-8 (only job present at 0), then J2 8-12, J4 12-17, J3 17-26; turnaround "
    "times 8, 11, 24 and 14, average 14.25 minutes. Preemptive priority: J1 0-1, J2 1-5, J4 5-10, J1 10-17, J3 "
    "17-26; waiting times J1 9, J2 0, J3 15, J4 2, average 6.5 minutes.")
o = ["J1, J2, J4, J3", "J2, J4, J1, J3", "J1, J2, J3, J4", "J2, J1, J4, J3"]
Q(T, "Functions", "Intermediate",
  "Refer to the EOD batch jobs. Under NON-preemptive priority scheduling, in what order do the jobs complete?", o,
  concept="Non-preemptive priority scheduling",
  explanation="At time 0 only J1 has arrived, so it starts and, being non-preemptive, runs to completion at 8. By "
              "then J2 (priority 1), J3 (4) and J4 (2) are all waiting; the highest priority, J2, runs 8-12, then J4 "
              "12-17, then J3 17-26.",
  steps=["t = 0: only J1 -> J1 runs 0-8", "t = 8: J2 (1), J4 (2), J3 (4) waiting", "J2 8-12, J4 12-17, J3 17-26"],
  wrong="J2, J4, J1, J3 is the preemptive order (J2 interrupts J1). J1, J2, J3, J4 is first-come, first-served. "
        "J2, J1, J4, J3 assumes J2 was present at time 0.", seconds=60, computed=True, stim=S_JOBS, pos=1)
assert ORDER == ["J1", "J2", "J4", "J3"]
o, a = ordered(14.25, [15.75, 7.75, 13.0], fmt=lambda v: f"{v:g} minutes")
Q(T, "Functions", "Advanced",
  "Refer to the EOD batch jobs. Under NON-preemptive priority scheduling, what is the average turnaround time?",
  o, a,
  concept="Turnaround time",
  explanation="Completion times: J1 8, J2 12, J4 17, J3 26. Turnaround = completion - arrival: J1 8 - 0 = 8, J2 "
              "12 - 1 = 11, J4 17 - 3 = 14, J3 26 - 2 = 24. Average = (8 + 11 + 14 + 24) / 4 = 57 / 4 = 14.25 "
              "minutes.",
  steps=["Completion: 8, 12, 17, 26", "Turnaround: 8, 11, 14, 24", "Sum 57 / 4 = 14.25"],
  wrong="15.75 averages the completion times without subtracting arrival times. 7.75 is the average WAITING time "
        "under this schedule. 13 is the average turnaround under PREEMPTIVE priority.", seconds=90, computed=True,
  stim=S_JOBS, pos=2)
o, a = ordered(6.5, [7.75, 4.0, 9.0], fmt=lambda v: f"{v:g} minutes")
Q(T, "Functions", "Advanced",
  "Refer to the EOD batch jobs. If the scheduler is changed to PREEMPTIVE priority (a newly arrived job with a "
  "higher priority immediately takes the CPU from the running job), what is the average waiting time?", o, a,
  concept="Preemptive priority scheduling",
  explanation="J1 runs 0-1; J2 arrives at 1 with priority 1 and preempts it, running 1-5. At 5, J4 (priority 2) "
              "beats J1 (3) and J3 (4): J4 runs 5-10. J1 finishes its remaining 7 minutes 10-17, then J3 runs 17-26. "
              "Waiting = completion - arrival - burst: J1 17 - 0 - 8 = 9, J2 5 - 1 - 4 = 0, J4 10 - 3 - 5 = 2, J3 26 "
              "- 2 - 9 = 15. Average = 26 / 4 = 6.5 minutes.",
  steps=["Gantt: J1 0-1, J2 1-5, J4 5-10, J1 10-17, J3 17-26", "Waiting: 9, 0, 2, 15", "26 / 4 = 6.5"],
  wrong="7.75 is the average waiting time WITHOUT preemption. 4 and 9 come from leaving out a job's waiting time or "
        "counting J1's wait as only 1 minute.", seconds=120, computed=True, stim=S_JOBS, pos=3)
Q(T, "Windows and Linux basics", "Basic",
  "A clerk copied several account numbers one after another and now wants to paste one she copied earlier, not "
  "the latest one. Which Windows keyboard shortcut opens the clipboard history so she can choose it?",
  ["Windows logo key + V", "Ctrl + V", "Windows logo key + C", "Ctrl + Shift + C"],
  concept="Windows keyboard shortcuts",
  explanation="Windows logo key + V opens the clipboard history (the first time, Windows asks you to turn it on), "
              "from which any of the recently copied items can be pasted. Ctrl + V pastes only the latest item.",
  steps=["Clipboard history -> Windows logo key + V"],
  wrong="Ctrl + V pastes only the most recent item. Windows logo key + C and Ctrl + Shift + C do not open the "
        "clipboard history.", seconds=15,
  facts=[fact("Microsoft lists Windows logo key + V as 'Open the clipboard history'.", MS_WIN_KEYS)])
Q(T, "Windows and Linux basics", "Basic",
  "On a Linux server, an officer wants to create a new, empty file named audit.log in the current directory. "
  "Which command does this when the file does not yet exist?",
  ["touch audit.log", "mkdir audit.log", "rm audit.log", "pwd audit.log"],
  concept="Basic Linux commands",
  explanation="touch updates a file's access and modification times; if the named file does not exist, it creates "
              "it as an empty file.",
  steps=["touch <file> -> creates an empty file if missing"],
  wrong="mkdir creates a directory, not a file. rm deletes files. pwd prints the current directory and takes no "
        "file name.", seconds=15,
  facts=[fact("touch: 'A FILE argument that does not exist is created empty, unless -c or -h is supplied.'",
              MAN_TOUCH)])
Q(T, "Windows and Linux basics", "Basic",
  "Most smartphones on which customers use mobile-banking apps run an operating system developed by Google that "
  "is built on the Linux kernel. Which operating system is it?",
  ["Android", "iOS", "Windows", "macOS"],
  concept="Mobile operating systems",
  explanation="Android, developed by Google, is a mobile operating system based on the Linux kernel and is used on "
              "most smartphones.",
  steps=["Google + Linux kernel + phones -> Android"],
  wrong="iOS is Apple's iPhone operating system. Windows and macOS are desktop operating systems from Microsoft and "
        "Apple.", seconds=10)
Q(T, "Windows and Linux basics", "Intermediate",
  "On a Linux server, the file recon.csv belongs to user asha, but it must now be handed over to user ravi, who "
  "takes over the reconciliation work. Which command changes the file's owner?",
  ["chown ravi recon.csv", "chmod ravi recon.csv", "mv recon.csv ravi", "su ravi recon.csv"],
  concept="File ownership in Linux",
  explanation="chown changes the user and/or group ownership of files: chown ravi recon.csv makes ravi the owner "
              "(normally run by root or with sudo).",
  steps=["Change owner -> chown <user> <file>"],
  wrong="chmod changes permission bits, not the owner. mv renames or moves the file (here to a file named ravi). su "
        "switches the user of the shell session.", seconds=20,
  facts=[fact("chown changes the user and/or group ownership of each given file.", MAN_CHOWN)])
Q(T, "Windows and Linux basics", "Intermediate",
  "A Linux administrator wants to know how many lines of the log file app.log contain the word FAILED. Which "
  "command line prints just that number?",
  ["grep FAILED app.log | wc -l", "grep FAILED app.log > wc -l", "wc -l app.log | grep FAILED",
   "cat app.log | wc -w FAILED"],
  concept="Pipes and filters",
  explanation="grep prints only the lines that contain FAILED; the pipe | sends that output to wc -l, which counts "
              "newlines, that is, the number of matching lines.",
  steps=["grep FAILED app.log -> matching lines", "| wc -l -> count those lines"],
  wrong="> redirects grep's output into a file named wc. wc -l app.log counts ALL lines of the file and grep then "
        "searches that count. wc -w counts words and would treat FAILED as a file name.", seconds=30,
  facts=[fact("wc prints newline, word and byte counts; -l, --lines prints the newline counts.", MAN_WC)])
Q(T, "File systems", "Intermediate",
  "A branch server's 4 TB disk must be split into six partitions. The technician notes that the older MBR "
  "partitioning scheme allows only a few partition-table entries, whereas GPT has no such small limit. How many "
  "partition-table entries does an MBR disk support, and what limit does Windows apply to GPT disks?",
  ["MBR: 4 entries (more needs an extended partition); Windows GPT: 128 partitions",
   "MBR: 8 entries; Windows GPT: 64 partitions", "MBR: 26 entries, one per drive letter; GPT: unlimited",
   "MBR: 128 entries; Windows GPT: 4 partitions"],
  concept="MBR and GPT partition tables",
  explanation="An MBR disk has only four partition-table entries; more partitions need an extended partition "
              "divided into logical drives. GPT, introduced with UEFI, allows an almost unlimited number by "
              "specification, but Windows limits it to 128 partitions. GPT also keeps a backup partition table and "
              "CRC32 checks.",
  steps=["MBR: 4 entries", "GPT in Windows: 128 partitions"],
  wrong="The other figures are not the MBR and GPT limits; drive letters have nothing to do with partition-table "
        "entries.", seconds=30,
  facts=[fact("Microsoft: MBR disks support only four partition table entries; for more, an extended partition is "
              "needed. The GPT specification allows an almost unlimited number of partitions, but the Windows "
              "implementation restricts this to 128.", MS_GPT)])
Q(T, "File systems", "Advanced",
  "On a shared Linux server, the directory /srv/upload is writable by all users, but officers must not be able "
  "to delete or rename one another's files in it. The administrator sets the sticky bit on the directory (chmod "
  "+t /srv/upload). What is the effect?",
  ["A file in the directory can be deleted or renamed only by the file's owner, the directory's owner or root",
   "Every file created in the directory automatically runs with its owner's privileges",
   "Files in the directory stay in RAM permanently for faster access",
   "New files in the directory automatically get the directory's group"],
  concept="Special permission bits",
  explanation="On a directory, the sticky bit restricts deletion and renaming: although all users may write into "
              "the directory, a file in it can be renamed or deleted only by the owner of the file, the owner of "
              "the directory or a privileged process. /tmp is set up the same way.",
  steps=["Sticky bit on a directory -> only owners (or root) can delete or rename entries"],
  wrong="Running with the owner's privileges is the setuid bit on an executable file. The old meaning of keeping "
        "program text in memory does not apply to directories on Linux. Inheriting the directory's group is the "
        "setgid bit on a directory.", seconds=40,
  facts=[fact("inode(7): in a directory with the sticky bit set, a file can be renamed or deleted only by the owner "
              "of the file, by the owner of the directory, and by a privileged process.", MAN_INODE)])

# ================================================================ 5. Input and Output Devices (2 / 1 / 1)
T = "Input and Output Devices"
Q(T, "Input devices", "Basic",
  "A cash-counter clerk keys in hundreds of amounts a day. To type digits quickly with one hand, she uses the block "
  "of number keys on the right side of a full-size keyboard, which works as digits only while a certain lock key "
  "is on. What are this block and its lock key called?",
  ["Numeric keypad; Num Lock", "Function keys; Fn Lock", "Arrow keys; Scroll Lock", "Top number row; Caps Lock"],
  concept="Keyboard layout",
  explanation="The numeric keypad on the right of a full-size keyboard is laid out like a calculator for fast "
              "number entry. When Num Lock is on, its keys type digits; when it is off, they act as cursor and "
              "navigation keys.",
  steps=["Calculator-style block on the right -> numeric keypad", "Toggle -> Num Lock"],
  wrong="Function keys are F1 to F12 along the top. Arrow keys move the cursor; Scroll Lock is a different toggle. "
        "Caps Lock affects letters, not the number row.", seconds=15)
Q(T, "Input devices", "Basic",
  "At an enrolment centre, a camera-like device photographs the coloured ring around the pupil of each eye so "
  "that a person can later be identified by it. Which input device is this?",
  ["Iris scanner", "Barcode reader", "Optical Mark Reader", "Light pen"],
  concept="Biometric input devices",
  explanation="An iris scanner captures the unique pattern of the iris (the coloured ring around the pupil) for "
              "biometric identification, alongside fingerprints and face images.",
  steps=["Pattern of the eye's coloured ring -> iris scanner"],
  wrong="A barcode reader reads printed bar patterns. An OMR reads marked bubbles on forms. A light pen points at "
        "or draws on a screen.", seconds=15)
Q(T, "Output devices", "Intermediate",
  "A talking ATM lets a visually impaired customer plug in headphones and hear the on-screen instructions and his "
  "balance read out. Which output technology converts the text into spoken words?",
  ["Speech synthesis (text-to-speech)", "Speech recognition", "Optical character recognition",
   "Haptic feedback"],
  concept="Audio output",
  explanation="Speech synthesis, or text-to-speech (TTS), produces spoken audio from text and is an OUTPUT "
              "technology. Talking ATMs and screen readers use it.",
  steps=["Text -> spoken words = speech synthesis (output)"],
  wrong="Speech recognition is the reverse: spoken words in, text out (input). OCR turns images of text into text. "
        "Haptic feedback is vibration, not sound.", seconds=20)
o, a = ordered(DOTS // 8, [DOTS, DOTS * 3, DOTS // 64], fmt=lambda v: f"{v:,} bytes")
Q(T, "Output devices", "Advanced",
  "A monochrome laser printer builds each page as a bitmap in its own memory before printing. The printable area "
  "is 8 inches x 10 inches, the resolution is 600 dots per inch in both directions, and each dot needs 1 bit (on "
  "or off). How much printer memory does one full page bitmap need?", o, a,
  concept="Raster page memory",
  explanation="Dots across = 8 x 600 = 4,800 and down = 10 x 600 = 6,000, so 4,800 x 6,000 = 28,800,000 dots. At "
              "1 bit per dot that is 28,800,000 bits = 28,800,000 / 8 = 3,600,000 bytes (about 3.6 MB).",
  steps=["8 x 600 = 4,800 dots", "10 x 600 = 6,000 dots", "4,800 x 6,000 = 28,800,000 bits", "/ 8 = 3,600,000 bytes"],
  wrong="28,800,000 bytes forgets to divide bits by 8. 86,400,000 bytes assumes 24-bit colour per dot. 450,000 "
        "bytes divides by 8 twice.", seconds=75,
  computed=True)
assert DOTS // 64 == 450_000

# ================================================================ 6. Memory (2 / 2 / 2)
T = "Memory"
Q(T, "Primary memory", "Basic",
  "A clerk sends a 40-page statement to a slow printer. The computer quickly places the data in a temporary "
  "memory area, from which the printer takes it at its own speed, so the clerk can continue working. What is "
  "such a temporary holding area called?",
  ["Buffer", "Register", "Virtual memory", "ROM"],
  concept="Buffers",
  explanation="A buffer is a temporary memory area that holds data while it moves between two devices or processes "
              "working at different speeds, such as a computer and a printer.",
  steps=["Temporary hold between fast and slow devices -> buffer"],
  wrong="Registers are tiny storage locations inside the CPU. Virtual memory uses disk space to extend RAM. ROM is "
        "permanent read-only memory.", seconds=15)
Q(T, "Primary memory", "Basic",
  "Main memory (RAM) is divided into millions of storage locations. How does the CPU tell which location it wants "
  "to read or write?",
  ["Each location has a unique number called its memory address", "Each location has a unique file name",
   "The CPU searches all locations for the data it needs", "Each location is identified by its IP address"],
  concept="Memory addressing",
  explanation="Every location (byte) of main memory has a unique numeric address. The CPU puts the address on the "
              "address bus to select that location for reading or writing.",
  steps=["Location identified by a number -> memory address"],
  wrong="File names identify files on storage, not RAM locations. Ordinary RAM is accessed by address, not by "
        "searching its contents. IP addresses identify devices on a network.", seconds=15)
o, a = ordered(92.5, [7.5, 95.0, 85.0], fmt=lambda v: f"{v:g}%")
Q(T, "Cache and units", "Intermediate",
  "During a test run, a processor makes 2,000 memory references; 150 of them are NOT found in the cache. What is "
  "the cache hit ratio?", o, a,
  concept="Cache hit ratio",
  explanation="Hits = 2,000 - 150 = 1,850. Hit ratio = hits / total references = 1,850 / 2,000 = 0.925 = 92.5%.",
  steps=["Hits = 2,000 - 150 = 1,850", "1,850 / 2,000 = 92.5%"],
  wrong="7.5% is the miss ratio. 95% and 85% come from arithmetic slips.", seconds=30, computed=True)
Q(T, "Secondary storage", "Intermediate",
  "SSD flash cells can store 1 bit (SLC), 2 bits (MLC), 3 bits (TLC) or 4 bits (QLC) each. For a server that "
  "rewrites its log data constantly, which cell type generally offers the highest endurance (number of "
  "write/erase cycles), at the highest cost per gigabyte?",
  ["SLC (single-level cell)", "MLC (multi-level cell)", "TLC (triple-level cell)", "QLC (quad-level cell)"],
  concept="NAND flash cell types",
  explanation="An SLC cell has only two charge levels to tell apart, so it tolerates wear best and lasts the most "
              "write/erase cycles; it also stores the fewest bits per cell, which makes it the most expensive per "
              "gigabyte. Endurance falls as more bits are packed into each cell (MLC, TLC, QLC).",
  steps=["Fewer levels per cell -> wider margins -> more cycles", "SLC: highest endurance, highest cost/GB"],
  wrong="MLC, TLC and QLC store more bits per cell, which lowers cost per gigabyte but also lowers endurance; QLC "
        "has the lowest.", seconds=30)
o, a = ordered(1000 % SETS, [232, 0, 15], fmt=str)
Q(T, "Cache and units", "Advanced",
  "A 4-way set-associative cache has 256 lines in all, grouped into sets of 4 lines. A main-memory block is "
  "placed in set number (block number) mod (number of sets), in any free line of that set. Into which set does "
  "block number 1000 go?", o, a,
  concept="Set-associative mapping",
  explanation="Number of sets = 256 / 4 = 64. Set = 1000 mod 64: 64 x 15 = 960 and 1000 - 960 = 40, so the block "
              "goes into set 40 (in any of its 4 lines).",
  steps=["Sets = 256 / 4 = 64", "1000 mod 64 = 40"],
  wrong="232 is 1000 mod 256, the line number in a direct-mapped cache of 256 lines. 0 is 1000 mod 4 (using the "
        "number of ways). 15 is the quotient 1000 / 64, not the remainder.", seconds=60, computed=True)
o, a = ordered(130, [120, 110, 210], fmt=lambda v: f"{v} ns")
Q(T, "Primary memory", "Advanced",
  "A system uses paging with a single-level page table kept in main memory and a TLB (translation lookaside "
  "buffer). A TLB lookup takes 10 ns and a main-memory access 100 ns. On a TLB hit, the address is translated and "
  "memory is accessed once; on a TLB miss, the page table must first be read from memory and then the data. The "
  "TLB hit ratio is 80%. What is the effective memory access time?", o, a,
  concept="Effective access time with a TLB",
  explanation="Hit: 10 + 100 = 110 ns. Miss: 10 (TLB check) + 100 (page-table entry) + 100 (data) = 210 ns. EAT = "
              "0.8 x 110 + 0.2 x 210 = 88 + 42 = 130 ns.",
  steps=["Hit = 110 ns", "Miss = 210 ns", "0.8 x 110 + 0.2 x 210 = 130 ns"],
  wrong="120 ns leaves out the 10 ns TLB lookup. 110 ns is the hit time only. 210 ns is the miss time only.",
  seconds=75, computed=True)

# ================================================================ 7. Internet (3 / 6 / 3)
T = "Internet"
S_DNS = new_stim(
    "data_table", "DNS records seen by a branch PC",
    "A branch technician looks up the bank's names with a DNS tool and gets these resource records (TTL in "
    "seconds; all records are class IN):\n\n"
    "| Name | TTL | Type | Data |\n|---|---|---|---|\n"
    "| netbanking.bank.example | 300 | CNAME | web.bank.example |\n"
    "| web.bank.example | 300 | A | 203.0.113.25 |\n| web.bank.example | 300 | AAAA | 2001:db8:10::25 |\n"
    "| bank.example | 3600 | MX | 10 mail1.bank.example |\n| bank.example | 3600 | MX | 20 mail2.bank.example |\n"
    "| bank.example | 86400 | NS | ns1.bank.example |\n| bank.example | 86400 | NS | ns2.bank.example |\n"
    "| 25.113.0.203.in-addr.arpa | 3600 | PTR | web.bank.example |",
    "netbanking.bank.example is an alias of web.bank.example, whose IPv4 address is 203.0.113.25 (A record) and "
    "IPv6 address is 2001:db8:10::25 (AAAA record). Mail goes first to mail1 (MX preference 10, lower is "
    "preferred). ns1 and ns2 are the authoritative name servers of the zone. The PTR record under in-addr.arpa "
    "maps the IP address back to a name. TTL tells resolvers how many seconds they may cache each record.")
Q(T, "Protocols", "Intermediate",
  "Refer to the DNS records. A PC that has only IPv6 connectivity opens netbanking.bank.example. To which address "
  "does it connect?",
  ["2001:db8:10::25, from the AAAA record of web.bank.example", "203.0.113.25, from the A record",
   "25.113.0.203, from the PTR record", "ns1.bank.example, from the NS record"],
  concept="DNS record types: A and AAAA",
  explanation="netbanking.bank.example is a CNAME (alias) for web.bank.example. For IPv6 the client asks for the "
              "AAAA record, which holds a 128-bit IPv6 address: 2001:db8:10::25. The A record holds the IPv4 "
              "address.",
  steps=["CNAME -> web.bank.example", "IPv6 -> AAAA record -> 2001:db8:10::25"],
  wrong="203.0.113.25 is the IPv4 address from the A record. The PTR owner name is the IPv4 address reversed, not "
        "an address to connect to. NS names the zone's name servers.", seconds=30, stim=S_DNS, pos=1,
  facts=[fact("RFC 3596: the AAAA resource record type stores a single IPv6 address; its type value is 28.",
              RFC3596)])
Q(T, "Protocols", "Intermediate",
  "Refer to the DNS records. A PC's resolver fetches and caches the A record of web.bank.example at 10:00:00. "
  "Until what time may it keep answering from its cache without asking the DNS servers again?",
  ["10:05:00", "11:00:00", "10:00:30", "10:00:00 the next day"],
  concept="DNS caching and TTL",
  explanation="The TTL (time to live) of a resource record is the number of seconds for which it may be cached. "
              "The A record's TTL is 300 seconds = 5 minutes, so the cached copy may be used until 10:05:00.",
  steps=["TTL = 300 s = 5 min", "10:00:00 + 5 min = 10:05:00"],
  wrong="11:00:00 uses the MX records' TTL of 3600 s. 10:00:30 reads 300 as tenths of seconds. The next day uses "
        "the NS records' TTL of 86400 s.", seconds=30, computed=True, stim=S_DNS, pos=2,
  facts=[fact("RFC 1035: TTL is a 32-bit unsigned integer that specifies the time interval (in seconds) that the "
              "resource record may be cached.", RFC1035)])
Q(T, "Protocols", "Intermediate",
  "Refer to the DNS records. A customer emails complaints@bank.example and both mail servers are working. To "
  "which server will the sending mail server try to deliver first?",
  ["mail1.bank.example, because its preference value 10 is lower", "mail2.bank.example, because 20 is higher",
   "ns1.bank.example, because name servers also accept mail", "web.bank.example, because it holds the A record"],
  concept="MX preference",
  explanation="Each MX record carries a preference number; lower values are preferred. The sender tries mail1 "
              "(10) first and falls back to mail2 (20) only if mail1 cannot be reached.",
  steps=["MX 10 mail1, MX 20 mail2", "Lower value is preferred -> mail1"],
  wrong="A higher preference number means LOWER priority. Name servers and web servers do not receive mail just "
        "because they appear in other records.", seconds=25, stim=S_DNS, pos=3,
  facts=[fact("RFC 1035: MX PREFERENCE is a 16-bit integer specifying the preference given to this RR among "
              "others at the same owner; lower values are preferred.", RFC1035)])
Q(T, "Protocols", "Intermediate",
  "Refer to the DNS records. What do the two NS records for bank.example tell other DNS servers?",
  ["That ns1.bank.example and ns2.bank.example are the authoritative name servers for the bank.example zone",
   "That ns1 and ns2 are the bank's mail servers", "That ns1 and ns2 are aliases of netbanking.bank.example",
   "That ns1 and ns2 are the IPv6 addresses of the bank's website"],
  concept="NS records",
  explanation="An NS record names a host that is authoritative for the domain: resolvers ask ns1 or ns2 for the "
              "official records of bank.example. Two are listed for redundancy.",
  steps=["NS = name server authoritative for the zone"],
  wrong="Mail servers come from MX records, aliases from CNAME records and IPv6 addresses from AAAA records.",
  seconds=25, stim=S_DNS, pos=4,
  facts=[fact("RFC 1035: NS RDATA is a domain name which specifies a host which should be authoritative for the "
              "specified class and domain.", RFC1035)])
Q(T, "Protocols", "Advanced",
  "Refer to the DNS records. A firewall log shows only the IP address 203.0.113.25, and an auditor wants the host "
  "name that belongs to it. Which lookup gives it, and under which name is the record stored?",
  ["A reverse lookup of the PTR record stored under 25.113.0.203.in-addr.arpa",
   "A forward lookup of the A record stored under 203.0.113.25.in-addr.arpa",
   "A lookup of the CNAME record stored under netbanking.bank.example",
   "A lookup of the MX record stored under bank.example"],
  concept="Reverse DNS",
  explanation="Address-to-name mapping uses PTR records in the special in-addr.arpa domain. The four octets of the "
              "IPv4 address are written in REVERSE order (25.113.0.203.in-addr.arpa), so that the most general part "
              "of the address comes last, as in a domain name. Here it returns web.bank.example.",
  steps=["IP -> name = reverse lookup", "Record type PTR", "Octets reversed + .in-addr.arpa"],
  wrong="A records map names to addresses (forward lookup), and the octets are not reversed in that option. CNAME "
        "and MX records do not map addresses back to names.", seconds=45, computed=True, stim=S_DNS, pos=5,
  facts=[fact("RFC 1035: the IN-ADDR.ARPA domain provides a guaranteed method to perform host address to host name "
              "mapping; PTR RDATA is a domain name which points to some location in the domain name space.",
              RFC1035)])
Q(T, "Web basics", "Basic",
  "Which network, set up by the US Defense Department's research agency and first connected in 1969 between UCLA "
  "and SRI, is regarded as the forerunner of today's internet?",
  ["ARPANET", "ETHERNET", "NICNET", "USENET"],
  concept="History of the internet",
  explanation="ARPANET, funded by DARPA (then ARPA), sent its first computer-to-computer message in 1969 between "
              "UCLA and SRI. It used packet switching and evolved into the internet in the early 1980s.",
  steps=["1969, US defence research agency, forerunner of the internet -> ARPANET"],
  wrong="Ethernet is a LAN technology. NICNET was India's National Informatics Centre network. Usenet is a "
        "discussion-group system that came later.", seconds=15,
  facts=[fact("DARPA: the roots of the modern internet lie in DARPA's work begun in the 1960s; ARPANET launched in "
              "1969 with the first computer-to-computer signal between UCLA and SRI and by 1983 had evolved into "
              "the internet.", DARPA_ARPANET)])
Q(T, "Web basics", "Basic",
  "Who invented the World Wide Web in 1989 while working at CERN, the European physics laboratory?",
  ["Tim Berners-Lee", "Vint Cerf", "Bill Gates", "Ray Tomlinson"],
  concept="History of the web",
  explanation="Tim Berners-Lee, a British scientist, proposed and built the World Wide Web at CERN, starting in "
              "1989; by the end of 1990 the first web server and browser were running there.",
  steps=["WWW, 1989, CERN -> Tim Berners-Lee"],
  wrong="Vint Cerf co-designed the TCP/IP protocols. Bill Gates co-founded Microsoft. Ray Tomlinson sent the first "
        "network email and chose the @ sign.", seconds=10,
  facts=[fact("CERN: Tim Berners-Lee, a British scientist, invented the World Wide Web (WWW) in 1989, while working "
              "at CERN.", CERN_WEB)])
Q(T, "Web basics", "Basic",
  "Bank staff keep their procedure manual on an internal website where any authorised employee can edit pages "
  "directly in the browser, and every change is saved in the page history. What is such a collaboratively "
  "edited website called?",
  ["Wiki", "Blog", "Search engine", "Web portal for payments"],
  concept="Types of websites",
  explanation="A wiki is a website whose pages many users can create and edit through the browser, with a history "
              "of every change. Wikipedia is the best-known example.",
  steps=["Many users edit pages + history -> wiki"],
  wrong="A blog is a series of dated posts usually written by one author or a small team. A search engine finds "
        "pages. A payment portal processes transactions.", seconds=15)
Q(T, "Protocols", "Intermediate",
  "A customer opens the bank's website, which runs behind a reverse proxy. The proxy is working, but the "
  "application server behind it has crashed, so the proxy cannot get a valid response from it. Which HTTP status "
  "code does the proxy most likely return?",
  ["502 Bad Gateway", "404 Not Found", "401 Unauthorized", "301 Moved Permanently"],
  concept="HTTP 5xx status codes",
  explanation="502 Bad Gateway means that a server acting as a gateway or proxy received an invalid response from "
              "the upstream server it contacted while trying to fulfil the request.",
  steps=["Proxy/gateway + bad response from upstream -> 502"],
  wrong="404 means the resource was not found. 401 means valid credentials are missing. 301 is a permanent "
        "redirect. None of them describes a failed upstream server.", seconds=20)
Q(T, "Web basics", "Intermediate",
  "An officer searches for jaguar insurance but keeps getting pages about the car brand. In a search engine such as "
  "Google, how should she leave out pages containing the word car?",
  ["jaguar insurance -car", "jaguar insurance +car", "jaguar insurance site:car",
   "\"jaguar insurance car\""],
  concept="Search operators",
  explanation="Putting a minus sign directly in front of a word (-car) tells the search engine to leave out results "
              "that contain that word.",
  steps=["Exclude a word -> -word"],
  wrong="+car does not exclude anything. site: limits results to a website or domain. Quotation marks search for "
        "the exact phrase, which would include car.", seconds=15,
  facts=[fact("Google Search Help: enter - in front of a word that you want to leave out, for example jaguar speed "
              "-car.", GOOGLE_REFINE)])
Q(T, "Web basics", "Advanced",
  "A net-banking site sets its session cookie with the attribute SameSite=Strict. A customer who is already "
  "logged in clicks a link to the bank's site from an email-provider web page (a different site). What happens "
  "to the session cookie on that first request?",
  ["The browser does not send it, because the request comes from another site; the customer may have to log in "
   "again",
   "The browser sends it, because the link opens the bank's own address",
   "The browser sends it only if the link uses HTTP rather than HTTPS",
   "The cookie is deleted permanently"],
  concept="SameSite cookies and CSRF protection",
  explanation="With SameSite=Strict, a cookie is sent only on requests that originate from the same site that set "
              "it. A navigation started from another site is cross-site, so the cookie is withheld; this blocks "
              "cross-site request forgery (CSRF) at the cost of sometimes asking the user to log in again. "
              "SameSite=Lax would send it on such top-level navigations with safe methods like GET.",
  steps=["Strict -> same-site requests only", "Link from another site = cross-site -> cookie not sent"],
  wrong="Sending it on cross-site top-level navigation is Lax behaviour, not Strict. SameSite has nothing to do "
        "with HTTP versus HTTPS (and secure session cookies are not sent over plain HTTP at all). The cookie is not "
        "deleted; it is simply not attached to that request.", seconds=45,
  facts=[fact("MDN Set-Cookie: SameSite=Strict sends the cookie only for requests originating from the same site "
              "that set the cookie; Lax also sends it for cross-site top-level navigations that use a safe "
              "method.", MDN_SETCOOKIE)])
Q(T, "Protocols", "Advanced",
  "A payment API may resend a request automatically after a network timeout. Under HTTP semantics, which group of "
  "request methods is defined as IDEMPOTENT, so that sending the same request several times has the same intended "
  "effect on the server as sending it once?",
  ["GET, HEAD, PUT and DELETE", "POST and PATCH only", "GET and POST only", "Only POST"],
  concept="Safe and idempotent HTTP methods",
  explanation="RFC 9110 defines PUT, DELETE and the safe methods (GET, HEAD, OPTIONS, TRACE) as idempotent. POST "
              "is not: repeating a POST may, for example, create two payments. That is why APIs that retry POST "
              "requests use idempotency keys.",
  steps=["Idempotent = PUT, DELETE + safe methods (GET, HEAD, OPTIONS, TRACE)", "POST is not idempotent"],
  wrong="POST is not idempotent, so every option that contains it is wrong; PATCH is not defined as idempotent "
        "either.", seconds=40,
  facts=[fact("RFC 9110 section 9.2.2: PUT, DELETE, and safe request methods are idempotent.", RFC9110)])

# ================================================================ 8. Networking (2 / 2 / 2)
T = "Networking"
Q(T, "Topologies", "Basic",
  "In a small branch, five PCs share files and a printer directly with one another; there is no dedicated server, "
  "and every PC can act both as a client and as a server. What type of network is this?",
  ["Peer-to-peer network", "Client-server network", "Metropolitan area network", "Virtual private network"],
  concept="Network models",
  explanation="In a peer-to-peer network, all computers have equal status and share their resources directly, each "
              "acting as both client and server. A client-server network has dedicated servers that provide "
              "services to clients.",
  steps=["No dedicated server, equal computers -> peer-to-peer"],
  wrong="Client-server needs a dedicated server. A MAN covers a city. A VPN is an encrypted tunnel over another "
        "network.", seconds=15)
Q(T, "Devices", "Basic",
  "During a power cut, a branch officer shares her phone's mobile-data connection over Wi-Fi so that her laptop "
  "can reach the internet. What is this feature called?",
  ["Mobile hotspot (tethering)", "Bluetooth pairing", "Airplane mode", "NFC payment"],
  concept="Sharing a mobile connection",
  explanation="A mobile hotspot (tethering) turns the phone into a small wireless router that shares its "
              "mobile-data internet connection with other devices over Wi-Fi (or USB or Bluetooth).",
  steps=["Phone shares its data connection with a laptop -> hotspot / tethering"],
  wrong="Bluetooth pairing only links two devices. Airplane mode switches the radios off. NFC is used for "
        "contactless payments over a few centimetres.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "A bank's new application server listens on TCP port 8443. According to the IANA port ranges, ports 0 to 1023 "
  "are the System (well-known) Ports. To which range does 8443 belong?",
  ["User (registered) Ports, 1024-49151", "System (well-known) Ports, 0-1023",
   "Dynamic (private, ephemeral) Ports, 49152-65535", "It is not a valid port number"],
  concept="Port number ranges",
  explanation="RFC 6335 divides the 16-bit port space into System Ports 0-1023, User (registered) Ports 1024-49151 "
              "and Dynamic (private or ephemeral) Ports 49152-65535. 8443 lies in 1024-49151.",
  steps=["1024 <= 8443 <= 49151 -> User (registered) Ports"],
  wrong="8443 is above 1023 and below 49152. Port numbers go up to 65535, so 8443 is valid.", seconds=25,
  computed=True,
  facts=[fact("RFC 6335: System Ports (Well Known Ports) 0-1023, User Ports (Registered Ports) 1024-49151, Dynamic "
              "(Private/Ephemeral) Ports 49152-65535.", RFC6335)])
assert 1024 <= 8443 <= 49151
Q(T, "Devices", "Intermediate",
  "A network engineer sees an unknown device with MAC address 00:1A:2B:3C:4D:5E on a branch switch and looks up "
  "the first three bytes, 00:1A:2B, in the IEEE registry. What do these 24 bits identify?",
  ["The organisation (manufacturer) to which that block of addresses was assigned - the OUI",
   "The branch's IP subnet", "The switch port the device is connected to", "The device's serial number"],
  concept="Structure of a MAC address",
  explanation="A 48-bit MAC address (EUI-48) is made of a 24-bit Organizationally Unique Identifier (OUI) assigned "
              "by the IEEE to the organisation, followed by 24 bits assigned by that organisation. Looking up the OUI "
              "reveals the vendor.",
  steps=["48 bits = 24-bit OUI + 24 organisation-assigned bits", "First 3 bytes -> manufacturer"],
  wrong="MAC addresses do not contain IP subnets or switch-port numbers. The last 24 bits, not the first, are "
        "chosen by the maker for each interface.", seconds=25,
  facts=[fact("IEEE: the OUI included in an MA-L assignment may be appended with 24 organization-supplied bits to "
              "form an EUI-48; the MA-L was previously referred to as an OUI.", IEEE_OUI)])
o, a = ordered(50, [66.7, 100, 33.3], fmt=lambda v: f"{v:g}%")
Q(T, "OSI and TCP/IP", "Advanced",
  "A branch on a long leased line sends 1,000-byte frames over a 1 Mbps link using stop-and-wait: after each frame it "
  "waits for an acknowledgement before sending the next. The one-way propagation delay is 4 ms. Ignoring the time "
  "to transmit the acknowledgement and any processing delay, what is the link utilisation (efficiency)?", o, a,
  concept="Stop-and-wait efficiency",
  explanation="Frame transmission time = 1,000 x 8 bits / 1,000,000 bps = 8 ms. After sending, the sender waits for "
              "the frame to arrive (4 ms) and the acknowledgement to return (4 ms). Each cycle is 8 + 2 x 4 = 16 ms, "
              "of which the link is busy for 8 ms: efficiency = 8 / 16 = 50%.",
  steps=["Tframe = 8,000 / 10^6 s = 8 ms", "Round trip = 2 x 4 = 8 ms", "8 / (8 + 8) = 50%"],
  wrong="66.7% counts the propagation delay only once (8 / 12). 100% ignores the waiting. 33.3% doubles the frame "
        "time as well.", seconds=75, computed=True)
o, a = ordered(370, [185, 2960, 3], fmt=str)
Q(T, "OSI and TCP/IP", "Advanced",
  "An IPv4 datagram of 4,000 bytes (a 20-byte header plus 3,980 bytes of data) must cross a link whose MTU is "
  "1,500 bytes, so a router fragments it. Each fragment gets its own 20-byte header, and the fragment-offset "
  "field counts in units of 8 bytes. What is the fragment-offset field value of the THIRD fragment?", o, a,
  concept="IPv4 fragmentation",
  explanation="Each fragment can carry 1,500 - 20 = 1,480 bytes of data (a multiple of 8). The fragments carry "
              "1,480, 1,480 and 1,020 bytes. The third starts at data byte 2,960, and the offset field stores "
              "2,960 / 8 = 370.",
  steps=["Data per fragment = 1,480", "Fragments: 0-1,479; 1,480-2,959; 2,960-3,979", "Offset = 2,960 / 8 = 370"],
  wrong="185 is the offset of the second fragment. 2,960 is the offset in bytes, not in 8-byte units. 3 is the "
        "fragment's position, not its offset.", seconds=90, computed=True,
  facts=[fact("RFC 791: the fragment offset is measured in units of 8 octets (64 bits).", RFC791)])
assert frags[2][0] == 370 and frags[1][0] == 185

# ================================================================ 9. Cybersecurity (2 / 4 / 4)
T = "Cybersecurity"
Q(T, "Phishing and social engineering", "Basic",
  "A customer gets an email saying he has won Rs 25 lakh in an international lottery he never entered, and that he "
  "must first pay a 'processing fee' of Rs 15,000 to release the prize. What is this?",
  ["An advance-fee (lottery) fraud", "A genuine prize notification", "A software update notice",
   "A denial-of-service attack"],
  concept="Advance-fee fraud",
  explanation="Advance-fee frauds promise a large reward (a lottery win, inheritance or loan) but first demand a "
              "smaller 'fee', 'tax' or 'charge'. Once paid, the fraudster asks for more or disappears; the prize "
              "does not exist. A lottery one never entered cannot be won.",
  steps=["Unexpected prize + pay a fee first -> advance-fee fraud"],
  wrong="Genuine prizes do not require upfront fees, and one cannot win a lottery one did not enter. The email has "
        "nothing to do with software updates or flooding a server.", seconds=15)
Q(T, "Phishing and social engineering", "Basic",
  "A customer searches the internet for her bank's customer-care number, calls the first number shown on a "
  "random website, and the 'executive' asks her to share the OTP to 'reverse a failed transaction'. What is the "
  "safest practice?",
  ["Take customer-care numbers only from the bank's official website, app, card or passbook, and never share an "
   "OTP with anyone",
   "Share the OTP, because she called the number herself",
   "Share only half of the OTP to be safe",
   "Ask the caller to send his employee ID before sharing the OTP"],
  concept="Fake customer-care numbers",
  explanation="Fraudsters publish fake helpline numbers on websites, listings and social media. Contact details "
              "should be taken only from official sources, and an OTP must never be shared with anyone, because it "
              "authorises a transaction.",
  steps=["Number from an unofficial page -> may be fake", "Never share an OTP"],
  wrong="Calling the number yourself does not make it genuine. Part of an OTP or an 'employee ID' from the caller "
        "gives no protection; any ID can be invented.", seconds=20)
Q(T, "Phishing and social engineering", "Intermediate",
  "A malicious website loads the bank's real fund-transfer page in an invisible frame and places a 'Claim your "
  "reward' button exactly over the hidden 'Confirm transfer' button. The user thinks he is clicking the reward "
  "button. What is this attack called?",
  ["Clickjacking (UI redress attack)", "SQL injection", "Pharming", "Keylogging"],
  concept="Clickjacking",
  explanation="Clickjacking hides or disguises a legitimate page under layers so that a user's click lands on a "
              "control of that page without his knowledge. Sites defend against it by forbidding other sites from "
              "framing them with the Content-Security-Policy frame-ancestors directive (or the older X-Frame-Options "
              "header).",
  steps=["Invisible frame + decoy button -> hijacked click -> clickjacking"],
  wrong="SQL injection attacks a database through input fields. Pharming redirects users through tampered DNS. "
        "Keylogging records keystrokes.", seconds=25,
  facts=[fact("OWASP describes clickjacking as a 'UI redress attack' and recommends the CSP frame-ancestors "
              "directive, with X-Frame-Options for older browsers.", OWASP_CLICK)])
Q(T, "Malware", "Intermediate",
  "An officer merely opens a compromised news website in an outdated browser and, without clicking any download "
  "or approving anything, malware is silently installed by exploiting a browser flaw. What is this called?",
  ["Drive-by download", "Baiting", "Logic bomb", "Typosquatting"],
  concept="Drive-by downloads",
  explanation="In a drive-by download, malicious code on a web page exploits a vulnerability in the browser or a "
              "plug-in to install malware simply because the page was visited. Keeping browsers patched is the main "
              "defence.",
  steps=["Just visiting a page + exploit + silent install -> drive-by download"],
  wrong="Baiting leaves an infected item (such as a USB drive) for a victim to use. A logic bomb waits for a "
        "condition inside a system. Typosquatting registers misspelt domain names.", seconds=20)
Q(T, "Malware", "Intermediate",
  "At a crowded railway station, an attacker exploits a weakness in a traveller's phone's Bluetooth to copy his "
  "contacts, messages and photos without his knowledge. What is this Bluetooth attack called?",
  ["Bluesnarfing", "Bluejacking", "Smishing", "Juice jacking"],
  concept="Bluetooth attacks",
  explanation="Bluesnarfing is the theft of data from a device over a Bluetooth connection without the owner's "
              "permission. Bluejacking only sends unsolicited messages to nearby Bluetooth devices.",
  steps=["Stealing data over Bluetooth -> bluesnarfing"],
  wrong="Bluejacking sends unwanted messages but does not steal data. Smishing is SMS phishing. Juice jacking "
        "attacks phones through tampered USB charging ports.", seconds=20)
Q(T, "Phishing and social engineering", "Intermediate",
  "A phishing link shows a domain that looks exactly like bank.example, but its letter 'a' is actually the "
  "Cyrillic letter 'а', which looks identical on screen, so it is a different domain owned by the fraudster. What "
  "is this technique called?",
  ["IDN homograph attack", "Typosquatting with a misspelt name", "Session hijacking", "Brute-force attack"],
  concept="Homograph attacks",
  explanation="Internationalised domain names (IDNs) can contain letters from other scripts. A homograph attack "
              "registers a domain whose characters look identical to a genuine one, such as a Cyrillic 'а' in place "
              "of the Latin 'a', so even a careful reader cannot spot the difference.",
  steps=["Look-alike characters from another script -> IDN homograph attack"],
  wrong="Typosquatting relies on visible misspellings or typing mistakes. Session hijacking steals an active "
        "session. A brute-force attack tries many passwords.", seconds=25)
o, a = ordered(D_, [3, 11, 13], fmt=str)
Q(T, "Encryption and authentication", "Advanced",
  "In a classroom RSA example, p = 3 and q = 11, so n = 33 and phi(n) = (p - 1)(q - 1) = 20. The public exponent is "
  "e = 3. The private exponent d is the smallest positive number with (e x d) mod phi(n) = 1. What is d?", o, a,
  concept="RSA key generation",
  explanation="We need 3d mod 20 = 1. Trying d = 1, 2, ...: 3 x 7 = 21 = 20 + 1, so d = 7. Check: encrypting 4 "
              "gives 4^3 mod 33 = 64 mod 33 = 31, and 31^7 mod 33 = 4, the original message.",
  steps=["Need 3d = 1 (mod 20)", "3 x 7 = 21 = 1 (mod 20)", "d = 7"],
  wrong="3 is e itself (3 x 3 = 9). 11 solves 3d = 1 mod 32, using n - 1 instead of phi(n). 13 gives 3 x 13 = 39 "
        "= 19 mod 20.", seconds=60, computed=True)
assert 3 * 13 % 20 == 19 and 3 * 3 % 20 == 9
Q(T, "Encryption and authentication", "Advanced",
  "A developer encrypts a bank's image of a cheque with AES in ECB (Electronic Codebook) mode, and the outline of "
  "the cheque is still visible in the encrypted image. Why does this happen?",
  ["ECB encrypts each block independently with the same key, so identical plaintext blocks give identical "
   "ciphertext blocks and patterns remain visible",
   "AES is a weak algorithm that does not really encrypt image data",
   "ECB mode leaves every second block unencrypted",
   "ECB uses a different random key for each block, which distorts but does not hide the image"],
  concept="Block cipher modes of operation",
  explanation="In ECB, every block is encrypted separately with the same key and no chaining or nonce, so "
              "repeated plaintext blocks (large areas of the same colour) produce repeated ciphertext blocks and "
              "the data's structure stays visible. Modes such as CBC, CTR or GCM mix in an IV, nonce or counter to "
              "hide such patterns.",
  steps=["ECB: same key, no chaining", "Same plaintext block -> same ciphertext block", "Patterns survive"],
  wrong="AES itself is strong; the weakness lies in the mode. ECB encrypts every block. It uses one key for all "
        "blocks, not a random key per block.", seconds=40,
  facts=[fact("ECB fails to hide data patterns because it encrypts identical plaintext blocks into identical "
              "ciphertext blocks.", WIKI_MODES),
         fact("NIST SP 800-38A defines five confidentiality modes for block ciphers: ECB, CBC, CFB, OFB and CTR.",
              NIST_80038A)])
Q(T, "Encryption and authentication", "Advanced",
  "A bank's server private key is stolen in 2026. Its old TLS 1.3 sessions recorded by an attacker in 2025 still "
  "cannot be decrypted, because each session's key was agreed with fresh (ephemeral) Diffie-Hellman values that "
  "were discarded afterwards. Which property is this?",
  ["Forward secrecy (perfect forward secrecy)", "Non-repudiation", "Key escrow", "Certificate pinning"],
  concept="Forward secrecy",
  explanation="With forward secrecy, session keys are derived from ephemeral key-exchange values that are thrown "
              "away after use, so compromising the long-term private key later does not reveal past session keys. "
              "TLS 1.3 removed static RSA key exchange, so all its public-key based key exchanges provide forward "
              "secrecy.",
  steps=["Ephemeral DH per session + long-term key stolen later -> past sessions safe", "= forward secrecy"],
  wrong="Non-repudiation stops a signer from denying a signature. Key escrow deposits keys with a third party. "
        "Certificate pinning makes an app accept only specific certificates.", seconds=40,
  facts=[fact("RFC 8446 (TLS 1.3): static RSA and Diffie-Hellman cipher suites have been removed; all public-key "
              "based key exchange mechanisms now provide forward secrecy.", RFC8446)])
Q(T, "Encryption and authentication", "Advanced",
  "A bank and a payment partner share a secret key. Every API message carries a tag computed from the message and "
  "the secret key with SHA-256, so the receiver can confirm the message was not altered and that it came from "
  "someone holding the key. What is this mechanism?",
  ["HMAC (hash-based message authentication code)", "A plain SHA-256 checksum", "Public-key encryption of the "
   "message", "Base64 encoding"],
  concept="Message authentication codes",
  explanation="HMAC combines a cryptographic hash function such as SHA-256 with a shared secret key. Only holders "
              "of the key can compute a valid tag, so it proves both integrity and the origin of the message. A "
              "plain hash proves neither against an attacker, who can recompute it after changing the message.",
  steps=["Hash + shared secret key -> HMAC", "Gives integrity and authenticity"],
  wrong="A plain SHA-256 checksum has no key, so an attacker can alter the message and recompute it. Public-key "
        "encryption gives confidentiality and uses key pairs, not a shared secret. Base64 is only an encoding.",
  seconds=40,
  facts=[fact("RFC 2104 describes HMAC, a mechanism for message authentication using cryptographic hash functions "
              "with a secret shared key.", RFC2104)])

# ================================================================ 10. Database Fundamentals (4 / 4 / 1)
T = "Database Fundamentals"
S_CHQ = new_stim(
    "data_table", "Cheques table of a branch",
    "Table **Cheques** records cheques presented for clearing (status NULL means the clerk has not yet entered a "
    "status):\n\n| chq_no | acc_no | amount | status | presented_on |\n|---|---|---|---|---|\n"
    "| C101 | A1 | 25000 | Cleared | 2026-11-02 |\n| C102 | A2 | 48000 | Returned | 2026-11-02 |\n"
    "| C103 | A1 | 12000 | Pending | 2026-11-03 |\n| C104 | A3 | 75000 | Cleared | 2026-11-03 |\n"
    "| C105 | A2 | 30000 | Cleared | 2026-11-04 |\n| C106 | A4 | 9000 | Returned | 2026-11-04 |\n"
    "| C107 | A3 | 60000 | NULL | 2026-11-04 |\n| C108 | A1 | 40000 | Pending | 2026-11-05 |\n\n"
    "Each question uses the table as shown (no earlier query has changed it).",
    "Returned cheques: C102 (48000) and C106 (9000). Accounts with both a cleared and a returned cheque: A2. Rows "
    "whose status is not 'Cleared': C102, C103, C106, C108 (C107's NULL is unknown, so it is not counted). "
    "Amounts above every returned amount: C104 and C107. A1's cheques in date order: 25000, 12000, 40000.")
o, a = ordered(9000, [48000, 12000, 57000], fmt=lambda v: f"{v:,}")
Q(T, "SQL basics", "Basic",
  "Refer to the Cheques table. What does this query return?\n\nSELECT MIN(amount) FROM Cheques WHERE status = "
  "'Returned';", o, a,
  concept="Aggregate functions with WHERE",
  explanation="WHERE keeps only the returned cheques, C102 (48,000) and C106 (9,000). MIN returns the smaller "
              "amount, 9,000.",
  steps=["Returned rows: 48000, 9000", "MIN = 9000"],
  wrong="48,000 is the MAX of the returned cheques. 12,000 is the smallest pending cheque. 57,000 is the SUM of "
        "the returned cheques.", seconds=25, computed=True, stim=S_CHQ, pos=1)
o, a = ordered(2, [3, 8, 1], fmt=str)
Q(T, "SQL basics", "Basic",
  "Refer to the Cheques table. How many rows does this statement change?\n\nUPDATE Cheques SET status = 'Cleared' "
  "WHERE status = 'Pending';", o, a,
  concept="UPDATE with WHERE",
  explanation="UPDATE changes only the rows that satisfy WHERE. Two rows are Pending (C103 and C108), so 2 rows "
              "become Cleared; the others are untouched.",
  steps=["Pending rows: C103, C108", "2 rows updated"],
  wrong="3 would also include the NULL row C107, which does not equal 'Pending'. 8 is what happens if the WHERE "
        "clause is left out. 1 counts only one account (A1), but UPDATE works on rows.", seconds=25,
  computed=True, stim=S_CHQ, pos=2)
o = ["A2", "A1 and A2", "A2 and A4", "A1, A2, A3 and A4"]
Q(T, "SQL basics", "Intermediate",
  "Refer to the Cheques table. What does this query return?\n\nSELECT acc_no FROM Cheques WHERE status = "
  "'Cleared'\nINTERSECT\nSELECT acc_no FROM Cheques WHERE status = 'Returned';", o,
  concept="INTERSECT",
  explanation="The first query gives the accounts with a cleared cheque: A1, A3, A2. The second gives the accounts "
              "with a returned cheque: A2, A4. INTERSECT keeps only values in both (without duplicates): A2.",
  steps=["Cleared: {A1, A2, A3}", "Returned: {A2, A4}", "Common: {A2}"],
  wrong="A1 has no returned cheque. A4 has no cleared cheque. Listing all four accounts is UNION, not INTERSECT.",
  seconds=45, computed=True, stim=S_CHQ, pos=3)
o, a = ordered(4, [5, 3, 8], fmt=str)
Q(T, "SQL basics", "Intermediate",
  "Refer to the Cheques table. What does this query return?\n\nSELECT COUNT(*) FROM Cheques WHERE status <> "
  "'Cleared';", o, a,
  concept="Comparisons with NULL",
  explanation="Rows that are not Cleared are C102, C103, C106 and C108 (4 rows). C107 has a NULL status: NULL <> "
              "'Cleared' evaluates to UNKNOWN, not TRUE, so WHERE drops that row too. The answer is 4.",
  steps=["Cleared: C101, C104, C105", "Others: C102, C103, C106, C107, C108", "NULL row gives UNKNOWN -> excluded",
         "Count = 4"],
  wrong="5 wrongly counts the NULL row. 3 is the number of Cleared rows. 8 is the whole table.", seconds=45,
  computed=True, stim=S_CHQ, pos=4)
o = ["C104 and C107", "C104 only", "All cheques except C106", "C102, C104 and C107"]
Q(T, "SQL basics", "Intermediate",
  "Refer to the Cheques table. Which cheques does this query return?\n\nSELECT chq_no FROM Cheques\nWHERE amount > "
  "ALL (SELECT amount FROM Cheques WHERE status = 'Returned');", o,
  concept="ALL with a subquery",
  explanation="The subquery returns the returned amounts 48,000 and 9,000. '> ALL' requires the amount to be "
              "greater than every one of them, that is, greater than 48,000: C104 (75,000) and C107 (60,000).",
  steps=["Subquery: {48000, 9000}", "> ALL = > 48000", "C104 75000, C107 60000"],
  wrong="C104 only forgets C107 (its NULL status does not matter; only its amount is compared). 'All except C106' "
        "is what '> ANY' (greater than at least one, i.e. > 9000) would give. C102 is 48,000, which is not GREATER "
        "than 48,000.", seconds=50, computed=True, stim=S_CHQ, pos=5)
o, a = ordered(28000, [15000, -13000, 40000], fmt=lambda v: f"{v:,}")
Q(T, "SQL basics", "Advanced",
  "Refer to the Cheques table. What value does this query show in the diff column for cheque C108?\n\nSELECT "
  "chq_no, amount - LAG(amount) OVER (PARTITION BY acc_no ORDER BY presented_on, chq_no) AS diff\nFROM Cheques;",
  o, a,
  concept="Window function LAG",
  explanation="PARTITION BY acc_no makes each account a separate window. A1's cheques in date order are C101 "
              "(25,000), C103 (12,000) and C108 (40,000). LAG gives the previous row's amount in the same window, "
              "so for C108 it is 12,000 and diff = 40,000 - 12,000 = 28,000.",
  steps=["A1 in order: 25000, 12000, 40000", "LAG for C108 = 12000", "40000 - 12000 = 28000"],
  wrong="15,000 subtracts the FIRST A1 cheque (25,000) instead of the previous one. -13,000 is the diff of C103. "
        "40,000 treats LAG as zero.", seconds=75, computed=True, stim=S_CHQ, pos=6)
Q(T, "DBMS concepts", "Basic",
  "Before creating any tables, a database designer writes down the overall logical structure of the bank's "
  "database: the tables, their columns and data types, and the relationships between them. In DBMS terms, this "
  "overall design is called the:",
  ["Schema", "Instance", "Tuple", "Query"],
  concept="Schema and instance",
  explanation="A schema is the overall logical design of a database (tables, attributes, types, constraints and "
              "relationships); it changes rarely. An instance is the data stored in the database at a particular "
              "moment.",
  steps=["Overall design / structure -> schema"],
  wrong="An instance is the actual data at one moment. A tuple is a single row. A query is a request to retrieve "
        "or change data.", seconds=15)
Q(T, "SQL basics", "Basic",
  "A test table named TempLoans is no longer needed. The DBA wants to remove the table completely - its rows, its "
  "structure and its definition. Which SQL command does this?",
  ["DROP TABLE TempLoans;", "DELETE FROM TempLoans;", "TRUNCATE TABLE TempLoans;",
   "ALTER TABLE TempLoans DROP COLUMN amount;"],
  concept="DDL: DROP",
  explanation="DROP TABLE removes the table itself, including its structure and data. DELETE (without WHERE) and "
              "TRUNCATE remove all rows but leave an empty table behind.",
  steps=["Remove table + structure -> DROP TABLE"],
  wrong="DELETE and TRUNCATE keep the (empty) table. ALTER TABLE ... DROP COLUMN removes only one column.",
  seconds=15)
Q(T, "Keys", "Intermediate",
  "In a Customers table, the bank does not use PAN or mobile number as the primary key, because they may be "
  "missing or may change. Instead the system generates a number such as 1000231 for each new customer; it has no "
  "business meaning and is used only to identify the row. What is such a key called?",
  ["Surrogate key", "Natural key", "Foreign key", "Composite key"],
  concept="Surrogate and natural keys",
  explanation="A surrogate key is an artificial, system-generated identifier (often an auto-incremented number) "
              "with no meaning in the business. A natural key is made of real-world data such as PAN.",
  steps=["System-generated, no business meaning -> surrogate key"],
  wrong="A natural key uses real-world attributes such as PAN. A foreign key refers to another table's key. A "
        "composite key is made of two or more columns.", seconds=20)

# ================================================================ 11. MS Office (2 / 4 / 2)
T = "MS Office"
S_GOLD = new_stim(
    "data_table", "Excel gold-loan register",
    "A branch keeps its gold-loan register in Excel. Rows 2 to 7 hold the data; H1:K2 holds the eligible loan per "
    "gram for each purity:\n\n"
    "| Row | A: Name | B: Branch | C: Sanction date | D: Gold (grams) | E: Purity (karat) |\n|---|---|---|---|---|---|\n"
    "| 2 | asha MENON | Pune | 14-Aug-2026 | 40 | 22 |\n| 3 | anil d'cruz | Delhi | 31-Aug-2026 | 18 | 18 |\n"
    "| 4 | RAVI shankar | Agra | 10-Sep-2026 | 25 | 20 |\n| 5 | meena iyer | Pune | 30-Sep-2026 | 32 | 24 |\n"
    "| 6 | john mathew | Delhi | 19-Oct-2026 | 12 | 22 |\n| 7 | farah khan | Agra | 05-Nov-2026 | 50 | 18 |\n\n"
    "| | H | I | J | K |\n|---|---|---|---|---|\n| 1 | 18 | 20 | 22 | 24 |\n| 2 | 4800 | 5300 | 5900 | 6400 |\n\n"
    "Dates are real Excel dates; results that are dates are shown in dd-mmm-yyyy format.",
    "PROPER(A3) = Anil D'Cruz (the letter after the apostrophe is also capitalised). EOMONTH(C2, 3) = 30-Nov-2026. "
    "Row 4: 25 g at 20 karat -> 25 x 5300 = 132,500. DATEDIF(C2, C7, \"m\") = 2 complete months (14-Aug to "
    "05-Nov).")
o, a = ordered(sum(c.isupper() for c in proper(GL[1][0])), [1, 2, 9], fmt=str)
Q(T, "MS Excel", "Intermediate",
  "Refer to the gold-loan register. A clerk tidies the names with =PROPER(A3). How many CAPITAL letters does the "
  "result contain?", o, a,
  concept="Excel text function PROPER",
  explanation="PROPER capitalises the first letter of the text and every letter that follows a character other "
              "than a letter, and makes all other letters lowercase. In anil d'cruz, 'a', 'd' (after the space) and "
              "'c' (after the apostrophe) become capitals: Anil D'Cruz, with 3 capital letters.",
  steps=["First letter -> A", "After space -> D", "After apostrophe (not a letter) -> C", "Others lowercase",
         "Result Anil D'Cruz: 3 capitals"],
  wrong="2 (Anil D'cruz) forgets that the apostrophe also triggers a capital. 1 capitalises only the first "
        "letter of the text. 9 is what UPPER would give (every letter).", seconds=30, computed=True, stim=S_GOLD, pos=1,
  facts=[fact("Microsoft: PROPER capitalizes the first letter in a text string and any other letters that follow "
              "any character other than a letter, and converts all other letters to lowercase ('2-Way Street').",
              MS_PROPER)])
o = ["30-Nov-2026", "31-Oct-2026", "14-Nov-2026", "01-Dec-2026"]
Q(T, "MS Excel", "Intermediate",
  "Refer to the gold-loan register. Interest on Asha's loan is first reviewed at the end of the third month after "
  "sanction. What does =EOMONTH(C2, 3) return?", o,
  concept="Excel date function EOMONTH",
  explanation="EOMONTH returns the last day of the month that is the given number of months before or after the "
              "start date. Three months after 14-Aug-2026 is November 2026, whose last day is 30-Nov-2026.",
  steps=["14-Aug-2026 + 3 months -> November 2026", "Last day of November = 30"],
  wrong="31-Oct-2026 is only two months ahead. 14-Nov-2026 is what EDATE(C2, 3) gives (same day number). "
        "01-Dec-2026 is the day after the correct answer.", seconds=30, computed=True, stim=S_GOLD, pos=2,
  facts=[fact("Microsoft: EOMONTH returns the serial number for the last day of the month that is the indicated "
              "number of months before or after start_date; =EOMONTH(1-Jan-11, 1) gives 28-Feb-2011.", MS_EOMONTH)])
assert eomonth(GL[0][2], 3) == dt.date(2026, 11, 30)
assert sum(c.isalpha() for c in GL[1][0]) == 9 and sum(c.isupper() for c in proper(GL[1][0])) == 3
o, a = ordered(132500, [120000, 147500, 160000], fmt=lambda v: f"{v:,}")
Q(T, "MS Excel", "Advanced",
  "Refer to the gold-loan register. What does this formula return for Ravi's loan?\n\n=D4 * HLOOKUP(E4, $H$1:$K$2, "
  "2, FALSE)", o, a,
  concept="HLOOKUP with exact match",
  explanation="HLOOKUP searches the TOP row of H1:K2 for E4 = 20 (exact match because of FALSE), finds it in column "
              "I and returns the value from row 2 of the table, 5,300. Then 25 grams x 5,300 = 1,32,500.",
  steps=["E4 = 20 found in I1", "Row 2 of that column: 5300", "D4 x 5300 = 25 x 5300 = 132,500"],
  wrong="120,000 uses the 18-karat rate (4,800). 147,500 uses the 22-karat rate (5,900). 160,000 uses the 24-karat "
        "rate (6,400).", seconds=45, computed=True, stim=S_GOLD, pos=3,
  facts=[fact("Microsoft: HLOOKUP searches for a value in the top row of a table and returns a value from the row "
              "given by row_index_num in the same column; with FALSE it finds an exact match.", MS_HLOOKUP)])
assert GL[2][3] * 6400 == 160000
o, a = ordered(2, [3, 83, 1], fmt=str)
Q(T, "MS Excel", "Advanced",
  "Refer to the gold-loan register. What does =DATEDIF(C2, C7, \"m\") return?", o, a,
  concept="DATEDIF: complete months",
  explanation="With the unit \"m\", DATEDIF returns the number of COMPLETE months between the two dates. From "
              "14-Aug-2026, two complete months end on 14-Oct-2026; the third would end on 14-Nov-2026, which is "
              "after 05-Nov-2026. So the result is 2.",
  steps=["14-Aug -> 14-Sep (1) -> 14-Oct (2)", "14-Nov is after 05-Nov -> stop", "Result 2"],
  wrong="3 just subtracts the month numbers (11 - 8). 83 is the number of days (unit \"d\"). 1 undercounts.",
  seconds=45, computed=True, stim=S_GOLD, pos=4,
  facts=[fact("Microsoft: DATEDIF calculates the number of days, months, or years between two dates; unit \"M\" "
              "gives the number of complete months in the period.", MS_DATEDIF)])
Q(T, "Shortcuts", "Basic",
  "In MS Word for Windows, which keyboard shortcut applies underline formatting to the selected text?",
  ["Ctrl + U", "Ctrl + B", "Ctrl + I", "Ctrl + L"],
  concept="Word formatting shortcuts",
  explanation="Ctrl + U applies (or removes) underline. Ctrl + B is bold, Ctrl + I is italic and Ctrl + L aligns "
              "the paragraph to the left.",
  steps=["Underline -> Ctrl + U"],
  wrong="Ctrl + B is bold, Ctrl + I italic, and Ctrl + L left alignment.", seconds=10,
  facts=[fact("Microsoft lists Ctrl+U as 'Apply underline formatting' in Word.", MS_WORD_KEYS)])
Q(T, "MS PowerPoint", "Basic",
  "On a PowerPoint slide, a trainer selects a logo, a text box and an arrow and wants to combine them so that they "
  "move and resize together as one object. Which shortcut does this in PowerPoint for Windows?",
  ["Ctrl + G (Group)", "Ctrl + M", "Ctrl + K", "Ctrl + D"],
  concept="PowerPoint shortcuts",
  explanation="Ctrl + G groups the selected objects so that they can be moved, resized and formatted as one unit.",
  steps=["Combine selected objects -> Group -> Ctrl + G"],
  wrong="Ctrl + M inserts a new slide. Ctrl + K inserts a hyperlink. Ctrl + D duplicates the selected objects, "
        "creating copies rather than grouping them.", seconds=15,
  facts=[fact("Microsoft lists, for PowerPoint, Ctrl+G 'Group the selected objects', Ctrl+M 'Insert a new slide', "
              "Ctrl+K 'Insert a hyperlink' and Ctrl+D 'Duplicate selected objects'.", MS_PPT_KEYS)])
Q(T, "Shortcuts", "Intermediate",
  "In MS Word for Windows, a clerk wants to make the selected heading bigger, one standard font size at a time, "
  "without opening the Font box. Which shortcut does this?",
  ["Ctrl + Shift + >", "Ctrl + Shift + <", "Ctrl + D", "Ctrl + Shift + N"],
  concept="Word font-size shortcuts",
  explanation="Ctrl + Shift + > increases the font size of the selected text (Ctrl + Shift + < decreases it; Ctrl "
              "+ ] and Ctrl + [ change it by one point).",
  steps=["Increase font size -> Ctrl + Shift + >"],
  wrong="Ctrl + Shift + < decreases the size. Ctrl + D opens the Font dialog box. Ctrl + Shift + N applies the "
        "Normal style.", seconds=20,
  facts=[fact("Microsoft lists, for Word, Ctrl+Shift+> 'Increase the font size', Ctrl+D 'Display the Font dialog "
              "box' and Ctrl+Shift+N 'Apply the Normal style'.", MS_WORD_KEYS)])
Q(T, "Shortcuts", "Intermediate",
  "In Excel for Windows, a clerk enters a branch name in B2, selects B2:B40 and wants to copy the contents and "
  "format of B2 into all the cells below it in one step. Which shortcut does this?",
  ["Ctrl + D (Fill Down)", "Ctrl + R", "Ctrl + Enter only, without typing", "F4"],
  concept="Excel fill shortcuts",
  explanation="Ctrl + D uses the Fill Down command: it copies the contents and format of the topmost cell of the "
              "selected range into the cells below.",
  steps=["Copy top cell into the cells below -> Fill Down -> Ctrl + D"],
  wrong="Ctrl + R fills to the RIGHT, from the leftmost column. Ctrl + Enter fills the selection only with an "
        "entry that is being typed. F4 repeats the last action or toggles absolute references.", seconds=20,
  facts=[fact("Microsoft: in Excel for Windows, Ctrl+D uses the Fill Down command to copy the contents and format "
              "of the topmost cell of a selected range into the cells below.", MS_EXCEL_KEYS)])

# ================================================================ 12. Digital Payments (1 / 2 / 1)
T = "Digital Payments"
Q(T, "Card security", "Basic",
  "When a customer pays at a shop with her DEBIT card, where does the money come from?",
  ["Directly from her own bank account linked to the card", "From a credit limit that she repays later",
   "From the shop's bank account", "From a prepaid balance stored on the card's magnetic stripe"],
  concept="Debit and credit cards",
  explanation="A debit card draws the payment directly from the cardholder's linked bank account. A credit card "
              "uses a credit limit given by the issuer, which the cardholder repays later.",
  steps=["Debit card -> money from the linked account"],
  wrong="A credit limit is how a credit card works. The shop's account receives the money; it does not pay. The "
        "magnetic stripe stores card data, not a balance.", seconds=10)
Q(T, "Payment technology", "Intermediate",
  "Under the Cheque Truncation System (CTS), what moves from the presenting bank to the paying bank for clearing?",
  ["An electronic image of the cheque with its data, while the physical cheque stays with the presenting bank",
   "The physical cheque, sent by courier to the paying bank", "Only an SMS with the cheque number",
   "A UPI collect request generated from the cheque"],
  concept="Cheque truncation",
  explanation="Cheque truncation stops the flow of the physical cheque during clearing as soon as an electronic "
              "image is generated. The presenting bank captures the image and data and sends them to the clearing "
              "house; the paper cheque is retained by the presenting bank.",
  steps=["Truncation = stop the paper", "Image + data travel electronically"],
  wrong="Moving the paper cheque is the old system CTS replaced. An SMS alone or a UPI request is not how cheques "
        "are cleared.", seconds=20,
  facts=[fact("RBI FAQ: cheque truncation means stopping the flow of a physical cheque during the course of a "
              "clearing cycle, immediately on generation of an electronic image for transmission.", RBI_CHEQUE_FAQ)])
Q(T, "Payment technology", "Intermediate",
  "A customer loads Rs 2,000 into a mobile wallet in advance and later uses that stored value to pay for "
  "groceries and recharge his phone. Under RBI regulation, such a wallet is a type of:",
  ["Prepaid Payment Instrument (PPI)", "Credit card", "Current account", "Cheque"],
  concept="Prepaid payment instruments",
  explanation="RBI classifies instruments that let holders buy goods and services, and use financial services and "
              "remittances, against value stored in them as Prepaid Payment Instruments. PPIs can be cards, wallets "
              "or other forms.",
  steps=["Money loaded in advance + spent later -> PPI"],
  wrong="A credit card spends borrowed money. A current account is a bank deposit account. A cheque is a paper "
        "instruction to a bank.", seconds=20,
  facts=[fact("RBI FAQ: PPIs are instruments that facilitate purchase of goods and services, financial services and "
              "remittances against the value stored on them; they can be issued as cards, wallets or other "
              "forms.", RBI_PPI_FAQ)])
Q(T, "Payment technology", "Advanced",
  "A company issues a cheque of Rs 3,00,000 and, before it is presented, sends its bank the cheque's key details "
  "(date, payee, amount and so on) through net banking, so that the bank can match them when the cheque arrives "
  "in clearing. Which RBI-mandated mechanism is this, and from what cheque amount must banks enable it for "
  "account holders?",
  ["Positive Pay System; for cheques of Rs 50,000 and above",
   "Positive Pay System; only for cheques of Rs 5,00,000 and above",
   "Cheque Truncation System; for cheques of Rs 10,000 and above",
   "NACH mandate; for all cheques"],
  concept="Positive Pay for cheques",
  explanation="Under the Positive Pay System, which took effect on 1 January 2021, the issuer re-confirms key "
              "details of a large-value cheque before it is presented, and CTS checks the presented cheque against "
              "them. Banks must enable it for all account holders issuing cheques of Rs 50,000 and above; its use "
              "is at the customer's discretion, though banks may make it mandatory for Rs 5,00,000 and above.",
  steps=["Issuer pre-confirms cheque details -> Positive Pay", "Enabled for Rs 50,000 and above"],
  wrong="Rs 5,00,000 is the level above which banks MAY make it mandatory, not the threshold for enabling it. CTS "
        "is the image-based clearing system itself. NACH handles bulk and recurring electronic mandates.",
  seconds=40,
  facts=[fact("RBI circular (25 September 2020): banks shall enable Positive Pay for all account holders issuing "
              "cheques for amounts of Rs 50,000 and above, may consider making it mandatory for Rs 5,00,000 and "
              "above; implemented from 1 January 2021.", RBI_PPS)])

# ================================================================ 13. Computer Abbreviations (2 / 1 / 4)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic",
  "Banks send transaction alerts to customers' phones as SMS. What does SMS stand for?",
  ["Short Message Service", "Secure Mobile System", "Simple Mail Service", "Standard Messaging Software"],
  concept="Mobile abbreviations",
  explanation="SMS = Short Message Service, the text-messaging service of mobile networks.",
  steps=["SMS = Short Message Service"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic",
  "Old branch records were archived on CDs. What does CD stand for?",
  ["Compact Disc", "Computer Data", "Central Drive", "Copy Device"],
  concept="Storage abbreviations",
  explanation="CD = Compact Disc, an optical disc that holds about 700 MB.",
  steps=["CD = Compact Disc"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "A customer transfers money to another bank's account through NEFT, a nation-wide payment system owned and "
  "operated by the RBI. What does NEFT stand for?",
  ["National Electronic Funds Transfer", "Net Electronic Fund Transaction", "National Exchange for Fast Transfer",
   "New Electronic Financial Transfer"],
  concept="Payment-system abbreviations",
  explanation="NEFT = National Electronic Funds Transfer, a nation-wide centralised payment system owned and "
              "operated by the Reserve Bank of India.",
  steps=["NEFT = National Electronic Funds Transfer"], wrong="The other expansions are made up.", seconds=10,
  facts=[fact("RBI FAQ: National Electronic Funds Transfer (NEFT) is a nation-wide centralised payment system owned "
              "and operated by the Reserve Bank of India.", RBI_NEFT_FAQ)])
Q(T, S, "Advanced",
  "IBM mainframes, still used by some banks' core systems, encode characters in EBCDIC rather than ASCII. What "
  "does EBCDIC stand for?",
  ["Extended Binary Coded Decimal Interchange Code", "Enhanced Binary Character Data Interchange Code",
   "Extended Byte Code for Digital Information Change", "Electronic Binary Coded Data Interface Code"],
  concept="Character-code abbreviations",
  explanation="EBCDIC = Extended Binary Coded Decimal Interchange Code, the 8-bit character encoding used on IBM "
              "mainframe and midrange systems.",
  steps=["EBCDIC = Extended Binary Coded Decimal Interchange Code"], wrong="The other expansions are made up.",
  seconds=15,
  facts=[fact("IBM documentation: IBM devices attached to host computers use the Extended Binary Coded Decimal "
              "Interchange Code (EBCDIC) to represent single-byte characters.", IBM_EBCDIC)])
Q(T, S, "Advanced",
  "The global coordination of domain names and IP address allocation is overseen by ICANN. What does ICANN stand "
  "for?",
  ["Internet Corporation for Assigned Names and Numbers", "International Council for Addresses and Network Names",
   "Internet Committee for Allocation of Network Numbers", "International Corporation for Address Naming Networks"],
  concept="Internet governance abbreviations",
  explanation="ICANN = Internet Corporation for Assigned Names and Numbers; it coordinates the internet's unique "
              "identifiers, such as domain names and IP address allocation to regional registries.",
  steps=["ICANN = Internet Corporation for Assigned Names and Numbers"], wrong="The other expansions are made up.",
  seconds=15,
  facts=[fact("ICANN's own page gives its name as Internet Corporation for Assigned Names and Numbers and describes "
              "its coordination of domain names and IP addresses.", ICANN_WHAT)])
Q(T, S, "Advanced",
  "Desktop PCs in a branch get their DC power from an SMPS inside the cabinet. What does SMPS stand for?",
  ["Switched-Mode Power Supply", "Standard Main Power Source", "System Memory Power Switch",
   "Single Mode Power Stabiliser"],
  concept="Hardware abbreviations",
  explanation="SMPS = Switched-Mode Power Supply, which converts AC mains power to the low DC voltages a computer "
              "needs by switching transistors rapidly, which makes it small and efficient.",
  steps=["SMPS = Switched-Mode Power Supply"], wrong="The other expansions are made up.", seconds=15)
Q(T, S, "Advanced",
  "Net-banking sites are protected by TLS, the successor to SSL; its current version is defined in RFC 8446. What "
  "does TLS stand for?",
  ["Transport Layer Security", "Transmission Line Security", "Trusted Link Service", "Transfer Level Secure"],
  concept="Security protocol abbreviations",
  explanation="TLS = Transport Layer Security, the protocol that encrypts and authenticates connections such as "
              "HTTPS.",
  steps=["TLS = Transport Layer Security"], wrong="The other expansions are made up.", seconds=15,
  facts=[fact("RFC 8446 is titled 'The Transport Layer Security (TLS) Protocol Version 1.3'.", RFC8446)])

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_010_plan.json").read_text(encoding="utf-8"))
cplan = next(s for s in plan["subjects"] if s["subject"] == CK)
want = Counter({(t["topic"], d): n for t in cplan["topics"] for d, n in t["quota"].items() if n})
got = Counter((q["topic"], q["difficulty"]) for q in questions)
assert got == want, (got - want, want - got)
subs = {t["topic"]: set(t["subtopics"]) for t in cplan["topics"]}
for q in questions:
    assert q["subtopic"] in subs[q["topic"]], (q["question_id"], q["subtopic"])
    assert q["solution"]["final_answer"].startswith(f"Option {q['correct_answer']}: ")
assert len(questions) == cplan["total"] == 99
assert questions[0]["question_id"] == cplan["question_ids"][0] and questions[-1]["question_id"] == cplan["question_ids"][1]
assert stimuli[0]["stimulus_id"] == cplan["stimulus_id_start"]
for s in stimuli:
    pos = [q["set_position"] for q in questions if q.get("stimulus_id") == s["stimulus_id"]]
    assert pos == list(range(1, len(pos) + 1)) and 3 <= len(pos) <= 6, (s["stimulus_id"], pos)
keys = Counter(q["correct_answer"] for q in questions)
assert max(keys.values()) <= 28 and min(keys.values()) >= 21, keys

n_set = sum(1 for q in questions if q.get("stimulus_id"))
batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_010",
    "created_at": TODAY,
    "notes": f"BATCH_010 Computer Knowledge part (final Computer batch): 99 original, mostly scenario-based "
             f"questions (BANK_COMP_000902 to BANK_COMP_001000), {n_set} of them in six shared sets "
             "(STIM_COMP_010001-010006: status word of a note-sorting machine, a teaching accumulator processor, "
             "overnight batch jobs on an EOD server, DNS records seen by a branch PC, a Cheques table for SQL and an "
             "Excel gold-loan register). Computable answers are re-derived in tools/batch_010/computer.py (bit "
             "fields, octal, rotation, a processor simulation, priority scheduling, TTL, set-associative mapping, "
             "TLB access time, printer bitmap, stop-and-wait, IPv4 fragmentation, toy RSA, SQL in sqlite3 with > ALL "
             "checked in Python, and Excel PROPER / EOMONTH / DATEDIF checked against Microsoft's own examples or "
             "definitions). Facts were checked on 2026-11-05 on RFC, Microsoft, MDN, man7, GNU, OWASP, NIST, IEEE, "
             "ICANN, IBM, RBI, DARPA, CERN, US Census Bureau, LibreOffice, Google and Wikipedia pages.",
    "stimuli": stimuli,
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_010_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
