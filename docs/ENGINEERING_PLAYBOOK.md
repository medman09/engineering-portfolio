# Engineering Playbook

**Version:** 1.0  
**Purpose:** lightweight operating system for systems engineering, software/hardware integration, experimentation, V&V, release management, and portfolio evidence.

## 1. Purpose

This playbook defines how engineering work should be structured so that implementation, architecture, verification, configuration, and professional evidence remain connected.

It is intentionally lightweight. It must improve technical quality and reproducibility without turning small changes into documentation exercises.

The governing principle is:

> Every significant engineering activity should produce both a technical result and, when relevant, a systems-engineering result.

## 2. Core principles

1. **System before component.** Understand the role of a change in the complete system.
2. **Evidence before confidence.** A result is accepted through verification, not intuition.
3. **Traceability proportional to impact.** High-impact changes require stronger traces than low-risk local changes.
4. **Git as source of truth.** Versionable engineering knowledge must survive outside chats and personal notes.
5. **Reproducibility.** Important experiments, releases, and baselines must be reconstructible.
6. **Explicit interfaces.** Hidden assumptions between components are technical debt.
7. **Small reviewable changes.** Prefer bounded changes with clear acceptance criteria.
8. **Document decisions, not activity.** Record why something matters and what was decided.
9. **Separate fact from assumption.** Unknowns must remain visible.
10. **Confidentiality by design.** Public portfolio material must be intentionally sanitized.

## 3. Work classification

Before implementation, classify the task.

| Type | Typical examples | Minimum expected output |
|---|---|---|
| Trivial | typo, formatting, non-functional cleanup | change only |
| Local bug | bounded logic fix | fix + focused test |
| Refactor | internal structure without intended behavior change | regression evidence |
| Configuration | parameter, launch, network, calibration selection | versioned config + rationale + validation |
| Feature | new behavior/capability | acceptance criteria + tests + affected docs |
| Interface | ROS topic/service, CAN contract, API, file format | interface update + compatibility analysis + tests |
| Experiment | algorithm/parameter/hardware evaluation | experiment record + metrics + verdict |
| Architecture | subsystem boundary, deployment, technology selection | ADR/trade study + architecture update |
| Infrastructure | build, CI, deployment, backup, tooling | reproducibility + rollback/validation |
| Safety/ODD | failure response, operational constraint | requirement/state/risk impact + verification |
| Release/Baseline | deployable validated system state | manifest + versions + evidence |

The classification can change during the work if the true impact becomes larger.

## 4. Standard engineering lifecycle

For significant work, use this sequence:

```text
Problem / Need
      |
      v
Context + Constraints
      |
      v
Impact Analysis
      |
      v
Requirement / Acceptance Criteria
      |
      v
Architecture / Design Decision
      |
      v
Implementation / Configuration
      |
      v
Verification
      |
      v
Evidence
      |
      v
Decision
      |
      v
Baseline / Release / Portfolio Candidate
```

Not every task requires every artifact. The sequence is a reasoning model, not a mandatory document list.

## 5. Change impact analysis

Before editing, ask:

### System
- What capability is affected?
- Is nominal behavior changed?
- Are degraded/failure modes affected?
- Is the Operational Design Domain affected?

### Interfaces
- Are topics, services, CAN frames, APIs, file formats, timing contracts, or physical connections changed?
- Are downstream consumers affected?

### Configuration
- Which parameters/calibrations/maps/network settings are involved?
- Where is the authoritative value stored?

### Deployment
- Which machine, ECU, controller, container, workspace, or vehicle is affected?
- Does the change alter build or deployment order?

### Verification
- How can the change be proven correct?
- Can it be tested offline?
- Is bench or vehicle validation required?

### Reproducibility
- Can another engineer reproduce the result from Git + documented external assets?

### Documentation
- Which existing document becomes incorrect if it is not updated?

## 6. Documentation trigger matrix

