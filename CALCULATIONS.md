# Calculation guide

## Question and evidence

Which assessment items warrant review?

Synthetic binary response matrices; optional criterion scores.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Calculate proportion correct, rest-score extreme-group discrimination and Cronbach alpha with degeneracy checks.

## Calculation and interpretation

`Alpha = k/(k-1) × (1 - sum(item variances)/variance(total score)).`

Difficulty is proportion correct, so larger values mean easier items. Discrimination uses rest scores to avoid part-whole inflation. Alpha is not dimensionality or validity; zero total variance makes it undefined.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| proportion correct | 0.5 | unitless | `outputs.proportion correct` |
| Cronbach alpha | 0.75 | unitless | `outputs.Cronbach alpha` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This assessment-analysis toolkit computes item difficulty, tie-safe extreme-group discrimination, and internal-consistency diagnostics from synthetic response matrices. Rest scores exclude the focal item when forming comparison groups, and undefined quantities remain explicit when the data cannot support an estimate. The repository explains how to inspect flagged items without treating alpha or a cutoff as proof of assessment validity.

## Verification performed in this review

19 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`item_difficulty`](src/assessment_design_lab/core.py#L59) | Return the proportion correct for a binary-scored item. |
| [`rest_scores`](src/assessment_design_lab/core.py#L66) | Return each respondent's total score excluding the focal item. |
| [`item_discrimination`](src/assessment_design_lab/core.py#L129) | Return upper-minus-lower proportion correct using tie-safe score groups. |
| [`cronbach_alpha`](src/assessment_design_lab/core.py#L161) | Compute Cronbach alpha for a rectangular numeric response matrix. |
| [`item_review_flags`](src/assessment_design_lab/core.py#L188) | Return transparent review prompts using configurable descriptive cutoffs. |
| [`analyze_assessment`](src/assessment_design_lab/core.py#L221) | Analyze a binary response matrix with item-level review signals. |

## What remains before a stronger research claim

Difficulty is proportion correct, so larger values mean easier items. Discrimination uses rest scores to avoid part-whole inflation. Alpha is not dimensionality or validity; zero total variance makes it undefined. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
