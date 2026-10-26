# Local AiiDA setup

This guide assumes Linux, AiiDA 2.9+, an installed `jhr` package, and a locally installed ORCA executable. It uses PostgreSQL storage and the built-in ZeroMQ broker.

## 1. Check the active profile

Activate the Python environment containing `aiida-core` and `jhr`, then inspect the profile:

```bash
conda activate tadf_aiida
verdi profile list
verdi status
```

The current development profile is named `tadf` and uses PostgreSQL (`aiida_db`) with its object repository under `/mnt/data/databases/aiida/tadf/repository`. These are **example values from one workstation**, not portable defaults. Do not create a second profile if the existing one works.

Start the daemon only after confirming a broker is configured:

```bash
verdi daemon start
verdi status
```

The ZeroMQ broker is managed with the daemon. No RabbitMQ installation is needed for this configuration.

## 2. Check registered computers and codes

```bash
verdi computer list
verdi code list
```

An empty list is normal immediately after creating a profile. Before submitting ORCA calculations, configure:

1. An AiiDA **Computer** representing the machine on which ORCA executes, with the appropriate transport and scheduler (`core.local`/`core.direct` for a simple local test, or a Slurm scheduler for cluster jobs).
2. An AiiDA installed **Code** pointing to the ORCA executable on that computer and associated with the `jhr.orca` calculation plugin.

Use `verdi computer setup --help` and `verdi code create --help` for the exact commands supported by your installed AiiDA version. Do not guess the ORCA executable path; confirm it with `command -v orca` after loading the same modules or environment that the job will use.

For Slurm, ensure that the AiiDA computer has a valid work directory and that the selected transport user can submit jobs. The AiiDA daemon must be running on a persistent host, rather than inside an ephemeral batch job.

## 3. Confirm plugin discovery

From the `jhr` repository, install the package in editable mode:

```bash
python -m pip install -e .
verdi plugin list aiida.calculations
verdi plugin list aiida.calculations jhr.orca
```

The `pyproject.toml` entry point must register `jhr.orca`. If the plugin is missing, verify the entry-point configuration, reinstall, and restart the daemon after updating plugin code.

## 4. Operational checks

```bash
verdi status
verdi daemon status
verdi computer test COMPUTER_LABEL
```

Replace `COMPUTER_LABEL` with the configured AiiDA computer label. AiiDA has not been fully configured for execution until a computer and a code have been registered and tested.

## Data protection

Back up **both** the PostgreSQL database and AiiDA file repository. Avoid embedding database passwords, SSH secrets, or other credentials in committed documentation or job scripts. AiiDA's profile configuration contains connection details and should remain private.
