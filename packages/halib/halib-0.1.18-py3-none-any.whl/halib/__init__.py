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
    "re"
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
import re

console = Console()

def norm_str(in_str):
    # Replace one or more whitespace characters with a single underscore
    norm_string = re.sub(r"\s+", "_", in_str)
    # Remove leading and trailing spaces
    norm_string = norm_string.strip()
    return norm_string

def console_rule(msg, do_norm_msg=True, is_end_tag=False):
    msg = norm_str(msg) if do_norm_msg else msg
    if is_end_tag:
        console.rule(f"</{msg}>")
    else:
        console.rule(f"<{msg}>")

def console_log(func):
    def wrapper(*args, **kwargs):
        console_rule(func.__name__)
        result = func(*args, **kwargs)
        console_rule(func.__name__, is_end_tag=True)
        return result

    return wrapper

class ConsoleLog:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        console_rule(self.message)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        console_rule(self.message, is_end_tag=True)
        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred.")
            print(f"Exception message: {exc_value}")
