# Simple Todo - MCP Elicitation Tutorial

Learn **MCP Elicitation Patterns** with a clean, simple **Todo App** using **FastMCP**.

## What You'll Build

A simple **Todo Manager** demonstrating both MCP elicitation patterns:
- 📊 **Data Discovery** - AI learns what todos exist before acting
- 💬 **User Elicitation** - Interactive todo creation with prompts
- ✅ Complete, list, and delete todos
- 🎯 Priority levels and status tracking

## Perfect For Learning

- **MCP Beginners**: Simple, focused example
- **Students**: Clear elicitation pattern demonstration  
- **Developers**: Easy to understand and extend
- **YouTube Tutorials**: Clean code for teaching

---

## Quick Start (2 Minutes)

## Quick Start (2 Minutes)

### Step 1: Install Dependencies

```bash
# Clone or download this project
cd mcp

# Install everything (uv + dependencies)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

### Step 2: Run the Server

```bash
uv run python simple-todo/server.py
```

Server is running! Press Ctrl+C to stop (we'll configure VS Code next).

### Step 3: Choose Your MCP Host

#### Option A: VS Code (Recommended for Developers)

1. **Install an MCP-compatible Extension**:
   
   Choose one of these (click to install):
   - **Cline** - Most popular MCP agent (`saoudrizwan.claude-dev`)
   - **Roo Code** - Team of AI agents (`rooveterinaryinc.roo-cline`)
   - **Copilot MCP** - Works with GitHub Copilot (`automatalabs.copilot-mcp`)

2. **The configuration file is already created!**
   
   Located at: `~/Library/Application Support/Code/User/mcp.json`
   
   Configuration format:
   ```json
   {
     "servers": {
       "simple-todo": {
         "type": "stdio",
         "command": "/Users/personal/Documents/youtube/projects/mcp/.venv/bin/python",
         "args": [
           "/Users/personal/Documents/youtube/projects/mcp/simple-todo/server.py"
         ],
         "env": {
           "VIRTUAL_ENV": "/Users/personal/Documents/youtube/projects/mcp/.venv",
           "PATH": "/Users/personal/Documents/youtube/projects/mcp/.venv/bin:/usr/local/bin:/usr/bin:/bin"
         }
       }
     },
     "inputs": []
   }
   ```
   
   **Note**: Replace the absolute paths with your actual project location.

3. **Using with GitHub Copilot**:
   - Open GitHub Copilot Chat in VS Code
   - Type `@mcp` to see available MCP tools
   - Or just ask: "Show me my todos"
   - Copilot will automatically discover and use the todo tools

4. **Start using it**:
   - Try: "Show me an overview of my todos"
   - Or: "I want to create a todo interactively"
   - Or: "Add a todo to buy groceries"

#### Option B: Claude Desktop (Alternative)

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "simple-todo": {
      "command": "/Users/personal/Documents/youtube/projects/mcp/.venv/bin/python",
      "args": [
        "/Users/personal/Documents/youtube/projects/mcp/simple-todo/server.py"
      ],
      "env": {
        "VIRTUAL_ENV": "/Users/personal/Documents/youtube/projects/mcp/.venv",
        "PATH": "/Users/personal/Documents/youtube/projects/mcp/.venv/bin:/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

**Note**: Replace the absolute paths with your actual project location.

Restart Claude Desktop after saving.

#### Option C: Direct Testing (Command Line)

Test the server directly:

```bash
# Start server
uv run python simple-todo/server.py

