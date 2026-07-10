from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer

from aprog.errors import ExitCode, fail

app = typer.Typer(
    name="aprog", help="Assignment programming orchestration CLI.", no_args_is_help=True
)
templates_app = typer.Typer(help="Template discovery commands.", no_args_is_help=True)
app.add_typer(templates_app, name="templates")

_Public = Annotated[
    Optional[Path], typer.Option("--public", help="Path to aprog-public root.")
]
_Private = Annotated[
    Optional[Path], typer.Option("--private", help="Path to aprog-private root.")
]


# -- new -----------------------------------------------------------------------


@app.command("new")
def new(
    slug: str,
    template: Annotated[str, typer.Option("--template", "-t", help="Template slug.")],
    difficulty: Annotated[Optional[str], typer.Option("--difficulty")] = None,
    topic: Annotated[Optional[list[str]], typer.Option("--topic")] = None,
    staging_dir: Annotated[Optional[Path], typer.Option("--staging-dir")] = None,
    force: Annotated[bool, typer.Option("--force")] = False,
    public: _Public = None,
) -> None:
    """Create a new assignment scaffold from a template."""
    from aprog.commands.new_cmd import cmd_new

    cmd_new(
        slug,
        template=template,
        difficulty=difficulty,
        topics=topic,
        staging_dir=staging_dir,
        force=force,
        public_root=public,
    )


# -- validate ------------------------------------------------------------------


@app.command("validate")
def validate(
    slug: Annotated[Optional[str], typer.Argument()] = None,
    all_: Annotated[bool, typer.Option("--all")] = False,
    private: _Private = None,
    public: _Public = None,
) -> None:
    """Validate assignment structure and metadata."""
    from aprog.commands.validate_cmd import cmd_validate, cmd_validate_all

    if all_:
        cmd_validate_all(private_repo=private, public_root=public)
    elif slug:
        code = cmd_validate(slug, private_repo=private, public_root=public)
        raise typer.Exit(code)
    else:
        fail("[red]Error:[/red] Provide a slug or --all", ExitCode.USAGE)


# -- scan-public ---------------------------------------------------------------


@app.command("scan-public")
def scan_public(
    slug: Annotated[Optional[str], typer.Argument()] = None,
    all_: Annotated[bool, typer.Option("--all")] = False,
    public: _Public = None,
) -> None:
    """Scan for private files accidentally in the public directory."""
    from aprog.commands.scan_cmd import cmd_scan_public

    cmd_scan_public(slug=slug, all_assignments=all_, public_root=public)


# -- check-generated -----------------------------------------------------------


@app.command("check-generated")
def check_generated(
    slug: Annotated[Optional[str], typer.Argument()] = None,
    all_: Annotated[bool, typer.Option("--all")] = False,
    private: _Private = None,
    public: _Public = None,
) -> None:
    """Check whether generated config files are current."""
    from aprog.commands.scan_cmd import cmd_check_generated

    cmd_check_generated(
        slug=slug, all_assignments=all_, private_repo=private, public_root=public
    )


# -- list / info ---------------------------------------------------------------


@app.command("list")
def list_assignments(
    language: Annotated[Optional[str], typer.Option("--language")] = None,
    difficulty: Annotated[Optional[str], typer.Option("--difficulty")] = None,
    topic: Annotated[Optional[list[str]], typer.Option("--topic")] = None,
    status: Annotated[Optional[str], typer.Option("--status")] = None,
    json_: Annotated[bool, typer.Option("--json")] = False,
    public: _Public = None,
) -> None:
    """List known assignments."""
    from aprog.commands.list_cmd import cmd_list

    cmd_list(
        language=language,
        difficulty=difficulty,
        topics=topic,
        status=status,
        as_json=json_,
        public_root=public,
    )


@app.command("info")
def info(
    slug: str,
    private: _Private = None,
    public: _Public = None,
) -> None:
    """Show detailed metadata for one assignment."""
    from aprog.commands.list_cmd import cmd_info

    cmd_info(slug, private_repo=private, public_root=public)


# -- templates -----------------------------------------------------------------


@templates_app.command("list")
def templates_list(
    language: Annotated[Optional[str], typer.Option("--language")] = None,
    public: _Public = None,
) -> None:
    """List available templates."""
    from aprog.commands.templates_cmd import cmd_templates_list

    cmd_templates_list(language=language, public_root=public)


@templates_app.command("info")
def templates_info(
    slug: str,
    public: _Public = None,
) -> None:
    """Show template details."""
    from aprog.commands.templates_cmd import cmd_templates_info

    cmd_templates_info(slug, public_root=public)


