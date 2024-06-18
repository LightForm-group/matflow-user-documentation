# How to run the examples

```
matflow go hello.yaml
```

# Things I learned

## about Matflow

- Task schemas, workflows (a list of tasks), and environments can go in the same yaml file
  (at least for development)

- In order to pass the input/output variables around, you need to wrap
  parameters and scripts etc with some matflow syntax like this:
  
  ```
  <<parameter:parameter_name>>
  <<script:/full/path/to/script>>
  ```
  
  The `<<script...` syntax adds some extra processing so you can call the (first)
  function in your python file with arguments, and pass any returned values back to matflow.

- Output variables from a function should be wrapped in a dictionary,
  containing keys from the task schema output parameters.

- A task can find output variables from previous tasks, and use them
  as inputs. There is generally no need specify them explicitly,
  but this can be done by using the `input_sources` key within a task
  to tell MatFlow where to obtain input values for a given input parameter,
  in combination with the dot notation e.g. `task.python_greet`.

- The `envs.yaml` file in use is defined in `~/.matflow-new/config.yaml` under `environment_sources`

- New Matflow environments can have module load/activate venv steps under `setup` key

- It is best to stick with using `python_script` as the label for any python executables,
  for consistency with existing matflow tasks which you might want to call in your workflow which will expect this label

- (python) functions used in task schemas which return values directly
  should return a dictionary with keys corresponding to the output parameters

- `save_files` tells matflow to copy files from the execute directory to the artifacts directory
  (matflow considers the execute directory temporary)

- It's possible to add a task to a completed workflow (not zipped) using `wk.add_task(...)`,
  but not using the CLI

- Errors like `ERROR matflow.persistence: batch update exception!`,
  without any obvious cause are sometimes caused by updating matflow and leftover submissions
  info which can be cleared with `matflow manage clear-known-subs`.

- `input_file_generators` is a convenience shortcut for a python script which generates an input file
  for a subsequent task. Not sure of all the  details but it's more compact, easier to reference,
  and has more interaction options.
  The first parameter in the input generator (python) function definition must be "path",
  which is the file path to `input_file`, the file you want to create.
  The `input_file` must point to the label of a file in `command_files`.
  `from_inputs` defines which of the task schema inputs are required for each of the `input_file_generators`.

- `output_file_parsers` is a shortcut for a python script which processes output files
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

- Matflow stores output values using its own storage format based on Zarr - as such
  not all possible options are supported (currently pandas dataframes are not).

- Matflow can run tasks over a set of inputs values, if the iterations are independent.
  For this, you use a `sequence`, and a `nesting_order` to control the nesting of the loops
  but you can also "zip" two or more lists of inputs by using the same level of nesting.

  ```
  sequences:
  - path: inputs.conductance_value
   values:
   - 0
   - 100
   - 200
   nesting_order: 0
  ```

## about YAML

- https://www.yaml.info/learn/bestpractices.html
  - YAML can use indented, or zero-indented lists (sequences), where the hyphen is
    at the same level of indentation as the previous line.
    The creators recommend this zero-indented approach, but you can use either, and interchangeably.
    It can help to view the indentation by considering the text rather than
    the hyphen.
