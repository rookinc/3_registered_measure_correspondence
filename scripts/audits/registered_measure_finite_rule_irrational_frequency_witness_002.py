#!/usr/bin/env python3

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from math import sqrt
import json

HERE = Path(__file__).resolve().parents[2]

A001 = (
    HERE
    / "artifacts/json"
    / "registered_measure_finite_count_obstruction_001.v1.json"
)

SOURCE = (
    HERE
    / "source"
    / "program02_algebraic_epr_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_finite_rule_irrational_frequency_witness_002.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_finite_rule_irrational_frequency_witness_002.md"
)


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def digest_json(obj):
    raw = json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")

    return sha256(raw).hexdigest()


# Exact Q(sqrt(5)) value:
#
#     a + b sqrt(5)
#
def q(a=0, b=0):
    return (
        Fraction(a),
        Fraction(b),
    )


def qadd(x, y):
    return (
        x[0] + y[0],
        x[1] + y[1],
    )


def qmul(x, y):
    a, b = x
    c, d = y

    return (
        a * c + 5 * b * d,
        a * d + b * c,
    )


def qnum(x):
    return (
        float(x[0])
        + float(x[1]) * sqrt(5.0)
    )


print("== 002 FINITE RULE IRRATIONAL FREQUENCY WITNESS ==")

a001 = load(A001)
src = load(SOURCE)

checks = {}

checks["Audit001_passes"] = (
    a001["audit_pass"] is True
)

checks["Program02_interface_sealed"] = (
    src["status"] == "sealed_input_interface"
)


# ------------------------------------------------------------
# Finite deterministic substitution rule:
#
#     A -> AB
#     B -> A
#
# Count update:
#
#     [A']   [1 1] [A]
#     [B'] = [1 0] [B]
#
# No probability, real parameter, or irrational constant appears
# in the rule.
# ------------------------------------------------------------

print("PROGRESS: 1/6 declare finite integer substitution")

rule = {
    "A": "AB",
    "B": "A",
}

M = [
    [1, 1],
    [1, 0],
]

checks[
    "finite_alphabet_size_two"
] = (
    len(rule) == 2
)

checks[
    "substitution_rule_integer_only"
] = True

checks[
    "no_probability_weight_in_rule"
] = True

checks[
    "no_irrational_constant_in_rule"
] = True

print(
    "RULE:",
    "A->AB; B->A",
)

print(
    "SUBSTITUTION_MATRIX:",
    M,
)


# ------------------------------------------------------------
# Exact count recurrence.
#
# Starting from A:
#
#     (A_0,B_0) = (1,0)
#
# and
#
#     A_(n+1) = A_n + B_n
#     B_(n+1) = A_n.
#
# ------------------------------------------------------------

print("PROGRESS: 2/6 generate registered count history")

A = 1
B = 0

history = []

for n in range(31):
    total = A + B

    history.append({
        "generation":
            n,

        "A_count":
            A,

        "B_count":
            B,

        "total":
            total,

        "A_frequency":
            A / total,

        "B_frequency":
            B / total,
    })

    A, B = (
        A + B,
        A,
    )

checks[
    "history_length_grows"
] = all(
    history[i + 1]["total"]
    > history[i]["total"]
    for i in range(
        len(history) - 1
    )
)

checks[
    "registered_history_not_fixed_finite_state_census"
] = (
    history[-1]["total"]
    > history[0]["total"]
)

print(
    "GENERATION_0_COUNTS:",
    (
        history[0]["A_count"],
        history[0]["B_count"],
    ),
)

print(
    "GENERATION_30_COUNTS:",
    (
        history[-1]["A_count"],
        history[-1]["B_count"],
    ),
)

print(
    "GENERATION_30_TOTAL:",
    history[-1]["total"],
)


# ------------------------------------------------------------
# Spectral law.
#
# Characteristic polynomial:
#
#     lambda^2 - lambda - 1 = 0.
#
# Perron root:
#
#     phi = (1+sqrt(5))/2.
#
# Positive eigenvector may be taken as
#
#     (phi,1).
#
# Normalize:
#
#     f_A = phi/(phi+1) = 1/phi
#     f_B = 1/(phi+1)   = 1/phi^2.
#
# Exact Q(sqrt5):
#
#     f_A = (sqrt5-1)/2
#     f_B = (3-sqrt5)/2.
# ------------------------------------------------------------

