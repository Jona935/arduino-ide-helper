#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def common_cli_candidates() -> list[Path]:
    home = Path.home()
    candidates = [
        Path(os.environ.get("ARDUINO_CLI_PATH", "")),
        Path("arduino-cli"),
        home / "AppData/Local/Programs/Arduino IDE/resources/app/lib/backend/resources/arduino-cli.exe",
        Path("C:/Program Files/Arduino IDE/resources/app/lib/backend/resources/arduino-cli.exe"),
        Path("C:/Program Files (x86)/Arduino IDE/resources/app/lib/backend/resources/arduino-cli.exe"),
        Path("/Applications/Arduino IDE.app/Contents/Resources/app/lib/backend/resources/arduino-cli"),
        home / "Applications/Arduino IDE.app/Contents/Resources/app/lib/backend/resources/arduino-cli",
        Path("/usr/local/bin/arduino-cli"),
        Path("/usr/bin/arduino-cli"),
    ]
    return [candidate for candidate in candidates if str(candidate)]


def resolve_arduino_cli() -> str:
    env_path = os.environ.get("ARDUINO_CLI_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    from_path = shutil.which("arduino-cli")
    if from_path:
        return from_path

    for candidate in common_cli_candidates():
        if candidate.exists():
            return str(candidate)

    raise SystemExit(
        "No encontre arduino-cli. Instala Arduino CLI o Arduino IDE 2.x, "
        "o define la variable ARDUINO_CLI_PATH."
    )


def run_cli(args: list[str]) -> None:
    cli = resolve_arduino_cli()
    process = subprocess.run([cli, *args], check=False)
    if process.returncode != 0:
        raise SystemExit(process.returncode)


def command_install_library(args: argparse.Namespace) -> None:
    run_cli(["lib", "update-index"])
    cli_args = ["lib", "install", args.library_name]
    if args.version:
        cli_args.extend(["--version", args.version])
    run_cli(cli_args)


def command_install_platform(args: argparse.Namespace) -> None:
    run_cli(["core", "update-index"])
    run_cli(["core", "install", args.platform])


def extract_includes(project_path: Path) -> list[str]:
    pattern = re.compile(r'^\s*#include\s*[<"]([^">]+)[">]')
    found: set[str] = set()

    for file_path in project_path.rglob("*"):
        if file_path.suffix.lower() not in {".ino", ".pde", ".h", ".hpp", ".c", ".cpp"}:
            continue
        if not file_path.is_file():
            continue
        try:
            contents = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line in contents:
            match = pattern.match(line)
            if match:
                found.add(match.group(1))

    return sorted(found)


def command_check_project(args: argparse.Namespace) -> None:
    project_path = Path(args.project_path).expanduser().resolve()
    if not project_path.exists() or not project_path.is_dir():
        raise SystemExit(f"La ruta no existe o no es una carpeta: {project_path}")

    ino_files = sorted(project_path.glob("*.ino"))
    if not ino_files:
        raise SystemExit(f"No encontre archivos .ino en {project_path}")

    print("Sketches encontrados:")
    for file_path in ino_files:
        print(f"- {file_path.name}")

    includes = extract_includes(project_path)
    if includes:
        print("\nIncludes detectados:")
        for include in includes:
            print(f"- {include}")

    if args.fqbn:
        print(f"\nCompilando proyecto con FQBN {args.fqbn}...")
        run_cli(["compile", "--fqbn", args.fqbn, str(project_path)])
        print("Revision completa: el proyecto compilo correctamente.")
    else:
        print("\nRevision estructural completa. No se compilo porque falta --fqbn.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Helper portable para agentes que trabajan con Arduino IDE y arduino-cli."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_library = subparsers.add_parser("install-library", help="Instala una libreria Arduino")
    install_library.add_argument("library_name")
    install_library.add_argument("--version")
    install_library.set_defaults(func=command_install_library)

    install_platform = subparsers.add_parser("install-platform", help="Instala una plataforma Arduino")
    install_platform.add_argument("platform")
    install_platform.set_defaults(func=command_install_platform)

    check_project = subparsers.add_parser("check-project", help="Revisa o compila un proyecto Arduino")
    check_project.add_argument("project_path")
    check_project.add_argument("--fqbn")
    check_project.set_defaults(func=command_check_project)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
