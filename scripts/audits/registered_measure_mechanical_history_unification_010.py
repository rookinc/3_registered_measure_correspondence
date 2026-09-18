#!/usr/bin/env python3

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math

HERE = Path(__file__).resolve().parents[2]

A006 = (
    HERE
    / "artifacts/json"
    / "registered_measure_bounded_residual_frequency_witness_006.v1.json"
)

A009 = (
    HERE
    / "artifacts/json"
    / "registered_measure_finite_morphism_weight_witness_009.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_mechanical_history_unification_010.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_mechanical_history_unification_010.md"
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


# Q(sqrt(5)): a + b sqrt(5)
def q(a=0, b=0):
    return Fraction(a), Fraction(b)


def qadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def qsub(x, y):
    return x[0] - y[0], x[1] - y[1]


def qscale(c, x):
    c = Fraction(c)
    return c*x[0], c*x[1]


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
    return float(x[0]) + float(x[1])*math.sqrt(5.0)


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

    a2 = a*a
    b2 = 5*b*b

    if a > 0:
        return 1 if a2 > b2 else -1

    return 1 if b2 > a2 else -1


def qcmp(x, y):
    return qsign(qsub(x, y))


def qfloor(x):
    n = math.floor(qnum(x))

    while qcmp(x, q(n)) < 0:
        n -= 1

    while qcmp(x, q(n + 1)) >= 0:
        n += 1

    return n


print("== 010 MECHANICAL HISTORY UNIFICATION ==")

a006 = load(A006)
a009 = load(A009)

checks = {}

checks["Audit006_passes"] = (
    a006["audit_pass"] is True
)

checks["Audit009_passes"] = (
    a009["audit_pass"] is True
)


# ------------------------------------------------------------
# Exact parameters.
# ------------------------------------------------------------

print("PROGRESS: 1/6 derive exact common slope")

mu = q(
    Fraction(1, 2),
    Fraction(1, 10),
)

alpha = q(
    Fraction(1, 2),
    Fraction(-1, 10),
)

phi = q(
    Fraction(1, 2),
    Fraction(1, 2),
)

phi2 = qmul(phi, phi)

beta = qadd(
    phi2,
    q(1),
)

inv_alpha = qinv(alpha)

checks["mu_plus_alpha_one"] = (
    qadd(mu, alpha) == q(1)
)

checks["beta_equals_phi2_plus_one"] = (
    beta
    == q(
        Fraction(5, 2),
        Fraction(1, 2),
    )
)

checks["beta_equals_inverse_alpha"] = (
    beta == inv_alpha
)

print(
    "MU:",
    "(5+sqrt(5))/10",
)

print(
    "ALPHA:",
    "(5-sqrt(5))/10",
)

print(
    "BETA:",
    "phi^2+1=(5+sqrt(5))/2",
)

print(
    "BETA_EQUALS_1_OVER_ALPHA:",
    checks["beta_equals_inverse_alpha"],
)


# ------------------------------------------------------------
# Generate Fibonacci fixed-point prefix.
#
# A -> AB
# B -> A
#
# Then apply
#
# A -> 1
# B -> 10.
# ------------------------------------------------------------

print("PROGRESS: 2/6 generate finite-morphism history")

N = 20000

word = "A"

while len(word) < N:
    word = "".join(
        "AB" if c == "A" else "A"
        for c in word
    )

morphic = "".join(
    "1" if c == "A" else "10"
    for c in word
)

morphic = morphic[:N]

checks["morphic_prefix_length"] = (
    len(morphic) == N
)

print(
    "PREFIX_LENGTH:",
    len(morphic),
)

print(
    "MORPHIC_PREFIX_40:",
    morphic[:40],
)


# ------------------------------------------------------------
# Generate exact residual/mechanical history.
#
# Use the same Audit006 rule but begin at residual r_0=mu.
#
# Then
#
# x_n = floor((n+1)mu)-floor(n mu), n>=1.
#
# This is exactly the one-receipt phase shift of the Audit006
# r_0=0 history.
# ------------------------------------------------------------

print("PROGRESS: 3/6 generate exact residual history")

r = mu
mechanical_bits = []

for _ in range(N):
    t = qadd(
        r,
        mu,
    )

    if qcmp(
        t,
        q(1),
    ) >= 0:
        mechanical_bits.append("1")
        r = qsub(
            t,
            q(1),
        )
    else:
        mechanical_bits.append("0")
        r = t

mechanical = "".join(mechanical_bits)

mismatch_count = sum(
    a != b
    for a, b in zip(
        morphic,
        mechanical,
    )
)

first_mismatch = None

for i, (a, b) in enumerate(
    zip(
        morphic,
        mechanical,
    ),
    start=1,
):
    if a != b:
        first_mismatch = i
        break

checks[
    "morphic_and_mechanical_prefix_exact_match"
] = (
    mismatch_count == 0
)

print(
    "MECHANICAL_PREFIX_40:",
    mechanical[:40],
)

print(
    "MISMATCH_COUNT:",
    mismatch_count,
)

print(
    "FIRST_MISMATCH:",
    first_mismatch,
)


# ------------------------------------------------------------
# Verify phase relation to Audit006 r0=0 history.
#
# r0=0 emits one leading 0. Dropping that first receipt must give
# the r0=mu history.
# ------------------------------------------------------------

print("PROGRESS: 4/6 verify one-receipt phase relation")

r0 = q(0)
zero_phase_bits = []

for _ in range(N + 1):
    t = qadd(
        r0,
        mu,
    )

    if qcmp(
        t,
        q(1),
    ) >= 0:
        zero_phase_bits.append("1")
        r0 = qsub(
            t,
            q(1),
        )
    else:
        zero_phase_bits.append("0")
        r0 = t

zero_phase = "".join(
    zero_phase_bits
)

checks[
    "mechanical_is_zero_phase_shifted_one_receipt"
] = (
    zero_phase[1:]
    == mechanical
)

print(
    "ZERO_PHASE_PREFIX_41:",
    zero_phase[:41],
)

print(
    "PHASE_SHIFT_RELATION:",
    "morphic = Audit006_history[1:]",
)


# ------------------------------------------------------------
# Beatty zero-position test.
#
# The k-th zero of the transformed Fibonacci history is predicted at
#
#     z_k = floor(k beta)
#
# where
#
#     beta = phi^2 + 1 = 1/alpha.
#
# This is exactly the zero-position law of the mechanical word of
# one-density mu.
# ------------------------------------------------------------

print("PROGRESS: 5/6 verify exact Beatty zero positions")

zero_positions = [
    i
    for i, bit in enumerate(
        morphic,
        start=1,
    )
    if bit == "0"
]

beatty_failures = 0

for k, observed in enumerate(
    zero_positions,
    start=1,
):
    predicted = qfloor(
        qscale(
            k,
            beta,
        )
    )

    if predicted != observed:
        beatty_failures += 1

checks[
    "all_observed_zero_positions_match_Beatty_law"
] = (
    beatty_failures == 0
)

print(
    "ZERO_COUNT_IN_PREFIX:",
    len(zero_positions),
)

print(
    "FIRST_ZERO_POSITIONS:",
    zero_positions[:12],
)

print(
    "BEATTY_ZERO_LAW:",
    "z_k=floor(k*(phi^2+1))=floor(k/(1-mu))",
)

print(
    "BEATTY_FAILURES:",
    beatty_failures,
)


# ------------------------------------------------------------
# Classification.
# ------------------------------------------------------------

print("PROGRESS: 6/6 classify")

failed = [
    k
    for k, v in checks.items()
    if not v
]

audit_pass = not failed

verdict = (
    "the_finite_Fibonacci_plus_receipt_morphism_witness_and_the_"
    "bounded_residual_accumulator_witness_generate_the_same_sqrt5_"
    "mechanical_registered_history_after_a_one_receipt_phase_shift_"
    "over_the_certified_prefix_and_share_the_same_exact_Beatty_"
    "zero_position_parameters"
    if audit_pass
    else
    "mechanical_history_unification_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_mechanical_history_unification_010",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "common_parameters": {
        "one_density":
            "(5+sqrt(5))/10",

        "zero_density":
            "(5-sqrt(5))/10",

        "zero_Beatty_spacing":
            "phi^2+1=(5+sqrt(5))/2",

        "zero_Beatty_spacing_equals_inverse_zero_density":
            True,
    },

    "finite_morphism_history": {
        "substitution":
            "A->AB; B->A",

        "morphism":
            "A->1; B->10",
    },

    "residual_history": {
        "increment":
            "(5+sqrt(5))/10",

        "phase_aligned_initial_residual":
            "mu",

        "rule":
            "add mu; emit 1 on unit crossing; retain remainder",
    },

    "prefix_certificate": {
        "length":
            N,

        "mismatch_count":
            mismatch_count,

        "first_mismatch":
            first_mismatch,

        "Beatty_zero_failure_count":
            beatty_failures,
    },

    "phase_relation": {
        "statement":
            (
                "finite-morphism history equals the Audit006 "
                "zero-residual history after dropping its first receipt"
            ),

        "shift":
            1,
    },

    "checks":
        checks,

    "boundary": {
        "two_witnesses_independent_mechanisms":
            False,

        "same_symbolic_dynamics_candidate":
            True,

        "infinite_native_conjugacy_theorem_closed":
            False,

        "Fibonacci_dynamics_native":
            False,

        "algebraic_residual_state_native":
            False,

        "frequency_correspondence_closed_natively":
            False,
    },

    "earned_statement": (
        "The two Program-03 frequency witnesses are not independent "
        "constructions. After one receipt of phase alignment, the "
        "Fibonacci substitution followed by A->1, B->10 and the exact "
        "bounded-residual threshold rule with increment "
        "mu=(5+sqrt(5))/10 produce identical registered binary history "
        "through the certified 20000-receipt prefix. Their exact "
        "parameters also coincide: zeros have density "
        "(5-sqrt(5))/10 and Beatty spacing "
        "phi^2+1=1/(1-mu). Thus the discrete morphic and algebraic "
        "rotation pictures are two representations of one mechanical "
        "history candidate, not competing frequency laws."
    ),

    "next_gate": (
        "Search native registered mechanics for either representation "
        "of this single mechanical history: a two-class Fibonacci-type "
        "recurrence or an algebraic phase increment. Evidence for "
        "either representation should be tested against the same "
        "receipt history rather than treated as a new mechanism."
    ),
}

artifact["artifact_sha256"] = digest(
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
    """# Mechanical history unification 010

## Result

The two correspondence witnesses are phase-aligned forms of the same
registered binary history.

Route 1:

    A -> AB
    B -> A

followed by

    A -> 1
    B -> 10.

Route 2:

    add mu
    emit 1 at unit crossing
    retain the residual,

with

    mu = (5+sqrt(5))/10.

Starting the residual rule at phase

    r_0 = mu

produces the same certified binary history as the finite morphism.

Starting at

    r_0 = 0

adds one leading receipt, so the two histories differ only by one receipt of
phase.

The zero density is

    alpha = (5-sqrt(5))/10

and the zero positions obey

    z_k = floor(k/(1-mu))
        = floor(k*(phi^2+1)).

## Meaning

The discrete substitution witness and algebraic residual witness should not
be treated as competing mechanisms.

They are two representations of one sqrt(5) mechanical-history candidate.

## Boundary

The certified prefix has finite length.

No native Fibonacci recurrence is yet established.

No native algebraic fractional phase is yet established.

The native correspondence question remains provenance of this mechanical
history, not construction of another frequency law.
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
    "CERTIFIED_PREFIX_LENGTH:",
    N,
)

print(
    "MISMATCH_COUNT:",
    mismatch_count,
)

print(
    "PHASE_SHIFT:",
    1,
)

print(
    "BEATTY_FAILURES:",
    beatty_failures,
)

print(
    "NEXT_GATE:",
    "native_mechanical_history_provenance",
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
