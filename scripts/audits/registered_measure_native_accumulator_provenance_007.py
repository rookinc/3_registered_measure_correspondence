#!/usr/bin/env python3

from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parents[2]

A006 = (
    HERE
    / "artifacts/json"
    / "registered_measure_bounded_residual_frequency_witness_006.v1.json"
)

HIST = (
    HERE
    / "source"
    / "registered_history_native_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_native_accumulator_provenance_007.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_native_accumulator_provenance_007.md"
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest_json(obj):
    raw = json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return sha256(raw).hexdigest()


print("== 007 NATIVE ACCUMULATOR PROVENANCE ==")

a006 = load(A006)
hist = load(HIST)

checks = {}

checks["Audit006_passes"] = (
    a006["audit_pass"] is True
)

checks["history_interface_sealed"] = (
    hist["status"] == "sealed_prior_theorem_interface"
)


# ------------------------------------------------------------
# Primitive 1: additive accumulation.
# ------------------------------------------------------------

print("PROGRESS: 1/5 additive accumulation")

additive_native = (
    hist[
        "results"
    ][
        "additive_time_coordinate"
    ][
        "integer_extension"
    ]
    == "tau(n gamma_r1)=n"
)

checks[
    "additive_integer_history_native"
] = additive_native

print(
    "ADDITIVE_ACCUMULATION:",
    "NATIVE" if additive_native else "OPEN",
)

print(
    "NATIVE_LAW:",
    "tau(n gamma_r1)=n",
)


# ------------------------------------------------------------
# Primitive 2: closure boundary.
# ------------------------------------------------------------

print("PROGRESS: 2/5 closure boundary")

closure_native = (
    hist[
        "results"
    ][
        "visible_closure"
    ][
        "statement"
    ]
    == "visible registration closes after two exchanges"
)

checks[
    "registration_closure_boundary_native"
] = closure_native

print(
    "CLOSURE_BOUNDARY:",
    "NATIVE" if closure_native else "OPEN",
)

print(
    "VISIBLE_CLOSURE:",
    "two exchanges",
)

print(
    "FULL_EXCHANGE_CLOSURE:",
    "four exchanges",
)


# ------------------------------------------------------------
# Primitive 3: retained residual/history.
# ------------------------------------------------------------

print("PROGRESS: 3/5 retained residual")

residual_native = (
    hist[
        "results"
    ][
        "residual_descent"
    ][
        "statement"
    ]
    == "D_a(g^2)=r1"
)

retention_native = (
    hist[
        "results"
    ][
        "finer_history_retention"
    ][
        "statement"
    ]
    == "registered-history surface remains displaced after visible closure"
)

checks[
    "retained_registered_residual_native"
] = (
    residual_native
    and retention_native
)

print(
    "RETAINED_RESIDUAL:",
    (
        "NATIVE"
        if checks[
            "retained_registered_residual_native"
        ]
        else "OPEN"
    ),
)

print(
    "RESIDUAL:",
    "r1 = D_a(g^2)",
)


# ------------------------------------------------------------
# Primitive 4: thresholded integer receipt emission.
#
# Audit006 requires:
#
#     t = r + mu
#
#     if t >= 1:
#         emit one receipt
#         retain t-1
#
# The prior registered-history theorems establish primitive integer
# winding and retained residual, but do not establish this exact
# normalized threshold rule for algebraic measure accumulation.
# ------------------------------------------------------------

print("PROGRESS: 4/5 thresholded receipt emission")

threshold_native = not (
    hist[
        "boundary"
    ][
        "thresholded_measure_receipt_rule_identified"
    ]
    is False
)

bounded_fractional_native = not (
    hist[
        "boundary"
    ][
        "bounded_fractional_residual_accumulator_identified"
    ]
    is False
)

checks[
    "threshold_rule_correctly_left_open"
] = (
    threshold_native is False
)

checks[
    "bounded_fractional_residual_correctly_left_open"
] = (
    bounded_fractional_native is False
)

print(
    "THRESHOLDED_MEASURE_RECEIPT:",
    "OPEN",
)

print(
    "BOUNDED_FRACTIONAL_RESIDUAL:",
    "OPEN",
)


# ------------------------------------------------------------
# Classification.
# ------------------------------------------------------------

print("PROGRESS: 5/5 classify")

failed = [
    name
    for name, passed
    in checks.items()
    if not passed
]

audit_pass = not failed

native_primitive_count = sum([
    additive_native,
    closure_native,
    (
        residual_native
        and retention_native
    ),
])

verdict = (
    "three_of_four_bounded_residual_frequency_primitives_are_already_"
    "native_to_registered_history_mechanics_and_the_only_missing_"
    "operation_is_normalized_thresholded_measure_receipt_emission_"
    "with_bounded_fractional_residual"
    if audit_pass
    else
    "native_accumulator_provenance_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_native_accumulator_provenance_007",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "Audit006_required_primitives": {
        "additive_accumulation": {
            "status":
                "native",

            "native_interface":
                "tau(n gamma_r1)=n"
        },

        "closure_boundary": {
            "status":
                "native",

            "native_interface":
                (
                    "visible registration closes after two exchanges "
                    "while full exchange closure requires four"
                )
        },

        "retained_residual": {
            "status":
                "native",

            "native_interface":
                "r1=D_a(g^2)"
        },

        "thresholded_integer_receipt_emission": {
            "status":
                "open",

            "required_rule":
                (
                    "add algebraic measure; emit one integer receipt "
                    "at normalized unit crossing; retain fractional "
                    "residual"
                )
        }
    },

    "native_primitive_count":
        native_primitive_count,

    "required_primitive_count":
        4,

    "remaining_native_gate": {
        "name":
            "normalized_thresholded_measure_receipt",

        "must_supply": [
            "normalized unit boundary",
            "measure accumulation below boundary",
            "one integer receipt at crossing",
            "fractional residual retained after crossing"
        ]
    },

    "checks":
        checks,

    "boundary": {
        "Audit006_promoted_to_native_law":
            False,

        "additive_history_native":
            True,

        "registration_closure_native":
            True,

        "retained_residual_history_native":
            True,

        "threshold_measure_rule_native":
            False,

        "frequency_correspondence_closed":
            False
    },

    "earned_statement": (
        "The bounded-residual frequency witness is not an arbitrary "
        "foreign grammar. Three of its four structural primitives are "
        "already present in the registered-history theory: additive "
        "integer winding tau, a registration closure boundary, and a "
        "retained nontrivial residual r1 after visible closure. What is "
        "not yet established is the specific measure-transduction law "
        "that accumulates an algebraic weight against a normalized unit "
        "boundary, emits one integer receipt at crossing, and retains "
        "the fractional remainder. Program 03 therefore has one "
        "precise native provenance gate rather than a general frequency "
        "mystery."
    ),

    "next_gate": (
        "Search only for a native normalized threshold operation in "
        "the existing receipt/cycle machinery. Do not search for new "
        "weighting laws or alternative irrational generators."
    )
}

artifact["artifact_sha256"] = digest_json(artifact)

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

note = """# Native accumulator provenance 007

## Result

Audit006 requires four primitives:

    additive accumulation
    closure boundary
    retained residual
    thresholded integer receipt emission.

Three are already native.

### Additive accumulation

Registered history has the primitive winding coordinate

    tau(gamma_r1)=1

and

    tau(n gamma_r1)=n.

### Closure boundary

Visible registration closes after two exchanges.

Full exchange closure requires four.

### Retained residual

The visible two-step closure retains

    r1 = D_a(g^2),

and the finer registered-history surface remains displaced.

### Missing primitive

The exact Audit006 measure rule is not yet native:

    r <- r + mu

followed by

    emit one integer receipt iff r >= 1

and retain

    r <- r - 1.

No existing sealed theorem yet identifies a normalized fractional measure
register with this threshold behavior.

## Conclusion

The frequency bridge is now reduced to one native gate:

    normalized thresholded measure receipt.

Do not reopen source weighting, Fibonacci provenance, or visibility.
"""

NOTE_OUT.write_text(
    note,
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
    "NATIVE_PRIMITIVES:",
    str(native_primitive_count) + "/4",
)

print(
    "MISSING_PRIMITIVE:",
    "normalized_thresholded_measure_receipt",
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
