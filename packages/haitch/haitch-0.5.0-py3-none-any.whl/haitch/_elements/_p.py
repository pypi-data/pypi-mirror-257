from __future__ import annotations

from typing import Mapping, NewType

from typing_extensions import Unpack

from haitch._attrs import AttributeValue, GlobalAttrs
from haitch._elements._element import Child, Element

ParagraphElement = NewType("ParagraphElement", Element)
"""A `<p>` element."""


def p(
    *children: Child,
    extra_attrs: Mapping[str, AttributeValue] = {},
    **attrs: Unpack[GlobalAttrs],
) -> ParagraphElement:
    """Represents a paragraph.

    Paragraphs are usually represented in visual media as blocks of text separated
    from adjacent blocks by blank lines and/or first-line indentation, but HTML
    paragraphs can be any structural grouping of related content, such as images
    or form fields.

    Paragraphs are block-level elements, and notably will automatically close if
    another block-level element is parsed before the closing </p> tag.

    <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/p>
    """
    el = Element("p")(**attrs, **extra_attrs)(*children)
    return ParagraphElement(el)
