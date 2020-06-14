#!/usr/bin/env python3

import os
import re

def scandir_recursive_sorted(path, mask=re.compile(''), ext_tuple=[],
    folders=True, files=True, hidden=False, min_len=0, max_len=9999, depth=0,
    files_before_dirs=False):
    ''' Create a scandir_recursive tree and sort it '''
    tree = scandir_recursive(path, mask, ext_tuple, folders, files, hidden,
                                min_len, max_len, depth)
    tree = tree_sort(tree, depth, files_before_dirs)

    return tree

def scandir_recursive(path, mask=re.compile(''), ext_tuple=[], folders=True,
    files=True, hidden=False, min_len=0, max_len=9999, depth=0):
    '''
        A scandir implementation that allows recursiveness by level and returns
        a list of os.DirEntry objects.
        Depth starts at the maximum value and goes down by one in each function
        call until it reaches 0 where it doesn't call the function anymore.

        Returns a list of os.DirEntry objects.

        Call diagram for an example depth=1:
        ***
            Original call depth=1
                finds a file -> add to list
                finds folder -> add to list
                depth > 0
                    Call function depth=depth-1=0
                        finds a file -> add to list
                        finds folder -> add to list
                        depth not > 0
                            Doesn't call function
                        Return list
                    Add the lists from last call to this call list
                Return list
        ***

        If the depth is -1 execute maximum recursiveness.
    '''
    tree = []

    # loop through scandir
    for entry in os.scandir(path):
        # BIIIG filter logic check to add entries
        if (mask.match(entry.name) and
            (not ext_tuple or entry.name.endswith(ext_tuple)) and
            ((folders and entry.is_dir(follow_symlinks=False)) or
            (files and entry.is_file())) and
            (hidden or not entry.name.startswith('.')) and
            (min_len <= len(entry.name) <= max_len)):

            tree.append(entry)

        # When entry.is_dir
        if (entry.is_dir(follow_symlinks=False) and (hidden or not entry.name.startswith('.'))):
            # Try calling the function again inside the directory
            try:
                # If depth is already 0 skip and continue with the next step
                # of the loop
                if depth == 0: continue
                # If the depth is larger than 0 call the function again
                # with depth-1. That'll produce that when it finds another
                # directory inside it it will call the function with
                # (depth-1)-1. It'll do that until there are no more folders
                # in which case it will go back up to where it left off
                # and repeat
                elif depth > 0: next_depth = depth - 1
                # And if depth is -1 call the function again with depth=-1.
                # This will cause to call the function in every possible
                # folder
                elif depth == -1: next_depth = -1

                tree1 = scandir_recursive(entry.path, mask=mask,
                                            ext_tuple=ext_tuple,
                                            folders=folders, files=files,
                                            hidden=hidden, min_len=min_len,
                                            max_len=max_len, depth=next_depth)
                tree = tree + tree1

            # Unless it catches any of this errors
            except (FileNotFoundError, NotADirectoryError, PermissionError):
                pass

    return tree

def tree_sort(tree, depth=-1, files_before_dirs=False):
    ''' Sort the tree list with a few options '''
    # When depth wasn't 0 sort alphabetically and case-insensitively (casefold)
    # the absolute paths, this will produce having a folder followed by
    # its contents
    if depth != 0:
        tree.sort(key=lambda entry: entry.path.casefold())

    # When the depth is 0 order the list first by directories first then files
    # or viceversa depending on the files_before_dirs flag, and then by name
    # case-insensitevely (casefold)
    else:
        tree.sort(key=lambda entry:
                    (entry.is_dir() if files_before_dirs else entry.is_file(),
                    entry.name.casefold()))

    return tree

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
    parser.add_argument('path', help='Path to scan',
                        type=str)
    # Optional argument, depth, defaults to 1 if not passed
    parser.add_argument('-d', '--depth', help='Levels of recursiveness',
                        type=int, default=1)
    # Check the filename against a regular expression
    parser.add_argument('--mask', help='Filters the filenames with regular expressions',
                        type=str, default='')
    # Return the files that have any of the extensions from the list you provide
    parser.add_argument('--exts', help='Filter by extension. Takes a list of extensions you want',
                        type=list)
    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group()
    # Show folders, exclusive of showing files
    group.add_argument('--folders', help="Don't show folders. Only usable without the --files switch", action='store_false')
    # Show files, exclusive of showing folders
    group.add_argument('--files', help="Don't show files. Only usable without the --folders switch", action='store_false')
    # Default to false and then interchange it when passing the value to the
    # function because it makes sense to show files when activating the
    # --files switch and viceversa, instead of only showing something when
    # activating the switch or turning them off when activating it
    # Show hidden directories and files
    parser.add_argument('--hidden', help='Show and access hidden files and folders', action='store_true')
    # Minimum filename length
    parser.add_argument('--min_len', help='Minimum filename length', type=int, default=0)
    # Maximum filename lenth
    parser.add_argument('--max_len', help='Maximum filename length', type=int, default=9999)
    # Show files before directories, only when depth=0 
    parser.add_argument('--files_before_dirs', help='Only avaible for depth=0. If active will show files before directories', action='store_true')
    # Switch to only output execution timing
    parser.add_argument('-q', '--quiet', action='store_true')

    args = parser.parse_args()

    # Compile the regular expressions mask
    mask = re.compile(args.mask)

    # Transform the list of extensions into a tuple and add a . before the
    # extension to make sure that its an extension and not just that the
    # filename ends in that
    if args.exts: ext_tuple = tuple(['.' + i for i in args.exts])
    else: ext_tuple = tuple()

    start = time.time()
    tree = scandir_recursive_sorted(path=args.path, mask=mask,
                                    ext_tuple=ext_tuple, folders=args.files,
                                    files=args.folders, hidden=args.hidden,
                                    min_len=args.min_len, max_len=args.max_len,
                                    depth=args.depth,
                                    files_before_dirs=args.files_before_dirs)
    end = time.time() - start

    if not args.quiet:
        # Output the list
        for entry in tree:
            try:
                print(entry.path)
            # Skips files that the name can't be shown in the terminal
            except UnicodeEncodeError:
                pass
        print()

    print('exectime: {:.4} s'.format(end))

if __name__ == '__main__':
    main()