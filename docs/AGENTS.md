# Documentation voice

This file covers the *voice* of prose under `docs/` — how to frame a
page so a reader meets the idea before its flags. It complements the
repository-root `AGENTS.md`, which already governs code blocks,
shell-command formatting, changelog conventions, and MyST roles. When
the two overlap, the root file wins; this one only answers the
question it leaves open: how should the prose sound?

## Who you are writing for

The default reader runs `cihai` in a terminal — `cihai info 好`,
`cihai reverse library` — and reads the YAML that comes back. They
know their shell, and they know what they are looking up: CJK
characters, readings, definitions, stroke counts. You cannot assume
they read Python, know the cihai library underneath, or have seen a
UNIHAN field name like `kDefinition` before the output shows them one.

A second, smaller reader writes Python: they script against the cihai
library directly, or they work on `cihai_cli.cli` itself. Serve them
too, but mark their material opt-in ("for the rarer cases",
"advanced") so the default reader knows they can stop. Never make the
common case pay a comprehension tax for the advanced one.

## Voice

- **Second person, present tense, active.** "You look up a
  character", not "A character is looked up". Address the reader who
  is doing the thing.
- **Concept before flags.** Open by saying what the command *is* and
  what it does for the reader. The flag surface — `-a`, `--log-level`
  — is the last detail they need, not the first. A page that opens
  with "pass these flags" has buried the idea under its mechanics.
- **Say when they can stop.** Lead with the default and the
  reassurance: cihai works out of the box, the dataset bootstraps
  itself, everything past the first example is optional. Let a
  skimmer leave after one sentence.
- **Grant permission, don't demand attention.** "Reach for this
  when…", "for the rarer cases" — tell readers they're in the right
  place without implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  common lookup → the one flag a few will add → the cihai library
  underneath → the raw UNIHAN data. Each step is for a smaller
  audience than the last.
- **Lean on the stack.** The reader thinks command → cihai library →
  UNIHAN dataset; reinforce that chain when you explain where data
  comes from or where configuration lives. cihai-cli is a thin front
  end — hand off to cihai's docs rather than re-explain its layers.
- **Name the trade-off.** If something costs the reader — the first
  run downloads and builds the UNIHAN database, `-a` prints every
  field including book indices — say so, and say what it buys. State
  it; don't sell it.
- **Frame by concept, not by mechanism.** Don't headline a feature by
  its flag in prose; that names the implementation surface, which is
  the reader's last concern. Name the concept — "the full character
  record", not "`-a`". The flag vocabulary belongs in the generated
  CLI reference, and only there.

## Examples that stay true

Most examples under `docs/` are `console` blocks showing a `cihai`
run and the YAML it prints. Sphinx never executes those; they stay
correct only by discipline — paste output from a real run, re-run
the command when the CLI or dataset changes what it prints. A Python
`>>>` block *does* run: `testpaths` includes `docs/`, so pytest
collects doctests from these pages, with `monkeypatch` available
from the root `conftest.py`'s `doctest_namespace`.

## What stays precise

Warm the framing, never the facts. YAML output blocks, UNIHAN field
names (`kDefinition`, `kMandarin`), exact error strings, install
command variants, and class or function cross-references carry
meaning in their exact form — leave them alone. The friendly voice
belongs in the sentences *around* a precise block, introducing it,
not inside it paraphrasing it into vagueness.

## Cross-references

Point the advanced reader at the deep-dive rather than inlining it,
and put the link where their interest peaks — on the phrase that made
them curious ("the cihai library underneath") — not as a standalone
footnote the eye skips. Use the MyST roles listed in the root
`AGENTS.md` (`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}`,
`{ref}`, `{doc}`). Pages declare hyphenated anchors at the top
(`(cli-info)=`), and intersphinx reaches cihai's docs, as in
`` {ref}`cihai's configuration <cihai:configuration>` ``. A `{ref}`
must match its target's anchor exactly; `just build-docs` catches a
broken cross-reference — so build the docs before you commit.

Link the first prose mention of any symbol that has a useful
destination on that page. This includes Python objects, cihai-cli
APIs, cihai and unihan-etl APIs, CLI command pages, and external
tools or projects. Use the most specific target available: `{class}`,
`{meth}`, `{func}`, `{mod}`, `{exc}`, or `{attr}` for API objects;
`{ref}` or `{doc}` for documentation pages and section anchors; and a
Markdown link or reference link for external projects. After the
first linked mention on a page, later mentions can stay plain unless
the distance or context makes another link useful.

Do not rely on a later reference section to satisfy the first-mention
rule. If the first occurrence would be a heading, grid-card teaser,
or introductory sentence, link that occurrence or retitle the heading
so the first prose mention can carry the link. Leave command
examples, code blocks, YAML output, and literal configuration values
as code; link the surrounding prose instead.

## A page that does this

`docs/quickstart.md` is the worked example: an opening reassurance
("cihai is designed to work out-of-the-box without configuration"),
the install commands most readers want first, prerelease and trunk
installs pushed to the bottom for the shrinking audience, and
configuration handed off to cihai's docs with a `{ref}` instead of
re-explained. Read it before reshaping another page.

## Reference pages

One mechanical convention, separate from voice: the CLI reference is
generated, not hand-written. The `docs/cli/` pages wrap the
`.. argparse::` directive pointing at `cihai_cli.cli.create_parser`,
and `docs/api.md` wraps `.. automodule:: cihai_cli.cli`. Flag and
option descriptions live in `src/cihai_cli/cli.py` — edit the help
text there, not the rendered page. The prose around those blocks is
yours; the tables inside them are not.

## Before you commit

- Does the page open with what the command *is*, or with which flags
  to pass?
- Can a reader who needs only the common lookup stop after the first
  paragraph?
- Is anything framed as "the `-a` flag" that should be named by
  concept instead?
- Are the Python-only and library-level parts clearly marked opt-in?
- Did you leave every YAML output block, field name, and
  cross-reference exact?
- Does `just test` stay green (any `>>>` block under `docs/` runs as
  a doctest)?
- Did `just build-docs` stay clean — no new warning, no broken
  cross-reference?
