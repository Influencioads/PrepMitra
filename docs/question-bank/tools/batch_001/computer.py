"""Writes batches/parts/BATCH_001_COMP.json: the 100 Computer Knowledge questions of BATCH_001.

Every computable answer (number-system conversions, timing, memory sizes, subnetting, SQL results on a given table,
Excel formula results, chmod permissions) is re-derived below with assertions before the file is written. If any
assertion fails, nothing is written.

    python tools/batch_001/computer.py      (run from docs/question-bank)
"""

import ipaddress
import json
import random
import re
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
FIRST_ID = 3
AI = ("ai:author-solve", "ai:independent-check")
COMPUTED = ("script:recompute", "ai:author-solve", "ai:independent-check")

_rng = random.Random(20261105)
_keys = Counter()
questions = []


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


def Q(topic, subtopic, difficulty, text, options, answer=None, *, concept, explanation, steps, wrong, seconds=30,
      shortcut=None, computed=False, facts=None):
    """Adds one question. With answer=None, options[0] is the correct text and it is placed at the least-used key
    so far (random tie-break, fixed seed). Ordered options (numbers, sequences) pass an explicit answer letter."""
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
    v = {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
         "verified_by": list(COMPUTED if computed else AI), "verified_at": TODAY}
    if facts:
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
assert len("0123456789ABCDEF") == 16
assert bin(45)[2:] == "101101"
assert int("2F", 16) == 47
assert int("1101", 2) + F(1, 2) + F(0, 4) + F(1, 8) == F(13625, 1000)
assert int("157", 8) == 111 and format(111, "X") == "6F"
assert format(-20 & 0xFF, "08b") == "11101100" and format(~20 & 0xFF, "08b") == "11101011"
assert F(1, 25 * 10**8) * 10**9 == F(2, 5)  # 2.5 GHz -> 0.4 ns per cycle
assert 4 * 2 == 8
PERM = {4: "r", 2: "w", 1: "x"}
rwx = lambda d: "".join(PERM[b] if d & b else "-" for b in (4, 2, 1))
assert [rwx(int(c)) for c in "754"] == ["rwx", "r-x", "r--"]
assert 1920 * 1080 * 3 == 6_220_800 and 1920 * 1080 == 2_073_600 and 1920 * 1080 * 4 == 8_294_400
assert 2 * 1024 * 1024 == 2_097_152
assert F(9, 10) * 10 + F(1, 10) * 110 == 20
assert ipaddress.ip_network("10.0.0.0/26").num_addresses - 2 == 62
net27 = ipaddress.ip_interface("192.168.10.77/27").network
assert str(net27.network_address) == "192.168.10.64" and str(net27.broadcast_address) == "192.168.10.95"
assert 6 * 5 // 2 == 15

ACCOUNTS = [(101, "Pune", 72000), (102, "Delhi", 45000), (103, "Pune", 51000), (104, "Delhi", 90000),
            (105, "Agra", 60000), (106, "Delhi", 55000), (107, "Pune", 30000), (108, "Agra", 20000)]
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Accounts (acc_id INTEGER PRIMARY KEY, branch TEXT, balance INTEGER)")
db.executemany("INSERT INTO Accounts VALUES (?, ?, ?)", ACCOUNTS)
SQL = ("SELECT branch, COUNT(*) FROM Accounts WHERE balance > 50000 GROUP BY branch HAVING COUNT(*) >= 2 "
       "ORDER BY branch")
assert db.execute(SQL).fetchall() == [("Delhi", 2), ("Pune", 2)]
SQL2 = "SELECT COUNT(*) FROM Accounts WHERE branch = 'Delhi' OR balance < 40000"
assert db.execute(SQL2).fetchone()[0] == 5  # 102, 104, 106 (Delhi) + 107, 108

SUMIF_DATA = [12, 45, 67, 23, 89]
assert sum(x for x in SUMIF_DATA if x > 40) == 201 and sum(SUMIF_DATA) == 236

VTABLE = {101: ("Asha", 25000), 102: ("Ravi", 40000), 103: ("Meena", 15500), 104: ("John", 32000)}
assert VTABLE[103][1] == 15500


def shift_formula(formula, rows, cols):
    """Copies a formula like Excel does: relative parts of A1-style references move, $-anchored parts stay."""
    def move(m):
        cabs, col, rabs, row = m.groups()
        if not cabs:
            n = 0
            for ch in col:
                n = n * 26 + ord(ch) - 64
            n += cols
            col = ""
            while n:
                n, r = divmod(n - 1, 26)
                col = chr(65 + r) + col
        if not rabs:
            row = str(int(row) + rows)
        return f"{cabs}{col}{rabs}{row}"
    return re.sub(r"(\$?)([A-Z]+)(\$?)(\d+)", move, formula)


assert shift_formula("=A1+$B$1", 2, 1) == "=B3+$B$1"  # C1 -> D3 is 2 rows down, 1 column right
assert shift_formula("=A$1*$C2", 3, 2) == "=C$1*$C5"

# ---------------------------------------------------------------- fact-check sources (pages opened 2026-11-05)
MS_EXCEL = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-9b7213f0040f"
MS_WORD = "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2"
MS_PPT = ("https://support.microsoft.com/en-us/office/use-keyboard-shortcuts-to-deliver-powerpoint-presentations-"
          "1524ffce-bd2a-45f4-9a7f-f18b992b93a0")
MS_WIN = "https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec"
MS_SUMIF = "https://support.microsoft.com/en-us/office/sumif-function-169b8c99-c05c-4483-a712-1697a653039b"

# ================================================================ 1. Computer Fundamentals (3 / 4 / 3)
T = "Computer Fundamentals"
Q(T, "Types of computers", "Basic",
  "A computer that works with continuously varying quantities such as temperature, pressure or voltage, rather "
  "than with discrete digits, is called a(n):",
  ["Analog computer", "Digital computer", "Hybrid computer", "Microcomputer"],
  concept="Analog vs digital vs hybrid computers",
  explanation="An analog computer measures continuously changing physical quantities. A speedometer needle or an "
              "old mercury thermometer works on the same idea. A digital computer works with discrete values "
              "(0 and 1), and a hybrid computer combines both.",
  steps=["Continuous quantities (temperature, voltage) = analog", "Discrete digits = digital",
         "So the answer is analog computer"],
  wrong="A digital computer counts in discrete digits; a hybrid computer mixes analog and digital parts; "
        "'microcomputer' describes size (a PC), not the type of data handled.", seconds=20)
Q(T, "Number systems", "Basic",
  "How many distinct symbols (digits) does the hexadecimal number system use?",
  ["8", "10", "15", "16"], "D",
  concept="Base of a number system",
  explanation="Hexadecimal is base 16. It uses 0 to 9 and then A, B, C, D, E, F for the values 10 to 15, which "
              "makes 16 symbols in all.",
  steps=["Digits 0-9 give 10 symbols", "Letters A-F give 6 more", "10 + 6 = 16"],
  wrong="8 is the base of octal and 10 the base of decimal. 15 is the value of the largest hex digit (F), "
        "but counting 0 there are 16 symbols.", seconds=15, computed=True)
Q(T, "Generations and history", "Basic",
  "Which electronic component was the main switching element in first-generation computers?",
  ["Vacuum tubes", "Transistors", "Integrated circuits", "Microprocessors"],
  concept="Technology used in each computer generation",
  explanation="First-generation computers used vacuum tubes, which were large, consumed a lot of power and "
              "produced a lot of heat. Later generations replaced them with transistors (second), integrated "
              "circuits (third) and microprocessors built with VLSI (fourth).",
  steps=["1st generation: vacuum tubes", "2nd: transistors, 3rd: ICs, 4th: microprocessors"],
  wrong="Transistors, integrated circuits and microprocessors are the defining technologies of the second, third "
        "and fourth generations respectively.", seconds=15)
Q(T, "Number systems", "Intermediate",
  "What is the binary equivalent of the decimal number 45?",
  ["100111", "101011", "101101", "110101"], "C",
  concept="Decimal to binary by repeated division by 2",
  explanation="Divide by 2 repeatedly and read the remainders from bottom to top. 45 = 32 + 8 + 4 + 1, so the bits "
              "for 32, 8, 4 and 1 are 1 and the others are 0: 101101.",
  steps=["45/2 = 22 r1; 22/2 = 11 r0; 11/2 = 5 r1; 5/2 = 2 r1; 2/2 = 1 r0; 1/2 = 0 r1",
         "Read remainders bottom-up: 101101", "Check: 32 + 8 + 4 + 1 = 45"],
  shortcut="Break 45 into powers of 2: 32 + 8 + 4 + 1.",
  wrong="100111 = 39, 101011 = 43 and 110101 = 53.", seconds=40, computed=True)
Q(T, "Number systems", "Intermediate",
  "The hexadecimal number 2F is equal to which decimal number?",
  ["37", "45", "47", "49"], "C",
  concept="Hexadecimal to decimal by place value",
  explanation="Each hex place is a power of 16. 2F = 2 x 16 + F x 1, and F stands for 15, so 2F = 32 + 15 = 47.",
  steps=["2 x 16 = 32", "F = 15, so 15 x 1 = 15", "32 + 15 = 47"],
  wrong="37 is hex 25, 45 is hex 2D and 49 is hex 31; none of them equals 2F.", seconds=30, computed=True)
Q(T, "Types of computers", "Intermediate",
  "A bank's core banking system must serve thousands of branch users at the same time and process millions of "
  "transactions reliably every day. Which type of computer is traditionally used for such work?",
  ["Mainframe computer", "Supercomputer", "Workstation", "Embedded computer"],
  concept="Mainframe vs supercomputer",
  explanation="Mainframes are built for very high transaction volumes, many simultaneous users and high "
              "reliability, which is why banks, insurers and railways use them. Supercomputers are built for raw "
              "calculation speed on scientific problems such as weather forecasting.",
  steps=["Many users + huge transaction volume + reliability", "That is the mainframe's role"],
  wrong="A supercomputer is optimised for complex scientific calculations, not bulk transactions; a workstation is "
        "a powerful single-user computer; an embedded computer is built into a device such as a washing machine.",
  seconds=25)
