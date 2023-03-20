"""
literer

A package that drops literature reviews in public places.
"""
from literer.assistant import summarize_papers, single_review, get_keywords, judge_paper
from literer.scholar import get_papers, create_bibliography
from literer.utils import get_gpt_model, set_gpt_model
from literer.reviewer import give_feedback, make_paragraphs

__version__ = "0.1.1"
__author__ = "Jonathan Chassot"
__all__ = [
    "get_keywords", 
    "get_papers", 
    "single_review", 
    "summarize_papers", 
    "judge_paper",
    "create_bibliography",
    "test_model",
    "get_gpt_model",
    "set_gpt_model",
    "give_feedback",
    "make_paragraphs"    
]
