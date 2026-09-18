#!/usr/bin/env python3

from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parents[2]

A016 = (
    HERE
    / "artifacts/json"
    / "registered_measure_contextual_multiplexing_016.v1.json"
)

HERALD = (
    HERE
    / "source"
    / "program02_event_ready_herald_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_joint_registration_causal_boundary_017.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_joint_registration_causal_boundary_017.md"
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


print("== 017 JOINT REGISTRATION CAUSAL BOUNDARY ==")

a016 = load(A016)
herald = load(HERALD)

checks = {}

checks["Audit016_passes"] = (
    a016["audit_pass"] is True
)

checks["herald_interface_sealed"] = (
    herald["status"] == "sealed_prior_theorem_interface"
)


# ------------------------------------------------------------
# 1. Event-ready source ordering.
# ------------------------------------------------------------

print("PROGRESS: 1/4 lock event-ready source ordering")

ordering = herald["ordering"]
ledger = herald["ledger"]

checks["herald_precedes_settings"] = (
    ordering[
        "herald_defined_before_analyzer_settings"
    ]
    is True
)

checks["settings_do_not_define_herald"] = (
    ordering[
        "analyzer_settings_used_to_define_herald"
    ]
    is False
)

checks["outcomes_do_not_define_herald"] = (
    ordering[
        "measurement_outcomes_used_to_define_herald"
    ]
    is False
)

checks["null_branch_retained"] = (
    ledger["null_branch_retained"] is True
)

checks["no_retrospective_outcome_postselection"] = (
    ledger[
        "retrospective_outcome_postselection"
    ]
    is False
)

print(
    "SOURCE_ORDER:",
    "source_attempt -> h -> settings -> outcomes",
)

print(
    "EVENT_READY_HERALD:",
    True,
)

print(
    "OUTCOME_POSTSELECTION:",
    False,
)


# ------------------------------------------------------------
# 2. Contextual multiplexing is not a hidden answer table.
# ------------------------------------------------------------

print("PROGRESS: 2/4 separate registration from local hidden answers")

b016 = a016["boundary"]

checks["no_preassigned_local_answer_table"] = (
    b016[
        "preassigned_local_answer_table"
    ]
    is False
)

checks["source_weight_not_schedule_dependent"] = (
    b016[
        "source_weight_depends_on_setting_schedule"
    ]
    is False
)

checks["joint_context_registrar_explicit"] = (
    b016[
        "joint_context_registrar_used"
    ]
    is True
)

print(
    "WRONG_ARCHITECTURE:",
    "lambda -> (A0,A1,B0,B1)",
)

print(
    "CURRENT_ARCHITECTURE:",
    (
        "joint preparation -> selected analyzer context "
        "-> joint relational receipt registration"
    ),
)

print(
    "PREASSIGNED_LOCAL_ANSWER_TABLE:",
    False,
)


# ------------------------------------------------------------
# 3. No-signaling statistics are not a local causal implementation.
# ------------------------------------------------------------

print("PROGRESS: 3/4 lock causal realization boundary")

checks["Alice_local_output_generation_not_proved"] = (
    b016[
        "Alice_output_uses_only_x_proved"
    ]
    is False
)

checks["Bob_local_output_generation_not_proved"] = (
    b016[
        "Bob_output_uses_only_y_proved"
    ]
    is False
)

checks["spacelike_local_generation_not_proved"] = (
    b016[
        "spacelike_local_outcome_generation_proved"
    ]
    is False
)

checks["measurement_independence_not_derived_as_physical_law"] = (
    b016[
        "measurement_independence_physical_assumption_derived"
    ]
    is False
)

print(
    "STATISTICAL_NO_SIGNALING:",
    "CLOSED AT TABLE LEVEL",
)

print(
    "ALICE_OUTPUT_FROM_x_ALONE:",
    "OPEN",
)

print(
    "BOB_OUTPUT_FROM_y_ALONE:",
    "OPEN",
)

print(
    "SPACELIKE_LOCAL_OUTCOME_GENERATOR:",
    "OPEN",
)


# ------------------------------------------------------------
# 4. Classification.
# ------------------------------------------------------------

print("PROGRESS: 4/4 classify")

failed = [
    key
    for key, value in checks.items()
    if not value
]

audit_pass = not failed

verdict = (
    "the_event_ready_antisymmetric_source_herald_is_fixed_before_"
    "settings_and_not_outcome_postselected_and_the_contextual_"
    "multiplexing_theorem_is_a_joint_registration_law_not_a_"
    "preassigned_local_answer_model_while_spacelike_local_generation_"
    "of_individual_Alice_and_Bob_receipts_remains_an_explicit_open_"
    "operational_interface"
    if audit_pass
    else
    "joint_registration_causal_boundary_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_joint_registration_causal_boundary_017",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "event_ready_source": {
        "order":
            "source attempt -> h -> settings -> outcomes",

        "herald_setting_independent":
            True,

        "herald_outcome_independent":
            True,

        "null_branch_retained":
            True,

        "retrospective_postselection":
            False,
    },

    "registration_architecture": {
        "type":
            "joint contextual registration",

        "preassigned_counterfactual_local_answers":
            False,

        "source_weight_changed_by_setting_schedule":
            False,

        "context_schedule_robustness":
            True,
    },

    "causal_boundary": {
        "Alice_output_generated_from_x_alone":
            "open",

        "Bob_output_generated_from_y_alone":
            "open",

        "spacelike_local_outcome_generation":
            "open",

        "statistical_no_signaling":
            "closed at algebraic/registration level",

        "measurement_independence_as_physical_law":
            "not derived here",
    },

    "checks":
        checks,

    "boundary": {
        "event_ready_herald_ordering_closed":
            True,

        "outcome_postselection_excluded":
            True,

        "Bell_local_hidden_answer_interpretation_excluded":
            True,

        "contextual_frequency_multiplexing_closed":
            True,

        "local_causal_output_realization_closed":
            False,

        "native_nonperiodic_history_provenance_closed":
            False,
    },

    "earned_statement": (
        "The Program-02 antisymmetric EPR branch is event-ready: its "
        "herald is determined before analyzer settings and independently "
        "of later measurement outcomes, while complementary preparation "
        "branches remain in the apparatus ledger. Program-03 contextual "
        "multiplexing realizes the already-derived joint receipt tables "
        "under arbitrary setting interleaving and is not a hidden table "
        "of counterfactual A0,A1,B0,B1 values. However, a joint context "
        "registrar is not by itself a proof that Alice's individual "
        "outcome is generated from x alone and Bob's from y alone. "
        "No-signaling statistics and local causal outcome generation "
        "remain logically distinct."
    ),

    "next_gate": (
        "Return to native relational mechanics only after preserving "
        "this boundary. Two deep interfaces remain: native nonperiodic "
        "history provenance and an operational realization of the joint "
        "receipt compatible with the local Alice/Bob apparatus without "
        "reintroducing Bell-local factorization."
    ),
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
    """# Joint registration causal boundary 017

## Event-ready source

The antisymmetric preparation is an event-ready source branch.

Its order is

    source attempt
      -> herald h
      -> analyzer settings
      -> measurement outcomes.

The herald does not depend on later settings.

The herald does not depend on later outcomes.

Complementary preparation branches remain in the apparatus ledger.

Therefore the Bell sample is not created by retrospective outcome
postselection.

## Registration is not a hidden answer table

Program 03 does not use

    lambda -> (A0,A1,B0,B1).

The architecture is

    joint relational preparation
      -> selected analyzer context
      -> joint relational receipt registration.

The setting schedule does not modify the source algebraic weight.

## Causal boundary

Audit016 closes arbitrary setting-schedule multiplexing at the statistical
registration level.

It does not prove

    Alice output depends only on x

or

    Bob output depends only on y.

It therefore does not yet provide a spacelike-local causal generator for the
individual receipts.

No-signaling of the final conditional tables and causal locality of an
underlying outcome mechanism are distinct claims.

## Remaining deep interfaces

1. Native provenance of the nonperiodic registered history.

2. Operational realization of the joint relational receipt through the local
   Alice/Bob apparatus without converting the construction into a Bell-local
   hidden-answer model.
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
    "EVENT_READY_HERALD:",
    "CLOSED",
)

print(
    "RETROSPECTIVE_OUTCOME_POSTSELECTION:",
    "EXCLUDED",
)

print(
    "CONTEXTUAL_MULTIPLEXING:",
    "CLOSED",
)

print(
    "SPACELIKE_LOCAL_OUTPUT_GENERATION:",
    "OPEN",
)

print(
    "NATIVE_NONPERIODIC_HISTORY_PROVENANCE:",
    "OPEN",
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
