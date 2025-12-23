
import asyncio
import json
import subprocess
import os
import sys

# Try to import mcp, if not available, we'll need to install it
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    # This script is intended to be run where 'mcp' is available.
    # If this fails, the user needs to install 'mcp' package.
    sys.exit("Error: 'mcp' package not found. Please install it using 'pip install mcp'")

# Initialize FastMCP server
mcp = FastMCP("opencode-swarm")

SWARM_CLI = "swarm"

async def run_swarm_tool(tool_name: str, args: dict = None) -> str:
    """Run a swarm tool via CLI and return the output."""
    cmd = [SWARM_CLI, "tool", tool_name]

    if args:
        cmd.extend(["--json", json.dumps(args)])

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode().strip() or stdout.decode().strip()
            return f"Error executing {tool_name}: {error_msg}"

        output = stdout.decode().strip()

        # Try to parse as JSON to return clean data if possible
        try:
            result = json.loads(output)
            if isinstance(result, dict):
                if result.get("success") and "data" in result:
                    return json.dumps(result["data"], indent=2)
                elif not result.get("success") and "error" in result:
                    return f"Tool Error: {result['error'].get('message', 'Unknown error')}"
            return output
        except json.JSONDecodeError:
            return output

    except Exception as e:
        return f"Exception executing {tool_name}: {str(e)}"

# Define tools based on swarm tool --list output

# --- Agent Mail Tools ---

@mcp.tool()
async def agentmail_init(project_path: str, agent_name: str = None, task_description: str = None) -> str:
    """Initialize Agent Mail session."""
    args = {"project_path": project_path}
    if agent_name: args["agent_name"] = agent_name
    if task_description: args["task_description"] = task_description
    return await run_swarm_tool("agentmail_init", args)

@mcp.tool()
async def agentmail_send(to: list[str], subject: str, body: str, thread_id: str = None, importance: str = None, ack_required: bool = None) -> str:
    """Send message to other agents."""
    args = {"to": to, "subject": subject, "body": body}
    if thread_id: args["thread_id"] = thread_id
    if importance: args["importance"] = importance
    if ack_required is not None: args["ack_required"] = ack_required
    return await run_swarm_tool("agentmail_send", args)

@mcp.tool()
async def agentmail_inbox(limit: int = 5, urgent_only: bool = None, since_ts: str = None) -> str:
    """Fetch inbox (CONTEXT-SAFE: bodies excluded)."""
    args = {"limit": limit}
    if urgent_only is not None: args["urgent_only"] = urgent_only
    if since_ts: args["since_ts"] = since_ts
    return await run_swarm_tool("agentmail_inbox", args)

@mcp.tool()
async def agentmail_read_message(message_id: int) -> str:
    """Fetch ONE message body by ID."""
    return await run_swarm_tool("agentmail_read_message", {"message_id": message_id})

@mcp.tool()
async def agentmail_summarize_thread(thread_id: str, include_examples: bool = None) -> str:
    """Summarize thread (PREFERRED over fetching all messages)."""
    args = {"thread_id": thread_id}
    if include_examples is not None: args["include_examples"] = include_examples
    return await run_swarm_tool("agentmail_summarize_thread", args)

@mcp.tool()
async def agentmail_reserve(paths: list[str], ttl_seconds: int = None, exclusive: bool = None, reason: str = None) -> str:
    """Reserve file paths for exclusive editing."""
    args = {"paths": paths}
    if ttl_seconds: args["ttl_seconds"] = ttl_seconds
    if exclusive is not None: args["exclusive"] = exclusive
    if reason: args["reason"] = reason
    return await run_swarm_tool("agentmail_reserve", args)

@mcp.tool()
async def agentmail_release(paths: list[str] = None, reservation_ids: list[int] = None) -> str:
    """Release file reservations."""
    args = {}
    if paths: args["paths"] = paths
    if reservation_ids: args["reservation_ids"] = reservation_ids
    return await run_swarm_tool("agentmail_release", args)

@mcp.tool()
async def agentmail_ack(message_id: int) -> str:
    """Acknowledge a message."""
    return await run_swarm_tool("agentmail_ack", {"message_id": message_id})

@mcp.tool()
async def agentmail_search(query: str, limit: int = None) -> str:
    """Search messages by keyword."""
    args = {"query": query}
    if limit: args["limit"] = limit
    return await run_swarm_tool("agentmail_search", args)

