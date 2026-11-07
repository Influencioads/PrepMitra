"""Writes batches/parts/BATCH_003_COMP.json: the 100 Computer Knowledge questions of BATCH_003.

Every computable answer (binary subtraction, octal conversion, one's complement, Gray code, pipeline cycles, DDR4
bandwidth, Round Robin waiting time, LRU page faults, umask, audio file size, print size, decimal vs binary units,
disk capacity, subnet sizing, IPv6 compression, Caesar cipher, SQL NOT BETWEEN with NULL via sqlite3, Excel LARGE,
INDEX/MATCH, COUNTIFS and SUMPRODUCT results) is re-derived below with assertions before the file is written. The
plan quota per (topic, difficulty), the ID range and the answer-key balance are also asserted. If any assertion
fails, nothing is written.

    python tools/batch_003/computer.py      (run from docs/question-bank)
"""

import ipaddress
import json
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
FIRST_ID = 203
AI = ("ai:author-solve", "ai:independent-check")
COMPUTED = ("script:recompute", "ai:author-solve", "ai:independent-check")

_rng = random.Random(20261105 + 3)
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
# Number systems
B = lambda s: int(s, 2)
assert B("110010") - B("10111") == 27 == B("11011")
assert [B(x) for x in ("10011", "11001", "11111")] == [19, 25, 31]
assert format(100, "o") == "144" and format(100, "x") == "64"
assert "".join("1" if c == "0" else "0" for c in "10110100") == "01001011"
assert format((B("01001011") + 1), "08b") == "01001100"  # two's complement distractor
gray = lambda n: n ^ (n >> 1)
assert format(13, "b") == "1101" and format(gray(13), "04b") == "1011"
assert format(gray(11), "04b") == "1110"  # distractor: Gray code of 11

# Pipelining: k stages, n instructions -> k + n - 1 cycles (one cycle per stage, no stalls)
assert 5 + 100 - 1 == 104 and 5 * 100 == 500
# DDR4-3200: 3200 MT/s x 64-bit (8-byte) bus
assert F(3200 * 10**6 * 8, 10**9) == F(256, 10)


# Round Robin, quantum 4, bursts P1=10, P2=4, P3=6, all arrive at 0
def rr_waits(bursts, q):
    rem, t, done, queue = list(bursts), 0, [0] * len(bursts), list(range(len(bursts)))
    while queue:
        i = queue.pop(0)
        run = min(q, rem[i])
        t += run
        rem[i] -= run
        if rem[i]:
            queue.append(i)
        else:
            done[i] = t
    return [done[i] - bursts[i] for i in range(len(bursts))], done


RR_W, RR_DONE = rr_waits([10, 4, 6], 4)
assert RR_W == [10, 4, 12] and RR_DONE == [20, 8, 18]
RR_AVG = F(sum(RR_W), 3)
assert RR_AVG == F(26, 3) and round(float(RR_AVG), 2) == 8.67
assert F(0 + 10 + 14, 3) == 8 and round(float(F(0 + 4 + 10, 3)), 2) == 4.67 and round(46 / 3, 2) == 15.33


# Page replacement, 3 frames
REFS = [2, 5, 2, 8, 6, 5, 2, 8, 6]


def lru_faults(refs, n):
    frames, faults = [], 0
    for p in refs:
        if p in frames:
            frames.remove(p)
        else:
            faults += 1
            if len(frames) == n:
                frames.pop(0)
        frames.append(p)
    return faults


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


assert lru_faults(REFS, 3) == 8 and fifo_faults(REFS, 3) == 5 and optimal_faults(REFS, 3) == 5

# umask 027 on a new regular file (base 666)
assert 0o666 & ~0o027 == 0o640
perm = lambda m: "".join(("r" if m & (4 << s) else "-") + ("w" if m & (2 << s) else "-") +
                         ("x" if m & (1 << s) else "-") for s in (6, 3, 0))
assert perm(0o640) == "rw-r-----" and perm(0o750) == "rwxr-x---" and perm(0o751) == "rwxr-x--x"

# Uncompressed audio: 44.1 kHz, 16-bit, stereo, 60 s
AUDIO = 44100 * 16 * 2 * 60 // 8
assert AUDIO == 10_584_000 and 44100 * 16 * 60 // 8 == 5_292_000 and 44100 * 16 * 2 * 60 == 84_672_000
# Print size
assert F(3000, 300) == 10 and round(2000 / 300, 2) == 6.67
# 1 TB (decimal) shown in binary GB (GiB)
assert round(10**12 / 2**30) == 931 and round(10**12 / (1024 * 10**6)) == 977
# Disk capacity
DISK = 4 * 2 * 2000 * 400 * 512
assert DISK == 3_276_800_000 and DISK // 2 == 1_638_400_000 and DISK * 2 == 6_553_600_000

# Networking
hosts = lambda p: ipaddress.ip_network(f"0.0.0.0/{p}").num_addresses - 2
assert [hosts(p) for p in (22, 23, 24, 25)] == [1022, 510, 254, 126]
assert max(p for p in range(1, 31) if hosts(p) >= 500) == 23
V6 = "2001:0db8:0000:0000:0000:ff00:0042:8329"
assert ipaddress.ip_address(V6).compressed == "2001:db8::ff00:42:8329"
assert ipaddress.ip_address("2001:db8::ff00:0042:8329") == ipaddress.ip_address(V6)  # valid but not canonical
assert ipaddress.ip_address("2001:db8::ff:42:8329") != ipaddress.ip_address(V6)


# Caesar cipher
def caesar(s, k):
    return "".join(chr((ord(c) - 65 + k) % 26 + 65) for c in s)


assert caesar("LOAN", 3) == "ORDQ" and caesar("LOAN", -3) == "ILXK" and caesar("LOAN", 1) == "MPBO"

# SQL
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Txn (txn_id INTEGER, amount INTEGER)")
TXN = [(1, 999), (2, 1000), (3, 2500), (4, None), (5, 5000), (6, 7000)]
db.executemany("INSERT INTO Txn VALUES (?, ?)", TXN)
assert db.execute("SELECT COUNT(*) FROM Txn WHERE amount NOT BETWEEN 1000 AND 5000").fetchone()[0] == 2
assert db.execute("SELECT COUNT(*) FROM Txn WHERE amount BETWEEN 1000 AND 5000").fetchone()[0] == 3

# Excel
LARGE_DATA = [45, 82, 67, 82, 30, 91]
assert sorted(LARGE_DATA, reverse=True)[3 - 1] == 82  # LARGE(A1:A6, 3) counts duplicates separately
assert sorted(set(LARGE_DATA), reverse=True)[3 - 1] == 67
NAMES = ["Asha", "Ravi", "Meena", "John", "Farah"]
BALS = [52000, 87000, 61000, 87500, 43000]
assert NAMES[BALS.index(max(BALS))] == "John"
CIF = [("Pune", 45000), ("Delhi", 72000), ("Pune", 50000), ("Agra", 90000), ("Pune", 81000), ("Delhi", 30000),
       ("Pune", 49999), ("Delhi", 50000)]
assert sum(1 for b, a in CIF if b == "Pune" and a >= 50000) == 2
assert sum(1 for b, a in CIF if b == "Pune" and a > 50000) == 1
assert sum(1 for b, a in CIF if b == "Pune") == 4 and sum(1 for b, a in CIF if a >= 50000) == 5
QTY, RATE = [12, 5, 8], [150, 420, 75]
assert sum(q * r for q, r in zip(QTY, RATE)) == 4500
assert sum(QTY) * sum(RATE) == 16125 and sum(QTY) + sum(RATE) == 670 and max(q * r for q, r in zip(QTY, RATE)) == 2100

# ---------------------------------------------------------------- fact-check sources
# Pages opened on 2026-11-05 (web:fact-check)
MS_WORD = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2"
MS_PPT = ("https://support.microsoft.com/en-us/office/use-keyboard-shortcuts-to-deliver-powerpoint-presentations-"
          "1524ffce-bd2a-45f4-9a7f-f18b992b93a0")
MS_WIN = "https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec"
MDN_COOKIE = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie"
MDN_OVERVIEW = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview"
RFC1035 = "https://www.rfc-editor.org/rfc/rfc1035"
RFC5952 = "https://www.rfc-editor.org/rfc/rfc5952"
RFC6238 = "https://www.rfc-editor.org/rfc/rfc6238"
RFC6376 = "https://www.rfc-editor.org/rfc/rfc6376"
# Confirmed only in search results (web:search-confirmed)
MS_REF = "https://support.microsoft.com/office/how-to-correct-a-ref-error-822c8e46-e610-4d02-bf29-ec4b8c5ff4be"
MS_FREEZE = ("https://support.microsoft.com/en-us/office/freeze-panes-to-lock-rows-and-columns-"
             "dab2ffc9-020d-4026-8121-67dd25f2508f")
MS_EXFAT = "https://learn.microsoft.com/windows/win32/fileio/exfat-specification"
PCI_CVC = "https://blog.pcisecuritystandards.org/faq-can-cvc-be-stored-for-card-on-file-or-recurring-transactions"
UEFI = "https://uefi.org/specs/UEFI/2.11/01_Introduction.html"
SC = "web:search-confirmed"

# ================================================================ 1. Computer Fundamentals (1 / 5 / 1)
T = "Computer Fundamentals"
Q(T, "Generations and history", "Basic",
  "ENIAC, completed in 1945 and one of the earliest general-purpose electronic digital computers, used about "
  "18,000 vacuum tubes. To which generation of computers does it belong?",
  ["First generation", "Second generation", "Third generation", "Fourth generation"],
  concept="Generations of computers",
  explanation="Computers built with vacuum tubes form the first generation (roughly 1940s to mid-1950s). ENIAC is "
              "the best-known example, along with UNIVAC I.",
  steps=["Vacuum tubes = first generation", "ENIAC used vacuum tubes, so it is a first-generation computer"],
  wrong="Second-generation machines used transistors, third-generation used integrated circuits and "
        "fourth-generation use microprocessors.", seconds=20)
o, a = ordered(27, [19, 25, 31], lambda v: format(v, "b"))
Q(T, "Number systems", "Intermediate",
  "What is the result of the binary subtraction 110010 - 10111?", o, a,
  concept="Binary subtraction with borrow",
  explanation="110010 is 50 and 10111 is 23 in decimal. 50 - 23 = 27, and 27 = 16 + 8 + 2 + 1 = 11011 in binary. "
              "Done directly in binary, each borrow from the next column brings in 2 (binary 10).",
  steps=["110010 = 32 + 16 + 2 = 50", "10111 = 16 + 4 + 2 + 1 = 23", "50 - 23 = 27", "27 = 11011"],
  shortcut="Convert both to decimal, subtract, convert back.",
  wrong="10011 = 19, 11001 = 25 and 11111 = 31; each comes from a missed or extra borrow.", seconds=45,
  computed=True)
