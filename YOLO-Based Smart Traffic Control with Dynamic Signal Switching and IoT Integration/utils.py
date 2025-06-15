import time


def logical_clock(current_time):
    return current_time + 1

def initiate_snapshot(comm, rank, state, size):
    marker_tag = 99
    snapshot = {'initiator': rank, 'state': state, 'timestamp': time.time(), 'neighbors': {}}

    for i in range(1, size):
        if i != rank:
            comm.send("MARKER", dest=i, tag=marker_tag)

    for i in range(1, size):
        if i != rank and comm.Iprobe(source=i, tag=marker_tag):
            snapshot['neighbors'][i] = comm.recv(source=i, tag=marker_tag)

    return snapshot



def heartbeat_check(comm, rank, size):
    if rank == 0:
        for i in range(1, size):
            comm.send("ping", dest=i, tag=9)
            if not comm.recv(source=i, tag=10):
                print(f"[Coordinator] No response from Node {i}!")
    else:
        if comm.recv(source=0, tag=9):
            comm.send("pong", dest=0, tag=10)