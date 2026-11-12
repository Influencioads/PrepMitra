"""Writes batches/parts/BATCH_005_COMP.json: the 100 Computer Knowledge questions of BATCH_005.

Every computable answer (sign-magnitude code, ASCII offset, two's-complement overflow, IEEE 754 exponent field via
struct, clock multiplier, little-endian byte order via struct, aspect ratio, webcam data rate, SRTF / SJF / FCFS
waiting times, FIFO page faults for Belady's anomaly, page-table size, QLC charge levels, collision and broadcast
domains, SQL LIKE and UNION / UNION ALL via sqlite3, Excel IFERROR, MOD and COUNTIF with wildcards) is re-derived
below with assertions before the file is written. The plan quota per (topic, difficulty), subtopics, the ID range
and the answer-key balance are also asserted. If any assertion fails, nothing is written.

    python tools/batch_005/computer.py      (run from docs/question-bank)
"""

import json
import math
import random
import re
import sqlite3
import struct
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
FIRST_ID = 403
AI = ("ai:author-solve", "ai:independent-check")
COMPUTED = ("script:recompute", "ai:author-solve", "ai:independent-check")

_rng = random.Random(20261105 + 5)
_keys = Counter()
questions = []


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


def ordered(correct, distractors, fmt=str):
    """Numeric options in ascending order; returns (option texts, answer letter)."""
    vals = sorted([correct] + list(distractors))
    assert len(set(vals)) == 4, vals
    return [fmt(v) for v in vals], LETTERS[vals.index(correct)]


def Q(topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, wrong, seconds=30,
      shortcut=None, computed=False, facts=None, web="web:fact-check"):
    """Adds one question. With answer=None, options[0] is the correct text and it is placed at the least-used key
    so far (random tie-break, fixed seed). Ordered options (numbers) pass an explicit answer letter.
    web is 'web:fact-check' (page opened) or 'web:search-confirmed' (confirmed only in search results)."""
    assert len(options) == 4 and len(set(options)) == 4, text
    if answer is None:
        low = min(_keys[k] for k in LETTERS)
        pos = LETTERS.index(_rng.choice([k for k in LETTERS if _keys[k] == low]))
        correct, wrongs = options[0], list(options[1:])
        options = wrongs[:pos] + [correct] + wrongs[pos:]
        answer = LETTERS[pos]
    assert answer in LETTERS
    _keys[answer] += 1
    qid = f"BANK_COMP_{FIRST_ID + len(questions):06d}"
    vb = list(COMPUTED if computed else AI)
    v = {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
         "verified_by": vb, "verified_at": TODAY}
    if facts:
        vb.append(web)
        v["fact_checks"] = facts
    questions.append({
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
    })


# ---------------------------------------------------------------- verification of computable answers
# Sign-magnitude, one's and two's complement of -37 in 8 bits
assert format(37, "08b") == "00100101"
SIGN_MAG = "1" + format(37, "07b")
ONES = format(~37 & 0xFF, "08b")
TWOS = format(-37 & 0xFF, "08b")
assert (SIGN_MAG, ONES, TWOS) == ("10100101", "11011010", "11011011")
# ASCII: 'A' = 65, lowercase = uppercase + 32
assert ord("A") == 65 and ord("e") == 101 and ord("E") == 69 and ord("d") == 100 and ord("a") - ord("A") == 32


# Two's-complement 8-bit overflow: 100 + 50
def s8(bits):
    v = int(bits, 2)
    return v - 256 if v >= 128 else v


