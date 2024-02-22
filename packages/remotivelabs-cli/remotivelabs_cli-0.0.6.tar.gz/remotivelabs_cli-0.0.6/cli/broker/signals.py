import json
import numbers
import os
import signal as os_signal
from pathlib import Path
from typing import List, TypedDict

import grpc
import plotext as plt
import typer
from rich import print as rich_rprint
from typing_extensions import Annotated

from .lib.broker import Broker
from .lib.errors import ErrorPrinter as err_printer

app = typer.Typer(help=help)


# signal_values:list = list()


class Signals(TypedDict):
    name: str
    signals: List


signal_values = {}


@app.command(help="List signals names on broker")
def signal_names(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option(None, help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY')
):
    try:
        broker = Broker(url, api_key)
        # print("Listing available signals")
        available_signals = broker.list_signal_names()
        print(json.dumps(available_signals))
    except grpc.RpcError as rpc_error:
        err_printer.print_grpc_error(rpc_error)


def read_scripted_code_file(file_path: Path) -> bytes:
    try:
        print(file_path)
        with open(file_path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found. Please check your file path.")
        exit(1)


@app.command()
def subscribe(
        url: str = typer.Option(help="Broker URL", envvar='REMOTIVE_BROKER_URL'),

        api_key: str = typer.Option("", help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY'),
        signal: List[str] = typer.Option(None, help='Signal names to subscribe to, '
                                                    'mandatory when not using script'),
        namespace: List[str] = typer.Option(None, help='Namespaces to subscribe to, '
                                                       'mandatory when not using script',
                                            envvar='REMOTIVE_BROKER_API_KEY'),
        script: Annotated[
            Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                writable=False,
                readable=True,
                resolve_path=True,
                help="Supply a path to Lua script that to use for signal transformation"
            )] = None,
        on_change_only: bool = typer.Option(default=False, help="Only get signal if value is changed"),
        x_plot: bool = typer.Option(default=False,
                                    help="Experimental: Plot the signal in terminal. Note graphs are not aligned by time"),
        x_plot_size: int = typer.Option(default=100, help="Experimental: how many points show for each plot")
        # samples: int = typer.Option(default=0, he)

):
    """
    Sample usage:

    remotive broker signals subscribe  --url http://localhost:50051 --namespace can0 --signal signal1 --signal signal2

    remotive broker signals subscribe  --url http://localhost:50051 --script myvss_script.lua
    """
    if script is None:
        if len(signal) == 0 or len(namespace) == 0:
            err_printer.print_generic_error(
                'You must use include at least one signal and one namespace or use script when subscribing')
            exit(1)

    if script is not None:
        if len(signal) > 0 or len(namespace) > 0:
            err_printer.print_generic_error("You must must not specify namespace or signal when using --script")

    plt.title("Signals")

    def exit_on_ctrlc(sig, frame):
        os._exit(0)

    def on_frame_plot(x):
        global signal_values

        plt.clt()  # to clear the terminal
        plt.cld()  # to clear the data only
        frames = list(x)
        plt.clf()
        plt.subplots(len(list(filter(lambda n: n.startswith("ts_"), signal_values.keys()))))
        plt.theme("pro")

        for frame in frames:
            name = frame['name']

            if not isinstance(frame['value'], numbers.Number):
                # Skip non numberic values
                # TODO - would exit and print info message if I knew how to
                continue

            y = [frame['value']]
            t = [frame['timestamp_us']]

            if name not in signal_values:
                signal_values[name] = [None] * x_plot_size
                signal_values[f"ts_{name}"] = [None] * x_plot_size
            signal_values[name] = signal_values[name] + y
            signal_values[f"ts_{name}"] = signal_values[f"ts_{name}"] + t

            if len(signal_values[name]) > x_plot_size:
                signal_values[name] = signal_values[name][len(signal_values[name]) - x_plot_size:]

            if len(signal_values[f"ts_{name}"]) > x_plot_size:
                signal_values[f"ts_{name}"] = signal_values[f"ts_{name}"][
                                              len(signal_values[f"ts_{name}"]) - x_plot_size:]

        cnt = 1
        for key in signal_values:
            if not key.startswith("ts_"):
                plt.subplot(cnt, 1).plot(signal_values[f"ts_{key}"], signal_values[key], label=key, color=cnt)
                cnt = cnt + 1
        plt.sleep(0.001)  # to add
        plt.show()

    def on_frame_print(x):
        rich_rprint(json.dumps(list(x)))

    os_signal.signal(os_signal.SIGINT, exit_on_ctrlc)

    if x_plot:
        on_frame_func = on_frame_plot
    else:
        on_frame_func = on_frame_print

    try:
        broker = Broker(url, api_key)
        if script is not None:
            script_src = read_scripted_code_file(script)
            broker.subscribe_on_script(script_src, on_frame_func, on_change_only)
        else:
            broker.subscribe(signal, namespace, on_frame_func, on_change_only)
        print("Subscribing to signals, press Ctrl+C to exit")
    except grpc.RpcError as rpc_error:
        err_printer.print_grpc_error(rpc_error)


@app.command(help="List namespaces on broker")
def namespaces(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option(None, help="Cloud Broker API-KEY or access token",
                                    envvar='REMOTIVE_BROKER_API_KEY')
):
    try:
        broker = Broker(url, api_key)
        namespaces_json = broker.list_namespaces()
        print(json.dumps(namespaces_json))
    except grpc.RpcError as rpc_error:
        err_printer.print_grpc_error(rpc_error)
