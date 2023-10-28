#!/usr/bin/env python3

import os
import re


def scandir_recursive(
    path,
    mask=re.compile(""),
    ext_tuple=tuple(),
    folders=True,
    files=True,
    hidden=False,
    min_name_len=0,
    max_name_len=9999,
    depth=0,
    max_find_items=0,
):
    """
    A scandir implementation that allows recursiveness by level and returns
    a generator object that extracts os.DirEntry objects.
    Depth starts at the maximum value and goes down by one in each function
    call until it reaches 0 where it doesn't call the function anymore.

    Call diagram for an example depth=1:
    ***
        Original call depth=1
            finds a file -> yield
            finds folder -> yield
            depth > 0
                Call function depth=depth-1=0
                    finds a file -> yield
                    finds folder -> yield
                    depth not > 0
                        Doesn't call function
                    return to the upper level call and continue
    ***

    If the depth is -1 execute maximum recursiveness.

    Returns: generator that yields os.DirEntry objects
    """

    # Sanitize func input
    if not os.path.isdir(path):
        raise FileNotFoundError("Directory doesn't exist.")
    # Make ext_tuple into a tuple of case insensitive non-duplicate exts
    ext_tuple = _format_exts_tuple(ext_tuple)

    return _scandir_recursive(
        path,
        mask=mask,
        ext_tuple=ext_tuple,
        folders=folders,
        files=files,
        hidden=hidden,
        min_name_len=min_name_len,
        max_name_len=max_name_len,
        depth=depth,
        max_find_items=max_find_items,
    )


def scandir_recursive_sorted(
    path,
    mask=re.compile(""),
    ext_tuple=[],
    folders=True,
    files=True,
    hidden=False,
    min_name_len=0,
    max_name_len=9999,
    depth=0,
    max_find_items=0,
    files_before_dirs=False,
):
    """Create a scandir_recursive tree and sort it

    Returns: list
    """
    tree = scandir_recursive(
        path,
        mask,
        ext_tuple,
        folders,
        files,
        hidden,
        min_name_len,
        max_name_len,
        depth,
        max_find_items,
    )
    tree = tree_sort(list(tree), depth, files_before_dirs)

    return tree


def _format_exts_tuple(tuple_):
    """
    Makes extensions case insensitive, adds leading "." and removes
    possible repeats
    """
    # Make sure its a tuple and not a single str
    if not tuple_:
        return tuple()
    elif isinstance(tuple_, str):
        return (_ext_create(tuple_),)

    return tuple(set(_ext_create(ext) for ext in tuple_ if _ext_create(ext)))


def _ext_create(ext):
    if ext and ext != ".":
        if not ext.startswith("."):
            return "." + ext.lower()
        else:
            return ext.lower()


def _scandir_recursive(
    path,
    mask=re.compile(""),
    ext_tuple=tuple(),
    folders=True,
    files=True,
    hidden=False,
    min_name_len=0,
    max_name_len=9999,
    depth=0,
    max_find_items=0,
):
    """Defines the inner private function to generate and wraps it with a check for max items"""

    def _scandir_recursive_inner(
        path,
        mask=re.compile(""),
        ext_tuple=[],
        folders=True,
        files=True,
        hidden=False,
        min_name_len=0,
        max_name_len=9999,
        depth=0,
        max_find_items=0,
    ):
        # loop through scandir
        for entry in os.scandir(path):
            # BIIIG filter logic check to add entries
            if (
                mask.match(entry.name)
                and (not ext_tuple or entry.name.lower().endswith(ext_tuple))
                and (
                    (folders and entry.is_dir(follow_symlinks=False))
                    or (files and entry.is_file())
                )
                and (hidden or not entry.name.startswith("."))
                and (min_name_len <= len(entry.name) <= max_name_len)
            ):
                yield entry

            # When entry.is_dir
            if entry.is_dir(follow_symlinks=False) and (
                hidden or not entry.name.startswith(".")
            ):
                # Try calling the function again inside the directory
                try:
                    # If depth is already 0 skip and continue with the next step
                    # of the loop
                    if depth == 0:
                        continue
                    # If the depth is larger than 0 call the function again
                    # with depth-1. That'll produce that when it finds another
                    # directory inside it it will call the function with
                    # (depth-1)-1. It'll do that until there are no more folders
                    # in which case it will go back up to where it left off
                    # and repeat
                    elif depth > 0:
                        next_depth = depth - 1
                    # And if depth is -1 call the function again with depth=-1.
                    # This will cause to call the function in every possible
                    # folder
                    elif depth == -1:
                        next_depth = -1

                    sub_tree = _scandir_recursive_inner(
                        entry.path,
                        mask=mask,
                        ext_tuple=ext_tuple,
                        folders=folders,
                        files=files,
                        hidden=hidden,
                        min_name_len=min_name_len,
                        max_name_len=max_name_len,
                        depth=next_depth,
                        max_find_items=max_find_items,
                    )
                    yield from sub_tree

                # Unless it catches any of this errors
                except (
                    FileNotFoundError,
                    NotADirectoryError,
                    PermissionError,
                ):
                    pass

    tree = _scandir_recursive_inner(
        path,
        mask=mask,
        ext_tuple=ext_tuple,
        folders=folders,
        files=files,
        hidden=hidden,
        min_name_len=min_name_len,
        max_name_len=max_name_len,
        depth=depth,
    )

    i = 0
    # Yields from generator while less items found than max
    # If max is 0 yield all
    while (x := next(tree, None)) is not None and (
        0 == max_find_items or i < max_find_items
    ):
        i += 1
        yield x


