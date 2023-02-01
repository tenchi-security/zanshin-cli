from collections.abc import Sequence, Mapping
from json import dumps
from typing import Iterator, Dict, Any
from prettytable import PrettyTable
from enum import Enum
import typer

class OutputFormat(str, Enum):
    """
    Used to specify command-line parameters indicating output format.
    """
    JSON = "json"
    TABLE = "table"
    CSV = "csv"
    HTML = "html"

def format_field(value: Any) -> str:
    """
    Function that formats a single field for output on a table or CSV output, in order to deal with nested arrays or
    objects in the JSON outputs of the API
    :param value: the value to format
    :return: a string that is fit for console output
    """
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        if all(isinstance(x, (str, bytes, int, float)) for x in value):
            return ", ".join([str(x) for x in value])
        else:
            return dumps(value)
    elif isinstance(value, Mapping):
        return dumps(value)
    else:
        return value


def output_iterable(iterator: Iterator[Dict], empty: Any = None, _each_iteration_function: Any = None) -> None:
    """
    Function that iterates over a series of dicts representing JSON objects returned by API list operations, and which
    outputs them using typer.echo in the specified format. Will use streaming processing for JSON, all others need to
    load all responses in memory in a PrettyTable prior to output, which could be problematic for large number of
    entries
    :param _each_iteration_function:
    :param empty:
    :param iterator: the iterator containing the JSON objects
    :return: None
    """
    global global_options

    global_options['entries'] = 0
    if global_options['format'] is OutputFormat.JSON:
        for entry in iterator:
            typer.echo(dumps(entry, indent=4))
            global_options['entries'] += 1
            if _each_iteration_function:
                _each_iteration_function()
    else:
        table = PrettyTable()
        for entry in iterator:
            if not table.field_names:
                table.field_names = sorted(entry.keys())
            else:
                for k in entry.keys():
                    if k not in table.field_names:
                        table.add_column(k, [empty] * global_options['entries'])
            table.add_row([format_field(entry.get(fn, empty)) for fn in table.field_names])
            global_options['entries'] += 1
            if _each_iteration_function:
                _each_iteration_function()
        if global_options['format'] is OutputFormat.TABLE:
            typer.echo(table.get_string())
        elif global_options['format'] is OutputFormat.CSV:
            typer.echo(table.get_csv_string())
        elif global_options['format'] is OutputFormat.HTML:
            typer.echo(table.get_html_string())
        else:
            raise NotImplementedError(f"unexpected format type {global_options['format']}")


def dump_json(out: [Dict, any]) -> None:
    typer.echo(dumps(out, indent=4))