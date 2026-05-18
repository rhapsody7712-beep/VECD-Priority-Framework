<!--
  VECD Priority Request — Intake Form
  ─────────────────────────────────────────────────────────────────────────────
  Framework: VECD (Value · Effort · Cost of Delay · Dependency)
  Version:   1.0
  Status:    [ ] Draft  [ ] Scored  [ ] Reviewed  [ ] Approved

  Platform-agnostic — this framework is reusable across any team, product,
  platform, or initiative. It does not assume a specific methodology, toolchain,
  or delivery model.

  HOW TO USE THIS TEMPLATE
  1. Complete the Initiative Overview section.
  2. Score each of the four VECD dimensions using the rubric embedded below.
  3. Sum the four dimension scores to get the Priority Score (max 40).
  4. Identify the Priority Tier from the score.
  5. If leadership adjusts the score, complete the Leadership Offset section.
  6. Assign the appropriate GitLab label before submitting.

  SCORING REFERENCE (quick view — see docs/scoring-guide.md for full rubric)
  ┌─────────────────────┬────────┬────────┬─────────────────────────────────┐
  │ Dimension           │ Range  │ Weight │ Higher score means…             │
  ├─────────────────────┼────────┼────────┼─────────────────────────────────┤
  │ V  Value            │  0–20  │  50%   │ Greater business / user value   │
  │ E  Effort           │  0–10  │  25%   │ Lower effort (easier to ship)   │
  │ C  Cost of Delay    │  0–5   │ 12.5%  │ More urgent to deliver now      │
  │ D  Dependency       │  0–5   │ 12.5%  │ Fewer blocking dependencies     │
  ├─────────────────────┼────────┼────────┼─────────────────────────────────┤
  │ Priority Score      │  0–40  │  100%  │ Sum of all four dimensions      │
  └─────────────────────┴────────┴────────┴─────────────────────────────────┘

  PRIORITY TIERS
  ● Critical   35–40   Immediate action required
  ● High       25–34   Schedule in current or next cycle
  ● Medium     15–24   Backlog — plan within 1–2 quarters
  ● Low         0–14   Defer, revisit, or close
-->

---

## Initiative Overview

**Title:**
<!-- A clear, descriptive name for this initiative, feature, or request. -->

**Submitter:**
<!-- Name and team of the person submitting this request. -->

**Date Submitted:** <!-- YYYY-MM-DD -->

**Target Team / Platform:**
<!-- Which team, product area, or platform will own this work? (Leave blank if cross-cutting.) -->

**Initiative Type:**
- [ ] New Feature
- [ ] Enhancement / Iteration
- [ ] Bug Fix / Reliability
- [ ] Technical Debt / Refactor
- [ ] Compliance / Security
- [ ] Research / Discovery
- [ ] Other: _______________

---

## Problem Statement

<!-- Required. What problem or opportunity does this address?
     Be specific: who is affected, how often, and what the impact is today.
     Bad:  "Users are unhappy with the dashboard."
     Good: "~40% of analysts re-export data manually each week because the
            dashboard lacks scheduled exports, costing ~2 hrs/person/week." -->

## Proposed Solution

<!-- Required. What is being proposed? Describe the approach at a level that
     allows a non-technical stakeholder to understand the scope.
     Note any known alternatives considered and why this approach was chosen. -->

## Success Metrics

<!-- How will you know this initiative succeeded?
     List 1–3 measurable outcomes (e.g. reduce churn by 5%, cut p99 latency to <200ms). -->

---

## VECD Scoring

> Complete all four dimensions. Each section includes a scoring rubric.
> Scores are additive. **Maximum total = 40.**

---

### V — Value `__ / 20` · Weight: 50%

**What it measures:** The strategic, business, or user value delivered if this work ships.
Includes revenue impact, user experience improvement, operational efficiency, and alignment
to stated goals or OKRs. This is the highest-weight dimension — score it carefully.

