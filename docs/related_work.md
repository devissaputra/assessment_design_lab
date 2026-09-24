# Related work and methodological context

Assessment Design Lab is an original implementation of a small classical-test-theory baseline. It is designed for transparency and teaching/research use rather than as a replacement for established psychometric software.

## Classical item analysis

The current baseline focuses on descriptive item statistics commonly used in classical test theory:

- proportion correct for binary-item difficulty
- upper/lower-group item discrimination
- total-score internal consistency

These statistics are useful for review but depend on the sample and assessment context.

## Cronbach alpha

The implementation follows the standard coefficient-alpha formula described in:

Cronbach, L. J. (1951). *Coefficient alpha and the internal structure of tests*. Psychometrika, 16, 297–334. https://doi.org/10.1007/BF02310555

Alpha should not be interpreted as proof of unidimensionality, validity, or overall assessment quality.

A practical discussion of common interpretation mistakes is:

Tavakol, M., & Dennick, R. (2011). *Making sense of Cronbach's alpha*. International Journal of Medical Education, 2, 53–55. https://doi.org/10.5116/ijme.4dfb.8dfd

## Rest-score discrimination

The repository forms extreme groups from each respondent's score on the **other items**, excluding the focal item. This avoids using the item as part of its own grouping criterion.

The implementation also preserves score ties rather than breaking them using the focal response.

## Established software context

Mature psychometric ecosystems provide substantially more capability than this repository, including item response theory, factor models, reliability alternatives, and differential item functioning. Examples include:

- R `psych`: https://cran.r-project.org/package=psych
- R `mirt`: https://cran.r-project.org/package=mirt

These are context for future benchmarking and extension. They are not dependencies of this prototype.

## Relationship to this repository

The goal here is not to reproduce a full psychometrics package. The goal is to make a compact assessment-design baseline whose assumptions, edge cases, and review signals are easy to inspect.

A future study should compare the transparent diagnostics with expert item review and, where appropriate, more advanced psychometric models.
