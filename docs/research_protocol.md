# Research protocol

## Project

Assessment Design Lab

## Research questions

1. Which binary-scored items show extreme proportions correct or weak/negative discrimination?
2. How stable are those item diagnostics across samples and administration conditions?
3. What does internal-consistency evidence add to item-level review, and where can it mislead?
4. How well do transparent statistical review flags agree with independent assessment-expert judgments?

## Current baseline

The current implementation uses classical, transparent diagnostics:

- proportion correct for item difficulty
- upper-minus-lower proportion correct for discrimination
- rest scores as the discrimination grouping criterion
- tie-preserving upper/lower groups
- Cronbach alpha for internal consistency
- explicit not-estimable states
- configurable item review flags

The code does not combine these measures into a single item-quality or assessment-quality score.

## Item difficulty

For dichotomously scored items, difficulty is reported as the proportion correct. A high value therefore means more respondents answered correctly. Whether that is desirable depends on the assessment purpose and item role.

## Item discrimination

The current discrimination statistic compares the proportion correct in upper and lower groups defined from **rest scores**. The focal item is excluded from the criterion score.

Group membership is determined from the criterion score only. Boundary ties are retained. If ties cause upper and lower groups to overlap, the statistic is reported as not estimable.

The default group fraction is one third and can be changed by the caller. A real study should justify its grouping choice and inspect sensitivity to alternatives.

## Internal consistency

Cronbach alpha is reported separately from item statistics. It is not treated as evidence that an assessment is valid, unidimensional, fair, or instructionally aligned. If all respondents have the same total score, alpha is reported as not estimable.

## Review flags

The baseline can flag:

- unusually low proportion correct
- unusually high proportion correct
- negative discrimination
- low discrimination
- discrimination not estimable

Default cutoffs are review prompts, not universal psychometric standards. They can be changed for a study.

## Evidence to collect

A credible empirical study should record:

- assessment purpose and stakes
- sample size and population
- item content/domain
- scoring rules
- administration conditions
- missing-response handling
- item revisions
- expert item-review judgments
- uncertainty around item statistics
- subgroup analyses where appropriate and ethically justified

## Validation

Use a response matrix large enough to make item statistics reasonably stable. Compare statistical flags with independent expert review and report where the two disagree.

Sensitivity analyses should vary:

- upper/lower group fraction
- minimum group size
- sample composition
- item exclusion/inclusion
- missing-response policy

## What counts as a useful result

A useful result identifies when transparent classical diagnostics help an assessment designer notice a real design problem, and when they create false confidence or unnecessary flags.

## Threats to validity

Small samples, multidimensional assessments, guessing, speededness, local item dependence, poorly targeted tests, unequal subgroup composition, missing responses, and changes in administration conditions can distort classical item statistics.

Cronbach alpha can also be misinterpreted as a general measure of test quality. It should be interpreted alongside the assessment design and other sources of validity and reliability evidence.
