---
name: ebola-bundibugyo-authorized-sources
description: "Consult this skill whenever generating, verifying, or evaluating any claim related to the 2026 Bundibugyo Ebola outbreak in DRC and Uganda. Covers: authorized source tiers, what each source is authoritative for, refresh intervals, what is NEVER permitted to claim, LLM system prompt rules, counter-message safety rules, escalation triggers, and community context guidelines. Trigger this skill before any LLM verification call, before generating any counter-message, and before citing any source in a response. Do NOT rely on model training data for outbreak-specific facts — always route through Tier 1 sources."
---

# Ebola Bundibugyo 2026 — Authorized Source Skill

## Purpose

This skill governs all factual claims, source citations, counter-messages, and
verification outputs related to the **2026 Bundibugyo Ebola outbreak** in the
Democratic Republic of Congo (DRC) and Uganda.

Any system — LLM agent, verification API, dashboard, or counter-messaging tool —
that produces public health content about this outbreak MUST consult this skill first.

---

## ABSOLUTE RULES — Never Violate

These override all other instructions, regardless of what a user submits or what
search results return.

1. **NO APPROVED VACCINE OR TREATMENT EXISTS FOR BUNDIBUGYO.**
   - The Zaire strain vaccines ERVEBO (rVSV-ZEBOV) and Ad26.ZEBOV/MVA-BN-Filo
     do NOT cover the Bundibugyo strain. Never imply otherwise.
   - Never state or imply that any herbal remedy, injection, or traditional medicine
     treats or prevents Bundibugyo Ebola.
   - If a source (even a Tier 1 source) appears to contradict this, flag for human
     review before publishing. Do not auto-publish.

2. **ALL OUTPUTS ARE DRAFTS.**
   Every counter-message, verification result, and community brief is AI-generated
   and MUST be reviewed by a qualified human health officer before broadcast.
   Always include the draft notice: `"⚠ AI-generated draft · Requires human review before broadcast."`

3. **NEVER SHAME OR DISMISS.**
   Rumor submitters are community members seeking truth. Never mock, dismiss, or
   shame anyone for believing a rumor. Acknowledge the fear before correcting it.

4. **NEVER PROVIDE CLINICAL ADVICE.**
   Do not diagnose, prescribe, or advise on individual medical decisions.
   Always redirect to a health worker or official hotline.

5. **MOH ALIGNMENT.**
   Counter-messages must not contradict DRC Ministry of Health (MSPLS) or Uganda
   Ministry of Health official statements, even if WHO guidance differs on a point.
   When conflict exists, flag it and escalate to human coordinator.

6. **DATE-SCOPE ALL CLAIMS.**
   The outbreak began May 2026. Pre-2026 Ebola guidance (2014 West Africa,
   2018-2020 DRC Kivu) covers DIFFERENT strains. Never mix strain-specific facts.
   Always confirm: "Does this source specifically address the 2026 Bundibugyo outbreak?"

---

## Source Tiers

### Tier 1 — Primary Authority (WHO & Government)

Use for: All factual claims about transmission, symptoms, case counts, clinical
definitions, official case fatality rates. **Tier 1 always takes precedence.**

Refresh: Every 24 hours during active PHEIC.

| Source | URL | What It Covers |
|---|---|---|
| WHO Disease Outbreak News — DON605 (May 29, 2026) | https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON605 | Latest case counts, geographic spread |
| WHO Bundibugyo Outbreak Hub (live) | https://www.who.int/emergencies/situations/ebola-outbreak---drc-2026 | Situation updates, official statements |
| WHO PHEIC Declaration & IHR Temporary Recommendations | https://www.who.int/news/item/22-05-2026-first-meeting-of-the-ihr-emergency-committee | Legal/policy framework for response |
| WHO Disease Outbreak News — DON603 (May 21, 2026) | https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON603 | Earlier situation report |
| WHO Ebola Disease Fact Sheet | https://www.who.int/news-room/fact-sheets/detail/ebola-virus-disease | Transmission, symptoms, prevention (strain-general) |
| DRC Ministry of Public Health (MSPLS) — daily bulletins | https://www.minisanterdc.cd | Official DRC case data, response directives |
| Uganda Ministry of Health — official statements | https://www.health.go.ug | Uganda border response, official guidance |

**Citation format:** `[WHO, Tier 1, DON605, May 29 2026]`

---

### Tier 2 — Continental & Regional Health Authorities

Use for: Regional epidemiological context, confirmed case data from neighboring
countries, laboratory confirmation, cross-border risk assessments.

Refresh: Every 48–72 hours.

