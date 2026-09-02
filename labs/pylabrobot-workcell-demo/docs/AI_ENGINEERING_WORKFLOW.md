# AI-native engineering workflow

Coding agents are intentionally part of this demonstrator. The purpose is not to claim that every implementation line was written manually; the purpose is to demonstrate engineering ownership when AI accelerates implementation.

## Human engineering responsibility

I retain responsibility for:

- defining the problem and acceptance criteria;
- deciding architecture and interface boundaries;
- classifying failure modes and safety/recovery behavior;
- reviewing generated changes and understanding their role;
- deciding what must be tested;
- reproducing and diagnosing failures;
- validating behavior against simulator/framework semantics;
- deciding when a change is acceptable to merge;
- clearly documenting limitations and what has not been validated on physical hardware.

## Appropriate coding-agent tasks

Agents may be used for:

- codebase/documentation exploration;
- implementation within a constrained scope;
- refactoring after characterization tests exist;
- test scaffolding and additional edge cases;
- repetitive typing and documentation synchronization;
- proposing alternative implementations for review.

## Validation rule

Generated code is not considered correct because it is syntactically plausible, builds, or passes a narrow happy-path test.

For each behavior change, evidence should cover the relevant combination of:

1. static review;
2. unit tests;
3. integration tests with simulated devices;
4. error and boundary paths;
5. framework/runtime validation;
6. staged physical validation if real hardware is introduced later.

## Mistake log

A portfolio-ready version of this project should contain at least two concrete examples in this section:

### Example A — pending

- **Agent proposal:**
- **Why it was questionable/wrong:**
- **How I detected it:**
- **Correction:**
- **Evidence after correction:**

### Example B — pending

- **Agent proposal:**
- **Why it was questionable/wrong:**
- **How I detected it:**
- **Correction:**
- **Evidence after correction:**

These examples must come from real development history; they should not be invented for presentation.