Q(T, "Generations and history", "Intermediate",
  "Which of the following correctly pairs a computer generation with its main technology?",
  ["Fourth generation - microprocessors built with VLSI", "First generation - integrated circuits",
   "Second generation - vacuum tubes", "Third generation - transistors"],
  concept="Generation-technology pairs",
  explanation="The accepted pairs are: first - vacuum tubes, second - transistors, third - integrated circuits, "
              "fourth - microprocessors (VLSI chips). Only the fourth-generation pair is stated correctly.",
  steps=["1 vacuum tubes, 2 transistors, 3 ICs, 4 microprocessors", "Check each pair against this list"],
  wrong="Integrated circuits belong to the third generation, vacuum tubes to the first and transistors to the "
        "second, so the other three pairs are mismatched.", seconds=30)
Q(T, "Number systems", "Advanced",
  "What is the decimal value of the binary number 1101.101?",
  ["11.625", "13.5", "13.625", "13.75"], "C",
  concept="Binary fractions",
  explanation="Digits left of the point have weights 8, 4, 2, 1; digits right of the point have weights 1/2, 1/4, "
              "1/8. 1101 = 8 + 4 + 1 = 13 and .101 = 1/2 + 1/8 = 0.625, giving 13.625.",
  steps=["Integer part 1101 = 8 + 4 + 0 + 1 = 13", "Fraction .101 = 0.5 + 0 + 0.125 = 0.625", "Total = 13.625"],
  wrong="13.5 ignores the last fractional bit; 13.75 reads .101 as .110; 11.625 misreads the integer part as 1011.",
  seconds=45, computed=True)
Q(T, "Number systems", "Advanced",
  "The octal number 157 is equal to which hexadecimal number?",
  ["6F", "6E", "7F", "9D"], "A",
  concept="Octal to hexadecimal through binary",
  explanation="Write each octal digit as 3 bits: 1 = 001, 5 = 101, 7 = 111, giving 001101111. Regroup into 4-bit "
              "groups from the right: 0110 1111 = 6F. Check in decimal: 1 x 64 + 5 x 8 + 7 = 111 = 6 x 16 + 15.",
  steps=["157 (octal) = 001 101 111 (binary)", "Regroup in fours: 0110 1111", "0110 = 6, 1111 = F, so 6F",
         "Check: 157 octal = 111 decimal = 6F hex"],
  shortcut="Go through binary: 3-bit groups for octal, 4-bit groups for hex.",
  wrong="6E = 110 and 7F = 127 in decimal; 9D = 157 in decimal, which is the result of reading 157 as a decimal "
        "number instead of an octal one.", seconds=60, computed=True)
Q(T, "Number systems", "Advanced",
  "What is the 8-bit two's complement representation of -20?",
  ["10010100", "11101011", "00010100", "11101100"], "D",
  concept="Two's complement of a negative number",
  explanation="Write +20 in 8 bits (00010100), invert every bit to get the one's complement (11101011), then add 1: "
              "11101100. Computers store negative integers this way so that subtraction can be done by addition.",
  steps=["+20 = 00010100", "Invert: 11101011 (one's complement)", "Add 1: 11101100"],
  shortcut="From the right, copy bits up to and including the first 1, then invert the rest: 0001|0100 -> "
           "1110|1100.",
  wrong="10010100 is sign-magnitude form, 11101011 is only the one's complement, and 00010100 is +20.",
  seconds=60, computed=True)

# ================================================================ 2. Hardware (2 / 3 / 2)
T = "Hardware"
Q(T, "CPU and components", "Basic",
  "Which part of the CPU performs arithmetic calculations and logical comparisons?",
  ["Arithmetic Logic Unit (ALU)", "Control Unit (CU)", "Program Counter", "Cache memory"],
  concept="Parts of the CPU",
  explanation="The ALU does arithmetic (add, subtract) and logic (compare, AND, OR). The control unit directs the "
              "flow of instructions and data but does not calculate. For example, checking whether a balance is "
              "greater than a withdrawal amount is a comparison done by the ALU.",
  steps=["Calculations and comparisons = ALU", "Coordination of operations = Control Unit"],
  wrong="The control unit coordinates and directs, the program counter only holds the next instruction's address, "
        "and cache memory stores frequently used data.", seconds=15)
Q(T, "Motherboard and ports", "Basic",
  "Which port is most commonly used today to connect a keyboard, mouse, pen drive and printer to a computer?",
  ["USB", "VGA", "RJ-45", "HDMI"],
  concept="Common computer ports",
  explanation="USB (Universal Serial Bus) is a general-purpose port that connects most peripherals, including "
              "keyboards, mice, pen drives and printers, and can also supply power to them.",
  steps=["General peripherals and storage connect over USB"],
  wrong="VGA and HDMI carry video to a monitor or projector, and RJ-45 is the Ethernet network connector.",
  seconds=15)
Q(T, "CPU and components", "Intermediate",
  "Which CPU register holds the memory address of the next instruction to be fetched?",
  ["Program Counter (PC)", "Instruction Register (IR)", "Accumulator", "Memory Data Register (MDR)"],
  concept="Special-purpose registers",
  explanation="The program counter stores the address of the next instruction. After each fetch it moves on to the "
              "following instruction, unless a jump or branch changes it.",
  steps=["Address of next instruction = Program Counter",
         "Instruction currently being decoded = Instruction Register"],
  wrong="The instruction register holds the current instruction itself, the accumulator holds intermediate ALU "
        "results, and the MDR holds data being read from or written to memory.", seconds=25)
Q(T, "Motherboard and ports", "Intermediate",
  "To connect a desktop to the office wired LAN with an Ethernet cable, which connector is used?",
  ["RJ-45", "RJ-11", "VGA", "PS/2"],
  concept="Network connectors",
  explanation="Ethernet cables (such as Cat5e or Cat6) end in an 8-pin RJ-45 connector, which plugs into the "
              "network port of the computer or switch.",
  steps=["Ethernet = 8-pin RJ-45", "Telephone line = smaller RJ-11"],
  wrong="RJ-11 is the smaller telephone or DSL connector, VGA is an analog video port, and PS/2 is an old "
        "keyboard and mouse port.", seconds=20)
Q(T, "Motherboard and ports", "Intermediate",
  "A desktop shows the wrong date and time every time it is switched on after being unplugged overnight. Which "
  "motherboard component most likely needs to be replaced?",
  ["CMOS battery", "SMPS (power supply unit)", "Heat sink", "RAM module"],
  concept="CMOS battery and the real-time clock",
  explanation="A small coin cell on the motherboard powers the real-time clock and keeps the firmware (BIOS/UEFI) "
              "settings while the computer has no mains power. When this battery is weak, the clock resets "
              "whenever the PC is unplugged.",
  steps=["Clock resets only when mains power is removed", "So the backup power for the clock has failed",
         "That backup is the CMOS battery"],
  wrong="A failed SMPS would stop the PC from starting at all; a heat sink only removes heat from the CPU; "
        "RAM loses its contents at every shutdown anyway and does not keep the clock.", seconds=30)
Q(T, "CPU and components", "Advanced",
  "A processor runs at a clock speed of 2.5 GHz. How long does one clock cycle take?",
  ["0.25 ns", "0.4 ns", "2.5 ns", "4 ns"], "B",
  concept="Clock period = 1 / frequency",
  explanation="2.5 GHz means 2.5 x 10^9 cycles per second. One cycle takes 1 / (2.5 x 10^9) seconds = 0.4 x 10^-9 "
              "seconds = 0.4 nanoseconds.",
  steps=["Period = 1 / f", "1 / (2.5 x 10^9 Hz) = 0.4 x 10^-9 s", "= 0.4 ns"],
  wrong="2.5 ns simply repeats the frequency figure; 4 ns and 0.25 ns come from misplacing the decimal point in "
        "1 / 2.5 = 0.4.", seconds=40, computed=True)
Q(T, "CPU and components", "Advanced",
  "A quad-core Intel processor supports Hyper-Threading, which runs 2 threads on each physical core. How many "
  "logical processors does the operating system see?",
  ["4", "6", "8", "16"], "C",
  concept="Physical cores vs logical processors (simultaneous multithreading)",
  explanation="With Hyper-Threading, each physical core appears to the OS as 2 logical processors. 4 cores x 2 "
              "threads per core = 8 logical processors. Task Manager on such a PC shows 4 cores and 8 logical "
              "processors.",
  steps=["Physical cores = 4", "Threads per core = 2", "Logical processors = 4 x 2 = 8"],
  wrong="4 counts only the physical cores; 16 multiplies by 4 instead of 2; 6 has no basis.", seconds=30,
  computed=True)

# ================================================================ 3. Software (2 / 3 / 2)
T = "Software"
Q(T, "System and application software", "Basic",
  "Which of the following is an example of system software?",
  ["Device driver", "Spreadsheet program", "Media player", "Web browser"],
  concept="System software vs application software",
  explanation="System software runs and manages the computer itself. Examples are the operating system, device "
              "drivers and utilities. A printer driver, for instance, lets the OS talk to the printer. "
              "Application software does a task for the user, such as making a spreadsheet or playing a video.",
  steps=["Manages hardware or the computer = system software", "A device driver controls a hardware device"],
  wrong="Spreadsheet programs, media players and web browsers all do tasks for the user, so they are "
        "application software.", seconds=20)
Q(T, "Licensing", "Basic",
  "Software whose source code is available for anyone to view, modify and redistribute is called:",
  ["Open-source software", "Freeware", "Shareware", "Proprietary software"],
  concept="Software licence types",
  explanation="Open-source software publishes its source code under a licence that allows people to study, change "
              "and share it. Linux and LibreOffice are examples.",
  steps=["Source code open + right to modify and share = open source"],
  wrong="Freeware costs nothing but its source code is usually closed; shareware is a trial version you are "
        "expected to pay for; proprietary software keeps its source code private.", seconds=20)