| Score Range | Meaning                                                                                     |
|-------------|---------------------------------------------------------------------------------------------|
| 18–20       | Transformative. Core to company strategy, a major OKR, or significant revenue impact.       |
| 14–17       | High value. Directly advances a key goal; meaningful impact on a large user segment.        |
| 9–13        | Moderate value. Improves experience or efficiency for a notable group; tied to a goal.      |
| 4–8         | Low value. Marginal improvement; addresses a small or infrequent pain point.                |
| 0–3         | Negligible. Nice-to-have with no clear business or user outcome.                            |

**Score (0–20):** `__`

**Justification:**
<!-- Required. Explain the score. Tie to a specific OKR, KPI, or user research finding.
     How many users or teams are affected? What outcome improves and by how much? -->

---

### E — Effort `__ / 10` · Weight: 25%

**What it measures:** Ease of delivery — a higher score means *lower* effort.
Factor in engineering complexity, cross-team coordination, testing burden,
operational overhead, and uncertainty. Effort depresses priority: high-effort
work must justify itself with high value or urgency.

| Score Range | Meaning                                                                                     |
|-------------|----------------------------------------------------------------------------------------------|
| 9–10        | Trivial. Hours of work, single contributor, no coordination required.                        |
| 7–8         | Small. 1–3 days, single team, low uncertainty.                                               |
| 5–6         | Medium. 1–2 weeks, possible cross-team dependencies, some unknowns.                          |
| 2–4         | Large. 2–6 weeks, multiple teams, significant design or infrastructure work.                 |
| 0–1         | Extra-large. Months of work, high uncertainty, requires discovery or architecture phase.     |

**Score (0–10):** `__`

**Justification:**
<!-- Required. Estimate team-weeks and explain key complexity drivers.
     Add 1–2 points of uncertainty if a spike or discovery is needed first.
     Do not conflate difficulty with value — a hard thing can still be low-value. -->

---

### C — Cost of Delay `__ / 5` · Weight: 12.5%

**What it measures:** The urgency cost of deferring this work — what is lost or risked
if delivery slips by 4 weeks, 3 months, or a quarter. Regulatory deadlines, customer
commitments, and competitive pressure all factor in.

| Score | Meaning                                                                                     |
|-------|---------------------------------------------------------------------------------------------|
| 5     | Critical urgency. Immediate financial, legal, reputational, or contractual consequence.     |
| 4     | High urgency. A hard deadline exists; missing it causes meaningful setback or penalty.      |
| 3     | Moderate urgency. A time-sensitive window; delay causes notable opportunity cost.           |
| 2     | Low urgency. Some value loss over time, but no hard deadline or external pressure.          |
| 0–1   | No urgency. Can be deferred indefinitely with minimal consequence.                          |

**Score (0–5):** `__`

**Justification:**
<!-- Required. Describe the consequence of a 4-week delay, then a 3-month delay.
     Cite any hard deadlines (e.g. "SOC 2 audit date: 2026-06-30", "Q3 customer commitment").
     Urgency caused by poor planning should not automatically score high. -->

---

### D — Dependency `__ / 5` · Weight: 12.5%

**What it measures:** Dependency *burden* on this initiative — **fewer dependencies = higher score**.
An item that can ship independently scores highest. An item blocked by many upstream teams,
external vendors, or undecided decisions scores lowest.

| Score | Meaning                                                                                     |
|-------|---------------------------------------------------------------------------------------------|
| 5     | Fully independent. No upstream blockers; can start and ship without waiting on anyone.      |
| 4     | Mostly independent. One minor dependency with a clear owner and near-term resolution.       |
| 3     | Moderate dependencies. 2–3 dependencies; some have workarounds, but progress requires them. |
| 2     | Heavily dependent. Multiple upstream blockers; meaningful risk of delay from other teams.   |
| 0–1   | Highly entangled. Blocked by unresolved decisions, external parties, or many other teams.   |

**Score (0–5):** `__`

**Justification:**
<!-- Required. List concrete upstream blockers or prerequisites.
     Distinguish hard blocks (cannot proceed) from soft blocks (workarounds exist).
     Include both technical dependencies (APIs, infra) and process dependencies (approvals, data). -->

---

## Priority Score

> **Score = V + E + C + D**
> Fill in each dimension score, then sum.

| Dimension         | Score  | Max |
|-------------------|--------|-----|
| V — Value         | `__`   | 20  |
| E — Effort        | `__`   | 10  |
| C — Cost of Delay | `__`   | 5   |
| D — Dependency    | `__`   | 5   |
| **Total**         | **`__`** | **40** |

