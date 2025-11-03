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
    "3.9",
    "3.10",
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


@nox.session(python="3.10")
def form(session: Session) -> None:
    """Format code with isort and black."""
    args = session.posargs or LOCATIONS
    session.run(poetry_path(), "install", "--no-dev", external=True)
    constrained_install(session, "isort", "black", external=True)
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


@nox.session(python="3.10")
def security(session: Session) -> None:
    """Check security safety."""
    session.run(
        poetry_path(),
        "export",
        "--dev",
        "--without-hashes",
        "--format=requirements.txt",
        "--output=requirements.txt",
        external=True,
    )
    session.install("--requirement=requirements.txt", "safety")
    session.run(
        "safety",
        "check",
        "--file=requirements.txt",
        "--full-report",
        "--ignore=44715",
        "--ignore=51457",  # https://github.com/pytest-dev/pytest/issues/10392
    )
    os.remove("requirements.txt")


@nox.session(python=VERSIONS, reuse_venv=False)
def tests(session: Session) -> None:
    """Run the test suite with pytest."""
    args = session.posargs or []
    session.run(poetry_path(), "install", "--no-dev", external=True)
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


@nox.session(python="3.10", reuse_venv=False)
def doc(session: Session) -> None:
    """Build the documentation."""
    session.run(poetry_path(), "install", "--no-dev", external=True)
    constrained_install(
        session,
        "sphinx",
        "sphinx-rtd-theme",
        "myst-parser",
        "pytest",
        "pytest-mock",
    )
    session.run("sphinx-build", "docs", "docs/_build")
