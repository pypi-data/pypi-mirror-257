# Python Service Library for Merrymake

This is the official Python service library for Merrymake. It defines all the basic functions needed to work with Merrymake.

## Usage

Here is the most basic example of how to use this library:

```python
import sys

from merrymake import Merrymake
from merrymake.merrymimetypes import MerryMimetypes
from merrymake.envelope import Envelope

def handle_hello(payloadBytes: bytearray, envelope: Envelope):
    payload = bytes(payloadBytes).decode('utf-8')
    Merrymake.reply_to_origin(f"Hello, {payload}!", MerryMimetypes.get_mime_type("txt"));

def main():
    (Merrymake.service()
        .handle("handle_hello", handle_hello));

if __name__ == "__main__":
    main()
```

## Tutorials and templates

For more information check out our tutorials at [merrymake.dev](https://merrymake.dev).

All templates are available through our CLI and on our [GitHub](https://github.com/merrymake).


