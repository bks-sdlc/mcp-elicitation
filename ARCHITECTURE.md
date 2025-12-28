# Architecture Documentation

## System Overview

This document describes the end-to-end architecture of the MCP Todo application, including how VS Code (MCP Host) communicates with the FastMCP server.

```
┌─────────────────────────────────────────────────────────────────┐
│                          VS Code (MCP Host)                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │               GitHub Copilot / MCP Client                   │ │
│  │  - User interacts via chat interface                       │ │
│  │  - Sends natural language requests                         │ │
│  │  - Displays responses to user                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              │ MCP Protocol (JSON-RPC)          │
│                              │ over stdio                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastMCP Server Process                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  uv run python server.py                                   │ │
│  │                                                            │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │         MCP Protocol Handler (FastMCP)               │ │ │
│  │  │  - Receives JSON-RPC requests                        │ │ │
│  │  │  - Routes to appropriate tools                       │ │ │
│  │  │  - Handles elicitation flow                          │ │ │
│  │  │  - Returns responses                                 │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                          │                                 │ │
│  │  ┌───────────────────────┴──────────────────────────────┐ │ │
│  │  │              5 MCP Tools                             │ │ │
│  │  │                                                      │ │ │
│  │  │  1. get_todos_overview()                            │ │ │
│  │  │     └─ Data discovery pattern                       │ │ │
│  │  │                                                      │ │ │
│  │  │  2. create_todo(ctx)                                │ │ │
│  │  │     └─ User elicitation pattern                     │ │ │
│  │  │                                                      │ │ │
│  │  │  3. list_todos(ctx)                                 │ │ │
│  │  │     └─ User elicitation pattern                     │ │ │
│  │  │                                                      │ │ │
│  │  │  4. complete_todo(ctx)                              │ │ │
│  │  │     └─ User elicitation pattern                     │ │ │
│  │  │                                                      │ │ │
│  │  │  5. delete_todo(ctx)                                │ │ │
│  │  │     └─ User elicitation pattern                     │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                          │                                 │ │
│  │  ┌───────────────────────┴──────────────────────────────┐ │ │
│  │  │           Data Layer (JSON Storage)                  │ │ │
│  │  │                                                      │ │ │
│  │  │  - load_todos()                                     │ │ │
│  │  │  - save_todos()                                     │ │ │
│  │  │  - File: todos.json                                 │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   todos.json         │
                    │  (Data Persistence)  │
                    └──────────────────────┘
```

---

## Component Details

### 1. MCP Host: VS Code

**Role**: The client application that hosts the MCP connection

**Components**:
- **VS Code MCP Client**: Built into VS Code, handles MCP protocol communication
- **GitHub Copilot Extension**: Provides chat interface and uses VS Code's MCP client to interact with servers
- **MCP Client**: Built into Copilot, handles MCP protocol communication

**Configuration** (`~/Library/Application Support/Code/User/mcp.json`):
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

**Responsibilities**:
- Launch MCP server process via `uv run python server.py`
- Maintain stdio connection to server
- Send user requests as JSON-RPC messages
- Handle elicitation prompts
- Display results to user

---

### 2. MCP Server: FastMCP (server.py)

**Role**: The server that provides todo management functionality via MCP protocol

**Technology Stack**:
- **FastMCP**: Python framework for building MCP servers
- **Python 3.10+**: Runtime
- **uv**: Package manager and virtual environment

**Key Components**:

#### A. MCP Protocol Handler (FastMCP Framework)
- Automatically handles JSON-RPC communication
- Tool registration and discovery
- Request routing
- Error handling
- Elicitation flow management

#### B. Tool Functions (5 total)

**Data Discovery Tool**:
1. **`get_todos_overview()`**
   - Returns statistics and overview
   - No parameters required
   - Enables AI to understand current state

**User Elicitation Tools** (use `ctx.elicit()`):
2. **`create_todo(ctx: Context)`**
   - Collects: title, description, priority
   - Uses `TodoInput` dataclass
   - Returns confirmation message

3. **`list_todos(ctx: Context)`**
   - Collects: filter status (all/pending/completed)
   - Uses `ListFilter` dataclass
   - Returns formatted list