# -- generate-config -----------------------------------------------------------


@app.command("generate-config")
def generate_config(
    slug: Annotated[Optional[str], typer.Argument()] = None,
    all_: Annotated[bool, typer.Option("--all")] = False,
    private: _Private = None,
    force: Annotated[bool, typer.Option("--force")] = False,
    public: _Public = None,
) -> None:
    """Generate normalized config artifacts."""
    from aprog.commands.generate_config_cmd import (
        cmd_generate_config,
        cmd_generate_config_all,
    )

    if all_:
        cmd_generate_config_all(private_repo=private, force=force, public_root=public)
    elif slug:
        cmd_generate_config(slug, private_repo=private, force=force, public_root=public)
    else:
        fail("[red]Error:[/red] Provide a slug or --all", ExitCode.USAGE)


# -- package-public ------------------------------------------------------------


@app.command("package-public")
def package_public(
    slug: str,
    output_dir: Annotated[Optional[Path], typer.Option("--output-dir")] = None,
    public: _Public = None,
) -> None:
    """Create a public-safe assignment bundle."""
    from aprog.commands.package_cmd import cmd_package_public

    cmd_package_public(slug, output_dir=output_dir, public_root=public)


# -- package-private -----------------------------------------------------------


@app.command("package-private")
def package_private(
    slug: str,
    solution: Annotated[Optional[Path], typer.Option("--solution")] = None,
    hidden_tests: Annotated[Optional[Path], typer.Option("--hidden-tests")] = None,
    grader: Annotated[Optional[Path], typer.Option("--grader")] = None,
    output_dir: Annotated[Optional[Path], typer.Option("--output-dir")] = None,
    public: _Public = None,
) -> None:
    """Create a private solution/hidden-test bundle."""
    from aprog.commands.package_cmd import cmd_package_private

    cmd_package_private(
        slug,
        solution=solution,
        hidden_tests=hidden_tests,
        grader=grader,
        output_dir=output_dir,
        public_root=public,
    )


# -- submit --------------------------------------------------------------------


@app.command("submit")
def submit(
    slug: str,
    solution: Annotated[Optional[Path], typer.Option("--solution")] = None,
    hidden_tests: Annotated[Optional[Path], typer.Option("--hidden-tests")] = None,
    grader: Annotated[Optional[Path], typer.Option("--grader")] = None,
    encrypt: Annotated[bool, typer.Option("--encrypt")] = False,
    public: _Public = None,
) -> None:
    """Package and deliver the private bundle to the maintainer."""
    from aprog.commands.submit_cmd import cmd_submit

    cmd_submit(
        slug,
        solution=solution,
        hidden_tests=hidden_tests,
        grader=grader,
        encrypt=encrypt,
        public_root=public,
    )


# -- intake --------------------------------------------------------------------


@app.command("intake")
def intake(
    bundle: Path,
    public: _Public = None,
    private: _Private = None,
    force: Annotated[bool, typer.Option("--force")] = False,
    validate_: Annotated[bool, typer.Option("--validate")] = False,
    generate: Annotated[bool, typer.Option("--generate")] = False,
) -> None:
    """Import a private submission bundle (maintainer)."""
    from aprog.commands.intake_cmd import cmd_intake

    cmd_intake(
        bundle,
        public_repo=public,
        private_repo=private,
        force=force,
        validate=validate_,
        generate=generate,
    )


# -- verify --------------------------------------------------------------------


@app.command("verify")
def verify(
    slug: Annotated[Optional[str], typer.Argument()] = None,
    all_: Annotated[bool, typer.Option("--all")] = False,
    public: _Public = None,
    private: _Private = None,
) -> None:
    """Run maintainer verification against the reference solution."""
    from aprog.commands.verify_cmd import cmd_verify, cmd_verify_all

    if all_:
        cmd_verify_all(public_repo=public, private_repo=private)
    elif slug:
        cmd_verify(slug, public_repo=public, private_repo=private)
    else:
        fail("[red]Error:[/red] Provide a slug or --all", ExitCode.USAGE)


# -- package-gradescope --------------------------------------------------------


@app.command("package-gradescope")
def package_gradescope(
    slug: str,
    public: _Public = None,
    private: _Private = None,
    output_dir: Annotated[Optional[Path], typer.Option("--output-dir")] = None,
) -> None:
    """Create a Gradescope-ready zip (maintainer)."""
    from aprog.commands.verify_cmd import cmd_package_gradescope

    cmd_package_gradescope(
        slug, public_repo=public, private_repo=private, output_dir=output_dir
    )


if __name__ == "__main__":
    app()
