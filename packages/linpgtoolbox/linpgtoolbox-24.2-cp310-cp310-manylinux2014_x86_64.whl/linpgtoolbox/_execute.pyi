from typing import Final

_PYTHON_PREFIX: Final[str]

def execute_python(*cmd: str, cwd: str | None = None) -> None: ...
