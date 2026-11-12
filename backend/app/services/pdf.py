"""PDF rendering for reports and GST invoices (reportlab).

Fonts: drop Noto font files (e.g. NotoSans-Regular.ttf, NotoSansDevanagari-Regular.ttf, NotoSansTamil-Regular.ttf)
into FONTS_DIR and they are picked per language. Without them Helvetica is used, which only covers Latin script.
Known limitation: reportlab does not shape complex Indic scripts (conjuncts may render imperfectly). For launch,
render Indic PDFs with a HarfBuzz-based engine (e.g. headless Chromium or WeasyPrint) behind this same module.
"""

import io
from functools import lru_cache
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from xml.sax.saxutils import escape

from app.config import get_settings

FONT_FILES = {
    "deva": ["NotoSansDevanagari-Regular.ttf"],  # hi mr ne kok mai sa doi brx
    "beng": ["NotoSansBengali-Regular.ttf"],  # bn as
    "taml": ["NotoSansTamil-Regular.ttf"],
    "telu": ["NotoSansTelugu-Regular.ttf"],
    "knda": ["NotoSansKannada-Regular.ttf"],
    "mlym": ["NotoSansMalayalam-Regular.ttf"],
    "gujr": ["NotoSansGujarati-Regular.ttf"],
    "guru": ["NotoSansGurmukhi-Regular.ttf"],
    "orya": ["NotoSansOriya-Regular.ttf"],
    "arab": ["NotoNastaliqUrdu-Regular.ttf", "NotoNaskhArabic-Regular.ttf"],  # ur sd ks
    "olck": ["NotoSansOlChiki-Regular.ttf"],
    "mtei": ["NotoSansMeeteiMayek-Regular.ttf"],
    "latn": ["NotoSans-Regular.ttf"],
}
SCRIPT_OF = {
    "hi": "deva", "mr": "deva", "ne": "deva", "kok": "deva", "mai": "deva", "sa": "deva", "doi": "deva",
    "brx": "deva", "bn": "beng", "as": "beng", "ta": "taml", "te": "telu", "kn": "knda", "ml": "mlym",
    "gu": "gujr", "pa": "guru", "or": "orya", "ur": "arab", "sd": "arab", "ks": "arab", "sat": "olck",
    "mni": "mtei", "en": "latn",
}


@lru_cache
def font_for(language: str) -> str:
    script = SCRIPT_OF.get(language, "latn")
    folder = Path(get_settings().fonts_dir)
    for name in FONT_FILES[script]:
        path = folder / name
        if path.exists():
            font_name = f"Noto-{script}"
            pdfmetrics.registerFont(TTFont(font_name, str(path)))
            return font_name
    return "Helvetica"


def _styles(language: str):
    font = font_for(language)
    base = getSampleStyleSheet()
    rtl = SCRIPT_OF.get(language) == "arab"
    align = 2 if rtl else 0
    return {
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName=font, alignment=align),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName=font, alignment=align),
        "p": ParagraphStyle("p", parent=base["BodyText"], fontName=font, leading=14, alignment=align),
        "small": ParagraphStyle("s", parent=base["BodyText"], fontName=font, fontSize=8, textColor=colors.grey),
    }


def _p(text, style) -> Paragraph:
    return Paragraph(escape(str(text if text is not None else "")), style)


def _table(rows: list[list], widths=None) -> Table:
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2f7")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


DISCLAIMER = ("Mock test based on the public exam pattern. Not affiliated with SSC, UPSC, IBPS, NTA or any exam body. "
              "Questions and feedback are AI-generated and reviewed for accuracy.")


