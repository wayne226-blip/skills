---
name: deal-finder-pipeline
description: "Find the best UK coupon deals and voucher codes across supermarkets, tech, fashion, restaurants, travel, and services. Orchestrates a 5-agent pipeline: dispatcher classifies the request, scouts search in parallel, verifier extracts structured deal data, ranker scores and deduplicates, formatter delivers output. Two modes: daily Telegram digest (scheduled) and on-demand query (interactive). Use when Wayne says 'find me deals', 'coupon codes for', 'any discounts on', 'deal digest', 'what offers are on', 'deals on X', 'voucher for', 'save me money on', 'best deals today', or 'uk deals'."
---

# UK Deal Finder Pipeline

Orchestrates 5 agents to find, verify, rank, and deliver the best UK coupon deals.

## Pipeline Architecture

```
deal-dispatcher → deal-scout (x3 parallel) → deal-verifier → deal-ranker → deal-formatter
```

## Step 1: Determine Mode

- If triggered by scheduled task → `mode = "digest"`, `query = ""`
- If triggered by user prompt → `mode = "query"`, extract the query text from the user's message
- Set `date` to today's date

## Step 2: Dispatch the Dispatcher

Launch the `deal-dispatcher` agent:

```
Agent(subagent_type="deal-dispatcher", prompt="""
You are the deal-dispatcher agent. Produce a dispatch plan for the deal-finder pipeline.

Mode: [digest|query]
Query: [user query text or "N/A"]
Date: [today's date]

Follow your instructions to produce a DISPATCH PLAN with category batches, search terms, and priority sources.
""")
```

Read the dispatch plan output. It will contain 1-3 batches of categories.

## Step 3: Fan Out Scouts in Parallel

For EACH batch in the dispatch plan, launch a `deal-scout` agent **in parallel** (use a single message with multiple Agent tool calls):

```
Agent(subagent_type="deal-scout", prompt="""
You are the deal-scout agent. Search for deals in the following categories.

[Paste the batch section from the dispatch plan — categories, search terms, priority sources]

Follow your instructions to produce SCOUT RESULTS for each category.
""")
```

Digest mode: 3 scouts in parallel (Batch A, B, C).
Query mode: 1-2 scouts depending on category count.

Collect all scout results.

## Step 4: Verify Deals

Aggregate all SCOUT RESULTS blocks and pass to the `deal-verifier` agent:

```
Agent(subagent_type="deal-verifier", prompt="""
You are the deal-verifier agent. Verify the following raw deals found by the scouts.

[Paste ALL aggregated SCOUT RESULTS blocks here]

Follow your instructions to produce VERIFIED DEALS.
""")
```

## Step 5: Rank Deals

Pass the verified deals to the `deal-ranker` agent:

```
Agent(subagent_type="deal-ranker", prompt="""
You are the deal-ranker agent. Score and rank these verified deals.

Mode: [digest|query]
Query: [user query or "N/A"]

[Paste the VERIFIED DEALS block here]

Follow your instructions to produce RANKED DEALS.
""")
```

## Step 6: Format and Deliver

Pass the ranked deals to the `deal-formatter` agent:

```
Agent(subagent_type="deal-formatter", prompt="""
You are the deal-formatter agent. Format these ranked deals for delivery.

Mode: [digest|query]
Date: [today's date]
Chat ID: 8470901209

[Paste the RANKED DEALS block here]

Follow your instructions.
- If mode is "digest": send the formatted message to Telegram using chat_id 8470901209
- If mode is "query": return the formatted text (do NOT send to Telegram)
""")
```

## Error Handling

Errors should degrade gracefully — partial results are better than no results.

| Failure | Recovery |
|---|---|
| deal-dispatcher fails | Abort pipeline. If digest mode, send Telegram: "Deal digest unavailable today — dispatcher error" |
| One deal-scout fails | Continue with remaining scouts. Note missing categories in output |
| All deal-scouts fail | Abort pipeline. If digest mode, send Telegram: "Deal digest unavailable — all searches failed" |
| deal-verifier fails | Pass raw scout results directly to ranker with all confidence = "low" |
| deal-ranker fails | Pass verified deals directly to formatter, unsorted |
| deal-formatter fails (digest) | Compose a basic Telegram message manually with top 3 deals from ranker output |

## On-Demand Usage Examples

- "find me deals on TVs" → mode=query, dispatches tech category, returns structured text
- "any Deliveroo voucher codes?" → mode=query, dispatches restaurants category with Deliveroo-specific terms
- "best deals today" → mode=digest, sweeps all categories, returns structured text (not Telegram)
- "deal digest" → mode=digest, sweeps all categories, sends to Telegram
