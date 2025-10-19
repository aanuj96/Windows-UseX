# Planner AI - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER INPUT                              │
│                "Complex Task Description"                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       PLANNER AI                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Analyze Task                                          │  │
│  │  2. Break Down into Steps                                │  │
│  │  3. Generate Execution Plan                              │  │
│  │     - Step descriptions                                  │  │
│  │     - Expected outcomes                                  │  │
│  │     - Complexity estimation                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTION PLAN                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Step 1: [Description] → Expected: [Outcome]             │   │
│  │ Step 2: [Description] → Expected: [Outcome]             │   │
│  │ Step 3: [Description] → Expected: [Outcome]             │   │
│  │ ...                                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   USER CONFIRMATION                              │
│  "Review Plan → Approve/Reject"                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STEP-BY-STEP EXECUTION                          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  For Each Step:                                         │   │
│  │  ┌──────────────────────────────────────────────────┐  │   │
│  │  │  1. Format Step Query with Context              │  │   │
│  │  │  2. Send to Action Agent                        │  │   │
│  │  │  3. Monitor Execution                           │  │   │
│  │  │  4. Record Results                              │  │   │
│  │  │  5. Handle Errors (Retry/Skip/Abort)           │  │   │
│  │  └──────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ACTION AGENT                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  GRAPH: REASON → ACTION → ANSWER                         │  │
│  │                                                           │  │
│  │  REASON:                                                 │  │
│  │  - Analyze current step                                  │  │
│  │  - Evaluate desktop state                                │  │
│  │  - Decide on tool to use                                 │  │
│  │                                                          │  │
│  │  ACTION:                                                 │  │
│  │  - Execute selected tool                                 │  │
│  │  - Interact with Windows GUI                            │  │
│  │  - Capture results                                      │  │
│  │                                                          │  │
│  │  ANSWER:                                                 │  │
│  │  - Return execution results                             │  │
│  │  - Report success/failure                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WINDOWS AUTOMATION                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Available Tools:                                          │  │
│  │ • Click Tool      - Click UI elements                    │  │
│  │ • Type Tool       - Type text                            │  │
│  │ • App Tool        - Launch applications                  │  │
│  │ • Shell Tool      - Execute commands                     │  │
│  │ • Scroll Tool     - Scroll windows                       │  │
│  │ • Drag Tool       - Drag & drop                          │  │
│  │ • Shortcut Tool   - Keyboard shortcuts                   │  │
│  │ • Wait Tool       - Wait/delay                           │  │
│  │ • Scrape Tool     - Extract information                  │  │
│  │ • Done Tool       - Mark completion                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTION SUMMARY                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Total Steps Executed                                    │  │
│  │ • Success Rate                                           │  │
│  │ • Detailed Results per Step                             │  │
│  │ • Error Reports (if any)                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Planning Phase

```
User Query
    ↓
Planner LLM (Mistral Small)
    ↓
JSON Plan Structure
    {
      "task_summary": "...",
      "steps": [...],
      "estimated_complexity": "..."
    }
```

### 2. Execution Phase

```
For each step in plan:
    ↓
Step Query Formatter
    ├─ Original task context
    ├─ Current step description
    ├─ Expected outcome
    └─ Previous steps completed
    ↓
Action Agent
    ├─ Reason: Analyze & decide
    ├─ Action: Execute tool
    └─ Answer: Return result
    ↓
Execution Record
    ├─ Step number
    ├─ Description
    ├─ Result/Error
    └─ Success status
```

## Component Details

### PlannerAI Class

**Responsibilities:**
- Task decomposition
- Plan generation
- Execution coordination
- Progress tracking
- Error handling

**Key Methods:**
```python
create_plan(user_query) -> dict
    - Generates execution plan using LLM

display_plan(plan_data)
    - Shows plan to user in formatted manner

execute_plan(user_query)
    - Orchestrates step-by-step execution

_format_step_query(step, original_query) -> str
    - Prepares query for agent with context

_display_summary()
    - Shows execution results and statistics
```

### Agent Class

**Responsibilities:**
- Single-step task execution
- Windows GUI interaction
- Tool management
- State tracking

**Key Components:**
- **Reason Node**: Decides what action to take
- **Action Node**: Executes the tool
- **Answer Node**: Provides final result

### Communication Flow

