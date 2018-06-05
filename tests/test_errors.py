import codecs
import os
import pytest
import tempfile

from . import v, REPO
assert v  # Silence pyflakes.


def test_syntax_error(v):
    v.scan("foo bar")
    assert int(v.report()) == 1


def test_null_byte(v):
    v.scan("\x00")
    assert int(v.report()) == 1


def test_confidence_range(v):
    v.scan("""\
def foo():
    pass
""")
    with pytest.raises(ValueError):
        v.get_unused_code(min_confidence=150)


def test_non_utf8_encoding(v):
    code = """\
def foo():
    pass

foo()
"""
    tests = os.path.join(REPO, 'tests')
    with tempfile.NamedTemporaryFile(mode='wb', dir=tests, suffix='.py') as f:
        f.write(codecs.BOM_UTF16_LE)
        f.write(code.encode('utf_16_le'))
        f.flush()  # Ensure that the file is actually written on disk.
        f.seek(0)  # Rewind the file object for Vulture.
        v.scavenge([f.name])
        assert v.found_dead_code_or_error
