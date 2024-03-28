# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Hellhound's Blog"
copyright = "2024, Jean-Pierre Chauvel"
author = "Jean-Pierre Chauvel"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

root_doc = "index"

html_title = "hellhound ©"

html_favicon = "favicon-48x48.gif"

html_logo = "hellhound.gif"

extensions = [
    "myst_parser",
    "sphinx_tags",
    "sphinx_design",
]

templates_path = ["_templates"]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

# -- Options for Sphinx Tags -------------------------------------------------
# https://sphinx-tags.readthedocs.io/en/latest/configuration.html

tags_create_tags = True

tags_extension = ["md"]

tags_page_header = ""

tags_index_head = ""

tags_page_title = "Tag"

tags_create_badges = True

tags_badge_colors = {
    "python": "success",
    "*": "primary",
}
