"""
WeKan CLI - Command line interface for WeKan REST API
"""
import click
import json
import os
import sys
from typing import Optional
from . import __version__
from .client import WeKanClient


def format_output(data, format_type: str = 'json', indent_level: int = 0):
    """
    Format output data for display
    
    Args:
        data: Data to format
        format_type: Output format (json, pretty, simple)
        indent_level: Current indentation level for nested structures
        
    Returns:
        Formatted string
    """
    if format_type == 'json':
        return json.dumps(data, indent=2)
    elif format_type == 'pretty':
        indent = '  ' * indent_level
        if isinstance(data, list):
            result = []
            for item in data:
                if isinstance(item, dict):
                    nested = format_output(item, 'pretty', indent_level + 1)
                    result.append(f"{indent}- {nested.lstrip()}")
                elif isinstance(item, list):
                    nested = format_output(item, 'pretty', indent_level + 1)
                    result.append(f"{indent}- {nested.lstrip()}")
                else:
                    result.append(f"{indent}- {item}")
            return '\n'.join(result)
        elif isinstance(data, dict):
            result = []
            for k, v in data.items():
                if isinstance(v, dict):
                    result.append(f"{indent}{k}:")
                    nested = format_output(v, 'pretty', indent_level + 1)
                    result.append(nested)
                elif isinstance(v, list):
                    result.append(f"{indent}{k}:")
                    nested = format_output(v, 'pretty', indent_level + 1)
                    result.append(nested)
                else:
                    result.append(f"{indent}{k}: {v}")
            return '\n'.join(result)
        else:
            return str(data)
    else:
        return str(data)


def get_client(base_url: Optional[str], username: Optional[str], 
               password: Optional[str], token: Optional[str]) -> WeKanClient:
    """
    Create and return a WeKan client instance
    
    Args:
        base_url: Base URL of WeKan instance
        username: Username for authentication
        password: Password for authentication
        token: Authentication token
        
    Returns:
        WeKanClient instance
    """
    # Get from environment variables if not provided
    base_url = base_url or os.getenv('WEKAN_URL')
    username = username or os.getenv('WEKAN_USERNAME')
    password = password or os.getenv('WEKAN_PASSWORD')
    token = token or os.getenv('WEKAN_TOKEN')
    
    if not base_url:
        click.echo("Error: WeKan URL is required. Provide via --url or WEKAN_URL environment variable.", err=True)
        sys.exit(1)
    
    return WeKanClient(base_url, username, password, token)


@click.group()
@click.version_option(version=__version__)
def main():
    """
    WeKan CLI - Command line interface for WeKan REST API
    
    This tool allows you to interact with WeKan Kanban boards via REST API
    from the command line. It provides commands to manage boards, lists, and cards.
    
    Authentication can be provided via command-line options or environment variables:
    - WEKAN_URL: Base URL of your WeKan instance
    - WEKAN_USERNAME: Your username
    - WEKAN_PASSWORD: Your password
    - WEKAN_TOKEN: Authentication token (alternative to username/password)
    """
    pass


@main.command()
@click.option('--url', help='WeKan instance URL')
@click.option('--username', help='Username for authentication')
@click.option('--password', help='Password for authentication', hide_input=True)
@click.option('--token', help='Authentication token')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty', 'simple']), 
              default='json', help='Output format')
def login(url, username, password, token, output_format):
    """Login to WeKan and get authentication token"""
    if token:
        click.echo("Token provided, no need to login", err=True)
        return
    
    if not username:
        username = click.prompt('Username')
    if not password:
        password = click.prompt('Password', hide_input=True)
    
    client = get_client(url, username, password, None)
    
    try:
        result = client.login()
        click.echo(format_output(result, output_format))
        
        if 'token' in result:
            click.echo(f"\nAuthentication token: {result['token']}", err=True)
            click.echo("Set WEKAN_TOKEN environment variable to use this token:", err=True)
            click.echo(f"export WEKAN_TOKEN={result['token']}", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--url', help='WeKan instance URL')
@click.option('--username', help='Username for authentication')
@click.option('--password', help='Password for authentication', hide_input=True)
@click.option('--token', help='Authentication token')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty', 'simple']), 
              default='json', help='Output format')
