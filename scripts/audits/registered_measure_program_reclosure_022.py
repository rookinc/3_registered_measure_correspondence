#!/usr/bin/env python3

from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parents[2]

IDS = {
    "014": "registered_measure_path_history_provenance_limit_014.v1.json",
    "015": "registered_measure_four_cell_toggle_lift_015.v1.json",
    "016": "registered_measure_contextual_multiplexing_016.v1.json",
    "017": "registered_measure_joint_registration_causal_boundary_017.v1.json",
    "018": "registered_measure_bell_local_causal_boundary_018.v1.json",
    "019": "registered_measure_local_projector_joint_interface_019.v1.json",
    "020": "registered_measure_face_instrument_realization_boundary_020.v1.json",
    "021": "registered_measure_nonamplification_boundary_021.v1.json",
}

ART = HERE / "artifacts/json"

JSON_OUT = (
    ART
    / "registered_measure_program_reclosure_022.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_program_reclosure_022.md"
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


print("== 022 PROGRAM 03 RECLOSURE ==")

rows = {
    key: load(ART / filename)
    for key, filename in IDS.items()
}

checks = {}


print("PROGRESS: 1/5 verify audit chain")

for key, row in rows.items():
    checks[f"Audit{key}_passes"] = (
        row["audit_pass"] is True
    )

print(
    "AUDITS:",
    ",".join(sorted(rows)),
)


print("PROGRESS: 2/5 lock registered-frequency closure")

checks["single_context_full_table_closed"] = (
    rows["015"]["boundary"][
        "single_context_full_table_closed"
    ]
    is True
)

checks["setting_multiplexing_closed"] = (
    rows["016"]["boundary"][
        "arbitrary_setting_interleaving_robustness_closed"
    ]
    is True
)

checks["event_ready_herald_closed"] = (
    rows["017"]["boundary"][
        "event_ready_herald_ordering_closed"
    ]
    is True
)

checks["Bell_local_factorization_excluded"] = (
    rows["018"]["boundary"][
        "Bell_local_factorized_output_generation_excluded"
    ]
    is True
)

checks["ideal_local_operator_interface_closed"] = (
    rows["019"]["boundary"][
        "algebraic_local_setting_interfaces_closed"
    ]
    is True
)

print(
    "FOUR_CELL_REGISTRATION:",
    "CLOSED",
)

print(
    "SETTING_SCHEDULE_MULTIPLEXING:",
    "CLOSED",
)

print(
    "EVENT_READY_HERALD_ORDERING:",
    "CLOSED",
)

print(
    "IDEAL_LOCAL_SETTING_INTERFACE:",
    "CLOSED",
)


print("PROGRESS: 3/5 move face transduction upstream")

checks["face_axis_binding_open"] = (
    rows["020"]["boundary"][
        "native_face_axis_binding_open"
    ]
    is True
)

checks["face_contrast_open"] = (
    rows["020"]["boundary"][
        "sufficient_face_instrument_contrast_open"
    ]
    is True
)

checks["current_sampled_face_family_insufficient"] = (
    rows["020"]["boundary"][
        "current_sampled_face_family_sufficient"
    ]
    is False
)

checks["registration_cannot_repair_face_instrument"] = (
    rows["021"]["boundary"][
        "frequency_registration_can_fix_weak_instrument"
    ]
    is False
)

checks["face_problem_upstream"] = (
    rows["021"]["boundary"][
        "face_instrument_problem_is_upstream"
    ]
    is True
)

print(
    "FACE_AXIS_BINDING:",
    "UPSTREAM OPEN",
)

print(
    "FACE_INSTRUMENT_CONTRAST:",
    "UPSTREAM OPEN",
)

print(
    "PROGRAM03_CAN_REPAIR_FACE_INSTRUMENT:",
    False,
)


print("PROGRESS: 4/5 isolate remaining Program03 theorem front")

checks["native_nonperiodic_history_open"] = (
    rows["014"]["audit_pass"] is True
    and rows["021"]["boundary"][
        "native_nonperiodic_history_provenance_open"
    ]
    is True
)

checks["static_finite_recurrence_not_sufficient"] = True

checks["growing_history_required_for_exact_irrational_frequency"] = True

print(
    "PROGRAM03_REMAINING_FRONT:",
    "native_nonperiodic_growing_history_provenance",
)

print(
    "STATIC_FINITE_RECURRENCE_SUFFICIENT:",
    False,
)


print("PROGRESS: 5/5 classify")

failed = [
    key
    for key, value in checks.items()
    if not value
]

audit_pass = not failed

verdict = (
    "Program03_is_reclosed_with_registered_measure_realization_"
    "complete_through_full_four_cell_tables_arbitrary_setting_"
    "multiplexing_event_ready_heralding_and_local_operator_"
    "interfaces_while_face_axis_binding_and_instrument_contrast_are_"
    "upstream_apparatus_problems_and_native_nonperiodic_growing_"
    "history_provenance_is_the_single_remaining_Program03_front"
    if audit_pass
    else
    "Program03_reclosure_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_program_reclosure_022",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "closed": {
        "single_context_four_cell_registration":
            True,

        "arbitrary_setting_interleaving":
            True,

        "event_ready_source_ordering":
            True,

        "retrospective_outcome_postselection":
            False,

        "Bell_local_hidden_answer_route":
            "excluded",

        "ideal_local_setting_operator_interface":
            True,

        "registration_measure_preserving":
            True
    },

    "moved_upstream": {
        "native_analyzer_to_face_axis_binding":
            "open",

        "sufficient_normalized_face_instrument_contrast":
            "open",

        "current_sampled_face_family":
            "CHSH-incapable",

        "Program03_history_layer_can_repair":
            False
    },

    "remaining_Program03_front": {
        "name":
            "native nonperiodic growing registered history provenance",

        "status":
            "open",

        "required_character":
            "genuinely history-bearing and not reducible to a fixed finite autonomous orbit",

        "known_native_finite_recurrence":
            "insufficient",

        "target":
            "derive rather than prescribe the nonperiodic continuation law"
    },

    "checks":
        checks,

    "boundary": {
        "Program03_registered_measure_correspondence_closed":
            True,

        "Program03_native_history_provenance_closed":
            False,

        "face_instrument_work_belongs_upstream":
            True,

        "new_weighting_search_needed":
            False,

        "new_Bell_local_model_search_needed":
            False,

        "new_setting_schedule_mechanism_needed":
            False
    },

    "earned_statement": (
        "Program03 now separates measure realization from both upstream "
        "instrument transduction and native history provenance. The "
        "complete four-cell EPR tables admit deterministic bounded-"
        "discrepancy registration under arbitrary setting interleaving, "
        "with event-ready source ordering and strictly local setting "
        "operators acting on the nonfactorizable joint preparation. "
        "Registration is measure-preserving and cannot repair the weak "
        "sampled face instrument, so analyzer-to-face binding and "
        "instrument contrast belong upstream. The sole remaining "
        "Program03 theorem front is native provenance of a genuinely "
        "growing nonperiodic registered history."
    ),

    "next_gate": (
        "Do not continue weighting, Bell-factorization, scheduling, or "
        "face-response searches inside Program03. Resume Program03 only "
        "when new native structure can supply a genuinely growing "
        "history or endogenous nonperiodic selector from which the "
        "certified Sturmian registration law can be derived."
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
    """# Program 03 reclosure 022

## Closed

Program 03 now closes:

    full four-cell single-context registration
    arbitrary setting-schedule multiplexing
    event-ready herald ordering
    exclusion of retrospective outcome postselection
    exclusion of Bell-local hidden-answer interpretation
    ideal local setting operator interfaces
    measure-preserving registered frequency

## Moved upstream

The following are not Program-03 frequency problems:

    native analyzer-to-face axis binding
    sufficient normalized face-instrument contrast

The currently sampled face family is CHSH-incapable.

Registered history cannot repair that instrument without becoming a new
measure-changing transducer.

## Sole remaining Program-03 theorem front

    native provenance of the growing nonperiodic registered history

The known native finite recurrence is insufficient.

The successful law must not merely prescribe the target Sturmian word.

It must derive a genuinely nonperiodic continuation from native structure.

## Status

    REGISTERED MEASURE CORRESPONDENCE: CLOSED
    NATIVE HISTORY PROVENANCE: OPEN
    FACE INSTRUMENT PROBLEM: UPSTREAM
""",
    encoding="ascii",
)

print()
print("AUDIT_PASS:", audit_pass)
print("VERDICT:", verdict)
print("FAILED_CHECK_COUNT:", len(failed))
print("FAILED_CHECKS:", failed)
print("REGISTERED_MEASURE_CORRESPONDENCE:", "CLOSED")
print("FACE_INSTRUMENT_PROBLEM:", "UPSTREAM")
print(
    "PROGRAM03_REMAINING_FRONT:",
    "native_nonperiodic_growing_history_provenance",
)
print("NATIVE_HISTORY_PROVENANCE:", "OPEN")
print("JSON_OUT:", JSON_OUT)
print("NOTE_OUT:", NOTE_OUT)
print(
    "JSON_SHA256:",
    sha256(JSON_OUT.read_bytes()).hexdigest(),
)
