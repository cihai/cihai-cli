# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, `CHANGES`, release notes, commit messages, CLI help text and error
messages, logging, docstrings, source comments, and the `docs/` Sphinx pages —
every surface a reader reaches.

For environment setup, the gates, and pull request workflow, see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Voice

Three surfaces, one voice. A docstring says what a caller may rely on; a
`CHANGES` entry says what changed; prose says what happens. All three are
present tense, lead with the thing being described, and stop. Why it was built
that way belongs in the commit message, which is timestamped and attached to
the diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks. Prefer
short declarative sentences, one operational fact each. Do not explain Python
to Python developers; do explain this project's semantics.

Type annotations describe shape. Documentation describes meaning. A sentence
that restates a signature has said nothing.

Use MUST, SHOULD, and MAY only where the normative sense is meant. Say what
actually happens rather than that something is "supported".

| Instead of                       | Prefer                             |
| --------------------------------- | ----------------------------------- |
| "We added…"                      | "`cihai info` now accepts…"        |
| "New and improved"               | "`cihai reverse` now…"             |
| "powerful", "seamless"           | state the capability                |
| "easily", "simply", "just"       | omit                                |
| "simple", "obvious", "intuitive" | omit                                 |
| "robust"                         | name the failure that is handled    |
| "comprehensive"                  | name what is covered                |
| "production-ready"               | state the guarantee                 |
| "optimized", "blazingly fast"    | give the magnitude                  |
| "various fixes"                  | name the components                 |
| "under the hood"                 | omit unless observable              |
| "please note that", "note that"  | state the fact                      |
| "leverage", "utilize"            | "use"                                |
| "delve into"                     | "read", or omit                     |
| "best practices"                 | name the practice                   |
| "in order to"                    | "to"                                 |

## Who you are writing for

The default reader runs `cihai` in a terminal — `cihai info 好`, `cihai reverse
library` — and reads the YAML that comes back. They know their shell, and they
know what they are looking up: CJK characters, readings, definitions, stroke
counts. Do not assume they read Python, know the `cihai` library underneath, or
have seen a UNIHAN field name like `kDefinition` before the output shows them
one.

A second, smaller reader writes Python: they script against the `cihai`
library directly, or they work on `cihai_cli.cli` itself. Serve them too, but
mark their material opt-in — "for the rarer cases", "advanced" — so the default
reader knows they can stop. Docstrings and source comments address this second
reader directly; README and CLI help text address the first. Never make the
common case pay a comprehension tax for the advanced one.

Rules that follow:

- **Second person, present tense, active.** "You look up a character", not "A
  character is looked up". Address the reader who is doing the thing.
- **Concept before flags or API surface.** Open by saying what the command or
  object *is* and what it does for the reader. The flag surface (`-a`,
  `--log-level`) or the signature is the last detail they need, not the first.
  A page that opens with "pass these flags" has buried the idea under its
  mechanics.
- **Say when they can stop.** Lead with the default and the reassurance: cihai
  works out of the box, the UNIHAN dataset bootstraps itself on first use,
  everything past the first example is optional. Let a skimmer leave after one
  paragraph.
- **Grant permission, do not demand attention.** "Reach for this when…", "for
  the rarer cases" — tell readers they are in the right place without implying
  they must read on.
- **Progressive disclosure.** Order by how many readers need it: the common
  lookup, then the one flag a few will add (`--all`), then the `cihai` library
  underneath, then the raw UNIHAN data. Each step is for a smaller audience
  than the last.
- **Lean on the stack.** The reader thinks command → `cihai` library → UNIHAN
  dataset; reinforce that chain when explaining where data comes from or where
  configuration lives. cihai-cli is a thin front end — hand off to `cihai`'s
  docs (`{ref}` with the `cihai:` intersphinx prefix) rather than re-explain
  its layers.
- **Name the trade-off.** If a call costs something — the first run downloads
  and builds the UNIHAN database, `-a` prints every field including book
  indices — say so, and say what it buys. State it; do not sell it.