# In another terminal, test with MCP inspector
npx @modelcontextprotocol/inspector uv run python simple-todo/server.py
```

### Step 4: Try It Out!

Example queries to test:

```
"Show me my todos overview"
"Create a todo interactively"
"List my todos" (will ask which status to filter)
"Complete a todo" (will show available todos and ask which one)
"Delete a todo" (will show all todos and ask which to delete)
```

🎉 Your Simple Todo MCP is live - **every tool uses elicitation**!

---

## What's Included

### 🛠️ Tools (All Use Elicitation!)

**Data Discovery Elicitation:**
1. **get_todos_overview()** - Shows all todos with counts by status/priority (AI discovers data first)

**User Elicitation (Interactive):**
2. **create_todo_interactive()** - Create a todo with step-by-step prompts
3. **list_todos_interactive()** - List todos with filter selection
4. **complete_todo_interactive()** - Complete a todo (shows available todos first)
5. **delete_todo_interactive()** - Delete a todo with confirmation (shows all todos first)

**Every single tool demonstrates elicitation patterns!**

### 📁 Project Structure

```
mcp/
├── README.md                           # You are here
├── pyproject.toml                     # UV dependencies
├── .venv/                             # Virtual environment
└── simple-todo/
    ├── server.py                      # FastMCP server (5 tools - all use elicitation!)
    └── todos.json                     # JSON data storage
```

---

## Understanding Elicitation

MCP supports **two types of elicitation** - both are implemented in this project!

### 1. 📊 Data Discovery Elicitation

**What it is**: Tools that let AI discover your data before acting on it.

**Tool**: `get_todos_overview()`

**Without Data Discovery ❌:**
```
You: "Complete my high priority todo"
AI: 🤷 Doesn't know what todos exist
AI: 🤷 Doesn't know their IDs or priorities
AI: ❌ Can't complete the task
AI: ❌ Has to ask you for the ID
```

**With Data Discovery ✅:**
```
You: "Complete my high priority todo"
AI: 🔍 Calls get_todos_overview() FIRST
AI: ✅ Discovers: Todo #3 "Finish report" is high priority
AI: 🎯 Calls complete_todo(3)
AI: ✅ Task completed automatically!
```

**Key Concept**: The AI discovers what exists before trying to modify it. This makes interactions smarter and more natural.

### 2. 💬 User Elicitation (Interactive Input)

**What it is**: Tools that pause and ask users for information step-by-step.

**Tool**: `create_todo_interactive()`

**Traditional Way:**
```
AI needs all parameters upfront:
add_todo(title="?", description="?", priority="?")
User must provide everything in one go
```

**Interactive Way:**
```
You: "Create a todo interactively"
AI: Asks "What's the task title?"
You: "Finish project report"
AI: Asks "Any additional details?"
You: "Include charts and conclusion section"
AI: Asks "What's the priority? (high/medium/low)"
You: "high"
AI: ✅ Todo created with all details!
AI: 🎯 Provides confirmation and next steps
```

**Key Concept**: Break complex input into simple steps. Better user experience for creating structured data.

### Try Both Patterns

**Data Discovery:**
```
"Show me my todos overview"
"What todos do I have?"
"List all pending tasks"
```

**User Elicitation:**
```
"Create a todo interactively"
"I want to add a task with guided prompts"
```

---

## Example Interactions

### Data Discovery
```
You: "What todos do I have?"
AI: Calls get_todos_overview()
AI: Shows 3 pending, 2 completed
AI: Shows breakdown by priority
AI: Lists your pending tasks
```

### Interactive Todo Creation
```
You: "Create a todo interactively"
AI: Prompts for title
You: "Buy groceries"
AI: Prompts for description
You: "Milk, eggs, bread"
AI: Prompts for priority
You: "medium"
AI: ✅ Todo #1 created!
```

### Interactive List with Filter
```
You: "List my todos"
AI: Asks which status to show
You: "pending"
AI: Shows all pending todos with details
```

### Interactive Complete
```
You: "Complete a todo"
AI: Shows all pending todos first (data discovery!)
AI: Asks which todo to complete
You: "1"
AI: ✅ Todo #1 completed!
```

### Interactive Delete
```
You: "Delete a todo"
AI: Shows all todos (so you can see what to delete)
AI: Asks which todo to delete
You: "2"
AI: 🗑️ Todo #2 deleted!
```

---

## How It Works

### FastMCP Magic

FastMCP makes building MCP servers incredibly simple:

```python
from fastmcp import FastMCP, Context
from dataclasses import dataclass

