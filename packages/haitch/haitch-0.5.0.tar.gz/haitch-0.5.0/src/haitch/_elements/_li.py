from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import NotRequired, Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

LiElement = NewType("LiElement", Element)
"""A `<li>` element."""


def li(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[LiAttrs],
) -> LiElement:
    """Represents an ordered list of items, typically rendered as a blileted list.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/li>
    """
    el = Element("li")(**attrs, **extra_attrs)(*children)
    return LiElement(el)


class LiAttrs(GlobalAttrs):
    """Attributes for the `<li>` element.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/li>
    """

    value: NotRequired[int]
    """Indicates the current ordinal value of the list item as defined by the `<ol>` element.

    The only allowed value for this attribute is a number, even if the list is displayed
    with Roman numerals or letters. List items that follow this one continue numbering
    from the value set. The value attribute has no meaning for unordered lists (`<ul>`)
    or for menus (`<menu>`).

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/li#value>
    """
