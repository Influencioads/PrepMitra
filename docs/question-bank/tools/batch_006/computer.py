"""Writes batches/parts/BATCH_006_COMP.json: the 100 Computer Knowledge questions of BATCH_006.

BATCH_006 leans on applied, scenario-based questions. Every computable answer is re-derived below with assertions
before the file is written: fractional binary, hex code space, floating-point 0.1 + 0.2, weighted CPI, SSTF and FCFS
disk-head movement, photo capacity in binary units, Mbps -> MB/s, Hamming check bits, route summarisation via
ipaddress, propagation delay, OTP guess probability, symmetric/asymmetric key counts, XOR cipher, SQL results on the
shared Loans table and the NULL comparison via sqlite3, Excel AVERAGEIF / RANK.EQ / COUNTIF(">"&AVERAGE) on the shared
sheet and an Excel date difference via datetime. The plan quota per (topic, difficulty), subtopics, the ID range,
stimulus IDs and the answer-key balance are also asserted. If any assertion fails, nothing is written.

    python tools/batch_006/computer.py      (run from docs/question-bank)
"""

import datetime as dt
import ipaddress
import json
import math
import random
import sqlite3
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
FIRST_ID = 503
AI = ("ai:author-solve", "ai:independent-check")
COMPUTED = ("script:recompute", "ai:author-solve", "ai:independent-check")

_rng = random.Random(20261105 + 6)
_keys = Counter()
questions = []
stimuli = []


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


def ordered(correct, distractors, fmt=str):
    """Numeric options in ascending order; returns (option texts, answer letter)."""
    vals = sorted([correct] + list(distractors))
    assert len(set(vals)) == 4, vals
    return [fmt(v) for v in vals], LETTERS[vals.index(correct)]


def Q(topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, wrong, seconds=30,
      shortcut=None, computed=False, facts=None, web="web:fact-check", stim=None, pos=None):
    """Adds one question. With answer=None, options[0] is the correct text and it is placed at the least-used key
    so far (random tie-break, fixed seed). Ordered options (numbers) pass an explicit answer letter.
    web is 'web:fact-check' (page opened) or 'web:search-confirmed' (confirmed only in search results)."""
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
# 0.75 = 1/2 + 1/4 -> 0.11 (binary)
def bin_frac(s):
    return sum(F(int(d), 2 ** (i + 1)) for i, d in enumerate(s))


assert bin_frac("11") == F(3, 4) and bin_frac("101") == F(5, 8) and bin_frac("111") == F(7, 8)
assert bin_frac("011") == F(3, 8)
# 4 hexadecimal digits -> 16^4 codes
assert 16 ** 4 == 65_536 and 16 ** 3 == 4096 and 16 ** 5 == 1_048_576
# Floating point: 0.1 + 0.2 is not exactly 0.3 in binary floating point
assert 0.1 + 0.2 != 0.3 and repr(0.1 + 0.2) == "0.30000000000000004"
# Weighted CPI: 50% x 1 + 30% x 2 + 20% x 3
CPI = F(50, 100) * 1 + F(30, 100) * 2 + F(20, 100) * 3
assert CPI == F(17, 10) and F(1 + 2 + 3, 3) == 2


# Disk scheduling: head at 50, queue 82, 170, 43, 140, 24, 16, 190
QUEUE = [82, 170, 43, 140, 24, 16, 190]


def sstf(head, reqs):
    left, total = list(reqs), 0
    while left:
        dists = sorted(abs(r - head) for r in left)
        assert len(dists) == 1 or dists[0] != dists[1], "tie"
        nxt = min(left, key=lambda r: abs(r - head))
        total += abs(nxt - head)
        head = nxt
        left.remove(nxt)
    return total


def fcfs_disk(head, reqs):
    total = 0
    for r in reqs:
        total += abs(r - head)
        head = r
    return total


SSTF, FCFS_D = sstf(50, QUEUE), fcfs_disk(50, QUEUE)
assert (SSTF, FCFS_D) == (208, 642)
assert (50 - 16) + (190 - 16) == 208  # same as SSTF here: go down to 16, then up to 190
# 64 GB pen drive, 4 MB photos, binary units
PHOTOS = 64 * 1024 // 4
assert PHOTOS == 16_384 and 64_000 // 4 == 16_000
# 100 Mbps -> MB/s (1 MB = 10^6 bytes)
assert F(100 * 10 ** 6, 8 * 10 ** 6) == F(25, 2)
# Hamming SEC check bits for 64 data bits: smallest r with 2^r >= m + r + 1
HAM = next(r for r in range(1, 20) if 2 ** r >= 64 + r + 1)
assert HAM == 7 and 2 ** 6 < 64 + 6 + 1
# Route summarisation of 192.168.4.0/24 ... 192.168.7.0/24
SUMM = list(ipaddress.collapse_addresses(ipaddress.ip_network(f"192.168.{i}.0/24") for i in range(4, 8)))
assert [str(n) for n in SUMM] == ["192.168.4.0/22"]
assert not ipaddress.ip_network("192.168.8.0/24").subnet_of(SUMM[0])
assert ipaddress.ip_network("192.168.4.0/23").num_addresses == 512  # /23 covers only 4.x and 5.x
# Propagation delay: 2000 km at 2 x 10^8 m/s
assert F(2000 * 1000, 2 * 10 ** 8) == F(1, 100)  # 0.01 s = 10 ms
# OTP: 6 digits, 3 distinct guesses
assert F(3, 10 ** 6) == F(3, 1_000_000) and 10 ** 6 == 1_000_000
# Keys for 10 users: symmetric pairwise C(10, 2); asymmetric 10 key pairs = 20 keys
assert math.comb(10, 2) == 45 and 10 * 2 == 20
# XOR cipher
PT, KEY = 0b10110011, 0b01101010
CT = PT ^ KEY
assert format(CT, "08b") == "11011001" and CT ^ KEY == PT
assert format(PT | KEY, "08b") == "11111011" and format(PT & KEY, "08b") == "00100010"
assert format(~CT & 0xFF, "08b") == "00100110"

# SQL: shared Loans table (stimulus 1)
LOANS = [("L1", "Pune", "Home", 2500000, "Active"), ("L2", "Delhi", "Car", 800000, "Closed"),
         ("L3", "Pune", "Car", 650000, "Active"), ("L4", "Agra", "Home", 1800000, "Active"),
         ("L5", "Delhi", "Home", 3200000, "Active"), ("L6", "Pune", "Gold", 150000, "Closed"),
         ("L7", "Agra", "Car", 900000, "Closed"), ("L8", "Delhi", "Gold", 200000, "Active")]
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Loans (loan_id TEXT, branch TEXT, type TEXT, amount INTEGER, status TEXT)")
db.executemany("INSERT INTO Loans VALUES (?, ?, ?, ?, ?)", LOANS)
SQL_B = db.execute("SELECT COUNT(*) FROM Loans WHERE status = 'Active' AND amount > 1000000").fetchone()[0]
assert SQL_B == 3
assert db.execute("SELECT COUNT(*) FROM Loans WHERE status = 'Active' OR amount > 1000000").fetchone()[0] == 5
assert db.execute("SELECT COUNT(*) FROM Loans WHERE status = 'Active'").fetchone()[0] == 5
assert db.execute("SELECT COUNT(*) FROM Loans WHERE amount > 1000000").fetchone()[0] == 3  # all three are Active
SQL_I = db.execute("SELECT branch, SUM(amount) AS total FROM Loans GROUP BY branch ORDER BY total DESC").fetchall()
assert SQL_I == [("Delhi", 4200000), ("Pune", 3300000), ("Agra", 2700000)]
SQL_A = db.execute("SELECT COUNT(*) FROM Loans WHERE type = 'Car' OR type = 'Home' AND status = 'Active'").fetchone()[0]
SQL_A_PAREN = db.execute(
    "SELECT COUNT(*) FROM Loans WHERE (type = 'Car' OR type = 'Home') AND status = 'Active'").fetchone()[0]
assert (SQL_A, SQL_A_PAREN) == (6, 4)
assert db.execute("SELECT COUNT(*) FROM Loans WHERE type IN ('Car', 'Home')").fetchone()[0] == 6
# NULL comparison
db.execute("CREATE TABLE Branch (code TEXT, manager TEXT)")
db.executemany("INSERT INTO Branch VALUES (?, ?)",
               [("B01", "Asha"), ("B02", None), ("B03", "Ravi"), ("B04", None), ("B05", "Meena")])
assert db.execute("SELECT COUNT(*) FROM Branch WHERE manager = NULL").fetchone()[0] == 0
assert db.execute("SELECT COUNT(*) FROM Branch WHERE manager IS NULL").fetchone()[0] == 2

# Excel: shared deposits sheet (stimulus 2)
SHEET = [("Asha", "Pune", 48), ("Ravi", "Delhi", 62), ("Meena", "Pune", 55), ("John", "Agra", 62),
         ("Farah", "Pune", 41), ("Kiran", "Delhi", 70)]
DEP = [d for _, _, d in SHEET]
PUNE = [d for _, b, d in SHEET if b == "Pune"]
AVG_IF = F(sum(PUNE), len(PUNE))
assert AVG_IF == 48 and sum(PUNE) == 144 and F(sum(DEP), 6) == F(338, 6)
RANK = 1 + sum(1 for d in DEP if d > SHEET[1][2])  # RANK.EQ(C3, C2:C7), descending
assert RANK == 2 and 1 + sum(1 for d in DEP if d < 62) == 4  # ascending rank would be 4
ABOVE = sum(1 for d in DEP if d > F(sum(DEP), len(DEP)))
assert ABOVE == 3
# Excel date difference: 15-Apr-2026 minus 15-Jan-2026
DAYS = (dt.date(2026, 4, 15) - dt.date(2026, 1, 15)).days
assert DAYS == 90

# ---------------------------------------------------------------- fact-check sources
# Pages opened on 2026-11-05 (web:fact-check)
MS_WIN = "https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec"
MS_SAFE = ("https://support.microsoft.com/en-us/windows/start-your-pc-in-safe-mode-in-windows-92c27cff-db89-8644-"
           "1ce4-b3e5e56fe234")
MS_AVGIF = "https://support.microsoft.com/en-us/office/averageif-function-faec8e2e-0dec-4308-af69-f5576d8ac642"
MS_RANK = "https://support.microsoft.com/en-us/office/rank-eq-function-284858ce-8ef6-450e-b662-26245be04a40"
MS_COUNTIF = "https://support.microsoft.com/en-us/office/countif-function-e0de10c6-f885-4e71-abb4-1f464816df34"
MS_DATE = "https://support.microsoft.com/en-us/office/date-function-e36c0c8c-4104-49da-ab83-82328b832349"
MS_DV = ("https://support.microsoft.com/en-us/office/apply-data-validation-to-cells-29fecbcc-d1b9-42c1-9d76-"
         "eff3ce5f7249")
MS_TOC = "https://support.microsoft.com/en-us/office/insert-a-table-of-contents-882e8564-0edb-435e-84b5-1d8552ccf0c0"
MS_KIOSK = ("https://support.microsoft.com/en-us/office/create-a-self-running-presentation-57fc41ae-f36a-4fb5-94a3-"
            "52d5bc466037")
RFC6455 = "https://www.rfc-editor.org/rfc/rfc6455"
RFC791 = "https://www.rfc-editor.org/rfc/rfc791"
MDN_ACAO = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Origin"
MITRE_SPRAY = "https://attack.mitre.org/techniques/T1110/003/"
MITRE_MFA = "https://attack.mitre.org/techniques/T1621/"
MITRE_WATER = "https://attack.mitre.org/techniques/T1189/"
MAN_MV = "https://man7.org/linux/man-pages/man1/mv.1.html"
SUDO = "https://www.sudo.ws/docs/man/sudo.man/"
# Confirmed only in search results (web:search-confirmed)
NPCI_LITE = ("https://www.npci.org.in/PDF/npci/upi/circular/2022/UPI-OC-138-Introduction-of-On-Device-wallet-UPI-"
             "Lite-for-Small-Value-Transactions.pdf")
ISO7812 = "https://en.wikipedia.org/wiki/ISO/IEC_7812"
MDR_SRC = "https://www.au.bank.in/blogs/what-is-merchant-discount-rate"
MS_OEM = ("https://learn.microsoft.com/en-us/archive/blogs/mssmallbiz/no-oem-microsoft-windows-licenses-cannot-be-"
          "transferred-to-another-pc")
