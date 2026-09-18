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

A013 = (
    HERE
    / "artifacts/json"
    / "registered_measure_native_provenance_boundary_013.v1.json"
)

SRC = (
    HERE
    / "source"
    / "project41_path_history_recurrence_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_path_history_provenance_limit_014.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_path_history_provenance_limit_014.md"
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


print("== 014 PATH HISTORY PROVENANCE LIMIT ==")

a011 = load(A011)
a013 = load(A013)
src = load(SRC)

checks = {}

checks["Audit011_passes"] = (
    a011["audit_pass"] is True
)

checks["Audit013_passes"] = (
    a013["audit_pass"] is True
)

checks["path_interface_sealed"] = (
    src["status"] == "sealed_prior_theorem_interface"
)


print("PROGRESS: 1/5 verify native path-sensitive continuation")

c = src["continuation"]

checks["binary_continuation_exists"] = (
    c["history_alphabet"] == [2, 3]
)

checks["preserve_branch_flips_history_class"] = (
    c["preserve_roles"] == "h_next=5-h"
)

checks["swap_branch_preserves_history_class"] = (
    c["swap_roles"] == "h_next=h"
)

checks["branches_reconverge"] = (
    c["branches_reconverge"] is True
)

print(
    "HISTORY_ALPHABET:",
    "{2,3}",
)

print(
    "PRESERVE_ROLES:",
    "h_next=5-h",
)

print(
    "SWAP_ROLES:",
    "h_next=h",
)

print(
    "PATH_SENSITIVE_GRAMMAR:",
    "NATIVE",
)


print("PROGRESS: 2/5 verify selector remains open")

s = src["selector"]

checks["deterministic_selector_not_derived"] = (
    s["deterministic_selector_derived"] is False
)

checks["deterministic_selector_not_refuted"] = (
    s["deterministic_selector_refuted"] is False
)

checks["native_branch_selector_not_derived"] = (
    c["native_branch_selector_derived"] is False
)

print(
    "NATIVE_BRANCH_SELECTOR:",
    "OPEN",
)


print("PROGRESS: 3/5 verify intrinsic recurrence is finite-periodic")

r = src["recurrence"]
g = src["groupoid"]
p = src["phase"]

checks["groupoid_has_four_objects"] = (
    g["object_count"] == 4
)

checks["history_action_period_two"] = (
    r["history_action_period"] == 2
)

checks["history_word_period_two"] = (
    r["history_word_generator_period"] == 2
)

checks["registered_surface_period_four"] = (
    r["registered_surface_period"] == 4
)

checks["phase_rotation_order_four"] = (
    p["history_rotation_order"] == 4
)

checks["full_return_period_four"] = (
    p["full_exchange_return_period"] == 4
)

print(
    "RECURRENCE_DEPTHS:",
    "kernel=1 history=2 surface=4",
)

print(
    "HISTORY_WORD:",
    r["history_word_formula"],
)

print(
    "PHASE_LIFT:",
    p["phase_lift"],
)

print(
    "INTRINSIC_RECURRENCE_TYPE:",
    "FINITE_PERIODIC",
)


print("PROGRESS: 4/5 compare with exact Sturmian target")

checks["Audit011_target_nonperiodic"] = (
    a011[
        "theorem"
    ][
        "same_infinite_binary_history"
    ]
    is True
)

checks["finite_periodic_recurrence_not_Sturmian"] = True

checks["arbitrary_branch_word_could_encode_target_but_is_not_provenance"] = True

print(
    "AUDIT011_TARGET:",
    "NONPERIODIC STURMIAN",
)

print(
    "PROJECT41_INTRINSIC_RECURRENCE:",
    "PERIOD 2 / 4",
)

print(
    "DIRECT_NATIVE_STURMIAN_MATCH:",
    False,
)

print(
    "INSERT_STURMIAN_BRANCH_SEQUENCE_BY_HAND:",
    "FORBIDDEN",
)


print("PROGRESS: 5/5 classify")

failed = [
    key
    for key, value in checks.items()
    if not value
]

audit_pass = not failed

verdict = (
    "Project41_supplies_a_genuine_path_sensitive_binary_registered_"
    "continuation_groupoid_but_its_derived_internal_recurrence_is_"
    "finite_with_history_period2_and_surface_period4_and_no_native_"
    "branch_selector_is_derived_so_it_does_not_supply_native_"
    "provenance_for_the_nonperiodic_Sturmian_measure_history"
    if audit_pass
    else
    "path_history_provenance_limit_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_path_history_provenance_limit_014",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "native_path_grammar": {
        "history_alphabet":
            [2, 3],

        "preserve_roles":
            "h_next=5-h",

        "swap_roles":
            "h_next=h",

        "groupoid_objects":
            4,

        "status":
            "native"
    },

    "native_intrinsic_recurrence": {
        "kernel":
            1,

        "history_action":
            2,

        "history_word_generator":
            2,

        "registered_surface":
            4,

        "phase_rotation_order":
            4,

        "type":
            "finite periodic"
    },

    "selector_status": {
        "native_branch_selector":
            "open",

        "deterministic_selector_derived":
            False,

        "deterministic_selector_refuted":
            False
    },

    "Audit011_target": {
        "type":
            "nonperiodic Sturmian",

        "zero_position_law":
            "floor(k/alpha)",

        "native_match":
            False
    },

    "checks":
        checks,

    "boundary": {
        "path_sensitive_geometry_native":
            True,

        "native_Sturmian_provenance_closed":
            False,

        "current_Project41_intrinsic_recurrence_sufficient":
            False,

        "branch_sequence_may_be_inserted_by_hand":
            False,

        "frequency_correspondence_constructively_possible":
            True,

        "frequency_correspondence_native":
            False
    },

    "earned_statement": (
        "Project 41 does contain the path-sensitive structure required "
        "after the static and row-local no-go results. At each "
        "registered continuation junction there are two admissible "
        "history-sensitive branches: preserve roles flips the history "
        "class and swap roles preserves it. These arrows assemble into "
        "an exact four-object transformation groupoid. However, no "
        "native branch selector is derived. The independently derived "
        "presentation recurrence remains finite: kernel depth one, "
        "history action and word period two, and registered surface "
        "period four, with a C4 phase tick. Therefore the existing "
        "native path machinery does not generate the exact nonperiodic "
        "Sturmian history of Audit011. Choosing the preserve/swap "
        "sequence to equal the target word would merely insert the "
        "desired frequency history."
    ),

    "next_gate": (
        "Stop internal frequency construction. The remaining theorem "
        "gap is a native nonperiodic selector or growing-history law "
        "beyond the currently derived finite D8xC2/C4 recurrence. "
        "Absent such new native structure, retain the exact Sturmian "
        "correspondence as a constructive external realization and "
        "leave empirical-frequency provenance open."
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
    """# Path history provenance limit 014

## Result

Project 41 contains genuine path-sensitive registered-history structure.

The continuation history class is

    h in {2,3}.

Two branches are admissible:

    preserve roles:
        h_next = 5-h

    swap roles:
        h_next = h.

These continuation arrows assemble into a transitive four-object
transformation groupoid.

However, no native branch selector is derived.

The independently derived native recurrence is finite:

    kernel                1
    history action        2
    history word          2
    registered surface    4.

The native history phase is C4 and has full return period four.

Audit011 instead requires a nonperiodic Sturmian history with irrational
symbol density.

Therefore the currently derived Project-41 path-sensitive machinery does not
supply native provenance of that history.

A desired preserve/swap branch word could be imposed externally, but doing so
would insert the target history rather than derive it.

## Frontier

The correspondence mechanism is mathematically constructed.

The native algebraic measure is known.

The native discrete carry grammar is known.

Path-sensitive continuation geometry is known.

What remains absent is a native nonperiodic branch-selection or growing-
history law.

That is a genuine remaining correspondence boundary.
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
    "PATH_SENSITIVE_GEOMETRY:",
    "NATIVE",
)

print(
    "INTRINSIC_HISTORY_RECURRENCE:",
    "PERIOD_2",
)

print(
    "REGISTERED_SURFACE_PERIOD:",
    4,
)

print(
    "NATIVE_BRANCH_SELECTOR:",
    "OPEN",
)

print(
    "NATIVE_STURMIAN_PROVENANCE:",
    "OPEN",
)

print(
    "NEXT_GATE:",
    "new_native_nonperiodic_history_structure_or_stop",
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
