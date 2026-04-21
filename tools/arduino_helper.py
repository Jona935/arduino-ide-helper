#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


SUPPORTED_SOURCE_SUFFIXES = {".ino", ".pde", ".h", ".hpp", ".c", ".cpp"}

BOARD_ALIASES = {
    "arduino uno": "arduino:avr:uno",
    "uno": "arduino:avr:uno",
    "arduino nano": "arduino:avr:nano",
    "nano": "arduino:avr:nano",
    "arduino mega 2560": "arduino:avr:mega",
    "mega 2560": "arduino:avr:mega",
    "mega": "arduino:avr:mega",
    "arduino leonardo": "arduino:avr:leonardo",
    "leonardo": "arduino:avr:leonardo",
    "esp32": "esp32:esp32:esp32",
    "esp32 dev module": "esp32:esp32:esp32",
    "esp8266": "esp8266:esp8266:nodemcuv2",
    "nodemcu": "esp8266:esp8266:nodemcuv2",
    "raspberry pi pico": "rp2040:rp2040:rpipico",
    "pico": "rp2040:rp2040:rpipico",
}

INCLUDE_LIBRARY_HINTS = {
    "arduinojson.h": "ArduinoJson",
    "wifi.h": "WiFi",
    "espasyncwebserver.h": "ESP Async WebServer",
    "asyncTCP.h": "AsyncTCP",
    "asynctcp.h": "AsyncTCP",
    "adafruit_sensor.h": "Adafruit Unified Sensor",
    "dht.h": "DHT sensor library",
    "pubsubclient.h": "PubSubClient",
    "liquidcrystal_i2c.h": "LiquidCrystal I2C",
    "u8g2lib.h": "U8g2",
    "adafruit_gfx.h": "Adafruit GFX Library",
    "adafruit_ssd1306.h": "Adafruit SSD1306",
    "fastled.h": "FastLED",
    "onewire.h": "OneWire",
    "dallastemperature.h": "DallasTemperature",
    "servo.h": "Servo",
    "accelstepper.h": "AccelStepper",
    "tle5012b.h": "TLE5012B",
}


