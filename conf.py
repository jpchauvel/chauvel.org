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
import subprocess
from typing import Any

from ablog.commands import find_confdir, read_conf

sys.path.append(str(Path(".").resolve()))

# -- Project information -----------------------------------------------------

project: str = "hellhound ©"
copyright: str = "2024, Jean-Pierre Chauvel"
author: str = "Jean-Pierre Chauvel"

# -- General configuration ---------------------------------------------------

extensions: list[str] = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinx_copybutton",
    "myst_parser",
    "ablog",
    "sphinxcontrib.youtube",
    "sphinx_togglebutton",
    "sphinx_sitemap",
    "sphinx_favicon",
    "sphinxext.opengraph",
    "jupyterlite_sphinx",
    # custom extentions
    "_extensions.gallery_directive",
    "_extensions.gravatar",
]

# Add any paths that contain templates here, relative to this directory.
templates_path: list[str] = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = [
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
    "pyodide-chat-gpt",
]

# -- MyST options ------------------------------------------------------------

# This allows us to use ::: to denote directives, useful for admonitions
myst_enable_extensions: list[str] = [
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
myst_heading_anchors: int = 2
myst_substitutions: dict[str, str] = {
    "rtd": "[Read the Docs](https://readthedocs.org/)"
}

# -- Internationalization ----------------------------------------------------

# specifying the natural language populates some key tags
language: str = "en"

# -- Ablog options -----------------------------------------------------------

blog_title: str = "hellhound ©"
blog_path: str = "blog"
blog_authors: dict[str, tuple[str, str]] = {
    "hellhound": ("Jean-Pierre Chauvel", "https://github.com/jpchauvel"),
}
blog_baseurl: str = "https://www.chauvel.org"
blog_feed_fulltext: bool = True
blog_feed_subtitle: str = (
    "This blog is dedicated to tech stuff,"
    " more specifically: Python related stuff."
)
fontawesome_included: bool = True
post_redirect_refresh: int = 1

# -- Options for HTML output -------------------------------------------------

html_title: str = ""
html_theme: str = "pydata_sphinx_theme"
html_logo: str = "_static/logo/hellhound.gif"
# html_favicon = "_static/favicon/favicon-48x48.gif"
html_sourcelink_suffix: str = ""
html_last_updated_fmt: str = ""  # to reveal the build date in the pages meta

html_theme_options: dict[str, Any] = {
    "header_links_before_dropdown": 4,
    "icon_links": [
        {
            "name": "Twitter",
            "url": "https://twitter.com/hellhoundorf",
            "icon": "fa-brands fa-x-twitter",
        },
        {
            "name": "Instagram",
            "url": "https://www.instagram.com/hellhoundorf",
            "icon": "fa-brands fa-instagram",
        },
        {
            "name": "YouTube",
            "url": "https://youtube.com/@hellhoundorf",
            "icon": "fa-brands fa-youtube",
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
            "name": "Stack Overflow",
            "url": "https://stackoverflow.com/users/434423/jean-pierre-chauvel",
            "icon": "fa-brands fa-stack-overflow",
        },
        {
            "name": "Fiverr",
            "url": "https://www.fiverr.com/s/2K0Wmwk",
            "icon": "https://fiverr-res.cloudinary.com/npm-assets/layout-service/favicon-32x32.8f21439.png",
            "type": "url",
        },
        {
            "name": "Python Perú",
            "url": "https://python.pe",
            "icon": "fa-brands fa-python",
        },
        {
            "name": "Blog RSS feed",
            "url": "https://www.chauvel.org/blog/atom.xml",
            "icon": "fa-solid fa-rss",
        },
    ],
    "use_edit_page_button": False,
    "show_toc_level": 1,
    "navbar_align": "left",
    "navbar_center": ["navbar-nav"],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "navigation_with_keys": True,
    "secondary_sidebar_items": {
        "**/*": ["page-toc", "sourcelink"],
        "examples/no-sidebar": [],
    },
    "article_footer_items": ["giscus.html"],
    "analytics": {
        "google_analytics_id": "G-F0WV9RGJW0",
    },
}

html_sidebars: dict[str, list[str]] = {
    "about": ["about.html"],
    "blog": [
        "ablog/categories.html",
        "ablog/tagcloud.html",
        "ablog/archives.html",
    ],
    "blog/**": [
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/archives.html",
    ],
}

html_context: dict[str, str] = {
    "github_user": "jpchauvel",
    "github_repo": "chauvel.org",
    "github_version": "gh-pages",
    "doc_path": "blog",
    "email": "jean.pierre@chauvel.org",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: list[str] = ["_static"]
todo_include_todos: bool = True
html_extra_path: list[str] = ["_extra"]
custom_css: str = "css/custom.css"


# -- Options for autosummary/autodoc output -----------------------------------
autosummary_generate: bool = True
autodoc_typehints: str = "description"
autodoc_member_order: str = "groupwise"

# -- Options for sitemap ------------------------------------------------------
html_baseurl: str = "https://www.chauvel.org/"
sitemap_url_scheme: str = "{link}"
sitemap_locales: list[None] = [None]

# -- Options for favicon ------------------------------------------------------
favicons: list[dict[str, str]] = [
    {"href": "favicon/favicon-16x16.gif"},
    {"href": "favicon/favicon-32x32.gif"},
    {"href": "favicon/favicon-48x48.gif"},
    {"rel": "apple-touch-icon", "href": "favicon/favicon-180x180.gif"},
]

# -- Options for OpenGraph ----------------------------------------------------

ogp_site_url: str = "https://www.chauvel.org"
ogp_enable_meta_description: bool = True
ogp_social_cards: dict[str, str] = {
    "line_color": "#4078c0",
    "image": "_static/logo/hellhound-profile.gif",
}

# -- Options for Jupyterlite-Sphinx -------------------------------------------

# Build-time configuration for JupyterLite
jupyterlite_config = "jupyter_lite_config.json"

# -- Custom Sphinx app setup to hook after the build is finished --------------


def setup(app) -> None:
    app.connect("builder-inited", build_inited_handler)
    app.connect("build-finished", build_finsihed_handler)
    app.add_css_file(custom_css)


def build_inited_handler(app) -> None:
    confdir: Any | str = find_confdir()
    conf = read_conf(confdir)
    website: str = os.path.join(
        confdir, getattr(conf, "ablog_builddir", "_website")
    )
    blog: str = os.path.join(website, getattr(conf, "ablog_path", "blog"))
    lite: str = os.path.join(blog, "lite")
    pyodide_chat_gpt_in_blog: str = os.path.join(blog, "pyodide-chat-gpt")
    pyodide_chat_gpt: str = os.path.join(confdir, "pyodide-chat-gpt")

    # Remove the lite directory
    shutil.rmtree(lite, ignore_errors=True)

    # Remove the pyodide-chat-gpt directory
    shutil.rmtree(pyodide_chat_gpt_in_blog, ignore_errors=True)

    # Build pyodide-chat-gpt
    subprocess.run(["make", "-C", pyodide_chat_gpt, "all"], check=True)


def build_finsihed_handler(app, exception) -> None:
    confdir: Any | str = find_confdir()
    conf = read_conf(confdir)
    website = os.path.join(
        confdir, getattr(conf, "ablog_builddir", "_website")
    )
    blog = os.path.join(website, getattr(conf, "ablog_path", "blog"))
    lite = os.path.join(website, "lite")
    pyodide_chat_gpt: str = os.path.join(confdir, "pyodide-chat-gpt", "build")

    # Move the lite directory
    shutil.copytree(lite, os.path.join(blog, "lite"), dirs_exist_ok=True)

    # Move the pyodide-chat-gpt directory
    shutil.copytree(
        pyodide_chat_gpt,
        os.path.join(blog, "pyodide-chat-gpt"),
        dirs_exist_ok=True,
    )
