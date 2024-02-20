nobar

- Why make a new progress bar?
- To have the right one! Pythonic, plain, which can be used)

Quick start:

pip install nobar

Examples:

```
from nobar import nobar
from time import sleep

# With init. You'll see itetations and time left

nobar('task_1', 50)
for i in range(50):
    sleep(0.8)
    nobar('task_1')
    
>>> task_1   50 / 50   pas 00:00:46   lef 00:00:00   tot 00:00:46   las 0.801   avg 0.922



# Without init. Only Passed 

for i in range(800):
    sleep(0.02)
    nobar('task_2')
    
>>> task_2   800 / ---   pas 00:00:16   lef --:--:--   tot --:--:--   las 0.020   avg 0.020



# Previous data saved

nobar(print_all=True)

>>> task_1   50 / 50   pas 00:00:46   lef 00:00:00   tot 00:00:46   las 0.801   avg 0.922
>>> task_2   800 / ---   pas 00:00:16   lef --:--:--   tot --:--:--   las 0.020   avg 0.020
```

