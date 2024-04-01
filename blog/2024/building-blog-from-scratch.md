---
blogpost: true
date: Mar 29, 2024
author: Jean-Pierre Chauvel
location: Lima, Perú
category: Blog
tags: python, ablog, sphinx, giscus, github-pages, github-actions
language: English
---
# Building and Deploying a Blog with Sphinx, Ablog, and PyData Sphinx Theme

Python is not only a powerful tool for data analysis and backend development – it's also an excellent platform for content creators who want to share their ideas with the world. As a fellow Pythonista, I was determined to build a blog using Python-centric tools. That's when I discovered a fantastic trio: Sphinx, Ablog, and the PyData Sphinx Theme. Here’s how to build your blog with these tools and deploy it on GitHub Pages with the power of GitHub Actions.

## Crafting Your Blog

Let's run through the steps to create your blog's scaffolding and content, all with a Python flavor.

### Step 1: Install the Necessary Packages

First, verify that your environment has Python and `pip` installed. Then, proceed with installing Sphinx, Ablog, and the PyData Sphinx Theme:

```bash
pip install sphinx ablog sphinx-pydata-theme
```

### Step 2: Start Your Blog with Ablog

Instead of using `sphinx-quickstart`, Ablog provides its command to create a new blog project:

```bash
ablog start
```

This command will set up your blog with typical Sphinx configurations and Ablog presets.

### Step 3: Configure Your Blog with PyData Theme and Ablog

After the initial setup, personalize your blog settings in the `conf.py` file:

```python
# conf.py

extensions = [
    'ablog',
    'sphinx.ext.intersphinx',
    # Add any other Sphinx extensions here.
]

html_theme = 'pydata_sphinx_theme'

# Additional theme options are available on the theme's documentation.
html_theme_options = {
    "search_bar_text": "Search this site...",
    # More theme options
}

# Configure ablog
blog_baseurl = "https://[github-username].github.io/[repository-name]/"
blog_title = "My Pythonista Blog"
blog_authors = {
    "Your Nickname": ("Your Name", None),
}

# For generating a feed
blog_feed_archives = True
```

### Step 4: Writing Blog Posts

Create your posts in reStructuredText format within the posts section you set up:

```rst
.. post:: Sept 15, 2023
   :tags: python, sphinx, ablog
   :category: python
   :author: Your Name

Journey with Python
===================

Begin storytelling with Python…
```

Save it into the correct directory with an `.rst` extension and the Sphinx/Ablog combination will handle the rest.

## Enhancing Engagement: Adding Giscus Comments

Engage with your readers by adding a comment section using Giscus, a comment service that uses GitHub discussions, right into your Sphinx blog.

### Step 1: Configure Giscus on Your Blog

Giscus requires a specific configuration embedded into your blog. You can include this in your Sphinx HTML templates:

```html
<!-- In _templates/layout.html -->
{% extends "!layout.html" %}

{% block extrahead %}
<script src="https://giscus.app/client.js"
        data-repo="[YourGitHubUsername]/[YourRepoName]"
        data-repo-id="[RepoID]"
        data-category="[DiscussionCategory]"
        data-category-id="[DiscussionCategoryID]"
        data-mapping="pathname"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-theme="preferred_color_scheme"
        async>
</script>
{{ super() }}
{% endblock %}
```

Remember to replace placeholders with your repository details. You can get these from your Giscus configuration page.

You need other steps to enable Giscus. Refer to https://github.com/giscus/giscus?tab=readme-ov-file.

### Step 2: Deploy with GitHub Actions

Automatic deployment to GitHub Pages can be set up using a workflow in the `.github/workflows/blog.yml` file:

```yaml
name: Deploy Blog to GitHub Pages

on:
  push:
    branches:
      - main  # or your default branch name

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'  # Replace '3.x' with your preferred version
      
      - name: Install Dependencies
        run: |
          pip install sphinx ablog sphinx_pydata_theme
      
      - name: Build Blog
        run: ablog build
      
      - name: Publish to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_build/html
```

This workflow will build and deploy your blog to GitHub Pages whenever you push to the main branch.

```{raw} html
---
file: ../../_templates/giscus.html
---
```
