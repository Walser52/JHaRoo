"""
AiiDA CalcJob implementation for conventional ORCA calculations.

This module connects the scientific calculation abstractions provided
by jhr with AiiDA's execution and provenance infrastructure.

The OrcaCalculation process accepts a molecular structure and a
serialized CalculationSpec, generates ORCA input through OrcaAdapter,
and instructs AiiDA how to execute the calculation.

Responsibilities
----------------
OrcaAdapter
    Translate scientific intent into ORCA input.

OrcaCalculation
    Stage input files, configure execution resources, and specify
    which output files AiiDA should retrieve.

AiiDA engine
    Manage process state, provenance, scheduling, execution,
    file transfer, and retrieval.

Notes
-----
This initial implementation supports conventional, single-step
ORCA calculations on one compute node.

Compound calculations and scientific output parsing will be added
in subsequent development stages.

The module does not depend on the aiida-orca plugin.
"""

from __future__ import annotations

from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.engine import CalcJob
from aiida.orm import Dict, Int, StructureData

from jhr.core.calculation import CalculationSpec
from jhr.codes.orca.adapter import OrcaAdapter


class OrcaCalculation(CalcJob):
    """
    Execute a conventional ORCA calculation through AiiDA.

    The process receives a scientific calculation specification,
    an atomistic structure, and execution resources.

    ORCA input generation is delegated to the code-independent
    jhr calculation framework and its ORCA adapter.

    Inputs
    ------
    code : aiida.orm.AbstractCode
        Registered ORCA executable associated with an AiiDA computer.

    structure : aiida.orm.StructureData
        Molecular geometry used to initialize the calculation.

    calculation : aiida.orm.Dict
        Serialized CalculationSpec.

        The dictionary must be compatible with
        ``CalculationSpec.from_dict``.

    maxcore_mb : aiida.orm.Int
        Maximum memory in megabytes per ORCA process.

        This value is translated into ORCA's ``%maxcore`` directive.

    metadata.options.resources : dict
        Scheduler resource configuration.

        This initial implementation requires one compute node and
        uses ``num_mpiprocs_per_machine`` as ORCA's parallel process
        count.

    metadata.options.max_wallclock_seconds : int
        Maximum wall-clock duration.

    Outputs
    -------
    retrieved : aiida.orm.FolderData
        Files retrieved from the ORCA working directory.

        Initially, the primary output and standard-error files
        are retrieved.

    Notes
    -----
    OrcaCalculation does not directly execute ORCA.

    Instead, it produces an AiiDA CalcInfo object describing
    the required execution.

    AiiDA then manages the scheduler submission and process lifecycle.

    ORCA launches its own parallel processes according to the
    ``%pal`` directive. Therefore, the executable is not wrapped
    in an additional MPI launcher.

    The scientific specification remains independent of the
    requested computational resources.

    Examples
    --------
    A process builder can be obtained from a configured AiiDA code:

    >>> # builder = code.get_builder()
    >>> # builder.structure = StructureData(ase=atoms)
    >>> # builder.calculation = Dict(dict=spec.to_dict())
    >>> # builder.maxcore_mb = Int(4000)
    """

    INPUT_FILENAME = "calc.inp"
    OUTPUT_FILENAME = "calc.out"
    ERROR_FILENAME = "calc.err"

    @classmethod
    def define(cls, spec):
        """
        Define the AiiDA process interface.

        Parameters
        ----------
        spec : aiida.engine.ProcessSpec
            Process specification configured by AiiDA.

        Notes
        -----
        The base CalcJob class provides common process inputs,
        including the executable code and scheduler metadata.

        Additional inputs define the scientific calculation and
        ORCA-specific memory requirement.
        """
        super().define(spec)

        spec.input(
            "structure",
            valid_type=StructureData,
            help=(
                "Atomic structure used to initialize "
                "the ORCA calculation."
            ),
        )

        spec.input(
            "calculation",
            valid_type=Dict,
            help=(
                "Serialized jhr CalculationSpec describing "
                "the requested scientific operation."
            ),
        )

        spec.input(
            "maxcore_mb",
            valid_type=Int,
            default=lambda: Int(4000),
            help=(
                "Maximum memory in MB per ORCA process."
            ),
        )

        spec.inputs["metadata"]["options"]["resources"].required = True

    def prepare_for_submission(self, folder):
        """
        Prepare an ORCA calculation for submission through AiiDA.

        Parameters
        ----------
        folder : aiida.common.folders.Folder
            Temporary AiiDA sandbox folder.

            Generated input files are written into this folder
            before AiiDA stages them on the target computer.

        Returns
        -------
        aiida.common.datastructures.CalcInfo
            Execution instructions containing the configured code,
            command-line arguments, and file retrieval requirements.

        Raises
        ------
        ValueError
            If the scientific specification is unsupported, the
            resource configuration is invalid, or memory settings
            are inconsistent.

        Notes
        -----
        Input generation is delegated to OrcaAdapter.

        The generated ORCA input contains scientific settings
        supplied by CalculationSpec.

        Parallel process count and memory settings are inserted
        separately using the AiiDA execution configuration.

        The implementation currently supports one compute node.

        The executable is launched directly without an external
        MPI wrapper. ORCA's internal parallel launcher is
        configured through the ``%pal`` directive.

        The retrieved files are:

        - calc.out: ORCA standard output.
        - calc.err: Standard error.

        Additional scientific files may be retrieved by later
        versions of this plugin.
        """
        # ----------------------------------------------------
        # 1. Reconstruct the scientific calculation
        # ----------------------------------------------------

        calculation_spec = CalculationSpec.from_dict(
            self.inputs.calculation.get_dict()
        )

        atoms = self.inputs.structure.get_ase()

        # ----------------------------------------------------
        # 2. Generate code-specific scientific input
        # ----------------------------------------------------

        adapter = OrcaAdapter()

        prepared = adapter.prepare(
            calculation_spec,
            atoms,
        )

        # ----------------------------------------------------
        # 3. Read AiiDA execution resources
        # ----------------------------------------------------

        resources = self.options.resources

        num_machines = resources.get("num_machines", 1)

        nprocs = resources.get(
            "num_mpiprocs_per_machine",
            1,
        )

        if num_machines != 1:
            raise ValueError(
                "The initial OrcaCalculation implementation "
                "supports only one compute node."
            )

        if type(nprocs) is not int or nprocs < 1:
            raise ValueError(
                "num_mpiprocs_per_machine must be "
                "a positive integer."
            )

        maxcore = self.inputs.maxcore_mb.value

        if maxcore < 1:
            raise ValueError(
                "maxcore_mb must be positive."
            )

        # ----------------------------------------------------
        # 4. Add ORCA execution resource settings
        # ----------------------------------------------------

        resource_block = (
            f"%pal nprocs {nprocs} end\n"
            f"%maxcore {maxcore}\n\n"
        )

        for filename, content in prepared.files.items():

            if filename == prepared.input_filename:
                content = resource_block + content

            with folder.open(
                filename,
                "w",
                encoding="utf-8",
            ) as handle:
                handle.write(content)

        # ----------------------------------------------------
        # 5. Configure the executable
        # ----------------------------------------------------

        codeinfo = CodeInfo()

        codeinfo.code_uuid = self.inputs.code.uuid

        codeinfo.cmdline_params = [
            prepared.input_filename,
        ]

        codeinfo.stdout_name = self.OUTPUT_FILENAME
        codeinfo.stderr_name = self.ERROR_FILENAME

        # ORCA manages its own parallel execution through %pal.
        codeinfo.withmpi = False

        # ----------------------------------------------------
        # 6. Configure AiiDA submission and retrieval
        # ----------------------------------------------------

        calcinfo = CalcInfo()

        calcinfo.codes_info = [codeinfo]

        calcinfo.retrieve_list = [
            self.OUTPUT_FILENAME,
            self.ERROR_FILENAME,
        ]

        return calcinfo