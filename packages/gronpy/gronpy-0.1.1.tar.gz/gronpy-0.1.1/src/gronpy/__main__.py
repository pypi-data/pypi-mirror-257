import decimal
import json
import select
import sys
from pathlib import Path
from urllib.parse import urlparse

import httpx
import typer
from js2py import PyJsException
from rich.console import Console
from rich.syntax import Syntax

from gronpy.__version__ import version_callback
from gronpy.gron import gron
from gronpy.ungron import ungron

app = typer.Typer()
console = Console()
err_console = Console(stderr=True)


class InputType:
    STDIN = "stdin"
    FILE = "file"
    HTTP = "http"


def type_of_input(input_path: str) -> Path:
    if not input_path:
        return InputType.STDIN

    try:
        parsed_url = urlparse(input_path)
    except Exception:
        return InputType.FILE

    if parsed_url.scheme:
        if parsed_url.scheme in ["http", "https"]:
            return InputType.HTTP
    else:
        return InputType.FILE


def has_data_on_stdin():
    return select.select([sys.stdin], [], [], 0.0)[0]


def get_stdin():
    if sys.stdin.isatty() or not has_data_on_stdin():
        err_console.print("Error: No data on stdin. Please provide input.")
        raise typer.Exit(1)
    return sys.stdin.buffer.read().decode()


def get_http(url):
    try:
        return httpx.get(url).text
    except httpx.ConnectError:
        err_console.print("Error: Connect error")
        raise typer.Exit(2)


def get_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        err_console.print(f"Error: File '{path}' not found")
        raise typer.Exit(3)


@app.command()
def main(
    input_path: str = typer.Argument(
        None, help="Input file path or URL. If not specified uses stdin.", show_default="stdin"
    ),
    gron_action: bool = typer.Option(True, "--gron/--ungron", help="Transform JSON into GRON or back again"),
    color: bool = typer.Option(True, help="Enable colouring in terminal."),
    _: bool = typer.Option(None, "-v", "--version", callback=version_callback, is_eager=True),
):
    input_type = type_of_input(input_path)

    if input_type == InputType.STDIN:
        data = get_stdin()
    elif input_type == InputType.HTTP:
        data = get_http(input_path)
    elif input_type == InputType.FILE:
        data = get_file(input_path)

    if gron_action:
        try:
            json_data = json.loads(data, parse_float=decimal.Decimal)
        except json.JSONDecodeError:
            err_console.print("Error: Unable to parse JSON")
            raise typer.Exit(4)
        gron_data = gron(json_data, "json")
        if console.is_terminal:
            if not color:
                print(gron_data)
            else:
                console.print(Syntax(gron_data, "javascript", background_color="default"))
        else:
            console.file.write(gron_data)
    else:
        try:
            ungron_data = ungron(data)
        except PyJsException:
            err_console.print("Error: Unable to parse gron file")
            raise typer.Exit(5)
        if console.is_terminal:
            if not color:
                print(ungron_data)
            else:
                console.print_json(ungron_data)
        else:
            console.file.write(ungron_data)


if __name__ == "__main__":
    app()
