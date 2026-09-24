# Analytic system card

## System

Assessment Design Lab

## Purpose

Transparent classical assessment diagnostics for reviewing binary-scored items and assessment-level internal consistency.

## Current maturity

Working research prototype. The bundled response matrix is synthetic and demonstrates the software path only. It does not establish that the default review cutoffs are appropriate for any real assessment.

## Inputs

`analyze_assessment()` expects a rectangular binary response matrix:

- rows = respondents
- columns = items
- values = 0 or 1

`cronbach_alpha()` can accept finite numeric item scores, but the integrated item-analysis workflow is intentionally limited to binary items.

## Outputs

The integrated analysis returns:

- respondent count
- item count
- Cronbach alpha or an explicit not-estimable value
- item difficulty as proportion correct
- item discrimination using upper/lower groups based on rest scores
- per-item review flags
- analysis settings used for the discrimination groups

## Discrimination safeguards

The focal item is excluded from the criterion score used to form the upper and lower groups.

Ties are resolved from criterion scores only. The focal response is never used as a tie-breaker. Boundary ties are retained; if they make the groups overlap, discrimination is reported as not estimable.

## Review flags

Flags identify cases worth inspection, such as very high/low proportions correct, low or negative discrimination, or an unestimable discrimination statistic.

They are not automatic item-deletion rules.

## Evidence needed before real use

Evaluate the diagnostics on a sufficiently large assessment dataset with documented item content and administration conditions. Report uncertainty, sensitivity to group definitions, and agreement/disagreement with independent expert item review.

## Main limitations

This is a classical binary-item baseline. It does not currently model item response theory, multidimensionality, guessing, speededness, distractor functioning, differential item functioning, missing responses, or content validity.

Cronbach alpha is an internal-consistency coefficient, not a general score for assessment quality.

## Human oversight

An assessment expert should inspect the item content, learning intent, scoring, distractors, administration context, and consequences before acting on any statistical flag.
