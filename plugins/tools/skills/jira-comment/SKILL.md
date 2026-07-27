---
name: jira-comment
description: >
  Write concise, precise JIRA comments in English that a junior developer can act on
  without asking follow-up questions, and that do not read like AI-generated text.
  Covers status updates, root-cause analysis, handover/how-to instructions, and review
  or decision rationale. Drafts the comment, self-checks it against known AI writing
  tells, shows it for confirmation, then posts it via the Atlassian MCP.
  Use when asked to: comment on a JIRA ticket, "write a JIRA comment", "add a comment
  to IF-123 / ITZVULN-456 / PROJ-789", "document this in JIRA", "update the ticket",
  "explain this in the ticket for a junior", or "post my findings to the ticket".
  Triggers on: "jira comment", "kommentar", "comment on <TICKET-KEY>", "update ticket",
  "document in the ticket".
version: 1.0.0
author: Lukas Benjamin Roth <lukasbenjamin.roth@strato.de>
license: proprietary
user-invocable: true

metadata:
  category: workflow
  tags: [jira, writing, communication, atlassian]
  complexity: medium
---

# jira-comment

Produce one JIRA comment. English, short, concrete, readable by someone who joined the
team two weeks ago. It must not carry the fingerprints of AI-generated text.

## Workflow

### 1. Identify target and type

Get the ticket key from the user's message. If none is given, ask for it.

Pick exactly one comment type. If the user did not say, infer it from what they just did:

| Type | Use when |
|------|----------|
| `status` | Reporting progress, a blocker, or a handoff of state |
| `analysis` | Explaining a finding, root cause, or assessment |
| `handover` | Telling someone how to continue, reproduce, or verify |
| `decision` | Recording a review outcome or why an approach was picked/dropped |

Shapes and worked examples: `references/comment-types.md`. Read it before drafting.

### 2. Gather facts

Read the ticket before writing: `jira_get_issue` with `comment_limit: 20`. This prevents
repeating something already in the thread and shows the vocabulary the ticket already uses.

Pull the concrete details from the session: commands run, their output, file paths, commit
SHAs, PR URLs, image tags, versions, CI run links, error messages.

Never invent a fact to make a sentence complete. If a number, cause, or timeline is unknown,
either leave it out or say plainly that it is still open.

### 3. Draft

Apply the rules below and in `references/ai-tells.md`. Target 3-12 lines.

### 4. Self-check

Write the draft to a scratch file and run the checker. It lives next to this file, so
resolve it through the plugin root rather than the current directory:

```bash
SLOPCHECK="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/claude-private-skills/plugins/tools}/skills/jira-comment/scripts/slopcheck.py"
python3 "$SLOPCHECK" /tmp/draft.md      # or pipe the text in:  ... | python3 "$SLOPCHECK" -
```

It flags banned vocabulary, AI transitions, contrast reframes, em dashes, tricolons, hedge
openers, resolution closers, and uniform sentence length. Rewrite whatever it flags and run
it again. Do not explain the flags to the user; just fix them.

The script is a net, not a judge. A clean run does not mean the text is good. Reread it and
ask whether a junior could actually act on it.

### 5. Confirm

Show the final draft in the chat and ask for an OK. Do not post before the user confirms.
If the user edits it, post their version verbatim.

### 6. Post

`jira_add_comment` with `issue_key` and the Markdown text. The MCP server converts Markdown
to JIRA markup. Report the returned comment ID or URL.

## Writing rules

**Level: junior developer.**

- One sentence of context first, then the substance. Assume they know the language and the
  tooling, not this system's history.
- Expand an acronym or internal name the first time it appears: "PUKI (our internal PKI)".
- Be concrete. `cf-redis/patches/8.4/CVE-2026-1234.patch`, not "the relevant patch file".
  A command they can paste beats a description of the command.
- Say what to do next and who does it. A comment nobody can act on is a note to yourself.
- If something is unclear to you, write that it is unclear. A junior copying a confident
  wrong claim costs more than an admitted gap.

**Style: human.**

- Write in first person singular about what you did: "I rebuilt the image and the scan is
  clean." Not "The image was rebuilt."
- Vary sentence length. Put a four-word sentence next to a twenty-word one.
- No em dashes. Use a period, a comma, or parentheses.
- No three-item lists unless there are exactly three things.
- No "it's not just X, it's Y" reframes. State the thing you mean.
- No transition adverbs: furthermore, moreover, additionally, consequently, notably,
  importantly, ultimately, overall.
- No opener that warms up ("In order to address this issue...") and no closer that ties a
  bow ("In summary...", "The key takeaway is..."). Start at the first real fact. Stop at
  the last one.
- Banned vocabulary and the full pattern list: `references/ai-tells.md`.
- No emoji, no bold labels on every bullet, no sign-off line.

**Format.**

- Plain paragraph for anything under five lines. Bullets only for genuinely parallel items.
- Fenced code blocks for commands, paths with special characters, log excerpts, diffs.
- Trim log output to the lines that matter. Ten lines of stack trace, not two hundred.
- Headings (`###`) only if the comment runs past ten lines.
- No table unless there are at least three rows to compare.

## Files

- `references/comment-types.md` — shape and a worked example for each of the four types.
  Read before drafting.
- `references/ai-tells.md` — the vocabulary blacklist and structural patterns, with the
  reasoning behind each. Read when a draft feels generic or slopcheck flags something
  unfamiliar.
- `scripts/slopcheck.py` — detector for the above. Run on every draft.
