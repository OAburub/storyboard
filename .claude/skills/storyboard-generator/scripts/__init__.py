# scripts/__init__.py
# Storyboard Generator engine package
#
# DOCX Usage:
#   from docx_engine import TestBuilder, ActivityBuilder, VideoBuilder
#   from docx_engine import ObjectivesBuilder, SummaryBuilder
#   from docx_engine import InfographicBuilder, DiscussionBuilder, AssignmentBuilder
#
# PPTX Usage:
#   from pptx_engine import LectureBuilder

from docx_engine import (
    DocxBuilder,
    TestBuilder,
    ActivityBuilder,
    VideoBuilder,
    ObjectivesBuilder,
    SummaryBuilder,
    InfographicBuilder,
    DiscussionBuilder,
    AssignmentBuilder,
)

try:
    from pptx_engine import LectureBuilder
    __all__ = [
        "DocxBuilder",
        "TestBuilder",
        "ActivityBuilder",
        "VideoBuilder",
        "ObjectivesBuilder",
        "SummaryBuilder",
        "InfographicBuilder",
        "DiscussionBuilder",
        "AssignmentBuilder",
        "LectureBuilder",
    ]
except ImportError:
    __all__ = [
        "DocxBuilder",
        "TestBuilder",
        "ActivityBuilder",
        "VideoBuilder",
        "ObjectivesBuilder",
        "SummaryBuilder",
        "InfographicBuilder",
        "DiscussionBuilder",
        "AssignmentBuilder",
    ]