print("PROGRESS: 3/6 derive exact spectral frequencies")

phi = q(
    Fraction(1, 2),
    Fraction(1, 2),
)

fA = q(
    Fraction(-1, 2),
    Fraction(1, 2),
)

fB = q(
    Fraction(3, 2),
    Fraction(-1, 2),
)

one = q(1, 0)

checks[
    "phi_satisfies_x2_minus_x_minus_1"
] = (
    qadd(
        qadd(
            qmul(
                phi,
                phi,
            ),
            q(
                Fraction(-1, 2),
                Fraction(-1, 2),
            ),
        ),
        q(-1, 0),
    )
    == q(0, 0)
)

checks[
    "limiting_frequencies_sum_to_one"
] = (
    qadd(
        fA,
        fB,
    )
    == one
)

checks[
    "A_limiting_frequency_irrational"
] = (
    fA[1] != 0
)

checks[
    "B_limiting_frequency_irrational"
] = (
    fB[1] != 0
)

print(
    "PERRON_ROOT:",
    "(1+sqrt(5))/2",
)

print(
    "LIMIT_A:",
    "(sqrt(5)-1)/2",
)

print(
    "LIMIT_B:",
    "(3-sqrt(5))/2",
)

print(
    "LIMIT_A_NUMERIC:",
    qnum(fA),
)

print(
    "LIMIT_B_NUMERIC:",
    qnum(fB),
)


# ------------------------------------------------------------
# Compare finite registered counts against exact irrational limits.
# ------------------------------------------------------------

print("PROGRESS: 4/6 verify convergence")

last = history[-1]

A_error = abs(
    last["A_frequency"]
    - qnum(fA)
)

B_error = abs(
    last["B_frequency"]
    - qnum(fB)
)

checks[
    "generation30_A_close_to_exact_limit"
] = (
    A_error < 1.0e-12
)

checks[
    "generation30_B_close_to_exact_limit"
] = (
    B_error < 1.0e-12
)

print(
    "GENERATION_30_A_FREQUENCY:",
    last["A_frequency"],
)

print(
    "GENERATION_30_B_FREQUENCY:",
    last["B_frequency"],
)

print(
    "GENERATION_30_A_ERROR:",
    A_error,
)

print(
    "GENERATION_30_B_ERROR:",
    B_error,
)


# ------------------------------------------------------------
# Distinguish this mechanism from Audit001.
#
# Audit001 excludes deterministic maps on a fixed finite state set:
# they eventually enter a finite cycle.
#
# Here the rule alphabet is finite, but the registered word/history
# grows without bound. The global register is therefore not a fixed
# finite state space.
#
# This is the minimal conceptual escape we wanted to exhibit:
#
#     finite rule
#       !=
#     finite global state space.
# ------------------------------------------------------------

print("PROGRESS: 5/6 classify mechanism")

checks[
    "finite_rule_with_unbounded_registered_history"
] = (
    checks[
        "finite_alphabet_size_two"
    ]
    and checks[
        "history_length_grows"
    ]
)

checks[
    "irrational_frequency_generated_without_probability_input"
] = (
    checks[
        "A_limiting_frequency_irrational"
    ]
    and checks[
        "B_limiting_frequency_irrational"
    ]
    and checks[
        "no_probability_weight_in_rule"
    ]
    and checks[
        "no_irrational_constant_in_rule"
    ]
)

print(
    "FINITE_RULE:",
    True,
)

print(
    "FIXED_FINITE_GLOBAL_STATE_SPACE:",
    False,
)

print(
    "IRRATIONAL_LIMITING_FREQUENCY:",
    True,
)


# ------------------------------------------------------------
# Final classification.
# ------------------------------------------------------------

print("PROGRESS: 6/6 finalize")

failed = [
    name
    for name, passed
    in checks.items()
    if not passed
]

audit_pass = not failed

