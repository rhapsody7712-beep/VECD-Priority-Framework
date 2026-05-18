# Offset Indicator Guide

Offset indicators let teams apply a justified adjustment to an issue's raw VECD score
when exceptional circumstances are not fully captured by the four scoring dimensions.

Offsets are **intentionally narrow**. They exist to handle real-world edge cases, not
to override scores based on gut feel or politics. Every offset must be documented.

---

## When to Use an Offset

Use an offset only when you can answer "yes" to both questions:

1. Does the circumstance materially change the priority in a way the VECD formula cannot capture?
2. Can you point to a concrete, verifiable reason (not just preference)?

If the answer is "we just really want this done soon" — do not apply an offset. Rescore instead.

---

## `offset::accelerate`

**Effect:** Boosts the effective priority above the raw VECD score.
**Label:** `offset::accelerate`

### Valid Reasons

| Trigger                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Regulatory / legal deadline    | A compliance mandate with a fixed external date.                            |
| Executive or board commitment  | A commitment made to a customer, board, or external stakeholder.            |
| Security incident response     | Active vulnerability or breach that requires immediate remediation.         |
| Hard external dependency       | A third-party vendor, partner, or government body is blocked on us.         |
| Time-boxed market window       | A product launch or seasonal event that cannot be moved.                    |

### How to Apply

1. Check the `offset::accelerate` box in the issue template.
2. In the "Offset Justification" field, state:
   - The specific trigger (e.g., "SOC 2 audit requires completion by 2026-06-30")
   - The consequence of not accelerating (e.g., "audit failure, potential contract loss")
   - Who approved the offset (e.g., "confirmed with VP Eng on 2026-05-15")
3. Apply the `offset::accelerate` label in GitLab.
4. Re-triage the issue in the next planning session.

---

## `offset::defer`

**Effect:** Lowers the effective priority below the raw VECD score.
**Label:** `offset::defer`

### Valid Reasons

| Trigger                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Resource constraint            | Required team or individual is unavailable for a defined period.            |
| Strategic pause                | Leadership has explicitly paused this initiative pending a decision.        |
| Upstream blocker               | Cannot begin until another team ships a prerequisite (and that team is slow).|
| Deliberate sequencing          | Another initiative must ship first to validate assumptions for this work.   |
| Dependency on external release | Requires a third-party API, SDK, or platform feature not yet available.     |

### How to Apply

1. Check the `offset::defer` box in the issue template.
2. In the "Offset Justification" field, state:
   - The specific reason for deferral (e.g., "ML platform team unavailable until Q3")
   - The expected unblock date or condition (e.g., "revisit after 2026-08-01")
   - Who approved the deferral
3. Apply the `offset::defer` label in GitLab.
4. Set a due date or milestone on the issue to trigger re-evaluation.

---

## Offset Governance

- **One offset per issue at a time.** You cannot apply both `accelerate` and `defer`.
- **Offsets expire.** Review and remove or re-justify offsets at each planning cycle.
- **Offsets do not change VECD scores.** The underlying V, E, C, D scores remain as scored.
  Offsets are a planning signal, not a scoring mutation.
- **Audit trail.** All offset justifications must be recorded in the issue body.
  Do not communicate offsets only via Slack or verbal agreement.

---

## Quick Reference

| Situation                                   | Action                          |
|---------------------------------------------|---------------------------------|
| Regulatory deadline next month              | `offset::accelerate`            |
| Key engineer on leave for 6 weeks           | `offset::defer`                 |
| "The CEO wants this done first"             | Rescore C (Cost of Delay), not offset |
| Blocked on a vendor API (no ETA)            | `offset::defer` + set reminder  |
| Security CVE in production                  | `offset::accelerate`            |
| Team disagrees with score                   | Rescore using rubric, not offset |
