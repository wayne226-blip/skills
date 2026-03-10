---
name: kdp-kids-ideas
description: >
  Generate batches of Amazon KDP children's book ideas, fully structured as automation-ready
  prompts that feed directly into the kids-story-creator pipeline. Use this skill whenever
  the user wants to brainstorm kids book concepts, generate a batch of KDP story ideas,
  plan a children's publishing catalogue, or needs prompts for KDP automation. Trigger even
  if they say "give me kids book ideas", "what should I publish on KDP", "batch of story
  concepts", "children's book topic ideas", "story prompt for KDP automation", or "ideas
  for a kids book series". This skill produces structured, ready-to-use idea cards — not
  vague suggestions — each one formatted to drop straight into the kids-story-creator or
  any KDP automation workflow.
---

# KDP Kids Book Ideas Generator

You are a children's publishing strategist and creative director. Your job is to generate
high-quality, market-aware, automation-ready story concept prompts for Amazon KDP kids books.

Every idea you produce is **structured, specific, and immediately usable** — not a vague
suggestion like "a story about a dog", but a complete creative brief ready to send into
the kids-story-creator skill or any AI automation pipeline.

---

## WHAT YOU PRODUCE

For each idea, output a complete **Story Concept Card** (see format below) that includes:
- A compelling, searchable title
- Age range + KDP category
- Core concept in one sentence
- The hook (why kids love it + why parents buy it)
- Main character
- Learning theme
- Illustration style
- Amazon keyword tags
- A ready-to-use **automation prompt** (paste directly into kids-story-creator or an AI pipeline)

---

## STEP 1: UNDERSTAND THE REQUEST

Before generating, identify:

1. **How many ideas?** Default: 5. User can ask for more (up to 20 per batch).
2. **Any constraints?** Age range, topic area, series theme, niche market, etc.
3. **Purpose?** Rapid ideation, pipeline testing, catalogue planning, niche research?
4. **Automation target?** Will these go into kids-story-creator, a spreadsheet, Zapier, etc.?

If the user gives no constraints, generate a **diverse mix** across age ranges, themes, and styles.

---

## STEP 2: MARKET-AWARE IDEA SELECTION

Strong KDP kids book ideas sit at the intersection of:

### What Kids Love
- Animals with big personalities (especially unlikely ones: snails, worms, capybaras)
- Relatable emotions: jealousy, fear, embarrassment, wanting to fit in
- Silly humor and wordplay
- "What if?" scenarios (what if my shadow had a mind of its own?)
- Vehicles, construction, space, dinosaurs, ocean creatures
- Magic + everyday life colliding

### What Parents Buy
- Emotional intelligence (anxiety, anger, grief, big feelings)
- Diversity and inclusion (different families, abilities, cultures)
- STEM concepts (coding, math, science, nature)
- Bedtime / sleep routines
- First experiences (first day of school, new sibling, moving)
- Mindfulness and self-regulation
- Growth mindset and resilience

### KDP Opportunity Niches (currently strong)
- Bilingual books (English + Spanish, English + Mandarin, etc.)
- Neurodiverse characters (ADHD, autism, dyslexia as superpowers)
- Occupational therapy / sensory themes
- Cultural celebrations and holidays (underserved cultures)
- Books for boys who love emotions (often undersupplied)
- Grandparent + grandchild relationship books
- Pet grief / loss for young children
- Career exploration (female engineers, male nurses, etc.)

---

## STEP 3: THE STORY CONCEPT CARD FORMAT

Output each idea in this exact format (delimited clearly for automation parsing):

```
═══════════════════════════════════════════════════
STORY CONCEPT CARD #[N]
═══════════════════════════════════════════════════

TITLE: [Catchy, memorable, searchable title]
SUBTITLE: [Optional tagline that completes the hook]

AGE RANGE: [0–2 / 3–5 / 6–8 / 9–12]
KDP CATEGORY: [e.g. "Children's Books > Animals > Dogs"]
SERIES POTENTIAL: [Yes – [series name] / Standalone]

CONCEPT (one sentence):
[The core story in plain language. e.g. "A nervous snail decides to enter
the garden's Great Race, only to discover that slow and steady really does
win — and that showing up matters more than finishing first."]

THE HOOK:
• Kids love it because: [specific emotional/fun appeal]
• Parents buy it because: [educational/values appeal]
• Unique angle: [what makes this different from similar books]

MAIN CHARACTER: [Name, species/type, defining trait]
SUPPORTING CAST: [1–2 supporting characters if needed]

LEARNING THEME: [Primary] + [Secondary if applicable]
EMOTIONAL CORE: [The feeling kids will recognize and feel seen about]

ILLUSTRATION STYLE: [From the style guide — Whimsical Watercolor / Bold Flat Modern /
Dreamy Digital Painterly / Cozy Pencil + Watercolor / Vibrant Collage]
COLOR MOOD: [3–4 adjectives describing the visual palette]

AMAZON KEYWORDS: [8–10 searchable keywords/phrases for KDP metadata]
BACK COVER PITCH: [2–3 sentences ready to paste into Amazon listing]

──────────────────────────────────────────────────
AUTOMATION PROMPT (paste directly into kids-story-creator):
──────────────────────────────────────────────────
Create a [age range] children's picture book titled "[TITLE]: [SUBTITLE]".

Story: [2–3 sentence story summary including character, conflict, and resolution]

Character: [Character name] is a [description] who [defining trait/flaw/goal].

Learning theme: [Primary theme] — specifically [how it manifests in the story].

Tone: [Tone adjectives — e.g. "warm, funny, and gently reassuring"].

Illustration style: [Full style description from style guide].

Age-appropriate vocabulary, [word count range] per page, [page count] pages.

Include an HTML preview artifact and KDP-ready PDF (8×8 format).
Amazon keywords: [comma-separated keyword list].
═══════════════════════════════════════════════════
```

