"""
Example Usage of CurriculumBuilderMCP
====================================

This script demonstrates how to use the CurriculumBuilderMCP system
to generate custom learning curricula.
"""

import asyncio
import json
from curriculum_builder_mcp import CurriculumBuilderMCP


async def example_python_curriculum():
    """Generate a Python curriculum for beginners"""
    print("🚀 Generating Python curriculum for beginners...")
    
    # Initialize the MCP
    mcp = CurriculumBuilderMCP()
    
    # Build curriculum
    curriculum = await mcp.build_curriculum(
        user_goal="Learn Python for web development",
        timeframe=6,
        skill_level="beginner"
    )
    
    # Export to different formats
    print("\n📤 Exporting curriculum...")
    
    # Export to JSON
    json_output = await mcp.export_curriculum(curriculum, 'json')
    with open('python_curriculum.json', 'w', encoding='utf-8') as f:
        f.write(json_output)
    print("✅ Saved to python_curriculum.json")
    
    # Export to Markdown
    markdown_output = await mcp.export_curriculum(curriculum, 'markdown')
    with open('python_curriculum.md', 'w', encoding='utf-8') as f:
        f.write(markdown_output)
    print("✅ Saved to python_curriculum.md")
    
    # Export to HTML
    html_output = await mcp.export_curriculum(curriculum, 'html')
    with open('python_curriculum.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    print("✅ Saved to python_curriculum.html")
    
    return curriculum


async def example_javascript_curriculum():
    """Generate a JavaScript curriculum for intermediate learners"""
    print("\n🚀 Generating JavaScript curriculum for intermediate learners...")
    
    mcp = CurriculumBuilderMCP()
    
    curriculum = await mcp.build_curriculum(
        user_goal="Master React and Redux for frontend development",
        timeframe=4,
        skill_level="intermediate"
    )
    
    # Print summary
    print(f"\n📋 Curriculum Summary:")
    print(f"Topic: {curriculum.goal_topic}")
    print(f"Duration: {curriculum.total_weeks} weeks")
    print(f"Skill Level: {curriculum.skill_level}")
    print(f"Weekly Time: {curriculum.estimated_hours_per_week} hours")
    
    return curriculum


async def example_data_science_curriculum():
    """Generate a Data Science curriculum for advanced learners"""
    print("\n🚀 Generating Data Science curriculum for advanced learners...")
    
    mcp = CurriculumBuilderMCP()
    
    curriculum = await mcp.build_curriculum(
        user_goal="Advanced machine learning and AI development",
        timeframe=8,
        skill_level="advanced"
    )
    
    # Show weekly breakdown
    print(f"\n📅 Weekly Breakdown:")
    for week in curriculum.weekly_content:
        print(f"Week {week.week_number}: {week.topic}")
        print(f"  🎯 {week.objective}")
        print(f"  📺 {len(week.videos)} videos")
        print(f"  📚 {len(week.documentation)} docs")
        print(f"  🔨 Project: {week.hands_on_project.get('title', 'N/A') if week.hands_on_project else 'None'}")
        print(f"  ❓ {len(week.quiz_questions)} quiz questions")
        print()
    
    return curriculum


async def demonstrate_export_features():
    """Demonstrate various export and integration features"""
    print("\n🔧 Demonstrating export features...")
    
    mcp = CurriculumBuilderMCP()
    
    # Generate a quick curriculum
    curriculum = await mcp.build_curriculum(
        user_goal="Learn web development basics",
        timeframe=4,
        skill_level="beginner"
    )
    
    # Get export summary
    summary = mcp.export_agent.get_export_summary(curriculum)
    print(f"\n📊 Export Summary:")
    print(json.dumps(summary, indent=2))
    
    # Demonstrate CSV export
    csv_output = await mcp.export_curriculum(curriculum, 'csv')
    with open('curriculum_summary.csv', 'w', encoding='utf-8') as f:
        f.write(csv_output)
    print("✅ CSV export saved to curriculum_summary.csv")


async def main():
    """Main demonstration function"""
    print("🎓 CurriculumBuilderMCP Demonstration")
    print("=" * 50)
    
    try:
        # Generate different types of curricula
        python_curriculum = await example_python_curriculum()
        js_curriculum = await example_javascript_curriculum()
        ds_curriculum = await example_data_science_curriculum()
        
        # Demonstrate export features
        await demonstrate_export_features()
        
        print("\n✅ All examples completed successfully!")
        print("\nGenerated files:")
        print("- python_curriculum.json")
        print("- python_curriculum.md") 
        print("- python_curriculum.html")
        print("- curriculum_summary.csv")
        
        print("\n🎉 CurriculumBuilderMCP demonstration complete!")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("This might be due to missing dependencies or API keys.")
        print("The system will still work with fallback content.")


if __name__ == "__main__":
    asyncio.run(main())
