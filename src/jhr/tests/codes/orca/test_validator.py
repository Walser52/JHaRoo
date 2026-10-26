"""
Tests for ORCA scientific output validation.

These tests use short representative output fragments.
They do not require an ORCA installation.
"""

import pytest

from jhr.codes.orca.validator import ORCAValidator


ENERGY = "FINAL SINGLE POINT ENERGY    -100.123456789"
TERMINATION = "ORCA TERMINATED NORMALLY"
OPTIMIZED = "THE OPTIMIZATION HAS CONVERGED"


def test_successful_single_point():
    """A normally terminated calculation with energy passes."""
    text = f"{ENERGY}\n{TERMINATION}"

    report = ORCAValidator.inspect(
        text,
        task="single_point",
    )

    assert report.successful
    assert report.energy_found
    assert report.terminated_normally


def test_missing_termination():
    """An interrupted run with an energy is classified as partial."""
    report = ORCAValidator.inspect(
        ENERGY,
        task="single_point",
    )

    assert report.status == "partial"
    assert not report.terminated_normally


def test_successful_optimization():
    """Geometry convergence is validated separately."""
    text = f"{ENERGY}\n{OPTIMIZED}\n{TERMINATION}"

    report = ORCAValidator.inspect(
        text,
        task="optimization",
    )

    assert report.successful
    assert report.optimization_converged is True


def test_unconverged_optimization():
    """Normal termination alone does not establish convergence."""
    text = f"{ENERGY}\n{TERMINATION}"

    report = ORCAValidator.inspect(
        text,
        task="optimization",
    )

    assert report.status == "partial"
    assert report.optimization_converged is False


def test_tddft_roots():
    """Singlet roots are counted within the correct TDDFT section."""
    text = f"""
    {ENERGY}

    TD-DFT/TDA EXCITED STATES (SINGLETS)

    STATE 1: E= 0.10 au
    STATE 2: E= 0.20 au
    STATE 3: E= 0.30 au

    {TERMINATION}
    """

    report = ORCAValidator.inspect(
        text,
        task="excited_states",
        expected_roots=3,
    )

    assert report.successful
    assert report.singlet_roots == 3


def test_tddft_does_not_mix_spin_roots():
    """Triplet roots cannot satisfy a singlet root requirement."""
    text = f"""
    {ENERGY}

    TD-DFT/TDA EXCITED STATES (SINGLETS)

    STATE 1: E= 0.10 au
    STATE 2: E= 0.20 au

    TD-DFT/TDA EXCITED STATES (TRIPLETS)

    STATE 1: E= 0.08 au
    STATE 2: E= 0.16 au
    STATE 3: E= 0.25 au

    {TERMINATION}
    """

    report = ORCAValidator.inspect(
        text,
        task="excited_states",
        expected_roots=3,
    )

    assert report.status == "partial"
    assert report.singlet_roots == 2
    assert report.triplet_roots == 3


def test_empty_output():
    """Empty output is classified as failed."""
    report = ORCAValidator.inspect(
        "",
        task="single_point",
    )

    assert report.status == "failed"
    assert not report.successful


def test_invalid_task():
    """Unsupported validation tasks are rejected."""
    with pytest.raises(ValueError):
        ORCAValidator.inspect(
            "some output",
            task="unsupported",
        )


def test_file_validation(tmp_path):
    """The legacy file-based API remains operational."""
    output = tmp_path / "calc.out"

    output.write_text(
        f"{ENERGY}\n{OPTIMIZED}\n{TERMINATION}"
    )

    assert ORCAValidator.validate_optimization(output)


def test_file_validation_failure(tmp_path):
    """Legacy validation raises when the calculation is incomplete."""
    output = tmp_path / "calc.out"
    output.write_text(ENERGY)

    with pytest.raises(RuntimeError):
        ORCAValidator.validate_termination(output)