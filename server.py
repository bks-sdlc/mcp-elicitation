"""
Simple Todo MCP Server - Demonstrating Elicitation Patterns

A clean, easy-to-understand MCP server showing:
1. Data Discovery Elicitation - AI learns what todos exist
2. User Elicitation - Interactive todo creation

Perfect for learning MCP and elicitation patterns!
"""

from fastmcp import FastMCP, Context
from dataclasses import dataclass
from typing import Literal
import json
from pathlib import Path
from datetime import datetime

# Initialize FastMCP server
mcp = FastMCP("Simple Todo")

# Data storage
BASE_DIR = Path(__file__).parent
TODOS_FILE = BASE_DIR / "todos.json"


def load_todos():
    """Load todos from JSON file."""
    if not TODOS_FILE.exists():
        return []
    with open(TODOS_FILE, 'r') as f:
        return json.load(f)


def save_todos(todos):
    """Save todos to JSON file."""
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=2)


@mcp.tool()
def get_todos_overview() -> str:
    """
    Shows what todos exist with counts and categories.
    
    Returns:
        Overview of all todos with counts and categories
    """
    todos = load_todos()
    
    if not todos:
        return """📋 **Your Todos** (Empty)

No todos yet! Ready to add your first task.

💡 **Try:**
- Use `create_todo` to add a todo
"""
    
    # Count by status
    pending = [t for t in todos if t['status'] == 'pending']
    completed = [t for t in todos if t['status'] == 'completed']
    
    # Count by priority
    high = [t for t in todos if t['priority'] == 'high']
    medium = [t for t in todos if t['priority'] == 'medium']
    low = [t for t in todos if t['priority'] == 'low']
    
    result = ["📋 **Your Todos Overview**\n"]
    result.append(f"**Total:** {len(todos)} todos")
    result.append(f"**Pending:** {len(pending)} tasks")
    result.append(f"**Completed:** {len(completed)} tasks\n")
    
    result.append("**By Priority:**")
    result.append(f"  🔴 High: {len(high)}")
    result.append(f"  🟡 Medium: {len(medium)}")
    result.append(f"  🟢 Low: {len(low)}\n")
    
    if pending:
        result.append("**Pending Tasks:**")
        for todo in pending[:5]:  # Show first 5
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[todo['priority']]
            result.append(f"  {priority_icon} [{todo['id']}] {todo['title']}")
        if len(pending) > 5:
            result.append(f"  ... and {len(pending) - 5} more")
    
    return "\n".join(result)


@dataclass
class TodoInput:
    """Structure for creating a todo."""
    title: str
    description: str
    priority: Literal["high", "medium", "low"]