Q(T, "Programming languages", "Intermediate",
  "Which language translator converts the whole high-level program into machine code before the program runs, "
  "producing a separate executable file?",
  ["Compiler", "Interpreter", "Assembler", "Loader"],
  concept="Compiler vs interpreter vs assembler",
  explanation="A compiler translates the entire source program at once into machine code (for example, a C "
              "program becomes an .exe file). The executable can then run again and again without translating "
              "it each time.",
  steps=["Whole program translated before running = compiler",
         "Line-by-line translation while running = interpreter"],
  wrong="An interpreter translates and runs one statement at a time; an assembler translates assembly language "
        "rather than a high-level language; a loader places a ready program in memory and translates nothing.",
  seconds=25)
Q(T, "Licensing", "Intermediate",
  "A company lets you use its accounting software free for 30 days, after which you must buy a licence to keep "
  "using it. This try-before-you-buy distribution model is commonly called:",
  ["Shareware", "Freeware", "Open-source software", "Public-domain software"],
  concept="Shareware (trialware)",
  explanation="Shareware is distributed free for evaluation, often with a time limit or reduced features, and the "
              "user is expected to pay to continue using it.",
  steps=["Free trial, then payment required = shareware"],
  wrong="Freeware stays free with no time limit; open-source software is defined by access to source code, not a "
        "trial period; public-domain software has no copyright restrictions at all.", seconds=20)
Q(T, "System and application software", "Intermediate",
  "When a computer is switched on, which program loads the operating system from the disk into main memory?",
  ["Bootstrap loader", "Compiler", "Device driver", "Antivirus program"],
  concept="The boot process",
  explanation="On power-on, the firmware (BIOS or UEFI) checks the hardware and runs the bootstrap loader (boot "
              "loader). The boot loader then reads the operating system from the disk into RAM and starts it.",
  steps=["Firmware runs the power-on self-test", "Bootstrap loader loads the OS into RAM", "OS takes over"],
  wrong="A compiler translates source code, a device driver controls one hardware device after the OS is "
        "running, and an antivirus scans for malware; none of them loads the OS.", seconds=25)
Q(T, "Programming languages", "Advanced",
  "Which statement about compilers and interpreters is correct?",
  ["An interpreter translates and executes a program one statement at a time, so execution stops at the first "
   "error it reaches",
   "An interpreter produces a standalone executable file that can run without the interpreter",
   "A compiled program must be translated again every time it is run",
   "A compiler executes each line immediately after translating it"],
  concept="How compilers and interpreters differ",
  explanation="An interpreter reads, translates and runs one statement, then moves to the next. The program can "
              "run partly before it hits an error on a later line. A compiler translates the whole program "
              "first and lists its syntax errors together; once compiled, the executable runs without being "
              "translated again.",
  steps=["Interpreter: statement-by-statement, halts at the first error reached",
         "Compiler: whole program first, executable reused"],
  wrong="Producing a standalone executable is what a compiler does; a compiled program does not need to be "
        "re-translated for every run; running each line right after translating it describes an interpreter.",
  seconds=45)
Q(T, "Licensing", "Advanced",
  "A developer modifies a program licensed under the GNU GPL and distributes the modified version to customers. "
  "What does the GPL require?",
  ["The modified version must also be released under the GPL, with its source code made available to recipients",
   "The source code of the modifications may be kept secret if the binary is sold",
   "A royalty must be paid to the original author for every copy distributed",
   "The software may be distributed only for non-commercial purposes"],
  concept="Copyleft licensing",
  explanation="The GPL is a 'copyleft' licence. Anyone may use, modify, share and even sell GPL software, but a "
              "distributed modified version must carry the same GPL terms and come with (or offer) its source "
              "code, so that the freedoms pass on to every user.",
  steps=["GPL = copyleft", "Derivative work distributed -> same licence + source code available"],
  wrong="Keeping the modified source code secret breaks the copyleft condition. The GPL charges no royalty, and "
        "it allows commercial distribution.", seconds=45,
  facts=[fact("GPLv3 requires conveyed modified versions to be licensed as a whole under the GPL and to provide "
              "corresponding source", "https://www.gnu.org/licenses/gpl-3.0.html")])

# ================================================================ 4. Operating Systems (3 / 3 / 3)
T = "Operating Systems"
Q(T, "Functions", "Basic",
  "Which of the following is NOT a function of an operating system?",
  ["Checking the spelling in a letter", "Memory management", "Process management", "File management"],
  concept="Functions of an operating system",
  explanation="An operating system manages the computer's resources: processes, memory, files, devices and "
              "security. Spell-checking is a feature of an application such as a word processor.",
  steps=["OS functions: process, memory, file, device and security management",
         "Spell-check belongs to an application"],
  wrong="Memory, process and file management are all core jobs of the operating system.", seconds=15)
Q(T, "Windows and Linux basics", "Basic",
  "Which of the following is an open-source operating system?",
  ["Linux", "Microsoft Windows", "Apple macOS", "MS-DOS"],
  concept="Open-source operating systems",
  explanation="The Linux kernel is released under the GNU GPL, and distributions such as Ubuntu and Fedora are "
              "free to use, study and modify. Android is also built on the Linux kernel.",
  steps=["Source code freely available and modifiable = open source", "Linux fits"],
  wrong="Windows, macOS and MS-DOS are proprietary operating systems whose source code is not open for anyone to "
        "modify and redistribute.", seconds=15)
Q(T, "File systems", "Basic",
  "In the Windows path C:\\Users\\Asha\\Reports\\may.xlsx, what is 'Reports'?",
  ["A folder (directory)", "A drive", "A file extension", "A file name"],
  concept="Parts of a file path",
  explanation="In a path, the drive comes first (C:), then folders separated by backslashes, and the file name "
              "with its extension comes last. 'Reports' sits between backslashes before the file name, so it is a "
              "folder.",
  steps=["C: = drive", "Users, Asha, Reports = folders", "may.xlsx = file name with .xlsx extension"],
  wrong="The drive is C:, the extension is .xlsx, and the file name is may.xlsx.", seconds=20)
Q(T, "Functions", "Intermediate",
  "Several programs are ready to run, but the CPU can execute only one at a time on a core. The operating system "
  "decides which program gets the CPU next. This function is called:",
  ["CPU scheduling", "Spooling", "Formatting", "Defragmentation"],
  concept="Process management and scheduling",
  explanation="The OS scheduler picks which ready process runs next and for how long, for example by giving "
              "each process a short turn in rotation (round-robin). Switching quickly between them makes "
              "many programs seem to run at once.",
  steps=["Choosing the next process for the CPU = CPU (process) scheduling"],
  wrong="Spooling queues jobs for slow devices such as printers; formatting prepares a disk; defragmentation "
        "rearranges file pieces on a hard disk.", seconds=25)
Q(T, "Windows and Linux basics", "Intermediate",
  "In Windows, which keyboard shortcut opens Task Manager directly?",
  ["Ctrl + Shift + Esc", "Ctrl + Alt + Tab", "Alt + F4", "Windows logo key + L"],
  concept="Windows keyboard shortcuts",
  explanation="Ctrl + Shift + Esc opens Task Manager directly, where you can see running apps and end a program "
              "that is not responding.",
  steps=["Task Manager = Ctrl + Shift + Esc"],
  wrong="Alt + F4 closes the active window and Windows + L locks the computer. Ctrl + Alt + Tab shows the "
        "open-window switcher, which stays open until you choose a window.", seconds=15,
  facts=[fact("Ctrl+Shift+Esc opens Task Manager; Windows logo key+L locks the PC; Alt+F4 closes the active window",
              MS_WIN)])
Q(T, "Windows and Linux basics", "Intermediate",
  "Which Linux command lists the files and folders in the current directory?",
  ["ls", "pwd", "cd", "rm"],
  concept="Basic Linux commands",
  explanation="ls lists the contents of a directory; for example, ls -l shows details such as size and "
              "permissions.",
  steps=["List contents = ls", "Show current path = pwd", "Change directory = cd", "Remove file = rm"],
  wrong="pwd prints the current directory's path, cd changes the directory, and rm deletes files.", seconds=15)
Q(T, "File systems", "Advanced",
  "A user cannot copy a 6 GB video file to a pen drive, even though the drive has 20 GB free. The drive is "
  "formatted with which file system, the likely cause?",
  ["FAT32", "NTFS", "exFAT", "ext4"],
  concept="File-system limits",
  explanation="FAT32 cannot store a single file of 4 GB or more (its limit is 4 GB minus 1 byte), whatever the free "
              "space. Reformatting the drive as exFAT or NTFS removes this limit.",
  steps=["Free space is enough, so the problem is the per-file size limit", "FAT32 max file size is just under 4 GB",
         "6 GB > 4 GB, so the drive is FAT32"],
  wrong="NTFS, exFAT and ext4 all support individual files far larger than 6 GB.", seconds=40)
Q(T, "Functions", "Advanced",
  "Process P1 holds the printer and waits for the scanner, while process P2 holds the scanner and waits for the "
  "printer. Neither can continue. This situation is called:",
  ["Deadlock", "Thrashing", "Starvation", "Spooling"],
  concept="Deadlock",
  explanation="A deadlock is a circular wait: each process holds a resource the other needs and neither releases "
              "it. Four conditions together cause it: mutual exclusion, hold and wait, no pre-emption and "
              "circular wait.",
  steps=["P1 waits for P2's resource and P2 waits for P1's", "Circular wait with no release = deadlock"],
  wrong="Thrashing is excessive paging when memory is overloaded; starvation is a process waiting indefinitely "
        "because others keep getting priority; spooling is queuing jobs for a device.", seconds=30)
Q(T, "Windows and Linux basics", "Advanced",
  "In Linux, the command chmod 754 report.sh is run. What permissions does the file's group get?",
  ["Read and execute", "Read, write and execute", "Read only", "Write and execute"],
  concept="Octal file permissions",
  explanation="Each digit sets the permissions of owner, group and others in that order, where read = 4, "
              "write = 2 and execute = 1. The group digit is 5 = 4 + 1, which is read and execute (r-x).",
  steps=["754 -> owner 7, group 5, others 4", "5 = 4 (read) + 1 (execute)", "Group: r-x"],
  wrong="Read, write and execute (7) is the owner's permission; read only (4) is what others get; write and "
        "execute would be 3.", seconds=40, computed=True)

