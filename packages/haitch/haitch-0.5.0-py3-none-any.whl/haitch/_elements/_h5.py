from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

H5Element = NewType("H5Element", Element)
"""A `<h5>` element."""


def h5(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> H5Element:
    """Represents fifth level section heading.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements>
    """
    el = Element("h5")(**attrs, **extra_attrs)(*children)
    return H5Element(el)
