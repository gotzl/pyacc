# pyacc
Tools to access Assetto Corsa Competizione shared memory with python. Most information is obtained from the [thread in the official forum](https://www.assettocorsa.net/forum/index.php?threads/acc-shared-memory-documentation.59965/).

# usage
ACC exposes three types of shared memory blocks, `acpmf_physics`, `acpmf_graphics` and `acpmf_static`.
These memory blocks can be accessed in python via a ctypes structure. The helper function `get_mapped_object(name)` returns
such a structure for both windows and Linux, or raises a `FileNotFoundError` if the mapping does not (yet) exist.

```
import pyacc
obj = pyacc.get_mapped_object('acpmf_physics')
print(obj.speedKmh)
```

Note: a wrapper is needed to get this working in Linux. This will be commited soon.
