import sys
import mmap
import ctypes

from .acc_types import *


# https://stackoverflow.com/questions/10322974/how-to-find-out-if-a-windows-memory-mapped-file-already-exists-using-python
def check_file_is_mapped_file(file_name, file_size):
    _CreateFileMapping = ctypes.windll.kernel32.CreateFileMappingW
    _CloseHandle = ctypes.windll.kernel32.CloseHandle
    _GetLastError = ctypes.windll.kernel32.GetLastError
    INVALID_HANDLE_VALUE = ctypes.wintypes.HANDLE(-1) #from msdn
    PAGE_READWRITE = 0x04 #from msdn
    ERROR_ALREADY_EXISTS = 0xB7 #from msdn
    h =_CreateFileMapping(INVALID_HANDLE_VALUE,0,PAGE_READWRITE,0,file_size, ctypes.c_wchar_p(file_name))
    ret = (h != INVALID_HANDLE_VALUE) and (_GetLastError() == ERROR_ALREADY_EXISTS)
    if h != INVALID_HANDLE_VALUE:
    	_CloseHandle(h)
    return ret


types = {
    'acpmf_physics': SPageFilePhysics,
    'acpmf_graphics': SPageFileGraphic,
    'acpmf_static': SPageFileStatic,
}


def get_mapped_object(name):
    if sys.platform == "win32":
        map_name = u"Local\\%s" % name
        if not check_file_is_mapped_file(map_name, 2048):
            raise FileNotFoundError('FileMapping \'%s\' does not exist.'%(map_name))
        _obj = types[name].from_buffer(mmap.mmap(-1, ctypes.sizeof(types[name]), map_name))
    else:
        # this does not work properly since the shm is not 'owned' by python
        # and needs to persist even if the reference to the shm is removed
        # _shm = shared_memory.SharedMemory(i, create=False)
        # shm[i] = ty.from_buffer(_shm.buf)

        with open('/dev/shm/%s' % name, 'r+b') as f:
            _obj = types[name].from_buffer(mmap.mmap(f.fileno(), 0))
    return _obj
