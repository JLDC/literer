"""
literer

A package that drops literature reviews in public places.
"""

from literer.assistant import summarize_papers, single_review, get_keywords
from literer.scholar import get_papers, create_bibliography

__version__ = "0.1.0"
__author__ = "Jonathan Chassot"
__all__ = ["get_keywords", "get_papers", "single_review", "summarize_papers", "create_bibliography"]