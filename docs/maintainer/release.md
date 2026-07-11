# Release

cifkit is built and maintained with
[scikit-package](https://scikit-package.github.io/scikit-package/),
which drives the release automation. The short version for maintainers:

## Every pull request carries a news file

Copy `news/TEMPLATE.rst` to `news/<branch-name>.rst` and fill in only
the section that applies (`Added`, `Changed`, `Deprecated`, `Removed`,
`Fixed`, `Security`), leaving the other placeholders untouched. CI
enforces the news file's presence. At release time the news fragments
are compiled into `CHANGELOG.rst`, which the [Changelog](../changelog)
page includes directly.

## Cutting a release

Releases follow the scikit-package release workflow: push an annotated
version tag (e.g. `1.2.1`) and the release GitHub Actions workflow
builds the wheel with `setuptools-git-versioning`, uploads to PyPI,
compiles the news fragments into `CHANGELOG.rst`, and creates the
GitHub release.

See the scikit-package
[release documentation](https://scikit-package.github.io/scikit-package/release-guide.html)
for the full checklist.

## Docs deployment

Canonical docs (also PyPI **Homepage** / **Documentation**):

**https://bobleesj.github.io/cifkit/**

LLM plain-text recipes: **https://bobleesj.github.io/cifkit/llms.txt**

This site builds from `docs/` with `jupyter-book` via
`.github/workflows/cifkit-docs.yml` on every push to `main` (and on PRs
for build-only). The workflow runs `scripts/docs_e2e_check.py`, then
publishes HTML to the **`gh-pages`** branch
(`peaceiris/actions-gh-pages`), which is the Pages source for
https://bobleesj.github.io/cifkit/ . `pyproject.toml` Homepage /
Documentation URLs point at that site so PyPI and LLMs land on the
Jupyter Book.

To build locally:

```bash
pip install -r docs/requirements.txt
pip install -e .
jupyter-book build docs
# docs/_build/html/index.html
# docs/_build/html/llms.txt  (and _static/llms.txt)
```

Tutorial pages are plain MyST with pasted, verified outputs — nothing
executes at build time. When behavior changes, re-run snippets against
the package and update the shown outputs in the same commit.
