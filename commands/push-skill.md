# Push Skill to Cowork

Copy a custom Claude Code skill into the Cowork Plugin directory so it's available in both apps. Replaces any existing copy — no duplicates.

## Usage

`/push-skill <skill-name>`

## Instructions

1. Run `python3 ~/Claude/scripts/push-skill.py $ARGUMENTS` and capture the output
2. Report the result — what was copied, where it went, and any warnings
3. If a WARNING about unexpected UUID sessions appears, flag it clearly — it means Cowork may have rotated its session ID and the script needs updating
