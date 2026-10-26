# JHaRoo documentation

**JHaRoo (`jhr`)** provides reusable scientific calculation interfaces for simulation codes, with optional workflow orchestration through AiiDA.

The scientific API is independent of any scheduler or provenance engine. A calculation is specified with `CalculationSpec`, a code adapter prepares the native input, and `CalculationResult` holds structured scientific properties and validation diagnostics.

## Start here

- [AiiDA overview](user-guide/aiida/index.md): what each component does and the present scope.
- [Local setup](user-guide/aiida/local-setup.md): PostgreSQL, ZeroMQ, computers, and codes.
- [Submitting ORCA jobs](user-guide/aiida/orca.md): specification, structure, builder, and dry run.
- [Developer architecture](developer-guide/aiida/architecture.md): contracts and design decisions.
- [ORCA CalcJob](developer-guide/aiida/orca-calcjob.md): implementation and extension points.

The AiiDA integration is under development. The initial target is a conventional, single-step ORCA `CalcJob`; Compound parsing and validation exist in `jhr`, but Compound submission and an AiiDA output parser are separate milestones.
