"""Writes batches/parts/BATCH_008_COMP.json: the 100 Computer Knowledge questions of BATCH_008.

BATCH_008 builds applied scenarios around six shared stimuli (a vault-alarm logic circuit, a Windows command-prompt
session with ipconfig and tracert, a web-server access log, a Txn table for SQL, an Excel fixed-deposit register and
a branch PC's specification sheet). Every computable answer is re-derived below with assertions before the file is
written: the logic circuit by brute force over all 16 inputs (output, count and the De Morgan complement), octal
digits, an 8-bit checksum, BCD addition, the DHCP renewal time (T1 = 0.5 x lease), tracert hop count, SQL in
sqlite3 (ORDER BY with two keys, CASE, EXCEPT, ROW_NUMBER and the NOT IN / NULL trap), Excel COUNTIF / EDATE / MAXIFS /
UNIQUE(exactly_once) / reverse XLOOKUP, binary-search comparisons (simulated), Nyquist rate, virtual-address split,
Base64 length, percent-encoding, cron fields and IPv4 class. The plan quota per (topic, difficulty), subtopics, the
ID range, stimulus IDs and the answer-key balance are also asserted. If any assertion fails, nothing is written.

    python tools/batch_008/computer.py      (run from docs/question-bank)
"""

import base64
import calendar
import datetime as dt
import ipaddress
import itertools
import json
import random
import sqlite3
import sys
import urllib.parse
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
LETTERS = "ABCD"
CK = "Computer Knowledge"
FIRST_ID = 703
AI = ("ai:author-solve", "ai:independent-check")
COMPUTED = ("script:recompute", "ai:author-solve", "ai:independent-check")
SC = "web:search-confirmed"

_rng = random.Random(20261105 + 8)
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
    sid = f"STIM_COMP_008{_stim_no[0]:03d}"
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
# Vault alarm: A = (D AND NOT K) OR (M AND N)
def alarm(d, k, m, n):
    return int((d and not k) or (m and n))


ALL16 = list(itertools.product((0, 1), repeat=4))
assert sum(alarm(*x) for x in ALL16) == 7
ALARM_OPTS = [(1, 0, 0, 0), (1, 1, 1, 0), (0, 1, 1, 0), (0, 0, 0, 1)]  # (D, K, M, N); first one sounds
assert [alarm(*x) for x in ALARM_OPTS] == [1, 0, 0, 0]
SILENT = {
    "(NOT D OR K) AND (NOT M OR NOT N)": lambda d, k, m, n: (not d or k) and (not m or not n),
    "(NOT D AND K) OR (NOT M AND NOT N)": lambda d, k, m, n: (not d and k) or (not m and not n),
    "(NOT D OR K) OR (NOT M OR NOT N)": lambda d, k, m, n: (not d or k) or (not m or not n),
    "(D OR NOT K) AND (M OR N)": lambda d, k, m, n: (d or not k) and (m or n),
}
assert [all(bool(f(*x)) == (alarm(*x) == 0) for x in ALL16) for f in SILENT.values()] == [True, False, False, False]
# NAND as NOT: tie both inputs together
assert all(int(not (a and a)) == int(not a) for a in (0, 1))
# Octal digits
OCT_OPTS = ["1238", "7056", "4410", "777"]
assert [all(c in "01234567" for c in s) for s in OCT_OPTS] == [False, True, True, True]
# 8-bit checksum: sum of bytes modulo 256
CK_BYTES = [0x4F, 0xB2, 0x9C, 0x31]
assert sum(CK_BYTES) == 462 == 0x1CE and sum(CK_BYTES) % 256 == 0xCE and (256 - 0xCE) == 0x32
# BCD addition 47 + 35
raw = 0b01000111 + 0b00110101
assert raw == 0b01111100
assert (raw & 0xF) > 9 and raw + 6 == 0b10000010 and 47 + 35 == 82 and bin(82) == "0b1010010"

# Command prompt: DHCP lease and tracert
LEASE_OBT = dt.datetime(2026, 11, 5, 9, 12, 40)
LEASE_EXP = dt.datetime(2026, 11, 6, 9, 12, 40)
T1 = LEASE_OBT + (LEASE_EXP - LEASE_OBT) / 2
T2 = LEASE_OBT + (LEASE_EXP - LEASE_OBT) * 7 / 8
assert T1 == dt.datetime(2026, 11, 5, 21, 12, 40) and T2 == dt.datetime(2026, 11, 6, 6, 12, 40)
TRACERT = [(1, "<1 ms", "172.18.4.1"), (2, "9 ms", "10.255.0.1"), (3, "35 ms", "10.50.0.1"),
           (4, "39 ms", "10.50.1.20")]
assert len(TRACERT) - 1 == 3 and TRACERT[0][2] == "172.18.4.1"
assert ipaddress.ip_address("172.18.4.37") in ipaddress.ip_network("172.18.4.0/22")
assert ipaddress.ip_network("172.18.4.0/22").netmask == ipaddress.ip_address("255.255.252.0")
# IPv4 class by first octet (classful): B = 128-191 (leading bits 10)
assert format(130, "08b").startswith("10") and not format(130, "08b").startswith("110")

# Web-server log
LOG = [
    ('203.0.113.45', '04/Nov/2026:10:15:02', 'GET /loans/home.html HTTP/1.1', 200, 5120),
    ('203.0.113.45', '04/Nov/2026:10:15:03', 'GET /images/logo.png HTTP/1.1', 304, 0),
    ('198.51.100.7', '04/Nov/2026:10:16:40', 'POST /login HTTP/1.1', 401, 312),
    ('198.51.100.7', '04/Nov/2026:10:16:41', 'POST /login HTTP/1.1', 401, 312),
    ('198.51.100.7', '04/Nov/2026:10:16:41', 'POST /login HTTP/1.1', 401, 312),
    ('198.51.100.7', '04/Nov/2026:10:16:42', 'POST /login HTTP/1.1', 401, 312),
    ('198.51.100.7', '04/Nov/2026:10:16:43', 'POST /login HTTP/1.1', 401, 312),
    ('198.51.100.7', '04/Nov/2026:10:16:43', 'POST /login HTTP/1.1', 401, 312),
    ('198.51.100.7', '04/Nov/2026:10:16:44', 'POST /login HTTP/1.1', 302, 0),
    ('192.0.2.66', '04/Nov/2026:10:20:11', "GET /statement?acc=1001'%20OR%20'1'='1 HTTP/1.1", 500, 1024),
    ('192.0.2.66', '04/Nov/2026:10:20:30', 'GET /download?file=../../../../etc/passwd HTTP/1.1', 403, 210),
    ('192.0.2.66', '04/Nov/2026:10:20:52', 'GET /search?q=<script>alert(1)</script> HTTP/1.1', 200, 2048),
]
assert sum(1 for ip, _, req, st, _ in LOG if ip == "198.51.100.7" and st == 401) == 6
assert LOG[1][3] == 304 and LOG[1][4] == 0
assert urllib.parse.unquote("1001'%20OR%20'1'='1") == "1001' OR '1'='1"

# SQL: Txn table
TXN = [("T01", "A11", "2026-10-01", "D", "Cash", 20000, None),
       ("T02", "A12", "2026-10-01", "W", "ATM", 5000, None),
       ("T03", "A11", "2026-10-02", "W", "UPI", 1500, "A13"),
       ("T04", "A13", "2026-10-02", "D", "UPI", 1500, "A11"),
       ("T05", "A12", "2026-10-03", "D", "NEFT", 50000, "A14"),
       ("T06", "A14", "2026-10-03", "W", "NEFT", 50000, "A12"),
       ("T07", "A11", "2026-10-04", "W", "ATM", 10000, None),
       ("T08", "A13", "2026-10-04", "W", "UPI", 800, "A16"),
       ("T09", "A15", "2026-10-05", "D", "Cash", 7000, None),
       ("T10", "A14", "2026-10-05", "W", "UPI", 2500, "A16")]
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Txn (txn_id TEXT PRIMARY KEY, acc_no TEXT, txn_date TEXT, type TEXT, channel TEXT, "
           "amount INTEGER, ref_acc TEXT)")
db.executemany("INSERT INTO Txn VALUES (?, ?, ?, ?, ?, ?, ?)", TXN)


def col(sql):
    return [r[0] for r in db.execute(sql)]


assert col("SELECT txn_id FROM Txn ORDER BY txn_date DESC, amount DESC")[:2] == ["T09", "T10"]
assert col("SELECT txn_id FROM Txn ORDER BY txn_date DESC, amount ASC")[0] == "T10"
assert col("SELECT txn_id FROM Txn ORDER BY txn_date ASC, amount DESC")[0] == "T01"
SQL_NET = db.execute("SELECT SUM(CASE WHEN type = 'D' THEN amount ELSE -amount END) FROM Txn "
                     "WHERE acc_no = 'A11'").fetchone()[0]
assert SQL_NET == 8500 and 20000 - 1500 == 18500 and sum(t[5] for t in TXN if t[1] == "A11") == 31500
SQL_EXC = col("SELECT acc_no FROM Txn WHERE channel = 'UPI' EXCEPT SELECT acc_no FROM Txn WHERE channel = 'ATM' "
              "ORDER BY 1")
assert SQL_EXC == ["A13", "A14"]
SQL_RN = db.execute("SELECT acc_no, txn_id FROM (SELECT acc_no, txn_id, ROW_NUMBER() OVER (PARTITION BY acc_no "
                    "ORDER BY amount DESC) AS rn FROM Txn) WHERE rn = 1 ORDER BY acc_no").fetchall()
assert len(SQL_RN) == 5 and dict(SQL_RN)["A13"] == "T04" and dict(SQL_RN)["A11"] == "T01"
assert col("SELECT DISTINCT acc_no FROM Txn WHERE acc_no NOT IN (SELECT ref_acc FROM Txn)") == []
assert col("SELECT DISTINCT acc_no FROM Txn WHERE acc_no NOT IN (SELECT ref_acc FROM Txn "
           "WHERE ref_acc IS NOT NULL)") == ["A15"]

# Excel: fixed-deposit register, rows 2-9 (A Name, B Branch, C Deposit date, D Amount, E Tenure months)
FD = [("Asha", "Pune", dt.date(2026, 1, 15), 50000, 12), ("Ravi", "Delhi", dt.date(2026, 2, 10), 120000, 24),
      ("Meena", "Agra", dt.date(2026, 3, 5), 75000, 6), ("Ravi", "Pune", dt.date(2026, 3, 20), 30000, 18),
      ("John", "Delhi", dt.date(2026, 4, 12), 200000, 36), ("Farah", "Nagpur", dt.date(2026, 5, 25), 40000, 12),
      ("Kiran", "Delhi", dt.date(2026, 6, 8), 90000, 9), ("Neha", "Pune", dt.date(2026, 7, 14), 60000, 24)]


def edate(d, months):
    y, m = divmod(d.month - 1 + months, 12)
    y, m = d.year + y, m + 1
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


assert sum(1 for r in FD if r[1] != "Pune") == 5
assert edate(FD[6][2], FD[6][4]) == dt.date(2027, 3, 8)
assert max(r[3] for r in FD if r[1] == "Delhi" and r[4] < 36) == 120000
assert max(r[3] for r in FD if r[1] == "Delhi") == 200000
BR = Counter(r[1] for r in FD)
assert sum(1 for b, c in BR.items() if c == 1) == 2 and len(BR) == 4
assert [r[3] for r in FD if r[0] == "Ravi"] == [120000, 30000]  # XLOOKUP default -> first, search_mode -1 -> last


# Binary search on 1,024 sorted items: worst-case comparisons
def bs_comparisons(n, target):
    lo, hi, c = 0, n - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if mid == target:
            return c
        if mid < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return c


