import subprocess

import pytest
from vulture.make_whitelist import make_whitelist

from . import v
assert v  # Silence pyflakes.


@pytest.fixture
def check_whitelist(v, tmpdir, capsys):
    def check(code, expected_output):
        sample = str(tmpdir.join("unused_code.py"))
        xml = str(tmpdir.join("coverage.xml"))
        with open(sample, 'w') as f:
            f.write(code)
        subprocess.call(["coverage", "run", sample])
        subprocess.call(["coverage", "xml", "-o", xml])
        v.scavenge([sample])
        # with capsys.disabled():
        #    print("coverage.xml: ")
        #    with open(xml, 'r') as f:
        #        print(f.read())
        capsys.readouterr()  # Flush output from coverage run
        make_whitelist(v, xml)
        output = capsys.readouterr().out
        print(output)
        assert output == expected_output.format(sample)
    return check


def test_create_whitelist(check_whitelist):
    code = """\
class Greeter:
    def greet(self):
        print("Hi")
greeter = Greeter()
greet_func = getattr(greeter, "greet")
greet_func()
"""
    expected_output = """\
# {}
greet

"""
    check_whitelist(code, expected_output)
