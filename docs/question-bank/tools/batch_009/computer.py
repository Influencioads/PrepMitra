"""Writes batches/parts/BATCH_009_COMP.json: the 99 Computer Knowledge questions of BATCH_009.

BATCH_009 builds applied scenarios around six shared stimuli (error checks on a cash-recycler link, a branch CCTV
recording system, a branch firewall rule table, complaints at a bank's cyber cell, a Staff table for SQL and an Excel
ATM cash-loading register). Every computable answer is re-derived below with assertions before the file is written:
Hamming distances and the minimum distance of the code, a CRC remainder by modulo-2 division, arithmetic shift and
bit masking, MIPS, 8-bit flags, byte order, postfix evaluation and a bubble-sort pass (simulated), internal
fragmentation, ADC step size, CCTV bit-rate / storage / RAID 6 / retention, DRAM refresh interval, SSD write
amplification, first-match firewall evaluation with ipaddress, SQL in sqlite3 (self-join, COALESCE, cross join,
correlated subquery, DENSE_RANK) and Excel LEFT / ROUNDUP / TEXT / NETWORKDAYS / IFS. The plan quota per (topic,
difficulty), subtopics, the ID range, stimulus IDs and the answer-key balance are also asserted. If any assertion
fails, nothing is written.

    python tools/batch_009/computer.py      (run from docs/question-bank)
"""

import datetime as dt
import ipaddress
import itertools
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
FIRST_ID = 803
SELF = "ai:self-recheck"
REC = "script:recompute"
IND = "ai:independent-check"
SC = "web:search-confirmed"
# A separate fresh subagent answered every question from a key-free dump (tools output in the author's scratchpad).
# BLIND_DONE is switched on only after that check; IDs it did not match are listed in BLIND_MISMATCH and do not get
# ai:independent-check.
BLIND_DONE = True
BLIND_MISMATCH = set()

_rng = random.Random(20261105 + 9)
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
    sid = f"STIM_COMP_009{_stim_no[0]:03d}"
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
def ham(a, b):
    return sum(x != y for x, y in zip(a, b))


CODE = ["000000", "001111", "110011", "111100"]
DMIN = min(ham(a, b) for a, b in itertools.combinations(CODE, 2))
assert DMIN == 4 and (DMIN - 1) == 3 and (DMIN - 1) // 2 == 1
RECV = "011111"
assert {c: ham(RECV, c) for c in CODE} == {"000000": 5, "001111": 1, "110011": 3, "111100": 3}


def crc_rem(msg, gen):
    bits = [int(c) for c in msg + "0" * (len(gen) - 1)]
    g = [int(c) for c in gen]
    for i in range(len(msg)):
        if bits[i]:
            for j in range(len(g)):
                bits[i + j] ^= g[j]
    return "".join(map(str, bits[-(len(gen) - 1):]))


CRC = crc_rem("1101", "1011")
assert CRC == "001"
assert format(0b1101 ^ 0b1011, "03b") == "110" and int("1101000", 2) % 11 == 5


# 8-bit two's complement arithmetic right shift
def to_s8(b):
    v = int(b, 2)
    return v - 256 if v >= 128 else v


def asr(b, n):
    v = to_s8(b) >> n
    return format(v & 0xFF, "08b")


assert to_s8("11101000") == -24 and asr("11101000", 2) == "11111010" and to_s8("11111010") == -6
assert format(int("11101000", 2) >> 2, "08b") == "00111010" and int("00111010", 2) == 58
# masking: clear bit 2 of 10110110
assert format(0b10110110 & 0b11111011, "08b") == "10110010"
assert format(0b10110110 | 0b00000100, "08b") == "10110110"  # OR would leave the bit set
assert format(0b10110110 ^ 0b11111011, "08b") == "01001101"
assert 0b10110110 & 0b00000100 == 0b100
# MIPS = clock / (CPI x 10^6)
assert 2.4e9 / (1.6 * 1e6) == 1500
# Flags after 8-bit addition F0 + 10
s = 0xF0 + 0x10
assert s == 0x100 and (s & 0xFF) == 0 and (s >> 8) == 1
assert to_s8(format(0xF0, "08b")) == -16  # -16 + 16 = 0: no signed overflow
# Network byte order of 10.20.30.40
assert int(ipaddress.ip_address("10.20.30.40")).to_bytes(4, "big")[0] == 0x0A
assert int(ipaddress.ip_address("10.20.30.40")) == 0x0A141E28


# Postfix evaluation 6 2 3 + * 4 -
def postfix(expr):
    st = []
    for t in expr.split():
        if t.isdigit():
            st.append(int(t))
        else:
            b, a = st.pop(), st.pop()
            st.append({"+": a + b, "-": a - b, "*": a * b}[t])
    assert len(st) == 1
    return st[0]


assert postfix("6 2 3 + * 4 -") == 26 and 4 - 30 == -26 and 6 + 2 * 3 - 4 == 8


