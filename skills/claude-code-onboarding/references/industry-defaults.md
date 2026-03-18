# Industry Defaults — Claude Code/Cowork Onboarding

Use these defaults to pre-fill brain files when client-specific data is incomplete. Client data always overrides these defaults.

---

### Estate Agents / Letting Agencies

**Terminology:**
vendor (not seller), instruct (not hire), applicant (not buyer in some contexts), property particulars, EPC, floorplan, chain-free, sole agency, under offer, SSTC, exchange, completion

**Compliance:**
Consumer Protection Regulations, Material Information requirements, Property Ombudsman, EPC disclosure, Money Laundering Regulations (ID checks)

**Default tone:**
Professional but warm, approachable. Confident without being pushy.

**Typical skills:**
- Property description writer
- Viewing follow-up emails
- Vendor update emails
- Social media posts (new listings, sold/let, market updates)
- Applicant matching emails
- Online enquiry responder

**Typical agents:**
- Vendor Communications Agent — handles all vendor-facing emails and updates
- Marketing Agent — property descriptions, social posts, listing copy

**Typical commands:**
- `/property-description` — generate property listing from bullet points
- `/vendor-update` — draft vendor update email with market feedback
- `/viewing-followup` — post-viewing follow-up email

**Banned phrases:**
"Don't miss out" (pressure selling), "investment opportunity" (unless regulated), "must see" (overused), "unique" (unless genuinely so)

**Key features:**
Two audiences — vendors (selling/letting) and applicants (buying/renting). Tone shifts slightly: more authoritative with vendors, more helpful/enthusiastic with applicants. Property descriptions need to be factual and comply with Material Information rules.

---

### Accountants / Financial Services

**Terminology:**
Tax year, HMRC, self-assessment, corporation tax, VAT return, annual accounts, engagement letter, bookkeeping, payroll, dividend, director's loan, capital gains, allowable expenses, filing deadline, MTD (Making Tax Digital)

**Compliance:**
FCA if regulated, professional indemnity references, never guarantee financial outcomes, disclaimers on advice, anti-money laundering obligations, ICAEW/ACCA standards

**Default tone:**
Authoritative, precise, trustworthy. Clear without being condescending. Avoids jargon with clients unless they're financially literate.

**Typical skills:**
- Client update email writer
- Tax deadline reminder writer
- Engagement letter writer
- Newsletter content writer
- Report/management accounts commentary writer

**Typical agents:**
- Client Communications Agent — all client-facing emails and updates
- Compliance Agent — engagement letters, disclaimers, regulatory language

**Typical commands:**
- `/client-update` — draft client update email
- `/tax-reminder` — seasonal tax deadline reminder
- `/engagement-letter` — new client engagement letter

**Banned phrases:**
"Guarantee" (re: financial outcomes), "promise" (re: savings/returns), "tax dodge" or "loophole" (use "tax-efficient" or "allowance")

**Key features:**
Seasonal awareness is critical — January (self-assessment deadline), April (new tax year), July (payments on account), September (MTD quarterly). Clients range from sole traders to SME directors, so tone needs to flex.

---

### Recruitment Agencies

**Terminology:**
Candidate, client, placement, perm, contract, day rate, notice period, CV, spec, briefing, shortlist, counteroffer, offer management, onboarding, temp, AWR, IR35

**Compliance:**
GDPR for candidate data, AWR for temps, IR35 awareness for contractors, REC Code of Practice

**Default tone:**
Energetic and consultative with clients (employers). Supportive and encouraging with candidates. Two distinct tones that switch depending on audience.

**Typical skills:**
- Job advert writer
- Candidate outreach message writer
- Client follow-up sequence writer
- LinkedIn post writer
- Interview confirmation email writer

**Typical agents:**
- Candidate Agent — all candidate-facing comms (supportive tone)
- Client Agent — all client-facing comms (consultative tone)
- Content Agent — LinkedIn posts, market insights, thought leadership

**Typical commands:**
- `/job-ad` — write a job advert from spec
- `/candidate-outreach` — draft outreach to passive candidate
- `/client-followup` — chase hiring manager for feedback

**Banned phrases:**
"Perfect candidate" (sets unrealistic expectations), age/gender/ethnicity references in job ads (discrimination), "young and dynamic team" (age discrimination)

**Key features:**
Dual tone is the most important feature — must know whether writing to a client or candidate and adjust. Job adverts must be inclusive and compliant. Speed matters in recruitment.

---

### Solicitors / Legal Practices

**Terminology:**
Matter, instruction, client care letter, completion, exchange, disbursements, conveyancing, litigation, tribunal, brief, counsel, disclosure, witness statement, consent order, decree

**Compliance:**
SRA Standards and Regulations, client money rules, complaints procedure (must reference in client care letters), conflict of interest checks, data protection, professional undertakings

