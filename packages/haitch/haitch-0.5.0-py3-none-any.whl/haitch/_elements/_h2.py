from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

H2Element = NewType("H2Element", Element)
"""A `<h2>` element."""


def h2(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> H2Element:
    """Represents second level section heading.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements>
    """
    el = Element("h2")(**attrs, **extra_attrs)(*children)
    return H2Element(el)
