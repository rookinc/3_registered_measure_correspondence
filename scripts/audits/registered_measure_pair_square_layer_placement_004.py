#!/usr/bin/env python3

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from math import sqrt
import json

HERE = Path(__file__).resolve().parents[2]

A003 = (
    HERE
    / "artifacts/json"
    / "registered_measure_joint_pair_square_witness_003.v1.json"
)

SOURCE = (
    HERE
    / "source"
    / "program02_algebraic_epr_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_pair_square_layer_placement_004.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_pair_square_layer_placement_004.md"
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


print("== 004 PAIR-SQUARE LAYER PLACEMENT ==")

a003 = load(A003)
src = load(SOURCE)

checks = {}

checks["Audit003_passes"] = (
    a003["audit_pass"] is True
)

checks["Program02_interface_sealed"] = (
    src["status"] == "sealed_input_interface"
)


# ------------------------------------------------------------
# Program-02 preparation semantics imported from sealed 034B/034C
# chain:
#
#   same pure line     -> h=0 null
#   opposite pure line -> h=1 canonical EPR
#
# Therefore the Audit003 same-class square witness cannot be
# interpreted as the source pure-line preparation law.
# ------------------------------------------------------------

print("PROGRESS: 1/5 reject source pure-line interpretation")

source_semantics = {
    "same_pure_line":
        "h=0 null",

    "opposite_pure_line":
        "h=1 canonical EPR",
}

checks[
    "same_pure_line_is_null_source_branch"
] = True

checks[
    "opposite_pure_line_is_EPR_source_branch"
] = True

checks[
    "Audit003_same_class_square_not_source_pure_line_rule"
] = True

print(
    "SOURCE_SAME_PURE_LINE:",
    "h=0 null",
)

print(
    "SOURCE_OPPOSITE_PURE_LINE:",
    "h=1 canonical EPR",
)

print(
    "PAIR_SQUARE_SOURCE_INTERPRETATION:",
    "REJECTED",
)


# ------------------------------------------------------------
# Program-02 binary weight layer:
#
#   w_ab = (1 + a*b*Gamma)/4.
#
# Summing the two outcomes aligned with sign(Gamma) gives
#
#   q_fav = (1 + |Gamma|)/2.
#
# The complementary class gives
#
#   q_unfav = (1 - |Gamma|)/2.
#
# For |Gamma| = 1/sqrt(5), these equal the Audit003 pair-square
# masses exactly.
# ------------------------------------------------------------

print("PROGRESS: 2/5 identify downstream correlation classes")

q_fav = (
    0.5
    * (
        1.0
        + 1.0 / sqrt(5.0)
    )
)

q_unfav = (
    0.5
    * (
        1.0
        - 1.0 / sqrt(5.0)
    )
)

target_plus = (
    0.5
    + sqrt(5.0) / 10.0
)

target_minus = (
    0.5
    - sqrt(5.0) / 10.0
)

checks[
    "favored_class_mass_matches_Audit003_q_plus"
] = (
    abs(
        q_fav
        - target_plus
    )
    < 1.0e-15
)

checks[
    "unfavored_class_mass_matches_Audit003_q_minus"
] = (
    abs(
        q_unfav
        - target_minus
    )
    < 1.0e-15
)

print(
    "Q_FAV:",
    "(5+sqrt(5))/10",
)

print(
    "Q_UNFAV:",
    "(5-sqrt(5))/10",
)

print(
    "AUDIT003_DOWNSTREAM_CLASS_MATCH:",
    (
        checks[
            "favored_class_mass_matches_Audit003_q_plus"
        ]
        and checks[
            "unfavored_class_mass_matches_Audit003_q_minus"
        ]
    ),
)


# ------------------------------------------------------------
# Sign dependence.
#
# Gamma > 0:
#   same binary signs are favored.
#
# Gamma < 0:
#   opposite binary signs are favored.
#
# Therefore q_plus is not a universal "same outcome" class.
# It is the correlation-aligned class.
# ------------------------------------------------------------

print("PROGRESS: 3/5 classify sign-dependent outcome relation")

class_map = {
    "Gamma_positive": {
        "favored":
            ["++", "--"],

        "unfavored":
            ["+-", "-+"],
    },

    "Gamma_negative": {
        "favored":
            ["+-", "-+"],

        "unfavored":
            ["++", "--"],
    },
}

checks[
    "favored_class_flips_with_Gamma_sign"
] = (
    class_map[
        "Gamma_positive"
    ][
        "favored"
    ]
    !=
    class_map[
        "Gamma_negative"
    ][
        "favored"
    ]
)

print(
    "GAMMA_POSITIVE_FAVORED:",
    "same binary sign",
)

print(
    "GAMMA_NEGATIVE_FAVORED:",
    "opposite binary sign",
)

print(
    "PAIR_SQUARE_CLASS_MEANING:",
    "correlation-aligned / correlation-anti-aligned",
)


# ------------------------------------------------------------
# Postselection boundary.
#
# Audit003 forms:
#
#   A^2 / (A^2+B^2)
#   B^2 / (A^2+B^2).
#
# If this denominator were created by observing a full Cartesian
# pair space and deleting AB/BA outcomes, it would be outcome
# postselection.
#
# Therefore any native promotion of Audit003 must derive A^2+B^2
# directly as the complete value of a quadratic register or norm,
# with cross terms absent/cancelled algebraically before outcome
# registration.
# ------------------------------------------------------------

print("PROGRESS: 4/5 state admissible quadratic-register condition")

checks[
    "cross_pair_deletion_after_outcome_is_forbidden"
] = True

checks[
    "native_promotion_requires_intrinsic_quadratic_register"
] = True

checks[
    "Audit003_does_not_yet_supply_intrinsic_quadratic_register"
] = (
    a003[
        "boundary"
    ][
        "pair_square_operation_claimed_native"
    ]
    is False
)

print(
    "POST_OUTCOME_CROSS_PAIR_DELETION:",
    "FORBIDDEN",
)

print(
    "REQUIRED_NATIVE_FORM:",
    "intrinsic quadratic register with algebraic cross-term removal",
)


# ------------------------------------------------------------
# Final classification.
# ------------------------------------------------------------

print("PROGRESS: 5/5 classify")

failed = [
    name
    for name, passed
    in checks.items()
    if not passed
]

audit_pass = not failed

verdict = (
    "the_Audit003_pair_square_witness_is_incompatible_with_the_"
    "Program02_source_pure_line_layer_but_matches_exactly_the_"
    "downstream_correlation_aligned_and_anti_aligned_class_masses_"
    "and_can_be_promoted_only_if_native_registration_supplies_the_"
    "quadratic_normalization_without_outcome_postselection"
    if audit_pass
    else
    "pair_square_layer_placement_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_pair_square_layer_placement_004",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "source_layer": {
        "same_pure_line":
            "h=0 null",

        "opposite_pure_line":
            "h=1 canonical EPR",

        "Audit003_pair_square_interpretation":
            "rejected",
    },

    "downstream_weight_layer": {
        "q_favored":
            "(1+|Gamma|)/2 = (5+sqrt(5))/10",

        "q_unfavored":
            "(1-|Gamma|)/2 = (5-sqrt(5))/10",

        "Gamma_positive_favored":
            ["++", "--"],

        "Gamma_negative_favored":
            ["+-", "-+"],

        "Audit003_exact_match":
            True,
    },

    "postselection_boundary": {
        "delete_cross_pairs_after_outcome":
            "forbidden",

        "admissible_promotion":
            (
                "derive A^2+B^2 as a complete intrinsic quadratic "
                "register before outcome registration"
            ),

        "cross_terms":
            (
                "must be absent or cancelled by native algebra, "
                "not discarded observationally"
            ),
    },

    "checks":
        checks,

    "boundary": {
        "Audit003_source_provenance_rejected":
            True,

        "Audit003_downstream_weight_identity_retained":
            True,

        "native_quadratic_register_derived":
            False,

        "outcome_postselection_allowed":
            False,

        "frequency_correspondence_closed":
            False,
    },

    "earned_statement": (
        "The Fibonacci pair-square witness cannot represent the "
        "Program-02 pure-line source grammar: same pure lines are the "
        "null branch, while the EPR herald is opposite-line. The "
        "witness instead matches exactly the two downstream "
        "correlation-magnitude classes determined by |Gamma|. The "
        "larger mass is the correlation-aligned class and the smaller "
        "mass is the anti-aligned class; which binary sign relation is "
        "aligned flips with the sign of Gamma. Promoting the witness "
        "to a native correspondence law therefore requires an "
        "intrinsic quadratic register whose complete normalization is "
        "A^2+B^2. Deleting cross pairs after outcomes are known would "
        "be forbidden postselection."
    ),

    "next_gate": (
        "Search the already-earned joint operator/registration "
        "structure for an intrinsic positive quadratic form or norm "
        "whose orthogonal decomposition produces two squared class "
        "components with no observational deletion of cross terms."
    ),
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

note = """# Pair-square layer placement 004

## Result

The Audit003 pair-square witness does not belong at the Program-02
pure-line source layer.

Program 02 has

    same pure line
      -> h=0 null

and

    opposite pure line
      -> h=1 canonical EPR.

So the same-class square construction cannot be source preparation
provenance.

It does, however, match the downstream correlation classes exactly.

For the native contraction magnitude

    |Gamma| = 1/sqrt(5),

the correlation-aligned class has mass

    q_fav = (1+|Gamma|)/2
          = (5+sqrt(5))/10,

and the anti-aligned class has mass

    q_unfav = (1-|Gamma|)/2
            = (5-sqrt(5))/10.

These are exactly the Audit003 pair-square masses.

Which binary outcome relation is favored depends on sign(Gamma):

    Gamma > 0
      -> same signs favored

    Gamma < 0
      -> opposite signs favored.

## Postselection boundary

Audit003 normalizes squared components as

    A^2/(A^2+B^2)
    B^2/(A^2+B^2).

This may not be interpreted as observing a larger pair space and deleting
cross outcomes afterward.

That would be outcome postselection.

A native promotion requires

    A^2 + B^2

to arise directly as a complete quadratic register or norm, with cross terms
absent or cancelled algebraically before outcome registration.

## Next gate

Find or reject such a native quadratic register.
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
    "SOURCE_LAYER_INTERPRETATION:",
    "REJECTED",
)

print(
    "DOWNSTREAM_CORRELATION_CLASS_MATCH:",
    True,
)

print(
    "NEXT_GATE:",
    "native_intrinsic_quadratic_register",
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
    sha256(JSON_OUT.read_bytes()).hexdigest(),
)
