"""
Tests for scientific code adapter abstractions.

These tests verify the shared adapter contract independently
of any particular scientific simulation program.
"""

import pytest

from jhr.core.adapter import (
    CodeAdapter,
    PreparedCalculation,
)

from jhr.core.calculation import (
    CalculationSpec,
    CalculationResult,
)


class DummyAdapter(CodeAdapter):
    """
    Minimal adapter for testing the abstract interface.

    This adapter does not interface with a real simulation program.
    It implements the required methods using predefined values.
    """

    code = "dummy"

    def validate_spec(self, spec):
        """Check that the specification targets the dummy code."""
        if spec.code != self.code:
            raise ValueError("Unsupported scientific code.")

    def prepare(self, spec, system):
        """Generate a minimal dummy input."""
        self.validate_spec(spec)

        return PreparedCalculation(
            files={"calculation.in": "dummy input"},
            input_filename="calculation.in",
        )

    def parse(self, outputs):
        """Produce a predefined scientific result."""
        return CalculationResult(
            status="completed",
            converged=True,
            properties={"energy": -1.0},
            units={"energy": "eV"},
        )

    def validate_result(self, spec, result):
        """Return a scientifically validated result."""
        self.validate_spec(spec)
        return result


@pytest.fixture
def dummy_spec():
    """Return a valid dummy calculation specification."""
    return CalculationSpec(
        name="test",
        code="dummy",
        task="single_point",
    )


def test_abstract_adapter():
    """The abstract base class cannot be instantiated."""
    with pytest.raises(TypeError):
        CodeAdapter()


def test_adapter_validation(dummy_spec):
    """A concrete adapter accepts its supported code."""
    adapter = DummyAdapter()
    adapter.validate_spec(dummy_spec)


def test_adapter_rejects_wrong_code():
    """An adapter rejects specifications for another code."""
    adapter = DummyAdapter()

    spec = CalculationSpec(
        name="test",
        code="orca",
        task="single_point",
    )

    with pytest.raises(ValueError):
        adapter.validate_spec(spec)


def test_adapter_preparation(dummy_spec):
    """Preparation produces an execution-independent input bundle."""
    adapter = DummyAdapter()

    prepared = adapter.prepare(dummy_spec, system=None)

    assert prepared.input_filename == "calculation.in"
    assert "calculation.in" in prepared.files


def test_adapter_parsing():
    """Parsing produces a structured CalculationResult."""
    adapter = DummyAdapter()

    result = adapter.parse({"calculation.out": "dummy output"})

    assert isinstance(result, CalculationResult)
    assert result.successful
    assert result.properties["energy"] == -1.0


def test_prepared_files_are_immutable():
    """Prepared input files cannot be modified after construction."""
    prepared = PreparedCalculation(
        files={"test.in": "original content"},
        input_filename="test.in",
    )

    with pytest.raises(TypeError):
        prepared.files["test.in"] = "modified content"


def test_prepared_input_must_exist():
    """The primary input must belong to the prepared file collection."""
    with pytest.raises(ValueError):
        PreparedCalculation(
            files={"other.in": "content"},
            input_filename="missing.in",
        )


@pytest.mark.parametrize(
    "filename",
    [
        "/tmp/calculation.in",
        "../calculation.in",
        "inputs/../../calculation.in",
        "inputs//calculation.in",
        "./calculation.in",
    ],
)
def test_invalid_input_paths(filename):
    """Unsafe or malformed relative paths are rejected."""
    with pytest.raises(ValueError):
        PreparedCalculation(
            files={filename: "content"},
            input_filename=filename,
        )