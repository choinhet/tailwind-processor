# Tailwind Processor

[![codecov](https://codecov.io/gh/choinhet/tailwind-processor/graph/badge.svg?token=${CODECOV_TOKEN})](https://codecov.io/gh/choinhet/tailwind-processor)

This is a Python package that processes Tailwind CSS classes into a single raw CSS string.
It's super modular and simple, you can just copy the class directly and use it in your code.
Just make sure to install pytailwindcss first.

It uses GO style error handling.

## Installation

```bash
pip install tailwind-processor
```

## Usage

```python
from tailwind_processor import TailwindProcessor

tp = TailwindProcessor()

result, err = tp.process(["text-red-500", "h-dvh"])
if err:
    # Or do another thing
    raise err

file_content = textwrap.dedent("""
    <div class="text-red-500 h-dvh">
        Hey!
    </div>
""")

result, err = tp.process_file_str(file_content)

if err:
    # Or do another thing
    raise err
```
