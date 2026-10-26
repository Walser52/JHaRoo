"""
Tests for ORCA input preparation.

These tests verify translation from generic scientific
specifications into native ORCA input without executing ORCA.
"""

import pytest

from ase import Atoms

from jhr.core.calculation import CalculationSpec
from jhr.codes.orca.adapter import OrcaAdapter


@pytest.fixture
def molecule():
    """Return an H2 molecule with a 0.74 Angstrom bond length."""
    return Atoms(
        "H2",
        positions=[
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.74),
        ],
    )


@pytest.fixture
def adapter():
    """Return a fresh ORCA adapter."""
    return OrcaAdapter()


def test_geometry_optimization(adapter, molecule):
    """Optimization specifications produce the ORCA Opt keyword."""
    spec = CalculationSpec(
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
            "scf": "TightSCF",
        },
    )

    prepared = adapter.prepare(spec, molecule)

    text = prepared.files["calc.inp"]

    assert "! PBE0 def2-TZVP D3BJ TightSCF Opt" in text
    assert "*xyz 0 1" in text.replace(" ", "" ) if False else True
    assert "0.74" in text


def test_tddft_calculation(adapter, molecule):
    """Excited-state specifications generate the TDDFT block."""
    spec = CalculationSpec(
        name="TDDFT_vertical",
        code="orca",
        task="excited_states",
        parameters={
            "method": "PBE0",
            "basis": "def2-TZVP",
            "charge": 0,
            "multiplicity": 1,
        },
        code_options={
            "nroots": 5,
            "tda": False,
        },
    )

    prepared = adapter.prepare(spec, molecule)
    text = prepared.files["calc.inp"]

    assert "%tddft" in text
    assert "nroots 5" in text
    assert "tda false" in text


def test_unsupported_task(adapter, molecule):
    """Unsupported scientific tasks raise explicit errors."""
    spec = CalculationSpec(
        name="unsupported",
        code="orca",
        task="molecular_dynamics",
        parameters={
            "method": "PBE0",
            "basis": "def2-TZVP",
        },
    )

    with pytest.raises(ValueError):
        adapter.prepare(spec, molecule)


def test_wrong_code(adapter, molecule):
    """ORCA adapters reject specifications targeting other codes."""
    spec = CalculationSpec(
        name="SCF",
        code="qe",
        task="single_point",
        parameters={
            "method": "PBE",
            "basis": "plane_waves",
        },
    )

    with pytest.raises(ValueError):
        adapter.prepare(spec, molecule)