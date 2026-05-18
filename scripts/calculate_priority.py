#!/usr/bin/env python3
"""
VECD Priority Score Calculator
───────────────────────────────────────────────────────────────────────────────
Scores an initiative across four dimensions and produces a composite priority
score and tier. Platform-agnostic — works for any team or initiative type.

DIMENSIONS
  -V / --value          Business or user value delivered          (0–20, weight 50%)
  -E / --effort         Ease of delivery (higher = less effort)   (0–10, weight 25%)
  -C / --cost-of-delay  Urgency cost of deferring this work       (0–5,  weight 12.5%)
  -D / --dependency     Independence (higher = fewer blockers)    (0–5,  weight 12.5%)

SCORING
  Priority Score  =  V + E + C + D   (max 40, additive — no weighting formula)

  Tier        Range    Meaning
  ─────────────────────────────────────────────────────
  Critical    35–40    Immediate action required
  High        25–34    Schedule in current or next cycle
  Medium      15–24    Backlog — plan within 1–2 quarters
  Low          0–14    Defer, revisit, or close

OFFSET FLAG
  If the score falls within 2 points of a tier boundary, the tool flags that a
  Leadership Offset may be worth considering to promote or demote the tier.

USAGE
  python calculate_priority.py -V 16 -E 7 -C 4 -D 3
  python calculate_priority.py --value 16 --effort 7 --cost-of-delay 4 --dependency 3
  python calculate_priority.py -V 12 -E 5 -C 2 -D 4 --json
  python calculate_priority.py -V 18 -E 9 -C 5 -D 5 --quiet
"""

import argparse
import json as json_module
import sys
from dataclasses import dataclass, asdict
from typing import Optional


# ── Tier definitions ──────────────────────────────────────────────────────────

@dataclass
class Tier:
    name: str
    label: str       # GitLab label value
    low: int         # inclusive lower bound
    high: int        # inclusive upper bound
    action: str      # plain-English action prompt


TIERS: list[Tier] = [
    Tier("Critical", "priority::critical", 35, 40, "Immediate action required"),
    Tier("High",     "priority::high",     25, 34, "Schedule in current or next cycle"),
    Tier("Medium",   "priority::medium",   15, 24, "Backlog — plan within 1–2 quarters"),
    Tier("Low",      "priority::low",       0, 14, "Defer, revisit, or close"),
]

# Boundaries where a score crossing means a tier change (ascending).
# Used to detect proximity and flag offset recommendations.
TIER_BOUNDARIES: list[int] = [15, 25, 35]

OFFSET_PROXIMITY = 2   # points from a boundary that triggers an offset flag


# ── Dimension definitions ─────────────────────────────────────────────────────

@dataclass
class Dimension:
    flag: str         # CLI short flag (single letter)
    name: str         # display name
    arg_name: str     # argparse dest name
    min: int
    max: int
    description: str


DIMENSIONS: list[Dimension] = [
    Dimension("V", "Value",          "value",         0, 20, "Business or user value delivered"),
    Dimension("E", "Effort",         "effort",        0, 10, "Ease of delivery (higher = less effort)"),
    Dimension("C", "Cost of Delay",  "cost_of_delay", 0,  5, "Urgency cost of deferring this work"),
    Dimension("D", "Dependency",     "dependency",    0,  5, "Independence (higher = fewer blockers)"),
]


# ── Core logic ────────────────────────────────────────────────────────────────

def get_tier(score: int) -> Tier:
    for tier in TIERS:
        if tier.low <= score <= tier.high:
            return tier
    # score is guaranteed valid (0–40) after validation, but be safe
    return TIERS[-1]


@dataclass
class OffsetFlag:
    recommended: bool
    reason: str
    nearest_boundary: Optional[int]
    points_away: Optional[int]
    direction: Optional[str]   # "above" or "below"


