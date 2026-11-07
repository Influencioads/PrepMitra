"""Writes batches/parts/BATCH_007_COMP.json: the 100 Computer Knowledge questions of BATCH_007.

BATCH_007 leans on applied scenarios built around nine shared stimuli (a pseudocode loop, a Linux terminal session,
a backup schedule, an email header, a branch network description, a security-incident timeline, a biometric test
report, a two-table SQL schema and an Excel loan sheet). Every computable answer is re-derived below with assertions
before the file is written: parity, bit shift, hex colour, hex-to-ASCII, 16-bit two's complement, UTF-8 length,
instruction-format arithmetic, the pseudocode loop (simulated), Linux permission bits and path resolution, backup
restore chains and sizes, subnet / broadcast / longest-prefix match via ipaddress, FAR / FRR, password key space,
SSD endurance, SQL via sqlite3 (with foreign keys enforced) and Excel SORT / COUNTBLANK / SUMIFS / MEDIAN. The plan
quota per (topic, difficulty), subtopics, the ID range, stimulus IDs and the answer-key balance are also asserted. If
any assertion fails, nothing is written.

    python tools/batch_007/computer.py      (run from docs/question-bank)
"""

import ipaddress
import json
import posixpath
import random
import sqlite3
import statistics
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
LETTERS = "ABCD"
CK = "Computer Knowledge"
FIRST_ID = 603
AI = ("ai:author-solve", "ai:independent-check")
COMPUTED = ("script:recompute", "ai:author-solve", "ai:independent-check")
SC = "web:search-confirmed"

_rng = random.Random(20261105 + 7)
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
    sid = f"STIM_COMP_007{_stim_no[0]:03d}"
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
    vb = list(COMPUTED if computed else AI)
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
# Even parity: exactly one received byte has an odd number of 1s
PARITY_OPTS = ["10110101", "11000011", "10101010", "01111110"]
assert [s.count("1") % 2 for s in PARITY_OPTS] == [1, 0, 0, 0]
# Left shift by 2 multiplies by 4
assert 0b00010110 == 22 and (0b00010110 << 2) == 0b01011000 == 88
# Hex colour #FF8C00
assert (0xFF, 0x8C, 0x00) == (255, 140, 0)
# Hex bytes to ASCII
assert bytes.fromhex("42414E4B").decode("ascii") == "BANK"
assert bytes.fromhex("42414D4B").decode("ascii") == "BAMK"
# 16-bit two's complement FF9C
assert 0xFF9C == 65436 and 0xFF9C - 2 ** 16 == -100
# UTF-8 length of the rupee sign U+20B9
assert len("₹".encode("utf-8")) == 3 and "₹".encode("utf-8").hex() == "e282b9"
assert len("A".encode("utf-8")) == 1
# Instruction format: 16-bit instruction, 4-bit opcode, 12-bit address
assert 2 ** 4 == 16 and 2 ** 12 == 4096 and 4 + 12 == 16

# Pseudocode loop (stimulus)


