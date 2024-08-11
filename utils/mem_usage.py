import psutil

def mem_usage():
    p = psutil.Process()
    print(f'mem usage : {p.memory_info().rss/2**20}MB')
    return p.memory_info().rss/2**20