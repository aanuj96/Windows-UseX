# 🚀 Quick Start Guide - Planner AI

Get started with Planner AI in 5 minutes!

## Prerequisites

- Python 3.12+
- Windows OS
- OpenRouter API Key (or other LLM provider)

## Step 1: Setup Environment

```bash
# Clone or navigate to the project
cd Windows-Use

# Install dependencies (if not already installed)
pip install -r requirements.txt
# or
uv pip install windows-use
```

## Step 2: Configure API Key

Create a `.env` file in the project root:

```bash
OPENROUTER_API_KEY=your_api_key_here
```

Or use any other LLM provider (Gemini, Cerebras, etc.) - see README.md for examples.

## Step 3: Run Tests (Optional but Recommended)

Verify everything is set up correctly:

```bash
python test_planner.py
```

Expected output:
```
🧪 PLANNER AI - TEST SUITE
Running tests to verify Planner AI installation...

✅ PASS: LLM Connection
✅ PASS: Agent Initialization
✅ PASS: Plan Generation

Total: 3/3 tests passed
🎉 All tests passed! Planner AI is ready to use.
```

## Step 4: Run Your First Task

### Option A: Interactive Mode

```bash
python main.py
```

You'll see:
```
🤖 Windows Use with Planner AI

Mode Selection:
  1. Use Planner AI (breaks down complex tasks into steps)
  2. Direct Agent Mode (single task execution)

Select mode (1 or 2): 
```

### Option B: Using Examples

```bash
python planner_example.py
```

Choose from pre-built examples to see how it works.

## Example Tasks to Try

### Simple Tasks (Use Mode 2 - Direct Agent)

1. "Open Calculator"
2. "Open Chrome browser"
3. "Create a new folder on Desktop called 'Test'"

### Complex Tasks (Use Mode 1 - Planner AI)

1. "Create a text file named 'todo.txt' on Desktop with a list of 3 tasks"
2. "Open Notepad, write 'Hello World', and save to Desktop as hello.txt"
3. "Open Calculator and perform the calculation 25 + 37"

## Understanding the Output

### When Using Planner AI Mode:

**1. Plan Generation:**
```
🧠 Planner AI: Analyzing task and creating plan...

╭─────────────── 📋 Execution Plan ───────────────╮
│ Task: Create a text file on Desktop              │
│ Complexity: MODERATE                             │
│ Total Steps: 4                                   │
╰──────────────────────────────────────────────────╯
```

**2. Step Breakdown:**
```
Step 1: Open File Explorer
  Expected: File Explorer window opens

Step 2: Navigate to Desktop folder
  Expected: Desktop folder is displayed
```

**3. Execution Progress:**
```
============================================================
📍 Executing Step 1/4
Action: Open File Explorer
============================================================

Iteration: 1
📝 Evaluate: Need to open File Explorer
💭 Thought: I will use the app_tool to launch File Explorer
🔧 Action: app_tool(app_name='File Explorer')
🔭 Observation: File Explorer opened successfully

✅ Step 1 Completed Successfully
```

**4. Summary:**
```
============================================================
📊 Execution Summary
============================================================

Total Steps: 4
Successful: 4
Failed: 0
Success Rate: 100.0%
```

## Troubleshooting

### Issue: "API Key not found"
**Solution:** Make sure your `.env` file exists and contains the correct API key.

### Issue: "Agent takes too long"
**Solution:** 
- Try using a faster model
- Reduce `max_steps` in the agent configuration
- Use Direct Mode for simple tasks

### Issue: "Step execution fails"
**Solution:**
- Use the retry option (press 'r')
- Make sure the required application is installed
- Check if you have necessary permissions

### Issue: "Plan is not detailed enough"
**Solution:**
- Provide more specific task descriptions
- Break down very complex tasks into smaller queries
- Adjust the Planner LLM temperature for more creativity

## Tips for Success

### Writing Good Task Descriptions

✅ **Good:**
- "Open Notepad, type 'Meeting at 3 PM', and save to Desktop as reminder.txt"
- "Create a new folder named 'Projects' on Desktop"
- "Open Calculator and calculate 150 divided by 3"

