"""
HandsOnBuilderAgent - Hands-On Project Generation
=================================================

This agent generates practical coding projects, exercises,
and hands-on tasks that reinforce learning for each topic.
"""

import asyncio
from typing import Dict, List, Optional, Any
import logging
import random

logger = logging.getLogger(__name__)


class HandsOnBuilderAgent:
    """
    Agent responsible for generating hands-on coding projects and exercises.
    
    Creates practical tasks that reinforce learning through doing,
    ranging from simple exercises to complete projects.
    """
    
    def __init__(self):
        self.project_templates = {
            'python': {
                'beginner': [
                    {
                        'type': 'exercise',
                        'title': 'Basic Calculator',
                        'description': 'Create a calculator that can perform basic arithmetic operations',
                        'learning_objectives': [
                            'Practice using variables and functions',
                            'Implement conditional logic',
                            'Handle user input and output',
                            'Basic error handling'
                        ],
                        'requirements': [
                            'Accept two numbers and an operation from user',
                            'Perform addition, subtraction, multiplication, division',
                            'Handle division by zero',
                            'Display results clearly'
                        ],
                        'estimated_time': '2-3 hours',
                        'difficulty': 'Easy',
                        'files_to_create': ['calculator.py'],
                        'starter_code': '''def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# TODO: Implement multiply and divide functions
# TODO: Add main function to handle user input
# TODO: Add error handling
'''
                    },
                    {
                        'type': 'project',
                        'title': 'Personal Budget Tracker',
                        'description': 'Build a simple budget tracking application',
                        'learning_objectives': [
                            'Work with lists and dictionaries',
                            'File I/O operations',
                            'Data validation',
                            'Basic data analysis'
                        ],
                        'requirements': [
                            'Add income and expense entries',
                            'Categorize expenses',
                            'Save data to file',
                            'Generate basic reports'
                        ],
                        'estimated_time': '4-6 hours',
                        'difficulty': 'Medium',
                        'files_to_create': ['budget_tracker.py', 'data.json'],
                        'starter_code': '''import json
from datetime import datetime

class BudgetTracker:
    def __init__(self):
        self.transactions = []
    
    def add_transaction(self, amount, category, description, transaction_type):
        # TODO: Implement transaction addition
        pass
    
    def save_to_file(self, filename):
        # TODO: Implement file saving
        pass
    
    def generate_report(self):
        # TODO: Implement report generation
        pass

if __name__ == "__main__":
    tracker = BudgetTracker()
    # TODO: Add main program loop
'''
                    }
                ]
            },
            'javascript': {
                'beginner': [
                    {
                        'type': 'exercise',
                        'title': 'Interactive To-Do List',
                        'description': 'Create a dynamic to-do list with add, remove, and complete functionality',
                        'learning_objectives': [
                            'DOM manipulation',
                            'Event handling',
                            'Local storage',
                            'Array methods'
                        ],
                        'requirements': [
                            'Add new tasks',
                            'Mark tasks as complete',
                            'Delete tasks',
                            'Persist data in localStorage'
                        ],
                        'estimated_time': '3-4 hours',
                        'difficulty': 'Medium',
                        'files_to_create': ['index.html', 'style.css', 'script.js'],
                        'starter_code': '''// script.js
class TodoList {
    constructor() {
        this.tasks = [];
        this.loadTasks();
        this.bindEvents();
    }
    
    addTask(taskText) {
        // TODO: Implement task addition
    }
    
    removeTask(taskId) {
        // TODO: Implement task removal
    }
    
    // TODO: Implement remaining methods
}

const todoList = new TodoList();
'''
                    }
                ]
            }
        }
        
        self.exercise_types = {
            'coding_challenges': [
                'Algorithm implementation',
                'Data structure exercises',
                'Problem-solving challenges',
                'Code optimization tasks'
            ],
            'mini_projects': [
                'Small utility applications',
                'Simple games',
                'Basic web applications',
                'Command-line tools'
            ],
            'real_world_scenarios': [
                'Business logic implementation',
                'API integration projects',
                'Database interaction tasks',
                'UI/UX implementation'
            ]
        }
        
        self.difficulty_progression = {
            'beginner': ['exercises', 'mini_projects'],
            'intermediate': ['mini_projects', 'real_world_scenarios'],
            'advanced': ['real_world_scenarios', 'coding_challenges']
        }
    
    async def generate_project(self, topic: str, skill_level: str, week_number: int) -> Dict[str, Any]:
        """
        Generate a hands-on project for the given topic and skill level.
        
        Args:
            topic: Learning topic (e.g., "Python Fundamentals")
            skill_level: beginner/intermediate/advanced
            week_number: Week number in the curriculum
            
        Returns:
            Dictionary containing project details
        """
        logger.info(f"🔨 Generating hands-on project for {topic} (Week {week_number}, {skill_level})")
        
        # Try to get specific project template
        project = self._get_project_template(topic, skill_level, week_number)
        
        if not project:
            # Generate generic project
            project = self._generate_generic_project(topic, skill_level, week_number)
        
        # Add week-specific enhancements
        project = self._enhance_project_for_week(project, week_number, skill_level)
        
        logger.info(f"🔨 Generated project: {project['title']}")
        return project
    
    def _get_project_template(self, topic: str, skill_level: str, week_number: int) -> Optional[Dict[str, Any]]:
        """Get a specific project template for the topic"""
        topic_lower = topic.lower()
        
        # Look for matching technology in templates
        for tech in self.project_templates:
            if tech in topic_lower:
                if skill_level in self.project_templates[tech]:
                    templates = self.project_templates[tech][skill_level]
                    # Select template based on week number (cycle through if needed)
                    template_index = (week_number - 1) % len(templates)
                    return templates[template_index].copy()
        
        return None
    
    def _generate_generic_project(self, topic: str, skill_level: str, week_number: int) -> Dict[str, Any]:
        """Generate a generic project when no specific template exists"""
        
        # Determine project type based on skill level and week
        project_types = self.difficulty_progression.get(skill_level, ['exercises'])
        project_type = project_types[(week_number - 1) % len(project_types)]
        
        if project_type == 'exercises':
            return self._generate_exercise_project(topic, skill_level)
        elif project_type == 'mini_projects':
            return self._generate_mini_project(topic, skill_level)
        else:  # real_world_scenarios
            return self._generate_real_world_project(topic, skill_level)
    
    def _generate_exercise_project(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a coding exercise project"""
        topic_clean = topic.replace(' Fundamentals', '').replace(' Basics', '').strip()
        
        return {
            'type': 'exercise',
            'title': f'{topic_clean} Practice Exercises',
            'description': f'Collection of hands-on exercises to practice {topic_clean} concepts',
            'learning_objectives': [
                f'Practice core {topic_clean} concepts',
                'Apply problem-solving skills',
                'Build coding fluency',
                'Reinforce syntax and patterns'
            ],
            'requirements': [
                'Complete 5-8 progressive exercises',
                'Test your solutions thoroughly',
                'Optimize for readability and efficiency',
                'Document your approach'
            ],
            'estimated_time': '2-4 hours',
            'difficulty': 'Easy' if skill_level == 'beginner' else 'Medium',
            'files_to_create': [f'{topic_clean.lower().replace(" ", "_")}_exercises.py'],
            'exercises': self._generate_exercise_list(topic_clean, skill_level),
            'starter_code': f'# {topic_clean} Practice Exercises\n# Complete each function below\n\n# Exercise 1\ndef exercise_1():\n    # TODO: Implement solution\n    pass\n'
        }
    
    def _generate_mini_project(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a mini project based on the specific topic"""
        topic_clean = topic.replace(' Fundamentals', '').replace(' Basics', '').strip()
        topic_lower = topic_clean.lower()
        
        # Generate topic-specific project ideas
        if 'python' in topic_lower:
            if 'web' in topic_lower or 'django' in topic_lower or 'flask' in topic_lower:
                project_ideas = ['Blog Platform', 'Task Manager API', 'Recipe Sharing Site', 'Weather Dashboard']
            elif 'data' in topic_lower or 'analysis' in topic_lower:
                project_ideas = ['Sales Data Analyzer', 'Stock Price Tracker', 'Survey Results Dashboard', 'Social Media Analytics']
            else:
                project_ideas = ['Personal Finance Tracker', 'File Organizer', 'Contact Manager', 'Quiz Application']
        elif 'javascript' in topic_lower:
            if 'react' in topic_lower:
                project_ideas = ['Todo App with React', 'Movie Search App', 'Recipe Finder', 'Weather Widget']
            elif 'node' in topic_lower:
                project_ideas = ['REST API Server', 'Chat Application', 'File Upload Service', 'User Authentication System']
            else:
                project_ideas = ['Interactive Dashboard', 'Memory Game', 'Calculator App', 'Image Gallery']
        elif 'web development' in topic_lower:
            project_ideas = ['Responsive Portfolio', 'Business Landing Page', 'E-commerce Product Page', 'Online Resume']
        elif 'java' in topic_lower:
            project_ideas = ['Library Management System', 'Banking Application', 'Student Grade Calculator', 'Inventory Tracker']
        elif 'data science' in topic_lower or 'machine learning' in topic_lower:
            project_ideas = ['Predictive Model', 'Data Visualization Dashboard', 'Customer Segmentation', 'Recommendation System']
        else:
            # Generic projects based on skill level
            if skill_level == 'beginner':
                project_ideas = ['Simple Calculator', 'To-Do List', 'Basic Game', 'Data Processor']
            elif skill_level == 'intermediate':
                project_ideas = ['Web Application', 'API Service', 'Data Dashboard', 'Mobile App']
            else:
                project_ideas = ['Microservice Architecture', 'ML Pipeline', 'Full-Stack Platform', 'Distributed System']
        
        # Select a project idea
        project_title = random.choice(project_ideas)
        
        return {
            'type': 'mini_project',
            'title': f'{topic_clean} {project_title}',
            'description': f'Build a {project_title.lower()} to practice {topic_clean} skills',
            'learning_objectives': [
                f'Apply {topic_clean} concepts in a real project',
                'Practice project planning and execution',
                'Implement user-friendly features',
                'Debug and test thoroughly'
            ],
            'requirements': [
                'Plan the application structure',
                'Implement core functionality',
                'Add error handling',
                'Create user documentation'
            ],
            'estimated_time': '4-8 hours',
            'difficulty': 'Medium',
            'files_to_create': self._get_project_files(topic_clean, project_title),
            'features': self._generate_project_features(project_title, skill_level),
            'bonus_challenges': self._generate_bonus_challenges(project_title)
        }
    
    def _generate_real_world_project(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a real-world scenario project"""
        topic_clean = topic.replace(' Fundamentals', '').replace(' Basics', '').strip()
        
        scenarios = [
            'E-commerce Product Catalog',
            'Employee Management System',
            'Event Booking Platform',
            'Content Management System',
            'Analytics Dashboard'
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            'type': 'real_world_project',
            'title': f'{topic_clean} {scenario}',
            'description': f'Build a {scenario.lower()} that solves real business needs',
            'learning_objectives': [
                f'Apply advanced {topic_clean} concepts',
                'Implement business logic',
                'Handle complex data structures',
                'Follow industry best practices'
            ],
            'requirements': [
                'Design scalable architecture',
                'Implement full CRUD operations',
                'Add authentication/authorization',
                'Include comprehensive testing'
            ],
            'estimated_time': '8-15 hours',
            'difficulty': 'Hard',
            'files_to_create': self._get_enterprise_project_files(topic_clean),
            'user_stories': self._generate_user_stories(scenario),
            'technical_requirements': self._generate_technical_requirements(scenario)
        }
    
    def _enhance_project_for_week(self, project: Dict[str, Any], week_number: int, skill_level: str) -> Dict[str, Any]:
        """Add week-specific enhancements to the project"""
        enhanced_project = project.copy()
        
        # Add progressive complexity based on week
        if week_number <= 2:
            enhanced_project['focus'] = 'Learning fundamentals through practice'
            enhanced_project['success_criteria'] = 'Complete basic functionality'
        elif week_number <= 4:
            enhanced_project['focus'] = 'Building confidence with guided projects'
            enhanced_project['success_criteria'] = 'Implement all core features'
        else:
            enhanced_project['focus'] = 'Independent problem-solving'
            enhanced_project['success_criteria'] = 'Add creative enhancements'
        
        # Add week-specific hints and resources
        enhanced_project['week_specific_tips'] = self._get_week_tips(week_number)
        enhanced_project['submission_guidelines'] = self._get_submission_guidelines(project['type'])
        
        return enhanced_project
    
    def _generate_exercise_list(self, topic: str, skill_level: str) -> List[str]:
        """Generate a list of exercises for the topic"""
        base_exercises = [
            f'Implement basic {topic} functionality',
            f'Create utility functions for {topic}',
            f'Process and manipulate {topic} data',
            f'Build simple {topic} algorithms',
            f'Handle edge cases in {topic} operations'
        ]
        
        if skill_level in ['intermediate', 'advanced']:
            base_exercises.extend([
                f'Optimize {topic} performance',
                f'Implement advanced {topic} patterns',
                f'Create reusable {topic} components'
            ])
        
        return base_exercises[:6]  # Return first 6 exercises
    
    def _generate_project_features(self, project_title: str, skill_level: str) -> List[str]:
        """Generate features for the project"""
        feature_map = {
            'Weather App': ['Current weather display', 'Location search', 'Forecast view', 'Favorite locations'],
            'Memory Game': ['Card matching', 'Score tracking', 'Difficulty levels', 'High scores'],
            'Password Generator': ['Custom length', 'Character options', 'Strength indicator', 'Copy to clipboard'],
            'Quiz Game': ['Multiple choice questions', 'Score tracking', 'Timer', 'Results summary']
        }
        
        features = feature_map.get(project_title, ['Core functionality', 'User interface', 'Data handling', 'Error management'])
        
        if skill_level in ['intermediate', 'advanced']:
            features.extend(['Data persistence', 'Advanced settings', 'Export functionality'])
        
        return features
    
    def _generate_bonus_challenges(self, project_title: str) -> List[str]:
        """Generate bonus challenges for extra practice"""
        return [
            'Add data validation and error handling',
            'Implement responsive design',
            'Add animation and visual effects',
            'Create unit tests for your functions',
            'Add accessibility features'
        ]
    
    def _get_project_files(self, topic: str, project_title: str) -> List[str]:
        """Determine files needed for the project"""
        topic_lower = topic.lower()
        
        if 'web' in topic_lower or 'html' in topic_lower or 'css' in topic_lower:
            return ['index.html', 'style.css', 'script.js', 'README.md']
        elif 'python' in topic_lower:
            return [f'{project_title.lower().replace(" ", "_")}.py', 'requirements.txt', 'README.md']
        elif 'java' in topic_lower:
            return [f'{project_title.replace(" ", "")}.java', 'README.md']
        else:
            return ['main.py', 'README.md']
    
    def _get_enterprise_project_files(self, topic: str) -> List[str]:
        """Get file structure for enterprise-level projects"""
        base_files = ['README.md', 'requirements.txt', '.gitignore']
        
        if 'web' in topic.lower():
            return base_files + ['index.html', 'src/css/style.css', 'src/js/app.js', 'src/js/utils.js']
        else:
            return base_files + ['src/main.py', 'src/models.py', 'src/utils.py', 'tests/test_main.py']
    
    def _generate_user_stories(self, scenario: str) -> List[str]:
        """Generate user stories for real-world projects"""
        return [
            f'As a user, I want to access {scenario.lower()} features easily',
            f'As an admin, I want to manage {scenario.lower()} data efficiently',
            f'As a user, I want my data to be secure and private',
            f'As a user, I want the system to be fast and reliable'
        ]
    
    def _generate_technical_requirements(self, scenario: str) -> List[str]:
        """Generate technical requirements for projects"""
        return [
            'Clean, readable code with proper documentation',
            'Modular architecture with separation of concerns',
            'Error handling and input validation',
            'Performance optimization and scalability considerations',
            'Security best practices implementation'
        ]
    
    def _get_week_tips(self, week_number: int) -> List[str]:
        """Get week-specific tips for learners"""
        tips = {
            1: ['Focus on understanding the basics', 'Don\'t worry about perfection', 'Ask questions when stuck'],
            2: ['Practice makes perfect', 'Try variations of the exercises', 'Review concepts regularly'],
            3: ['Start planning before coding', 'Break problems into smaller parts', 'Test your code frequently'],
            4: ['Focus on code organization', 'Add comments and documentation', 'Consider edge cases'],
            5: ['Think about user experience', 'Optimize for performance', 'Add error handling'],
            6: ['Polish your project', 'Add extra features', 'Prepare for presentation']
        }
        
        return tips.get(week_number, tips[3])  # Default to week 3 tips
    
    def _get_submission_guidelines(self, project_type: str) -> List[str]:
        """Get submission guidelines for different project types"""
        guidelines = {
            'exercise': [
                'Submit all completed exercise files',
                'Include comments explaining your approach',
                'Test your solutions before submission'
            ],
            'mini_project': [
                'Include all project files and dependencies',
                'Write a README with setup instructions',
                'Document any challenges and solutions'
            ],
            'real_world_project': [
                'Provide complete project documentation',
                'Include setup and deployment instructions',
                'Present your solution and architecture decisions'
            ]
        }
        
        return guidelines.get(project_type, guidelines['exercise'])
