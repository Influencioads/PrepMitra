"""Writes batches/parts/BATCH_002_COMP.json: the 100 Computer Knowledge questions of BATCH_002.

Every computable answer (number systems, BCD, two's complement range, CPU time, scheduling, page replacement,
memory addressing, disk latency, cache mapping, pixel density, subnet masks, transfer time, Luhn check digit, SQL
results on given tables, Excel formula results) is re-derived below with assertions before the file is written.
The plan quota per (topic, difficulty) and the ID range are also asserted. If any assertion fails, nothing is written.

    python tools/batch_002/computer.py      (run from docs/question-bank)
"""

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
FIRST_ID = 103
AI = ("ai:author-solve", "ai:independent-check")
COMPUTED = ("script:recompute", "ai:author-solve", "ai:independent-check")

_rng = random.Random(20261105 + 2)
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
      shortcut=None, computed=False, facts=None):
    """Adds one question. With answer=None, options[0] is the correct text and it is placed at the least-used key
    so far (random tie-break, fixed seed). Ordered options (numbers) pass an explicit answer letter."""
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
        vb.append("web:fact-check")
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
# Number systems
assert int("11111111", 2) == 255 and 2**8 == 256
assert format(200, "X") == "C8" and int("8C", 16) == 140 and int("D8", 16) == 216 and int("CC", 16) == 204
assert int("1011", 2) * int("101", 2) == 55 and format(55, "b") == "110111"
assert [int(x, 2) for x in ("101111", "110011", "111011")] == [47, 51, 59]
bcd = lambda n: " ".join(format(int(d), "04b") for d in str(n))
assert bcd(59) == "0101 1001" and format(59, "08b") == "00111011"
assert (-(2**7), 2**7 - 1) == (-128, 127)
assert int("A3", 16) + int("5E", 16) == 0x101 and format(0x101, "X") == "101"

# CPU time = instructions x CPI / clock rate
assert F(2 * 10**9) * F(3, 2) / F(3 * 10**9) == 1

# FCFS and SJF waiting times for bursts 18, 6, 3 (all arrive at 0, order P1, P2, P3)
BURSTS = [18, 6, 3]


def avg_wait(bursts):
    t, waits = 0, []
    for b in bursts:
        waits.append(t)
        t += b
    return F(sum(waits), len(waits))


def avg_tat(bursts):
    t, tats = 0, []
    for b in bursts:
        t += b
        tats.append(t)
    return F(sum(tats), len(tats))


FCFS_W, SJF_W, FCFS_T = avg_wait(BURSTS), avg_wait(sorted(BURSTS)), avg_tat(BURSTS)
assert (FCFS_W, SJF_W, FCFS_T) == (14, 4, 23)

# Page replacement on reference string with 3 frames
REFS = [4, 7, 4, 1, 7, 2, 4, 3, 7]


def fifo_faults(refs, n):
    frames, faults = [], 0
    for p in refs:
        if p not in frames:
            faults += 1
            if len(frames) == n:
                frames.pop(0)
            frames.append(p)
    return faults


def optimal_faults(refs, n):
    frames, faults = [], 0
    for i, p in enumerate(refs):
        if p in frames:
            continue
        faults += 1
        if len(frames) == n:
            fut = refs[i + 1:]
            victim = max(frames, key=lambda f: fut.index(f) if f in fut else 10**9)
            frames.remove(victim)
        frames.append(p)
    return faults


assert fifo_faults(REFS, 3) == 7 and optimal_faults(REFS, 3) == 5

# Memory and disk
assert 2**16 == 65536 == 64 * 1024
LAT_MS = F(60 * 1000, 7200) / 2
assert round(float(LAT_MS), 2) == 4.17 and round(float(F(60000, 7200)), 2) == 8.33
assert 1000 % 128 == 104 and 1000 // 128 == 7

# Display pixel density
PPI = math.hypot(2560, 1440) / 27
assert round(PPI) == 109 and round(math.hypot(1920, 1080) / 24) == 92

# Networking
assert str(ipaddress.ip_network("0.0.0.0/20").netmask) == "255.255.240.0"
assert str(ipaddress.ip_network("0.0.0.0/19").netmask) == "255.255.224.0"
assert str(ipaddress.ip_network("0.0.0.0/21").netmask) == "255.255.248.0"
PRIVATE_BLOCKS = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")]
is_rfc1918 = lambda a: any(ipaddress.ip_address(a) in b for b in PRIVATE_BLOCKS)
assert is_rfc1918("172.20.5.4") and not any(map(is_rfc1918, ["172.32.1.1", "192.169.1.1", "11.0.0.1"]))
assert F(25 * 10**6 * 8, 50 * 10**6) == 4


# Luhn check digit
def luhn_check_digit(payload):
    total = 0
    for i, ch in enumerate(reversed(payload)):
        d = int(ch)
        if i % 2 == 0:  # these digits get doubled once the check digit is appended
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - total % 10) % 10


