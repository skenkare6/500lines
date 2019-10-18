import sys
from argparse import ArgumentParser, Namespace
from sys import stdin
from cachesim import Cache, MainMemory, CacheSimulator
import csv

def create_cache(f):
    """
    :param f: command line args
    :return:
    """
    mem = MainMemory()
    # cache type, sets, associativity, block size, eviction pattern: LRU, MRU, RR and FIFO
    l3 = Cache("L3", f.c3, f.a3, f.b3, "LRU")  # 20MB: 20480 sets, 16-ways with cacheline size of 64 bytes
    mem.load_to(l3)
    mem.store_from(l3)
    l2 = Cache("L2", f.c2, f.a2, f.b2, "LRU", store_to=l3, load_from=l3)  # 256KB
    l1 = Cache("L1",  f.c1, f.a1, f.b1, "LRU", store_to=l2, load_from=l2)  # 32KB
    return CacheSimulator(l1, mem)


def simulate_cache(f):
    """0x
    :param f: command line args
    :return:
    """
    cs = create_cache(f)
    # cs.load(2342)  # Loads one byte from address 2342, should be a miss in all cache-levels
    # cs.store(512, length=8)  # Stores 8 bytes to addresses 512-519,
    # # will also be a load miss (due to write-allocate)
    # cs.load(512, length=8)  # Loads from address 512 until (exclusive) 520 (eight bytes)

    index = 0
    for line in f.i:
        t = filter(None, line.split(" "))
        if len(t) < 2 or t[0] == '#':
            continue
        t[0] = t[0].split(":")[0]
        instr = int(t[0], 0)
        cs.load(int(t[2], 0))
        size = int(t[3])
        if t[1] == 'R':
            cs.load(instr)
        else:
            cs.store(instr, length=size)

        index += 1
        if index > 1000000:
            break

    cs.force_write_back()
    return cs

def row_iteration(nf, row, csvr):
    sc = simulate_cache(nf).stats()
    for s in sc:  # get the cache levels
        row.append(round(100 * s['HIT_count'] / float(s['HIT_count'] + s['MISS_count']), 2))  # hit rate percent
    csvr.writerow(row)
    f.i.seek(0)

def copy_change_arg(f, field, value):
    nf = Namespace(**vars(f))
    setattr(nf, field, value)
    return nf

def range_simulate(f):
    stddata = ['L1 HR', 'L2 HR', 'L3 HR']
    csvr = csv.writer(f.o)
    csvr.writerow(['a1'] + stddata)
    for i in range(1, f.a1, 1): # change associativity of 1st level cache
        row = [i]
        nf = copy_change_arg(f, 'a1', i)
        row_iteration(nf,row,csvr)

    csvr.writerow([])
    csvr.writerow(['a2'] + stddata)
    for i in range(1, f.a2, 1):
        row = [i]
        nf = copy_change_arg(f, 'a2', i)
        row_iteration(nf,row,csvr)

    csvr.writerow([])
    csvr.writerow(['a3'] + stddata)
    for i in range(1, f.a3, 1):
        row = [i]
        nf = copy_change_arg(f, 'a3', i)
        row_iteration(nf, row, csvr)

    csvr.writerow([])
    csvr.writerow(['b1'] + stddata)
    for i in range(4,10):
        bs = 2 ** i
        row = [bs]
        nf = copy_change_arg(f, 'b1', bs)
        row_iteration(nf, row, csvr)

    csvr.writerow([])
    csvr.writerow(['b2'] + stddata)
    for i in range(4,10):
        bs = 2 ** i
        row = [bs]
        nf = copy_change_arg(f, 'b2', bs)
        row_iteration(nf, row, csvr)

    csvr.writerow([])
    csvr.writerow(['b3'] + stddata)
    for i in range(4,10):
        bs = 2 ** i
        row = [bs]
        nf = copy_change_arg(f, 'b3', bs)
        row_iteration(nf, row, csvr)

    csvr.writerow([])
    csvr.writerow(['c1'] + stddata)
    for i in range(7,15):
        bs = 2 ** i
        row = [bs]
        nf = copy_change_arg(f, 'c1', bs)
        row_iteration(nf, row, csvr)

    csvr.writerow([])
    csvr.writerow(['c2'] + stddata)
    for i in range(7,15):
        bs = 2 ** i
        row = [bs]
        nf = copy_change_arg(f, 'c2', bs)
        row_iteration(nf, row, csvr)

    csvr.writerow([])
    csvr.writerow(['c3'] + stddata)
    for i in range(7,15):
        bs = 2 ** i
        row = [bs]
        nf = copy_change_arg(f, 'c3', bs)
        row_iteration(nf, row, csvr)


if __name__ == "__main__":
    args = ArgumentParser(description='Cache simulator based on memory trace (cachesize = a*b*c Bytes)')
    # defaults based on i7-4770k
    args.add_argument('-r', dest='r', action='store_const', default=False, const=True,
                        help='run sim over a range of values based on parameters and outputs a csv file')
    args.add_argument('-a1', dest='a1', action='store', type=int, default=8,
                        help='associativity of l1 cache (default: 8)')
    args.add_argument('-a2', dest='a2', action='store', type=int, default=8,
                        help='associativity of l2 cache (default: 8)')
    args.add_argument('-a3', dest='a3', action='store', type=int, default=16,
                        help='associativity of l3 cache (default: 16)')
    args.add_argument('-b1', dest='b1', action='store', type=int, default=64,
                        help='block size of l1 cache in B (default: 64)')
    args.add_argument('-b2', dest='b2', action='store', type=int, default=64,
                        help='block size of l2 cache in B (default: 64)')
    args.add_argument('-b3', dest='b3', action='store', type=int, default=64,
                        help='block size of l3 cache in B (default: 64)')
    args.add_argument('-c1', dest='c1', action='store', type=int, default=128,
                        help='sets of cache lines of l1 (default: 128)') # default 64KB (32 data + 32 instruction)
    args.add_argument('-c2', dest='c2', action='store', type=int, default=512,
                        help='sets of cache lines l2 (default: 512)') # default 256KB
    args.add_argument('-c3', dest='c3', action='store', type=int, default=16384,
                        help='sets of cache lines l3 (default: 16384)') # default 8MB
    args.add_argument('-i', dest='i', action='store', type=file, default=stdin,
                        help='input pinatrace file')
    args.add_argument('-o', dest='o', action='store', type=file, default=sys.stdout,
                        help='output file (default stdout)')
    f = args.parse_args()
    if f.r:
        range_simulate(f)
    else:
        simulate_cache(f).print_stats()


