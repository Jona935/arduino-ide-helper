#!/usr/bin/env node

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const packageRoot = path.resolve(__dirname, "..");
const pluginName = "arduino-ide-helper";
const version = "0.4.0";

const ansi = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  green: "\x1b[32m",
  cyan: "\x1b[36m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  magenta: "\x1b[35m"
};

const mascot = String.raw`
        .-.
   ____ |+|   tiny board buddy
  | __ || |   pins up, signals clean
  ||__|||_|   ready to boot firmware
  |_____[_] 
`;

const banner = String.raw`
      _         _       _
     / \   _ __| | ___ (_)_ __   ___
    / _ \ | '__| |/ _ \| | '_ \ / _ \
   / ___ \| |  | | (_) | | | | | (_) |
  /_/   \_\_|  |_|\___/|_|_| |_|\___/
`;

function colorize(text, color) {
  if (!process.stdout.isTTY) {
    return text;
  }
  return `${ansi[color]}${text}${ansi.reset}`;
}

function sleepMs(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

function showIntro(mode = "default") {
  if (!process.stdout.isTTY) {
    console.log("Arduino IDE Helper");
    return;
  }

  console.log(colorize(banner, "cyan"));
  console.log(colorize(mascot, "green"));
  console.log(`${colorize("Arduino IDE Helper", "bold")} ${colorize(`v${version}`, "yellow")}`);
  console.log(colorize("firmware + sensores + templates + conocimiento", "blue"));
  console.log("");

  const frames = [
    colorize("[=         ] booting boards", "cyan"),
    colorize("[===       ] syncing sensors", "blue"),
    colorize("[=====     ] loading templates", "magenta"),
    colorize("[=======   ] routing project intent", "yellow"),
    colorize("[========= ] ready for firmware", "green")
  ];

  if (mode !== "animated") {
    console.log(frames[frames.length - 1]);
    console.log("");
    return;
  }

  for (const frame of frames) {
    process.stdout.write(`\r${frame}`);
    sleepMs(60);
  }
  process.stdout.write("\n\n");
}

function showSuccess(title, lines = []) {
  const header = process.stdout.isTTY ? colorize(`OK ${title}`, "green") : `OK ${title}`;
  console.log(header);
  for (const line of lines) {
    console.log(process.stdout.isTTY ? colorize(`  - ${line}`, "dim") : `  - ${line}`);
  }
  console.log("");
}

function printHelp() {
  showIntro("default");
  console.log(`arduino-ide-helper

Uso:
  arduino-ide-helper install codex
  arduino-ide-helper install claude --project <ruta>
  arduino-ide-helper install opencode --project <ruta>
  arduino-ide-helper install all --project <ruta>
  arduino-ide-helper doctor
  arduino-ide-helper help

Comandos:
  install codex         Instala el plugin en ~/plugins y actualiza ~/.agents/plugins/marketplace.json
  install claude        Copia CLAUDE.md al proyecto indicado
  install opencode      Copia OPENCODE.md al proyecto indicado
  install all           Ejecuta codex + claude + opencode
  doctor                Verifica Node, Python y arduino-cli
`);
}

function fail(message) {
  console.error(process.stdout.isTTY ? colorize(`Error: ${message}`, "yellow") : `Error: ${message}`);
  process.exit(1);
}

function parseArgs(argv) {
  const args = argv.slice(2);
  const flags = {};
  const positionals = [];

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--project") {
      flags.project = args[i + 1];
      i += 1;
    } else if (arg === "--force") {
      flags.force = true;
    } else if (arg === "--help" || arg === "-h") {
      flags.help = true;
    } else {
      positionals.push(arg);
    }
  }

  return { positionals, flags };
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function copyRecursive(source, destination) {
  const stat = fs.statSync(source);
  if (stat.isDirectory()) {
    ensureDir(destination);
    for (const entry of fs.readdirSync(source)) {
      copyRecursive(path.join(source, entry), path.join(destination, entry));
    }
    return;
  }
  ensureDir(path.dirname(destination));
  fs.copyFileSync(source, destination);
}

function writeFileIfAllowed(source, destination, force) {
  if (!force && fs.existsSync(destination)) {
    console.log(`Saltando ${destination} porque ya existe. Usa --force para sobrescribir.`);
    return false;
  }
  ensureDir(path.dirname(destination));
  fs.copyFileSync(source, destination);
  console.log(`Escribi ${destination}`);
  return true;
}

