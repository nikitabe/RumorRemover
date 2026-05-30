# Ebola Bundibugyo 2026 — Rumor Verification Context

> This file is the **ground-truth reference** the assistant must use when assessing a rumor.
> It is compiled from official public-health reporting (WHO, CDC), national situation reports
> (INSP/COUSP-RDC), and humanitarian updates (IOM, IFRC, ACAPS) as of **27–29 May 2026**.
> Figures change as the outbreak evolves — treat counts as point-in-time, not permanent truth.

---

## 1. Outbreak basics

- The outbreak is caused by **Bundibugyo virus disease (BVD)**, a species of Ebola virus. It is a **severe** form of Ebola disease.
- It is affecting the **Democratic Republic of the Congo (DRC)** and **Uganda**.
- On **17 May 2026**, the **WHO declared the outbreak a Public Health Emergency of International Concern (PHEIC)**.
- The DRC officially declared its **17th Ebola outbreak** on **15 May 2026** after sequencing identified the Bundibugyo strain.
- Confirmed DRC cases are in **Ituri, Nord-Kivu, and Sud-Kivu** provinces. Uganda's cases are linked to the DRC outbreak.

## 2. Case and death counts (point-in-time)

- **As of 27 May 2026 (CDC):** DRC and Uganda ministries reported **1,077 suspected cases, 121 confirmed cases, 246 suspected deaths, and 17 confirmed deaths in DRC**; and **7 confirmed cases and 1 confirmed death in Uganda**.
- **By 29 May 2026:** **134 confirmed cases** (including nine in Uganda) and **18 confirmed deaths** had been reported across both countries.
- **No outbreak-associated Ebola cases have been confirmed in the United States.** Risk to the U.S. public and to travelers remains **low**.

## 3. Transmission and clinical facts

- Transmission occurs through **direct contact with blood, secretions, organs, or other bodily fluids** of infected or deceased people, or via **contaminated surfaces and materials**.
- Transmission is amplified by **inadequate infection prevention and control (IPC)** in healthcare settings and by **unsafe burial practices**.
- The **incubation period is 2 to 21 days**. People are **usually not infectious until symptoms appear**.
- Reported symptoms in this outbreak: **fever, headache, vomiting, severe weakness, abdominal pain, nosebleeds, and vomiting blood.**
- Most DRC cases reported so far are among people aged **20–39 years**, and roughly **two-thirds are female**.

## 4. Vaccines and treatment — IMPORTANT

- There is currently **NO licensed or approved vaccine** for Bundibugyo virus disease.
- There is currently **NO FDA-approved or authorized treatment specifically for BVD**.
- The licensed Ebola vaccine **ERVEBO targets *Zaire* ebolavirus and is NOT expected to protect against Bundibugyo virus.**
- A **candidate vaccine, ChAdOx1 BDBV** (ChAdOx-based, monovalent), is being developed by the **University of Oxford** with the Serum Institute of India. It is **investigational / not yet licensed**.
- The mainstay of care is **early, high-quality supportive care**: oral and IV rehydration, electrolyte management, fever and pain control, treating complications, nutritional support, and clinical monitoring.
- Core control measures: **early detection, isolation, IPC, contact tracing, safe and dignified burial, and community engagement.**

## 5. Context — geography, mobility, conflict

- Centered in **eastern DRC, especially Ituri Province** (~5.9–7 million people, nearly 1 million internally displaced).
- Major mining areas such as **Mongbwalu** drive population movement; urban centers include **Bunia**.
- Linguistically diverse: **French, Swahili, Lingala**, plus local languages such as **Lendu and Nyali**. Major groups include Hema, Lendu, Alur, Lugbara, and Nande.
- The region has **persistent insecurity** (armed groups, roadblocks, attacks on health infrastructure) that constrains surveillance and response.
- **Cross-border mobility** to Uganda, Rwanda, and South Sudan increases risk of undetected transmission.
- **Funeral and burial practices** (body washing, touching, mourning gatherings) are a major transmission and trust issue. Messaging should **adapt rituals safely, not simply prohibit them.**

## 6. Travel and border measures

- Uganda began restricting movement at the **Ishasha-Kyeshero** crossing; South Sudan issued an alert and began monitoring its DRC border.
- **IOM** supports points-of-entry/control operations in Bunia, Beni, Goma, and N'djili International Airport, and flow monitoring across 12 points of entry in Uganda.
- **WHO Priority 1 countries:** DRC, Uganda, South Sudan, Burundi, Rwanda. **Priority 2:** Angola, CAR, Ethiopia, Kenya, Republic of Congo, Tanzania, Zambia.
- **United States (announced 18 May 2026):** Enhanced screening for travelers who were in DRC, Uganda, or South Sudan in the prior 21 days. Certain non-U.S. citizens recently in those countries are temporarily restricted from entry. U.S. citizens/nationals may enter but undergo enhanced screening and should monitor for symptoms for 21 days. Affected travelers may be routed to Washington-Dulles, Atlanta (Hartsfield-Jackson), or Houston (George Bush Intercontinental).

## 7. Common rumors and the verified reality

- **"There is a cure / a proven medicine for this Ebola strain."** → FALSE. No approved specific treatment exists; only supportive care. An investigational Oxford vaccine candidate exists but is not licensed.
- **"The ERVEBO Ebola vaccine protects against this outbreak."** → FALSE/MISLEADING. ERVEBO targets Zaire ebolavirus, not Bundibugyo.
- **"Treatment centers are where people go to be poisoned / killed."** → FALSE. Treatment centers provide isolation and supportive care; this is a known harmful rumor that delays care-seeking.
- **"Ebola is spreading widely in the United States."** → FALSE. No outbreak-associated cases confirmed in the U.S.; risk remains low.
- **"You can catch Ebola from someone who has no symptoms."** → MOSTLY FALSE. People are usually not infectious until symptoms appear.
- **"Safe burial means families cannot mourn or be involved at all."** → FALSE/MISLEADING. Safe and dignified burial adapts rituals (family consultation, prayers, escort, safe substitutes) rather than banning them.

---

## Assessment guidance for the assistant

When given a rumor:
1. Decide a **verdict**: `TRUE`, `FALSE`, `MISLEADING`, or `UNVERIFIABLE` (use UNVERIFIABLE if this context does not cover the claim — do not invent facts).
2. Give a short, plain-language **explanation** grounded only in the context above. If the context lacks the relevant fact, say so explicitly.
3. Provide a **suggested counter-message**: a short, calm, culturally sensitive statement field teams could broadcast, aligned with official guidance.
4. Note any **caveats** (e.g., figures are point-in-time, or the claim is partly true).
5. Never fabricate statistics, studies, vaccines, or treatments not present in this context.
