from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._void_elements._void_element import VoidElement

WbrElement = NewType("WbrElement", VoidElement)
"""A `<wbr>` element."""


def wbr(
    *,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> WbrElement:
    """Represents a word break opportunity.

    This is a position within text where the browser may optionally break a line, though
    its line-breaking rules would not otherwise create a break at that location

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/wbr>
    """
    el = VoidElement("wbr")(**attrs, **extra_attrs)
    return WbrElement(el)