def luhn_valid(number):
    total = 0
    for i, ch in enumerate(reversed(number)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


assert luhn_check_digit("7992739871") == 3  # published textbook example, used only as a self-test
LUHN_PAYLOAD = "6082419"
LUHN_DIGIT = luhn_check_digit(LUHN_PAYLOAD)
assert LUHN_DIGIT == 0 and luhn_valid(LUHN_PAYLOAD + "0")
# Distractors: doubling the wrong set of digits gives 7; not subtracting 9 from doubled values gives 3
assert luhn_check_digit("6082419" + "") == 0 and (10 - (2 + 4 + 0 + 9 + 4 + 8 + 6) % 10) % 10 == 7
assert (10 - (18 + 8 + 16 + 12 + 1 + 2 + 0) % 10) % 10 == 3
assert sum(not luhn_valid(LUHN_PAYLOAD + str(d)) for d in range(10)) == 9

# SQL
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Customers (cust_id INTEGER PRIMARY KEY, name TEXT, city TEXT)")
db.execute("CREATE TABLE Loans (loan_id TEXT PRIMARY KEY, cust_id INTEGER, amount INTEGER)")
CUSTOMERS = [(1, "Asha", "Pune"), (2, "Ravi", "Delhi"), (3, "Meena", "Pune"), (4, "John", "Agra"),
             (5, "Farah", "Delhi"), (6, "Kiran", "Agra")]
LOANS = [("L1", 1, 500000), ("L2", 1, 200000), ("L3", 3, 800000), ("L4", 5, 150000)]
db.executemany("INSERT INTO Customers VALUES (?, ?, ?)", CUSTOMERS)
db.executemany("INSERT INTO Loans VALUES (?, ?, ?)", LOANS)
SQL_LJ = "SELECT c.name, l.loan_id FROM Customers c LEFT JOIN Loans l ON c.cust_id = l.cust_id"
SQL_IJ = "SELECT c.name, l.loan_id FROM Customers c INNER JOIN Loans l ON c.cust_id = l.cust_id"
assert len(db.execute(SQL_LJ).fetchall()) == 7 and len(db.execute(SQL_IJ).fetchall()) == 4
db.execute("CREATE TABLE Staff (emp TEXT, bonus INTEGER)")
STAFF = [("E1", 4000), ("E2", None), ("E3", 6000), ("E4", 8000), ("E5", None)]
db.executemany("INSERT INTO Staff VALUES (?, ?)", STAFF)
assert db.execute("SELECT AVG(bonus), COUNT(*), COUNT(bonus), SUM(bonus) FROM Staff").fetchone() == (6000.0, 5, 3,
                                                                                                    18000)
assert 18000 / 5 == 3600 and 18000 / 4 == 4500

# Excel
TRIM_IN = "  Bank   of  India "
TRIM_OUT = " ".join(w for w in TRIM_IN.split(" ") if w)
assert TRIM_OUT == "Bank of India" and len(TRIM_OUT) == 13 and len(TRIM_IN) == 19
# ROUND(1234.567, -2): round half away from zero to the nearest hundred
assert int(F("1234.567") / 100 + F(1, 2)) * 100 == 1200


def excel_if_demo(b2, c2):
    if b2 > 50000 and c2 == "Yes":
        return "Eligible"
    if b2 > 60000 or c2 == "Yes":
        return "Review"
    return "Reject"


assert excel_if_demo(72000, "No") == "Review"
NAME = "Kumar, Asha"
find_comma = NAME.index(",") + 1  # FIND is 1-based
assert find_comma == 6
assert NAME[find_comma + 2 - 1:][:len(NAME)] == "Asha"  # MID(A1, 8, 11) runs to the end of the text

# ---------------------------------------------------------------- fact-check sources (pages opened 2026-11-05)
MS_WORD = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2"
MS_EXCEL = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-9b7213f0040f"
MS_PPT = ("https://support.microsoft.com/en-us/office/use-keyboard-shortcuts-to-deliver-powerpoint-presentations-"
          "1524ffce-bd2a-45f4-9a7f-f18b992b93a0")
MS_WIN = "https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec"
MS_ROUND = "https://support.microsoft.com/en-us/office/round-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c"
MS_TRIM = "https://support.microsoft.com/en-us/office/trim-function-410388fa-c5df-49c6-b16c-9e5630b479f9"
MS_MID = "https://support.microsoft.com/en-us/office/mid-midb-functions-d5f9e25c-d7d6-472e-b568-4ecb12433028"
RFC1918 = "https://www.rfc-editor.org/rfc/rfc1918"
RFC1122 = "https://www.rfc-editor.org/rfc/rfc1122"
RFC9293 = "https://www.rfc-editor.org/rfc/rfc9293"
RFC1035 = "https://www.rfc-editor.org/rfc/rfc1035"
RFC3596 = "https://www.rfc-editor.org/rfc/rfc3596"
MDN_GET = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods/GET"
EMV_3DS = "https://www.emvco.com/emv-technologies/3-d-secure/"

# ================================================================ 1. Computer Fundamentals (4 / 1 / 4)
T = "Computer Fundamentals"
Q(T, "Generations and history", "Basic",
  "Who designed the Analytical Engine, a mechanical machine with a 'mill' for calculation and a 'store' for "
  "memory that is regarded as the first design of a general-purpose computer?",
  ["Charles Babbage", "Blaise Pascal", "Herman Hollerith", "John von Neumann"],
  concept="Pioneers of computing",
  explanation="Charles Babbage designed the Analytical Engine in the 1830s. Its 'mill' worked like a modern CPU "
              "and its 'store' like memory, and it was to be programmed with punched cards, which is why Babbage "
              "is called the father of the computer.",
  steps=["Analytical Engine (mill + store, punched cards) = Charles Babbage"],
  wrong="Pascal built the Pascaline, an adding machine. Hollerith built the punched-card tabulator for the 1890 US "
        "census. Von Neumann described the stored-program architecture in the 1940s.", seconds=20)
o, a = ordered(255, [127, 256, 511])
Q(T, "Number systems", "Basic",
  "What is the decimal value of the binary number 11111111?", o, a,
  concept="Binary to decimal; all-ones numbers",
  explanation="A binary number made of n ones equals 2^n - 1. Eight ones give 2^8 - 1 = 255, which is the largest "
              "value an unsigned byte can hold.",
  steps=["128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255", "Or: 2^8 - 1 = 256 - 1 = 255"],
  shortcut="n ones in binary = 2^n - 1.",
  wrong="127 is seven ones (1111111). 256 is 2^8, which needs nine bits (100000000). 511 is nine ones.",
  seconds=25, computed=True)
Q(T, "Types of computers", "Basic",
  "The small computer built into a washing machine to control its wash cycle, which performs only that one "
  "dedicated task, is an example of a(n):",
  ["Embedded computer", "Mainframe computer", "Supercomputer", "Workstation"],
  concept="Embedded systems",
  explanation="An embedded computer is a microcontroller built inside another device to do one dedicated job, such as "
              "running a washing machine, microwave oven, ATM keypad or car engine control unit.",
  steps=["Built inside an appliance + one dedicated task = embedded computer"],
  wrong="Mainframes serve thousands of users, supercomputers do massive scientific calculations, and workstations "
        "are powerful single-user desktops. None is built into an appliance.", seconds=20)
Q(T, "Types of computers", "Basic",
  "Which type of computer is used for weather forecasting, climate modelling and nuclear simulations, where "
  "trillions of calculations per second are needed?",
  ["Supercomputer", "Minicomputer", "Personal computer", "Embedded computer"],
  concept="Classification of computers by power",
  explanation="Supercomputers are the fastest computers. They use thousands of processors working in parallel and "
              "their speed is measured in FLOPS (floating-point operations per second). India's PARAM series are "
              "supercomputers.",
  steps=["Massive scientific calculation (weather, simulations) = supercomputer"],
  wrong="Minicomputers and personal computers are far too slow for such workloads, and embedded computers do a "
        "single small control task.", seconds=20)
Q(T, "Number systems", "Intermediate",
  "What is the hexadecimal equivalent of the decimal number 200?",
  ["C8", "8C", "CC", "D8"],
  concept="Decimal to hexadecimal by repeated division by 16",
  explanation="200 / 16 = 12 remainder 8. 12 is written C in hexadecimal, so 200 = C8 (hex). Check: 12 x 16 + 8 = 200.",
  steps=["200 / 16 = 12 r 8", "12 = C, so read C then 8", "C8 = 12 x 16 + 8 = 200"],
  wrong="8C = 140 (digits reversed), CC = 204 and D8 = 216.", seconds=35, computed=True)
o, a = ordered(55, [47, 51, 59], lambda v: format(v, "b"))
Q(T, "Number systems", "Advanced",
  "What is the product of the binary numbers 1011 and 101, written in binary?", o, a,
  concept="Binary multiplication (shift and add)",
  explanation="Multiply as in decimal: for each 1 in the multiplier, write the multiplicand shifted left, then add. "
              "1011 x 101 = 1011 + 101100 = 110111. Check in decimal: 11 x 5 = 55 = 110111.",
  steps=["1011 x 1 = 1011", "1011 x 0 (shifted one place) = 0", "1011 x 1 (shifted two places) = 101100",
         "1011 + 101100 = 110111", "Check: 11 x 5 = 55 = 32 + 16 + 4 + 2 + 1"],
  shortcut="Convert to decimal, multiply, convert back: 11 x 5 = 55 = 110111.",
  wrong="101111 = 47, 110011 = 51 and 111011 = 59; none equals 11 x 5.", seconds=60, computed=True)
Q(T, "Number systems", "Advanced",
  "What is the BCD (Binary Coded Decimal, 8421 code) representation of the decimal number 59?",
  ["0101 1001", "0011 1011", "1001 0101", "0101 1010"],
  concept="BCD: each decimal digit coded separately in 4 bits",
  explanation="In BCD each decimal digit is replaced by its own 4-bit binary code. 5 = 0101 and 9 = 1001, so "
              "59 = 0101 1001. This differs from the pure binary value of 59, which is 0011 1011.",
  steps=["5 -> 0101", "9 -> 1001", "59 -> 0101 1001"],
  wrong="0011 1011 is 59 in pure binary, not BCD. 1001 0101 codes the digits in reverse order (95). 0101 1010 "
        "would need the invalid BCD group 1010 (ten).", seconds=40, computed=True)
Q(T, "Number systems", "Advanced",
  "What range of integers can be stored in 8 bits using two's complement representation?",
  ["-128 to +127", "-127 to +127", "-128 to +128", "0 to 255"],
  concept="Range of n-bit two's complement numbers",
  explanation="With n bits, two's complement stores -2^(n-1) to 2^(n-1) - 1. For 8 bits that is -128 to +127. "
              "There is only one zero (00000000), so one extra negative number (10000000 = -128) fits.",
  steps=["n = 8", "Lowest = -2^7 = -128", "Highest = 2^7 - 1 = +127"],
  wrong="-127 to +127 is the range of sign-magnitude and one's complement, which have two zeros. +128 does not fit "
        "in 8-bit two's complement. 0 to 255 is the unsigned range.", seconds=35, computed=True)
o, a = ordered(0x101, [0xF1, 0xFF, 0x111], lambda v: format(v, "X"))
Q(T, "Number systems", "Advanced",
  "What is the sum of the hexadecimal numbers A3 and 5E, in hexadecimal?", o, a,
  concept="Hexadecimal addition with carry",
  explanation="Add column by column in base 16. 3 + E = 3 + 14 = 17 = 16 + 1, so write 1 and carry 1. Then "
              "A + 5 + 1 = 10 + 5 + 1 = 16, so write 0 and carry 1. The result is 101 (hex) = 257.",
  steps=["Units: 3 + 14 = 17 = 1 carry 1", "Sixteens: 10 + 5 + 1 = 16 = 0 carry 1", "Result: 101 (hex)",
         "Check: 163 + 94 = 257 = 1 x 256 + 0 x 16 + 1"],
  wrong="F1 (241) and FF (255) ignore a carry; 111 (273) adds an extra carry.", seconds=50, computed=True)

# ================================================================ 2. Hardware (3 / 5 / 1)
T = "Hardware"
Q(T, "CPU and components", "Basic",
  "Which part of the CPU fetches instructions, decodes them and directs the other parts of the computer on how to "
  "carry them out?",
  ["Control Unit (CU)", "Arithmetic Logic Unit (ALU)", "Cache memory", "Power supply unit"],
  concept="Components of the CPU",
  explanation="The Control Unit acts as the CPU's manager. It fetches each instruction, decodes it and sends control "
              "signals to the ALU, memory and I/O devices. It does not do the calculations itself.",
  steps=["Fetch, decode, direct = Control Unit"],
  wrong="The ALU performs the arithmetic and logic but takes orders from the CU. Cache only stores data. The power "
        "supply unit is not part of the CPU.", seconds=20)
Q(T, "Motherboard and ports", "Basic",
  "The main printed circuit board of a computer, which holds the CPU socket, RAM slots and expansion slots and "
  "connects all other parts, is called the:",
  ["Motherboard", "Daughter board", "Hard disk", "SMPS"],
  concept="Motherboard",
  explanation="The motherboard (system board) is the main circuit board. The CPU, memory, storage, ports and "
              "expansion cards all connect through it.",
  steps=["Main board holding CPU, RAM and slots = motherboard"],
  wrong="A daughter board is a smaller add-on board that plugs into the motherboard. The hard disk is storage. "
        "The SMPS supplies power but does not connect the components.", seconds=15)
Q(T, "Motherboard and ports", "Basic",
  "Which port carries high-definition digital video and audio together over a single cable to a TV or monitor?",
  ["HDMI", "VGA", "PS/2", "RJ-11"],
  concept="Display ports",
  explanation="HDMI (High-Definition Multimedia Interface) carries digital video and audio over one cable.",
  steps=["Digital video + audio in one cable = HDMI"],
  wrong="VGA carries analog video only. PS/2 connects an old-style keyboard or mouse. RJ-11 is the telephone-line "
        "connector.", seconds=20)
Q(T, "CPU and components", "Intermediate",
  "In which order does a CPU carry out the basic steps of the instruction (machine) cycle?",
  ["Fetch, Decode, Execute, Store", "Decode, Fetch, Execute, Store", "Fetch, Execute, Decode, Store",
   "Execute, Fetch, Decode, Store"],
  concept="Instruction cycle",
  explanation="The CPU first fetches the instruction from memory (using the program counter), decodes it to "
              "know what to do, executes it, and finally stores (writes back) the result.",
  steps=["Fetch from memory", "Decode the instruction", "Execute it", "Store the result"],
  wrong="An instruction cannot be decoded before it is fetched, or executed before it is decoded.", seconds=20)
Q(T, "CPU and components", "Intermediate",
  "Which CPU register holds the address of the memory location that is about to be read from or written to?",
  ["Memory Address Register (MAR)", "Memory Data Register (MDR)", "Accumulator", "Instruction Register (IR)"],
  concept="Special-purpose registers",
  explanation="The MAR holds the address of the memory location being accessed. The data that is read or to be "
              "written passes through the MDR (also called the MBR).",
  steps=["Address being accessed = MAR", "Data being transferred = MDR"],
  wrong="The MDR holds the data, not the address. The accumulator holds intermediate ALU results. The IR holds the "
        "instruction currently being decoded.", seconds=25)
Q(T, "Motherboard and ports", "Intermediate",
  "A user wants to add a dedicated graphics card to a modern desktop. Which motherboard slot is normally used?",
  ["PCI Express (PCIe) x16 slot", "DIMM slot", "SATA port", "M.2 slot reserved for Wi-Fi cards"],
  concept="Expansion slots",
  explanation="Modern graphics cards plug into the PCI Express x16 slot, which gives them the widest, fastest link "
              "to the CPU.",
  steps=["Graphics card = expansion card", "Fastest expansion slot = PCIe x16"],
  wrong="DIMM slots hold RAM modules, SATA ports connect drives, and a Wi-Fi M.2 slot (Key E) is too small and slow "
        "for a graphics card.", seconds=25)
Q(T, "CPU and components", "Intermediate",
  "Of the three parts of the system bus, which one is unidirectional, carrying signals only from the CPU to memory "
  "and I/O devices?",
  ["Address bus", "Data bus", "Control bus", "All three are unidirectional"],
  concept="System bus: address, data and control",
  explanation="Only the CPU places addresses on the address bus, so it is one-way. Data flows both ways on the data "
              "bus (reads and writes), and the control bus carries signals in both directions (e.g. read/write "
              "from the CPU, interrupt requests to it).",
  steps=["Address: CPU -> memory/IO only", "Data: both ways", "Control: both ways"],
  wrong="The data bus must carry data to and from the CPU, and the control bus carries interrupt and ready signals "
        "back to the CPU, so they are bidirectional.", seconds=25)
Q(T, "CPU and components", "Intermediate",
  "Which processor is designed to perform thousands of similar calculations in parallel and is used for rendering "
  "graphics and training AI models?",
  ["GPU", "CPU", "ALU", "PSU"],
  concept="CPU vs GPU",
  explanation="A GPU (Graphics Processing Unit) has thousands of small cores that do the same operation on lots of "
              "data at once. That suits image rendering and the matrix calculations of machine learning.",
  steps=["Massive parallel calculation = GPU"],
  wrong="A CPU has a few powerful cores tuned for general, sequential work. The ALU is only a part of a processor. "
        "The PSU is the power supply.", seconds=20)
o, a = ordered(1, [F(1, 2), 2, F(9, 2)], lambda v: f"{float(v):g} second{'s' if v != 1 else ''}")
Q(T, "CPU and components", "Advanced",
  "A program executes 2 x 10^9 instructions on a processor with a clock rate of 3 GHz. On average each instruction "
  "takes 1.5 clock cycles (CPI = 1.5). How long does the program take to run?", o, a,
  concept="CPU time = instruction count x CPI / clock rate",
  explanation="Total clock cycles = 2 x 10^9 x 1.5 = 3 x 10^9. At 3 GHz the CPU completes 3 x 10^9 cycles per "
              "second, so the program takes exactly 1 second.",
  steps=["Cycles = 2 x 10^9 x 1.5 = 3 x 10^9", "Time = cycles / clock rate = 3 x 10^9 / 3 x 10^9 = 1 s"],
  wrong="0.5 s divides by CPI instead of multiplying. 2 s mixes up the instruction count and clock rate. 4.5 s "
        "multiplies all three numbers.", seconds=50, computed=True)

# ================================================================ 3. Software (2 / 2 / 3)
T = "Software"
Q(T, "System and application software", "Basic",
  "Which of the following is an example of application software?",
  ["A spreadsheet program", "An operating system", "A device driver", "A disk defragmenter"],
  concept="System software vs application software",
  explanation="Application software helps the user do a particular task, such as making a spreadsheet, writing a "
              "letter or editing photos. System software runs and maintains the computer itself.",
  steps=["User task (calculations in a sheet) = application software"],
  wrong="Operating systems, device drivers and utilities such as a disk defragmenter are system software.",
  seconds=15)
Q(T, "Programming languages", "Basic",
  "Which language can a computer's processor execute directly, without any translation?",
  ["Machine language", "Assembly language", "Python", "Java"],
  concept="Levels of programming languages",
  explanation="Machine language is written in binary (0s and 1s), the only form a processor understands directly. "
              "Every other language must be translated into it.",
  steps=["Binary instructions run directly = machine language"],
  wrong="Assembly language needs an assembler; Python and Java need an interpreter, compiler or virtual machine.",
  seconds=15)
Q(T, "Licensing", "Intermediate",
  "A PDF reader can be downloaded and used free of charge for as long as you like, but its source code is not "
  "published and you may not modify it. Such software is called:",
  ["Freeware", "Shareware", "Open-source software", "Public-domain software"],
  concept="Software licence types",
  explanation="Freeware costs nothing to use, without a time limit, but the author keeps the copyright and the "
              "source code closed.",
  steps=["Free + unlimited use + closed source = freeware"],
  wrong="Shareware must be paid for after a trial. Open-source software publishes its source code. Public-domain "
        "software carries no copyright at all.", seconds=25)
Q(T, "Programming languages", "Intermediate",
  "Which translator converts a program written with mnemonics such as MOV, ADD and JMP into machine code?",
  ["Assembler", "Compiler", "Interpreter", "Loader"],
  concept="Language translators",
  explanation="Mnemonics like MOV and ADD are assembly language. An assembler translates assembly language into "
              "machine code.",
  steps=["MOV/ADD/JMP = assembly language", "Assembly -> machine code = assembler"],
  wrong="Compilers and interpreters translate high-level languages. A loader places an executable in memory; it does "
        "not translate.", seconds=20)
Q(T, "Programming languages", "Advanced",
  "After compilation, a program exists as several object files that refer to functions in each other and in "
  "library files. Which program combines them into one executable file?",
  ["Linker", "Loader", "Debugger", "Interpreter"],
  concept="Compile, link, load",
  explanation="The linker resolves references between object files and libraries and joins them into one "
              "executable. The loader later copies that executable into memory to run it.",
  steps=["Source -> compiler -> object files", "Object files + libraries -> linker -> executable",
         "Executable -> loader -> memory"],
  wrong="The loader runs after linking, the debugger helps find errors, and an interpreter executes source code "
        "line by line without making an executable.", seconds=30)
Q(T, "Licensing", "Advanced",
  "A company wants to use an open-source library inside its closed-source banking app without publishing the "
  "app's source code. Which type of licence on the library allows this, as long as the copyright notice is kept?",
  ["A permissive licence such as MIT", "A strong copyleft licence such as GNU GPL",
   "A shareware licence", "No licence at all (all rights reserved by the author)"],
  concept="Permissive vs copyleft open-source licences",
  explanation="Permissive licences (MIT, BSD, Apache 2.0) let anyone use, modify and include the code in "
              "proprietary products, usually only requiring the copyright and licence notice to be kept.",
  steps=["Closed-source app + reuse allowed = permissive licence"],
  wrong="The GPL requires a distributed derived work to be released under the GPL too. Shareware is not "
        "open-source. Code without any licence cannot legally be copied or reused.", seconds=35)
Q(T, "Programming languages", "Advanced",
  "In object-oriented programming, class SavingsAccount is defined as a child of class Account and "
  "automatically gets Account's fields and methods such as deposit(). Which OOP concept is this?",
  ["Inheritance", "Encapsulation", "Abstraction", "Overloading"],
  concept="Pillars of OOP",
  explanation="Inheritance lets a child (derived) class reuse the fields and methods of a parent (base) class and "
              "add or override its own.",
  steps=["Child class reuses parent's members = inheritance"],
  wrong="Encapsulation hides data inside a class, abstraction shows only essential features, and overloading "
        "defines several methods with the same name but different parameters.", seconds=25)

# ================================================================ 4. Operating Systems (1 / 3 / 3)
T = "Operating Systems"
Q(T, "Windows and Linux basics", "Basic",
  "Which of the following is NOT an operating system?",
  ["Python", "Android", "Ubuntu", "macOS"],
  concept="Examples of operating systems",
  explanation="Python is a programming language. Android, Ubuntu (a Linux distribution) and macOS are operating "
              "systems.",
  steps=["Programming language, not OS = Python"],
  wrong="Android runs phones, Ubuntu is a Linux-based OS and macOS runs Apple computers; all are operating systems.",
  seconds=15)
Q(T, "Windows and Linux basics", "Intermediate",
  "A bank cashier leaves the counter for a few minutes. Which Windows keyboard shortcut locks the computer "
  "immediately?",
  ["Windows logo key + L", "Windows logo key + D", "Alt + F4", "Ctrl + Alt + Tab"],
  concept="Windows shortcuts",
  explanation="Windows logo key + L locks the PC, so the password or PIN is needed to continue. It is a good "
              "security habit whenever you leave a desk.",
  steps=["Lock = Windows + L"],
  wrong="Windows + D shows and hides the desktop but leaves the session open. Alt + F4 closes the active window. "
        "Ctrl + Alt + Tab shows open windows for switching.", seconds=15,
  facts=[fact("Windows logo key + L locks the computer; Windows logo key + D displays and hides the desktop.",
              MS_WIN)])
Q(T, "File systems", "Intermediate",
  "Which file system is the standard for Windows system drives and supports file-level permissions, journaling "
  "and very large files?",
  ["NTFS", "FAT32", "exFAT", "ext4"],
  concept="File systems",
  explanation="NTFS (New Technology File System) is the default file system for Windows system drives. It "
              "supports access permissions, a journal for crash recovery, encryption and very large files.",
  steps=["Windows system drive + permissions + journaling = NTFS"],
  wrong="FAT32 and exFAT have no file permissions or journaling and are mainly used on removable drives. ext4 is a "
        "Linux file system.", seconds=20)
Q(T, "Functions", "Intermediate",
  "When RAM is not large enough for all running programs, the operating system uses part of the hard disk or SSD "
  "as an extension of main memory. This technique is called:",
  ["Virtual memory", "Cache memory", "Spooling", "Defragmentation"],
  concept="Memory management by the OS",
  explanation="Virtual memory moves pages that are not being used from RAM to a page file or swap space on disk, "
              "so programs can use more memory than is physically installed.",
  steps=["Disk used as extension of RAM = virtual memory"],
  wrong="Cache is a small, fast memory near the CPU. Spooling queues jobs (e.g. print jobs) on disk. "
        "Defragmentation rearranges file fragments on a hard disk.", seconds=20)
o, a = ordered(14, [4, 23, 27], lambda v: f"{v} ms")
Q(T, "Functions", "Advanced",
  "Processes P1, P2 and P3 arrive at time 0 in that order, with CPU burst times of 18 ms, 6 ms and 3 ms. Using "
  "First-Come, First-Served (FCFS) scheduling, what is the average waiting time?", o, a,
  concept="FCFS scheduling: waiting time = start time - arrival time",
  explanation="Under FCFS the processes run in arrival order. P1 waits 0 ms, P2 waits for P1 (18 ms), and P3 waits "
              "for both (18 + 6 = 24 ms). Average = (0 + 18 + 24) / 3 = 14 ms.",
  steps=["P1: 0 to 18, wait 0", "P2: 18 to 24, wait 18", "P3: 24 to 27, wait 24", "Average = 42 / 3 = 14 ms"],
  wrong="4 ms is the average under Shortest Job First (3, 6, 18). 23 ms is the average turnaround time "
        "(18 + 24 + 27) / 3. 27 ms is the time when the last process finishes.", seconds=60, computed=True)
o, a = ordered(7, [5, 8, 9])
Q(T, "Functions", "Advanced",
  "A system has 3 page frames, all empty at the start. Using FIFO page replacement, how many page faults occur for "
  "the reference string 4, 7, 4, 1, 7, 2, 4, 3, 7?", o, a,
  concept="FIFO page replacement",
  explanation="A fault occurs whenever the page is not in memory; when all frames are full, FIFO removes the page "
              "that was loaded earliest. Tracing the string gives 7 faults (4, 7, 1, 2, 4, 3, 7) and 2 hits "
              "(the second 4 and the second 7).",
  steps=["4 F [4]; 7 F [4,7]; 4 hit; 1 F [4,7,1]; 7 hit",
         "2 F, remove 4 -> [7,1,2]; 4 F, remove 7 -> [1,2,4]",
         "3 F, remove 1 -> [2,4,3]; 7 F, remove 2 -> [4,3,7]", "Faults = 7"],
  wrong="5 is the count under the Optimal algorithm. 8 and 9 forget that the second 4 and the first repeat of 7 "
        "are hits.", seconds=75, computed=True)
Q(T, "File systems", "Advanced",
  "In Linux, file report.txt has a hard link h1 and a symbolic (soft) link s1. If report.txt is then deleted, what "
  "happens?",
  ["h1 still opens the data, but s1 becomes a broken (dangling) link",
   "Both h1 and s1 still open the data", "Both h1 and s1 become broken links",
   "s1 still opens the data, but h1 becomes a broken link"],
  concept="Hard links vs symbolic links",
  explanation="A hard link is another directory entry for the same inode, so the data stays until the last hard "
              "link is removed. A symbolic link only stores the path 'report.txt'; when that name disappears, the "
              "link points to nothing.",
  steps=["Hard link -> same inode -> data still reachable", "Symbolic link -> stored path -> path gone -> dangling"],
  wrong="A symbolic link cannot survive the deletion of its target path, and a hard link does not depend on the "
        "original name.", seconds=40)

# ================================================================ 5. Input and Output Devices (2 / 4 / 1)
T = "Input and Output Devices"
Q(T, "Input devices", "Basic",
  "A branch officer wants to store a signed customer form in the computer as an image. Which device should she use?",
  ["Scanner", "Plotter", "Projector", "Speaker"],
  concept="Input devices",
  explanation="A scanner captures a paper document or photo and sends it to the computer as a digital image.",
  steps=["Paper -> digital image = scanner (input device)"],
  wrong="A plotter and a projector are output devices, and a speaker outputs sound.", seconds=15)
Q(T, "Output devices", "Basic",
  "The print quality (resolution) of a printer is commonly expressed in:",
  ["DPI (dots per inch)", "RPM (revolutions per minute)", "MIPS (million instructions per second)",
   "bps (bits per second)"],
  concept="Printer resolution",
  explanation="Print resolution is the number of dots a printer places in one inch, e.g. 600 x 600 dpi. More dots "
              "per inch give sharper output.",
  steps=["Printer resolution = DPI"],
  wrong="RPM measures disk rotation speed, MIPS measures processor speed, and bps measures data transfer rate.",
  seconds=15)
Q(T, "Input devices", "Intermediate",
  "A bank wants to turn old typed letters into text that can be edited and searched in a word processor. Which "
  "technology is needed after scanning?",
  ["OCR (Optical Character Recognition)", "OMR (Optical Mark Recognition)",
   "MICR (Magnetic Ink Character Recognition)", "Barcode reader"],
  concept="Recognition technologies",
  explanation="OCR recognises the shapes of printed or typed letters in a scanned image and converts them into "
              "editable text.",
  steps=["Scanned printed text -> editable text = OCR"],
  wrong="OMR detects filled bubbles, MICR reads special magnetic-ink characters on cheques, and a barcode reader "
        "reads bars, not ordinary text.", seconds=20)
Q(T, "Input devices", "Intermediate",
  "Which of the following works as both an input device and an output device?",
  ["Touchscreen", "Keyboard", "Monitor without touch", "Scanner"],
  concept="Input/output devices",
  explanation="A touchscreen displays output and also takes input when it is touched, so it is both an input and an "
              "output device.",
  steps=["Displays (output) + senses touch (input) = touchscreen"],
  wrong="A keyboard and a scanner are input only; a monitor without touch is output only.", seconds=15)
Q(T, "Output devices", "Intermediate",
  "Which printer uses a laser, a light-sensitive drum and toner powder that is fused to the paper by heat?",
  ["Laser printer", "Inkjet printer", "Dot-matrix printer", "Thermal printer"],
  concept="Types of printers",
  explanation="A laser printer draws the page on a drum with a laser, the toner sticks to the charged areas and "
              "is fused onto the paper by a heated roller.",
  steps=["Laser + drum + toner = laser printer"],
  wrong="Inkjets spray liquid ink, dot-matrix printers strike an inked ribbon with pins, and thermal printers use "
        "heat-sensitive paper (as in ATM slips).", seconds=20)
Q(T, "Output devices", "Intermediate",
  "A monitor is advertised as having a 144 Hz refresh rate. What does this figure tell you?",
  ["The screen image is redrawn 144 times per second", "The screen has 144 pixels per inch",
   "The monitor responds to a key press in 144 ms", "The monitor can show 144 colours"],
  concept="Refresh rate",
  explanation="Refresh rate, measured in hertz (Hz), is how many times per second the display redraws the image. "
              "A higher refresh rate gives smoother motion.",
  steps=["Hz = times per second", "144 Hz = 144 redraws per second"],
  wrong="Pixels per inch measure pixel density, response time is in milliseconds, and colour depth is measured in "
        "bits.", seconds=20)
o, a = ordered(109, [92, 128, 151], lambda v: f"About {v} PPI")
Q(T, "Output devices", "Advanced",
  "A 27-inch monitor (measured diagonally) has a resolution of 2560 x 1440 pixels. What is its approximate pixel "
  "density?", o, a,
  concept="Pixel density = diagonal pixels / diagonal inches",
  explanation="The diagonal in pixels is sqrt(2560^2 + 1440^2) = sqrt(6,553,600 + 2,073,600) = sqrt(8,627,200), "
              "about 2937 pixels. Dividing by 27 inches gives about 109 pixels per inch.",
  steps=["2560^2 + 1440^2 = 8,627,200", "sqrt = about 2937 pixels", "2937 / 27 = about 109 PPI"],
  wrong="92 PPI is what 1920 x 1080 would give on a 24-inch screen; 128 and 151 do not follow from the given "
        "figures (2560 / 20 = 128 uses neither the diagonal nor 27 inches).", seconds=70, computed=True)

# ================================================================ 6. Memory (3 / 1 / 3)
T = "Memory"
Q(T, "Primary memory", "Basic",
  "Which memory is non-volatile and holds the firmware instructions a computer needs when it is switched on?",
  ["ROM", "RAM", "Cache", "Registers"],
  concept="ROM vs RAM",
  explanation="ROM (Read-Only Memory) keeps its contents without power, so it stores the start-up firmware.",
  steps=["Non-volatile + start-up instructions = ROM"],
  wrong="RAM, cache and registers are volatile and lose their contents when the power goes off.", seconds=15)
Q(T, "Cache and units", "Basic",
  "Which of the following is the largest unit of storage?",
  ["Petabyte", "Terabyte", "Gigabyte", "Megabyte"],
  concept="Storage units",
  explanation="The order is KB < MB < GB < TB < PB, each 1024 times the previous (in binary units). So a petabyte "
              "is the largest of these.",
  steps=["MB < GB < TB < PB"],
  wrong="Megabyte, gigabyte and terabyte are all smaller than a petabyte.", seconds=15)
Q(T, "Secondary storage", "Basic",
  "Which of the following is an optical storage medium, read using a laser?",
  ["DVD", "SSD", "Pen drive", "Hard disk drive"],
  concept="Types of secondary storage",
  explanation="CDs, DVDs and Blu-ray discs are optical media: a laser reads pits and lands on the disc surface.",
  steps=["Laser-read disc = optical = DVD"],
  wrong="SSDs and pen drives use flash memory, and a hard disk stores data magnetically.", seconds=15)
Q(T, "Cache and units", "Intermediate",
  "Cache memory improves speed because programs tend to reuse recently used data and to access nearby memory "
  "locations. What is this tendency called?",
  ["Locality of reference", "Thrashing", "Fragmentation", "Paging"],
  concept="Why caching works",
  explanation="Locality of reference has two forms: temporal (recently used items are likely to be used again soon) "
              "and spatial (items near a recently used address are likely to be used next). Caches keep such data "
              "close to the CPU.",
  steps=["Reuse of recent/nearby data = locality of reference"],
  wrong="Thrashing is excessive paging that slows a system. Fragmentation is wasted or scattered memory/disk "
        "space. Paging divides memory into fixed-size pages.", seconds=25)
o, a = ordered(64, [16, 32, 128], lambda v: f"{v} KB")
Q(T, "Primary memory", "Advanced",
  "A memory chip has 16 address lines and each memory location stores 1 byte. What is its total capacity?", o, a,
  concept="Capacity = 2^(address lines) x word size",
  explanation="16 address lines can select 2^16 = 65,536 different locations. With 1 byte per location, the "
              "capacity is 65,536 bytes = 64 KB (1 KB = 1024 bytes).",
  steps=["Locations = 2^16 = 65,536", "65,536 x 1 byte = 65,536 bytes", "65,536 / 1024 = 64 KB"],
  shortcut="2^10 = 1 KB, so 2^16 = 2^6 KB = 64 KB.",
  wrong="16 KB uses 2^14 locations, 32 KB uses 2^15 and 128 KB uses 2^17.", seconds=40, computed=True)
o, a = ordered(LAT_MS, [F(25, 12), F(25, 3), F(50, 3)], lambda v: f"{float(v):.2f} ms")
Q(T, "Secondary storage", "Advanced",
  "A hard disk spins at 7200 RPM. What is its average rotational latency?", o, a,
  concept="Average rotational latency = half of one rotation time",
  explanation="7200 rotations per minute = 120 per second, so one rotation takes 1/120 s = 8.33 ms. On average the "
              "required sector is half a turn away, so the average latency is 8.33 / 2 = 4.17 ms.",
  steps=["7200 / 60 = 120 rotations per second", "One rotation = 1000 / 120 = 8.33 ms",
         "Average latency = 8.33 / 2 = 4.17 ms"],
  wrong="8.33 ms is a full rotation, not the average. 2.08 ms is a quarter turn. 16.67 ms is two full rotations.",
  seconds=50, computed=True)
o, a = ordered(104, [7, 88, 112])
Q(T, "Cache and units", "Advanced",
  "A direct-mapped cache has 128 lines, numbered 0 to 127. To which cache line does main-memory block number 1000 "
  "map?", o, a,
  concept="Direct mapping: line = block number mod number of lines",
  explanation="In a direct-mapped cache each block can go into exactly one line, found by block number mod number "
              "of lines. 1000 mod 128 = 1000 - 7 x 128 = 1000 - 896 = 104.",
  steps=["128 x 7 = 896", "1000 - 896 = 104", "Line = 104"],
  wrong="7 is the quotient (it becomes part of the tag), not the line. 88 and 112 come from arithmetic slips.",
  seconds=40, computed=True)

# ================================================================ 7. Internet (1 / 2 / 2)
T = "Internet"
Q(T, "Web basics", "Basic",
  "Google Chrome, Mozilla Firefox and Microsoft Edge are examples of:",
  ["Web browsers", "Search engines", "Operating systems", "Web servers"],
  concept="Web browser",
  explanation="A web browser is application software that requests web pages from servers and displays them.",
  steps=["Chrome, Firefox, Edge = web browsers"],
  wrong="A search engine (such as Google Search) is a website that runs inside a browser. These are not operating "
        "systems, and web servers deliver pages rather than display them.", seconds=15)
Q(T, "Email", "Intermediate",
  "Which email protocol, in its usual setting, downloads messages from the mail server to one device and then "
  "removes them from the server?",
  ["POP3", "IMAP", "SMTP", "HTTP"],
  concept="Email retrieval protocols",
  explanation="POP3 (Post Office Protocol version 3) is designed to download mail to a single device; by default "
              "the copies on the server are deleted after download.",
  steps=["Download + remove from server = POP3"],
  wrong="IMAP keeps mail on the server and syncs it across devices. SMTP sends mail; it does not retrieve it. HTTP "
        "is the web page protocol.", seconds=20)
Q(T, "Web basics", "Intermediate",
  "A website stores a small text file in your browser so that it remembers your login session and language choice "
  "on your next visit. This file is called a:",
  ["Cookie", "Cache", "Plug-in", "Bookmark"],
  concept="Browser cookies",
  explanation="A cookie is a small piece of data a website saves in the browser and reads back on later requests to "
              "remember sessions and preferences.",
  steps=["Small file to remember login and preferences = cookie"],
  wrong="The browser cache stores copies of pages and images to load faster. A plug-in adds features to a browser. "
        "A bookmark is a saved link chosen by the user.", seconds=20)
Q(T, "Protocols", "Advanced",
  "A developer is building a net-banking login form. Which HTTP method should submit the username and password, "
  "and why?",
  ["POST, because the data travels in the request body instead of appearing in the URL",
   "GET, because it is the only method that works with HTTPS",
   "GET, because it is safe and idempotent and so cannot leak data",
   "POST, because it sends the password without needing HTTPS"],
  concept="HTTP GET vs POST",
  explanation="GET sends form data in the URL query string, which can end up in browser history, server logs and "
              "shared links. POST puts the data in the request body. HTTPS is still needed with POST to encrypt the "
              "data in transit.",
  steps=["GET -> data in the URL (visible, logged)", "POST -> data in the body", "Use POST over HTTPS for passwords"],
  wrong="Both GET and POST work over HTTPS. 'Safe and idempotent' means GET does not change server data; it says "
        "nothing about hiding the data. POST without HTTPS sends the password in plain text.", seconds=40,
  facts=[fact("GET carries data in the URL query string and should not have a request body; GET is safe and "
              "idempotent.", MDN_GET)])
Q(T, "Protocols", "Advanced",
  "Which DNS resource record type maps a host name such as www.example.in to an IPv4 address?",
  ["A record", "AAAA record", "MX record", "CNAME record"],
  concept="DNS record types",
  explanation="An A (address) record holds a 32-bit IPv4 address for a host name. AAAA records hold IPv6 "
              "addresses, MX records name the mail servers for a domain, and CNAME records make one name an alias "
              "of another.",
  steps=["Host name -> IPv4 address = A record"],
  wrong="AAAA is for IPv6 addresses, MX for mail exchange servers and CNAME for aliases.", seconds=25,
  facts=[fact("RFC 1035 lists type A as 'a host address', CNAME as 'the canonical name for an alias' and MX as "
              "'mail exchange'.", RFC1035),
         fact("RFC 3596 defines the AAAA record as storing a single IPv6 address.", RFC3596)])

# ================================================================ 8. Networking (4 / 6 / 3)
T = "Networking"
Q(T, "Topologies", "Basic",
  "In which network topology are all computers connected to one common backbone cable, so that a break in that "
  "cable stops the whole network?",
  ["Bus", "Star", "Mesh", "Tree"],
  concept="Network topologies",
  explanation="In a bus topology every node taps into a single shared cable (the backbone), with terminators at "
              "both ends. It is cheap, but a break in the backbone brings the network down.",
  steps=["Single shared backbone cable = bus"],
  wrong="Star uses a central device, mesh uses many point-to-point links, and tree connects star groups to a "
        "backbone hierarchy.", seconds=15)
Q(T, "Devices", "Basic",
  "Which simple network device repeats every incoming signal to all its ports, without checking which computer the "
  "data is meant for?",
  ["Hub", "Switch", "Router", "Firewall"],
  concept="Network devices",
  explanation="A hub works at the physical layer. It does not read addresses; it simply repeats incoming data to "
              "every port, which wastes bandwidth.",
  steps=["Repeats to all ports, no address check = hub"],
  wrong="A switch sends frames only to the port of the destination MAC address, a router forwards by IP address, "
        "and a firewall filters traffic by rules.", seconds=15)
Q(T, "Topologies", "Basic",
  "In which topology is each computer connected to exactly two neighbours, so that data travels around a closed "
  "loop from one node to the next?",
  ["Ring", "Bus", "Star", "Mesh"],
  concept="Network topologies",
  explanation="In a ring topology the nodes form a closed loop. Data passes from node to node, often in one "
              "direction, until it reaches its destination.",
  steps=["Closed loop, two neighbours each = ring"],
  wrong="Bus uses one shared cable, star connects all nodes to a centre, and mesh connects nodes to many others.",
  seconds=15)
Q(T, "OSI and TCP/IP", "Basic",
  "Which is the lowest layer of the OSI model, dealing with cables, connectors and the transmission of raw bits?",
  ["Physical layer", "Data link layer", "Network layer", "Application layer"],
  concept="OSI layers",
  explanation="Layer 1, the physical layer, defines how raw bits are sent as electrical, optical or radio signals "
              "over cables, connectors and wireless links.",
  steps=["Layer 1 = physical = bits on the medium"],
  wrong="The data link layer (2) handles frames and MAC addresses, the network layer (3) handles IP routing, and the "
        "application layer (7) is the top layer.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "Which OSI layer is responsible for data translation, encryption and compression, so that data from one system "
  "can be read by another?",
  ["Presentation layer", "Session layer", "Transport layer", "Data link layer"],
  concept="OSI layer functions",
  explanation="The presentation layer (layer 6) deals with the format of the data: character encoding "
              "translation, encryption/decryption and compression.",
  steps=["Format, encryption, compression = layer 6, presentation"],
  wrong="The session layer manages dialogues between applications, the transport layer handles end-to-end delivery "
        "and the data link layer handles frames between neighbouring nodes.", seconds=20)
Q(T, "OSI and TCP/IP", "Intermediate",
  "According to RFC 1122, the Internet (TCP/IP) protocol suite is organised into how many layers?",
  ["4", "5", "6", "7"], "A",
  concept="TCP/IP model vs OSI model",
  explanation="RFC 1122 describes four layers: Link, Internet, Transport and Application. The OSI reference model "
              "has seven. Some textbooks show a five-layer hybrid by splitting the link layer into physical and "
              "data link, which is why the question names RFC 1122.",
  steps=["RFC 1122 layers: Application, Transport, Internet, Link", "Count = 4"],
  wrong="5 is a textbook hybrid model, 7 is the OSI model, and no standard model has 6 layers.", seconds=20,
  facts=[fact("RFC 1122 section 1.1.3 lists four layers: Application, Transport, Internet and Link.", RFC1122)])
Q(T, "Devices", "Intermediate",
  "Which device connects two networks that use entirely different protocols or architectures and converts the data "
  "from one format to the other?",
  ["Gateway", "Repeater", "Hub", "Bridge"],
  concept="Gateway",
  explanation="A gateway acts as a translator between networks that use different protocols, converting data "
              "formats so that they can communicate.",
  steps=["Different protocols + conversion = gateway"],
  wrong="A repeater only boosts signals, a hub repeats data to all ports, and a bridge joins two segments of the "
        "same type of network.", seconds=20)
Q(T, "Topologies", "Intermediate",
  "A company connects several star networks, one per floor, to a main backbone in a hierarchy. This arrangement is "
  "called a:",
  ["Tree topology", "Ring topology", "Bus topology", "Full mesh topology"],
  concept="Tree (hierarchical) topology",
  explanation="A tree topology joins several star-configured groups to a backbone in a hierarchy, combining "
              "features of bus and star topologies.",
  steps=["Stars connected to a backbone in levels = tree"],
  wrong="A ring is a closed loop, a bus has all nodes on one cable, and a full mesh links every node to every other.",
  seconds=20)
Q(T, "OSI and TCP/IP", "Intermediate",
  "What is the unit of data (protocol data unit) called at the data link layer of the OSI model?",
  ["Frame", "Packet", "Segment", "Bit"],
  concept="PDUs at each layer",
  explanation="Data link layer = frame; network layer = packet; transport layer = segment (TCP) or datagram (UDP); "
              "physical layer = bits.",
  steps=["Layer 2 PDU = frame"],
  wrong="Packet belongs to the network layer, segment to the transport layer and bit to the physical layer.",
  seconds=20)
Q(T, "OSI and TCP/IP", "Intermediate",
  "In what order are segments exchanged when a TCP connection is set up by the three-way handshake?",
  ["SYN, SYN-ACK, ACK", "ACK, SYN, SYN-ACK", "SYN, ACK, FIN", "SYN-ACK, SYN, ACK"],
  concept="TCP three-way handshake",
  explanation="The client sends SYN with its initial sequence number. The server replies with SYN-ACK, sending its "
              "own SYN and acknowledging the client's. The client sends ACK, and the connection is established.",
  steps=["Client -> SYN", "Server -> SYN + ACK", "Client -> ACK"],
  wrong="The handshake must begin with the client's SYN, and FIN is used to close a connection, not open it.",
  seconds=20,
  facts=[fact("RFC 9293 shows connection set-up as SYN from peer A, SYN plus ACK from peer B, then ACK from peer A.",
              RFC9293)])
Q(T, "OSI and TCP/IP", "Advanced",
  "What is the subnet mask, in dotted-decimal form, for the prefix /20?",
  ["255.255.240.0", "255.255.224.0", "255.255.248.0", "255.255.255.240"],
  concept="CIDR prefix to subnet mask",
  explanation="/20 means 20 one-bits: 8 + 8 + 4. The first two octets are 255. The third octet has four 1s "
              "followed by four 0s: 11110000 = 128 + 64 + 32 + 16 = 240. The last octet is 0.",
  steps=["20 = 8 + 8 + 4", "Third octet = 11110000 = 240", "Mask = 255.255.240.0"],
  wrong="255.255.224.0 is /19, 255.255.248.0 is /21 and 255.255.255.240 is /28.", seconds=40, computed=True)
Q(T, "OSI and TCP/IP", "Advanced",
  "Which of the following IPv4 addresses belongs to a private address range defined in RFC 1918?",
  ["172.20.5.4", "172.32.1.1", "192.169.1.1", "11.0.0.1"],
  concept="Private IPv4 ranges",
  explanation="RFC 1918 reserves 10.0.0.0/8, 172.16.0.0/12 (172.16.0.0 to 172.31.255.255) and 192.168.0.0/16 for "
              "private networks. 172.20.5.4 falls inside 172.16 to 172.31.",
  steps=["172.16.0.0/12 covers 172.16.x.x to 172.31.x.x", "172.20 is in that range"],
  wrong="172.32.1.1 is just past the 172.31 limit, 192.169.1.1 is outside 192.168/16, and 11.0.0.1 is outside "
        "10/8. All three are public addresses.", seconds=35, computed=True,
  facts=[fact("RFC 1918 reserves 10.0.0.0-10.255.255.255, 172.16.0.0-172.31.255.255 and "
              "192.168.0.0-192.168.255.255 for private internets.", RFC1918)])
o, a = ordered(4, [F(1, 2), 2, 8], lambda v: f"{float(v):g} second{'s' if v != 1 else ''}")
Q(T, "Devices", "Advanced",
  "A 25 MB file (1 MB = 10^6 bytes) is sent over a 50 Mbps link. Ignoring protocol overhead and delays, how long "
  "does the transfer take?", o, a,
  concept="Transfer time = data size in bits / bandwidth",
  explanation="Link speeds are in bits per second, file sizes in bytes. 25 MB = 25 x 10^6 x 8 = 200 x 10^6 bits. "
              "At 50 x 10^6 bits per second this takes 200 / 50 = 4 seconds.",
  steps=["25 MB x 8 = 200 Mb", "200 Mb / 50 Mbps = 4 s"],
  shortcut="Bytes to bits: multiply by 8 before dividing by the link speed.",
  wrong="0.5 s forgets to convert bytes to bits (25 / 50). 2 s converts with 4 bits per byte, and 8 s doubles the "
        "correct answer.", seconds=40, computed=True)

# ================================================================ 9. Cybersecurity (2 / 3 / 2)
T = "Cybersecurity"
Q(T, "Malware", "Basic",
  "Which type of malware copies itself across a network from computer to computer on its own, without needing to "
  "attach to a host file or be run by the user?",
  ["Worm", "Virus", "Adware", "Spyware"],
  concept="Types of malware",
  explanation="A worm is self-replicating and self-spreading: it exploits network weaknesses to copy itself to "
              "other machines without a host program.",
  steps=["Spreads by itself over networks, no host file = worm"],
  wrong="A virus needs a host file that the user runs. Adware shows unwanted ads and spyware secretly collects "
        "information; neither is defined by self-spreading.", seconds=20)
Q(T, "Phishing and social engineering", "Basic",
  "Someone standing behind a customer at an ATM watches him type his PIN. This kind of attack is called:",
  ["Shoulder surfing", "Phishing", "Spoofing", "Skimming"],
  concept="Social engineering",
  explanation="Shoulder surfing is stealing information such as a PIN or password by watching the victim enter it. "
              "Covering the keypad prevents it.",
  steps=["Watching over someone's shoulder = shoulder surfing"],
  wrong="Phishing uses fake messages, spoofing fakes an identity such as a caller ID or email address, and skimming "
        "copies card data with a device fitted to the card slot.", seconds=15)
Q(T, "Malware", "Intermediate",
  "Malicious software that secretly records every key pressed on a computer, in order to capture passwords and "
  "card numbers, is called a:",
  ["Keylogger", "Rootkit", "Logic bomb", "Botnet"],
  concept="Spyware types",
  explanation="A keylogger records keystrokes and sends them to the attacker. This is why banks offer on-screen "
              "virtual keyboards for entering passwords.",
  steps=["Records keystrokes = keylogger"],
  wrong="A rootkit hides malware deep in the system, a logic bomb triggers on a condition such as a date, and a "
        "botnet is a network of infected computers controlled remotely.", seconds=20)
Q(T, "Encryption and authentication", "Intermediate",
  "Authentication factors are grouped as something you know, something you have and something you are. Which of "
  "these is a 'something you are' factor?",
  ["Fingerprint", "Password", "OTP received on a registered mobile", "Debit card"],
  concept="Authentication factors",
  explanation="'Something you are' means a biometric trait, such as a fingerprint, face or iris.",
  steps=["Biometric = something you are = fingerprint"],
  wrong="A password is something you know. The OTP proves possession of the registered phone and the debit card is "
        "a physical item, so both are something you have.", seconds=20)
Q(T, "Phishing and social engineering", "Intermediate",
  "An attacker studies a particular bank employee's social-media profile and sends her an email that mentions her "
  "manager by name and a project she is working on, asking her to open an attachment. This targeted attack is:",
  ["Spear phishing", "Vishing", "Pharming", "Baiting"],
  concept="Targeted phishing",
  explanation="Spear phishing is phishing aimed at one specific person or group, using personal details to make "
              "the message look genuine.",
  steps=["Email + personalised for one target = spear phishing"],
  wrong="Vishing uses phone calls, pharming redirects users to fake websites through DNS or hosts-file tampering, "
        "and baiting leaves infected media (such as a pen drive) for victims to find.", seconds=25)
Q(T, "Encryption and authentication", "Advanced",
  "Which of the following is a cryptographic hash function rather than an encryption algorithm?",
  ["SHA-256", "AES", "RSA", "DES"],
  concept="Hashing vs encryption",
  explanation="A hash function such as SHA-256 turns any input into a fixed-length (256-bit) digest and is one-way: "
              "the input cannot be recovered from it. Encryption is reversible with the right key.",
  steps=["One-way fixed-length digest = hash = SHA-256"],
  wrong="AES and DES are symmetric encryption algorithms and RSA is an asymmetric one; all three can be decrypted "
        "with the right key.", seconds=25)
Q(T, "Phishing and social engineering", "Advanced",
  "Customers type the correct address of their bank's website but are silently taken to a fake look-alike site, "
  "because the attacker has tampered with DNS records. This attack is called:",
  ["Pharming", "Phishing", "Smishing", "Tailgating"],
  concept="Pharming",
  explanation="Pharming redirects users to a fake website even when they type the correct URL, by poisoning DNS or "
              "altering the hosts file. Unlike phishing, it needs no tempting link.",
  steps=["Correct URL typed + redirected via DNS tampering = pharming"],
  wrong="Phishing and smishing trick users into clicking a link in an email or SMS. Tailgating is following an "
        "authorised person through a secure door.", seconds=25)

# ================================================================ 10. Database Fundamentals (2 / 2 / 3)
T = "Database Fundamentals"
Q(T, "DBMS concepts", "Basic",
  "Information that describes other data, such as a table's column names, data types and constraints, is called:",
  ["Metadata", "Raw data", "Big data", "Redundant data"],
  concept="Metadata and the data dictionary",
  explanation="Metadata is 'data about data'. A DBMS keeps it in the data dictionary (system catalog).",
  steps=["Data about data = metadata"],
  wrong="Raw data is unprocessed facts, big data refers to very large data sets, and redundant data is unnecessary "
        "duplication.", seconds=15)
Q(T, "SQL basics", "Basic",
  "Which SQL command is used to retrieve rows from a table?",
  ["SELECT", "INSERT", "UPDATE", "CREATE"],
  concept="Basic SQL commands",
  explanation="SELECT reads (queries) data from one or more tables.",
  steps=["Retrieve = SELECT"],
  wrong="INSERT adds rows, UPDATE changes rows and CREATE makes database objects such as tables.", seconds=10)
Q(T, "Keys", "Intermediate",
  "A Customers table has two candidate keys, CustomerID and PAN. CustomerID is chosen as the primary key. What is "
  "PAN now called?",
  ["Alternate key", "Foreign key", "Composite key", "Super key only"],
  concept="Candidate, primary and alternate keys",
  explanation="Every candidate key could serve as the primary key. The one chosen becomes the primary key, and each "
              "remaining candidate key is an alternate key.",
  steps=["Candidate keys: CustomerID, PAN", "Chosen: CustomerID (primary)", "Not chosen: PAN = alternate key"],
  wrong="A foreign key refers to another table's key. A composite key has more than one column. PAN is indeed a "
        "super key, but the specific name for an unchosen candidate key is alternate key.", seconds=25)
Q(T, "SQL basics", "Intermediate",
  "Which SQL command removes all rows from a table but keeps the table's structure for future use, and is "
  "classified as a DDL command?",
  ["TRUNCATE", "DELETE", "DROP", "ALTER"],
  concept="DELETE vs TRUNCATE vs DROP",
  explanation="TRUNCATE TABLE empties a table quickly and keeps its structure. It is a DDL command. DELETE is "
              "DML and removes rows one by one (optionally with WHERE). DROP removes the whole table, structure "
              "included.",
  steps=["All rows gone + structure kept + DDL = TRUNCATE"],
  wrong="DELETE is DML, not DDL. DROP removes the structure too. ALTER changes the structure but does not remove "
        "rows.", seconds=25)
o, a = ordered(7, [3, 4, 6])
Q(T, "SQL basics", "Advanced",
  "Customers (cust_id, name): (1, Asha), (2, Ravi), (3, Meena), (4, John), (5, Farah), (6, Kiran). Loans "
  "(loan_id, cust_id): (L1, 1), (L2, 1), (L3, 3), (L4, 5). How many rows does this query return?\n"
  "SELECT c.name, l.loan_id FROM Customers c LEFT JOIN Loans l ON c.cust_id = l.cust_id;", o, a,
  concept="LEFT OUTER JOIN",
  explanation="A LEFT JOIN returns every row of the left table. Customers with matching loans appear once per "
              "matching loan; customers without loans appear once with NULL for loan_id. Asha has 2 loans "
              "(2 rows), Meena 1, Farah 1, and Ravi, John and Kiran appear once each with NULL: 2 + 1 + 1 + 3 = 7.",
  steps=["Asha: L1, L2 -> 2 rows", "Meena: L3 -> 1 row; Farah: L4 -> 1 row",
         "Ravi, John, Kiran: no loan -> 1 row each with NULL", "Total = 7"],
  wrong="4 is the INNER JOIN result (matched rows only). 6 is the number of customers, forgetting Asha's second "
        "loan. 3 counts only the customers without loans.", seconds=60, computed=True)
o, a = ordered(6000, [3600, 4500, 18000], lambda v: f"{v:,}")
Q(T, "SQL basics", "Advanced",
  "Table Staff has a column bonus with the values 4000, NULL, 6000, 8000, NULL (five rows). What does "
  "SELECT AVG(bonus) FROM Staff; return?", o, a,
  concept="Aggregate functions ignore NULL",
  explanation="AVG, SUM and COUNT(column) skip NULL values. The three non-NULL bonuses add to 18,000, and "
              "18,000 / 3 = 6,000.",
  steps=["Non-NULL values: 4000, 6000, 8000", "Sum = 18,000, count = 3", "AVG = 6,000"],
  wrong="3,600 divides by all 5 rows, treating NULL as 0. 4,500 divides by 4. 18,000 is SUM, not AVG.",
  seconds=40, computed=True)
Q(T, "DBMS concepts", "Advanced",
  "During a fund transfer, Rs 5,000 is debited from account A, but the system crashes before account B is "
  "credited. On recovery the DBMS rolls back the debit. Which ACID property ensures this all-or-nothing behaviour?",
  ["Atomicity", "Consistency", "Isolation", "Durability"],
  concept="ACID properties of transactions",
  explanation="Atomicity means a transaction is indivisible: either all of its operations take effect or none do. "
              "A half-done transfer is undone.",
  steps=["All-or-nothing = atomicity"],
  wrong="Consistency keeps the database valid under its rules, isolation stops concurrent transactions from "
        "interfering, and durability keeps committed changes safe after a crash.", seconds=25)

# ================================================================ 11. MS Office (4 / 6 / 2)
T = "MS Office"
Q(T, "MS Word", "Basic",
  "Which view in MS Word shows the document as it will look when printed, with margins, headers and footers?",
  ["Print Layout", "Draft", "Outline", "Read Mode"],
  concept="Word document views",
  explanation="Print Layout is Word's default editing view. It shows pages with their margins, headers, footers and "
              "images as they will print.",
  steps=["As it will be printed = Print Layout"],
  wrong="Draft hides headers, footers and page edges. Outline shows the heading structure. Read Mode is for reading "
        "on screen and reflows the text.", seconds=20)
Q(T, "MS Excel", "Basic",
  "What is the default file extension of a workbook saved in Excel 2007 or later?",
  [".xlsx", ".xls", ".docx", ".pptx"],
  concept="Office file extensions",
  explanation="Since Excel 2007, workbooks are saved by default as .xlsx (Office Open XML).",
  steps=["Excel 2007+ workbook = .xlsx"],
  wrong=".xls is the older Excel 97-2003 format, .docx is Word and .pptx is PowerPoint.", seconds=15)
Q(T, "MS PowerPoint", "Basic",
  "During a PowerPoint slide show, which key ends the presentation?",
  ["Esc", "F5", "Enter", "Tab"],
  concept="Slide show keys",
  explanation="Pressing Esc ends the slide show and returns to the normal editing view.",
  steps=["End slide show = Esc"],
  wrong="F5 starts a slide show, Enter moves to the next slide or animation, and Tab moves between hyperlinks or "
        "objects on a slide.", seconds=15,
  facts=[fact("Esc ends the presentation in PowerPoint.", MS_PPT)])
Q(T, "Shortcuts", "Basic",
  "In MS Word, which keyboard shortcut opens the Print options for the document?",
  ["Ctrl + P", "Ctrl + R", "Ctrl + T", "Ctrl + N"],
  concept="Common Word shortcuts",
  explanation="Ctrl + P prints the document (opens the Print screen).",
  steps=["Print = Ctrl + P"],
  wrong="In Word, Ctrl + R right-aligns a paragraph, Ctrl + T creates a hanging indent and Ctrl + N creates a new "
        "document.", seconds=15,
  facts=[fact("Ctrl+P prints the document in Word.", MS_WORD)])
Q(T, "Shortcuts", "Intermediate",
  "In MS Word, which keyboard shortcut centres the selected paragraph?",
  ["Ctrl + E", "Ctrl + C", "Ctrl + J", "Ctrl + L"],
  concept="Paragraph alignment shortcuts",
  explanation="Word's alignment shortcuts are Ctrl + L (left), Ctrl + E (centre), Ctrl + R (right) and Ctrl + J "
              "(justify).",
  steps=["Centre = Ctrl + E"],
  wrong="Ctrl + C copies, Ctrl + J justifies and Ctrl + L left-aligns.", seconds=15,
  facts=[fact("In Word, Ctrl+E centers the paragraph and Ctrl+J justifies it.", MS_WORD)])
Q(T, "MS Excel", "Intermediate",
  "What value does the Excel formula =ROUND(1234.567, -2) return?",
  ["1200", "1234.57", "1235", "1300"],
  concept="ROUND with a negative number of digits",
  explanation="A negative num_digits rounds to the left of the decimal point. -2 rounds to the nearest hundred. "
              "1234.567 is nearer to 1200 than to 1300.",
  steps=["-2 -> nearest hundred", "Tens digit is 3 (< 5), so round down", "Result = 1200"],
  wrong="1234.57 uses +2 digits, 1235 uses 0 digits, and 1300 rounds up instead of to the nearest hundred.",
  seconds=30, computed=True,
  facts=[fact("If num_digits is less than 0, ROUND rounds to the left of the decimal point.", MS_ROUND)])
Q(T, "MS Excel", "Intermediate",
  "Cell A1 contains the text '  Bank   of  India ' (with extra spaces at the start, between the words and at the "
  "end). What does =LEN(TRIM(A1)) return?",
  ["13", "11", "15", "19"],
  concept="TRIM and LEN",
  explanation="TRIM removes leading and trailing spaces and reduces runs of spaces between words to a single space, "
              "giving 'Bank of India'. LEN counts its characters: 4 + 1 + 2 + 1 + 5 = 13.",
  steps=["TRIM -> 'Bank of India'", "Letters: 4 + 2 + 5 = 11", "Plus 2 single spaces = 13"],
  wrong="11 removes all spaces, which TRIM does not do. 19 is the length before trimming. 15 keeps some extra "
        "spaces.", seconds=40, computed=True,
  facts=[fact("TRIM removes all spaces from text except for single spaces between words.", MS_TRIM)])
Q(T, "MS PowerPoint", "Intermediate",
  "A bank wants its logo, fonts and colour scheme to appear the same on every slide of a 40-slide presentation, "
  "and to change them in one place. Which PowerPoint feature should be used?",
  ["Slide Master", "Slide Sorter", "Notes Page", "Animation Pane"],
  concept="Slide Master",
  explanation="The Slide Master holds the theme, fonts, colours, background and placeholders used by all slide "
              "layouts. A change made there applies to every slide based on it.",
  steps=["Common design on all slides, edited once = Slide Master"],
  wrong="Slide Sorter reorders slides, Notes Page shows speaker notes, and the Animation Pane manages animations.",
  seconds=20)
Q(T, "MS Word", "Intermediate",
  "A branch must send a personalised letter to 500 customers, each with the customer's own name and address taken "
  "from an Excel list. Which MS Word feature does this?",
  ["Mail Merge", "Track Changes", "Macros", "Hyperlink"],
  concept="Mail Merge",
  explanation="Mail Merge combines a main document with a data source (such as an Excel sheet) and produces one "
              "personalised copy for each record.",
  steps=["One letter + list of recipients -> many personalised letters = Mail Merge"],
  wrong="Track Changes records edits, macros automate repeated actions, and a hyperlink links to another location.",
  seconds=20)
Q(T, "Shortcuts", "Intermediate",
  "In Excel for Windows, which key puts the active cell into edit mode with the insertion point at the end of its "
  "contents?",
  ["F2", "F4", "F7", "F12"],
  concept="Excel function keys",
  explanation="F2 edits the active cell and places the insertion point at the end of its contents.",
  steps=["Edit active cell = F2"],
  wrong="F4 repeats the last action or cycles reference types, F7 runs the spelling check, and F12 opens "
        "Save As.", seconds=20,
  facts=[fact("F2 edits the active cell and puts the insertion point at the end of its contents.", MS_EXCEL)])
Q(T, "MS Excel", "Advanced",
  "In Excel, B2 = 72000 and C2 = \"No\". What does this formula return?\n"
  "=IF(AND(B2>50000,C2=\"Yes\"),\"Eligible\",IF(OR(B2>60000,C2=\"Yes\"),\"Review\",\"Reject\"))",
  ["Review", "Eligible", "Reject", "#VALUE!"],
  concept="Nested IF with AND and OR",
  explanation="AND needs both conditions true: 72000 > 50000 is TRUE but C2 = \"Yes\" is FALSE, so AND is FALSE "
              "and the second IF is checked. OR needs at least one true condition: 72000 > 60000 is TRUE, so the "
              "result is \"Review\".",
  steps=["AND(TRUE, FALSE) = FALSE -> go to inner IF", "OR(TRUE, FALSE) = TRUE", "Result = \"Review\""],
  wrong="\"Eligible\" needs C2 = \"Yes\". \"Reject\" would need both OR conditions false. The formula is valid, "
        "so there is no #VALUE! error.", seconds=45, computed=True)
Q(T, "MS Excel", "Advanced",
  "Cell A1 contains the text Kumar, Asha. What does =MID(A1, FIND(\",\", A1) + 2, LEN(A1)) return?",
  ["Asha", "Kumar, Asha", "Kumar", "sha"],
  concept="MID with FIND",
  explanation="FIND returns the position of the comma, 6. Adding 2 skips the comma and the space, so MID starts at "
              "position 8. Asking for LEN(A1) = 11 characters is more than are left, so MID returns everything to "
              "the end: Asha.",
  steps=["FIND(\",\") = 6", "Start = 6 + 2 = 8 (the 'A' of Asha)", "MID returns the rest of the text: Asha"],
  wrong="'Kumar, Asha' would need MID to start at position 1. 'Kumar' is what LEFT(A1, FIND(\",\", A1) - 1) "
        "returns. 'sha' would need a start position of 9 (+ 3).",
  seconds=50, computed=True,
  facts=[fact("If start_num plus num_chars exceeds the text length, MID returns the characters up to the end of "
              "text.", MS_MID)])

# ================================================================ 12. Digital Payments (1 / 2 / 2)
T = "Digital Payments"
Q(T, "Payment technology", "Basic",
  "In UPI, an address such as asha@okbank that is used to receive money without sharing the bank account number "
  "and IFSC is called a:",
  ["Virtual Payment Address (VPA)", "MMID", "IFSC code", "URL"],
  concept="UPI ID / VPA",
  explanation="A Virtual Payment Address (also called UPI ID) is a name@handle identifier linked to a bank "
              "account. Payers need only the VPA, not the account number and IFSC.",
  steps=["name@handle in UPI = VPA (UPI ID)"],
  wrong="MMID is a 7-digit identifier used with IMPS, IFSC identifies a bank branch, and a URL is a web address.",
  seconds=20)
Q(T, "Payment technology", "Intermediate",
  "Which wireless technology lets a customer pay by simply tapping a contactless card or phone on a POS terminal "
  "from a few centimetres away?",
  ["NFC (Near Field Communication)", "Bluetooth Low Energy", "Wi-Fi Direct", "Infrared (IrDA)"],
  concept="Contactless payments",
  explanation="NFC works only over a few centimetres, which suits tap-to-pay: the short range makes accidental or "
              "distant reading unlikely.",
  steps=["Tap within a few cm = NFC"],
  wrong="Bluetooth and Wi-Fi Direct work over metres and are not used for card taps; infrared needs line of sight "
        "and is not used by payment cards.", seconds=20)
Q(T, "Card security", "Intermediate",
  "Why is an EMV chip card harder to clone than an old magnetic-stripe card?",
  ["The chip generates a different cryptogram for every transaction, so copied data cannot be reused",
   "The chip stores the PIN in plain text so the terminal can check it faster",
   "The chip card has no card number, so nothing can be copied",
   "The chip works only at ATMs and not at shops"],
  concept="EMV chip security",
  explanation="A magnetic stripe holds static data that a skimmer can copy and write onto a fake card. An EMV chip "
              "creates a unique cryptogram for each transaction using a secret key stored in the chip, so copied "
              "transaction data is useless for the next one.",
  steps=["Magstripe = static data = easy to copy", "Chip = dynamic cryptogram per transaction = hard to clone"],
  wrong="The chip never exposes the PIN in plain text, chip cards still have card numbers, and they are used at "
        "shops as well as ATMs.", seconds=30)
Q(T, "Card security", "Advanced",
  "When a customer pays online with a card, the issuing bank may ask for an OTP or biometric check before "
  "approving the payment. The EMVCo protocol that supports this issuer authentication for card-not-present "
  "e-commerce payments is:",
  ["3-D Secure", "EMV contact chip", "Magnetic stripe", "Tokenisation"],
  concept="EMV 3-D Secure",
  explanation="EMV 3-D Secure lets the merchant pass transaction and device data to the issuer, which assesses risk "
              "and, for riskier payments, asks the cardholder for extra authentication such as an OTP or "
              "biometrics. It is designed to cut card-not-present fraud.",
  steps=["Online card payment + issuer asks OTP = 3-D Secure"],
  wrong="The contact chip and magnetic stripe are used when the card is present at a terminal. Tokenisation "
        "replaces the card number with a token but does not itself authenticate the cardholder.", seconds=30,
  facts=[fact("EMV 3-D Secure helps prevent card-not-present fraud in e-commerce; issuers may require further "
              "authentication such as a one-time passcode or biometrics.", EMV_3DS)])
o, a = ordered(LUHN_DIGIT, [3, 5, 7])
Q(T, "Card security", "Advanced",
  "Card numbers end with a check digit calculated by the Luhn (mod 10) algorithm. Starting from the rightmost digit "
  "of the payload 6082419 and moving left, every alternate digit (starting with that rightmost one) is doubled; "
  "if a doubled value exceeds 9, 9 is subtracted; then all digits are added. What check digit must be appended to "
  "6082419?", o, a,
  concept="Luhn check digit",
  explanation="Payload 6 0 8 2 4 1 9. Doubling from the right: 9 -> 18 -> 9, 4 -> 8, 8 -> 16 -> 7, 6 -> 12 -> 3, "
              "which add to 27. The undoubled digits 1, 2 and 0 add to 3. The total is 30, already a multiple of "
              "10, so the check digit is 0 and the full number 60824190 passes the Luhn test.",
  steps=["Doubled (from right): 9->9, 4->8, 8->7, 6->3; sum 27", "Not doubled: 1, 2, 0; sum 3",
         "Total = 30", "Check digit = (10 - 30 mod 10) mod 10"],
  wrong="7 comes from doubling the wrong set of digits (1, 2, 0 instead of 9, 4, 8, 6). 3 comes from forgetting "
        "to subtract 9 from doubled values above 9 (total 57). 5 has no basis; with any digit other than 0 the "
        "number fails the Luhn test.", seconds=75, computed=True)

# ================================================================ 13. Computer Abbreviations (1 / 3 / 1)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic",
  "What does RAM stand for?",
  ["Random Access Memory", "Read Access Memory", "Rapid Action Memory", "Random Allocation Module"],
  concept="Memory abbreviations",
  explanation="RAM (Random Access Memory) is the computer's main working memory; any location can be accessed "
              "directly in about the same time.",
  steps=["RAM = Random Access Memory"],
  wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "Bank staff working from home connect to the office network through an encrypted tunnel over the internet. "
  "What does VPN, the name of this technology, stand for?",
  ["Virtual Private Network", "Verified Public Network", "Virtual Protected Node", "Variable Private Network"],
  concept="Networking abbreviations",
  explanation="A VPN (Virtual Private Network) creates an encrypted tunnel across a public network so that remote "
              "users can work as if they were on the private office network.",
  steps=["VPN = Virtual Private Network"],
  wrong="The other expansions are invented.", seconds=15)
