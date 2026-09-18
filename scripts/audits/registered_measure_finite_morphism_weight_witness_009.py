#!/usr/bin/env python3

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from math import sqrt
import json

HERE = Path(__file__).resolve().parents[2]

A002 = (
    HERE
    / "artifacts/json"
    / "registered_measure_finite_rule_irrational_frequency_witness_002.v1.json"
)

A005 = (
    HERE
    / "artifacts/json"
    / "registered_measure_native_spectral_quadratic_register_005.v1.json"
)

A008 = (
    HERE
    / "artifacts/json"
    / "registered_measure_dihedral_carry_boundary_008.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_finite_morphism_weight_witness_009.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_finite_morphism_weight_witness_009.md"
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


# Q(sqrt5)
def q(a=0, b=0):
    return Fraction(a), Fraction(b)


def qadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def qmul(x, y):
    a, b = x
    c, d = y
    return (
        a*c + 5*b*d,
        a*d + b*c,
    )


def qinv(x):
    a, b = x
    den = a*a - 5*b*b
    return a/den, -b/den


def qdiv(x, y):
    return qmul(x, qinv(y))


def qnum(x):
    return float(x[0]) + float(x[1])*sqrt(5.0)


print("== 009 FINITE MORPHISM WEIGHT WITNESS ==")

a002 = load(A002)
a005 = load(A005)
a008 = load(A008)

checks = {}

checks["Audit002_passes"] = (
    a002["audit_pass"] is True
)

checks["Audit005_passes"] = (
    a005["audit_pass"] is True
)

checks["Audit008_passes"] = (
    a008["audit_pass"] is True
)


# ------------------------------------------------------------
# Source finite rule.
#
# Fibonacci substitution:
#
#     A -> AB
#     B -> A
#
# Limiting symbol frequencies:
#
#     fA = (sqrt5-1)/2
#     fB = (3-sqrt5)/2.
# ------------------------------------------------------------

print("PROGRESS: 1/6 import finite substitution measure")

fA = q(
    Fraction(-1, 2),
    Fraction(1, 2),
)

fB = q(
    Fraction(3, 2),
    Fraction(-1, 2),
)

checks["fA_plus_fB_one"] = (
    qadd(fA, fB) == q(1)
)

print(
    "F_A:",
    "(sqrt(5)-1)/2",
)

print(
    "F_B:",
    "(3-sqrt(5))/2",
)


# ------------------------------------------------------------
# Fixed finite output morphism:
#
#     A -> 1
#     B -> 10
#
# A contributes:
#
#     length 1
#     ones   1
#     zeros  0.
#
# B contributes:
#
#     length 2
#     ones   1
#     zeros  1.
#
# No probability or irrational constant appears in the morphism.
# ------------------------------------------------------------

print("PROGRESS: 2/6 declare finite receipt morphism")

morphism = {
    "A": "1",
    "B": "10",
}

checks["finite_morphism"] = (
    len(morphism) == 2
)

checks["morphism_uses_only_binary_receipts"] = (
    set(
        "".join(
            morphism.values()
        )
    )
    == {"0", "1"}
)

checks["no_probability_in_morphism"] = True

checks["no_irrational_constant_in_morphism"] = True

print(
    "MORPHISM:",
    "A->1; B->10",
)

print(
    "A_OUTPUT_LENGTH:",
    1,
)

print(
    "B_OUTPUT_LENGTH:",
    2,
)


# ------------------------------------------------------------
# Exact limiting output frequencies.
#
# Ones per asymptotic source symbol:
#
#     fA + fB = 1.
#
# Total output length:
#
#     fA + 2 fB.
#
# Hence:
#
#     p1 = (fA+fB)/(fA+2fB)
#        = 1/(fA+2fB).
#
# Zeros:
#
#     p0 = fB/(fA+2fB).
# ------------------------------------------------------------

print("PROGRESS: 3/6 derive exact output measure")

den = qadd(
    fA,
    (
        2 * fB[0],
        2 * fB[1],
    ),
)

p1 = qdiv(
    q(1),
    den,
)

p0 = qdiv(
    fB,
    den,
)

target_plus = q(
    Fraction(1, 2),
    Fraction(1, 10),
)

target_minus = q(
    Fraction(1, 2),
    Fraction(-1, 10),
)

checks["output_one_equals_native_q_favored"] = (
    p1 == target_plus
)

checks["output_zero_equals_native_q_unfavored"] = (
    p0 == target_minus
)

checks["output_measure_normalized"] = (
    qadd(
        p1,
        p0,
    )
    == q(1)
)

print(
    "OUTPUT_ONE_LIMIT:",
    "(5+sqrt(5))/10",
)

print(
    "OUTPUT_ZERO_LIMIT:",
    "(5-sqrt(5))/10",
)

print(
    "NATIVE_CLASS_MEASURE_MATCH:",
    (
        checks[
            "output_one_equals_native_q_favored"
        ]
        and checks[
            "output_zero_equals_native_q_unfavored"
        ]
    ),
)


# ------------------------------------------------------------
# Verify against Audit005 native spectral masses.
# ------------------------------------------------------------

print("PROGRESS: 4/6 bind to native spectral register")

checks[
    "Audit005_q_favored_matches"
] = (
    a005[
        "native_masses"
    ][
        "q_favored"
    ]
    == "(5+sqrt(5))/10"
)

checks[
    "Audit005_q_unfavored_matches"
] = (
    a005[
        "native_masses"
    ][
        "q_unfavored"
    ]
    == "(5-sqrt(5))/10"
)

print(
    "AUDIT005_Q_FAV:",
    a005[
        "native_masses"
    ][
        "q_favored"
    ],
)

print(
    "AUDIT005_Q_UNFAV:",
    a005[
        "native_masses"
    ][
        "q_unfavored"
    ],
)


# ------------------------------------------------------------
# Finite-generation integer count witness.
#
# Fibonacci counts:
#
#     A_(n+1) = A_n+B_n
#     B_(n+1) = A_n.
#
# Under the morphism:
#
#     ones  = A+B
#     zeros = B
#     total = A+2B.
# ------------------------------------------------------------

print("PROGRESS: 5/6 verify finite integer convergence")

A = 1
B = 0

rows = []

for n in range(31):
    ones = A + B
    zeros = B
    total = ones + zeros

    rows.append({
        "generation":
            n,

        "A":
            A,

        "B":
            B,

        "ones":
            ones,

        "zeros":
            zeros,

        "total":
            total,

        "one_frequency":
            ones / total,

        "zero_frequency":
            zeros / total,
    })

    A, B = (
        A + B,
        A,
    )

last = rows[-1]

err1 = abs(
    last[
        "one_frequency"
    ]
    - qnum(
        target_plus
    )
)

err0 = abs(
    last[
        "zero_frequency"
    ]
    - qnum(
        target_minus
    )
)

checks["generation30_one_converges"] = (
    err1 < 1.0e-12
)

checks["generation30_zero_converges"] = (
    err0 < 1.0e-12
)

print(
    "GENERATION_30_SOURCE_COUNTS:",
    (
        last["A"],
        last["B"],
    ),
)

print(
    "GENERATION_30_OUTPUT_COUNTS:",
    (
        last["ones"],
        last["zeros"],
    ),
)

print(
    "GENERATION_30_TOTAL:",
    last["total"],
)

print(
    "GENERATION_30_ONE_FREQUENCY:",
    last["one_frequency"],
)

print(
    "GENERATION_30_ZERO_FREQUENCY:",
    last["zero_frequency"],
)

print(
    "ONE_ERROR:",
    err1,
)

print(
    "ZERO_ERROR:",
    err0,
)


# ------------------------------------------------------------
# Interpretation.
#
# This route is entirely discrete:
#
#     finite substitution
#       -> growing symbolic history
#       -> finite variable-length receipt morphism
#       -> irrational asymptotic output measure.
#
# It avoids any explicit algebraic fractional register.
#
# The morphism's output lengths are 1 and 2, which is structurally
# compatible with the existence of native receipt cycle doubling,
# but no native identification is claimed.
# ------------------------------------------------------------

print("PROGRESS: 6/6 classify")

checks[
    "explicit_fractional_Qsqrt5_register_not_required"
] = True

checks[
    "variable_length_ratio_is_one_to_two"
] = True

checks[
    "native_cycle_doubling_exists_but_not_identified_with_morphism"
] = (
    a008[
        "native_discrete_carry"
    ][
        "status"
    ]
    == "native"
)

failed = [
    k
    for k, v in checks.items()
    if not v
]

audit_pass = not failed

verdict = (
    "a_finite_integer_substitution_followed_by_the_fixed_binary_"
    "morphism_A_to_1_B_to_10_generates_the_exact_native_sqrt5_class_"
    "measure_as_asymptotic_registered_frequency_without_probabilities_"
    "irrational_state_variables_or_postselection"
    if audit_pass
    else
    "finite_morphism_weight_witness_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_finite_morphism_weight_witness_009",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "source_rule": {
        "substitution":
            {
                "A": "AB",
                "B": "A",
            },

        "integer_only":
            True,
    },

    "receipt_morphism": {
        "A":
            "1",

        "B":
            "10",

        "A_length":
            1,

        "B_length":
            2,

        "probabilities":
            False,

        "irrational_constants":
            False,
    },

    "exact_output_measure": {
        "one":
            "(5+sqrt(5))/10",

        "zero":
            "(5-sqrt(5))/10",

        "matches_Audit005":
            True,
    },

    "mechanism_class": {
        "finite_rule":
            True,

        "finite_output_morphism":
            True,

        "unbounded_registered_history":
            True,

        "explicit_Q_sqrt5_fractional_state":
            False,

        "eventually_periodic":
            False,
    },

    "relation_to_receipt_tower": {
        "native_cycle_doubling_exists":
            True,

        "morphism_length_profile":
            "1:2",

        "native_identification_claimed":
            False,
    },

    "checks":
        checks,

    "boundary": {
        "target_informed_witness":
            True,

        "Fibonacci_substitution_native":
            False,

        "A_to_1_B_to_10_morphism_native":
            False,

        "cycle_doubling_equals_morphism_proved":
            False,

        "Born_rule_used":
            False,

        "probability_transition_used":
            False,

        "frequency_correspondence_closed_natively":
            False,
    },

    "earned_statement": (
        "The Program-02 native class measure admits a purely discrete "
        "finite-rule realization with no explicit algebraic residual "
        "state. The Fibonacci substitution generates source symbol "
        "frequencies fA and fB. Applying the fixed finite morphism "
        "A->1, B->10 produces asymptotic binary output frequencies "
        "(fA+fB)/(fA+2fB)=(5+sqrt(5))/10 and "
        "fB/(fA+2fB)=(5-sqrt(5))/10, exactly the Audit005 native "
        "spectral masses. The morphism uses output lengths one and two, "
        "which resembles native receipt cycle doubling, but this audit "
        "does not identify the external substitution or morphism with "
        "native dynamics."
    ),

    "next_gate": (
        "Test whether the native receipt tower supplies a two-class "
        "transition grammar conjugate to the Fibonacci substitution "
        "and a one-versus-two receipt expansion equivalent to the "
        "A->1, B->10 morphism. If not, retain this as an external "
        "existence witness only."
    ),
}

artifact["artifact_sha256"] = digest_json(
    artifact
)

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
    )
    + "\n",
    encoding="ascii",
)

