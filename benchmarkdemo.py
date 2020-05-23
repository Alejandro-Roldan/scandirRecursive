#!/usr/bin/env python3

from scandirrecursive import scandir_recursive
import os
import time


def walker(path, levels=1):
    ''' Small recursive limited os.walk implementation '''
    files=[]
    directories=[]

    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath[len(path):].count(os.sep) >= levels:
            del dirnames[:]
        for name in filenames:
            files.append(os.path.join(dirpath, name))
        for name in dirnames:
            directories.append(os.path.join(dirpath, name))

    files.sort(key=str.lower)
    directories.sort(key=str.lower)

    return files, directories

def lister(path):
    '''
        listdir that outputs in the same way as my scandir_recursive
        (a directories list and a files list with absolute paths)
    '''
    files=[]
    directories=[]

    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)): directories.append(item)
        else: files.append(item)

    files.sort(key=str.lower)
    directories.sort(key=str.lower)

    return files, directories


###########################################################################
###########################################################################
'''
    Compare the scandir_recursive function against the listdir for depth 0 and
    os.walk for different depths and time the execution times.
'''
path = '/'

###########################################################################
# DEPTH 0
start = time.time()
dirs, files = scandir_recursive(path, depth=0)
end = time.time() - start
print('scandir_recursive (depth=0):')
print('\ttime: {:.3}s'.format(end))

start = time.time()
dirs, files = lister(path)
end = time.time() - start
print('listdir (not recursive func):')
print('\ttime: {:.3}s'.format(end))

print('-'*50)##############################################################
# DEPTH 6
start = time.time()
dirs, files = scandir_recursive(path, depth=6)
end = time.time() - start
print('scandir_recursive (depth=6):')
print('\ttime: {:.3}s'.format(end))

start = time.time()
dirs, files = walker(path, levels=6)
end = time.time() - start
print('walk_limited (depth=6):')
print('\ttime: {:.3}s'.format(end))

print('-'*50)##############################################################
# MAS DEPTH
start = time.time()
dirs, files = scandir_recursive(path, depth=-1)
end = time.time() - start
print('scandir_recursive (max depth):')
print('\ttime: {:.3}s'.format(end))

start = time.time()
dirs, files = walker(path, levels=999999999999)
end = time.time() - start
print('walk (max depth):')
print('\ttime: {:.3}s'.format(end))

print('-'*50)##############################################################
