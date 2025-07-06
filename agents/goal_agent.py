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
        """Generate weekly milestone descriptions based on actual goal analysis"""
        milestones = []
        goal_topic_clean = goal_topic.lower()
        
        # Technology-specific milestone generation
        if any(tech in goal_topic_clean for tech in ['python', 'django', 'flask']):
            milestones = self._generate_python_milestones(skill_level, target_stack, total_weeks)
        elif any(tech in goal_topic_clean for tech in ['javascript', 'react', 'vue', 'angular', 'node']):
            milestones = self._generate_javascript_milestones(skill_level, target_stack, total_weeks)
        elif any(tech in goal_topic_clean for tech in ['java', 'spring']):
            milestones = self._generate_java_milestones(skill_level, target_stack, total_weeks)
        elif any(tech in goal_topic_clean for tech in ['data science', 'machine learning', 'ai', 'ml']):
            milestones = self._generate_data_science_milestones(skill_level, target_stack, total_weeks)
        elif any(tech in goal_topic_clean for tech in ['web development', 'frontend', 'backend', 'fullstack']):
            milestones = self._generate_web_dev_milestones(skill_level, target_stack, total_weeks)
        else:
            # Generic milestone generation based on goal analysis
            milestones = self._generate_generic_milestones(goal_topic, skill_level, total_weeks)
        
        # Ensure we have exactly the requested number of weeks
        while len(milestones) < total_weeks:
            milestones.append(f"Week {len(milestones) + 1}: Advanced {goal_topic} Application")
        
        return milestones[:total_weeks]
    
    def _generate_python_milestones(self, skill_level: str, target_stack: List[str], total_weeks: int) -> List[str]:
        """Generate Python-specific learning milestones"""
        if skill_level == 'beginner':
            base_milestones = [
                "Week 1: Python Environment Setup and Basic Syntax",
                "Week 2: Variables, Data Types, and String Manipulation", 
                "Week 3: Control Structures and Loops",
                "Week 4: Functions and Error Handling",
                "Week 5: Data Structures (Lists, Dictionaries, Sets)",
                "Week 6: File I/O and Working with Modules",
                "Week 7: Object-Oriented Programming Basics",
                "Week 8: Libraries and Package Management"
            ]
        elif skill_level == 'intermediate':
            base_milestones = [
                "Week 1: Advanced Python Features and Decorators",
                "Week 2: Object-Oriented Design Patterns", 
                "Week 3: Testing with pytest and unittest",
                "Week 4: Working with APIs and HTTP Requests",
                "Week 5: Database Integration and ORM",
                "Week 6: Asynchronous Programming"
            ]
        else:  # advanced
            base_milestones = [
                "Week 1: Python Performance Optimization",
                "Week 2: Concurrency and Parallel Processing",
                "Week 3: Advanced Design Patterns and Architecture",
                "Week 4: Production Deployment and Monitoring"
            ]
        
        # Add framework-specific milestones
        if 'django' in target_stack:
            base_milestones.extend([
                f"Week {len(base_milestones) + 1}: Django Framework Fundamentals",
                f"Week {len(base_milestones) + 2}: Django Models and Database Design",
                f"Week {len(base_milestones) + 3}: Django Views and Templates",
                f"Week {len(base_milestones) + 4}: Django REST API Development"
            ])
        elif 'flask' in target_stack:
            base_milestones.extend([
                f"Week {len(base_milestones) + 1}: Flask Application Structure",
                f"Week {len(base_milestones) + 2}: Flask Blueprints and Database Integration",
                f"Week {len(base_milestones) + 3}: Flask API Development and Testing"
            ])
        
        return base_milestones
    
    def _generate_javascript_milestones(self, skill_level: str, target_stack: List[str], total_weeks: int) -> List[str]:
        """Generate JavaScript-specific learning milestones"""
        if skill_level == 'beginner':
            base_milestones = [
                "Week 1: JavaScript Fundamentals and DOM Manipulation",
                "Week 2: Functions, Scope, and Closures",
                "Week 3: Arrays, Objects, and Data Manipulation", 
                "Week 4: Asynchronous JavaScript and Promises",
                "Week 5: ES6+ Features and Modern JavaScript",
                "Week 6: Working with APIs and Fetch"
            ]
        elif skill_level == 'intermediate':
            base_milestones = [
                "Week 1: Advanced JavaScript Patterns",
                "Week 2: Module Systems and Bundling",
                "Week 3: Testing JavaScript Applications",
                "Week 4: Performance Optimization"
            ]
        else:  # advanced
            base_milestones = [
                "Week 1: JavaScript Engine Internals",
                "Week 2: Advanced Async Patterns and Web Workers",
                "Week 3: Microservices and Serverless Architecture"
            ]
        
        # Add framework-specific milestones
        if 'react' in target_stack:
            base_milestones.extend([
                f"Week {len(base_milestones) + 1}: React Components and JSX",
                f"Week {len(base_milestones) + 2}: React State Management and Hooks",
                f"Week {len(base_milestones) + 3}: React Router and Navigation",
                f"Week {len(base_milestones) + 4}: React Testing and Deployment"
            ])
        elif 'vue' in target_stack:
            base_milestones.extend([
                f"Week {len(base_milestones) + 1}: Vue.js Components and Directives",
                f"Week {len(base_milestones) + 2}: Vue Router and Vuex State Management",
                f"Week {len(base_milestones) + 3}: Vue CLI and Build Tools"
            ])
        elif 'node' in target_stack:
            base_milestones.extend([
                f"Week {len(base_milestones) + 1}: Node.js Server Development",
                f"Week {len(base_milestones) + 2}: Express.js and Middleware",
                f"Week {len(base_milestones) + 3}: Database Integration with Node.js"
            ])
        
        return base_milestones
    
    def _generate_data_science_milestones(self, skill_level: str, target_stack: List[str], total_weeks: int) -> List[str]:
        """Generate Data Science-specific learning milestones"""
        if skill_level == 'beginner':
            return [
                "Week 1: Python for Data Science and Jupyter Notebooks",
                "Week 2: NumPy and Array Operations",
                "Week 3: Pandas for Data Manipulation",
                "Week 4: Data Visualization with Matplotlib and Seaborn",
                "Week 5: Statistical Analysis and Descriptive Statistics",
                "Week 6: Introduction to Machine Learning with Scikit-learn",
                "Week 7: Data Cleaning and Preprocessing",
                "Week 8: End-to-End Data Science Project"
            ]
        elif skill_level == 'intermediate':
            return [
                "Week 1: Advanced Pandas and Data Engineering",
                "Week 2: Feature Engineering and Selection",
                "Week 3: Machine Learning Algorithms Deep Dive",
                "Week 4: Model Evaluation and Hyperparameter Tuning",
                "Week 5: Time Series Analysis",
                "Week 6: Natural Language Processing Basics"
            ]
        else:  # advanced
            return [
                "Week 1: Deep Learning with TensorFlow/PyTorch",
                "Week 2: Advanced NLP and Computer Vision",
                "Week 3: MLOps and Model Deployment",
                "Week 4: Big Data Processing with Spark"
            ]
    
    def _generate_web_dev_milestones(self, skill_level: str, target_stack: List[str], total_weeks: int) -> List[str]:
        """Generate Web Development-specific learning milestones"""
        if skill_level == 'beginner':
            return [
                "Week 1: HTML5 Fundamentals and Semantic Markup",
                "Week 2: CSS3 Styling and Layout Techniques",
                "Week 3: Responsive Design and CSS Grid/Flexbox",
                "Week 4: JavaScript DOM Manipulation",
                "Week 5: Frontend Frameworks Introduction",
                "Week 6: Backend Development Basics",
                "Week 7: Database Integration",
                "Week 8: Full-Stack Project Development"
            ]
        elif skill_level == 'intermediate':
            return [
                "Week 1: Advanced CSS and Preprocessors",
                "Week 2: Modern JavaScript and ES6+",
                "Week 3: Frontend Build Tools and Bundlers",
                "Week 4: API Development and RESTful Services",
                "Week 5: Authentication and Security",
                "Week 6: Testing and Deployment"
            ]
        else:  # advanced
            return [
                "Week 1: Microservices Architecture",
                "Week 2: Performance Optimization and Caching",
                "Week 3: DevOps and CI/CD Pipelines",
                "Week 4: Scalability and Cloud Deployment"
            ]
    
    def _generate_java_milestones(self, skill_level: str, target_stack: List[str], total_weeks: int) -> List[str]:
        """Generate Java-specific learning milestones"""
        if skill_level == 'beginner':
            return [
                "Week 1: Java Environment Setup and Basic Syntax",
                "Week 2: Object-Oriented Programming in Java",
                "Week 3: Collections Framework and Generics",
                "Week 4: Exception Handling and File I/O",
                "Week 5: Multithreading and Concurrency",
                "Week 6: Java Streams and Lambda Expressions"
            ]
        elif skill_level == 'intermediate':
            return [
                "Week 1: Advanced Java Features and Design Patterns",
                "Week 2: Spring Framework Fundamentals",
                "Week 3: Spring Boot and Microservices",
                "Week 4: Database Integration with JPA/Hibernate"
            ]
        else:  # advanced
            return [
                "Week 1: Java Performance Tuning and JVM Optimization",
                "Week 2: Enterprise Java Patterns",
                "Week 3: Distributed Systems with Java"
            ]
    
    def _generate_generic_milestones(self, goal_topic: str, skill_level: str, total_weeks: int) -> List[str]:
        """Generate generic milestones for any topic"""
        milestones = []
        topic_name = goal_topic.replace(' for', '').replace(' with', '').strip()
        
        if skill_level == 'beginner':
            milestone_templates = [
                f"Week 1: {topic_name} Fundamentals and Environment Setup",
                f"Week 2: Core Concepts and Basic Operations",
                f"Week 3: Working with Data and Basic Algorithms",
                f"Week 4: Functions and Code Organization",
                f"Week 5: Working with Libraries and Frameworks",
                f"Week 6: Building Your First Project",
                f"Week 7: Testing and Debugging Techniques",
                f"Week 8: Best Practices and Next Steps"
            ]
        elif skill_level == 'intermediate':
            milestone_templates = [
                f"Week 1: Advanced {topic_name} Concepts",
                f"Week 2: Design Patterns and Architecture",
                f"Week 3: Performance Optimization",
                f"Week 4: Testing and Quality Assurance",
                f"Week 5: Integration and Deployment",
                f"Week 6: Capstone Project Development"
            ]
        else:  # advanced
            milestone_templates = [
                f"Week 1: Expert-Level {topic_name} Techniques",
                f"Week 2: System Design and Scalability",
                f"Week 3: Production Best Practices",
                f"Week 4: Leadership and Mentoring in {topic_name}"
            ]
        
        return milestone_templates
