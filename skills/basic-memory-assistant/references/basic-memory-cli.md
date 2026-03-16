# Basic Memory CLI Reference

Basic Memory provides a command-line interface to manage local and cloud-synced knowledge bases. Use these commands via terminal execution when required.

## Core Local Commands
- `basic-memory init [project-name]`: Creates a new directory and initializes a project configuration.
- `basic-memory sync`: Crawls the project directory and updates the search index. Always run this after manually adding or editing notes outside of the AI workflow.
- `basic-memory run`: Starts the MCP server manually (useful for debugging and validating local routing).
- `basic-memory project list`: Lists all configured projects to help manage multiple isolated knowledge bases.
- `basic-memory status`: Checks the current file synchronization status.
- `basic-memory reset`: Resets the local SQLite/PostgreSQL database and re-indexes all files.

## Cloud & Synchronization Commands
- `bm cloud login`: Authenticate with Basic Memory cloud services.
- `bm cloud setup`: Initialize cloud synchronization for a specific project directory.
- `bm cloud upload`: Upload local files to cloud projects (can bypass `.gitignore` filtering if explicitly flagged).
- `bm cloud bisync --name [project] --resync`: Perform a bidirectional sync with the cloud. Required for initial syncs or resolving state corruption.