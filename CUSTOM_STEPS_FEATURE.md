# ⚙️ Custom Max Steps Feature

## 🎯 What's New?

You can now **control how many iterations** each step gets before timing out!

### ✅ Fixed Issues:

1. **Mode 4 "max steps reached" error** - Now has unlimited mode
2. **Mode 3 custom steps** - You decide iteration limits
3. **Mode 1 custom steps** - Same control for step-by-step

---

## 🎮 How It Works

### Available in Modes 1, 3, and 4:

```
When you select Mode 1, 3, or 4, you'll see:

⚙️  Configuration:
Max iterations per step (press Enter for default 10, 0 for unlimited): 
```

**Your Options:**

- **Press Enter** → Use default (10 iterations per step)
- **Type a number** (e.g., "5", "20") → Use custom limit
- **Type "0"** → Unlimited mode (100 iterations max)

---

## 📊 What Are Iterations?

### Iteration = One Agent Reasoning Cycle

```
Step: "Open Notepad"

Iteration 1:
  📸 Capture desktop state
  💭 Think: "I need to open Start menu"
  🔧 Execute: Press Windows key
  🔭 Observe result

Iteration 2:
  📸 Capture desktop state
  💭 Think: "Start menu is open, now type Notepad"
  🔧 Execute: Type "Notepad"
  🔭 Observe result

Iteration 3:
  📸 Capture desktop state
  💭 Think: "Notepad in results, click it"
  🔧 Execute: Click Notepad
  🔭 Observe result

Iteration 4:
  📸 Capture desktop state
  💭 Think: "Notepad is now open, task complete"
  ✅ Use Done Tool

Total: 4 iterations to complete this step
```

---

## 🎯 Why Custom Steps Matter

### Problem: Default Limit Too Low

```
Task: "Create complex HTML file"
Step: "Type entire HTML code"

Default (10 iterations):
  Iteration 1-9: Typing code...
  Iteration 10: ❌ MAX STEPS REACHED
  
Result: Task incomplete! ❌
```

### Solution: Custom or Unlimited

```
With Custom (20 iterations):
  Iteration 1-15: Typing code...
  Iteration 16: ✅ Code complete, Done Tool
  
Result: Task completed! ✅

With Unlimited (0):
  Iterations 1-30: Complex operations...
  Iteration 31: ✅ Everything done
  
Result: No artificial limits! ✅
```

---

## 🎮 Usage Examples

### Example 1: Mode 1 with Custom Steps

```bash
python main.py

Select mode: 1
Enter task: Create HTML file with complex code

⚙️  Configuration:
Max iterations per step: 20
✅ Using 20 max iterations per step

[Planner creates plan]
[Each step gets 20 iterations to complete]
```

### Example 2: Mode 3 with Unlimited

```bash
python main.py

Select mode: 3
Enter task: Open app and configure settings

⚙️  Configuration:
Max iterations per step: 0
✅ Using unlimited mode (max 100 iterations per step)

[Planner creates plan]
[Each step has no practical limit]
[Can handle very complex operations]
```

### Example 3: Mode 4 Automatic Unlimited

```bash
python main.py

Select mode: 4
Enter task: Create and test HTML file

[Planner creates detailed plan]
Execute in one go? yes

⚙️  Mode 4: Using unlimited mode (max 100 iterations)
🚀 Executing entire plan...

[Agent executes all 15 steps successfully]
✅ Execution Complete!
```

---

## 📈 When to Use Each Setting

### Default (10 iterations) - Press Enter
```
✅ Good for:
  - Simple steps (1-3 actions)
  - Quick operations
  - Standard workflows
  - Most common tasks

❌ Not good for:
  - Complex multi-action steps
  - Long typing sequences
  - Complicated configurations
```

### Custom (5-50) - Type a number
```
✅ Good for:
  - You know task complexity
  - Want precise control
  - Optimizing performance
  - Specific requirements

Examples:
  5  → Very simple steps
  15 → Medium complexity
  30 → Complex operations
  50 → Very complex tasks
```

### Unlimited (0) - Type zero
```
✅ Good for:
  - Unknown complexity
  - Complex operations
  - Don't want limits
  - Testing/development
  - Mode 4 (auto-enabled)

⚠️  Note:
  - Still capped at 100 for safety
  - Prevents infinite loops
  - Agent usually completes sooner
```

---

## 🎯 Mode-Specific Behavior

### Mode 1: Step-by-Step Planner
```
Custom steps apply to: Each individual step
Example:
  Step 1: Gets N iterations
  Step 2: Gets N iterations
  Step 3: Gets N iterations
  
Use unlimited if: Any step might be complex
```

### Mode 3: Continuous
```
Custom steps apply to: Each step in each execution
Example:
  Execution 1:
    Step 1: Gets N iterations
    Step 2: Gets N iterations
  Execution 2:
    Step 1: Gets N iterations (same limit)
    Step 2: Gets N iterations (same limit)
    
Use unlimited if: Repeated complex operations
```

### Mode 4: Guided Single
```
Custom steps apply to: The entire task execution
Automatically: Sets to unlimited (100)
Example:
  Agent gets 100 iterations total
  To complete ALL steps
  
No user input needed: Mode 4 handles it
```