# ================================================================ 5. Input and Output Devices (2 / 2 / 2)
T = "Input and Output Devices"
Q(T, "Output devices", "Basic",
  "Which of the following is an output device?",
  ["Plotter", "Scanner", "Joystick", "Light pen"],
  concept="Input vs output devices",
  explanation="A plotter draws large, precise graphics such as engineering drawings and maps on paper, so it "
              "produces output.",
  steps=["Data goes out of the computer to paper = output device"],
  wrong="A scanner, a joystick and a light pen all send data into the computer, so they are input devices.",
  seconds=15)
Q(T, "Input devices", "Basic",
  "Which input technology reads the special magnetic-ink characters printed along the bottom of bank cheques?",
  ["MICR", "OMR", "OCR", "Barcode reader"],
  concept="Magnetic Ink Character Recognition",
  explanation="MICR (Magnetic Ink Character Recognition) reads characters printed with magnetic ink, such as the "
              "cheque number and MICR code on a cheque, so banks can process cheques quickly and securely.",
  steps=["Cheques + magnetic ink = MICR"],
  wrong="OMR reads marks such as darkened bubbles, OCR reads ordinary printed text, and a barcode reader reads "
        "barcodes.", seconds=15)
Q(T, "Input devices", "Intermediate",
  "A recruitment agency must evaluate one lakh answer sheets on which candidates darken bubbles for each answer. "
  "Which input device is best suited for this?",
  ["Optical Mark Reader (OMR)", "MICR reader", "Optical Character Reader (OCR)", "Digitiser (graphics tablet)"],
  concept="Choosing an input device",
  explanation="An OMR detects the presence or absence of pencil or pen marks in fixed positions, which is exactly "
              "how bubble answer sheets are checked in bulk.",
  steps=["Darkened bubbles in fixed positions = marks", "Marks are read by OMR"],
  wrong="MICR needs magnetic ink, OCR recognises the shapes of printed characters, and a digitiser converts "
        "hand-drawn graphics into digital form.", seconds=20)
Q(T, "Output devices", "Intermediate",
  "A branch needs a printer that can print through multi-part carbon forms, producing several copies in one "
  "pass. Which printer should it choose?",
  ["Dot-matrix printer", "Laser printer", "Inkjet printer", "Thermal printer"],
  concept="Impact vs non-impact printers",
  explanation="A dot-matrix printer is an impact printer: its pins strike an inked ribbon against the paper, and "
              "that pressure carries through to the carbon copies underneath.",
  steps=["Multi-part carbon copies need physical impact", "Dot-matrix is an impact printer"],
  wrong="Laser, inkjet and thermal printers are non-impact printers. Nothing strikes the paper, so they cannot "
        "make carbon copies.", seconds=25)
Q(T, "Output devices", "Advanced",
  "An uncompressed image of 1920 x 1080 pixels uses 24-bit colour. How much storage does it need?",
  ["2,073,600 bytes", "6,220,800 bytes", "8,294,400 bytes", "49,766,400 bytes"], "B",
  concept="Image size = pixels x bytes per pixel",
  explanation="24-bit colour uses 24 / 8 = 3 bytes per pixel. The image has 1920 x 1080 = 2,073,600 pixels, so "
              "it needs 2,073,600 x 3 = 6,220,800 bytes (about 5.9 MB).",
  steps=["Pixels = 1920 x 1080 = 2,073,600", "Bytes per pixel = 24 bits / 8 = 3",
         "Size = 2,073,600 x 3 = 6,220,800 bytes"],
  wrong="2,073,600 is just the pixel count (1 byte per pixel); 8,294,400 assumes 32-bit colour (4 bytes); "
        "49,766,400 is the size in bits, not bytes.", seconds=60, computed=True)
Q(T, "Input devices", "Advanced",
  "A customer's phone touchscreen does not respond when she wears ordinary woollen gloves, but works with a bare "
  "finger. Which touchscreen technology does the phone most likely use?",
  ["Capacitive", "Resistive", "Infrared grid", "Optical mark sensing"],
  concept="Touchscreen technologies",
  explanation="A capacitive screen detects the small change in electric charge caused by a conductive object such "
              "as a finger. Insulating gloves block this, so the screen does not respond. A resistive screen "
              "responds to pressure from anything, including gloves and plastic styluses.",
  steps=["Works with a finger, fails with insulating gloves", "So it senses electrical charge = capacitive"],
  wrong="A resistive screen responds to pressure, so it works with gloves. An infrared grid detects any object "
        "that blocks its light beams. Optical mark sensing is how OMR sheets are read and is not a touchscreen "
        "technology.", seconds=40)

# ================================================================ 6. Memory (2 / 3 / 2)
T = "Memory"
Q(T, "Primary memory", "Basic",
  "Which type of memory loses its contents when the power is switched off?",
  ["RAM", "ROM", "Hard disk", "Pen drive"],
  concept="Volatile vs non-volatile memory",
  explanation="RAM is volatile: it holds data only while powered. That is why unsaved work is lost in a power "
              "cut. ROM, hard disks and pen drives keep their data without power.",
  steps=["Volatile = loses data without power", "RAM is volatile"],
  wrong="ROM, hard disks and pen drives are non-volatile and keep data when switched off.", seconds=15)
Q(T, "Cache and units", "Basic",
  "A nibble consists of how many bits?",
  ["2", "4", "8", "16"], "B",
  concept="Units of data",
  explanation="A nibble is half a byte, which is 4 bits. One hexadecimal digit can be stored in exactly one nibble.",
  steps=["1 byte = 8 bits", "Nibble = half a byte = 4 bits"],
  wrong="8 bits make a byte and 16 bits make two bytes; 2 bits has no standard name.", seconds=15)
Q(T, "Cache and units", "Intermediate",
  "Arrange these storage components from SLOWEST to FASTEST access speed.",
  ["Hard disk, RAM, Cache, CPU registers", "RAM, Hard disk, CPU registers, Cache",
   "Cache, RAM, Hard disk, CPU registers", "Hard disk, Cache, RAM, CPU registers"],
  concept="Memory hierarchy",
  explanation="Speed increases (and capacity and cost per byte change) as you move closer to the CPU: secondary "
              "storage (hard disk) is slowest, then main memory (RAM), then cache, and the CPU's own registers "
              "are fastest.",
  steps=["Farthest from CPU: hard disk (slowest)", "Then RAM, then cache", "Inside the CPU: registers (fastest)"],
  wrong="The other orders either put the hard disk faster than RAM or put cache slower than RAM, both of which "
        "reverse the hierarchy.", seconds=30)
Q(T, "Secondary storage", "Intermediate",
  "Which storage device has no moving parts and stores data in flash memory chips?",
  ["Solid State Drive (SSD)", "Hard Disk Drive (HDD)", "Magnetic tape drive", "DVD drive"],
  concept="SSD vs HDD",
  explanation="An SSD stores data in NAND flash chips, so it has no spinning platters or moving heads. This makes "
              "it faster, quieter and more shock-resistant than an HDD.",
  steps=["No moving parts + flash memory = SSD"],
  wrong="An HDD has spinning magnetic platters and a moving head, a tape drive winds magnetic tape, and a DVD "
        "drive spins an optical disc.", seconds=20)
Q(T, "Primary memory", "Intermediate",
  "Which type of RAM must be refreshed thousands of times per second and is commonly used as a computer's main "
  "memory?",
  ["DRAM", "SRAM", "EEPROM", "PROM"],
  concept="DRAM vs SRAM",
  explanation="DRAM stores each bit as charge in a tiny capacitor that leaks, so it must be refreshed constantly. "
              "It is cheap and dense, so it is used for main memory. SRAM uses flip-flops, needs no refresh, and "
              "is faster but costlier, so it is used for cache.",
  steps=["Needs refresh = dynamic RAM", "Main memory = DRAM; cache = SRAM"],
  wrong="SRAM needs no refresh and is used for cache; EEPROM and PROM are types of ROM, not RAM.", seconds=25)
Q(T, "Cache and units", "Advanced",
  "Using binary units (1 KB = 1024 bytes and 1 MB = 1024 KB), how many bytes are there in 2 MB?",
  ["2,000,000", "2,048,000", "2,097,152", "2,147,483,648"], "C",
  concept="Binary storage units",
  explanation="With binary units, 1 MB = 1024 x 1024 = 1,048,576 bytes. So 2 MB = 2 x 1,048,576 = 2,097,152 bytes.",
  steps=["1 MB = 1024 KB = 1024 x 1024 bytes = 1,048,576 bytes", "2 MB = 2,097,152 bytes"],
  wrong="2,000,000 uses decimal units (1 MB = 10^6 bytes), which the question rules out; 2,048,000 mixes 1024 "
        "and 1000; 2,147,483,648 is 2 GB.", seconds=40, computed=True)
Q(T, "Cache and units", "Advanced",
  "A CPU finds the data it needs in cache 90% of the time. A cache hit takes 10 ns. On a miss, the access takes "
  "110 ns in total (cache check plus main memory). What is the average memory access time?",
  ["19 ns", "20 ns", "55 ns", "110 ns"], "B",
  concept="Average access time with a cache hit ratio",
  explanation="Average time = (hit ratio x hit time) + (miss ratio x miss time) = 0.9 x 10 + 0.1 x 110 = 9 + 11 = "
              "20 ns. A high hit ratio keeps the average close to cache speed even though main memory is much "
              "slower.",
  steps=["Hits: 0.9 x 10 = 9 ns", "Misses: 0.1 x 110 = 11 ns", "Average = 9 + 11 = 20 ns"],
  wrong="19 ns uses 100 ns for a miss, but the question says a miss takes 110 ns in total; 55 ns is a simple "
        "average of 10 and 100; 110 ns is the miss time alone.", seconds=60, computed=True)

