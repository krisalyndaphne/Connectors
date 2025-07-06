"""
DocFinderAgent - Documentation and Article Discovery
===================================================

This agent finds relevant online documentation, tutorials,
and articles from trusted educational sources.
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
import logging
import re
from urllib.parse import quote

logger = logging.getLogger(__name__)


class DocFinderAgent:
    """
    Agent responsible for finding relevant documentation and articles.
    
    Searches through trusted educational sources to find high-quality
    written content that complements video learning.
    """
    
    def __init__(self):
        self.trusted_sources = {
            'programming': [
                'developer.mozilla.org',
                'docs.python.org',
                'www.freecodecamp.org',
                'realpython.com',
                'dev.to',
                'medium.com',
                'stackoverflow.com',
                'github.com',
                'w3schools.com',
                'tutorialspoint.com'
            ],
            'frameworks': [
                'reactjs.org',
                'vuejs.org',
                'angular.io',
                'flask.palletsprojects.com',
                'docs.djangoproject.com',
                'spring.io',
                'expressjs.com'
            ],
            'data_science': [
                'pandas.pydata.org',
                'scikit-learn.org',
                'tensorflow.org',
                'pytorch.org',
                'kaggle.com',
                'towardsdatascience.com'
            ]
        }
        
        # Pre-curated documentation for common topics
        self.curated_docs = {
            'python': {
                'beginner': [
                    {
                        'title': 'Python Tutorial - Official Documentation',
                        'url': 'https://docs.python.org/3/tutorial/',
                        'source': 'docs.python.org',
                        'type': 'Official Documentation',
                        'description': 'Comprehensive official Python tutorial covering all basics'
                    },
                    {
                        'title': 'Python Basics - Real Python',
                        'url': 'https://realpython.com/python-basics/',
                        'source': 'realpython.com',
                        'type': 'Tutorial Series',
                        'description': 'High-quality Python tutorials for beginners'
                    },
                    {
                        'title': 'Learn Python - freeCodeCamp',
                        'url': 'https://www.freecodecamp.org/learn/scientific-computing-with-python/',
                        'source': 'freecodecamp.org',
                        'type': 'Interactive Course',
                        'description': 'Free interactive Python course with projects'
                    }
                ]
            },
            'javascript': {
                'beginner': [
                    {
                        'title': 'JavaScript Guide - MDN',
                        'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
                        'source': 'developer.mozilla.org',
                        'type': 'Official Documentation',
                        'description': 'Comprehensive JavaScript guide from Mozilla'
                    },
                    {
                        'title': 'JavaScript Tutorial - W3Schools',
                        'url': 'https://www.w3schools.com/js/',
                        'source': 'w3schools.com',
                        'type': 'Tutorial',
                        'description': 'Interactive JavaScript tutorial with examples'
                    },
                    {
                        'title': 'Learn JavaScript - freeCodeCamp',
                        'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
                        'source': 'freecodecamp.org',
                        'type': 'Interactive Course',
                        'description': 'Free JavaScript course with algorithmic thinking'
                    }
                ]
            },
            'react': {
                'beginner': [
                    {
                        'title': 'React Documentation',
                        'url': 'https://reactjs.org/docs/getting-started.html',
                        'source': 'reactjs.org',
                        'type': 'Official Documentation',
                        'description': 'Official React documentation and guides'
                    },
                    {
                        'title': 'React Tutorial - Intro to React',
                        'url': 'https://reactjs.org/tutorial/tutorial.html',
                        'source': 'reactjs.org',
                        'type': 'Official Tutorial',
                        'description': 'Step-by-step React tutorial building a tic-tac-toe game'
                    }
                ]
            }
        }
        
        # Search patterns for different types of content
        self.search_patterns = {
            'documentation': ['{topic} documentation', '{topic} official docs', '{topic} reference'],
            'tutorials': ['{topic} tutorial', 'learn {topic}', '{topic} guide'],
            'examples': ['{topic} examples', '{topic} code samples', '{topic} projects'],
            'best_practices': ['{topic} best practices', '{topic} patterns', '{topic} tips']
        }
    
    async def find_documentation(self, topic: str, skill_level: str, num_docs: int = 3) -> List[Dict[str, str]]:
        """
        Find relevant documentation and articles for a topic.
        
        Args:
            topic: Learning topic (e.g., "Python Fundamentals")
            skill_level: beginner/intermediate/advanced
            num_docs: Number of documents to return
            
        Returns:
            List of documentation dictionaries
        """
        logger.info(f"📚 Finding documentation for topic: {topic} ({skill_level})")
        
        # Try curated docs first
        curated = self._get_curated_docs(topic, skill_level, num_docs)
        if curated:
            logger.info(f"📚 Found {len(curated)} curated documents")
            return curated
        
        # Generate generic docs
        docs = self._generate_generic_docs(topic, skill_level, num_docs)
        logger.info(f"📚 Generated {len(docs)} generic documentation links")
        return docs
    
    def _get_curated_docs(self, topic: str, skill_level: str, num_docs: int) -> List[Dict[str, str]]:
        """Get curated documentation from pre-defined sources"""
        topic_lower = topic.lower()
        
        # Try to match topic with available curated docs
        for tech in self.curated_docs:
            if tech in topic_lower:
                if skill_level in self.curated_docs[tech]:
                    return self.curated_docs[tech][skill_level][:num_docs]
        
        return []
    
    def _generate_generic_docs(self, topic: str, skill_level: str, num_docs: int) -> List[Dict[str, str]]:
        """Generate generic documentation recommendations"""
        docs = []
        topic_clean = self._clean_topic_name(topic)
        
        # Generate different types of documentation
        doc_types = ['documentation', 'tutorials', 'examples']
        if skill_level in ['intermediate', 'advanced']:
            doc_types.append('best_practices')
        
        for i, doc_type in enumerate(doc_types[:num_docs]):
            search_queries = self.search_patterns[doc_type]
            search_query = search_queries[0].format(topic=topic_clean)
            
            doc = {
                'title': self._generate_doc_title(topic_clean, doc_type, skill_level),
                'url': f"https://www.google.com/search?q={quote(search_query)}",
                'source': 'Search Results',
                'type': doc_type.replace('_', ' ').title(),
                'description': f"Search for {doc_type.replace('_', ' ')} related to {topic_clean}",
                'search_query': search_query
            }
            docs.append(doc)
        
        # Add specific trusted sources
        if len(docs) < num_docs:
            trusted_doc = self._generate_trusted_source_doc(topic_clean, skill_level)
            docs.append(trusted_doc)
        
        return docs[:num_docs]
    
    def _clean_topic_name(self, topic: str) -> str:
        """Clean topic name for better search results"""
        # Remove common words and clean up
        topic_clean = re.sub(r'\b(fundamentals|basics|introduction|advanced|intermediate)\b', '', topic, flags=re.IGNORECASE)
        topic_clean = re.sub(r'\s+', ' ', topic_clean).strip()
        return topic_clean
    
    def _generate_doc_title(self, topic: str, doc_type: str, skill_level: str) -> str:
        """Generate appropriate title for documentation link"""
        if doc_type == 'documentation':
            if skill_level == 'beginner':
                return f"{topic} - Getting Started Guide"
            else:
                return f"{topic} - Official Documentation"
        elif doc_type == 'tutorials':
            return f"Learn {topic} - Step-by-Step Tutorial"
        elif doc_type == 'examples':
            return f"{topic} Code Examples and Projects"
        elif doc_type == 'best_practices':
            return f"{topic} Best Practices and Patterns"
        else:
            return f"{topic} Learning Resources"
    
    def _generate_trusted_source_doc(self, topic: str, skill_level: str) -> Dict[str, str]:
        """Generate documentation link for a trusted source"""
        topic_lower = topic.lower()
        
        # Determine best trusted source based on topic
        if any(term in topic_lower for term in ['python', 'django', 'flask']):
            source = 'realpython.com'
            url = f"https://realpython.com/search?q={quote(topic)}"
        elif any(term in topic_lower for term in ['javascript', 'react', 'vue', 'angular', 'html', 'css']):
            source = 'developer.mozilla.org'
            url = f"https://developer.mozilla.org/en-US/search?q={quote(topic)}"
        elif any(term in topic_lower for term in ['data', 'machine learning', 'ai', 'pandas', 'numpy']):
            source = 'towardsdatascience.com'
            url = f"https://towardsdatascience.com/search?q={quote(topic)}"
        else:
            source = 'freecodecamp.org'
            url = f"https://www.freecodecamp.org/news/search/?query={quote(topic)}"
        
        return {
            'title': f"{topic} - {source}",
            'url': url,
            'source': source,
            'type': 'Trusted Source',
            'description': f"High-quality {topic} content from {source}"
        }
    
    async def validate_url(self, url: str) -> bool:
        """Validate if a URL is accessible"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except:
            return False
    
    def get_documentation_by_category(self, topic: str, category: str) -> List[Dict[str, str]]:
        """Get documentation filtered by category"""
        docs = []
        topic_clean = self._clean_topic_name(topic)
        
        if category in self.search_patterns:
            for pattern in self.search_patterns[category]:
                search_query = pattern.format(topic=topic_clean)
                doc = {
                    'title': self._generate_doc_title(topic_clean, category, 'general'),
                    'url': f"https://www.google.com/search?q={quote(search_query)}",
                    'source': 'Search Results',
                    'type': category.replace('_', ' ').title(),
                    'description': f"Search for {category.replace('_', ' ')} related to {topic_clean}",
                    'search_query': search_query
                }
                docs.append(doc)
        
        return docs
    
    def get_framework_docs(self, framework: str) -> List[Dict[str, str]]:
        """Get official documentation for specific frameworks"""
        framework_docs = {
            'react': {
                'title': 'React Documentation',
                'url': 'https://reactjs.org/docs/getting-started.html',
                'source': 'reactjs.org',
                'type': 'Official Documentation'
            },
            'vue': {
                'title': 'Vue.js Guide',
                'url': 'https://vuejs.org/guide/',
                'source': 'vuejs.org',
                'type': 'Official Documentation'
            },
            'angular': {
                'title': 'Angular Documentation',
                'url': 'https://angular.io/docs',
                'source': 'angular.io',
                'type': 'Official Documentation'
            },
            'django': {
                'title': 'Django Documentation',
                'url': 'https://docs.djangoproject.com/',
                'source': 'docs.djangoproject.com',
                'type': 'Official Documentation'
            },
            'flask': {
                'title': 'Flask Documentation',
                'url': 'https://flask.palletsprojects.com/',
                'source': 'flask.palletsprojects.com',
                'type': 'Official Documentation'
            }
        }
        
        framework_lower = framework.lower()
        if framework_lower in framework_docs:
            return [framework_docs[framework_lower]]
        else:
            return self._generate_generic_docs(framework, 'beginner', 1)
