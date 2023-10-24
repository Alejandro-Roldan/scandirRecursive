#!/usr/bin/env python3

"""
    Compare the scandir_recursive function against the listdir for depth 0 and
    os.walk for different depths and measure the execution times.
"""

from scandirrecursive import scandir_recursive
import os
import time


def walker(path, levels=1):
    tree = []

    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath[len(path) :].count(os.sep) >= levels:
            del dirnames[:]
        for name in filenames:
            tree.append(os.path.join(dirpath, name))
        for name in dirnames:
            tree.append(os.path.join(dirpath, name))

    return tree


def lister(path):
    tree = [item for item in os.listdir(path)]

    return tree


###############################################################################
###############################################################################

path = "/"

###############################################################################
# DEPTH 0
start = time.time()
tree = scandir_recursive(path, depth=0)
end = time.time() - start
print("scandir_recursive (depth=0):")
print("\ttime: {:.3}s".format(end))

start = time.time()
tree = lister(path)
end = time.time() - start
print("listdir (not recursive func):")
print("\ttime: {:.3}s".format(end))

print("-" * 50)  ##############################################################
# DEPTH 6
start = time.time()
tree = scandir_recursive(path, depth=6)
end = time.time() - start
print("scandir_recursive (depth=6):")
print("\ttime: {:.3}s".format(end))

start = time.time()
tree = walker(path, levels=6)
end = time.time() - start
print("walk_limited (depth=6):")
print("\ttime: {:.3}s".format(end))

print("-" * 50)  ##############################################################
# MAX DEPTH
start = time.time()
tree = scandir_recursive(path, depth=-1)
end = time.time() - start
print("scandir_recursive (max depth):")
print("\ttime: {:.3}s".format(end))

start = time.time()
tree = walker(path, levels=999999999999)
end = time.time() - start
print("walk (max depth):")
print("\ttime: {:.3}s".format(end))

print("-" * 50)  ##############################################################
