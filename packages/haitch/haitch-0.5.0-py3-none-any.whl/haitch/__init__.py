"""
haitch - a lazy HTML element builder.
=====================================

Import any element you like from the root module:

>>> import haitch as H

Lazily build a dom tree by passing children and/or attributes to the
`__init__` and/or `__call__` methods:

>>> dom = H.a(href="https://example.com")("Check out my website")

In order render the object to HTML, you need to invoke the `__str__` method:

>>> str(dom)
'<a href="https://example.com">Check out my website</a>'
"""

from haitch._elements._a import AnchorElement, a
from haitch._elements._body import BodyElement, body
from haitch._elements._div import DivElement, div
from haitch._elements._element import Element, fragment
from haitch._elements._h1 import H1Element, h1
from haitch._elements._h2 import H2Element, h2
from haitch._elements._h3 import H3Element, h3
from haitch._elements._h4 import H4Element, h4
from haitch._elements._h5 import H5Element, h5
from haitch._elements._h6 import H6Element, h6
from haitch._elements._head import HeadElement, head
from haitch._elements._html import HtmlElement, html
from haitch._elements._li import LiElement, li
from haitch._elements._noscript import NoscriptElement, noscript
from haitch._elements._ol import OlElement, ol
from haitch._elements._p import ParagraphElement, p
from haitch._elements._pre import PreElement, pre
from haitch._elements._script import ScriptElement, script
from haitch._elements._span import SpanElement, span
from haitch._elements._style import StyleElement, style
from haitch._elements._table import TableElement, table
from haitch._elements._td import TdElement, td
from haitch._elements._th import ThElement, th
from haitch._elements._title import TitleElement, title
from haitch._elements._tr import TrElement, tr
from haitch._elements._ul import UlElement, ul
from haitch._typing import Html, SupportsHtml
from haitch._void_elements._area import AreaElement, area
from haitch._void_elements._base import BaseElement, base
from haitch._void_elements._br import BrElement, br
from haitch._void_elements._col import ColElement, col
from haitch._void_elements._embed import EmbedElement, embed
from haitch._void_elements._hr import HrElement, hr
from haitch._void_elements._img import ImgElement, img
from haitch._void_elements._input import InputElement, input
from haitch._void_elements._link import LinkElement, link
from haitch._void_elements._meta import MetaElement, meta
from haitch._void_elements._source import SourceElement, source
from haitch._void_elements._track import TrackElement, track
from haitch._void_elements._void_element import VoidElement
from haitch._void_elements._wbr import WbrElement, wbr

__all__ = [
    "AnchorElement",
    "AreaElement",
    "BaseElement",
    "BodyElement",
    "BrElement",
    "ColElement",
    "DivElement",
    "Element",
    "EmbedElement",
    "H1Element",
    "H2Element",
    "H3Element",
    "H4Element",
    "H5Element",
    "H6Element",
    "HeadElement",
    "HrElement",
    "Html",
    "HtmlElement",
    "ImgElement",
    "InputElement",
    "LiElement",
    "LinkElement",
    "MetaElement",
    "NoscriptElement",
    "OlElement",
    "ParagraphElement",
    "PreElement",
    "ScriptElement",
    "SourceElement",
    "SpanElement",
    "StyleElement",
    "SupportsHtml",
    "TableElement",
    "TdElement",
    "ThElement",
    "TitleElement",
    "TrElement",
    "TrackElement",
    "UlElement",
    "VoidElement",
    "WbrElement",
    "a",
    "area",
    "base",
    "body",
    "br",
    "col",
    "div",
    "embed",
    "fragment",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "hr",
    "html",
    "img",
    "input",
    "li",
    "link",
    "meta",
    "noscript",
    "ol",
    "p",
    "pre",
    "script",
    "source",
    "span",
    "style",
    "table",
    "td",
    "th",
    "title",
    "tr",
    "track",
    "ul",
    "wbr",
]


def __getattr__(tag: str) -> Element:
    return Element(tag)
