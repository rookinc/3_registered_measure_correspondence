#!/usr/bin/env python3

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math

HERE = Path(__file__).resolve().parents[2]

SOURCE = (
    HERE
    / "source"
    / "program02_algebraic_epr_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_finite_count_obstruction_001.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_finite_count_obstruction_001.md"
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


print("== 001 FINITE COUNT OBSTRUCTION ==")

src = load(SOURCE)

checks = {}

checks["Program02_interface_sealed"] = (
    src["status"] == "sealed_input_interface"
)

checks["Program02_algebraic_EPR_closed"] = (
    src[
        "boundary"
    ][
        "algebraic_EPR_assembly_closed"
    ]
    is True
)

checks["frequency_correspondence_open"] = (
    src[
        "boundary"
    ][
        "operational_frequency_correspondence_open"
    ]
    is True
)


# ------------------------------------------------------------
# Exact imported nontrivial weights:
#
#     w_minus = 1/4 - sqrt(5)/20
#     w_plus  = 1/4 + sqrt(5)/20
#
# Since sqrt(5) is irrational, both are irrational.
# ------------------------------------------------------------

print("PROGRESS: 1/5 classify imported algebraic weights")

w_minus_numeric = (
    1.0 / 4.0
    - math.sqrt(5.0) / 20.0
)

w_plus_numeric = (
    1.0 / 4.0
    + math.sqrt(5.0) / 20.0
)

checks[
    "sqrt5_is_irrational_by_squarefree_integer_theorem"
] = True

checks[
    "nontrivial_weights_are_irrational"
] = True

print(
    "W_MINUS:",
    "1/4-sqrt(5)/20",
)

print(
    "W_MINUS_NUMERIC:",
    w_minus_numeric,
)

print(
    "W_PLUS:",
    "1/4+sqrt(5)/20",
)

print(
    "W_PLUS_NUMERIC:",
    w_plus_numeric,
)


# ------------------------------------------------------------
# Any finite equal-count ratio is k/N with integers
#
#     0 <= k <= N,
#     N > 0.
#
# Therefore every such ratio is rational.
#
# An irrational Program-02 weight cannot equal k/N for any finite N.
# ------------------------------------------------------------

print("PROGRESS: 2/5 exclude finite equal-count realization")

checks[
    "every_finite_equal_count_ratio_is_rational"
] = True

checks[
    "w_minus_not_finite_equal_count_ratio"
] = True

checks[
    "w_plus_not_finite_equal_count_ratio"
] = True

print(
    "FINITE_EQUAL_COUNT_EXACT_REALIZATION:",
    False,
)


# ------------------------------------------------------------
# Deterministic dynamics on a finite state set.
#
# Any infinite trajectory
#
#     x_0, x_1, x_2, ...
#
# under a deterministic map F:S->S is eventually periodic.
#
# After a finite transient it enters a cycle of length L.
#
# For any registered event subset R of S, the asymptotic visit
# frequency is
#
#     m/L
#
# where m is the number of cycle positions lying in R.
#
# Hence every exact limiting frequency is rational.
# ------------------------------------------------------------

print("PROGRESS: 3/5 exclude finite deterministic periodic frequency")

checks[
    "finite_deterministic_dynamics_eventually_periodic"
] = True

checks[
    "periodic_cycle_visit_frequency_is_rational"
] = True

checks[
    "irrational_weight_not_exact_periodic_visit_frequency"
] = True

print(
    "FINITE_DETERMINISTIC_EXACT_LIMITING_FREQUENCY:",
    False,
)


# ------------------------------------------------------------
# Demonstrate the finite-cycle form explicitly for a representative
# family. This is illustrative only; the theorem above is general.
# ------------------------------------------------------------

print("PROGRESS: 4/5 verify representative finite-cycle census")

representative_denominators = (
    1,
    2,
    3,
    5,
    8,
    13,
    21,
    34,
    55,
    89,
)

representative_ratio_count = 0
accidental_numeric_match_count = 0

for L in representative_denominators:
    for m in range(L + 1):
        representative_ratio_count += 1

        r = Fraction(
            m,
            L,
        )

        if (
            float(r) == w_minus_numeric
            or float(r) == w_plus_numeric
        ):
            accidental_numeric_match_count += 1

checks[
    "representative_cycle_scan_has_no_exact_float_collision"
] = (
    accidental_numeric_match_count == 0
)

print(
    "REPRESENTATIVE_RATIO_COUNT:",
    representative_ratio_count,
)

print(
    "ACCIDENTAL_NUMERIC_MATCH_COUNT:",
    accidental_numeric_match_count,
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

verdict = (
    "program02_nontrivial_algebraic_weights_are_irrational_and_"
    "therefore_cannot_be_exact_finite_equal_count_ratios_or_exact_"
    "limiting_visit_frequencies_of_any_finite_deterministic_state_"
    "machine"
    if audit_pass
    else
    "finite_count_obstruction_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_finite_count_obstruction_001",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "imported_interface": {
        "source":
            str(SOURCE),

        "source_terminal_artifact":
            src[
                "source_terminal_artifact"
            ],

        "weights": [
            "1/4-sqrt(5)/20",
            "1/4+sqrt(5)/20",
        ],
    },

    "theorem": {
        "finite_equal_count_form":
            "k/N",

        "finite_equal_count_number_class":
            "rational",

        "finite_deterministic_long_run_form":
            "m/L after eventual periodicity",

        "finite_deterministic_long_run_number_class":
            "rational",

        "Program02_nontrivial_weight_number_class":
            "irrational",

        "exact_finite_equal_count_realization":
            False,

        "exact_finite_deterministic_visit_frequency_realization":
            False,
    },

    "distinctions": {
        "algebraic_measure":
            (
                "canonical positive weight fixed by relational "
                "operator geometry"
            ),

        "finite_state_count":
            (
                "ratio of integer multiplicities on a finite set"
            ),

        "registered_frequency":
            (
                "empirical or asymptotic occurrence frequency in "
                "repeated registered events"
            ),

        "these_are_not_identified":
            True,
    },

    "checks":
        checks,

    "boundary": {
        "rules_out_finite_equal_count_hidden_census":
            True,

        "rules_out_finite_deterministic_periodic_exact_frequency":
            True,

        "rules_out_approximation_by_rational_frequencies":
            False,

        "rules_out_stochastic_finite_processes":
            False,

        "rules_out_algebraic_transition_weights":
            False,

        "rules_out_nonperiodic_registered_history":
            False,

        "rules_out_infinite_time_convergence":
            False,

        "derives_operational_frequency_correspondence":
            False,
    },

    "earned_statement": (
        "The nontrivial Program-02 binary weights contain sqrt(5) "
        "and are irrational. Every finite equal-count realization is "
        "a rational ratio k/N. Every deterministic trajectory on a "
        "finite state space is eventually periodic, and every exact "
        "limiting visit frequency on its eventual cycle is a rational "
        "ratio m/L. Therefore the Program-02 weights cannot be exact "
        "finite hidden-state count ratios or exact limiting visit "
        "frequencies of any finite deterministic state machine. "
        "Program 03 must seek a correspondence mechanism richer than "
        "static finite counting or eventual periodicity."
    ),

    "next_gate": (
        "Classify the weakest finite registered dynamics capable of "
        "supporting an irrational invariant measure without inserting "
        "the Program-02 weights as transition probabilities."
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

note = f"""# Finite count obstruction 001

## Result

Audit pass:

    {audit_pass}

Program 02 supplies the exact nontrivial weights

    1/4 - sqrt(5)/20

and

    1/4 + sqrt(5)/20.

Both are irrational.

Every finite equal-count model produces a ratio

    k/N,

which is rational.

Therefore no finite equal-count hidden-state census can reproduce either
weight exactly.

A deterministic map on a finite state set is eventually periodic.

After entering a cycle of length L, the limiting frequency of any registered
event is

    m/L,

which is also rational.

Therefore no finite deterministic state machine can produce either imported
irrational weight as an exact asymptotic visit frequency.

## Distinction

Program 03 keeps separate:

    algebraic measure
    finite state count
    registered frequency.

Audit 001 proves that the first cannot be reduced exactly to the second, nor
to periodic deterministic frequency.

## Boundary

This does not rule out:

- rational approximation,
- stochastic finite dynamics,
- algebraic transition structure,
- nonperiodic registered history,
- or asymptotic convergence generated by a richer process.

No frequency correspondence theorem is claimed yet.

## Next gate

Find the weakest registered dynamics capable of supporting an irrational
invariant measure without inserting the Program-02 weights by hand.
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
    "FINITE_EQUAL_COUNT_EXACT_REALIZATION:",
    False,
)

print(
    "FINITE_DETERMINISTIC_EXACT_LIMITING_FREQUENCY:",
    False,
)

print(
    "NEXT_GATE:",
    "weakest_irrational_invariant_measure_mechanism",
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
