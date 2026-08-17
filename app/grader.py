"""
Runs learner-submitted Python code against a topic's test cases.

Safety approach (this is a personal training tool, not a public multi-tenant
sandbox, but we still don't want a stray `import os; os.system(...)` to touch
the host):
  - Executed in a separate `multiprocessing.Process`, not in the API process.
  - A hard wall-clock timeout kills the process if code hangs (infinite loops).
  - `__builtins__` is replaced with a small allow-list - no `open`, `eval`,
    `exec`, `__import__`, `input`, or file/network access.
  - stdout is captured and returned so learners can use print() to debug.
"""

import builtins
import multiprocessing as mp
import traceback
from dataclasses import dataclass
from io import StringIO
from typing import List, Dict, Any
import contextlib

TIMEOUT_SECONDS = 5

_ALLOWED_BUILTIN_NAMES = [
    "__build_class__",  # required by Python internally to execute any `class` statement
    "abs", "all", "any", "bool", "dict", "enumerate", "float", "format",
    "frozenset", "int", "isinstance", "issubclass", "len", "list", "map",
    "max", "min", "object", "print", "property", "range", "repr",
    "reversed", "round", "set", "sorted", "staticmethod", "classmethod",
    "str", "sum", "tuple", "type", "zip", "super", "getattr", "setattr",
    "hasattr", "Exception", "ValueError", "TypeError", "KeyError",
    "IndexError", "StopIteration", "ArithmeticError", "NotImplementedError",
    "RuntimeError", "AttributeError", "ZeroDivisionError", "True", "False",
    "None", "id", "iter", "next", "callable", "vars", "dir",
]

SAFE_BUILTINS = {name: getattr(builtins, name) for name in _ALLOWED_BUILTIN_NAMES if hasattr(builtins, name)}

# A handful of OOP-relevant stdlib modules are useful in challenges (abc,
# functools.total_ordering, dataclasses, enum, typing hints). Everything else
# (os, sys, subprocess, socket, shutil, ...) stays blocked.
_ALLOWED_MODULES = {
    "abc", "functools", "dataclasses", "typing", "collections",
    "collections.abc", "math", "enum", "itertools", "datetime", "re",
    "copy", "operator",
}


def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name not in _ALLOWED_MODULES:
        raise ImportError(f"module '{name}' is not available in this sandbox")
    return builtins.__import__(name, globals, locals, fromlist, level)


SAFE_BUILTINS["__import__"] = _safe_import


@dataclass
class TestCase:
    name: str
    code: str  # a python snippet, e.g. "assert Car('Toyota').make == 'Toyota'"


def _worker(code: str, tests: List[Dict[str, str]], conn):
    results = []
    stdout_buf = StringIO()
    namespace = {"__builtins__": SAFE_BUILTINS, "__name__": "__sandbox__"}
    try:
        with contextlib.redirect_stdout(stdout_buf):
            exec(code, namespace)
            for t in tests:
                try:
                    exec(t["code"], namespace)
                    results.append({"name": t["name"], "passed": True, "message": "Passed"})
                except AssertionError as e:
                    msg = str(e) or "Assertion failed"
                    results.append({"name": t["name"], "passed": False, "message": msg})
                except Exception as e:
                    results.append({"name": t["name"], "passed": False, "message": f"{type(e).__name__}: {e}"})
        conn.send({"ok": True, "results": results, "stdout": stdout_buf.getvalue(), "error": None})
    except Exception:
        conn.send({
            "ok": False,
            "results": results,
            "stdout": stdout_buf.getvalue(),
            "error": traceback.format_exc(limit=3),
        })
    finally:
        conn.close()


def run_challenge(code: str, tests: List[Dict[str, str]]) -> Dict[str, Any]:
    parent_conn, child_conn = mp.Pipe()
    proc = mp.Process(target=_worker, args=(code, tests, child_conn), daemon=True)
    proc.start()
    proc.join(TIMEOUT_SECONDS)

    if proc.is_alive():
        proc.terminate()
        proc.join()
        return {
            "passed": False,
            "tests": [{"name": t["name"], "passed": False, "message": "Not run (timeout)"} for t in tests],
            "stdout": "",
            "error": f"Your code took longer than {TIMEOUT_SECONDS}s to run - check for infinite loops.",
        }

    if parent_conn.poll():
        payload = parent_conn.recv()
    else:
        payload = {"ok": False, "results": [], "stdout": "", "error": "Process crashed unexpectedly."}

    test_results = payload["results"]
    all_passed = bool(test_results) and all(r["passed"] for r in test_results) and payload["ok"]

    return {
        "passed": all_passed,
        "tests": test_results,
        "stdout": payload["stdout"],
        "error": payload["error"],
    }
