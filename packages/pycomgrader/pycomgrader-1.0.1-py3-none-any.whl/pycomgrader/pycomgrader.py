"""
This module provides a grader for C++ programs.
"""

import subprocess
import time

import psutil

from enum import auto, Enum
from dataclasses import dataclass
from pathlib import Path


class GraderError(Exception):
    """
    An exception raised when there's an error while grading a submission.
    """

    pass


class Status(Enum):
    """
    An enumeration of possible statuses for a test case.
    """

    AC = auto()
    WA = auto()
    TLE = auto()
    MLE = auto()
    RTE = auto()


@dataclass
class TestCase:
    """
    A class representing a test case.

    Attributes:
        name: str
            The name of the test case.
        status: Status
            The status of the test case (either AC, WA, TLE, MLE, or RTE).
        time: float
            The time taken by the program to complete the test case.
        mem: float
            The maximum memory used by the program during the test case.
    """

    name: str
    status: Status
    time: float
    mem: float


class Grader:
    """
    A class that manages the grading process for a programming assignment.

    Attributes:
        time_limit (int): The maximum amount of time (in milliseconds) allowed for the grading process.
        memory_limit (int): The maximum amount of memory (in megabytes) allowed for the grading process.
        source_file (str or Path): The path to the source code file to be graded.
        exec_file (str or Path): The path to the executable file to be graded.

    Methods:
        grader(test_case_directory: str) -> List[TestCase]:
            Graders the test cases in the given directory and returns a list of TestCase objects.

        check_test_case(input_file: str, output_file: str) -> TestCase:
            Checks a single test case by running the program with the given input and output files and returns a TestCase object.

        _valid_file(file : str) -> Path:
            Returns a `Path` object if the file exists and is a regular file.

        _valid_dir(dir : str) -> Path:
            Returns a `Path` object if the directory exists and is a regular directory.

        _compile() -> None:
            Compiles the source code file and raises a GraderException if there are any compilation errors.

        _kill(pid: int) -> None:
            Kills the process with the given PID and all its children.

        _process_memory(pid: int) -> int:
            Returns the resident set size (RSS) of the process with the given PID.
    """

    def __init__(
        self,
        time_limit=1000,
        memory_limit=32,
        *,
        source_file: str | Path = None,
        exec_file: str | Path = None,
    ):
        """
        Initializes a Grader instance.

        Parameters:
            time_limit (int, optional): The maximum amount of time (in milliseconds) allowed for the grading process. Defaults to 1000.
            memory_limit (int, optional): The maximum amount of memory (in megabytes) allowed for the grading process. Defaults to 32.
            source_file (str or Path, optional): The path to the source code file to be graded. If not provided, an executable file must be provided.
            exec_file (str or Path, optional): The path to the executable file to be graded. If not provided, a source file must be provided.

        Raises:
            GraderError: If both a source file and an executable file are provided, or if neither a source file nor an executable file is provided.
        """
        if source_file and exec_file:
            raise GraderError(
                "expected either a source code file or an executable but not both"
            )
        if not source_file and not exec_file:
            raise GraderError("expected either a source code file or an executable")

        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.source_file = source_file
        self.exec_file = exec_file
        self._compiled

    @property
    def source_file(self):
        return self._source_file

    @source_file.setter
    def source_file(self, source_file):
        if source_file is None:
            self._source_file = None
            return
        path = self._valid_file(source_file)

        self._source_file = path
        self.exec_file = None
        self._compiled = False

    @property
    def exec_file(self):
        return self._exec_file

    @exec_file.setter
    def exec_file(self, exec_file):
        if exec_file is None:
            self._exec_file = None
            return
        path = self._valid_file(exec_file)

        self.source_file = None
        self._exec_file = path
        self._compiled = True

    def grade(self, test_cases_dir: str | Path):
        """
        Grades a set of test cases located in the specified directory.

        Parameters:
            test_cases_dir (str | Path): The directory containing the test cases.

        Returns:
            List[TestCase]: A list of `TestCase` objects, each representing a test case and containing information about its name, status, time, and memory usage.
        """
        test_cases_dir = self._valid_dir(test_cases_dir)
        in_list = sorted(test_cases_dir.glob("*.in"))
        out_list = sorted(test_cases_dir.glob("*.out"))
        results = []

        for input_file, output_file in zip(in_list, out_list):
            results.append(self.check_test_case(input_file, output_file))

        return results

    def check_test_case(self, input_file: str | Path, expected_output: str | Path):
        """
        Checks a test case against the expected output.

        Parameters:
            input_file (str | Path): The path to the input file for the test case.
            expected_output (str | Path): The path to the expected output file for the test case.

        Returns:
            TestCase: An object containing information about the test case, including its name, status, execution time, and memory usage.
        """
        if not self._compiled:
            self._compile()

        input_file = self._valid_file(input_file)
        expected_output = self._valid_file(expected_output)

        subm_output = self.exec_file.with_suffix(".out.tmp")

        with open(input_file) as in_file, open(subm_output, "w") as out_file:
            try:
                proc = subprocess.Popen(
                    [self.exec_file],
                    stdin=in_file,
                    stdout=out_file,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                raise GraderError(f"error while executing {self.exec_file}") from None
            start = time.perf_counter()
            end = time.perf_counter()
            max_mem = 0

            while proc.poll() is None:
                end = time.perf_counter()
                if end - start > self.time_limit / 1000:
                    self._kill(proc.pid)
                    return TestCase(
                        input_file.stem, Status.TLE, end - start, max_mem / 1024**2
                    )

                max_mem = max(max_mem, self._process_memory(proc.pid))
                if max_mem / 1024**2 > self.memory_limit:
                    self._kill(proc.pid)
                    return TestCase(
                        input_file.stem, Status.MLE, end - start, max_mem / 1024**2
                    )

        if proc.returncode:
            return TestCase(input_file.stem, Status.RTE, end - start, max_mem / 1024**2)

        if subm_output.read_text() == expected_output.read_text():
            return TestCase(input_file.stem, Status.AC, end - start, max_mem / 1024**2)
        else:
            return TestCase(input_file.stem, Status.WA, end - start, max_mem / 1024**2)

    def _valid_file(self, file):
        """
        Returns a `Path` object if the file exists and is a regular file.

        Parameters:
            file (str): File path or name

        Return:
            Path: A `Path` instance representing the valid file

        Raises:
            TypeError: If the file does not exist or is not a regular file.
        """
        path = Path(file)
        if path.exists() and path.is_file():
            return path

        raise TypeError(f"file doesn't exist ({file})")

    def _valid_dir(self, dir):
        """
        Returns a `Path` object if the directory exists and is a regular directory.

        Parameters:
            file (str): Directory path or name

        Return:
            Path: A `Path` instance representing the valid directory

        Raises:
            TypeError: If the directory does not exist or is not a regular directory.
        """
        path = Path(dir)
        if path.exists() and path.is_dir():
            return path

        raise TypeError(f"directory doesn't exist ({dir})")

    def _compile(self):
        """
        Compiles the submitted program.

        Raises:
            GraderCompileError: If there are any compilation errors.
        """
        try:
            subprocess.check_output(
                ["g++", self._source_file, "-o", self._source_file.with_suffix(".o")],
                stderr=subprocess.DEVNULL,
            )
            self._compiled = True
            self.exec_file = self._source_file.with_suffix(".o")
        except subprocess.CalledProcessError:
            raise GraderError("compile error") from None

    def _process_memory(self, proc_pid):
        """
        Gets the resident set size (RSS) of a process with the given PID.

        Parameters:
            proc_pid (int): The process ID of the process to get the memory usage for.

        Returns:
            int: The RSS of the process in bytes.
        """
        try:
            process = psutil.Process(proc_pid)
            mem_info = process.memory_info()
            return mem_info.rss
        except psutil.NoSuchProcess:
            return 0

    def _kill(self, proc_pid):
        """
        Kills a process and all its children.

        Parameters:
            proc_pid (int): The process ID of the process to kill.
        """
        try:
            process = psutil.Process(proc_pid)
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()
        except psutil.NoSuchProcess:
            pass
