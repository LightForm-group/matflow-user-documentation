# Terminology
## Workflow template
A workflow template can be thought of like a function definition
in python: it shows the required inputs,
the steps which would be executed, and the resulting outputs.
However, it doesn't actually run the workflow.
A workflow template consists of the matflow environment,
the task schemas, and the command files.

## Task schemas
These are like a template for a task you want to run,
with definitions of the input and outputs that are expected.

Matflow has many build-in task schemas, but you may want to
write your own.

## Command files
If you want to refer to any files that are used as inputs or output,
they should be listed under `command_files`

```
command_files:
  - label: new_inp_file
    name:
      name: friction_conductance.inp
```
## Tasks
These are actual usages of a task schema, run with defined inputs.

## Workflows
A workflow is just a list of tasks run one after the other.

# Writing your own task schemas and workflows
## Workflow files
In-built matflow workflows are split up over a few different files,
but for development, your workflow code can all go in one yaml file.
The workflow template has a top-level key `template_components:`
underneath which comes the `task_schema`, `environments` and `command_files` keys.

The workflow itself goes under a different top-level `tasks:` key

## Components of a task schema
### Required keys
- `objective` (this is a name or label for the schema)
- `actions` (what the task schema actual "does")

### Optional keys
- `inputs`
- `outputs`

## Matflow syntax
If you want to reference parameters in the action of your task schema,
it should be done using this syntax:
`<<parameter:your_parameter_name>>`.

Similarly, commands defined in an environment can be used like this:
`<<executable:your_executable>>`, and files defined as `command_files`
are referenced using `<<file:your_command_file>>` e.g.
```
actions:
- commands:
  - command: <<executable:abaqus>> job=sub_script_check input=<<file:new_inp_file>> interactive
```

Note that while command files can be referenced in an action, they cannot be referenced in this way as an input to a task schema.

Python scripts however are executed slightly differently, and run the first
function defined in your python file, which must have the same name as the python file.
The `<<script:...` syntax adds some extra processing so you can call the (first)
function in your python file with arguments, and pass any returned values back to matflow e.g:
```
actions:
- script: <<script:/full/path/to/my_script.py>>
```
where `my_script.py` would start with a function definition like this:
```python
def my_script():
    ...
```


## Passing variables around a workflow
Python scripts that are run by top-level actions and which return values directly
(i.e. instead of saving to a file) should return a dictionary of values,
containing keys matching the output parameters defined in the task schema.
e.g.
```
return {output_parameter_1: values, output_parameter_2: other_values}
```

In order for the dictionaries returned from tasks to be accessible to other tasks,
the task schemas needs to set the input and output type accordingly:

```
...
  actions:
  - script: <<script:/full/path/to/my_script.py>>
    script_data_in: direct
    script_data_out: direct
```

It might however be more appropriate to save results to files instead.

In addition to passing variables directly,
tasks can read parameters from (and save to) various file formats including json and HDF5.

An example of passing variables via json files is given in [pass_as_json.yaml](pass_as_json.yaml).
MatFlow writes the input parameters into a json file `js_0_act_0_inputs.json`,
and the output into a file `js_0_act_0_outputs.json`.
These file names are generated automatically,
and MatFlow keeps track of where the various parameters are stored.
So if any parameters saved in json files (or passed directly) are needed as input for another function,
MatFlow can pass them directly or via json as specified in the task schema.
An example is given of both combinations.

The particular variables names used to pass parameters using json/HDF5 depend on
which language is being used.
For example using MATLAB uses this syntax `inputs_JSON_path`, `outputs_HDF5_path`
instead of the python equivalents `_input_files` and `_output_files`
See the MTEX examples for more details.

## Writing a workflow
A workflow is just a list of tasks, which are run like this

```
tasks:
- schema: my_task_schema
  inputs:
    my_input: input_value
```

A task can find output variables from previous tasks, and use them
as inputs. There is generally no need specify them explicitly,
but this can be done by using the `input_sources` key within a task
to tell MatFlow where to obtain input values for a given input parameter,
in combination with the dot notation e.g.

```
- schema: print
  # Explicitly reference output parameter from a task
  input_sources:
    string_to_print: task.python_greet
```

When running a workflow with Matflow, the required files are copied into a directory
that matflow creates, and any output files are saved into the `execute` directory.
If you want to keep any of theses files, you should copy them to the `artifacts`
directory using `save_files`:

```
task_schemas:
- objective: my_task_schema
  inputs:
  - parameter: my_input
  outputs:
  - parameter: my_output
  actions:
  - environments: ...
    commands: ...
    save_files:
    - my_command_file
```
There are a couple of examples of this in the [example advanced workflow](advanced_workflow.yaml)

## Running your workflow
```
matflow go my_workflow.yaml
```

## Checking on a workflow
When a workflow is running, or indeed after it has finished, you can check whether it was successful using

```
matflow show
```

or if you want task-level detail
```
matflow show -f
```

This will show the last few workflows. However if you're checking on an older workflow you might need to
tell MatFlow to show more results. This is done using e.g.

```
matflow show -f -r N
```
to show the last `N` results.

## Cancelling a workflow
Sometimes you might want to cancel a workflow that is running.
Use
```
matflow cancel WORKFLOW_REF
```
where `WORKFLOW_REF` is either the path to the workflow directory, or the number of the workflow
displayed by `matflow show`.
