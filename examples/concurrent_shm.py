import ctypes
SHM_ID = 400

def Tsum1():
    shm: int = sys_shmat(SHM_ID)
    # get the "pointer" from address id in c style
    buffer = ctypes.cast(shm, ctypes.py_object).value

    buffer.count += 1
    print(f'[print][Tsum1] buffer.count {buffer.count}')
    sys_sched()
    buffer.count += 1
    print(f'[print][Tsum1] buffer.count {buffer.count}')

def Tsum10():
    shm: int = sys_shmat(SHM_ID)
    # get the "pointer" from address id in c style
    buffer = ctypes.cast(shm, ctypes.py_object).value

    buffer.count += 10
    print(f'[print][Tsum10] buffer.count {buffer.count}')
    sys_sched()
    buffer.count += 10
    print(f'[print][Tsum10] buffer.count {buffer.count}')

def main():
    sys_shmget(SHM_ID)
    shm: int = sys_shmat(SHM_ID)
    # get the "pointer" from address id in c style
    buffer = ctypes.cast(shm, ctypes.py_object).value
    buffer.count = 0
    print(f'[print][main] buffer.count {buffer.count}')
    pid = sys_fork()
    sys_sched()  # non-deterministic context switch
    if pid == 0:
        sys_spawn(Tsum1)
        sys_spawn(Tsum10)

    else:
        buffer.count = 100
        print(f'[print][main] buffer.count {buffer.count}')
