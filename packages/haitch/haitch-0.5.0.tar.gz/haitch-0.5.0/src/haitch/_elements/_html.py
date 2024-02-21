from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

HtmlElement = NewType("HtmlElement", Element)
"""A `<html>` element."""


def html(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> HtmlElement:
    """Represents the root of an HTML document, also referred to as root element.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/html>
    """
    el = Element("html")(**attrs, **extra_attrs)(*children)
    return HtmlElement(el)
