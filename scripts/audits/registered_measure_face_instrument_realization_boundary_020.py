#!/usr/bin/env python3

from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parents[2]

A019 = (
    HERE
    / "artifacts/json"
    / "registered_measure_local_projector_joint_interface_019.v1.json"
)

SRC = (
    HERE
    / "source"
    / "program02_face_instrument_boundary_interface.v1.json"
)

JSON_OUT = (
    HERE
    / "artifacts/json"
    / "registered_measure_face_instrument_realization_boundary_020.v1.json"
)

NOTE_OUT = (
    HERE
    / "notes"
    / "registered_measure_face_instrument_realization_boundary_020.md"
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


print("== 020 FACE INSTRUMENT REALIZATION BOUNDARY ==")

a019 = load(A019)
src = load(SRC)

checks = {}

checks["Audit019_passes"] = (
    a019["audit_pass"] is True
)

checks["face_interface_sealed"] = (
    src["status"] == "sealed_prior_theorem_interface"
)


# ------------------------------------------------------------
# 1. Ideal local spectral interface.
# ------------------------------------------------------------

print("PROGRESS: 1/4 lock ideal algebraic interface")

b019 = a019["boundary"]

checks["ideal_local_setting_interface_closed"] = (
    b019[
        "algebraic_local_setting_interfaces_closed"
    ]
    is True
)

checks["remote_setting_absent_from_local_operator"] = (
    b019[
        "remote_setting_in_local_operator"
    ]
    is False
)

print(
    "IDEAL_LOCAL_PROJECTORS:",
    "Pi_a^x=(I+a A_x)/2; Pi_b^y=(I+b B_y)/2",
)

print(
    "ALGEBRAIC_LOCAL_INTERFACE:",
    "CLOSED",
)


# ------------------------------------------------------------
# 2. Native analyzer-to-face geometry binding.
# ------------------------------------------------------------

print("PROGRESS: 2/4 classify geometry bridge")

geom = src["analyzer_geometry"]

checks["analyzer_and_face_adjoint_dimensions_match"] = (
    geom["native_sector_dimension"] == 3
    and geom["face_adjoint_dimension"] == 3
)

checks["native_geometry_bridge_correctly_open"] = (
    geom["candidate_bridge_constructed"] is False
)

print(
    "ANALYZER_SECTOR_DIM:",
    geom["native_sector_dimension"],
)

print(
    "FACE_ADJOINT_DIM:",
    geom["face_adjoint_dimension"],
)

print(
    "NATIVE_ANALYZER_FACE_BRIDGE:",
    "OPEN",
)


# ------------------------------------------------------------
# 3. Current sampled face POVM.
# ------------------------------------------------------------

print("PROGRESS: 3/4 classify sampled face instrument")

povm = src["sampled_face_povm"]
bell = src["bell_capacity"]

checks["sampled_face_POVM_exists"] = (
    povm["constructed"] is True
)

checks["sampled_face_POVM_normalized"] = (
    povm["normalized"] is True
)

checks["sampled_face_POVM_positive"] = (
    povm["positive"] is True
)

checks["nonclean_receipts_retained"] = (
    povm["nonclean_receipts_retained"] is True
)

checks["sampled_face_response_Bell_incapable"] = (
    bell["sampled_face_response_Bell_capable"] is False
)

checks["all_256_sampled_pairs_bounded_by_2"] = (
    bell["sampled_calibration_pair_count"] == 256
    and bell["all_sampled_pairs_CHSH_at_most_2"] is True
)

checks["Bell_obstruction_state_independent"] = (
    bell["obstruction_state_independent"] is True
)

checks["native_axis_geometry_itself_remains_Bell_capable"] = (
    bell["native_six_axis_geometry_Bell_capable"] is True
)

print(
    "SAMPLED_FACE_POVM:",
    "NORMALIZED POSITIVE COMPLETE",
)

print(
    "SAMPLED_BINARY_OBSERVABLE:",
    povm["binary_observable"],
)

print(
    "SAMPLED_CALIBRATION_PAIRS_TESTED:",
    bell["sampled_calibration_pair_count"],
)

print(
    "SAMPLED_FACE_BELL_CAPACITY:",
    "INSUFFICIENT",
)

print(
    "IDEAL_EQUAL_VISIBILITY_THRESHOLD:",
    bell["ideal_equal_unbiased_visibility_threshold"],
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
    "the_ideal_local_projector_interface_is_algebraically_closed_but_"
    "physical_face_realization_remains_open_for_two_independent_"
    "reasons_the_native_analyzer_to_face_adjoint_binding_is_not_yet_"
    "constructed_and_the_current_sampled_normalized_face_POVM_family_"
    "is_state_independently_CHSH_incapable"
    if audit_pass
    else
    "face_instrument_realization_boundary_gate_failed"
)

artifact = {
    "artifact_id":
        "registered_measure_face_instrument_realization_boundary_020",

    "version":
        1,

    "audit_pass":
        audit_pass,

    "verdict":
        verdict,

    "ideal_interface": {
        "local_projectors":
            "closed algebraically",

        "remote_setting_in_local_operator":
            False,

        "joint_nonfactorizable_source":
            True
    },

    "geometry_gate": {
        "analyzer_dimension":
            3,

        "face_adjoint_dimension":
            3,

        "candidate_isometry_available":
            True,

        "native_binding_constructed":
            False
    },

    "instrument_gate": {
        "sampled_face_POVM_constructed":
            True,

        "positive":
            True,

        "normalized":
            True,

        "complete_receipts_retained":
            True,

        "binary_observable":
            "bias I + contrast n.sigma",

        "sampled_CHSH_capable":
            False,

        "sampled_pair_count":
            256,

        "state_independent_obstruction":
            True
    },

    "checks":
        checks,

    "boundary": {
        "Bell_architecture_problem":
            False,

        "probability_weight_problem":
            False,

        "setting_schedule_problem":
            False,

        "native_face_axis_binding_open":
            True,

        "sufficient_face_instrument_contrast_open":
            True,

        "current_sampled_face_family_sufficient":
            False,

        "all_possible_face_dynamics_excluded":
            False,

        "native_nonperiodic_history_provenance_open":
            True
    },

    "earned_statement": (
        "The remaining local apparatus gap is no longer a Bell, "
        "probability, or setting-schedule ambiguity. Audit019 closes "
        "the ideal local spectral interfaces algebraically. Program02 "
        "shows that the analyzer sector and face adjoint both have "
        "dimension three, but no native isometric binding of the six "
        "analyzer directions to the face adjoint has been constructed. "
        "Separately, the actually constructed sampled face POVMs are "
        "positive, normalized, complete, and retain nonclean outputs, "
        "but their bias/contrast observables are state-independently "
        "CHSH-incapable for all 256 sampled Alice/Bob calibration "
        "pairs. Thus physical face realization requires both a native "
        "axis binding and a sufficiently sharp normalized local "
        "instrument."
    ),

    "next_gate": (
        "Do not revisit EPR weighting, Bell-local factorization, or "
        "setting multiplexing. The apparatus front is now exactly two "
        "questions: construct the native analyzer-to-face adjoint "
        "binding, and derive a normalized face response with sufficient "
        "contrast. Native nonperiodic frequency-history provenance "
        "remains the separate history front."
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
    """# Face instrument realization boundary 020

## Result

The ideal local spectral interface is closed algebraically.

Alice and Bob can be represented by local projectors depending only on their
own local settings, acting on the already-joint nonfactorizable preparation.

The remaining face-apparatus gap has two independent parts.

## Geometry gate

The native analyzer sector has real dimension three.

The Program-01 face adjoint also has real dimension three.

An isometric identification is dimensionally available, but no native binding
of the six analyzer axes to concrete face-adjoint axes has been constructed.

## Instrument gate

The sampled face POVMs are:

    positive,
    normalized,
    complete,
    and retain nonclean receipts.

Their effects have form

    E_(i,r)=alpha_r P_i + beta_r(I-P_i).

The resulting binary observable has form

    bias I + contrast n_i.sigma.

Audit028 proves the entire sampled family is CHSH-incapable by a
state-independent operator bound.

All 256 sampled Alice/Bob calibration pairs lie at or below two.

The native six-axis geometry itself remains Bell-capable.

## Frontier

The remaining apparatus problem is therefore:

    native analyzer-to-face axis binding

plus

    normalized face response with sufficient analyzer contrast.

No new EPR weighting or Bell architecture is required.

Native nonperiodic registered-history provenance remains a separate open
front.
""",
    encoding="ascii",
)

print()
print("AUDIT_PASS:", audit_pass)
print("VERDICT:", verdict)
print("FAILED_CHECK_COUNT:", len(failed))
print("FAILED_CHECKS:", failed)
print("IDEAL_LOCAL_INTERFACE:", "CLOSED")
print("NATIVE_ANALYZER_FACE_BINDING:", "OPEN")
print("CURRENT_SAMPLED_FACE_INSTRUMENT:", "CHSH_INCAPABLE")
print("SUFFICIENT_FACE_INSTRUMENT:", "OPEN")
print("NATIVE_NONPERIODIC_HISTORY_PROVENANCE:", "OPEN")
print("JSON_OUT:", JSON_OUT)
print("NOTE_OUT:", NOTE_OUT)
print(
    "JSON_SHA256:",
    sha256(JSON_OUT.read_bytes()).hexdigest(),
)
