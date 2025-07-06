"""
GoalAgent - Goal Analysis and Parameter Determination
=====================================================

This agent parses user's learning goals and determines:
- Goal topic and target technology stack
- Skill level (beginner/intermediate/advanced)
- Appropriate timeframe and weekly milestones
"""

import re
import asyncio
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class GoalAgent:
    """
    Agent responsible for parsing and analyzing user learning goals.
    
    Takes raw user input and converts it into structured learning parameters
    that other agents can work with.
    """
    
    def __init__(self):
        self.skill_indicators = {
            'beginner': ['learn', 'start', 'begin', 'basics', 'introduction', 'getting started', 'new to'],
            'intermediate': ['improve', 'better', 'enhance', 'deepen', 'advance', 'build upon'],
            'advanced': ['master', 'expert', 'deep dive', 'advanced', 'professional', 'production']
        }
        
        self.technology_stacks = {
            'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'scikit-learn'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular', 'express'],
            'java': ['java', 'spring', 'hibernate', 'maven', 'gradle'],
            'web_development': ['html', 'css', 'frontend', 'backend', 'fullstack', 'web development'],
            'data_science': ['data science', 'machine learning', 'ai', 'ml', 'analytics', 'statistics'],
            'mobile': ['mobile', 'android', 'ios', 'flutter', 'react native', 'swift', 'kotlin'],
            'devops': ['devops', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform'],
            'database': ['database', 'sql', 'postgresql', 'mysql', 'mongodb', 'redis']
        }
        
        self.time_estimates = {
            'beginner': {'min_weeks': 6, 'max_weeks': 12, 'hours_per_week': 8},
            'intermediate': {'min_weeks': 4, 'max_weeks': 8, 'hours_per_week': 6},
            'advanced': {'min_weeks': 3, 'max_weeks': 6, 'hours_per_week': 10}
        }
    
    async def analyze_goal(self, user_goal: str, timeframe: Optional[int] = None, 
                          skill_level: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze user's learning goal and extract structured parameters.
        
        Args:
            user_goal: Raw user input (e.g., "Learn Python for data science")
            timeframe: Optional explicit timeframe in weeks
            skill_level: Optional explicit skill level
            
        Returns:
            Dictionary with analyzed goal parameters
        """
        logger.info(f"🎯 Analyzing goal: {user_goal}")
        
        # Extract goal topic and technology stack
        goal_topic = self._extract_goal_topic(user_goal)
        target_stack = self._identify_technology_stack(user_goal)
        
        # Determine skill level
        if not skill_level:
            skill_level = self._determine_skill_level(user_goal)
        
        # Calculate timeframe
        if not timeframe:
            timeframe = self._calculate_timeframe(skill_level, target_stack)
        
        # Generate weekly milestones
        weekly_milestones = self._generate_milestones(goal_topic, target_stack, skill_level, timeframe)
        
        result = {
            'goal_topic': goal_topic,
            'target_stack': target_stack,
            'skill_level': skill_level,
            'total_weeks': timeframe,
            'weekly_milestones': weekly_milestones,
            'estimated_hours_per_week': self.time_estimates[skill_level]['hours_per_week']
        }
        
        logger.info(f"📊 Goal analysis complete: {result}")
        return result
    
    def _extract_goal_topic(self, user_goal: str) -> str:
        """Extract the main topic from user goal"""
        goal_lower = user_goal.lower()
        
        # Look for patterns like "learn X", "master Y", "get into Z"
        patterns = [
            r'learn\s+(.+?)(?:\s+for|\s+in|\s+with|$)',
            r'master\s+(.+?)(?:\s+for|\s+in|\s+with|$)',
            r'get\s+into\s+(.+?)(?:\s+for|\s+in|\s+with|$)',
            r'start\s+with\s+(.+?)(?:\s+for|\s+in|\s+with|$)',
            r'study\s+(.+?)(?:\s+for|\s+in|\s+with|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, goal_lower)
            if match:
                return match.group(1).strip().title()
        
        # If no pattern matches, return the goal as is
        return user_goal.strip().title()
    
    def _identify_technology_stack(self, user_goal: str) -> List[str]:
        """Identify relevant technology stack from user goal"""
        goal_lower = user_goal.lower()
        identified_stack = []
        
        for stack_category, technologies in self.technology_stacks.items():
            for tech in technologies:
                if tech in goal_lower:
                    identified_stack.append(tech)
        
        # Remove duplicates and return
        return list(set(identified_stack))
    
    def _determine_skill_level(self, user_goal: str) -> str:
        """Determine skill level based on language indicators"""
        goal_lower = user_goal.lower()
        
        # Count indicators for each skill level
        level_scores = {}
        for level, indicators in self.skill_indicators.items():
            score = sum(1 for indicator in indicators if indicator in goal_lower)
            level_scores[level] = score
        
        # Return the level with highest score, default to beginner
        if max(level_scores.values()) == 0:
            return 'beginner'
        
        return max(level_scores, key=level_scores.get)
    
    def _calculate_timeframe(self, skill_level: str, target_stack: List[str]) -> int:
        """Calculate appropriate timeframe based on skill level and complexity"""
        base_weeks = self.time_estimates[skill_level]['min_weeks']
        
        # Adjust based on technology stack complexity
        stack_complexity = len(target_stack)
        if stack_complexity > 3:
            base_weeks += 2
        elif stack_complexity > 1:
            base_weeks += 1
        
        # Ensure within reasonable bounds
        max_weeks = self.time_estimates[skill_level]['max_weeks']
        return min(base_weeks, max_weeks)
    
    def _generate_milestones(self, goal_topic: str, target_stack: List[str], 
                           skill_level: str, total_weeks: int) -> List[str]:
        """Generate weekly milestone descriptions"""
        milestones = []
        
        if skill_level == 'beginner':
            milestones = [
                f"Week 1: Introduction to {goal_topic} - Setup and Fundamentals",
                f"Week 2: Core Concepts and Basic Syntax",
                f"Week 3: Data Structures and Control Flow",
                f"Week 4: Functions and Modules",
                f"Week 5: Working with External Libraries",
                f"Week 6: First Project Development",
                f"Week 7: Testing and Debugging",
                f"Week 8: Advanced Topics and Best Practices"
            ]
        elif skill_level == 'intermediate':
            milestones = [
                f"Week 1: Advanced {goal_topic} Concepts",
                f"Week 2: Design Patterns and Architecture",
                f"Week 3: Framework Deep Dive",
                f"Week 4: Performance Optimization",
                f"Week 5: Testing and CI/CD",
                f"Week 6: Final Project"
            ]
        else:  # advanced
            milestones = [
                f"Week 1: Expert-Level {goal_topic} Techniques",
                f"Week 2: System Design and Architecture",
                f"Week 3: Performance and Scalability",
                f"Week 4: Production Best Practices"
            ]
        
        # Return only the number of weeks requested
        return milestones[:total_weeks]
