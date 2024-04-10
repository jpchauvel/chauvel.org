"""A set of directives to generate an image tag with a Gravatar image and an
iframe with a Gravatar profile.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from jinja2 import BaseLoader, Environment
from libgravatar import Gravatar
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

GRAVATAR_IMAGE_TEMPLATE = """
<div class="{{ klass }}">
    <img src={{ url }}
    {% if align %} align="{{ align }}"{% endif %}
    {% if klass %} class="{{ klass }}"{% endif %}
    {% if style %} style="{{ style }}"{% endif %}
    {% if width %} width="{{ width }}"{% endif %}
    {% if height %} height="{{ height }}"{% endif %}>
</div>
"""

GRAVATAR_PROFILE_TEMPLATE = """
<iframe
    src="{{ url }}"
    width="{{ width }}"
    height="{{ height }}"
    frameborder="0"
    {% if klass %} class="{{ klass }}"{% endif %}
    {% if style %} style="{{ style }}"{% endif %}
</iframe>
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
        "height": lambda a: a.strip(),
    }

    def run(self):
        email = self.content[0]
        align = self.options.get("align")
        klass = self.options.get("class")
        style = self.options.get("style")
        width = self.options.get("width")
        height = self.options.get("height")

        logger.info(f"Getting Gravatar image for email: {email}")
        url = Gravatar(email).get_image()
        logger.info(f"Got image URL: {url}")

        template = Environment(
            loader=BaseLoader, trim_blocks=True, lstrip_blocks=True
        ).from_string(GRAVATAR_IMAGE_TEMPLATE)

        out = template.render(
            url=url,
            align=align,
            klass=klass,
            style=style,
            width=width,
            height=height,
        )
        # User a raw pass-through node
        para = nodes.raw("", out, format="html")
        return [para]


class GravatarProfile(Directive):
    arguments = 1
    has_content = True
    final_argument_whitespace = False
    option_spec = {
        "class": lambda a: a.strip(),
        "style": lambda a: a.strip(),
        "width": lambda a: a.strip(),
        "height": lambda a: a.strip(),
    }

    def run(self):
        email = self.content[0]
        klass = self.options.get("class")
        style = self.options.get("style")
        width = self.options.get("width", "200px")
        height = self.options.get("height", "200px")

        logger.info(f"Getting Gravatar profile for email: {email}")
        url = Gravatar(email).get_profile()
        logger.info(f"Got profile URL: {url}")

        template = Environment(
            loader=BaseLoader, trim_blocks=True, lstrip_blocks=True
        ).from_string(GRAVATAR_PROFILE_TEMPLATE)

        out = template.render(
            url=url,
            klass=klass,
            style=style,
            width=width,
            height=height,
        )
        # User a raw pass-through node
        para = nodes.raw("", out, format="html")
        return [para]


def setup(app: Sphinx):
    app.add_directive("gravatar-image", GravatarImage)
    app.add_directive("gravatar-profile", GravatarProfile)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