4. **`complete_todo(ctx: Context)`**
   - Step 1: Collects priority filter (all/high/medium/low)
   - Step 2: Shows filtered pending todos
   - Step 3: Collects comma-separated todo IDs for multi-completion
   - Uses two elicitation calls (PriorityFilterInput, TodoIdsInput)
   - Updates status and timestamp for multiple todos

5. **`delete_todo(ctx: Context)`**
   - Shows all todos first
   - Collects: todo_id
   - Uses `DeleteTodoInput` dataclass
   - Removes todo permanently

#### C. Data Layer
- **`load_todos()`**: Read from todos.json
- **`save_todos(todos)`**: Write to todos.json
- Simple JSON file storage

---

### 3. Data Storage: todos.json

**Format**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high",
    "status": "pending",
    "created_at": "2025-12-27T10:30:00",
    "completed_at": null
  }
]
```

**Schema**:
- `id`: Unique integer identifier
- `title`: Task name (string)
- `description`: Details (string)
- `priority`: "high", "medium", or "low"
- `status`: "pending" or "completed"
- `created_at`: ISO 8601 timestamp
- `completed_at`: ISO 8601 timestamp or null

---

## Communication Flow

### 1. Standard Tool Call (Data Discovery)

```
User: "Show me my todos"
   │
   ▼
[VS Code MCP Client]
   │ JSON-RPC: tools/call
   │ { "name": "get_todos_overview" }
   ▼
[FastMCP Server]
   │ Execute tool
   │ load_todos()
   │ Format response
   ▼
[VS Code MCP Client]
   │ Display result
   ▼
User sees: "📋 **Your Todos Overview**\n..."
```

### 2. Elicitation Flow (User Input Collection)

```
User: "Create a todo"
   │
   ▼
[VS Code MCP Client]
   │ JSON-RPC: tools/call
   │ { "name": "create_todo" }
   ▼
[FastMCP Server]
   │ Tool executes
   │ Calls ctx.elicit(TodoInput)
   │
   │ JSON-RPC: elicitation/request
   │ { "schema": { "title": "str", "description": "str", ... } }
   ▼
[VS Code MCP Client]
   │ Prompts user for each field:
   │ - "title?"
   │ - "description?"
   │ - "priority?"
   │
   │ JSON-RPC: elicitation/response
   │ { "action": "accept", "data": { ... } }
   ▼
[FastMCP Server]
   │ Receives user input
   │ Creates todo
   │ save_todos()
   │
   │ Returns success message
   ▼
[VS Code MCP Client]
   │ Display result
   ▼
User sees: "✅ **Todo Created!**\n..."
```

---

## MCP Protocol Details

### Protocol: JSON-RPC over stdio

**Communication Channel**:
- VS Code launches server process
- Bidirectional communication via stdin/stdout
- Messages are newline-delimited JSON

### Key Message Types

**1. Tool Discovery** (on startup):
```json
Request:  { "method": "tools/list" }
Response: {
  "tools": [
    {
      "name": "get_todos_overview",
      "description": "Shows what todos exist...",
      "inputSchema": {}
    },
    {
      "name": "create_todo",
      "description": "Create a todo...",
      "inputSchema": {}
    }
    // ... other tools
  ]
}
```

**2. Tool Execution**:
```json
Request: {
  "method": "tools/call",
  "params": {
    "name": "create_todo",
    "arguments": {}
  }
}
```

**3. Elicitation Request** (server → client):
```json
{
  "method": "elicitation/request",
  "params": {
    "message": "Please provide todo details",
    "schema": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "description": { "type": "string" },
        "priority": { "enum": ["high", "medium", "low"] }
      }
    }
  }
}
```

**4. Elicitation Response** (client → server):
```json
{
  "action": "accept",
  "data": {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "medium"
  }
}
```

---

## Elicitation Patterns

### Pattern 1: Data Discovery

**Purpose**: Allow AI to discover existing data before acting

**Implementation**:
- Tool: `get_todos_overview()`
- No user input required
- Returns current state of all todos
- AI can make informed decisions

**Example Use Case**:
```
User: "What's on my todo list?"

Flow:
1. AI calls get_todos_overview()
2. Server loads todos from JSON
3. Returns formatted overview with counts and stats
4. AI presents information to user
5. No user input required
```

### Pattern 2: User Elicitation

**Purpose**: Collect structured data interactively

**Implementation**:
- Tools: `create_todo()`, `list_todos()`, `complete_todo()`, `delete_todo()`
- Use `await ctx.elicit(response_type=DataClass)`
- FastMCP handles the elicitation protocol
- User provides data step-by-step

**Example Use Case**:
```
User: "Add a todo"

