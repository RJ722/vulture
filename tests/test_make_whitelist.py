import subprocess

from vulture.make_whitelist import make_whitelist

from . import v
assert v  # Silence pyflakes.


def check_whitelist(code, expected_output, v, tmpdir, capsys):
    sample = str(tmpdir.join("unused_code.py"))
    xml = str(tmpdir.join("coverage.xml"))
    with open(sample, 'w') as f:
        f.write(code)
    subprocess.call(["coverage", "run", sample])
    subprocess.call(["coverage", "xml", "-o", xml])
    v.scavenge([sample])
    capsys.readouterr()  # Flush output from coverage run 
    make_whitelist(v, xml)
    assert capsys.readouterr().out == expected_output.format(sample)


def test_create_whitelist(v, tmpdir, capsys):
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
    check_whitelist(code, expected_output, v, tmpdir, capsys)
