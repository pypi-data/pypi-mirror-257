<img width="200px" src="https://git.sr.ht/~loges/haitch/blob/master/docs/img/logo.svg" alt='haitch logo'>

_A lazy HTML element builder._

[![builds.sr.ht status](https://builds.sr.ht/~loges/haitch.svg)](https://builds.sr.ht/~loges/haitch?)
[![PyPI - Version](https://img.shields.io/pypi/v/haitch.svg)](https://pypi.org/project/haitch)

# haitch

> _haitch_, an alternative pronunciation for the letter "H".

The `haitch` package provides a builder for composing HTML elements in a Document Object Model (DOM) tree. The element nodes will only be rendered when the `__str__` method is invoked.

Why write your HTML in templates when you can do it in Python?

## Features

- Compose HTML elements.
- Lazily evaluate DOM tree.
- 100% test coverage.
- 100% type annotated codebase.
- Zero dependencies.

## Requirements

Python 3.8+

## Quickstart

Install `haitch` using pip:

```console
$ pip install haitch
```

Import the library like so:

```python
import haitch as H
```

By importing the root module, you now have access to any element you want:

```python
# Render known `h1` tag.
h1 = H.h1("Hello, world")
print(h1) # <h1>Hello, world</h1>

# Render custom `foo` tag (useful for web components).
foo = H.foo("Hello, world")
print(foo) # <foo>Hello, world!</foo>
```

Here is a simple, real-world example that showcases the advantage of writing HTML in Python. Let's say we want a list of customer emails based on some business logic:

```python
# Fetch customers from a data store.
customers = [
    ("jane@aol.com", False, True),
    ("bob@example.com", True, False),
    ("mark@mail.org", True, False),
    ("karen@hr.org", False, False),
]

# Build the DOM tree with attributes and children.
dom = H.div(class_="container")(
    H.h1("Customers to contact:"),
    H.ul()(
        [
            H.li(
                H.a(href=f"mailto:{email}")(email),
            )
            for email, is_premium, is_new in customers
            if is_premium or is_new
        ],
    ),
)

print(dom)
# <div class="container">
#   <h1>Customers to contact:</h1>
#   <ul>
#     <li><a href="mailto:jane@aol.com">jane@aol.com</a></li>
#     <li><a href="mailto:bob@example.com">bob@example.com</a></li>
#     <li><a href="mailto:mark@mail.org">mark@mail.org</a></li>
#   </ul>
# </div>
```

FYI: The example output is prettified for better readability. The actual output is a minified string with no formatting.

## Motivation

I was inspired by the fantastic [htbuilder](https://github.com/tvst/htbuilder) library as an alternative to template engines. The library met most of my needs, but I really wanted to expand its functionality by leveraging modern Python features like type annotations. This coincided with my excitement for [Hypermedia-Driven Applications (HDAs)](https://htmx.org/essays/hypermedia-driven-applications/) with tools like `htmx` and `alpine`.

While writing HDAs has simplified my application logic, the lack of autocompletion and diagnostics in templates are quite annoying. Therefore, my goal with this package is to make writing HTML as simple and fun as writing normal Python code _by writing normal Python code_.

## Roadmap

- Explicit attribute annotations for known elements like `a`, `img`, etc.
- Document elements based on [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML).
- Extra Annotations for common third-party plugins like [htmx](https://htmx.org/) and [alpine](https://alpinejs.dev/).

## Non-goals

The following features will _not_ be supported:

- **Deprecated elements and attributes**: if you want to use them, that is fine by me as `haitch` supports generic elements and attributes. However, I am not going to write the annotations and documentation for them.
- **100% input validation**: this library is meant to assist the developer to write valid HTML with the help of type annotations and documentation. In the end, it is up to the developer and browser to verify that the input is of the correct type. So for example, I will not add any validation to make sure that a `<col>` element is directly nested inside of a `<colgroup>` element or that the `span` attribute for the `<col>` element is a positive integer.

## License

`haitch` is distributed under the terms of the [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
