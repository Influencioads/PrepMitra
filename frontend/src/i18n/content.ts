import { useCallback } from 'react';
import { useUiLang } from './index';

/**
 * Hindi for catalog content that arrives in English (exam/role names, descriptions, section
 * names, marking rules) — from the API or the demo catalog. The UI strings live in messages/*.
 * Lookup is by the exact English text, so it works for both data sources. Anything not listed
 * (e.g. a new exam added by the admin) falls back to the English text. Long term the backend
 * should return localized content (`?lang=hi`); this table is the stop-gap for launch.
 *
 * Exam names (SSC CGL, IBPS PO…) are proper nouns and stay as they are.
 */
const HI: Record<string, string> = {
  // ---- category labels / conducting bodies (API) ----
  'Campus and corporate hiring': 'कैंपस और कॉर्पोरेट हायरिंग',
  'Central government jobs': 'केंद्र सरकार की नौकरियाँ',

  'IT services hiring pattern': 'IT सर्विसेज़ हायरिंग पैटर्न',
  'Common aptitude pattern': 'सामान्य एप्टीट्यूड पैटर्न',

  // ---- topics (sample questions, progress charts) ----
  Analogy: 'सादृश्य',
  'Reading Comprehension': 'रीडिंग कॉम्प्रिहेंशन',
  'Idioms and Phrases': 'मुहावरे और वाक्यांश',
  'Compound Interest': 'चक्रवृद्धि ब्याज',
  Averages: 'औसत',
  'Error Spotting': 'त्रुटि पहचान',
  'Blood Relations': 'रक्त संबंध',
  'Sentence Improvement': 'वाक्य सुधार',
  'Time and Work': 'समय और कार्य',
  'Seating Arrangement': 'बैठक व्यवस्था',
  'Profit and Loss': 'लाभ और हानि',
  'Time Speed Distance': 'समय, गति और दूरी',
  'Direction Sense': 'दिशा ज्ञान',
  Science: 'विज्ञान',
  History: 'इतिहास',
  Antonyms: 'विलोम शब्द',
  'Indian Polity': 'भारतीय राजव्यवस्था',
  'Number system': 'संख्या पद्धति',
  'Analogy and classification': 'सादृश्य और वर्गीकरण',
  'Reading comprehension': 'रीडिंग कॉम्प्रिहेंशन',
  Percentages: 'प्रतिशत',
  'Profit and loss': 'लाभ और हानि',
  'Time and work': 'समय और कार्य',
  'Seating arrangement': 'बैठक व्यवस्था',
  Syllogism: 'न्याय निगमन (सिलोजिज़्म)',

  // ---- section names ----
  'General Intelligence & Reasoning': 'सामान्य बुद्धि और रीज़निंग',
  'General Intelligence and Reasoning': 'सामान्य बुद्धि और रीज़निंग',
  'General Intelligence': 'सामान्य बुद्धि',
  'General Awareness': 'सामान्य जागरूकता',
  'Quantitative Aptitude': 'मात्रात्मक योग्यता',
  'Quantitative aptitude': 'मात्रात्मक योग्यता',
  'Quantitative Ability': 'मात्रात्मक क्षमता',
  'English Comprehension': 'अंग्रेज़ी बोध',
  'English Language': 'अंग्रेज़ी भाषा',
  English: 'अंग्रेज़ी',
  Mathematics: 'गणित',
  Reasoning: 'रीज़निंग',
  'Reasoning Ability': 'रीज़निंग क्षमता',
  'Numerical Ability': 'संख्यात्मक क्षमता',
  'Data Analysis & Interpretation': 'डेटा एनालिसिस और इंटरप्रिटेशन',
  'Reasoning & Computer Aptitude': 'रीज़निंग और कंप्यूटर एप्टीट्यूड',
  'Reasoning Ability & Computer Aptitude': 'रीज़निंग क्षमता और कंप्यूटर एप्टीट्यूड',
  'Computer Knowledge': 'कंप्यूटर ज्ञान',
  'General English': 'सामान्य अंग्रेज़ी',
  'General/ Financial Awareness': 'सामान्य / वित्तीय जागरूकता',
  'General Awareness/ Economy/ Banking Knowledge': 'सामान्य जागरूकता / अर्थव्यवस्था / बैंकिंग ज्ञान',
  'General/ Economy/ Banking Awareness/ Digital/ Financial Awareness including RBI circulars':
    'सामान्य / अर्थव्यवस्था / बैंकिंग / डिजिटल / वित्तीय जागरूकता (RBI सर्कुलर सहित)',
  'English Language (or Hindi Language - candidate opts one)': 'अंग्रेज़ी भाषा (या हिंदी भाषा — उम्मीदवार एक चुनता है)',
  'Prelims mock based on the SBI Junior Associate (Customer Support and Sales) pattern: 100 questions in 60 minutes with sectional timing.':
    'SBI जूनियर एसोसिएट (कस्टमर सपोर्ट और सेल्स) पैटर्न पर प्रीलिम्स मॉक: 60 मिनट में 100 प्रश्न, सेक्शनल टाइमिंग के साथ।',
  'Regional Rural Bank Officer Scale I prelims mock: 80 questions, 80 marks, 45 minutes across reasoning and quantitative aptitude.':
    'क्षेत्रीय ग्रामीण बैंक ऑफ़िसर स्केल I प्रीलिम्स मॉक: 80 प्रश्न, 80 अंक, 45 मिनट — रीज़निंग और मात्रात्मक योग्यता।',
  'Regional Rural Bank Office Assistant (Multipurpose) prelims mock: 80 questions, 80 marks, 45 minutes across reasoning and numerical ability.':
    'क्षेत्रीय ग्रामीण बैंक ऑफ़िस असिस्टेंट (मल्टीपर्पज़) प्रीलिम्स मॉक: 80 प्रश्न, 80 अंक, 45 मिनट — रीज़निंग और संख्यात्मक क्षमता।',
  'IBPS PO Mains mock: 170 questions, 200 marks, 160 minutes with sectional timing, including banking and financial awareness and data analysis.':
    'IBPS PO मेन्स मॉक: 170 प्रश्न, 200 अंक, 160 मिनट, सेक्शनल टाइमिंग — बैंकिंग और वित्तीय जागरूकता तथा डेटा एनालिसिस सहित।',
  'SBI PO Mains mock: 170 questions, 200 marks, 180 minutes with sectional timing, including reasoning and computer aptitude and data analysis.':
    'SBI PO मेन्स मॉक: 170 प्रश्न, 200 अंक, 180 मिनट, सेक्शनल टाइमिंग — रीज़निंग और कंप्यूटर एप्टीट्यूड तथा डेटा एनालिसिस सहित।',
  'IBPS CSA (Clerk) Mains mock: 160 questions, 200 marks, 125 minutes with sectional timing across awareness, English, reasoning and quant.':
    'IBPS CSA (क्लर्क) मेन्स मॉक: 160 प्रश्न, 200 अंक, 125 मिनट, सेक्शनल टाइमिंग — जागरूकता, अंग्रेज़ी, रीज़निंग और क्वांट।',
  'SBI Junior Associate (Clerk) Mains mock: 190 questions, 200 marks, 160 minutes with sectional timing across awareness, English, quant and reasoning with computer aptitude.':
    'SBI जूनियर एसोसिएट (क्लर्क) मेन्स मॉक: 190 प्रश्न, 200 अंक, 160 मिनट, सेक्शनल टाइमिंग — जागरूकता, अंग्रेज़ी, क्वांट और रीज़निंग के साथ कंप्यूटर एप्टीट्यूड।',
  'IBPS RRB Officer Scale I Mains mock: 200 questions, 200 marks, 120 minutes with sectional timing, including computer knowledge and general awareness.':
    'IBPS RRB ऑफ़िसर स्केल I मेन्स मॉक: 200 प्रश्न, 200 अंक, 120 मिनट, सेक्शनल टाइमिंग — कंप्यूटर ज्ञान और सामान्य जागरूकता सहित।',
  'IBPS RRB Office Assistant Mains mock: 200 questions, 200 marks, 120 minutes with sectional timing, including computer knowledge and general awareness.':
    'IBPS RRB ऑफ़िस असिस्टेंट मेन्स मॉक: 200 प्रश्न, 200 अंक, 120 मिनट, सेक्शनल टाइमिंग — कंप्यूटर ज्ञान और सामान्य जागरूकता सहित।',
  'General Studies I': 'सामान्य अध्ययन I',
  'CSAT (Aptitude)': 'CSAT (एप्टीट्यूड)',
  VARC: 'VARC (वर्बल और रीडिंग)',
  DILR: 'DILR (डेटा और लॉजिकल रीज़निंग)',
  'General Aptitude': 'सामान्य एप्टीट्यूड',
  'Computer Science': 'कंप्यूटर साइंस',
  'Electronics & Communication': 'इलेक्ट्रॉनिक्स और कम्युनिकेशन',
  'Language Comprehension': 'भाषा बोध',
  'Reasoning & Quant': 'रीज़निंग और क्वांट',
  'Logical Reasoning': 'लॉजिकल रीज़निंग',
  'Logical reasoning': 'लॉजिकल रीज़निंग',
  'Verbal Ability': 'वर्बल एबिलिटी',
  'Verbal ability': 'वर्बल एबिलिटी',
  'Programming Logic': 'प्रोग्रामिंग लॉजिक',

  // ---- exam names that are descriptive, not proper nouns ----
  'Free Mini Mock - General Aptitude': 'फ़्री मिनी मॉक - सामान्य एप्टीट्यूड',
  'General Aptitude Mini Mock': 'सामान्य एप्टीट्यूड मिनी मॉक',
  'Campus Placement Aptitude (IT services)': 'कैंपस प्लेसमेंट एप्टीट्यूड (IT सर्विसेज़)',
  'IT Services Placement Aptitude Test': 'IT सर्विसेज़ प्लेसमेंट एप्टीट्यूड टेस्ट',
  'IT Placement': 'IT प्लेसमेंट',

  // ---- exam descriptions (API) ----
  'A free 30-minute mock with a full AI report, to see how PrepMitra works.':
    '30 मिनट का फ़्री मॉक, पूरी AI रिपोर्ट के साथ — देखें PrepMitra कैसे काम करता है।',
  'Placement-style aptitude test used by IT services companies (no negative marking).':
    'IT सर्विसेज़ कंपनियों का प्लेसमेंट-स्टाइल एप्टीट्यूड टेस्ट (कोई नेगेटिव मार्किंग नहीं)।',
  'Mock test based on the IBPS PO preliminary exam pattern.': 'IBPS PO प्रारंभिक परीक्षा पैटर्न पर आधारित मॉक टेस्ट।',
  'Mock test based on the SSC CGL Tier-1 pattern: 100 questions, 200 marks, 60 minutes.':
    'SSC CGL Tier-1 पैटर्न पर आधारित मॉक टेस्ट: 100 प्रश्न, 200 अंक, 60 मिनट।',
  // ---- exam descriptions (demo catalog) ----
  'Full-length mock based on the SSC Combined Graduate Level Tier 1 pattern covering reasoning, general awareness, quantitative aptitude and English comprehension.':
    'SSC CGL Tier 1 पैटर्न पर आधारित फ़ुल-लेंथ मॉक — रीज़निंग, सामान्य जागरूकता, मात्रात्मक योग्यता और अंग्रेज़ी बोध।',
  'Practice paper following the SSC Combined Higher Secondary Level Tier 1 structure for LDC, JSA and DEO aspirants.':
    'LDC, JSA और DEO उम्मीदवारों के लिए SSC CHSL Tier 1 ढाँचे पर अभ्यास पेपर।',
  'Computer-based test practice based on the Railway Recruitment Board NTPC CBT-1 pattern with mathematics, reasoning and general awareness.':
    'RRB NTPC CBT-1 पैटर्न पर कंप्यूटर-आधारित अभ्यास — गणित, रीज़निंग और सामान्य जागरूकता।',
  'Speed-focused prelims mock based on the IBPS Probationary Officer pattern with sectional timing for English, quant and reasoning.':
    'IBPS PO पैटर्न पर स्पीड वाला प्रीलिम्स मॉक — अंग्रेज़ी, क्वांट और रीज़निंग की सेक्शनल टाइमिंग के साथ।',
  'Prelims practice based on the IBPS Clerk pattern with emphasis on accuracy under strict sectional timing.':
    'IBPS Clerk पैटर्न पर प्रीलिम्स अभ्यास — सख़्त सेक्शनल टाइमिंग में सटीकता पर ज़ोर।',
  'High-difficulty prelims mock modelled on the SBI Probationary Officer pattern, including data interpretation and arrangement puzzles.':
    'SBI PO पैटर्न पर कठिन प्रीलिम्स मॉक — डेटा इंटरप्रिटेशन और अरेंजमेंट पज़ल सहित।',
  'Civil Services Preliminary mock with General Studies Paper I and CSAT Paper II questions, including negative-marking risk analysis.':
    'सिविल सेवा प्रारंभिक मॉक — GS पेपर I और CSAT पेपर II, नेगेटिव मार्किंग जोखिम विश्लेषण के साथ।',
  'MBA entrance mock following the CAT structure: Verbal Ability & Reading Comprehension, Data Interpretation & Logical Reasoning, and Quantitative Ability.':
    'CAT ढाँचे पर MBA प्रवेश मॉक: VARC, DILR और मात्रात्मक क्षमता।',
  'GATE CS mock with General Aptitude plus core computer science: algorithms, data structures, OS, DBMS, networks and theory of computation.':
    'GATE CS मॉक — सामान्य एप्टीट्यूड और कोर कंप्यूटर साइंस: एल्गोरिद्म, डेटा स्ट्रक्चर, OS, DBMS, नेटवर्क और थ्योरी ऑफ़ कंप्यूटेशन।',
  'GATE EC mock covering networks, signals and systems, analog and digital electronics, and communication alongside General Aptitude.':
    'GATE EC मॉक — नेटवर्क, सिग्नल और सिस्टम, एनालॉग और डिजिटल इलेक्ट्रॉनिक्स, कम्युनिकेशन और सामान्य एप्टीट्यूड।',
  'Postgraduate entrance mock with language comprehension, general awareness, reasoning and quantitative aptitude.':
    'पोस्टग्रेजुएट प्रवेश मॉक — भाषा बोध, सामान्य जागरूकता, रीज़निंग और मात्रात्मक योग्यता।',
  'A 30-minute mini mock covering quantitative aptitude, logical reasoning and verbal ability. Free for every new user, with a full report.':
    '30 मिनट का मिनी मॉक — मात्रात्मक योग्यता, लॉजिकल रीज़निंग और वर्बल एबिलिटी। हर नए यूज़र के लिए फ़्री, पूरी रिपोर्ट के साथ।',
  'Placement-style test modelled on common IT services hiring rounds: numerical ability, logical reasoning, verbal ability and programming logic.':
    'IT सर्विसेज़ हायरिंग राउंड जैसा प्लेसमेंट टेस्ट: संख्यात्मक क्षमता, लॉजिकल रीज़निंग, वर्बल एबिलिटी और प्रोग्रामिंग लॉजिक।',

  // ---- marking rules (demo catalog; API ones are generated, see below) ----
  'No negative marking': 'कोई नेगेटिव मार्किंग नहीं',
  '0.50 marks deducted for each wrong answer': 'हर गलत उत्तर पर 0.50 अंक कटेंगे',
  '0.25 marks deducted for each wrong answer': 'हर गलत उत्तर पर 0.25 अंक कटेंगे',
  '1/3 mark deducted for each wrong answer': 'हर गलत उत्तर पर 1/3 अंक कटेगा',
  'One-third of the question’s marks deducted for each wrong answer': 'हर गलत उत्तर पर प्रश्न के अंकों का एक-तिहाई कटेगा',
  '−1 for wrong MCQs; no negative marking on numeric (TITA) answers': 'गलत MCQ पर −1; न्यूमेरिक (TITA) उत्तरों पर कोई नेगेटिव मार्किंग नहीं',
  '1/3 negative for MCQs only; no negative marking for MSQ and NAT': 'सिर्फ़ MCQ पर 1/3 नेगेटिव; MSQ और NAT पर कोई नेगेटिव मार्किंग नहीं',
  '+4 for correct, −1 for wrong': 'सही पर +4, गलत पर −1',
  'One quarter of the marks for the question deducted for each wrong answer': 'हर गलत उत्तर पर उस प्रश्न के अंकों का एक-चौथाई कटेगा',

  // ---- interview roles (API) ----
  'Bank PO interview': 'Bank PO इंटरव्यू',
  'Software developer (fresher)': 'सॉफ़्टवेयर डेवलपर (फ़्रेशर)',
  'Realistic Bank PO interview mock interview: introduction, resume, role, situational and HR rounds.':
    'Bank PO का असली जैसा मॉक इंटरव्यू: परिचय, रिज़्यूमे, भूमिका, सिचुएशनल और HR राउंड।',
  'Realistic Software developer (fresher) mock interview: introduction, resume, role, situational and HR rounds.':
    'सॉफ़्टवेयर डेवलपर (फ़्रेशर) का असली जैसा मॉक इंटरव्यू: परिचय, रिज़्यूमे, भूमिका, सिचुएशनल और HR राउंड।',
  'Role knowledge': 'भूमिका की जानकारी',
  'Answer structure': 'उत्तर की संरचना',
  Communication: 'संवाद',
  Confidence: 'आत्मविश्वास',
  'Resume consistency': 'रिज़्यूमे से मेल',
  // ---- interview roles (demo catalog) ----
  Jobs: 'नौकरियाँ',
  'IT & Technology': 'IT और टेक्नोलॉजी',
  Banking: 'बैंकिंग',
  'Human Resources': 'मानव संसाधन',
  Sales: 'सेल्स',
  Finance: 'फ़ाइनेंस',
  'Civil Services': 'सिविल सेवा',
  'Software Developer — Fresher': 'सॉफ़्टवेयर डेवलपर — फ़्रेशर',
  'Software Developer': 'सॉफ़्टवेयर डेवलपर',
  'Bank PO Interview': 'Bank PO इंटरव्यू',
  'HR Executive': 'HR एग्ज़ीक्यूटिव',
  'Sales and Business Development': 'सेल्स और बिज़नेस डेवलपमेंट',
  'Sales & BD': 'सेल्स और BD',
  'Accountant / Financial Analyst': 'अकाउंटेंट / फ़ाइनेंशियल एनालिस्ट',
  Accountant: 'अकाउंटेंट',
  'Civil Services Personality Test': 'सिविल सेवा पर्सनैलिटी टेस्ट',
  'UPSC Personality Test': 'UPSC पर्सनैलिटी टेस्ट',
  'Campus-style technical interview covering programming fundamentals, a project deep-dive, problem-solving and HR questions.':
    'कैंपस-स्टाइल टेक्निकल इंटरव्यू: प्रोग्रामिंग की बुनियाद, प्रोजेक्ट पर गहराई से सवाल, प्रॉब्लम-सॉल्विंग और HR प्रश्न।',
  'Panel-style interview for probationary officer roles: banking awareness, current affairs, situational judgement and motivation.':
    'प्रोबेशनरी ऑफ़िसर के लिए पैनल इंटरव्यू: बैंकिंग जागरूकता, करेंट अफ़ेयर्स, सिचुएशनल जजमेंट और प्रेरणा।',
  'Interview for HR generalist roles covering recruitment, employee relations, labour-law basics and conflict handling.':
    'HR जनरलिस्ट भूमिका का इंटरव्यू: भर्ती, कर्मचारी संबंध, श्रम क़ानून की बुनियाद और विवाद सुलझाना।',
  'Sales interview focusing on prospecting, objection handling, target ownership and a live pitch exercise.':
    'सेल्स इंटरव्यू: प्रॉस्पेक्टिंग, आपत्तियों का जवाब, टारगेट की ज़िम्मेदारी और लाइव पिच।',
  'Finance interview on accounting principles, GST basics, financial statements, Excel modelling and analytical thinking.':
    'फ़ाइनेंस इंटरव्यू: अकाउंटिंग सिद्धांत, GST की बुनियाद, फ़ाइनेंशियल स्टेटमेंट, Excel मॉडलिंग और विश्लेषण।',
  'Board-style personality test simulation exploring your background, optional subject, ethics, governance and current affairs.':
    'बोर्ड-स्टाइल पर्सनैलिटी टेस्ट: आपकी पृष्ठभूमि, वैकल्पिक विषय, नैतिकता, शासन और करेंट अफ़ेयर्स।',
  'DSA and OOP fundamentals': 'DSA और OOP की बुनियाद',
  'Project ownership': 'प्रोजेक्ट की ज़िम्मेदारी',
  'Problem-solving approach': 'प्रॉब्लम-सॉल्विंग का तरीक़ा',
  'Banking awareness': 'बैंकिंग जागरूकता',
  'Customer orientation': 'ग्राहक-केंद्रित सोच',
  'Situational judgement': 'सिचुएशनल जजमेंट',
  'Clarity of motivation': 'प्रेरणा की स्पष्टता',
  'HR process knowledge': 'HR प्रक्रियाओं की जानकारी',
  'Empathy and judgement': 'सहानुभूति और विवेक',
  'Structured answers': 'संरचित उत्तर',
  Persuasion: 'समझाने की क्षमता',
  'Target orientation': 'टारगेट पर फ़ोकस',
  'Objection handling': 'आपत्तियों का जवाब',
  'Accounting concepts': 'अकाउंटिंग कॉन्सेप्ट',
  'Analytical reasoning': 'विश्लेषणात्मक सोच',
  'Attention to detail': 'बारीकी पर ध्यान',
  'Balanced opinions': 'संतुलित राय',
  'Ethical reasoning': 'नैतिक तर्क',
  'Awareness of governance': 'शासन की समझ',
  Composure: 'संयम',
};

/** Translates one piece of catalog content; generated marking rules are handled by pattern. */
export function contentText(text: string, lang: 'en' | 'hi'): string {
  if (lang === 'en' || !text) return text;
  const hit = HI[text];
  if (hit) return hit;
  const pattern = /^(.+) pattern$/.exec(text);
  if (pattern) return `${pattern[1]} पैटर्न`;
  const neg = /^−([\d.]+) per wrong answer$/.exec(text);
  if (neg) return `हर गलत उत्तर पर −${neg[1]}`;
  return text;
}

/** `const ct = useContentT(); ct(exam.description)` */
export function useContentT() {
  const lang = useUiLang();
  return useCallback((text: string) => contentText(text, lang), [lang]);
}
