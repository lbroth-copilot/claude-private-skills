# What makes text read as AI-written

Contents:
1. Why this matters for a JIRA comment
2. Structural tells (the ones that actually give it away)
3. Vocabulary blacklist
4. Punctuation and formatting tells
5. Rewrite examples
6. What human technical writing looks like instead

---

## 1. Why this matters for a JIRA comment

Readers discount a comment they think a bot wrote, even when the content is right. In a
ticket thread the damage is concrete: the junior dev stops trusting the analysis and
re-does the investigation.

Detection in practice is not statistical. A colleague scanning the ticket recognises a
handful of patterns. Those patterns are listed below in the order they get noticed.

## 2. Structural tells

These matter more than any single word. Research on AI text consistently finds structure,
not vocabulary, to be the reliable signal.

**Hedge opener.** A first sentence that establishes context without carrying information:
"In order to address the issue described in this ticket...", "As part of the ongoing effort
to...". A human starts at the first fact. Delete the warm-up sentence and check whether
anything was lost. Usually nothing was.

**Resolution closer.** A last sentence that ties a bow: "In summary...", "The key takeaway
is...", "This ensures the system remains secure going forward." Human comments end on the
last fact or on an open question. Stopping abruptly is normal and reads as authentic.

**Tricolon (rule of three).** Three parallel items when the real count is two or five:
"faster, safer, and easier to maintain". LLMs default to three regardless of how many
things exist. Count the actual items and list that many. Two is fine. Four is fine.

**Contrast reframe.** "It's not just a build failure, it's a dependency problem." /
"This isn't about X, it's about Y." This manufactures the feeling of insight without
adding any. Say the second half only.

**Symmetry and uniform rhythm.** AI sentences cluster around one length, with 3-5x less
variance than human writing on the same topic. Bullets come out the same length too, each
one a full grammatical sentence. Humans write a fragment, then a long clause-heavy
sentence, then three words.

**Everything resolved.** Every thread closed, every risk acknowledged and dismissed, no
loose ends. Real investigation leaves loose ends. Write them down: "I still don't know why
it only fails on the arm64 runner."

**Restating the question.** Opening by summarising the ticket back at people who can read
the ticket. Skip it.

**Balanced both-sides hedging.** "While this approach has benefits, it also has drawbacks."
Pick a side or state the specific tradeoff with numbers.

**Comprehensiveness for its own sake.** Covering every angle in a status update. A human
writes the two things the reader needs and stops.

## 3. Vocabulary blacklist

High-signal words. Their presence is close to a fingerprint, because models pick them from
the safe middle of the distribution rather than because they fit:

delve, leverage, robust, seamless, seamlessly, tapestry, testament, pivotal, intricate,
meticulous, meticulously, navigate (figurative), landscape (figurative), realm, unlock,
empower, transformative, game-changer, cutting-edge, state-of-the-art, utilize, facilitate,
streamline, harness, underscore, holistic, myriad, plethora, vibrant, crucial, paramount,
foster, elevate, embark, unwavering, ever-evolving, rapidly evolving.

Transition adverbs that no one uses in a ticket comment:

furthermore, moreover, additionally, consequently, notably, importantly, significantly,
subsequently, thus, hence, ultimately, overall, in conclusion, in summary, that being said,
it is worth noting, it is important to note.

Filler adverbs that manufacture depth on a mundane sentence:

quietly, fundamentally, essentially, effectively, arguably, simply put, at its core,
in essence.

Phrase templates:

- "plays a crucial role in"
- "serves as a testament to"
- "a deep dive into"
- "when it comes to X"
- "in today's / in an era where"
- "at the end of the day"
- "the key takeaway"
- "let's break it down"
- "I hope this helps"
- "feel free to reach out"

Technical exceptions: `robust` is legitimate in "robustness test", `navigate` is legitimate
about a UI or a filesystem, `landscape` is legitimate about an actual threat landscape
report. The blacklist targets the figurative use.

## 4. Punctuation and formatting tells

**Em dash (—).** The best-known tell, fair or not. Do not use one. A period, a comma, a
colon, or parentheses covers every case.

**Bold label on every bullet.** `**Root cause:** ...` repeated down a list. One or two is
fine. A full column of them is a template, and templates read as generated.

**Emoji as section markers.** ✅ ⚠️ 🚀 in a status update. Never in these comments.

**Headings on a six-line comment.** Structure heavier than the content it holds.

**Curly quotes and ellipsis characters** (" " ' ' …) in a technical comment where the
surrounding thread uses plain ASCII.

**Perfectly parallel bullet grammar.** Every bullet starting with a gerund, or every bullet
exactly one sentence. Break the pattern.

## 5. Rewrite examples

Before:
> In order to address the vulnerability described in this ticket, I performed a
> comprehensive analysis of the affected component. The investigation revealed that the
> issue stems from an outdated dependency — specifically, the `golang.org/x/net` module.
> Furthermore, it is important to note that this dependency is not reachable from any
> executed code path. In summary, the image is not affected and a VEX statement is the
> appropriate remediation.

After:
> The finding comes from `golang.org/x/net` v0.23.0, which is vendored in the binary but
> never called. I checked with `go mod why golang.org/x/net` and traced the two importing
> packages, both of them test-only helpers. So the image is not exploitable here and we
> can close this with a VEX `vulnerable_code_not_present` statement instead of a rebuild.

What changed: the warm-up sentence is gone, the em dash is gone, "comprehensive",
"revealed", "Furthermore", "it is important to note" and "In summary" are gone, and two
verifiable facts got added (the exact command, the module version).

Before:
> The build is now green. The fix was straightforward, involving three key changes: updating
> the base image, adjusting the patch file, and bumping the Go version. This ensures the
> pipeline remains stable going forward.

After:
> Build is green again: https://github.com/.../actions/runs/1234567. Two changes were
> needed, the base image bump to `cf-base-ubuntu:24.04-20260715` and a rebased patch in
> `patches/0001-fix-cgo.patch`. The Go version was already current, I misread the diff
> earlier.

What changed: the invented third list item is gone, the closer is gone, a link and exact
identifiers are in, and an admitted mistake makes it read as a person.

## 6. What human technical writing looks like

- Specific over general. A version number, a path, a run ID, a timestamp.
- First person, active. "I ran", "I broke", "I don't know yet".
- Uneven. Some sentences short. Some carrying two clauses because the thought needed them.
- Willing to be incomplete. "Haven't checked the arm64 build yet."
- Occasionally informal in a way a template never is. "That took way longer than it should."
- No moral at the end.
