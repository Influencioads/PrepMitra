"""Writes batches/parts/BATCH_003_GA.json: the 150 General Awareness questions of BATCH_003.

Current-affairs topics (National and International Current Affairs, Appointments, Awards, Sports, Summits, Economic
Affairs, Business) test events dated between 2025-11-01 and 2026-11-04; event dates come from the sources and every
such question carries current_affairs {event_date, review_by 2027-05-05}. Other time-sensitive facts (themes of days,
index ranks, heads of bodies, policy changes, schemes) carry current_affairs too.

Every question has fact_checks. Each URL is marked OPENED (fetched and read on 2026-11-05, giving "web:fact-check")
or SEARCH (confirmed only from search-result text on 2026-11-05, giving "web:search-confirmed"). nobelprize.org,
weforum.org and pib.gov.in returned HTTP 403 to fetches, so facts from them were confirmed from search results or
from other pages that were opened.

All earlier GA stems (BATCH_000 sample, BATCH_001_GA, BATCH_002_GA) were read first; no fact or event tested there is
tested again here.

Statement questions have their key fixed by the statements; other questions are written with the correct option
first and answer "*", and are then placed so that keys are balanced A to D.

    python tools/batch_003/ga.py
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
BATCH = "BATCH_003"
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
    # Economic affairs
    "gdp_q2_bt": ("https://www.businesstoday.in/latest/economy/story/indias-q2-gdp-surges-82-full-year-growth-to-stay-"
                  "above-7-says-cea-504214-2025-11-28", SEARCH),
    "gdp_q2_tribune": ("https://www.tribuneindia.com/news/business/indian-economy-grows-8-2-in-q2-2025-26", SEARCH),
    "survey_dh": ("https://www.deccanherald.com/amp/story/business%2Funion-budget%2Feconomic-survey-pegs-fy27-gdp-"
                  "growth-at-68-to-72-3878643", SEARCH),
    "survey_ml": ("https://moneylife.in/article/economic-survey-projects-stable-growth-path-pegs-fy26-gdp-growth-at-74-"
                  "percentage-despite-global-uncertainty/79509.html", SEARCH),
    "imf_oct": ("https://www.businesstoday.in/latest/economy/story/imf-raises-indias-growth-forecast-to-7-for-2026-"
                "upgrades-outlook-by-60-bps-561120-2026-10-13", SEARCH),
    "imf_dd": ("https://ddindia.co.in/2026/10/imf-raises-indias-growth-forecast-to-7-for-2026-keeps-it-among-fastest-"
               "growing-major-economies/", SEARCH),
    "imf_jan": ("https://www.thestatesman.com/business/india-to-grow-6-4-in-2026-2027-remain-fastest-growing-major-"
                "economy-imf-1503543098.html", SEARCH),
    "mpc_jun_bs": ("https://www.business-standard.com/finance/news/rbi-holds-repo-rate-at-5-25-keeps-policy-stance-"
                   "neutral-126060500287_1.html", SEARCH),
    "mpc_jun_angel": ("https://www.angelone.in/news/Economy/rbi-mpc-june-2026-5-key-takeaways-as-rbi-keeps-repo-rate-"
                      "unchanged-at-5-25-percent", SEARCH),
    "gst_air": ("https://newsonair.gov.in/gst-collections-hit-all-time-high-of-over-%E2%82%B92-42-lakh-crore-in-april/",
                SEARCH),
    "gst_munim": ("https://themunim.com/gst-collections-april-2026/", SEARCH),
    "cpi_sep_tt": ("https://telanganatoday.com/india-retail-inflation-rises-to-5-54pc-in-september-food-prices-drive-"
                   "increase", SEARCH),
    "cpi_sep_gr": ("https://www.goodreturns.in/news/india-cpi-inflation-september-2026-retail-inflation-rises-to-5-54-"
                   "as-food-prices-surge-onion-infl-1540859.html", SEARCH),
    "mpc_feb_week": ("https://www.theweek.in/news/biz-tech/2026/02/06/mpc-feb-2026-rbi-holds-repo-rate-at-525percent-"
                     "lifts-gdp-outlook-to-74percent-on-robust-demand.html", SEARCH),
    "mpc_feb_fpj": ("https://www.freepressjournal.in/business/rbi-keeps-repo-rate-unchanged-maintains-neutral-policy-"
                    "stance-indicating-balanced-focus-on-growth-inflation-risks", SEARCH),
    "fd_dh": ("https://www.deccanherald.com/business/economy/government-achieves-fiscal-deficit-target-of-44-for-fy26-"
              "4023562", SEARCH),
    "fd_ob": ("https://www.outlookbusiness.com/amp/story/economy-and-policy/govt-achieves-fiscal-deficit-target-of-44-"
              "for-fy26", SEARCH),
    "gdp_fy26_bt": ("https://www.businesstoday.in/latest/economy/story/indias-economy-accelerates-gdp-growth-hits-7-7-"
                    "in-fy26-fastest-pace-in-two-years-535164-2026-06-05", SEARCH),
    "gdp_fy26_ob": ("https://www.outlookbusiness.com/economy-and-policy/indias-gdp-grows-78-in-q4-full-year-growth-at-"
                    "77", SEARCH),
    "cad_fpj": ("https://www.freepressjournal.in/business/indias-current-account-deficit-widens-to-usd-42-billion-in-"
                "q1-fy27-rbi-data", SEARCH),
    "cad_print": ("https://theprint.in/economy/current-account-deficit-widens-to-usd-4-2-bn-in-q1-rbi-data/3030972/",
                  SEARCH),
    # Government policies
    "vbsa_prs": ("https://prsindia.org/billtrack/prs-products/prs-bill-summary-1765905039", OPENED),
    "vbsa_dh": ("https://www.deccanherald.com/amp/story/education%2Fexplained-viksit-bharat-shiksha-adhishthan-bill-"
                "aims-to-create-single-higher-education-regulator-3831996", SEARCH),
    "hsns_air": ("https://www.newsonair.gov.in/parliament-passes-health-security-and-national-security-cess-bill-2025/",
                 SEARCH),
    "hsns_dc": ("https://www.deccanchronicle.com/nation/pan-masala-cess-bill-passed-funds-earmarked-for-national-"
                "security-and-public-health-1921859", SEARCH),
    "cea_tribune": ("https://www.tribuneindia.com/news/business/lok-sabha-passes-bill-to-levy-excise-duty-on-tobacco-"
                    "as-gst-cess-nears-end", SEARCH),
    "cea_statesman": ("https://www.thestatesman.com/business/parliament-oks-bill-to-hike-central-excise-on-tobacco-"
                      "replacing-gst-cess-1503521617.html", SEARCH),
    "ibc_tribune": ("https://www.tribuneindia.com/news/business/parliament-passes-ibc-amendment-bill-to-cut-delays-"
                    "improve-transparency-boost-recovery-ecosystem/", SEARCH),
    "ibc_indialaw": ("https://www.indialaw.in/blog/regulatory/insolvency-and-bankruptcy-code-amendment-act-2026/",
                     SEARCH),
    "jv_etv": ("https://www.etvbharat.com/amp/en/bharat/lok-sabha-passes-jan-vishwas-amendment-bill-enn26040106684",
               SEARCH),
    "jv_statesman": ("https://www.thestatesman.com/india/parliament-clears-jan-vishwas-bill-2026-replacing-criminal-"
                     "penalties-with-civil-fines-1503577040.html", SEARCH),
    "acq_open": ("https://openthemagazine.com/business/banks-get-green-light-for-acquisition-financing-under-revised-"
                 "rbi-capital-market-rules", SEARCH),
    "acq_vision": ("https://visionias.in/current-affairs/upsc-daily-news-summary/article/2025-11-17/business-standard/"
                   "economy/rbis-10-tier-i-cap-on-acquisition-financing-restrictive-say-bankers", SEARCH),
    "acq_caalley": ("https://caalley.com/news-updates/indian-news/rbi-eases-acquisition-finance-rules-allows-higher-"
                    "limits-and-top-up-stake-purchases", SEARCH),
    "mf_taxmann": ("https://www.taxmann.com/post/blog/sebi-notifies-mutual-funds-regulations-2026", SEARCH),
    "mf_elp": ("https://elplaw.in/leadership/sebi-revamps-and-replaces-its-30-year-old-regulations-for-mutual-funds/",
               SEARCH),
    # Schemes
    "epm_mp": ("https://www.millenniumpost.in/business/government-approves-rs-25060-cr-export-promotion-mission-for-"
               "6-yrs-635251", SEARCH),
    "epm_angel": ("https://www.angelone.in/news/market-updates/cabinet-clears-45-060-crore-scheme-for-exporters-and-"
                  "msmes", SEARCH),
    "rdi_etv": ("https://www.etvbharat.com/en/technology/pm-modi-inaugurates-emerging-science-and-technology-"
                "innovation-conclave-2025-enn25110301430", SEARCH),
    "rdi_upstox": ("https://upstox.com/news/business-news/latest-updates/pm-modi-launches-1-lakh-crore-rdi-fund-to-"
                   "boost-private-sector-research-innovation/article-183956", SEARCH),
    "repm_tribune": ("https://www.tribuneindia.com/news/business/cabinet-approves-rs-7280-crore-rare-earth-permanent-"
                     "magnets-scheme-to-enhance-self-reliance-promote-repm-ecosystem", SEARCH),
    "repm_bt": ("https://www.businesstoday.in/latest/corporate/story/centre-clears-rs-7280-cr-push-to-boost-rare-earth-"
                "magnet-production-cut-import-dependence-503845-2025-11-26", SEARCH),
    # Important days
    "math_wiki": ("https://en.wikipedia.org/wiki/National_Mathematics_Day_(India)", SEARCH),
    "math_ibt": ("https://www.ibtimes.co.in/pm-declares-ramanujan039s-birthday-as-national-mathematics-day-272654",
                 SEARCH),
    "kisan_vikas": ("https://vikaspedia.in/agriculture/agri-directory/important-days/national-farmers-day", SEARCH),
    "kisan_fpj": ("https://www.freepressjournal.in/india/kisan-diwas-a-tribute-to-former-prime-minister-chaudhary-"
                  "charan-singh", SEARCH),
    "flag_tribune": ("https://tribuneindia.com/news/armed-forces-flag-day-saluting-our-bravehearts", SEARCH),
    "flag_air": ("https://www.newsonair.gov.in/armed-forces-flag-day-being-observed-today", SEARCH),
    "girl_wiki": ("https://en.wikipedia.org/wiki/National_Girl_Child_Day", SEARCH),
    "girl_cry": ("https://www.cry.org/blog/national-girl-child-day-history-and-purpose/", SEARCH),
    "wed_page": ("https://www.worldenvironmentday.global/2026/about/theme-and-host", OPENED),
    "wed_unep": ("https://www.unep.org/en/events/un-day/world-environment-day-2026", SEARCH),
    "wwd_arizona": ("https://has.arizona.edu/events/world-water-day-2026-water-and-gender-where-water-flows-equality-"
                    "grows", SEARCH),
    "wwd_eu": ("https://climate-pact.europa.eu/articles-and-events/events/climate-action-days-world-water-day-2026-"
               "celebration-and-launch-un-world-water-development-report-2026-03-23_en", SEARCH),
    "whd_who": ("https://www.who.int/southeastasia/navigation/mega-menu/news/world-health-day-2026", SEARCH),
    "whd_devaid": ("https://www.developmentaid.org/news-stream/post/205864/who-world-health-day-2026-stand-with-"
                   "science-global-health-action", SEARCH),
    "idy_air": ("https://newsonair.gov.in/international-yoga-day-2026-being-celebrated-across-the-globe-with-theme-"
                "yoga-for-healthy-ageing/", SEARCH),
    "idy_drishti": ("https://www.drishtiias.com/state-pcs-current-affairs/12th-international-day-of-yoga-2026/"
                    "print_manually", SEARCH),
    # Reports and indexes
    "grr_wef": ("https://www.weforum.org/press/2026/01/global-risks-report-2026-geopolitical-and-economic-risks-rise-"
                "in-new-age-of-competition/", SEARCH),
    "grr_bt": ("https://www.businesstoday.in/wef-2026/story/wef-summit-davos-2026-world-faces-stormy-next-decade-"
               "geoeconomic-confrontation-now-top-risk-warns-wef-510919-2026-01-14", SEARCH),
    "egr_dte": ("https://downtoearth.org.in/climate-change/new-climate-pledges-fail-to-move-the-needle-on-warming-"
                "world-still-on-track-for-25c-unep", SEARCH),
    "egr_pbl": ("https://www.pbl.nl/en/publications/unep-emissions-gap-report-2025", SEARCH),
    "tb_scroll": ("https://scroll.in/latest/1088510/india-recorded-highest-tuberculosis-cases-globally-in-2024-who",
                  SEARCH),
    "tb_wire": ("https://thewire.in/health/india-records-21-drop-in-tb-incidence-who-report", SEARCH),
    "weo_iea": ("https://www.iea.org/events/world-energy-outlook-2025", SEARCH),
    "weo_dte": ("https://www.downtoearth.org.in/energy/world-energy-outlook-2025-iea-warns-of-mounting-security-risks-"
                "in-age-of-electricity", SEARCH),
    "henley_bt": ("https://www.businesstoday.in/nri/visa/story/henley-passport-index-2026-indian-passport-climbs-five-"
                  "places-to-gain-80th-spot-510835-2026-01-14", SEARCH),
    "henley_fpj": ("https://www.freepressjournal.in/india/indian-passport-rises-to-80th-rank-in-henley-passport-index-"
                   "2026-despite-fewer-visa-free-destinations", SEARCH),
    "cpi_ti_de": ("https://www.dailyexcelsior.com/?p=2156056", SEARCH),
    "cpi_ti_nb": ("https://www.newsbytesapp.com/news/india/corruption-perceptions-index-2025-india-ranks-91st-among-"
                  "182-countries/story", SEARCH),
    "wpfi_wire": ("https://thewire.in/media/india-is-157th-out-of-180-countries-on-rsfs-2026-world-press-freedom-index",
                  OPENED),
    "wpfi_fpj": ("https://www.freepressjournal.in/india/press-freedom-index-2026-india-drops-to-157-rsf-cites-rising-"
                 "pressure-on-media", SEARCH),
    "ccpi_wire": ("https://thewire.in/news/india-slips-13-ranks-on-climate-change-performance-index", SEARCH),
    "ccpi_print": ("https://theprint.in/environment/india-slides-13-spots-on-climate-change-performance-index-coal-"
                   "conflicts-major-barriers/2787636", SEARCH),
    "gpi_ot": ("https://www.outlooktraveller.com/News/global-peace-index-2026-the-10-most-peaceful-countries-in-the-"
               "world-right-now", SEARCH),
    "gpi_drishti": ("https://www.drishtiias.com/state-pcs-current-affairs/global-peace-index-2026/print_manually",
                    SEARCH),
    # Organisations
    "imo_wiki": ("https://en.wikipedia.org/wiki/International_Maritime_Organization", SEARCH),
    "imo_hsn": ("https://www.hellenicshippingnews.com/?p=1104061", SEARCH),
    "icao_brit": ("https://www.britannica.com/topic/International-Civil-Aviation-Organization", SEARCH),
    "icao_unsceb": ("https://www.unsceb.org/international-civil-aviation-organization", SEARCH),
    "itu_wiki": ("https://en.wikipedia.org/wiki/International_Telecommunication_Union", SEARCH),
    "itu_hist": ("https://www.itu.int/en/history/documents/itu-history-overview.pdf", SEARCH),
    "au_channels": ("https://www.channelstv.com/2025/02/15/mahmoud-ali-youssouf-elected-to-head-african-union-"
                    "commission", SEARCH),
    "au_gna": ("https://gna.org.gh/2025/02/djiboutis-foreign-minister-elected-as-chairperson-of-african-union-"
               "commission", SEARCH),
    "opec_gulf": ("https://gulfnews.com/business/haitham-al-ghais-takes-office-as-opec-secretary-general-1.89647931",
                  SEARCH),
    "opec_wiki": ("https://en.wikipedia.org/wiki/Haitham_al-Ghais", SEARCH),
    "bulg_bdf": ("https://www.banque-france.fr/en/news/21st-member-euro-area-2026-bulgaria", SEARCH),
    "bulg_eu": ("https://learning-corner.learning.europa.eu/news-and-competitions/bulgaria-joins-euro-new-chapter-"
                "begins-2026-01-01_en", SEARCH),
    "irena_wiki": ("https://en.wikipedia.org/wiki/International_Renewable_Energy_Agency", SEARCH),
    "irena_masdar": ("https://masdar.ae/en/news/newsroom/hh-sheikh-abdullah-bin-zayed-al-nahyan-inaugurates-irena-hq-"
                     "in-masdar-city", SEARCH),
    "wmo_news": ("https://wmo.int/media/news/celeste-saulo-of-argentina-appointed-first-female-secretary-general-of-"
                 "wmo", SEARCH),
    "wto_wam": ("https://www.wam.ae/en/article/b1uxh0h-comoros-timor-leste-formally-join-wto-during-mc13", SEARCH),
    "wto_tatoli": ("https://en.tatoli.tl/2024/02/26/timor-leste-officially-becomes-full-member-of-the-wto/19/", SEARCH),
    "wto_newarab": ("https://newarab.com/news/comoros-becomes-165th-member-wto", SEARCH),
    "unicef_pr": ("https://www.unicef.org/press-releases/catherine-russell-assumes-functions-new-unicef-executive-"
                  "director", SEARCH),
    # Static
    "birr_rb": ("https://www.remitbee.com/world-currency/ethiopian-birr", SEARCH),
    "birr_ww": ("https://wikiwand.com/en/articles/Ethiopian_birr", SEARCH),
    "jod_wiki": ("https://en.wikipedia.org/wiki/Jordanian_dinar", SEARCH),
    # National
    "cji_bt": ("https://www.businesstoday.in/india/story/justice-surya-kant-sworn-in-as-the-53rd-chief-justice-of-"
               "india-503369-2025-11-24", SEARCH),
    "cji_week": ("https://www.theweek.in/news/india/2025/11/24/protect-the-last-citizen-justice-surya-kant-takes-"
                 "charge-as-53rd-chief-justice-of-india.html", SEARCH),
    "kerala_bt": ("https://www.businesstoday.in/india/story/kerala-becomes-first-indian-state-to-eradicate-extreme-"
                  "poverty-says-cm-pinarayi-vijayan-500442-2025-11-01", SEARCH),
    "kerala_etv": ("https://www.etvbharat.com/en/state/kerala-declares-itself-first-state-in-india-free-of-extreme-"
                   "poverty-opposition-protests-enn25110101914", SEARCH),
    "vbs_week": ("https://www.theweek.in/news/biz-tech/2026/01/17/first-ever-vande-bharat-sleeper-flagged-off-from-"
                 "kamakhya-to-howrah.html", SEARCH),
    "vbs_fpj": ("https://www.freepressjournal.in/india/indias-first-vande-bharat-sleeper-train-flagged-off-by-pm-modi-"
                "check-features-fares-route-details", SEARCH),
    "nmia_air": ("https://www.newsonair.gov.in/navi-mumbai-international-airport-starts-commercial-flight-operations",
                 SEARCH),
    "nmia_fpj": ("https://www.freepressjournal.in/amp/mumbai/nmia-takes-off-today-as-navi-mumbai-international-airport-"
                 "begins-commercial-operations-making-mmr-indias-first-dual-airport-system", SEARCH),
    "mahe_statesman": ("https://www.thestatesman.com/india/anti-submarine-warfare-shallow-water-craft-ins-mahe-"
                       "commissioned-into-indian-navy-1503516549.html", SEARCH),
    "mahe_tribune": ("https://www.tribuneindia.com/news/india/indian-navy-commissions-indigenous-anti-submarine-"
                     "warfare-vessel-ins-mahe", SEARCH),
    "ikshak_mp": ("https://www.millenniumpost.in/nation/navy-inducts-survey-vessel-ins-ikshak-in-kochi-634407", SEARCH),
    "ikshak_ra": ("https://raksha-anirveda.com/ins-ikshak-third-of-the-svl-class-ship-commissioned", SEARCH),
    "cms03_tribune": ("https://www.tribuneindia.com/news/india/isro-launches-heaviest-comsat-to-boost-navy-grid",
                      SEARCH),
    "cms03_week": ("https://www.theweek.in/news/sci-tech/2025/11/03/lvm3-m5-mission-how-india-s-bahubali-rocket-"
                   "defied-weight-limits.amp.html", SEARCH),
    "pslv_bt": ("https://www.businesstoday.in/science/story/isros-pslv-c62-mission-fails-second-rare-setback-in-eight-"
                "months-for-workhorse-launcher-510482-2026-01-12", SEARCH),
    "pslv_nsf": ("https://www.nasaspaceflight.com/2026/01/indias-pslv-solve-third-stage-second-failure/", SEARCH),
    "pudu_air": ("https://www.newsonair.gov.in/n-rangasamy-sworn-in-as-puducherry-chief-minister-for-record-fifth-"
                 "term/", SEARCH),
    "pudu_tribune": ("https://www.tribuneindia.com/news/india/rangasamy-takes-oath-as-puducherry-cm-for-5th-time/",
                     SEARCH),
    "army_outlook": ("https://www.outlookindia.com/national/lt-gen-dhiraj-seth-appointed-next-army-chief-to-take-"
                     "charge-on-june-30", SEARCH),
    "army_statesman": ("https://www.thestatesman.com/india/lt-gen-dhiraj-seth-appointed-next-chief-of-army-staff-"
                       "1503605271.html", SEARCH),
    "iaf_morung": ("https://morungexpress.com/air-marshal-ashutosh-dixit-appointed-new-iaf-chief-to-succeed-ap-singh",
                   SEARCH),
    "iaf_psu": ("https://www.psuconnect.in/news/air-chief-marshal-ashutosh-dixit-takes-charge-as-29th-iaf-cas", SEARCH),
    "ramsar_open": ("https://openthemagazine.com/india/explained-why-patna-bird-sanctuary-and-chhari-dhand-are-now-"
                    "ramsar-sites", SEARCH),
    "ramsar_star": ("https://www.thestar.com.my/aseanplus/aseanplus-news/2026/02/02/two-new-wetlands-added-to-ramsar-"
                    "sites-list", SEARCH),
    "rday_bt": ("https://www.businesstoday.in/india/story/77th-republic-day-150-years-of-vande-mataram-operation-"
                "sindoor-tableau-brahmos-roll-out-and-rafales-overhead-512850-2026-01-26", SEARCH),
    "rday_adu": ("https://www.aviation-defence-universe.com/150-years-of-vande-mataram-to-be-the-theme-of-republic-"
                 "day-parade-2026-at-kartavya-path", SEARCH),
    "navy_onm": ("https://www.onmanorama.com/news/kerala/2025/12/03/indian-navy-day-2025-president-droupadi-murmu.html",
                 SEARCH),
    "navy_adu": ("https://www.aviation-defence-universe.com/indian-navys-operational-demonstration-of-maritime-"
                 "strength-marks-navy-day-2025-at-shangumugham-beach-thiruvananthapuram", SEARCH),
    "ms_air": ("https://www.newsonair.gov.in/india-sri-lanka-joint-military-exercise-mitra-shakti-2025-underway-in-"
               "belagavi-karnataka", SEARCH),
    "ms_statesman": ("https://www.thestatesman.com/india/11th-edition-of-indo-sri-lanka-exercise-mitra-shakti-to-be-"
                     "held-in-belagavi-from-november-10-1503509281.html", SEARCH),
    "cic_dh": ("https://www.deccanherald.com/amp/story/india/ex-bureaucrat-raj-kumar-goyal-sworn-in-as-chief-"
               "information-commissioner-3831280", SEARCH),
    "cic_site": ("https://cic.gov.in/cicrg", SEARCH),
    "trishul_wiki": ("https://en.wikipedia.org/wiki/Exercise_Trishul", SEARCH),
    "trishul_strat": ("https://stratpost.com/indian-navy-to-lead-tri-services-exercise-trishul/", SEARCH),
    "vm_tribune": ("https://www.tribuneindia.com/news/india/150-years-of-vande-mataram-pm-modi-releases-stamp-coin",
                   SEARCH),
    "vm_pmindia": ("https://www.pmindia.gov.in/en/news_updates/pm-inaugurates-year-long-commemoration-of-150-years-of-"
                   "the-national-song-vande-mataram/", SEARCH),
    "ladakh_tv": ("https://www.indiatvnews.com/news/india/ladakh-gets-five-new-districts-as-lg-saxena-approves-"
                  "proposal-check-names-2026-04-27-1039080", SEARCH),
    "ladakh_kr": ("https://kashmirreader.com/2026/04/28/creation-of-5-new-districts-in-ladakh-approved/", SEARCH),
    "aw_air": ("https://www.newsonair.gov.in/8th-india-uk-ajeya-warrior-military-exercise-begins-in-bikaner", SEARCH),
    "aw_statesman": ("https://www.thestatesman.com/india/india-uk-joint-military-exercise-ajeya-warrior-25-kicks-off-"
                     "in-rajasthan-1503513471.html", SEARCH),
    "lvm6_bt": ("https://www.businesstoday.in/india/story/isro-successfully-launches-lvm3-m6-rocket-with-bluebird-"
                "block-2-satellite-setting-new-records-507954-2025-12-24", SEARCH),
    "lvm6_arab": ("https://www.arabnews.pk/node/2627347", SEARCH),
    # International
    "mamdani_aj": ("https://www.aljazeera.com/news/2025/11/5/zohran-mamdani-elected-as-new-york-mayor-in-historic-win",
                   SEARCH),
    "mamdani_scmp": ("https://www.scmp.com/news/world/united-states-canada/article/3331564/zohran-mamdani-wins-new-"
                     "york-city-mayors-race-capping-stunning-ascent", SEARCH),
    "chile_kpbs": ("https://www.kpbs.org/news/international/2025/12/14/chile-shifts-sharply-right-as-jose-antonio-kast-"
                   "wins-presidency", SEARCH),
    "chile_star": ("https://www.thestar.com.my/news/world/2025/12/14/chile-votes-in-presidential-race-expected-to-"
                   "lurch-country-to-the-right", SEARCH),
    "hun_euronews": ("https://www.euronews.com/my-europe/2026/05/09/peter-magyar-sworn-in-as-hungarys-new-prime-"
                     "minister-after-landslide-april-election-victor", SEARCH),
    "hun_star": ("https://www.thestar.com.my/news/world/2026/05/10/magyar-sworn-in-as-hungary039s-prime-minister-on-"
                 "promises-of-change", SEARCH),
    "nepal_dawn": ("https://www.dawn.com/news/1986102", SEARCH),
    "nepal_print": ("https://theprint.in/world/ex-rapper-shah-sworn-in-as-nepal-prime-minister-after-sweeping-election-"
                    "win/2890024", SEARCH),
    "port_kpbs": ("https://www.kpbs.org/news/international/2026/02/08/center-left-socialist-candidate-wins-over-"
                  "populist-in-portugals-presidential-runoff", SEARCH),
    "port_star": ("https://www.thestar.com.my/news/world/2026/02/08/portugal-votes-in-presidential-runoff-with-"
                  "socialist-poised-for-victory", SEARCH),
    "japan_star": ("https://www.thestar.com.my/aseanplus/aseanplus-news/2026/02/10/japan-election-results-confirm-"
                   "super-majority-for-takaichi039s-party", SEARCH),
    "japan_nippon": ("https://www.nippon.com/en/japan-data/h02703/", SEARCH),
    "brazil_benin": ("https://beninwebtv.bj/en/brazil-lula-re-elected-against-flavio-bolsonaro-in-runoff/", SEARCH),
    "brazil_bah": ("https://www.newsofbahrain.com/en/article/lula-wins-re-election-in-brazil-as-bolsonaro-rejects-run-"
                   "off-result", SEARCH),
    "peru_merco": ("https://en.mercopress.com/2026/06/30/keiko-fujimori-wins-peru-s-presidency-as-the-full-count-"
                   "confirms-her-by-49-641-votes/comments", SEARCH),
    "peru_ap": ("https://www.record-eagle.com/ap/international/conservative-candidate-keiko-fujimori-wins-peru-s-"
                "presidential-election-in-a-runoff/article_d072c07f-e10d-5855-832b-4d496409449c.html", SEARCH),
    "col_dawn": ("https://www.dawn.com/news/2010187", SEARCH),
    "col_local10": ("https://www.local10.com/news/politics/2026/06/22/colombias-preliminary-vote-count-showing-de-la-"
                    "espriellas-narrow-victory-is-accurate-registrar-says/", SEARCH),
    "aus_dawn": ("https://www.dawn.com/news/1960333", SEARCH),
    "aus_air": ("https://www.newsonair.gov.in/australia-becomes-worlds-first-country-to-ban-social-media-for-teenagers-"
                "under-the-age-of-16", SEARCH),
    "mya_star": ("https://www.thestar.com.my/aseanplus/aseanplus-news/2026/04/05/039i039m-the-boss-now039-myanmars-"
                 "parliament-elects-the-ruling-general-as-president-keeping-the-army-firmly-in-charge", SEARCH),
    "mya_arab": ("https://www.arabnews.pk/node/2638631", SEARCH),
    "cr_havana": ("https://havanatimes.org/news/laura-fernandez-wins-costa-rica-presidential-election/", SEARCH),
    "cr_wgcu": ("https://www.wgcu.org/2026-02-02/populist-conservative-laura-fernandez-wins-costa-ricas-presidential-"
                "election", SEARCH),
    "thai_prd": ("https://thailand.prd.go.th/en/content/category/detail/id/48/iid/486890", SEARCH),
    "thai_dawn": ("https://www.dawn.com/news/1983932", SEARCH),
    "hond_ksl": ("https://www.ksl.com/article/51423482/trump-backed-asfura-wins-honduras-presidency-after-disputed-"
                 "election", SEARCH),
    "hond_bah": ("https://buenosairesherald.com/world/latin-america/nasry-asfura-declared-victor-of-honduran-"
                 "presidential-election", SEARCH),
    "ven_aj": ("https://www.aljazeera.com/news/2026/1/5/delcy-rodriguez-sworn-in-as-venezuelas-president-after-maduro-"
               "abduction", SEARCH),
    "ven_nat": ("https://www.thenationalnews.com/news/2026/01/04/maduro-capture-venezuela-delcy-rodriguez/", SEARCH),
    "sb_hci": ("https://www.hcicolombo.gov.in/section/press-releases/1operation-sagar-bandhu-india-extends-immediate-"
               "humanitarian-relief-to-sri-lanka-amid-cyclone-ditwah/", SEARCH),
    "sb_air": ("https://www.newsonair.gov.in/india-launches-operation-sagar-bandhu-to-support-sri-lanka-after-cyclone-"
               "ditwah", SEARCH),
    "sb_gk": ("https://m.greaterkashmir.com/article/india-continues-providing-emergency-hadr-support-to-sri-lanka/"
              "458515", SEARCH),
    "ustrade_bt": ("https://www.businesstoday.in/latest/economy/story/inside-the-india-us-interim-trade-agreement-"
                   "reciprocal-tariffs-on-india-to-come-down-to-18-0-duty-on-generic-pharma-515053-2026-02-07", SEARCH),
    "ustrade_gov": ("https://www.govinfo.gov/content/pkg/DCPD-202600084/pdf/DCPD-202600084.pdf", SEARCH),
    "knesset_quint": ("https://www.thequint.com/news/breaking-news/modi-addresses-israeli-parliament-backs-gaza-peace",
                      SEARCH),
    "knesset_fpj": ("https://www.freepressjournal.in/india/pm-modi-receives-speaker-of-the-knesset-first-indian-pm-to-"
                    "be-conferred-with-highest-honour-of-israel-parliament-video", SEARCH),
    "bop_aj": ("https://www.aljazeera.com/news/2026/1/22/trump-launches-board-of-peace-at-ceremony-in-davos", SEARCH),
    "bop_na": ("https://newsarenaindia.com/nation/india-absent-at-signing-of-trump-s-board-of-peace-in-davos/68117",
               SEARCH),
    "jordan_nm": ("https://www.narendramodi.in/prime-minister-meets-with-his-majesty-king-abdullah-ii-of-jordan",
                  SEARCH),
    "jordan_fpj": ("https://www.freepressjournal.in/world/royal-engagements-to-renewable-energy-pacts-10-key-highlights-"
                   "from-pm-modis-jordan-visit", SEARCH),
    "deep_air": ("https://www.newsonair.gov.in/unesco-adds-deepavali-to-intangible-cultural-heritage-list", SEARCH),
    "deep_sb18": ("https://www.storyboard18.com/digital/deepavali-enters-unescos-intangible-cultural-heritage-list-"
                  "becomes-indias-16th-global-cultural-inscription-85646.htm", SEARCH),
    "hg_aj": ("https://www.aljazeera.com/amp/news/2025/11/25/ethiopian-volcano-erupts-after-12000-years-what-we-know",
              SEARCH),
    "hg_tribune": ("https://www.tribuneindia.com/news/world/ash-cloud-from-ethiopias-hayli-gubbi-volcano-disrupts-"
                   "major-international-flights-from-delhi", SEARCH),
    # Appointments
    "warsh_cbs": ("https://www.cbsnews.com/news/kevin-warsh-sworn-in-federal-reserve-chair/", SEARCH),
    "wipo_pr": ("https://www.wipo.int/pressroom/en/articles/2026/article_0007.html", OPENED),
    "ecb_pr": ("https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260225~44db0697e5.en.html", OPENED),
    "ecb_mondo": ("https://mondovisione.com/news/european-council-appoints-boris-vuji-as-vice-president-of-the-"
                  "european-central-2026320", SEARCH),
    "undp_un": ("https://press.un.org/en/2025/ga12730.doc.htm", SEARCH),
    "undp_star": ("https://www.the-star.co.ke/news/world/2025-11-19-ex-belgian-pm-appointed-as-new-undp-administrator",
                  SEARCH),
    "interpol_print": ("https://theprint.in/world/interpol-elects-frances-lucas-philippe-as-new-president/2793264",
                       SEARCH),
    "interpol_mwn": ("https://www.moroccoworldnews.com/2025/11/269806/interpols-93rd-general-assembly-closes-in-"
                     "marrakech-with-major-security-resolutions/", SEARCH),
    "yes_bt": ("https://www.businesstoday.in/amp/markets/stocks/story/yes-bank-shares-rbi-approved-appointment-of-new-"
               "md-ceo-stock-reacts-514507-2026-02-04", SEARCH),
    "yes_ob": ("https://www.outlookbusiness.com/corporate/rbi-approves-appointment-of-former-sbi-md-vinay-tonse-as-"
               "yes-bank-md-ceo", SEARCH),
    "icici_bt": ("https://www.businesstoday.in/latest/corporate/story/rbi-clears-sandeep-bakhshis-reappointment-as-"
                 "icici-bank-ceo-till-2028-532974-2026-05-23", SEARCH),
    "lic_pm": ("https://www.peoplematters.in/amp/news/appointments/centre-names-lic-investment-chief-ramakrishnan-"
               "chander-as-md-47510", SEARCH),
    "lic_reinasia": ("https://reinasia.com/lic-appoints-ramakrishnan-chander-as-managing-director/", SEARCH),
    "pant_psu": ("https://www.psuconnect.in/new-faces-in-psus/lic-md-dinesh-pant-appointed-whole-time-member-actuary-"
                 "at-irdai", SEARCH),
    "dfs_wi": ("https://news.webindia123.com/news/Articles/Business/20260601/4457184.html", SEARCH),
    "dfs_im": ("https://indianmasterminds.com/news/ias-sanjay-lohiya-secretary-department-of-financial-services-"
               "profile-207693/", SEARCH),
    "gunveer_an": ("https://newsable.asianetnews.com/amp/business/rbi-appoints-gunveer-singh-as-new-executive-"
                   "director-for-payment-systems-articleshow-o22y3a4", SEARCH),
    "gunveer_lm": ("https://www.lokmattimes.com/business/rbi-promotes-gunveer-singh-as-executive-director/amp/", SEARCH),
    "ray_ll": ("https://www.livelawbiz.com/banking-nbfc/reserve-bank-of-india-elevates-suman-roy-executive-director-"
               "548137", SEARCH),
    "ray_nk": ("https://www.newkerala.com/news/a/rbi-appoints-suman-ray-as-new-executive-director-690.htm", SEARCH),
    "kotak_bt": ("https://www.businesstoday.in/markets/stocks/story/kotak-mahindra-bank-shares-in-focus-on-rbi-nod-for-"
                 "anup-kumar-saha-as-md-ceo-558933-2026-10-01", SEARCH),
    "kotak_ml": ("https://www.moneylife.in/article/kotak-mahindra-bank-rbi-approves-anup-kumar-sahas-3year-term-as-"
                 "mdceo/81813.html", SEARCH),
    # Awards
    "phys_print": ("https://theprint.in/world/francis-halzen-wins-2026-nobel-prize-in-physics/3063266/", OPENED),
    "phys_dm": ("https://dailymaverick.co.za/article/2026-10-06-francis-halzen-wins-2026-nobel-prize-in-physics",
                SEARCH),
    "chem_kt": ("https://www.khaleejtimes.com/world/henri-kagan-kenso-soai-win-2026-nobel-chemistry-prize", OPENED),
    "med_gpb": ("https://www.gpb.org/news/2026/10/05/nobel-medicine-prize-goes-3-scientists-for-research-brain-"
                "activity", SEARCH),
    "med_nobel": ("https://www.nobelprize.org/prizes/medicine/2026/", SEARCH),
    "oscar_abc": ("https://abc13.com/post/oscars-2026-battle-another-wins-best-picture-98th-academy-awards/18719481/",
                  SEARCH),
    "oscar_mb": ("https://mb.com.ph/2026/03/16/one-battle-after-another-wins-best-picture-at-98th-academy-awards",
                 SEARCH),
    "jnan_omm": ("https://ommcomnews.com/india-news/tamil-poet-lyricist-vairamuthu-named-2025-jnanpith-award-winner/",
                 SEARCH),
    "jnan_drishti": ("https://www.drishtiias.com/daily-updates/daily-news-analysis/r-vairamuthu-conferred-60th-"
                     "jnanpith-award/print_manually", SEARCH),
    "sa_statesman": ("https://www.thestatesman.com/india/veteran-diplomat-navtej-sarna-wins-sahitya-akademi-award-"
                     "1503571321.html", SEARCH),
    "sa_print": ("https://theprint.in/india/sahitya-akademi-awards-24-writers-honoured-including-mamta-kalia-ex-"
                 "diplomat-navtej-sarna/2880559", SEARCH),
    "time_euronews": ("https://www.euronews.com/2025/12/11/time-person-of-the-year-2025-announced-the-architects-of-ai",
                      SEARCH),
    "time_cbs": ("https://www.cbsnews.com/news/the-architects-of-ai-are-times-2025-person-of-the-year", SEARCH),
    "kr_nb": ("https://www.newsbytesapp.com/news/sports/no-khel-ratna-for-2025-arjuna-awards-announced/story", SEARCH),
    "kr_open": ("https://openthemagazine.com/sports/no-cricketers-but-plenty-of-champions-whos-on-indias-national-"
                "sports-awards-2025-list", SEARCH),
    "abel_lms": ("https://www.lms.ac.uk/news/gerd-faltings-abel-prize-2026", SEARCH),
    "abel_ems": ("https://euromathsoc.org/news/gerd-faltings-awarded-the-2026-abel-prize-206", SEARCH),
    "pritz_euronews": ("https://www.euronews.com/culture/2026/03/12/chilean-smiljan-radic-clarke-wins-2026-pritzker-"
                       "architecture-prize", SEARCH),
    "pritz_wallpaper": ("https://www.wallpaper.com/architecture/smiljan-radic-clarke-2026-pritzker-architecture-prize",
                        SEARCH),
    "eth_print": ("https://theprint.in/world/pm-modi-conferred-with-ethiopias-highest-honour-during-addis-ababa-visit-"
                  "first-world-leader-to-receive-it/2807188", SEARCH),
    "eth_air": ("https://www.newsonair.gov.in/prime-minister-modi-conferred-ethiopias-highest-award-the-great-honour-"
                "nishan-of-ethiopia/", SEARCH),
    "padma_gulf": ("https://gulfnews.com/world/asia/india/padma-awards-2026-dharmendra-vs-achuthanandan-get-padma-"
                   "vibhushan-posthumously-1.500420249", SEARCH),
    "padma_dh": ("https://www.deccanherald.com/amp/story/india%2Ffrom-dharmendra-mammootty-to-kt-thomas-heres-full-"
                 "list-of-2026-padma-award-winners-3874244", SEARCH),
    "mag_mb": ("https://mb.com.ph/2026/08/31/3-transformative-leaders-named-2026-ramon-magsaysay-awardees", SEARCH),
    "mag_gma": ("https://www.gmanetwork.com/news/lifestyle/content/1000519/the-2026-ramon-magsaysay-award-reveals-"
                "recipients-from-singapore-bangladesh-myanmar/story/", SEARCH),
    "grammy_arab": ("https://www.arabnews.com/node/2631456/lifestyle", SEARCH),
    "grammy_ol": ("https://www.outlookindia.com/art-entertainment/hollywood/grammy-awards-2026-full-list-of-winners",
                  SEARCH),
    "wfp_drishti": ("https://www.drishtiias.com/state-pcs-current-affairs/world-food-prize-2026/print_manually", SEARCH),
    "wfp_site": ("https://www.worldfoodprize.org/en/newsroom/archived_news_coverage/laureate_announcement_ceremony_"
                 "news_coverage/2026_laureate_announcement_ceremony/", SEARCH),
    # Sports
    "ao_espn": ("https://africa.espn.com/tennis/story/_/id/39343618/australian-open-winners-mens-womens-singles-"
                "champions", SEARCH),
    "ao_wiki": ("https://en.wikipedia.org/wiki/2026_Australian_Open", SEARCH),
    "wim_drishti": ("https://www.drishtiias.com/state-pcs-current-affairs/jannik-sinner-wins-wimbledon-2026-mens-"
                    "singles-title/print_manually", SEARCH),
    "wim_ahram": ("https://english.ahram.org.eg/News/572741.aspx", SEARCH),
    "wo_outlook": ("https://www.outlookindia.com/sports/others/winter-olympics-2026-milano-cortina-final-medal-tally-"
                   "check-full-standings", SEARCH),
    "wo_fj": ("https://www.francsjeux.com/en/short/Milan-Cortina-2026-Norway-USA-Netherlands%3A-The-final-medal-table-"
              "of-the-Winter-Olympic-Games/", SEARCH),
    "cwg_fpj": ("https://www.freepressjournal.in/sports/commonwealth-games-2026-medal-tally-india-jump-to-4th-after-"
                "boxing-run-total-rises-to-39-in-glasgow", SEARCH),
    "cwg_brut": ("https://www.brut.media/in/articles/commonwealth-games-2026-india-wins-39-medals-finishes-fourth",
                 SEARCH),
    "cand_chess": ("https://www.chess.com/news/view/sindarov-vaishali-win-7-fide-candidates-2026-conclusions", SEARCH),
    "cand_cb": ("https://en.chessbase.com/post/candidates-tournament-2026-closing-ceremony", SEARCH),
    # Summits
    "cop31_ccn": ("https://www.climatechangenews.com/2025/11/20/cop31-un-climate-summit-turkiye-australia-antalya/"
                  "?utm_id=158", SEARCH),
    "cop31_wong": ("https://www.foreignminister.gov.au/minister/penny-wong/media-release/cop-be-hosted-turkiye-"
                   "australia-leading-negotiations", SEARCH),
    "mc14_wef": ("https://www.weforum.org/stories/2026/04/mc14-yaounde-wto-trade/", SEARCH),
    "mc14_dte": ("https://www.downtoearth.org.in/economy/wto-mc14-key-conference-outcomes-us-stance-drives-deadlock",
                 SEARCH),
    "wef_pr": ("https://www.weforum.org/press/2026/01/annual-meeting-2026-a-spirit-of-dialogue-ceb3ae9c08/", SEARCH),
    "wef_bt": ("https://www.businesstoday.in/amp/wef-2026/story/davos-2026-3000-leaders-from-130-countries-to-attend-"
               "wefs-56th-annual-meeting-from-jan-19-23-510803-2026-01-14", SEARCH),
    "imfwb_imf": ("https://www.imf.org/en/meetings/2026/annual", SEARCH),
    "imfwb_pm": ("https://www.pattayamail.com/thailandnews/15000-delegates-expected-as-thailand-hosts-imf-world-bank-"
                 "annual-meetings-2026-556975", SEARCH),
    "asean_ptv": ("https://ptvnews.ph/all-systems-go-for-48th-asean-summit-in-cebu-pco-noc/", SEARCH),
    "asean_star": ("https://www.thestar.com.my/aseanplus/aseanplus-news/2026/05/07/asean-eyes-first-charter-amendment-"
                   "at-cebu-summit", SEARCH),
    "doha_un": ("https://www.un.org/sustainabledevelopment/blog/2025/11/world-social-summit-adopt-doha-declaration",
                OPENED),
    "doha_unnews": ("https://news.un.org/en/story/2025/11/1166275", SEARCH),
    "raisina_tribune": ("https://www.tribuneindia.com/news/world/pm-modi-to-inaugurate-raisina-dialogue-2026-today-"
                        "finnish-president-alexander-stubb-to-be-chief-guest/", SEARCH),
    "raisina_air": ("https://www.newsonair.gov.in/pm-narendra-modi-to-inaugurate-raisina-dialogue-2026-in-new-delhi-"
                    "today", SEARCH),
    "nato_nato": ("https://www.nato.int/en/news-and-events/events/2026/07/overview---2026-nato-summit-in-ankara-",
                  SEARCH),
    "nato_sabah": ("https://www.dailysabah.com/world/nato-reaffirms-ironclad-joint-defense-in-ankara-declaration/news",
                   SEARCH),
    "quad_star": ("https://www.thestar.com.my/aseanplus/aseanplus-news/2026/05/28/quad-foreign-ministers-fight-for-"
                  "relevance-in-new-delhi-as-leaders-summit-remains-elusive", SEARCH),
    "quad_print": ("https://theprint.in/diplomacy/annual-quad-summits-unlikely-going-forward-india-to-pass-on-baton-to-"
                   "australia-amid-scheduling-issues/2941060/", SEARCH),
    # Business
    "kc_cbs": ("https://www.cbsnews.com/amp/news/kenvue-kimberly-clark-acquisition-tylenol", SEARCH),
    "kc_fw": ("https://www.financierworldwide.com/fw-news/2025/11/6/kimberly-clark-to-acquire-kenvue-in-487bn-deal",
              SEARCH),
    "wbd_abc": ("https://abc13.com/post/warner-bros-agrees-110-billion-deal-paramount-reports-say/18658334/", SEARCH),
    "wbd_rte": ("https://www.rte.ie/news/business/2026/0228/1560892-paramount-warner-bros", SEARCH),
    "amzn_week": ("https://www.theweek.in/news/biz-tech/2025/12/10/after-microsoft-amazon-to-invest-35-billion-for-ai-"
                  "and-export-growth-in-india.amp.html", SEARCH),
    "amzn_ds": ("https://www.dealstreetasia.com/stories/amazon-unveils-35b-investment-in-india-466153", SEARCH),
    "msft_star": ("https://www.thestar.com.my/business/business-news/2025/12/12/amazon-microsoft-pledge-us52bil-"
                  "funding", SEARCH),
    "msft_af": ("https://www.asiafinancial.com/amazon-microsoft-set-to-spend-over-50-billion-on-ai-in-india", SEARCH),
    "jal_bt": ("https://www.businesstoday.in/markets/stocks/story/adani-enterprises-says-nclt-approves-resolution-plan-"
               "for-jaiprakash-associates-520989-2026-03-17", SEARCH),
    "jal_mp": ("https://www.millenniumpost.in/business/nclt-approves-adani-group-rs-14535-crore-bid-to-acquire-"
               "bankrupt-jaiprakash-associates-652213", SEARCH),
    "groww_bt": ("https://www.businesstoday.in/markets/stocks/story/groww-shares-delivers-positive-surprise-on-d-st-"
                 "debut-stock-lists-at-14-premium-501802-2025-11-12", SEARCH),
    "groww_ys": ("https://yourstory.com/2025/12/a-busy-november-ends-with-gains-for-groww-pine-labs-and-lenskart-"
                 "losses-for-physicswallah", SEARCH),
    "magnum_star": ("https://www.thestar.com.my/business/business-news/2025/12/08/unilever-completes-ice-cream-demerger-"
                    "with-magnum-set-to-list", SEARCH),
    "magnum_rte": ("https://www.rte.ie/news/business/2025/1208/1547814-unilever-completes-demerger-with-magnum-set-to-"
                   "list", SEARCH),
    "tmcv_bt": ("https://www.businesstoday.in/markets/stocks/story/tata-motors-shares-commercial-vehicle-arm-makes-a-"
                "solid-stock-market-debut-check-details-501804-2025-11-12", SEARCH),
    "tmcv_bs": ("https://www.business-standard.com/amp/markets/news/tata-motors-cv-shares-make-strong-debut-close-at-"
                "330-on-listing-day-125111201123_1.html", SEARCH),
    "mufg_bs": ("https://www.business-standard.com/companies/news/shriram-finance-mufg-invest-39618-crore-20-percent-"
                "stake-preferential-issue-125121900473_1.html", SEARCH),
    "mufg_ml": ("https://moneylife.in/article/mufg-bank-buys-20-percentage-stake-in-shriram-finance-for-rs39618-crore-"
                "marking-biggest-fdi-in-indian-nbfc-sector/79171.html", SEARCH),
    "idbi_tt": ("https://telanganatoday.com/ccea-approves-60-72pc-stake-sale-in-idbi-bank-for-rs-52878-crore", OPENED),
    "idbi_ol": ("https://www.outlookindia.com/business/idbi-bank-gets-new-owner-as-fairfax-wins-6072-stake-sale",
                SEARCH),
    "fed_week": ("https://www.theweek.in/news/biz-tech/2025/10/25/blackstone-invests-in-federal-bank-as-merger-"
                 "acqusition-boom-in-india-s-financial-services-sector-continues.html", SEARCH),
    "fed_livelaw": ("https://www.livelaw.in/news-updates/cci-approves-blackstone-backed-entitys-warrant-acquisition-in-"
                    "federal-bank-514339", SEARCH),
    "fed_bt": ("https://www.businesstoday.in/markets/story/blackstone-stake-federal-bank-rbi-banking-foreign-investment-"
               "private-banking-india-fdi-514875-2026-02-05", SEARCH),
    "ihc_pr": ("https://ihcuae.com/media-centre/press-releases/ihc-advances-usd-1-billion-investment-to-acquire-"
               "majority-stake-in-indias-sammaan-capital", SEARCH),
    "icicipru_chit": ("https://www.chittorgarh.com/compare/icici-prudential-amc-ipo-vs-meesho-ipo/83/", SEARCH),
    "icicipru_hdfc": ("https://hdfcsky.com/news/icici-prudential-amc-set-for-listing-tomorrow-on-december-19", SEARCH),
    "kw_impact": ("https://www.impactonnet.com/more-from-impact/kwality-walls-india-lists-on-bse-nse-after-hul-ice-"
                  "cream-demerger-13433.html", SEARCH),
    "kw_ob": ("https://www.outlookbusiness.com/corporate/magnum-ice-cream-kwality-walls-india-stake-promoter", SEARCH),
}


def fact(claim, key):
    url, how = U[key]
    return {"claim": claim, "source_url": url, "checked_on": TODAY, "_how": how}


# ====================================================================== National Current Affairs (4 / 13 / 4)
T = "National Current Affairs"
GOV, ST, DEF = "Government decisions", "States and UTs", "Defence"

G(T, GOV, "Basic",
  "Who was sworn in as the 53rd Chief Justice of India on 24 November 2025?",
  ["Justice Surya Kant", "Justice B. R. Gavai", "Justice Sanjiv Khanna", "Justice Vikram Nath"], "*",
  "Chief Justice of India, November 2025",
  "President Droupadi Murmu administered the oath to Justice Surya Kant as the 53rd CJI at Rashtrapati Bhavan on "
  "24 November 2025. He succeeded Justice B. R. Gavai, who demitted office on 23 November, and is the first CJI from "
  "Haryana. He is due to retire on 9 February 2027.",
  ["53rd CJI: Justice Surya Kant (24 Nov 2025)", "Predecessor (52nd): Justice B. R. Gavai"],
  [fact("Justice Surya Kant sworn in as 53rd CJI on 24 Nov 2025, succeeding Justice B. R. Gavai", "cji_bt"),
   fact("Surya Kant took charge as 53rd Chief Justice of India on 24 Nov 2025", "cji_week")],
  why="Justice Gavai was the 52nd CJI whom he succeeded; Justice Khanna was an earlier CJI; Justice Vikram Nath was "
      "not sworn in on that date.",
  current=ca("2025-11-24"))

G(T, ST, "Basic",
  "On 1 November 2025, which state's government declared it the first state in India free of extreme poverty?",
  ["Kerala", "Tamil Nadu", "Goa", "Sikkim"], "*",
  "Extreme-poverty-free declaration",
  "Chief Minister Pinarayi Vijayan declared Kerala free of extreme poverty in a special Assembly session on "
  "1 November 2025, the state's formation day, after a four-year drive led by local bodies. The opposition called the "
  "claim a fraud and boycotted the session.",
  ["Date: 1 November 2025 (Kerala Piravi)", "Declared by: CM Pinarayi Vijayan", "State: Kerala"],
  [fact("Kerala declared first Indian state to eradicate extreme poverty on 1 Nov 2025", "kerala_bt"),
   fact("Kerala declares itself first state free of extreme poverty; opposition protests", "kerala_etv")],
  why="None of the other states made such a declaration on that date.",
  current=ca("2025-11-01"))

G(T, GOV, "Basic",
  "India's first Vande Bharat Sleeper train, flagged off by the Prime Minister on 17 January 2026, runs between "
  "Howrah and which station?",
  ["Kamakhya (Guwahati)", "New Delhi", "Patna", "Bhubaneswar"], "*",
  "First Vande Bharat Sleeper",
  "The Prime Minister flagged off India's first Vande Bharat Sleeper on 17 January 2026 on the Howrah-Kamakhya "
  "(Guwahati) route. The 16-coach train has about 823 berths (11 Third AC, 4 Second AC and 1 First AC coach).",
  ["Route: Howrah (Kolkata) - Kamakhya (Guwahati)", "Flag-off: 17 January 2026"],
  [fact("First Vande Bharat Sleeper flagged off on 17 Jan 2026 between Kamakhya and Howrah", "vbs_week"),
   fact("First Vande Bharat Sleeper: 16 coaches, about 823 berths, Howrah-Guwahati route", "vbs_fpj")],
  why="New Delhi, Patna and Bhubaneswar are not on the first sleeper route.",
  current=ca("2026-01-17"))

G(T, ST, "Basic",
  "Navi Mumbai International Airport began commercial flight operations on 25 December 2025. It is co-developed by "
  "Adani Airports Holdings and which agency?",
  ["CIDCO", "MMRDA", "Airports Authority of India", "MIDC"], "*",
  "Navi Mumbai International Airport",
  "The airport at Ulwe in Raigad district was inaugurated by the Prime Minister on 8 October 2025 and started "
  "commercial operations on 25 December 2025, when IndiGo flight 6E460 from Bengaluru landed first. It is co-developed "
  "by Adani Airports Holdings and the City and Industrial Development Corporation of Maharashtra (CIDCO), giving the "
  "Mumbai region a second airport.",
  ["Commercial operations: 25 Dec 2025", "Developers: Adani Airports Holdings + CIDCO"],
  [fact("Navi Mumbai International Airport started commercial flight operations on 25 Dec 2025", "nmia_air"),
   fact("NMIA co-developed by Adani Airports Holdings and CIDCO; MMR becomes a dual-airport system", "nmia_fpj")],
  why="MMRDA and MIDC are other Maharashtra bodies; AAI is not the co-developer of NMIA.",
  current=ca("2025-12-25"))

G(T, DEF, "Intermediate",
  "INS Mahe, the first of the Indian Navy's indigenous Mahe-class Anti-Submarine Warfare Shallow Water Craft, was "
  "commissioned on 24 November 2025 at which place?",
  ["Naval Dockyard, Mumbai", "Naval Base, Kochi", "Visakhapatnam", "Naval Base, Karwar"], "*",
  "INS Mahe",
  "INS Mahe, lead ship of eight ASW Shallow Water Craft built by Cochin Shipyard, was commissioned at the Naval "
  "Dockyard in Mumbai on 24 November 2025 in the presence of Army Chief General Upendra Dwivedi. It joins the Western "
  "Naval Command and has over 80% indigenous content.",
  ["Commissioned: 24 Nov 2025", "Place: Naval Dockyard, Mumbai", "Role: anti-submarine work in shallow waters"],
  [fact("INS Mahe commissioned at Naval Dockyard Mumbai on 24 Nov 2025; first Mahe-class ASW-SWC", "mahe_statesman"),
   fact("Navy commissions indigenous anti-submarine warfare vessel INS Mahe", "mahe_tribune")],
  why="Kochi is where it was built (Cochin Shipyard), not where it was commissioned; Visakhapatnam and Karwar are "
      "other naval bases.",
  current=ca("2025-11-24"))

G(T, DEF, "Intermediate",
  "INS Ikshak, commissioned at Kochi on 6 November 2025, belongs to which class of ships?",
  ["Survey Vessel (Large)", "Anti-Submarine Warfare Shallow Water Craft", "Project 17A stealth frigate",
   "Diving Support Vessel"], "*",
  "INS Ikshak",
  "INS Ikshak, built by Garden Reach Shipbuilders & Engineers, Kolkata, is the third of four Survey Vessel (Large) "
  "ships after INS Sandhayak and INS Nirdeshak. It does coastal and deep-water hydrographic survey, is the first survey "
  "vessel with accommodation for women, and is based with the Southern Naval Command.",
  ["Commissioned: 6 Nov 2025, Kochi", "Class: Survey Vessel (Large), third of four", "Builder: GRSE"],
  [fact("INS Ikshak commissioned at Kochi on 6 Nov 2025", "ikshak_mp"),
   fact("INS Ikshak is the third of the Survey Vessel (Large) class", "ikshak_ra")],
  why="ASW Shallow Water Craft are the Mahe/Arnala types; Project 17A are frigates; Ikshak is a survey ship.",
  current=ca("2025-11-06"))

G(T, DEF, "Intermediate",
  "CMS-03 (GSAT-7R), launched by LVM3-M5 from Sriharikota on 2 November 2025, is a communication satellite meant "
  "mainly for which user?",
  ["Indian Navy", "Indian Army", "BSNL", "Indian Railways"], "*",
  "CMS-03 (GSAT-7R)",
  "LVM3-M5 placed CMS-03, a military communication satellite for the Indian Navy weighing about 4,400 kg, in "
  "geosynchronous transfer orbit on 2 November 2025. It was described as the heaviest satellite carried by an Indian "
  "rocket to that orbit; the vehicle's capacity was enhanced for it.",
  ["Launch: 2 Nov 2025, LVM3-M5", "Satellite: CMS-03 / GSAT-7R, about 4,400 kg", "User: Indian Navy"],
  [fact("ISRO launched its heaviest communication satellite CMS-03 to boost the Navy's network", "cms03_tribune"),
   fact("LVM3-M5 carried the ~4,400 kg CMS-03 to GTO on 2 Nov 2025", "cms03_week")],
  why="CMS-03 / GSAT-7R serves the Navy, not the Army, BSNL or the Railways.",
  current=ca("2025-11-02"))

G(T, GOV, "Intermediate",
  "PSLV-C62, which failed on 12 January 2026 after an anomaly near the end of its third stage, was carrying which "
  "primary satellite?",
  ["EOS-N1 (Anvesha)", "CMS-03", "BlueBird Block-2", "EOS-08"], "*",
  "PSLV-C62 failure",
  "PSLV-C62 lifted off on 12 January 2026 with DRDO's hyperspectral earth-observation satellite EOS-N1 (Anvesha) and "
  "15 smaller payloads. Roll disturbances near the end of the third stage led to a deviation in the flight path and the "
  "payloads were lost. It was the second PSLV third-stage failure in eight months, after PSLV-C61 in May 2025.",
  ["Mission: PSLV-C62, 12 Jan 2026", "Primary payload: EOS-N1 (Anvesha)", "Cause: third-stage anomaly"],
  [fact("PSLV-C62 mission fails on 12 Jan 2026; second rare setback in eight months", "pslv_bt"),
   fact("PSLV-C62 third-stage failure lost EOS-N1 and co-passengers", "pslv_nsf")],
  why="CMS-03 and BlueBird Block-2 flew on LVM3 rockets; EOS-08 was not the PSLV-C62 payload.",
  current=ca("2026-01-12"))

G(T, ST, "Intermediate",
  "N. Rangasamy took oath as Chief Minister of Puducherry for a fifth time on 13 May 2026. Which party does he lead?",
  ["All India N.R. Congress", "Dravida Munnetra Kazhagam", "Bharatiya Janata Party", "Indian National Congress"], "*",
  "Puducherry government, May 2026",
  "Lieutenant Governor K. Kailashnathan administered the oath to N. Rangasamy, founder of the All India N.R. Congress "
  "(AINRC), at Lok Nivas on 13 May 2026, as the NDA retained power in the Union Territory. BJP leader "
  "A. Namassivayam took oath with him.",
  ["CM: N. Rangasamy (AINRC), fifth term", "Oath: 13 May 2026, by LG K. Kailashnathan"],
  [fact("N. Rangasamy sworn in as Puducherry CM for a record fifth term", "pudu_air"),
   fact("Rangasamy takes oath as Puducherry CM for 5th time", "pudu_tribune")],
  why="The BJP is the AINRC's NDA partner; the DMK and Congress are in the opposition.",
  current=ca("2026-05-13"))

G(T, DEF, "Intermediate",
  "Who took over as Chief of the Army Staff on 30 June 2026, succeeding General Upendra Dwivedi?",
  ["General Dhiraj Seth", "General N. S. Raja Subramani", "General Manoj Pande", "Air Chief Marshal Ashutosh Dixit"],
  "*", "Army Chief, June 2026",
  "The government named Lt Gen Dhiraj Seth, then Vice Chief of the Army Staff, as the next Army Chief on 13 June 2026. "
  "He took over on 30 June 2026, when General Upendra Dwivedi retired.",
  ["Appointment announced: 13 June 2026", "Took over: 30 June 2026", "Earlier post: Vice Chief of the Army Staff"],
  [fact("Lt Gen Dhiraj Seth appointed next Army Chief, to take charge on 30 June 2026", "army_outlook"),
   fact("Dhiraj Seth appointed next Chief of Army Staff, succeeding Gen Dwivedi", "army_statesman")],
  why="Gen Raja Subramani became CDS in 2026; Gen Pande was Army Chief before Dwivedi; Dixit is the IAF chief.",
  current=ca("2026-06-30"))

G(T, DEF, "Intermediate",
  "Air Chief Marshal Ashutosh Dixit took over as Chief of the Air Staff on 31 October 2026. Whom did he succeed?",
  ["Air Chief Marshal A. P. Singh", "Air Chief Marshal V. R. Chaudhari", "Air Marshal Inderpal Singh Walia",
   "Air Chief Marshal R. K. S. Bhadauria"], "*",
  "IAF Chief, October 2026",
  "Air Marshal Ashutosh Dixit, the Vice Chief of the Air Staff, was named IAF chief on 6 October 2026 and took over on "
  "31 October 2026 as the 29th Chief of the Air Staff when Air Chief Marshal A. P. (Amar Preet) Singh retired. Air "
  "Marshal Inderpal Singh Walia became the new Vice Chief from 1 November 2026.",
  ["Took over: 31 Oct 2026 (29th CAS)", "Predecessor: ACM A. P. Singh", "New VCAS: Air Marshal I. S. Walia"],
  [fact("Air Marshal Ashutosh Dixit appointed new IAF chief, to succeed A. P. Singh", "iaf_morung"),
   fact("Ashutosh Dixit takes charge as 29th Chief of the Air Staff on 31 Oct 2026", "iaf_psu")],
  why="Chaudhari and Bhadauria were earlier chiefs; Walia became Vice Chief, not the predecessor.",
  current=ca("2026-10-31"))

G(T, ST, "Intermediate",
  "Which two wetlands were added to India's list of Ramsar sites ahead of World Wetlands Day 2026, taking the total "
  "to 98?",
  ["Patna Bird Sanctuary (Uttar Pradesh) and Chhari-Dhand (Gujarat)", "Sultanpur and Bhindawas (Haryana)",
   "Chilika Lake and Bhitarkanika (Odisha)", "Keoladeo (Rajasthan) and Loktak (Manipur)"], "*",
  "Ramsar sites, 2026",
  "Environment Minister Bhupender Yadav announced on 31 January 2026 that the Patna Bird Sanctuary in Etah district "
  "(Uttar Pradesh) and Chhari-Dhand in Kutch (Gujarat) had been added to the Ramsar list, raising India's count to 98.",
  ["New sites: Patna Bird Sanctuary (Etah, UP), Chhari-Dhand (Kutch, Gujarat)", "Count: 98"],
  [fact("Patna Bird Sanctuary and Chhari-Dhand became Ramsar sites", "ramsar_open"),
   fact("Two new wetlands added to Ramsar list ahead of World Wetlands Day 2026", "ramsar_star")],
  why="The other pairs are older Ramsar sites, not the 2026 additions.",
  current=ca("2026-01-31"))

G(T, GOV, "Intermediate",
  "What was the central theme of the 77th Republic Day parade on Kartavya Path on 26 January 2026?",
  ["150 years of Vande Mataram", "Nari Shakti", "Swarnim Bharat: Virasat aur Vikas", "Viksit Bharat @2047"], "*",
  "Republic Day 2026",
  "The 2026 parade was built around 150 years of the national song Vande Mataram, with sub-themes such as "
  "'Svatantrata Ka Mantr - Vande Mataram' and 'Samriddhi Ka Mantr - Aatmanirbhar Bharat'. The Ministry of Culture's "
  "tableau was titled '150 Years of Vande Mataram'.",
  ["Theme: 150 years of Vande Mataram", "Date: 26 January 2026 (77th Republic Day)"],
  [fact("77th Republic Day parade themed on 150 years of Vande Mataram", "rday_bt"),
   fact("150 years of Vande Mataram to be the theme of Republic Day parade 2026", "rday_adu")],
  why="The other phrases were not the 2026 parade theme.",
  current=ca("2026-01-26"))

G(T, DEF, "Intermediate",
  "Where did the Indian Navy hold its Navy Day 2025 Operational Demonstration on 3 December 2025, with President "
  "Droupadi Murmu as chief guest?",
  ["Shangumugham Beach, Thiruvananthapuram", "Puri, Odisha", "Marina Beach, Chennai", "RK Beach, Visakhapatnam"], "*",
  "Navy Day 2025",
  "The Navy Day Operational Demonstration was held for the first time at Shangumugham Beach in Thiruvananthapuram on "
  "3 December 2025, hosted by Admiral Dinesh K. Tripathi. The 2024 edition was held at Puri, Odisha.",
  ["Venue 2025: Shangumugham Beach, Thiruvananthapuram", "Venue 2024: Puri"],
  [fact("Navy Day 2025 operational demonstration at Shangumugham Beach with the President as chief guest",
        "navy_adu"),
   fact("President Murmu attended the Navy Day 2025 demonstration in Thiruvananthapuram on 3 Dec 2025", "navy_onm")],
  why="Puri hosted the 2024 demonstration; Chennai and Visakhapatnam were not the 2025 venue.",
  current=ca("2025-12-03"))

G(T, DEF, "Intermediate",
  "The 11th edition of Exercise Mitra Shakti was held at the Foreign Training Node, Belagavi, in November 2025. It is "
  "a joint military exercise between India and which country?",
  ["Sri Lanka", "Maldives", "Nepal", "Bangladesh"], "*",
  "Exercise Mitra Shakti 2025",
  "Mitra Shakti is the India-Sri Lanka army exercise held alternately in the two countries. The 11th edition ran at "
  "Belagavi, Karnataka, from 10 November 2025, focusing on counter-terrorism in urban and semi-urban terrain.",
  ["Partner: Sri Lanka", "Venue 2025: Belagavi, Karnataka", "Edition: 11th"],
  [fact("India-Sri Lanka exercise Mitra Shakti-2025 underway in Belagavi", "ms_air"),
   fact("11th edition of Indo-Sri Lanka exercise Mitra Shakti to be held in Belagavi from 10 Nov", "ms_statesman")],
  why="India's exercises with the Maldives, Nepal and Bangladesh have other names (Ekuverin, Surya Kiran, Sampriti).",
  current=ca("2025-11-10"))

G(T, GOV, "Intermediate",
  "Who was sworn in as the Chief Information Commissioner on 15 December 2025?",
  ["Raj Kumar Goyal", "Heeralal Samariya", "Gyanesh Kumar", "Sanjay Kothari"], "*",
  "Chief Information Commissioner",
  "President Droupadi Murmu administered the oath to Raj Kumar Goyal, a retired IAS officer and former Secretary, "
  "Department of Justice, as Chief Information Commissioner at Rashtrapati Bhavan on 15 December 2025. Eight "
  "information commissioners also took oath, bringing the Central Information Commission to full strength.",
  ["CIC: Raj Kumar Goyal (from 15 Dec 2025)", "Predecessor: Heeralal Samariya"],
  [fact("Raj Kumar Goyal sworn in as Chief Information Commissioner on 15 Dec 2025", "cic_dh"),
   fact("CIC profile: Goyal sworn in by the President on 15 Dec 2025", "cic_site")],
  why="Samariya was the previous CIC; Gyanesh Kumar is the Chief Election Commissioner; Kothari was a former CVC.",
  current=ca("2025-12-15"))

G(T, DEF, "Intermediate",
  "Exercise Trishul, the tri-service exercise held along India's western front in November 2025, was led by which "
  "service?",
  ["Indian Navy (Western Naval Command)", "Indian Army (Southern Command)", "Indian Air Force (South Western Air Command)",
   "Indian Coast Guard"], "*",
  "Exercise Trishul 2025",
  "Tri-Services Exercise Trishul was led by the Indian Navy's Western Naval Command, with the Army's Southern Command "
  "and the IAF's South Western Air Command as the main participating formations. It covered Rajasthan, Gujarat, Sir "
  "Creek and the northern Arabian Sea and ended with an amphibious exercise off Saurashtra on 13 November 2025.",
  ["Lead service: Indian Navy (Western Naval Command)", "Other formations: Army Southern Command, IAF SWAC"],
  [fact("Exercise Trishul: led by Western Naval Command, 3-13 Nov 2025, ended off Saurashtra coast", "trishul_wiki"),
   fact("Indian Navy to lead Tri-Services Exercise Trishul", "trishul_strat")],
  why="The Army and IAF formations took part but did not lead; the Coast Guard was not the lead.",
  current=ca("2025-11-13"))

GS(T, GOV, "Advanced", "the commemoration of 150 years of the national song Vande Mataram",
   ["On 7 November 2025 the Prime Minister inaugurated a year-long commemoration and released a postage stamp and a "
    "coin.",
    "The song was written by Bankim Chandra Chatterjee, and 7 November 1875 is taken as its date of composition.",
    "The year-long commemoration was scheduled to end on 26 January 2026."],
   [True, True, False],
   "Vande Mataram at 150",
   "The PM opened the year-long celebration at the Indira Gandhi Indoor Stadium, New Delhi, on 7 November 2025, "
   "released a commemorative stamp and coin and launched a portal. The date marks the song's composition by Bankim "
   "Chandra Chatterjee on 7 November 1875. The commemoration runs until 7 November 2026, not 26 January 2026.",
   [fact("PM releases stamp and coin to mark 150 years of Vande Mataram on 7 Nov 2025", "vm_tribune"),
    fact("PM inaugurates year-long commemoration of 150 years of Vande Mataram", "vm_pmindia")],
   why="Statement 3 is wrong: the commemoration runs to 7 November 2026.",
   current=ca("2025-11-07"))

GS(T, ST, "Advanced", "the new districts created in the Union Territory of Ladakh in April 2026",
   ["The Lieutenant Governor approved five new districts, taking Ladakh's total to seven.",
    "Nubra and Sham were carved out of Kargil district.",
    "Zanskar and Drass were carved out of Kargil district."],
   [True, False, True],
   "Ladakh's new districts",
   "On 27 April 2026 Lt Governor Vinai Kumar Saxena approved five new districts, raising the count from two to seven. "
   "Nubra, Sham and Changthang were carved out of Leh district; Zanskar and Drass came from Kargil district. The MHA had "
   "approved the plan in August 2024.",
   [fact("Ladakh gets five new districts as LG Saxena approves proposal (27 Apr 2026)", "ladakh_tv"),
    fact("Creation of five new districts in Ladakh approved; Nubra, Sham, Changthang from Leh", "ladakh_kr")],
   why="Statement 2 is wrong: Nubra and Sham came from Leh district.",
   current=ca("2026-04-27"))

GS(T, DEF, "Advanced", "Exercise Ajeya Warrior-25",
   ["It was the eighth edition of the exercise and was held in Rajasthan in November 2025.",
    "It is a joint military exercise between India and the United Kingdom.",
    "Its previous edition was held at Salisbury Plains in the United Kingdom in 2023."],
   [True, True, True],
   "Exercise Ajeya Warrior",
   "The 8th India-UK Ajeya Warrior exercise ran from 17 to 30 November 2025 at the Mahajan Field Firing Ranges near "
   "Bikaner, Rajasthan, focusing on counter-terrorism under a UN mandate. The 7th edition (2023) was held at Salisbury "
   "Plains, UK; the exercise is biennial and alternates between the two countries.",
   [fact("8th India-UK Ajeya Warrior exercise begins in Bikaner on 17 Nov 2025", "aw_air"),
    fact("Ajeya Warrior-25 kicks off in Rajasthan; earlier edition at Salisbury Plains, UK, 2023", "aw_statesman")],
   why="All three statements are correct.",
   current=ca("2025-11-17"))

GS(T, GOV, "Advanced", "the LVM3-M6 mission of 24 December 2025",
   ["It placed its satellite in a geosynchronous transfer orbit.",
    "It launched AST SpaceMobile's BlueBird Block-2 satellite of about 6,100 kg, the heaviest payload carried by an "
    "LVM3.",
    "It was ISRO's first dedicated commercial launch for a customer from the United States."],
   [False, True, True],
   "LVM3-M6 / BlueBird Block-2",
   "LVM3-M6 lifted off from Sriharikota on 24 December 2025 and placed the ~6,100 kg BlueBird Block-2 communication "
   "satellite of US firm AST SpaceMobile in a low Earth orbit of about 520 km. It beat the ~4,400 kg CMS-03 as the "
   "heaviest LVM3 payload and was ISRO's first dedicated commercial launch for a US customer.",
   [fact("LVM3-M6 launched BlueBird Block-2 on 24 Dec 2025, setting new records", "lvm6_bt"),
    fact("India's heaviest launched satellite: BlueBird Block-2 (~6,100 kg) beat CMS-03", "lvm6_arab")],
   why="Statement 1 is wrong: the satellite went to low Earth orbit (~520 km), not GTO.",
   current=ca("2025-12-24"))

# ====================================================================== International Current Affairs (9 / 5 / 8)
T = "International Current Affairs"
BIL, GLO = "Bilateral relations", "Global events"

G(T, GLO, "Basic",
  "Zohran Mamdani, who won the election of 4 November 2025, became the first Muslim mayor of which city?",
  ["New York City", "London", "Chicago", "Toronto"], "*",
  "New York City mayoral election 2025",
  "Democratic socialist Zohran Mamdani defeated Andrew Cuomo and Curtis Sliwa on 4 November 2025 with about 50.6% of "
  "the vote, becoming New York City's first Muslim and first South Asian mayor. He took office on 1 January 2026.",
  ["Election: 4 Nov 2025", "City: New York", "Firsts: first Muslim and South Asian mayor"],
  [fact("Zohran Mamdani elected mayor of New York City on 4 Nov 2025 in a historic win", "mamdani_aj"),
   fact("Mamdani wins New York City mayor's race", "mamdani_scmp")],
  why="London's mayor is Sadiq Khan; Chicago and Toronto did not hold this election.",
  current=ca("2025-11-04"))

G(T, GLO, "Basic",
  "Who won Chile's presidential runoff held on 14 December 2025?",
  ["José Antonio Kast", "Jeannette Jara", "Gabriel Boric", "Evelyn Matthei"], "*",
  "Chile presidential election 2025",
  "José Antonio Kast won the runoff of 14 December 2025 with about 58% of the vote against left-wing candidate "
  "Jeannette Jara, who conceded. It was his third run for the presidency and the sharpest shift to the right since "
  "Chile's return to democracy in 1990.",
  ["Runoff: 14 Dec 2025", "Winner: José Antonio Kast (~58%)", "Runner-up: Jeannette Jara"],
  [fact("Chile shifts sharply right as José Antonio Kast wins the presidency on 14 Dec 2025", "chile_kpbs"),
   fact("Chile elects Kast as president", "chile_star")],
  why="Jara lost the runoff; Boric was the outgoing president; Matthei did not win.",
  current=ca("2025-12-14"))

G(T, GLO, "Basic",
  "Péter Magyar, whose Tisza party won the election of 12 April 2026, was sworn in on 9 May 2026 as Prime Minister of "
  "which country, ending Viktor Orbán's 16-year rule?",
  ["Hungary", "Poland", "Slovakia", "Czech Republic"], "*",
  "Hungary's change of government",
  "Tisza won 141 of 199 seats in Hungary's parliamentary election of 12 April 2026, a two-thirds majority. Péter "
  "Magyar was elected Prime Minister at the inaugural session of the new National Assembly on 9 May 2026.",
  ["Election: 12 Apr 2026 (Tisza: 141/199 seats)", "PM sworn in: 9 May 2026"],
  [fact("Péter Magyar sworn in as Hungary's PM on 9 May 2026 after landslide April election", "hun_euronews"),
   fact("Magyar sworn in as Hungary's prime minister", "hun_star")],
  why="Orbán was Hungary's PM; the other countries were not involved.",
  current=ca("2026-05-09"))

G(T, GLO, "Basic",
  "Who was sworn in as Prime Minister of Nepal on 27 March 2026 after the Rastriya Swatantra Party won 182 of 275 "
  "seats?",
  ["Balendra Shah", "Sushila Karki", "K. P. Sharma Oli", "Pushpa Kamal Dahal"], "*",
  "Nepal general election 2026",
  "The snap election of 5 March 2026 followed the September 2025 protests. The RSP won 182 of 275 seats and former "
  "Kathmandu mayor Balendra (Balen) Shah, 35, took oath on 27 March 2026 before President Ramchandra Paudel. He also "
  "defeated K. P. Sharma Oli in Oli's own constituency.",
  ["Election: 5 Mar 2026", "Oath: 27 Mar 2026", "PM: Balendra Shah (RSP)"],
  [fact("Rapper Balendra Shah sworn in as Nepali prime minister on 27 Mar 2026", "nepal_dawn"),
   fact("Ex-rapper Shah sworn in as Nepal PM after sweeping election win", "nepal_print")],
  why="Sushila Karki was the interim PM; Oli and Dahal are former PMs.",
  current=ca("2026-03-27"))

G(T, GLO, "Basic",
  "António José Seguro, who defeated André Ventura in the runoff of 8 February 2026, was elected President of which "
  "country?",
  ["Portugal", "Spain", "Brazil", "Italy"], "*",
  "Portugal presidential election 2026",
  "Socialist António José Seguro won the 8 February 2026 runoff with about 67% against Chega leader André Ventura. It "
  "was the first presidential runoff in Portugal in 40 years. He took office on 9 March 2026, succeeding Marcelo Rebelo "
  "de Sousa.",
  ["Runoff: 8 Feb 2026", "Winner: António José Seguro", "Took office: 9 Mar 2026"],
  [fact("Centre-left Socialist candidate Seguro wins Portugal's presidential runoff on 8 Feb 2026", "port_kpbs"),
   fact("Portugal elects Socialist as president by landslide", "port_star")],
  why="The election was in Portugal; Ventura leads Portugal's Chega party.",
  current=ca("2026-02-08"))

G(T, GLO, "Basic",
  "In Japan's snap general election of 8 February 2026, the Liberal Democratic Party won a two-thirds majority in the "
  "lower house on its own under which Prime Minister?",
  ["Sanae Takaichi", "Shigeru Ishiba", "Fumio Kishida", "Yoshihide Suga"], "*",
  "Japan general election 2026",
  "Prime Minister Sanae Takaichi called a snap election three months after taking office. On 8 February 2026 the LDP "
  "won about 315 of 465 seats, a single-party supermajority and its best lower-house result, beating 304 seats in 1986.",
  ["Election: 8 Feb 2026", "LDP: ~315 of 465 seats", "PM: Sanae Takaichi"],
  [fact("Japan election results confirm super-majority for Takaichi's party", "japan_star"),
   fact("LDP's previous best lower-house result was 304 seats in 1986", "japan_nippon")],
  why="Ishiba, Kishida and Suga were earlier LDP prime ministers.",
  current=ca("2026-02-08"))

G(T, GLO, "Basic",
  "Who won Brazil's presidential runoff of 25 October 2026?",
  ["Luiz Inácio Lula da Silva", "Flávio Bolsonaro", "Jair Bolsonaro", "Tarcísio de Freitas"], "*",
  "Brazil presidential election 2026",
  "Flávio Bolsonaro led the first round on 4 October 2026, but President Lula won the runoff of 25 October 2026 with "
  "about 51.8% of the valid votes, securing a fourth, non-consecutive term. Bolsonaro sought to annul the result.",
  ["First round: 4 Oct 2026", "Runoff: 25 Oct 2026", "Winner: Lula (fourth term)"],
  [fact("Lula re-elected against Flávio Bolsonaro in the runoff", "brazil_benin"),
   fact("Lula wins re-election in Brazil as Bolsonaro rejects run-off result", "brazil_bah")],
  why="Flávio Bolsonaro lost the runoff; Jair Bolsonaro and Tarcísio de Freitas were not in it.",
  current=ca("2026-10-25"))

G(T, GLO, "Basic",
  "Who won Peru's presidential runoff of 7 June 2026?",
  ["Keiko Fujimori", "Roberto Sánchez", "Dina Boluarte", "Pedro Castillo"], "*",
  "Peru presidential election 2026",
  "Keiko Fujimori of Fuerza Popular beat leftist Roberto Sánchez in the runoff of 7 June 2026 with 50.135% of valid "
  "votes, a margin of 49,641 votes at the full count.",
  ["Runoff: 7 June 2026", "Winner: Keiko Fujimori (50.135%)", "Runner-up: Roberto Sánchez"],
  [fact("Keiko Fujimori wins Peru's presidency as full count confirms her by 49,641 votes", "peru_merco"),
   fact("Conservative candidate Keiko Fujimori wins Peru's presidential runoff", "peru_ap")],
  why="Sánchez lost; Boluarte and Castillo are former presidents.",
  current=ca("2026-06-07"))

G(T, GLO, "Basic",
  "Abelardo de la Espriella narrowly won the presidential runoff of 21 June 2026 in which country?",
  ["Colombia", "Venezuela", "Ecuador", "Chile"], "*",
  "Colombia presidential election 2026",
  "Right-wing populist Abelardo de la Espriella won Colombia's runoff of 21 June 2026 with about 49.7% against Iván "
  "Cepeda (48.7%). The registrar confirmed the count and Cepeda conceded on 24 June. The new president took office on "
  "7 August 2026, succeeding Gustavo Petro.",
  ["Runoff: 21 June 2026", "Winner: de la Espriella", "Runner-up: Iván Cepeda"],
  [fact("Colombian right-wing candidate Espriella wins tight presidential race", "col_dawn"),
   fact("Registrar says preliminary count showing de la Espriella's narrow victory is accurate", "col_local10")],
  why="The election was in Colombia, not in the other countries.",
  current=ca("2026-06-21"))

G(T, GLO, "Intermediate",
  "From 10 December 2025, which country became the first to enforce a nationwide ban on social media accounts for "
  "children under 16?",
  ["Australia", "New Zealand", "Denmark", "Malaysia"], "*",
  "Under-16 social media ban",
  "Australia's law took effect at midnight on 10 December 2025, requiring platforms such as Facebook, Instagram, "
  "TikTok, Snapchat, YouTube, X, Reddit and others to block or remove accounts of users under 16, with fines of up to "
  "A$49.5 million. Denmark, New Zealand and Malaysia said they may study or copy the model.",
  ["Effective: 10 Dec 2025", "Country: Australia", "Age limit: under 16"],
  [fact("Australia begins enforcing world-first teen social media ban", "aus_dawn"),
   fact("Australia becomes world's first country to ban social media for under-16s", "aus_air")],
  why="Denmark, New Zealand and Malaysia were only studying similar rules.",
  current=ca("2025-12-10"))

G(T, GLO, "Intermediate",
  "Who was elected President of Myanmar by its new parliament in April 2026 and sworn in on 10 April 2026?",
  ["Min Aung Hlaing", "Ye Win Oo", "Aung San Suu Kyi", "Win Myint"], "*",
  "Myanmar presidency 2026",
  "After elections dominated by the army-backed party, parliament elected Senior General Min Aung Hlaing, leader of "
  "the 2021 coup, as President with 429 of 584 votes. He first gave up the post of Commander-in-Chief, which went to "
  "Ye Win Oo, as the constitution bars the president from holding it.",
  ["Votes: 429 of 584", "Sworn in: 10 April 2026", "New C-in-C: Ye Win Oo"],
  [fact("Myanmar's parliament elects ruling general as president, keeping army in charge", "mya_star"),
   fact("Junta chief Min Aung Hlaing elected president by pro-military parliament", "mya_arab")],
  why="Ye Win Oo became army chief; Suu Kyi and Win Myint were ousted in the 2021 coup.",
  current=ca("2026-04-10"))

G(T, GLO, "Intermediate",
  "Laura Fernández won the presidential election of 1 February 2026 in the first round, becoming the second woman "
  "president of which country?",
  ["Costa Rica", "Honduras", "Panama", "Chile"], "*",
  "Costa Rica presidential election 2026",
  "Laura Fernández, candidate of the ruling party and former minister of the presidency under Rodrigo Chaves, won "
  "about 48.3% on 1 February 2026, above the 40% needed to avoid a runoff. She is Costa Rica's second woman president.",
  ["Election: 1 Feb 2026", "Share: ~48.3% (threshold 40%)", "Country: Costa Rica"],
  [fact("Laura Fernández wins Costa Rica presidential election", "cr_havana"),
   fact("Populist conservative Laura Fernández wins Costa Rica's presidential election", "cr_wgcu")],
  why="The election was in Costa Rica; Honduras elected Nasry Asfura, Chile elected José Antonio Kast.",
  current=ca("2026-02-01"))

G(T, GLO, "Intermediate",
  "After Thailand's general election of 8 February 2026, who was elected Prime Minister by the new parliament on "
  "19 March 2026?",
  ["Anutin Charnvirakul", "Paetongtarn Shinawatra", "Srettha Thavisin", "Prayut Chan-o-cha"], "*",
  "Thailand after the 2026 election",
  "Anutin Charnvirakul's Bhumjaithai Party won 193 of 500 seats on 8 February 2026, the most of any party. With Pheu "
  "Thai and 14 smaller parties as partners, Anutin was re-elected PM with 293 votes on 19 March 2026.",
  ["Election: 8 Feb 2026 (Bhumjaithai 193/500)", "PM vote: 19 Mar 2026, Anutin re-elected"],
  [fact("Bhumjaithai leader Anutin Charnvirakul re-elected Prime Minister of Thailand", "thai_prd"),
   fact("Thailand's new parliament elects Anutin Charnvirakul as prime minister", "thai_dawn")],
  why="Paetongtarn, Srettha and Prayut are former prime ministers.",
  current=ca("2026-03-19"))

G(T, GLO, "Intermediate",
  "Nasry Asfura was declared winner on 24 December 2025 of the presidential election held on 30 November 2025 in "
  "which country?",
  ["Honduras", "Guatemala", "El Salvador", "Costa Rica"], "*",
  "Honduras presidential election 2025",
  "Honduras's electoral authority declared National Party candidate Nasry Asfura, a former mayor of Tegucigalpa, the "
  "winner with 40.3% against 39.5% for Salvador Nasralla, more than three weeks after a vote marked by delays and "
  "fraud allegations.",
  ["Vote: 30 Nov 2025", "Declared: 24 Dec 2025", "Asfura 40.3% vs Nasralla 39.5%"],
  [fact("Trump-backed Asfura wins Honduras presidency after disputed election", "hond_ksl"),
   fact("Nasry Asfura declared victor of Honduran presidential election", "hond_bah")],
  why="The election was in Honduras.",
  current=ca("2025-12-24"))

GS(T, GLO, "Advanced", "the events in Venezuela in January 2026",
   ["Nicolás Maduro and his wife were seized in a US operation on 3 January 2026 and flown to New York to face "
    "charges.",
    "Delcy Rodríguez was administered the oath as acting president on 5 January 2026 by National Assembly President "
    "Jorge Rodríguez.",
    "Delcy Rodríguez publicly welcomed the US operation."],
   [True, True, False],
   "Venezuela, January 2026",
   "A US operation on Saturday 3 January 2026 seized Maduro and Cilia Flores, who were flown to New York on drug and "
   "weapons charges. Vice President Delcy Rodríguez was entrusted with the government by the Supreme Court and sworn "
   "in on 5 January by her brother Jorge Rodríguez. She denounced the operation and demanded Maduro's release.",
   [fact("Delcy Rodríguez sworn in as Venezuela's president after Maduro abduction (5 Jan 2026)", "ven_aj"),
    fact("Maduro captured in US operation on 3 Jan 2026", "ven_nat")],
   why="Statement 3 is wrong: she condemned the operation as a breach of the UN Charter.",
   current=ca("2026-01-03"))

GS(T, BIL, "Advanced", "Operation Sagar Bandhu",
   ["It was launched to help the Maldives after floods in November 2025.",
    "India launched it on 28 November 2025 as the first responder after Cyclone Ditwah hit Sri Lanka.",
    "Indian Army teams installed Bailey bridges in Sri Lanka as part of it."],
   [False, True, True],
   "Operation Sagar Bandhu",
   "India began Operation Sagar Bandhu on 28 November 2025 to help Sri Lanka after Cyclone Ditwah. Navy warships and "
   "IAF aircraft carried relief (12 tonnes on a C-130J on 29 November, 53 tonnes by 1 December), and the Army later ran "
   "medical camps and installed Bailey bridges, for example on the Kandy-Nuwara Eliya road.",
   [fact("India launched Operation Sagar Bandhu on 28 Nov 2025 as first responder after Cyclone Ditwah", "sb_hci"),
    fact("India launches Operation Sagar Bandhu to support Sri Lanka after Cyclone Ditwah", "sb_air"),
    fact("Army installed Bailey bridges and treated 1,250 people in Sri Lanka", "sb_gk")],
   why="Statement 1 is wrong: the operation was for Sri Lanka, not the Maldives.",
   current=ca("2025-11-28"))

GS(T, BIL, "Advanced", "the India-US trade framework announced in February 2026",
   ["The joint statement on a framework for an interim trade agreement is dated 6 February 2026.",
    "Under the framework the US is to apply a reciprocal tariff of 18% on most goods imported from India.",
    "The interim agreement was fully concluded and brought into force in February 2026."],
   [True, True, False],
   "India-US interim trade framework",
   "The joint statement of 6 February 2026 set out a framework for an interim agreement: the US would charge 18% on "
   "most Indian goods and remove the reciprocal tariff on items such as generic medicines, gems and aircraft parts once "
   "the interim agreement is concluded, while India would cut tariffs on US industrial and some farm goods. The "
   "agreement itself was still to be finalised.",
   [fact("Joint Statement on a Framework for an Interim Agreement dated 6 Feb 2026", "ustrade_gov"),
    fact("Reciprocal tariffs on India to come down to 18%; 0% on generic pharma, subject to the interim deal",
         "ustrade_bt")],
   why="Statement 3 is wrong: the framework was only a step towards an interim agreement still to be concluded.",
   current=ca("2026-02-06"))

GS(T, BIL, "Advanced", "Prime Minister Modi's visit to Israel in February 2026",
   ["On 25 February 2026 he became the first Indian Prime Minister to address the Knesset.",
    "He was conferred the 'Speaker of the Knesset Medal', the highest honour of the Israeli Parliament."],
   [True, True],
   "PM's visit to Israel, 2026",
   "During his state visit of 25-26 February 2026, PM Modi addressed the Knesset, the first Indian PM to do so, and "
   "Speaker Amir Ohana presented him the Speaker of the Knesset Medal immediately afterwards.",
   [fact("PM Modi addressed the Knesset on 25 Feb 2026, the first Indian PM to do so", "knesset_quint"),
    fact("PM Modi received the Speaker of the Knesset Medal, highest honour of Israel's parliament", "knesset_fpj")],
   why="Both statements are correct.",
   current=ca("2026-02-25"))

GS(T, GLO, "Advanced", "the 'Board of Peace' for Gaza",
   ["US President Donald Trump signed its charter at the World Economic Forum in Davos on 22 January 2026.",
    "India signed the charter at Davos as a founding member."],
   [True, False],
   "Board of Peace",
   "Trump launched the Gaza Board of Peace and signed its charter at Davos on 22 January 2026; Pakistan, Saudi Arabia, "
   "the UAE, Qatar and others signed on, and permanent membership was priced at USD 1 billion. India was invited but "
   "did not attend the signing and had not decided whether to join.",
   [fact("Trump launches Board of Peace at signing ceremony in Davos on 22 Jan 2026", "bop_aj"),
    fact("India absent at signing of Trump's Board of Peace in Davos", "bop_na")],
   why="Statement 2 is wrong: India stayed away from the signing.",
   current=ca("2026-01-22"))

GS(T, BIL, "Advanced", "Prime Minister Modi's visit to Jordan in December 2025",
   ["The visit on 15-16 December 2025 marked 75 years of diplomatic relations between India and Jordan.",
    "A twinning arrangement between Petra and Ellora, both UNESCO World Heritage Sites, was agreed.",
    "Jordan was the first leg of a three-nation tour that also took him to Ethiopia and Oman."],
   [True, True, True],
   "India-Jordan, December 2025",
   "At King Abdullah II's invitation the PM visited Jordan on 15-16 December 2025, marking 75 years of ties. MoUs on "
   "renewable energy, water, culture and digital technology were signed, Petra and Ellora were twinned, and he proposed "
   "doubling trade to USD 5 billion. He then went to Ethiopia and Oman.",
   [fact("Joint statement: PM Modi visited Jordan on 15-16 Dec 2025, 75 years of relations", "jordan_nm"),
    fact("Highlights of PM's Jordan visit: Petra-Ellora twinning, energy and water MoUs; first leg of three-nation tour",
         "jordan_fpj")],
   why="All three statements are correct.",
   current=ca("2025-12-15"))

GS(T, GLO, "Advanced", "the inscription of Deepavali by UNESCO",
   ["Deepavali was inscribed on UNESCO's Representative List of the Intangible Cultural Heritage of Humanity on "
    "10 December 2025, at the committee session held at the Red Fort, New Delhi.",
    "Deepavali is the first element from India on that list."],
   [True, False],
   "Deepavali on UNESCO's list",
   "The 20th session of the Intergovernmental Committee for the Safeguarding of the Intangible Cultural Heritage met at "
   "the Red Fort from 8 to 13 December 2025 and inscribed Deepavali on 10 December. It is India's 16th element on the "
   "Representative List; earlier ones include Kumbh Mela, Yoga and Durga Puja in Kolkata.",
   [fact("UNESCO adds Deepavali to Intangible Cultural Heritage list on 10 Dec 2025 at Red Fort session", "deep_air"),
    fact("Deepavali becomes India's 16th inscription on the list", "deep_sb18")],
   why="Statement 2 is wrong: Deepavali is India's 16th element on the list.",
   current=ca("2025-12-10"))

GS(T, GLO, "Advanced", "the eruption of the Hayli Gubbi volcano",
   ["It erupted on 23 November 2025 in the Afar region of Ethiopia, its first known eruption in about 12,000 years.",
    "Its ash cloud drifted over India and led to flight cancellations and delays."],
   [True, True],
   "Hayli Gubbi eruption",
   "Hayli Gubbi in Ethiopia's Afar region erupted on Sunday 23 November 2025, sending ash about 14 km high. Winds "
   "carried the ash over the Red Sea, Yemen, Oman and the Arabian Sea to western and northern India, where airlines "
   "cancelled or delayed flights before the IMD said the cloud would clear on 25 November.",
   [fact("Ethiopian volcano Hayli Gubbi erupted after about 12,000 years", "hg_aj"),
    fact("Ash cloud from Hayli Gubbi disrupts international flights from Delhi", "hg_tribune")],
   why="Both statements are correct.",
   current=ca("2025-11-23"))

# ====================================================================== Government Schemes (0 / 3 / 1)
T = "Government Schemes"
CEN, LAU = "Central schemes", "Scheme launches and changes"

G(T, LAU, "Intermediate",
  "What is the outlay of the Export Promotion Mission approved by the Union Cabinet in November 2025 for 2025-26 to "
  "2030-31?",
  ["₹25,060 crore", "₹20,000 crore", "₹45,060 crore", "₹7,280 crore"], "*",
  "Export Promotion Mission",
  "On 12 November 2025 the Cabinet approved the Export Promotion Mission with ₹25,060 crore over six years, folding "
  "export schemes such as the Interest Equalisation Scheme and the Market Access Initiative into one framework. It "
  "also approved a separate ₹20,000 crore Credit Guarantee Scheme for Exporters, so the package totals ₹45,060 crore.",
  ["EPM: ₹25,060 crore (FY26-FY31)", "CGSE: ₹20,000 crore", "Total: ₹45,060 crore"],
  [fact("Government approves ₹25,060 crore Export Promotion Mission for six years", "epm_mp"),
   fact("Cabinet clears ₹45,060 crore for exporters: EPM plus ₹20,000 crore credit guarantee scheme", "epm_angel")],
  why="₹20,000 crore is the credit guarantee scheme; ₹45,060 crore is the combined package; ₹7,280 crore is the rare "
      "earth magnet scheme.",
  current=ca("2025-11-12"))

G(T, LAU, "Intermediate",
  "The ₹1 lakh crore Research, Development and Innovation (RDI) Scheme launched by the Prime Minister on 3 November "
  "2025 has its fund housed in which body?",
  ["Anusandhan National Research Foundation (ANRF)", "NITI Aayog", "SIDBI", "Department of Biotechnology"], "*",
  "RDI Scheme",
  "The PM launched the RDI Scheme Fund at the Emerging Science, Technology and Innovation Conclave (ESTIC) 2025 at "
  "Bharat Mandapam on 3 November 2025. A special purpose vehicle within the ANRF is custodian of the ₹1 lakh crore "
  "corpus, which will back private-sector R&D in areas such as deep tech, AI, semiconductors and quantum technology.",
  ["Launched: 3 Nov 2025 at ESTIC 2025", "Corpus: ₹1 lakh crore", "Custodian: SPV within ANRF"],
  [fact("PM launched ₹1 lakh crore RDI Scheme Fund at ESTIC 2025", "rdi_etv"),
   fact("RDI fund to be housed in a special purpose vehicle under ANRF", "rdi_upstox")],
  why="NITI Aayog, SIDBI and DBT are not the custodian of the RDI fund.",
  current=ca("2025-11-03"))

G(T, CEN, "Intermediate",
  "The ₹7,280 crore scheme approved by the Union Cabinet in November 2025 aims to create domestic capacity of how much "
  "sintered rare earth permanent magnets?",
  ["6,000 tonnes per annum", "1,500 tonnes per annum", "60,000 tonnes per annum", "600 tonnes per annum"], "*",
  "Rare earth permanent magnet scheme",
  "Approved on 26 November 2025, the scheme gives ₹6,450 crore of sales-linked incentives over five years and ₹750 "
  "crore of capital subsidy for integrated plants totalling 6,000 tonnes a year, from rare earth oxides to finished "
  "magnets. It runs seven years from award, including a two-year gestation period.",
  ["Outlay: ₹7,280 crore (₹6,450 cr incentives + ₹750 cr subsidy)", "Capacity target: 6,000 MTPA"],
  [fact("Cabinet approves ₹7,280 crore rare earth permanent magnets scheme for 6,000 MTPA", "repm_tribune"),
   fact("Centre clears ₹7,280 crore push to boost rare earth magnet production", "repm_bt")],
  why="The other figures are not the scheme's capacity target.",
  current=ca("2025-11-26"))

GS(T, CEN, "Advanced", "the export support schemes approved in November 2025",
   ["The Export Promotion Mission covers the period 2025-26 to 2030-31.",
    "Under the Credit Guarantee Scheme for Exporters, NCGTC gives lenders 100% guarantee cover on eligible export "
    "credit.",
    "Only MSME exporters are eligible under the Credit Guarantee Scheme for Exporters."],
   [True, True, False],
   "EPM and CGSE",
   "The Export Promotion Mission runs for six years from 2025-26. Under the ₹20,000 crore CGSE, the National Credit "
   "Guarantee Trustee Company gives member lending institutions 100% cover on additional credit to exporters; both "
   "MSME and non-MSME exporters are eligible.",
   [fact("EPM approved for six years, FY 2025-26 to 2030-31", "epm_mp"),
    fact("CGSE: NCGTC provides 100% cover; MSME and non-MSME exporters eligible", "epm_angel")],
   why="Statement 3 is wrong: non-MSME exporters are also eligible.",
   current=ca("2025-11-12"))

# ====================================================================== Important Appointments (2 / 10 / 1)
T = "Important Appointments"
BNK, INTL = "Banking and finance heads", "International bodies"

G(T, BNK, "Basic",
  "Who was sworn in as Chair of the US Federal Reserve on 22 May 2026, succeeding Jerome Powell?",
  ["Kevin Warsh", "Kevin Hassett", "Christopher Waller", "Michelle Bowman"], "*",
  "US Federal Reserve Chair",
  "Kevin Warsh was sworn in as the 17th Fed Chair at the White House on 22 May 2026; Justice Clarence Thomas "
  "administered the oath. He took over from Jerome Powell, who stayed on the Board of Governors.",
  ["Sworn in: 22 May 2026", "17th Fed Chair: Kevin Warsh", "Predecessor: Jerome Powell"],
  [fact("Kevin Warsh sworn in as Federal Reserve chair on 22 May 2026, replacing Powell", "warsh_cbs")],
  why="Kevin Hassett is a White House economic adviser; Waller and Bowman are Fed governors, not the new chair.",
  current=ca("2026-05-22"))

G(T, INTL, "Basic",
  "Daren Tang of Singapore was appointed in April 2026 to a second six-year term as Director General of which UN "
  "agency?",
  ["World Intellectual Property Organization (WIPO)", "World Trade Organization (WTO)",
   "International Telecommunication Union (ITU)", "UNCTAD"], "*",
  "WIPO Director General",
  "WIPO's member states appointed Daren Tang on 21 April 2026 to a second term running from 1 October 2026 to "
  "30 September 2032, after the Coordination Committee nominated him in February.",
  ["Appointed: 21 April 2026", "Term: 1 Oct 2026 - 30 Sep 2032", "Body: WIPO, Geneva"],
  [fact("WIPO member states appointed Daren Tang on 21 Apr 2026 to a second term, 1 Oct 2026 - 30 Sep 2032",
        "wipo_pr")],
  why="The WTO is headed by Ngozi Okonjo-Iweala; ITU and UNCTAD have other heads.",
  current=ca("2026-04-21"))

G(T, BNK, "Intermediate",
  "Boris Vujčić, who became Vice-President of the European Central Bank on 1 June 2026, was earlier Governor of which "
  "country's central bank?",
  ["Croatia", "Slovenia", "Bulgaria", "Spain"], "*",
  "ECB Vice-President",
  "The Governor of Hrvatska narodna banka (Croatian National Bank), Boris Vujčić, was appointed ECB Vice-President for "
  "a non-renewable eight-year term from 1 June 2026, succeeding Spain's Luis de Guindos, whose term ended on 31 May "
  "2026.",
  ["Term: 8 years, non-renewable, from 1 June 2026", "Predecessor: Luis de Guindos (Spain)"],
  [fact("ECB opinion: Vujčić, Governor of Hrvatska narodna banka, to serve 8-year term from 1 June 2026, succeeding "
        "de Guindos", "ecb_pr"),
   fact("European Council appoints Boris Vujčić as ECB Vice-President", "ecb_mondo")],
  why="De Guindos, whom he succeeded, is from Spain; Slovenia and Bulgaria are other euro members.",
  current=ca("2026-06-01"))

G(T, INTL, "Intermediate",
  "The UN General Assembly confirmed former Belgian Prime Minister Alexander De Croo in November 2025 as head of which "
  "body?",
  ["UN Development Programme (UNDP)", "UNICEF", "UN Environment Programme (UNEP)", "UN Population Fund (UNFPA)"], "*",
  "UNDP Administrator",
  "On 17 November 2025 the General Assembly confirmed Alexander De Croo as UNDP Administrator for a four-year term, "
  "on the Secretary-General's nomination. Associate Administrator Haoliang Xu acted until he took office.",
  ["Confirmed: 17 Nov 2025", "Post: UNDP Administrator (4 years)"],
  [fact("General Assembly confirms Alexander De Croo as UNDP Administrator", "undp_un"),
   fact("Ex-Belgian PM appointed as new UNDP administrator", "undp_star")],
  why="UNICEF, UNEP and UNFPA have other heads.",
  current=ca("2025-11-17"))

G(T, INTL, "Intermediate",
  "Lucas Philippe, elected President of INTERPOL at its 93rd General Assembly in Marrakech on 27 November 2025, is "
  "from which country?",
  ["France", "United Arab Emirates", "Morocco", "China"], "*",
  "INTERPOL President",
  "Lucas Philippe of France won 84 votes at the General Assembly held in Marrakech from 24 to 27 November 2025 and was "
  "elected for four years, succeeding Ahmed Naser Al-Raisi of the UAE. Wang Yong of China was elected a "
  "Vice-President for Asia.",
  ["Elected: 27 Nov 2025, Marrakech", "Term: 4 years", "Predecessor: Ahmed Naser Al-Raisi (UAE)"],
  [fact("INTERPOL elects France's Lucas Philippe as new president", "interpol_print"),
   fact("INTERPOL's 93rd General Assembly closes in Marrakech", "interpol_mwn")],
  why="The UAE was the predecessor's country, Morocco the host and China a Vice-President's country.",
  current=ca("2025-11-27"))

G(T, BNK, "Intermediate",
  "In February 2026 the RBI approved Vinay Muralidhar Tonse, a former Managing Director of SBI, as MD and CEO of which "
  "bank?",
  ["Yes Bank", "IDBI Bank", "RBL Bank", "Federal Bank"], "*",
  "Yes Bank leadership",
  "By a letter dated 3 February 2026 the RBI approved Tonse's appointment as MD and CEO of Yes Bank for three years "
  "from the date he takes charge, succeeding Prashant Kumar. Tonse was SBI's MD for Retail Business and Operations "
  "until 30 November 2025.",
  ["RBI approval: 3 Feb 2026", "Term: 3 years", "Predecessor: Prashant Kumar"],
  [fact("RBI approved new Yes Bank MD & CEO by letter dated 3 Feb 2026", "yes_bt"),
   fact("RBI approves former SBI MD Vinay Tonse as Yes Bank MD & CEO", "yes_ob")],
  why="He was not appointed to IDBI, RBL or Federal Bank.",
  current=ca("2026-02-03"))

G(T, BNK, "Intermediate",
  "In May 2026 the RBI approved the re-appointment of Sandeep Bakhshi as MD and CEO of ICICI Bank. For how long does "
  "the re-appointment run from 4 October 2026?",
  ["Two years", "Three years", "Five years", "One year"], "*",
  "ICICI Bank leadership",
  "The RBI's letter of 22 May 2026 approved Bakhshi's re-appointment for two years from 4 October 2026, i.e. till "
  "2028. His previous three-year term ran till 3 October 2026.",
  ["RBI letter: 22 May 2026", "New term: 2 years from 4 Oct 2026", "Previous term: 3 years, to 3 Oct 2026"],
  [fact("RBI clears Sandeep Bakhshi's re-appointment as ICICI Bank CEO for two years, till 2028", "icici_bt")],
  why="Three years was his previous term; five and one year are wrong.",
  current=ca("2026-05-22"))

G(T, BNK, "Intermediate",
  "Who was appointed a Managing Director of Life Insurance Corporation of India with effect from 1 December 2025?",
  ["Ramakrishnan Chander", "R. Doraiswamy", "Siddhartha Mohanty", "Ajay Seth"], "*",
  "LIC leadership",
  "The Centre named Ramakrishnan Chander, LIC's investment chief, as Managing Director from 1 December 2025, until his "
  "superannuation on 30 September 2027. R. Doraiswamy has been LIC's MD and CEO since July 2025.",
  ["New MD: Ramakrishnan Chander (from 1 Dec 2025)", "MD & CEO: R. Doraiswamy"],
  [fact("Centre names LIC investment chief Ramakrishnan Chander as MD", "lic_pm"),
   fact("LIC appoints Ramakrishnan Chander as Managing Director", "lic_reinasia")],
  why="Doraiswamy is MD & CEO (appointed earlier); Mohanty is a former chairman; Ajay Seth heads IRDAI.",
  current=ca("2025-12-01"))

G(T, BNK, "Intermediate",
  "Dinesh Pant, a Managing Director of LIC, was appointed in June 2026 to which post?",
  ["Whole-Time Member (Actuary), IRDAI", "Chairperson, PFRDA", "Chairperson, IRDAI", "Deputy Governor, RBI"], "*",
  "IRDAI membership",
  "LIC informed the exchanges on 16 June 2026 that its MD Dinesh Pant had been appointed Whole-Time Member (Actuary) of "
  "the Insurance Regulatory and Development Authority of India. IRDAI is chaired by Ajay Seth and PFRDA by "
  "S. Ramann.",
  ["Appointment disclosed: 16 June 2026", "Post: IRDAI Whole-Time Member (Actuary)"],
  [fact("LIC MD Dinesh Pant appointed Whole-Time Member (Actuary) at IRDAI", "pant_psu")],
  why="He did not become chair of IRDAI or PFRDA or an RBI Deputy Governor.",
  current=ca("2026-06-16"))

G(T, BNK, "Intermediate",
  "Sanjay Lohiya assumed charge on 1 June 2026 as Secretary of which department of the Finance Ministry?",
  ["Department of Financial Services", "Department of Economic Affairs", "Department of Revenue",
   "Department of Investment and Public Asset Management"], "*",
  "Finance Ministry secretaries",
  "Sanjay Lohiya, a 1994-batch IAS officer of the Assam-Meghalaya cadre, became Secretary, Department of Financial "
  "Services on 1 June 2026. He had been Special Secretary in DFS earlier in the year. DFS looks after public sector "
  "banks, insurers and financial inclusion schemes.",
  ["Post: Secretary, DFS", "Took charge: 1 June 2026"],
  [fact("Sanjay Lohiya assumed charge as Secretary, Department of Financial Services on 1 June 2026", "dfs_wi"),
   fact("Profile: IAS Sanjay Lohiya, Secretary, Department of Financial Services", "dfs_im")],
  why="He did not take charge of DEA, Revenue or DIPAM.",
  current=ca("2026-06-01"))

G(T, BNK, "Intermediate",
  "Gunveer Singh, promoted as an Executive Director of the RBI in May 2026, heads which department?",
  ["Department of Payment and Settlement Systems", "Department of Currency Management", "Foreign Exchange Department",
   "Department of Statistics and Information Management"], "*",
  "RBI Executive Directors",
  "On 18 May 2026 the RBI promoted Gunveer Singh, Chief General Manager-in-Charge of the Department of Payment and "
  "Settlement Systems, as Executive Director; he continues to head that department. In later 2026 releases Ravi "
  "Shankar was made ED for Statistics and Information Management and Monisha Chakraborty for the Foreign Exchange "
  "Department.",
  ["Promoted: 18 May 2026", "Department: Payment and Settlement Systems"],
  [fact("RBI appoints Gunveer Singh as new Executive Director for payment systems", "gunveer_an"),
   fact("RBI promotes Gunveer Singh as Executive Director", "gunveer_lm")],
  why="The other departments are looked after by other EDs.",
  current=ca("2026-05-18"))

G(T, BNK, "Intermediate",
  "Suman Ray, appointed an Executive Director of the RBI from 1 September 2026, oversees the Premises Department and "
  "which entity?",
  ["Deposit Insurance and Credit Guarantee Corporation (DICGC)", "National Payments Corporation of India (NPCI)",
   "NABARD", "Bharatiya Reserve Bank Note Mudran"], "*",
  "RBI Executive Directors",
  "Suman Ray, earlier the RBI's Regional Director for Maharashtra, was elevated as Executive Director from 1 September "
  "2026 and looks after the DICGC and the Premises Department. The DICGC insures bank deposits up to ₹5 lakh per "
  "depositor per bank.",
  ["Appointed ED: 1 Sep 2026", "Portfolio: DICGC and Premises Department"],
  [fact("RBI appoints Suman Ray as Executive Director with effect from 1 September", "ray_ll"),
   fact("RBI appoints Suman Ray as new Executive Director", "ray_nk")],
  why="NPCI and NABARD are separate institutions; BRBNML is the note-printing subsidiary, not his charge.",
  current=ca("2026-09-01"))

GS(T, BNK, "Advanced", "the leadership change at Kotak Mahindra Bank",
   ["The RBI approved Anup Kumar Saha as MD and CEO under Section 35B of the Banking Regulation Act, 1949, by an "
    "approval dated 30 September 2026.",
    "His three-year term is to begin on 1 January 2027.",
    "He succeeds Uday Kotak as MD and CEO."],
   [True, True, False],
   "Kotak Mahindra Bank MD and CEO",
   "Kotak's filing of 1 October 2026 said the RBI approved Saha for three years from 1 January 2027. He succeeds Ashok "
   "Vaswani, who chose not to seek re-appointment when his term ends on 31 December 2026. Kotak had also recommended "
   "Paritosh Kashyap to the RBI.",
   [fact("Kotak Mahindra Bank shares in focus on RBI nod for Anup Kumar Saha as MD & CEO", "kotak_bt"),
    fact("RBI approves Anup Kumar Saha's 3-year term as Kotak MD & CEO", "kotak_ml")],
   why="Statement 3 is wrong: he succeeds Ashok Vaswani.",
   current=ca("2026-09-30"))

# ====================================================================== Awards and Honours (6 / 1 / 8)
T = "Awards and Honours"
NAT, INT_A = "National awards", "International awards"

G(T, INT_A, "Basic",
  "Francis Halzen won the 2026 Nobel Prize in Physics for decisive contributions to which observatory?",
  ["IceCube Neutrino Observatory", "LIGO gravitational-wave observatory", "James Webb Space Telescope",
   "Event Horizon Telescope"], "*",
  "Nobel Prize in Physics 2026",
  "On 6 October 2026 the Royal Swedish Academy of Sciences gave the full physics prize to Belgian-American physicist "
  "Francis Halzen for decisive contributions to the IceCube Neutrino Observatory and the discovery of high-energy "
  "neutrinos of astrophysical origin.",
  ["Announced: 6 Oct 2026", "Laureate: Francis Halzen (sole)", "Work: IceCube, astrophysical neutrinos"],
  [fact("Francis Halzen wins 2026 Nobel Prize in Physics for IceCube contributions (6 Oct 2026)", "phys_print"),
   fact("Francis Halzen wins 2026 Nobel Prize in Physics", "phys_dm")],
  why="The other facilities were not the basis of the 2026 prize.",
  current=ca("2026-10-06"))

G(T, INT_A, "Basic",
  "Henri Kagan and Kenso Soai shared the 2026 Nobel Prize in Chemistry for discoveries in which area?",
  ["Non-linear effects and autocatalysis in asymmetric organic synthesis", "Metal-organic frameworks",
   "Click chemistry and bioorthogonal chemistry", "Computational protein design"], "*",
  "Nobel Prize in Chemistry 2026",
  "The 2026 chemistry prize, announced on 7 October 2026, went to Henri Kagan and Kenso Soai 'for the discovery of "
  "non-linear effects and autocatalysis in asymmetric organic synthesis'.",
  ["Announced: 7 Oct 2026", "Laureates: Henri Kagan, Kenso Soai"],
  [fact("Henri Kagan and Kenso Soai win 2026 Nobel chemistry prize for non-linear effects and autocatalysis in "
        "asymmetric organic synthesis", "chem_kt")],
  why="The other fields were honoured in earlier years, not in 2026.",
  current=ca("2026-10-07"))

G(T, INT_A, "Basic",
  "Karl Deisseroth, Peter Hegemann and Georg Nagel won the 2026 Nobel Prize in Physiology or Medicine for discoveries "
  "concerning what?",
  ["Light-gated ion channels and optogenetics", "MicroRNA and gene regulation", "Peripheral immune tolerance",
   "Nucleoside modifications enabling mRNA vaccines"], "*",
  "Nobel Prize in Medicine 2026",
  "On 5 October 2026 the prize was awarded jointly to the three for discoveries concerning light-gated ion channels and "
  "optogenetics, a technique that switches individual nerve cells on or off with light to study brain function.",
  ["Announced: 5 Oct 2026", "Work: light-gated ion channels, optogenetics"],
  [fact("Nobel medicine prize 2026 goes to three scientists for research into brain activity", "med_gpb"),
   fact("Nobel Prize in Physiology or Medicine 2026: Deisseroth, Hegemann, Nagel, for light-gated ion channels and "
        "optogenetics", "med_nobel")],
  why="The other topics were honoured in earlier years.",
  current=ca("2026-10-05"))

G(T, INT_A, "Basic",
  "Which film won Best Picture at the 98th Academy Awards held on 15 March 2026?",
  ["One Battle After Another", "Sinners", "Hamnet", "Frankenstein"], "*",
  "Oscars 2026",
  "Paul Thomas Anderson's One Battle After Another won Best Picture and five other awards, including Best Director. "
  "Michael B. Jordan won Best Actor for Sinners and Jessie Buckley Best Actress for Hamnet.",
  ["Ceremony: 15 Mar 2026, Dolby Theatre", "Best Picture: One Battle After Another"],
  [fact("One Battle After Another wins Best Picture at the 98th Academy Awards", "oscar_abc"),
   fact("One Battle After Another wins best picture, 15 Mar 2026", "oscar_mb")],
  why="Sinners, Hamnet and Frankenstein won other awards but not Best Picture.",
  current=ca("2026-03-15"))

G(T, NAT, "Basic",
  "The 60th Jnanpith Award (for 2025), announced in March 2026, went to which writer?",
  ["R. Vairamuthu", "Vinod Kumar Shukla", "Gulzar", "Jayakanthan"], "*",
  "Jnanpith Award",
  "The selection board chaired by Pratibha Ray named Tamil poet and lyricist R. Vairamuthu for the 60th Jnanpith "
  "Award on 14 March 2026. He is the third Tamil writer to win it, after Akilan (1975) and Jayakanthan (2002). The "
  "59th award went to Vinod Kumar Shukla and the 58th to Gulzar and Jagadguru Rambhadracharya.",
  ["60th Jnanpith (2025): R. Vairamuthu", "59th: Vinod Kumar Shukla", "58th: Gulzar, Rambhadracharya"],
  [fact("Tamil poet-lyricist Vairamuthu named 2025 Jnanpith Award winner (14 Mar 2026)", "jnan_omm"),
   fact("R. Vairamuthu conferred 60th Jnanpith Award", "jnan_drishti")],
  why="Shukla and Gulzar won the previous two awards; Jayakanthan won in 2002.",
  current=ca("2026-03-14"))

G(T, NAT, "Basic",
  "Former diplomat Navtej Sarna won the Sahitya Akademi Award 2025 in English for which novel?",
  ["Crimson Spring", "Jeete Jee Allahabad", "Flesh", "Taiwan Travelogue"], "*",
  "Sahitya Akademi Award 2025",
  "The Akademi announced its 2025 awards in 24 languages on 16 March 2026. The English award went to Navtej Sarna's "
  "Crimson Spring, a novel set around the 1919 Jallianwala Bagh massacre; the Hindi award went to Mamta Kalia's memoir "
  "Jeete Jee Allahabad.",
  ["Announced: 16 Mar 2026", "English: Crimson Spring (Navtej Sarna)", "Hindi: Jeete Jee Allahabad (Mamta Kalia)"],
  [fact("Veteran diplomat Navtej Sarna wins Sahitya Akademi Award for Crimson Spring", "sa_statesman"),
   fact("Sahitya Akademi Awards: 24 writers honoured including Mamta Kalia and Navtej Sarna", "sa_print")],
  why="Jeete Jee Allahabad won in Hindi; Flesh and Taiwan Travelogue are international prize winners.",
  current=ca("2026-03-16"))

G(T, INT_A, "Intermediate",
  "Whom did TIME magazine name as its Person of the Year for 2025?",
  ["The Architects of AI", "Donald Trump", "Pope Leo XIV", "Zohran Mamdani"], "*",
  "TIME Person of the Year 2025",
  "On 11 December 2025 TIME named 'the Architects of AI', a group of technology leaders including OpenAI's Sam Altman "
  "and Meta's Mark Zuckerberg, as its 2025 Person of the Year. Donald Trump was the 2024 choice.",
  ["Announced: 11 Dec 2025", "Choice: the Architects of AI (a group)", "2024: Donald Trump"],
  [fact("TIME Person of the Year 2025 announced: the architects of AI", "time_euronews"),
   fact("The architects of AI are TIME's 2025 Person of the Year", "time_cbs")],
  why="Trump was the 2024 Person of the Year; the others were not chosen.",
  current=ca("2025-12-11"))

GS(T, NAT, "Advanced", "the National Sports Awards 2025 announced in August 2026",
   ["No sportsperson was selected for the Major Dhyan Chand Khel Ratna Award 2025.",
    "Before this, the last year without a Khel Ratna awardee was 2014."],
   [True, True],
   "National Sports Awards 2025",
   "The Sports Ministry announced the 2025 awards on 18 August 2026 without any Khel Ratna recipient; 17 sportspersons "
   "were selected for the Arjuna Award. The last year without a Khel Ratna was 2014.",
   [fact("No Khel Ratna for 2025; Arjuna Awards announced", "kr_nb"),
    fact("National Sports Awards 2025 list: no Khel Ratna, first such year since 2014", "kr_open")],
   why="Both statements are correct.",
   current=ca("2026-08-18"))

GS(T, INT_A, "Advanced", "the Abel Prize 2026",
   ["It was awarded to Gerd Faltings, the first German mathematician to win it.",
    "Faltings is the first mathematician to have won both the Fields Medal and the Abel Prize."],
   [True, False],
   "Abel Prize 2026",
   "The Norwegian Academy of Science and Letters gave the 2026 Abel Prize to Gerd Faltings of the Max Planck Institute "
   "for Mathematics, Bonn, for his work in arithmetic geometry, including the proof of the Mordell conjecture. He won "
   "the Fields Medal in 1986, but earlier Abel laureates such as Jean-Pierre Serre had also won both prizes.",
   [fact("Gerd Faltings awarded the 2026 Abel Prize", "abel_ems"),
    fact("Faltings: first German Abel laureate; Fields Medal 1986", "abel_lms")],
   why="Statement 2 is wrong: others had won both prizes before him.",
   current=ca("2026-03-19"))

GS(T, INT_A, "Advanced", "the Pritzker Architecture Prize 2026",
   ["It was awarded to Chilean architect Smiljan Radić Clarke.",
    "He is the 55th laureate of the prize.",
    "The jury was chaired by Chilean Pritzker laureate Alejandro Aravena."],
   [True, True, True],
   "Pritzker Prize 2026",
   "The Hyatt Foundation announced on 12 March 2026 that Smiljan Radić Clarke of Santiago, Chile, is the 55th Pritzker "
   "laureate. The jury was chaired by Alejandro Aravena, the 2016 laureate.",
   [fact("Chilean Smiljan Radić Clarke wins 2026 Pritzker Architecture Prize (12 Mar 2026)", "pritz_euronews"),
    fact("Smiljan Radić Clarke named 55th Pritzker laureate; jury chaired by Alejandro Aravena", "pritz_wallpaper")],
   why="All three statements are correct.",
   current=ca("2026-03-12"))

GS(T, INT_A, "Advanced", "the honour conferred on Prime Minister Modi in Ethiopia",
   ["He received the 'Great Honour Nishan of Ethiopia' in Addis Ababa on 16 December 2025.",
    "He is the first global head of state or government to receive this honour."],
   [True, True],
   "Great Honour Nishan of Ethiopia",
   "Ethiopian Prime Minister Abiy Ahmed Ali conferred Ethiopia's highest honour on PM Modi at the Addis International "
   "Convention Centre on 16 December 2025, during his first bilateral visit. Indian reports counted it as his 28th "
   "international honour.",
   [fact("PM Modi conferred Ethiopia's highest honour, first world leader to receive it", "eth_print"),
    fact("Prime Minister conferred the Great Honour Nishan of Ethiopia", "eth_air")],
   why="Both statements are correct.",
   current=ca("2025-12-16"))

GS(T, NAT, "Advanced", "the Padma Awards 2026",
   ["Former Supreme Court judge K. T. Thomas was among the Padma Vibhushan awardees.",
    "Five Padma Vibhushan awards were announced.",
    "A total of 113 Padma awards were announced."],
   [True, True, False],
   "Padma Awards 2026",
   "The awards announced on 25 January 2026 comprised 5 Padma Vibhushan, 13 Padma Bhushan and 113 Padma Shri, 131 in "
   "all, with 16 posthumous. K. T. Thomas was one of the Padma Vibhushan recipients. 113 is the Padma Shri count, not "
   "the total.",
   [fact("Padma Awards 2026: 5 Padma Vibhushan, 13 Padma Bhushan, 113 Padma Shri", "padma_gulf"),
    fact("Full list of 2026 Padma award winners including K. T. Thomas", "padma_dh")],
   why="Statement 3 is wrong: 131 awards were announced; 113 were Padma Shri.",
   current=ca("2026-01-25"))

GS(T, INT_A, "Advanced", "the Ramon Magsaysay Award 2026",
   ["One of the three awardees is from India.",
    "Singaporean diplomat and academic Tommy Koh is among the awardees.",
    "Myanmar human rights activist Bo Kyi is among the awardees."],
   [False, True, True],
   "Ramon Magsaysay Award 2026",
   "The foundation named three awardees on 31 August 2026: Tommy Koh (Singapore), social entrepreneur Runa Khan "
   "(Bangladesh) and Bo Kyi (Myanmar). None is Indian. The awards are presented in Manila.",
   [fact("Three transformative leaders named 2026 Ramon Magsaysay awardees (31 Aug 2026)", "mag_mb"),
    fact("2026 Magsaysay Award recipients from Singapore, Bangladesh and Myanmar", "mag_gma")],
   why="Statement 1 is wrong: the awardees are from Singapore, Bangladesh and Myanmar.",
   current=ca("2026-08-31"))

GS(T, INT_A, "Advanced", "the 68th Grammy Awards held on 1 February 2026",
   ["Bad Bunny's 'Debí Tirar Más Fotos' won Album of the Year.",
    "It was the first Spanish-language album to win Album of the Year."],
   [True, True],
   "Grammy Awards 2026",
   "At the ceremony at Crypto.com Arena, Los Angeles, on 1 February 2026, Bad Bunny's Debí Tirar Más Fotos won Album "
   "of the Year, the first Spanish-language album to take the top prize.",
   [fact("Bad Bunny makes Grammys history with Album of the Year win", "grammy_arab"),
    fact("Grammys 2026 full winners list: Bad Bunny wins Album of the Year", "grammy_ol")],
   why="Both statements are correct.",
   current=ca("2026-02-01"))

GS(T, INT_A, "Advanced", "the World Food Prize 2026",
   ["Dutch scientist Huub Lelieveld was named the 2026 laureate.",
    "The prize carries a cash award of USD 1 million."],
   [True, False],
   "World Food Prize 2026",
   "The World Food Prize Foundation announced on 25 March 2026 that Huub Lelieveld, founder of the Global "
   "Harmonization Initiative for food safety, is the 2026 laureate. The prize carries USD 500,000 and was presented in "
   "Des Moines, Iowa, in October.",
   [fact("World Food Prize 2026 laureate Huub Lelieveld", "wfp_drishti"),
    fact("2026 laureate announcement ceremony; prize of USD 500,000", "wfp_site")],
   why="Statement 2 is wrong: the prize is USD 500,000.",
   current=ca("2026-03-25"))

# ====================================================================== Sports (4 / 1 / 0)
T = "Sports"
TW, VR = "Tournaments and winners", "Venues and records"

G(T, TW, "Basic",
  "Who won the men's singles title at the Australian Open 2026, beating Novak Djokovic in the final?",
  ["Carlos Alcaraz", "Jannik Sinner", "Alexander Zverev", "Daniil Medvedev"], "*",
  "Australian Open 2026",
  "Carlos Alcaraz beat Novak Djokovic 2-6, 6-2, 6-3, 7-5 for his first Australian Open title. Elena Rybakina won the "
  "women's singles, beating Aryna Sabalenka. Defending champion Jannik Sinner lost in the semi-finals.",
  ["Men: Carlos Alcaraz bt Djokovic", "Women: Elena Rybakina bt Sabalenka"],
  [fact("Alcaraz won the 2026 Australian Open men's title, beating Djokovic", "ao_espn"),
   fact("2026 Australian Open results", "ao_wiki")],
  why="Sinner lost in the semi-finals; Zverev and Medvedev did not win.",
  current=ca("2026-02-01"))

G(T, TW, "Basic",
  "Who won the men's singles title at Wimbledon 2026?",
  ["Jannik Sinner", "Carlos Alcaraz", "Alexander Zverev", "Novak Djokovic"], "*",
  "Wimbledon 2026",
  "Jannik Sinner retained his Wimbledon title on 12 July 2026, beating Alexander Zverev 6-7(7), 7-6(2), 6-3, 6-4 in "
  "Zverev's first Wimbledon final. Sinner beat Djokovic in the semi-final.",
  ["Final: 12 July 2026", "Winner: Jannik Sinner", "Runner-up: Alexander Zverev"],
  [fact("Jannik Sinner wins Wimbledon 2026 men's singles title", "wim_drishti"),
   fact("Wimbledon 2026 winners list", "wim_ahram")],
  why="Zverev was the runner-up; Djokovic lost in the semi-final; Alcaraz did not win.",
  current=ca("2026-07-12"))

G(T, VR, "Basic",
  "Which country topped the medal table at the Milano Cortina 2026 Winter Olympics?",
  ["Norway", "United States", "Italy", "Germany"], "*",
  "Winter Olympics 2026",
  "Norway finished first with 18 gold medals and about 41 medals in all, its fourth straight Winter Games at the top. "
  "The United States were second on golds (12); host Italy had its best Winter Games with 10 golds and 30 medals.",
  ["1st: Norway (18 gold)", "2nd: USA (12 gold)", "Host Italy: 10 gold"],
  [fact("Milano Cortina 2026 final medal tally: Norway on top", "wo_outlook"),
   fact("Final medal table of the 2026 Winter Olympics: Norway, USA, Netherlands", "wo_fj")],
  why="The USA was second; Italy and Germany finished lower.",
  current=ca("2026-02-22"))

G(T, VR, "Basic",
  "At the Glasgow 2026 Commonwealth Games, India finished fourth on the medal table. How many medals did India win?",
  ["39", "61", "22", "13"], "*",
  "Commonwealth Games 2026",
  "India won 39 medals (13 gold, 17 silver, 9 bronze) at Glasgow, finishing fourth behind Australia, England and "
  "Canada. Boxing gave 10 medals including 7 golds. The Games ended on 2 August 2026; Ahmedabad hosts in 2030.",
  ["Total: 39 (13 G, 17 S, 9 B)", "Position: 4th"],
  [fact("Commonwealth Games 2026: India total rises to 39, fourth on the table", "cwg_fpj"),
   fact("India wins 39 medals, finishes fourth", "cwg_brut")],
  why="13 is India's gold count; 61 and 22 are not the 2026 figures.",
  current=ca("2026-08-02"))

G(T, TW, "Intermediate",
  "Who became the first Indian to win the FIDE Women's Candidates Tournament, held in Cyprus in March-April 2026?",
  ["R. Vaishali", "Koneru Humpy", "Divya Deshmukh", "Harika Dronavalli"], "*",
  "FIDE Candidates 2026",
  "The Candidates tournaments ran from 28 March to 16 April 2026 at Peyia, Paphos, Cyprus. R. Vaishali won the "
  "women's event, the first Indian to do so, qualifying for the Women's World Championship match. Javokhir Sindarov "
  "won the open event and earned a match against world champion D. Gukesh.",
  ["Women's Candidates: R. Vaishali", "Open Candidates: Javokhir Sindarov", "Venue: Cyprus"],
  [fact("Sindarov and Vaishali win FIDE Candidates 2026", "cand_chess"),
   fact("Closing ceremony of the 2026 Candidates tournaments in Cyprus", "cand_cb")],
  why="The other Indian players did not win the 2026 Women's Candidates.",
  current=ca("2026-04-16"))

# ====================================================================== Summits and Conferences (0 / 9 / 0)
T = "Summits and Conferences"
GRP, HOST = "G20, BRICS, SCO and others", "Hosting countries"

G(T, HOST, "Intermediate",
  "Under the arrangement agreed at COP30 in November 2025, COP31 will be held in Antalya, Türkiye. Which country will "
  "lead the negotiations as 'President of Negotiations'?",
  ["Australia", "Brazil", "Türkiye", "Fiji"], "*",
  "COP31 arrangement",
  "Australia and Türkiye had both bid for COP31. Under the deal reached at COP30 in Belém, Türkiye hosts COP31 in "
  "Antalya and holds the presidency, while Australia's representative chairs the negotiations; a pre-COP is to be held "
  "in a Pacific country.",
  ["Host and presidency: Türkiye (Antalya)", "Negotiations: Australia", "Pre-COP: a Pacific country"],
  [fact("COP31 will be hosted by Türkiye but negotiations run by Australia", "cop31_ccn"),
   fact("COP to be hosted by Türkiye with Australia leading negotiations", "cop31_wong")],
  why="Brazil hosted COP30; Türkiye hosts and presides; Fiji is not the negotiations chair.",
  current=ca("2025-11-20"))

G(T, HOST, "Intermediate",
  "The WTO's 14th Ministerial Conference (MC14) was held in March 2026 in which city?",
  ["Yaoundé", "Abu Dhabi", "Nairobi", "Geneva"], "*",
  "WTO MC14",
  "MC14 met in Yaoundé, Cameroon, in late March 2026 and closed on 30 March. The moratorium on customs duties on "
  "electronic transmissions lapsed for the first time since 1998, and most major issues were sent back to Geneva. MC13 "
  "had been held in Abu Dhabi in 2024.",
  ["MC14: Yaoundé, Cameroon (March 2026)", "MC13: Abu Dhabi (2024)"],
  [fact("MC14 in Yaoundé: what the WTO delivered and what it did not", "mc14_wef"),
   fact("WTO MC14 key outcomes; e-commerce moratorium lapsed", "mc14_dte")],
  why="Abu Dhabi hosted MC13; Nairobi and Geneva did not host MC14.",
  current=ca("2026-03-30"))

G(T, GRP, "Intermediate",
  "What was the theme of the World Economic Forum's 56th Annual Meeting held in Davos from 19 to 23 January 2026?",
  ["A Spirit of Dialogue", "Collaboration for the Intelligent Age", "Rebuilding Trust",
   "Cooperation in a Fragmented World"], "*",
  "WEF Annual Meeting 2026",
  "The 56th Annual Meeting in Davos-Klosters (19-23 January 2026) had the theme 'A Spirit of Dialogue' and drew nearly "
  "3,000 leaders from over 130 countries, including a record number of heads of state and government.",
  ["Dates: 19-23 Jan 2026", "Theme: A Spirit of Dialogue"],
  [fact("WEF Annual Meeting 2026: A Spirit of Dialogue", "wef_pr"),
   fact("Davos 2026: 3,000 leaders from 130 countries at WEF's 56th Annual Meeting, 19-23 Jan", "wef_bt")],
  why="The other phrases were themes of earlier Davos meetings.",
  current=ca("2026-01-19"))

G(T, HOST, "Intermediate",
  "The 2026 Annual Meetings of the IMF and the World Bank Group, held from 12 to 18 October 2026, took place in which "
  "city?",
  ["Bangkok", "Washington, D.C.", "Marrakech", "Jakarta"], "*",
  "IMF-World Bank Annual Meetings 2026",
  "Every third year the Annual Meetings are held outside Washington. The 2026 meetings were held at the Queen Sirikit "
  "National Convention Center, Bangkok, the first in the city since 1991. The 2023 meetings were in Marrakech.",
  ["Dates: 12-18 Oct 2026", "Venue: Bangkok, Thailand"],
  [fact("2026 Annual Meetings of the IMF and World Bank Group in Bangkok, 12-18 October", "imfwb_imf"),
   fact("15,000 delegates expected as Thailand hosts IMF-World Bank Annual Meetings 2026", "imfwb_pm")],
  why="Washington hosts the other years; Marrakech hosted in 2023; Jakarta did not host.",
  current=ca("2026-10-12"))

G(T, GRP, "Intermediate",
  "The 48th ASEAN Summit, held in Cebu in May 2026, was hosted by which country as ASEAN chair for 2026?",
  ["Philippines", "Malaysia", "Singapore", "Vietnam"], "*",
  "ASEAN Summit 2026",
  "The Philippines chairs ASEAN in 2026 under the theme 'Navigating Our Future, Together' and hosted the 48th Summit "
  "at Lapu-Lapu City, Cebu, on 6-8 May 2026. A 49th summit was planned for later in 2026.",
  ["Chair 2026: Philippines", "48th Summit: Cebu, May 2026"],
  [fact("All systems go for 48th ASEAN Summit in Cebu", "asean_ptv"),
   fact("ASEAN eyes first Charter amendment at Cebu summit", "asean_star")],
  why="Malaysia chaired ASEAN in 2025; Singapore and Vietnam were not the 2026 chair.",
  current=ca("2026-05-08"))

G(T, HOST, "Intermediate",
  "The Second World Summit for Social Development, which adopted the Doha Political Declaration on 4 November 2025, "
  "was held in which country?",
  ["Qatar", "Denmark", "United Arab Emirates", "Egypt"], "*",
  "World Social Summit 2025",
  "The summit was held in Doha, Qatar, from 4 to 6 November 2025, thirty years after the first summit in Copenhagen "
  "(1995). Leaders adopted the Doha Political Declaration on its first day; it rests on poverty eradication, decent "
  "work and social integration.",
  ["Venue: Doha, Qatar (4-6 Nov 2025)", "First summit: Copenhagen, 1995"],
  [fact("Second World Summit for Social Development in Doha, 4-6 Nov 2025; Doha Political Declaration adopted 4 Nov",
        "doha_un"),
   fact("World leaders adopt Doha declaration at the social summit", "doha_unnews")],
  why="Denmark (Copenhagen) hosted the first summit in 1995; the UAE and Egypt did not host.",
  current=ca("2025-11-04"))

G(T, GRP, "Intermediate",
  "Who was the chief guest at the 11th Raisina Dialogue, inaugurated by the Prime Minister in New Delhi on 5 March "
  "2026?",
  ["Alexander Stubb, President of Finland", "Christopher Luxon, Prime Minister of New Zealand",
   "Giorgia Meloni, Prime Minister of Italy", "Ursula von der Leyen, President of the European Commission"], "*",
  "Raisina Dialogue 2026",
  "Finnish President Alexander Stubb was chief guest and gave the inaugural keynote at the 11th Raisina Dialogue "
  "(5-7 March 2026). New Zealand's PM Christopher Luxon was chief guest in 2025 and Italy's Giorgia Meloni in 2023.",
  ["Edition: 11th (5-7 Mar 2026)", "Chief guest: Alexander Stubb (Finland)"],
  [fact("PM Modi to inaugurate Raisina Dialogue 2026; Finnish President Stubb chief guest", "raisina_tribune"),
   fact("PM to inaugurate Raisina Dialogue 2026 in New Delhi on 5 March", "raisina_air")],
  why="Luxon (2025) and Meloni (2023) were earlier chief guests; von der Leyen was a Republic Day chief guest.",
  current=ca("2026-03-05"))

G(T, HOST, "Intermediate",
  "The 36th NATO summit, at which the allies adopted the Ankara Summit Declaration, was held on 7-8 July 2026 in which "
  "city?",
  ["Ankara", "Istanbul", "The Hague", "Brussels"], "*",
  "NATO summit 2026",
  "Leaders of NATO's 32 members met at the Beştepe Presidential Complex in Ankara on 7-8 July 2026, reaffirming Article "
  "5 and support for Ukraine. It was the second NATO summit hosted by Türkiye, after Istanbul in 2004.",
  ["Venue: Ankara, Türkiye (7-8 July 2026)", "Previous summit in Türkiye: Istanbul, 2004"],
  [fact("Overview: 2026 NATO Summit in Ankara", "nato_nato"),
   fact("NATO reaffirms ironclad joint defence in Ankara Declaration", "nato_sabah")],
  why="Istanbul hosted in 2004; The Hague and Brussels did not host in 2026.",
  current=ca("2026-07-07"))

G(T, HOST, "Intermediate",
  "In May 2026 the foreign ministers of the Quad (India, the US, Japan and Australia) met in which city?",
  ["New Delhi", "Tokyo", "Washington, D.C.", "Canberra"], "*",
  "Quad foreign ministers, 2026",
  "The Quad foreign ministers wrapped up their meeting in New Delhi on 26 May 2026 without fixing a date for the "
  "leaders' summit that India was due to host.",
  ["Meeting: Quad foreign ministers, New Delhi", "Ended: 26 May 2026"],
  [fact("Quad foreign ministers meet in New Delhi as leaders' summit remains elusive", "quad_star"),
   fact("Annual Quad summits unlikely; India may pass on baton to Australia", "quad_print")],
  why="The 2026 foreign ministers' meeting was in New Delhi.",
  current=ca("2026-05-26"))

# ====================================================================== Important Days (4 / 0 / 4)
T = "Important Days"
DT = "Days and themes"

G(T, DT, "Basic",
  "National Mathematics Day, observed on 22 December, marks the birth anniversary of which mathematician?",
  ["Srinivasa Ramanujan", "C. R. Rao", "Aryabhata", "D. R. Kaprekar"], "*",
  "National Mathematics Day",
  "22 December is Srinivasa Ramanujan's birth anniversary (born 1887). The day was announced at his 125th birth "
  "anniversary celebrations and first observed on 22 December 2012, which was also named National Mathematical Year.",
  ["Date: 22 December", "Honours: Srinivasa Ramanujan"],
  [fact("National Mathematics Day (India) on 22 December marks Ramanujan's birth anniversary", "math_wiki"),
   fact("PM declares Ramanujan's birthday as National Mathematics Day", "math_ibt")],
  why="National Statistics Day honours P. C. Mahalanobis, not C. R. Rao; the others are not linked to 22 December.")

G(T, DT, "Basic",
  "Kisan Diwas (National Farmers' Day), observed on 23 December, marks the birth anniversary of whom?",
  ["Chaudhary Charan Singh", "Lal Bahadur Shastri", "M. S. Swaminathan", "Sardar Vallabhbhai Patel"], "*",
  "Kisan Diwas",
  "Kisan Diwas has been observed since 2001 on the birth anniversary of former Prime Minister Chaudhary Charan Singh, "
  "known for his work for farmers. He was awarded the Bharat Ratna in 2024.",
  ["Date: 23 December", "Honours: Chaudhary Charan Singh (5th PM)", "Observed since: 2001"],
  [fact("National Farmers' Day on 23 December, birth anniversary of Chaudhary Charan Singh", "kisan_vikas"),
   fact("Kisan Diwas: a tribute to former PM Chaudhary Charan Singh", "kisan_fpj")],
  why="The others are not linked to 23 December.")

G(T, DT, "Basic",
  "Armed Forces Flag Day, observed since 1949 to raise funds for the welfare of armed forces personnel, falls on which "
  "date?",
  ["7 December", "15 January", "4 December", "8 October"], "*",
  "Armed Forces Flag Day",
  "A committee under the Defence Minister decided on 28 August 1949 to observe a Flag Day every year on 7 December; "
  "token flags are distributed to collect money for ex-servicemen, serving personnel and their families.",
  ["Flag Day: 7 December", "Army Day: 15 Jan; Navy Day: 4 Dec; Air Force Day: 8 Oct"],
  [fact("Armed Forces Flag Day on 7 December, observed since 1949", "flag_tribune"),
   fact("Armed Forces Flag Day being observed on 7 December", "flag_air")],
  why="15 January is Army Day, 4 December Navy Day and 8 October Air Force Day.")

G(T, DT, "Basic",
  "National Girl Child Day, observed in India since 2008, falls on which date?",
  ["24 January", "11 October", "8 March", "14 November"], "*",
  "National Girl Child Day",
  "The Ministry of Women and Child Development began National Girl Child Day on 24 January in 2008 to raise awareness "
  "of discrimination faced by girls. 11 October is the UN's International Day of the Girl Child.",
  ["Date: 24 January", "Started: 2008 by the Ministry of Women and Child Development"],
  [fact("National Girl Child Day is observed on 24 January", "girl_wiki"),
   fact("National Girl Child Day began in 2008 under the Ministry of WCD", "girl_cry")],
  why="11 October is the International Day of the Girl Child, 8 March Women's Day and 14 November Children's Day.")

G(T, DT, "Advanced",
  "Which country hosted the global celebration of World Environment Day on 5 June 2026?",
  ["Azerbaijan", "Republic of Korea", "Saudi Arabia", "Côte d'Ivoire"], "*",
  "World Environment Day 2026",
  "UNEP chose Azerbaijan to host World Environment Day 2026, with the global event in Baku on 5 June 2026; the 2026 "
  "edition focused on climate action.",
  ["Date: 5 June 2026", "Host: Azerbaijan (Baku)", "Focus: climate action"],
  [fact("World Environment Day 2026: host Azerbaijan, global event in Baku; theme climate action", "wed_page"),
   fact("World Environment Day 2026 (UNEP)", "wed_unep")],
  why="The other countries hosted earlier editions.",
  current=ca("2026-06-05"))

G(T, DT, "Advanced",
  "What was the theme of World Water Day 2026 (22 March)?",
  ["Water and Gender", "Glacier Preservation", "Water for Peace", "Groundwater: Making the Invisible Visible"], "*",
  "World Water Day 2026",
  "UN-Water's 2026 theme was 'Water and Gender', with the slogan 'Where water flows, equality grows'; UNICEF and UN "
  "Women led the campaign. The UN World Water Development Report 2026 was launched on the day.",
  ["Date: 22 March 2026", "Theme: Water and Gender"],
  [fact("World Water Day 2026: Water and Gender - where water flows, equality grows", "wwd_arizona"),
   fact("World Water Day 2026 celebration and launch of UN World Water Development Report", "wwd_eu")],
  why="The other themes belong to earlier years.",
  current=ca("2026-03-22"))

G(T, DT, "Advanced",
  "What was the theme of World Health Day 2026 (7 April)?",
  ["Together for health. Stand with science.", "Healthy beginnings, hopeful futures", "My health, my right",
   "Health for All"], "*",
  "World Health Day 2026",
  "WHO's 2026 campaign 'Together for health. Stand with science.' built on the One Health approach, and the day was "
  "linked to an International One Health Summit hosted by WHO and France on 7 April.",
  ["Date: 7 April 2026", "Theme: Together for health. Stand with science."],
  [fact("World Health Day 2026: Together for health. Stand with science.", "whd_who"),
   fact("WHO calls on the world to stand with science on World Health Day", "whd_devaid")],
  why="The other themes belong to earlier years.",
  current=ca("2026-04-07"))

GS(T, DT, "Advanced", "the International Day of Yoga 2026",
   ["Its theme was 'Yoga for Healthy Ageing'.",
    "It was the 12th International Day of Yoga."],
   [True, True],
   "International Day of Yoga 2026",
   "The Ministry of Ayush announced in May 2026 that the theme of IDY 2026 would be 'Yoga for Healthy Ageing'. The "
   "first IDY was observed in 2015, so 21 June 2026 was the 12th edition.",
   [fact("International Yoga Day 2026 celebrated with theme 'Yoga for Healthy Ageing'", "idy_air"),
    fact("12th International Day of Yoga 2026", "idy_drishti")],
   why="Both statements are correct.",
   shortcut="2015 + 11 = 2026, so 2026 is the 12th edition.",
   current=ca("2026-06-21"))

# ====================================================================== National and International Organizations (2/6/2)
T = "National and International Organizations"
HQ, MEM = "Headquarters and heads", "Membership"

G(T, HQ, "Basic",
  "The International Maritime Organization (IMO), the UN specialised agency for shipping, is headquartered in which "
  "city?",
  ["London", "Geneva", "Hamburg", "Rotterdam"], "*",
  "IMO headquarters",
  "The IMO is headquartered at 4 Albert Embankment, London, and is the only UN specialised agency based in the United "
  "Kingdom. Its building was opened by Queen Elizabeth II in 1983.",
  ["IMO HQ: London"],
  [fact("IMO is a UN specialised agency headquartered in London", "imo_wiki"),
   fact("London's only UN agency headquarters (IMO)", "imo_hsn")],
  why="Hamburg hosts the International Tribunal for the Law of the Sea; Geneva and Rotterdam are not the IMO's seat.")

G(T, HQ, "Basic",
  "The International Civil Aviation Organization (ICAO), created by the Chicago Convention of 1944, has its "
  "headquarters in which city?",
  ["Montreal", "Chicago", "Geneva", "Washington, D.C."], "*",
  "ICAO headquarters",
  "The Convention on International Civil Aviation was signed in Chicago on 7 December 1944 and came into force on "
  "4 April 1947. ICAO's permanent headquarters is in Montreal, Canada.",
  ["Chicago Convention: 1944", "ICAO HQ: Montreal"],
  [fact("ICAO's permanent headquarters is in Montreal", "icao_brit"),
   fact("International Civil Aviation Organization profile", "icao_unsceb")],
  why="Chicago is where the convention was signed, not the headquarters.")

G(T, HQ, "Intermediate",
  "The International Telecommunication Union, founded in Paris in 1865 as the International Telegraph Union, is "
  "headquartered in which city?",
  ["Geneva", "Bern", "Paris", "New York"], "*",
  "ITU headquarters",
  "The ITU was founded in Paris in 1865, ran its bureau from Bern from 1868 and moved to Geneva in 1948. It became a "
  "UN specialised agency in 1947 and is the oldest UN agency.",
  ["Founded: Paris, 1865", "Bureau in Bern from 1868", "Geneva since 1948"],
  [fact("ITU headquartered in Geneva since 1948, moved from Bern; UN specialised agency since 1947", "itu_wiki"),
   fact("ITU history overview: founded in Paris in 1865", "itu_hist")],
  why="Paris was where it was founded and Bern its earlier seat; New York hosts UN headquarters.")

G(T, HQ, "Intermediate",
  "Mahmoud Ali Youssouf, elected Chairperson of the African Union Commission at the AU summit in Addis Ababa in "
  "February 2025, is from which country?",
  ["Djibouti", "Chad", "Algeria", "Ethiopia"], "*",
  "African Union Commission",
  "Djibouti's long-serving Foreign Minister Mahmoud Ali Youssouf won after seven rounds of voting at the 38th AU "
  "summit for the 2025-2028 term, succeeding Chad's Moussa Faki Mahamat. Algeria's Selma Haddadi was elected Deputy "
  "Chairperson. The AU is headquartered in Addis Ababa.",
  ["Chairperson: Mahmoud Ali Youssouf (Djibouti)", "Predecessor: Moussa Faki Mahamat (Chad)",
   "Deputy: Selma Haddadi (Algeria)"],
  [fact("Mahmoud Ali Youssouf elected to head African Union Commission", "au_channels"),
   fact("Djibouti's Foreign Minister elected Chairperson of AU Commission", "au_gna")],
  why="Chad was the predecessor's country, Algeria the deputy's, and Ethiopia hosts the AU headquarters.",
  current=ca("2025-02-15"))

G(T, HQ, "Intermediate",
  "Haitham Al Ghais, whose second three-year term as Secretary General of OPEC began on 1 August 2025, is from which "
  "country?",
  ["Kuwait", "Saudi Arabia", "Nigeria", "United Arab Emirates"], "*",
  "OPEC Secretary General",
  "Haitham Al Ghais of Kuwait took office at the OPEC Secretariat in Vienna on 1 August 2022, succeeding Nigeria's "
  "Mohammad Sanusi Barkindo. In December 2024 he was re-appointed for three more years from 1 August 2025.",
  ["SG: Haitham Al Ghais (Kuwait)", "Second term from: 1 Aug 2025", "OPEC Secretariat: Vienna"],
  [fact("Haitham Al Ghais takes office as OPEC Secretary-General in Vienna", "opec_gulf"),
   fact("Al Ghais re-appointed for a further three years from 1 Aug 2025", "opec_wiki")],
  why="Barkindo, his predecessor, was from Nigeria; he is not from Saudi Arabia or the UAE.",
  current=ca("2025-08-01"))

G(T, MEM, "Intermediate",
  "Bulgaria adopted the euro on 1 January 2026. How many EU member states use the euro after its entry?",
  ["21", "20", "19", "27"], "*",
  "Euro area membership",
  "EU finance ministers approved Bulgaria's entry on 8 July 2025, and it became the 21st euro area member on 1 January "
  "2026, replacing the lev. Croatia had become the 20th member in 2023. The EU itself has 27 members.",
  ["Euro area before: 20", "Bulgaria joined 1 Jan 2026 -> 21"],
  [fact("Bulgaria became the 21st member of the euro area in 2026", "bulg_bdf"),
   fact("Bulgaria joins euro: a new chapter begins on 1 Jan 2026", "bulg_eu")],
  why="20 was the count before Bulgaria; 27 is the EU's membership.",
  shortcut="Croatia was the 20th (2023), so Bulgaria is the 21st.",
  current=ca("2026-01-01"))

G(T, HQ, "Intermediate",
  "The International Renewable Energy Agency (IRENA) has its headquarters in which city?",
  ["Abu Dhabi", "Bonn", "Vienna", "Gurugram"], "*",
  "IRENA headquarters",
  "IRENA was formed in 2009; the UAE beat Germany and Austria for the headquarters, and its permanent headquarters in "
  "Masdar City, Abu Dhabi, was inaugurated in 2015.",
  ["IRENA founded: 2009", "HQ: Masdar City, Abu Dhabi"],
  [fact("IRENA is headquartered in Masdar City, Abu Dhabi", "irena_wiki"),
   fact("Sheikh Abdullah bin Zayed inaugurates IRENA HQ in Masdar City", "irena_masdar")],
  why="Gurugram hosts the International Solar Alliance; Bonn and Vienna lost the bid.")

G(T, HQ, "Intermediate",
  "Celeste Saulo, the first woman to head the World Meteorological Organization, is from which country?",
  ["Argentina", "Chile", "Brazil", "Finland"], "*",
  "WMO Secretary-General",
  "Celeste Saulo, earlier Director of Argentina's National Meteorological Service, was appointed by the World "
  "Meteorological Congress in 2023 and took office on 1 January 2024, succeeding Finland's Petteri Taalas.",
  ["WMO SG: Celeste Saulo (Argentina)", "Took office: 1 Jan 2024", "Predecessor: Petteri Taalas (Finland)"],
  [fact("Celeste Saulo of Argentina appointed first female Secretary-General of WMO", "wmo_news")],
  why="Finland was her predecessor's country; she is not from Chile or Brazil.",
  current=ca("2024-01-01"))

GS(T, MEM, "Advanced", "recent accessions to the World Trade Organization",
   ["Comoros became the 165th member of the WTO in 2024.",
    "Timor-Leste became the 166th member of the WTO in 2024.",
    "These were the first accessions since Liberia and Afghanistan joined in 2016."],
   [True, True, True],
   "WTO membership",
   "The accessions of Comoros and Timor-Leste were approved at MC13 in Abu Dhabi on 26 February 2024. Comoros became "
   "the 165th member on 21 August 2024 and Timor-Leste the 166th on 30 August 2024, the first new members since Liberia "
   "and Afghanistan in 2016.",
   [fact("Comoros, Timor-Leste formally join WTO during MC13 in Abu Dhabi", "wto_wam"),
    fact("Timor-Leste officially becomes full member of the WTO", "wto_tatoli"),
    fact("Comoros becomes 165th member of the WTO", "wto_newarab")],
   why="All three statements are correct.",
   current=ca("2024-08-30"))

GS(T, HQ, "Advanced", "UNICEF",
   ["Catherine Russell took office as UNICEF's Executive Director on 1 February 2022.",
    "She succeeded Henrietta Fore.",
    "UNICEF is headquartered in Geneva."],
   [True, True, False],
   "UNICEF leadership",
   "Catherine Russell of the United States became UNICEF's eighth Executive Director on 1 February 2022, succeeding "
   "Henrietta Fore. UNICEF is headquartered in New York.",
   [fact("Catherine Russell assumes functions as new UNICEF Executive Director, succeeding Henrietta Fore",
         "unicef_pr")],
   why="Statement 3 is wrong: UNICEF headquarters is in New York.",
   current=ca("2022-02-01"))

# ====================================================================== Important Reports and Indexes (5 / 0 / 5)
T = "Important Reports and Indexes"
PUB, RANK = "Publishing body", "India's rank"

G(T, PUB, "Basic",
  "The Global Risks Report, whose 2026 edition named geoeconomic confrontation as the top risk, is published by which "
  "organisation?",
  ["World Economic Forum", "International Monetary Fund", "World Bank", "UN Development Programme"], "*",
  "Global Risks Report",
  "The WEF publishes the Global Risks Report each January before its Davos meeting. The 21st edition, released on "
  "14 January 2026, ranked geoeconomic confrontation as the top short-term risk.",
  ["Publisher: World Economic Forum", "2026 top risk: geoeconomic confrontation"],
  [fact("Global Risks Report 2026 (WEF press release)", "grr_wef"),
   fact("WEF: geoeconomic confrontation now top risk", "grr_bt")],
  why="The IMF publishes the World Economic Outlook, the World Bank Global Economic Prospects and UNDP the HDR.",
  current=ca("2026-01-14"))

G(T, PUB, "Basic",
  "The Emissions Gap Report, whose 2025 edition 'Off Target' was released in November 2025, is published by which "
  "body?",
  ["UN Environment Programme (UNEP)", "Intergovernmental Panel on Climate Change (IPCC)",
   "World Meteorological Organization", "International Energy Agency"], "*",
  "Emissions Gap Report",
  "UNEP's annual Emissions Gap Report compares pledged and needed emission cuts. The 2025 edition projected 2.3-2.5 °C "
  "of warming this century if national pledges are fully implemented.",
  ["Publisher: UNEP", "2025 edition: 'Off Target'"],
  [fact("UNEP Emissions Gap Report 2025: world on track for 2.3-2.5 °C", "egr_dte"),
   fact("UNEP Emissions Gap Report 2025", "egr_pbl")],
  why="The IPCC writes assessment reports, the WMO climate bulletins and the IEA the World Energy Outlook.",
  current=ca("2025-11-04"))

G(T, PUB, "Basic",
  "The Global Tuberculosis Report, whose 2025 edition said India accounted for about a quarter of TB cases worldwide, "
  "is published by which organisation?",
  ["World Health Organization", "UNICEF", "The Global Fund", "UNAIDS"], "*",
  "Global Tuberculosis Report",
  "WHO publishes the Global TB Report every year. The 2025 edition said India had the most TB cases in 2024, about 25% "
  "of the world's total, though its incidence fell 21% between 2015 and 2024.",
  ["Publisher: WHO", "India's share (2024): about 25%"],
  [fact("India recorded the most TB cases globally in 2024: WHO", "tb_scroll"),
   fact("India records 21% drop in TB incidence: WHO report", "tb_wire")],
  why="The other bodies fund or work on health but do not publish this report.",
  current=ca("2025-11-12"))

G(T, PUB, "Basic",
  "The World Energy Outlook, an annual flagship report on global energy trends, is published by which body?",
  ["International Energy Agency (IEA)", "OPEC", "International Renewable Energy Agency (IRENA)", "World Bank"], "*",
  "World Energy Outlook",
  "The Paris-based IEA publishes the World Energy Outlook. The 2025 edition, released in November 2025, described an "
  "'Age of Electricity' and warned of energy security risks.",
  ["Publisher: International Energy Agency"],
  [fact("World Energy Outlook 2025 (IEA)", "weo_iea"),
   fact("World Energy Outlook 2025: IEA warns of security risks in Age of Electricity", "weo_dte")],
  why="OPEC publishes the World Oil Outlook; IRENA and the World Bank have other reports.")

G(T, PUB, "Basic",
  "The Henley Passport Index, which ranks passports by the number of destinations their holders can enter without a "
  "prior visa, is published by which firm?",
  ["Henley & Partners", "International Air Transport Association", "Arton Capital", "World Economic Forum"], "*",
  "Henley Passport Index",
  "The index is compiled by Henley & Partners, a London-based citizenship and residence advisory firm, using IATA "
  "data. Its 2026 edition was released in January 2026.",
  ["Publisher: Henley & Partners", "Data source: IATA"],
  [fact("Henley Passport Index 2026 released by Henley & Partners", "henley_bt")],
  why="IATA supplies the data but does not publish the index; Arton Capital publishes a different passport index.",
  current=ca("2026-01-13"))

G(T, RANK, "Advanced",
  "What was India's rank in Transparency International's Corruption Perceptions Index 2025, released in February "
  "2026?",
  ["91st", "96th", "85th", "101st"], "*",
  "Corruption Perceptions Index 2025",
  "India ranked 91st of 182 countries and territories with a score of 39/100, up five places from 96th (score 38) in "
  "the 2024 index. Denmark topped the index.",
  ["CPI 2025: 91st of 182 (score 39)", "CPI 2024: 96th (score 38)"],
  [fact("India jumps 5 places on CPI, holds 91st rank", "cpi_ti_de"),
   fact("CPI 2025: India ranks 91st among 182 countries", "cpi_ti_nb")],
  why="96th was India's rank in the 2024 index; the other ranks are wrong.",
  current=ca("2026-02-10"))

G(T, RANK, "Advanced",
  "What was India's rank in the RSF World Press Freedom Index 2026?",
  ["157th", "151st", "159th", "161st"], "*",
  "World Press Freedom Index 2026",
  "In the index released on 30 April 2026, India ranked 157th of 180 countries with a score of 31.96, down six places "
  "from 151st in 2025, in the 'very serious' category. Norway topped the index.",
  ["2026: 157th of 180", "2025: 151st", "2024: 159th"],
  [fact("India is 157th out of 180 countries on RSF's 2026 World Press Freedom Index", "wpfi_wire"),
   fact("Press Freedom Index 2026: India drops to 157 from 151", "wpfi_fpj")],
  why="151st was the 2025 rank and 159th the 2024 rank.",
  current=ca("2026-04-30"))

G(T, RANK, "Advanced",
  "In the Climate Change Performance Index 2026, released at COP30 in November 2025, what was India's rank?",
  ["23rd", "10th", "7th", "13th"], "*",
  "Climate Change Performance Index 2026",
  "India fell 13 places from 10th to 23rd (score 61.31), moving from the 'high' to the 'medium' category, mainly for "
  "lacking a coal phase-out timeline. The CCPI is published by Germanwatch, NewClimate Institute and Climate Action "
  "Network; the top three places were left vacant.",
  ["CCPI 2025: 10th", "CCPI 2026: 23rd (down 13)"],
  [fact("India slips 13 ranks on Climate Change Performance Index", "ccpi_wire"),
   fact("India slides 13 spots on CCPI; coal a major barrier", "ccpi_print")],
  why="10th was the previous year's rank; 13 is the number of places India fell.",
  shortcut="10 + 13 = 23.",
  current=ca("2025-11-18"))

G(T, RANK, "Advanced",
  "What was India's rank in the Global Peace Index 2026 published by the Institute for Economics and Peace?",
  ["127th", "115th", "116th", "131st"], "*",
  "Global Peace Index 2026",
  "India ranked 127th of 163 countries in GPI 2026 (score 2.409), down from 115th in 2025. Iceland stayed the most "
  "peaceful country and Russia ranked last.",
  ["GPI 2026: 127th of 163", "GPI 2025: 115th"],
  [fact("Global Peace Index 2026: the 10 most peaceful countries; India 127th", "gpi_ot"),
   fact("Global Peace Index 2026: India 127th, down from 115th", "gpi_drishti")],
  why="115th was the 2025 rank; 116th was India's World Happiness Report 2026 rank; 131st its Gender Gap rank.",
  current=ca("2026-06-15"))

G(T, RANK, "Advanced",
  "What was India's rank in the Henley Passport Index 2026, released in January 2026?",
  ["80th", "85th", "77th", "55th"], "*",
  "Henley Passport Index 2026",
  "India rose five places from 85th to 80th, sharing the rank with Algeria and Niger, even though visa-free or "
  "visa-on-arrival access fell from 57 to 55 destinations. Singapore ranked first with access to 192 destinations.",
  ["2025: 85th", "2026: 80th", "Destinations: 55"],
  [fact("Henley Passport Index 2026: Indian passport climbs five places to 80th", "henley_bt"),
   fact("Indian passport rises to 80th despite fewer visa-free destinations (55)", "henley_fpj")],
  why="85th was the 2025 rank and 55 is the number of destinations, not the rank.",
  current=ca("2026-01-13"))

# ====================================================================== Economic Affairs (3 / 3 / 4)
T = "Economic Affairs"
GDP, INF, FIS, MP = "GDP and growth projections", "Inflation data", "Fiscal data", "Monetary policy decisions"

G(T, GDP, "Basic",
  "According to estimates released on 28 November 2025, what was India's real GDP growth in the July-September "
  "quarter (Q2) of 2025-26?",
  ["8.2%", "5.6%", "8.7%", "7.4%"], "*",
  "Q2 2025-26 GDP",
  "The National Statistics Office estimated real GDP growth of 8.2% in Q2 of 2025-26, a six-quarter high, against "
  "5.6% in Q2 of 2024-25. Nominal GDP grew 8.7%, and real growth in the first half (April-September) was 8.0%.",
  ["Q2 2024-25: 5.6%", "Q2 2025-26: 8.2% (real)", "Nominal Q2 2025-26: 8.7%"],
  [fact("India's Q2 FY26 GDP surges 8.2%", "gdp_q2_bt"),
   fact("Indian economy grows 8.2% in Q2 2025-26, up from 5.6%", "gdp_q2_tribune")],
  why="5.6% is the same quarter a year earlier; 8.7% is nominal growth; 7.4% was a full-year projection.",
  current=ca("2025-11-28"))

G(T, GDP, "Basic",
  "In its World Economic Outlook of October 2026, what growth did the IMF project for India for 2026 (fiscal year "
  "2026-27)?",
  ["7.0%", "6.4%", "3.1%", "7.8%"], "*",
  "IMF projection, October 2026",
  "The IMF raised India's projection for fiscal 2026 to 7.0%, 0.6 percentage point above its July 2026 update, keeping "
  "India among the fastest-growing major economies. It projected global growth of 3.1% in 2026.",
  ["IMF Oct 2026, India FY27: 7.0%", "Global growth 2026: 3.1%"],
  [fact("IMF raises India's growth forecast to 7% for 2026, up 60 bps", "imf_oct"),
   fact("IMF raises India's growth forecast to 7%, among fastest-growing major economies", "imf_dd"),
   fact("Earlier IMF projection for 2026-27: 6.4%", "imf_jan")],
  why="6.4% was an earlier IMF projection; 3.1% is the global growth projection; 7.8% is India's actual Q1 growth.",
  current=ca("2026-10-13"))

G(T, MP, "Basic",
  "What did the RBI's Monetary Policy Committee decide on the policy repo rate at its meeting of 3-5 June 2026?",
  ["Kept it unchanged at 5.25%", "Cut it by 25 bps to 5.00%", "Raised it by 25 bps to 5.50%",
   "Kept it unchanged at 5.50%"], "*",
  "MPC, June 2026",
  "The MPC voted unanimously on 5 June 2026 to keep the repo rate at 5.25% with a neutral stance, its third pause in a "
  "row after the December 2025 cut. The rate was raised to 5.50% only in October 2026.",
  ["Repo after Dec 2025 cut: 5.25%", "June 2026: unchanged at 5.25%", "Oct 2026: raised to 5.50%"],
  [fact("RBI holds repo rate at 5.25%, keeps stance neutral (5 June 2026)", "mpc_jun_bs"),
   fact("RBI MPC June 2026: repo unchanged at 5.25%", "mpc_jun_angel")],
  why="There was no cut; the hike to 5.50% came in October 2026.",
  current=ca("2026-06-05"))

G(T, FIS, "Intermediate",
  "Gross GST collections reached an all-time monthly high in April 2026. About how much was collected?",
  ["₹2.43 lakh crore", "₹2.11 lakh crore", "₹22.27 lakh crore", "₹3.10 lakh crore"], "*",
  "GST collections, April 2026",
  "Gross GST collections in April 2026 were ₹2,42,702 crore (about ₹2.43 lakh crore), up 8.7% year on year and the "
  "highest monthly figure since GST began in 2017. After refunds of ₹31,793 crore, net collections were ₹2,10,909 "
  "crore. Gross collections for the whole of 2025-26 crossed ₹22.27 lakh crore.",
  ["Gross April 2026: ₹2,42,702 crore", "Net: ₹2,10,909 crore", "Gross FY 2025-26: ₹22.27 lakh crore"],
  [fact("GST collections hit all-time high of over ₹2.42 lakh crore in April 2026", "gst_air"),
   fact("April 2026 gross ₹2,42,702 crore, net ₹2,10,909 crore; FY26 gross ₹22.27 lakh crore", "gst_munim")],
  why="₹2.11 lakh crore is the net figure; ₹22.27 lakh crore is the whole-year figure.",
  current=ca("2026-05-01"))

G(T, GDP, "Intermediate",
  "The Economic Survey 2025-26, tabled on 29 January 2026, projected India's real GDP growth for 2026-27 in which "
  "range?",
  ["6.8% to 7.2%", "6.3% to 6.8%", "7.4% to 7.8%", "6.0% to 6.4%"], "*",
  "Economic Survey 2025-26",
  "The Survey tabled by the Finance Minister on 29 January 2026 projected 6.8-7.2% growth for 2026-27, slower than the "
  "7.4% then projected for 2025-26, and called for caution but not pessimism.",
  ["FY27 projection: 6.8-7.2%", "FY26 estimate then: 7.4%"],
  [fact("Economic Survey pegs FY27 GDP growth at 6.8 to 7.2%", "survey_dh"),
   fact("Economic Survey pegs FY26 GDP growth at 7.4%", "survey_ml")],
  why="The other ranges are not the Survey's projection for 2026-27.",
  current=ca("2026-01-29"))

G(T, INF, "Intermediate",
  "What was India's headline CPI (retail) inflation for September 2026, released on 12 October 2026?",
  ["5.54%", "4.83%", "7.74%", "6.08%"], "*",
  "CPI inflation, September 2026",
  "On the 2024-base CPI series, headline inflation rose to 5.54% in September 2026 from 4.83% in August, driven by "
  "food prices: food inflation was 7.74%. Rural inflation was 6.08% and urban 4.88%.",
  ["Aug 2026: 4.83%", "Sep 2026: 5.54%", "Food: 7.74%; rural 6.08%; urban 4.88%"],
  [fact("India's retail inflation rises to 5.54% in September 2026 on food prices", "cpi_sep_tt"),
   fact("CPI Sept 2026: 5.54%; food 7.74%; rural 6.08%, urban 4.88%", "cpi_sep_gr")],
  why="4.83% is August's figure; 7.74% is food inflation; 6.08% is rural inflation.",
  current=ca("2026-10-12"))

GS(T, MP, "Advanced", "the RBI Monetary Policy Committee review of 4-6 February 2026",
   ["It kept the policy repo rate unchanged at 5.25%.",
    "It changed the policy stance from neutral to accommodative.",
    "By then the repo rate had been cut by a cumulative 125 basis points since February 2025."],
   [True, False, True],
   "MPC, February 2026",
   "In the first review after the Union Budget 2026-27, the MPC kept the repo rate at 5.25% and the stance neutral "
   "(the SDF stayed at 5.00% and the MSF and Bank Rate at 5.50%). The rate had been cut by 125 bps since February 2025 "
   "(25 in Feb, 25 in Apr, 50 in June and 25 in Dec 2025). The MPC raised its 2025-26 growth estimate to 7.4%.",
   [fact("RBI holds repo at 5.25% in February 2026, lifts GDP outlook to 7.4%", "mpc_feb_week"),
    fact("RBI keeps repo unchanged, maintains neutral stance; cumulative 125 bps cut since Feb 2025", "mpc_feb_fpj")],
   why="Statement 2 is wrong: the stance stayed neutral.",
   shortcut="25 + 25 + 50 + 25 = 125 bps.",
   current=ca("2026-02-06"))

GS(T, FIS, "Advanced", "the Centre's provisional accounts for 2025-26 released by the Controller General of Accounts "
   "on 1 June 2026",
   ["The fiscal deficit target of 4.4% of GDP for 2025-26 was met.",
    "The fiscal deficit in absolute terms was 97.5% of the Revised Estimate.",
    "The fiscal deficit for 2024-25 had been 4.8% of GDP."],
   [True, True, True],
   "Fiscal outcome 2025-26",
   "CGA data showed a provisional fiscal deficit of ₹15,19,169 crore for 2025-26, 97.5% of the Revised Estimate of "
   "₹15,58,492 crore, so the 4.4%-of-GDP target was met. The deficit in 2024-25 was 4.8% of GDP.",
   [fact("Government achieves fiscal deficit target of 4.4% for FY26; deficit 97.5% of RE", "fd_dh"),
    fact("Govt achieves fiscal deficit target of 4.4% for FY26; FY25 deficit 4.8%", "fd_ob")],
   why="All three statements are correct.",
   current=ca("2026-06-01"))

GS(T, GDP, "Advanced", "the provisional estimates of national income for 2025-26 released on 5 June 2026",
   ["Real GDP grew 7.7% in 2025-26, up from 7.1% in 2024-25.",
    "Real GDP grew 7.8% in the January-March 2026 quarter.",
    "The estimates are at constant 2011-12 prices."],
   [True, True, False],
   "Provisional estimates 2025-26",
   "The provisional estimates put 2025-26 real GDP growth at 7.7% (above the 7.6% estimated in February) and Q4 growth "
   "at 7.8%. They use the new series at constant 2022-23 prices, not the old 2011-12 base.",
   [fact("India's GDP growth hits 7.7% in FY26, fastest in two years", "gdp_fy26_bt"),
    fact("India's GDP grows 7.8% in Q4, full-year growth at 7.7%", "gdp_fy26_ob")],
   why="Statement 3 is wrong: the base year is now 2022-23.",
   current=ca("2026-06-05"))

GS(T, GDP, "Advanced", "India's balance of payments in April-June 2026, as per RBI data released on 1 September 2026",
   ["The current account deficit was USD 4.2 billion, or 0.5% of GDP.",
    "The current account deficit was narrower than in April-June 2025.",
    "Foreign portfolio investors made net outflows during the quarter."],
   [True, False, True],
   "Current account, Q1 2026-27",
   "The CAD widened to USD 4.2 billion (0.5% of GDP) in Q1 2026-27 from USD 3.4 billion (0.4%) a year earlier, as the "
   "merchandise trade deficit rose to USD 86.1 billion. Foreign portfolio investors pulled out a net USD 9.6 billion.",
   [fact("India's CAD widens to USD 4.2 billion in Q1 FY27: RBI data", "cad_fpj"),
    fact("Current account deficit widens to USD 4.2 bn in Q1, from USD 3.4 bn", "cad_print")],
   why="Statement 2 is wrong: the deficit widened from USD 3.4 billion.",
   current=ca("2026-09-01"))

# ====================================================================== Government Policies (0 / 7 / 0)
T = "Government Policies"
POL, REG = "Policy changes", "Regulatory reforms"

G(T, REG, "Intermediate",
  "The Viksit Bharat Shiksha Adhishthan Bill, 2025, introduced in the Lok Sabha on 15 December 2025, proposes to "
  "replace which regulators with a single higher education body?",
  ["UGC, AICTE and NCTE", "UGC, NAAC and NCERT", "AICTE, Bar Council of India and National Medical Commission",
   "UGC, CBSE and NCTE"], "*",
  "Viksit Bharat Shiksha Adhishthan Bill",
  "The Bill would replace the UGC, AICTE and NCTE and repeal the Acts that set them up. The Adhishthan would have a "
  "Regulatory Council, an Accreditation Council and a Standards Council. Legal and medical education stay outside it. "
  "The Bill was referred to a Joint Parliamentary Committee.",
  ["Replaces: UGC, AICTE, NCTE", "Councils: regulatory, accreditation, standards", "Excludes: legal, medical"],
  [fact("PRS: Bill replaces UGC, AICTE and NCTE; three councils; legal and medical education exempt; introduced "
        "15 Dec 2025", "vbsa_prs"),
   fact("Explained: Viksit Bharat Shiksha Adhishthan Bill aims to create single higher education regulator",
        "vbsa_dh")],
  why="NCERT and CBSE are school bodies; the BCI and NMC regulate legal and medical education, which are excluded.",
  current=ca("2025-12-15"))

G(T, POL, "Intermediate",
  "The Health Security se National Security Cess, approved by Parliament in December 2025, is levied on the "
  "production capacity of which product to begin with?",
  ["Pan masala", "Cigarettes", "Aerated sugary drinks", "Online gaming services"], "*",
  "Health Security se National Security Cess",
  "The Bill passed the Lok Sabha on 5 December and the Rajya Sabha on 8 December 2025. It levies a monthly cess on "
  "machines or processes used to make pan masala, with power to add other goods by notification; the proceeds fund "
  "national security and public health. Pan masala also attracts the 40% GST rate.",
  ["Passed: 8 Dec 2025", "Product: pan masala (others can be notified)", "Basis: production capacity"],
  [fact("Parliament passes Health Security and National Security Cess Bill, 2025 (8 Dec 2025)", "hsns_air"),
   fact("Pan masala cess bill passed; funds for national security and public health", "hsns_dc")],
  why="Cigarettes are covered by the Central Excise (Amendment) Act; the others are not covered.",
  current=ca("2025-12-08"))

G(T, POL, "Intermediate",
  "Parliament passed the Central Excise (Amendment) Bill, 2025 in December 2025 to raise excise duty on tobacco "
  "products. Which levy, due to end, is it meant to replace?",
  ["GST compensation cess", "Health and education cess on income tax", "Agriculture Infrastructure and Development Cess",
   "Securities transaction tax"], "*",
  "Central Excise (Amendment) Act, 2025",
  "With the GST compensation cess ending once its loans are repaid, the Bill (passed by the Lok Sabha on 3 December "
  "and approved by Parliament on 4 December 2025) restores higher excise duties on cigarettes and other tobacco so "
  "that the tax burden on them does not fall.",
  ["Problem: compensation cess ending", "Solution: higher central excise on tobacco"],
  [fact("Lok Sabha passes bill to levy excise duty on tobacco as GST cess nears end", "cea_tribune"),
   fact("Parliament OKs bill to hike central excise on tobacco, replacing GST cess", "cea_statesman")],
  why="The other levies are unrelated to tobacco taxation.",
  current=ca("2025-12-04"))

G(T, REG, "Intermediate",
  "Which new process does the Insolvency and Bankruptcy Code (Amendment) Act, 2026 add through new Sections 58A to "
  "58K?",
  ["Creditor-Initiated Insolvency Resolution Process", "Pre-packaged Insolvency Resolution Process for MSMEs",
   "Fast-track Corporate Insolvency Resolution Process", "Insolvency resolution for personal guarantors"], "*",
  "IBC (Amendment) Act, 2026",
  "Passed by the Lok Sabha on 30 March and the Rajya Sabha on 1 April 2026, the Act received assent on 6 April 2026. "
  "It adds a largely out-of-court Creditor-Initiated Insolvency Resolution Process (CIIRP) for select financial "
  "creditors and a chapter on group insolvency, and requires the NCLT to admit a financial creditor's application once "
  "debt and default are shown.",
  ["Assent: 6 April 2026", "New: CIIRP (Sections 58A-58K), group insolvency (Chapter VA)"],
  [fact("Parliament passes IBC amendment bill to cut delays", "ibc_tribune"),
   fact("IBC (Amendment) Act 2026: CIIRP under new Sections 58A to 58K; group insolvency; assent 6 Apr 2026",
        "ibc_indialaw")],
  why="Pre-packs for MSMEs, fast-track CIRP and personal guarantor insolvency already existed.",
  current=ca("2026-04-06"))

G(T, POL, "Intermediate",
  "The Jan Vishwas (Amendment of Provisions) Bill, 2026, passed by Parliament in April 2026, amends provisions in how "
  "many Central Acts?",
  ["79", "42", "17", "183"], "*",
  "Jan Vishwas 2026",
  "The Lok Sabha passed the Bill on 1 April and the Rajya Sabha on 2 April 2026. It amends 784 provisions in 79 Central "
  "Acts handled by 23 ministries and decriminalises 717 of them, mainly by replacing jail terms with penalties. It "
  "replaced a 2025 Bill covering 17 Acts that was withdrawn in March 2026.",
  ["Acts amended: 79", "Provisions: 784 amended, 717 decriminalised", "Earlier 2025 Bill: 17 Acts"],
  [fact("Lok Sabha passes Jan Vishwas Bill: 784 provisions in 79 Acts", "jv_etv"),
   fact("Parliament clears Jan Vishwas Bill 2026, replacing criminal penalties with civil fines", "jv_statesman")],
  why="42 Acts were covered by the 2023 Jan Vishwas Act; 17 by the withdrawn 2025 Bill; 183 provisions were "
      "decriminalised in 2023.",
  current=ca("2026-04-02"))

G(T, REG, "Intermediate",
  "Under capital market exposure directions issued by the RBI on 13 February 2026, effective from 1 April 2026, banks "
  "may for the first time provide which kind of finance?",
  ["Finance for corporate acquisitions", "Loans against gold jewellery", "Finance for priority sector borrowers",
   "Loans to Self-Help Groups"], "*",
  "Acquisition finance by banks",
  "Banks were earlier not allowed to fund acquisitions of companies. The RBI's revised capital market exposure rules "
  "now allow acquisition financing within exposure limits; the October 2025 draft had capped it at 10% of Tier 1 "
  "capital, and reports say the final rules relaxed the limits.",
  ["Issued: 13 Feb 2026", "Effective: 1 Apr 2026", "New: acquisition financing by banks"],
  [fact("Banks get green light for acquisition financing under revised RBI capital market rules", "acq_open"),
   fact("Draft proposed a 10% of Tier 1 cap on acquisition financing", "acq_vision"),
   fact("RBI eases acquisition finance rules, allows higher limits", "acq_caalley")],
  why="Banks already lend against gold, to the priority sector and to SHGs.",
  current=ca("2026-02-13"))

G(T, REG, "Intermediate",
  "The SEBI (Mutual Funds) Regulations, 2026, which came into force on 1 April 2026, replaced regulations of which "
  "year?",
  ["1996", "1993", "2008", "2019"], "*",
  "SEBI Mutual Funds Regulations, 2026",
  "SEBI notified the new regulations on 14 January 2026, effective 1 April 2026, replacing the 30-year-old SEBI "
  "(Mutual Funds) Regulations, 1996. They bring in an MF Lite regime for passive funds, a Specialized Investment Fund "
  "category and a 'Base Expense Ratio'.",
  ["Notified: 14 Jan 2026", "Effective: 1 Apr 2026", "Replaced: 1996 regulations"],
  [fact("SEBI notifies Mutual Funds Regulations, 2026", "mf_taxmann"),
   fact("SEBI revamps and replaces its 30-year-old mutual fund regulations", "mf_elp")],
  why="The 1993 regulations were the first MF rules; 1996 is the set that was replaced.",
  current=ca("2026-01-14"))

# ====================================================================== Business and Corporate News (6 / 1 / 7)
T = "Business and Corporate News"
MA, CP = "Mergers and acquisitions", "Corporate partnerships"

G(T, MA, "Basic",
  "In November 2025 Kimberly-Clark agreed to acquire which company, maker of Tylenol, in a deal valued at about USD "
  "48.7 billion?",
  ["Kenvue", "Haleon", "Reckitt", "Procter & Gamble"], "*",
  "Kimberly-Clark and Kenvue",
  "Announced on 3 November 2025, the cash-and-stock deal gives Kenvue shareholders $3.50 plus 0.14625 Kimberly-Clark "
  "share per share. Kimberly-Clark holders would own about 54% of the combined company, led by Mike Hsu and based in "
  "Irving, Texas. Closing was expected in the second half of 2026.",
  ["Announced: 3 Nov 2025", "Value: about USD 48.7 billion", "Target: Kenvue (Tylenol)"],
  [fact("Kimberly-Clark to acquire Tylenol maker Kenvue in USD 48.7 billion deal", "kc_cbs"),
   fact("Kimberly-Clark to acquire Kenvue in USD 48.7 bn deal", "kc_fw")],
  why="Haleon, Reckitt and P&G were not part of this deal.",
  current=ca("2025-11-03"))

G(T, MA, "Basic",
  "Warner Bros. Discovery agreed in February 2026 to be acquired by which company in a deal of about USD 110 billion, "
  "after Netflix declined to raise its offer?",
  ["Paramount Skydance", "Comcast", "Amazon", "Apple"], "*",
  "Paramount and Warner Bros. Discovery",
  "Warner Bros. Discovery had earlier agreed to sell its studios and streaming business to Netflix, but in "
  "late February 2026 declared Paramount Skydance's $31-a-share bid for the whole company superior. Netflix declined to "
  "match, and Paramount paid the $2.8 billion break fee owed to Netflix. The deal needed regulatory approvals.",
  ["Winning bidder: Paramount Skydance ($31/share, ~USD 110 bn)", "Netflix exited"],
  [fact("Paramount and Warner Bros. Discovery announce USD 110 billion deal", "wbd_abc"),
   fact("Paramount to buy Warner Bros after Netflix exits", "wbd_rte")],
  why="Netflix withdrew; Comcast, Amazon and Apple were not the buyers.",
  current=ca("2026-02-27"))

G(T, CP, "Basic",
  "Which company announced in December 2025 that it will invest more than USD 35 billion in India by 2030?",
  ["Amazon", "Microsoft", "Google", "Meta"], "*",
  "Big tech investment in India",
  "Amazon said on 10 December 2025 that it will invest over USD 35 billion in India by 2030 in AI, logistics and "
  "exports. A day earlier Microsoft pledged USD 17.5 billion for AI and cloud infrastructure.",
  ["Amazon: > USD 35 bn by 2030", "Microsoft: USD 17.5 bn"],
  [fact("After Microsoft, Amazon to invest USD 35 billion in India", "amzn_week"),
   fact("Amazon unveils USD 35 billion investment in India", "amzn_ds")],
  why="Microsoft's pledge was USD 17.5 billion; Google and Meta made no such pledge then.",
  current=ca("2025-12-10"))

G(T, MA, "Basic",
  "In March 2026 the NCLT approved Adani Enterprises' resolution plan for which insolvent company?",
  ["Jaiprakash Associates", "Jet Airways", "Reliance Communications", "Videocon Industries"], "*",
  "Adani and Jaiprakash Associates",
  "The NCLT Allahabad Bench approved the plan on 17 March 2026. Creditors had backed it with 93.81% of votes in "
  "November 2025. The plan is worth about ₹14,535 crore; Adani paid the first ₹6,000 crore tranche in May 2026 and the "
  "NCLAT refused Vedanta's plea to halt it.",
  ["NCLT approval: 17 Mar 2026", "Plan value: about ₹14,535 crore", "Rival: Vedanta"],
  [fact("Adani Enterprises says NCLT approves resolution plan for Jaiprakash Associates", "jal_bt"),
   fact("NCLT approves Adani Group ₹14,535 crore bid for Jaiprakash Associates", "jal_mp")],
  why="The other companies were not part of this resolution.",
  current=ca("2026-03-17"))

G(T, CP, "Basic",
  "Billionbrains Garage Ventures, which listed on the stock exchanges on 12 November 2025, is the parent company of "
  "which platform?",
  ["Groww", "Zerodha", "PhonePe", "Lenskart"], "*",
  "Groww IPO",
  "The online investment platform Groww's parent listed on 12 November 2025 at a premium of about 14% on the BSE after "
  "its IPO of 4-7 November. Lenskart had listed separately on 10 November 2025.",
  ["Parent: Billionbrains Garage Ventures", "Platform: Groww", "Listing: 12 Nov 2025"],
  [fact("Groww shares list at 14% premium on 12 Nov 2025", "groww_bt"),
   fact("A busy November: gains for Groww, Pine Labs and Lenskart", "groww_ys")],
  why="Zerodha and PhonePe are unlisted; Lenskart listed on its own.",
  current=ca("2025-11-12"))

G(T, MA, "Basic",
  "The Magnum Ice Cream Company, which completed its demerger from Unilever on 8 December 2025, has its primary listing "
  "in which city?",
  ["Amsterdam", "London", "New York", "Mumbai"], "*",
  "Magnum demerger",
  "Unilever completed the spin-off of its ice cream business on 8 December 2025. The Magnum Ice Cream Company listed "
  "on Euronext Amsterdam, with secondary listings in London and New York.",
  ["Demerger: 8 Dec 2025", "Primary listing: Amsterdam", "Secondary: London, New York"],
  [fact("Unilever completes ice cream demerger with Magnum set to list in Amsterdam", "magnum_star"),
   fact("Unilever completes demerger with Magnum set to list", "magnum_rte")],
  why="London and New York are secondary listings; Mumbai is where Kwality Wall's (India) listed.",
  current=ca("2025-12-08"))

G(T, MA, "Intermediate",
  "After Tata Motors' demerger, the commercial vehicles business listed separately on 12 November 2025. In what ratio "
  "did Tata Motors shareholders receive its shares?",
  ["1:1", "1:2", "2:1", "1:5"], "*",
  "Tata Motors demerger",
  "Shareholders on the record date of 14 October 2025 got one share of the commercial vehicles company for every Tata "
  "Motors share held. It listed at ₹335 on the NSE on 12 November 2025 and took the name Tata Motors Ltd; the passenger "
  "vehicle, EV and JLR business became Tata Motors Passenger Vehicles (TMPV).",
  ["Ratio: 1 CV share for 1 Tata Motors share", "Record date: 14 Oct 2025", "Listing: 12 Nov 2025 (₹335 on NSE)"],
  [fact("Tata Motors CV arm makes solid stock market debut on 12 Nov 2025", "tmcv_bt"),
   fact("Tata Motors CV shares close at ₹330 on listing day", "tmcv_bs")],
  why="The entitlement was one for one.",
  current=ca("2025-11-12"))

GS(T, MA, "Advanced", "MUFG's investment in Shriram Finance",
   ["MUFG Bank agreed to acquire a 20% stake in Shriram Finance for about ₹39,618 crore.",
    "It was described as the largest foreign direct investment in an Indian financial services company.",
    "The stake was acquired by buying shares from the existing promoters."],
   [True, True, False],
   "MUFG and Shriram Finance",
   "Shriram Finance's board approved the deal on 19 December 2025: MUFG Bank subscribed to new shares through a "
   "preferential issue for a 20% fully diluted stake for about ₹39,618 crore. It completed in April 2026 and MUFG can "
   "nominate two directors.",
   [fact("MUFG to invest ₹39,618 crore for 20% stake in Shriram Finance via preferential issue", "mufg_bs"),
    fact("MUFG's 20% stake in Shriram Finance is the biggest FDI in the Indian NBFC sector", "mufg_ml")],
   why="Statement 3 is wrong: the stake came through a preferential issue of new shares.",
   current=ca("2025-12-19"))

GS(T, MA, "Advanced", "the strategic sale of IDBI Bank approved in October 2026",
   ["The Cabinet Committee on Economic Affairs approved the sale of a 60.72% stake to a subsidiary of Fairfax "
    "Financial Holdings.",
    "The government is selling 30.48% and LIC is selling 30.24%.",
    "After the sale the government will hold 15% and LIC 19%."],
   [True, True, True],
   "IDBI Bank strategic sale",
   "On 14 October 2026 the CCEA approved selling 60.72% of IDBI Bank for ₹52,878 crore to a Canadian subsidiary of "
   "Fairfax Financial Holdings: 30.48% from the government and 30.24% from LIC. The government keeps 15% and LIC 19%. "
   "The transfer needs regulatory approvals, and the buyer must make an open offer.",
   [fact("CCEA approves 60.72% stake sale in IDBI Bank for ₹52,878 crore; govt 30.48%, LIC 30.24%; residual 15% and "
         "19%", "idbi_tt"),
    fact("IDBI Bank gets new owner as Fairfax wins 60.72% stake sale", "idbi_ol")],
   why="All three statements are correct.",
   current=ca("2026-10-14"))

GS(T, MA, "Advanced", "Blackstone's investment in Federal Bank",
   ["The Competition Commission of India rejected the proposal.",
    "A Blackstone affiliate is to acquire up to 9.99% through preferential equity shares and warrants worth about "
    "₹6,196.5 crore.",
    "The RBI approved the acquisition in February 2026."],
   [False, True, True],
   "Blackstone and Federal Bank",
   "Federal Bank's board approved the issue to a Blackstone affiliate in October 2025. The CCI approved it in December "
   "2025 and the RBI in February 2026. The affiliate gets a board nomination right after the warrants convert.",
   [fact("Federal Bank board approves 9.99% stake sale to Blackstone affiliate for ₹6,196.5 crore", "fed_week"),
    fact("CCI approves Blackstone-backed entity's acquisition in Federal Bank", "fed_livelaw"),
    fact("Blackstone's 9.99% stake in Federal Bank gets RBI green light", "fed_bt")],
   why="Statement 1 is wrong: the CCI approved the proposal.",
   current=ca("2026-02-05"))

GS(T, MA, "Advanced", "International Holding Company's (IHC) investment in Sammaan Capital",
   ["IHC, an Abu Dhabi-based group, is investing about USD 1 billion for a stake of over 40% in Sammaan Capital.",
    "IHC said that on completion it will be classified as a promoter of Sammaan Capital."],
   [True, True],
   "IHC and Sammaan Capital",
   "IHC said on 31 March 2026 that it had received all required regulatory approvals for its roughly USD 1 billion "
   "investment for about 41.5% of Sammaan Capital (formerly Indiabulls Housing Finance), after which it will be a "
   "promoter.",
   [fact("IHC advances USD 1 billion investment to acquire majority stake in India's Sammaan Capital; to be classified "
         "as promoter", "ihc_pr")],
   why="Both statements are correct.",
   current=ca("2026-03-31"))

GS(T, CP, "Advanced", "the IPO of ICICI Prudential Asset Management Company",
   ["The issue of about ₹10,602.65 crore was entirely an offer for sale.",
    "Its price band was ₹1,061 to ₹1,165 per share."],
   [True, False],
   "ICICI Prudential AMC IPO",
   "The IPO was open from 12 to 16 December 2025 at a price band of ₹2,061-2,165, as an offer for sale of 4.90 crore "
   "shares worth ₹10,602.65 crore; the shares listed on the BSE and NSE on 19 December 2025.",
   [fact("ICICI Prudential AMC IPO: ₹10,602.65 crore offer for sale; price band ₹2,061-2,165", "icicipru_chit"),
    fact("ICICI Prudential AMC set for listing on 19 December", "icicipru_hdfc")],
   why="Statement 2 is wrong: the price band was ₹2,061-2,165.",
   current=ca("2025-12-19"))

GS(T, CP, "Advanced", "Microsoft's investment announcement for India in December 2025",
   ["Microsoft pledged USD 17.5 billion for AI and cloud infrastructure in India.",
    "It was described as Microsoft's largest investment in Asia."],
   [True, True],
   "Microsoft in India",
   "On 9 December 2025 Microsoft pledged USD 17.5 billion for AI and cloud infrastructure in India, its largest "
   "investment in Asia, on top of USD 3 billion pledged earlier in 2025. Amazon followed a day later with a pledge of "
   "over USD 35 billion by 2030.",
   [fact("Amazon and Microsoft pledge over USD 52 billion for India", "msft_star"),
    fact("Microsoft's USD 17.5 billion India pledge is its largest in Asia", "msft_af")],
   why="Both statements are correct.",
   current=ca("2025-12-09"))

GS(T, MA, "Advanced", "Kwality Wall's (India) Limited",
   ["It listed on the BSE and NSE after Hindustan Unilever's ice cream business was demerged into it.",
    "HUL shareholders received one Kwality Wall's (India) share for every HUL share held.",
    "The Magnum Ice Cream Company acquired the Unilever group's 61.9% stake in it."],
   [True, True, True],
   "Kwality Wall's (India) demerger",
   "HUL demerged its ice cream business into Kwality Wall's (India) Ltd, which listed in February 2026; HUL holders as "
   "of 5 December 2025 got shares one for one. Magnum Ice Cream Company Holdco acquired Unilever's 61.9% stake, as "
   "the company disclosed on 30 March 2026.",
   [fact("Kwality Wall's India lists on BSE and NSE after HUL ice cream demerger; 1:1 entitlement", "kw_impact"),
    fact("Magnum Ice Cream acquires 61.9% stake in Kwality Wall's India, becomes promoter", "kw_ob")],
   why="All three statements are correct.",
   current=ca("2026-03-30"))

# ====================================================================== Static Awareness (0 / 1 / 1)
T = "Static Awareness"
CC = "Capitals and currencies"

G(T, CC, "Intermediate",
  "Prime Minister Modi received Ethiopia's highest honour in Addis Ababa in December 2025. What is the currency of "
  "Ethiopia?",
  ["Birr", "Nakfa", "Shilling", "Dinar"], "*",
  "Ethiopia",
  "Ethiopia's currency is the birr (ETB), issued by the National Bank of Ethiopia and divided into 100 santim. Addis "
  "Ababa is the capital and also hosts the African Union headquarters.",
  ["Currency: birr (ETB)", "Issuer: National Bank of Ethiopia"],
  [fact("Ethiopian birr (ETB) is the currency of Ethiopia", "birr_rb"),
   fact("Ethiopian birr issued by the National Bank of Ethiopia", "birr_ww")],
  why="The nakfa is Eritrea's currency; shillings are used in Kenya, Uganda, Tanzania and Somalia.")

GS(T, CC, "Advanced", "Jordan",
   ["Its capital is Amman.",
    "Its currency, the Jordanian dinar, is pegged to the US dollar.",
    "The Jordanian dinar is divided into 100 fils."],
   [True, True, False],
   "Jordan",
   "Amman is Jordan's capital and largest city. The Jordanian dinar (JOD), used since 1950 and pegged to the US dollar, "
   "is divided into 100 qirsh (piastres) or 1,000 fils, not 100 fils.",
   [fact("Jordanian dinar: pegged to the US dollar; divided into 100 qirsh or 1,000 fils; Amman capital",
         "jod_wiki")],
   why="Statement 3 is wrong: a dinar has 1,000 fils.")


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
    # no repeated stems or URLs used for unrelated facts by mistake: every URL key referenced exists (fact() asserts)
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
    "notes": "BATCH_003 General Awareness part: 150 original questions. Current-affairs topics (National and "
             "International Current Affairs, Appointments, Awards, Sports, Summits, Economic Affairs, Business) test "
             "events dated 2025-11-01 to 2026-11-04, with event dates from the sources and review_by 2027-05-05. "
             "Other time-sensitive facts also carry current_affairs dates. No fact or event tested in BATCH_000, "
             "BATCH_001 or BATCH_002 GA is tested again. Fact checks dated 2026-11-05; verified_by says whether each "
             "question's sources were opened (web:fact-check) or confirmed only in search results "
             "(web:search-confirmed). Pending human review.",
    "stimuli": [],
    "questions": questions,
}
out = ROOT / "batches" / "parts" / f"{BATCH}_GA.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(questions)} questions; keys {dict(sorted(keys.items()))})")