```
Planner AI                    Action Agent
    |                              |
    |--- Step Query ------------->|
    |                              |
    |                         [REASON]
    |                              |
    |                         [ACTION]
    |                              |
    |                         [ANSWER]
    |                              |
    |<---- Result/Error -----------|
    |                              |
    |--- Next Step Query -------->|
```

## Error Handling Strategy

```
Step Execution Failed
    ↓
User Prompted with Options:
    ├─ (r) Retry
    │   └─> Re-execute same step
    ├─ (s) Skip
    │   └─> Continue to next step
    └─ (a) Abort
        └─> Stop entire execution
```

## State Management

### Planner State
```python
{
    'current_plan': [list of steps],
    'completed_steps': [successfully completed],
    'execution_history': [all attempts with results]
}
```

### Agent State
```python
{
    'steps': current_step_number,
    'max_steps': maximum_allowed,
    'messages': conversation_history,
    'agent_data': current_action_data,
    'previous_observation': last_result,
    'error': error_message_if_any
}
```

## LLM Integration

### Two LLM Instances

1. **Planner LLM**
   - Model: Mistral Small 3.1 (or configurable)
   - Temperature: 0.3 (slightly creative)
   - Purpose: Generate execution plans

2. **Agent LLM**
   - Model: Mistral Small 3.1 (or configurable)
   - Temperature: 0.2 (more deterministic)
   - Purpose: Execute individual steps

### Why Separate LLMs?

- **Separation of Concerns**: Planning vs execution
- **Different Temperature Settings**: Creative planning vs precise execution
- **Scalability**: Can use different models for each role
- **Cost Optimization**: Can use cheaper models for planning

## Desktop Integration

```
Agent
  ↓
Desktop Service
  ├─ State Capture
  │   ├─ Active applications
  │   ├─ UI elements (tree)
  │   ├─ Cursor position
  │   └─ Screenshot (if vision enabled)
  │
  └─ Tool Execution
      ├─ UIAutomation
      │   └─ Element interaction
      └─ PyAutoGUI
          └─ Low-level input
```

## Example Execution Flow

```
User: "Create a file called notes.txt on Desktop"

PLANNER AI:
  Step 1: Open File Explorer
  Step 2: Navigate to Desktop
  Step 3: Right-click in empty space
  Step 4: Select New > Text Document
  Step 5: Rename to "notes.txt"

EXECUTION:
  Step 1 → Agent → [app_tool] → Success ✓
  Step 2 → Agent → [click_tool] → Success ✓
  Step 3 → Agent → [click_tool] → Success ✓
  Step 4 → Agent → [click_tool] → Success ✓
  Step 5 → Agent → [type_tool] → Success ✓

RESULT:
  5/5 steps completed
  Success rate: 100%
  File created successfully
```

## Advantages of This Architecture

1. **Modularity**: Clear separation between planning and execution
2. **Flexibility**: Can use different LLMs for different roles
3. **Robustness**: Error handling at each step
4. **Transparency**: User sees the plan before execution
5. **Controllability**: User can intervene at any point
6. **Scalability**: Easy to add new tools or features
7. **Context Awareness**: Each step knows about previous steps

## Future Enhancements

### Possible Improvements

1. **Dynamic Replanning**
   - Adjust plan based on execution results
   - Learn from failures

2. **Parallel Execution**
   - Execute independent steps simultaneously
   - Optimize execution time

3. **Learning System**
   - Store successful plans
   - Reuse similar patterns

4. **Vision Integration**
   - Use screenshots for better context
   - Visual verification of results

5. **Multi-Agent Collaboration**
   - Multiple agents working together
   - Specialized agents for different tasks

6. **Plan Optimization**
   - Minimize number of steps
   - Find most efficient path

## Performance Considerations

### Latency Factors

1. **LLM API Calls**
   - Planning: 1 call
   - Execution: 1-3 calls per step

2. **Tool Execution Time**
   - Varies by tool and system
   - Typically 1-5 seconds per action

3. **State Capture**
   - Desktop scanning: ~0.5-2 seconds
   - UI tree building: ~1-3 seconds

### Optimization Tips

1. Use faster LLM models for simple tasks
2. Reduce max_steps for time-critical operations
3. Enable auto_minimize to avoid IDE interference
4. Use Direct Mode for single-action tasks
5. Batch independent steps when possible

