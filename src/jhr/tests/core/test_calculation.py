"""
Tests for the core scientific calculation specification.

These tests verify validation, normalization, immutability,
and serialization independently of scientific simulation codes.
"""

import json

import pytest

from jhr.core.calculation import CalculationSpec, CalculationResult

@pytest.fixture
def orca_spec():
    """Return a representative ORCA geometry optimization specification."""
    return CalculationSpec(
        name="S0_opt",
        code="orca",
        task="optimization",
        parameters={
            "method": "PBE0",
            "basis": "def2-TZVP",
            "charge": 0,
            "multiplicity": 1,
        },
        code_options={
            "dispersion": "D3BJ",
        },
    )


def test_specification_creation(orca_spec):
    """A valid specification retains its scientific parameters."""
    assert orca_spec.name == "S0_opt"
    assert orca_spec.code == "orca"
    assert orca_spec.task == "optimization"
    assert orca_spec.parameters["method"] == "PBE0"


def test_identifier_normalization():
    """Code and task identifiers are normalized."""
    spec = CalculationSpec(
        name=" Test ",
        code="ORCA",
        task="OPTIMIZATION",
    )

    assert spec.name == "Test"
    assert spec.code == "orca"
    assert spec.task == "optimization"


def test_empty_identifier():
    """Empty identifiers are rejected."""
    with pytest.raises(ValueError):
        CalculationSpec(
            name="",
            code="orca",
            task="optimization",
        )


def test_serialization_roundtrip(orca_spec):
    """Serialization preserves the calculation specification."""
    data = orca_spec.to_dict()

    restored = CalculationSpec.from_dict(data)

    assert restored == orca_spec


def test_json_serialization(orca_spec):
    """Serialized specifications are JSON-compatible."""
    serialized = json.dumps(orca_spec.to_dict())

    assert isinstance(serialized, str)


def test_parameters_are_immutable(orca_spec):
    """Parameters cannot be modified after initialization."""
    with pytest.raises(TypeError):
        orca_spec.parameters["method"] = "B3LYP"


def test_nested_parameters_are_immutable():
    """Nested dictionaries and lists are recursively protected."""
    spec = CalculationSpec(
        name="test",
        code="orca",
        task="excited_states",
        code_options={
            "tddft": {
                "roots": [1, 2, 3],
            },
        },
    )

    with pytest.raises(TypeError):
        spec.code_options["tddft"]["roots"] = [4, 5]


def test_invalid_parameter_type():
    """Arbitrary Python objects are not valid specification values."""
    with pytest.raises(TypeError):
        CalculationSpec(
            name="test",
            code="orca",
            task="single_point",
            parameters={"object": object()},
        )


def test_invalid_floating_point():
    """Non-finite floating-point values are rejected."""
    with pytest.raises(ValueError):
        CalculationSpec(
            name="test",
            code="orca",
            task="single_point",
            parameters={"threshold": float("nan")},
        )

def test_result_creation():
    """A result stores scientific properties and convergence."""
    result = CalculationResult(
        status="completed",
        converged=True,
        properties={"total_energy": -100.5},
        units={"total_energy": "eV"},
    )

    assert result.successful
    assert result.converged is True
    assert result.properties["total_energy"] == -100.5


def test_partial_result():
    """An unconverged calculation may retain useful properties."""
    result = CalculationResult(
        status="partial",
        converged=False,
        properties={"total_energy": -100.0},
        warnings=["Optimization did not converge."],
    )

    assert not result.successful
    assert result.properties["total_energy"] == -100.0


def test_result_serialization():
    """Serialization and reconstruction preserve result contents."""
    result = CalculationResult(
        status="completed",
        converged=True,
        properties={"energy": -42.0},
        units={"energy": "eV"},
        metadata={"scf_iterations": 15},
    )

    restored = CalculationResult.from_dict(result.to_dict())

    assert restored == result


def test_invalid_status():
    """Unknown scientific outcome states are rejected."""
    with pytest.raises(ValueError):
        CalculationResult(status="running")


def test_invalid_units():
    """Units cannot reference nonexistent scientific properties."""
    with pytest.raises(ValueError):
        CalculationResult(
            status="completed",
            units={"energy": "eV"},
        )


def test_result_immutability():
    """Scientific properties cannot be modified after construction."""
    result = CalculationResult(
        status="completed",
        properties={"energy": -100.0},
    )

    with pytest.raises(TypeError):
        result.properties["energy"] = -200.0