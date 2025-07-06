# 🎓 CurriculumBuilderMCP - Intelligent Learning Journey Orchestrator

An autonomous Modular Control Plane (MCP) agent that takes in a user's learning goal and outputs a structured **multi-week curriculum** with hands-on components.

## 🧩 Core Objective

Design an autonomous MCP agent that takes in a user's learning goal (e.g., "Learn Java", "Master React", "Get into AI/ML"), and outputs a structured **multi-week curriculum** including:

1. ✅ **Weekly topics** with specific learning objectives
2. 🔨 **Hands-on projects** or coding tasks  
3. 🎥 **Curated YouTube videos** and documentation links
4. ❓ **3–5 quiz questions** per week
5. 📤 **Export options** to Notion/Trello for tracking

## 🛠️ Architecture

The system uses **6 specialized sub-agents** orchestrated by the main CurriculumBuilderMCP:

### 1. 🎯 GoalAgent
- Parse the user's goal and timeframe (default: 4–8 weeks)
- Determine the skill level (beginner/intermediate/advanced)
- Output: goal_topic, target_stack, total_weeks, weekly_milestones

### 2. 📋 CurriculumPlannerAgent  
- Turn milestones into week-by-week topics
- For each week, generate topic, objective, expected outcomes

### 3. 🎥 VideoCuratorAgent
- Use YouTube API or search API to fetch 2–3 high-quality videos per topic
- Prioritize videos with high views, engagement, updated content
- Return titles + links + durations

### 4. 📚 DocFinderAgent
- Find relevant online documentation or blog posts
- Sources: MDN, freeCodeCamp, official docs, Dev.to, etc.

### 5. 🔨 HandsOnBuilderAgent
- Generate practical coding projects, exercises, and challenges
- Scale complexity based on skill level and week number
- Include starter code, requirements, and evaluation criteria

### 6. ❓ QuizGeneratorAgent
- Create 3–5 questions per week (multiple choice, coding, practical)
- Mix question types based on skill level
- Include answer keys and explanations

### 7. 📤 ExportAgent
- Export to multiple formats (JSON, Markdown, HTML, CSV)
- Push to Notion, Trello, or other project management tools
- Generate summary reports

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/krisalyndaphne/MCP.git
cd MCP

# Install dependencies
pip install -r curriculum_requirements.txt

# Optional: Set up API keys
export YOUTUBE_API_KEY="your_youtube_api_key"
export NOTION_TOKEN="your_notion_token"
```

### Basic Usage

```bash
# Generate a Python curriculum for beginners
python curriculum_builder_mcp.py "Learn Python for web development" --weeks 8 --skill-level beginner

# Generate an intermediate React curriculum
python curriculum_builder_mcp.py "Master React and Redux" --weeks 6 --skill-level intermediate --export markdown --output react_curriculum.md

# Export to Notion
python curriculum_builder_mcp.py "Learn Data Science" --notion-token YOUR_TOKEN --notion-database DATABASE_ID
```

### Python API Usage

```python
import asyncio
from curriculum_builder_mcp import CurriculumBuilderMCP

async def main():
    # Initialize the MCP
    mcp = CurriculumBuilderMCP()
    
    # Build curriculum
    curriculum = await mcp.build_curriculum(
        user_goal="Learn Python for data science",
        timeframe=8,
        skill_level="beginner"
    )
    
    # Export to markdown
    markdown_output = await mcp.export_curriculum(curriculum, 'markdown')
    print(markdown_output)
    
    # Push to Notion (optional)
    # await mcp.push_to_notion(curriculum, notion_token, database_id)

if __name__ == "__main__":
    asyncio.run(main())
```

## 📊 Example Output

For the goal "Learn Python for web development", the system generates:

```
Week 1: Python Fundamentals
├── 🎯 Objective: Learn Python syntax, variables, and basic data types  
├── 🎥 Videos: 3 curated YouTube tutorials
├── 📚 Docs: Official Python tutorial, Real Python guides
├── 🔨 Project: Build a simple calculator
└── ❓ Quiz: 5 questions on syntax and data types

