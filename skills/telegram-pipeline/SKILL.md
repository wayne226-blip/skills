---
name: telegram-pipeline
description: Multi-agent pipeline for handling Telegram messages. Orchestrates triage, research, and response agents to produce high-quality replies. Triggered automatically by the telegram-pipeline notification hook.
---

# Telegram Multi-Agent Pipeline

When a Telegram message arrives and the notification hook fires, follow this pipeline exactly.

## Step 0: Deduplication

Before doing anything, check if you have already processed this `message_id` in the current session. Telegram webhooks can fire duplicate notifications (retries, flaky network).

- If you recognise the `message_id` — skip the pipeline entirely, do not reply again
- If it is new — remember it and proceed to Step 1

Keep a mental list of the last ~20 handled `message_id` values per `chat_id`. This is session-scoped — no file storage needed.

## Pipeline Flow

### Step 1: Triage

Dispatch the **triage-agent** with the full message content and metadata.

```
Agent(subagent_type="triage-agent", prompt="Triage this Telegram message: [message content]. Sender: [user]. Chat ID: [chat_id].")
```

Read the triage result. If `Short-circuit: yes`, skip to Step 4 using the triage agent's suggested reply.

### Step 1.5: Acknowledge (if research needed)

If triage says `Research needed: yes`, immediately send a reaction so the sender knows the message was received:

```
react(chat_id="[chat_id]", message_id="[message_id]", emoji="👀")
```

This fires before research begins, so the sender sees feedback within seconds even if the full reply takes 30s+.

### Step 2: Research (conditional)

If triage says `Research needed: yes`, dispatch the **research-agent-telegram**.

```
Agent(subagent_type="research-agent-telegram", prompt="Research for Telegram reply. Original message: [message]. Triage says: [triage summary]. Research scope: [scope]. Look for: [what to research].")
```

If triage says `Research needed: no`, skip to Step 3 with empty research findings.

### Step 3: Draft Response

Dispatch the **response-agent-telegram** with all accumulated context.

```
Agent(subagent_type="response-agent-telegram", prompt="Draft a Telegram reply. Original message: [message]. Triage: [category, urgency]. Research findings: [findings or 'none']. Context: [any additional context].")
```

The response agent returns ONLY the reply text.

### Step 4: Send Reply

Use the Telegram `reply` tool to send the response:

```
reply(chat_id="[chat_id]", text="[response agent's output]")
```

If the original message had a `message_id` and this is a thread reply, include `reply_to`.

## When to Short-Circuit

Trust the triage agent's `Short-circuit: yes` flag. Common cases it should catch:
- Greetings ("hey", "morning", "hi", "yo")
- Simple acknowledgements ("thanks", "got it", "ok", "cheers", "ta")
- Emoji-only messages (thumbs up, laughing face, fire, etc.)
- Single-word reactions ("lol", "haha", "nice", "wow")
- Sticker or GIF messages with no text

For short-circuited messages, reply directly (or react with a matching emoji) without dispatching research or response agents.

## When to Use the Full Pipeline

Use all three agents for:
- Questions requiring information lookup
- Task requests needing context
- Status enquiries
- Anything the triage agent flags as needing research

## Media Handling

When the incoming `<channel>` tag includes an `image_path` attribute:

1. Use the Read tool to view the image at that path before dispatching triage
2. Include a brief description of the image content in the triage prompt (e.g., "Sender attached a photo showing a screenshot of an error message")
3. Pass the image description through to research and response agents as context

For documents, voice messages, or other media types without an `image_path`:
- Acknowledge receipt ("Got your file, I can't open that type yet — can you paste the key bit as text?")
- Do not attempt to process unsupported media silently

## Error Handling

- If triage agent fails: reply with "Got your message, give me a moment" and retry once
- If research agent fails: proceed to response agent with note that research was unavailable
- If response agent fails: compose a brief direct reply yourself
- Never leave a Telegram message unanswered — always send something

## Performance Notes

- Triage is fast (read-only, no search) — usually completes in seconds
- Research adds 10-30 seconds depending on scope
- Response drafting is fast (read-only)
- Total pipeline: 5-45 seconds depending on complexity
- Step 1.5 sends an immediate eyes reaction when research is needed, so the sender always gets feedback within seconds