o, a = ordered(0o144, [0o64, 0o124, 0o154], lambda v: format(v, "o"))
Q(T, "Number systems", "Intermediate",
  "What is the octal (base 8) equivalent of the decimal number 100?", o, a,
  concept="Decimal to octal by repeated division by 8",
  explanation="Divide by 8 and read the remainders from the last to the first: 100 / 8 = 12 r 4, 12 / 8 = 1 r 4, "
              "1 / 8 = 0 r 1. Reading upwards gives 144. Check: 1 x 64 + 4 x 8 + 4 = 100.",
  steps=["100 / 8 = 12 r 4", "12 / 8 = 1 r 4", "1 / 8 = 0 r 1", "Read remainders bottom-up: 144"],
  wrong="64 is 100 written in hexadecimal, not octal (read as octal, 64 is only 52). 124 (octal) = 84 and 154 "
        "(octal) = 108.", seconds=35, computed=True)
Q(T, "Number systems", "Intermediate",
  "What is the one's complement of the 8-bit binary number 10110100?",
  ["01001011", "01001100", "00101101", "10110101"],
  concept="One's complement",
  explanation="The one's complement is formed by inverting every bit: each 1 becomes 0 and each 0 becomes 1. "
              "10110100 becomes 01001011.",
  steps=["Invert each bit of 1 0 1 1 0 1 0 0", "Result: 0 1 0 0 1 0 1 1"],
  shortcut="One's complement = flip every bit; two's complement = one's complement + 1.",
  wrong="01001100 is the two's complement (one's complement + 1). 00101101 is the original bits reversed in order, "
        "not inverted. 10110101 only adds 1 to the original number.", seconds=25, computed=True)
Q(T, "Types of computers", "Intermediate",
  "A hospital ICU machine measures a patient's heartbeat and blood pressure as continuous signals and then converts "
  "them into digital readings that are processed and displayed as numbers. Which type of computer combines both "
  "these features?",
  ["Hybrid computer", "Analog computer", "Digital computer", "Mainframe computer"],
  concept="Analog, digital and hybrid computers",
  explanation="A hybrid computer combines the analog ability to measure continuously varying quantities with the "
              "digital ability to process and display them as exact numbers. ICU monitoring equipment and petrol "
              "pump dispensers are standard examples.",
  steps=["Continuous measurement = analog feature", "Numerical processing and display = digital feature",
         "Both together = hybrid computer"],
  wrong="An analog computer alone does not produce digital processing, and a purely digital computer cannot take "
        "the continuous signal directly. 'Mainframe' describes size and number of users, not the kind of data.",
  seconds=25)
Q(T, "Generations and history", "Intermediate",
  "In which generation of computers did transistors replace vacuum tubes and high-level languages such as FORTRAN "
  "and COBOL come into wide use?",
  ["Second generation", "First generation", "Third generation", "Fifth generation"],
  concept="Generations of computers",
  explanation="The second generation (roughly 1956 to 1963) used transistors, which were smaller, faster, cooler "
              "and more reliable than vacuum tubes. High-level languages such as FORTRAN and COBOL became common "
              "in this period, replacing much machine-language programming.",
  steps=["Transistors = second generation", "FORTRAN and COBOL spread in the same period"],
  wrong="The first generation used vacuum tubes and machine language. The third generation is known for "
        "integrated circuits and the fifth for artificial intelligence.", seconds=20)
o, a = ordered(0b1011, [0b1001, 0b1101, 0b1110], lambda v: format(v, "04b"))
Q(T, "Number systems", "Advanced",
  "In Gray code, consecutive values differ in exactly one bit. A binary number is converted to Gray code by keeping "
  "the most significant bit and then XOR-ing each pair of adjacent bits. What is the Gray code of the decimal number "
  "13?", o, a,
  concept="Binary to Gray code conversion",
  explanation="13 = 1101 in binary. Keep the first bit (1). Then XOR adjacent bits: 1 XOR 1 = 0, 1 XOR 0 = 1, "
              "0 XOR 1 = 1. The Gray code is 1011. Equivalently, Gray = n XOR (n >> 1) = 1101 XOR 0110 = 1011.",
  steps=["13 = 1101", "First bit: 1", "1 XOR 1 = 0", "1 XOR 0 = 1", "0 XOR 1 = 1", "Gray code = 1011"],
  shortcut="Gray = binary XOR (binary shifted right by one place).",
  wrong="1101 is plain binary for 13, not Gray code. 1110 is the Gray code of 11. 1001 comes from XOR-ing the "
        "wrong pairs of bits.", seconds=60, computed=True)

# ================================================================ 2. Hardware (3 / 1 / 3)
T = "Hardware"
Q(T, "Motherboard and ports", "Basic",
  "Which unit inside a desktop cabinet converts the AC mains supply from the wall socket into the low-voltage DC "
  "needed by the motherboard and drives?",
  ["SMPS (power supply unit)", "UPS", "CMOS battery", "Voltage stabiliser"],
  concept="Power supply in a computer",
  explanation="The SMPS (Switched-Mode Power Supply) is the computer's internal power supply unit. It converts AC "
              "mains into regulated DC voltages such as 12 V, 5 V and 3.3 V for the components.",
  steps=["AC from wall -> DC for components = SMPS"],
  wrong="A UPS provides backup power during outages and sits outside the cabinet. The CMOS battery only keeps the "
        "clock and firmware settings. A voltage stabiliser evens out mains voltage but does not convert AC to DC.",
  seconds=20)
Q(T, "CPU and components", "Basic",
  "What is the main purpose of the heat sink and fan fixed on top of a computer's processor?",
  ["To carry heat away from the CPU so it does not overheat", "To increase the CPU's clock speed",
   "To store frequently used data close to the CPU", "To supply electrical power to the CPU"],
  concept="CPU cooling",
  explanation="A processor produces heat while it works. The metal heat sink absorbs this heat and the fan blows it "
              "away. Without cooling, the CPU slows itself down (throttles) or shuts down to avoid damage.",
  steps=["Heat sink + fan = cooling the CPU"],
  wrong="Cooling does not raise the clock speed by itself, caching is the job of cache memory, and power comes "
        "from the power supply through the motherboard.", seconds=15)
Q(T, "Motherboard and ports", "Basic",
  "Which 15-pin, D-shaped port carries only analog video signals and is found on older monitors and projectors?",
  ["VGA", "HDMI", "USB Type-C", "RJ-45"],
  concept="Display ports",
  explanation="VGA (Video Graphics Array) uses a 15-pin D-sub connector and carries analog video only, with no "
              "audio. It is being replaced by digital ports such as HDMI and DisplayPort.",
  steps=["15-pin D-shaped + analog video only = VGA"],
  wrong="HDMI and USB Type-C carry digital signals. RJ-45 is the Ethernet network connector.", seconds=20)
Q(T, "CPU and components", "Intermediate",
  "A processor is described as '64-bit'. This figure refers to its:",
  ["Word size: the number of bits it processes as one unit", "Clock speed in gigahertz",
   "Number of processor cores", "Amount of cache memory in kilobytes"],
  concept="Word size (word length) of a CPU",
  explanation="Word size is the number of bits a CPU handles as one unit in its registers and ALU operations. A "
              "64-bit processor works on 64-bit chunks of data and can use 64-bit memory addresses.",
  steps=["'n-bit processor' = word size of n bits"],
  wrong="Clock speed is measured in GHz, cores are counted separately (dual-core, quad-core) and cache is measured "
        "in KB or MB.", seconds=20)
o, a = ordered(104, [100, 105, 500])
Q(T, "CPU and components", "Advanced",
  "A processor has a 5-stage instruction pipeline, and each stage takes one clock cycle. Ignoring stalls and "
  "hazards, how many clock cycles are needed to complete 100 instructions?", o, a,
  concept="Instruction pipelining",
  explanation="In a k-stage pipeline the first instruction needs k cycles to pass through every stage. After that, "
              "one instruction finishes every cycle. So n instructions need k + (n - 1) cycles: 5 + 99 = 104.",
  steps=["First instruction: 5 cycles", "Each of the remaining 99 instructions: 1 more cycle",
         "Total = 5 + 99 = 104 cycles"],
  shortcut="Pipeline cycles = k + n - 1; without a pipeline = k x n.",
  wrong="100 ignores the cycles needed to fill the pipeline. 105 adds one cycle too many. 500 is the time without "
        "pipelining (5 x 100).", seconds=45, computed=True)
Q(T, "CPU and components", "Advanced",
  "Which of the following is a typical feature of a RISC (Reduced Instruction Set Computer) processor, compared "
  "with a CISC processor?",
  ["Simple fixed-length instructions, most completing in one cycle, with only load and store instructions "
   "accessing memory",
   "Many complex variable-length instructions that can operate directly on memory",
   "Fewer general-purpose registers so that instructions can be longer",
   "Heavy use of microcode to run each complex instruction in many cycles"],
  concept="RISC versus CISC",
  explanation="RISC designs use a small set of simple, fixed-length instructions that pipeline well, usually finish "
              "in one cycle, and follow a load/store design: only load and store touch memory, all other operations "
              "work on registers. ARM processors in phones are RISC; x86 processors are CISC.",
  steps=["RISC = simple, fixed-length, one-cycle instructions", "Load/store architecture with many registers"],
  wrong="Complex variable-length instructions that work directly on memory, and multi-cycle microcoded "
        "instructions, describe CISC. RISC processors usually have more registers, not fewer.", seconds=35)
o, a = ordered(F(256, 10), [F(32, 10), F(128, 10), F(512, 10)], lambda v: f"{float(v):.1f} GB/s")
Q(T, "Motherboard and ports", "Advanced",
  "A DDR4-3200 memory module performs 3,200 million transfers per second on a 64-bit wide memory bus. What is its "
  "peak data transfer rate (1 GB = 10^9 bytes)?", o, a,
  concept="Memory bandwidth = transfer rate x bus width",
  explanation="Each transfer moves 64 bits = 8 bytes. 3,200 x 10^6 transfers per second x 8 bytes = 25,600 x 10^6 "
              "bytes per second = 25.6 GB/s. This is why DDR4-3200 modules are also labelled PC4-25600.",
  steps=["Bus width = 64 bits = 8 bytes", "3,200 x 10^6 x 8 = 25.6 x 10^9 bytes/s", "= 25.6 GB/s"],
  shortcut="MT/s x 8 = MB/s for a 64-bit module (3200 x 8 = 25600).",
  wrong="3.2 GB/s forgets that each transfer carries 8 bytes. 12.8 GB/s halves the rate (the 'double' in DDR is "
        "already inside the 3,200 MT/s figure). 51.2 GB/s doubles it again or assumes two channels.", seconds=50,
  computed=True)

# ================================================================ 3. Software (3 / 5 / 1)
T = "Software"
Q(T, "System and application software", "Basic",
  "Antivirus programs, disk clean-up tools and file-compression tools such as a ZIP utility are classified as:",
  ["Utility software", "Application software", "Programming languages", "Firmware"],
  concept="Types of system software",
  explanation="Utility software is system software that helps maintain, protect and optimise the computer. "
              "Antivirus, backup, disk clean-up and compression tools are utilities.",
  steps=["Maintaining and protecting the system = utility software"],
  wrong="Application software does user tasks such as writing letters or making spreadsheets. Programming languages "
        "are used to write programs. Firmware is software stored permanently in a device's chip.", seconds=20)
