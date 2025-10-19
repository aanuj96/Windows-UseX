# Planner AI - Usage Guide

## Overview

The **Planner AI Model** is an intelligent task orchestrator that breaks down complex user requests into step-by-step actions and coordinates their execution with the Action Agent.

## Architecture

```
User Query → Planner AI → Step-by-Step Plan → Action Agent (executes each step) → Results
```

### Components

1. **Planner AI**: Analyzes user queries and creates detailed execution plans
2. **Action Agent**: Executes individual steps using Windows automation tools
3. **Execution Monitor**: Tracks progress, handles errors, and provides feedback

## Features

### ✨ Key Features

- **Task Decomposition**: Automatically breaks down complex tasks into manageable steps
- **Sequential Execution**: Executes steps in logical order with context awareness
- **Error Handling**: Provides retry, skip, or abort options when steps fail
- **Progress Tracking**: Real-time monitoring of execution status
- **Execution Summary**: Detailed report of completed, failed, and skipped steps
- **Two Modes**: 
  - **Planner Mode**: For complex multi-step tasks
  - **Direct Mode**: For simple single-action tasks

### 🎯 How It Works

1. **Planning Phase**:
   - User provides a high-level task description
   - Planner AI analyzes the task
   - Creates a structured plan with:
     - Task summary
     - Step-by-step breakdown
     - Expected outcomes for each step
     - Complexity estimation

2. **Review Phase**:
   - Displays the complete plan to the user
   - Shows all steps and expected outcomes
   - Asks for confirmation before execution

3. **Execution Phase**:
   - Executes each step sequentially
   - Provides context from previous steps
   - Monitors for errors and handles failures
   - Displays real-time progress

4. **Summary Phase**:
   - Shows detailed execution report
   - Displays success/failure statistics
   - Provides results for each step

## Usage

### Running the Application

```bash
python main.py
```

### Mode Selection

When you run the application, you'll see:

```
🤖 Windows Use with Planner AI

Mode Selection:
  1. Use Planner AI (breaks down complex tasks into steps)
  2. Direct Agent Mode (single task execution)

Select mode (1 or 2): 
```

### Example Tasks

#### Complex Task (Use Planner AI - Mode 1)

```
Task: "Create a presentation about Python and save it to my Desktop"

Plan Generated:
1. Open PowerPoint application
2. Create a new blank presentation
3. Add title slide with "Python Programming" as title
4. Add content slides about Python features
5. Save the presentation to Desktop with name "Python.pptx"
6. Close PowerPoint
```

#### Simple Task (Use Direct Mode - Mode 2)

```
Task: "Open Chrome browser"
```

## Error Handling

When a step fails, you have three options:

- **Retry (r)**: Try the same step again
- **Skip (s)**: Skip the failed step and continue
- **Abort (a)**: Stop the entire execution

## Example Session

```
Select mode (1 or 2): 1
Enter your task: Send an email to john@example.com with subject "Meeting Reminder"

🧠 Planner AI: Analyzing task and creating plan...

╭─────────────── 📋 Execution Plan ───────────────╮
│ Task: Send an email with meeting reminder        │
│ Complexity: MODERATE                             │
│ Total Steps: 5                                   │
╰──────────────────────────────────────────────────╯

Step-by-Step Breakdown:

Step 1: Open default email client or web browser
  Expected: Email application launches

Step 2: Click on 'New Mail' or 'Compose' button
  Expected: New email composition window opens

Step 3: Enter recipient email address: john@example.com
  Expected: Recipient field populated

Step 4: Enter subject line: Meeting Reminder
  Expected: Subject field populated

Step 5: Click Send button
  Expected: Email sent successfully

🚀 Proceed with execution? (yes/no): yes

🚀 Starting Plan Execution...

============================================================
📍 Executing Step 1/5
Action: Open default email client or web browser
============================================================

[Agent execution details...]

✅ Step 1 Completed Successfully

[... continues for all steps ...]

============================================================
📊 Execution Summary
============================================================

Total Steps: 5
Successful: 5
Failed: 0
Success Rate: 100.0%

============================================================
```

## Configuration

### Planner LLM Settings

In `main.py`, you can adjust:

```python
planner_llm = ChatOpenRouter(
    model="mistralai/mistral-small-3.1-24b-instruct:free",
    api_key=api_key,
    temperature=0.3  # Higher for creative planning
)
```

### Agent Settings

```python
agent = Agent(
    llm=agent_llm,
    browser=Browser.EDGE,
    use_vision=False,
    auto_minimize=True,
    max_steps=25  # Max steps per individual action
)
```

## Benefits

### Why Use Planner AI?

1. **Complex Task Automation**: Handles multi-step workflows automatically
2. **Clear Visibility**: See the entire plan before execution
3. **Error Recovery**: Built-in error handling and retry mechanisms
4. **Context Awareness**: Each step knows what happened in previous steps
5. **Progress Tracking**: Real-time monitoring and detailed summaries
6. **Flexibility**: Switch between planner and direct modes as needed

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed task descriptions
2. **Complex Tasks**: Use Planner Mode (1) for multi-step operations
3. **Simple Tasks**: Use Direct Mode (2) for single actions
4. **Review Plans**: Always review the generated plan before execution
5. **Monitor Progress**: Watch the execution logs for any issues

## Troubleshooting

### Plan Not Generated Correctly

- Make sure your task description is clear and specific
- The Planner AI will create a simple fallback plan if JSON parsing fails

### Step Execution Fails

- Use the retry option to try again
- Check if the required application is installed
- Verify you have necessary permissions

### Agent Takes Too Long

- Adjust `max_steps` parameter in agent configuration
- Break down the task into smaller subtasks

## Future Enhancements

Potential improvements:

- Dynamic replanning based on execution results
- Parallel step execution for independent tasks
- Learning from execution history
- Vision integration for better context understanding
- Custom tool integration for domain-specific tasks

## API Reference

### PlannerAI Class

```python
class PlannerAI:
    def __init__(self, llm, agent: Agent)
    def create_plan(self, user_query: str) -> dict
    def display_plan(self, plan_data: dict)
    def execute_plan(self, user_query: str)
```

### Plan Data Structure

```json
{
  "task_summary": "Brief summary of the task",
  "steps": [
    {
      "step_number": 1,
      "description": "What to do in this step",
      "expected_outcome": "What should happen"
    }
  ],
  "estimated_complexity": "simple|moderate|complex"
}
```

## Support

For issues or questions:
- Check the execution logs for detailed error messages
- Review the plan structure to ensure steps are clear
- Try running in Direct Mode first to test basic functionality

