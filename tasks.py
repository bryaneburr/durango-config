"""Invoke tasks for the Durango project."""

from __future__ import annotations

import shlex
from collections.abc import Mapping, Sequence
from pathlib import Path

from invoke import Context, task

PROJECT_ROOT = Path(__file__).parent


def _run_uv(
    ctx: Context,
    args: Sequence[str],
    *,
    echo: bool = True,
    dry_run: bool = False,
    env: Mapping[str, str] | None = None,
) -> None:
    """Execute a uv command with consistent logging."""

    command = shlex.join(("uv", *args))
    if dry_run:
        print(f"[dry-run] {command}")
        return
    run_env = dict(ctx.config.run.env or {})
    if env:
        run_env.update(env)
    ctx.run(command, echo=echo, pty=True, env=run_env)


@task(help={"dev": "Install development extras defined in pyproject.toml."})
def sync(ctx: Context, dev: bool = True) -> None:
    """Synchronise the environment with uv."""

    args: list[str] = ["sync"]
    if dev:
        args.extend(["--extra", "dev", "--extra", "docs"])
    _run_uv(ctx, args)


@task(
    help={
        "fix": "Apply Ruff auto-fixes where possible.",
        "check_format": "Run `ruff format --check` before linting.",
    }
)
def lint(ctx: Context, fix: bool = False, check_format: bool = False) -> None:
    """Run Ruff formatting and lint checks via uv."""

    if check_format:
        _run_uv(ctx, ["run", "ruff", "format", "--check", "src", "tests"])
    args: list[str] = ["run", "ruff", "check", "src", "tests"]
    if fix:
        args.append("--fix")
    _run_uv(ctx, args)


@task(
    help={
        "markers": "Pytest -m expression to filter tests.",
        "k": "Pytest -k expression to filter tests.",
        "path": "Test path or dotted module (defaults to tests/).",
        "options": "Extra CLI arguments appended to pytest.",
    }
)
def tests(
    ctx: Context,
    markers: str = "",
    k: str = "",
    path: str = "tests",
    options: str = "",
) -> None:
    """Run the pytest suite with uv."""

    args: list[str] = ["run", "pytest"]
    if markers:
        args.extend(["-m", markers])
    if k:
        args.extend(["-k", k])
    if options:
        args.extend(shlex.split(options))
    if path:
        args.append(path)
    _run_uv(ctx, args)


@task
def mypy(ctx: Context) -> None:
    """Execute MyPy against the source tree."""

    _run_uv(ctx, ["run", "mypy", "src"])


@task(help={"all_files": "Run hooks across the entire repository."})
def precommit(ctx: Context, all_files: bool = False) -> None:
    """Run the configured pre-commit hooks using uv."""

    args: list[str] = ["run", "pre-commit", "run"]
    if all_files:
        args.append("--all-files")
    _run_uv(ctx, args)


@task(help={"strict": "Fail on warnings when building the docs."})
def docs_build(ctx: Context, strict: bool = True) -> None:
    """Build the MkDocs site with the shadcn theme."""

    args: list[str] = ["run", "mkdocs", "build"]
    if strict:
        args.append("--strict")
    _run_uv(ctx, args)


@task(help={"host": "Bind address", "port": "Bind port"})
def docs_serve(ctx: Context, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Serve the MkDocs documentation locally."""

    _run_uv(ctx, ["run", "mkdocs", "serve", "-a", f"{host}:{port}"])


@task
def ci(ctx: Context) -> None:
    """Run the same checks as CI."""

    lint(ctx, check_format=True)
    mypy(ctx)
    tests(ctx)
    docs_build(ctx)
