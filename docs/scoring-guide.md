# VECD Scoring Guide

Full rubric and worked examples for the VECD Priority Framework.
For a concise summary, see the README. For offset governance, see
`docs/offset-indicator-guide.md`.

---

## Scoring Model

VECD uses an **additive scoring model**. Each dimension has a fixed maximum
that encodes its relative weight. Scores are integers. No formula or calculator
is required — sum the four values.

```
Priority Score  =  V  +  E  +  C  +  D
Maximum Score   =  20 + 10  +  5  +  5  =  40
```

| Dimension         | Range | Max | Weight | Direction                        |
|-------------------|-------|-----|--------|----------------------------------|
| V — Value         |  0–20 |  20 |   50%  | Higher = greater value           |
| E — Effort        |  0–10 |  10 |   25%  | Higher = less effort             |
| C — Cost of Delay |   0–5 |   5 | 12.5%  | Higher = more urgent             |
| D — Dependency    |   0–5 |   5 | 12.5%  | Higher = fewer upstream blockers |

**Note on Effort:** Unlike RICE, Effort is *additive* here — a higher score
means the work is *easier* to ship. This keeps all four dimensions moving in
the same direction (higher is better) and makes the breakdown easier to read
and discuss. Assess Effort as ease of delivery, then score inversely to the
effort required.

---

## Priority Tiers

| Tier         | Score Range | Action                                     | GitLab Label         |
|--------------|-------------|--------------------------------------------|----------------------|
| **Critical** |    35–40    | Immediate action required                  | `priority::critical` |
| **High**     |    25–34    | Schedule in current or next cycle          | `priority::high`     |
| **Medium**   |    15–24    | Backlog — plan within 1–2 quarters         | `priority::medium`   |
| **Low**      |     0–14    | Defer, revisit at roadmap review, or close | `priority::low`      |

Tier boundaries: **15**, **25**, **35**. A score within 2 points of a boundary
means a Leadership Offset may be worth considering to promote or demote the tier.
The CLI calculator flags this automatically.

---

## V — Value `0–20`

**What it measures:** The strategic, business, or user value delivered if this
initiative ships. This is the highest-weighted dimension (50%). Score it relative
to current stated goals, OKRs, or KPIs — not against an abstract ideal.

| Score  | Anchor                                                                                                    |
|--------|-----------------------------------------------------------------------------------------------------------|
| 18–20  | Transformative. Core to company strategy, a flagship OKR, or significant direct revenue impact.          |
| 14–17  | High value. Directly advances a key goal; meaningful outcome for a large segment or system.              |
|  9–13  | Moderate value. Improves experience or efficiency for a notable group or measurable metric.              |
|  4–8   | Low value. Marginal improvement; addresses a small, infrequent, or indirect pain point.                  |
|  0–3   | Negligible. Nice-to-have with no clear business outcome, user impact, or strategic alignment.            |

**Scoring guidance:**

- Tie to a specific OKR, KPI, or documented user research finding wherever possible.
  A score without an evidence anchor is harder to defend and easier to challenge.
- Consider both *reach* (how many users, teams, or systems are affected) and
  *impact* (by how much does the outcome change for them). High reach with low
  impact and low reach with high impact can both land in the mid-range.
- Do not inflate Value because the work is technically interesting or long overdue.
  Longevity in the backlog is not a value signal.
- Do not conflate value with effort. A two-hour change that unblocks a revenue
  stream scores the same as a complex one that achieves the same outcome.
- For platform or infrastructure work where users are downstream teams: estimate
  the aggregate value delivered to those teams, not the value of the infra itself.

---

## E — Effort `0–10`

**What it measures:** The *ease* of delivery — **higher score means lower effort**.
Factor in engineering complexity, cross-team coordination, testing burden,
operational overhead, and uncertainty.

| Score | Anchor                                                                                              |
|-------|-----------------------------------------------------------------------------------------------------|
|  9–10 | Trivial. Hours of work, single contributor, well-understood scope, no coordination required.        |
|  7–8  | Small. 1–3 days, single team, low uncertainty, straightforward testing.                             |
|  5–6  | Medium. 1–2 weeks, possible cross-team touch points, some design decisions still open.              |
|  2–4  | Large. 2–6 weeks, multiple teams, significant architecture, infrastructure, or compliance work.     |
|  0–1  | Extra-large. Months of work, high uncertainty, requires discovery phase or architectural spike.     |

**Scoring guidance:**

- Score Effort as you would estimate the *total* delivery cost: implementation,
  code review, testing, documentation, deployment, and any ongoing operational burden.
- If a discovery spike or scoping exercise is needed before the work can be
  properly estimated, score it at 0–1 and rescore after the spike concludes.
- Cross-team coordination is a significant effort multiplier. If the work requires
  alignment, sign-off, or active contribution from teams outside your own, reduce
  the score by 1–2 points to reflect the coordination overhead.
- A score of 5–6 is the most common for well-defined, single-team work of typical
  sprint size. Scores below 3 should be rare and represent genuinely significant
  investments of time or organizational complexity.

---

## C — Cost of Delay `0–5`

**What it measures:** The cost or harm incurred by deferring this initiative.
Framed as: *what is materially lost or risked if delivery slips by 4 weeks?
By an entire quarter?*

| Score | Anchor                                                                                              |
|-------|-----------------------------------------------------------------------------------------------------|
|   5   | Critical urgency. Immediate financial, legal, reputational, or contractual consequence if delayed. |
|   4   | High urgency. A hard external deadline exists; missing it causes a meaningful penalty or setback.  |
|   3   | Moderate urgency. A time-sensitive window; delay causes a notable but recoverable opportunity cost.|
|   2   | Low urgency. Incremental value loss over time, but no hard deadline or external pressure.           |
|  0–1  | No urgency. Can be deferred indefinitely with negligible consequence to users or the business.     |

