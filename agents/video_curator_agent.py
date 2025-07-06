"""
VideoCuratorAgent - Video Content Curation
==========================================

This agent finds and curates high-quality educational videos
for each topic using YouTube API and other video platforms.
"""

import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any
import logging
import os
from urllib.parse import quote

logger = logging.getLogger(__name__)


class VideoCuratorAgent:
    """
    Agent responsible for finding and curating educational videos.
    
    Uses YouTube API and search algorithms to find high-quality
    educational content for each curriculum topic.
    """
    
    def __init__(self):
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.search_engines = [
            'youtube',
            'vimeo',
            'educational_platforms'
        ]
        
        # Quality criteria for video selection
        self.quality_criteria = {
            'min_views': 1000,
            'min_likes_ratio': 0.8,  # likes / (likes + dislikes)
            'max_duration': 3600,    # 1 hour max
            'min_duration': 300,     # 5 minutes min
            'preferred_channels': [
                'freeCodeCamp.org',
                'Programming with Mosh',
                'Traversy Media',
                'The Net Ninja',
                'Academind',
                'CS Dojo',
                'Corey Schafer',
                'sentdex',
                'TechWorld with Nana'
            ]
        }
        
        # Fallback video databases for when API is not available
        self.fallback_videos = {
            'python': {
                'beginner': [
                    {
                        'title': 'Python Tutorial - Python Full Course for Beginners',
                        'url': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc',
                        'duration': '4:26:52',
                        'channel': 'Programming with Mosh',
                        'views': '15M+',
                        'description': 'Complete Python tutorial for beginners covering all fundamentals'
                    },
                    {
                        'title': 'Learn Python - Full Course for Beginners [Tutorial]',
                        'url': 'https://www.youtube.com/watch?v=rfscVS0vtbw',
                        'duration': '4:20:19',
                        'channel': 'freeCodeCamp.org',
                        'views': '28M+',
                        'description': 'Comprehensive Python course from freeCodeCamp'
                    }
                ]
            },
            'javascript': {
                'beginner': [
                    {
                        'title': 'JavaScript Tutorial for Beginners: Learn JavaScript in 1 Hour',
                        'url': 'https://www.youtube.com/watch?v=W6NZfCO5SIk',
                        'duration': '1:00:00',
                        'channel': 'Programming with Mosh',
                        'views': '8M+',
                        'description': 'Quick and comprehensive JavaScript tutorial for beginners'
                    },
                    {
                        'title': 'Learn JavaScript - Full Course for Beginners',
                        'url': 'https://www.youtube.com/watch?v=PkZNo7MFNFg',
                        'duration': '3:26:42',
                        'channel': 'freeCodeCamp.org',
                        'views': '19M+',
                        'description': 'Complete JavaScript course covering all basics'
                    }
                ]
            }
        }
    
    async def curate_videos(self, topic: str, skill_level: str, num_videos: int = 3) -> List[Dict[str, str]]:
        """
        Curate high-quality educational videos for a specific topic.
        
        Args:
            topic: Learning topic (e.g., "Python Fundamentals")
            skill_level: beginner/intermediate/advanced
            num_videos: Number of videos to return
            
        Returns:
            List of curated video dictionaries
        """
        logger.info(f"🎥 Curating videos for topic: {topic} ({skill_level})")
        
        # Try YouTube API first
        if self.youtube_api_key:
            try:
                videos = await self._search_youtube_api(topic, skill_level, num_videos)
                if videos:
                    logger.info(f"🎥 Found {len(videos)} videos via YouTube API")
                    return videos
            except Exception as e:
                logger.warning(f"YouTube API search failed: {e}")
        
        # Fall back to curated video database
        videos = self._get_fallback_videos(topic, skill_level, num_videos)
        logger.info(f"🎥 Using {len(videos)} fallback videos")
        return videos
    
    async def _search_youtube_api(self, topic: str, skill_level: str, num_videos: int) -> List[Dict[str, str]]:
        """Search YouTube using the official API"""
        if not self.youtube_api_key:
            raise ValueError("YouTube API key not provided")
        
        # Construct search query
        search_query = self._build_search_query(topic, skill_level)
        
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': search_query,
            'type': 'video',
            'maxResults': num_videos * 3,  # Get more to filter
            'order': 'relevance',
            'videoDuration': 'medium',  # 4-20 minutes
            'key': self.youtube_api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    videos = await self._process_youtube_results(data, num_videos)
                    return videos
                else:
                    raise Exception(f"YouTube API returned {response.status}")
    
    async def _process_youtube_results(self, data: Dict, num_videos: int) -> List[Dict[str, str]]:
        """Process YouTube API results and filter for quality"""
        videos = []
        
        for item in data.get('items', []):
            video_info = {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'channel': item['snippet']['channelTitle'],
                'description': item['snippet']['description'][:200] + '...',
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'published': item['snippet']['publishedAt']
            }
            
            # Check if channel is in preferred list
            if any(pref in video_info['channel'] for pref in self.quality_criteria['preferred_channels']):
                video_info['quality_score'] = 10
            else:
                video_info['quality_score'] = 5
            
            videos.append(video_info)
        
        # Sort by quality score and return top videos
        videos.sort(key=lambda x: x['quality_score'], reverse=True)
        return videos[:num_videos]
    
    def _build_search_query(self, topic: str, skill_level: str) -> str:
        """Build an effective search query for the topic"""
        # Clean topic and add skill level modifiers
        base_query = topic.lower()
        
        if skill_level == 'beginner':
            modifiers = ['tutorial', 'beginners', 'learn', 'introduction']
        elif skill_level == 'intermediate':
            modifiers = ['course', 'guide', 'deep dive']
        else:  # advanced
            modifiers = ['advanced', 'masterclass', 'expert']
        
        # Combine base query with modifiers
        search_query = f"{base_query} {modifiers[0]} {modifiers[1]}"
        
        return search_query
    
    def _get_fallback_videos(self, topic: str, skill_level: str, num_videos: int) -> List[Dict[str, str]]:
        """Get curated videos from fallback database"""
        topic_lower = topic.lower()
        
        # Try to match topic with available fallback videos
        for tech, levels in self.fallback_videos.items():
            if tech in topic_lower:
                if skill_level in levels:
                    return levels[skill_level][:num_videos]
        
        # Generic fallback videos
        return self._generate_generic_videos(topic, skill_level, num_videos)
    
    def _generate_generic_videos(self, topic: str, skill_level: str, num_videos: int) -> List[Dict[str, str]]:
        """Generate generic video recommendations when no specific videos are available"""
        generic_videos = []
        
        for i in range(num_videos):
            if skill_level == 'beginner':
                title_templates = [
                    f"{topic} Tutorial for Beginners",
                    f"Learn {topic} - Complete Course",
                    f"{topic} Crash Course"
                ]
            elif skill_level == 'intermediate':
                title_templates = [
                    f"Advanced {topic} Course",
                    f"{topic} Deep Dive",
                    f"Mastering {topic}"
                ]
            else:  # advanced
                title_templates = [
                    f"Expert {topic} Techniques",
                    f"Professional {topic} Development",
                    f"{topic} Best Practices"
                ]
            
            video = {
                'title': title_templates[i % len(title_templates)],
                'url': f"https://www.youtube.com/results?search_query={quote(topic + ' tutorial')}",
                'channel': 'Search Results',
                'description': f"Search for high-quality {topic} tutorials on YouTube",
                'duration': 'Various',
                'note': 'Manual search required - curated videos not available for this topic'
            }
            generic_videos.append(video)
        
        return generic_videos
    
    async def get_video_details(self, video_url: str) -> Dict[str, Any]:
        """Get detailed information about a specific video"""
        # Extract video ID from URL
        video_id = self._extract_video_id(video_url)
        
        if self.youtube_api_key and video_id:
            return await self._get_youtube_video_details(video_id)
        else:
            return {'error': 'Unable to fetch video details'}
    
    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        import re
        
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    async def _get_youtube_video_details(self, video_id: str) -> Dict[str, Any]:
        """Get detailed video information from YouTube API"""
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            'part': 'snippet,statistics,contentDetails',
            'id': video_id,
            'key': self.youtube_api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['items']:
                        item = data['items'][0]
                        return {
                            'title': item['snippet']['title'],
                            'channel': item['snippet']['channelTitle'],
                            'duration': item['contentDetails']['duration'],
                            'views': item['statistics'].get('viewCount', 'N/A'),
                            'likes': item['statistics'].get('likeCount', 'N/A'),
                            'description': item['snippet']['description']
                        }
                
                return {'error': 'Video not found'}
