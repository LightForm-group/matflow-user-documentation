# Setup

## Learning objectives

Be able to:

- Install MatFlow
- Configure environments file

## Installation

It is generally recommended to use separate python virtual environments for each project you're working on,

and to install MatFlow into a venv for each new project you work on.

### CSF3

- Load a recent version of python e.g.
  
  ```bash
  module load apps/binapps/anaconda3/2023.09
  ```

- Create a virtual environment where you'll install the packages needed for your project.
  This makes for a reproducible set up, and avoids potential conflicts with other packages.
  
  ```bash
  python -m venv .venv
  ```

- Activate your virtual environment (you need to do this each time you log back in to the CSF
  and want to use this venv)
  
  ```bash
  source .venv/bin/activate
  ```

- Install MatFlow as a python package (and any other python packages needed)
  
  ```bash
  pip install matflow-new
  ```

## Configuring MatFlow

This generally only needs doing once per machine

### CSF3

- Pull the CSF3 config file from a github repo
  
  ```bash
  matflow config import github://hpcflow:matflow-configs@main/manchester-CSF3.yaml
  ```
  
  This creates a file `~/.matflow-new/config.yaml` which tells MatFlow to use a shared environments file
  `/mnt/eps01-rds/jf01-home01/shared/software/matflow_envs/envs_CSF3.yaml`.

- Some of these shared environments don't include python or MatFlow itself,
  but instead "stand alone" software such as MATLAB, DAMASK, etc.
  These environments will work with any version of MatFlow.
  
  However, several of the shared environments use python packages and MatFlow,
  and they need to be used in conjunction with a specific version of MatFlow.

  We will make a copy of the shared environments file and redefine this type of environment to point
  to the venv we created earlier, so that we can use the current version of MatFlow.

  ```bash
  cp /mnt/eps01-rds/jf01-home01/shared/software/matflow_envs/envs_CSF3.yaml ~/.matflow-new
  ```

  Then we need to edit each of the environments (damask_parse, formable, defap) like this
  (remove the red `-` lines, and add the green `+` lines):
  
  ```diff
  @@ -1,37 +1,31 @@
   - name: damask_parse_env
  -  setup: |
  -    module purge
  -    source /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/matflow_full_env-linux/bin/activate
  +  setup: source /full/path/to/your/project/.venv/bin/activate
    executables:
      - label: python_script
        instances:
  -       - command: /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/matflow_full_env-linux/bin/python <<script_name>> <<args>>
  +       - command: python <<script_name>> <<args>>
            num_cores:
              start: 1
              stop: 32
            parallel_mode: null

   - name: formable_env
  -  setup: |
  -    module purge
  -    source /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/matflow_full_env-linux/bin/activate
  +  setup: source /full/path/to/your/project/.venv/bin/activate
    executables:
      - label: python_script
        instances:
  -       - command: /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/matflow_full_env-linux/bin/python <<script_name>> <<args>>
  +       - command: python <<script_name>> <<args>>
            num_cores:
              start: 1
              stop: 32
            parallel_mode: null

   - name: defdap_env
  -  setup: |
  -    module purge
  -    source /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/defdap_env-linux/bin/activate
  +  setup: source /full/path/to/your/project/.venv/bin/activate
    executables:
      - label: python_script
        instances:
  -       - command: /mnt/eps01-rds/jf01-home01/shared/software/matflow_conda_envs/defdap_env-linux/bin/python <<script_name>> <<args>>
  +       - command: python <<script_name>> <<args>>
            num_cores:
              start: 1
              stop: 32
  ```

- Edit the config file `~/.config.yaml` to point to your modified copy of the environments file 

  ```diff
  @@ -36,7 +36,7 @@
        telemetry: true
        log_file_path: logs/<<app_name>>_v<<app_version>>.log
        environment_sources:
  -       - /mnt/eps01-rds/jf01-home01/shared/software/matflow_envs/envs_CSF3.yaml
  +       - /full/path/to/HOME/.matflow-new/envs_CSF3.yaml
        task_schema_sources: []
        command_file_sources: []
        parameter_sources: []
  ```

Once you've set up MatFlow on CSF3 following the steps above,
you might prefer to reuse the python venv for subsequent projects,
to avoid reconfiguring for each venv you create.

## Running MatFlow

You will need to activate your venv each time you log in to the CSF3 and want to run MatFlow.
This is done using from directory which contains your `.venv` directory.

```bash
source .venv/bin/activate
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
