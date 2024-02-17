__all__ = "timer", "statistics"

import statistics as st
import time as _time
from dataclasses import dataclass
from functools import wraps
from asyncio import gather as _gather
from inspect import iscoroutinefunction
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from collections import defaultdict

from prettytable import PrettyTable, MARKDOWN, SINGLE_BORDER, DOUBLE_BORDER
from termplotlib import figure
from memory_profiler import memory_usage
import numpy as np
from typing import Any


@dataclass(slots=True)
class RunResult:
    result: Any
    execution_time: float
    memory_usage: float


class timer:
    def __init__(self, f):
        self.f = f

    def __get__(self, instance, owner):
        if instance is None:
            return self.f
        return self._method_wrapper(instance)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            return False

    def __call__(self, *args, **kwargs):
        if iscoroutinefunction(self.f):
            return self._async_func_wrapper(*args, **kwargs)
        return self._sync_func_wrapper(*args, **kwargs)

    def _sync_func_wrapper(self, *args, **kwargs):
        start = _time.perf_counter()
        result = self.f(*args, **kwargs)
        end = _time.perf_counter()
        self.print_execution_time(end - start)
        return result

    async def _async_func_wrapper(self, *args, **kwargs):
        start = _time.perf_counter()
        result = await self.f(*args, **kwargs)
        end = _time.perf_counter()
        self.print_execution_time(end - start)
        return result

    def _method_wrapper(self, instance):
        @wraps(self.f)
        def wrapper(*args, **kwargs):
            if iscoroutinefunction(self.f):
                return self._async_method_wrapper(instance, *args, **kwargs)
            return self._sync_method_wrapper(instance, *args, **kwargs)
        return wrapper

    def _sync_method_wrapper(self, instance, *args, **kwargs):
        start = _time.perf_counter()
        result = self.f(instance, *args, **kwargs)
        end = _time.perf_counter()
        self.print_execution_time(end - start)
        return result

    async def _async_method_wrapper(self, instance, *args, **kwargs):
        start = _time.perf_counter()
        result = await self.f(instance, *args, **kwargs)
        end = _time.perf_counter()
        self.print_execution_time(end - start)
        return result

    def print_execution_time(self, execution_time):
        print(f"[{self.f.__name__}] Execution time: {execution_time:.5f}s")


def repeat(n=2):
    """
    Decorator that repeats the decorated function `n` times and returns the results as a tuple.

    Args:
        n (int): The number of times to repeat the function. Default is 2.

    Returns:
        tuple: The results of the repeated function calls.

    Example:
        @repeat(3)
        def multiply_by_two(x):
            return x * 2

        result = multiply_by_two(5)
        # Output: (10, 10, 10)
    """
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            results = tuple(func(*args, **kwargs) for _ in range(n))
            return results
        return wrapped
    return wrapper