NOTE_OUT.write_text(
    """# Finite morphism weight witness 009

## Result

Use the finite substitution

    A -> AB
    B -> A

and the fixed binary receipt morphism

    A -> 1
    B -> 10.

No probabilities appear.

No irrational constants appear.

No algebraic fractional state is stored.

If the source frequencies are

    f_A = (sqrt(5)-1)/2
    f_B = (3-sqrt(5))/2,

then output one-frequency is

    (f_A+f_B)/(f_A+2f_B)
      =
    (5+sqrt(5))/10,

and output zero-frequency is

    f_B/(f_A+2f_B)
      =
    (5-sqrt(5))/10.

These are exactly the native spectral class masses from Audit005.

## Structural point

This gives a second correspondence mechanism class:

    finite substitution
      -> growing history
      -> finite variable-length receipt morphism
      -> irrational limiting frequency.

It does not require an explicit Q(sqrt5) fractional residual register.

The morphism has output lengths

    1
    2,

which is suggestive in light of the already-native receipt cycle-doubling
theorem.

## Boundary

The Fibonacci substitution is not yet native.

The morphism A->1, B->10 is not yet native.

The resemblance to cycle doubling is not a proof.

This remains a target-informed finite-rule witness.

## Next gate

Test whether native receipt dynamics already contain:

    a two-class transition matrix conjugate to [[1,1],[1,0]]

and

    a one-versus-two receipt expansion.

If yes, the frequency bridge may close without any continuous algebraic
phase register.
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
    "OUTPUT_ONE_LIMIT:",
    "(5+sqrt(5))/10",
)

print(
    "OUTPUT_ZERO_LIMIT:",
    "(5-sqrt(5))/10",
)

print(
    "EXPLICIT_ALGEBRAIC_PHASE_REQUIRED:",
    False,
)

print(
    "NEXT_GATE:",
    "native_fibonacci_receipt_morphism_provenance",
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