def check_offset(score: int) -> OffsetFlag:
    """
    Return an OffsetFlag if the score is within OFFSET_PROXIMITY points of
    any tier boundary. Proximity to a boundary means a small adjustment could
    change the tier — a leadership offset may be worth considering.
    """
    nearest_boundary = None
    nearest_distance = None

    for boundary in TIER_BOUNDARIES:
        distance = abs(score - boundary)
        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_boundary = boundary

    if nearest_distance is None or nearest_distance > OFFSET_PROXIMITY:
        return OffsetFlag(False, "Score is comfortably within its tier.", None, None, None)

    direction = "above" if score >= nearest_boundary else "below"
    crossing = "promote" if direction == "below" else "demote"

    if nearest_distance == 0:
        # Score sits exactly on a boundary — it already achieved the higher tier,
        # but a single-point drop would demote it.
        reason = (
            f"Score {score} sits exactly on the {nearest_boundary}-point tier boundary. "
            f"A 1-point Leadership Offset would demote this item to the tier below."
        )
    else:
        pts = f"{nearest_distance} point{'s' if nearest_distance != 1 else ''}"
        reason = (
            f"Score {score} is {pts} {direction} the {nearest_boundary}-point tier boundary. "
            f"A Leadership Offset of {pts} would {crossing} this item to the next tier."
        )

    return OffsetFlag(
        recommended=True,
        reason=reason,
        nearest_boundary=nearest_boundary,
        points_away=nearest_distance,
        direction=direction,
    )


@dataclass
class Result:
    score: int
    tier: Tier
    offset: OffsetFlag
    inputs: dict[str, int]


def calculate(inputs: dict[str, int]) -> Result:
    score = sum(inputs.values())
    tier = get_tier(score)
    offset = check_offset(score)
    return Result(score=score, tier=tier, offset=offset, inputs=inputs)


# ── Validation ────────────────────────────────────────────────────────────────

def validate_inputs(args: argparse.Namespace) -> dict[str, int]:
    """Validate all dimension scores against their allowed ranges. Exit on error."""
    errors: list[str] = []
    inputs: dict[str, int] = {}

    for dim in DIMENSIONS:
        value = getattr(args, dim.arg_name)
        if not isinstance(value, int) or not (dim.min <= value <= dim.max):
            errors.append(
                f"  --{dim.arg_name.replace('_', '-')} ({dim.flag}): "
                f"must be an integer {dim.min}–{dim.max}, got {value!r}"
            )
        else:
            inputs[dim.arg_name] = value

    if errors:
        print("Validation failed:\n" + "\n".join(errors), file=sys.stderr)
        sys.exit(2)

    return inputs


# ── Output renderers ──────────────────────────────────────────────────────────

# ANSI colour codes — suppressed when --no-color is set or output is not a TTY
COLOURS = {
    "Critical": "\033[91m",   # bright red
    "High":     "\033[93m",   # bright yellow
    "Medium":   "\033[94m",   # bright blue
    "Low":      "\033[37m",   # light grey
    "offset":   "\033[95m",   # bright magenta
    "dim":      "\033[2m",    # dim
    "bold":     "\033[1m",    # bold
    "reset":    "\033[0m",
}


def coloured(text: str, *keys: str, use_color: bool = True) -> str:
    if not use_color:
        return text
    prefix = "".join(COLOURS[k] for k in keys if k in COLOURS)
    return f"{prefix}{text}{COLOURS['reset']}"


