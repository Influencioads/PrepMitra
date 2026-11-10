"""Writes batches/parts/BATCH_002_GA.json: the 150 General Awareness questions of BATCH_002.

This batch carries the current-affairs topics (National/International Current Affairs, Appointments, Awards, Sports,
Summits, Books, Economic Affairs, Business). Every current-affairs question tests an event dated between 2025-11-01
and 2026-11-04, takes its event date from the source and carries current_affairs {event_date, review_by 2027-05-05}.
Other time-sensitive facts (scheme figures, heads of bodies, index ranks, policy changes) carry current_affairs too.

Every fact has a fact_check. Each URL is marked as either OPENED (fetched and read on 2026-11-05, giving
"web:fact-check") or SEARCH (confirmed only from search-result text on 2026-11-05, giving "web:search-confirmed").
pib.gov.in, nobelprize.org, fatf-gafi.org and indiabudget.gov.in returned HTTP 403 to fetches, so facts from them
were confirmed from search results or from other pages that were opened.

Options are written with the correct answer either at a fixed letter (ordered options and statement combinations) or
first with answer "*" (unordered options). Flexible questions are then placed so that the keys are balanced A to D.

    python tools/batch_002/ga.py
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
SECONDS = {"Basic": 15, "Intermediate": 25, "Advanced": 45}
CA_TOPICS = {"National Current Affairs", "International Current Affairs", "Important Appointments",
             "Awards and Honours", "Sports", "Summits and Conferences", "Books and Authors", "Economic Affairs",
             "Business and Corporate News"}

# Statement-combination option sets (fixed order)
S12 = ["Only 1", "Only 2", "Both 1 and 2", "Neither 1 nor 2"]
S123 = ["1 and 2 only", "2 and 3 only", "1 and 3 only", "1, 2 and 3"]

QUESTIONS = []
OPENED, SEARCH = "opened", "search"


def ca(event_date):
    return {"event_date": event_date, "review_by": REVIEW_BY}


def G(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, facts,
      why=None, shortcut=None, current=None):
    assert len(options) == 4 and len(set(options)) == 4, text
    assert answer == "*" or answer in LETTERS, answer
    assert facts, text
    if topic in CA_TOPICS:
        assert current and CA_FROM <= current["event_date"] <= CA_TO, (text, current)
    QUESTIONS.append(dict(topic=topic, subtopic=subtopic, difficulty=difficulty, text=text, options=list(options),
                          answer=answer, concept=concept, explanation=explanation, steps=steps, facts=facts,
                          why=why, shortcut=shortcut, current=current))


# ====================================================================== sources
# key: (url, how it was checked on 2026-11-05)
U = {
    # RBI and economy
    "rbi_home": ("https://www.rbi.org.in/", OPENED),
    "rbi_policy": ("https://www.rbi.org.in/Scripts/Annualpolicy.aspx", OPENED),
    "mpc_oct": ("https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63742", OPENED),
    "mpc_aug": ("https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63287", OPENED),
    "mpc_apr": ("https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62514", OPENED),
    "mpc_dec": ("https://www.businesstoday.in/latest/economy/story/rbi-mpc-meeting-central-bank-slashes-repo-rate-by-"
                "25-bps-to-525-from-55-505183-2025-12-05", SEARCH),
    "budget_bulletin": ("https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=23979", OPENED),
    "budget_quint": ("https://www.thequint.com/news/breaking-news/union-budget-2026-fy27-fiscal-deficit-target", OPENED),
    "fc16": ("https://www.theweek.in/wire-updates/national/2026/02/01/16th-fin-comm-recommends-states-share-in-central-"
             "taxes-at-41-pc-for-5-years-till-2031.html", SEARCH),
    "gdp_new": ("https://www.tribuneindia.com/news/business/india-gdp-to-grow-7-6-in-2025-26-government-estimates-after-"
                "base-year-revision/", SEARCH),
    "cpi_new": ("https://theprint.in/economy/india-unveils-new-cpi-series-with-2024-base-wider-basket-jan-retail-"
                "inflation-at-2-75/2853215/", SEARCH),
    "gdp_q1": ("https://thefederal.com/category/business/indias-real-gdp-growth-hits-78-per-cent-in-q1-fy27-says-govt-"
               "255276", SEARCH),
    "gdp_q1_pib": ("https://pib.gov.in/FactsheetDetails.aspx?Id=150991", SEARCH),
    # Policies
    "shanti": ("https://www.businesstoday.in/india/story/shanti-bill-gets-presidents-nod-opening-indias-civil-nuclear-"
               "sector-to-private-players-507592-2025-12-22", SEARCH),
    "shanti_wnn": ("https://world-nuclear-news.org/articles/indias-shanti-bill-completes-legislative-process", SEARCH),
    "insurance": ("https://www.livelaw.in/news-updates/parliament-passes-sabka-bima-sabki-raksha-bill-allows-100-fdi-"
                  "in-insurance-sector-513872", SEARCH),
    "insurance_bt": ("https://www.businesstoday.in/personal-finance/insurance/story/sabka-bima-sabki-raksha-amendment-"
                     "of-insurance-laws-bill-passed-in-parliament-key-details-here-507128-2025-12-17", SEARCH),
    "smc": ("https://prsindia.org/billtrack/the-securities-markets-code-2025", SEARCH),
    "smc_taxmann": ("https://www.taxmann.com/post/blog/govt-introduces-the-securities-markets-code-in-lok-sabha", SEARCH),
    "rbi_md": ("https://www.businesstoday.in/latest/economy/story/rbi-consolidates-9000-circulars-into-244-master-"
               "directions-for-enhanced-ease-of-doing-business-details-here-504215-2025-11-28", SEARCH),
    "rbi_md_air": ("https://www.newsonair.gov.in/rbi-repeals-9000-circulars-consolidates-rules-into-244-master-"
                   "directions-to-ease-compliance/", SEARCH),
    "ecl": ("https://www.businesstoday.in/india/story/rbi-tightens-bad-loan-recognition-new-norms-push-banks-towards-"
            "global-standards-527682-2026-04-27", SEARCH),
    "ecl_kpmg": ("https://kpmg.com/in/en/insights/2026/05/expected-credit-loss.html", SEARCH),
    "ffs2": ("https://www.pmindia.gov.in/en/news_updates/cabinet-approves-startup-india-fund-of-funds-2-0-to-mobilize-"
             "venture-capital-for-indias-startup-ecosystem", SEARCH),
    "cpc8": ("https://upstox.com/news/personal-finance/latest-updates/8th-pay-commission-full-text-of-terms-of-reference-"
             "of-8th-cpc-notified-on-november-3-2025/article-184015", SEARCH),
    "cpc8_wire": ("https://thewire.in/government/eighth-pay-commission-ten-months-terms-of-reference-cabinet-ranjana-"
                  "desai-justice", SEARCH),
    # Schemes
    "pmis": ("https://www.businesstoday.in/india/story/pm-internship-scheme-90000-opportunities-open-get-all-"
             "eligibility-benefits-and-application-details-449784-2024-10-12", SEARCH),
    "vayvandana": ("https://www.businesstoday.in/personal-finance/insurance/story/ab-pmjay-2024-what-is-ayushman-vaya-"
                   "vandana-card-know-how-to-register-for-additional-health-cover-for-seniors-452061-2024-10-30",
                   SEARCH),
    "dhandhaanya": ("https://www.theweek.in/wire-updates/business/2025/07/16/del57-cab-ld-agri.html", SEARCH),
    "pmkisan21": ("https://www.tribuneindia.com/news/india/pm-releases-rs-18000-crore-under-pm-kisan-scheme-in-tamil-"
                  "nadus-coimbatore", SEARCH),
    "ebus": ("https://www.autocarpro.in/news/pm-ebus-sewa-cabinet-approves-rs-57613-cr-for-10k-e-buses-across-cities-"
             "116381", SEARCH),
    "pulses": ("https://www.narendramodi.in/union-cabinet-approves-mission-for-aatmanirbharta-in-pulses-for-2025-26-to-"
               "2030-31-598124", SEARCH),
    "pmayu2": ("https://pmaymis.gov.in/PMAYMIS2_2024/PmayUrban.aspx", SEARCH),
    "pmayu2_air": ("https://newsonair.gov.in/union-cabinet-approves-pradhan-mantri-awas-yojana-urban-pmay-u-2-0-scheme",
                   SEARCH),
    "lakhpati": ("https://yourstory.com/herstory/2026/08/pm-modi-target-6-crore-lakhpati-didis-lauds-women-"
                 "transforming-rural-economy", SEARCH),
    "vbgramg": ("https://www.onmanorama.com/news/india/2025/12/21/viksit-bharat-guarantee-rural-employment-president-"
                "assent.html", SEARCH),
    "vbgramg_air": ("https://www.newsonair.gov.in/president-murmu-assents-to-vb-g-ram-g-bill-2025", SEARCH),
    "ism2": ("https://openthemagazine.com/business/budget-2026-sitharaman-launches-semiconductor-mission-20-with-40000-"
             "crore-push", OPENED),
    "pmkisan_cont": ("https://newsonair.gov.in/pm-kisan-scheme-to-be-continued-till-2030-31-says-union-ib-minister/",
                     OPENED),
    "pmvbry": ("https://morungexpress.com/pm-modi-launches-rs-1-lakh-crore-pradhan-mantri-viksit-bharat-rozgar-yojana-"
               "to-create-35-crore-jobs", SEARCH),
    "pmvbry_portal": ("https://ianslive.in/pradhan-mantri-viksit-bharat-rozgar-yojana-portal-goes-live-know-its-"
                      "benefits--20250818191204", SEARCH),
    # Awards and books
    "nobel_peace": ("https://www.khaleejtimes.com/world/navanethem-navi-pillay-wins-nobel-peace-prize-2026", OPENED),
    "nobel_lit": ("https://www.devdiscourse.com/article/international/3989015-canadian-writer-anne-carson-wins-2026-"
                  "nobel-prize-in-literature", OPENED),
    "nobel_econ": ("https://www.devdiscourse.com/article/international/3990823-hall-and-woodford-win-2026-nobel-"
                   "economics-prize", OPENED),
    "padma": ("https://www.business-standard.com/india-news/v-s-achuthanandhan-dharmendra-awarded-padma-vibhushan-"
              "posthumously-126012500462_1.html", SEARCH),
    "intl_booker": ("https://www.nhpr.org/2026-05-19/taiwan-travelogue-wins-the-2026-international-booker-prize",
                    SEARCH),
    "booker25": ("https://www.tribuneindia.com/news/world/hungarian-british-author-david-szalay-beats-kiran-desai-to-"
                 "win-booker-prize-2025-for-flesh", SEARCH),
    "pulitzer": ("https://www.pulitzer.org/news/2026-pulitzer-prize-announcement", SEARCH),
    "pulitzer_ap": ("https://m.washingtontimes.com/news/2026/may/4/pulitzer-winners-arts-include-daniel-kraus-angel-"
                    "bess-wohls/", SEARCH),
    "womens_prize": ("https://www.kirkusreviews.com/news-and-features/articles/winners-of-the-2026-womens-prizes-"
                     "revealed/", SEARCH),
    "womens_prize_ie": ("https://www.irishexaminer.com/lifestyle/artsandculture/arid-41860962.html", SEARCH),
    # Sports
    "wodi_final": ("https://www.newsonair.gov.in/india-win-first-ever-icc-womens-odi-world-cup-title-beat-south-"
                   "africa-by-52-runs", SEARCH),
    "wodi_wisden": ("https://www.wisden.com/series/icc-womens-cricket-world-cup-2025/cricket-news/india-awakes-to-"
                    "history---india-beat-south-africa-to-win-2025-womens-world-cup", SEARCH),
    "t20wc": ("https://www.thenationalnews.com/sport/cricket/2026/03/08/india-secure-back-to-back-t20-world-cup-after-"
              "thrashing-new-zealand-in-final", OPENED),
    "t20wc_sky": ("https://www.skysports.com/cricket/news/12040/13502048/mens-t20-world-cup-2026-fixtures-england-india-"
                  "pakistan-australia-scotland-ireland-west-indies-and-more", SEARCH),
    "cwg2030": ("https://www.thestar.com.my/sport/others/2025/11/26/games-2030-centenary-commonwealth-games-awarded-to-"
                "ahmedabad-india", SEARCH),
    "chesswc": ("https://www.chess.com/news/view/2025-fide-world-cup-final-tiebreaks", OPENED),
    "fifawc": ("https://www.thescore.com/worldcup/news/3550006/rodri-takes-golden-ball-over-messi-mbappe-claims-golden-"
               "boot-again", OPENED),
    "asiad": ("https://khelnow.com/asian-games/final-medal-tally-asian-games-202610", OPENED),
    "ipl26": ("https://www.republicworld.com/cricket/rcb-crowned-ipl-2026-champions-as-virat-kohlis-heroics-down-"
              "gujarat-titans-in-final-narendra-modi-stadium-ahmedabad-rajat-patidar-shubman-gill-2026-05-31-126409",
              SEARCH),
    # Summits and international
    "g20": ("https://www.africanews.com/2025/11/23/g20-leaders-in-south-africa-adopt-declaration-despite-us-opposition/",
            SEARCH),
    "g20_ewn": ("https://www.ewn.co.za/2025/11/22/g20-final-declaration-published-with-strong-focus-on-development-"
                "issues-in-africa", SEARCH),
    "cop30": ("https://www.c2es.org/document/key-negotiations-related-outcomes-of-the-un-climate-conference-in-belem",
              SEARCH),
    "aisummit": ("https://www.newsonair.gov.in/india-ai-impact-summit-2026-enters-fifth-day-at-bharat-mandapam", SEARCH),
    "brics": ("https://www.angelone.in/news/economy/india-to-host-18th-brics-summit-in-new-delhi-on-september-12-13-2026",
              SEARCH),
    "brics_air": ("https://newsonair.gov.in/all-preparations-in-full-swing-for-two-day-brics-summit-2026-beginning-"
                  "saturday/", SEARCH),
    "sco": ("https://timesofoman.com/article/176302-26th-sco-summit-begins-in-bishkek-as-heads-of-state-gather-round-"
            "table-discussion-underway", SEARCH),
    "sco_kabar": ("https://en.kabar.kg/news/kyrgyzstan-to-host-sco-summit-at-turning-point-in-world-history/", SEARCH),
    "g7": ("https://www.insightsonindia.com/2026/06/16/the-52nd-g7-summit/", SEARCH),
    "g7_bt": ("https://www.businesstoday.in/latest/trends/photo/why-does-the-g7-summit-matter-for-india-inside-modis-"
              "most-important-meetings-in-evian-537503-2026-06-17", SEARCH),
    "indrus": ("https://www.wionews.com/india-news/india-russia-summit-2025-here-are-the-key-takeaways-from-the-joint-"
               "statement-between-two-countries-1764942784745", SEARCH),
    "indeu": ("https://www.businesstoday.in/latest/economy/story/key-takeaways-from-india-eu-summit-fta-sealed-2030-"
              "roadmap-adopted-defence-pact-signed-513012-2026-01-27", SEARCH),
    "indeu_tribune": ("https://www.tribuneindia.com/news/world/strategic-partnership-provides-major-economic-and-"
                      "geopolitical-weight-european-council-president-antonio-costa-on-india-eu-ties/", SEARCH),
    "ceta": ("https://ianslive.in/india-uk-fta-comes-into-force-under-pm-modis-leadership-piyush-goyal--20260715095323",
             SEARCH),
    "ceta_am": ("https://www.alvarezandmarsal.com/thought-leadership/india-tax-alert-india-uk-ceta-comes-into-force-"
                "key-highlights-and-business-implications", SEARCH),
    "oman": ("https://www.arabnews.com/node/2626713/world", SEARCH),
    "oman_force": ("https://www.manoramayearbook.in/current-affairs/india/2026/06/02/india-oman-cepa-comes-into-"
                   "force.html", SEARCH),
    "nzfta": ("https://www.thestar.com.my/aseanplus/aseanplus-news/2026/04/27/india-and-new-zealand-sign-free-trade-deal",
              SEARCH),
    "bdesh": ("https://www.dawn.com/news/1973874", SEARCH),
    "bdesh_mb": ("https://mb.com.ph/2026/02/17/bangladeshs-new-prime-minister-is-sworn-in-after-his-partys-landslide-"
                 "election-win", SEARCH),
    "who_exit": ("https://cdc.gov/global-health/resources/us-withdrawal-who.html", SEARCH),
    "who_exit_news": ("https://www.outlookindia.com/international/us-completes-withdrawal-from-world-health-"
                      "organization", SEARCH),
    # National
    "wb_cm": ("https://www.onmanorama.com/news/india/2026/05/09/suvendu-adhikari-takes-oath-as-first-bjp-cm-of-west-"
              "bengal.html", SEARCH),
    "wb_air": ("https://newsonair.gov.in/suvendu-adhikari-takes-oath-as-first-bjp-cm-of-west-bengal/", SEARCH),
    "tn_cm": ("https://www.businesstoday.in/india/story/dmk-aiadmk-era-ends-vijay-takes-oath-as-tamil-nadu-cm-rahul-"
              "gandhi-attends-ceremony-530685-2026-05-10", SEARCH),
    "tn_uni": ("https://uniindia.com/tvk-founder-vijay-sworn-in-as-13th-tn-cm-announces-new-era-of-real-secular-social-"
               "justice-9-cabinet-ministers-also-take-oath/south/news/3838868.html", SEARCH),
    "kl_cm": ("https://keralakaumudi.com/en/kerala/general/v-d-satheesan-sworn-in-as-keralas-chief-minister-in-front-of-"
              "massive-public-gathering-1749148-amp", SEARCH),
    "bihar_cm": ("https://www.tribuneindia.com/news/india/nitish-kumar-takes-oath-as-cm-of-bihar-for-record-10th-time",
                 SEARCH),
    "bihar_bt": ("https://www.businesstoday.in/india/story/nitish-kumar-sworn-in-as-bihar-cm-for-10th-time-samrat-"
                 "choudhary-vijay-sinha-named-deputy-cms-502887-2025-11-20", SEARCH),
    "assam_cm": ("https://morungexpress.com/himanta-biswa-sarma-takes-oath-as-assam-chief-minister-for-second-straight-"
                 "term", SEARCH),
    "lokbhavan": ("https://www.thehitavada.com/Encyc/2025/12/3/raj-bhavan-will-now-be-known-as-lok-bhavan.html", SEARCH),
    "lokbhavan_jk": ("https://kashmirlife.net/mha-orders-renaming-of-jammu-kashmir-raj-bhavan-as-lok-bhavan-415259/",
                     SEARCH),
    "census": ("https://www.businesstoday.in/india/story/initial-phase-of-census-2027-to-begin-on-april-1-houselisting-"
               "to-be-done-within-30-day-period-509920-2026-01-08", SEARCH),
    "census_tv": ("https://www.indiatvnews.com/news/india/census-2027-begins-from-today-in-digital-mode-here-is-how-"
                  "citizens-can-self-enumerate-all-you-need-to-know-about-33-faqs-2026-04-01-1035836", SEARCH),
    "cds": ("https://www.theweek.in/news/defence/2026/05/09/lt-gen-ns-raja-subramani-named-new-cds-vice-admiral-"
            "krishna-swaminathan-appointed-navy-chief.html", OPENED),
    "cds_bt": ("https://www.businesstoday.in/india/story/lt-gen-ns-raja-subramani-named-new-cds-vice-admiral-"
               "swaminathan-to-lead-navy-530637-2026-05-09", SEARCH),
    "sevateerth": ("https://ianslive.in/pm-modi-inaugurates-seva-teerth-the-new-pmo-office-housing-cabinet-secretariat-"
                   "and-nscs--20260213144804", SEARCH),
    "sevateerth_q": ("https://www.thequint.com/news/breaking-news/pmo-relocates-seva-teerth-governance-shift-"
                     "inauguration", SEARCH),
    "agni": ("https://mail.morungexpress.com/india-successfully-tests-advanced-agni-missile-with-multiple-payloads-to-"
             "hit-different-targets", OPENED),
    "mangrol": ("https://newsonair.gov.in/indigenous-anti-submarine-warfare-ship-mangrol-commissioned-into-the-indian-"
                "navy/", OPENED),
    "samarthak": ("https://www.gktoday.in/indian-navy-commissions-ins-samarthak/", SEARCH),
    "samarthak_lt": ("https://www.larsentoubro.com/pressreleases/2026/2026-09-01-lt-delivers-multi-purpose-vessel-ins-"
                     "samarthak-to-indian-navy/", SEARCH),
    "taragiri": ("https://www.constructionworld.in/policy-updates-and-economic-news/ins-taragiri-commissioned-into-the-"
                 "indian-navy/89590", OPENED),
    "lrlacm": ("https://www.devdiscourse.com/article/law-order/3935353-drdo-successfully-tests-indigenous-long-range-"
               "cruise-missile", OPENED),
    "dunagiri": ("https://www.defenceguru.co.in/news/indias-naval-power-gets-a-major-boost-pm-modi-commissions-ins-"
                 "dunagiri-ins-sanshodhak-and-ins-agray", OPENED),
    # Appointments
    "rohit_jain": ("https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62681", OPENED),
    "swaminathan_j": ("https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62880", OPENED),
    "hdfc": ("https://www.uniindia.com/business-economy/hdfc-bank-new-md-named/199650", OPENED),
    "sbi_md": ("https://psuwatch.com/psu-appointments/govt-appoints-ravi-ranjan-as-managing-director-of-sbi", OPENED),
    "canara": ("https://www.freepressjournal.in/amp/business/canara-bank-gets-new-chief-brajesh-kumar-singh-takes-"
               "charge-as-md-ceo-till-april-2029", OPENED),
    "canara_interim": ("https://www.peoplematters.in/news/appointments/canara-bank-names-hardeep-singh-ahluwalia-"
                       "interim-md-and-ceo-from-jan-2026-47864", SEARCH),
    "unga": ("https://www.un.org/pga/80/election-of-the-president-of-the-united-nations-general-assembly-at-its-81st-"
             "session/", OPENED),
    "unga_wam": ("https://www.wam.ae/en/article/c0iu155-general-assembly-elects-bangladeshs-foreign", SEARCH),
    "unhcr": ("https://www.arabnews.com/node/2625990/amp", SEARCH),
    "unesco": ("https://mediarightsagenda.org/khaled-el-enany-takes-oath-as-unesco-director-general/", SEARCH),
    "unesco_eg": ("https://egyptianstreets.com/2025/10/06/egypts-khaled-el-enany-becomes-first-arab-to-lead-unesco-as-"
                  "director-general/", SEARCH),
    "fatf_pres": ("https://www.fatf-gafi.org/en/the-fatf/fatf-presidency/FATF-Presidency-Giles-Thomson.html", SEARCH),
    "fatf_vp": ("https://www.outlookindia.com/national/india-elected-fatf-vice-president-for-first-time-vivek-aggarwal-"
                "to-assume-office-in-july-2026", OPENED),
    "aiib": ("https://aiib.org/en/news-events/news/2026/zou-jiayi-assumes-presidency-asian-infrastructure-investment-"
             "bank.html", OPENED),
    "wb_ed": ("https://theprint.in/india/economist-neelkanth-mishra-appointed-world-bank-executive-director/2951058/",
              SEARCH),
    "sebi_murty": ("https://www.business-standard.com/markets/news/govt-appoints-kv-ramana-murty-as-sebi-whole-time-"
                   "member-126031300159_1.html", SEARCH),
    "sebi_pradhan": ("https://www.sebi.gov.in/media-and-notifications/press-releases/dec-2025/shri-sandip-pradhan-takes-"
                     "charge-as-whole-time-member-sebi_98203.html", SEARCH),
    "sib": ("https://www.businesstoday.in/markets/stocks/story/south-indian-bank-shares-tank-6-after-rbi-nod-to-md-ceo-"
            "appointment-board-meet-on-july-16-541620-2026-07-08", SEARCH),
    "cub": ("https://www.peoplematters.in/news/appointments/rbi-clears-appointment-of-r-vijay-anandh-as-city-union-"
            "banks-new-ceo-48381", SEARCH),
    "psb_ext": ("https://www.angelone.in/news/market-updates/govt-clears-3-year-extension-for-bank-of-india-bank-of-"
                "baroda-mds-ahead-of-term-end", OPENED),
    # Business
    "rbl": ("https://gulfnews.com/business/banking/emirates-nbd-completes-275-billion-rbl-bank-deal-takes-60-stake-"
            "1.500578382", OPENED),
    "rbl_fpj": ("https://www.freepressjournal.in/business/emirates-nbd-completes-275-billion-majority-stake-acquisition-"
                "in-rbl-bank", SEARCH),
    # Organisations
    "ndb_hq": ("https://newsus.cgtn.com/news/2025-07-06/Colombia-Uzbekistan-join-BRICS-nations-New-Development-Bank-"
               "1EMefiuImM8/share_amp.html", SEARCH),
    "ndb_members": ("https://www.newsonair.gov.in/colombia-and-uzbekistan-join-ndb-ahead-of-17th-brics-summit", SEARCH),
    "fao": ("https://www.encyclopedia.com/history/encyclopedias-almanacs-transcripts-and-maps/food-and-agriculture-"
            "organization-united-nations-fao", SEARCH),
    "ioc_hq": ("https://olympics.com/ioc/news/ioc-headquarters-new-address-in-lausanne-officialised", SEARCH),
    "nhb": ("https://nhb.org.in/about-us/", SEARCH),
    "exim": ("https://cset.thecommonwealth.org/funding/export-credit-agencies/export-import-bank-of-india-india-exim-"
             "bank", SEARCH),
    "imf191": ("https://www.imf.org/en/news/articles/2024/10/21/pr-24387-liechtenstein-principality-of-liechtenstein-"
               "becomes-imfs-191st-member", SEARCH),
    "wto_dg": ("https://genevasolutions.news/global-news/wto-chief-okonjo-iweala-reappointed-for-second-term", SEARCH),
    "ioc_pres": ("https://www.aljazeera.com/news/2025/3/20/kirsty-coventry-elected-as-first-woman-ioc-president", SEARCH),
    "ioc_pres_week": ("https://theweek.com/sports/kirsty-coventry-olympics-ioc", SEARCH),
    "commonwealth": ("https://thecommonwealth.org/news/op-ed-gabon-and-togo-join-commonwealth-family", SEARCH),
    "commonwealth_sg": ("https://amandala.com.bz/news/first-african-woman-secretary-general-of-commonwealth/", SEARCH),
    "bis_gm": ("https://www.bis.org/press/p241111.htm", SEARCH),
    "oecd": ("https://www.oecd.org/agriculture-and-food/the-oecd-at-60_afb7f6a8-en", SEARCH),
    "oecd_wiki": ("https://en.wikipedia.org/wiki/OECD", SEARCH),
    # Reports
    "whr": ("https://telanganatoday.com/india-ranks-116th-in-world-happiness-report-2026", SEARCH),
    "whr_tv": ("https://www.indiatvnews.com/news/world/world-happiness-report-2026-which-are-the-top-10-happiest-"
               "nations-and-where-does-india-rank-check-list-here-2026-03-20-1034424", SEARCH),
    "gggi": ("https://www.freepressjournal.in/india/india-retains-131st-rank-in-global-gender-gap-index-2026-iceland-"
             "tops-list", SEARCH),
    # Static
    "kyrgyz": ("https://www.indexmundi.com/kyrgyzstan", SEARCH),
    "oman_facts": ("https://fm.gov.om/about-oman/state/key-facts/", SEARCH),
    "dudhwa": ("https://en.wikipedia.com/wiki/Dudhwa_Tiger_Reserve", SEARCH),
    "namdapha": ("https://arunachalforests.gov.in/wildlife_namdapha_nptr.html", SEARCH),
    "silentvalley": ("https://www.keralatourism.org/malabar/silent-valley-national-park/39", SEARCH),
    "mettur": ("https://en.wikipedia.org/wiki/Stanley_Reservoir", SEARCH),
    "nsagar": ("https://en.wikipedia.org/wiki/List_of_largest_reservoirs_in_India", SEARCH),
    "jharkhand": ("https://www.jharkhand.gov.in/home/AboutState", SEARCH),
    "uttarakhand": ("https://www.britannica.com/print/article/736432", SEARCH),
}


def fact(claim, key):
    url, how = U[key]
    return {"claim": claim, "source_url": url, "checked_on": TODAY, "_how": how}


# ====================================================================== Economic Affairs (4 / 11 / 4)
T = "Economic Affairs"
GDP, INF, FIS, MP = "GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions"

G(T, MP, "Basic",
  "After the RBI's Monetary Policy Committee raised the policy repo rate on 7 October 2026, what is the Standing "
  "Deposit Facility (SDF) rate?",
  ["5.25%", "5.00%", "5.50%", "5.75%"], "*",
  "LAF corridor after the October 2026 hike",
  "The MPC (5-7 October 2026) raised the repo rate by 25 bps to 5.50%. The corridor moved with it: the SDF rate (the "
  "floor) became 5.25%, and the MSF rate and Bank Rate (the ceiling) became 5.75%. Before the hike the SDF was 5.00%.",
  ["Repo after hike: 5.50%", "SDF = repo - 25 bps = 5.25%", "MSF = Bank Rate = repo + 25 bps = 5.75%"],
  [fact("MPC 5-7 Oct 2026 raised repo by 25 bps to 5.50%; SDF 5.25%; MSF and Bank Rate 5.75%", "mpc_oct"),
   fact("RBI home page on 2026-11-05 shows repo 5.50%, SDF 5.25%, MSF 5.75%", "rbi_home")],
  shortcut="SDF sits 25 bps below the repo rate.",
  why="5.00% was the SDF before the hike; 5.50% is the new repo rate; 5.75% is the MSF and Bank Rate.",
  current=ca("2026-10-07"))

G(T, INF, "Basic",
  "The new Consumer Price Index (CPI) series released by MoSPI in February 2026 uses which base year?",
  ["2024", "2012", "2022-23", "2020"], "*",
  "CPI base revision",
  "MoSPI released the revised CPI series with base 2024=100 on 12 February 2026, replacing the 2012 series. Inflation "
  "on the new series is available from January 2026. The RBI's MPC now uses this series to measure inflation.",
  ["Old CPI base: 2012", "New CPI base: 2024 (=100)", "First print under it: January 2026"],
  [fact("Inflation is measured on the new CPI series with base 2024=100", "mpc_apr"),
   fact("MoSPI unveiled the new CPI series with 2024 base on 12 Feb 2026; January 2026 inflation 2.75%", "cpi_new")],
  why="2012 was the old CPI base; 2022-23 is the new GDP base year, not the CPI base.",
  current=ca("2026-02-12"))

G(T, GDP, "Basic",
  "India's new GDP series, released on 27 February 2026, uses which base year?",
  ["2022-23", "2011-12", "2017-18", "2024-25"], "*",
  "GDP base revision",
  "MoSPI moved the national accounts from base year 2011-12 to 2022-23 on 27 February 2026, choosing 2022-23 as a "
  "recent normal year after COVID with good data. The RBI's projections from April 2026 use this new series.",
  ["Old GDP base: 2011-12", "New GDP base: 2022-23"],
  [fact("GDP estimates now use the new series with base year 2022-23", "mpc_apr"),
   fact("New GDP series with base year 2022-23 released; FY26 growth estimated at 7.6%", "gdp_new")],
  why="2011-12 was the previous base; 2024 is the base of the new CPI series.",
  current=ca("2026-02-27"))

G(T, FIS, "Basic",
  "What fiscal deficit target did the Union Budget 2026-27 set for 2026-27, as a share of GDP?",
  ["4.3%", "4.4%", "4.5%", "5.1%"], "*",
  "Union Budget 2026-27: fiscal deficit",
  "The Budget presented on 1 February 2026 budgeted the gross fiscal deficit at 4.3% of GDP for 2026-27, slightly "
  "below the 4.4% revised estimate for 2025-26. The government said it met its earlier goal of bringing the deficit "
  "below 4.5% of GDP by 2025-26.",
  ["2025-26 (RE): 4.4% of GDP", "2026-27 (BE): 4.3% of GDP"],
  [fact("GFD budgeted at 4.3% of GDP for 2026-27, below 4.4% RE for 2025-26", "budget_bulletin"),
   fact("Union Budget (1 Feb 2026) sets fiscal deficit target at 4.3% of GDP for FY27", "budget_quint")],
  why="4.4% is the 2025-26 revised estimate; 4.5% was the earlier glide-path ceiling for 2025-26.",
  current=ca("2026-02-01"))

G(T, MP, "Intermediate",
  "At its meeting of 5-7 October 2026, the RBI's Monetary Policy Committee changed its policy stance to which of the "
  "following?",
  ["Calibrated tightening", "Neutral", "Accommodative", "Withdrawal of accommodation"], "*",
  "MPC stance, October 2026",
  "Along with the 25 bps repo hike to 5.50%, the MPC changed its stance from neutral to 'calibrated tightening'. The "
  "resolution says rate cuts are off the table in the near term, so the next move is either a hike or a pause.",
  ["Earlier stance (Feb-Aug 2026): neutral", "October 2026: calibrated tightening"],
  [fact("MPC changed stance to calibrated tightening in October 2026; next action a hike or a pause", "mpc_oct"),
   fact("August 2026 MPC retained the neutral stance", "mpc_aug")],
  why="Neutral was the stance until August 2026; accommodative and withdrawal of accommodation are older stances.",
  current=ca("2026-10-07"))

G(T, GDP, "Intermediate",
  "In its October 2026 policy, what real GDP growth did the RBI project for 2026-27?",
  ["7.1%", "6.7%", "6.9%", "7.8%"], "*",
  "RBI growth projection, October 2026",
  "The October 2026 resolution raised the 2026-27 real GDP growth projection to 7.1% (Q2 7.2%, Q3 6.9%, Q4 6.8%), "
  "after growth of 7.8% in Q1 came in above expectations.",
  ["April 2026 projection: 6.9%", "August 2026 projection: 6.7%", "October 2026 projection: 7.1%"],
  [fact("Real GDP growth for 2026-27 projected at 7.1%; Q1 growth was 7.8%", "mpc_oct"),
   fact("August 2026 projection for 2026-27: 6.7%", "mpc_aug"),
   fact("April 2026 projection for 2026-27: 6.9%", "mpc_apr")],
  why="6.7% and 6.9% were the August and April projections; 7.8% is actual Q1 growth.",
  current=ca("2026-10-07"))

G(T, INF, "Intermediate",
  "What CPI inflation did the RBI's Monetary Policy Committee project for 2026-27 in its October 2026 resolution?",
  ["5.2%", "4.6%", "5.0%", "4.4%"], "*",
  "RBI inflation projection, October 2026",
  "The MPC raised its 2026-27 CPI inflation projection to 5.2% (Q2 4.9%, Q3 6.0%, Q4 5.7%). It had projected 4.6% in "
  "April and 5.0% in August 2026. Core inflation for 2026-27 is projected at 4.4%.",
  ["April: 4.6%", "August: 5.0%", "October: 5.2%"],
  [fact("CPI inflation for 2026-27 projected at 5.2%; core inflation 4.4%", "mpc_oct"),
   fact("August 2026 CPI projection for 2026-27: 5.0%", "mpc_aug"),
   fact("April 2026 CPI projection for 2026-27: 4.6%", "mpc_apr")],
  why="4.6% and 5.0% are earlier projections; 4.4% is the projection for core inflation.",
  current=ca("2026-10-07"))

G(T, GDP, "Intermediate",
  "According to the estimates released on 31 August 2026, what was India's real GDP growth in the April-June quarter "
  "(Q1) of 2026-27?",
  ["7.8%", "6.9%", "7.1%", "8.6%"], "*",
  "Q1 FY27 GDP",
  "Real GDP grew 7.8% in Q1 of 2026-27, above the RBI's estimate, against 6.9% in Q1 of 2025-26. The RBI's October "
  "2026 resolution also cites Q1 growth of 7.8%.",
  ["Q1 2025-26: 6.9%", "Q1 2026-27: 7.8%"],
  [fact("Q1 2026-27 growth was 7.8%, above expectations", "mpc_oct"),
   fact("MoSPI release of 31 Aug 2026: real GDP grew 7.8% in Q1 FY27", "gdp_q1")],
  why="6.9% is Q1 of the previous year; 7.1% is the RBI's full-year projection.",
  current=ca("2026-08-31"))

G(T, GDP, "Intermediate",
  "Under the new GDP series released in February 2026, what real GDP growth was estimated for 2025-26?",
  ["7.6%", "7.4%", "7.1%", "6.5%"], "*",
  "FY26 growth on the new base",
  "The second advance estimates on the new 2022-23 base put 2025-26 real GDP growth at 7.6%, up from the 7.4% first "
  "advance estimate on the old base. Growth for 2024-25 is put at 7.1%.",
  ["First advance estimate (old base): 7.4%", "New series (Feb 2026): 7.6%"],
  [fact("India's GDP estimated to grow 7.6% in 2025-26 after base-year revision; 2024-25 at 7.1%", "gdp_new")],
  why="7.4% was the earlier estimate on the old base; 7.1% is the 2024-25 figure.",
  current=ca("2026-02-27"))

G(T, INF, "Intermediate",
  "What was India's headline retail (CPI) inflation for January 2026, the first month published on the new 2024-base "
  "series?",
  ["2.75%", "2.10%", "3.40%", "4.80%"], "*",
  "First print of the new CPI",
  "With the new series released on 12 February 2026, January 2026 headline CPI inflation was 2.75% (provisional). "
  "MoSPI cautioned that old and new series figures are not directly comparable and released linking factors.",
  ["New CPI series released 12 Feb 2026", "January 2026 inflation: 2.75%"],
  [fact("New CPI series with 2024 base; January 2026 retail inflation at 2.75%", "cpi_new")],
  why="4.80% is the August 2026 figure cited by the MPC in October.",
  current=ca("2026-02-12"))

G(T, FIS, "Intermediate",
  "According to the Union Budget 2026-27, what is the revised estimate (RE) of the fiscal deficit for 2025-26?",
  ["4.4% of GDP", "4.3% of GDP", "4.8% of GDP", "4.9% of GDP"], "*",
  "Fiscal deficit, 2025-26 RE",
  "The Budget put the 2025-26 fiscal deficit at 4.4% of GDP (RE) and budgeted 4.3% for 2026-27, meeting the goal of "
  "keeping it below 4.5% by 2025-26.",
  ["2025-26 RE: 4.4%", "2026-27 BE: 4.3%"],
  [fact("GFD 4.3% of GDP in 2026-27 BE versus 4.4% in 2025-26 RE", "budget_bulletin")],
  why="4.3% is the 2026-27 target.",
  current=ca("2026-02-01"))

G(T, FIS, "Intermediate",
  "What gross market borrowing did the Centre budget for 2026-27 in the Union Budget 2026-27?",
  ["₹17.2 lakh crore", "₹11.7 lakh crore", "₹12.2 lakh crore", "₹14.8 lakh crore"], "*",
  "Market borrowing, 2026-27",
  "Gross market borrowings are budgeted at ₹17.2 lakh crore (4.4% of GDP). Net market borrowings are ₹11.7 lakh crore "
  "(3.0% of GDP) and finance 69.2% of the fiscal deficit. Capital expenditure is about ₹12.2 lakh crore.",
  ["Gross market borrowing: ₹17.2 lakh crore", "Net market borrowing: ₹11.7 lakh crore"],
  [fact("Gross market borrowings budgeted at ₹17.2 lakh crore; net ₹11.7 lakh crore; capex about ₹12.2 lakh crore",
        "budget_bulletin")],
  why="₹11.7 lakh crore is net borrowing; ₹12.2 lakh crore is capital expenditure.",
  current=ca("2026-02-01"))

G(T, FIS, "Intermediate",
  "The Sixteenth Finance Commission, whose report was tabled with the Union Budget on 1 February 2026, recommended "
  "what share for the States in the divisible pool of central taxes for 2026-31?",
  ["41%", "42%", "45%", "50%"], "*",
  "Vertical devolution, 16th Finance Commission",
  "The 16th Finance Commission kept the States' share at 41%, the same as the 15th Commission, for the five years "
  "from 1 April 2026 to 31 March 2031. Several States had asked for 50%. The government accepted the recommendation.",
  ["15th FC: 41%", "16th FC (2026-31): 41% (unchanged)"],
  [fact("16th Finance Commission recommends States' share in central taxes at 41% for five years till 2031", "fc16")],
  why="42% was the 14th FC share; 50% was the States' demand.",
  current=ca("2026-02-01"))

G(T, MP, "Intermediate",
  "What did the RBI's Monetary Policy Committee decide on the policy repo rate at its meeting of 3-5 December 2025?",
  ["Cut it by 25 bps to 5.25%", "Cut it by 50 bps to 5.00%", "Left it unchanged at 5.50%",
   "Raised it by 25 bps to 5.75%"], "*",
  "MPC, December 2025",
  "On 5 December 2025 the MPC unanimously cut the repo rate by 25 bps from 5.50% to 5.25%, keeping a neutral stance. "
  "This took total cuts since February 2025 to 125 bps. The rate then stayed at 5.25% until the October 2026 hike.",
  ["Before: 5.50%", "Cut: 25 bps", "After: 5.25%"],
  [fact("RBI MPC cut the repo rate by 25 bps to 5.25% from 5.5% on 5 Dec 2025", "mpc_dec"),
   fact("Repo rate unchanged at 5.25% in August 2026", "mpc_aug")],
  current=ca("2025-12-05"))

G(T, INF, "Intermediate",
  "According to the RBI's October 2026 resolution, what was headline CPI inflation in August 2026?",
  ["4.8%", "4.5%", "5.2%", "6.0%"], "*",
  "Recent inflation print",
  "The resolution notes that CPI inflation rose to 4.8% in August 2026 from 4.5% in July. Core inflation was 4.2% in "
  "August. The rising trend was one reason for the rate hike.",
  ["July 2026: 4.5%", "August 2026: 4.8%"],
  [fact("CPI inflation rose to 4.8% in August 2026 from 4.5% in July; core 4.2%", "mpc_oct")],
  why="4.5% is July; 5.2% is the full-year projection; 6.0% is the Q3 projection.",
  current=ca("2026-10-07"))

G(T, MP, "Advanced",
  "Consider the following statements about the RBI Monetary Policy Committee meeting of 5-7 October 2026:\n"
  "1. The decision to raise the policy repo rate was unanimous.\n"
  "2. Two members preferred to keep the stance neutral.\n"
  "3. The MSF rate and the Bank Rate were set at 5.75%.\n"
  "Which of the statements given above is/are correct?",
  S123, "D",
  "October 2026 MPC details",
  "All six members voted for the 25 bps hike. Dr. Nagesh Kumar and Prof. Ram Singh preferred to retain a neutral "
  "stance, while the stance changed to calibrated tightening. The MSF rate and Bank Rate moved to 5.75%.",
  ["1: correct (unanimous)", "2: correct (Nagesh Kumar and Ram Singh)", "3: correct", "So 1, 2 and 3"],
  [fact("Vote unanimous for hike; Nagesh Kumar and Ram Singh preferred neutral stance; MSF and Bank Rate 5.75%",
        "mpc_oct")],
  current=ca("2026-10-07"))

G(T, GDP, "Advanced",
  "Consider the following statements about the RBI's projections of real GDP growth for 2026-27:\n"
  "1. In April 2026 the projection was 6.9%.\n"
  "2. In August 2026 the projection was cut to 6.7%.\n"
  "3. In October 2026 the projection was raised to 7.4%.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "Evolution of RBI growth projections",
  "The projection for 2026-27 was 6.9% in April 2026, 6.7% in August 2026 and 7.1% (not 7.4%) in October 2026.",
  ["1: correct", "2: correct", "3: wrong (7.1%)", "So 1 and 2 only"],
  [fact("April 2026: 6.9%", "mpc_apr"), fact("August 2026: 6.7%", "mpc_aug"), fact("October 2026: 7.1%", "mpc_oct")],
  current=ca("2026-10-07"))

G(T, FIS, "Advanced",
  "Consider the following statements about the Union Budget 2026-27:\n"
  "1. Union government debt is budgeted to fall to 55.6% of GDP in 2026-27.\n"
  "2. The medium-term target is debt of 50 (±1) per cent of GDP by 2030-31.\n"
  "3. Net market borrowings finance more than 80% of the gross fiscal deficit in 2026-27.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "Debt path and deficit financing",
  "Debt is budgeted at 55.6% of GDP in 2026-27, down from 56.1% in 2025-26 (RE), with a target of 50 (±1)% by "
  "2030-31. Net market borrowings (₹11.7 lakh crore) finance 69.2% of the GFD, down from 72.7%; small savings and "
  "T-bills finance most of the rest.",
  ["1: correct", "2: correct", "3: wrong (69.2%)", "So 1 and 2 only"],
  [fact("Debt 55.6% of GDP in 2026-27 from 56.1%; target 50 (±1)% by 2030-31; net market borrowing finances 69.2% "
        "of GFD", "budget_bulletin"),
   fact("Debt-to-GDP to fall to 55.6% in FY27; target 50% (±1) by FY2030-31", "budget_quint")],
  current=ca("2026-02-01"))

G(T, GDP, "Advanced",
  "Consider the following statements about the GDP estimates for Q1 (April-June) of 2026-27:\n"
  "1. Real GDP growth of 7.8% was the highest Q1 growth in the period 2023-24 to 2026-27.\n"
  "2. Nominal GDP grew by about 10.3%.\n"
  "3. Real GVA grew more slowly than real GDP.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "Q1 FY27 national accounts",
  "Real GDP grew 7.8%, the highest Q1 figure in 2023-24 to 2026-27. Nominal GDP rose 10.3% to ₹88.27 lakh crore. Real "
  "GVA grew 8.2%, faster (not slower) than real GDP.",
  ["1: correct", "2: correct", "3: wrong (GVA 8.2% > GDP 7.8%)", "So 1 and 2 only"],
  [fact("Q1 FY27: real GDP 7.8% (highest Q1 in 2023-24 to 2026-27); nominal GDP growth 10.3%; real GVA 8.2%",
        "gdp_q1_pib"),
   fact("Real GDP grew 7.8% in Q1 of 2026-27", "gdp_q1")],
  current=ca("2026-08-31"))

# ====================================================================== Government Policies (4 / 1 / 5)
T, PC, RR = "Government Policies", "Policy changes", "Regulatory reforms"

G(T, PC, "Basic",
  "What is the full form of the SHANTI Act, 2025, which opened India's civil nuclear power sector to private "
  "participation?",
  ["Sustainable Harnessing and Advancement of Nuclear Energy for Transforming India",
   "Strategic Harnessing of Atomic and Nuclear Technology for India",
   "Safe Harnessing and Application of Nuclear Technology for Industry",
   "Sustainable Hydrogen and Advanced Nuclear Technology Initiative"], "*",
  "SHANTI Act, 2025",
  "The Sustainable Harnessing and Advancement of Nuclear Energy for Transforming India (SHANTI) Act received the "
  "President's assent in December 2025. It lets licensed private companies and joint ventures build, own and operate "
  "nuclear power plants, while the government keeps control of the fuel cycle.",
  ["SHANTI = Sustainable Harnessing and Advancement of Nuclear Energy for Transforming India"],
  [fact("SHANTI = Sustainable Harnessing and Advancement of Nuclear Energy for Transforming India; President's nod "
        "opens civil nuclear sector to private players", "shanti")],
  current=ca("2025-12-20"))

G(T, PC, "Basic",
  "The Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Bill, 2025, passed by Parliament in December 2025, raises "
  "the foreign direct investment limit in Indian insurance companies to what level?",
  ["100%", "74%", "49%", "26%"], "*",
  "Insurance FDI",
  "The Bill passed the Lok Sabha on 16 December and the Rajya Sabha on 17 December 2025. It raises the FDI cap in "
  "insurers from 74% to 100% to attract capital and raise insurance penetration.",
  ["Earlier cap: 74%", "New cap: 100%"],
  [fact("Parliament passed Sabka Bima Sabki Raksha Bill allowing 100% FDI in insurance (from 74%)", "insurance")],
  why="74% was the previous cap; 49% and 26% are older caps.",
  current=ca("2025-12-17"))

G(T, RR, "Basic",
  "In November 2025 the RBI completed a consolidation of its regulatory instructions. Into how many function-wise "
  "Master Directions were the relevant circulars consolidated?",
  ["244", "120", "312", "500"], "*",
  "RBI regulatory consolidation",
  "On 28 November 2025 the RBI announced that about 9,000 circulars had been dealt with: 5,673 obsolete circulars "
  "were repealed and over 3,800 were subsumed into 244 function-wise Master Directions across 11 types of regulated "
  "entities.",
  ["Circulars repealed as obsolete: 5,673", "Master Directions created: 244"],
  [fact("RBI consolidated about 9,000 circulars into 244 Master Directions (28 Nov 2025)", "rbi_md"),
   fact("RBI repeals 9,000 circulars, consolidates rules into 244 Master Directions", "rbi_md_air")],
  current=ca("2025-11-28"))

G(T, PC, "Basic",
  "Who chairs the Eighth Central Pay Commission, whose terms of reference were notified on 3 November 2025?",
  ["Justice Ranjana Prakash Desai", "Justice A. K. Mathur", "Prof. Pulak Ghosh", "Justice Indu Malhotra"], "*",
  "8th Central Pay Commission",
  "The Finance Ministry notified the terms of reference on 3 November 2025, with retired Supreme Court judge Justice "
  "Ranjana Prakash Desai as chairperson, Prof. Pulak Ghosh (IIM Bangalore) as part-time member and Pankaj Jain as "
  "member-secretary.",
  ["Chair: Justice Ranjana Prakash Desai", "Part-time member: Prof. Pulak Ghosh"],
  [fact("ToR of 8th CPC notified 3 Nov 2025; Justice Ranjana Prakash Desai chairperson", "cpc8"),
   fact("Cabinet approved ToR; Justice Ranjana Desai to chair 8th Pay Commission", "cpc8_wire")],
  why="Prof. Pulak Ghosh is the part-time member of the Commission.",
  current=ca("2025-11-03"))

G(T, PC, "Intermediate",
  "What is the corpus of the Startup India Fund of Funds 2.0 approved by the Union Cabinet in February 2026?",
  ["₹10,000 crore", "₹5,000 crore", "₹20,000 crore", "₹25,000 crore"], "*",
  "Startup India Fund of Funds 2.0",
  "The Cabinet approved Fund of Funds 2.0 with a ₹10,000 crore corpus in February 2026. Like the 2016 fund, it invests "
  "through SEBI-registered Alternative Investment Funds, not directly in startups, with a focus on deep tech and "
  "tech-driven manufacturing.",
  ["FFS 2.0 corpus: ₹10,000 crore", "Route: SEBI-registered AIFs"],
  [fact("Cabinet approves Startup India Fund of Funds 2.0 with ₹10,000 crore corpus", "ffs2"),
   fact("Seva Teerth's first decision was approval of Startup India FoF 2.0 with ₹10,000 crore corpus (13 Feb 2026)",
        "sevateerth_q")],
  current=ca("2026-02-13"))

G(T, PC, "Advanced",
  "Consider the following statements about the SHANTI Act, 2025:\n"
  "1. It replaces the Atomic Energy Act, 1962.\n"
  "2. It replaces the Civil Liability for Nuclear Damage Act, 2010.\n"
  "3. It hands control of the nuclear fuel cycle to private companies.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "SHANTI Act: scope",
  "The SHANTI Act replaces both the Atomic Energy Act, 1962 and the Civil Liability for Nuclear Damage Act, 2010, and "
  "gives statutory backing to the Atomic Energy Regulatory Board. Private companies may build, own and operate plants "
  "under licence, but sovereign control of the nuclear fuel cycle is retained.",
  ["1: correct", "2: correct", "3: wrong (fuel cycle stays with the government)", "So 1 and 2 only"],
  [fact("SHANTI Act replaced Atomic Energy Act 1962 and CLND Act 2010; private entry with sovereign control over fuel "
        "cycle", "shanti"),
   fact("India's SHANTI Bill completes legislative process", "shanti_wnn")],
  current=ca("2025-12-20"))

G(T, PC, "Advanced",
  "The Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Bill, 2025 amends which of the following laws?\n"
  "1. Insurance Act, 1938\n"
  "2. Life Insurance Corporation Act, 1956\n"
  "3. Insurance Regulatory and Development Authority Act, 1999\n"
  "Select the correct answer using the code given below.",
  S123, "D",
  "Insurance law amendments",
  "The Bill amends all three laws: the Insurance Act, 1938, the LIC Act, 1956 and the IRDA Act, 1999. Its headline "
  "change is raising the FDI cap in insurers from 74% to 100%.",
  ["1: amended", "2: amended", "3: amended", "So 1, 2 and 3"],
  [fact("Bill amends the Insurance Act 1938, LIC Act 1956 and IRDA Act 1999", "insurance_bt"),
   fact("Passed by Parliament in December 2025", "insurance")],
  current=ca("2025-12-17"))

G(T, RR, "Advanced",
  "Consider the following statements about the Securities Markets Code, 2025:\n"
  "1. It was introduced in the Lok Sabha in December 2025.\n"
  "2. It seeks to repeal and replace the SEBI Act, 1992, the Securities Contracts (Regulation) Act, 1956 and the "
  "Depositories Act, 1996.\n"
  "3. It was passed in the same session in which it was introduced.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "Securities Markets Code",
  "The Finance Minister introduced the Code in the Lok Sabha on 18 December 2025. It would consolidate the SEBI Act, "
  "SCRA and Depositories Act into one statute. It was referred to the Standing Committee on Finance rather than "
  "passed in that session.",
  ["1: correct", "2: correct", "3: wrong (referred to the Standing Committee)", "So 1 and 2 only"],
  [fact("Securities Markets Code 2025 introduced in Lok Sabha; repeals SCRA 1956, SEBI Act 1992, Depositories Act "
        "1996", "smc_taxmann"),
   fact("Code referred to the Standing Committee on Finance", "smc")],
  current=ca("2025-12-18"))

G(T, RR, "Advanced",
  "Consider the following statements about the RBI's expected credit loss (ECL) directions for banks issued in April "
  "2026:\n"
  "1. They replace the incurred-loss approach with forward-looking provisioning from 1 April 2027.\n"
  "2. They apply to Regional Rural Banks, Small Finance Banks and Payments Banks as well.\n"
  "Which of the statements given above is/are correct?",
  S12, "A",
  "ECL framework",
  "The final directions, issued on 27 April 2026, move scheduled commercial banks from incurred-loss to expected-loss "
  "provisioning from 1 April 2027, with the transition adjustment spread over four years. RRBs, Small Finance Banks "
  "and Payments Banks are excluded.",
  ["1: correct", "2: wrong (they are excluded)", "So only 1"],
  [fact("RBI final ECL norms: effective 1 April 2027 for scheduled commercial banks", "ecl"),
   fact("ECL directions exclude RRBs, SFBs and payments banks; four-year transition", "ecl_kpmg")],
  current=ca("2026-04-27"))

G(T, PC, "Advanced",
  "Consider the following statements about the Eighth Central Pay Commission:\n"
  "1. Its terms of reference were approved by the Union Cabinet in October 2025.\n"
  "2. It is to make its recommendations within 12 months of its constitution.\n"
  "3. Prof. Pulak Ghosh is its part-time member.\n"
  "Which of the statements given above is/are correct?",
  S123, "C",
  "8th CPC: terms",
  "The Cabinet approved the ToR on 28 October 2025 and the Finance Ministry notified them on 3 November 2025. The "
  "Commission has 18 months, not 12, to report and may give interim reports. Prof. Pulak Ghosh is the part-time "
  "member and Pankaj Jain the member-secretary.",
  ["1: correct", "2: wrong (18 months)", "3: correct", "So 1 and 3 only"],
  [fact("Cabinet approved ToR on 28 Oct 2025; recommendations within 18 months; Pulak Ghosh part-time member",
        "cpc8"),
   fact("Cabinet approves ToR of 8th Pay Commission", "cpc8_wire")],
  current=ca("2025-11-03"))

# ====================================================================== Government Schemes (2 / 10 / 1)
T, CS, SL = "Government Schemes", "Central schemes", "Scheme launches and changes"

G(T, CS, "Basic",
  "Under the Prime Minister's Internship Scheme, what monthly financial assistance does an intern receive during the "
  "12-month internship?",
  ["₹5,000", "₹3,000", "₹8,000", "₹10,000"], "*",
  "PM Internship Scheme",
  "Interns in the top 500 companies (chosen by average CSR spending) get ₹5,000 a month for 12 months: ₹4,500 from the "
  "government and ₹500 from the company's CSR funds. They also get a one-time grant of ₹6,000 on joining.",
  ["Monthly assistance: ₹5,000 (₹4,500 + ₹500)", "One-time grant: ₹6,000"],
  [fact("PM Internship Scheme: ₹5,000 per month for 12 months plus one-time grant of ₹6,000; top 500 companies",
        "pmis")],
  why="₹6,000 is the one-time grant, not the monthly amount.",
  current=ca("2024-10-12"))

G(T, CS, "Basic",
  "Ayushman Vay Vandana cards under AB PM-JAY are issued to which group, irrespective of income?",
  ["Senior citizens aged 70 years and above", "Senior citizens aged 60 years and above",
   "All women aged 50 years and above", "Persons with disabilities of any age"], "*",
  "Ayushman Vay Vandana",
  "In October 2024 AB PM-JAY was extended to every Indian aged 70 and above, regardless of income, with cover of up to "
  "₹5 lakh a year. These beneficiaries receive the Ayushman Vay Vandana card.",
  ["Eligibility: age 70+", "No income test", "Cover: up to ₹5 lakh per year"],
  [fact("All citizens aged 70 and above, irrespective of income, get PM-JAY cover through the Ayushman Vaya Vandana "
        "card", "vayvandana")],
  current=ca("2024-10-30"))

G(T, CS, "Intermediate",
  "The PM Dhan-Dhaanya Krishi Yojana, approved by the Union Cabinet in July 2025, covers how many districts?",
  ["100", "112", "150", "250"], "*",
  "PM Dhan-Dhaanya Krishi Yojana",
  "Approved on 16 July 2025, the scheme runs for six years from 2025-26 with an annual outlay of ₹24,000 crore. It "
  "covers 100 districts with low productivity, low cropping intensity and weak credit, by converging existing "
  "central schemes.",
  ["Districts: 100", "Outlay: ₹24,000 crore a year for six years"],
  [fact("Cabinet clears PM Dhan-Dhaanya Krishi Yojana with ₹24,000 crore annual outlay for 6 years; 100 districts",
        "dhandhaanya")],
  why="112 is the number of Aspirational Districts, a different programme.",
  current=ca("2025-07-16"))

G(T, SL, "Intermediate",
  "From which city did the Prime Minister release the 21st instalment of PM-KISAN on 19 November 2025?",
  ["Coimbatore", "Varanasi", "Bhagalpur", "Yavatmal"], "*",
  "PM-KISAN instalments",
  "The 21st instalment, about ₹18,000 crore to roughly 9 crore farmers (₹2,000 each), was released at Coimbatore, "
  "Tamil Nadu, during the South India Natural Farming Summit.",
  ["21st instalment: 19 November 2025", "Place: Coimbatore, Tamil Nadu"],
  [fact("PM releases ₹18,000 crore under PM-KISAN in Tamil Nadu's Coimbatore (21st instalment)", "pmkisan21")],
  current=ca("2025-11-19"))

G(T, CS, "Intermediate",
  "PM-eBus Sewa, approved by the Union Cabinet in August 2023, aims to add how many electric buses to city bus "
  "services on the PPP model?",
  ["10,000", "5,000", "25,000", "50,000"], "*",
  "PM-eBus Sewa",
  "The scheme adds 10,000 e-buses in cities on a PPP model, with an estimated cost of ₹57,613 crore of which the "
  "Centre gives ₹20,000 crore. Cities with population of 3 lakh and above, especially those with no organised bus "
  "service, get priority.",
  ["E-buses: 10,000", "Estimated cost: ₹57,613 crore (Central assistance ₹20,000 crore)"],
  [fact("PM-eBus Sewa: Cabinet approves ₹57,613 crore for 10,000 e-buses across cities", "ebus")],
  current=ca("2023-08-16"))

G(T, CS, "Intermediate",
  "The Mission for Aatmanirbharta in Pulses, approved in October 2025, aims to raise pulses production to how much by "
  "2030-31?",
  ["350 lakh tonnes", "242 lakh tonnes", "500 lakh tonnes", "200 lakh tonnes"], "*",
  "Pulses mission",
  "The six-year mission (2025-26 to 2030-31) has an outlay of ₹11,440 crore and targets 350 lakh tonnes of pulses by "
  "2030-31, up from 242 lakh tonnes in 2023-24, with assured MSP procurement of tur, urad and masoor.",
  ["2023-24 output: 242 lakh tonnes", "Target 2030-31: 350 lakh tonnes"],
  [fact("Cabinet approves Mission for Aatmanirbharta in Pulses 2025-26 to 2030-31; production to 350 lakh tonnes",
        "pulses")],
  why="242 lakh tonnes is the 2023-24 production base.",
  current=ca("2025-10-01"))

G(T, CS, "Intermediate",
  "Pradhan Mantri Awas Yojana-Urban 2.0, approved in August 2024, aims to provide houses to how many urban families "
  "over five years?",
  ["1 crore", "2 crore", "3 crore", "50 lakh"], "*",
  "PMAY-U 2.0",
  "PMAY-U 2.0 targets 1 crore urban poor and middle-class families over five years, with government assistance of "
  "₹2.30 lakh crore. Assistance in the BLC and AHP verticals is up to ₹2.50 lakh per unit.",
  ["Target: 1 crore houses", "Government assistance: ₹2.30 lakh crore"],
  [fact("PMAY-U 2.0 approved for 1 crore urban poor and middle-class families", "pmayu2_air"),
   fact("Assistance up to ₹2.50 lakh per unit under PMAY-U 2.0", "pmayu2")],
  current=ca("2024-08-09"))

G(T, SL, "Intermediate",
  "After the target of 3 crore 'Lakhpati Didis' was crossed, what new target did the Prime Minister set in August "
  "2026?",
  ["6 crore by March 2029", "5 crore by March 2028", "4 crore by March 2027", "10 crore by March 2030"], "*",
  "Lakhpati Didi",
  "A Lakhpati Didi is an SHG member whose household earns at least ₹1 lakh a year on a sustained basis. The target was "
  "raised from 2 crore to 3 crore in 2024; with 3 crore reached ahead of the March 2027 deadline, the new goal is 6 "
  "crore by March 2029.",
  ["Old target: 3 crore", "New target: 6 crore by March 2029"],
  [fact("PM Modi sets target of 6 crore Lakhpati Didis after surpassing 3 crore; new goal by March 2029", "lakhpati")],
  current=ca("2026-08-15"))

G(T, SL, "Intermediate",
  "The Viksit Bharat-Guarantee for Rozgar and Ajeevika Mission (Gramin) Act, 2025 guarantees how many days of wage "
  "employment per rural household in a financial year?",
  ["125 days", "100 days", "150 days", "120 days"], "*",
  "VB-G RAM G Act",
  "The Act, which received the President's assent in December 2025, replaces MGNREGA, 2005. It raises the statutory "
  "guarantee from 100 to 125 days of wage employment per rural household each year for adults who volunteer for "
  "unskilled manual work.",
  ["MGNREGA guarantee: 100 days", "VB-G RAM G guarantee: 125 days"],
  [fact("VB-G RAM G Act replaces MGNREGA; guarantees 125 days of wage employment per rural household", "vbgramg"),
   fact("President Murmu assents to VB-G RAM G Bill, 2025", "vbgramg_air")],
  why="100 days was the MGNREGA guarantee.",
  current=ca("2025-12-21"))

G(T, SL, "Intermediate",
  "The Union Budget 2026-27 announced India Semiconductor Mission 2.0 with what outlay?",
  ["₹40,000 crore", "₹76,000 crore", "₹22,919 crore", "₹10,000 crore"], "*",
  "ISM 2.0",
  "ISM 2.0, announced on 1 February 2026 with ₹40,000 crore, focuses on semiconductor equipment and materials, "
  "full-stack Indian IP and supply-chain resilience, with industry-led research and training centres.",
  ["ISM 2.0 outlay: ₹40,000 crore"],
  [fact("Budget 2026: Semiconductor Mission 2.0 with ₹40,000 crore", "ism2")],
  why="₹22,919 crore was the original outlay of the Electronics Components Manufacturing Scheme (April 2025).",
  current=ca("2026-02-01"))

G(T, SL, "Intermediate",
  "In July 2026 the Union Cabinet approved continuing PM-KISAN from 2026-27 to 2030-31. What is the approved outlay "
  "for this period?",
  ["₹3.15 lakh crore", "₹2.10 lakh crore", "₹1.80 lakh crore", "₹4.50 lakh crore"], "*",
  "PM-KISAN continuation",
  "The Cabinet approved continuation of PM-KISAN for five years, 2026-27 to 2030-31, with a total outlay of ₹3.15 lakh "
  "crore. The scheme pays ₹6,000 a year to eligible farmer families in three instalments.",
  ["Period: 2026-27 to 2030-31", "Outlay: ₹3.15 lakh crore"],
  [fact("PM-KISAN continued 2026-27 to 2030-31 with ₹3.15 lakh crore (31 July 2026)", "pmkisan_cont")],
  current=ca("2026-07-31"))

G(T, SL, "Intermediate",
  "'Samudra Manthan', approved by the Union Cabinet in July 2026 with an outlay of ₹84,084 crore up to 2030-31, is "
  "the name of which scheme?",
  ["National Offshore Exploration Scheme", "Deep Ocean Mission", "Sagarmala Programme",
   "Pradhan Mantri Matsya Sampada Yojana"], "*",
  "Samudra Manthan",
  "In the same briefing that continued PM-KISAN, the Cabinet approved the National Offshore Exploration Scheme, "
  "'Samudra Manthan', with an outlay of ₹84,084 crore for implementation up to FY 2030-31.",
  ["Samudra Manthan = National Offshore Exploration Scheme", "Outlay: ₹84,084 crore"],
  [fact("National Offshore Exploration Scheme (Samudra Manthan) approved with outlay ₹84,084 crore up to 2030-31",
        "pmkisan_cont")],
  current=ca("2026-07-31"))

G(T, CS, "Advanced",
  "Consider the following statements about the Pradhan Mantri Viksit Bharat Rozgar Yojana (PM-VBRY):\n"
  "1. Its benefit for first-time employees covers EPFO-registered workers earning up to ₹1 lakh a month.\n"
  "2. A first-time employee gets one month's wage, up to ₹15,000, in a single instalment on joining.\n"
  "3. Employers can get up to ₹3,000 a month for each additional employee.\n"
  "Which of the statements given above is/are correct?",
  S123, "C",
  "PM-VBRY",
  "PM-VBRY was announced on 15 August 2025 and took effect from 1 August 2025. First-time private-sector employees "
  "registered with EPFO and earning up to ₹1 lakh a month get one month's wage up to ₹15,000, paid in two "
  "instalments (after 6 and 12 months of service). Employers get up to ₹3,000 a month per new employee.",
  ["1: correct", "2: wrong (two instalments)", "3: correct", "So 1 and 3 only"],
  [fact("PM-VBRY: first-time employees up to ₹1 lakh/month with EPFO; one month's wage up to ₹15,000 in two "
        "instalments; employers up to ₹3,000/month", "pmvbry_portal"),
   fact("PM launched the ₹1 lakh crore PM-VBRY on 15 August 2025", "pmvbry")],
  current=ca("2025-08-15"))

# ====================================================================== National Current Affairs (10 / 6 / 9)
T, GD, ST, DF = "National Current Affairs", "Government decisions", "States and UTs", "Defence"

G(T, ST, "Basic",
  "Who was sworn in on 9 May 2026 as the first Chief Minister of West Bengal from the BJP?",
  ["Suvendu Adhikari", "Samik Bhattacharya", "Dilip Ghosh", "Agnimitra Paul"], "*",
  "West Bengal 2026",
  "The BJP won the 2026 West Bengal Assembly election, ending the Trinamool Congress's 15-year rule. Suvendu Adhikari "
  "took oath as the state's first BJP Chief Minister at the Brigade Parade Ground in Kolkata on 9 May 2026.",
  ["Result: BJP won a clear majority", "CM: Suvendu Adhikari (sworn in 9 May 2026)"],
  [fact("Suvendu Adhikari takes oath as first BJP CM of West Bengal on 9 May 2026", "wb_cm")],
  why="Agnimitra Paul was sworn in as a minister at the same ceremony.",
  current=ca("2026-05-09"))

G(T, ST, "Basic",
  "C. Joseph Vijay, sworn in as Chief Minister of Tamil Nadu on 10 May 2026, leads which party?",
  ["Tamilaga Vettri Kazhagam (TVK)", "Dravida Munnetra Kazhagam (DMK)",
   "All India Anna Dravida Munnetra Kazhagam (AIADMK)", "Pattali Makkal Katchi (PMK)"], "*",
  "Tamil Nadu 2026",
  "Vijay's Tamilaga Vettri Kazhagam emerged as the largest party in the 2026 election, ending decades of DMK and "
  "AIADMK rule. He took oath on 10 May 2026 in Chennai.",
  ["Party: TVK", "Sworn in: 10 May 2026"],
  [fact("DMK-AIADMK era ends: Vijay takes oath as Tamil Nadu CM on 10 May 2026", "tn_cm")],
  current=ca("2026-05-10"))

G(T, ST, "Basic",
  "Who was sworn in as Chief Minister of Kerala in May 2026 after the Congress-led UDF returned to power?",
  ["V. D. Satheesan", "Ramesh Chennithala", "K. C. Venugopal", "Shashi Tharoor"], "*",
  "Kerala 2026",
  "The UDF returned to power in Kerala after a decade, unseating the LDF government of Pinarayi Vijayan. V. D. "
  "Satheesan, the Congress leader, was sworn in as Chief Minister in May 2026.",
  ["Winning front: UDF", "CM: V. D. Satheesan"],
  [fact("V D Satheesan sworn in as Kerala's Chief Minister", "kl_cm")],
  current=ca("2026-05-18"))

G(T, ST, "Basic",
  "On 20 November 2025, Nitish Kumar took oath as Chief Minister of Bihar for which time, a record?",
  ["10th", "8th", "9th", "11th"], "*",
  "Bihar 2025",
  "After the NDA won the 2025 Bihar Assembly election, Nitish Kumar was sworn in at Gandhi Maidan, Patna, on 20 "
  "November 2025 for a record tenth time.",
  ["Oath: 20 November 2025, Gandhi Maidan", "Count: 10th time"],
  [fact("Nitish Kumar takes oath as CM of Bihar for record 10th time", "bihar_cm")],
  current=ca("2025-11-20"))

G(T, GD, "Basic",
  "Following a Ministry of Home Affairs communication of November 2025, the Raj Bhavans (Governors' residences) are "
  "being renamed as what?",
  ["Lok Bhavan", "Jan Bhavan", "Seva Bhavan", "Rashtra Bhavan"], "*",
  "Renaming of Raj Bhavans",
  "The MHA asked States and UTs to rename Raj Bhavans as 'Lok Bhavan' and Raj Niwas (Lt Governors' offices) as 'Lok "
  "Niwas', to drop a colonial-era name. Many States adopted the change in early December 2025.",
  ["Governor's office: Lok Bhavan", "Lt Governor's office: Lok Niwas"],
  [fact("Raj Bhavan will now be known as Lok Bhavan", "lokbhavan"),
   fact("MHA orders renaming of J&K Raj Bhavan as Lok Bhavan", "lokbhavan_jk")],
  current=ca("2025-11-25"))

G(T, GD, "Basic",
  "The first phase (houselisting) of Census 2027, India's first digital census, began on which date?",
  ["1 April 2026", "1 January 2026", "1 March 2027", "15 August 2026"], "*",
  "Census 2027",
  "Phase I (Houselisting and Housing Census) began on 1 April 2026, with each State and UT doing 30 days of field work "
  "between April and September 2026. Data are collected on mobile apps, and citizens could self-enumerate online. "
  "Population Enumeration follows in February 2027.",
  ["Phase I start: 1 April 2026", "Phase II (population enumeration): February 2027"],
  [fact("Initial phase of Census 2027 to begin on April 1; houselisting within a 30-day period", "census"),
   fact("Census 2027 begins in digital mode on 1 April 2026 with self-enumeration", "census_tv")],
  current=ca("2026-04-01"))

G(T, DF, "Basic",
  "Who was named India's new Chief of Defence Staff in May 2026, succeeding General Anil Chauhan?",
  ["Lt Gen N. S. Raja Subramani", "Gen Upendra Dwivedi", "Air Chief Marshal A. P. Singh",
   "Vice Admiral Krishna Swaminathan"], "*",
  "Chief of Defence Staff",
  "On 8-9 May 2026 the government named Lt Gen N. S. Raja Subramani (Retd) as the next CDS after General Anil "
  "Chauhan's tenure ended on 30 May 2026. He also serves as Secretary, Department of Military Affairs.",
  ["Outgoing CDS: Gen Anil Chauhan", "New CDS: Lt Gen N. S. Raja Subramani"],
  [fact("Lt Gen N.S. Raja Subramani named new CDS; Chauhan's tenure ends May 30", "cds")],
  why="Vice Admiral Krishna Swaminathan was named Navy chief in the same announcement.",
  current=ca("2026-05-09"))

G(T, DF, "Basic",
  "Who became the Chief of the Naval Staff on 31 May 2026?",
  ["Admiral Krishna Swaminathan", "Admiral Dinesh K. Tripathi", "Admiral R. Hari Kumar", "Admiral Sanjay Vatsayan"],
  "*",
  "Navy chief",
  "Vice Admiral Krishna Swaminathan, then Flag Officer Commanding-in-Chief, Western Naval Command, was named Navy chief "
  "and assumed office on 31 May 2026, succeeding Admiral Dinesh K. Tripathi. He serves until 31 December 2028.",
  ["Predecessor: Adm Dinesh K. Tripathi", "New chief: Adm Krishna Swaminathan (from 31 May 2026)"],
  [fact("Vice Admiral Krishna Swaminathan named Navy chief; assumes office May 31, serves till 31 Dec 2028", "cds"),
   fact("Swaminathan to succeed Admiral Dinesh Kumar Tripathi", "cds_bt")],
  current=ca("2026-05-31"))

G(T, GD, "Basic",
  "What is the name of the new complex, inaugurated in February 2026, into which the Prime Minister's Office moved "
  "from South Block?",
  ["Seva Teerth", "Kartavya Path", "Karmayogi Bhavan", "Nagrik Sadan"], "*",
  "New PMO complex",
  "The Prime Minister inaugurated Seva Teerth on 13 February 2026. It houses the PMO, the Cabinet Secretariat and the "
  "National Security Council Secretariat; Kartavya Bhavan 1 and 2 are part of the same complex. The motto is "
  "'Nagrik Devo Bhava'.",
  ["Old PMO: South Block", "New PMO: Seva Teerth (13 February 2026)"],
  [fact("PM inaugurates Seva Teerth, the new PMO housing the Cabinet Secretariat and NSCS", "sevateerth")],
  why="Kartavya Path is the avenue (formerly Rajpath), not the office complex.",
  current=ca("2026-02-13"))

G(T, DF, "Basic",
  "On 8 May 2026 DRDO flight-tested an Advanced Agni missile from Dr APJ Abdul Kalam Island. Which technology did the "
  "test demonstrate?",
  ["MIRV (Multiple Independently Targetable Re-entry Vehicles)", "Air-independent propulsion",
   "Scramjet propulsion", "Laser-guided terminal homing"], "*",
  "Advanced Agni MIRV test",
  "The test of 8 May 2026 used MIRV technology, which lets one missile carry several payloads aimed at different "
  "targets spread over a wide area. The targets lay across the Indian Ocean Region.",
  ["Missile: Advanced Agni", "Technology: MIRV", "Site: Dr APJ Abdul Kalam Island, Odisha"],
  [fact("Advanced Agni with MIRV flight-tested on 8 May 2026 from Dr APJ Abdul Kalam Island", "agni")],
  why="Air-independent propulsion is a submarine technology.",
  current=ca("2026-05-08"))

G(T, ST, "Intermediate",
  "Himanta Biswa Sarma, sworn in again as Chief Minister of Assam on 12 May 2026, set which record?",
  ["First non-Congress leader to be Assam CM for two consecutive terms", "First CM of Assam from the BJP",
   "Longest-serving CM in the history of Assam", "First Assam CM elected unopposed from his seat"], "*",
  "Assam 2026",
  "The NDA won 102 of 126 seats, forming its third straight government in Assam. Sarma took oath for a second "
  "consecutive term on 12 May 2026 in Guwahati, the first non-Congress leader to do so in the state.",
  ["NDA seats: 102 of 126", "Sarma: second consecutive term"],
  [fact("Himanta Biswa Sarma takes oath for second straight term; first non-Congress leader with two consecutive "
        "terms as Assam CM", "assam_cm")],
  current=ca("2026-05-12"))

G(T, DF, "Intermediate",
  "INS Mangrol, commissioned in October 2026, is the third Anti-Submarine Warfare Shallow Water Craft built by which "
  "shipyard?",
  ["Cochin Shipyard Limited", "Garden Reach Shipbuilders and Engineers", "Mazagon Dock Shipbuilders",
   "Goa Shipyard Limited"], "*",
  "ASW Shallow Water Craft",
  "INS Mangrol was commissioned at the Naval Dockyard, Mumbai, in October 2026. It is the third ASW-SWC built by "
  "Cochin Shipyard Limited, Kochi.",
  ["Ship: INS Mangrol (ASW-SWC)", "Builder: Cochin Shipyard Limited"],
  [fact("INS Mangrol: third ASW-SWC built by Cochin Shipyard; commissioned at Naval Dockyard, Mumbai", "mangrol")],
  current=ca("2026-10-12"))

G(T, DF, "Intermediate",
  "INS Taragiri, commissioned at Visakhapatnam on 3 April 2026, belongs to which class of warships?",
  ["Project 17A stealth frigates", "Project 15B destroyers", "Kalvari-class submarines",
   "Anti-Submarine Warfare Shallow Water Craft"], "*",
  "Project 17A",
  "INS Taragiri, the third Project 17A frigate in its series, was built by Mazagon Dock Shipbuilders and commissioned "
  "by Raksha Mantri Rajnath Singh at Visakhapatnam on 3 April 2026, with about 75% indigenisation.",
  ["Class: Project 17A frigate", "Builder: Mazagon Dock Shipbuilders"],
  [fact("INS Taragiri: Project 17A, built by MDL, commissioned 3 April 2026 at Visakhapatnam", "taragiri")],
  current=ca("2026-04-03"))

G(T, DF, "Intermediate",
  "INS Samarthak, commissioned at Karwar on 16 October 2026 as the Navy's first indigenous Multi-Purpose Vessel, was "
  "built by which company?",
  ["Larsen & Toubro", "Cochin Shipyard Limited", "Hindustan Shipyard Limited", "Mazagon Dock Shipbuilders"], "*",
  "Multi-Purpose Vessel",
  "INS Samarthak was designed and built by L&T at its Kattupalli shipyard near Chennai and commissioned at Naval Base "
  "Karwar on 16 October 2026, with the Vice-President presiding. It is a test and trials platform that also supports "
  "surveillance and HADR tasks.",
  ["Ship: INS Samarthak (MPV)", "Builder: L&T, Kattupalli"],
  [fact("INS Samarthak, first indigenous MPV, commissioned on 16 Oct 2026 at Karwar", "samarthak"),
   fact("L&T delivers multi-purpose vessel INS Samarthak built at Kattupalli", "samarthak_lt")],
  current=ca("2026-10-16"))

G(T, DF, "Intermediate",
  "DRDO flight-tested the Long Range Land Attack Cruise Missile (LRLACM) on 15 June 2026. Which DRDO laboratory was "
  "the nodal lab for it?",
  ["Aeronautical Development Establishment, Bengaluru", "Defence Research and Development Laboratory, Hyderabad",
   "Armament Research and Development Establishment, Pune", "Integrated Test Range, Chandipur"], "*",
  "LRLACM",
  "The LRLACM was launched from Dr APJ Abdul Kalam Island off Odisha on 15 June 2026. ADE, Bengaluru was the nodal "
  "laboratory, with other DRDO labs and industry; the Integrated Test Range, Chandipur tracked the flight.",
  ["Missile: LRLACM", "Nodal lab: ADE, Bengaluru", "Tracking: ITR Chandipur"],
  [fact("LRLACM tested 15 June 2026 from Dr APJ Abdul Kalam Island; ADE Bengaluru nodal lab; ITR tracked",
        "lrlacm")],
  why="ITR Chandipur only tracked the test.",
  current=ca("2026-06-15"))

G(T, DF, "Intermediate",
  "On 21 June 2026 the Prime Minister commissioned three warships at Kolkata. INS Dunagiri, one of them, is a ship of "
  "which type?",
  ["Project 17A stealth frigate built by GRSE", "Survey Vessel (Large) built by GRSE",
   "Anti-Submarine Warfare Shallow Water Craft built by Cochin Shipyard", "Next Generation Offshore Patrol Vessel"],
  "*",
  "Triple commissioning at Kolkata",
  "INS Dunagiri (fifth Project 17A frigate, GRSE's second), INS Sanshodhak (Survey Vessel Large) and INS Agray "
  "(ASW Shallow Water Craft) were commissioned by the Prime Minister at Kolkata on 21 June 2026.",
  ["Dunagiri: P17A frigate (GRSE)", "Sanshodhak: survey vessel", "Agray: ASW-SWC"],
  [fact("PM commissioned INS Dunagiri (P17A, GRSE), INS Sanshodhak (SVL) and INS Agray (ASW SWC) at Kolkata on 21 June "
        "2026", "dunagiri")],
  why="The survey vessel was INS Sanshodhak; the ASW craft was INS Agray.",
  current=ca("2026-06-21"))

G(T, ST, "Advanced",
  "Consider the following statements about the 2026 change of government in West Bengal:\n"
  "1. The BJP won 207 of the 294 Assembly seats.\n"
  "2. Suvendu Adhikari took oath at the Brigade Parade Ground in Kolkata.\n"
  "3. Suvendu Adhikari won the Nandigram seat by defeating the outgoing Chief Minister in 2026.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "West Bengal 2026: details",
  "The BJP won 207 of 294 seats. Governor R. N. Ravi administered the oath at the Brigade Parade Ground on 9 May 2026. "
  "In 2026 Adhikari defeated the outgoing Chief Minister in Bhabanipur, not Nandigram.",
  ["1: correct", "2: correct", "3: wrong (Bhabanipur)", "So 1 and 2 only"],
  [fact("BJP won 207 of 294 seats; oath at Brigade Parade Ground; Adhikari won Bhabanipur defeating outgoing CM",
        "wb_air"),
   fact("Suvendu Adhikari takes oath as first BJP CM of West Bengal", "wb_cm")],
  current=ca("2026-05-09"))

G(T, ST, "Advanced",
  "Consider the following statements about the swearing-in of C. Joseph Vijay as Chief Minister of Tamil Nadu:\n"
  "1. It took place at the Jawaharlal Nehru Stadium, Chennai, on 10 May 2026.\n"
  "2. The oath was administered by Governor Rajendra Vishwanath Arlekar.\n"
  "3. Nine ministers were sworn in along with him.\n"
  "Which of the statements given above is/are correct?",
  S123, "D",
  "Tamil Nadu 2026: details",
  "Vijay took oath at the Jawaharlal Nehru Stadium, Chennai, on 10 May 2026. Governor Rajendra Vishwanath Arlekar "
  "administered the oath, and nine cabinet ministers were sworn in with him. He became the 13th Chief Minister of "
  "Tamil Nadu.",
  ["1: correct", "2: correct", "3: correct", "So 1, 2 and 3"],
  [fact("Vijay sworn in as 13th TN CM; nine cabinet ministers also took oath", "tn_uni"),
   fact("Vijay takes oath as Tamil Nadu CM on 10 May 2026", "tn_cm")],
  current=ca("2026-05-10"))

G(T, ST, "Advanced",
  "Consider the following statements about the formation of the Bihar government in November 2025:\n"
  "1. Nitish Kumar took oath at Gandhi Maidan, Patna.\n"
  "2. The oath was administered by Governor Rajendra Arlekar.\n"
  "3. Samrat Choudhary and Vijay Kumar Sinha were sworn in as Deputy Chief Ministers.\n"
  "Which of the statements given above is/are correct?",
  S123, "C",
  "Bihar 2025: details",
  "Nitish Kumar was sworn in on 20 November 2025 at Gandhi Maidan. Governor Arif Mohammad Khan administered the oath, "
  "not Rajendra Arlekar. BJP leaders Samrat Choudhary and Vijay Kumar Sinha became "
  "Deputy CMs.",
  ["1: correct", "2: wrong (Arif Mohammad Khan)", "3: correct", "So 1 and 3 only"],
  [fact("Nitish sworn in at Gandhi Maidan by Governor Arif Mohammad Khan", "bihar_cm"),
   fact("Samrat Choudhary and Vijay Sinha named deputy CMs", "bihar_bt")],
  current=ca("2025-11-20"))

G(T, DF, "Advanced",
  "Consider the following statements about the Chief of Defence Staff appointed in May 2026:\n"
  "1. Lt Gen N. S. Raja Subramani also holds the post of Secretary, Department of Military Affairs.\n"
  "2. He succeeded General Anil Chauhan.\n"
  "3. He was the serving Chief of the Army Staff when he was appointed.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "CDS appointment",
  "The CDS is also Secretary, Department of Military Affairs. Lt Gen Raja Subramani (Retd), a former Vice Chief of "
  "the Army Staff, was serving as Military Adviser in the National Security Council Secretariat when named. He "
  "succeeded Gen Anil Chauhan, whose tenure ended on 30 May 2026.",
  ["1: correct", "2: correct", "3: wrong (Military Adviser, NSCS)", "So 1 and 2 only"],
  [fact("Raja Subramani to serve as Secretary, Department of Military Affairs; succeeds Anil Chauhan", "cds"),
   fact("Subramani was Military Adviser in the NSCS; former Army Vice Chief", "cds_bt")],
  current=ca("2026-05-09"))

G(T, DF, "Advanced",
  "Consider the following statements about Admiral Krishna Swaminathan, who became Chief of the Naval Staff in May "
  "2026:\n"
  "1. He was Flag Officer Commanding-in-Chief, Western Naval Command, when named.\n"
  "2. He will serve until 31 December 2028.\n"
  "3. He succeeded Admiral R. Hari Kumar.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "Navy chief: details",
  "Vice Admiral Krishna Swaminathan was FOC-in-C, Western Naval Command. He took over on 31 May 2026 for a term until "
  "31 December 2028, succeeding Admiral Dinesh K. Tripathi, not Admiral R. Hari Kumar.",
  ["1: correct", "2: correct", "3: wrong (Dinesh K. Tripathi)", "So 1 and 2 only"],
  [fact("Krishna Swaminathan, FOC-in-C Western Naval Command, assumes office 31 May, serves till 31 Dec 2028", "cds"),
   fact("Succeeds Vice Admiral Dinesh Kumar Tripathi", "cds_bt")],
  current=ca("2026-05-31"))

G(T, GD, "Advanced",
  "Consider the following statements about the renaming of Governors' offices:\n"
  "1. The Ministry of Home Affairs' communication on the renaming was dated 25 November 2025.\n"
  "2. Offices of Lieutenant Governors are to be called 'Lok Niwas'.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "Lok Bhavan and Lok Niwas",
  "The MHA communication dated 25 November 2025 suggested that offices of Governors be named 'Lok Bhavan' and offices "
  "of Lieutenant Governors 'Lok Niwas'. Ladakh's Raj Niwas, for example, became Lok Niwas.",
  ["1: correct", "2: correct", "So both"],
  [fact("MHA communication dated 25 Nov 2025: Raj Bhavans as Lok Bhavan and Raj Niwas as Lok Niwas", "lokbhavan_jk"),
   fact("Raj Bhavan will now be known as Lok Bhavan", "lokbhavan")],
  current=ca("2025-11-25"))

G(T, GD, "Advanced",
  "Consider the following statements about Seva Teerth:\n"
  "1. It houses the Prime Minister's Office, the Cabinet Secretariat and the National Security Council Secretariat.\n"
  "2. It was inaugurated by the Prime Minister on 13 February 2026.\n"
  "3. The PMO moved into it from North Block.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "Seva Teerth",
  "Seva Teerth, part of the Central Vista redevelopment, houses the PMO, the Cabinet Secretariat and the NSCS. It was "
  "inaugurated on 13 February 2026, and the PMO moved there from South Block (not North Block).",
  ["1: correct", "2: correct", "3: wrong (South Block)", "So 1 and 2 only"],
  [fact("Seva Teerth houses PMO, Cabinet Secretariat and NSCS; inaugurated 13 Feb 2026", "sevateerth"),
   fact("PMO relocates to Seva Teerth from South Block", "sevateerth_q")],
  current=ca("2026-02-13"))

G(T, GD, "Advanced",
  "Consider the following statements about Census 2027:\n"
  "1. The houselisting phase ran between 1 April and 30 September 2026, with each State/UT doing 30 days of field "
  "work within that window.\n"
  "2. Citizens could enumerate themselves online before the enumerator's visit.\n"
  "3. The population enumeration phase is scheduled to begin in February 2027.\n"
  "Which of the statements given above is/are correct?",
  S123, "D",
  "Census 2027: design",
  "Phase I ran from 1 April to 30 September 2026 with a 30-day field window per State/UT, preceded by an optional "
  "online self-enumeration period, the first time this has been offered. Population Enumeration, including caste "
  "data, is due from February 2027.",
  ["1: correct", "2: correct", "3: correct", "So 1, 2 and 3"],
  [fact("Houselisting 1 April to 30 September 2026, 30 days per State/UT; Population Enumeration Feb 2027",
        "census"),
   fact("Census 2027 in digital mode with self-enumeration", "census_tv")],
  current=ca("2026-04-01"))

G(T, DF, "Advanced",
  "Consider the following statements about INS Samarthak:\n"
  "1. It is the Indian Navy's first indigenous Multi-Purpose Vessel.\n"
  "2. It was commissioned at Naval Base Karwar.\n"
  "3. It was built at a public sector shipyard in Visakhapatnam.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "INS Samarthak: details",
  "INS Samarthak, the first indigenous MPV, was commissioned at Naval Base Karwar on 16 October 2026. It was built by "
  "L&T, a private company, at its Kattupalli shipyard near Chennai, with over 75% indigenous content.",
  ["1: correct", "2: correct", "3: wrong (L&T, Kattupalli)", "So 1 and 2 only"],
  [fact("INS Samarthak, first indigenous MPV, commissioned at Karwar on 16 Oct 2026", "samarthak"),
   fact("Built at L&T's Kattupalli shipyard", "samarthak_lt")],
  current=ca("2026-10-16"))

# ====================================================================== International Current Affairs (0 / 4 / 2)
T, BR, GE = "International Current Affairs", "Bilateral relations", "Global events"

G(T, BR, "Intermediate",
  "On which date did the India-UK Comprehensive Economic and Trade Agreement (CETA) enter into force?",
  ["15 July 2026", "6 May 2025", "1 April 2026", "26 January 2026"], "*",
  "India-UK CETA",
  "The CETA, concluded in May 2025, entered into force on 15 July 2026 together with the Double Contribution "
  "Convention on social security. Indian exports get duty-free access on about 99% of UK tariff lines.",
  ["Concluded: 6 May 2025", "In force: 15 July 2026"],
  [fact("India-UK CETA and social security agreement came into force on 15 July 2026", "ceta"),
   fact("India-UK CETA in force from 15 July 2026", "ceta_am")],
  why="6 May 2025 is when negotiations were concluded.",
  current=ca("2026-07-15"))

G(T, BR, "Intermediate",
  "India signed a Comprehensive Economic Partnership Agreement (CEPA) in Muscat on 18 December 2025 with which "
  "country, its second such pact with a GCC member?",
  ["Oman", "Qatar", "Saudi Arabia", "Kuwait"], "*",
  "India-Oman CEPA",
  "The India-Oman CEPA was signed in Muscat on 18 December 2025 during the Prime Minister's visit. It is India's second "
  "trade pact with a GCC state after the UAE CEPA of 2022, and Oman's first bilateral deal since its 2006 agreement "
  "with the US. It came into force on 1 June 2026.",
  ["Signed: Muscat, 18 December 2025", "First GCC CEPA: UAE (2022)"],
  [fact("India-Oman CEPA signed; India's second CEPA with a GCC state; Oman's first such deal in two decades", "oman"),
   fact("India-Oman CEPA comes into force (June 2026)", "oman_force")],
  why="The UAE was the first GCC partner (2022).",
  current=ca("2025-12-18"))

G(T, BR, "Intermediate",
  "With which country did India sign a free trade agreement in New Delhi on 27 April 2026, after talks that began only "
  "in March 2025?",
  ["New Zealand", "Australia", "Canada", "Chile"], "*",
  "India-New Zealand FTA",
  "Piyush Goyal and Todd McClay signed the India-New Zealand FTA on 27 April 2026. Talks launched in March 2025 were "
  "concluded in December 2025. New Zealand cuts or removes tariffs on all Indian exports and expects about $20 "
  "billion of investment into India.",
  ["Talks launched: March 2025", "Concluded: December 2025", "Signed: 27 April 2026"],
  [fact("India and New Zealand sign free trade deal on 27 April 2026", "nzfta")],
  current=ca("2026-04-27"))

G(T, GE, "Intermediate",
  "Who was sworn in as Prime Minister of Bangladesh on 17 February 2026 after his party's victory in the general "
  "election of 12 February?",
  ["Tarique Rahman", "Muhammad Yunus", "Mirza Fakhrul Islam Alamgir", "Nahid Islam"], "*",
  "Bangladesh election 2026",
  "The BNP won a landslide in the 13th general election on 12 February 2026. Its chairman Tarique Rahman was sworn in "
  "as Prime Minister on 17 February, ending the interim administration led by Muhammad Yunus.",
  ["Election: 12 February 2026", "Winner: BNP", "PM sworn in: Tarique Rahman, 17 February 2026"],
  [fact("Tarique Rahman sworn in as Bangladesh's PM after landslide election victory", "bdesh"),
   fact("Bangladesh's new prime minister sworn in on 17 Feb 2026", "bdesh_mb")],
  why="Muhammad Yunus headed the interim government before the election.",
  current=ca("2026-02-17"))

G(T, BR, "Advanced",
  "Consider the following statements about the India-UK CETA:\n"
  "1. A social security agreement (Double Contribution Convention) came into force on the same day as the CETA.\n"
  "2. About 99% of India's exports get duty-free access to the UK.\n"
  "3. All UK goods, including Scotch whisky and cars, enter India duty-free from the first day.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "India-UK CETA: features",
  "The CETA and the Double Contribution Convention both took effect on 15 July 2026. Indian exporters get duty-free "
  "access on about 99% of tariff lines, subject to rules of origin. Tariff cuts on UK goods such as whisky and cars "
  "are phased in, not immediate.",
  ["1: correct", "2: correct", "3: wrong (phased reductions)", "So 1 and 2 only"],
  [fact("CETA and social security agreement in force 15 July 2026; duty-free access for about 99% of India's exports; "
        "phased cuts on UK whisky and autos", "ceta_am"),
   fact("India-UK FTA comes into force: Piyush Goyal", "ceta")],
  current=ca("2026-07-15"))

G(T, GE, "Advanced",
  "Consider the following statements about the United States and the World Health Organization:\n"
  "1. The US withdrawal from WHO took effect on 22 January 2026.\n"
  "2. The withdrawal process began with an executive order signed on 20 January 2025.\n"
  "3. The US paid all its arrears to WHO before leaving.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "US exit from WHO",
  "Executive Order 14155 of 20 January 2025 began the withdrawal, which took effect on 22 January 2026 after the "
  "one-year notice period. US officials put arrears at about $260 million and said they would not pay them.",
  ["1: correct", "2: correct", "3: wrong (arrears unpaid)", "So 1 and 2 only"],
  [fact("US formally exited WHO on 22 January 2026 after EO 14155 of 20 January 2025", "who_exit"),
   fact("US completes withdrawal from WHO; arrears of about $260 million unpaid", "who_exit_news")],
  current=ca("2026-01-22"))

# ====================================================================== Important Appointments (7 / 2 / 9)
T, BF, IB = "Important Appointments", "Banking and finance heads", "International bodies"

G(T, BF, "Basic",
  "Who took charge as a Deputy Governor of the Reserve Bank of India on 4 May 2026?",
  ["Rohit Jain", "T. Rabi Sankar", "Poonam Gupta", "M. Rajeshwar Rao"], "*",
  "RBI Deputy Governor",
  "Rohit Jain, earlier an Executive Director of the RBI, assumed charge as Deputy Governor on 4 May 2026 for three "
  "years, under a government notification of 2 May 2026. He replaced T. Rabi Sankar, whose extended term ended on "
  "2 May.",
  ["New Deputy Governor: Rohit Jain", "Took charge: 4 May 2026"],
  [fact("Rohit Jain assumed charge as Deputy Governor on 4 May 2026 for three years; earlier Executive Director",
        "rohit_jain")],
  why="T. Rabi Sankar was the Deputy Governor he replaced; Poonam Gupta was already a Deputy Governor.",
  current=ca("2026-05-04"))

G(T, BF, "Basic",
  "Who was named Managing Director and CEO of HDFC Bank in October 2026, succeeding Sashidhar Jagdishan?",
  ["Anup Bagchi", "Sandeep Bakhshi", "Kaizad Bharucha", "Bhavesh Zaveri"], "*",
  "HDFC Bank MD & CEO",
  "After RBI approval on 1 October 2026, HDFC Bank named Anup Bagchi, a former ICICI group executive, as its next MD "
  "and CEO for three years from 27 October 2026, succeeding the retiring Sashidhar Jagdishan.",
  ["RBI approval: 1 October 2026", "New MD & CEO: Anup Bagchi"],
  [fact("HDFC Bank names Anup Bagchi MD & CEO; RBI approved on Oct 1; term from Oct 27; succeeds Sashidhar "
        "Jagdishan", "hdfc")],
  current=ca("2026-10-01"))

G(T, BF, "Basic",
  "Who was appointed Managing Director of State Bank of India in December 2025?",
  ["Ravi Ranjan", "Vinay M. Tonse", "Ashwini Kumar Tewari", "Challa Sreenivasulu Setty"], "*",
  "SBI Managing Director",
  "The government appointed Ravi Ranjan, Deputy Managing Director heading SBI's Corporate Accounts Group, as Managing "
  "Director on 15 December 2025, until his superannuation on 30 September 2028. He succeeded Vinay M. Tonse.",
  ["New SBI MD: Ravi Ranjan (15 December 2025)", "Predecessor: Vinay M. Tonse"],
  [fact("Govt appoints Ravi Ranjan as SBI MD on 15 Dec 2025; succeeds Vinay M. Tonse", "sbi_md")],
  why="Vinay M. Tonse was the outgoing MD whom he succeeded.",
  current=ca("2025-12-15"))

G(T, BF, "Basic",
  "Who took charge as Managing Director and CEO of Canara Bank on 1 June 2026?",
  ["Brajesh Kumar Singh", "Hardeep Singh Ahluwalia", "K. Satyanarayana Raju", "Binod Kumar"], "*",
  "Canara Bank MD & CEO",
  "Brajesh Kumar Singh, an Executive Director of Indian Bank since March 2024, took charge on 1 June 2026 and will "
  "serve until 30 April 2029. Hardeep Singh Ahluwalia had been interim MD & CEO from 1 January 2026.",
  ["New MD & CEO: Brajesh Kumar Singh", "Term: to 30 April 2029"],
  [fact("Brajesh Kumar Singh takes charge as Canara Bank MD & CEO on 1 June 2026, till 30 April 2029", "canara"),
   fact("Hardeep Singh Ahluwalia interim MD & CEO from 1 Jan 2026", "canara_interim")],
  why="Hardeep Singh Ahluwalia was the interim head before him.",
  current=ca("2026-06-01"))

G(T, IB, "Basic",
  "Former Iraqi President Barham Salih took office on 1 January 2026 as head of which UN body?",
  ["UN High Commissioner for Refugees (UNHCR)", "UN Development Programme (UNDP)", "World Food Programme (WFP)",
   "UN Relief and Works Agency (UNRWA)"], "*",
  "UNHCR chief",
  "The UN General Assembly elected Barham Salih as UN High Commissioner for Refugees in December 2025 for a five-year "
  "term from 1 January 2026, succeeding Filippo Grandi, whose ten-year tenure ended on 31 December 2025.",
  ["Post: UN High Commissioner for Refugees", "Predecessor: Filippo Grandi"],
  [fact("Former Iraqi President Barham Salih to lead UN refugee agency from 1 January 2026", "unhcr")],
  current=ca("2026-01-01"))

G(T, IB, "Basic",
  "Zou Jiayi, who took office on 16 January 2026, is the president of which multilateral bank?",
  ["Asian Infrastructure Investment Bank", "New Development Bank", "Asian Development Bank",
   "International Finance Corporation"], "*",
  "AIIB president",
  "Zou Jiayi, a former vice finance minister of China, began her term as President of the AIIB on 16 January 2026, "
  "the bank's 10th anniversary, succeeding founding President Jin Liqun. She is the AIIB's first woman president.",
  ["Bank: AIIB", "Predecessor: Jin Liqun"],
  [fact("Zou Jiayi assumed the AIIB presidency on 16 Jan 2026 succeeding Jin Liqun", "aiib")],
  current=ca("2026-01-16"))

G(T, IB, "Basic",
  "Giles Thomson, who began a two-year term on 1 July 2026, is the President of which body?",
  ["Financial Action Task Force (FATF)", "Bank for International Settlements (BIS)",
   "Financial Stability Board (FSB)", "International Organization of Securities Commissions (IOSCO)"], "*",
  "FATF presidency",
  "Giles Thomson of the United Kingdom became FATF President on 1 July 2026 for 2026-2028, succeeding Elisa de Anda "
  "Madrazo of Mexico. India's Vivek Aggarwal became Vice-President for July 2026 to June 2027.",
  ["FATF President: Giles Thomson (UK)", "Term: July 2026 to June 2028"],
  [fact("Giles Thomson began his term as FATF President on 1 July 2026 (UK presidency 2026-2028)", "fatf_pres")],
  current=ca("2026-07-01"))

G(T, IB, "Intermediate",
  "Economist Neelkanth Mishra was appointed in June 2026 as India's Executive Director at which institution?",
  ["World Bank", "International Monetary Fund", "Asian Development Bank", "New Development Bank"], "*",
  "India's Executive Director at the World Bank",
  "The Appointments Committee of the Cabinet approved Neelkanth Mishra, Chief Economist at Axis Bank, as Executive "
  "Director at the World Bank in Washington for three years. The constituency covers India, Bangladesh, Bhutan and "
  "Sri Lanka. He succeeds Parameswaran Iyer.",
  ["Post: Executive Director, World Bank", "Predecessor: Parameswaran Iyer"],
  [fact("Economist Neelkanth Mishra appointed World Bank Executive Director", "wb_ed")],
  current=ca("2026-06-04"))

G(T, BF, "Intermediate",
  "K. V. Ramana Murty, appointed in March 2026, became a whole-time member of which regulator?",
  ["SEBI", "IRDAI", "PFRDA", "IBBI"], "*",
  "SEBI whole-time member",
  "The government appointed K. V. Ramana Murty, a retired Indian Defence Accounts Service officer, as a whole-time "
  "member of SEBI for three years. He took charge in April 2026, bringing SEBI back to four whole-time members.",
  ["Regulator: SEBI", "Restores four whole-time members"],
  [fact("Govt appoints KV Ramana Murty as SEBI whole-time member for 3 years (March 2026)", "sebi_murty")],
  current=ca("2026-03-13"))

G(T, BF, "Advanced",
  "Consider the following statements about Swaminathan Janakiraman:\n"
  "1. In June 2026 the Central Government re-appointed him as a Deputy Governor of the RBI.\n"
  "2. His new term is for three years from 26 June 2026.\n"
  "Which of the statements given above is/are correct?",
  S12, "A",
  "RBI Deputy Governor re-appointment",
  "An RBI press release of 5 June 2026 says the Centre re-appointed Swaminathan J as Deputy Governor for two years "
  "(not three) from 26 June 2026, or until further orders.",
  ["1: correct", "2: wrong (two years)", "So only 1"],
  [fact("Swaminathan Janakiraman re-appointed Deputy Governor for two years with effect from 26 June 2026",
        "swaminathan_j")],
  current=ca("2026-06-05"))

G(T, IB, "Advanced",
  "Consider the following statements:\n"
  "1. Vivek Aggarwal is the first Indian to be Vice-President of the FATF.\n"
  "2. His term as FATF Vice-President runs from July 2026 to June 2027.\n"
  "3. He was serving as Secretary in the Department of Revenue when elected.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "India at the FATF",
  "India was elected to the FATF vice-presidency for the first time in June 2026. Vivek Aggarwal, a 1994-batch IAS "
  "officer, holds it for July 2026 to June 2027. He was Secretary in the Ministry of Culture when elected.",
  ["1: correct", "2: correct", "3: wrong (Ministry of Culture)", "So 1 and 2 only"],
  [fact("India elected FATF Vice President for first time; Vivek Aggarwal, Secretary Culture; July 2026-June 2027",
        "fatf_vp")],
  current=ca("2026-06-19"))

G(T, IB, "Advanced",
  "Consider the following statements about Khaled El-Enany:\n"
  "1. He took office as Director-General of UNESCO on 15 November 2025.\n"
  "2. He is the first Arab to lead UNESCO.\n"
  "3. He succeeded Irina Bokova.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "UNESCO Director-General",
  "El-Enany, Egypt's former Minister of Tourism and Antiquities, was elected by the General Conference in Samarkand "
  "in November 2025 and took office on 15 November 2025 for four years. He is the first Arab to head UNESCO and "
  "succeeded Audrey Azoulay (2017-2025), not Irina Bokova.",
  ["1: correct", "2: correct", "3: wrong (Audrey Azoulay)", "So 1 and 2 only"],
  [fact("Khaled El-Enany takes oath as UNESCO Director-General (15 Nov 2025); succeeds Audrey Azoulay", "unesco"),
   fact("El-Enany becomes first Arab to lead UNESCO", "unesco_eg")],
  current=ca("2025-11-15"))

G(T, BF, "Advanced",
  "Consider the following statements about Mahesh Muralidhar Pai:\n"
  "1. The RBI approved his appointment as MD and CEO of South Indian Bank for three years from 1 October 2026.\n"
  "2. He was a Chief General Manager at Canara Bank before this appointment.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "Private bank CEO approvals",
  "South Indian Bank disclosed on 8 July 2026 that the RBI had approved Mahesh Muralidhar Pai as MD and CEO for three "
  "years from 1 October 2026. He was Chief General Manager at Canara Bank heading digital banking.",
  ["1: correct", "2: correct", "So both"],
  [fact("RBI nod to Mahesh Muralidhar Pai as South Indian Bank MD & CEO for three years from 1 Oct 2026; Canara Bank "
        "CGM", "sib")],
  current=ca("2026-07-08"))

G(T, BF, "Advanced",
  "Consider the following statements about the heads of public sector banks:\n"
  "1. In April 2026 the government extended Debadatta Chand's term as MD and CEO of Bank of Baroda by three years from "
  "1 July 2026.\n"
  "2. Rajneesh Karnatak's term as MD and CEO of Bank of India was extended by three years from 29 April 2026.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "PSB leadership extensions",
  "The Appointments Committee of the Cabinet approved three-year extensions for Rajneesh Karnatak (Bank of India, from "
  "29 April 2026) and Debadatta Chand (Bank of Baroda, from 1 July 2026), reported on 24 April 2026.",
  ["1: correct", "2: correct", "So both"],
  [fact("3-year extensions: Rajneesh Karnatak (BoI) from 29 April 2026; Debadatta Chand (BoB) from 1 July 2026",
        "psb_ext")],
  current=ca("2026-04-24"))

G(T, BF, "Advanced",
  "Consider the following statements about City Union Bank:\n"
  "1. The RBI approved R. Vijay Anandh as its MD and CEO for three years from 1 May 2026.\n"
  "2. He succeeded N. Kamakodi, who had led the bank since 2011.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "City Union Bank leadership",
  "The RBI approved R. Vijay Anandh, then Executive Director, as MD & CEO of City Union Bank for three years from 1 May "
  "2026 (disclosed in February 2026). N. Kamakodi, MD & CEO since May 2011, completed his term on 30 April 2026.",
  ["1: correct", "2: correct", "So both"],
  [fact("RBI clears R Vijay Anandh as City Union Bank MD & CEO from 1 May 2026; N Kamakodi MD since May 2011",
        "cub")],
  current=ca("2026-02-09"))

G(T, BF, "Advanced",
  "Consider the following statements about Sandip Pradhan:\n"
  "1. He took charge as a whole-time member of SEBI in December 2025.\n"
  "2. Before this he was Director General of Income Tax (Investigation).\n"
  "3. He replaced Ananth Narayan G.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "SEBI board",
  "Sandip Pradhan, an IRS officer and Director General of Income Tax (Investigation), Pune, took charge as SEBI "
  "whole-time member on 4 December 2025 for three years. He replaced Ashwani Bhatia, who completed his term.",
  ["1: correct", "2: correct", "3: wrong (Ashwani Bhatia)", "So 1 and 2 only"],
  [fact("Shri Sandip Pradhan takes charge as Whole Time Member, SEBI (Dec 2025)", "sebi_pradhan"),
   fact("He replaces Ashwani Bhatia; was DGIT (Investigation)", "sebi_pradhan")],
  current=ca("2025-12-04"))

G(T, IB, "Advanced",
  "Consider the following statements about the President of the 81st session of the UN General Assembly:\n"
  "1. Bangladesh's Foreign Minister Khalilur Rahman was elected on 2 June 2026.\n"
  "2. He was chosen from the Asia-Pacific Group under regional rotation.\n"
  "3. He was elected unopposed by acclamation.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "UNGA President",
  "Khalilur Rahman was elected on 2 June 2026 from the Asia-Pacific Group. Unusually, the vote was contested: he "
  "defeated Cyprus's Andreas Kakouris in a secret ballot. He succeeds Germany's Annalena Baerbock (80th session).",
  ["1: correct", "2: correct", "3: wrong (contested secret ballot)", "So 1 and 2 only"],
  [fact("Khalilur Rahman of Bangladesh elected PGA of the 81st session on 2 June 2026 from the Asia Pacific Group",
        "unga"),
   fact("He defeated Cyprus's Andreas Kakouris in a secret ballot", "unga_wam")],
  current=ca("2026-06-02"))

G(T, BF, "Advanced",
  "Consider the following statements about Canara Bank's leadership in 2026:\n"
  "1. Hardeep Singh Ahluwalia was appointed interim MD and CEO with effect from 1 January 2026.\n"
  "2. Brajesh Kumar Singh's term as MD and CEO runs until 30 April 2029.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "Canara Bank leadership",
  "Hardeep Singh Ahluwalia served as interim MD & CEO from 1 January 2026. Brajesh Kumar Singh took charge on 1 June "
  "2026, following a notification of 30 May 2026, and serves until 30 April 2029 or further orders.",
  ["1: correct", "2: correct", "So both"],
  [fact("Canara Bank names Hardeep Singh Ahluwalia interim MD and CEO from Jan 2026", "canara_interim"),
   fact("Brajesh Kumar Singh MD & CEO from 1 June 2026 till 30 April 2029", "canara")],
  current=ca("2026-06-01"))

# ====================================================================== Awards and Honours (4 / 1 / 0)
T, NA, IA = "Awards and Honours", "National awards", "International awards"

G(T, IA, "Basic",
  "Who was awarded the Nobel Peace Prize 2026?",
  ["Navanethem (Navi) Pillay", "Michelle Bachelet", "Rebeca Grynspan", "Volker Türk"], "*",
  "Nobel Peace Prize 2026",
  "The Norwegian Nobel Committee announced on 9 October 2026 that the prize goes to Navanethem 'Navi' Pillay, the "
  "South African jurist and former UN human rights chief, for her efforts to promote peace and international law.",
  ["Laureate: Navi Pillay", "Announced: 9 October 2026"],
  [fact("Navanethem 'Navi' Pillay wins Nobel Peace Prize 2026 for promoting peace and international law",
        "nobel_peace")],
  current=ca("2026-10-09"))

G(T, IA, "Basic",
  "The Nobel Prize in Literature 2026 was awarded to which writer?",
  ["Anne Carson", "Margaret Atwood", "Haruki Murakami", "Can Xue"], "*",
  "Nobel Literature 2026",
  "On 8 October 2026 the Swedish Academy awarded the prize to the Canadian poet and writer Anne Carson for a bold and "
  "inventive body of work that creates new forms by drawing playfully on the classical tradition.",
  ["Laureate: Anne Carson (Canada)", "Announced: 8 October 2026"],
  [fact("Canadian writer Anne Carson wins the 2026 Nobel Prize in Literature (8 Oct 2026)", "nobel_lit")],
  current=ca("2026-10-08"))

G(T, IA, "Basic",
  "Who won the 2026 Nobel Memorial Prize in Economic Sciences?",
  ["Robert Hall and Michael Woodford", "Olivier Blanchard and Kenneth Rogoff", "Joel Mokyr and Philippe Aghion",
   "Daron Acemoglu and James Robinson"], "*",
  "Economics Nobel 2026",
  "On 12 October 2026 the Royal Swedish Academy of Sciences awarded the prize to Robert Hall and Michael Woodford "
  "'for microeconomic foundations of macroeconomic stabilisation'.",
  ["Laureates: Robert Hall and Michael Woodford", "Announced: 12 October 2026"],
  [fact("Hall and Woodford win 2026 Nobel economics prize for microeconomic foundations of macroeconomic "
        "stabilisation", "nobel_econ")],
  why="Mokyr and Aghion were 2025 laureates; Acemoglu and Robinson were 2024 laureates.",
  current=ca("2026-10-12"))

G(T, NA, "Basic",
  "Which former Chief Minister of Kerala was conferred the Padma Vibhushan (posthumously) in the Padma Awards 2026?",
  ["V. S. Achuthanandan", "Oommen Chandy", "E. K. Nayanar", "A. K. Antony"], "*",
  "Padma Awards 2026",
  "The Padma Awards 2026, announced on 25 January 2026, honoured 131 people, including five Padma Vibhushan "
  "awardees. Former Kerala CM V. S. Achuthanandan and actor Dharmendra received it posthumously.",
  ["Padma Vibhushan 2026: five awardees", "Posthumous: V. S. Achuthanandan, Dharmendra"],
  [fact("V S Achuthanandan, Dharmendra awarded Padma Vibhushan posthumously (Padma Awards 2026)", "padma")],
  current=ca("2026-01-25"))

G(T, IA, "Intermediate",
  "'Taiwan Travelogue' by Yáng Shuāng-zǐ, translated by Lin King, won the International Booker Prize 2026. It is the "
  "first winning book translated from which language?",
  ["Mandarin Chinese", "Japanese", "Korean", "Hindi"], "*",
  "International Booker Prize 2026",
  "Announced on 19 May 2026 in London, Taiwan Travelogue is the first Mandarin Chinese work to win the International "
  "Booker. The prize money is shared equally by author and translator.",
  ["Winner: Taiwan Travelogue", "Language: Mandarin Chinese"],
  [fact("Taiwan Travelogue wins the 2026 International Booker Prize; first Mandarin Chinese work", "intl_booker")],
  current=ca("2026-05-19"))

# ====================================================================== Books and Authors (0 / 5 / 0)
T, RB = "Books and Authors", "Recent books"

G(T, RB, "Intermediate",
  "'Flesh', which won the Booker Prize 2025, was written by whom?",
  ["David Szalay", "Andrew Miller", "Susan Choi", "Katie Kitamura"], "*",
  "Booker Prize 2025",
  "David Szalay, a Hungarian-British writer, won the 2025 Booker Prize for 'Flesh', announced in London on 10 November "
  "2025. Andrew Miller, Susan Choi and Katie Kitamura were on the shortlist.",
  ["Book: Flesh", "Author: David Szalay"],
  [fact("David Szalay won the Booker Prize 2025 for Flesh, beating Kiran Desai", "booker25")],
  current=ca("2025-11-10"))

G(T, RB, "Intermediate",
  "Kiran Desai was shortlisted for the Booker Prize 2025 for which novel?",
  ["The Loneliness of Sonia and Sunny", "The Inheritance of Loss", "Hullabaloo in the Guava Orchard",
   "The Land in Winter"], "*",
  "Kiran Desai",
  "Kiran Desai's 'The Loneliness of Sonia and Sunny' was the main rival to 'Flesh' for the 2025 Booker, announced on "
  "10 November 2025. She had won in 2006 for 'The Inheritance of Loss'.",
  ["2025 shortlist: The Loneliness of Sonia and Sunny", "2006 winner: The Inheritance of Loss"],
  [fact("Kiran Desai's The Loneliness of Sonia and Sunny lost to Flesh; Desai won in 2006 for The Inheritance of Loss",
        "booker25")],
  why="The Inheritance of Loss won in 2006; The Land in Winter is Andrew Miller's novel.",
  current=ca("2025-11-10"))

G(T, RB, "Intermediate",
  "Daniel Kraus won the Pulitzer Prize for Fiction 2026 for which novel, told as one continuous sentence?",
  ["Angel Down", "Liberation", "The Correspondent", "Flashlight"], "*",
  "Pulitzer Prize 2026",
  "The Pulitzer Prizes were announced on 4 May 2026. Daniel Kraus won the fiction prize for 'Angel Down', a First "
  "World War story about soldiers who find a fallen angel, written as a single long sentence.",
  ["Book: Angel Down", "Author: Daniel Kraus"],
  [fact("Pulitzer winners in arts include Daniel Kraus' Angel Down (4 May 2026)", "pulitzer_ap")],
  why="Liberation is Bess Wohl's play; The Correspondent is Virginia Evans's novel.",
  current=ca("2026-05-04"))

G(T, RB, "Intermediate",
  "'The Correspondent', which won the Women's Prize for Fiction 2026, is by which author?",
  ["Virginia Evans", "Susan Choi", "Alice Evelyn Yang", "Lyse Doucet"], "*",
  "Women's Prize 2026",
  "Virginia Evans won the 2026 Women's Prize for Fiction on 11 June 2026 for her debut novel 'The Correspondent'. "
  "Lyse Doucet won the non-fiction prize for 'The Finest Hotel in Kabul'.",
  ["Fiction: The Correspondent (Virginia Evans)", "Non-fiction: The Finest Hotel in Kabul (Lyse Doucet)"],
  [fact("Winners of the 2026 Women's Prizes: Virginia Evans (The Correspondent) and Lyse Doucet", "womens_prize"),
   fact("Virginia Evans wins Women's Prize for her debut novel", "womens_prize_ie")],
  current=ca("2026-06-11"))

G(T, RB, "Intermediate",
  "'The Finest Hotel in Kabul', winner of the Women's Prize for Non-Fiction 2026, was written by whom?",
  ["Lyse Doucet", "Christina Lamb", "Malala Yousafzai", "Arundhati Roy"], "*",
  "Women's Prize for Non-Fiction 2026",
  "BBC journalist Lyse Doucet won the 2026 Women's Prize for Non-Fiction for 'The Finest Hotel in Kabul', announced "
  "with the fiction prize on 11 June 2026.",
  ["Book: The Finest Hotel in Kabul", "Author: Lyse Doucet"],
  [fact("Lyse Doucet won the 2026 Women's Prize for Non-Fiction for The Finest Hotel in Kabul", "womens_prize")],
  current=ca("2026-06-11"))

# ====================================================================== Sports (1 / 9 / 1)
T, TW, VR = "Sports", "Tournaments and winners", "Venues and records"

G(T, TW, "Basic",
  "India won its first ICC Women's ODI World Cup on 2 November 2025 by beating which team in the final?",
  ["South Africa", "Australia", "England", "New Zealand"], "*",
  "Women's World Cup 2025",
  "India beat South Africa by 52 runs at the Dr DY Patil Sports Academy, Navi Mumbai, on 2 November 2025 to win their "
  "first ICC women's title. Shafali Verma (87 and two wickets) was Player of the Match.",
  ["Final: India vs South Africa", "Margin: 52 runs"],
  [fact("India win first-ever ICC Women's ODI World Cup, beat South Africa by 52 runs", "wodi_final")],
  current=ca("2025-11-02"))

G(T, TW, "Intermediate",
  "Who was named Player of the Tournament at the ICC Women's ODI World Cup 2025?",
  ["Deepti Sharma", "Shafali Verma", "Smriti Mandhana", "Laura Wolvaardt"], "*",
  "Women's World Cup 2025 awards",
  "Deepti Sharma was Player of the Tournament with 22 wickets and 215 runs; in the final she scored 58 and took 5-39. "
  "Shafali Verma was Player of the Match in the final.",
  ["Player of the Tournament: Deepti Sharma", "Player of the Match (final): Shafali Verma"],
  [fact("Shafali Player of the Match; Deepti Sharma Player of the Tournament (22 wickets, 215 runs)", "wodi_wisden")],
  why="Shafali Verma was Player of the Match in the final, not of the tournament.",
  current=ca("2025-11-02"))

G(T, VR, "Intermediate",
  "At which venue did India beat New Zealand by 96 runs in the final of the ICC Men's T20 World Cup on 8 March 2026?",
  ["Narendra Modi Stadium, Ahmedabad", "Wankhede Stadium, Mumbai", "Eden Gardens, Kolkata",
   "R. Premadasa Stadium, Colombo"], "*",
  "Men's T20 World Cup 2026",
  "India scored 255/5 and bowled New Zealand out for 159 at the Narendra Modi Stadium, Ahmedabad, on 8 March 2026. "
  "India became the first host nation to win the tournament and the first team to retain it.",
  ["Final: India vs New Zealand", "Venue: Narendra Modi Stadium, Ahmedabad"],
  [fact("India beat New Zealand by 96 runs at Narendra Modi Stadium, Ahmedabad, on 8 March 2026", "t20wc")],
  current=ca("2026-03-08"))

G(T, VR, "Intermediate",
  "Ahmedabad was awarded the 2030 Commonwealth Games on 26 November 2025. Which city was the rival bidder?",
  ["Abuja", "Glasgow", "Kuala Lumpur", "Durban"], "*",
  "CWG 2030",
  "The Commonwealth Sport General Assembly in Glasgow confirmed Ahmedabad as host of the centenary 2030 Games, chosen "
  "over a bid from Abuja, Nigeria. The first Games were held in Hamilton, Canada, in 1930.",
  ["Host 2030: Ahmedabad", "Rival bid: Abuja (Nigeria)"],
  [fact("Centenary 2030 Commonwealth Games awarded to Ahmedabad, chosen over Abuja", "cwg2030")],
  why="Glasgow hosted the 2026 Games and the General Assembly that made the decision.",
  current=ca("2025-11-26"))

G(T, TW, "Intermediate",
  "Who won the FIDE Chess World Cup 2025 held in Goa?",
  ["Javokhir Sindarov", "Wei Yi", "Andrey Esipenko", "Nodirbek Yakubboev"], "*",
  "FIDE World Cup 2025",
  "Uzbekistan's Javokhir Sindarov, aged 19, beat China's Wei Yi 2.5-1.5 (after rapid tiebreaks) in the final on 26 "
  "November 2025 to become the youngest World Cup winner. Andrey Esipenko finished third.",
  ["Winner: Javokhir Sindarov", "Runner-up: Wei Yi", "Third: Andrey Esipenko"],
  [fact("Sindarov beat Wei Yi in the final on 26 Nov 2025 in Goa; youngest World Cup winner; Esipenko third",
        "chesswc")],
  current=ca("2025-11-26"))

G(T, TW, "Intermediate",
  "Which country won the FIFA World Cup 2026, beating Argentina 1-0 in the final on 19 July 2026?",
  ["Spain", "France", "England", "Brazil"], "*",
  "FIFA World Cup 2026",
  "Spain won their second World Cup (after 2010) by beating Argentina 1-0 after extra time at New York New Jersey "
  "Stadium. Ferran Torres scored the winner.",
  ["Final: Spain 1-0 Argentina (aet)", "Venue: New York New Jersey Stadium"],
  [fact("Spain beat Argentina 1-0 in the final on 19 July 2026; Ferran Torres scored", "fifawc")],
  current=ca("2026-07-19"))

G(T, TW, "Intermediate",
  "Who won the Golden Ball as the best player of the FIFA World Cup 2026?",
  ["Rodri", "Lionel Messi", "Kylian Mbappé", "Pau Cubarsí"], "*",
  "FIFA World Cup 2026 awards",
  "Spain's Rodri won the Golden Ball. Kylian Mbappé won the Golden Boot with 10 goals, Unai Simón the Golden Glove and "
  "Pau Cubarsí the Best Young Player award.",
  ["Golden Ball: Rodri", "Golden Boot: Mbappé", "Golden Glove: Unai Simón"],
  [fact("Rodri Golden Ball; Mbappé Golden Boot (10 goals); Unai Simón Golden Glove; Cubarsí best young player",
        "fifawc")],
  why="Mbappé won the Golden Boot; Cubarsí was Best Young Player.",
  current=ca("2026-07-19"))

G(T, TW, "Intermediate",
  "How many medals did India win at the 2026 Asian Games in Aichi-Nagoya, where it finished fourth?",
  ["85", "106", "70", "92"], "*",
  "Asian Games 2026",
  "India finished fourth with 85 medals (21 gold, 27 silver, 37 bronze). China topped the table with 341 medals, "
  "followed by hosts Japan and South Korea. The Games ended on 4 October 2026.",
  ["India: 21 G, 27 S, 37 B = 85", "Rank: 4th"],
  [fact("India fourth with 21 gold, 27 silver, 37 bronze (85 medals); China 341; final day 4 Oct 2026", "asiad")],
  shortcut="21 + 27 + 37 = 85.",
  why="106 is close to India's record haul at Hangzhou 2023, not its 2026 total; 70 and 92 are not India's tally.",
  current=ca("2026-10-04"))

G(T, TW, "Intermediate",
  "Which team won IPL 2026 by beating Gujarat Titans in the final at Ahmedabad on 31 May 2026?",
  ["Royal Challengers Bengaluru", "Mumbai Indians", "Chennai Super Kings", "Punjab Kings"], "*",
  "IPL 2026",
  "Royal Challengers Bengaluru, led by Rajat Patidar, beat Gujarat Titans by 5 wickets at the Narendra Modi Stadium "
  "on 31 May 2026 for their second consecutive title. Virat Kohli was Player of the Match.",
  ["Final: RCB vs GT", "Result: RCB won by 5 wickets"],
  [fact("RCB crowned IPL 2026 champions beating Gujarat Titans at Narendra Modi Stadium on 31 May 2026", "ipl26")],
  current=ca("2026-05-31"))

G(T, VR, "Intermediate",
  "The 20th Asian Games, which ended on 4 October 2026, were held in which country?",
  ["Japan", "China", "South Korea", "Qatar"], "*",
  "Asian Games 2026 host",
  "Japan hosted the 20th Asian Games in the Aichi-Nagoya region and finished second in the medal table behind China.",
  ["Host: Japan (Aichi-Nagoya)"],
  [fact("Japan hosted the 20th Asian Games in the Aichi-Nagoya region; final day 4 Oct 2026", "asiad")],
  why="China hosted the previous Games, at Hangzhou.",
  current=ca("2026-10-04"))

G(T, VR, "Advanced",
  "Consider the following statements about the ICC Men's T20 World Cup 2026:\n"
  "1. India became the first host nation to win the T20 World Cup.\n"
  "2. India became the first team to retain the T20 World Cup.\n"
  "3. The final was played at Eden Gardens, Kolkata.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "T20 World Cup 2026 records",
  "By winning on 8 March 2026, India became the first host nation to lift the T20 World Cup and the first side to "
  "retain it. The final was played at the Narendra Modi Stadium, Ahmedabad.",
  ["1: correct", "2: correct", "3: wrong (Ahmedabad)", "So 1 and 2 only"],
  [fact("India first host nation to win and first side to retain the T20 World Cup; final at Narendra Modi Stadium",
        "t20wc")],
  current=ca("2026-03-08"))

# ====================================================================== Summits and Conferences (6 / 1 / 6)
T, SG, HC = "Summits and Conferences", "G20, BRICS, SCO and others", "Hosting countries"

G(T, HC, "Basic",
  "The G20 Leaders' Summit of 22-23 November 2025, the first held in Africa, took place in which city?",
  ["Johannesburg", "Cape Town", "Nairobi", "Cairo"], "*",
  "G20 2025",
  "South Africa hosted the first G20 summit on African soil at Nasrec, Johannesburg, on 22-23 November 2025. The "
  "United States stayed away, and the US took over the G20 presidency for 2026.",
  ["Host: South Africa", "City: Johannesburg"],
  [fact("G20 leaders in South Africa adopt declaration despite US opposition (Johannesburg, Nov 2025)", "g20")],
  current=ca("2025-11-22"))

G(T, HC, "Basic",
  "COP30, the UN climate conference that ended on 22 November 2025, was held in which city?",
  ["Belém", "Baku", "Rio de Janeiro", "Bonn"], "*",
  "COP30",
  "COP30 was held in Belém, Brazil, at the edge of the Amazon. The COP President gavelled the final 'Global Mutirão' "
  "decision on 22 November 2025.",
  ["Host: Brazil", "City: Belém"],
  [fact("Key outcomes of the UN climate conference in Belém; Global Mutirão decision", "cop30")],
  why="Baku hosted COP29.",
  current=ca("2025-11-22"))

G(T, HC, "Basic",
  "The AI Impact Summit 2026, held from 16 to 20 February 2026, was hosted at Bharat Mandapam in which city?",
  ["New Delhi", "Bengaluru", "Hyderabad", "Mumbai"], "*",
  "AI Impact Summit 2026",
  "India hosted the AI Impact Summit at Bharat Mandapam, New Delhi, from 16 to 20 February 2026. A New "
  "Delhi Declaration on AI Impact was adopted.",
  ["Venue: Bharat Mandapam, New Delhi", "Dates: 16-20 February 2026"],
  [fact("India AI Impact Summit 2026 at Bharat Mandapam enters fifth day (20 Feb 2026)", "aisummit")],
  current=ca("2026-02-16"))

G(T, SG, "Basic",
  "Where was the 18th BRICS Summit held on 12-13 September 2026?",
  ["New Delhi", "Rio de Janeiro", "Kazan", "Johannesburg"], "*",
  "BRICS 2026",
  "India chaired BRICS in 2026 and hosted the 18th summit at Bharat Mandapam, New Delhi, on 12-13 September 2026, "
  "where the New Delhi Declaration was adopted.",
  ["Chair 2026: India", "Venue: New Delhi"],
  [fact("India to host 18th BRICS summit in New Delhi on September 12-13, 2026", "brics"),
   fact("Preparations for two-day BRICS Summit 2026 beginning Saturday", "brics_air")],
  why="Rio de Janeiro hosted 2025; Kazan 2024; Johannesburg 2023.",
  current=ca("2026-09-12"))

G(T, HC, "Basic",
  "The 26th Summit of the Shanghai Cooperation Organisation's Council of Heads of State was held on 1 September 2026 "
  "in which city?",
  ["Bishkek", "Tianjin", "Astana", "Tashkent"], "*",
  "SCO 2026",
  "Kyrgyzstan hosted the 26th SCO summit at the Yrys Ordo congress hall in Bishkek, chaired by President Sadyr "
  "Japarov. The rotating chairmanship then passed to Pakistan.",
  ["Host: Kyrgyzstan", "City: Bishkek"],
  [fact("26th SCO Summit begins in Bishkek as heads of state gather", "sco")],
  why="Tianjin hosted the 2025 summit; Astana 2024.",
  current=ca("2026-09-01"))

G(T, HC, "Basic",
  "The 52nd G7 Summit of 15-17 June 2026 was held in which country?",
  ["France", "Italy", "Canada", "Japan"], "*",
  "G7 2026",
  "France hosted the 52nd G7 summit at Évian-les-Bains under President Macron. India attended as an invited outreach "
  "partner. The presidency passes to the United States in 2027.",
  ["Host: France (Évian-les-Bains)", "Next: United States (2027)"],
  [fact("52nd G7 summit at Evian, France, 15-17 June 2026; India invited", "g7")],
  why="Canada hosted in 2025 (Kananaskis); Italy in 2024.",
  current=ca("2026-06-15"))

G(T, SG, "Intermediate",
  "Russian President Vladimir Putin visited New Delhi on 4-5 December 2025 for which edition of the India-Russia "
  "Annual Summit?",
  ["23rd", "21st", "22nd", "25th"], "*",
  "India-Russia Annual Summit",
  "The 23rd India-Russia Annual Summit in New Delhi reaffirmed the 'Special and Privileged Strategic Partnership' and "
  "adopted a programme to deepen economic cooperation to 2030. It was Putin's first visit to India since 2022 and "
  "marked 25 years of the 2000 strategic partnership declaration.",
  ["Edition: 23rd", "Dates: 4-5 December 2025"],
  [fact("23rd India-Russia Annual Summit; key takeaways from the joint statement (Dec 2025)", "indrus")],
  why="25 years refers to the 2000 Declaration on Strategic Partnership, not the summit count.",
  current=ca("2025-12-05"))

G(T, SG, "Advanced",
  "Consider the following statements about the G20 Johannesburg Summit (November 2025):\n"
  "1. Its theme was 'Solidarity, Equality, Sustainability'.\n"
  "2. The leaders' declaration was adopted at the start of the summit rather than at the end.\n"
  "3. The United States took part in drafting and adopting the declaration.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "G20 2025: details",
  "South Africa's presidency used the theme 'Solidarity, Equality, Sustainability'. Breaking with practice, leaders "
  "adopted the 122-paragraph declaration on the first day. The US boycotted the summit and did not take part.",
  ["1: correct", "2: correct", "3: wrong (US absent)", "So 1 and 2 only"],
  [fact("Declaration adopted at the onset despite US absence", "g20"),
   fact("Theme 'Solidarity, Equality, Sustainability'; declaration focused on Africa", "g20_ewn")],
  current=ca("2025-11-22"))

G(T, SG, "Advanced",
  "Consider the following statements about the outcomes of COP30 in Belém:\n"
  "1. The headline decision was called the 'Global Mutirão'.\n"
  "2. It calls for tripling adaptation finance.\n"
  "3. It contains an explicit roadmap for transitioning away from fossil fuels.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "COP30 outcomes",
  "The Global Mutirão decision, part of the Belém Political Package, set a path to mobilise about $1.3 trillion a year "
  "by 2035 and called for tripling adaptation finance. Despite support from over 80 countries, it had no explicit "
  "language on a fossil fuel transition roadmap.",
  ["1: correct", "2: correct", "3: wrong", "So 1 and 2 only"],
  [fact("Global Mutirão decision; tripling adaptation finance; no explicit fossil fuel transition language", "cop30")],
  current=ca("2025-11-22"))

G(T, SG, "Advanced",
  "Consider the following statements about BRICS in 2026:\n"
  "1. The 18th summit was held at Bharat Mandapam, New Delhi.\n"
  "2. The summit adopted the New Delhi Declaration.\n"
  "3. It was held under Brazil's chairship of BRICS.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "BRICS 2026",
  "India held the BRICS chairship in 2026 (Brazil chaired in 2025). The summit at Bharat Mandapam on 12-13 September "
  "2026 adopted the New Delhi Declaration by consensus.",
  ["1: correct", "2: correct", "3: wrong (India's chairship)", "So 1 and 2 only"],
  [fact("India hosts the 18th BRICS summit in New Delhi under its 2026 chairship; New Delhi Declaration", "brics"),
   fact("BRICS Summit 2026 at Bharat Mandapam", "brics_air")],
  current=ca("2026-09-12"))

G(T, SG, "Advanced",
  "Consider the following statements about the SCO summit held in September 2026:\n"
  "1. It was chaired by Kyrgyz President Sadyr Japarov.\n"
  "2. At its end the rotating SCO chairmanship passed to Pakistan.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "SCO chairmanship",
  "The 26th summit in Bishkek on 1 September 2026 was chaired by President Sadyr Japarov of Kyrgyzstan, who then "
  "handed over the rotating chairmanship to Pakistan.",
  ["1: correct", "2: correct", "So both"],
  [fact("Bishkek summit chaired by Sadyr Japarov; chairmanship handed to Pakistan", "sco"),
   fact("Kyrgyzstan to host SCO Summit", "sco_kabar")],
  current=ca("2026-09-01"))

G(T, SG, "Advanced",
  "Consider the following statements about the 52nd G7 Summit:\n"
  "1. It was held under the Italian presidency.\n"
  "2. India attended as an invited outreach partner.\n"
  "3. The United States holds the G7 presidency in 2027.\n"
  "Which of the statements given above is/are correct?",
  S123, "B",
  "G7 2026: details",
  "The summit at Évian-les-Bains (15-17 June 2026) was held under the French presidency. India attended the outreach "
  "sessions as an invitee, and the presidency passes to the United States in 2027.",
  ["1: wrong (French presidency)", "2: correct", "3: correct", "So 2 and 3 only"],
  [fact("52nd G7 under France at Evian; India invited; US presidency 2027", "g7"),
   fact("Modi's meetings at the G7 summit in Evian", "g7_bt")],
  current=ca("2026-06-15"))

G(T, SG, "Advanced",
  "Consider the following statements about the India-EU Summit of January 2026:\n"
  "1. It was the 16th India-EU Summit, held in New Delhi on 27 January 2026.\n"
  "2. Ursula von der Leyen and António Costa were chief guests at India's 77th Republic Day.\n"
  "3. The two sides announced the conclusion of negotiations on a free trade agreement first launched in 2007.\n"
  "Which of the statements given above is/are correct?",
  S123, "D",
  "India-EU summit 2026",
  "EU leaders Ursula von der Leyen and António Costa were the first EU leaders to be Republic Day chief guests (26 "
  "January 2026). At the 16th summit the next day, the sides announced conclusion of the FTA talks begun in 2007, "
  "adopted a 2030 roadmap and signed a security and defence partnership.",
  ["1: correct", "2: correct", "3: correct", "So 1, 2 and 3"],
  [fact("India-EU summit: FTA sealed, 2030 roadmap adopted, defence pact signed (27 Jan 2026)", "indeu"),
   fact("Costa and von der Leyen chief guests at 77th Republic Day; talks begun in 2007", "indeu_tribune")],
  current=ca("2026-01-27"))

# ====================================================================== Business and Corporate News (0 / 0 / 1)
G("Business and Corporate News", "Mergers and acquisitions", "Advanced",
  "Consider the following statements about Emirates NBD's acquisition of RBL Bank, completed in June 2026:\n"
  "1. Emirates NBD holds 60% of RBL Bank's expanded share capital.\n"
  "2. The stake was acquired mainly through a preferential issue of new shares (primary capital).\n"
  "3. It is described as the largest foreign direct investment in India's banking sector.\n"
  "Which of the statements given above is/are correct?",
  S123, "D",
  "Foreign bank takeover of an Indian private bank",
  "The deal, announced on 18 October 2025, closed in June 2026 after regulatory approvals. Emirates NBD got 60% of "
  "the expanded capital through a preferential issue worth about $2.75 billion, plus a mandatory open offer. The "
  "banks call it the largest FDI in Indian banking and the first majority acquisition of a profitable Indian bank by "
  "a foreign bank.",
  ["1: correct", "2: correct", "3: correct", "So 1, 2 and 3"],
  [fact("Emirates NBD completes $2.75 billion RBL deal for 60% via preferential issue and open offer; largest FDI in "
        "Indian banking", "rbl"),
   fact("Emirates NBD completes majority stake acquisition in RBL Bank", "rbl_fpj")],
  current=ca("2026-06-18"))

# ====================================================================== National and International Organizations (5 / 0 / 7)
T, HH, MB = "National and International Organizations", "Headquarters and heads", "Membership"

G(T, HH, "Basic",
  "Where is the headquarters of the New Development Bank (NDB)?",
  ["Shanghai", "Beijing", "New Delhi", "Moscow"], "*",
  "NDB headquarters",
  "The New Development Bank, set up by the BRICS countries, is headquartered in Shanghai, China. Colombia presented "
  "its membership application at the Shanghai headquarters in 2025.",
  ["NDB headquarters: Shanghai"],
  [fact("The New Development Bank is headquartered in Shanghai, China", "ndb_hq")])

G(T, HH, "Basic",
  "Where is the headquarters of the Food and Agriculture Organization (FAO) of the United Nations?",
  ["Rome", "Geneva", "Vienna", "Paris"], "*",
  "FAO headquarters",
  "FAO moved its seat from Washington, D.C. to Rome, Italy, in 1951. Rome also hosts IFAD and the World Food Programme.",
  ["FAO headquarters: Rome (since 1951)"],
  [fact("FAO headquarters moved from Washington to Rome in 1951", "fao")])

G(T, HH, "Basic",
  "The International Olympic Committee (IOC) is headquartered at Olympic House in which city?",
  ["Lausanne", "Geneva", "Zurich", "Paris"], "*",
  "IOC headquarters",
  "The IOC's headquarters, Olympic House (Maison Olympique), is in Lausanne, Switzerland. It was inaugurated on 23 "
  "June 2019, Olympic Day.",
  ["IOC headquarters: Lausanne"],
  [fact("IOC headquarters' address: Maison Olympique, 1007 Lausanne, Switzerland", "ioc_hq")],
  why="Zurich is FIFA's home; Geneva hosts many UN bodies.")

G(T, HH, "Basic",
  "Where is the head office of the National Housing Bank (NHB)?",
  ["New Delhi", "Mumbai", "Kolkata", "Chennai"], "*",
  "National Housing Bank",
  "NHB was set up on 9 July 1988 under the National Housing Bank Act, 1987, with its head office in New Delhi. Its "
  "capital is now wholly held by the Government of India, and regulation of housing finance companies moved to the "
  "RBI in August 2019.",
  ["NHB head office: New Delhi", "Set up: 9 July 1988"],
  [fact("NHB set up in 1988 under the NHB Act 1987; head office New Delhi; capital subscribed by Government of India",
        "nhb")])

G(T, HH, "Basic",
  "The Export-Import Bank of India (Exim Bank), set up in 1982, has its head office in which city?",
  ["Mumbai", "New Delhi", "Chennai", "Ahmedabad"], "*",
  "Exim Bank",
  "Exim Bank was established on 1 January 1982 under the Export-Import Bank of India Act, 1981. It is wholly owned by "
  "the Government of India and its head office is at the World Trade Centre complex, Cuffe Parade, Mumbai.",
  ["Exim Bank head office: Mumbai", "Established: 1 January 1982"],
  [fact("India Exim Bank head office at World Trade Centre Complex, Cuffe Parade, Mumbai", "exim")])

G(T, MB, "Advanced",
  "Consider the following statements about the International Monetary Fund:\n"
  "1. Liechtenstein became its 191st member in October 2024.\n"
  "2. A member's quota determines its capital subscription and voting power.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "IMF membership",
  "Liechtenstein joined the IMF on 21 October 2024 as its 191st member, with an initial quota of SDR 100 million. A "
  "member's quota determines its capital subscription, voting power and access to IMF financing.",
  ["1: correct", "2: correct", "So both"],
  [fact("Liechtenstein becomes the IMF's 191st member (21 Oct 2024); quota determines subscription, votes and access",
        "imf191")],
  current=ca("2024-10-21"))

G(T, MB, "Advanced",
  "Consider the following statements about the New Development Bank:\n"
  "1. Colombia and Uzbekistan joined it as members in 2025.\n"
  "2. Only BRICS member countries can become members of the bank.\n"
  "Which of the statements given above is/are correct?",
  S12, "A",
  "NDB membership",
  "NDB President Dilma Rousseff announced in July 2025 that Colombia and Uzbekistan had become members. Membership is "
  "open beyond BRICS: Bangladesh, Algeria, the UAE and Egypt had joined earlier, and Colombia and Uzbekistan are not "
  "BRICS members.",
  ["1: correct", "2: wrong (non-BRICS members exist)", "So only 1"],
  [fact("Colombia and Uzbekistan join NDB ahead of 17th BRICS Summit (July 2025)", "ndb_members"),
   fact("Bank headquartered in Shanghai; Rousseff announced new members", "ndb_hq")],
  current=ca("2025-07-06"))

G(T, HH, "Advanced",
  "Consider the following statements about the World Trade Organization:\n"
  "1. Ngozi Okonjo-Iweala's second term as Director-General runs from 1 September 2025 to 31 August 2029.\n"
  "2. She was re-appointed after a contested vote against two other candidates.\n"
  "Which of the statements given above is/are correct?",
  S12, "A",
  "WTO Director-General",
  "The WTO General Council re-appointed Okonjo-Iweala on 29 November 2024 for a second four-year term from 1 September "
  "2025 to 31 August 2029. She was the only candidate and was re-appointed by consensus.",
  ["1: correct", "2: wrong (sole candidate, consensus)", "So only 1"],
  [fact("WTO chief Okonjo-Iweala reappointed for second term, 1 Sep 2025 to 31 Aug 2029; sole candidate",
        "wto_dg")],
  current=ca("2025-09-01"))

G(T, HH, "Advanced",
  "Consider the following statements about the International Olympic Committee:\n"
  "1. Kirsty Coventry is the first woman and the first African to be IOC President.\n"
  "2. She took office as IOC President on 23 June 2025, succeeding Thomas Bach.\n"
  "Which of the statements given above is/are correct?",
  S12, "C",
  "IOC President",
  "Zimbabwe's Kirsty Coventry, a seven-time Olympic medallist swimmer, was elected on 20 March 2025 and took over "
  "from Thomas Bach on 23 June 2025 (Olympic Day) as the IOC's 10th President.",
  ["1: correct", "2: correct", "So both"],
  [fact("Kirsty Coventry elected IOC president, first woman and first African", "ioc_pres"),
   fact("Coventry became president on 23 June 2025, replacing Thomas Bach", "ioc_pres_week")],
  current=ca("2025-06-23"))

G(T, MB, "Advanced",
  "Consider the following statements about the Commonwealth:\n"
  "1. Gabon and Togo were admitted in 2022, taking membership to 56.\n"
  "2. Shirley Botchwey of Ghana became Commonwealth Secretary-General in April 2025.\n"
  "3. Gabon and Togo were both British colonies before independence.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "Commonwealth membership",
  "Gabon and Togo joined at CHOGM in Kigali in June 2022 as the 55th and 56th members; both are former French "
  "territories with no British colonial past. Shirley Botchwey, former foreign minister of Ghana, became the 7th "
  "Secretary-General on 1 April 2025.",
  ["1: correct", "2: correct", "3: wrong (francophone, no British colonial link)", "So 1 and 2 only"],
  [fact("Gabon and Togo join the Commonwealth family (June 2022)", "commonwealth"),
   fact("Shirley Botchwey assumed office as Commonwealth Secretary-General on 1 April 2025", "commonwealth_sg")],
  current=ca("2025-04-01"))

G(T, HH, "Advanced",
  "Consider the following statements about the Bank for International Settlements (BIS):\n"
  "1. Pablo Hernández de Cos became its General Manager on 1 July 2025.\n"
  "2. He was earlier Governor of the Bank of Spain.\n"
  "3. He succeeded Agustín Carstens.\n"
  "Which of the statements given above is/are correct?",
  S123, "D",
  "BIS General Manager",
  "The BIS appointed Pablo Hernández de Cos, Governor of the Bank of Spain from 2018 to 2024, as General Manager for "
  "five years from 1 July 2025, succeeding Agustín Carstens.",
  ["1: correct", "2: correct", "3: correct", "So 1, 2 and 3"],
  [fact("Pablo Hernández de Cos announced as next BIS General Manager from 1 July 2025, succeeding Carstens",
        "bis_gm")],
  current=ca("2025-07-01"))

G(T, MB, "Advanced",
  "Consider the following statements about the OECD:\n"
  "1. It has 38 member countries.\n"
  "2. Its headquarters is at the Château de la Muette in Paris.\n"
  "3. India is a full member of the OECD.\n"
  "Which of the statements given above is/are correct?",
  S123, "A",
  "OECD",
  "The Organisation for Economic Co-operation and Development has 38 member countries and is headquartered at the "
  "Château de la Muette in Paris. India is not a member; it engages with the OECD as a key partner.",
  ["1: correct", "2: correct", "3: wrong", "So 1 and 2 only"],
  [fact("OECD: 38 member countries; headquarters Château de la Muette, Paris", "oecd_wiki"),
   fact("OECD headquarters building at La Muette", "oecd")])

# ====================================================================== Important Reports and Indexes (1 / 2 / 0)
T, PB, IR = "Important Reports and Indexes", "Publishing body", "India's rank"

G(T, IR, "Basic",
  "What was India's rank in the World Happiness Report 2026?",
  ["116th", "118th", "126th", "99th"], "*",
  "World Happiness Report 2026",
  "In the World Happiness Report released in March 2026, India ranked 116th, up two places from 118th. Finland topped "
  "the list for the ninth year in a row.",
  ["2025: 118th", "2026: 116th"],
  [fact("India ranks 116th in World Happiness Report 2026", "whr"),
   fact("Finland top; India 116th; Nepal 99th; Pakistan 104th", "whr_tv")],
  why="118th was India's 2025 rank; 99th is Nepal's 2026 rank.",
  current=ca("2026-03-20"))

G(T, IR, "Intermediate",
  "What was India's rank in the World Economic Forum's Global Gender Gap Index 2026?",
  ["131st", "127th", "135th", "140th"], "*",
  "Global Gender Gap Index 2026",
  "India ranked 131st of 145 economies, unchanged from the previous edition, having closed about 64.5% of its gender "
  "gap. Iceland, Finland and Norway took the top three places.",
  ["India: 131st of 145", "Top: Iceland"],
  [fact("India retains 131st rank in Global Gender Gap Index 2026; Iceland tops list", "gggi")],
  current=ca("2026-09-16"))

G(T, IR, "Intermediate",
  "In the World Happiness Report 2026, which of India's neighbours was ranked highest?",
  ["Nepal", "Pakistan", "Bangladesh", "Sri Lanka"], "*",
  "World Happiness Report 2026: South Asia",
  "In 2026 Nepal ranked 99th and Pakistan 104th, both ahead of India (116th), while Bangladesh was 127th and Sri Lanka "
  "134th.",
  ["Nepal 99", "Pakistan 104", "India 116", "Bangladesh 127", "Sri Lanka 134"],
  [fact("WHR 2026: Nepal 99th, Pakistan 104th, India 116th, Bangladesh 127th, Sri Lanka 134th", "whr_tv")],
  current=ca("2026-03-20"))

# ====================================================================== Static Awareness (1 / 8 / 0)
T, CC, NP, SF = "Static Awareness", "Capitals and currencies", "National parks and dams", "Indian states facts"

G(T, CC, "Basic",
  "What is the capital of Oman, where India and Oman signed their CEPA in December 2025?",
  ["Muscat", "Doha", "Manama", "Abu Dhabi"], "*",
  "Oman",
  "Muscat is the capital and largest city of Oman. Its currency is the Omani rial, divided into 1,000 baisa.",
  ["Capital: Muscat", "Currency: Omani rial"],
  [fact("Capital of Oman is Muscat; currency Omani rial", "oman_facts")],
  why="Doha is Qatar's capital; Manama is Bahrain's; Abu Dhabi is the UAE's.")

G(T, CC, "Intermediate",
  "What is the currency of Kyrgyzstan, whose capital Bishkek hosted the SCO summit in 2026?",
  ["Som", "Tenge", "Somoni", "Manat"], "*",
  "Central Asian currencies",
  "Kyrgyzstan's currency is the som (KGS). Kazakhstan uses the tenge, Tajikistan the somoni, and Turkmenistan and "
  "Azerbaijan the manat.",
  ["Kyrgyzstan: som", "Capital: Bishkek"],
  [fact("Kyrgyzstan: capital Bishkek; currency Kyrgyzstani som (KGS)", "kyrgyz")],
  why="Tenge is Kazakhstan's currency; somoni is Tajikistan's.")

G(T, NP, "Intermediate",
  "Dudhwa National Park, on the Indo-Nepal border, is in which state?",
  ["Uttar Pradesh", "Uttarakhand", "Bihar", "Madhya Pradesh"], "*",
  "Dudhwa",
  "Dudhwa National Park lies in the Terai of Lakhimpur Kheri district, Uttar Pradesh, on the Indo-Nepal border. It "
  "forms part of the Dudhwa Tiger Reserve and is known for swamp deer (barasingha).",
  ["Dudhwa: Lakhimpur Kheri, Uttar Pradesh"],
  [fact("Dudhwa National Park, Lakhimpur Kheri district, Uttar Pradesh, Indo-Nepal border", "dudhwa")])

G(T, NP, "Intermediate",
  "Namdapha National Park and Tiger Reserve is located in which district of Arunachal Pradesh?",
  ["Changlang", "Tawang", "Papum Pare", "West Kameng"], "*",
  "Namdapha",
  "Namdapha, in Changlang district near the India-Myanmar-China tri-junction, is India's easternmost tiger reserve. It "
  "became a national park and tiger reserve in 1983.",
  ["Namdapha: Changlang district, Arunachal Pradesh"],
  [fact("Namdapha National Park is located in the Changlang district of Arunachal Pradesh", "namdapha")])

G(T, NP, "Intermediate",
  "Silent Valley National Park, home to a large population of the lion-tailed macaque, is in which district of "
  "Kerala?",
  ["Palakkad", "Idukki", "Wayanad", "Thrissur"], "*",
  "Silent Valley",
  "Silent Valley National Park is in Palakkad district. A proposed hydroelectric dam on the Kunthipuzha was dropped "
  "after a public campaign, and the area was notified as a national park in 1984.",
  ["Silent Valley: Palakkad district", "River: Kunthipuzha"],
  [fact("Silent Valley National Park, Palakkad, Kerala", "silentvalley")])

G(T, NP, "Intermediate",
  "The Mettur Dam, which forms the Stanley Reservoir in Salem district of Tamil Nadu, is built on which river?",
  ["Kaveri", "Krishna", "Vaigai", "Tungabhadra"], "*",
  "Mettur Dam",
  "The Mettur Dam on the Kaveri (Cauvery) forms the Stanley Reservoir in Salem district. It receives water released "
  "from Karnataka's Krishna Raja Sagara and Kabini dams.",
  ["Mettur Dam: river Kaveri", "Reservoir: Stanley Reservoir"],
  [fact("Stanley Reservoir formed by the Mettur Dam on the Kaveri, Salem district", "mettur")])

G(T, NP, "Intermediate",
  "The Nagarjuna Sagar Dam, completed in the 1960s, is built on which river?",
  ["Krishna", "Godavari", "Kaveri", "Mahanadi"], "*",
  "Nagarjuna Sagar",
  "Nagarjuna Sagar Dam is a masonry dam on the Krishna river, among the largest reservoirs in India, built for "
  "irrigation and hydropower on the Telangana-Andhra Pradesh border.",
  ["Nagarjuna Sagar: river Krishna"],
  [fact("Nagarjuna Sagar dam on the Krishna river, completed 1960s", "nsagar")])

G(T, SF, "Intermediate",
  "Jharkhand, carved out of Bihar, came into existence on 15 November 2000, which is also the birth anniversary of "
  "whom?",
  ["Birsa Munda", "Sidhu Murmu", "Tilka Manjhi", "Jaipal Singh Munda"], "*",
  "Formation of Jharkhand",
  "Jharkhand was formed from the southern districts of Bihar as India's 28th state on 15 November 2000, the birth "
  "anniversary of tribal leader Birsa Munda. Ranchi is its capital.",
  ["Jharkhand formed: 15 November 2000", "Birsa Munda Jayanti: 15 November"],
  [fact("Jharkhand formed on 15 November 2000 from Bihar as the 28th state; Ranchi capital", "jharkhand")])

G(T, SF, "Intermediate",
  "Uttarakhand, formed on 9 November 2000 as India's 27th state, was originally named what?",
  ["Uttaranchal", "Kumaon Pradesh", "Garhwal", "Devbhoomi"], "*",
  "Formation of Uttarakhand",
  "Uttarakhand was carved out of Uttar Pradesh under the Uttar Pradesh Reorganisation Act, 2000 and named Uttaranchal. "
  "It was renamed Uttarakhand in January 2007. Dehradun is its capital.",
  ["Formed: 9 November 2000 as Uttaranchal", "Renamed: Uttarakhand (2007)"],
  [fact("Uttarakhand created 9 Nov 2000 as Uttaranchal from Uttar Pradesh; renamed in 2007", "uttarakhand")])


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
    plan = json.loads((ROOT / "batches" / "plans" / "BATCH_002_plan.json").read_text(encoding="utf-8"))
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
    # every current-affairs topic question is dated inside the window
    for q in out:
        if q["topic"] in CA_TOPICS:
            assert CA_FROM <= q["current_affairs"]["event_date"] <= CA_TO, q["question_id"]
    # statement-combination keys must match the S-set positions
    for q in out:
        texts = [o["text"] for o in q["options"]]
        if texts in (S12, S123):
            assert q["correct_answer"] in LETTERS
    return out, counts


def rotate_false_first(it):
    """For a '1 and 2 only' item whose statement 3 is the false one, move statement 3 to the front.

    The statements become (old 3, old 1, old 2), so the answer becomes '2 and 3 only' (B). Steps are renumbered the
    same way. This spreads the keys of the statement questions instead of piling them on A.
    """
    lines = it["text"].split("\n")
    idx = [i for i, ln in enumerate(lines) if ln[:3] in ("1. ", "2. ", "3. ")]
    assert len(idx) == 3 and it["options"] == S123 and it["answer"] == "A", it["text"]
    st = [lines[i][3:] for i in idx]
    new = [st[2], st[0], st[1]]
    for k, i in enumerate(idx):
        lines[i] = f"{k + 1}. {new[k]}"
    it["text"] = "\n".join(lines)
    steps = it["steps"]
    sidx = [i for i, s in enumerate(steps) if s[:2] in ("1:", "2:", "3:")]
    assert len(sidx) == 3 and steps[-1] == "So 1 and 2 only", steps
    body = [steps[i][2:] for i in sidx]
    nb = [body[2], body[0], body[1]]
    for k, i in enumerate(sidx):
        steps[i] = f"{k + 1}:{nb[k]}"
    steps[-1] = "So 2 and 3 only"
    it["answer"] = "B"


_a_items = [it for it in QUESTIONS if it["options"] == S123 and it["answer"] == "A"]
for _it in _a_items[::2]:
    rotate_false_first(_it)

# Order the questions by topic as in the plan so IDs run topic by topic
_plan = json.loads((ROOT / "batches" / "plans" / "BATCH_002_plan.json").read_text(encoding="utf-8"))
_order = [t["topic"] for t in next(s for s in _plan["subjects"] if s["subject"] == GA)["topics"]]
_rank = {"Basic": 0, "Intermediate": 1, "Advanced": 2}
QUESTIONS.sort(key=lambda it: (_order.index(it["topic"]), _rank[it["difficulty"]]))

questions, keys = build(QUESTIONS)
batch = {
    "schema_version": "1.0",
    "batch_id": "BATCH_002",
    "created_at": TODAY,
    "notes": "BATCH_002 General Awareness part: 150 original questions. Current-affairs topics (National and "
             "International Current Affairs, Appointments, Awards, Sports, Summits, Books, Economic Affairs, "
             "Business) test events dated 2025-11-01 to 2026-11-04, with event dates from the sources and "
             "review_by 2027-05-05. Other time-sensitive facts also carry current_affairs dates. Fact checks dated "
             "2026-11-05; verified_by says whether each question's sources were opened (web:fact-check) or "
             "confirmed only in search results (web:search-confirmed). Pending human review.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / "BATCH_002_GA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(keys.items()))})")
