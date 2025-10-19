# 🎨 Planner AI - Visual Guide

## System Flow Diagram

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                  ┃
┃                    USER PROVIDES TASK                            ┃
┃          "Create a presentation and save to Desktop"             ┃
┃                                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                          │
                          ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                     PLANNER AI                                   ┃
┃  ┌────────────────────────────────────────────────────────┐     ┃
┃  │ 🧠 ANALYZING TASK...                                   │     ┃
┃  │                                                         │     ┃
┃  │ • Understanding requirements                           │     ┃
┃  │ • Identifying applications needed                      │     ┃
┃  │ • Breaking down into logical steps                     │     ┃
┃  │ • Estimating complexity                                │     ┃
┃  └────────────────────────────────────────────────────────┘     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                          │
                          ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    EXECUTION PLAN                                ┃
┃  ╔════════════════════════════════════════════════════════╗     ┃
┃  ║ 📋 TASK: Create PowerPoint presentation               ║     ┃
┃  ║ 🎯 COMPLEXITY: Moderate                                ║     ┃
┃  ║ 📊 TOTAL STEPS: 6                                      ║     ┃
┃  ╠════════════════════════════════════════════════════════╣     ┃
┃  ║                                                         ║     ┃
┃  ║ Step 1: Open PowerPoint application                   ║     ┃
┃  ║   ↳ Expected: PowerPoint launches                     ║     ┃
┃  ║                                                         ║     ┃
┃  ║ Step 2: Create new blank presentation                 ║     ┃
┃  ║   ↳ Expected: New presentation created                ║     ┃
┃  ║                                                         ║     ┃
┃  ║ Step 3: Add title slide                               ║     ┃
┃  ║   ↳ Expected: Title slide added                       ║     ┃
┃  ║                                                         ║     ┃
┃  ║ Step 4: Add content slides                            ║     ┃
┃  ║   ↳ Expected: Content slides created                  ║     ┃
┃  ║                                                         ║     ┃
┃  ║ Step 5: Save to Desktop as "Presentation.pptx"        ║     ┃
┃  ║   ↳ Expected: File saved successfully                 ║     ┃
┃  ║                                                         ║     ┃
┃  ║ Step 6: Close PowerPoint                              ║     ┃
┃  ║   ↳ Expected: Application closed                      ║     ┃
┃  ║                                                         ║     ┃
┃  ╚════════════════════════════════════════════════════════╝     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                          │
                          ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    USER APPROVAL                                 ┃
┃                                                                  ┃
┃       🚀 Proceed with execution? (yes/no):  yes                 ┃
┃                                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                          │
                          ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                 STEP-BY-STEP EXECUTION                           ┃
┃                                                                  ┃
┃  ┌──────────────────────────────────────────────────────────┐  ┃
┃  │ 📍 STEP 1/6: Open PowerPoint application                 │  ┃
┃  │                                                           │  ┃
┃  │   ACTION AGENT WORKING...                                │  ┃
┃  │   ├─ 📝 Evaluate: Need to launch PowerPoint             │  ┃
┃  │   ├─ 💭 Thought: Use app_tool to open PowerPoint        │  ┃
┃  │   ├─ 🔧 Action: app_tool(app_name='PowerPoint')         │  ┃
┃  │   └─ 🔭 Observation: PowerPoint opened successfully     │  ┃
┃  │                                                           │  ┃
┃  │   ✅ Step 1 Completed Successfully                       │  ┃
┃  └──────────────────────────────────────────────────────────┘  ┃
┃                                                                  ┃
┃  ┌──────────────────────────────────────────────────────────┐  ┃
┃  │ 📍 STEP 2/6: Create new blank presentation               │  ┃
┃  │                                                           │  ┃
┃  │   ACTION AGENT WORKING...                                │  ┃
┃  │   ├─ 📝 Evaluate: Blank presentation needed             │  ┃
┃  │   ├─ 💭 Thought: Click on 'Blank Presentation'          │  ┃
┃  │   ├─ 🔧 Action: click_tool(element='Blank Presentation') │  ┃
┃  │   └─ 🔭 Observation: New presentation created           │  ┃
┃  │                                                           │  ┃
┃  │   ✅ Step 2 Completed Successfully                       │  ┃
┃  └──────────────────────────────────────────────────────────┘  ┃
┃                                                                  ┃
┃  ... (Steps 3-6 continue similarly) ...                         ┃
┃                                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                          │
                          ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    EXECUTION SUMMARY                             ┃
