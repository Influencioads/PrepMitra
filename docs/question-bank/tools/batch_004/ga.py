"""Writes batches/parts/BATCH_004_GA.json: the 150 General Awareness questions of BATCH_004.

Current-affairs topics (National and International Current Affairs, Appointments, Awards, Sports, Summits, Economic
Affairs, Business) test events dated between 2025-11-01 and 2026-11-04; event dates come from the sources and every
such question carries current_affairs {event_date, review_by 2027-05-05}. Other time-sensitive facts (themes of days,
index ranks, books, schemes announced in the window, policy changes) carry current_affairs too.

Every question has fact_checks. Each URL is marked OPENED (fetched and read on 2026-11-05, giving "web:fact-check")
or SEARCH (confirmed only from search-result text on 2026-11-05, giving "web:search-confirmed"). Sites that refused a
fetch (HTTP 403/429 or timeouts, e.g. pulitzer.org, thebookerprizes.com, fiercepharma.com, business-standard.com,
dailymaverick.co.za, regjeringen.no) were not worked around; other pages that stated the fact were opened instead, or
the fact rests on search results.

All earlier GA stems (BATCH_000 sample, BATCH_001_GA, BATCH_002_GA, BATCH_003_GA) were read first; no fact or event
tested there is tested again here.

Statement questions have their key fixed by the statements (computed from truth values); other questions are written
with the correct option first and answer "*", and are then placed so that keys are balanced A to D.

    python tools/batch_004/ga.py
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
CA_FROM, CA_TO = "2025-11-01", "2026-11-04"
LETTERS = "ABCD"
GA = "General Awareness and Current Affairs"
BATCH = "BATCH_004"
SECONDS = {"Basic": 15, "Intermediate": 25, "Advanced": 45}
CA_TOPICS = {"National Current Affairs", "International Current Affairs", "Important Appointments",
             "Awards and Honours", "Sports", "Summits and Conferences", "Economic Affairs",
             "Business and Corporate News"}

S12 = ["Only 1", "Only 2", "Both 1 and 2", "Neither 1 nor 2"]
S123 = ["1 and 2 only", "2 and 3 only", "1 and 3 only", "1, 2 and 3"]
KEY12 = {(True, False): "A", (False, True): "B", (True, True): "C", (False, False): "D"}
KEY123 = {(True, True, False): "A", (False, True, True): "B", (True, False, True): "C", (True, True, True): "D"}

QUESTIONS = []
OPENED, SEARCH = "opened", "search"


def ca(event_date):
    return {"event_date": event_date, "review_by": REVIEW_BY}


def stmt(about, statements, truth):
    """Build a statement question; the key is computed from the truth values, so it cannot drift."""
    lines = [f"Consider the following statements about {about}:"]
    lines += [f"{i + 1}. {s}" for i, s in enumerate(statements)]
    lines.append("Which of the statements given above is/are correct?")
    if len(statements) == 2:
        return "\n".join(lines), list(S12), KEY12[tuple(truth)]
    assert len(statements) == 3 and tuple(truth) in KEY123, (about, truth)
    return "\n".join(lines), list(S123), KEY123[tuple(truth)]


def G(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, facts,
      why=None, shortcut=None, current=None):
    assert len(options) == 4 and len(set(options)) == 4, text
    assert answer == "*" or answer in LETTERS, answer
    assert facts and why, text
    if topic in CA_TOPICS:
        assert current and CA_FROM <= current["event_date"] <= CA_TO, (text, current)
    if current:
        assert CA_FROM <= current["event_date"] <= CA_TO or topic not in CA_TOPICS, (text, current)
    QUESTIONS.append(dict(topic=topic, subtopic=subtopic, difficulty=difficulty, text=text, options=list(options),
                          answer=answer, concept=concept, explanation=explanation, steps=steps, facts=facts,
                          why=why, shortcut=shortcut, current=current))


def GS(topic, subtopic, difficulty, about, statements, truth, concept, explanation, facts, why, current=None,
       shortcut=None):
    text, options, key = stmt(about, statements, truth)
    steps = [f"{i + 1}: {'correct' if t else 'incorrect'}" for i, t in enumerate(truth)]
    steps.append("So " + options[LETTERS.index(key)])
    G(topic, subtopic, difficulty, text, options, key, concept, explanation, steps, facts, why=why,
      shortcut=shortcut, current=current)


# ====================================================================== sources
# key: (url, how it was checked on 2026-11-05)
U = {
    # ---------------- National
    "manipur_print": ("https://theprint.in/politics/presidents-rule-revoked-in-manipur-after-a-year-new-cm-to-be-sworn-"
                      "in-today/2845550", OPENED),
    "manipur_air": ("https://www.newsonair.gov.in/presidents-rule-revoked-in-manipur", SEARCH),
    "ifr_org": ("https://organiser.org/2026/02/19/340824/bharat/ifr-2026-indigenous-naval-prowess-echoes-the-resolve-"
                "for-secure-maritime-corridors-shared-spirit-for-ocean-diplomacy/", OPENED),
    "ifr_air": ("https://www.newsonair.gov.in/president-droupadi-murmu-to-witness-international-fleet-review-2026-in-"
                "visakhapatnam", OPENED),
    "arid_print": ("https://theprint.in/defence/india-commissions-its-third-nuclear-powered-ballistic-missile-"
                   "submarine-ins-aridhaman/2895692/", OPENED),
    "arid_tv": ("https://www.indiatvnews.com/news/india/ins-aridaman-india-s-third-nuclear-powered-submarine-"
                "commissioned-into-indian-navy-2026-04-03-1036196", OPENED),
    "malabar_baird": ("https://www.bairdmaritime.com/security/naval/guam-hosts-joint-maritime-exercise-malabar-2025",
                      OPENED),
    "malabar_ians": ("https://ianslive.in/ins-sahyadri-docks-at-guam-for-malabar-2025-showcasing-indias-naval-"
                     "strength-amid-strained-indo-us-ties--20251109175902", SEARCH),
    "nomadic_air": ("https://newsonair.gov.in/18th-india-mongolia-joint-military-exercise-nomadic-elephant-begins-in-"
                    "pithoragarh/", OPENED),
    "tripura_itne": ("https://www.indiatodayne.in/tripura/story/tripura-becomes-first-state-to-complete-all-"
                     "deregulation-priority-areas-under-phase-i-and-ii-1392082-2026-05-15", OPENED),
    "dharma_drishti": ("https://www.drishtiias.com/state-pcs-current-affairs/dharma-guardian-2026-begins-in-"
                       "uttarakhand/print_manually", OPENED),
    "austrahind_air": ("https://newsonair.gov.in/joint-military-exercise-austrahind-2026-between-india-and-australia-"
                       "commences-in-thiruvananthapuram/", OPENED),
    "yudh_gk": ("https://www.gktoday.in/india-us-yudh-abhyas-2026-begins-at-auli-and-mahajan/", OPENED),
    "defsec_nk": ("https://www.newkerala.com/news/a/defence-secretary-rajesh-kumar-singh-gets-one-year-extension-"
                  "179.htm", OPENED),
    "sikkim_na": ("https://newsarenaindia.com/states/sikkim-becomes-india-s-fifth-fully-literate-state/78490", OPENED),
    "sikkim_gk": ("https://gknow.in/sikkim-declared-fully-literate-state-under-ullas-programme/", SEARCH),
    "jk_tnpsc": ("https://www.tnpscthervupettagam.com/currentaffairs-detail/statehood-resolution-jammu-and-kashmir",
                 OPENED),
    "pragati_dd": ("https://www.devdiscourse.com/article/law-order/3915294-exercise-pragati-2026-begins-in-meghalaya-"
                   "with-participation-from-12-friendly-nations", OPENED),
    # ---------------- International
    "babis_star": ("https://www.thestar.com.my/news/world/2025/12/09/czech-president-appoints-andrej-babis-as-new-"
                   "prime-minister", OPENED),
    "jetten_eu": ("https://euronews.com/2026/02/23/new-dutch-minority-government-sworn-in-under-the-nations-youngest-"
                  "prime-minister-rob-jette", OPENED),
    "scot_wiki": ("https://en.wikipedia.org/wiki/2026_Scottish_Parliament_election", OPENED),
    "scot_ms": ("https://morningstaronline.co.uk/article/swinney-re-elected-first-minister", SEARCH),
    "tolam_vns": ("https://vietnamnews.vn/politics-laws/1764380/to-lam-re-elected-general-secretary-of-the-14th-"
                  "party-central-committee.html", OPENED),
    "swe_aj": ("https://www.aljazeera.com/news/2026/9/17/sweden-prime-minister-to-resign-as-left-wing-bloc-seals-"
               "narrow-election-win", OPENED),
    "iraq_aj": ("https://www.aljazeera.com/news/2026/5/14/iraqs-parliament-approves-new-ali-al-zaidi-government",
                OPENED),
    "bhutan_ob": ("https://www.outlookbusiness.com/industry/modi-bhutan-visit-punatsangchhu-hydropower-project",
                  OPENED),
    "merz_ians": ("https://ianslive.in/german-chancellor-friedrich-merz-departs-after-concluding-india-visit--"
                  "20260113143848", OPENED),
    "carney_air": ("https://www.newsonair.gov.in/pm-modi-and-his-canadian-counterpart-mark-carney-hold-bilateral-talks-"
                   "in-new-delhi-decide-to-expedite-comprehensive-economic-partnership-agreement/", OPENED),
    "carney_sm": ("https://www.thestatesman.com/india/canadian-pm-mark-carney-arrives-in-mumbai-on-four-day-official-"
                  "visit-to-india-1503563961.html", SEARCH),
    "nz_star": ("https://www.thestar.com.my/news/world/2026/07/03/indian-pm-modi-to-make-first-official-visit-to-new-"
                "zealand-next-week", OPENED),
    "nz_swarajya": ("https://swarajyamag.com/world/pm-modi-arrives-in-auckland-for-first-visit-by-an-indian-prime-"
                    "minister-to-new-zealand-in-four-decades", SEARCH),
    "norway_sm": ("https://www.thestatesman.com/india/pm-modi-norwegian-pm-store-hold-delegation-level-talks-elevate-"
                  "india-norway-ties-to-green-strategic-partnership-1503595270.html", SEARCH),
    "norway_org": ("https://organiser.org/2026/05/19/354084/world/five-nation-visit-pm-modi-becomes-first-indian-pm-in-"
                   "40-years-to-visit-norway-seals-green-strategic-partnership/", SEARCH),
    "uae_gt": ("https://www.gulf-times.com/article/725514/international/india/india-deepens-defence-energy-ties-with-"
               "uae-during-pm-modi-visit/amp", OPENED),
    "nl_print": ("https://theprint.in/diplomacy/modi-hails-17-new-agreements-says-india-netherlands-ties-will-gain-"
                 "unparalleled-momentum/2933539/", OPENED),
    "nordic_air": ("https://www.newsonair.gov.in/pm-modi-to-attend-3rd-india-nordic-summit-in-oslo-norway-today/",
                   OPENED),
    "nordic_vision": ("https://dce.visionias.in/news-today/2026-05-20/international-relations/3rd-india-nordic-summit-"
                      "2026-held-in-oslo-norway", SEARCH),
    "eth_dawan": ("https://www.dawan.africa/news/prosperity-party-wins-438-seats-in-ethiopias-parliament", OPENED),
    "eth_ena": ("https://www.ena.et/web/eng/w/eng_9074409", OPENED),
    "uganda_cit": ("https://www.thecitizen.co.tz/tanzania/news/east-africa-news/museveni-declared-winner-of-uganda-"
                   "election-extending-rule-beyond-40-years-5329704", OPENED),
    "uganda_all": ("https://allafrica.com/stories/202601180053.html", SEARCH),
    "iran_bt": ("https://www.businesstoday.in/world/story/agreed-to-open-strait-of-hormuz-trump-announces-two-week-"
                "ceasefire-with-iran-drops-threat-to-end-a-whole-civilisation-524538-2026-04-08", OPENED),
    "iran_nat": ("https://www.thenationalnews.com/news/mena/2026/06/15/us-and-iran-agree-peace-framework-and-set-plan-"
                 "to-reopen-strait-of-hormuz/", SEARCH),
    "indo_antara": ("https://en.antaranews.com/news/421737/prabowo-hosts-modi-for-talks-on-strategic-cooperation",
                    OPENED),
    "indo_ap": ("https://www.ottumwacourier.com/news/national_news/modi-and-prabowo-seal-a-deal-for-indonesia-to-"
                "acquire-indias-brahmos-missiles/article_a0e14a6c-8b91-581e-8b7a-a808ce0c46dd.html", SEARCH),
    "indo_ians": ("https://ianslive.in/pm-modi-highlights-strong-and-vibrant-india-indonesia-ties-as-landmark-"
                  "agreements-deepen-partnership--20260708094232", SEARCH),
    # ---------------- Schemes
    "bbbp_wiki": ("https://en.wikipedia.org/wiki/Beti_Bachao_Beti_Padhao", OPENED),
    "sbm_wiki": ("https://en.wikipedia.org/wiki/Swachh_Bharat_Mission", OPENED),
    "pmgsy_wiki": ("https://en.wikipedia.org/wiki/Pradhan_Mantri_Gram_Sadak_Yojana", OPENED),
    "startup_wiki": ("https://en.wikipedia.org/wiki/Startup_India", OPENED),
    "digital_wiki": ("https://en.wikipedia.org/wiki/Digital_India", OPENED),
    "mi_wiki": ("https://en.wikipedia.org/wiki/Mission_Indradhanush", OPENED),
    "atal_wiki": ("https://en.wikipedia.org/wiki/Atal_Bhujal_Yojana", OPENED),
    "kisan_angel": ("https://www.angelone.in/news/government-schemes/pm-kisan-scheme-22nd-instalment-around-9-32-crore-"
                    "farmers-receive-2-000", OPENED),
    "kisan_tv": ("https://www.indiatvnews.com/business/personal-finance/pm-kisan-22nd-instalment-date-2026-update-pm-"
                 "modi-to-release-rs-2000-on-farmers-account-from-guwahti-2026-03-11-1033414", SEARCH),
    "khelo_air": ("https://newsonair.gov.in/cabinet-approves-expanded-khelo-india-scheme-with-%E2%82%B936441-crore-"
                  "outlay/", OPENED),
    "udan_ii": ("https://indianinfrastructure.com/2026/03/26/union-cabinet-approves-modified-udan-scheme-with-rs-288-40-"
                "billion-outlay/", OPENED),
    "shp_psu": ("https://psuwatch.com/amp/story/newsupdates/cabinet-approves-small-hydro-power-shp-development-scheme-"
                "with-outlay-of-rs-2584-cr", OPENED),
    "mpms_fpj": ("https://www.freepressjournal.in/business/cabinet-approves-219-lakh-crore-projects-including-semicon-"
                 "20-and-mobile-scheme", OPENED),
    "mpms_nm": ("https://www.narendramodi.in/amp/category/news/mpms", SEARCH),
    "sarthak_tv": ("https://www.indiatvnews.com/business/markets/cabinet-clears-rs-25530-crore-for-extension-of-"
                   "sarthak-pds-scheme-for-5-years-check-details-2026-05-27-1042675", OPENED),
    "eclgs_myind": ("https://myind.net/Home/viewArticle/cabinet-approves-152-lakh-crore-mega-push-for-agriculture-"
                    "infrastructure-manufacturing", OPENED),
    # ---------------- Appointments
    "donohoe_rte": ("https://www.rte.ie/news/politics/2025/1118/1544567-paschal-donohoe-politics", OPENED),
    "pierr_ief": ("https://www.iefimerida.gr/english/greece-pierrakakis-elected-eurogroup-president", OPENED),
    "pierr_n4j": ("https://www.news4jax.com/business/2025/12/11/in-stunning-reversal-for-europe-greek-finance-minister-"
                  "elected-as-eurogroup-president/", SEARCH),
    "kremer_star": ("https://www.thestar.com.my/news/world/2026/09/16/world-bank-names-nobel-laureate-michael-kremer-"
                    "as-next-chief-economist", OPENED),
    "tenreyro_fpj": ("https://www.freepressjournal.in/business/imf-appoints-silvana-tenreyro-as-chief-economist-former-"
                     "bank-of-england-policymaker-to-take-charge-from-august-10", OPENED),
    # ---------------- Awards
    "nfa_ol": ("https://outlookindia.com/art-entertainment/72nd-national-film-awards-winners-full-list", OPENED),
    "venice_eu": ("https://www.euronews.com/culture/2026/09/12/venice-film-festival-2026-woman-unknown-of-may-el-"
                  "toukhy-wins-the-golden-lion", OPENED),
    "cannes_eu": ("https://www.euronews.com/2026/05/23/cannes-2026-cristian-mungius-political-drama-fjord-wins-the-palme-"
                  "dor", OPENED),
    "cannes_ol": ("https://www.outlookindia.com/art-entertainment/cannes-2026-romanian-director-cristian-mungiu-wins-his-"
                  "second-palme-dor-for-fjord", SEARCH),
    "berlin_eu": ("https://www.euronews.com/2026/02/21/berlin-film-festival-yellow-letters-wins-the-golden-bear-award-"
                  "2026", OPENED),
    "phalke_air": ("https://newsonair.gov.in/veteran-kannada-actor-anant-nag-to-be-conferred-with-dadasaheb-phalke-"
                   "award-for-2024/", OPENED),
    "turing_eur": ("https://www.eurekalert.org/news-releases/1120415", OPENED),
    "laureus_ol": ("https://outlookindia.com/sports/others/laureus-world-awards-2026-full-winners-list-carlos-alcaraz-"
                   "aryna-sabalenka", OPENED),
    "laureus_dt": ("https://www.dhakatribune.com/sport/408296/alcaraz-sabalenka-headline-star-studded-laureus", SEARCH),
    "templeton_trt": ("https://templetonreligiontrust.org/explore/professor-simon-conway-morris-receives-2026-templeton-"
                      "prize/", OPENED),
    "templeton_var": ("https://www.varsity.co.uk/news/31588", SEARCH),
    "saraswati_air": ("https://newsonair.gov.in/bengali-novel-hara-parbati-katha-by-author-ramkumar-mukhopadhyay-"
                      "selected-for-saraswati-samman/", OPENED),
    "kyoto_kp": ("https://www.kyotoprize.org/en/260619", OPENED),
    "ballon_bein": ("https://www.beinsports.com/en-us/soccer/articles/live-ballon-d-or-2026-winners-and-all-awards-"
                    "2026-10-26?Vz=Qx", OPENED),
    "rla_bol": ("https://bolnews.com/pakistan/pakistani-human-rights-lawyer-wins-alternative-nobel-award", OPENED),
    "rla_cd": ("https://www.commondreams.org/news/right-livelihood", SEARCH),
    # ---------------- Sports
    "wt20_ol": ("https://www.outlookindia.com/sports/cricket/england-vs-australia-icc-womens-t20-world-cup-2026-final-"
                "toss-match-report-eng-w-v-aus-w-playing-xis-lords", OPENED),
    "f1_f1": ("https://www.formula1.com/en/latest/article/norris-secures-maiden-f1-title-in-abu-dhabi-with-podium-"
              "finish-behind.EMJtmvRA0uzmzUC4MZgmw", OPENED),
    "ranji_ol": ("https://www.outlookindia.com/sports/cricket/karnataka-vs-jammu-and-kashmir-ranji-trophy-2025-26-"
                 "final-match-report-hubballi", OPENED),
    "ranji_wiki": ("https://en.wikipedia.org/wiki/2025%E2%80%9326_Ranji_Trophy", OPENED),
    "wpl_wiki": ("https://en.wikipedia.org/wiki/2026_Women%27s_Premier_League_(cricket)_final", OPENED),
    "thomas_cgtn": ("https://news.cgtn.com/news/2026-05-04/China-retains-Thomas-Cup-ROK-hoists-Uber-Cup-in-Denmark-"
                    "1MRJXGzuLu0/p.html", OPENED),
    "davis_star": ("https://www.thestar.com.my/sport/tennis/2025/11/24/tennis-berrettini-cobolli-lead-italy-past-spain-"
                   "for-third-straight-davis-cup-title", OPENED),
    "bwf_wiki": ("https://en.wikipedia.org/wiki/2026_BWF_World_Championships", OPENED),
    "fo_cgtn": ("https://news.cgtn.com/news/2026-06-08/Zverev-captures-first-Grand-Slam-title-with-French-Open-triumph-"
                "1NNMWwOLOW4/p.html", OPENED),
    "uso_katv": ("https://katv.com/news/nation-world/rybakina-tops-sabalenka-to-win-us-open-claim-no-1-ranking", OPENED),
    "hwc_air": ("https://newsonair.gov.in/germany-retain-fih-mens-hockey-world-cup-title-with-1-0-win-over-spain/",
                OPENED),
    "hwc_ol": ("https://www.outlookindia.com/sports/hockey/germany-vs-spain-fih-mens-world-cup-2026-match-report-wavre",
               SEARCH),
    "hwcw_wiki": ("https://en.wikipedia.org/wiki/2026_Women%27s_FIH_Hockey_World_Cup", OPENED),
    "hwcw_nk": ("https://www.newkerala.com/news/a/argentina-beat-netherlands-shootout-clinch-womens-hockey-world-432.htm",
                SEARCH),
    "ucl_fs": ("https://www.flashscore.com.au/news/soccer-champions-league-imperious-psg-come-from-behind-again-to-"
               "clinch-2025-26-champions-league-crown/63fLM8qf/", OPENED),
    "ucl_fandom": ("https://football.fandom.com/wiki/2026_UEFA_Champions_League_Final", SEARCH),
    "jhwc_trib": ("https://www.tribuneindia.com/news/sports/germany-win-record-extending-8th-hockey-junior-world-cup",
                  OPENED),
    "chess_fide": ("https://www.fide.com/uzbekistans-dream-finish-olympiad-gold-in-samarkand/", OPENED),
    "durand_ae": ("https://theawayend.co/2026/08/23/135th-durand-cup-2026-final-east-bengal-fc-defeat-mohun-bagan-4-1/",
                  OPENED),
    # ---------------- Summit
    "apec_ptv": ("https://ptvnews.ph/pbbm-apec-leaders-adopt-gyeongju-declaration-on-ai-growth/", OPENED),
    # ---------------- Days
    "iwd_rep": ("https://www.republicworld.com/lifestyle/international-womens-day-2026-theme-rights-justice-action-give-"
                "to-gain-significance", OPENED),
    "wwd_gen": ("https://www.genevaenvironmentnetwork.org/resources/updates/celebrating-world-wildlife-day/", OPENED),
    "tb_who": ("https://www.who.int/news-room/speeches/item/who-director-general-s-remarks-at-the-world-tb-day-talk-"
               "show---18-march-2026", OPENED),
    "idb_cbd": ("https://www.cbd.int/biodiversity-day/2026/theme", OPENED),
    "wfd_fao": ("https://www.fao.org/world-food-day/events/detail/3/en", OPENED),
    # ---------------- Books
    "naravane_rupa": ("https://rupapublications.co.in/book/the-curious-and-the-classified-unearthing-military-myths-and-"
                      "mysteries", OPENED),
    "naravane_trib": ("https://www.tribuneindia.com/news/india/in-news-over-his-unpublished-controversial-memoir-gen-"
                      "naravane-pens-new-book/", SEARCH),
    "ghosh_fpj": ("https://www.freepressjournal.in/lifestyle/award-winning-author-amitav-ghoshs-new-novel-ghost-eye-"
                  "brings-together-food-myth-memory", OPENED),
    "rushdie_peng": ("https://www.penguin.co.uk/books/475244/the-eleventh-hour-by-rushdie-salman/9781529968842", OPENED),
    "rushdie_br": ("https://www.bookreporter.com/reviews/the-eleventh-hour-a-quintet-of-stories", SEARCH),
    "pulitzer_lit": ("https://lithub.com/here-are-the-2026-pulitzer-prize-winners/", OPENED),
    "nba_kunc": ("https://www.kunc.org/2025-11-20/here-are-the-winners-of-the-2025-national-book-awards", OPENED),
    "nif_site": ("https://www.newindiafoundation.org/winner-nif-book-prize-2025", OPENED),
    "bg_lit": ("https://lithub.com/helen-garner-has-won-the-2025-baillie-gifford-prize-for-nonfiction", OPENED),
    "booker_lit": ("https://lithub.com/heres-the-shortlist-for-the-2026-booker-prize/", OPENED),
    "booker_br": ("https://bookriot.com/booker-prize-shortlist-2026/", SEARCH),
    # ---------------- Organisations
    "upu_wiki": ("https://en.wikipedia.org/wiki/Universal_Postal_Union", OPENED),
    "gcc_wiki": ("https://en.wikipedia.org/wiki/Gulf_Cooperation_Council", OPENED),
    "unido_wiki": ("https://en.wikipedia.org/wiki/United_Nations_Industrial_Development_Organization", OPENED),
    "iea_wiki": ("https://en.wikipedia.org/wiki/International_Energy_Agency", OPENED),
    "afdb_wiki": ("https://en.wikipedia.org/wiki/African_Development_Bank", OPENED),
    # ---------------- Reports
    "wmr_wiki": ("https://en.wikipedia.org/wiki/World_Migration_Report", OPENED),
    "ghi_fpj": ("https://www.freepressjournal.in/world/world-food-day-2026-india-ranks-100th-among-122-countries-in-"
                "global-hunger-index", OPENED),
    "imd_gk": ("https://www.gktoday.in/indias-performance-in-international-economic-rankings/", OPENED),
    "ief_wiki": ("https://en.wikipedia.org/wiki/Index_of_Economic_Freedom", OPENED),
    "eiu_wiki": ("https://en.wikipedia.org/wiki/The_Economist_Democracy_Index", OPENED),
    "sowc_wiki": ("https://en.wikipedia.org/wiki/The_State_of_the_World%27s_Children", OPENED),
    "gsi_wiki": ("https://en.wikipedia.org/wiki/Global_Slavery_Index", OPENED),
    "hci_wiki": ("https://en.wikipedia.org/wiki/Human_Capital_Index", OPENED),
    "sofi_fao": ("https://www.fao.org/publications/home/fao-flagship-publications/the-state-of-food-security-and-"
                 "nutrition-in-the-world/en", OPENED),
    # ---------------- Economic
    "wb_ians": ("https://ianslive.in/world-bank-lifts-india-growth-outlook-despite-gulf-war-embargoed-until-thursday-"
                "june-11-at-7-pm-ist--20260611081504", OPENED),
    "imf_fpj": ("https://www.freepressjournal.in/business/imf-raises-indias-growth-forecast-to-65-in-fy27-after-eased-"
                "tariffs-despite-war", OPENED),
    "gdp_print": ("https://theprint.in/economy/economy-grows-by-7-8-pc-in-q3-of-fy26-as-per-new-gdp-series-govt-data/"
                  "2865636", OPENED),
    "wpi_air": ("https://newsonair.gov.in/wholesale-price-index-inflation-rises-to-11-39-in-september-this-year/",
                OPENED),
    "gst_print": ("https://theprint.in/economy/gst-collections-rise-9-pc-to-over-rs-2-lakh-cr-in-march-third-highest-in-"
                  "fy26/2893963", OPENED),
    "exp_air": ("https://newsonair.gov.in/indias-exports-cross-860-billion-in-2025-26-says-union-minister-piyush-goyal/",
                OPENED),
    "exp_asianet": ("https://newsable.asianetnews.com/business/indias-exports-hit-record-high-of-860-billion-in-fy26-up-"
                    "422-articleshow-k17rqvx", SEARCH),
    "fd_wi": ("https://news.webindia123.com/news/Articles/Business/20261030/4513727.html", OPENED),
    "cpi_angel": ("https://www.angelone.in/news/economy/india-s-retail-inflation-rises-to-4-38-in-june-2026-food-"
                  "inflation-at-5-32", OPENED),
    "fdi_om": ("https://www.outlookmoney.com/invest/fdi-equity-inflows-jump-18-to-5884-billion-in-fy26", OPENED),
    "cad_ob": ("https://www.outlookbusiness.com/news/india-records-71-bn-current-account-surplus-in-q4-fy26-rbi-data",
               OPENED),
    "adb_adb": ("https://www.adb.org/news/adb-projects-india-gdp-moderate-6-9-percent-fy2026-rising-7-3-percent-fy2027",
                OPENED),
    "adb_fpj": ("https://www.freepressjournal.in/business/adb-cuts-india-fy27-growth-forecast-to-66-amid-higher-oil-"
                "costs", OPENED),
    "mpcapr_5p": ("https://www.5paisa.com/news/rbi-keeps-repo-rate-at-525-5-key-takeaways-from-april-mpc-decision",
                  OPENED),
    "mpcapr_ao": ("https://www.angelone.in/news/economy/rbi-kept-repo-rate-unchanged-maintained-policy-stance-neutral",
                  SEARCH),
    "mpcaug_scc": ("https://www.scconline.com/blog/post/2026/08/10/rbi-repo-rate-unchanged-august-2026-neutral-stance/",
                   OPENED),
    "plfs_dd": ("https://ddindia.co.in/2026/10/urban-workforce-participation-improves-in-september-female-lfpr-reaches-"
                "highest-level-since-october-2025/", OPENED),
    # ---------------- Policy
    "keralam_scc": ("https://www.scconline.com/blog/post/2026/08/21/parliament-monsoon-session-2026-key-acts-bills/",
                    OPENED),
    # ---------------- Business
    "metsera_rte": ("https://www.rte.ie/news/business/2025/1110/1543102-pfizer-wins-10-billion-bidding-war-for-metsera",
                    OPENED),
    "metsera_fp": ("https://www.fiercepharma.com/biotech/pfizer-finalizes-metsera-buy-after-contentious-bidding-war-"
                   "novo-nordisk", SEARCH),
    "exact_md": ("https://www.massdevice.com/abbott-confirms-21b-exact-sciences-acquisition/", SEARCH),
    "exact_ipp": ("https://www.indianpharmapost.com/news/abbott-to-acquire-exact-sciences-for-21-billion-18350", SEARCH),
    "ibm_tz": ("https://www.techzine.eu/news/infrastructure/137056/ibm-to-acquire-confluent-for-11-billion/", OPENED),
    "meesho_week": ("https://www.theweek.in/news/biz-tech/2025/12/10/meesho-shares-debut-on-nse-and-bse-at-46-per-cent-"
                    "premium-for-alloted-investors.html", OPENED),
    "lens_week": ("https://www.theweek.in/news/biz-tech/2025/11/10/lenskart-ipo-makes-a-weak-debut-on-bourses-lists-at-"
                  "1-74-per-cent-discount-to-issue-price.html", OPENED),
    "iveco_mio": ("https://www.motorindiaonline.in/tata-motors-completes-iveco-acquisition-for-e3-43-billion/", OPENED),
    "sun_gene": ("https://www.geneonline.com/sun-pharma-acquires-organon-in-12-billion-deal-largest-takeover-by-indian-"
                 "pharma-company/", OPENED),
    "anomaly_week": ("https://www.theweek.in/wire-updates/business/2026/04/30/reliance-retail-acquires-priyanka-"
                     "chopra%E2%80%99s-haircare-brand-anomaly.html", OPENED),
    "nagarro_p2": ("https://pulse2.com/nagarro-board-backs-persistents-e81-per-share-takeover-offer-at-140-premium/",
                   SEARCH),
    "nagarro_ent": ("https://india.entrepreneur.com/business-news/persistents-takeover-offer-for-nagarro-succeeds-"
                    "secures-83-25-stake", SEARCH),
    # ---------------- Static
    "ranth_wiki": ("https://en.wikipedia.org/wiki/Ranthambore_National_Park", OPENED),
    "bandh_wiki": ("https://en.wikipedia.org/wiki/Bandhavgarh_National_Park", OPENED),
    "koyna_wiki": ("https://en.wikipedia.org/wiki/Koyna_Dam", OPENED),
    "idukki_wiki": ("https://en.wikipedia.org/wiki/Idukki_Dam", OPENED),
    "isagar_wiki": ("https://en.wikipedia.org/wiki/Indira_Sagar_Dam", OPENED),
    "ghnp_wiki": ("https://en.wikipedia.org/wiki/Great_Himalayan_National_Park", OPENED),
    "megh_wiki": ("https://en.wikipedia.org/wiki/Meghalaya", OPENED),
    "chh_wiki": ("https://en.wikipedia.org/wiki/Chhattisgarh", OPENED),
    "vof_wiki": ("https://en.wikipedia.org/wiki/Valley_of_Flowers_National_Park", OPENED),
    "huf_wiki": ("https://en.wikipedia.org/wiki/Hungarian_forint", OPENED),
    "miz_wiki": ("https://en.wikipedia.org/wiki/Mizoram", OPENED),
    "nok_wiki": ("https://en.wikipedia.org/wiki/Norwegian_krone", OPENED),
    "wlg_wiki": ("https://en.wikipedia.org/wiki/Wellington", OPENED),
    "uga_wiki": ("https://en.wikipedia.org/wiki/Uganda", OPENED),
    "czk_wiki": ("https://en.wikipedia.org/wiki/Czech_koruna", OPENED),
}


def fact(claim, key):
    url, how = U[key]
    return {"claim": claim, "source_url": url, "checked_on": TODAY, "_how": how}


# ====================================================================== National Current Affairs (4 / 4 / 5)
T = "National Current Affairs"
GOV, ST, DEF = "Government decisions", "States and UTs", "Defence"

G(T, DEF, "Basic",
  "INS Aridhaman, commissioned into the Indian Navy on 3 April 2026, is India's third vessel of which type?",
  ["Nuclear-powered ballistic missile submarine (SSBN)", "Stealth guided-missile frigate",
   "Indigenous aircraft carrier", "Anti-submarine warfare shallow water craft"], "*",
  "India's SSBN fleet",
  "INS Aridhaman (hull S4) was commissioned on 3 April 2026 as India's third nuclear-powered ballistic missile "
  "submarine. It follows INS Arihant (commissioned 2016) and INS Arighaat (commissioned August 2024), and is larger "
  "than its predecessors, carrying more long-range missiles.",
  ["SSBN 1: INS Arihant (2016)", "SSBN 2: INS Arighaat (Aug 2024)", "SSBN 3: INS Aridhaman (3 Apr 2026)"],
  [fact("India commissions its third nuclear-powered ballistic missile submarine INS Aridhaman; predecessors Arihant "
        "and Arighaat", "arid_print"),
   fact("INS Aridhaman, India's third nuclear-powered submarine, commissioned on Friday 3 April 2026", "arid_tv")],
  why="Aridhaman is a submarine, not a frigate, carrier or shallow water craft.",
  current=ca("2026-04-03"))

G(T, DEF, "Basic",
  "Exercise Malabar 2025, held from 10 to 18 November 2025 by the navies of India, the US, Japan and Australia, took "
  "place in and around which location?",
  ["Guam", "Visakhapatnam", "Okinawa", "Darwin"], "*",
  "Malabar 2025",
  "The 2025 edition of the four-nation naval exercise Malabar was held in and around Guam, a US territory in the "
  "western Pacific, from 10 to 18 November 2025. India sent the stealth frigate INS Sahyadri.",
  ["Malabar 2025: 10-18 Nov 2025", "Venue: Guam and the West Pacific", "Indian ship: INS Sahyadri"],
  [fact("Malabar 2025 held 10-18 November 2025 in and around Guam with Australia, India, Japan and the US; INS "
        "Sahyadri took part", "malabar_baird"),
   fact("INS Sahyadri docks at Guam for Malabar-2025", "malabar_ians")],
  why="Visakhapatnam, Okinawa and Darwin did not host Malabar 2025.",
  current=ca("2025-11-10"))

G(T, DEF, "Basic",
  "The 18th edition of Exercise Nomadic Elephant was held at Pithoragarh, Uttarakhand, from 21 September to 3 October "
  "2026. It is a joint military exercise between India and which country?",
  ["Mongolia", "Kazakhstan", "Kyrgyzstan", "Nepal"], "*",
  "Exercise Nomadic Elephant",
  "Nomadic Elephant is an annual India-Mongolia exercise held alternately in the two countries. The 18th edition was "
  "held at the Foreign Training Node, Pithoragarh; the previous one was at Ulaanbaatar in May-June 2025.",
  ["Nomadic Elephant: India-Mongolia", "18th edition: Pithoragarh, 21 Sep-3 Oct 2026"],
  [fact("18th India-Mongolia exercise Nomadic Elephant begins at Pithoragarh, 21 Sep to 3 Oct 2026; last edition at "
        "Ulaanbaatar", "nomadic_air")],
  why="Kazakhstan (Prabal Dostyk), Kyrgyzstan (Khanjar) and Nepal (Surya Kiran) have other exercises with India.",
  current=ca("2026-09-21"))

G(T, ST, "Basic",
  "In May 2026, which state became the first in India to complete all priority areas under Phase I and Phase II of "
  "the Centre's compliance reduction and deregulation initiative?",
  ["Tripura", "Gujarat", "Odisha", "Haryana"], "*",
  "Deregulation initiative",
  "Tripura completed all 51 priority reform areas under Deregulation Phase I and Phase II, becoming the first state "
  "to do so (reported 15 May 2026). The national initiative is led by the Cabinet Secretariat.",
  ["State: Tripura", "51 priority areas (Phase I and II)", "Initiative led by the Cabinet Secretariat"],
  [fact("Tripura becomes first state to complete all deregulation priority areas under Phase I and II; 51 areas; "
        "initiative led by Cabinet Secretariat", "tripura_itne")],
  why="None of the other states was reported as the first to complete both phases.",
  current=ca("2026-05-15"))

G(T, DEF, "Intermediate",
  "The 7th edition of Exercise Dharma Guardian was held at Chaubattia, Uttarakhand, from February to March 2026. It "
  "is a joint military exercise between India and which country?",
  ["Japan", "France", "Australia", "Singapore"], "*",
  "Exercise Dharma Guardian",
  "Dharma Guardian is the annual India-Japan army exercise, held alternately in the two countries. Its 7th edition "
  "began at Chaubattia, Uttarakhand, in late February 2026.",
  ["Dharma Guardian: India-Japan", "7th edition: Chaubattia, Uttarakhand (Feb 2026)"],
  [fact("Dharma Guardian 2026, 7th edition, India and Japan, at Chaubattia, Uttarakhand", "dharma_drishti")],
  why="France (Shakti), Australia (AUSTRAHIND) and Singapore (Agni Warrior) have differently named exercises.",
  current=ca("2026-02-24"))

G(T, DEF, "Intermediate",
  "AUSTRAHIND 2026, the fifth edition of the India-Australia joint military exercise, began in October 2026 at which "
  "place?",
  ["Thiruvananthapuram", "Belagavi", "Pithoragarh", "Umroi"], "*",
  "AUSTRAHIND 2026",
  "The fifth edition of AUSTRAHIND opened at the Foreign Training Node in Thiruvananthapuram, Kerala, around "
  "20 October 2026 and runs to 1 November. New Zealand sent observers for the first time.",
  ["Exercise: AUSTRAHIND (India-Australia), 5th edition", "Venue: Thiruvananthapuram"],
  [fact("AUSTRAHIND 2026, fifth edition, commenced at Thiruvananthapuram; concludes 1 November", "austrahind_air")],
  why="Belagavi hosted Mitra Shakti, Pithoragarh hosted Nomadic Elephant and Umroi hosted PRAGATI.",
  current=ca("2026-10-20"))

G(T, DEF, "Intermediate",
  "Yudh Abhyas 2026, which began in September 2026 at Auli (Uttarakhand) and Mahajan (Rajasthan), is a joint military "
  "exercise between India and which country?",
  ["United States", "United Kingdom", "Russia", "Egypt"], "*",
  "Exercise Yudh Abhyas",
  "Yudh Abhyas is the India-US army exercise. The 2026 edition began in mid-September 2026 at two locations, Auli in "
  "Uttarakhand and Mahajan in Rajasthan.",
  ["Yudh Abhyas: India-US", "2026 venues: Auli and Mahajan"],
  [fact("India-US Yudh Abhyas 2026 begins at Auli and Mahajan", "yudh_gk")],
  why="The UK exercise is Ajeya Warrior, Russia's is INDRA and Egypt's is Cyclone.",
  current=ca("2026-09-15"))

G(T, GOV, "Intermediate",
  "In October 2026 the Appointments Committee of the Cabinet extended the tenure of Rajesh Kumar Singh by one year, "
  "to 31 October 2027. Which post does he hold?",
  ["Defence Secretary", "Cabinet Secretary", "Home Secretary", "Finance Secretary"], "*",
  "Defence Secretary's extension",
  "On 24 October 2026 the ACC extended Defence Secretary Rajesh Kumar Singh's service by one year, until "
  "31 October 2027 or until further orders. He is a 1989-batch IAS officer of the Kerala cadre.",
  ["Post: Defence Secretary", "Extension: to 31 Oct 2027", "Approved by ACC on 24 Oct 2026"],
  [fact("Defence Secretary Rajesh Kumar Singh gets one-year extension to 31 Oct 2027; approved by ACC on 24 Oct 2026",
        "defsec_nk")],
  why="He is the Defence Secretary, not the Cabinet, Home or Finance Secretary.",
  current=ca("2026-10-24"))

GS(T, ST, "Advanced", "the end of President's Rule in Manipur in February 2026",
   ["President's Rule was revoked on 4 February 2026 and Yumnam Khemchand Singh was sworn in as Chief Minister.",
    "President's Rule had been imposed under Article 356 on 13 February 2025, after N. Biren Singh resigned.",
    "The oath was administered by Governor Ajay Kumar Bhalla at Raj Niwas, Imphal."],
   [True, True, False],
   "Manipur government formation",
   "The MHA revoked President's Rule on 4 February 2026 and BJP MLA Y. Khemchand Singh took oath the same day. "
   "President's Rule had been imposed under Article 356 on 13 February 2025. Governor Ajay Kumar Bhalla administered "
   "the oath at Lok Bhavan (the renamed Raj Bhavan), not at a 'Raj Niwas'.",
   [fact("President's Rule revoked effective 4 Feb 2026; Y. Khemchand Singh to be sworn in at Lok Bhavan; imposed 13 "
         "Feb 2025 under Article 356; Governor Ajay Kumar Bhalla", "manipur_print"),
    fact("President's Rule revoked in Manipur", "manipur_air")],
   why="Statement 3 is wrong: the oath was taken at Lok Bhavan.",
   current=ca("2026-02-04"))

GS(T, DEF, "Advanced", "the International Fleet Review (IFR) 2026",
   ["It was held off Visakhapatnam, where the President reviewed the fleet on 18 February 2026.",
    "The President reviewed the fleet from INS Sumedha, which served as the Presidential Yacht.",
    "Exercise MILAN was held alongside it."],
   [True, True, True],
   "IFR 2026",
   "President Droupadi Murmu, as Supreme Commander, reviewed the fleet at the Review Anchorage Area off "
   "Visakhapatnam on 18 February 2026, embarked on INS Sumedha. The multilateral naval exercise MILAN was held "
   "alongside, with around 70 countries taking part.",
   [fact("IFR 2026: President reviewed fleets on 18 Feb from INS Sumedha (Presidential Yacht); MILAN held alongside off "
         "Visakhapatnam", "ifr_org"),
    fact("President Murmu to witness International Fleet Review 2026 in Visakhapatnam", "ifr_air")],
   why="All three statements are correct.",
   current=ca("2026-02-18"))

GS(T, ST, "Advanced", "Sikkim being declared a fully literate state in May 2026",
   ["The declaration was made under the ULLAS programme of the Ministry of Education.",
    "Sikkim became the first fully literate state in India.",
    "It was announced at the Sikkim University convocation in the presence of President Droupadi Murmu."],
   [True, False, True],
   "Sikkim fully literate",
   "Sikkim was recognised as fully literate under ULLAS (Understanding of Lifelong Learning for All in Society), the "
   "adult-literacy programme under NEP 2020. It is the fifth fully literate state and the third in the Northeast; "
   "Mizoram was the first.",
   [fact("Sikkim becomes India's fifth fully literate state under ULLAS; third in Northeast; Mizoram first; announced "
         "at Sikkim University convocation with President Murmu", "sikkim_na"),
    fact("Sikkim declared fully literate state under ULLAS programme", "sikkim_gk")],
   why="Statement 2 is wrong: Sikkim is the fifth such state.",
   current=ca("2026-05-27"))

GS(T, ST, "Advanced", "the statehood resolution of the Jammu and Kashmir Legislative Assembly",
   ["It was moved by Chief Minister Omar Abdullah and passed on 28 September 2026.",
    "It sought the immediate restoration of full statehood.",
    "It was passed unanimously, with BJP legislators voting in favour."],
   [True, True, False],
   "J&K statehood resolution",
   "Omar Abdullah moved the resolution on 25 September 2026 and the Assembly passed it by voice vote on 28 September, "
   "seeking 'immediate restoration of full Statehood'. The 29 BJP legislators opposed it and walked out.",
   [fact("J&K Assembly passed statehood resolution on 28 Sep 2026, moved by CM Omar Abdullah; BJP legislators opposed "
         "and walked out", "jk_tnpsc")],
   why="Statement 3 is wrong: the BJP opposed it and walked out.",
   current=ca("2026-09-28"))

GS(T, DEF, "Advanced", "Exercise PRAGATI 2026",
   ["PRAGATI stands for Partnership of Regional Armies for Growth and Transformation in the Indian Ocean Region.",
    "It began at Umroi Military Station in Meghalaya on 20 May 2026.",
    "Armies of 12 friendly nations, including Pakistan and China, took part."],
   [True, True, False],
   "Exercise PRAGATI",
   "PRAGATI 2026 began at Umroi, Meghalaya, on 20 May 2026 with 12 nations: Bhutan, Cambodia, Indonesia, Laos, "
   "Malaysia, Maldives, Myanmar, Nepal, the Philippines, Seychelles, Sri Lanka and Vietnam. Pakistan and China were "
   "not among them.",
   [fact("PRAGATI 2026 began 20 May 2026 at Umroi Military Station, Meghalaya; 12 nations listed; full form given",
         "pragati_dd")],
   why="Statement 3 is wrong: neither Pakistan nor China took part.",
   current=ca("2026-05-20"))

# ====================================================================== International Current Affairs (3 / 12 / 3)
T = "International Current Affairs"
BI, GE = "Bilateral relations", "Global events"

G(T, GE, "Basic",
  "Billionaire Andrej Babiš, leader of the ANO party, was appointed Prime Minister of which country on 9 December "
  "2025?",
  ["Czech Republic", "Slovakia", "Hungary", "Poland"], "*",
  "Czech Prime Minister",
  "President Petr Pavel appointed Andrej Babiš, 71, as Czech Prime Minister on 9 December 2025 after ANO won the "
  "October election. Babiš said he would put his Agrofert group into a trust to resolve a conflict of interest.",
  ["Country: Czech Republic", "Appointed by: President Petr Pavel, 9 Dec 2025", "Party: ANO"],
  [fact("Czech President Petr Pavel appoints Andrej Babis (ANO) as prime minister on 9 Dec 2025", "babis_star")],
  why="Slovakia, Hungary and Poland have other prime ministers.",
  current=ca("2025-12-09"))

G(T, GE, "Basic",
  "Rob Jetten, sworn in on 23 February 2026 as his country's youngest-ever prime minister, heads the government of "
  "which country?",
  ["Netherlands", "Belgium", "Denmark", "Luxembourg"], "*",
  "Dutch Prime Minister",
  "King Willem-Alexander swore in Rob Jetten of the centrist D66 at Huis ten Bosch Palace on 23 February 2026. He is "
  "the Netherlands' youngest and first openly gay prime minister and leads a minority coalition of D66, CDA and VVD "
  "with 66 of 150 seats.",
  ["Country: Netherlands", "Party: D66", "Sworn in: 23 Feb 2026"],
  [fact("Rob Jetten sworn in as Dutch PM on 23 Feb 2026; youngest-ever; D66-CDA-VVD minority with 66 of 150 seats",
        "jetten_eu")],
  why="Belgium, Denmark and Luxembourg have other heads of government.",
  current=ca("2026-02-23"))

G(T, GE, "Basic",
  "After the Scottish Parliament election of 7 May 2026, in which the SNP won 58 of 129 seats, who was re-elected "
  "First Minister of Scotland?",
  ["John Swinney", "Humza Yousaf", "Anas Sarwar", "Alex Cole-Hamilton"], "*",
  "Scottish election 2026",
  "The SNP won 58 of 129 seats, seven short of a majority, in the election of 7 May 2026. John Swinney was re-elected "
  "First Minister by the Parliament in May 2026 to lead a minority government.",
  ["Election: 7 May 2026", "SNP: 58 of 129 seats", "First Minister: John Swinney"],
  [fact("2026 Scottish Parliament election on 7 May; SNP 58 of 129 seats; First Minister John Swinney", "scot_wiki"),
   fact("Swinney re-elected First Minister", "scot_ms")],
  why="Yousaf was an earlier First Minister; Sarwar (Labour) and Cole-Hamilton (Lib Dem) lead other parties.",
  current=ca("2026-05-07"))

G(T, GE, "Intermediate",
  "To Lam was re-elected General Secretary of which country's ruling Communist Party on 23 January 2026, after its "
  "14th National Party Congress?",
  ["Vietnam", "Laos", "China", "Cuba"], "*",
  "Vietnam's party leadership",
  "The 14th Central Committee of the Communist Party of Vietnam unanimously re-elected To Lam as General Secretary at "
  "its first plenum in Hanoi on 23 January 2026. The 14th Congress had opened on 20 January.",
  ["Party: Communist Party of Vietnam", "Congress: 14th (opened 20 Jan 2026)", "Re-elected: 23 Jan 2026, unanimous"],
  [fact("14th Central Committee of the CPV unanimously re-elected To Lam General Secretary on 23 Jan 2026",
        "tolam_vns")],
  why="Laos, China and Cuba have their own party leaders.",
  current=ca("2026-01-23"))

G(T, GE, "Intermediate",
  "In Sweden's general election of 13 September 2026, the left-leaning opposition won 176 of 349 seats. Which "
  "outgoing Prime Minister announced he would resign?",
  ["Ulf Kristersson", "Stefan Löfven", "Jonas Gahr Støre", "Mette Frederiksen"], "*",
  "Sweden election 2026",
  "The four left-wing opposition parties won 176 of 349 seats against 173 for the outgoing bloc. Centre-right Prime "
  "Minister Ulf Kristersson said he would resign; Social Democrat leader Magdalena Andersson, whose party was the "
  "largest, was seen as the likely successor.",
  ["Election: 13 Sep 2026", "Left bloc 176, outgoing bloc 173", "Outgoing PM: Ulf Kristersson"],
  [fact("Sweden PM Kristersson to resign as left-wing bloc wins 176 of 349 seats; election 13 September 2026",
        "swe_aj")],
  why="Löfven is a former Swedish PM; Støre and Frederiksen lead Norway and Denmark.",
  current=ca("2026-09-13"))

G(T, GE, "Intermediate",
  "On 14 May 2026, Iraq's parliament approved the government of a new Prime Minister, then aged 40 and the youngest "
  "to hold the post. Who is he?",
  ["Ali al-Zaidi", "Mohammed Shia al-Sudani", "Mustafa al-Kadhimi", "Fuad Hussein"], "*",
  "Iraq's new government",
  "Ali al-Zaidi, named prime minister-designate on 27 April 2026, won a confidence vote on 14 May 2026, but only 14 "
  "of 23 ministers were approved; posts such as interior and defence stayed vacant. Fuad Hussein was kept as foreign "
  "minister.",
  ["New PM: Ali al-Zaidi (age 40)", "Confidence vote: 14 May 2026", "Partial cabinet: 14 of 23 ministers"],
  [fact("Iraq's parliament approves Ali al-Zaidi government on 14 May 2026; 14 of 23 ministers; Fuad Hussein foreign "
        "minister", "iraq_aj")],
  why="Al-Sudani and al-Kadhimi are former prime ministers; Fuad Hussein is the foreign minister.",
  current=ca("2026-05-14"))

G(T, BI, "Intermediate",
  "During his state visit to Bhutan, Prime Minister Modi inaugurated a 1,020 MW hydroelectric project on 11 November "
  "2025. Which project was it?",
  ["Punatsangchhu-II", "Mangdechhu", "Kholongchhu", "Chukha"], "*",
  "India-Bhutan hydropower",
  "The 1,020 MW Punatsangchhu-II Hydroelectric Project was inaugurated on 11 November 2025 during PM Modi's state "
  "visit to Bhutan, marking the start of electricity exports from it to India. Work on the 1,200 MW Punatsangchhu-I "
  "was also to resume.",
  ["Project: Punatsangchhu-II (1,020 MW)", "Inaugurated: 11 Nov 2025"],
  [fact("PM Modi inaugurates 1,020 MW Punatsangchhu-II hydroelectric project in Bhutan on 11 Nov 2025", "bhutan_ob")],
  why="Mangdechhu (720 MW) was inaugurated in 2019; Kholongchhu and Chukha are other projects.",
  current=ca("2025-11-11"))

G(T, BI, "Intermediate",
  "German Chancellor Friedrich Merz visited India on 12-13 January 2026. In which state did he hold talks with Prime "
  "Minister Modi, after which 19 agreements were signed?",
  ["Gujarat", "Maharashtra", "Karnataka", "Delhi"], "*",
  "Merz in India",
  "Merz's two-day visit was in Gujarat: delegation-level talks at Mahatma Mandir, Gandhinagar, and events in "
  "Ahmedabad, including the kite festival. The two sides signed 19 agreements; the visit marked 25 years of the "
  "Strategic Partnership. He then went to Bengaluru.",
  ["Visit: 12-13 Jan 2026", "Talks: Gandhinagar, Gujarat", "19 agreements signed"],
  [fact("Merz's two-day Gujarat visit on 12-13 Jan 2026; talks at Mahatma Mandir, Gandhinagar; 19 agreements",
        "merz_ians")],
  why="The talks were held in Gujarat; Bengaluru (Karnataka) was his next stop.",
  current=ca("2026-01-12"))

G(T, BI, "Intermediate",
  "After talks between Prime Minister Modi and Canadian Prime Minister Mark Carney in New Delhi in early March 2026, "
  "the two sides decided to expedite which agreement?",
  ["Comprehensive Economic Partnership Agreement (CEPA)", "Civil Nuclear Cooperation Agreement",
   "Mutual Legal Assistance Treaty", "Double Taxation Avoidance Agreement"], "*",
  "India-Canada reset",
  "Carney's official visit to India (late February to 2 March 2026) reset ties strained since 2023. The leaders "
  "decided to expedite talks on a Comprehensive Economic Partnership Agreement; energy cooperation was described as "
  "a defining pillar of the visit.",
  ["Visit: Carney to India, Feb-Mar 2026", "Decision: expedite CEPA negotiations"],
  [fact("PM Modi and Mark Carney hold talks in New Delhi; decide to expedite CEPA", "carney_air"),
   fact("Canadian PM Mark Carney arrives in Mumbai on four-day official visit to India", "carney_sm")],
  why="The other agreements were not the focus announced after the talks.",
  current=ca("2026-03-02"))

G(T, BI, "Intermediate",
  "Prime Minister Modi arrived in Auckland on 10 July 2026 for the first official visit by an Indian Prime Minister to "
  "New Zealand in how many years?",
  ["40 years", "20 years", "25 years", "60 years"], "*",
  "Modi in New Zealand",
  "New Zealand PM Christopher Luxon said the July 2026 visit was the first official visit by an Indian PM in 40 years. "
  "It followed the India-New Zealand free trade agreement signed in April 2026.",
  ["Visit: Auckland, 10-11 July 2026", "First in 40 years"],
  [fact("Modi to make first official visit to New Zealand in 40 years; arrives Auckland on 10 July 2026",
        "nz_star"),
   fact("PM Modi arrives in Auckland for first visit by an Indian PM to New Zealand in four decades", "nz_swarajya")],
  why="The gap was four decades, not 20, 25 or 60 years.",
  current=ca("2026-07-10"))

G(T, BI, "Intermediate",
  "During Prime Minister Modi's visit to Oslo in May 2026, the first by an Indian PM since 1983, India-Norway ties "
  "were elevated to which level?",
  ["Green Strategic Partnership", "Comprehensive Strategic Partnership", "Special Strategic Partnership",
   "Privileged Partnership"], "*",
  "India-Norway",
  "On 18 May 2026 PM Modi and Norwegian PM Jonas Gahr Støre raised ties to a Green Strategic Partnership covering "
  "green shipping, clean energy and ocean-based activities. Modi then attended the 3rd India-Nordic Summit in Oslo.",
  ["Visit: Oslo, May 2026", "Ties: Green Strategic Partnership"],
  [fact("PM Modi and Norwegian PM Store elevate India-Norway ties to Green Strategic Partnership", "norway_sm"),
   fact("PM Modi becomes first Indian PM in 40 years to visit Norway, seals Green Strategic Partnership",
        "norway_org")],
  why="The other labels describe India's ties with other countries (for example, Israel's Special Strategic "
      "Partnership in 2026).",
  current=ca("2026-05-18"))

G(T, BI, "Intermediate",
  "During Prime Minister Modi's visit to the UAE in May 2026, ADNOC agreed to potentially expand its crude oil "
  "storage in India's strategic petroleum reserves to up to how much?",
  ["30 million barrels", "6 million barrels", "60 million barrels", "100 million barrels"], "*",
  "India-UAE energy ties",
  "On the first leg of his May 2026 five-nation tour, Modi and the UAE agreed a framework for a strategic defence "
  "partnership and an LPG pact; ADNOC's crude storage in India could rise to up to 30 million barrels. Under a 2018 "
  "deal ADNOC stored about six million barrels.",
  ["ADNOC storage in India: up to 30 million barrels", "Also: strategic defence partnership framework, LPG pact"],
  [fact("India-UAE: strategic defence partnership framework; ADNOC crude storage in India potentially up to 30 million "
        "barrels; LPG pact; USD 5 bn investment", "uae_gt")],
  why="Six million barrels was the 2018 arrangement; 60 and 100 million were not the figures.",
  current=ca("2026-05-15"))

G(T, BI, "Intermediate",
  "During Prime Minister Modi's visit to the Netherlands in May 2026, an MoU between Tata Electronics and which Dutch "
  "company was signed to support a semiconductor fab at Dholera, Gujarat?",
  ["ASML", "Philips", "NXP Semiconductors", "Shell"], "*",
  "India-Netherlands Strategic Partnership",
  "India and the Netherlands elevated ties to a Strategic Partnership with a 2026-2030 roadmap and 17 outcomes, "
  "including an MoU between Tata Electronics and ASML, the Dutch maker of chip lithography machines, for the Dholera "
  "fab, and the return of the Chola copper plates.",
  ["17 outcomes; Strategic Partnership", "Tata Electronics-ASML MoU for Dholera fab"],
  [fact("Modi hails 17 agreements with Netherlands under PM Rob Jetten; Strategic Partnership; Tata Electronics-ASML "
        "MoU for Dholera fab", "nl_print")],
  why="Philips, NXP and Shell were not party to the Dholera MoU.",
  current=ca("2026-05-16"))

G(T, GE, "Intermediate",
  "The 3rd India-Nordic Summit, attended by Prime Minister Modi and the prime ministers of the five Nordic countries, "
  "was held on 19 May 2026 in which city?",
  ["Oslo", "Stockholm", "Copenhagen", "Helsinki"], "*",
  "India-Nordic Summit",
  "Norway's PM Jonas Gahr Støre hosted the 3rd India-Nordic Summit in Oslo on 19 May 2026. The first was held in "
  "Stockholm (2018) and the second in Copenhagen (2022).",
  ["3rd India-Nordic Summit: Oslo, 19 May 2026", "Host: Norway"],
  [fact("PM Modi to attend 3rd India-Nordic Summit in Oslo, Norway, on 19 May 2026", "nordic_air"),
   fact("3rd India-Nordic Summit 2026 held in Oslo, Norway", "nordic_vision")],
  why="Stockholm and Copenhagen hosted the earlier summits; Helsinki has not hosted one yet.",
  current=ca("2026-05-19"))

G(T, GE, "Intermediate",
  "In Ethiopia's seventh general election, held on 1 June 2026, which party won 438 of the 501 contested seats in the "
  "House of Peoples' Representatives?",
  ["Prosperity Party", "Tigray People's Liberation Front", "National Movement of Amhara", "Ezema"], "*",
  "Ethiopia election 2026",
  "The ruling Prosperity Party of Prime Minister Abiy Ahmed won 438 of 501 contested seats in the 1 June 2026 "
  "election, results announced on 21 June. Voting did not take place in parts of Amhara and Tigray.",
  ["Election: 1 June 2026 (7th general election)", "Prosperity Party: 438 of 501 seats"],
  [fact("Prosperity Party wins 438 of 501 seats; election on 1 June 2026", "eth_dawan"),
   fact("Prosperity Party wins majority in Ethiopia's Seventh General Election held on 1 June", "eth_ena")],
  why="The other parties are opposition or regional parties with few or no seats.",
  current=ca("2026-06-01"))

GS(T, GE, "Advanced", "Uganda's presidential election of January 2026",
   ["Yoweri Museveni was declared the winner with about 71.6% of the vote.",
    "His main challenger, Robert Kyagulanyi (Bobi Wine), won about 24.7% and rejected the result.",
    "Museveni first took office as President in 1996."],
   [True, True, False],
   "Uganda election 2026",
   "The Electoral Commission declared Museveni (NRM) the winner of the 15 January 2026 vote on 17 January with 71.61%, "
   "extending a rule that began in 1986 into a fifth decade. Kyagulanyi (NUP) got 24.72% and called it fraudulent.",
   [fact("Museveni declared winner with 71.61%; Kyagulanyi 24.72% rejected results; Museveni first took office in "
         "1986; election 15 Jan 2026", "uganda_cit"),
    fact("Museveni wins again, secures seventh term as Bobi Wine cries foul", "uganda_all")],
   why="Statement 3 is wrong: Museveni has been President since 1986.",
   current=ca("2026-01-15"))

GS(T, GE, "Advanced", "the US-Iran ceasefire announced in April 2026",
   ["It was a two-week ceasefire conditional on Iran reopening the Strait of Hormuz.",
    "The talks that followed were to be held in Islamabad, with Pakistan's Prime Minister Shehbaz Sharif as mediator.",
    "In June 2026 the two sides announced a framework for an immediate ceasefire and a roadmap to end the war."],
   [True, True, True],
   "US-Iran ceasefire",
   "On 7-8 April 2026 President Trump announced a two-week ceasefire if Iran lifted its blockade of the Strait of "
   "Hormuz. US and Iranian delegations were to meet in Islamabad, mediated by Shehbaz Sharif. On 15 June 2026 the two "
   "sides announced a memorandum setting a framework for a ceasefire and a phased roadmap to end the war.",
   [fact("Trump announces two-week ceasefire with Iran conditional on opening Strait of Hormuz; talks in Islamabad; "
         "mediator Shehbaz Sharif", "iran_bt"),
    fact("US and Iran agree peace framework and set plan to reopen Strait of Hormuz (15 June 2026)", "iran_nat")],
   why="All three statements are correct.",
   current=ca("2026-04-08"))

GS(T, BI, "Advanced", "Prime Minister Modi's state visit to Indonesia in July 2026",
   ["He held talks with President Prabowo Subianto at Merdeka Palace, Jakarta, on 7 July 2026.",
    "Indonesia signed a deal to acquire India's BrahMos supersonic cruise missiles.",
    "Prabowo conferred Indonesia's highest state honour on Modi."],
   [True, True, True],
   "India-Indonesia",
   "Modi's state visit (6-8 July 2026) included talks at Merdeka Palace on 7 July. Indonesia's defence ministry "
   "signed a contract with BrahMos Aerospace, and Prabowo conferred the Bintang Adipurna, Indonesia's highest honour, "
   "on Modi. Many agreements were signed (counts differ between reports).",
   [fact("Prabowo hosts Modi at Merdeka Palace on 7 July 2026; awards Indonesia's highest state honour",
         "indo_antara"),
    fact("Modi and Prabowo seal deal for Indonesia to acquire India's BrahMos missiles", "indo_ap"),
    fact("PM Modi highlights India-Indonesia ties as landmark agreements deepen partnership", "indo_ians")],
   why="All three statements are correct.",
   current=ca("2026-07-07"))

# ====================================================================== Government Schemes (8 / 3 / 7)
T = "Government Schemes"
CS, SL = "Central schemes", "Scheme launches and changes"

G(T, CS, "Basic",
  "Beti Bachao Beti Padhao was launched by the Prime Minister on 22 January 2015 at which place?",
  ["Panipat, Haryana", "Jhunjhunu, Rajasthan", "Varanasi, Uttar Pradesh", "Rajghat, New Delhi"], "*",
  "Beti Bachao Beti Padhao",
  "BBBP was launched at Panipat, Haryana, on 22 January 2015 to address the falling child sex ratio and promote girls' "
  "education. It is a joint initiative of the Ministries of Women and Child Development, Health and Family Welfare, "
  "and Education.",
  ["Launch: 22 Jan 2015", "Place: Panipat, Haryana"],
  [fact("BBBP launched on 22 January 2015 at Panipat, Haryana; tri-ministerial initiative", "bbbp_wiki")],
  why="Jhunjhunu hosted the POSHAN Abhiyaan launch; Rajghat saw the Swachh Bharat launch.")

G(T, CS, "Basic",
  "On which date was the Swachh Bharat Mission launched?",
  ["2 October 2014", "15 August 2014", "26 January 2015", "25 December 2014"], "*",
  "Swachh Bharat Mission",
  "The Prime Minister launched the Swachh Bharat Mission on 2 October 2014, Gandhi Jayanti, at Rajghat, New Delhi. Its "
  "rural part is run by the Department of Drinking Water and Sanitation (Jal Shakti) and its urban part by the "
  "Ministry of Housing and Urban Affairs.",
  ["Launch: 2 Oct 2014 (Gandhi Jayanti)", "Place: Rajghat, New Delhi"],
  [fact("Swachh Bharat Mission launched on 2 October 2014 at Rajghat", "sbm_wiki")],
  why="The other dates are not linked to the launch.")

G(T, CS, "Basic",
  "The Pradhan Mantri Gram Sadak Yojana (PMGSY), which aims to give all-weather road connectivity to unconnected "
  "villages, was launched in which year?",
  ["2000", "2005", "2014", "1995"], "*",
  "PMGSY",
  "PMGSY was launched on 25 December 2000 and is run by the Ministry of Rural Development, to connect eligible "
  "unconnected habitations with all-weather roads.",
  ["Launch: 25 Dec 2000", "Ministry: Rural Development"],
  [fact("PMGSY launched 25 December 2000; Ministry of Rural Development; all-weather road connectivity",
        "pmgsy_wiki")],
  why="2005 (Bharat Nirman, NREGA), 2014 and 1995 are not PMGSY's launch year.")

G(T, CS, "Basic",
  "The Startup India initiative, administered by the Department for Promotion of Industry and Internal Trade (DPIIT), "
  "was launched on which date?",
  ["16 January 2016", "1 July 2015", "25 September 2014", "15 August 2015"], "*",
  "Startup India",
  "Startup India was launched on 16 January 2016 and is administered by DPIIT under the Ministry of Commerce and "
  "Industry.",
  ["Launch: 16 Jan 2016", "Administered by DPIIT"],
  [fact("Startup India launched on 16 January 2016; administered by DPIIT", "startup_wiki")],
  why="1 July 2015 is Digital India's launch; 25 September 2014 is Make in India's.")

G(T, CS, "Basic",
  "The Digital India programme, administered mainly by the Ministry of Electronics and Information Technology, was "
  "launched on which date?",
  ["1 July 2015", "16 January 2016", "2 October 2014", "28 August 2014"], "*",
  "Digital India",
  "The Prime Minister launched Digital India on 1 July 2015. MeitY is the main ministry administering it.",
  ["Launch: 1 July 2015", "Ministry: MeitY"],
  [fact("Digital India launched on 1 July 2015; administered by MeitY", "digital_wiki")],
  why="16 January 2016 is Startup India; 2 October 2014 is Swachh Bharat; 28 August 2014 is PMJDY.")

G(T, CS, "Basic",
  "Mission Indradhanush, a drive to raise full immunisation coverage of children and pregnant women, was launched by "
  "the Ministry of Health and Family Welfare on which date?",
  ["25 December 2014", "1 April 2015", "8 March 2018", "2 October 2016"], "*",
  "Mission Indradhanush",
  "Union Health Minister J. P. Nadda launched Mission Indradhanush on 25 December 2014. Intensified Mission "
  "Indradhanush was launched by the PM on 8 October 2017.",
  ["Launch: 25 Dec 2014", "Ministry: Health and Family Welfare"],
  [fact("Mission Indradhanush launched 25 December 2014 by Health Minister J. P. Nadda; IMI on 8 October 2017",
        "mi_wiki")],
  why="The other dates are not linked to the launch.")

G(T, SL, "Basic",
  "The 22nd instalment of PM-KISAN, about ₹2,000 each to around 9.32 crore farmers, was released by the Prime Minister "
  "on 13 March 2026 from which city?",
  ["Guwahati", "Coimbatore", "Varanasi", "Bhagalpur"], "*",
  "PM-KISAN 22nd instalment",
  "The 22nd instalment was released on 13 March 2026 at an event in Guwahati, Assam, transferring ₹2,000 each to "
  "about 9.32 crore farmers (over ₹18,640 crore).",
  ["22nd instalment: 13 Mar 2026", "Place: Guwahati, Assam", "About 9.32 crore farmers"],
  [fact("PM-KISAN 22nd instalment released 13 March 2026 at Guwahati; about 9.32 crore farmers; ₹2,000 each",
        "kisan_angel"),
   fact("PM Modi to release 22nd instalment from Guwahati", "kisan_tv")],
  why="Coimbatore hosted the 21st instalment; Varanasi and Bhagalpur hosted earlier ones.",
  current=ca("2026-03-13"))

G(T, SL, "Basic",
  "In July 2026 the Union Cabinet approved an expanded Khelo India Scheme, together with enhanced assistance to "
  "National Sports Federations, for 2026-27 to 2030-31. What is the combined outlay?",
  ["₹36,441 crore", "₹3,165 crore", "₹84,084 crore", "₹62,500 crore"], "*",
  "Expanded Khelo India",
  "The Cabinet approved ₹36,441 crore for the expanded Khelo India Scheme and assistance to National Sports "
  "Federations for 2026-27 to 2030-31, giving a pathway from the grassroots up to the Target Olympic Podium Scheme.",
  ["Outlay: ₹36,441 crore", "Period: 2026-27 to 2030-31"],
  [fact("Cabinet approves expanded Khelo India scheme with ₹36,441 crore outlay for 2026-27 to 2030-31",
        "khelo_air")],
  why="₹84,084 crore is Samudra Manthan and ₹62,500 crore the Mobile Phone Manufacturing Scheme.",
  current=ca("2026-07-31"))

G(T, SL, "Intermediate",
  "The Small Hydro Power Development Scheme approved by the Union Cabinet in March 2026, with an outlay of about "
  "₹2,584.60 crore for FY 2026-27 to 2030-31, targets about how much new capacity?",
  ["1,500 MW", "500 MW", "5,000 MW", "15,000 MW"], "*",
  "Small Hydro Power scheme",
  "The scheme supports about 1,500 MW of small hydro projects of 1 to 25 MW each, with ₹2,584.60 crore over "
  "FY 2026-27 to FY 2030-31.",
  ["Target: about 1,500 MW", "Project size: 1-25 MW", "Outlay: ₹2,584.60 crore"],
  [fact("SHP scheme: ₹2,584.60 crore, FY27-FY31, about 1,500 MW, projects of 1-25 MW", "shp_psu")],
  why="The other figures do not match the scheme's target.",
  current=ca("2026-03-18"))

G(T, SL, "Intermediate",
  "What is the budgetary outlay of the Mobile Phone Manufacturing Scheme (MPMS) approved by the Union Cabinet on "
  "15 July 2026?",
  ["₹62,500 crore", "₹1,27,500 crore", "₹22,919 crore", "₹40,000 crore"], "*",
  "Mobile Phone Manufacturing Scheme",
  "On 15 July 2026 the Cabinet approved seven decisions worth ₹2,19,353 crore, including Semicon 2.0 at ₹1,27,500 "
  "crore and the Mobile Phone Manufacturing Scheme at ₹62,500 crore (FY 2026-27 to 2030-31).",
  ["MPMS: ₹62,500 crore", "Semicon 2.0: ₹1,27,500 crore (same day)"],
  [fact("Cabinet approves ₹2.19 lakh crore projects incl. Semicon 2.0 (₹1,27,500 crore) and Mobile Phone "
        "Manufacturing Scheme (₹62,500 crore) on 15 July 2026", "mpms_fpj"),
   fact("Cabinet approves Mobile Phone Manufacturing Scheme (MPMS)", "mpms_nm")],
  why="₹1,27,500 crore is Semicon 2.0; ₹22,919 crore was the 2025 electronics component scheme; ₹40,000 crore was the "
      "Budget figure for components.",
  current=ca("2026-07-15"))

G(T, SL, "Intermediate",
  "Sarthak-PDS, an umbrella scheme for ration transport, fair price shop dealers' margins and PDS automation, was "
  "approved in May 2026 for April 2026 to March 2031 with what outlay?",
  ["₹25,530 crore", "₹2,530 crore", "₹18,100 crore", "₹5,659 crore"], "*",
  "Sarthak-PDS",
  "The CCEA approved Sarthak-PDS ('Scheme for Assistance in Ration Transport and Handling-Income with Automation in "
  "PDS') with ₹25,530 crore for five years. It merges support for intra-state foodgrain movement and FPS dealers' "
  "margins under the NFSA with the SMART-PDS modernisation scheme.",
  ["Outlay: ₹25,530 crore", "Period: Apr 2026-Mar 2031"],
  [fact("Cabinet clears ₹25,530 crore for Sarthak-PDS for April 2026 to March 2031; merges two schemes",
        "sarthak_tv")],
  why="₹18,100 crore is ECLGS 5.0 and ₹5,659 crore the cotton mission.",
  current=ca("2026-05-27"))

GS(T, SL, "Advanced", "the Regional Connectivity Scheme - Modified UDAN approved in March 2026",
   ["Its total outlay is ₹28,840 crore over ten years, from FY 2026-27 to FY 2035-36.",
    "It plans to develop 100 airports from existing unserved airstrips.",
    "It plans to build 200 helipads."],
   [True, True, True],
   "Modified UDAN",
   "The Cabinet approved Modified UDAN on 25 March 2026 with ₹28,840 crore for ten years. It includes 100 airports "
   "from unserved airstrips, 200 modern helipads, O&M support for about 441 aerodromes, and viability gap funding "
   "for airlines.",
   [fact("Modified UDAN approved 25 March 2026: ₹288.4 billion over FY27-FY36; 100 airports; 200 helipads; VGF",
         "udan_ii")],
   why="All three statements are correct.",
   current=ca("2026-03-25"))

GS(T, SL, "Advanced", "the Emergency Credit Line Guarantee Scheme (ECLGS) 5.0 approved in May 2026",
   ["Its outlay is ₹18,100 crore, for MSMEs and airlines hit by the West Asia conflict.",
    "The guarantee is provided by SIDBI.",
    "MSMEs get 100% guarantee cover on the additional credit."],
   [True, False, True],
   "ECLGS 5.0",
   "ECLGS 5.0 (₹18,100 crore) aims at about ₹2.55 lakh crore of additional credit, ₹5,000 crore of it for airlines. "
   "The guarantee is given by the National Credit Guarantee Trustee Company (NCGTC): 100% for MSMEs and 90% for "
   "non-MSMEs and airlines.",
   [fact("ECLGS 5.0: ₹18,100 crore; MSMEs and airlines hit by West Asia conflict; NCGTC guarantee 100% for MSMEs, 90% "
         "for others", "eclgs_myind")],
   why="Statement 2 is wrong: NCGTC, not SIDBI, gives the guarantee.",
   current=ca("2026-05-05"))

GS(T, CS, "Advanced", "the Atal Bhujal Yojana",
   ["It was launched on 25 December 2019, the birth anniversary of Atal Bihari Vajpayee.",
    "It covers seven states, including Gujarat, Haryana and Uttar Pradesh.",
    "It is supported by the Asian Development Bank."],
   [True, True, False],
   "Atal Bhujal Yojana",
   "The PM launched the community-led groundwater management scheme on 25 December 2019. It covers Gujarat, Haryana, "
   "Karnataka, Madhya Pradesh, Maharashtra, Rajasthan and Uttar Pradesh, and is supported by the World Bank, whose "
   "Board approved it in June 2018.",
   [fact("Atal Bhujal Yojana launched 25 Dec 2019; 7 states listed; World Bank funding", "atal_wiki")],
   why="Statement 3 is wrong: the World Bank, not the ADB, supports it.")

GS(T, CS, "Advanced", "Mission Indradhanush",
   ["Intensified Mission Indradhanush (IMI) was launched by the Prime Minister on 8 October 2017.",
    "It is implemented by the Ministry of Women and Child Development."],
   [True, False],
   "Intensified Mission Indradhanush",
   "IMI was launched by the PM on 8 October 2017 to speed up full immunisation; IMI 2.0 followed for December 2019 to "
   "March 2020. The mission is run by the Ministry of Health and Family Welfare.",
   [fact("Intensified Mission Indradhanush launched 8 October 2017; Ministry of Health and Family Welfare", "mi_wiki")],
   why="Statement 2 is wrong: the Health Ministry implements it.")

GS(T, CS, "Advanced", "the Pradhan Mantri Gram Sadak Yojana (PMGSY)",
   ["It is implemented by the Ministry of Rural Development.",
    "Its original target in hill, tribal and desert areas included habitations of 250 or more people.",
    "Its original target in the plains included habitations of 250 or more people."],
   [True, True, False],
   "PMGSY targets",
   "PMGSY's original targets were habitations of 1,000+ (by 2003) and 500+ (by 2007) in the plains, and 500+ and 250+ "
   "in hill, tribal and desert states. The plains threshold was 500, not 250.",
   [fact("PMGSY: Ministry of Rural Development; targets 1,000+/500+ in plains and 500+/250+ in hill, tribal and desert "
         "states", "pmgsy_wiki")],
   why="Statement 3 is wrong: the lowest plains threshold was 500.")

GS(T, CS, "Advanced", "Beti Bachao Beti Padhao",
   ["It is a tri-ministerial initiative of the Ministries of Women and Child Development, Health and Family Welfare, "
    "and Education.",
    "Its main aim is to reverse the falling child sex ratio and promote girls' education."],
   [True, True],
   "BBBP ministries",
   "BBBP is run jointly by three ministries (WCD, Health and Family Welfare, Education) to address the declining "
   "child sex ratio and advance girls' education and empowerment.",
   [fact("BBBP: joint tri-ministerial initiative of WCD, Health and Family Welfare, Education; aims to reverse falling "
         "child sex ratio", "bbbp_wiki")],
   why="Both statements are correct.")

GS(T, CS, "Advanced", "the Swachh Bharat Mission",
   ["Its urban component is overseen by the Ministry of Housing and Urban Affairs.",
    "Its rural component is under the Department of Drinking Water and Sanitation of the Ministry of Jal Shakti.",
    "It was launched at India Gate, New Delhi."],
   [True, True, False],
   "SBM components",
   "SBM-Urban is under the Ministry of Housing and Urban Affairs and SBM-Gramin under the Department of Drinking Water "
   "and Sanitation, now part of the Ministry of Jal Shakti. The mission was launched at Rajghat.",
   [fact("SBM launched at Rajghat; Gramin under Dept of Drinking Water and Sanitation (Jal Shakti); Urban under MoHUA",
         "sbm_wiki")],
   why="Statement 3 is wrong: the launch was at Rajghat.")

# ====================================================================== Important Appointments (0 / 3 / 1)
T = "Important Appointments"
BF, IB = "Banking and finance heads", "International bodies"

G(T, IB, "Intermediate",
  "Ireland's Finance Minister Paschal Donohoe resigned on 18 November 2025, also giving up the Eurogroup presidency, "
  "to take up which post?",
  ["Managing Director and Chief Knowledge Officer, World Bank", "First Deputy Managing Director, IMF",
   "President, European Investment Bank", "Secretary-General, OECD"], "*",
  "Donohoe to the World Bank",
  "Donohoe resigned as Minister for Finance and Eurogroup president on 18 November 2025 to become Managing Director "
  "and Chief Knowledge Officer of the World Bank, its second most senior post. Simon Harris took over the finance "
  "ministry.",
  ["New post: MD and Chief Knowledge Officer, World Bank", "Resigned: 18 Nov 2025"],
  [fact("Donohoe resigns 18 Nov 2025 to become World Bank Managing Director and Chief Knowledge Officer; Simon Harris "
        "to take finance", "donohoe_rte")],
  why="He did not take any of the other posts.",
  current=ca("2025-11-18"))

G(T, IB, "Intermediate",
  "Kyriakos Pierrakakis, elected President of the Eurogroup in December 2025 for a two-and-a-half-year term, is the "
  "finance minister of which country?",
  ["Greece", "Cyprus", "Belgium", "Portugal"], "*",
  "Eurogroup president",
  "Greek finance minister Kyriakos Pierrakakis was elected Eurogroup president on 11 December 2025, beating "
  "Belgium's Vincent Van Peteghem. He succeeded Paschal Donohoe; Cyprus's Makis Keravnos had been acting president.",
  ["President: Kyriakos Pierrakakis (Greece)", "Elected: 11 Dec 2025", "Term: 2.5 years"],
  [fact("Greece's Pierrakakis elected Eurogroup president over Belgium's Van Peteghem; 2.5-year term; succeeds "
        "Donohoe", "pierr_ief"),
   fact("Greek finance minister elected Eurogroup president on 11 December 2025", "pierr_n4j")],
  why="Cyprus's minister was only acting president; Belgium's candidate lost.",
  current=ca("2025-12-11"))

G(T, IB, "Intermediate",
  "Nobel laureate Michael Kremer became the World Bank's Chief Economist with effect from 1 October 2026. Whom did he "
  "succeed?",
  ["Indermit Gill", "Pierre-Olivier Gourinchas", "Gita Gopinath", "Carmen Reinhart"], "*",
  "World Bank Chief Economist",
  "The World Bank named Michael Kremer (University of Chicago; 2019 Nobel with Banerjee and Duflo) its Chief Economist "
  "from 1 October 2026, succeeding Indermit Gill, who retired in August 2026.",
  ["New Chief Economist: Michael Kremer (from 1 Oct 2026)", "Predecessor: Indermit Gill"],
  [fact("World Bank names Nobel laureate Michael Kremer chief economist from 1 October; predecessor Indermit Gill",
        "kremer_star")],
  why="Gourinchas and Gopinath were IMF economists; Reinhart was an earlier World Bank chief economist.",
  current=ca("2026-09-16"))

GS(T, IB, "Advanced", "Silvana Tenreyro",
   ["She was appointed Chief Economist of the IMF, succeeding Pierre-Olivier Gourinchas.",
    "She was an external member of the Bank of England's Monetary Policy Committee from 2017 to 2023.",
    "She took charge on 1 October 2026."],
   [True, True, False],
   "IMF Chief Economist",
   "The IMF appointed LSE professor Silvana Tenreyro as Chief Economist and head of Research (announced July 2026), "
   "taking charge on 10 August 2026 and succeeding Gourinchas. She sat on the Bank of England's MPC from 2017 to 2023.",
   [fact("IMF appoints Silvana Tenreyro chief economist from 10 August; succeeds Gourinchas; BoE MPC 2017-2023",
         "tenreyro_fpj")],
   why="Statement 3 is wrong: she took charge on 10 August 2026.",
   current=ca("2026-08-10"))

# ====================================================================== Awards and Honours (1 / 10 / 1)
T = "Awards and Honours"
NA, IA = "National awards", "International awards"

G(T, NA, "Basic",
  "Which film won the Best Feature Film award at the 72nd National Film Awards, announced on 18 July 2026?",
  ["Article 370", "Amaran", "Chandu Champion", "Bramayugam"], "*",
  "72nd National Film Awards",
  "The 72nd National Film Awards (for 2024) named Article 370 Best Feature Film; Yami Gautam won Best Actress for it. "
  "Kartik Aaryan (Chandu Champion) and Mammootty (Bramayugam) shared Best Actor; Rajkumar Periasamy (Amaran) was Best "
  "Director.",
  ["Best Feature Film: Article 370", "Announced: 18 July 2026"],
  [fact("72nd National Film Awards: Best Feature Film Article 370; Best Actress Yami Gautam; Best Actor shared; Best "
        "Director Rajkumar Periasamy (Amaran); announced 18 July 2026", "nfa_ol")],
  why="Amaran won Best Director; Chandu Champion and Bramayugam won Best Actor awards.",
  current=ca("2026-07-18"))

G(T, IA, "Intermediate",
  "Which film won the Golden Lion at the 83rd Venice International Film Festival in September 2026?",
  ["Woman Unknown", "Possible Love", "Wild Horse Nine", "Dau"], "*",
  "Venice 2026",
  "May el-Toukhy's Woman Unknown won the Golden Lion on 12 September 2026; jury president was Maggie Gyllenhaal. Lee "
  "Chang-dong's Possible Love won the Grand Jury Prize and John Malkovich won Best Actor for Wild Horse Nine.",
  ["Golden Lion: Woman Unknown (May el-Toukhy)", "Closing: 12 Sep 2026"],
  [fact("Venice 2026: Golden Lion to Woman Unknown by May el-Toukhy; jury president Maggie Gyllenhaal; Grand Jury "
        "Prize Possible Love", "venice_eu")],
  why="The other films won other Venice awards.",
  current=ca("2026-09-12"))

G(T, IA, "Intermediate",
  "Romanian director Cristian Mungiu won the Palme d'Or at the 79th Cannes Film Festival in May 2026 for which film?",
  ["Fjord", "Minotaur", "4 Months, 3 Weeks and 2 Days", "Sentimental Value"], "*",
  "Cannes 2026",
  "Fjord won the Palme d'Or on 23 May 2026 (jury president Park Chan-wook). It is Mungiu's second, after 4 Months, 3 "
  "Weeks and 2 Days in 2007. Andrey Zvyagintsev's Minotaur won the Grand Prix.",
  ["Palme d'Or 2026: Fjord (Cristian Mungiu)", "Mungiu's earlier Palme: 2007"],
  [fact("Cannes 2026: Fjord by Cristian Mungiu wins Palme d'Or; jury Park Chan-wook; Grand Prix Minotaur; 23 May "
        "2026", "cannes_eu"),
   fact("Cristian Mungiu wins his second Palme d'Or for Fjord", "cannes_ol")],
  why="Minotaur won the Grand Prix; 4 Months... won in 2007; Sentimental Value is a 2025 film.",
  current=ca("2026-05-23"))

G(T, IA, "Intermediate",
  "İlker Çatak's 'Yellow Letters' won which top award in February 2026?",
  ["Golden Bear, Berlin International Film Festival", "Golden Lion, Venice Film Festival",
   "Palme d'Or, Cannes Film Festival", "Golden Leopard, Locarno Film Festival"], "*",
  "Berlinale 2026",
  "Yellow Letters, about a Turkish director and his actor wife barred from working for their views, won the Golden "
  "Bear at the 2026 Berlinale (ceremony 21 February); jury president was Wim Wenders.",
  ["Golden Bear 2026: Yellow Letters (İlker Çatak)", "Jury president: Wim Wenders"],
  [fact("Yellow Letters by Ilker Catak wins Golden Bear at 2026 Berlinale; jury president Wim Wenders", "berlin_eu")],
  why="Venice, Cannes and Locarno gave their top prizes to other films.",
  current=ca("2026-02-21"))

G(T, NA, "Intermediate",
  "The Dadasaheb Phalke Award for 2024, announced on 16 September 2026, went to which veteran actor?",
  ["Anant Nag", "Mohanlal", "Mithun Chakraborty", "Mammootty"], "*",
  "Dadasaheb Phalke Award",
  "The Ministry of Information and Broadcasting announced the Phalke Award for 2024 for Kannada actor Anant Nag, to "
  "be presented at the 72nd National Film Awards in Kevadia, Gujarat. Mohanlal (2023) and Mithun Chakraborty (2022) "
  "were earlier recipients.",
  ["Phalke Award 2024: Anant Nag", "Announced: 16 Sep 2026"],
  [fact("Veteran Kannada actor Anant Nag to be conferred Dadasaheb Phalke Award for 2024; announced by I&B Ministry",
        "phalke_air")],
  why="Mohanlal and Mithun Chakraborty received it for 2023 and 2022; Mammootty shared Best Actor in 2026.",
  current=ca("2026-09-16"))

G(T, IA, "Intermediate",
  "Charles H. Bennett and Gilles Brassard received the 2025 ACM A.M. Turing Award, announced in March 2026, for "
  "foundational work in which field?",
  ["Quantum information science", "Deep learning", "Public-key cryptography based on elliptic curves",
   "Distributed databases"], "*",
  "Turing Award 2025",
  "The ACM honoured Bennett (IBM Research) and Brassard (Université de Montréal) for quantum information science, "
  "including the BB84 quantum cryptography protocol (1984) and quantum teleportation (1993). The prize is USD 1 "
  "million, funded by Google; announced 18 March 2026.",
  ["Winners: Bennett and Brassard", "Field: quantum information science (BB84, teleportation)"],
  [fact("2025 Turing Award to Bennett and Brassard for quantum information science; USD 1 million; Google; announced "
        "18 March 2026", "turing_eur")],
  why="Their work is in quantum information, not the other fields.",
  current=ca("2026-03-18"))

G(T, IA, "Intermediate",
  "Who was named Laureus World Sportsman of the Year at the Laureus World Sports Awards held in April 2026?",
  ["Carlos Alcaraz", "Jannik Sinner", "Lando Norris", "Lamine Yamal"], "*",
  "Laureus 2026",
  "At the 2026 Laureus Awards in Madrid (20 April 2026), Carlos Alcaraz was Sportsman of the Year and Aryna Sabalenka "
  "Sportswoman of the Year; PSG was Team of the Year, Lando Norris Breakthrough and Lamine Yamal Young Sportsperson.",
  ["Sportsman: Carlos Alcaraz", "Sportswoman: Aryna Sabalenka", "Team: PSG"],
  [fact("Laureus 2026: Sportsman Alcaraz, Sportswoman Sabalenka, Team PSG, Breakthrough Norris, Young Yamal",
        "laureus_ol"),
   fact("Alcaraz, Sabalenka headline Laureus 2026 awards in Madrid", "laureus_dt")],
  why="Norris and Yamal won other Laureus categories; Sinner did not win this award.",
  current=ca("2026-04-20"))

G(T, IA, "Intermediate",
  "Cambridge palaeontologist Simon Conway Morris, known for work on convergent evolution and the Cambrian explosion, "
  "received which prize in 2026?",
  ["Templeton Prize", "Crafoord Prize", "Kyoto Prize", "Wolf Prize"], "*",
  "Templeton Prize 2026",
  "Simon Conway Morris received the 2026 Templeton Prize (announced April 2026), valued at about USD 1.4 million, for "
  "work on evolutionary biology linking science and big questions of purpose.",
  ["Templeton Prize 2026: Simon Conway Morris"],
  [fact("Professor Simon Conway Morris, paleontologist, receives 2026 Templeton Prize", "templeton_trt"),
   fact("Cambridge professor awarded $1.4m Templeton Prize", "templeton_var")],
  why="He was not a 2026 laureate of the Crafoord, Kyoto or Wolf prizes.",
  current=ca("2026-04-21"))

G(T, NA, "Intermediate",
  "Bengali writer Ramkumar Mukhopadhyay was selected for the Saraswati Samman 2025 for which novel?",
  ["Hara Parbati Katha", "Roudra Sathwikam", "Crimson Spring", "Teesta Parer Brittanto"], "*",
  "Saraswati Samman 2025",
  "The K. K. Birla Foundation selected Ramkumar Mukhopadhyay's Bengali novel Hara Parbati Katha for the 2025 Saraswati "
  "Samman (₹15 lakh, citation and plaque), reported on 25 March 2026.",
  ["Saraswati Samman 2025: Ramkumar Mukhopadhyay, Hara Parbati Katha", "Given by: K. K. Birla Foundation"],
  [fact("Ramkumar Mukhopadhyay selected for Saraswati Samman 2025 for Bengali novel Hara Parbati Katha; ₹15 lakh; "
        "K. K. Birla Foundation", "saraswati_air")],
  why="Roudra Sathwikam won an earlier Saraswati Samman; Crimson Spring won the Sahitya Akademi Award (English); "
      "Teesta Parer Brittanto is an older Bengali novel.",
  current=ca("2026-03-25"))

G(T, IA, "Intermediate",
  "Japanese chemist Tsutomu Miyasaka, a 2026 Kyoto Prize laureate in Advanced Technology, is known for creating which "
  "technology?",
  ["Perovskite solar cells", "Lithium-ion batteries", "Blue light-emitting diodes", "Quantum dots"], "*",
  "Kyoto Prize 2026",
  "The 2026 Kyoto Prize (announced 19 June 2026) went to Tsutomu Miyasaka (Advanced Technology) for perovskite solar "
  "cells, Farooq Azam (Basic Sciences) for the marine 'microbial loop', and Laurie Anderson (Arts and Philosophy).",
  ["Miyasaka: perovskite solar cells", "Azam: microbial loop", "Anderson: multimedia art"],
  [fact("2026 Kyoto Prize: Miyasaka for perovskite solar cells; Azam; Laurie Anderson", "kyoto_kp")],
  why="Lithium-ion batteries, blue LEDs and quantum dots are linked to other scientists.",
  current=ca("2026-06-19"))

G(T, IA, "Intermediate",
  "Who won the women's Ballon d'Or 2026, her third, at the ceremony held in London on 26 October 2026?",
  ["Alexia Putellas", "Aitana Bonmatí", "Vicky López", "Cata Coll"], "*",
  "Ballon d'Or 2026",
  "Alexia Putellas won her third women's Ballon d'Or at the 2026 ceremony, the first held outside Paris (London). "
  "Vicky López won the women's Kopa Trophy and Cata Coll the women's Yashin Trophy.",
  ["Women's Ballon d'Or 2026: Alexia Putellas (third)"],
  [fact("Ballon d'Or 2026: women's award to Alexia Putellas, her third; Kopa Vicky Lopez; Yashin Cata Coll",
        "ballon_bein")],
  why="López and Coll won the Kopa and Yashin trophies; Bonmatí did not win in 2026.",
  current=ca("2026-10-26"))

GS(T, IA, "Advanced", "the Right Livelihood Award 2026",
   ["AI researcher Timnit Gebru is one of the laureates.",
    "The Georgian Young Lawyers' Association is the first laureate from Georgia.",
    "The laureates were announced in Oslo."],
   [True, True, False],
   "Right Livelihood Award 2026",
   "Announced in Stockholm on 30 September 2026, the four laureates were Pakistani lawyer Jalila Haider, Timnit Gebru, "
   "the Rural Women's Assembly (Southern Africa) and the Georgian Young Lawyers' Association, the first laureate from "
   "Georgia.",
   [fact("Right Livelihood 2026 announced 30 Sep 2026 in Stockholm: Jalila Haider, Timnit Gebru, Rural Women's "
         "Assembly, Georgian Young Lawyers' Association (first from Georgia)", "rla_bol"),
    fact("GYLA first Right Livelihood winner from Georgia", "rla_cd")],
   why="Statement 3 is wrong: the announcement was made in Stockholm.",
   current=ca("2026-09-30"))

# ====================================================================== Sports (6 / 1 / 8)
T = "Sports"
TW, VR = "Tournaments and winners", "Venues and records"

G(T, TW, "Basic",
  "Which team won the ICC Women's T20 World Cup 2026, beating hosts England by seven wickets in the final at Lord's?",
  ["Australia", "India", "South Africa", "West Indies"], "*",
  "Women's T20 World Cup 2026",
  "Australia beat England by seven wickets with 17 balls to spare at Lord's on 5 July 2026, winning their seventh "
  "Women's T20 World Cup title.",
  ["Winner: Australia (7th title)", "Final: v England at Lord's, 5 July 2026"],
  [fact("Australia beat England by 7 wickets at Lord's to win seventh Women's T20 World Cup title", "wt20_ol")],
  why="India, South Africa and West Indies did not win the 2026 final.",
  current=ca("2026-07-05"))

G(T, TW, "Basic",
  "Who won the 2025 Formula One World Drivers' Championship, clinched at the Abu Dhabi Grand Prix on 7 December 2025?",
  ["Lando Norris", "Max Verstappen", "Oscar Piastri", "Lewis Hamilton"], "*",
  "F1 2025",
  "McLaren's Lando Norris finished third in Abu Dhabi on 7 December 2025 to win his first title by two points over "
  "race winner Max Verstappen; Oscar Piastri was second in the race.",
  ["Champion: Lando Norris (McLaren)", "Margin: 2 points over Verstappen"],
  [fact("Norris secures maiden F1 title in Abu Dhabi, two points ahead of Verstappen; race on 7 Dec 2025", "f1_f1")],
  why="Verstappen won the race but not the title; Piastri was third in the standings.",
  current=ca("2025-12-07"))

G(T, TW, "Basic",
  "Which team won its first-ever Ranji Trophy title in the 2025-26 season, beating Karnataka on first-innings lead in "
  "the final at Hubballi?",
  ["Jammu and Kashmir", "Vidarbha", "Kerala", "Madhya Pradesh"], "*",
  "Ranji Trophy 2025-26",
  "Jammu and Kashmir, led by Paras Dogra, won their maiden Ranji Trophy when the final against Karnataka at Hubballi "
  "ended in a draw on 28 February 2026; J&K's 584 gave them a 291-run first-innings lead.",
  ["Champion: Jammu and Kashmir (first title)", "Final: v Karnataka, Hubballi, drawn; won on first-innings lead"],
  [fact("J&K win maiden Ranji Trophy; final v Karnataka at Hubballi drawn; 291-run first-innings lead; 28 Feb 2026",
        "ranji_ol"),
   fact("2025-26 Ranji Trophy: Jammu and Kashmir champions, Karnataka runners-up", "ranji_wiki")],
  why="Vidarbha, Kerala and Madhya Pradesh did not win the 2025-26 title.",
  current=ca("2026-02-28"))

G(T, TW, "Basic",
  "Which team won the Women's Premier League 2026, beating Delhi Capitals by six wickets in the final at Vadodara on "
  "5 February 2026?",
  ["Royal Challengers Bengaluru", "Mumbai Indians", "Gujarat Giants", "UP Warriorz"], "*",
  "WPL 2026",
  "Royal Challengers Bengaluru beat Delhi Capitals by six wickets at the BCA Stadium, Vadodara, on 5 February 2026 for "
  "their second WPL title; Smriti Mandhana was Player of the Match.",
  ["Winner: RCB (second title)", "Final: v Delhi Capitals, Vadodara"],
  [fact("WPL 2026 final: RCB beat Delhi Capitals by 6 wickets at Vadodara on 5 Feb 2026; second title; Mandhana POTM",
        "wpl_wiki")],
  why="The other teams did not reach or win the final.",
  current=ca("2026-02-05"))

G(T, TW, "Basic",
  "Which country won the Davis Cup 2025, beating Spain 2-0 in the final in Bologna on 23 November 2025 for a third "
  "straight title?",
  ["Italy", "Germany", "Australia", "Netherlands"], "*",
  "Davis Cup 2025",
  "Italy beat Spain 2-0 in Bologna (Berrettini and Cobolli won their singles) for a third straight title and fourth "
  "overall (1976, 2023, 2024, 2025).",
  ["Winner: Italy (third in a row)", "Final: v Spain, Bologna, 23 Nov 2025"],
  [fact("Italy beat Spain 2-0 in Bologna on 23 Nov 2025 for third straight Davis Cup; fourth overall", "davis_star")],
  why="The other countries did not win the 2025 final.",
  current=ca("2025-11-23"))

G(T, TW, "Basic",
  "Which country won the Thomas Cup 2026, beating France 3-1 in the final at Horsens, Denmark, on 3 May 2026?",
  ["China", "Indonesia", "Denmark", "India"], "*",
  "Thomas Cup 2026",
  "China retained the Thomas Cup by beating first-time finalists France 3-1 at Horsens on 3 May 2026, their 12th title. "
  "South Korea won the Uber Cup by beating China 3-1.",
  ["Thomas Cup: China beat France 3-1", "Uber Cup: South Korea beat China 3-1"],
  [fact("China retains Thomas Cup, beating France 3-1 at Horsens on 3 May 2026; South Korea wins Uber Cup",
        "thomas_cgtn")],
  why="Indonesia, Denmark and India did not win the 2026 Thomas Cup.",
  current=ca("2026-05-03"))

G(T, TW, "Intermediate",
  "Who won the men's singles title at the BWF World Championships 2026, held at the Indira Gandhi Arena, New Delhi, in "
  "August 2026?",
  ["Alex Lanier", "Kodai Naraoka", "Shi Yu Qi", "Lakshya Sen"], "*",
  "BWF World Championships 2026",
  "At the World Championships in New Delhi (17-23 August 2026), France's Alex Lanier beat Japan's Kodai Naraoka in the "
  "men's singles final. An Se-young won the women's singles; India's only medal was a women's doubles bronze for "
  "Treesa Jolly and Gayatri Gopichand.",
  ["Men's singles: Alex Lanier (France)", "Runner-up: Kodai Naraoka (Japan)"],
  [fact("2026 BWF World Championships, New Delhi, 17-23 Aug: men's singles Alex Lanier beat Kodai Naraoka; India one "
        "bronze (Treesa-Gayatri)", "bwf_wiki")],
  why="Naraoka was runner-up; Shi Yu Qi was the 2025 champion; Lakshya Sen did not win a medal.",
  current=ca("2026-08-23"))

GS(T, TW, "Advanced", "the men's singles final of the French Open 2026",
   ["Alexander Zverev beat Flavio Cobolli in the final.",
    "It was Zverev's first Grand Slam singles title.",
    "The final was decided in straight sets."],
   [True, True, False],
   "French Open 2026",
   "Second seed Alexander Zverev beat Italy's Flavio Cobolli 6-1, 4-6, 6-4, 6-7(5), 6-1 on 7 June 2026 for his first "
   "major title after three lost finals.",
   [fact("Zverev beat Cobolli 6-1, 4-6, 6-4, 6-7(5), 6-1 on 7 June 2026 for first Grand Slam title", "fo_cgtn")],
   why="Statement 3 is wrong: the final went to five sets.",
   current=ca("2026-06-07"))

GS(T, TW, "Advanced", "the women's singles at the US Open 2026",
   ["Elena Rybakina beat Aryna Sabalenka in the final.",
    "It was Rybakina's first Grand Slam singles title.",
    "Rybakina had also beaten Sabalenka in the Australian Open 2026 final."],
   [True, False, True],
   "US Open 2026",
   "Rybakina (Kazakhstan) beat Sabalenka 6-4, 5-7, 6-2 on 12 September 2026 for her first US Open and third Grand Slam "
   "title; she also beat Sabalenka in the 2026 Australian Open final and rose to world No. 1.",
   [fact("Rybakina tops Sabalenka 6-4, 5-7, 6-2 on 12 Sep 2026; third Grand Slam title; also won 2026 Australian Open "
         "beating Sabalenka", "uso_katv")],
   why="Statement 2 is wrong: it was her third Grand Slam title.",
   current=ca("2026-09-12"))

GS(T, VR, "Advanced", "the Men's FIH Hockey World Cup 2026",
   ["Germany beat Spain 1-0 in the final.",
    "The final was played in Wavre, Belgium.",
    "Germany thereby won the title for the fourth time."],
   [True, True, True],
   "Men's Hockey World Cup 2026",
   "Defending champions Germany beat Spain 1-0 at the Belfius Hockey Arena, Wavre, on 30 August 2026 (Michel "
   "Struthoff scoring) for a fourth title, equalling Pakistan's record. Argentina took bronze.",
   [fact("Germany retain Men's Hockey World Cup with 1-0 win over Spain at Wavre; fourth title", "hwc_air"),
    fact("Germany vs Spain, FIH Men's World Cup 2026 final report, Wavre", "hwc_ol")],
   why="All three statements are correct.",
   current=ca("2026-08-30"))

GS(T, TW, "Advanced", "the Women's FIH Hockey World Cup 2026",
   ["Argentina beat the Netherlands in a penalty shoot-out in the final.",
    "It was Argentina's first Women's World Cup title.",
    "Belgium won the bronze medal by beating Australia."],
   [True, False, True],
   "Women's Hockey World Cup 2026",
   "Argentina beat co-hosts and defending champions the Netherlands on penalties in the final at Amstelveen (29 August "
   "2026) for their third title. Belgium beat Australia 1-0 for bronze.",
   [fact("Women's FIH Hockey World Cup 2026: Argentina won (third title) on shoot-out v Netherlands; bronze Belgium "
         "beat Australia 1-0", "hwcw_wiki"),
    fact("Argentina beat Netherlands in shootout to clinch Women's Hockey World Cup", "hwcw_nk")],
   why="Statement 2 is wrong: it was Argentina's third title.",
   current=ca("2026-08-29"))

GS(T, VR, "Advanced", "the UEFA Champions League 2025-26 final",
   ["Paris Saint-Germain beat Arsenal on penalties.",
    "It was played at the Puskás Aréna in Budapest.",
    "It was Paris Saint-Germain's first Champions League title."],
   [True, True, False],
   "UCL final 2026",
   "PSG came from a goal down to draw with Arsenal and won the shoot-out 4-3 in Budapest on 30 May 2026, retaining the "
   "title they had won in 2025 against Inter.",
   [fact("PSG beat Arsenal 4-3 on penalties in Budapest to retain the Champions League", "ucl_fs"),
    fact("2026 UEFA Champions League Final at Puskas Arena, Budapest", "ucl_fandom")],
   why="Statement 3 is wrong: PSG were defending the title won in 2025.",
   current=ca("2026-05-30"))

GS(T, TW, "Advanced", "the FIH Men's Junior Hockey World Cup 2025 held in Tamil Nadu",
   ["India finished as runners-up.",
    "Germany beat Spain in a shoot-out in the final at Chennai.",
    "It was Germany's eighth junior world title."],
   [False, True, True],
   "Junior Hockey World Cup 2025",
   "Germany beat first-time finalists Spain 3-2 on penalties after a 1-1 draw at Chennai on 10 December 2025 for a "
   "record eighth title. India beat Argentina for bronze.",
   [fact("Germany win record-extending 8th Junior World Cup, beating Spain in shoot-out at Chennai on 10 Dec 2025; "
         "India bronze", "jhwc_trib")],
   why="Statement 1 is wrong: India won bronze.",
   current=ca("2025-12-10"))

GS(T, VR, "Advanced", "the 46th Chess Olympiad held in September 2026",
   ["It was held in Samarkand, and the host Uzbekistan won the Open section.",
    "India won gold in the Women's section."],
   [True, False],
   "Chess Olympiad 2026",
   "Uzbekistan won the Open section at Samarkand, with India silver and Germany bronze. China won the Women's section, "
   "ahead of Kazakhstan and India (bronze).",
   [fact("46th Olympiad Samarkand: Open Uzbekistan, India, Germany; Women China, Kazakhstan, India", "chess_fide")],
   why="Statement 2 is wrong: India won bronze in the Women's section.",
   current=ca("2026-09-27"))

GS(T, TW, "Advanced", "the 135th Durand Cup final in August 2026",
   ["East Bengal beat Mohun Bagan Super Giant 4-1.",
    "The win drew East Bengal level with Mohun Bagan at 17 Durand Cup titles each."],
   [True, True],
   "Durand Cup 2026",
   "East Bengal beat Mohun Bagan Super Giant 4-1 in Kolkata on 23 August 2026, Edmund Lalrindika scoring a hat-trick, "
   "for a 17th title that drew them level with Mohun Bagan.",
   [fact("135th Durand Cup final: East Bengal beat Mohun Bagan SG 4-1 on 23 Aug 2026; 17th title, level with Mohun "
         "Bagan", "durand_ae")],
   why="Both statements are correct.",
   current=ca("2026-08-23"))

# ====================================================================== Summits and Conferences (1 / 0 / 0)
T = "Summits and Conferences"
G(T, "G20, BRICS, SCO and others", "Basic",
  "The 32nd APEC Economic Leaders' Meeting, which adopted the Gyeongju Declaration on 1 November 2025, was hosted by "
  "which country?",
  ["South Korea", "Japan", "China", "Peru"], "*",
  "APEC 2025",
  "APEC leaders met at Gyeongju, South Korea, and adopted the Gyeongju Declaration on 1 November 2025, also endorsing "
  "the APEC AI Initiative.",
  ["Host: South Korea (Gyeongju)", "Outcome: Gyeongju Declaration, 1 Nov 2025"],
  [fact("APEC leaders adopt Gyeongju Declaration at 32nd leaders' meeting in Gyeongju, South Korea, 1 Nov 2025",
        "apec_ptv")],
  why="Peru hosted APEC 2024; China hosts in 2026; Japan did not host in 2025.",
  current=ca("2025-11-01"))

# ====================================================================== Important Days (0 / 5 / 0)
T = "Important Days"
DT = "Days and themes"

G(T, DT, "Intermediate",
  "What was the UN theme for International Women's Day 2026 (8 March)?",
  ["Rights. Justice. Action. For ALL Women and Girls.", "Accelerate Action", "Invest in women: Accelerate progress",
   "DigitALL: Innovation and technology for gender equality"], "*",
  "International Women's Day 2026",
  "The UN theme for 2026 was 'Rights. Justice. Action. For ALL Women and Girls.', focusing on closing legal gaps; the "
  "separate campaign theme was 'Give To Gain'.",
  ["IWD 2026 UN theme: Rights. Justice. Action. For ALL Women and Girls."],
  [fact("UN theme for IWD 2026: Rights. Justice. Action. For ALL Women and Girls.; campaign Give To Gain", "iwd_rep")],
  why="The other options are themes of earlier years.",
  current=ca("2026-03-08"))

G(T, DT, "Intermediate",
  "What was the theme of World Wildlife Day 2026 (3 March)?",
  ["Medicinal and Aromatic Plants: Conserving Health, Heritage and Livelihoods",
   "Wildlife Conservation Finance: Investing in People and Planet", "Connecting People and Planet",
   "Forests and Livelihoods: Sustaining People and Planet"], "*",
  "World Wildlife Day 2026",
  "World Wildlife Day, marking the signing of CITES on 3 March 1973, had the 2026 theme 'Medicinal and Aromatic "
  "Plants: Conserving Health, Heritage and Livelihoods'. The CITES Secretariat facilitates it.",
  ["Theme 2026: Medicinal and Aromatic Plants", "3 March: CITES signed in 1973"],
  [fact("World Wildlife Day 2026 theme: Medicinal and Aromatic Plants: Conserving Health, Heritage and Livelihoods; "
        "3 March marks CITES signing", "wwd_gen")],
  why="The other options are themes of earlier years.",
  current=ca("2026-03-03"))

G(T, DT, "Intermediate",
  "What was the theme of World Tuberculosis Day 2026 (24 March)?",
  ["Yes! We Can End TB: Led by countries, powered by people", "Yes! We can end TB: Commit, Invest, Deliver",
   "Invest to End TB. Save Lives.", "The Clock is Ticking"], "*",
  "World TB Day 2026",
  "WHO's Director-General cited the 2026 theme 'Yes! We Can End TB: Led by countries, powered by people'. 24 March "
  "marks Robert Koch's 1882 discovery of the TB bacterium.",
  ["Theme 2026: Yes! We Can End TB: Led by countries, powered by people"],
  [fact("World TB Day 2026 theme: Yes! We Can End TB: Led by countries, powered by people", "tb_who")],
  why="The other options are themes of earlier years.",
  current=ca("2026-03-24"))

G(T, DT, "Intermediate",
  "What was the theme of the International Day for Biological Diversity 2026 (22 May)?",
  ["Acting locally for global impact", "Harmony with nature and sustainable development", "Be part of the Plan",
   "From Agreement to Action: Build Back Biodiversity"], "*",
  "Biodiversity Day 2026",
  "The CBD Secretariat set 'Acting locally for global impact' as the 2026 theme, linking local action to the "
  "Kunming-Montreal Global Biodiversity Framework.",
  ["Theme 2026: Acting locally for global impact"],
  [fact("International Day for Biological Diversity 2026 theme: Acting locally for global impact; 22 May", "idb_cbd")],
  why="The other options are themes of earlier years.",
  current=ca("2026-05-22"))

G(T, DT, "Intermediate",
  "World Food Day 2026 (16 October), which marks the founding of FAO in 1945, was observed under which theme?",
  ["Innovate today. Nourish tomorrow.", "Hand in hand for better foods and a better future",
   "Right to foods for a better life and a better future", "Water is life, water is food. Leave no one behind"], "*",
  "World Food Day 2026",
  "FAO events for 16 October 2026 ran under 'Innovate today. Nourish tomorrow.' The day marks FAO's founding on "
  "16 October 1945.",
  ["Theme 2026: Innovate today. Nourish tomorrow."],
  [fact("World Food Day 2026 on 16 October; events titled 'Innovate Today, Nourish Tomorrow'", "wfd_fao")],
  why="The other options are themes of earlier years.",
  current=ca("2026-10-16"))

# ====================================================================== Books and Authors (4 / 1 / 4)
T = "Books and Authors"
RB = "Recent books"

G(T, RB, "Basic",
  "'The Curious and the Classified: Unearthing Military Myths and Mysteries', published by Rupa in 2026, was written "
  "by which former Army Chief?",
  ["General Manoj Naravane", "General Bipin Rawat", "General V. K. Singh", "General Upendra Dwivedi"], "*",
  "Naravane's new book",
  "General Manoj Naravane (retd) wrote this non-fiction book of lesser-known stories from the Army, Navy and Air Force, "
  "published by Rupa in April 2026. His memoir 'Four Stars of Destiny' remained unpublished.",
  ["Author: Gen. Manoj Naravane", "Publisher: Rupa"],
  [fact("The Curious and the Classified by General Manoj Naravane (Retired), Rupa, non-fiction", "naravane_rupa"),
   fact("Gen Naravane pens new book amid row over unpublished memoir (April 2026)", "naravane_trib")],
  why="The other generals did not write this book.",
  current=ca("2026-04-22"))

G(T, RB, "Basic",
  "Who wrote 'Ghost-Eye', a 2026 novel about a three-year-old girl in Calcutta, reincarnation and the Sundarbans?",
  ["Amitav Ghosh", "Kiran Desai", "Arundhati Roy", "Vikram Seth"], "*",
  "Ghost-Eye",
  "Jnanpith winner Amitav Ghosh's novel Ghost-Eye (2026) follows Varsha Gupta, a girl from a vegetarian Marwari family "
  "who insists on eating fish, and explores past lives, food, climate and folklore.",
  ["Author: Amitav Ghosh", "Novel: Ghost-Eye (2026)"],
  [fact("Amitav Ghosh's new novel Ghost-Eye; Calcutta and Sundarbans; reincarnation; published Jan 2026 article",
        "ghosh_fpj")],
  why="The other authors did not write Ghost-Eye.",
  current=ca("2026-01-17"))

G(T, RB, "Basic",
  "'The Eleventh Hour', a collection of five stories set in India, England and America and published in November "
  "2025, was written by whom?",
  ["Salman Rushdie", "Amitav Ghosh", "Jhumpa Lahiri", "Kazuo Ishiguro"], "*",
  "The Eleventh Hour",
  "Salman Rushdie's The Eleventh Hour: A Quintet of Stories was published on 4 November 2025; its stories move "
  "between Chennai, Bombay, an English college and America.",
  ["Author: Salman Rushdie", "Five stories"],
  [fact("The Eleventh Hour by Salman Rushdie; five stories set in India, England and America", "rushdie_peng"),
   fact("The Eleventh Hour: A Quintet of Stories, published November 2025", "rushdie_br")],
  why="The other writers did not write this book.",
  current=ca("2025-11-04"))

G(T, RB, "Basic",
  "'There Is No Place for Us: Working and Homeless in America', winner of the Pulitzer Prize for General Nonfiction "
  "2026, was written by whom?",
  ["Brian Goldstone", "Daniel Kraus", "Jill Lepore", "Omar El Akkad"], "*",
  "Pulitzer General Nonfiction 2026",
  "Brian Goldstone's book, following working families in Atlanta, won the 2026 Pulitzer for General Nonfiction "
  "(announced 4 May 2026).",
  ["Author: Brian Goldstone", "Prize: Pulitzer, General Nonfiction 2026"],
  [fact("2026 Pulitzer General Nonfiction: There Is No Place for Us by Brian Goldstone; announced 4 May 2026",
        "pulitzer_lit")],
  why="Kraus won Fiction, Lepore won History, and El Akkad won a 2025 National Book Award.",
  current=ca("2026-05-04"))

G(T, RB, "Intermediate",
  "Rabih Alameddine won the National Book Award for Fiction 2025 (US) for which novel?",
  ["The True True Story of Raja the Gullible (and His Mother)", "An Unnecessary Woman", "We Are Green and Trembling",
   "One Day, Everyone Will Have Always Been Against This"], "*",
  "National Book Award 2025",
  "At the 19 November 2025 ceremony Alameddine won Fiction for The True True Story of Raja the Gullible (and His "
  "Mother). Omar El Akkad won Nonfiction and Gabriela Cabezón Cámara won Translated Literature.",
  ["Fiction 2025: Rabih Alameddine"],
  [fact("2025 National Book Awards: Fiction Rabih Alameddine; Nonfiction Omar El Akkad; Translated Gabriela Cabezon "
        "Camara; 19 Nov 2025", "nba_kunc")],
  why="An Unnecessary Woman is his earlier novel; the other two won other categories.",
  current=ca("2025-11-19"))

GS(T, RB, "Advanced", "the Kamaladevi Chattopadhyay NIF Book Prize 2025",
   ["It was won by Aparajith Ramnath for a biography of engineer M. Visvesvaraya.",
    "The prize carries ₹15 lakh, a trophy and a citation.",
    "It was presented at the Jaipur Literature Festival."],
   [True, True, False],
   "NIF Book Prize 2025",
   "The New India Foundation named Aparajith Ramnath's 'Engineering a Nation: The Life and Career of "
   "M. Visvesvaraya' the winner on 17 November 2025; the prize was presented on 6 December 2025 at the 14th Bangalore "
   "Literature Festival.",
   [fact("NIF Book Prize 2025: Aparajith Ramnath, Engineering a Nation (Visvesvaraya); ₹15 lakh, trophy, citation; "
         "presented at 14th Bangalore Literature Festival", "nif_site")],
   why="Statement 3 is wrong: it was presented at the Bangalore Literature Festival.",
   current=ca("2025-11-17"))

GS(T, RB, "Advanced", "the Baillie Gifford Prize for Non-Fiction 2025",
   ["It was won by Helen Garner for 'How to End a Story: Collected Diaries'.",
    "It was the first diary collection to win the prize.",
    "The winner receives £50,000."],
   [True, True, True],
   "Baillie Gifford Prize 2025",
   "Australian writer Helen Garner won on 4 November 2025 with her collected diaries, the first diary collection to "
   "win; the prize is £50,000.",
   [fact("Helen Garner wins 2025 Baillie Gifford Prize for How to End a Story; first diary collection; £50,000",
         "bg_lit")],
   why="All three statements are correct.",
   current=ca("2025-11-04"))

GS(T, RB, "Advanced", "the Booker Prize 2026 shortlist announced on 22 September 2026",
   ["Douglas Stuart's 'John of John' is on the shortlist.",
    "Elizabeth Strout is shortlisted for 'Lucy by the Sea'.",
    "The winner is to be announced on 9 November 2026."],
   [True, False, True],
   "Booker Prize 2026 shortlist",
   "The six shortlisted books are The End of Everything (M. John Harrison), The Disappearers (Marlon James), Black Bag "
   "(Luke Kennard), May We Feed the King (Rebecca Perry), The Things We Never Say (Elizabeth Strout) and John of John "
   "(Douglas Stuart). The winner is due on 9 November 2026.",
   [fact("Booker 2026 shortlist announced 22 Sep 2026: six titles incl. John of John (Stuart) and The Things We Never "
         "Say (Strout); winner on 9 Nov", "booker_lit"),
    fact("2026 Booker Prize shortlist", "booker_br")],
   why="Statement 2 is wrong: Strout is shortlisted for 'The Things We Never Say'.",
   current=ca("2026-09-22"))

GS(T, RB, "Advanced", "the Pulitzer Prizes 2026 in books",
   ["Jill Lepore won the History prize for 'We the People: A History of the U.S. Constitution'.",
    "Yiyun Li won the Memoir prize for 'Things in Nature Merely Grow'.",
    "Amanda Vaill won the Fiction prize."],
   [True, True, False],
   "Pulitzer 2026 books",
   "The 2026 book winners (4 May 2026) included Daniel Kraus (Fiction, Angel Down), Brian Goldstone (General "
   "Nonfiction), Jill Lepore (History), Amanda Vaill (Biography, Pride and Pleasure), Yiyun Li (Memoir) and Juliana "
   "Spahr (Poetry).",
   [fact("2026 Pulitzers: History Jill Lepore; Biography Amanda Vaill; Memoir Yiyun Li; Fiction Daniel Kraus",
         "pulitzer_lit")],
   why="Statement 3 is wrong: Vaill won Biography; Daniel Kraus won Fiction.",
   current=ca("2026-05-04"))

# ====================================================================== National and International Organizations (2/3/0)
T = "National and International Organizations"
HH = "Headquarters and heads"

G(T, HH, "Basic",
  "Where is the headquarters of the Universal Postal Union (UPU), set up by the Treaty of Bern in 1874?",
  ["Bern", "Geneva", "Vienna", "Paris"], "*",
  "Universal Postal Union",
  "The UPU, founded as the General Postal Union in 1874 by the Treaty of Bern, is headquartered in Bern, Switzerland. "
  "It has 192 members.",
  ["HQ: Bern, Switzerland", "Founded: 1874"],
  [fact("UPU headquartered in Bern; founded 1874 by Treaty of Bern; 192 members", "upu_wiki")],
  why="Geneva, Vienna and Paris host other UN bodies.")

G(T, HH, "Basic",
  "The secretariat of the Gulf Cooperation Council (GCC), founded in 1981, is located in which city?",
  ["Riyadh", "Doha", "Abu Dhabi", "Kuwait City"], "*",
  "Gulf Cooperation Council",
  "The GCC, whose charter was signed on 25 May 1981 by Bahrain, Kuwait, Oman, Qatar, Saudi Arabia and the UAE, has its "
  "secretariat in Riyadh.",
  ["Secretariat: Riyadh", "Six members"],
  [fact("GCC secretariat in Riyadh; founded 1981; six members", "gcc_wiki")],
  why="Doha, Abu Dhabi and Kuwait City are capitals of other members.")

G(T, HH, "Intermediate",
  "The United Nations Industrial Development Organization (UNIDO), which became a UN specialised agency in 1985, is "
  "headquartered in which city?",
  ["Vienna", "Geneva", "Rome", "Nairobi"], "*",
  "UNIDO",
  "UNIDO was created by the UN General Assembly in 1966 and became a specialised agency in 1985. It is headquartered in "
  "Vienna; Gerd Müller has been Director-General since December 2021.",
  ["HQ: Vienna", "Specialised agency: 1985"],
  [fact("UNIDO HQ Vienna; founded 1966; specialised agency 1985; DG Gerd Muller since Dec 2021", "unido_wiki")],
  why="Geneva hosts WHO and ILO, Rome hosts FAO, Nairobi hosts UNEP.")

G(T, HH, "Intermediate",
  "The International Energy Agency (IEA), set up in 1974 within the OECD framework and with which India has had an "
  "association status since 2017, is headquartered in which city?",
  ["Paris", "Vienna", "Abu Dhabi", "Brussels"], "*",
  "International Energy Agency",
  "The IEA was established on 18 November 1974 after the 1973 oil crisis and is headquartered in Paris. Fatih Birol "
  "has been Executive Director since 2015; India became an association country on 30 March 2017.",
  ["HQ: Paris", "Founded: 1974", "India: association country (2017)"],
  [fact("IEA HQ Paris; founded 18 Nov 1974 under OECD; Executive Director Fatih Birol; India association country since "
        "30 March 2017", "iea_wiki")],
  why="Vienna hosts OPEC, Abu Dhabi hosts IRENA, Brussels hosts NATO.")

G(T, HH, "Intermediate",
  "The African Development Bank Group, founded in 1964, is headquartered in which city?",
  ["Abidjan", "Addis Ababa", "Nairobi", "Tunis"], "*",
  "African Development Bank",
  "The AfDB is headquartered in Abidjan, Côte d'Ivoire. It was temporarily based in Tunis during the Ivorian civil war "
  "and returned to Abidjan in September 2014.",
  ["HQ: Abidjan, Côte d'Ivoire", "Founded: 1964"],
  [fact("AfDB HQ Abidjan; founded 1964; temporarily in Tunis, returned Sep 2014", "afdb_wiki")],
  why="Addis Ababa hosts the African Union; Tunis was only a temporary seat; Nairobi hosts UNEP.")

# ====================================================================== Important Reports and Indexes (1 / 6 / 2)
T = "Important Reports and Indexes"
PB, IR = "Publishing body", "India's rank"

G(T, PB, "Basic",
  "The World Migration Report, released every two years since 2000, is the flagship publication of which "
  "organisation?",
  ["International Organization for Migration (IOM)", "UNHCR", "International Labour Organization",
   "UN Population Fund"], "*",
  "World Migration Report",
  "The IOM publishes the World Migration Report every two years; the 2026 edition is the thirteenth.",
  ["Publisher: IOM", "Biennial since 2000"],
  [fact("World Migration Report published by IOM, biennially since 2000", "wmr_wiki")],
  why="UNHCR publishes Global Trends; the ILO publishes World Employment and Social Outlook; UNFPA publishes State of "
      "World Population.")

G(T, PB, "Intermediate",
  "The Human Capital Index, which measures the human capital a child born today can expect to attain by age 18, is "
  "published by which organisation?",
  ["World Bank", "UNDP", "World Economic Forum", "OECD"], "*",
  "Human Capital Index",
  "The Human Capital Index is published by the World Bank; it was introduced with the World Development Report 2019 "
  "as part of its Human Capital Project.",
  ["Publisher: World Bank"],
  [fact("The World Bank publishes the Human Capital Index, introduced with the World Development Report 2019",
        "hci_wiki")],
  why="UNDP publishes the Human Development Index; the WEF and OECD publish other reports.")

G(T, IR, "Intermediate",
  "What was India's rank in the IMD World Competitiveness Ranking 2026, which covered 70 economies?",
  ["44th", "41st", "39th", "37th"], "*",
  "IMD World Competitiveness Ranking 2026",
  "India ranked 44th of 70 economies in 2026, down from 41st in 2025 and 39th in 2024. The ranking was released on "
  "18 June 2026.",
  ["2026: 44th of 70", "2025: 41st; 2024: 39th"],
  [fact("India 44th of 70 in IMD World Competitiveness Ranking 2026; 41st in 2025; 39th in 2024", "imd_gk")],
  why="41st and 39th were India's 2025 and 2024 ranks; 37th was its 2022 rank.",
  current=ca("2026-06-18"))

G(T, PB, "Intermediate",
  "The Index of Economic Freedom, an annual ranking created in 1995, is published by which organisation?",
  ["The Heritage Foundation", "Fraser Institute", "World Economic Forum", "Cato Institute"], "*",
  "Index of Economic Freedom",
  "The Heritage Foundation created the index in 1995 together with The Wall Street Journal.",
  ["Publisher: The Heritage Foundation (with WSJ originally)"],
  [fact("Index of Economic Freedom published by The Heritage Foundation and The Wall Street Journal, created 1995",
        "ief_wiki")],
  why="The Fraser Institute publishes Economic Freedom of the World, a different index.")

G(T, PB, "Intermediate",
  "The Democracy Index, which classifies countries as full democracies, flawed democracies, hybrid regimes or "
  "authoritarian regimes, is published by:",
  ["Economist Intelligence Unit", "Freedom House", "V-Dem Institute", "International IDEA"], "*",
  "Democracy Index",
  "The Economist Intelligence Unit has published the Democracy Index since 2006, using 60 indicators in five "
  "categories.",
  ["Publisher: EIU", "Four regime types; five categories"],
  [fact("Democracy Index by the Economist Intelligence Unit; five categories; four regime types; first published 2006",
        "eiu_wiki")],
  why="Freedom House publishes Freedom in the World; V-Dem and International IDEA publish their own reports.")

G(T, PB, "Intermediate",
  "'The State of the World's Children' is the annual flagship report of which organisation?",
  ["UNICEF", "UNESCO", "UNFPA", "WHO"], "*",
  "State of the World's Children",
  "UNICEF publishes The State of the World's Children as its flagship annual report.",
  ["Publisher: UNICEF"],
  [fact("The State of the World's Children is UNICEF's flagship annual report", "sowc_wiki")],
  why="UNFPA publishes State of World Population; UNESCO publishes the GEM Report.")

G(T, PB, "Intermediate",
  "The Global Slavery Index is published by which organisation?",
  ["Walk Free", "International Labour Organization", "Amnesty International", "Human Rights Watch"], "*",
  "Global Slavery Index",
  "The Global Slavery Index is published by Walk Free (formerly the Walk Free Foundation), part of the Minderoo "
  "Foundation.",
  ["Publisher: Walk Free (Minderoo Foundation)"],
  [fact("Global Slavery Index published by Walk Free, part of Minderoo Foundation", "gsi_wiki")],
  why="The other organisations publish other reports.")

GS(T, IR, "Advanced", "India in the Global Hunger Index 2026, released on 14 October 2026",
   ["India ranked 100th among 122 countries.",
    "India's score placed it in the 'serious' category of hunger.",
    "Pakistan had a better (lower) score than India."],
   [True, True, False],
   "Global Hunger Index 2026",
   "India ranked 100th of 122 with a score of 24.1 ('serious'). Pakistan scored 25.5 and Afghanistan 28.6, worse than "
   "India; Bangladesh (19.2) and Nepal (14.5) did better.",
   [fact("GHI 2026: India 100th of 122, score 24.1, serious; Pakistan 25.5, Bangladesh 19.2, Nepal 14.5; released "
         "14 October", "ghi_fpj")],
   why="Statement 3 is wrong: Pakistan's score (25.5) was worse than India's (24.1).",
   current=ca("2026-10-14"))

GS(T, PB, "Advanced", "'The State of Food Security and Nutrition in the World' (SOFI) report",
   ["It is co-produced by FAO and IFAD.",
    "UNICEF, WFP and WHO also co-produce it.",
    "The World Bank is one of its co-producers."],
   [True, True, False],
   "SOFI report",
   "SOFI is co-produced by five UN agencies: FAO, IFAD, UNICEF, WFP and WHO. The World Bank is not a co-producer.",
   [fact("SOFI co-produced by FAO with IFAD, UNICEF, WFP and WHO", "sofi_fao")],
   why="Statement 3 is wrong: the World Bank is not a co-producer.")

# ====================================================================== Economic Affairs (8 / 2 / 6)
T = "Economic Affairs"
GDP, INF, FIS, MON = ("GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions")

G(T, GDP, "Basic",
  "In its Global Economic Prospects report of June 2026, what growth did the World Bank project for India for 2026 "
  "(FY 2026-27)?",
  ["6.6%", "6.5%", "7.2%", "5.8%"], "*",
  "World Bank GEP June 2026",
  "The World Bank raised India's forecast to 6.6% from 6.5% in January, while cutting global growth for 2026 to 2.5%, "
  "the weakest since the pandemic, because of the Middle East conflict and higher oil prices.",
  ["India 2026: 6.6% (Jan: 6.5%)", "Global 2026: 2.5%"],
  [fact("World Bank lifts India 2026 forecast to 6.6% from 6.5%; global 2.5%", "wb_ians")],
  why="6.5% was the January forecast; 7.2% was for the following year.",
  current=ca("2026-06-11"))

G(T, GDP, "Basic",
  "In its World Economic Outlook of April 2026, what growth did the IMF project for India for FY 2026-27?",
  ["6.5%", "7.0%", "6.4%", "7.4%"], "*",
  "IMF WEO April 2026",
  "The IMF raised India's FY27 forecast to 6.5% from 6.4% as lower US tariffs offset the hit from the West Asia war, "
  "while cutting global 2026 growth from 3.3% to 3.1%. (In October 2026 it raised India's forecast to 7.0%.)",
  ["April 2026: 6.5% (earlier 6.4%)", "Global 2026 cut to 3.1%"],
  [fact("IMF raises India's FY27 growth forecast to 6.5% from 6.4%; global 3.1%", "imf_fpj")],
  why="7.0% is the October 2026 figure; 6.4% was the earlier estimate.",
  current=ca("2026-04-14"))

G(T, GDP, "Basic",
  "Under the new GDP series (base 2022-23) released on 27 February 2026, what was India's real GDP growth in the "
  "October-December 2025 quarter?",
  ["7.8%", "8.4%", "7.4%", "6.9%"], "*",
  "GDP Q3 FY26",
  "MoSPI's first release under the new series put Q3 FY26 growth at 7.8% (7.4% a year earlier) and revised Q2 up to "
  "8.4% from 8.2%.",
  ["Q3 FY26: 7.8%", "Q2 FY26 revised: 8.4%"],
  [fact("Q3 FY26 GDP grew 7.8% under new series (base 2022-23); Q2 revised to 8.4%; released 27 Feb 2026",
        "gdp_print")],
  why="8.4% is the revised Q2 figure; 7.4% is the year-earlier Q3 figure.",
  current=ca("2026-02-27"))

G(T, INF, "Basic",
  "What was India's WPI (wholesale) inflation for September 2026?",
  ["11.39%", "9.92%", "5.54%", "8.66%"], "*",
  "WPI September 2026",
  "WPI inflation rose to 11.39% in September 2026 from 9.92% in August, led by fuel and power (25.85%). The WPI food "
  "index rose 8.66%.",
  ["September 2026 WPI: 11.39%", "August: 9.92%"],
  [fact("WPI inflation 11.39% in September 2026 vs 9.92% in August; fuel and power 25.85%; food index 8.66%",
        "wpi_air")],
  why="9.92% was August; 5.54% was September CPI; 8.66% was the WPI food index.",
  current=ca("2026-10-14"))

G(T, FIS, "Basic",
  "What were India's gross GST collections for the full financial year 2025-26?",
  ["Over ₹22.27 lakh crore", "Over ₹20.18 lakh crore", "Over ₹18.08 lakh crore", "Over ₹25.10 lakh crore"], "*",
  "GST collections FY26",
  "Gross GST collections in 2025-26 were over ₹22.27 lakh crore, up 8.3%. March 2026 alone brought in over ₹2 lakh "
  "crore.",
  ["FY26 gross GST: over ₹22.27 lakh crore (+8.3%)"],
  [fact("FY26 gross GST over ₹22.27 lakh crore, up 8.3%; March 2026 over ₹2 lakh crore", "gst_print")],
  why="The other totals do not match FY26.",
  current=ca("2026-04-01"))

G(T, GDP, "Basic",
  "India's total exports of goods and services reached a record of about how much in 2025-26?",
  ["Over USD 860 billion", "About USD 778 billion", "About USD 1 trillion", "About USD 650 billion"], "*",
  "Exports FY26",
  "Commerce Minister Piyush Goyal said total exports crossed USD 860 billion in 2025-26 (about USD 860.09 billion, up "
  "4.22%; later revised to about USD 863 billion).",
  ["FY26 exports: over USD 860 billion"],
  [fact("India's exports cross 860 billion dollars in 2025-26, says Piyush Goyal", "exp_air"),
   fact("India's exports hit record high of USD 860 billion in FY26, up 4.22%", "exp_asianet")],
  why="USD 778 billion was the FY24 figure; the others do not match.",
  current=ca("2026-04-15"))

G(T, FIS, "Basic",
  "According to CGA data for April-September 2026, the Centre's fiscal deficit reached what share of the 2026-27 "
  "Budget Estimate?",
  ["42.1%", "36.5%", "50.3%", "29.9%"], "*",
  "Fiscal deficit H1 FY27",
  "The fiscal deficit for April-September 2026 was ₹7.14 lakh crore, 42.1% of the BE of ₹16.96 lakh crore, against "
  "36.5% a year earlier. Total receipts were 50.3% of the BE.",
  ["H1 FY27 deficit: ₹7.14 lakh crore = 42.1% of BE", "H1 FY26: 36.5%"],
  [fact("April-September FY27 fiscal deficit ₹7.14 lakh crore, 42.1% of BE; 36.5% last year; receipts 50.3%",
        "fd_wi")],
  why="36.5% is the year-earlier figure; 50.3% is receipts; 29.9% is unrelated.",
  current=ca("2026-10-30"))

G(T, INF, "Basic",
  "What was India's headline CPI (retail) inflation for June 2026, on the 2024=100 series?",
  ["4.38%", "3.93%", "5.32%", "2.75%"], "*",
  "CPI June 2026",
  "Retail inflation rose to 4.38% in June 2026 from 3.93% in May, its first reading above 4% on the new series; food "
  "inflation was 5.32%.",
  ["June 2026 CPI: 4.38%", "May: 3.93%"],
  [fact("India's retail inflation 4.38% in June 2026; food inflation 5.32%; base 2024", "cpi_angel")],
  why="3.93% was May; 5.32% was food inflation; 2.75% was January 2026.",
  current=ca("2026-07-13"))

G(T, GDP, "Intermediate",
  "According to DPIIT data, which country was the largest source of FDI equity inflows into India in 2025-26?",
  ["Singapore", "Mauritius", "United States", "Netherlands"], "*",
  "FDI sources FY26",
  "FDI equity inflows rose 18% to USD 58.84 billion in 2025-26; Singapore was the largest source with USD 19.8 billion.",
  ["Top source FY26: Singapore (USD 19.8 bn)"],
  [fact("FDI equity inflows USD 58.84 bn in FY26, up 18%; Singapore top source USD 19.8 bn", "fdi_om")],
  why="Mauritius, the US and the Netherlands contributed less.",
  current=ca("2026-06-04"))

G(T, FIS, "Intermediate",
  "According to RBI data released in June 2026, what was India's current account balance in January-March 2026?",
  ["Surplus of USD 7.1 billion", "Deficit of USD 7.1 billion", "Surplus of USD 13.7 billion",
   "Deficit of USD 25.2 billion"], "*",
  "Current account Q4 FY26",
  "India had a current account surplus of USD 7.1 billion (0.7% of GDP) in Q4 FY26, against USD 13.7 billion a year "
  "earlier. For 2025-26 as a whole the deficit was USD 25.2 billion (0.6% of GDP).",
  ["Q4 FY26: surplus USD 7.1 bn (0.7% of GDP)", "FY26: deficit USD 25.2 bn"],
  [fact("Q4 FY26 current account surplus USD 7.1 bn (0.7% of GDP); Q4 FY25 USD 13.7 bn; FY26 CAD USD 25.2 bn",
        "cad_ob")],
  why="USD 13.7 billion was the year-earlier surplus; USD 25.2 billion was the full-year deficit.",
  current=ca("2026-06-08"))

GS(T, GDP, "Advanced", "the Asian Development Bank's growth forecasts for India in 2026",
   ["In April 2026 the ADB projected growth of 6.9% for FY 2026-27.",
    "In July 2026 it cut the FY 2026-27 forecast to 6.6%.",
    "In July 2026 it raised its FY 2026-27 inflation forecast to 5.2%."],
   [True, True, True],
   "ADB forecasts",
   "ADB's April 2026 ADO projected 6.9% for FY2026 (FY27) and 7.3% for FY2027. In July it cut FY27 growth to 6.6% "
   "because of higher oil prices and raised FY27 inflation to 5.2% from 4.5%.",
   [fact("ADB April 2026: India 6.9% in FY2026, 7.3% in FY2027", "adb_adb"),
    fact("ADB cuts India FY27 growth forecast to 6.6% from 6.9%; inflation raised to 5.2%", "adb_fpj")],
   why="All three statements are correct.",
   current=ca("2026-07-09"))

GS(T, MON, "Advanced", "the RBI Monetary Policy Committee's review of 6-8 April 2026",
   ["It kept the policy repo rate unchanged at 5.25%.",
    "It changed the policy stance to accommodative.",
    "It projected CPI inflation for 2026-27 at 4.6%."],
   [True, False, True],
   "MPC April 2026",
   "In the first review of FY27 (8 April 2026) the MPC held the repo rate at 5.25% and kept a neutral stance. It "
   "projected FY27 CPI inflation at 4.6%.",
   [fact("April 2026 MPC: repo held at 5.25%; neutral stance; FY27 CPI projected 4.6%", "mpcapr_5p"),
    fact("RBI kept repo rate unchanged, maintained policy stance neutral", "mpcapr_ao")],
   why="Statement 2 is wrong: the stance stayed neutral.",
   current=ca("2026-04-08"))

GS(T, MON, "Advanced", "the RBI Monetary Policy Committee meeting of 3-5 August 2026",
   ["The decision to keep the repo rate at 5.25% was unanimous.",
    "After the meeting the SDF rate stood at 5.00% and the MSF rate at 5.50%.",
    "It projected CPI inflation for 2026-27 at 4.0%."],
   [True, True, False],
   "MPC August 2026",
   "At its 62nd meeting the MPC unanimously held the repo rate at 5.25% with a neutral stance; SDF was 5.00% and "
   "MSF/Bank Rate 5.50%. It projected FY27 CPI inflation at 5.0%.",
   [fact("62nd MPC, 3-5 Aug 2026: repo 5.25% unanimous; SDF 5.00%; MSF 5.50%; FY27 CPI 5.0%", "mpcaug_scc")],
   why="Statement 3 is wrong: the projection was 5.0%.",
   current=ca("2026-08-05"))

GS(T, INF, "Advanced", "the PLFS monthly bulletin for September 2026",
   ["The overall unemployment rate (age 15 and above) was 5.0%.",
    "The urban unemployment rate was lower than the rural rate.",
    "Urban female LFPR rose to 25.9%, its highest since October 2025."],
   [True, False, True],
   "PLFS September 2026",
   "The overall unemployment rate was 5.0% (unchanged from August); rural was 4.2% and urban 6.9%. Urban female LFPR "
   "rose to 25.9%.",
   [fact("PLFS Sep 2026: UR 5%; rural 4.2%, urban 6.9%; urban female LFPR 25.9%, highest since Oct 2025", "plfs_dd")],
   why="Statement 2 is wrong: urban unemployment (6.9%) was higher than rural (4.2%).",
   current=ca("2026-10-15"))

GS(T, GDP, "Advanced", "India's FDI inflows in 2025-26",
   ["FDI equity inflows rose 18% to about USD 58.8 billion.",
    "Maharashtra was the top destination state.",
    "Total FDI inflows were below USD 80 billion."],
   [True, True, False],
   "FDI FY26",
   "DPIIT data showed equity inflows of USD 58.84 billion (+18%); total FDI including reinvested earnings was about "
   "USD 94.5 billion (+17%). Maharashtra drew USD 18.41 billion.",
   [fact("FDI equity USD 58.84 bn (+18%); total FDI USD 94.5 bn; Maharashtra top state USD 18.41 bn", "fdi_om")],
   why="Statement 3 is wrong: total FDI was about USD 94.5 billion.",
   current=ca("2026-06-04"))

GS(T, INF, "Advanced", "India's retail inflation for June 2026",
   ["Headline CPI inflation was 4.38%.",
    "The CPI series used has 2024 as its base year.",
    "Urban inflation was higher than rural inflation."],
   [True, True, False],
   "CPI June 2026 details",
   "June 2026 CPI inflation was 4.38% on the 2024=100 series; rural was 4.74% and urban 3.92%; food inflation 5.32%.",
   [fact("June 2026 CPI 4.38%; base year 2024; rural 4.74%, urban 3.92%", "cpi_angel")],
   why="Statement 3 is wrong: rural inflation (4.74%) was higher than urban (3.92%).",
   current=ca("2026-07-13"))

# ====================================================================== Government Policies (1 / 0 / 0)
T = "Government Policies"
G(T, "Policy changes", "Basic",
  "The Kerala (Alteration of Name) Act, 2026, passed in the Monsoon Session of Parliament, renames the State of Kerala "
  "as what?",
  ["Keralam", "Keraladesam", "Malanadu", "Kerala Pradesh"], "*",
  "Renaming of Kerala",
  "The Act, which received assent on 14 August 2026, renames the State of Kerala as Keralam and makes consequential "
  "changes to laws. It was one of 11 Acts from the Monsoon Session (20 July-13 August 2026).",
  ["New name: Keralam", "Assent: 14 Aug 2026"],
  [fact("Kerala (Alteration of Name) Act, 2026 renames Kerala as Keralam; assent 14 August", "keralam_scc")],
  why="The Act uses the name Keralam.",
  current=ca("2026-08-14"))

# ====================================================================== Business and Corporate News (0 / 9 / 0)
T = "Business and Corporate News"
MA, CP = "Mergers and acquisitions", "Corporate partnerships"

G(T, MA, "Intermediate",
  "In November 2025 Pfizer won a bidding war against Novo Nordisk to acquire which obesity-drug developer for about "
  "USD 10 billion?",
  ["Metsera", "Kenvue", "Viking Therapeutics", "Structure Therapeutics"], "*",
  "Pfizer-Metsera",
  "Metsera accepted Pfizer's raised offer (USD 65.60 cash plus a CVR of up to USD 20.65 per share) on 7 November 2025 "
  "after Novo Nordisk declined to raise its bid; Pfizer completed the deal on 13 November.",
  ["Target: Metsera", "Rival bidder: Novo Nordisk"],
  [fact("Pfizer wins USD 10 billion bidding war for Metsera; Novo exits; $65.60 + CVR up to $20.65", "metsera_rte"),
   fact("Pfizer finalizes Metsera buy after bidding war with Novo Nordisk", "metsera_fp")],
  why="Kenvue was bought by Kimberly-Clark; the others were not acquired by Pfizer.",
  current=ca("2025-11-07"))

G(T, MA, "Intermediate",
  "Abbott agreed in November 2025 to acquire which cancer-diagnostics company, maker of the Cologuard test, for about "
  "USD 21 billion?",
  ["Exact Sciences", "Guardant Health", "Illumina", "Natera"], "*",
  "Abbott-Exact Sciences",
  "Abbott agreed on 20 November 2025 to buy Exact Sciences for USD 105 per share, about USD 21 billion in equity value "
  "(about USD 23 billion including debt).",
  ["Target: Exact Sciences", "Price: USD 105 per share"],
  [fact("Abbott confirms USD 21 billion Exact Sciences acquisition at $105 per share", "exact_md"),
   fact("Abbott to acquire Exact Sciences for $21 billion", "exact_ipp")],
  why="The other companies were not part of this deal.",
  current=ca("2025-11-20"))

G(T, MA, "Intermediate",
  "IBM announced on 8 December 2025 that it would acquire which data-streaming company, built on Apache Kafka, for "
  "about USD 11 billion?",
  ["Confluent", "Databricks", "Snowflake", "HashiCorp"], "*",
  "IBM-Confluent",
  "IBM agreed to buy Confluent, whose platform is built on Apache Kafka for real-time data streams, for about USD 11 "
  "billion, to strengthen its AI and hybrid cloud offerings.",
  ["Target: Confluent", "Value: about USD 11 billion"],
  [fact("IBM to acquire Confluent for $11 billion; Apache Kafka platform; dated 8 Dec 2025", "ibm_tz")],
  why="HashiCorp was an earlier IBM purchase; Databricks and Snowflake were not acquired.",
  current=ca("2025-12-08"))

G(T, CP, "Intermediate",
  "Meesho's shares debuted on the NSE on 10 December 2025 at ₹162.50. What was the IPO issue price?",
  ["₹111", "₹105", "₹128", "₹162"], "*",
  "Meesho listing",
  "Meesho's IPO was priced at ₹111 (band ₹105-111); the shares opened at ₹162.50 on the NSE (about 46% premium) and "
  "₹161.20 on the BSE.",
  ["Issue price: ₹111", "NSE open: ₹162.50 (+46%)"],
  [fact("Meesho listed 10 Dec 2025; issue price ₹111; NSE open ₹162.5 (46.4% premium)", "meesho_week")],
  why="₹105 was the lower end of the band; ₹162 was close to the listing price.",
  current=ca("2025-12-10"))

G(T, CP, "Intermediate",
  "Eyewear retailer Lenskart Solutions listed on 10 November 2025. How did the shares open on the NSE compared with the "
  "₹402 issue price?",
  ["At ₹395, a discount of about 1.7%", "At ₹450, a premium of about 12%", "At ₹402, flat",
   "At ₹362, a discount of about 10%"], "*",
  "Lenskart listing",
  "Lenskart opened at ₹395 on the NSE (about 1.74% below ₹402) and ₹390 on the BSE (about 2.98% below).",
  ["Issue price: ₹402", "NSE open: ₹395"],
  [fact("Lenskart listed 10 Nov 2025 at ₹395 on NSE, 1.74% discount to ₹402; ₹390 on BSE", "lens_week")],
  why="The shares neither opened at a premium nor flat; ₹362 was not the opening price.",
  current=ca("2025-11-10"))

G(T, MA, "Intermediate",
  "On 30 October 2026 Tata Motors' subsidiary completed the settlement of its tender offer for 89.42% of which "
  "European truck and bus maker?",
  ["Iveco Group", "Scania", "MAN Truck & Bus", "Volvo Group"], "*",
  "Tata Motors-Iveco",
  "TML CV Holdings acquired 89.42% of Iveco Group at €14.40 per share (about €3.43 billion) on 30 October 2026, with "
  "the offer reopened for remaining shares.",
  ["Target: Iveco Group", "Stake: 89.42% at €14.40/share"],
  [fact("Tata Motors completes Iveco acquisition: 89.42% at €14.40 per share, €3.43 bn; settlement 30 Oct 2026",
        "iveco_mio")],
  why="Scania and MAN belong to Traton (Volkswagen); Volvo Group was not acquired.",
  current=ca("2026-10-30"))

G(T, MA, "Intermediate",
  "In 2026 Sun Pharmaceutical Industries agreed to acquire which US-based company in a deal of about USD 12 billion, "
  "the largest takeover by an Indian pharmaceutical company?",
  ["Organon", "Viatris", "Perrigo", "Taro Pharmaceutical"], "*",
  "Sun Pharma-Organon",
  "Sun Pharma's agreement to buy Organon, worth about USD 12 billion, was reported in May 2026 as the largest takeover "
  "by an Indian pharma company to date.",
  ["Target: Organon", "Value: about USD 12 billion"],
  [fact("Sun Pharma acquires Organon in USD 12 billion deal, largest takeover by Indian pharma company", "sun_gene")],
  why="Taro was an earlier Sun Pharma acquisition; Viatris and Perrigo were not targets.",
  current=ca("2026-05-04"))

G(T, MA, "Intermediate",
  "Reliance Retail announced on 30 April 2026 that it had acquired Anomaly, a haircare brand founded in 2021 by whom?",
  ["Priyanka Chopra Jonas", "Deepika Padukone", "Katrina Kaif", "Alia Bhatt"], "*",
  "Reliance-Anomaly",
  "Reliance Retail acquired Anomaly, the haircare brand founded by Priyanka Chopra Jonas in 2021, for an undisclosed "
  "sum; she remains Creative Director.",
  ["Brand: Anomaly", "Founder: Priyanka Chopra Jonas"],
  [fact("Reliance Retail acquires Priyanka Chopra Jonas's haircare brand Anomaly on 30 April 2026; undisclosed amount",
        "anomaly_week")],
  why="The other actors own other beauty brands (82°E, Kay Beauty, Ed-a-Mamma).",
  current=ca("2026-04-30"))

G(T, MA, "Intermediate",
  "Persistent Systems made a voluntary public takeover offer of €81 per share in 2026 for which Germany-listed IT "
  "services company?",
  ["Nagarro", "SAP", "Software AG", "Bechtle"], "*",
  "Persistent-Nagarro",
  "Persistent's subsidiary offered €81 per share for Nagarro (about 140% above its pre-offer price), backed by "
  "Nagarro's board; the offer closed in October 2026 with most shares tendered.",
  ["Target: Nagarro", "Offer: €81 per share"],
  [fact("Nagarro board backs Persistent's €81-per-share takeover offer at 140% premium", "nagarro_p2"),
   fact("Persistent's takeover offer for Nagarro succeeds", "nagarro_ent")],
  why="SAP, Software AG and Bechtle were not targets.",
  current=ca("2026-06-28"))

# ====================================================================== Static Awareness (6 / 1 / 8)
T = "Static Awareness"
CC, NP, SF = "Capitals and currencies", "National parks and dams", "Indian states facts"

G(T, NP, "Basic",
  "Bandhavgarh National Park, declared a national park in 1968, is located in which state?",
  ["Madhya Pradesh", "Chhattisgarh", "Maharashtra", "Odisha"], "*",
  "Bandhavgarh",
  "Bandhavgarh National Park is in Umaria district, Madhya Pradesh; it became a tiger reserve in 1993.",
  ["State: Madhya Pradesh (Umaria district)"],
  [fact("Bandhavgarh NP in Umaria district, Madhya Pradesh; NP 1968; tiger reserve 1993", "bandh_wiki")],
  why="It is in Madhya Pradesh.")

G(T, NP, "Basic",
  "The Indira Sagar Dam in Khandwa district, Madhya Pradesh, is built on which river?",
  ["Narmada", "Tapti", "Chambal", "Betwa"], "*",
  "Indira Sagar Dam",
  "The Indira Sagar Dam at Narmada Nagar, Khandwa district, is on the Narmada and has 1,000 MW installed capacity.",
  ["River: Narmada", "Capacity: 1,000 MW"],
  [fact("Indira Sagar Dam on the Narmada in Khandwa district, MP; 1,000 MW", "isagar_wiki")],
  why="The dam is on the Narmada.")

G(T, SF, "Basic",
  "Chhattisgarh, which came into existence on 1 November 2000, was carved out of which state?",
  ["Madhya Pradesh", "Bihar", "Uttar Pradesh", "Odisha"], "*",
  "Chhattisgarh",
  "Chhattisgarh was formed from Madhya Pradesh on 1 November 2000; its capital is Raipur.",
  ["Formed: 1 Nov 2000 from Madhya Pradesh", "Capital: Raipur"],
  [fact("Chhattisgarh formed 1 November 2000 from Madhya Pradesh; capital Raipur", "chh_wiki")],
  why="Jharkhand came from Bihar and Uttarakhand from Uttar Pradesh.")

G(T, CC, "Basic",
  "What is the currency of Hungary?",
  ["Forint", "Koruna", "Zloty", "Leu"], "*",
  "Hungary's currency",
  "Hungary's currency is the forint (HUF), introduced on 1 August 1946 and issued by the Hungarian National Bank.",
  ["Currency: forint (HUF)"],
  [fact("Hungarian forint is Hungary's currency, introduced 1946, issued by Hungarian National Bank", "huf_wiki")],
  why="The koruna is Czech, the zloty Polish and the leu Romanian.")

G(T, CC, "Basic",
  "What is the capital of New Zealand?",
  ["Wellington", "Auckland", "Christchurch", "Hamilton"], "*",
  "New Zealand's capital",
  "Wellington, at the south-western tip of the North Island, has been New Zealand's capital since 1865. Auckland is the "
  "largest city.",
  ["Capital: Wellington (since 1865)"],
  [fact("Wellington is the capital of New Zealand since 1865, on the North Island", "wlg_wiki")],
  why="Auckland, Christchurch and Hamilton are other cities.")

G(T, CC, "Basic",
  "What is the capital of Uganda?",
  ["Kampala", "Entebbe", "Nairobi", "Kigali"], "*",
  "Uganda's capital",
  "Kampala is the capital and largest city of Uganda; the currency is the Ugandan shilling.",
  ["Capital: Kampala", "Currency: Ugandan shilling"],
  [fact("Uganda: capital Kampala; currency Ugandan shilling", "uga_wiki")],
  why="Entebbe hosts the airport; Nairobi and Kigali are capitals of Kenya and Rwanda.")

G(T, CC, "Intermediate",
  "Prime Minister Modi visited Norway in May 2026. What is the currency of Norway, issued by Norges Bank?",
  ["Krone", "Krona", "Euro", "Mark"], "*",
  "Norway's currency",
  "Norway's currency is the krone, issued by Norges Bank and introduced in 1875. Sweden uses the krona; Norway is not "
  "in the EU or the euro area.",
  ["Currency: Norwegian krone (NOK)", "Issuer: Norges Bank"],
  [fact("Norwegian krone, currency of Norway, issued by Norges Bank, introduced 1875", "nok_wiki")],
  why="The krona is Sweden's; Norway does not use the euro; the mark was a former currency of Finland and Germany.")

GS(T, NP, "Advanced", "Ranthambore National Park",
   ["It is in Sawai Madhopur district of Rajasthan.",
    "It is bounded by the Banas river to the north and the Chambal to the south.",
    "It was declared a national park in 1955."],
   [True, True, False],
   "Ranthambore",
   "Ranthambore in Sawai Madhopur district lies between the Banas (north) and Chambal (south). It came under Project "
   "Tiger in 1974 and was declared a national park in 1980.",
   [fact("Ranthambore: Sawai Madhopur, Rajasthan; NP 1980; Project Tiger 1974; Banas north, Chambal south",
         "ranth_wiki")],
   why="Statement 3 is wrong: it became a national park in 1980.")

GS(T, NP, "Advanced", "the Koyna Dam",
   ["It is in Satara district of Maharashtra.",
    "Its reservoir is called Shivasagar Lake.",
    "It was damaged by the Latur earthquake of 1993."],
   [True, True, False],
   "Koyna Dam",
   "The Koyna Dam on the Koyna river, in Satara district, forms Shivasagar Lake. It was cracked by the 1967 "
   "Koynanagar earthquake, not the 1993 Latur quake.",
   [fact("Koyna Dam: Koyna river, Satara district, Maharashtra; reservoir Shivasagar; cracked in 1967 Koynanagar "
         "earthquake", "koyna_wiki")],
   why="Statement 3 is wrong: the damage was from the 1967 Koynanagar earthquake.")

GS(T, NP, "Advanced", "the Idukki Dam",
   ["It is a double-curvature arch dam on the Periyar river.",
    "It stands between the Kuravanmala and Kurathimala hills.",
    "Its power station is at Moolamattom."],
   [True, True, True],
   "Idukki Dam",
   "The Idukki arch dam on the Periyar in Kerala stands in a gorge between Kuravanmala and Kurathimala; its "
   "underground power station is at Moolamattom.",
   [fact("Idukki Dam: double-curvature arch dam on Periyar; between Kuravanmala and Kurathimala; power station at "
         "Moolamattom", "idukki_wiki")],
   why="All three statements are correct.")

GS(T, NP, "Advanced", "the Great Himalayan National Park",
   ["It is in Kullu district of Himachal Pradesh.",
    "It was inscribed as a UNESCO World Heritage Site in 2014."],
   [True, True],
   "Great Himalayan NP",
   "GHNP, in the Banjar sub-division of Kullu district, was established in 1984, notified as a national park in 1999 "
   "and inscribed on the World Heritage List in 2014.",
   [fact("GHNP in Kullu district, Himachal Pradesh; World Heritage 2014", "ghnp_wiki")],
   why="Both statements are correct.")

GS(T, NP, "Advanced", "the Valley of Flowers National Park",
   ["It is in Chamoli district of Uttarakhand.",
    "It became a World Heritage Site in 1988, at the same time as Nanda Devi National Park."],
   [True, False],
   "Valley of Flowers",
   "The Valley of Flowers in Chamoli district was added in 2005 as an extension of the Nanda Devi World Heritage Site "
   "inscribed in 1988; the site is now 'Nanda Devi and Valley of Flowers National Parks'.",
   [fact("Valley of Flowers NP in Chamoli, Uttarakhand; UNESCO site 1988 with Valley of Flowers added in 2005",
         "vof_wiki")],
   why="Statement 2 is wrong: the Valley of Flowers was added in 2005.")

GS(T, SF, "Advanced", "Meghalaya",
   ["It became a full state on 21 January 1972 under the North-Eastern Areas (Reorganisation) Act, 1971.",
    "Before that it was an autonomous state within Assam from 1970.",
    "Its capital is Imphal."],
   [True, True, False],
   "Meghalaya",
   "Meghalaya was an autonomous state within Assam from 2 April 1970 and became a full state on 21 January 1972. Its "
   "capital is Shillong; Imphal is Manipur's capital.",
   [fact("Meghalaya: full statehood 21 Jan 1972 under NEA (Reorganisation) Act 1971; autonomous state from 1970; "
         "capital Shillong", "megh_wiki")],
   why="Statement 3 is wrong: Meghalaya's capital is Shillong.")

GS(T, SF, "Advanced", "Mizoram",
   ["It became India's 23rd state on 20 February 1987.",
    "The Mizoram Peace Accord was signed in 1986.",
    "Its capital is Aizawl."],
   [True, True, True],
   "Mizoram",
   "After the Mizoram Peace Accord of 30 June 1986, Mizoram became the 23rd state on 20 February 1987, with Aizawl as "
   "its capital.",
   [fact("Mizoram 23rd state on 20 Feb 1987; Peace Accord 30 June 1986; capital Aizawl", "miz_wiki")],
   why="All three statements are correct.")

GS(T, CC, "Advanced", "the Czech koruna",
   ["It is the currency of the Czech Republic, introduced in 1993.",
    "It is divided into 100 haléř (hellers).",
    "The Czech Republic adopted the euro in 2010."],
   [True, True, False],
   "Czech koruna",
   "The koruna replaced the Czechoslovak koruna in 1993 and is issued by the Czech National Bank. The plan to adopt the "
   "euro in 2010 was suspended in 2005; Czechia still uses the koruna.",
   [fact("Czech koruna introduced 1993; 1 koruna = 100 hellers; euro plan for 2010 suspended", "czk_wiki")],
   why="Statement 3 is wrong: Czechia has not adopted the euro.")


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
    plan = json.loads((ROOT / "batches" / "plans" / f"{BATCH}_plan.json").read_text(encoding="utf-8"))
    ga = next(s for s in plan["subjects"] if s["subject"] == GA)
    first = int(ga["question_ids"][0].rsplit("_", 1)[1])
    counts = place_answers(items)
    out = []
    for n, it in enumerate(items):
        ans = it["answer"]
        opts = it["options"]
        hows = {f.pop("_how") for f in it["facts"]}
        verified_by = ["ai:author-solve"]
        if OPENED in hows:
            verified_by.append("web:fact-check")
        if SEARCH in hows:
            verified_by.append("web:search-confirmed")
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
        q["verification"] = {"answer_verified": True, "solution_verified": True,
                             "review_status": "Pending Human Review",
                             "verified_by": verified_by, "verified_at": TODAY,
                             "fact_checks": it["facts"]}
        out.append(q)

    # quota check against the plan before writing
    have = Counter((q["topic"], q["difficulty"]) for q in out)
    for t in ga["topics"]:
        for d, k in t["quota"].items():
            assert have[(t["topic"], d)] == k, (t["topic"], d, have[(t["topic"], d)], k)
        assert all(q["subtopic"] in t["subtopics"] for q in out if q["topic"] == t["topic"]), t["topic"]
    assert len(out) == ga["total"] == 150
    assert out[0]["question_id"] == ga["question_ids"][0] and out[-1]["question_id"] == ga["question_ids"][1]
    for q in out:
        if q["topic"] in CA_TOPICS:
            assert CA_FROM <= q["current_affairs"]["event_date"] <= CA_TO, q["question_id"]
        texts = [o["text"] for o in q["options"]]
        if texts in (S12, S123):
            assert q["correct_answer"] in LETTERS
    assert len({q["question_text"] for q in out}) == len(out)
    assert max(counts.values()) - min(counts.values()) <= 2, counts
    return out, counts


_plan = json.loads((ROOT / "batches" / "plans" / f"{BATCH}_plan.json").read_text(encoding="utf-8"))
_order = [t["topic"] for t in next(s for s in _plan["subjects"] if s["subject"] == GA)["topics"]]
_rank = {"Basic": 0, "Intermediate": 1, "Advanced": 2}
QUESTIONS.sort(key=lambda it: (_order.index(it["topic"]), _rank[it["difficulty"]]))

questions, keys = build(QUESTIONS)
batch = {
    "schema_version": "1.0",
    "batch_id": BATCH,
    "created_at": TODAY,
    "notes": "BATCH_004 General Awareness part: 150 original questions. Current-affairs topics (National and "
             "International Current Affairs, Appointments, Awards, Sports, Summits, Economic Affairs, Business) test "
             "events dated 2025-11-01 to 2026-11-04, with event dates from the sources and review_by 2027-05-05. "
             "Other time-sensitive facts also carry current_affairs dates. No fact or event tested in BATCH_000 to "
             "BATCH_003 GA is tested again. Fact checks dated 2026-11-05; verified_by says whether each question's "
             "sources were opened (web:fact-check) or confirmed only in search results (web:search-confirmed). "
             "Pending human review.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / f"{BATCH}_GA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(keys.items()))})")
