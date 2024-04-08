"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Path setup --------------------------------------------------------------
import os
import shutil
import sys
from pathlib import Path
from ablog.commands import find_confdir, read_conf

sys.path.append(str(Path(".").resolve()))

# -- Project information -----------------------------------------------------

project = "hellhound ©"
copyright = "2024, Jean-Pierre Chauvel"
author = "Jean-Pierre Chauvel"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinx_copybutton",
    # custom extentions
    "_extensions.gallery_directive",
    # For extension examples and demos
    "myst_parser",
    "ablog",
    "sphinxcontrib.youtube",
    "sphinx_togglebutton",
    "sphinx_sitemap",
    "jupyterlite_sphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_website",
    "build",
    "Thumbs.db",
    ".DS_Store",
    "__pychache__",
    "README.md",
    "LICENSE.md",
    "giscus.json",
    "poetry.lock",
    "pyproject.toml",
    "requirements.txt",
    "environment.yaml",
    "notebooks",
]

# -- MyST options ------------------------------------------------------------

# This allows us to use ::: to denote directives, useful for admonitions
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
myst_heading_anchors = 2
myst_substitutions = {"rtd": "[Read the Docs](https://readthedocs.org/)"}

# -- Internationalization ----------------------------------------------------

# specifying the natural language populates some key tags
language = "en"

# -- Ablog options -----------------------------------------------------------

blog_path = "blog"
blog_authors = {
    "hellhound": ("Jean-Pierre Chauvel", "https://github.com/jpchauvel"),
}

# -- Options for HTML output -------------------------------------------------

html_title = ""
html_theme = "pydata_sphinx_theme"
html_logo = "_static/logo/hellhound.gif"
html_favicon = "_static/favicon/favicon-48x48.gif"
html_sourcelink_suffix = ""
html_last_updated_fmt = ""  # to reveal the build date in the pages meta

html_theme_options = {
    "header_links_before_dropdown": 4,
    "icon_links": [
        {
            "name": "Twitter",
            "url": "https://twitter.com/hellhoundorf",
            "icon": "fa-brands fa-twitter",
        },
        {
            "name": "WhatsApp",
            "url": "https://wa.me/+51989804478",
            "icon": "fa-brands fa-whatsapp",
        },
        {
            "name": "LinkedIn",
            "url": "https://linkedin.com/in/jpchauvel",
            "icon": "fa-brands fa-linkedin",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/jpchauvel",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Python Perú",
            "url": "https://blog.python.pe",
            "icon": "fa-brands fa-python",
        },
    ],
    "use_edit_page_button": False,
    "show_toc_level": 1,
    "navbar_align": "left",
    "navbar_center": ["navbar-nav"],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "secondary_sidebar_items": {
        "**/*": ["page-toc", "sourcelink"],
        "examples/no-sidebar": [],
    },
    "article_footer_items": ["giscus.html"],
}

html_sidebars = {
    "about": [
        "ablog/categories.html",
        "ablog/tagcloud.html",
        "ablog/archives.html"
    ],
    "blog": [
        "ablog/categories.html",
        "ablog/tagcloud.html",
        "ablog/archives.html"
    ],
    "blog/**": [
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/archives.html"
    ],
}

html_context = {
    "github_user": "jpchauvel",
    "github_repo": "chauvel.org",
    "github_version": "gh-pages",
    "doc_path": "blog",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
todo_include_todos = True


# -- Options for autosummary/autodoc output -----------------------------------
autosummary_generate = True
autodoc_typehints = "description"
autodoc_member_order = "groupwise"

# -- Options for sitemap ------------------------------------------------------
html_baseurl = "https://www.chauvel.org/"
sitemap_url_scheme = "{link}"
sitemap_locales = [None]

# -- Custom Sphinx app setup to hook after the build is finished --------------


def setup(app):
    app.connect('builder-inited', build_inited_handler)
    app.connect('build-finished', build_finsihed_handler)


def build_inited_handler(app):
    confdir = find_confdir()
    conf = read_conf(confdir)
    website = os.path.join(
        confdir, getattr(conf, "ablog_builddir", "_website")
    )
    blog = os.path.join(website, getattr(conf, "ablog_path", "blog"))
    lite = os.path.join(blog, "lite")
    shutil.rmtree(lite, ignore_errors=True)


def build_finsihed_handler(app, exception):
    confdir = find_confdir()
    conf = read_conf(confdir)
    website = os.path.join(
        confdir, getattr(conf, "ablog_builddir", "_website")
    )
    blog = os.path.join(website, getattr(conf, "ablog_path", "blog"))
    lite = os.path.join(website, "lite")
    shutil.copytree(lite, os.path.join(blog, "lite"))