┃  ╔════════════════════════════════════════════════════════╗     ┃
┃  ║ 📊 RESULTS                                             ║     ┃
┃  ╠════════════════════════════════════════════════════════╣     ┃
┃  ║                                                         ║     ┃
┃  ║ Total Steps:      6                                    ║     ┃
┃  ║ Successful:       6  ✅                                ║     ┃
┃  ║ Failed:           0  ❌                                ║     ┃
┃  ║ Success Rate:     100.0%                               ║     ┃
┃  ║                                                         ║     ┃
┃  ╠════════════════════════════════════════════════════════╣     ┃
┃  ║ DETAILED RESULTS                                       ║     ┃
┃  ╠════════════════════════════════════════════════════════╣     ┃
┃  ║                                                         ║     ┃
┃  ║ ✅ Step 1: Open PowerPoint application                ║     ┃
┃  ║    Result: PowerPoint opened successfully              ║     ┃
┃  ║                                                         ║     ┃
┃  ║ ✅ Step 2: Create new blank presentation              ║     ┃
┃  ║    Result: New presentation created                    ║     ┃
┃  ║                                                         ║     ┃
┃  ║ ✅ Step 3: Add title slide                            ║     ┃
┃  ║    Result: Title slide added successfully              ║     ┃
┃  ║                                                         ║     ┃
┃  ║ ✅ Step 4: Add content slides                         ║     ┃
┃  ║    Result: Content slides created                      ║     ┃
┃  ║                                                         ║     ┃
┃  ║ ✅ Step 5: Save to Desktop as "Presentation.pptx"     ║     ┃
┃  ║    Result: File saved to Desktop successfully          ║     ┃
┃  ║                                                         ║     ┃
┃  ║ ✅ Step 6: Close PowerPoint                           ║     ┃
┃  ║    Result: Application closed                          ║     ┃
┃  ║                                                         ║     ┃
┃  ╚════════════════════════════════════════════════════════╝     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  USER                                                       │
│    │                                                        │
│    │ 1. Provides task                                      │
│    ▼                                                        │
│  ┌─────────────────┐                                       │
│  │  MAIN.PY        │                                       │
│  │  (Entry Point)  │                                       │
│  └────────┬────────┘                                       │
│           │                                                 │
│           │ 2. Initializes                                 │
│           ▼                                                 │
│  ┌─────────────────┐        ┌─────────────────┐           │
│  │  PLANNER AI     │───────▶│  PLANNER LLM    │           │
│  │                 │        │  (Temperature    │           │
│  │ • create_plan() │  3.    │   = 0.3)        │           │
│  │ • display_plan()│ Calls  └─────────────────┘           │
│  │ • execute_plan()│                                       │
│  └────────┬────────┘                                       │
│           │                                                 │
│           │ 4. For each step                               │
│           ▼                                                 │
│  ┌─────────────────┐        ┌─────────────────┐           │
│  │  ACTION AGENT   │───────▶│  AGENT LLM      │           │
│  │                 │        │  (Temperature    │           │
│  │ • reason()      │  5.    │   = 0.2)        │           │
│  │ • action()      │ Calls  └─────────────────┘           │
│  │ • answer()      │                                       │
│  └────────┬────────┘                                       │
│           │                                                 │
│           │ 6. Uses tools                                  │
│           ▼                                                 │
│  ┌─────────────────┐                                       │
│  │  TOOL REGISTRY  │                                       │
│  │                 │                                       │
│  │ • click_tool    │                                       │
│  │ • type_tool     │                                       │
│  │ • app_tool      │                                       │
│  │ • shell_tool    │                                       │
│  │ • etc...        │                                       │
│  └────────┬────────┘                                       │
│           │                                                 │
│           │ 7. Interacts                                   │
│           ▼                                                 │
│  ┌─────────────────┐                                       │
│  │  WINDOWS GUI    │                                       │
│  │                 │                                       │
│  │ • UIAutomation  │                                       │
│  │ • PyAutoGUI     │                                       │
│  └─────────────────┘                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Decision Tree

