from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

HeadElement = NewType("HeadElement", Element)
"""A `<head>` element."""


def head(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> HeadElement:
    """Contains metadata about the document, like title, scripts, and style sheets.

    Note: <head> primarily holds information for machine processing, not
    human-readability. For human-visible information, like top-level headings
    and listed authors, see the <header> element.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/head>
    """
    el = Element("head")(**attrs, **extra_attrs)(*children)
    return HeadElement(el)
