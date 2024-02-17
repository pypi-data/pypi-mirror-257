import importlib.resources
import subprocess
from pathlib import Path

from casefy import kebabcase, snakecase
from jinja2 import Template


def generate_provider_executable(
    dest_dir_path: Path,
    provider_name: str,
    provider_version: str,
    provider_python_package_name: str,
    provider_python_main_module: str,
    provider_env_var_name: str,
) -> None:
    template_source = (
        importlib.resources.files(__package__)
        / "provider-executable-template.sh.jinja2"
    ).read_text()
    t = Template(template_source)
    r = t.render(
        required_python_version=">=3.9",
        provider_fqname=f"{provider_name}-{provider_version}",
        provider_main_module=provider_python_main_module,
        provider_package_name=provider_python_package_name,
        provider_env_var_name=provider_env_var_name,
    )
    executable_name = f"terraform-provider-{provider_name}_v{provider_version}"
    executable_path = dest_dir_path / executable_name
    executable_path.write_text(r)
    executable_path.chmod(0o755)


def generate_provider_dir(
    dest_dir_path: Path,
    provider_name: str,
    provider_version: str,
    provider_python_package_name: str | None = None,
    provider_python_main_module: str | None = None,
    provider_env_var_prefix: str | None = None,
):
    if not all(c.isdigit() or c.isalnum() or c == "-" for c in provider_name):
        raise ValueError(
            f"invalid provider name {provider_name!r}; "
            "provider names may only contain letters, numbers and dashes"
        )
    if provider_python_package_name is None:
        provider_python_package_name = kebabcase(provider_name)
    if provider_python_main_module is None:
        provider_python_main_module = snakecase(provider_name)
    if provider_env_var_prefix is None:
        provider_env_var_prefix = snakecase(provider_name).upper()
    generate_provider_executable(
        dest_dir_path,
        provider_name,
        provider_version,
        provider_python_package_name,
        provider_python_main_module,
        provider_env_var_prefix,
    )
    subprocess.run(
        "python3 -m pip install --platform any --no-deps --only-binary :all: "
        "--implementation py packaging -t .",
        shell=True,
        cwd=dest_dir_path,
        check=True,
    )
