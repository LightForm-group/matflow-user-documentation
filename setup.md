# Setup

## Learning objectives

Be able to:

- Install matflow
- Configure environments file

## Installation

It is recommended to use separate python virtual environments for each project you're working on,

and to install MatFlow into a venv for each new project you work on.

### CSF3

- Load a recent version of python e.g.
  
  ```
  module load apps/binapps/anaconda3/2023.09
  ```

- Create a virtual environment where you'll install the packages needed for your project.
  This makes for a reproducible set up, and avoids potential conflicts with other packages.
  
  ```
  python -m venv .venv
  ```

- Activate your virtual environment (you need to do this each time you log back in to the CSF
  and want to use this venv)
  
  ```
  source .venv/bin/activate
  ```

- Install MatFlow as a python package (and any other python packages needed)
  
  ```
  pip install matflow-new
  ```

## Configuring MatFlow

This generally only needs doing once per machine

### CSF3

- Pull the CSF3 config file from a github repo
  
  ```
  matflow config import github://hpcflow:matflow-configs@main/manchester-CSF3.yaml
  ```
  
  This creates a file `~/.matflow-new/config.yaml` which tells MatFlow to use a shared environments file
  `/mnt/eps01-rds/jf01-home01/shared/software/matflow_envs/envs_CSF3.yaml`.

- We need to make a copy of this ...
  
  ```
  cp /mnt/eps01-rds/jf01-home01/shared/software/matflow_envs/envs_CSF3.yaml ~/.matflow-new/
  ```

- ... and then edit the copy. We're removing the `setup` section for the first three environments
  (see the diff below)
   We'll use the shared conda environments that it defines, but use our recently created python venv
   for any the python-based MatFlow environments.
  
  ```diff
  @@ -1,7 +1,4 @@
   - name: damask_parse_env
  -  setup: |
  -   module purge
  -   source /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/matflow_full_env-linux/bin/activate
    executables:
      - label: python_script
      instances:
  @@ -12,9 +9,6 @@
          parallel_mode: null
  
    - name: formable_env
  - setup: |
  -   module purge
  -   source /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/matflow_full_env-linux/bin/activate
    executables:
       - label: python_script
         instances:
  @@ -25,9 +19,6 @@
             parallel_mode: null
    - name: defdap_env
  -   setup: |
  -     module purge
  -     source /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/defdap_env-linux/bin/activate
      executables:
        - label: python_script
            instances:
  ```

- Edit the config file `~/.config.yaml` to point to your modified copy of the environments file 
  
  ```diff
  @@ -36,7 +36,7 @@
         telemetry: true
         log_file_path: logs/<<app_name>>_v<<app_version>>.log
         environment_sources:
  -      - /mnt/eps01-rds/jf01-home01/shared/software/matflow_envs/envs_CSF3.yaml
  +      - /full/path/to/HOME/.matflow-new/envs_CSF3.yaml
         task_schema_sources: []
         command_file_sources: []
         parameter_sources: []
  ```



## Matflow environments

Matflow has the concept of environments, similar to python virtual environments.
These allow tasks to run using the specific software they require.
Your environment file can be be opened using `matflow open env-source`.

It is possible to have more than one environment file,
however be careful not to duplicate environments as this will lead to an error:
https://docs.matflow.io/stable/user/how_to/environments.html

Alternatively, the environment file is specified in the config file,
which can be found using `matflow manage get-config-path`, or opened directly using
`matflow open config`.
Your environment file should be listed under `environment_sources`.

An example environment file is given at [`envs.yaml`](envs.yaml).

[installation_instructions]: https://docs.matflow.io/stable/installation.html
[install_matflow_with_pip]: https://docs.matflow.io/stable/installation.html#matflow-python-package
