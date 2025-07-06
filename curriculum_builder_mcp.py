"""
CurriculumBuilderMCP - Intelligent Learning Journey Orchestrator
===============================================================

An autonomous MCP agent that takes in a user's learning goal and outputs
a structured multi-week curriculum with hands-on components.

This orchestrator coordinates multiple specialized sub-agents to build
comprehensive learning journeys.
"""

import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WeeklyContent:
    """Structure for weekly curriculum content"""
    week_number: int
    topic: str
    objective: str
    expected_outcomes: List[str]
    videos: List[Dict[str, str]]
    documentation: List[Dict[str, str]]
    hands_on_project: Dict[str, Any]
    quiz_questions: List[Dict[str, Any]]


@dataclass
class CurriculumPlan:
    """Complete curriculum plan structure"""
    goal_topic: str
    target_stack: List[str]
    total_weeks: int
    skill_level: str
    weekly_content: List[WeeklyContent]
    created_at: str
    estimated_hours_per_week: int


class CurriculumBuilderMCP:
    """
    Main orchestrator for the CurriculumBuilderMCP system.
    
    Coordinates multiple sub-agents to build custom learning journeys
    from high-level user goals.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.goal_agent = GoalAgent()
        self.curriculum_planner = CurriculumPlannerAgent()
        self.video_curator = VideoCuratorAgent()
        self.doc_finder = DocFinderAgent()
        self.hands_on_builder = HandsOnBuilderAgent()
        self.quiz_generator = QuizGeneratorAgent()
        self.export_agent = ExportAgent()
        
    async def build_curriculum(self, user_goal: str, timeframe: Optional[int] = None, 
                             skill_level: Optional[str] = None) -> CurriculumPlan:
        """
        Main orchestration method that builds a complete curriculum.
        
        Args:
            user_goal: High-level learning goal (e.g., "Learn Java", "Master React")
            timeframe: Optional number of weeks (default: 4-8 weeks)
            skill_level: Optional skill level override
            
        Returns:
            Complete curriculum plan
        """
        logger.info(f"🚀 Starting curriculum building for goal: {user_goal}")
        
        # Step 1: Parse goal and determine parameters
        goal_analysis = await self.goal_agent.analyze_goal(user_goal, timeframe, skill_level)
        logger.info(f"📊 Goal analysis complete: {goal_analysis['goal_topic']}")
        
        # Step 2: Generate curriculum structure
        curriculum_structure = await self.curriculum_planner.plan_curriculum(goal_analysis)
        logger.info(f"📋 Curriculum structure created: {curriculum_structure['total_weeks']} weeks")
        
        # Step 3: Build weekly content concurrently
        weekly_content_tasks = []
        for week_info in curriculum_structure['weekly_topics']:
            task = self._build_weekly_content(week_info, goal_analysis['skill_level'])
            weekly_content_tasks.append(task)
        
        weekly_content = await asyncio.gather(*weekly_content_tasks)
        
        # Step 4: Assemble final curriculum
        curriculum = CurriculumPlan(
            goal_topic=goal_analysis['goal_topic'],
            target_stack=goal_analysis['target_stack'],
            total_weeks=goal_analysis['total_weeks'],
            skill_level=goal_analysis['skill_level'],
            weekly_content=weekly_content,
            created_at=datetime.now().isoformat(),
            estimated_hours_per_week=curriculum_structure['estimated_hours_per_week']
        )
        
        logger.info("✅ Curriculum building complete!")
        return curriculum
    
    async def _build_weekly_content(self, week_info: Dict, skill_level: str) -> WeeklyContent:
        """Build content for a single week concurrently"""
        week_number = week_info['week_number']
        topic = week_info['topic']
        
        logger.info(f"🔨 Building content for Week {week_number}: {topic}")
        
        # Run all content generation tasks concurrently
        tasks = [
            self.video_curator.curate_videos(topic, skill_level),
            self.doc_finder.find_documentation(topic, skill_level),
            self.hands_on_builder.generate_project(topic, skill_level, week_number),
            self.quiz_generator.generate_quiz(topic, skill_level)
        ]
        
        videos, documentation, hands_on_project, quiz_questions = await asyncio.gather(*tasks)
        
        return WeeklyContent(
            week_number=week_number,
            topic=topic,
            objective=week_info['objective'],
            expected_outcomes=week_info['expected_outcomes'],
            videos=videos,
            documentation=documentation,
            hands_on_project=hands_on_project,
            quiz_questions=quiz_questions
        )
    
    async def export_curriculum(self, curriculum: CurriculumPlan, 
                              export_format: str = 'json') -> str:
        """Export curriculum to various formats"""
        return await self.export_agent.export(curriculum, export_format)
    
    async def push_to_notion(self, curriculum: CurriculumPlan, 
                           notion_token: str, database_id: str) -> bool:
        """Push curriculum to Notion for tracking"""
        return await self.export_agent.push_to_notion(curriculum, notion_token, database_id)


# Import all sub-agents
from agents.goal_agent import GoalAgent
from agents.curriculum_planner_agent import CurriculumPlannerAgent
from agents.video_curator_agent import VideoCuratorAgent
from agents.doc_finder_agent import DocFinderAgent
from agents.hands_on_builder_agent import HandsOnBuilderAgent
from agents.quiz_generator_agent import QuizGeneratorAgent
from agents.export_agent import ExportAgent


# CLI Interface
async def main():
    """CLI interface for the CurriculumBuilderMCP"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CurriculumBuilderMCP - Build Custom Learning Journeys")
    parser.add_argument("goal", help="Learning goal (e.g., 'Learn Python', 'Master React')")
    parser.add_argument("--weeks", type=int, help="Number of weeks (default: auto-determine)")
    parser.add_argument("--skill-level", choices=['beginner', 'intermediate', 'advanced'], 
                       help="Skill level override")
    parser.add_argument("--export", choices=['json', 'markdown', 'html'], 
                       default='json', help="Export format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--notion-token", help="Notion API token")
    parser.add_argument("--notion-database", help="Notion database ID")
    
    args = parser.parse_args()
    
    # Initialize the MCP
    mcp = CurriculumBuilderMCP()
    
    try:
        # Build curriculum
        curriculum = await mcp.build_curriculum(
            user_goal=args.goal,
            timeframe=args.weeks,
            skill_level=args.skill_level
        )
        
        # Export curriculum
        output = await mcp.export_curriculum(curriculum, args.export)
        
        # Save to file
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✅ Curriculum saved to {args.output}")
        else:
            print(output)
        
        # Push to Notion if configured
        if args.notion_token and args.notion_database:
            success = await mcp.push_to_notion(curriculum, args.notion_token, args.notion_database)
            if success:
                print("✅ Curriculum pushed to Notion successfully!")
            else:
                print("❌ Failed to push to Notion")
                
    except Exception as e:
        logger.error(f"❌ Error building curriculum: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