SC = "web:search-confirmed"

# ================================================================ 1. Computer Fundamentals (2 / 1 / 1)
T = "Computer Fundamentals"
Q(T, "Types of computers", "Basic",
  "A bank's data-analytics officer needs a powerful single-user desktop computer with a fast multi-core processor, "
  "a large RAM and a professional graphics card to run heavy statistical models on his own desk. Which type of "
  "computer is this?",
  ["Workstation", "Mainframe computer", "Thin client", "Embedded computer"],
  concept="Types of computers by purpose",
  explanation="A workstation is a high-performance computer meant for one user doing technical or analytical work "
              "such as modelling, CAD or video editing. It is more powerful than an ordinary office PC but is still "
              "a single-user desk machine.",
  steps=["Single user + very high performance + on the desk = workstation"],
  wrong="A mainframe serves thousands of users from a data centre. A thin client has little processing power and "
        "depends on a server. An embedded computer is built into another device for one fixed task.", seconds=15)
o = ["0.11", "0.101", "0.111", "0.011"]
Q(T, "Number systems", "Basic",
  "An interest rate of 0.75 is to be stored in binary. Which binary fraction is exactly equal to the decimal "
  "number 0.75?", o,
  concept="Decimal fraction to binary",
  explanation="Multiply the fraction by 2 repeatedly and take the whole-number parts: 0.75 x 2 = 1.5 (digit 1), "
              "0.5 x 2 = 1.0 (digit 1), and the remainder is 0. So 0.75 = 0.11 in binary, i.e. 1/2 + 1/4.",
  steps=["0.75 x 2 = 1.5 -> 1", "0.5 x 2 = 1.0 -> 1, stop", "0.75 = (0.11) base 2"],
  shortcut="Place values after the binary point are 1/2, 1/4, 1/8 ...; 0.75 = 1/2 + 1/4.",
  wrong="0.101 = 1/2 + 1/8 = 0.625; 0.111 = 0.875; 0.011 = 1/4 + 1/8 = 0.375.", seconds=30, computed=True)
o, a = ordered(65536, [64, 4096, 1048576], fmt=lambda v: f"{v:,}")
Q(T, "Number systems", "Intermediate",
  "A bank gives each of its terminals an ID made of exactly 4 hexadecimal digits (0-9, A-F), for example 0A7F. "
  "How many different terminal IDs are possible?", o, a,
  concept="Counting codes in a number system",
  explanation="Each hexadecimal digit can take 16 values, and the 4 positions are independent, so the number of "
              "codes is 16 x 16 x 16 x 16 = 16^4 = 65,536 (0000 to FFFF). This equals 2^16, because each hex digit "
              "stands for 4 bits.",
  steps=["Choices per digit = 16", "Positions = 4", "16^4 = 65,536"],
  shortcut="4 hex digits = 16 bits, and 2^16 = 65,536.",
  wrong="64 multiplies 16 by 4 instead of raising it to the power 4. 4,096 is for 3 digits and 1,048,576 for 5.",
  seconds=30, computed=True)
Q(T, "Number systems", "Advanced",
  "A programmer adds 0.1 and 0.2 in a program that uses standard binary floating-point numbers, and the result "
  "prints as 0.30000000000000004 instead of 0.3. What is the reason?",
  ["0.1 and 0.2 have no exact finite binary representation, so they are stored as close approximations",
   "The processor's adder circuit is faulty and must be replaced",
   "Floating-point numbers can store only whole numbers exactly, so every fraction is rounded to an integer",
   "The result overflowed the largest number that a floating-point variable can hold"],
  concept="Representation error in binary floating point",
  explanation="Just as 1/3 becomes 0.333... in decimal, 1/10 becomes a never-ending repeating fraction in binary "
              "(0.000110011...). A float keeps only a fixed number of bits, so 0.1 and 0.2 are stored as tiny "
              "approximations, and their sum is not exactly the stored value nearest to 0.3. This is why money is "
              "usually handled with decimal types or as whole paise.",
  steps=["0.1 in binary = 0.0001100110011... (repeats forever)", "Stored value is rounded",
         "Rounding errors show up in the sum"],
  wrong="The hardware works correctly; this is a representation limit. Floats do store fractions, only not every "
        "fraction exactly. The values are far below the overflow limit.", seconds=35, computed=True)

# ================================================================ 2. Hardware (1 / 3 / 3)
T = "Hardware"
Q(T, "Motherboard and ports", "Basic",
  "An old branch PC has a keyboard whose plug is round with six small pins and is usually colour-coded purple. "
  "Which port is this keyboard meant for?",
  ["PS/2 port", "HDMI port", "RJ-45 port", "VGA port"],
  concept="Legacy input ports",
  explanation="PS/2 is a round 6-pin mini-DIN connector used on older PCs for keyboards (purple) and mice (green). "
              "USB has largely replaced it.",
  steps=["Round 6-pin keyboard/mouse connector = PS/2"],
  wrong="HDMI carries digital video and audio, RJ-45 is the Ethernet network connector, and VGA is a 15-pin "
        "D-shaped analog video port.", seconds=15)
Q(T, "CPU and components", "Intermediate",
  "A teller's laptop becomes very hot when its cooling vents are blocked by files, and the processor "
  "automatically lowers its clock speed so that its temperature stays within safe limits. What is this behaviour "
  "called?",
  ["Thermal throttling", "Overclocking", "Hyper-Threading", "Pipelining"],
  concept="CPU temperature protection",
  explanation="When a processor reaches its temperature limit, it reduces its clock speed (and voltage) to produce "
              "less heat. This protects the chip but makes the computer slower until it cools down.",
  steps=["Too hot -> processor slows itself = thermal throttling"],
  wrong="Overclocking raises the clock above the rated speed. Hyper-Threading runs two threads on one core. "
        "Pipelining overlaps the stages of several instructions.", seconds=20)
Q(T, "Motherboard and ports", "Intermediate",
  "One disk in a bank's file server fails. The technician pulls the failed disk out of its front bay and inserts "
  "a new one while the server keeps running and users stay connected. Which capability of the drive bays and "
  "interface allows this?",
  ["Hot swapping", "Cold booting", "Overclocking", "Defragmentation"],
  concept="Replacing hardware without shutting down",
  explanation="Hot swapping (hot plugging) means a component can be removed and replaced while the system is "
              "powered on. Server drive bays with SAS/SATA backplanes support it, usually together with RAID so "
              "that no data is lost when a disk is removed.",
  steps=["Replace a part while the system runs = hot swap"],
  wrong="A cold boot starts a computer from power-off. Overclocking speeds up a processor. Defragmentation "
        "rearranges file pieces on a hard disk.", seconds=20)
Q(T, "CPU and components", "Intermediate",
  "Almost all smartphones, including those used for mobile banking, use processors based on a RISC "
  "instruction-set architecture known for low power use. Which architecture is it?",
  ["ARM", "x86-64", "IBM z/Architecture", "Itanium (IA-64)"],
  concept="Processor architectures",
  explanation="ARM is a RISC architecture whose designs are licensed to many chip makers. Its energy efficiency "
              "makes it the standard for smartphones and tablets.",
  steps=["Smartphone processor architecture = ARM (RISC)"],
  wrong="x86-64 is the CISC architecture of most desktop and laptop PCs. z/Architecture is used in IBM mainframes. "
        "Itanium was a server architecture that has been discontinued.", seconds=20)
o, a = ordered(F(17, 10), [F(3, 2), F(19, 10), F(2)], fmt=lambda v: f"{float(v):.1f}")
Q(T, "CPU and components", "Advanced",
  "In a program, 50% of executed instructions are ALU operations taking 1 clock cycle each, 30% are load/store "
  "instructions taking 2 cycles, and 20% are branches taking 3 cycles. What is the average CPI (cycles per "
  "instruction)?", o, a,
  concept="Weighted average CPI",
  explanation="Average CPI is the sum of (fraction of instructions x cycles) over all instruction classes: "
              "0.5 x 1 + 0.3 x 2 + 0.2 x 3 = 0.5 + 0.6 + 0.6 = 1.7.",
  steps=["ALU: 0.5 x 1 = 0.5", "Load/store: 0.3 x 2 = 0.6", "Branch: 0.2 x 3 = 0.6", "CPI = 1.7"],
  wrong="2.0 is the simple average of 1, 2 and 3, ignoring how often each class occurs. 1.5 and 1.9 come from "
        "arithmetic slips.", seconds=45, computed=True)
Q(T, "CPU and components", "Advanced",
  "In a pipelined processor, the instruction ADD R1, R2, R3 is immediately followed by SUB R4, R1, R5. SUB needs "
  "the new value of R1 before ADD has written it back. What kind of pipeline problem is this?",
  ["Data hazard (read after write)", "Structural hazard", "Control hazard", "Cache coherence problem"],
  concept="Pipeline hazards",
  explanation="A data hazard arises when an instruction depends on the result of an earlier instruction still in "
              "the pipeline. Here SUB reads R1 after ADD writes it (RAW). It is handled by forwarding the result "
              "or by stalling.",
  steps=["Second instruction needs first one's result = data dependency", "Read after write -> data hazard"],
  wrong="A structural hazard is two instructions needing the same hardware unit at once. A control hazard comes "
        "from branches. Cache coherence concerns copies of data in several processors' caches.", seconds=30)
Q(T, "CPU and components", "Advanced",
  "In a loop, the processor reaches a conditional jump before the condition has been worked out. Instead of "
  "waiting, it guesses which way the jump will go from its past behaviour and starts fetching instructions on that "
  "path; if the guess is wrong, those instructions are discarded. What is this technique called?",
  ["Branch prediction", "Operand forwarding", "Direct memory access", "Interrupt handling"],
  concept="Keeping the pipeline full",
  explanation="A branch predictor records how branches behaved before and predicts the next outcome. Correct "
              "guesses keep the pipeline busy; a wrong guess flushes the speculatively fetched instructions.",
  steps=["Guess the direction of a conditional jump = branch prediction"],
  wrong="Operand forwarding passes a result directly to a waiting instruction. DMA moves data between a device "
        "and memory without the CPU. Interrupt handling responds to device signals.", seconds=25)

# ================================================================ 3. Software (3 / 4 / 2)
T = "Software"
Q(T, "Programming languages", "Basic",
  "An interest program compiles without errors. While it is running, it crashes with a 'division by zero' message "
  "when it processes a branch that has no accounts. What type of error is this?",
  ["Runtime error", "Syntax error", "Compilation error", "Linker error"],
  concept="Types of program errors",
  explanation="A runtime error occurs only while the program is executing, when an operation becomes impossible, "
              "such as dividing by zero or opening a missing file. The program was syntactically correct, so it "
              "compiled.",
  steps=["Compiled fine, failed while running = runtime error"],
  wrong="Syntax and compilation errors stop the program from being compiled at all. A linker error occurs when "
        "the parts of a program are combined, before it runs.", seconds=15)
Q(T, "Licensing", "Basic",
  "A new laptop is bought with Windows already installed by the laptop maker. Its licence is tied to that laptop "
  "and cannot be moved to another computer. What type of licence is this?",
  ["OEM licence", "Site licence", "Open-source licence", "Public domain licence"],
  concept="Software licence types",
  explanation="An OEM (Original Equipment Manufacturer) licence comes pre-installed by the hardware maker. It is "
              "bound to the device it first ships with and generally has no transfer rights.",
  steps=["Pre-installed by maker + tied to device = OEM licence"],
  wrong="A site licence covers many computers at one organisation's premises. An open-source licence lets users "
        "see and change the code. Public domain software has no copyright at all.", seconds=15, web=SC,
  facts=[fact("Microsoft small-business blog: OEM Windows licences have no transfer rights and stay with the "
              "computer they were shipped with and installed on.", MS_OEM)])
Q(T, "System and application software", "Basic",
  "A branch officer adds a small add-on to her web browser that blocks pop-up advertisements. The add-on works "
  "only inside the browser and extends what the browser can do. What is such software called?",
  ["Browser extension (plug-in)", "Device driver", "Operating system", "Firmware"],
  concept="Add-on software",
  explanation="An extension or plug-in is a small program that adds a feature to a host application such as a "
              "browser. It cannot run on its own.",
  steps=["Adds a feature to the browser = extension / plug-in"],
  wrong="A device driver lets the OS control hardware. The operating system manages the whole computer. Firmware "
        "is stored in a device's chip and controls its basic functions.", seconds=15)
