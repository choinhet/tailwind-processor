# Tailwind Processor

[![codecov](https://codecov.io/gh/choinhet/tailwind-processor/graph/badge.svg?token=${CODECOV_TOKEN})](https://codecov.io/gh/choinhet/tailwind-processor)

This is a Python package that processes Tailwind CSS classes into a single raw CSS string.
It's super modular and simple, you can just copy the class directly and use it in your code.
Just make sure to install pytailwindcss first.

## Installation

```bash
pip install tailwind-processor
```

## Usage

```python
from tailwind_processor import TailwindProcessor

tp = TailwindProcessor()
tp.process(["text-red-500", "h-dvh"])
```