# ================================================================ 7. Internet (2 / 3 / 2)
T = "Internet"
Q(T, "Web basics", "Basic",
  "What does URL stand for?",
  ["Uniform Resource Locator", "Universal Routing Link", "Uniform Remote Login", "Universal Resource Library"],
  concept="Web addresses",
  explanation="A URL (Uniform Resource Locator) is the address of a resource on the web, such as "
              "https://www.example.com/index.html. It names the protocol, the host and the path.",
  steps=["URL = Uniform Resource Locator"],
  wrong="The other expansions are made up; none of them is a recognised term.", seconds=15)
Q(T, "Email", "Basic",
  "While sending an email, which field adds recipients whose addresses are hidden from all other recipients?",
  ["Bcc", "Cc", "To", "Subject"],
  concept="To, Cc and Bcc",
  explanation="Bcc (blind carbon copy) recipients get the email, but their addresses are not shown to anyone "
              "else. It is useful when writing to many customers who should not see each other's addresses.",
  steps=["Hidden copy = Blind carbon copy = Bcc"],
  wrong="Addresses in To and Cc are visible to every recipient, and Subject is the title of the email, not a "
        "recipient field.", seconds=15)
Q(T, "Protocols", "Intermediate",
  "Priya reads her office email on both her phone and her laptop and wants messages to stay on the server, with "
  "folders and read/unread status the same on both devices. Which protocol should her email app use to receive "
  "mail?",
  ["IMAP", "POP3", "SMTP", "FTP"],
  concept="IMAP vs POP3",
  explanation="IMAP keeps mail on the server and syncs folders and message status across every device. POP3 "
              "usually downloads mail to one device and often removes it from the server.",
  steps=["Several devices + mail kept on server + sync = IMAP"],
  wrong="POP3 is built for downloading to a single device; SMTP sends mail rather than receiving it; FTP transfers "
        "files.", seconds=25)
Q(T, "Web basics", "Intermediate",
  "In the address https://www.example.co.in/loans/home.html, what is the top-level domain (TLD)?",
  [".in", ".co", "example", "https"],
  concept="Parts of a domain name",
  explanation="A domain name is read from right to left. The last label, 'in', is the top-level domain, here a "
              "country-code TLD for India. 'co' is a second-level label under .in, and 'example' is the "
              "registered name.",
  steps=["Host: www.example.co.in", "Rightmost label = TLD = .in"],
  wrong="'.co' is a second-level label under .in; 'example' is the organisation's chosen name; 'https' is the "
        "protocol (scheme), not part of the domain.", seconds=25)
Q(T, "Protocols", "Intermediate",
  "When you type www.example.com into a browser, which service finds the IP address of that website's server?",
  ["DNS", "DHCP", "ARP", "FTP"],
  concept="Domain Name System",
  explanation="DNS works like the internet's phone book: it translates human-friendly domain names into the IP "
              "addresses that computers use to connect.",
  steps=["Domain name -> IP address = DNS"],
  wrong="DHCP gives a device its own IP address on a network, ARP finds the MAC address for a known IP address on "
        "the local network, and FTP transfers files.", seconds=20)
Q(T, "Protocols", "Advanced",
  "A secure banking website is opened with https:// and no port number is given. Which default TCP port does "
  "the browser connect to?",
  ["443", "80", "21", "25"],
  concept="Well-known port numbers",
  explanation="HTTPS (HTTP over TLS) uses TCP port 443 by default, while plain HTTP uses port 80.",
  steps=["https:// with no port -> 443", "http:// with no port -> 80"],
  wrong="Port 80 is plain HTTP, port 21 is FTP control and port 25 is SMTP.", seconds=20,
  facts=[fact("If no port is given, TCP port 443 is the default for the https scheme",
              "https://www.rfc-editor.org/rfc/rfc9110.html")])
Q(T, "Web basics", "Advanced",
  "A customer clicks an old link and the server responds with HTTP status code 404. What does this mean?",
  ["The server could not find the requested resource", "The server hit an internal error",
   "The client is not permitted to access the resource", "The resource has moved permanently to a new URL"],
  concept="HTTP status codes",
  explanation="404 Not Found means the server is reachable, but the page or resource at that address does not "
              "exist, often because the page was deleted or renamed. 4xx codes are client-side errors, and 5xx "
              "codes are server-side errors.",
  steps=["404 = Not Found", "403 = Forbidden, 500 = Internal Server Error, 301 = Moved Permanently"],
  wrong="An internal server error is 500, access forbidden is 403, and moved permanently is 301.", seconds=25)

# ================================================================ 8. Networking (3 / 4 / 3)
T = "Networking"
Q(T, "Topologies", "Basic",
  "In which network topology are all computers connected to a single central device such as a hub or switch?",
  ["Star", "Bus", "Ring", "Mesh"],
  concept="Network topologies",
  explanation="In a star topology every node has its own cable to a central hub or switch. A typical office LAN "
              "is wired this way: if one cable fails, only that computer is affected.",
  steps=["Central device with separate links = star"],
  wrong="A bus topology shares one backbone cable, a ring connects each node to two neighbours in a loop, and a "
        "mesh links nodes directly to many or all other nodes.", seconds=15)
Q(T, "OSI and TCP/IP", "Basic",
  "How many layers does the OSI reference model have?",
  ["4", "5", "6", "7"], "D",
  concept="OSI model",
  explanation="The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation and "
              "Application. The TCP/IP model is usually described with 4 layers.",
  steps=["Physical, Data Link, Network, Transport, Session, Presentation, Application = 7"],
  wrong="4 is the usual count for the TCP/IP model; 5 and 6 are not OSI layer counts.", seconds=15)
Q(T, "Devices", "Basic",
  "Which device converts a computer's digital signals into analog signals for a telephone line, and back again?",
  ["Modem", "Router", "Repeater", "Hub"],
  concept="Modem = modulator-demodulator",
  explanation="A modem modulates digital data into analog signals for transmission and demodulates incoming "
              "analog signals back into digital data, as in dial-up and DSL internet connections.",
  steps=["Digital <-> analog conversion = modulation/demodulation = modem"],
  wrong="A router forwards packets between networks, a repeater regenerates a weakening signal, and a hub copies "
        "data to all its ports. None of them converts between digital and analog.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "At which OSI layer does a router mainly operate when it forwards packets using IP addresses?",
  ["Network layer", "Data link layer", "Transport layer", "Physical layer"],
  concept="Devices and OSI layers",
  explanation="Routers read the destination IP address and choose a path between networks. Logical addressing "
              "and routing are jobs of the network layer (layer 3).",
  steps=["IP addressing and routing = layer 3 = network layer"],
  wrong="Switches work mainly at the data link layer using MAC addresses, the transport layer handles end-to-end "
        "delivery (TCP/UDP), and hubs and repeaters work at the physical layer.", seconds=20)
Q(T, "Devices", "Intermediate",
  "Which device learns MAC addresses and sends a frame only to the port of the destination computer, instead of "
  "to every port?",
  ["Switch", "Hub", "Repeater", "Modem"],
  concept="Switch vs hub",
  explanation="A switch builds a table of which MAC address sits on which port and forwards each frame only where "
              "it needs to go. This cuts unnecessary traffic and collisions.",
  steps=["Uses MAC addresses + selective forwarding = switch"],
  wrong="A hub repeats every frame to all ports, a repeater only regenerates the signal, and a modem converts "
        "between digital and analog signals.", seconds=20)
Q(T, "Topologies", "Intermediate",
  "A bank wants a network in which every branch server has a direct link to every other branch server, so that "
  "traffic can be rerouted if any link fails. Which topology meets this need?",
  ["Full mesh", "Bus", "Ring", "Star"],
  concept="Mesh topology and redundancy",
  explanation="In a full mesh each node is directly connected to every other node. There are many alternative "
              "paths, so the network keeps working even if a link fails, but it needs a lot of cabling.",
  steps=["Direct link between every pair = full mesh", "Many alternative paths = high redundancy"],
  wrong="In a bus, a break in the backbone disrupts the network. In a ring, one break can stop or isolate traffic. "
        "In a star, everything depends on the central device.", seconds=25)
Q(T, "OSI and TCP/IP", "Intermediate",
  "Which transport-layer protocol is connectionless, does not guarantee delivery, and is therefore preferred for "
  "live video calls where speed matters more than resending lost data?",
  ["UDP", "TCP", "ARP", "ICMP"],
  concept="TCP vs UDP",
  explanation="UDP sends datagrams without setting up a connection and without acknowledgements, so it has low "
              "delay. A lost video frame is simply skipped. TCP is connection-oriented and resends lost data, "
              "which suits file transfer and web pages.",
  steps=["Connectionless + no delivery guarantee + low delay = UDP"],
  wrong="TCP is connection-oriented and reliable; ARP resolves IP addresses to MAC addresses and ICMP carries error "
        "and diagnostic messages (as in ping). Neither ARP nor ICMP is a transport protocol.", seconds=25)
Q(T, "OSI and TCP/IP", "Advanced",
  "How many usable host addresses does an IPv4 subnet with prefix /26 provide?",
  ["30", "62", "64", "126"], "B",
  concept="Hosts per subnet = 2^(host bits) - 2",
  explanation="/26 leaves 32 - 26 = 6 host bits, giving 2^6 = 64 addresses. The first is the network address and "
              "the last is the broadcast address, so 64 - 2 = 62 can be assigned to hosts.",
  steps=["Host bits = 32 - 26 = 6", "Total addresses = 2^6 = 64", "Usable = 64 - 2 = 62"],
  wrong="30 is for /27, 126 is for /25, and 64 forgets to subtract the network and broadcast addresses.",
  seconds=45, computed=True)