Q(T, "Programming languages", "Intermediate",
  "A developer wants to stop a loan program at a chosen line, run it one statement at a time and watch how the "
  "value of a variable changes, to find a bug. Which tool should she use?",
  ["Debugger", "Linker", "Assembler", "Loader"],
  concept="Programming tools",
  explanation="A debugger lets a programmer set breakpoints, step through code line by line and inspect or watch "
              "variables while the program runs, which helps locate logic and runtime errors.",
  steps=["Breakpoints + step through + watch variables = debugger"],
  wrong="A linker joins object files into one executable, an assembler translates assembly language into machine "
        "code, and a loader copies a program into memory to run it.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "A function to find the balance after n years is written as: balance(n) = balance(n - 1) x 1.07, with "
  "balance(0) = the opening deposit. The function calls itself with a smaller value of n until n reaches 0. What "
  "is this programming technique called?",
  ["Recursion", "Encapsulation", "Inheritance", "Compilation"],
  concept="Recursion",
  explanation="A recursive function solves a problem by calling itself on a smaller version of the same problem, "
              "and stops at a base case (here n = 0).",
  steps=["Function calls itself + base case = recursion"],
  wrong="Encapsulation hides an object's data behind its methods. Inheritance lets a class reuse another class's "
        "members. Compilation translates source code into machine code.", seconds=20)
Q(T, "System and application software", "Intermediate",
  "Ten programmers work on the same banking app. The team needs software that records every change to the source "
  "files, shows who changed what, lets each person work on a separate branch, and can bring back any earlier "
  "version. Which kind of tool is this?",
  ["Version control system such as Git", "Compiler such as GCC", "Spreadsheet program", "Disk defragmenter"],
  concept="Software development tools",
  explanation="A version control system keeps the full history of a project's files, supports branches and "
              "merging, and lets the team compare or restore any earlier version. Git is the most widely used.",
  steps=["Track changes, branches, restore old versions = version control"],
  wrong="A compiler translates code but keeps no change history. A spreadsheet is an application for tables of "
        "numbers. A defragmenter rearranges file pieces on a hard disk.", seconds=20)
Q(T, "Licensing", "Intermediate",
  "A budgeting app can be used free of charge forever with its basic features, with no time limit. Advanced "
  "features such as detailed reports are unlocked only after paying for a premium plan. What is this business "
  "model called?",
  ["Freemium", "Shareware", "Freeware", "Public domain"],
  concept="Software distribution models",
  explanation="Freemium (free + premium) gives a basic version free permanently and charges for extra features "
              "or capacity.",
  steps=["Free basic version forever + paid extras = freemium"],
  wrong="Shareware is a trial that must be bought after the trial period. Freeware is fully free with no paid "
        "tier. Public domain software has no copyright owner.", seconds=20)
Q(T, "System and application software", "Advanced",
  "Several programs on a Windows server use the same library file (a .dll file). The library is not copied into "
  "each program; it is loaded when a program runs, so replacing the one library file fixes a bug in all of them. "
  "What is this method of linking called?",
  ["Dynamic linking", "Static linking", "Cross-compilation", "Interpretation"],
  concept="Static and dynamic linking",
  explanation="With dynamic linking, the library code (a DLL on Windows, a .so file on Linux) stays in a separate "
              "file and is attached when the program is loaded or run. Programs share it and get its updates "
              "automatically. Static linking copies the library code into each executable at build time.",
  steps=["Library loaded at run time and shared = dynamic linking"],
  wrong="Static linking copies the code into every program, so each would need rebuilding. Cross-compilation "
        "produces code for another platform. Interpretation executes source code line by line.", seconds=30)
Q(T, "Programming languages", "Advanced",
  "A developer writes the software for an ATM's card-reader controller on his Windows PC. He compiles it on the PC "
  "into machine code for the controller's different (ARM) processor and then loads it onto the device. What kind "
  "of compiler is he using?",
  ["Cross-compiler", "Interpreter", "Decompiler", "Just-in-time compiler"],
  concept="Compiling for another platform",
  explanation="A cross-compiler runs on one platform (the host) and produces executable code for a different "
              "platform (the target). It is standard for embedded devices that are too small to compile code "
              "themselves.",
  steps=["Compile on machine A, run on machine B with a different processor = cross-compiler"],
  wrong="An interpreter executes code directly without producing an executable. A decompiler turns machine code "
        "back into source-like code. A JIT compiler compiles while the program runs, on the same machine.",
  seconds=25)

# ================================================================ 4. Operating Systems (1 / 4 / 1)
T = "Operating Systems"
Q(T, "Windows and Linux basics", "Basic",
  "A cashier has the core banking screen, a calculator and an email window open on Windows. Which keyboard "
  "shortcut lets him switch quickly between these open windows?",
  ["Alt + Tab", "Ctrl + Z", "Windows logo key + L", "Ctrl + P"],
  concept="Windows keyboard shortcuts",
  explanation="Alt + Tab switches between open windows; holding Alt and pressing Tab repeatedly cycles through "
              "them.",
  steps=["Switch between open windows = Alt + Tab"],
  wrong="Ctrl + Z undoes the last action, Windows + L locks the computer, and Ctrl + P prints.", seconds=10,
  facts=[fact("Microsoft: Alt + Tab switches between open windows; hold Alt and press Tab repeatedly to cycle "
              "through them.", MS_WIN)])
Q(T, "Windows and Linux basics", "Intermediate",
  "On a Linux server, an administrator wants to rename the file report.txt to report_2026.txt in the same folder. "
  "Which command does this?",
  ["mv report.txt report_2026.txt", "cp report.txt report_2026.txt", "rm report.txt report_2026.txt",
   "cat report.txt report_2026.txt"],
  concept="Linux file commands",
  explanation="Linux has no separate rename command for this everyday task: mv (move) renames a file when the "
              "destination is a new name in the same directory, and moves it when the destination is another "
              "directory.",
  steps=["Rename = move to a new name = mv old new"],
  wrong="cp makes a copy and leaves the original. rm deletes the files. cat displays file contents.", seconds=20,
  facts=[fact("Linux man page: mv - move (rename) files; rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.",
              MAN_MV)])
Q(T, "Windows and Linux basics", "Intermediate",
  "A Linux user who is not logged in as root needs to install a software package, which requires administrative "
  "rights. Which command should he put before the install command so that it runs with superuser privileges, if "
  "the system's policy permits him?",
  ["sudo", "pwd", "grep", "chmod"],
  concept="Running commands as the superuser",
  explanation="sudo lets a permitted user run a command as the superuser (or another user), as allowed by the "
              "security policy, usually after entering his own password. Every use can be logged.",
  steps=["Run one command with admin rights = sudo command"],
  wrong="pwd prints the current directory, grep searches text, and chmod changes file permissions; none of them "
        "raises the user's privileges.", seconds=15,
  facts=[fact("sudo manual: sudo allows a permitted user to execute a command as the superuser or another user, "
              "as specified by the security policy.", SUDO)])
Q(T, "Functions", "Intermediate",
  "After a faulty printer driver was installed, a branch PC crashes during every normal start-up. The technician "
  "wants Windows to start with only a basic set of files and drivers so that he can remove the faulty driver. "
  "Which start-up mode should he use?",
  ["Safe Mode", "Sleep mode", "Airplane mode", "Tablet mode"],
  concept="Troubleshooting start-up",
  explanation="Safe Mode starts Windows in a basic state with a limited set of files and drivers. If the problem "
              "does not appear in Safe Mode, default drivers and settings are not the cause, and the faulty "
              "driver can be removed.",
  steps=["Start with minimal drivers to troubleshoot = Safe Mode"],
  wrong="Sleep mode pauses a running session in low power. Airplane mode turns off wireless radios. Tablet mode "
        "changes the interface for touch use.", seconds=15,
  facts=[fact("Microsoft: Safe mode starts Windows in a basic state, using a limited set of files and drivers.",
              MS_SAFE)])
Q(T, "File systems", "Intermediate",
  "On Linux, the ls command does not show the configuration file .bashrc in a user's home directory, although the "
  "file exists. Which command will list it?",
  ["ls -a", "ls -l", "pwd", "mkdir .bashrc"],
  concept="Hidden files in Linux",
  explanation="In Linux, any file or directory whose name begins with a dot is hidden from a normal listing. "
              "ls -a (all) shows these hidden entries too.",
  steps=["Name starts with '.' -> hidden", "Show all entries -> ls -a"],
  wrong="ls -l gives a long listing with permissions and sizes but still hides dot-files. pwd prints the current "
        "directory. mkdir creates a directory.", seconds=20)
o, a = ordered(SSTF, [140, 174, FCFS_D])
Q(T, "Functions", "Advanced",
  "A disk's read/write head is at cylinder 50. Requests are waiting for cylinders 82, 170, 43, 140, 24, 16 and 190 "
  "(in that order of arrival). Using SSTF (Shortest Seek Time First) disk scheduling, what is the total head "
  "movement in cylinders?", o, a,
  concept="Disk scheduling: SSTF",
  explanation="SSTF always serves the pending request closest to the current head position. From 50: 43 (7), "
              "24 (19), 16 (8), then the nearest is 82 (66), 140 (58), 170 (30), 190 (20). Total = 7 + 19 + 8 + "
              "66 + 58 + 30 + 20 = 208 cylinders.",
  steps=["50 -> 43 -> 24 -> 16: 7 + 19 + 8 = 34", "16 -> 82 -> 140 -> 170 -> 190: 66 + 58 + 30 + 20 = 174",
         "Total = 34 + 174 = 208"],
  wrong="642 is the movement under FCFS, serving requests in arrival order. 174 counts only the upward sweep "
        "from 16, and 140 is just 190 - 50.", seconds=75, computed=True)

# ================================================================ 5. Input and Output Devices (2 / 1 / 3)
T = "Input and Output Devices"
Q(T, "Output devices", "Basic",
  "A training officer wants to show his PowerPoint slides on a large wall screen to 60 new recruits in a hall. "
  "Which output device should he connect to the laptop?",
  ["Projector", "Scanner", "Webcam", "Barcode reader"],
  concept="Output devices",
  explanation="A projector takes the computer's video signal and throws an enlarged image onto a screen or wall, "
              "so a large audience can see it.",
  steps=["Large image for an audience = projector (output)"],
  wrong="A scanner, a webcam and a barcode reader are all input devices; they send data into the computer.",
  seconds=10)
Q(T, "Output devices", "Basic",
  "A branch prints a customer's account statement on paper. Output that is produced in a permanent physical form "
  "such as paper is called:",
  ["Hard copy", "Soft copy", "Source code", "Cache copy"],
  concept="Hard copy and soft copy",
  explanation="Hard copy is printed (physical) output, for example from a printer or plotter. Soft copy is output "
              "seen on a screen or stored as a file, which disappears from view when the display changes.",
  steps=["Printed on paper = hard copy"],
  wrong="Soft copy is on-screen or electronic. Source code is a program's text. A cache copy is temporary data "
        "kept for faster access.", seconds=10)
Q(T, "Output devices", "Intermediate",
  "When a user types on a smartphone's on-screen keyboard, the phone gives a short vibration with each key press, "
  "so that the touch feels like pressing a real key. This kind of touch-based output is called:",
  ["Haptic feedback", "Optical character recognition", "Speech synthesis", "Refresh rate"],
  concept="Haptic output",
  explanation="Haptic (tactile) feedback uses small vibration motors or actuators to give the user a sense of "
              "touch, such as a 'click' or a buzz to confirm an action.",
  steps=["Output felt as vibration/touch = haptic feedback"],
  wrong="OCR converts images of text into editable text (input). Speech synthesis is spoken output. Refresh rate "
        "is how many times per second a display redraws its image.", seconds=20)
Q(T, "Output devices", "Advanced",
  "In one kind of inkjet printer, the print head does not heat the ink. Instead, a crystal material changes shape "
  "when a voltage is applied, and this movement pushes each ink droplet out of the nozzle. What type of inkjet "
  "technology is this?",
  ["Piezoelectric inkjet", "Thermal (bubble) inkjet", "Dot-matrix impact", "Laser electrophotography"],
  concept="Inkjet print-head technologies",
  explanation="Inkjet printers use one of two main methods. Thermal (bubble) inkjets heat the ink to form a "
              "bubble that forces a drop out. Piezoelectric inkjets use a crystal that flexes when voltage is "
              "applied, which pushes the drop out without heating the ink.",
  steps=["Crystal flexes under voltage, no heating = piezoelectric inkjet"],
  wrong="A thermal inkjet heats the ink. A dot-matrix printer strikes an inked ribbon with pins. A laser printer "
        "uses a drum and toner.", seconds=25)
