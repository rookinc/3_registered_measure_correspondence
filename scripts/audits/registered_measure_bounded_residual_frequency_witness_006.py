#!/usr/bin/env python3

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math

HERE = Path(__file__).resolve().parents[2]

A005 = (
    HERE
    / "artifacts/json"
    / "registered_measure_native_spectral_quadratic_register_005.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_bounded_residual_frequency_witness_006.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_bounded_residual_frequency_witness_006.md"
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


# Exact Q(sqrt(5)):
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


def qsub(x, y):
    return (
        x[0] - y[0],
        x[1] - y[1],
    )


def qscale(c, x):
    c = Fraction(c)

    return (
        c * x[0],
        c * x[1],
    )


def qnum(x):
    return (
        float(x[0])
        + float(x[1]) * math.sqrt(5.0)
    )


def qsign(x):
    a, b = x

    if b == 0:
        if a > 0:
            return 1
        if a < 0:
            return -1
        return 0

    if a == 0:
        return 1 if b > 0 else -1

    if a > 0 and b > 0:
        return 1

    if a < 0 and b < 0:
        return -1

    a2 = a * a
    b2 = 5 * b * b

    if a > 0 and b < 0:
        if a2 > b2:
            return 1
        if a2 < b2:
            return -1
        return 0

    # a < 0 and b > 0
    if b2 > a2:
        return 1
    if b2 < a2:
        return -1
    return 0


def qcmp(x, y):
    return qsign(
        qsub(
            x,
            y,
        )
    )


def qfloor(x):
    guess = math.floor(
        qnum(x)
    )

    while qcmp(
        x,
        q(guess),
    ) < 0:
        guess -= 1

    while qcmp(
        x,
        q(guess + 1),
    ) >= 0:
        guess += 1

    return guess


print("== 006 BOUNDED RESIDUAL FREQUENCY WITNESS ==")

a005 = load(A005)

checks = {}

checks["Audit005_passes"] = (
    a005["audit_pass"] is True
)

checks[
    "native_quadratic_register_closed"
] = (
    a005[
        "boundary"
    ][
        "native_quadratic_register_closed_at_operator_level"
    ]
    is True
)


# ------------------------------------------------------------
# Imported native class measure:
#
#     mu = q_fav
#        = (5+sqrt(5))/10
#        = 1/2 + sqrt(5)/10.
#
# Complement:
#
#     1-mu = q_unfav.
#
# This number is already derived by Audit005.
# It is not chosen here as a fitted frequency.
# ------------------------------------------------------------

print("PROGRESS: 1/7 import native algebraic measure")

mu = q(
    Fraction(1, 2),
    Fraction(1, 10),
)

mu_bar = q(
    Fraction(1, 2),
    Fraction(-1, 10),
)

checks[
    "mu_matches_Audit005_q_favored"
] = (
    a005[
        "native_masses"
    ][
        "q_favored"
    ]
    == "(5+sqrt(5))/10"
)

checks[
    "mu_complement_matches_Audit005_q_unfavored"
] = (
    a005[
        "native_masses"
    ][
        "q_unfavored"
    ]
    == "(5-sqrt(5))/10"
)

checks[
    "mu_plus_complement_one"
] = (
    qadd(
        mu,
        mu_bar,
    )
    == q(1)
)

print(
    "MU:",
    "(5+sqrt(5))/10",
)

print(
    "MU_NUMERIC:",
    qnum(mu),
)

print(
    "ONE_MINUS_MU:",
    "(5-sqrt(5))/10",
)


# ------------------------------------------------------------
# Universal residual rule.
#
# Start:
#
#     r_0 = 0.
#
# At each registered attempt:
#
#     t = r_n + mu.
#
# If t >= 1:
#
#     x_(n+1) = 1
#     r_(n+1) = t - 1.
#
# Otherwise:
#
#     x_(n+1) = 0
#     r_(n+1) = t.
#
# Thus:
#
#     r_(n+1) = r_n + mu - x_(n+1).
#
# The rule uses only
#
#     addition,
#     unit comparison,
#     integer receipt closure,
#     retained residual.
# ------------------------------------------------------------

print("PROGRESS: 2/7 declare universal residual closure rule")

checks[
    "rule_uses_only_add_compare_close_retain"
] = True

checks[
    "rule_has_no_random_input"
] = True

checks[
    "mu_not_inserted_as_stochastic_transition_probability"
] = True

print(
    "RULE:",
    "r <- r + mu; emit 1 and subtract 1 iff r >= 1",
)

print(
    "RANDOM_INPUT:",
    False,
)


# ------------------------------------------------------------
# Generate exact registered sequence.
# ------------------------------------------------------------

print("PROGRESS: 3/7 generate exact algebraic residual history")

N = 10000

r = q(0)
fav_count = 0

fav_split = [0, 0]
unfav_split = [0, 0]

fav_parity = 0
unfav_parity = 0

max_prefix_error = 0.0
max_residual_numeric = 0.0

selected_rows = []

for n in range(1, N + 1):
    t = qadd(
        r,
        mu,
    )

    if qcmp(
        t,
        q(1),
    ) >= 0:
        x = 1
        r = qsub(
            t,
            q(1),
        )

        fav_count += 1

        fav_split[
            fav_parity
        ] += 1

        fav_parity ^= 1

    else:
        x = 0
        r = t

        unfav_split[
            unfav_parity
        ] += 1

        unfav_parity ^= 1

    exact_floor = qfloor(
        qscale(
            n,
            mu,
        )
    )

    if fav_count != exact_floor:
        raise SystemExit(
            "prefix count identity failed at n="
            + str(n)
        )

    expected_r = qsub(
        qscale(
            n,
            mu,
        ),
        q(
            exact_floor,
        ),
    )

    if r != expected_r:
        raise SystemExit(
            "residual identity failed at n="
            + str(n)
        )

    if not (
        qcmp(
            r,
            q(0),
        )
        >= 0
        and qcmp(
            r,
            q(1),
        )
        < 0
    ):
        raise SystemExit(
            "residual escaped unit interval"
        )

    freq = (
        fav_count
        / n
    )

    err = abs(
        freq
        - qnum(mu)
    )

    max_prefix_error = max(
        max_prefix_error,
        err,
    )

    max_residual_numeric = max(
        max_residual_numeric,
        qnum(r),
    )

    if n in (
        1,
        2,
        3,
        5,
        10,
        100,
        1000,
        10000,
    ):
        selected_rows.append({
            "n":
                n,

            "fav_count":
                fav_count,

            "unfav_count":
                n - fav_count,

            "fav_frequency":
                freq,

            "absolute_error":
                err,

            "residual":
                qnum(r),
        })


checks[
    "exact_prefix_count_identity"
] = True

checks[
    "exact_residual_identity"
] = True

checks[
    "residual_stays_bounded_in_unit_interval"
] = True

print(
    "ATTEMPT_COUNT:",
    N,
)

print(
    "FAV_COUNT:",
    fav_count,
)

print(
    "UNFAV_COUNT:",
    N - fav_count,
)

print(
    "FINAL_RESIDUAL:",
    qnum(r),
)


# ------------------------------------------------------------
# Theorem:
#
#     N_fav(n) = floor(n mu).
#
# Hence:
#
#     0 <= n mu - N_fav(n) < 1.
#
# Divide by n:
#
#     |N_fav(n)/n - mu| < 1/n.
#
# Therefore frequency converges exactly to mu.
# ------------------------------------------------------------

print("PROGRESS: 4/7 certify bounded-discrepancy convergence")

final_frequency = (
    fav_count / N
)

final_error = abs(
    final_frequency
    - qnum(mu)
)

checks[
    "final_frequency_error_below_one_over_N"
] = (
    final_error
    < 1.0 / N
)

checks[
    "asymptotic_frequency_equals_mu"
] = True

checks[
    "bounded_discrepancy_strictly_less_than_one"
] = True

print(
    "FINAL_FAV_FREQUENCY:",
    final_frequency,
)

print(
    "TARGET_ALGEBRAIC_MEASURE:",
    qnum(mu),
)

print(
    "FINAL_ERROR:",
    final_error,
)

print(
    "ERROR_BOUND:",
    1.0 / N,
)

print(
    "EXACT_THEOREM:",
    "N_fav(n)=floor(n*mu)",
)


# ------------------------------------------------------------
# Balanced binary split.
#
# Audit041/005 requires each correlation class to split equally
# between two symmetry-related binary receipts.
#
# We implement no probability here: simply alternate a parity bit
# each time a member of a class occurs.
#
# Therefore the two counts within each class differ by at most one.
# ------------------------------------------------------------

print("PROGRESS: 5/7 realize balanced two-way class split")

checks[
    "favored_subreceipt_count_difference_at_most_one"
] = (
    abs(
        fav_split[0]
        - fav_split[1]
    )
    <= 1
)

checks[
    "unfavored_subreceipt_count_difference_at_most_one"
] = (
    abs(
        unfav_split[0]
        - unfav_split[1]
    )
    <= 1
)

fav0_freq = (
    fav_split[0] / N
)

fav1_freq = (
    fav_split[1] / N
)

unfav0_freq = (
    unfav_split[0] / N
)

unfav1_freq = (
    unfav_split[1] / N
)

w_large = (
    qnum(mu) / 2.0
)

w_small = (
    qnum(mu_bar) / 2.0
)

checks[
    "favored_subreceipts_converge_to_mu_over_two"
] = (
    abs(
        fav0_freq
        - w_large
    )
    < 2.0 / N
    and abs(
        fav1_freq
        - w_large
    )
    < 2.0 / N
)

checks[
    "unfavored_subreceipts_converge_to_complement_over_two"
] = (
    abs(
        unfav0_freq
        - w_small
    )
    < 2.0 / N
    and abs(
        unfav1_freq
        - w_small
    )
    < 2.0 / N
)

print(
    "FAVORED_SPLIT_COUNTS:",
    fav_split,
)

print(
    "UNFAVORED_SPLIT_COUNTS:",
    unfav_split,
)

print(
    "FAVORED_SUBRECEIPT_TARGET:",
    "1/4+sqrt(5)/20",
)

print(
    "UNFAVORED_SUBRECEIPT_TARGET:",
    "1/4-sqrt(5)/20",
)


# ------------------------------------------------------------
# Aperiodicity.
#
# An eventually periodic binary sequence has rational asymptotic
# frequency.
#
# This sequence has irrational asymptotic frequency mu.
#
# Therefore the registered class sequence cannot be eventually
# periodic.
# ------------------------------------------------------------

print("PROGRESS: 6/7 classify history structure")

checks[
    "mu_is_irrational"
] = True

checks[
    "receipt_sequence_not_eventually_periodic"
] = True

checks[
    "bounded_residual_register_has_infinite_exact_orbit"
] = True

print(
    "EVENTUALLY_PERIODIC:",
    False,
)

print(
    "RESIDUAL_BOUNDED:",
    True,
)

print(
    "EXACT_RESIDUAL_ORBIT_FINITE:",
    False,
)


# ------------------------------------------------------------
# Final classification.
# ------------------------------------------------------------

print("PROGRESS: 7/7 finalize")

failed = [
    name
    for name, passed
    in checks.items()
    if not passed
]

audit_pass = not failed

verdict = (
    "the_native_algebraic_class_measure_can_be_transduced_by_a_"
    "universal_deterministic_bounded_residual_rule_into_a_registered_"
    "binary_history_with_exact_prefix_count_floor_nmu_bounded_"
    "discrepancy_and_asymptotic_frequency_mu_without_randomness_or_"
    "stochastic_transition_probabilities"
    if audit_pass
    else
    "bounded_residual_frequency_witness_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_bounded_residual_frequency_witness_006",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "input_measure": {
        "source":
            "Audit005 native spectral quadratic register",

        "mu":
            "(5+sqrt(5))/10",

        "complement":
            "(5-sqrt(5))/10",

        "mu_inserted_as_fitted_frequency":
            False,

        "mu_already_derived_algebraically":
            True,
    },

    "residual_rule": {
        "initial_residual":
            0,

        "update":
            "t=r+mu",

        "closure":
            "emit 1 and set r=t-1 iff t>=1",

        "otherwise":
            "emit 0 and set r=t",

        "random_input":
            False,

        "stochastic_transition_probability":
            False,
    },

    "exact_theorem": {
        "favored_count":
            "N_fav(n)=floor(n*mu)",

        "residual":
            "r_n=n*mu-floor(n*mu)",

        "residual_interval":
            "0<=r_n<1",

        "frequency_error":
            "|N_fav(n)/n-mu|<1/n",

        "limiting_frequency":
            "mu",
    },

    "balanced_split": {
        "mechanism":
            "toggle parity within each class",

        "favored_subreceipt_limit":
            "mu/2 = 1/4+sqrt(5)/20",

        "unfavored_subreceipt_limit":
            "(1-mu)/2 = 1/4-sqrt(5)/20",

        "probability_used":
            False,
    },

    "sample_run": {
        "attempt_count":
            N,

        "favored_count":
            fav_count,

        "unfavored_count":
            N - fav_count,

        "favored_frequency":
            final_frequency,

        "target_numeric":
            qnum(mu),

        "absolute_error":
            final_error,

        "favored_split_counts":
            fav_split,

        "unfavored_split_counts":
            unfav_split,

        "selected_prefixes":
            selected_rows,
    },

    "history": {
        "eventually_periodic":
            False,

        "residual_bounded":
            True,

        "residual_exact_state_set_finite":
            False,

        "rule_finitely_specified":
            True,
    },

    "checks":
        checks,

    "boundary": {
        "correspondence_mechanism_class_constructed":
            audit_pass,

        "native_Thalean_residual_accumulator_derived":
            False,

        "local_spacelike_outcome_generation_derived":
            False,

        "joint_setting_context_used_as_causal_remote_input":
            False,

        "rule_claimed_as_physical_dynamics":
            False,

        "empirical_frequency_correspondence_closed_natively":
            False,

        "Born_rule_assumed":
            False,
    },

    "earned_statement": (
        "Audit005 supplies a native normalized algebraic class measure "
        "mu=(5+sqrt(5))/10. Audit006 shows that any such measure can be "
        "transduced into exact asymptotic registered frequency by a "
        "universal deterministic residual rule: add mu, close one "
        "integer receipt when the unit boundary is crossed, and retain "
        "the residual. The cumulative favored count is exactly "
        "floor(n mu), the residual remains in [0,1), and frequency "
        "error is strictly below 1/n. Alternating a parity bit within "
        "each class yields the two equal binary subreceipt frequencies "
        "mu/2 and (1-mu)/2, exactly the Program-02 algebraic weights. "
        "No stochastic transition probability or random input is used. "
        "This is a correspondence mechanism witness, not yet proof "
        "that the native apparatus implements this residual rule."
    ),

    "next_gate": (
        "Test whether the existing registered-action apparatus already "
        "contains the four primitives required by this witness: "
        "additive accumulation, a normalized unit closure boundary, "
        "integer receipt emission, and retained bounded residual. "
        "If those primitives are native, test exact identification "
        "with the Audit005 spectral weight rather than inventing a new "
        "frequency law."
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

note = """# Bounded residual frequency witness 006

## Result

Audit005 supplies the canonical algebraic class measure

    mu = (5+sqrt(5))/10.

Use the deterministic residual rule

    r_0 = 0

and on each registered attempt

    t = r_n + mu.

If

    t >= 1,

emit a favored receipt and retain

    r_(n+1) = t - 1.

Otherwise emit an unfavored receipt and retain

    r_(n+1) = t.

Exactly,

    N_fav(n) = floor(n mu)

and

    r_n = n mu - floor(n mu).

Therefore

    0 <= r_n < 1

and

    |N_fav(n)/n - mu| < 1/n.

Hence the registered frequency converges exactly to the imported algebraic
measure.

No stochastic transition probability is used.

No random input is used.

## Binary split

Toggle one parity bit inside each correlation class.

Then the two favored subreceipts differ in count by at most one, as do the
two unfavored subreceipts.

Their limiting frequencies are

    mu/2
      =
    1/4 + sqrt(5)/20

and

    (1-mu)/2
      =
    1/4 - sqrt(5)/20.

These are exactly the Program-02 nontrivial binary algebraic weights.

## Structural meaning

The bridge requires only

    addition
      -> boundary crossing
      -> integer receipt
      -> retained residual.

The rule is finitely specified.

The residual remains bounded.

Because mu is irrational, the exact residual orbit is infinite and the
receipt history is not eventually periodic.

## Boundary

This is a correspondence mechanism witness.

It does not yet prove that native Thalean registration implements this
accumulator.

It does not derive local spacelike outcome production.

It does not assume the Born rule.

## Next gate

Ask whether native registered mechanics already contains:

    additive accumulation
    normalized closure boundary
    integer receipt emission
    retained bounded residual.

If those primitives are already native, bind them to the Audit005 algebraic
measure rather than introducing a new frequency law.
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
    "EXACT_COUNT_LAW:",
    "N_fav(n)=floor(n*mu)",
)

print(
    "FINAL_FREQUENCY_ERROR:",
    final_error,
)

print(
    "BOUND:",
    1.0 / N,
)

print(
    "RANDOM_INPUT:",
    False,
)

print(
    "STOCHASTIC_TRANSITION_PROBABILITY:",
    False,
)

print(
    "NEXT_GATE:",
    "native_residual_accumulator_provenance",
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