❌ **Bad:**
- "Do something with files" (too vague)
- "Make it work" (unclear)
- "Fix my computer" (too broad)

### When to Use Each Mode

**Use Planner AI (Mode 1) when:**
- Task has multiple steps
- Steps depend on each other
- You want to review the plan first
- Task involves different applications

**Use Direct Agent (Mode 2) when:**
- Single, simple action
- Quick task execution needed
- You know exactly what needs to be done

## Advanced Usage

### Programmatic Use

```python
from windows_use.llm.openrouter import ChatOpenRouter
from windows_use.agent import Agent, Browser
from main import PlannerAI
import os

# Setup
api_key = os.getenv("OPENROUTER_API_KEY")
planner_llm = ChatOpenRouter(model="...", api_key=api_key)
agent_llm = ChatOpenRouter(model="...", api_key=api_key)
agent = Agent(llm=agent_llm, browser=Browser.EDGE)
planner = PlannerAI(llm=planner_llm, agent=agent)

# Execute
planner.execute_plan("Your task here")
```

### Generate Plan Only (No Execution)

```python
# Just create the plan
plan_data = planner.create_plan("Your task here")
planner.display_plan(plan_data)
# No execution happens
```

### Custom Configuration

```python
# Use different models for planning vs execution
planner_llm = ChatOpenRouter(
    model="openai/gpt-4o",  # Smarter model for planning
    temperature=0.4
)

agent_llm = ChatOpenRouter(
    model="mistralai/mistral-small",  # Faster model for execution
    temperature=0.1
)

# Adjust agent settings
agent = Agent(
    llm=agent_llm,
    browser=Browser.CHROME,  # Use Chrome instead of Edge
    use_vision=True,  # Enable vision capabilities
    auto_minimize=True,  # Auto-minimize IDE
    max_steps=50  # Allow more steps per action
)
```

## Next Steps

1. ✅ Run `test_planner.py` to verify setup
2. ✅ Try a simple task with Direct Mode
3. ✅ Try a complex task with Planner AI
4. ✅ Read [PLANNER_GUIDE.md](PLANNER_GUIDE.md) for detailed documentation
5. ✅ Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
6. ✅ Experiment with different tasks and configurations

## Resources

- **Full Documentation:** [PLANNER_GUIDE.md](PLANNER_GUIDE.md)
- **Architecture Details:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Example Scripts:** [planner_example.py](planner_example.py)
- **Test Suite:** [test_planner.py](test_planner.py)
- **Main README:** [README.md](README.md)

## Getting Help

1. Check the troubleshooting section above
2. Review the execution logs for error details
3. Try running tests: `python test_planner.py`
4. Read the full documentation in PLANNER_GUIDE.md
5. Check if your API key is valid and has credits

## Common Patterns

### Pattern 1: File Creation
```
Task: "Create a text file called notes.txt on Desktop"

Plan:
1. Open File Explorer
2. Navigate to Desktop
3. Create new text file
4. Rename to notes.txt
```

### Pattern 2: Application Workflow
```
Task: "Open Calculator and calculate 25 * 8"

Plan:
1. Launch Calculator app
2. Input number 25
3. Click multiply button
4. Input number 8
5. Click equals button
```

### Pattern 3: Multi-App Workflow
```
Task: "Copy text from Notepad to a new Word document"

Plan:
1. Open Notepad
2. Type the text
3. Select all and copy
4. Open Word
5. Create new document
6. Paste text
7. Save document
```

## Performance Tips

1. **Use appropriate models:** Faster models for simple tasks, smarter models for complex planning
2. **Enable auto_minimize:** Prevents interference from IDE
3. **Adjust max_steps:** Lower for quick tasks, higher for complex workflows
4. **Batch tasks:** Run related tasks together instead of separately
5. **Monitor execution:** Watch the logs to understand what's happening

---

**Ready to start? Run:** `python main.py`

Have fun automating your Windows tasks! 🎉

