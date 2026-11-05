"""Server-side message catalog: notification and email texts (PDF 5.8, 8).

Client UI strings live in the web/mobile apps' own i18n files. English is the fallback for every key; the
Tier 1 languages below are starter translations and must be reviewed by native speakers before launch.
"""

MESSAGES: dict[str, dict[str, tuple[str, str]]] = {
    "en": {
        "result_ready": ("Your AI report is ready", "Your report for {exam} is ready. See your strengths, weak topics and 7-day plan."),
        "interview_report_ready": ("Your interview report is ready", "Your {role} mock interview report is ready."),
        "report_failed": ("Report delayed - credit restored", "We could not generate your report for {name} in time. Your credit has been restored."),
        "payment_receipt": ("Payment received", "We received ₹{amount} for {plan}. {credits} credit(s) added, valid until {expires}. Invoice {invoice}."),
        "plan_expiring": ("Credits expiring soon", "{credits} credit(s) expire on {expires}. Take a mock test before they lapse."),
        "practice_reminder": ("Time for a practice test", "You have not practised for a week. A short mock keeps your preparation on track."),
        "refund_processed": ("Refund processed", "Your refund of ₹{amount} for order {order} has been processed."),
        "mentor_morning": ("Good morning! {days} days to {exam}", "Today's focus: {focus}."),
        "mentor_countdown": ("Only {days} days left for {exam}", "{advice}. Today's focus: {focus}."),
        "mentor_afternoon": ("Today's practice is waiting", "You have not completed today's {subject} practice yet: {task}."),
        "mentor_evening": ("Your day in review", "{status}{extra}"),
        "mentor_missed": ("Let's get back on track", "You have missed your planned preparation for {days} days. {exam} is {exam_days} days away, so your schedule has been adjusted."),
    },
    "hi": {
        "result_ready": ("आपकी AI रिपोर्ट तैयार है", "{exam} की आपकी रिपोर्ट तैयार है। अपनी ताकत, कमजोर विषय और 7-दिन की योजना देखें।"),
        "interview_report_ready": ("आपकी इंटरव्यू रिपोर्ट तैयार है", "आपके {role} मॉक इंटरव्यू की रिपोर्ट तैयार है।"),
        "report_failed": ("रिपोर्ट में देरी - क्रेडिट वापस", "{name} की रिपोर्ट समय पर नहीं बन सकी। आपका क्रेडिट वापस कर दिया गया है।"),
        "payment_receipt": ("भुगतान प्राप्त हुआ", "{plan} के लिए ₹{amount} प्राप्त हुए। {credits} क्रेडिट जोड़े गए, {expires} तक मान्य। इनवॉइस {invoice}।"),
        "plan_expiring": ("क्रेडिट जल्द समाप्त होंगे", "{credits} क्रेडिट {expires} को समाप्त होंगे। उससे पहले एक मॉक टेस्ट दें।"),
        "practice_reminder": ("अभ्यास का समय", "आपने एक सप्ताह से अभ्यास नहीं किया है। एक छोटा मॉक टेस्ट दें।"),
        "refund_processed": ("रिफंड हो गया", "ऑर्डर {order} के लिए ₹{amount} का रिफंड प्रोसेस हो गया है।"),
        "mentor_morning": ("सुप्रभात! {exam} में {days} दिन बाकी", "आज का फोकस: {focus}।"),
        "mentor_countdown": ("{exam} में केवल {days} दिन बाकी", "{advice}। आज का फोकस: {focus}।"),
        "mentor_afternoon": ("आज का अभ्यास बाकी है", "आपने आज का {subject} अभ्यास अभी पूरा नहीं किया है: {task}।"),
        "mentor_evening": ("आज की तैयारी", "{status}{extra}"),
        "mentor_missed": ("चलिए फिर से शुरू करें", "आपकी योजना की तैयारी {days} दिन से छूट गई है। {exam} {exam_days} दिन दूर है, इसलिए आपका शेड्यूल बदल दिया गया है।"),
    },
    "ta": {
        "result_ready": ("உங்கள் AI அறிக்கை தயார்", "{exam} க்கான உங்கள் அறிக்கை தயார். உங்கள் பலம், பலவீனமான பகுதிகள் மற்றும் 7 நாள் திட்டத்தைப் பாருங்கள்."),
        "interview_report_ready": ("உங்கள் நேர்காணல் அறிக்கை தயார்", "உங்கள் {role} மாதிரி நேர்காணல் அறிக்கை தயார்."),
        "report_failed": ("அறிக்கை தாமதம் - கிரெடிட் திருப்பி அளிக்கப்பட்டது", "{name} க்கான அறிக்கையை உருவாக்க முடியவில்லை. உங்கள் கிரெடிட் திருப்பி அளிக்கப்பட்டது."),
        "payment_receipt": ("பணம் பெறப்பட்டது", "{plan} க்கு ₹{amount} பெறப்பட்டது. {credits} கிரெடிட் சேர்க்கப்பட்டது, {expires} வரை செல்லும். இன்வாய்ஸ் {invoice}."),
        "plan_expiring": ("கிரெடிட் விரைவில் காலாவதியாகும்", "{credits} கிரெடிட் {expires} அன்று காலாவதியாகும்."),
        "practice_reminder": ("பயிற்சி நேரம்", "ஒரு வாரமாக நீங்கள் பயிற்சி செய்யவில்லை. ஒரு சிறிய மாதிரி தேர்வு எழுதுங்கள்."),
        "refund_processed": ("பணம் திருப்பி அளிக்கப்பட்டது", "ஆர்டர் {order} க்கான ₹{amount} திருப்பி அளிக்கப்பட்டது."),
    },
}


class _SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def message(kind: str, language: str, **params) -> tuple[str, str]:
    title, body = MESSAGES.get(language, {}).get(kind) or MESSAGES["en"][kind]
    return title.format_map(_SafeDict(params)), body.format_map(_SafeDict(params))
