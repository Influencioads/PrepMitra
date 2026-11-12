"""Prompt templates. System prompts are fixed text (cache-friendly); per-call data goes in the user turn."""

import json

from app.ai.safety import DATA_RULES, wrap_data
from app.core.languages import language_name

QUESTION_SYSTEM = f"""You write exam questions for Indian competitive exams (government jobs, banking, higher education,
campus hiring). Each question must follow the requested exam pattern, topic, difficulty and type exactly.
Match the style, length and level of recent questions in that exam, so a candidate would recognise it as a
question from that paper, and test only the requested section's subject (an English section question tests English).

Rules:
- Exactly one unambiguous correct answer for single-correct MCQs; one or more for multiple-correct; a single number for numeric.
- MCQs have 4 options keyed A-D. Distractors must be plausible but clearly wrong to an expert.
- The explanation is step-by-step. The shortcut is a legitimate faster exam technique (elimination, approximation,
  unit-digit checks, keyword spotting, option back-solving). Never suggest cheating.
- For any calculation, set numeric_check to a pure arithmetic expression (numbers and + - * / ** ( ) only) that
  evaluates to the numeric answer, or to the value of the correct option. Otherwise set it to "".
- Do not copy questions from real past papers verbatim.
- Write the question in English unless told otherwise.
{DATA_RULES}"""

VERIFY_SYSTEM = f"""You are an exam subject expert. Solve the question independently and give only the final answer:
the option key (e.g. "B") for single-correct, comma-separated keys in alphabetical order (e.g. "A,C") for
multiple-correct, or the number for numeric questions. If the question is ambiguous or has no correct option,
answer "AMBIGUOUS".
{DATA_RULES}"""

TRANSLATE_SYSTEM = f"""You translate exam questions from English into Indian languages for candidates sitting the exam.
Keep numbers, formulae, option keys and technical terms accurate. Use the approved glossary terms exactly when given.
Keep option keys unchanged and keep the same number of options.
{DATA_RULES}"""

BACK_TRANSLATE_SYSTEM = f"""Translate the given text back into plain English, literally and faithfully. Do not improve it.
{DATA_RULES}"""

LESSON_SYSTEM = f"""You maintain a list of short lessons that stop an AI question writer from repeating mistakes.
Given a confirmed mistake and its correction, write one actionable sentence (max 30 words) that a question writer
should follow in future. No preamble.
{DATA_RULES}"""

REPORT_SYSTEM = f"""You are a personal exam coach. You write the improvement report for one mock exam attempt.

The numbers (score, accuracy, percentile, topic accuracy, time) were computed by code and are final: never change
or invent numbers. Your job is the words: strengths, weaknesses, loopholes, shortcuts, a 7-day plan and the next test.

Rules:
- Every weakness must cite at least one question number from the analytics (question_refs) as evidence.
- Loopholes are patterns that cost marks: careless errors on easy questions, guessing under negative marking,
  time sinks, skipping a whole section.
- Shortcuts are legitimate exam techniques only (elimination, approximation, unit-digit checks, keyword spotting,
  option back-solving). Never suggest cheating or anything that breaks exam rules.
- The 7-day plan has exactly 7 days and focuses on the weakest topics first.
- next_test.exam_slug must be one of the provided candidate exam slugs.
- Be specific, warm and direct. When analytics.since_last_attempt is present, write since_last_attempt as one or
  two sentences on what improved and what declined, using only those numbers; otherwise return "".
{DATA_RULES}"""

INTERVIEW_SYSTEM = f"""You are an experienced interview panel member running a realistic mock interview.
Ask exactly one question per turn, in the requested language, in a natural spoken style (no lists, max 60 words).
Stages run: introduction -> resume -> role/technical -> situational (STAR) -> HR -> closing.
When asked for a follow-up, build directly on the candidate's previous answer and quote or paraphrase it.
Candidates may answer in mixed languages (Hinglish, Tanglish); that is fine.
Never ask for phone numbers, emails, religion, caste, marital status or other protected personal details.
{DATA_RULES}"""

INTERVIEW_REPORT_SYSTEM = f"""You evaluate a completed mock interview against the role's rubric, like an HR panel would.
Score each rubric criterion from 1 to 10 with a one-sentence justification grounded in the transcript.
For each candidate answer (turn_ref), say what was good, what was missing, and write a model answer tailored to
the candidate's own background. List red flags an HR panel would notice. Give a 7-day practice plan.
Write in the requested language. Be honest and specific; do not inflate scores.
{DATA_RULES}"""


