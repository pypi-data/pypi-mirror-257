import select
import sys
import warnings
from enum import Enum
from urllib.parse import urlparse

import httpx
import typer
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from click import ClickException, UsageError
from greml.__version__ import version_callback
from rich.console import Console
from soupsieve.util import SelectorSyntaxError

warnings.filterwarnings("error")

app = typer.Typer()
console = Console()
err_console = Console(stderr=True)


class Error(ClickException):
    def __init__(self, message: str, exit_code=1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class InputType(Enum):
    STDIN = "stdin"
    FILE = "file"
    HTTP = "http"


def type_of_input(input_path):
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
        raise Error("No data on stdin. Please provide input.", 10)
    return sys.stdin.buffer.read().decode()


def get_http(url):
    try:
        return httpx.get(url).text
    except httpx.ConnectError:
        raise Error("Connect error", 11)


def get_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise Error(f"File '{path}' not found", 12)


def display_callback(value):
    if value in ["text", "json"]:
        return value, None
    if value.startswith("attr."):
        attr = value.split(".")
        return attr[0], "".join(attr[1:])
    raise typer.BadParameter("Must be 'text', 'json' or 'attr.ATTR'")


@app.command()
def main(
    input_path: str = typer.Argument(
        None, help="Input file path or URL. If not specified uses stdin.", show_default="stdin"
    ),
    selector: str = typer.Argument(None, help="HTML selector"),
    display: str = typer.Option("text", help="How to display, either 'text', 'json' or 'attr.ATTR'", callback=display_callback),
    _: bool = typer.Option(None, "-v", "--version", callback=version_callback, is_eager=True),
):
    # input_path should be optional and default to stdin. If it's set but the selector isn't then swap them around
    if selector is None and input_path is not None:
        selector = input_path
        input_path = None

    # Get display method and the name of the attr if desired
    display, attr = display[0], display[1]

    if not selector:
        raise UsageError("No selector provided")

    input_type = type_of_input(input_path)

    if input_type == InputType.STDIN:
        html_doc = get_stdin()
    elif input_type == InputType.HTTP:
        html_doc = get_http(input_path)
    elif input_type == InputType.FILE:
        html_doc = get_file(input_path)

    try:
        soup = BeautifulSoup(html_doc, "html.parser")
    except MarkupResemblesLocatorWarning:
        raise Error("Markup resembles a locator rather than content", 14)

    try:
        elements = soup.select(selector)
    except SelectorSyntaxError as exc:
        raise Error(f"Unable to parse selector:\n{exc.context}", 13)

    json_data = []
    for element in elements:
        if display == "text":
            if element_text := element.get_text():
                print(element_text.strip())
        elif display == "json":
            element_json = {"text": element.get_text()}
            element_json.update(element.attrs)
            json_data.append(element_json)
        elif display == "attr":
            if element_attr := element.get(attr):
                print(element_attr)

    if display == "json":
        console.print_json(data=json_data)


if __name__ == "__main__":
    app()
