# AGENTS.md

This file is the working contract for coding agents in FEMIC GNN Instance.

Prototype FEMIC/ws4 model for the proposed Gwa'sala-'Nakwaxda'xw Nations Statement of Intent area.

Keep this file short. Each rule below either checks itself or points to the page that explains it.
The workflow rules come from the UBC-FRESH dev workflow, which this project was seeded from. Project-
specific rules go at the end, each with its reason.

## Session start

Before you change anything, read in this order:

1. This file.
2. `ROADMAP.md`: the active phase and its "Detailed Next Steps Notes".
3. The latest entries in `CHANGE_LOG.md`.
4. The notes your task names, in `notes/`.
5. The docs pages that govern your task, in `docs/`.

Cite the pages you relied on in your report.

## Working principles

- **Evidence over trust.** Cite command output, diffs, commit hashes, and URLs.
- **One bounded move at a time.** Stop and report after each one.
- **No oracle, no capability.** A new agent-facing capability needs a validator that can fail.
- **Workflow as scaffold.** Create the parent issue, the branch, and the roadmap entry before the work.
- **Structured handoff.** Issues, the roadmap, notes, and the changelog carry the state.
- **Preserve uncertainty.** Say what you did not verify, and why.
- **Scope discipline.** Stay inside the active phase and task.
- **Sanitized output.** Keep private data, credentials, raw transcripts, and personal paths out of
  tracked files.

## The green dashboard rule

`python scripts/dashboard.py` runs every quality gate: lint, format, strict types, tests with a coverage
gate, the workflow validator, and the docs build with warnings as errors.

- Every commit leaves the dashboard green.
- Any change from green is investigated and fixed immediately. There are no exceptions.
- A failure you did not cause is still yours to fix, or to report with evidence before you continue.
- Do not weaken a gate to make it pass. A gate changes only with a changelog entry that explains why.
- Record the dashboard result in the changelog entry for each task that you close.

## Typing and docstrings

- Every function, method, and test has complete type annotations. `mypy --strict` must pass.
- Every public function has a numpy-style docstring. Its parameters and return value match its annotations.
- Do not use `Any`, `# type: ignore`, or `cast` without a comment that says why. A suppression names its error code.

## Testing policy

- Every function you write or change gets unit tests in the same change set. Tests must be able to
  fail, and each one asserts a specific behavior.
- Keep the layers: unit tests for each function, contract tests for public interfaces, integration
  tests for the command-line tools, property tests for invariants, and the self-check.
- The coverage gate is 95 percent branch coverage of `scripts/`. Aim near 100 percent, with tests that
  assert something.

## Embedded agent capabilities

If this project ships complicated software, it may offer agents validated capabilities instead of
documentation alone. A capability is a prompt, a validator over real state, and a bounded retry
budget. No oracle, no capability. Each capability needs offline tests with a fake provider, and it
must say what its validator checks and what it does not.

## CI and merges

- CI runs every gate on every pull request, and on every push to `main`.
- No pull request merges while CI is red.
- A merge happens only as part of an approved phase close-out. Queue the pull request, write the report in `notes/reports/`, and wait for the maintainer's approval.

## Planning workflow

- One phase is one GitHub parent issue and one feature branch, `feature/p<n>-<slug>`.
- One task is one child issue, linked to the parent as a sub-issue.
- A subtask is a checklist item in the child issue body. Three levels at most.
- Keep `ROADMAP.md`, `CHANGE_LOG.md`, `notes/`, issue bodies, and PR descriptions in step.

## Approval gates

You may, within the active phase: create and commit to its branch, push that branch, open and update
its issues and pull requests, and run local checks.

After the maintainer approves a phase close-out, carry out what the report recommends: squash-merge the pull request, delete its branch, close the parent issue, and launch the next phase. Name every settings change, tag, release, or external account in the report, with its exact command, and wait for approval of each one.

You must wait for an explicit approval before you: create a tag or a release; change repository visibility, settings, or branch protection; create an external account, repository, or server; touch private data or credentials; or delete anything beyond the branch that an approved report names.

## GitHub hygiene

- Audit read-only first: `gh issue list`, `gh issue view <n>`, `gh pr list`.
- Write bodies and comments to files, and post them with `--body-file`. Never build them from escaped strings.
- Read back every comment or edit with `gh issue view` before you report it as posted.
- Post a progress comment when a task or phase milestone completes, and a closeout comment before you close an issue.

## Formatting

- Put section labels on their own lines, such as `Phase identifier: P0`.
- Use real task-list syntax, one item per line.
- Wrap branch names, paths, commands, and commit hashes in backticks.
- Start commit messages with the task ID, for example `P0.1 add license`.

## Verification

Run the dashboard before you report a change as done:

```bash
python scripts/dashboard.py
```

Record the result in the changelog entry for the milestone.

## Public safety

- No private data, credentials, raw transcripts, unpublished documents, or machine-specific paths in
  tracked files.
- Use placeholders, repository-relative paths, or environment variables in examples.

## Project-specific rules

- **Proposed boundary, not legal title.** The AOI is the BCGW proposed GNN Statement of Intent polygon. Label it that way in every public surface. Confirm the boundary and public-output plan with GNN before release. Reason: the SOI map is under review and is not a treaty or title determination.
- **Derived THLB and AAC.** The THLB and annual AAC are derived from the TSA 46/47 base models and are not legal determinations. Keep the derivation and the non-legal label visible. Reason: there is no standalone GNN legal THLB or AAC.
- **Keep TSA-prefixed AUs.** Do not merge TSA 46 and TSA 47 model AUs by nominal stratum and SI. The curves differ materially; a reporting crosswalk is allowed, a model merge is not. Reason: merging would hide curve provenance and productivity differences.
- **No AAC tuning.** Do not adjust curves, density, or management assumptions to make the derived AAC or a decade target fit. Judge the model against ground observations. Reason: the benchmark is derived, and fit to it is not evidence of accuracy.
- **Pipeline is separate.** `scripts/` is workflow tooling and carries the strict lint, type, docstring, and coverage gates. `pipeline/` holds the build and analysis entry points. Reason: data-pipeline scripts are validated by execution and `ws4 validate`; the workflow tooling needs the seed's strict gates.
- **Model artifacts are local.** `runtime/`, `output/`, `data/*.feather`, and model bundles are gitignored. Do not commit model artifacts or raw data. Reason: they are large and reproducible from the documented pipeline.
