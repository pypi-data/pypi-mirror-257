import argparse

import pathtype

from enum import Enum
from pathlib import Path
from time import sleep

from pycomgrader import Grader, GraderError, Status
from rich.console import Console


class StatusMessage(Enum):
    """Enumeration class representing different status messages."""

    AC = "[bold green]accepted[/bold green]"
    WA = "[bold red]wrong answer[/bold red]"
    TLE = "[bold red]time limit exceeded[/bold red]"
    MLE = "[bold red]memory limit exceeded[/bold red]"
    RTE = "[bold yellow]runtime error[/bold yellow]"
    CE = "[bold blue]compile error[/bold blue]"


def cli_grader():
    """Command-line interface for grading C++ programs."""

    parser = argparse.ArgumentParser(description="offline grader for C++ programs")
    parser.add_argument(
        "file",
        type=pathtype.Path(exists=True),
        help="path to the program to submit",
    )
    parser.add_argument(
        "dir",
        type=pathtype.Path(validator=validator_is_dir),
        help="path to the directory containing the test cases",
    )
    parser.add_argument(
        "time",
        nargs="?",
        type=int,
        default=1000,
        help="maximum amount of time (in milliseconds) to run the program",
    )
    parser.add_argument(
        "mem",
        nargs="?",
        type=int,
        default=32,
        help="maximum amount of memory (in megabytes) to allocate to the program",
    )
    parser.add_argument(
        "-e",
        "--executable",
        action="store_true",
        help="notifies the grader that the file is executable",
    )
    args = parser.parse_args()

    grade(args.file, args.dir, args.time, args.mem, args.executable)


def validator_is_dir(path: Path, _arg: str):
    """Validator function for ensuring that a path is a directory."""

    if not path.is_dir() or not path.exists():
        raise argparse.ArgumentTypeError(f"directory doesn't exist ({path})")


def grade(file, dir, time=1000, mem=32, exec=False):
    """Grades a C++ program using PyGrader."""

    if exec:
        grader = Grader(exec_file=file, time_limit=time, memory_limit=mem)
    else:
        grader = Grader(source_file=file, time_limit=time, memory_limit=mem)

    accepted = 0
    console = Console()

    try:
        results = grader.grade(dir)
    except GraderError:
        console.print(StatusMessage.CE.value)
        return

    with console.status(f"[bold]running {file.stem}...") as _status:
        for result in results:
            sleep(0.3)
            message = (
                f"test case {result.name}:\t{StatusMessage[result.status.name].value}\t"
                + f"[{result.time:.3f} s,{result.mem:.2f} MB]"
            )
            console.print(message)
            if result.status == Status.AC:
                accepted += 1

        points = accepted * 100 / len(results) if results else 0.0
        console.print(
            f"[bold]final score: {accepted}/{len(results)} ({points:.1f} points)"
        )
