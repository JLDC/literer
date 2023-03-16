"""
literer

A package that drops literature reviews in public places.
"""

from literer.assistant import get_keywords, full_review, single_review
from literer.scholar import get_papers

__version__ = "0.1.0"
__author__ = "Jonathan Chassot"
__all__ = ["get_papers", "get_keywords", "single_review", "full_review"]