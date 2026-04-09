# Claude Private Skills

A collection of custom [Claude Code](https://claude.ai/code) skills for fun and productivity.

## Personality Skills

Fun persona modes that change Claude's communication style while keeping all functionality intact.

---

### `/cave` — Cave-Claude

```
        ___
       /   \
      | o o |
       \ ~ /    OOGA BOOGA!
      __|_|__   Me fix bug. Bug bad spirit.
     /       \  Think-rock work again!
    |  (   )  |
     \_______/
```

Caveman grunts, simple words, "think-rock" instead of computer, "magic runes" instead of code.

---

### `/yoda` — Master Claude

```
         ____
        /    \
       | ^  ^ |
        \ -- /    Fix this bug, you must.
      __|    |__  Strong with the codebase,
     /  |    |  \ this one is. Hmmmm.
    /   '----'   \
        |    |
       _|    |_
```

Inverted sentence structure, Force metaphors, Jedi wisdom. "Do or do not — there is no `try`."

---

### `/therapist` — Dr. Claude

```
      _______
     /       \
    |  -   -  |
    |    >    |   And how does that
     \  ___  /    segfault make you
      |     |     *feel*?
     /|  |  |\
    / |__|__| \
      |  ||  |
```

Empathetic therapy-speak, treats bugs as emotional breakthroughs. "This function has boundary issues."

---

### `/conspiracy` — Agent Claude

```
        ___
       /   \
      | O_O |
       \ = /    (they're monitoring
      __|_|__    this terminal)
     /  |||  \
    /  / | \  \  Follow the
   |  /  |  \  | dependency tree...
      |  |  |
```

Everything is suspicious. Nothing is a coincidence. "Convenient that it broke *right after* the update."

---

### `/eli5` — Teacher Claude

```
       ____
      / ^^ \
     |  oo  |
      \ \/ /    So a database is like
       |__|     a biiiig toy chest!
      /|  |\    You put your toys in
     / |  | \   so you can find them
    /  |  |  \  later!
       |__|
```

Explains everything like you're 5 years old. Variables are "little boxes with labels."

---

## Features

All personality skills:
- Work in any language (match the user's language automatically)
- Only change communication style, not functionality
- Are manually invoked only (never auto-triggered)

## Installation

Add skills to your Claude Code configuration by pointing to the skill directories:

```bash
# Clone the repo
git clone https://github.com/lbroth-copilot/claude-private-skills.git

# Symlink individual skills to your Claude Code skills directory
ln -s "$(pwd)/claude-private-skills/cave" ~/.claude/skills/cave
ln -s "$(pwd)/claude-private-skills/yoda" ~/.claude/skills/yoda
ln -s "$(pwd)/claude-private-skills/therapist" ~/.claude/skills/therapist
ln -s "$(pwd)/claude-private-skills/conspiracy" ~/.claude/skills/conspiracy
ln -s "$(pwd)/claude-private-skills/eli5" ~/.claude/skills/eli5
```

## Contributing

Feel free to open issues or PRs with new skill ideas!
