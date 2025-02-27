"""A directive to generate an image tag with a Gravatar pic.
"""

from typing import Any, Callable

from docutils import nodes
from docutils.parsers.rst import Directive
from jinja2 import BaseLoader, Environment, Template
from libgravatar import Gravatar
from sphinx.application import Sphinx
from sphinx.util import logging

logger: logging.SphinxLoggerAdapter = logging.getLogger(__name__)

GRAVATAR_TEMPLATE: str = """
<div class="{{ klass }}">
    <img src={{ url }}
    {% if align %} align="{{ align }}"{% endif %}
    {% if klass %} class="{{ klass }}"{% endif %}
    {% if style %} style="{{ style }}"{% endif %}
    {% if width %} width="{{ width }}" height="{{ width }}"{% endif %}>
</div>
"""


class GravatarImage(Directive):
    has_content = True
    final_argument_whitespace = False
    option_spec: dict[str, Callable[[str], Any]] = {
        "align": lambda a: a.strip(),
        "class": lambda a: a.strip(),
        "style": lambda a: a.strip(),
        "width": lambda a: a.strip(),
    }

    def run(self) -> list[nodes.raw]:
        email: str = self.content[0]
        align: str | None = self.options.get("align")
        klass: str | None = self.options.get("class")
        style: str | None = self.options.get("style")
        width: str | None = self.options.get("width")

        logger.info(f"Getting Gravatar image for email: {email}")
        url: str = Gravatar(email).get_image()
        if width is not None:
            url = f"{url}?s={width}"
        logger.info(f"Got image URL: {url}")

        template: Template = Environment(
            loader=BaseLoader, trim_blocks=True, lstrip_blocks=True
        ).from_string(GRAVATAR_TEMPLATE)

        out: str = template.render(
            url=url,
            align=align,
            klass=klass,
            style=style,
            width=width,
        )
        # User a raw pass-through node
        para: nodes.raw = nodes.raw("", out, format="html")
        return [para]


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_directive("gravatar", GravatarImage)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
