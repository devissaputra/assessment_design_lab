# Data Documentation

## Included data

`sample.csv` contains a small synthetic binary response matrix used for demonstrations and tests. It contains no real learner records.

## Current schema

- `respondent_id`: synthetic row identifier
- `item_1` ... `item_4`: binary item scores where 1 = correct and 0 = incorrect
- `total`: simple sum of the four item scores for readability

The analysis code recomputes the statistics from the item responses. The `total` column is not treated as authoritative input.

## Current assumptions

The implemented item-analysis path assumes:

- dichotomously scored items
- one response row per respondent
- no missing responses in the current baseline
- all items are intended to contribute to the same assessment-level analysis

Cronbach alpha accepts finite numeric item scores, but `analyze_assessment()` deliberately requires binary 0/1 data because its difficulty and discrimination functions are defined for binary items.

## Discrimination criterion

Item discrimination is calculated using **rest scores**: each respondent's total score excluding the focal item. This avoids the direct part-whole inflation that occurs when the item is included in its own grouping criterion.

Upper and lower groups are created from criterion scores only. Ties at the group boundary are retained. If ties make the extreme groups overlap, discrimination is reported as not estimable rather than breaking the tie using the focal response.

## Future item metadata

A real study should store item metadata separately, for example:

- item ID
- content domain or learning outcome
- item format
- keyed answer
- distractor options
- cognitive demand
- administration conditions
- item revision history

Distractor analysis is **not** implemented in the current version.

## Missing responses

The current baseline rejects missing or non-finite values. A future version should define a documented missing-data policy before calculating item statistics.

## Do not commit

Do not commit identifiable student records, secure test content, unreleased examination items, private LMS exports, answer keys that must remain confidential, or licensed assessment data that cannot be redistributed.

## Dataset card requirement

For empirical work, document the assessment purpose, population, administration conditions, scoring rules, sample size, exclusions, missing-response handling, item revisions, security constraints, consent or lawful basis, and permitted uses.
