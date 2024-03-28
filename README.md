Hellhound's Blog
================

To build, make sure you have Python 3.12 installed. Then install `poetry`:

```sh
pip install -U poetry
```

Then install all the necessary packages (make sure to change to the root directory of the project):

```sh
poetry install
```

And then, you can build the html files of the blog by running the following commands:

```sh
poetry shell
make html
```

The built html files would be placed in the `build/html` subdirectory.