### Priority Tier

Mark the tier that matches the total score:

- [ ] **Critical** `35–40` — Immediate action required; escalate to current sprint or cycle
- [ ] **High** `25–34` — Schedule in current or next planning cycle
- [ ] **Medium** `15–24` — Add to backlog; plan within 1–2 quarters
- [ ] **Low** `0–14` — Defer, revisit at next roadmap review, or close

---

## Leadership Offset Indicator

> **Use sparingly.** An offset is justified only when a specific, verifiable circumstance
> materially changes priority in a way the VECD formula cannot capture.
> Offsets are not a substitute for rescoring. If the scores feel wrong, rescore first.
> All offsets require an approver, a rationale, and a revised score.

**Is a leadership offset being applied?**
- [ ] No offset — VECD score stands as calculated
- [ ] Accelerate — Adjusted score is *higher* than calculated
- [ ] Defer — Adjusted score is *lower* than calculated

*(Complete the section below only if an offset is applied.)*

---

**Approver Name:** <!-- Full name of the person authorizing the offset -->

**Approver Role:** <!-- e.g. VP Engineering, Director of Product, CTO -->

**Date of Approval:** <!-- YYYY-MM-DD -->

**Offset Type:**
- [ ] Accelerate
- [ ] Defer

**Trigger (select all that apply):**
- [ ] Regulatory or legal deadline
- [ ] Executive or board commitment
- [ ] Active security incident or CVE
- [ ] Hard external dependency (vendor, partner, government body)
- [ ] Time-boxed market or seasonal window
- [ ] Strategic resource constraint (key team unavailable)
- [ ] Strategic pause pending a leadership decision
- [ ] Upstream blocker with no near-term resolution
- [ ] Deliberate sequencing (another initiative must ship first)
- [ ] Other: _______________

**Rationale:**
<!-- Required. State the specific trigger, the consequence of not applying the offset,
     and any external deadline or commitment that was made.
     Example: "SOC 2 Type II audit requires completion by 2026-06-30. Failure to comply
     risks contract renewal with our three largest enterprise customers (combined ARR: $4.2M).
     Committed to CISO and Legal on 2026-05-01." -->

**VECD Calculated Score:** `__` / 40

**Leadership-Adjusted Score:** `__` / 40

**Adjusted Priority Tier:**
- [ ] Critical `35–40`
- [ ] High `25–34`
- [ ] Medium `15–24`
- [ ] Low `0–14`

**Offset Expiry / Re-evaluation Date:** <!-- YYYY-MM-DD — when should this offset be reviewed? -->

---

## Acceptance Criteria

<!--
Define concrete, testable conditions that determine when this initiative is complete.
Use the format: "Given [context], when [action], then [outcome]."
Or use a simple checklist:
- [ ] ...
- [ ] ...
-->

## Dependencies & Risks

<!-- List all known upstream dependencies, blockers, and risks with owners where known.
     Format: [Dependency/Risk] — [Owner or team] — [Status or ETA] -->

## Supporting Materials

<!-- Links to specs, mockups, data queries, research, Slack threads, or related issues.
     This section is optional but strongly encouraged for High and Critical tier items. -->

---

<!--
  SCORING NOTES FOR REVIEWERS
  ─────────────────────────────────────────────────────────────────────────────
  This framework is platform-agnostic and is designed to be reused across any
  team, initiative, or delivery methodology (Agile, Kanban, quarterly planning,
  OKR cycles, etc.). The four dimensions — Value, Effort, Cost of Delay, and
  Dependency — are universally applicable regardless of tech stack, org structure,
  or industry.

  Score integrity rules:
  · Scores must be justified in writing. Unjustified scores will be returned.
  · Offsets must be approved by a named leader. Verbal approvals do not count.
  · Offsets do not change underlying VECD scores — they are a planning signal only.
  · Offset labels expire at each planning cycle unless re-approved.

  GitLab label to apply before submitting:
  · vecd::pending-score  (replaced with vecd::scored once all fields are complete)
-->

/label ~"vecd::pending-score"