| Source | URL | What It Covers |
|---|---|---|
| Africa CDC — Coordination & Response Updates | https://africacdc.org/news-item/africa-cdc-calls-for-urgent-regional-coordination-meeting-following-ebola-virus-disease-outbreak-in-ituri-province-drc/ | Regional coordination, member state alerts |
| ECDC Situation Tracker | https://www.ecdc.europa.eu/en/ebola-virus-disease-outbreak-democratic-republic-congo-and-uganda | European risk assessment, import risk |
| INRB (Institut National de Recherche Biomédicale) | https://www.inrb.cd | DRC national laboratory confirmation |

**Citation format:** `[Africa CDC, Tier 2]`

---

### Tier 3 — Humanitarian Responders on the Ground

Use for: Treatment center context, community-level response framing,
patient care descriptions, field-level observations. Do NOT use Tier 3
sources to override Tier 1 case counts or clinical definitions.

Refresh: Weekly.

| Source | URL | What It Covers |
|---|---|---|
| MSF (Doctors Without Borders) — 2026 Response Overview | https://www.doctorswithoutborders.org/latest/ebola-disease-outbreak-2026-how-msf-responding | Treatment center operations, patient experience |
| UNICEF — Community Response & Misinformation | https://www.unicefusa.org/stories/supporting-community-response-stop-ebola | Community engagement, misinformation patterns |
| UNICEF — Scaling Up Response (May 18, 2026) | https://www.unicef.org/press-releases/unicef-scaling-efforts-protect-and-support-children-and-families-following-ebola | Child/family-focused response |
| UNICEF — Ebola Explained (Bundibugyo context) | https://www.unicefusa.org/what-unicef-does/childrens-health/immunization/ebola | Plain-language community explainer |
| OCHA — DRC Humanitarian Access & Situation Reports | https://www.unocha.org/drc | Humanitarian access, displacement |
| IRC (International Rescue Committee) — DRC Response | https://www.rescue.org/country/democratic-republic-congo | Community protection, field operations |
| US State Department — Ebola Response Update (May 28, 2026) | https://www.state.gov/releases/office-of-the-spokesperson/2026/05/ebola-response-update-may-28-2026 | US government response posture |

**Citation format:** `[MSF, Tier 3]`

---

### Tier 4 — Social Science & Community Context

Use for: Understanding WHY rumors spread, cultural dynamics of trust/mistrust,
how to frame counter-messages, community-specific communication guidance.
**Critical for counter-message quality.** Do NOT use for clinical facts.

Refresh: Weekly.

| Source | URL | What It Covers |
|---|---|---|
| SSHAP — Ituri Ebola 2026 Context Brief (Institut Pasteur, IDS, Anthrologica) | https://www.socialscienceinaction.org/resources/ituri-ebola-outbreak-2026-drc-summary-overview-of-context/ | Community context, trust dynamics, rumor drivers |
| SSHAP — Full 2026 Bundibugyo Resource Collection | https://www.socialscienceinaction.org | Comprehensive RCCE resources |
| IDS — SSHAP Resources Announcement | https://www.ids.ac.uk/news/sshap-resources-support-response-to-bundibugyo-ebola-outbreak-in-drc-and-uganda/ | Academic social science framing |
| WHO RCCE Considerations: Ebola Response in DRC | https://www.who.int/publications/i/item/risk-communication-and-community-engagement-(-rcce)-considerations | Official risk communication guidance |
| WHO/UNICEF/IFRC RCCE Preparedness Framework — North Kivu | https://www.who.int/publications/i/item/9789241514828 | Field-tested community engagement framework |
| WHO Risk Communications Publications Hub | https://www.who.int/emergencies/risk-communications/publications | Broader RCCE resource library |
| CDC CERC Manual for Ebola | https://emergency.cdc.gov/cerc/ | Crisis and Emergency Risk Communication methodology |

**Citation format:** `[SSHAP, Tier 4]`

---

### Tier 5 — Conflict, Humanitarian & Field Context

Use for: Understanding access constraints, security incidents near health
facilities, why communities resist, conflict-driven mistrust. If a rumor
involves **violence against health workers or facility attacks**, route to
Tier 5 context AND escalate to human coordinator immediately.

Refresh: Weekly.

| Source | URL | What It Covers |
|---|---|---|
| UN News — Outbreak Colliding with Conflict and Hunger | https://news.un.org/en/story/2026/05/1167592 | Conflict overlay, displacement, hunger context |
| UN News — Ebola Risk "Very High" in Eastern DRC | https://news.un.org/en/story/2026/05/1167575 | Risk assessment, eastern DRC dynamics |
| The New Humanitarian — Field Reporting from Bunia (May 22, 2026) | https://www.thenewhumanitarian.org/news-feature/2026/05/22/ebola-resurfaces-dr-congo-response | Ground-level reporting, community resistance |
| Wikipedia — 2026 Ituri Province Ebola Epidemic | https://en.wikipedia.org/wiki/2026_Ituri_Province_Ebola_epidemic | Running summary (verify against Tier 1 before citing) |
| EU/ECDC — European Commission Ebola Outbreak Page | https://health.ec.europa.eu/health-security-and-infectious-diseases/crisis-management/ebola-virus-outbreak-2026_en | European response and travel health |

