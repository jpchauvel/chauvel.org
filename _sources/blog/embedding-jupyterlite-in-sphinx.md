---
blogpost: true
date: 08 Apr, 2024
author: hellhound
location: Lima, Perú
category: JupyterLite
tags: jupyterlite, sphinx
language: English
---

# Exploring JupyterLite and Embedding it in Your Sphinx Blog

![JupyterLite](/_static/images/jupyterlite.png){ height=300px align=center }

## Introduction

As a developer and data enthusiast, I always find myself exploring new
technologies and tools to enhance my projects and documentation. Recently, my
curiosity led me to discover JupyterLite, a lightweight implementation of
JupyterLab that runs entirely in the browser without the need for a server.
Intrigued by its capabilities, I decided to experiment with embedding
JupyterLite in my Sphinx blog using the jupyterlite-sphinx extension. In this
post, I will share my journey of integrating JupyterLite into my documentation
and the steps I took to make it work seamlessly with my Sphinx-built blog.

## Installation and Setup

The first step to integrating JupyterLite into your Sphinx documentation is to
install the `jupyterlite-sphinx` package. You can do this easily using pip:

```sh
pip install jupyterlite-sphinx
```

After installing the extension, you need to add it to the extensions list in
your Sphinx project's `conf.py` file:

```sh
extensions = [
    'jupyterlite_sphinx',
    # Other Sphinx extensions
    # ...
]
```

Once you have added the extension, JupyterLite should automatically show up in
your online documentation. To preview it locally, you can navigate to the build
directory (e.g., `_build/html`) and use Python's built-in HTTP server to serve
the site:

```sh
python -m http.server
```

By default, jupyterlite-sphinx does not install a Python kernel. If you want to
have a Python kernel available in your documentation, you can install either
`jupyterlite-pyodide-kernel` or `jupyterlite-xeus` with pip:

```sh
pip install jupyterlite-pyodide-kernel
```

## Configuration

JupyterLite-sphinx provides several configuration options that allow you to
customize how JupyterLite behaves in your documentation. You can embed custom
content, such as notebooks and data files, in your JupyterLite build by
specifying the `jupyterlite_contents` variable in your `conf.py` file:

```python
jupyterlite_contents = ["./path/to/my/notebooks/", "my_other_notebook.ipynb"]
```

If you want to change the default build directory from the `docs` directory,
you can specify a custom directory using the `jupyterlite_dir` variable:

```python
jupyterlite_dir = "/path/to/your/lite/dir"
```

To pre-install Python packages in the kernel environment, you can use
`jupyterlite-pyodide` with the `pyodide-python` kernel. You can define the
dependencies in an `environment.yml` file in your docs directory:

```yaml
name: pyodide-python-kernel
channels:
  - https://repo.mamba.pm/emscripten-forge
  - https://repo.mamba.pm/conda-forge
dependencies:
  - numpy
  - matplotlib
  - ipycanvas
```

Additionally, jupyterlite-sphinx provides a `replite` Sphinx directive that
allows you to embed a REPLite console in your documentation. This directive
accepts various options, including the kernel type, height, prompt text, and
prompt color:

```rst
.. replite::
   :kernel: python
   :height: 600px
   :prompt: Try Replite!
   :prompt_color: #dc3545

   import matplotlib.pyplot as plt
   import numpy as np

   x = np.linspace(0, 2 * np.pi, 200)
   y = np.sin(x)

   fig, ax = plt.subplots()
   ax.plot(x, y)
   plt.show()
```

## Try it out!

Enter some Python code and then press Shift + Enter.

```{replite}
---
kernel: python
height: 600px
prompt: Try Replite!
prompt_color: #dc3545
---
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
```

## Conclusion

In conclusion, experimenting with JupyterLite and embedding it in my Sphinx blog
using the jupyterlite-sphinx extension has been a rewarding experience.
The ability to seamlessly integrate interactive Jupyter notebooks and REPL
consoles into my documentation has added a new level of interactivity and
engagement for my readers. By following the installation steps and configuration
options provided by jupyterlite-sphinx, it is easy to enhance your Sphinx-built
blog with JupyterLite features. I look forward to further exploring the
possibilities that JupyterLite opens up for creating dynamic and interactive
documentation experiences.
