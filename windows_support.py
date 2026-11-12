"""Windows metrics and a kill-on-close job; Python standard library only."""
import ctypes,os,platform,shutil
from ctypes import wintypes as w

class Memory(ctypes.Structure):
    _fields_=[('length',w.DWORD),('load',w.DWORD)]+[(n,ctypes.c_ulonglong) for n in
        ['totalPhys','availPhys','totalPage','availPage','totalVirtual','availVirtual','availExtended']]

def hardware():
    m=Memory();m.length=ctypes.sizeof(m)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):raise ctypes.WinError()
    return {'os':platform.platform(),'cpu':platform.processor(),'logicalProcessors':os.cpu_count(),
            'physicalRamBytes':m.totalPhys,'availableRamBytes':m.availPhys,
            'physicalRamGiB':round(m.totalPhys/1024**3,2),'targetRamGB':16,
            'targetHardwareTest':14*1024**3<=m.totalPhys<=18*1024**3}

class BasicLimits(ctypes.Structure):
    _fields_=[('processTime',ctypes.c_longlong),('jobTime',ctypes.c_longlong),('flags',w.DWORD),
        ('minWork',ctypes.c_size_t),('maxWork',ctypes.c_size_t),('active',w.DWORD),
        ('affinity',ctypes.c_size_t),('priority',w.DWORD),('scheduling',w.DWORD)]
class IoCounters(ctypes.Structure):
    _fields_=[(n,ctypes.c_ulonglong) for n in ['readOps','writeOps','otherOps','readBytes','writeBytes','otherBytes']]
class ExtendedLimits(ctypes.Structure):
    _fields_=[('basic',BasicLimits),('io',IoCounters)]+[(n,ctypes.c_size_t) for n in
        ['processMemory','jobMemory','peakProcessMemory','peakJobMemory']]

class ChildJob:
    def __init__(self,process):
        self.k=ctypes.WinDLL('kernel32',use_last_error=True)
        self.k.CreateJobObjectW.argtypes=[ctypes.c_void_p,w.LPCWSTR];self.k.CreateJobObjectW.restype=w.HANDLE
        self.k.SetInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p,w.DWORD]
        self.k.SetInformationJobObject.restype=w.BOOL
        self.k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];self.k.OpenProcess.restype=w.HANDLE
        self.k.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE];self.k.AssignProcessToJobObject.restype=w.BOOL
        self.k.CloseHandle.argtypes=[w.HANDLE];self.k.CloseHandle.restype=w.BOOL
        self.handle=self.k.CreateJobObjectW(None,None)
        if not self.handle:raise ctypes.WinError(ctypes.get_last_error())
        limits=ExtendedLimits();limits.basic.flags=0x2000 # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.k.SetInformationJobObject(self.handle,9,ctypes.byref(limits),ctypes.sizeof(limits)):
            error=ctypes.WinError(ctypes.get_last_error());self.close();raise error
        child=self.k.OpenProcess(0x0100|0x0001,False,process.pid)
        if not child:self.close();raise ctypes.WinError(ctypes.get_last_error())
        try:
            if not self.k.AssignProcessToJobObject(self.handle,child):
                error=ctypes.WinError(ctypes.get_last_error());self.close();raise error
        finally:self.k.CloseHandle(child)
    def close(self):
        if self.handle:self.k.CloseHandle(self.handle);self.handle=None

def clean_child_env(engine_dir,key):
    system=os.environ.get('SystemRoot',r'C:\Windows')
    env={k:os.environ[k] for k in ['SystemRoot','WINDIR','TEMP','TMP','COMSPEC','NUMBER_OF_PROCESSORS','PROCESSOR_ARCHITECTURE'] if k in os.environ}
    env.update(PATH=str(engine_dir)+os.pathsep+os.path.join(system,'System32'),OMP_NUM_THREADS='2',LLAMA_API_KEY=key)
    return env