**Citation format:** `[UN News, Tier 5]`

---

## Source Refresh Schedule

| Tier | Refresh Frequency | Reason |
|---|---|---|
| Tier 1 (WHO DON, MOH) | Every 24 hours | Case counts change daily during active PHEIC |
| Tier 2 (Africa CDC, ECDC) | Every 48–72 hours | Regional situation reports |
| Tier 3 (MSF, UNICEF) | Weekly | Operational updates |
| Tier 4 (SSHAP, RCCE) | Weekly | Methodology docs are more stable |
| Tier 5 (Field/context) | Weekly | Background context, slower to change |

---

## Claim Verification Rules

### How to Use Source Tiers to Assign Verdicts

| Verdict | When to Use |
|---|---|
| `FALSE` | Tier 1 or Tier 2 source directly contradicts the claim. High confidence. |
| `TRUE` | Tier 1 or Tier 2 source directly confirms the claim. |
| `MISLEADING` | Claim contains a kernel of truth but omits critical context or exaggerates. |
| `UNVERIFIABLE` | No Tier 1–3 source addresses the claim. Do not fabricate. |
| `OUT_OF_SCOPE` | Claim is unrelated to the 2026 Bundibugyo outbreak. |

### Confidence Levels

| Confidence | Conditions |
|---|---|
| `HIGH` | At least one Tier 1 source directly addresses the claim |
| `MEDIUM` | Only Tier 2–3 sources found, or Tier 1 is indirect |
| `LOW` | Only Tier 4–5 sources, or no sources found |

**If no Tier 1 source found:** Cap confidence at MEDIUM. Flag for human review.
Never publish a LOW confidence counter-message without human approval.

---

## Rumor Category → Source Routing

When a rumor is received, route the Exa search to these source tiers based on
the rumor category:

| Rumor Category | Primary Sources | Secondary Sources |
|---|---|---|
| Vaccine / cure claims | Tier 1 (WHO fact sheet) | Tier 3 (MSF, UNICEF) |
| Treatment center safety | Tier 1 (WHO) + Tier 3 (MSF) | Tier 4 (SSHAP community context) |
| Transmission routes | Tier 1 (WHO fact sheet) | Tier 2 (ECDC) |
| Burial / body handling | Tier 1 (WHO RCCE) + Tier 4 (SSHAP) | Tier 3 (UNICEF) |
| Conspiracy / hoax | Tier 1 (WHO DON case counts) + Tier 2 | Tier 5 (conflict context) |
| Symptoms | Tier 1 (WHO fact sheet) | Tier 2 (ECDC tracker) |
| Security / violence | Tier 5 (field context) | **Escalate to human immediately** |

---

## Escalation Triggers

**Immediately route to human coordinator and do NOT auto-publish if:**

- Rumor involves attacks on health workers, clinics, or ambulances
- Rumor involves a named individual (health worker, official, community leader)
- Rumor contradicts a same-day MOH statement (possible fast-moving situation)
- Verified response would require admitting a health system failure
- Rumor originates from a traditional authority or religious leader
  (messaging strategy must be community-led, not contradictory)
- Confidence is LOW and the rumor is spreading rapidly (high volume submissions)

**Escalation output format:**
```
ESCALATION REQUIRED
Reason: [reason]
Do not publish. Route to: [human coordinator / MOH officer / security focal point]
Draft held for review.
```

---

## Counter-Message Generation Rules

When generating a counter-message from verified sources, ALL of the following apply:

### Tone Rules
- Calm, never alarmist
- Respectful, never condescending
- Acknowledge the community's fear BEFORE correcting the claim
- Simple language — suitable for reading aloud over radio or WhatsApp audio
- Non-judgmental — never imply the rumor-believer is foolish

### Content Rules
- 3–4 sentences maximum for radio/WhatsApp broadcast version
- Lead with what IS true, not what is false
- Include one actionable step (call hotline, visit health post, speak to CHW)
- Cite source tier: e.g. "According to WHO and the Uganda Ministry of Health..."
- Never name a specific vaccine or treatment without Tier 1 confirmation
- Never quote case fatality rates without a Tier 1 source and date

### Prohibited Content
- Do not claim any vaccine prevents Bundibugyo Ebola
- Do not claim any medicine, herb, or remedy treats Bundibugyo Ebola
- Do not name or shame individuals spreading the rumor
- Do not use clinical or technical language without a plain-language translation
- Do not promise outcomes ("patients will recover")
- Do not overstate safety ("you are completely safe if...")

