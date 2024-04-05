# How to run the examples

```
matflow go hello.yaml
```

# Things I learned

## about Matflow

- Task schemas and workflows (a list of tasks) can go in the same yaml file 
  (at least for development)

- In order to pass the input/output variables around, you need to wrap 
  parameters and scripts etc with some matflow syntax like this:

  ```
  <<parameter:parameter_name>>
  <<script:path/to/script>>
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

- The env.yaml file in use is defined in the config.yaml file under `environment_sources`

- New Matflow environments can have module load/activate venv steps under `setup` key

- It is best to stick with using `python_script` as the label for any python executables,
  for consistency with existing matflow tasks which you might want to call in your workflow
  which will expect this label

## about YAML

- https://www.yaml.info/learn/bestpractices.html
  - YAML can use indented, or zero-indented lists (sequences), where the hyphen is
    at the same level of indentation as the previous line.
    The creators recommend this zero-indented approach, but you can use either, and interchangeably.
    It can help to view the indentation by considering the text rather than
    the hyphen.
