"""
Client command for MCPM
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from mcpm.utils.config import ConfigManager
from mcpm.utils.client_registry import ClientRegistry

console = Console()
config_manager = ConfigManager()

@click.command()
@click.argument("client_name", required=False)
@click.option("--list", is_flag=True, help="List all supported clients")
def client(client_name, list):
    """Manage the active MCP client.
    
    If no arguments are provided, shows the current active client.
    If a client name is provided, sets it as the active client.
    
    Examples:
        mcpm client         # Show current active client
        mcpm client --list  # List all supported clients
        mcpm client claude-desktop  # Set Claude Desktop as the active client
    """
    # Get the list of supported clients
    supported_clients = ClientRegistry.get_supported_clients()
    
    # List all supported clients if requested
    if list:
        table = Table(title="Supported MCP Clients")
        table.add_column("Client Name", style="cyan")
        table.add_column("Status", style="green")
        
        active_client = ClientRegistry.get_active_client()
        
        for client in sorted(supported_clients):
            status = "[bold green]ACTIVE[/]" if client == active_client else ""
            table.add_row(client, status)
            
        console.print(table)
        return
    
    # If no client name specified, show the current active client
    if not client_name:
        active_client = ClientRegistry.get_active_client()
        console.print(f"Current active client: [bold cyan]{active_client}[/]")
        
        # Display some helpful information about setting clients
        console.print("\nTo change the active client, run:")
        for client in sorted(supported_clients):
            if client != active_client:
                console.print(f"  mcpm client {client}")
        
        # Display a note about using --list
        console.print("\nTo see all supported clients:")
        console.print("  mcpm client --list")
        return
    
    # Set the active client if provided
    if client_name not in supported_clients:
        console.print(f"[bold red]Error:[/] Unknown client: {client_name}")
        console.print(f"Supported clients: {', '.join(sorted(supported_clients))}")
        return
    
    # Set the active client
    if client_name == ClientRegistry.get_active_client():
        console.print(f"[bold yellow]Note:[/] {client_name} is already the active client")
        return
    
    # Attempt to set the active client
    success = ClientRegistry.set_active_client(client_name)
    if success:
        console.print(f"[bold green]Success:[/] Active client set to {client_name}")
        
        # Provide information about what this means
        panel = Panel(
            f"The active client ({client_name}) will be used for all MCP operations.\n"
            f"Commands like 'mcpm list', 'mcpm status', and 'mcpm install' will now operate on {client_name}.",
            title="Active Client Changed",
            border_style="green"
        )
        console.print(panel)
    else:
        console.print(f"[bold red]Error:[/] Failed to set {client_name} as the active client")
