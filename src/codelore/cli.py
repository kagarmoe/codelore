from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from codelore import __version__

app = typer.Typer(
    name="codelore",
    help="Construct and query evidence-backed project memory.",
    no_args_is_help=True,
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"codelore {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            help="Show the installed CodeLore version.",
        ),
    ] = False,
) -> None:
    return None


@app.command("build-window")
def build_window(
    repo: Annotated[
        Path,
        typer.Option(
            "--repo",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="Local repository to ingest.",
        ),
    ],
    start_ref: Annotated[str, typer.Option("--start-ref", help="Window start ref.")],
    end_ref: Annotated[str, typer.Option("--end-ref", help="Window end ref.")],
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Evidence-pack output path.",
        ),
    ] = Path("evidence-pack.json"),
) -> None:
    """Build a release-window evidence pack.

    Phase 1 only defines the command surface. Phase 2 will attach git-first
    ingestion and artifact normalization.
    """
    console.print(
        "[yellow]build-window is scaffolded; git ingestion is planned for Phase 2.[/]"
    )
    console.print(f"repo={repo}")
    console.print(f"start_ref={start_ref}")
    console.print(f"end_ref={end_ref}")
    console.print(f"output={output}")


@app.command("ask")
def ask(
    question: Annotated[str, typer.Argument(help="Bounded historical question.")],
    evidence_pack: Annotated[
        Path,
        typer.Option(
            "--evidence-pack",
            "-e",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            help="Evidence pack to query.",
        ),
    ],
) -> None:
    """Ask a question against an evidence pack."""
    console.print("[yellow]ask is scaffolded; retrieval is planned for Phase 5.[/]")
    console.print(f"evidence_pack={evidence_pack}")
    console.print(f"question={question}")


@app.command("export-evidence-pack")
def export_evidence_pack(
    evidence_pack: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            help="Evidence pack to export.",
        ),
    ],
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Export output path."),
    ] = Path("dossier.md"),
) -> None:
    """Export a human-readable dossier from an evidence pack."""
    console.print(
        "[yellow]export-evidence-pack is scaffolded; "
        "dossier export is planned for Phase 5.[/]"
    )
    console.print(f"evidence_pack={evidence_pack}")
    console.print(f"output={output}")