Q(T, "System and application software", "Basic",
  "The permanent software stored in a flash or ROM chip of a device such as a router or printer, which controls "
  "the device's basic functions, is called:",
  ["Firmware", "Freeware", "Middleware", "Shareware"],
  concept="Firmware",
  explanation="Firmware is software built into a hardware device's non-volatile chip. It controls the device at a "
              "low level and is changed only by a firmware update. BIOS/UEFI is the firmware of a PC.",
  steps=["Software stored permanently in a device's chip = firmware"],
  wrong="Freeware and shareware are licensing models. Middleware is software that connects applications to each "
        "other or to databases.", seconds=15)
Q(T, "Licensing", "Basic",
  "Software whose author has given up all copyright, so that anyone may use, copy and change it without any "
  "restriction, is called:",
  ["Public domain software", "Proprietary software", "Shareware", "Trial software"],
  concept="Software licensing categories",
  explanation="Public domain software has no copyright owner, so there are no licence conditions at all. Open-source "
              "software, by contrast, is still copyrighted but released under a licence.",
  steps=["No copyright, no restrictions = public domain"],
  wrong="Proprietary software is owned and restricted by its publisher. Shareware and trial software are "
        "copyrighted and must be paid for after a trial.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "An interest-calculation program compiles and runs without any error message, but it prints wrong interest "
  "amounts because the formula multiplies by the rate instead of dividing it by 100. What kind of error is this?",
  ["Logic error", "Syntax error", "Compilation error", "Linker error"],
  concept="Types of programming errors",
  explanation="A logic error lets the program run but makes it produce wrong results because the instructions "
              "themselves are wrong. The compiler cannot detect it; it is found by testing.",
  steps=["Program runs + output wrong = logic error"],
  wrong="Syntax and compilation errors stop the program from compiling. A linker error occurs when a referenced "
        "function or library cannot be found while building the executable.", seconds=25)
Q(T, "Licensing", "Intermediate",
  "While installing a proprietary application, the user must click 'I Agree' to a legal contract stating how the "
  "software may be used. This contract is called the:",
  ["EULA (End User License Agreement)", "GPL (General Public License)", "SLA (Service Level Agreement)",
   "NDA (Non-Disclosure Agreement)"],
  concept="Software licence agreements",
  explanation="The EULA is the agreement between the software publisher and the user. It sets out how many "
              "devices the software may be installed on, and what the user may not do, such as copying or "
              "reverse-engineering it.",
  steps=["Agreement accepted at installation = EULA"],
  wrong="The GPL is an open-source licence. An SLA sets service levels (such as uptime) between a provider and a "
        "client. An NDA is a confidentiality agreement.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "Assembly language, which uses mnemonics such as ADD and MOV, belongs to which generation of programming "
  "languages?",
  ["Second generation (2GL)", "First generation (1GL)", "Third generation (3GL)", "Fourth generation (4GL)"],
  concept="Generations of programming languages",
  explanation="1GL is machine language (binary). 2GL is assembly language with mnemonics. 3GL covers high-level "
              "languages such as C, Java and Python. 4GL covers languages closer to human requests, such as SQL.",
  steps=["Machine code = 1GL", "Assembly (mnemonics) = 2GL"],
  wrong="1GL is pure binary machine code. 3GL and 4GL are high-level languages.", seconds=20)
Q(T, "System and application software", "Intermediate",
  "A bank's data centre runs several operating systems at the same time on one physical server, each in its own "
  "virtual machine. Which software layer makes this possible?",
  ["Hypervisor", "Compiler", "Device driver", "Web browser"],
  concept="Virtualisation",
  explanation="A hypervisor (virtual machine monitor) divides one physical machine's CPU, memory and storage among "
              "several virtual machines, each running its own operating system.",
  steps=["Several OSes on one physical server = virtual machines", "Software managing VMs = hypervisor"],
  wrong="A compiler translates programs, a device driver lets the OS control one piece of hardware, and a browser "
        "displays web pages.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "In an object-oriented program, the balance of an Account object is declared private and can be changed only "
  "through the object's deposit() and withdraw() methods. Which OOP principle does this show?",
  ["Encapsulation", "Inheritance", "Polymorphism", "Compilation"],
  concept="Principles of object-oriented programming",
  explanation="Encapsulation bundles data with the methods that act on it and hides the data from outside code. "
              "Other code cannot set the balance directly; it must go through the controlled methods.",
  steps=["Private data + access only through methods = encapsulation"],
  wrong="Inheritance lets a class reuse another class's members. Polymorphism lets one method name behave "
        "differently for different classes. Compilation is translation, not an OOP principle.", seconds=25)
Q(T, "Programming languages", "Advanced",
  "Which phase of a compiler reads the source program character by character and groups the characters into "
  "tokens such as keywords, identifiers, operators and constants?",
  ["Lexical analysis", "Syntax analysis (parsing)", "Code optimisation", "Code generation"],
  concept="Phases of a compiler",
  explanation="Lexical analysis (scanning) is the first phase. It removes spaces and comments and turns the "
              "character stream into tokens. The parser then checks whether the tokens form valid grammar, and "
              "later phases optimise and generate machine code.",
  steps=["Characters -> tokens = lexical analysis", "Tokens -> parse tree = syntax analysis",
         "Then semantic analysis, optimisation, code generation"],
  wrong="Syntax analysis works on tokens, not characters. Optimisation and code generation come near the end of "
        "compilation.", seconds=30)

# ================================================================ 4. Operating Systems (3 / 2 / 4)
T = "Operating Systems"
Q(T, "Windows and Linux basics", "Basic",
  "In Windows, which keyboard shortcut opens File Explorer?",
  ["Windows logo key + E", "Windows logo key + D", "Windows logo key + I", "Windows logo key + R"],
  concept="Windows keyboard shortcuts",
  explanation="Windows logo key + E opens File Explorer. Windows logo key + D shows or hides the desktop and "
              "Windows logo key + I opens Settings.",
  steps=["Win + E = Explorer"],
  wrong="Win + D shows the desktop, Win + I opens Settings and Win + R opens the Run dialog.", seconds=15,
  facts=[fact("Windows logo key + E opens File Explorer; + D displays and hides the desktop; + I opens Settings.",
              MS_WIN)])
Q(T, "Windows and Linux basics", "Basic",
  "Which Linux command displays the full path of the directory you are currently working in?",
  ["pwd", "cd", "ls", "mkdir"],
  concept="Basic Linux commands",
  explanation="pwd (print working directory) prints the full path of the current directory, for example "
              "/home/asha/reports.",
  steps=["Show current directory path = pwd"],
  wrong="cd changes the directory, ls lists its contents and mkdir creates a new directory.", seconds=15)
Q(T, "Functions", "Basic",
  "An operating system interface in which the user types commands at a prompt, such as the Windows Command Prompt "
  "or a Linux terminal, is called a:",
  ["Command-line interface (CLI)", "Graphical user interface (GUI)", "Touch user interface",
   "Menu-driven interface"],
  concept="User interfaces of an operating system",
  explanation="In a command-line interface the user types text commands and the system replies in text. In a GUI "
              "the user works with windows, icons and menus using a mouse or touch.",
  steps=["Typed commands at a prompt = CLI"],
  wrong="A GUI uses icons and windows, a touch interface uses taps and gestures, and a menu-driven interface lets "
        "the user pick from listed choices.", seconds=15)
Q(T, "Functions", "Intermediate",
  "A computer with too little RAM spends most of its time moving pages between main memory and the disk, so "
  "programs become extremely slow even though the CPU is busy with paging. This condition is called:",
  ["Thrashing", "Deadlock", "Spooling", "Fragmentation"],
  concept="Thrashing in virtual memory",
  explanation="Thrashing happens when processes do not have enough frames for the pages they are actively using. "
              "Page faults become so frequent that the system does more swapping than useful work.",
  steps=["Constant paging + very little useful work = thrashing"],
  wrong="Deadlock is processes waiting for each other's resources. Spooling queues jobs (for example print jobs) on "
        "disk. Fragmentation is wasted or scattered storage space.", seconds=25)
Q(T, "File systems", "Intermediate",
  "Microsoft designed which file system as the successor to FAT32, intended for flash media such as USB drives "
  "and SD cards, and able to store individual files larger than 4 GB?",
  ["exFAT", "FAT16", "ext4", "HFS+"],
  concept="File systems for removable flash media",
  explanation="exFAT (Extended File Allocation Table) succeeds FAT32 in the FAT family. It uses 64 bits to describe "
              "file size, so it removes FAT32's 4 GB per-file limit while staying simple enough for cameras, SD "
              "cards and pen drives.",
  steps=["Successor to FAT32 + flash media + files over 4 GB = exFAT"],
  wrong="FAT16 is older and more limited than FAT32. ext4 is a Linux file system and HFS+ an older Apple file "
        "system; neither was designed by Microsoft.", seconds=25, web=SC,
  facts=[fact("Microsoft's exFAT specification describes exFAT as the successor to FAT32 in the FAT family; exFAT "
              "uses 64 bits to describe file size, lifting FAT32's 4 GB file-size limit.", MS_EXFAT)])
o, a = ordered(RR_AVG, [F(14, 3), F(8), F(46, 3)], lambda v: f"{float(v):.2f} ms")
Q(T, "Functions", "Advanced",
  "Processes P1, P2 and P3 arrive at time 0 in that order with CPU burst times of 10 ms, 4 ms and 6 ms. They are "
  "scheduled by Round Robin with a time quantum of 4 ms. What is the average waiting time?", o, a,
  concept="Round Robin scheduling",
  explanation="Gantt chart: P1 0-4, P2 4-8 (done), P3 8-12, P1 12-16, P3 16-18 (done), P1 18-20 (done). Waiting time "
              "= completion time - burst time: P1 = 20 - 10 = 10, P2 = 8 - 4 = 4, P3 = 18 - 6 = 12. Average = "
              "26 / 3 = 8.67 ms.",
  steps=["P1 0-4, P2 4-8, P3 8-12, P1 12-16, P3 16-18, P1 18-20", "Completion: P1 20, P2 8, P3 18",
         "Waiting: 10, 4, 12", "Average = 26 / 3 = 8.67 ms"],
  shortcut="With all arrivals at 0, waiting time = completion time - burst time.",
  wrong="4.67 ms is the Shortest Job First result, 8.00 ms is FCFS, and 15.33 ms is the average turnaround time, "
        "not the waiting time.", seconds=90, computed=True)
