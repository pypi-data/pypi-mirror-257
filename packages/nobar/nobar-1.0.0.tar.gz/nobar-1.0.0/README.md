nobar

- Why make a new progress bar?
- To have the right one! Pythonic, plain, which can be used)

Quick start:

pip install nobar

Examples:

```
from nobar import nobar

# With init. You'll see left itetations and time
nobar('taskname', 3000)
for i in range(3000):
    nobar('taskname')
    sleep(0.02)

# Without init. Only Passed 
for i in range(3000):
    nobar('taskname')
    sleep(0.02)
    
# Mixed. Few bars simultaneously.
nobar('task_1',3000)
nobar('task_2')
for i in range(3000):
    nobar('task_1')
    if i%3 == 0:
        nobar('task_2')
    sleep(0.02)
```

More arguments in the class

