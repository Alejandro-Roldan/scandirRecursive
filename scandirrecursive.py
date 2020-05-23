#!/usr/bin/env python3

import os

def scandir_recursive(path, depth=1, rtrn_names=False):
    '''
        A scandir implementation that allows recursiveness by level.
        Depth starts at the maximum value and goes down by one in each function
        call until it reaches 0 where it doesn't call the function anymore.
        Call diagram for an example depth 1:
        ***
            Original call depth 1
                finds a file -> add to list
                finds folder -> add to list
                depth > 0
                    Call function depth 0
                        finds a file -> add to list
                        finds folder -> add to list
                        depth not > 0
                            Doenst call function
                    add the lists from last call to this calls lists
                Return lists
        ***

        If the depth is -1 does maximum recursiveness.

    '''
    def _scandir_recursive(path, depth=1):
        # Initialize empty lists
        files=[]
        directories=[]

        # loop through scandir
        for entry in os.scandir(path):
            if entry.is_file() or entry.is_symlink():
                files.append(entry.path)
            else:
                directories.append(entry.path)
                # For directories after adding them try to call the function
                # again on the directory
                try:
                    # If depth is already 0 continue with the next step of
                    # the loop
                    if depth == 0:
                        continue
                    # If the depth is larger than 0 call the function again
                    # with depth-1. Thatll produce that when it finds another
                    # directory inside it will call the function with
                    # (depth-1)-1. Itll do that until there are no more folders
                    # in which case it will go back up to where it left of
                    # and repeat
                    elif depth > 0:
                        files1, directories1 = _scandir_recursive(entry.path, depth-1)
                    # And if depth is -1 call the function again with depth -1.
                    # This will cause to call the function in every possible
                    # folder
                    elif depth == -1:
                        files1, directories1 = _scandir_recursive(entry.path, -1)

                    # Now add the files and directories from that subfolder to
                    # the list in this level
                    files = files + files1
                    directories = directories + directories1

                # Unless it catches any of this errors
                except (FileNotFoundError, NotADirectoryError, PermissionError):
                    pass

        return files, directories

    directories, files = _scandir_recursive(path, depth)

    # Once the whole lists have been created, sort them
    files.sort(key=str.lower)
    directories.sort(key=str.lower)

    # Transform them to basenames
    if rtrn_names:
        files = _split(files)
        directories = _split(directories)

    return files, directories

def _split(list_):
    ''' Takes a list of absolute paths and returns the basename '''
    return [os.path.split(item)[1] for item in list_]

###############################################################################
'''
MAIN
'''
###############################################################################

def main():
    import time
    import argparse

    # Call the argument parse object
    parser = argparse.ArgumentParser()
    # Define the arguments
    # Obligatory argument, path
    parser.add_argument("path", help="path to scan",
                        type=str)
    # Optional argument, depth, defaults to 1 if not passed
    parser.add_argument("-d", "--depth", help="levels of recursiveness",
                        type=int, default=1)
    # Switch to return names instead of absolute paths
    parser.add_argument("-p", "--returnnames", help="output basenames",
                    action="store_true")
    # Switch to only output execution timing
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()


    start = time.time()
    files, directories= scandir_recursive(
                                            args.path,
                                            depth=args.depth,
                                            rtrn_names=args.returnnames
                                            )
    end = time.time() - start

    # Join file and dirs into one list and sort it
    files_and_dirs = sorted(directories + files, key=str.lower)
    if not args.quiet:
        # Output the list
        for item in files_and_dirs:
            try:
                print(item)
            # Skips files with non-UTF-8 names
            except UnicodeEncodeError:
                pass
        print()

    print('exectime: {:.4} s'.format(end))

if __name__ == '__main__':
    main()