function readJson(filePath, fallback) {
  if (!fs.existsSync(filePath)) {
    return fallback;
  }
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeJson(filePath, payload) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function requireProject(flags) {
  const projectPath = flags.project ? path.resolve(flags.project) : process.cwd();
  if (!fs.existsSync(projectPath) || !fs.statSync(projectPath).isDirectory()) {
    fail(`La carpeta del proyecto no existe: ${projectPath}`);
  }
  return projectPath;
}

function installAll(flags) {
  showIntro("animated");
  const codexLines = installCodexBody();
  const claudeLines = installClaudeBody(flags);
  const opencodeLines = installOpenCodeBody(flags);
  showSuccess("Instalacion completa", [...codexLines, ...claudeLines, ...opencodeLines]);
}

function installCodexBody() {
  const home = os.homedir();
  const pluginSource = path.join(packageRoot, "plugins", pluginName);
  const pluginDestination = path.join(home, "plugins", pluginName);
  const marketplacePath = path.join(home, ".agents", "plugins", "marketplace.json");

  if (!fs.existsSync(pluginSource)) {
    fail(`No encontre el plugin base en ${pluginSource}`);
  }

  copyRecursive(pluginSource, pluginDestination);
  console.log(`Plugin copiado a ${pluginDestination}`);

  const marketplace = readJson(marketplacePath, {
    name: "local-plugins",
    interface: { displayName: "Local Plugins" },
    plugins: []
  });

  if (!Array.isArray(marketplace.plugins)) {
    marketplace.plugins = [];
  }

  const newEntry = {
    name: pluginName,
    source: {
      source: "local",
      path: `./plugins/${pluginName}`
    },
    policy: {
      installation: "AVAILABLE",
      authentication: "ON_INSTALL"
    },
    category: "Developer Tools"
  };

  const existingIndex = marketplace.plugins.findIndex((entry) => entry && entry.name === pluginName);
  if (existingIndex >= 0) {
    marketplace.plugins[existingIndex] = newEntry;
  } else {
    marketplace.plugins.push(newEntry);
  }

  writeJson(marketplacePath, marketplace);
  console.log(`Marketplace actualizado en ${marketplacePath}`);
  return [
    `plugin en ${pluginDestination}`,
    `marketplace en ${marketplacePath}`
  ];
}

function installClaudeBody(flags) {
  const projectPath = requireProject(flags);
  const written = writeFileIfAllowed(
    path.join(packageRoot, "CLAUDE.md"),
    path.join(projectPath, "CLAUDE.md"),
    flags.force
  );
  return [written ? `CLAUDE.md instalado en ${projectPath}` : `CLAUDE.md conservado en ${projectPath}`];
}

function installOpenCodeBody(flags) {
  const projectPath = requireProject(flags);
  const written = writeFileIfAllowed(
    path.join(packageRoot, "OPENCODE.md"),
    path.join(projectPath, "OPENCODE.md"),
    flags.force
  );
  return [written ? `OPENCODE.md instalado en ${projectPath}` : `OPENCODE.md conservado en ${projectPath}`];
}

function probe(command, args = ["--version"]) {
  const result = spawnSync(command, args, { encoding: "utf8", shell: false });
  if (result.status === 0) {
    return { ok: true, output: (result.stdout || result.stderr || "").trim() };
  }
  return { ok: false, output: (result.stderr || result.stdout || "").trim() };
}

function doctor() {
  showIntro("default");
  const nodeVersion = process.version;
  const lines = [`Node: ${nodeVersion}`];

  const python = probe("python", ["--version"]);
  const pyLauncher = python.ok ? null : probe("py", ["--version"]);
  const pythonMessage = python.ok
    ? python.output
    : pyLauncher && pyLauncher.ok
      ? pyLauncher.output
      : "no encontrado";
  lines.push(`Python: ${pythonMessage}`);

  const arduinoCliEnv = process.env.ARDUINO_CLI_PATH;
  if (arduinoCliEnv && fs.existsSync(arduinoCliEnv)) {
    lines.push(`arduino-cli: ${arduinoCliEnv}`);
    lines.forEach((line) => console.log(line));
    showSuccess("Doctor completo", lines);
    return;
  }

  const arduinoCli = probe("arduino-cli", ["version"]);
  if (arduinoCli.ok) {
    lines.push(`arduino-cli: ${arduinoCli.output}`);
    lines.forEach((line) => console.log(line));
    showSuccess("Doctor completo", lines);
    return;
  }

  const candidates = [
    path.join(os.homedir(), "AppData", "Local", "Programs", "Arduino IDE", "resources", "app", "lib", "backend", "resources", "arduino-cli.exe"),
    path.join("C:", "Program Files", "Arduino IDE", "resources", "app", "lib", "backend", "resources", "arduino-cli.exe"),
    path.join("C:", "Program Files (x86)", "Arduino IDE", "resources", "app", "lib", "backend", "resources", "arduino-cli.exe"),
    "/Applications/Arduino IDE.app/Contents/Resources/app/lib/backend/resources/arduino-cli",
    "/usr/local/bin/arduino-cli",
    "/usr/bin/arduino-cli"
  ];

  const detected = candidates.find((candidate) => fs.existsSync(candidate));
  lines.push(detected ? `arduino-cli: ${detected}` : "arduino-cli: no encontrado");
  lines.forEach((line) => console.log(line));
  showSuccess("Doctor completo", lines);
}

function main() {
  const { positionals, flags } = parseArgs(process.argv);
  const command = positionals[0];
  const target = positionals[1];

  if (flags.help || !command || command === "help") {
    printHelp();
    return;
  }

  if (command === "doctor") {
    doctor();
    return;
  }

  if (command !== "install") {
    fail(`Comando no soportado: ${command}`);
  }

  if (!target) {
    fail("Debes indicar que instalar: codex, claude, opencode o all.");
  }

  if (target === "codex") {
    showIntro("animated");
    showSuccess("Codex listo", installCodexBody());
    return;
  }
  if (target === "claude") {
    showIntro("animated");
    showSuccess("Claude Code listo", installClaudeBody(flags));
    return;
  }
  if (target === "opencode") {
    showIntro("animated");
    showSuccess("OpenCode listo", installOpenCodeBody(flags));
    return;
  }
  if (target === "all") {
    installAll(flags);
    return;
  }

  fail(`Objetivo no soportado: ${target}`);
}

main();