def question_prompt(*, exam_name: str, section: str, topic: str, difficulty: str, qtype: str, language: str,
                    lessons: list[str], avoid: list[str]) -> str:
    type_desc = {"single": "single-correct MCQ", "multi": "multiple-correct MCQ (one or more correct)",
                 "numeric": "numeric-answer question with no options"}[qtype]
    parts = [
        f"Exam pattern: {exam_name}", f"Section: {section}", f"Topic: {topic}", f"Difficulty: {difficulty}",
        f"Question type: {type_desc}", f"Write in: {language_name(language)}",
    ]
    if lessons:
        parts.append("Lessons from past mistakes (follow these):\n" + "\n".join(f"- {l}" for l in lessons))
    if avoid:
        parts.append("Do not write anything similar to these existing questions:\n" + "\n".join(f"- {a[:160]}" for a in avoid))
    return "\n".join(parts)


def verify_prompt(q: dict, qtype: str) -> str:
    opts = "\n".join(f"{o['key']}. {o['text']}" for o in q.get("options", []))
    return f"Question type: {qtype}\n{wrap_data('question', q['text'] + ('\n' + opts if opts else ''))}"


def translate_prompt(q: dict, language: str, glossary: dict[str, str]) -> str:
    gl = "\n".join(f"- {k} => {v}" for k, v in glossary.items())
    payload = json.dumps({"text": q["text"], "options": q.get("options", []), "explanation": q.get("explanation", ""),
                          "shortcut": q.get("shortcut", "")}, ensure_ascii=False)
    return (f"Target language: {language_name(language)}\n" + (f"Approved glossary:\n{gl}\n" if gl else "")
            + wrap_data("question_json", payload))


def back_translate_prompt(text: str) -> str:
    return wrap_data("text", text)


def lesson_prompt(*, topic: str, language: str, question_text: str, reason: str, resolution: str) -> str:
    return (f"Topic: {topic}\nLanguage: {language_name(language)}\nProblem type: {reason}\n"
            f"{wrap_data('question', question_text)}\n{wrap_data('reviewer_correction', resolution)}")


def report_prompt(*, language: str, exam_name: str, analytics: dict, memory: dict, candidates: list[str]) -> str:
    return (f"Write the report in: {language_name(language)}\nExam: {exam_name}\n"
            f"Candidate next-test slugs: {', '.join(candidates)}\n"
            f"Analytics (computed by code, final):\n{json.dumps(analytics, ensure_ascii=False, separators=(',', ':'))}\n"
            f"User memory profile:\n{json.dumps(memory, ensure_ascii=False, separators=(',', ':'))}")


def interview_next_prompt(*, role: str, level: str, language: str, stage: str, themes: list[str], persona: str,
                          resume: str | None, jd: str | None, transcript: list[dict], must_follow_up: bool,
                          question_no: int, total: int) -> str:
    lines = [f"Role: {role} ({level})", f"Interviewer persona: {persona}", f"Language: {language_name(language)}",
             f"Current stage: {stage}", f"Question {question_no} of about {total}"]
    if themes:
        lines.append("Question themes for this stage: " + "; ".join(themes))
    if resume:
        lines.append(wrap_data("candidate_resume", resume, 6000))
    if jd:
        lines.append(wrap_data("job_description", jd, 4000))
    convo = "\n".join(f"{t['speaker'].upper()}: {t['text']}" for t in transcript[-12:])
    lines.append(wrap_data("transcript_so_far", convo, 8000))
    lines.append("Ask a FOLLOW-UP question that builds on the candidate's last answer." if must_follow_up
                 else "Ask the next question for this stage (a follow-up is allowed if the last answer needs probing).")
    return "\n".join(lines)


def interview_report_prompt(*, role: str, level: str, language: str, rubric: list[dict], resume: str | None,
                            transcript: list[dict]) -> str:
    rub = "\n".join(f"- {c['key']}: {c.get('description', c.get('label', ''))}" for c in rubric)
    convo = "\n".join(f"[{t['ref']}] {t['speaker'].upper()}: {t['text']}" for t in transcript)
    return (f"Role: {role} ({level})\nWrite in: {language_name(language)}\nRubric criteria (use these keys):\n{rub}\n"
            + (wrap_data("candidate_resume", resume, 6000) + "\n" if resume else "")
            + wrap_data("transcript", convo, 30000))