def render_human(result: Result, use_color: bool) -> str:
    tier = result.tier
    offset = result.offset
    score = result.score

    tier_colour = tier.name if use_color else ""
    bar_filled = round((score / 40) * 30)
    bar = "█" * bar_filled + "░" * (30 - bar_filled)

    lines: list[str] = []
    sep = "─" * 52

    lines.append("")
    lines.append(coloured("  VECD Priority Score", "bold", use_color=use_color))
    lines.append(f"  {sep}")

    # Dimension breakdown
    max_widths = {"Value": 20, "Effort": 10, "Cost of Delay": 5, "Dependency": 5}
    for dim in DIMENSIONS:
        value = result.inputs[dim.arg_name]
        max_val = dim.max
        pct = int((value / max_val) * 100) if max_val else 0
        lines.append(
            f"  {dim.flag}  {dim.name:<14}  "
            + coloured(f"{value:>3}", "bold", use_color=use_color)
            + f" / {max_val:<3}  ({pct:>3}% of max)"
        )

    lines.append(f"  {sep}")

    # Score and bar
    score_str = coloured(f"{score}", "bold", tier_colour, use_color=use_color)
    lines.append(f"  Priority Score  :  {score_str} / 40")
    lines.append(f"  {coloured(bar, tier_colour, use_color=use_color)}")

    lines.append("")

    # Tier block
    tier_label = coloured(f"  ● {tier.name.upper()}", "bold", tier_colour, use_color=use_color)
    lines.append(tier_label)
    lines.append(f"    {tier.action}")
    lines.append(f"    GitLab label: ~\"{tier.label}\"")
    lines.append(f"    Tier range:   {tier.low}–{tier.high} points")

    lines.append("")

    # Tier map — show where the score sits
    lines.append(coloured("  Tier Map", "dim", use_color=use_color))
    for t in TIERS:
        marker = "◀ you are here" if t.name == tier.name else ""
        marker_str = coloured(f"  {marker}", "bold", tier_colour, use_color=use_color) if marker else ""
        indicator = coloured("●", "bold", t.name, use_color=use_color)
        lines.append(f"    {indicator}  {t.name:<9}  {t.low:>2}–{t.high:<2}{marker_str}")

    lines.append("")

    # Offset section
    if offset.recommended:
        offset_header = coloured("  ⚑  Leadership Offset Recommended", "bold", "offset", use_color=use_color)
        lines.append(offset_header)
        lines.append(f"  {sep}")
        # Wrap the reason at ~70 chars
        words = offset.reason.split()
        current_line = "  "
        for word in words:
            if len(current_line) + len(word) + 1 > 72:
                lines.append(current_line)
                current_line = "  " + word
            else:
                current_line += (" " if current_line != "  " else "") + word
        if current_line.strip():
            lines.append(current_line)
        lines.append("")
        lines.append("  To apply an offset, complete the Leadership Offset Indicator")
        lines.append("  section in the issue template (docs/offset-indicator-guide.md).")
    else:
        lines.append(coloured("  ✓  No Leadership Offset flagged", "dim", use_color=use_color))
        lines.append(f"  {coloured(offset.reason, 'dim', use_color=use_color)}")

    lines.append("")
    return "\n".join(lines)


def render_json(result: Result) -> str:
    tier = result.tier
    offset = result.offset

    data = {
        "score": result.score,
        "max_score": 40,
        "tier": {
            "name": tier.name,
            "label": tier.label,
            "range": {"low": tier.low, "high": tier.high},
            "action": tier.action,
        },
        "inputs": result.inputs,
        "offset": {
            "recommended": offset.recommended,
            "reason": offset.reason,
            "nearest_boundary": offset.nearest_boundary,
            "points_away": offset.points_away,
            "direction": offset.direction,
        },
    }
    return json_module.dumps(data, indent=2)


def render_quiet(result: Result) -> str:
    return str(result.score)


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calculate_priority.py",
        description="Calculate a VECD composite priority score and tier.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    for dim in DIMENSIONS:
        parser.add_argument(
            f"-{dim.flag}",
            f"--{dim.arg_name.replace('_', '-')}",
            type=int,
            required=True,
            metavar=f"{dim.min}-{dim.max}",
            help=f"{dim.description}  [{dim.min}–{dim.max}]",
        )

    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output (useful for CI / scripting)",
    )
    output.add_argument(
        "--quiet",
        action="store_true",
        help="Emit score integer only — no labels, no offset flag",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colour codes in human-readable output",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    inputs = validate_inputs(args)
    result = calculate(inputs)

    use_color = not args.no_color and sys.stdout.isatty()

    if args.quiet:
        print(render_quiet(result))
    elif args.json:
        print(render_json(result))
    else:
        print(render_human(result, use_color=use_color))


if __name__ == "__main__":
    main()
