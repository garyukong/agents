---
name: basic-memory-assistant
description: Use when the user wants to store, retrieve, or manage persistent knowledge across conversations. This skill interfaces with the Basic Memory MCP server, a local-first knowledge management system that builds a semantic graph from Markdown files. Trigger keywords include basic-memory, remember this, save to memory, search memory, sync knowledge base, persistent memory.
license: AGPL-3.0
compatibility: Requires basic-memory MCP server to be installed and running via Claude Desktop, Codex, OpenClaw, or compatible MCP clients.
metadata:
  version: "1.1.0"
  author: "basicmachines-co"
  category: "memory-management"
---

# Basic Memory AI Assistant Guide

You are equipped to interact with Basic Memory, a local-first knowledge management system that allows you to read, write, and reason about persistent semantic knowledge graphs. Knowledge is stored in standard Markdown files on the user's local machine, ensuring data ownership and offline accessibility.

## Core Workflows

### 1. Storing New Knowledge
When the user asks you to remember something, document a workflow, or save notes:
1. Identify the relevant project context (or ask the user if unspecified).
2. Create a new Markdown file or update an existing one using your file writing tools.
3. **Title Formatting:** If the memory or note relates to a Jira ticket, the title must always be prefixed strictly as `<JIRA ticket>-<short-ticket-description>` (e.g., `PROJ-123-api-auth-update`).
4. **Crucial:** You must always prepend the following YAML frontmatter exactly to ensure the Basic Memory indexer processes the file correctly:
   ```yaml
   ---
   title: "Document Title" # Must use the Jira prefix format if applicable
   date: "YYYY-MM-DD"
   tags: [tag1, tag2]
   aliases: ["Alternate Title"]
   ---

### 2. Retrieving Knowledge
When answering questions that require past context or searching the knowledge base:
1. Use the Basic Memory MCP search tools to query the semantic graph.
2. If necessary, read specific Markdown files referenced in the search results to extract full context.
3. Synthesize the retrieved information into your response, citing the source documents where appropriate.

### 3. Managing Projects
To create or switch between isolated knowledge bases:
1. Use the `basic-memory` CLI to list, initialize, or manage projects.
2. Refer to `references/basic-memory-cli.md` for exact command syntaxes.

## Constraints and Best Practices
- **Format Strictly**: Ensure all Markdown files contain valid YAML frontmatter. Broken or malformed YAML will cause indexing errors and prevent knowledge retrieval.
- **Semantic Linking**: Encourage connecting ideas by adding relevant tags, metadata, and explicit links between related notes.
- **Troubleshooting**: If you encounter connection timeouts, database locks, or synchronization errors, consult `references/troubleshooting.md` for resolution steps before alerting the user.

## External References
- For detailed CLI commands and cloud sync instructions, see the [CLI Reference](references/basic-memory-cli.md).
- For resolving common errors (e.g., MCP connection, database locks, sync failures), see the [Troubleshooting Guide](references/troubleshooting.md).