o, a = ordered(lru_faults(REFS, 3), [5, 7, 9])
Q(T, "Functions", "Advanced",
  "A system has 3 page frames, all empty at the start. Using LRU (Least Recently Used) page replacement, how many "
  "page faults occur for the reference string 2, 5, 2, 8, 6, 5, 2, 8, 6?", o, a,
  concept="LRU page replacement",
  explanation="LRU removes the page that has not been used for the longest time. 2 F, 5 F, 2 hit, 8 F (frames 2, "
              "5, 8). 6 F replaces 5 (least recent) -> 2, 8, 6. 5 F replaces 2 -> 8, 6, 5. 2 F replaces 8 -> 6, 5, "
              "2. 8 F replaces 6 -> 5, 2, 8. 6 F replaces 5 -> 2, 8, 6. Total 8 faults.",
  steps=["2 F, 5 F, 2 hit, 8 F", "6 F (out 5), 5 F (out 2), 2 F (out 8)", "8 F (out 6), 6 F (out 5)",
         "Faults = 8"],
  wrong="5 is what FIFO and the Optimal algorithm both give for this string, not LRU. 7 comes from evicting a "
        "wrong page at one step. 9 counts the hit on the third reference (page 2) as a fault.", seconds=90, computed=True)
Q(T, "Functions", "Advanced",
  "Which of the following is NOT one of the four necessary (Coffman) conditions for a deadlock?",
  ["Preemption: the OS can take a resource away from a process holding it", "Mutual exclusion",
   "Hold and wait", "Circular wait"],
  concept="Necessary conditions for deadlock",
  explanation="A deadlock can occur only if all four hold: mutual exclusion, hold and wait, NO preemption and "
              "circular wait. If resources can be preempted, the cycle can be broken, so preemption prevents "
              "deadlock rather than causing it.",
  steps=["Four conditions: mutual exclusion, hold and wait, no preemption, circular wait",
         "Preemption is the opposite of 'no preemption'"],
  wrong="Mutual exclusion, hold and wait and circular wait are all necessary conditions.", seconds=35)
Q(T, "Windows and Linux basics", "Advanced",
  "On a Linux system, new regular files are created with base permissions 666. If the user's umask is 027, what "
  "permissions does a newly created file get?",
  ["rw-r----- (640)", "rwxr-x--- (750)", "rw-rw-r-- (664)", "rwxr-x--x (751)"],
  concept="umask and default file permissions",
  explanation="The umask lists permission bits to remove. 666 with 027 removed: owner 6 - 0 = 6 (rw-), group "
              "6 - 2 = 4 (r--), others 6 - 7 -> 0 (---). Result 640 = rw-r-----.",
  steps=["Base for files = 666 (rw-rw-rw-)", "Remove umask bits 027: 666 AND NOT 027 = 640", "640 = rw-r-----"],
  shortcut="Files: 666 minus umask bits; directories: 777 minus umask bits.",
  wrong="750 (rwxr-x---) is what a new directory gets (777 with 027 removed); regular files never get execute "
        "from the base 666. 664 is the result of umask 002. 751 matches no step of the calculation.", seconds=60,
  computed=True)

# ================================================================ 5. Input and Output Devices (1 / 2 / 3)
T = "Input and Output Devices"
Q(T, "Input devices", "Basic",
  "At a supermarket billing counter, which input device reads the pattern of black and white lines printed on "
  "each product?",
  ["Barcode reader", "MICR reader", "Light pen", "Plotter"],
  concept="Input devices for retail",
  explanation="A barcode reader shines light on the bars and reads the reflected pattern, which encodes the "
              "product number. The billing software then looks up the price.",
  steps=["Black-and-white lines on products = barcode", "Device = barcode reader"],
  wrong="MICR reads magnetic-ink characters on cheques. A light pen points at a screen. A plotter is an output "
        "device.", seconds=15)
Q(T, "Output devices", "Intermediate",
  "Monitors create colours by mixing red, green and blue light. Which colour model do colour printers use when "
  "mixing inks on paper?",
  ["CMYK (cyan, magenta, yellow, black)", "RGB (red, green, blue)", "HSL (hue, saturation, lightness)",
   "YUV (luminance and two colour-difference signals)"],
  concept="Additive and subtractive colour models",
  explanation="Screens emit light, so they use the additive RGB model. Printers put ink on white paper, which "
              "absorbs light, so they use the subtractive CMYK model. Black (K) is added because mixing C, M and Y "
              "does not give a deep black.",
  steps=["Light (screens) = RGB", "Ink (printers) = CMYK"],
  wrong="RGB is the screen model. HSL is a way of describing colours in software, and YUV is used in video "
        "encoding, not in printer inks.", seconds=25)
Q(T, "Input devices", "Intermediate",
  "Which pointing device stays still on the desk while the user moves the pointer by rolling an exposed ball with "
  "the thumb or fingers?",
  ["Trackball", "Joystick", "Touchpad", "Digitiser (graphics tablet)"],
  concept="Pointing devices",
  explanation="A trackball is like an upside-down mouse: the body stays in place and the user rolls the ball on "
              "top. It needs little desk space.",
  steps=["Device fixed + ball rolled by hand = trackball"],
  wrong="A joystick uses a tilting lever, a touchpad senses a finger sliding on a flat surface, and a digitiser "
        "uses a pen on a tablet.", seconds=20)
o, a = ordered(AUDIO, [5_292_000, 1_323_000, 84_672_000], lambda v: f"{v:,} bytes")
Q(T, "Output devices", "Advanced",
  "A one-minute stereo (2-channel) audio clip is recorded without compression at a sampling rate of 44.1 kHz with "
  "16 bits per sample. How much storage does it need?", o, a,
  concept="Size of uncompressed (PCM) audio",
  explanation="Size = sampling rate x bits per sample x channels x seconds / 8. 44,100 x 16 x 2 x 60 = 84,672,000 "
              "bits, and dividing by 8 gives 10,584,000 bytes (about 10.6 MB).",
  steps=["Bits per second = 44,100 x 16 x 2 = 1,411,200", "x 60 s = 84,672,000 bits", "/ 8 = 10,584,000 bytes"],
  wrong="5,292,000 bytes counts only one channel. 1,323,000 bytes divides by 8 twice. 84,672,000 is the size in "
        "bits, not bytes.", seconds=60, computed=True)
Q(T, "Output devices", "Advanced",
  "A digital photo of 3,000 x 2,000 pixels is printed at 300 DPI (dots per inch) with one pixel per dot. What is the "
  "size of the print?",
  ["10 inches x about 6.67 inches", "30 inches x 20 inches", "1 inch x about 0.67 inch", "100 inches x about 66.7 inches"],
  concept="Print size = pixels / DPI",
  explanation="Each inch of paper holds 300 pixels. Width = 3,000 / 300 = 10 inches and height = 2,000 / 300 = "
              "6.67 inches.",
  steps=["Width = 3000 / 300 = 10 in", "Height = 2000 / 300 = 6.67 in"],
  wrong="30 x 20 divides by 100 instead of 300. 1 x 0.67 divides by 3,000. 100 x 66.7 divides by 30.",
  seconds=40, computed=True)
Q(T, "Output devices", "Advanced",
  "Which display technology needs no backlight because each pixel produces its own light, so that black pixels are "
  "completely switched off?",
  ["OLED", "LCD with LED backlight", "CRT", "DLP projector"],
  concept="Display technologies",
  explanation="In an OLED (Organic Light-Emitting Diode) display, every pixel emits light itself. A black pixel is "
              "simply off, which gives very deep blacks and allows thin, flexible screens.",
  steps=["Self-emitting pixels, no backlight = OLED"],
  wrong="An LCD only blocks or passes light from a backlight, so it always needs one. A CRT fires an electron beam "
        "at phosphors from a tube, and a DLP projector reflects a lamp or laser light off tiny mirrors.",
  seconds=30)

# ================================================================ 6. Memory (2 / 5 / 1)
T = "Memory"
Q(T, "Cache and units", "Basic",
  "SRAM is faster and more expensive than DRAM and does not need refreshing. For which purpose is SRAM mainly used "
  "in a computer?",
  ["Cache memory", "Main memory (system RAM sticks)", "Long-term file storage", "Optical discs"],
  concept="SRAM and DRAM",
  explanation="SRAM stores each bit in a flip-flop, so it is fast and needs no refresh, but it takes more space "
              "and costs more. It is therefore used for small, fast caches inside the CPU, while cheaper DRAM is "
              "used for main memory.",
  steps=["Fast + costly + no refresh = SRAM", "Small, fast memory = cache"],
  wrong="Main memory uses DRAM. Long-term storage uses HDDs or SSDs, and optical discs are read by a laser.",
  seconds=20)
Q(T, "Secondary storage", "Basic",
  "A pen drive (USB flash drive) stores data using which technology?",
  ["Flash memory", "Magnetic platters", "Optical laser pits", "Magnetic tape"],
  concept="Storage technologies",
  explanation="A pen drive uses flash memory, a non-volatile semiconductor memory that keeps data without power "
              "and has no moving parts.",
  steps=["Pen drive = flash memory chips"],
  wrong="Magnetic platters are used in hard disks, laser pits in CDs and DVDs, and magnetic tape in tape backups.",
  seconds=15)
o, a = ordered(931, [977, 1000, 1024], lambda v: f"About {v} GB")
Q(T, "Cache and units", "Intermediate",
  "A hard disk is sold as 1 TB, where the manufacturer uses 1 TB = 10^12 bytes. The operating system counts in "
  "binary units (1 GB = 2^30 bytes). About how many GB does the operating system show?", o, a,
  concept="Decimal (SI) and binary storage units",
  explanation="10^12 / 2^30 = 1,000,000,000,000 / 1,073,741,824 = about 931. The disk is not missing space; the two "
              "sides simply use different definitions of a gigabyte.",
  steps=["2^30 = 1,073,741,824", "10^12 / 1,073,741,824 = 931.3", "About 931 GB"],
  wrong="1000 GB uses decimal units on both sides. 1024 GB wrongly assumes 1 TB = 1024 GB in this case. 977 mixes "
        "units (dividing by 1024 x 10^6).", seconds=45, computed=True)
Q(T, "Primary memory", "Intermediate",
  "Which type of ROM is erased by exposing the chip to ultraviolet light through a small quartz window and can "
  "then be reprogrammed?",
  ["EPROM", "EEPROM", "PROM", "Mask ROM"],
  concept="Types of ROM",
  explanation="EPROM (Erasable Programmable ROM) is erased with strong UV light through a window on top of the "
              "chip, then reprogrammed with a special device.",
  steps=["Erased by UV light = EPROM"],
  wrong="EEPROM is erased electrically. PROM can be programmed only once. Mask ROM is written at the factory and "
        "cannot be changed.", seconds=20)
Q(T, "Cache and units", "Intermediate",
  "With a write-through cache policy, what happens when the CPU writes data to a block that is in the cache?",
  ["The data is written to both the cache and main memory at the same time",
   "The data is written only to the cache and copied to main memory when the block is replaced",
   "The data is written only to main memory and the cache block is deleted",
   "The write waits until the cache is completely full"],
  concept="Cache write policies",
  explanation="Write-through updates the cache and main memory together, so memory is always up to date, at the "
              "cost of more memory traffic. Write-back updates only the cache and marks the block 'dirty'; memory "
              "is updated when the block is evicted.",
  steps=["Write-through = cache + memory together", "Write-back = cache now, memory on eviction"],
  wrong="Writing only to the cache until replacement is write-back. Write-through never skips the cache "
        "copy or deletes the block; it updates both. Caches never wait to fill up "
        "before writing.", seconds=30)