Q(T, "Output devices", "Advanced",
  "A visually impaired bank officer reads screen text through a device placed below the keyboard, on which small "
  "pins rise and fall to form Braille characters that change as he moves through the document. What is this "
  "device?",
  ["Refreshable Braille display", "Optical mark reader", "Graphics tablet", "Light pen"],
  concept="Assistive output devices",
  explanation="A refreshable Braille display is an output device. Screen-reader software sends text to it, and "
              "electronically controlled pins form Braille cells that the user reads by touch; the pins change "
              "as the text changes.",
  steps=["Pins forming Braille from screen text = refreshable Braille display (output)"],
  wrong="An optical mark reader reads marked bubbles on forms. A graphics tablet and a light pen are input "
        "devices for drawing or pointing.", seconds=25)
Q(T, "Input devices", "Advanced",
  "When a customer turns her phone sideways, the banking app switches from portrait to landscape view. Which "
  "built-in input sensor detects the change in the phone's orientation from the direction of gravity?",
  ["Accelerometer", "Proximity sensor", "Ambient light sensor", "Fingerprint sensor"],
  concept="Sensors as input devices",
  explanation="An accelerometer measures acceleration along three axes, including the constant pull of gravity, "
              "so the phone can tell which way it is being held and rotate the screen. A gyroscope often helps "
              "with rotation.",
  steps=["Detect tilt/orientation from gravity = accelerometer"],
  wrong="A proximity sensor detects an object near the screen (e.g. the ear during a call). An ambient light sensor "
        "adjusts brightness. A fingerprint sensor authenticates the user.", seconds=20)

# ================================================================ 6. Memory (5 / 4 / 1)
T = "Memory"
Q(T, "Secondary storage", "Basic",
  "A branch saves scanned documents to an online service so that they are stored on the provider's remote servers "
  "and can be opened from any computer through the internet. What is this type of storage called?",
  ["Cloud storage", "Cache memory", "ROM", "CPU register"],
  concept="Types of storage",
  explanation="Cloud storage keeps files on servers run by a provider, reached over the internet. Users can access "
              "them from many devices, and the provider handles backup of the hardware.",
  steps=["Files on remote servers via internet = cloud storage"],
  wrong="Cache memory and registers are small, fast memories inside or near the CPU. ROM holds firmware on the "
        "computer itself.", seconds=10)
o, a = ordered(PHOTOS, [2048, 16000, 65536], fmt=lambda v: f"{v:,}")
Q(T, "Cache and units", "Basic",
  "A pen drive has 64 GB of free space. How many photos of exactly 4 MB each can it hold? (Use 1 GB = 1024 MB.)",
  o, a,
  concept="Storage unit conversion",
  explanation="64 GB = 64 x 1024 MB = 65,536 MB. Each photo uses 4 MB, so the drive holds 65,536 / 4 = 16,384 "
              "photos.",
  steps=["64 GB = 64 x 1024 = 65,536 MB", "65,536 / 4 = 16,384 photos"],
  wrong="16,000 uses 1 GB = 1000 MB. 65,536 forgets to divide by the photo size. 2,048 divides by 32 instead of "
        "4.", seconds=30, computed=True)
Q(T, "Secondary storage", "Basic",
  "A clerk needs an optical disc on which backup files can be written, erased and written again many times. Which "
  "disc should he use?",
  ["CD-RW", "CD-ROM", "CD-R", "Blu-ray BD-ROM"],
  concept="Optical disc types",
  explanation="RW (ReWritable) discs can be erased and re-recorded many times. R discs can be written only once, "
              "and ROM discs come pre-recorded and cannot be written by the user.",
  steps=["Write, erase and rewrite = RW disc"],
  wrong="CD-ROM and BD-ROM are read-only discs pressed at the factory. A CD-R can be written only once.",
  seconds=10)
Q(T, "Primary memory", "Basic",
  "A branch PC becomes slow when the clerk keeps the core banking application, several browser tabs and a "
  "spreadsheet open together. Which upgrade most directly lets the PC hold more running programs at once?",
  ["Adding more RAM", "Adding a larger hard disk for archives", "Replacing the keyboard",
   "Installing a higher-resolution monitor"],
  concept="Role of RAM",
  explanation="Running programs and their data must be held in RAM (main memory). With too little RAM, the "
              "system keeps moving data to and from disk, which slows it down. More RAM lets more programs stay in "
              "memory at once.",
  steps=["Many programs open at once -> need more main memory -> add RAM"],
  wrong="Extra archive disk space does not help programs that are already running. The keyboard and monitor do not "
        "affect how many programs can be kept in memory.", seconds=15)
o, a = ordered(F(25, 2), [F(5, 4), F(100), F(800)], fmt=lambda v: f"{float(v):g} MB per second")
Q(T, "Cache and units", "Basic",
  "A branch's internet connection is 100 Mbps (megabits per second). At full speed, how many megabytes of data can "
  "it download per second? (Take 1 byte = 8 bits.)", o, a,
  concept="Bits and bytes in data rates",
  explanation="Network speeds use bits (small b), file sizes use bytes (capital B). Dividing by 8 converts bits "
              "to bytes: 100 / 8 = 12.5 MB per second.",
  steps=["1 byte = 8 bits", "100 Mbps / 8 = 12.5 MBps"],
  wrong="100 confuses megabits with megabytes. 800 multiplies by 8 instead of dividing. 1.25 divides by 80.",
  seconds=20, computed=True)
Q(T, "Secondary storage", "Intermediate",
  "A video-editing PC stripes its data across two disks so that reads and writes are split between them and are "
  "faster, but there is no copy or parity: if either disk fails, all the data is lost. Which RAID level is this?",
  ["RAID 0", "RAID 1", "RAID 5", "RAID 6"],
  concept="RAID levels",
  explanation="RAID 0 (striping) spreads blocks across disks for speed and uses their full combined capacity, but "
              "it has no redundancy, so the failure of any one disk destroys the array.",
  steps=["Striping, no redundancy = RAID 0"],
  wrong="RAID 1 mirrors data on two disks. RAID 5 stripes with one disk's worth of parity and RAID 6 with two, so "
        "both survive disk failures.", seconds=20)
Q(T, "Secondary storage", "Intermediate",
  "Each flash memory cell in an SSD can be erased and rewritten only a limited number of times. The SSD's "
  "controller therefore spreads writes evenly across all its cells, so that no area wears out early. What is "
  "this technique called?",
  ["Wear levelling", "Defragmentation", "Disk mirroring", "Low-level formatting"],
  concept="SSD endurance",
  explanation="Wear levelling maps logical blocks to different physical cells over time, so that writes are "
              "spread evenly and the drive lasts longer.",
  steps=["Spread writes evenly over flash cells = wear levelling"],
  wrong="Defragmentation rearranges file pieces on hard disks and is not needed on SSDs. Mirroring copies data to a "
        "second disk. Low-level formatting prepares the physical surface of a disk.", seconds=20)
Q(T, "Primary memory", "Intermediate",
  "A report-generation program runs for days on a server. Each run allocates RAM for temporary data but never "
  "releases it, so the program's memory use keeps rising until the server slows down and the program crashes. "
  "What is this fault called?",
  ["Memory leak", "Buffer cache", "Thrashing", "Memory interleaving"],
  concept="Memory management faults",
  explanation="A memory leak happens when a program keeps allocating memory but fails to free memory it no longer "
              "needs. Usage grows steadily until memory runs out. Restarting the program releases the memory, but "
              "the fix is in the code.",
  steps=["Memory allocated, never freed, usage keeps growing = memory leak"],
  wrong="A buffer cache is a useful store of disk data in RAM. Thrashing is constant paging when RAM is too small "
        "for the working set, a possible effect but not the fault itself. Interleaving spreads addresses across "
        "memory banks for speed.", seconds=25)
Q(T, "Primary memory", "Intermediate",
  "A technician installs two identical 8 GB RAM modules in the matching coloured slots of a motherboard instead "
  "of one 16 GB module, so that the memory controller can access both modules at the same time and nearly double "
  "the memory bandwidth. Which feature is being used?",
  ["Dual-channel memory", "Virtual memory", "ECC memory", "Cache write-back"],
  concept="Memory channels",
  explanation="In dual-channel mode, the memory controller uses two independent 64-bit channels in parallel, "
              "giving a 128-bit path to RAM and nearly double the bandwidth. Modules must be placed in the paired "
              "slots shown in the motherboard manual.",
  steps=["Two matched modules in paired slots, accessed together = dual channel"],
  wrong="Virtual memory uses disk space as an extension of RAM. ECC memory detects and corrects bit errors. "
        "Write-back is a cache write policy.", seconds=25)
o, a = ordered(HAM, [5, 6, 8])
Q(T, "Cache and units", "Advanced",
  "A server's ECC memory uses a Hamming code that can correct any single-bit error in a 64-bit data word. For m "
  "data bits, the number of check bits r must satisfy 2^r >= m + r + 1. What is the smallest number of check bits "
  "needed?", o, a,
  concept="Hamming code check bits",
  explanation="Try values of r. r = 6: 2^6 = 64, but 64 + 6 + 1 = 71, so 64 < 71 fails. r = 7: 2^7 = 128 and "
              "64 + 7 + 1 = 72, so 128 >= 72 holds. Seven check bits are needed; adding one overall parity bit "
              "for double-error detection gives the familiar 72-bit ECC word (SECDED).",
  steps=["r = 6: 64 >= 71? No", "r = 7: 128 >= 72? Yes", "r = 7"],
  wrong="5 and 6 are too few (32 and 64 are less than the required 70 and 71). 8 is the SECDED total with the "
        "extra parity bit, not the minimum for single-error correction.", seconds=50, computed=True)

# ================================================================ 7. Internet (1 / 4 / 2)
T = "Internet"
Q(T, "Web basics", "Basic",
  "A customer applying for a loan online selects the scanned copy of her PAN card on her computer and sends it to "
  "the bank's website. Sending a file from your computer to a server on the internet is called:",
  ["Uploading", "Downloading", "Browsing", "Bookmarking"],
  concept="Uploading and downloading",
  explanation="Uploading transfers a file from the local computer to a remote server. Downloading is the "
              "opposite: copying a file from a server to the local computer.",
  steps=["Local computer -> server = upload"],
  wrong="Downloading copies data from the server to the computer. Browsing is viewing web pages. Bookmarking saves "
        "a page's address.", seconds=10)
Q(T, "Web basics", "Intermediate",
  "A bank updates its home page, but one employee keeps seeing the old version even after re-typing the address, "
  "while colleagues see the new page. The usual fix is to clear the browser's stored copies of recently visited "
  "pages and images. What are these stored copies called?",
  ["Browser cache", "Browsing history", "Bookmarks", "Plug-ins"],
  concept="Browser cache",
  explanation="Browsers keep local copies of pages, images and scripts in a cache so that sites load faster on "
              "later visits. If the cached copy is still used, the user sees outdated content until the cache is "
              "cleared or the page is reloaded fresh.",
  steps=["Old stored copy of a page shown = browser cache"],
  wrong="History is only a list of visited addresses. Bookmarks are saved links. Plug-ins add features to the "
        "browser and do not store page copies.", seconds=20)
Q(T, "Web basics", "Intermediate",
  "In the address https://bank.example/locate?branch=pune&type=atm , what is the part branch=pune&type=atm "
  "(after the question mark) called?",
  ["Query string", "Domain name", "Protocol (scheme)", "Port number"],
  concept="Parts of a URL",
  explanation="In a URL, the part after ? is the query string. It passes name=value pairs, joined by &, to the "
              "server, here asking for ATMs in Pune. https is the scheme, bank.example the domain name and "
              "/locate the path.",
  steps=["After '?' = query string of name=value pairs joined by '&'"],
  wrong="The domain name is bank.example and the scheme is https. No port is written, so the default 443 is used.",
  seconds=20)
