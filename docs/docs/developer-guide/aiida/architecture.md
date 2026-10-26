# Architecture and contracts

The key design constraint is **scientific code must not depend on AiiDA**. The dependency direction is from `jhr.integrations.aiida` toward `jhr.core` and `jhr.codes`, never the reverse.

## Core abstractions

| Abstraction | Contract | Must not do |
| --- | --- | --- |
| `CalculationSpec` | Immutable scientific intent; JSON-compatible round trip | Choose paths or launch commands |
| `CalculationResult` | Immutable, structured properties, units, convergence and diagnostics | Own raw job directories |
| `PreparedCalculation` | Relative input filenames mapped to text contents | Write files or schedule jobs |
| `CodeAdapter` | Validate specifications, prepare inputs, parse and validate results | Submit AiiDA processes |
| `ORCAParser` | Extract numeric quantities from output text | Claim scientific convergence |
| `ORCAValidator` | Evaluate task-specific scientific completion | Parse every scientific property |
| `CompoundResult` | Preserve one result per logical Compound step | Confuse overall termination with per-step convergence |

The in-memory APIs simplify unit tests: no ORCA installation, scheduler, database, or daemon is needed to test input rendering, parsing, and validation.

## Immutability and serialization

`CalculationSpec` and `CalculationResult` freeze nested dictionaries and lists into read-only mappings and tuples. `to_dict()` creates independent JSON-compatible dictionaries and lists. The AiiDA integration can wrap these in `aiida.orm.Dict`; it should not store Python `MappingProxyType` objects directly.

## Scientific versus execution status

An ORCA process may terminate normally without converging geometrically. The numerical result can also be partial but still scientifically useful. Keep the following distinct:

- AiiDA process state and scheduler exit status;
- ORCA overall termination marker;
- task-specific convergence and completion;
- data availability and parser errors.

For Compound calculations, validate each numbered step against its corresponding `CalculationSpec`; preserve the overall Compound termination independently. The final step needs an overall completion safeguard because it has no subsequent step marker.

## Resource ownership

`CalculationSpec` describes physical and numerical intent. `CalcJob` owns executable arguments, `%pal`, `%maxcore`, scheduler resource settings, working directories, and retrieval lists. Avoid duplicate resource directives from native code-options blocks.

## Planned extensions

1. Verify the conventional `OrcaCalculation` with a local AiiDA dry run and one H₂ calculation.
2. Implement an AiiDA parser emitting `Dict` and, where appropriate, structure/array nodes.
3. Define a Compound execution input (ordered specifications) and step-aware AiiDA outputs.
4. Add `WorkChain` dependency management, failure classification, retry policies, and concurrency controls.
5. Extend code adapters to additional simulation programs without coupling their scientific APIs to AiiDA.
