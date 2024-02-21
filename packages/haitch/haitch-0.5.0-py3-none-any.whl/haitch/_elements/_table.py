from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

TableElement = NewType("TableElement", Element)
"""A `<table>` element."""


def table(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> TableElement:
    """Represents tabular data.

    Following elements are part of the table structure:
        - `<caption>`
        - `<thead>`
        - `<colgroup>`
        - `<col>`
        - `<th>`
        - `<tbody>`
        - `<tr>`
        - `<td>`
        - `<tfoot>`

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table>
    """
    el = Element("table")(**attrs, **extra_attrs)(*children)
    return TableElement(el)