**Default tone:**
Formal, measured, precise. Never vague. Empathetic where appropriate (family law, personal injury) but always professional. Legal precision is non-negotiable.

**Typical skills:**
- Client care letter writer
- Matter update email writer
- Internal file note writer
- New enquiry responder
- Complaint handling letter writer

**Typical agents:**
- Client Care Agent — all client-facing correspondence (formal, precise)
- File Management Agent — internal notes, case summaries, preparation docs

**Typical commands:**
- `/client-care-letter` — new matter client care letter
- `/matter-update` — progress update email to client
- `/file-note` — internal file note from call/meeting notes

**Banned phrases:**
"We guarantee" (re: case outcome), "you will win", "easy case", "no-brainer" — any language implying certainty of outcome

**Key features:**
Legal precision is the defining requirement. Never use vague language. Different practice areas have different terminology. Client care letters must include required SRA information.

---

### Retailers (Online / High Street)

**Terminology:**
SKU, product line, collection, seasonal, markdown, footfall (physical), conversion (online), basket value, upsell, cross-sell, drop, restock, launch, limited edition

**Compliance:**
Consumer Rights Act, distance selling regulations (online), returns policy references, advertising standards (ASA), pricing accuracy

**Default tone:**
Friendly, approachable, enthusiastic about products. Conversational but not sloppy. Matches the energy of the brand.

**Typical skills:**
- Product description writer
- Customer reply handler (queries, complaints, reviews)
- Social media post writer (Instagram/Facebook heavy)
- Newsletter/email campaign writer
- Review response handler

**Typical agents:**
- Customer Service Agent — handles all customer queries, complaints, review responses
- Marketing Agent — product descriptions, social posts, campaigns, newsletters

**Typical commands:**
- `/product-description` — write product listing from specs/photos
- `/review-reply` — respond to customer review
- `/campaign` — draft email campaign or social media series

**Banned phrases:**
"Cheap" (use "affordable" or "great value"), "buy now" in isolation (pushy), misleading discount claims

**Key features:**
Heavy visual/social focus — posts need to work alongside images. Seasonal cycles drive content. Online retailers need conversion-focused copy; high street needs footfall-driving copy.

---

### Tradespeople / Contractors

**Terminology:**
Quote, job, site, call-out, materials, labour, warranty, guarantee, first fix, second fix, snagging, sign-off, building regs, Part P, Gas Safe, NICEIC

**Compliance:**
Industry-specific certifications (Gas Safe, NICEIC, FGAS, etc.), building regulations, warranty terms, insurance references

**Default tone:**
Direct, no-nonsense, plain language. Friendly but professional. No waffle.

**Typical skills:**
- Quote follow-up email writer
- Job confirmation message writer
- Review response handler
- Social media post writer (before/after style)
- Invoice chaser email writer

**Typical agents:**
- Customer Agent — all customer comms (quotes, confirmations, chasers)
- Social Agent — before/after posts, completed job showcases

**Typical commands:**
- `/quote-followup` — chase a sent quote
- `/job-confirm` — confirm job booking with customer
- `/invoice-chase` — polite payment reminder

**Banned phrases:**
"Honestly" (implies sometimes dishonest), overpromising on timelines, technical jargon to customers

**Key features:**
Short, punchy communications. Before/after content works well on social media. Many are sole traders — personal and business brand overlap.

---

### Coaches / Consultants / Freelancers

**Terminology:**
Discovery call, programme, package, transformation, results, case study, testimonial, retainer, session, framework, methodology, niche, ideal client, funnel

**Compliance:**
Varies — some regulated (financial coaches, therapists), most not. Testimonial/results claims should include "results may vary" where appropriate.

**Default tone:**
Confident, personal, thought-leader positioning. Warm but authoritative. The person IS the brand.

**Typical skills:**
- LinkedIn post writer
- Proposal/scope of work writer
- Follow-up sequence writer (post-discovery, post-event)
- Blog/long-form content writer
- Programme/package description writer

**Typical agents:**
- Content Agent — LinkedIn posts, blogs, thought leadership
- Sales Agent — proposals, follow-ups, discovery call summaries
- Brand Voice Agent — ensures all output matches personal brand

**Typical commands:**
- `/linkedin-post` — write LinkedIn post on topic
- `/proposal` — draft proposal/scope of work
- `/followup` — post-discovery call follow-up email

**Banned phrases:**
"Pick my brain" (devalues expertise), "guru" or "ninja" (overused), income claims without evidence, "guaranteed transformation"

**Key features:**
Personal brand IS the business brand — ME.md and BRAND.md overlap significantly. LinkedIn is typically the primary platform. Content needs to establish authority while remaining approachable.
