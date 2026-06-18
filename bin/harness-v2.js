#!/usr/bin/env node
"use strict";

const { spawnSync } = require("node:child_process");
const path = require("node:path");

const packageRoot = path.resolve(__dirname, "..");
const userArgs = process.argv.slice(2);

function pythonCandidates() {
  if (process.platform === "win32") {
    return [
      { command: "py", args: ["-3"] },
      { command: "python", args: [] },
      { command: "python3", args: [] }
    ];
  }

  return [
    { command: "python3", args: [] },
    { command: "python", args: [] }
  ];
}

function pythonEnvironment() {
  const env = { ...process.env, PYTHONDONTWRITEBYTECODE: "1" };
  env.PYTHONPATH = env.PYTHONPATH
    ? `${packageRoot}${path.delimiter}${env.PYTHONPATH}`
    : packageRoot;
  return env;
}

function findPython() {
  for (const candidate of pythonCandidates()) {
    const probe = spawnSync(candidate.command, [...candidate.args, "--version"], {
      stdio: "ignore",
      windowsHide: true
    });
    if (!probe.error && probe.status === 0) {
      return candidate;
    }
  }
  return null;
}

const python = findPython();
if (!python) {
  console.error(
    "HARNESS V2 requires Python 3.11 or newer. Install Python 3.11+ and ensure py -3, python3, or python is on PATH."
  );
  process.exit(1);
}

const result = spawnSync(
  python.command,
  [...python.args, "-m", "harness_v2", ...userArgs],
  {
    cwd: process.cwd(),
    env: pythonEnvironment(),
    stdio: "inherit",
    windowsHide: true
  }
);

if (result.error) {
  console.error(`HARNESS V2 failed to start Python: ${result.error.message}`);
  process.exit(1);
}

if (result.signal) {
  console.error(`HARNESS V2 Python process terminated by signal ${result.signal}`);
  process.exit(1);
}

process.exit(result.status === null ? 1 : result.status);