mcp = FastMCP("Simple Todo")

# Data Discovery Elicitation
@mcp.tool()
def get_todos_overview() -> str:
    """Shows what todos exist - AI discovers data first"""
    todos = load_todos()
    # Returns counts, priorities, pending tasks
    return overview

# User Elicitation
@dataclass
class TodoInput:
    title: str
    description: str
    priority: str

@mcp.tool()
def create_todo_interactive(ctx: Context) -> str:
    """Interactive todo creation with prompts"""
    result = ctx.elicit(
        prompt="Provide todo details...",
        schema=TodoInput
    )
    match result:
        case ctx.AcceptedElicitation(value=todo):
            # User provided input - create todo
            return save_todo(todo)
        case ctx.DeclinedElicitation():
            return "Cancelled"

mcp.run()
```

That's it! FastMCP handles all the MCP protocol complexity.

### Key Features Used

1. **JSON Storage** - Simple file-based data persistence
2. **Priority Levels** - High, medium, low task organization
3. **Status Tracking** - Pending and completed states
4. **Timestamps** - Creation and completion tracking
5. **Clean Code** - Easy to read and understand
6. **Pure Elicitation** - Every tool uses data discovery or user elicitation!
7. **Under 300 lines** - Perfect for learning!

---

## Customizing Your Todo App

### Add New Fields

Edit [simple-todo/server.py](simple-todo/server.py) to add tags or categories:

```python
@dataclass
class TodoInput:
    title: str
    description: str
    priority: Literal["high", "medium", "low"]
    tags: str = ""  # Add tags field
    category: str = "general"  # Add category
```

### Add Due Dates

```python
from datetime import datetime, date

@dataclass
class TodoInput:
    title: str
    description: str
    priority: str
    due_date: str = ""  # Format: YYYY-MM-DD

# Then in the tool:
if todo_input.due_date:
    new_todo["due_date"] = todo_input.due_date
```

### Add Subtasks

```python
@mcp.tool()
def add_subtask(parent_id: int, subtask_title: str) -> str:
    """Add a subtask to an existing todo"""
    todos = load_todos()
    for todo in todos:
        if todo['id'] == parent_id:
            if 'subtasks' not in todo:
                todo['subtasks'] = []
            todo['subtasks'].append(subtask_title)
            save_todos(todos)
            return f"✅ Subtask added to todo #{parent_id}"
    return f"❌ Todo #{parent_id} not found"
```

---

## Troubleshooting

### Server won't start
```bash
# Check Python version (need 3.10+)
python3 --version

# Re-sync dependencies
uv sync

