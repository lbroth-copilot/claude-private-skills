#!/usr/bin/env python3
"""Flag AI-writing tells in a draft JIRA comment.

Usage:
    slopcheck.py DRAFT.md
    cat draft.md | slopcheck.py -

Exit code 0 when nothing above LOW severity is found, 1 otherwise.
Fenced code blocks, inline code and URLs are ignored.
"""

import re
import statistics
import sys

# (regex, severity, category, hint)
CHECKS = [
    # --- vocabulary -------------------------------------------------------
    (r"\b(delve|delves|delving)\b", "HIGH", "vocab", "say 'look at' / 'go through'"),
    (r"\b(leverage|leverages|leveraging)\b", "HIGH", "vocab", "use / run / apply"),
    (r"\b(utilize|utilizes|utilizing)\b", "HIGH", "vocab", "use"),
    (r"\b(facilitate|facilitates)\b", "HIGH", "vocab", "name the concrete action"),
    (r"\b(streamline[sd]?|harness(es|ed)?)\b", "HIGH", "vocab", "name the concrete action"),
    (r"\b(seamless|seamlessly)\b", "HIGH", "vocab", "delete, or say what does not break"),
    (r"\b(robust|robustly)\b", "MED", "vocab", "ok in 'robustness test', else be specific"),
    (r"\b(pivotal|paramount|crucial|vital)\b", "HIGH", "vocab", "important, or drop it"),
    (r"\b(intricate|meticulous(ly)?|nuanced)\b", "HIGH", "vocab", "plain adjective or none"),
    (r"\b(tapestry|testament|realm|myriad|plethora|vibrant)\b", "HIGH", "vocab", "drop it"),
    (r"\b(transformative|game.?changer|cutting.?edge|state.of.the.art)\b", "HIGH", "vocab", "drop it"),
    (r"\b(unlock|empower|foster|elevate|embark)\b", "HIGH", "vocab", "plain verb"),
    (r"\b(underscore[sd]?|holistic|unwavering)\b", "HIGH", "vocab", "drop it"),
    (r"\b(ever.evolving|rapidly evolving|fast.paced)\b", "HIGH", "vocab", "drop it"),
    (r"\b(comprehensive|comprehensively)\b", "MED", "vocab", "say what was covered"),
    (r"\bnavigat(e|ing|ed)\b(?!\s+(to|the (file|dir|menu|page|tree)))", "LOW", "vocab",
     "fine for UI/paths, not for problems"),
    (r"\blandscape\b(?!\s*(orientation|mode))", "LOW", "vocab", "fine literally, not as metaphor"),
    (r"\b(plays? a (crucial|key|vital|significant) role)\b", "HIGH", "phrase", "say what it does"),
    (r"\b(deep dive|dive into|let'?s break (it|this) down)\b", "HIGH", "phrase", "just explain it"),
    (r"\bwhen it comes to\b", "HIGH", "phrase", "start at the noun"),
    (r"\bin (today'?s|an era|the world of|the realm of)\b", "HIGH", "phrase", "cut the warm-up"),
    (r"\bit'?s worth noting\b|\bit is (important|worth) to note\b|\bnote that\b",
     "MED", "phrase", "if it is worth noting, just note it"),

    # --- AI transitions ---------------------------------------------------
    (r"(?i)(^|[.;]\s+|\n)\s*(furthermore|moreover|additionally|consequently|notably|"
     r"importantly|subsequently|thus|hence|ultimately|overall)\b",
     "HIGH", "transition", "delete, or start a new sentence"),
    (r"\b(that being said|with that said|as previously mentioned)\b", "HIGH", "transition", "delete"),

    # --- filler adverbs ---------------------------------------------------
    (r"\b(quietly|fundamentally|essentially|effectively|arguably|simply put|at its core|in essence)\b",
     "MED", "filler", "delete, it adds no fact"),
    (r"\b(significantly|substantially|considerably)\b(?!\s+(faster|slower|smaller|larger)\b.*\d)",
     "LOW", "filler", "give the number instead"),

    # --- contrast reframe -------------------------------------------------
    (r"(?i)\bnot just\b[^.\n]{0,60}\b(it'?s|but|it is)\b", "HIGH", "reframe", "state only the second half"),
    (r"(?i)\bis ?n'?t (just )?about\b[^.\n]{0,60}\bit'?s about\b", "HIGH", "reframe", "state only the second half"),
    (r"(?i)\bit'?s not\b[^.\n]{0,60},\s*it'?s\b", "HIGH", "reframe", "state only the second half"),
    (r"(?i)\bnot (only|merely)\b[^.\n]{0,60}\bbut\b", "MED", "reframe", "say both plainly"),

    # --- punctuation / formatting ----------------------------------------
    (r"—", "HIGH", "em-dash", "period, comma or parentheses"),
    (r"\s–\s", "MED", "en-dash", "period, comma or parentheses"),
    (r"\s--\s", "MED", "dash", "period, comma or parentheses"),
    (r"[“”‘’…]", "LOW", "typography", "use plain ASCII quotes and ..."),
]

