# Developing the ORCA CalcJob

Module: `jhr.integrations.aiida.calculations.orca`

Entry point:

```toml
[project.entry-points."aiida.calculations"]
"jhr.orca" = "jhr.integrations.aiida.calculations.orca:OrcaCalculation"
```

## Process interface

`OrcaCalculation.define()` declares `structure: StructureData`, `calculation: Dict` (a serialized `CalculationSpec`), and `maxcore_mb: Int`. The inherited `code` port identifies the ORCA executable; scheduler resources are provided through `metadata.options`.

## Submission lifecycle

1. Reconstruct `CalculationSpec` with `CalculationSpec.from_dict()`.
2. Convert `StructureData` to ASE `Atoms` using `get_ase()`.
3. Call `OrcaAdapter.prepare(spec, atoms)` to generate an in-memory `PreparedCalculation`.
4. Add `%pal` and `%maxcore` based on AiiDA execution resources.
5. Write input files to AiiDA's temporary sandbox; return `CalcInfo` with one `CodeInfo`.
6. Set `CodeInfo.withmpi=False` and use `cmdline_params=['calc.inp']`.
7. Retrieve `calc.out` and `calc.err` for the initial implementation.

Only step 4 should know about scheduler allocations. AiiDA's engine handles the submission script and remote file staging.

## Development checks

```bash
python -m pytest tests/core/ tests/codes/orca/ -v
python -m pip install -e .
verdi plugin list aiida.calculations jhr.orca
```

After modifying an installed plugin, restart the AiiDA daemon if it was already running, so its workers load the updated code.

## Testing strategy

| Test layer | Requires ORCA? | Requires AiiDA storage? |
| --- | --- | --- |
| `CalculationSpec`, `CalculationResult`, adapter tests | No | No |
| `ORCAParser` and `ORCAValidator` fixtures | No | No |
| CalcJob submission preparation/dry run | No execution | Usually yes for an integrated dry run |
| Local ORCA integration test | Yes | Yes |
| Slurm integration test | Yes | Yes |

Use real ORCA output fixtures in parser regression tests. A Compound output must not be parsed as one conventional calculation: its last `FINAL SINGLE POINT ENERGY` belongs to the last Compound step, not necessarily the optimization step.

## Known limitations

- `OrcaCalculation` presently represents a single conventional ORCA input.
- There is no AiiDA parser entry point producing scientific output nodes yet.
- Large output artifacts (`.gbw`, trajectories, wavefunctions) need explicit, selective retrieval policies.
- AiiDA job exit codes and scientific validation outcomes need a clearly defined mapping when the parser is added.
- Test memory and MPI behavior under the actual Slurm configuration before high-throughput scaling.