def bubble_pass(a):
    a = list(a)
    for i in range(len(a) - 1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
    return a


P1 = bubble_pass([42, 17, 58, 9, 33])
assert P1 == [17, 42, 9, 33, 58] and bubble_pass(P1) == [17, 9, 33, 42, 58]
# Internal fragmentation: 18,000 bytes in 4 KB pages
PAGES = -(-18000 // 4096)
assert PAGES == 5 and PAGES * 4096 - 18000 == 2480 and 18000 - 4 * 4096 == 1616
# ADC step: 12-bit over 0-3.3 V
assert round(3.3 / 4096 * 1000, 3) == 0.806 and round(3.3 / 2048 * 1000, 3) == 1.611
assert round(3.3 / 256 * 1000, 3) == 12.891 and round(3.3 / 12 * 1000) == 275

# CCTV: 8 cameras x 4 Mbps, RAID 6 of six 4 TB disks (decimal units)
CAMS, MBPS = 8, 4
TOTAL_MBPS = CAMS * MBPS
assert TOTAL_MBPS == 32 and TOTAL_MBPS / 50 * 100 == 64
GB_DAY = TOTAL_MBPS * 86400 / 8 / 1000
assert GB_DAY == 345.6 and GB_DAY / 24 == 14.4 and GB_DAY / 8 == 43.2
RAID6 = (6 - 2) * 4
PARITY_DISKS = 2  # RAID 6: survives as many simultaneous failures as it has parity blocks per stripe
assert 0x3F == 0b00111111 and 16 == 2 ** 4 and len(format(0xF, "b")) == 4
assert RAID6 == 16 and RAID6 == (6 - PARITY_DISKS) * 4 and (6 - 1) * 4 == 20 and 6 * 4 == 24
DAYS = int(RAID6 * 1000 // GB_DAY)
assert DAYS == 46 and int(20000 // GB_DAY) == 57 and int(24000 // GB_DAY) == 69 and int(16000 // 43.2) == 370
# DRAM refresh: 8,192 rows every 64 ms
assert 64e-3 / 8192 * 1e6 == 7.8125
# SSD write amplification
assert 250 / 100 == 2.5

# Firewall: first match wins, implicit deny
RULES = [  # (no, action, proto, src, dst, port)
    (1, "Allow", "TCP", "10.20.30.0/24", "any", 443),
    (2, "Deny", "TCP", "any", "any", 3389),
    (3, "Allow", "TCP", "10.20.30.10/32", "10.20.0.0/16", 3389),
    (4, "Allow", "TCP", "10.20.30.0/24", "10.20.0.25/32", 993),
    (5, "Allow", "UDP", "10.20.30.0/24", "10.20.0.53/32", 53),
]


def inside(ip, net):
    return net == "any" or ipaddress.ip_address(ip) in ipaddress.ip_network(net)


def fw(proto, src, dst, port, rules=RULES):
    for no, act, p, s_, d_, pt in rules:
        if p == proto and inside(src, s_) and inside(dst, d_) and pt == port:
            return no, act
    return None, "Deny"


assert fw("UDP", "10.20.30.44", "10.20.0.53", 53) == (5, "Allow")
assert fw("TCP", "10.20.30.10", "10.20.0.70", 3389) == (2, "Deny")
assert fw("TCP", "10.20.30.10", "10.20.0.70", 3389, [RULES[2], RULES[1]] + [RULES[0]] + RULES[3:]) == (3, "Allow")
assert fw("TCP", "10.20.31.5", "203.0.113.80", 443) == (None, "Deny")
assert fw("TCP", "10.20.30.44", "203.0.113.80", 443) == (1, "Allow")

# SQL: Staff table
STAFF = [("E1", "Asha", "Pune", 90000, None), ("E2", "Ravi", "Pune", 60000, "E1"),
         ("E3", "Meena", "Delhi", 75000, "E1"), ("E4", "John", "Delhi", 75000, "E3"),
         ("E5", "Farah", "Pune", 62000, "E2"), ("E6", "Kiran", "Delhi", 48000, "E3"),
         ("E7", "Neha", "Agra", 52000, "E1"), ("E8", "Tara", "Agra", 40000, "E7")]
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Staff (emp_id TEXT PRIMARY KEY, name TEXT, branch TEXT, salary INTEGER, manager_id TEXT)")
db.executemany("INSERT INTO Staff VALUES (?, ?, ?, ?, ?)", STAFF)
db.execute("CREATE TABLE Branches (branch TEXT PRIMARY KEY, city_code TEXT)")
db.executemany("INSERT INTO Branches VALUES (?, ?)", [("Pune", "PN"), ("Delhi", "DL"), ("Agra", "AG")])


def col(sql):
    return [r[0] for r in db.execute(sql)]


SQL_SELF = ("SELECT e.name FROM Staff e JOIN Staff m ON e.manager_id = m.emp_id WHERE e.salary > m.salary")
assert col(SQL_SELF) == ["Farah"]
assert col(SQL_SELF.replace(">", ">=")) == ["John", "Farah"] or sorted(col(SQL_SELF.replace(">", ">="))) == \
    ["Farah", "John"]
SQL_COAL = "SELECT COUNT(*) FROM Staff WHERE COALESCE(manager_id, 'E1') = 'E1'"
assert col(SQL_COAL) == [4] and col("SELECT COUNT(*) FROM Staff WHERE manager_id = 'E1'") == [3]
assert col("SELECT COUNT(*) FROM Staff, Branches") == [24]
SQL_CORR = ("SELECT name FROM Staff s WHERE salary > (SELECT AVG(salary) FROM Staff WHERE branch = s.branch) "
            "ORDER BY emp_id")
assert col(SQL_CORR) == ["Asha", "Meena", "John", "Neha"]
assert col("SELECT name FROM Staff WHERE salary > (SELECT AVG(salary) FROM Staff) ORDER BY emp_id") == \
    ["Asha", "Meena", "John"]
DR = dict(db.execute("SELECT name, DENSE_RANK() OVER (ORDER BY salary DESC) FROM Staff").fetchall())
RK = dict(db.execute("SELECT name, RANK() OVER (ORDER BY salary DESC) FROM Staff").fetchall())
assert DR["Farah"] == 3 and RK["Farah"] == 4 and DR["John"] == DR["Meena"] == 2

# Excel: ATM cash-loading register, rows 2-7 (A IFSC, B ATM ID, C load date, D loaded, E dispensed)
ATM = [("PMBK0004521", "ATM-PN-01", dt.date(2026, 10, 26), 2350000, 1880000),
       ("PMBK0004521", "ATM-PN-02", dt.date(2026, 10, 28), 1500000, 600000),
       ("PMBK0007810", "ATM-DL-01", dt.date(2026, 10, 31), 2000000, 1900000),
       ("PMBK0007810", "ATM-DL-02", dt.date(2026, 11, 3), 1800000, 1710000),
       ("PMBK0003302", "ATM-AG-01", dt.date(2026, 11, 4), 1200000, 540000),
       ("PMBK0003302", "ATM-AG-02", dt.date(2026, 11, 5), 900000, 450000)]
assert all(len(r[0]) == 11 and r[0][4] == "0" for r in ATM)
assert ATM[0][0][:4] == "PMBK"
assert -(-ATM[0][3] // 1000000) == 3 and round(ATM[0][3] / 1000000) == 2
assert ATM[2][2].strftime("%A") == "Saturday"


def networkdays(a, b, hol=()):
    n, d = 0, a
    while d <= b:
        if d.weekday() < 5 and d not in hol:
            n += 1
        d += dt.timedelta(days=1)
    return n


# Microsoft's own example: 1-Oct-2012 to 1-Mar-2013 -> 110; with 22-Nov-2012 -> 109; with 3 holidays -> 107
_H = [dt.date(2012, 11, 22), dt.date(2012, 12, 4), dt.date(2013, 1, 21)]
assert networkdays(dt.date(2012, 10, 1), dt.date(2013, 3, 1)) == 110
assert networkdays(dt.date(2012, 10, 1), dt.date(2013, 3, 1), _H[:1]) == 109
assert networkdays(dt.date(2012, 10, 1), dt.date(2013, 3, 1), _H) == 107
HOL = dt.date(2026, 11, 2)
assert networkdays(ATM[0][2], ATM[5][2], (HOL,)) == 8 and networkdays(ATM[0][2], ATM[5][2]) == 9
assert (ATM[5][2] - ATM[0][2]).days + 1 == 11
R5 = ATM[3][4] / ATM[3][3]
assert R5 == 0.95


def ifs(r):
    return "Watch" if r >= 0.6 else ("Reload today" if r >= 0.9 else "OK")


assert ifs(R5) == "Watch"

# ---------------------------------------------------------------- fact-check sources
# Pages opened on 2026-11-05 (web:fact-check)
CHM_TRANSISTOR = "https://www.computerhistory.org/siliconengine/invention-of-the-point-contact-transistor/"
MAN_BYTEORDER = "https://man7.org/linux/man-pages/man3/byteorder.3.html"
MAN_CAT = "https://man7.org/linux/man-pages/man1/cat.1.html"
MS_WIN_KEYS = ("https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-"
               "cb9706c75eec")
RFC2131 = "https://www.rfc-editor.org/rfc/rfc2131"
RFC2453 = "https://www.rfc-editor.org/rfc/rfc2453"
RFC4291 = "https://www.rfc-editor.org/rfc/rfc4291"
RFC8314 = "https://www.rfc-editor.org/rfc/rfc8314"
RFC6585 = "https://www.rfc-editor.org/rfc/rfc6585"
RFC9051 = "https://www.rfc-editor.org/rfc/rfc9051"
MS_RDP = ("https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/"
          "change-listening-port")
MDN_CSP = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP"
MDN_FRAG = "https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment"
MS_NETWORKDAYS = ("https://support.microsoft.com/en-us/office/networkdays-function-48e717bf-a7a3-495f-969e-"
                  "5005e3eb18e7")
MS_TEXT = "https://support.microsoft.com/en-us/office/text-function-20d5ac4d-7b94-49fd-bb38-93d29371225c"
MS_IFS = "https://support.microsoft.com/en-us/office/ifs-function-36329a26-37b2-467c-972b-4a39bd951d45"
MS_ROUNDUP = "https://support.microsoft.com/en-us/office/roundup-function-f8bc9b23-e795-47db-8703-db171d0c42a7"
MS_WORD_KEYS = ("https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-"
                "f762f663ceb2")
MS_PPT_DELIVER = ("https://support.microsoft.com/en-us/office/keyboard-shortcuts-to-deliver-powerpoint-"
                  "presentations-1524ffce-bd2a-45f4-9a7f-f18b992b93a0")
MS_EXCEL_KEYS = ("https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-"
                 "9b7213f0040f")
MS_LINEBREAKS = "https://support.microsoft.com/en-us/Word/line-and-page-breaks"
RBI_NEFT_FAQ = "https://www.rbi.org.in/Scripts/FAQView.aspx?Id=60"
CVE_OVERVIEW = "https://www.cve.org/About/Overview"
WIKI_DUKPT = "https://en.wikipedia.org/wiki/Derived_unique_key_per_transaction"
# Confirmed only in search results (web:search-confirmed)
NPCI_BBPS = "https://www.npci.org.in/PDF/npci/press-releases/2016/NPCI_BBPS_Pilot_launch.pdf"
NPCI_RUPAY_UPI = "https://www.npci.org.in/what-we-do/rupay/rupay-credit-card-on-upi"

# ================================================================ 1. Computer Fundamentals (4 / 2 / 4)
T = "Computer Fundamentals"
S_ERR = new_stim(
    "input_output", "Error checks on a cash-recycler link",
    "A branch's cash-recycling machine talks to its controller over a serial link that uses two error checks.\n\n"
    "**Check 1 - code words.** Each command is sent as one of only four valid 6-bit code words:\n\n"
    "| Command | Code word |\n|---|---|\n| IDLE | 000000 |\n| COUNT | 001111 |\n| DISPENSE | 110011 |\n"
    "| LOCK | 111100 |\n\nThe Hamming distance between two words is the number of bit positions in which they "
    "differ. A received word that is not valid is corrected to the nearest valid code word.\n\n"
    "**Check 2 - CRC.** Status messages are 4 bits long. The sender appends 3 zeros to the message, divides the "
    "result by the generator 1011 using modulo-2 (XOR) division with no carries or borrows, and appends the 3-bit "
    "remainder to the message as the CRC.",
    "Every pair of valid code words differs in exactly 4 positions, so the minimum distance is 4: up to 3 bit errors "
    "are always detected and 1 bit error can always be corrected. 011111 is 1 bit from COUNT (001111). For the "
    "message 1101, 1101000 divided by 1011 leaves the remainder 001, so 1101001 is sent.")
o = ["001111 (COUNT)", "000000 (IDLE)", "110011 (DISPENSE)", "111100 (LOCK)"]
Q(T, "Number systems", "Intermediate",
  "Refer to the cash-recycler link. The controller receives the invalid word 011111. To which valid code word "
  "will it be corrected?", o,
  concept="Hamming distance and nearest-code-word correction",
  explanation="Count the positions in which 011111 differs from each valid word: from 000000 it differs in 5 "
              "positions, from 001111 in 1 (the second bit), from 110011 in 3 and from 111100 in 3. The nearest "
              "valid word is 001111 (COUNT), so a single flipped bit is assumed.",
  steps=["d(011111, 000000) = 5", "d(011111, 001111) = 1", "d(011111, 110011) = 3", "d(011111, 111100) = 3",
         "Nearest = 001111"],
  shortcut="XOR the two words and count the 1s.",
  wrong="IDLE is 5 bits away. DISPENSE and LOCK are each 3 bits away, so they are less likely than a single-bit "
        "error from COUNT.", seconds=45, computed=True, stim=S_ERR, pos=1)
o = ["Detect up to 3 bit errors; correct 1 bit error", "Detect up to 4 bit errors; correct 2 bit errors",
     "Detect up to 3 bit errors; correct 2 bit errors", "Detect up to 2 bit errors; correct 1 bit error"]
Q(T, "Number systems", "Advanced",
  "Refer to the cash-recycler link. Considering the minimum Hamming distance between the four valid code words, "
  "how many bit errors in one word can the code always detect, and how many can it always correct?", o,
  concept="Minimum distance and error-control capability",
  explanation="All six pairs of valid words differ in exactly 4 bits, so the minimum distance d = 4. A code with "
              "minimum distance d always detects up to d - 1 = 3 errors (3 flips cannot turn one valid word into "
              "another) and always corrects up to floor((d - 1) / 2) = 1 error.",
  steps=["Pairwise distances are all 4 -> d = 4", "Detect: d - 1 = 3", "Correct: floor(3 / 2) = 1"],
  wrong="Detecting 4 errors is not guaranteed: 4 flips can turn one valid word into another. Correcting 2 errors "
        "needs d >= 5. Saying only 2 errors are detected understates the capability.", seconds=60, computed=True,
  stim=S_ERR, pos=2)
o, a = ordered(int(CRC, 2), [0b110, 0b101, 0b111], fmt=lambda v: format(v, "03b"))
Q(T, "Number systems", "Advanced",
  "Refer to the cash-recycler link. Which 3-bit CRC is appended to the status message 1101?", o, a,
  concept="Cyclic redundancy check (modulo-2 division)",
  explanation="Append three zeros: 1101000. Divide by 1011 with XOR: 1101 XOR 1011 = 0110; bring down 0 -> 1100; "
              "1100 XOR 1011 = 0111; bring down 0 -> 1110; 1110 XOR 1011 = 0101; bring down 0 -> 1010; 1010 XOR "
              "1011 = 0001. The remainder is 001, so the frame sent is 1101001.",
  steps=["1101000 / 1011 (XOR)", "1101 ^ 1011 = 110", "1100 ^ 1011 = 111", "1110 ^ 1011 = 101",
         "1010 ^ 1011 = 001", "CRC = 001"],
  wrong="110 is the remainder if the three zeros are not appended (1101 XOR 1011). 101 is the remainder of "
        "ordinary integer division (104 mod 11 = 5), which uses borrows. 111 stops the division after the second "
        "step.", seconds=90, computed=True, stim=S_ERR, pos=3)
Q(T, "Number systems", "Basic",
  "A memory dump shows each byte as two hexadecimal digits, for example 3F. How many binary bits does ONE "
  "hexadecimal digit stand for?", ["4", "2", "8", "16"],
  concept="Hexadecimal and binary",
  explanation="16 = 2^4, so each hexadecimal digit (0 to F) corresponds to exactly 4 bits. Two hex digits make 8 "
              "bits, which is one byte.",
  steps=["16 = 2^4", "1 hex digit = 4 bits", "3F = 0011 1111"],
  wrong="8 bits is one byte, which needs two hex digits. 16 is the base of the system, not its bit count. 2 bits "
        "can show only 4 values.", seconds=15, computed=True)
o = ["AND with 11111011", "OR with 00000100", "XOR with 11111011", "AND with 00000100"]
Q(T, "Number systems", "Advanced",
  "An ATM's 8-bit status register holds 1011 0110. Bit 2 (counting the rightmost bit as bit 0) is the 'door open' "
  "flag. Which single operation switches OFF bit 2 only and leaves all the other bits unchanged?", o,
  concept="Bit masking with AND, OR and XOR",
  explanation="ANDing with 1 keeps a bit and ANDing with 0 clears it. The mask 11111011 has a 0 only in bit 2, so "
              "1011 0110 AND 1111 1011 = 1011 0010: bit 2 is cleared and every other bit is kept.",
  steps=["Need: clear bit 2, keep the rest", "Mask with 0 at bit 2, 1 elsewhere = 11111011",
         "10110110 AND 11111011 = 10110010"],
  wrong="OR with 00000100 sets bit 2 (it stays 1). XOR with 11111011 flips every bit except bit 2 (gives "
        "01001101). AND with 00000100 clears every bit except bit 2.", seconds=50, computed=True)
o = ["11111010", "00111010", "11110100", "10111010"]
Q(T, "Number systems", "Advanced",
  "A register holds the 8-bit two's-complement value 11101000 (that is, -24). The processor performs an "
  "ARITHMETIC right shift by 2 places, which copies the sign bit into the vacated positions. What does the "
  "register hold now?", o,
  concept="Arithmetic vs logical shift",
  explanation="An arithmetic right shift moves the bits right and refills the left with copies of the sign bit "
              "(1 here), so the sign is kept and the value is divided by 2 for each place: -24 / 4 = -6, which is "
              "11111010.",
  steps=["11101000 >> 1 (arithmetic) = 11110100 (-12)", ">> 1 again = 11111010 (-6)"],
  shortcut="Arithmetic right shift by n = divide by 2^n (rounding towards minus infinity).",
  wrong="00111010 is a logical shift that fills with zeros (it reads as +58). 11110100 is a shift by only one "
        "place. 10111010 keeps the sign bit but fills the next places with zeros.", seconds=60, computed=True)
Q(T, "Types of computers", "Basic",
  "The speed of supercomputers used for weather forecasting is compared in units such as petaFLOPS. What does "
  "FLOPS measure?",
  ["Floating-point operations per second", "Files loaded per second", "Frames of light processed per second",
   "Fixed logical operations per cycle"],
  concept="Measuring supercomputer performance",
  explanation="FLOPS (floating-point operations per second) counts how many calculations on real (decimal) numbers "
              "a computer completes each second. Supercomputers are ranked in petaFLOPS (10^15) and exaFLOPS "
              "(10^18).",
  steps=["FLOPS = floating-point operations per second"],
  wrong="The other expansions are made up; FLOPS is a rate of floating-point arithmetic.", seconds=15)
Q(T, "Generations and history", "Basic",
  "In the usual classification of computer generations, which generation is associated with artificial "
  "intelligence, natural-language processing and parallel processing, based on ULSI technology?",
  ["Fifth generation", "Third generation", "Second generation", "First generation"],
  concept="Generations of computers",
  explanation="The fifth generation (from the 1980s onwards in most textbooks) aims at intelligent systems: "
              "artificial intelligence, natural-language understanding, parallel processing and ULSI chips.",
  steps=["AI + ULSI + parallel processing = fifth generation"],
  wrong="The first used vacuum tubes, the second transistors and the third integrated circuits.", seconds=15)
Q(T, "Generations and history", "Basic",
  "Which ancient calculating tool, still used to teach arithmetic, works by sliding beads along rods in a frame?",
  ["Abacus", "Slide rule", "Napier's bones", "Pascaline"],
  concept="Early calculating devices",
  explanation="The abacus is one of the earliest calculating aids: beads on rods stand for units, tens, hundreds "
              "and so on, and numbers are added or subtracted by moving the beads.",
  steps=["Beads on rods = abacus"],
  wrong="A slide rule uses sliding logarithmic scales. Napier's bones are numbered rods for multiplication, with "
        "no beads. The Pascaline is Pascal's geared mechanical adder.", seconds=15)
Q(T, "Generations and history", "Intermediate",
  "Second-generation computers replaced vacuum tubes with transistors. Where, and by whom, was the first "
  "working (point-contact) transistor demonstrated in December 1947?",
  ["At Bell Labs, by John Bardeen and Walter Brattain", "At IBM, by Howard Aiken and Grace Hopper",
   "At Intel, by Gordon Moore and Robert Noyce", "At the University of Pennsylvania, by Eckert and Mauchly"],
  concept="Invention of the transistor",
  explanation="John Bardeen and Walter Brattain achieved transistor action in a germanium point-contact device at "
              "Bell Laboratories in December 1947 (working with William Shockley's group). The transistor became "
              "the switching element of second-generation computers.",
  steps=["Transistor, 1947 = Bardeen and Brattain at Bell Labs"],
  wrong="Aiken and Hopper are linked to the Harvard Mark I. Intel was founded in 1968. Eckert and Mauchly built "
        "ENIAC, which used vacuum tubes.", seconds=20,
  facts=[fact("CHM Silicon Engine: Bardeen and Brattain achieved transistor action in a germanium point-contact "
              "device at Bell Labs in December 1947.", CHM_TRANSISTOR)])

# ================================================================ 2. Hardware (1 / 2 / 3)
T = "Hardware"
Q(T, "Motherboard and ports", "Basic",
  "A branch's server room has four servers but only one keyboard, one monitor and one mouse. Which device lets "
  "the administrator control all four servers from that single set by switching between them?",
  ["KVM switch", "Network switch", "Modem", "UPS"],
  concept="KVM switches",
  explanation="A KVM (Keyboard, Video, Mouse) switch connects one keyboard, monitor and mouse to several computers "
              "and lets the user choose which computer they control at any moment.",
  steps=["One keyboard/monitor/mouse for many computers = KVM switch"],
  wrong="A network switch connects computers to a LAN. A modem converts signals for a telephone or cable line. A "
        "UPS supplies backup power.", seconds=15)
Q(T, "CPU and components", "Intermediate",
  "When a program calls a function, the CPU pushes the return address onto the stack in memory and later pops it "
  "back. Which CPU register always holds the address of the current top of the stack?",
  ["Stack Pointer (SP)", "Program Counter (PC)", "Instruction Register (IR)", "Memory Data Register (MDR)"],
  concept="Special-purpose registers",
  explanation="The Stack Pointer holds the address of the top of the stack. A push stores data there and moves "
              "SP; a pop reads from SP and moves it back. Calls, returns and interrupts all use it.",
  steps=["Top of stack address = Stack Pointer"],
  wrong="The PC holds the address of the next instruction. The IR holds the instruction being executed. The MDR "
        "holds data moving to or from memory.", seconds=20)
Q(T, "CPU and components", "Intermediate",
  "The microcontroller inside a POS terminal has one memory for program instructions and a separate memory for "
  "data, each with its own bus, so it can fetch an instruction and read data in the same cycle. Which architecture "
  "is this?",
  ["Harvard architecture", "Von Neumann architecture", "Client-server architecture", "Pipeline architecture"],
  concept="Harvard vs von Neumann architecture",
  explanation="In the Harvard architecture, instructions and data are kept in separate memories with separate "
              "paths, so both can be accessed at once. It is common in microcontrollers and signal processors.",
  steps=["Separate instruction and data memories and buses = Harvard"],
  wrong="Von Neumann uses one shared memory and path for both. Client-server describes network computing. "
        "Pipelining overlaps instruction stages and does not by itself mean separate memories.", seconds=20)
o, a = ordered(1500, [667, 2400, 3840], fmt=lambda v: f"{v:,} MIPS")
Q(T, "CPU and components", "Advanced",
  "A processor runs at 2.4 GHz and, for a bank's batch program, needs on average 1.6 clock cycles per instruction "
  "(CPI). What is its rating in MIPS (million instructions per second) for this program?", o, a,
  concept="MIPS rating",
  explanation="MIPS = clock rate / (CPI x 10^6) = 2.4 x 10^9 / (1.6 x 10^6) = 1,500.",
  steps=["Instructions per second = 2.4 x 10^9 / 1.6 = 1.5 x 10^9", "Divide by 10^6 -> 1,500 MIPS"],
  wrong="3,840 multiplies by the CPI instead of dividing. 2,400 ignores the CPI. 667 divides the CPI by the clock "
        "in GHz.", seconds=45, computed=True)
o = ["Result 00 (hex); Carry flag = 1; Zero flag = 1", "Result 100 (hex); Carry flag = 0; Zero flag = 0",
     "Result 00 (hex); Carry flag = 0; Zero flag = 1", "Result 00 (hex); Carry flag = 1; Zero flag = 0"]
Q(T, "CPU and components", "Advanced",
  "An 8-bit processor adds F0 (hex) and 10 (hex). The result is kept in an 8-bit register, and the ALU sets the "
  "Carry flag if a carry goes out of bit 7 and the Zero flag if the 8-bit result is zero. What is the outcome?", o,
  concept="ALU status flags",
  explanation="F0 + 10 = 100 (hex), which needs 9 bits. The register keeps the low 8 bits, 00, and the 9th bit "
              "goes out as a carry, so Carry = 1. The stored result is zero, so Zero = 1.",
  steps=["F0 + 10 = 100 hex", "8-bit result = 00 -> Zero = 1", "Bit 8 = 1 -> Carry = 1"],
  wrong="100 cannot fit in 8 bits. The carry out of bit 7 must be recorded. The Zero flag looks at the stored 8-bit "
        "result, which is 00.", seconds=50, computed=True)
o = ["0A", "28", "14", "1E"]
Q(T, "CPU and components", "Advanced",
  "A branch PC with a little-endian processor sends the IPv4 address 10.20.30.40 (hex 0A 14 1E 28) inside a "
  "packet header. Before sending, the program converts the value to network byte order. Which byte goes out "
  "first?", o,
  concept="Network byte order (big-endian)",
  explanation="Internet protocols send multi-byte numbers most significant byte first (big-endian), whatever the "
              "host's own byte order. Functions such as htonl() convert from host order. The most significant byte "
              "of 0A141E28 is 0A, so it is sent first.",
  steps=["Network byte order = most significant byte first", "0A 14 1E 28 -> 0A first"],
  wrong="28 is the least significant byte, which a little-endian host stores first in its own memory but which "
        "is not sent first. 14 and 1E are middle bytes.", seconds=40, computed=True,
  facts=[fact("man7 byteorder(3): network byte order, as used on the Internet, is Most Significant Byte first; "
              "htonl() converts from host byte order to network byte order.", MAN_BYTEORDER)])

# ================================================================ 3. Software (3 / 4 / 2)
T = "Software"
Q(T, "Programming languages", "Basic",
  "Before writing code for an EMI calculator, a trainee lists the exact steps: read the loan amount, read the rate, "
  "read the tenure, apply the formula, show the EMI. A finite, ordered set of clear steps that solves a problem is "
  "called a(n):", ["Algorithm", "Compiler", "Operating system", "Database"],
  concept="Algorithms",
  explanation="An algorithm is a finite sequence of well-defined steps that solves a problem. It can be written in "
              "plain language, pseudocode or a flowchart before being coded in any language.",
  steps=["Ordered, finite steps to solve a problem = algorithm"],
  wrong="A compiler translates programs. An operating system manages the computer. A database stores data.",
  seconds=15)
Q(T, "System and application software", "Basic",
  "A bank hires a software firm to build a loan-tracking program designed only for its own procedures and forms, "
  "instead of buying a ready-made product sold to many customers. Such software is called:",
  ["Custom (tailor-made) software", "Packaged (off-the-shelf) software", "Firmware", "Utility software"],
  concept="Custom vs packaged software",
  explanation="Custom (bespoke) software is developed for the specific needs of one organisation. Packaged "
              "(off-the-shelf) software is made once and sold to many users.",
  steps=["Built for one organisation's needs = custom software"],
  wrong="Packaged software is the ready-made alternative the bank chose not to buy. Firmware is stored in a "
        "device's chip. Utility software maintains the computer.", seconds=15)
Q(T, "Licensing", "Basic",
  "An employee copies a licensed office suite from the branch PC and installs it on ten home computers of his "
  "friends without buying licences. What is this called?",
  ["Software piracy", "Open-source distribution", "Freeware sharing", "Software patching"],
  concept="Software piracy",
  explanation="Copying, installing or distributing licensed software beyond what the licence allows, without "
              "paying for it, is software piracy and infringes the publisher's copyright.",
  steps=["Unlicensed copying of paid software = piracy"],
  wrong="Open-source and freeware licences allow sharing, but this suite is licensed per installation. Patching "
        "means installing fixes.", seconds=15)
Q(T, "Licensing", "Intermediate",
  "A bank pays once for a version of an accounting package and may keep using that version for as long as it "
  "likes, with no recurring fee (updates to later versions may cost extra). What type of licence is this?",
  ["Perpetual licence", "Subscription licence", "Trial licence", "Public-domain licence"],
  concept="Perpetual vs subscription licences",
  explanation="A perpetual licence is a one-time purchase that gives the right to use the licensed version "
              "indefinitely. A subscription licence must be renewed (monthly or yearly) or the software stops "
              "being licensed.",
  steps=["Pay once + use indefinitely = perpetual licence"],
  wrong="A subscription needs recurring payments. A trial ends after a fixed period. Public-domain software has no "
        "copyright and needs no purchase.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "An analyst writes SELECT branch, SUM(amount) FROM Loans GROUP BY branch; stating WHAT result is wanted rather "
  "than the step-by-step procedure to get it. In the generations of programming languages, SQL is usually "
  "classed as a:",
  ["Fourth-generation language (4GL)", "First-generation language (machine language)",
   "Second-generation language (assembly)", "Third-generation procedural language like C"],
  concept="Language generations",
  explanation="Fourth-generation languages are closer to human language and are largely declarative: the user "
              "states the result required (as in SQL queries and report generators) and the system works out how "
              "to produce it.",
  steps=["Declarative query/report language = 4GL"],
  wrong="1GL is binary machine code and 2GL is assembly with mnemonics. 3GLs such as C and Java are procedural: "
        "the programmer writes the steps.", seconds=20)
Q(T, "System and application software", "Intermediate",
  "Before a new loan-origination system goes live, branch officers who will actually use it run real business "
  "scenarios on it and formally confirm that it meets their requirements. Which testing phase is this?",
  ["User acceptance testing (UAT)", "Unit testing", "Integration testing", "Regression testing"],
  concept="Software testing levels",
  explanation="User acceptance testing is the final phase, in which the business users verify that the system "
              "does what they need in real-world scenarios before it is accepted for production.",
  steps=["End users approve before go-live = UAT"],
  wrong="Unit testing checks individual modules, usually by developers. Integration testing checks that modules "
        "work together. Regression testing re-checks old features after a change.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "In an object-oriented banking program, Account is defined once with fields such as balance and methods such as "
  "deposit(). Then acc1 and acc2 are created from it, each with its own balance. What are Account and acc1?",
  ["Account is a class; acc1 is an object (instance) of that class",
   "Account is an object; acc1 is a class", "Both are methods", "Account is a variable; acc1 is a data type"],
  concept="Classes and objects",
  explanation="A class is a blueprint that defines fields and methods. Objects are instances created from the "
              "class; each object has its own copy of the fields (acc1 and acc2 hold separate balances).",
  steps=["Blueprint = class", "Created instance = object"],
  wrong="The relationship is the other way round: objects are made from classes. Methods are the functions such as "
        "deposit(). Account is not a simple variable.", seconds=20)
o, a = ordered(26, [-26, 8, 30])
Q(T, "Programming languages", "Advanced",
  "A calculator program evaluates expressions in postfix (Reverse Polish) notation using a stack: a number is "
  "pushed; an operator pops the top two numbers, applies the operator (second-popped OPERATOR first-popped) and "
  "pushes the result. What is the value of  6 2 3 + * 4 -  ?", o, a,
  concept="Stack evaluation of postfix expressions",
  explanation="Push 6, 2, 3. '+' pops 3 and 2 and pushes 5. '*' pops 5 and 6 and pushes 30. Push 4. '-' pops 4 and "
              "30 and pushes 30 - 4 = 26. The expression is 6 x (2 + 3) - 4 in ordinary notation.",
  steps=["Stack: 6, 2, 3", "+ -> 6, 5", "* -> 30", "push 4 -> 30, 4", "- -> 26"],
  wrong="30 forgets the final subtraction. -26 takes the operands of '-' in the wrong order (4 - 30). 8 reads "
        "the expression as the infix 6 + 2 x 3 - 4.", seconds=60, computed=True)
o = ["17, 42, 9, 33, 58", "9, 17, 33, 42, 58", "17, 42, 58, 9, 33", "17, 9, 33, 42, 58"]
Q(T, "Programming languages", "Advanced",
  "Bubble sort arranges a list in ascending order by comparing each pair of neighbours from left to right and "
  "swapping them if the left one is larger. After ONE complete pass over the list 42, 17, 58, 9, 33, what is the "
  "list?", o,
  concept="Bubble sort",
  explanation="Compare 42 and 17: swap -> 17, 42, 58, 9, 33. 42 and 58: no swap. 58 and 9: swap -> 17, 42, 9, 58, "
              "33. 58 and 33: swap -> 17, 42, 9, 33, 58. After one pass the largest value, 58, has 'bubbled' to the "
              "end.",
  steps=["(42,17) swap", "(42,58) keep", "(58,9) swap", "(58,33) swap", "-> 17, 42, 9, 33, 58"],
  wrong="9, 17, 33, 42, 58 is the fully sorted list, which needs more passes. 17, 42, 58, 9, 33 stops after the "
        "first swap. 17, 9, 33, 42, 58 is the list after the second pass.", seconds=60, computed=True)

# ================================================================ 4. Operating Systems (2 / 1 / 1)
T = "Operating Systems"
Q(T, "Windows and Linux basics", "Basic",
  "A clerk wants to close the active window of the program she has finished using, from the keyboard. Which "
  "Windows shortcut does this?", ["Alt + F4", "Ctrl + F4 + Shift", "Windows logo key + F4", "Alt + Tab"],
  concept="Windows keyboard shortcuts",
  explanation="Alt + F4 closes the active window; if no window is open, it opens the shut-down dialog.",
  steps=["Close active window = Alt + F4"],
  wrong="Alt + Tab switches between windows. The other two combinations are not the standard close shortcut.",
  seconds=10,
  facts=[fact("Microsoft: Alt+F4 - close the active window; if no windows are open, prompt to shut down.",
              MS_WIN_KEYS)])
Q(T, "Windows and Linux basics", "Basic",
  "On a Linux server, an officer wants to display the contents of the text file branch_list.txt on the screen. "
  "Which command should he use?",
  ["cat branch_list.txt", "cd branch_list.txt", "mkdir branch_list.txt", "pwd branch_list.txt"],
  concept="Basic Linux commands",
  explanation="cat (concatenate) prints the contents of one or more files to the standard output, i.e. the "
              "screen.",
  steps=["Show file contents = cat"],
  wrong="cd changes directory, mkdir creates a directory and pwd prints the current directory; none shows a "
        "file's contents.", seconds=10,
  facts=[fact("man7 cat(1): cat - concatenate files and print on the standard output.", MAN_CAT)])
Q(T, "Functions", "Intermediate",
  "An application program wants to read a file from the disk, but ordinary programs run in user mode and cannot "
  "control the disk directly. How does the program get the file read?",
  ["It makes a system call, which switches the CPU to kernel mode so that the operating system performs the read",
   "It writes directly to the disk controller's registers", "It asks the BIOS to load the file each time",
   "It copies the file into the cache by itself"],
  concept="System calls, user mode and kernel mode",
  explanation="Hardware access is reserved for the kernel. A program requests services such as file reading "
              "through a system call; the CPU switches to kernel mode, the OS checks permissions, performs the I/O "
              "and returns the result to the program in user mode.",
  steps=["User program -> system call (e.g. read)", "CPU enters kernel mode", "OS does the I/O, returns"],
  wrong="User-mode programs are not allowed to touch device registers directly. BIOS/UEFI services are not used "
        "for routine file access by a running OS. Cache is managed by hardware and the OS, not by the program.",
  seconds=25)
o, a = ordered(2480, [1616, 2000, 4096], fmt=lambda v: f"{v:,} bytes")
Q(T, "Functions", "Advanced",
  "An operating system allocates memory in fixed pages of 4 KB (4,096 bytes), and a process needs 18,000 bytes. "
  "It is given the smallest whole number of pages that can hold it. How much allocated memory is wasted as "
  "internal fragmentation?", o, a,
  concept="Internal fragmentation in paging",
  explanation="18,000 / 4,096 = 4.39, so 5 pages are needed: 5 x 4,096 = 20,480 bytes. Unused space in the last "
              "page = 20,480 - 18,000 = 2,480 bytes.",
  steps=["Pages = ceil(18,000 / 4,096) = 5", "Allocated = 20,480 bytes", "Waste = 20,480 - 18,000 = 2,480"],
  wrong="1,616 is the part of the process in the fifth page, not the unused part. 2,000 wrongly takes 4 KB as "
        "4,000 bytes. 4,096 is a whole page.", seconds=50, computed=True)

# ================================================================ 5. Input and Output Devices (1 / 2 / 2)
T = "Input and Output Devices"
Q(T, "Input devices", "Basic",
  "A bank's training centre uses flight-style and driving simulators in which trainees control movement by "
  "tilting a lever mounted on a base in any direction. Which input device is this?",
  ["Joystick", "Light pen", "Scanner", "Plotter"],
  concept="Pointing and control devices",
  explanation="A joystick is a lever that pivots on a base; its direction and angle are sent to the computer. It "
              "is used in games, simulators and to control machines.",
  steps=["Tilting lever on a base = joystick"],
  wrong="A light pen points at a screen. A scanner captures images of documents. A plotter is an output device.",
  seconds=15)
Q(T, "Output devices", "Intermediate",
  "Printers are classified as impact or non-impact. Which of these is an IMPACT printer?",
  ["Daisy-wheel printer", "Laser printer", "Inkjet printer", "Thermal printer"],
  concept="Impact vs non-impact printers",
  explanation="Impact printers form characters by physically striking an inked ribbon against the paper. A "
              "daisy-wheel printer strikes a wheel of raised characters; dot-matrix and line printers are other "
              "impact printers.",
  steps=["Physical strike on ribbon = impact", "Daisy wheel strikes characters"],
  wrong="Laser printers fuse toner, inkjets spray ink, and thermal printers heat special paper; none strikes the "
        "paper, so all are non-impact.", seconds=20)
Q(T, "Output devices", "Intermediate",
  "A training PC plays recorded lectures through speakers. The audio is stored as digital numbers, but speakers "
  "need a continuously varying electrical signal. Which component on the sound card (or audio chip) performs this "
  "conversion?",
  ["Digital-to-analog converter (DAC)", "Analog-to-digital converter (ADC)", "Network interface card",
   "Graphics processing unit"],
  concept="Audio output",
  explanation="A DAC turns the stream of digital samples into a continuous analog voltage that drives the "
              "speakers or headphones. An ADC does the opposite for microphone input.",
  steps=["Digital -> analog for speakers = DAC"],
  wrong="An ADC converts analog to digital (used for recording). The NIC handles networking and the GPU handles "
        "graphics.", seconds=20)
o, a = ordered(0.806, [1.611, 12.891, 275.0], fmt=lambda v: f"{v:g} mV")
Q(T, "Input devices", "Advanced",
  "A temperature sensor in a data-centre rack outputs 0 to 3.3 V, which a 12-bit analog-to-digital converter "
  "(ADC) turns into numbers. Taking the step size as the full range divided by the number of levels (2^12), what "
  "is the smallest voltage change the ADC can distinguish, approximately?", o, a,
  concept="ADC resolution (quantisation step)",
  explanation="A 12-bit ADC has 2^12 = 4,096 levels. Step = 3.3 V / 4,096 = 0.000806 V = 0.806 mV.",
  steps=["Levels = 2^12 = 4,096", "Step = 3.3 / 4,096 V", "= 0.806 mV"],
  wrong="1.611 mV uses 2^11 levels. 12.891 mV is the step of an 8-bit ADC (256 levels). 275 mV divides the range "
        "by 12 (the bit count) instead of 2^12.", seconds=50, computed=True)
Q(T, "Output devices", "Advanced",
  "A display is labelled 1080p while an older broadcast format is 1080i. What does the 'i' mean, compared with "
  "'p'?",
  ["Interlaced: each refresh draws only alternate lines (odd, then even), while progressive draws every line each "
   "time", "Integrated: the screen has built-in speakers", "Inverted: colours are shown in negative",
   "Infrared: the screen uses infrared touch sensing"],
  concept="Interlaced vs progressive scanning",
  explanation="In interlaced video each field contains only half the lines (odd lines, then even lines) and two "
              "fields make a frame. Progressive scan draws all the lines in every frame, giving smoother motion "
              "and sharper text.",
  steps=["i = interlaced (alternate lines per field)", "p = progressive (all lines each frame)"],
  wrong="The other expansions are made up; 'i' and 'p' describe how lines are scanned.", seconds=25)

# ================================================================ 6. Memory (3 / 6 / 3) and the CCTV set
T = "Memory"
S_CCTV = new_stim(
    "data_table", "CCTV recording system of a branch",
    "A branch installs a CCTV system. All figures use decimal units (1 GB = 1,000 MB, 1 TB = 1,000 GB, 1 byte = "
    "8 bits).\n\n| Item | Specification |\n|---|---|\n| Cameras | 8 IP cameras, each streaming continuously at a "
    "constant 4 Mbps (megabits per second) |\n| Recorder | Network video recorder (NVR) that records all streams "
    "24 hours a day |\n| NVR storage | 6 hard disks of 4 TB each, configured as RAID 6 (two disks' worth of "
    "capacity used for parity) |\n| Head-office link | 50 Mbps link used to view the cameras live from the "
    "regional office |\n| Policy | When the disks are full, the oldest recording is overwritten |",
    "Total stream = 8 x 4 = 32 Mbps. Per day: 32 Mbps x 86,400 s = 2,764,800 Mb = 345,600 MB = 345.6 GB. RAID 6 "
    "usable capacity = (6 - 2) x 4 = 16 TB, and the array survives any two simultaneous disk failures. Retention = "
    "16,000 / 345.6 = 46.3, so 46 full days are kept.")
o, a = ordered(64, [16, 32, 80], fmt=lambda v: f"{v}%")
Q("Networking", "Devices", "Intermediate",
  "Refer to the CCTV system. If all eight cameras are viewed live from the regional office at the same time, what "
  "percentage of the 50 Mbps head-office link do the streams use?", o, a,
  concept="Bandwidth utilisation",
  explanation="Total = 8 cameras x 4 Mbps = 32 Mbps. 32 / 50 = 0.64 = 64% of the link.",
  steps=["8 x 4 = 32 Mbps", "32 / 50 = 64%"],
  wrong="32% treats the link as 100 Mbps. 16% uses a link of 200 Mbps or 4 cameras at 2 Mbps. 80% is 40 Mbps, as "
        "if there were 10 cameras.", seconds=30, computed=True, stim=S_CCTV, pos=1)
o, a = ordered(345.6, [14.4, 43.2, 2764.8], fmt=lambda v: f"{v:,} GB")
Q(T, "Cache and units", "Intermediate",
  "Refer to the CCTV system. How much storage do the eight cameras use in one full day of recording?", o, a,
  concept="Data-rate to storage conversion",
  explanation="32 Mbps x 86,400 seconds = 2,764,800 megabits. Divide by 8 for megabytes: 345,600 MB, and by 1,000 "
              "for gigabytes: 345.6 GB.",
  steps=["32 Mb/s x 86,400 s = 2,764,800 Mb", "/ 8 = 345,600 MB", "/ 1,000 = 345.6 GB"],
  shortcut="1 Mbps for a day = 86,400 / 8 = 10.8 GB; 32 x 10.8 = 345.6 GB.",
  wrong="2,764.8 forgets to convert bits to bytes. 43.2 divides by 8 twice. 14.4 GB is one hour's recording.",
  seconds=60, computed=True, stim=S_CCTV, pos=2)
o, a = ordered(16, [12, 20, 24], fmt=lambda v: f"{v} TB")
Q(T, "Secondary storage", "Intermediate",
  "Refer to the CCTV system. Ignoring formatting overhead, how much usable recording space does the RAID 6 array "
  "provide?", o, a,
  concept="RAID 6 capacity",
  explanation="RAID 6 stores two independent parity blocks in every stripe, so two disks' worth of capacity is "
              "used for parity: usable = (6 - 2) x 4 TB = 16 TB.",
  steps=["Disks = 6 x 4 TB", "Parity = 2 disks", "Usable = 4 x 4 = 16 TB"],
  wrong="20 TB would be RAID 5 (one parity disk). 24 TB is the raw total with no protection. 12 TB is half the raw "
        "capacity, as in mirroring.", seconds=30, computed=True, stim=S_CCTV, pos=3)
o, a = ordered(PARITY_DISKS, [0, 1, 3], fmt=lambda v: f"{v}" + (" disk" if v == 1 else " disks"))
Q(T, "Secondary storage", "Intermediate",
  "Refer to the CCTV system. What is the largest number of disks that can fail at the same time without any "
  "recording being lost?", o, a,
  concept="RAID 6 fault tolerance",
  explanation="With dual parity, RAID 6 can rebuild the data after any two disks fail together. A third failure "
              "before the rebuild finishes would lose data.",
  steps=["RAID 6 = double parity", "Tolerates 2 simultaneous failures"],
  wrong="RAID 5 tolerates only 1 failure and RAID 0 tolerates none. 3 failures exceed the two parity blocks.",
  seconds=20, computed=True, stim=S_CCTV, pos=4)
o, a = ordered(DAYS, [57, 69, 370], fmt=lambda v: f"{v} days")
Q(T, "Cache and units", "Advanced",
  "Refer to the CCTV system. When the NVR is full it overwrites the oldest recording. About how many full days of "
  "recording does the system keep?", o, a,
  concept="Storage capacity planning",
  explanation="Usable space = 16 TB = 16,000 GB. Daily use = 345.6 GB. 16,000 / 345.6 = 46.3, so 46 complete days "
              "of recording are retained.",
  steps=["Usable = (6 - 2) x 4 TB = 16,000 GB", "Per day = 32 x 86,400 / 8 / 1,000 = 345.6 GB",
         "16,000 / 345.6 = 46.3 -> 46 days"],
  wrong="57 days uses RAID 5 capacity (20 TB) and 69 days the raw 24 TB. 370 days forgets to convert bits to bytes "
        "correctly (43.2 GB a day).", seconds=90, computed=True, stim=S_CCTV, pos=5)
Q(T, "Cache and units", "Basic",
  "What is the smallest unit of data that a computer can store, having only the value 0 or 1?",
  ["Bit", "Byte", "Nibble", "Word"],
  concept="Units of data",
  explanation="A bit (binary digit) holds a single 0 or 1. A nibble is 4 bits, a byte is 8 bits, and a word is "
              "the processor's natural unit (for example 32 or 64 bits).",
  steps=["Single 0 or 1 = bit"],
  wrong="Nibble (4 bits), byte (8 bits) and word (several bytes) are all made of bits.", seconds=10)
Q(T, "Secondary storage", "Basic",
  "A branch's body-worn camera and digital camera save photos on a small removable flash card about the size of a "
  "postage stamp. What is this storage device usually called?",
  ["SD (memory) card", "Floppy disk", "Magnetic tape", "Blu-ray disc"],
  concept="Removable flash storage",
  explanation="SD (Secure Digital) cards, including microSD, are small removable flash-memory cards used in "
              "cameras, phones and recorders.",
  steps=["Small removable flash card = SD card"],
  wrong="A floppy disk is an old magnetic disk in a plastic case. Magnetic tape is used for bulk backups. Blu-ray "
        "is an optical disc read by a laser.", seconds=10)
Q(T, "Cache and units", "Basic",
  "Where does cache memory sit in a computer, and why is it used?",
  ["Between the CPU and main memory (RAM), to hold frequently used data so the CPU waits less",
   "Between RAM and the hard disk, to make the disk larger", "Inside the monitor, to store screen images",
   "On the network card, to store web pages"],
  concept="Role of cache memory",
  explanation="Cache is a small, very fast memory (SRAM) placed between the CPU and main memory. It keeps copies "
              "of recently and frequently used data and instructions so that most requests do not have to wait "
              "for the slower RAM.",
  steps=["CPU <-> cache <-> RAM", "Purpose: reduce the CPU's waiting time"],
  wrong="Cache does not add capacity to the disk. Screen images are held in video memory. A browser keeps its "
        "cache on disk, which is a different meaning of the word.", seconds=15)
Q(T, "Secondary storage", "Intermediate",
  "An SSD controller cannot overwrite a used flash page in place. Before new data can be written there, what must "
  "happen?",
  ["The whole erase block containing that page must be erased first, because flash is written in pages but erased "
   "only in larger blocks", "The disk must spin up to full speed",
   "The page must be magnetised in the opposite direction", "The data must first be copied to the CPU cache"],
  concept="NAND flash write and erase granularity",
  explanation="NAND flash is programmed (written) a page at a time but erased only in much larger blocks of many "
              "pages. A used page must be erased before it can be programmed again, so controllers move valid data "
              "and erase whole blocks in the background (garbage collection).",
  steps=["Write unit = page", "Erase unit = block (many pages)", "Erase before rewrite"],
  wrong="Flash has no spinning disk or magnetic recording. The CPU cache plays no part in the SSD's internal "
        "writes.", seconds=25)
Q(T, "Primary memory", "Intermediate",
  "The program in a cheap calculator chip is built into the chip's circuit pattern at the factory and can never be "
  "changed by the user or erased. Which kind of ROM is this?",
  ["Mask ROM", "PROM", "EPROM", "EEPROM"],
  concept="Types of ROM",
  explanation="In mask ROM the data is fixed by the photomask used during manufacturing. It is cheapest in very "
              "large quantities but cannot be changed afterwards.",
  steps=["Programmed during manufacture, unchangeable = mask ROM"],
  wrong="PROM is programmed once by the user after manufacture. EPROM is erased with UV light. EEPROM is erased "
        "electrically.", seconds=20)
Q(T, "Primary memory", "Intermediate",
  "A technician is buying extra RAM for a branch LAPTOP. Laptops use a shorter memory module than the DIMMs of "
  "desktop PCs. What is this smaller module called?",
  ["SO-DIMM (Small Outline DIMM)", "SIMM", "M.2 SSD", "CMOS module"],
  concept="Memory module form factors",
  explanation="SO-DIMMs are roughly half the length of desktop DIMMs and are used in laptops, mini PCs and some "
              "printers and routers.",
  steps=["Laptop RAM module = SO-DIMM"],
  wrong="SIMMs are an obsolete older module type. An M.2 SSD is storage, not RAM. CMOS stores firmware settings.",
  seconds=15)
o, a = ordered(7.8125, [0.128, 64.0, 128.0], fmt=lambda v: f"{v:g} microseconds")
Q(T, "Primary memory", "Advanced",
  "A DRAM chip has 8,192 rows, and every row must be refreshed once every 64 ms. If the memory controller spreads "
  "the refreshes evenly, refreshing one row at a time, how often must it issue a refresh?", o, a,
  concept="DRAM refresh",
  explanation="64 ms must cover 8,192 row refreshes: 64 ms / 8,192 = 0.0078125 ms = 7.8125 microseconds between "
              "refresh commands.",
  steps=["64 ms = 64,000 microseconds", "64,000 / 8,192 = 7.8125 microseconds"],
  wrong="128 divides 8,192 by 64 (rows per millisecond, not a time). 0.128 is the reciprocal mistake. 64 "
        "microseconds misreads milliseconds as microseconds.", seconds=50, computed=True)
o, a = ordered(2.5, [0.4, 1.5, 3.5])
Q(T, "Secondary storage", "Advanced",
  "Over a month, a server's operating system writes 100 GB of data to its SSD, but the SSD's controller reports "
  "that 250 GB were actually written to the NAND flash (because of garbage collection and moving valid data). What "
  "is the write amplification factor?", o, a,
  concept="SSD write amplification",
  explanation="Write amplification factor = data written to flash / data written by the host = 250 / 100 = 2.5. "
              "Higher values wear the flash out faster; TRIM and over-provisioning help reduce it.",
  steps=["WAF = NAND writes / host writes", "= 250 / 100 = 2.5"],
  wrong="0.4 inverts the ratio. 1.5 is the extra 150 GB divided by 100. 3.5 adds the two figures.", seconds=40,
  computed=True)

# ================================================================ 7. Networking (2 / 4 / 4) + Internet set
S_FW = new_stim(
    "data_table", "Firewall rules of a branch",
    "A branch firewall checks each new connection against these rules from top to bottom and applies the FIRST rule "
    "that matches (protocol, source, destination and destination port must all match). A connection that matches "
    "no rule is dropped. The firewall is stateful.\n\n| Rule | Action | Protocol | Source | Destination | "
    "Destination port |\n|---|---|---|---|---|---|\n| 1 | Allow | TCP | 10.20.30.0/24 | any | 443 |\n| 2 | Deny | "
    "TCP | any | any | 3389 |\n| 3 | Allow | TCP | 10.20.30.10 | 10.20.0.0/16 | 3389 |\n| 4 | Allow | TCP | "
    "10.20.30.0/24 | 10.20.0.25 | 993 |\n| 5 | Allow | UDP | 10.20.30.0/24 | 10.20.0.53 | 53 |\n\nThe branch LAN "
    "is 10.20.30.0/24; head-office servers are in 10.20.0.0/16.",
    "Rules are matched in order, so rule 2 blocks all RDP (port 3389) before rule 3 is ever reached; rule 3 must be "
    "moved above rule 2. Traffic matching no rule meets the implicit deny. A stateful firewall remembers allowed "
    "connections and lets their reply packets back in automatically. Port 993 is IMAP over TLS.")
Q("Networking", "Devices", "Intermediate",
  "Refer to the firewall rules. A clerk's PC, 10.20.30.44, sends a DNS query over UDP to 10.20.0.53 on port 53. "
  "What happens?",
  ["Rule 5 matches and the query is allowed", "Rule 1 matches and the query is allowed",
   "Rule 2 matches and the query is denied", "No rule matches, so the query is dropped"],
  concept="First-match firewall rules",
  explanation="Rules 1 to 4 are for TCP, so a UDP packet cannot match them. Rule 5 is UDP from 10.20.30.0/24 to "
              "10.20.0.53 port 53: the source 10.20.30.44 is inside the /24, so rule 5 matches and allows it.",
  steps=["Protocol UDP -> rules 1-4 do not apply", "Rule 5: source in 10.20.30.0/24, dst 10.20.0.53, port 53",
         "Allowed by rule 5"],
  wrong="Rule 1 covers TCP port 443 only. Rule 2 covers TCP port 3389. A rule does match, so the default drop "
        "does not apply.", seconds=40, computed=True, stim=S_FW, pos=1)
Q("Networking", "Devices", "Advanced",
  "Refer to the firewall rules. The administrator's PC, 10.20.30.10, tries to open a Remote Desktop (RDP, TCP "
  "3389) session to the server 10.20.0.70, but the connection is blocked even though rule 3 allows it. What is the "
  "fix?",
  ["Move rule 3 above rule 2, because rule 2 matches first and denies the connection",
   "Change rule 3's action from Allow to Deny", "Delete rule 5", "Change the RDP port in rule 3 to 443"],
  concept="Rule order in firewalls",
  explanation="The firewall applies the first matching rule. The RDP packet matches rule 2 (any source, any "
              "destination, TCP 3389), which denies it, so rule 3 is never checked. Placing the specific allow rule "
              "(rule 3) before the general deny (rule 2) lets only the administrator's RDP through.",
  steps=["Packet: TCP 10.20.30.10 -> 10.20.0.70:3389", "Rule 1 no (port 443)", "Rule 2 yes -> Deny",
         "Specific allow must come before general deny"],
  wrong="Making rule 3 a Deny blocks the administrator permanently. Rule 5 is for DNS and is irrelevant. RDP "
        "listens on 3389, not 443.", seconds=50, computed=True, stim=S_FW, pos=2,
  facts=[fact("Microsoft Learn: Remote Desktop uses RDP and listens on port 3389 by default.", MS_RDP)])
Q("Networking", "Devices", "Intermediate",
  "Refer to the firewall rules. A guest laptop on the separate guest network 10.20.31.5 tries to open the HTTPS "
  "site 203.0.113.80 on TCP port 443. What happens?",
  ["It is dropped, because no rule matches and the firewall's default is to deny",
   "It is allowed by rule 1, because the port is 443", "It is denied by rule 2",
   "It is allowed, because HTTPS is always permitted"],
  concept="Implicit deny",
  explanation="Rule 1 allows port 443 only from 10.20.30.0/24 (10.20.30.0 to 10.20.30.255); 10.20.31.5 is outside "
              "it. No other rule matches TCP 443, so the connection reaches the end of the list and is dropped by "
              "the default (implicit) deny.",
  steps=["10.20.31.5 not in 10.20.30.0/24", "Rules 2-5: wrong port or protocol", "No match -> default deny"],
  wrong="Rule 1 requires the source to be in the branch LAN. Rule 2 is about port 3389. No firewall permits a "
        "port automatically; only the rules decide.", seconds=40, computed=True, stim=S_FW, pos=3)
Q("Networking", "Devices", "Advanced",
  "Refer to the firewall rules. A clerk's PC opens a connection to a website on port 443 (allowed by rule 1). There "
  "is no rule allowing traffic FROM the website back to the PC, yet the web pages arrive. Why?",
  ["The stateful firewall records the allowed outgoing connection and automatically lets its reply packets back in",
   "Replies to port 443 are never checked by any firewall", "Rule 5 allows all replies",
   "The router converts the replies into DNS traffic"],
  concept="Stateful inspection",
  explanation="A stateful firewall keeps a table of active connections. Packets that belong to a connection it has "
              "already allowed (the replies) are passed without needing their own rule, while unsolicited incoming "
              "packets are still dropped.",
  steps=["Outgoing connection allowed -> entry in state table", "Matching replies allowed automatically"],
  wrong="A stateless packet filter would need an explicit return rule; it is the state table, not the port, that "
        "lets replies in. Rule 5 covers only DNS queries to 10.20.0.53. Routers do not turn web traffic into DNS.",
  seconds=35, stim=S_FW, pos=4)
Q("Internet", "Email", "Intermediate",
  "Refer to the firewall rules. Rule 4 allows branch PCs to reach the head-office mail server 10.20.0.25 on TCP "
  "port 993. What do the PCs' email programs use this port for?",
  ["Reading mailboxes with IMAP over TLS (IMAPS)", "Sending mail with SMTP message submission",
   "Downloading mail with POP3 over TLS", "Opening the bank's website over HTTPS"],
  concept="Well-known email ports",
  explanation="Port 993 is the default port of IMAP over implicit TLS ('imaps'), used to read and manage "
              "mailboxes on the server over an encrypted connection.",
  steps=["993 = IMAPS"],
  wrong="Message submission uses 587 (or 465 with implicit TLS). POP3 over TLS uses 995. HTTPS uses 443.",
  seconds=20, stim=S_FW, pos=5,
  facts=[fact("RFC 8314: imaps default port 993; pop3s default port 995; submissions default port 465.", RFC8314)])
T = "Networking"
Q(T, "Topologies", "Basic",
  "Which is the largest example of a WAN (Wide Area Network), linking networks across countries and continents?",
  ["The Internet", "A branch LAN", "A Bluetooth PAN", "A home Wi-Fi network"],
  concept="Types of networks by area",
  explanation="A WAN covers a large geographical area. The Internet, a worldwide network of networks, is the "
              "largest WAN.",
  steps=["Worldwide network of networks = Internet = largest WAN"],
  wrong="A LAN covers a building or branch, a PAN a few metres around a person, and home Wi-Fi a single house.",
  seconds=10)
Q(T, "Devices", "Basic",
  "A cable-broadband connection reaches a branch through a round cable with a central copper conductor, an "
  "insulating layer, a braided metal shield and an outer jacket. Which cable is this?",
  ["Coaxial cable", "Twisted-pair cable", "Optical fibre cable", "Ribbon cable"],
  concept="Network cables",
  explanation="Coaxial cable has one central conductor surrounded by insulation and a metal shield on the same "
              "axis. It is used for cable TV and cable broadband.",
  steps=["Central conductor + shield on the same axis = coaxial"],
  wrong="Twisted pair has pairs of wires twisted together. Fibre carries light in glass strands. Ribbon cable is "
        "flat, used inside computers.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "A new branch PC joins the network and gets its IP address automatically from a DHCP server. In what order are "
  "the four DHCP messages exchanged?",
  ["Discover, Offer, Request, Acknowledge", "Request, Offer, Discover, Acknowledge",
   "Offer, Discover, Acknowledge, Request", "Discover, Request, Offer, Acknowledge"],
  concept="DHCP address allocation (DORA)",
  explanation="The client broadcasts DHCPDISCOVER; servers reply with DHCPOFFER; the client broadcasts "
              "DHCPREQUEST for the chosen offer; the chosen server confirms with DHCPACK.",
  steps=["D - Discover", "O - Offer", "R - Request", "A - Acknowledge"],
  shortcut="Remember DORA.",
  wrong="The client must discover servers before any offer, and it requests only after receiving an offer.",
  seconds=20,
  facts=[fact("RFC 2131 section 3.1: the client broadcasts DHCPDISCOVER, servers respond with DHCPOFFER, the client "
              "broadcasts DHCPREQUEST, and the server responds with DHCPACK.", RFC2131)])
Q(T, "OSI and TCP/IP", "Advanced",
  "A small bank network uses RIP, a distance-vector routing protocol that counts hops. A network that is 16 hops "
  "away is treated as unreachable. What is the largest network diameter RIP supports?",
  ["15 hops", "16 hops", "255 hops", "No limit"],
  concept="RIP hop-count limit",
  explanation="RIP uses hop count as its metric and treats a metric of 16 as infinity (unreachable), so it is "
              "limited to networks whose longest path is 15 hops. The small limit helps end counting-to-infinity "
              "loops quickly.",
  steps=["Metric 16 = infinity", "Max usable path = 15 hops"],
  wrong="16 is the 'unreachable' value, not a usable distance. 255 is the maximum IPv4 TTL, not RIP's limit. RIP "
        "is deliberately limited.", seconds=20,
  facts=[fact("RFC 2453: the protocol is limited to networks whose longest path is 15 hops; the value 16 "
              "(infinity) indicates the destination is not reachable.", RFC2453)])
Q(T, "OSI and TCP/IP", "Advanced",
  "Every IPv6-enabled branch PC automatically has an address beginning with fe80:: on each interface, usable only "
  "to talk to devices on the same link (for example, the local router). What type of address is it?",
  ["Link-local unicast address (fe80::/10), which routers never forward to other links",
   "Global unicast address, routable on the internet", "Multicast address for all routers",
   "Loopback address of the PC itself"],
  concept="IPv6 address types",
  explanation="fe80::/10 is the IPv6 link-local prefix. Every interface configures such an address automatically; "
              "it is used for neighbour discovery and routing protocols on the local link, and routers must not "
              "forward packets with link-local source or destination to other links.",
  steps=["fe80::/10 = link-local", "Valid only on the local link"],
  wrong="Global unicast addresses (typically from 2000::/3) are internet-routable. IPv6 multicast addresses begin "
        "with ff. The loopback address is ::1.", seconds=25,
  facts=[fact("RFC 4291: Link-Local unicast prefix is FE80::/10; routers must not forward any packets with "
              "link-local source or destination addresses to other links.", RFC4291)])

# ================================================================ 8. Internet (1 / 2 / 2)
T = "Internet"
Q(T, "Email", "Basic",
  "In the email address loans.pune@bank.example, which symbol separates the mailbox (user) name from the domain "
  "name?", ["@", "#", "/", "&"],
  concept="Structure of an email address",
  explanation="An email address has the form local-part@domain: 'loans.pune' is the mailbox and 'bank.example' is "
              "the domain whose mail server receives the message.",
  steps=["user @ domain"],
  wrong="#, / and & are not used to separate the parts of an email address.", seconds=10)
Q(T, "Web basics", "Intermediate",
  "A circular's link is https://bank.example/rules.html#section4. When the browser requests the page, which part "
  "of the address is NOT sent to the web server?",
  ["#section4 (the fragment), which the browser uses to jump to that part of the page",
   "https:// (the scheme)", "bank.example (the host)", "/rules.html (the path)"],
  concept="URL fragment",
  explanation="The fragment starts with # and identifies a part of the resource. The browser requests "
              "/rules.html from bank.example over HTTPS, then scrolls to the element 'section4' itself; the "
              "fragment never goes to the server.",
  steps=["Request = scheme + host + path (+ query)", "Fragment (#...) handled only by the browser"],
  wrong="The scheme decides the protocol used, the host is where the request goes, and the path is the resource "
        "requested; all are used to make the request.", seconds=25,
  facts=[fact("MDN: the fragment is the last part of the URI, starting with #; it is not sent to the server when the "
              "URI is requested and is processed by the client.", MDN_FRAG)])
Q(T, "Protocols", "Advanced",
  "A fintech app calls a bank's balance API 500 times in one minute. The API starts answering with HTTP status "
  "429. What does this mean, and what should the app do?",
  ["Too Many Requests: the client is being rate-limited and should slow down and retry later",
   "Unauthorized: the API key is wrong", "Not Found: the API address has changed",
   "Internal Server Error: the bank's server has crashed"],
  concept="HTTP status 429",
  explanation="429 Too Many Requests (RFC 6585) says the user has sent too many requests in a given time (rate "
              "limiting). The server may send a Retry-After header; the client should back off and retry later.",
  steps=["429 = rate limited", "Reduce request rate; respect Retry-After"],
  wrong="Wrong credentials give 401, a missing resource 404, and a server fault 500. None of these is about the "
        "request rate.", seconds=20,
  facts=[fact("RFC 6585 section 4: the 429 status code indicates that the user has sent too many requests in a "
              "given amount of time ('rate limiting').", RFC6585)])
Q(T, "Web basics", "Advanced",
  "A net-banking site sends the response header  Content-Security-Policy: script-src 'self'  with every page. "
  "What protection does this give?",
  ["The browser runs only scripts loaded from the site's own origin, which blocks most injected (XSS) scripts",
   "It forces the browser to use HTTPS for all future visits", "It encrypts the cookies stored in the browser",
   "It stops other websites from showing the bank's pages in a frame"],
  concept="Content Security Policy",
  explanation="CSP tells the browser which sources of content are allowed. script-src 'self' permits JavaScript "
              "only from the page's own origin, so inline or third-party scripts injected by an attacker are not "
              "executed. Its main use is to reduce cross-site scripting (XSS).",
  steps=["CSP = allow-list of content sources", "script-src 'self' -> only same-origin scripts run"],
  wrong="Forcing HTTPS is HSTS. Cookies are not encrypted by CSP. Framing control is done by the frame-ancestors "
        "directive or X-Frame-Options, not by script-src.", seconds=30,
  facts=[fact("MDN: CSP controls which resources, especially JavaScript, a document may load; it is mainly a "
              "defence against XSS and is delivered in the Content-Security-Policy response header.", MDN_CSP)])

# ================================================================ 9. Cybersecurity (5 / 5 / 1)
T = "Cybersecurity"
S_CYB = new_stim(
    "passage", "Complaints received at a bank's cyber cell",
    "The cyber cell of a bank logged these four complaints in one week:\n\n"
    "1. **Customer Mr. P** got a call from someone claiming to be from the bank's 'KYC team', who asked him to "
    "install a 'support app' from the app store and read out a code shown in it. Moments later, the caller could "
    "see Mr. P's phone screen, watched him open his banking app, and money was transferred out.\n"
    "2. **The bank's accounts team** received an email that looked like it came from a regular stationery supplier, "
    "from the domain supp1ier-mart.example instead of supplier-mart.example. It said the supplier's bank account "
    "had changed and asked that the pending invoice be paid to the new account. The team paid Rs 4.8 lakh.\n"
    "3. **A branch manager** received a phone call in a voice that sounded exactly like the regional head's, urgently "
    "asking her to release a large payment before an audit. The regional head later confirmed he never called; the "
    "voice had been generated by software trained on his speeches posted online.\n"
    "4. **Several customers** of an online store found their card details misused. The store's site was genuine and "
    "used HTTPS, but investigators found that attackers had inserted a small JavaScript file into the checkout page "
    "that copied card details as they were typed and sent them to the attackers' server.",
    "1: remote-access (screen-sharing) app fraud. 2: business email compromise using a look-alike domain. 3: "
    "deepfake voice cloning (AI-generated vishing). 4: formjacking / digital (web) skimming of a checkout page.")
Q(T, "Phishing and social engineering", "Basic",
  "Refer to the cyber-cell complaints. In complaint 1, how did the fraudster get control of Mr. P's banking session, "
  "and what is the right advice?",
  ["The 'support app' was a remote-access (screen-sharing) app; never install such apps or share their codes at a "
   "caller's request", "The phone's SIM was swapped; change the SIM card",
   "The bank's server was hacked; nothing could have prevented it", "A virus came through the phone's charger"],
  concept="Remote-access app fraud",
  explanation="Screen-sharing or remote-access apps let another person see, and sometimes control, the phone. By "
              "getting the access code, the fraudster watched the screen (including OTPs and PINs) while the "
              "customer used the banking app. Banks never ask customers to install such apps.",
  steps=["Caller asks to install app + share code", "Screen visible to fraudster", "Remote-access app fraud"],
  wrong="The SIM was not changed; Mr. P kept his signal. The bank's systems were used normally with Mr. P's own "
        "credentials. Nothing points to a charging-port attack.", seconds=25, stim=S_CYB, pos=1)
Q(T, "Phishing and social engineering", "Intermediate",
  "Refer to the cyber-cell complaints. Which attack does complaint 2 describe, and which control would most "
  "likely have stopped the loss?",
  ["Business email compromise (BEC); confirming any change of a supplier's bank details by calling the supplier on "
   "a number already on record", "Ransomware; keeping offline backups", "Pharming; flushing the DNS cache",
   "Cryptojacking; monitoring CPU usage"],
  concept="Business email compromise",
  explanation="BEC impersonates a trusted business contact (here, through a look-alike domain) to divert payments, "
              "often by announcing 'new bank details'. Independent verification through a known phone number "
              "before changing payee details defeats it.",
  steps=["Look-alike supplier domain + 'new bank account' = BEC", "Verify out-of-band before paying"],
  wrong="No files were encrypted (ransomware), no DNS was tampered with (pharming), and no computing power was "
        "stolen (cryptojacking).", seconds=30, stim=S_CYB, pos=2)
Q(T, "Phishing and social engineering", "Intermediate",
  "Refer to the cyber-cell complaints. What made the call in complaint 3 convincing?",
  ["An AI-generated deepfake (cloned) voice of the regional head, built from his recordings",
   "A keylogger on the manager's PC", "A forged SSL certificate", "A logic bomb in the payment system"],
  concept="Deepfake voice cloning",
  explanation="Deepfake audio uses machine learning trained on samples of a person's voice to produce new speech "
              "in that voice. Combined with urgency and authority, it is a powerful form of vishing; a call-back on "
              "a known number or a code word defeats it.",
  steps=["Synthetic voice imitating a real person = deepfake voice cloning"],
  wrong="A keylogger records keystrokes. A forged certificate concerns websites. A logic bomb is hidden code "
        "triggered by a condition. None imitates a voice.", seconds=20, stim=S_CYB, pos=3)
Q(T, "Malware", "Advanced",
  "Refer to the cyber-cell complaints. Complaint 4 describes card data being stolen from a genuine HTTPS checkout "
  "page by an injected script. What is this attack called, and why did HTTPS not prevent it?",
  ["Formjacking (digital / web skimming); the malicious script runs inside the genuine page in the customer's "
   "browser, so it reads the data before it is encrypted for sending", "Card skimming at an ATM; HTTPS does not "
   "cover ATMs", "Man-in-the-middle attack; HTTPS was switched off", "SQL injection; HTTPS does not protect "
   "databases"],
  concept="Formjacking (Magecart-style web skimming)",
  explanation="In formjacking, attackers add JavaScript to a legitimate site's payment form (often through a "
              "compromised third-party script). The script runs in the shopper's browser with the page's own "
              "privileges and copies the card details as they are typed, then sends them out. HTTPS protects data "
              "in transit, not data that a script on the page itself reads. Content Security Policy, script "
              "integrity checks and monitoring of page changes are defences.",
  steps=["Injected JS on checkout page", "Reads form fields in the browser", "HTTPS encrypts only the transfer"],
  wrong="ATM skimming uses a physical device on the card slot. A man-in-the-middle attack intercepts traffic, but "
        "here the connection was genuine HTTPS. SQL injection attacks the database through input, not a script "
        "in the page.", seconds=40, stim=S_CYB, pos=4)
Q(T, "Malware", "Basic",
  "An antivirus program finds a suspicious file and, instead of deleting it, moves it to a protected isolated area "
  "where it cannot run but can be restored if it turns out to be safe. What is this action called?",
  ["Quarantine", "Formatting", "Defragmentation", "Compression"],
  concept="Antivirus actions",
  explanation="Quarantine isolates a suspected file in a secure location so it cannot execute or spread, while "
              "keeping it in case it is a false alarm.",
  steps=["Isolate, do not delete = quarantine"],
  wrong="Formatting erases a whole drive. Defragmentation rearranges file pieces. Compression reduces size.",
  seconds=10)
Q(T, "Phishing and social engineering", "Basic",
  "A bank hires security professionals, with written permission, to try to break into its systems and report the "
  "weaknesses so that they can be fixed. These authorised testers are known as:",
  ["Ethical (white-hat) hackers", "Black-hat hackers", "Script kiddies", "Hacktivists"],
  concept="Types of hackers",
  explanation="White-hat or ethical hackers test systems with the owner's permission (for example in penetration "
              "tests) to find and fix weaknesses before criminals exploit them.",
  steps=["Authorised, to improve security = white hat"],
  wrong="Black-hat hackers break in illegally for gain. Script kiddies use others' tools without skill. "
        "Hacktivists attack for political or social causes.", seconds=15)
Q(T, "Phishing and social engineering", "Basic",
  "A customer's phone shows the bank's genuine helpline number on an incoming call, but the caller is a fraudster. "
  "The fraudster has falsified the number displayed to the receiver. What is this technique called?",
  ["Caller ID spoofing", "Shoulder surfing", "Tailgating", "Juice jacking"],
  concept="Spoofing",
  explanation="Caller ID spoofing makes a call appear to come from a trusted number. Customers should not trust "
              "the displayed number alone and should call back on the official number themselves.",
  steps=["Fake number displayed = caller ID spoofing"],
  wrong="Shoulder surfing is watching someone type. Tailgating is following someone through a secure door. Juice "
        "jacking is an attack through public USB charging ports.", seconds=15)
Q(T, "Encryption and authentication", "Basic",
  "A loan officer must use long, different passwords for twelve bank systems. Which tool safely stores them in an "
  "encrypted vault, unlocked by one master password, and can generate strong new ones?",
  ["Password manager", "Spreadsheet saved on the desktop", "Sticky notes under the keyboard", "Browser history"],
  concept="Password managers",
  explanation="A password manager keeps credentials in an encrypted vault, fills them in on the right sites, and "
              "generates strong unique passwords, so users do not reuse or write down passwords.",
  steps=["Encrypted vault + generator = password manager"],
  wrong="A plain spreadsheet or sticky notes expose the passwords to anyone who sees them. Browser history records "
        "visited pages, not passwords.", seconds=15)
Q(T, "Encryption and authentication", "Intermediate",
  "A customer approves a large RTGS transfer with a digital signature made with her private key. Later she claims "
  "she never sent the instruction. The signature lets the bank prove that only her key could have signed it. Which "
  "security property is this?",
  ["Non-repudiation", "Availability", "Anonymity", "Compression"],
  concept="Non-repudiation",
  explanation="Non-repudiation means the sender cannot credibly deny having sent a message. Because a digital "
              "signature can be created only with the signer's private key, a valid signature is evidence that she "
              "authorised the instruction.",
  steps=["Cannot deny sending = non-repudiation", "Provided by digital signatures"],
  wrong="Availability is about systems being usable when needed. Anonymity is the opposite of proving identity. "
        "Compression reduces size and has nothing to do with proof.", seconds=20)
Q(T, "Encryption and authentication", "Intermediate",
  "An insider hides confidential customer data inside the pixels of an ordinary-looking holiday photo and emails "
  "it out. The picture looks normal, and nobody suspects that it carries hidden data. What is this technique?",
  ["Steganography", "Hashing", "Tokenisation", "Phishing"],
  concept="Steganography",
  explanation="Steganography hides the existence of a message by embedding it in another file (image, audio, "
              "video), for example in the least significant bits of pixels. Encryption hides the content; "
              "steganography hides the fact that there is a message at all.",
  steps=["Data hidden inside a normal-looking image = steganography"],
  wrong="Hashing makes a fixed-length digest. Tokenisation replaces card numbers with tokens. Phishing is a "
        "deceptive message aimed at victims.", seconds=20)
Q(T, "Malware", "Intermediate",
  "A bank's security team sets up a fake server that looks like a poorly protected payments database but holds no "
  "real data. Any connection to it is suspicious, and the team studies the attackers' methods. What is this decoy "
  "called?",
  ["Honeypot", "Firewall", "Proxy server", "Load balancer"],
  concept="Honeypots",
  explanation="A honeypot is a deliberately exposed decoy system used to attract attackers, detect intrusions and "
              "learn their tools and techniques, without risking real data.",
  steps=["Decoy system to lure and study attackers = honeypot"],
  wrong="A firewall filters traffic. A proxy forwards requests for clients. A load balancer spreads traffic over "
        "real servers.", seconds=15)

# ================================================================ 10. Database Fundamentals (1 / 3 / 2)
T = "Database Fundamentals"
S_SQL = new_stim(
    "data_table", "Staff and Branches tables",
    "Table **Staff** (manager_id refers to the emp_id of the employee's manager; NULL means no manager):\n\n"
    "| emp_id | name | branch | salary | manager_id |\n|---|---|---|---|---|\n| E1 | Asha | Pune | 90000 | NULL |\n"
    "| E2 | Ravi | Pune | 60000 | E1 |\n| E3 | Meena | Delhi | 75000 | E1 |\n| E4 | John | Delhi | 75000 | E3 |\n"
    "| E5 | Farah | Pune | 62000 | E2 |\n| E6 | Kiran | Delhi | 48000 | E3 |\n| E7 | Neha | Agra | 52000 | E1 |\n"
    "| E8 | Tara | Agra | 40000 | E7 |\n\nTable **Branches**:\n\n| branch | city_code |\n|---|---|\n| Pune | PN |\n"
    "| Delhi | DL |\n| Agra | AG |",
    "Branch averages: Pune 70,666.67, Delhi 66,000, Agra 46,000; overall average 62,750. Farah (62,000) earns more "
    "than her manager Ravi (60,000); John equals his manager Meena. Salaries in descending order: 90,000; 75,000 "
    "(two); 62,000; 60,000; 52,000; 48,000; 40,000.")
Q(T, "SQL basics", "Intermediate",
  "Refer to the Staff table. Which names does this query return?\n\nSELECT e.name FROM Staff e JOIN Staff m ON "
  "e.manager_id = m.emp_id WHERE e.salary > m.salary;",
  ["Farah only", "Farah and John", "John only", "No rows"],
  concept="Self-join",
  explanation="The table is joined to itself: e is the employee and m is that employee's manager. Comparing each "
              "salary with the manager's: Ravi 60,000 < Asha 90,000; Meena 75,000 < 90,000; John 75,000 = Meena "
              "75,000 (not greater); Farah 62,000 > Ravi 60,000; Kiran < Meena; Neha < Asha; Tara < Neha. Asha has "
              "no manager, so she has no join row. Only Farah qualifies.",
  steps=["Pair each employee with manager", "Keep e.salary > m.salary", "Only Farah (62,000 > 60,000)"],
  wrong="John's salary equals his manager's, so the strict > excludes him. 'No rows' ignores Farah.",
  seconds=60, computed=True, stim=S_SQL, pos=1)
o, a = ordered(4, [1, 3, 5])
Q(T, "SQL basics", "Intermediate",
  "Refer to the Staff table. How many rows does this query count?\n\nSELECT COUNT(*) FROM Staff WHERE "
  "COALESCE(manager_id, 'E1') = 'E1';", o, a,
  concept="COALESCE and NULL",
  explanation="COALESCE returns its first non-NULL argument, so Asha's NULL manager_id becomes 'E1' for this test. "
              "Rows with 'E1': Asha (from NULL), Ravi, Meena and Neha = 4.",
  steps=["COALESCE(NULL, 'E1') = 'E1' -> Asha counts", "manager_id = 'E1': Ravi, Meena, Neha", "Total 4"],
  wrong="3 is what manager_id = 'E1' alone gives, because NULL = 'E1' is not true. 1 counts only the NULL row. 5 "
        "adds a row that does not match.", seconds=45, computed=True, stim=S_SQL, pos=2)
o, a = ordered(24, [3, 8, 11])
Q(T, "SQL basics", "Intermediate",
  "Refer to the tables. An analyst forgets the join condition and runs:\n\nSELECT COUNT(*) FROM Staff, Branches;\n\n"
  "What number is returned?", o, a,
  concept="Cartesian product (cross join)",
  explanation="Without a join condition, every row of Staff is paired with every row of Branches: 8 x 3 = 24 "
              "rows.",
  steps=["Staff rows = 8", "Branches rows = 3", "8 x 3 = 24"],
  wrong="11 adds the row counts. 8 and 3 are the sizes of the individual tables.", seconds=30, computed=True,
  stim=S_SQL, pos=3)
o = ["Asha, Meena, John and Neha", "Asha, Meena and John", "Asha only", "Meena, John and Neha"]
Q(T, "SQL basics", "Advanced",
  "Refer to the Staff table. Which names does this correlated subquery return?\n\nSELECT name FROM Staff s WHERE "
  "salary > (SELECT AVG(salary) FROM Staff WHERE branch = s.branch);", o,
  concept="Correlated subqueries",
  explanation="The inner query is re-evaluated for each outer row, using that row's branch. Pune average = "
              "(90,000 + 60,000 + 62,000) / 3 = 70,666.67 -> Asha. Delhi average = (75,000 + 75,000 + 48,000) / 3 "
              "= 66,000 -> Meena and John. Agra average = (52,000 + 40,000) / 2 = 46,000 -> Neha.",
  steps=["Pune avg 70,666.67: Asha", "Delhi avg 66,000: Meena, John", "Agra avg 46,000: Neha"],
  wrong="Asha, Meena and John is the result of comparing with the overall average (62,750), which ignores the "
        "branch condition. The other options miss someone in Pune or Agra.", seconds=90, computed=True,
  stim=S_SQL, pos=4)
o, a = ordered(3, [2, 4, 5])
Q(T, "SQL basics", "Advanced",
  "Refer to the Staff table. What value does this query show for Farah?\n\nSELECT name, DENSE_RANK() OVER (ORDER "
  "BY salary DESC) AS rnk FROM Staff;", o, a,
  concept="RANK vs DENSE_RANK",
  explanation="Order: Asha 90,000 (1); Meena and John 75,000 tie (both 2); Farah 62,000. DENSE_RANK leaves no "
              "gap after a tie, so Farah gets 3. (RANK would skip to 4.)",
  steps=["90,000 -> 1", "75,000, 75,000 -> 2, 2", "62,000 -> 3 with DENSE_RANK"],
  wrong="4 is what RANK gives, skipping a number after the tie. 2 is the tied rank above her. 5 counts her row "
        "position wrongly.", seconds=45, computed=True, stim=S_SQL, pos=5)
Q(T, "DBMS concepts", "Basic",
  "In an old file system, a customer's address is stored separately in the savings, loan and locker files, so the "
  "same data appears three times and may not match after one copy is changed. What is the repeated storage of the "
  "same data called?",
  ["Data redundancy", "Data independence", "Data encryption", "Data compression"],
  concept="Redundancy and inconsistency",
  explanation="Data redundancy is the unnecessary duplication of the same data in several places. It wastes space "
              "and leads to inconsistency when only some copies are updated; a DBMS reduces it by storing each "
              "fact once.",
  steps=["Same data stored repeatedly = redundancy"],
  wrong="Data independence means programs are unaffected by changes in how data is stored. Encryption protects "
        "data. Compression reduces its size.", seconds=15)

# ================================================================ 11. MS Office (3 / 3 / 4)
T = "MS Office"
S_XL = new_stim(
    "data_table", "Excel ATM cash-loading register",
    "A branch keeps this register in Excel (dates are real Excel dates; amounts are in rupees):\n\n"
    "| | A (IFSC) | B (ATM ID) | C (Load date) | D (Loaded) | E (Dispensed) |\n|---|---|---|---|---|---|\n"
    "| 2 | PMBK0004521 | ATM-PN-01 | 26-Oct-2026 | 2350000 | 1880000 |\n"
    "| 3 | PMBK0004521 | ATM-PN-02 | 28-Oct-2026 | 1500000 | 600000 |\n"
    "| 4 | PMBK0007810 | ATM-DL-01 | 31-Oct-2026 | 2000000 | 1900000 |\n"
    "| 5 | PMBK0007810 | ATM-DL-02 | 03-Nov-2026 | 1800000 | 1710000 |\n"
    "| 6 | PMBK0003302 | ATM-AG-01 | 04-Nov-2026 | 1200000 | 540000 |\n"
    "| 7 | PMBK0003302 | ATM-AG-02 | 05-Nov-2026 | 900000 | 450000 |\n\n"
    "Cell G2 holds the date 02-Nov-2026, a branch holiday. (PMBK is a made-up bank code.)",
    "An IFSC has 11 characters: 4 letters for the bank, a fifth character 0, and 6 characters for the branch. "
    "26-Oct-2026 is a Monday and 31-Oct-2026 a Saturday. From 26-Oct to 05-Nov there are 9 weekdays, 8 after "
    "excluding the 2-Nov holiday. Row 5 dispensed 95% of its load.")
o = ["PMBK", "PMBK0", "4521", "0004521"]
Q(T, "MS Excel", "Basic",
  "Refer to the ATM register. An Indian IFSC has 11 characters, and its first four letters identify the bank. What "
  "does =LEFT(A2, 4) return?", o,
  concept="LEFT text function",
  explanation="LEFT(text, n) returns the first n characters. The first 4 characters of PMBK0004521 are PMBK, the "
              "bank code. (The fifth character of an IFSC is 0 and the last six identify the branch.)",
  steps=["LEFT('PMBK0004521', 4)", "= PMBK"],
  wrong="PMBK0 has five characters. 4521 and 0004521 are taken from the right side (as RIGHT would do).",
  seconds=15, computed=True, stim=S_XL, pos=1,
  facts=[fact("RBI NEFT FAQ: IFSC is an 11-character code; the first four alphabetic characters represent the bank, "
              "the fifth character is 0 and the last six characters represent the branch.", RBI_NEFT_FAQ)])
o, a = ordered(3, [2, 2.35, 4], fmt=lambda v: f"{v:g}")
Q(T, "MS Excel", "Intermediate",
  "Refer to the ATM register. Each cash cassette holds at most Rs 10,00,000. To find how many cassettes ATM-PN-01 "
  "needs for its load, the clerk enters =ROUNDUP(D2/1000000, 0). What does it return?", o, a,
  concept="ROUNDUP",
  explanation="D2 / 1,000,000 = 2,350,000 / 1,000,000 = 2.35. ROUNDUP rounds away from zero to 0 decimal places, "
              "giving 3 (two cassettes cannot hold Rs 23.5 lakh).",
  steps=["2,350,000 / 1,000,000 = 2.35", "ROUNDUP(2.35, 0) = 3"],
  wrong="2 is what ROUND or INT would give, leaving Rs 3.5 lakh without a cassette. 2.35 ignores the rounding. 4 "
        "over-rounds.", seconds=30, computed=True, stim=S_XL, pos=2,
  facts=[fact("Microsoft: ROUNDUP rounds a number up, away from 0 (zero).", MS_ROUNDUP)])
o = ["Saturday", "Friday", "Sunday", "31"]
Q(T, "MS Excel", "Advanced",
  "Refer to the ATM register. Given that 26-Oct-2026 (cell C2) is a Monday, what does =TEXT(C4, \"dddd\") return?",
  o,
  concept="TEXT function with date format codes",
  explanation="The format code dddd shows the full name of the weekday. C4 is 31-Oct-2026, five days after Monday "
              "26-Oct, so it is a Saturday.",
  steps=["26-Oct = Monday", "+5 days = 31-Oct = Saturday", "dddd -> full day name"],
  wrong="Friday and Sunday are a day off. '31' would be the result of the code d or dd (day of the month).",
  seconds=40, computed=True, stim=S_XL, pos=3,
  facts=[fact("Microsoft TEXT function: =TEXT(TODAY(),\"DDDD\") returns today's day of the week, like Monday.",
              MS_TEXT)])
o, a = ordered(8, [7, 9, 11])
Q(T, "MS Excel", "Advanced",
  "Refer to the ATM register. What does =NETWORKDAYS(C2, C7, G2) return? (NETWORKDAYS counts working days from the "
  "start date to the end date, both included, leaving out Saturdays, Sundays and the listed holidays.)", o, a,
  concept="NETWORKDAYS",
  explanation="From Monday 26-Oct to Thursday 05-Nov 2026: 26-30 Oct gives 5 weekdays, 2-5 Nov gives 4 weekdays, "
              "total 9. The holiday in G2 (Monday 02-Nov) is removed: 9 - 1 = 8.",
  steps=["26-30 Oct: 5 weekdays", "31 Oct, 1 Nov: weekend", "2-5 Nov: 4 weekdays", "9 - 1 holiday = 8"],
  wrong="9 forgets the holiday. 7 also leaves out the start date. 11 counts every calendar day.", seconds=60,
  computed=True, stim=S_XL, pos=4,
  facts=[fact("Microsoft: NETWORKDAYS returns the number of whole working days between start_date and end_date; "
              "working days exclude weekends and dates identified in holidays (example: 1-Oct-2012 to 1-Mar-2013 "
              "= 110, used to confirm both ends are counted).", MS_NETWORKDAYS)])
o = ["Watch", "Reload today", "OK", "#N/A"]
Q(T, "MS Excel", "Advanced",
  "Refer to the ATM register. A clerk writes this formula for row 5:\n\n=IFS(E5/D5>=0.6, \"Watch\", E5/D5>=0.9, "
  "\"Reload today\", TRUE, \"OK\")\n\nWhat does it return?", o,
  concept="IFS returns the first TRUE condition",
  explanation="E5 / D5 = 1,710,000 / 1,800,000 = 0.95. IFS checks the conditions in order and returns the value of "
              "the FIRST one that is TRUE. 0.95 >= 0.6 is already TRUE, so the result is 'Watch', even though 0.95 "
              ">= 0.9 is also true. The tests should be written from the strictest (>= 0.9) down.",
  steps=["Ratio = 0.95", "First test 0.95 >= 0.6 -> TRUE", "Return 'Watch'"],
  wrong="'Reload today' would need the 0.9 test to come first. 'OK' is reached only when both tests fail. #N/A "
        "appears only when no condition is TRUE, but here TRUE is the last test anyway.", seconds=50, computed=True,
  stim=S_XL, pos=5,
  facts=[fact("Microsoft: IFS returns a value that corresponds to the first TRUE condition; if no TRUE conditions "
              "are found, it returns #N/A.", MS_IFS)])
Q(T, "Shortcuts", "Basic",
  "In MS Word for Windows, which keyboard shortcut aligns the selected paragraph to the RIGHT margin, as often done "
  "for the date line of a letter?", ["Ctrl + R", "Ctrl + L", "Ctrl + E", "Ctrl + J"],
  concept="Paragraph alignment shortcuts",
  explanation="Ctrl + R right-aligns the paragraph. Ctrl + L left-aligns, Ctrl + E centres and Ctrl + J justifies.",
  steps=["Right align = Ctrl + R"],
  wrong="Ctrl + L, Ctrl + E and Ctrl + J give left, centre and justified alignment.", seconds=10,
  facts=[fact("Microsoft Word keyboard shortcuts: Ctrl+R right-aligns the paragraph.", MS_WORD_KEYS)])
Q(T, "MS PowerPoint", "Basic",
  "During a PowerPoint slide show, a trainer wants the screen to go completely black for a while to hold the "
  "audience's attention, and then to return to the same slide. Which key does this (on Windows)?",
  ["B", "W", "Esc", "Home"],
  concept="Slide-show controls",
  explanation="Pressing B (or the full stop key) shows a blank black screen; pressing it again returns to the "
              "presentation at the same slide.",
  steps=["Black screen = B", "Press B again to return"],
  wrong="W shows a blank WHITE screen. Esc ends the slide show. Home jumps to the first slide.", seconds=15,
  facts=[fact("Microsoft: during a slide show, B or Period displays a blank black slide or returns from it; W or "
              "Comma displays a blank white slide.", MS_PPT_DELIVER)])
Q(T, "Shortcuts", "Intermediate",
  "A clerk typed a heading in all small letters. In MS Word, which shortcut cycles the selected text through "
  "UPPERCASE, lowercase and Capitalise Each Word?", ["Shift + F3", "Shift + F7", "Ctrl + F3", "Alt + F3"],
  concept="Change case shortcut",
  explanation="Shift + F3 cycles the selected text through uppercase, lowercase and title (each word capitalised) "
              "case.",
  steps=["Change case = Shift + F3"],
  wrong="Shift + F7 opens the Thesaurus. The other combinations do not change case.", seconds=15,
  facts=[fact("Microsoft Word keyboard shortcuts: Shift+F3 switches the selected text between uppercase, lowercase "
              "and title case; Shift+F7 opens the Thesaurus.", MS_WORD_KEYS)])
Q(T, "Shortcuts", "Intermediate",
  "In Excel for Windows, a clerk selects a block of loan data and wants to convert it into an Excel Table with "
  "banded rows, filter buttons and automatic expansion for new rows. Which shortcut opens the Create Table dialog?",
  ["Ctrl + T", "Ctrl + 1", "Ctrl + Page Down", "Alt + ="],
  concept="Excel shortcuts",
  explanation="Ctrl + T (or Ctrl + L) displays the Create Table dialog, which turns the selected range into a "
              "structured Excel Table.",
  steps=["Create Table = Ctrl + T"],
  wrong="Ctrl + 1 opens Format Cells. Ctrl + Page Down moves to the next sheet. Alt + = inserts AutoSum.",
  seconds=15,
  facts=[fact("Microsoft Excel keyboard shortcuts (Windows): Ctrl+L or Ctrl+T displays the Create Table dialog box; "
              "Ctrl+Page Down moves to the next sheet.", MS_EXCEL_KEYS)])
Q(T, "MS Word", "Advanced",
  "In a long loan agreement, a paragraph sometimes leaves just its first line alone at the bottom of a page, or "
  "just its last line alone at the top of the next page. Which paragraph setting in Word (Paragraph > Line and Page "
  "Breaks) prevents these single stranded lines?",
  ["Widow/Orphan control", "Keep with next", "Page break before", "Suppress line numbers"],
  concept="Pagination control",
  explanation="Widow/Orphan control stops Word from printing the last line of a paragraph by itself at the top of "
              "a page (a widow) or the first line by itself at the bottom of a page (an orphan); it moves an extra "
              "line so at least two stay together. It is on by default.",
  steps=["Single line stranded at page top/bottom = widow/orphan", "Paragraph > Line and Page Breaks"],
  wrong="Keep with next keeps a paragraph on the same page as the next one (used for headings). Page break before "
        "always starts the paragraph on a new page. Suppress line numbers hides line numbering.", seconds=25,
  facts=[fact("Microsoft: Widow/Orphan control is a Pagination option on the Line and Page Breaks tab of the "
              "Paragraph dialog and is turned on by default.", MS_LINEBREAKS)])

# ================================================================ 12. Digital Payments (1 / 1 / 1)
T = "Digital Payments"
Q(T, "Payment technology", "Basic",
  "Which NPCI-operated system lets customers pay electricity, water, gas and telecom bills of many billers through "
  "banks, apps and agent outlets in one interoperable network, with instant confirmation?",
  ["Bharat Bill Payment System (BBPS)", "RTGS", "AePS", "NACH"],
  concept="Bill payment infrastructure",
  explanation="BBPS, conceived by the RBI and run by NPCI, is an interoperable bill-payment system: a customer "
              "can pay many billers' bills through any participating bank, app or agent and get instant "
              "confirmation.",
  steps=["Interoperable utility bill payments = BBPS"],
  wrong="RTGS is RBI's large-value funds transfer system. AePS is Aadhaar-based cash withdrawal and transfer. NACH "
        "handles bulk debits and credits such as salaries and EMIs.", seconds=15,
  facts=[fact("NPCI: Bharat Bill Payment System, an RBI-conceptualised interoperable bill-payment system operated by "
              "NPCI, covering electricity, water, gas and telecom bills with instant confirmation (pilot launched "
              "2016).", NPCI_BBPS)], web=SC)
Q(T, "Payment technology", "Intermediate",
  "A shopper wants to pay a merchant by scanning a UPI QR code but have the amount charged to her credit card rather "
  "than her savings account. Which type of credit card can be linked to a UPI ID for this purpose?",
  ["A RuPay credit card", "Any foreign-issued credit card", "Only a corporate card of an international network",
   "No credit card; UPI works only with bank accounts"],
  concept="Credit cards on UPI",
  explanation="NPCI allows RuPay credit cards to be linked to UPI IDs in UPI apps. The customer sets a UPI PIN for "
              "the card and can then pay merchants by scanning QR codes, with the amount billed to the card.",
  steps=["Credit card linked on UPI = RuPay credit card"],
  wrong="Foreign-issued cards cannot be linked to UPI. The facility is for RuPay credit cards. UPI is no longer "
        "limited to bank accounts.", seconds=20,
  facts=[fact("NPCI 'RuPay Credit Card on UPI': customers can link RuPay credit cards to a UPI ID on UPI apps; only "
              "RuPay credit cards are eligible.", NPCI_RUPAY_UPI)], web=SC)
Q(T, "Card security", "Advanced",
  "A bank's PIN pads encrypt each customer's PIN with a different key for every transaction, all derived from one "
  "base key held securely at the bank, so that if one transaction key is ever exposed, past and future "
  "transactions remain protected. Which key-management scheme is this?",
  ["DUKPT (Derived Unique Key Per Transaction)", "A single static key shared by every terminal",
   "ROT13 substitution", "Hashing the PIN with MD5"],
  concept="DUKPT key management",
  explanation="DUKPT gives each transaction a unique key derived from a base derivation key; the terminal sends a "
              "key serial number so the host can re-derive the key. Compromise of one derived key does not reveal "
              "keys of past or future transactions.",
  steps=["Unique key per transaction from a base key = DUKPT"],
  wrong="A shared static key exposes every terminal if leaked. ROT13 is a trivial letter substitution, not "
        "encryption. MD5 is a broken hash and is not reversible encryption of the PIN.", seconds=25,
  facts=[fact("DUKPT: for every transaction a unique key is used which is derived from a fixed key; if a derived "
              "key is compromised, future and past transaction data are still protected.", WIKI_DUKPT)])

# ================================================================ 13. Computer Abbreviations (3 / 4 / 1)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic",
  "Training videos are distributed to branches on a DVD. What does DVD stand for?",
  ["Digital Versatile Disc", "Digital Video Drive", "Direct Visual Display", "Dual Volume Disk"],
  concept="Storage abbreviations",
  explanation="DVD stands for Digital Versatile Disc (originally often called Digital Video Disc), an optical disc "
              "holding about 4.7 GB per layer.",
  steps=["DVD = Digital Versatile Disc"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic",
  "Most branch monitors and the token display boards use LED backlighting. What does LED stand for?",
  ["Light Emitting Diode", "Liquid Electronic Display", "Low Energy Device", "Laser Enhanced Diode"],
  concept="Display abbreviations",
  explanation="LED = Light Emitting Diode, a semiconductor that gives out light when current flows through it.",
  steps=["LED = Light Emitting Diode"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic",
  "A short animated banner on the bank's intranet is saved as a GIF file. What does GIF stand for?",
  ["Graphics Interchange Format", "General Image File", "Graphic Interface Frame", "Global Image Format"],
  concept="File-format abbreviations",
  explanation="GIF = Graphics Interchange Format, a lossless image format limited to 256 colours that also "
              "supports simple animation.",
  steps=["GIF = Graphics Interchange Format"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "The bank's developers write, run and debug code in an IDE such as Visual Studio Code or Eclipse. What does IDE "
  "stand for?",
  ["Integrated Development Environment", "Internal Data Exchange", "Interactive Design Editor",
   "Intelligent Debugging Engine"],
  concept="Software abbreviations",
  explanation="An IDE (Integrated Development Environment) combines an editor, build tools and a debugger in one "
              "application.",
  steps=["IDE = Integrated Development Environment"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "A customer's phone lists nearby Wi-Fi networks by name, such as 'Branch_Guest'. This network name is called the "
  "SSID. What does SSID stand for?",
  ["Service Set Identifier", "Secure Signal ID", "System Security Identity", "Shared Station Index"],
  concept="Wireless abbreviations",
  explanation="SSID = Service Set Identifier, the name that identifies a wireless LAN.",
  steps=["SSID = Service Set Identifier"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "Officers read office email on phones and laptops with the IMAP protocol, which keeps mail on the server. What "
  "does IMAP stand for?",
  ["Internet Message Access Protocol", "Internal Mail Allocation Process", "Integrated Mail Application Program",
   "Internet Mailbox Archive Protocol"],
  concept="Email protocol abbreviations",
  explanation="IMAP = Internet Message Access Protocol, used by mail clients to access and manage mailboxes stored "
              "on a server.",
  steps=["IMAP = Internet Message Access Protocol"], wrong="The other expansions are made up.", seconds=10,
  facts=[fact("RFC 9051 is titled 'Internet Message Access Protocol (IMAP) - Version 4rev2'.", RFC9051)])
Q(T, S, "Intermediate",
  "The bank requires MFA for remote access, combining a password with a code from a phone app. What does MFA stand "
  "for?",
  ["Multi-Factor Authentication", "Main Frame Access", "Mobile Fund Authorisation", "Multiple File Allocation"],
  concept="Security abbreviations",
  explanation="MFA = Multi-Factor Authentication: access needs two or more factors from different categories "
              "(something you know, have or are).",
  steps=["MFA = Multi-Factor Authentication"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Advanced",
  "A security bulletin tells the bank's IT team to patch a flaw listed with an identifier of the form "
  "CVE-YYYY-NNNNN. What does CVE stand for?",
  ["Common Vulnerabilities and Exposures", "Critical Virus Emergency", "Computer Vulnerability Evaluation",
   "Certified Vulnerability Entry"],
  concept="Security abbreviations",
  explanation="CVE = Common Vulnerabilities and Exposures, the program that assigns a unique public identifier to "
              "each disclosed cybersecurity vulnerability so that vendors, scanners and advisories refer to it "
              "consistently.",
  steps=["CVE = Common Vulnerabilities and Exposures"], wrong="The other expansions are made up.", seconds=15,
  facts=[fact("CVE.org page title: Common Vulnerabilities and Exposures (CVE).", CVE_OVERVIEW)])

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_009_plan.json").read_text(encoding="utf-8"))
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
    "batch_id": "BATCH_009",
    "created_at": TODAY,
    "notes": f"BATCH_009 Computer Knowledge part: 99 original, mostly scenario-based questions (BANK_COMP_000803 to "
             f"BANK_COMP_000901), {n_set} of them in six shared sets (STIM_COMP_009001-009006: error checks on a "
             "cash-recycler link, branch CCTV recording system, branch firewall rules, cyber-cell complaints, Staff "
             "and Branches tables for SQL, Excel ATM cash-loading register). Computable answers are re-derived in "
             "tools/batch_009/computer.py (Hamming distances, CRC, shifts and masks, MIPS, flags, postfix, bubble "
             "sort, CCTV storage/RAID 6/retention, firewall first-match with ipaddress, SQL in sqlite3, Excel "
             "results with NETWORKDAYS checked against Microsoft's own example). Facts from Microsoft, RFC, MDN, "
             "man7, RBI, CHM, CVE.org and Wikipedia (DUKPT) pages were checked on 2026-11-05; BBPS and RuPay credit "
             "card on UPI were confirmed from search results only (web:search-confirmed).",
    "stimuli": stimuli,
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_009_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
