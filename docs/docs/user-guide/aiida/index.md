# AiiDA integration

JHaRoo separates scientific intent from execution. **You describe the calculation; AiiDA records it and manages its execution.**

| Layer | Responsibility |
| --- | --- |
| `CalculationSpec` | Scientific task, method, basis, charge, multiplicity, and code options |
| `OrcaAdapter` | Translate a specification and ASE structure into ORCA input text |
| `ORCAParser` and validators | Extract results and assess scientific completion |
| AiiDA `CalcJob` | Stage files, invoke the code, retrieve outputs, record provenance |
| AiiDA `WorkChain` (planned) | Dependencies, recovery strategies, and high-throughput orchestration |
| Slurm or direct scheduler | Resource allocation and job launching |

## Storage and services

AiiDA's `core.psql_dos` storage combines PostgreSQL with a filesystem-backed object repository. They must both be preserved when backing up a profile. The ZeroMQ broker is built into AiiDA 2.9+ and is started with the daemon; it does not require a separate server.

The database location and the file-repository URI are different settings. The repository is managed by AiiDA: do not modify its files manually.

## Current scope

- Conventional ORCA single-point, optimization, and vertical TDDFT input generation.
- Task-specific output validation and basic energy parsing in the scientific layer.
- Compound output splitting and step-aware result representation in the scientific layer.
- Initial AiiDA `jhr.orca` `CalcJob` for one conventional calculation, subject to local verification.

**Not yet implemented:** a registered AiiDA parser for scientific outputs, Compound submission via AiiDA, automated retries, and high-throughput `WorkChain`s. Until an AiiDA parser is connected, expect retrieved files but no parsed scientific output nodes.

Continue with [local setup](local-setup.md) and [ORCA submission](orca.md).
