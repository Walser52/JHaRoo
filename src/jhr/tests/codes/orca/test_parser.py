"""
Tests for ORCA numerical output parsing and adapter integration.

The tests use representative output fragments and do not require
an ORCA executable.
"""

import pytest

from jhr.core.calculation import CalculationSpec
from jhr.codes.orca.adapter import OrcaAdapter
from jhr.codes.orca.parser import ORCAParser


def test_parse_energy():
    """The parser extracts the final electronic energy."""
    text = """
    FINAL SINGLE POINT ENERGY    -100.123456789
    ORCA TERMINATED NORMALLY
    """

    result = ORCAParser.parse(text)

    assert result.properties["total_energy"] == pytest.approx(
        -100.123456789
    )
    assert result.units["total_energy"] == "Hartree"
    assert result.status == "partial"


def test_parse_last_energy():
    """The final energy record is selected."""
    text = """
    FINAL SINGLE POINT ENERGY    -100.0
    FINAL SINGLE POINT ENERGY    -101.0
    FINAL SINGLE POINT ENERGY    -102.0
    """

    result = ORCAParser.parse(text)

    assert result.properties["total_energy"] == -102.0
    assert result.metadata["energy_records"] == 3


def test_missing_energy():
    """Missing energy produces a failed preliminary result."""
    result = ORCAParser.parse(
        "ORCA calculation started but produced no energy"
    )

    assert result.status == "failed"
    assert "total_energy" not in result.properties


def test_adapter_successful_single_point():
    """The adapter combines parsing and scientific validation."""
    spec = CalculationSpec(
        name="SP",
        code="orca",
        task="single_point",
        parameters={
            "method": "PBE0",
            "basis": "def2-TZVP",
        },
    )

    outputs = {
        "calc.out": """
        FINAL SINGLE POINT ENERGY    -100.5
        ORCA TERMINATED NORMALLY
        """,
    }

    adapter = OrcaAdapter()

    parsed = adapter.parse(outputs)
    result = adapter.validate_result(spec, parsed, outputs)

    assert result.successful
    assert result.properties["total_energy"] == -100.5
    assert result.converged is None


def test_adapter_unconverged_optimization():
    """Normal termination does not imply geometry convergence."""
    spec = CalculationSpec(
        name="S0_opt",
        code="orca",
        task="optimization",
        parameters={
            "method": "PBE0",
            "basis": "def2-TZVP",
        },
    )

    outputs = {
        "calc.out": """
        FINAL SINGLE POINT ENERGY    -100.5
        ORCA TERMINATED NORMALLY
        """,
    }

    adapter = OrcaAdapter()

    parsed = adapter.parse(outputs)
    result = adapter.validate_result(spec, parsed, outputs)

    assert result.status == "partial"
    assert result.converged is False
    assert result.properties["total_energy"] == -100.5


def test_adapter_missing_output():
    """A missing required output file raises a clear error."""
    adapter = OrcaAdapter()

    with pytest.raises(ValueError):
        adapter.parse({})

def test_compound_step_parsing():
    """Compound calculations retain independent scientific results."""
    text = """
    COMPOUND JOB  1

    FINAL SINGLE POINT ENERGY -100.0
    THE OPTIMIZATION HAS CONVERGED
    FINAL SINGLE POINT ENERGY -101.0

    COMPOUND JOB  2

    FINAL SINGLE POINT ENERGY -100.5

    TD-DFT/TDA EXCITED STATES (SINGLETS)

    STATE 1: E= 0.100000 au  2.721 eV  Mult 1
    STATE 2: E= 0.120000 au  3.265 eV  Mult 1

    TD-DFT/TDA EXCITED STATES (TRIPLETS)

    STATE 3: E= 0.080000 au  2.177 eV  Mult 3

    ORCA TERMINATED NORMALLY
    """

    compound = ORCAParser.parse_compound(text)

    assert len(compound.steps) == 2
    assert compound.terminated_normally

    optimization = compound.step(1)
    tddft = compound.step(2)

    assert optimization.properties["total_energy"] == -101.0
    assert tddft.properties["total_energy"] == -100.5

    assert tddft.properties["excitation_energies_singlets"] == (
        2.721,
        3.265,
    )

    assert tddft.properties["excitation_energies_triplets"] == (
        2.177,
    )


def test_compound_missing_steps():
    """Non-Compound outputs are rejected by the Compound parser."""
    with pytest.raises(ValueError):
        ORCAParser.parse_compound(
            "FINAL SINGLE POINT ENERGY -100.0"
        )


def test_compound_step_lookup():
    """Requesting an unknown step raises KeyError."""
    text = """
    COMPOUND JOB 1
    FINAL SINGLE POINT ENERGY -100.0
    ORCA TERMINATED NORMALLY
    """

    compound = ORCAParser.parse_compound(text)

    with pytest.raises(KeyError):
        compound.step(3)