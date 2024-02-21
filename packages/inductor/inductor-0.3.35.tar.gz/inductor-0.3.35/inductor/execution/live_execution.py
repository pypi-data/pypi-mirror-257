# Copyright 2023 Inductor, Inc.
"""Functionality for live execution tasks."""

import contextlib
import contextvars
import datetime
import functools
import inspect
import traceback
from typing import Any, Callable, Dict, Iterator, List, Optional

from inductor import auth_session
from inductor.backend_client import backend_client, wire_model
from inductor.data_model import data_model
from inductor.execution import execution


# Stores a boolean flag indicating whether the current LLM program execution is
# the primary (top-level) execution. This flag allows nested functions that are
# decorated with the logger decorator to be collapsed into a single LLM program
# execution, without sending duplicate data to the backend.
_primary_execution = contextvars.ContextVar("active_execution", default=True)


@contextlib.contextmanager
def _manage_executions():
    """Manage the state of the primary execution context variable.

    Manage the state of the primary execution context variable
    (_primary_execution). If the variable is initially True, it is set to
    False and True is yielded. If the variable is initially False, False is
    yielded. On exit, the variable is restored to its original value.

    The purpose of this context manager is to allow the logger decorator to
    determine whether it is the primary (top-level) execution. This is
    necessary because the logger decorator should only send data to the
    backend if it is the primary execution. For example, when the logger
    decorator decorates a function that is called by another function also
    decorated with the logger decorator, the logger decorator should not send
    data to the backend during the inner function call.

    Yields:
        True if the primary execution context variable was True, False
        otherwise.
    """
    primary_execution = _primary_execution.get()
    if primary_execution:
        _primary_execution.set(False)
    try:
        yield primary_execution
    finally:
        _primary_execution.set(primary_execution)


def _complete_live_execution(
    *,
    primary_execution: bool,
    inputs: Optional[Dict[str, Any]] = None,
    output: Optional[Any] = None,
    error_str: Optional[str] = None,
    stdout: Optional[str] = None,
    stderr: Optional[str] = None,
    started_at: datetime.datetime,
    logged_values: List[wire_model.LoggedValue],
    program_details: wire_model.ProgramDetails,
    auth_access_token: str,
):
    """Complete a LLM program live execution.

    If the LLM program execution is the primary execution:
        - Send the execution data to the backend.
    Otherwise:
        - Call the Inductor client's `log()` function to log this execution as
            part of the current overarching primary execution.

    Args:
        primary_execution: Whether this is the primary execution.
        inputs: Input arguments to the LLM program.
        output: Output of the LLM program. If the output is an
            `execution.IteratorWrapper` the values yielded by the iterator
            will be used as the output.
        error_str: Error (in string form) raised by the LLM program, if any.
        stdout: Contents of stdout.
        stderr: Contents of stderr.
        started_at: Time at which the LLM program execution started.
        logged_values: Values logged by the LLM program.
        program_details: Details of the LLM program.
        auth_access_token: Auth0 access token to be used to authenticate
            requests to the backend.
    """
    ended_at = datetime.datetime.now(datetime.timezone.utc)

    if isinstance(output, execution.IteratorWrapper):
        # If the output is the result of an iterator, get the actual
        # output value and any error that occurred during the iteration.
        iterator_wrapper = output
        output = iterator_wrapper._get_completed_values()  # pylint: disable=protected-access
        assert error_str is None, (
            "An error occurred during the initial execution of the LLM "
            "program, but the output was an iterator. We do not expect an "
            "output from a function that raises an error.")
        error = iterator_wrapper._iteration_error  # pylint: disable=protected-access
        error_str = str(error) if error is not None else None

    if primary_execution:
        backend_client.log_llm_program_execution(
            wire_model.LogLlmProgramExecutionRequest(
                program_details=program_details,
                execution_details=wire_model.ExecutionDetails(
                    mode="DEPLOYED",
                    inputs=inputs if inputs else {},
                    output=output,
                    error=error_str,
                    stdout=stdout,
                    stderr=stderr,
                    execution_time_secs=(
                        ended_at - started_at).total_seconds(),
                    started_at=started_at,
                    ended_at=ended_at,
                    logged_values=logged_values or None)),
            auth_access_token)

    else:
        execution.log(
            {
                "llm_program": program_details.fully_qualified_name,
                "inputs": inputs if inputs else {},
                "output": output
            },
            name="Nested LLM program execution")