| Change | Requirement | Architecture | ADR / trade study | Interface doc | Verification evidence | Portfolio candidate |
|---|---:|---:|---:|---:|---:|---:|
| typo / cleanup | no | no | no | no | optional | no |
| local bug | if linked | usually no | no | if affected | yes | rarely |
| refactor | no new req | no intended change | rarely | if affected | yes | rarely |
| parameter tuning | if KPI-driven | usually no | no | no | yes | sometimes |
| new sensor | yes | yes | often | yes | yes | yes |
| new protocol/interface | yes | yes | often | yes | yes | yes |
| algorithm replacement | yes | yes | yes/trade study | likely | yes | yes |
| degraded mode | yes | yes | often | likely | yes | yes |
| release/baseline | trace links | reference | no unless decision | if changed | yes | sometimes |

Use this table as a decision aid, not as a compliance checklist.

## 7. Requirements

Requirements should be:

- necessary
- unambiguous
- feasible
- implementation-independent when possible
- measurable/verifiable
- uniquely identifiable

Example:

Bad:

> Localization should be stable.

Better:

> SYS-LOC-001 — During operation in ODD-LOC-01, the localization subsystem shall maintain lateral position error below the defined threshold for the validated route dataset.

The threshold and verification method belong in the requirement or an associated verification specification.

Recommended IDs:

```text
SN-xxx       Stakeholder need
SYS-xxx      System requirement
SW-xxx       Software requirement
HW-xxx       Hardware requirement
IF-xxx       Interface requirement
SAF-xxx      Safety/degraded-mode requirement
```

Avoid inventing thresholds without measured or agreed engineering justification.

## 8. Architecture

Use architecture only at the level needed to make boundaries and decisions explicit.

Recommended views:

1. **System context** — actors, external systems, system boundary.
2. **Functional architecture** — what the system must do.
3. **Logical architecture** — logical components and responsibilities.
4. **Deployment architecture** — which component runs where.
5. **Interfaces/data flow** — information, control, timing, and dependencies.

Markdown + Mermaid + YAML are sufficient until the project clearly needs heavier MBSE tooling.

Architecture documents should answer questions, not merely contain diagrams.

## 9. Interfaces

For important interfaces record, as applicable:

- producer / consumer
- protocol
- direction
- message/topic/service/frame
- units
- coordinate frame
- update rate
- timestamp source
- timeout
- valid ranges
- error behavior
- startup assumptions
- version/compatibility
- owner

Timing and timestamp semantics are part of the interface.

## 10. ADR and trade studies

Create an Architecture Decision Record when a decision:

- has long-term consequences
- affects multiple components
- is expensive to reverse
- selects between plausible alternatives
- introduces a new dependency or technology
- changes deployment architecture
- changes data ownership or interfaces

An ADR should contain:

```text
Context
Decision
Alternatives considered
Trade-offs
Consequences
Verification / follow-up
Status
```

Do not create ADRs for obvious local implementation details.

## 11. Experiments

Use an experiment when the answer is unknown and must be measured.

Recommended identity:

```text
EXP-<domain>-<topic>-NNN
SIM-RUN-NNN
RUN-NNN
DATASET-NNN
```

An experiment record should include:

- objective
- question/hypothesis
- requirements/KPIs being evaluated
- controlled variables
- input dataset
- hardware/software configuration
- Git SHA(s)
- parameters
- timing assumptions
- procedure
- metrics
- acceptance criteria
- anomalies
- result
- decision
- follow-up

Do not change acceptance criteria after seeing the result without explicitly recording why.

## 12. Evidence chain

The target trace is:

```text
Need
  -> Requirement
  -> Architecture allocation
  -> Test / Experiment
  -> RUN / SIM-RUN
  -> Metrics
  -> PASS / FAIL
  -> Evidence
  -> Decision
```

A RUN manifest can serve as the technical evidence carrier.

Suggested fields:

```yaml
run_id:
experiment_id:
timestamp:
system_version:
git_shas:
configuration:
map:
calibration:
dataset:
hardware:
requirements:
test_case:
metrics:
anomalies:
results:
verdict:
operator:
notes:
```

For automated systems, include enough information to reconstruct the software and configuration state.

## 13. Configuration management

Keep these concepts separate:

