from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

NoscriptElement = NewType("NoscriptElement", Element)
"""A `<noscript>` element."""


def noscript(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> NoscriptElement:
    """Defines HTML to be inserted if a script type on the page is unsupported.

    This can occur if scripting is turned off in the browser.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/noscript>
    """
    el = Element("noscript")(**attrs, **extra_attrs)(*children)
    return NoscriptElement(el)
