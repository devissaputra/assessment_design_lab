# Analytic system card

## System

Assessment Design Lab

## Purpose

Transparent assessment analytics for item difficulty, discrimination, reliability, and evidence based item review.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces item difficulty, item discrimination, and internal consistency estimates. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Use a sufficiently large response matrix, report uncertainty around item statistics, and compare flagged items with an independent expert review. Reliability should be interpreted in the context of the assessment design.

## Main limitation

These statistics do not establish content validity, fairness, or instructional alignment on their own. The bundled matrix is synthetic and only demonstrates the calculations.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
