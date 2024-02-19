"""
Utilities for getting metadata about your own package.
"""

import importlib.metadata
import inspect
from pathlib import Path


def _get_package_name(caller: inspect.FrameInfo) -> str:
    """
    Determine the name of the package of the given stack frame.
    """
    # Get the module name
    module_name = caller.frame.f_globals["__name__"]
    assert isinstance(module_name, str)

    # If the module is a package, return its name
    if module_name != "__main__":
        return module_name.split(".", maxsplit=1)[0]

    # If the module is not a package, try to find the package name from the
    # file path
    file_path = caller.filename
    assert isinstance(file_path, str)
    return Path(file_path).stem


def _get_root_directory(caller: inspect.FrameInfo) -> Path:
    """
    Return the root directory of the calling module, accounting for submodules.

    For example, if the calling module is `foo.bar.baz`, and `foo` is located
    at `/home/user/foo`, this function will return `/home/user/foo`.
    """
    caller_dir = Path(caller.filename).resolve().parent

    # How deep is this submodule?
    depth = caller.frame.f_globals["__name__"].count(".")

    for _ in range(depth):
        caller_dir = caller_dir.parent

    return caller_dir


def get_calling_package_name() -> str:
    """
    Determine the name of **the calling package**.
    """
    return _get_package_name(inspect.stack()[1])


def get_package_version() -> str:
    """
    Determine the version of **the calling package**.
    """
    # Who dis?
    caller_frame = inspect.stack()[1]
    caller = _get_package_name(caller_frame)

    # Try to just ask python
    try:
        return importlib.metadata.version(caller)
    except importlib.metadata.PackageNotFoundError:
        pass

    # While the approach above is clean, it fails during development. In that
    # case, read the version from the `pyproject.toml` file.
    import tomllib

    # TODO: What if the caller is foo.bar.baz, but the package is just foo?
    toml_path = _get_root_directory(caller_frame) / "pyproject.toml"

    try:
        with open(toml_path, "rb") as f:
            toml_contents = tomllib.load(f)

    except FileNotFoundError:
        raise RuntimeError(f"Cannot find `pyproject.toml` at `{toml_path}`") from None

    except tomllib.TOMLDecodeError as e:
        raise RuntimeError(f"`{toml_path}` is invalid TOML: {e}") from None

    try:
        return toml_contents["tool"]["poetry"]["version"]
    except KeyError:
        raise RuntimeError(
            f"`{toml_path}` does not contain a `tool.poetry.version` field"
        ) from None
