# VECD Priority Framework

A structured, governance-ready prioritization framework for teams that need
more than gut feel — and more than a spreadsheet — to make defensible sequencing
decisions at scale.

VECD is a **RICE-inspired adaptation** that replaces Reach and Confidence with
two dimensions better suited to cross-functional and platform-level prioritization:
**Cost of Delay** (urgency) and **Dependency** (autonomy of execution). The result
is a framework that surfaces not just what is valuable, but what is valuable *now*
and what can actually *ship*.

**Platform-agnostic by design.** VECD does not assume a specific methodology,
toolchain, team structure, or delivery model. It works equally well for product
teams, platform teams, data teams, operations, and leadership. Any initiative that
can be described in terms of value, effort, urgency, and blockers can be scored.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Dimensions and Scoring Rubric](#dimensions-and-scoring-rubric)
  - [V — Value](#v--value--20)
  - [E — Effort](#e--effort--10)
  - [C — Cost of Delay](#c--cost-of-delay--5)
  - [D — Dependency](#d--dependency--5)
- [Priority Score and Tiers](#priority-score-and-tiers)
- [Leadership Offset Indicator](#leadership-offset-indicator)
- [Calculator](#calculator)
- [Issue Template](#issue-template)
- [GitLab Labels](#gitlab-labels)
- [Repository Structure](#repository-structure)
- [Design Rationale](#design-rationale)

---

## How It Works

Score an initiative across four dimensions. Add the scores. Look up the tier.

```
Priority Score  =  V  +  E  +  C  +  D
Maximum Score   =  20 + 10  +  5  +  5  =  40
```

The score is additive and integer-only. It is calculated by hand or with the
included CLI tool. No spreadsheet formula, no proprietary tooling, no configuration
required to get started.

| Dimension       | Max | Weight | Higher score means…                        |
|-----------------|-----|--------|--------------------------------------------|
| V — Value       |  20 |   50%  | Greater business or user value             |
| E — Effort      |  10 |   25%  | Lower effort (easier and faster to ship)   |
| C — Cost of Delay|  5 |  12.5% | More urgent — delay is more costly         |
| D — Dependency  |   5 |  12.5% | Fewer upstream blockers                    |

Weights reflect the philosophy that **value is the primary signal**, effort is
the practical constraint, and urgency and autonomy are secondary but meaningful
modifiers that prevent high-value-but-intractable work from clogging the top of
the backlog.

---

## Dimensions and Scoring Rubric

Use the anchors below to assign each score. Interpolate between anchors for
in-between cases. Every score must be accompanied by a written justification
in the issue template — unjustified scores will be returned for revision.

---

### V — Value `/ 20`

**What it measures:** The strategic, business, or user value delivered if this
initiative ships. This is the highest-weighted dimension. Score it relative to
the team or organization's current stated goals, OKRs, or KPIs — not against
an abstract ideal.

| Score  | Anchor                                                                                     |
|--------|--------------------------------------------------------------------------------------------|
| 18–20  | Transformative. Core to company strategy, a flagship OKR, or significant revenue impact.  |
| 14–17  | High value. Directly advances a key goal; meaningful impact on a large segment.            |
|  9–13  | Moderate value. Improves experience or efficiency for a notable group or metric.           |
|  4–8   | Low value. Marginal improvement; addresses a small or infrequent pain point.               |
|  0–3   | Negligible. Nice-to-have with no clear business or user outcome.                           |

**Scoring guidance:**
- Tie to a specific OKR, KPI, or user research finding wherever possible.
- Consider both *reach* (how many users or systems are affected) and *impact*
  (by how much does the outcome change).
- Resist the temptation to inflate Value because the work feels important.
  The rubric must be applied consistently for the tier system to be meaningful.
- Do not conflate effort with value. A two-hour change can be a 20/20.

---

### E — Effort `/ 10`

**What it measures:** The *ease* of delivery — a higher score means *lower* effort.
Factor in engineering complexity, cross-team coordination requirements, testing
burden, operational overhead, and uncertainty. Effort acts as a natural moderator:
high-effort work must justify its place at the top of the backlog with commensurately
high value or urgency.

| Score | Anchor                                                                                      |
|-------|---------------------------------------------------------------------------------------------|
|  9–10 | Trivial. Hours of work, single contributor, no coordination required.                       |
|  7–8  | Small. 1–3 days, single team, well-understood scope, low uncertainty.                       |
|  5–6  | Medium. 1–2 weeks, possible cross-team dependencies, some design decisions open.            |
|  2–4  | Large. 2–6 weeks, multiple teams, significant architecture or infrastructure work.          |
|  0–1  | Extra-large. Months of work, high uncertainty, requires discovery or a dedicated spike.     |

**Scoring guidance:**
- Add 1–2 points of uncertainty margin if a spike or discovery phase is needed
  before the work can be properly scoped.
- Factor in the *total* delivery cost: implementation, testing, documentation,
  code review, deployment, and operational on-call burden.
- If the work requires sign-off or approval from a party outside the team,
  treat that as a coordination cost and score accordingly.

---

### C — Cost of Delay `/ 5`

**What it measures:** The cost or harm incurred by deferring this initiative.
Framed as: *what is lost or risked if delivery slips by 4 weeks? By 3 months?*
Regulatory deadlines, contractual commitments, and competitive windows all
factor in.

| Score | Anchor                                                                                      |
|-------|---------------------------------------------------------------------------------------------|
|   5   | Critical urgency. Immediate financial, legal, reputational, or contractual consequence.     |
|   4   | High urgency. A hard deadline exists; missing it causes meaningful penalty or setback.      |
|   3   | Moderate urgency. A time-sensitive opportunity; delay causes notable opportunity cost.      |
|   2   | Low urgency. Some incremental value loss over time, but no hard deadline or pressure.       |
|  0–1  | No urgency. Can be deferred indefinitely with negligible consequence.                       |

**Scoring guidance:**
- Apply the "4-week test" explicitly: state what happens if this slips one month,
  then three months. The answer should drive the score.
- Urgency that exists because of poor planning or self-imposed deadlines should
  not automatically score high. External accountability (contracts, audits,
  customer commitments) is a stronger signal.
- SLA breach risk, active security vulnerability, and regulatory non-compliance
  are strong indicators for a score of 4 or 5.

---

### D — Dependency `/ 5`

**What it measures:** The *dependency burden* on this initiative — **fewer
dependencies yields a higher score**. An initiative that can start and ship
independently scores 5. An initiative entangled in upstream blockers, unresolved
decisions, or third-party timelines scores 0 or 1.

This dimension reflects execution risk: a high-value initiative that cannot
move without waiting on three other teams is not a true top-of-backlog item
until those blockers resolve.

| Score | Anchor                                                                                      |
|-------|---------------------------------------------------------------------------------------------|
|   5   | Fully independent. No upstream blockers; can start and ship without waiting on anyone.      |
|   4   | Mostly independent. One minor dependency with a clear owner and near-term resolution.       |
|   3   | Moderate. 2–3 dependencies; some have workarounds, but meaningful progress requires them.  |
|   2   | Heavily dependent. Multiple blockers; meaningful risk of delay from other teams.            |
|  0–1  | Highly entangled. Blocked by unresolved decisions, external parties, or many other teams.   |

**Scoring guidance:**
- Identify *concrete* upstream dependencies, not hypothetical future ones.
  "We might need the data team" is not the same as "the data team must deliver
  a schema change before we can begin."
- Distinguish hard blocks (cannot proceed at all) from soft blocks (a workaround
  exists, even if suboptimal). A soft dependency is worth 1–2 fewer points than
  a hard block.
- Include both technical dependencies (APIs, infrastructure, data pipelines) and
  process dependencies (approvals, compliance reviews, architectural decisions).

---

## Priority Score and Tiers

Sum the four dimension scores. The maximum possible score is **40**.

```
Priority Score  =  V  +  E  +  C  +  D
```

Map the score to a tier:

| Tier         | Score Range | Meaning                                    | GitLab Label         |
|--------------|-------------|--------------------------------------------|----------------------|
| **Critical** |    35–40    | Immediate action required                  | `priority::critical` |
| **High**     |    25–34    | Schedule in current or next cycle          | `priority::high`     |
| **Medium**   |    15–24    | Backlog — plan within 1–2 quarters         | `priority::medium`   |
| **Low**      |     0–14    | Defer, revisit at roadmap review, or close | `priority::low`      |

### Worked Example

| Dimension       | Score | Reasoning                                                   |
|-----------------|-------|-------------------------------------------------------------|
| V — Value       |  16   | Unblocks a partner integration tied to a Q3 revenue OKR     |
| E — Effort      |   7   | ~3 days, single team, well-understood scope                  |
| C — Cost of Delay|  4   | Partner launch committed for next month; delay risks penalty |
| D — Dependency  |   3   | Requires a schema change from the data team (in progress)    |
| **Total**       | **30**| → **High** — schedule in current or next cycle              |

---

## Leadership Offset Indicator

The Leadership Offset Indicator is a **formal governance mechanism** for cases
where a stakeholder-driven organizational or strategic priority cannot be fully
captured by the four VECD dimensions. It exists to make those decisions visible,
traceable, and accountable — not to bypass the scoring process.

### Purpose

Prioritization frameworks break down at the edges. A regulatory mandate, a
board commitment, or a critical security incident may require an initiative to
jump tiers regardless of its raw score. Equally, a resource constraint or
strategic pause may require an initiative to be held below its scored tier.

The Leadership Offset Indicator provides a sanctioned, documented path for
these exceptions. It does not change the underlying VECD scores. It is a
planning signal that sits *on top* of the score, with an expiry date and
a named owner.

### Governance Requirements

An offset is only valid when all four of the following are present in the
issue record:

| Field              | Requirement                                                         |
|--------------------|---------------------------------------------------------------------|
| **Approver Name**  | Full name of the person authorizing the offset                      |
| **Approver Role**  | Organizational role (e.g. VP Engineering, Director of Product, CTO) |
| **Rationale**      | Specific trigger, consequence of not acting, and any external deadline or commitment |
| **Adjusted Score** | The leadership-adjusted score and resulting tier                    |

Verbal approvals, Slack messages, and informal agreements do not satisfy the
governance requirement. The record must live in the issue body.

### Valid Offset Triggers

**Accelerate** (raises effective priority above VECD score):

- Regulatory or legal deadline with a fixed external date
- Executive or board commitment made to a customer or partner
- Active security incident or production-impacting vulnerability
- Hard external dependency where a third party is blocked on this team
- Time-boxed market or seasonal window that cannot be moved

**Defer** (lowers effective priority below VECD score):

- Required team or key individual unavailable for a defined period
- Leadership has explicitly paused the initiative pending a strategic decision
- Upstream blocker with no near-term resolution
- Deliberate sequencing: another initiative must ship first to validate assumptions
- Dependency on an external release, API, or platform feature not yet available

### What an Offset Is Not

An offset is not a way to act on executive preference without transparency, to
override a scoring decision informally, or to avoid the work of rescoring when
circumstances have genuinely changed. If the scores feel wrong — rescore first.
Apply an offset only when the VECD dimensions themselves cannot capture the
relevant constraint or commitment.

### Offset Governance Rules

- **One offset per issue at a time.** Accelerate and defer cannot coexist.
- **Offsets expire.** They must be re-approved or removed at each planning cycle.
  Every offset requires a re-evaluation date.
- **Offsets do not mutate VECD scores.** The underlying V, E, C, D scores
  remain as originally assessed. The offset is a separate, clearly labeled layer.
- **Audit trail is mandatory.** All offset details must be recorded in the issue
  body. This creates a searchable, reviewable record of every non-formula
  prioritization decision the organization makes.

---

## Calculator

The included CLI tool validates inputs, calculates the priority score, outputs
the tier, and flags when a Leadership Offset may be worth considering
(score within 2 points of a tier boundary).

```bash
# Basic usage
python scripts/calculate_priority.py -V 16 -E 7 -C 4 -D 3

# Output
#   Priority Score  :  30 / 40
#   Tier            :  HIGH — Schedule in current or next cycle

# JSON output (for CI pipelines or scripting)
python scripts/calculate_priority.py -V 16 -E 7 -C 4 -D 3 --json

# Score only (for shell variable capture)
python scripts/calculate_priority.py -V 16 -E 7 -C 4 -D 3 --quiet

# Plain text (no ANSI colour, for logs)
python scripts/calculate_priority.py -V 16 -E 7 -C 4 -D 3 --no-color
```

**Argument reference:**

| Flag                  | Dimension       | Range | Required |
|-----------------------|-----------------|-------|----------|
| `-V` / `--value`      | Value           |  0–20 | Yes      |
| `-E` / `--effort`     | Effort          |  0–10 | Yes      |
| `-C` / `--cost-of-delay` | Cost of Delay|  0–5  | Yes      |
| `-D` / `--dependency` | Dependency      |  0–5  | Yes      |

All inputs are validated against their allowed ranges. The tool exits with
code `2` on invalid input.

---

## Issue Template

All scoring and offset documentation lives in a single GitLab issue template:

```
.gitlab/issue_templates/VECD_Priority_Request.md
```

The template covers:
- Initiative overview, problem statement, and success metrics
- Guided scoring for all four VECD dimensions with embedded rubric anchors
- Priority Score summary table and tier selection
- Leadership Offset Indicator section with all governance fields
- Acceptance criteria and dependency/risk register

New issues opened from this template are automatically labeled
`~"vecd::pending-score"`. Replace with `~"vecd::scored"` once all four
dimension scores and justifications are complete.

---

## GitLab Labels

Create the following labels in **Settings → Labels** before using the framework.

**Priority tier labels** — applied after scoring:

| Label                 | Color     | When to apply                      |
|-----------------------|-----------|------------------------------------|
| `priority::critical`  | `#c0392b` | Score 35–40                        |
| `priority::high`      | `#e67e22` | Score 25–34                        |
| `priority::medium`    | `#3498db` | Score 15–24                        |
| `priority::low`       | `#95a5a6` | Score 0–14                         |

**Workflow labels** — track scoring status:

| Label                 | Color     | When to apply                                  |
|-----------------------|-----------|------------------------------------------------|
| `vecd::pending-score` | `#f39c12` | Issue opened, scoring not yet complete         |
| `vecd::scored`        | `#27ae60` | All four dimensions scored and justified       |

**Offset labels** — applied when a Leadership Offset is in effect:

| Label                 | Color     | When to apply                                  |
|-----------------------|-----------|------------------------------------------------|
| `offset::accelerate`  | `#8e44ad` | Offset raises effective priority above score   |
| `offset::defer`       | `#7f8c8d` | Offset lowers effective priority below score   |

Offset labels must be removed or re-applied at each planning cycle. A stale
offset label with no corresponding justification in the issue body is not valid.

---

## Repository Structure

```
vecd-priority-framework/
├── README.md                                        # This document
├── .gitlab/
│   └── issue_templates/
│       └── VECD_Priority_Request.md                # Issue intake and scoring form
├── docs/
│   ├── scoring-guide.md                            # Extended rubric with worked examples
│   └── offset-indicator-guide.md                  # Offset governance reference
└── scripts/
    └── calculate_priority.py                       # CLI priority score calculator
```

---

## Design Rationale

### Why RICE was not enough

RICE (Reach × Impact × Confidence ÷ Effort) is a widely used framework, but it
has limitations in cross-functional and platform contexts:

- **Reach** is difficult to quantify for infrastructure, internal tooling, or
  governance work where users are downstream teams rather than direct end-users.
- **Confidence** introduces a second-order uncertainty score that is rarely
  calibrated consistently across teams and tends to compress scores toward the
  middle.
- RICE does not account for *when* something needs to ship, only *whether* it
  should. Two initiatives with identical RICE scores but different urgency
  profiles will be treated as equivalent.

### Why these four dimensions

**Value** replaces Reach × Impact as a single unified signal. Evaluating them
together forces scorers to weigh both factors against each other rather than
inflating one to compensate for a weak other.

**Effort** is inverted relative to RICE: instead of dividing by effort, it is a
first-class additive score. This makes the trade-off between value and effort
explicit in the number, visible in the breakdown, and easier to discuss in
planning sessions.

**Cost of Delay** operationalizes urgency as a formal dimension. It forces teams
to articulate the consequence of waiting — a discipline that prevents high-value
but non-urgent work from crowding out time-sensitive work that scores similarly
on value alone.

**Dependency** addresses execution risk directly. A high-scoring initiative that
cannot move without resolving three upstream blockers is not equivalent to one
that can start tomorrow. Surfacing this in the score prevents planning sessions
from repeatedly cycling back to the same blocked items.

### Why the score is additive, not weighted

Weighted formulas introduce tuning complexity and make scores harder to explain
to stakeholders. An additive system with dimension-specific maximums (20, 10, 5, 5)
encodes the same relative weights while keeping the arithmetic transparent:
anyone can verify a score with mental math. The framework's goal is alignment
and shared understanding, not algorithmic precision.
