# AI Cost Watch — interactive tool

An interactive front-end over the *AI Cost Watch* series: a recurring, dated note on the unit economics of the AI buildout, tracking whether its cost and demand assumptions are holding. Each issue states a falsifiable forward call.

**Live:** https://nmairesearch.github.io/cost-watch/
**Series concept DOI (always the latest issue):** [10.5281/zenodo.20541643](https://doi.org/10.5281/zenodo.20541643)

## What it does

Two views over the same frozen dataset:

- **By edition** — pick an issue and read its signal status, the month's developments, the net read, and the indicators it flagged to watch next. Each edition links to its own citable Zenodo record.
- **By indicator across editions** — pick a tracked indicator (the core capex-guidance signal, the frontier-to-floor price spread, capex intensity, the token-expenditure index, PJM announced-vs-delivered power, and others) and see how it moved issue to issue.

The spine of the series is one signal: a down-revision in the Big Four's forward capital-expenditure guidance. It has not fired in any issue to date. The tool makes that monitoring log legible at a glance.

## Files

- `costwatch.json` — the frozen dataset: issues (status, developments, net read, watch list) and the tracked indicators with their per-issue readings.
- `build.py` — regenerates `index.html` from `costwatch.json` (standard library only, no dependencies).
- `index.html` — the self-contained, dependency-free page (data embedded verbatim).

## Reproduce / update

```
python3 build.py
```

To add the next issue: append one object to `"issues"` in `costwatch.json`, add any new `"readings"` to the indicators, and re-run `build.py`. Nothing else changes. Issue 6 follows the late-July Q2 reports.

## Notes

Every figure is sourced in the linked paper and stated at its true tier: vendor claims are labelled by the seller's business model, not treated as findings. Conflict of interest: the series is produced with assistance from an Anthropic model, and Anthropic is among the companies it tracks, so any reading that touches Anthropic is non-neutral and primary or vendor-independent sources are preferred. Independent analysis, not investment advice. CC BY 4.0.
