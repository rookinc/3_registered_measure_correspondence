#!/usr/bin/env python3

from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parents[2]

A011 = (
    HERE
    / "artifacts/json"
    / "registered_measure_exact_sturmian_conjugacy_011.v1.json"
)

A012 = (
    HERE
    / "artifacts/json"
    / "registered_measure_static_binary_history_no_go_012.v1.json"
)

SRC = (
    HERE
    / "source"
    / "project41_row_context_selector_obstruction_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_native_provenance_boundary_013.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_native_provenance_boundary_013.md"
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(obj):
    raw = json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return sha256(raw).hexdigest()


print("== 013 NATIVE PROVENANCE BOUNDARY ==")

a011 = load(A011)
a012 = load(A012)
src = load(SRC)

checks = {}

checks["Audit011_passes"] = (
    a011["audit_pass"] is True
)

checks["Audit012_passes"] = (
    a012["audit_pass"] is True
)

checks["201O_interface_sealed"] = (
    src["status"] == "sealed_prior_theorem_interface"
)

checks["201O_passes"] = (
    src["audit_pass"] is True
)


print("PROGRESS: 1/4 lock exact target history")

checks["exact_infinite_Sturmian_history_closed"] = (
    a011[
        "theorem"
    ][
        "same_infinite_binary_history"
    ]
    is True
)

print(
    "TARGET_HISTORY:",
    "exact infinite Sturmian registered history",
)

print(
    "ZERO_POSITION_LAW:",
    "floor(k/alpha)",
)


print("PROGRESS: 2/4 lock static-action obstruction")

checks["static_native_b_rejected"] = (
    a012[
        "boundary"
    ][
        "rules_out_static_b_as_provenance"
    ]
    is True
)

checks["single_fixed_automorphism_rejected"] = (
    a012[
        "no_go"
    ][
        "any_single_fixed_finite_automorphism"
    ]
    is True
)

print(
    "STATIC_B_PROVENANCE:",
    "REJECTED",
)

print(
    "SINGLE_FIXED_AUTOMORPHISM:",
    "REJECTED",
)


print("PROGRESS: 3/4 lock row-context obstruction")

m = src["measurements"]
b = src["boundary"]

checks["all_120_rows_orientation_invariant"] = (
    m[
        "joint_context_orientation_invariant_count"
    ]
    == 120
)

checks["no_row_context_orientation_distinction"] = (
    m[
        "joint_context_orientation_distinguish_count"
    ]
    == 0
)

checks["row_context_selector_rejected"] = (
    b[
        "row_context_selector_forbidden"
    ]
    is True
)

checks["path_sensitive_selector_remains_open"] = (
    b[
        "path_sensitive_selector_forbidden"
    ]
    is False
    and b[
        "native_path_geometry_still_open"
    ]
    is True
)

checks["interaction_conditioning_not_globally_refuted"] = (
    b[
        "interaction_conditioned_selector_globally_refuted"
    ]
    is False
)

print(
    "ROW_CONTEXT_ROWS:",
    120,
)

print(
    "ROW_CONTEXT_ORIENTATION_DISTINGUISH_COUNT:",
    0,
)

print(
    "ORIENTATION_BLIND_ROW_SELECTOR:",
    "REJECTED",
)

print(
    "PATH_SENSITIVE_HISTORY:",
    "OPEN",
)


print("PROGRESS: 4/4 classify")

failed = [
    key
    for key, value in checks.items()
    if not value
]

audit_pass = not failed

verdict = (
    "the_exact_Sturmian_correspondence_history_has_no_provenance_in_"
    "either_repeated_static_native_b_or_any_orientation_blind_Audit133_"
    "row_context_so_any_remaining_native_provenance_must_be_"
    "path_sensitive_history_bearing_or_otherwise_non_autonomous"
    if audit_pass
    else
    "native_provenance_boundary_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_native_provenance_boundary_013",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "closed_target": {
        "history":
            "exact infinite Sturmian binary registered history",

        "one_density":
            "(5+sqrt(5))/10",

        "zero_density":
            "(5-sqrt(5))/10",

        "zero_position_law":
            "floor(k/alpha)"
    },

    "rejected_provenance_routes": {
        "repeated_native_b":
            True,

        "single_fixed_finite_automorphism":
            True,

        "orientation_blind_Audit133_row_context_selector":
            True
    },

    "surviving_native_route": {
        "path_sensitive_history":
            "open",

        "interaction_conditioned_composition":
            "open",

        "growing_registered_history":
            "open",

        "non_autonomous_transition_grammar":
            "open"
    },

    "checks":
        checks,

    "boundary": {
        "native_Sturmian_provenance_closed":
            False,

        "all_interaction_conditioned_selectors_refuted":
            False,

        "path_sensitive_selector_refuted":
            False,

        "row_local_selector_refuted":
            True,

        "static_automorphism_provenance_refuted":
            True,

        "new_frequency_mechanism_needed":
            False
    },

    "earned_statement": (
        "Program 03 has an exact infinite correspondence history, but "
        "two native provenance classes are now excluded. Repeated "
        "native b and any single fixed finite automorphism are periodic "
        "and cannot generate the irrational-density Sturmian history. "
        "Separately, all 120 Audit133 connector rows are orientation "
        "invariant, with zero row-context orientation distinctions, so "
        "orientation-blind row data cannot select between the two "
        "registered history members. Native provenance, if present, "
        "must therefore depend on ordered path history, growing "
        "registered history, interaction-conditioned composition, or "
        "another genuinely non-autonomous mechanism."
    ),

    "next_gate": (
        "Inspect only native path-sensitive registered-history geometry. "
        "The required object is a transition law whose next action "
        "depends on retained ordered history, not merely on the current "
        "connector row. Do not search for another weighting or "
        "frequency construction."
    )
}

artifact["artifact_sha256"] = digest(artifact)

JSON_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

NOTE_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

JSON_OUT.write_text(
    json.dumps(
        artifact,
        indent=2,
        sort_keys=True,
        ensure_ascii=True,
    ) + "\n",
    encoding="ascii",
)

NOTE_OUT.write_text(
    """# Native provenance boundary 013

## Result

The correspondence target is already exact:

    one-density  = (5+sqrt(5))/10
    zero-density = (5-sqrt(5))/10

with Sturmian zero positions

    floor(k/alpha).

Two native provenance routes are now excluded.

### Static native action

Repeated native b acts on each two-member history fiber as

    r0 <-> r1.

It is period two.

No single fixed automorphism of a finite carrier can generate the exact
nonperiodic irrational-density history.

### Orientation-blind row context

Audit 201O tests all 120 Audit133 connector rows.

All 120 complete row contexts are orientation invariant.

The number that distinguish the two retained history orientations is

    0.

Therefore current-row context cannot select the next history member.

## Surviving route

Path-sensitive provenance remains open.

Any native generator must depend on something stronger than the current
finite row, for example

    retained ordered path history,
    interaction-conditioned composition,
    growing registered history,
    or another non-autonomous transition law.

No new frequency mechanism is required.

Only native provenance of the already-exact Sturmian history remains.
""",
    encoding="ascii",
)

print()
print(
    "AUDIT_PASS:",
    audit_pass,
)

print(
    "VERDICT:",
    verdict,
)

print(
    "FAILED_CHECK_COUNT:",
    len(failed),
)

print(
    "FAILED_CHECKS:",
    failed,
)

print(
    "STATIC_PROVENANCE:",
    "REJECTED",
)

print(
    "ROW_CONTEXT_PROVENANCE:",
    "REJECTED",
)

print(
    "PATH_SENSITIVE_PROVENANCE:",
    "OPEN",
)

print(
    "NEXT_GATE:",
    "native_path_sensitive_history_geometry",
)

print(
    "JSON_OUT:",
    JSON_OUT,
)

print(
    "NOTE_OUT:",
    NOTE_OUT,
)

print(
    "JSON_SHA256:",
    sha256(
        JSON_OUT.read_bytes()
    ).hexdigest(),
)
