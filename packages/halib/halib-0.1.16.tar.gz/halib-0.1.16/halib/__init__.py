__all__ = [
    "cmd",
    "fs",
    "filetype",
    "np",
    "pd",
    "timebudget",
    "tqdm",
    "logger",
    "inspect",
    "rprint",
    "console",
    "pprint",
    "plt",
    "console",
    "console_log",
    "ConsoleLog",
]

import numpy as np
import pandas as pd
from .filetype import *
from .sys import cmd
from .sys import filesys as fs

# for log
from loguru import logger
from rich import inspect
from rich import print as rprint
from rich.console import Console
from rich.pretty import pprint
from timebudget import timebudget
from tqdm import tqdm
import matplotlib.pyplot as plt

console = Console()


def console_log(func):
    def wrapper(*args, **kwargs):
        console.rule(f"<{func.__name__}>")
        result = func(*args, **kwargs)
        console.rule(f"</{func.__name__}>")
        return result

    return wrapper

class ConsoleLog:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        console.rule(f"<{self.message}>")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        console.rule(f"</{self.message}>")
        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred.")
            print(f"Exception message: {exc_value}")