Week 2: Control Structures and Functions  
├── 🎯 Objective: Master conditional statements, loops, and functions
├── 🎥 Videos: Function tutorials, best practices
├── 📚 Docs: Python function documentation  
├── 🔨 Project: Create a number guessing game
└── ❓ Quiz: 5 questions on control flow

[... continues for 8 weeks]
```

## 🔧 Configuration

### API Keys (Optional)

```bash
# YouTube API (for video curation)
export YOUTUBE_API_KEY="your_api_key"

# Notion Integration  
export NOTION_TOKEN="your_integration_token"

# Trello Integration
export TRELLO_KEY="your_trello_key"  
export TRELLO_TOKEN="your_trello_token"
```

### Custom Configuration

```python
config = {
    "default_weeks": 6,
    "hours_per_week": 8,
    "video_sources": ["youtube", "vimeo"],
    "export_formats": ["json", "markdown", "html"]
}

mcp = CurriculumBuilderMCP(config=config)
```

## 📤 Export Formats

### Supported Formats
- **JSON**: Structured data for programmatic use
- **Markdown**: Human-readable format for documentation  
- **HTML**: Styled web page with navigation
- **CSV**: Spreadsheet-compatible format
- **PDF**: Print-ready document (requires additional dependencies)

### Integration Platforms
- **Notion**: Create database entries with rich content
- **Trello**: Generate boards with cards for each week
- **GitHub**: Export as repository with README and files
- **Airtable**: Structured database records

## 🏗️ Project Structure

```
MCP/
├── curriculum_builder_mcp.py      # Main orchestrator
├── agents/                        # Specialized sub-agents
│   ├── __init__.py
│   ├── goal_agent.py             # Goal analysis
│   ├── curriculum_planner_agent.py # Curriculum structure  
│   ├── video_curator_agent.py     # Video curation
│   ├── doc_finder_agent.py        # Documentation finding
│   ├── hands_on_builder_agent.py  # Project generation
│   ├── quiz_generator_agent.py    # Quiz creation
│   └── export_agent.py            # Export and integration
├── curriculum_requirements.txt    # Dependencies
├── curriculum_README.md          # This file
└── examples/                     # Example outputs
    ├── python_beginner.json
    ├── react_intermediate.md
    └── data_science_advanced.html
```

## 🎯 Supported Learning Goals

### Programming Languages
- **Python**: Web development, data science, automation
- **JavaScript**: Frontend, backend, full-stack
- **Java**: Enterprise development, Android
- **C++**: Systems programming, game development
- **Go**: Backend services, cloud development

### Frameworks & Technologies  
- **Web**: React, Vue, Angular, Django, Flask
- **Mobile**: React Native, Flutter, Swift, Kotlin
- **Data**: Pandas, NumPy, TensorFlow, PyTorch
- **DevOps**: Docker, Kubernetes, AWS, CI/CD

### Skill Levels
- **Beginner**: No prior experience, focus on fundamentals
- **Intermediate**: Some experience, building practical skills  
- **Advanced**: Expert-level topics, architecture, best practices

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov-report=html

# Test specific agent
pytest tests/test_goal_agent.py -v
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Agents

```python
class NewAgent:
    async def process_task(self, input_data):
        # Implement agent logic
        return result

# Register in main orchestrator
self.new_agent = NewAgent()
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by modern educational platforms and personalized learning approaches
- Built with async Python for high performance and scalability
- Integrates with popular productivity tools for seamless workflow

## 📞 Support

- 📧 Email: support@curriculumbuilder.dev
- 🐛 Issues: [GitHub Issues](https://github.com/krisalyndaphne/MCP/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/krisalyndaphne/MCP/discussions)

---

**Made with ❤️ for learners everywhere** 🌟