def common_cli_candidates() -> list[Path]:
    home = Path.home()
    candidates = [
        Path(os.environ.get("ARDUINO_CLI_PATH", "")),
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


def run_cli(args: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    cli = resolve_arduino_cli()
    process = subprocess.run(
        [cli, *args],
        check=False,
        capture_output=capture,
        text=True,
    )
    if process.returncode != 0:
        if capture and process.stderr:
            print(process.stderr.strip(), file=sys.stderr)
        raise SystemExit(process.returncode)
    return process


def update_indexes() -> None:
    run_cli(["core", "update-index"])
    run_cli(["lib", "update-index"])


def normalize_lookup_key(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def resolve_fqbn_name(board_name: str) -> str:
    board_name = board_name.strip()
    if board_name.count(":") >= 2:
        return board_name

    key = normalize_lookup_key(board_name)
    alias = BOARD_ALIASES.get(key)
    if alias:
        return alias

    raise SystemExit(
        f"No pude mapear '{board_name}' a un FQBN conocido. "
        "Prueba algo como arduino:avr:uno o usa detect-board."
    )


def gather_source_files(project_path: Path) -> list[Path]:
    files: list[Path] = []
    for file_path in project_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_SOURCE_SUFFIXES:
            files.append(file_path)
    return sorted(files)


def extract_includes(project_path: Path) -> list[str]:
    pattern = re.compile(r'^\s*#include\s*[<"]([^">]+)[">]')
    found: set[str] = set()

    for file_path in gather_source_files(project_path):
        try:
            contents = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line in contents:
            match = pattern.match(line)
            if match:
                found.add(match.group(1))

    return sorted(found)


def infer_library_candidates(includes: list[str]) -> list[str]:
    libraries: set[str] = set()
    for include_name in includes:
        include_key = include_name.lower()
        hint = INCLUDE_LIBRARY_HINTS.get(include_key)
        if hint:
            libraries.add(hint)
            continue

        stem = Path(include_name).stem
        if stem:
            libraries.add(stem)

    return sorted(libraries)


def ensure_project_path(project_path_arg: str) -> Path:
    project_path = Path(project_path_arg).expanduser().resolve()
    if not project_path.exists() or not project_path.is_dir():
        raise SystemExit(f"La ruta no existe o no es una carpeta: {project_path}")
    return project_path


def find_sketches(project_path: Path) -> list[Path]:
    return sorted(project_path.glob("*.ino"))


def command_install_library(args: argparse.Namespace) -> None:
    run_cli(["lib", "update-index"])
    cli_args = ["lib", "install", args.library_name]
    if args.version:
        cli_args.extend(["--version", args.version])
    run_cli(cli_args)


def command_install_platform(args: argparse.Namespace) -> None:
    run_cli(["core", "update-index"])
    run_cli(["core", "install", args.platform])


def command_list_libraries(args: argparse.Namespace) -> None:
    cli_args = ["lib", "list"]
    if args.all:
        cli_args.append("--all")
    run_cli(cli_args)


def command_list_platforms(args: argparse.Namespace) -> None:
    cli_args = ["core", "list"]
    if args.all:
        cli_args.append("--all")
    run_cli(cli_args)


def command_list_boards(args: argparse.Namespace) -> None:
    cli_args = ["board", "list"]
    if args.watch:
        cli_args.append("--watch")
    run_cli(cli_args)


def command_detect_board(args: argparse.Namespace) -> None:
    board_name = args.board_name.strip()
    if board_name:
        try:
            fqbn = resolve_fqbn_name(board_name)
            print(f"{board_name} -> {fqbn}")
            return
        except SystemExit:
            print(f"No encontre alias local para '{board_name}'. Buscando en arduino-cli...")
            run_cli(["board", "listall", board_name])
            return

    print("Alias conocidos:")
    for alias, fqbn in sorted(BOARD_ALIASES.items()):
        print(f"- {alias} -> {fqbn}")


def print_project_summary(project_path: Path, includes: list[str], suggestions: list[str]) -> None:
    ino_files = find_sketches(project_path)
    print("Sketches encontrados:")
    for file_path in ino_files:
        print(f"- {file_path.name}")

    if includes:
        print("\nIncludes detectados:")
        for include in includes:
            print(f"- {include}")

    if suggestions:
        print("\nLibrerias sugeridas:")
        for library_name in suggestions:
            print(f"- {library_name}")


def command_check_project(args: argparse.Namespace) -> None:
    project_path = ensure_project_path(args.project_path)
    ino_files = find_sketches(project_path)
    if not ino_files:
        raise SystemExit(f"No encontre archivos .ino en {project_path}")

    includes = extract_includes(project_path)
    suggestions = infer_library_candidates(includes)
    print_project_summary(project_path, includes, suggestions)

    if args.fqbn:
        fqbn = resolve_fqbn_name(args.fqbn)
        print(f"\nCompilando proyecto con FQBN {fqbn}...")
        run_cli(["compile", "--fqbn", fqbn, str(project_path)])
        print("Revision completa: el proyecto compilo correctamente.")
    else:
        print("\nRevision estructural completa. No se compilo porque falta --fqbn.")


def command_fix_deps(args: argparse.Namespace) -> None:
    project_path = ensure_project_path(args.project_path)
    ino_files = find_sketches(project_path)
    if not ino_files:
        raise SystemExit(f"No encontre archivos .ino en {project_path}")

    includes = extract_includes(project_path)
    suggestions = infer_library_candidates(includes)
    print_project_summary(project_path, includes, suggestions)

    if not suggestions:
        print("\nNo detecte dependencias externas obvias para instalar.")
        return

    if args.install:
        print("\nActualizando indices de librerias...")
        run_cli(["lib", "update-index"])
        for library_name in suggestions:
            print(f"Instalando sugerencia: {library_name}")
            run_cli(["lib", "install", library_name])
        print("Dependencias sugeridas instaladas.")
    else:
        print("\nUsa --install para intentar instalar automaticamente las librerias sugeridas.")

    if args.fqbn:
        fqbn = resolve_fqbn_name(args.fqbn)
        print(f"\nCompilando proyecto con FQBN {fqbn}...")
        run_cli(["compile", "--fqbn", fqbn, str(project_path)])
        print("Proyecto compilado despues de revisar dependencias.")


def command_compile(args: argparse.Namespace) -> None:
    project_path = ensure_project_path(args.project_path)
    fqbn = resolve_fqbn_name(args.fqbn)
    cli_args = ["compile", "--fqbn", fqbn]
    if args.output_dir:
        cli_args.extend(["--output-dir", str(Path(args.output_dir).expanduser().resolve())])
    cli_args.append(str(project_path))
    run_cli(cli_args)


def command_upload(args: argparse.Namespace) -> None:
    project_path = ensure_project_path(args.project_path)
    fqbn = resolve_fqbn_name(args.fqbn)
    cli_args = ["upload", "-b", fqbn, "-p", args.port]
    if args.verify:
        cli_args.append("--verify")
    cli_args.append(str(project_path))
    run_cli(cli_args)


def command_monitor(args: argparse.Namespace) -> None:
    cli_args = ["monitor", "-p", args.port]
    if args.fqbn:
        cli_args.extend(["-b", resolve_fqbn_name(args.fqbn)])
    if args.config:
        cli_args.extend(["--config", args.config])
    if args.describe:
        cli_args.append("--describe")
    if args.timestamp:
        cli_args.append("--timestamp")
    run_cli(cli_args)


def command_doctor(args: argparse.Namespace) -> None:
    print(f"Python: {sys.version.split()[0]}")
    try:
        cli_path = resolve_arduino_cli()
        print(f"arduino-cli: {cli_path}")
    except SystemExit as exc:
        print(str(exc))
        return

    run_cli(["version"])


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

    list_libraries = subparsers.add_parser("list-libraries", help="Lista librerias instaladas")
    list_libraries.add_argument("--all", action="store_true", help="Incluye librerias integradas")
    list_libraries.set_defaults(func=command_list_libraries)

    list_platforms = subparsers.add_parser("list-platforms", help="Lista plataformas instaladas")
    list_platforms.add_argument("--all", action="store_true", help="Incluye plataformas instalables")
    list_platforms.set_defaults(func=command_list_platforms)

    list_boards = subparsers.add_parser("list-boards", help="Lista placas conectadas")
    list_boards.add_argument("--watch", action="store_true", help="Mantiene observacion de cambios")
    list_boards.set_defaults(func=command_list_boards)

    detect_board = subparsers.add_parser("detect-board", help="Mapea un alias o busca una placa por nombre")
    detect_board.add_argument("board_name", nargs="?", default="")
    detect_board.set_defaults(func=command_detect_board)

    check_project = subparsers.add_parser("check-project", help="Revisa o compila un proyecto Arduino")
    check_project.add_argument("project_path")
    check_project.add_argument("--fqbn")
    check_project.set_defaults(func=command_check_project)

    fix_deps = subparsers.add_parser("fix-deps", help="Sugiere o instala librerias faltantes basadas en includes")
    fix_deps.add_argument("project_path")
    fix_deps.add_argument("--fqbn")
    fix_deps.add_argument("--install", action="store_true")
    fix_deps.set_defaults(func=command_fix_deps)

    compile_command = subparsers.add_parser("compile", help="Compila un proyecto Arduino")
    compile_command.add_argument("project_path")
    compile_command.add_argument("--fqbn", required=True)
    compile_command.add_argument("--output-dir")
    compile_command.set_defaults(func=command_compile)

    upload_command = subparsers.add_parser("upload", help="Sube un sketch ya compilado o compilable al dispositivo")
    upload_command.add_argument("project_path")
    upload_command.add_argument("--fqbn", required=True)
    upload_command.add_argument("--port", required=True)
    upload_command.add_argument("--verify", action="store_true")
    upload_command.set_defaults(func=command_upload)

    monitor_command = subparsers.add_parser("monitor", help="Abre el monitor serial de arduino-cli")
    monitor_command.add_argument("--port", required=True)
    monitor_command.add_argument("--fqbn")
    monitor_command.add_argument("--config", help="Ejemplo: baudrate=115200")
    monitor_command.add_argument("--describe", action="store_true")
    monitor_command.add_argument("--timestamp", action="store_true")
    monitor_command.set_defaults(func=command_monitor)

    doctor_command = subparsers.add_parser("doctor", help="Verifica Python y arduino-cli")
    doctor_command.set_defaults(func=command_doctor)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