Flow:
1. AI calls create_todo()
2. Server elicits TodoInput
3. VS Code prompts: "title?"
4. User: "Buy groceries"
5. VS Code prompts: "description?"
6. User: "Milk, eggs, bread"
7. VS Code prompts: "priority?"
8. User: "medium"
9. Server creates todo
10. Returns confirmation
```

**Multi-Todo Completion Example**:
```
User: "Complete my todos"

Flow:
1. AI calls complete_todo()
2. First elicitation: priority_filter
3. User selects priority (e.g., "high")
4. Server filters: shows only high priority pending todos
5. Second elicitation: todo_ids
6. User enters "1,3,5" (multiple IDs)
7. Server completes all three todos
8. Returns batch confirmation
```

---

## Data Flow

### Create Todo Flow
```
User Input (VS Code Chat)
   ↓
MCP Client (Copilot)
   ↓ tools/call: create_todo
FastMCP Server
   ↓ ctx.elicit(TodoInput)
MCP Client
   ↓ Collect: title, description, priority
User Input (Form Fields)
   ↓
MCP Client
   ↓ elicitation/response
FastMCP Server
   ↓ Create todo object
   ↓ load_todos()
todos.json (read)
   ↓ todos list
FastMCP Server
   ↓ Append new todo
   ↓ save_todos()
todos.json (write)
   ↓ Success confirmation
FastMCP Server
   ↓ Return message
MCP Client
   ↓ Display
User sees result (VS Code Chat)
```

### List Todos Flow
```
User: "List my todos"
   ↓
MCP Client
   ↓ tools/call: list_todos
FastMCP Server
   ↓ ctx.elicit(ListFilter)
MCP Client
   ↓ Collect: status filter
User: "pending"
   ↓
MCP Client
   ↓ elicitation/response
FastMCP Server
   ↓ load_todos()
todos.json (read)
   ↓ Filter by status
   ↓ Format output
FastMCP Server
   ↓ Return formatted list
MCP Client
   ↓ Display
User sees todos
```

---

## Deployment

### Prerequisites
- Python 3.10+
- uv package manager
- VS Code with GitHub Copilot
- MCP support in Copilot

### Installation
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
cd todo
uv sync
```

### Configuration
1. Create `mcp.json` in VS Code config directory
2. Configure server with `uv run` command
3. Reload VS Code

### Runtime
- Server process launched automatically by VS Code
- Runs in background
- Communicates via stdio
- Terminated when VS Code closes or MCP disabled

---

## Security Considerations

1. **File Access**: Server only accesses `todos.json` in its directory
2. **Validation**: FastMCP validates all input schemas
3. **No Network**: Communication is local stdio only
4. **Isolation**: Server runs in isolated uv virtual environment
5. **User Control**: All operations require user confirmation via elicitation

---

## Performance

- **Startup**: ~500ms (Python + FastMCP initialization)
- **Tool Calls**: <50ms (simple JSON operations)
- **Elicitation**: Network latency + user input time
- **File I/O**: Minimal (small JSON files)

---

## Error Handling

### Server Errors
- FastMCP catches exceptions
- Returns error messages to client
- Server continues running

### Elicitation Errors
- User can decline (cancel operation)
- Validation errors shown in VS Code
- Invalid schemas rejected by FastMCP

### File Errors
- Missing todos.json → creates empty file
- Corrupted JSON → returns error to user
- Write failures → error message displayed

---

## Future Enhancements

1. **Additional Tools**:
   - Search todos
   - Update todo
   - Add tags/categories
   - Set due dates

2. **Better Storage**:
   - SQLite database
   - Backup functionality
   - Version history

3. **Advanced Features**:
   - Recurring todos
   - Subtasks
   - Attachments
   - Notifications

---

## References

- **MCP Specification**: https://modelcontextprotocol.io
- **FastMCP Documentation**: https://gofastmcp.com
- **Elicitation Guide**: https://gofastmcp.com/servers/elicitation
- **GitHub Repository**: https://github.com/bks-sdlc/mcp-elicitation