Q(T, "Web basics", "Intermediate",
  "When a customer logs in to net banking, the server builds a page at that moment showing his own name, accounts "
  "and latest balance from the database. The same address shows different content to different customers. What "
  "kind of web page is this?",
  ["Dynamic web page", "Static web page", "Home page", "Offline web page"],
  concept="Static and dynamic web pages",
  explanation="A dynamic page is generated by the server (or by scripts) when it is requested, usually from a "
              "database, so its content changes with the user and time. A static page is a fixed file that "
              "everyone sees in the same form.",
  steps=["Content built per request, differs per user = dynamic page"],
  wrong="A static page is the same for every visitor. A home page is a site's starting page, which may be static "
        "or dynamic. An offline page is a saved copy.", seconds=20)
Q(T, "Email", "Intermediate",
  "A regional office wants to send circulars to all 40 branch managers by typing a single address, such as "
  "branch-managers@bank.example, instead of entering 40 addresses each time. What is such a group address "
  "called?",
  ["Distribution list (mailing list)", "Bcc field", "Email signature", "Auto-reply"],
  concept="Group email addresses",
  explanation="A distribution list (mailing list or contact group) is one name or address that stands for many "
              "members. A message sent to it is delivered to everyone on the list, and membership can be changed "
              "centrally.",
  steps=["One address that reaches many members = distribution list"],
  wrong="Bcc hides recipients but still needs each address typed. A signature is text added at the end of "
        "messages. An auto-reply answers incoming mail automatically.", seconds=20)
Q(T, "Protocols", "Advanced",
  "A share-trading screen must receive price updates pushed by the server the moment they change, and also send "
  "orders, over one long-lived two-way connection rather than repeatedly asking the server with new HTTP "
  "requests. Which protocol, standardised in RFC 6455, is designed for this?",
  ["WebSocket", "FTP", "POP3", "SNMP"],
  concept="Full-duplex web communication",
  explanation="The WebSocket protocol starts with an HTTP handshake and then keeps a single TCP connection open, "
              "over which both client and server can send messages at any time. This suits live prices, chat and "
              "notifications.",
  steps=["Persistent two-way browser-server channel = WebSocket"],
  wrong="FTP transfers files, POP3 downloads email, and SNMP monitors and manages network devices.", seconds=25,
  facts=[fact("RFC 6455: the WebSocket Protocol enables two-way communication between a client and a remote host.",
              RFC6455)])
Q(T, "Web basics", "Advanced",
  "A script on https://partner.example tries to read data from an API at https://api.bank.example. Because the "
  "origins differ, the browser blocks the script from reading the response unless the bank's server sends a "
  "particular response header naming the allowed origin. Which header is it?",
  ["Access-Control-Allow-Origin", "Strict-Transport-Security", "Set-Cookie", "Content-Length"],
  concept="Cross-Origin Resource Sharing (CORS)",
  explanation="Under CORS, a server lists which other origins may read its responses. The browser checks the "
              "Access-Control-Allow-Origin header and lets the script read the response only if the requesting "
              "origin is allowed.",
  steps=["Cross-origin read permission = CORS header Access-Control-Allow-Origin"],
  wrong="Strict-Transport-Security forces HTTPS for a site. Set-Cookie stores a cookie. Content-Length gives the "
        "body size.", seconds=30,
  facts=[fact("MDN: the Access-Control-Allow-Origin response header indicates whether the response can be shared "
              "with requesting code from the given origin.", MDN_ACAO)])

# ================================================================ 8. Networking (4 / 2 / 5)
T = "Networking"
Q(T, "Topologies", "Basic",
  "A bank links the computers of all its branches and offices spread across one city, such as Pune, into a single "
  "network. A network covering a city is called a:",
  ["MAN (Metropolitan Area Network)", "PAN (Personal Area Network)", "LAN (Local Area Network)",
   "WAN (Wide Area Network) spanning several countries"],
  concept="Networks by geographic size",
  explanation="By area: a PAN covers a person's devices, a LAN one building or campus, a MAN a city, and a WAN "
              "large regions, countries or the world.",
  steps=["City-wide network = MAN"],
  wrong="A PAN links personal devices a few metres apart. A LAN covers one building or campus. A WAN spanning "
        "countries is much larger than one city.", seconds=10)
Q(T, "Devices", "Basic",
  "A bank's data centre links two buildings with a cable that carries data as pulses of light through thin glass "
  "strands, so that it is unaffected by electrical interference and can run long distances at high speed. Which "
  "cable is this?",
  ["Optical fibre cable", "Coaxial cable", "Unshielded twisted pair (UTP) cable", "Telephone cable (RJ-11)"],
  concept="Transmission media",
  explanation="Optical fibre sends data as light through glass or plastic cores. It offers very high bandwidth, "
              "long distances and immunity to electromagnetic interference.",
  steps=["Light pulses through glass = optical fibre"],
  wrong="Coaxial, twisted-pair and telephone cables all carry electrical signals over copper and are affected by "
        "electrical interference.", seconds=10)
Q(T, "Devices", "Basic",
  "Wi-Fi networks in bank branches follow a family of wireless LAN standards published by the IEEE. What is the "
  "number of this family of standards?",
  ["IEEE 802.11", "IEEE 802.3", "IEEE 802.15.1", "IEEE 1394"],
  concept="Networking standards",
  explanation="IEEE 802.11 is the family of wireless LAN standards on which Wi-Fi is based (802.11n, ac, ax and so "
              "on).",
  steps=["Wi-Fi = IEEE 802.11"],
  wrong="IEEE 802.3 is wired Ethernet, 802.15.1 is the basis of Bluetooth, and IEEE 1394 is FireWire.", seconds=10)
Q(T, "OSI and TCP/IP", "Basic",
  "Which OSI layer provides end-to-end delivery between processes on two computers, using port numbers, "
  "segmentation of data and (with TCP) error recovery and flow control?",
  ["Transport layer", "Data link layer", "Physical layer", "Presentation layer"],
  concept="OSI layer functions",
  explanation="The transport layer (layer 4) carries data between applications on the source and destination "
              "hosts. TCP and UDP work here, and port numbers identify the applications.",
  steps=["End-to-end, ports, segments = transport layer (layer 4)"],
  wrong="The data link layer delivers frames on one link using MAC addresses. The physical layer sends raw bits. "
        "The presentation layer handles data format, encryption and compression.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "A branch PC can print to the printer and open shared folders on its own LAN, but cannot reach any website or "
  "the head-office server outside the LAN. Its IP address and subnet mask are correct. Which setting is most "
  "likely missing or wrong?",
  ["Default gateway", "MAC address", "Screen resolution", "Printer driver"],
  concept="Default gateway",
  explanation="A host sends traffic for its own subnet directly, but traffic for any other network goes to the "
              "default gateway, normally the router's LAN address. If the gateway is missing or wrong, local "
              "access works while everything beyond the LAN fails.",
  steps=["Local works, remote fails = no route out = check default gateway"],
  wrong="The MAC address is burned into the network card and local traffic already works. Screen resolution and "
        "printer drivers have nothing to do with reaching other networks.", seconds=25)
Q(T, "OSI and TCP/IP", "Intermediate",
  "With a walkie-talkie, both people can talk to each other, but only one at a time; each must wait until the "
  "other stops. Which data transmission mode does this represent?",
  ["Half duplex", "Full duplex", "Simplex", "Multiplex"],
  concept="Transmission modes",
  explanation="Simplex sends in one direction only (like TV broadcast). Half duplex allows both directions but not "
              "at the same time (walkie-talkie). Full duplex allows both directions at once (telephone call).",
  steps=["Both ways, one at a time = half duplex"],
  wrong="Full duplex lets both talk at once. Simplex is one-way only. Multiplexing combines several signals on one "
        "channel and is not a direction mode.", seconds=15)
o = ["192.168.4.0/22", "192.168.4.0/23", "192.168.0.0/21", "192.168.4.0/24"]
Q(T, "OSI and TCP/IP", "Advanced",
  "A regional router learns four branch networks: 192.168.4.0/24, 192.168.5.0/24, 192.168.6.0/24 and "
  "192.168.7.0/24. To keep the routing table small, they are to be advertised as one summary route that covers "
  "exactly these four networks. What is the summary route?", o,
  concept="Route summarisation (supernetting)",
  explanation="Four /24 networks need 2 fewer prefix bits: /22. The third octets 4 to 7 are 000001 00 to 000001 11, "
              "so the first 6 bits of the third octet (000001) are common. The summary is 192.168.4.0/22, which "
              "covers 192.168.4.0 to 192.168.7.255.",
  steps=["4 networks = 2^2 -> prefix 24 - 2 = /22", "4 = 00000100, 7 = 00000111: common bits 000001",
         "Summary = 192.168.4.0/22"],
  shortcut="A /22 block starts at a multiple of 4 in the third octet; 4 is a multiple of 4.",
  wrong="/23 covers only 4.x and 5.x. 192.168.0.0/21 covers 0.x to 7.x, eight networks, more than required. /24 "
        "covers only 192.168.4.x.", seconds=60, computed=True)
o, a = ordered(F(10), [F(1), F(20, 3), F(100)], fmt=lambda v: f"{float(v):.3g} ms")
Q(T, "OSI and TCP/IP", "Advanced",
  "A fibre link between two data centres is 2,000 km long, and signals travel through the fibre at 2 x 10^8 m/s. "
  "What is the one-way propagation delay?", o, a,
  concept="Propagation delay",
  explanation="Propagation delay = distance / signal speed = (2,000 x 10^3 m) / (2 x 10^8 m/s) = 0.01 s = 10 ms. "
              "It depends on distance and the medium, not on the bandwidth of the link.",
  steps=["Distance = 2 x 10^6 m", "Delay = 2 x 10^6 / 2 x 10^8 = 10^-2 s", "= 10 ms"],
  wrong="6.67 ms uses the speed of light in vacuum (3 x 10^8 m/s). 1 ms and 100 ms are out by a factor of 10.",
  seconds=40, computed=True)
Q(T, "Devices", "Advanced",
  "A Wi-Fi radio cannot detect a collision while it is transmitting, because its own strong signal drowns out "
  "others. So before sending, it listens to the channel, waits a random back-off time, and relies on "
  "acknowledgements. Which media-access method does Wi-Fi use?",
  ["CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)",
   "CSMA/CD (Carrier Sense Multiple Access with Collision Detection)", "Token passing", "Polling by a master hub"],
  concept="Media access control",
  explanation="Classic shared (half-duplex) Ethernet used CSMA/CD: transmit, detect a collision, stop and retry. "
              "Wireless stations cannot reliably detect collisions, so IEEE 802.11 uses CSMA/CA, avoiding "
              "collisions with carrier sensing, random back-off and acknowledgements (optionally RTS/CTS).",
  steps=["Wireless cannot detect collisions -> avoid them", "Wi-Fi = CSMA/CA"],
  wrong="CSMA/CD needs collision detection, which radios lack. Token passing was used in Token Ring networks. "
        "Polling is not the Wi-Fi access method.", seconds=30)
Q(T, "OSI and TCP/IP", "Advanced",
  "Because of a routing mistake, packets between two routers keep going round in a loop. Which field in the IPv4 "
  "header makes sure that such a packet is eventually discarded instead of circulating forever?",
  ["Time to Live (TTL)", "Header checksum", "Type of Service", "Source address"],
  concept="IPv4 header fields",
  explanation="Every router that forwards an IPv4 packet decreases its TTL by at least 1. When the TTL reaches "
              "zero, the packet is destroyed (and an ICMP Time Exceeded message is usually sent back). The "
              "traceroute tool uses this behaviour.",
  steps=["Each hop: TTL - 1", "TTL = 0 -> packet discarded"],
  wrong="The header checksum detects header corruption. Type of Service marks priority. The source address "
        "identifies the sender. None limits the packet's lifetime.", seconds=25,
  facts=[fact("RFC 791: the Time to Live field must be decreased at each point that the internet header is "
              "processed; if it contains zero, the datagram must be destroyed.", RFC791)])
Q(T, "Devices", "Advanced",
  "A bank connects its core switches with redundant links for reliability. Without protection, these loops would "
  "let broadcast frames circulate endlessly (a broadcast storm). Which protocol makes the switches block some "
  "links logically to form a loop-free tree, and re-enables them if an active link fails?",
  ["Spanning Tree Protocol (STP)", "Address Resolution Protocol (ARP)",
   "Dynamic Host Configuration Protocol (DHCP)", "Simple Mail Transfer Protocol (SMTP)"],
  concept="Loop prevention in switched networks",
  explanation="STP (IEEE 802.1D, with the faster RSTP) elects a root bridge and puts redundant ports into a "
              "blocking state, so that exactly one active path exists between any two switches. If a link fails, "
              "a blocked port is moved to forwarding.",
  steps=["Redundant switch links + loop prevention = STP"],
  wrong="ARP maps IP addresses to MAC addresses, DHCP assigns IP settings to hosts, and SMTP sends email.",
  seconds=25)