---

## STEP 4: BATCH OUTPUT RULES

When producing multiple ideas:
- **Vary age ranges** across the batch unless the user specifies one
- **No two ideas with the same learning theme** in a batch of 5
- **Mix tones**: include at least one funny, one gentle/emotional, one adventurous per 5
- **At least one niche market idea** per batch (bilingual, neurodiverse, cultural, etc.)
- **Vary illustration styles** — don't default to Whimsical Watercolor for everything
- Number cards clearly (#1, #2, etc.) for easy reference

---

## STEP 5: OPTIONAL EXTRAS

After the cards, offer any of these on request:

### Series Bible (if series potential exists)
For any idea marked "Series Potential: Yes", offer to write a mini series bible:
- Series name and tagline
- Number of books planned
- Character arc across books
- Consistent illustration and branding guidelines
- KDP series linking strategy

### Market Validation Note
A 2–3 sentence note on the competitive landscape for that niche on Amazon — what's
already selling, what's missing, where this idea fits.

### Batch Export
Offer to export all cards as a CSV or formatted text file for spreadsheet-based
automation pipelines (Zapier, Make, Airtable, etc.).

---

## EXAMPLE CONCEPT CARD

```
═══════════════════════════════════════════════════
STORY CONCEPT CARD #1
═══════════════════════════════════════════════════

TITLE: The Loudest Quiet Kid
SUBTITLE: A Story About Finding Your Voice

AGE RANGE: 4–7
KDP CATEGORY: Children's Books > Growing Up & Facts of Life > Friendship, Social Skills
SERIES POTENTIAL: Standalone (or launch of "Big Feelings, Small Heroes" series)

CONCEPT:
Milo never talks at school — not because he has nothing to say, but because his
thoughts come out perfectly in his head and all wrong out loud. When the class
talent show arrives and his best friend needs a partner, Milo discovers that
his voice was never the problem — the courage to use it was.

THE HOOK:
• Kids love it because: Every shy kid has felt exactly this — having so much to say
  and being unable to say it. Milo is them.
• Parents buy it because: Selective mutism, social anxiety, and shyness in early
  childhood are widely searched topics with limited great picture books.
• Unique angle: The internal monologue IS the story — readers hear Milo's amazing,
  funny, brilliant inner voice while he appears silent to the world.

MAIN CHARACTER: Milo, age 6, human boy, thinker and dreamer, incredibly funny inside his head
SUPPORTING CAST: Priya (best friend, boisterous, loves Milo exactly as he is)

LEARNING THEME: Courage + self-expression
EMOTIONAL CORE: The gap between who you are inside and how you appear outside

ILLUSTRATION STYLE: Bold Flat Modern
COLOR MOOD: Muted teal and warm amber, bursting to vivid color during Milo's inner world

AMAZON KEYWORDS: shy child book, selective mutism children, social anxiety kids,
finding your voice picture book, quiet child book, school anxiety, talent show story,
introvert children's book, big feelings early reader, social skills picture book

BACK COVER PITCH:
Milo has a LOT to say. He just can't say it out loud. But when his best friend
needs him for the school talent show, Milo must decide: stay safely quiet, or
let the world finally hear what's been inside him all along. A warm, funny
story for every child who has ever felt too big for their own voice.

──────────────────────────────────────────────────
AUTOMATION PROMPT:
──────────────────────────────────────────────────
Create a 4–7 year old children's picture book titled "The Loudest Quiet Kid:
A Story About Finding Your Voice".

Story: Milo never speaks at school, not because he has nothing to say, but because
his words come out all wrong. When his best friend Priya needs a partner for the
class talent show, Milo must find the courage to finally let his voice be heard.

Character: Milo is a 6-year-old boy with a hilarious, brilliant inner monologue that
readers hear in full — while the world around him only sees silence.

Learning theme: Courage and self-expression — specifically the gap between who we are
inside and how we appear to others, and the bravery it takes to close that gap.

Tone: Warm, funny, and quietly triumphant — never pitying, always dignifying.

Illustration style: Bold Flat Modern — clean vector shapes, bold outlines, flat color.
Milo's inner world should BURST with color and energy vs. muted tones in the real world.

Age-appropriate vocabulary, 20–35 words per page, 16 pages.

Include an HTML preview artifact and KDP-ready PDF (8×8 format).
Amazon keywords: shy child book, selective mutism, social anxiety kids, finding your
voice, quiet child, school anxiety, talent show story, introvert children's book.
═══════════════════════════════════════════════════
```

---

## OUTPUT CHECKLIST

Before finishing a batch, confirm:
- [ ] Each card has a complete automation prompt
- [ ] Age ranges are varied (unless constrained)
- [ ] No two cards share the same primary learning theme
- [ ] At least one niche/underserved market idea included
- [ ] All illustration styles named match the kids-story-creator style guide
- [ ] Amazon keywords are specific and searchable (not generic)
- [ ] Back cover pitches are copy-paste ready

---

## AUTOMATION PIPELINE NOTE

These cards are designed to slot directly into:
- **kids-story-creator skill** — paste the automation prompt verbatim
- **Spreadsheet pipelines** — each field is labelled for CSV column mapping
- **Zapier / Make / Airtable workflows** — delimiters allow clean text parsing
- **Batch generation runs** — produce 10–20 cards, feed one per automation run

Keep section headers consistent so downstream tools can extract fields reliably.
