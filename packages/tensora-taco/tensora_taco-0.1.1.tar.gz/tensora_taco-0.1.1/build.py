import platform
import subprocess
from pathlib import Path

from cmake import CMAKE_BIN_DIR

project_dir = Path(__file__).parent.resolve()
taco_source_dir = project_dir.joinpath("src/taco")
taco_build_dir = project_dir.joinpath("build/taco/")
taco_install_dir = project_dir.joinpath("src/tensora_taco/taco/")

# Cannot invoke cmake from the path because Poetry does not put build dependencies on the path
# https://github.com/python-poetry/poetry/issues/8807
cmake_path = Path(CMAKE_BIN_DIR).joinpath("cmake")


def build(setup_kwargs):
    # Build taco
    os = platform.system()
    if os == "Linux":
        install_path = r"-DCMAKE_INSTALL_RPATH=\$ORIGIN/../lib"
    elif os == "Darwin":
        install_path = r"-DCMAKE_INSTALL_RPATH=@loader_path/../lib"
    else:
        raise NotImplementedError(f"Tensora cannot be installed on {os}")

    taco_build_dir.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            str(cmake_path),
            str(taco_source_dir),
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DCMAKE_INSTALL_PREFIX={taco_install_dir}",
            install_path,
        ],
        cwd=taco_build_dir,
    )
    subprocess.check_call(["make", "-j8"], cwd=taco_build_dir)
    subprocess.check_call(["make", "install"], cwd=taco_build_dir)

    # wheel include must be included here because Setuptools makes the wheel
    # sdist include must be in pyproject.toml because Poetry makes the sdist
    setup_kwargs["package_data"] = {"tensora_taco": ["taco/bin/taco", "taco/lib/libtaco*"]}