# ================================================================ 9. Cybersecurity (3 / 6 / 2)
T = "Cybersecurity"
Q(T, "Malware", "Basic",
  "During a festival sale, a bank's net-banking website becomes unreachable because thousands of infected "
  "computers around the world send it a huge flood of requests at the same time. What is this attack called?",
  ["Distributed Denial of Service (DDoS) attack", "Phishing attack", "Shoulder surfing", "Keylogging"],
  concept="Availability attacks",
  explanation="A DDoS attack overloads a server or network with traffic from many sources, usually a botnet, so "
              "that genuine users cannot get service. It attacks availability rather than stealing data.",
  steps=["Flood of traffic from many machines -> service down = DDoS"],
  wrong="Phishing tricks users into revealing data. Shoulder surfing watches someone type a PIN or password. "
        "Keylogging records keystrokes.", seconds=15)
Q(T, "Encryption and authentication", "Basic",
  "An attacker uses a program that tries every possible combination of characters, one after another, until it "
  "finds a user's password. What is this method called?",
  ["Brute-force attack", "Phishing", "Tailgating", "Pharming"],
  concept="Password attacks",
  explanation="A brute-force attack systematically tries all possible passwords. Long, complex passwords and "
              "account lockout after a few failed attempts make it impractical.",
  steps=["Try every combination = brute force"],
  wrong="Phishing tricks the user into giving the password. Tailgating is following someone through a secure door. "
        "Pharming redirects users to a fake site by tampering with DNS.", seconds=10)
Q(T, "Malware", "Basic",
  "Which practice best allows a branch to recover its files after a ransomware attack without paying the "
  "attackers?",
  ["Keeping regular backups that are stored offline or separately from the network",
   "Saving all files on the same desktop for easy access",
   "Turning off the screen saver password",
   "Sharing one administrator password among all staff"],
  concept="Ransomware protection",
  explanation="Ransomware encrypts files on infected systems and on drives they can reach. Recent backups kept "
              "offline or isolated cannot be encrypted by the attack, so data can be restored after cleaning the "
              "systems.",
  steps=["Restore from clean, separate backups instead of paying"],
  wrong="Keeping files on the desktop, removing screen-lock passwords and sharing admin passwords all make attacks "
        "easier, not recovery.", seconds=15)
Q(T, "Phishing and social engineering", "Intermediate",
  "Attackers find that employees of several banks often visit a particular banking-industry news website. They "
  "secretly plant malicious code on that site, so that bank employees' computers get infected when they visit "
  "it. What is this attack called?",
  ["Watering hole attack", "Vishing", "Baiting", "Shoulder surfing"],
  concept="Targeted web compromise",
  explanation="In a watering hole attack, attackers compromise a legitimate website that their target group is "
              "known to visit, and wait for victims to come to it, like a predator waiting at a watering hole.",
  steps=["Infect a site the target group visits = watering hole"],
  wrong="Vishing uses phone calls. Baiting leaves an infected device or tempting download for victims. Shoulder "
        "surfing is watching someone type.", seconds=20,
  facts=[fact("MITRE ATT&CK T1189: a targeted campaign using websites visited by a specific community is often "
              "referred to as a strategic web compromise or watering hole attack.", MITRE_WATER)])
Q(T, "Phishing and social engineering", "Intermediate",
  "An attacker who has stolen an officer's password logs in again and again late at night, so that the officer's "
  "phone keeps receiving 'Approve sign-in?' push notifications. Hoping to stop the alerts, the officer finally "
  "taps Approve. What is this attack called?",
  ["MFA fatigue (push bombing)", "SIM swap fraud", "Credential stuffing", "Juice jacking"],
  concept="Attacks on multi-factor authentication",
  explanation="MFA fatigue abuses push-based MFA by flooding the user with approval requests until he approves "
              "one. Defences include number matching, limits on prompts and training users to report unexpected "
              "prompts.",
  steps=["Has password + floods approval prompts until user accepts = MFA fatigue"],
  wrong="SIM swap takes over the victim's mobile number. Credential stuffing tries leaked passwords on many sites. "
        "Juice jacking abuses public USB charging ports.", seconds=20,
  facts=[fact("MITRE ATT&CK T1621: adversaries may bombard users with MFA push notifications, SMS messages and "
              "phone calls; repeatedly generating prompts until the user accepts is known as MFA fatigue.",
              MITRE_MFA)])
Q(T, "Phishing and social engineering", "Intermediate",
  "A fraudster registers the domain examp1ebank.com (with the digit 1 in place of the letter l) to catch customers "
  "who mistype or misread the genuine examplebank.com, and sets up a look-alike login page there. What is this "
  "technique called?",
  ["Typosquatting", "Cryptojacking", "Logic bomb", "Botnet"],
  concept="Look-alike domains",
  explanation="Typosquatting (URL hijacking) registers domain names that differ slightly from a real brand's "
              "domain, relying on typing mistakes or careless reading, and uses them for phishing or malware.",
  steps=["Misspelt look-alike domain to catch users = typosquatting"],
  wrong="Cryptojacking mines cryptocurrency on victims' machines. A logic bomb is code triggered by a condition. "
        "A botnet is a network of infected computers.", seconds=20)
Q(T, "Encryption and authentication", "Intermediate",
  "A bank locks an account after five wrong passwords. An attacker avoids this by trying the same two or three "
  "very common passwords against thousands of different customer accounts, so that no single account gets enough "
  "failures to be locked. What is this attack called?",
  ["Password spraying", "Brute-force attack on one account", "Pharming", "Man-in-the-middle attack"],
  concept="Password spraying",
  explanation="Password spraying tries one or a few common passwords across many accounts. It stays under "
              "per-account lockout limits, so detection must look at failures across accounts and sources.",
  steps=["Few common passwords x many accounts, avoids lockout = password spraying"],
  wrong="A brute-force attack tries many passwords on one account and would trigger the lockout. Pharming "
        "redirects users through DNS tampering. A man-in-the-middle attack intercepts traffic.", seconds=20,
  facts=[fact("MITRE ATT&CK T1110.003: adversaries may use a single or small list of commonly used passwords "
              "against many different accounts to attempt to acquire valid account credentials.", MITRE_SPRAY)])
o = ["3 in 1,000,000", "1 in 1,000,000", "3 in 100,000", "1 in 10,000"]
Q(T, "Encryption and authentication", "Intermediate",
  "A transaction OTP has 6 digits (000000 to 999999), each value equally likely, and the bank allows only 3 "
  "attempts. If a fraudster guesses 3 different values, what is the probability that one of them is correct?", o,
  concept="Guessing probability and OTP length",
  explanation="There are 10^6 = 1,000,000 possible 6-digit OTPs. Three different guesses cover 3 of them, so the "
              "chance of success is 3 / 1,000,000. Limiting attempts keeps this tiny.",
  steps=["Possible OTPs = 10^6", "Guesses = 3 distinct values", "P = 3 / 1,000,000"],
  wrong="1 in 1,000,000 is the chance with a single guess. 3 in 100,000 assumes 5 digits. 1 in 10,000 is for a "
        "single guess of a 4-digit code.", seconds=30, computed=True)
Q(T, "Malware", "Intermediate",
  "A bank's email security system opens suspicious attachments in an isolated virtual environment and watches what "
  "they do there before delivering them, so that malware cannot harm real systems. What is this technique called?",
  ["Sandboxing", "Defragmentation", "Port forwarding", "Spooling"],
  concept="Malware analysis and containment",
  explanation="A sandbox is a restricted, isolated environment in which untrusted code can run. Its behaviour "
              "(changing files, contacting servers) can be observed without risk to the real network.",
  steps=["Run untrusted file in isolation and observe = sandboxing"],
  wrong="Defragmentation rearranges disk files, port forwarding redirects network traffic to an internal host, and "
        "spooling queues jobs such as print jobs.", seconds=20)
o = ["45 secret keys with symmetric encryption; 20 keys (10 key pairs) with public-key encryption",
     "90 secret keys with symmetric encryption; 10 keys with public-key encryption",
     "10 secret keys with symmetric encryption; 45 keys with public-key encryption",
     "20 secret keys with symmetric encryption; 20 keys (10 key pairs) with public-key encryption"]
Q(T, "Encryption and authentication", "Advanced",
  "Ten branch servers must each be able to communicate privately with every other one. How many keys are needed "
  "if every pair shares its own secret symmetric key, and how many if each server instead has its own public-"
  "private key pair?", o,
  concept="Key management: symmetric vs asymmetric",
  explanation="With symmetric keys, each pair of servers needs its own key: C(10, 2) = 10 x 9 / 2 = 45 keys. With "
              "public-key cryptography, each server needs only one key pair (a public and a private key), so 10 "
              "pairs = 20 keys in total. This is why asymmetric cryptography scales better.",
  steps=["Symmetric: n(n - 1)/2 = 10 x 9 / 2 = 45", "Asymmetric: 2n = 20 keys (10 pairs)"],
  shortcut="Symmetric grows as n^2/2; asymmetric grows as 2n.",
  wrong="90 counts every ordered pair twice. 10 or 20 secret keys are too few for every pair to have its own key. "
        "45 public keys confuses the two schemes.", seconds=45, computed=True)
o = ["11011001", "11111011", "00100010", "00100110"]
Q(T, "Encryption and authentication", "Advanced",
  "A simple stream cipher encrypts by XOR-ing each plaintext bit with a key bit. If the plaintext byte is 10110011 "
  "and the key byte is 01101010, what is the ciphertext?", o,
  concept="XOR in encryption",
  explanation="XOR gives 1 when the two bits differ and 0 when they are equal. 10110011 XOR 01101010 = 11011001. "
              "XOR-ing the ciphertext with the same key gives back the plaintext, which is why XOR is used in "
              "stream ciphers and the one-time pad.",
  steps=["1^0=1, 0^1=1, 1^1=0, 1^0=1, 0^1=1, 0^0=0, 1^1=0, 1^0=1", "Ciphertext = 11011001",
         "Check: 11011001 XOR 01101010 = 10110011"],
  wrong="11111011 is the OR of the two bytes, 00100010 the AND, and 00100110 the XNOR (inverted XOR).", seconds=45,
  computed=True)

# ================================================================ 10. Database Fundamentals (3 / 1 / 2)
T = "Database Fundamentals"
S_SQL = "STIM_COMP_006001"
stimuli.append({
    "stimulus_id": S_SQL, "type": "data_table", "title": "Loans table of a bank",
    "content": "Table **Loans** (amount in Rs):\n\n"
               "| loan_id | branch | type | amount | status |\n|---|---|---|---|---|\n"
               + "\n".join(f"| {l} | {b} | {t} | {a_} | {s} |" for l, b, t, a_, s in LOANS),
    "solution": "Active loans above Rs 10,00,000: L1, L4, L5. Branch totals: Delhi 42,00,000, Pune 33,00,000, "
                "Agra 27,00,000. AND is evaluated before OR in SQL conditions.",
})
o, a = ordered(SQL_B, [2, 5, 8])
Q(T, "SQL basics", "Basic",
  "Refer to the Loans table. How many rows does this query count?\n"
  "SELECT COUNT(*) FROM Loans WHERE status = 'Active' AND amount > 1000000;", o, a,
  concept="WHERE with AND",
  explanation="With AND, a row is counted only if both conditions are true. Active loans are L1, L3, L4, L5 and "
              "L8; of these, amount > 10,00,000 holds for L1 (25,00,000), L4 (18,00,000) and L5 (32,00,000). "
              "Count = 3.",
  steps=["Active: L1, L3, L4, L5, L8", "Of these, amount > 1000000: L1, L4, L5", "COUNT = 3"],
  wrong="5 counts all Active loans (or uses OR). 8 counts every row. 2 misses one qualifying loan.", seconds=40,
  computed=True, stim=S_SQL, pos=1)
