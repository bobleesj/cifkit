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
GitHub release. The conda-forge feedstock bot then opens the version
bump PR against
[conda-forge/cifkit-feedstock](https://github.com/conda-forge/cifkit-feedstock).

See the scikit-package
[release documentation](https://scikit-package.github.io/scikit-package/release-guide.html)
for the full checklist.

## Docs deployment

This site builds from `docs/` with `jupyter-book` via
`.github/workflows/cifkit-docs.yml` on every push to `main` that
touches `docs/**`, and deploys to GitHub Pages through
`actions/deploy-pages`. To build locally:

```bash
pip install -r docs/requirements.txt
pip install -e .
jupyter-book build docs
open docs/_build/html/index.html
```

The tutorial pages are plain MyST markdown with pasted, verified
outputs - nothing executes at build time. When behavior changes,
re-run the tutorial snippets against the released package and update
the shown outputs in the same commit.