def tree_sort(tree, depth=-1, files_before_dirs=False):
    """Sort the tree list with a few options"""
    # When depth wasn't 0 sort alphabetically and case-insensitively (casefold)
    # the absolute paths. This will produce having a folder followed by
    # its contents
    if depth != 0:
        tree.sort(key=lambda entry: entry.path.casefold())

    # When the depth is 0 order the list by directories first, then files
    # or viceversa depending on the files_before_dirs flag, and then by name
    # case-insensitevely (casefold)
    else:
        tree.sort(
            key=lambda entry: (
                entry.is_dir() if files_before_dirs else entry.is_file(),
                entry.name.casefold(),
            )
        )

    return tree


###############################################################################
"""
MAIN
"""
###############################################################################


def cli_run():
    import time
    import argparse

    # Call the argument parse object
    parser = argparse.ArgumentParser()
    # Define the arguments
    # Obligatory argument, path
    parser.add_argument("path", help="Path to scan", type=str)
    # Optional argument, depth, defaults to 0 if not passed
    parser.add_argument(
        "-d",
        "--depth",
        help=(
            "Levels of recursiveness. Defaults to 0 (just the specified direct"
            "ory)"
        ),
        type=int,
        default=0,
    )
    # Check the filename against a regular expression
    parser.add_argument(
        "--mask",
        help="Filters the filenames with regular expressions",
        type=str,
        default="",
    )
    # Return the files that have any of the extensions from the list you provide
    parser.add_argument(
        "--exts",
        help="Filter by extension. Takes a list of extensions you want",
        nargs="*",
        type=str,
        default=tuple(),
    )
    # Create a mutually exclusive group
    files_or_folders = parser.add_mutually_exclusive_group()
    # Show folders, exclusive of showing files
    files_or_folders.add_argument(
        "--folders",
        help="Only show folders. Only usable without the --files switch",
        action="store_false",
    )
    # Show files, exclusive of showing folders
    files_or_folders.add_argument(
        "--files",
        help="Only show files. Only usable without the --folders switch",
        action="store_false",
    )
    # Default to false and then interchange it when passing the value to the
    # function because it makes sense to show files when activating the
    # --files switch and viceversa, instead of only showing something when
    # activating the switch or turning them off when activating it
    # Show hidden directories and files
    parser.add_argument(
        "--hidden",
        help="Show and access hidden files and folders",
        action="store_true",
    )
    # Minimum filename length
    parser.add_argument(
        "--min_name_len", help="Minimum filename length", type=int, default=0
    )
    # Maximum filename lenth
    parser.add_argument(
        "--max_name_len",
        help="Maximum filename length",
        type=int,
        default=9999,
    )
    # Maximum items found
    parser.add_argument(
        "--max_find_items",
        help="Stop Searching when max found items are reached",
        type=int,
        default=0,
    )
    # Show files before directories, only when depth=0
    parser.add_argument(
        "--files_before_dirs",
        help=(
            "Only avaible for depth=0. If active will show files before direct"
            "ories"
        ),
        action="store_true",
    )
    # Switch to only output execution timing
    parser.add_argument("-q", "--quiet", action="store_true")

    args = parser.parse_args()

    # Compile the regular expressions mask
    mask = re.compile(args.mask)

    start = time.time()
    tree = scandir_recursive_sorted(
        path=args.path,
        mask=mask,
        ext_tuple=args.exts,
        folders=args.files,
        files=args.folders,
        hidden=args.hidden,
        min_name_len=args.min_name_len,
        max_name_len=args.max_name_len,
        depth=args.depth,
        max_find_items=args.max_find_items,
        files_before_dirs=args.files_before_dirs,
    )
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

    print(f"Found items: {len(tree)}")
    print(f"exectime: {end:.4}s")


if __name__ == "__main__":
    cli_run()