o, a = ordered(4200000, [2700000, 3200000, 3300000], fmt=lambda v: f"{v:,}")
Q(T, "SQL basics", "Intermediate",
  "Refer to the Loans table. What value of total appears in the FIRST row returned by this query?\n"
  "SELECT branch, SUM(amount) AS total FROM Loans GROUP BY branch ORDER BY total DESC;", o, a,
  concept="GROUP BY with SUM and ORDER BY",
  explanation="GROUP BY makes one row per branch with the sum of its loan amounts: Pune 25,00,000 + 6,50,000 + "
              "1,50,000 = 33,00,000; Delhi 8,00,000 + 32,00,000 + 2,00,000 = 42,00,000; Agra 18,00,000 + "
              "9,00,000 = 27,00,000. ORDER BY total DESC puts the largest first: Delhi with 4,200,000.",
  steps=["Pune = 3,300,000", "Delhi = 4,200,000", "Agra = 2,700,000", "Descending -> first row Delhi, 4,200,000"],
  wrong="3,300,000 is Pune's total (second row). 2,700,000 is Agra's (last row). 3,200,000 is the largest single "
        "loan, not a branch total.", seconds=60, computed=True, stim=S_SQL, pos=2)
o, a = ordered(SQL_A, [1, SQL_A_PAREN, 8])
Q(T, "SQL basics", "Advanced",
  "Refer to the Loans table. How many rows does this query count?\n"
  "SELECT COUNT(*) FROM Loans WHERE type = 'Car' OR type = 'Home' AND status = 'Active';", o, a,
  concept="Operator precedence: AND before OR",
  explanation="In SQL, AND binds more tightly than OR, so the condition means type = 'Car' OR (type = 'Home' AND "
              "status = 'Active'). Car loans: L2, L3, L7 (any status). Active Home loans: L1, L4, L5. Total = 6. "
              "To count only active Car or Home loans, brackets are needed: (type = 'Car' OR type = 'Home') AND "
              "status = 'Active', which gives 4.",
  steps=["Read as: Car OR (Home AND Active)", "Car: L2, L3, L7 = 3", "Home and Active: L1, L4, L5 = 3",
         "COUNT = 6"],
  wrong="4 assumes the OR is evaluated first. 1 counts only active Car loans. 8 counts every row.", seconds=60,
  computed=True, stim=S_SQL, pos=3)
Q(T, "DBMS concepts", "Basic",
  "While designing a database for a bank, an analyst draws an E-R (Entity-Relationship) diagram. In the standard "
  "notation, which shape represents an entity set such as Customer or Account?",
  ["Rectangle", "Diamond", "Ellipse (oval)", "Double ellipse"],
  concept="E-R diagram notation",
  explanation="In Chen's E-R notation, entity sets are rectangles, relationships are diamonds, attributes are "
              "ellipses and multivalued attributes are double ellipses.",
  steps=["Entity = rectangle"],
  wrong="A diamond shows a relationship (e.g. Holds), an ellipse an attribute (e.g. Name), and a double ellipse a "
        "multivalued attribute (e.g. several phone numbers).", seconds=15)
Q(T, "Keys", "Basic",
  "In a bank's database, one customer can hold many accounts, but each account belongs to exactly one customer. "
  "What type of relationship exists between Customer and Account?",
  ["One-to-many", "One-to-one", "Many-to-many", "No relationship"],
  concept="Cardinality of relationships",
  explanation="One customer row is linked to many account rows, and each account row to one customer: one-to-many. "
              "It is implemented by putting the customer's primary key as a foreign key in the Account table.",
  steps=["Customer -> many accounts; account -> one customer = one-to-many"],
  wrong="One-to-one would allow only one account per customer. Many-to-many would let an account belong to many "
        "customers. The two tables are clearly related.", seconds=15)
o, a = ordered(0, [2, 3, 5])
Q(T, "SQL basics", "Advanced",
  "Table Branch has 5 rows; the manager column is NULL in 2 of them and holds a name in the other 3. What does "
  "this query return?\nSELECT COUNT(*) FROM Branch WHERE manager = NULL;", o, a,
  concept="Comparing with NULL",
  explanation="NULL means an unknown value, so manager = NULL is never true; it evaluates to UNKNOWN for every row, "
              "and WHERE keeps only rows where the condition is true. The count is 0. The correct test is "
              "WHERE manager IS NULL, which would return 2.",
  steps=["Any comparison with NULL using = gives UNKNOWN", "No row satisfies the WHERE", "COUNT(*) = 0"],
  wrong="2 is the answer for IS NULL. 3 counts rows with a manager. 5 counts every row.", seconds=40,
  computed=True)

# ================================================================ 11. MS Office (1 / 3 / 4)
T = "MS Office"
S_XL = "STIM_COMP_006002"
stimuli.append({
    "stimulus_id": S_XL, "type": "data_table", "title": "Excel sheet of staff deposit collections",
    "content": "An Excel sheet holds deposits mobilised by six officers (row 1 has headings):\n\n"
               "| Row | A (Officer) | B (Branch) | C (Deposits, Rs lakh) |\n|---|---|---|---|\n"
               + "\n".join(f"| {i + 2} | {n} | {b} | {d} |" for i, (n, b, d) in enumerate(SHEET)),
    "solution": "Pune values: 48, 55, 41 (sum 144, average 48). All values sum to 338; average 56.33. Descending "
                "order: 70, 62, 62, 55, 48, 41.",
})
o = ["48", "56.33", "144", "3"]
Q(T, "MS Excel", "Intermediate",
  "Refer to the Excel sheet. What does =AVERAGEIF(B2:B7, \"Pune\", C2:C7) return?", o,
  concept="AVERAGEIF",
  explanation="AVERAGEIF averages the cells of C2:C7 whose matching cell in B2:B7 is 'Pune': 48, 55 and 41. "
              "(48 + 55 + 41) / 3 = 144 / 3 = 48.",
  steps=["Pune rows: 2, 4, 6", "Values 48, 55, 41; sum 144", "Average = 144 / 3 = 48"],
  wrong="56.33 is the average of all six values. 144 is the SUMIF result. 3 is the COUNTIF result.", seconds=40,
  computed=True, stim=S_XL, pos=1,
  facts=[fact("Microsoft: AVERAGEIF returns the average (arithmetic mean) of all the cells in a range that meet a "
              "given criteria; syntax AVERAGEIF(range, criteria, [average_range]).", MS_AVGIF)])
o, a = ordered(RANK, [F(5, 2), 3, 4], fmt=lambda v: f"{float(v):g}")
Q(T, "MS Excel", "Advanced",
  "Refer to the Excel sheet. What does =RANK.EQ(C3, C2:C7) return?", o, a,
  concept="RANK.EQ with ties",
  explanation="With the order argument omitted, RANK.EQ ranks in descending order. C3 = 62. Only one value (70) is "
              "larger, so 62 gets rank 2. John's 62 is tied and also gets rank 2 (tied values share the top rank "
              "of the group); the next value, 55, gets rank 4.",
  steps=["Descending: 70, 62, 62, 55, 48, 41", "Values greater than 62: one (70)", "Rank = 1 + 1 = 2"],
  wrong="2.5 is what RANK.AVG gives for the tie. 3 would skip the tie rule. 4 is the rank in ascending order.",
  seconds=40, computed=True, stim=S_XL, pos=2,
  facts=[fact("Microsoft RANK.EQ: if order is 0 or omitted, Excel ranks number as if ref were sorted in descending "
              "order; if more than one value has the same rank, the top rank of that set is returned.", MS_RANK)])
o, a = ordered(ABOVE, [0, 2, 4])
Q(T, "MS Excel", "Advanced",
  "Refer to the Excel sheet. What does =COUNTIF(C2:C7, \">\"&AVERAGE(C2:C7)) return?", o, a,
  concept="COUNTIF with a calculated criterion",
  explanation="The & operator joins \">\" with the result of AVERAGE(C2:C7) = 338 / 6 = 56.33, giving the "
              "criterion \">56.33\". Values above it are 62, 62 and 70, so the count is 3.",
  steps=["AVERAGE = 338 / 6 = 56.33", "Criterion = \">56.33\"", "62, 62, 70 qualify -> 3"],
  shortcut="Put the operator in quotes and join the calculated value with &.",
  wrong="0 is what you get if the whole criterion is typed as text \">AVERAGE(C2:C7)\", which matches nothing. 2 "
        "counts the tied 62s only once. 4 wrongly includes 55.", seconds=50, computed=True, stim=S_XL, pos=3,
  facts=[fact("Microsoft COUNTIF: in =COUNTIF(B2:B5,\"<>\"&B4) the ampersand merges the comparison operator with "
              "the value in B4.", MS_COUNTIF)])
Q(T, "MS Word", "Basic",
  "A clerk wants the bank's name and the document title to appear automatically at the top of every page of a "
  "30-page Word report. Which feature should she use?",
  ["Header", "Footnote", "Watermark", "Page break"],
  concept="Headers and footers",
  explanation="A header is an area in the top margin whose content repeats on every page (or every page of a "
              "section). A footer does the same at the bottom.",
  steps=["Same text at the top of every page = header"],
  wrong="A footnote is a note at the bottom of one page tied to a reference mark. A watermark is faint text or "
        "an image behind the page text. A page break starts a new page.", seconds=10)
Q(T, "MS Excel", "Intermediate",
  "In a loan-entry sheet, the Branch column must accept only Pune, Delhi or Agra, chosen from a drop-down list, so "
  "that clerks cannot type wrong names. Which Excel feature should be applied to the column?",
  ["Data Validation", "Conditional Formatting", "Freeze Panes", "Goal Seek"],
  concept="Restricting cell entries",
  explanation="Data Validation (Data tab) restricts what can be entered in cells, for example a list of allowed "
              "values shown as a drop-down, a number range or a date range, and shows an error for invalid "
              "entries.",
  steps=["Allow only listed values with a drop-down = Data Validation (List)"],
  wrong="Conditional Formatting only changes how cells look. Freeze Panes keeps rows or columns visible while "
        "scrolling. Goal Seek finds an input value for a target result.", seconds=20,
  facts=[fact("Microsoft: use data validation to restrict the type of data or the values that users enter into a "
              "cell, like a dropdown list.", MS_DV)])
Q(T, "MS Word", "Intermediate",
  "A 120-page credit-policy document must have a contents page listing every chapter and section with its page "
  "number, which can be refreshed after the text is edited. What must be done to the chapter and section titles "
  "so that Word can build this automatically?",
  ["Format them with built-in Heading styles (Heading 1, Heading 2 ...)", "Type them in bold capital letters",
   "Insert a page break before each of them", "Add each of them as a footnote"],
  concept="Automatic table of contents",
  explanation="Word builds an automatic table of contents from text formatted with Heading styles. After edits, "
              "Update Table refreshes the entries and page numbers.",
  steps=["Apply Heading styles -> References > Table of Contents -> update when needed"],
  wrong="Bold capitals only change appearance; Word does not treat them as headings. Page breaks and footnotes do "
        "not mark text as headings.", seconds=25,
  facts=[fact("Microsoft: Word uses the headings in your document to build an automatic table of contents that "
              "can be updated when you change the heading text, sequence or level.", MS_TOC)])
o, a = ordered(DAYS, [89, 91, 92])
Q(T, "MS Excel", "Advanced",
  "A1 contains the date 15-Jan-2026 and B1 contains 15-Apr-2026. C1 holds =B1-A1 and is formatted as Number with "
  "no decimals. What does C1 show?", o, a,
  concept="Date arithmetic in Excel",
  explanation="Excel stores dates as serial numbers (one per day), so subtracting two dates gives the number of "
              "days between them. Jan 15 to Apr 15, 2026 = 16 (rest of January) + 28 (February 2026 is not a leap "
              "year) + 31 (March) + 15 (April) = 90 days.",
  steps=["Jan: 31 - 15 = 16", "Feb 2026: 28", "Mar: 31", "Apr: 15", "Total = 90"],
  wrong="91 counts both the start and the end date, or treats February 2026 as having 29 days. 89 and 92 come "
        "from other month-length slips.", seconds=40, computed=True,
  facts=[fact("Microsoft DATE function: Excel stores dates as sequential serial numbers so that they can be used "
              "in calculations; January 1, 1900 is serial number 1.", MS_DATE)])
Q(T, "MS PowerPoint", "Advanced",
  "A bank wants a PowerPoint presentation about its deposit schemes to play by itself in a loop on a screen in "
  "the branch lobby, with full-screen display and no presenter, until someone presses Esc. Which Set Up Slide Show "
  "option should be chosen?",
  ["Browsed at a kiosk (full screen)", "Presented by a speaker (full screen)", "Browsed by an individual (window)",
   "Presenter View"],
  concept="Self-running presentations",
  explanation="'Browsed at a kiosk (full screen)' loops the slide show until Esc is pressed and stops viewers from "
              "changing slides by clicking; slides should have rehearsed timings so they advance automatically.",
  steps=["Unattended, looping, full screen = Browsed at a kiosk"],
  wrong="'Presented by a speaker' expects a presenter to advance slides. 'Browsed by an individual' opens the show "
        "in a window. Presenter View shows notes to a speaker on a second screen.", seconds=25,
  facts=[fact("Microsoft: Browsed at a kiosk (full screen) loops your slide show until the person watching presses "
              "Esc.", MS_KIOSK)])