Q(T, "OSI and TCP/IP", "Advanced",
  "A host has the IP address 192.168.10.77 with prefix /27. What is the network address of its subnet?",
  ["192.168.10.32", "192.168.10.64", "192.168.10.77", "192.168.10.96"], "B",
  concept="Finding the network address from a prefix",
  explanation="/27 means a subnet mask of 255.255.255.224, so subnets go up in blocks of 32 in the last octet: "
              "0, 32, 64, 96, and so on. 77 falls in the block 64 to 95. The network address is 192.168.10.64 "
              "and the broadcast address is 192.168.10.95.",
  steps=["Block size = 256 - 224 = 32", "Blocks: 0-31, 32-63, 64-95, ...", "77 is in 64-95 -> network .64"],
  wrong="192.168.10.32 is the previous subnet, 192.168.10.96 is the next subnet, and 192.168.10.77 is the host's "
        "own address.", seconds=60, computed=True)
Q(T, "Topologies", "Advanced",
  "How many point-to-point links are needed to connect 6 devices in a full mesh topology?",
  ["12", "15", "30", "36"], "B",
  concept="Links in a full mesh = n(n - 1) / 2",
  explanation="Each of the 6 devices connects to the other 5, giving 6 x 5 = 30 connection ends. Every link joins "
              "two devices, so it has been counted twice: 30 / 2 = 15 links.",
  steps=["n = 6", "n(n - 1) / 2 = 6 x 5 / 2 = 15"],
  wrong="30 counts each link twice; 36 is n squared; 12 has no basis in the formula.", seconds=40,
  computed=True)

# ================================================================ 9. Cybersecurity (3 / 4 / 3)
T = "Cybersecurity"
Q(T, "Malware", "Basic",
  "Which type of malware attaches itself to a host program or file and spreads when that infected program is run?",
  ["Virus", "Worm", "Spyware", "Adware"],
  concept="Virus vs worm",
  explanation="A computer virus needs a host file and spreads only when the user runs the infected program or "
              "opens the file. A worm, by contrast, copies itself across networks on its own.",
  steps=["Needs a host program + spreads when run = virus"],
  wrong="A worm spreads by itself without a host file, spyware secretly collects information, and adware shows "
        "unwanted advertisements.", seconds=20)
Q(T, "Phishing and social engineering", "Basic",
  "An email that pretends to come from a customer's bank and asks him to click a link and enter his net-banking "
  "password is an example of:",
  ["Phishing", "Pharming", "Keylogging", "Cryptojacking"],
  concept="Phishing",
  explanation="Phishing uses fake messages, usually emails, that copy a trusted organisation to trick people into "
              "revealing passwords, card numbers or OTPs. A bank never asks for your password by email.",
  steps=["Fake email + link + asks for credentials = phishing"],
  wrong="Pharming redirects users to a fake site by tampering with DNS or the hosts file, without a bait link; "
        "keylogging records keystrokes with hidden software or hardware; cryptojacking secretly uses a victim's "
        "computer to mine cryptocurrency.", seconds=20)
Q(T, "Phishing and social engineering", "Basic",
  "A fraudster telephones a customer, pretends to be from the bank and asks for the OTP he has just received. This "
  "type of attack is called:",
  ["Vishing", "Smishing", "Whaling", "Spamming"],
  concept="Types of phishing by channel",
  explanation="Vishing is voice phishing: the fraud happens over a phone call. No genuine bank official will ever "
              "ask for an OTP, PIN or CVV.",
  steps=["Phone call = voice = vishing"],
  wrong="Smishing uses SMS, whaling targets senior executives, and spamming is sending bulk unsolicited messages.",
  seconds=15)
Q(T, "Malware", "Intermediate",
  "A branch's computers suddenly show a message that all files have been encrypted and will be unlocked only after "
  "payment in cryptocurrency. Which type of malware is this?",
  ["Ransomware", "Rootkit", "Adware", "Spyware"],
  concept="Ransomware",
  explanation="Ransomware encrypts the victim's files (or locks the system) and demands a ransom for the "
              "decryption key. Regular offline backups are the main defence.",
  steps=["Files encrypted + payment demanded = ransomware"],
  wrong="A rootkit hides malicious activity deep in the system, adware shows advertisements, and spyware secretly "
        "gathers information; none of them demands a ransom.", seconds=20)
Q(T, "Phishing and social engineering", "Intermediate",
  "A customer receives an SMS: 'Your KYC expires today. Update now at this link or your account will be blocked.' "
  "This is an example of:",
  ["Smishing", "Vishing", "Whaling", "Baiting"],
  concept="SMS phishing",
  explanation="Smishing is phishing by SMS (text message). It uses urgency and a fake link to steal details. The "
              "safe response is to ignore the link and contact the bank through its official channels.",
  steps=["Delivered by SMS + fake link + urgency = smishing"],
  wrong="Vishing uses voice calls, whaling targets top executives, and baiting leaves tempting bait such as an "
        "infected pen drive.", seconds=20)
Q(T, "Encryption and authentication", "Intermediate",
  "Logging in to internet banking with a password and then entering an OTP sent to the registered mobile number "
  "is an example of:",
  ["Two-factor authentication", "Single sign-on", "Biometric-only authentication", "CAPTCHA verification"],
  concept="Multi-factor authentication",
  explanation="Two-factor authentication combines two different kinds of factor: something you know (the "
              "password) and something you have (the phone that receives the OTP). A thief who steals only the "
              "password still cannot log in.",
  steps=["Password = something you know", "OTP on phone = something you have", "Two factor types = 2FA"],
  wrong="Single sign-on lets one login work across many services; biometric-only uses just a fingerprint or face; "
        "CAPTCHA checks that the user is human, not who the user is.", seconds=20)
Q(T, "Malware", "Intermediate",
  "A user downloads a 'free game' that works normally but secretly opens a backdoor so that an attacker can "
  "control the computer. This malware is a:",
  ["Trojan horse", "Worm", "Logic bomb", "Adware"],
  concept="Trojan horse",
  explanation="A Trojan horse looks like useful or harmless software but carries a hidden malicious payload, such "
              "as a backdoor. Unlike a virus or worm, it does not replicate itself.",
  steps=["Disguised as useful software + hidden harmful function = Trojan"],
  wrong="A worm replicates across networks on its own, a logic bomb triggers when a set condition such as a date "
        "is met, and adware displays advertisements.", seconds=20)
Q(T, "Encryption and authentication", "Advanced",
  "Meera wants to send a confidential file to Ravi using public-key (asymmetric) encryption, so that only Ravi can "
  "read it. Which key should Meera use to encrypt the file?",
  ["Ravi's public key", "Ravi's private key", "Meera's private key", "Meera's public key"],
  concept="Asymmetric encryption for confidentiality",
  explanation="Encrypt with the receiver's public key; only the matching private key can decrypt. Anyone can "
              "have Ravi's public key, but only Ravi holds his private key, so only he can read the file.",
  steps=["Confidentiality: encrypt with the receiver's public key", "Receiver decrypts with own private key"],
  wrong="Meera never has Ravi's private key. Encrypting with Meera's private key lets anyone with her public key "
        "decrypt it, which proves who sent it but keeps nothing secret. Encrypting with Meera's public key means "
        "only Meera could decrypt it.", seconds=45)
Q(T, "Encryption and authentication", "Advanced",
  "A digital signature lets a receiver confirm who sent a document and that it was not altered. Which key does the "
  "sender use to create the signature?",
  ["The sender's private key", "The sender's public key", "The receiver's public key", "The receiver's private key"],
  concept="Digital signatures",
  explanation="The sender signs a hash of the document with the sender's own private key. Anyone can verify the "
              "signature with the sender's public key. Only the sender has that private key, so a valid "
              "signature proves who signed and that the document has not changed.",
  steps=["Sign with own private key", "Others verify with the signer's public key"],
  wrong="A signature made with a public key would prove nothing, because anyone can get a public key. The "
        "receiver's keys are used for encrypting to the receiver, not for proving who the sender is.",
  seconds=40)
Q(T, "Encryption and authentication", "Advanced",
  "Which of the following is a symmetric-key encryption algorithm, using the same secret key to encrypt and "
  "decrypt?",
  ["AES", "RSA", "Elliptic Curve Cryptography (ECC)", "Diffie-Hellman"],
  concept="Symmetric vs asymmetric algorithms",
  explanation="AES (Advanced Encryption Standard) is a symmetric block cipher: sender and receiver share one "
              "secret key. It is fast, which is why it encrypts the bulk of data in HTTPS sessions.",
  steps=["One shared secret key = symmetric", "AES is symmetric"],
  wrong="RSA and ECC are public-key (asymmetric) systems, and Diffie-Hellman is an asymmetric key-exchange method "
        "used to agree on a shared key, not to encrypt data directly.", seconds=30)

# ================================================================ 10. Database Fundamentals (2 / 3 / 2)
T = "Database Fundamentals"
Q(T, "DBMS concepts", "Basic",
  "In a relational database table, a single row is also called a:",
  ["Tuple", "Attribute", "Domain", "Schema"],
  concept="Relational terminology",
  explanation="In the relational model a table is a relation, a row is a tuple (one record, such as one "
              "customer), and a column is an attribute (such as the customer name).",
  steps=["Row = tuple = record", "Column = attribute = field"],
  wrong="An attribute is a column, a domain is the set of allowed values for a column, and a schema is the "
        "structure of the database.", seconds=15)
Q(T, "Keys", "Basic",
  "Which key uniquely identifies each record in a table and cannot contain a NULL value?",
  ["Primary key", "Foreign key", "Non-key attribute", "Derived attribute"],
  concept="Primary key",
  explanation="A primary key, such as an account number, has a unique value for every row and can never be empty "
              "(NULL), so each record can be identified without confusion.",
  steps=["Unique + NOT NULL + identifies each row = primary key"],
  wrong="A foreign key refers to another table and can repeat; a non-key attribute (such as a name) may repeat; "
        "a derived attribute is calculated from other data, such as age from date of birth.", seconds=15)
