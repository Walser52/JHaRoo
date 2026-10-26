"""
Tests for scientific validation of ORCA Compound calculations.

The tests verify that scientific completion is evaluated separately
for each Compound step and independently of overall termination.
"""

from jhr.core.calculation import CalculationSpec
from jhr.codes.orca.parser import ORCAParser
from jhr.codes.orca.compound_validator import ORCACompoundValidator


def make_specs():
    """Construct specifications for optimization followed by TDDFT."""
    optimization = CalculationSpec(
        name="S0_opt",
        code="orca",
        task="optimization",
        parameters={
            "method": "PBE0",
            "basis": "def2-TZVP",
        },
    )

    tddft = CalculationSpec(
        name="TDDFT_vertical",
        code="orca",
        task="excited_states",
        parameters={
            "method": "PBE0",
            "basis": "def2-TZVP",
        },
        code_options={
            "nroots": 2,
        },
    )

    return [optimization, tddft]


def test_successful_compound():
    """Both scientifically complete steps are validated independently."""
    text = """
    COMPOUND JOB 1

    FINAL SINGLE POINT ENERGY -101.0
    THE OPTIMIZATION HAS CONVERGED
    OPTIMIZATION RUN DONE

    COMPOUND JOB 2

    FINAL SINGLE POINT ENERGY -100.5

    TD-DFT/TDA EXCITED STATES (SINGLETS)

    STATE 1: E= 0.100000 au  2.721 eV  Mult 1
    STATE 2: E= 0.120000 au  3.265 eV  Mult 1

    ORCA TERMINATED NORMALLY
    """

    parsed = ORCAParser.parse_compound(text)

    validated = ORCACompoundValidator.validate(
        specs=make_specs(),
        compound=parsed,
        text=text,
    )

    assert validated.terminated_normally
    assert validated.step(1).successful
    assert validated.step(1).converged is True

    assert validated.step(2).successful
    assert validated.step(2).converged is None


def test_partial_optimization():
    """An unconverged optimization is not promoted to completed."""
    text = """
    COMPOUND JOB 1

    FINAL SINGLE POINT ENERGY -101.0

    COMPOUND JOB 2

    FINAL SINGLE POINT ENERGY -100.5

    TD-DFT/TDA EXCITED STATES (SINGLETS)

    STATE 1: E= 0.100000 au  2.721 eV  Mult 1
    STATE 2: E= 0.120000 au  3.265 eV  Mult 1

    ORCA TERMINATED NORMALLY
    """

    parsed = ORCAParser.parse_compound(text)

    validated = ORCACompoundValidator.validate(
        specs=make_specs(),
        compound=parsed,
        text=text,
    )

    assert validated.step(1).status == "partial"
    assert validated.step(1).converged is False

    assert validated.step(2).successful


def test_interrupted_final_step():
    """An interrupted final step cannot be marked completed."""
    text = """
    COMPOUND JOB 1

    FINAL SINGLE POINT ENERGY -101.0
    THE OPTIMIZATION HAS CONVERGED

    COMPOUND JOB 2

    FINAL SINGLE POINT ENERGY -100.5

    TD-DFT/TDA EXCITED STATES (SINGLETS)

    STATE 1: E= 0.100000 au  2.721 eV  Mult 1
    STATE 2: E= 0.120000 au  3.265 eV  Mult 1
    """

    parsed = ORCAParser.parse_compound(text)

    validated = ORCACompoundValidator.validate(
        specs=make_specs(),
        compound=parsed,
        text=text,
    )

    assert validated.step(1).successful
    assert validated.step(2).status == "partial"
    assert not validated.terminated_normally