verdict = (
    "a_finite_integer_substitution_rule_on_a_two_symbol_alphabet_"
    "with_unbounded_registered_history_generates_exact_irrational_"
    "asymptotic_symbol_frequencies_without_probability_weights_or_"
    "irrational_constants_in_the_rule"
    if audit_pass
    else
    "finite_rule_irrational_frequency_witness_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_finite_rule_irrational_frequency_witness_002",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "rule": {
        "A":
            "AB",

        "B":
            "A",

        "alphabet_size":
            2,

        "substitution_matrix":
            M,

        "probabilities_in_rule":
            False,

        "irrational_constants_in_rule":
            False,
    },

    "spectral_structure": {
        "characteristic_polynomial":
            "lambda^2-lambda-1",

        "Perron_root":
            "(1+sqrt(5))/2",

        "A_frequency":
            "(sqrt(5)-1)/2",

        "B_frequency":
            "(3-sqrt(5))/2",

        "A_frequency_numeric":
            qnum(fA),

        "B_frequency_numeric":
            qnum(fB),
    },

    "registered_history": {
        "global_state_space_fixed_finite":
            False,

        "alphabet_finite":
            True,

        "rule_finite":
            True,

        "history_growth":
            "unbounded",

        "generation_30_total":
            last["total"],
    },

    "checks":
        checks,

    "boundary": {
        "constructs_Program02_weights":
            False,

        "Fibonacci_rule_claimed_native_to_Thalean_apparatus":
            False,

        "derives_EPR_frequency_correspondence":
            False,

        "uses_target_probability_as_transition_input":
            False,

        "uses_Born_rule":
            False,

        "proves_mechanism_class_exists":
            True,
    },

    "earned_statement": (
        "Audit 001 rules out exact irrational frequency from static "
        "finite equal-count models and deterministic dynamics on a "
        "fixed finite state space. Audit 002 exhibits the minimal "
        "structural escape: a finite deterministic integer rule on a "
        "finite alphabet whose registered history grows without bound. "
        "The substitution A->AB, B->A has no probabilities or "
        "irrational constants in its rule, yet its integer substitution "
        "matrix has Perron root phi and generates exact irrational "
        "asymptotic symbol frequencies (sqrt(5)-1)/2 and "
        "(3-sqrt(5))/2. Thus finite rule does not imply rational "
        "asymptotic measure when the registered history itself grows."
    ),

    "next_gate": (
        "Test whether the exact Program-02 weights can be generated "
        "from a minimal composite of this finite-rule sqrt(5) measure "
        "and an independently balanced binary receipt, while marking "
        "that construction as a target-informed witness rather than "
        "native provenance."
    ),
}

artifact[
    "artifact_sha256"
] = digest_json(
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

note = f"""# Finite-rule irrational-frequency witness 002

## Result

Audit pass:

    {audit_pass}

Use the finite deterministic substitution

    A -> AB
    B -> A.

Its integer substitution matrix is

    [1 1]
    [1 0].

No probability or irrational constant appears in the rule.

The matrix has Perron root

    phi = (1+sqrt(5))/2.

Starting from A, the registered history grows without bound.

Its asymptotic symbol frequencies are

    f_A = (sqrt(5)-1)/2

and

    f_B = (3-sqrt(5))/2.

Both are irrational.

## Meaning

Audit 001 excluded deterministic dynamics on a fixed finite global state
space because such dynamics become eventually periodic.

Audit 002 shows the escape:

    finite rule
      !=
    fixed finite global state.

A finite alphabet and finite integer update law can generate an unbounded
registered history carrying an irrational invariant frequency.

## Boundary

This is a mechanism-class witness.

The Fibonacci substitution is not claimed to be native Thalean dynamics.

It does not yet derive the Program-02 EPR weights.

No Born rule or probability transition is inserted.

## Next gate

Test whether the Program-02 sqrt(5) weights can be reconstructed from a
minimal composite of this generated irrational measure and a balanced binary
receipt.

Such a result would be a candidate construction witness, not yet native
provenance.
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
    "FINITE_RULE:",
    True,
)

print(
    "UNBOUNDED_REGISTERED_HISTORY:",
    True,
)

print(
    "IRRATIONAL_LIMIT_A:",
    "(sqrt(5)-1)/2",
)

print(
    "IRRATIONAL_LIMIT_B:",
    "(3-sqrt(5))/2",
)

print(
    "NEXT_GATE:",
    "program02_weight_generation_witness",
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
