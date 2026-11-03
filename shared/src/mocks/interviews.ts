import { liveCatalog } from '../api/live';
import type { InterviewRole, LanguageCode, ScriptedQuestion } from '../types/core';
import { TIER1_LANGUAGES } from '../constants';

const T1 = TIER1_LANGUAGES as LanguageCode[];

export const INTERVIEW_ROLES: InterviewRole[] = [
  {
    id: 'software-developer',
    title: 'Software Developer — Fresher',
    shortTitle: 'Software Developer',
    category: 'IT & Technology',
    icon: 'code',
    description:
      'Campus-style technical interview covering programming fundamentals, a project deep-dive, problem-solving and HR questions.',
    levels: ['fresher', '1-3'],
    durationMin: 25,
    questionCount: 9,
    evaluates: ['DSA and OOP fundamentals', 'Project ownership', 'Problem-solving approach', 'Communication'],
    themes: ['OOP', 'Data structures', 'Projects', 'Debugging', 'Teamwork'],
    languages: T1,
    voiceAvailable: true,
    creditCost: 1,
    status: 'published',
    popularity: 97,
  },
  {
    id: 'bank-po',
    title: 'Bank PO Interview',
    shortTitle: 'Bank PO',
    category: 'Banking',
    icon: 'banknote',
    description:
      'Panel-style interview for probationary officer roles: banking awareness, current affairs, situational judgement and motivation.',
    levels: ['fresher', '1-3'],
    durationMin: 20,
    questionCount: 9,
    evaluates: ['Banking awareness', 'Customer orientation', 'Situational judgement', 'Clarity of motivation'],
    themes: ['Banking terms', 'RBI policy', 'Financial inclusion', 'Customer handling'],
    languages: T1,
    voiceAvailable: true,
    creditCost: 1,
    status: 'published',
    popularity: 90,
  },
  {
    id: 'hr-executive',
    title: 'HR Executive',
    shortTitle: 'HR Executive',
    category: 'Human Resources',
    icon: 'users',
    description:
      'Interview for HR generalist roles covering recruitment, employee relations, labour-law basics and conflict handling.',
    levels: ['fresher', '1-3', '3-5'],
    durationMin: 20,
    questionCount: 9,
    evaluates: ['HR process knowledge', 'Empathy and judgement', 'Structured answers', 'Confidence'],
    themes: ['Recruitment', 'Onboarding', 'Grievances', 'Policies'],
    languages: T1,
    voiceAvailable: true,
    creditCost: 1,
    status: 'published',
    popularity: 78,
  },
  {
    id: 'sales-bd',
    title: 'Sales and Business Development',
    shortTitle: 'Sales & BD',
    category: 'Sales',
    icon: 'trending',
    description:
      'Sales interview focusing on prospecting, objection handling, target ownership and a live pitch exercise.',
    levels: ['fresher', '1-3', '3-5'],
    durationMin: 20,
    questionCount: 9,
    evaluates: ['Persuasion', 'Target orientation', 'Objection handling', 'Communication'],
    themes: ['Pitching', 'Negotiation', 'Pipeline', 'CRM discipline'],
    languages: T1,
    voiceAvailable: true,
    creditCost: 1,
    status: 'published',
    popularity: 82,
  },
  {
    id: 'accountant',
    title: 'Accountant / Financial Analyst',
    shortTitle: 'Accountant',
    category: 'Finance',
    icon: 'calculator',
    description:
      'Finance interview on accounting principles, GST basics, financial statements, Excel modelling and analytical thinking.',
    levels: ['fresher', '1-3', '3-5'],
    durationMin: 25,
    questionCount: 9,
    evaluates: ['Accounting concepts', 'Analytical reasoning', 'Attention to detail', 'Answer structure'],
    themes: ['Financial statements', 'GST', 'Reconciliation', 'Excel'],
    languages: T1,
    voiceAvailable: true,
    creditCost: 1,
    status: 'published',
    popularity: 75,
  },
  {
    id: 'civil-services-pt',
    title: 'Civil Services Personality Test',
    shortTitle: 'UPSC Personality Test',
    category: 'Civil Services',
    icon: 'scale',
    description:
      'Board-style personality test simulation exploring your background, optional subject, ethics, governance and current affairs.',
    levels: ['fresher', '1-3', '3-5'],
    durationMin: 30,
    questionCount: 9,
    evaluates: ['Balanced opinions', 'Ethical reasoning', 'Awareness of governance', 'Composure'],
    themes: ['DAF-based questions', 'Ethics', 'Governance', 'Current affairs'],
    languages: ['en', 'hi'],
    voiceAvailable: true,
    creditCost: 2,
    status: 'published',
    popularity: 85,
  },
];

