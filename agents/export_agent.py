"""
ExportAgent - Curriculum Export and Integration
===============================================

This agent handles exporting curriculum to various formats
and integration with external tools like Notion, Trello, etc.
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
from dataclasses import asdict

logger = logging.getLogger(__name__)


class ExportAgent:
    """
    Agent responsible for exporting curriculum and integrating with external tools.
    
    Supports multiple export formats and can push curriculum data
    to project management and note-taking platforms.
    """
    
    def __init__(self):
        self.supported_formats = ['json', 'markdown', 'html', 'csv', 'pdf']
        self.integration_platforms = ['notion', 'trello', 'airtable', 'github']
        
    async def export(self, curriculum, export_format: str = 'json') -> str:
        """
        Export curriculum to specified format.
        
        Args:
            curriculum: CurriculumPlan object to export
            export_format: Target format (json, markdown, html, csv, pdf)
            
        Returns:
            Exported curriculum as string
        """
        logger.info(f"📤 Exporting curriculum to {export_format} format")
        
        if export_format not in self.supported_formats:
            raise ValueError(f"Unsupported export format: {export_format}")
        
        if export_format == 'json':
            return self._export_json(curriculum)
        elif export_format == 'markdown':
            return self._export_markdown(curriculum)
        elif export_format == 'html':
            return self._export_html(curriculum)
        elif export_format == 'csv':
            return self._export_csv(curriculum)
        elif export_format == 'pdf':
            return await self._export_pdf(curriculum)
        else:
            raise ValueError(f"Export format {export_format} not implemented")
    
    def _export_json(self, curriculum) -> str:
        """Export curriculum as JSON"""
        # Convert dataclass to dictionary
        curriculum_dict = asdict(curriculum)
        return json.dumps(curriculum_dict, indent=2, ensure_ascii=False)
    
    def _export_markdown(self, curriculum) -> str:
        """Export curriculum as Markdown"""
        md_content = []
        
        # Header
        md_content.append(f"# {curriculum.goal_topic} Learning Curriculum")
        md_content.append(f"*Created: {curriculum.created_at}*")
        md_content.append("")
        
        # Overview
        md_content.append("## 📋 Overview")
        md_content.append(f"- **Goal:** {curriculum.goal_topic}")
        md_content.append(f"- **Skill Level:** {curriculum.skill_level.title()}")
        md_content.append(f"- **Duration:** {curriculum.total_weeks} weeks")
        md_content.append(f"- **Time Commitment:** {curriculum.estimated_hours_per_week} hours/week")
        md_content.append("")
        
        # Technology Stack
        if curriculum.target_stack:
            md_content.append("## 🛠️ Technology Stack")
            for tech in curriculum.target_stack:
                md_content.append(f"- {tech}")
            md_content.append("")
        
        # Weekly Breakdown
        md_content.append("## 📅 Weekly Curriculum")
        
        for week in curriculum.weekly_content:
            md_content.append(f"### Week {week.week_number}: {week.topic}")
            md_content.append(f"**Objective:** {week.objective}")
            md_content.append("")
            
            # Expected Outcomes
            md_content.append("**Expected Outcomes:**")
            for outcome in week.expected_outcomes:
                md_content.append(f"- {outcome}")
            md_content.append("")
            
            # Videos
            if week.videos:
                md_content.append("**📺 Videos:**")
                for video in week.videos:
                    md_content.append(f"- [{video['title']}]({video['url']}) - {video.get('channel', 'Unknown')}")
                md_content.append("")
            
            # Documentation
            if week.documentation:
                md_content.append("**📚 Documentation:**")
                for doc in week.documentation:
                    md_content.append(f"- [{doc['title']}]({doc['url']}) - {doc.get('source', 'Unknown')}")
                md_content.append("")
            
            # Hands-on Project
            if week.hands_on_project:
                project = week.hands_on_project
                md_content.append("**🔨 Hands-On Project:**")
                md_content.append(f"- **Title:** {project.get('title', 'Project')}")
                md_content.append(f"- **Description:** {project.get('description', 'No description')}")
                md_content.append(f"- **Estimated Time:** {project.get('estimated_time', 'N/A')}")
                md_content.append("")
            
            # Quiz Questions
            if week.quiz_questions:
                md_content.append("**❓ Quiz Questions:**")
                for i, question in enumerate(week.quiz_questions, 1):
                    md_content.append(f"{i}. {question.get('question', 'Question not available')}")
                md_content.append("")
            
            md_content.append("---")
            md_content.append("")
        
        return "\\n".join(md_content)
    
    def _export_html(self, curriculum) -> str:
        """Export curriculum as HTML"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{curriculum.goal_topic} Learning Curriculum</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #2980b9;
            background: #ecf0f1;
            padding: 10px;
            border-left: 4px solid #3498db;
        }}
        .overview {{
            background: #e8f6ff;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .week-content {{
            border: 1px solid #ddd;
            margin: 20px 0;
            border-radius: 5px;
            overflow: hidden;
        }}
        .week-header {{
            background: #3498db;
            color: white;
            padding: 15px;
            font-weight: bold;
        }}
        .week-body {{
            padding: 20px;
        }}
        .resource-list {{
            list-style-type: none;
            padding: 0;
        }}
        .resource-list li {{
            background: #f8f9fa;
            margin: 5px 0;
            padding: 10px;
            border-left: 3px solid #28a745;
            border-radius: 3px;
        }}
        .project-box {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .quiz-box {{
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 {curriculum.goal_topic} Learning Curriculum</h1>
        <p><em>Created: {curriculum.created_at}</em></p>
        
        <div class="overview">
            <h2>📋 Overview</h2>
            <ul>
                <li><strong>Goal:</strong> {curriculum.goal_topic}</li>
                <li><strong>Skill Level:</strong> {curriculum.skill_level.title()}</li>
                <li><strong>Duration:</strong> {curriculum.total_weeks} weeks</li>
                <li><strong>Time Commitment:</strong> {curriculum.estimated_hours_per_week} hours/week</li>
            </ul>
        </div>
        
        {"<h2>🛠️ Technology Stack</h2><ul>" + "".join(f"<li>{tech}</li>" for tech in curriculum.target_stack) + "</ul>" if curriculum.target_stack else ""}
        
        <h2>📅 Weekly Curriculum</h2>
        """
        
        for week in curriculum.weekly_content:
            # Build week content
            week_html = f"""
        <div class="week-content">
            <div class="week-header">
                Week {week.week_number}: {week.topic}
            </div>
            <div class="week-body">
                <p><strong>Objective:</strong> {week.objective}</p>
                
                <h4>Expected Outcomes:</h4>
                <ul>
                    {"".join(f"<li>{outcome}</li>" for outcome in week.expected_outcomes)}
                </ul>"""
            
            # Add videos section
            if week.videos:
                video_items = "".join(f'<li><a href="{video["url"]}" target="_blank">{video["title"]}</a> - {video.get("channel", "Unknown")}</li>' for video in week.videos)
                week_html += f"""
                
                <h4>📺 Videos:</h4>
                <ul class="resource-list">
                    {video_items}
                </ul>"""
            
            # Add documentation section
            if week.documentation:
                doc_items = "".join(f'<li><a href="{doc["url"]}" target="_blank">{doc["title"]}</a> - {doc.get("source", "Unknown")}</li>' for doc in week.documentation)
                week_html += f"""
                
                <h4>📚 Documentation:</h4>
                <ul class="resource-list">
                    {doc_items}
                </ul>"""
            
            # Add project section
            if week.hands_on_project:
                week_html += f"""
                
                <div class="project-box">
                    <h4>🔨 Hands-On Project: {week.hands_on_project.get("title", "Project")}</h4>
                    <p>{week.hands_on_project.get("description", "No description")}</p>
                    <p><strong>Estimated Time:</strong> {week.hands_on_project.get("estimated_time", "N/A")}</p>
                </div>"""
            
            # Add quiz section
            if week.quiz_questions:
                quiz_items = "".join(f'<li>{question.get("question", "Question not available")}</li>' for question in week.quiz_questions)
                week_html += f"""
                
                <div class="quiz-box">
                    <h4>❓ Quiz Questions:</h4>
                    <ol>
                        {quiz_items}
                    </ol>
                </div>"""
            
            week_html += """
            </div>
        </div>"""
            
            html_content += week_html
        
        html_content += """
    </div>
</body>
</html>
        """
        
        return html_content
    
    def _export_csv(self, curriculum) -> str:
        """Export curriculum as CSV"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            'Week', 'Topic', 'Objective', 'Expected Outcomes', 
            'Videos', 'Documentation', 'Project', 'Quiz Questions'
        ])
        
        # Data rows
        for week in curriculum.weekly_content:
            videos = "; ".join([f"{v['title']} ({v['url']})" for v in week.videos])
            docs = "; ".join([f"{d['title']} ({d['url']})" for d in week.documentation])
            outcomes = "; ".join(week.expected_outcomes)
            project = f"{week.hands_on_project.get('title', '')} - {week.hands_on_project.get('description', '')}" if week.hands_on_project else ""
            quiz = "; ".join([q.get('question', '') for q in week.quiz_questions])
            
            writer.writerow([
                week.week_number,
                week.topic,
                week.objective,
                outcomes,
                videos,
                docs,
                project,
                quiz
            ])
        
        return output.getvalue()
    
    async def _export_pdf(self, curriculum) -> str:
        """Export curriculum as PDF (requires additional dependencies)"""
        # This would require libraries like reportlab or weasyprint
        # For now, return HTML that can be converted to PDF
        logger.warning("PDF export not fully implemented. Returning HTML for PDF conversion.")
        return self._export_html(curriculum)
    
    async def push_to_notion(self, curriculum, notion_token: str, database_id: str) -> bool:
        """
        Push curriculum to Notion database.
        
        Args:
            curriculum: CurriculumPlan object
            notion_token: Notion API token
            database_id: Target Notion database ID
            
        Returns:
            Success status
        """
        logger.info("📝 Pushing curriculum to Notion")
        
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Create a page for the curriculum
                page_data = {
                    "parent": {"database_id": database_id},
                    "properties": {
                        "Name": {
                            "title": [
                                {
                                    "text": {
                                        "content": f"{curriculum.goal_topic} Curriculum"
                                    }
                                }
                            ]
                        },
                        "Skill Level": {
                            "select": {
                                "name": curriculum.skill_level.title()
                            }
                        },
                        "Duration": {
                            "number": curriculum.total_weeks
                        },
                        "Created": {
                            "date": {
                                "start": curriculum.created_at.split('T')[0]
                            }
                        }
                    }
                }
                
                async with session.post(
                    "https://api.notion.com/v1/pages",
                    headers=headers,
                    json=page_data
                ) as response:
                    if response.status == 200:
                        page = await response.json()
                        page_id = page["id"]
                        
                        # Add curriculum content as blocks
                        await self._add_curriculum_blocks(session, headers, page_id, curriculum)
                        
                        logger.info("✅ Successfully pushed curriculum to Notion")
                        return True
                    else:
                        logger.error(f"Failed to create Notion page: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error pushing to Notion: {e}")
            return False
    
    async def _add_curriculum_blocks(self, session, headers: Dict, page_id: str, curriculum):
        """Add curriculum content as Notion blocks"""
        blocks = []
        
        # Add overview
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📋 Overview"}}]
            }
        })
        
        overview_text = f"Skill Level: {curriculum.skill_level.title()}\\nDuration: {curriculum.total_weeks} weeks\\nTime Commitment: {curriculum.estimated_hours_per_week} hours/week"
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": overview_text}}]
            }
        })
        
        # Add weekly content
        for week in curriculum.weekly_content:
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": f"Week {week.week_number}: {week.topic}"}}]
                }
            })
            
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"Objective: {week.objective}"}}]
                }
            })
        
        # Send blocks to Notion
        try:
            async with session.patch(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
                headers=headers,
                json={"children": blocks}
            ) as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Error adding blocks to Notion: {e}")
            return False
    
    async def push_to_trello(self, curriculum, trello_token: str, trello_key: str, board_id: str) -> bool:
        """
        Push curriculum to Trello board.
        
        Args:
            curriculum: CurriculumPlan object
            trello_token: Trello API token
            trello_key: Trello API key
            board_id: Target Trello board ID
            
        Returns:
            Success status
        """
        logger.info("📋 Pushing curriculum to Trello")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Create lists for each week
                for week in curriculum.weekly_content:
                    list_data = {
                        "name": f"Week {week.week_number}: {week.topic}",
                        "idBoard": board_id,
                        "key": trello_key,
                        "token": trello_token
                    }
                    
                    async with session.post(
                        "https://api.trello.com/1/lists",
                        data=list_data
                    ) as response:
                        if response.status == 200:
                            list_info = await response.json()
                            list_id = list_info["id"]
                            
                            # Create cards for resources
                            await self._create_trello_cards(session, trello_key, trello_token, list_id, week)
                
                logger.info("✅ Successfully pushed curriculum to Trello")
                return True
                
        except Exception as e:
            logger.error(f"Error pushing to Trello: {e}")
            return False
    
    async def _create_trello_cards(self, session, trello_key: str, trello_token: str, list_id: str, week):
        """Create Trello cards for week content"""
        # Create cards for videos, documentation, project, etc.
        if week.videos:
            for video in week.videos:
                card_data = {
                    "name": f"📺 {video['title']}",
                    "desc": f"Channel: {video.get('channel', 'Unknown')}\\nURL: {video['url']}",
                    "idList": list_id,
                    "key": trello_key,
                    "token": trello_token
                }
                
                await session.post("https://api.trello.com/1/cards", data=card_data)
        
        if week.hands_on_project:
            project = week.hands_on_project
            card_data = {
                "name": f"🔨 {project.get('title', 'Project')}",
                "desc": project.get('description', 'No description'),
                "idList": list_id,
                "key": trello_key,
                "token": trello_token
            }
            
            await session.post("https://api.trello.com/1/cards", data=card_data)
    
    def get_export_summary(self, curriculum) -> Dict[str, Any]:
        """Generate a summary of the curriculum for export"""
        return {
            "curriculum_title": f"{curriculum.goal_topic} Learning Curriculum",
            "total_weeks": curriculum.total_weeks,
            "skill_level": curriculum.skill_level,
            "total_videos": sum(len(week.videos) for week in curriculum.weekly_content),
            "total_documentation": sum(len(week.documentation) for week in curriculum.weekly_content),
            "total_projects": sum(1 for week in curriculum.weekly_content if week.hands_on_project),
            "total_quiz_questions": sum(len(week.quiz_questions) for week in curriculum.weekly_content),
            "estimated_total_hours": curriculum.total_weeks * curriculum.estimated_hours_per_week,
            "created_at": curriculum.created_at,
            "export_formats_available": self.supported_formats,
            "integration_platforms_supported": self.integration_platforms
        }