OVF = format((100 + 50) & 0xFF, "08b")
assert OVF == "10010110" and s8(OVF) == -106 and 100 + 50 > 127
# IEEE 754 single precision: exponent field of 6.5 = 1.101 x 2^2 -> 2 + 127 = 129
BITS65 = format(struct.unpack(">I", struct.pack(">f", 6.5))[0], "032b")
assert BITS65[0] == "0" and BITS65[1:9] == "10000001" == format(129, "08b") and BITS65[9:].startswith("101")
# Clock multiplier: 100 MHz x 36
assert 100 * 36 == 3600
# Little-endian storage of 0x12345678 at addresses 100..103
LE = struct.pack("<I", 0x12345678)
assert LE[1] == 0x56 and LE[0] == 0x78 and LE[3] == 0x12
# Aspect ratio of 1680 x 1050
g = math.gcd(1680, 1050)
assert (1680 // g, 1050 // g) == (8, 5) and F(1680, 1050) == F(16, 10)
# Webcam: 1280 x 720, 24-bit, 30 fps, uncompressed
FRAME = 1280 * 720 * 3
assert FRAME == 2_764_800 and FRAME * 30 == 82_944_000 and 1280 * 720 * 30 == 27_648_000
assert FRAME * 30 * 8 == 663_552_000


# CPU scheduling: P1 (0, 7), P2 (2, 4), P3 (4, 1), P4 (5, 4)
PROCS = {"P1": (0, 7), "P2": (2, 4), "P3": (4, 1), "P4": (5, 4)}


def srtf(procs):
    rem = {p: b for p, (a, b) in procs.items()}
    t, done = 0, {}
    while rem:
        ready = [p for p in rem if procs[p][0] <= t]
        if not ready:
            t += 1
            continue
        best = min(rem[p] for p in ready)
        assert sum(1 for p in ready if rem[p] == best) == 1, ("tie", t)  # no ties in this data
        p = next(p for p in ready if rem[p] == best)
        rem[p] -= 1
        t += 1
        if rem[p] == 0:
            del rem[p]
            done[p] = t
    return F(sum(done[p] - a - b for p, (a, b) in procs.items()), len(procs))


def nonpreemptive(procs, key):
    t, waits, left = 0, [], dict(procs)
    while left:
        ready = [p for p in left if left[p][0] <= t]
        p = min(ready, key=lambda q: key(q, left[q]))
        a, b = left.pop(p)
        waits.append(t - a)
        t += b
    return F(sum(waits), len(waits))


SRTF = srtf(PROCS)
SJF = nonpreemptive(PROCS, lambda p, ab: (ab[1], ab[0]))
FCFS = nonpreemptive(PROCS, lambda p, ab: (ab[0],))
assert (SRTF, SJF, FCFS) == (3, 4, F(19, 4))


# Belady's anomaly with FIFO
def fifo_faults(refs, frames):
    mem, faults = [], 0
    for r in refs:
        if r not in mem:
            faults += 1
            if len(mem) == frames:
                mem.pop(0)
            mem.append(r)
    return faults


BELADY = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
assert fifo_faults(BELADY, 3) == 9 and fifo_faults(BELADY, 4) == 10
# Page table: 32-bit virtual address, 4 KiB pages, 4-byte entries
ENTRIES = 2 ** 32 // 2 ** 12
assert ENTRIES == 2 ** 20 and ENTRIES * 4 == 4 * 2 ** 20
# QLC: 4 bits per cell -> 2^4 charge levels
assert 2 ** 4 == 16 and 2 ** 3 == 8
# Domains: router joins two 16-port switches, every port used (15 PCs + 1 router uplink each)
BCAST, COLL = 2, 16 + 16
assert (BCAST, COLL) == (2, 32)

# SQL
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Customer (name TEXT)")
db.executemany("INSERT INTO Customer VALUES (?)", [(n,) for n in ["Asha", "Ravi", "Rahul", "Karan", "Arjun", "Raman"]])
LIKE_N = db.execute("SELECT COUNT(*) FROM Customer WHERE name LIKE '_a%'").fetchone()[0]
assert LIKE_N == 4
assert db.execute("SELECT COUNT(*) FROM Customer WHERE name LIKE 'a%'").fetchone()[0] == 2
assert db.execute("SELECT COUNT(*) FROM Customer WHERE name LIKE '%a%'").fetchone()[0] == 6
db.execute("CREATE TABLE Savings (cust TEXT)")
db.execute("CREATE TABLE Loans (cust TEXT)")
db.executemany("INSERT INTO Savings VALUES (?)", [(n,) for n in ["Asha", "Ravi", "Meena", "John"]])
db.executemany("INSERT INTO Loans VALUES (?)", [(n,) for n in ["Ravi", "John", "Farah"]])
U = db.execute("SELECT COUNT(*) FROM (SELECT cust FROM Savings UNION SELECT cust FROM Loans)").fetchone()[0]
UA = db.execute("SELECT COUNT(*) FROM (SELECT cust FROM Savings UNION ALL SELECT cust FROM Loans)").fetchone()[0]
INTERSECT = db.execute("SELECT COUNT(*) FROM (SELECT cust FROM Savings INTERSECT SELECT cust FROM Loans)").fetchone()[0]
assert (U, UA, INTERSECT) == (5, 7, 2)
# Excel MOD: result has the sign of the divisor (= Python's %)
assert -7 % 3 == 2 and math.fmod(-7, 3) == -1
# Excel COUNTIF wildcards (case-insensitive): "S?n*"
NAMES = ["Sharma", "Singh", "Asha", "Suresh", "Kumar", "Sinha"]
WILD = sum(1 for n in NAMES if re.fullmatch(r"s.n.*", n, re.I))
assert WILD == 2 and sum(1 for n in NAMES if re.fullmatch(r"s.*", n, re.I)) == 4
# IFERROR(5000/0, "NA") -> "NA" because 5000/0 is #DIV/0!
try:
    5000 / 0
    raise AssertionError
except ZeroDivisionError:
    pass

# ---------------------------------------------------------------- fact-check sources
# Pages opened on 2026-11-05 (web:fact-check)
MS_WIN = "https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec"
MS_WORD = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2"
MS_EXCEL = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-9b7213f0040f"
MS_PRESENTER = ("https://support.microsoft.com/en-us/office/start-the-presentation-and-see-your-notes-in-presenter-"
                "view-4de90e28-487e-435c-9401-eb49a3801257")
MS_MOD = "https://support.microsoft.com/en-us/office/mod-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3"
MS_COUNTIF = "https://support.microsoft.com/en-us/office/countif-function-e0de10c6-f885-4e71-abb4-1f464816df34"
MS_IFERROR = "https://support.microsoft.com/en-us/office/iferror-function-c526fd07-caeb-47b8-8bb6-63f3e417f611"
MS_NAME = "https://support.microsoft.com/en-us/office/how-to-correct-a-name-error-b6d54e31-a743-4d7d-9b61-40002a7b4286"
MS_GOAL = ("https://support.microsoft.com/en-us/office/use-goal-seek-to-find-the-result-you-want-by-adjusting-an-"
           "input-value-320cb99e-f4a4-417f-b1c3-4f369d6e66c7")
MDN_STATUS = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status"
MDN_HSTS = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security"
RFC7489 = "https://www.rfc-editor.org/rfc/rfc7489"
RFC9114 = "https://www.rfc-editor.org/rfc/rfc9114"
RFC9000 = "https://www.rfc-editor.org/rfc/rfc9000"
RFC8551 = "https://www.rfc-editor.org/rfc/rfc8551"
RFC8200 = "https://www.rfc-editor.org/rfc/rfc8200"
RFC1035 = "https://www.rfc-editor.org/rfc/rfc1035"
NIST_HSM = "https://csrc.nist.gov/glossary/term/hardware_security_module_hsm"
IT_66D = "https://lawx.in/acts/section/17/224/2231"
CENSUS = ("https://www.census.gov/about/history/bureau-history/census-innovations/technology/"
          "tabulation-and-processing.html")
CHM_MOORE = "https://www.computerhistory.org/revolution/digital-logic/12/267"
ANDROID_HCE = "https://developer.android.com/develop/connectivity/nfc/hce"
# Confirmed only in search results (web:search-confirmed)
MS_LANDSCAPE = "https://support.microsoft.com/en-us/word/print-with-landscape-orientation-in-word"
IEEE_OUI = "https://standards.ieee.org/products-services/regauth/oui/"
NPCI_123PAY = "https://npci.org.in/what-we-do/upi-123pay/product-overview"
SC = "web:search-confirmed"

# ================================================================ 1. Computer Fundamentals (2 / 4 / 3)
T = "Computer Fundamentals"
Q(T, "Generations and history", "Basic",
  "Who wrote what is regarded as the first published computer program, a method for calculating Bernoulli numbers "
  "on Charles Babbage's Analytical Engine?",
  ["Ada Lovelace", "Blaise Pascal", "Alan Turing", "John von Neumann"],
  concept="Pioneers of computing",
  explanation="In 1843 Ada Lovelace published notes on Babbage's Analytical Engine that included a step-by-step "
              "method for computing Bernoulli numbers on the machine. It is regarded as the first published "
              "computer program, so she is often called the first computer programmer.",
  steps=["Program for Babbage's Analytical Engine = Ada Lovelace"],
  wrong="Blaise Pascal built a mechanical adding machine (the Pascaline) in the 1640s. Alan Turing described the "
        "Turing machine in 1936. John von Neumann described the stored-program architecture in 1945.", seconds=15)
Q(T, "Types of computers", "Basic",
  "Desktops, laptops and tablets are general-purpose computers built around a single microprocessor and meant for "
  "one user at a time. In the size-based classification of computers, they are:",
  ["Microcomputers", "Minicomputers", "Mainframe computers", "Supercomputers"],
  concept="Classification of computers by size",
  explanation="By size and power, computers are grouped as supercomputers, mainframes, minicomputers and "
              "microcomputers. Microcomputers (personal computers) use a microprocessor as their CPU and are built "
              "for a single user; desktops, laptops, tablets and smartphones belong here.",
  steps=["Single microprocessor + one user = microcomputer (personal computer)"],
  wrong="Minicomputers were mid-sized multi-user machines for departments. Mainframes serve thousands of users at "
        "once. Supercomputers are the fastest machines, used for scientific simulation.", seconds=15)
Q(T, "Number systems", "Intermediate",
  "In 8-bit sign-magnitude representation, the leftmost bit is the sign (1 for negative) and the remaining 7 bits "
  "hold the magnitude. How is -37 written?",
  ["10100101", "11011011", "11011010", "00100101"],
  concept="Sign-magnitude representation",
  explanation="37 in 7 bits is 0100101. Putting the sign bit 1 in front gives 1 0100101 = 10100101. Sign-magnitude "
              "is the simplest signed code, but it has two zeros (00000000 and 10000000), which is why computers use "
              "two's complement for arithmetic.",
  steps=["37 = 32 + 4 + 1 = 0100101 (7 bits)", "Negative -> sign bit 1", "-37 = 10100101"],
  wrong="11011011 is the two's complement of -37 and 11011010 its one's complement. 00100101 is +37.",
  seconds=35, computed=True)
o, a = ordered(101, [37, 69, 100])
Q(T, "Number systems", "Intermediate",
  "In the ASCII code, the capital letter 'A' has the decimal code 65. What is the decimal ASCII code of the small "
  "letter 'e'?", o, a,
  concept="ASCII codes of letters",
  explanation="ASCII codes the capital letters A to Z as 65 to 90 and the small letters a to z as 97 to 122. Each "
              "small letter is exactly 32 more than its capital. 'E' = 65 + 4 = 69, so 'e' = 69 + 32 = 101.",
  steps=["'E' = 65 + 4 = 69", "Small letter = capital + 32", "'e' = 69 + 32 = 101"],
  shortcut="Remember 'A' = 65 and 'a' = 97; then count forward.",
  wrong="69 is capital 'E'. 100 is 'd' (one letter short). 37 subtracts 32 instead of adding it.",
  seconds=30, computed=True)
Q(T, "Generations and history", "Intermediate",
  "For the 1890 United States census, Herman Hollerith's machines read each person's data from cards and counted "
  "the results electrically. How was the data stored on these cards?",
  ["As holes punched in the cards", "On a magnetic stripe", "In vacuum-tube memory", "As printed barcodes"],
  concept="Punched-card tabulation",
  explanation="Hollerith's tabulating machine used specially encoded punched cards, one per person; electrical "
              "contacts passing through the holes advanced counters. The census office leased the machines for the "
              "1890 count. Hollerith's company later became part of IBM, and punched cards remained the main input "
              "medium for decades.",
  steps=["Hollerith, 1890 census = punched cards"],
  wrong="Magnetic stripes, vacuum-tube memory and barcodes all came decades later.", seconds=20,
  facts=[fact("US Census Bureau: Hollerith's machine used specially encoded punch cards, each representing an "
              "individual's census data; the Census Office leased the machines for the 1890 census count.", CENSUS)])
Q(T, "Types of computers", "Intermediate",
  "Tellers in a bank use low-cost desktop devices with little local storage. The banking application and data run "
  "on a central server, and the device mainly shows the screen and sends keyboard and mouse input. Such a device "
  "is called a:",
  ["Thin client", "Workstation", "Supercomputer", "Standalone computer"],
  concept="Thin clients",
  explanation="A thin client depends on a server for processing and storage; it only handles display and input. "
              "It is cheap to manage and secure, because data stays on the central server, which suits branches "
              "with many identical counters.",
  steps=["Processing on a central server, device only displays = thin client"],
  wrong="A workstation is a powerful machine that does heavy work locally. A supercomputer is for large scientific "
        "calculations. A standalone computer works on its own without depending on a server.", seconds=20)
Q(T, "Number systems", "Advanced",
  "Two signed numbers, 100 (01100100) and 50 (00110010), are added in an 8-bit two's-complement register. What does "
  "the register hold, and how should the result be read?",
  ["10010110, which reads as -106 because the true sum overflowed the 8-bit range",
   "10010110, which correctly reads as +150",
   "00010110, which reads as +22 after the carry is discarded",
   "11101010, which reads as -22"],
  concept="Overflow in two's-complement addition",
  explanation="8-bit two's complement holds -128 to +127. The true sum 150 is outside this range. Binary addition "
              "gives 01100100 + 00110010 = 10010110. Its sign bit is 1, so it is read as 150 - 256 = -106. Adding two "
              "positive numbers and getting a negative result is the sign of overflow.",
  steps=["01100100 + 00110010 = 10010110", "Sign bit 1 -> value = 150 - 256 = -106",
         "150 > 127 -> overflow (two positives gave a negative)"],
  shortcut="Overflow happens only when two numbers of the same sign give a result of the opposite sign.",
  wrong="+150 cannot be held in signed 8 bits. There is no carry out of bit 7 here, so nothing is discarded to give "
        "00010110. 11101010 is not the bit pattern produced by the addition.",
  seconds=50, computed=True)
Q(T, "Number systems", "Advanced",
  "In IEEE 754 single precision (1 sign bit, 8 exponent bits with a bias of 127, 23 fraction bits), the number 6.5 "
  "is stored. What is in its 8-bit exponent field?",
  ["10000001", "00000010", "10000010", "01111111"],
  concept="IEEE 754 floating point",
  explanation="6.5 = 110.1 in binary = 1.101 x 2^2. The true exponent is 2, and the stored exponent is 2 + 127 = "
              "129 = 10000001. The fraction field holds 101 followed by zeros (the leading 1 is implicit), and the "
              "sign bit is 0.",
  steps=["6.5 = 110.1 (binary)", "= 1.101 x 2^2", "Stored exponent = 2 + 127 = 129", "129 = 10000001"],
  wrong="00000010 is the unbiased exponent 2. 10000010 (130) counts one place too many. 01111111 (127) is the bias "
        "itself, which would mean an exponent of 0.", seconds=60, computed=True)
Q(T, "Generations and history", "Advanced",
  "In 1975 Gordon Moore revised his famous forecast about integrated circuits. What did the revised 'Moore's law' "
  "predict?",
  ["The number of components on a chip would double about every two years",
   "Processor clock speed would double every year",
   "The price of memory would halve every six months",
   "Hard disk capacity would grow tenfold every decade"],
  concept="Moore's law",
  explanation="In 1965 Moore forecast that the number of components on an integrated circuit would double every "
              "year. In 1975, with new data, he revised this to doubling about every two years. The revised "
              "forecast became a target for the chip industry for decades.",
  steps=["1965: doubling every year", "1975 revision: chip density doubles every two years"],
  wrong="Moore's law is about transistor (component) count on a chip, not clock speed, memory prices or disk "
        "capacity. The popular '18 months' figure is a later restatement about performance, not Moore's own.",
  seconds=25,
  facts=[fact("Computer History Museum: with new data, in 1975 Moore revised his prediction, forecasting that IC "
              "density would double every two years.", CHM_MOORE)])

# ================================================================ 2. Hardware (3 / 4 / 2)
T = "Hardware"
Q(T, "CPU and components", "Basic",
  "Which CPU register holds the instruction that is currently being decoded and executed?",
  ["Instruction Register (IR)", "Program Counter (PC)", "Memory Address Register (MAR)", "Stack Pointer (SP)"],
  concept="CPU registers",
  explanation="After an instruction is fetched from memory, it is placed in the Instruction Register, where the "
              "control unit decodes it and then carries it out.",
  steps=["Current instruction being decoded = Instruction Register"],
  wrong="The PC holds the address of the next instruction. The MAR holds the memory address being accessed. The "
        "stack pointer holds the address of the top of the stack.", seconds=15)
Q(T, "Motherboard and ports", "Basic",
  "Which small connector is used to plug a telephone line into a landline phone or a DSL modem?",
  ["RJ-11", "RJ-45", "HDMI", "VGA"],
  concept="Telephone and network connectors",
  explanation="RJ-11 is the small telephone connector with fewer contacts. It connects phones and DSL modems to the "
              "telephone line.",
  steps=["Telephone line connector = RJ-11"],
  wrong="RJ-45 is the wider Ethernet LAN connector. HDMI and VGA carry video to a display.", seconds=15)
Q(T, "CPU and components", "Basic",
  "In many processors, a special register inside the CPU temporarily holds one operand and the result of "
  "arithmetic and logic operations carried out by the ALU. This register is the:",
  ["Accumulator", "Program Counter", "Instruction Register", "Memory Data Register"],
  concept="Accumulator",
  explanation="In accumulator-based designs the accumulator supplies one operand to the ALU and receives the "
              "result, so a series of additions can build up (accumulate) a total without going to memory each time.",
  steps=["Holds ALU operands and results = accumulator"],
  wrong="The PC holds the address of the next instruction, the IR holds the current instruction, and the MDR holds "
        "data moving to or from memory.", seconds=15)
Q(T, "Motherboard and ports", "Intermediate",
  "On a motherboard, which set of chips manages the flow of data between the processor, memory, storage and "
  "expansion devices, and decides which features (such as the number of USB and SATA ports) the board supports?",
  ["Chipset", "CMOS battery", "Heat sink", "Power supply unit"],
  concept="Motherboard chipset",
  explanation="The chipset (historically the northbridge and southbridge, now usually one platform controller hub) "
              "connects the CPU to the rest of the system and controls the board's I/O features.",
  steps=["Controls data flow between CPU and other components = chipset"],
  wrong="The CMOS battery keeps the clock and firmware settings, the heat sink removes heat, and the power supply "
        "converts mains AC to DC.", seconds=20)
Q(T, "Motherboard and ports", "Intermediate",
  "Inside a desktop, which interface with thin 7-pin data cables is commonly used to connect internal hard disks, "
  "2.5-inch SSDs and optical drives to the motherboard?",
  ["SATA", "HDMI", "PS/2", "RJ-45"],
  concept="Storage interfaces",
  explanation="SATA (Serial ATA) replaced the older wide parallel ATA (IDE) ribbon cables. It is the usual "
              "interface for internal hard disks, 2.5-inch SSDs and DVD drives.",
  steps=["Internal drives -> SATA cable"],
  wrong="HDMI carries video and audio to a display, PS/2 is an old keyboard and mouse port, and RJ-45 is the "
        "Ethernet connector.", seconds=20)
o, a = ordered(3600, [136, 360, 36000], lambda v: f"{v / 1000:g} GHz" if v >= 1000 else f"{v} MHz")
Q(T, "CPU and components", "Intermediate",
  "A processor's core clock is produced by multiplying a 100 MHz base clock by a multiplier. If the multiplier is "
  "set to 36, what is the core clock speed?", o, a,
  concept="Base clock and multiplier",
  explanation="Core clock = base clock x multiplier = 100 MHz x 36 = 3,600 MHz = 3.6 GHz.",
  steps=["100 MHz x 36 = 3,600 MHz", "3,600 MHz = 3.6 GHz"],
  wrong="136 MHz adds instead of multiplying. 360 MHz and 36 GHz misplace the decimal point.",
  seconds=25, computed=True)
Q(T, "CPU and components", "Intermediate",
  "A network card has to move a large block of received data into RAM. Which feature lets it transfer the data "
  "directly to memory while the CPU continues with other work, interrupting the CPU only when the transfer is done?",
  ["Direct Memory Access (DMA)", "Polling", "Pipelining", "Virtual memory"],
  concept="Direct Memory Access",
  explanation="With DMA, a DMA controller (or the device itself) takes over the bus and copies data between the "
              "device and memory without the CPU moving each byte. The CPU only sets up the transfer and is "
              "interrupted at the end.",
  steps=["Device <-> memory without the CPU copying data = DMA"],
  wrong="In polling the CPU keeps checking the device, which wastes CPU time. Pipelining overlaps instruction "
        "stages inside the CPU. Virtual memory uses disk space to extend RAM.", seconds=25)
o, a = ordered(0x56, [0x12, 0x34, 0x78], lambda v: f"0x{v:02X}")
Q(T, "CPU and components", "Advanced",
  "A little-endian processor stores the 32-bit value 0x12345678 in memory addresses 100 to 103. Which byte is "
  "stored at address 101?", o, a,
  concept="Endianness",
  explanation="Little-endian machines store the least significant byte at the lowest address. So address 100 holds "
              "0x78, 101 holds 0x56, 102 holds 0x34 and 103 holds 0x12. A big-endian machine would store them in "
              "the opposite order.",
  steps=["Bytes from least significant: 78, 56, 34, 12", "Little-endian: lowest address gets 78",
         "Address 101 -> 0x56"],
  wrong="0x34 would be at address 101 on a big-endian machine. 0x78 is at 100 and 0x12 at 103 on this machine.",
  seconds=40, computed=True)
Q(T, "CPU and components", "Advanced",
  "A processor has several execution units and can issue and complete more than one instruction in the same clock "
  "cycle when the instructions do not depend on each other. Such a processor is described as:",
  ["Superscalar", "Scalar", "Single-cycle", "Microprogrammed"],
  concept="Instruction-level parallelism",
  explanation="A superscalar processor fetches and dispatches several instructions per cycle to multiple execution "
              "units, so its throughput can exceed one instruction per clock cycle. Pipelining alone overlaps stages "
              "but still completes at most one instruction per cycle.",
  steps=["More than one instruction per cycle via multiple execution units = superscalar"],
  wrong="A scalar processor issues at most one instruction per cycle. A single-cycle design finishes each "
        "instruction in one long cycle. Microprogramming is a way of implementing the control unit.", seconds=30)

# ================================================================ 3. Software (1 / 3 / 1)
T = "Software"
Q(T, "System and application software", "Basic",
  "A software vendor releases a small update that fixes a security flaw in a program that customers have already "
  "installed. Such an update is called a:",
  ["Patch", "Compiler", "Macro", "Plug-in"],
  concept="Software updates",
  explanation="A patch is a piece of code that corrects bugs or closes security holes in installed software. Banks "
              "apply security patches quickly because attackers target known, unpatched flaws.",
  steps=["Fix for an installed program = patch"],
  wrong="A compiler translates source code into machine code. A macro is a recorded series of commands. A plug-in "
        "adds a new feature to a program.", seconds=15)
Q(T, "Licensing", "Intermediate",
  "A bank buys a single licence agreement that allows a software product to be installed on all computers at its "
  "head-office premises, instead of buying a separate licence for each computer. This is called a:",
  ["Site licence", "Single-user licence", "Freeware licence", "Trial licence"],
  concept="Types of software licences",
  explanation="A site licence lets an organisation use the software on many computers at one location, usually "
              "for a single negotiated fee. It is simpler and cheaper than buying one licence per machine.",
  steps=["One licence covering all computers at a location = site licence"],
  wrong="A single-user licence covers one user or computer. Freeware needs no payment at all. A trial licence "
        "allows use only for a limited period.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "Which programming language runs inside web browsers and is used to make web pages interactive, for example to "
  "check a form field before it is submitted?",
  ["JavaScript", "COBOL", "SQL", "Assembly language"],
  concept="Client-side scripting",
  explanation="JavaScript is executed by the browser on the user's device. It can react to clicks, validate form "
              "inputs and update parts of a page without reloading it. (Despite its name, it is a separate language "
              "from Java.)",
  steps=["Runs in the browser, makes pages interactive = JavaScript"],
  wrong="COBOL is used for business and banking back-end programs, SQL queries databases, and assembly language is "
        "a low-level language for a specific processor.", seconds=20)
Q(T, "System and application software", "Intermediate",
  "A bank's core banking system, mobile app and card system must exchange messages with each other. Software that "
  "sits between these applications and the operating system, passing messages and data between them, is called:",
  ["Middleware", "Firmware", "Freeware", "Malware"],
  concept="Middleware",
  explanation="Middleware (such as message queues, application servers and API gateways) is the 'glue' that lets "
              "separate applications communicate and share data, so each does not have to know how the others work "
              "inside.",
  steps=["Connects separate applications and passes messages = middleware"],
  wrong="Firmware is software stored in a device's chip. Freeware is software given away free. Malware is "
        "malicious software.", seconds=20)
Q(T, "Programming languages", "Advanced",
  "In languages such as Java, Python and C#, the runtime automatically finds objects that the program can no "
  "longer reach and frees the memory they use. What is this feature called?",
  ["Garbage collection", "Memory leak", "Paging", "Fragmentation"],
  concept="Automatic memory management",
  explanation="A garbage collector tracks which objects are still referenced and reclaims the memory of the rest. "
              "In C, by contrast, the programmer must free memory explicitly, and forgetting to do so causes memory "
              "leaks.",
  steps=["Runtime reclaims unreachable objects automatically = garbage collection"],
  wrong="A memory leak is the problem of memory that is never freed. Paging is how the OS moves memory pages "
        "between RAM and disk. Fragmentation is free memory being broken into small scattered pieces.", seconds=25)

# ================================================================ 4. Operating Systems (4 / 1 / 3)
T = "Operating Systems"
Q(T, "Windows and Linux basics", "Basic",
  "In Windows, which keyboard shortcut opens the Run dialog box, where a user can type a program name such as "
  "notepad to start it?",
  ["Windows logo key + R", "Windows logo key + E", "Windows logo key + D", "Windows logo key + L"],
  concept="Windows shortcuts",
  explanation="Windows logo key + R opens the Run dialog box.",
  steps=["Run dialog = Windows logo key + R"],
  wrong="Windows + E opens File Explorer, Windows + D shows or hides the desktop, and Windows + L locks the PC.",
  seconds=10,
  facts=[fact("Microsoft keyboard shortcuts in Windows: Windows logo key + R - Open the Run dialog box.", MS_WIN)])
Q(T, "Windows and Linux basics", "Basic",
  "Which Linux command copies a file, for example to make a backup copy of report.txt?",
  ["cp", "mv", "rm", "cat"],
  concept="Basic Linux commands",
  explanation="cp copies files or directories: cp report.txt report_backup.txt creates a second copy.",
  steps=["Copy = cp"],
  wrong="mv moves or renames a file, rm deletes it, and cat displays its contents.", seconds=10)
Q(T, "Functions", "Basic",
  "A computer that is already running is restarted using the Restart option, without switching the power off "
  "completely. This is called a:",
  ["Warm boot", "Cold boot", "Hibernation", "Log off"],
  concept="Booting",
  explanation="Booting loads the operating system into memory. A cold (hard) boot starts the computer from a "
              "powered-off state. A warm (soft) boot restarts a computer that is already on.",
  steps=["Restart while powered on = warm boot"],
  wrong="A cold boot starts from power off. Hibernation saves the session to disk and powers off. Logging off ends "
        "the user's session without restarting.", seconds=15)
Q(T, "File systems", "Basic",
  "In the Linux file system, every file and directory lies under a single top-level directory. How is this "
  "directory written?",
  ["/ (a single forward slash)", "C:\\ (drive letter C)", "~ (tilde)", ".. (two dots)"],
  concept="Linux directory tree",
  explanation="Linux has one directory tree whose top is the root directory, written as a single forward slash (/). "
              "Other drives are mounted as directories inside it, for example /mnt/usb.",
  steps=["Top of the Linux tree = / (root directory)"],
  wrong="C:\\ is a Windows drive. ~ is the current user's home directory, and .. is the parent of the current "
        "directory.", seconds=15)
Q(T, "Functions", "Intermediate",
  "Several users send documents to one office printer at the same time. The operating system stores the print jobs "
  "on disk in a queue and feeds them to the slow printer one by one, so the users can continue working. This "
  "technique is called:",
  ["Spooling", "Thrashing", "Swapping", "Booting"],
  concept="Spooling",
  explanation="Spooling (simultaneous peripheral operations on-line) puts output for a slow device into a buffer, "
              "usually on disk, so programs need not wait for the device. A print spooler is the classic example.",
  steps=["Print jobs queued on disk for the printer = spooling"],
  wrong="Thrashing is excessive paging, swapping moves whole processes between RAM and disk, and booting starts "
        "the computer.", seconds=20)
Q(T, "Functions", "Advanced",
  "With FIFO page replacement, the reference string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 causes 9 page faults with 3 "
  "page frames but 10 page faults with 4 frames. What is this behaviour called?",
  ["Belady's anomaly", "Thrashing", "Locality of reference", "Starvation"],
  concept="Belady's anomaly",
  explanation="Normally more frames mean fewer page faults. Belady's anomaly is the case where giving FIFO more "
              "frames increases the number of faults, as here (9 faults with 3 frames, 10 with 4). Stack algorithms "
              "such as LRU and Optimal never show this anomaly.",
  steps=["More frames -> more faults with FIFO", "= Belady's anomaly"],
  wrong="Thrashing is a system spending most of its time paging. Locality of reference is the tendency of programs "
        "to reuse nearby data. Starvation is a process waiting indefinitely for a resource.",
  seconds=35, computed=True)
o, a = ordered(SRTF, [F(5, 2), SJF, FCFS], lambda v: f"{float(v):g} ms")
Q(T, "Functions", "Advanced",
  "Four processes have these (arrival time, CPU burst) values in milliseconds: P1 (0, 7), P2 (2, 4), P3 (4, 1) and "
  "P4 (5, 4). Using preemptive Shortest Remaining Time First (SRTF) scheduling, what is the average waiting time?",
  o, a,
  concept="SRTF scheduling",
  explanation="SRTF always runs the process with the least remaining time, preempting the current one if a shorter "
              "job arrives. Timeline: P1 0-2, P2 2-4, P3 4-5, P2 5-7, P4 7-11, P1 11-16. Waiting time = completion "
              "- arrival - burst: P1 16 - 0 - 7 = 9, P2 7 - 2 - 4 = 1, P3 5 - 4 - 1 = 0, P4 11 - 5 - 4 = 2. "
              "Average = 12 / 4 = 3 ms.",
  steps=["Timeline: P1 0-2, P2 2-4, P3 4-5, P2 5-7, P4 7-11, P1 11-16",
         "Waits: 9, 1, 0, 2", "Average = 12 / 4 = 3 ms"],
  wrong="4 ms is non-preemptive SJF (P1, P3, P2, P4) and 4.75 ms is FCFS. 2.5 ms comes from errors in the "
        "timeline.", seconds=90, computed=True)
Q(T, "Functions", "Advanced",
  "Before granting a resource request, an operating system checks whether the system would still be in a 'safe "
  "state', in which every process can finish in some order with the resources left. It grants the request only if "
  "the state stays safe. Which algorithm does this, and what is it used for?",
  ["Banker's algorithm, used for deadlock avoidance", "Banker's algorithm, used for deadlock detection",
   "Round Robin algorithm, used for CPU scheduling", "LRU algorithm, used for page replacement"],
  concept="Deadlock avoidance",
  explanation="Dijkstra's Banker's algorithm knows each process's maximum need and refuses (delays) any request that "
              "would lead to an unsafe state, so a deadlock can never form. That is avoidance, not detection.",
  steps=["Check safe state before granting = Banker's algorithm", "Prevents deadlocks from forming = avoidance"],
  wrong="Detection lets deadlocks happen and then finds them, for example with a wait-for graph. Round Robin "
        "shares CPU time and LRU replaces memory pages; neither checks for safe states.", seconds=35)

# ================================================================ 5. Input and Output Devices (3 / 4 / 1)
T = "Input and Output Devices"
Q(T, "Input devices", "Basic",
  "During video KYC, a bank officer must see the customer live on a laptop. Which input device captures the "
  "customer's live video?",
  ["Webcam", "Speaker", "Plotter", "Projector"],
  concept="Video input devices",
  explanation="A webcam is a digital camera that captures live video and sends it to the computer, for video calls "
              "and video KYC.",
  steps=["Captures live video = webcam (input)"],
  wrong="A speaker gives sound output, a plotter draws large drawings on paper, and a projector shows the screen "
        "on a wall; all three are output devices.", seconds=10)
Q(T, "Input devices", "Basic",
  "Which pen-shaped input device is pointed at a screen to select items or draw directly on the display?",
  ["Light pen", "Joystick", "Trackball", "Barcode reader"],
  concept="Pointing devices",
  explanation="A light pen has a light-sensitive tip. When pointed at the screen it detects the position, so the "
              "user can select or draw directly on the display.",
  steps=["Pen pointed at the screen to select or draw = light pen"],
  wrong="A joystick is a lever used mainly for games. A trackball is a ball rolled with the fingers. A barcode "
        "reader scans product codes.", seconds=10)
Q(T, "Output devices", "Basic",
  "Which type of printer forms characters and images by spraying tiny droplets of liquid ink onto the paper?",
  ["Inkjet printer", "Laser printer", "Dot-matrix printer", "Thermal printer"],
  concept="Printer types",
  explanation="An inkjet printer has a print head with very small nozzles that spray ink drops onto the paper. It is "
              "common for home and small-office colour printing.",
  steps=["Sprays liquid ink droplets = inkjet"],
  wrong="A laser printer fuses toner powder with heat, a dot-matrix printer strikes an inked ribbon with pins, and "
        "a thermal printer darkens heat-sensitive paper.", seconds=10)
Q(T, "Output devices", "Intermediate",
  "A data centre must print very long reports on continuous paper at high speed, one complete line of text at a "
  "time. Which printer is designed for this?",
  ["Line printer", "Inkjet printer", "Plotter", "Thermal receipt printer"],
  concept="Impact printers",
  explanation="A line printer is a high-speed impact printer that prints an entire line in one operation. Line "
              "printers were the standard for bulk mainframe output such as statements and reports.",
  steps=["Prints a whole line at a time = line printer"],
  wrong="An inkjet prints a character or a strip at a time and is much slower for bulk work. A plotter draws "
        "drawings with pens. A thermal receipt printer prints short receipts.", seconds=20)
Q(T, "Output devices", "Intermediate",
  "A monitor has a resolution of 1680 x 1050 pixels. What is its aspect ratio (width : height)?",
  ["16:10", "16:9", "4:3", "5:4"],
  concept="Aspect ratio",
  explanation="Divide both numbers by their highest common factor, 210: 1680 / 210 = 8 and 1050 / 210 = 5, so the "
              "ratio is 8:5, which is written 16:10.",
  steps=["HCF(1680, 1050) = 210", "1680 : 1050 = 8 : 5", "8 : 5 = 16 : 10"],
  shortcut="1680 / 1050 = 1.6. 16:9 = 1.78, 4:3 = 1.33, 5:4 = 1.25 and 16:10 = 1.6.",
  wrong="16:9 is the ratio of 1920 x 1080. 4:3 is the ratio of 1024 x 768. 5:4 is the ratio of 1280 x 1024.",
  seconds=30, computed=True)
Q(T, "Output devices", "Intermediate",
  "A branch is comparing printers for speed. In which unit is a printer's printing speed usually stated?",
  ["Pages per minute (PPM)", "Dots per inch (DPI)", "Frames per second (FPS)", "Revolutions per minute (RPM)"],
  concept="Printer specifications",
  explanation="Printer speed is given in pages per minute (PPM). Print quality (resolution) is given separately in "
              "dots per inch.",
  steps=["Printer speed = PPM"],
  wrong="DPI measures print resolution, not speed. FPS measures video frame rate, and RPM measures the spin speed "
        "of a disk.", seconds=15)
Q(T, "Input devices", "Intermediate",
  "The standard English keyboard layout is called QWERTY. Where does this name come from?",
  ["The first six letters of the top row of letter keys",
   "The initials of the company that invented the keyboard",
   "The six keys typed most often in English",
   "The six function keys at the top of the keyboard"],
  concept="Keyboard layouts",
  explanation="Reading the top letter row from the left gives Q, W, E, R, T, Y. The layout comes from 19th-century "
              "typewriters and is still the most common keyboard layout.",
  steps=["Top letter row starts Q W E R T Y"],
  wrong="QWERTY is not a company name, the letters are not the most frequent in English, and the function keys are "
        "named F1 to F12.", seconds=15)
o, a = ordered(82_944_000, [2_764_800, 27_648_000, 663_552_000], lambda v: f"{v:,} bytes")
Q(T, "Input devices", "Advanced",
  "A webcam captures uncompressed video at 1280 x 720 pixels, 24-bit colour and 30 frames per second. How much data "
  "does it produce every second?", o, a,
  concept="Video data rate",
  explanation="One frame = 1280 x 720 pixels x 3 bytes (24 bits) = 2,764,800 bytes. At 30 frames per second, data "
              "per second = 2,764,800 x 30 = 82,944,000 bytes (about 83 MB/s), which is why video is compressed "
              "before it is sent.",
  steps=["Pixels per frame = 1280 x 720 = 921,600", "Bytes per frame = 921,600 x 3 = 2,764,800",
         "Per second = 2,764,800 x 30 = 82,944,000 bytes"],
  wrong="2,764,800 bytes is one frame only. 27,648,000 uses 1 byte per pixel instead of 3. 663,552,000 is the "
        "figure in bits, not bytes.", seconds=60, computed=True)

# ================================================================ 6. Memory (1 / 4 / 2)
T = "Memory"
Q(T, "Primary memory", "Basic",
  "Which of the following is NOT part of a computer's primary memory?",
  ["Hard disk", "RAM", "ROM", "Cache memory"],
  concept="Primary and secondary memory",
  explanation="Primary memory is directly accessed by the CPU: RAM, ROM and cache. A hard disk is secondary "
              "storage; its data must be loaded into RAM before the CPU can use it.",
  steps=["Primary = RAM, ROM, cache", "Hard disk = secondary storage"],
  wrong="RAM, ROM and cache memory are all directly accessible by the CPU, so they are primary memory.", seconds=10)
Q(T, "Secondary storage", "Intermediate",
  "When files are deleted, the operating system sends a command to the SSD telling it which data blocks are no "
  "longer in use, so that the drive can erase them in the background and keep its write speed high. What is this "
  "command called?",
  ["TRIM", "Defragmentation", "Format", "Refresh"],
  concept="SSD maintenance",
  explanation="Flash memory must erase a block before writing to it again. TRIM informs the SSD which blocks hold "
              "deleted data, so it can clean them in advance (garbage collection) instead of during a later write.",
  steps=["OS tells SSD which blocks are unused = TRIM"],
  wrong="Defragmentation rearranges file pieces and is not needed on SSDs. Formatting prepares a whole drive with a "
        "new file system. Refresh is the periodic recharging of DRAM cells.", seconds=25)
Q(T, "Primary memory", "Intermediate",
  "Why is DDR SDRAM called 'Double Data Rate' memory?",
  ["It transfers data on both the rising and the falling edge of the clock signal",
   "It has twice as many memory chips as SDRAM",
   "It stores two bits in every memory cell",
   "It runs on double the voltage of SDRAM"],
  concept="DDR memory",
  explanation="Ordinary SDRAM transfers data once per clock cycle. DDR SDRAM transfers data on both edges of the "
              "clock, giving twice the transfer rate at the same clock frequency.",
  steps=["Data on both clock edges -> two transfers per cycle = double data rate"],
  wrong="DDR does not double the number of chips or the bits per cell, and newer DDR generations use lower, not "
        "higher, voltages.", seconds=25)
Q(T, "Cache and units", "Intermediate",
  "Which type of memory is searched by its contents rather than by an address, comparing a search key with all "
  "stored entries at the same time, and is used in TLBs and network switches?",
  ["Associative memory (content-addressable memory)", "Flash memory", "Virtual memory", "Sequential-access memory"],
  concept="Associative memory",
  explanation="Content-addressable (associative) memory compares the given data with every stored word in "
              "parallel and returns the matching location. This makes look-ups very fast, which is why it is used in "
              "the TLB and in switch MAC tables.",
  steps=["Searched by content, all entries in parallel = associative memory"],
  wrong="Flash memory is non-volatile storage. Virtual memory uses disk to extend RAM. Sequential-access memory, "
        "such as tape, must be read in order.", seconds=25)
Q(T, "Primary memory", "Intermediate",
  "Bank servers often use a special kind of RAM that stores extra check bits with each word so that it can "
  "automatically find and correct single-bit errors. What is this RAM called?",
  ["ECC memory", "Cache memory", "Virtual memory", "Video RAM"],
  concept="Error-correcting memory",
  explanation="ECC (Error-Correcting Code) memory adds check bits to each data word. It can correct any single-bit "
              "error and detect double-bit errors, protecting critical data in servers from random memory faults.",
  steps=["Extra check bits, corrects single-bit errors = ECC memory"],
  wrong="Cache memory is small fast memory near the CPU. Virtual memory uses disk space. Video RAM is used by "
        "graphics cards. None of these is defined by error correction.", seconds=20)
o, a = ordered(4 * 2 ** 20, [2 ** 20, 4 * 2 ** 10, 16 * 2 ** 20],
               lambda v: f"{v // 2 ** 20} MB" if v >= 2 ** 20 else f"{v // 2 ** 10} KB")
Q(T, "Primary memory", "Advanced",
  "A system uses 32-bit virtual addresses and 4 KB pages, and each page-table entry is 4 bytes. How large is the "
  "page table of one process if it is kept as a single-level table? (1 KB = 2^10 bytes, 1 MB = 2^20 bytes)", o, a,
  concept="Page-table size",
  explanation="Number of pages = 2^32 / 2^12 = 2^20 (about one million). Each needs a 4-byte entry, so the table "
              "is 2^20 x 4 bytes = 4 MB. Such large tables are why systems use multi-level page tables.",
  steps=["Page size 4 KB = 2^12 -> 12 offset bits", "Pages = 2^(32 - 12) = 2^20",
         "Table = 2^20 x 4 bytes = 4 MB"],
  wrong="1 MB counts entries but forgets the 4 bytes per entry. 4 KB is one page. 16 MB multiplies by 16 instead "
        "of 4.", seconds=50, computed=True)
o, a = ordered(16, [4, 8, 32])
Q(T, "Secondary storage", "Advanced",
  "A QLC (quad-level cell) NAND flash cell stores 4 bits. How many distinct charge (voltage) levels must each cell "
  "be able to hold and tell apart?", o, a,
  concept="Bits per flash cell",
  explanation="To store n bits, a cell needs 2^n distinguishable levels. SLC (1 bit) needs 2, MLC (2 bits) 4, TLC "
              "(3 bits) 8 and QLC (4 bits) 16. More levels mean more capacity but slower writes and lower endurance.",
  steps=["Levels = 2^bits", "QLC: 2^4 = 16"],
  wrong="4 is the number of bits, not levels. 8 levels are for TLC (3 bits). 32 levels would store 5 bits.",
  seconds=30, computed=True)

# ================================================================ 7. Internet (3 / 2 / 5)
T = "Internet"
Q(T, "Email", "Basic",
  "Asha receives an email sent to her and four colleagues. If she clicks 'Reply All', who receives her reply?",
  ["The sender and all the other visible recipients of the original email",
   "Only the sender of the original email",
   "Everyone in Asha's contact list",
   "Only the recipients who were in the Bcc field"],
  concept="Reply and Reply All",
  explanation="Reply sends the response only to the sender. Reply All sends it to the sender and to everyone in the "
              "To and Cc fields. Bcc recipients are hidden, so they are not included.",
  steps=["Reply = sender only", "Reply All = sender + all To and Cc recipients"],
  wrong="Replying only to the sender is plain Reply. Reply All does not use the contact list, and Bcc addresses "
        "are hidden from other recipients, so they are not added.", seconds=15)
Q(T, "Web basics", "Basic",
  "A bank runs a private website, built with the same web technologies as the internet, that only its employees "
  "can open to read circulars and use internal tools. This private network is called an:",
  ["Intranet", "Extranet", "Internet", "Ethernet"],
  concept="Intranet",
  explanation="An intranet is an organisation's private network that uses internet technologies (web servers, "
              "browsers, email) but is open only to its own staff.",
  steps=["Private, employees only = intranet"],
  wrong="An extranet also lets selected outsiders in. The internet is the public worldwide network. Ethernet is a "
        "wired LAN technology.", seconds=15)
Q(T, "Web basics", "Basic",
  "In a web browser, which feature saves the address of a page so that the user can open it again later with one "
  "click?",
  ["Bookmark (Favourite)", "Cache", "Cookie", "Pop-up"],
  concept="Browser features",
  explanation="A bookmark (called a Favourite in some browsers) stores the page's address in the browser so the "
              "user can return to it quickly.",
  steps=["Save a page's address for later = bookmark"],
  wrong="The cache stores copies of page files to load them faster, a cookie is small data a website stores, and "
        "a pop-up is a window that opens on its own.", seconds=10)
Q(T, "Protocols", "Intermediate",
  "A web server replies with HTTP status code 301. To which class of status codes does it belong?",
  ["Redirection (3xx)", "Successful (2xx)", "Client error (4xx)", "Server error (5xx)"],
  concept="HTTP status code classes",
  explanation="HTTP status codes are grouped by their first digit: 1xx informational, 2xx successful, 3xx "
              "redirection, 4xx client error and 5xx server error. 301 Moved Permanently tells the browser that the "
              "resource has a new URL, which is given in the response.",
  steps=["First digit 3 -> redirection", "301 = Moved Permanently"],
  wrong="2xx codes (such as 200 OK) mean success, 4xx codes (such as 404) are client errors, and 5xx codes (such "
        "as 500) are server errors.", seconds=20,
  facts=[fact("MDN: responses are grouped in five classes, including redirection messages (300-399); 301 Moved "
              "Permanently means the URL of the requested resource has been changed permanently.", MDN_STATUS)])
Q(T, "Web basics", "Intermediate",
  "A bank lets its business correspondents and partner insurance companies log in to a restricted part of its "
  "private network to upload documents. A private network that is opened in this way to selected outside users "
  "is called an:",
  ["Extranet", "Intranet", "Internet", "Darknet"],
  concept="Extranet",
  explanation="An extranet extends part of an organisation's intranet to authorised outsiders such as partners, "
              "suppliers or agents, usually with logins and access controls.",
  steps=["Private network + authorised outsiders = extranet"],
  wrong="An intranet is for employees only. The internet is public. A darknet is an overlay network reached only "
        "with special software.", seconds=20)
Q(T, "Protocols", "Advanced",
  "A net-banking site sends the response header Strict-Transport-Security (HSTS). What effect does this have on "
  "the user's browser?",
  ["The browser will use only HTTPS for that site, upgrading any http:// request, and will not let the user "
   "bypass certificate errors",
   "The browser will block all cookies sent by that site",
   "The browser will stop JavaScript on the page from reading cookies",
   "The browser will load the site's pages only from the same origin"],
  concept="HTTP Strict Transport Security",
  explanation="HSTS tells browsers that the host must be reached only over HTTPS. Future http:// attempts are "
              "upgraded automatically, and the browser does not allow clicking through certificate errors. This "
              "defeats attacks that strip HTTPS from a connection.",
  steps=["HSTS = HTTPS only, auto-upgrade, no bypass of certificate errors"],
  wrong="HSTS does not block cookies. Stopping scripts from reading a cookie is the HttpOnly attribute, and the "
        "same-origin policy is a separate browser rule.", seconds=30,
  facts=[fact("MDN: the Strict-Transport-Security header informs browsers that the host should only be accessed "
              "using HTTPS, future HTTP attempts are upgraded, and the user cannot bypass secure connection errors "
              "such as an invalid certificate.", MDN_HSTS)])
Q(T, "Email", "Advanced",
  "A bank already uses SPF and DKIM. It now publishes a DNS record telling receiving mail servers what to do with "
  "messages that claim to be from its domain but fail these checks (for example, reject them) and where to send "
  "reports. Which mechanism is this?",
  ["DMARC", "MX record", "S/MIME", "IMAP"],
  concept="Email domain authentication",
  explanation="DMARC builds on SPF and DKIM. The domain owner publishes a policy (none, quarantine or reject) for "
              "mail that fails, and receivers send aggregate reports back. A message passes DMARC if SPF or DKIM "
              "verifies a domain that matches the visible From domain.",
  steps=["Policy for failing mail + reports, built on SPF and DKIM = DMARC"],
  wrong="An MX record only names the domain's mail servers. S/MIME signs and encrypts individual messages. IMAP is "
        "used to read mail from a mailbox.", seconds=30,
  facts=[fact("RFC 7489: DMARC is a mechanism by which a mail-originating organisation can express domain-level "
              "policies and preferences for message validation, disposition and reporting; it uses SPF and DKIM "
              "results.", RFC7489)])
Q(T, "Web basics", "Advanced",
  "A bank's website stores copies of its images, scripts and videos on many servers in different cities, and each "
  "visitor is served from the server nearest to him, which loads pages faster and absorbs traffic spikes. What is "
  "this network of servers called?",
  ["Content Delivery Network (CDN)", "Virtual Private Network (VPN)", "Storage Area Network (SAN)",
   "Peer-to-peer network"],
  concept="Content delivery networks",
  explanation="A CDN caches content on edge servers spread across many locations. Users get files from a nearby "
              "server, which cuts delay and reduces the load on the origin server; CDNs also help absorb traffic "
              "floods.",
  steps=["Copies of content on servers near users = CDN"],
  wrong="A VPN creates an encrypted tunnel for private access. A SAN is a dedicated network that connects servers "
        "to shared disk storage. In peer-to-peer networks users' own computers share files with each other.",
  seconds=25)
Q(T, "Protocols", "Advanced",
  "HTTP/1.1 and HTTP/2 normally run over TCP. On which transport does HTTP/3 run?",
  ["QUIC, which is carried in UDP datagrams", "TCP with TLS 1.3", "SCTP", "ICMP"],
  concept="HTTP/3 and QUIC",
  explanation="HTTP/3 maps HTTP onto QUIC, a transport protocol whose packets are carried in UDP datagrams. QUIC "
              "builds in TLS 1.3 encryption and avoids TCP's head-of-line blocking across streams.",
  steps=["HTTP/3 -> QUIC", "QUIC packets travel in UDP datagrams"],
  wrong="TCP with TLS is how HTTPS works for HTTP/1.1 and HTTP/2. SCTP is a different transport protocol not used "
        "for HTTP/3. ICMP carries error and diagnostic messages.", seconds=25,
  facts=[fact("RFC 9114: HTTP/3 describes a mapping of HTTP semantics over QUIC; servers may serve HTTP/3 on any "
              "UDP port.", RFC9114),
         fact("RFC 9000: QUIC packets are carried in UDP datagrams.", RFC9000)])
Q(T, "Email", "Advanced",
  "A bank wants each email it sends to customers to be digitally signed and, when needed, encrypted end to end, "
  "using X.509 certificates. Which standard provides this?",
  ["S/MIME", "SMTP", "POP3", "SPF"],
  concept="Secure email",
  explanation="S/MIME (Secure/Multipurpose Internet Mail Extensions) uses certificates to sign messages "
              "(authentication, integrity, non-repudiation) and to encrypt them (confidentiality).",
  steps=["Signed and encrypted email with certificates = S/MIME"],
  wrong="SMTP transfers mail but does not sign or encrypt messages. POP3 downloads mail. SPF lists which servers "
        "may send for a domain; it does not sign or encrypt messages.", seconds=25,
  facts=[fact("RFC 8551: S/MIME digital signatures provide authentication, message integrity and non-repudiation "
              "with proof of origin; encryption provides data confidentiality.", RFC8551)])

# ================================================================ 8. Networking (2 / 5 / 2)
T = "Networking"
Q(T, "Devices", "Basic",
  "Which network device joins two LAN segments and forwards a frame to the other segment only if the destination "
  "MAC address is on that side, reducing unnecessary traffic?",
  ["Bridge", "Hub", "Repeater", "Modem"],
  concept="Bridges",
  explanation="A bridge works at the data link layer. It learns which MAC addresses are on each side and filters "
              "frames, passing only those meant for the other segment. A switch is essentially a multi-port bridge.",
  steps=["Joins two LAN segments, filters by MAC = bridge"],
  wrong="A hub and a repeater pass every signal on without looking at addresses. A modem converts digital signals "
        "for a telephone or cable line.", seconds=15)
Q(T, "Topologies", "Basic",
  "In a star topology, what happens if the central switch fails?",
  ["The whole network stops working", "Only one computer is cut off",
   "Data automatically travels around a ring instead", "Nothing, because every computer is linked to every other"],
  concept="Star topology",
  explanation="In a star, every computer is connected only to the central device, so all traffic passes through it. "
              "If one cable fails only that computer is cut off, but if the centre fails the whole network stops.",
  steps=["All traffic goes through the centre", "Centre fails -> whole network down"],
  wrong="Losing only one computer happens when a single cable fails. Rerouting around a ring and links between "
        "every pair of computers describe ring and mesh topologies.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "A browser asks a DNS server for the IP address of a website. Which transport protocol and port does an ordinary "
  "DNS query normally use?",
  ["UDP port 53", "TCP port 80", "TCP port 443", "UDP port 123"],
  concept="DNS transport",
  explanation="Standard DNS queries are sent as UDP datagrams to port 53, because the query and reply are small "
              "and quick. DNS also uses TCP on port 53, for example for zone transfers or large replies.",
  steps=["DNS = port 53", "Normal queries = UDP"],
  wrong="TCP 80 and 443 are HTTP and HTTPS. UDP 123 is NTP (time synchronisation).", seconds=20,
  facts=[fact("RFC 1035: the Internet supports name server access using TCP on server port 53 as well as datagram "
              "access using UDP on UDP port 53; messages carried by UDP are restricted to 512 bytes.", RFC1035)])
Q(T, "Devices", "Intermediate",
  "A bank's internet-banking website runs on six identical web servers. Which device spreads incoming customer "
  "requests across these servers so that no single server is overloaded, and stops sending traffic to a server "
  "that fails?",
  ["Load balancer", "Repeater", "Modem", "Hub"],
  concept="Load balancing",
  explanation="A load balancer receives client connections and distributes them among a pool of servers, for "
              "example in turn or to the least busy. Health checks let it skip a failed server, which improves both "
              "speed and availability.",
  steps=["Distributes requests among several servers = load balancer"],
  wrong="A repeater regenerates a weak signal, a modem converts signals for a phone or cable line, and a hub copies "
        "data to all ports; none of them chooses between servers.", seconds=20)
Q(T, "OSI and TCP/IP", "Intermediate",
  "As data moves down the TCP/IP layers before transmission, it is wrapped with headers at each layer "
  "(encapsulation). What is the correct order of the data units, from the transport layer down to the wire?",
  ["Segment -> Packet -> Frame -> Bits", "Packet -> Segment -> Frame -> Bits", "Frame -> Packet -> Segment -> Bits",
   "Segment -> Frame -> Packet -> Bits"],
  concept="Encapsulation",
  explanation="The transport layer adds a TCP or UDP header to make a segment (or datagram). The network layer adds "
              "an IP header to make a packet. The data link layer adds a header and trailer to make a frame. The "
              "physical layer sends it as bits.",
  steps=["Transport -> segment", "Network -> packet", "Data link -> frame", "Physical -> bits"],
  wrong="The other orders put the layers in the wrong sequence; the packet (network layer) always sits between the "
        "segment (transport) and the frame (data link).", seconds=25)
Q(T, "Devices", "Intermediate",
  "How many bits long is the MAC (hardware) address of an Ethernet network card, usually written as six pairs of "
  "hexadecimal digits such as 00:1A:2B:3C:4D:5E?",
  ["48 bits", "32 bits", "64 bits", "128 bits"],
  concept="MAC addresses",
  explanation="An Ethernet MAC address (EUI-48) is 48 bits = 6 bytes, written as 12 hexadecimal digits. The first "
              "24 bits are the OUI that the IEEE assigns to the manufacturer; the manufacturer sets the rest.",
  steps=["6 pairs of hex digits = 6 bytes", "6 x 8 = 48 bits"],
  shortcut="Each hex digit is 4 bits: 12 digits x 4 = 48 bits.",
  wrong="32 bits is the size of an IPv4 address and 128 bits of an IPv6 address. 64 bits is the EUI-64 identifier "
        "format, not the usual Ethernet MAC.", seconds=20, web=SC,
  facts=[fact("IEEE Registration Authority: an OUI-based assignment may be appended with 24 organisation-supplied "
              "bits to form a EUI-48 identifier.", IEEE_OUI)])
Q(T, "OSI and TCP/IP", "Intermediate",
  "IPv4 addresses are 32 bits long. How long is an IPv6 address?",
  ["128 bits", "64 bits", "48 bits", "256 bits"],
  concept="IPv6 addressing",
  explanation="IPv6 increases the IP address size from 32 bits to 128 bits, giving about 3.4 x 10^38 addresses and "
              "solving the shortage of IPv4 addresses. It is written as eight groups of four hexadecimal digits.",
  steps=["IPv6 address = 128 bits (8 groups x 16 bits)"],
  wrong="64 bits is only the usual interface-identifier half of an IPv6 address, 48 bits is the size of an "
        "Ethernet MAC address, and 256 bits is not an IP address size.", seconds=15,
  facts=[fact("RFC 8200: IPv6 increases the IP address size from 32 bits to 128 bits; the Source and Destination "
              "Address fields are 128-bit addresses.", RFC8200)])
Q(T, "OSI and TCP/IP", "Advanced",
  "Fifty PCs in a branch have private IPv4 addresses, yet all of them browse the internet through the branch "
  "router's single public IP address. The router keeps track of each connection by changing the source address and "
  "port number. What is this technique called?",
  ["PAT (Port Address Translation, or NAT overload)", "ARP (Address Resolution Protocol)",
   "DHCP (Dynamic Host Configuration Protocol)", "Static one-to-one NAT"],
  concept="Network address translation",
  explanation="NAT rewrites private addresses into a public one. In PAT (NAT overload), many private hosts share "
              "one public address; the router gives each connection a unique source port and keeps a translation "
              "table so replies reach the right PC.",
  steps=["Many private hosts, one public IP, tracked by port = PAT / NAT overload"],
  wrong="ARP finds MAC addresses for IP addresses on a LAN. DHCP hands out IP addresses. Static NAT maps one "
        "private address to one public address, so 50 PCs would need 50 public addresses.", seconds=30)
Q(T, "Devices", "Advanced",
  "A router connects two LANs. Each LAN has a 16-port switch with all ports in use: 15 PCs and one link to the "
  "router. There are no VLANs. How many broadcast domains and how many collision domains are there?",
  ["2 broadcast domains and 32 collision domains", "1 broadcast domain and 32 collision domains",
   "2 broadcast domains and 2 collision domains", "32 broadcast domains and 2 collision domains"],
  concept="Collision and broadcast domains",
  explanation="Every switch port is its own collision domain: 16 + 16 = 32 (the router links are two of these). "
              "Switches forward broadcasts, but routers do not, so each router interface marks a separate broadcast "
              "domain: 2.",
  steps=["Switch port = 1 collision domain each -> 16 + 16 = 32", "Router interface = 1 broadcast domain each -> 2"],
  shortcut="Switches split collision domains; routers (or VLANs) split broadcast domains.",
  wrong="1 broadcast domain ignores the router. 2 collision domains would be true only if hubs were used. 32 "
        "broadcast domains mixes up the two kinds of domain.", seconds=45, computed=True)

# ================================================================ 9. Cybersecurity (3 / 2 / 4)
T = "Cybersecurity"
Q(T, "Malware", "Basic",
  "While browsing, a user sees a flashing pop-up: 'WARNING! 27 viruses found on your PC. Buy CleanMax now to remove "
  "them.' The warning is fake and is meant to frighten the user into paying or installing harmful software. This "
  "is called:",
  ["Scareware", "Firewall", "Patch", "Cookie"],
  concept="Scareware",
  explanation="Scareware uses fake security alerts to create panic, so the user pays for useless 'protection' or "
              "installs malware. Real antivirus warnings come from software the user installed, not from a web "
              "pop-up.",
  steps=["Fake alarm to frighten user into buying or installing = scareware"],
  wrong="A firewall filters network traffic, a patch fixes software flaws, and a cookie is a small file stored by a "
        "website; none is a fake alert.", seconds=15)
Q(T, "Malware", "Basic",
  "A traveller charges his phone at a free public USB charging port at a railway station. Criminals have tampered "
  "with the port so that it copies data from, or installs malware on, connected phones. This attack is known as:",
  ["Juice jacking", "Tailgating", "Shoulder surfing", "Pharming"],
  concept="Juice jacking",
  explanation="A USB port carries data as well as power. A tampered public charging port can steal data or plant "
              "malware. Using your own charger in a power socket, or a charge-only cable, avoids this.",
  steps=["Tampered public USB charging point = juice jacking"],
  wrong="Tailgating is following someone through a secure door, shoulder surfing is watching someone type a PIN, "
        "and pharming redirects users to fake websites.", seconds=15)
Q(T, "Phishing and social engineering", "Basic",
  "A fraudster convinces a mobile operator to issue a new SIM card for a customer's mobile number. The customer's "
  "phone loses signal, and the fraudster starts receiving the bank's OTPs. What is this fraud called?",
  ["SIM swap fraud", "Card skimming", "Cryptojacking", "Adware"],
  concept="SIM swap fraud",
  explanation="In a SIM swap the criminal takes over the victim's mobile number, often using stolen identity "
              "details, and then receives the SMS OTPs needed to authorise transactions. A sudden loss of mobile "
              "signal is a warning sign to report to the bank and operator at once.",
  steps=["Duplicate SIM to receive the victim's OTPs = SIM swap fraud"],
  wrong="Skimming copies card data at a card reader, cryptojacking secretly uses computers to mine cryptocurrency, "
        "and adware shows unwanted advertisements.", seconds=15)
Q(T, "Phishing and social engineering", "Intermediate",
  "A sticker with a fake QR code is pasted over a shop's genuine one. Customers who scan it are taken to a "
  "look-alike payment page that steals their details. Phishing through malicious QR codes is called:",
  ["Quishing", "Vishing", "Smishing", "Whaling"],
  concept="QR-code phishing",
  explanation="Quishing (QR phishing) hides a malicious link inside a QR code, which the user cannot read before "
              "scanning. Checking the payee name shown in the payment app before paying protects against it.",
  steps=["Phishing via QR code = quishing"],
  wrong="Vishing uses voice calls, smishing uses SMS, and whaling targets senior executives.", seconds=15)
Q(T, "Encryption and authentication", "Intermediate",
  "On a café's public Wi-Fi, an attacker secretly places himself between a user's laptop and the internet, so "
  "that he can read and change the traffic passing between them while both sides think they are talking directly. "
  "What is this attack called?",
  ["Man-in-the-middle attack", "Brute-force attack", "Denial-of-service attack", "Logic bomb"],
  concept="Man-in-the-middle (MITM)",
  explanation="In a MITM attack the attacker intercepts and relays communication between two parties. Strong "
              "encryption with certificate checking (HTTPS) and a VPN on public Wi-Fi protect against it.",
  steps=["Attacker secretly between two parties, reading and changing traffic = man-in-the-middle"],
  wrong="A brute-force attack tries every possible password. A denial-of-service attack floods a system to make it "
        "unavailable. A logic bomb is malicious code triggered by a condition.", seconds=20)
Q(T, "Encryption and authentication", "Advanced",
  "Banks keep the cryptographic keys used for PIN verification and card transactions inside a tamper-resistant "
  "physical device that also performs the cryptographic operations, so the keys never appear in plain form in "
  "ordinary server memory. What is this device?",
  ["Hardware Security Module (HSM)", "Network Attached Storage (NAS)", "Uninterruptible Power Supply (UPS)",
   "Intrusion Detection System (IDS)"],
  concept="Hardware security modules",
  explanation="An HSM is a dedicated, tamper-evident and intrusion-resistant device that generates, stores and "
              "protects cryptographic keys and performs encryption, decryption and signing inside itself. Payment "
              "systems use HSMs for PIN processing and key management.",
  steps=["Tamper-resistant device that safeguards keys and does crypto = HSM"],
  wrong="NAS is a file-storage device on a network, a UPS supplies backup power, and an IDS monitors network "
        "traffic for attacks; none of them protects keys in this way.", seconds=25,
  facts=[fact("NIST CSRC glossary: an HSM is a physical computing device that safeguards and manages cryptographic "
              "keys and provides cryptographic processing; it offers tamper-evident and intrusion-resistant "
              "safeguarding of keys.", NIST_HSM)])
Q(T, "Encryption and authentication", "Advanced",
  "Attackers take millions of username-password pairs leaked from a shopping website and use automated tools to "
  "try them on a bank's login page, succeeding wherever customers reused the same password. Which attack is this, "
  "and which control defeats it best?",
  ["Credential stuffing; multi-factor authentication", "Brute-force attack; a longer encryption key",
   "Phishing; an email spam filter", "SQL injection; input validation"],
  concept="Credential stuffing",
  explanation="Credential stuffing reuses real credentials stolen from another site. Because the passwords are "
              "correct, complexity rules do not help. Multi-factor authentication stops it, since the attacker also "
              "needs the second factor; rate-limiting and checks for breached passwords help too.",
  steps=["Leaked pairs tried on another site = credential stuffing", "Correct passwords -> need a second factor = MFA"],
  wrong="A brute-force attack guesses passwords rather than reusing leaked ones, and key length does not protect a "
        "login. No phishing message is involved. SQL injection attacks database queries, not reused passwords.",
  seconds=35)
Q(T, "Phishing and social engineering", "Advanced",
  "A fraudster pretends to be a bank officer on a phone call and on WhatsApp and tricks a customer into sharing an "
  "OTP. Under India's Information Technology Act, 2000, which section specifically punishes cheating by "
  "personation using a computer resource or communication device?",
  ["Section 66D", "Section 43A", "Section 67", "Section 65"],
  concept="IT Act offences",
  explanation="Section 66D punishes whoever, by means of any communication device or computer resource, cheats by "
              "personation, with imprisonment of up to three years and a fine of up to Rs 1 lakh. It covers "
              "impersonation frauds such as fake bank officers and phishing.",
  steps=["Cheating by personation using a computer resource = Section 66D"],
  wrong="Section 43A deals with compensation for failure to protect sensitive personal data, Section 67 with "
        "publishing obscene material electronically, and Section 65 with tampering with computer source documents.",
  seconds=25,
  facts=[fact("IT Act 2000, Section 66D: whoever, by means of any communication device or computer resource cheats "
              "by personation, shall be punished with imprisonment up to three years and fine up to one lakh "
              "rupees.", IT_66D)])
Q(T, "Malware", "Advanced",
  "An attack leaves no malicious program file on the disk. Instead it runs its code in memory through trusted "
  "built-in tools such as PowerShell, so that antivirus scans of files find nothing. This is known as:",
  ["Fileless malware", "A macro virus", "A boot-sector virus", "Adware"],
  concept="Fileless malware",
  explanation="Fileless malware 'lives off the land': it uses legitimate system tools and runs in memory, leaving "
              "few traces on disk. Detecting it needs behaviour monitoring rather than only file signatures.",
  steps=["No file on disk, runs in memory via trusted tools = fileless malware"],
  wrong="A macro virus lives inside document files, a boot-sector virus infects the disk's boot record, and adware "
        "is an installed program that shows ads; all of these leave files or disk changes.", seconds=30)

# ================================================================ 10. Database Fundamentals (1 / 2 / 2)
T = "Database Fundamentals"
Q(T, "DBMS concepts", "Basic",
  "Which of the following is a database management system (DBMS)?",
  ["MySQL", "MS Paint", "Google Chrome", "Windows Media Player"],
  concept="DBMS software",
  explanation="MySQL is a relational DBMS used to create, store, query and manage databases. Oracle Database, "
              "PostgreSQL and Microsoft SQL Server are other examples.",
  steps=["MySQL = relational DBMS"],
  wrong="MS Paint is a drawing program, Chrome is a web browser and Windows Media Player plays audio and video.",
  seconds=10)
Q(T, "DBMS concepts", "Intermediate",
  "A Transactions table has 50 crore rows, and queries that search by account number are slow. The DBA creates an "
  "index on the account-number column. What is the usual trade-off?",
  ["Searches by account number become faster, but inserts and updates become slightly slower and extra storage is "
   "used",
   "Every query on the table becomes faster with no cost at all",
   "The table's duplicate rows are removed automatically",
   "The column automatically becomes the table's primary key"],
  concept="Indexing",
  explanation="An index (usually a B-tree) lets the DBMS find matching rows without scanning the whole table, like "
              "the index of a book. But each insert, update or delete must also update the index, and the index "
              "takes extra disk space.",
  steps=["Index -> fast look-up on that column", "Cost -> slower writes + extra storage"],
  wrong="Indexes help only queries that can use them and always cost something. Creating an index does not remove "
        "duplicates or create a primary key.", seconds=30)
Q(T, "SQL basics", "Intermediate",
  "Table Customer has a column name with six rows: Asha, Ravi, Rahul, Karan, Arjun and Raman. How many rows does "
  "this query return?\nSELECT name FROM Customer WHERE name LIKE '_a%';",
  ["4", "2", "3", "6"],
  concept="SQL LIKE wildcards",
  explanation="In LIKE patterns, _ matches exactly one character and % matches any number of characters. '_a%' "
              "means 'any one character, then a, then anything': the second letter must be 'a'. That fits Ravi, "
              "Rahul, Karan and Raman, but not Asha (s) or Arjun (r).",
  steps=["_ = one character, % = any characters", "Second letter 'a': Ravi, Rahul, Karan, Raman", "Count = 4"],
  wrong="2 counts names starting with 'a' (pattern 'a%'). 6 counts names containing 'a' anywhere ('%a%'). 3 "
        "misses one of the four matches.", seconds=35, computed=True)
Q(T, "DBMS concepts", "Advanced",
  "Two tellers read the same balance of Rs 10,000 at the same moment. One deposits Rs 2,000 and writes 12,000; the "
  "other then withdraws Rs 1,000 and writes 9,000, overwriting the first write. The final balance should be "
  "11,000. Which concurrency problem is this?",
  ["Lost update", "Dirty read", "Phantom read", "Deadlock"],
  concept="Concurrency anomalies",
  explanation="In a lost update, two transactions read the same value and both write back, so the later write "
              "overwrites the earlier one and its change is lost. Locking (for example SELECT ... FOR UPDATE) or a "
              "suitable isolation level prevents it.",
  steps=["Both read 10,000", "Writes 12,000, then 9,000 overwrites it", "The deposit is lost = lost update"],
  wrong="A dirty read reads uncommitted data that is later rolled back. A phantom read sees new rows appear when a "
        "query is repeated. A deadlock is two transactions waiting for each other's locks.", seconds=35)
Q(T, "SQL basics", "Advanced",
  "Table Savings holds customers Asha, Ravi, Meena and John. Table Loans holds Ravi, John and Farah. How many rows "
  "do these two queries return?\nQuery 1: SELECT cust FROM Savings UNION SELECT cust FROM Loans;\n"
  "Query 2: SELECT cust FROM Savings UNION ALL SELECT cust FROM Loans;",
  ["Query 1: 5 rows, Query 2: 7 rows", "Query 1: 7 rows, Query 2: 5 rows", "Query 1: 2 rows, Query 2: 7 rows",
   "Query 1: 5 rows, Query 2: 5 rows"],
  concept="UNION and UNION ALL",
  explanation="UNION combines both results and removes duplicates: Asha, Ravi, Meena, John, Farah = 5 rows. UNION "
              "ALL keeps duplicates: 4 + 3 = 7 rows (Ravi and John appear twice).",
  steps=["UNION removes duplicates -> 4 + 3 - 2 common = 5", "UNION ALL keeps all -> 4 + 3 = 7"],
  wrong="The reverse pairing swaps the two operators. 2 rows is INTERSECT (customers in both tables). UNION ALL "
        "does not remove duplicates, so it cannot return 5 here.", seconds=40, computed=True)

# ================================================================ 11. MS Office (4 / 6 / 3)
T = "MS Office"
Q(T, "MS Word", "Basic",
  "In MS Word, which tool copies the formatting (font, size, colour) of selected text so that it can be applied to "
  "other text with a click?",
  ["Format Painter", "Find and Replace", "Spelling and Grammar", "Word Count"],
  concept="Copying formatting",
  explanation="Format Painter (the paintbrush icon on the Home tab) picks up the formatting of the selected text "
              "and applies it to the next text you select. Double-clicking it keeps it on for several uses.",
  steps=["Copy formatting only = Format Painter"],
  wrong="Find and Replace changes words, Spelling and Grammar checks errors, and Word Count counts words; none of "
        "them copies formatting.", seconds=10)
Q(T, "MS Excel", "Basic",
  "In MS Excel, a user types 'Jan' in a cell and drags the small square at the bottom-right corner of the cell "
  "down, and Feb, Mar, Apr ... fill the cells below. What is this small square called?",
  ["Fill handle", "Name box", "Formula bar", "Scroll bar"],
  concept="AutoFill",
  explanation="The fill handle is the small square at the bottom-right corner of the selected cell or range. "
              "Dragging it copies data or extends a series such as months, days or numbers (AutoFill).",
  steps=["Drag the corner square to extend a series = fill handle"],
  wrong="The name box shows the active cell's address, the formula bar shows its contents, and scroll bars move "
        "the view.", seconds=10)
Q(T, "MS PowerPoint", "Basic",
  "In PowerPoint, the visual effect seen when the presentation moves from one slide to the next, such as a fade or "
  "a push, is called a:",
  ["Transition", "Animation", "Theme", "Layout"],
  concept="Transitions and animations",
  explanation="A transition is applied to a slide and plays as that slide appears during a slide show. An animation "
              "is applied to an object (text, picture) within a slide.",
  steps=["Effect between slides = transition"],
  wrong="An animation moves objects within a slide. A theme sets colours and fonts for the whole presentation. A "
        "layout arranges placeholders on a slide.", seconds=10)
Q(T, "Shortcuts", "Basic",
  "In MS Word for Windows, which key starts the spelling and grammar check of the document (shown in the Editor "
  "pane in current versions)?",
  ["F7", "F5", "F12", "F1"],
  concept="Word function keys",
  explanation="Pressing F7 in Word opens the Editor task pane to check spelling and grammar in the document or the "
              "selected text.",
  steps=["Spelling and grammar = F7"],
  wrong="F5 opens Go To in Word, F12 opens Save As, and F1 opens Help.", seconds=10,
  facts=[fact("Microsoft keyboard shortcuts in Word: F7 alone displays the Editor task pane to check spelling and "
              "grammar in the document or the selected text.", MS_WORD)])
Q(T, "MS Excel", "Intermediate",
  "In Excel, A1 contains 5000 and B1 contains 0. What does =IFERROR(A1/B1, \"NA\") return?",
  ["NA", "#DIV/0!", "0", "5000"],
  concept="IFERROR",
  explanation="A1/B1 divides by zero, which gives the #DIV/0! error. IFERROR returns its second argument when the "
              "first one evaluates to an error, so the cell shows NA.",
  steps=["5000 / 0 -> #DIV/0!", "Error -> IFERROR returns \"NA\""],
  wrong="#DIV/0! is what A1/B1 shows without IFERROR. IFERROR does not change an error into 0 or into the "
        "numerator; it returns exactly the value given.", seconds=25, computed=True,
  facts=[fact("Microsoft: IFERROR returns a value you specify if a formula evaluates to an error; otherwise, it "
              "returns the result of the formula. It handles #DIV/0! among other errors.", MS_IFERROR)])
Q(T, "MS Excel", "Intermediate",
  "A clerk types =SUMM(B2:B10) in an Excel cell. Which error value appears?",
  ["#NAME?", "#VALUE!", "#REF!", "#N/A"],
  concept="Excel error values",
  explanation="Excel does not recognise the function name SUMM, so it shows #NAME?. A typo in a function name is "
              "the most common cause of this error.",
  steps=["Unknown function name -> #NAME?"],
  wrong="#VALUE! means a wrong type of argument (such as text in arithmetic), #REF! means an invalid cell "
        "reference, and #N/A means a lookup value was not found.", seconds=20,
  facts=[fact("Microsoft: the top reason why the #NAME? error appears in a formula is a typo in the formula name.",
              MS_NAME)])
Q(T, "MS Excel", "Intermediate",
  "An Excel sheet has 20,000 loan records with columns Branch, Month, Product and Amount. The manager wants an "
  "interactive summary of total Amount by Branch and Month that can be rearranged by dragging fields. Which "
  "feature should be used?",
  ["PivotTable", "Freeze Panes", "Mail Merge", "Text to Columns"],
  concept="PivotTables",
  explanation="A PivotTable summarises large data (sum, count, average) grouped by the fields you choose. Fields "
              "can be dragged between rows, columns, values and filters to change the summary instantly.",
  steps=["Interactive summary by groups = PivotTable"],
  wrong="Freeze Panes keeps headings visible while scrolling. Mail Merge is a Word feature for personalised "
        "letters. Text to Columns splits one column into several.", seconds=20)
Q(T, "MS Word", "Intermediate",
  "A Word report is in portrait orientation, but page 5 holds a wide table that must be printed in landscape. "
  "What must the document have so that only that page can be landscape?",
  ["Section breaks before and after that page", "A page break before that page", "A column break",
   "A text box around the table"],
  concept="Section breaks",
  explanation="Page setup settings such as orientation and margins apply to a whole section. Putting section "
              "breaks around page 5 makes it a separate section that can be landscape while the rest stays "
              "portrait. (If the content is selected first, Word inserts the breaks automatically.)",
  steps=["Orientation applies per section", "Section breaks around page 5 -> landscape for that section only"],
  wrong="A page break only starts a new page; the page is still in the same section, so its orientation cannot "
        "differ. A column break works inside columns, and a text box does not change page orientation.",
  seconds=25, web=SC,
  facts=[fact("Microsoft support (print with landscape orientation in Word): to change orientation for part of a "
              "document, the document must be divided by section breaks and the orientation applied to that "
              "section.", MS_LANDSCAPE)])
Q(T, "MS PowerPoint", "Intermediate",
  "A presenter connects a laptop to a projector. She wants the audience to see only the slides while her laptop "
  "screen also shows her speaker notes. Which PowerPoint feature does this?",
  ["Presenter View", "Slide Sorter view", "Outline view", "Reading View"],
  concept="Presenter View",
  explanation="Presenter View shows the speaker notes, a timer and the next slide on the presenter's screen, while "
              "the projector shows only the slides.",
  steps=["Notes on presenter's screen, slides for audience = Presenter View"],
  wrong="Slide Sorter shows thumbnails for reordering, Outline view shows slide text as an outline, and Reading "
        "View plays the presentation in a window; none splits notes and slides across two screens.", seconds=20,
  facts=[fact("Microsoft: Presenter View lets you view your presentation with speaker notes on one computer while "
              "only the slides appear on the screen the audience sees.", MS_PRESENTER)])
Q(T, "Shortcuts", "Intermediate",
  "In Excel for Windows, which keyboard shortcut opens the Format Cells dialog box?",
  ["Ctrl + 1", "Ctrl + F", "Ctrl + Shift + F3", "Alt + F1"],
  concept="Excel shortcuts",
  explanation="Ctrl + 1 opens the Format Cells dialog, where number format, alignment, font, border, fill and "
              "protection can be set.",
  steps=["Format Cells = Ctrl + 1"],
  wrong="Ctrl + F opens Find, Ctrl + Shift + F3 creates names from a selection, and Alt + F1 inserts a chart of the "
        "selected data.", seconds=15,
  facts=[fact("Microsoft keyboard shortcuts in Excel: open the Format Cells dialog box - Ctrl+1.", MS_EXCEL)])
o, a = ordered(2, [-2, -1, 1])
Q(T, "MS Excel", "Advanced",
  "What value does the Excel formula =MOD(-7, 3) return?", o, a,
  concept="Excel MOD with negative numbers",
  explanation="Excel's MOD returns a result with the same sign as the divisor, using MOD(n, d) = n - d x INT(n/d). "
              "INT(-7/3) = INT(-2.33) = -3, so MOD = -7 - 3 x (-3) = -7 + 9 = 2.",
  steps=["-7 / 3 = -2.33", "INT(-2.33) = -3 (rounds down)", "-7 - 3 x (-3) = 2"],
  shortcut="The result always has the divisor's sign, so with divisor 3 the answer lies between 0 and 2.",
  wrong="-1 is the truncated remainder that some programming languages return (-7 = 3 x (-2) - 1). -2 and 1 come "
        "from sign errors.", seconds=40, computed=True,
  facts=[fact("Microsoft MOD function: returns the remainder after number is divided by divisor; the result has the "
              "same sign as divisor (e.g. =MOD(-3, 2) returns 1).", MS_MOD)])
o, a = ordered(WILD, [0, 1, 4])
Q(T, "MS Excel", "Advanced",
  "Cells A1:A6 contain Sharma, Singh, Asha, Suresh, Kumar and Sinha. What does =COUNTIF(A1:A6, \"S?n*\") return?",
  o, a,
  concept="Wildcards in COUNTIF",
  explanation="In criteria, ? matches exactly one character and * matches any sequence. 'S?n*' means: S, any one "
              "letter, n, then anything. Singh (S-i-n) and Sinha (S-i-n) match. Sharma (S-h-a) and Suresh (S-u-r) "
              "do not, and Asha and Kumar do not start with S.",
  steps=["Pattern: S + one character + n + anything", "Matches: Singh, Sinha", "Count = 2"],
  wrong="4 counts every name starting with S (\"S*\"). 1 and 0 miss matches.", seconds=40, computed=True,
  facts=[fact("Microsoft COUNTIF: a question mark matches any single character; an asterisk matches any sequence "
              "of characters.", MS_COUNTIF)])
Q(T, "MS Excel", "Advanced",
  "B4 holds an EMI formula that depends on the loan amount in B1. A loan officer wants Excel to find the loan amount "
  "that makes the EMI exactly Rs 15,000 by changing B1 automatically. Which tool should be used?",
  ["Goal Seek (Data > What-If Analysis)", "Data Validation", "Conditional Formatting", "Remove Duplicates"],
  concept="What-If Analysis",
  explanation="Goal Seek works backwards: you give the formula cell (B4), the result wanted (15000) and the input "
              "cell to change (B1), and Excel adjusts the input until the formula reaches the target.",
  steps=["Known result, unknown input = Goal Seek"],
  wrong="Data Validation restricts what can be entered, Conditional Formatting changes cell appearance based on "
        "values, and Remove Duplicates deletes repeated rows; none of them solves for an input.", seconds=25,
  facts=[fact("Microsoft: Goal Seek finds the input value a formula needs to produce a result you want; it is under "
              "Data > What-If Analysis.", MS_GOAL)])

# ================================================================ 12. Digital Payments (1 / 2 / 1)
T = "Digital Payments"
Q(T, "Payment technology", "Basic",
  "At a shop's billing counter, the customer inserts or taps a debit card on a small machine that reads the card "
  "and sends the payment for authorisation. What is this machine called?",
  ["POS (Point of Sale) terminal", "ATM (Automated Teller Machine)", "Cash deposit machine", "Passbook printer"],
  concept="Card acceptance devices",
  explanation="A POS terminal at a merchant reads cards (chip, stripe or contactless), takes the PIN when needed "
              "and sends the transaction through the acquirer for approval.",
  steps=["Card payment machine at a shop = POS terminal"],
  wrong="An ATM dispenses cash to cardholders, a cash deposit machine accepts cash, and a passbook printer updates "
        "passbooks at a branch.", seconds=10)
Q(T, "Card security", "Intermediate",
  "A customer buys a train ticket online by typing his card number, expiry date and CVV; the card itself is never "
  "physically read by a terminal. How is such a payment classified?",
  ["Card-not-present (CNP) transaction", "Card-present transaction", "Cash-on-delivery transaction",
   "Offline chip transaction"],
  concept="Card-present and card-not-present",
  explanation="In a CNP transaction (online, phone or mail order) the merchant cannot check the physical card or "
              "chip, so CNP payments carry a higher fraud risk. Extra checks such as the CVV and OTP-based "
              "authentication are used.",
  steps=["Card not physically read = card-not-present"],
  wrong="A card-present transaction reads the card at a terminal. Cash on delivery uses no card. An offline chip "
        "transaction happens at a terminal with the chip inserted.", seconds=20)
Q(T, "Payment technology", "Intermediate",
  "Which NPCI service lets users of basic feature phones (without internet or smartphone apps) make UPI payments, "
  "for example by calling an IVR number or giving a missed call?",
  ["UPI 123PAY", "BHIM Aadhaar Pay", "NETC FASTag", "Bharat BillPay"],
  concept="UPI for feature phones",
  explanation="UPI 123PAY gives feature-phone users UPI options such as IVR calls, missed calls, apps built into "
              "feature phones and sound-based proximity payments; the payment is authorised with the UPI PIN.",
  steps=["UPI without internet on a feature phone = UPI 123PAY"],
  wrong="BHIM Aadhaar Pay lets merchants accept payments using the customer's Aadhaar and fingerprint. NETC FASTag "
        "is for toll payment, and Bharat BillPay is for paying bills.", seconds=20, web=SC,
  facts=[fact("NPCI: UPI 123PAY offers feature phone users options that work without internet, including calling "
              "an IVR number, app functionality in feature phones, a missed-call-based approach and proximity "
              "sound-based payments.", NPCI_123PAY)])
Q(T, "Payment technology", "Advanced",
  "A banking app lets an Android phone make contactless card payments at NFC terminals. Instead of storing the "
  "card in a separate secure-element chip, the app itself emulates the card and talks to the reader through the "
  "phone's NFC controller. What is this technique called?",
  ["Host Card Emulation (HCE)", "Magnetic Secure Transmission (MST)", "Dynamic QR code", "Card skimming"],
  concept="Host Card Emulation",
  explanation="On Android 4.4 and later, host-based card emulation routes NFC data from the reader to an app on "
              "the host CPU, so a payment app can emulate a contactless card without a secure element. The app "
              "usually relies on tokens instead of the real card number.",
  steps=["App emulates the card, no secure element = Host Card Emulation"],
  wrong="MST imitates a magnetic stripe signal for old swipe terminals. A dynamic QR code is scanned with a camera, "
        "not NFC. Card skimming is a fraud, not a payment technology.", seconds=30,
  facts=[fact("Android developers: Android 4.4 and higher provide a method of card emulation that does not involve "
              "a secure element, called host-based card emulation, which allows any Android application to "
              "emulate a card and talk directly to the NFC reader.", ANDROID_HCE)])

# ================================================================ 13. Computer Abbreviations (2 / 1 / 1)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic", "What does CPU stand for?",
  ["Central Processing Unit", "Central Program Utility", "Computer Processing Unit", "Control Peripheral Unit"],
  concept="Hardware abbreviations",
  explanation="The CPU (Central Processing Unit) is the processor that fetches, decodes and executes instructions; "
              "it contains the ALU, the control unit and registers.",
  steps=["CPU = Central Processing Unit"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic", "Databases are queried using SQL. What does SQL stand for?",
  ["Structured Query Language", "Simple Query Logic", "Standard Question Language", "Sequential Query List"],
  concept="Database abbreviations",
  explanation="SQL (Structured Query Language) is the standard language for defining, querying and changing data "
              "in relational databases.",
  steps=["SQL = Structured Query Language"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "A fintech app fetches a customer's account balance from the bank's systems through a published interface "
  "called an API. What does API stand for?",
  ["Application Programming Interface", "Advanced Program Integration", "Automated Payment Interface",
   "Application Protocol Internet"],
  concept="Software abbreviations",
  explanation="An API (Application Programming Interface) is a defined set of requests and responses through which "
              "one program uses the services or data of another.",
  steps=["API = Application Programming Interface"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Advanced",
  "IP address blocks such as 10.20.0.0/16 are written in CIDR notation. What does CIDR stand for?",
  ["Classless Inter-Domain Routing", "Classified Internet Data Routing", "Common IP Distribution Register",
   "Centralised Internet Domain Registry"],
  concept="Networking abbreviations",
  explanation="CIDR (Classless Inter-Domain Routing) replaced the fixed class A, B and C system. The /16 shows how "
              "many leading bits form the network prefix.",
  steps=["CIDR = Classless Inter-Domain Routing"], wrong="The other expansions are made up.", seconds=15)

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_005_plan.json").read_text(encoding="utf-8"))
cplan = next(s for s in plan["subjects"] if s["subject"] == CK)
want = Counter({(t["topic"], d): n for t in cplan["topics"] for d, n in t["quota"].items() if n})
got = Counter((q["topic"], q["difficulty"]) for q in questions)
assert got == want, (got - want, want - got)
subs = {t["topic"]: set(t["subtopics"]) for t in cplan["topics"]}
for q in questions:
    assert q["subtopic"] in subs[q["topic"]], (q["question_id"], q["subtopic"])
    final = q["solution"]["final_answer"]
    assert final.startswith(f"Option {q['correct_answer']}: ")
assert len(questions) == 100
assert questions[0]["question_id"] == cplan["question_ids"][0] and questions[-1]["question_id"] == cplan["question_ids"][1]
keys = Counter(q["correct_answer"] for q in questions)
assert max(keys.values()) <= 28 and min(keys.values()) >= 22, keys

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_005",
    "created_at": TODAY,
    "notes": "BATCH_005 Computer Knowledge part: 100 original questions (BANK_COMP_000403 to BANK_COMP_000502). "
             "Computable answers (sign-magnitude, ASCII offset, two's-complement overflow, IEEE 754 exponent via "
             "struct, clock multiplier, little-endian byte order, aspect ratio, webcam data rate, SRTF/SJF/FCFS "
             "waiting times, FIFO faults for Belady's anomaly, page-table size, QLC levels, collision/broadcast "
             "domains, SQL LIKE and UNION/UNION ALL via sqlite3, Excel IFERROR, MOD and COUNTIF wildcards) are "
             "re-derived in tools/batch_005/computer.py. Windows/Word/Excel shortcuts, IFERROR, #NAME?, MOD, "
             "COUNTIF wildcards, Goal Seek, Presenter View, HTTP status classes, HSTS, DMARC, HTTP/3 over QUIC/UDP, "
             "S/MIME, IPv6 size, DNS port 53, HSM, IT Act s.66D, Hollerith's punched cards, Moore's 1975 revision "
             "and Android HCE were checked on the cited pages on 2026-11-05; the Word section-break rule, EUI-48 "
             "MAC length and UPI 123PAY were confirmed from search results only (web:search-confirmed).",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_005_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
