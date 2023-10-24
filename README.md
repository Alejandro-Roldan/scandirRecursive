# scandirRecursive
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An os.scandir implementation that supports recursiveness aswell as a maximum threshold depth in the recursiveness.
More or less same speed as os.list and os.walk (a bit slower) but has the advantage that this scandir_recursive returns os.DirEntry objects, which is way faster if you intend to manipulate the tree further since you don't need to call os.stat again.
Also can filter the outputted entries by several fields.

- scandir_recursive(path, mask=re.compile(''), ext_tuple=\[\], folders=True, files=True, hidden=False, min_len=0, max_len=9999, depth=0, max_find_items=0): A scandir implementation that allows recursiveness by level and returns a generator object that extracts os.DirEntry objects. It doesn't follow symbolic links.
Depth starts at the maximum value and goes down by one in each function call until it reaches 0 where it doesn't call the function anymore.
Returns a list of os.DirEntry objects.
If the depth is -1 execute maximum recursiveness.
It takes a path, a depth level int (where -1 means max) and the optional filters:
	- mask: Filters the filenames with regular expressions. A str containing the regular expression to match.
	- exts: Filter by extension. Takes a list of extensions you want in the form \['mp3','jpg'\]
	- folders: Show folders but don't show files
	- files: Show files but don't show folders
	- hidden: Show and look inside hidden files and folders
	- min_len: Minimum filename length
	- max_len: Maximum filename length
	- depth: Maximum depth level to recursed
	- max_find_items: Maximum matches

*Usage examples*

Generator object _scandir_recursive
```python
tree = scandir_recursive(path, **kwargs)
```
List of os.DirEntry's
```python
tree_list = [item for item in scandir_recursive(path, **kwargs)]
```
Applying a function to each item at run time
```python
tree_foo = foo(item) for item in scandir_recursive(path, **kwargs)
```

## Work diagram for an example depth=1:
```
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
```

- tree_sort(tree, depth=-1, files_before_dirs=False): Sort the list tree that scandir_recursive outputs alphabetically and case-insensitively the absolute paths, this will produce having a folder followed by its contents. When the depth=0 sort files first then folders or folders first then files (the default). Takes the tree list and the optional arguments:
	- depth: default value of -1
	- files_before_dirs: Only avaible for depth=0. If active will show files before directories
    
- scandir_recursive_sorted(path, mask=re.compile(''), ext_tuple=[], folders=True, files=True, hidden=False, min_len=0, max_len=9999, depth=0, max_find_items=0, files_before_dirs=False): Calls the scandir_recursive and tree_sort functions one after the other. For easyness. Takes the combination of both functions arguments (except the tree argument from tree_sort since it takes the output of the scandir_recursive directly).

*Usage examples*

List of os.DirEntry's alphabetically ordered
```python
tree_sorted = scandir_recursive_sorted(path, **kwargs)
```

- main(): Calling the script from terminal deploys a command utility much like the command "ls". Mainly for testing and measure timing.

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
os.listdir is so much faster since it doesn't do any os.stat calls at all and exclusively returns the names, but even in large directories the difference in speed is barely noticeable plus it gives no info compared to scandir_recursive.

After that, scandir_recursive and the common implementation of the os.walk for leveled recursiveness are quite hand in hand in terms of speed and, again, os.walk returns less item information than scandir_recursive and would need extra os.stat calls to be on par.

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
