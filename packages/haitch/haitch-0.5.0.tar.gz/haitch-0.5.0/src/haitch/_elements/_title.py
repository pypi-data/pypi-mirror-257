from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

TitleElement = NewType("TitleElement", Element)
"""A `<title>` element."""


def title(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> TitleElement:
    """Defines the document's title that is shown in a browser's title bar or page's tab.

    Note: it only contains text; tags within the element are ignored.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title>
    """
    el = Element("title")(**attrs, **extra_attrs)(*children)
    return TitleElement(el)
