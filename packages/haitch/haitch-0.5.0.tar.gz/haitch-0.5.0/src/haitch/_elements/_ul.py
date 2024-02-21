from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

UlElement = NewType("UlElement", Element)
"""A `<ul>` element."""


def ul(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> UlElement:
    """Represents an unordered list of items, typically rendered as a bulleted list.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul>
    """
    el = Element("ul")(**attrs, **extra_attrs)(*children)
    return UlElement(el)
