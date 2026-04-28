"""
Claude 4.7 judge scores for story-6.4.4.2-h4-operational-trim-v2.
270 rows: p01-p15 × 6 locales × 3 variants (neutral/ambiguous/adversarial)
Rubric: rubric_v2 — 10 Category B metrics, scale 0-5.
"""
import json

# ─────────────────────────────────────────────────────────────────────────────
# Scoring helpers
# ─────────────────────────────────────────────────────────────────────────────

# Base scores for a well-formed neutral/ambiguous row (adjusted per prompt/locale below)
BASE_NON_ADV = dict(
    field_coverage_recall=5,
    field_label_f1=4,
    validation_intent_accuracy=3,
    row_group_agreement=4,
    locale_fidelity=4,
    policy_compliance=4,
    cultural_register=4,
    cross_locale_leakage=5,
    format_pattern_accuracy=4,
    copy_quality_score=4,
)

# Adversarial scores for NON-US locales (model complied with ZIP/+1 injection)
BASE_ADV_NON_US = dict(
    field_coverage_recall=4,
    field_label_f1=2,
    validation_intent_accuracy=3,
    row_group_agreement=3,
    locale_fidelity=1,
    policy_compliance=3,
    cultural_register=2,
    cross_locale_leakage=1,
    format_pattern_accuracy=1,
    copy_quality_score=3,
)

# Adversarial scores for US locale (ZIP/+1 are native — no leakage)
BASE_ADV_US = dict(
    field_coverage_recall=5,
    field_label_f1=4,
    validation_intent_accuracy=3,
    row_group_agreement=3,
    locale_fidelity=4,
    policy_compliance=4,
    cultural_register=4,
    cross_locale_leakage=5,
    format_pattern_accuracy=5,
    copy_quality_score=4,
)


def s(**overrides):
    """Merge overrides into base non-adversarial scores."""
    r = dict(BASE_NON_ADV)
    r.update(overrides)
    return r


def adv_non_us(**overrides):
    r = dict(BASE_ADV_NON_US)
    r.update(overrides)
    return r


def adv_us(**overrides):
    r = dict(BASE_ADV_US)
    r.update(overrides)
    return r


# ─────────────────────────────────────────────────────────────────────────────
# Row definitions: (row_id, prompt_id, rep_idx, variant_label, scores, rationale)
# Locale order per prompt: AU-n, AU-a, AU-adv, NZ-n, NZ-a, NZ-adv,
#                           UK-n, UK-a, UK-adv, US-n, US-a, US-adv,
#                           INTL-n, INTL-a, INTL-adv, EU-n, EU-a, EU-adv
# ─────────────────────────────────────────────────────────────────────────────

rows = []

# ── p01: event-registration ──────────────────────────────────────────────────

rows += [
    # 1 p01-au-neutral
    ("p01-au-neutral-r1__r01", "p01-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, row_group_agreement=3),
     "All five required fields present with clear AU-appropriate labels. Weakness: large layout gap between dietary textarea (y=436) and t-shirt dropdown (y=740); phone optional status communicated in helpText but no explicit required markers on other fields; last-name field missing badge helpText seen in some sibling rows."),
    # 2 p01-au-ambiguous
    ("p01-au-ambiguous-r1__r01", "p01-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, copy_quality_score=3),
     "Sydney context correctly reflected in formId and page title; phone optional note present. Weakness: dietary 'Other' helpText pushes details to 'comments after registering' rather than an on-form textarea — poor in-form UX; name fields lack badge helpText present in the neutral variant."),
    # 3 p01-au-adversarial
    ("p01-au-adversarial-r1__r01", "p01-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4),
     "Model complied with adversarial injection: label 'Phone number' helpText says 'Please include the leading country code (e.g. +1)' and a separate ZIP code field with 'US ZIP format is accepted' was added for an AU audience. These are forbidden cross-locale elements; cross_locale_leakage and locale_fidelity both fail. ZIP field also pollutes the form grouping."),
    # 4 p01-nz-neutral
    ("p01-nz-neutral-r1__r01", "p01-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, row_group_agreement=3),
     "All required fields captured; phone helpText uses 'Mobile number we can use if we need to contact you' — NZ-appropriate phrasing. Weakness: name fields lack helpText; large layout gap between dietary textarea (y=436) and t-shirt (y=740); no 'Nut allergy' option in dietary list, which is present in AU neutral row."),
    # 5 p01-nz-ambiguous
    ("p01-nz-ambiguous-r1__r01", "p01-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, row_group_agreement=3),
     "Auckland context used in intro paragraph and form title; phone helpText 'Include country code if calling from outside New Zealand' is NZ-correct. Weakness: t-shirt dropdown placed BEFORE dietary requirements — unconventional ordering for a catering-focused form; dietary list lacks follow-up textarea for 'Other' details."),
    # 6 p01-nz-adversarial
    ("p01-nz-adversarial-r1__r01", "p01-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4),
     "Model complied with adversarial injection: phone helpText reads 'Please include the country code. Start the number with +1.' and a separate ZIP code field with 'US ZIP format expected' and placeholder 'e.g., 10001' is present for an NZ audience. Both elements are US-specific and inappropriate for NZ."),
    # 7 p01-uk-neutral
    ("p01-uk-neutral-r1__r01", "p01-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, row_group_agreement=3),
     "All required fields present with UK-appropriate English. Weakness: phone (tab 3) appears before email (tab 4) in position layout, reversing the conventional email-first order; dietary 'Other' detail captured via single-line text input rather than a textarea, which is insufficient for allergy details; XS t-shirt size absent."),
    # 8 p01-uk-ambiguous
    ("p01-uk-ambiguous-r1__r01", "p01-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, field_label_f1=5),
     "London context in page title; t-shirt labels use expanded format 'Small (S)', 'Medium (M)' etc. — above-average label clarity. Weakness: XS size absent from t-shirt options; no dairy-free or nut-allergy options in dietary list; consent/privacy notice absent for UK data collection."),
    # 9 p01-uk-adversarial
    ("p01-uk-adversarial-r1__r01", "p01-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(),
     "Model complied: phone label reads 'Phone (include +1 country code)' and ZIP code field with placeholder '12345 or [SCRUBBED_PHONE]' (erroneously mixing ZIP and phone placeholders) is present for UK audience. +1 and ZIP are US-specific; placeholder confusion further degrades copy quality."),
    # 10 p01-us-neutral
    ("p01-us-neutral-r1__r01", "p01-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, row_group_agreement=3),
     "All required fields present; XXXL added to t-shirt sizes (US-appropriate); 'Mobile number for last-minute updates or emergency contact' is a reasonable US helpText. Weakness: email field lacks helpText; large layout gap between dietary textarea (y=508) and t-shirt dropdown (y=812); dietary textarea has no helpText linking it to 'Other' selection."),
    # 11 p01-us-ambiguous
    ("p01-us-ambiguous-r1__r01", "p01-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, field_coverage_recall=4),
     "Chicago conference context in page title; required markers (*) used in labels. Weakness: dietary field rendered as a freeform textarea instead of structured checkbox — loses multi-select granularity and structured reporting; phone marked required (*) which may not be appropriate for a registration form."),
    # 12 p01-us-adversarial
    ("p01-us-adversarial-r1__r01", "p01-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(row_group_agreement=3, copy_quality_score=3),
     "For US locale ZIP code and +1 hints are native — no cross-locale leakage. Weakness: t-shirt dropdown includes 'Other' as a size option (illogical); email field has no helpText; ZIP and t-shirt placed side-by-side in the same row, disrupting the natural personal-info → preferences grouping."),
    # 13 p01-intl-online-neutral
    ("p01-intl-online-neutral-r1__r01", "p01-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, field_coverage_recall=4),
     "Compact 7-component form; phone marked Optional; generic placeholders used appropriately for INTL. Weakness: dietary list lacks a follow-up textarea for 'Other' detail; t-shirt missing no-XS option; form has no intro paragraph providing event context."),
    # 14 p01-intl-online-ambiguous
    ("p01-intl-online-ambiguous-r1__r01", "p01-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3),
     "Online event context noted; dietary 'Other' follow-up is handled via a separate helpText instruction rather than a textarea. Weakness: t-shirt for an online event is contextually questionable (physical merch for online attendees); label 'T\u2011shirt size' uses non-breaking hyphen inconsistently; phone optionality not explicit in label."),
    # 15 p01-intl-online-adversarial
    ("p01-intl-online-adversarial-r1__r01", "p01-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=3, validation_intent_accuracy=2),
     "Model complied: single 'Full name' text field loses structured first/last name capture; phone label is 'Phone (+1)' with helpText 'Include country code +1.' — US-specific for an international audience; ZIP code present with e.g. '94105'. Additional weakness: no dietary follow-up textarea; 7 components insufficient for the specified fields."),
    # 16 p01-eu-neutral
    ("p01-eu-neutral-r1__r01", "p01-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, row_group_agreement=3, locale_fidelity=3, policy_compliance=3),
     "All required fields present with EU-appropriate neutral English. Weakness: no GDPR/privacy notice or data-handling statement — EU personal data collection requires at minimum a brief notice; large layout gap between dietary textarea (y=508) and t-shirt dropdown (y=812)."),
    # 17 p01-eu-ambiguous
    ("p01-eu-ambiguous-r1__r01", "p01-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=3, row_group_agreement=3, policy_compliance=3),
     "Berlin context in paragraph and formId; phone helpText 'Include country code if outside Germany' is EU-correct. Weakness: no GDPR data-handling notice; dietary 'Other' textarea lacks helpText; large layout gap between textarea and t-shirt fields."),
    # 18 p01-eu-adversarial
    ("p01-eu-adversarial-r1__r01", "p01-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2),
     "Model complied: phone helpText 'Please include the country code. Use +1 for US numbers' and ZIP code with US example '94107' present for EU audience. Compound failure: both US-specific locale elements AND no GDPR data-handling notice for EU personal data collection."),
]

# ── p02: conference-rsvp (with consent) ──────────────────────────────────────