```text
CODE
CONFIG
CALIBRATION
DATASET
EXPERIMENT
VARIANT
BASELINE
RELEASE / BUNDLE
```

A **variant** is a controlled alternative.

A **baseline** is an accepted system state.

A **release/bundle** is a deployable representation of a baseline.

A baseline should identify:

- source revisions
- dependencies
- configuration
- calibration
- maps/data references
- deployment instructions
- hardware compatibility
- validation evidence
- known limitations

Do not rely on undocumented files living only on a vehicle PC.

## 14. Verification and validation

Use the cheapest valid verification level first:

```text
static checks
-> unit/component tests
-> integration tests
-> simulator/fake device
-> replay
-> bench
-> controlled target hardware
-> vehicle/system validation
```

The goal is not to avoid physical validation; it is to reserve it for what truly requires physical validation.

For each important test record:

- purpose
- input
- expected result
- measured result
- PASS/FAIL criterion
- evidence location

## 15. Failure and degraded behavior

For autonomous/robotic systems, important failures must be treated as system behavior.

Pattern:

```text
Fault
-> Detection
-> Diagnosis / confidence
-> System response
-> Degraded or minimal-risk state
-> Recovery condition
-> Verification
```

Examples may include:

- localization divergence
- sensor loss
- compute-node communication loss
- planning/control unavailable
- CAN timeout
- map invalidity
- timing/synchronization failure

Do not assume a component failure is handled merely because the nominal component restarts.

## 16. Git workflow

For significant changes:

1. create issue/change objective when useful
2. create bounded branch
3. define acceptance criteria
4. inspect existing implementation
5. implement smallest coherent change
6. add/adjust tests
7. run verification
8. update affected docs
9. review the diff
10. create PR with evidence
11. resolve findings
12. merge
13. tag/baseline when applicable

Commit messages should explain intent.

Pull Requests should capture:

- problem
- scope
- system impact
- verification
- evidence
- documentation updates
- risks/limitations
- rollback considerations when relevant

## 17. Definition of Done

A significant engineering change is done when:

- intended behavior is implemented
- acceptance criteria are evaluated
- relevant tests pass
- system/interface impact is understood
- configuration is versioned
- affected documentation is updated
- known limitations are explicit
- required evidence is preserved
- no confidential information is unintentionally exposed
- the change is reviewable and reproducible

A change is not done merely because it compiles or runs once.

## 18. Portfolio evidence

Do not publish raw internal work automatically.

First create an internal achievement record.

Then classify it:

```text
NOT PORTFOLIO MATERIAL
INTERNAL ONLY
PUBLIC AFTER SANITIZATION
PUBLIC NOW
```

Strong case-study structure:

```text
Problem
Context / constraints
Responsibility
Architecture / interfaces
Engineering decisions
Implementation strategy
Verification
Result
Lessons / competencies
```

Remove or generalize:

- proprietary mappings
- credentials
- private addresses
- partner-sensitive measurements
- unreleased architecture
- confidential datasets
- safety-sensitive operational details
- copied vendor/upstream code

The portfolio should demonstrate engineering ownership, not expose employer intellectual property.

## 19. Review questions

Before accepting an important change, ask:

- What evidence proves this?
- Which assumption is still unverified?
- What breaks if this component is unavailable?
- Is the interface explicit?
- Can this state be reproduced?
- Is the configuration under version control?
- Is there a rollback/recovery path?
- Does the documentation still describe reality?
- Does the portfolio claim only what can be defended?

## 20. Anti-patterns

Avoid:

- documentation written after the fact only to look professional
- requirements that cannot be tested
- diagrams with no ownership or purpose
- tuning without a repeatable dataset
- manual vehicle-PC edits without traceability
- accepting AI-generated code because it looks plausible
- mixing source, build output, datasets, and release artifacts
- publishing internal project details as portfolio content
- creating a new framework when an existing project convention is sufficient

## 21. Principle of proportionality

This playbook is successful only if it improves engineering decisions.

Use the lightest artifact that preserves:

- clarity
- traceability
- reproducibility
- verification
- maintainability

When in doubt, document the decision and evidence, not every action.