def exam_report_pdf(*, app_name: str, exam_name: str, language: str, analytics: dict, report: dict) -> bytes:
    st = _styles(language)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, title=f"{exam_name} report")
    acc = analytics.get("accuracy")
    pct = analytics.get("percentile")
    flow = [
        _p(f"{app_name} - {exam_name}", st["h1"]),
        _p(report.get("summary", ""), st["p"]), Spacer(1, 6),
        _table([["Score", "Accuracy", "Percentile", "Attempted", "Negative marks lost", "Time (min)"],
                [f"{analytics['score']} / {analytics['max_score']}", f"{round((acc or 0) * 100)}%",
                 "-" if pct is None else f"{pct}", analytics["attempted"], analytics["negative_marks_lost"],
                 round(analytics["total_time_sec"] / 60, 1)]]),
        Spacer(1, 8), _p("Sections", st["h2"]),
        _table([["Section", "Score", "Correct", "Wrong", "Skipped", "Accuracy"]] + [
            [s["name"], f"{s['score']} / {s['max_score']}", s["correct"], s["wrong"], s["unanswered"],
             "-" if s["accuracy"] is None else f"{round(s['accuracy'] * 100)}%"] for s in analytics["sections"]]),
    ]
    for title, key in (("Strengths", "strengths"), ("Weaknesses", "weaknesses"), ("Loopholes", "loopholes")):
        flow += [Spacer(1, 8), _p(title, st["h2"])]
        for item in report.get(key, []):
            refs = item.get("question_refs")
            head = item.get("topic") or item.get("pattern", "")
            suffix = f" (questions {', '.join(map(str, refs))})" if refs else ""
            flow.append(_p(f"{head}: {item.get('detail', '')}{suffix}", st["p"]))
    flow += [Spacer(1, 8), _p("Smart shortcuts", st["h2"])]
    for s in report.get("shortcuts", []):
        flow.append(_p(f"Q{s['question_ref']} - {s['technique']}: {s['explanation']}", st["p"]))
    flow += [Spacer(1, 8), _p("7-day plan", st["h2"])]
    for d in report.get("study_plan", []):
        flow.append(_p(f"Day {d['day']}: {d['focus']} - {'; '.join(d.get('tasks', []))}", st["p"]))
    nt = report.get("next_test") or {}
    if nt.get("name") or nt.get("exam_slug"):
        flow += [Spacer(1, 8), _p(f"Next test: {nt.get('name') or nt.get('exam_slug')} - {nt.get('reason', '')}", st["p"])]
    flow += [Spacer(1, 12), _p(DISCLAIMER, st["small"])]
    doc.build(flow)
    return buf.getvalue()


def interview_report_pdf(*, app_name: str, role_name: str, language: str, report: dict) -> bytes:
    st = _styles(language)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, title=f"{role_name} interview")
    flow = [_p(f"{app_name} - {role_name} mock interview", st["h1"]), _p(report.get("summary", ""), st["p"]),
            Spacer(1, 6),
            _table([["Criterion", "Score (1-10)", "Why"]] + [
                [s["label"], s["score"], _p(s.get("justification", ""), st["p"])] for s in report.get("scores", [])],
                widths=[45 * mm, 25 * mm, 105 * mm])]
    vm = report.get("voice_metrics")
    if vm:
        flow += [Spacer(1, 6), _p(f"Speaking pace: {vm.get('words_per_minute')} words/min - "
                                  f"filler words: {vm.get('filler_count')}", st["p"])]
    flow += [Spacer(1, 8), _p("Answer by answer", st["h2"])]
    for q in report.get("per_question", []):
        flow += [_p(f"Q: {q.get('question', '')}", st["p"]), _p(f"Good: {q.get('good', '')}", st["p"]),
                 _p(f"Missing: {q.get('missing', '')}", st["p"]), _p(f"Model answer: {q.get('model_answer', '')}", st["p"]),
                 Spacer(1, 4)]
    flow += [_p("Red flags", st["h2"])] + [_p(f"- {r}", st["p"]) for r in report.get("red_flags", [])]
    flow += [Spacer(1, 8), _p("7-day practice plan", st["h2"])]
    for d in report.get("study_plan", []):
        flow.append(_p(f"Day {d['day']}: {d['focus']} - {'; '.join(d.get('tasks', []))}", st["p"]))
    flow += [Spacer(1, 12), _p("AI-generated feedback for practice purposes.", st["small"])]
    doc.build(flow)
    return buf.getvalue()


