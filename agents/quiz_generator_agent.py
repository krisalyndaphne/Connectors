"""
QuizGeneratorAgent - Quiz and Assessment Generation
==================================================

This agent generates quiz questions and assessments
to test understanding of each curriculum topic.
"""

import asyncio
from typing import Dict, List, Optional, Any
import logging
import random

logger = logging.getLogger(__name__)


class QuizGeneratorAgent:
    """
    Agent responsible for generating quiz questions and assessments.
    
    Creates multiple choice, coding, and practical questions
    to test understanding and reinforce learning.
    """
    
    def __init__(self):
        self.question_templates = {
            'python': {
                'beginner': [
                    {
                        'type': 'multiple_choice',
                        'question': 'What is the correct way to define a function in Python?',
                        'options': [
                            'def my_function():',
                            'function my_function():',
                            'define my_function():',
                            'func my_function():'
                        ],
                        'correct_answer': 0,
                        'explanation': 'In Python, functions are defined using the "def" keyword followed by the function name and parentheses.',
                        'difficulty': 'easy',
                        'topic': 'Functions'
                    },
                    {
                        'type': 'coding',
                        'question': 'Write a function that takes a list of numbers and returns the sum of all even numbers.',
                        'starter_code': 'def sum_even_numbers(numbers):\n    # Your code here\n    pass',
                        'expected_output': 'For input [1, 2, 3, 4, 5, 6], should return 12',
                        'test_cases': [
                            {'input': [1, 2, 3, 4, 5, 6], 'expected': 12},
                            {'input': [1, 3, 5], 'expected': 0},
                            {'input': [2, 4, 6, 8], 'expected': 20}
                        ],
                        'difficulty': 'medium',
                        'topic': 'Lists and Functions'
                    }
                ]
            },
            'javascript': {
                'beginner': [
                    {
                        'type': 'multiple_choice',
                        'question': 'Which method is used to add an element to the end of an array in JavaScript?',
                        'options': [
                            'append()',
                            'push()',
                            'add()',
                            'insert()'
                        ],
                        'correct_answer': 1,
                        'explanation': 'The push() method adds one or more elements to the end of an array and returns the new length of the array.',
                        'difficulty': 'easy',
                        'topic': 'Arrays'
                    },
                    {
                        'type': 'coding',
                        'question': 'Create a function that validates if an email address is in a basic valid format.',
                        'starter_code': 'function isValidEmail(email) {\n    // Your code here\n}',
                        'expected_output': 'Should return true for valid emails, false for invalid ones',
                        'test_cases': [
                            {'input': 'test@example.com', 'expected': True},
                            {'input': 'invalid.email', 'expected': False},
                            {'input': 'user@domain.co.uk', 'expected': True}
                        ],
                        'difficulty': 'medium',
                        'topic': 'String Validation'
                    }
                ]
            }
        }
        
        self.question_types = [
            'multiple_choice',
            'true_false',
            'short_answer',
            'coding',
            'practical'
        ]
        
        self.difficulty_levels = ['easy', 'medium', 'hard']
        
        # Generic question templates for any topic
        self.generic_templates = {
            'multiple_choice': [
                'What is the primary purpose of {concept}?',
                'Which of the following best describes {concept}?',
                'What happens when you {action} in {topic}?',
                'Which {item} is most commonly used for {purpose}?'
            ],
            'true_false': [
                '{statement} is always true in {topic}.',
                'You can {action} without {requirement} in {topic}.',
                '{concept} is only used for {specific_purpose}.'
            ],
            'short_answer': [
                'Explain the difference between {concept1} and {concept2}.',
                'What are the main benefits of using {concept}?',
                'Describe when you would use {technique} in {topic}.',
                'List three important considerations when {action}.'
            ],
            'coding': [
                'Write a function that {task} using {topic} concepts.',
                'Implement {algorithm} for {specific_use_case}.',
                'Create a {program_type} that demonstrates {concept}.',
                'Fix the bug in this {topic} code snippet.'
            ]
        }
    
    async def generate_quiz(self, topic: str, skill_level: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """
        Generate quiz questions for a specific topic and skill level.
        
        Args:
            topic: Learning topic (e.g., "Python Fundamentals")
            skill_level: beginner/intermediate/advanced
            num_questions: Number of questions to generate
            
        Returns:
            List of quiz question dictionaries
        """
        logger.info(f"❓ Generating quiz for topic: {topic} ({skill_level})")
        
        questions = []
        
        # Try to get specific questions first
        specific_questions = self._get_specific_questions(topic, skill_level)
        questions.extend(specific_questions)
        
        # Generate additional generic questions if needed
        while len(questions) < num_questions:
            generic_question = self._generate_generic_question(topic, skill_level)
            questions.append(generic_question)
        
        # Shuffle and return requested number of questions
        random.shuffle(questions)
        final_questions = questions[:num_questions]
        
        # Add metadata
        for i, question in enumerate(final_questions):
            question['question_number'] = i + 1
            question['points'] = self._get_question_points(question['type'], question.get('difficulty', 'medium'))
        
        logger.info(f"❓ Generated {len(final_questions)} quiz questions")
        return final_questions
    
    def _get_specific_questions(self, topic: str, skill_level: str) -> List[Dict[str, Any]]:
        """Get pre-defined questions for specific topics"""
        topic_lower = topic.lower()
        questions = []
        
        # Look for matching topic in templates
        for tech in self.question_templates:
            if tech in topic_lower:
                if skill_level in self.question_templates[tech]:
                    questions = self.question_templates[tech][skill_level].copy()
                    break
        
        return questions
    
    def _generate_generic_question(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a generic question for any topic"""
        question_type = random.choice(self.question_types)
        
        if question_type == 'multiple_choice':
            return self._generate_multiple_choice(topic, skill_level)
        elif question_type == 'true_false':
            return self._generate_true_false(topic, skill_level)
        elif question_type == 'short_answer':
            return self._generate_short_answer(topic, skill_level)
        elif question_type == 'coding':
            return self._generate_coding_question(topic, skill_level)
        else:  # practical
            return self._generate_practical_question(topic, skill_level)
    
    def _generate_multiple_choice(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a multiple choice question"""
        topic_clean = self._clean_topic_name(topic)
        
        # Generate question based on skill level
        if skill_level == 'beginner':
            question_templates = [
                f'What is the basic syntax for {topic_clean}?',
                f'Which statement is true about {topic_clean}?',
                f'What is the purpose of {topic_clean}?'
            ]
        elif skill_level == 'intermediate':
            question_templates = [
                f'What is the best practice when working with {topic_clean}?',
                f'Which approach is most efficient for {topic_clean}?',
                f'What are the limitations of {topic_clean}?'
            ]
        else:  # advanced
            question_templates = [
                f'How would you optimize {topic_clean} for large-scale applications?',
                f'What are the advanced features of {topic_clean}?',
                f'How does {topic_clean} compare to alternative approaches?'
            ]
        
        question = random.choice(question_templates)
        
        return {
            'type': 'multiple_choice',
            'question': question,
            'options': self._generate_realistic_options(topic_clean, skill_level),
            'correct_answer': 0,  # First option is correct by default
            'explanation': f'This tests understanding of {topic_clean} concepts at {skill_level} level.',
            'difficulty': self._get_difficulty_for_level(skill_level),
            'topic': topic_clean
        }
    
    def _generate_true_false(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a true/false question"""
        topic_clean = self._clean_topic_name(topic)
        
        statements = [
            f'{topic_clean} is essential for modern development',
            f'You must always use {topic_clean} in professional projects',
            f'{topic_clean} has no performance implications',
            f'Learning {topic_clean} requires advanced programming knowledge'
        ]
        
        statement = random.choice(statements)
        is_true = random.choice([True, False])
        
        return {
            'type': 'true_false',
            'question': f'True or False: {statement}',
            'correct_answer': is_true,
            'explanation': f'This statement about {topic_clean} is {"true" if is_true else "false"} based on standard practices.',
            'difficulty': 'easy',
            'topic': topic_clean
        }
    
    def _generate_short_answer(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a short answer question"""
        topic_clean = self._clean_topic_name(topic)
        
        question_templates = [
            f'Explain the key benefits of using {topic_clean}.',
            f'Describe a practical use case for {topic_clean}.',
            f'What are the main challenges when learning {topic_clean}?',
            f'How does {topic_clean} improve code quality?'
        ]
        
        question = random.choice(question_templates)
        
        return {
            'type': 'short_answer',
            'question': question,
            'sample_answer': f'A comprehensive answer should discuss the practical applications and benefits of {topic_clean}.',
            'key_points': [
                f'Understanding of {topic_clean} fundamentals',
                'Practical application knowledge',
                'Awareness of best practices',
                'Recognition of common challenges'
            ],
            'difficulty': self._get_difficulty_for_level(skill_level),
            'topic': topic_clean
        }
    
    def _generate_coding_question(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a coding question"""
        topic_clean = self._clean_topic_name(topic)
        
        if skill_level == 'beginner':
            tasks = [
                'create a simple function',
                'implement basic logic',
                'process user input',
                'display formatted output'
            ]
        elif skill_level == 'intermediate':
            tasks = [
                'implement an algorithm',
                'create a reusable class',
                'handle error conditions',
                'optimize performance'
            ]
        else:  # advanced
            tasks = [
                'design a scalable solution',
                'implement design patterns',
                'create efficient algorithms',
                'build robust error handling'
            ]
        
        task = random.choice(tasks)
        
        return {
            'type': 'coding',
            'question': f'Write code that will {task} related to {topic_clean}.',
            'starter_code': f'# {topic_clean} coding challenge\n# {task.capitalize()}\n\ndef solution():\n    # Your code here\n    pass',
            'expected_output': f'Code should demonstrate understanding of {topic_clean} concepts.',
            'evaluation_criteria': [
                'Correct implementation',
                'Code readability',
                'Proper use of concepts',
                'Error handling (if applicable)'
            ],
            'difficulty': self._get_difficulty_for_level(skill_level),
            'topic': topic_clean
        }
    
    def _generate_practical_question(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Generate a practical application question"""
        topic_clean = self._clean_topic_name(topic)
        
        scenarios = [
            'building a web application',
            'solving a business problem',
            'optimizing system performance',
            'implementing user requirements'
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            'type': 'practical',
            'question': f'You are {scenario}. How would you apply {topic_clean} concepts to achieve the best results?',
            'scenario_details': f'Consider a real-world situation where {topic_clean} knowledge is essential.',
            'evaluation_points': [
                'Understanding of practical applications',
                'Knowledge of best practices',
                'Problem-solving approach',
                'Consideration of constraints and requirements'
            ],
            'difficulty': self._get_difficulty_for_level(skill_level),
            'topic': topic_clean
        }
    
    def _generate_realistic_options(self, topic: str, skill_level: str) -> List[str]:
        """Generate realistic multiple choice options"""
        # This is a simplified version - in a real implementation,
        # you would have more sophisticated option generation
        return [
            f'Correct approach for {topic}',
            f'Common misconception about {topic}',
            f'Outdated method for {topic}',
            f'Unrelated concept to {topic}'
        ]
    
    def _clean_topic_name(self, topic: str) -> str:
        """Clean topic name for better question generation"""
        return topic.replace(' Fundamentals', '').replace(' Basics', '').replace(' Introduction', '').strip()
    
    def _get_difficulty_for_level(self, skill_level: str) -> str:
        """Map skill level to difficulty"""
        mapping = {
            'beginner': 'easy',
            'intermediate': 'medium',
            'advanced': 'hard'
        }
        return mapping.get(skill_level, 'medium')
    
    def _get_question_points(self, question_type: str, difficulty: str) -> int:
        """Calculate points for a question based on type and difficulty"""
        base_points = {
            'multiple_choice': 2,
            'true_false': 1,
            'short_answer': 3,
            'coding': 5,
            'practical': 4
        }
        
        multiplier = {
            'easy': 1,
            'medium': 1.5,
            'hard': 2
        }
        
        return int(base_points.get(question_type, 2) * multiplier.get(difficulty, 1))
    
    def generate_quiz_metadata(self, questions: List[Dict[str, Any]], topic: str) -> Dict[str, Any]:
        """Generate metadata for the entire quiz"""
        total_points = sum(q.get('points', 0) for q in questions)
        question_types = list(set(q['type'] for q in questions))
        difficulties = list(set(q.get('difficulty', 'medium') for q in questions))
        
        return {
            'quiz_title': f'{topic} Assessment Quiz',
            'total_questions': len(questions),
            'total_points': total_points,
            'question_types': question_types,
            'difficulty_levels': difficulties,
            'estimated_time': f'{len(questions) * 3} minutes',
            'passing_score': int(total_points * 0.7),  # 70% to pass
            'instructions': [
                'Read each question carefully',
                'Choose the best answer for multiple choice questions',
                'Write clear, concise answers for short answer questions',
                'Test your code before submitting coding questions'
            ]
        }
    
    def create_answer_key(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create an answer key for the quiz"""
        answer_key = {}
        
        for i, question in enumerate(questions, 1):
            key = f'question_{i}'
            
            if question['type'] == 'multiple_choice':
                answer_key[key] = {
                    'correct_answer': question['correct_answer'],
                    'explanation': question.get('explanation', '')
                }
            elif question['type'] == 'true_false':
                answer_key[key] = {
                    'correct_answer': question['correct_answer'],
                    'explanation': question.get('explanation', '')
                }
            elif question['type'] in ['short_answer', 'coding', 'practical']:
                answer_key[key] = {
                    'sample_answer': question.get('sample_answer', ''),
                    'key_points': question.get('key_points', []),
                    'evaluation_criteria': question.get('evaluation_criteria', [])
                }
        
        return answer_key