Q(T, "Keys", "Intermediate",
  "Table Accounts(AccountNo, CustomerID, Balance) has AccountNo as its primary key. CustomerID refers to the "
  "primary key of the Customers table, and one customer may hold several accounts. In Accounts, CustomerID is a:",
  ["Foreign key", "Primary key", "Candidate key", "Super key on its own"],
  concept="Foreign key",
  explanation="A foreign key is a column in one table that refers to the primary key of another table and links "
              "the two. Because a customer can have several accounts, CustomerID repeats in Accounts, so it cannot "
              "identify a row by itself.",
  steps=["Refers to the primary key of another table = foreign key",
         "Values repeat, so it is not a primary, candidate or super key here"],
  wrong="AccountNo is the primary key; a candidate key or super key must be unique for every row, and CustomerID "
        "repeats when a customer has several accounts.", seconds=30)
Q(T, "SQL basics", "Intermediate",
  "Which SQL clause filters groups AFTER the GROUP BY step, for example to show only branches having more than 100 "
  "accounts?",
  ["HAVING", "WHERE", "ORDER BY", "DISTINCT"],
  concept="WHERE vs HAVING",
  explanation="WHERE filters individual rows before grouping; HAVING filters the groups after GROUP BY and can use "
              "aggregate functions, for example HAVING COUNT(*) > 100.",
  steps=["Condition on an aggregate of a group = HAVING"],
  wrong="WHERE works on individual rows and cannot use aggregates such as COUNT(*); ORDER BY only sorts the "
        "result; DISTINCT removes duplicate rows.", seconds=25)
Q(T, "DBMS concepts", "Intermediate",
  "The SQL commands CREATE, ALTER and DROP belong to which category?",
  ["DDL (Data Definition Language)", "DML (Data Manipulation Language)", "DCL (Data Control Language)",
   "TCL (Transaction Control Language)"],
  concept="SQL command categories",
  explanation="DDL commands define or change the structure of database objects: CREATE makes a table, ALTER "
              "changes its structure and DROP removes it.",
  steps=["Structure of objects = DDL", "INSERT/UPDATE/DELETE = DML", "GRANT/REVOKE = DCL",
         "COMMIT/ROLLBACK = TCL"],
  wrong="DML changes the data inside tables, DCL controls access rights, and TCL manages transactions.",
  seconds=20)
Q(T, "SQL basics", "Advanced",
  "Table Accounts has these rows (acc_id, branch, balance): (101, Pune, 72000), (102, Delhi, 45000), "
  "(103, Pune, 51000), (104, Delhi, 90000), (105, Agra, 60000), (106, Delhi, 55000), (107, Pune, 30000), "
  "(108, Agra, 20000).\n\nWhich branches does this query return?\n\n"
  "SELECT branch, COUNT(*) FROM Accounts WHERE balance > 50000 GROUP BY branch HAVING COUNT(*) >= 2;",
  ["Pune and Delhi", "Pune, Delhi and Agra", "Delhi only", "Pune only"],
  concept="WHERE, GROUP BY and HAVING together",
  explanation="WHERE runs first and keeps rows with balance above 50000: 101 Pune, 103 Pune, 104 Delhi, 105 Agra "
              "and 106 Delhi. GROUP BY then counts them per branch: Pune 2, Delhi 2, Agra 1. HAVING keeps groups "
              "with a count of at least 2, so the result is Pune and Delhi.",
  steps=["WHERE balance > 50000 -> 101, 103, 104, 105, 106", "Counts: Pune 2, Delhi 2, Agra 1",
         "HAVING COUNT(*) >= 2 -> Pune, Delhi"],
  wrong="Agra has only one account above 50000. Delhi has three accounts in all, but one (102, 45000) is removed by "
        "WHERE, leaving 2, and Pune likewise has 2.", seconds=90, computed=True)
Q(T, "DBMS concepts", "Advanced",
  "A relation is in First Normal Form and has a composite primary key. Which additional condition puts it in "
  "Second Normal Form (2NF)?",
  ["No non-key attribute depends on only a part of the composite primary key",
   "No non-key attribute depends on another non-key attribute",
   "Every determinant is a candidate key",
   "The relation has no multi-valued dependencies"],
  concept="Normal forms",
  explanation="2NF removes partial dependencies: every non-key attribute must depend on the whole composite key, "
              "not on just part of it. For example, in Enrolment(StudentID, CourseID, StudentName), StudentName "
              "depends only on StudentID, which breaks 2NF.",
  steps=["1NF: atomic values", "2NF: 1NF + no partial dependency on part of a composite key",
         "3NF: 2NF + no transitive dependency", "BCNF: every determinant is a candidate key"],
  wrong="'No non-key attribute depends on another non-key attribute' is the 3NF rule (no transitive dependency); "
        "'every determinant is a candidate key' defines BCNF; removing multi-valued dependencies is 4NF.",
  seconds=45)

# ================================================================ 11. MS Office (3 / 4 / 3)
T = "MS Office"
Q(T, "Shortcuts", "Basic",
  "In MS Word and MS Excel, which keyboard shortcut undoes the last action?",
  ["Ctrl + Z", "Ctrl + Y", "Ctrl + X", "Ctrl + V"],
  concept="Common Office shortcuts",
  explanation="Ctrl + Z reverses (undoes) the most recent action, such as deleting a paragraph by mistake.",
  steps=["Undo = Ctrl + Z", "Redo/repeat = Ctrl + Y"],
  wrong="Ctrl + Y redoes or repeats an action, Ctrl + X cuts, and Ctrl + V pastes.", seconds=15,
  facts=[fact("Ctrl+Z undoes the previous action; Ctrl+Y redoes; Ctrl+X cuts; Ctrl+V pastes", MS_WORD)])
Q(T, "MS Excel", "Basic",
  "In an MS Excel worksheet, the box formed where a row and a column intersect is called a:",
  ["Cell", "Range", "Workbook", "Ribbon"],
  concept="Excel terminology",
  explanation="A cell is the intersection of a row and a column and is named by them, for example B4 is column B, "
              "row 4.",
  steps=["Row x column intersection = cell"],
  wrong="A range is a group of cells (such as A1:C5), a workbook is the whole Excel file, and the ribbon is the "
        "command toolbar at the top.", seconds=15)
Q(T, "MS PowerPoint", "Basic",
  "Which key starts a PowerPoint slide show from the first slide?",
  ["F5", "F7", "F1", "F12"],
  concept="PowerPoint presentation shortcuts",
  explanation="F5 starts the presentation from the beginning. Shift + F5 starts it from the slide currently "
              "selected.",
  steps=["From beginning = F5", "From current slide = Shift + F5"],
  wrong="F7 runs the spelling check, F1 opens Help, and F12 opens the Save As dialog.", seconds=15,
  facts=[fact("F5 starts a presentation from the beginning; Shift+F5 from the current slide", MS_PPT)])
Q(T, "MS Word", "Intermediate",
  "In MS Word, which keyboard shortcut inserts a manual page break so that the following text starts on a new page?",
  ["Ctrl + Enter", "Shift + Enter", "Ctrl + Shift + Enter", "Alt + Enter"],
  concept="Breaks in Word",
  explanation="Ctrl + Enter inserts a page break. Shift + Enter inserts only a line break within the same "
              "paragraph, and Ctrl + Shift + Enter inserts a column break.",
  steps=["Page break = Ctrl + Enter", "Line break = Shift + Enter", "Column break = Ctrl + Shift + Enter"],
  wrong="Shift + Enter starts a new line in the same paragraph, Ctrl + Shift + Enter inserts a column break, and "
        "Alt + Enter does not insert a page break.", seconds=20,
  facts=[fact("Word: Ctrl+Enter inserts a page break, Shift+Enter a line break, Ctrl+Shift+Enter a column break",
              MS_WORD)])
Q(T, "MS Excel", "Intermediate",
  "While editing a formula in Excel, you select the reference A1. Which key cycles it through $A$1, A$1, $A1 and "
  "back to A1?",
  ["F4", "F2", "F9", "F11"],
  concept="Absolute and relative references",
  explanation="F4 cycles a selected cell reference through every combination of absolute and relative. This "
              "saves typing the $ signs by hand when building a formula you plan to copy.",
  steps=["Toggle absolute/relative reference = F4"],
  wrong="F2 edits the active cell, F9 recalculates the workbooks, and F11 creates a chart on a separate chart "
        "sheet.", seconds=20,
  facts=[fact("F4 cycles through combinations of absolute and relative references when a reference is selected in "
              "a formula; F2 edits the active cell; F9 calculates; F11 creates a chart sheet", MS_EXCEL)])
Q(T, "MS PowerPoint", "Intermediate",
  "Which PowerPoint view shows all slides as thumbnails on one screen, so you can easily drag slides into a new "
  "order?",
  ["Slide Sorter view", "Notes Page view", "Reading View", "Presenter View"],
  concept="PowerPoint views",
  explanation="Slide Sorter view arranges every slide as a thumbnail in a grid, which makes reordering, "
              "duplicating or deleting slides quick.",
  steps=["All slides as thumbnails for reordering = Slide Sorter"],
  wrong="Notes Page view shows one slide with its speaker notes, Reading View plays the slides in a window, and "
        "Presenter View is the presenter's screen during a slide show.", seconds=20)
Q(T, "Shortcuts", "Intermediate",
  "In MS Excel, which keyboard shortcut enters today's date as a fixed value in the active cell?",
  ["Ctrl + ;", "Ctrl + Shift + :", "Ctrl + D", "Ctrl + T"],
  concept="Date and time shortcuts in Excel",
  explanation="Ctrl + ; (semicolon) types the current date as a fixed value that will not change later. "
              "Ctrl + Shift + : (colon) enters the current time.",
  steps=["Current date = Ctrl + ;", "Current time = Ctrl + Shift + :"],
  wrong="Ctrl + Shift + : enters the current time, Ctrl + D fills down from the cell above, and Ctrl + T creates "
        "a table.", seconds=20,
  facts=[fact("Excel: Ctrl+; enters the current date; Ctrl+Shift+: enters the current time; Ctrl+D fills down; "
              "Ctrl+T opens Create Table", MS_EXCEL)])