def invoice_pdf(*, order, plan_name: str, buyer_name: str | None, buyer_state: str | None) -> bytes:
    s = get_settings()
    st = _styles("en")
    total = order.amount_paise / 100
    gst = order.gst_amount_paise / 100
    taxable = round(total - gst, 2)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, title=f"Invoice {order.invoice_no}")
    flow = [
        _p("Tax Invoice", st["h1"]),
        _p(f"{s.company_legal_name}" + (f" - GSTIN {s.gstin}" if s.gstin else " - GSTIN: to be configured"), st["p"]),
        _p(f"Invoice no: {order.invoice_no}    Date: {order.paid_at:%d %b %Y}", st["p"]),
        _p(f"Billed to: {buyer_name or 'Customer'}" + (f", {buyer_state}" if buyer_state else ""), st["p"]),
        Spacer(1, 6),
        _table([["Description", "SAC", "Taxable value (₹)", f"GST {s.gst_rate_percent}% (₹)", "Total (₹)"],
                [plan_name, "999293", f"{taxable:.2f}", f"{gst:.2f}", f"{total:.2f}"]]),
        Spacer(1, 6),
        _p("Prices are inclusive of GST. CGST/SGST or IGST split depends on the place of supply and is applied once "
           "the GSTIN and state are configured.", st["small"]),
        _p(f"Payment reference: {order.gateway} {order.gateway_payment_id or ''}", st["small"]),
    ]
    doc.build(flow)
    return buf.getvalue()


def study_material_pdf(*, app_name: str, title: str, language: str, payload: dict) -> bytes:
    """Notes, formula sheets, topic decks, deep dives and mistake summaries as a printable PDF.

    Walks the JSON generically: keys become headings, lists become bullets, 2-D lists become tables. Mermaid
    diagrams are printed as their source (the app draws them; a server-side Mermaid renderer can replace this)."""
    st = _styles(language)
    mono = ParagraphStyle("mono", parent=st["p"], fontName="Courier", fontSize=8, leading=10,
                          backColor=colors.HexColor("#f6f8fa"))
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, title=title)
    flow = [_p(f"{app_name} - {title}", st["h1"])]

    def label(k: str) -> str:
        return k.replace("_", " ").strip().capitalize()

    def walk(value, depth=0):
        if isinstance(value, dict):
            if value.get("type") == "mermaid" and value.get("mermaid"):
                flow.append(Paragraph(escape(value["mermaid"]).replace("\n", "<br/>"), mono))
                if value.get("caption"):
                    flow.append(_p(value["caption"], st["small"]))
                return
            if value.get("type") == "table" and value.get("table"):
                flow.append(_table(value["table"]))
                return
            for k, v in value.items():
                if k in ("type", "mermaid", "table") or v in ("", None, [], {}):
                    continue
                if isinstance(v, (str, int, float)):
                    flow.append(_p(f"{label(k)}: {v}", st["p"]))
                else:
                    flow.append(_p(label(k), st["h2"]))
                    walk(v, depth + 1)
        elif isinstance(value, list):
            if value and all(isinstance(r, list) for r in value):
                flow.append(_table(value))
                return
            for i, item in enumerate(value, 1):
                if isinstance(item, (str, int, float)):
                    flow.append(_p(f"• {item}", st["p"]))
                else:
                    flow.append(Spacer(1, 4))
                    walk(item, depth + 1)
        elif value not in ("", None):
            flow.append(_p(value, st["p"]))

    walk({k: v for k, v in payload.items() if k != "title"})
    flow += [Spacer(1, 12), _p(DISCLAIMER, st["small"])]
    doc.build(flow)
    return buf.getvalue()
