#!/usr/bin/env python3

from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parents[2]

A017 = (
    HERE
    / "artifacts/json"
    / "registered_measure_joint_registration_causal_boundary_017.v1.json"
)

BELL = (
    HERE
    / "source"
    / "program02_bell_local_factorization_obstruction.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_bell_local_causal_boundary_018.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_bell_local_causal_boundary_018.md"
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


print("== 018 BELL-LOCAL CAUSAL BOUNDARY ==")

a017 = load(A017)
bell = load(BELL)

checks = {}

checks["Audit017_passes"] = (
    a017["audit_pass"] is True
)

checks["Bell_obstruction_interface_sealed"] = (
    bell["status"] == "sealed_prior_theorem_interface"
)


print("PROGRESS: 1/4 lock Bell-local factorization obstruction")

checks["deterministic_vertex_count_16"] = (
    bell[
        "deterministic_vertices"
    ][
        "count"
    ]
    == 16
)

checks["deterministic_CHSH_abs_2"] = (
    bell[
        "deterministic_vertices"
    ][
        "CHSH_absolute_value"
    ]
    == 2
)

checks["positive_local_convex_bound_2"] = (
    bell[
        "convex_extension"
    ][
        "all_positive_setting_independent_local_models_obey_CHSH_bound"
    ]
    == 2
)

checks["target_outside_local_polytope"] = (
    bell[
        "target"
    ][
        "outside_Bell_local_polytope"
    ]
    is True
)

print(
    "BELL_LOCAL_FACTOR_FORM:",
    "P(a,b|x,y,lambda)=P(a|x,lambda)P(b|y,lambda)",
)

print(
    "BELL_LOCAL_CHSH_BOUND:",
    2,
)

print(
    "TARGET_CHSH:",
    bell["target"]["CHSH"],
)


print("PROGRESS: 2/4 reclassify local-output target")

checks["Bell_local_factorized_generator_excluded"] = (
    bell[
        "boundary"
    ][
        "Bell_local_factorized_generator_excluded"
    ]
    is True
)

checks["joint_nonfactorizable_registration_not_excluded"] = (
    bell[
        "boundary"
    ][
        "joint_relational_registration_excluded"
    ]
    is False
)

print(
    "BELL_LOCAL_FACTORIZED_OUTPUT_GENERATOR:",
    "EXCLUDED",
)

print(
    "NONFACTORIZABLE_JOINT_RELATIONAL_REGISTRATION:",
    "OPEN",
)


print("PROGRESS: 3/4 preserve no-signaling / causality distinction")

causal = a017["causal_boundary"]

checks["table_level_no_signaling_closed"] = (
    causal[
        "statistical_no_signaling"
    ]
    == "closed at algebraic/registration level"
)

checks["Alice_local_interface_open"] = (
    causal[
        "Alice_output_generated_from_x_alone"
    ]
    == "open"
)

checks["Bob_local_interface_open"] = (
    causal[
        "Bob_output_generated_from_y_alone"
    ]
    == "open"
)

print(
    "STATISTICAL_NO_SIGNALING:",
    "CLOSED",
)

print(
    "CLASSICAL_BELL_LOCAL_CAUSAL_FACTORIZATION:",
    "EXCLUDED",
)

print(
    "LOCAL_INTERFACE_TO_NONFACTORIZABLE_JOINT_OBJECT:",
    "OPEN",
)


print("PROGRESS: 4/4 classify")

failed = [
    key
    for key, value in checks.items()
    if not value
]

audit_pass = not failed

verdict = (
    "the_remaining_operational_interface_cannot_be_a_setting_"
    "independent_Bell_local_factorized_output_generator_because_that_"
    "class_is_already_excluded_by_CHSH_while_a_no_signaling_"
    "nonfactorizable_joint_relational_registration_with_local_setting_"
    "interfaces_remains_the_correct_open_target"
    if audit_pass
    else
    "Bell_local_causal_boundary_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_bell_local_causal_boundary_018",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "excluded_architecture": {
        "form":
            "P(a,b|x,y,lambda)=P(a|x,lambda)P(b|y,lambda)",

        "source_distribution":
            "positive and setting-independent",

        "CHSH_bound":
            2,

        "status":
            "excluded"
    },

    "target_architecture": {
        "joint_preparation":
            "canonical nonfactorizable relational object",

        "setting_interfaces":
            "Alice x and Bob y remain local inputs",

        "joint_receipt":
            "nonfactorizable",

        "statistical_no_signaling":
            True,

        "operational_realization":
            "open"
    },

    "checks":
        checks,

    "boundary": {
        "Bell_local_factorized_output_generation_open":
            False,

        "Bell_local_factorized_output_generation_excluded":
            True,

        "no_signaling_joint_registration_closed":
            True,

        "local_setting_interface_to_joint_relation_closed":
            False,

        "native_nonperiodic_history_provenance_closed":
            False
    },

    "earned_statement": (
        "The remaining operational problem must not be described as "
        "finding a Bell-local spacelike output generator. Program-02 "
        "Audit039 already excludes every positive setting-independent "
        "local factorization, including stochastic models through their "
        "convex decomposition into deterministic local vertices. The "
        "target CHSH value lies outside that polytope. What remains "
        "operationally open is a realization in which Alice and Bob "
        "retain local setting interfaces to an already-joint "
        "nonfactorizable relational preparation, while the final "
        "conditional tables remain no-signaling."
    ),

    "next_gate": (
        "Inspect the native Alice/Bob face apparatus only for an "
        "interface to the nonfactorizable joint preparation. Do not "
        "seek a classical setting-independent local hidden response "
        "factorization, because that architecture is already ruled out."
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
    """# Bell-local causal boundary 018

## Result

The remaining operational interface is not an open search for a
Bell-local factorized outcome generator.

Any model of the form

    P(a,b|x,y,lambda)
      =
    P(a|x,lambda) P(b|y,lambda)

with positive setting-independent source weights lies inside the Bell-local
polytope and obeys

    |CHSH| <= 2.

The Program-02 target has

    CHSH = 1 + 3/sqrt(5) > 2.

Therefore that architecture is excluded.

## Correct open target

The open operational problem is:

    local Alice setting interface x
      +
    local Bob setting interface y
      +
    already-joint nonfactorizable relational preparation
      ->
    joint registered receipts

while retaining statistical no-signaling.

This must not be replaced by preassigned local counterfactual answers.

## Remaining deep fronts

1. Operational local interfaces to the nonfactorizable joint relation.

2. Native provenance of the nonperiodic registered history.

These are distinct problems.
""",
    encoding="ascii",
)

print()
print("AUDIT_PASS:", audit_pass)
print("VERDICT:", verdict)
print("FAILED_CHECK_COUNT:", len(failed))
print("FAILED_CHECKS:", failed)
print(
    "BELL_LOCAL_FACTORIZED_OUTPUT_GENERATOR:",
    "EXCLUDED",
)
print(
    "NONFACTORIZABLE_JOINT_RELATIONAL_REALIZATION:",
    "OPEN",
)
print(
    "STATISTICAL_NO_SIGNALING:",
    "CLOSED",
)
print(
    "NATIVE_NONPERIODIC_HISTORY_PROVENANCE:",
    "OPEN",
)
print("JSON_OUT:", JSON_OUT)
print("NOTE_OUT:", NOTE_OUT)
print(
    "JSON_SHA256:",
    sha256(JSON_OUT.read_bytes()).hexdigest(),
)
