from vulture.core import __version__, Vulture

if not __version__:
    raise AssertionError
if not Vulture:
    raise AssertionError
