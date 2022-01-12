pyint = int

from os.path import join as path_join
from config import INPUT_DIR
input_file = path_join(INPUT_DIR, 'day-16.txt')
with open(input_file) as file:
    lines = file.readlines()
    data = lines[0].strip()

print(data)

def int(x, y = 10):
    return pyint("".join(x), y)

k = list("".join(bin(int(c, 16))[2:].zfill(4) for c in data.strip()))
print("".join(k))
breakpoint()

def parse(k):
    version = int(k[:3], 2)
    k[:] = k[3:]
    typeid = int(k[:3], 2)
    k[:] = k[3:]
    if typeid == 4:
        data = []
        while True:
            cont = k.pop(0)
            data += k[:4]
            k[:] = k[4:]
            if cont == "0": break
        data = int(data, 2)
        print((version, typeid, data))
        return (version, typeid, data)
    else:
        packets = []
        if k.pop(0) == "0":
            length = int(k[:15], 2)
            k[:] = k[15:]
            d = k[:length]
            k[:] = k[length:]
            while d:
                packets.append(parse(d))
        else:
            num = int(k[:11], 2)
            k[:] = k[11:]
            for _ in range(num):
                packets.append(parse(k))
        print((version, typeid, len(packets)))
        return (version, typeid, packets)

def vsum(k):
    t = k[0]
    if k[1] == 4:
        return t
    else:
        return t + sum(map(vsum, k[2]))

q = parse(k)
print(q)

print(vsum(q))