def run_loop(balance, integer_rate=False, limit=1000):
    year, checks = 0, 0
    while True:
        checks += 1
        if not balance < 15000:
            break
        rate = (10 // 100) if integer_rate else F(10, 100)
        balance = balance + balance * rate
        year += 1
        if year > limit:
            return None, None, None  # never terminates
    return year, balance, checks


LOOP_YEAR, LOOP_BAL, LOOP_CHECKS = run_loop(10000)
assert (LOOP_YEAR, LOOP_BAL, LOOP_CHECKS) == (5, F(161051, 10), 6)
assert run_loop(20000)[0] == 0 and run_loop(20000)[2] == 1
assert run_loop(10000, integer_rate=True) == (None, None, None)

# Linux terminal session (stimulus)
LS = [("drwxr-x---", "asha", "audit", "archive"), ("-rw-r-----", "asha", "audit", "loans_oct.csv"),
      ("-rwxr-xr-x", "asha", "audit", "backup.sh"), ("-rw-rw-r--", "ravi", "audit", "notes.txt")]


def octal(perm):
    return "".join(str(sum(b for b, c in zip((4, 2, 1), perm[i:i + 3]) if c != "-")) for i in (1, 4, 7))


assert [p for p, *_ in LS if p.startswith("d")] == ["drwxr-x---"]
assert octal("-rwxr-xr-x") == "755" and octal("-rwxr-xrwx") == "757"
assert LS[3][0][4:7] == "rw-"  # group bits of notes.txt
assert posixpath.normpath(posixpath.join("/home/asha/reports", "..")) == "/home/asha"
assert posixpath.normpath(posixpath.join("/home/asha/reports", "../../ravi/notes.txt")) == "/home/ravi/notes.txt"

# Backup schedule (stimulus): full on Sunday, changes Mon..Sat, failure Thursday 15:00
CHANGES = {"Mon": 6, "Tue": 4, "Wed": 10, "Thu": 5, "Fri": 8, "Sat": 3}
DAYS = list(CHANGES)
INCR_SETS = 1 + DAYS.index("Thu")  # full + Mon, Tue, Wed incrementals
DIFF_SETS = 2  # full + Wednesday differential
assert INCR_SETS == 4
DIFF_SIZES = [sum(list(CHANGES.values())[:i + 1]) for i in range(6)]
assert DIFF_SIZES == [6, 10, 20, 25, 33, 36] and sum(DIFF_SIZES) == 130 and sum(CHANGES.values()) == 36
LOSS_HOURS = (24 - 23) + 15  # Wed 23:00 -> Thu 15:00
assert LOSS_HOURS == 16
# SSD endurance: 600 TBW at 200 GB written per day (1 TB = 1000 GB)
TBW_DAYS = 600 * 1000 / 200
assert TBW_DAYS == 3000 and round(TBW_DAYS / 365, 1) == 8.2

# Branch network (stimulus)
LAN = ipaddress.ip_network("10.20.30.0/26")
assert ipaddress.ip_address("10.20.30.25") in LAN and ipaddress.ip_address("10.20.30.70") not in LAN
assert ipaddress.ip_interface("10.20.30.70/26").network == ipaddress.ip_network("10.20.30.64/26")
assert str(LAN.broadcast_address) == "10.20.30.63" and LAN.num_addresses - 2 == 62
assert ipaddress.ip_address("169.254.18.7") in ipaddress.ip_network("169.254.0.0/16")
ROUTES = {"10.20.0.0/16": "Tunnel to head office", "10.20.30.0/26": "LAN (directly connected)",
          "10.0.0.0/8": "MPLS link", "0.0.0.0/0": "ISP link (default route)"}


def lpm(dst):
    best = max((ipaddress.ip_network(n) for n in ROUTES if ipaddress.ip_address(dst) in ipaddress.ip_network(n)),
               key=lambda n: n.prefixlen)
    return ROUTES[str(best)]


assert lpm("10.20.7.9") == "Tunnel to head office"
assert sum(ipaddress.ip_address("10.20.7.9") in ipaddress.ip_network(n) for n in ROUTES) == 3

# Biometric test report (stimulus)
GENUINE, IMPOSTOR = 2000, 5000
BIO = {"Low": (20, 150), "Medium": (60, 25), "High": (180, 5)}  # (false rejects, false accepts)
FAR = {k: F(fa, IMPOSTOR) for k, (fr, fa) in BIO.items()}
FRR = {k: F(fr, GENUINE) for k, (fr, fa) in BIO.items()}
assert FAR["Medium"] == F(5, 1000) and FRR["High"] == F(9, 100)
assert min(FAR, key=FAR.get) == "High" and min(FRR, key=FRR.get) == "Low"
# Password key space: 8 -> 10 characters from 62 symbols
assert 62 ** 10 // 62 ** 8 == 3844 and 62 ** 2 == 3844

# SQL: two tables (stimulus)
CUST = [(1, "Asha", "Pune"), (2, "Ravi", "Delhi"), (3, "Meena", "Nagpur"), (4, "John", "Pune"),
        (5, "Farah", "Delhi"), (6, "Kiran", "Agra")]
ACC = [("A101", 1, "SB", 45000, "Raj"), ("A102", 1, "FD", 200000, None), ("A103", 2, "SB", 12000, "Sita"),
       ("A104", 3, "CA", 90000, None), ("A105", 4, "SB", 30000, "Anil"), ("A106", 4, "FD", 150000, "Anil"),
       ("A107", 4, "SB", 8000, None), ("A108", 5, "CA", 60000, "Zoya")]
db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.execute("CREATE TABLE Customers (cust_id INTEGER PRIMARY KEY, name TEXT, city TEXT)")
db.execute("CREATE TABLE Accounts (acc_no TEXT PRIMARY KEY, cust_id INTEGER REFERENCES Customers(cust_id), "
           "type TEXT, balance INTEGER, nominee TEXT)")
db.executemany("INSERT INTO Customers VALUES (?, ?, ?)", CUST)
db.executemany("INSERT INTO Accounts VALUES (?, ?, ?, ?, ?)", ACC)
SQL_IN = [r[0] for r in db.execute("SELECT name FROM Customers WHERE city IN ('Pune', 'Agra') ORDER BY cust_id")]
assert SQL_IN == ["Asha", "John", "Kiran"]
SQL_LJ = [r[0] for r in db.execute("SELECT c.name FROM Customers c LEFT JOIN Accounts a ON c.cust_id = a.cust_id "
                                   "WHERE a.acc_no IS NULL")]
assert SQL_LJ == ["Kiran"]
assert db.execute("SELECT COUNT(*) FROM Customers c JOIN Accounts a ON c.cust_id = a.cust_id").fetchone()[0] == 8
SQL_HAV = db.execute("SELECT cust_id, COUNT(*) FROM Accounts GROUP BY cust_id HAVING COUNT(*) >= 2").fetchall()
assert SQL_HAV == [(1, 2), (4, 3)]
assert len(db.execute("SELECT cust_id FROM Accounts GROUP BY cust_id").fetchall()) == 5
SQL_CNT = db.execute("SELECT COUNT(*), COUNT(nominee), COUNT(DISTINCT nominee) FROM Accounts").fetchone()
assert SQL_CNT == (8, 5, 4)
FK_TRY = {"('A109', 6, 'SB', 5000, NULL)": True, "('A110', 2, 'FD', 75000, 'Sita')": True,
          "('A111', 7, 'SB', 5000, NULL)": False, "('A112', 1, 'CA', 20000, NULL)": True}
for vals, ok in FK_TRY.items():
    try:
        db.execute("SAVEPOINT s")
        db.execute(f"INSERT INTO Accounts VALUES {vals}")
        accepted = True
    except sqlite3.IntegrityError:
        accepted = False
    db.execute("ROLLBACK TO s")
    db.execute("RELEASE s")
    assert accepted == ok, vals
SQL_AVG = db.execute("SELECT AVG(balance) FROM Accounts").fetchone()[0]
assert SQL_AVG == 74375
SQL_SUB = [r[0] for r in db.execute(
    "SELECT name FROM Customers WHERE cust_id IN (SELECT cust_id FROM Accounts WHERE balance > "
    "(SELECT AVG(balance) FROM Accounts)) ORDER BY cust_id")]
assert SQL_SUB == ["Asha", "Meena", "John"]

# Excel: loan sheet (stimulus); E = Remarks ('' = blank)
SHEET = [("Asha", "Pune", "Home", 42, "OK"), ("Ravi", "Delhi", "Car", 8, ""), ("Meena", "Pune", "Car", 12,
         "Docs pending"), ("John", "Agra", "Home", 35, ""), ("Farah", "Pune", "Home", 28, "OK"),
         ("Kiran", "Delhi", "Home", 50, ""), ("Vikas", "Pune", "Gold", 3, "OK"), ("Neha", "Agra", "Car", 10, "")]
SORTED = sorted(SHEET, key=lambda r: -r[3])
assert [r[0] for r in SORTED[:3]] == ["Kiran", "Asha", "John"]  # data rows 2, 3, 4 after sorting
assert sum(1 for r in SHEET if r[4] == "") == 4
SUMIFS = sum(r[3] for r in SHEET if r[1] == "Pune" and r[2] == "Home")
assert SUMIFS == 70 and sum(r[3] for r in SHEET if r[1] == "Pune") == 85
assert sum(r[3] for r in SHEET if r[2] == "Home") == 155
MED = statistics.median(r[3] for r in SHEET)
assert MED == 20 and F(sum(r[3] for r in SHEET), 8) == F(188, 8)
assert sorted(r[3] for r in SHEET)[3:5] == [12, 28]

# ---------------------------------------------------------------- fact-check sources
# Pages opened on 2026-11-05 (web:fact-check)
CHM_PASCAL = "https://www.computerhistory.org/revolution/calculators/1/47"
CHM_JACQUARD = "https://computerhistory.org/blog/artifact-adopted-preserving-the-legend-of-j-m-jacquard/"
MS_SECUREBOOT = "https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-secure-boot"
MS_WIN = "https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec"
MAN_CHMOD = "https://man7.org/linux/man-pages/man1/chmod.1.html"
POSIX_SH = "https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html"
RFC5322 = "https://www.rfc-editor.org/rfc/rfc5322#section-3.6.2"
RFC5321 = "https://www.rfc-editor.org/rfc/rfc5321#section-4.4"
RFC6409 = "https://www.rfc-editor.org/rfc/rfc6409"
MDN_403 = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/403"
MDN_3PC = "https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Third-party_cookies"
RFC3927 = "https://www.rfc-editor.org/rfc/rfc3927"
RFC4301 = "https://www.rfc-editor.org/rfc/rfc4301"
MITRE_LM = "https://attack.mitre.org/tactics/TA0008/"
MITRE_C2 = "https://attack.mitre.org/tactics/TA0011/"
MITRE_EX = "https://attack.mitre.org/tactics/TA0010/"
MS_XL_KEYS = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-9b7213f0040f"
MS_FLASH = "https://support.microsoft.com/en-au/office/flash-fill-a-column-of-data-3a9337e2-ccd9-4203-bec5-027d255f0d0e"
MS_WATERMARK = "https://support.microsoft.com/en-us/word/training/insert-a-watermark"
MS_HIDE = "https://support.microsoft.com/en-us/powerpoint/hide-or-show-a-slide"
MS_REHEARSE = "https://support.microsoft.com/en-us/powerpoint/training/rehearse-and-time-the-delivery-of-a-presentation"
# Confirmed only in search results (web:search-confirmed)
PARAM = "https://en.wikipedia.org/wiki/PARAM"
TURING = "https://computinghistory.org.uk/det/6028/Alan%20Turing%20invents%20the%20principle%20of%20the%20modern%20computer"
ERUPI = "https://www.npci.org.in/PDF/npci/e-rupi/Product-Booklet.pdf"
AUTOPAY = ("https://npci.org.in/PDF/npci/press-releases/2020/NPCI_Press_Release-NPCI_introduces_AutoPay_facility_on_"
           "UPI_for_recurring_payments.pdf")
FASTAG = "https://en.vikaspedia.in/e-governance/citizen-services/fastag-for-electronic-toll-collection"
UPI_SHIELD = "https://npci.org.in/what-we-do/upi/upi-safety-shield"
CERTIN = ("https://en.vikaspedia.in/education/digital-litercy/information-security/directions-of-certin-on-"
          "information-security")

# ================================================================ 1. Computer Fundamentals (3 / 6 / 3)
T = "Computer Fundamentals"
Q(T, "Generations and history", "Basic",
  "IBM's System/360 family of the mid-1960s replaced discrete transistors with integrated circuits (ICs), each "
  "holding many transistors on one small silicon chip. To which generation of computers do IC-based machines like "
  "this belong?",
  ["Third generation", "First generation", "Second generation", "Fifth generation"],
  concept="Generations of computers",
  explanation="First generation: vacuum tubes. Second: transistors. Third: integrated circuits (SSI/MSI chips), "
              "which made computers smaller, cheaper and more reliable. Fourth: microprocessors (VLSI). Fifth: "
              "AI-oriented, ULSI and parallel processing.",
  steps=["Vacuum tube -> transistor -> IC -> microprocessor", "IC = third generation"],
  wrong="First generation used vacuum tubes and second generation discrete transistors. Fifth generation refers "
        "to AI-oriented, massively parallel systems.", seconds=15)
Q(T, "Types of computers", "Basic",
  "India's Centre for Development of Advanced Computing (C-DAC) builds the PARAM series of machines, which are "
  "used for weather forecasting, drug discovery and other research needing enormous calculation speed. What type "
  "of computer is a PARAM machine?",
  ["Supercomputer", "Minicomputer", "Embedded computer", "Personal computer"],
  concept="Types of computers by capacity",
  explanation="PARAM is C-DAC's family of supercomputers, starting with PARAM 8000 in the early 1990s; newer "
              "systems have been installed under the National Supercomputing Mission.",
  steps=["PARAM = C-DAC's supercomputer series"],
  wrong="Minicomputers are mid-sized multi-user machines, embedded computers control one device, and personal "
        "computers serve one user; none is meant for national-scale scientific computing.", seconds=15,
  facts=[fact("PARAM is a series of supercomputers designed and assembled by C-DAC, Pune; PARAM 8000 was "
              "unveiled around 1990-91.", PARAM)], web=SC)
o = list(PARITY_OPTS)
Q(T, "Number systems", "Basic",
  "A bank's old data link sends 8-bit codes using EVEN parity, so every correctly received code must contain an "
  "even number of 1s. Which received code must have been corrupted on the way?", o,
  concept="Parity check",
  explanation="With even parity, the sender sets the parity bit so that the total number of 1s is even. A received "
              "code with an odd number of 1s is therefore certainly wrong. 10110101 has five 1s (odd). The other "
              "three codes have four or six 1s.",
  steps=["Count 1s: 10110101 -> 5", "11000011 -> 4, 10101010 -> 4, 01111110 -> 6", "Odd count = error"],
  wrong="11000011, 10101010 and 01111110 each have an even number of 1s, so they pass the even-parity check.",
  seconds=30, computed=True)
o, a = ordered(88, [24, 44, 176])
Q(T, "Number systems", "Intermediate",
  "A register holds the 8-bit value 00010110. The processor shifts all bits two places to the LEFT, filling the "
  "empty places with 0 (no 1-bit is lost). What decimal value does the register now hold?", o, a,
  concept="Binary shift = multiply by a power of 2",
  explanation="00010110 = 16 + 4 + 2 = 22. Shifting left by one place doubles a binary number; by two places it "
              "multiplies by 4. 01011000 = 64 + 16 + 8 = 88.",
  steps=["00010110 = 22", "Left shift by 2 -> 01011000", "= 64 + 16 + 8 = 88 (= 22 x 4)"],
  shortcut="Left shift by n multiplies by 2^n (while no 1-bit falls off).",
  wrong="44 is a shift by only one place. 176 is a shift by three places. 24 just adds 2.", seconds=30,
  computed=True)
o = ["Red 255, Green 140, Blue 0", "Red 255, Green 128, Blue 0", "Red 15, Green 140, Blue 0",
     "Red 255, Green 140, Blue 12"]
Q(T, "Number systems", "Intermediate",
  "The bank's website uses the colour code #FF8C00 for its buttons. Such a code gives the red, green and blue "
  "intensities as three pairs of hexadecimal digits (RRGGBB). What are the decimal intensities?", o,
  concept="Hexadecimal colour codes",
  explanation="Split into pairs: FF, 8C, 00. FF = 15 x 16 + 15 = 255. 8C = 8 x 16 + 12 = 140. 00 = 0. So red 255, "
              "green 140, blue 0 (an orange shade).",
  steps=["FF = 255", "8C = 8 x 16 + 12 = 140", "00 = 0"],
  wrong="128 would be 80 in hex. 15 reads only one F. 12 wrongly takes C as a separate blue value.", seconds=40,
  computed=True)
o = ["BANK", "BAMK", "CANK", "BANL"]
Q(T, "Number systems", "Intermediate",
  "A hex dump of a file shows the four bytes 42 41 4E 4B. In ASCII, 'A' is 41 (hex) and the capital letters follow "
  "in alphabetical order. What text do these bytes spell?", o,
  concept="Hexadecimal and ASCII",
  explanation="41 = A, so 42 = B. 4E is 41 + D (13) places on: A + 13 = N. 4B is A + 10 = K. The text is BANK.",
  steps=["41 = A, 42 = B", "4E - 41 = 0D = 13 -> N", "4B - 41 = 0A = 10 -> K"],
  wrong="BAMK reads 4E as M (4D). CANK takes 42 as C (43). BANL reads 4B as L (4C).", seconds=40, computed=True)
Q(T, "Generations and history", "Intermediate",
  "In the 1640s a French mathematician built a mechanical calculating machine with toothed wheels to help his "
  "father, a tax collector, with additions. Who built this machine, and what is it called?",
  ["Blaise Pascal - the Pascaline", "Charles Babbage - the Difference Engine",
   "Gottfried Leibniz - the Stepped Reckoner", "John Napier - Napier's bones"],
  concept="Early calculating machines",
  explanation="Blaise Pascal invented the Pascaline in the 1640s for his tax-collector father; it could add "
              "(subtraction was done by complements). It is one of the earliest mechanical calculators.",
  steps=["1640s + tax-collector father = Pascal's Pascaline"],
  wrong="Babbage's Difference Engine is from the 1820s. Leibniz's Stepped Reckoner (1670s) could also multiply. "
        "Napier's bones (1617) were numbered rods, not a geared machine.", seconds=20,
  facts=[fact("CHM: In the 1640s Pascal invented for his father, a tax collector, a machine that could add.",
              CHM_PASCAL)])
Q(T, "Generations and history", "Intermediate",
  "In 1804 a French weaver built a loom whose weaving pattern was controlled by a chain of punched cards; "
  "Charles Babbage later planned to use punched cards to feed instructions to his Analytical Engine. Who built "
  "this loom?",
  ["Joseph-Marie Jacquard", "Herman Hollerith", "Blaise Pascal", "Konrad Zuse"],
  concept="Punched cards in computing history",
  explanation="Joseph-Marie Jacquard's loom (1804) used punched cards to select which threads were lifted, so the "
              "pattern could be changed by changing the cards. Babbage borrowed the idea for the Analytical "
              "Engine, and Hollerith later used punched cards for census data.",
  steps=["Loom + punched cards + 1804 = Jacquard"],
  wrong="Hollerith used punched cards for the 1890 US census, not for weaving. Pascal built an adding machine. "
        "Zuse built early electromechanical computers in the 1930s-40s.", seconds=20,
  facts=[fact("CHM: Jacquard developed his card control for power looms in 1804; Babbage designed the Analytical "
              "Engine with a control mechanism using loops of punched cards.", CHM_JACQUARD)])
Q(T, "Types of computers", "Intermediate",
  "In the 1970s, a regional office ran its accounts on a mid-sized computer that was much cheaper and smaller "
  "than a mainframe but still served about 30 terminals at the same time, such as a DEC PDP or VAX machine. In "
  "the size-based classification, what is such a computer called?",
  ["Minicomputer", "Microcomputer", "Supercomputer", "Thin client"],
  concept="Types of computers by size",
  explanation="Minicomputers sit between mainframes and microcomputers: multi-user machines for a department or "
              "medium-sized organisation. DEC's PDP and VAX lines are classic examples. Today mid-range servers fill "
              "this role.",
  steps=["Multi-user, smaller than a mainframe, bigger than a PC = minicomputer"],
  wrong="A microcomputer is a single-user PC. A supercomputer is for very heavy scientific work. A thin client is "
        "a terminal that depends on a server.", seconds=20)
o, a = ordered(-100, [-99, 100, 65436])
Q(T, "Number systems", "Advanced",
  "A program stores a balance adjustment as a 16-bit signed integer in two's complement form. Its memory shows "
  "the hexadecimal value FF9C. What decimal value does it represent?", o, a,
  concept="16-bit two's complement",
  explanation="The leading hex digit F means the sign bit is 1, so the number is negative. Its value is "
              "(unsigned value) - 2^16 = 65,436 - 65,536 = -100. Check: +100 = 0064 hex; invert -> FF9B; add 1 "
              "-> FF9C.",
  steps=["FF9C unsigned = 65,436", "Sign bit 1 -> subtract 2^16 = 65,536", "65,436 - 65,536 = -100"],
  shortcut="Negative value = -(2^16 - unsigned value) = -(65,536 - 65,436).",
  wrong="65,436 reads the bits as unsigned. -99 forgets to add 1 after inverting (one's complement). +100 ignores "
        "the sign bit.", seconds=60, computed=True)
o, a = ordered(3, [1, 2, 4])
Q(T, "Number systems", "Advanced",
  "A bank's app stores text in UTF-8. English letters such as 'A' (U+0041) take 1 byte each. How many bytes does "
  "UTF-8 use for the Indian rupee sign (U+20B9)?", o, a,
  concept="UTF-8 variable-length encoding",
  explanation="UTF-8 uses 1 byte for U+0000-U+007F, 2 bytes for U+0080-U+07FF, 3 bytes for U+0800-U+FFFF and 4 "
              "bytes above that. U+20B9 lies in U+0800-U+FFFF, so it takes 3 bytes (E2 82 B9).",
  steps=["U+20B9 > U+07FF and <= U+FFFF", "-> 3-byte form", "Encoded as E2 82 B9"],
  wrong="1 byte is only for ASCII characters. 2 bytes cover up to U+07FF (e.g. many Latin, Greek and Arabic "
        "letters). 4 bytes are for code points above U+FFFF, such as emoji.", seconds=45, computed=True)
Q(T, "Generations and history", "Advanced",
  "In a 1936 paper, 'On Computable Numbers', a British mathematician described an abstract machine that reads and "
  "writes symbols on an endless tape, one square at a time, following a table of rules. The idea became the "
  "theoretical model of a general-purpose computer. Who wrote it?",
  ["Alan Turing", "John von Neumann", "Claude Shannon", "Charles Babbage"],
  concept="Theoretical foundations of computing",
  explanation="Alan Turing's 1936 paper defined what is now called the Turing machine, and showed that one "
              "universal machine could imitate any other, the basic idea of a stored-program computer.",
  steps=["1936 + 'On Computable Numbers' + tape machine = Alan Turing"],
  wrong="Von Neumann described the stored-program architecture in 1945. Shannon founded information theory "
        "(1948). Babbage designed mechanical engines in the 1800s.", seconds=20,
  facts=[fact("Turing's paper 'On Computable Numbers' (1936) described an abstract machine with a tape of "
              "symbols read and written by a head following rules.", TURING)], web=SC)

# ================================================================ 2. Hardware (2 / 1 / 1)
T = "Hardware"
o = ["The processor's clock ticks about 3 billion times per second", "The processor can store 3 GB of data",
     "The processor can run 3 programs at once", "The processor's cache is 3 GB"]
Q(T, "CPU and components", "Basic",
  "A teller PC's specification reads: 'Processor: 6 cores, 3.0 GHz'. What does '3.0 GHz' tell you?", o,
  concept="Clock speed",
  explanation="GHz (gigahertz) measures the processor's clock frequency. 3.0 GHz = 3 x 10^9 clock cycles per "
              "second; each cycle is a step in which the processor can do work.",
  steps=["Hz = cycles per second", "Giga = 10^9", "3.0 GHz = 3 billion cycles per second"],
  wrong="Storage and cache are measured in bytes (MB, GB), not hertz. The number of programs handled at once "
        "depends on cores and threads, not on GHz.", seconds=15)
Q(T, "CPU and components", "Basic",
  "While fitting a new heat sink on a processor, a technician first spreads a thin layer of grey paste on top of "
  "the processor. What is this paste for?",
  ["It fills tiny air gaps so that heat passes better from the processor to the heat sink",
   "It glues the processor permanently into its socket", "It insulates the processor from electric current",
   "It stores the processor's settings when the PC is off"],
  concept="Thermal interface material",
  explanation="Thermal paste (thermal compound) fills the microscopic unevenness between the processor's metal lid "
              "and the heat sink. Air conducts heat poorly, so filling these gaps lets heat flow into the heat "
              "sink and keeps the processor cool.",
  steps=["Paste between CPU and heat sink = better heat transfer"],
  wrong="The processor is held by the socket's lever, not glued. The paste is not an electrical insulator for the "
        "chip. Settings are kept in firmware/CMOS memory.", seconds=15)
Q(T, "Motherboard and ports", "Intermediate",
  "A bank enables Secure Boot in the UEFI firmware of all its desktops. What does this feature do when a PC starts?",
  ["The firmware checks the digital signature of each piece of boot software and runs only trusted, signed "
   "software", "It encrypts the whole hard disk before Windows starts",
   "It asks for a BIOS password every time the PC is switched on", "It scans all user files for viruses before the "
   "desktop appears"],
  concept="UEFI Secure Boot",
  explanation="With Secure Boot, the firmware verifies the signatures of UEFI drivers, boot loaders and the "
              "operating system loader against a database of trusted keys. Unsigned or tampered boot code, such "
              "as a bootkit, is refused.",
  steps=["Secure Boot = signature check of boot software", "Only trusted (signed) code is allowed to boot"],
  wrong="Disk encryption is done by tools such as BitLocker. A firmware password is a separate setting. File "
        "scanning is antivirus work after Windows starts.", seconds=30,
  facts=[fact("Microsoft: Secure boot helps make sure a device boots using only software trusted by the OEM; the "
              "firmware checks the signature of each piece of boot software.", MS_SECUREBOOT)])
o = ["16 operations and 4,096 memory addresses", "4 operations and 12 memory addresses",
     "16 operations and 65,536 memory addresses", "12 operations and 4,096 memory addresses"]
Q(T, "CPU and components", "Advanced",
  "A simple processor uses 16-bit instructions. The first 4 bits hold the operation code (opcode) and the "
  "remaining 12 bits hold a memory address. How many different operations can the instruction set have, and how "
  "many memory locations can an instruction address directly?", o,
  concept="Instruction format",
  explanation="n bits give 2^n combinations. A 4-bit opcode gives 2^4 = 16 operations; a 12-bit address field "
              "gives 2^12 = 4,096 addressable locations.",
  steps=["Opcode: 2^4 = 16", "Address: 2^12 = 4,096", "4 + 12 = 16 bits in total"],
  wrong="4 and 12 are the field widths, not the counts. 65,536 = 2^16 would need all 16 bits for the address. "
        "12 operations confuses the address width with the opcode count.", seconds=45, computed=True)

# ================================================================ 3. Software (1 / 3 / 3)
T = "Software"
Q(T, "System and application software", "Basic",
  "Before a new mobile-banking app is launched, the bank gives an early, nearly finished version to a group of "
  "outside users so they can report bugs in real use. What is this pre-release version called?",
  ["Beta version", "Final (stable) release", "Patch", "Source code"],
  concept="Software release stages",
  explanation="Alpha testing is done internally; a beta version is released to a limited group of real users to "
              "find remaining bugs before the stable public release.",
  steps=["Early version given to outside users for testing = beta"],
  wrong="The stable release comes after beta. A patch fixes software that is already released. Source code is the "
        "program text written by developers, not a release stage.", seconds=15)
Q(T, "Licensing", "Intermediate",
  "A bank buys 20 licences of an analytics package for its 50 analysts. Any analyst may start the program, but "
  "the licence server allows only 20 people to use it at the same moment; the 21st user must wait until someone "
  "closes it. What type of licence is this?",
  ["Concurrent-user (floating) licence", "Site licence", "OEM licence", "Freeware licence"],
  concept="Software licensing models",
  explanation="A concurrent (floating) licence limits the number of simultaneous users, not the number of "
              "installations or named users. A licence server hands out and takes back licences as people open "
              "and close the program.",
  steps=["Limit on users at the same time = concurrent / floating licence"],
  wrong="A site licence covers every computer at a location without a per-user limit. An OEM licence is tied to "
        "one machine sold with it. Freeware costs nothing and needs no licence server.", seconds=20)
S_CODE = new_stim(
    "input_output", "Pseudocode: years for a deposit to grow",
    "A trainee writes this pseudocode to find how many years a deposit takes to reach Rs 15,000 at 10% interest "
    "compounded yearly:\n\n```\nbalance = 10000\nyear = 0\nWHILE balance < 15000\n    balance = balance + balance "
    "* 10 / 100\n    year = year + 1\nEND WHILE\nPRINT year, balance\n```\n\nAll calculations use exact decimal "
    "arithmetic unless a question says otherwise.",
    "Balance after each pass: 11,000; 12,100; 13,310; 14,641; 16,105.1. The condition is tested 6 times (5 true, "
    "1 false); the program prints 5 and 16105.1.")
o, a = ordered(LOOP_YEAR, [4, 6, 7])
Q(T, "Programming languages", "Intermediate",
  "Refer to the pseudocode. What value of year is printed?", o, a,
  concept="Tracing a WHILE loop",
  explanation="Each pass adds 10%: 10,000 -> 11,000 (year 1) -> 12,100 (2) -> 13,310 (3) -> 14,641 (4) -> "
              "16,105.1 (5). Now balance < 15000 is false, so the loop stops and year = 5 is printed.",
  steps=["Trace balance: 11000, 12100, 13310, 14641, 16105.1", "Loop stops after 5 passes", "Prints 5"],
  wrong="4 stops while the balance (14,641) is still below 15,000. 6 and 7 run extra passes after the condition "
        "has become false.", seconds=60, computed=True, stim=S_CODE, pos=1)
o, a = ordered(0, [1, 5, 10])
Q(T, "Programming languages", "Intermediate",
  "Refer to the pseudocode. If the first line is changed to balance = 20000, how many times will the two "
  "statements inside the loop run?", o, a,
  concept="Entry-controlled (pre-test) loop",
  explanation="A WHILE loop tests its condition BEFORE each pass. 20000 < 15000 is false at the very first test, "
              "so the body never runs; the program prints 0 and 20000.",
  steps=["Condition checked first: 20000 < 15000 is false", "Body runs 0 times"],
  wrong="1 would be true of a post-test (DO ... WHILE / REPEAT ... UNTIL) loop, which runs its body at least once. "
        "5 is the answer for the original deposit. 10 has no basis.", seconds=40, computed=True, stim=S_CODE, pos=2)
o, a = ordered(LOOP_CHECKS, [4, 5, 7])
Q(T, "Programming languages", "Advanced",
  "Refer to the pseudocode, with the original values. How many times is the condition balance < 15000 evaluated "
  "while the program runs?", o, a,
  concept="Counting loop tests",
  explanation="The condition is tested before every pass and once more when it finally fails. There are 5 passes "
              "(true each time) plus 1 final test (16,105.1 < 15,000 is false) = 6 evaluations.",
  steps=["True before each of the 5 passes", "False once at the end", "5 + 1 = 6"],
  shortcut="For a pre-test loop: number of tests = number of passes + 1.",
  wrong="5 counts only the passes and forgets the final failing test. 4 and 7 miscount the passes.", seconds=60,
  computed=True, stim=S_CODE, pos=3)
Q(T, "Programming languages", "Advanced",
  "Refer to the pseudocode. A programmer rewrites the interest line as balance = balance + balance * (10 / 100) "
  "in a language where dividing one integer by another gives an integer result (the fraction is dropped), and "
  "balance is an integer. What happens when the program runs?",
  ["The loop never ends, because 10 / 100 becomes 0 and the balance never grows",
   "It prints 5 and 16105, the same as before", "It stops with a division-by-zero error",
   "It prints 0, because the loop body is skipped"],
  concept="Integer division and infinite loops",
  explanation="Brackets make 10 / 100 be evaluated first. With integer division, 10 / 100 = 0, so balance * 0 = 0 "
              "and balance stays 10,000 for ever. The condition 10000 < 15000 is always true: an infinite loop. "
              "(The original order, balance * 10 / 100, gives 100000 / 100 = 1000 and works.)",
  steps=["10 / 100 in integer division = 0", "balance = balance + 0, never changes", "Condition always true -> "
                                                                                     "infinite loop"],
  wrong="The result is not the same, because the increase is now zero. There is no division by zero (100 is the "
        "divisor). The body is not skipped, since 10000 < 15000 is true.", seconds=60, computed=True, stim=S_CODE,
  pos=4)
Q(T, "Programming languages", "Advanced",
  "A recursive function to compute interest has no base case, so each call makes another call to itself without "
  "ever returning. After a few thousand calls the program crashes. What error does this typically cause?",
  ["Stack overflow, because every unfinished call keeps a frame on the call stack",
   "Syntax error, because recursion is not allowed in most languages",
   "Memory leak, because the heap is never freed", "Deadlock, because two processes wait for each other"],
  concept="Recursion and the call stack",
  explanation="Each function call pushes a stack frame (return address, parameters, local variables). Without a "
              "base case the calls never return, frames pile up, and the limited stack space runs out: a stack "
              "overflow.",
  steps=["Recursive call without base case", "Stack frames keep growing", "Stack space exhausted = stack overflow"],
  wrong="Recursion is legal, so it is not a syntax error. A memory leak is heap memory never released, which grows "
        "slowly. Deadlock involves processes waiting for each other's resources.", seconds=30)

# ================================================================ 4. Operating Systems (3 / 4 / 2)
T = "Operating Systems"
S_LINUX = new_stim(
    "input_output", "Linux terminal session of an audit officer",
    "Asha (user asha, member of group audit) opens a terminal on the bank's Linux audit server:\n\n```\n$ pwd\n"
    "/home/asha/reports\n$ ls -l\n"
    + "\n".join(f"{p} {2 if p.startswith('d') else 1} {u} {g} {n}" for p, u, g, n in LS) +
    "\n```\n\n(Link counts, sizes and dates are omitted. User meena is also a member of group audit; user "
    "ravi owns notes.txt.)",
    "archive is the only directory. notes.txt: owner ravi rw-, group audit rw-, others r--. backup.sh is 755; "
    "after chmod o+w it becomes 757.")
Q(T, "File systems", "Basic",
  "Refer to the terminal session. Which entry is a directory (folder)?",
  ["archive", "loans_oct.csv", "backup.sh", "notes.txt"],
  concept="Reading ls -l output",
  explanation="The first character of each ls -l line shows the type: d = directory, - = regular file. Only the "
              "archive line starts with d.",
  steps=["First character d = directory", "drwxr-x--- ... archive"],
  wrong="loans_oct.csv, backup.sh and notes.txt start with -, so they are regular files (backup.sh is an "
        "executable script, but still a file).", seconds=20, stim=S_LINUX, pos=1)
Q(T, "Windows and Linux basics", "Basic",
  "Refer to the terminal session. Asha types cd .. and then pwd. What does pwd now print?",
  ["/home/asha", "/home", "/home/asha/reports/..", "/"],
  concept="Parent directory ..",
  explanation=".. means the parent of the current directory. The parent of /home/asha/reports is /home/asha, and "
              "pwd prints the current directory's full path.",
  steps=["Current: /home/asha/reports", "cd .. -> one level up", "pwd -> /home/asha"],
  wrong="/home is two levels up. pwd prints the resolved path, not the literal '..'. / is the root directory.",
  seconds=20, computed=True, stim=S_LINUX, pos=2)
Q(T, "Windows and Linux basics", "Intermediate",
  "Refer to the terminal session. User meena (not the owner, but a member of group audit) wants to work on "
  "notes.txt. What may she do with it?",
  ["Read it and change (write) it", "Only read it", "Read, write and execute it", "Nothing at all"],
  concept="Owner / group / others permissions",
  explanation="-rw-rw-r-- splits as owner rw-, group rw-, others r--. Meena is not the owner (ravi) but is in the "
              "file's group (audit), so the group bits rw- apply: read and write, no execute.",
  steps=["Permissions: rw- | rw- | r--", "Meena -> group audit", "Group = rw- -> read and write"],
  wrong="'Only read' is the others' permission. No class has x on this file. She is in the group, so she does have "
        "access.", seconds=40, computed=True, stim=S_LINUX, pos=3)
Q(T, "Windows and Linux basics", "Intermediate",
  "Refer to the terminal session. Asha now runs ls -l > list.txt. What happens?",
  ["The listing is written into list.txt (replacing any earlier contents) instead of being shown on the screen",
   "The listing is shown on the screen and also added to the end of list.txt",
   "Only files larger than list.txt are listed", "list.txt is renamed to ls"],
  concept="Output redirection",
  explanation="> redirects a command's standard output to a file. The file is created if absent, or truncated "
              "(emptied) if it exists, and the output goes there instead of the terminal. >> would append, and "
              "tee would show and save.",
  steps=["> = send output to a file", "Existing file is overwritten", "Nothing is printed on screen"],
  wrong="Appending is >>, and showing on screen while saving needs tee. > is not a comparison operator here. "
        "Renaming is done with mv.", seconds=30, stim=S_LINUX, pos=4,
  facts=[fact("POSIX shell 2.7.2: output redirection opens the file as if with O_TRUNC (truncated) or creates it; "
              ">> opens it with O_APPEND.", POSIX_SH)])
o, a = ordered(757, [755, 775, 777])
Q(T, "Windows and Linux basics", "Advanced",
  "Refer to the terminal session. Asha runs chmod o+w backup.sh. What are the permissions of backup.sh now, in "
  "octal (numeric) form?", o, a,
  concept="Symbolic chmod to octal",
  explanation="backup.sh was rwxr-xr-x = 755. o+w adds write for 'others' only and leaves the rest: rwxr-xrwx. "
              "Owner rwx = 7, group r-x = 5, others rwx = 7 -> 757.",
  steps=["Before: rwx r-x r-x = 755", "o+w: others r-x -> rwx", "After: 7 5 7"],
  wrong="755 is the old value. 775 gives write to the group instead. 777 gives write to group and others.",
  seconds=45, computed=True, stim=S_LINUX, pos=5,
  facts=[fact("chmod(1): u, g, o, a select the owner, the file's group, others not in the group, or all; + adds "
              "the selected bits to the existing mode.", MAN_CHMOD)])
Q(T, "File systems", "Advanced",
  "Refer to the terminal session. Without changing directory, Asha opens the relative path ../../ravi/notes.txt. "
  "Which absolute path does this refer to?",
  ["/home/ravi/notes.txt", "/home/asha/ravi/notes.txt", "/ravi/notes.txt", "/home/asha/reports/ravi/notes.txt"],
  concept="Resolving relative paths",
  explanation="A relative path starts from the current directory /home/asha/reports. The first .. goes to "
              "/home/asha, the second to /home; then ravi/notes.txt gives /home/ravi/notes.txt.",
  steps=["Start: /home/asha/reports", "../ -> /home/asha; ../ -> /home", "+ ravi/notes.txt -> /home/ravi/notes.txt"],
  wrong="/home/asha/ravi/... climbs only one level. /ravi/... climbs three levels. The last option ignores both "
        "'..' parts.", seconds=40, computed=True, stim=S_LINUX, pos=6)
Q(T, "Windows and Linux basics", "Basic",
  "A branch officer wants to open the Windows Settings app quickly to change the display brightness. Which "
  "keyboard shortcut opens Settings?",
  ["Windows logo key + I", "Windows logo key + L", "Windows logo key + E", "Windows logo key + D"],
  concept="Windows keyboard shortcuts",
  explanation="Windows logo key + I opens the Settings app directly.",
  steps=["Win + I = Settings"],
  wrong="Win + L locks the PC, Win + E opens File Explorer and Win + D shows or hides the desktop.", seconds=15,
  facts=[fact("Microsoft: Windows logo key + I - Open Settings.", MS_WIN)])
Q(T, "File systems", "Intermediate",
  "A branch server loses power in the middle of saving many files. After restart, its NTFS (or Linux ext4) volume "
  "is checked in seconds and its directory structure is consistent, because the file system had first written a "
  "record of each pending change to a special log. What is this file-system feature called?",
  ["Journaling", "Defragmentation", "Compression", "Spooling"],
  concept="Journaling file systems",
  explanation="A journaling file system writes intended metadata changes to a journal (log) before applying them. "
              "After a crash it replays or discards the logged changes instead of scanning the whole disk, so "
              "recovery is fast and the structure stays consistent.",
  steps=["Log changes first, apply later = journaling", "Crash -> replay journal -> consistent volume"],
  wrong="Defragmentation rearranges file pieces for speed. Compression saves space. Spooling queues jobs for slow "
        "devices such as printers.", seconds=25)
Q(T, "Functions", "Intermediate",
  "The controller of a car's airbag, or of an ATM's cash-dispensing mechanism, must always respond to an event "
  "within a fixed, guaranteed time; a late response is treated as a failure. Which type of operating system is "
  "designed for this?",
  ["Real-time operating system (RTOS)", "Batch operating system", "Time-sharing operating system",
   "Network operating system"],
  concept="Types of operating systems",
  explanation="A real-time OS guarantees that tasks are handled within strict deadlines (deterministic timing). "
              "Hard real-time systems such as airbag controllers treat a missed deadline as a failure.",
  steps=["Guaranteed response time = real-time OS"],
  wrong="Batch systems run jobs in groups without interaction. Time-sharing systems share the CPU fairly among "
        "users but do not guarantee deadlines. A network OS manages shared resources across a network.",
  seconds=20)

# ================================================================ 5. Input and Output Devices (1 / 2 / 1)
T = "Input and Output Devices"
Q(T, "Input devices", "Basic",
  "At a shop's counter, a cashier slides an old card through a slot on the side of the POS terminal so that the "
  "black strip on the back of the card is read. Which input device reads this strip?",
  ["Magnetic stripe reader", "Barcode reader", "Optical mark reader", "Biometric scanner"],
  concept="Card readers",
  explanation="The black strip on the back of a card is a magnetic stripe holding the card's data. A magnetic "
              "stripe reader reads it when the card is swiped.",
  steps=["Swiped black strip = magnetic stripe -> magnetic stripe reader"],
  wrong="A barcode reader reads printed bars, an OMR reads pencil marks on forms, and a biometric scanner reads "
        "fingerprints or irises.", seconds=15)
Q(T, "Output devices", "Intermediate",
  "A bank's training centre wants to make physical plastic models of a new branch kiosk design directly from the "
  "computer design file, by building the object layer by layer. Which output device is needed?",
  ["3D printer", "Plotter", "Laser printer", "Projector"],
  concept="Additive manufacturing",
  explanation="A 3D printer builds a solid object by depositing material (e.g. melted plastic) layer upon layer, "
              "following a digital 3D model. This is called additive manufacturing.",
  steps=["Solid object, layer by layer = 3D printer"],
  wrong="A plotter draws large 2D drawings on paper. A laser printer prints flat pages. A projector only shows "
        "images on a screen.", seconds=15)
Q(T, "Output devices", "Intermediate",
  "The interest-rate boards in a bank branch use a display that looks like printed paper, can be read "
  "easily in sunlight, and uses power only when the displayed rates change, keeping the image without power in "
  "between. Which display technology is this?",
  ["Electronic paper (e-ink)", "LCD with backlight", "CRT", "Plasma"],
  concept="Display technologies",
  explanation="E-paper (e-ink) displays move charged pigment particles to form the image. The image stays without "
              "power (bistable), so power is used only for changes; they reflect ambient light like paper and need "
              "no backlight.",
  steps=["Paper-like, readable in sunlight, power only when changed = e-paper"],
  wrong="A backlit LCD, a CRT and a plasma panel all need continuous power to keep showing an image.", seconds=20)
Q(T, "Input devices", "Advanced",
  "A banking app lets users 'twist' the phone quickly to reveal the balance. The app must measure how fast the "
  "phone is rotating about its axes (angular velocity), not just which way gravity points. Which built-in sensor "
  "measures this?",
  ["Gyroscope", "Proximity sensor", "Ambient light sensor", "Magnetometer"],
  concept="Smartphone motion sensors",
  explanation="A gyroscope measures the rate of rotation about the phone's three axes. An accelerometer measures "
              "linear acceleration (including gravity) and is used for portrait/landscape detection; the two are "
              "often combined for motion sensing.",
  steps=["Rate of rotation = gyroscope"],
  wrong="A proximity sensor detects an object near the screen (e.g. the ear). A light sensor measures brightness. "
        "A magnetometer measures the magnetic field to act as a compass.", seconds=25)

# ================================================================ 6. Memory (2 / 3 / 3)
T = "Memory"
Q(T, "Secondary storage", "Basic",
  "Instead of each PC keeping its own copy of shared files, a branch installs a small box with several hard disks "
  "that connects to the office LAN and lets all PCs store and open files over the network. What is this device "
  "called?",
  ["Network Attached Storage (NAS)", "Optical disc drive", "RAM module", "Pen drive"],
  concept="Shared storage on a network",
  explanation="A NAS is a dedicated storage device connected directly to the network. It serves files to many "
              "computers and often uses RAID to protect against a disk failure.",
  steps=["Storage box on the LAN shared by many PCs = NAS"],
  wrong="An optical drive reads discs in one PC. RAM is volatile main memory. A pen drive is portable storage "
        "plugged into one computer at a time.", seconds=15)
Q(T, "Secondary storage", "Basic",
  "A branch must hand over a 3 GB training video on a single optical disc. A CD holds about 700 MB, and a "
  "single-layer DVD holds about 4.7 GB. Which disc should it use?",
  ["A single-layer DVD", "A CD", "Either; both hold 3 GB", "Neither; no optical disc holds 3 GB"],
  concept="Optical disc capacities",
  explanation="3 GB is far more than a CD's 700 MB but fits within a single-layer DVD's 4.7 GB.",
  steps=["3 GB > 0.7 GB (CD)", "3 GB < 4.7 GB (DVD)", "Use a DVD"],
  wrong="A CD is too small. 'Either' ignores the CD's limit. A DVD does hold 3 GB (and Blu-ray holds even more).",
  seconds=15)
S_BACKUP = new_stim(
    "caselet", "Backup schedule of a branch file server",
    "A branch file server holds 200 GB of data. A full backup is taken every Sunday at 23:00. On Monday to "
    "Saturday a backup is taken at 23:00 every night, under one of two plans:\n\n"
    "- Plan X: incremental backups (only data changed since the previous backup of any kind).\n"
    "- Plan Y: differential backups (all data changed since the last full backup).\n\n"
    "New or changed data each day (no data changes twice in the week): "
    + ", ".join(f"{d} {g} GB" for d, g in CHANGES.items()) +
    ".\n\nCopies of every backup are kept on tape in a safe at the bank's disaster-recovery site in another city. "
    "The server's disks fail on Thursday at 15:00.",
    "Plan X restore: Sunday full + Mon, Tue, Wed incrementals (4 sets). Plan Y restore: Sunday full + Wednesday "
    "differential (2 sets). Plan Y daily sizes 6, 10, 20, 25, 33, 36 GB (total 130 GB); Plan X total 36 GB. "
    "Changes after Wednesday 23:00 (16 hours) are lost.")
o, a = ordered(INCR_SETS, [2, 3, 5])
Q(T, "Secondary storage", "Intermediate",
  "Refer to the backup schedule. Under Plan X (incremental), how many backup sets must be restored, at minimum, to "
  "get the server back to its state as of the last backup before the failure?", o, a,
  concept="Restoring incremental backups",
  explanation="Each incremental holds only the changes since the previous backup, so all of them are needed in "
              "order: Sunday's full, then Monday's, Tuesday's and Wednesday's incrementals = 4 sets. (Thursday's "
              "23:00 backup had not run yet.)",
  steps=["Full (Sun)", "+ Mon + Tue + Wed incrementals", "= 4 sets"],
  wrong="2 is the differential answer. 3 forgets one incremental. 5 counts a Thursday backup that never ran.",
  seconds=40, computed=True, stim=S_BACKUP, pos=1)
o, a = ordered(DIFF_SETS, [1, 3, 4])
Q(T, "Secondary storage", "Intermediate",
  "Refer to the backup schedule. Under Plan Y (differential), how many backup sets must be restored, at minimum, "
  "for the same recovery?", o, a,
  concept="Restoring differential backups",
  explanation="A differential holds every change since the last full backup, so only the latest differential is "
              "needed on top of the full backup: Sunday's full + Wednesday's differential = 2 sets.",
  steps=["Full (Sun)", "+ latest differential (Wed)", "= 2 sets"],
  wrong="1 (the full alone) loses Monday-Wednesday changes. 3 and 4 restore unnecessary older differentials, which "
        "the Wednesday differential already contains.", seconds=40, computed=True, stim=S_BACKUP, pos=2)
Q(T, "Secondary storage", "Intermediate",
  "Refer to the backup schedule. Against which risk does keeping the backup tapes at the disaster-recovery site "
  "in another city mainly protect the bank?",
  ["A fire, flood or other disaster that destroys the branch and everything in it",
   "A single disk failing inside the server", "A user opening a file slowly",
   "Data that changed since the last backup"],
  concept="Off-site backups",
  explanation="Backups kept in the same building would be destroyed along with the server in a fire, flood or "
              "theft. An off-site (geographically separate) copy survives a disaster at the main site.",
  steps=["Separate location -> survives a site-wide disaster"],
  wrong="A single disk failure is handled by RAID or any local backup. Slow file access is a performance issue. "
        "Changes made after the last backup are lost wherever the tapes are kept.", seconds=20, stim=S_BACKUP, pos=3)
o, a = ordered(sum(DIFF_SIZES), [36, 66, 200], fmt=lambda v: f"{v} GB")
Q(T, "Secondary storage", "Advanced",
  "Refer to the backup schedule. Ignoring compression, how much backup storage do the six Monday-to-Saturday "
  "backups of one week take in total under Plan Y (differential)?", o, a,
  concept="Size of differential backups",
  explanation="Each differential contains all changes since Sunday, so the sizes grow: Mon 6, Tue 6 + 4 = 10, "
              "Wed 20, Thu 25, Fri 33, Sat 36. Total = 6 + 10 + 20 + 25 + 33 + 36 = 130 GB. Plan X would need only "
              "6 + 4 + 10 + 5 + 8 + 3 = 36 GB.",
  steps=["Running totals: 6, 10, 20, 25, 33, 36", "Sum = 130 GB"],
  shortcut="Differential sizes are the running (cumulative) totals of the daily changes.",
  wrong="36 GB is the incremental total. 200 GB is the size of the full backup. 66 GB has no basis in the "
        "schedule.", seconds=60, computed=True, stim=S_BACKUP, pos=4)
o, a = ordered(LOSS_HOURS, [8, 15, 39], fmt=lambda v: f"{v} hours")
Q(T, "Secondary storage", "Advanced",
  "Refer to the backup schedule. Under either plan, for how long a period of the most recent work may data be "
  "lost because of the failure, since it is in no backup?", o, a,
  concept="Recovery point (data-loss window)",
  explanation="The last backup ran on Wednesday at 23:00. Anything created or changed between then and the "
              "failure on Thursday at 15:00 is not in any backup: 1 hour (to midnight) + 15 hours = 16 hours. To "
              "shrink this window, backups must be taken more often.",
  steps=["Last backup: Wed 23:00", "Failure: Thu 15:00", "1 + 15 = 16 hours"],
  wrong="15 hours forgets the hour before midnight on Wednesday. 39 hours counts from Tuesday's backup. 8 hours "
        "has no basis.", seconds=45, computed=True, stim=S_BACKUP, pos=5)
o, a = ordered(F(82, 10), [F(3, 1), F(16, 10), F(30, 1)], fmt=lambda v: f"About {float(v):g} years")
Q(T, "Cache and units", "Advanced",
  "An SSD for a branch server has an endurance rating of 600 TBW (terabytes written). The server writes about 200 "
  "GB to it every day. Taking 1 TB = 1,000 GB, for about how long can the SSD be written at this rate before it "
  "reaches its rated endurance?", o, a,
  concept="SSD endurance",
  explanation="600 TB = 6,00,000 GB. 6,00,000 / 200 = 3,000 days. 3,000 / 365 = about 8.2 years.",
  steps=["600 TBW = 600,000 GB", "600,000 / 200 GB per day = 3,000 days", "3,000 / 365 = 8.2 years"],
  wrong="3 years treats 3,000 days as 3,000 / 1,000. 1.6 years and 30 years come from misplacing the units.",
  seconds=60, computed=True)

# ================================================================ 7. Internet (5 / 4 / 1)
T = "Internet"
S_MAIL = new_stim(
    "input_output", "Header of an email received by a branch officer",
    "Deepak, a branch officer, opens this email and views its full header:\n\n```\n"
    "From: \"Asha Kulkarni\" <asha.kulkarni@branchmail.bank.example>\n"
    "To: deepak.rao@bank.example\n"
    "Cc: ops-team@bank.example, meena.s@bank.example\n"
    "Reply-To: asha.k.backup@freemail.example\n"
    "Subject: Updated cash-limit sheet\n"
    "Attachment: cash_limits.xlsx\n"
    "Received: from mx2.bank.example by mail.bank.example; Tue, 3 Nov 2026 10:02:11 +0530\n"
    "Received: from smtp.freemail.example by mx2.bank.example; Tue, 3 Nov 2026 10:02:09 +0530\n"
    "Received: from [203.0.113.45] by smtp.freemail.example; Tue, 3 Nov 2026 10:02:05 +0530\n```",
    "Sender domain: branchmail.bank.example. Visible copies (Cc): 2. Replies go to the Reply-To address. Each "
    "server adds its Received line at the top, so the bottom line is the first hop: the message entered at "
    "smtp.freemail.example, not at a bank server.")
Q(T, "Email", "Basic",
  "Refer to the email header. What is the domain part of the sender's (From) address?",
  ["branchmail.bank.example", "asha.kulkarni", "bank.example only because Deepak works there",
   "freemail.example"],
  concept="Parts of an email address",
  explanation="An email address is local-part@domain. In asha.kulkarni@branchmail.bank.example, the local part "
              "(mailbox) is asha.kulkarni and the domain is branchmail.bank.example.",
  steps=["Split at @", "Right side = domain = branchmail.bank.example"],
  wrong="asha.kulkarni is the local part (user name). The receiver's domain does not decide the sender's. "
        "freemail.example appears in the Reply-To, not the From address.", seconds=15, stim=S_MAIL, pos=1)
o, a = ordered(2, [0, 1, 3])
Q(T, "Email", "Basic",
  "Refer to the email header. Apart from Deepak, how many addresses were openly sent a copy of this email?", o, a,
  concept="To and Cc fields",
  explanation="The Cc (carbon copy) field lists ops-team@bank.example and meena.s@bank.example, so 2 other "
              "addresses received a visible copy. (Any Bcc recipients would not appear in the header.)",
  steps=["Cc lists 2 addresses", "Deepak is the only To recipient"],
  wrong="0 ignores the Cc line. 1 counts only one of the two Cc addresses. 3 wrongly counts the Reply-To address, "
        "which is not a recipient.", seconds=20, computed=True, stim=S_MAIL, pos=2)
Q(T, "Email", "Basic",
  "Refer to the email header. Deepak wants to send this same email, together with the attached cash_limits.xlsx, "
  "to his branch manager. Which email option should he use?",
  ["Forward", "Reply", "Reply All", "Move to Junk"],
  concept="Forward vs Reply",
  explanation="Forward sends a copy of a received message, including its attachments, to new recipients that the "
              "user chooses.",
  steps=["Send received mail + attachment to someone new = Forward"],
  wrong="Reply and Reply All answer the existing sender/recipients and usually drop the attachment. Moving to Junk "
        "sends nothing.", seconds=15, stim=S_MAIL, pos=3)
Q(T, "Email", "Intermediate",
  "Refer to the email header. If Deepak clicks Reply (not Reply All), to which address will his email program "
  "normally send the reply?",
  ["asha.k.backup@freemail.example", "asha.kulkarni@branchmail.bank.example", "ops-team@bank.example",
   "deepak.rao@bank.example"],
  concept="The Reply-To header",
  explanation="When a Reply-To field is present, mail programs send replies to that address instead of the From "
              "address. Here a reply would go to a free-mail account outside the bank, a common sign of a phishing "
              "or business-email-compromise attempt.",
  steps=["Reply-To present -> replies go there", "= asha.k.backup@freemail.example"],
  wrong="The From address is used only when there is no Reply-To. ops-team is a Cc recipient (Reply All would "
        "include it). deepak.rao is Deepak's own address.", seconds=30, stim=S_MAIL, pos=4,
  facts=[fact("RFC 5322 3.6.2: When the Reply-To field is present, it indicates the address(es) to which the "
              "author suggests that replies be sent.", RFC5322)])
Q(T, "Protocols", "Advanced",
  "Refer to the email header. Which server first accepted this message from the sender's computer?",
  ["smtp.freemail.example", "mail.bank.example", "mx2.bank.example", "branchmail.bank.example"],
  concept="Reading Received headers",
  explanation="Every SMTP server that handles a message adds its own Received line at the TOP of the header. So "
              "the lines are read from the bottom up: the bottom line shows the first hop, where "
              "smtp.freemail.example received the message from the sender's computer [203.0.113.45]. It then "
              "went to mx2 and finally mail.bank.example. No branchmail.bank.example server appears at all, even "
              "though the From address claims that domain.",
  steps=["Newest Received line is on top", "Read bottom-up", "First hop: smtp.freemail.example"],
  wrong="mail.bank.example is the last (delivering) server and mx2 the middle hop. branchmail.bank.example is only "
        "written in the From line; no server of that name handled the message.", seconds=45, stim=S_MAIL, pos=5,
  facts=[fact("RFC 5321 4.4: when an SMTP server receives a message it MUST insert trace (Received) information at "
              "the beginning of the message content.", RFC5321)])
Q(T, "Web basics", "Basic",
  "A clerk wants a search engine to show only pages that contain the exact phrase fixed deposit rates, with the "
  "words together and in that order. How should she type the search?",
  ["\"fixed deposit rates\" (inside double quotation marks)", "fixed-deposit-rates?", "fixed OR deposit OR rates",
   "#fixeddepositrates"],
  concept="Search operators",
  explanation="Putting words inside double quotation marks tells a search engine to match that exact phrase, with "
              "the words together and in that order.",
  steps=["Exact phrase = put it in quotes"],
  wrong="Hyphens and a question mark do not force an exact phrase. OR finds pages with any one of the words. A "
        "hashtag searches tagged social-media posts.", seconds=15)
Q(T, "Email", "Basic",
  "On a training trip, an officer reads and sends her office email by opening a web browser on a hotel computer "
  "and logging in to the bank's mail website, without installing any email program. What is this way of using "
  "email called?",
  ["Webmail", "POP3 download", "Newsgroup", "FTP"],
  concept="Ways to access email",
  explanation="Webmail is email accessed through a web browser; the messages stay on the mail server and no email "
              "client program needs to be installed.",
  steps=["Email through a browser = webmail"],
  wrong="POP3 is used by an email client to download mail. Newsgroups are discussion forums. FTP transfers files.",
  seconds=15)
Q(T, "Protocols", "Intermediate",
  "A clerk is correctly logged in to the bank's intranet, but when she opens the salary-revision page meant only "
  "for HR staff, the server replies with HTTP status code 403. What does this mean?",
  ["The server understood the request but refuses it, because she lacks permission for that page",
   "The page does not exist on the server", "The server has crashed with an internal error",
   "The page has moved permanently to a new address"],
  concept="HTTP status codes",
  explanation="403 Forbidden means the server identified the request but will not allow it, typically because the "
              "user does not have the required permission. Logging in again does not help, unlike 401 "
              "Unauthorized, which asks for valid credentials.",
  steps=["403 = Forbidden = no permission"],
  wrong="'Does not exist' is 404. An internal server error is 500. Moved permanently is 301.", seconds=20,
  facts=[fact("MDN: 403 Forbidden indicates that the server understood the request but refused to process it; "
              "unlike 401, re-authenticating makes no difference.", MDN_403)])
o, a = ordered(587, [21, 110, 443])
Q(T, "Protocols", "Intermediate",
  "A bank's email program hands each outgoing message to the bank's mail server using the standard 'message "
  "submission' service, on which the user must authenticate. Which TCP port is reserved for this service?", o, a,
  concept="Email ports",
  explanation="Port 587 is reserved for message submission (an email client submitting mail to its own server, "
              "usually with authentication). Port 25 is used for relaying between mail servers.",
  steps=["Client -> own server submission = port 587"],
  wrong="21 is FTP control, 110 is POP3 and 443 is HTTPS.", seconds=20,
  facts=[fact("RFC 6409 3.1: Port 587 is reserved for email message submission.", RFC6409)])
Q(T, "Web basics", "Intermediate",
  "A customer reads a news site that shows an advertising company's banner. The banner sets a cookie belonging to "
  "the advertising company's domain, and the same company's banners on many other sites read that cookie to build "
  "a profile of her browsing. What is such a cookie called?",
  ["Third-party (cross-site) cookie", "Session cookie of the news site", "HttpOnly cookie", "Cache file"],
  concept="First-party and third-party cookies",
  explanation="A cookie set by a domain other than the site in the address bar is a third-party (cross-site) "
              "cookie. Ad and tracking companies use them across many sites to follow users and build profiles.",
  steps=["Cookie from a different domain than the site visited = third-party cookie"],
  wrong="A first-party session cookie belongs to the news site itself. HttpOnly only blocks JavaScript access to a "
        "cookie. The cache stores copies of pages and images, not tracking identifiers.", seconds=25,
  facts=[fact("MDN: if the domain and scheme are different, the cookie is not from the same site and is a "
              "third-party cookie; third-party servers can combine them across sites to profile a user.",
              MDN_3PC)])

# ================================================================ 8. Networking (1 / 4 / 2)
T = "Networking"
Q(T, "Devices", "Basic",
  "A branch installs CCTV cameras on the ceiling where there are no power sockets. Each camera gets both its data "
  "connection and its electrical power through a single Ethernet cable from a special switch. What is this "
  "technology called?",
  ["Power over Ethernet (PoE)", "Wi-Fi", "Bluetooth", "Fibre optics"],
  concept="Power over Ethernet",
  explanation="PoE switches send DC power along the same twisted-pair Ethernet cable that carries data, so devices "
              "such as IP cameras, access points and IP phones need no separate power supply.",
  steps=["Data + power on one Ethernet cable = PoE"],
  wrong="Wi-Fi and Bluetooth are wireless and carry no power. Fibre carries light, not electrical power.",
  seconds=15)
S_NET = new_stim(
    "caselet", "Branch network configuration",
    "Branch router R1 has its LAN interface at 10.20.30.1/26; this is the default gateway for all branch PCs. A "
    "DHCP service on R1 leases addresses from this LAN. The DNS server is 10.20.0.53 at head office. R1 reaches "
    "head office over an IPsec site-to-site VPN tunnel across the internet.\n\nR1 routing table:\n\n"
    "| Destination | Next hop / interface |\n|---|---|\n"
    + "\n".join(f"| {n} | {h} |" for n, h in ROUTES.items()) +
    "\n\nBranch PCs (address/prefix, gateway):\n\n| PC | Address | Gateway |\n|---|---|---|\n"
    "| PC1 | 10.20.30.25/26 | 10.20.30.1 |\n| PC2 | 10.20.30.70/26 | 10.20.30.1 |\n"
    "| PC3 | 169.254.18.7/16 | (none) |\n| PC4 | 10.20.30.31/26 | 10.20.30.1 |",
    "LAN 10.20.30.0/26 = 10.20.30.0-10.20.30.63 (broadcast .63). PC2 (10.20.30.70) is in 10.20.30.64/26, outside "
    "the gateway's subnet. PC3 has a self-assigned link-local address (no DHCP lease). 10.20.7.9 matches /16, /8 "
    "and /0; the longest, /16, wins.")
Q(T, "OSI and TCP/IP", "Intermediate",
  "Refer to the branch network. PC2 cannot reach its gateway or anything outside the branch. What is the cause?",
  ["Its address 10.20.30.70/26 lies in subnet 10.20.30.64/26, not in the gateway's subnet 10.20.30.0/26",
   "Its gateway address 10.20.30.1 is a broadcast address", "Its address is a private address that cannot be used "
   "on a LAN", "A /26 prefix allows only 26 hosts, and they are all in use"],
  concept="Host and gateway in the same subnet",
  explanation="A /26 block has 64 addresses, so 10.20.30.0/26 covers .0 to .63 and the next block is .64 to .127. "
              "PC2's address .70 is in 10.20.30.64/26, while the gateway .1 is in 10.20.30.0/26. The PC thinks the "
              "gateway is on another network that it cannot reach directly, so it cannot use it.",
  steps=["/26 -> blocks of 64: .0-.63, .64-.127", "PC2 .70 -> 10.20.30.64/26", "Gateway .1 -> 10.20.30.0/26 -> "
                                                                                "mismatch"],
  wrong="10.20.30.1 is a usable host address (the broadcast is .63). Private addresses are meant for LANs. A /26 "
        "gives 62 usable hosts, not 26.", seconds=60, computed=True, stim=S_NET, pos=1)
Q(T, "OSI and TCP/IP", "Intermediate",
  "Refer to the branch network. PC3 shows the address 169.254.18.7. What does this most likely indicate?",
  ["PC3 could not get an address from the DHCP service, so it assigned itself a link-local address",
   "PC3 has been given a public internet address by the ISP", "PC3 is the branch's DNS server",
   "PC3 is correctly configured for head-office access"],
  concept="Link-local (APIPA) addresses",
  explanation="Addresses in 169.254.0.0/16 are IPv4 link-local addresses. A computer set to obtain an address "
              "automatically picks one when no DHCP server answers (Windows calls this APIPA). It can talk only "
              "to devices on the same link, not through a gateway. Check the cable, the switch port and the DHCP "
              "service.",
  steps=["169.254.x.x = link-local, self-assigned", "Means: no DHCP lease", "No gateway, so no access beyond the "
                                                                             "LAN"],
  wrong="169.254.0.0/16 is not a public address. The DNS server is 10.20.0.53. Link-local addresses cannot be "
        "routed, so it cannot reach head office.", seconds=30, stim=S_NET, pos=2,
  facts=[fact("RFC 3927: IPv4 link-local addresses use the prefix 169.254/16; hosts pick an address from "
              "169.254.1.0 to 169.254.254.255.", RFC3927)])
Q(T, "OSI and TCP/IP", "Intermediate",
  "Refer to the branch network. From PC4, the clerk can open the head-office portal by typing its IP address, "
  "http://10.20.0.80, but typing portal.bank.example gives 'server not found'. Which service is most likely "
  "failing?",
  ["DNS (name resolution)", "The default gateway", "The PC's network cable", "DHCP"],
  concept="Troubleshooting by layers",
  explanation="Reaching 10.20.0.80 by its address proves that the cable, the IP settings, the gateway and the "
              "route to head office all work. Only the step that turns the name into an address fails: DNS, "
              "served by 10.20.0.53.",
  steps=["By IP: works -> cable, gateway, routing OK", "By name: fails -> name-to-address step", "= DNS"],
  wrong="If the gateway or cable were faulty, the IP address would not open either. PC4 already has a valid "
        "address, so DHCP is not the issue.", seconds=30, stim=S_NET, pos=3)
Q(T, "OSI and TCP/IP", "Intermediate",
  "Refer to the branch network. The branch's traffic to head office is protected by an IPsec VPN tunnel. At which "
  "OSI layer does IPsec provide its protection?",
  ["Network layer", "Data link layer", "Transport layer", "Application layer"],
  concept="Where security protocols work",
  explanation="IPsec protects IP packets themselves: it authenticates and encrypts traffic at the IP (network) "
              "layer, so all applications above benefit without changes. TLS, by contrast, sits above the "
              "transport layer.",
  steps=["IPsec = security for IP packets = network layer"],
  wrong="Data link security (e.g. Wi-Fi WPA) protects one link only. TLS works above TCP for individual "
        "applications. Application-layer security is built into a particular program.", seconds=20, stim=S_NET,
  pos=4, facts=[fact("RFC 4301 3.1: IPsec security services are offered at the IP layer.", RFC4301)])
o = ["10.20.30.63", "10.20.30.64", "10.20.30.255", "10.20.30.62"]
Q(T, "OSI and TCP/IP", "Advanced",
  "Refer to the branch network. A packet is sent to the broadcast address of the branch LAN (10.20.30.0/26), so "
  "that every host on it receives it. What is that address?", o,
  concept="Broadcast address of a subnet",
  explanation="A /26 leaves 32 - 26 = 6 host bits, i.e. 64 addresses: 10.20.30.0 to 10.20.30.63. The first is the "
              "network address and the last, 10.20.30.63, is the broadcast address.",
  steps=["Host bits = 6 -> 64 addresses", "Range .0-.63", "Broadcast = last = 10.20.30.63"],
  shortcut="Broadcast = network address + block size - 1 = 0 + 64 - 1.",
  wrong="10.20.30.64 is the network address of the next subnet. 10.20.30.255 would be the broadcast of a /24. "
        "10.20.30.62 is the last usable host.", seconds=45, computed=True, stim=S_NET, pos=5)
o = list(ROUTES.values())
assert o[0] == lpm("10.20.7.9")
Q(T, "Devices", "Advanced",
  "Refer to the branch network. R1 receives a packet for 10.20.7.9. Which entry of its routing table does it use "
  "to forward the packet?", o,
  concept="Longest prefix match",
  explanation="10.20.7.9 matches three entries: 10.20.0.0/16, 10.0.0.0/8 and the default 0.0.0.0/0 (it is not in "
              "10.20.30.0/26, which covers only 10.20.30.0-63). A router always chooses the most specific match, "
              "the longest prefix: /16, so the packet goes through the tunnel to head office.",
  steps=["Matches: /16, /8, /0", "Longest prefix = /16", "-> Tunnel to head office"],
  wrong="The LAN route does not match 10.20.7.9. The MPLS (/8) and default (/0) routes also match but are less "
        "specific than /16.", seconds=50, computed=True, stim=S_NET, pos=6)

# ================================================================ 9. Cybersecurity (4 / 2 / 6)
T = "Cybersecurity"
S_INC = new_stim(
    "caselet", "Incident timeline at a bank",
    "The bank's security operations centre (SOC) reconstructs this incident:\n\n"
    "- Day 1, 09:12 - A clerk at Branch 14 receives an email with the attachment Revised_TDS_Rates.docm, opens it "
    "and clicks 'Enable Content' when Word asks.\n"
    "- Day 1, 09:13 onwards - The clerk's PC sends a small HTTPS request to an unknown server abroad every 60 "
    "seconds and receives short instructions in reply.\n"
    "- Day 2 - Using an administrator password stored on the clerk's PC, the attacker logs in to the branch file "
    "server and from there to the head-office HR server.\n"
    "- Day 3, 02:00 - 4 GB of HR records are compressed and uploaded to a cloud-storage account controlled by "
    "the attacker.\n"
    "- Day 3, 11:00 - The SOC computes the SHA-256 hash of the payroll master file and finds it different from "
    "the hash recorded at last week's audit, although no authorised change was made.",
    "Macro malware (initial access) -> command-and-control beaconing -> lateral movement -> exfiltration; the "
    "changed hash shows that the payroll file's integrity has been violated.")
Q(T, "Malware", "Basic",
  "Refer to the incident timeline. Clicking 'Enable Content' in the .docm file allowed what to run on the clerk's "
  "PC?",
  ["Macros (small programs embedded in the document)", "A printer driver", "The PC's BIOS update",
   "A Windows system restore"],
  concept="Macro malware",
  explanation="A .docm file is a Word document that can contain macros. Word disables them by default; 'Enable "
              "Content' lets them run, and a malicious macro can then download or run malware. Office files from "
              "unknown senders should never have macros enabled.",
  steps=[".docm = macro-enabled document", "Enable Content -> macros run -> malware"],
  wrong="The click does not install drivers, update the BIOS or restore Windows; it only lets the document's "
        "embedded code run.", seconds=20, stim=S_INC, pos=1)
Q(T, "Malware", "Intermediate",
  "Refer to the incident timeline. The PC's regular 60-second requests to a server abroad, which sends back "
  "instructions, are typical of which malware activity?",
  ["Command-and-control (C2) beaconing", "Disk defragmentation", "A software licence check",
   "A denial-of-service attack on the bank"],
  concept="Command and control",
  explanation="After infection, malware 'beacons' to the attacker's command-and-control server at regular "
              "intervals to receive commands. Using HTTPS and small messages helps it blend into normal web "
              "traffic.",
  steps=["Regular check-ins + instructions received = C2 beaconing"],
  wrong="Defragmentation is a local disk task. A licence check does not take instructions from an unknown server "
        "every minute. One PC's small requests are not a flood of traffic (DoS).", seconds=25, stim=S_INC, pos=2,
  facts=[fact("MITRE ATT&CK TA0011 Command and Control: the adversary is trying to communicate with compromised "
              "systems to control them.", MITRE_C2)])
Q(T, "Encryption and authentication", "Intermediate",
  "Refer to the incident timeline. On Day 3 the payroll file's SHA-256 hash no longer matches last week's value. "
  "Which security property does this show has been violated?",
  ["Integrity: the file has been altered", "Availability: the file cannot be opened",
   "Confidentiality: the file has been read by an outsider", "Non-repudiation: the sender denies sending it"],
  concept="Hashes and integrity",
  explanation="A cryptographic hash changes completely if even one bit of the file changes. A different hash with "
              "no authorised change means the file has been modified: its integrity is lost.",
  steps=["Hash differs -> content changed", "Unauthorised change = integrity violation"],
  wrong="A hash says nothing about whether the file can be opened or who read it. Non-repudiation concerns a "
        "signer denying an action.", seconds=25, stim=S_INC, pos=3)
Q(T, "Malware", "Advanced",
  "Refer to the incident timeline. In the MITRE ATT&CK framework, which tactic describes the Day 2 activity, where "
  "the attacker uses stolen credentials to go from the clerk's PC to the file server and then to the HR server?",
  ["Lateral Movement", "Initial Access", "Exfiltration", "Reconnaissance"],
  concept="Attack life cycle (MITRE ATT&CK tactics)",
  explanation="Lateral Movement is the attacker moving through the environment from the first compromised system "
              "to others, often with stolen credentials, to reach valuable targets.",
  steps=["Moving from one internal system to another = Lateral Movement"],
  wrong="Initial Access was the Day 1 email. Exfiltration is the Day 3 upload. Reconnaissance is gathering "
        "information before the attack.", seconds=30, stim=S_INC, pos=4,
  facts=[fact("MITRE ATT&CK TA0008 Lateral Movement: the adversary is trying to move through your environment.",
              MITRE_LM)])
Q(T, "Malware", "Advanced",
  "Refer to the incident timeline. Which MITRE ATT&CK tactic describes the Day 3, 02:00 event?",
  ["Exfiltration", "Lateral Movement", "Persistence", "Privilege Escalation"],
  concept="Attack life cycle (MITRE ATT&CK tactics)",
  explanation="Compressing data and uploading it to an attacker-controlled cloud account is stealing data out of "
              "the network: the Exfiltration tactic. Its impact is a breach of confidentiality.",
  steps=["Data sent out to attacker = Exfiltration"],
  wrong="Lateral Movement was Day 2. Persistence keeps access across reboots. Privilege Escalation gains higher "
        "rights; neither describes sending data out.", seconds=25, stim=S_INC, pos=5,
  facts=[fact("MITRE ATT&CK TA0010 Exfiltration: the adversary is trying to steal data.", MITRE_EX)])
S_BIO = new_stim(
    "data_table", "Test report of a fingerprint login system",
    f"A bank tests a fingerprint login system with {GENUINE:,} genuine attempts (real users) and {IMPOSTOR:,} "
    "impostor attempts (other people's fingers), at three matching thresholds:\n\n"
    "| Threshold | Genuine attempts rejected | Impostor attempts accepted |\n|---|---|---|\n"
    + "\n".join(f"| {k} | {fr} | {fa} |" for k, (fr, fa) in BIO.items()) +
    "\n\nFalse Acceptance Rate (FAR) = impostor attempts accepted / impostor attempts. False Rejection Rate (FRR) = "
    "genuine attempts rejected / genuine attempts.",
    "FAR: Low 3%, Medium 0.5%, High 0.1%. FRR: Low 1%, Medium 3%, High 9%. A stricter threshold lowers FAR and "
    "raises FRR.")
o, a = ordered(F(5, 10), [F(25, 100), F(125, 100), F(3, 1)], fmt=lambda v: f"{float(v):g}%")
Q(T, "Encryption and authentication", "Advanced",
  "Refer to the fingerprint test report. What is the False Acceptance Rate (FAR) at the Medium threshold?", o, a,
  concept="False Acceptance Rate",
  explanation="FAR = 25 / 5,000 = 0.005 = 0.5%. It is the share of impostor attempts that were wrongly accepted.",
  steps=["Impostors accepted at Medium = 25", "25 / 5,000 = 0.005", "= 0.5%"],
  wrong="1.25% divides 25 by 2,000 (genuine attempts). 3% is the FRR at Medium (and the FAR at Low). 0.25% "
        "halves the correct value.", seconds=45, computed=True, stim=S_BIO, pos=1)
o, a = ordered(F(9, 1), [F(36, 10), F(3, 1), F(1, 10)], fmt=lambda v: f"{float(v):g}%")
Q(T, "Encryption and authentication", "Advanced",
  "Refer to the fingerprint test report. What is the False Rejection Rate (FRR) at the High threshold?", o, a,
  concept="False Rejection Rate",
  explanation="FRR = 180 / 2,000 = 0.09 = 9%. Nine in every hundred genuine customers would be wrongly refused and "
              "have to try again.",
  steps=["Genuine rejected at High = 180", "180 / 2,000 = 0.09", "= 9%"],
  wrong="3.6% divides 180 by 5,000 (impostor attempts). 0.1% is the FAR at High. 3% is the FRR at Medium.",
  seconds=45, computed=True, stim=S_BIO, pos=2)
Q(T, "Encryption and authentication", "Advanced",
  "Refer to the fingerprint test report. For approving high-value fund transfers, the bank's top priority is that "
  "an impostor is almost never accepted, even if genuine users must sometimes retry. Which threshold fits best, "
  "and what is the trade-off?",
  ["High: lowest FAR (0.1%), but the highest FRR (9%)", "Low: lowest FRR (1%), and also the lowest FAR",
   "Medium: it has the lowest FAR of the three", "Any threshold, because FAR and FRR do not depend on the "
   "threshold"],
  concept="FAR-FRR trade-off",
  explanation="FAR: Low 150/5,000 = 3%, Medium 0.5%, High 5/5,000 = 0.1%. FRR: Low 1%, Medium 3%, High 9%. A "
              "stricter threshold accepts fewer impostors but rejects more genuine users. To minimise wrong "
              "acceptance, choose High and accept more retries.",
  steps=["FAR: 3%, 0.5%, 0.1%", "FRR: 1%, 3%, 9%", "Minimise FAR -> High; cost: FRR 9%"],
  wrong="Low has the HIGHEST FAR (3%). Medium's FAR (0.5%) is above High's. The table shows both rates change "
        "with the threshold.", seconds=60, computed=True, stim=S_BIO, pos=3)
o, a = ordered(3844, [2, 62, 124], fmt=lambda v: f"{v:,} times")
Q(T, "Encryption and authentication", "Advanced",
  "Passwords for a bank's internal portal use characters from a set of 62 (A-Z, a-z, 0-9). The minimum length is "
  "raised from 8 to 10 characters. For an attacker trying every possible password, by what factor does the "
  "number of possible 10-character passwords exceed the number of 8-character ones?", o, a,
  concept="Password key space",
  explanation="The number of passwords of length n from 62 symbols is 62^n. 62^10 / 62^8 = 62^2 = 3,844. Each extra "
              "character multiplies the brute-force effort by 62.",
  steps=["8 chars: 62^8", "10 chars: 62^10", "Ratio = 62^2 = 3,844"],
  wrong="2 counts only the extra characters. 62 is the factor for one extra character. 124 adds instead of "
        "multiplying (62 x 2).", seconds=45, computed=True)
Q(T, "Encryption and authentication", "Basic",
  "A bank gives tellers access only to the screens and data they need for their counter work; they cannot open "
  "the loan-approval or HR systems. Which security principle is this?",
  ["Principle of least privilege", "Security through obscurity", "Single sign-on", "Open access"],
  concept="Access control principles",
  explanation="Least privilege means each user or program gets only the minimum access needed for its job. It "
              "limits mistakes and the damage an attacker can do with a stolen account.",
  steps=["Only the access needed for the job = least privilege"],
  wrong="Security through obscurity relies on hiding how a system works. Single sign-on lets one login open many "
        "systems; it does not restrict access. Open access is the opposite of the scenario.", seconds=15)
Q(T, "Phishing and social engineering", "Basic",
  "An email shows the sender name 'SBI Customer Care', but when the customer looks closely, the actual address is "
  "care.sbi.verify@mailbox-free.example. What should she conclude?",
  ["The email is likely a phishing attempt, because the real sending address is not the bank's domain",
   "The email is genuine, because the sender name says SBI Customer Care",
   "The email is safe as long as it has no spelling mistakes", "The email is genuine because 'sbi' appears in "
   "the address"],
  concept="Spotting phishing emails",
  explanation="The display name can be set to anything. What matters is the domain of the actual address. A free "
              "mail domain pretending to be a bank is a classic phishing sign; the customer should not click links "
              "and should report it.",
  steps=["Ignore display name", "Check the domain after @", "Not the bank's domain -> suspect phishing"],
  wrong="Display names and words like 'sbi' inside the local part are easy to fake. Good spelling does not prove "
        "an email is genuine.", seconds=20)
Q(T, "Encryption and authentication", "Basic",
  "A loan officer's laptop is stolen from a train. The bank is not worried about customer data, because the whole "
  "disk was protected with BitLocker and cannot be read without the key. What protected the data?",
  ["Full-disk encryption of data at rest", "A firewall", "Antivirus software", "A strong Wi-Fi password"],
  concept="Encryption of data at rest",
  explanation="Full-disk encryption (BitLocker on Windows) encrypts everything stored on the drive. Without the "
              "key or password, a thief who removes the disk sees only ciphertext.",
  steps=["Stolen device + unreadable disk = full-disk encryption"],
  wrong="A firewall filters network traffic, antivirus detects malware and a Wi-Fi password protects the wireless "
        "network; none of them stops someone reading a stolen disk.", seconds=15)

# ================================================================ 10. Database Fundamentals (2 / 4 / 1)
T = "Database Fundamentals"
S_SQL = new_stim(
    "data_table", "Customers and Accounts tables",
    "Table **Customers** (cust_id is the primary key):\n\n| cust_id | name | city |\n|---|---|---|\n"
    + "\n".join(f"| {i} | {n} | {c} |" for i, n, c in CUST) +
    "\n\nTable **Accounts** (acc_no is the primary key; cust_id is a foreign key referencing Customers.cust_id; "
    "balance in Rs):\n\n| acc_no | cust_id | type | balance | nominee |\n|---|---|---|---|---|\n"
    + "\n".join(f"| {a_} | {c} | {t} | {b} | {n or 'NULL'} |" for a_, c, t, b, n in ACC),
    "Kiran (6) has no account. Customers 1 and 4 hold 2 and 3 accounts. Nominee is NULL in 3 rows. Average "
    "balance = 5,95,000 / 8 = 74,375; accounts above it belong to customers 1, 3 and 4.")
o = [", ".join(SQL_IN), "Asha, John", "Asha, John, Kiran, Meena", "Kiran"]
Q(T, "SQL basics", "Basic",
  "Refer to the tables. Which names does this query return?\nSELECT name FROM Customers WHERE city IN ('Pune', "
  "'Agra');", o,
  concept="The IN operator",
  explanation="city IN ('Pune', 'Agra') is true when city equals any value in the list. Pune: Asha, John; Agra: "
              "Kiran.",
  steps=["Pune -> Asha, John", "Agra -> Kiran"],
  wrong="'Asha, John' misses Agra. Meena lives in Nagpur. 'Kiran' alone misses Pune.", seconds=30, computed=True,
  stim=S_SQL, pos=1)
o = ["Kiran", "Meena", "Ravi and Kiran", "No name (empty result)"]
Q(T, "SQL basics", "Intermediate",
  "Refer to the tables. What does this query return?\nSELECT c.name FROM Customers c LEFT JOIN Accounts a ON "
  "c.cust_id = a.cust_id WHERE a.acc_no IS NULL;", o,
  concept="LEFT JOIN to find unmatched rows",
  explanation="A LEFT JOIN keeps every customer. Customers with no matching account get NULL in all Accounts "
              "columns. WHERE a.acc_no IS NULL keeps only these rows: Kiran (cust_id 6) has no account.",
  steps=["LEFT JOIN keeps all customers", "No match -> account columns NULL", "Only Kiran -> 'Kiran'"],
  wrong="Meena and Ravi each have one account. An INNER JOIN would give no row for Kiran, but this is a LEFT JOIN.",
  seconds=50, computed=True, stim=S_SQL, pos=2)
o, a = ordered(len(SQL_HAV), [1, 3, 5])
Q(T, "SQL basics", "Intermediate",
  "Refer to the tables. How many rows does this query return?\nSELECT cust_id, COUNT(*) FROM Accounts GROUP BY "
  "cust_id HAVING COUNT(*) >= 2;", o, a,
  concept="GROUP BY with HAVING",
  explanation="Accounts per customer: 1 -> 2, 2 -> 1, 3 -> 1, 4 -> 3, 5 -> 1. HAVING keeps groups with at least 2 "
              "rows: customers 1 and 4. Result: 2 rows.",
  steps=["Group counts: 2, 1, 1, 3, 1", "Keep >= 2: customers 1 and 4", "2 rows"],
  wrong="5 is the number of groups before HAVING. 1 keeps only customer 4 (as if > 2). 3 is customer 4's count, "
        "not a row count.", seconds=50, computed=True, stim=S_SQL, pos=3)
o = ["8 and 5", "8 and 8", "5 and 5", "8 and 4"]
Q(T, "SQL basics", "Intermediate",
  "Refer to the tables. What two values does this query return?\nSELECT COUNT(*), COUNT(nominee) FROM Accounts;",
  o,
  concept="COUNT(*) vs COUNT(column)",
  explanation="COUNT(*) counts all rows: 8. COUNT(nominee) counts only rows where nominee is not NULL: 8 - 3 (A102, "
              "A104, A107) = 5.",
  steps=["COUNT(*) = 8", "NULL nominees: 3", "COUNT(nominee) = 5"],
  wrong="8 and 8 assumes COUNT(column) counts NULLs. 5 and 5 assumes COUNT(*) skips them too. 8 and 4 is "
        "COUNT(DISTINCT nominee), since Anil appears twice.", seconds=40, computed=True, stim=S_SQL, pos=4)
Q(T, "Keys", "Intermediate",
  "Refer to the tables. The database enforces the foreign key on Accounts.cust_id. Which of these INSERT "
  "statements will the database REJECT?",
  ["INSERT INTO Accounts VALUES ('A111', 7, 'SB', 5000, NULL);",
   "INSERT INTO Accounts VALUES ('A109', 6, 'SB', 5000, NULL);",
   "INSERT INTO Accounts VALUES ('A110', 2, 'FD', 75000, 'Sita');",
   "INSERT INTO Accounts VALUES ('A112', 1, 'CA', 20000, NULL);"],
  concept="Referential integrity",
  explanation="A foreign key value must match an existing primary-key value in the referenced table (or be NULL). "
              "There is no customer with cust_id 7, so the row for A111 would refer to a non-existent customer and "
              "is rejected. Customers 6, 2 and 1 exist, and the new account numbers are unique.",
  steps=["Check cust_id against Customers: 7 does not exist", "-> referential-integrity violation"],
  wrong="cust_id 6 (Kiran), 2 (Ravi) and 1 (Asha) exist, and A109, A110 and A112 are new primary-key values; a "
        "NULL nominee is allowed.", seconds=40, computed=True, stim=S_SQL, pos=5)
o = [", ".join(SQL_SUB), "Asha, John", "Asha, Meena, John, Farah", "Asha, Ravi, Meena, John, Farah"]
Q(T, "SQL basics", "Advanced",
  "Refer to the tables. Which names does this query return?\nSELECT name FROM Customers WHERE cust_id IN (SELECT "
  "cust_id FROM Accounts WHERE balance > (SELECT AVG(balance) FROM Accounts));", o,
  concept="Nested subqueries",
  explanation="Innermost: AVG(balance) = (45,000 + 2,00,000 + 12,000 + 90,000 + 30,000 + 1,50,000 + 8,000 + "
              "60,000) / 8 = 5,95,000 / 8 = 74,375. Accounts above it: A102 (cust 1), A104 (cust 3), A106 (cust "
              "4). Names: Asha, Meena, John.",
  steps=["AVG = 74,375", "Balances above: A102, A104, A106 -> cust 1, 3, 4", "Names: Asha, Meena, John"],
  wrong="'Asha, John' leaves out Meena's 90,000. Farah's 60,000 is below the average. The last option lists every "
        "customer who holds any account.", seconds=75, computed=True, stim=S_SQL, pos=6)
Q(T, "DBMS concepts", "Basic",
  "A bank wants tellers to see each customer's name, account number and balance, but not the customer's PAN or "
  "income stored in the same tables. The DBA creates a saved query that tellers use like a table, showing only the "
  "allowed columns, without storing a second copy of the data. What is this called?",
  ["View", "Index", "Trigger", "Backup"],
  concept="Views",
  explanation="A view is a virtual table defined by a stored query. It shows selected rows and columns from base "
              "tables, is used like a table, and is a common way to restrict what users can see.",
  steps=["Virtual table from a saved query = view"],
  wrong="An index speeds up searches. A trigger runs code automatically when data changes. A backup is a copy of "
        "the data for recovery.", seconds=20)

# ================================================================ 11. MS Office (4 / 3 / 3)
T = "MS Office"
S_XL = new_stim(
    "data_table", "Excel sheet of loan applications",
    "An Excel sheet lists loan applications (row 1 has headings; column E is empty where no remark was "
    "entered):\n\n| Row | A (Officer) | B (Branch) | C (Product) | D (Amount, Rs lakh) | E (Remarks) |\n"
    "|---|---|---|---|---|---|\n"
    + "\n".join(f"| {i + 2} | {o_} | {b} | {p} | {d} | {r} |" for i, (o_, b, p, d, r) in enumerate(SHEET)),
    "Amounts sorted descending: 50, 42, 35, 28, 12, 10, 8, 3. Blank remarks: 4. Pune Home loans: 42 + 28 = 70. "
    "Median = (12 + 28) / 2 = 20.")
Q(T, "MS Excel", "Basic",
  "Refer to the Excel sheet. The rows 2 to 9 are sorted by column D from largest to smallest (descending). "
  "Whose name will then be in cell A4?",
  ["John", "Asha", "Kiran", "Farah"],
  concept="Sorting data",
  explanation="Descending order of amounts: 50 (Kiran) in row 2, 42 (Asha) in row 3, 35 (John) in row 4, then 28 "
              "(Farah) and so on.",
  steps=["Largest first: 50, 42, 35, ...", "Row 4 = third data row = 35 = John"],
  wrong="Kiran is in row 2 and Asha in row 3. Farah would be in row 5.", seconds=30, computed=True, stim=S_XL,
  pos=1)
o, a = ordered(4, [0, 3, 8])
Q(T, "MS Excel", "Basic",
  "Refer to the Excel sheet. What does =COUNTBLANK(E2:E9) return?", o, a,
  concept="COUNTBLANK",
  explanation="COUNTBLANK counts the empty cells in a range. Remarks are empty for Ravi, John, Kiran and Neha: 4 "
              "cells.",
  steps=["Empty E cells: rows 3, 5, 7, 9", "Count = 4"],
  wrong="3 misses one empty cell. 8 counts every cell. 0 would mean no cell is empty.", seconds=25, computed=True,
  stim=S_XL, pos=2)
o, a = ordered(SUMIFS, [42, 85, 155])
Q(T, "MS Excel", "Intermediate",
  "Refer to the Excel sheet. What does =SUMIFS(D2:D9, B2:B9, \"Pune\", C2:C9, \"Home\") return?", o, a,
  concept="SUMIFS with two criteria",
  explanation="SUMIFS adds the values of D where ALL conditions hold: branch Pune AND product Home. Asha (42) and "
              "Farah (28) qualify: 42 + 28 = 70.",
  steps=["Pune and Home: Asha 42, Farah 28", "Sum = 70"],
  wrong="85 adds every Pune loan. 155 adds every Home loan. 42 takes only the first match.", seconds=40,
  computed=True, stim=S_XL, pos=3)
o, a = ordered(MED, [F(47, 2), 12, 28], fmt=lambda v: f"{float(v):g}")
Q(T, "MS Excel", "Advanced",
  "Refer to the Excel sheet. What does =MEDIAN(D2:D9) return?", o, a,
  concept="MEDIAN with an even number of values",
  explanation="Sorted values: 3, 8, 10, 12, 28, 35, 42, 50. With 8 values (an even number) the median is the "
              "average of the 4th and 5th values: (12 + 28) / 2 = 20.",
  steps=["Sort: 3, 8, 10, 12, 28, 35, 42, 50", "Middle two: 12 and 28", "(12 + 28) / 2 = 20"],
  wrong="12 and 28 are just one of the two middle values. 23.5 is the mean (188 / 8).", seconds=45, computed=True,
  stim=S_XL, pos=4)
Q(T, "MS Word", "Basic",
  "A draft loan policy circulated in MS Word must show the word DRAFT in large, faint, diagonal letters behind the "
  "text of every page. Which Word feature does this?",
  ["Watermark", "Footnote", "Drop Cap", "WordArt in the header only"],
  concept="Watermarks",
  explanation="Design > Watermark places faint text such as DRAFT, CONFIDENTIAL or DO NOT COPY (or a picture) "
              "behind the text on every page.",
  steps=["Faint text behind every page = Watermark"],
  wrong="A footnote adds a note at the bottom of a page. Drop Cap enlarges the first letter of a paragraph. "
        "WordArt in a header would not sit faintly behind the body text by itself.", seconds=15,
  facts=[fact("Microsoft: On the Design tab, select Watermark and choose a pre-configured watermark like DRAFT, "
              "CONFIDENTIAL or DO NOT COPY.", MS_WATERMARK)])
Q(T, "MS PowerPoint", "Basic",
  "On one slide of a PowerPoint presentation, a trainer wants the three bullet points to appear one by one, each "
  "flying in when she clicks. Which PowerPoint feature should she apply to the bullet text?",
  ["Animation", "Transition", "Slide Master", "Hyperlink"],
  concept="Animations vs transitions",
  explanation="Animations are effects applied to objects ON a slide (text, pictures, shapes), such as Fly In, and "
              "can be triggered by clicks. Transitions are effects between one slide and the next.",
  steps=["Effect on an object within a slide = Animation"],
  wrong="A transition changes how the whole slide replaces the previous one. Slide Master controls common design. "
        "A hyperlink jumps to another slide or page.", seconds=15)
Q(T, "Shortcuts", "Intermediate",
  "In Excel for Windows, a clerk wants to type a customer's address on two lines inside the same cell. Which key "
  "combination starts a new line within the cell?",
  ["Alt + Enter", "Enter", "Ctrl + Enter", "Shift + Tab"],
  concept="Excel keyboard shortcuts",
  explanation="Alt + Enter inserts a line break inside the cell being edited.",
  steps=["New line in the same cell = Alt + Enter"],
  wrong="Enter finishes the entry and moves to the next cell. Ctrl + Enter fills the selected cells with the "
        "current entry. Shift + Tab moves to the previous cell.", seconds=15,
  facts=[fact("Microsoft Excel shortcuts: Start a new line in the same cell - Alt+Enter.", MS_XL_KEYS)])
Q(T, "MS PowerPoint", "Intermediate",
  "A presenter has a slide of detailed figures that she wants to keep in the file and show only if someone asks, "
  "but it must be skipped during the normal slide show. What should she do?",
  ["Hide the slide (Slide Show > Hide Slide)", "Delete the slide", "Move the slide to the end",
   "Apply a slow transition to the slide"],
  concept="Hidden slides",
  explanation="A hidden slide stays in the presentation but is skipped in Slide Show view. It can still be shown "
              "on demand during the show.",
  steps=["Keep in file + skip in show = Hide Slide"],
  wrong="Deleting removes the slide from the file. Moving it to the end still shows it. A transition only changes "
        "how it appears.", seconds=20,
  facts=[fact("Microsoft: A hidden slide remains in the file; it is merely hidden when you run Slide Show view.",
              MS_HIDE)])
Q(T, "Shortcuts", "Advanced",
  "Column A of a sheet has 2,000 full names such as 'Kumar, Asha'. A clerk types 'Asha Kumar' in B2 next to the "
  "first name, then presses one key combination, and Excel fills the rest of column B by recognising the pattern, "
  "without any formula. Which feature and shortcut is this?",
  ["Flash Fill - Ctrl + E", "AutoSum - Alt + =", "Fill Down - Ctrl + D", "Find and Replace - Ctrl + H"],
  concept="Flash Fill",
  explanation="Flash Fill detects the pattern from the example(s) typed and fills the column to match (here, "
              "swapping first and last names). It is started from Data > Flash Fill or with Ctrl + E.",
  steps=["Pattern from an example, no formula = Flash Fill", "Shortcut Ctrl + E"],
  wrong="AutoSum inserts a SUM formula. Fill Down (Ctrl + D) just copies the top cell downwards, giving 'Asha "
        "Kumar' in every row. Find and Replace changes given text.", seconds=25,
  facts=[fact("Microsoft: Flash Fill fills a column using the data pattern, like first and last name; select "
              "Data > Flash Fill or press Ctrl+E.", MS_FLASH)])
Q(T, "MS PowerPoint", "Advanced",
  "For a branch-lobby display, a presenter wants PowerPoint to record how long she actually spends on each slide "
  "while she practises, and then save these times so the slides later advance automatically. Which feature "
  "should she use?",
  ["Rehearse Timings", "Slide Sorter view", "Presenter View", "Hide Slide"],
  concept="Rehearsing slide timings",
  explanation="Slide Show > Rehearse Timings runs the show with a timer, records the time spent on each slide, and "
              "at the end asks whether to save the timings, which can then advance the slides automatically.",
  steps=["Record time per slide while practising = Rehearse Timings"],
  wrong="Slide Sorter view shows thumbnails (and saved timings), but does not record them. Presenter View shows "
        "notes to the speaker. Hide Slide skips a slide.", seconds=20,
  facts=[fact("Microsoft: Select Slide Show > Rehearse Timings; at the end select Yes to save the slide timings "
              "or No to discard them.", MS_REHEARSE)])

# ================================================================ 12. Digital Payments (1 / 2 / 1)
T = "Digital Payments"
Q(T, "Payment technology", "Basic",
  "A car passes through a national-highway toll plaza without stopping, and the toll is deducted automatically "
  "because a reader at the plaza detects the FASTag sticker on the windscreen. Which wireless technology does "
  "FASTag use?",
  ["RFID (Radio Frequency Identification)", "Bluetooth", "GPS", "Infrared"],
  concept="Electronic toll collection",
  explanation="FASTag is a passive RFID tag linked to a prepaid wallet or bank account. The reader at the toll "
              "plaza powers and reads the tag by radio waves, and the toll is debited automatically.",
  steps=["Windscreen tag read by radio at the plaza = RFID"],
  wrong="Bluetooth needs pairing between devices. GPS finds location from satellites. Infrared needs a clear line "
        "of sight and is not used by FASTag.", seconds=15,
  facts=[fact("FASTag is an electronic toll collection system that uses RFID technology to make toll payments "
              "from the linked prepaid or bank account.", FASTAG)], web=SC)
Q(T, "Payment technology", "Intermediate",
  "A government scheme sends a beneficiary a prepaid voucher for a health check-up as a QR code or an SMS string "
  "on her mobile. She can redeem it only for that purpose at the listed hospital, even without a bank account, "
  "card or payment app. Which NPCI product is this?",
  ["e-RUPI", "UPI Lite", "RuPay credit card", "IMPS"],
  concept="Purpose-specific digital vouchers",
  explanation="e-RUPI is a person-specific and purpose-specific cashless e-voucher delivered as a QR code or SMS "
              "string; the beneficiary does not need a bank account to redeem it.",
  steps=["Voucher + QR/SMS + one purpose + no bank account needed = e-RUPI"],
  wrong="UPI Lite is an on-device wallet in a UPI app. A RuPay card is linked to an account or credit line. IMPS "
        "is an instant account-to-account transfer.", seconds=20,
  facts=[fact("NPCI e-RUPI product booklet: a person- and purpose-specific cashless e-voucher, distributed only as "
              "a QR code or SMS string; the beneficiary need not have a bank account.", ERUPI)], web=SC)
Q(T, "Payment technology", "Intermediate",
  "A customer wants her monthly OTT subscription to be paid automatically from her bank account through her UPI "
  "app, after approving it once with her UPI PIN. Which UPI facility does this?",
  ["UPI AutoPay (recurring e-mandate)", "UPI 123PAY", "Collect request", "Static QR code"],
  concept="Recurring payments on UPI",
  explanation="UPI AutoPay lets a customer create an e-mandate, authorised with the UPI PIN, for recurring "
              "payments (daily, weekly, monthly and so on); later debits run automatically within the set limits.",
  steps=["Recurring automatic debit after one approval = UPI AutoPay"],
  wrong="123PAY is UPI for feature phones. A collect request asks for one payment and must be approved each time. "
        "A static QR code is a fixed merchant code for one-off payments.", seconds=20,
  facts=[fact("NPCI introduced AutoPay on UPI for recurring payments; customers create an e-mandate authorised with "
              "the UPI PIN.", AUTOPAY)], web=SC)
Q(T, "Payment technology", "Advanced",
  "A 'buyer' of a customer's old sofa on an online marketplace sends her a UPI request and says, 'Enter your UPI "
  "PIN to RECEIVE the Rs 8,000 payment.' What is actually happening?",
  ["It is a collect-request fraud: entering the UPI PIN approves a payment OUT of her account",
   "Entering the PIN is needed to receive money, so it is safe",
   "The PIN only confirms her identity and moves no money",
   "The money will come in first and the PIN only reverses it if needed"],
  concept="UPI collect-request fraud",
  explanation="In UPI, the PIN is entered only to authorise a debit from one's own account. Receiving money never "
              "needs a PIN (or a QR scan by the receiver). A request that asks for the PIN to 'receive' money is a "
              "payment request, and approving it sends Rs 8,000 to the fraudster.",
  steps=["UPI PIN = authorise money going out", "Receiving needs no PIN", "-> fraud"],
  wrong="Receiving never needs the PIN. Entering the PIN on a request always approves a debit, not just an "
        "identity check, and there is no automatic reversal.", seconds=25,
  facts=[fact("NPCI UPI Safety Shield: Enter UPI PIN only to deduct money from your account; UPI PIN is not "
              "required for receiving money.", UPI_SHIELD)], web=SC)

# ================================================================ 13. Computer Abbreviations (1 / 2 / 3)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic",
  "Customers withdraw cash at any time from a machine outside the branch called an ATM. What does ATM stand for?",
  ["Automated Teller Machine", "Any Time Money", "Automatic Transaction Monitor", "Account Transfer Machine"],
  concept="Banking-technology abbreviations",
  explanation="ATM = Automated Teller Machine: it performs a teller's routine tasks (cash withdrawal, balance "
              "enquiry, mini statement) without a human teller.",
  steps=["ATM = Automated Teller Machine"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "A customer sends money instantly to another bank account at 11 p.m. on a Sunday through IMPS. What does IMPS "
  "stand for?",
  ["Immediate Payment Service", "Internet Money Processing System", "Instant Mobile Payment Scheme",
   "Interbank Message Posting Service"],
  concept="Payment-system abbreviations",
  explanation="IMPS (Immediate Payment Service), run by NPCI, provides instant interbank transfers round the clock "
              "through mobile, internet banking, ATMs and branches.",
  steps=["IMPS = Immediate Payment Service"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "A bank allows officers to read office email on their personal smartphones under a BYOD policy, provided the "
  "phones have a screen lock and the bank's security app. What does BYOD stand for?",
  ["Bring Your Own Device", "Backup Your Office Data", "Block Your Own Download", "Bank Your Online Deposits"],
  concept="IT-policy abbreviations",
  explanation="BYOD (Bring Your Own Device) policies let employees use personal devices for work, with security "
              "rules to protect the organisation's data.",
  steps=["BYOD = Bring Your Own Device"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Advanced",
  "A bank's security operations centre collects logs from firewalls, servers and branch PCs in one SIEM system, "
  "which correlates events and raises alerts on suspicious patterns. What does SIEM stand for?",
  ["Security Information and Event Management", "System Integrity and Error Monitoring",
   "Secure Internet Email Manager", "Server Incident Escalation Module"],
  concept="Security abbreviations",
  explanation="SIEM (Security Information and Event Management) gathers and analyses log data from across an "
              "organisation in real time to detect and investigate security incidents.",
  steps=["SIEM = Security Information and Event Management"], wrong="The other expansions are made up.",
  seconds=15)
Q(T, S, "Advanced",
  "Under Section 70B of the IT Act, 2000, banks must report certain cyber incidents to CERT-In, India's national "
  "agency for responding to computer security incidents. What does CERT-In stand for?",
  ["Indian Computer Emergency Response Team", "Centre for Electronic Records and Transactions - India",
   "Cyber Enforcement and Regulatory Taskforce - India", "Certified Electronic Risk Testing - India"],
  concept="Cyber-security institutions",
  explanation="CERT-In (Indian Computer Emergency Response Team), under the Ministry of Electronics and "
              "Information Technology, is the national nodal agency for responding to computer security "
              "incidents under Section 70B of the IT Act.",
  steps=["CERT-In = Indian Computer Emergency Response Team"], wrong="The other expansions are made up.",
  seconds=15,
  facts=[fact("CERT-In (Indian Computer Emergency Response Team) is the national agency for incident response "
              "under Section 70B of the IT Act, 2000.", CERTIN)], web=SC)
Q(T, S, "Advanced",
  "A bank installs DLP software that detects and blocks attempts to send customer account numbers or Aadhaar "
  "numbers outside the bank by email, USB drive or upload. What does DLP stand for?",
  ["Data Loss Prevention", "Digital Licence Protection", "Download Limit Policy", "Data Link Protocol"],
  concept="Security abbreviations",
  explanation="DLP (Data Loss Prevention) tools identify sensitive data in use, in motion and at rest, and block or "
              "alert on attempts to move it out through unauthorised channels.",
  steps=["DLP = Data Loss Prevention"],
  wrong="The other expansions are not what DLP means in security; 'data link protocol' is an unrelated networking "
        "term.", seconds=15)

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_007_plan.json").read_text(encoding="utf-8"))
cplan = next(s for s in plan["subjects"] if s["subject"] == CK)
want = Counter({(t["topic"], d): n for t in cplan["topics"] for d, n in t["quota"].items() if n})
got = Counter((q["topic"], q["difficulty"]) for q in questions)
assert got == want, (got - want, want - got)
subs = {t["topic"]: set(t["subtopics"]) for t in cplan["topics"]}
for q in questions:
    assert q["subtopic"] in subs[q["topic"]], (q["question_id"], q["subtopic"])
    assert q["solution"]["final_answer"].startswith(f"Option {q['correct_answer']}: ")
assert len(questions) == 100
assert questions[0]["question_id"] == cplan["question_ids"][0] and questions[-1]["question_id"] == cplan["question_ids"][1]
assert stimuli[0]["stimulus_id"] == cplan["stimulus_id_start"]
for s in stimuli:
    pos = [q["set_position"] for q in questions if q.get("stimulus_id") == s["stimulus_id"]]
    assert pos == list(range(1, len(pos) + 1)) and 3 <= len(pos) <= 6, (s["stimulus_id"], pos)
keys = Counter(q["correct_answer"] for q in questions)
assert max(keys.values()) <= 28 and min(keys.values()) >= 22, keys

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_007",
    "created_at": TODAY,
    "notes": "BATCH_007 Computer Knowledge part: 100 original, mostly scenario-based questions (BANK_COMP_000603 to "
             "BANK_COMP_000702), 44 of them in nine shared sets (STIM_COMP_007001-007009: pseudocode loop, Linux "
             "terminal session, backup schedule, email header, branch network, incident timeline, biometric test "
             "report, Customers/Accounts SQL tables, Excel loan sheet). Computable answers are re-derived in "
             "tools/batch_007/computer.py (loop simulated; SQL run in sqlite3 with foreign keys on; subnetting and "
             "longest-prefix match via ipaddress; Excel results recomputed). Facts from Microsoft, RFC, MDN, MITRE "
             "ATT&CK, POSIX, man7 and Computer History Museum pages were checked on 2026-11-05; PARAM, Turing 1936, "
             "e-RUPI, UPI AutoPay, FASTag, the UPI PIN safety rule and CERT-In were confirmed from search results "
             "only (web:search-confirmed).",
    "stimuli": stimuli,
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_007_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