CLOSERS = re.compile(
    r"(?i)\b(in summary|in conclusion|to summarize|to sum up|at the end of the day|"
    r"the key takeaway|all in all|going forward|this ensures|hope (this|that) helps|"
    r"feel free to (reach out|ask)|let me know if you (have any|need anything))\b"
)

OPENERS = re.compile(
    r"(?i)^\s*(in order to|in today'?s|in an era|as part of the ongoing|as we all know|"
    r"this (comment|update) (serves|is intended|aims)|following up on the above|"
    r"i wanted to (provide|share|give) (an?|some))"
)

TRICOLON = re.compile(
    r"\b[\w'’()./-]+(?:\s+[\w'’()./-]+){0,3},\s+[\w'’()./-]+(?:\s+[\w'’()./-]+){0,3},\s+"
    r"(?:and|or)\s+[\w'’()./-]+"
)

BOLD_BULLET = re.compile(r"^\s*[-*+]\s+\*\*[^*]{2,40}:?\*\*")

EMOJI = re.compile(
    "[" "\U0001F300-\U0001FAFF" "☀-➿" "⬀-⯿" "✅❌️" "]"
)

FIRST_PERSON = re.compile(r"(?i)\b(i|i'?ve|i'?m|i'?ll|my|we|we'?ve|our)\b")

SEVERITY_RANK = {"HIGH": 0, "MED": 1, "LOW": 2}


def strip_noise(lines):
    """Blank out fenced code blocks, inline code and URLs, keeping line numbering."""
    out = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence:
            out.append("")
            continue
        clean = re.sub(r"`[^`]*`", " ", line)
        clean = re.sub(r"https?://\S+", " ", clean)
        clean = re.sub(r"\[([^]]*)]\([^)]*\)", r"\1", clean)
        out.append(clean)
    return out


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if len(p.split()) >= 3]


def analyse(raw):
    lines = raw.splitlines()
    clean = strip_noise(lines)
    findings = []

    def add(lineno, sev, cat, match, hint):
        findings.append((lineno, sev, cat, match.strip()[:60], hint))

    for i, line in enumerate(clean, 1):
        if not line.strip():
            continue
        spans = []  # (category, start, end) of matches already reported on this line
        for pattern, sev, cat, hint in CHECKS:
            for m in re.finditer(pattern, line, re.IGNORECASE):
                if any(c == cat and m.start() < e and s < m.end() for c, s, e in spans):
                    continue  # a broader pattern of the same kind already caught this
                spans.append((cat, m.start(), m.end()))
                add(i, sev, cat, m.group(0), hint)
        for m in TRICOLON.finditer(line):
            add(i, "MED", "tricolon", m.group(0),
                "three items is the default AI count, list the real number")
        for m in EMOJI.finditer(line):
            add(i, "HIGH", "emoji", m.group(0), "no emoji in a ticket comment")

    body = " ".join(l.strip() for l in clean if l.strip())
    sents = sentences(body)

    if sents and OPENERS.search(sents[0]):
        add(1, "HIGH", "hedge-opener", sents[0], "start at the first real fact")

    tail = " ".join(sents[-2:]) if sents else ""
    m = CLOSERS.search(tail)
    if m:
        add(len(lines), "HIGH", "resolution-closer", m.group(0), "stop at the last fact")

    bold_bullets = sum(1 for l in clean if BOLD_BULLET.match(l))
    if bold_bullets >= 3:
        add(0, "MED", "template", f"{bold_bullets} bold-labelled bullets",
            "reads as a filled-in template, use prose for some of them")

    if len(sents) >= 5:
        counts = [len(s.split()) for s in sents]
        mean = statistics.mean(counts)
        cv = statistics.pstdev(counts) / mean if mean else 0
        if cv < 0.28:
            add(0, "MED", "rhythm",
                f"sentence lengths {counts} (variation {cv:.2f})",
                "human drafts vary more, add a short sentence or merge two")

    words = len(body.split())
    if words >= 40 and not FIRST_PERSON.search(body):
        add(0, "LOW", "voice", "no first person",
            "say what you did: 'I ran', 'I checked'")

    if len([l for l in lines if l.strip()]) > 15:
        add(0, "LOW", "length", f"{len(lines)} lines",
            "a JIRA comment over ~12 lines usually carries two messages, split it")

    return findings


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    raw = sys.stdin.read() if args[0] == "-" else open(args[0], encoding="utf-8").read()

    findings = analyse(raw)
    if not findings:
        print("slopcheck: clean")
        return 0

    findings.sort(key=lambda f: (SEVERITY_RANK[f[1]], f[0]))
    seen = set()
    counts = {"HIGH": 0, "MED": 0, "LOW": 0}
    for lineno, sev, cat, match, hint in findings:
        key = (sev, cat, match.lower())
        if key in seen:
            continue
        seen.add(key)
        counts[sev] += 1
        where = f"line {lineno}" if lineno else "whole text"
        print(f"{where:>11}  {sev:<4}  {cat:<18}  {match!r}\n{'':>11}  -> {hint}")

    print(f"\nslopcheck: {counts['HIGH']} high, {counts['MED']} medium, {counts['LOW']} low")
    return 1 if counts["HIGH"] or counts["MED"] else 0


if __name__ == "__main__":
    sys.exit(main())
