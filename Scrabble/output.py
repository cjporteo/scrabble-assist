from rack import Rack
import time


def results(tiles, dd, t, rows):

    rack = Rack(tiles, dd, t)
    cutoffs = {0: 15,
               1: 10,
               2: 7,
               3: 0}

    time_0 = time.time()

    if rack.num_letters >= cutoffs[min(rack.num_blanks, 3)]:
        res = rack.frequency_solve()
        solver = 'F'
    else:
        res = rack.permute_solve()
        solver = 'P'

    time_1 = time.time()
    time_ms = 1000 * (time_1 - time_0)

    if len(res) < 1:
        print("\nNo valid words found. ({}-Solve runtime: {:.2f} ms)".format(solver, time_ms))
        return

    entries = []  # cells of the table
    lines = [""] * rows  # rows of the table
    pad_wc, pad_bc = 4, 8  # padding within column, padding between columns
    shift = pad_wc + len(res[0])

    for play in res:
        spaces = shift - len(play) if len(play) < 10 else shift - 1 - len(play)
        entries.append(play + (" " * spaces) + str(len(play)))
    print("\nLongest words: ({}-Solve runtime: {:.2f} ms)".format(solver, time_ms))

    for i, entry in enumerate(entries):
        spaces = " " * pad_bc if i >= rows else ""
        lines[i%rows] += spaces + entry

    for line in lines:
        if line:
            print(line)
