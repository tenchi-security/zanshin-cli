from collections.abc import Mapping, Sequence
from json import dumps
from typing import Any, Dict, Iterator, Union

import typer
from prettytable import PrettyTable

import src.config.sdk as sdk_config
from src.lib.models import OutputFormat


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


def dump_json(out: Union[dict, any]) -> None:
    typer.echo(dumps(out, indent=4))


def output_iterable(
    iterator: Iterator[Dict], empty: Any = None, _each_iteration_function: Any = None
) -> None:
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

    sdk_config.entries = 0
    if sdk_config.format is OutputFormat.JSON:
        for entry in iterator:
            typer.echo(dumps(entry, indent=4))
            sdk_config.entries += 1
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
                        table.add_column(k, [empty] * sdk_config.entries)
            table.add_row(
                [format_field(entry.get(fn, empty)) for fn in table.field_names]
            )
            sdk_config.entries += 1
            if _each_iteration_function:
                _each_iteration_function()
        if sdk_config.format is OutputFormat.TABLE:
            typer.echo(table.get_string())
        elif sdk_config.format is OutputFormat.CSV:
            typer.echo(table.get_csv_string())
        elif sdk_config.format is OutputFormat.HTML:
            typer.echo(table.get_html_string())
        else:
            raise NotImplementedError(f"unexpected format type {sdk_config.format}")
