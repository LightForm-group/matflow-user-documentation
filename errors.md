# Errors
## `ERROR matflow.persistence: batch update exception!`
This is sometimes (usually?) caused by updating matflow and leftover submissions
info causes the newer matflow version to get confused.
The fix? `matflow manage clear-known-subs`.