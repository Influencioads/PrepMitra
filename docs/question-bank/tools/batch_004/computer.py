"""Writes batches/parts/BATCH_004_COMP.json: the 100 Computer Knowledge questions of BATCH_004.

Every computable answer (binary addition, bits needed for a number, hex to binary, radix of an equation, excess-3
code, Amdahl's law, colour depth, mouse counts, cache tag bits, RAID 5 capacity, memory chip count, subnet count,
bandwidth-delay product, SQL COUNT(DISTINCT) / ORDER BY / second-highest via sqlite3, Excel INT, PMT and approximate
VLOOKUP) is re-derived below with assertions before the file is written. The plan quota per (topic, difficulty), the
ID range and the answer-key balance are also asserted. If any assertion fails, nothing is written.

    python tools/batch_004/computer.py      (run from docs/question-bank)
"""

import bisect
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
FIRST_ID = 303
AI = ("ai:author-solve", "ai:independent-check")
COMPUTED = ("script:recompute", "ai:author-solve", "ai:independent-check")

_rng = random.Random(20261105 + 4)
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
B = lambda s: int(s, 2)
# Binary addition 1011 + 0110
assert B("1011") + B("0110") == 17 == B("10001")
assert [B(x) for x in ("1101", "10011", "11101")] == [13, 19, 29]
# Minimum bits for 300 (unsigned)
assert (300).bit_length() == 9 and 2**8 - 1 < 300 <= 2**9 - 1
# Hex 3B7 to binary
assert format(0x3B7, "b") == "1110110111"
HEX_WRONG = ["1110100111", "1101110111", "1110110110"]
assert all(x != "1110110111" for x in HEX_WRONG) and len(set(HEX_WRONG)) == 3


# Radix: 24 + 15 = 42 holds only in base 7 (digits up to 5 need base >= 6)
def val(s, b):
    return int(s, b)


RADIX = [b for b in range(6, 17) if val("24", b) + val("15", b) == val("42", b)]
assert RADIX == [7]
assert val("43", 6) == 27  # base 6 gives 43, not 42


# Excess-3 of 47
def xs3(n):
    return " ".join(format(int(d) + 3, "04b") for d in str(n))


assert xs3(47) == "0111 1010"
assert " ".join(format(int(d), "04b") for d in "47") == "0100 0111"  # plain BCD distractor
assert format(47, "08b") == "00101111"

