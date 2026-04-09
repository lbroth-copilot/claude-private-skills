# claude-private-skills

A personal [Claude Code](https://claude.ai/code) skill marketplace with a plugin system for easy installation and management.

## Quick Start

```bash
git clone https://github.com/lbroth-copilot/claude-private-skills.git
cd claude-private-skills
./bin/marketplace install personality
```

That's it. All personality skills are now available as `/commands` in Claude Code.

## Available Plugins

### personality

Fun persona modes that change Claude's communication style while keeping full functionality.

```
        ___
       /   \                    ____                _______
      | o o |                  /    \              /       \
       \ ~ /                  | ^  ^ |            |  -   -  |
      __|_|__                  \ -- /              |    >    |
     /       \               __|    |__             \  ___  /
                            /  |    |  \             |     |

    /cave                    /yoda                 /therapist
    Cave-Claude              Master Claude          Dr. Claude
    "Ooga! Me fix bug!"      "Fix this, you must."  "How does that
                                                     make you *feel*?"


        ___                    ____
       /   \                  / ^^ \
      | O_O |                |  oo  |
       \ = /                  \ \/ /
      __|_|__                  |__|
     /  |||  \                /|  |\

    /conspiracy              /eli5
    Agent Claude             Teacher Claude
    "(they're watching       "So a database is
     this terminal)"          like a toy chest!"
```

## Usage

```bash
# List all available plugins and skills
./bin/marketplace list

# Install a plugin (symlinks to ~/.claude/skills/)
./bin/marketplace install personality

# Install to project scope instead
./bin/marketplace install personality --scope project

# Preview without installing
./bin/marketplace install personality --dry-run

# Overwrite existing skills
./bin/marketplace install personality --force

# Remove a plugin
./bin/marketplace uninstall personality

# Validate all skill frontmatter
./bin/marketplace validate

# Regenerate the skill catalog
./bin/marketplace generate
```

## Repository Structure

```
claude-private-skills/
├── .claude-plugin/
│   └── marketplace.json            # Central marketplace manifest
├── bin/
│   └── marketplace                 # CLI: install, uninstall, list, validate, generate
├── catalog/
│   ├── generate-catalog.py         # Catalog generator
│   └── skills-catalog.json         # Generated skill registry
├── plugins/
│   └── personality/                # Plugin: personality modes
│       ├── .claude-plugin/
│       │   └── plugin.json         # Plugin metadata
│       └── skills/
│           ├── cave/SKILL.md
│           ├── yoda/SKILL.md
│           ├── therapist/SKILL.md
│           ├── conspiracy/SKILL.md
│           └── eli5/SKILL.md
└── templates/
    └── skill-template/SKILL.md     # Template for new skills
```

## Creating a New Skill

1. Copy the template:
   ```bash
   cp -r templates/skill-template plugins/<plugin>/skills/<skill-name>
   ```
2. Edit `SKILL.md` — fill in the YAML frontmatter and instructions
3. Validate: `./bin/marketplace validate`
4. Regenerate catalog: `./bin/marketplace generate`
5. Install: `./bin/marketplace install <plugin> --force`

## Creating a New Plugin

1. Create the plugin directory structure:
   ```bash
   mkdir -p plugins/<name>/.claude-plugin plugins/<name>/skills
   ```
2. Add `plugin.json` with name, version, description, author, keywords
3. Add skills under `plugins/<name>/skills/`
4. Update `.claude-plugin/marketplace.json` to register the plugin

## License

MIT
