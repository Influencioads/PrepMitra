"""Writes batches/parts/BATCH_001_GA.json: the 150 General Awareness questions of BATCH_001 (static topics only).

Every question carries at least one fact_check whose source_url was opened or confirmed in a web search on
2026-11-05. pib.gov.in returns HTTP 403 to automated fetches, so PIB facts were confirmed from search results that
quote the release. Facts that can change (scheme limits, member counts, index ranks) carry current_affairs dates.

Options are written with the correct answer either at a fixed letter (ordered options such as numbers, dates and
statement combinations) or first with answer "*" (unordered options such as cities or organisations). Flexible
questions are then placed so that the answer keys come out balanced across A to D.

    python tools/batch_001/ga.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-05"
REVIEW_BY = "2027-05-05"
LETTERS = "ABCD"
GA = "General Awareness and Current Affairs"
SECONDS = {"Basic": 15, "Intermediate": 25, "Advanced": 45}

# Statement-combination option sets (fixed order)
S12 = ["Only 1", "Only 2", "Both 1 and 2", "Neither 1 nor 2"]
S123 = ["1 and 2 only", "2 and 3 only", "1 and 3 only", "1, 2 and 3"]
S123b = ["1 only", "1 and 2 only", "1 and 3 only", "1, 2 and 3"]
S1234 = ["1, 2 and 3 only", "1 and 3 only", "2, 3 and 4 only", "1, 2, 3 and 4"]

QUESTIONS = []


def fact(claim, url):
    return {"claim": claim, "source_url": url, "checked_on": TODAY}


def ca(event_date):
    return {"event_date": event_date, "review_by": REVIEW_BY}


def G(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, facts,
      why=None, shortcut=None, current=None):
    assert len(options) == 4 and len(set(options)) == 4, text
    assert answer == "*" or answer in LETTERS, answer
    assert facts, text
    QUESTIONS.append(dict(topic=topic, subtopic=subtopic, difficulty=difficulty, text=text, options=list(options),
                          answer=answer, concept=concept, explanation=explanation, steps=steps, facts=facts,
                          why=why, shortcut=shortcut, current=current))


# ====================================================================== sources (opened or search-confirmed)
PIB = "https://www.pib.gov.in/"
U = {
    # Government schemes
    "pmkisan": PIB + "PressReleaseIframePage.aspx?PRID=1946816&reg=48&lang=2",
    "pmjdy11": PIB + "PressReleseDetailm.aspx?PRID=2161401",
    "jansuraksha10": PIB + "PressReleasePage.aspx?PRID=2127981&reg=48&lang=2",
    "pmsby": PIB + "PressNoteDetails.aspx?ModuleId=3&NoteId=154426&reg=3&lang=2",
    "mudra10": PIB + "PressReleasePage.aspx?PRID=2119954",
    "tarunplus": "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2024/oct/doc20241029426401.pdf",
    "standup": "https://www.standupmitra.in/",
    "vishwakarma_site": "https://pmvishwakarma.gov.in/",
    "vishwakarma_bg": PIB + "PressNoteDetails.aspx?NoteId=159998&ModuleId=3&reg=48&lang=2",
    "pmjay_launch": PIB + "newsite/PrintRelease.aspx?relid=183635&reg=48&lang=2",
    "pmjay_pre": PIB + "Pressreleaseshare.aspx?PRID=1546948&reg=48&lang=2",
    "ujjwala": PIB + "newsite/PrintRelease.aspx?relid=142608&reg=3&lang=2",
    "svanidhi": PIB + "PressReleasePage.aspx?PRID=2267102&lang=2&reg=48",
    "pmfby": PIB + "newsite/PrintRelease.aspx?relid=134432&reg=3&lang=2",
    "suryaghar": PIB + "PressReleaseIframePage.aspx?PRID=2010130&reg=48&lang=2",
    "ssy": PIB + "PressReleasePage.aspx?PRID=2216748&reg=3&lang=1&noshow=1",
    "svamitva": PIB + "PressReleasePage.aspx?PRID=2123886&reg=3&lang=2",
    "jjm": PIB + "PressNoteDetails.aspx?NoteId=155710&ModuleId=3&reg=3&lang=1",
    "makeinindia": PIB + "PressReleasePage.aspx?PRID=2058603&reg=48&lang=2",
    "pmkmy": "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2022/jan/doc20221185101.pdf",
    "soilhealth": PIB + "FactsheetDetails.aspx?Id=148602&reg=48&lang=2",
    "ups": PIB + "PressReleseDetailm.aspx?PRID=2048607&reg=3&lang=2",
    "enam": "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2023/apr/doc2023414181301.pdf",
    "janman": PIB + "PressReleasePage.aspx?PRID=1994794",
    "gatishakti": PIB + "PressReleasePage.aspx?PRID=2064378&reg=3&lang=2",
    "pmmsy": PIB + "PressReleasePage.aspx?PRID=1625535",
    "pmegp": PIB + "PressReleseDetailm.aspx?PRID=2079789&reg=48&lang=2",
    "aif": PIB + "PressReleasePage.aspx?PRID=1644529",
    "smartcities": PIB + "PressNoteDetails.aspx?NoteId=151908&ModuleId=3&reg=3&lang=2",
    "pmwani": PIB + "PressReleasePage.aspx?PRID=2327417&reg=48&lang=2",
    "pmgkay": PIB + "PressReleasePage.aspx?PRID=1980689",
    "pmsym": PIB + "PressReleasePage.aspx?PRID=1565071",
    "udan": PIB + "PressReleaseIframePage.aspx?PRID=2066445&reg=48&lang=2",
    "kusum": PIB + "FactsheetDetails.aspx?Id=148576&reg=48&lang=2",
    "kcc": PIB + "PressReleasePage.aspx?PRID=2238004&reg=3&lang=1",
    "poshan": PIB + "PressReleasePage.aspx?PRID=2082323&reg=48&lang=2",
    # Important days
    "yoga": "https://www.un.org/en/delegate/learn-more-about-international-day-yoga",
    "who_history": "https://www.who.int/about/history",
    "population": "https://www.un.org/en/observances/world-population-day/background",
    "literacy": "https://www.unesco.org/en/days/literacy",
    "environment": "https://www.un.org/en/observances/environment-day/background",
    "statsday": PIB + "PressReleasePage.aspx?PRID=2140329&reg=48&lang=2",
    "voters": PIB + "newsite/printrelease.aspx?relid=157579&reg=3&lang=2",
    "constday": PIB + "FactsheetDetails.aspx?Id=148584&reg=3&lang=2",
    "sportsday": PIB + "PressNoteDetails.aspx?NoteId=155107&ModuleId=3&reg=48&lang=2",
    "youthday": PIB + "newsite/PrintRelease.aspx?relid=114503&reg=3&lang=2",
    "scienceday": PIB + "PressNoteDetails.aspx?ModuleId=3&NoteId=151846&reg=48&lang=2",
    "humanrights": "https://www.un.org/en/observances/human-rights-day",
    "udhr_history": "https://www.un.org/en/about-us/udhr/history-of-the-declaration",
    "tourism": "https://www.un.org/en/observances/tourism-day/background",
    # Organisations
    "adb_about": "https://www.adb.org/who-we-are/about",
    "adb_contact": "https://www.adb.org/contacts/main",
    "aiib": "https://www.aiib.org/en/news-events/news/2016/AIIBs-Charter-Enters-into-Force-On-25-December-2015.html",
    "aiib_timeline": "https://www.aiib.org/en/about-aiib/who-we-are/timeline/",
    "bis": "https://www.bis.org/about/history.htm",
    "wto": "https://www.wto.org/english/thewto_e/30y_e/30ytimeline_e.htm",
    "imf_aa": "https://www.imf.org/external/pubs/ft/aa/",
    "imf_sdr": "https://www.imf.org/external/pubs/ft/finop/2014/pdf/ch4.pdf",
    "imf_bylaws": "https://www.imf.org/external/pubs/ft/bl/bl01.htm",
    "wbg_basics": "https://libguides.worldbank.org/WBGInfoguide/basics",
    "wb_members": "https://www.worldbank.org/en/about/leadership/members",
    "ilo": "https://www.ilo.org/about-ilo/history-ilo",
    "ifad": "https://www.ifad.org/documents/d/new-ifad.org/agree_e-pdf",
    "isa": "https://isa.int/who-we-are/",
    "fatf": "https://www.fatf-gafi.org/en/the-fatf/history-of-the-fatf.html",
    "bimstec": "https://bimstec.org/history",
    "saarc": "https://www.mea.gov.in/Portal/ForeignRelation/India-SAARC-June-2026.pdf",
    "opec": "https://www.opec.org/brief-history.html",
    "asean_founding": "https://asean.org/the-founding-of-asean/",
    "asean_tl": "https://asean.org/forging-a-new-era-timor-leste-admitted-into-asean/",
    "sco_mea": "https://www.mea.gov.in/Portal/ForeignRelation/SCO-21-Aug-25.pdf",
    "sco_about": "https://eng.sectsco.org/20170109/192193.html",
    "g20_decl": "https://www.mea.gov.in/Images/CPV/G20-New-Delhi-Leaders-Declaration.pdf",
    "g20_brief": "https://www.mea.gov.in/Portal/ForeignRelation/G20_Brief_upto_MAR_25.pdf",
    "nabard": "https://www.nabard.org/content.aspx?id=2",
    "sidbi": "https://www.sidbi.in/en/about/",
    "unep": "https://www.unep.org/who-we-are/frequently-asked-questions",
    "interpol": "https://www.interpol.int/en/Who-we-are/What-is-INTERPOL",
    "niti": PIB + "newsite/PrintRelease.aspx?relid=114276&reg=48&lang=2",
    "brics": "https://brics.br/en/about-the-brics/frequently-asked-questions-about-the-brics",
    "iaea": "https://www.iaea.org/about/overview/history",
    "npci": "https://www.npci.org.in/",
    "unesco": "https://unesdoc.unesco.org/archives/about-unesco-history-and-mission",
    "irdai_addr": "https://irdai.gov.in/address-for-communication",
    # Reports and indexes
    "hdr_india": "https://www.undp.org/india/press-releases/"
                 "indias-human-development-continues-make-progress-ranks-130-out-193-countries",
    "mpi": "https://ophi.org.uk/global-mpi",
    "gggr": "https://www.weforum.org/publications/global-gender-gap-report-2025/benchmarking-gender-gaps-2025",
    "ghi": "https://www.globalhungerindex.org/methodology.html",
    "cpi": "https://www.transparency.org/en/cpi/2025",
    "rsf": "https://rsf.org/en/world-press-freedom-index",
    "whr_about": "https://www.worldhappiness.report/about/",
    "whr_faq": "https://www.worldhappiness.report/faq/",
    "wir": "https://unctad.org/publication/world-investment-report-2026-international-investment-turbulent-era",
    "iep": "https://www.economicsandpeace.org/",
    "gep": "https://www.worldbank.org/en/publication/global-economic-prospects",
    "imd": "https://www.imd.org/centers/wcc/world-competitiveness-center/",
    "epi": "https://epi.yale.edu/epi-team",
    "gii_wipo": "https://www.wipo.int/edocs/gii-ranking/2025/in.pdf",
    "gii_pib": PIB + "PressReleasePage.aspx?PRID=2219992&reg=48&lang=2",
    "fsr": "https://www.rbi.org.in/Scripts/PublicationReportDetails.aspx?UrlPage=&ID=1283",
    "sdgindex": PIB + "PressReleasePage.aspx?PRID=2032857&reg=48&lang=2",
    "lpi": PIB + "PressReleasePage.aspx?PRID=2003541",
    "swop": "https://www.unfpa.org/swp2025",
    "fiindex": PIB + "PressNoteDetails.aspx?ModuleId=3&NoteId=154980&lang=1&reg=3",
    # Government policies
    "gst56": PIB + "PressReleasePage.aspx?PRID=2163555&reg=48&lang=2",
    "gst56faq": PIB + "PressReleasePage.aspx?PRID=2163560&reg=3&lang=2",
    "gst_factsheet": PIB + "FactsheetDetails.aspx?Id=148644&reg=3&lang=1",
    "gst_council": PIB + "newsite/PrintRelease.aspx?relid=149732",
    "labourcodes": PIB + "PressReleseDetailm.aspx?PRID=2192463&reg=48&lang=2",
    "itact": PIB + "PressReleasePage.aspx?PRID=2248005&reg=48&lang=2",
    "ftp": PIB + "PressReleasePage.aspx?PRID=2079986&reg=3&lang=2",
    "janvishwas": PIB + "PressReleasePage.aspx?PRID=1990377&reg=48&lang=2",
    "ibc_faq": "https://ibbi.gov.in/uploads/faqs/CIRPFAQs%20Final2408.pdf",
    "nep": PIB + "PressReleasePage.aspx?PRID=1642061&reg=48&lang=2",
    "dpdp": PIB + "PressReleasePage.aspx?PRID=2190014&reg=3&lang=2",
    "corptax": PIB + "PressReleaseIframePage.aspx?PRID=1585641&reg=3&lang=2",
    # Static awareness
    "cia_bhutan": "https://www.cia.gov/the-world-factbook/countries/bhutan/summaries",
    "cia_burma": "https://www.cia.gov/the-world-factbook/about/archives/2023/countries/burma/",
    "cia_srilanka": "https://www.cia.gov/the-world-factbook/countries/sri-lanka/summaries",
    "cia_sa": "https://www.cia.gov/the-world-factbook/about/archives/2022/countries/south-africa/",
    "cia_kaz": "https://www.cia.gov/the-world-factbook/countries/kazakhstan/summaries",
    "cia_maldives": "https://www.cia.gov/the-world-factbook/about/archives/2023/countries/maldives/travel-facts",
    "cia_vietnam": "https://www.cia.gov/the-world-factbook/countries/vietnam/summaries",
    "kaziranga": "https://whc.unesco.org/en/list/337/",
    "sundarbans": "https://whc.unesco.org/en/list/452/",
    "whc_india": "https://whc.unesco.org/en/statesparties/in/",
    "keoladeo": "https://whc.unesco.org/document/6955",
    "keibul": PIB + "PressReleasePage.aspx?PRID=1903423&reg=48&lang=2",
    "corbett": "https://corbettgov.org/about",
    "gir": PIB + "PressReleseDetailm.aspx?PRID=2223755&reg=3&lang=2",
    "tehri": "https://thdc.co.in/en/projects/hydro/tehri-dam-HPP-stage-I",
    "hirakud": "https://sambalpur.odisha.gov.in/tourism/tourist-places/hirakud-dam",
    "bhakra": "https://bbmb.gov.in/bhakra.htm",
    "ssp": "https://nca.gov.in/faq.htm",
    "telangana": PIB + "PressReleasePage.aspx?PRID=1829839&reg=3&lang=2",
    "goa": "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2023/may/doc2023531206701.pdf",
    "sikkim": "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2023/may/doc2023516199301.pdf",
    "jk": PIB + "PressReleseDetailm.aspx?PRID=1597617&reg=48&lang=2",
    "gujarat": "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2022/may/doc20225152301.pdf",
    "nagaland": "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2023/dec/doc2023121276901.pdf",
}

# ====================================================================== Government Schemes (12 / 16 / 12)
T, CS, SL = "Government Schemes", "Central schemes", "Scheme launches and changes"

# ---- Basic
G(T, CS, "Basic",
  "Under the PM-KISAN scheme, how much income support does an eligible landholding farmer family receive in a year?",
  ["₹6,000 in three equal instalments", "₹4,000 in two equal instalments", "₹10,000 in four equal instalments",
   "₹12,000 in twelve monthly instalments"], "*",
  "PM-KISAN income support",
  "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi), launched on 24 February 2019 by the Ministry of Agriculture and "
  "Farmers Welfare, pays ₹6,000 a year in three equal instalments of ₹2,000 directly into Aadhaar-seeded bank "
  "accounts through DBT. It began for small and marginal farmers and was extended to all landholding farmers from "
  "1 June 2019.",
  ["PM-KISAN benefit: ₹6,000 per year", "Paid in three equal instalments of ₹2,000 by DBT"],
  [fact("PM-KISAN launched 24 Feb 2019; ₹6,000 per year in three equal instalments by DBT; extended to all "
        "landholding farmers from 1 June 2019", U["pmkisan"])],
  shortcut="6,000 = 3 × 2,000.", current=ca("2019-02-24"))

G(T, SL, "Basic",
  "On which date was the Pradhan Mantri Jan Dhan Yojana (PMJDY) launched?",
  ["15 August 2014", "2 October 2014", "28 August 2014", "26 January 2015"], "C",
  "PMJDY launch",
  "PMJDY, the National Mission for Financial Inclusion, was launched by the Prime Minister on 28 August 2014. It "
  "gives every unbanked adult a basic savings account with a free RuPay debit card. The Department of Financial "
  "Services (Ministry of Finance) runs it.",
  ["PMJDY launch date: 28 August 2014", "So the answer is 28 August 2014"],
  [fact("PMJDY was launched by the Prime Minister on 28 August 2014", U["pmjdy11"])],
  why="15 August 2014 is the Independence Day speech in which it was announced; 2 October 2014 is the launch of "
      "Swachh Bharat Mission.")

G(T, CS, "Basic",
  "What is the annual premium payable by a subscriber under the Pradhan Mantri Suraksha Bima Yojana (PMSBY)?",
  ["₹12", "₹330", "₹436", "₹20"], "D",
  "Jan Suraksha schemes: PMSBY",
  "PMSBY is an accident insurance scheme for people aged 18 to 70 with a bank or post office account. For an annual "
  "premium of ₹20 (₹12 before 2022) it gives ₹2 lakh for accidental death or total permanent disability and ₹1 lakh "
  "for partial disability.",
  ["PMSBY premium: ₹20 a year", "Cover: ₹2 lakh (death/total disability), ₹1 lakh (partial disability)"],
  [fact("PMSBY premium ₹20 a year (earlier ₹12); cover ₹2 lakh / ₹1 lakh; age 18-70", U["pmsby"])],
  why="₹12 was the old PMSBY premium; ₹436 is the PMJJBY (life cover) premium; ₹330 was the old PMJJBY premium.",
  current=ca("2022-06-01"))

G(T, CS, "Basic",
  "The Pradhan Mantri Ujjwala Yojana, which provides LPG connections to women of poor households, is implemented by "
  "which ministry?",
  ["Ministry of Petroleum and Natural Gas", "Ministry of Rural Development",
   "Ministry of Consumer Affairs, Food and Public Distribution", "Ministry of Women and Child Development"], "*",
  "PM Ujjwala Yojana",
  "PMUY was launched by the Prime Minister at Ballia, Uttar Pradesh, on 1 May 2016 by the Ministry of Petroleum and "
  "Natural Gas. Its first target was 5 crore deposit-free LPG connections to BPL households in three years; the "
  "target was later raised to 8 crore.",
  ["PMUY is a Ministry of Petroleum and Natural Gas scheme", "Launched at Ballia, UP, on 1 May 2016"],
  [fact("PMUY launched at Ballia on 1 May 2016 by the Ministry of Petroleum and Natural Gas; 5 crore BPL "
        "connections in three years", U["ujjwala"])])

G(T, CS, "Basic",
  "Under Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (AB PM-JAY), what is the health cover per family per year?",
  ["₹1 lakh", "₹2 lakh", "₹5 lakh", "₹10 lakh"], "C",
  "AB PM-JAY",
  "AB PM-JAY gives each eligible family cover of up to ₹5 lakh a year for secondary and tertiary care "
  "hospitalisation, cashless, at empanelled public and private hospitals. It is run by the National Health "
  "Authority.",
  ["PM-JAY cover: ₹5,00,000 per family per year", "Covers secondary and tertiary hospitalisation"],
  [fact("PM-JAY provides coverage up to ₹5,00,000 per family per year for secondary and tertiary care "
        "hospitalisation", U["pmjay_pre"])],
  current=ca("2018-09-23"))

G(T, CS, "Basic",
  "The PM SVANidhi scheme provides collateral-free working capital loans to which group?",
  ["Street vendors", "Small and marginal farmers", "Traditional artisans", "Construction workers"], "*",
  "PM SVANidhi",
  "PM SVANidhi (PM Street Vendor's AtmaNirbhar Nidhi) was launched by the Ministry of Housing and Urban Affairs on "
  "1 June 2020 to help street vendors restart businesses hit by COVID-19, through collateral-free working capital "
  "loans in rising tranches, an interest subsidy and cashback for digital payments.",
  ["SVANidhi: Street Vendor's AtmaNirbhar Nidhi", "Beneficiaries: urban street vendors"],
  [fact("PM SVANidhi launched by MoHUA on 1 June 2020 to give street vendors collateral-free working capital loans",
        U["svanidhi"])],
  why="Traditional artisans are covered by PM Vishwakarma; farmers by PM-KISAN.")

G(T, CS, "Basic",
  "Which ministry implements the SVAMITVA scheme, under which drones are used to map rural inhabited land and issue "
  "property cards?",
  ["Ministry of Panchayati Raj", "Ministry of Rural Development", "Ministry of Housing and Urban Affairs",
   "Ministry of Earth Sciences"], "*",
  "SVAMITVA",
  "SVAMITVA (Survey of Villages and Mapping with Improvised Technology in Village Areas) was launched by the Prime "
  "Minister on National Panchayati Raj Day, 24 April 2020. The Ministry of Panchayati Raj implements it with the "
  "Survey of India; owners get a 'record of rights' (property card) that can be used for bank loans.",
  ["SVAMITVA is a Ministry of Panchayati Raj scheme", "Launched on National Panchayati Raj Day, 24 April 2020"],
  [fact("SVAMITVA launched on 24 April 2020; Ministry of Panchayati Raj with Survey of India; drone survey and "
        "property cards", U["svamitva"])])

G(T, CS, "Basic",
  "Jal Jeevan Mission, which aims to give every rural household a functional household tap connection, is "
  "implemented by which ministry?",
  ["Ministry of Jal Shakti", "Ministry of Rural Development", "Ministry of Environment, Forest and Climate Change",
   "Ministry of Housing and Urban Affairs"], "*",
  "Jal Jeevan Mission",
  "Jal Jeevan Mission is run by the Ministry of Jal Shakti in partnership with the States. Its goal is a Functional "
  "Household Tap Connection (FHTC) for every rural home.",
  ["JJM: tap water to every rural household", "Implementing ministry: Jal Shakti"],
  [fact("Jal Jeevan Mission is run by the Ministry of Jal Shakti with States to provide FHTCs to rural households",
        U["jjm"])])

G(T, CS, "Basic",
  "PM Vishwakarma scheme supports artisans and craftspeople working in how many traditional trades?",
  ["9", "12", "15", "18"], "D",
  "PM Vishwakarma",
  "PM Vishwakarma, run mainly by the Ministry of MSME, supports artisans in 18 family-based traditional trades such "
  "as carpenter, boat maker, goldsmith, potter, barber, tailor and fishing-net maker. It gives recognition (a "
  "certificate and ID card), skill training, a toolkit incentive, collateral-free credit and digital incentives.",
  ["PM Vishwakarma covers 18 trades", "So the answer is 18"],
  [fact("PM Vishwakarma covers 18 family-based traditional trades; Ministry of MSME", U["vishwakarma_site"])])

G(T, SL, "Basic",
  "The Soil Health Card scheme was launched by the Prime Minister on 19 February 2015 at which place?",
  ["Suratgarh, Rajasthan", "Panipat, Haryana", "Ballia, Uttar Pradesh", "Ranchi, Jharkhand"], "*",
  "Soil Health Card scheme",
  "The Soil Health Card scheme was launched at Suratgarh, Rajasthan, on 19 February 2015. Each card reports the "
  "soil's nutrient status and recommends fertiliser doses. Since 2022-23 it is the 'Soil Health & Fertility' "
  "component of the Rashtriya Krishi Vikas Yojana.",
  ["Launch: 19 February 2015", "Place: Suratgarh, Rajasthan"],
  [fact("PM launched the Soil Health Card scheme on 19 February 2015 at Suratgarh, Rajasthan", U["soilhealth"])],
  why="Panipat: Beti Bachao Beti Padhao (2015); Ballia: Ujjwala (2016); Ranchi: PM-JAY (2018).")

G(T, CS, "Basic",
  "Up to what age of a girl child can a Sukanya Samriddhi Yojana account be opened in her name?",
  ["5 years", "10 years", "14 years", "18 years"], "B",
  "Sukanya Samriddhi Yojana",
  "A Sukanya Samriddhi account can be opened from the birth of a girl child until she turns 10. The minimum deposit "
  "is ₹250 and the maximum ₹1.5 lakh a year; the account matures 21 years after opening. SSY was launched on "
  "22 January 2015 under Beti Bachao, Beti Padhao.",
  ["SSY: girl child below 10 years", "So the answer is 10 years"],
  [fact("SSY account can be opened from birth until the girl attains 10 years; matures after 21 years; ₹250 "
        "minimum, ₹1.5 lakh maximum a year", U["ssy"])])

G(T, SL, "Basic",
  "In which year was the 'Make in India' initiative launched?",
  ["2014", "2015", "2016", "2017"], "A",
  "Make in India",
  "Make in India was launched on 25 September 2014 to make India a global manufacturing hub. Its current phase, Make "
  "in India 2.0, focuses on 27 sectors.",
  ["Launch: 25 September 2014", "So the answer is 2014"],
  [fact("Make in India was launched on 25 September 2014", U["makeinindia"])])

# ---- Intermediate
G(T, CS, "Intermediate",
  "What is the entry age group for the Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)?",
  ["18 to 40 years", "18 to 50 years", "18 to 60 years", "18 to 70 years"], "B",
  "Jan Suraksha schemes: PMJJBY",
  "PMJJBY is a one-year renewable life cover of ₹2 lakh for death from any cause, for a premium of ₹436 a year. It "
  "is open to bank or post office account holders aged 18 to 50; those who join before 50 can keep the cover up to "
  "55 by paying the premium.",
  ["PMJJBY: age 18-50", "Cover ₹2 lakh, premium ₹436 a year"],
  [fact("PMJJBY: ₹2 lakh life cover, ₹436 premium, age 18-50", U["jansuraksha10"])],
  why="18-40 is the Atal Pension Yojana entry age; 18-70 is PMSBY.", current=ca("2025-05-09"))

G(T, CS, "Intermediate",
  "Atal Pension Yojana (APY) guarantees a monthly pension in which range after the subscriber turns 60?",
  ["₹3,000 fixed", "₹500 to ₹2,500", "₹2,000 to ₹10,000", "₹1,000 to ₹5,000"], "D",
  "Atal Pension Yojana",
  "APY is open to bank account holders aged 18 to 40 who are not income-tax payers. Depending on the contribution "
  "and the entry age, it guarantees a monthly pension of ₹1,000, 2,000, 3,000, 4,000 or 5,000 from age 60.",
  ["APY pension slabs: ₹1,000 to ₹5,000", "Entry age 18-40"],
  [fact("APY: age 18-40, non-income-tax payers, guaranteed pension ₹1,000 to ₹5,000 a month after 60",
        U["jansuraksha10"])],
  why="₹3,000 fixed is the PM Shram Yogi Maan-dhan and PM Kisan Maan-dhan pension.", current=ca("2025-05-09"))

G(T, SL, "Intermediate",
  "Under the Pradhan Mantri MUDRA Yojana, what is the upper loan limit of the 'Tarun Plus' category introduced in "
  "2024?",
  ["₹10 lakh", "₹15 lakh", "₹20 lakh", "₹25 lakh"], "C",
  "MUDRA loan categories",
  "PMMY (launched 8 April 2015) gives collateral-free loans to non-farm micro enterprises in categories Shishu (up "
  "to ₹50,000), Kishore (₹50,000 to ₹5 lakh) and Tarun (₹5 lakh to ₹10 lakh). Tarun Plus, announced in the Union "
  "Budget 2024-25 and effective 24 October 2024, covers ₹10 lakh to ₹20 lakh for borrowers who have repaid an "
  "earlier Tarun loan.",
  ["Tarun: up to ₹10 lakh", "Tarun Plus: ₹10 lakh to ₹20 lakh"],
  [fact("MUDRA loan limit raised to ₹20 lakh from ₹10 lakh through the Tarun Plus category", U["tarunplus"]),
   fact("PMMY launched 8 April 2015", U["mudra10"])],
  current=ca("2024-10-24"))

G(T, CS, "Intermediate",
  "Stand-Up India facilitates bank loans in which range for SC/ST and women entrepreneurs setting up greenfield "
  "enterprises?",
  ["₹10 lakh to ₹1 crore", "₹50,000 to ₹10 lakh", "₹1 crore to ₹5 crore", "Up to ₹20 lakh"], "*",
  "Stand-Up India",
  "Stand-Up India (launched 5 April 2016) facilitates bank loans between ₹10 lakh and ₹1 crore to at least one "
  "SC or ST borrower and at least one woman borrower per bank branch, for a greenfield enterprise. Borrowers must "
  "be above 18 years.",
  ["Stand-Up India range: ₹10 lakh to ₹1 crore", "At least one SC/ST and one woman borrower per branch"],
  [fact("Stand-Up India facilitates bank loans between ₹10 lakh and ₹1 crore to SC/ST and women entrepreneurs; "
        "at least one of each per bank branch", U["standup"])],
  why="Up to ₹20 lakh is the MUDRA Tarun Plus ceiling.")

G(T, CS, "Intermediate",
  "What concessional rate of interest does a beneficiary pay on the collateral-free enterprise development loan "
  "under PM Vishwakarma?",
  ["5%", "7%", "8%", "9%"], "A",
  "PM Vishwakarma credit support",
  "PM Vishwakarma gives collateral-free loans of ₹1 lakh (first tranche, 18 months) and ₹2 lakh (second tranche, "
  "30 months). The beneficiary pays a concessional 5%; the Ministry of MSME pays interest subvention capped at 8%, "
  "and the Government bears the credit guarantee fee. The scheme was launched on Vishwakarma Jayanti, 17 September "
  "2023.",
  ["Beneficiary rate: 5%", "Subvention up to 8% paid by MoMSME"],
  [fact("Concessional interest 5% charged from the beneficiary; interest subvention cap of 8% paid by MoMSME; "
        "₹1 lakh and ₹2 lakh tranches", U["vishwakarma_site"]),
   fact("PM Vishwakarma launched on Vishwakarma Jayanti, 17 September 2023", U["vishwakarma_bg"])],
  why="8% is the cap on the interest subvention the government pays to the lender, not the borrower's rate.",
  current=ca("2023-09-17"))

G(T, CS, "Intermediate",
  "Under the Pradhan Mantri Fasal Bima Yojana, what is the maximum premium payable by farmers for Rabi food and "
  "oilseed crops?",
  ["1.5% of sum insured", "2% of sum insured", "2.5% of sum insured", "5% of sum insured"], "A",
  "PMFBY premium rates",
  "PMFBY (approved January 2016, from Kharif 2016) caps the farmer's premium at 2% for Kharif food and oilseed "
  "crops, 1.5% for Rabi food and oilseed crops and 5% for annual commercial and horticultural crops. The rest of the "
  "premium is paid by the Centre and States. It replaced NAIS and MNAIS.",
  ["Kharif 2%, Rabi 1.5%, commercial/horticultural 5%", "So the answer is 1.5%"],
  [fact("PMFBY farmer premium: 2% Kharif, 1.5% Rabi, 5% annual commercial/horticultural crops", U["pmfby"])],
  shortcut="Rabi < Kharif < cash crops: 1.5 < 2 < 5.", current=ca("2016-01-13"))

G(T, SL, "Intermediate",
  "PM-Surya Ghar: Muft Bijli Yojana, approved by the Union Cabinet in February 2024, aims to install rooftop solar "
  "in how many households?",
  ["25 lakh", "50 lakh", "1 crore", "2 crore"], "C",
  "PM Surya Ghar",
  "The Cabinet approved PM-Surya Ghar: Muft Bijli Yojana on 29 February 2024 with an outlay of ₹75,021 crore to "
  "install rooftop solar in one crore households, which are expected to get up to 300 units of free electricity a "
  "month. The Ministry of New and Renewable Energy runs it.",
  ["Target: 1 crore households", "Benefit: up to 300 units a month"],
  [fact("Cabinet approved PM-Surya Ghar on 29 Feb 2024, ₹75,021 crore, rooftop solar for one crore households, up to "
        "300 units free a month", U["suryaghar"])],
  current=ca("2024-02-29"))

G(T, SL, "Intermediate",
  "Under the Pradhan Mantri Garib Kalyan Anna Yojana as extended from 1 January 2024, how much free foodgrain does "
  "an Antyodaya Anna Yojana (AAY) household get each month?",
  ["5 kg", "10 kg", "25 kg", "35 kg"], "D",
  "PMGKAY entitlements",
  "In November 2023 the Cabinet decided to give free foodgrains under PMGKAY to about 81.35 crore beneficiaries for "
  "five years from 1 January 2024: 35 kg per AAY household per month and 5 kg per person per month for Priority "
  "Households, as entitled under the National Food Security Act.",
  ["AAY: 35 kg per household per month", "Priority household: 5 kg per person per month"],
  [fact("Free foodgrains for 81.35 crore for five years from 1 Jan 2024; 35 kg per AAY household, 5 kg per person "
        "for PHH", U["pmgkay"])],
  why="5 kg is the per-person entitlement of priority households.", current=ca("2023-11-29"))

G(T, CS, "Intermediate",
  "The Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM) pension scheme is meant for unorganised workers with a monthly "
  "income of up to how much?",
  ["₹10,000", "₹15,000", "₹21,000", "₹25,000"], "B",
  "PM-SYM",
  "PM-SYM (launched in 2019) is a voluntary, contributory pension scheme for unorganised workers aged 18 to 40 with "
  "a monthly income of up to ₹15,000. The worker's contribution (₹55 to ₹200 a month by entry age) is matched by "
  "the government, and a minimum pension of ₹3,000 a month is paid from age 60.",
  ["Income ceiling ₹15,000 a month", "Pension ₹3,000 a month from 60"],
  [fact("PM-SYM for unorganised workers with monthly income up to ₹15,000, age 18-40, ₹3,000 pension",
        U["pmsym"])],
  why="₹21,000 is the ESI wage ceiling.", current=ca("2019-02-15"))

G(T, CS, "Intermediate",
  "Which institution is the pension fund manager of the Pradhan Mantri Kisan Maan-Dhan Yojana (PM-KMY)?",
  ["Life Insurance Corporation of India", "Pension Fund Regulatory and Development Authority",
   "State Bank of India", "NABARD"], "*",
  "PM Kisan Maan-Dhan Yojana",
  "PM-KMY is a voluntary contributory pension scheme for small and marginal farmers aged 18 to 40. It pays a "
  "minimum pension of ₹3,000 a month after 60; the Centre matches the farmer's contribution 1:1. LIC is the pension "
  "fund manager and handles the pension payout.",
  ["PM-KMY fund manager: LIC", "Pension ₹3,000 a month after 60"],
  [fact("LIC shall be the Pension Fund Manager and responsible for pension payout under PM-KMY; age 18-40; ₹3,000",
        U["pmkmy"])],
  why="PFRDA regulates the NPS and APY; it is not the fund manager of PM-KMY.")

G(T, SL, "Intermediate",
  "The first flight under the UDAN regional connectivity scheme, flagged off by the Prime Minister on 27 April "
  "2017, connected Delhi with which city?",
  ["Shimla", "Chandigarh", "Dehradun", "Kullu"], "*",
  "UDAN",
  "UDAN (Ude Desh ka Aam Nagrik) was launched on 21 October 2016 by the Ministry of Civil Aviation under the "
  "National Civil Aviation Policy 2016 to connect unserved and underserved airports. The first UDAN flight, on the "
  "Shimla-Delhi route, was flagged off by the Prime Minister on 27 April 2017.",
  ["UDAN launched 21 October 2016", "First flight: Shimla-Delhi, 27 April 2017"],
  [fact("UDAN launched 21 October 2016 by the Ministry of Civil Aviation; first flight Shimla-Delhi on 27 April "
        "2017", U["udan"])])

G(T, CS, "Intermediate",
  "Which agency is the lead implementing agency of the National Agriculture Market (e-NAM)?",
  ["Small Farmers' Agribusiness Consortium (SFAC)", "NABARD", "NAFED", "Food Corporation of India"], "*",
  "e-NAM",
  "e-NAM, an online trading platform linking APMC mandis, was launched by the Prime Minister on 14 April 2016 in "
  "21 mandis of 8 States. It is fully funded by the Centre and implemented by SFAC under the Ministry of "
  "Agriculture and Farmers Welfare.",
  ["e-NAM launched 14 April 2016", "Lead implementing agency: SFAC"],
  [fact("e-NAM launched 14 April 2016; SFAC is the Lead Implementing Agency under the Ministry of Agriculture",
        U["enam"])])

G(T, SL, "Intermediate",
  "PM-JANMAN, launched on Janjatiya Gaurav Divas (15 November 2023) at Khunti, Jharkhand, targets which group?",
  ["Particularly Vulnerable Tribal Groups (PVTGs)", "Denotified and nomadic tribes",
   "Landless agricultural labourers", "Manual scavengers"], "*",
  "PM-JANMAN",
  "Pradhan Mantri Janjati Adivasi Nyaya Maha Abhiyan (PM-JANMAN) aims to give PVTG households and habitations basic "
  "facilities such as housing, drinking water, roads, electricity, health and education. It covers 75 PVTG "
  "communities and is coordinated by the Ministry of Tribal Affairs with 9 ministries.",
  ["PM-JANMAN: PVTGs", "Launched 15 November 2023 at Khunti"],
  [fact("PM-JANMAN launched 15 Nov 2023 (Janjatiya Gaurav Divas) at Khunti for Particularly Vulnerable Tribal "
        "Groups", U["janman"])])

G(T, CS, "Intermediate",
  "What was the total approved outlay of the Pradhan Mantri Matsya Sampada Yojana (PMMSY) for FY 2020-21 to "
  "FY 2024-25?",
  ["₹7,522 crore", "₹15,000 crore", "₹20,050 crore", "₹1 lakh crore"], "C",
  "PMMSY",
  "PMMSY, the fisheries flagship of the Department of Fisheries, was approved by the Cabinet in May 2020 with an "
  "outlay of ₹20,050 crore (Centre ₹9,407 crore, States ₹4,880 crore, beneficiaries ₹5,763 crore) and launched on "
  "10 September 2020. It has since been extended to 2025-26.",
  ["PMMSY outlay: ₹20,050 crore", "Period FY21 to FY25"],
  [fact("PMMSY: total outlay ₹20,050 crore over five years FY 2020-21 to 2024-25", U["pmmsy"])],
  why="₹1 lakh crore is the size of the Agriculture Infrastructure Fund.")

G(T, CS, "Intermediate",
  "Under the Agriculture Infrastructure Fund, what rate of interest subvention is given on loans for post-harvest "
  "management infrastructure?",
  ["1.5% per annum", "2% per annum", "3% per annum", "4% per annum"], "C",
  "Agriculture Infrastructure Fund",
  "The ₹1 lakh crore Agriculture Infrastructure Fund (launched by the PM on 9 August 2020) gives 3% per annum "
  "interest subvention and credit guarantee cover under CGTMSE on loans of up to ₹2 crore for post-harvest "
  "management infrastructure and community farming assets. The scheme runs from FY2020 to FY2029.",
  ["AIF interest subvention: 3% a year", "Credit guarantee for loans up to ₹2 crore"],
  [fact("AIF ₹1 lakh crore; interest subvention 3% per annum; CGTMSE guarantee for loans up to ₹2 crore",
        U["aif"])],
  why="1.5% is the interest subvention to lenders under the Modified Interest Subvention Scheme for KCC loans.",
  current=ca("2020-08-09"))

G(T, SL, "Intermediate",
  "PM POSHAN, approved in September 2021, was earlier known by which name?",
  ["National Programme for Mid-Day Meal in Schools", "Integrated Child Development Services",
   "POSHAN Abhiyaan", "Annapurna Scheme"], "*",
  "PM POSHAN",
  "The Cabinet approved Pradhan Mantri Poshan Shakti Nirman (PM POSHAN) on 29 September 2021 as a modified version "
  "of the Mid-Day Meal scheme, for 2021-22 to 2025-26. It gives a hot cooked meal to children of Classes I-VIII in "
  "government and government-aided schools and adds pre-primary (Balvatika). The Ministry of Education runs it.",
  ["PM POSHAN = renamed Mid-Day Meal scheme", "Ministry of Education"],
  [fact("PM POSHAN earlier known as National Programme for Mid-Day Meal in Schools; approved 29 Sept 2021; "
        "Classes I-VIII plus Balvatika", U["poshan"])],
  why="ICDS and POSHAN Abhiyaan are Ministry of Women and Child Development programmes.")

# ---- Advanced
G(T, CS, "Advanced",
  "Consider the following statements about the Pradhan Mantri Jan Dhan Yojana (PMJDY):\n"
  "1. It is described as the National Mission for Financial Inclusion.\n"
  "2. The RuPay debit card issued to accounts opened after 28 August 2018 carries accident insurance cover of "
  "₹2 lakh.\n"
  "3. Account holders can avail an overdraft facility of up to ₹25,000.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "PMJDY features",
  "PMJDY, the National Mission for Financial Inclusion, gives a basic savings account, a free RuPay card with "
  "accident cover of ₹2 lakh (₹1 lakh for accounts opened before 28 August 2018) and an overdraft facility of up to "
  "₹10,000, not ₹25,000.",
  ["Statement 1: correct", "Statement 2: correct (₹1 lakh before 28.8.2018)",
   "Statement 3: wrong, the overdraft limit is ₹10,000", "So 1 and 2 only"],
  [fact("PMJDY National Mission for Financial Inclusion; overdraft up to ₹10,000; RuPay accident cover ₹2 lakh "
        "(₹1 lakh before 28.8.2018)", U["pmjdy11"])],
  current=ca("2025-08-28"))

G(T, SL, "Advanced",
  "Consider the following statements about the Unified Pension Scheme (UPS) for Central Government employees:\n"
  "1. The assured pension is 50% of the average basic pay of the last 12 months before superannuation, for a "
  "minimum qualifying service of 25 years.\n"
  "2. The assured family pension is 60% of the employee's pension.\n"
  "3. A minimum assured pension of ₹10,000 a month is paid on superannuation after at least 10 years of service.\n"
  "4. The scheme came into effect from 1 April 2024.\n"
  "Which of the statements given above are correct?",
  S1234, "A",
  "Unified Pension Scheme",
  "The Cabinet approved UPS on 24 August 2024 as an option under the NPS for Central Government employees. It "
  "assures 50% of the average basic pay of the last 12 months (25 years' service, proportionate down to 10 years), "
  "60% family pension and a minimum pension of ₹10,000 a month. It took effect from 1 April 2025, not 2024.",
  ["Statements 1, 2 and 3 match the Cabinet decision", "Statement 4 is wrong: effective 1 April 2025",
   "So 1, 2 and 3 only"],
  [fact("UPS: 50% of average basic pay of last 12 months for 25 years service; family pension 60%; minimum "
        "₹10,000 after 10 years; effective 1 April 2025", U["ups"])],
  current=ca("2024-08-24"))

G(T, CS, "Advanced",
  "Under PM-KUSUM, implemented by the Ministry of New and Renewable Energy, what does Component-B provide for?",
  ["Installation of standalone solar-powered agricultural pumps",
   "Decentralised ground-mounted grid-connected solar plants of up to 2 MW each",
   "Solarisation of existing grid-connected agricultural pumps, including feeder-level solarisation",
   "Rooftop solar plants on rural houses with up to 300 units of free electricity"], "*",
  "PM-KUSUM components",
  "PM-KUSUM, approved by the CCEA on 19 February 2019, has three components: A, decentralised grid-connected "
  "renewable plants of up to 2 MW each; B, standalone (off-grid) solar agricultural pumps; and C, solarisation of "
  "grid-connected agricultural pumps, including feeder-level solarisation.",
  ["Component A: small grid-connected plants (up to 2 MW)", "Component B: standalone solar pumps",
   "Component C: solarising grid-connected pumps"],
  [fact("PM-KUSUM approved 19.2.2019 with Components A (plants up to 2 MW), B (standalone solar pumps) and C "
        "(solarisation of grid-connected pumps)", U["kusum"])],
  why="Rooftop solar with 300 free units is PM Surya Ghar, not PM-KUSUM.")

G(T, CS, "Advanced",
  "Consider the following statements about the Kisan Credit Card (KCC):\n"
  "1. The KCC scheme was introduced in 1998.\n"
  "2. Under the Modified Interest Subvention Scheme, farmers get short-term KCC loans at 7%, which falls to an "
  "effective 4% with the 3% prompt repayment incentive.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "KCC and interest subvention",
  "The KCC scheme was introduced in 1998 so that farmers could buy inputs and draw cash for production needs. Under "
  "the Modified Interest Subvention Scheme, short-term crop loans through KCC carry 7% interest (lenders get 1.5% "
  "subvention), and prompt repayment earns a further 3% incentive, bringing the effective rate to 4%.",
  ["Statement 1: correct (1998)", "Statement 2: correct (7% − 3% = 4%)", "So both"],
  [fact("KCC introduced in 1998; MISS: 7% interest, 1.5% subvention to lenders, 3% PRI, effective 4%", U["kcc"])],
  shortcut="7 − 3 = 4.", current=ca("2025-05-28"))

G(T, SL, "Advanced",
  "Consider the following statements about Ayushman Bharat PM-JAY:\n"
  "1. It was launched by the Prime Minister at Ranchi, Jharkhand, on 23 September 2018.\n"
  "2. It covers only primary and outpatient care.\n"
  "3. It is implemented by the National Health Authority.\n"
  "Which of the statements given above is/are correct?",
  S123, "C",
  "AB PM-JAY",
  "PM-JAY was launched at Ranchi on 23 September 2018 and is run by the National Health Authority. It covers "
  "secondary and tertiary care hospitalisation (not primary/OPD care) of up to ₹5 lakh per family per year. "
  "Primary care is delivered through the Ayushman Arogya Mandirs (Health and Wellness Centres), the other pillar "
  "of Ayushman Bharat.",
  ["1: correct", "2: wrong, PM-JAY covers secondary and tertiary hospitalisation", "3: correct",
   "So 1 and 3 only"],
  [fact("PM launched AB-PMJAY at Ranchi on 23 September 2018", U["pmjay_launch"]),
   fact("PM-JAY covers secondary and tertiary hospitalisation; run by the National Health Authority",
        U["pmjay_pre"])])

G(T, SL, "Advanced",
  "Consider the following statements about the Smart Cities Mission:\n"
  "1. It was launched on 25 June 2015.\n"
  "2. It covers 100 cities.\n"
  "3. It is implemented by the Ministry of Rural Development.\n"
  "Which of the statements given above is/are correct?",
  S123b, "B",
  "Smart Cities Mission",
  "The Smart Cities Mission was launched by the Prime Minister on 25 June 2015, the same day as AMRUT, for 100 "
  "cities with central assistance of ₹48,000 crore. Being an urban mission, it is run by the Ministry of Housing "
  "and Urban Affairs, not the Ministry of Rural Development.",
  ["1: correct", "2: correct", "3: wrong (MoHUA)", "So 1 and 2 only"],
  [fact("Smart Cities Mission launched 25 June 2015 for 100 cities (MoHUA)", U["smartcities"])])

G(T, CS, "Advanced",
  "Consider the following statements about the Prime Minister's Employment Generation Programme (PMEGP):\n"
  "1. The Khadi and Village Industries Commission (KVIC) is its nodal agency at the national level.\n"
  "2. It is a credit-linked subsidy programme for micro enterprises in the farm sector only.\n"
  "Which of the statements given above is/are correct?",
  S12, "A",
  "PMEGP",
  "PMEGP, run by the Ministry of MSME since 2008-09, is a credit-linked subsidy programme for self-employment "
  "through micro enterprises in the non-farm sector. KVIC is the national nodal agency; at State level KVIC "
  "offices, KVIBs, the Coir Board and District Industries Centres implement it.",
  ["1: correct", "2: wrong, it is for the non-farm sector", "So only 1"],
  [fact("PMEGP since 2008-09 for self-employment in the non-farm sector through banks; KVIC nodal agency",
        U["pmegp"])])

G(T, SL, "Advanced",
  "Consider the following statements:\n"
  "1. The PM GatiShakti National Master Plan was launched on 13 October 2021.\n"
  "2. The National Logistics Policy was launched before the PM GatiShakti National Master Plan.\n"
  "Which of the statements given above is/are correct?",
  ["Only 2", "Both 1 and 2", "Neither 1 nor 2", "Only 1"], "D",
  "PM GatiShakti and National Logistics Policy",
  "The PM GatiShakti National Master Plan, a GIS-based platform for integrated multimodal infrastructure planning, "
  "was launched on 13 October 2021. The National Logistics Policy came later, on 17 September 2022, to deal with "
  "the 'soft' side (processes, skills, digital systems) through the Comprehensive Logistics Action Plan.",
  ["1: correct (13 Oct 2021)", "2: wrong, NLP came on 17 Sept 2022", "So only 1"],
  [fact("PM GatiShakti NMP launched 13 October 2021; National Logistics Policy launched 17 September 2022",
        U["gatishakti"])])

G(T, SL, "Advanced",
  "Consider the following statements about the Jal Jeevan Mission:\n"
  "1. It was announced by the Prime Minister on 15 August 2019.\n"
  "2. When it began, only about 3.23 crore (about 17%) rural households had tap water connections.\n"
  "3. The mission has been extended up to 2028.\n"
  "Which of the statements given above is/are correct?",
  S123, "D",
  "Jal Jeevan Mission",
  "JJM was announced from the Red Fort on 15 August 2019 with the goal of tap water for every rural household by "
  "2024. At the start only 3.23 crore households (16.71%) had tap connections; the mission has since been "
  "extended to 2028.",
  ["1: correct", "2: correct (3.23 crore, 16.71%)", "3: correct (extended to 2028)", "So all three"],
  [fact("JJM launched 15 Aug 2019; at launch 3.23 crore households (16.71%) had tap water; extended to 2028",
        U["jjm"])],
  current=ca("2025-02-01"))

G(T, CS, "Advanced",
  "Consider the following statements about PM SVANidhi:\n"
  "1. It was launched by the Ministry of Housing and Urban Affairs on 1 June 2020.\n"
  "2. It is a joint responsibility of the Ministry of Housing and Urban Affairs and the Department of Financial "
  "Services.\n"
  "3. Loans under the scheme require collateral security.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "1 and 3 only", "1 and 2 only", "1, 2 and 3"], "C",
  "PM SVANidhi",
  "PM SVANidhi was launched by MoHUA on 1 June 2020 and is run jointly with the Department of Financial Services. "
  "Its working-capital loans are collateral-free, with an interest subsidy and cashback on digital transactions. "
  "Lending has been extended to March 2030.",
  ["1: correct", "2: correct", "3: wrong, loans are collateral-free", "So 1 and 2 only"],
  [fact("PM SVANidhi launched by MoHUA 1 June 2020; joint responsibility of MoHUA and DFS; collateral-free loans",
        U["svanidhi"])])

G(T, CS, "Advanced",
  "Under PM-Surya Ghar: Muft Bijli Yojana, central financial assistance is 60% of the system cost for rooftop solar "
  "systems of up to what capacity (with 40% of the additional cost above that, capped at 3 kW)?",
  ["1 kW", "2 kW", "3 kW", "5 kW"], "B",
  "PM Surya Ghar subsidy structure",
  "Central financial assistance under PM Surya Ghar is 60% of the system cost for systems of up to 2 kW and 40% of "
  "the additional cost for systems between 2 and 3 kW, capped at 3 kW. At benchmark prices this is about ₹30,000 "
  "for 1 kW, ₹60,000 for 2 kW and ₹78,000 for 3 kW or more.",
  ["60% CFA up to 2 kW", "40% on the 2-3 kW part; cap 3 kW"],
  [fact("CFA 60% of system cost for 2 kW systems and 40% of additional cost between 2 and 3 kW, capped at 3 kW",
        U["suryaghar"])],
  current=ca("2024-02-29"))

G(T, SL, "Advanced",
  "Consider the following statements about the PM-WANI scheme of the Department of Telecommunications:\n"
  "1. It was approved by the Union Cabinet in December 2020.\n"
  "2. Public Data Offices (PDOs) set up Wi-Fi hotspots, while PDO Aggregators handle functions such as user "
  "authorisation and accounting.\n"
  "3. A PDO needs a telecom licence and must pay a licence fee.\n"
  "Which of the statements given above is/are correct?",
  ["2 only", "1 and 2 only", "2 and 3 only", "1, 2 and 3"], "B",
  "PM-WANI",
  "PM-WANI (approved on 9 December 2020) builds public Wi-Fi through a decentralised, licence-free model: local "
  "Public Data Offices run hotspots, PDO Aggregators provide authorisation and accounting, and app providers "
  "let users find and log in to hotspots.",
  ["1: correct", "2: correct", "3: wrong, the PDO model is licence-free", "So 1 and 2 only"],
  [fact("PM-WANI approved by Cabinet 9 Dec 2020; licence-free PDOs; PDOAs handle authorisation and accounting",
        U["pmwani"])])

# ====================================================================== Important Days (4 / 6 / 4)
T, DT = "Important Days", "Days and themes"

G(T, DT, "Basic", "On which date is the International Day of Yoga observed every year?",
  ["5 June", "21 June", "11 July", "8 September"], "B",
  "International Day of Yoga",
  "The UN General Assembly proclaimed 21 June as the International Day of Yoga, and it has been observed since "
  "2015. 21 June is the summer solstice, the longest day of the year in the Northern Hemisphere.",
  ["International Day of Yoga: 21 June", "First observed in 2015"],
  [fact("UNGA proclaimed 21 June each year as the International Day of Yoga; marked since 2015", U["yoga"])],
  why="5 June is World Environment Day, 11 July World Population Day and 8 September International Literacy Day.")

G(T, DT, "Basic", "National Voters' Day, observed every year since 2011, falls on which date?",
  ["23 January", "24 January", "25 January", "26 January"], "C",
  "National Voters' Day",
  "National Voters' Day is observed on 25 January to mark the foundation of the Election Commission of India, "
  "which came into existence on 25 January 1950, the eve of the first Republic Day. The day has been observed since "
  "2011 to encourage voter enrolment, especially of new voters.",
  ["ECI founded 25 January 1950", "So National Voters' Day: 25 January"],
  [fact("National Voters' Day instituted in 2011; ECI came into existence on 25 January 1950", U["voters"])],
  why="24 January is National Girl Child Day; 26 January is Republic Day.")

G(T, DT, "Basic", "National Statistics Day (29 June) marks the birth anniversary of which statistician?",
  ["P. C. Mahalanobis", "C. R. Rao", "C. V. Raman", "Homi J. Bhabha"], "*",
  "National Statistics Day",
  "The Government of India observes 29 June, the birth anniversary of Prof. Prasanta Chandra Mahalanobis, as "
  "Statistics Day to honour his work in statistics and economic planning. He founded the Indian Statistical "
  "Institute and introduced the Mahalanobis distance.",
  ["29 June = birth anniversary of P. C. Mahalanobis", "So the answer is P. C. Mahalanobis"],
  [fact("Government designated 29 June, birth day of Prof. P. C. Mahalanobis, as Statistics Day", U["statsday"])],
  why="C. V. Raman is linked to National Science Day (28 February).")

G(T, DT, "Basic", "National Sports Day, observed on 29 August, commemorates the birth anniversary of whom?",
  ["Major Dhyan Chand", "Milkha Singh", "K. D. Jadhav", "Balbir Singh Sr."], "*",
  "National Sports Day",
  "National Sports Day on 29 August marks the birth anniversary of hockey legend Major Dhyan Chand, who led India to "
  "Olympic gold in 1928, 1932 and 1936. The national sports awards are usually conferred by the President around "
  "this day.",
  ["29 August = Dhyan Chand's birth anniversary", "So the answer is Major Dhyan Chand"],
  [fact("National Sports Day on 29 August commemorates the birth anniversary of Major Dhyan Chand",
        U["sportsday"])])

G(T, DT, "Intermediate", "World Health Day, observed on 7 April, marks which event?",
  ["The coming into force of the WHO Constitution in 1948", "The Alma-Ata Declaration on primary health care",
   "The declaration of smallpox eradication", "The adoption of the International Health Regulations"], "*",
  "World Health Day",
  "World Health Day is observed every year on 7 April, the anniversary of WHO's founding: the WHO Constitution came "
  "into force on 7 April 1948, when the 26th of the 61 signatory governments ratified it.",
  ["WHO Constitution in force: 7 April 1948", "World Health Day marks that anniversary"],
  [fact("WHO Constitution came into force on 7 April 1948; World Health Day marks the anniversary",
        U["who_history"])])

G(T, DT, "Intermediate",
  "World Population Day (11 July) was established in 1989 by the Governing Council of which body?",
  ["United Nations Development Programme (UNDP)", "United Nations Population Fund (UNFPA)", "UNICEF",
   "UN Economic and Social Council (ECOSOC)"], "*",
  "World Population Day",
  "World Population Day was established in 1989 by the then Governing Council of UNDP. It grew out of interest in "
  "the 'Day of Five Billion' on 11 July 1987, when world population was estimated to reach five billion. UNFPA "
  "now leads the observance.",
  ["Established 1989 by the UNDP Governing Council", "Inspired by the Day of Five Billion, 11 July 1987"],
  [fact("World Population Day established by the then Governing Council of UNDP in 1989, outgrowth of the Day of "
        "Five Billion on 11 July 1987", U["population"])],
  why="UNFPA leads the observance today, but the day was set up by UNDP's Governing Council.")

G(T, DT, "Intermediate",
  "5 June was chosen as World Environment Day because it was the opening day of which conference?",
  ["Earth Summit, Rio de Janeiro (1992)", "Kyoto climate conference (1997)",
   "UN Conference on the Human Environment, Stockholm (1972)", "COP21, Paris (2015)"], "C",
  "World Environment Day",
  "In December 1972 the UN General Assembly designated 5 June, the opening day of the 1972 Stockholm Conference on "
  "the Human Environment, as World Environment Day. The same session created UNEP, which has led the day since "
  "the first celebration in 1973.",
  ["Stockholm Conference opened 5 June 1972", "UNGA designated 5 June as World Environment Day"],
  [fact("UNGA designated 5 June (opening day of the 1972 Stockholm Conference) as World Environment Day; UNEP "
        "created the same day", U["environment"])])

G(T, DT, "Intermediate",
  "International Literacy Day (8 September) was proclaimed by UNESCO in which year?",
  ["1946", "1966", "1975", "1990"], "B",
  "International Literacy Day",
  "UNESCO proclaimed International Literacy Day at the 14th session of its General Conference in 1966, and it has "
  "been celebrated on 8 September every year since 1967. 2026 marks its 60th anniversary.",
  ["Proclaimed 1966 (14th General Conference)", "Celebrated since 1967"],
  [fact("International Literacy Day proclaimed by UNESCO in 1966 at its 14th General Conference; celebrated on "
        "8 September since 1967", U["literacy"])])

G(T, DT, "Intermediate",
  "National Science Day, which marks C. V. Raman's discovery of the Raman Effect on 28 February 1928, was first "
  "observed in which year?",
  ["1928", "1930", "1987", "1999"], "C",
  "National Science Day",
  "In 1986 the National Council for Science and Technology Communication asked the Government to designate "
  "28 February as National Science Day, and it was first celebrated on 28 February 1987. Raman won the Nobel Prize "
  "in Physics in 1930 for the Raman Effect.",
  ["Discovery: 28 February 1928", "First National Science Day: 1987"],
  [fact("NCSTC requested in 1986; first National Science Day celebrated 28 February 1987; Raman Effect discovered "
        "28 Feb 1928", U["scienceday"])],
  why="1928 is the discovery and 1930 the Nobel Prize, not the first observance.")

G(T, DT, "Intermediate", "World Tourism Day (27 September) marks the anniversary of which event?",
  ["Adoption of the Statutes of the World Tourism Organization in 1970", "Founding of the UN in 1945",
   "First World Tourism Conference in Manila", "Signing of the Global Code of Ethics for Tourism"], "*",
  "World Tourism Day",
  "World Tourism Day has been held on 27 September since 1980. The date marks the adoption of the Statutes of the "
  "World Tourism Organization (now UN Tourism) on 27 September 1970.",
  ["Statutes adopted 27 September 1970", "Day observed since 1980"],
  [fact("World Tourism Day on 27 September since 1980 marks the adoption of the UNWTO Statutes on 27 September 1970",
        U["tourism"])])

G(T, DT, "Advanced",
  "Consider the following statements about the International Day of Yoga:\n"
  "1. It was proclaimed by a UN General Assembly resolution adopted on 11 December 2014.\n"
  "2. The draft resolution proposed by India was endorsed by 175 Member States.\n"
  "3. It was first observed in 2014.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "International Day of Yoga",
  "The idea was proposed by India's Prime Minister at the 69th UNGA. Resolution 69/131 was adopted on 11 December "
  "2014 with a record 175 co-sponsoring Member States. The first International Day of Yoga was held on 21 June "
  "2015, not in 2014.",
  ["1: correct", "2: correct", "3: wrong (first observed 2015)", "So 1 and 2 only"],
  [fact("Resolution 69/131 adopted 11 Dec 2014; endorsed by 175 Member States; observed since 2015", U["yoga"])])

G(T, DT, "Advanced",
  "Consider the following statements about the Universal Declaration of Human Rights, whose adoption is marked by "
  "Human Rights Day on 10 December:\n"
  "1. It was adopted by the UN General Assembly meeting in Paris in 1948.\n"
  "2. It was adopted unanimously, with no abstentions.\n"
  "3. It has been translated into more than 500 languages.\n"
  "Which of the statements given above is/are correct?",
  S123, "C",
  "Human Rights Day and the UDHR",
  "The UNGA, meeting in Paris, adopted the UDHR on 10 December 1948 by resolution 217 A (III). No country voted "
  "against it, but eight abstained, so it was not 'unanimous with no abstentions'. It is the most translated "
  "document in the world, available in more than 500 languages.",
  ["1: correct", "2: wrong, eight countries abstained", "3: correct", "So 1 and 3 only"],
  [fact("UDHR adopted by UNGA in Paris on 10 Dec 1948, resolution 217 A (III), eight abstentions, none against; "
        "translated into more than 500 languages", U["humanrights"])])

G(T, DT, "Advanced",
  "Consider the following statements about National Youth Day:\n"
  "1. It is observed on 12 January, the birth anniversary of Swami Vivekananda.\n"
  "2. The Government of India has observed it since 1985, and the week beginning that day is observed as National "
  "Youth Week.\n"
  "Which of the statements given above is/are correct?",
  ["Only 1", "Both 1 and 2", "Only 2", "Neither 1 nor 2"], "B",
  "National Youth Day",
  "Since 1985 the Government of India has observed 12 January, Swami Vivekananda's birth anniversary, as National "
  "Youth Day and the week beginning that day as National Youth Week. The National Youth Festival has been held "
  "around 12-16 January.",
  ["1: correct", "2: correct", "So both"],
  [fact("Every year since 1985 GoI observes 12 January, Vivekananda's birth anniversary, as National Youth Day and "
        "the week from that day as National Youth Week", U["youthday"])])

G(T, DT, "Advanced",
  "Consider the following statements about Constitution Day (Samvidhan Divas):\n"
  "1. It marks the adoption of the Constitution of India by the Constituent Assembly on 26 November 1949.\n"
  "2. The Government of India formally declared 26 November as Constitution Day in 2015.\n"
  "3. It is observed on the same date as National Voters' Day.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "2 and 3 only", "1 and 2 only", "1, 2 and 3"], "C",
  "Constitution Day",
  "26 November is observed as Constitution Day because the Constituent Assembly adopted the Constitution on "
  "26 November 1949. The Government formally declared it Constitution Day in 2015 (the 125th birth anniversary year "
  "of Dr B. R. Ambedkar). National Voters' Day is on 25 January.",
  ["1: correct", "2: correct", "3: wrong (Voters' Day is 25 January)", "So 1 and 2 only"],
  [fact("In 2015 GoI declared 26 November as Constitution Day to honour adoption of the Constitution in 1949",
        U["constday"])])

# ====================================================================== National and International Organizations
T, HQ, MB = "National and International Organizations", "Headquarters and heads", "Membership"

G(T, HQ, "Basic", "Where is the headquarters of the Asian Development Bank (ADB)?",
  ["Manila (Metro Manila), Philippines", "Tokyo, Japan", "Singapore", "Beijing, China"], "*",
  "ADB",
  "ADB was founded in 1966 and is headquartered in Metro Manila (6 ADB Avenue, Mandaluyong City), Philippines. It "
  "is owned by 69 members, 50 of them from the region.",
  ["ADB HQ: Mandaluyong, Metro Manila", "Founded 1966"],
  [fact("ADB headquarters: 6 ADB Avenue, Mandaluyong City, Metro Manila, Philippines", U["adb_contact"]),
   fact("ADB founded in 1966; owned by 69 members", U["adb_about"])],
  why="Beijing hosts the AIIB.")

G(T, HQ, "Basic", "The Bank for International Settlements (BIS) is headquartered in which city?",
  ["Basel", "Geneva", "Zurich", "Bern"], "*",
  "BIS",
  "The BIS, the world's oldest international financial institution, began operations in Basel, Switzerland, on "
  "17 May 1930. It is owned by central banks and is often called the 'central bank of central banks'; the Basel "
  "Committee on Banking Supervision is hosted there.",
  ["BIS HQ: Basel, Switzerland", "Founded 1930"],
  [fact("BIS created 1930, headquartered in Basel since 1930", U["bis"])])

G(T, HQ, "Basic",
  "The International Fund for Agricultural Development (IFAD), both a UN specialised agency and an international "
  "financial institution, is headquartered in which city?",
  ["Rome", "Geneva", "Vienna", "Nairobi"], "*",
  "IFAD",
  "IFAD came into existence on 30 November 1977, following the 1974 World Food Conference, and has its seat in "
  "Rome. Rome also hosts the FAO and the World Food Programme.",
  ["IFAD seat: Rome", "Established 1977"],
  [fact("Agreement Establishing IFAD: seat of the Fund in Rome; entered into force 30 November 1977", U["ifad"])])

G(T, HQ, "Basic", "The headquarters of the United Nations Environment Programme (UNEP) is located in which city?",
  ["Nairobi", "Geneva", "Paris", "Bonn"], "*",
  "UNEP",
  "UNEP, created by the UN General Assembly in December 1972, is headquartered in Nairobi, Kenya. It was the first "
  "UN headquarters in the Global South. UN-Habitat is also headquartered in Nairobi.",
  ["UNEP HQ: Nairobi, Kenya", "Created December 1972"],
  [fact("UNEP headquarters are in Nairobi; adopted as home base on 15 December 1972", U["unep"])])

G(T, HQ, "Basic", "Where is the General Secretariat headquarters of INTERPOL located?",
  ["Lyon", "Paris", "Brussels", "The Hague"], "*",
  "INTERPOL",
  "INTERPOL's General Secretariat is headquartered in Lyon, France, with a global complex for innovation in "
  "Singapore. INTERPOL began in 1923 in Vienna as the International Criminal Police Commission and has 196 member "
  "countries.",
  ["INTERPOL HQ: Lyon, France", "Founded 1923"],
  [fact("INTERPOL General Secretariat headquarters in Lyon; 196 member countries", U["interpol"])],
  why="The Hague hosts Europol.")

G(T, HQ, "Basic", "The International Solar Alliance (ISA) has its headquarters in which city?",
  ["Gurugram", "New Delhi", "Paris", "Bengaluru"], "*",
  "International Solar Alliance",
  "The ISA was established in 2015 as a joint initiative of India and France on the sidelines of COP21 in Paris. "
  "Its secretariat is at the National Institute of Solar Energy campus in Gurugram, Haryana, making it the first "
  "international intergovernmental organisation headquartered in India.",
  ["ISA secretariat: NISE campus, Gurugram", "Joint initiative of India and France (2015)"],
  [fact("ISA Secretariat at Surya Bhawan, NISE Campus, Gurugram, Haryana; established 2015 by India and France",
        U["isa"])])

G(T, HQ, "Basic", "Where is the head office of the Small Industries Development Bank of India (SIDBI)?",
  ["Lucknow", "Mumbai", "New Delhi", "Kolkata"], "*",
  "SIDBI",
  "SIDBI was set up on 2 April 1990 under the SIDBI Act, 1989. Its head office is at SIDBI Tower, Lucknow. It is "
  "the principal financial institution for the promotion, financing and development of the MSME sector.",
  ["SIDBI head office: Lucknow", "Set up 2 April 1990"],
  [fact("SIDBI set up on 2 April 1990 under an Act of Parliament; head office in Lucknow", U["sidbi"])],
  why="NABARD and EXIM Bank are headquartered in Mumbai.")

G(T, HQ, "Basic", "The secretariat of the South Asian Association for Regional Cooperation (SAARC) is in which city?",
  ["Kathmandu", "Dhaka", "Colombo", "New Delhi"], "*",
  "SAARC",
  "SAARC was established when the SAARC Charter was signed in Dhaka on 8 December 1985. Its secretariat was set up "
  "in Kathmandu on 17 January 1987. It has eight members: Afghanistan, Bangladesh, Bhutan, India, Maldives, Nepal, "
  "Pakistan and Sri Lanka.",
  ["Charter signed: Dhaka, 1985", "Secretariat: Kathmandu (1987)"],
  [fact("SAARC Charter signed in Dhaka 8 Dec 1985; Secretariat set up in Kathmandu on 17 Jan 1987", U["saarc"])],
  why="Dhaka is where the Charter was signed (and where the BIMSTEC secretariat is).")

G(T, HQ, "Basic", "NITI Aayog, constituted on 1 January 2015, replaced which body?",
  ["Planning Commission", "National Development Council", "Finance Commission", "Inter-State Council"], "*",
  "NITI Aayog",
  "NITI Aayog (National Institution for Transforming India) was constituted by a Union Cabinet resolution of "
  "1 January 2015 to replace the Planning Commission set up in 1950. The Prime Minister is its Chairperson; its "
  "Governing Council includes all Chief Ministers and Lt. Governors of UTs.",
  ["NITI Aayog replaced the Planning Commission (1950)", "Chairperson: Prime Minister"],
  [fact("Government establishes NITI Aayog on 1 Jan 2015 to replace the Planning Commission", U["niti"])],
  why="The Finance Commission is a separate constitutional body under Article 280 and still exists.")

G(T, HQ, "Intermediate",
  "The Asian Infrastructure Investment Bank (AIIB), whose Articles of Agreement entered into force on 25 December "
  "2015, is headquartered in which city?",
  ["Beijing", "Shanghai", "Hong Kong", "Singapore"], "*",
  "AIIB",
  "AIIB's Articles of Agreement entered into force on 25 December 2015 and the bank began operations on 16 January "
  "2016 in Beijing, where it is headquartered. India is a founding member.",
  ["AIIB HQ: Beijing", "Operations from 16 January 2016"],
  [fact("AIIB Articles of Agreement entered into force on 25 December 2015", U["aiib"]),
   fact("AIIB inaugural meeting and headquarters in Beijing", U["aiib_timeline"])],
  why="Shanghai is the headquarters of the BRICS New Development Bank, a common trap.")

G(T, MB, "Intermediate",
  "The World Trade Organization, which replaced GATT on 1 January 1995, was established by which agreement?",
  ["Marrakesh Agreement", "Havana Charter", "Bretton Woods Agreement", "Doha Declaration"], "*",
  "WTO",
  "The Marrakesh Agreement establishing the WTO was signed on 15 April 1994 at the end of the Uruguay Round, and "
  "the WTO came into being on 1 January 1995, replacing GATT (1947). Unlike GATT, the WTO also covers services and "
  "intellectual property. Its headquarters is in Geneva.",
  ["Marrakesh Agreement signed 15 April 1994", "WTO from 1 January 1995"],
  [fact("Marrakesh Agreement signed 15 April 1994; WTO replaced GATT on 1 January 1995", U["wto"])],
  why="The Havana Charter (1948) tried to create an International Trade Organization that never came into being; "
      "Doha (2001) launched a negotiating round.")

G(T, MB, "Intermediate", "Which of the following was NOT one of the five founding members of OPEC in 1960?",
  ["Qatar", "Iran", "Kuwait", "Venezuela"], "*",
  "OPEC founding members",
  "OPEC was created at the Baghdad Conference of 10-14 September 1960 by Iran, Iraq, Kuwait, Saudi Arabia and "
  "Venezuela. Qatar joined later (1961) and left in 2019. The headquarters moved from Geneva to Vienna in 1965.",
  ["Founders: Iran, Iraq, Kuwait, Saudi Arabia, Venezuela", "Qatar joined later"],
  [fact("OPEC created at Baghdad, Sept 1960, by Iran, Iraq, Kuwait, Saudi Arabia and Venezuela; HQ moved to Vienna "
        "in 1965", U["opec"])])

G(T, MB, "Intermediate", "Which of the following was NOT a founding member of ASEAN in 1967?",
  ["Vietnam", "Indonesia", "Malaysia", "Philippines"], "*",
  "ASEAN founding members",
  "ASEAN was founded on 8 August 1967 in Bangkok with the ASEAN (Bangkok) Declaration signed by Indonesia, "
  "Malaysia, the Philippines, Singapore and Thailand. Vietnam joined in 1995.",
  ["Founders: Indonesia, Malaysia, Philippines, Singapore, Thailand", "Vietnam joined later"],
  [fact("ASEAN Declaration signed in Bangkok 8 Aug 1967 by Indonesia, Malaysia, Philippines, Singapore and "
        "Thailand", U["asean_founding"])])

G(T, MB, "Intermediate",
  "India became a full member of the Shanghai Cooperation Organisation (SCO) at the summit held in which city in "
  "June 2017?",
  ["Astana", "Ufa", "Qingdao", "Bishkek"], "*",
  "SCO membership",
  "India and Pakistan became full members of the SCO at the Astana Summit in June 2017. The SCO was founded in "
  "Shanghai on 15 June 2001. Iran joined in 2023 and Belarus in 2024.",
  ["India joined: Astana Summit, June 2017", "SCO founded 15 June 2001"],
  [fact("India formally joined the SCO at the Astana Summit in June 2017; Pakistan's accession at the same summit",
        U["sco_mea"])],
  why="The 2015 Ufa summit started the accession process; Qingdao (2018) was India's first summit as a member.")

G(T, HQ, "Intermediate", "Where is the permanent secretariat of BIMSTEC located?",
  ["Dhaka", "Bangkok", "Kathmandu", "Colombo"], "*",
  "BIMSTEC",
  "BIMSTEC was formed on 6 June 1997 through the Bangkok Declaration. It has seven members: Bangladesh, Bhutan, "
  "India, Myanmar, Nepal, Sri Lanka and Thailand. Its permanent secretariat was inaugurated in Dhaka on "
  "13 September 2014; the BIMSTEC Charter entered into force on 20 May 2024.",
  ["BIMSTEC secretariat: Dhaka (2014)", "Seven members"],
  [fact("BIMSTEC founded 6 June 1997 (Bangkok Declaration); secretariat in Dhaka inaugurated 13 Sept 2014",
        U["bimstec"])],
  why="Bangkok is where BIMSTEC was founded; Kathmandu hosts the SAARC secretariat.")

G(T, HQ, "Intermediate",
  "NABARD came into existence on 12 July 1982 on the recommendation of the committee (CRAFICARD) chaired by whom?",
  ["B. Sivaraman", "M. Narasimham", "R. N. Malhotra", "Y. V. Reddy"], "*",
  "NABARD",
  "The Committee to Review Arrangements for Institutional Credit for Agriculture and Rural Development (CRAFICARD), "
  "set up by the RBI in 1979 under B. Sivaraman, recommended a new development financial institution. NABARD was "
  "created by Act 61 of 1981 and came into existence on 12 July 1982, with its head office in Mumbai.",
  ["CRAFICARD chair: B. Sivaraman", "NABARD from 12 July 1982"],
  [fact("CRAFICARD formed 30 March 1979 under B. Sivaraman; NABARD came into existence 12 July 1982; head office "
        "Mumbai", U["nabard"])],
  why="M. Narasimham chaired the banking sector reform committees; R. N. Malhotra chaired the insurance reform "
      "committee.")

G(T, HQ, "Intermediate", "The head office of the Insurance Regulatory and Development Authority of India (IRDAI) is in "
  "which city?",
  ["Hyderabad", "Mumbai", "New Delhi", "Chennai"], "*",
  "IRDAI",
  "IRDAI was constituted under the IRDA Act, 1999, following the Malhotra Committee report. Its head office is in "
  "the Financial District, Nanakramguda, Gachibowli, Hyderabad. SEBI is in Mumbai and PFRDA in New Delhi.",
  ["IRDAI head office: Hyderabad", "Set up under IRDA Act, 1999"],
  [fact("IRDAI head office: Sy No. 115/1, Financial District, Nanakramguda, Gachibowli, Hyderabad",
        U["irdai_addr"])])

G(T, HQ, "Intermediate", "The National Payments Corporation of India (NPCI) is an initiative of which two bodies?",
  ["RBI and the Indian Banks' Association", "RBI and SEBI", "Ministry of Finance and SBI", "NABARD and SIDBI"], "*",
  "NPCI",
  "NPCI is an umbrella organisation for retail payments and settlement systems, set up as an initiative of the RBI "
  "and the Indian Banks' Association under the Payment and Settlement Systems Act, 2007. It is a not-for-profit "
  "company and runs UPI, RuPay, IMPS and NACH.",
  ["NPCI: initiative of RBI and IBA", "Under the PSS Act, 2007"],
  [fact("NPCI, an umbrella organisation for retail payments, is an initiative of RBI and IBA under the PSS Act 2007",
        U["npci"])])

G(T, HQ, "Intermediate", "Where is the headquarters of the International Atomic Energy Agency (IAEA)?",
  ["Vienna", "Geneva", "New York", "The Hague"], "*",
  "IAEA",
  "The IAEA's Statute came into force in July 1957, inspired by President Eisenhower's 1953 'Atoms for Peace' "
  "speech. In October 1957 the first General Conference chose Vienna as headquarters; the Agency is at the Vienna "
  "International Centre.",
  ["IAEA HQ: Vienna", "Established 1957"],
  [fact("IAEA born 29 July 1957; First General Conference (Oct 1957) decided HQ in Vienna", U["iaea"])])

G(T, HQ, "Intermediate",
  "UNESCO's Constitution was signed in London in November 1945. Where is UNESCO headquartered?",
  ["Paris", "London", "Geneva", "New York"], "*",
  "UNESCO",
  "UNESCO's Constitution was signed in London on 16 November 1945 and came into force on 4 November 1946. A "
  "resolution of the London conference fixed Paris as the seat, and the first General Conference met in Paris in "
  "1946.",
  ["Constitution signed in London (1945)", "Seat: Paris"],
  [fact("UNESCO Constitution signed in London 16 Nov 1945, in force 4 Nov 1946; seat in Paris", U["unesco"])])

G(T, HQ, "Advanced",
  "Consider the following statements about the International Labour Organization (ILO):\n"
  "1. It was created in 1919 as part of the Treaty of Versailles.\n"
  "2. It has a tripartite structure of governments, employers and workers.\n"
  "3. It was awarded the Nobel Peace Prize in 1969.\n"
  "Which of the statements given above is/are correct?",
  S123, "D",
  "ILO",
  "The ILO was created in 1919 by the Treaty of Versailles together with the League of Nations, and became the UN's "
  "specialised agency for the world of work in 1946. It is the only tripartite UN agency (governments, employers, "
  "workers). It won the Nobel Peace Prize in 1969, its 50th anniversary. Headquarters: Geneva.",
  ["1: correct", "2: correct", "3: correct", "So all three"],
  [fact("ILO created 1919 under Treaty of Versailles; tripartite; Nobel Peace Prize 1969", U["ilo"])])

G(T, MB, "Advanced",
  "Consider the following statements about the World Bank Group:\n"
  "1. It consists of five institutions: IBRD, IDA, IFC, MIGA and ICSID.\n"
  "2. MIGA provides political risk insurance and credit enhancement for foreign direct investment.\n"
  "3. A country must be a member of the IMF before it can join the IBRD.\n"
  "4. ICSID provides concessional loans to the poorest countries.\n"
  "Which of the statements given above are correct?",
  S1234, "A",
  "World Bank Group institutions",
  "The World Bank Group has five legally separate institutions. IBRD lends to middle-income countries and IDA gives "
  "concessional loans and grants to the poorest; IFC finances the private sector; MIGA gives political risk "
  "insurance; ICSID settles investment disputes between states and foreign investors. IBRD membership requires IMF "
  "membership.",
  ["1, 2 and 3: correct", "4: wrong, concessional lending is IDA's job; ICSID resolves investment disputes",
   "So 1, 2 and 3 only"],
  [fact("WBG five institutions; MIGA political risk insurance; ICSID dispute settlement; IDA concessional",
        U["wbg_basics"]),
   fact("To become a member of the Bank, a country must first join the IMF", U["wb_members"])])

G(T, MB, "Advanced",
  "Consider the following statements about the International Monetary Fund:\n"
  "1. Its Articles of Agreement were adopted at the Bretton Woods conference in July 1944.\n"
  "2. Special Drawing Rights (SDRs) were created at the Bretton Woods conference.\n"
  "3. Its by-laws require its principal office to be located within the metropolitan area of Washington, D.C.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "1 and 2 only", "1 and 3 only", "1, 2 and 3"], "C",
  "IMF",
  "The IMF's Articles were adopted at the UN Monetary and Financial Conference at Bretton Woods on 22 July 1944. "
  "SDRs came much later, in 1969, as a supplementary international reserve asset. The by-laws place the principal "
  "office within the Washington, D.C. metropolitan area.",
  ["1: correct", "2: wrong, SDRs were created in 1969", "3: correct", "So 1 and 3 only"],
  [fact("IMF Articles adopted at Bretton Woods on 22 July 1944", U["imf_aa"]),
   fact("SDRs created in 1969 as an international reserve asset", U["imf_sdr"]),
   fact("Principal office of the Fund located within the metropolitan area of Washington, D.C.", U["imf_bylaws"])])

G(T, HQ, "Advanced",
  "Consider the following statements about the Financial Action Task Force (FATF):\n"
  "1. It was established by the G7 Summit held in Paris in 1989.\n"
  "2. Its secretariat is housed at the OECD in Paris.\n"
  "3. It is a specialised agency of the United Nations.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "1 and 2 only", "2 and 3 only", "1, 2 and 3"], "B",
  "FATF",
  "The FATF was created by the G7 Summit in Paris in 1989 to fight money laundering, and later also terrorist "
  "financing. Its small secretariat is housed at the OECD in Paris, but the FATF is a separate inter-governmental "
  "task force, not a UN agency. It maintains the 'grey' and 'black' lists of high-risk jurisdictions.",
  ["1: correct", "2: correct", "3: wrong", "So 1 and 2 only"],
  [fact("FATF created by G7 Summit in Paris 1989; Secretariat housed at the OECD; a task force of member governments",
        U["fatf"])])

G(T, MB, "Advanced",
  "Consider the following statements about BRICS membership:\n"
  "1. Egypt, Ethiopia, Iran and the UAE became members from 1 January 2024, following a decision at the Johannesburg "
  "Summit of August 2023.\n"
  "2. Indonesia formally joined as a full member in January 2025.\n"
  "3. Nigeria is a full member of BRICS.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "2 and 3 only", "1 and 2 only", "1, 2 and 3"], "C",
  "BRICS expansion",
  "Leaders at the XV BRICS Summit (Johannesburg, August 2023) admitted new members from 1 January 2024, including "
  "Egypt, Ethiopia, Iran and the UAE. Brazil's presidency announced Indonesia's formal entry on 6 January 2025. The "
  "Kazan Summit (2024) created a 'partner country' status; Nigeria joined BRICS as a partner country, not a member.",
  ["1: correct", "2: correct", "3: wrong, Nigeria is a partner country", "So 1 and 2 only"],
  [fact("Egypt, Ethiopia, Iran, UAE became members 1 Jan 2024 after XV Summit; Indonesia entry announced 6 Jan "
        "2025; partner country status created at Kazan; Nigeria a partner", U["brics"])],
  current=ca("2025-01-06"))

G(T, MB, "Advanced",
  "Consider the following statements about the G20:\n"
  "1. The African Union was made a permanent member of the G20 at the New Delhi Summit in September 2023.\n"
  "2. The first G20 summit in which the African Union took part as a permanent member was held in Rio de Janeiro "
  "in November 2024.\n"
  "Which of the statements given above is/are correct?",
  ["Neither 1 nor 2", "Only 2", "Only 1", "Both 1 and 2"], "D",
  "G20 membership",
  "Under India's presidency, the New Delhi Leaders' Declaration (9-10 September 2023) welcomed the African Union "
  "as a permanent member. The Rio de Janeiro summit of November 2024 was the first in which the AU took part as a "
  "permanent member. The G20 now has 19 countries, the European Union and the African Union.",
  ["1: correct", "2: correct", "So both"],
  [fact("New Delhi Leaders' Declaration welcomed the African Union as a permanent member", U["g20_decl"]),
   fact("Rio de Janeiro summit (Nov 2024) was the first in which the AU participated as a permanent member",
        U["g20_brief"])])

G(T, MB, "Advanced",
  "Consider the following statements:\n"
  "1. Timor-Leste was admitted as the eleventh member of ASEAN in October 2025.\n"
  "2. After this admission ASEAN has twelve member states.\n"
  "Which of the statements given above is/are correct?",
  ["Both 1 and 2", "Only 1", "Only 2", "Neither 1 nor 2"], "B",
  "ASEAN membership",
  "The declaration admitting Timor-Leste was signed at the opening of the 47th ASEAN Summit in Kuala Lumpur on "
  "26 October 2025, making it ASEAN's eleventh member. ASEAN therefore has eleven member states, not twelve.",
  ["1: correct", "2: wrong (eleven members)", "So only 1"],
  [fact("Timor-Leste admitted into ASEAN at the 47th ASEAN Summit on 26 October 2025; eleven Member States",
        U["asean_tl"])],
  current=ca("2025-10-26"))

G(T, HQ, "Advanced",
  "Consider the following statements about the Shanghai Cooperation Organisation:\n"
  "1. The Executive Committee of its Regional Anti-Terrorist Structure (RATS) is located in Tashkent.\n"
  "2. Its Secretariat is located in Moscow.\n"
  "3. Belarus became its tenth member state in 2024.\n"
  "Which of the statements given above is/are correct?",
  S123, "C",
  "SCO permanent bodies",
  "The SCO has two permanent bodies: the Secretariat in Beijing and the RATS Executive Committee in Tashkent, both "
  "working since January 2004. Iran became a member at the virtual summit hosted by India in July 2023, and "
  "Belarus became the tenth member at the Astana Summit in July 2024.",
  ["1: correct", "2: wrong, the Secretariat is in Beijing", "3: correct", "So 1 and 3 only"],
  [fact("SCO Secretariat in Beijing, RATS in Tashkent; Belarus joined as tenth member at Astana in July 2024",
        U["sco_mea"])],
  current=ca("2024-07-04"))

G(T, HQ, "Advanced",
  "Consider the following statements:\n"
  "1. NABARD took over the agricultural credit functions of the RBI and the refinance functions of the "
  "Agricultural Refinance and Development Corporation (ARDC).\n"
  "2. SIDBI was set up on 2 April 1990 under the SIDBI Act, 1989.\n"
  "3. NABARD's head office is in New Delhi.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "1 and 2 only", "2 and 3 only", "1, 2 and 3"], "B",
  "Development financial institutions",
  "NABARD came into existence on 12 July 1982 by transferring the agricultural credit functions of the RBI and the "
  "refinance functions of ARDC; its head office is in Mumbai, not New Delhi. SIDBI was set up on 2 April 1990 under "
  "the SIDBI Act, 1989, with its head office in Lucknow.",
  ["1: correct", "2: correct", "3: wrong (Mumbai)", "So 1 and 2 only"],
  [fact("NABARD took over RBI agricultural credit and ARDC refinance functions on 12 July 1982; head office Mumbai",
        U["nabard"]),
   fact("SIDBI set up 2 April 1990 under SIDBI Act 1989", U["sidbi"])])

# ====================================================================== Important Reports and Indexes (8 / 10 / 8)
T, PB, IR = "Important Reports and Indexes", "Publishing body", "India's rank"

G(T, PB, "Basic", "The World Press Freedom Index is published by which organisation?",
  ["Reporters Without Borders (RSF)", "Freedom House", "Amnesty International", "Transparency International"], "*",
  "World Press Freedom Index",
  "The World Press Freedom Index has been published every year since 2002 by Reporters Without Borders (RSF), "
  "based in Paris. It ranks 180 countries and territories.",
  ["Publisher: RSF", "Annual since 2002, 180 countries"],
  [fact("World Press Freedom Index published every year since 2002 by RSF; 180 countries", U["rsf"])],
  why="Freedom House publishes 'Freedom in the World'; Transparency International publishes the CPI.")

G(T, PB, "Basic", "Which organisation publishes the Corruption Perceptions Index (CPI)?",
  ["Transparency International", "World Bank", "Amnesty International", "International Monetary Fund"], "*",
  "Corruption Perceptions Index",
  "Transparency International's CPI ranks countries by perceived public-sector corruption on a scale from "
  "0 (highly corrupt) to 100 (very clean), drawing on independent expert and business surveys.",
  ["CPI publisher: Transparency International", "Scale 0-100"],
  [fact("Transparency International's CPI measures perceived public-sector corruption on a 0-100 scale",
        U["cpi"])])

G(T, PB, "Basic", "The Global Gender Gap Report is published by which organisation?",
  ["World Economic Forum", "UN Women", "UNDP", "World Bank"], "*",
  "Global Gender Gap Report",
  "The World Economic Forum introduced the Global Gender Gap Index in 2006 and publishes it every year. It measures "
  "gaps between women and men in four areas.",
  ["Publisher: World Economic Forum", "First edition 2006"],
  [fact("WEF first introduced the Global Gender Gap Index in 2006; published annually", U["gggr"])],
  why="UNDP publishes the Gender Development Index and Gender Inequality Index in its Human Development Report.")

G(T, PB, "Basic", "The Human Development Report, which contains the Human Development Index, is published by:",
  ["United Nations Development Programme (UNDP)", "World Bank", "UNESCO", "World Health Organization"], "*",
  "Human Development Report",
  "The HDR is published by UNDP's Human Development Report Office. The HDI combines life expectancy, education "
  "(expected and mean years of schooling) and GNI per capita.",
  ["HDR publisher: UNDP", "HDI dimensions: health, education, income"],
  [fact("UNDP's Human Development Report ranks countries on HDI", U["hdr_india"])])

G(T, PB, "Basic", "The Global Innovation Index is published by which organisation?",
  ["World Intellectual Property Organization (WIPO)", "World Trade Organization", "World Economic Forum",
   "UNCTAD"], "*",
  "Global Innovation Index",
  "WIPO, the UN agency for intellectual property based in Geneva, publishes the Global Innovation Index every year. "
  "It ranks about 140 economies on innovation inputs and outputs using about 80 indicators.",
  ["GII publisher: WIPO", "Annual ranking of about 140 economies"],
  [fact("India ranking in the Global Innovation Index 2025, published by WIPO", U["gii_wipo"])])

G(T, PB, "Basic", "The World Investment Report, which tracks global foreign direct investment, is published by:",
  ["UNCTAD", "World Trade Organization", "International Monetary Fund", "OECD"], "*",
  "World Investment Report",
  "The World Investment Report is UNCTAD's annual flagship on FDI trends and investment policy. UNCTAD (UN Trade and "
  "Development) is headquartered in Geneva.",
  ["WIR publisher: UNCTAD", "Subject: FDI flows and policy"],
  [fact("World Investment Report 2026 published by UNCTAD", U["wir"])])

G(T, PB, "Basic", "The 'Global Economic Prospects' report, released every January and June, is published by:",
  ["World Bank", "International Monetary Fund", "OECD", "World Economic Forum"], "*",
  "Global Economic Prospects",
  "Global Economic Prospects is a World Bank flagship report published twice a year (January and June), with a "
  "special focus on emerging market and developing economies.",
  ["GEP publisher: World Bank", "Semiannual: January and June"],
  [fact("Global Economic Prospects is a semiannual (January and June) World Bank flagship report", U["gep"])],
  why="The IMF publishes the World Economic Outlook (April and October).")

G(T, PB, "Basic", "In India, the Financial Stability Report is published by:",
  ["Reserve Bank of India", "Securities and Exchange Board of India", "Ministry of Finance", "NITI Aayog"], "*",
  "Financial Stability Report",
  "The RBI publishes the Financial Stability Report. It draws contributions from all financial sector regulators "
  "and assesses risks to the stability of the Indian financial system.",
  ["FSR publisher: RBI", "Covers risks to financial stability"],
  [fact("The FSR is published by the RBI", U["fsr"])])

G(T, PB, "Intermediate", "The Global Hunger Index is jointly published by which organisations?",
  ["Welthungerhilfe and Concern Worldwide", "FAO and World Food Programme", "IFPRI and the World Bank",
   "UNICEF and WHO"], "*",
  "Global Hunger Index",
  "The GHI is a peer-reviewed annual report co-published by Welthungerhilfe (Bonn) and Concern Worldwide (Dublin). "
  "It scores countries on undernourishment, child stunting, child wasting and child mortality.",
  ["Publishers: Welthungerhilfe and Concern Worldwide", "Four indicators"],
  [fact("GHI published by Welthungerhilfe (Bonn) and Concern Worldwide (Dublin)", U["ghi"])],
  why="FAO, IFAD, UNICEF, WFP and WHO jointly publish a different report, SOFI.")

G(T, PB, "Intermediate",
  "The World Happiness Report is published by the Wellbeing Research Centre of which university, in partnership with "
  "Gallup and the UN Sustainable Development Solutions Network?",
  ["University of Oxford", "Harvard University", "University of Cambridge", "Columbia University"], "*",
  "World Happiness Report",
  "The annual World Happiness Report is published by the University of Oxford's Wellbeing Research Centre in "
  "partnership with Gallup, the UN Sustainable Development Solutions Network and an editorial board. Its main data "
  "source is the Gallup World Poll.",
  ["Publisher: Oxford Wellbeing Research Centre", "Partners: Gallup, UN SDSN"],
  [fact("WHR published by the University of Oxford's Wellbeing Research Centre with Gallup and UN SDSN",
        U["whr_about"])])

G(T, PB, "Intermediate", "The Global Peace Index is published by which organisation?",
  ["Institute for Economics & Peace", "Stockholm International Peace Research Institute", "Brookings Institution",
   "Chatham House"], "*",
  "Global Peace Index",
  "The Institute for Economics & Peace (IEP), a Sydney-headquartered think tank, publishes the Global Peace Index, "
  "the Global Terrorism Index and the Positive Peace Report.",
  ["GPI publisher: IEP (Sydney)", "IEP also publishes the Global Terrorism Index"],
  [fact("IEP develops the Global Peace Index, Global Terrorism Index and Positive Peace", U["iep"])],
  why="SIPRI is known for its military expenditure and arms transfer databases.")

G(T, PB, "Intermediate", "The World Competitiveness Ranking is published by:",
  ["IMD World Competitiveness Center, Lausanne", "World Economic Forum, Geneva", "OECD, Paris",
   "World Bank, Washington"], "*",
  "World Competitiveness Ranking",
  "The IMD World Competitiveness Center at IMD business school in Lausanne, Switzerland, publishes the World "
  "Competitiveness Ranking (yearbook since 1989), along with the World Digital Competitiveness and World Talent "
  "rankings.",
  ["Publisher: IMD, Lausanne", "Yearbook since 1989"],
  [fact("World Competitiveness Ranking by IMD World Competitiveness Center", U["imd"])],
  why="The WEF published the Global Competitiveness Report, a different report.")

G(T, PB, "Intermediate", "The Environmental Performance Index is produced jointly by:",
  ["Yale University and Columbia University", "Harvard University and MIT", "Oxford and Cambridge",
   "Stanford and Princeton"], "*",
  "Environmental Performance Index",
  "The EPI is produced by the Yale Center for Environmental Law & Policy and the Center for International Earth "
  "Science Information Network (CIESIN) at Columbia University. It ranks countries on environmental health, "
  "ecosystem vitality and climate change.",
  ["EPI: Yale (YCELP) and Columbia (CIESIN)", "Three policy objectives"],
  [fact("EPI is run by the Yale Center for Environmental Law & Policy and CIESIN at Columbia University",
        U["epi"])])

G(T, PB, "Intermediate", "The Global Multidimensional Poverty Index is published jointly by UNDP and:",
  ["Oxford Poverty and Human Development Initiative (OPHI)", "World Bank", "UNICEF", "International Labour "
                                                                                      "Organization"], "*",
  "Global MPI",
  "The global MPI was developed by OPHI (University of Oxford) with UNDP for the 2010 Human Development Report and "
  "has been published annually since. A person is 'MPI poor' if deprived in a third or more of ten weighted "
  "indicators across health, education and living standards.",
  ["Publishers: OPHI and UNDP", "Ten indicators, three dimensions"],
  [fact("Global MPI developed by OPHI with UNDP in 2010 and published annually; ten weighted indicators",
        U["mpi"])])

G(T, IR, "Intermediate",
  "In the World Bank's Logistics Performance Index 2023, what was India's rank out of 139 countries?",
  ["22nd", "38th", "44th", "54th"], "B",
  "Logistics Performance Index",
  "India ranked 38th of 139 countries in the World Bank's LPI 2023, up six places from 44th in 2018 (and from 54th "
  "in 2014). The government credits PM GatiShakti and the National Logistics Policy.",
  ["LPI 2023: India 38th of 139", "2018: 44th; 2014: 54th"],
  [fact("India ranks 38 of 139 in LPI 2023; improved from 44 (2018) and 54 (2014)", U["lpi"])],
  current=ca("2023-04-21"))

G(T, IR, "Intermediate",
  "In UNDP's Human Development Report 2025, what was India's HDI rank out of 193 countries?",
  ["126th", "130th", "134th", "142nd"], "B",
  "Human Development Index",
  "India ranked 130th of 193 countries in the HDR 2025 with an HDI value of 0.685 (for 2023), in the medium human "
  "development category. Inequality reduces India's HDI by 30.7%.",
  ["HDR 2025: India 130 of 193", "HDI 0.685"],
  [fact("India ranks 130 out of 193 countries in the 2025 HDR; HDI 0.685", U["hdr_india"])],
  why="134 was India's rank in the 2023-24 report.", current=ca("2025-05-06"))

G(T, IR, "Intermediate", "What was India's rank in WIPO's Global Innovation Index 2025?",
  ["39th", "40th", "38th", "48th"], "C",
  "Global Innovation Index",
  "India ranked 38th in the GII 2025, its best so far, up from 66th in 2019 and 81st in 2015. It ranks first in "
  "the Central and Southern Asia region.",
  ["GII 2025: India 38th", "2019: 66th"],
  [fact("India's GII rank improved to 38th in 2025 from 66th in 2019", U["gii_pib"])],
  current=ca("2025-09-16"))

G(T, PB, "Intermediate", "The 'State of World Population' report is the annual flagship publication of which body?",
  ["United Nations Population Fund (UNFPA)", "UN Department of Economic and Social Affairs", "UNDP",
   "World Health Organization"], "*",
  "State of World Population",
  "The State of World Population report is UNFPA's annual flagship. Each edition takes up a population or sexual "
  "and reproductive health theme; the 2025 edition was titled 'The real fertility crisis'.",
  ["SWOP publisher: UNFPA", "Annual"],
  [fact("State of World Population 2025 published by UNFPA", U["swop"])],
  why="UN DESA publishes 'World Population Prospects', a different report.")

G(T, PB, "Advanced",
  "Consider the following statements about the Global Hunger Index (GHI):\n"
  "1. It is based on four indicators: undernourishment, child stunting, child wasting and child mortality.\n"
  "2. All four indicators carry equal weight in the GHI score.\n"
  "Which of the statements given above is/are correct?",
  ["Both 1 and 2", "Only 2", "Neither 1 nor 2", "Only 1"], "D",
  "GHI methodology",
  "The GHI combines four indicators. Undernourishment and child mortality each contribute one-third of the score, "
  "while child stunting and child wasting each contribute one-sixth, so the weights are not equal.",
  ["1: correct", "2: wrong (1/3, 1/3, 1/6, 1/6)", "So only 1"],
  [fact("GHI: undernourishment and child mortality one-third each; stunting and wasting one-sixth each", U["ghi"])])

G(T, PB, "Advanced",
  "In the RBI's Financial Inclusion Index (FI-Index), which of the three sub-indices carries the highest weight?",
  ["Usage", "Access", "Quality", "All three carry equal weight"], "*",
  "FI-Index",
  "The RBI's FI-Index (0 to 100) has three sub-indices: Access (35%), Usage (45%) and Quality (20%), built from 97 "
  "indicators. It is published annually; the index for March 2025 was 67.0.",
  ["Weights: Access 35, Usage 45, Quality 20", "So Usage has the highest weight"],
  [fact("FI-Index sub-indices Access 35%, Usage 45%, Quality 20%; 97 indicators", U["fiindex"])])

G(T, PB, "Advanced",
  "Consider the following statements about the RBI's Financial Stability Report (FSR):\n"
  "1. It is a half-yearly publication.\n"
  "2. It presents the collective assessment of the Sub-Committee of the Financial Stability and Development Council "
  "(FSDC).\n"
  "3. It is published by the Ministry of Finance.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "Financial Stability Report",
  "The FSR is a half-yearly RBI publication (June and December) with contributions from all financial sector "
  "regulators. It reflects the collective assessment of the Sub-Committee of the FSDC (chaired by the RBI "
  "Governor) on risks to financial stability.",
  ["1: correct", "2: correct", "3: wrong, it is an RBI publication", "So 1 and 2 only"],
  [fact("FSR is a half-yearly publication presenting the collective assessment of the Sub Committee of the FSDC",
        U["fsr"])])

G(T, PB, "Advanced",
  "Consider the following statements about the World Happiness Report:\n"
  "1. Country rankings are based on life evaluations on the Cantril ladder (0 to 10) from the Gallup World Poll.\n"
  "2. The ranking score is a composite index that adds up weighted values of GDP, life expectancy and other "
  "metrics.\n"
  "Which of the statements given above is/are correct?",
  ["Only 1", "Only 2", "Both 1 and 2", "Neither 1 nor 2"], "A",
  "World Happiness Report method",
  "Rankings use people's own answers on the Cantril ladder (0 = worst possible life, 10 = best), averaged over three "
  "years. GDP per capita, social support and other factors are used only to explain the differences; the report "
  "does not build a composite index.",
  ["1: correct", "2: wrong, the ranking is not a composite index", "So only 1"],
  [fact("Rankings based on Cantril ladder from the Gallup World Poll rather than an index from multiple metrics",
        U["whr_faq"])])

G(T, PB, "Advanced",
  "Consider the following statements about the World Press Freedom Index:\n"
  "1. It has been published every year since 2002.\n"
  "2. It ranks 180 countries and territories.\n"
  "3. It measures the quality of journalism in each country.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "1 and 3 only", "2 and 3 only", "1 and 2 only"], "D",
  "World Press Freedom Index method",
  "RSF's Index, published every year since 2002, ranks 180 countries and territories on political, economic, legal, "
  "social and security indicators. It measures the conditions for press freedom, not the quality of journalism.",
  ["1: correct", "2: correct", "3: wrong", "So 1 and 2 only"],
  [fact("Published every year since 2002; 180 countries; not a measure of journalism quality", U["rsf"])])

G(T, IR, "Advanced",
  "In NITI Aayog's SDG India Index 2023-24 (the fourth edition), what was India's overall composite score?",
  ["57", "66", "71", "75"], "C",
  "SDG India Index",
  "The SDG India Index 2023-24, released on 12 July 2024, gave India a composite score of 71, up from 66 in 2020-21 "
  "and 57 in the 2018 baseline. It tracks States and UTs on 113 indicators aligned to MoSPI's National Indicator "
  "Framework. Goal 13 (Climate Action) improved the most.",
  ["2018: 57", "2020-21: 66", "2023-24: 71"],
  [fact("Overall SDG score 71 for 2023-24, up from 66 (2020-21) and 57 (2018); 113 indicators", U["sdgindex"])],
  current=ca("2024-07-12"))

G(T, PB, "Advanced", "Which of the following is NOT one of the four subindexes of the Global Gender Gap Index?",
  ["Digital Access", "Political Empowerment", "Health and Survival", "Educational Attainment"], "*",
  "Global Gender Gap Index structure",
  "The Global Gender Gap Index has four subindexes: Economic Participation and Opportunity, Educational Attainment, "
  "Health and Survival, and Political Empowerment. Political Empowerment has the largest remaining gap.",
  ["Four subindexes: economic, education, health, political", "Digital access is not one of them"],
  [fact("GGGI subindexes: Economic Participation and Opportunity, Educational Attainment, Health and Survival, "
        "Political Empowerment", U["gggr"])])

G(T, IR, "Advanced",
  "Consider the following statements about India in the Global Innovation Index (GII):\n"
  "1. India was ranked 66th in 2019.\n"
  "2. In 2025 India topped the lower middle-income group of economies.\n"
  "Which of the statements given above is/are correct?",
  ["Only 1", "Only 2", "Neither 1 nor 2", "Both 1 and 2"], "D",
  "India in the GII",
  "The Economic Survey 2025-26 notes that India's GII rank rose from 66th in 2019 to 38th in 2025. This places India "
  "at the top of the lower middle-income group and first in Central and Southern Asia.",
  ["1: correct", "2: correct", "So both"],
  [fact("GII rank improved from 66th in 2019 to 38th in 2025; top of lower middle-income group", U["gii_pib"])],
  current=ca("2026-01-29"))

# ====================================================================== Government Policies (5 / 7 / 5)
T, PC, RR = "Government Policies", "Policy changes", "Regulatory reforms"

G(T, RR, "Basic", "The Goods and Services Tax (GST) was rolled out in India from which date?",
  ["1 April 2017", "1 July 2017", "1 October 2017", "1 January 2018"], "B",
  "GST launch",
  "GST was rolled out at midnight on 30 June-1 July 2017 at a ceremony in the Central Hall of Parliament. It "
  "replaced many central and state taxes such as excise duty, service tax, VAT and entry tax. 1 July is observed as "
  "GST Day.",
  ["GST roll-out: 1 July 2017", "So the answer is 1 July 2017"],
  [fact("GST rolled out on the midnight of 1 July 2017 in the Central Hall of Parliament", U["gst_factsheet"])])

G(T, RR, "Basic", "Who chairs the GST Council?",
  ["Union Finance Minister", "Prime Minister", "Governor of the RBI", "Chairman of the CBIC"], "*",
  "GST Council",
  "Under Article 279A, the GST Council is a joint forum of the Centre and the States. The Union Finance Minister is "
  "its Chairperson; the Union Minister of State for Revenue and the Finance or Taxation Ministers of the States are "
  "members.",
  ["Article 279A: GST Council", "Chairperson: Union Finance Minister"],
  [fact("GST Council under Article 279A: Union Finance Minister as Chairperson, MoS Revenue and State Finance "
        "Ministers as members", U["gst_council"])])

G(T, PC, "Basic", "The Income-tax Act, 2025, which came into force on 1 April 2026, replaced which law?",
  ["Income-tax Act, 1961", "Income-tax Act, 1922", "Finance Act, 1994", "Direct Taxes Code Bill, 2010"], "*",
  "Income-tax Act, 2025",
  "The Income-tax Act, 2025 was passed by Parliament on 12 August 2025, received assent on 21 August 2025 and came "
  "into force on 1 April 2026, replacing the Income-tax Act, 1961. It simplifies language and roughly halves the "
  "word count, without major rate changes.",
  ["New law: Income-tax Act, 2025", "Replaced: Income-tax Act, 1961"],
  [fact("Income-tax Act, 2025 came into force on 1 April 2026, replacing the Income-tax Act, 1961", U["itact"])])

G(T, PC, "Basic", "Under the National Education Policy 2020, the 10+2 school structure is replaced by which structure?",
  ["5+3+3+4", "4+4+4+3", "5+5+2+3", "3+4+3+5"], "*",
  "National Education Policy 2020",
  "NEP 2020, approved on 29 July 2020, replaces the 10+2 structure with 5+3+3+4, covering ages 3-8 (foundational), "
  "8-11 (preparatory), 11-14 (middle) and 14-18 (secondary). This brings ages 3-6 into the school curriculum for "
  "the first time.",
  ["New structure: 5+3+3+4", "Ages 3-8, 8-11, 11-14, 14-18"],
  [fact("10+2 replaced by 5+3+3+4 corresponding to ages 3-8, 8-11, 11-14 and 14-18", U["nep"])],
  shortcut="Add the years: 5+3+3+4 = 15 years, from age 3 to 18.")

G(T, RR, "Basic",
  "How many Labour Codes did the Government of India make effective from 21 November 2025, consolidating 29 central "
  "labour laws?",
  ["Two", "Three", "Four", "Five"], "C",
  "Labour Codes",
  "From 21 November 2025 the Government made four Labour Codes effective: the Code on Wages, 2019; the Industrial "
  "Relations Code, 2020; the Code on Social Security, 2020; and the Occupational Safety, Health and Working "
  "Conditions Code, 2020. Together they replace 29 central labour laws.",
  ["Four codes", "Replacing 29 central laws"],
  [fact("Four Labour Codes effective 21 November 2025, consolidating 29 Central labour laws", U["labourcodes"])],
  current=ca("2025-11-21"))

G(T, RR, "Intermediate",
  "Under the GST rate rationalisation effective from 22 September 2025, what are the two main GST rates?",
  ["5% and 12%", "5% and 18%", "12% and 18%", "12% and 28%"], "B",
  "Next-generation GST reform",
  "On the recommendation of the 56th GST Council meeting (3 September 2025), the four-slab structure (5, 12, 18, "
  "28%) was replaced from 22 September 2025 by two main rates, 5% (merit) and 18% (standard), plus a special 40% "
  "rate for a few sin and luxury goods.",
  ["Main rates: 5% and 18%", "Special rate 40%"],
  [fact("56th GST Council: two main rates 5% and 18% plus special 40%; effective 22 September 2025", U["gst56"])],
  current=ca("2025-09-22"))

G(T, RR, "Intermediate",
  "After the GST changes effective 22 September 2025, what is the special GST rate applied to a few sin and luxury "
  "goods, such as cars above 1500 cc?",
  ["28%", "35%", "40%", "50%"], "C",
  "Special GST rate",
  "The special 40% rate covers a few sin and luxury goods, such as mid-size and large cars (above 1500 cc or longer "
  "than 4000 mm) and motorcycles above 350 cc. Most of these goods earlier carried 28% GST plus compensation cess; "
  "the cess was merged into the GST rate as the cess is being ended.",
  ["Special rate: 40%", "Example: cars above 1500 cc, motorcycles above 350 cc"],
  [fact("Special 40% rate on few sin and luxury goods; cars above 1500 cc or 4000 mm at 40%; motorcycles above "
        "350 cc at 40%", U["gst56faq"])],
  why="28% was the highest regular slab before the reform.", current=ca("2025-09-22"))

G(T, PC, "Intermediate",
  "The Income-tax Act, 2025 replaces the concepts of 'Previous Year' and 'Assessment Year' with which single "
  "concept?",
  ["Tax Year", "Fiscal Period", "Accounting Year", "Revenue Year"], "*",
  "Income-tax Act, 2025: Tax Year",
  "The new Act uses one term, 'Tax Year', defined as the twelve-month financial year starting on 1 April, in place of "
  "the old pair of 'Previous Year' (when income is earned) and 'Assessment Year' (when it is assessed).",
  ["Old: Previous Year + Assessment Year", "New: Tax Year (from 1 April)"],
  [fact("Income-tax Act 2025 replaces 'Assessment Year' and 'Previous Year' with a single 'Tax Year'",
        U["itact"])])

G(T, RR, "Intermediate",
  "The Jan Vishwas (Amendment of Provisions) Act, 2023 decriminalised 183 provisions in how many Central Acts?",
  ["19", "42", "76", "183"], "B",
  "Jan Vishwas Act, 2023",
  "The Jan Vishwas Act, 2023 decriminalised 183 provisions in 42 Central Acts administered by 19 ministries and "
  "departments, replacing many imprisonment clauses for minor and technical offences with monetary penalties to "
  "improve ease of living and doing business.",
  ["183 provisions", "42 Acts", "19 ministries/departments"],
  [fact("Jan Vishwas Act 2023 decriminalized 183 provisions under 42 Acts administered by 19 Ministries/Departments",
        U["janvishwas"])],
  why="19 is the number of ministries/departments and 183 the number of provisions.")

G(T, RR, "Intermediate",
  "Under the Insolvency and Bankruptcy Code, 2016, the corporate insolvency resolution process must be completed "
  "within an outer limit of how many days, including extensions and litigation time?",
  ["180 days", "270 days", "330 days", "365 days"], "C",
  "IBC timelines",
  "The CIRP must normally finish within 180 days of admission, extendable once by up to 90 days with a 66% vote of "
  "the committee of creditors. A 2019 amendment set an overall cap of 330 days that includes extensions and time "
  "taken in legal proceedings. If no resolution plan is approved, the corporate debtor goes into liquidation.",
  ["Normal: 180 days", "Extension: up to 90 days", "Outer limit: 330 days"],
  [fact("CIRP 180 days, one extension up to 90 days, overall 330 days including legal proceedings", U["ibc_faq"])],
  why="270 days = 180 + 90, without litigation time.")

G(T, PC, "Intermediate", "India's Foreign Trade Policy 2023 came into effect on which date?",
  ["1 April 2021", "1 April 2022", "1 October 2022", "1 April 2023"], "D",
  "Foreign Trade Policy 2023",
  "The Foreign Trade Policy 2023 was launched on 31 March 2023 and came into effect on 1 April 2023. Unlike earlier "
  "five-year policies, it has no fixed end date and is updated as needed. It is administered by the DGFT under the "
  "Ministry of Commerce and Industry.",
  ["Launched 31 March 2023", "Effective 1 April 2023"],
  [fact("FTP 2023 launched on 31 March 2023 and came into effect from 1 April 2023", U["ftp"])])

G(T, PC, "Intermediate",
  "Under the corporate tax cuts of September 2019, what is the base income-tax rate for new domestic manufacturing "
  "companies incorporated on or after 1 October 2019 that claim no exemptions?",
  ["15%", "17%", "22%", "25%"], "A",
  "Corporate tax reform, 2019",
  "The Taxation Laws (Amendment) Ordinance, 2019 let existing domestic companies pay 22% (effective 25.17% with "
  "surcharge and cess) and new domestic manufacturing companies incorporated on or after 1 October 2019 pay 15% "
  "(effective 17.01%), if they give up exemptions and incentives.",
  ["New manufacturing companies: 15% (effective 17.01%)", "Other domestic companies: 22% (effective 25.17%)"],
  [fact("15% for new domestic manufacturing companies incorporated on or after 1 October 2019; 22% for existing "
        "domestic companies", U["corptax"])],
  why="22% is the rate for existing domestic companies; 17% is close to the effective rate including surcharge "
      "and cess.", current=ca("2019-09-20"))

G(T, RR, "Advanced",
  "Consider the following statements about GST:\n"
  "1. It was introduced through the Constitution (101st Amendment) Act, 2016.\n"
  "2. The GST Council is constituted under Article 279A of the Constitution.\n"
  "3. At its launch in 2017, GST had a single uniform rate of 18%.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "1 and 3 only", "2 and 3 only", "1 and 2 only"], "D",
  "Constitutional basis of GST",
  "GST was enabled by the Constitution (101st Amendment) Act, 2016 (the 122nd Amendment Bill), which inserted "
  "Article 279A for the GST Council. At launch GST had four main slabs of 5%, 12%, 18% and 28%, not a single rate.",
  ["1: correct", "2: correct", "3: wrong (four slabs)", "So 1 and 2 only"],
  [fact("Constitution (101st Amendment) Act 2016; Article 279A GST Council; four-slab structure 5, 12, 18, 28%",
        U["gst_factsheet"])])

G(T, RR, "Advanced",
  "Consider the following statements about the Labour Codes made effective in November 2025:\n"
  "1. Fixed-term employees become eligible for gratuity after one year of service instead of five.\n"
  "2. ESIC coverage is mandatory for establishments with more than 10 employees.\n"
  "3. The four codes together replace 44 central labour laws.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "1 and 2 only", "2 and 3 only", "1, 2 and 3"], "B",
  "Labour Codes",
  "The Labour Codes reduce the gratuity eligibility period for fixed-term employees to one year, extend ESIC "
  "coverage on a mandatory basis to establishments with more than 10 employees and give every worker a statutory "
  "right to minimum wages. They consolidate 29 central labour laws, not 44.",
  ["1: correct", "2: correct", "3: wrong (29 laws)", "So 1 and 2 only"],
  [fact("Labour Codes: gratuity after one year for fixed-term employees; ESIC mandatory for more than 10 employees; "
        "29 central laws", U["labourcodes"])],
  current=ca("2025-11-21"))

G(T, RR, "Advanced",
  "Consider the following statements about India's data protection framework:\n"
  "1. The Digital Personal Data Protection Rules, 2025 were notified in November 2025 to operationalise the DPDP "
  "Act, 2023.\n"
  "2. Appeals against decisions of the Data Protection Board of India lie with the TDSAT.\n"
  "3. The highest penalty, up to ₹250 crore, applies to a Data Fiduciary's failure to maintain reasonable security "
  "safeguards.\n"
  "4. The Rules give organisations a phased compliance period of 36 months.\n"
  "Which of the statements given above are correct?",
  S1234, "A",
  "DPDP Act and Rules",
  "The DPDP Rules, 2025 were notified in November 2025, fully operationalising the DPDP Act, 2023. They set up a "
  "fully digital Data Protection Board; appeals go to TDSAT. The highest penalty (up to ₹250 crore) is for failing "
  "to maintain reasonable security safeguards. The phased compliance timeline is 18 months, not 36.",
  ["1, 2 and 3: correct", "4: wrong (18 months)", "So 1, 2 and 3 only"],
  [fact("DPDP Rules 2025 notified; Data Protection Board; appeals to TDSAT; 18-month phased compliance; penalty up to "
        "₹250 crore for security safeguards failure", U["dpdp"])],
  current=ca("2025-11-14"))

G(T, PC, "Advanced",
  "Consider the following statements about the National Education Policy 2020:\n"
  "1. It was approved by the Union Cabinet on 29 July 2020.\n"
  "2. It replaced the National Policy on Education, 1986.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "National Education Policy 2020",
  "The Union Cabinet approved NEP 2020 on 29 July 2020. It replaced the 34-year-old National Policy on Education, "
  "1986, and is the first education policy of the 21st century.",
  ["1: correct", "2: correct", "So both"],
  [fact("NEP 2020 approved 29 July 2020; replaces the National Policy on Education, 1986", U["nep"])])

G(T, PC, "Advanced",
  "Consider the following statements about the corporate tax reform of September 2019:\n"
  "1. Domestic companies opting for the 22% rate have an effective tax rate of 25.17%, including surcharge and cess.\n"
  "2. Companies opting for the 22% rate are exempt from Minimum Alternate Tax (MAT).\n"
  "3. The 22% option is available only to companies incorporated on or after 1 October 2019.\n"
  "Which of the statements given above is/are correct?",
  ["1 and 2 only", "2 only", "1 and 3 only", "1, 2 and 3"], "A",
  "Corporate tax reform, 2019",
  "Any domestic company that gives up exemptions and incentives can opt for 22% (effective 25.17%) and is then not "
  "required to pay MAT. The 1 October 2019 incorporation condition applies only to the separate 15% option for new "
  "manufacturing companies.",
  ["1: correct", "2: correct", "3: wrong, that condition is for the 15% option", "So 1 and 2 only"],
  [fact("22% option for domestic companies, effective 25.17%, not required to pay MAT; 15% for new manufacturing "
        "companies incorporated on or after 1 Oct 2019", U["corptax"])],
  current=ca("2019-09-20"))

# ====================================================================== Static Awareness (7 / 10 / 7)
T, CC, NP, SF = "Static Awareness", "Capitals and currencies", "National parks and dams", "Indian states facts"

G(T, CC, "Basic", "What is the currency of Bhutan?",
  ["Ngultrum", "Taka", "Kyat", "Rufiyaa"], "*",
  "Currencies of neighbouring countries",
  "Bhutan's currency is the ngultrum (BTN), pegged at par with the Indian rupee. Its capital is Thimphu.",
  ["Bhutan: ngultrum, capital Thimphu"],
  [fact("Bhutan: capital Thimphu; currency ngultrum (BTN)", U["cia_bhutan"])],
  why="Taka: Bangladesh; Kyat: Myanmar; Rufiyaa: Maldives.")

G(T, CC, "Basic", "What is the capital of Kazakhstan?",
  ["Astana", "Almaty", "Tashkent", "Bishkek"], "*",
  "Capitals of Central Asia",
  "Kazakhstan's capital is Astana; its currency is the tenge. Almaty is its largest city and former capital.",
  ["Kazakhstan: capital Astana, currency tenge"],
  [fact("Kazakhstan: capital Astana; currency tenge (KZT)", U["cia_kaz"])],
  why="Tashkent is the capital of Uzbekistan and Bishkek of Kyrgyzstan.")

G(T, CC, "Basic", "What is the capital of Vietnam?",
  ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hue"], "*",
  "Capitals of South-East Asia",
  "Vietnam's capital is Hanoi; its currency is the dong. Ho Chi Minh City (formerly Saigon) is its largest city.",
  ["Vietnam: capital Hanoi, currency dong"],
  [fact("Vietnam: capital Hanoi (Ha Noi)", U["cia_vietnam"])])

G(T, NP, "Basic", "Kaziranga National Park, famous for the one-horned rhinoceros, is in which state?",
  ["Assam", "West Bengal", "Arunachal Pradesh", "Meghalaya"], "*",
  "National parks of India",
  "Kaziranga National Park in Assam was inscribed as a UNESCO World Heritage Site in 1985. It holds the world's "
  "largest population of the greater one-horned rhinoceros.",
  ["Kaziranga: Assam", "Largest one-horned rhino population"],
  [fact("Kaziranga National Park, Assam, inscribed 1985; largest population of Indian one-horned rhino",
        U["kaziranga"])])

G(T, NP, "Basic", "The Gir landscape of Gujarat is the only wild home of which animal?",
  ["Asiatic lion", "Bengal tiger", "Snow leopard", "One-horned rhinoceros"], "*",
  "Gir and the Asiatic lion",
  "The Asiatic lion survives in the wild only in the Gir landscape of Gujarat. The population rose from 674 in 2020 "
  "to 891 in 2025; the census is held every five years.",
  ["Asiatic lion: only in Gir landscape, Gujarat"],
  [fact("Asiatic lion population in Gir landscape rose from 674 (2020) to 891 (2025)", U["gir"])])

G(T, NP, "Basic", "The Tehri Dam in Uttarakhand is built on which river?",
  ["Bhagirathi", "Alaknanda", "Yamuna", "Sharda"], "*",
  "Dams of India",
  "Tehri Dam is a 260.5 m earth and rockfill dam on the Bhagirathi, just downstream of its confluence with the "
  "Bhilangana, in Uttarakhand. THDC India Ltd operates it.",
  ["Tehri Dam: Bhagirathi river", "Height 260.5 m"],
  [fact("Tehri: 260.5 m earth and rockfill dam across River Bhagirathi; THDC", U["tehri"])])

G(T, SF, "Basic", "In which year did Telangana come into existence as a separate state?",
  ["2000", "2011", "2014", "2019"], "C",
  "Formation of states",
  "Telangana, India's youngest state, came into existence on 2 June 2014 under the Andhra Pradesh Reorganisation "
  "Act, 2014. 2 June is Telangana Formation Day.",
  ["Telangana formed: 2 June 2014"],
  [fact("Telangana, India's youngest State, came into existence on 2 June 2014", U["telangana"])],
  why="2000 saw the creation of Chhattisgarh, Uttarakhand and Jharkhand; in 2019 J&K was reorganised into UTs.")

G(T, CC, "Intermediate", "Which city is the administrative capital of Myanmar?",
  ["Nay Pyi Taw", "Yangon", "Mandalay", "Bago"], "*",
  "Capitals of neighbouring countries",
  "Myanmar's administrative capital is Nay Pyi Taw; Yangon (Rangoon) was the earlier capital and is the largest "
  "city. Myanmar's currency is the kyat.",
  ["Myanmar: administrative capital Nay Pyi Taw, currency kyat"],
  [fact("Burma: Nay Pyi Taw is the administrative capital; currency kyat (MMK)", U["cia_burma"])])

G(T, CC, "Intermediate", "Which city is the legislative capital of Sri Lanka?",
  ["Sri Jayewardenepura Kotte", "Colombo", "Kandy", "Galle"], "*",
  "Capitals of neighbouring countries",
  "Sri Lanka has two capitals: Sri Jayewardenepura Kotte (legislative capital, seat of Parliament) and Colombo "
  "(commercial capital). Kotte's name means 'Resplendent City of Growing Victory'.",
  ["Legislative capital: Sri Jayewardenepura Kotte", "Commercial capital: Colombo"],
  [fact("Sri Lanka: Colombo (commercial capital); Sri Jayewardenepura Kotte (legislative capital)",
        U["cia_srilanka"])])

G(T, CC, "Intermediate", "What is the currency of the Maldives?",
  ["Rufiyaa", "Rupee", "Ngultrum", "Dinar"], "*",
  "Currencies of neighbouring countries",
  "The Maldives uses the rufiyaa (MVR); its capital is Male. Nepal, Pakistan and Sri Lanka use rupees, and Bhutan "
  "uses the ngultrum.",
  ["Maldives: rufiyaa, capital Male"],
  [fact("Maldives currency: rufiyaa (MVR)", U["cia_maldives"])])

G(T, NP, "Intermediate",
  "Keibul Lamjao, described as the only floating national park in the world, is located in which state?",
  ["Manipur", "Mizoram", "Assam", "Tripura"], "*",
  "Keibul Lamjao National Park",
  "Keibul Lamjao lies on Loktak Lake in Manipur and is made of floating mats of vegetation called phumdis. It is the "
  "only natural home of the sangai (brow-antlered deer), Manipur's state animal.",
  ["Keibul Lamjao: Loktak Lake, Manipur", "Home of the sangai deer"],
  [fact("Keibul Lamjao on Loktak Lake, Manipur: sangai deer habitat on floating phumdis", U["keibul"])])

G(T, NP, "Intermediate", "Jim Corbett National Park was originally established in 1936 under which name?",
  ["Hailey National Park", "Ramganga National Park", "Victoria National Park", "Dudhwa National Park"], "*",
  "Jim Corbett National Park",
  "Corbett was established in 1936 as Hailey National Park, after Sir Malcolm Hailey, Governor of the United "
  "Provinces; it was the first national park of mainland Asia. It was briefly called Ramganga National Park "
  "(1954-55) and was renamed after Jim Corbett in 1956.",
  ["1936: Hailey National Park", "1954-55: Ramganga NP", "1956: Corbett NP"],
  [fact("Originally established as Hailey National Park in 1936; Ramganga NP 1954-55; renamed after Jim Corbett "
        "in 1956", U["corbett"])],
  why="Ramganga was a later, short-lived name, not the original one.")

G(T, NP, "Intermediate", "In which year was the Sundarbans National Park (India) inscribed as a UNESCO World Heritage "
  "Site?",
  ["1985", "1987", "1993", "2002"], "B",
  "UNESCO natural sites in India",
  "Sundarbans National Park in West Bengal, the world's largest mangrove delta and a tiger habitat, was inscribed in "
  "1987. Kaziranga, Manas and Keoladeo were inscribed earlier, in 1985.",
  ["Sundarbans: inscribed 1987", "Kaziranga, Manas, Keoladeo: 1985"],
  [fact("Sundarbans National Park inscribed 1987 under criteria (ix) and (x)", U["sundarbans"])])

G(T, NP, "Intermediate", "The Hirakud Dam, near Sambalpur in Odisha, is built on which river?",
  ["Mahanadi", "Godavari", "Brahmani", "Subarnarekha"], "*",
  "Dams of India",
  "Hirakud Dam is on the Mahanadi about 15 km from Sambalpur, Odisha. It is often described as one of the longest "
  "earthen dams in the world, and its reservoir is among the largest artificial lakes in Asia.",
  ["Hirakud: Mahanadi river, Odisha"],
  [fact("Hirakud Dam on the Mahanadi near Sambalpur", U["hirakud"])])

G(T, NP, "Intermediate", "What is the name of the reservoir formed by the Bhakra Dam on the Sutlej?",
  ["Gobind Sagar", "Rana Pratap Sagar", "Govind Ballabh Pant Sagar", "Nizam Sagar"], "*",
  "Dams of India",
  "Bhakra Dam is a 225.55 m concrete gravity dam across the Sutlej in Bilaspur district, Himachal Pradesh. Its "
  "reservoir is Gobind Sagar. The Bhakra Beas Management Board (BBMB) operates it.",
  ["Bhakra: Sutlej, Himachal Pradesh", "Reservoir: Gobind Sagar"],
  [fact("Bhakra Dam on Sutlej, Bilaspur HP; reservoir Gobind Sagar; BBMB", U["bhakra"])],
  why="Rana Pratap Sagar is on the Chambal; Govind Ballabh Pant Sagar (Rihand) is in Uttar Pradesh.")

G(T, SF, "Intermediate", "Goa became which state of the Indian Union on 30 May 1987?",
  ["22nd", "24th", "25th", "26th"], "C",
  "Statehood of Goa",
  "Goa, administered as a Union Territory (with Daman and Diu) after its liberation in 1961, became the 25th state "
  "on 30 May 1987, celebrated as Goa Statehood Day.",
  ["Goa: 25th state, 30 May 1987"],
  [fact("Goa became the 25th State of the Indian Union on 30 May 1987", U["goa"])])

G(T, SF, "Intermediate", "On which date was Nagaland inaugurated as a state?",
  ["1 November 1956", "1 December 1963", "21 January 1972", "20 February 1987"], "B",
  "Statehood of Nagaland",
  "Nagaland was formally inaugurated as the 16th state of India on 1 December 1963 under the State of Nagaland Act, "
  "1962. The Hornbill Festival begins on Statehood Day, 1 December.",
  ["Nagaland: 16th state, 1 December 1963"],
  [fact("Nagaland inaugurated 1 December 1963 as the 16th state of India", U["nagaland"])],
  why="21 January 1972: Manipur, Meghalaya and Tripura; 20 February 1987: Arunachal Pradesh and Mizoram.")

G(T, CC, "Advanced",
  "Consider the following statements about South Africa:\n"
  "1. Pretoria is its administrative capital.\n"
  "2. Cape Town is its judicial capital.\n"
  "3. Bloemfontein is its judicial capital.\n"
  "Which of the statements given above is/are correct?",
  S123, "C",
  "Countries with more than one capital",
  "South Africa has three capitals: Pretoria (administrative), Cape Town (legislative) and Bloemfontein "
  "(judicial). Its currency is the rand.",
  ["1: correct", "2: wrong (Cape Town is legislative)", "3: correct", "So 1 and 3 only"],
  [fact("South Africa: Pretoria administrative, Cape Town legislative, Bloemfontein judicial", U["cia_sa"])])

G(T, NP, "Advanced",
  "The power from the Sardar Sarovar Project on the Narmada is shared among states under the Narmada tribunal "
  "award. Which state gets the largest share?",
  ["Madhya Pradesh", "Gujarat", "Maharashtra", "Rajasthan"], "*",
  "Sardar Sarovar Project",
  "Sardar Sarovar Dam at Kevadia (Narmada district, Gujarat) is an inter-state project of Madhya Pradesh, "
  "Maharashtra, Gujarat and Rajasthan. Its 1,450 MW of power is shared 57% to Madhya Pradesh, 27% to Maharashtra "
  "and 16% to Gujarat; Rajasthan gets water but no power. The Statue of Unity stands near the dam.",
  ["Power share: MP 57%, Maharashtra 27%, Gujarat 16%", "So Madhya Pradesh"],
  [fact("SSP at Kevadia; interstate project of MP, Maharashtra, Gujarat, Rajasthan; power 57% MP, 27% Maharashtra, "
        "16% Gujarat", U["ssp"])],
  why="Gujarat hosts the dam and gets most of the water, but the smallest power share.")

G(T, NP, "Advanced",
  "Consider the following statements about Jim Corbett National Park:\n"
  "1. It was renamed after Jim Corbett in 1956.\n"
  "2. Project Tiger was launched at Corbett on 1 April 1973.\n"
  "Which of the statements given above is/are correct?",
  ["Only 1", "Only 2", "Both 1 and 2", "Neither 1 nor 2"], "C",
  "Corbett and Project Tiger",
  "The park was renamed in honour of Jim Corbett in 1956, after his death. Project Tiger was launched at the "
  "Corbett Tiger Reserve on 1 April 1973 (the Dhikala Forest Rest House was the venue), starting with nine tiger "
  "reserves.",
  ["1: correct", "2: correct", "So both"],
  [fact("Renamed in honour of Jim Corbett in 1956; launch site of Project Tiger on 1 April 1973", U["corbett"])])

G(T, NP, "Advanced",
  "Consider the following statements:\n"
  "1. Kaziranga National Park was inscribed as a World Heritage Site in 1985.\n"
  "2. Keoladeo National Park was the only wintering ground in India of the Siberian crane.\n"
  "3. Keoladeo National Park is located in Gujarat.\n"
  "Which of the statements given above is/are correct?",
  ["1 only", "1 and 3 only", "2 and 3 only", "1 and 2 only"], "D",
  "UNESCO natural sites in India",
  "Kaziranga (Assam) and Keoladeo were both inscribed in 1985. Keoladeo National Park is at Bharatpur in "
  "Rajasthan, not Gujarat; it was the only wintering ground in India of the rare Siberian crane and is also a "
  "Ramsar wetland.",
  ["1: correct", "2: correct", "3: wrong (Bharatpur, Rajasthan)", "So 1 and 2 only"],
  [fact("Kaziranga National Park inscribed 1985", U["kaziranga"]),
   fact("Keoladeo National Park, Bharatpur: only wintering ground in India of the Siberian crane", U["keoladeo"]),
   fact("Keoladeo National Park inscribed 1985", U["whc_india"])])

G(T, SF, "Advanced",
  "Consider the following statements about the reorganisation of Jammu and Kashmir:\n"
  "1. The Union Territories of Jammu and Kashmir and Ladakh came into existence on 31 October 2019.\n"
  "2. The Union Territory of Ladakh has a legislature.\n"
  "3. The Union Territory of Jammu and Kashmir has a legislature.\n"
  "Which of the statements given above is/are correct?",
  S123, "C",
  "J&K Reorganisation Act, 2019",
  "Under the Jammu and Kashmir Reorganisation Act, 2019, the state was split into the UT of Jammu and Kashmir (with "
  "a legislature) and the UT of Ladakh (without a legislature), with effect from 31 October 2019, the birth "
  "anniversary of Sardar Patel.",
  ["1: correct", "2: wrong (Ladakh has no legislature)", "3: correct", "So 1 and 3 only"],
  [fact("UT of J&K with legislature and UT of Ladakh without legislature, in force from 31 October 2019", U["jk"])])

G(T, SF, "Advanced",
  "Consider the following statements:\n"
  "1. Gujarat and Maharashtra were formed on 1 May 1960 by dividing the former Bombay State.\n"
  "2. Sikkim became a state of India on 16 May 1975.\n"
  "Which of the statements given above is/are correct?",
  ["Only 1", "Only 2", "Neither 1 nor 2", "Both 1 and 2"], "D",
  "Formation of states",
  "On 1 May 1960 the bilingual Bombay State was divided into Gujarat and Maharashtra, and both observe 1 May as "
  "their Foundation Day. Sikkim became a state on 16 May 1975 (Constitution 36th Amendment); 2025 marked 50 years of "
  "its statehood.",
  ["1: correct", "2: correct", "So both"],
  [fact("Gujarat carved out of the former Bombay State on 1 May 1960", U["gujarat"]),
   fact("Sikkim Statehood Day 16 May (1975)", U["sikkim"])])

G(T, NP, "Advanced",
  "Consider the following statements about the Tehri Dam:\n"
  "1. It is a 260.5 m high earth and rockfill dam.\n"
  "2. It is owned and operated by NHPC Limited.\n"
  "Which of the statements given above is/are correct?",
  ["Only 1", "Only 2", "Both 1 and 2", "Neither 1 nor 2"], "A",
  "Tehri Hydro Power Complex",
  "Tehri is a 260.5 m earth and rockfill dam with a 1,000 MW underground power house. It is owned and operated by "
  "THDC India Ltd, not NHPC. The Tehri complex also includes a 1,000 MW pumped storage plant.",
  ["1: correct", "2: wrong (THDC India Ltd)", "So only 1"],
  [fact("Tehri HPP: 260.5 m earth and rockfill dam; THDC India Ltd", U["tehri"])])


# ====================================================================== build
def place_answers(items):
    """Keep fixed keys; move the correct option of flexible items so overall keys are balanced."""
    counts = Counter(it["answer"] for it in items if it["answer"] != "*")
    turn = 0
    for it in items:
        if it["answer"] != "*":
            continue
        low = min(counts.get(k, 0) for k in LETTERS)
        candidates = [k for k in LETTERS if counts.get(k, 0) == low]
        key = candidates[turn % len(candidates)]
        turn += 1
        idx = LETTERS.index(key)
        opts = it["options"]
        opts[0], opts[idx] = opts[idx], opts[0]
        it["answer"] = key
        counts[key] += 1
    return counts


def build(items):
    plan = json.loads((ROOT / "batches" / "plans" / "BATCH_001_plan.json").read_text(encoding="utf-8"))
    ga = next(s for s in plan["subjects"] if s["subject"] == GA)
    first = int(ga["question_ids"][0].rsplit("_", 1)[1])
    counts = place_answers(items)
    out = []
    for n, it in enumerate(items):
        ans = it["answer"]
        opts = it["options"]
        q = {
            "question_id": f"BANK_GA_{first + n:06d}",
            "exam_mappings": default_mappings(GA, it["difficulty"]),
            "subject": GA, "topic": it["topic"], "subtopic": it["subtopic"], "difficulty": it["difficulty"],
            "question_type": "MCQ", "language": "en",
            "question_text": it["text"],
            "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(opts)],
            "correct_answer": ans,
            "solution": {"concept": it["concept"], "explanation": it["explanation"], "steps": it["steps"],
                         "shortcut": it["shortcut"], "why_others_wrong": it["why"],
                         "final_answer": f"Option {ans}: {opts[LETTERS.index(ans)]}"},
            "suggested_time_seconds": SECONDS[it["difficulty"]],
        }
        if it["current"]:
            q["current_affairs"] = it["current"]
        q["source"] = {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                       "original_exam_year": None, "license_note": None}
        # pib.gov.in answered 403 to every fetch, so facts resting only on PIB pages were confirmed via search results
        pib_only = all("pib.gov.in" in f["source_url"] for f in it["facts"])
        q["verification"] = {"answer_verified": True, "solution_verified": True,
                             "review_status": "Pending Human Review",
                             "verified_by": ["ai:author-solve",
                                             "web:search-confirmed" if pib_only else "web:fact-check"],
                             "verified_at": TODAY,
                             "fact_checks": it["facts"]}
        out.append(q)

    # quota check against the plan before writing
    have = Counter((q["topic"], q["difficulty"]) for q in out)
    for t in ga["topics"]:
        for d, k in t["quota"].items():
            assert have[(t["topic"], d)] == k, (t["topic"], d, have[(t["topic"], d)], k)
            assert all(q["subtopic"] in t["subtopics"] for q in out if q["topic"] == t["topic"])
    assert len(out) == ga["total"] == 150
    assert out[-1]["question_id"] == ga["question_ids"][1]
    return out, counts


questions, keys = build(QUESTIONS)
batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_001",
    "created_at": TODAY,
    "notes": "BATCH_001 General Awareness part: 150 original questions on the static GA topics (Government Schemes, "
             "Important Days, National and International Organizations, Important Reports and Indexes, Government "
             "Policies, Static Awareness). No current-affairs topics. Every question has web fact checks dated "
             "2026-11-05; facts that can change carry current_affairs review dates. Pending human review.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_001_GA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(keys.items()))})")
