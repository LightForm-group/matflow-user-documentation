# Errors
## When submitting a workflow
If you get an error which (often) starts with 
```
ERROR matflow.persistence: batch update exception!
```
and ends with something like
```
File "hpcflow/sdk/app.py", line 1150, in read_known_submissions_file
File "hpcflow/sdk/app.py", line 1122, in _parse_known_submissions_line
ValueError: not enough values to unpack (expected 8, got 6)
```
This is sometimes (usually?) caused by updating matflow and leftover submissions
info causes the newer matflow version to get confused.
The fix? `matflow manage clear-known-subs`.