```
                    START
                      │
                      ▼
           ┌──────────────────────┐
           │ User provides task   │
           └──────────┬───────────┘
                      │
                      ▼
           ┌──────────────────────┐
           │ Select Mode:         │
           │ 1. Planner AI        │
           │ 2. Direct Agent      │
           └──────────┬───────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
┌────────────────┐       ┌────────────────┐
│ MODE 1:        │       │ MODE 2:        │
│ Planner AI     │       │ Direct Agent   │
└───────┬────────┘       └───────┬────────┘
        │                        │
        ▼                        │
┌────────────────┐               │
│ Create Plan    │               │
└───────┬────────┘               │
        │                        │
        ▼                        │
┌────────────────┐               │
│ Display Plan   │               │
└───────┬────────┘               │
        │                        │
        ▼                        │
┌────────────────┐               │
│ User Approves? │               │
└───────┬────────┘               │
        │                        │
    ┌───┴───┐                    │
    │       │                    │
   YES     NO                    │
    │       │                    │
    │       ▼                    │
    │  ┌────────┐                │
    │  │ Cancel │                │
    │  └────────┘                │
    │                            │
    ▼                            │
┌────────────────┐               │
│ Execute Steps  │◄──────────────┘
│ Sequentially   │
└───────┬────────┘
        │
        ▼
   ┌────────────┐
   │ Step N     │
   └─────┬──────┘
         │
    ┌────┴────┐
    │         │
 SUCCESS   FAILURE
    │         │
    │         ▼
    │    ┌────────────┐
    │    │ User Choice│
    │    └─────┬──────┘
    │          │
    │     ┌────┴────┬─────────┐
    │     │         │         │
    │   RETRY     SKIP      ABORT
    │     │         │         │
    │     │         │         ▼
    │     │         │     ┌────────┐
    │     │         │     │  END   │
    │     │         │     └────────┘
    │     │         │
    │     └─────────┘
    │          │
    ▼          ▼
┌─────────────────┐
│ Next Step or    │
│ Summary         │
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │ Display │
    │ Summary │
    └─────────┘
         │
         ▼
       END
```

## Data Flow

```
┌─────────────────────────────────────────────────────────┐
│  USER INPUT                                             │
│  "Create a PowerPoint presentation"                     │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  PLANNER LLM INPUT                                      │
│  ┌───────────────────────────────────────────────────┐ │
│  │ System Prompt: You are a Task Planner AI...      │ │
│  │ User Prompt: Create PowerPoint presentation      │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  PLANNER LLM OUTPUT                                     │
│  ┌───────────────────────────────────────────────────┐ │
│  │ {                                                 │ │
│  │   "task_summary": "Create PowerPoint",           │ │
│  │   "steps": [                                     │ │
│  │     {                                            │ │
│  │       "step_number": 1,                          │ │
│  │       "description": "Open PowerPoint",          │ │
│  │       "expected_outcome": "App launches"         │ │
│  │     },                                           │ │
│  │     ...                                          │ │
│  │   ],                                             │ │
│  │   "estimated_complexity": "moderate"             │ │
│  │ }                                                │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  FORMATTED STEP QUERY                                   │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Part of larger task: Create PowerPoint           │ │
│  │                                                   │ │
│  │ Current Step: Open PowerPoint application        │ │
│  │                                                   │ │
│  │ Expected Outcome: PowerPoint launches            │ │
│  │                                                   │ │
│  │ Previous steps completed:                        │ │
│  │ (none yet)                                       │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  AGENT LLM INPUT                                        │
│  ┌───────────────────────────────────────────────────┐ │
│  │ System: Windows agent with tools...              │ │
│  │ User: Open PowerPoint application                │ │
│  │ Desktop State: [current UI elements]             │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  AGENT LLM OUTPUT                                       │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Evaluate: Need to launch PowerPoint              │ │
│  │ Thought: Use app_tool with PowerPoint            │ │
│  │ Action: app_tool(app_name="PowerPoint")          │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  TOOL EXECUTION                                         │
│  app_tool(app_name="PowerPoint")                        │
│  ↓                                                      │
│  Windows automation                                     │
│  ↓                                                      │
│  PowerPoint opens                                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  EXECUTION RESULT                                       │
│  ┌───────────────────────────────────────────────────┐ │
│  │ {                                                 │ │
│  │   "success": true,                                │ │
│  │   "content": "PowerPoint opened successfully",    │ │
│  │   "error": null                                   │ │
│  │ }                                                 │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  EXECUTION HISTORY UPDATE                               │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Step 1: ✅ Success                                │ │
│  │ Description: Open PowerPoint                      │ │
│  │ Result: PowerPoint opened successfully            │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
               REPEAT FOR NEXT STEP
```

## Error Handling Flow