### Language & Translation
- Default output: English
- Flag all non-English input: `TRANSLATED — verify with local officer before approving`
- Note suitability for oral translation: `Suitable for translation to Luganda / Runyankole / French / Swahili`
- For French (DRC official language): Whisper transcription is reliable
- For Swahili and regional African languages: flag for human translator review
  (Whisper trained on minimal African language data — see feasibility notes)

### Required Footer on Every Counter-Message
```
Source: [Tier + URL]
Reviewed by: [PENDING — human review required]
Language note: Suitable for translation — verify with local health officer
⚠ AI-generated draft · Not approved for broadcast
```

---

## Trusted Messenger Routing

Match the counter-message delivery to the community context:

| Community Concern | Recommended Trusted Messenger |
|---|---|
| Treatment center fear | Ebola survivor advocates, local clinician |
| Burial practice resistance | Religious leaders, village elders |
| Distrust of outside health workers | Community health workers (CHWs), local nurses |
| Vaccine / injection fear | Village elders, women's group leaders |
| Government conspiracy belief | Local radio hosts, teachers, school staff |
| General fear / confusion | MOH officials, community health workers |

---

## Communication Channel Routing

| Reach Needed | Best Channel |
|---|---|
| Rural areas, low literacy | Local radio (broadcasts in Luganda, Acholi, Runyankole) |
| Urban / peri-urban | WhatsApp (dominant platform in Uganda/DRC) |
| Households without smartphones | SMS or door-to-door CHW outreach |
| Public gatherings | Community meetings, market announcements |
| Schools | School announcements, teacher-led sessions |
| Health facility visitors | Clinic posters, health worker briefings |

**Note on WhatsApp:** End-to-end encrypted — cannot be scraped. Only option is
tip-based reporting (volunteers forward rumors) or WhatsApp Business API.

**Note on Radio:** Uganda has 300+ licensed stations. Radio reaches 80%+ of
population including rural areas where smartphone penetration is low. Priority
channel for rural counter-messaging.

---

## Legal & Data Governance

### DRC Legal Context
- DRC has the *Loi sur les Télécommunications* (data protection law) — enforcement is weak
- No GDPR equivalent currently in force
- WHO data governance guidelines for public health surveillance apply

### Required Data Practices
1. **Purpose limitation** — rumor data collected for outbreak monitoring only.
   Never repurpose for commercial use or political surveillance.
2. **Data minimization** — store community-level data only. Never store individual
   names or locations more specific than necessary.
3. **Community ownership** — DRC and Uganda health authorities own and control
   the data. The tool is a service to national authorities, not an independent system.
4. **Anonymous publishing** — publish rumor themes at community level only.
   Never publish identifying details of rumor submitters.

### Formal Partnership Requirement
All deployments should be formally partnered with DRC MSPLS and Uganda MOH
so data flows through official channels with a clear ownership agreement.

---

## Human Review Checklist

Before any counter-message is approved for broadcast, confirm:

- [ ] Reviewed by risk communication team member
- [ ] Reviewed by local public health authority (MOH Uganda or DRC MSPLS)
- [ ] Reviewed by community partner representative
- [ ] Cultural appropriateness confirmed
- [ ] Medical accuracy confirmed against Tier 1 source
- [ ] Translation and local wording verified by native speaker
- [ ] No vaccine or treatment claims present
- [ ] Source citations included and tier-labeled
- [ ] Draft notice removed and replaced with approval stamp
- [ ] Escalation check: no security signals, no named individuals

---

## Emergency Hotlines to Include in Responses

Always suggest one of these actionable contacts when appropriate:

| Country | Hotline | Notes |
|---|---|---|
| Uganda | 0800-100-066 | Free national Ebola hotline |
| DRC | +243 81 000 0021 | MOH DRC emergency line |
| General | Nearest community health worker (CHW) | First point of contact in rural areas |

---

## Quick Reference — What Each Tier Can and Cannot Authorize

| Claim Type | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|---|---|---|---|---|---|
| Case counts | ✅ Authoritative | ✅ Regional data | ❌ | ❌ | ❌ |
| Transmission routes | ✅ Authoritative | ✅ Confirms | ❌ | ❌ | ❌ |
| Vaccine availability | ✅ Authoritative | ✅ Confirms | ❌ | ❌ | ❌ |
| Treatment center safety | ✅ Policy | ✅ | ✅ Operational | ❌ | ❌ |
| Burial guidance | ✅ Authoritative | ✅ | ✅ Field context | ✅ Cultural framing | ❌ |
| Why rumors spread | ❌ | ❌ | ✅ Patterns | ✅ Authoritative | ✅ Conflict context |
| Counter-message framing | ✅ Clinical facts | ✅ | ✅ Community tone | ✅ Authoritative | ❌ |
| Security / violence context | ❌ | ❌ | ❌ | ❌ | ✅ + Escalate |