# scandirRecursive
A os.scandir implementation that supports recursiveness aswell as a maximum threshold depth in the recursiveness.
Faster than os.listdir and os.walk (slightly at max depth)

It takes a path, a depth level int (where -1 means max) and a boolean value to return paths or basenames.

It doesn't follow symbolic links, returns a list of directories and a list of files (both ordered alphabetically and case-insensitively), can return the lists in absolutepaths (the default) or in basenames (considering removing this since you can always do it yourself if you want it).

Calling the script from terminal deploys a command utility much like the command "ls". Mainly for testing since its obviously worse as a command.

Benchmarks
----------
When running the benchmark that compares the os.walk method with this recursive scandir method, both starting from the root directory, the results are:
```
scandir_recursive (depth=0):
	time: 5.2e-05s
listdir (not recursive func):
	time: 0.00014s
--------------------------------------------------
scandir_recursive (depth=6):
	time: 1.46s
walk_limited (depth=6):
	time: 2.15s
--------------------------------------------------
scandir_recursive (max depth):
	time: 3.3s
walk (max depth):
	time: 3.44s
```

Also for comparison timing the command ls with max recursiveness
```
time sudo ls -AR "/" > /dev/null
```

```
real	0m1.997s
user	0m1.181s
sys	0m0.703s
```

Dependencies
------------
* Python (`>=3.5`)
