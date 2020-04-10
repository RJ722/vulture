import ast
import glob
import os.path
import subprocess
import sys

import pytest

from vulture import core

DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(DIR)
WHITELISTS = glob.glob(os.path.join(REPO, "vulture", "whitelists", "*.py"))

skip_if_not_has_async = pytest.mark.skipif(
    not hasattr(ast, "AsyncFunctionDef"),
    reason="needs async support (added in Python 3.5)",
)


def call_vulture(args, **kwargs):
    return subprocess.call(
        [sys.executable, "-m", "vulture"] + args, cwd=REPO, **kwargs
    )


def check(items_or_names, expected_names):
    """items_or_names must be a collection of Items or a set of strings."""
    try:
        if sorted(item.name for item in items_or_names) != sorted(
            expected_names
        ):
            raise AssertionError
    except AttributeError:
        if items_or_names != set(expected_names):
            raise AssertionError


def check_unreachable(v, lineno, size, name):
    if len(v.unreachable_code) != 1:
        raise AssertionError
    item = v.unreachable_code[0]
    if item.first_lineno != lineno:
        raise AssertionError
    if item.size != size:
        raise AssertionError
    if item.name != name:
        raise AssertionError


@pytest.fixture
def v():
    return core.Vulture(verbose=True)
