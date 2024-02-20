nobar

- Why make a new progress bar?
- To have the right one! Pythonic, plain, which can be used)

Quick start:

pip install nobar

Examples:

```
from nobar import nobar

# With init. You'll see itetations and time left

nobar('task_1', 3000)
for i in range(3000):
    nobar('task_1')
    sleep(0.02)
    
>>> task_1  127 of 3000    passed : 00:00:21    left: 00:08:27    avg: 00:00:00.169

# Without init. Only Passed 

for i in range(3000):
    nobar('task_2')
    sleep(0.02)
    
>>> task_2  150 of n/a    passed : 00:00:13    left: n/a    avg: 00:00:00.088

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

