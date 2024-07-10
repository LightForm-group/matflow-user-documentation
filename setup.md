# Setup
## Learning objectives
Be able to:
- Install matflow
- Configure environments file

## Installation

To install matflow, choose one of the options from the [official instructions][installation_instructions].
Matflow is installed on a shared area on CSF3, but (currently) for full functionality
i.e. being able to pass matflow parameters directly between tasks, 
you need (the same version of) matflow installed in the task environment.

## Matflow environments

Matflow has the concept of environments, similar to python virtual environments.
These allow tasks to run using the specific software they require.
Your environment file can be be opened using `matflow open env-source`.

Alternatively, the environment file is specified in the config file,
which can be found using `matflow manage get-config-path`, or opened directly using
`matflow open config`. 
Your environment file should be listed under `environment_sources`.

An example environment file is given at [`envs.yaml`](envs.yaml).

[installation_instructions]: https://docs.matflow.io/stable/installation.html