assert max(bs_comparisons(1024, t) for t in range(1024)) == 11
assert max(bs_comparisons(1024, t) for t in [-1, 1024]) <= 11
# Nyquist: highest frequency 20 kHz -> sample at least 40 kHz
assert 2 * 20 == 40
# Virtual address split, 4 KB pages -> 12-bit offset
VA = 0x0003A7F2
assert 4096 == 2 ** 12 and VA >> 12 == 0x3A and VA & 0xFFF == 0x7F2
# Base64 length of a 1,000-byte attachment
assert len(base64.b64encode(bytes(1000))) == 1336 == 4 * -(-1000 // 3)
# Percent-encoding of a space
assert ord(" ") == 0x20 and urllib.parse.quote("branch list.pdf") == "branch%20list.pdf"
# Cron: minute hour day-of-month month day-of-week
CRON = "30 2 * * 1-5".split()
assert CRON[0] == "30" and CRON[1] == "2" and CRON[4] == "1-5"

# ---------------------------------------------------------------- fact-check sources
# Pages opened on 2026-11-05 (web:fact-check)
CHM_MARK1 = "https://www.computerhistory.org/revolution/birth-of-the-computer/4/86"
MS_TRACERT = "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tracert"
RFC2131 = "https://www.rfc-editor.org/rfc/rfc2131"
MDN_304 = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/304"
MDN_401 = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401"
OWASP_PT = "https://community.owasp.org/attacks/Path_Traversal"
OWASP_SQLI = "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
OWASP_XSS = "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"
MAN_CRON = "https://man7.org/linux/man-pages/man5/crontab.5.html"
MAN_TAIL = "https://man7.org/linux/man-pages/man1/tail.1.html"
MS_LOCK = ("https://support.microsoft.com/en-us/office/lock-or-unlock-specific-areas-of-a-protected-worksheet-"
           "75481b72-db8a-4267-8c43-042a5f2cd93a")
MS_WORD_KEYS = ("https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-"
                "f762f663ceb2")
MS_EDATE = "https://support.microsoft.com/en-us/office/edate-function-3c920eb2-6e66-44e7-a1f5-753ae47ee4f5"
MS_MAXIFS = "https://support.microsoft.com/en-us/office/maxifs-function-dfd611e6-da2c-488a-919b-9b6376b28883"
MS_UNIQUE = "https://support.microsoft.com/en-us/office/unique-function-c5ab87fd-30a3-4ce9-9d1a-40204fb85e1e"
MS_XLOOKUP = "https://support.microsoft.com/en-us/office/xlookup-function-b7fd680e-6d10-43e6-84f9-88eae8bf5929"
MS_HANDOUT = ("https://support.microsoft.com/en-us/office/print-your-powerpoint-slides-handouts-or-notes-194d4320-"
              "aa03-478b-9300-df25f0d15dc4")
MS_ROLLBACK = ("https://support.microsoft.com/en-us/windows/update-drivers-through-device-manager-in-windows-"
               "ec62f46c-ff14-c91d-eead-d7126dc1f7b6")
RBI_CARDS = "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11788"
FIDO_PASSKEYS = "https://fidoalliance.org/passkeys/"
NIST_ZT = "https://csrc.nist.gov/pubs/sp/800/207/final"
DENSO_QR = "https://www.qrcode.com/en/history/"
RFC4648 = "https://www.rfc-editor.org/rfc/rfc4648#section-4"
RFC1034 = "https://www.rfc-editor.org/rfc/rfc1034"
RFC4511 = "https://www.rfc-editor.org/rfc/rfc4511"
GOOGLE_SITE = "https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site"
CHM_RAID = "https://www.computerhistory.org/storageengine/u-c-berkeley-paper-catalyses-interest-in-raid/"
# Confirmed only in search results (web:search-confirmed)
NPCI_USSD = ("https://www.npci.org.in/PDF/npci/press-releases/2016/NPCI_Press Release_USSD based Mobile Banking "
             "Appliaction.pdf").replace(" ", "%20")
NPCI_BHIM = "https://www.npci.org.in/PDF/npci/press-releases/2017/BHIM-transactions-gaining-pace-each-passing-month.pdf"
BHARATQR = "https://en.wikipedia.org/wiki/BharatQR"

# ================================================================ 1. Computer Fundamentals (1 / 3 / 4)
T = "Computer Fundamentals"
S_LOGIC = new_stim(
    "input_output", "Logic circuit of a strong-room alarm",
    "A bank's strong room has four sensors, each giving 1 (true) or 0 (false):\n\n- D = 1 when the strong-room "
    "door is open\n- K = 1 when a valid key card has been swiped\n- M = 1 when the motion sensor detects movement\n"
    "- N = 1 when night mode is switched on\n\nThe alarm output A is produced by this circuit:\n\n```\nA = (D AND "
    "(NOT K)) OR (M AND N)\n```\n\nThe alarm sounds when A = 1.",
    "A = 1 for 7 of the 16 input combinations: D = 1, K = 0 (4 combinations) plus M = 1, N = 1 (4 combinations), "
    "less the 1 combination counted twice. By De Morgan's laws, the alarm is silent when (NOT D OR K) AND (NOT M "
    "OR NOT N).")
o = ["D = 1, K = 0, M = 0, N = 0", "D = 1, K = 1, M = 1, N = 0", "D = 0, K = 1, M = 1, N = 0",
     "D = 0, K = 0, M = 0, N = 1"]
Q(T, "Number systems", "Intermediate",
  "Refer to the strong-room alarm. For which of these input combinations does the alarm sound?", o,
  concept="Evaluating a logic expression",
  explanation="A = 1 if either bracket is 1. (D AND NOT K) needs the door open with no valid key card. (M AND N) "
              "needs motion during night mode. D = 1, K = 0 makes the first bracket 1, so the alarm sounds.",
  steps=["D = 1, K = 0 -> D AND NOT K = 1 AND 1 = 1", "1 OR anything = 1", "Alarm sounds"],
  wrong="D = 1, K = 1: the key card cancels the first bracket, and M = 1 with N = 0 keeps the second at 0. "
        "D = 0, K = 1, M = 1, N = 0: both brackets are 0. D = 0, K = 0, M = 0, N = 1: night mode without motion "
        "gives 0.", seconds=40, computed=True, stim=S_LOGIC, pos=1)
Q(T, "Number systems", "Intermediate",
  "Refer to the strong-room alarm. The supplier wants to build the whole circuit, including the NOT gate, using "
  "only one type of gate. Which gate type can do this on its own?",
  ["NAND gate", "AND gate", "OR gate", "XOR gate"],
  concept="Universal gates",
  explanation="NAND (and also NOR) is a universal gate: NOT, AND and OR can all be built from NAND gates alone. "
              "For example, a NAND gate with both inputs tied together gives NOT A, and a NAND followed by such a "
              "NOT gives AND.",
  steps=["NOT A = A NAND A", "A AND B = NOT (A NAND B)", "A OR B = (NOT A) NAND (NOT B)"],
  wrong="AND and OR gates alone cannot produce inversion, so NOT cannot be built. XOR alone cannot make AND or OR "
        "from the inputs, so it is not universal.", seconds=25, computed=True, stim=S_LOGIC, pos=2)
o, a = ordered(7, [4, 8, 9])
Q(T, "Number systems", "Advanced",
  "Refer to the strong-room alarm. The four inputs can take 2^4 = 16 combinations. For how many of them does the "
  "alarm sound?", o, a,
  concept="Counting true rows of a Boolean function",
  explanation="(D AND NOT K) is 1 when D = 1 and K = 0, whatever M and N are: 4 combinations. (M AND N) is 1 when "
              "M = 1 and N = 1, whatever D and K are: 4 combinations. The combination D = 1, K = 0, M = 1, N = 1 "
              "is in both groups, so it is counted once: 4 + 4 - 1 = 7.",
  steps=["First bracket: 2 x 2 = 4 rows", "Second bracket: 2 x 2 = 4 rows", "Overlap: 1 row", "4 + 4 - 1 = 7"],
  shortcut="Inclusion-exclusion: |X or Y| = |X| + |Y| - |X and Y|.",
  wrong="8 forgets to remove the overlapping row. 4 counts only one bracket. 9 adds the overlap instead of "
        "subtracting it.", seconds=60, computed=True, stim=S_LOGIC, pos=3)
o = list(SILENT)
Q(T, "Number systems", "Advanced",
  "Refer to the strong-room alarm. Which expression is true exactly when the alarm is SILENT (A = 0)?", o,
  concept="De Morgan's laws",
  explanation="Silent = NOT A = NOT[(D AND NOT K) OR (M AND N)]. De Morgan: NOT(X OR Y) = (NOT X) AND (NOT Y), "
              "and NOT(X AND Y) = (NOT X) OR (NOT Y). So NOT(D AND NOT K) = NOT D OR K, NOT(M AND N) = NOT M OR "
              "NOT N, and NOT A = (NOT D OR K) AND (NOT M OR NOT N).",
  steps=["NOT A = NOT(D.K') AND NOT(M.N)", "NOT(D.K') = D' + K", "NOT(M.N) = M' + N'",
         "Silent = (D' + K)(M' + N')"],
  wrong="(NOT D AND K) OR (NOT M AND NOT N) changes AND/OR inside the brackets wrongly. Joining the brackets with OR "
        "forgets that NOT of an OR becomes an AND. (D OR NOT K) AND (M OR N) does not complement the variables.",
  seconds=60, computed=True, stim=S_LOGIC, pos=4)
o = list(OCT_OPTS)
Q(T, "Number systems", "Basic",
  "A system log stores file permissions as octal (base 8) numbers. Which of these values CANNOT be a valid octal "
  "number?", o,
  concept="Digits of the octal system",
  explanation="Octal uses only the digits 0 to 7. 1238 contains the digit 8, so it cannot be an octal number.",
  steps=["Octal digits: 0-7", "1238 contains 8 -> invalid"],
  wrong="7056, 4410 and 777 use only the digits 0-7, so each is a valid octal number.", seconds=15, computed=True)
Q(T, "Generations and history", "Intermediate",
  "A large electromechanical calculator, driven by a 50-foot rotating shaft, was conceived by Howard Aiken, built "
  "by IBM and completed in 1944; Grace Hopper was one of its programmers. Which machine is this?",
  ["Harvard Mark I", "ENIAC", "UNIVAC I", "Colossus"],
  concept="Early computers",
  explanation="The Harvard Mark I (IBM's Automatic Sequence Controlled Calculator) was Howard Aiken's idea, built "
              "by IBM and completed in 1944. It was electromechanical (relays, switches and a long rotating shaft), "
              "not fully electronic. Grace Hopper programmed it during World War II.",
  steps=["Aiken + IBM + 1944 + electromechanical = Harvard Mark I"],
  wrong="ENIAC (1945) was electronic, built at the University of Pennsylvania with vacuum tubes. UNIVAC I (1951) "
        "was an early commercial electronic computer. Colossus was a British electronic code-breaking machine.",
  seconds=20,
  facts=[fact("CHM: The Harvard Mark I was the brainchild of Howard Aiken but built by IBM, completed in 1944, "
              "electromechanical and powered by a 50-foot rotating shaft; Grace Hopper programmed it.", CHM_MARK1)])
o, a = ordered(0xCE, [0x32, 0xE1, 0x1CE], fmt=lambda v: f"{v:X} (hex)")
Q(T, "Number systems", "Advanced",
  "A simple data link protects each message with an 8-bit checksum: the sender adds all the bytes and keeps only "
  "the lowest 8 bits of the sum (that is, the sum modulo 256). A message has the bytes 4F, B2, 9C and 31 "
  "(hexadecimal). What checksum is sent?", o, a,
  concept="Checksums with modulo arithmetic",
  explanation="4F + B2 + 9C + 31 = 79 + 178 + 156 + 49 = 462 = 1CE (hex). Keeping only 8 bits (two hex digits) "
              "drops the carry 1, leaving CE.",
  steps=["Convert: 79, 178, 156, 49", "Sum = 462 = 1CE hex", "Modulo 256 -> CE"],
  shortcut="Add in hex directly: 4F + B2 = 101; + 9C = 19D; + 31 = 1CE; keep the last two digits.",
  wrong="1CE keeps the carry, which does not fit in 8 bits. 32 is the two's complement of CE (256 - 206), used "
        "by some other checksum schemes but not the one described. E1 reverses the digits.", seconds=60,
  computed=True)
o = ["1000 0010", "0111 1100", "0101 0010", "1000 1000"]
Q(T, "Number systems", "Advanced",
  "A calculator chip adds the decimal numbers 47 and 35 in BCD (8421 code), so it adds 0100 0111 and 0011 0101. "
  "Plain binary addition gives 0111 1100, whose lower group 1100 is not a valid BCD digit. After the standard BCD "
  "correction, what is the correct BCD result?", o,
  concept="BCD addition and the +6 correction",
  explanation="When a 4-bit group of a BCD sum exceeds 9 (or produces a carry), 6 (0110) is added to that group. "
              "1100 + 0110 = 1 0010: the group becomes 0010 and a carry of 1 goes to the next group. 0111 + 1 = "
              "1000. The result 1000 0010 is BCD for 82 (= 47 + 35).",
  steps=["0111 1100: lower group 1100 = 12 > 9", "Add 0110 -> 0010, carry 1", "Upper group 0111 + 1 = 1000",
         "Result 1000 0010 = 82"],
  wrong="0111 1100 is the uncorrected sum. 0101 0010 is 82 in pure binary, not BCD. 1000 1000 adds the carry but "
        "leaves the lower group wrong.", seconds=60, computed=True)

# ================================================================ 2. Hardware (3 / 4 / 2)
T = "Hardware"
S_SPEC = new_stim(
    "data_table", "Specification sheet of a new branch PC",
    "| Component | Specification |\n|---|---|\n| Processor | 8 cores / 16 threads; base clock 2.4 GHz, max turbo "
    "4.6 GHz; 24 MB L3 cache (shared); TDP 65 W |\n| Memory | 16 GB DDR5 (2 x 8 GB), 2 slots free |\n| Storage | 512 "
    "GB NVMe SSD |\n| Display | 23.8-inch IPS, 1920 x 1080 |\n| Rear ports | 4 x USB-A, 1 x USB-C, HDMI, DisplayPort, "
    "RJ-45, 3.5 mm audio jacks (green: line-out, pink: mic) |\n| Printer (shared) | Laser, 40 pages per minute, "
    "automatic duplex unit |",
    "TDP is the heat the cooler must remove under sustained load. The CPU runs at 2.4 GHz base and boosts up to "
    "4.6 GHz when there is power and thermal headroom. The L3 cache is shared by all eight cores. Headphones use the "
    "green 3.5 mm jack. The duplex unit prints on both sides of the sheet.")
Q(T, "Motherboard and ports", "Basic",
  "Refer to the specification sheet. A clerk wants to plug in wired headphones with an ordinary 3.5 mm plug to "
  "listen to a training video. Where should she plug them in?",
  ["The green 3.5 mm audio jack (line-out)", "The pink 3.5 mm audio jack", "The RJ-45 port", "The HDMI port"],
  concept="Audio ports",
  explanation="On PCs the green 3.5 mm jack is the audio output (line-out) for speakers or headphones; the pink "
              "jack is the microphone input.",
  steps=["Headphones = audio output", "Green 3.5 mm jack = line-out"],
  wrong="The pink jack is for a microphone (input). RJ-45 is the network port. HDMI carries audio to a monitor or "
        "TV, not to a 3.5 mm plug.", seconds=15, stim=S_SPEC, pos=1)
Q(T, "CPU and components", "Intermediate",
  "Refer to the specification sheet. What does 'TDP 65 W' tell the technician choosing a cooler for this "
  "processor?",
  ["The cooling system must be able to remove about 65 W of heat produced under sustained load",
   "The processor can never draw more than 65 W from the power supply, even for a moment",
   "The SMPS (power supply) must be rated at exactly 65 W", "The processor runs at 65 W only in turbo mode"],
  concept="Thermal Design Power",
  explanation="TDP (Thermal Design Power) is the amount of heat, in watts, that the cooling solution is designed to "
              "dissipate when the processor runs a sustained workload at its base clock. Short turbo bursts can "
              "draw more power than the TDP.",
  steps=["TDP = heat the cooler is designed to handle", "65 W cooler rating needed"],
  wrong="Brief turbo bursts can exceed the TDP. The SMPS powers the whole PC and must be rated well above 65 W. TDP "
        "relates to sustained base-clock load, not only to turbo.", seconds=25, stim=S_SPEC, pos=2)
Q(T, "CPU and components", "Intermediate",
  "Refer to the specification sheet. The processor is listed with a base clock of 2.4 GHz and a max turbo of 4.6 "
  "GHz. Which statement is correct?",
  ["It normally runs at 2.4 GHz or above and raises its speed automatically, up to 4.6 GHz, when the workload needs "
   "it and power and temperature allow", "Each of the 8 cores always runs at 4.6 GHz",
   "The total speed is 2.4 + 4.6 = 7.0 GHz", "4.6 GHz is available only after the user overclocks it in the BIOS"],
  concept="Turbo boost (dynamic frequency)",
  explanation="Modern processors change their clock speed with the load. The base clock is the guaranteed speed "
              "at the rated TDP; turbo raises the clock of some or all cores up to the maximum when there is "
              "power and thermal headroom, and drops it again when the load ends or the chip gets hot.",
  steps=["Base = guaranteed speed", "Turbo = automatic boost up to the maximum", "Limited by power and heat"],
  wrong="Not all cores run at maximum turbo all the time. Clock speeds are not added together. Turbo is automatic; "
        "it is not manual overclocking.", seconds=30, stim=S_SPEC, pos=3)
Q("Memory", "Cache and units", "Intermediate",
  "Refer to the specification sheet. The processor has '24 MB L3 cache (shared)'. What does 'shared' mean here?",
  ["All eight cores use the same 24 MB L3 cache, so data loaded by one core can be found there by another",
   "Each core has its own separate 24 MB of L3 cache", "The L3 cache is a part of the 16 GB main memory",
   "The L3 cache is shared with the SSD as a write buffer"],
  concept="Cache levels",
  explanation="L1 (and usually L2) caches are private to each core and very small and fast. L3 is larger, slower "
              "than L1/L2 but much faster than RAM, and is shared by all cores on the chip. One core can find data "
              "there that another core loaded.",
  steps=["L1/L2: per core", "L3: one pool shared by all cores"],
  wrong="'Shared' means one 24 MB pool, not 24 MB per core. Cache is SRAM on the processor chip, not part of the "
        "DDR5 main memory, and it is not the SSD's buffer.", seconds=25, stim=S_SPEC, pos=4)
Q("Input and Output Devices", "Output devices", "Intermediate",
  "Refer to the specification sheet. The shared laser printer has an 'automatic duplex unit'. What does this let "
  "the branch do?",
  ["Print on both sides of a sheet without turning the paper over by hand", "Print two copies at the same time",
   "Scan and print at the same time", "Print in two colours"],
  concept="Duplex printing",
  explanation="Duplex printing means printing on both sides of the paper. An automatic duplex unit turns the sheet "
              "inside the printer, saving paper for long statements and circulars.",
  steps=["Duplex = both sides of the page", "Automatic = printer flips the sheet itself"],
  wrong="Copies are printed one after another. Scanning needs a scanner (multi-function device). Colour depends on "
        "toner, not on duplexing.", seconds=15, stim=S_SPEC, pos=5)
Q(T, "CPU and components", "Basic",
  "A branch PC's processor is described as 'quad-core'. What does this mean?",
  ["The processor chip has four independent processing units that can run instructions at the same time",
   "The processor has four times more RAM than usual", "The processor runs at 4 GHz",
   "The motherboard has four processor sockets"],
  concept="Multi-core processors",
  explanation="A core is a complete processing unit (with its own ALU, control logic and registers). A quad-core "
              "processor has four cores on one chip, so it can work on four tasks (threads) in parallel.",
  steps=["Core = processing unit", "Quad = 4", "Four cores on one chip"],
  wrong="RAM is separate from the processor. Clock speed is given in GHz. Several sockets would mean several "
        "processors, not several cores.", seconds=15)
Q(T, "Motherboard and ports", "Basic",
  "A branch connects a printer, a scanner and a webcam to a desktop computer. Devices that are attached to a "
  "computer to add input, output or storage functions, but are not part of its core (CPU and main memory), are "
  "called:",
  ["Peripheral devices", "Firmware", "Registers", "System software"],
  concept="Peripherals",
  explanation="Peripherals are external or add-on devices such as keyboards, mice, printers, scanners and external "
              "drives, connected through ports or wirelessly.",
  steps=["Printer, scanner, webcam attached to the PC = peripherals"],
  wrong="Firmware is software stored in a chip. Registers are tiny storage cells inside the CPU. System software is "
        "programs such as the operating system.", seconds=15)
Q(T, "CPU and components", "Intermediate",
  "A budget teller PC has no separate graphics card; its processor contains integrated graphics (iGPU). Where does "
  "this integrated graphics get the memory it needs to hold screen images?",
  ["It reserves part of the system's main RAM", "From its own dedicated GDDR video memory chips",
   "From the hard disk's swap file only", "From the CMOS chip"],
  concept="Integrated vs dedicated graphics",
  explanation="Integrated graphics is built into the processor and shares the system RAM: part of main memory is "
              "used as video memory. A dedicated graphics card has its own video memory (VRAM).",
  steps=["iGPU = graphics inside the CPU", "No VRAM of its own -> shares main RAM"],
  wrong="Dedicated GDDR memory is found on separate graphics cards. A swap file is far too slow for display. The "
        "CMOS chip stores firmware settings only.", seconds=20)
Q(T, "Motherboard and ports", "Intermediate",
  "While replacing a desktop processor, a technician notices that the CPU underside has only flat gold contact "
  "pads, while hundreds of tiny spring pins stand up in the motherboard socket. What kind of socket is this?",
  ["LGA (Land Grid Array): the pins are in the socket", "PGA (Pin Grid Array): the pins are on the processor",
   "DIMM slot", "PCIe x16 slot"],
  concept="Processor sockets",
  explanation="In an LGA socket the pins are on the motherboard and the processor has flat 'lands' (pads). In a PGA "
              "design the pins are on the processor and fit into holes in the socket. DIMM and PCIe are slots for "
              "memory and expansion cards.",
  steps=["Pads on CPU, pins in socket = LGA"],
  wrong="PGA is the opposite arrangement. A DIMM slot holds RAM modules. A PCIe x16 slot holds a graphics or "
        "expansion card.", seconds=25)
Q(T, "CPU and components", "Advanced",
  "In one processor design, each machine instruction is carried out by a small sequence of micro-instructions "
  "stored in a special control memory inside the control unit, so new or complex instructions can be added by "
  "changing that stored microcode. In another, the control signals come from fixed logic circuits. What is the "
  "first type of control unit called?",
  ["Microprogrammed control unit", "Hardwired control unit", "Arithmetic logic unit", "Memory management unit"],
  concept="Control unit design",
  explanation="A microprogrammed control unit generates control signals by reading micro-instructions from a "
              "control memory: flexible, easy to change, typical of CISC designs. A hardwired control unit uses "
              "fixed logic gates: faster, but hard to change, typical of RISC designs.",
  steps=["Control signals from stored micro-instructions = microprogrammed"],
  wrong="A hardwired control unit is the second (fixed-logic) type. The ALU does arithmetic and logic, not control. "
        "The MMU translates virtual addresses to physical addresses.", seconds=30)
Q(T, "CPU and components", "Advanced",
  "In an assembly program, the instruction MOV R1, #500 places the number 500 itself into register R1, while MOV "
  "R1, 500 copies into R1 whatever value is stored at memory address 500. Which addressing modes are these?",
  ["#500 is immediate addressing; 500 is direct (absolute) addressing",
   "#500 is direct addressing; 500 is immediate addressing",
   "Both are register-indirect addressing", "#500 is indexed addressing; 500 is relative addressing"],
  concept="Addressing modes",
  explanation="In immediate addressing the operand value is part of the instruction itself (often marked with #). "
              "In direct addressing the instruction gives the memory address of the operand, so the CPU must read "
              "memory to get the value.",
  steps=["Value inside instruction = immediate", "Address of value inside instruction = direct"],
  wrong="The second option swaps the two. Register-indirect takes the address from a register. Indexed and "
        "relative addressing add an index register or the program counter to a base, which is not happening here.",
  seconds=35)

# ================================================================ 3. Software (2 / 1 / 1)
T = "Software"
Q(T, "Programming languages", "Basic",
  "A programmer writes an interest-calculation program in C, as human-readable statements in a text file. What is "
  "this program text called, before it is translated into machine code?",
  ["Source code", "Object code", "Machine code", "Firmware"],
  concept="Source code and object code",
  explanation="Source code is the program as written by the programmer in a programming language. A compiler "
              "translates it into object code / machine code that the processor can run.",
  steps=["Human-written program text = source code"],
  wrong="Object code and machine code are the translated, machine-readable forms. Firmware is software stored in a "
        "device's chip.", seconds=15)
Q(T, "Programming languages", "Basic",
  "A trainee draws a flowchart for a loan-approval program. Which symbol should he use for the step 'Is the credit "
  "score above 750?', where the flow splits into Yes and No paths?",
  ["Diamond (decision)", "Rectangle (process)", "Parallelogram (input/output)", "Oval (start/end)"],
  concept="Flowchart symbols",
  explanation="In a flowchart, a diamond marks a decision: a question with two or more exits such as Yes/No. "
              "Rectangles show processing steps, parallelograms show input or output, and ovals (terminators) mark "
              "start and end.",
  steps=["Yes/No question = decision = diamond"],
  wrong="A rectangle is a calculation or action. A parallelogram is for reading or printing data. An oval marks "
        "the start or end of the flowchart.", seconds=15)
Q(T, "Programming languages", "Intermediate",
  "A branch's token system serves customers strictly in the order in which they took tokens: a new token joins at "
  "the back, and the counter always calls the token at the front. Which data structure models this?",
  ["Queue (first in, first out)", "Stack (last in, first out)", "Binary tree", "Hash table"],
  concept="Stacks and queues",
  explanation="A queue is a FIFO structure: items are added at the rear (enqueue) and removed from the front "
              "(dequeue), so the earliest item is served first.",
  steps=["Join at back, served from front", "First come, first served = FIFO = queue"],
  wrong="A stack serves the most recent item first (LIFO), like a pile of plates. A binary tree organises data "
        "hierarchically for searching. A hash table finds items by key, not by arrival order.", seconds=20)
o, a = ordered(11, [10, 512, 1024])
Q(T, "Programming languages", "Advanced",
  "A program keeps 1,024 account numbers in ascending order and uses binary search: it compares the wanted number "
  "with the middle item and discards the half that cannot contain it, repeating until it finds the number. In the "
  "worst case, how many comparisons does it need to find an account number that is in the list?", o, a,
  concept="Binary search",
  explanation="Each comparison halves the search range. For n items the worst case is floor(log2 n) + 1 "
              "comparisons. log2 1024 = 10, so the worst case is 10 + 1 = 11. Linear search could need up to 1,024.",
  steps=["1024 -> 512 -> 256 -> ... -> 1: ten halvings", "Plus the comparison on the last remaining item",
         "10 + 1 = 11"],
  shortcut="Worst case = number of bits needed to write n (1024 = 2^10 has 11 bits).",
  wrong="10 forgets the final comparison. 512 is half the list. 1,024 is the worst case of linear search.",
  seconds=45, computed=True)

# ================================================================ 4. Operating Systems (1 / 4 / 3)
T = "Operating Systems"
S_CMD = new_stim(
    "input_output", "Command prompt on a branch PC",
    "A technician checks a branch PC (Windows) that is slow to open the head-office portal:\n\n```\nC:\\> ipconfig /all"
    "\nEthernet adapter Ethernet:\n   Physical Address. . . . . . . : 3C-52-82-1A-7F-09\n   DHCP Enabled. . . . . . . "
    ". . : Yes\n   IPv4 Address. . . . . . . . . : 172.18.4.37(Preferred)\n   Subnet Mask . . . . . . . . . : "
    "255.255.252.0\n   Lease Obtained. . . . . . . . : 05 November 2026 09:12:40\n   Lease Expires . . . . . . . . "
    ": 06 November 2026 09:12:40\n   Default Gateway . . . . . . . : 172.18.4.1\n   DHCP Server . . . . . . . . . : "
    "172.18.4.2\n   DNS Servers . . . . . . . . . : 172.18.4.3\n\nC:\\> tracert -d 10.50.1.20\nTracing route to "
    "10.50.1.20 over a maximum of 30 hops\n"
    + "\n".join(f"  {h}   {t:>6}  {ip}" for h, t, ip in TRACERT) +
    "\nTrace complete.\n```\n\n(10.50.1.20 is the head-office portal server.)",
    "The gateway 172.18.4.1 is the branch router and is hop 1. Hops 1-3 are routers; hop 4 is the server itself. "
    "The DHCP lease is 24 hours, so the PC first tries to renew it at T1 = half the lease = 21:12:40 on 5 November.")
Q("Networking", "Devices", "Basic",
  "Refer to the command prompt. The 'Default Gateway' 172.18.4.1 is the address of which device?",
  ["The branch router, which forwards traffic for other networks", "The DNS server", "The PC's own network card",
   "The laser printer"],
  concept="Default gateway",
  explanation="The default gateway is the router interface on the local network. The PC sends it every packet "
              "whose destination is outside its own subnet. In the tracert output the same address is hop 1.",
  steps=["Traffic for other networks -> default gateway", "Gateway = local router (hop 1 in tracert)"],
  wrong="The DNS server is listed separately (172.18.4.3). The PC's own address is 172.18.4.37. A printer does "
        "not route traffic.", seconds=20, stim=S_CMD, pos=1)
Q(T, "Windows and Linux basics", "Basic",
  "Refer to the command prompt. The technician wants the PC to ask the DHCP server for its IP settings again right "
  "away. Which command should he run?",
  ["ipconfig /renew", "ipconfig /all", "tracert /d", "ping /a"],
  concept="Windows network commands",
  explanation="ipconfig /renew asks the DHCP server to renew (or give) the adapter's IP address and settings. "
              "ipconfig /release gives up the current lease.",
  steps=["Get a fresh DHCP lease = ipconfig /renew"],
  wrong="ipconfig /all only displays the settings. tracert shows the route to a host. ping tests reachability.",
  seconds=15, stim=S_CMD, pos=2)
o, a = ordered(3, [1, 2, 4])
Q("Networking", "Devices", "Intermediate",
  "Refer to the command prompt. According to the tracert output, how many routers lie on the path between the PC "
  "and the portal server?", o, a,
  concept="Reading tracert output",
  explanation="Each line of tracert is one hop. Hops 1, 2 and 3 (172.18.4.1, 10.255.0.1, 10.50.0.1) are routers "
              "that forwarded the packets. Hop 4 is 10.50.1.20, the destination server itself.",
  steps=["4 lines = 4 hops", "Last hop = destination", "Routers = 4 - 1 = 3"],
  wrong="4 counts the destination server as a router. 1 and 2 leave out routers shown in the output.", seconds=30,
  computed=True, stim=S_CMD, pos=3)
Q("Networking", "OSI and TCP/IP", "Intermediate",
  "Refer to the command prompt. How does tracert discover the address of each router on the path?",
  ["It sends packets with TTL = 1, 2, 3, ...; each router that reduces the TTL to 0 returns an ICMP 'Time "
   "Exceeded' message, revealing its address", "It asks the DNS server for a list of routers",
   "It reads the routing table of the head-office server", "It broadcasts an ARP request to every router"],
  concept="How traceroute works",
  explanation="Every router decrements the IP TTL field by 1. tracert sends its first probe with TTL 1, so the "
              "first router drops it and replies with ICMP Time Exceeded; then TTL 2 reaches the second router, "
              "and so on, until the destination answers with an Echo Reply.",
  steps=["Probe with TTL = n", "Router n decrements TTL to 0 -> ICMP Time Exceeded", "Increase n until destination "
                                                                                       "replies"],
  wrong="DNS maps names to addresses; it does not list routers (and -d turns off name lookup). tracert cannot read "
        "a remote routing table. ARP works only within the local network.", seconds=30, stim=S_CMD, pos=4,
  facts=[fact("Microsoft: tracert sends ICMP Echo Requests with incrementally increasing TTL; when the TTL reaches "
              "0 a router returns an ICMP Time Exceeded message, and the path is found from these messages.",
              MS_TRACERT)])
o = [f"{T1:%d %B %Y, %H:%M:%S}", f"{T2:%d %B %Y, %H:%M:%S}", f"{LEASE_EXP:%d %B %Y, %H:%M:%S}",
     f"{LEASE_OBT + (LEASE_EXP - LEASE_OBT) / 4:%d %B %Y, %H:%M:%S}"]
Q("Networking", "OSI and TCP/IP", "Advanced",
  "Refer to the command prompt. If the DHCP server sets no special renewal times, when will the PC first try to "
  "renew its lease with the DHCP server that gave it?", o,
  concept="DHCP lease renewal (T1 and T2)",
  explanation="RFC 2131: the renewal time T1 defaults to 0.5 x the lease duration, and the rebinding time T2 to "
              "0.875 x the lease duration. The lease runs 24 hours from 09:12:40 on 5 November, so T1 is 12 hours "
              "later: 21:12:40 on 5 November. If renewal fails, at T2 (06:12:40 on 6 November) the client "
              "broadcasts to any DHCP server.",
  steps=["Lease = 24 h", "T1 = 0.5 x 24 h = 12 h after 09:12:40", "= 05 November 2026, 21:12:40"],
  wrong="06:12:40 on 6 November is T2 (87.5%), the rebinding time. 09:12:40 on 6 November is when the lease "
        "expires. 15:12:40 on 5 November is only a quarter of the lease.", seconds=60, computed=True, stim=S_CMD,
  pos=5,
  facts=[fact("RFC 2131 4.4.5: T1 defaults to (0.5 * duration_of_lease); T2 defaults to (0.875 * "
              "duration_of_lease).", RFC2131)])
Q(T, "Windows and Linux basics", "Intermediate",
  "A Linux administrator wants to watch the bank's application log /var/log/app.log live, so that each new line is "
  "shown on the screen as soon as the application writes it. Which command does this?",
  ["tail -f /var/log/app.log", "head /var/log/app.log", "cat /var/log/app.log", "rm -f /var/log/app.log"],
  concept="Following a log file",
  explanation="tail prints the last 10 lines of a file; with -f (follow) it keeps the file open and prints new "
              "data as it is appended, until the user presses Ctrl+C.",
  steps=["tail = end of file", "-f = keep following new lines"],
  wrong="head shows the first lines. cat prints the file once and exits. rm -f deletes the file.", seconds=20,
  facts=[fact("tail(1): prints the last 10 lines of each file; -f outputs appended data as the file grows.",
              MAN_TAIL)])
Q(T, "Functions", "Intermediate",
  "A bank's data-centre server has two physical processors, and the operating system runs different processes on "
  "both processors at the same instant. What is this capability called?",
  ["Multiprocessing", "Multiprogramming on a single CPU", "Batch processing", "Spooling"],
  concept="Multiprogramming, multitasking and multiprocessing",
  explanation="Multiprocessing means a system with two or more CPUs (or cores) executing processes truly in "
              "parallel. Multiprogramming keeps several programs in memory so that one CPU switches to another "
              "when the current one waits; only one runs at any instant.",
  steps=["More than one CPU running at the same time = multiprocessing"],
  wrong="Multiprogramming on one CPU interleaves programs but never runs two at the same instant. Batch "
        "processing runs jobs one after another without interaction. Spooling queues jobs for slow devices.",
  seconds=20)
Q(T, "Windows and Linux basics", "Intermediate",
  "After Windows Update installs a new network-card driver, a branch PC loses its network connection. The "
  "previous driver worked well. In Device Manager, which option on the network card's Driver tab is the quickest "
  "fix?",
  ["Roll Back Driver", "Disable Device", "Scan for hardware changes", "Uninstall the network card from the BIOS"],
  concept="Device drivers in Windows",
  explanation="Roll Back Driver reinstalls the previously installed driver version for that device, undoing a "
              "faulty recent update. It needs administrator rights and is available only if an older driver was "
              "kept.",
  steps=["New driver broke the device", "Driver tab -> Roll Back Driver -> previous version restored"],
  wrong="Disabling the device switches the network card off completely. Scanning for hardware changes just "
        "re-detects the same driver. The BIOS does not uninstall Windows drivers.", seconds=20,
  facts=[fact("Microsoft: Device Manager -> device Properties -> Driver tab -> Roll Back Driver, for when a recent "
              "update was installed; administrator permissions are needed.", MS_ROLLBACK)])
Q(T, "File systems", "Intermediate",
  "A Linux server's application stops saving files with a 'No space left on device' error. Which command shows, "
  "for each mounted file system, its size, used space and free space in easy units such as G and M?",
  ["df -h", "ls -l", "pwd", "chmod 755"],
  concept="Disk-space commands",
  explanation="df (disk free) reports the total, used and available space of each mounted file system; -h prints "
              "the sizes in human-readable units (K, M, G).",
  steps=["Free space per file system = df", "-h = human-readable sizes"],
  wrong="ls -l lists files in a directory. pwd prints the current directory. chmod changes permissions.",
  seconds=20)
Q(T, "Functions", "Advanced",
  "An operating system uses priority scheduling. Low-priority report jobs keep waiting because high-priority jobs "
  "keep arriving, and some report jobs never get the CPU (starvation). Which technique solves this by gradually "
  "raising the priority of processes the longer they wait?",
  ["Aging", "Thrashing", "Swapping", "Context switching"],
  concept="Starvation and aging",
  explanation="Aging increases a waiting process's priority over time (e.g. by 1 every few minutes), so even the "
              "lowest-priority process eventually gets the highest priority and runs.",
  steps=["Problem: starvation in priority scheduling", "Fix: raise priority with waiting time = aging"],
  wrong="Thrashing is excessive paging. Swapping moves processes between memory and disk. Context switching saves "
        "and loads process state; none of them removes starvation.", seconds=25)
Q(T, "Functions", "Advanced",
  "Two processes update the same account balance. To make sure only one of them is inside the code that reads and "
  "writes the balance at any time, each process does wait(S) before that code and signal(S) after it, using a "
  "variable S that starts at 1. What is S, and what is that section of code called?",
  ["S is a (binary) semaphore guarding the critical section", "S is a page table guarding the kernel",
   "S is a deadlock guarding the critical section", "S is a program counter guarding the stack"],
  concept="Process synchronisation",
  explanation="A semaphore is an integer variable changed only by the atomic operations wait (P) and signal (V). "
              "With S = 1, the first process's wait sets S to 0 and enters; another process's wait must block until "
              "signal sets S back to 1. The protected shared-data code is the critical section, and this gives "
              "mutual exclusion.",
  steps=["wait(S): enter if S > 0, else block", "signal(S): release", "Protected code = critical section"],
  wrong="A page table maps virtual pages to frames. A deadlock is a problem, not a tool. The program counter holds "
        "the next instruction's address.", seconds=30)
Q(T, "Windows and Linux basics", "Advanced",
  "A Linux backup script is scheduled with this crontab line:\n\n30 2 * * 1-5 /opt/scripts/backup.sh\n\nWhen does it "
  "run?",
  ["At 02:30 every Monday to Friday", "At 30 minutes past every hour on days 2 to 5 of each month",
   "At 02:30 on the 1st to 5th of every month", "Every 30 minutes on Tuesdays only"],
  concept="cron schedule format",
  explanation="The five crontab time fields are minute, hour, day of month, month and day of week. Here: minute 30, "
              "hour 2, any day of month, any month, day of week 1-5 (Monday to Friday; 0 or 7 is Sunday).",
  steps=["Fields: min hour dom month dow", "30 2 -> 02:30", "* * -> every day of month, every month",
         "1-5 in the day-of-week field -> Monday to Friday"],
  wrong="The second option reads the fields in the wrong order. The third puts 1-5 in the day-of-month field. "
        "The last invents a 30-minute repeat, which would need */30 in the minute field.", seconds=45,
  computed=True,
  facts=[fact("crontab(5): fields are minute, hour, day of month, month, day of week; 0 or 7 is Sunday; ranges "
              "are inclusive.", MAN_CRON)])

# ================================================================ 5. Input and Output Devices (3 / 4 / 2)
T = "Input and Output Devices"
Q(T, "Input devices", "Basic",
  "On a laptop without a mouse, a loan officer moves the pointer by sliding a finger on a flat, touch-sensitive "
  "pad below the keyboard. What is this pad called?",
  ["Touchpad (trackpad)", "Trackball", "Joystick", "Light pen"],
  concept="Pointing devices",
  explanation="A touchpad senses the position and movement of a finger on its surface and moves the pointer; taps "
              "act as clicks. It is the built-in pointing device of most laptops.",
  steps=["Finger slides on a flat pad = touchpad"],
  wrong="A trackball has a ball rolled by the thumb or fingers. A joystick is a lever for games and machines. A "
        "light pen is pointed at the screen.", seconds=15)
Q(T, "Output devices", "Basic",
  "A customer checks his account statement on the bank app's screen instead of printing it. Output shown on a "
  "screen, which is not permanent and disappears when the display changes, is called:",
  ["Soft copy", "Hard copy", "Hard disk", "Firmware"],
  concept="Soft copy and hard copy",
  explanation="Soft copy is output displayed on a screen (or heard through speakers); it is temporary. Hard copy is "
              "permanent output on paper or another physical medium.",
  steps=["On screen, temporary = soft copy"],
  wrong="Hard copy is printed output. A hard disk is a storage device. Firmware is software in a chip.", seconds=15)
Q(T, "Input devices", "Basic",
  "A bank's phone-banking system lets customers say 'balance enquiry' instead of pressing keys. Which input device "
  "captures the customer's voice so that speech-recognition software can process it?",
  ["Microphone", "Speaker", "Scanner", "Plotter"],
  concept="Audio input",
  explanation="A microphone converts sound into an electrical signal, which is digitised and analysed by "
              "speech-recognition software.",
  steps=["Voice input = microphone"],
  wrong="A speaker is an output device. A scanner captures images of documents. A plotter draws large drawings.",
  seconds=10)
Q(T, "Output devices", "Intermediate",
  "A bank's trading desk compares two monitors. One has a 1 ms response time and the other 8 ms. What does "
  "'response time' measure?",
  ["How quickly a pixel can change from one colour to another, which affects blurring in moving images",
   "How many times per second the whole screen is redrawn", "The delay before the monitor switches on",
   "How many pixels the screen has per inch"],
  concept="Monitor specifications",
  explanation="Response time is the time a pixel takes to change colour (often grey-to-grey), in milliseconds. "
              "Lower is better: fast-moving content shows less smearing or ghosting.",
  steps=["Response time = pixel transition time (ms)", "Lower = less motion blur"],
  wrong="Redraws per second is the refresh rate (Hz). Start-up delay is not a display specification. Pixels per "
        "inch is pixel density.", seconds=20)
Q(T, "Input devices", "Intermediate",
  "At a branch counter, a customer signs with a stylus on a small screen-less pad. The device records the "
  "signature as digital data, including the pen's movement, so that it can be stored with the account-opening "
  "form. What is this device?",
  ["Electronic signature pad", "Optical mark reader", "MICR reader", "Barcode reader"],
  concept="Special-purpose input devices",
  explanation="An electronic signature pad captures a handwritten signature as it is written (position, and on "
              "many pads pressure and timing) and passes it to the computer as digital data.",
  steps=["Sign with stylus, captured digitally = signature pad"],
  wrong="An OMR reads pencil marks in fixed bubbles. A MICR reader reads the magnetic-ink characters on cheques. A "
        "barcode reader reads printed bars.", seconds=20)
Q(T, "Input devices", "Intermediate",
  "A bank's counters used laser barcode scanners that read one-dimensional (1D) barcodes. Customers now show UPI "
  "and e-receipt QR codes on their phone screens, and the old scanners cannot read them. What kind of scanner is "
  "needed?",
  ["A camera-based (image) scanner that can read 2D codes", "A faster laser scanner for 1D barcodes",
   "An optical mark reader", "A MICR reader"],
  concept="1D and 2D code readers",
  explanation="A QR code is a 2D matrix code: data is stored both across and down. A laser scanner sweeps a single "
              "line and reads only 1D barcodes; a camera-based (imager) scanner takes a picture and decodes 2D codes "
              "such as QR, including from phone screens.",
  steps=["QR = 2D code", "Laser line scanner reads only 1D", "Need an imager (camera) scanner"],
  wrong="A faster laser scanner still reads only one line. OMR reads pencil bubbles. MICR reads magnetic ink on "
        "cheques.", seconds=25)
o, a = ordered(40, [10, 20, 80], fmt=lambda v: f"{v} kHz")
Q(T, "Input devices", "Advanced",
  "A recording system must capture sounds with frequencies up to 20 kHz through a microphone without losing "
  "information (no aliasing). According to the Nyquist-Shannon sampling theorem, what is the minimum sampling "
  "rate?", o, a,
  concept="Sampling theorem",
  explanation="A signal can be rebuilt from its samples only if the sampling rate is more than twice its highest "
              "frequency (the Nyquist rate). 2 x 20 kHz = 40 kHz, which is why CD audio uses 44.1 kHz.",
  steps=["Minimum rate = 2 x highest frequency", "2 x 20 kHz = 40 kHz"],
  wrong="10 kHz and 20 kHz are below twice the highest frequency, so high sounds would be distorted (aliased). 80 "
        "kHz works but is not the minimum.", seconds=30, computed=True)
Q(T, "Input devices", "Advanced",
  "A scanner box says 'Optical resolution 600 x 600 dpi; enhanced (interpolated) resolution 19,200 dpi'. Which "
  "figure shows how much real detail the scanner's sensor can capture?",
  ["600 x 600 dpi, because interpolated resolution only adds estimated pixels by software calculation",
   "19,200 dpi, because it is the larger number", "Both are equally real; interpolation uses a second sensor",
   "Neither; resolution of scanners is measured in pages per minute"],
  concept="Optical vs interpolated resolution",
  explanation="Optical resolution is what the sensor actually samples. Interpolated (enhanced) resolution is made "
              "by software inserting calculated pixels between real ones; it makes the file bigger but adds no new "
              "detail.",
  steps=["Real sensor detail = optical resolution", "Interpolation = estimated pixels"],
  wrong="A larger interpolated figure adds no real information. Interpolation is software, not a second sensor. "
        "Pages per minute is a speed rating.", seconds=25)

# ================================================================ 6. Memory (1 / 2 / 2)
T = "Memory"
Q(T, "Secondary storage", "Basic",
  "A branch must hand each auditor a disc of signed records that can be written once and then only read, never "
  "erased or rewritten. Which disc should it use?",
  ["CD-R", "CD-RW", "RAM", "A pen drive"],
  concept="Recordable and rewritable discs",
  explanation="CD-R (Recordable) and DVD-R discs can be written once; after that they can be read many times but "
              "not erased. CD-RW discs can be erased and rewritten.",
  steps=["Write once, read many = CD-R"],
  wrong="CD-RW can be rewritten. RAM is volatile main memory. A pen drive can be erased and rewritten.", seconds=15)
Q(T, "Secondary storage", "Intermediate",
  "For audit and regulatory reasons, a bank stores transaction logs on storage that allows each record to be "
  "written once and then prevents anyone, even administrators, from changing or deleting it until the retention "
  "period ends. What is this type of storage called?",
  ["WORM (Write Once, Read Many) storage", "RAID 0 storage", "Volatile storage", "Cache storage"],
  concept="Immutable storage for compliance",
  explanation="WORM storage (on optical media, special tapes or locked object storage) accepts a write once and "
              "afterwards allows only reading, which protects records from tampering.",
  steps=["Write once, cannot change or delete = WORM"],
  wrong="RAID 0 stripes data for speed and is fully modifiable. Volatile storage loses data when power is off. "
        "Cache is fast temporary memory.", seconds=20)
o = ["Page number 3A (hex), offset 7F2 (hex)", "Page number 3A7 (hex), offset F2 (hex)",
     "Page number 3 (hex), offset A7F2 (hex)", "Page number 3A7F (hex), offset 2 (hex)"]
Q(T, "Primary memory", "Advanced",
  "A system uses 32-bit virtual addresses and a page size of 4 KB (4,096 bytes). A program accesses the virtual "
  "address 0003A7F2 (hex). Into which page number and offset does the memory-management unit split it?", o,
  concept="Paging: page number and offset",
  explanation="A 4 KB page needs 12 offset bits (2^12 = 4096), which are the last 3 hex digits. The remaining "
              "high-order bits form the page number. 0003A7F2: offset = 7F2, page number = 0003A = 3A.",
  steps=["Page size 4096 = 2^12 -> 12-bit offset", "12 bits = 3 hex digits -> 7F2", "Rest: 0003A -> page 3A"],
  wrong="Taking 2 hex digits (8 bits) as the offset fits a 256-byte page. 4 hex digits fit a 64 KB page. One hex "
        "digit fits a 16-byte page.", seconds=50, computed=True)
Q(T, "Primary memory", "Advanced",
  "The firmware of an ATM's controller board is stored in a flash chip from which the processor can run "
  "instructions directly, byte by byte, without first copying them into RAM. The large SSDs in the bank's servers "
  "use a different flash type that is cheaper and denser but is read in pages. Which flash type stores the "
  "firmware?",
  ["NOR flash", "NAND flash", "DRAM", "SRAM"],
  concept="NOR vs NAND flash",
  explanation="NOR flash allows fast random access to any byte, so code can execute in place (XIP); it is used for "
              "firmware. NAND flash is denser and cheaper per bit and is accessed in pages and blocks, so it is used "
              "for bulk storage such as SSDs, memory cards and pen drives.",
  steps=["Execute in place, random byte access = NOR", "Dense, page-based bulk storage = NAND"],
  wrong="NAND is the type in the SSDs. DRAM and SRAM are volatile and would lose the firmware when power is off.",
  seconds=30)

# ================================================================ 7. Internet (2 / 3 / 3)
T = "Internet"
S_LOG = new_stim(
    "input_output", "Access log of a bank's web server",
    "Extract from the web server's access log (client IP, time, request, status code, response size in bytes):\n\n"
    "```\n" + "\n".join(f'{ip} - - [{t} +0530] "{r}" {st} {sz}' for ip, t, r, st, sz in LOG) + "\n```\n\n(%20 in a "
    "URL stands for a space.)",
    "203.0.113.45 is a normal visitor (its logo request gets 304 because its cached copy is still valid). "
    "198.51.100.7 fails to log in six times in about three seconds and then succeeds (302 redirect): automated "
    "password guessing. 192.0.2.66 tries SQL injection (500 error), path traversal (blocked with 403) and "
    "cross-site scripting.")
Q("Cybersecurity", "Encryption and authentication", "Intermediate",
  "Refer to the access log. What do the requests from 198.51.100.7 between 10:16:40 and 10:16:44 most likely show, "
  "and which control would best stop it?",
  ["An automated tool guessing passwords rapidly; limit login attempts (with lockout, delays or CAPTCHA) and use "
   "multi-factor authentication", "A customer with a slow connection; increase the server's bandwidth",
   "A DDoS attack from thousands of computers; buy a bigger web server",
   "A browser caching problem; ask the user to clear the cache"],
  concept="Recognising password-guessing in logs",
  explanation="Six failed POST /login requests (401) from one IP within about three seconds, followed by a "
              "successful login (302 redirect), is far faster than a human types: an automated guessing attack that "
              "found a working password. Rate-limiting or locking out after a few failures slows it, and MFA "
              "stops a guessed password alone from being enough.",
  steps=["Count failures: 6 x 401 in ~3 s", "Then 302 = login succeeded", "Fix: attempt limits + MFA"],
  wrong="A slow connection would not produce repeated failed logins each second. A DDoS comes from many sources; "
        "this is one IP. Caching affects GET requests for pages and images, not login failures.", seconds=40,
  computed=True, stim=S_LOG, pos=1)
Q(T, "Protocols", "Intermediate",
  "Refer to the access log. The failed login requests receive status code 401. What does this status code mean?",
  ["The request lacks valid authentication credentials for the resource", "The page has moved permanently",
   "The server crashed while processing the request", "The request succeeded and the page was sent"],
  concept="HTTP status codes",
  explanation="401 Unauthorized means the request was not successful because it lacks valid authentication "
              "credentials. (403 Forbidden means the server knows who the client is, or does not need to, but "
              "refuses access.)",
  steps=["4xx = client error", "401 = authentication missing or wrong"],
  wrong="A permanent move is 301. A server-side failure is 500. Success is 200.", seconds=20, stim=S_LOG, pos=2,
  facts=[fact("MDN: 401 Unauthorized indicates that a request was not successful because it lacks valid "
              "authentication credentials for the requested resource.", MDN_401)])
Q("Cybersecurity", "Malware", "Intermediate",
  "Refer to the access log. The 10:20:11 request from 192.0.2.66 contains acc=1001' OR '1'='1 and makes the "
  "server fail with error 500. Which attack is being attempted, and what is the primary defence?",
  ["SQL injection; build database queries with parameterised (prepared) statements",
   "Cross-site scripting; encode output shown in web pages", "Phishing; train customers to check sender addresses",
   "Path traversal; restrict file names to a fixed list"],
  concept="SQL injection",
  explanation="The quote ends the account-number value early, and OR '1'='1 is always true, so if the input is "
              "pasted into an SQL query the WHERE clause matches every row. The 500 error shows the input reached "
              "the database query. Prepared statements send data separately from the SQL code, so input can never "
              "change the query's structure.",
  steps=["' closes the string", "OR '1'='1' always true", "Input changes the SQL = SQL injection",
         "Defence: parameterised queries"],
  wrong="Cross-site scripting injects script into web pages, not SQL. Phishing tricks people, not the server. Path "
        "traversal uses ../ to reach files.", seconds=35, stim=S_LOG, pos=3,
  facts=[fact("OWASP: the primary defence against SQL injection is prepared statements with parameterised queries, "
              "which define the SQL structure separately from data values.", OWASP_SQLI)])
Q("Cybersecurity", "Malware", "Intermediate",
  "Refer to the access log. The 10:20:30 request asks for file=../../../../etc/passwd. What is the attacker trying "
  "to do?",
  ["Path (directory) traversal: climb out of the download folder to read a system file",
   "SQL injection: change the database query", "Denial of service: crash the server with traffic",
   "Session hijacking: steal another user's cookie"],
  concept="Path traversal",
  explanation="Each ../ moves one directory up. Enough of them escape the folder that the download feature is meant "
              "to serve and reach files elsewhere, such as /etc/passwd on a Linux server. The 403 shows the server "
              "blocked it.",
  steps=["../ = parent directory", "Repeated ../ escapes the web folder", "Target /etc/passwd = system file"],
  wrong="There is no SQL in this request. A single request is not a traffic flood. No cookie is involved.",
  seconds=25, stim=S_LOG, pos=4,
  facts=[fact("OWASP: a path traversal attack aims to access files and directories stored outside the web root "
              "folder by manipulating ../ sequences.", OWASP_PT)])
Q("Cybersecurity", "Malware", "Intermediate",
  "Refer to the access log. The 10:20:52 request puts <script>alert(1)</script> into the search box, and the "
  "server returns the results page with status 200. If the page displays the search text exactly as typed, which "
  "attack succeeds?",
  ["Cross-site scripting (XSS): the attacker's script runs in the browser of whoever opens that page",
   "SQL injection: the database runs the attacker's command", "Brute-force attack on the search box",
   "Pharming: the bank's DNS record is changed"],
  concept="Cross-site scripting",
  explanation="XSS happens when untrusted input is placed into a web page without encoding, so the browser treats "
              "it as code. An attacker can send a victim a link with such a search text; the script then runs with "
              "the bank site's privileges, for example to steal session data. The defence is context-aware output "
              "encoding (e.g. turning < into &lt;).",
  steps=["Input contains <script>", "Page echoes it unencoded", "Browser executes it = XSS"],
  wrong="The text targets the browser, not the database. One request is not a brute-force attempt. Pharming "
        "changes DNS, not page content.", seconds=30, stim=S_LOG, pos=5,
  facts=[fact("OWASP: XSS occurs when an application includes untrusted data in a page that the browser runs as "
              "code; output encoding is the main defence.", OWASP_XSS)])
Q(T, "Protocols", "Advanced",
  "Refer to the access log. The request for /images/logo.png at 10:15:03 gets status 304 with 0 bytes of body. "
  "What has happened?",
  ["The browser asked whether its cached copy was still current; the server said it was not modified, so the "
   "browser reuses its cached copy", "The logo file was not found on the server",
   "The logo has moved to a new address, which the browser must follow", "The server refused to send the logo"],
  concept="Conditional requests and caching",
  explanation="304 Not Modified is sent in reply to a conditional GET (with If-Modified-Since or If-None-Match) "
              "when the resource has not changed. No body is sent, which saves bandwidth; the browser shows its "
              "cached copy.",
  steps=["Conditional GET from browser cache", "Unchanged -> 304 with no body", "Cached copy reused"],
  wrong="Not found is 404. A moved resource is 301/302 with a Location header. A refusal is 403.", seconds=30,
  stim=S_LOG, pos=6,
  facts=[fact("MDN: 304 Not Modified indicates no need to retransmit the resource; it is sent for conditional "
              "GET/HEAD requests and confirms that the client's cached copy is still valid.", MDN_304)])
Q(T, "Web basics", "Basic",
  "A clerk wants to find the website of a bank's loan scheme that she visited last week but did not bookmark. "
  "Which browser feature lists the pages she visited earlier?",
  ["History", "Bookmarks", "Downloads", "Extensions"],
  concept="Browser features",
  explanation="The browser's History list records pages visited, with dates, so a page can be found again. In "
              "most Windows browsers Ctrl+H opens it.",
  steps=["Pages visited earlier = History"],
  wrong="Bookmarks contain only pages saved deliberately. Downloads lists files saved. Extensions are add-ons.",
  seconds=10)
Q(T, "Email", "Basic",
  "A manager writes an email to the regional office but has to leave before finishing it. She saves it without "
  "sending. In which mail folder will she find it later?",
  ["Drafts", "Sent Items", "Outbox", "Junk"],
  concept="Email folders",
  explanation="Unsent messages that have been saved are kept in the Drafts folder until they are sent or deleted.",
  steps=["Saved but not sent = Drafts"],
  wrong="Sent Items holds messages already sent. The Outbox holds messages waiting to be transmitted. Junk holds "
        "suspected spam received.", seconds=10)
Q(T, "Web basics", "Intermediate",
  "An officer wants a search engine to show results ONLY from the RBI website (rbi.org.in) for the words 'master "
  "direction KYC'. What should she type?",
  ["master direction KYC site:rbi.org.in", "master direction KYC +rbi.org.in", "\"rbi.org.in\" master direction KYC",
   "master direction KYC -rbi.org.in"],
  concept="Search operators",
  explanation="The site: operator limits the results to the given domain, URL or URL prefix.",
  steps=["Results from one website = site:domain"],
  wrong="+ is not a domain filter. Putting the domain in quotes searches for that text anywhere. - excludes a "
        "term, which is the opposite of what she wants.", seconds=20,
  facts=[fact("Google Search Central: the site: operator returns results from the specified domain, URL or URL "
              "prefix.", GOOGLE_SITE)])
Q(T, "Web basics", "Intermediate",
  "A branch circular's link reads https://bank.example/circulars/branch%20list.pdf. What does %20 represent in "
  "this address?",
  ["A space character, written as its hexadecimal ASCII code 20", "The 20th version of the file",
   "A forward slash (/)", "A percentage discount of 20%"],
  concept="URL percent-encoding",
  explanation="Some characters cannot appear directly in a URL, so they are written as % followed by the two-digit "
              "hexadecimal code of the byte. A space is ASCII 32 = 20 hex, hence %20. The file name is 'branch list"
              ".pdf'.",
  steps=["% + hex code", "20 hex = 32 decimal = space"],
  wrong="%20 is not a version or a discount. A forward slash would be %2F.", seconds=20, computed=True)
o, a = ordered(1336, [1000, 1333, 1334])
Q(T, "Email", "Advanced",
  "An email program sends a 1,000-byte attachment using Base64 encoding, which turns every group of 3 bytes into 4 "
  "text characters and pads the last group with '=' to a full 4 characters. Ignoring line breaks, how many "
  "characters does the encoded attachment take?", o, a,
  concept="Base64 encoding in MIME",
  explanation="1,000 bytes = 333 full groups of 3 bytes plus 1 leftover byte. 333 groups give 1,332 characters, "
              "and the leftover byte gives one more group of 4 characters (2 data characters + '=='). Total 1,336.",
  steps=["1000 / 3 = 333 groups, remainder 1", "333 x 4 = 1332", "+ 4 for the padded last group = 1336"],
  shortcut="Length = 4 x ceil(n / 3) = 4 x 334.",
  wrong="1,000 ignores encoding growth. 1,333 is 1000 x 4/3 rounded down and forgets padding. 1,334 adds only "
        "the 2 data characters of the last group without '=='.", seconds=50, computed=True,
  facts=[fact("RFC 4648: Base64 represents 24-bit groups of input bits as 4 encoded characters; padding at the end "
              "uses '='.", RFC4648)])
Q(T, "Protocols", "Advanced",
  "A bank wants www.bank.example and netbanking.bank.example to point to the same server, and to change that "
  "server's IP address in only one place. It gives netbanking.bank.example a DNS record saying it is an alias of "
  "www.bank.example. Which DNS record type is this?",
  ["CNAME", "MX", "A", "PTR"],
  concept="DNS record types",
  explanation="A CNAME (canonical name) record makes one name an alias of another; a resolver that finds it "
              "restarts the lookup at the target name. Only www.bank.example then needs an A record with the IP "
              "address.",
  steps=["Alias name -> canonical name = CNAME"],
  wrong="MX names the mail servers of a domain. An A record maps a name directly to an IPv4 address (it would need "
        "updating in two places). PTR maps an IP address back to a name.", seconds=25,
  facts=[fact("RFC 1034: a CNAME RR identifies its owner name as an alias and gives the canonical name; the lookup "
              "restarts at the canonical name.", RFC1034)])

# ================================================================ 8. Networking (5 / 5 / 1)
T = "Networking"
Q(T, "Topologies", "Basic",
  "An officer connects his wireless earbuds, smartwatch and phone to each other with Bluetooth, within a few "
  "metres of his body. Which type of network do these devices form?",
  ["PAN (Personal Area Network)", "LAN (Local Area Network)", "MAN (Metropolitan Area Network)",
   "WAN (Wide Area Network)"],
  concept="Networks by area",
  explanation="A PAN links devices around one person, over a few metres, typically with Bluetooth or USB. LAN, MAN "
              "and WAN cover a building, a city and countries respectively.",
  steps=["A few metres around one person = PAN"],
  wrong="A LAN covers an office or building, a MAN a city, a WAN countries or continents.", seconds=15)
Q(T, "OSI and TCP/IP", "Basic",
  "In a bank lobby, a display board only receives the exchange rates sent by a central computer; it never sends "
  "any data back. Which data transmission mode is this?",
  ["Simplex", "Half duplex", "Full duplex", "Multiplex"],
  concept="Transmission modes",
  explanation="Simplex communication flows in one direction only, as in radio/TV broadcasting or a display that "
              "only receives. Half duplex is both ways but one at a time; full duplex is both ways at once.",
  steps=["One direction only = simplex"],
  wrong="Half duplex and full duplex both allow data back from the board. Multiplexing combines several signals on "
        "one link; it is not a direction mode.", seconds=15)
Q(T, "Devices", "Basic",
  "A branch's LAN uses Cat6 cables with RJ-45 plugs. Inside the cable, pairs of copper wires are wound around each "
  "other to reduce interference. What type of cable is this?",
  ["Twisted-pair cable", "Coaxial cable", "Optical fibre cable", "Serial ribbon cable"],
  concept="Network cables",
  explanation="Ethernet cables such as Cat5e and Cat6 are twisted-pair cables: each pair is twisted to cancel "
              "electromagnetic interference. They end in RJ-45 connectors.",
  steps=["Copper pairs twisted together + RJ-45 = twisted pair"],
  wrong="Coaxial cable has one central conductor and a shield (cable TV). Optical fibre carries light in glass. "
        "Ribbon cables are flat bundles of parallel wires.", seconds=15)
Q(T, "OSI and TCP/IP", "Basic",
  "A branch switch learns which computer is on which port by reading the MAC addresses in Ethernet frames. In the "
  "OSI model, at which layer does such a switch mainly work?",
  ["Data link layer (Layer 2)", "Network layer (Layer 3)", "Physical layer (Layer 1)", "Transport layer (Layer 4)"],
  concept="Devices and OSI layers",
  explanation="An ordinary switch forwards frames using MAC addresses, which belong to the data link layer "
              "(Layer 2). Routers use IP addresses at Layer 3; hubs and repeaters work at Layer 1.",
  steps=["MAC addresses / frames = Layer 2 = data link"],
  wrong="The network layer uses IP addresses (routers). The physical layer only handles signals (hubs). The "
        "transport layer works with ports and segments in the end computers.", seconds=15)
Q(T, "OSI and TCP/IP", "Intermediate",
  "In the old 'classful' IPv4 addressing, the class of an address was decided by its first octet. To which class "
  "does the address 130.45.2.9 belong?",
  ["Class B", "Class A", "Class C", "Class D"],
  concept="IPv4 address classes",
  explanation="Class A: first octet 1-126 (leading bit 0). Class B: 128-191 (leading bits 10). Class C: 192-223 "
              "(110). Class D: 224-239 (multicast). 130 lies in 128-191, so 130.45.2.9 is Class B (default mask "
              "255.255.0.0).",
  steps=["First octet = 130", "128 <= 130 <= 191", "Class B"],
  wrong="Class A ends at 126, Class C starts at 192 and Class D (224-239) is for multicast.", seconds=20,
  computed=True)
Q(T, "OSI and TCP/IP", "Intermediate",
  "A technician runs ping 127.0.0.1 on a branch PC whose network cable is unplugged, and gets replies. What does "
  "this test check?",
  ["That the PC's own TCP/IP software works, because 127.0.0.1 is the loopback address that refers to the computer "
   "itself", "That the branch router is working", "That the internet connection is working",
   "That the DNS server is reachable"],
  concept="Loopback address",
  explanation="127.0.0.1 (the 127.0.0.0/8 block, also called localhost) is the loopback address: packets sent to it "
              "never leave the computer. Replies show that the local TCP/IP stack is working, even without a "
              "cable.",
  steps=["127.0.0.1 = this computer (loopback)", "No cable needed", "Tests the local TCP/IP stack"],
  wrong="With the cable unplugged nothing outside the PC can be reached, so the router, the internet and the DNS "
        "server are not being tested.", seconds=20)
Q(T, "Devices", "Intermediate",
  "All branch PCs reach websites through one server that receives their web requests, forwards them to the "
  "internet on their behalf, keeps copies of frequently visited pages to serve them faster, and blocks sites "
  "banned by the bank. What is this server called?",
  ["Proxy server", "DHCP server", "Mail server", "Database server"],
  concept="Proxy servers",
  explanation="A (forward) proxy server is an intermediary for client requests. It can cache content, filter "
              "sites, log access and hide internal addresses from the internet.",
  steps=["Forwards requests on behalf of clients + caching + filtering = proxy"],
  wrong="A DHCP server hands out IP settings. A mail server handles email. A database server stores and queries "
        "data.", seconds=20)

# ================================================================ 9. Cybersecurity (2 / 5 / 2)
T = "Cybersecurity"
Q(T, "Phishing and social engineering", "Basic",
  "A customer sees a padlock icon next to the address of a website that looks like her bank's login page. What "
  "does the padlock actually confirm?",
  ["That the connection between her browser and that website is encrypted (HTTPS); it does not prove the site is "
   "genuinely her bank's", "That the website belongs to her bank and is safe to use",
   "That the website has been checked by the RBI", "That the site cannot contain any malware"],
  concept="HTTPS and phishing sites",
  explanation="The padlock means the site uses HTTPS with a valid certificate for the address shown, so data in "
              "transit is encrypted. Phishing sites can also get certificates for their own look-alike domains, so "
              "the customer must still check the exact domain name.",
  steps=["Padlock = encrypted connection to that domain", "Still check the domain itself"],
  wrong="Fraudsters can obtain certificates for fake domains, so the padlock alone proves neither ownership nor "
        "safety. The RBI does not certify websites through the padlock.", seconds=20)
Q(T, "Malware", "Basic",
  "Why must the antivirus software on branch PCs download updates every day?",
  ["To get the latest virus definitions (signatures) so that it can recognise newly discovered malware",
   "To increase the PC's RAM", "To make the internet connection faster", "To renew the Windows licence"],
  concept="Antivirus updates",
  explanation="Signature-based antivirus compares files against a database of known malware patterns. New malware "
              "appears daily, so the database (definitions) must be updated to detect it.",
  steps=["New malware every day", "Updated definitions = detection of new threats"],
  wrong="Antivirus updates do not add RAM, speed up the internet or renew licences of other software.", seconds=15)
Q(T, "Phishing and social engineering", "Intermediate",
  "At an airport, a traveller sees two open Wi-Fi networks: 'Airport_Free_WiFi' (genuine) and an identically named "
  "one with a stronger signal that a criminal is broadcasting from a laptop to capture users' traffic and login "
  "details. What is the criminal's access point called?",
  ["Evil twin", "Honeypot", "Botnet", "Logic bomb"],
  concept="Wireless attacks",
  explanation="An evil twin is a rogue Wi-Fi access point that copies the name of a legitimate network so that "
              "users connect to it, letting the attacker intercept or alter their traffic (a man-in-the-middle "
              "position).",
  steps=["Fake access point with the same name = evil twin"],
  wrong="A honeypot is a decoy system set up by defenders to attract attackers. A botnet is a network of infected "
        "computers. A logic bomb is code that triggers on a condition.", seconds=20)
Q(T, "Encryption and authentication", "Advanced",
  "A bank lets customers sign in with passkeys (FIDO credentials) instead of passwords. Why do passkeys resist "
  "phishing far better than passwords, even if a customer opens a perfect copy of the bank's site?",
  ["The passkey is tied to the bank's real site and works by a public-key challenge-response, so there is no "
   "shared secret the customer could type into a fake site", "Passkeys are long passwords that are hard to guess",
   "Passkeys are sent by SMS for every login", "Passkeys encrypt the customer's password before sending it"],
  concept="Phishing-resistant authentication",
  explanation="With a passkey, the device holds a private key for that account and service; the server stores only "
              "the public key. At sign-in the device signs a challenge, and the credential is used only with the "
              "service it was created for. There is no password to reveal, so a look-alike site gets nothing "
              "reusable.",
  steps=["Private key stays with the user's device; server has the public key",
         "Login = signed challenge, bound to the real site", "No shared secret to phish"],
  wrong="Passkeys are not passwords at all. They do not use SMS codes. They do not involve sending an encrypted "
        "password.", seconds=35,
  facts=[fact("FIDO Alliance: passkeys are phishing resistant and secure by design; they are tied to a user's "
              "account on a website or app, use public-key challenge-response, and have no shared secrets.",
              FIDO_PASSKEYS)])
Q(T, "Encryption and authentication", "Advanced",
  "A bank redesigns its security so that a device inside the head-office LAN is no longer trusted automatically: "
  "every request to every application must be authenticated and authorised, whatever network it comes from. Which "
  "security model is this?",
  ["Zero trust architecture", "Perimeter (castle-and-moat) security", "Security through obscurity",
   "Single sign-on"],
  concept="Zero trust",
  explanation="Zero trust assumes no implicit trust is granted to users or devices based only on their network "
              "location or ownership; access is decided per request using identity, device state and policy.",
  steps=["No trust from being 'inside' = zero trust"],
  wrong="Perimeter security trusts everything inside the firewall, which is exactly what is being removed. "
        "Obscurity relies on secrecy of design. Single sign-on is one login for many applications, not a trust "
        "model.", seconds=25,
  facts=[fact("NIST SP 800-207: zero trust assumes no implicit trust is granted to assets or user accounts based "
              "solely on their physical or network location or on asset ownership.", NIST_ZT)])

# ================================================================ 10. Database Fundamentals (2 / 2 / 4)
T = "Database Fundamentals"
S_TXN = new_stim(
    "data_table", "Txn table of a bank",
    "Table Txn (type D = deposit, W = withdrawal; ref_acc = the other account in a transfer, NULL for cash and "
    "ATM):\n\n| txn_id | acc_no | txn_date | type | channel | amount | ref_acc |\n|---|---|---|---|---|---|---|\n"
    + "\n".join(f"| {t} | {a} | {d} | {ty} | {ch} | {am} | {r or 'NULL'} |" for t, a, d, ty, ch, am, r in TXN),
    "Ordering by txn_date DESC, amount DESC puts T09 first. A11 net = 20000 - 1500 - 10000 = 8500. UPI accounts "
    "{A11, A13, A14} minus ATM accounts {A11, A12} = {A13, A14}. Largest transaction per account: 5 rows (A13 -> "
    "T04). NOT IN against a list containing NULL returns no rows.")
Q(T, "SQL basics", "Basic",
  "Refer to the Txn table. Which txn_id appears in the FIRST row of this query's result?\n\nSELECT txn_id FROM Txn "
  "ORDER BY txn_date DESC, amount DESC;", ["T09", "T10", "T01", "T05"],
  concept="ORDER BY with two keys",
  explanation="Rows are sorted by txn_date, newest first. Two rows share the latest date 2026-10-05 (T09, 7000 and "
              "T10, 2500); the second key, amount DESC, puts T09 first.",
  steps=["Latest date 2026-10-05: T09 and T10", "Tie broken by amount DESC: 7000 > 2500", "First row T09"],
  wrong="T10 would be first with amount ASC. T01 is the oldest date (first with txn_date ASC). T05 has the largest "
        "amount but an older date.", seconds=30, computed=True, stim=S_TXN, pos=1)
o, a = ordered(SQL_NET, [-8500, 18500, 31500])
Q(T, "SQL basics", "Intermediate",
  "Refer to the Txn table. What does this query return?\n\nSELECT SUM(CASE WHEN type = 'D' THEN amount ELSE "
  "-amount END) FROM Txn WHERE acc_no = 'A11';", o, a,
  concept="CASE expressions in aggregates",
  explanation="A11 has T01 (D, 20000), T03 (W, 1500) and T07 (W, 10000). CASE turns deposits positive and "
              "withdrawals negative: 20000 - 1500 - 10000 = 8500, the net change in A11's balance.",
  steps=["A11 rows: T01, T03, T07", "+20000 - 1500 - 10000", "= 8500"],
  wrong="31,500 adds all three amounts ignoring the type. -8,500 reverses the signs. 18,500 leaves out the ATM "
        "withdrawal T07.", seconds=45, computed=True, stim=S_TXN, pos=2)
o = ["A13 and A14", "A11, A13 and A14", "A11 and A12", "A13 only"]
Q(T, "SQL basics", "Intermediate",
  "Refer to the Txn table. Which accounts does this query return?\n\nSELECT acc_no FROM Txn WHERE channel = 'UPI'\n"
  "EXCEPT\nSELECT acc_no FROM Txn WHERE channel = 'ATM';", o,
  concept="EXCEPT (set difference)",
  explanation="The first query gives the accounts with UPI transactions: A11, A13, A14. The second gives accounts "
              "with ATM transactions: A12, A11. EXCEPT keeps the rows of the first result that are not in the "
              "second (and removes duplicates): A13 and A14.",
  steps=["UPI: {A11, A13, A14}", "ATM: {A11, A12}", "{A11, A13, A14} - {A11, A12} = {A13, A14}"],
  wrong="A11 also used an ATM, so it is removed. A11 and A12 are the ATM users (the reverse difference would give "
        "only A12). A13 only forgets A14's UPI transaction T10.", seconds=45, computed=True, stim=S_TXN, pos=3)
o = ["5 rows; for A13 it returns T04", "5 rows; for A13 it returns T08", "10 rows; for A13 it returns T04",
     "1 row: T05"]
Q(T, "SQL basics", "Advanced",
  "Refer to the Txn table. How many rows does this query return, and which txn_id does it give for account "
  "A13?\n\nSELECT acc_no, txn_id FROM (SELECT acc_no, txn_id, ROW_NUMBER() OVER (PARTITION BY acc_no ORDER BY "
  "amount DESC) AS rn FROM Txn) AS t WHERE rn = 1;", o,
  concept="Window functions: ROW_NUMBER with PARTITION BY",
  explanation="PARTITION BY acc_no numbers the rows separately within each account, largest amount first. rn = 1 "
              "keeps each account's largest transaction: one row per account. There are 5 accounts (A11-A15), so 5 "
              "rows. For A13 (T04 1500, T08 800) it returns T04.",
  steps=["One partition per acc_no: A11, A12, A13, A14, A15", "rn = 1 -> largest amount in each",
         "A13: T04 (1500) > T08 (800)"],
  wrong="T08 is A13's smaller transaction. 10 rows would mean no filtering by rn. A single row (T05 or T06, the "
        "largest overall) would need ROW_NUMBER without PARTITION BY.", seconds=60, computed=True, stim=S_TXN, pos=4)
o = ["No rows", "A15 only", "A12 and A15", "All five accounts"]
Q(T, "SQL basics", "Advanced",
  "Refer to the Txn table. An analyst wants the accounts that never appear as the other party (ref_acc) of any "
  "transaction, and writes:\n\nSELECT DISTINCT acc_no FROM Txn WHERE acc_no NOT IN (SELECT ref_acc FROM Txn);\n\n"
  "What does the query return?", o,
  concept="NOT IN with NULL values",
  explanation="The subquery returns A13, A11, A14, A12, A16 and also NULLs. For acc_no X, 'X NOT IN (..., NULL)' "
              "means X <> each value AND X <> NULL; any comparison with NULL is UNKNOWN, so the condition is never "
              "TRUE and no row is returned. Adding WHERE ref_acc IS NOT NULL in the subquery (or using NOT EXISTS) "
              "would give the intended answer, A15.",
  steps=["Subquery list contains NULL", "X <> NULL is UNKNOWN", "NOT IN can never be TRUE -> empty result"],
  wrong="A15 is what the analyst intended, but the NULLs prevent it. A12 does appear as ref_acc (T06). The query "
        "cannot return all accounts, because each one is compared with the same list.", seconds=60, computed=True,
  stim=S_TXN, pos=5)
Q(T, "DBMS concepts", "Basic",
  "A Customers table has 6 columns and 2,500 rows. In relational database terms, what is the number 2,500 called?",
  ["Cardinality of the relation", "Degree of the relation", "Domain of the relation", "Schema of the relation"],
  concept="Degree and cardinality",
  explanation="Cardinality is the number of tuples (rows) in a relation; degree is the number of attributes "
              "(columns). Here the cardinality is 2,500 and the degree is 6.",
  steps=["Rows = tuples = cardinality"],
  wrong="Degree is the number of columns (6). A domain is the set of allowed values of an attribute. The schema is "
        "the table's structure (name and columns).", seconds=15)
Q(T, "DBMS concepts", "Advanced",
  "Table Teaching(student, subject, faculty) records that each faculty member teaches only one subject, and each "
  "student has one faculty member per subject. Its candidate keys are {student, subject} and {student, faculty}. "
  "The dependency faculty -> subject holds, but faculty alone is not a candidate key. The table is in 3NF. Which "
  "normal form does it violate?",
  ["BCNF (Boyce-Codd Normal Form), because the determinant 'faculty' is not a super key",
   "First Normal Form, because it has a composite key", "Second Normal Form, because subject is a non-key "
   "attribute", "It violates no normal form"],
  concept="BCNF",
  explanation="BCNF requires that for every non-trivial functional dependency X -> Y, X is a super key. In "
              "faculty -> subject, faculty is not a super key. The table still satisfies 3NF because subject is a "
              "prime attribute (part of a candidate key), which 3NF allows but BCNF does not.",
  steps=["FD: faculty -> subject", "faculty is not a super key", "Subject is prime -> 3NF OK", "BCNF violated"],
  wrong="A composite key does not break 1NF (atomic values do). Subject is part of a candidate key, so it is not a "
        "non-key attribute and 2NF/3NF hold. The faculty -> subject dependency does violate BCNF.", seconds=50)
Q(T, "DBMS concepts", "Advanced",
  "Transaction T1 runs SELECT COUNT(*) FROM Loans WHERE branch = 'Pune' and gets 40. Before T1 finishes, T2 "
  "inserts a new Pune loan and commits. T1 runs the same query again and gets 41. What is this anomaly called?",
  ["Phantom read", "Dirty read", "Lost update", "Deadlock"],
  concept="Transaction isolation anomalies",
  explanation="A phantom read occurs when a transaction re-runs a query with a search condition and finds a "
              "different set of rows because another committed transaction inserted or deleted matching rows. "
              "The SERIALIZABLE isolation level prevents it.",
  steps=["Same condition, new row appears", "Inserted and committed by another transaction = phantom"],
  wrong="A dirty read reads uncommitted data, but T2 had committed. A lost update overwrites another update. A "
        "deadlock is two transactions waiting for each other's locks.", seconds=30)

# ================================================================ 11. MS Office (4 / 4 / 3)
T = "MS Office"
S_FD = new_stim(
    "data_table", "Excel fixed-deposit register",
    "Rows 2 to 9 of a branch's Excel sheet (row 1 holds the headings; dates are true Excel dates shown as "
    "dd-mmm-yyyy):\n\n| Row | A: Name | B: Branch | C: Deposit date | D: Amount (Rs) | E: Tenure (months) |\n"
    "|---|---|---|---|---|---|\n"
    + "\n".join(f"| {i} | {n} | {b} | {d:%d-%b-%Y} | {amt} | {ten} |" for i, (n, b, d, amt, ten) in
                enumerate(FD, start=2)),
    "Five rows are not Pune. Kiran's maturity date is 08-Mar-2027. The largest Delhi deposit with tenure under 36 "
    "months is 120,000. Agra and Nagpur occur exactly once. The last Ravi row (row 5) has 30,000.")
o, a = ordered(5, [3, 4, 8])
Q(T, "MS Excel", "Basic",
  "Refer to the fixed-deposit register. What does =COUNTIF(B2:B9, \"<>Pune\") return?", o, a,
  concept="COUNTIF with a 'not equal to' criterion",
  explanation="<> means 'not equal to'. Pune appears 3 times among the 8 branch cells, so 8 - 3 = 5 cells are not "
              "Pune (Delhi x 3, Agra, Nagpur).",
  steps=["Total cells = 8", "Pune = 3", "8 - 3 = 5"],
  wrong="3 counts the Pune rows themselves. 4 forgets one non-Pune row. 8 counts every row.", seconds=30,
  computed=True, stim=S_FD, pos=1)
o = ["08-Mar-2027", "08-Sep-2026", "08-Jun-2027", "17-Jun-2026"]
Q(T, "MS Excel", "Intermediate",
  "Refer to the fixed-deposit register. Cell F8 contains =EDATE(C8, E8) and is formatted as a date. What does it "
  "show?", o,
  concept="EDATE",
  explanation="EDATE(start_date, months) returns the date that is the given number of months after the start "
              "date. Row 8 is Kiran: 08-Jun-2026 plus 9 months = 08-Mar-2027, the maturity date.",
  steps=["Row 8: C8 = 08-Jun-2026, E8 = 9", "Add 9 months -> 08-Mar-2027"],
  wrong="08-Sep-2026 adds only 3 months. 08-Jun-2027 adds 12 months. 17-Jun-2026 adds 9 days instead of 9 months.",
  seconds=40, computed=True, stim=S_FD, pos=2,
  facts=[fact("Microsoft: EDATE returns the serial number of the date that is the indicated number of months "
              "before or after the start date.", MS_EDATE)])
o, a = ordered(120000, [90000, 200000, 0])
Q(T, "MS Excel", "Intermediate",
  "Refer to the fixed-deposit register. What does this formula return?\n\n=MAXIFS(D2:D9, B2:B9, \"Delhi\", E2:E9, "
  "\"<36\")", o, a,
  concept="MAXIFS with several criteria",
  explanation="MAXIFS(max_range, criteria_range1, criteria1, ...) returns the largest value among rows meeting "
              "all criteria. Delhi rows: Ravi 120000 (24 months), John 200000 (36), Kiran 90000 (9). Tenure < 36 "
              "excludes John. The maximum of 120000 and 90000 is 120000.",
  steps=["Delhi rows: 120000/24, 200000/36, 90000/9", "Keep tenure < 36: 120000, 90000", "Max = 120000"],
  wrong="200000 ignores the tenure condition (36 is not < 36). 90000 is the minimum, not the maximum. 0 would "
        "appear only if no row matched.", seconds=40, computed=True, stim=S_FD, pos=3,
  facts=[fact("Microsoft: MAXIFS(max_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...) returns "
              "the maximum among cells specified by the criteria.", MS_MAXIFS)])
o, a = ordered(2, [0, 4, 6])
Q(T, "MS Excel", "Advanced",
  "Refer to the fixed-deposit register. In Excel 365, what does this formula return?\n\n=ROWS(UNIQUE(B2:B9, , "
  "TRUE))", o, a,
  concept="UNIQUE with exactly_once",
  explanation="UNIQUE(array, [by_col], [exactly_once]). With exactly_once = TRUE it returns only the values that "
              "occur exactly once. Pune occurs 3 times, Delhi 3, Agra 1, Nagpur 1, so the result is {Agra; "
              "Nagpur} and ROWS gives 2.",
  steps=["Counts: Pune 3, Delhi 3, Agra 1, Nagpur 1", "exactly_once = TRUE -> Agra, Nagpur", "ROWS = 2"],
  wrong="4 is the number of distinct branches (exactly_once omitted or FALSE). 6 counts the rows of Pune and Delhi. "
        "0 would mean every branch repeats.", seconds=50, computed=True, stim=S_FD, pos=4,
  facts=[fact("Microsoft: UNIQUE's exactly_once = TRUE returns all distinct rows or columns that occur exactly once; "
              "FALSE or omitted returns all distinct ones.", MS_UNIQUE)])
o, a = ordered(30000, [120000, 150000, 0], fmt=lambda v: "None" if v == 0 else f"{v}")
Q(T, "MS Excel", "Advanced",
  "Refer to the fixed-deposit register. What does this formula return?\n\n=XLOOKUP(\"Ravi\", A2:A9, D2:D9, "
  "\"None\", 0, -1)", o, a,
  concept="XLOOKUP search mode",
  explanation="XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode]). "
              "match_mode 0 = exact match; search_mode -1 searches from the last item upwards. 'Ravi' is in rows 3 "
              "and 5; searching from the bottom finds row 5 first, whose amount is 30000.",
  steps=["Ravi in rows 3 (120000) and 5 (30000)", "search_mode -1 = last to first", "Row 5 -> 30000"],
  wrong="120000 is the first Ravi (default search_mode 1). 150000 adds both deposits, which XLOOKUP never does. "
        "'None' appears only if no Ravi exists.", seconds=50, computed=True, stim=S_FD, pos=5,
  facts=[fact("Microsoft: XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], "
              "[search_mode]); search_mode -1 performs a reverse search starting at the last item.", MS_XLOOKUP)])
Q(T, "Shortcuts", "Basic",
  "In MS Word, a clerk undoes a change with Ctrl + Z and then realises the change was correct after all. Which "
  "shortcut redoes the undone action?",
  ["Ctrl + Y", "Ctrl + R", "Ctrl + U", "Ctrl + D"],
  concept="Word shortcuts",
  explanation="Ctrl + Y redoes the last undone action (or repeats the last action if nothing was undone).",
  steps=["Undo = Ctrl + Z", "Redo = Ctrl + Y"],
  wrong="Ctrl + R right-aligns a paragraph, Ctrl + U underlines and Ctrl + D opens the Font dialog in Word.",
  seconds=10,
  facts=[fact("Microsoft: Ctrl+Y - Redo the previous action, if possible.", MS_WORD_KEYS)])
Q(T, "MS PowerPoint", "Basic",
  "A trainer wants to give participants printed copies of a 30-slide presentation with six small slides on each "
  "page and space to take notes. Which print layout should she choose in PowerPoint?",
  ["Handouts (6 slides per page)", "Full Page Slides", "Notes Pages", "Outline"],
  concept="Printing in PowerPoint",
  explanation="In File > Print, the Layout list offers Handouts with 1, 2, 3, 4, 6 or 9 slides per page, which "
              "puts several slide images on each sheet for the audience.",
  steps=["Several slides per sheet for audience = Handouts"],
  wrong="Full Page Slides prints one slide per page. Notes Pages prints one slide with the speaker's notes. Outline "
        "prints only the text.", seconds=15,
  facts=[fact("Microsoft: to print several slides per page, select one of the Handout options from the Layout list "
              "on the Print screen.", MS_HANDOUT)])
Q(T, "MS Excel", "Basic",
  "An Excel sheet lists 3,000 loan accounts from all branches. A manager wants to see only the rows for Pune for "
  "a moment, without deleting or moving the other rows. Which feature should she use?",
  ["Filter (AutoFilter) on the Branch column", "Sort the sheet by Branch", "Delete the other rows",
   "Merge & Center"],
  concept="Filtering data",
  explanation="A filter hides the rows that do not meet the chosen condition; they reappear when the filter is "
              "cleared. The data itself is not changed.",
  steps=["Show only matching rows, temporarily = Filter"],
  wrong="Sorting reorders all rows but still shows them. Deleting removes data permanently. Merge & Center "
        "combines cells for headings.", seconds=15)
Q(T, "Shortcuts", "Intermediate",
  "In MS Word, an officer wants the selected paragraph to line up evenly with both the left and the right margins, "
  "like a newspaper column. Which shortcut applies this alignment?",
  ["Ctrl + J", "Ctrl + E", "Ctrl + L", "Ctrl + R"],
  concept="Paragraph alignment shortcuts",
  explanation="Ctrl + J justifies the paragraph (adds space between words so lines reach both margins). Ctrl + E "
              "centres, Ctrl + L aligns left and Ctrl + R aligns right.",
  steps=["Both margins = justify = Ctrl + J"],
  wrong="Ctrl + E centres the text, Ctrl + L aligns it to the left margin only, Ctrl + R to the right only.",
  seconds=15,
  facts=[fact("Microsoft: Ctrl+J - Justify the paragraph.", MS_WORD_KEYS)])
Q(T, "MS Excel", "Intermediate",
  "In a loan sheet, the manager wants every EMI-due date that has already passed to turn red automatically, and to "
  "go back to normal if the date is corrected, without anyone colouring cells by hand. Which Excel feature should "
  "be used?",
  ["Conditional Formatting", "Data Validation", "Freeze Panes", "Format Painter"],
  concept="Conditional Formatting",
  explanation="Conditional Formatting applies a format (fill, font colour, icons) to cells only when a rule is true, "
              "for example 'cell value is less than =TODAY()', and updates as values change.",
  steps=["Format depends on a rule = Conditional Formatting"],
  wrong="Data Validation restricts what can be typed. Freeze Panes keeps headings visible. Format Painter copies "
        "fixed formatting once.", seconds=20)
Q(T, "MS Excel", "Advanced",
  "A clerk must be able to type only in the input cells B2:B6 of an EMI calculator; all formula cells must be "
  "protected from changes. She selects the whole sheet and clicks Protect Sheet, but now she cannot type in B2:B6 "
  "either. What should she have done first?",
  ["Removed the 'Locked' setting (Format Cells > Protection) from B2:B6, because every cell is locked by default "
   "and locking takes effect only when the sheet is protected",
   "Hidden the formula cells before protecting the sheet", "Saved the workbook as .csv",
   "Applied Data Validation to the formula cells"],
  concept="Locked cells and sheet protection",
  explanation="Every cell's Locked property is on by default, but it has no effect until the sheet is protected. "
              "To leave input cells editable, unlock them first (Format Cells > Protection > clear Locked) and then "
              "protect the sheet.",
  steps=["Default: all cells Locked", "Unlock B2:B6", "Then Protect Sheet"],
  wrong="Hiding formula cells does not make B2:B6 editable. CSV loses formulas and protection. Data Validation "
        "controls values, not protection.", seconds=40,
  facts=[fact("Microsoft: by default, protecting a worksheet locks all cells so none are editable; cells must be "
              "unlocked before the sheet is protected to stay editable.", MS_LOCK)])

# ================================================================ 12. Digital Payments (2 / 1 / 1)
T = "Digital Payments"
Q(T, "Payment technology", "Basic",
  "A farmer with a basic feature phone and no mobile internet wants to check his balance and send money. Which "
  "NPCI service lets him do this by dialling a short code and choosing from on-screen menus?",
  ["*99# (USSD-based mobile banking)", "UPI Lite", "NETC FASTag", "Internet banking"],
  concept="USSD banking",
  explanation="NPCI's *99# service uses USSD, which works on the voice/signalling channel of ordinary GSM phones, "
              "so it needs neither a smartphone nor mobile data.",
  steps=["Feature phone + no internet + dial a code = *99# USSD"],
  wrong="UPI Lite is a small-value wallet inside a UPI app. FASTag is for tolls. Internet banking needs internet "
        "access.", seconds=15,
  facts=[fact("NPCI's USSD-based mobile banking service (*99#) lets users do basic banking from any GSM handset "
              "without mobile internet.", NPCI_USSD)], web=SC)
Q(T, "Payment technology", "Basic",
  "Which UPI-based mobile payment app was developed by NPCI and launched on 30 December 2016?",
  ["BHIM", "RuPay", "AePS", "NEFT"],
  concept="NPCI products",
  explanation="BHIM (Bharat Interface for Money) is NPCI's own UPI app, launched on 30 December 2016, for sending "
              "and receiving money directly between bank accounts.",
  steps=["NPCI's UPI app from December 2016 = BHIM"],
  wrong="RuPay is NPCI's card network. AePS is Aadhaar-based payments at micro-ATMs. NEFT is an RBI-run "
        "funds-transfer system, not an app.", seconds=15,
  facts=[fact("NPCI: BHIM was launched on December 30, 2016 by the Prime Minister; it is NPCI's UPI-based app.",
              NPCI_BHIM)], web=SC)
Q(T, "Card security", "Intermediate",
  "A customer receives a new debit card and uses it at an ATM in her town without problems, but her first online "
  "shopping payment is declined. Under the RBI's January 2020 directions on card security, what is the most likely "
  "reason?",
  ["New cards are enabled only for domestic contact-based use (ATM and PoS); she must switch on online use through "
   "her bank's app, net banking or another channel the bank offers", "Debit cards can never be used online in India",
   "Online use is allowed only after six months", "She must first use the card for an international payment"],
  concept="Card usage controls",
  explanation="RBI (January 15, 2020) directed that cards be enabled at issue only for contact-based use at ATMs "
              "and PoS in India. Card-not-present (online), international and contactless use must be enabled by "
              "the customer, who can switch each channel on or off and set limits at any time.",
  steps=["New card -> domestic contact-based use only", "Online use off until enabled", "Enable via bank's "
                                                                                         "channels"],
  wrong="Debit cards can be used online once enabled. There is no six-month wait. International use is a separate "
        "switch and is not needed first.", seconds=30,
  facts=[fact("RBI (RBI/2019-20/142, 15 January 2020): cards shall be enabled for use only at contact-based points "
              "of usage within India at issue; issuers must provide a facility to switch on/off and set limits for "
              "online, international and contactless transactions.", RBI_CARDS)])
Q(T, "Payment technology", "Advanced",
  "A small shopkeeper displays one QR code that customers can scan to pay with apps linked to Visa, Mastercard or "
  "RuPay cards, and also with UPI apps. This interoperable QR standard, launched in India in February 2017 and "
  "developed with NPCI by the card networks, is called:",
  ["BharatQR", "UPI Lite X", "e-RUPI", "NETC"],
  concept="Interoperable QR payments",
  explanation="BharatQR is a common QR standard developed by NPCI with Mastercard and Visa (American Express and "
              "RuPay are supported), so one code accepts payments from different card networks; it is also "
              "interoperable with UPI.",
  steps=["One QR across card networks and UPI = BharatQR"],
  wrong="UPI Lite X is for offline UPI-Lite payments. e-RUPI is a purpose-specific prepaid voucher. NETC is the "
        "FASTag toll system.", seconds=20,
  facts=[fact("BharatQR was launched on 20 February 2017 as a common QR standard developed by NPCI, Mastercard and "
              "Visa, interoperable across RuPay, Mastercard, Visa and American Express and with UPI.", BHARATQR)],
  web=SC)

# ================================================================ 13. Computer Abbreviations (2 / 2 / 2)
T = "Computer Abbreviations"
S = "Common abbreviations"
Q(T, S, "Basic",
  "Each branch server is connected to a UPS so that it keeps running for a few minutes during a power cut. What "
  "does UPS stand for?",
  ["Uninterruptible Power Supply", "Universal Power Source", "Unified Processing System", "Uninterrupted Port "
                                                                                           "Switch"],
  concept="Hardware abbreviations",
  explanation="A UPS (Uninterruptible Power Supply) uses a battery to supply power instantly when the mains fails, "
              "giving time to save work and shut down safely.",
  steps=["UPS = Uninterruptible Power Supply"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Basic",
  "A branch PC stores its data on an HDD with spinning magnetic platters. What does HDD stand for?",
  ["Hard Disk Drive", "High Density Disc", "Hybrid Data Device", "Hard Data Directory"],
  concept="Storage abbreviations",
  explanation="HDD = Hard Disk Drive, a storage device that records data magnetically on rotating platters.",
  steps=["HDD = Hard Disk Drive"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Intermediate",
  "Merchants display QR codes for UPI payments. The QR code was invented in Japan in 1994. What does QR stand for?",
  ["Quick Response", "Quality Record", "Quick Reader", "Query Reference"],
  concept="Common abbreviations",
  explanation="QR stands for Quick Response: the 2D code was developed by Denso Wave (Masahiro Hara's team) and "
              "announced in 1994 with fast reading as its aim.",
  steps=["QR = Quick Response"], wrong="The other expansions are made up.", seconds=10,
  facts=[fact("DENSO WAVE: QR stands for 'quick response'; the QR Code was announced in 1994.", DENSO_QR)])
Q(T, S, "Intermediate",
  "Banks exchange some financial messages in XML, a text format with user-defined tags such as <Amount>. What does "
  "XML stand for?",
  ["Extensible Markup Language", "Extra Machine Language", "Executable Multi-Layer", "Extended Mail Link"],
  concept="Web and data abbreviations",
  explanation="XML (Extensible Markup Language) is a W3C standard for structured data in text form, where users "
              "define their own tags (unlike HTML's fixed tags).",
  steps=["XML = Extensible Markup Language"], wrong="The other expansions are made up.", seconds=10)
Q(T, S, "Advanced",
  "A bank's file server keeps working when one disk fails because its disks are combined in a RAID array. The "
  "1988 Berkeley paper that introduced the term used 'Inexpensive' for the letter I; what does RAID stand for in "
  "today's usage?",
  ["Redundant Array of Independent Disks", "Rapid Access Integrated Drive", "Random Allocation of Indexed Data",
   "Remote Array for Instant Duplication"],
  concept="Storage abbreviations",
  explanation="RAID first meant Redundant Arrays of Inexpensive Disks (Patterson, Gibson and Katz, 1988); the "
              "industry later changed it to Redundant Array of Independent Disks.",
  steps=["RAID = Redundant Array of Independent (originally Inexpensive) Disks"],
  wrong="The other expansions are made up.", seconds=15,
  facts=[fact("CHM: RAID stood for Redundant Arrays of Inexpensive Disks in the 1988 paper and was later changed to "
              "Redundant Array of Independent Disks.", CHM_RAID)])
Q(T, S, "Advanced",
  "A bank's applications check employees' user names, passwords and group memberships against a central directory "
  "service using the LDAP protocol. What does LDAP stand for?",
  ["Lightweight Directory Access Protocol", "Local Domain Authentication Process", "Layered Data Access Policy",
   "Logical Device Allocation Protocol"],
  concept="Network protocol abbreviations",
  explanation="LDAP (Lightweight Directory Access Protocol) is the standard protocol for reading and updating "
              "directory services such as Active Directory, often used for central login and user lookups.",
  steps=["LDAP = Lightweight Directory Access Protocol"], wrong="The other expansions are made up.", seconds=15,
  facts=[fact("RFC 4511 is titled 'Lightweight Directory Access Protocol (LDAP): The Protocol'.", RFC4511)])

# ---------------------------------------------------------------- checks and output
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_008_plan.json").read_text(encoding="utf-8"))
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

n_set = sum(1 for q in questions if q.get("stimulus_id"))
batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_008",
    "created_at": TODAY,
    "notes": f"BATCH_008 Computer Knowledge part: 100 original, mostly scenario-based questions (BANK_COMP_000703 to "
             f"BANK_COMP_000802), {n_set} of them in six shared sets (STIM_COMP_008001-008006: strong-room alarm "
             "logic circuit, PC specification sheet, command prompt with ipconfig/tracert, web-server access log, "
             "Txn table for SQL, Excel fixed-deposit register). Computable answers are re-derived in "
             "tools/batch_008/computer.py (logic circuit brute-forced over 16 inputs; SQL run in sqlite3; Excel "
             "results, DHCP T1, Base64 length, binary search and address splits recomputed). Facts from Microsoft, "
             "RFC, MDN, OWASP, man7, NIST, FIDO Alliance, RBI, DENSO WAVE, Google and Computer History Museum pages "
             "were checked on 2026-11-05; *99#, BHIM and BharatQR were confirmed from search results only "
             "(web:search-confirmed).",
    "stimuli": stimuli,
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_008_COMP.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions, keys {dict(sorted(keys.items()))})")
