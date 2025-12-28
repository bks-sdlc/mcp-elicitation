# MCP Elicitation Tutorial

Learn **MCP Elicitation Patterns** with a simple **Todo App** using **FastMCP**.

## Features

- 📊 **Data Discovery Elicitation** - AI discovers todos before acting
- 💬 **User Elicitation** - Interactive todo creation with step-by-step prompts
- ✅ Complete, list, and delete todos (supports multi-completion)
- 🎯 Priority filtering - complete only high/medium/low priority todos
- 🔍 Status tracking and smart filtering

---

## Quick Start

### 1. Install Dependencies

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### 2. Configure MCP Host

**VS Code (with GitHub Copilot)**

Add to `~/Library/Application Support/Code/User/mcp.json`:

```json
{
  "servers": {
    "todo": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/mcp-elicitation/todo"
    }
  }
}
```

**Claude Desktop**

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "todo": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/mcp-elicitation/todo"
    }
  }
}
```

Replace `/path/to/mcp-elicitation/todo` with your actual path.

### 3. Try It Out

Example queries:
- "Show me my todos overview"
- "Create a todo" (interactive prompts)
- "List my todos" (choose filter)
- "Complete my todo" (choose priority filter, then select)
- "Complete todos 1,2,3" (multi-completion)
- "Delete a todo" (select from list)

---

## Project Structure

```
todo/
├── server.py        # FastMCP server with 5 elicitation tools
├── todos.json       # Data storage
├── pyproject.toml   # Dependencies
├── uv.lock          # Locked dependencies
└── README.md        # This file
```

## Available Tools

**Data Discovery:**
- `get_todos_overview()` - Shows all todos with stats

**User Elicitation (Interactive):**
- `create_todo()` - Create todo with prompts
- `list_todos()` - List with filter selection
- `complete_todo()` - Complete with priority filter + selection (multi-todo support)
- `delete_todo()` - Delete with confirmation

---

## Understanding Elicitation

### 1. Data Discovery Elicitation

AI discovers existing data before acting:

```python
@mcp.tool()
def get_todos_overview() -> str:
    """Shows todos with counts and stats"""
    todos = load_todos()
    return formatted_overview
```

**Example:** "Complete my todo"
- AI calls `complete_todo()`
- Step 1: User selects priority filter (e.g., "high")
- Server shows only filtered pending todos
- Step 2: User selects which todo(s) to complete
- Todos completed with confirmation

### 2. User Elicitation (Interactive)

Tools pause to collect structured input step-by-step:

```python
@mcp.tool()
async def create_todo(ctx: Context) -> str:
    result = await ctx.elicit(
        message="Provide todo details",
        response_type=TodoInput
    )
    if result.action == "accept":
        return save_todo(result.data)
```

**Example:** "Create a todo"
- AI asks for title
- AI asks for description  
- AI asks for priority
- Todo created with all details

---

## Troubleshooting

**Server won't start:**
```bash
uv sync
uv run python server.py
```

**Tools not appearing:**
- Verify config file path is correct
- Use absolute paths in config
- Reload VS Code or restart Claude Desktop
- Check MCP host supports elicitation

**Test directly:**
```bash
npx @modelcontextprotocol/inspector uv run python server.py
```

---

## Resources

- **MCP Docs**: https://modelcontextprotocol.io
- **FastMCP**: https://gofastmcp.com
- **FastMCP Elicitation**: https://gofastmcp.com/servers/elicitation
- **UV**: https://docs.astral.sh/uv/

---

## License

MIT License
