---
description: Generate a Nano Banana 2 image prompt for a children's book page spread. Specify the character, scene, or page number.
---

Use the image-prompter agent to handle this task.

The user wants a JSON-structured image prompt for Nano Banana 2. Their input: $ARGUMENTS

If a character, scene, or page number was given, read the relevant manuscript or illustration brief from the current project folder and produce the prompt(s) immediately.

If no arguments, ask which book and which page spread(s) they need prompts for.

Always output prompts labelled by page number so Wayne can run them with generate-image.py in the right order.