# ================================================================ 12. Digital Payments (1 / 2 / 2)
T = "Digital Payments"
Q(T, "Card security", "Basic",
  "After scanning a merchant's QR code and entering the amount in a UPI app, what secret does the customer enter "
  "to authorise the payment from his bank account?",
  ["UPI PIN", "Card CVV", "IFSC code", "Customer ID"],
  concept="Authorising UPI payments",
  explanation="Every standard UPI payment is authorised with the UPI PIN, a secret number set by the customer for "
              "the linked bank account. It should never be shared, and it is not needed to receive money.",
  steps=["Authorise UPI debit = UPI PIN"],
  wrong="The CVV is used for card payments. The IFSC identifies a bank branch and is not secret. A customer ID is "
        "an identifier, not a payment authorisation.", seconds=10)
Q(T, "Payment technology", "Intermediate",
  "A customer loads a small balance into an on-device wallet in her UPI app so that she can make quick, small-"
  "value payments (such as for tea or bus tickets) without entering the UPI PIN for each one. Which NPCI feature "
  "is this?",
  ["UPI Lite", "UPI 123PAY", "AePS", "NACH"],
  concept="Small-value UPI payments",
  explanation="UPI Lite is an on-device wallet for small-value UPI payments. Money is loaded into it (with the UPI "
              "PIN), and small payments from it do not need the PIN each time, which also reduces load on banks' "
              "core systems.",
  steps=["On-device wallet, small payments without PIN = UPI Lite"],
  wrong="UPI 123PAY is UPI for feature phones. AePS allows Aadhaar-and-biometric transactions at micro-ATMs. "
        "NACH handles bulk and recurring debits and credits.", seconds=20, web=SC,
  facts=[fact("NPCI circular UPI OC 138 introduced UPI Lite, an on-device wallet for small-value transactions.",
              NPCI_LITE)])
Q(T, "Payment technology", "Intermediate",
  "An online shop wants to accept card and net-banking payments. It needs a service that securely carries the "
  "customer's payment details from its checkout page to the banks and card networks for authorisation and returns "
  "the result to the website. What is this service called?",
  ["Payment gateway", "Domain name server", "Content delivery network", "Web browser"],
  concept="Online payment infrastructure",
  explanation="A payment gateway is the technology layer between a merchant's website or app and the acquiring "
              "bank / card networks. It encrypts and forwards payment data for authorisation and sends the "
              "approval or decline back.",
  steps=["Carries payment data from website to banks and back = payment gateway"],
  wrong="A DNS server maps names to IP addresses. A CDN serves website files from nearby servers. A browser is the "
        "customer's software for viewing pages.", seconds=20)
Q(T, "Card security", "Advanced",
  "Under the ISO/IEC 7812 numbering scheme, the leading digits of a payment card number identify the institution "
  "that issued the card, which lets a terminal route the transaction to the right network and issuer. What are "
  "these leading digits called?",
  ["Issuer Identification Number (IIN), also called BIN", "Card Verification Value (CVV)",
   "Personal Identification Number (PIN)", "International Bank Account Number (IBAN)"],
  concept="Structure of a card number",
  explanation="A card number begins with the IIN (often called the Bank Identification Number, BIN), whose first "
              "digit is the Major Industry Identifier. Then come the issuer-assigned account digits, and the last "
              "digit is the Luhn check digit.",
  steps=["Leading digits that identify the issuer = IIN / BIN"],
  wrong="The CVV is a separate security code, not part of the card number. The PIN is a secret known only to the "
        "cardholder. The IBAN is an international bank account number format, not a card number part.",
  seconds=25, web=SC,
  facts=[fact("ISO/IEC 7812: the first six or eight digits of a card number, including the major industry "
              "identifier, compose the issuer identification number (IIN), which identifies the issuing "
              "organisation.", ISO7812)])
Q(T, "Payment technology", "Advanced",
  "A shop that accepts debit and credit cards finds that, for each card sale, its bank keeps a small percentage of "
  "the amount as a fee before crediting the rest to the shop's account. What is this fee called?",
  ["Merchant Discount Rate (MDR)", "Marginal Standing Facility (MSF) rate", "Cash Reserve Ratio (CRR)",
   "Interchange Settlement Number (ISN)"],
  concept="Cost of accepting digital payments",
  explanation="The MDR is charged to the merchant by the acquiring bank for card-payment services, usually as a "
              "percentage of the transaction amount. It is shared among the acquirer, the issuer (interchange) and "
              "the card network.",
  steps=["Fee a merchant pays its bank per card transaction = MDR"],
  wrong="MSF and CRR are RBI monetary-policy instruments for banks, not merchant fees. 'Interchange Settlement "
        "Number' is not a payment term.", seconds=20, web=SC,
  facts=[fact("MDR is the fee charged to a merchant by a bank for providing debit and credit card payment "
              "facilities, usually a percentage of the transaction amount.", MDR_SRC)])

# ================================================================ 13. Computer Abbreviations (3 / 5 / 2)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic",
  "The firmware of a computer is stored in ROM, whose contents are not lost when the power is switched off. What "
  "does ROM stand for?",
  ["Read-Only Memory", "Random Operating Memory", "Rapid Output Module", "Readable Optical Media"],
  concept="Memory abbreviations",
  explanation="ROM (Read-Only Memory) is non-volatile memory whose contents are written at manufacture or by "
              "special programming, and are normally only read during use.",
  steps=["ROM = Read-Only Memory"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic",
  "At an ATM, a customer types a secret 4-digit number to prove that the card is his. This number is the PIN. What "
  "does PIN stand for?",
  ["Personal Identification Number", "Private Internet Number", "Payment Instruction Note",
   "Protected Index Number"],
  concept="Banking-technology abbreviations",
  explanation="A PIN (Personal Identification Number) is a secret numeric code that authenticates the cardholder "
              "('something you know').",
  steps=["PIN = Personal Identification Number"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic",
  "Every device on the internet is given an IP address, such as 192.168.1.10. What does IP stand for here?",
  ["Internet Protocol", "Internal Port", "Information Packet", "Interface Program"],
  concept="Networking abbreviations",
  explanation="IP (Internet Protocol) is the network-layer protocol that addresses and routes packets between "
              "networks; an IP address identifies a device's network interface.",
  steps=["IP = Internet Protocol"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "The internet service that converts a website name such as www.bank.example into its IP address is DNS. What "
  "does DNS stand for?",
  ["Domain Name System", "Digital Network Service", "Data Naming Server", "Dynamic Node Switching"],
  concept="Internet abbreviations",
  explanation="DNS (Domain Name System) is the distributed, hierarchical directory that maps domain names to IP "
              "addresses and other records.",
  steps=["DNS = Domain Name System"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "A bank uses CRM software to record every customer's enquiries, complaints and product holdings so that "
  "relationship managers can offer suitable products. What does CRM stand for?",
  ["Customer Relationship Management", "Central Records Monitor", "Credit Risk Model", "Client Response Machine"],
  concept="Business-software abbreviations",
  explanation="CRM (Customer Relationship Management) software manages an organisation's interactions with its "
              "customers: contact history, leads, service requests and sales opportunities.",
  steps=["CRM = Customer Relationship Management"],
  wrong="The other expansions are not what CRM means in business software.", seconds=10)
Q(T, S, "Intermediate",
  "Because of CBS, a customer can deposit or withdraw money at any branch of his bank, not only at his home "
  "branch, since all branches work on one centralised system. What does CBS stand for?",
  ["Core Banking Solution", "Central Branch Server", "Customer Banking Service", "Computerised Bank Settlement"],
  concept="Banking-technology abbreviations",
  explanation="CBS (Core Banking Solution) runs a bank's accounts and transactions on central servers in a data "
              "centre, so every branch and channel works on the same up-to-date data ('anywhere banking').",
  steps=["CBS = Core Banking Solution"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "SIM swap fraud tricks a mobile operator into issuing a new SIM for a customer's number. What does SIM stand "
  "for?",
  ["Subscriber Identity Module", "Secure Internet Mobile", "System Information Memory", "Signal Interface Modem"],
  concept="Mobile abbreviations",
  explanation="The SIM (Subscriber Identity Module) card securely stores the subscriber's identity and keys that "
              "the mobile network uses to authenticate the phone number.",
  steps=["SIM = Subscriber Identity Module"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "A bank uses ERP software to run its internal functions, such as HR, payroll, procurement and fixed-asset "
  "accounting, on one integrated system. What does ERP stand for?",
  ["Enterprise Resource Planning", "Electronic Records Processing", "External Reporting Platform",
   "Enterprise Risk Protection"],
  concept="Business-software abbreviations",
  explanation="ERP (Enterprise Resource Planning) software integrates an organisation's core business processes "
              "(finance, HR, purchasing, inventory) around one shared database.",
  steps=["ERP = Enterprise Resource Planning"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Advanced",
  "Email was designed for plain text; the standard that lets an email carry attachments such as PDF statements, "
  "images and non-English text is MIME. What does MIME stand for?",
  ["Multipurpose Internet Mail Extensions", "Multimedia Internet Message Encoding", "Mail Integrity and Message "
   "Encryption", "Multiple Inbox Mail Exchange"],
  concept="Email abbreviations",
  explanation="MIME (Multipurpose Internet Mail Extensions) defines how email messages carry non-text attachments, "
              "multiple parts and character sets. Its media types (such as application/pdf) are also used on the "
              "web.",
  steps=["MIME = Multipurpose Internet Mail Extensions"], wrong="The other expansions are made up.", seconds=15)
Q(T, S, "Advanced",
  "A bank's network team monitors the status, traffic and errors of all its routers and switches from one console "
  "using the SNMP protocol. What does SNMP stand for?",
  ["Simple Network Management Protocol", "Secure Node Monitoring Process", "Standard Network Mapping Program",
   "Switched Network Message Protocol"],
  concept="Networking abbreviations",
  explanation="SNMP (Simple Network Management Protocol) lets a management station read and set information on "
              "network devices and receive alerts (traps) from them.",
  steps=["SNMP = Simple Network Management Protocol"], wrong="The other expansions are made up.", seconds=15)

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_006_plan.json").read_text(encoding="utf-8"))
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
    pos = sorted(q["set_position"] for q in questions if q.get("stimulus_id") == s["stimulus_id"])
    assert pos == list(range(1, len(pos) + 1)) and 3 <= len(pos) <= 6, (s["stimulus_id"], pos)
keys = Counter(q["correct_answer"] for q in questions)
assert max(keys.values()) <= 28 and min(keys.values()) >= 22, keys

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_006",
    "created_at": TODAY,
    "notes": "BATCH_006 Computer Knowledge part: 100 original, mostly scenario-based questions (BANK_COMP_000503 to "
             "BANK_COMP_000602) with two shared data tables (STIM_COMP_006001 SQL Loans table, STIM_COMP_006002 "
             "Excel deposits sheet). Computable answers (fractional binary, hex code space, 0.1 + 0.2 float error, "
             "weighted CPI, SSTF/FCFS disk-head movement, photo capacity, Mbps to MB/s, Hamming check bits, route "
             "summarisation, propagation delay, OTP guess probability, key counts, XOR cipher, SQL via sqlite3, "
             "Excel AVERAGEIF/RANK.EQ/COUNTIF and date difference) are re-derived in tools/batch_006/computer.py. "
             "Alt+Tab, Safe Mode, mv, sudo, AVERAGEIF, RANK.EQ, COUNTIF with &, Excel date serials, Data "
             "Validation, Word TOC, PowerPoint kiosk mode, WebSocket (RFC 6455), Access-Control-Allow-Origin, IPv4 "
             "TTL (RFC 791) and the MITRE ATT&CK descriptions of watering hole, MFA fatigue and password spraying "
             "were checked on the cited pages on 2026-11-05; the OEM licence rule, UPI Lite, IIN and MDR were "
             "confirmed from search results only (web:search-confirmed).",
    "stimuli": stimuli,
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_006_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
