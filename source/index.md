[//]: # "Hellhound's Blog master file, created by sphinx-quickstart on Wed Mar 27 20:07:35 2024.
You can adapt this file completely to your liking, but it should at least contain the
root `toctree` directive."

hellhound ©
===========

```python
def main():
    print("Hi, my name is Jean-Pierre Chauvel and I'm a Software Engineer and Pythonista.")

    print("This blog is dedicated to tech stuff more specifically: Python related stuff.")


if __name__ == "__main__":
    main()
```

Recent posts:

```{postlist} 5
---
date: "%A, %B %d, %Y"
format: "{title} by {author} on {date}"
list-style: circle
excerpts:
sort:
expand: Read more ...
---
```

```{eval-rst}

.. toctree::
   :hidden:

   about.md
   blog.md

```
