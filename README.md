# Tacit

Tacit provides writing tools for software engineers. The `prose` plugin uses a
base skill with two optional modifiers:

- **Prose** drafts and edits conservatively under a shared preservation
  contract.
- **Compress** selects the information required for the document's purpose and
  removes optional content.
- **Laconic** changes the register of retained information without removing
  unique content.

When both modifiers are requested, apply Compress first and Laconic second.
The final preservation check compares the result with the source and the
retained semantic inventory. See [Foundations](plugins/prose/FOUNDATIONS.md)
for the full contract and sources.

## Claude Code

```text
/plugin marketplace add dabd/tacit
/plugin install prose@tacit
```

Invoke each operation with its Claude command:

```text
/prose:polish <draft>
/prose:compress <draft or target; optional hard limit>
/prose:laconic <draft>
```

Update the marketplace and plugin, then restart Claude Code:

```bash
claude plugin marketplace update tacit
claude plugin update prose@tacit
```

## Codex

Add the marketplace and install the plugin:

```bash
codex plugin marketplace add dabd/tacit
codex plugin add prose@tacit
```

Invoke each operation with its plugin-qualified Codex skill:

```text
$prose:prose <draft>
$prose:compress <draft or target; optional hard limit>
$prose:laconic <draft>
```

Upgrade the marketplace and reinstall the plugin:

```bash
codex plugin marketplace upgrade tacit
codex plugin add prose@tacit
```

Start a new thread after installing or updating so Codex loads the current
skills.

## Validate

From the repository root:

```bash
python3 -B -m unittest discover -s plugins/prose/tests -v
claude plugin validate .
claude plugin validate ./plugins/prose
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool plugins/prose/.codex-plugin/plugin.json
```

## Versioning

Both plugin manifests use semantic versions. Behavior changes bump both
versions and use `prose--v<version>` release tags.

## License

Tacit is available under the [MIT License](LICENSE).

## Credits

- dabd wrote the MIT-licensed skills.
- Joseph M. Williams and Joseph Bizup's *Style: Lessons in Clarity and Grace*
  informs the structure and concision guidance.
- Verlyn Klinkenborg's *Several Short Sentences About Writing* and the plain
  style of Grant's field orders inform the laconic register. The wording in this
  repository is original.