**Scoring guidance:**

- Apply the **4-week test** explicitly in the justification: state what happens
  if this slips one month, then state what happens if it slips an entire quarter.
  The answers should directly drive the score.
- **Strong signals for 4 or 5:** regulatory audit deadline, SLA breach risk,
  contractual penalty clause, active security vulnerability in production,
  customer commitment with financial consequences.
- **Weak signals (do not inflate):** self-imposed internal deadlines, urgency
  created by deferral decisions made in previous cycles, "the team really wants
  to ship this," or executive enthusiasm without a hard external commitment.
- Urgency manufactured by poor planning should not score the same as urgency
  imposed by an external party. Distinguish between pressure that exists
  regardless of internal choices and pressure that the team created.

---

## D — Dependency `0–5`

**What it measures:** The *dependency burden* on this initiative —
**fewer upstream blockers yields a higher score**. An initiative that can
start and ship independently scores 5. One that is entangled in unresolved
upstream decisions, third-party timelines, or multiple teams' deliverables
scores 0 or 1.

| Score | Anchor                                                                                              |
|-------|-----------------------------------------------------------------------------------------------------|
|   5   | Fully independent. No upstream blockers; can start and ship without waiting on anyone.              |
|   4   | Mostly independent. One minor dependency with a clear owner and a near-term, reliable resolution.  |
|   3   | Moderate. 2–3 dependencies; some have workarounds, but meaningful progress requires them.           |
|   2   | Heavily dependent. Multiple upstream blockers; meaningful risk that another team causes delay.      |
|  0–1  | Highly entangled. Blocked by unresolved decisions, external vendors, or many other teams.           |

**Scoring guidance:**

- List *concrete* dependencies in the justification — not hypothetical ones.
  "We might need the data team" is not a blocker. "The data team must deliver
  a schema migration before we can begin" is.
- Distinguish **hard blocks** (the work literally cannot start or complete
  without this) from **soft blocks** (a workaround exists, even if imperfect).
  A soft dependency is typically worth 1–2 fewer points of reduction than a
  hard block.
- Include both technical dependencies (APIs, infrastructure, data pipelines,
  third-party SDKs) and process dependencies (compliance approvals,
  architectural review sign-off, legal clearance, data privacy assessments).
- If a dependency is expected to resolve within the current planning cycle
  with high confidence, it may be scored as a soft block. If resolution
  timing is uncertain, score it as a hard block.

---

## Worked Examples

### Example 1 — High tier, no offset

**Initiative:** Add scheduled export to the analytics dashboard

| Dimension         | Score | Reasoning                                                                      |
|-------------------|-------|--------------------------------------------------------------------------------|
| V — Value         |  16   | Eliminates ~2 hrs/week of manual re-export for ~40% of analysts (Q3 KPI)       |
| E — Effort        |   7   | ~3 days, single team, export pipeline already exists                            |
| C — Cost of Delay |   3   | No hard deadline; delay causes ongoing inconvenience but no contractual risk   |
| D — Dependency    |   4   | Needs a minor config change from the infra team — owner identified, 2-day ETA  |
| **Total**         | **30**| → **High** — schedule in current or next cycle                                 |

---

### Example 2 — Critical tier with offset flag

**Initiative:** Migrate auth service to OAuth 2.0

| Dimension         | Score | Reasoning                                                                      |
|-------------------|-------|--------------------------------------------------------------------------------|
| V — Value         |  17   | Enables partner revenue channel; directly tied to Q3 revenue OKR               |
| E — Effort        |   5   | ~2 weeks; involves security review, two teams, and compliance sign-off         |
| C — Cost of Delay |   5   | Partner launch committed for next month; delay triggers contract penalty clause |
| D — Dependency    |   4   | Requires security team review — owner confirmed, review slotted for next week  |
| **Total**         | **31**| → **High** — but proximity to Critical boundary (4 points away) noted          |

> Score 31 is 4 points below the Critical boundary (35). The CLI would not flag an
> offset here. If the contract penalty was confirmed in writing by legal, a scorer
> might reconsider C=5 and E, and if the true effort is lower, the score could rise.
> Rescore before applying an offset.

---

### Example 3 — Low tier, high effort drag

**Initiative:** Rewrite the legacy reporting module in a new framework

| Dimension         | Score | Reasoning                                                                      |
|-------------------|-------|--------------------------------------------------------------------------------|
| V — Value         |  10   | Improves developer experience; no direct user-facing or revenue outcome        |
| E — Effort        |   1   | Months of work; high uncertainty; cross-team; requires discovery spike first   |
| C — Cost of Delay |   1   | No deadline; existing module is slow but functional                             |
| D — Dependency    |   5   | Fully independent; no upstream blockers                                         |
| **Total**         | **17**| → **Medium** — backlog, plan within 1–2 quarters                               |

> The low Effort score (very high effort) is the primary drag here. If the
> discovery spike surfaces a smaller, phased approach, rescore after scoping.

---

## Common Scoring Errors

| Error                                    | Correction                                                                 |
|------------------------------------------|----------------------------------------------------------------------------|
| Scoring Value high because work is overdue | Longevity in the backlog is not value. Score against business outcomes.  |
| Inflating Cost of Delay for internal deadlines | Only external commitments and hard constraints score 4–5.           |
| Scoring Dependency based on downstream blockers | D measures upstream blockers on *this* work, not what *this* blocks. |
| Giving Effort a high score for uncertain work | Uncertainty reduces the Effort score. Spike first, then rescore.     |
| Skipping written justifications          | Unjustified scores will be returned. Numbers without reasoning are not defensible. |