# Test server manually
uv run python simple-todo/server.py
```

### VS Code: MCP tools not appearing
- ✅ GitHub Copilot installed and activated
- ✅ MCP configuration at: `~/Library/Application Support/Code/User/mcp.json`
- ✅ Configuration uses proper format with `servers`, `type`, `command`, `args`, and `env`
- ✅ Configuration points to correct Python interpreter (.venv/bin/python)
- ✅ Reload VS Code window (`Cmd+Shift+P` → "Reload Window")
- ✅ Try `@mcp` in GitHub Copilot Chat

### Claude Desktop: Can't find the server
- ✅ Use **absolute paths** in config (not relative)
- ✅ Point directly to Python interpreter: `.venv/bin/python`
- ✅ Include `env` section with VIRTUAL_ENV and PATH
- ✅ Restart Claude Desktop after config changes
- ✅ Check logs: `~/Library/Logs/Claude/mcp*.log`

### Tools not appearing
- ✅ Server must start without errors
- ✅ Config file must be valid JSON
- ✅ Path in config must point to activated Python interpreter
- ✅ Include environment variables in config
- ✅ Try restarting your MCP host (VS Code/Claude)

### Database errors
Data is auto-created on first run. If issues:
```bash
rm simple-todo/todos.json  # Delete and recreate
uv run python simple-todo/server.py  # Server creates empty file
```

### Testing the server directly
Use the MCP Inspector to debug:
```bash
npx @modelcontextprotocol/inspector uv run python simple-todo/server.py
```
Opens a web UI at http://localhost:6274 to test all tools interactively.

---

## Why This Stack?

### FastMCP
- ⚡ **Simple API** - Decorator-based, minimal boilerplate
- 🎯 **Elicitation Support** - Built-in ctx.elicit() for interactive tools
- 📝 **Type hints** - Uses Python dataclasses for structured input
- 🚀 **Fast development** - Production-ready servers in minutes

### UV
- ⚡ **10-100x faster** than pip
- 🦀 **Written in Rust** - Modern and reliable
- 🎯 **Auto-manages venv** - No activation needed
- 📦 **Better dependencies** - Fewer conflicts

### SQLite
- 💾 **File-based** - No server needed
- 🔒 **Reliable** - ACID compliant
- 📦 **Built-in** - Comes with Python
- ⚡ **Fast** - Perfect for development and small-scale production

### JSON
- 📝 **Simple** - Human-readable format
- 🔧 **Easy to edit** - Can modify manually if needed
- 📦 **Built-in** - No extra dependencies
- 🎯 **Perfect for learning** - Clear data structure

---

## Learn More

### Resources
- **MCP Docs**: https://modelcontextprotocol.io
- **FastMCP**: https://gofastmcp.com
- **FastMCP Elicitation**: https://gofastmcp.com/servers/elicitation
- **UV**: https://docs.astral.sh/uv/

### What is MCP?
Model Context Protocol lets AI assistants securely access:
- Your local data files
- Todo lists and notes
- External APIs
- Local tools and services
- Any data source you control

### What is Elicitation?
Two key patterns:
1. **Data Discovery** - AI learns what exists before acting (prevents errors and assumptions)
2. **User Elicitation** - AI prompts users for structured input interactively (better UX for complex data)

Always implement both patterns in your MCP servers for the best experience!

---

## YouTube Video Ideas

### Video 1: "Build an AI Todo App in 5 Minutes with MCP"
- Show the quick start
- Create todos interactively
- Demonstrate data discovery
- Complete and list todos

### Video 2: "Understanding MCP Elicitation - The Right Way"
- Explain both patterns (discovery + user elicitation)
- Show get_todos_overview() in action
- Demonstrate interactive todo creation
- Compare with traditional approach

### Video 3: "Extend Your MCP Todo App"
- Add tags and categories
- Add due dates
- Create subtasks
- Add filtering and sorting

### Video 4: "Build Production MCP Servers"
- Error handling best practices
- Data validation
- Logging and monitoring
- Security considerations

---

## Tips for Success

✅ **Start with discovery** - Always call get_todos_overview() first to see what exists
✅ **Everything is interactive** - Every tool asks for input or shows context first
✅ **Pure elicitation** - No tool requires parameters upfront
✅ **Keep it simple** - The code is under 300 lines for a reason
✅ **Read the code** - [simple-todo/server.py](simple-todo/server.py) is well-commented
✅ **Use absolute paths** - In mcp.json configuration
✅ **Reload VS Code** - After config changes
✅ **Check the data** - Look at [simple-todo/todos.json](simple-todo/todos.json) to see what's stored  

---

## License

MIT License - Free to use for learning and production!

---

## Next Steps

1. ✅ Follow Quick Start guide
2. 🔍 Try get_todos_overview() to see data discovery
3. 📝 Create a todo interactively
4. 🛠️ Add your own custom field (tags, due dates)
5. 🎥 Understand elicitation and build your own MCP server!

**Ready to start?**

```bash
uv sync
uv run python knowledge-base/server.py
```

Then configure Claude Desktop and start building your second brain! 🧠✨
