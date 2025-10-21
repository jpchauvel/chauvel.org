---
blogpost: true
date: 10 Apr, 2024
author: hellhound
location: Lima, Perú
category: Gravatar
tags: gravatar, sphinx, directive
language: English
---

# Adding a Sphinx Directive to Render Your Gravatar Pic

![Gravatar](/_static/images/gravatar.png){ align=center width=200px }

I was having this idea of embedding my gravatar pic along the kind-of-corny text
that is located in the [about](../about.md) page. So, I decided to create a
Shpinx directive that allowed me to insert/embed into a Markdown file my
Gravatar pic.

I immediately dismissed the idea because it was better to do it using javascript
alone in a Sphinx template (as a matter of fact, the gravatar API is pretty
simple, you just have to append a SHA-256 hash of your email address linked to
your Gravatar account to this URL https://gravatar.com/avatar/{your_hash_here}).

The directive is called `{gravatar}`.

## Example

````markdown
```{gravatar} jean.pierre@chauvel.org
---
align: center
class: something
style: "border-radius: 200px; margin: 0 auto; display: block;"
width: 200
---
```
````

```{gravatar} jean.pierre@chauvel.org
---
align: center
class: something
style: "border-radius: 200px; margin: 0 auto; display: block;"
width: 200
---
```

## Source Code

```python
"""A directive to generate an image tag with a Gravatar pic.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from jinja2 import BaseLoader, Environment
from libgravatar import Gravatar
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

GRAVATAR_TEMPLATE = """
<div class="{{ klass }}">
    <img src={{ url }}
    {% if align %} align="{{ align }}"{% endif %}
    {% if klass %} class="{{ klass }}"{% endif %}
    {% if style %} style="{{ style }}"{% endif %}
    {% if width %} width="{{ width }}" height="{{ width }}"{% endif %}>
</div>
"""


class GravatarImage(Directive):
    arguments = 1
    has_content = True
    final_argument_whitespace = False
    option_spec = {
        "align": lambda a: a.strip(),
        "class": lambda a: a.strip(),
        "style": lambda a: a.strip(),
        "width": lambda a: a.strip(),
    }

    def run(self):
        email = self.content[0]
        align = self.options.get("align")
        klass = self.options.get("class")
        style = self.options.get("style")
        width = self.options.get("width")

        logger.info(f"Getting Gravatar image for email: {email}")
        url = Gravatar(email).get_image()
        if width is not None:
            url = f"{url}?s={width}"
        logger.info(f"Got image URL: {url}")

        template = Environment(
            loader=BaseLoader, trim_blocks=True, lstrip_blocks=True
        ).from_string(GRAVATAR_TEMPLATE)

        out = template.render(
            url=url,
            align=align,
            klass=klass,
            style=style,
            width=width,
        )
        # User a raw pass-through node
        para = nodes.raw("", out, format="html")
        return [para]


def setup(app: Sphinx):
    app.add_directive("gravatar", GravatarImage)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
```
