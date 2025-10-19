"""
Quick test script for Planner AI

This script runs a simple test to verify the Planner AI is working correctly.
"""

from windows_use.llm.openrouter import ChatOpenRouter
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from main import PlannerAI

load_dotenv()

def test_plan_generation():
    """Test if the planner can generate a plan"""
    
    print("="*60)
    print("TEST 1: Plan Generation")
    print("="*60)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenRouter API key")
        return False
    
    try:
        planner_llm = ChatOpenRouter(
            model="mistralai/mistral-small-3.1-24b-instruct:free",
            api_key=api_key,
            temperature=0.3
        )
        
        agent_llm = ChatOpenRouter(
            model="mistralai/mistral-small-3.1-24b-instruct:free",
            api_key=api_key
        )
        
        agent = Agent(llm=agent_llm, browser=Browser.EDGE)
        planner = PlannerAI(llm=planner_llm, agent=agent)
        
        # Simple test task
        task = "Open Notepad and type 'Hello World'"
        
        print(f"\nGenerating plan for: '{task}'")
        plan_data = planner.create_plan(task)
        
        print("\n✅ Plan generated successfully!")
        print(f"Task Summary: {plan_data['task_summary']}")
        print(f"Number of Steps: {len(plan_data['steps'])}")
        print(f"Complexity: {plan_data['estimated_complexity']}")
        
        print("\nSteps:")
        for step in plan_data['steps']:
            print(f"  {step['step_number']}. {step['description']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        return False


def test_agent_initialization():
    """Test if the agent initializes correctly"""
    
    print("\n" + "="*60)
    print("TEST 2: Agent Initialization")
    print("="*60)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not found")
        return False
    
    try:
        llm = ChatOpenRouter(
            model="mistralai/mistral-small-3.1-24b-instruct:free",
            api_key=api_key
        )
        
        agent = Agent(
            llm=llm,
            browser=Browser.EDGE,
            use_vision=False,
            auto_minimize=True,
            max_steps=25
        )
        
        print("\n✅ Agent initialized successfully!")
        print(f"Agent Name: {agent.name}")
        print(f"Description: {agent.description}")
        print(f"Max Steps: {agent.max_steps}")
        print(f"Browser: {agent.browser.value}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        return False


def test_llm_connection():
    """Test if LLM connection works"""
    
    print("\n" + "="*60)
    print("TEST 3: LLM Connection")
    print("="*60)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not found")
        return False
    
    try:
        from langchain_core.messages import HumanMessage
        
        llm = ChatOpenRouter(
            model="mistralai/mistral-small-3.1-24b-instruct:free",
            api_key=api_key
        )
        
        print("\nSending test message to LLM...")
        response = llm.invoke([HumanMessage(content="Say 'Hello' in one word.")])
        
        print(f"\n✅ LLM responded successfully!")
        print(f"Response: {response.content[:100]}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    
    print("\n" + "="*60)
    print("🧪 PLANNER AI - TEST SUITE")
    print("="*60)
    print("\nRunning tests to verify Planner AI installation...\n")
    
    tests = [
        ("LLM Connection", test_llm_connection),
        ("Agent Initialization", test_agent_initialization),
        ("Plan Generation", test_plan_generation),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Planner AI is ready to use.")
        print("\nRun 'python main.py' to start using the Planner AI!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("  - Make sure OPENROUTER_API_KEY is set in .env file")
        print("  - Check your internet connection")
        print("  - Verify all dependencies are installed")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    run_all_tests()

