"""Audits every missing-number series question for a second rule that lands on another option.

A missing-number series question is broken when some other common rule explains the series just as well with a wrong
option in the gap. For each option this fills the gap (anywhere in the series, not only at the end) and asks a library
of common rules whether the completed series fits. It prints questions where a wrong option also fits some rule, and,
separately, questions whose keyed answer fits no library rule (not an error: the library is not exhaustive). It
reports; it never edits.

    python tools/series_audit.py batches/BATCH_000_sample.json batches/parts/BATCH_0*_QUANT.json
"""

import json
import re
import sys
from fractions import Fraction as F

NUM = re.compile(r"-?\d[\d,]*(?:\.\d+)?|\?")


def parse(text):
    """The series: the first line holding a '?' and at least four numbers. Returns a list with None at the gap."""
    for line in text.replace("−", "-").splitlines():  # the bank writes negatives with a Unicode minus
        body = line.split(":", 1)[-1] if ":" in line else line
        body = re.sub(r"^[^0-9?-]*", "", body)
        toks = [t for t in re.split(r",\s+|\s+", body.strip().rstrip(".")) if t]
        if "?" not in toks:
            continue
        vals = []
        for t in toks:
            if t == "?":
                vals.append(None)
            elif re.fullmatch(r"-?\d[\d,]*(?:\.\d+)?", t):
                vals.append(F(t.replace(",", "")))
            else:
                vals = []
                break
        if len(vals) >= 5 and vals.count(None) == 1:
            return vals
    return None


def rules(s):
    """Names of library rules that explain every term of the complete series s."""
    n, out = len(s), []
    d1 = [s[i + 1] - s[i] for i in range(n - 1)]
    d2 = [d1[i + 1] - d1[i] for i in range(n - 2)]
    if len(set(d1)) == 1:
        out.append("constant difference")
    if len(set(d2)) == 1:
        out.append("constant second difference")
    d3 = [d2[i + 1] - d2[i] for i in range(n - 3)]
    if n >= 6 and len(set(d3)) == 1:
        out.append("constant third difference")
    if all(x != 0 for x in d1[:-1]) and len({d1[i + 1] / d1[i] for i in range(n - 2)}) == 1:
        out.append("differences in geometric progression")
    if all(x != 0 for x in s[:-1]) and len({s[i + 1] / s[i] for i in range(n - 1)}) == 1:
        out.append("constant ratio")
    if s[1] != s[0]:
        a = (s[2] - s[1]) / (s[1] - s[0])
        b = s[1] - a * s[0]
        if all(s[i + 1] == a * s[i] + b for i in range(n - 1)):
            out.append(f"x*{a}+{b}")
    for m0 in range(-3, 7):
        for dm in (0, 1, -1, 2):
            for c0 in range(-12, 13):
                for dc in (0, 1, -1, 2, -2, 3):
                    if (dm, dc) != (0, 0) and all(s[i + 1] == s[i] * (m0 + dm * i) + c0 + dc * i for i in range(n - 1)):
                        out.append(f"x*({m0}+{dm}k)+({c0}+{dc}k)")
    # x(k+1) = x(k) * r(k) where r steps arithmetically (×0.5, ×1, ×1.5 ...)
    if all(x != 0 for x in s[:-1]):
        r = [s[i + 1] / s[i] for i in range(n - 1)]
        if len({r[i + 1] - r[i] for i in range(n - 2)}) == 1:
            out.append("ratio steps arithmetically")
    if all(s[i] == s[i - 1] + s[i - 2] for i in range(2, n)):
        out.append("sum of previous two")
    if all(s[i] == s[i - 1] + s[i - 2] + s[i - 3] for i in range(3, n)):
        out.append("sum of previous three")
    if all(s[i] == 2 * s[i - 1] + s[i - 2] for i in range(2, n)):
        out.append("2*previous + one before")
    forms = {"k^2": lambda k: k * k, "k^3": lambda k: k ** 3, "2^k": lambda k: 2 ** k, "3^k": lambda k: 3 ** k,
             "k^2+k": lambda k: k * k + k, "k^3+k": lambda k: k ** 3 + k, "2^k+k": lambda k: 2 ** k + k,
             "2^k+k^2": lambda k: 2 ** k + k * k, "k^3-k": lambda k: k ** 3 - k, "k^2-1": lambda k: k * k - 1,
             "k^k": lambda k: k ** k, "k!": lambda k: __import__("math").factorial(k)}
    for name, g in forms.items():
        for base in (0, 1, 2):
            for scale in (1, 2, 3):
                off = s[0] - scale * g(base)
                if all(s[i] == scale * g(i + base) + off for i in range(n)):
                    out.append(f"{scale}*{name}+{off} (k from {base})")
    if n >= 6:
        ev, od = s[0::2], s[1::2]
        ap = lambda t: len({t[i + 1] - t[i] for i in range(len(t) - 1)}) == 1
        gp = lambda t: 0 not in t[:-1] and len({t[i + 1] / t[i] for i in range(len(t) - 1)}) == 1
        if (ap(ev) or gp(ev)) and (ap(od) or gp(od)):
            out.append("two interleaved series")
    return out


def main(paths):
    checked, unparsed, suspects, unknown = 0, [], [], []
    for p in paths:
        for q in json.load(open(p, encoding="utf-8"))["questions"]:
            if q.get("topic") != "Number Series":
                continue
            s = parse(q["question_text"])
            if not s:
                unparsed.append(q["question_id"])
                continue
            checked += 1
            gap = s.index(None)
            fits = {}
            for o in q["options"]:
                t = o["text"].replace(",", "").strip()
                if re.fullmatch(r"-?\d+(?:\.\d+)?", t):
                    filled = s[:gap] + [F(t)] + s[gap + 1:]
                    fits[o["key"]] = rules(filled)
            key = q["correct_answer"]
            wrong = {k: v for k, v in fits.items() if k != key and v}
            if wrong:
                suspects.append(f"{q['question_id']} key {key}: "
                                + "; ".join(f"option {k} fits {', '.join(v[:2])}" for k, v in wrong.items()))
            elif not fits.get(key):
                unknown.append(q["question_id"])
    for line in suspects:
        print("SUSPECT", line)
    print(f"checked {checked} missing-number series questions: {len(suspects)} suspect(s); "
          f"{len(unknown)} keyed answers use a rule outside the library (fine); unparsed: {unparsed or 'none'}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