Q(T, "Secondary storage", "Intermediate",
  "On a hard disk platter, data is recorded on concentric circles, and each circle is divided into small "
  "arc-shaped units. What are the circles and units called?",
  ["Tracks and sectors", "Sectors and clusters", "Cylinders and pages", "Blocks and frames"],
  concept="Hard disk organisation",
  explanation="Each platter surface has concentric tracks, and each track is divided into sectors, the smallest "
              "unit the disk reads or writes. The same track on all surfaces forms a cylinder.",
  steps=["Concentric circles = tracks", "Divisions of a track = sectors"],
  wrong="A cluster is a group of sectors used by the file system. Pages and frames belong to virtual memory, not "
        "disk geometry.", seconds=20)
Q(T, "Secondary storage", "Intermediate",
  "A server stores identical copies of all data on two disks, so that it keeps working if one disk fails. Which RAID "
  "level is this?",
  ["RAID 1 (mirroring)", "RAID 0 (striping)", "RAID 5 (striping with parity)", "RAID 6 (double parity)"],
  concept="RAID levels",
  explanation="RAID 1 mirrors every write to two (or more) disks. Either disk alone holds the full data, so one "
              "disk failure loses nothing, though only half the raw capacity is usable.",
  steps=["Identical copies on two disks = mirroring = RAID 1"],
  wrong="RAID 0 splits data across disks with no redundancy. RAID 5 needs at least three disks and stores parity, "
        "not full copies. RAID 6 stores two sets of parity across at least four disks.", seconds=25)
