# WeKan CLI

Command line client for WeKan REST API - A command-line interface for interacting with WeKan Kanban boards via REST API.

## Installation

Install the package using pip:

```bash
pip install -e .
```

## Quick Start

The CLI can be configured using environment variables or command-line options:

```bash
export WEKAN_URL="https://wekan.example.com"
export WEKAN_TOKEN="your-auth-token"
```

Or provide credentials directly:

```bash
wekancli --url https://wekan.example.com --token your-token boards
```

## Authentication

You can authenticate using either:

1. **Token authentication** (recommended):
   ```bash
   export WEKAN_TOKEN="your-auth-token"
   ```

2. **Username and password**:
   ```bash
   wekancli login --url https://wekan.example.com --username user --password pass
   ```

## Available Commands

### List all boards
```bash
wekancli boards
```

### Get a specific board
```bash
wekancli board <board-id>
```

### List all lists in a board
```bash
wekancli lists <board-id>
```

### List all cards in a list
```bash
wekancli cards <board-id> <list-id>
```

### Create a new board
```bash
wekancli create-board "My New Board"
```

### Create a new list
```bash
wekancli create-list <board-id> "My New List"
```

### Create a new card
```bash
wekancli create-card <board-id> <list-id> "Card Title" --description "Card description"
```

## Output Formats

The CLI supports multiple output formats:

- `json` (default): Formatted JSON output
- `pretty`: Human-readable formatted output
- `simple`: Simple text output

Example:
```bash
wekancli boards --format pretty
```

## Environment Variables

- `WEKAN_URL`: Base URL of your WeKan instance
- `WEKAN_USERNAME`: Your username
- `WEKAN_PASSWORD`: Your password
- `WEKAN_TOKEN`: Authentication token (alternative to username/password)

## Help

For detailed help on any command:

```bash
wekancli --help
wekancli <command> --help
```

## License

MIT License - see LICENSE file for details.
