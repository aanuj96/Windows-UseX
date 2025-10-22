from windows_use.llm.openrouter import ChatOpenRouter
from windows_use.agent import Agent, Browser
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from termcolor import colored
import os
import json
import re
import subprocess
import time
from datetime import datetime

load_dotenv()

def show_toast(title: str, message: str, icon_type: str = "info"):
    """Show Windows toast notification using PowerShell"""
    try:
        # Map icon types to Windows notification icons
        icon_map = {
            "success": "✅",
            "fail": "❌",
            "info": "ℹ️"
        }
        icon = icon_map.get(icon_type, "ℹ️")
        
        # Use PowerShell to show a native Windows notification
        ps_script = f"""
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
        
        $template = @"
        <toast>
            <visual>
                <binding template="ToastText02">
                    <text id="1">{icon} {title}</text>
                    <text id="2">{message}</text>
                </binding>
            </visual>
        </toast>
"@
        
        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Windows-Use Agent").Show($toast)
        """
        
        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        # Fallback to console notification if toast fails
        print(colored(f"\n{icon} {title}: {message}", 
                     'green' if icon_type == 'success' else 'red' if icon_type == 'fail' else 'cyan'))

class AgentMonitor:
    """Monitor agent execution to detect loops and track per-iteration timing"""
    
    def __init__(self, agent: Agent):
        self.agent = agent
        self.error_history = []  # Track last N errors to detect loops
        self.iteration_timings = []
        
    def invoke_with_monitoring(self, query: str):
        """Invoke agent with loop detection and per-iteration timing"""
        print(colored("\n⏱️  Execution Monitoring Active:", color='cyan', attrs=['bold']))
        print(colored("   Tracking: LLM calls, Screenshots, Tool execution, Loop detection", color='cyan'))
        print("="*60)
        
        # Wrap the invoke to capture iteration-level details
        start_time = time.time()
        result = self.agent.invoke(query)
        total_time = time.time() - start_time
        
        # Track error patterns
        if result.error:
            error_sig = str(result.error)[:100]  # First 100 chars as signature
            self.error_history.append(error_sig)
            
            # Keep only last 5 errors
            if len(self.error_history) > 5:
                self.error_history.pop(0)
            
            # Detect loop: same error 3+ times in a row
            if len(self.error_history) >= 3:
                if self.error_history[-1] == self.error_history[-2] == self.error_history[-3]:
                    print(colored("\n🔴 LOOP DETECTED: Same error repeated 3 times!", color='red', attrs=['bold']))
                    print(colored(f"   Error pattern: {error_sig}", color='red'))
                    print(colored("   Agent is stuck in infinite loop!", color='red'))
                    print(colored("\n   🆘 Actions taken:", color='yellow', attrs=['bold']))
                    print(colored("   - Triggering fallback model automatically", color='yellow'))
                    print(colored("   - Will try alternative approach", color='yellow'))
                    print(colored("   - User can manually intervene if needed\n", color='yellow'))
                    # Mark this for fallback handling
                    result.loop_detected = True
        else:
            # Clear error history on success
            self.error_history = []
        
        # Display detailed timing summary
        print("\n" + "="*60)
        print(colored("⏱️  Performance Metrics:", color='yellow', attrs=['bold']))
        print("="*60)
        print(colored(f"Total time: {total_time:.2f}s", color='yellow'))
        print(colored(f"   ├─ LLM calls: Included in total", color='cyan'))
        
        if self.agent.use_vision:
            print(colored(f"   ├─ Screenshots: ENABLED (~3x overhead)", color='cyan'))
            estimated_screenshot_time = total_time * 0.6  # Rough estimate
            estimated_llm_time = total_time * 0.4
            print(colored(f"   │  ├─ Est. screenshot time: ~{estimated_screenshot_time:.2f}s", color='magenta'))
            print(colored(f"   │  └─ Est. LLM+tool time: ~{estimated_llm_time:.2f}s", color='magenta'))
        else:
            print(colored(f"   ├─ Screenshots: DISABLED (faster!)", color='green'))
            print(colored(f"   │  └─ Saved: ~{total_time * 2:.2f}s (3x speed boost)", color='green'))
        
        print(colored(f"   └─ Tool execution: Included in total", color='cyan'))
        print("="*60)
        
        return result
    
    def check_for_loop(self) -> bool:
        """Check if agent is stuck in a loop"""
        if len(self.error_history) >= 3:
            return self.error_history[-1] == self.error_history[-2] == self.error_history[-3]
        return False

