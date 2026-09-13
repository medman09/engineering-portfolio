# Portfolio Update Workflow

This document defines how real engineering work is promoted into the public `engineering-portfolio` repository without exposing confidential or misleading material.

## 1. Two-stage model

Never move directly from internal development to public portfolio.

Use:

```text
REAL ENGINEERING WORK
        |
        v
INTERNAL ACHIEVEMENT RECORD
        |
        v
CONFIDENTIALITY / ATTRIBUTION REVIEW
        |
        v
SANITIZED CASE STUDY
        |
        v
PUBLIC PORTFOLIO
```

## 2. Create an achievement record

For significant work, create a private record using `ENGINEERING_ACHIEVEMENT_TEMPLATE.md`.

The record is not marketing material. It should capture what actually happened while the evidence is still fresh.

Record:

- problem
- context
- constraints
- personal responsibility
- architecture/technical decisions
- implementation contribution
- verification
- measurable result
- evidence references
- competencies demonstrated
- confidentiality level

## 3. Portfolio candidacy criteria

A task is a good candidate when it demonstrates at least one meaningful engineering capability such as:

- system architecture
- hardware/software integration
- requirements engineering
- interface definition
- verification and validation
- reproducibility/configuration management
- simulation/replay
- complex troubleshooting
- performance engineering
- safety/degraded behavior
- technical leadership
- engineering-process improvement

Routine maintenance and low-complexity fixes usually remain internal evidence only.

## 4. Attribution review

Before publishing, verify:

- the claimed responsibility is accurate
- AI assistance is represented honestly
- upstream/vendor work is not presented as original work
- team/partner contributions are not appropriated
- results can be technically defended

Use wording that distinguishes:

- designed
- integrated
- implemented
- adapted
- validated
- contributed to
- led
- supported

## 5. Confidentiality review

Do not publish:

- credentials or secrets
- private network information
- proprietary CAN/communication mappings
- unreleased partner architectures
- confidential measurements
- internal datasets
- customer/partner-sensitive test results
- safety-sensitive operational details
- private source code without authorization

When the engineering lesson is valuable but the implementation is private, create a synthetic public example or generalized architecture.

## 6. Public case-study structure

Recommended structure:

```text
# Project title

## Engineering problem
## System context
## Constraints
## My responsibility
## Architecture / interfaces
## Engineering decisions
## Implementation approach
## Verification and validation
## Result
## What this demonstrates
## Confidentiality / scope note
```

The public case study should focus on engineering reasoning and evidence rather than exposing internal source code.

## 7. Updating an existing case study

Prefer improving an existing project page when the new work belongs to the same engineering story.

Create a new project page only when:

- the system/problem is materially different
- it demonstrates a different engineering capability
- merging it into an existing case study would make the story unclear

## 8. Evidence linkage

Internal evidence can include:

- issue/PR
- commit SHA
- experiment ID
- RUN/SIM-RUN ID
- test report
- release/baseline ID
- architecture decision
- validation note

Public pages should not link to private evidence if doing so exposes metadata that should remain private.

## 9. Portfolio review cadence

Review achievement candidates:

- after a major validated milestone
- after a baseline/release
- after a substantial architecture decision
- before CV/job-application updates

Do not update the portfolio for every commit.

## 10. Final publication check

Before merging public portfolio content:

- [ ] claim is accurate
- [ ] personal contribution is clear
- [ ] evidence exists
- [ ] confidential details removed
- [ ] AI use represented honestly where relevant
- [ ] no vendor/upstream code presented as original
- [ ] case study explains engineering reasoning
- [ ] result is measurable or clearly bounded
