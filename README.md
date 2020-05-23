# scandirRecursive
A os.scandir implementation that supports recursiveness aswell as a maximum threshold depth in the recursiveness.
Faster than the os.walk and os.listdir functions, both for no recursiveness, recursiveness and max recursiveness.

It doesn't follow symbolic links, returns a list of directories and a list of files (both ordered alphabetically and case-insensitively), can return the lists in absolutepaths (the default) or in basenames (considering removing this since you can always do it yourself if you want it).

Calling the script from terminal deploys a command utility much like the command "ls". Mainly for testing since its obviously worse as a command.

Benchmarks
----------
When running the benchmark that compares the os.walk method with this recursive scandir method, both starting from the root directory, the results are:
```
scandir_recursive (depth=2):
	time: 0.0558934211730957s
walk_limited (depth=2):
	time: 9.656803607940674s
scandir_recursive (max depth):
	time: 8.259679794311523s
walk_limited (max depth):
  not actually timed because it takes so long
```

Also for comparison timing the command ls
```
time sudo ls -AR "/" > /dev/null
```
First time calling it
```
real	0m7.487s
user	0m1.630s
sys	0m1.541s
```
But in subsequent calls
```
real	0m5.131s
user	0m1.946s
sys	0m1.566s
```
This last result also seems consistent.

Dependencies
------------
* Python (`>=3.5`)
