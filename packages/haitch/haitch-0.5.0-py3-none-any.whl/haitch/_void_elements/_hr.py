from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._void_elements._void_element import VoidElement

HrElement = NewType("HrElement", VoidElement)
"""An `<hr>` element."""


def hr(
    *,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> HrElement:
    """Represents a thematic break between paragraph-level elements.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/hr>
    """
    el = VoidElement("hr")(**attrs, **extra_attrs)
    return HrElement(el)