@mcp.tool()
async def agentmail_health() -> str:
    """Check if Agent Mail server is running."""
    return await run_swarm_tool("agentmail_health", {})

# --- Beads Tools ---

@mcp.tool()
async def beads_create(title: str, type: str = "task", priority: int = 2, description: str = None, parent_id: str = None) -> str:
    """Create a new bead with type-safe validation."""
    args = {"title": title, "type": type, "priority": priority}
    if description: args["description"] = description
    if parent_id: args["parent_id"] = parent_id
    return await run_swarm_tool("beads_create", args)

@mcp.tool()
async def beads_create_epic(epic_title: str, subtasks: list[dict], epic_description: str = None) -> str:
    """Create epic with subtasks in one atomic operation."""
    args = {"epic_title": epic_title, "subtasks": subtasks}
    if epic_description: args["epic_description"] = epic_description
    return await run_swarm_tool("beads_create_epic", args)

@mcp.tool()
async def beads_query(status: str = None, type: str = None, ready: bool = None, limit: int = 20) -> str:
    """Query beads with filters."""
    args = {"limit": limit}
    if status: args["status"] = status
    if type: args["type"] = type
    if ready is not None: args["ready"] = ready
    return await run_swarm_tool("beads_query", args)

@mcp.tool()
async def beads_update(id: str, status: str = None, description: str = None, priority: int = None) -> str:
    """Update bead status/description."""
    args = {"id": id}
    if status: args["status"] = status
    if description: args["description"] = description
    if priority is not None: args["priority"] = priority
    return await run_swarm_tool("beads_update", args)

@mcp.tool()
async def beads_close(id: str, reason: str) -> str:
    """Close a bead with reason."""
    return await run_swarm_tool("beads_close", {"id": id, "reason": reason})

@mcp.tool()
async def beads_start(id: str) -> str:
    """Mark a bead as in-progress."""
    return await run_swarm_tool("beads_start", {"id": id})

@mcp.tool()
async def beads_ready() -> str:
    """Get the next ready bead (unblocked, highest priority)."""
    return await run_swarm_tool("beads_ready", {})

@mcp.tool()
async def beads_sync(auto_pull: bool = None) -> str:
    """Sync beads to git and push (MANDATORY at session end)."""
    args = {}
    if auto_pull is not None: args["auto_pull"] = auto_pull
    return await run_swarm_tool("beads_sync", args)

@mcp.tool()
async def beads_link_thread(bead_id: str, thread_id: str) -> str:
    """Add metadata linking bead to Agent Mail thread."""
    return await run_swarm_tool("beads_link_thread", {"bead_id": bead_id, "thread_id": thread_id})


# --- Swarm Tools ---

@mcp.tool()
async def swarm_init(project_path: str = None) -> str:
    """Initialize swarm session and check tool availability."""
    args = {}
    if project_path: args["project_path"] = project_path
    return await run_swarm_tool("swarm_init", args)

@mcp.tool()
async def swarm_select_strategy(task: str, codebase_context: str = None) -> str:
    """Analyze task and recommend decomposition strategy."""
    args = {"task": task}
    if codebase_context: args["codebase_context"] = codebase_context
    return await run_swarm_tool("swarm_select_strategy", args)

@mcp.tool()
async def swarm_plan_prompt(task: str, strategy: str = None, max_subtasks: int = None, context: str = None, query_cass: bool = None, cass_limit: int = None) -> str:
    """Generate strategy-specific decomposition prompt."""
    args = {"task": task}
    if strategy: args["strategy"] = strategy
    if max_subtasks: args["max_subtasks"] = max_subtasks
    if context: args["context"] = context
    if query_cass is not None: args["query_cass"] = query_cass
    if cass_limit: args["cass_limit"] = cass_limit
    return await run_swarm_tool("swarm_plan_prompt", args)

@mcp.tool()
async def swarm_decompose(task: str, max_subtasks: int = None, context: str = None, query_cass: bool = None, cass_limit: int = None) -> str:
    """Generate decomposition prompt for breaking task into subtasks."""
    args = {"task": task}
    if max_subtasks: args["max_subtasks"] = max_subtasks
    if context: args["context"] = context
    if query_cass is not None: args["query_cass"] = query_cass
    if cass_limit: args["cass_limit"] = cass_limit
    return await run_swarm_tool("swarm_decompose", args)

