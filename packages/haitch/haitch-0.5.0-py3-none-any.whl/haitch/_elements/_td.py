from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

TdElement = NewType("TdElement", Element)
"""A `<td>` element."""


def td(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> TdElement:
    """Defines a cell of a table that contains data.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/td>
    """
    el = Element("td")(**attrs, **extra_attrs)(*children)
    return TdElement(el)
