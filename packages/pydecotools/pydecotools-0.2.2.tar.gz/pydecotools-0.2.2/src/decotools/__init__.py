#!/usr/bin/env python
"""The collection of decorator utilities."""

__title__ = "pydecotools"
__description__ = "The collection of decorator utilities."
__url__ = f"https://github.com/ilotoki0804/{__title__}"
__raw_source_url__ = f"https://raw.githubusercontent.com/ilotoki0804/{__title__}/master"
__version_info__ = (0, 2, 2)
__version__ = str.join(".", map(str, __version_info__))
__author__ = "ilotoki0804"
__credits__ = ["ilotoki0804"]
__copyright__ = "Copyright 2023 ilotoki0804"
__author_email__ = "ilotoki0804@gmail.com"
__license__ = "MIT License"
__status__ = (1, "Planning")
__is_deprecated__ = False

from .applier import (
    DecoratorOperatorMeta,
    decorator,
    smart_partial,
)
