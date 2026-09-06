# Empty conftest.py at the project root so pytest adds this directory to
# sys.path, letting tests/test_app.py do `from app import app` regardless of
# which directory pytest is invoked from.
