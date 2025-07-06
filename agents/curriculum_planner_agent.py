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
        """Generate dynamic curriculum template based on goal analysis"""
        
        # Generate curriculum based on actual goal and technology stack
        weekly_topics = self._generate_dynamic_curriculum(
            goal_topic, skill_level, total_weeks, target_stack
        )
        
        return weekly_topics
    
    def _generate_dynamic_curriculum(self, goal_topic: str, skill_level: str, 
                                   total_weeks: int, target_stack: List[str]) -> List[Dict[str, Any]]:
        """Generate dynamic curriculum based on goal analysis"""
        weekly_topics = []
        goal_lower = goal_topic.lower()
        
        # Technology-specific curriculum generation
        if any(tech in goal_lower for tech in ['python', 'django', 'flask']):
            weekly_topics = self._generate_python_curriculum(goal_topic, skill_level, total_weeks, target_stack)
        elif any(tech in goal_lower for tech in ['javascript', 'react', 'vue', 'angular', 'node']):
            weekly_topics = self._generate_javascript_curriculum(goal_topic, skill_level, total_weeks, target_stack)
        elif any(tech in goal_lower for tech in ['java', 'spring']):
            weekly_topics = self._generate_java_curriculum(goal_topic, skill_level, total_weeks, target_stack)
        elif any(tech in goal_lower for tech in ['data science', 'machine learning', 'ai', 'ml']):
            weekly_topics = self._generate_data_science_curriculum(goal_topic, skill_level, total_weeks, target_stack)
        elif any(tech in goal_lower for tech in ['web development', 'frontend', 'backend', 'fullstack']):
            weekly_topics = self._generate_web_development_curriculum(goal_topic, skill_level, total_weeks, target_stack)
        else:
            # Generate based on generic goal analysis
            weekly_topics = self._generate_goal_based_curriculum(goal_topic, skill_level, total_weeks, target_stack)
        
        return weekly_topics
    
    def _generate_python_curriculum(self, goal_topic: str, skill_level: str, 
                                  total_weeks: int, target_stack: List[str]) -> List[Dict[str, Any]]:
        """Generate Python-specific curriculum"""
        weeks = []
        
        # Determine if it's web development, data science, or general Python
        is_web_dev = any(term in goal_topic.lower() for term in ['web', 'django', 'flask', 'api'])
        is_data_science = any(term in goal_topic.lower() for term in ['data', 'science', 'analysis', 'machine learning'])
        
        if skill_level == 'beginner':
            base_weeks = [
                {
                    'topic': 'Python Environment and Syntax',
                    'objective': 'Set up Python development environment and learn basic syntax',
                    'expected_outcomes': [
                        'Install Python and set up development environment',
                        'Understand Python syntax and indentation',
                        'Write simple Python programs',
                        'Use Python REPL effectively'
                    ]
                },
                {
                    'topic': 'Variables and Data Types',
                    'objective': 'Master Python data types and variable manipulation',
                    'expected_outcomes': [
                        'Work with strings, numbers, and booleans',
                        'Understand type conversion and casting',
                        'Use string formatting and manipulation',
                        'Handle user input and output'
                    ]
                },
                {
                    'topic': 'Control Flow and Logic',
                    'objective': 'Implement conditional statements and loops',
                    'expected_outcomes': [
                        'Use if/elif/else statements effectively',
                        'Implement for and while loops',
                        'Understand loop control with break/continue',
                        'Apply logical operators and comparisons'
                    ]
                },
                {
                    'topic': 'Functions and Modules',
                    'objective': 'Create reusable code with functions and modules',
                    'expected_outcomes': [
                        'Define and call functions with parameters',
                        'Understand scope and return values',
                        'Import and use Python modules',
                        'Create your own modules'
                    ]
                },
                {
                    'topic': 'Data Structures',
                    'objective': 'Work with Python collections and data structures',
                    'expected_outcomes': [
                        'Manipulate lists, tuples, and sets',
                        'Use dictionaries for key-value storage',
                        'Apply list comprehensions',
                        'Choose appropriate data structures'
                    ]
                },
                {
                    'topic': 'File Handling and Error Management',
                    'objective': 'Handle files and manage errors gracefully',
                    'expected_outcomes': [
                        'Read and write files safely',
                        'Work with CSV and JSON data',
                        'Implement try/except error handling',
                        'Debug common Python errors'
                    ]
                }
            ]
            
            # Add specialized weeks based on focus area
            if is_web_dev:
                base_weeks.extend([
                    {
                        'topic': 'Web Development Foundations',
                        'objective': 'Introduction to web development concepts with Python',
                        'expected_outcomes': [
                            'Understand HTTP and web protocols',
                            'Learn about web frameworks',
                            'Set up a basic web server',
                            'Handle web requests and responses'
                        ]
                    },
                    {
                        'topic': 'Building Web Applications',
                        'objective': 'Create your first web application with Python',
                        'expected_outcomes': [
                            'Build a complete web application',
                            'Implement user authentication',
                            'Connect to a database',
                            'Deploy your application'
                        ]
                    }
                ])
            elif is_data_science:
                base_weeks.extend([
                    {
                        'topic': 'Data Science Libraries',
                        'objective': 'Introduction to NumPy and Pandas for data manipulation',
                        'expected_outcomes': [
                            'Work with NumPy arrays',
                            'Manipulate data with Pandas',
                            'Load and clean datasets',
                            'Perform basic data analysis'
                        ]
                    },
                    {
                        'topic': 'Data Visualization and Analysis',
                        'objective': 'Create visualizations and perform statistical analysis',
                        'expected_outcomes': [
                            'Create charts with Matplotlib',
                            'Build interactive visualizations',
                            'Perform statistical analysis',
                            'Present data insights'
                        ]
                    }
                ])
            else:
                # General Python path
                base_weeks.extend([
                    {
                        'topic': 'Object-Oriented Programming',
                        'objective': 'Learn OOP concepts and implement classes',
                        'expected_outcomes': [
                            'Define classes and create objects',
                            'Implement inheritance and polymorphism',
                            'Use encapsulation and abstraction',
                            'Apply OOP design principles'
                        ]
                    },
                    {
                        'topic': 'Advanced Python and Best Practices',
                        'objective': 'Master advanced Python features and coding standards',
                        'expected_outcomes': [
                            'Use decorators and generators',
                            'Implement context managers',
                            'Follow PEP 8 coding standards',
                            'Write maintainable Python code'
                        ]
                    }
                ])
        elif skill_level == 'intermediate':
            base_weeks = [
                {
                    'topic': 'Advanced Python Features',
                    'objective': 'Master advanced Python language features',
                    'expected_outcomes': [
                        'Use decorators and generators effectively',
                        'Implement context managers',
                        'Apply metaclasses and descriptors',
                        'Master advanced Python patterns'
                    ]
                },
                {
                    'topic': 'Object-Oriented Design Patterns',
                    'objective': 'Apply OOP design patterns in Python',
                    'expected_outcomes': [
                        'Implement common design patterns',
                        'Use inheritance and composition effectively',
                        'Apply SOLID principles',
                        'Design maintainable class hierarchies'
                    ]
                },
                {
                    'topic': 'Testing and Quality Assurance',
                    'objective': 'Implement comprehensive testing strategies',
                    'expected_outcomes': [
                        'Write unit tests with pytest',
                        'Implement integration testing',
                        'Use mocking and fixtures',
                        'Apply test-driven development'
                    ]
                },
                {
                    'topic': 'API Development and Integration',
                    'objective': 'Build and consume APIs with Python',
                    'expected_outcomes': [
                        'Create RESTful APIs with Flask/FastAPI',
                        'Handle HTTP requests and responses',
                        'Implement authentication and security',
                        'Integrate with third-party APIs'
                    ]
                }
            ]
        else:  # advanced
            base_weeks = [
                {
                    'topic': 'Python Performance Optimization',
                    'objective': 'Optimize Python applications for performance',
                    'expected_outcomes': [
                        'Profile and benchmark Python code',
                        'Implement caching strategies',
                        'Use asyncio for concurrent programming',
                        'Optimize memory usage and algorithms'
                    ]
                },
                {
                    'topic': 'Advanced Architecture Patterns',
                    'objective': 'Design scalable Python applications',
                    'expected_outcomes': [
                        'Implement microservices architecture',
                        'Use message queues and event-driven design',
                        'Apply hexagonal architecture',
                        'Design for scalability and maintainability'
                    ]
                }
            ]
        
        # Add framework-specific content for web development
        if is_web_dev and skill_level == 'intermediate':
            base_weeks.extend([
                {
                    'topic': 'Advanced Web Framework Development',
                    'objective': 'Master advanced web development with Python',
                    'expected_outcomes': [
                        'Build scalable web applications',
                        'Implement advanced authentication',
                        'Use database migrations and ORM',
                        'Deploy to production environments'
                    ]
                }
            ])
        elif is_data_science and skill_level == 'intermediate':
            base_weeks.extend([
                {
                    'topic': 'Advanced Data Science Techniques',
                    'objective': 'Apply advanced data science methods',
                    'expected_outcomes': [
                        'Implement advanced ML algorithms',
                        'Handle big data with Python',
                        'Create production ML pipelines',
                        'Deploy models to production'
                    ]
                }
            ])
        
        # Add week numbers and ensure we have the right number of weeks
        for i, week in enumerate(base_weeks[:total_weeks]):
            week['week_number'] = i + 1
            weeks.append(week)
        
        # Fill remaining weeks if needed
        while len(weeks) < total_weeks:
            weeks.append(self._generate_additional_week(goal_topic, skill_level, len(weeks) + 1))
        
        return weeks
    
    def _generate_javascript_curriculum(self, goal_topic: str, skill_level: str, 
                                      total_weeks: int, target_stack: List[str]) -> List[Dict[str, Any]]:
        """Generate JavaScript-specific curriculum"""
        weeks = []
        is_react = 'react' in target_stack or 'react' in goal_topic.lower()
        is_node = 'node' in target_stack or 'backend' in goal_topic.lower()
        
        base_weeks = []
        
        if skill_level == 'beginner':
            base_weeks = [
                {
                    'topic': 'JavaScript Fundamentals',
                    'objective': 'Master core JavaScript syntax and concepts',
                    'expected_outcomes': [
                        'Understand variables, data types, and operators',
                        'Write functions and understand scope',
                        'Use arrays and objects effectively',
                        'Handle basic DOM manipulation'
                    ]
                },
                {
                    'topic': 'Advanced Functions and Closures',
                    'objective': 'Deep dive into JavaScript functions and scope',
                    'expected_outcomes': [
                        'Create higher-order functions',
                        'Understand closures and lexical scope',
                        'Use arrow functions appropriately',
                        'Apply functional programming concepts'
                    ]
                },
                {
                    'topic': 'Asynchronous JavaScript',
                    'objective': 'Master promises, async/await, and API calls',
                    'expected_outcomes': [
                        'Handle asynchronous operations with promises',
                        'Use async/await syntax',
                        'Make HTTP requests with fetch',
                        'Handle errors in async code'
                    ]
                },
                {
                    'topic': 'Modern JavaScript (ES6+)',
                    'objective': 'Learn modern JavaScript features and syntax',
                    'expected_outcomes': [
                        'Use destructuring and spread operator',
                        'Understand modules and imports',
                        'Apply template literals and symbols',
                        'Use classes and inheritance'
                    ]
                }
            ]
        elif skill_level == 'intermediate':
            base_weeks = [
                {
                    'topic': 'Advanced JavaScript Patterns',
                    'objective': 'Master design patterns and advanced concepts',
                    'expected_outcomes': [
                        'Implement design patterns',
                        'Use advanced array methods',
                        'Understand prototype inheritance',
                        'Apply modular programming'
                    ]
                },
                {
                    'topic': 'Modern Development Workflow',
                    'objective': 'Use modern tools and build processes',
                    'expected_outcomes': [
                        'Configure webpack and bundlers',
                        'Use package managers effectively',
                        'Implement testing strategies',
                        'Set up development environments'
                    ]
                },
                {
                    'topic': 'Performance and Optimization',
                    'objective': 'Optimize JavaScript applications',
                    'expected_outcomes': [
                        'Profile and optimize code',
                        'Implement lazy loading',
                        'Use web workers',
                        'Optimize bundle sizes'
                    ]
                }
            ]
        else:  # advanced
            base_weeks = [
                {
                    'topic': 'JavaScript Engine Internals',
                    'objective': 'Understand how JavaScript engines work',
                    'expected_outcomes': [
                        'Understand V8 engine mechanics',
                        'Optimize for JIT compilation',
                        'Handle memory management',
                        'Debug performance issues'
                    ]
                }
            ]
        
        # Add framework-specific weeks based on focus
        if is_react:
            if skill_level == 'beginner':
                base_weeks.extend([
                    {
                        'topic': 'React Fundamentals',
                        'objective': 'Build your first React applications',
                        'expected_outcomes': [
                            'Create React components',
                            'Manage component state',
                            'Handle events in React',
                            'Understand props and data flow'
                        ]
                    },
                    {
                        'topic': 'React Hooks and State Management',
                        'objective': 'Master React hooks and complex state',
                        'expected_outcomes': [
                            'Use useState and useEffect hooks',
                            'Implement custom hooks',
                            'Manage complex application state',
                            'Handle side effects properly'
                        ]
                    }
                ])
            elif skill_level in ['intermediate', 'advanced']:
                base_weeks.extend([
                    {
                        'topic': 'Advanced React Patterns',
                        'objective': 'Master advanced React development patterns',
                        'expected_outcomes': [
                            'Implement compound components',
                            'Use render props and HOCs',
                            'Apply advanced hooks patterns',
                            'Optimize component performance'
                        ]
                    }
                ])
        elif is_node:
            base_weeks.extend([
                {
                    'topic': 'Node.js Fundamentals',
                    'objective': 'Build server-side applications with Node.js',
                    'expected_outcomes': [
                        'Set up Node.js development environment',
                        'Work with modules and npm',
                        'Handle file system operations',
                        'Create basic HTTP servers'
                    ]
                },
                {
                    'topic': 'Express.js and APIs',
                    'objective': 'Build RESTful APIs with Express.js',
                    'expected_outcomes': [
                        'Create Express.js applications',
                        'Build RESTful API endpoints',
                        'Handle middleware and routing',
                        'Connect to databases'
                    ]
                }
            ])
        elif skill_level == 'beginner':  # Only add DOM manipulation for beginners without React/Node
            base_weeks.extend([
                {
                    'topic': 'DOM Manipulation and Events',
                    'objective': 'Create interactive web pages',
                    'expected_outcomes': [
                        'Select and modify DOM elements',
                        'Handle user events effectively',
                        'Create dynamic content',
                        'Implement form validation'
                    ]
                },
                {
                    'topic': 'JavaScript Project Development',
                    'objective': 'Build a complete JavaScript application',
                    'expected_outcomes': [
                        'Plan and architect a JS project',
                        'Implement core functionality',
                        'Handle browser compatibility',
                        'Deploy your application'
                    ]
                }
            ])
        
        # Add week numbers
        for i, week in enumerate(base_weeks[:total_weeks]):
            week['week_number'] = i + 1
            weeks.append(week)
        
        while len(weeks) < total_weeks:
            weeks.append(self._generate_additional_week(goal_topic, skill_level, len(weeks) + 1))
        
        return weeks
    
    def _generate_data_science_curriculum(self, goal_topic: str, skill_level: str, 
                                        total_weeks: int, target_stack: List[str]) -> List[Dict[str, Any]]:
        """Generate Data Science-specific curriculum"""
        weeks = []
        
        if skill_level == 'beginner':
            base_weeks = [
                {
                    'topic': 'Data Science Environment Setup',
                    'objective': 'Set up Python environment for data science',
                    'expected_outcomes': [
                        'Install Anaconda and Jupyter',
                        'Understand data science workflow',
                        'Use Jupyter notebooks effectively',
                        'Basic Python for data science'
                    ]
                },
                {
                    'topic': 'NumPy and Array Operations',
                    'objective': 'Master numerical computing with NumPy',
                    'expected_outcomes': [
                        'Create and manipulate NumPy arrays',
                        'Perform mathematical operations',
                        'Handle array indexing and slicing',
                        'Use broadcasting and vectorization'
                    ]
                },
                {
                    'topic': 'Pandas for Data Manipulation',
                    'objective': 'Learn data manipulation with Pandas',
                    'expected_outcomes': [
                        'Work with DataFrames and Series',
                        'Load data from various sources',
                        'Clean and preprocess data',
                        'Perform data aggregation and grouping'
                    ]
                },
                {
                    'topic': 'Data Visualization',
                    'objective': 'Create compelling data visualizations',
                    'expected_outcomes': [
                        'Create plots with Matplotlib',
                        'Build statistical visualizations with Seaborn',
                        'Design effective data stories',
                        'Create interactive visualizations'
                    ]
                },
                {
                    'topic': 'Statistical Analysis',
                    'objective': 'Perform statistical analysis on data',
                    'expected_outcomes': [
                        'Calculate descriptive statistics',
                        'Perform hypothesis testing',
                        'Understand correlation and regression',
                        'Interpret statistical results'
                    ]
                },
                {
                    'topic': 'Introduction to Machine Learning',
                    'objective': 'Build your first machine learning models',
                    'expected_outcomes': [
                        'Understand ML concepts and terminology',
                        'Build classification and regression models',
                        'Evaluate model performance',
                        'Use scikit-learn effectively'
                    ]
                }
            ]
        
        # Add week numbers
        for i, week in enumerate(base_weeks[:total_weeks]):
            week['week_number'] = i + 1
            weeks.append(week)
        
        while len(weeks) < total_weeks:
            weeks.append(self._generate_additional_week(goal_topic, skill_level, len(weeks) + 1))
        
        return weeks
    
    def _generate_web_development_curriculum(self, goal_topic: str, skill_level: str, 
                                           total_weeks: int, target_stack: List[str]) -> List[Dict[str, Any]]:
        """Generate Web Development-specific curriculum"""
        weeks = []
        
        if skill_level == 'beginner':
            base_weeks = [
                {
                    'topic': 'HTML5 and Semantic Markup',
                    'objective': 'Master modern HTML structure and semantics',
                    'expected_outcomes': [
                        'Create well-structured HTML documents',
                        'Use semantic HTML5 elements',
                        'Implement forms and input validation',
                        'Understand accessibility principles'
                    ]
                },
                {
                    'topic': 'CSS3 and Responsive Design',
                    'objective': 'Style websites with modern CSS techniques',
                    'expected_outcomes': [
                        'Apply CSS selectors and properties',
                        'Use Flexbox and CSS Grid',
                        'Create responsive layouts',
                        'Implement animations and transitions'
                    ]
                },
                {
                    'topic': 'JavaScript for Web Development',
                    'objective': 'Add interactivity to web pages',
                    'expected_outcomes': [
                        'Manipulate DOM elements',
                        'Handle user events',
                        'Validate forms with JavaScript',
                        'Make AJAX requests'
                    ]
                },
                {
                    'topic': 'Frontend Build Tools',
                    'objective': 'Use modern development tools and workflows',
                    'expected_outcomes': [
                        'Set up development environment',
                        'Use package managers (npm/yarn)',
                        'Configure build tools',
                        'Optimize code for production'
                    ]
                }
            ]
        
        # Add week numbers
        for i, week in enumerate(base_weeks[:total_weeks]):
            week['week_number'] = i + 1
            weeks.append(week)
        
        while len(weeks) < total_weeks:
            weeks.append(self._generate_additional_week(goal_topic, skill_level, len(weeks) + 1))
        
        return weeks
    
    def _generate_java_curriculum(self, goal_topic: str, skill_level: str, 
                                total_weeks: int, target_stack: List[str]) -> List[Dict[str, Any]]:
        """Generate Java-specific curriculum"""
        weeks = []
        
        if skill_level == 'beginner':
            base_weeks = [
                {
                    'topic': 'Java Environment and Basics',
                    'objective': 'Set up Java development and learn syntax',
                    'expected_outcomes': [
                        'Install JDK and IDE setup',
                        'Understand Java syntax and structure',
                        'Compile and run Java programs',
                        'Use basic data types and variables'
                    ]
                },
                {
                    'topic': 'Object-Oriented Programming in Java',
                    'objective': 'Master Java OOP concepts',
                    'expected_outcomes': [
                        'Create classes and objects',
                        'Implement inheritance and polymorphism',
                        'Use interfaces and abstract classes',
                        'Apply encapsulation principles'
                    ]
                }
            ]
        
        # Add week numbers
        for i, week in enumerate(base_weeks[:total_weeks]):
            week['week_number'] = i + 1
            weeks.append(week)
        
        while len(weeks) < total_weeks:
            weeks.append(self._generate_additional_week(goal_topic, skill_level, len(weeks) + 1))
        
        return weeks
    
    def _generate_goal_based_curriculum(self, goal_topic: str, skill_level: str, 
                                      total_weeks: int, target_stack: List[str]) -> List[Dict[str, Any]]:
        """Generate curriculum based on generic goal analysis"""
        weeks = []
        topic_name = goal_topic.replace(' for', '').replace(' with', '').strip()
        
        base_weeks = [
            {
                'topic': f'{topic_name} Fundamentals',
                'objective': f'Learn the basics of {topic_name}',
                'expected_outcomes': [
                    f'Understand {topic_name} concepts',
                    'Set up development environment',
                    'Write your first programs',
                    'Follow best practices'
                ]
            },
            {
                'topic': f'Intermediate {topic_name}',
                'objective': f'Build practical skills in {topic_name}',
                'expected_outcomes': [
                    f'Apply {topic_name} to real problems',
                    'Use advanced features',
                    'Build small projects',
                    'Debug and troubleshoot'
                ]
            }
        ]
        
        # Add week numbers
        for i, week in enumerate(base_weeks[:total_weeks]):
            week['week_number'] = i + 1
            weeks.append(week)
        
        while len(weeks) < total_weeks:
            weeks.append(self._generate_additional_week(goal_topic, skill_level, len(weeks) + 1))
        
        return weeks
    
    def _generate_additional_week(self, goal_topic: str, skill_level: str, week_number: int) -> Dict[str, Any]:
        """Generate additional week content when template is insufficient"""
        if skill_level == 'beginner':
            return {
                'week_number': week_number,
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
                'week_number': week_number,
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
                'week_number': week_number,
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