class PlannerAI:
    """
    Planner AI Model that breaks down complex tasks into step-by-step instructions
    and coordinates the execution with the Action Agent.
    """
    
    def __init__(self, llm, agent: Agent, fallback_llm=None):
        self.llm = llm
        self.fallback_llm = fallback_llm  # Backup model for difficult tasks
        self.agent = agent
        self.monitor = AgentMonitor(agent)  # Add monitoring
        self.console = Console()
        self.current_plan = []
        self.completed_steps = []
        self.execution_history = []
        self.using_fallback = False
        self.timing_stats = {
            'planner_llm_time': 0,
            'agent_execution_time': 0,
            'total_time': 0,
            'batch_times': []
        }
        
    def create_plan(self, user_query: str) -> list[dict]:
        """Create a detailed step-by-step plan for the user's query"""
        
        system_prompt = """You are a Task Planner AI. Your job is to break down complex user requests into VERY SPECIFIC, ISOLATED steps that will be executed ONE AT A TIME by an AI agent.

⚡ EXECUTION PRIORITY (Always prefer in this order):
1. 🖥️ TERMINAL COMMANDS (PowerShell/CMD) - Most efficient for file ops, system tasks, app launching
2. ⌨️ KEYBOARD SHORTCUTS - Fast, reliable, no GUI dependency (Win+R, Ctrl+C, Alt+Tab, etc.)
3. 🖱️ GUI INTERACTIONS - Only when terminal/keyboard methods aren't available

🎯 CRITICAL REQUIREMENTS:
1. Each step must be a SINGLE, ATOMIC action - DO NOT combine multiple actions
2. Each step will be executed INDEPENDENTLY - the agent will NOT see other steps
3. Be EXTREMELY specific - include exact button names, exact text to type, exact locations
4. Break down even simple tasks into granular steps
5. Each step should take only 1-3 actions maximum
6. NEVER say "complete the task" or "finish" - be explicit about the exact action
7. ALWAYS prefer Shell Tool + keyboard shortcuts over clicking buttons

❌ BAD EXAMPLE (GUI-Heavy):
"Open Notepad and type hello world" (This is TWO actions combined!)

✅ BETTER EXAMPLE (Terminal/Keyboard-First):
Step 1: "Use Shell Tool to run command: Start-Process notepad"
Step 2: "Type the text 'hello world' in Notepad"

✅ BEST EXAMPLE (Pure Terminal):
Step 1: "Use Shell Tool: notepad | Out-Null; Start-Sleep -Seconds 2"
Step 2: "Use Shortcut Tool: Win+R, then type 'notepad', then Enter"

🎯 TERMINAL-FIRST EXAMPLES:
- Opening apps: Shell Tool → `Start-Process chrome` OR Shortcut Tool → Win+R → type app name
- File operations: Shell Tool → `Copy-Item`, `Move-Item`, `Remove-Item`, `New-Item`
- Text manipulation: Shell Tool → `Set-Content`, `Add-Content`, `Get-Content`
- Clipboard: Shortcut Tool → Ctrl+C (copy), Ctrl+V (paste), Ctrl+X (cut)
- Navigation: Shortcut Tool → Win+E (Explorer), Win+S (Search), Alt+Tab (Switch apps)

Guidelines:
- Each step = ONE clear action only
- Be specific about UI elements (button names, menu items, etc.)
- Include prerequisite steps (opening apps, focusing windows, etc.)
- Steps execute sequentially but independently
- Agent won't remember previous step instructions
- Expected outcomes MUST be verifiable (agent checks desktop state after each action)
- Make expected outcomes specific and observable (e.g., "Notepad window is open" not just "success")

Return your plan in the following JSON format:
{
  "task_summary": "Brief summary of what needs to be accomplished",
  "steps": [
    {
      "step_number": 1,
      "description": "ONE specific action to perform (be extremely detailed)",
      "expected_outcome": "Exact result after this single action",
      "alternative_approach": "DIFFERENT way to achieve same outcome if primary approach fails (use different tool/method)"
    }
  ],
  "estimated_complexity": "simple/moderate/complex"
}

IMPORTANT: Always provide an alternative_approach for each step. This is a backup method if the primary approach fails.

Examples of alternatives (PREFER Terminal/Keyboard):
- Primary: "Use Shell Tool: Start-Process notepad" → Alternative: "Press Win+R, type 'notepad', press Enter"
- Primary: "Click button with label 49" → Alternative: "Use keyboard shortcut Win+S or Shell Tool command"
- Primary: "Type in search box" → Alternative: "Use Shell Tool to pipe text or keyboard shortcut"
- Primary: "Click File menu" → Alternative: "Use keyboard shortcut Alt+F"
- Primary: "Click Save button" → Alternative: "Use Shortcut Tool: Ctrl+S"
- Primary: "Navigate to folder" → Alternative: "Use Shell Tool: Set-Location or Win+E + type path"

Only return valid JSON, nothing else."""

        user_prompt = f"""User Request: {user_query}

Please create a detailed step-by-step plan to accomplish this task on a Windows computer."""

        print(colored("\n🧠 Planner AI: Analyzing task and creating plan...\n", color='cyan', attrs=['bold']))
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        # Track planner LLM time
        planner_start = time.time()
        response = self.llm.invoke(messages)
        planner_time = time.time() - planner_start
        self.timing_stats['planner_llm_time'] = planner_time
        
        print(colored(f"⏱️  Planner LLM: {planner_time:.2f}s\n", color='yellow'))
        
        try:
            # Extract JSON from the response
            content = response.content
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                plan_data = json.loads(json_match.group())
            else:
                plan_data = json.loads(content)
                
            return plan_data
        except json.JSONDecodeError as e:
            print(f"Error parsing plan: {e}")
            print(f"Response content: {response.content}")
            # Fallback: create a simple single-step plan
            return {
                "task_summary": user_query,
                "steps": [
                    {
                        "step_number": 1,
                        "description": user_query,
                        "expected_outcome": "Task completed"
                    }
                ],
                "estimated_complexity": "unknown"
            }
    
    def display_plan(self, plan_data: dict):
        """Display the plan in a formatted way"""
        
        self.console.print(Panel.fit(
            f"[bold cyan]Task:[/bold cyan] {plan_data['task_summary']}\n"
            f"[bold yellow]Complexity:[/bold yellow] {plan_data['estimated_complexity'].upper()}\n"
            f"[bold green]Total Steps:[/bold green] {len(plan_data['steps'])}",
            title="📋 Execution Plan",
            border_style="cyan"
        ))
        
        self.console.print("\n[bold underline]Step-by-Step Breakdown:[/bold underline]\n")
        for step in plan_data['steps']:
            self.console.print(
                f"[bold blue]Step {step['step_number']}:[/bold blue] {step['description']}"
            )
            self.console.print(
                f"  [dim]Expected: {step['expected_outcome']}[/dim]"
            )
            if 'alternative_approach' in step and step['alternative_approach']:
                self.console.print(
                    f"  [yellow]💡 Backup: {step['alternative_approach']}[/yellow]\n"
                )
            else:
                self.console.print("")
    
    def execute_plan(self, user_query: str, reuse_plan: bool = False):
        """Execute the plan step by step using the agent"""
        
        # Only create plan if we don't have one or not reusing
        if not reuse_plan or not self.current_plan:
            # Create the plan
            plan_data = self.create_plan(user_query)
            self.current_plan = plan_data['steps']
            
            # Display the plan
            self.display_plan(plan_data)
            
            # Ask for confirmation
            self.console.print("\n" + "="*60)
            proceed = input("\n🚀 Proceed with execution? (yes/no): ").strip().lower()
            
            if proceed not in ['yes', 'y']:
                print("Execution cancelled by user.")
                return
        else:
            print(colored("\n♻️  Reusing existing plan (skipping planner call)...\n", color='cyan', attrs=['bold']))
        
        # Reset for new execution
        self.completed_steps = []
        self.execution_history = []
        step_failures = {}  # Track failures per step
        
        print("\n" + "="*60)
        print(colored("\n🚀 Starting Plan Execution...\n", color='green', attrs=['bold']))
        
        # Execute each step
        i = 0
        while i < len(self.current_plan):
            step = self.current_plan[i]
            step_num = i + 1
            
            # Check failure count
            failure_count = step_failures.get(step_num, 0)
            use_alternative = failure_count >= 2 and failure_count < 3
            use_fallback = failure_count >= 3 and self.fallback_llm is not None
            
            # Display execution status
            if use_fallback:
                print("="*60)
                print(colored(f"\n🆘 Step {step_num}/{len(self.current_plan)} - USING FALLBACK MODEL", color='red', attrs=['bold']))
                print(colored(f"Primary model failed 3 times, switching to fallback LLM", color='yellow'))
                print(colored(f"Fallback Model: {self.fallback_llm._identifying_params.get('model', 'backup')}", color='white'))
                print(colored(f"Action: {step['description']}\n", color='white'))
                print("="*60 + "\n")
                
                # Switch agent's LLM to fallback
                original_llm = self.agent.llm
                self.agent.llm = self.fallback_llm
                self.using_fallback = True
                step_query = self._format_step_query(step, user_query, use_alternative=False)
                
            elif use_alternative and 'alternative_approach' in step and step['alternative_approach']:
                print("="*60)
                print(colored(f"\n🔄 Step {step_num}/{len(self.current_plan)} - USING ALTERNATIVE APPROACH", color='magenta', attrs=['bold']))
                print(colored(f"Primary failed 2 times, trying backup method", color='yellow'))
                print(colored(f"Alternative: {step['alternative_approach']}\n", color='white'))
                print("="*60 + "\n")
                step_query = self._format_step_query(step, user_query, use_alternative=True)
                
            else:
                print("="*60)
                print(colored(f"\n📍 Executing Step {step_num}/{len(self.current_plan)}", color='yellow', attrs=['bold']))
                if failure_count > 0:
                    print(colored(f"   (Attempt {failure_count + 1})", color='cyan'))
                print(colored(f"Action: {step['description']}\n", color='white'))
                print("="*60 + "\n")
                step_query = self._format_step_query(step, user_query)
            
            # Execute the step using the agent WITH MONITORING
            result = self.monitor.invoke_with_monitoring(step_query)
            
            # Check for loop detection
            if hasattr(result, 'loop_detected') and result.loop_detected:
                print(colored("\n🆘 LOOP DETECTED - Forcing fallback model activation!\n", color='red', attrs=['bold']))
                # Force to 3 failures to trigger fallback
                step_failures[step_num] = 3
                
                if not use_fallback and self.fallback_llm:
                    print(colored("   Activating fallback model on next retry...\n", color='yellow'))
                    continue  # Retry with fallback
                else:
                    print(colored("   ⚠️  Already using fallback or no fallback configured", color='yellow'))
                    print(colored("   Asking user for manual intervention...\n", color='yellow'))
                    
                    retry = input(f"Agent is stuck. (r)etry, (s)kip, or (a)bort? ").strip().lower()
                    if retry == 'r':
                        step_failures[step_num] = 0  # Reset and retry
                        self.monitor.error_history = []  # Clear error history
                        continue
                    elif retry == 'a':
                        print(colored("\n⛔ Execution aborted by user.\n", color='red', attrs=['bold']))
                        return
                    else:
                        print(colored(f"\n⏭️  Skipping step {step_num}...\n", color='yellow'))
                        i += 1
                        continue
            
            # Restore original LLM if we used fallback
            if use_fallback:
                self.agent.llm = original_llm
                self.using_fallback = False
            
            # Record the execution
            execution_record = {
                'step_number': step_num,
                'description': step['description'],
                'query': step_query,
                'result': result.content,
                'error': result.error,
                'success': result.error is None,
                'used_alternative': use_alternative,
                'used_fallback': use_fallback
            }
            self.execution_history.append(execution_record)
            
            if result.error:
                # Increment failure count
                step_failures[step_num] = step_failures.get(step_num, 0) + 1
                
                print(colored(f"\n❌ Step {step_num} Failed (Attempt {step_failures[step_num]}): {result.error}\n", color='red', attrs=['bold']))
                
                # Check if we should try alternative (after 2 failures)
                if step_failures[step_num] == 2 and not use_alternative and not use_fallback:
                    if 'alternative_approach' in step and step['alternative_approach']:
                        print(colored("💡 Primary approach failed twice. Will try alternative approach next.\n", color='yellow', attrs=['bold']))
                        # Don't increment i, will retry with alternative
                        continue
                    else:
                        print(colored("⚠️  No alternative approach available. Will try fallback model if configured.\n", color='yellow'))
                        # Jump to 3 to trigger fallback
                        step_failures[step_num] = 3
                        continue
                
                # Check if we should activate fallback model (after 3 failures)
                if step_failures[step_num] == 3 and not use_fallback:
                    if self.fallback_llm:
                        print(colored("🆘 Both primary and alternative failed. Activating fallback model.\n", color='red', attrs=['bold']))
                        print(colored("   Fallback model will keep trying until step succeeds.\n", color='cyan'))
                        # Don't increment i, will retry with fallback
                        continue
                    else:
                        print(colored("⚠️  No fallback model configured.\n", color='red'))
                
                # If using fallback and it fails, keep retrying with fallback
                if use_fallback:
                    if step_failures[step_num] < 10:  # Allow up to 10 attempts with fallback
                        print(colored(f"🆘 Fallback model will retry (attempt {step_failures[step_num] - 2} with fallback)...\n", color='yellow'))
                        # Keep trying with fallback, don't increment i
                        continue
                    else:
                        print(colored(f"⚠️  Fallback model failed {step_failures[step_num] - 2} times. Manual intervention needed.\n", color='red', attrs=['bold']))
                
                # If too many failures or no fallback, ask user
                if (not use_fallback and step_failures[step_num] > 3) or (use_fallback and step_failures[step_num] >= 10):
                    print(colored(f"⚠️  All attempts exhausted. Manual intervention needed.\n", color='red', attrs=['bold']))
                    
                    # Ask user what to do
                    retry = input(f"Would you like to (r)etry, (s)skip, or (a)bort? ").strip().lower()
                    
                    if retry == 'r':
                        # Reset failure count for manual retry
                        step_failures[step_num] = 0
                        continue
                    elif retry == 'a':
                        print(colored("\n⛔ Execution aborted by user.\n", color='red', attrs=['bold']))
                        break
                    else:
                        print(colored(f"\n⏭️  Skipping step {step_num}...\n", color='yellow'))
                        i += 1
                        continue
                
                # For other failure cases, keep retrying
                continue
                
            else:
                print(colored(f"\n✅ Step {step_num} Completed Successfully\n", color='green', attrs=['bold']))
                if use_fallback:
                    print(colored(f"   🆘 Fallback model succeeded! Returning to primary model for next step.\n", color='green', attrs=['bold']))
                elif use_alternative:
                    print(colored(f"   ✨ Alternative approach worked!\n", color='green'))
                self.completed_steps.append(step)
                i += 1  # Move to next step
        
        # Display final summary
        self._display_summary()
    
    def execute_plan_in_batches(self, user_query: str, num_batches: int, show_screenshots: bool = False):
        """Execute the plan divided into batches, each batch executed at once"""
        
        if not self.current_plan:
            print(colored("No plan to execute!", color='red'))
            return
        
        # Reset for new execution
        self.completed_steps = []
        self.execution_history = []
        
        # Divide steps into batches
        total_steps = len(self.current_plan)
        batch_size = max(1, total_steps // num_batches)
        
        print("\n" + "="*60)
        print(colored(f"\n🚀 Executing {total_steps} steps in {num_batches} batches...\n", color='green', attrs=['bold']))
        
        # Show screenshot info
        vision_status = "📸 Screenshots ENABLED" if self.agent.use_vision else "🚫 Screenshots DISABLED (faster execution)"
        print(colored(f"{vision_status}\n", color='cyan'))
        
        if show_screenshots:
            print(colored(f"📊 Screenshot info will be displayed for each iteration\n", color='yellow'))
        
        batch_num = 0
        for i in range(0, total_steps, batch_size):
            batch_num += 1
            batch_steps = self.current_plan[i:i + batch_size]
            
            if not batch_steps:
                continue
            
            print("="*60)
            print(colored(f"\n📦 BATCH {batch_num}/{num_batches}", color='cyan', attrs=['bold']))
            print(colored(f"   Executing steps {i+1} to {min(i+batch_size, total_steps)}", color='yellow'))
            print("="*60 + "\n")
            
            # Format all steps in this batch as a single instruction
            batch_instruction = f"""TASK: {user_query}

You are executing BATCH {batch_num} of {num_batches}.

STEPS TO COMPLETE IN THIS BATCH (execute ALL in sequence):

"""
            for step in batch_steps:
                batch_instruction += f"""
Step {step['step_number']}: {step['description']}
  → Expected: {step['expected_outcome']}
"""
            
            batch_instruction += """

INSTRUCTIONS:
1. Execute ALL steps above in sequence
2. Verify each expected outcome as you go
3. Complete all steps in this batch
4. Report results when done

Begin execution now."""
            
            # Execute the batch
            print(colored(f"⚡ Executing {len(batch_steps)} steps with unlimited iterations...\n", color='green'))
            
            # Show screenshot status for each execution
            if show_screenshots:
                screenshot_msg = "Taking screenshots each iteration" if self.agent.use_vision else "NO screenshots (text-only mode)"
                print(colored(f"   📸 {screenshot_msg}\n", color='cyan'))
            
            # Track batch execution time
            batch_start = time.time()
            print(colored(f"⏱️  Batch started at: {datetime.now().strftime('%H:%M:%S')}\n", color='cyan'))
            
            # Use monitoring for batch execution
            result = self.monitor.invoke_with_monitoring(batch_instruction)
            
            # Check for loop in batch execution
            if hasattr(result, 'loop_detected') and result.loop_detected:
                print(colored("\n🆘 LOOP DETECTED in batch execution!\n", color='red', attrs=['bold']))
                print(colored("   Agent is repeating same error. Consider:", color='yellow'))
                print(colored("   - Using alternative approach", color='yellow'))
                print(colored("   - Breaking batch into smaller parts", color='yellow'))
                print(colored("   - Manual intervention\n", color='yellow'))
            
            batch_time = time.time() - batch_start
            self.timing_stats['batch_times'].append({
                'batch_num': batch_num,
                'steps': len(batch_steps),
                'time': batch_time,
                'success': result.error is None
            })
            
            # Display timing breakdown
            print(colored(f"\n⏱️  Batch {batch_num} Timing:", color='yellow', attrs=['bold']))
            print(colored(f"   Total time: {batch_time:.2f}s", color='yellow'))
            print(colored(f"   Avg per step: {batch_time/len(batch_steps):.2f}s", color='yellow'))
            print(colored(f"   Screenshot mode: {'ENABLED' if self.agent.use_vision else 'DISABLED'}", color='yellow'))
            
            # Record the execution
            for step in batch_steps:
                execution_record = {
                    'step_number': step['step_number'],
                    'description': step['description'],
                    'query': batch_instruction,
                    'result': result.content if not result.error else None,
                    'error': result.error,
                    'success': result.error is None
                }
                self.execution_history.append(execution_record)
                
                if result.error is None:
                    self.completed_steps.append(step)
            
            if result.error:
                error_msg = f"Batch {batch_num} Failed: {result.error}"
                print(colored(f"\n❌ {error_msg}\n", color='red', attrs=['bold']))
                
                # Show toast notification for failure
                show_toast(
                    f"Batch {batch_num}/{num_batches} Failed",
                    f"Steps {i+1}-{min(i+batch_size, total_steps)} failed",
                    "fail"
                )
                
                # Ask if should continue
                retry = input(f"Would you like to (r)etry this batch, (s)kip to next, or (a)bort? ").strip().lower()
                
                if retry == 'r':
                    # Retry this batch
                    batch_num -= 1
                    i -= batch_size
                    continue
                elif retry == 'a':
                    print(colored("\n⛔ Execution aborted by user.\n", color='red', attrs=['bold']))
                    break
                else:
                    print(colored(f"\n⏭️  Skipping to next batch...\n", color='yellow'))
                    continue
            else:
                success_msg = f"Batch {batch_num} Completed Successfully ({len(batch_steps)} steps)"
                print(colored(f"\n✅ {success_msg}\n", color='green', attrs=['bold']))
                
                # Show toast notification for success
                show_toast(
                    f"Batch {batch_num}/{num_batches} Complete! ✅",
                    f"Steps {i+1}-{min(i+batch_size, total_steps)} successful",
                    "success"
                )
        
        # Display final summary
        self._display_summary()
    
    def _format_step_query(self, step: dict, original_query: str, use_alternative: bool = False) -> str:
        """Format a step into a query for the agent"""
        
        context = ""
        if self.completed_steps:
            context = "\n\n📋 Context - Already Completed:\n"
            for i, completed_step in enumerate(self.completed_steps, 1):
                context += f"  ✅ Step {i}: {completed_step['description']}\n"
        
        # Choose which approach to use
        if use_alternative and 'alternative_approach' in step and step['alternative_approach']:
            action_description = step['alternative_approach']
            approach_note = "\n⚠️ NOTE: Primary approach failed twice. Using ALTERNATIVE approach below."
        else:
            action_description = step['description']
            approach_note = ""
        
        # Create explicit, isolated instruction with verification requirement
        query = f"""🎯 EXECUTE AND VERIFY THIS SPECIFIC STEP ONLY
{approach_note}

⚡ EXECUTION PRIORITY (Use in this order):
1. 🖥️ Shell Tool (PowerShell commands) - Most efficient and reliable
2. ⌨️ Shortcut Tool (Keyboard shortcuts) - Fast and accurate
3. 🖱️ GUI Tools (Click/Type) - Only if terminal/keyboard won't work

⚠️ CRITICAL REQUIREMENTS:
1. Complete ONLY the action described below
2. PREFER Shell Tool or Shortcut Tool over clicking when possible
3. VERIFY the expected result was achieved
4. Do NOT continue to other steps

📌 YOUR TASK FOR THIS STEP:
{action_description}

🎯 EXPECTED RESULT (MUST VERIFY):
{step['expected_outcome']}

✅ VERIFICATION PROCESS:
1. Execute the action
2. Check the current desktop state
3. CONFIRM the expected result was achieved
4. If expected result NOT achieved, report the issue
5. Only use Done Tool if verification confirms success

⛔ STOP CONDITION:
After executing the action and VERIFYING the expected result:
- If SUCCESS and matches expected outcome → Use Done Tool
- If FAILED or doesn't match expected → Report the failure
- Do NOT proceed to any other actions
{context}

💡 COMMON POWERSHELL COMMANDS (Shell Tool):
- Open app: Start-Process notepad | Start-Process chrome | Start-Process explorer
- File ops: Copy-Item, Move-Item, Remove-Item, New-Item, Get-Content, Set-Content
- Navigation: Set-Location "C:\\path" | Get-ChildItem | Test-Path
- Text: "text" | Set-Content file.txt | Get-Content file.txt | Add-Content
- System: Get-Process | Stop-Process | Get-Service | Start-Service

⌨️ ESSENTIAL KEYBOARD SHORTCUTS (Shortcut Tool):
- Apps: Win (Start), Win+R (Run), Win+E (Explorer), Win+S (Search), Win+D (Desktop)
- Editing: Ctrl+C (Copy), Ctrl+V (Paste), Ctrl+X (Cut), Ctrl+Z (Undo), Ctrl+S (Save)
- Navigation: Alt+Tab (Switch), Alt+F4 (Close), F2 (Rename), F5 (Refresh)
- Menus: Alt+F (File), Alt+E (Edit), Alt+V (View), Ctrl+N (New), Ctrl+O (Open)

IMPORTANT: You MUST verify that "{step['expected_outcome']}" actually happened before completing this step."""
        
        return query
    
    def _display_summary(self):
        """Display execution summary with timing statistics"""
        
        successful = sum(1 for record in self.execution_history if record['success'])
        total = len(self.execution_history)
        
        print("\n" + "="*60)
        print(colored("\n📊 Execution Summary\n", color='cyan', attrs=['bold']))
        print("="*60)
        print(f"\nTotal Steps: {total}")
        print(f"Successful: {colored(str(successful), 'green')}")
        print(f"Failed: {colored(str(total - successful), 'red')}")
        print(f"Success Rate: {colored(f'{(successful/total*100):.1f}%', 'yellow')}")
        
        # Display timing statistics
        print("\n" + "="*60)
        print(colored("\n⏱️  Performance Breakdown\n", color='yellow', attrs=['bold']))
        print("="*60)
        
        # Planner LLM time
        if self.timing_stats['planner_llm_time'] > 0:
            print(colored(f"\n🧠 Planner LLM Time: {self.timing_stats['planner_llm_time']:.2f}s", color='cyan'))
        
        # Batch execution times
        if self.timing_stats['batch_times']:
            print(colored(f"\n⚡ Agent Execution Times:", color='green', attrs=['bold']))
            total_exec_time = 0
            for batch_info in self.timing_stats['batch_times']:
                status = "✅" if batch_info['success'] else "❌"
                print(colored(f"   {status} Batch {batch_info['batch_num']}: {batch_info['time']:.2f}s ({batch_info['steps']} steps, avg {batch_info['time']/batch_info['steps']:.2f}s/step)", color='yellow'))
                total_exec_time += batch_info['time']
            
            self.timing_stats['agent_execution_time'] = total_exec_time
            print(colored(f"\n   Total execution: {total_exec_time:.2f}s", color='green', attrs=['bold']))
        
        # Total time
        total_time = self.timing_stats['planner_llm_time'] + self.timing_stats['agent_execution_time']
        self.timing_stats['total_time'] = total_time
        
        print(colored(f"\n🏁 Total Time: {total_time:.2f}s", color='cyan', attrs=['bold']))
        
        # Time breakdown percentages
        if total_time > 0:
            planner_pct = (self.timing_stats['planner_llm_time'] / total_time) * 100
            exec_pct = (self.timing_stats['agent_execution_time'] / total_time) * 100
            
            print(colored(f"\n📊 Time Distribution:", color='magenta'))
            print(colored(f"   Planner: {planner_pct:.1f}% ({self.timing_stats['planner_llm_time']:.2f}s)", color='cyan'))
            print(colored(f"   Execution: {exec_pct:.1f}% ({self.timing_stats['agent_execution_time']:.2f}s)", color='green'))
        
        # Screenshot info
        screenshot_status = "ENABLED" if self.agent.use_vision else "DISABLED"
        screenshot_impact = " (saves ~3x time)" if not self.agent.use_vision else " (slower but visual verification)"
        print(colored(f"\n📸 Screenshots: {screenshot_status}{screenshot_impact}", color='yellow'))
        
        print("\n" + "="*60 + "\n")
        
        # Display detailed results
        self.console.print("\n[bold underline]Detailed Results:[/bold underline]\n")
        for record in self.execution_history:
            status_icon = "✅" if record['success'] else "❌"
            status_color = "green" if record['success'] else "red"
            alt_badge = " ✨[used alternative]" if record.get('used_alternative', False) else ""
            
            self.console.print(
                f"{status_icon} [bold]Step {record['step_number']}:[/bold] {record['description']}{alt_badge}"
            )
            if record['success']:
                result_text = record['result'][:200] if record['result'] else "Completed"
                self.console.print(f"  [{status_color}]Result: {result_text}...[/{status_color}]\n")
            else:
                self.console.print(f"  [{status_color}]Error: {record['error']}[/{status_color}]\n")


def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    # Initialize LLM for both planner and agent
    planner_llm = ChatOpenRouter(
        model="openai/gpt-4o",
        api_key=api_key,
        temperature=0.3  # Slightly higher temperature for creative planning
    )
    
    agent_llm = ChatOpenRouter(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        api_key=api_key,
        temperature=0.2
    )
    
    # Initialize Fallback LLM (activates after 3 failures)
    fallback_llm = ChatOpenRouter(
        model="google/gemini-2.5-flash-image",  # More powerful model for difficult tasks
        api_key=api_key,
        temperature=0.2
    )
    
    # Initialize Agent with default settings
    # Note: max_steps can be adjusted per mode
    agent = Agent(
        llm=agent_llm,
        browser=Browser.EDGE,
        use_vision=False,
        auto_minimize=True,
        max_steps=10  # Default for step-by-step modes
    )
    
    # Initialize Planner with fallback model
    planner = PlannerAI(llm=planner_llm, agent=agent, fallback_llm=fallback_llm)
    
    console = Console()
    
    # Display welcome message
    console.print(Panel.fit(
        "[bold cyan]🤖 Windows Use with Planner AI[/bold cyan]\n\n"
        "[yellow]Mode Selection:[/yellow]\n"
        "  [green]1.[/green] Planner AI (step-by-step execution with verification)\n"
        "  [green]2.[/green] Direct Agent (single execution, no planning)\n"
        "  [green]3.[/green] Continuous Mode (plan once, execute multiple times)\n"
        "  [green]4.[/green] Guided Single Execution (detailed plan → agent executes all at once)\n"
        "  [green]5.[/green] ⚡ Terminal-First Mode (maximum keyboard/terminal usage, minimal GUI) ⚡\n",
        border_style="cyan",
        title="Welcome"
    ))
    
    mode = input("\nSelect mode (1, 2, 3, 4, or 5): ").strip()
    
    if mode == "1":
        # Use Planner AI (single execution)
        user_query = input("\nEnter your task: ").strip()
        
        # Ask for custom max_steps per action
        console.print("\n" + "="*60)
        print(colored("⚙️  Configuration:", color='yellow', attrs=['bold']))
        max_steps_input = input("Max iterations per step (press Enter for default 10, 0 for unlimited): ").strip()
        
        if max_steps_input == "0":
            agent.max_steps = 100
            print(colored(f"✅ Using unlimited mode (max 100 iterations per step)\n", color='green'))
        elif max_steps_input.isdigit() and int(max_steps_input) > 0:
            agent.max_steps = int(max_steps_input)
            print(colored(f"✅ Using {agent.max_steps} max iterations per step\n", color='green'))
        else:
            print(colored(f"✅ Using default (10 iterations per step)\n", color='green'))
        
        planner.execute_plan(user_query)
        
    elif mode == "2":
        # Direct agent execution
        user_query = input("\nEnter your task: ").strip()
        print(colored("\n🤖 Executing task directly with Agent...\n", color='blue', attrs=['bold']))
        agent.print_response(query=user_query)
        
    elif mode == "3":
        # Continuous mode - plan once, execute multiple times
        user_query = input("\nEnter your task: ").strip()
        
        print(colored("\n🎯 Continuous Mode: Creating plan once, you can execute it multiple times", color='cyan', attrs=['bold']))
        print(colored("💰 This saves costs by calling the planner LLM only once!\n", color='green', attrs=['bold']))
        
        # Ask for execution batches
        console.print("\n" + "="*60)
        print(colored("⚙️  Configuration:", color='yellow', attrs=['bold']))
        batch_input = input("Divide plan into how many execution batches? (press Enter for step-by-step): ").strip()
        
        # Set agent to unlimited for batch execution
        agent.max_steps = 100  # Unlimited for each batch
        
        # Create plan once
        plan_data = planner.create_plan(user_query)
        planner.current_plan = plan_data['steps']
        planner.display_plan(plan_data)
        
        # Determine batch execution mode
        use_batches = False
        num_batches = 1
        
        if batch_input.isdigit() and int(batch_input) > 0:
            num_batches = int(batch_input)
            total_steps = len(planner.current_plan)
            steps_per_batch = max(1, total_steps // num_batches)
            use_batches = True
            print(colored(f"\n✅ Dividing {total_steps} steps into {num_batches} execution batches", color='green'))
            print(colored(f"   ~{steps_per_batch} steps per batch, unlimited iterations per batch\n", color='cyan'))
        else:
            print(colored(f"✅ Using step-by-step mode (unlimited iterations per step)\n", color='green'))
        
        # Continuous execution loop
        while True:
            console.print("\n" + "="*60)
            execute = input("\n🚀 Execute this plan? (yes/no): ").strip().lower()
            
            if execute not in ['yes', 'y']:
                print("Exiting continuous mode.")
                break
            
            if use_batches:
                # Batch execution mode
                planner.execute_plan_in_batches(user_query, num_batches, show_screenshots=False)
            else:
                # Regular step-by-step execution
                planner.execute_plan(user_query, reuse_plan=True)
            
            # Ask if want to continue
            console.print("\n" + "="*60)
            continue_exec = input("\n🔄 Execute the same plan again? (yes/no): ").strip().lower()
            
            if continue_exec not in ['yes', 'y']:
                print(colored("\n✅ Exiting continuous mode. Plan is saved for this session.\n", color='green'))
                break
                
    elif mode == "4":
        # Guided Single Execution - Plan with detail, execute all at once
        user_query = input("\nEnter your task: ").strip()
        
        print(colored("\n🎯 Guided Single Execution Mode:", color='cyan', attrs=['bold']))
        print(colored("📋 Creating detailed plan...", color='yellow'))
        print(colored("🚀 Then executing everything in ONE agent run\n", color='green'))
        
        # Create detailed plan
        plan_data = planner.create_plan(user_query)
        planner.display_plan(plan_data)
        
        # Ask for confirmation
        console.print("\n" + "="*60)
        proceed = input("\n🚀 Execute this plan in one go? (yes/no): ").strip().lower()
        
        if proceed not in ['yes', 'y']:
            print("Execution cancelled.")
        else:
            # Set unlimited steps for Mode 4 (agent will complete all steps)
            original_max_steps = agent.max_steps
            agent.max_steps = 100  # Very high limit for guided execution
            
            print(colored(f"⚙️  Mode 4: Using unlimited mode (max {agent.max_steps} iterations)\n", color='cyan'))
            
            # Format the detailed plan as a single comprehensive instruction
            detailed_instruction = f"""TASK: {plan_data['task_summary']}

DETAILED EXECUTION PLAN (Follow these steps in order):

"""
            for step in plan_data['steps']:
                detailed_instruction += f"""
Step {step['step_number']}: {step['description']}
  → Expected: {step['expected_outcome']}
"""
            
            detailed_instruction += """

INSTRUCTIONS:
1. Execute ALL steps above in sequence
2. Verify each expected outcome as you go
3. Complete the entire task
4. Report final results

Begin execution now."""
            
            print("\n" + "="*60)
            print(colored("\n🚀 Executing entire plan with Agent...\n", color='green', attrs=['bold']))
            print(colored("📝 Providing detailed plan to agent as context\n", color='cyan'))
            
            # Execute with the detailed plan as context
            result = agent.invoke(detailed_instruction)
            
            # Restore original max_steps
            agent.max_steps = original_max_steps
            
            print("\n" + "="*60)
            if result.error:
                print(colored(f"\n❌ Execution Error: {result.error}\n", color='red', attrs=['bold']))
            else:
                print(colored(f"\n✅ Execution Complete!\n", color='green', attrs=['bold']))
                console.print(Markdown(result.content))
    
    elif mode == "5":
        # Terminal-First Mode - Maximum keyboard/terminal usage, minimal GUI with BATCH EXECUTION
        user_query = input("\nEnter your task: ").strip()
        
        print(colored("\n⚡ TERMINAL-FIRST MODE ACTIVATED", color='green', attrs=['bold']))
        print(colored("🖥️  Prioritizing: Shell Commands → Keyboard Shortcuts → GUI (last resort)", color='cyan'))
        print(colored("⚡ FAST BATCH EXECUTION: Unlimited iterations per batch\n", color='green', attrs=['bold']))
        
        # Add special instructions for terminal-first execution
        agent.instructions.append(
            "🎯 TERMINAL-FIRST EXECUTION MODE:\n"
            "1. ALWAYS try Shell Tool (PowerShell) commands FIRST\n"
            "2. Use Shortcut Tool (keyboard) for quick actions\n"
            "3. Only use Click/Type tools if terminal/keyboard impossible\n\n"
            "PREFER:\n"
            "- Start-Process over Start Menu clicking\n"
            "- Keyboard shortcuts over menu navigation\n"
            "- PowerShell file operations over File Explorer\n"
            "- Ctrl+C/V over right-click menus\n"
            "- Win+R over searching Start Menu\n"
        )
        
        # Create and display plan with terminal-first approach
        plan_data = planner.create_plan(user_query)
        planner.current_plan = plan_data['steps']
        planner.display_plan(plan_data)
        
        console.print("\n" + "="*60)
        console.print("[yellow]⚡ This plan emphasizes terminal commands and keyboard shortcuts[/yellow]")
        console.print("[cyan]📊 Expected benefits: Faster execution, higher reliability, less GUI dependency[/cyan]")
        
        # Ask for configuration - BATCH EXECUTION STYLE
        console.print("\n" + "="*60)
        print(colored("⚙️  Configuration:", color='yellow', attrs=['bold']))
        
        total_steps = len(planner.current_plan)
        
        # Show screenshot status
        vision_status = "📸 Screenshots ENABLED" if agent.use_vision else "🚫 Screenshots DISABLED (faster!)"
        print(colored(f"{vision_status}", color='cyan'))
        
        batch_input = input(f"Divide {total_steps} steps into how many execution batches? (press Enter for {total_steps}, 0 for single batch): ").strip()
        
        # Set agent to unlimited for batch execution (like Mode 4)
        agent.max_steps = 100  # Unlimited iterations per batch
        
        # Determine batch execution mode
        use_batches = True
        num_batches = total_steps  # Default: one batch per step
        
        if batch_input == "0":
            num_batches = 1
            print(colored(f"\n✅ Single batch mode: All {total_steps} steps in ONE execution", color='green'))
            print(colored(f"   ♾️  Unlimited iterations to complete entire task\n", color='cyan'))
        elif batch_input.isdigit() and int(batch_input) > 0:
            num_batches = int(batch_input)
            steps_per_batch = max(1, total_steps // num_batches)
            print(colored(f"\n✅ Dividing {total_steps} steps into {num_batches} execution batches", color='green'))
            print(colored(f"   ~{steps_per_batch} steps per batch, ♾️ unlimited iterations per batch\n", color='cyan'))
        else:
            print(colored(f"\n✅ Default: {total_steps} batches (1 step per batch)", color='green'))
            print(colored(f"   ♾️  Unlimited iterations per step\n", color='cyan'))
        
        # Ask about showing screenshot info
        show_screenshot_info = input("Show screenshot status for each iteration? (y/n, default: y): ").strip().lower()
        show_screenshots = show_screenshot_info != 'n'
        
        # Execute with terminal-first priority using batch mode
        console.print("\n" + "="*60)
        proceed = input("\n🚀 Execute this terminal-first plan? (yes/no): ").strip().lower()
        
        if proceed in ['yes', 'y']:
            # Show starting toast
            show_toast(
                "Terminal-First Mode Started! ⚡",
                f"Executing {total_steps} steps in {num_batches} batches",
                "info"
            )
            
            # Execute in batches with toast notifications
            planner.execute_plan_in_batches(user_query, num_batches, show_screenshots)
            
            # Show completion toast
            show_toast(
                "Execution Complete! 🎉",
                f"All batches finished",
                "success"
            )
        else:
            print("Execution cancelled.")
    
    else:
        print("Invalid mode selected.")

if __name__ == "__main__":
    main()