---

## 💡 Smart Defaults

### What We Recommend:

```
Task Complexity  → Recommended Setting
─────────────────────────────────────
Simple            → Default (10) or 5
Medium            → 15-20
Complex           → 30-50
Very Complex      → Unlimited (0)
Unknown           → Unlimited (0)
Mode 4            → Automatic (100)
```

---

## 🚨 Troubleshooting

### Issue: "Agent has reached maximum steps"

**Solution 1: Use Unlimited**
```
Max iterations per step: 0
✅ Using unlimited mode
```

**Solution 2: Increase Limit**
```
Max iterations per step: 30
✅ Using 30 max iterations
```

**Solution 3: Break Down Task**
```
Instead of: "Create entire complex app"
Try: Multiple simpler tasks
  - "Create HTML structure"
  - "Add CSS styling"  
  - "Add JavaScript"
```

### Issue: Steps completing too quickly

**Solution: Reduce iterations**
```
Max iterations per step: 5
✅ Faster execution for simple steps
```

### Issue: Task too slow

**Possible causes:**
1. Too many iterations allowed
2. Agent overthinking
3. Task complexity high

**Solution:**
- Use default (10) for simple tasks
- Increase only when needed
- Mode 4 for speed

---

## 📊 Performance Impact

### Iteration Limits and Speed:

```
Lower Limit (5):
  ✅ Faster (less overthinking)
  ❌ May timeout on complex steps

Default (10):
  ✅ Balanced
  ✅ Works for most tasks

Higher Limit (30-50):
  ❌ Slower (more iterations)
  ✅ Handles complex operations

Unlimited (100):
  ❌ Slowest if agent uses all
  ✅ Guaranteed completion
```

---

## 🎯 Real-World Examples

### Example 1: Simple File Creation

```
Task: Create text file with "hello"
Recommended: Default (10)

Why: Only needs 3-4 iterations
  1. Open Notepad
  2. Type text
  3. Save file
  4. Done
```

### Example 2: Complex HTML File

```
Task: Create HTML with 500 lines
Recommended: Unlimited (0)

Why: Needs many iterations
  - Open Notepad: 3 iterations
  - Type all code: 20-40 iterations
  - Save file: 3 iterations
  - Open browser: 3 iterations
  - Test: 2 iterations
Total: ~30-50 iterations needed
```

### Example 3: App Configuration

```
Task: Configure app with 10 settings
Recommended: 30-50

Why: Each setting needs multiple clicks
  - Navigate menus: 2-3 iterations each
  - Change settings: 1-2 iterations each
  - Verify changes: 1 iteration each
Total: ~30 iterations
```

---

## 💰 Cost Implications

### More Iterations = More API Calls

```
Iteration Count → Cost Impact
─────────────────────────────
Low (5)        → Cheapest
Default (10)   → Standard
High (30)      → More expensive
Unlimited      → Most expensive (if used)
```

**But:** Agent usually completes before hitting limit!

```
Unlimited (100 max):
  Agent typically uses: 10-30 iterations
  Rarely hits the 100 limit
  Only pays for what's used ✅
```

---

## 🎮 Interactive Configuration

### Mode 1 Example:

```
Select mode: 1
Enter task: Your task here

⚙️  Configuration:
Max iterations per step (press Enter for default 10, 0 for unlimited): 

Your choice:
  [Enter]    → 10 iterations per step
  5          → 5 iterations per step
  20         → 20 iterations per step
  0          → Unlimited (100 max)
```

### Mode 3 Example:

```
Select mode: 3
Enter task: Your task here

⚙️  Configuration:
Max iterations per step (press Enter for default 10, 0 for unlimited): 0
✅ Using unlimited mode (max 100 iterations per step)

[Plan displayed]

Execute? yes
[Each step execution uses unlimited mode]

Execute again? yes
[Still using same unlimited setting]
```

### Mode 4 - Automatic:

```
Select mode: 4
Enter task: Your task here

[Plan displayed]
Execute in one go? yes

⚙️  Mode 4: Using unlimited mode (max 100 iterations)
[No user input needed - automatically set]
```

---

## ✅ Summary

### What You Can Control:

```
Mode 1: ✅ Custom steps per action
Mode 2: ❌ Not applicable (direct execution)
Mode 3: ✅ Custom steps per action
Mode 4: ✅ Automatic unlimited (100)
```

### How to Choose:

```
1. Start with default (just press Enter)
2. If "max steps reached" → Use unlimited (0)
3. If want control → Use custom number
4. Mode 4 → No choice needed (automatic)
```

### Benefits:

```
✅ No more "max steps reached" errors
✅ Tasks can complete fully
✅ User control over execution
✅ Flexible for any task complexity
✅ Mode 4 optimized automatically
```

---

## 🚀 Try It Now!

```bash
python main.py

# Mode 1 or 3: You'll be asked for max steps
# Mode 4: Automatic unlimited

Test with unlimited (0) to see the difference!
```

---

**Version:** 1.5.0  
**Feature:** Custom Max Steps Control  
**Status:** ✅ Ready to use  
**Recommendation:** Use unlimited (0) when in doubt! 🚀

