# scandirRecursive
A os.scandir implementation that supports recursiveness aswell as a maximum threshold depth in the recursiveness.
More or less same speed as os.list and os.walk (a bit slower) but has the advantage that my sacandir_recursive returns a list of os.DirEntry objects which is a big plus since it has a lot more information at hands reach and faster too since you don't need to call os.stat again. Also can optianally filter the outputted entries by several fields.

- scandir_recursive(): A scandir implementation that allows recursiveness by level and returns a list of os.DirEntry objects. It doesn't follow symbolic links.

Depth starts at the maximum value and goes down by one in each function call until it reaches 0 where it doesn't call the function anymore.

Returns a list of os.DirEntry objects.

Call diagram for an example depth=1:
```
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
```
If the depth is -1 execute maximum recursiveness.

It takes a path, a depth level int (where -1 means max) and the optional filters:
	- mask: Filters the filenames with regular expressions
	- exts: Filter by extension. Takes a list of extensions you want in the form \['mp3','jpg'\]
	- folders: Don't show folders
	- files: Don't show files
	- hidden: Show and access hidden files and folders
	- min_len: Minimum filename length
	- max_len: Maximum filename length
	
- tree_sort(): Sort the list tree that scandir_recursive outputs alphabetically and case-insensitively the absolute paths, this will produce having a folder followed by its contents. When the depth=0 separate the tree into files and directories, sort each of them alphabetically case-insensitive, and then join them together again. Takes the tree list and the optional arguments:
	- depth: default value of -1
	- files_before_dirs: Only avaible for depth=0. If active will show files before directories
    
- scandir_recursive_sorted(): Calls the scandir_recursive and tree_sort functions one after the other. For easyness and code cleaness. Takes the combination of both functions arguments (except the tree argument from tree_sort since it takes the output of the scandir_recursive directly).

Calling the script from terminal deploys a command utility much like the command "ls". Mainly for testing since its obviously worse as a command.

Benchmarks
----------
When running the benchmark that compares the os.walk method with this recursive scandir method, both starting from the root directory, the results are:
```
scandir_recursive (depth=0):
	time: 7.56e-05s
listdir (not recursive func):
	time: 3.43e-05s
--------------------------------------------------
scandir_recursive (depth=6):
	time: 1.98s
walk_limited (depth=6):
	time: 2.34s
--------------------------------------------------
scandir_recursive (max depth):
	time: 3.85s
walk (max depth):
	time: 3.72s
```
os.listdir is so much faster since it doesn't do any os.stat calls at all and exclusively returns the names, but even in large directories the difference in speed is barely noticible plus it give almost no info.

After that, scandir_recursive and the common implementation of the os.walk for leveled recursiveness are quite hand in hand in terms of speed and again os.walk returns less item information than scandir_recursive and would need extra os.stat calls to be on par.

Also for comparison timing the command ls with max recursiveness
```
time sudo ls -AR "/" > /dev/null
```

```
real	0m2.130s
user	0m1.243s
sys	0m0.748s
```

Dependencies
------------
* Python (`>=3.5`)
