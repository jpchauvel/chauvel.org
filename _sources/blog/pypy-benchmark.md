---
blogpost: true
date: 13 May, 2024
author: hellhound
location: Lima, Perú
category: PyPy
tags: python, pypy, cpython, numba
language: English
---

# Exploring Python Performance: PyPy vs CPython vs Numba

Python developers often face the decision of choosing between different
implementations for their projects, especially when performance is a crucial
factor. In this blog post, we delve into a comparative benchmarking study
between PyPy, CPython, and Numba, focusing on calculating Pi value using a
custom script.

## Introduction

The benchmarking setup involved running the same Python script on PyPy 7.3.16
with Python 3.10.14, CPython 3.12.3, and Numba 0.59.1 on a Macbook Pro M1 Max
with 10 cores and 64GB of RAM.

## Performance Results

```{note}
Repository https://github.com/jpchauvel/pypy-test
```

### PyPy Performance
- Pi value obtained: 3.1420208
- Elapsed time: 2.2179 seconds

PyPy demonstrated decent performance in calculating Pi but was slightly slower
compared to CPython and Numba.

### CPython/Numba Performance
- Pi value obtained: 3.14182408
- Elapsed time: 0.5820 seconds

CPython with Numba outperformed PyPy in both accuracy and speed, presenting the
most efficient solution among the three test cases.


## Final Thoughts

While PyPy offers a balance between performance and Python compatibility, its
execution time in this benchmark was marginally slower than CPython. For tasks
prioritizing speed, CPython emerges as the preferred choice. Numba, leveraging
JIT compilation, was noted as a potential contender for performance-critical
applications.

In conclusion, the choice between PyPy, CPython, and Numba depends on the
specific requirements of the project, with developers considering factors such
as execution speed, accuracy, and compatibility with Python libraries.
