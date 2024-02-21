from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

PreElement = NewType("PreElement", Element)
"""A `<pre>` element."""


def pre(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> PreElement:
    """Represents preformatted text presented exactly as written in the HTML file.

    The text is typically rendered using a non-proportional, or monospaced, font.
    Whitespace inside this element is displayed as written.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/pre>
    """
    el = Element("pre")(**attrs, **extra_attrs)(*children)
    return PreElement(el)
