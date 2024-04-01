---
blogpost: true
date: Mar 29, 2024
author: Jean-Pierre Chauvel
location: Lima, Perú
category: Python
tags: python, numba
language: English
---
# Calculating π with Numba

Here is a version of the calculation of π using numba. Numba does just-in-time compilation from Python code and also supports parallelism. I was able to test `calculate_pi()` in the order of billions of iteretions and without consuming too much memory.

```python
#!/usr/bin/env python3
import argparse
import random

from numba import njit, prange
import numpy as np

@njit(parallel=True)
def calculate_pi(n: int) -> float:
    result = np.zeros(n)
    for i in prange(n):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        distance = x ** 2 + y ** 2

        if distance <= 1:
            result[i] = 1
    return result.sum() * 4 / n

if __name__ = "__main__":
    parser = argparse.ArgumentParser(description="Calculate п.")
    parser.add_argument(
        "iteration", metavar="n", type=int, help="number of iterations"
    )
    args = parser.parse_args()
    n = args.iteration
    print(calculate_pi(n))
```

**Note:** This calculation method is described in this Wikipedia article https://en.wikipedia.org/wiki/Approximations_of_π#Summing_a_circle's_area.

```{raw} html
---
file: ../../_templates/giscus.html
---
```