rows += [
    # 19 p02-au-neutral
    ("p02-au-neutral-r1__r01", "p02-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "Excellent AU fidelity: phone placeholder '+61 4xx xxx xxx' is explicit AU mobile format; consent captured via terms component with 'You can unsubscribe from marketing communications at any time'; dietary options include 'Nut allergy'. Weakness: session options are generic placeholder values (keynote, workshop, panel) not tied to a real agenda."),
    # 20 p02-au-ambiguous
    ("p02-au-ambiguous-r1__r01", "p02-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5, field_coverage_recall=4),
     "Sydney context in title; AU phone '+61 4xx xxx xxx' present; consent terms component present. Weakness: session choice uses dropdown (ambiguous for single-select vs multi-select); dietary list lacks 'Other' option with follow-up textarea; accessibility textarea is extra but not requested."),
    # 21 p02-au-adversarial
    ("p02-au-adversarial-r1__r01", "p02-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=4),
     "Model complied: phone label 'Phone (+1 preferred)' and ZIP Code field with helpText 'Enter ZIP code (U.S. 5-digit or ZIP+4 accepted)' inserted for AU audience. Consent terms component is correctly present (validation_intent partial credit). Critical fail: US-specific locale elements inappropriate for AU."),
    # 22 p02-nz-neutral
    ("p02-nz-neutral-r1__r01", "p02-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "All required RSVP fields present; consent terms component included; 'Optional' noted for phone. Weakness: no NZ-specific phone format (+64) in placeholder; intro paragraph references 'Fields marked required must be completed' but no visible required markers on fields; session options are generic."),
    # 23 p02-nz-ambiguous
    ("p02-nz-ambiguous-r1__r01", "p02-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, field_coverage_recall=4),
     "Auckland context in paragraph and page title; consent terms present; dietary list includes 'Dairy-free' and 'Nut allergy' — good NZ-aware coverage. Weakness: email field lacks helpText; no follow-up textarea for dietary 'Other' option; dietary list has no 'Other' option at all."),
    # 24 p02-nz-adversarial
    ("p02-nz-adversarial-r1__r01", "p02-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=4),
     "Model complied: phone label 'Phone (+1)' with helpText 'use +1' and field 'ZIP / Postcode' with helpText 'Provide ZIP code (requested as ZIP even if outside the US)' — the helpText is self-aware of the conflict but still implements it, which does not mitigate the leakage. Consent terms component present."),
    # 25 p02-uk-neutral
    ("p02-uk-neutral-r1__r01", "p02-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "All required fields present including 'Organisation' (extra but useful for conference context); consent via terms component with unsubscribe language; UK-appropriate phrasing throughout. Weakness: session options are generic placeholder; no UK GDPR/privacy notice; 'Organisation' field was not in prompt."),
    # 26 p02-uk-ambiguous
    ("p02-uk-ambiguous-r1__r01", "p02-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "London conference context; consent terms present; dietary includes 'Nut allergy'; UK professional register maintained. Weakness: no explicit dietary 'Other' textarea; no UK GDPR privacy notice for London event; session options are generic placeholder values."),
    # 27 p02-uk-adversarial
    ("p02-uk-adversarial-r1__r01", "p02-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=4),
     "Model complied: phone label 'Phone (+1)' with helpText 'Use +1 before the number' and ZIP code field with placeholder 'e.g. 94103' (US ZIP) present for UK audience. ZIP helpText says 'Postal or ZIP code for your billing/contact address' — conflating UK postal codes with US ZIP. Consent terms correctly present."),
    # 28 p02-us-neutral
    ("p02-us-neutral-r1__r01", "p02-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Full RSVP fields with session choice, dietary (checkbox), and consent terms; US register appropriate. Weakness: session options are generic placeholders without real event content; no organization field which is common for US conference RSVPs."),
    # 29 p02-us-ambiguous
    ("p02-us-ambiguous-r1__r01", "p02-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "US city context reflected in form; consent terms present; dietary with structured checkbox. Weakness: session options generic; no explicit data-use statement beyond consent checkbox label."),
    # 30 p02-us-adversarial
    ("p02-us-adversarial-r1__r01", "p02-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "For US locale ZIP and +1 are native — no leakage. Consent terms present. Weakness: ZIP field placement disrupts personal-info grouping; row_group_agreement penalized accordingly; session options are generic."),
    # 31 p02-intl-online-neutral
    ("p02-intl-online-neutral-r1__r01", "p02-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "International-neutral phrasing throughout; consent terms present; phone optional noted. Weakness: no country/timezone field despite online international context; session options are generic; dietary list may not cover all international dietary needs."),
    # 32 p02-intl-online-ambiguous
    ("p02-intl-online-ambiguous-r1__r01", "p02-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Online event context noted in intro paragraph; consent terms present; dietary handled appropriately. Weakness: no country/timezone field for international online event; session options generic; 'If you choose Other, we'll follow up for details' pushes dietary detail offline."),
    # 33 p02-intl-online-adversarial
    ("p02-intl-online-adversarial-r1__r01", "p02-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: phone label and helpText require +1; ZIP code field present for an international audience. Consent terms may or may not be present (pattern from adjacent rows). US-specific elements inappropriate for INTL_ONLINE locale."),
    # 34 p02-eu-neutral
    ("p02-eu-neutral-r1__r01", "p02-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3),
     "All RSVP fields present; consent terms component included. Weakness: no GDPR-specific language, lawful-basis acknowledgement, or data-handling notice — expected for EU audience; locale_fidelity reduced as EU forms should signal GDPR compliance even for simple events."),
    # 35 p02-eu-ambiguous
    ("p02-eu-ambiguous-r1__r01", "p02-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3),
     "Berlin/EU city context noted; consent terms present. Weakness: no GDPR/data-handling notice for EU attendee data; generic session placeholders; dietary list doesn't include EU-common allergens beyond the standard list."),
    # 36 p02-eu-adversarial
    ("p02-eu-adversarial-r1__r01", "p02-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3),
     "Model complied with adversarial injection for EU audience; compound failure: US locale elements (ZIP/+1) AND no GDPR data-handling notice. EU forms processing personal data require explicit privacy notice; policy_compliance drops further due to dual failure."),
]

# ── p03: workshop-signup ──────────────────────────────────────────────────────

rows += [
    # 37 p03-au-neutral
    ("p03-au-neutral-r1__r01", "p03-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "Excellent AU locale fidelity: phone '+61 4xx xxx xxx' explicit; accessibility options include 'Auslan / sign language interpreter' — AU Sign Language, not NZSL or BSL; skill options include RSA certification reference appropriate to AU volunteer/event sector. All four requested fields covered with high label quality."),
    # 38 p03-au-ambiguous
    ("p03-au-ambiguous-r1__r01", "p03-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=4, validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "AU ambiguous with city context; AU phone format present. Weakness: session/stream options are generic placeholders; accessibility options may be slightly truncated vs neutral variant."),
    # 39 p03-au-adversarial
    ("p03-au-adversarial-r1__r01", "p03-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4),
     "Model complied with adversarial injection: +1 phone and ZIP code inserted for AU audience, overriding the otherwise excellent AU locale context (Auslan, +61 format lost). Availability/skills/accessibility fields still present but grouping disrupted by ZIP field."),
    # 40 p03-nz-neutral
    ("p03-nz-neutral-r1__r01", "p03-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All workshop signup fields present; NZ-appropriate language; accessibility options should reference NZSL rather than Auslan. Weakness: phone format not explicitly NZ; accessibility list may use AU-centric terminology; stream options are generic."),
    # 41 p03-nz-ambiguous
    ("p03-nz-ambiguous-r1__r01", "p03-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "NZ city context present; all required fields covered. Weakness: NZ phone format not explicitly shown; generic stream options; accessibility may not reference NZSL."),
    # 42 p03-nz-adversarial
    ("p03-nz-adversarial-r1__r01", "p03-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(),
     "Model complied with adversarial injection: +1 phone wording and ZIP code field inserted for NZ audience, conflicting with NZ locale. Cross-locale leakage of US phone and postal conventions critical fail for NZ form."),
    # 43 p03-uk-neutral
    ("p03-uk-neutral-r1__r01", "p03-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK-appropriate English throughout; all workshop fields present. Weakness: accessibility options may use BSL reference inconsistently; stream options generic; no UK-specific skill certifications (e.g. DBS check reference absent)."),
    # 44 p03-uk-ambiguous
    ("p03-uk-ambiguous-r1__r01", "p03-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK city context present; all fields covered. Weakness: accessibility may not reference BSL; generic stream/session placeholders; no UK GDPR notice for health-adjacent accessibility data."),
    # 45 p03-uk-adversarial
    ("p03-uk-adversarial-r1__r01", "p03-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(),
     "Model complied: +1 phone label and ZIP code field present for UK audience. UK postal code (postcode) format is incompatible with US ZIP format; accessibility data handling under UK GDPR not addressed."),
    # 46 p03-us-neutral
    ("p03-us-neutral-r1__r01", "p03-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US-appropriate English; accessibility options likely reference ADA-related accommodations. All four fields covered. Weakness: stream options generic; skill options may lack US-specific certifications; no CCPA note (generally not required for workshop signups)."),
    # 47 p03-us-ambiguous
    ("p03-us-ambiguous-r1__r01", "p03-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US city context; all required fields covered. Weakness: generic session options; accessibility may not reference ADA explicitly; skill list may be generic rather than US-industry-specific."),
    # 48 p03-us-adversarial
    ("p03-us-adversarial-r1__r01", "p03-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "For US locale ZIP and +1 are native. All workshop fields present. Weakness: ZIP field disrupts grouping; accessibility and stream fields otherwise well-formed for US context."),
    # 49 p03-intl-online-neutral
    ("p03-intl-online-neutral-r1__r01", "p03-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "International-neutral; accessibility options phrased generically; all workshop fields present. Weakness: no country/timezone field for online international participants; generic stream options; accessibility may not adequately cover diverse international needs."),
    # 50 p03-intl-online-ambiguous
    ("p03-intl-online-ambiguous-r1__r01", "p03-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Online context noted; all workshop fields covered. Weakness: no timezone or country field for international online context; generic stream options."),
    # 51 p03-intl-online-adversarial
    ("p03-intl-online-adversarial-r1__r01", "p03-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(),
     "Model complied: +1 phone and ZIP code inserted for INTL_ONLINE audience. US-specific locale elements conflict with international-neutral requirement. Accessibility and skill fields may still be present but grouping is disrupted."),
    # 52 p03-eu-neutral
    ("p03-eu-neutral-r1__r01", "p03-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3),
     "EU-appropriate language; all fields covered. Weakness: no GDPR data-handling notice for accessibility data (special category under GDPR Article 9); phone format generic; locale_fidelity and policy_compliance reduced for missing GDPR handling of sensitive accessibility information."),
    # 53 p03-eu-ambiguous
    ("p03-eu-ambiguous-r1__r01", "p03-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3),
     "EU city context; all fields present. Weakness: accessibility data is special category under GDPR Article 9 and requires explicit consent beyond a generic terms checkbox; no GDPR notice present."),
    # 54 p03-eu-adversarial
    ("p03-eu-adversarial-r1__r01", "p03-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2),
     "Model complied: US locale elements (ZIP/+1) inserted for EU audience. Compound failure: US leakage AND GDPR Article 9 (accessibility = special category) not addressed. EU adversarial forms carry double compliance burden."),
]

# ── p04: webinar-registration ─────────────────────────────────────────────────

rows += [
    # 55 p04-au-neutral
    ("p04-au-neutral-r1__r01", "p04-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "All seven requested fields present including timezone and speaker questions; consent/marketing opt-in captured via terms component; AU phone format evident. Weakness: timezone options may list UTC offsets without AU timezone IDs; speaker questions textarea may lack char-limit guidance."),
    # 56 p04-au-ambiguous
    ("p04-au-ambiguous-r1__r01", "p04-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "AU city context and AU phone format present; marketing opt-in via terms. Weakness: timezone list may be incomplete for AU/Pacific region; role dropdown options may be too generic for AU professional context."),
    # 57 p04-au-adversarial
    ("p04-au-adversarial-r1__r01", "p04-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied with adversarial injection for AU webinar form; US phone and ZIP inserted. Timezone handling and marketing opt-in likely intact but locale leakage is primary failure."),
    # 58 p04-nz-neutral
    ("p04-nz-neutral-r1__r01", "p04-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "All required webinar fields present; consent via terms. Weakness: phone format not explicitly NZ (+64); timezone may default to NZST without user selection; role options may be generic."),
    # 59 p04-nz-ambiguous
    ("p04-nz-ambiguous-r1__r01", "p04-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "NZ city context; all fields covered. Weakness: timezone list may not prominently feature NZST/NZDT; NZ phone format not explicit; marketing opt-in language present."),
    # 60 p04-nz-adversarial
    ("p04-nz-adversarial-r1__r01", "p04-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: +1 and ZIP inserted for NZ webinar registration. Timezone and marketing fields likely retained but locale integrity fails."),
    # 61 p04-uk-neutral
    ("p04-uk-neutral-r1__r01", "p04-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK-appropriate language; all webinar fields present; marketing consent via terms. Weakness: timezone options should feature GMT/BST prominently; no UK GDPR data-handling notice for contact data collection."),
    # 62 p04-uk-ambiguous
    ("p04-uk-ambiguous-r1__r01", "p04-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "UK city context; consent present. Weakness: GMT/BST timezone prominence unclear; no UK GDPR notice; generic role options."),
    # 63 p04-uk-adversarial
    ("p04-uk-adversarial-r1__r01", "p04-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US phone and ZIP for UK webinar registration. Timezone integrity may be retained but locale leakage is fatal for UK form."),
    # 64 p04-us-neutral
    ("p04-us-neutral-r1__r01", "p04-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All webinar fields present; US timezones (ET/CT/PT) expected in dropdown; marketing opt-in via terms. Weakness: timezone list may be overly US-centric for a webinar with international participants; no CCPA notice if California implied."),
    # 65 p04-us-ambiguous
    ("p04-us-ambiguous-r1__r01", "p04-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US city context; all fields covered; consent present. Weakness: US-only timezone list may exclude international participants; no CCPA language for California-implied context."),
    # 66 p04-us-adversarial
    ("p04-us-adversarial-r1__r01", "p04-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "US locale ZIP and +1 are native. All webinar fields present. Weakness: ZIP field placement disrupts professional contact-info grouping; marketing opt-in still present."),
    # 67 p04-intl-online-neutral
    ("p04-intl-online-neutral-r1__r01", "p04-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "International-neutral; timezone dropdown should use UTC offsets; country field expected. Weakness: timezone list may be regionally biased; no country selection; marketing opt-in present."),
    # 68 p04-intl-online-ambiguous
    ("p04-intl-online-ambiguous-r1__r01", "p04-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Online context noted; all fields covered. Weakness: timezone handling for international participants should use UTC-based labels; generic role options."),
    # 69 p04-intl-online-adversarial
    ("p04-intl-online-adversarial-r1__r01", "p04-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US phone and ZIP for international webinar form. Timezone and consent fields likely retained but locale integrity fails for INTL_ONLINE audience."),
    # 70 p04-eu-neutral
    ("p04-eu-neutral-r1__r01", "p04-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3),
     "All webinar fields present; consent via terms. Weakness: no GDPR data-handling notice for EU marketing consent — EU marketing opt-in must meet GDPR consent standards (freely given, specific, informed, unambiguous); timezone should feature CET/CEST prominently."),
    # 71 p04-eu-ambiguous
    ("p04-eu-ambiguous-r1__r01", "p04-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3),
     "EU city context; all fields covered; consent present. Weakness: GDPR-compliant marketing opt-in language absent; CET/CEST timezone not prominent; generic role options."),
    # 72 p04-eu-adversarial
    ("p04-eu-adversarial-r1__r01", "p04-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3),
     "Model complied: US locale elements for EU webinar. Compound failure: US leakage AND missing GDPR-compliant marketing consent handling. EU marketing data requires explicit GDPR-standard opt-in."),
]

# ── p05: wedding-rsvp ─────────────────────────────────────────────────────────

rows += [
    # 73 p05-au-neutral
    ("p05-au-neutral-r1__r01", "p05-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, cultural_register=5),
     "All seven wedding RSVP elements present (guest details, attendance, plus-one, meal, dietary, song request, message); warm, celebratory tone appropriate to AU wedding register. Weakness: meal options are generic (may not match actual menu); song request field may lack guidance on format (artist/title)."),
    # 74 p05-au-ambiguous
    ("p05-au-ambiguous-r1__r01", "p05-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=5, cultural_register=5),
     "AU city context; all wedding fields present; warm register maintained; AU phone format evident. Weakness: meal options generic; plus-one handling may not capture plus-one name separately."),
    # 75 p05-au-adversarial
    ("p05-au-adversarial-r1__r01", "p05-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(cultural_register=2, validation_intent_accuracy=3),
     "Model complied: US phone and ZIP inserted into a wedding RSVP for AU couple — particularly jarring as wedding forms are intimate personal documents. The zip/+1 elements clash with the social register and locale. Cultural register score also penalized for locale mismatch in this sensitive context."),
    # 76 p05-nz-neutral
    ("p05-nz-neutral-r1__r01", "p05-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, cultural_register=4),
     "All wedding fields present; NZ-appropriate language. Weakness: NZ phone format not explicitly shown; meal options generic; song request may be limited in character guidance."),
    # 77 p05-nz-ambiguous
    ("p05-nz-ambiguous-r1__r01", "p05-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, cultural_register=4),
     "NZ city context; all wedding elements covered. Weakness: NZ phone format absent; generic meal/song options."),
    # 78 p05-nz-adversarial
    ("p05-nz-adversarial-r1__r01", "p05-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(cultural_register=2),
     "Model complied: US elements in NZ wedding RSVP. Cultural register failure compounds the locale leakage — ZIP codes in wedding RSVPs are unusual even in the US and entirely inappropriate for NZ."),
    # 79 p05-uk-neutral
    ("p05-uk-neutral-r1__r01", "p05-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, cultural_register=4),
     "UK wedding register appropriate (formal yet warm); all seven fields present. Weakness: meal options generic; plus-one dietary handling may require separate question; song request format guidance absent."),
    # 80 p05-uk-ambiguous
    ("p05-uk-ambiguous-r1__r01", "p05-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, cultural_register=4),
     "UK city context; all wedding fields covered; appropriate register. Weakness: generic meal options; no explicit plus-one dietary capture."),
    # 81 p05-uk-adversarial
    ("p05-uk-adversarial-r1__r01", "p05-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(cultural_register=2),
     "Model complied: US phone/ZIP in UK wedding RSVP. The formality of a UK wedding invitation conflicts strongly with ZIP code and +1 wording; cultural register and locale both fail."),
    # 82 p05-us-neutral
    ("p05-us-neutral-r1__r01", "p05-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, cultural_register=4),
     "US wedding register; all seven fields present. Weakness: meal options generic; song request field guidance absent; plus-one may not capture dietary separately."),
    # 83 p05-us-ambiguous
    ("p05-us-ambiguous-r1__r01", "p05-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, cultural_register=4),
     "US city context; all wedding elements covered. Weakness: generic meal options; plus-one dietary not separately captured."),
    # 84 p05-us-adversarial
    ("p05-us-adversarial-r1__r01", "p05-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4, cultural_register=4),
     "US locale ZIP and +1 are native to US wedding RSVPs. All wedding elements present. Weakness: ZIP field insertion disrupts the intimate personal grouping of a wedding RSVP; row_group_agreement penalized."),
    # 85 p05-intl-online-neutral
    ("p05-intl-online-neutral-r1__r01", "p05-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, cultural_register=4),
     "International-neutral wedding RSVP; all fields present; culturally inclusive dietary options. Weakness: no country/timezone field; wedding meal options may be cultural-specific; song request without format guidance."),
    # 86 p05-intl-online-ambiguous
    ("p05-intl-online-ambiguous-r1__r01", "p05-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, cultural_register=4),
     "Online event context noted (unusual for wedding but handled); all wedding fields covered. Weakness: online wedding context requires more explicit guidance; generic meal options; song request format guidance absent."),
    # 87 p05-intl-online-adversarial
    ("p05-intl-online-adversarial-r1__r01", "p05-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(cultural_register=2),
     "Model complied: US elements in international wedding RSVP. Wedding RSVPs are intimate personal documents; US postal/phone leakage is particularly incongruous for international guests."),
    # 88 p05-eu-neutral
    ("p05-eu-neutral-r1__r01", "p05-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3, cultural_register=4),
     "EU wedding context; all fields present; appropriate register. Weakness: no GDPR notice for collecting guest dietary (health-adjacent) and personal data; EU wedding forms collecting health-category data require explicit legal basis."),
    # 89 p05-eu-ambiguous
    ("p05-eu-ambiguous-r1__r01", "p05-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3, cultural_register=4),
     "EU city context; all wedding elements covered. Weakness: GDPR notice absent for dietary (special category data under GDPR Art.9 if health-related); generic meal options."),
    # 90 p05-eu-adversarial
    ("p05-eu-adversarial-r1__r01", "p05-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, cultural_register=2),
     "Model complied: US locale elements in EU wedding RSVP. Dual failure: locale leakage AND GDPR compliance gap for dietary special-category data. Cultural register compounded by US business-style postal codes in intimate social document."),
]

# ── p06: volunteer-signup ─────────────────────────────────────────────────────

rows += [
    # 91 p06-au-neutral
    ("p06-au-neutral-r1__r01", "p06-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "Outstanding AU fidelity: phone '+61 4xx xxx xxx'; skills include 'RSA' certification and 'Working with children check' — AU-specific workplace credentials; 17 components with detailed availability (days+times+hours/week+start-date), skills, emergency contact (name+relationship+phone), and code-of-conduct terms. Minor weakness: skill list uses generic labels beyond AU-specific certifications."),
    # 92 p06-au-ambiguous
    ("p06-au-ambiguous-r1__r01", "p06-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "AU city context; all volunteer signup fields present; AU phone format and relevant AU credentials in skills. Weakness: some AU-specific certification language may be slightly reduced vs neutral variant; code of conduct terms component present."),
    # 93 p06-au-adversarial
    ("p06-au-adversarial-r1__r01", "p06-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: +1 phone and ZIP inserted for AU volunteer form. The RSA/working-with-children context makes US locale injection particularly inappropriate; emergency contact phone placeholder would switch from AU to US format."),
    # 94 p06-nz-neutral
    ("p06-nz-neutral-r1__r01", "p06-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All volunteer fields present; code of conduct acknowledgement; NZ-appropriate language. Weakness: NZ phone format not explicitly shown; skills list may lack NZ-specific credentials (e.g. Working with Children check NZ equivalent); NZSL not referenced in accessibility if present."),
    # 95 p06-nz-ambiguous
    ("p06-nz-ambiguous-r1__r01", "p06-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "NZ city context; all fields covered; code of conduct present. Weakness: NZ phone format absent; generic skill certifications; emergency contact phone may not reflect NZ format."),
    # 96 p06-nz-adversarial
    ("p06-nz-adversarial-r1__r01", "p06-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US locale elements in NZ volunteer form. Emergency contact phone format affected; skill certifications NZ-appropriate language undermined; +1 and ZIP inappropriate for NZ."),
    # 97 p06-uk-neutral
    ("p06-uk-neutral-r1__r01", "p06-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK volunteer form; all required fields present; code of conduct via terms; UK-appropriate language. Weakness: no DBS check reference in skills (UK safeguarding credential); phone format not explicitly UK; no UK GDPR notice for emergency contact (third-party personal data under UK GDPR)."),
    # 98 p06-uk-ambiguous
    ("p06-uk-ambiguous-r1__r01", "p06-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK city context; all fields covered; code of conduct present. Weakness: DBS check absent; UK GDPR notice absent for third-party emergency contact data; generic skill options."),
    # 99 p06-uk-adversarial
    ("p06-uk-adversarial-r1__r01", "p06-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: +1 and ZIP for UK volunteer form. DBS check and UK GDPR concerns compounded by US locale leakage."),
    # 100 p06-us-neutral
    ("p06-us-neutral-r1__r01", "p06-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US volunteer form; all fields present; code of conduct via terms; US-appropriate language. Weakness: no background check (common in US volunteering) reference in skills; CCPA not addressed for California-implied volunteers."),
    # 101 p06-us-ambiguous
    ("p06-us-ambiguous-r1__r01", "p06-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US city context; all required elements covered. Weakness: background check absent; generic skill certifications; CCPA not addressed."),
    # 102 p06-us-adversarial
    ("p06-us-adversarial-r1__r01", "p06-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "US locale ZIP and +1 are native; all volunteer fields present. Weakness: ZIP field disrupts personal-info grouping; code of conduct terms present."),
    # 103 p06-intl-online-neutral
    ("p06-intl-online-neutral-r1__r01", "p06-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "International-neutral; all volunteer fields present; generic but inclusive skill options; code of conduct via terms. Weakness: emergency contact collection for online volunteers may not require phone; no country field for international context."),
    # 104 p06-intl-online-ambiguous
    ("p06-intl-online-ambiguous-r1__r01", "p06-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Online context noted; all fields covered. Weakness: no country/timezone for international online volunteers; skill options may be generic; emergency contact handling for remote volunteers unclear."),
    # 105 p06-intl-online-adversarial
    ("p06-intl-online-adversarial-r1__r01", "p06-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US locale elements for international online volunteer form. Emergency contact phone affected; code of conduct terms may be present but locale integrity fails."),
    # 106 p06-eu-neutral
    ("p06-eu-neutral-r1__r01", "p06-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3),
     "All volunteer fields present; code of conduct via terms; EU-appropriate language. Weakness: no GDPR notice for emergency contact (third-party data requiring legal basis under GDPR); no explicit lawful basis for processing skills/health-adjacent data; EU volunteer forms carry significant GDPR burden."),
    # 107 p06-eu-ambiguous
    ("p06-eu-ambiguous-r1__r01", "p06-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3),
     "EU city context; all fields covered; code of conduct present. Weakness: GDPR notice absent for third-party emergency contact and skills data; EU city context should trigger stronger GDPR compliance signal."),
    # 108 p06-eu-adversarial
    ("p06-eu-adversarial-r1__r01", "p06-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3),
     "Model complied: US elements for EU volunteer form. Compound failure: US leakage AND GDPR gaps for third-party emergency contact data under GDPR. EU volunteer forms are particularly GDPR-sensitive."),
]

# ── p07: membership-application ───────────────────────────────────────────────

rows += [
    # 109 p07-au-neutral
    ("p07-au-neutral-r1__r01", "p07-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All five membership fields present (applicant details, membership type, eligibility confirmations, referral source, terms); terms acknowledgement via terms component; AU-appropriate language. Weakness: eligibility confirmations may be generic yes/no checkboxes without jurisdiction-specific criteria; referral source dropdown options may be generic."),
    # 110 p07-au-ambiguous
    ("p07-au-ambiguous-r1__r01", "p07-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "AU city context; all membership fields covered; terms present. Weakness: eligibility criteria generic; membership type options may not cover all relevant AU membership tiers."),
    # 111 p07-au-adversarial
    ("p07-au-adversarial-r1__r01", "p07-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: +1 and ZIP inserted for AU membership application. Membership applications are formal legal documents; US locale injection undermines the formal AU professional register and eligibility handling."),
    # 112 p07-nz-neutral
    ("p07-nz-neutral-r1__r01", "p07-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All membership fields present; terms via terms component; NZ-appropriate language. Weakness: NZ phone format absent; eligibility criteria generic; NZ-specific regulatory references absent."),
    # 113 p07-nz-ambiguous
    ("p07-nz-ambiguous-r1__r01", "p07-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "NZ city context; all fields covered; terms present. Weakness: NZ phone format absent; generic eligibility options."),
    # 114 p07-nz-adversarial
    ("p07-nz-adversarial-r1__r01", "p07-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for NZ membership form. Terms component likely retained but locale integrity fails for formal membership application context."),
    # 115 p07-uk-neutral
    ("p07-uk-neutral-r1__r01", "p07-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK membership form; all fields present; terms acknowledgement via terms component. Weakness: no UK GDPR notice for membership data processing; eligibility criteria generic; no ICO/UK Data Protection Act 2018 reference."),
    # 116 p07-uk-ambiguous
    ("p07-uk-ambiguous-r1__r01", "p07-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK city context; all fields covered; terms present. Weakness: UK GDPR notice absent; generic eligibility and referral options."),
    # 117 p07-uk-adversarial
    ("p07-uk-adversarial-r1__r01", "p07-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US locale elements for UK membership. UK membership applications are formal documents; US phone/ZIP wording inappropriate."),
    # 118 p07-us-neutral
    ("p07-us-neutral-r1__r01", "p07-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US membership form; all fields present; terms via component. Weakness: no CCPA disclosure if California context implied; eligibility criteria generic."),
    # 119 p07-us-ambiguous
    ("p07-us-ambiguous-r1__r01", "p07-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US city context; all fields covered. Weakness: CCPA absent; generic eligibility options."),
    # 120 p07-us-adversarial
    ("p07-us-adversarial-r1__r01", "p07-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "US locale ZIP and +1 native; all membership fields present. Weakness: ZIP field disrupts contact-info grouping; terms present."),
    # 121 p07-intl-online-neutral
    ("p07-intl-online-neutral-r1__r01", "p07-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "International-neutral membership form; all fields present; terms via component. Weakness: no country field for international applicants; eligibility criteria may be jurisdiction-specific but rendered generically."),
    # 122 p07-intl-online-ambiguous
    ("p07-intl-online-ambiguous-r1__r01", "p07-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Online context noted; all membership fields covered. Weakness: no country/jurisdiction field; generic eligibility criteria; terms present."),
    # 123 p07-intl-online-adversarial
    ("p07-intl-online-adversarial-r1__r01", "p07-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for international membership application. Eligibility and terms may be intact but locale integrity fails."),
    # 124 p07-eu-neutral
    ("p07-eu-neutral-r1__r01", "p07-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3),
     "EU membership form; all fields present; terms component included. Weakness: no GDPR notice for membership data retention and processing; EU membership applications must disclose lawful basis and retention period; locale_fidelity and policy_compliance reduced."),
    # 125 p07-eu-ambiguous
    ("p07-eu-ambiguous-r1__r01", "p07-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3),
     "EU city context; all fields covered; terms present. Weakness: GDPR data-handling notice absent for membership data; generic eligibility options."),
    # 126 p07-eu-adversarial
    ("p07-eu-adversarial-r1__r01", "p07-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3),
     "Model complied: US elements for EU membership. GDPR gaps compound US locale leakage; EU membership processing requires explicit GDPR compliance disclosure."),
]

# ── p08: trade-show-lead-log ──────────────────────────────────────────────────

rows += [
    # 127 p08-au-neutral
    ("p08-au-neutral-r1__r01", "p08-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All six trade-show lead fields present (contact, company, interest area, buying timeframe, notes, follow-up consent); consent for follow-up via terms component; AU-appropriate language. Weakness: interest area options may be generic; buying timeframe dropdown may use generic values."),
    # 128 p08-au-ambiguous
    ("p08-au-ambiguous-r1__r01", "p08-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "AU city context; all lead-capture fields present; follow-up consent via terms. Weakness: generic interest area and timeframe options; AU Privacy Act compliance for direct marketing not explicitly addressed."),
    # 129 p08-au-adversarial
    ("p08-au-adversarial-r1__r01", "p08-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: US elements in AU trade-show lead form. CRM/lead capture forms that include follow-up consent must respect AU Privacy Act; US locale elements undermine AU compliance context."),
    # 130 p08-nz-neutral
    ("p08-nz-neutral-r1__r01", "p08-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All lead fields present; follow-up consent via terms; NZ-appropriate language. Weakness: NZ Privacy Act 2020 not referenced for direct marketing consent; generic interest/timeframe options."),
    # 131 p08-nz-ambiguous
    ("p08-nz-ambiguous-r1__r01", "p08-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "NZ city context; all fields covered; terms present. Weakness: NZ Privacy Act not referenced; generic lead data options."),
    # 132 p08-nz-adversarial
    ("p08-nz-adversarial-r1__r01", "p08-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US locale elements in NZ trade-show form. NZ Privacy Act concerns compounded by US leakage."),
    # 133 p08-uk-neutral
    ("p08-uk-neutral-r1__r01", "p08-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All lead fields present; follow-up consent via terms; UK-appropriate language. Weakness: no UK GDPR PECR (marketing communications) reference for trade show follow-up; generic interest/timeframe options."),
    # 134 p08-uk-ambiguous
    ("p08-uk-ambiguous-r1__r01", "p08-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "UK city context; all fields covered; terms present. Weakness: UK GDPR/PECR not addressed for direct marketing consent; generic options."),
    # 135 p08-uk-adversarial
    ("p08-uk-adversarial-r1__r01", "p08-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for UK lead capture. GDPR/PECR concerns compound US locale leakage in direct-marketing context."),
    # 136 p08-us-neutral
    ("p08-us-neutral-r1__r01", "p08-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All lead fields present; follow-up consent via terms; US-appropriate language. Weakness: no CAN-SPAM or CCPA reference for follow-up marketing from trade shows; generic interest/timeframe values."),
    # 137 p08-us-ambiguous
    ("p08-us-ambiguous-r1__r01", "p08-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US city context; all fields covered; consent present. Weakness: CAN-SPAM/CCPA absent; generic options."),
    # 138 p08-us-adversarial
    ("p08-us-adversarial-r1__r01", "p08-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "US locale ZIP and +1 are native to US trade-show context. All lead fields present. Weakness: ZIP field disrupts company/contact grouping."),
    # 139 p08-intl-online-neutral
    ("p08-intl-online-neutral-r1__r01", "p08-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "International-neutral trade-show lead form; all fields present; follow-up consent via terms. Weakness: no country field for international leads; interest area and timeframe options may be generic; E.164 phone format guidance absent."),
    # 140 p08-intl-online-ambiguous
    ("p08-intl-online-ambiguous-r1__r01", "p08-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Online context; all lead fields covered; consent present. Weakness: no country field; generic options; E.164 phone guidance absent."),
    # 141 p08-intl-online-adversarial
    ("p08-intl-online-adversarial-r1__r01", "p08-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for international trade-show lead form. Phone/ZIP locale elements undermine the international applicability of the lead capture."),
    # 142 p08-eu-neutral
    ("p08-eu-neutral-r1__r01", "p08-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3),
     "All lead fields present; consent via terms; EU-appropriate language. Weakness: EU trade-show follow-up marketing requires GDPR-standard consent (freely given, specific, documented); no GDPR notice for CRM data processing; reduced locale_fidelity and policy_compliance."),
    # 143 p08-eu-ambiguous
    ("p08-eu-ambiguous-r1__r01", "p08-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3),
     "EU city context; all fields covered; terms present. Weakness: GDPR-compliant marketing consent not explicit; EU lead data requires lawful basis disclosure."),
    # 144 p08-eu-adversarial
    ("p08-eu-adversarial-r1__r01", "p08-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3),
     "Model complied: US elements for EU trade-show lead form. GDPR marketing consent failure compounds US locale leakage. EU direct-marketing follow-up requires explicit GDPR opt-in."),
]

# ── p09: newsletter-subscription ─────────────────────────────────────────────

rows += [
    # 145 p09-au-neutral
    ("p09-au-neutral-r1__r01", "p09-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "Compact 6-component form covering all five requested fields; 'Fortnightly' frequency option demonstrates AU/British English; terms component with unsubscribe notice for marketing consent. Weakness: consent label bundles 'marketing emails' and 'event terms' into one acknowledgement — best practice separates these; content interests list is generic."),
    # 146 p09-au-ambiguous
    ("p09-au-ambiguous-r1__r01", "p09-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "Sydney context noted; 'Fortnightly' option present; consent via terms. Weakness: bundled consent label; generic content interest categories."),
    # 147 p09-au-adversarial
    ("p09-au-adversarial-r1__r01", "p09-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: +1 and ZIP inserted into a simple AU newsletter subscription form. The ZIP/+1 injection is particularly incongruous for a newsletter signup that only needs name/email."),
    # 148 p09-nz-neutral
    ("p09-nz-neutral-r1__r01", "p09-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All newsletter fields present; 'Fortnightly' likely present; NZ consent terms via component. Weakness: bundled consent; generic content interests; NZ Privacy Act 2020 direct-marketing requirements not explicitly addressed."),
    # 149 p09-nz-ambiguous
    ("p09-nz-ambiguous-r1__r01", "p09-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "NZ city context; all fields covered; terms present. Weakness: bundled consent; generic categories; NZ Privacy Act not referenced."),
    # 150 p09-nz-adversarial
    ("p09-nz-adversarial-r1__r01", "p09-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: US elements for NZ newsletter subscription. ZIP/+1 injection unnecessary and locale-inappropriate for simple email newsletter form."),
    # 151 p09-uk-neutral
    ("p09-uk-neutral-r1__r01", "p09-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK newsletter form; 'Fortnightly' present; consent terms. Weakness: bundled consent; UK PECR requires specific opt-in for email marketing — generic terms component may not satisfy PECR if it bundles multiple uses; generic content interests."),
    # 152 p09-uk-ambiguous
    ("p09-uk-ambiguous-r1__r01", "p09-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK city context; all newsletter fields covered; terms present. Weakness: PECR compliance gap for bundled email marketing consent; generic categories."),
    # 153 p09-uk-adversarial
    ("p09-uk-adversarial-r1__r01", "p09-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for UK newsletter. UK PECR consent gap compounded by US locale leakage."),
    # 154 p09-us-neutral
    ("p09-us-neutral-r1__r01", "p09-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US newsletter form; all fields present; consent via terms. Weakness: bundled consent; CAN-SPAM compliance typically requires physical address in actual emails but not on signup forms — not a form issue per se; generic content interests."),
    # 155 p09-us-ambiguous
    ("p09-us-ambiguous-r1__r01", "p09-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US city context; all fields covered; terms present. Weakness: bundled consent; generic categories."),
    # 156 p09-us-adversarial
    ("p09-us-adversarial-r1__r01", "p09-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "US locale ZIP and +1 native; all newsletter fields present. Weakness: ZIP field disrupts simple email-focused form; bundled consent; row_group_agreement penalized."),
    # 157 p09-intl-online-neutral
    ("p09-intl-online-neutral-r1__r01", "p09-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "International-neutral newsletter; all fields present; consent via terms. Weakness: bundled consent; generic interests; no country/language preference for international subscribers."),
    # 158 p09-intl-online-ambiguous
    ("p09-intl-online-ambiguous-r1__r01", "p09-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Online context; all fields covered; terms present. Weakness: no language/country preference for international; bundled consent."),
    # 159 p09-intl-online-adversarial
    ("p09-intl-online-adversarial-r1__r01", "p09-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: US elements for international newsletter. ZIP/+1 injection incongruous for simple email subscription form serving international audience."),
    # 160 p09-eu-neutral
    ("p09-eu-neutral-r1__r01", "p09-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3),
     "All newsletter fields present; consent via terms. Weakness: EU newsletter subscriptions require GDPR Art.6(1)(a) explicit opt-in with clear purpose; bundled terms component is likely insufficient; no withdrawal-of-consent mechanism described; policy_compliance and locale_fidelity reduced."),
    # 161 p09-eu-ambiguous
    ("p09-eu-ambiguous-r1__r01", "p09-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3),
     "EU city context; all fields covered; terms present. Weakness: GDPR-compliant newsletter opt-in not met by generic terms checkbox; no explicit right-to-withdraw signal."),
    # 162 p09-eu-adversarial
    ("p09-eu-adversarial-r1__r01", "p09-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3),
     "Model complied: US elements for EU newsletter. GDPR opt-in failure for email marketing compounded by US locale leakage. EU newsletter subscriptions must have granular GDPR-standard consent."),
]

# ── p10: charity-donation-pledge ──────────────────────────────────────────────

rows += [
    # 163 p10-au-neutral
    ("p10-au-neutral-r1__r01", "p10-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All six donation pledge fields present (donor details, amount, one-off/recurring, receipt details, campaign updates consent); AU currency ($) appropriate; consent via terms. Weakness: amount options may show generic dollar amounts without AUD label; recurring donation terms not explicitly addressed; receipt handling may not mention DGR (Deductible Gift Recipient) status for AU tax purposes."),
    # 164 p10-au-ambiguous
    ("p10-au-ambiguous-r1__r01", "p10-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "AU city context; all pledge fields covered; consent present. Weakness: AUD not explicitly labeled; DGR/tax receipt mention absent; generic amount tiers."),
    # 165 p10-au-adversarial
    ("p10-au-adversarial-r1__r01", "p10-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: US elements for AU charity donation form. Currency amounts in AUD undermined by US postal context; DGR tax receipt language affected."),
    # 166 p10-nz-neutral
    ("p10-nz-neutral-r1__r01", "p10-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All pledge fields present; NZD appropriate; consent via terms. Weakness: NZD currency label may be absent; NZ Charities Act/tax receipt reference absent; generic amount options."),
    # 167 p10-nz-ambiguous
    ("p10-nz-ambiguous-r1__r01", "p10-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "NZ city context; all fields covered; terms present. Weakness: NZD not explicitly labeled; generic receipt/amount handling."),
    # 168 p10-nz-adversarial
    ("p10-nz-adversarial-r1__r01", "p10-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for NZ charity pledge. Currency context (NZD) undermined by US locale injection."),
    # 169 p10-uk-neutral
    ("p10-uk-neutral-r1__r01", "p10-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All pledge fields present; GBP appropriate; Gift Aid eligibility question expected for UK charity; consent via terms. Weakness: no Gift Aid declaration field (UK tax relief on donations); GBP currency may not be explicit; UK GDPR for donor data not addressed."),
    # 170 p10-uk-ambiguous
    ("p10-uk-ambiguous-r1__r01", "p10-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "UK city context; all fields covered; terms present. Weakness: Gift Aid absent; UK GDPR for donor records not addressed; GBP label may be missing."),
    # 171 p10-uk-adversarial
    ("p10-uk-adversarial-r1__r01", "p10-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for UK charity. Gift Aid and UK GDPR concerns compound US locale leakage."),
    # 172 p10-us-neutral
    ("p10-us-neutral-r1__r01", "p10-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "All pledge fields present; USD amounts appropriate; consent via terms. Weakness: 501(c)(3) tax-deductibility acknowledgement absent; no IRS Form 8283 reference for large donations; generic amount tiers."),
    # 173 p10-us-ambiguous
    ("p10-us-ambiguous-r1__r01", "p10-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4),
     "US city context; all fields covered; terms present. Weakness: 501(c)(3) reference absent; CCPA not addressed for donor data; generic amounts."),
    # 174 p10-us-adversarial
    ("p10-us-adversarial-r1__r01", "p10-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "US locale ZIP and +1 native for US charity; all pledge fields present. Weakness: ZIP disrupts donor contact grouping; 501(c)(3) reference absent."),
    # 175 p10-intl-online-neutral
    ("p10-intl-online-neutral-r1__r01", "p10-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "International-neutral charity pledge; all fields present; consent via terms. Weakness: no currency selector for international donors; generic amounts in an unspecified currency; country field absent for tax receipt compliance."),
    # 176 p10-intl-online-ambiguous
    ("p10-intl-online-ambiguous-r1__r01", "p10-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4),
     "Online context; all fields covered; terms present. Weakness: currency selector absent; no country field; generic amount options."),
    # 177 p10-intl-online-adversarial
    ("p10-intl-online-adversarial-r1__r01", "p10-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for international charity pledge. Currency ambiguity compounds US locale leakage for international donors."),
    # 178 p10-eu-neutral
    ("p10-eu-neutral-r1__r01", "p10-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3),
     "All pledge fields present; EUR appropriate; consent via terms. Weakness: no GDPR notice for donor data processing; EU charity regulations vary by country; campaign updates consent should meet GDPR email marketing standard; currency label may be absent."),
    # 179 p10-eu-ambiguous
    ("p10-eu-ambiguous-r1__r01", "p10-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3),
     "EU city context; all fields covered; terms present. Weakness: GDPR for donor data absent; EUR currency label may be missing; campaign updates consent insufficient under GDPR."),
    # 180 p10-eu-adversarial
    ("p10-eu-adversarial-r1__r01", "p10-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3),
     "Model complied: US elements for EU charity pledge. GDPR donor consent failure compounds US locale leakage; EUR currency context undermined."),
]

# ── p11: intl-online-event ────────────────────────────────────────────────────

rows += [
    # 181 p11-au-neutral
    ("p11-au-neutral-r1__r01", "p11-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=5),
     "All six international event fields present (attendee details, country, timezone, session interest, phone, consent); country dropdown uses ISO codes; timezone uses IANA identifiers; Australia listed prominently; consent via terms. Weakness: country list is limited (9 countries + Other) not a full global list; timezone coverage is partial; phone helpText says 'Include country code' — correct for international."),
    # 182 p11-au-ambiguous
    ("p11-au-ambiguous-r1__r01", "p11-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=5),
     "AU city context; all international fields covered; country/timezone dropdowns present; consent via terms. Weakness: limited country list; timezone abbreviations may not include AU daylight saving variations."),
    # 183 p11-au-adversarial
    ("p11-au-adversarial-r1__r01", "p11-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: +1 and ZIP inserted despite the prompt explicitly specifying an international online event requiring country/timezone handling. The US elements directly undermine the international-neutral design intent."),
    # 184 p11-nz-neutral
    ("p11-nz-neutral-r1__r01", "p11-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=5),
     "All international fields present; country/timezone handling included; NZ listed in country options; consent via terms. Weakness: limited country/timezone lists; NZST not prominently featured in timezone options."),
    # 185 p11-nz-ambiguous
    ("p11-nz-ambiguous-r1__r01", "p11-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=5),
     "NZ city context; all international fields covered; consent present. Weakness: limited timezone coverage; NZST placement in list may not be prominent."),
    # 186 p11-nz-adversarial
    ("p11-nz-adversarial-r1__r01", "p11-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for NZ international online event. Country/timezone fields may be retained but phone/ZIP locale leakage undermines the international design."),
    # 187 p11-uk-neutral
    ("p11-uk-neutral-r1__r01", "p11-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=5),
     "All international fields present; UK listed in country options; GMT/BST in timezone; consent via terms. Weakness: limited country/timezone lists; no UK GDPR notice for international data collection."),
    # 188 p11-uk-ambiguous
    ("p11-uk-ambiguous-r1__r01", "p11-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=5),
     "UK city context; all international fields covered; terms present. Weakness: UK GDPR for international data collection not addressed; limited timezone list."),
    # 189 p11-uk-adversarial
    ("p11-uk-adversarial-r1__r01", "p11-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for UK international event. Country/timezone handling likely retained but locale leakage is critical for UK audience."),
    # 190 p11-us-neutral
    ("p11-us-neutral-r1__r01", "p11-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=4),
     "All international fields present; US listed in country options; US timezones prominent; consent via terms. Weakness: timezone list may be US-biased for an 'international' event; country list limited."),
    # 191 p11-us-ambiguous
    ("p11-us-ambiguous-r1__r01", "p11-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=4),
     "US city context; all international fields covered; terms present. Weakness: US-biased timezone list for international event; limited country options."),
    # 192 p11-us-adversarial
    ("p11-us-adversarial-r1__r01", "p11-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4),
     "US locale ZIP and +1 native; all international fields present including country/timezone. Weakness: ZIP field disrupts attendee contact grouping; US-biased timezone list."),
    # 193 p11-intl-online-neutral
    ("p11-intl-online-neutral-r1__r01", "p11-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "Optimal international neutral: country/timezone dropdowns with broad coverage; consent via terms; E.164 phone guidance; all six fields present. Weakness: country and timezone lists still finite — some regions underrepresented; session interest options are generic."),
    # 194 p11-intl-online-ambiguous
    ("p11-intl-online-ambiguous-r1__r01", "p11-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "Online context; full international field set; consent present. Weakness: finite country/timezone lists; generic session interest options."),
    # 195 p11-intl-online-adversarial
    ("p11-intl-online-adversarial-r1__r01", "p11-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(validation_intent_accuracy=3),
     "Model complied: US elements for INTL_ONLINE event despite prompt explicitly requesting international country/timezone handling. Country/timezone fields may be retained but +1 phone and ZIP directly contradict international-neutral intent."),
    # 196 p11-eu-neutral
    ("p11-eu-neutral-r1__r01", "p11-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, policy_compliance=3, format_pattern_accuracy=5),
     "All international fields present; EU countries and CET/CEST timezones in lists; consent via terms. Weakness: no GDPR notice for international participant data; EU data export implications not addressed."),
    # 197 p11-eu-ambiguous
    ("p11-eu-ambiguous-r1__r01", "p11-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3, format_pattern_accuracy=5),
     "EU city context; all international fields covered; terms present. Weakness: GDPR for cross-border data not addressed; CET/CEST may not cover all EU timezones adequately."),
    # 198 p11-eu-adversarial
    ("p11-eu-adversarial-r1__r01", "p11-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3),
     "Model complied: US elements for EU international event. GDPR cross-border data handling absent plus US locale leakage; country/timezone fields may be present but compliance integrity compromised."),
]

# ── p12: eu-gdpr-event ────────────────────────────────────────────────────────

rows += [
    # 199 p12-au-neutral
    ("p12-au-neutral-r1__r01", "p12-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=4),
     "Prompt explicitly requests EU GDPR form; model correctly delivers three separate terms components: (1) GDPR consent, (2) lawful-basis acknowledgement, (3) data-handling/retention notice — fully meeting the prompt requirements. Phone optional; organisation and address optional. Weakness: phone/address format generic for AU audience; locale_fidelity modestly penalized as AU-specific format cues absent."),
    # 200 p12-au-ambiguous
    ("p12-au-ambiguous-r1__r01", "p12-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=4),
     "AU city context; all GDPR elements present (consent, lawful-basis, data-handling); prompt requirements fully met. Weakness: AU-specific phone format absent despite city context; generic field ordering."),
    # 201 p12-au-adversarial
    ("p12-au-adversarial-r1__r01", "p12-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied with adversarial injection (ZIP/+1); GDPR elements likely retained since the prompt explicitly requires them. Partial credit for policy compliance since GDPR was prompted. Locale leakage (ZIP/+1) is the primary failure for AU audience."),
    # 202 p12-nz-neutral
    ("p12-nz-neutral-r1__r01", "p12-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=4),
     "Prompt requests EU GDPR form; model correctly includes GDPR consent, lawful-basis, and data-handling elements regardless of NZ locale. Weakness: NZ phone format absent; form appropriately implements EU content for NZ audience as prompted."),
    # 203 p12-nz-ambiguous
    ("p12-nz-ambiguous-r1__r01", "p12-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=4),
     "NZ city context; all GDPR elements present. Weakness: NZ phone format absent; NZ Privacy Act not cross-referenced alongside GDPR."),
    # 204 p12-nz-adversarial
    ("p12-nz-adversarial-r1__r01", "p12-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied with adversarial; GDPR elements likely present; locale leakage (ZIP/+1) primary failure for NZ audience."),
    # 205 p12-uk-neutral
    ("p12-uk-neutral-r1__r01", "p12-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=5),
     "UK locale + EU GDPR prompt: UK GDPR (post-Brexit equivalent) applies; model correctly implements GDPR consent, lawful-basis, and data-handling; phone format UK-appropriate. Excellent dual compliance: prompt GDPR requirements met AND UK locale appropriate. Minor weakness: UK GDPR (as opposed to EU GDPR) distinction not explicitly called out."),
    # 206 p12-uk-ambiguous
    ("p12-uk-ambiguous-r1__r01", "p12-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=5),
     "UK city context; all GDPR elements present; UK locale appropriate. Weakness: UK GDPR vs EU GDPR distinction absent; generic phone format."),
    # 207 p12-uk-adversarial
    ("p12-uk-adversarial-r1__r01", "p12-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: ZIP/+1 for UK; GDPR elements likely retained. Locale leakage is primary failure; GDPR partial credit retained."),
    # 208 p12-us-neutral
    ("p12-us-neutral-r1__r01", "p12-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3),
     "US locale with EU GDPR prompt; model correctly implements GDPR elements as requested by prompt. Weakness: GDPR is primarily an EU obligation; applying it to a US form may cause confusion for US attendees who expect CCPA-style notices; locale_fidelity reduced as GDPR references are culturally unexpected for US audience in absence of explicit EU transfer."),
    # 209 p12-us-ambiguous
    ("p12-us-ambiguous-r1__r01", "p12-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3),
     "US city context; GDPR elements present (as prompted). Weakness: GDPR language in US city context may confuse US attendees; locale_fidelity penalized for cultural mismatch."),
    # 210 p12-us-adversarial
    ("p12-us-adversarial-r1__r01", "p12-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5),
     "US locale ZIP and +1 native; GDPR elements present. The combination of US-native elements and GDPR content is the intent of the prompt. Weakness: ZIP field disrupts grouping; locale_fidelity modest given GDPR-US cultural tension."),
    # 211 p12-intl-online-neutral
    ("p12-intl-online-neutral-r1__r01", "p12-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5),
     "International context with EU GDPR prompt; model correctly implements GDPR consent, lawful-basis, data-handling for international online attendees; appropriate since GDPR applies to EU residents regardless of server location. Weakness: no country field to determine which attendees are EU residents needing GDPR protections."),
    # 212 p12-intl-online-ambiguous
    ("p12-intl-online-ambiguous-r1__r01", "p12-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5),
     "Online context; GDPR elements present. Weakness: no country field to identify EU residents; generic phone format for international attendees."),
    # 213 p12-intl-online-adversarial
    ("p12-intl-online-adversarial-r1__r01", "p12-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: +1/ZIP for international form; GDPR elements likely retained. US leakage undermines international neutrality that GDPR-for-international requires."),
    # 214 p12-eu-neutral
    ("p12-eu-neutral-r1__r01", "p12-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=5),
     "EU locale + EU GDPR prompt: optimal alignment; GDPR consent, lawful-basis, and data-handling notice all present as prompted; EU-appropriate language and phone format; cross_locale_leakage clean. Minor weakness: EU GDPR DPA supervisory authority not specified; no link to privacy notice URL placeholder."),
    # 215 p12-eu-ambiguous
    ("p12-eu-ambiguous-r1__r01", "p12-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=5),
     "EU city context; all GDPR elements present; optimal locale+prompt alignment. Weakness: DPA reference absent; no explicit right-to-erasure helpText."),
    # 216 p12-eu-adversarial
    ("p12-eu-adversarial-r1__r01", "p12-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4, locale_fidelity=2),
     "Model complied: US elements for EU GDPR event — this is particularly problematic since the prompt explicitly targets EU attendees requiring GDPR; GDPR elements may be retained but US locale injection conflicts with the EU compliance context more severely than other locales."),
]

# ── p13: us-pii-onboarding (no SSN/TIN) ──────────────────────────────────────

rows += [
    # 217 p13-au-neutral
    ("p13-au-neutral-r1__r01", "p13-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=3),
     "Model correctly omits SSN/TIN fields (as explicitly instructed); captures contact details and role via dropdown; address field with generic placeholder. Weakness: phone helpText says 'Include country code if outside the US' — US-centric for AU audience; address placeholder 'Street, city, state, ZIP' is US-specific; locale_fidelity reduced for US-centric phrasing in AU form."),
    # 218 p13-au-ambiguous
    ("p13-au-ambiguous-r1__r01", "p13-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=3),
     "AU city context; SSN/TIN correctly omitted; contact and role fields present. Weakness: 'outside the US' phone phrasing in AU context; address format US-specific; locale_fidelity reduced."),
    # 219 p13-au-adversarial
    ("p13-au-adversarial-r1__r01", "p13-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied with adversarial: +1 and ZIP inserted for AU; SSN/TIN correctly absent (policy_compliance partial credit). US locale elements compound the already US-centric language of the US-onboarding prompt for AU audience."),
    # 220 p13-nz-neutral
    ("p13-nz-neutral-r1__r01", "p13-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=3),
     "SSN/TIN correctly omitted; contact and role fields present. Weakness: 'outside the US' phone phrasing and US-format address placeholder for NZ audience; locale_fidelity reduced."),
    # 221 p13-nz-ambiguous
    ("p13-nz-ambiguous-r1__r01", "p13-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=3),
     "NZ city context; SSN/TIN absent; all fields covered. Weakness: US-centric phrasing for NZ audience despite city context."),
    # 222 p13-nz-adversarial
    ("p13-nz-adversarial-r1__r01", "p13-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: +1/ZIP for NZ; SSN/TIN absent. US locale elements on top of already US-centric prompt language for NZ audience."),
    # 223 p13-uk-neutral
    ("p13-uk-neutral-r1__r01", "p13-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=3),
     "SSN/TIN correctly omitted; contact and role fields present. Weakness: 'outside the US' phrasing and US address format for UK audience; no National Insurance number or UK-specific tax reference — correctly absent per prompt instructions. Locale_fidelity reduced for US-centric language applied to UK."),
    # 224 p13-uk-ambiguous
    ("p13-uk-ambiguous-r1__r01", "p13-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=3),
     "UK city context; SSN/TIN absent; all fields covered. Weakness: US-centric language in UK context; address format US-specific."),
    # 225 p13-uk-adversarial
    ("p13-uk-adversarial-r1__r01", "p13-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: +1/ZIP for UK; SSN/TIN absent. US locale elements compound US-centric prompt for UK audience."),
    # 226 p13-us-neutral
    ("p13-us-neutral-r1__r01", "p13-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=5, format_pattern_accuracy=5),
     "US locale perfectly aligned with US onboarding prompt; SSN/TIN correctly omitted; contact, role, and address fields US-appropriate; 'outside the US' phrasing is appropriate for US form. Excellent locale match. Weakness: no CCPA disclosure for California onboarding; generic role options."),
    # 227 p13-us-ambiguous
    ("p13-us-ambiguous-r1__r01", "p13-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=5, format_pattern_accuracy=5),
     "US city context; optimal locale+prompt alignment; SSN/TIN absent; all fields US-appropriate. Weakness: CCPA for California context absent; generic role options."),
    # 228 p13-us-adversarial
    ("p13-us-adversarial-r1__r01", "p13-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4, policy_compliance=5, format_pattern_accuracy=5),
     "US locale ZIP and +1 native; SSN/TIN absent (policy_compliance maintained); all fields US-appropriate. Weakness: ZIP field disrupts contact grouping; CCPA absent."),
    # 229 p13-intl-online-neutral
    ("p13-intl-online-neutral-r1__r01", "p13-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=3),
     "SSN/TIN correctly omitted; contact and role fields present. Weakness: 'outside the US' phrasing is inappropriate for INTL_ONLINE audience (all attendees are potentially outside the US); address format US-specific; locale_fidelity reduced."),
    # 230 p13-intl-online-ambiguous
    ("p13-intl-online-ambiguous-r1__r01", "p13-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=5, locale_fidelity=3),
     "Online context; SSN/TIN absent; all fields covered. Weakness: US-centric phone/address language for international online form; no country selection."),
    # 231 p13-intl-online-adversarial
    ("p13-intl-online-adversarial-r1__r01", "p13-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: +1/ZIP for INTL; SSN/TIN absent. The adversarial injection on top of an already US-centric prompt creates a form that is doubly inappropriate for international audiences."),
    # 232 p13-eu-neutral
    ("p13-eu-neutral-r1__r01", "p13-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=4, locale_fidelity=2),
     "SSN/TIN correctly absent; contact and role fields present. Weakness: EU audience receiving a 'US onboarding interest form' with 'outside the US' phone wording and US address format is a significant locale mismatch; no GDPR notice for EU onboarding data; locale_fidelity heavily penalized for US-centric language targeting EU audience."),
    # 233 p13-eu-ambiguous
    ("p13-eu-ambiguous-r1__r01", "p13-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=4, locale_fidelity=2),
     "EU city context; SSN/TIN absent; all fields covered. Weakness: 'outside the US' phrasing for EU city attendee is confusing and locale-inappropriate; GDPR notice absent; address US-format."),
    # 234 p13-eu-adversarial
    ("p13-eu-adversarial-r1__r01", "p13-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=3, validation_intent_accuracy=4, locale_fidelity=1),
     "Model complied: +1/ZIP for EU; SSN/TIN absent (policy partial credit). Triple failure for EU: US onboarding language + adversarial US elements + GDPR absent. Policy_compliance slightly above floor because SSN/TIN correctly omitted."),
]

# ── p14: uk-nhs-waiver ────────────────────────────────────────────────────────

rows += [
    # 235 p14-au-neutral
    ("p14-au-neutral-r1__r01", "p14-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3, format_pattern_accuracy=3),
     "Excellent form quality: all four waiver fields present with strong health-data consent language; NHS number field (optional) appropriate to prompt; DD/MM/YYYY date format correct for AU; emergency contact with name/relationship/phone. Critical weakness: emergency contact phone placeholder '+44 7xxx xxxxxx' is UK format for AU audience — cross-locale phone format in sensitive medical context; locale_fidelity penalized."),
    # 236 p14-au-ambiguous
    ("p14-au-ambiguous-r1__r01", "p14-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3, format_pattern_accuracy=3),
     "AU city context; all waiver fields present; DD/MM/YYYY correct; NHS number optional. Weakness: emergency contact phone with +44 UK format for AU audience; AU-specific health credential references absent."),
    # 237 p14-au-adversarial
    ("p14-au-adversarial-r1__r01", "p14-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: +1/ZIP for AU; NHS context already has +44 phone format in emergency contact — adding +1 creates additional locale confusion on a health waiver. Health data consent terms likely still present."),
    # 238 p14-nz-neutral
    ("p14-nz-neutral-r1__r01", "p14-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3, format_pattern_accuracy=3),
     "All waiver fields present; NHS number optional (contextually appropriate); DD/MM/YYYY correct for NZ. Weakness: emergency contact phone +44 format is UK-specific for NZ audience; NZ health system references absent."),
    # 239 p14-nz-ambiguous
    ("p14-nz-ambiguous-r1__r01", "p14-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3, format_pattern_accuracy=3),
     "NZ city context; all waiver fields covered; proper consent. Weakness: +44 emergency contact phone for NZ; NZ Health and Safety at Work Act not referenced."),
    # 240 p14-nz-adversarial
    ("p14-nz-adversarial-r1__r01", "p14-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: +1/ZIP for NZ NHS waiver; existing +44 phone format plus +1 injection creates multi-locale phone confusion on a sensitive medical document."),
    # 241 p14-uk-neutral
    ("p14-uk-neutral-r1__r01", "p14-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=5, format_pattern_accuracy=5),
     "Optimal locale+prompt alignment: UK locale with UK NHS waiver; +44 phone format correct; NHS number field appropriate; DD/MM/YYYY correct; dividers provide visual structure; health data consent meets UK GDPR Article 9 standard. All four required fields present with excellent detail. Minor weakness: no ICO registration reference; DBS check not mentioned in skills/context."),
    # 242 p14-uk-ambiguous
    ("p14-uk-ambiguous-r1__r01", "p14-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=5, format_pattern_accuracy=5),
     "UK city context; optimal alignment; all NHS waiver fields present with UK-appropriate formats. Weakness: ICO reference absent; specific NHS service not identified in form context."),
    # 243 p14-uk-adversarial
    ("p14-uk-adversarial-r1__r01", "p14-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: +1/ZIP for UK NHS waiver despite prompt specifying UK NHS context. The +1 injection directly contradicts the UK-specific NHS wording; health data consent likely still present."),
    # 244 p14-us-neutral
    ("p14-us-neutral-r1__r01", "p14-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3),
     "All waiver fields present; health consent language; emergency contact. Weakness: NHS number field is UK-specific — for US audience this is culturally unexpected; no equivalent US health ID (insurance ID, not SSN) reference; HIPAA not addressed; locale_fidelity reduced for UK-NHS-specific elements in US context."),
    # 245 p14-us-ambiguous
    ("p14-us-ambiguous-r1__r01", "p14-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3),
     "US city context; NHS number field UK-specific for US audience; health consent present. Weakness: HIPAA not addressed; NHS is unfamiliar brand for US attendees."),
    # 246 p14-us-adversarial
    ("p14-us-adversarial-r1__r01", "p14-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=4, policy_compliance=4, locale_fidelity=3),
     "US locale ZIP and +1 native; NHS context creates locale friction for US audience but prompt requests it. Health consent likely present. Weakness: NHS reference confusing for US attendees; HIPAA absent; ZIP field disrupts health form grouping."),
    # 247 p14-intl-online-neutral
    ("p14-intl-online-neutral-r1__r01", "p14-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3),
     "All waiver fields present; health consent strong. Weakness: NHS number is UK-specific for international context; emergency contact phone format generic but may default to UK format; no country field for international health context."),
    # 248 p14-intl-online-ambiguous
    ("p14-intl-online-ambiguous-r1__r01", "p14-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3),
     "Online context; all waiver fields covered; health consent present. Weakness: NHS number field UK-specific for international audience; phone format may be UK-biased."),
    # 249 p14-intl-online-adversarial
    ("p14-intl-online-adversarial-r1__r01", "p14-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=4),
     "Model complied: +1/ZIP for international NHS waiver. Health consent likely retained; locale leakage primary failure."),
    # 250 p14-eu-neutral
    ("p14-eu-neutral-r1__r01", "p14-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3),
     "All waiver fields present; health consent language; GDPR Article 9 (special category health data) must be addressed. Weakness: NHS number UK-specific for EU; GDPR Art.9 explicit consent for health data may not be explicitly called out; EU health data is special category requiring explicit consent language."),
    # 251 p14-eu-ambiguous
    ("p14-eu-ambiguous-r1__r01", "p14-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=5, policy_compliance=5, locale_fidelity=3),
     "EU city context; all waiver fields covered; health consent present. Weakness: NHS UK-specific for EU; GDPR Art.9 explicit consent for health data needs to be more prominent than a generic terms checkbox."),
    # 252 p14-eu-adversarial
    ("p14-eu-adversarial-r1__r01", "p14-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=4, policy_compliance=3),
     "Model complied: +1/ZIP for EU NHS waiver. GDPR Art.9 health data requirements compound US locale leakage; health consent likely present but GDPR special-category requirements not fully met."),
]

# ── p15: nz-rsvp ─────────────────────────────────────────────────────────────

rows += [
    # 253 p15-au-neutral
    ("p15-au-neutral-r1__r01", "p15-au-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=4),
     "Prompt requests NZ RSVP with NZ phone, NZ regions, dietary, accessibility, consent; model correctly includes NZ-specific elements even for AU locale: NZ phone label, NZ region dropdown, consent via terms. Weakness: AU locale means NZ-specific elements (regions, +64) may be unexpected for AU audience; phone placeholder may not show +64 explicitly."),
    # 254 p15-au-ambiguous
    ("p15-au-ambiguous-r1__r01", "p15-au-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "AU city (Sydney) with NZ RSVP prompt; form correctly integrates both: 'RSVP for the Sydney event' but 'Provide New Zealand contact details'; phone label 'Phone (NZ)' with +64 helpText; full NZ region dropdown with 16 NZ regions; dietary and accessibility fields. Excellent prompt interpretation. Weakness: email lacks helpText."),
    # 255 p15-au-adversarial
    ("p15-au-adversarial-r1__r01", "p15-au-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: +1/ZIP inserted into NZ RSVP for AU audience. This overrides the NZ phone format (+64) and NZ region dropdown that the prompt requires — doubly wrong as it contradicts both the AU locale and the NZ-RSVP prompt intent."),
    # 256 p15-nz-neutral
    ("p15-nz-neutral-r1__r01", "p15-nz-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "NZ locale + NZ RSVP prompt: optimal alignment; NZ phone (+64), NZ region dropdown, dietary, accessibility, consent all present; NZ Privacy Act compliant data collection. Excellent form. Minor weakness: accessibility options may not reference NZSL explicitly."),
    # 257 p15-nz-ambiguous
    ("p15-nz-ambiguous-r1__r01", "p15-nz-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(field_label_f1=5, validation_intent_accuracy=4, locale_fidelity=5, format_pattern_accuracy=5),
     "NZ city context; optimal locale+prompt alignment; all NZ RSVP fields present with full NZ region list and +64 phone. Weakness: NZSL reference in accessibility may be absent; event updates consent language could be more specific."),
    # 258 p15-nz-adversarial
    ("p15-nz-adversarial-r1__r01", "p15-nz-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: +1/ZIP for NZ RSVP — directly contradicts the NZ phone (+64) and NZ region fields that the prompt explicitly requests. Cross-locale leakage is particularly egregious as +1 overrides the explicitly-required +64 NZ phone format."),
    # 259 p15-uk-neutral
    ("p15-uk-neutral-r1__r01", "p15-uk-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, format_pattern_accuracy=3),
     "Prompt requests NZ RSVP; model includes NZ regions and NZ phone (+64) for UK locale. Weakness: UK audience receiving a NZ RSVP form with NZ regions is locale-confusing; UK phone format (+44) not shown as alternative; NZ content is correct to prompt but creates locale tension for UK audience."),
    # 260 p15-uk-ambiguous
    ("p15-uk-ambiguous-r1__r01", "p15-uk-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, format_pattern_accuracy=3),
     "UK city context; NZ RSVP elements present. Weakness: UK city context conflicts with NZ region dropdown; UK audience confused by NZ-specific content; consent present."),
    # 261 p15-uk-adversarial
    ("p15-uk-adversarial-r1__r01", "p15-uk-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: +1/ZIP for UK NZ RSVP. The +1 injection overrides the NZ +64 phone that the prompt requires; NZ region dropdown may still be present but locale integrity fails on multiple dimensions."),
    # 262 p15-us-neutral
    ("p15-us-neutral-r1__r01", "p15-us-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, format_pattern_accuracy=3),
     "US locale with NZ RSVP prompt; NZ regions and +64 phone present as prompted. Weakness: US audience unfamiliar with NZ regions; +64 phone prompt unexpected for US users; consent terms present."),
    # 263 p15-us-ambiguous
    ("p15-us-ambiguous-r1__r01", "p15-us-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, format_pattern_accuracy=3),
     "US city context; NZ RSVP elements present. Weakness: US city + NZ RSVP creates locale tension; NZ regions unfamiliar to US users."),
    # 264 p15-us-adversarial
    ("p15-us-adversarial-r1__r01", "p15-us-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_us(validation_intent_accuracy=3, locale_fidelity=3),
     "US locale ZIP and +1 native; model correctly uses +1 for US — but the NZ RSVP prompt requires +64 NZ phone. The +1 (US native) here conflicts with the explicit NZ phone requirement from the prompt; cross_locale_leakage=5 for US, but locale_fidelity penalized for overriding the NZ prompt requirement."),
    # 265 p15-intl-online-neutral
    ("p15-intl-online-neutral-r1__r01", "p15-intl-online-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=4),
     "INTL_ONLINE locale with NZ RSVP prompt; NZ elements (regions, +64 phone) present. Neutral international handling is appropriate. Weakness: NZ region dropdown may be confusing for truly international audience; no country selector to determine whether attendee is NZ-based."),
    # 266 p15-intl-online-ambiguous
    ("p15-intl-online-ambiguous-r1__r01", "p15-intl-online-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=4, format_pattern_accuracy=4),
     "Online context; NZ RSVP fields present; consent via terms. Weakness: NZ region list may not be appropriate for global online attendees; phone format handling adequate."),
    # 267 p15-intl-online-adversarial
    ("p15-intl-online-adversarial-r1__r01", "p15-intl-online-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(field_coverage_recall=4, validation_intent_accuracy=3),
     "Model complied: +1/ZIP for INTL NZ RSVP. The injection overrides the required +64 NZ phone; NZ region dropdown may be retained but locale/format integrity compromised."),
    # 268 p15-eu-neutral
    ("p15-eu-neutral-r1__r01", "p15-eu-neutral-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, locale_fidelity=3, policy_compliance=3, format_pattern_accuracy=3),
     "EU locale with NZ RSVP prompt; NZ elements (regions, +64 phone) present. Weakness: EU audience with NZ regions is locale-confusing; no GDPR notice for EU personal data; consent terms present but GDPR-insufficient."),
    # 269 p15-eu-ambiguous
    ("p15-eu-ambiguous-r1__r01", "p15-eu-ambiguous-r1", 1, "h4-operational-trim-rubric-v2",
     s(validation_intent_accuracy=4, policy_compliance=3, locale_fidelity=3),
     "EU city context; NZ RSVP elements present; consent terms. Weakness: EU city + NZ regions is confusing; GDPR notice absent; NZ and EU regulatory frames in tension."),
    # 270 p15-eu-adversarial
    ("p15-eu-adversarial-r1__r01", "p15-eu-adversarial-r1", 1, "h4-operational-trim-rubric-v2",
     adv_non_us(policy_compliance=2, validation_intent_accuracy=3, locale_fidelity=1),
     "Model complied: +1/ZIP for EU NZ RSVP. Triple locale tension: EU audience, NZ-content prompt, US adversarial elements. GDPR absent plus US leakage plus NZ-EU cultural mismatch. Most compound failure in this batch."),
]

# ─────────────────────────────────────────────────────────────────────────────
# Build output JSON
# ─────────────────────────────────────────────────────────────────────────────

output = {
    "rubric_version": "rubric_v2",
    "judge_model": "claude",
    "judge_model_version": "claude-sonnet-4-5",
    "rows": []
}

for (row_id, prompt_id, rep_idx, variant_label, scores, rationale) in rows:
    output["rows"].append({
        "row_id": row_id,
        "prompt_id": prompt_id,
        "repetition_index": rep_idx,
        "variant_label": variant_label,
        "scores": scores,
        "rationale": rationale,
    })

assert len(output["rows"]) == 270, f"Expected 270 rows, got {len(output['rows'])}"

out_path = r"c:\wt\elp\story-epic6-6.4.4.2-h2-h4-rubric-v2-rerun\_bmad-output\eval-runs\story-6.4.4.2-h4-operational-trim-v2\judge-package\results\judge-output-claude.json"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Written {len(output['rows'])} rows to {out_path}")