const intro = (role: string): ScriptedQuestion => ({
  id: 'intro',
  stage: 'introduction',
  text: `Welcome! Let’s begin. Please introduce yourself and tell me why you are interested in this ${role} role.`,
  keywords: ['background', 'experience', 'interested', 'skills', 'because', 'project', 'degree'],
  modelAnswer:
    'Start with one line on your education, follow with two relevant achievements or experiences, and close with a specific reason this role matches your strengths and goals. Keep it under 90 seconds.',
  followUp: {
    trigger: ['project', 'internship'],
    text: 'You mentioned a project or internship. What was the single hardest problem you solved there, and how?',
  },
});

const closing: ScriptedQuestion = {
  id: 'closing',
  stage: 'closing',
  text: 'Thank you. Before we wrap up, do you have any questions for us?',
  keywords: ['team', 'growth', 'learning', 'expect', 'success', 'role'],
  modelAnswer:
    'Ask one or two thoughtful questions, for example: “What would success look like in the first 90 days?” or “How does the team support learning for new joiners?”',
};

export const INTERVIEW_SCRIPTS: Record<string, ScriptedQuestion[]> = {
  'software-developer': [
    intro('software developer'),
    {
      id: 'sd-resume', stage: 'resume',
      text: 'Walk me through the most significant project on your resume. What was your exact contribution?',
      keywords: ['built', 'designed', 'api', 'database', 'react', 'team', 'deployed', 'users', 'responsible'],
      modelAnswer:
        'Use STAR: “In my final-year project (Situation) I built a library management API (Task). I designed the PostgreSQL schema and wrote the REST endpoints in Node.js, adding caching that cut response times by 40% (Action). It was used by 300 students in our college (Result).”',
      followUp: { trigger: ['database', 'api', 'sql'], text: 'How did you design the database schema, and what would you change now?' },
    },
    {
      id: 'sd-oop', stage: 'technical',
      text: 'Explain the difference between an abstract class and an interface. When would you use each?',
      keywords: ['abstract', 'interface', 'implementation', 'multiple', 'inheritance', 'contract', 'method'],
      modelAnswer:
        'An interface defines a contract with no state; a class can implement many. An abstract class can hold shared state and partial implementation but supports single inheritance. Use interfaces for capabilities (e.g. Comparable) and abstract classes for a common base with shared code.',
    },
    {
      id: 'sd-dsa', stage: 'technical',
      text: 'How would you detect a cycle in a linked list? What is the time and space complexity?',
      keywords: ['floyd', 'slow', 'fast', 'pointer', 'o(n)', 'o(1)', 'hash'],
      modelAnswer:
        'Use Floyd’s tortoise-and-hare: move a slow pointer one step and a fast pointer two steps; if they meet there is a cycle. Time O(n), space O(1). A hash set also works in O(n) time but O(n) space.',
      followUp: { trigger: ['hash', 'set'], text: 'Can you do it without extra memory?' },
    },
    {
      id: 'sd-situational', stage: 'situational',
      text: 'Tell me about a time a bug reached production or a demo. How did you handle it?',
      keywords: ['root cause', 'fixed', 'tested', 'communicated', 'learned', 'logs', 'rollback'],
      modelAnswer:
        'Describe the impact, how you reproduced it with logs, the fix and rollback plan, how you communicated with the team, and the test you added so it never recurred.',
    },
    {
      id: 'sd-hr', stage: 'hr',
      text: 'Where do you see yourself in three years, and how does this role help you get there?',
      keywords: ['grow', 'learn', 'lead', 'skills', 'contribute', 'ownership'],
      modelAnswer:
        'Show ambition aligned with the company: “In three years I want to own a module end-to-end and mentor new joiners. This role’s exposure to production systems is the fastest path to that.”',
    },
    {
      id: 'sd-sql', stage: 'technical',
      text: 'Write the idea of a SQL query to find the second-highest salary from an Employees table. What edge cases would you handle?',
      keywords: ['distinct', 'order by', 'limit', 'offset', 'max', 'subquery', 'null', 'duplicate'],
      modelAnswer:
        'Use SELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees), or SELECT DISTINCT salary ORDER BY salary DESC LIMIT 1 OFFSET 1. Handle duplicates with DISTINCT and return NULL when there is no second salary.',
      followUp: { trigger: ['limit', 'offset'], text: 'How would you find the Nth highest salary for any N, and how does it perform on a large table?' },
    },
    {
      id: 'sd-team', stage: 'situational',
      text: 'A teammate keeps pushing code without tests and it breaks the build. How would you handle it?',
      keywords: ['talk', 'privately', 'understand', 'ci', 'review', 'help', 'process', 'team'],
      modelAnswer:
        'Speak to them privately first to understand the reason, offer to pair on writing tests, and suggest a team-level fix such as required CI checks and pull-request reviews, so it becomes a process improvement rather than a personal complaint.',
    },
    closing,
  ],
  'bank-po': [
    intro('Bank PO'),
    {
      id: 'po-why', stage: 'resume',
      text: 'You have a background that is not in finance. Why do you want to join banking?',
      keywords: ['stability', 'customers', 'financial inclusion', 'growth', 'serve', 'economy', 'rural'],
      modelAnswer:
        'Connect your background to banking: analytical skills from your degree, interest in financial inclusion, and the PO role’s exposure to credit, operations and customer service across branches.',
    },
    {
      id: 'po-repo', stage: 'technical',
      text: 'What is the repo rate, and how does a change in it affect customers?',
      keywords: ['rbi', 'lend', 'banks', 'loan', 'emi', 'inflation', 'interest'],
      modelAnswer:
        'The repo rate is the rate at which the RBI lends short-term funds to banks. When it rises, banks’ cost of funds rises, so loan EMIs usually increase and deposit rates may rise; it is used to control inflation.',
      followUp: { trigger: ['inflation'], text: 'What other tools does the RBI use to control inflation?' },
    },
    {
      id: 'po-npa', stage: 'technical',
      text: 'What is an NPA, and what steps can a branch take to reduce it?',
      keywords: ['90 days', 'non-performing', 'recovery', 'monitoring', 'restructuring', 'sarfaesi'],
      modelAnswer:
        'An NPA is a loan whose interest or principal is overdue for more than 90 days. Branches can reduce NPAs through careful credit appraisal, early-warning monitoring, follow-ups, restructuring and recovery under SARFAESI where appropriate.',
    },
    {
      id: 'po-situational', stage: 'situational',
      text: 'An elderly customer is upset because their pension has not been credited. How would you handle this at the branch?',
      keywords: ['listen', 'calm', 'check', 'escalate', 'update', 'empathy', 'resolve'],
      modelAnswer:
        'Listen calmly, apologise for the inconvenience, check the transaction status and the pension disbursing authority, escalate if needed, give a clear timeline and follow up personally.',
    },
    {
      id: 'po-hr', stage: 'hr',
      text: 'Are you comfortable being posted in a rural branch?',
      keywords: ['yes', 'learn', 'financial inclusion', 'adapt', 'experience', 'serve'],
      modelAnswer:
        'Yes — a rural posting gives direct exposure to priority-sector lending and financial inclusion, and teaches adaptability, which are valuable for a long banking career.',
    },
    {
      id: 'po-digital', stage: 'technical',
      text: 'What is UPI, and how has it changed banking for small businesses in India?',
      keywords: ['npci', 'real-time', 'qr', 'merchant', 'interoperable', 'low cost', 'credit history', 'cash'],
      modelAnswer:
        'UPI, run by NPCI, enables instant, interoperable bank-to-bank payments through a mobile app or QR code. It lets small merchants accept digital payments at almost no cost, reduces cash handling, and creates a transaction history banks can use to offer them credit.',
      followUp: { trigger: ['fraud', 'security'], text: 'What would you tell a customer who has lost money to a UPI fraud?' },
    },
    {
      id: 'po-target', stage: 'situational',
      text: 'Your branch manager asks you to push an insurance product to customers who may not need it, to meet a target. What would you do?',
      keywords: ['customer', 'suitability', 'needs', 'ethics', 'mis-selling', 'explain', 'manager', 'rbi'],
      modelAnswer:
        'Meet the target ethically: identify customers for whom the product genuinely suits their needs, explain terms clearly, and avoid mis-selling. Politely share with the manager that mis-selling creates complaints and regulatory risk, and propose a better-targeted outreach plan.',
    },
    closing,
  ],
  'hr-executive': [
    intro('HR executive'),
    {
      id: 'hr-recruit', stage: 'resume',
      text: 'Describe the end-to-end recruitment process you have followed or would follow for a role.',
      keywords: ['job description', 'sourcing', 'screening', 'interview', 'offer', 'onboarding', 'stakeholder'],
      modelAnswer:
        'Align with the hiring manager on the JD, source candidates through job portals and referrals, screen, coordinate interviews with a structured scorecard, roll out the offer, and manage onboarding with clear first-week plans.',
    },
    {
      id: 'hr-law', stage: 'technical',
      text: 'What are the key components of a salary structure in India?',
      keywords: ['basic', 'hra', 'pf', 'gratuity', 'allowance', 'ctc', 'esi'],
      modelAnswer:
        'Basic pay, HRA, special allowances, employer PF contribution, gratuity, ESI where applicable, and variable pay. CTC includes employer contributions; take-home excludes deductions like PF and professional tax.',
    },
    {
      id: 'hr-conflict', stage: 'situational',
      text: 'Two team members have a conflict that is affecting deliverables. How would you resolve it?',
      keywords: ['listen', 'separately', 'neutral', 'facts', 'mediate', 'agreement', 'follow up'],
      modelAnswer:
        'Speak to each person separately, gather facts, hold a mediated conversation focused on shared goals, agree on specific actions, and follow up after two weeks to check progress.',
      followUp: { trigger: ['manager', 'escalate'], text: 'At what point would you escalate to their manager, and why?' },
    },
    {
      id: 'hr-attrition', stage: 'technical',
      text: 'Attrition in a sales team has reached 35%. What would you analyse first?',
      keywords: ['exit interview', 'data', 'manager', 'compensation', 'engagement', 'tenure'],
      modelAnswer:
        'Segment attrition by tenure, manager and location, review exit interviews, compare pay with the market, and run a quick engagement pulse. Then prioritise two or three actions with measurable targets.',
    },
    {
      id: 'hr-hr', stage: 'hr',
      text: 'What is your biggest weakness, and what are you doing about it?',
      keywords: ['improving', 'learning', 'feedback', 'practice', 'course', 'example'],
      modelAnswer:
        'Pick a genuine but non-critical weakness, give an example, and show concrete steps you are taking — for example, “I used to avoid public speaking, so I now present our weekly report and have joined a Toastmasters club.”',
    },
    {
      id: 'hr-onboard', stage: 'technical',
      text: 'How would you design the first week of onboarding for a new sales hire?',
      keywords: ['buddy', 'manager', 'goals', 'training', 'tools', 'policies', 'feedback', 'checklist'],
      modelAnswer:
        'Send documents and equipment before day one, assign a buddy, schedule a manager meeting to set 30-60-90 day goals, cover policies and tools in short sessions, let them shadow calls, and collect feedback at the end of the week.',
    },
    {
      id: 'hr-posh', stage: 'situational',
      text: 'An employee tells you in confidence about harassment by their team lead. What steps do you take?',
      keywords: ['posh', 'internal committee', 'confidential', 'document', 'support', 'inquiry', 'retaliation', 'policy'],
      modelAnswer:
        'Listen without judgement, assure confidentiality within legal limits, document the details, explain the POSH process and the Internal Committee, protect the employee from retaliation, and ensure the complaint reaches the IC within the required timelines.',
      followUp: { trigger: ['confidential'], text: 'What if the employee asks you not to report it formally?' },
    },
    closing,
  ],
  'sales-bd': [
    intro('sales and business development'),
    {
      id: 'sales-target', stage: 'resume',
      text: 'Tell me about a target you achieved or a time you persuaded someone to say yes.',
      keywords: ['target', 'achieved', 'percent', 'client', 'convinced', 'result', 'number'],
      modelAnswer:
        'Quantify it: “I had a target of 40 college admissions in a quarter. I mapped schools by location, ran demo sessions and followed up within 24 hours, closing 52 — 130% of target.”',
    },
    {
      id: 'sales-pitch', stage: 'technical',
      text: 'Pitch our mock-test platform to a coaching institute owner in 60 seconds.',
      keywords: ['problem', 'benefit', 'students', 'results', 'cost', 'trial', 'value'],
      modelAnswer:
        'Open with their problem (students need more practice with feedback), state the benefit (unlimited AI papers with personalised reports), add proof (pilot results), handle cost (per-student pricing) and close with a clear next step (a free two-week pilot).',
    },
    {
      id: 'sales-objection', stage: 'situational',
      text: 'The client says, “Your product is too expensive.” How do you respond?',
      keywords: ['understand', 'value', 'roi', 'compare', 'option', 'discount', 'question'],
      modelAnswer:
        'Acknowledge the concern, ask what they are comparing against, re-anchor on value and ROI, offer a smaller starting package if needed — avoid discounting immediately.',
      followUp: { trigger: ['discount'], text: 'If you offer a discount, what would you ask for in return?' },
    },
    {
      id: 'sales-pipeline', stage: 'technical',
      text: 'How do you plan your week to keep a healthy sales pipeline?',
      keywords: ['crm', 'prospect', 'follow-up', 'priority', 'funnel', 'meetings'],
      modelAnswer:
        'Block time for prospecting daily, prioritise deals by stage and value in the CRM, schedule follow-ups immediately after meetings, and review conversion rates at the end of the week.',
    },
    {
      id: 'sales-hr', stage: 'hr',
      text: 'How do you handle rejection, given that most sales calls do not convert?',
      keywords: ['learn', 'resilient', 'next', 'feedback', 'positive', 'improve'],
      modelAnswer:
        'Treat rejection as data: note the reason, refine the pitch, and move to the next prospect. Share an example where feedback from a lost deal helped you win a later one.',
    },
    {
      id: 'sales-discovery', stage: 'technical',
      text: 'What questions would you ask in a first discovery call with a new client?',
      keywords: ['problem', 'budget', 'decision', 'timeline', 'current', 'goals', 'pain', 'listen'],
      modelAnswer:
        'Ask open questions about their current process, biggest pain points, goals for the next quarter, who makes and influences the decision, budget range and timeline. Listen more than you speak and summarise their needs before proposing anything.',
    },
    {
      id: 'sales-lost', stage: 'situational',
      text: 'A key account tells you they are moving to a competitor next month. What do you do?',
      keywords: ['understand', 'reason', 'meeting', 'value', 'offer', 'escalate', 'feedback', 'relationship'],
      modelAnswer:
        'Request a meeting quickly to understand the real reason, revisit the value they have received, address the gap with a concrete plan or offer within approval limits, involve senior leadership if needed, and keep the relationship positive even if they leave.',
      followUp: { trigger: ['discount', 'price'], text: 'If price is the only reason, how low would you go, and why?' },
    },
    closing,
  ],
  accountant: [
    intro('accountant / financial analyst'),
    {
      id: 'acc-resume', stage: 'resume',
      text: 'Which accounting tools or ERPs have you worked with, and on what kind of tasks?',
      keywords: ['tally', 'excel', 'sap', 'zoho', 'reconciliation', 'gst', 'entries'],
      modelAnswer:
        'Name tools specifically and tie them to tasks: “I used Tally Prime for journal entries and GST returns, and Excel for monthly bank reconciliation and variance analysis.”',
    },
    {
      id: 'acc-statements', stage: 'technical',
      text: 'How are the three financial statements linked to each other?',
      keywords: ['net income', 'retained earnings', 'cash flow', 'balance sheet', 'profit', 'depreciation'],
      modelAnswer:
        'Net income from the P&L flows into retained earnings on the balance sheet and is the starting point of the cash-flow statement. Non-cash items like depreciation are added back, and closing cash ties to the balance sheet.',
      followUp: { trigger: ['depreciation'], text: 'If depreciation increases by ₹10, walk me through the effect on all three statements.' },
    },
    {
      id: 'acc-gst', stage: 'technical',
      text: 'What is input tax credit under GST, and when can it be denied?',
      keywords: ['input', 'credit', 'output', 'invoice', 'gstr', 'blocked', 'supplier'],
      modelAnswer:
        'ITC lets a business reduce its output GST by the GST paid on inputs. It can be denied if the supplier has not filed returns, the invoice is missing, goods are not received, or the item is in the blocked-credit list (e.g. personal-use items).',
    },
    {
      id: 'acc-situational', stage: 'situational',
      text: 'At month-end, the bank balance does not match the books by ₹48,000. How do you investigate?',
      keywords: ['reconciliation', 'cheques', 'charges', 'timing', 'entries', 'statement'],
      modelAnswer:
        'Prepare a bank reconciliation: check uncleared cheques and deposits in transit, bank charges and interest not recorded, duplicate or missing entries, then pass correcting entries and document the reason.',
    },
    {
      id: 'acc-hr', stage: 'hr',
      text: 'How do you make sure your work is accurate when deadlines are tight?',
      keywords: ['checklist', 'review', 'prioritise', 'reconcile', 'double-check', 'automation'],
      modelAnswer:
        'Use checklists and templates, reconcile control totals, prioritise high-risk items first, and request a peer review for critical filings.',
    },
    {
      id: 'acc-excel', stage: 'technical',
      text: 'Which Excel functions do you use most for reconciliation and reporting, and for what?',
      keywords: ['vlookup', 'xlookup', 'sumifs', 'pivot', 'index', 'match', 'conditional formatting', 'if'],
      modelAnswer:
        'XLOOKUP or INDEX-MATCH to match ledger entries with bank statements, SUMIFS to total by account or period, pivot tables for summaries, IF with conditional formatting to highlight mismatches, and data validation to prevent entry errors.',
    },
    {
      id: 'acc-deadline', stage: 'situational',
      text: 'Your manager wants the monthly report two days early, but GST filing is due the same day. How do you prioritise?',
      keywords: ['deadline', 'statutory', 'penalty', 'communicate', 'plan', 'help', 'priority', 'manager'],
      modelAnswer:
        'Statutory filings carry penalties, so GST comes first. Tell the manager early, share a realistic plan for the report (for example, a summary early and the full report on time), and ask for support or reprioritisation of other tasks.',
    },
    closing,
  ],
  'civil-services-pt': [
    {
      id: 'intro', stage: 'introduction',
      text: 'Good morning. Please tell the board briefly about yourself and what motivated you towards the civil services.',
      keywords: ['serve', 'public', 'district', 'background', 'experience', 'change', 'governance'],
      modelAnswer:
        'Keep it concise and authentic: your background, one formative experience with public service or governance, and the specific kind of impact you want to have.',
    },
    {
      id: 'cs-daf', stage: 'resume',
      text: 'Your hometown is mentioned in your form. What is one major development challenge there, and how would you address it as a district collector?',
      keywords: ['water', 'employment', 'health', 'education', 'scheme', 'community', 'data'],
      modelAnswer:
        'Name a specific challenge with data, mention existing schemes, and propose practical steps: convergence of departments, community participation, monitoring with clear indicators.',
    },
    {
      id: 'cs-ethics', stage: 'situational',
      text: 'A senior officer asks you to approve a file that you believe violates the rules. What will you do?',
      keywords: ['rules', 'record', 'writing', 'integrity', 'escalate', 'polite', 'conduct'],
      modelAnswer:
        'Politely explain the rule, put your objection on record in the file, suggest a lawful alternative, and if pressure continues, escalate through proper channels — maintaining integrity without confrontation.',
      followUp: { trigger: ['escalate'], text: 'What if escalation could harm your career prospects?' },
    },
    {
      id: 'cs-governance', stage: 'technical',
      text: 'What are the strengths and limitations of cooperative federalism in India today?',
      keywords: ['centre', 'state', 'gst council', 'niti aayog', 'finance commission', 'balance'],
      modelAnswer:
        'Strengths: GST Council and NITI Aayog as platforms for joint decision-making; limitations: fiscal dependence of states and concerns over centrally sponsored schemes. Conclude with a balanced way forward.',
    },
    {
      id: 'cs-current', stage: 'technical',
      text: 'How can technology improve last-mile delivery of welfare schemes?',
      keywords: ['dbt', 'aadhaar', 'digital', 'leakage', 'grievance', 'exclusion', 'privacy'],
      modelAnswer:
        'Direct Benefit Transfer reduces leakages, digital grievance systems improve accountability, but exclusion errors and privacy must be handled with offline fallbacks and strong data protection.',
    },
    {
      id: 'cs-hr', stage: 'hr',
      text: 'If you are not selected this year, what will you do?',
      keywords: ['continue', 'learn', 'career', 'serve', 'plan', 'improve'],
      modelAnswer:
        'Show composure and a plan: reflect on feedback, continue preparing while building a meaningful career, and remain committed to public service in any capacity.',
    },
    {
      id: 'cs-optional', stage: 'technical',
      text: 'How is your optional subject relevant to the work of a civil servant?',
      keywords: ['policy', 'administration', 'analysis', 'example', 'district', 'decision', 'public'],
      modelAnswer:
        'Link the subject to real administrative work with one or two concrete examples, such as how economics helps evaluate subsidy schemes or how sociology helps understand community resistance to a project.',
    },
    {
      id: 'cs-crisis', stage: 'situational',
      text: 'As a district collector, a flood warning arrives at midnight for low-lying villages. What are your first three actions?',
      keywords: ['evacuate', 'ndrf', 'shelter', 'communication', 'control room', 'coordination', 'vulnerable'],
      modelAnswer:
        'Activate the district control room and alert all departments, begin evacuation of low-lying areas prioritising the elderly, children and the sick with NDRF/SDRF support, and set up relief shelters with food, water and medical aid while keeping communication channels open.',
      followUp: { trigger: ['evacuate'], text: 'Some villagers refuse to leave their homes and livestock. What do you do?' },
    },
    closing,
  ],
};

export const getRoleById = (id: string): InterviewRole | undefined => liveCatalog.role(id) ?? INTERVIEW_ROLES.find((r) => r.id === id);
