__all__ = ["taco_cli"]

import subprocess
from pathlib import Path

from returns.result import Failure, Result, Success

taco_binary = Path(__file__).parent.joinpath("taco/bin/taco")


def taco_cli(arguments: list[str]) -> Result[str, str]:
    """Invoke the taco binary.

    The `taco` binary packaged with this distribution is invoked in a subprocess.

    Args:
        arguments: The CLI arguments to pass to the taco binary.

    Returns:
        A `Success` containing the standard output of the taco binary if the
        return code is 0, or a `Failure` containing the standard error if the
        return code is non-zero.
    """
    # Call taco to write the kernels to standard out
    result = subprocess.run([taco_binary, *arguments], capture_output=True, text=True)

    if result.returncode != 0:
        return Failure(result.stderr)

    return Success(result.stdout)
