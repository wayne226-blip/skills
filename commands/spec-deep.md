---
name: spec-deep
description: Generate an in-depth spec for a new feature or project before coding. Covers user journey, data model, integrations, screens, risks, and open questions. Use when Wayne wants a thorough plan before touching any code.
argument-hint: "[project or feature name]"
allowed-tools: Read, Write
---

# Deep Spec Writer

Your job is to help Wayne write a thorough spec before he starts coding. Guide him through 13 short questions — one at a time — then produce a complete spec document.

## How to run this

Ask each question individually. Wait for the answer before asking the next one. Keep it conversational — this is voice-dictated most of the time so expect informal phrasing and typos. Fix them mentally and carry on.

Group the questions into 4 sections as you go — tell Wayne which section you're moving into before the first question of each section.

---

## Section 1: The Basics

Announce: "Let's start with the basics."

1. **What is it?**
   Ask: "In one sentence — what are you building?"

2. **Who uses it?**
   Ask: "Who is the user? (You, a customer, an agent, an API?)"

3. **What problem does it solve?**
   Ask: "What's currently broken or missing that this fixes?"

4. **Key features**
   Ask: "What are the 3–5 most important things it must do?"

5. **Out of scope**
   Ask: "Anything it explicitly should NOT do? (Or skip if none.)"

---

## Section 2: User Journey & UI

Announce: "Now let's map out how it actually works."

6. **User journey**
   Ask: "Walk me through the main user journey — what does the user actually do, step by step? Start from when they open it."

7. **Screens / views**
   Ask: "What are the main screens or views the user sees? Even rough names are fine — e.g. dashboard, settings, detail page."

---

## Section 3: Data & Integrations

Announce: "A few questions about the data and connections."

8. **Data model**
   Ask: "What data does it store or work with? What are the key things — users, records, files, etc.?"

9. **Integrations**
   Ask: "Does it connect to anything external — APIs, Zapier, databases, third-party services? If none, just say none."

10. **Auth / access**
    Ask: "Does it need login or user accounts? If so, how? (Google, email/password, magic link, none?)"

---

## Section 4: Risk, Decisions & Delivery

Announce: "Last section — risks and how you'll know it's done."

11. **Biggest risk**
    Ask: "What's the biggest thing that could go wrong, or the part you're least sure about?"

12. **Open questions**
    Ask: "Any decisions you haven't made yet — things you're still figuring out? (Or skip if none.)"

13. **Tech stack**
    Ask: "What tools, language, or platform will this run on?"

14. **Done looks like**
    Ask: "How will you know it's working? What's the success condition?"

---

## After collecting all answers

Produce a spec in this exact format:

```
# Deep Spec: [Project/Feature Name]
**Date:** [today's date]

---

## What Is It?
[one sentence from answer 1]

## Who Uses It?
[answer 2]

## Problem It Solves
[answer 3 — expand slightly if needed, max 3 sentences]

---

## Key Features
- [feature 1]
- [feature 2]
- [feature 3]
(add more if given)

## Out of Scope
- [answer 5, or "None specified" if skipped]

---

## User Journey
[answer 6 — write this as a numbered step-by-step flow, e.g.:
1. User opens the app
2. User does X
3. System does Y
Keep it concrete and sequential]

## Screens & UI
[answer 7 — bullet list of screen/view names with a one-line description of each]

---

## Data Model
[answer 8 — bullet list of key entities with a brief note on what each stores]

## Integrations
[answer 9, or "None" if skipped]

## Auth / Access
[answer 10]

---

## Risks
- [answer 11 — be specific, not vague]

## Open Questions
- [answer 12, or "None" if skipped]

---

## Tech Stack
[answer 13]

## Done Looks Like
[answer 14 — make this specific and testable if possible]
```

---

## After producing the spec

Ask: "Should I save this as `spec-deep.md` in the current directory?"

If yes — write it to `./spec-deep.md`.

Then ask: "Want me to generate a todo list from this spec now?"

If yes — read the spec and produce a phased todo list:

```
## Todo: [Project Name]

### Phase 1: Setup & Scaffold
- [ ] 1. [task]

### Phase 2: Core Features
- [ ] 3. [task]

### Phase 3: Data & Integrations
- [ ] 6. [task]

### Phase 4: UI & Polish
- [ ] 9. [task]

### Phase 5: Test & Ship
- [ ] 12. [task]
```

Save as `./todo.md` and tell Wayne which task to start with.
