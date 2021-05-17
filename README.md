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

# Linux
The little prog `acc_wrapper.exe` is needed to map the shared files to linux shm. There are two ways to do this

## a) 'automatic' start
Go to the ACC steamapps folder and rename `acc.exe -> _acc.exe`. Copy `acc_wrapper.exe` into the folder and rename it to `acc.exe`. When starting ACC from steam, the wrapper is invoked which then starts ACC, maps the files and waits for ACC to finish.

## b) 'manual' start (!! doesn't work yet !!)
Use the `acc_wrapper.sh` script to start `acc_wrapper.exe` in the proton prefix of ACC. The script takes two (and an optional third) arguments: 

    1. proton version, eg "6.3" or "- Experimental"
    2. path to the steamapps dir, eg "/games/steam/steamapps
    (3. path to the steamapps dir where proton is installed)

Note: the proton version has to match the one that's select in the "Compatibility" properties page of the game.
