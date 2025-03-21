Hellhound's Blog
================

To build, install `uv`, follow the instructions in their documentation
https://docs.astral.sh/uv/getting-started/installation/, `uv` will handle all
the dependencies and the python installation as well. So we don't need to
install `python` separately.

Then install all the necessary packages (make sure to change to the root
directory of the project):

```sh
uv sync
```

And then, you can build the html files of the blog by running the following
command:

```sh
uv run ablog build
```

Then you can serve the files locally using this command:

```sh
uv run ablog serve
```
