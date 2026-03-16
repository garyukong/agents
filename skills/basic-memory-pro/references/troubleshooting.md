# Troubleshooting Guide

Use these steps to diagnose and resolve errors encountered while operating the Basic Memory MCP server.

## MCP Connection Issues
- **Check Absolute Paths**: Ensure complete, absolute paths are used in the MCP configuration (e.g., `Claude Desktop config`).
- **Verify Installation**: Confirm `uv tool run basic-memory mcp` executes successfully.
- **Restart Host Applications**: Terminate and reopen both the Terminal and the AI client to re-establish the transport layer.

## Sync & Indexing Issues
- **Verify File Permissions**: Ensure the Basic Memory process has read/write access to the target project directory.
- **Check `.gitignore` Patterns**: Files matching ignore patterns are silently skipped during the sync phase.
- **Reset the Database**: If search yields empty results despite files existing, run `basic-memory reset`. Note: This may take time for large knowledge bases.

## Database & Performance Issues
- **Locked Database**: Close other applications (like SQLite viewers) that might be accessing the database concurrently.
- **Remove Lock Files**: If processes are stuck or hanging, terminate the process (`pkill -f "basic-memory"`) and remove `~/.basic-memory/memory.db-shm` and `~/.basic-memory/memory.db-wal`.
- **Adjust Configuration for Scale**: 
  - To handle high IO latency, add `"sync_delay": 2000` to `~/.basic-memory/config.json`.
  - For massive knowledge bases, increase concurrency by adding `"sync_thread_pool_size": 8`.