```
                 STEP EXECUTION
                        │
                        ▼
                ┌───────────────┐
                │ Execute Step  │
                └───────┬───────┘
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
    ┌─────────┐                  ┌─────────┐
    │ SUCCESS │                  │ FAILURE │
    └────┬────┘                  └────┬────┘
         │                            │
         ▼                            ▼
┌────────────────┐          ┌──────────────────┐
│ Record Success │          │ Display Error    │
│ ✅ Mark Step   │          │ ❌ Show Details  │
│ Continue Next  │          └────────┬─────────┘
└────────────────┘                   │
         │                           ▼
         │                  ┌──────────────────┐
         │                  │ User Prompt:     │
         │                  │ (r)etry          │
         │                  │ (s)kip           │
         │                  │ (a)bort          │
         │                  └────────┬─────────┘
         │                           │
         │            ┌──────────────┼──────────────┐
         │            │              │              │
         │            ▼              ▼              ▼
         │      ┌─────────┐    ┌─────────┐    ┌─────────┐
         │      │  RETRY  │    │  SKIP   │    │  ABORT  │
         │      └────┬────┘    └────┬────┘    └────┬────┘
         │           │              │              │
         │           │              │              ▼
         │           │              │         ┌─────────┐
         │           │              │         │   END   │
         │           │              │         │ SHOW    │
         │           │              │         │ SUMMARY │
         │           │              │         └─────────┘
         │           │              │
         │           └──────────────┘
         │                    │
         ▼                    ▼
    ┌────────────────────────────┐
    │     NEXT STEP OR END       │
    └────────────────────────────┘
```

## State Transitions

```
STATE:                ACTION:              NEXT STATE:

IDLE ──────────────▶ User Input ─────────▶ PLANNING

PLANNING ──────────▶ Create Plan ────────▶ PLAN_CREATED

PLAN_CREATED ──────▶ Display Plan ───────▶ AWAITING_APPROVAL

AWAITING_APPROVAL ─▶ User Approves ─────▶ EXECUTING
                  │
                  └─▶ User Rejects ──────▶ IDLE

EXECUTING ─────────▶ Step Success ───────▶ NEXT_STEP

NEXT_STEP ─────────▶ More Steps? ────────▶ EXECUTING
                  │
                  └─▶ No More Steps ─────▶ COMPLETED

EXECUTING ─────────▶ Step Failure ───────▶ ERROR_HANDLING

ERROR_HANDLING ────▶ User: Retry ────────▶ EXECUTING

ERROR_HANDLING ────▶ User: Skip ─────────▶ NEXT_STEP

ERROR_HANDLING ────▶ User: Abort ────────▶ ABORTED

COMPLETED ─────────▶ Show Summary ───────▶ IDLE

ABORTED ───────────▶ Show Summary ───────▶ IDLE
```

## Success Indicators

```
┌─────────────────────────────────────────┐
│  GREEN FLAGS ✅                         │
├─────────────────────────────────────────┤
│                                         │
│  ✅ Plan generated successfully         │
│  ✅ User approves plan                  │
│  ✅ Each step executes successfully     │
│  ✅ No errors encountered               │
│  ✅ All steps completed                 │
│  ✅ 100% success rate                   │
│  ✅ Expected outcomes achieved          │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  YELLOW FLAGS ⚠️                        │
├─────────────────────────────────────────┤
│                                         │
│  ⚠️  Some steps skipped                 │
│  ⚠️  Retries needed                     │
│  ⚠️  Partial success                    │
│  ⚠️  Unexpected behavior                │
│  ⚠️  50-99% success rate                │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  RED FLAGS ❌                           │
├─────────────────────────────────────────┤
│                                         │
│  ❌ Plan generation failed              │
│  ❌ User rejected plan                  │
│  ❌ Multiple step failures              │
│  ❌ Critical errors                     │
│  ❌ Execution aborted                   │
│  ❌ < 50% success rate                  │
│                                         │
└─────────────────────────────────────────┘
```

## Quick Reference

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  PLANNER AI QUICK REFERENCE            ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                         ┃
┃  START:     python main.py             ┃
┃  TESTS:     python test_planner.py     ┃
┃  EXAMPLES:  python planner_example.py  ┃
┃                                         ┃
┃  MODE 1:    Planner AI (complex)       ┃
┃  MODE 2:    Direct Agent (simple)      ┃
┃                                         ┃
┃  RETRY:     Press 'r' on failure       ┃
┃  SKIP:      Press 's' on failure       ┃
┃  ABORT:     Press 'a' on failure       ┃
┃                                         ┃
┃  DOCS:      QUICKSTART.md              ┃
┃             PLANNER_GUIDE.md           ┃
┃             ARCHITECTURE.md            ┃
┃                                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

*Visual representations help understand complex systems. Use these diagrams as a reference while working with Planner AI!*

