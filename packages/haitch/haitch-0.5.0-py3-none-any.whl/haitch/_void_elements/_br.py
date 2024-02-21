from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._void_elements._void_element import VoidElement

BrElement = NewType("BrElement", VoidElement)
"""A `<br>` element."""


def br(
    *,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> BrElement:
    """Produces a line break in text (carriage-return).

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/br>
    """
    el = VoidElement("br")(**attrs, **extra_attrs)
    return BrElement(el)