# Amdahl's law: 80% parallel on 4 cores
AMDAHL = 1 / (F(2, 10) + F(8, 10) / 4)
assert AMDAHL == F(5, 2)
# 10 bits per channel
assert 2 ** 30 == 1_073_741_824 and 2 ** 24 == 16_777_216 and 3 * 2 ** 10 == 3072
# Mouse: 1,600 counts per inch x 1.5 inches
assert 1600 * F(3, 2) == 2400 and round(1600 / 1.5) == 1067
# Direct-mapped cache 32 KB, 64-byte blocks, 32-bit byte address
LINES = 32 * 1024 // 64
OFFSET, INDEX = int(math.log2(64)), int(math.log2(LINES))
assert LINES == 512 and OFFSET == 6 and INDEX == 9 and 32 - INDEX - OFFSET == 17
# RAID 5 with five 2 TB disks
assert (5 - 1) * 2 == 8
# 64K x 8 memory from 16K x 4 chips
assert (64 // 16) * (8 // 4) == 8
# Subnets: /16 split into /20
assert 2 ** (20 - 16) == 16
# Bandwidth-delay product: 100 Mbps x 80 ms RTT
BDP_BITS = 100 * 10**6 * F(80, 1000)
assert BDP_BITS == 8_000_000 and BDP_BITS / 8 == 1_000_000 and BDP_BITS / 2 / 8 == 500_000

# SQL
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Accounts (acc_id INTEGER, branch TEXT)")
db.executemany("INSERT INTO Accounts VALUES (?, ?)",
               [(1, "Pune"), (2, "Delhi"), (3, "Pune"), (4, "Agra"), (5, "Delhi"), (6, "Pune")])
assert db.execute("SELECT COUNT(DISTINCT branch) FROM Accounts").fetchone()[0] == 3
assert db.execute("SELECT COUNT(branch) FROM Accounts").fetchone()[0] == 6
db.execute("CREATE TABLE Emp (emp_id INTEGER, salary INTEGER)")
SAL = [(1, 45000), (2, 72000), (3, 72000), (4, 60000), (5, 38000)]
db.executemany("INSERT INTO Emp VALUES (?, ?)", SAL)
SECOND = db.execute("SELECT MAX(salary) FROM Emp WHERE salary < (SELECT MAX(salary) FROM Emp)").fetchone()[0]
assert SECOND == 60000
db.execute("CREATE TABLE Cust (name TEXT, balance INTEGER)")
db.executemany("INSERT INTO Cust VALUES (?, ?)", [("Asha", 52000), ("Ravi", 18000), ("Meena", 75000)])
assert [r[0] for r in db.execute("SELECT name FROM Cust ORDER BY balance")] == ["Ravi", "Asha", "Meena"]

# Excel INT rounds down (towards minus infinity)
assert math.floor(-7.5) == -8 and int(-7.5) == -7
# Excel PMT: =ROUND(PMT(12%/12, 12, -100000), 2)
r, n, pv = 0.01, 12, 100000
EMI = round(pv * r / (1 - (1 + r) ** -n), 2)
assert EMI == 8884.88
assert round(pv * 1.12 / 12, 2) == 9333.33 and round(pv / 12, 2) == 8333.33
# Approximate VLOOKUP: largest first-column value <= lookup value (sorted ascending)
SLAB_LIMITS, SLAB_RATES = [0, 50000, 100000, 500000], ["3.0%", "3.5%", "4.0%", "4.5%"]
assert SLAB_RATES[bisect.bisect_right(SLAB_LIMITS, 73000) - 1] == "3.5%"

# ---------------------------------------------------------------- fact-check sources
# Pages opened on 2026-11-05 (web:fact-check)
MS_WIN = "https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec"
MS_WORD = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2"
MS_EXCEL = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-9b7213f0040f"
MS_PPT = ("https://support.microsoft.com/en-us/office/use-keyboard-shortcuts-to-create-powerpoint-presentations-"
          "ebb3d20e-dcd4-444f-a38e-bb5c5ed180f4")
MS_INT = "https://support.microsoft.com/en-us/office/int-function-a6c4af9e-356d-4369-ab6a-cb1fd9d343ef"
MS_PMT = "https://support.microsoft.com/en-us/office/pmt-function-0214da64-9a63-4996-bc20-214433fa6441"
MDN_SOP = "https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy"
NIST_BIN = "https://physics.nist.gov/cuu/Units/binary.html"
RFC7208 = "https://www.rfc-editor.org/rfc/rfc7208"
RFC5905 = "https://www.rfc-editor.org/rfc/rfc5905"
RFC792 = "https://www.rfc-editor.org/rfc/rfc792"
APACHE = "https://www.apache.org/licenses/LICENSE-2.0"
CHROME_INCOG = "https://support.google.com/chrome/answer/95464?hl=en"
# Confirmed only in search results (web:search-confirmed)
INTEL_4004 = "https://intel.com/content/www/us/en/newsroom/news/intel-marks-50th-anniversary-4004.html"
NPCI_RUPAY = "https://www.npci.org.in/product/rupay/about-rupay"
NPCI_AEPS = "https://www.npci.org.in/PDF/AePS/Product-Booklet.pdf"
SC = "web:search-confirmed"

# ================================================================ 1. Computer Fundamentals (4 / 4 / 3)
T = "Computer Fundamentals"
Q(T, "Generations and history", "Basic",
  "In which computer architecture are program instructions and data stored in the same main memory and fetched "
  "over the same path?",
  ["Von Neumann architecture", "Harvard architecture", "Client-server architecture", "Peer-to-peer architecture"],
  concept="Stored-program (von Neumann) architecture",
  explanation="The von Neumann architecture, described in the 1945 report on the EDVAC, keeps both the program "
              "and its data in one memory and moves them over a shared bus. Most general-purpose computers still "
              "follow this design.",
  steps=["Instructions and data in the same memory = von Neumann architecture"],
  wrong="The Harvard architecture uses separate memories (and paths) for instructions and data. Client-server and "
        "peer-to-peer describe how networked computers share work, not how a CPU stores programs.", seconds=20)
Q(T, "Number systems", "Basic",
  "What is the largest digit used in the octal (base 8) number system?",
  ["7", "8", "9", "F"],
  concept="Digits of a number system",
  explanation="A base-b system uses the digits 0 to b - 1. Octal is base 8, so its digits are 0 to 7 and the "
              "largest is 7.",
  steps=["Base 8 -> digits 0 to 8 - 1", "Largest digit = 7"],
  wrong="8 itself is written 10 in octal. 9 is the largest decimal digit and F the largest hexadecimal digit.",
  seconds=10)
Q(T, "Types of computers", "Basic",
  "A computer in a bank's data centre provides files, email and the internet-banking website to many other "
  "computers over the network. Such a computer is called a:",
  ["Server", "Client", "Workstation", "Embedded computer"],
  concept="Servers and clients",
  explanation="A server is a computer that provides services or resources to other computers (clients) over a "
              "network. Web servers, mail servers and file servers are common examples.",
  steps=["Provides services to other computers = server"],
  wrong="A client requests services from a server. A workstation is a powerful single-user computer. An embedded "
        "computer is built into a device to do one dedicated job.", seconds=15)
o, a = ordered(17, [13, 19, 29], lambda v: format(v, "b"))
Q(T, "Number systems", "Basic",
  "What is the sum of the binary numbers 1011 and 0110?", o, a,
  concept="Binary addition with carry",
  explanation="Add column by column from the right: 1 + 0 = 1; 1 + 1 = 10 (write 0, carry 1); 0 + 1 + 1 = 10 "
              "(write 0, carry 1); 1 + 0 + 1 = 10 (write 0, carry 1); the final carry gives 1. Result 10001. "
              "Check: 11 + 6 = 17 = 10001.",
  steps=["1011 = 11, 0110 = 6", "11 + 6 = 17", "17 = 16 + 1 = 10001"],
  shortcut="Convert to decimal, add, convert back.",
  wrong="1101 = 13 ignores the carries. 10011 = 19 and 11101 = 29 place a carry in the wrong column.", seconds=30,
  computed=True)
o, a = ordered(9, [8, 10, 11])
Q(T, "Number systems", "Intermediate",
  "What is the minimum number of bits needed to represent the decimal number 300 as an unsigned binary number?", o, a,
  concept="Bits needed for a number",
  explanation="n bits can represent 0 to 2^n - 1. With 8 bits the maximum is 255, which is less than 300. With 9 "
              "bits the maximum is 511, which covers 300. So 9 bits are needed. (300 = 100101100 in binary.)",
  steps=["2^8 - 1 = 255 < 300", "2^9 - 1 = 511 >= 300", "Minimum = 9 bits"],
  shortcut="Find the smallest power of 2 greater than the number: 512 = 2^9, so 9 bits.",
  wrong="8 bits stop at 255. 10 and 11 bits would work but are not the minimum.", seconds=30, computed=True)
o, a = ordered("1110110111", HEX_WRONG)
Q(T, "Number systems", "Intermediate",
  "What is the binary equivalent of the hexadecimal number 3B7?", o, a,
  concept="Hexadecimal to binary",
  explanation="Each hexadecimal digit maps to exactly 4 bits: 3 = 0011, B = 1011, 7 = 0111. Joining them gives "
              "0011 1011 0111; dropping the leading zeros gives 1110110111.",
  steps=["3 = 0011", "B = 1011", "7 = 0111", "0011 1011 0111 = 1110110111"],
  shortcut="Replace every hex digit by its 4-bit group.",
  wrong="1110100111 is 3A7 (B written as 1010), 1101110111 is 377 (B written as 0111), and 1110110110 is 3B6 "
        "(7 written as 0110).",
  seconds=35, computed=True)
Q(T, "Generations and history", "Intermediate",
  "The Intel 4004, introduced in 1971, is remembered in computer history as:",
  ["The first commercially available microprocessor", "The first integrated circuit",
   "The first transistor-based computer", "The first IBM personal computer"],
  concept="Microprocessors and the fourth generation",
  explanation="The Intel 4004 was a 4-bit processor that put the whole CPU on a single chip. It was the first "
              "commercially available microprocessor and opened the way to the microprocessor-based fourth "
              "generation of computers.",
  steps=["CPU on one chip, 1971 = Intel 4004", "First commercially available microprocessor"],
  wrong="The integrated circuit was invented in 1958-59, transistor computers belong to the 1950s, and the IBM PC "
        "(1981) used the Intel 8088.", seconds=20, web=SC,
  facts=[fact("Intel newsroom: the Intel 4004, the world's first commercially available microprocessor, made its "
              "debut in November 1971.", INTEL_4004)])
Q(T, "Types of computers", "Intermediate",
  "In a quantum computer, the basic unit of information can exist in a superposition of 0 and 1 at the same time. "
  "What is this unit called?",
  ["Qubit", "Nibble", "Byte", "Pixel"],
  concept="Quantum computers",
  explanation="A qubit (quantum bit) can be 0, 1 or a superposition of both. Quantum computers use superposition "
              "and entanglement of qubits to attack certain problems, such as factoring or simulating molecules, "
              "far faster than classical computers.",
  steps=["Quantum unit of information = qubit"],
  wrong="A nibble (4 bits) and a byte (8 bits) are groups of classical bits. A pixel is a picture element on a "
        "screen.", seconds=15)
o, a = ordered(7, [6, 8, 9])
Q(T, "Number systems", "Advanced",
  "In which number base is the addition 24 + 15 = 42 correct?", o, a,
  concept="Finding an unknown base",
  explanation="In base b: 24 = 2b + 4, 15 = b + 5 and 42 = 4b + 2. So 2b + 4 + b + 5 = 4b + 2, giving 3b + 9 = "
              "4b + 2 and b = 7. The digit 5 is allowed because 5 < 7. Check in base 7: 18 + 12 = 30 = 4 x 7 + 2.",
  steps=["2b + 4 + b + 5 = 4b + 2", "3b + 9 = 4b + 2", "b = 7", "Check: 18 + 12 = 30 = 42 (base 7)"],
  wrong="In base 6 the sum is 16 + 11 = 27, written 43. In base 8 it is 20 + 13 = 33, written 41. In base 9 it is "
        "22 + 14 = 36, written 40.", seconds=60, computed=True)
Q(T, "Number systems", "Advanced",
  "In Excess-3 code, each decimal digit is written as the 4-bit binary value of (digit + 3). What is the Excess-3 "
  "code for the decimal number 47?",
  ["0111 1010", "0100 0111", "0010 1111", "0111 1011"],
  concept="Excess-3 code",
  explanation="Add 3 to each digit and write the result in 4 bits: 4 + 3 = 7 = 0111 and 7 + 3 = 10 = 1010. The "
              "code is 0111 1010. Excess-3 is a self-complementing BCD code.",
  steps=["4 + 3 = 7 = 0111", "7 + 3 = 10 = 1010", "Excess-3 = 0111 1010"],
  wrong="0100 0111 is plain BCD (8421) for 47. 0010 1111 is 47 in pure binary. 0111 1011 adds 4 instead of 3 to "
        "the second digit.", seconds=40, computed=True)
Q(T, "Types of computers", "Advanced",
  "In Flynn's classification of computer architectures, a GPU that applies the same instruction to many data "
  "elements at once, such as brightening every pixel of an image together, is an example of:",
  ["SIMD (Single Instruction, Multiple Data)", "SISD (Single Instruction, Single Data)",
   "MISD (Multiple Instruction, Single Data)", "MIMD (Multiple Instruction, Multiple Data)"],
  concept="Flynn's taxonomy",
  explanation="Flynn classified computers by the number of instruction streams and data streams. One instruction "
              "applied to many data items at once is SIMD, the model used by GPUs and vector units.",
  steps=["Same instruction -> single instruction stream", "Many pixels -> multiple data streams", "= SIMD"],
  wrong="SISD is a simple single-core sequential processor. MISD (several instructions on the same data) is rare. "
        "MIMD is a multi-core or multi-processor system running different instructions on different data.",
  seconds=30)

# ================================================================ 2. Hardware (1 / 3 / 1)
T = "Hardware"
Q(T, "Motherboard and ports", "Basic",
  "Which hardware component, built into the motherboard or added as an expansion card, connects a computer to a "
  "network?",
  ["Network Interface Card (NIC)", "Sound card", "Graphics card", "SMPS"],
  concept="Network adapter",
  explanation="A NIC (network interface card or network adapter) provides the Ethernet or Wi-Fi connection. Each "
              "NIC has its own MAC address.",
  steps=["Connects computer to a network = NIC"],
  wrong="A sound card handles audio, a graphics card handles video output, and the SMPS supplies power.",
  seconds=15)
Q(T, "CPU and components", "Intermediate",
  "Which CPU register holds the data that has just been read from memory, or that is about to be written to "
  "memory?",
  ["Memory Data Register (MDR)", "Program Counter (PC)", "Instruction Register (IR)", "Stack Pointer (SP)"],
  concept="CPU registers",
  explanation="The MDR (also called the Memory Buffer Register, MBR) temporarily stores the data word moving "
              "between the CPU and memory. The MAR holds the address and the MDR holds the contents.",
  steps=["Address of memory location -> MAR", "Data going to or from that location -> MDR"],
  wrong="The PC holds the address of the next instruction, the IR holds the instruction being decoded, and the SP "
        "points to the top of the stack.", seconds=20)
Q(T, "Motherboard and ports", "Intermediate",
  "Which USB connector is small, oval and reversible, so it can be plugged in either way up, and is used on most "
  "new smartphones and laptops?",
  ["USB Type-C", "USB Type-A", "Micro-USB", "Mini-USB"],
  concept="USB connector types",
  explanation="USB Type-C has a symmetrical oval shape that fits either way up. It carries data, charging power "
              "and, on many devices, video.",
  steps=["Reversible oval connector = USB Type-C"],
  wrong="Type-A is the flat rectangular plug found on chargers and pen drives. Micro-USB and Mini-USB are older "
        "small connectors that fit only one way.", seconds=15)
Q(T, "CPU and components", "Intermediate",
  "When a key is pressed, the keyboard sends a signal that makes the CPU pause its current task, save its state, "
  "run a routine to read the key, and then resume. What is this signal called?",
  ["Interrupt", "Clock pulse", "Bus request", "Cache miss"],
  concept="Interrupts",
  explanation="An interrupt is a signal from hardware or software asking the CPU for immediate attention. The CPU "
              "saves its state, runs the interrupt service routine (handler) and then returns to the interrupted "
              "task.",
  steps=["Device needs attention -> interrupt", "CPU runs the interrupt handler, then resumes"],
  wrong="Clock pulses only time the CPU's operations. A bus request asks for control of the bus. A cache miss means "
        "data was not found in cache.", seconds=20)
o, a = ordered(F(5, 2), [F(2), F(16, 5), F(4)], lambda v: f"{float(v):g} times")
Q(T, "CPU and components", "Advanced",
  "80% of a program's running time can be split across processor cores; the remaining 20% must run on one core. "
  "According to Amdahl's law, what is the maximum overall speed-up on 4 cores?", o, a,
  concept="Amdahl's law",
  explanation="Speed-up = 1 / ((1 - p) + p / n), where p is the parallel fraction and n the number of cores. "
              "= 1 / (0.2 + 0.8 / 4) = 1 / (0.2 + 0.2) = 1 / 0.4 = 2.5. The serial 20% limits the gain.",
  steps=["p = 0.8, n = 4", "Time = 0.2 + 0.8 / 4 = 0.4", "Speed-up = 1 / 0.4 = 2.5"],
  shortcut="Even with infinite cores the speed-up cannot exceed 1 / 0.2 = 5.",
  wrong="4 assumes the whole program is parallel. 3.2 multiplies 0.8 by 4. 2 uses 1 / (0.2 + 0.8 / 2), i.e. 2 "
        "cores.", seconds=50, computed=True)

# ================================================================ 3. Software (3 / 1 / 3)
T = "Software"
Q(T, "Programming languages", "Basic",
  "A programmer misspells the keyword 'while' as 'whlie' and leaves out a closing bracket. The compiler stops and "
  "reports an error without creating the program. What kind of error is this?",
  ["Syntax error", "Logic error", "Runtime error", "Hardware error"],
  concept="Types of program errors",
  explanation="A syntax error breaks the grammar rules of the programming language, so the translator cannot "
              "understand the code and reports it before the program runs.",
  steps=["Rule of the language broken -> syntax error", "Detected at compile time"],
  wrong="A logic error gives wrong results without any error message. A runtime error happens while the program is "
        "running, for example division by zero. A hardware error is a fault in a device.", seconds=15)
Q(T, "Programming languages", "Basic",
  "Which of the following is a high-level programming language?",
  ["Java", "Assembly language", "Machine language", "Binary code"],
  concept="Levels of programming languages",
  explanation="High-level languages such as Java, Python and C use English-like statements and are independent of "
              "a particular processor. They must be compiled or interpreted before the CPU can run them.",
  steps=["English-like and machine-independent = high-level", "Java is high-level"],
  wrong="Assembly language uses processor-specific mnemonics and is low-level. Machine language and binary code "
        "are the 0s and 1s the CPU runs directly.", seconds=10)
Q(T, "Licensing", "Basic",
  "Software that is owned by a company, sold under a licence, and whose source code is kept secret so that users "
  "cannot view or change it is called:",
  ["Proprietary software", "Open-source software", "Public domain software", "Freeware"],
  concept="Software licensing types",
  explanation="Proprietary (closed-source) software remains the property of its publisher. Users buy a licence to "
              "use it, but the source code is not shared and copying or modifying it is not allowed.",
  steps=["Owned, licensed, source code secret = proprietary"],
  wrong="Open-source software publishes its source code. Public domain software has no copyright. Freeware costs "
        "nothing, which is not the defining feature here.", seconds=15)
Q(T, "System and application software", "Intermediate",
  "After a program has been compiled and linked, which system program copies the executable file from disk into "
  "main memory and prepares it to start running?",
  ["Loader", "Linker", "Assembler", "Debugger"],
  concept="Language processors and system programs",
  explanation="The loader places the executable into memory, sets up addresses and hands control to the program's "
              "first instruction. The order is compile -> link -> load -> execute.",
  steps=["Compile -> link -> load -> run", "Placing the executable in memory = loader"],
  wrong="The linker combines object files into one executable but does not load it. The assembler translates "
        "assembly code. A debugger helps find errors.", seconds=20)
Q(T, "Licensing", "Advanced",
  "A bank's software team wants an open-source licence that is permissive (it allows use in closed-source "
  "products) and that also contains an express grant of patent rights from every contributor. Which licence fits?",
  ["Apache License 2.0", "MIT License", "BSD 2-Clause License", "Creative Commons Zero (CC0)"],
  concept="Permissive licences and patent grants",
  explanation="The Apache License 2.0 is permissive, and its Section 3 gives users a patent licence from each "
              "contributor for their contributions, which ends for anyone who sues claiming the work infringes a "
              "patent.",
  steps=["Permissive + explicit patent grant = Apache 2.0"],
  wrong="The MIT and BSD 2-Clause licences are permissive but say nothing about patents. CC0 waives copyright but "
        "expressly does not grant patent rights.", seconds=30,
  facts=[fact("Apache License 2.0, Section 3 'Grant of Patent License': each Contributor grants a perpetual, "
              "worldwide patent license.", APACHE)])
Q(T, "Programming languages", "Advanced",
  "The Java Virtual Machine first interprets bytecode, then compiles the frequently executed parts into native "
  "machine code while the program is running. What is this technique called?",
  ["Just-in-time (JIT) compilation", "Ahead-of-time (AOT) compilation", "Cross-compilation", "Static linking"],
  concept="Just-in-time compilation",
  explanation="A JIT compiler translates code into native machine code at run time, usually for 'hot' code that "
              "runs often. This combines the portability of bytecode with speed close to compiled code.",
  steps=["Compilation during execution = just-in-time"],
  wrong="AOT compilation happens before the program runs. Cross-compilation produces code for a different "
        "platform. Static linking joins libraries into the executable at build time.", seconds=25)
Q(T, "Programming languages", "Advanced",
  "Classes SavingsAccount and FixedDeposit both inherit from Account, and each provides its own version of the "
  "method calculateInterest(). When calculateInterest() is called through an Account reference, the version that "
  "runs depends on the actual type of the object. Which OOP concept is this?",
  ["Polymorphism", "Encapsulation", "Abstraction", "Inheritance"],
  concept="Run-time polymorphism (method overriding)",
  explanation="Polymorphism ('many forms') lets one method call behave differently for different object types. "
              "Here each subclass overrides calculateInterest() and the right version is chosen at run time.",
  steps=["Same call, different behaviour by object type = polymorphism"],
  wrong="Inheritance only lets the subclasses reuse Account's members; choosing the overridden version at run time "
        "is polymorphism. Encapsulation hides data behind methods. Abstraction shows only essential features.",
  seconds=30)

# ================================================================ 4. Operating Systems (3 / 6 / 1)
T = "Operating Systems"
Q(T, "Windows and Linux basics", "Basic",
  "In Windows, which keyboard shortcut displays and hides the desktop?",
  ["Windows logo key + D", "Windows logo key + E", "Windows logo key + L", "Alt + F4"],
  concept="Windows shortcuts",
  explanation="Windows logo key + D shows the desktop by minimising the open windows; pressing it again restores "
              "them.",
  steps=["Win + D = display and hide the desktop"],
  wrong="Win + E opens File Explorer, Win + L locks the PC and Alt + F4 closes the active window.", seconds=10,
  facts=[fact("Microsoft Support: Windows logo key + D - Display and hide the desktop.", MS_WIN)])
Q(T, "Windows and Linux basics", "Basic",
  "Which Linux command creates a new directory?",
  ["mkdir", "rmdir", "cd", "touch"],
  concept="Linux directory commands",
  explanation="mkdir (make directory) creates a new directory, for example mkdir reports.",
  steps=["make directory = mkdir"],
  wrong="rmdir removes an empty directory, cd changes the current directory and touch creates an empty file or "
        "updates a file's timestamp.", seconds=10)
Q(T, "Functions", "Basic",
  "The core part of an operating system, which stays in memory and directly manages the CPU, memory and devices, "
  "is called the:",
  ["Kernel", "Shell", "Desktop", "Compiler"],
  concept="Kernel and shell",
  explanation="The kernel is the heart of the OS. It handles process scheduling, memory management, device "
              "control and system calls. The shell is the interface through which users give commands to it.",
  steps=["Core of the OS = kernel"],
  wrong="The shell is the user interface layer around the kernel, the desktop is part of the GUI, and a compiler "
        "is a language translator, not part of the OS core.", seconds=15)
Q(T, "Windows and Linux basics", "Intermediate",
  "On a Linux system, what is the user name of the superuser account that has full administrative control?",
  ["root", "admin", "sudo", "guest"],
  concept="Linux users",
  explanation="root is the Linux superuser (user ID 0) and can read, change or delete any file and run any "
              "command. Ordinary users run single commands as root through sudo.",
  steps=["Linux superuser = root"],
  wrong="'admin' is not the standard Linux superuser name. sudo is a command for running commands with root "
        "rights, not an account. guest is a limited account.", seconds=15)
Q(T, "Windows and Linux basics", "Intermediate",
  "Which Linux command searches files for lines that match a given text pattern, for example to find every line "
  "containing 'FAILED' in a log file?",
  ["grep", "find", "cat", "wc"],
  concept="Linux text tools",
  explanation="grep prints the lines of a file that match a pattern: grep FAILED app.log shows every line "
              "containing FAILED.",
  steps=["Search inside files for a pattern = grep"],
  wrong="find searches for files by name, size or date, not for text inside them. cat displays a file's whole "
        "contents and wc counts lines, words and characters.", seconds=15)
Q(T, "Functions", "Intermediate",
  "A running process asks to read data from the disk and cannot continue until the data arrives. In which state "
  "does the operating system place it meanwhile?",
  ["Waiting (blocked)", "Ready", "New", "Terminated"],
  concept="Process states",
  explanation="A process waiting for an event such as I/O completion moves from Running to Waiting (Blocked). "
              "When the I/O finishes it goes to Ready, and later the scheduler gives it the CPU again.",
  steps=["Running -> I/O request -> Waiting", "I/O done -> Ready -> Running"],
  wrong="Ready processes can run as soon as they get the CPU, which this one cannot. New is a process being "
        "created and Terminated is one that has finished.", seconds=20)
Q(T, "Functions", "Intermediate",
  "When the operating system stops one process and starts another, it saves the old process's registers and "
  "program counter in its process control block and loads those of the new process. This is called:",
  ["Context switching", "Thrashing", "Spooling", "Paging"],
  concept="Context switch",
  explanation="A context switch saves the state (context) of the running process and restores the state of the "
              "next one, so each process can later resume exactly where it stopped. It is pure overhead, so OS "
              "designers try to keep it fast.",
  steps=["Save state of old process, load state of new = context switch"],
  wrong="Thrashing is excessive paging. Spooling queues jobs such as print jobs on disk. Paging divides memory "
        "into fixed-size pages.", seconds=20)
Q(T, "File systems", "Intermediate",
  "Over time, the pieces of many files on a branch PC's hard disk get scattered across non-adjacent sectors, and "
  "files open slowly. Which maintenance task rearranges the pieces so that each file is stored contiguously?",
  ["Defragmentation", "Formatting", "Disk partitioning", "Compression"],
  concept="Disk fragmentation",
  explanation="Defragmentation moves the scattered fragments of files so that each file's blocks are next to each "
              "other, reducing the head movement on a hard disk. In Windows it is done by 'Defragment and Optimize "
              "Drives'.",
  steps=["Scattered file pieces = fragmentation", "Putting them back together = defragmentation"],
  wrong="Formatting erases and prepares a drive, partitioning divides it into separate volumes, and compression "
        "reduces file size.", seconds=20)
Q(T, "Windows and Linux basics", "Intermediate",
  "In Windows File Explorer, which keyboard shortcut deletes the selected file permanently, without moving it to "
  "the Recycle Bin?",
  ["Shift + Delete", "Ctrl + Delete", "Alt + Delete", "Ctrl + D"],
  concept="Deleting files in Windows",
  explanation="Pressing Delete moves a file to the Recycle Bin, from where it can be restored. Shift + Delete "
              "skips the Recycle Bin, so the file cannot be restored from there.",
  steps=["Delete -> Recycle Bin", "Shift + Delete -> bypasses the Recycle Bin"],
  wrong="Ctrl + Delete and Alt + Delete are not the bypass shortcut, and Ctrl + D, like Delete, sends the item to "
        "the Recycle Bin.", seconds=15,
  facts=[fact("Microsoft Support (Windows 11): Shift + Delete - Permanently delete the selected item without "
              "moving it to the Recycle Bin.", MS_WIN)])
Q(T, "File systems", "Advanced",
  "In a Linux ext4 file system, which data structure stores a file's owner, permissions, size, timestamps and "
  "pointers to its data blocks, but NOT the file's name?",
  ["Inode", "Superblock", "Directory entry", "Boot block"],
  concept="Inodes",
  explanation="Every file has an inode holding its metadata and the locations of its data blocks. The file name "
              "is kept in a directory entry that maps the name to the inode number. This is why one inode can have "
              "several names (hard links).",
  steps=["Per-file metadata + block pointers = inode", "Name -> directory entry -> inode number"],
  wrong="The superblock describes the whole file system (size, block count, free space). A directory entry holds "
        "the name, not the metadata. The boot block holds start-up code.", seconds=30)

# ================================================================ 5. Input and Output Devices (1 / 2 / 2)
T = "Input and Output Devices"
Q(T, "Input devices", "Basic",
  "At a bank's customer service point, a customer withdraws cash by giving her Aadhaar number and placing her "
  "finger on a small device. Which input device is this?",
  ["Biometric (fingerprint) scanner", "Light pen", "Joystick", "Barcode reader"],
  concept="Biometric input devices",
  explanation="A biometric fingerprint scanner captures the pattern of the finger so it can be matched with the "
              "stored record for authentication.",
  steps=["Finger placed on a device to verify identity = biometric scanner"],
  wrong="A light pen draws or selects on a screen, a joystick controls movement in games and simulators, and a "
        "barcode reader reads product codes.", seconds=15)
Q(T, "Output devices", "Intermediate",
  "ATMs and card-payment (POS) terminals print receipts without ink or toner, using special paper that darkens "
  "where it is heated. Which printer is this?",
  ["Thermal printer", "Inkjet printer", "Laser printer", "Dot-matrix printer"],
  concept="Types of printers",
  explanation="A thermal printer has a print head with tiny heating elements that darken heat-sensitive paper. It "
              "is small, quiet, fast and needs no ink, so it suits receipts and tickets.",
  steps=["Heat-sensitive paper, no ink = thermal printer"],
  wrong="Inkjet printers spray ink droplets, laser printers fuse toner, and dot-matrix printers strike an inked "
        "ribbon.", seconds=20)
Q(T, "Input devices", "Intermediate",
  "An architect draws plans by moving a pen-like stylus on a flat pressure-sensitive board, and the drawing appears "
  "on the computer screen. Which input device is she using?",
  ["Graphics tablet (digitiser)", "Touchpad", "Trackball", "Scanner"],
  concept="Pointing and drawing devices",
  explanation="A graphics tablet (digitiser) converts the position and pressure of a stylus on its surface into "
              "digital input, which is ideal for drawing, design and tracing maps.",
  steps=["Stylus on a flat board for drawing = graphics tablet"],
  wrong="A touchpad is a laptop's finger-operated pointer. A trackball is a ball rolled by the thumb. A scanner "
        "copies an existing paper image instead of capturing live drawing.", seconds=20)
o, a = ordered(2 ** 30, [3 * 2 ** 10, 2 ** 24, 10 ** 9], lambda v: f"{v:,}")
Q(T, "Output devices", "Advanced",
  "An HDR monitor uses 10 bits for each of the red, green and blue channels of a pixel. How many different colours "
  "can a pixel show?", o, a,
  concept="Colour depth",
  explanation="10 bits per channel give 2^10 = 1,024 levels for each of the 3 channels. The total number of "
              "colours is 1,024 x 1,024 x 1,024 = 2^30 = 1,073,741,824 (about 1.07 billion).",
  steps=["Bits per pixel = 3 x 10 = 30", "Colours = 2^30 = 1,073,741,824"],
  shortcut="Colours = 2^(total bits per pixel).",
  wrong="3,072 adds the levels (3 x 1,024) instead of multiplying them. 16,777,216 = 2^24 is ordinary 8-bit-per-"
        "channel colour. 1,000,000,000 treats 'about a billion' as exact.", seconds=40, computed=True)
o, a = ordered(2400, [1067, 1600, 3200], lambda v: f"{v:,} pixels")
Q(T, "Input devices", "Advanced",
  "A mouse sensor is set to 1,600 DPI (counts per inch). With pointer acceleration turned off and each count moving "
  "the pointer by one pixel, how far does the pointer move when the mouse is moved 1.5 inches?", o, a,
  concept="Mouse sensitivity (DPI/CPI)",
  explanation="The sensor reports 1,600 counts for every inch moved. 1.5 inches give 1,600 x 1.5 = 2,400 counts, "
              "and at one pixel per count the pointer moves 2,400 pixels.",
  steps=["Counts = DPI x distance", "1,600 x 1.5 = 2,400", "1 count = 1 pixel -> 2,400 pixels"],
  wrong="1,067 divides instead of multiplying. 1,600 is the movement for one inch. 3,200 is the movement for two "
        "inches.", seconds=30, computed=True)

# ================================================================ 6. Memory (3 / 2 / 5)
T = "Memory"
Q(T, "Secondary storage", "Basic",
  "Blu-ray discs store far more data than DVDs mainly because they are read and written with a laser of which "
  "colour, whose shorter wavelength allows smaller pits?",
  ["Blue-violet", "Red", "Infrared", "Green"],
  concept="Optical storage",
  explanation="Blu-ray uses a blue-violet laser of about 405 nm. Its shorter wavelength focuses on a smaller spot, "
              "so data can be packed more densely than on a DVD (red laser) or a CD (infrared laser).",
  steps=["Blu-ray -> blue-violet laser -> denser data"],
  wrong="DVDs use a red laser and CDs an infrared laser. Green lasers are not used for these discs.", seconds=15)
Q(T, "Primary memory", "Basic",
  "Which type of ROM is supplied blank and can be programmed by the user only once?",
  ["PROM", "EPROM", "EEPROM", "Mask ROM"],
  concept="Types of ROM",
  explanation="PROM (Programmable ROM) is written once with a special programmer by blowing internal fuses; after "
              "that it cannot be changed.",
  steps=["Programmed once by the user = PROM"],
  wrong="EPROM can be erased with ultraviolet light and reprogrammed, EEPROM can be erased electrically, and Mask "
        "ROM is programmed by the manufacturer during fabrication.", seconds=15)
Q(T, "Secondary storage", "Basic",
  "Which storage medium is a sequential-access device, because it must be wound to the position of the data, and is "
  "still used for low-cost long-term backups and archives?",
  ["Magnetic tape", "Hard disk", "SSD", "RAM"],
  concept="Sequential and direct access",
  explanation="Magnetic tape must be wound to the right position to reach data, so access is sequential. Its low "
              "cost per gigabyte suits archives and backups.",
  steps=["Sequential access + backups = magnetic tape"],
  wrong="Hard disks and SSDs allow direct (random) access, and RAM is volatile primary memory.", seconds=15)
Q(T, "Cache and units", "Intermediate",
  "Which level of cache memory is the smallest and fastest, and is built into each processor core?",
  ["L1 cache", "L2 cache", "L3 cache", "Main memory"],
  concept="Cache levels",
  explanation="L1 cache sits inside each core, often split into instruction and data caches, and is the fastest "
              "and smallest. L2 is larger and slower, and L3 is larger still and usually shared by all cores.",
  steps=["Closest to the core = L1 = smallest and fastest"],
  wrong="L2 and L3 caches are larger but slower, and main memory (RAM) is far slower than any cache.", seconds=15)
Q(T, "Secondary storage", "Intermediate",
  "Modern M.2 SSDs use a protocol designed for flash memory that talks to the CPU over PCI Express lanes, making "
  "them much faster than SSDs on the older SATA interface. What is this protocol?",
  ["NVMe", "IDE", "SCSI", "USB 2.0"],
  concept="Storage interfaces",
  explanation="NVMe (Non-Volatile Memory Express) uses PCIe lanes and many deep command queues suited to flash, "
              "giving several times the throughput of SATA, which was designed for hard disks.",
  steps=["Flash protocol over PCIe = NVMe"],
  wrong="IDE (PATA) and SCSI are older interfaces designed for disks, and USB 2.0 is an external peripheral bus "
        "limited to 480 Mbit/s.", seconds=20)
Q(T, "Cache and units", "Advanced",
  "In a write-back cache, data written by the CPU is updated only in the cache at first. What marks a cache block "
  "whose contents have changed and must be written to main memory before the block is replaced?",
  ["The dirty (modified) bit", "The valid bit", "The parity bit", "The sign bit"],
  concept="Write-back caching",
  explanation="Each block has a dirty bit that is set when the CPU writes to it. When a dirty block is evicted, it "
              "is first copied back to main memory; a clean block can simply be discarded.",
  steps=["Write hits change only the cache", "Dirty bit set", "Dirty block written back on replacement"],
  wrong="The valid bit shows whether the block holds valid data at all. A parity bit detects errors. A sign bit "
        "marks a number as negative.", seconds=25)
o, a = ordered(17, [15, 18, 26])
Q(T, "Cache and units", "Advanced",
  "A direct-mapped cache of 32 KB uses 64-byte blocks, and the processor uses 32-bit byte addresses. How many bits "
  "of each address form the tag?", o, a,
  concept="Address split in a direct-mapped cache",
  explanation="Offset bits = log2(64) = 6. Number of lines = 32 KB / 64 B = 512, so index bits = log2(512) = 9. "
              "Tag bits = 32 - 9 - 6 = 17.",
  steps=["Offset = log2(64) = 6", "Lines = 32,768 / 64 = 512 -> index = 9", "Tag = 32 - 9 - 6 = 17"],
  shortcut="Tag = address bits - log2(cache size in bytes) for a direct-mapped cache: 32 - 15 = 17.",
  wrong="15 is log2 of the cache size, not the tag. 18 uses only 8 index bits. 26 subtracts only the offset.",
  seconds=60, computed=True)
o, a = ordered(8, [2, 6, 10], lambda v: f"{v} TB")
Q(T, "Secondary storage", "Advanced",
  "A server uses RAID 5 across five 2 TB disks. Ignoring formatting overhead, how much usable storage does the "
  "array provide?", o, a,
  concept="RAID 5 capacity",
  explanation="RAID 5 stripes data with distributed parity, and the parity takes the space of one disk. Usable "
              "capacity = (n - 1) x disk size = (5 - 1) x 2 TB = 8 TB. The array survives the failure of any one "
              "disk.",
  steps=["Parity uses 1 disk's worth of space", "(5 - 1) x 2 TB = 8 TB"],
  shortcut="RAID 5 usable = (n - 1) x size; RAID 1 = half; RAID 0 = all.",
  wrong="10 TB ignores the parity. 6 TB reserves two disks, as RAID 6 would. 2 TB is the capacity of a single "
        "disk.", seconds=35, computed=True)
o, a = ordered(8, [2, 4, 16])
Q(T, "Primary memory", "Advanced",
  "How many 16K x 4 RAM chips are needed to build a memory of 64K x 8 (64K locations of 8 bits each)?", o, a,
  concept="Memory organisation with chips",
  explanation="To get 8-bit words from 4-bit chips, 2 chips are placed side by side. To get 64K locations from 16K "
              "chips, 4 such rows are needed. Total = 4 x 2 = 8 chips.",
  steps=["Width: 8 / 4 = 2 chips per row", "Depth: 64K / 16K = 4 rows", "Total = 2 x 4 = 8"],
  shortcut="Chips = (total bits) / (bits per chip) = (64K x 8) / (16K x 4) = 8.",
  wrong="2 only matches the word width and 4 only the number of locations. 16 doubles the correct count.",
  seconds=40, computed=True)
Q(T, "Cache and units", "Advanced",
  "Under the IEC binary prefixes, which unit is exactly 2^30 bytes (1,073,741,824 bytes)?",
  ["Gibibyte (GiB)", "Gigabyte (GB)", "Mebibyte (MiB)", "Tebibyte (TiB)"],
  concept="Binary (IEC) and decimal (SI) prefixes",
  explanation="IEC prefixes for powers of 2 are kibi (2^10), mebi (2^20), gibi (2^30) and tebi (2^40). The SI "
              "prefix giga means 10^9, so 1 GB = 1,000,000,000 bytes, while 1 GiB = 2^30 bytes.",
  steps=["gibi = (2^10)^3 = 2^30", "1 GiB = 1,073,741,824 bytes"],
  wrong="A gigabyte in the SI sense is 10^9 bytes. A mebibyte is 2^20 bytes and a tebibyte is 2^40 bytes.",
  seconds=20,
  facts=[fact("NIST, prefixes for binary multiples: gibi, symbol Gi, factor 2^30 (IEC 60027-2).", NIST_BIN)])

# ================================================================ 7. Internet (2 / 5 / 1)
T = "Internet"
Q(T, "Web basics", "Basic",
  "A word or image on a web page that takes you to another page or file when you click it is called a:",
  ["Hyperlink", "Bookmark", "Web browser", "Domain"],
  concept="Hyperlinks",
  explanation="A hyperlink connects one web resource to another. Clicking it makes the browser load the linked "
              "page or file.",
  steps=["Clickable link to another page = hyperlink"],
  wrong="A bookmark is a saved address in the browser, a browser is the program that shows pages, and a domain is "
        "the name of a website.", seconds=10)
Q(T, "Email", "Basic",
  "Unsolicited bulk email, such as advertisements sent to thousands of addresses without permission, is called:",
  ["Spam", "Draft", "Attachment", "Signature"],
  concept="Email terms",
  explanation="Spam is unwanted bulk email. Mail services filter it into a separate Spam or Junk folder.",
  steps=["Unwanted bulk email = spam"],
  wrong="A draft is an unsent message being written, an attachment is a file sent with an email and a signature "
        "is text added automatically at the end of messages.", seconds=10)
Q(T, "Protocols", "Intermediate",
  "Which protocol is designed for uploading and downloading files between a client and a server and traditionally "
  "uses TCP port 21 for its control connection?",
  ["FTP", "SMTP", "SNMP", "Telnet"],
  concept="File Transfer Protocol",
  explanation="FTP (File Transfer Protocol) transfers files between a client and a server, using port 21 for "
              "commands. Because plain FTP is unencrypted, secure alternatives such as SFTP or FTPS are preferred.",
  steps=["File transfer, port 21 = FTP"],
  wrong="SMTP sends email, SNMP manages network devices, and Telnet gives an unencrypted remote terminal.",
  seconds=15)
Q(T, "Protocols", "Intermediate",
  "A bank's system administrator logs in to a remote Linux server through an encrypted command-line session that "
  "replaced the insecure Telnet and uses TCP port 22 by default. Which protocol is this?",
  ["SSH", "HTTP", "FTP", "POP3"],
  concept="Secure remote login",
  explanation="SSH (Secure Shell) encrypts the login, commands and output between the administrator and the "
              "server, so passwords are not sent in plain text as with Telnet.",
  steps=["Encrypted remote login, port 22 = SSH"],
  wrong="HTTP serves web pages, FTP transfers files and POP3 downloads email.", seconds=15)
Q(T, "Web basics", "Intermediate",
  "A customer uses a browser's private (Incognito) window to check her account. Which statement about this mode is "
  "correct?",
  ["The browser does not keep her history or that session's cookies after the window is closed, but her employer "
   "or internet provider may still see the sites she visits",
   "It hides all her activity from websites, her employer and her internet provider",
   "It protects her computer from viruses and phishing sites",
   "It encrypts every website she visits, even those using plain HTTP"],
  concept="Private browsing",
  explanation="Private browsing only stops the browser from saving browsing history, cookies and site data on the "
              "device once the session ends. Websites, network administrators and the internet provider can still "
              "observe the activity.",
  steps=["Private mode = nothing kept on the device afterwards", "Network-level visibility is unchanged"],
  wrong="It does not make the user anonymous to websites, employers or ISPs, it is not antivirus or anti-phishing "
        "protection, and it does not add encryption to HTTP sites.", seconds=30,
  facts=[fact("Google Chrome Help: Chrome does not retain a record of sites visited in Incognito; cookies are "
              "removed when the session ends; websites and organisations managing the network, such as an "
              "employer or internet service provider, may still see the activity.", CHROME_INCOG)])
Q(T, "Email", "Intermediate",
  "A bank publishes a DNS TXT record listing the mail servers that are allowed to send email for its domain, so "
  "receiving servers can detect messages from forged senders. Which email-authentication mechanism is this?",
  ["SPF (Sender Policy Framework)", "MX record", "IMAP", "S/MIME"],
  concept="Email sender authentication",
  explanation="SPF lets a domain owner publish, in a DNS TXT record, which hosts may send mail using that domain. "
              "A receiver checks whether the sending server's IP address is on the list.",
  steps=["List of authorised sending servers in DNS = SPF"],
  wrong="An MX record says which server receives mail for a domain. IMAP is used to read mail from a server. "
        "S/MIME signs or encrypts individual messages with certificates.", seconds=25,
  facts=[fact("RFC 7208: SPF lets domain owners authorize the hosts allowed to use their domain names; SPF records "
              "must be published as DNS TXT records.", RFC7208)])
Q(T, "Protocols", "Intermediate",
  "For audit trails, all of a bank's servers and branch systems must show exactly the same time. Which protocol "
  "synchronises computer clocks over a network?",
  ["NTP", "SNMP", "DHCP", "ARP"],
  concept="Network Time Protocol",
  explanation="NTP (Network Time Protocol) synchronises a computer's clock with reference time servers, usually to "
              "within milliseconds. Consistent timestamps are essential for logs, transactions and investigations.",
  steps=["Clock synchronisation = NTP"],
  wrong="SNMP monitors network devices, DHCP assigns IP addresses and ARP finds MAC addresses.", seconds=15,
  facts=[fact("RFC 5905: The Network Time Protocol (NTP) is widely used to synchronize computer clocks in the "
              "Internet.", RFC5905)])
Q(T, "Web basics", "Advanced",
  "Two URLs have the same origin only if their scheme, host and port are all the same. Which URL has the same origin "
  "as https://www.bank.example/login?",
  ["https://www.bank.example:443/help", "http://www.bank.example/login", "https://bank.example/login",
   "https://www.bank.example:8443/login"],
  concept="Same-origin policy",
  explanation="https uses port 443 by default, so https://www.bank.example:443/help has the same scheme (https), "
              "host (www.bank.example) and port (443) as the original. A different path does not matter.",
  steps=["Original: https, www.bank.example, port 443", "Option with :443 matches all three; path is ignored"],
  wrong="http:// changes the scheme (and the default port to 80). bank.example is a different host from "
        "www.bank.example. Port 8443 differs from 443.", seconds=40,
  facts=[fact("MDN: two URLs have the same origin if the protocol, port (if specified) and host are the same; a "
              "different path alone does not change the origin.", MDN_SOP)])

# ================================================================ 8. Networking (3 / 2 / 3)
T = "Networking"
Q(T, "Devices", "Basic",
  "Which device lets laptops and phones connect over Wi-Fi to a bank branch's wired LAN?",
  ["Wireless access point", "Repeater", "Modem", "Hub"],
  concept="Wireless networking devices",
  explanation="A wireless access point (WAP) broadcasts a Wi-Fi network and bridges wireless devices to the wired "
              "Ethernet LAN.",
  steps=["Wi-Fi devices joining a wired LAN = access point"],
  wrong="A repeater only regenerates a signal, a modem converts signals for a telephone or cable line, and a hub "
        "joins wired devices.", seconds=15)
Q(T, "Topologies", "Basic",
  "A company's head office uses a star network and its warehouse uses a ring network, and the two are connected "
  "together. A topology that combines two or more different basic topologies is called a:",
  ["Hybrid topology", "Mesh topology", "Bus topology", "Point-to-point topology"],
  concept="Hybrid topology",
  explanation="A hybrid topology joins two or more different topologies, such as star with ring or bus, into one "
              "network. Large organisations usually end up with hybrid networks.",
  steps=["Star + ring joined = hybrid"],
  wrong="Mesh links devices to many others directly, bus uses one backbone cable and point-to-point is a single "
        "link between two devices.", seconds=15)
Q(T, "OSI and TCP/IP", "Basic",
  "Which layer of the OSI model is closest to the user and provides network services such as email, file transfer "
  "and web browsing to applications?",
  ["Application layer", "Physical layer", "Network layer", "Data link layer"],
  concept="OSI layers",
  explanation="The application layer (layer 7) is the top layer. Protocols such as HTTP, SMTP and FTP work here "
              "and give applications access to the network.",
  steps=["Top layer, user-facing services = application layer (7)"],
  wrong="The physical layer carries raw bits, the network layer routes packets and the data link layer handles "
        "frames between neighbouring devices.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "The ping command checks whether a host is reachable by sending Echo Request messages and waiting for Echo "
  "Replies. Which protocol carries these messages?",
  ["ICMP", "ARP", "UDP", "DHCP"],
  concept="ICMP and ping",
  explanation="ICMP (Internet Control Message Protocol) carries control and error messages for IP. Ping sends ICMP "
              "Echo (type 8) and the target answers with Echo Reply (type 0).",
  steps=["ping = ICMP Echo Request / Echo Reply"],
  wrong="ARP finds MAC addresses, UDP is a transport protocol for applications, and DHCP assigns IP addresses.",
  seconds=20,
  facts=[fact("RFC 792 (ICMP): type 8 is the echo message and type 0 the echo reply; the data received in the "
              "echo message must be returned in the echo reply.", RFC792)])
Q(T, "Devices", "Intermediate",
  "Which network security device or program examines incoming and outgoing traffic and allows or blocks it "
  "according to a set of rules, for example at the boundary between a bank's internal network and the internet?",
  ["Firewall", "Repeater", "Hub", "Modem"],
  concept="Firewalls",
  explanation="A firewall enforces a security policy: it permits or denies traffic based on rules such as source, "
              "destination, port and protocol, separating trusted internal networks from untrusted ones.",
  steps=["Rule-based allow/block of traffic = firewall"],
  wrong="A repeater regenerates signals, a hub copies traffic to every port and a modem converts signals; none of "
        "them filter traffic by rules.", seconds=15)
o, a = ordered(16, [4, 20, 4096])
Q(T, "OSI and TCP/IP", "Advanced",
  "A bank divides the IPv4 block 172.16.0.0/16 into equal subnets with prefix /20. How many subnets are formed?",
  o, a,
  concept="Counting subnets",
  explanation="Going from /16 to /20 borrows 20 - 16 = 4 bits for the subnet part, so there are 2^4 = 16 subnets "
              "(172.16.0.0, 172.16.16.0, ..., 172.16.240.0), each with 2^12 = 4,096 addresses.",
  steps=["Borrowed bits = 20 - 16 = 4", "Subnets = 2^4 = 16"],
  shortcut="Subnets = 2^(new prefix - old prefix).",
  wrong="4 is the number of borrowed bits, not subnets. 20 is the prefix length. 4,096 is the number of addresses "
        "in each /20 subnet.", seconds=40, computed=True)
Q(T, "Devices", "Advanced",
  "A bank wants its ATMs, teller PCs and CCTV cameras connected to the same physical switches but kept in separate "
  "broadcast domains, as if they were on separate networks. Which technology does this?",
  ["VLAN (IEEE 802.1Q)", "VPN", "NAT", "Repeater"],
  concept="Virtual LANs",
  explanation="A VLAN logically divides one physical switched network into separate broadcast domains. Traffic "
              "between VLANs must pass through a router or layer-3 switch, where it can be filtered. IEEE 802.1Q "
              "tags frames with their VLAN ID.",
  steps=["Same switches, separate broadcast domains = VLAN"],
  wrong="A VPN builds an encrypted tunnel over another network, NAT translates private addresses to public ones, "
        "and a repeater only boosts signals.", seconds=30)
o, a = ordered(1_000_000, [125_000, 500_000, 8_000_000], lambda v: f"{v:,} bytes")
Q(T, "OSI and TCP/IP", "Advanced",
  "To keep a link fully busy, TCP must be allowed to have at least (bandwidth x round-trip time) of data in flight. "
  "For a 100 Mbps link with a round-trip time of 80 ms, what is this amount in bytes?", o, a,
  concept="Bandwidth-delay product",
  explanation="Bandwidth x RTT = 100 x 10^6 bits/s x 0.08 s = 8,000,000 bits. Dividing by 8 gives 1,000,000 bytes "
              "(about 1 MB), so the TCP window must be at least this large.",
  steps=["100 x 10^6 x 0.080 = 8 x 10^6 bits", "8 x 10^6 / 8 = 1,000,000 bytes"],
  wrong="125,000 bytes is the data sent in just 10 ms. 500,000 bytes uses the one-way delay (40 ms). 8,000,000 is "
        "the answer in bits, not bytes.", seconds=50, computed=True)

# ================================================================ 9. Cybersecurity (2 / 3 / 2)
T = "Cybersecurity"
Q(T, "Malware", "Basic",
  "Software that secretly monitors a user's activity, such as websites visited and data typed, and sends this "
  "information to a third party without the user's knowledge is called:",
  ["Spyware", "Ransomware", "Firewall", "Defragmenter"],
  concept="Spyware",
  explanation="Spyware hides on a device and collects information about the user, such as browsing habits, "
              "credentials or personal data, and sends it to an outsider.",
  steps=["Secretly collects and sends user information = spyware"],
  wrong="Ransomware locks or encrypts files for a ransom. A firewall is a security tool. A defragmenter "
        "reorganises files on a disk.", seconds=15)
Q(T, "Encryption and authentication", "Basic",
  "Converting readable data (plaintext) into an unreadable form (ciphertext), so that only someone with the right "
  "key can read it, is called:",
  ["Encryption", "Decryption", "Compression", "Formatting"],
  concept="Encryption",
  explanation="Encryption scrambles plaintext into ciphertext using an algorithm and a key. Decryption, with the "
              "correct key, turns the ciphertext back into plaintext.",
  steps=["Plaintext -> ciphertext = encryption"],
  wrong="Decryption is the reverse process. Compression reduces size and formatting prepares a disk; neither "
        "protects data with a key.", seconds=10)
Q(T, "Phishing and social engineering", "Intermediate",
  "A man in a vendor's uniform walks into a branch, says he has been sent to upgrade the server after a 'failed "
  "audit', mentions the regional manager by name, and asks the clerk for the administrator password. Building such "
  "an invented story to obtain information is called:",
  ["Pretexting", "Tailgating", "Baiting", "Shoulder surfing"],
  concept="Pretexting",
  explanation="In pretexting the attacker creates a believable false scenario (the pretext) and plays a role, such "
              "as an engineer or auditor, to persuade the victim to hand over information or access.",
  steps=["Made-up scenario + impersonation to get information = pretexting"],
  wrong="Tailgating is following someone through a secured door. Baiting leaves a tempting item such as an "
        "infected USB drive. Shoulder surfing is watching someone type.", seconds=25)
Q(T, "Malware", "Intermediate",
  "A bank's servers become slow and their CPU usage stays near 100%. Investigation finds hidden software using the "
  "computers to mine cryptocurrency for an attacker. This is called:",
  ["Cryptojacking", "Ransomware", "Adware", "Phishing"],
  concept="Cryptojacking",
  explanation="Cryptojacking secretly uses a victim's computing power to mine cryptocurrency. Signs are high CPU "
              "use, heat and slowness; files are not encrypted and no ransom is demanded.",
  steps=["Hidden mining with the victim's CPU = cryptojacking"],
  wrong="Ransomware encrypts data and demands payment. Adware shows advertisements. Phishing is a deceptive "
        "message, not mining software.", seconds=20)
Q(T, "Encryption and authentication", "Intermediate",
  "When a browser opens an HTTPS banking site, it trusts the site's public key because the site's certificate is "
  "digitally signed by a trusted third party. What is this third party called?",
  ["Certificate Authority (CA)", "Internet Service Provider (ISP)", "Domain Name System (DNS) server",
   "Network Interface Card (NIC)"],
  concept="Digital certificates and PKI",
  explanation="A Certificate Authority verifies who owns a domain or organisation and signs a digital certificate "
              "binding that identity to a public key. Browsers trust certificates issued by CAs in their trust "
              "store.",
  steps=["Signs certificates that bind identity to public key = CA"],
  wrong="An ISP provides internet access, a DNS server translates names to IP addresses, and a NIC is network "
        "hardware.", seconds=20)
Q(T, "Encryption and authentication", "Advanced",
  "In HTTPS (TLS), public-key cryptography is used to set up a shared session key, and the actual data is then "
  "encrypted with a symmetric cipher such as AES. Why is this combination used?",
  ["Symmetric encryption is much faster for bulk data, while public-key methods solve the problem of agreeing a "
   "key securely",
   "Symmetric ciphers can never be broken, so public-key methods are not needed for data",
   "Public-key cryptography cannot encrypt any data at all",
   "Symmetric keys do not need to be kept secret"],
  concept="Hybrid encryption",
  explanation="Asymmetric operations are slow but let two parties establish a secret over an open network. "
              "Symmetric ciphers are fast but need a shared secret key. TLS uses the first to agree the key and the "
              "second to protect the bulk of the data.",
  steps=["Asymmetric: key agreement / authentication", "Symmetric: fast bulk encryption"],
  wrong="No practical cipher is unbreakable in principle. Public-key methods can encrypt data, just slowly. A "
        "symmetric key must be kept secret, because anyone holding it can decrypt.", seconds=35)
Q(T, "Phishing and social engineering", "Advanced",
  "An attacker copies a genuine email that customers recently received from their bank, keeps the same text and "
  "layout, replaces the link with one to a fake site, and resends it as an 'updated version'. This technique is:",
  ["Clone phishing", "Whaling", "Vishing", "Pharming"],
  concept="Clone phishing",
  explanation="Clone phishing reuses a legitimate message the victim has already seen, swapping its link or "
              "attachment for a malicious one. Familiarity with the original makes the copy convincing.",
  steps=["Copy of a real earlier email with a swapped link = clone phishing"],
  wrong="Whaling targets senior executives. Vishing uses phone calls. Pharming redirects users through tampered "
        "DNS without any email.", seconds=25)

# ================================================================ 10. Database Fundamentals (3 / 5 / 3)
T = "Database Fundamentals"
Q(T, "DBMS concepts", "Basic",
  "In a relational database table, a column (such as Name or Balance) is also called a(n):",
  ["Attribute", "Tuple", "Relation", "Cardinality"],
  concept="Relational terminology",
  explanation="In the relational model a table is a relation, a row is a tuple and a column is an attribute (also "
              "called a field).",
  steps=["Column = attribute (field)"],
  wrong="A tuple is a row, a relation is the whole table and cardinality is the number of rows.", seconds=10)
Q(T, "SQL basics", "Basic",
  "Which SQL command changes the values in existing rows of a table, for example to correct a customer's mobile "
  "number?",
  ["UPDATE", "INSERT", "ALTER", "SELECT"],
  concept="DML commands",
  explanation="UPDATE modifies data in existing rows: UPDATE Customers SET mobile = '...' WHERE cust_id = 7.",
  steps=["Change existing data = UPDATE"],
  wrong="INSERT adds new rows, ALTER changes the table's structure (columns), and SELECT only reads data.",
  seconds=10)
Q(T, "DBMS concepts", "Basic",
  "The number of attributes (columns) in a relation is called its:",
  ["Degree", "Cardinality", "Domain", "Instance"],
  concept="Degree and cardinality",
  explanation="Degree = number of columns; cardinality = number of rows. A table with 5 columns and 200 rows has "
              "degree 5 and cardinality 200.",
  steps=["Columns -> degree", "Rows -> cardinality"],
  wrong="Cardinality counts rows, a domain is the set of allowed values for an attribute, and an instance is the "
        "data in the table at a given moment.", seconds=15)
Q(T, "SQL basics", "Intermediate",
  "Table Cust has rows (Asha, 52000), (Ravi, 18000) and (Meena, 75000) for (name, balance). In what order are the "
  "names returned by SELECT name FROM Cust ORDER BY balance; ?",
  ["Ravi, Asha, Meena", "Meena, Asha, Ravi", "Asha, Ravi, Meena", "Asha, Meena, Ravi"],
  concept="ORDER BY default order",
  explanation="ORDER BY sorts in ascending order unless DESC is written. Ascending balances are 18000 (Ravi), 52000 "
              "(Asha), 75000 (Meena).",
  steps=["No ASC/DESC -> ascending", "18000 < 52000 < 75000", "Ravi, Asha, Meena"],
  wrong="Meena, Asha, Ravi is descending order. Asha, Ravi, Meena is the insertion order. Asha, Meena, Ravi is "
        "alphabetical order of names.", seconds=25, computed=True)
o, a = ordered(3, [2, 4, 6])
Q(T, "SQL basics", "Intermediate",
  "Table Accounts has six rows whose branch values are Pune, Delhi, Pune, Agra, Delhi and Pune. What does SELECT "
  "COUNT(DISTINCT branch) FROM Accounts; return?", o, a,
  concept="COUNT(DISTINCT ...)",
  explanation="DISTINCT removes duplicate values before counting. The different branches are Pune, Delhi and Agra, "
              "so the result is 3.",
  steps=["Distinct values: Pune, Delhi, Agra", "Count = 3"],
  wrong="6 is COUNT(branch) or COUNT(*), counting every row. 2 and 4 miscount the distinct values.", seconds=20,
  computed=True)
Q(T, "DBMS concepts", "Intermediate",
  "A customer's fund transfer is committed and the system shows 'Transaction successful'. One second later the "
  "server loses power. On restart, the transfer is still recorded. Which ACID property guarantees this?",
  ["Durability", "Atomicity", "Consistency", "Isolation"],
  concept="ACID properties",
  explanation="Durability means that once a transaction commits, its changes survive later failures such as power "
              "loss or crashes. DBMSs achieve this with write-ahead logs and recovery.",
  steps=["Committed changes survive failure = durability"],
  wrong="Atomicity is all-or-nothing execution, consistency keeps data valid under the rules, and isolation stops "
        "concurrent transactions from interfering.", seconds=20)
Q(T, "Keys", "Intermediate",
  "In Customers(CustID, Name, City), CustID alone uniquely identifies every row. The set {CustID, Name} also "
  "uniquely identifies every row, but it is not minimal. Such a set of attributes is called a:",
  ["Super key", "Candidate key", "Foreign key", "Alternate key"],
  concept="Super keys and candidate keys",
  explanation="A super key is any set of attributes that uniquely identifies rows, even if it contains extra "
              "attributes. A candidate key is a minimal super key. {CustID, Name} is a super key but not a "
              "candidate key, because CustID alone is enough.",
  steps=["Unique but not minimal = super key", "Minimal super key = candidate key"],
  wrong="A candidate key must be minimal. A foreign key refers to another table. An alternate key is a candidate "
        "key not chosen as the primary key.", seconds=25)
Q(T, "SQL basics", "Intermediate",
  "The SQL commands COMMIT, ROLLBACK and SAVEPOINT belong to which category?",
  ["TCL (Transaction Control Language)", "DDL (Data Definition Language)", "DML (Data Manipulation Language)",
   "DCL (Data Control Language)"],
  concept="Categories of SQL commands",
  explanation="TCL commands manage transactions: COMMIT makes changes permanent, ROLLBACK undoes them and "
              "SAVEPOINT marks a point to roll back to.",
  steps=["Transaction control = TCL"],
  wrong="DDL defines structure (CREATE, ALTER, DROP), DML works on data (INSERT, UPDATE, DELETE) and DCL handles "
        "permissions (GRANT, REVOKE).", seconds=15)
o, a = ordered(60000, [38000, 45000, 72000], lambda v: f"{v:,}")
Q(T, "SQL basics", "Advanced",
  "Table Emp has salaries 45000, 72000, 72000, 60000 and 38000. What does this query return? "
  "SELECT MAX(salary) FROM Emp WHERE salary < (SELECT MAX(salary) FROM Emp);", o, a,
  concept="Subquery for the second-highest value",
  explanation="The subquery returns the highest salary, 72000. The outer query takes the maximum of salaries below "
              "72000: 45000, 60000 and 38000, which is 60000. Both 72000 rows are excluded.",
  steps=["Inner MAX = 72000", "Salaries < 72000: 45000, 60000, 38000", "MAX = 60000"],
  wrong="72000 is the highest salary, excluded by the < condition. 45000 is the third-highest distinct value, "
        "and 38000 is the lowest.", seconds=40, computed=True)
Q(T, "DBMS concepts", "Advanced",
  "Transaction T1 changes an account's balance from 10,000 to 4,000 but has not committed. Transaction T2 reads "
  "4,000 and uses it. T1 then rolls back. What is T2's problem called?",
  ["Dirty read", "Lost update", "Phantom read", "Non-repeatable read"],
  concept="Concurrency anomalies",
  explanation="A dirty read happens when a transaction reads data written by another transaction that has not yet "
              "committed. Here T2 used 4,000, a value that never officially existed after T1's rollback. The READ "
              "COMMITTED isolation level prevents it.",
  steps=["T2 reads uncommitted change", "T1 rolls back", "= dirty read"],
  wrong="A lost update is one write overwriting another. A phantom read is new rows appearing in a repeated query. "
        "A non-repeatable read is a committed value changing between two reads by the same transaction.",
  seconds=30)
Q(T, "DBMS concepts", "Advanced",
  "Table Employee(EmpID, Name, DeptID, DeptName) has primary key EmpID, and DeptID determines DeptName. Which normal "
  "form does this table violate, and why?",
  ["Third Normal Form, because DeptName depends on EmpID only through DeptID (a transitive dependency)",
   "First Normal Form, because DeptName is not atomic",
   "Second Normal Form, because DeptName depends on part of a composite key",
   "None; the table is already in Third Normal Form"],
  concept="Third Normal Form",
  explanation="3NF requires that no non-key attribute depends on another non-key attribute. EmpID -> DeptID -> "
              "DeptName is a transitive dependency. The table is in 2NF (its key has a single column, so no partial "
              "dependency is possible) but not in 3NF. Moving (DeptID, DeptName) to a Department table fixes it.",
  steps=["Key = EmpID (single column) -> 2NF holds", "DeptID -> DeptName: non-key -> non-key",
         "Transitive dependency -> violates 3NF"],
  wrong="All values are atomic, so 1NF holds. With a one-column key there is no partial dependency, so 2NF holds. "
        "The transitive dependency means it is not in 3NF.", seconds=40)

# ================================================================ 11. MS Office (2 / 3 / 2)
T = "MS Office"
Q(T, "Shortcuts", "Basic",
  "In MS Word, which keyboard shortcut selects all the content of the document?",
  ["Ctrl + A", "Ctrl + S", "Ctrl + E", "Ctrl + L"],
  concept="Word shortcuts",
  explanation="Ctrl + A selects all document content, for example to change the font of the whole document at "
              "once.",
  steps=["Select All = Ctrl + A"],
  wrong="Ctrl + S saves, Ctrl + E centres the paragraph and Ctrl + L left-aligns it.", seconds=10,
  facts=[fact("Microsoft Support, Word shortcuts: Select all document content - Ctrl+A.", MS_WORD)])
Q(T, "MS PowerPoint", "Basic",
  "In PowerPoint, which keyboard shortcut inserts a new slide?",
  ["Ctrl + M", "Ctrl + N", "Ctrl + D", "F5"],
  concept="PowerPoint shortcuts",
  explanation="Ctrl + M inserts a new slide after the current one.",
  steps=["New slide = Ctrl + M"],
  wrong="Ctrl + N creates a new presentation, Ctrl + D duplicates the selected object or slide, and F5 starts "
        "the slide show.", seconds=10,
  facts=[fact("Microsoft Support, PowerPoint shortcuts: Insert a new slide - Ctrl+M.", MS_PPT)])
Q(T, "Shortcuts", "Intermediate",
  "In Excel for Windows, which keyboard shortcut inserts the SUM formula (AutoSum) for the cells above or to the "
  "left of the active cell?",
  ["Alt + =", "Ctrl + T", "Shift + F3", "F4"],
  concept="Excel shortcuts",
  explanation="Alt + = (Alt and the equal sign) inserts =SUM() with a suggested range, the same as clicking "
              "AutoSum.",
  steps=["AutoSum = Alt + ="],
  wrong="Ctrl + T creates a table, Shift + F3 opens the Insert Function dialog, and F4 repeats the last action "
        "or cycles cell references.", seconds=15,
  facts=[fact("Microsoft Support, Excel shortcuts (Windows): Insert the Sum formula - Alt+Equal sign (=).",
              MS_EXCEL)])
o, a = ordered(-8, [-7, 7, 8])
Q(T, "MS Excel", "Intermediate",
  "What value does the Excel formula =INT(-7.5) return?", o, a,
  concept="INT rounds down",
  explanation="INT rounds a number down to the nearest integer. For negative numbers 'down' means away from zero, "
              "so -7.5 becomes -8, not -7.",
  steps=["INT = round down to an integer", "-8 < -7.5 < -7", "Down -> -8"],
  shortcut="INT(x) is the floor of x; TRUNC(x) simply drops the decimals (TRUNC(-7.5) = -7).",
  wrong="-7 is what TRUNC gives (removing the decimal part). 7 and 8 lose the minus sign.", seconds=20,
  computed=True,
  facts=[fact("Microsoft Support, INT: rounds a number down to the nearest integer; =INT(-8.9) gives -9 because "
              "rounding a negative number down rounds it away from 0.", MS_INT)])
Q(T, "MS Word", "Intermediate",
  "A loan agreement drafted in MS Word is sent to the legal team. The team wants every insertion and deletion they "
  "make to be marked so the author can accept or reject each one. Which Word feature should they turn on?",
  ["Track Changes", "Mail Merge", "Format Painter", "AutoCorrect"],
  concept="Reviewing documents in Word",
  explanation="Track Changes (Review tab; shortcut Ctrl + Shift + E) records every edit with the reviewer's name. "
              "The author can then accept or reject each change.",
  steps=["Record edits for accept/reject = Track Changes"],
  wrong="Mail Merge creates personalised copies, Format Painter copies formatting, and AutoCorrect fixes typing "
        "mistakes automatically.", seconds=20,
  facts=[fact("Microsoft Support, Word shortcuts: Turn change tracking on or off - Ctrl+Shift+E.", MS_WORD)])
o, a = ordered(EMI, [1000.00, 8333.33, 9333.33], lambda v: f"{v:,.2f}")
Q(T, "MS Excel", "Advanced",
  "A loan of Rs 1,00,000 is repaid in 12 equal monthly instalments at 12% per year, compounded monthly. What does "
  "=ROUND(PMT(12%/12, 12, -100000), 2) return?", o, a,
  concept="PMT function (EMI)",
  explanation="PMT(rate, nper, pv) gives the equal payment per period. Monthly rate = 1%, nper = 12, pv = 100000 "
              "(entered as negative so the payment is positive). EMI = P x r / (1 - (1 + r)^-n) = 100000 x 0.01 / "
              "(1 - 1.01^-12) = 8,884.88.",
  steps=["rate = 12% / 12 = 1%", "EMI = 1000 / (1 - 1.01^-12)", "1.01^-12 = 0.88745", "1000 / 0.11255 = 8,884.88"],
  wrong="1,000.00 is only the first month's interest. 8,333.33 repays principal with no interest. 9,333.33 is "
        "flat interest (1,12,000 / 12), which ignores the reducing balance.", seconds=60, computed=True,
  facts=[fact("Microsoft Support, PMT: syntax PMT(rate, nper, pv, [fv], [type]); for monthly payments use the "
              "annual rate / 12 and keep units of rate and nper consistent.", MS_PMT)])
Q(T, "MS Excel", "Advanced",
  "A2:A5 hold balance slabs 0, 50000, 100000 and 500000 (sorted ascending), and B2:B5 hold interest rates 3.0%, "
  "3.5%, 4.0% and 4.5%. What does =VLOOKUP(73000, A2:B5, 2, TRUE) return?",
  ["3.5%", "3.0%", "4.0%", "#N/A"],
  concept="VLOOKUP approximate match",
  explanation="With TRUE (approximate match) and the first column sorted ascending, VLOOKUP finds the largest value "
              "that is less than or equal to the lookup value. 73000 is not in the list; the largest slab not above "
              "it is 50000, whose rate is 3.5%.",
  steps=["Approximate match -> largest value <= 73000", "= 50000", "Return column 2 -> 3.5%"],
  shortcut="Approximate VLOOKUP is the standard way to look up slabs: it always picks the slab you have reached.",
  wrong="3.0% belongs to the 0 slab, which is not the largest value <= 73000. 4.0% belongs to 100000, which is "
        "above 73000. #N/A would appear with FALSE (exact match) or if the value were below the first slab.",
  seconds=40, computed=True)

# ================================================================ 12. Digital Payments (2 / 1 / 1)
T = "Digital Payments"
Q(T, "Payment technology", "Basic",
  "Which domestic card payment network was launched by NPCI to give India its own scheme for debit, credit and "
  "prepaid cards?",
  ["RuPay", "Visa", "Mastercard", "American Express"],
  concept="Indian card networks",
  explanation="RuPay is the card scheme of the National Payments Corporation of India (NPCI). It provides debit, "
              "credit and prepaid cards accepted at ATMs, POS terminals and online.",
  steps=["NPCI's card network = RuPay"],
  wrong="Visa, Mastercard and American Express are international card networks headquartered in the United States.",
  seconds=10, web=SC,
  facts=[fact("NPCI: RuPay is the first-of-its-kind domestic card payment network of India, launched by NPCI to "
              "fulfil RBI's vision of domestic payment cards.", NPCI_RUPAY)])
Q(T, "Card security", "Basic",
  "Fraudsters fit a hidden device over an ATM's card slot that copies the magnetic-stripe data of every card "
  "inserted, so that fake cards can be made. This fraud is called:",
  ["Card skimming", "Tokenisation", "Vishing", "Pharming"],
  concept="ATM skimming",
  explanation="A skimmer reads card data as the card enters the slot; often a hidden camera or fake keypad also "
              "captures the PIN. Chip cards and checking the slot for loose attachments reduce the risk.",
  steps=["Device copies card data at the slot = skimming"],
  wrong="Tokenisation is a security measure that replaces card numbers with tokens. Vishing is fraud by phone call "
        "and pharming redirects users to fake websites.", seconds=15)
Q(T, "Payment technology", "Intermediate",
  "At a business correspondent's micro-ATM in a village, a customer withdraws cash using only her Aadhaar number, "
  "her bank's name and her fingerprint, without any card. Which NPCI system is this?",
  ["AePS (Aadhaar Enabled Payment System)", "NACH (National Automated Clearing House)",
   "NETC (National Electronic Toll Collection)", "BBPS (Bharat Bill Payment System)"],
  concept="Aadhaar-based payments",
  explanation="AePS lets a customer use Aadhaar authentication (biometrics) at micro-ATMs run by business "
              "correspondents for cash withdrawal, deposit, balance enquiry and fund transfer from an Aadhaar-linked "
              "bank account.",
  steps=["Aadhaar + fingerprint at a micro-ATM = AePS"],
  wrong="NACH handles bulk recurring debits and credits, NETC is FASTag toll collection, and BBPS is for paying "
        "bills.", seconds=20, web=SC,
  facts=[fact("NPCI AePS product booklet: NPCI developed AePS to leverage Aadhaar authentication through the "
              "Business Correspondent channel; it is accessed at biometric-enabled micro-ATMs.", NPCI_AEPS)])
Q(T, "Payment technology", "Advanced",
  "When a customer pays at a shop's card terminal, several parties are involved. Which of them is the 'acquirer' "
  "(acquiring bank)?",
  ["The merchant's bank, which processes card payments on the merchant's behalf and credits its account",
   "The cardholder's bank, which issued the card and approves or declines the payment",
   "The card network, such as RuPay or Visa, which routes the transaction between banks",
   "The company that manufactures the card terminal"],
  concept="Parties in a card transaction",
  explanation="The acquirer is the bank (or payment processor) that has signed up the merchant, accepts its card "
              "transactions and settles the money into its account. The issuer is the cardholder's bank. The "
              "network connects acquirer and issuer.",
  steps=["Issuer = cardholder's bank", "Acquirer = merchant's bank", "Network = routes between them"],
  wrong="The cardholder's bank is the issuer. The card network is the scheme that links the two banks. The terminal "
        "maker only supplies hardware.", seconds=30)

# ================================================================ 13. Computer Abbreviations (1 / 3 / 3)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic",
  "When a computer is switched on, its firmware first runs a quick check of the RAM, keyboard and other hardware, "
  "called POST. What does POST stand for?",
  ["Power-On Self-Test", "Primary Operating System Test", "Power Output Status Test", "Processor On-Start Timer"],
  concept="Boot abbreviations",
  explanation="POST (Power-On Self-Test) is the diagnostic routine run by BIOS/UEFI firmware before the operating "
              "system loads. Errors may be reported by beep codes or messages.",
  steps=["POST = Power-On Self-Test"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate", "Screenshots are often saved in the lossless PNG format. What does PNG stand for?",
  ["Portable Network Graphics", "Personal Network Graphics", "Portable Native Graphic", "Picture Network Group"],
  concept="File-format abbreviations",
  explanation="PNG (Portable Network Graphics) is a lossless image format that supports transparency, so it suits "
              "screenshots, logos and diagrams.",
  steps=["PNG = Portable Network Graphics"], wrong="The other expansions are made up.", seconds=15)
Q(T, S, "Intermediate", "What does LCD, a common flat-panel display technology, stand for?",
  ["Liquid Crystal Display", "Light Crystal Diode", "Liquid Colour Display", "Low Current Display"],
  concept="Display abbreviations",
  explanation="An LCD (Liquid Crystal Display) uses liquid crystals that control light from a backlight to form "
              "the image.",
  steps=["LCD = Liquid Crystal Display"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "Smart meters, connected ATMs and sensors that send data over the internet are examples of IoT. What does IoT "
  "stand for?",
  ["Internet of Things", "Integration of Technology", "Internet of Terminals", "Input over Transmission"],
  concept="Technology abbreviations",
  explanation="IoT (Internet of Things) refers to everyday physical devices fitted with sensors and network "
              "connections so they can collect and exchange data.",
  steps=["IoT = Internet of Things"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Advanced", "What is the full form of SMTP, the protocol used to send email between mail servers?",
  ["Simple Mail Transfer Protocol", "Secure Mail Transmission Protocol", "Standard Message Transfer Process",
   "Simple Message Transport Program"],
  concept="Protocol abbreviations",
  explanation="SMTP (Simple Mail Transfer Protocol) is used by email clients to submit mail and by mail servers to "
              "relay it to other servers.",
  steps=["SMTP = Simple Mail Transfer Protocol"], wrong="The other expansions are made up.", seconds=15)
Q(T, S, "Advanced", "Wi-Fi networks in a branch should be secured with WPA2 or WPA3. What does WPA stand for?",
  ["Wi-Fi Protected Access", "Wireless Private Address", "Wide Protocol Authentication", "Web Protection Algorithm"],
  concept="Wireless security abbreviations",
  explanation="WPA (Wi-Fi Protected Access) is the family of Wi-Fi security protocols that replaced the weak WEP. "
              "WPA2 and WPA3 encrypt wireless traffic and authenticate devices.",
  steps=["WPA = Wi-Fi Protected Access"], wrong="The other expansions are made up.", seconds=15)
Q(T, S, "Advanced",
  "SSL was the original protocol for securing web connections and has been replaced by TLS. What does SSL stand for?",
  ["Secure Sockets Layer", "Secure System Login", "Safe Server Link", "Standard Security Layer"],
  concept="Security abbreviations",
  explanation="SSL (Secure Sockets Layer) was developed by Netscape in the 1990s. Its successor TLS (Transport "
              "Layer Security) is what HTTPS uses today, though certificates are still often called 'SSL "
              "certificates'.",
  steps=["SSL = Secure Sockets Layer"], wrong="The other expansions are made up.", seconds=15)

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_004_plan.json").read_text(encoding="utf-8"))
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
    "batch_id": "BATCH_004",
    "created_at": TODAY,
    "notes": "BATCH_004 Computer Knowledge part: 100 original questions (BANK_COMP_000303 to BANK_COMP_000402). "
             "Computable answers (binary addition, bits for 300, hex to binary, unknown radix, excess-3, Amdahl's "
             "law, 10-bit colour depth, mouse counts, cache tag bits, RAID 5 capacity, chip count, subnet count, "
             "bandwidth-delay product, SQL ORDER BY / COUNT(DISTINCT) / second-highest via sqlite3, Excel INT, PMT "
             "and approximate VLOOKUP) are re-derived in tools/batch_004/computer.py. Shortcuts, INT, PMT, "
             "same-origin, IEC prefixes, SPF, NTP, ICMP echo, Apache 2.0 patent grant and Incognito behaviour were "
             "checked on the cited pages on 2026-11-05; Intel 4004, RuPay and AePS were confirmed from search "
             "results only (web:search-confirmed).",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_004_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
