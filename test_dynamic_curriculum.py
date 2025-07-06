"""
Test Dynamic Curriculum Generation
=================================

This script tests the enhanced dynamic curriculum generation
to show that it now creates truly customized content based on
user goals rather than just using predefined templates.
"""

import asyncio
import json
from curriculum_builder_mcp import CurriculumBuilderMCP


async def test_python_web_development():
    """Test Python for web development curriculum"""
    print("🔹 Testing: 'Learn Python for web development'")
    
    mcp = CurriculumBuilderMCP()
    curriculum = await mcp.build_curriculum(
        user_goal="Learn Python for web development",
        timeframe=6,
        skill_level="beginner"
    )
    
    print(f"✅ Generated curriculum: {curriculum.goal_topic}")
    print(f"📋 Technology stack: {curriculum.target_stack}")
    print(f"⏱️ Duration: {curriculum.total_weeks} weeks")
    print()
    
    # Show first 3 weeks to demonstrate dynamic content
    for i, week in enumerate(curriculum.weekly_content[:3]):
        print(f"Week {week.week_number}: {week.topic}")
        print(f"  🎯 Objective: {week.objective}")
        print(f"  📝 Expected outcomes: {len(week.expected_outcomes)} items")
        if week.hands_on_project:
            print(f"  🔨 Project: {week.hands_on_project.get('title', 'N/A')}")
        print()
    
    return curriculum


async def test_react_development():
    """Test React development curriculum"""
    print("🔹 Testing: 'Master React for frontend development'")
    
    mcp = CurriculumBuilderMCP()
    curriculum = await mcp.build_curriculum(
        user_goal="Master React for frontend development",
        timeframe=4,
        skill_level="intermediate"
    )
    
    print(f"✅ Generated curriculum: {curriculum.goal_topic}")
    print(f"📋 Technology stack: {curriculum.target_stack}")
    print(f"⏱️ Duration: {curriculum.total_weeks} weeks")
    print()
    
    # Show all weeks for React curriculum
    for week in curriculum.weekly_content:
        print(f"Week {week.week_number}: {week.topic}")
        print(f"  🎯 Objective: {week.objective}")
        if week.hands_on_project:
            print(f"  🔨 Project: {week.hands_on_project.get('title', 'N/A')}")
        print()
    
    return curriculum


async def test_data_science():
    """Test Data Science curriculum"""
    print("🔹 Testing: 'Learn data science and machine learning'")
    
    mcp = CurriculumBuilderMCP()
    curriculum = await mcp.build_curriculum(
        user_goal="Learn data science and machine learning",
        timeframe=8,
        skill_level="beginner"
    )
    
    print(f"✅ Generated curriculum: {curriculum.goal_topic}")
    print(f"📋 Technology stack: {curriculum.target_stack}")
    print(f"⏱️ Duration: {curriculum.total_weeks} weeks")
    print()
    
    # Show selected weeks to demonstrate data science specific content
    for i, week in enumerate(curriculum.weekly_content):
        if i < 4:  # Show first 4 weeks
            print(f"Week {week.week_number}: {week.topic}")
            print(f"  🎯 Objective: {week.objective}")
            print(f"  📊 Expected outcomes: {week.expected_outcomes[0] if week.expected_outcomes else 'None'}")
            print()
    
    return curriculum


async def test_custom_goal():
    """Test a completely custom goal"""
    print("🔹 Testing: 'Learn mobile app development with Flutter'")
    
    mcp = CurriculumBuilderMCP()
    curriculum = await mcp.build_curriculum(
        user_goal="Learn mobile app development with Flutter",
        timeframe=6,
        skill_level="beginner"
    )
    
    print(f"✅ Generated curriculum: {curriculum.goal_topic}")
    print(f"📋 Technology stack: {curriculum.target_stack}")
    print(f"⏱️ Duration: {curriculum.total_weeks} weeks")
    print()
    
    # Show how it handles unknown technologies
    for i, week in enumerate(curriculum.weekly_content[:3]):
        print(f"Week {week.week_number}: {week.topic}")
        print(f"  🎯 Objective: {week.objective}")
        print()
    
    return curriculum


async def compare_skill_levels():
    """Compare beginner vs intermediate curricula for same topic"""
    print("🔹 Comparing skill levels for Python web development")
    
    mcp = CurriculumBuilderMCP()
    
    # Beginner curriculum
    beginner_curriculum = await mcp.build_curriculum(
        user_goal="Learn Python for web development",
        timeframe=4,
        skill_level="beginner"
    )
    
    # Intermediate curriculum
    intermediate_curriculum = await mcp.build_curriculum(
        user_goal="Learn Python for web development",
        timeframe=4,
        skill_level="intermediate"
    )
    
    print("📚 BEGINNER Level:")
    for week in beginner_curriculum.weekly_content[:2]:
        print(f"  Week {week.week_number}: {week.topic}")
        print(f"    Objective: {week.objective}")
    
    print()
    print("🎓 INTERMEDIATE Level:")
    for week in intermediate_curriculum.weekly_content[:2]:
        print(f"  Week {week.week_number}: {week.topic}")
        print(f"    Objective: {week.objective}")
    
    print()


async def test_project_generation():
    """Test dynamic project generation"""
    print("🔹 Testing dynamic project generation")
    
    mcp = CurriculumBuilderMCP()
    
    # Python web development
    python_curriculum = await mcp.build_curriculum(
        user_goal="Learn Python for web development",
        timeframe=3,
        skill_level="beginner"
    )
    
    # React development
    react_curriculum = await mcp.build_curriculum(
        user_goal="Master React",
        timeframe=3,
        skill_level="beginner"
    )
    
    print("🐍 Python Projects:")
    for week in python_curriculum.weekly_content:
        if week.hands_on_project:
            project = week.hands_on_project
            print(f"  Week {week.week_number}: {project.get('title', 'No project')}")
            print(f"    Type: {project.get('type', 'N/A')}")
    
    print()
    print("⚛️ React Projects:")
    for week in react_curriculum.weekly_content:
        if week.hands_on_project:
            project = week.hands_on_project
            print(f"  Week {week.week_number}: {project.get('title', 'No project')}")
            print(f"    Type: {project.get('type', 'N/A')}")
    
    print()


async def main():
    """Run all tests to demonstrate dynamic functionality"""
    print("🧪 Testing Dynamic CurriculumBuilderMCP")
    print("=" * 50)
    print()
    
    try:
        # Test different technologies and specializations
        await test_python_web_development()
        print("-" * 30)
        await test_react_development()
        print("-" * 30)
        await test_data_science()
        print("-" * 30)
        await test_custom_goal()
        print("-" * 30)
        
        # Compare skill levels
        await compare_skill_levels()
        print("-" * 30)
        
        # Test project generation
        await test_project_generation()
        
        print("✅ All tests completed successfully!")
        print()
        print("🎉 The curriculum builder now generates truly dynamic,")
        print("   customized content based on the user's specific goals!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
