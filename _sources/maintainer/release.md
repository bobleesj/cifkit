# Changelog and release

This page is the single maintainer entry for **what shipped** and **how to
cut a release**. cifkit follows
[scikit-package](https://scikit-package.github.io/scikit-package/) for
news fragments, tagging, and PyPI upload.

## Every pull request carries a news file

Copy `news/TEMPLATE.rst` to `news/<branch-name>.rst` and fill in only the
section that applies (`Added`, `Changed`, `Deprecated`, `Removed`,
`Fixed`, `Security`), leaving the other placeholders untouched. CI
enforces the news file's presence.

At release time those fragments are compiled into `CHANGELOG.rst` (the
history below).

## Cutting a release

1. Ensure main is green and news fragments for the release are present.
2. Push an annotated version tag (e.g. `1.2.3`).
3. The release GitHub Actions workflow builds the wheel with
   `setuptools-git-versioning`, uploads to PyPI, compiles news fragments
   into `CHANGELOG.rst`, and creates the GitHub release.

Full checklist:
[scikit-package release guide](https://scikit-package.github.io/scikit-package/release-guide.html).

## Docs deployment

Canonical docs (also PyPI **Homepage** / **Documentation**):

**https://bobleesj.github.io/cifkit/**

LLM plain-text recipes: **https://bobleesj.github.io/cifkit/llms.txt**

This site builds from `docs/` with `jupyter-book` via
`.github/workflows/cifkit-docs.yml` on every push to `main` (and on PRs
for build-only). The workflow runs `scripts/docs_e2e_check.py`, then
publishes HTML to the **`gh-pages`** branch
(`peaceiris/actions-gh-pages`).

To build locally:

```bash
pip install -r docs/requirements.txt
pip install -e .
jupyter-book build docs
# docs/_build/html/index.html
```

Tutorial pages are plain MyST with pasted, verified outputs - nothing
executes at build time. When behavior changes, re-run snippets against
the package and update the shown outputs in the same commit.

## Release notes (changelog)

Compiled history from `CHANGELOG.rst` (news fragments + past releases):

```{eval-rst}
.. include:: ../../CHANGELOG.rst
```
