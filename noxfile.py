# -*- coding: utf-8 -*-
"""Nox session configuration."""

import os
from typing import Any, List

import nox
from nox.sessions import Session

PACKAGE: str = "lta"
LOCATIONS: List[str] = [
    PACKAGE,
    "noxfile.py",
    "tests",
]
VERSIONS: List[str] = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]

nox.options.stop_on_first_error = False
nox.options.reuse_existing_virtualenvs = True


def poetry_path() -> str:
    """Get the path to poetry."""
    return os.environ.get("POETRY_PATH", "poetry")


def constrained_install(
    session: Session, *args: str, **kwargs: Any  # noqa: ANN401
) -> None:
    """Install packages with poetry version constraint."""
    session.run(
        poetry_path(),
        "export",
        "--with",
        "dev",
        "--without-hashes",
        "--format=requirements.txt",
        "--output=requirements.txt",
        external=True,
    )
    session.install("--requirement=requirements.txt", *args, **kwargs)
    os.remove("requirements.txt")


@nox.session(python="3.13")
def form(session: Session) -> None:
    """Format code with isort and black."""
    args = session.posargs or LOCATIONS
    session.run(poetry_path(), "install", "--only", "main", external=True)
    constrained_install(session, "isort", "black")
    session.run("isort", *args)
    session.run("black", *args)


@nox.session(python=VERSIONS)
def lint(session: Session) -> None:
    """Lint files with flake8."""
    args = session.posargs or LOCATIONS
    constrained_install(
        session,
        "flake8",
        "pyproject-flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-bugbear",
        "flake8-comprehensions",
        "flake8-docstrings",
        "flake8-pytest-style",
        "flake8-spellcheck",
        "darglint",
    )
    if session.python == "3.14":
        # flake8-bandit/bandit use ast.Constant.s removed in Python 3.14; remove to prevent crash
        session.run("pip", "uninstall", "-y", "flake8-bandit", "bandit")
        session.run("pflake8", "--extend-ignore=S", *args)
    else:
        session.run("pflake8", *args)


@nox.session(python=VERSIONS)
def type(session: Session) -> None:
    """Type check files with mypy."""
    args = session.posargs or LOCATIONS
    constrained_install(
        session,
        "mypy",
    )
    session.run("mypy", "--ignore-missing-imports", *args)


@nox.session(python="3.13")
def security(session: Session) -> None:
    """Check security safety."""
    session.run(
        poetry_path(),
        "export",
        "--with",
        "dev",
        "--without-hashes",
        "--format=requirements.txt",
        "--output=requirements.txt",
        external=True,
    )
    session.install("pip-audit")
    session.run("pip-audit", "-r", "requirements.txt", "--skip-editable")
    os.remove("requirements.txt")


@nox.session(python=VERSIONS, reuse_venv=False)
def tests(session: Session) -> None:
    """Run the test suite with pytest."""
    args = session.posargs or []
    session.run(poetry_path(), "install", "--only", "main", external=True)
    constrained_install(  # These are required for tests. Don't clutter w/ all dependencies!
        session,
        "coverage",
        "tomli",
        "pytest",
        "pytest-clarity",
        "pytest-sugar",
        "pytest-mock",
        "pytest-cov",
        "pytest-xdist",
        "xdoctest",
    )
    session.run("pytest", *args)


@nox.session(python="3.13", reuse_venv=False)
def doc(session: Session) -> None:
    """Build the documentation."""
    session.run(poetry_path(), "install", "--only", "main", external=True)
    constrained_install(
        session,
        "sphinx",
        "sphinx-rtd-theme",
        "myst-parser",
        "pytest",
        "pytest-mock",
    )
    session.run("sphinx-build", "docs", "docs/_build")