@mcp.tool()
async def create_todo(ctx: Context) -> str:
    """
    Create a todo by collecting details step-by-step.
    
    Returns:
        Confirmation message with todo details
    """
    result = await ctx.elicit(
        message="Please provide todo details",
        response_type=TodoInput
    )
    
    if result.action == "accept":
        todo_input = result.data
        # Load existing todos
        todos = load_todos()
        
        # Generate new ID
        new_id = max([t['id'] for t in todos], default=0) + 1
        
        # Create new todo
        new_todo = {
            "id": new_id,
            "title": todo_input.title,
            "description": todo_input.description,
            "priority": todo_input.priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Save
        todos.append(new_todo)
        save_todos(todos)
        
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[todo_input.priority]
        
        return f"""✅ **Todo Created!**

{priority_icon} **{todo_input.title}** (#{new_id})
📝 {todo_input.description}
🎯 Priority: {todo_input.priority}

Use `list_todos` to see all your tasks!
"""
    elif result.action == "decline":
        return "❌ Todo creation cancelled."
    else:
        return "⚠️  Todo creation was cancelled."


@dataclass
class ListFilter:
    """Structure for filtering todos."""
    status: Literal["all", "pending", "completed"]


@mcp.tool()
async def list_todos(ctx: Context) -> str:
    """
    List todos with filter selection.
    
    Returns:
        Formatted list of filtered todos
    """
    result = await ctx.elicit(
        message="""📋 **List Todos**

Which todos would you like to see?

**Status**: all, pending, or completed

Example:
```
status: pending
```
""",
        response_type=ListFilter
    )
    
    if result.action == "accept":
        filter_input = result.data
        todos = load_todos()
        
        if not todos:
            return "📋 No todos found. Use `create_todo` to add one!"
        
        # Filter by status
        if filter_input.status == "pending":
            todos = [t for t in todos if t['status'] == 'pending']
        elif filter_input.status == "completed":
            todos = [t for t in todos if t['status'] == 'completed']
        
        if not todos:
            return f"No {filter_input.status} todos found."
        
        result_lines = [f"📋 **{filter_input.status.title()} Todos** ({len(todos)})\n"]
        
        for todo in todos:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[todo['priority']]
            status_icon = "✅" if todo['status'] == 'completed' else "⏳"
            
            result_lines.append(f"\n{status_icon} {priority_icon} **[{todo['id']}] {todo['title']}**")
            if todo['description']:
                result_lines.append(f"   📝 {todo['description']}")
            result_lines.append(f"   📅 Created: {todo['created_at'][:10]}")
            if todo['completed_at']:
                result_lines.append(f"   ✅ Completed: {todo['completed_at'][:10]}")
        
        return "\n".join(result_lines)
    elif result.action == "decline":
        return "❌ List operation cancelled."
    else:
        return "⚠️  List operation was cancelled."


@dataclass
class CompleteTodoInput:
    """Structure for completing todos."""
    todo_ids: str  # Comma-separated IDs like "1,2,3" or single ID like "1"
    priority_filter: Literal["all", "high", "medium", "low"] = "all"


@mcp.tool()
async def complete_todo(ctx: Context) -> str:
    """
    Mark todos as completed.
    Shows available pending todos (optionally filtered by priority), then asks which to complete.
    Supports completing multiple todos at once.
    
    Returns:
        Confirmation message
    """
    # First ask for priority filter to show relevant todos
    todos = load_todos()
    pending = [t for t in todos if t['status'] == 'pending']
    
    if not pending:
        return "✅ No pending todos to complete!"
    
    # First elicit priority filter
    @dataclass
    class PriorityFilterInput:
        priority_filter: Literal["all", "high", "medium", "low"] = "all"
    
    filter_result = await ctx.elicit(
        message="**Filter by priority?**\nChoose: all, high, medium, or low",
        response_type=PriorityFilterInput
    )
    
    if filter_result.action != "accept":
        return "❌ Complete operation cancelled."
    
    priority_filter = filter_result.data.priority_filter
    
    # Filter pending todos by priority
    if priority_filter != "all":
        pending = [t for t in pending if t['priority'] == priority_filter]
    
    if not pending:
        return f"No pending {priority_filter} priority todos found."
    
    # Build prompt with filtered todos
    prompt_lines = [f"📋 **Complete {priority_filter.title()} Priority Todos**\n\nAvailable todos:\n"]
    for todo in pending:
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[todo['priority']]
        prompt_lines.append(f"  {priority_icon} [{todo['id']}] {todo['title']}")
    
    prompt_lines.append("\n**Which todos would you like to complete?**\n")
    prompt_lines.append("Enter one or more todo IDs (comma-separated for multiple like '1,2,3')\n")
    
    @dataclass
    class TodoIdsInput:
        todo_ids: str
    
    result = await ctx.elicit(
        message="\n".join(prompt_lines),
        response_type=TodoIdsInput
    )
    
    if result.action == "accept":
        # Parse comma-separated IDs
        try:
            todo_ids = [int(id.strip()) for id in result.data.todo_ids.split(',')]
        except ValueError:
            return "❌ Invalid todo IDs format. Please use comma-separated numbers like '1,2,3' or a single number."
        
        completed = []
        not_found = []
        already_completed = []
        
        # Get list of pending todo IDs for validation
        pending_ids = {t['id'] for t in pending}
        
        for todo_id in todo_ids:
            if todo_id not in pending_ids:
                not_found.append(str(todo_id))
                continue
                
            # Find todo in full list and update
            for todo in todos:
                if todo['id'] == todo_id:
                    if todo['status'] == 'completed':
                        already_completed.append(f"#{todo_id} {todo['title']}")
                    else:
                        todo['status'] = 'completed'
                        todo['completed_at'] = datetime.now().isoformat()
                        completed.append(f"#{todo_id} {todo['title']}")
                    break
        
        # Save if any changes were made
        if completed:
            save_todos(todos)
        
        # Build response message
        messages = []
        if completed:
            messages.append(f"✅ **Completed ({len(completed)}):**\n" + "\n".join(f"  • {t}" for t in completed))
        if already_completed:
            messages.append(f"⚠️  **Already completed ({len(already_completed)}):**\n" + "\n".join(f"  • {t}" for t in already_completed))
        if not_found:
            messages.append(f"❌ **Not found in {priority_filter} priority todos:** {', '.join(not_found)}")
        
        return "\n\n".join(messages) if messages else "No todos were completed."
    elif result.action == "decline":
        return "❌ Complete operation cancelled."
    else:
        return "⚠️  Complete operation was cancelled."


@dataclass
class DeleteTodoInput:
    """Structure for deleting a todo."""
    todo_id: int


@mcp.tool()
async def delete_todo(ctx: Context) -> str:
    """
    Delete a todo.
    Shows available todos, then asks which to delete.
    
    Returns:
        Confirmation message
    """
    # First show what's available (data discovery)
    todos = load_todos()
    
    if not todos:
        return "📋 No todos to delete!"
    
    # Build prompt with available todos
    prompt_lines = ["🗑️  **Delete a Todo**\n\nYour todos:\n"]
    for todo in todos:
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[todo['priority']]
        status_icon = "✅" if todo['status'] == 'completed' else "⏳"
        prompt_lines.append(f"  {status_icon} {priority_icon} [{todo['id']}] {todo['title']}")
    
    prompt_lines.append("\n**Which todo would you like to delete?**\n")
    prompt_lines.append("⚠️  This cannot be undone!\n")
    prompt_lines.append("```\ntodo_id: <number>\n```")
    
    result = await ctx.elicit(
        message="\n".join(prompt_lines),
        response_type=DeleteTodoInput
    )
    
    if result.action == "accept":
        input_data = result.data
        for i, todo in enumerate(todos):
            if todo['id'] == input_data.todo_id:
                title = todo['title']
                todos.pop(i)
                save_todos(todos)
                return f"🗑️  Deleted: {title}"
        
        return f"❌ Todo #{input_data.todo_id} not found"
    elif result.action == "decline":
        return "❌ Delete operation cancelled."
    else:
        return "⚠️  Delete operation was cancelled."


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
