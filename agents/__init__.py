"""
CurriculumBuilderMCP Agents Package
==================================

This package contains all the specialized sub-agents used by the
CurriculumBuilderMCP orchestrator.
"""

__version__ = "1.0.0"

from .goal_agent import GoalAgent
from .curriculum_planner_agent import CurriculumPlannerAgent
from .video_curator_agent import VideoCuratorAgent
from .doc_finder_agent import DocFinderAgent
from .hands_on_builder_agent import HandsOnBuilderAgent
from .quiz_generator_agent import QuizGeneratorAgent
from .export_agent import ExportAgent

__all__ = [
    'GoalAgent',
    'CurriculumPlannerAgent',
    'VideoCuratorAgent',
    'DocFinderAgent',
    'HandsOnBuilderAgent',
    'QuizGeneratorAgent',
    'ExportAgent'
]