Q(T, S, "Intermediate",
  "What is the full form of ASCII, the character-encoding standard?",
  ["American Standard Code for Information Interchange", "American Standard Character for Internal Information",
   "Automatic System Code for Information Integration", "Advanced Standard Code for Internet Interchange"],
  concept="Character-encoding abbreviations",
  explanation="ASCII (American Standard Code for Information Interchange) is a 7-bit code for 128 characters; for "
              "example, 'A' is 65.",
  steps=["ASCII = American Standard Code for Information Interchange"],
  wrong="The other expansions are invented.", seconds=20)
Q(T, S, "Intermediate",
  "A bank uses an email service that runs entirely on the provider's servers and is accessed through a browser on a "
  "subscription. This cloud model is called SaaS. What does SaaS stand for?",
  ["Software as a Service", "Storage as a Service", "System as a Server", "Security as a Service"],
  concept="Cloud service models",
  explanation="SaaS (Software as a Service) delivers ready-to-use applications over the internet. The other main "
              "models are PaaS (Platform as a Service) and IaaS (Infrastructure as a Service).",
  steps=["SaaS = Software as a Service"],
  wrong="The other expansions are not the standard cloud model names.", seconds=20)
Q(T, S, "Advanced",
  "What is the full form of CMOS, the technology used in processors and in the chip that stores BIOS/UEFI "
  "settings?",
  ["Complementary Metal-Oxide-Semiconductor", "Central Memory Operating System", "Computer Managed Output Signal",
   "Complementary Magnetic-Oxide Storage"],
  concept="Hardware abbreviations",
  explanation="CMOS (Complementary Metal-Oxide-Semiconductor) is a chip-making technology that uses very little "
              "power. A small battery-backed CMOS memory keeps firmware settings and the clock.",
  steps=["CMOS = Complementary Metal-Oxide-Semiconductor"],
  wrong="The other expansions are invented; CMOS is not an operating system or a magnetic store.", seconds=20)

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_002_plan.json").read_text(encoding="utf-8"))
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
    "batch_id": "BATCH_002",
    "created_at": TODAY,
    "notes": "BATCH_002 Computer Knowledge part: 100 original questions (BANK_COMP_000103 to BANK_COMP_000202). "
             "Computable answers (number systems, BCD, CPU time, FCFS, FIFO paging, memory and disk figures, cache "
             "mapping, pixel density, subnet masks, RFC 1918 ranges, transfer time, Luhn check digit, SQL on given "
             "tables via sqlite3, Excel formula results) are re-derived in tools/batch_002/computer.py. Shortcuts, "
             "Excel functions and protocol facts were checked on Microsoft Support, RFC Editor, MDN and EMVCo pages "
             "on 2026-11-05.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_002_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
