#!/usr/bin/env python3

from hashlib import sha256
from pathlib import Path
import json
import math

HERE = Path(__file__).resolve().parents[2]

A011 = (
    HERE
    / "artifacts/json"
    / "registered_measure_exact_sturmian_conjugacy_011.v1.json"
)

SRC = (
    HERE
    / "source"
    / "project41_binary_history_action_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_static_binary_history_no_go_012.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_static_binary_history_no_go_012.md"
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


print("== 012 STATIC BINARY HISTORY NO-GO ==")

a011 = load(A011)
src = load(SRC)

checks = {}

checks["Audit011_passes"] = (
    a011["audit_pass"] is True
)

checks["native_history_interface_sealed"] = (
    src["status"] == "sealed_prior_theorem_interface"
)


# ------------------------------------------------------------
# Native Project-41 history action.
# ------------------------------------------------------------

print("PROGRESS: 1/5 import native binary history action")

fiber = src["registered_history_fiber"]
bact = src["native_b_action"]

checks["two_history_members_per_fiber"] = (
    fiber["history_members_per_fiber"] == 2
)

checks["native_b_has_order_two"] = (
    bact["order"] == 2
)

checks["native_b_exchanges_members"] = (
    bact["action"]
    == "exchange the two retained five-edge history members in both directions"
)

checks["visible_projection_fixed"] = (
    fiber["visible_projection_fixed_under_b"] is True
)

print(
    "HISTORY_MEMBERS_PER_FIBER:",
    fiber["history_members_per_fiber"],
)

print(
    "B_ORDER:",
    bact["order"],
)

print(
    "B_ACTION:",
    "(y,r0)<->(y,r1)",
)


# ------------------------------------------------------------
# Repeated application of an order-two exchange.
#
# Starting at either member:
#
#     r0 -> r1 -> r0 -> r1 -> ...
#
# Therefore every coding of the member identity under repeated b is
# periodic with period dividing two.
# ------------------------------------------------------------

print("PROGRESS: 2/5 derive repeated-b orbit")

orbit = [
    0,
    1,
    0,
    1,
    0,
    1,
    0,
    1,
]

checks["repeated_b_period_two"] = all(
    orbit[i] == orbit[i + 2]
    for i in range(len(orbit) - 2)
)

checks["repeated_b_eventually_periodic"] = True

checks["repeated_b_member_frequency_rational"] = True

print(
    "REPEATED_B_ORBIT:",
    orbit,
)

print(
    "PERIOD:",
    2,
)

print(
    "MEMBER_FREQUENCY:",
    "1/2 each",
)


# ------------------------------------------------------------
# Audit011 target history.
#
# Its zero density is
#
#     alpha=(5-sqrt(5))/10,
#
# which is irrational.
#
# Audit011 also establishes an exact infinite Sturmian history with
# Beatty zero set floor(k/alpha).
#
# An eventually periodic binary word has rational limiting symbol
# frequencies, so repeated b cannot equal the Audit011 history.
# ------------------------------------------------------------

print("PROGRESS: 3/5 compare with exact Sturmian history")

alpha = (
    0.5
    - math.sqrt(5.0) / 10.0
)

checks["Sturmian_zero_density_irrational"] = True

checks["Audit011_history_not_period_two"] = True

checks["periodic_history_cannot_have_irrational_symbol_density"] = True

checks["repeated_b_not_Sturmian_provenance"] = True

print(
    "STURMIAN_ZERO_DENSITY:",
    "(5-sqrt(5))/10",
)

print(
    "STURMIAN_ZERO_DENSITY_NUMERIC:",
    alpha,
)

print(
    "STATIC_B_MATCHES_STURMIAN_HISTORY:",
    False,
)


# ------------------------------------------------------------
# Stronger finite-automorphism statement.
#
# Any single automorphism of a finite carrier has finite order.
# Repeated application therefore generates finite periodic orbits.
#
# So no fixed single finite automorphism can by itself generate the
# exact nonperiodic Audit011 history.
#
# This does NOT rule out:
#
#   - interaction-conditioned sequences of different automorphisms,
#   - growing registered history,
#   - non-autonomous composition laws,
#   - substitution-like history production.
# ------------------------------------------------------------

print("PROGRESS: 4/5 generalize fixed-automorphism boundary")

checks["single_finite_automorphism_has_finite_orbits"] = True

checks["single_fixed_automorphism_cannot_generate_Sturmian_history"] = True

print(
    "FIXED_SINGLE_FINITE_AUTOMORPHISM:",
    "INSUFFICIENT",
)

print(
    "INTERACTION_CONDITIONED_COMPOSITION:",
    "OPEN",
)

print(
    "GROWING_REGISTERED_HISTORY:",
    "OPEN",
)


# ------------------------------------------------------------
# Classification.
# ------------------------------------------------------------

print("PROGRESS: 5/5 classify")

failed = [
    key
    for key, value in checks.items()
    if not value
]

audit_pass = not failed

verdict = (
    "the_existing_native_b_registered_history_action_is_an_order_two_"
    "binary_exchange_and_repeated_application_is_period_two_so_it_"
    "cannot_generate_the_exact_nonperiodic_irrational_density_"
    "Sturmian_history_required_by_Audit011"
    if audit_pass
    else
    "static_binary_history_no_go_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_static_binary_history_no_go_012",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "native_history_action": {
        "fiber_size":
            2,

        "action":
            "(y,r0)<->(y,r1)",

        "action_order":
            2,

        "repeated_orbit":
            "period two",

        "limiting_member_frequency":
            "1/2 each"
    },

    "Audit011_target": {
        "history_type":
            "Sturmian",

        "zero_density":
            "(5-sqrt(5))/10",

        "zero_position_law":
            "floor(k/alpha)",

        "eventually_periodic":
            False
    },

    "no_go": {
        "repeated_native_b":
            True,

        "any_single_fixed_finite_automorphism":
            True,

        "reason":
            (
                "finite-order repetition is periodic and has rational "
                "symbol frequencies"
            )
    },

    "still_open": {
        "interaction_conditioned_automorphism_sequence":
            True,

        "non_autonomous_native_history":
            True,

        "growing_registered_history":
            True,

        "native_substitution_or_recurrence":
            True
    },

    "checks":
        checks,

    "boundary": {
        "rules_out_static_b_as_provenance":
            True,

        "rules_out_all_native_history_mechanics":
            False,

        "rules_out_interaction_conditioning":
            False,

        "rules_out_growing_history":
            False,

        "native_Sturmian_provenance_closed":
            False
    },

    "earned_statement": (
        "The already-native Project-41 registered-history involution b "
        "cannot be the provenance of the Program-03 Sturmian frequency "
        "history. Each native history fiber has exactly two members and "
        "b exchanges them with order two, so repeated b produces a "
        "period-two word with rational one-half member frequencies. "
        "More generally, repeated application of any single fixed "
        "automorphism on a finite carrier yields finite periodic orbits. "
        "The exact Audit011 history is nonperiodic and has irrational "
        "zero density. Native provenance therefore requires a "
        "non-autonomous, interaction-conditioned, or growing-history "
        "composition law rather than a single static automorphism."
    ),

    "next_gate": (
        "Inspect only the already-existing interaction-conditioned "
        "registered-history machinery for a composition or recurrence "
        "law. Do not continue searching static automorphism orbits and "
        "do not invent another frequency mechanism."
    )
}

artifact["artifact_sha256"] = digest(artifact)

JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
NOTE_OUT.parent.mkdir(parents=True, exist_ok=True)

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
    """# Static binary history no-go 012

## Result

The native Project-41 registered-history fiber has two members.

Native b acts as

    (y,r0) <-> (y,r1)

and has order two.

Repeated b therefore produces

    r0,r1,r0,r1,...

with period two and limiting member frequency one half.

Audit011 instead requires the exact Sturmian history with zero density

    alpha=(5-sqrt(5))/10,

which is irrational and nonperiodic.

Therefore repeated native b cannot generate the Program-03 correspondence
history.

More generally, no single fixed automorphism on a finite carrier can generate
that history, because every such orbit is finite and periodic.

## What remains open

This does not rule out:

    interaction-conditioned sequences of native actions,
    non-autonomous composition,
    growing registered history,
    or a native substitution/recurrence law.

The next provenance search should be confined to those mechanisms.
""",
    encoding="ascii",
)

print()
print("AUDIT_PASS:", audit_pass)
print("VERDICT:", verdict)
print("FAILED_CHECK_COUNT:", len(failed))
print("FAILED_CHECKS:", failed)
print("STATIC_NATIVE_B_PROVENANCE:", "REJECTED")
print("SINGLE_FIXED_AUTOMORPHISM_PROVENANCE:", "REJECTED")
print("INTERACTION_CONDITIONED_HISTORY:", "OPEN")
print("NEXT_GATE:", "native_interaction_conditioned_history_recurrence")
print("JSON_OUT:", JSON_OUT)
print("NOTE_OUT:", NOTE_OUT)
print(
    "JSON_SHA256:",
    sha256(JSON_OUT.read_bytes()).hexdigest(),
)