o, a = ordered(DISK, [409_600_000, DISK // 2, DISK * 2], lambda v: f"{v:,} bytes")
Q(T, "Secondary storage", "Advanced",
  "A hard disk has 4 platters and both surfaces of each platter store data. Each surface has 2,000 tracks, each "
  "track has 400 sectors, and each sector holds 512 bytes. What is the disk's capacity?", o, a,
  concept="Disk capacity = surfaces x tracks x sectors x bytes per sector",
  explanation="4 platters x 2 surfaces = 8 surfaces. Capacity = 8 x 2,000 x 400 x 512 = 3,276,800,000 bytes "
              "(about 3.28 GB).",
  steps=["Surfaces = 4 x 2 = 8", "8 x 2,000 = 16,000 tracks", "x 400 = 6,400,000 sectors",
         "x 512 = 3,276,800,000 bytes"],
  wrong="409,600,000 bytes counts one surface only. 1,638,400,000 bytes counts one surface per platter. "
        "6,553,600,000 bytes counts 16 surfaces.", seconds=60, computed=True)

# ================================================================ 7. Internet (3 / 1 / 3)
T = "Internet"
Q(T, "Web basics", "Basic",
  "Websites such as Google Search and Bing, which find web pages matching the keywords you type, are called:",
  ["Search engines", "Web browsers", "Web servers", "Operating systems"],
  concept="Search engines and browsers",
  explanation="A search engine indexes web pages and returns the ones that match a query. A browser is the "
              "program you use to open the search engine and other websites.",
  steps=["Find pages for keywords = search engine"],
  wrong="A browser displays pages, a web server hosts them, and an operating system runs the computer.",
  seconds=15)
Q(T, "Email", "Basic",
  "A file, such as a PDF statement, that is sent along with an email message is called a(n):",
  ["Attachment", "Signature", "Subject line", "Inbox"],
  concept="Parts of an email",
  explanation="An attachment is a file sent together with the email, usually shown with a paper-clip icon.",
  steps=["File sent with an email = attachment"],
  wrong="A signature is the text block at the end of a message, the subject line summarises the message and the "
        "inbox is the folder that receives emails.", seconds=10)
Q(T, "Web basics", "Basic",
  "The main or starting page of a website, which usually opens first and links to its other pages, is called the:",
  ["Home page", "Web portal", "Bookmark", "Search bar"],
  concept="Web basics",
  explanation="The home page is the main entry page of a website, for example the page that opens when you type "
              "only the domain name.",
  steps=["Main starting page of a website = home page"],
  wrong="A portal is a website that gathers many services, a bookmark is a saved link in the browser, and the "
        "search bar is where queries are typed.", seconds=10)
Q(T, "Protocols", "Intermediate",
  "Mail servers use DNS to find which server accepts email for a domain such as example.in. Which DNS record type "
  "provides this information?",
  ["MX record", "A record", "CNAME record", "PTR record"],
  concept="DNS record types",
  explanation="An MX (Mail Exchange) record names the host that accepts email for the domain, along with a "
              "preference number used when there are several mail servers.",
  steps=["Mail server for a domain = MX record"],
  wrong="An A record maps a name to an IPv4 address, a CNAME gives an alias for another name, and a PTR record "
        "maps an address back to a name (reverse lookup).", seconds=25,
  facts=[fact("RFC 1035 defines the MX type (value 15) as 'mail exchange' and PTR (value 12) as a domain name "
              "pointer; MX data holds a preference and a host willing to act as mail exchange.", RFC1035)])
Q(T, "Email", "Advanced",
  "A bank adds DKIM to its outgoing email. What does DKIM let a receiving mail server check?",
  ["That the message carries a valid cryptographic signature from the sending domain, using a public key "
   "published in that domain's DNS",
   "That the message has been encrypted so that only the recipient can read it",
   "That the recipient's mailbox has enough free space for the message",
   "That the sender typed a correct password into the bank's webmail"],
  concept="Email authentication: DKIM",
  explanation="DKIM (DomainKeys Identified Mail) lets a domain take responsibility for a message by signing it. "
              "The receiver fetches the public key from the signer's DNS and verifies the signature, which shows "
              "the signed parts were not changed and that the domain vouched for the message. It helps detect "
              "spoofed mail.",
  steps=["Sender's server signs the message with a private key", "Public key published in DNS",
         "Receiver verifies the signature"],
  wrong="DKIM signs messages; it does not encrypt them. It has nothing to do with mailbox space or with the "
        "sender's login password.", seconds=35,
  facts=[fact("RFC 6376: DKIM lets an organisation claim responsibility for a message by associating its domain "
              "with it, validated through a cryptographic signature and a public key retrieved from the signer's "
              "domain.", RFC6376)])
Q(T, "Web basics", "Advanced",
  "A net-banking site sets its session cookie with the HttpOnly attribute. What does this attribute do?",
  ["It stops JavaScript running in the page from reading the cookie, reducing the damage from cross-site scripting",
   "It makes the browser send the cookie only over unencrypted HTTP connections",
   "It deletes the cookie as soon as the page finishes loading",
   "It encrypts the cookie's value with the user's password"],
  concept="Cookie security attributes",
  explanation="HttpOnly forbids scripts from accessing the cookie (for example through document.cookie), though "
              "the browser still sends it with requests. An attacker who injects JavaScript into the page then "
              "cannot simply read and steal the session cookie.",
  steps=["HttpOnly = no access from JavaScript", "Protects session cookies against XSS theft"],
  wrong="Sending a cookie only over HTTPS is the job of the Secure attribute, not HttpOnly, and HttpOnly certainly "
        "does not force plain HTTP. It does not delete or encrypt the cookie.", seconds=35,
  facts=[fact("MDN Set-Cookie: HttpOnly forbids JavaScript from accessing the cookie, for example through "
              "Document.cookie, which mitigates attacks against cross-site scripting.", MDN_COOKIE)])
Q(T, "Protocols", "Advanced",
  "HTTP is described as a 'stateless' protocol. What does this mean?",
  ["Each request is handled independently, with no built-in link to earlier requests; sessions need extra "
   "mechanisms such as cookies",
   "HTTP cannot carry any data from the client to the server",
   "The server never stores any files",
   "The connection is always encrypted, so no state can be seen"],
  concept="Stateless HTTP and sessions",
  explanation="In plain HTTP there is no link between two successive requests, even on the same connection. "
              "Websites add state, such as a login session or a shopping basket, by using cookies in the headers.",
  steps=["Stateless = no memory of earlier requests in the protocol itself", "Cookies add sessions on top"],
  wrong="HTTP does carry data from client to server (for example in a POST body). 'Stateless' says nothing about "
        "storing files or about encryption; encryption comes from HTTPS/TLS.", seconds=30,
  facts=[fact("MDN: HTTP is stateless, with no link between two requests successively carried out on the same "
              "connection; HTTP cookies allow the use of stateful sessions.", MDN_OVERVIEW)])

# ================================================================ 8. Networking (1 / 2 / 2)
T = "Networking"
Q(T, "Devices", "Basic",
  "Which network device receives a weakened signal and regenerates it at full strength, so that a cable can run "
  "beyond its normal maximum distance?",
  ["Repeater", "Router", "Firewall", "Modem"],
  concept="Network devices",
  explanation="A repeater works at the physical layer. It regenerates the signal it receives so the network can "
              "cover a longer distance; it does not read addresses.",
  steps=["Regenerate weak signal to extend distance = repeater"],
  wrong="A router forwards packets between networks using IP addresses, a firewall filters traffic and a modem "
        "converts digital signals for a telephone or cable line.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "Which OSI layer sets up, manages and ends the dialogue (session) between two applications, and can add "
  "checkpoints so that a long transfer resumes from the last checkpoint after a failure?",
  ["Session layer", "Transport layer", "Application layer", "Network layer"],
  concept="OSI layer functions",
  explanation="The session layer (layer 5) handles dialogue control and synchronisation: it opens, manages and "
              "closes sessions and inserts checkpoints for recovery.",
  steps=["Dialogue control + checkpoints = session layer (layer 5)"],
  wrong="The transport layer gives end-to-end delivery and error control. The application layer provides services "
        "to users. The network layer handles logical addressing and routing.", seconds=25)
Q(T, "OSI and TCP/IP", "Intermediate",
  "A computer knows the IPv4 address of another machine on its LAN but needs that machine's MAC address to send it "
  "an Ethernet frame. Which protocol finds the MAC address?",
  ["ARP (Address Resolution Protocol)", "DNS (Domain Name System)", "DHCP (Dynamic Host Configuration Protocol)",
   "ICMP (Internet Control Message Protocol)"],
  concept="Address Resolution Protocol",
  explanation="ARP broadcasts 'who has this IP address?' on the local network, and the owner replies with its MAC "
              "address, which is then cached.",
  steps=["IP address known, MAC needed = ARP"],
  wrong="DNS maps names to IP addresses, DHCP hands out IP addresses, and ICMP carries error and diagnostic "
        "messages such as ping.", seconds=25)
Q(T, "OSI and TCP/IP", "Advanced",
  "A branch LAN must support 500 hosts in one IPv4 subnet. What is the longest prefix (smallest subnet) that "
  "provides at least 500 usable host addresses?",
  ["/23", "/22", "/24", "/25"],
  concept="Sizing a subnet",
  explanation="Usable hosts = 2^(32 - prefix) - 2. A /24 gives 254 (too few). A /23 gives 2^9 - 2 = 510, enough. "
              "A /22 gives 1,022, which also works but is larger than needed.",
  steps=["Need 2^h - 2 >= 500", "h = 9 gives 510", "Prefix = 32 - 9 = /23"],
  shortcut="Find the smallest power of 2 above 501: 512 = 2^9, so the prefix is 32 - 9.",
  wrong="/22 gives 1,022 hosts, not the smallest subnet. /24 gives 254 and /25 gives 126, both too few.",
  seconds=50, computed=True)
Q(T, "OSI and TCP/IP", "Advanced",
  "Following RFC 5952's rules for writing IPv6 addresses as text, what is the canonical form of "
  "2001:0db8:0000:0000:0000:ff00:0042:8329?",
  ["2001:db8::ff00:42:8329", "2001:db8::ff00:0042:8329", "2001:db8::ff:42:8329", "2001:db8:0:0:0:ff00:42:8329"],
  concept="IPv6 address text representation",
  explanation="RFC 5952 requires leading zeros in each 16-bit group to be removed (0db8 -> db8, 0042 -> 42) and the "
              "longest run of all-zero groups to be replaced by '::'. The three zero groups become '::', giving "
              "2001:db8::ff00:42:8329.",
  steps=["Drop leading zeros: 2001:db8:0:0:0:ff00:42:8329", "Replace the run of zero groups with ::",
         "Result: 2001:db8::ff00:42:8329"],
  wrong="2001:db8::ff00:0042:8329 keeps a leading zero, which RFC 5952 forbids. 2001:db8::ff:42:8329 removes "
        "trailing zeros from ff00, which changes the address. 2001:db8:0:0:0:ff00:42:8329 is valid but does not "
        "use '::' as required.", seconds=50, computed=True,
  facts=[fact("RFC 5952: leading zeros MUST be suppressed; '::' MUST be used to its maximum capability on the "
              "longest run of zero fields; hex digits MUST be lowercase.", RFC5952)])

# ================================================================ 9. Cybersecurity (4 / 6 / 4)
T = "Cybersecurity"
Q(T, "Malware", "Basic",
  "Software that keeps showing unwanted pop-up advertisements on a user's computer, often installed bundled with "
  "free programs, is called:",
  ["Adware", "Ransomware", "Firmware", "Worm"],
  concept="Types of malware",
  explanation="Adware displays unwanted advertisements, often bundled with free software, and may also track "
              "browsing to target the ads.",
  steps=["Unwanted ads = adware"],
  wrong="Ransomware locks files for payment, firmware is legitimate device software and a worm spreads itself "
        "across networks.", seconds=15)
Q(T, "Malware", "Basic",
  "A large number of infected computers secretly controlled by an attacker, for example to send spam or flood a "
  "website with traffic, is called a:",
  ["Botnet", "Firewall", "Intranet", "Sandbox"],
  concept="Botnets",
  explanation="A botnet is a network of compromised computers ('bots' or 'zombies') remotely controlled by an "
              "attacker, often used for spam and distributed denial-of-service (DDoS) attacks.",
  steps=["Many infected machines under remote control = botnet"],
  wrong="A firewall filters network traffic, an intranet is an organisation's private network and a sandbox is an "
        "isolated area for safely running untrusted programs.", seconds=15)
Q(T, "Phishing and social engineering", "Basic",
  "An attacker leaves a USB pen drive labelled 'Salary details 2026' in a bank's car park, hoping an employee will "
  "plug it into an office computer. This social-engineering trick is called:",
  ["Baiting", "Vishing", "Pharming", "Shoulder surfing"],
  concept="Social engineering techniques",
  explanation="Baiting lures victims with something tempting, such as an infected pen drive or a free download, so "
              "that they install malware themselves.",
  steps=["Tempting item left to be picked up = baiting"],
  wrong="Vishing uses phone calls, pharming redirects website traffic through DNS tampering, and shoulder surfing "
        "is watching someone type.", seconds=20)
Q(T, "Encryption and authentication", "Basic",
  "Which of these is the strongest password?",
  ["T7#qL!9vR2@m", "password123", "Rahul1990", "12345678"],
  concept="Strong passwords",
  explanation="A strong password is long and mixes upper-case and lower-case letters, digits and symbols, without "
              "dictionary words, names or dates. T7#qL!9vR2@m meets all these conditions.",
  steps=["Long + mixed character types + no words or dates = strong"],
  wrong="password123 and 12345678 are among the most commonly guessed passwords, and Rahul1990 is a name plus a "
        "year, which is easy to guess.", seconds=15)
Q(T, "Phishing and social engineering", "Intermediate",
  "A phishing email aimed specifically at a bank's Chairman and Managing Director, pretending to be a legal notice, "
  "is a type of spear phishing known as:",
  ["Whaling", "Smishing", "Baiting", "Tailgating"],
  concept="Phishing variants",
  explanation="Whaling targets senior executives ('big fish'), whose access and authority make them valuable "
              "targets. The messages are carefully tailored, such as fake legal or regulatory notices.",
  steps=["Phishing aimed at top executives = whaling"],
  wrong="Smishing uses SMS, baiting uses tempting items such as infected pen drives and tailgating is following "
        "someone through a secured door.", seconds=20)
Q(T, "Malware", "Intermediate",
  "Which type of malware hides deep inside the operating system, often with administrator-level access, and "
  "conceals its own files and processes so that ordinary tools cannot detect it?",
  ["Rootkit", "Adware", "Worm", "Spam"],
  concept="Rootkits",
  explanation="A rootkit gives an attacker privileged ('root') control and modifies the operating system to hide "
              "itself and other malware. Removing it often needs special tools or reinstalling the OS.",
  steps=["Hidden in OS + privileged access + conceals itself = rootkit"],
  wrong="Adware shows ads, a worm spreads over networks, and spam is unwanted bulk email, not malware that hides "
        "in the OS.", seconds=25)
Q(T, "Malware", "Intermediate",
  "A dismissed programmer hides code in a payroll system that will delete records on 1 April if his employee ID "
  "is no longer present. Malicious code that waits for a specific date or condition before acting is called a:",
  ["Logic bomb", "Botnet", "Keylogger", "Cookie"],
  concept="Logic bombs",
  explanation="A logic bomb lies dormant inside a legitimate program until a trigger condition, such as a date or "
              "an event, occurs, and then carries out its harmful action.",
  steps=["Dormant code + trigger (date/condition) = logic bomb"],
  wrong="A botnet is a network of infected machines, a keylogger records keystrokes, and a cookie is a small "
        "browser data file.", seconds=25)
Q(T, "Phishing and social engineering", "Intermediate",
  "An unauthorised person follows a bank employee closely through a door that opens only with an access card, "
  "without using a card of his own. This physical social-engineering technique is called:",
  ["Tailgating (piggybacking)", "Pretexting", "Phishing", "Spoofing"],
  concept="Physical social engineering",
  explanation="Tailgating means entering a restricted area by following an authorised person through a secured "
              "entrance. Staff are trained not to hold access-controlled doors for others.",
  steps=["Following someone through a secured door = tailgating"],
  wrong="Pretexting is inventing a false story to get information, phishing uses fake messages and spoofing "
        "fakes an identity such as an email address or caller ID.", seconds=20)
Q(T, "Encryption and authentication", "Intermediate",
  "An authenticator app on a phone shows a 6-digit code that changes every 30 seconds and works even without a "
  "network connection. The code is calculated from a secret shared with the server and the current time. This is "
  "called a:",
  ["TOTP (Time-based One-Time Password)", "Static PIN", "CAPTCHA", "Digital certificate"],
  concept="Time-based one-time passwords",
  explanation="TOTP (RFC 6238) computes a short-lived one-time password from a shared secret key and the current "
              "time, divided into time steps (30 seconds by default). Phone and server calculate the same code "
              "independently, so no network is needed on the phone.",
  steps=["Shared secret + current time -> code", "Changes every time step (default 30 s) = TOTP"],
  wrong="A static PIN never changes. A CAPTCHA tells humans from bots. A digital certificate binds a public key to "
        "an identity; it does not produce changing codes.", seconds=25,
  facts=[fact("RFC 6238 defines TOTP, a time-based variant of the OTP algorithm giving short-lived OTP values; the "
              "time step X has a default value of 30 seconds; K is the shared secret.", RFC6238)])
Q(T, "Malware", "Intermediate",
  "Attackers exploit a security flaw in a widely used application before its vendor knows about it or has released "
  "a patch. Such a flaw is called a:",
  ["Zero-day vulnerability", "Logic bomb", "Firewall rule", "Digital signature"],
  concept="Zero-day vulnerabilities",
  explanation="A zero-day is a vulnerability unknown to the vendor, so defenders have had 'zero days' to fix it. "
              "Attacks using it can succeed even against fully updated systems.",
  steps=["Flaw exploited before vendor knows / patch exists = zero-day"],
  wrong="A logic bomb is planted malicious code with a trigger. A firewall rule and a digital signature are "
        "security controls, not flaws.", seconds=20)
Q(T, "Encryption and authentication", "Advanced",
  "Before storing passwords as hashes, a bank's system adds a random value, unique to each user, to each password. "
  "What is the main benefit of this 'salt'?",
  ["Users with the same password get different hashes, which defeats precomputed (rainbow table) attacks",
   "It lets the bank decrypt the stored password whenever needed",
   "It makes the hash shorter so it needs less storage",
   "It removes the need for users to choose strong passwords"],
  concept="Password salting",
  explanation="A unique salt changes the input to the hash function for each user. Two identical passwords then "
              "produce different hashes, and an attacker cannot use one precomputed table of hashes for every "
              "account but must attack each one separately.",
  steps=["hash(salt + password) stored with the salt", "Same password, different salt -> different hash",
         "Rainbow tables become useless"],
  wrong="Hashes are one-way, so salting does not allow decryption. The hash length is fixed by the algorithm. "
        "Weak passwords can still be guessed one account at a time.", seconds=35)
Q(T, "Encryption and authentication", "Advanced",
  "In a Caesar cipher, each letter is replaced by the letter a fixed number of places later in the alphabet, "
  "wrapping from Z back to A. With a shift of 3, how is the word LOAN encrypted?",
  ["ORDQ", "ILXK", "MPBO", "ORDP"],
  concept="Substitution cipher (Caesar cipher)",
  explanation="Shift each letter 3 places forward: L -> O, O -> R, A -> D, N -> Q. The ciphertext is ORDQ.",
  steps=["L(12) + 3 = O(15)", "O(15) + 3 = R(18)", "A(1) + 3 = D(4)", "N(14) + 3 = Q(17)"],
  wrong="ILXK shifts 3 places backwards (decryption direction). MPBO shifts by only 1. ORDP shifts the last letter "
        "by 2 instead of 3.", seconds=40, computed=True)
Q(T, "Encryption and authentication", "Advanced",
  "What problem does the Diffie-Hellman key exchange solve?",
  ["It lets two parties agree on a shared secret key over an insecure channel without ever sending the key itself",
   "It compresses data before transmission",
   "It proves that a document has not changed by producing a fixed-length hash",
   "It stores passwords safely in a database"],
  concept="Key exchange",
  explanation="In Diffie-Hellman, each side combines its own private value with public values exchanged openly. "
              "Both arrive at the same secret, while an eavesdropper who sees only the public values cannot "
              "feasibly compute it. The shared secret is then used for fast symmetric encryption, as in TLS.",
  steps=["Exchange public values openly", "Each side combines them with its private value",
         "Both get the same shared secret key"],
  wrong="Compression is unrelated to key exchange. Producing a fixed-length digest is what a hash function does. "
        "Password storage uses salted hashing.", seconds=35)
Q(T, "Malware", "Advanced",
  "A virus changes its own code (for example by re-encrypting itself with a new key) every time it infects a new "
  "file, so that no two copies look alike and signature-based antivirus finds it hard to detect. This is a:",
  ["Polymorphic virus", "Boot sector virus", "Macro virus", "Logic bomb"],
  concept="Polymorphic malware",
  explanation="A polymorphic virus mutates its appearance with each infection while keeping the same behaviour. "
              "Because a fixed byte pattern cannot match every copy, defenders rely on behaviour-based and "
              "heuristic detection.",
  steps=["Code changes with each infection to dodge signatures = polymorphic"],
  wrong="A boot sector virus is defined by where it lives (the boot sector). A macro virus spreads through "
        "document macros. A logic bomb waits for a trigger; none of these is defined by changing its code.",
  seconds=30)

# ================================================================ 10. Database Fundamentals (1 / 2 / 1)
T = "Database Fundamentals"
Q(T, "SQL basics", "Basic",
  "Which SQL command adds a new row of data to a table?",
  ["INSERT", "UPDATE", "ALTER", "CREATE"],
  concept="DML commands",
  explanation="INSERT INTO table VALUES (...) adds new rows. UPDATE changes values in existing rows.",
  steps=["Add new row = INSERT"],
  wrong="UPDATE modifies existing rows, ALTER changes a table's structure and CREATE makes a new table or other "
        "object.", seconds=15)
Q(T, "Keys", "Intermediate",
  "In a table Attendance(EmployeeID, Date, Status), neither EmployeeID nor Date alone is unique, but the pair "
  "(EmployeeID, Date) is. A primary key made of two or more columns like this is called a:",
  ["Composite key", "Foreign key", "Alternate key", "Surrogate key"],
  concept="Composite keys",
  explanation="A composite key uses two or more columns together to identify each row uniquely, because no single "
              "column can do it alone.",
  steps=["Two columns together unique = composite key"],
  wrong="A foreign key refers to another table's key. An alternate key is a candidate key not chosen as primary. "
        "A surrogate key is an artificial single column such as an auto-number ID.", seconds=20)
Q(T, "SQL basics", "Intermediate",
  "The SQL commands GRANT and REVOKE, which give and take away users' permissions on database objects, belong to "
  "which category?",
  ["DCL (Data Control Language)", "DDL (Data Definition Language)", "DML (Data Manipulation Language)",
   "TCL (Transaction Control Language)"],
  concept="Categories of SQL commands",
  explanation="DCL commands control access rights: GRANT gives privileges and REVOKE removes them.",
  steps=["Permissions = DCL (GRANT, REVOKE)"],
  wrong="DDL defines structure (CREATE, ALTER, DROP), DML works on data (INSERT, UPDATE, DELETE) and TCL manages "
        "transactions (COMMIT, ROLLBACK).", seconds=20)
o, a = ordered(2, [3, 4, 5])
Q(T, "SQL basics", "Advanced",
  "Table Txn has six rows with these values of amount: 999, 1000, 2500, NULL, 5000, 7000. What does this query "
  "return? SELECT COUNT(*) FROM Txn WHERE amount NOT BETWEEN 1000 AND 5000;", o, a,
  concept="BETWEEN is inclusive; comparisons with NULL are unknown",
  explanation="BETWEEN 1000 AND 5000 includes both end values, so 1000, 2500 and 5000 are inside the range. NOT "
              "BETWEEN keeps 999 and 7000. For the NULL row the condition is UNKNOWN, not TRUE, so WHERE drops it. "
              "The count is 2.",
  steps=["Inside range (inclusive): 1000, 2500, 5000", "NOT BETWEEN: 999, 7000", "NULL -> UNKNOWN -> excluded",
         "COUNT(*) = 2"],
  wrong="3 wrongly counts the NULL row. 4 treats BETWEEN as exclusive (adding 1000 and 5000). 5 makes both "
        "mistakes.", seconds=60, computed=True)

# ================================================================ 11. MS Office (3 / 3 / 4)
T = "MS Office"
Q(T, "Shortcuts", "Basic",
  "In MS Word, which keyboard shortcut inserts a hyperlink?",
  ["Ctrl + K", "Ctrl + H", "Ctrl + L", "Ctrl + Y"],
  concept="Word keyboard shortcuts",
  explanation="Ctrl + K opens the Insert Hyperlink dialog in Word.",
  steps=["Hyperlink = Ctrl + K"],
  wrong="Ctrl + H opens Replace, Ctrl + L left-aligns text and Ctrl + Y redoes or repeats the last action.",
  seconds=15, facts=[fact("Word for Windows: Ctrl+K inserts a hyperlink.", MS_WORD)])
Q(T, "MS Excel", "Basic",
  "Which character is normally typed first to begin a formula in an Excel cell?",
  ["= (equal sign)", "# (hash)", "& (ampersand)", "$ (dollar sign)"],
  concept="Entering formulas in Excel",
  explanation="Excel treats an entry starting with = as a formula, for example =A1+B1. Without it, the entry is "
              "stored as text or a number.",
  steps=["Formulas start with ="],
  wrong="# begins error values such as #REF!, & joins text inside a formula, and $ makes a cell reference "
        "absolute.", seconds=10)
Q(T, "MS PowerPoint", "Basic",
  "In PowerPoint, which shortcut starts the slide show from the CURRENT slide rather than from the first slide?",
  ["Shift + F5", "F5", "Ctrl + F5", "Alt + F4"],
  concept="PowerPoint slide-show shortcuts",
  explanation="Shift + F5 starts the presentation from the slide currently selected. F5 alone starts from the "
              "beginning.",
  steps=["From current slide = Shift + F5"],
  wrong="F5 starts from the first slide. Ctrl + F5 is not the slide-show shortcut, and Alt + F4 closes the "
        "window.", seconds=15,
  facts=[fact("PowerPoint: Shift+F5 starts a presentation from the current slide.", MS_PPT)])
Q(T, "MS Word", "Intermediate",
  "In MS Word, which keyboard shortcut opens the dialog to find a word and replace it with another throughout the "
  "document?",
  ["Ctrl + H", "Ctrl + F", "Ctrl + R", "Ctrl + G"],
  concept="Find and Replace in Word",
  explanation="Ctrl + H opens the Replace dialog box, used to find and replace text, formatting or special items.",
  steps=["Replace = Ctrl + H"],
  wrong="Ctrl + F opens the Navigation pane for finding only, Ctrl + R right-aligns a paragraph and Ctrl + G opens "
        "Go To.", seconds=15,
  facts=[fact("Word for Windows: Ctrl+H displays the Replace dialog box to find and replace text, specific "
              "formatting or special items.", MS_WORD)])
Q(T, "MS Excel", "Intermediate",
  "An Excel sheet has 2,000 rows of customer data. Which feature keeps the heading row visible at the top while "
  "the user scrolls down?",
  ["Freeze Panes", "Sort & Filter", "Wrap Text", "Merge & Center"],
  concept="Freeze Panes",
  explanation="View > Freeze Panes (or Freeze Top Row) locks rows and/or columns so they stay on screen while the "
              "rest of the sheet scrolls.",
  steps=["Keep heading visible while scrolling = Freeze Panes"],
  wrong="Wrap Text shows long text on several lines in a cell, Merge & Center joins cells, and Sort & Filter "
        "reorders or hides rows; none keeps the heading on screen.", seconds=20, web=SC,
  facts=[fact("Excel's Freeze Panes locks rows, columns or both to the top and left of the sheet so they stay "
              "visible while scrolling (View > Freeze Panes).", MS_FREEZE)])
o, a = ordered(82, [45, 67, 91])
Q(T, "MS Excel", "Intermediate",
  "Cells A1 to A6 contain 45, 82, 67, 82, 30 and 91. What does =LARGE(A1:A6, 3) return?", o, a,
  concept="LARGE function with duplicate values",
  explanation="LARGE(range, k) returns the k-th largest value, counting duplicates separately. Sorted from the "
              "top: 91, 82, 82, 67, 45, 30. The third value is 82.",
  steps=["Sort descending: 91, 82, 82, 67, 45, 30", "1st = 91, 2nd = 82, 3rd = 82"],
  wrong="67 would be the answer only if duplicates were counted once. 91 is the largest and 45 the 5th largest.",
  seconds=40, computed=True)
Q(T, "MS Excel", "Advanced",
  "B2:B6 contain the names Asha, Ravi, Meena, John and Farah, and C2:C6 contain their balances 52000, 87000, 61000, "
  "87500 and 43000. What does =INDEX(B2:B6, MATCH(MAX(C2:C6), C2:C6, 0)) return?",
  ["John", "Ravi", "Meena", "Farah"],
  concept="INDEX with MATCH",
  explanation="MAX(C2:C6) = 87500. MATCH(87500, C2:C6, 0) finds its exact position, 4. INDEX(B2:B6, 4) returns the "
              "4th name, John.",
  steps=["MAX = 87500", "MATCH(87500, C2:C6, 0) = 4", "INDEX(B2:B6, 4) = John"],
  wrong="Ravi has 87000, just below the maximum. Meena is the middle row and Farah the last row; neither has the "
        "highest balance.", seconds=60, computed=True)
o, a = ordered(2, [1, 4, 5])
Q(T, "MS Excel", "Advanced",
  "A2:A9 holds branches and B2:B9 amounts: Pune 45000, Delhi 72000, Pune 50000, Agra 90000, Pune 81000, Delhi "
  "30000, Pune 49999, Delhi 50000. What does =COUNTIFS(A2:A9, \"Pune\", B2:B9, \">=50000\") return?", o, a,
  concept="COUNTIFS with several criteria",
  explanation="COUNTIFS counts rows that meet every condition. Pune rows: 45000, 50000, 81000, 49999. Of these, "
              "only 50000 and 81000 are >= 50000, so the result is 2.",
  steps=["Pune rows: 45000, 50000, 81000, 49999", "Of these >= 50000: 50000, 81000", "Count = 2"],
  wrong="1 treats >= as > (dropping 50000). 4 counts all Pune rows. 5 counts all amounts >= 50000 in any branch.",
  seconds=60, computed=True)
o, a = ordered(4500, [670, 2100, 16125])
Q(T, "MS Excel", "Advanced",
  "B2:B4 contain quantities 12, 5 and 8, and C2:C4 contain unit rates 150, 420 and 75. What does "
  "=SUMPRODUCT(B2:B4, C2:C4) return?", o, a,
  concept="SUMPRODUCT",
  explanation="SUMPRODUCT multiplies matching items and adds the products: 12 x 150 + 5 x 420 + 8 x 75 = 1800 + "
              "2100 + 600 = 4500.",
  steps=["12 x 150 = 1800", "5 x 420 = 2100", "8 x 75 = 600", "Sum = 4500"],
  wrong="670 adds all the numbers. 2100 is only the largest single product. 16125 multiplies the two totals "
        "(25 x 645).", seconds=50, computed=True)
Q(T, "MS Excel", "Advanced",
  "Cell D2 contains =SUM(A2,B2,C2). The user then deletes column B. Which error value does the formula now show?",
  ["#REF!", "#VALUE!", "#NAME?", "#DIV/0!"],
  concept="Excel error values",
  explanation="When a cell that a formula refers to explicitly is deleted, the reference is no longer valid and "
              "Excel shows #REF!. Using a range such as =SUM(A2:C2) instead would simply shrink and avoid the error.",
  steps=["Explicit reference to a deleted cell", "Invalid reference = #REF!"],
  wrong="#VALUE! comes from the wrong type of argument, #NAME? from an unrecognised function or name, and "
        "#DIV/0! from dividing by zero.", seconds=30, web=SC,
  facts=[fact("Microsoft: #REF! appears when a formula refers to a cell that is not valid, most often when "
              "referenced cells are deleted; =SUM(B2,C2,D2) returns #REF! if a referenced column is deleted.",
              MS_REF)])

# ================================================================ 12. Digital Payments (1 / 2 / 1)
T = "Digital Payments"
Q(T, "Payment technology", "Basic",
  "At a small shop, a customer pays through UPI by pointing her phone camera at a square printed pattern displayed "
  "at the counter. What is this pattern called?",
  ["QR code", "Barcode", "Hologram", "Watermark"],
  concept="QR-code payments",
  explanation="A QR (Quick Response) code is a two-dimensional code that stores the merchant's payment details. The "
              "UPI app reads it so the customer need not type the payee's address.",
  steps=["Square pattern scanned for UPI = QR code"],
  wrong="A barcode is one-dimensional lines on products. Holograms and watermarks are anti-counterfeiting marks.",
  seconds=15)
Q(T, "Payment technology", "Intermediate",
  "How does a dynamic QR code at a merchant's billing counter differ from a static QR code pasted on the wall?",
  ["It is generated for each transaction and already contains that bill's amount and reference",
   "It can be scanned only by debit cards", "It works without any bank account behind it",
   "It never changes, so it can be printed once and used forever"],
  concept="Static and dynamic QR codes",
  explanation="A static QR code holds only the merchant's details; the customer types the amount. A dynamic QR "
              "code is generated for each sale and carries the amount and a transaction reference, which reduces "
              "errors and makes reconciliation easier.",
  steps=["Static = merchant details only, customer enters amount", "Dynamic = new code per bill with amount"],
  wrong="QR codes are scanned by phone apps, not cards. Every QR payment settles to a bank account. A code that "
        "never changes is a static QR.", seconds=25)
Q(T, "Card security", "Intermediate",
  "Which security standard must merchants, payment processors and banks follow when they store, process or transmit "
  "payment-card data?",
  ["PCI DSS", "ISO 9001", "HTML5", "IEEE 802.11"],
  concept="Card data security standards",
  explanation="PCI DSS (Payment Card Industry Data Security Standard), maintained by the PCI Security Standards "
              "Council, sets requirements for protecting cardholder data, such as encryption, access control and "
              "monitoring.",
  steps=["Card data protection standard = PCI DSS"],
  wrong="ISO 9001 is a quality-management standard, HTML5 is a web markup language and IEEE 802.11 is the Wi-Fi "
        "standard.", seconds=20, web=SC,
  facts=[fact("The PCI Security Standards Council's PCI DSS governs storage of card data; it prohibits storing "
              "card verification codes after authorization.", PCI_CVC)])
Q(T, "Card security", "Advanced",
  "An online shop wants to keep each customer's card verification code (CVV/CVC) on file after the first payment so "
  "that repeat purchases are faster, and customers have agreed. Under PCI DSS, is this allowed?",
  ["No; card verification codes must not be stored after authorization, even if encrypted or if the customer agrees",
   "Yes, if the code is encrypted",
   "Yes, if the customer has given written permission",
   "Yes, but only for recurring payments such as subscriptions"],
  concept="Sensitive authentication data under PCI DSS",
  explanation="The card verification code is sensitive authentication data. PCI DSS forbids storing it after "
              "authorization, even in encrypted form, and customer permission does not change this. It is not "
              "needed for card-on-file or recurring payments, which instead use stored card data or tokens.",
  steps=["CVV/CVC = sensitive authentication data", "Storage after authorization prohibited",
         "Encryption or customer consent does not make it allowed"],
  wrong="Encryption does not lift the ban; customer permission does not lift it; and recurring payments do not "
        "need the code, so storing it for them is also prohibited.", seconds=35, web=SC,
  facts=[fact("PCI SSC FAQ: card verification codes are not needed for card-on-file or recurring transactions and "
              "storing them for these purposes is prohibited, regardless of any permission from the customer; the "
              "ban on storing sensitive authentication data after authorization applies even if it is encrypted.",
              PCI_CVC)])

# ================================================================ 13. Computer Abbreviations (4 / 4 / 2)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic", "What does GUI stand for?",
  ["Graphical User Interface", "General Utility Interface", "Graphical Unit Integration", "Global User Internet"],
  concept="Interface abbreviations",
  explanation="A GUI (Graphical User Interface) lets users work with windows, icons, menus and a pointer instead of "
              "typed commands.", steps=["GUI = Graphical User Interface"],
  wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic", "What is the full form of USB?",
  ["Universal Serial Bus", "Unified System Board", "Universal Storage Block", "United Serial Bridge"],
  concept="Hardware abbreviations",
  explanation="USB (Universal Serial Bus) is the standard port and cable system for connecting peripherals and "
              "charging devices.", steps=["USB = Universal Serial Bus"],
  wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic", "A network connecting the computers inside one bank branch is a LAN. What does LAN stand for?",
  ["Local Area Network", "Large Access Network", "Linked Area Node", "Logical Access Network"],
  concept="Network abbreviations",
  explanation="A LAN (Local Area Network) covers a small area such as an office, branch or building. A WAN (Wide "
              "Area Network) links distant sites.", steps=["LAN = Local Area Network"],
  wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic", "What is the full form of WWW?",
  ["World Wide Web", "World Wide Wire", "Wide World Web", "Web World Wide"],
  concept="Internet abbreviations",
  explanation="WWW (World Wide Web) is the system of linked web pages accessed over the internet with a browser.",
  steps=["WWW = World Wide Web"], wrong="The other expansions are incorrect word orders or made up.", seconds=10)
Q(T, S, "Intermediate", "What does HTTP stand for?",
  ["HyperText Transfer Protocol", "High Transfer Text Protocol", "HyperText Transmission Process",
   "Hyperlink Text Transfer Program"],
  concept="Protocol abbreviations",
  explanation="HTTP (HyperText Transfer Protocol) is the protocol browsers and web servers use to exchange web "
              "pages; HTTPS is its secure version over TLS.", steps=["HTTP = HyperText Transfer Protocol"],
  wrong="The other expansions are made up.", seconds=15)
Q(T, S, "Intermediate", "The company that provides a home or office with its internet connection is called an "
  "ISP. What does ISP stand for?",
  ["Internet Service Provider", "Internal Server Protocol", "Internet Security Program", "Integrated Service Portal"],
  concept="Internet abbreviations",
  explanation="An ISP (Internet Service Provider) gives customers access to the internet through broadband, fibre "
              "or mobile data.", steps=["ISP = Internet Service Provider"],
  wrong="The other expansions are made up.", seconds=15)
Q(T, S, "Intermediate", "Photographs are commonly saved in the JPEG format. What does JPEG stand for?",
  ["Joint Photographic Experts Group", "Joint Picture Encoding Group", "Java Photo Exchange Graphics",
   "Joint Photographic Electronic Graphics"],
  concept="File-format abbreviations",
  explanation="JPEG is named after the Joint Photographic Experts Group, the committee that created this lossy "
              "image-compression standard.", steps=["JPEG = Joint Photographic Experts Group"],
  wrong="The other expansions are made up.", seconds=20)
Q(T, S, "Intermediate", "Internet banking sends a one-time code to the registered mobile number to confirm a "
  "transaction. What does OTP stand for?",
  ["One-Time Password", "Online Transfer Protocol", "Official Transaction PIN", "Open Token Process"],
  concept="Security abbreviations",
  explanation="An OTP (One-Time Password) is valid for only one login or transaction, usually for a short time.",
  steps=["OTP = One-Time Password"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Advanced", "Modern PCs use UEFI firmware instead of the older BIOS. What does UEFI stand for?",
  ["Unified Extensible Firmware Interface", "Universal External Firmware Interface",
   "Unified Embedded File Index", "Universal Extensible Function Integration"],
  concept="Firmware abbreviations",
  explanation="UEFI (Unified Extensible Firmware Interface) is a specification, maintained by the UEFI Forum, for "
              "the interface between the operating system and platform firmware. It replaces the legacy BIOS and "
              "supports features such as Secure Boot.", steps=["UEFI = Unified Extensible Firmware Interface"],
  wrong="The other expansions are made up.", seconds=20, web=SC,
  facts=[fact("The UEFI Forum publishes the Unified Extensible Firmware Interface (UEFI) specification at "
              "uefi.org.", UEFI)])
Q(T, S, "Advanced", "Branches increasingly make phone calls over their data network instead of traditional "
  "telephone lines, using VoIP. What does VoIP stand for?",
  ["Voice over Internet Protocol", "Video over Internet Port", "Voice of Integrated Phones",
   "Virtual Online Internet Phone"],
  concept="Communication abbreviations",
  explanation="VoIP (Voice over Internet Protocol) carries voice calls as data packets over IP networks such as "
              "the internet or a bank's WAN.", steps=["VoIP = Voice over Internet Protocol"],
  wrong="The other expansions are made up.", seconds=20)

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_003_plan.json").read_text(encoding="utf-8"))
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
    "batch_id": "BATCH_003",
    "created_at": TODAY,
    "notes": "BATCH_003 Computer Knowledge part: 100 original questions (BANK_COMP_000203 to BANK_COMP_000302). "
             "Computable answers (binary subtraction, octal, one's complement, Gray code, pipeline cycles, DDR4 "
             "bandwidth, Round Robin, LRU, umask, audio size, print size, TB vs GiB, disk capacity, subnet sizing, "
             "IPv6 compression, Caesar cipher, SQL NOT BETWEEN with NULL via sqlite3, Excel LARGE, INDEX/MATCH, "
             "COUNTIFS, SUMPRODUCT) are re-derived in tools/batch_003/computer.py. Shortcuts and protocol facts were "
             "checked on Microsoft Support, RFC Editor and MDN pages on 2026-11-05; exFAT, Freeze Panes, #REF!, "
             "PCI DSS and UEFI were confirmed from search results only (web:search-confirmed).",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_003_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
