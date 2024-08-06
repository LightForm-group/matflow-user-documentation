# Resources

Requesting resources can be done using a `resources` block, either for the whole workflow at the top level,

```
resources:
  any:
    scheduler: sge # Setting the scheduler is not normally needed because a
                   # `default_scheduler` will be set in the config file.
    scheduler_args:
      shebang_args: --login
      options:
        -l: short
```

or at the task level

```
- schema: simulate_VE_loading_damask
  resources:
    any:
      # This will use two cores for input file generators and output file parsers
      num_cores: 2
    main:
      # Use 16 cores for the "main" part of the task (the simulation in this case)
      num_cores: 16
  inputs:
    ...
```

We can see from above that it is possible to request resources for subsets of the actions
in a task schema. A full list of the different options you can select resources for is given below.

- `input_file_generator`
- `output_file_parser`
- `processing` (a shortcut for `input_file_generator` +  `output_file_parser`)
- `main` (the main part of the action i.e. not `processing`)
- `any` (anything not already specified with any of the above options)

These are used to choose resources (done at the workflow/task level),
and also the same values can be used within the schema to select an `environment`
by `scope` e.g.

```
actions:
- environments:
  - scope:
      type: processing
    environment: damask_parse_env
  - scope:
      type: main
    environment: damask_env
```

MatFlow is then looking for a match within your environment definitions for the requested
resources, and will run the command which matches those resources.

The [official docs](https://docs.matflow.io/stable/reference/_autosummary/matflow.ResourceSpec.html)
list the available resource options that can be requested.

# Tasks

## Sequences

Matflow can run tasks over a set of inputs values, if the iterations are independent.
For this, you use a `sequence`, and a `nesting_order` to control the nesting of the loops
but you can also "zip" two or more lists of inputs by using the same level of nesting.
Lower values of `nesting_order` act like the "outer" loop.

```
tasks:
- schema: my_schema
  sequences:
  - path: inputs.conductance_value
  values:
  - 0
  - 100
  - 200
  nesting_order: 0
```

## Groups

To combine outputs from multiple sequences, you can use a `group` in a task schema:

```
- objective: my_task_schema
  inputs:
  - parameter: p2
    group: my_group
```

combined with a `groups` entry in the task itself.

```
- schema: my_task_schema
  groups:
  - name: my_group
```

Then whichever parameters are linked with the group in the task schema will be received by the task as a list.

# Task schemas

## Input file generators

`input_file_generators` is a convenience shortcut for a python script which generates an input file
for a subsequent action within a task. It's more compact, easier to reference, and has more interaction options.
The first parameter in the input generator (python) function definition must be "path",
which is the file path to `input_file`, the file you want to create.
Given this is a Matflow input file, the path is just the file name which will be created in the
execute directory.
The `input_file` must point to the label of a file in `command_files`.
`from_inputs` defines which of the task schema inputs are required for each of the `input_file_generators`.

```
task_schemas:
- objective: my_task_schema
  actions:
  - input_file_generators:
    - input_file: my_command_file
    from_inputs:
    - my_input_1
    - my_input_2
    script: <<script:/full/path/to/generate_input_file.py>>
```

An example is given in [advanced_workflow.yaml](advanced_workflow.yaml), along with the alternative code which would be needed

to achieve the same result without an input file generator.

## Output file parsers

`output_file_parsers` is a shortcut for a python script which processes output files
from previous steps.
The function in the python script must have parameters for each of the files listed
in `from_files`, and this function should return data in a dictionary.
If you want to save results to a file, this can be done in the python function too,
but the function should return a dict. This can be hard-coded in the function,
or via an `inputs: [path_to_output_file]` line in the output file parser,
and it will come after the output files in the function signature.
There is currently a bug such that files used in `output_file_parsers` are
automatically saved, so if you have explictly saved them already using `save_files` in
the main action, it will crash. You need to remove them from that `save_files` list in
the main action, but leave them as `command_files` because they're referenced by the
output file parser.
The "name" of the `output_file_parsers` is the parameter returned i.e.

```
output_file_parsers:
  return_parameter: # This should be listed as an output parameter for the task schema
    from_files:
    - command_file1
    - command_file2
    script: <<script:your_processing_script.py>>
    save_files:
    - command_file_you_want_to_save
```

The output_file_parser script that is run as the action should return one variable,
rather than a dictionary. This is different behaviour to
a "main" action script.
i.e. `return the_data` rather than `return {"return_parameter": the_data}`
