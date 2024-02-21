import json
import os
import os.path
import sys

import pexpect
import typer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich import print
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

app = typer.Typer()
console = Console()
data = {}


def run_cli():
    global data
    PATH = os.path.dirname(__file__)
    config_filename = f"{PATH}/config.json"
    if not os.path.exists(config_filename):
        with open(config_filename, "w") as f:
            json.dump({}, f)
    data = json.loads(open(config_filename, "r").read())
    app()


def select_environment_option():
    options = data.keys()
    if len(options) == 0:
        print("No Environment found!!!")
        sys.exit()
    completer = WordCompleter(options)
    selected_option = prompt("Select an environment: ", completer=completer)
    return selected_option


def select_server_option(environment):
    options = data.get(environment, {}).keys()
    if len(options) == 0:
        print("No Server found!!!")
        sys.exit()
    completer = WordCompleter(options)
    selected_option = prompt("Select a server: ", completer=completer)
    return selected_option


def list_environments():
    table = Table("Available Environments")
    for env in data:
        table.add_row(env)
    console.print(table)


def list_servers(environment):
    table = Table("Availbale Servers")
    for server in data.get(environment, {}):
        table.add_row(server)
    console.print(table)


def update_config(data):
    PATH = os.path.dirname(__file__)
    with open(f"{PATH}/config.json", "w") as json_file:
        json.dump(data, json_file)


def ssh_interactive_shell(hostname, username, password=None, port=22):
    try:
        # Spawn SSH session
        ssh_newkey = "Are you sure you want to continue connecting"
        p = pexpect.spawn(f"ssh -p {port} {username}@{hostname}")

        # Expect SSH password prompt
        i = p.expect([ssh_newkey, "password:", pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            p.sendline("yes")
            i = p.expect([ssh_newkey, "password:", pexpect.EOF, pexpect.TIMEOUT])

        # Enter SSH password
        if i == 1:
            p.sendline(password)
            p.expect("Last login")

        # Interactive shell
        p.interact()

    except Exception as e:
        print(f"An error occurred: {str(e)}")


@app.command()
def connect_to_server(
    environment: Annotated[
        str,
        typer.Option(help="Environment name", rich_help_panel="Environment name"),
    ],
):
    list_servers(environment)
    server_name = select_server_option(environment)
    if server_name not in data.get(environment):
        print(f"[bold red]ERROR: Server name {server_name} not found![/bold red]")
        sys.exit()
    server_config = data.get(environment, {}).get(server_name)
    user = server_config.get("user")
    host = server_config.get("host")
    print(f"[bold yellow]Environment:{environment} Server:{server_name}![/bold yellow]")
    print(f"[bold green]Connecting to {user}@{host}![/bold green] :boom:")
    ssh_interactive_shell(host, user)


@app.command()
def connect():
    list_environments()
    environment = select_environment_option()
    if environment not in data:
        print(f"[bold red]ERROR: Invalid environment {environment}![/bold red] :boom:")
        sys.exit()
    connect_to_server(environment=environment)


@app.command()
def addenv():
    list_environments()
    environment = prompt("New Environment name: ")
    if environment in data:
        print(f"[bold red]ERROR: Environment {environment} already exists![/bold red]")
        sys.exit()
    data[environment] = {}
    update_config(data)


@app.command()
def addserver():
    list_environments()
    environment = select_environment_option()
    list_servers(environment)
    server_name = prompt("New Server name: ")
    if server_name in data.get(environment, {}):
        print(f"[bold red]ERROR: Server {server_name} already exists![/bold red]")
        sys.exit()
    username = prompt("Server username: ")
    hostname = prompt("Server hostname: ")
    server_data = {"user": username, "host": hostname}
    data[environment][server_name] = server_data
    update_config(data)


@app.command()
def dlserver():
    list_environments()
    environment = select_environment_option()
    list_servers(environment)
    server_name = select_server_option(environment)
    del data[environment][server_name]
    print("[bold green]Success![/bold green] :boom:")
    update_config(data)


@app.command()
def modserver():
    list_environments()
    environment = select_environment_option()
    list_servers(environment)
    server_name = select_server_option(environment)
    server_data = data[environment][server_name]
    user = server_data.get("user")
    host = server_data.get("host")
    print(f"Current Username - [bold]{user}[/bold] Hostname - [bold]{host}[/bold]")
    new_user = prompt("New Username(Press enter if no change): ")
    new_host = prompt("New Hostname(Press enter if no change): ")
    if new_user:
        data[environment][server_name]["user"] = new_user
    if new_host:
        data[environment][server_name]["host"] = new_host
    print("[bold green]Success![/bold green] :boom:")
    update_config(data)
