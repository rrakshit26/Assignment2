#!/usr/bin/env python3
import os
import subprocess
import argparse

def get_memory_usage():
    with open('/proc/meminfo', 'r') as f:
        meminfo = f.readlines()
    total = int([line for line in meminfo if "MemTotal" in line][0].split()[1])
    available = int([line for line in meminfo if "MemAvailable" in line][0].split()[1])
    return total - available, total

def display_bar(used, total, bar_length=20):
    usage_percent = used / total
    filled_length = int(bar_length * usage_percent)
    bar = "#" * filled_length + " " * (bar_length - filled_length)
    print(f"Memory         [{bar} | {usage_percent:.0%}] {used}/{total} kB")

def get_process_memory(pid):
    rss_total = 0
    smaps_file = f'/proc/{pid}/smaps'
    if os.path.exists(smaps_file):
        with open(smaps_file, 'r') as f:
            for line in f:
                if line.startswith('Rss:'):
                    rss_total += int(line.split()[1])
    return rss_total

def main():
    parser = argparse.ArgumentParser(description="Memory Usage Viewer")
    parser.add_argument('program', nargs='?', help="Program name to analyze")
    parser.add_argument('-H', action='store_true', help="Show memory in GiB")
    parser.add_argument('-l', type=int, default=20, help="Length of the bar graph")
    args = parser.parse_args()

    if args.program:
        pids = subprocess.getoutput(f"pidof {args.program}").split()
        total_used = 0
        for pid in pids:
            rss = get_process_memory(pid)
            total_used += rss
            print(f"Process {pid}: {rss} kB")
        print(f"Total for {args.program}: {total_used} kB")
    else:
        used, total = get_memory_usage()
        if args.H:
            used, total = used / (1024 ** 2), total / (1024 ** 2)
        display_bar(used, total, args.l)

if __name__ == "__main__":
    main()
