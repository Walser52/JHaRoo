# Submitting an ORCA calculation

This guide describes the intended first AiiDA integration: one conventional ORCA calculation. It assumes that an AiiDA Computer and an installed ORCA Code have already been configured.

## 1. Describe the science

```python
from ase import Atoms
from jhr.core.calculation import CalculationSpec

atoms = Atoms("H2", positions=[(0, 0, 0), (0, 0, 0.74)])

spec = CalculationSpec(
    name="H2_sp",
    code="orca",
    task="single_point",
    parameters={
        "method": "PBE0",
        "basis": "def2-SVP",
        "charge": 0,
        "multiplicity": 1,
    },
    code_options={"scf": "TightSCF"},
)
```

`CalculationSpec` contains no file path, ORCA executable path, Slurm directive, or AiiDA node. It can also be used outside AiiDA.

## 2. Build and dry-run the AiiDA job

After registering the `jhr.orca` entry point and an AiiDA ORCA Code:

```python
from aiida import load_profile
from aiida.orm import Dict, Int, StructureData, load_code

load_profile("tadf")

code = load_code("orca@localhost")  # Replace with your registered full label
builder = code.get_builder()
builder.structure = StructureData(ase=atoms)
builder.calculation = Dict(dict=spec.to_dict())
builder.maxcore_mb = Int(1000)
builder.metadata.options.resources = {
    "num_machines": 1,
    "num_mpiprocs_per_machine": 1,
}
builder.metadata.options.max_wallclock_seconds = 1800
builder.metadata.dry_run = True
```

Save the snippet in a script and run it with `verdi run your_script.py` (or use a Python process with the profile loaded). The dry run prepares submission files but does not execute ORCA. Inspect the resulting sandbox input and scheduler script before actual submission.

## 3. Submit only after inspection

Remove the dry-run setting, then submit:

```python
from aiida.engine import submit

builder.metadata.dry_run = False
node = submit(builder)
print(node.pk)
```

Monitor the node and daemon:

```bash
verdi process list
verdi process show PK
verdi daemon status
```

Replace `PK` with the printed process identifier. The initial plugin retrieves `calc.out` and `calc.err`. A registered AiiDA parser producing scientific output nodes is a later milestone.

## ORCA resources

- AiiDA launches the ORCA executable **once**, without an outer `mpirun`.
- The CalcJob writes `%pal nprocs N` from the scheduler resources.
- `%maxcore` is **per ORCA process**, not the total job-memory allocation. Allow headroom beyond `N × maxcore_mb`.
- The first implementation supports one machine per calculation.

## Current limitations

The initial AiiDA `CalcJob` supports conventional single-step inputs. ORCA Compound execution requires its own input and retrieval handling. The scientific Compound parser and validator do not, by themselves, make the AiiDA plugin Compound-aware.