def boards(url, username, password, token, output_format):
    """List all boards"""
    client = get_client(url, username, password, token)
    
    try:
        if not token and username and password:
            client.login()
        
        result = client.get_boards()
        click.echo(format_output(result, output_format))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument('board_id')
@click.option('--url', help='WeKan instance URL')
@click.option('--username', help='Username for authentication')
@click.option('--password', help='Password for authentication', hide_input=True)
@click.option('--token', help='Authentication token')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty', 'simple']), 
              default='json', help='Output format')
def board(board_id, url, username, password, token, output_format):
    """Get details of a specific board"""
    client = get_client(url, username, password, token)
    
    try:
        if not token and username and password:
            client.login()
        
        result = client.get_board(board_id)
        click.echo(format_output(result, output_format))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument('board_id')
@click.option('--url', help='WeKan instance URL')
@click.option('--username', help='Username for authentication')
@click.option('--password', help='Password for authentication', hide_input=True)
@click.option('--token', help='Authentication token')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty', 'simple']), 
              default='json', help='Output format')
def lists(board_id, url, username, password, token, output_format):
    """List all lists in a board"""
    client = get_client(url, username, password, token)
    
    try:
        if not token and username and password:
            client.login()
        
        result = client.get_lists(board_id)
        click.echo(format_output(result, output_format))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument('board_id')
@click.argument('list_id')
@click.option('--url', help='WeKan instance URL')
@click.option('--username', help='Username for authentication')
@click.option('--password', help='Password for authentication', hide_input=True)
@click.option('--token', help='Authentication token')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty', 'simple']), 
              default='json', help='Output format')
def cards(board_id, list_id, url, username, password, token, output_format):
    """List all cards in a list"""
    client = get_client(url, username, password, token)
    
    try:
        if not token and username and password:
            client.login()
        
        result = client.get_cards(board_id, list_id)
        click.echo(format_output(result, output_format))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument('title')
@click.option('--url', help='WeKan instance URL')
@click.option('--username', help='Username for authentication')
@click.option('--password', help='Password for authentication', hide_input=True)
@click.option('--token', help='Authentication token')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty', 'simple']), 
              default='json', help='Output format')
def create_board(title, url, username, password, token, output_format):
    """Create a new board"""
    client = get_client(url, username, password, token)
    
    try:
        if not token and username and password:
            client.login()
        
        result = client.create_board(title)
        click.echo(format_output(result, output_format))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument('board_id')
@click.argument('title')
@click.option('--url', help='WeKan instance URL')
@click.option('--username', help='Username for authentication')
@click.option('--password', help='Password for authentication', hide_input=True)
@click.option('--token', help='Authentication token')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty', 'simple']), 
              default='json', help='Output format')
def create_list(board_id, title, url, username, password, token, output_format):
    """Create a new list in a board"""
    client = get_client(url, username, password, token)
    
    try:
        if not token and username and password:
            client.login()
        
        result = client.create_list(board_id, title)
        click.echo(format_output(result, output_format))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument('board_id')
@click.argument('list_id')
@click.argument('title')
@click.option('--description', help='Card description')
@click.option('--url', help='WeKan instance URL')
@click.option('--username', help='Username for authentication')
@click.option('--password', help='Password for authentication', hide_input=True)
@click.option('--token', help='Authentication token')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty', 'simple']), 
              default='json', help='Output format')
def create_card(board_id, list_id, title, description, url, username, password, token, output_format):
    """Create a new card in a list"""
    client = get_client(url, username, password, token)
    
    try:
        if not token and username and password:
            client.login()
        
        result = client.create_card(board_id, list_id, title, description)
        click.echo(format_output(result, output_format))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
