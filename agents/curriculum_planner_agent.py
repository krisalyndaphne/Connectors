"""
CurriculumPlannerAgent - Curriculum Structure Planning
=====================================================

This agent takes goal analysis and converts it into a detailed
week-by-week curriculum structure with specific topics, objectives,
and expected outcomes.
"""

import asyncio
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class CurriculumPlannerAgent:
    """
    Agent responsible for creating detailed curriculum structure.
    
    Takes goal analysis from GoalAgent and creates week-by-week
    curriculum with specific learning objectives and outcomes.
    """
    
    def __init__(self):
        self.curriculum_templates = {
            'python': {
                'beginner': [
                    {
                        'topic': 'Python Fundamentals',
                        'objective': 'Learn Python syntax, variables, and basic data types',
                        'expected_outcomes': [
                            'Write basic Python programs',
                            'Understand variables and data types',
                            'Use Python REPL effectively',
                            'Set up Python development environment'
                        ]
                    },
                    {
                        'topic': 'Control Structures and Functions',
                        'objective': 'Master conditional statements, loops, and function creation',
                        'expected_outcomes': [
                            'Write conditional logic with if/elif/else',
                            'Create and use for/while loops',
                            'Define and call functions',
                            'Understand scope and parameters'
                        ]
                    },
                    {
                        'topic': 'Data Structures',
                        'objective': 'Work with lists, dictionaries, sets, and tuples',
                        'expected_outcomes': [
                            'Manipulate lists and dictionaries',
                            'Choose appropriate data structures',
                            'Perform data structure operations',
                            'Understand indexing and slicing'
                        ]
                    },
                    {
                        'topic': 'File Handling and Modules',
                        'objective': 'Read/write files and organize code with modules',
                        'expected_outcomes': [
                            'Read and write text files',
                            'Handle CSV and JSON data',
                            'Import and create modules',
                            'Understand Python package structure'
                        ]
                    },
                    {
                        'topic': 'Object-Oriented Programming',
                        'objective': 'Learn classes, objects, and OOP principles',
                        'expected_outcomes': [
                            'Define classes and create objects',
                            'Understand inheritance and polymorphism',
                            'Use encapsulation and abstraction',
                            'Apply OOP best practices'
                        ]
                    },
                    {
                        'topic': 'Error Handling and Testing',
                        'objective': 'Handle exceptions and write unit tests',
                        'expected_outcomes': [
                            'Use try/except blocks effectively',
                            'Handle different exception types',
                            'Write unit tests with unittest',
                            'Debug Python programs'
                        ]
                    }
                ]
            },
            'javascript': {
                'beginner': [
                    {
                        'topic': 'JavaScript Fundamentals',
                        'objective': 'Learn JavaScript syntax, variables, and basic concepts',
                        'expected_outcomes': [
                            'Write basic JavaScript programs',
                            'Understand variables and data types',
                            'Use browser developer tools',
                            'Set up JavaScript development environment'
                        ]
                    },
                    {
                        'topic': 'Functions and Scope',
                        'objective': 'Master function creation, arrow functions, and scope',
                        'expected_outcomes': [
                            'Create regular and arrow functions',
                            'Understand function scope and closures',
                            'Use callback functions',
                            'Apply functional programming concepts'
                        ]
                    },
                    {
                        'topic': 'DOM Manipulation',
                        'objective': 'Interact with HTML elements using JavaScript',
                        'expected_outcomes': [
                            'Select and modify DOM elements',
                            'Handle user events',
                            'Create dynamic web content',
                            'Understand event propagation'
                        ]
                    },
                    {
                        'topic': 'Asynchronous JavaScript',
                        'objective': 'Learn promises, async/await, and API calls',
                        'expected_outcomes': [
                            'Use promises and async/await',
                            'Make HTTP requests with fetch',
                            'Handle asynchronous operations',
                            'Work with JSON data'
                        ]
                    }
                ]
            }
        }
        
        self.generic_templates = {
            'beginner': [
                {
                    'topic': 'Fundamentals and Setup',
                    'objective': 'Learn basic concepts and set up development environment',
                    'expected_outcomes': [
                        'Understand core concepts',
                        'Set up development environment',
                        'Write first program',
                        'Use basic syntax effectively'
                    ]
                },
                {
                    'topic': 'Core Concepts',
                    'objective': 'Master fundamental programming concepts',
                    'expected_outcomes': [
                        'Understand data types and variables',
                        'Use control structures',
                        'Apply basic algorithms',
                        'Debug simple programs'
                    ]
                },
                {
                    'topic': 'Intermediate Topics',
                    'objective': 'Explore more advanced concepts and patterns',
                    'expected_outcomes': [
                        'Use advanced data structures',
                        'Apply design patterns',
                        'Understand best practices',
                        'Build small projects'
                    ]
                },
                {
                    'topic': 'Project Development',
                    'objective': 'Build a complete project using learned concepts',
                    'expected_outcomes': [
                        'Plan and architect a project',
                        'Implement core functionality',
                        'Test and debug code',
                        'Deploy the project'
                    ]
                }
            ]
        }
    
    async def plan_curriculum(self, goal_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create detailed curriculum structure from goal analysis.
        
        Args:
            goal_analysis: Output from GoalAgent containing goal parameters
            
        Returns:
            Dictionary with detailed curriculum structure
        """
        logger.info(f"📋 Planning curriculum for {goal_analysis['goal_topic']}")
        
        # Extract parameters
        goal_topic = goal_analysis['goal_topic'].lower()
        skill_level = goal_analysis['skill_level']
        total_weeks = goal_analysis['total_weeks']
        target_stack = goal_analysis['target_stack']
        
        # Get appropriate curriculum template
        weekly_topics = self._get_curriculum_template(goal_topic, skill_level, total_weeks, target_stack)
        
        # Calculate estimated hours
        estimated_hours_per_week = goal_analysis['estimated_hours_per_week']
        
        curriculum_structure = {
            'total_weeks': total_weeks,
            'estimated_hours_per_week': estimated_hours_per_week,
            'weekly_topics': weekly_topics,
            'learning_path': self._generate_learning_path(weekly_topics),
            'prerequisites': self._determine_prerequisites(goal_topic, skill_level),
            'final_outcomes': self._generate_final_outcomes(goal_topic, skill_level)
        }
        
        logger.info(f"📋 Curriculum structure created: {len(weekly_topics)} weeks planned")
        return curriculum_structure
    
    def _get_curriculum_template(self, goal_topic: str, skill_level: str, 
                               total_weeks: int, target_stack: List[str]) -> List[Dict[str, Any]]:
        """Get appropriate curriculum template based on goal"""
        
        # Try to find specific template for the technology
        template = None
        for tech in target_stack:
            if tech in self.curriculum_templates:
                if skill_level in self.curriculum_templates[tech]:
                    template = self.curriculum_templates[tech][skill_level]
                    break
        
        # Fall back to generic template
        if not template:
            template = self.generic_templates.get(skill_level, self.generic_templates['beginner'])
        
        # Adjust template to match requested weeks
        weekly_topics = []
        for i in range(total_weeks):
            if i < len(template):
                topic_data = template[i].copy()
            else:
                # Generate additional weeks if needed
                topic_data = self._generate_additional_week(goal_topic, skill_level, i + 1)
            
            topic_data['week_number'] = i + 1
            weekly_topics.append(topic_data)
        
        return weekly_topics
    
    def _generate_additional_week(self, goal_topic: str, skill_level: str, week_number: int) -> Dict[str, Any]:
        """Generate additional week content when template is insufficient"""
        if skill_level == 'beginner':
            return {
                'topic': f'Advanced {goal_topic} Topics',
                'objective': f'Explore advanced concepts and build practical projects',
                'expected_outcomes': [
                    'Apply advanced techniques',
                    'Build complex projects',
                    'Follow best practices',
                    'Prepare for next level'
                ]
            }
        elif skill_level == 'intermediate':
            return {
                'topic': f'Professional {goal_topic} Development',
                'objective': 'Master professional development practices',
                'expected_outcomes': [
                    'Use professional tools',
                    'Apply industry standards',
                    'Build portfolio projects',
                    'Optimize performance'
                ]
            }
        else:  # advanced
            return {
                'topic': f'Expert-Level {goal_topic}',
                'objective': 'Master expert-level concepts and techniques',
                'expected_outcomes': [
                    'Solve complex problems',
                    'Architect scalable solutions',
                    'Mentor others',
                    'Contribute to open source'
                ]
            }
    
    def _generate_learning_path(self, weekly_topics: List[Dict[str, Any]]) -> List[str]:
        """Generate overall learning path description"""
        path = []
        for week in weekly_topics:
            path.append(f"Week {week['week_number']}: {week['topic']}")
        return path
    
    def _determine_prerequisites(self, goal_topic: str, skill_level: str) -> List[str]:
        """Determine prerequisites for the learning goal"""
        if skill_level == 'beginner':
            return [
                'Basic computer literacy',
                'Willingness to problem-solve',
                'Time commitment (6-10 hours per week)'
            ]
        elif skill_level == 'intermediate':
            return [
                f'Basic knowledge of {goal_topic}',
                'Programming fundamentals',
                'Development environment setup',
                'Time commitment (4-8 hours per week)'
            ]
        else:  # advanced
            return [
                f'Strong background in {goal_topic}',
                'Professional development experience',
                'Understanding of software architecture',
                'Time commitment (8-12 hours per week)'
            ]
    
    def _generate_final_outcomes(self, goal_topic: str, skill_level: str) -> List[str]:
        """Generate expected final outcomes for the curriculum"""
        if skill_level == 'beginner':
            return [
                f'Solid foundation in {goal_topic}',
                'Ability to build basic projects',
                'Understanding of best practices',
                'Readiness for intermediate topics',
                'Portfolio of learning projects'
            ]
        elif skill_level == 'intermediate':
            return [
                f'Advanced proficiency in {goal_topic}',
                'Ability to build complex applications',
                'Understanding of design patterns',
                'Professional development practices',
                'Portfolio of production-ready projects'
            ]
        else:  # advanced
            return [
                f'Expert-level mastery of {goal_topic}',
                'Ability to architect scalable systems',
                'Leadership in technical decisions',
                'Contribution to community/open source',
                'Mentoring capabilities'
            ]
