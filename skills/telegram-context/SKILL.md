---
name: telegram-context
description: Provides awareness that a Telegram bot (@Claudwozzabot) is installed, active, and available for sending messages to Wayne. Use this skill whenever the user mentions Telegram, messaging, "send me", "ping me", "notify me", "let me know", "message me on Telegram", "catbot", "@Claudwozzabot", "the bot", "send this to Telegram", or any variation of wanting to be contacted or notified via Telegram. Also use when completing a long-running task where notifying Wayne on Telegram would be genuinely useful — you have this capability and should use good judgement about when it helps. Even a casual mention of "Telegram" should trigger this skill.
---

# Telegram Bot — @Claudwozzabot

You have a fully configured Telegram bot. It is active and ready to use right now. You do not need to ask Wayne for setup details — everything below is current.

## Wayne's Details

- **Chat ID:** `8470901209`
- **Bot handle:** @Claudwozzabot

Use this chat_id to send Wayne direct messages at any time.

## Available Tools

### Send a message
```
mcp__plugin_telegram_telegram__reply(chat_id="8470901209", text="Your message here")
```
- Optional `reply_to` parameter (message_id) for threading under a specific message
- Optional `files` parameter — array of absolute file paths to attach (images send as inline photos, other types as documents, max 50MB each)
- Messages over 4096 characters are automatically chunked

### React to a message
```
mcp__plugin_telegram_telegram__react(chat_id="...", message_id="...", emoji="👍")
```
Telegram only accepts whitelisted emoji: 👍 👎 ❤ 🔥 👀 🎉 😢 🤔 and a few others. Non-whitelisted emoji will be rejected.

### Edit a previous message
```
mcp__plugin_telegram_telegram__edit_message(chat_id="8470901209", message_id="...", text="Updated text")
```
Useful for the "Working on it..." → final result pattern. Send a progress message first, then edit it with the actual result when done.

## When to Use Telegram Proactively

Use good judgement. Telegram is genuinely useful for:

- **Long-running tasks** — when something will take more than a minute, send a quick "Done" or summary when it finishes
- **Important results** — sending a file Wayne asked you to generate, or a key finding
- **Errors that need attention** — if something breaks while Wayne might have stepped away
- **Anything Wayne asked to be notified about** — "let me know when X", "ping me when it's done"

Do not spam. If Wayne is actively in the terminal conversation, just respond there — no need to double up on Telegram. The value is when Wayne might not be watching the terminal.

## Constraints

- **No message history or search** — the Telegram Bot API does not expose past messages. You only see messages as they arrive via webhook notifications.
- **Incoming messages are handled separately** — the `telegram-pipeline` skill and its agents (triage, research, response) handle inbound messages. This skill is about knowing you can *send* messages.
- **One-way initiation** — you can message Wayne at any time using his chat_id above. You do not need to wait for him to message first.