def logger(
    # NOTE: The function is optional to allow for the decorator to be used
    # with or without parentheses. This is important for when we add
    # additional arguments to the decorator.
    original_function: Optional[Callable] = None,
) -> Callable:
    """Log the inputs, outputs, and inductor.log calls of the given function.

    Use `logger` as a decorator to automatically log the arguments and return
    value of, as well as calls to inductor.log within, the decorated function.

    For example:
        @inductor.logger
        def hello_world(name: str) -> str:
            inductor.log(len(name), description="name length")
            return f"Hello {name}!"

    Args:
        original_function: Function to wrap. This argument should not
            be explicitly set when using @decorator syntax.

    Returns:
        Decorator.
    """
    try:
        auth_access_token = auth_session.get_auth_session().access_token
    except Exception as error:  # pylint: disable=broad-except
        traceback.print_exc()
        print(
            f"[ERROR] Exception occurred during setup of inductor.logger. "
            f"No data will be sent to Inductor through the logger decorator "
            f"for this session. {error}")
        def _blank_wrapper(func: Callable) -> Callable:
            return func
        return _blank_wrapper

    def _logger(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if execution.logger_decorator_enabled:
                func_result = None
                func_error = None
                func_completed = False

                try:
                    # Notes regarding the `with` clause immediately below:
                    # - We use backslashes to split the clause, rather than
                    # enclosing in parentheses, because enclosing in
                    # parentheses apparently causes a SyntaxError when running
                    # in Python 3.8.
                    # - We actually don't need to capture stdout and stderr if
                    # we are not in the primary execution. However, since
                    # stdout and stderr are not suppressed, the user will not
                    # be impacted, and we allow stdout and stdout to be
                    # captured nonetheless to simplify the code.
                    with execution.capture_logged_values() as logged_values, \
                        _manage_executions() as primary_execution, \
                        execution.capture_stdout_stderr(suppress=False) as (
                            stdout, stderr):

                        llm_program = data_model.LazyCallable(func)

                        # Get input arguments using the function's signature.
                        signature = inspect.signature(func)
                        bound_arguments = signature.bind(*args, **kwargs)
                        bound_arguments.apply_defaults()
                        processed_input_args = {}
                        for key, value in bound_arguments.arguments.items():
                            processed_input_args[key] = (
                                data_model.deepcopy_or_str(value))

                        started_at = datetime.datetime.now(
                            datetime.timezone.utc)

                        try:
                            func_result = func(*args, **kwargs)
                        except Exception as e:  # pylint: disable=broad-except
                            func_error = e
                        finally:
                            func_completed = True

                        execution_details = {
                            "primary_execution": primary_execution,
                            "inputs": processed_input_args,
                            "error_str": (
                                str(func_error)
                                if func_error is not None else None
                            ),
                            "stdout": stdout.getvalue(),
                            "stderr": stderr.getvalue(),
                            "started_at": started_at,
                            "logged_values": logged_values,
                            "program_details":
                                llm_program.get_program_details(),
                            "auth_access_token": auth_access_token,
                        }

                        if isinstance(func_result, Iterator):
                            # We cannot assume that the iterator can be
                            # re-used. Therefore we return a wrapper for the
                            # iterator that captures returned values and will
                            # complete the execution when the iterator is
                            # exhausted.
                            return execution.IteratorWrapper(
                                func_result,
                                stop_signal_handler=_complete_live_execution,
                                stop_signal_handler_kwargs=execution_details,
                                iterator_wrapper_error_message=(
                                    "[ERROR] Exception occurred during "
                                    "iteration of the LLM program result. No "
                                    "data will be sent to Inductor as part of "
                                    "this LLM program execution. "
                                ))

                        execution_details["output"] = (
                            data_model.deepcopy_or_str(func_result))
                        _complete_live_execution(**execution_details)

                        if func_error is not None:
                            raise func_error  # pylint: disable=raise-missing-from
                        return func_result

                except Exception as decorator_error:  # pylint: disable=broad-except
                    traceback.print_exc()
                    print(
                        f"[ERROR] Exception occurred in inductor.logger. No "
                        f"data will be sent to Inductor as part of this LLM "
                        f"program execution. {decorator_error}")
                    if func_completed:
                        # If the LLM program execution completed, there is no
                        # need to rerun the LLM program. Rerunning the LLM
                        # program could significantly hurt performance or could
                        # cause wider issues if the LLM program has side
                        # effects.
                        if func_error is not None:
                            raise func_error  # pylint: disable=raise-missing-from
                        return func_result
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper

    if original_function is not None:
        return _logger(original_function)

    return _logger
