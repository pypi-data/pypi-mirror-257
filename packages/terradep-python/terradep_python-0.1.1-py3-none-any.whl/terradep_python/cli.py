from dataclasses import dataclass
from pathlib import Path

import typer

from . import __distribution_name__, __version__
from .core import generate_provider_dir

cli_app = typer.Typer(
    context_settings={
        "auto_envvar_prefix": "TERRADEP_PYTHON_CLI",
    }
)


@dataclass
class TyperState:
    verbosity: int = 0


# Typer's idiom for implementing --version... don't even ask.
# https://typer.tiangolo.com/tutorial/options/version/
def version_callback(value: bool):
    if value:
        print(f"{__distribution_name__} {__version__}")
        raise typer.Exit()


@cli_app.callback(
    help="""
    Launcher/installer generation for Terraform providers written in Python.
    """
)
def typer_callback(
    ctx: typer.Context,
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Verbose output (repeat to increase verbosity, e.g. -vv, -vvv).",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        callback=version_callback,
        help="Print version information and exit.",
        is_eager=True,
    ),
):
    ctx.obj = TyperState(verbosity=verbose)


@cli_app.command(
    help="""
    Generate provider launcher/installer.

    Generates a launcher script meant to be used as the provider executable,
    plus its dependencies. These files can be packed into a Terraform provider
    archive to allow that provider to use a system's existing Python
    installation(s).
    """
)
def generate(
    dest_dir: str = typer.Argument(
        help="Directory in which to place the generated provider files."
    ),
    provider_name: str = typer.Option(
        help="Provider name (may only contain letters, numbers and hyphens)",
    ),
    provider_version: str = typer.Option(
        help="Provider version",
    ),
    provider_python_package_name: str = typer.Option(
        None,
        help="Name of the provider's (outer) Python package; "
        "must be present as a directory in the provider directory "
        "and will be installed with pip",
    ),
    provider_python_main_module: str = typer.Option(
        None,
        help="The provider's main (= runnable) module; "
        "will be called to start the actual Python provider",
    ),
    provider_env_var_prefix: str = typer.Option(
        None,
        help="Prefix for env vars that the end user may use to "
        "configure provider installation or behavior",
    ),
):
    generate_provider_dir(
        Path(dest_dir),
        provider_name,
        provider_version,
        provider_python_package_name,
        provider_python_main_module,
        provider_env_var_prefix,
    )


@cli_app.command()
def install():
    raise NotImplementedError("not yet implemented")


def main():
    cli_app()
