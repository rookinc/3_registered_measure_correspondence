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

SOURCE = (
    HERE
    / "source"
    / "program02_algebraic_epr_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_joint_pair_square_witness_003.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_joint_pair_square_witness_003.md"
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


# Q(sqrt(5)): a + b sqrt(5)
def q(a=0, b=0):
    return Fraction(a), Fraction(b)


def qadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def qsub(x, y):
    return x[0] - y[0], x[1] - y[1]


def qmul(x, y):
    a, b = x
    c, d = y
    return (
        a*c + 5*b*d,
        a*d + b*c,
    )


def qscale(c, x):
    c = Fraction(c)
    return c*x[0], c*x[1]


def qinv(x):
    a, b = x
    den = a*a - 5*b*b
    if den == 0:
        raise ZeroDivisionError
    return a/den, -b/den


def qdiv(x, y):
    return qmul(x, qinv(y))


def qnum(x):
    return float(x[0]) + float(x[1])*sqrt(5.0)


print("== 003 JOINT PAIR-SQUARE WITNESS ==")

a002 = load(A002)
src = load(SOURCE)

checks = {}

checks["Audit002_passes"] = (
    a002["audit_pass"] is True
)

checks["Program02_interface_sealed"] = (
    src["status"] == "sealed_input_interface"
)


# ------------------------------------------------------------
# Fibonacci limiting measure.
# ------------------------------------------------------------

print("PROGRESS: 1/6 reconstruct Fibonacci limiting frequencies")

fA = q(
    Fraction(-1, 2),
    Fraction(1, 2),
)

fB = q(
    Fraction(3, 2),
    Fraction(-1, 2),
)

phi = q(
    Fraction(1, 2),
    Fraction(1, 2),
)

phi2 = qmul(phi, phi)

checks["fA_plus_fB_one"] = (
    qadd(fA, fB) == q(1)
)

checks["fA_over_fB_equals_phi"] = (
    qdiv(fA, fB) == phi
)

print(
    "F_A:",
    "(sqrt(5)-1)/2",
)

print(
    "F_B:",
    "(3-sqrt(5))/2",
)

print(
    "F_A_OVER_F_B:",
    "phi",
)


# ------------------------------------------------------------
# Program-02 two-class weights.
#
# Each nontrivial binary weight occurs twice:
#
#     w_plus  = (5+sqrt5)/20
#     w_minus = (5-sqrt5)/20
#
# so the corresponding two-class totals are
#
#     q_plus  = 2 w_plus
#     q_minus = 2 w_minus.
# ------------------------------------------------------------

print("PROGRESS: 2/6 reconstruct Program02 two-class totals")

w_plus = q(
    Fraction(1, 4),
    Fraction(1, 20),
)

w_minus = q(
    Fraction(1, 4),
    Fraction(-1, 20),
)

q_plus = qscale(
    2,
    w_plus,
)

q_minus = qscale(
    2,
    w_minus,
)

checks["Program02_class_totals_sum_one"] = (
    qadd(q_plus, q_minus) == q(1)
)

checks["Program02_class_ratio_phi_squared"] = (
    qdiv(q_plus, q_minus) == phi2
)

print(
    "Q_PLUS:",
    "(5+sqrt(5))/10",
)

print(
    "Q_MINUS:",
    "(5-sqrt(5))/10",
)

print(
    "Q_PLUS_OVER_Q_MINUS:",
    "phi^2",
)


# ------------------------------------------------------------
# Pair-square identity.
#
# Form same-class ordered pair masses from the limiting Fibonacci
# measure:
#
#     fA^2
#     fB^2.
#
# Condition only on the union of those two same-class pair sectors.
#
# The normalized masses are exactly q_plus and q_minus.
# ------------------------------------------------------------

print("PROGRESS: 3/6 prove exact pair-square identity")

fA2 = qmul(fA, fA)
fB2 = qmul(fB, fB)

pair_total = qadd(
    fA2,
    fB2,
)

pair_A = qdiv(
    fA2,
    pair_total,
)

pair_B = qdiv(
    fB2,
    pair_total,
)

checks["pair_A_equals_q_plus"] = (
    pair_A == q_plus
)

checks["pair_B_equals_q_minus"] = (
    pair_B == q_minus
)

checks["pair_ratio_equals_phi_squared"] = (
    qdiv(pair_A, pair_B) == phi2
)

print(
    "NORMALIZED_AA_PAIR_WEIGHT:",
    "(5+sqrt(5))/10",
)

print(
    "NORMALIZED_BB_PAIR_WEIGHT:",
    "(5-sqrt(5))/10",
)

print(
    "PAIR_SQUARE_MATCHES_PROGRAM02_CLASSES:",
    (
        checks["pair_A_equals_q_plus"]
        and checks["pair_B_equals_q_minus"]
    ),
)


# ------------------------------------------------------------
# Finite deterministic count witness.
#
# Start from Fibonacci counts and form the integer pair counts
#
#     A_n^2
#     B_n^2.
#
# Every finite generation is rational. Their normalized limit is
# the irrational Program-02 class measure.
# ------------------------------------------------------------

print("PROGRESS: 4/6 generate finite pair-count convergence")

A = 1
B = 0

rows = []

for n in range(31):
    AA = A*A
    BB = B*B
    total = AA + BB

    if total:
        pAA = AA / total
        pBB = BB / total
    else:
        pAA = 0.0
        pBB = 0.0

    rows.append({
        "generation": n,
        "A": A,
        "B": B,
        "AA": AA,
        "BB": BB,
        "pair_total": total,
        "normalized_AA": pAA,
        "normalized_BB": pBB,
    })

    A, B = A + B, A

last = rows[-1]

err_plus = abs(
    last["normalized_AA"]
    - qnum(q_plus)
)

err_minus = abs(
    last["normalized_BB"]
    - qnum(q_minus)
)

checks["generation30_pair_plus_converges"] = (
    err_plus < 1.0e-12
)

checks["generation30_pair_minus_converges"] = (
    err_minus < 1.0e-12
)

print(
    "GENERATION_30_PAIR_COUNTS:",
    (
        last["AA"],
        last["BB"],
    ),
)

print(
    "GENERATION_30_NORMALIZED_AA:",
    last["normalized_AA"],
)

print(
    "GENERATION_30_NORMALIZED_BB:",
    last["normalized_BB"],
)

print(
    "TARGET_Q_PLUS:",
    qnum(q_plus),
)

print(
    "TARGET_Q_MINUS:",
    qnum(q_minus),
)

print(
    "Q_PLUS_ERROR:",
    err_plus,
)

print(
    "Q_MINUS_ERROR:",
    err_minus,
)


# ------------------------------------------------------------
# Balanced binary duplication.
#
# Program02 zero local marginals force the two binary outcomes inside
# each correlation-sign class to have equal weights.
#
# Therefore splitting q_plus and q_minus into two equal receipts gives
# exactly w_plus and w_minus.
# ------------------------------------------------------------

print("PROGRESS: 5/6 recover four binary weights")

recovered_w_plus = qscale(
    Fraction(1, 2),
    pair_A,
)

recovered_w_minus = qscale(
    Fraction(1, 2),
    pair_B,
)

checks["balanced_split_recovers_w_plus"] = (
    recovered_w_plus == w_plus
)

checks["balanced_split_recovers_w_minus"] = (
    recovered_w_minus == w_minus
)

print(
    "RECOVERED_W_PLUS:",
    "1/4+sqrt(5)/20",
)

print(
    "RECOVERED_W_MINUS:",
    "1/4-sqrt(5)/20",
)

print(
    "FOUR_WEIGHT_MATCH:",
    (
        checks["balanced_split_recovers_w_plus"]
        and checks["balanced_split_recovers_w_minus"]
    ),
)


# ------------------------------------------------------------
# Classification.
# ------------------------------------------------------------

print("PROGRESS: 6/6 classify")

failed = [
    name
    for name, passed
    in checks.items()
    if not passed
]

audit_pass = not failed

verdict = (
    "the_Program02_nontrivial_binary_weights_are_exactly_the_"
    "balanced_split_of_the_normalized_same_class_pair_square_measure_"
    "generated_from_the_Fibonacci_finite_rule_limiting_frequencies"
    if audit_pass
    else
    "joint_pair_square_witness_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_joint_pair_square_witness_003",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "Fibonacci_measure": {
        "fA":
            "(sqrt(5)-1)/2",

        "fB":
            "(3-sqrt(5))/2",

        "ratio":
            "phi",
    },

    "Program02_two_class_measure": {
        "q_plus":
            "(5+sqrt(5))/10",

        "q_minus":
            "(5-sqrt(5))/10",

        "ratio":
            "phi^2",
    },

    "pair_square_identity": {
        "q_plus":
            "fA^2/(fA^2+fB^2)",

        "q_minus":
            "fB^2/(fA^2+fB^2)",

        "exact":
            True,
    },

    "balanced_binary_split": {
        "w_plus":
            "q_plus/2 = 1/4+sqrt(5)/20",

        "w_minus":
            "q_minus/2 = 1/4-sqrt(5)/20",
    },

    "finite_generation_witness": {
        "generation":
            30,

        "AA_count":
            last["AA"],

        "BB_count":
            last["BB"],

        "AA_normalized":
            last["normalized_AA"],

        "BB_normalized":
            last["normalized_BB"],

        "q_plus_error":
            err_plus,

        "q_minus_error":
            err_minus,
    },

    "checks":
        checks,

    "boundary": {
        "target_informed_witness":
            True,

        "Fibonacci_rule_claimed_native":
            False,

        "pair_square_operation_claimed_native":
            False,

        "same_class_pair_condition_claimed_native":
            False,

        "Born_rule_used":
            False,

        "irrational_probability_inserted_into_rule":
            False,

        "Program02_weights_inserted_into_recurrence":
            False,

        "native_frequency_correspondence_closed":
            False,
    },

    "earned_statement": (
        "The Program-02 nontrivial binary weights admit an exact "
        "finite-rule correspondence witness. The Fibonacci integer "
        "substitution generates limiting frequencies fA and fB with "
        "ratio phi. Forming same-class pair counts gives limiting "
        "masses proportional to fA^2 and fB^2, whose normalized ratio "
        "is phi^2. These normalized pair masses are exactly "
        "(5+sqrt(5))/10 and (5-sqrt(5))/10. Splitting each class "
        "equally across its two symmetry-related binary receipts gives "
        "the exact Program-02 weights 1/4 +/- sqrt(5)/20. No "
        "irrational constant or probability is inserted into the "
        "finite recurrence. This is a target-informed construction "
        "witness, not yet native provenance."
    ),

    "next_gate": (
        "Determine whether a native joint registered process supplies "
        "the pair-product and balanced-split operations used by this "
        "witness. If not, reject the witness as non-native rather than "
        "promoting it to a correspondence law."
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

note = f"""# Joint pair-square witness 003

## Result

Audit pass:

    {audit_pass}

The Fibonacci finite rule generates limiting frequencies

    f_A = (sqrt(5)-1)/2
    f_B = (3-sqrt(5))/2

with

    f_A / f_B = phi.

Program 02 requires the two nontrivial correlation-class masses

    q_plus  = (5+sqrt(5))/10
    q_minus = (5-sqrt(5))/10.

Their ratio is

    q_plus / q_minus = phi^2.

Exactly,

    q_plus
      =
    f_A^2 / (f_A^2 + f_B^2)

and

    q_minus
      =
    f_B^2 / (f_A^2 + f_B^2).

Thus integer Fibonacci counts A_n and B_n produce integer joint pair counts

    A_n^2
    B_n^2,

whose normalized proportions converge to the exact Program-02 class masses.

A balanced two-way split then gives

    w_plus  = q_plus/2
    w_minus = q_minus/2,

which are exactly

    1/4 + sqrt(5)/20

and

    1/4 - sqrt(5)/20.

## Boundary

This is target-informed.

The Fibonacci substitution is not yet native Thalean dynamics.

The pair-square operation is not yet derived from the apparatus.

The same-class restriction is not yet derived from the apparatus.

No Born rule or irrational transition probability is inserted.

## Next gate

Ask whether native joint registration itself supplies:

    product pairing
      + same-class closure
      + balanced binary split.

If it does, this witness becomes a correspondence candidate.

If it does not, reject it.
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
    "PAIR_SQUARE_MATCH:",
    checks["pair_A_equals_q_plus"]
    and checks["pair_B_equals_q_minus"],
)

print(
    "BALANCED_SPLIT_MATCH:",
    checks["balanced_split_recovers_w_plus"]
    and checks["balanced_split_recovers_w_minus"],
)

print(
    "NEXT_GATE:",
    "native_joint_pair_product_provenance",
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