@mcp.tool()
async def swarm_validate_decomposition(response: str) -> str:
    """Validate a decomposition response against BeadTreeSchema."""
    return await run_swarm_tool("swarm_validate_decomposition", {"response": response})

@mcp.tool()
async def swarm_status(epic_id: str, project_key: str) -> str:
    """Get status of a swarm by epic ID."""
    return await run_swarm_tool("swarm_status", {"epic_id": epic_id, "project_key": project_key})

@mcp.tool()
async def swarm_progress(project_key: str, agent_name: str, bead_id: str, status: str, message: str = None, progress_percent: float = None, files_touched: list[str] = None) -> str:
    """Report progress on a subtask to coordinator."""
    args = {"project_key": project_key, "agent_name": agent_name, "bead_id": bead_id, "status": status}
    if message: args["message"] = message
    if progress_percent is not None: args["progress_percent"] = progress_percent
    if files_touched: args["files_touched"] = files_touched
    return await run_swarm_tool("swarm_progress", args)

@mcp.tool()
async def swarm_complete(project_key: str, agent_name: str, bead_id: str, summary: str, evaluation: str = None, files_touched: list[str] = None, skip_ubs_scan: bool = None) -> str:
    """Mark subtask complete, release reservations, notify coordinator."""
    args = {"project_key": project_key, "agent_name": agent_name, "bead_id": bead_id, "summary": summary}
    if evaluation: args["evaluation"] = evaluation
    if files_touched: args["files_touched"] = files_touched
    if skip_ubs_scan is not None: args["skip_ubs_scan"] = skip_ubs_scan
    return await run_swarm_tool("swarm_complete", args)

@mcp.tool()
async def swarm_record_outcome(bead_id: str, duration_ms: int, success: bool, error_count: int = None, retry_count: int = None, files_touched: list[str] = None, criteria: list[str] = None, strategy: str = None) -> str:
    """Record subtask outcome for implicit feedback scoring."""
    args = {"bead_id": bead_id, "duration_ms": duration_ms, "success": success}
    if error_count is not None: args["error_count"] = error_count
    if retry_count is not None: args["retry_count"] = retry_count
    if files_touched: args["files_touched"] = files_touched
    if criteria: args["criteria"] = criteria
    if strategy: args["strategy"] = strategy
    return await run_swarm_tool("swarm_record_outcome", args)

@mcp.tool()
async def swarm_subtask_prompt(agent_name: str, bead_id: str, epic_id: str, subtask_title: str, files: list[str], subtask_description: str = None, shared_context: str = None) -> str:
    """Generate the prompt for a spawned subtask agent."""
    args = {"agent_name": agent_name, "bead_id": bead_id, "epic_id": epic_id, "subtask_title": subtask_title, "files": files}
    if subtask_description: args["subtask_description"] = subtask_description
    if shared_context: args["shared_context"] = shared_context
    return await run_swarm_tool("swarm_subtask_prompt", args)

@mcp.tool()
async def swarm_spawn_subtask(bead_id: str, epic_id: str, subtask_title: str, files: list[str], subtask_description: str = None, shared_context: str = None) -> str:
    """Prepare a subtask for spawning with Task tool."""
    args = {"bead_id": bead_id, "epic_id": epic_id, "subtask_title": subtask_title, "files": files}
    if subtask_description: args["subtask_description"] = subtask_description
    if shared_context: args["shared_context"] = shared_context
    return await run_swarm_tool("swarm_spawn_subtask", args)

@mcp.tool()
async def swarm_complete_subtask(bead_id: str, task_result: str, files_touched: list[str] = None) -> str:
    """Handle subtask completion after Task agent returns."""
    args = {"bead_id": bead_id, "task_result": task_result}
    if files_touched: args["files_touched"] = files_touched
    return await run_swarm_tool("swarm_complete_subtask", args)

@mcp.tool()
async def swarm_evaluation_prompt(bead_id: str, subtask_title: str, files_touched: list[str]) -> str:
    """Generate self-evaluation prompt for a completed subtask."""
    return await run_swarm_tool("swarm_evaluation_prompt", {"bead_id": bead_id, "subtask_title": subtask_title, "files_touched": files_touched})

if __name__ == "__main__":
    mcp.run()
