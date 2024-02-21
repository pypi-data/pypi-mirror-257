from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

H1Element = NewType("H1Element", Element)
"""A `<h1>` element."""


def h1(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> H1Element:
    """Represents first level section heading.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements>
    """
    el = Element("h1")(**attrs, **extra_attrs)(*children)
    return H1Element(el)
