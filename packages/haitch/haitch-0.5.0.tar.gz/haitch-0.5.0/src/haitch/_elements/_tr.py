from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

TrElement = NewType("TrElement", Element)
"""A `<tr>` element."""


def tr(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> TrElement:
    """Defines a row of cells in a table.

    The row's cells can then be established using a mix of `<td>` (data cell) and
    `<th>` (header cell) elements.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tr>
    """
    el = Element("tr")(**attrs, **extra_attrs)(*children)
    return TrElement(el)
