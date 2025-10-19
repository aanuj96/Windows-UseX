"""
Example demonstrating the Planner AI capabilities

This script shows how to use the Planner AI programmatically
without the interactive menu.
"""

from windows_use.llm.openrouter import ChatOpenRouter
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))
from main import PlannerAI

load_dotenv()

def example_complex_task():
    """Example: Complex multi-step task"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    # Initialize LLMs
    planner_llm = ChatOpenRouter(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        api_key=api_key,
        temperature=0.3
    )
    
    agent_llm = ChatOpenRouter(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        api_key=api_key,
        temperature=0.2
    )
    
    # Initialize Agent
    agent = Agent(
        llm=agent_llm,
        browser=Browser.EDGE,
        use_vision=False,
        auto_minimize=True,
        max_steps=25
    )
    
    # Initialize Planner
    planner = PlannerAI(llm=planner_llm, agent=agent)
    
    # Complex task example
    task = """
    Create a text file named 'meeting_notes.txt' on my Desktop with the following content:
    - Meeting Date: Today
    - Attendees: Team Members
    - Topics: Project Update, Budget Review
    """
    
    print("="*60)
    print("EXAMPLE: Complex Task with Planner AI")
    print("="*60)
    print(f"\nTask: {task}\n")
    
    # Execute the plan
    planner.execute_plan(task)


def example_simple_task():
    """Example: Simple single-step task"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    agent_llm = ChatOpenRouter(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        api_key=api_key,
        temperature=0.2
    )
    
    agent = Agent(
        llm=agent_llm,
        browser=Browser.EDGE,
        use_vision=False,
        auto_minimize=True
    )
    
    task = "Open Calculator application"
    
    print("="*60)
    print("EXAMPLE: Simple Task with Direct Agent")
    print("="*60)
    print(f"\nTask: {task}\n")
    
    # Execute directly
    result = agent.invoke(task)
    
    if result.error:
        print(f"❌ Error: {result.error}")
    else:
        print(f"✅ Success: {result.content}")


def example_plan_only():
    """Example: Generate plan without execution"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    planner_llm = ChatOpenRouter(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        api_key=api_key,
        temperature=0.3
    )
    
    # Create a dummy agent (won't be used for execution)
    agent_llm = ChatOpenRouter(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        api_key=api_key
    )
    agent = Agent(llm=agent_llm, browser=Browser.EDGE)
    
    planner = PlannerAI(llm=planner_llm, agent=agent)
    
    task = "Research Python pandas library and create a summary document"
    
    print("="*60)
    print("EXAMPLE: Generate Plan Only (No Execution)")
    print("="*60)
    print(f"\nTask: {task}\n")
    
    # Create and display plan only
    plan_data = planner.create_plan(task)
    planner.display_plan(plan_data)
    
    print("\nNote: This is just the plan. No execution performed.")


def main():
    print("\n" + "="*60)
    print("  PLANNER AI EXAMPLES")
    print("="*60 + "\n")
    
    print("Available examples:")
    print("1. Complex multi-step task (with Planner AI)")
    print("2. Simple single-step task (Direct Agent)")
    print("3. Generate plan only (no execution)")
    print("4. Run all examples")
    print()
    
    choice = input("Select an example (1-4): ").strip()
    
    if choice == "1":
        example_complex_task()
    elif choice == "2":
        example_simple_task()
    elif choice == "3":
        example_plan_only()
    elif choice == "4":
        print("\nRunning all examples...\n")
        example_plan_only()
        print("\n\n")
        # Uncomment to run other examples
        # example_simple_task()
        # print("\n\n")
        # example_complex_task()
    else:
        print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()