- **Frame by concept, not by mechanism.** Do not headline a feature by its flag
  in prose; that names the implementation surface, which is the reader's last
  concern. Name the concept — "the full character record", not "`-a`". The
  flag vocabulary belongs in the generated CLI reference, and only there.

## README

A README is the shortest path from "what is this?" to competent use, not the
project's autobiography.

The first sentence is a contract. It says what abstraction the reader has been
handed, concretely enough to tell this package apart from the neighbouring
one.

Get to a runnable command before anything the reader can skip. A logo, a
mission statement, a comparison matrix and three paragraphs of history in
front of the install line all cost the same thing.

State the minimum Python version and meaningful platform constraints in prose,
not only in badges. `requires-python` in `pyproject.toml` is the authority; the
README must agree with it.

Name the distribution (`cihai-cli`), the import (`cihai_cli`), and the
executable (`cihai`) separately wherever they differ. That distinction
prevents a Python-specific class of confusion.

Examples are executable, not illustrative fiction. Never
`cihai <some-options>`. See
[Documented examples that run](#documented-examples-that-run) for which blocks
are executed and how to write one that qualifies.

Document the semantic model, not the flag list. `--help` already enumerates
flags; what it cannot say is precedence, filesystem effects, what goes to
stdout versus stderr, and what a non-zero exit means. See
[CLI, help text, and error messages](#cli-help-text-and-error-messages).

State defaults explicitly — defaults are API. State negative guarantees where
they exist: "does not modify your configuration file", "bootstraps the UNIHAN
dataset on first use and caches it, no network access afterward". They
establish boundaries faster than any amount of description.

Headings stay conventional and stable, because people deep-link them. Badges
are few and load-bearing.

## Documented examples that run

Examples in this fleet are tests. This section is the contract for writing one
the test suite can actually see, and states this repo's real mechanism.

**A fence tag is cosmetic. Only a `>>> ` prompt executes.** A block written as

    ```python
    from cihai_cli._colors import Colors
    ```

is prose that looks like a test. Nothing collects it, nothing runs it, and it
can be wrong for years. The same block written with prompts is a test:

    ```python
    >>> from cihai_cli._colors import Colors
    ```

This is the single most expensive mistake available when editing
documentation, because removing the prompts leaves a green test suite and a
silently deleted test. When editing a file that contains examples, count the
prompts before and after.

**The fence tag is `python`.** Not `pycon`, not bare. This is uniform across
the fleet and tooling depends on it.

**Where examples run, in this repo.** `pyproject.toml`'s
`[tool.pytest.ini_options]` sets `addopts = "... --doctest-modules"` and
`testpaths = ["src/cihai_cli", "tests", "docs"]`. A `>>> ` block under
`src/cihai_cli/` or `docs/` is collected and run by `pytest`. **`README.md` is
not in `testpaths`** — a `>>> ` block there is inert; it never runs, and
`pytest --collect-only` will not show it. Keep README examples as plain
`console` blocks with real output pasted in, correct by discipline rather than
by execution.

`doctest_optionflags = "ELLIPSIS NORMALIZE_WHITESPACE"` is set globally, so
`...` elides variable output (a `-a` field list, a UNIHAN record whose
non-human fields differ by dataset version) and whitespace differences do not
fail a comparison.

The root `conftest.py` defines an autouse `doctest_namespace` fixture that
injects exactly one name into every doctest: **`monkeypatch`** (a
`pytest.MonkeyPatch` instance, undone after the block runs). A doctest may use
`monkeypatch.setenv(...)` and `monkeypatch.delenv(...)` without importing
anything; see `src/cihai_cli/_colors.py` for a worked example that toggles
`NO_COLOR`. No other name is injected — do not assume `cihai`, `Cihai`, or any
fixture from `tests/conftest.py` is available in a doctest; import what you
need.

**A second, separate mechanism checks `docs/index.md`.**
`tests/test_docs_examples.py` is not a doctest: it is a regular pytest test
that reads `docs/index.md`, finds the literal lines `$ cihai info 好` and `$
cihai reverse good`, takes the fenced block that follows each, runs the real
CLI against a fixture-backed UNIHAN database, and asserts the page's block
appears in the command's captured log output. Those two command lines and
their following YAML fences are load-bearing test input even though neither
carries a `>>> ` prompt. Do not rewrite or remove either command line in
`docs/index.md`, or reword its output block, without updating
`tests/test_docs_examples.py` to match.

**`# doctest: +SKIP` is not permitted.** It is a workaround that tests
nothing. Use `monkeypatch`, or narrow the example.

**Do not downgrade a doctest to a non-executed block to make it pass.** A
` ```yaml ` output block or an unprompted fence does not run. If an example
cannot pass, fix the example or fix the code.

**Docstring examples** use the NumPy `Examples` section:

    Examples
    --------
    >>> style("hello", fg="green")
    '\x1b[32mhello\x1b[0m'

**Room to grow.** The doctest collector reads any file under `testpaths`, so a
prompted block added to `docs/` or (were it ever added to `testpaths`)
`README.md` is executed from that moment with no configuration change. The
MyST `{doctest}` directive and Sphinx's own `.. doctest::` block (enabled via
`sphinx.ext.doctest` in `docs/conf.py`, run with `just -f docs/justfile
doctest`) are available for an explicitly marked block inside a documentation
page; none of the current pages use them.

## CLI, help text, and error messages

`cihai` is the flagship command of the cihai family, and this is this repo's
real, observed I/O contract — not an aspiration.

**Exit statuses.**

| Exit | Meaning | Example |
| ---- | ------- | ------- |
| `0`  | Command ran to completion, including a lookup that found nothing. | `cihai info 好`; `cihai info <char-not-in-dataset>` |
| `2`  | argparse usage error: missing required argument, unknown flag, invalid subcommand. | `cihai info` (no character); `cihai bogus` |

A `0` exit does not mean a character was found. `cihai info` and `cihai
reverse` log `"No records found for <term>"` and exit `0` on a miss, the same
as on a hit. Scripting against "did this find anything" means checking the
output, not the exit status.

**stdout vs stderr.** `--help` and `--version` are argparse-native and print to
stdout. Everything else the command produces — the YAML record from `info` and
`reverse`, `"No records found for …"`, and `"Bootstrapping Unihan database"` —
is emitted through `logging` at `INFO` level to a `StreamHandler`, which
defaults to **stderr**. `cihai info 好 | less` shows nothing; the record is on
stderr. Redirect or capture accordingly (`2>&1`, `capsys.readouterr().err` in
tests).

**`--log-level` gates the actual output, not just diagnostics.** Because the
YAML record is an `INFO`-level log record, `cihai --log-level WARNING info 好`
prints nothing at all — raising the level above `INFO` silences the command's
result along with its diagnostics. `--log-level` is not a verbosity dial
layered on top of a separate output channel; it is the same channel.

**No stable machine-readable contract today.** The YAML comes from
`yaml.safe_dump`, unfiltered field selection differs between the default view
and `--all`, and it travels over the logging channel described above. Do not
document it as a stable interface for scripts; state only what it does today.
A human should decide whether to give it one (see the report for this
refactor).

**Help text is test-asserted; edit it at the source.** `CLI_DESCRIPTION`,
`INFO_DESCRIPTION`, and `REVERSE_DESCRIPTION` in `src/cihai_cli/cli.py` build
the `examples:` sections argparse prints for `--help`.
`tests/test_cli.py::test_cli_help_contains_examples` and its per-subcommand
siblings assert on exact substrings of that generated text (`"info
examples:"`, `"cihai info 好"`). Edit help text and its examples in
`src/cihai_cli/cli.py`; never hand-edit the rendered `docs/cli/*.md` pages to
change what `--help` prints — those pages wrap `.. argparse::` and regenerate
from the parser (see [Reference pages](#reference-pages)).

**Error messages** are lowercase-led sentences naming the term that failed
(`"No records found for %s"`), logged rather than printed, and carry no
recovery advice beyond what `--all` or `--help` already documents.

## Logging

Logging is this CLI's user-facing output channel (see
[CLI, help text, and error messages](#cli-help-text-and-error-messages)), so
its conventions are prose policy, not an implementation detail.

**Logger setup.** Use `logging.getLogger(__name__)` in every module. Add a
`NullHandler` in library `__init__.py` files. Never configure handlers,
levels, or formatters in library code — `setup_logger` in `cli.py` is the
CLI's own entry point's job, once, at the top.

**Structured context via `extra`.** Pass structured data on a log call where
it helps filtering, searching, or test assertions.

Core keys (stable, scalar, safe at any level):

| Key | Type | Context |
| --- | ---- | ------- |
| `unihan_field` | `str` | UNIHAN field name |
| `unihan_source_file` | `str` | source data file path |
| `unihan_record_count` | `int` | records processed |
| `cihai_command` | `str` | CLI command name |

Heavy/optional keys (`DEBUG` only, potentially large):

| Key | Type | Context |
| --- | ---- | ------- |
| `unihan_stdout` | `list[str]` | subprocess stdout lines (truncate or cap) |
| `unihan_stderr` | `list[str]` | subprocess stderr lines (same caveats) |

Treat established keys as compatibility-sensitive — downstream users may build
dashboards and alerts on them. Change deliberately.

`snake_case`, `unihan_` prefix, stable scalars over ad-hoc objects. Heavy keys
stay `DEBUG`-only; consider a companion `_len` field or hard truncation instead
of logging an unbounded list.

**Lazy formatting.** `logger.debug("msg %s", val)`, never an f-string in a log
call: interpolation is skipped entirely when the level is filtered, and a
literal `"Running %s"` groups as one signature in an aggregator instead of one
unique line per call. Guard an expensive `val` with
`if logger.isEnabledFor(logging.DEBUG)`.

**`stacklevel` for wrappers.** Increment it for each wrapper layer so
`%(filename)s:%(lineno)d` and any OpenTelemetry `code.filepath` point at the
real caller. Re-verify whenever call depth changes.

**`LoggerAdapter` for persistent context.** For an object with stable identity
(a dataset, a reader, an exporter), use `LoggerAdapter` instead of repeating
the same `extra` on every call — override `process()` to merge;
`merge_extra=True` simplifies this on Python 3.13+.

**Log levels.**

| Level | Use for | Examples |
| ----- | ------- | -------- |
| `DEBUG` | Internal mechanics, data I/O | Field parsing, record transformation |
| `INFO` | Data lifecycle, user-visible output | Bootstrap completed, a lookup result |
| `WARNING` | Recoverable issues, deprecation, user-actionable config | Missing optional field, deprecated data format |
| `ERROR` | Failures that stop an operation | Download failed, parse error |

Config-discovery noise stays `DEBUG`; only surprising or user-actionable
config issues rise to `WARNING`.

**Message style.** Lowercase, past tense for events: `"download completed"`,
`"parse error"`. No trailing punctuation. Keep the message short; put details
in `extra`, not the string.

**Exception logging.** Use `logger.exception()` only inside an `except` block
you are not re-raising from. Use `logger.error(..., exc_info=True)` for a
traceback outside an `except` block. Never `logger.exception()` followed by
`raise` — that duplicates the traceback; either add `extra` context that would
otherwise be lost, or let the exception propagate.

**Testing logs.** Assert on `caplog.records` attributes, not string matching
on `caplog.text`. Scope capture (`caplog.at_level(logging.DEBUG,
logger="cihai_cli.cli")`), filter records rather than index by position
(`[r for r in caplog.records if hasattr(r, "unihan_field")]`), assert on
schema (`record.unihan_record_count == 100`, not `"100 records" in
caplog.text`). `caplog.record_tuples` cannot access `extra` fields — always
use `caplog.records`.

**Avoid:** f-strings/`.format()` in log calls; unguarded logging in hot loops;
catch-log-reraise without adding context; `print()` for diagnostics; logging a
secret env var's value (log the key name only); non-scalar ad-hoc objects in
`extra`; a format string that requires a custom `extra` field with no default
(a missing key raises `KeyError`).

## The changelog

`CHANGES` is the changelog, rendered as the project's changelog page via
`{include}` in `docs/history.md`. Modeled on Django's release-notes shape:
deliverables get titles and prose, not bullets.

**Release entry boilerplate.** Every release header is `## cihai-cli X.Y.Z
(YYYY-MM-DD)`. The file opens with a `## cihai-cli X.Y.Z (unreleased)`
placeholder fenced by `<!-- KEEP THIS PLACEHOLDER ... -->` and `<!-- END
PLACEHOLDER ... -->` HTML comments — new entries land immediately below the
END marker, never above it.

**Unreleased entries carry no lead paragraph and no version summary.**
Sections only (`### Breaking changes`, `### What's new` deliverables, `###
Fixes`, …). Speaking for a release — what the version "is", "ships", or
"focuses on" — is presumptuous before its scope is final. Only the person
cutting the release writes that lead, and only when the user explicitly asks
to release. Never write or edit a lead paragraph from a feature branch, and
never ask or imply that a release should happen.

**A release lead paragraph**, once written, is two to four sentences, opens
with the version as sentence subject (*"cihai-cli X.Y.Z ships …"*) so it reads
standalone when excerpted, states user-visible takeaways rather than internal
mechanism, and cross-references detail with `{ref}` to stay compact.

**Each deliverable is a section, not a bullet.** Inside `### What's new`, every
distinct deliverable gets a `#### Deliverable title (#NN)` heading naming it in
user vocabulary, followed by one to three prose paragraphs. Do not wrap a
paragraph in `- ` — bullets are for enumerable lists, not paragraph
containers. Cross-link detail docs (`See {ref}`foo` for details.`) so prose
stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the
deliverable, in user vocabulary?" If that has no one-sentence answer, the
entry is not ready. Mechanism — helper internals, byte counters,
schema-validation locations — belongs in PR descriptions and code comments,
not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`,
`### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`, `###
Development`. Dev tooling (helper scripts, internal automation) lives under
`### Development`. A breaking change shows the migration path with concrete
inline code — a `# Before` / `# After` fenced block — not a pointer to one.
Dependency floor bumps use the form ``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**When bullets are appropriate.** Catch-all sections (`### Fixes`,
occasionally `### Documentation`) with three or more genuinely small items use
bullets — one line each, never paragraphs. If a bullet swells past two lines,
promote it to a `#### Title (#NN)` heading with a prose body.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**Anti-patterns.** Fragile metrics that go stale silently — token ceilings,
third-party version pins, percent benchmarks, exact byte counts. Describe the
capability, not the math. Private symbols and internal jargon — leading
underscore identifiers, algorithm names exposed for the first time, backend
scaffolding. Walls of text dressed up as bullets. Breaking changes buried
mid-entry instead of given their own subheading at the top.

**Always link autodoc'd APIs.** Any class, method, function, exception, or
attribute with its own rendered page is cited via the matching role —
`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}` — never plain backticks. A doc
page without an explicit ref label uses `{doc}`; an anchor inside a page uses
`{ref}`. Plain backticks stay correct for code syntax, env vars, parameter
names, and file paths that are not doc pages.

**Summarization style.** Asked "what changed in the latest version", lead with
the entry's lead paragraph (paraphrased if needed), then each `####`
deliverable heading under `### What's new` with a one-sentence summary. Cite
`(#NN)` only if asked for source links. Do not invent versions, dates, or
numbers absent from `CHANGES`. Do not quote line numbers or file offsets —
those shift as the file evolves.

Versions are PEP 440 identifiers. Semantic-versioning meaning applies to the
documented public API, which includes command names, options, exit statuses,
UNIHAN field selection (`--all` vs. the default set), and configuration keys —
not only imported Python symbols.

## Docstrings

The prime directive: never restate the type. The annotation is the source of
truth; the docstring carries what the annotation cannot.

This is documentation debt wearing a docstring:

    def get_id(pane: Pane) -> str:
        """Get the pane's identifier.

        Parameters
        ----------
        pane : Pane
            The pane.

        Returns
        -------
        str
            The identifier.
        """

Document instead the dimensions the type system cannot encode: mutation,
ownership, ordering, timing, failure (which exceptions, what triggers each),
idempotence, units and ranges, boundary behaviour, platform differences, and
the security boundary — what is executed versus only read.

**Classes with fields** — `NamedTuple`, dataclasses — document every field, in
an `Attributes` section or as a docstring on each field:

```python
class HelpTheme(t.NamedTuple):
    """Color codes for help text elements.

    Attributes
    ----------
    prog : str
        Program name color (magenta + bold).
    action : str
        Subcommand/action color (cyan).
    reset : str
        ANSI reset code.
    """
```

Autodoc renders every field whether or not you describe it, so an undocumented
field ships to the API docs as "Alias for field number 0" and a dataclass
field ships bare. Document all of them — a class with three fields and two
documented still ships a stub for the third.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. Do not repeat an introspectable
signature.

One docstring dialect per repository — NumPy style here, enforced by
`ruff`'s `pydocstyle` convention rather than relitigated in review.

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real time
rediscovering intent, an invariant, a constraint, or a failure mode the code
and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write this
comment, at this length? Those projects state the constraint and stop. They do
not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that hand-syncs a
value the code owns — a count, an offset, a line reference, a duplicated
constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several facts, in
which case split it, or arguing, in which case cut it to the fact.

Rationale, alternatives weighed, and the story of how the code got here belong
in the commit message: timestamped, attached to the exact diff, and free to
maintain.

A comment often holds both a constraint and the deliberation that found it.
Keep the constraint, cut the deliberation. "Runs at most once per second"
survives; "this is the right trade for now" does not.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, lifetime, and concurrency requirements
  that types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not reintroduce
  the bug.
- A high-level sketch of an algorithm whose local operations do not reveal the
  whole.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- Speculation about future requirements.
- History version control already holds, including commented-out code.
- Ticket and issue numbers. They say nothing to a reader without tracker
  access, and they rot when the tracker moves. Unfinished work goes in the
  tracker, not the source.
- Transient observations — "currently", "for now", "the latest release" —
  that go stale with no nearby edit.

### The upkeep gate in practice

It reaches values that track our own code. It does not reach frozen external
facts.

Bad (Delete):

```python
# There are 321 tests to complete for servers.
```

Good (Keep):

```python
# CPython < 3.11 has no ExceptionGroup, so this branch stays.
```

### Documentation exception

Doctests, minimal usage examples, and `Parameters`, `Returns`, `Attributes`,
and `Raises` entries on public API are exempt from the loss gate — they serve
the caller, not the maintainer. They are exempt from nothing else. Ceiling: a
good man page entry. Autodoc ships every field whether or not you describe it,
and a doctest that runs is also a test — both fall under this exception.

## Terminology and capitalization

Pick the domain noun and keep it. If the code calls something a session, do
not call it a workspace in one paragraph and an environment in the next.

Stable vocabulary is what makes search, deep links, and an agent's retrieval
work at all.

Python and PyPI keep their own capitalisation. Distribution names are written
as they are published. See [README](#readme) for the distribution/import/
executable distinction (`cihai-cli` / `cihai_cli` / `cihai`).

**CJK/UNIHAN terms, pinned:**

- **Character** — the CJK ideograph itself: what a reader passes to `cihai
  info` or gets back from `cihai reverse` (好, 圕). This is the default term.
  Do not call it a "glyph" or a "codepoint" as a synonym.
- **Codepoint** — the Unicode scalar value, always written `U+XXXX`
  (uppercase hex, no leading zeros beyond four digits). The CLI exposes it as
  the `ucn` field.
- **Glyph** — a specific visual rendering or regional variant of a character,
  used narrowly: the `kHKGlyph` field names a Hong Kong glyph variant. Do not
  use "glyph" as a general synonym for "character" — the docs' own CLI
  reference (`docs/cli/index.md`) already distinguishes "character by glyph or
  codepoint" and that distinction is the one to preserve.
- **UNIHAN field names** — write them exactly as UNIHAN and the CLI's own
  output do: `kDefinition`, `kMandarin`, `kCantonese`, `kTotalStrokes`, in
  backticks, camelCase with a leading lowercase `k`. Never retitle a field in
  prose ("the Mandarin reading field" is fine as a description; `kMandarin`
  stays `kMandarin` when referenced as a field).
- **CJK text in prose and examples** — write the literal character (好, not
  its codepoint or a transliteration) as a command argument or example output.
  Quote it in backticks only when it appears as a shell argument or metavar
  (`` `<character>` ``); leave it unquoted in flowing prose ("look up 好").
  Preserve tone marks and diacritics from the dataset exactly (`hǎo`, not
  `hao3` or `hao`) — they are the reading, not a decoration.

Do not write counts into prose — how many symbols exist, how many tests there
are. They go stale silently and no reader needs them. Counts that pin a
fixture or guard an invariant are different, and belong in code.

## MyST roles and cross-references

Class references use `{class}`, methods use `{meth}`, functions use `{func}`,
exceptions use `{exc}`, attributes use `{attr}`, internal anchors use `{ref}`,
doc-path links use `{doc}`. A `{ref}` must match its target's anchor exactly;
`just build-docs` catches a broken cross-reference — build the docs before you
commit.

Link the first prose mention of any symbol that has a useful destination on
that page: Python objects, cihai-cli APIs, `cihai` and `unihan-etl` APIs, CLI
command pages, and external tools or projects (a Markdown link for those).
Point an advanced reader at the deep-dive rather than inlining it, and put the
link on the phrase that made them curious ("the cihai library underneath"),
not as a standalone footnote the eye skips. Pages declare hyphenated anchors
at the top (`(cli-info)=`), and intersphinx reaches `cihai`'s docs, as in
`` {ref}`cihai's configuration <cihai:configuration>` ``.

After the first linked mention on a page, later mentions can stay plain unless
distance or context makes another link useful. Do not rely on a later
reference section to satisfy the first-mention rule — if the first occurrence
is a heading, grid-card teaser, or introductory sentence, link that occurrence
or retitle the heading so the first prose mention can carry the link. Leave
command examples, code blocks, YAML output, and literal configuration values
as code; link the surrounding prose instead.

### Reference pages

The CLI reference is generated, not hand-written: `docs/cli/*.md` wraps the
`.. argparse::` directive pointing at `cihai_cli.cli.create_parser`, and
`docs/api.md` wraps `.. automodule:: cihai_cli.cli`. Flag and option
descriptions live in `src/cihai_cli/cli.py` — edit the help text there, not
the rendered page (see
[CLI, help text, and error messages](#cli-help-text-and-error-messages)). The
prose around those blocks is yours; the tables inside them are not.

### What stays precise

Warm the framing, never the facts. YAML output blocks, UNIHAN field names,
exact error strings, install command variants, and class or function
cross-references carry meaning in their exact form — leave them alone. The
friendly voice belongs in the sentences *around* a precise block, introducing
it, not inside it paraphrasing it into vagueness.

## Markdown

Prose wraps at 80 columns. Table rows, badge lines, and long links are exempt,
because breaking them harms rendering. A pull request or issue body does not
wrap at all: GitHub renders a single newline as a space in a file and as a
line break in a comment, so a wrapped comment body arrives as ragged stubs.

GitHub alert blocks — `> [!NOTE]`, `> [!WARNING]` — render as literal text
outside GitHub, so reserve them for at most one load-bearing warning per
document. Write the sentence so it carries the fact on its own, and a renderer
that drops the marker loses nothing.

Do not use a local absolute path or an email address in anything published.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action. Executed examples are exempt — the test suite runs them,
nobody pastes them.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is then
  one logical command.
- **Explanations go in prose above the block**, never as `#` comments inside
  it.
- **Command menus are per-command blocks with prose lead-ins**, not tables.
- **Shell commands use the `console` tag with a `$ ` prefix.** This separates
  interactive commands from scripts and enables prompt-aware copy.
- **Split long commands with `\`** — one flag or flag+value pair per indented
  continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing `(#NN)`
pull request reference, and wrap body lines at 72. Separate the `why:` and
`what:` blocks with a blank line.

Routine maintenance commits drop the colon and take a capitalised description,
which is what distinguishes them at a glance in `git log --oneline`:

```
py(deps[dev]) Bump dev packages
ai(rules[AGENTS]) Judge comments by three gates
```

Everything that changes behaviour keeps the colon.

Common types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **ci**: Workflow and pipeline changes
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[commands])**: Claude Code command changes

Example:

```
cli(feat[reverse]): Add --all to reverse lookups

why: Match info's field selection for consistency.

what:
- Add the --all flag to the reverse subparser
- Route it through command_reverse's show_all parameter
```

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

### Release commits

Never create tags. Never push tags. The owner handles tagging and tag pushes,
because a tag triggers the publish workflow.

A release commit subject is plain and short: `Tag v<version>`. The detailed
why and what go in the body. Do not use the `Scope(type[detail]):` format for
a release — it buries the lede.

## Slop prevention

Treat AI slop as review-hostile noise, not as proof that text or code is
wrong. The goal is to maximise information density.

- **AI signatures.** No "Generated by", no conversational filler, no
  unexplained emoji, no tool metadata.
- **Brittle references.** No hard-coded line numbers, fragile file counts,
  dated "as of" claims, bare SHAs, or local absolute paths — unless they are
  strict evidentiary artefacts such as a benchmark log.
- **Diff narration.** Do not restate what moved, was renamed, or was removed
  in anything the reader holds alongside the diff: code, docstrings, README,
  or a pull request description. The diff and the commit message already
  carry it.
- **Branch-internal narrative.** Do not mention intermediate states,
  abandoned approaches, or "no longer" behaviour unless users of a published
  release actually experienced the old state.
- **Low-value scaffolding.** No ownerless TODOs, unused future-proofing,
  debug artefacts, or defensive wrappers around failure modes nothing can
  reach.
- **Prose inflation.** The diction table under [Voice](#voice) governs;
  replace an inflated word with a concrete description of behaviour,
  constraints, or trade-offs.
- **Coded labels.** Write rules and findings as plain imperatives. No `[R1]`,
  `Option B`, or any index a reader has to decode.

Preserve the "why". Never delete a comment documenting an invariant, a
protocol constraint, a platform quirk, or an upstream workaround — those are
the facts [Source comments](#source-comments) keeps, and every other comment
is judged by it.

### Durable source links

Link to a pinned revision, never to trunk, when citing this repo's own code as
evidence. Prefer a release tag (`blob/v0.34.0/…`); otherwise a 7-char commit
ref reachable from trunk (`blob/9a29b1a/…`), never a PR-head SHA. Reserve
`blob/master/…` for living documents meant to always show the latest state,
such as this file or the contributing guide. Line anchors (`#L120-L145`) are
only safe on a pinned ref.