Q(T, "MS Excel", "Advanced",
  "Cells A1 to A5 contain 12, 45, 67, 23 and 89. What value does =SUMIF(A1:A5,\">40\") return?",
  ["156", "201", "212", "236"], "B",
  concept="SUMIF with a comparison criterion",
  explanation="SUMIF adds only the cells that meet the condition. The values greater than 40 are 45, 67 and 89, "
              "and 45 + 67 + 89 = 201.",
  steps=["Values > 40: 45, 67, 89", "45 + 67 + 89 = 201"],
  wrong="236 is the sum of all five cells; 156 leaves out 45 (it adds only 67 and 89); 212 has no basis in "
        "the data.", seconds=45, computed=True,
  facts=[fact("SUMIF sums cells that meet a criterion; criteria with comparison symbols such as \">5\" are enclosed "
              "in quotation marks", MS_SUMIF)])
Q(T, "MS Excel", "Advanced",
  "In Excel, A2:C5 holds customer data (ID, Name, Balance): 101 Asha 25000; 102 Ravi 40000; 103 Meena 15500; "
  "104 John 32000. What does =VLOOKUP(103,A2:C5,3,FALSE) return?",
  ["Meena", "15500", "32000", "#N/A"], "B",
  concept="VLOOKUP with exact match",
  explanation="VLOOKUP looks for 103 in the first column of A2:C5. FALSE asks for an exact match, which is found "
              "in the row for Meena. The function then returns the value from the 3rd column of the range "
              "(Balance), which is 15500.",
  steps=["Find 103 in column A (exact match) -> row 'Meena'", "Column index 3 -> Balance", "Result = 15500"],
  wrong="'Meena' is in column 2, so it would need column index 2; 32000 is John's balance in the next row; "
        "#N/A appears only when the ID is not found, and 103 exists.", seconds=45, computed=True)
Q(T, "MS Excel", "Advanced",
  "Cell C1 contains the formula =A1+$B$1. It is copied and pasted into cell D3. What formula appears in D3?",
  ["=B3+$B$1", "=A3+$B$1", "=B3+$C$3", "=A1+$B$1"], "A",
  concept="Relative vs absolute references when copying",
  explanation="Moving from C1 to D3 is 2 rows down and 1 column right. The relative reference A1 shifts the same "
              "way and becomes B3. The absolute reference $B$1 is locked and stays $B$1. So D3 contains =B3+$B$1.",
  steps=["Offset: C1 -> D3 = +1 column, +2 rows", "A1 -> B3 (relative)", "$B$1 stays $B$1 (absolute)"],
  wrong="=A3+$B$1 moves only the row and not the column; =B3+$C$3 wrongly shifts the absolute reference; "
        "=A1+$B$1 treats both references as absolute.", seconds=45, computed=True)

# ================================================================ 12. Digital Payments (1 / 1 / 1)
T = "Digital Payments"
Q(T, "Payment technology", "Basic",
  "What does UPI stand for in digital payments?",
  ["Unified Payments Interface", "Universal Payment Identifier", "Unified Payment Integration",
   "Universal Payments Interchange"],
  concept="UPI",
  explanation="UPI (Unified Payments Interface), developed by NPCI, lets users link bank accounts to a mobile "
              "app and transfer money instantly using a virtual payment address (UPI ID) or QR code.",
  steps=["UPI = Unified Payments Interface"],
  wrong="The other expansions are made-up variations.", seconds=15)
Q(T, "Card security", "Intermediate",
  "When paying online with a debit card, the website asks for the 3-digit number printed on the back of the card. "
  "This number is the:",
  ["CVV", "PIN", "OTP", "IFSC"],
  concept="Card verification value",
  explanation="The CVV (Card Verification Value) printed on the card helps prove that the buyer has the physical "
              "card when shopping online. Never share it, because together with the card number and expiry date "
              "it can be misused.",
  steps=["Printed 3-digit code on the back of the card = CVV"],
  wrong="The PIN is a secret number that is never printed on the card, the OTP is a one-time code sent by SMS, "
        "and IFSC identifies a bank branch.", seconds=15)
Q(T, "Card security", "Advanced",
  "Under card tokenisation, what does a merchant's app store and use for repeat payments instead of the customer's "
  "actual card number?",
  ["A unique substitute value (token) from which the merchant cannot recover the card number",
   "The card number in plain text, protected only by the customer's password",
   "The CVV printed on the back of the card", "The one-time password from the last transaction"],
  concept="Card tokenisation",
  explanation="Tokenisation replaces the real card number with a unique token tied to that card, merchant and "
              "device. If the merchant's systems are breached, attackers get only tokens. Only the token service "
              "(card network or issuer) can map a token back to the card, and the token is useless elsewhere.",
  steps=["Real card number -> token issued through the card network", "Merchant stores only the token"],
  wrong="Storing the card number in plain text is exactly what tokenisation avoids. CVVs must not be stored by "
        "merchants, and an OTP is valid for one transaction only.", seconds=30)

# ================================================================ 13. Computer Abbreviations (2 / 3 / 2)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic",
  "What is the full form of HTML?",
  ["HyperText Markup Language", "High Transfer Machine Language", "HyperText Machine Link",
   "Home Tool Markup Language"],
  concept="Web abbreviations",
  explanation="HTML (HyperText Markup Language) is the standard language for structuring web pages, using tags such "
              "as <p> for paragraphs and <a> for links.",
  steps=["HTML = HyperText Markup Language"],
  wrong="The other expansions are made up.", seconds=15)
Q(T, S, "Basic",
  "A bank statement is emailed as a .pdf file. What does PDF stand for?",
  ["Portable Document Format", "Printed Document File", "Public Data Format", "Protected Document File"],
  concept="File-format abbreviations",
  explanation="PDF (Portable Document Format) keeps a document's layout the same on any device, which is why "
              "statements and forms are shared as PDFs.",
  steps=["PDF = Portable Document Format"],
  wrong="The other expansions are not real.", seconds=15)
Q(T, S, "Intermediate",
  "Every network card has a hardware address called a MAC address. What does MAC stand for here?",
  ["Media Access Control", "Machine Address Code", "Memory Access Controller", "Main Area Connection"],
  concept="Networking abbreviations",
  explanation="MAC (Media Access Control) address is the 48-bit hardware address of a network interface, usually "
              "written like 3C:52:82:1A:4F:09, and is used for delivery within a local network.",
  steps=["MAC = Media Access Control"],
  wrong="The other expansions are made up and do not name the data-link layer's addressing.", seconds=20)
Q(T, S, "Intermediate",
  "What does BIOS stand for?",
  ["Basic Input/Output System", "Binary Integrated Operating System", "Basic Internal Operating Software",
   "Boot Input/Output Sequence"],
  concept="Firmware abbreviations",
  explanation="BIOS (Basic Input/Output System) is firmware stored on the motherboard. It tests the hardware at "
              "start-up and starts the boot loader. Newer PCs use UEFI, which does the same job.",
  steps=["BIOS = Basic Input/Output System"],
  wrong="The other expansions are invented; BIOS is not an operating system.", seconds=20)
Q(T, S, "Intermediate",
  "In computing, what does DHCP stand for?",
  ["Dynamic Host Configuration Protocol", "Digital Hypertext Control Protocol", "Domain Host Connection Process",
   "Dynamic Hardware Communication Port"],
  concept="Protocol abbreviations",
  explanation="DHCP (Dynamic Host Configuration Protocol) automatically gives devices on a network an IP address, "
              "subnet mask, default gateway and DNS server, so users do not have to configure them by hand.",
  steps=["DHCP = Dynamic Host Configuration Protocol"],
  wrong="The other expansions are invented.", seconds=20)
Q(T, S, "Advanced",
  "What is the full form of EEPROM?",
  ["Electrically Erasable Programmable Read-Only Memory", "Electronically Encrypted Programmable Read-Only Memory",
   "Extended Erasable Programmable Random-Only Memory", "Electrically Encoded Permanent Read-Only Memory"],
  concept="Types of ROM",
  explanation="EEPROM is ROM that can be erased and rewritten electrically, byte by byte, without removing the "
              "chip. EPROM, by contrast, is erased with ultraviolet light. Flash memory is a type of EEPROM that "
              "erases in blocks.",
  steps=["E = Electrically, E = Erasable, P = Programmable, ROM = Read-Only Memory"],
  wrong="The other expansions change 'Electrically Erasable' or 'Read-Only' into terms that do not describe the "
        "chip.", seconds=25)
Q(T, S, "Advanced",
  "What does CAPTCHA stand for?",
  ["Completely Automated Public Turing test to tell Computers and Humans Apart",
   "Computer Assisted Program To Check Human Access",
   "Controlled Access Protocol To Confirm Human Authentication",
   "Completely Automated Password Test for Checking Human Accounts"],
  concept="Security abbreviations",
  explanation="A CAPTCHA (Completely Automated Public Turing test to tell Computers and Humans Apart) is a "
              "challenge, such as typing distorted text or selecting images, that humans find easy but bots find "
              "hard. Banks use it to block automated login attempts.",
  steps=["CAPTCHA = Completely Automated Public Turing test to tell Computers and Humans Apart"],
  wrong="The other expansions are invented and miss the 'Turing test' idea at the heart of CAPTCHA.", seconds=25)

# ---------------------------------------------------------------- checks and output
assert len(questions) == 100, len(questions)
keys = Counter(q["correct_answer"] for q in questions)
assert max(keys.values()) <= 28 and min(keys.values()) >= 22, keys
for q in questions:
    final = q["solution"]["final_answer"]
    assert final.startswith(f"Option {q['correct_answer']}: ")

batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_001",
    "created_at": TODAY,
    "notes": "BATCH_001 Computer Knowledge part: 100 original questions (BANK_COMP_000003 to BANK_COMP_000102). "
             "Computable answers (number systems, timing, memory sizes, subnetting, SQL on a given table, Excel "
             "formula results, chmod) are re-derived in tools/batch_001/computer.py. MS Office and Windows "
             "shortcuts were checked against Microsoft Support pages on 2026-11-05.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_001_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