class statistics:
    _statistics = defaultdict(list)
    _TABLE_FIELDS = (
        "mean",
        "median",
        "std",
        "min",
        "max"
    )

    def __init__(
        self,
        repeat=1,
        precision=6,
        threaded=False,
        process=False,
        cumulative=False,
        silent=False,
        memory=True,
        table=True,
        plot=True,
        extra_args=tuple(),
        extra_kwargs=dict()
    ):
        self.repeat = repeat
        self.precision = precision
        self.cumulative = cumulative
        self.threaded = threaded
        self.process = process
        self.silent = silent
        self.show_memory = memory
        self.show_table = table
        self.show_plot = plot
        self.extra_args = extra_args
        self.extra_kwargs = extra_kwargs

    def __call__(self, f):
        if iscoroutinefunction(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                args = (*args, *self.extra_args)
                kwargs = {**kwargs, **self.extra_kwargs}
                results = await self.run_async(f, *args, **kwargs)
                results, execution_times = zip(*results)

                if not self.silent:
                    if self.show_plot:
                        self._show_figure(f, execution_times)
                    if self.show_table:
                        self._show_table(f, execution_times)
                    if self.show_memory:
                        self._show_memory(f, *args, **kwargs)

                if self.cumulative:
                    return self._statistics[f]

                if len(results) == 1 or all(result == results[0] for result in results):
                    return results[0]
                return results
        else:
            @wraps(f)
            def wrapper(*args, **kwargs):
                args = (*args, *self.extra_args)
                kwargs = {**kwargs, **self.extra_kwargs}
                results = self.run(f, *args, **kwargs)
                results, execution_times, memory_usages = zip(*tuple((data.result, data.execution_time, data.memory_usage) for data in results))

                if not self.silent:
                    if self.show_plot:
                        self._show_figure(f, execution_times)
                    if self.show_table:
                        self._show_table(f, execution_times)
                    if self.show_memory:
                        self._show_memory(memory_usages)

                if self.cumulative:
                    return self._statistics[f]

                if len(results) == 1 or all(result == results[0] for result in results):
                    return results[0]
                return results
        return wrapper

#------------------------------------------------------------------------------------------------
# Execution

    def run(self, f, *args, **kwargs):
        if self.threaded:
            return self._run_threaded(f, *args, **kwargs)
        if self.process:
            return self._run_process(f, *args, **kwargs)
        else:
            return tuple(self._run(f, *args, **kwargs) for _ in range(self.repeat))

    def _execute(self, executor, f, *args, **kwargs):
        return tuple(future.result() for future in as_completed(
                (executor.submit(self._run, f, *args, **kwargs) for _ in range(self.repeat))
            )
        )

    def _run_threaded(self, f, *args, **kwargs):
        with ThreadPoolExecutor(30) as executor:
            return self._execute(executor, f, *args, **kwargs)

    # TODO: Fix this
    def _run_process(self, f, *args, **kwargs):
        with ProcessPoolExecutor() as executor:
            return self._execute(executor, f, *args, **kwargs)

    def _run(self, f, *args, **kwargs):
        start = _time.perf_counter()

        if self.show_memory:
            results = memory_usage((f, args, kwargs), retval=True, max_usage=True)
        else:
            results = (None, f(*args, **kwargs))

        end = _time.perf_counter()
        execution_time = end - start

        result = RunResult(results[1], execution_time, results[0])
        self._statistics[f].append(execution_time)
        return result

    async def run_async(self, f, *args, **kwargs):
        return await _gather(*(
            self._run_async(f, *args, **kwargs) for _ in range(self.repeat))
        )


    async def _run_async(self, f, *args, **kwargs):
        start = _time.perf_counter()
        results = await f(*args, **kwargs)
        end = _time.perf_counter()
        execution_time = end - start
        self._statistics[f].append(execution_time)
        return results, execution_time

#------------------------------------------------------------------------------------------------
# Plot

    def _get_bins(self, data):
        """
        Calculate the optimal number of bins using Sturges' formula.

        Args:
        data (array-like): Array of execution times

        Returns:
        int: Optimal number of bins
        """
        n = len(data)
        k = int(np.ceil(1 + np.log2(n)))  # Sturges' formula
        return k

    def _get_histogram(self, data, remove_outliers=True, rounding=True):
        if remove_outliers:
            lower = np.percentile(data, 5)
            upper = np.percentile(data, 95)
            #mean = st.mean(data)
            #std = st.pstdev(data)
            #threshold = mean + 3 * std
            data = [self.round(d) if rounding else d for d in data if lower <= d <= upper]

        counts, bin_edges = np.histogram(data)
        return counts, bin_edges

    def _get_figure(self, f, results):
        data = results if not self.cumulative else self._statistics[f]
        fig = figure()
        fig.hist(*self._get_histogram(data), orientation="horizontal", force_ascii=False)
        return fig

    def _show_figure(self, f, results):
        fig = self._get_figure(f, results)
        fig.show()

#------------------------------------------------------------------------------------------------
# Table

    def _format_table(self, f, results):
        data = results if not self.cumulative else self._statistics[f]
        table = PrettyTable()
        title = f"{f.__name__} ({len(data)})"
        if len(data) > 1:
            table.field_names = self._TABLE_FIELDS
            table.add_row(
                (
                    f"{st.mean(data):.{self.precision}f}",
                    f"{st.median(data):.{self.precision}f}",
                    f"{st.stdev(data):.{self.precision}f}",
                    f"{min(data):.{self.precision}f}",
                    f"{max(data):.{self.precision}f}"
                )
            )
        else:
            table.field_names = ("execution time",)
            table.add_row((f"{self._statistics[f][-1]: .5f}",))

        table.set_style(SINGLE_BORDER)
        maxline = len(max(table.get_string().split("\n")))
        table = table.get_string(title=title)
        message = "\n".join((
            "\n" + "-" * maxline,
            table,
        ))
        return message

    def _show_table(self, f, execution_time):
        table = self._format_table(f, execution_time)
        print(table)

#------------------------------------------------------------------------------------------------
# Memory


    def _show_memory(self, results):
        mem_usage = max(results)
        print(f"Memory usage: {mem_usage}MiB")

#--------------------------------------------------------------------------------
# Helpers

    def round(self, number):
        return round(number, self.precision)