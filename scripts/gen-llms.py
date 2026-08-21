#!/usr/bin/env python3
"""
gen-llms.py — Master Agent-First Publishing Architecture & Context Corpus Exporter for IEPE Protocol.

Generates versioned llms index and full codebase corpus files in the top-level `.agents/` directory:
  .agents/llms.txt
  .agents/llms-iepe-v<version>.txt
  .agents/llms-full.txt
  .agents/llms-full-iepe-v<version>.txt
"""

import os
import sys
import re
import json
import glob
import hashlib
import subprocess
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(ROOT_DIR, ".agents")
PYPROJECT_PATH = os.path.join(ROOT_DIR, "pyproject.toml")

def get_root_version():
    """Returns the IEPE protocol version from git tags or pyproject.toml."""
    # 1. Try git describe --tags
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=ROOT_DIR, stderr=subprocess.DEVNULL, text=True
        ).strip()
        if tag:
            return tag.lstrip("v")
    except Exception:
        pass

    # 2. Check pyproject.toml
    if os.path.exists(PYPROJECT_PATH):
        try:
            with open(PYPROJECT_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1).lstrip("v")
        except Exception:
            pass

    return "0.2.0"

def get_repo_identity():
    """Collects git commit SHA, tag, and dirty state for IEPE Core."""
    info = {}
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT_DIR, stderr=subprocess.DEVNULL, text=True
        ).strip()
        info["sha"] = sha
        
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=ROOT_DIR, stderr=subprocess.DEVNULL, text=True
        ).strip()
        if status:
            info["sha"] += " (dirty)"
    except Exception:
        info["sha"] = "unknown"
        
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--always"],
            cwd=ROOT_DIR, stderr=subprocess.DEVNULL, text=True
        ).strip()
        info["tag"] = tag
    except Exception:
        info["tag"] = "untagged"

    return f"IEPE Core Protocol: v{VERSION} ({info['sha']})"

VERSION = get_root_version()
ABBR = "iepe"
DATE = datetime.now().strftime("%Y-%m-%d")

EXCLUDED_DIRS = {
    "_scripts",
    "scratch",
    "node_modules",
    "target",
    "worktrees",
    ".worktrees",
    ".git",
    ".github",
    ".vscode",
    ".pytest_cache",
    ".cache",
    "dist",
    "build",
    "coverage",
    "tmp",
    "temp",
    "out",
    "__pycache__",
    "iepe_core.egg-info",
    ".egg-info",
}

EXCLUDED_FILE_SUBSTRINGS = {
    "-lock.json",
    ".lock",
    "pnpm-lock.yaml",
    "yarn.lock",
    ".DS_Store",
    ".map",
    ".min.js",
    ".min.css",
}

ALLOWED_EXTS = {
    ".py", ".json", ".md", ".toml", ".txt", ".sh", ".yaml", ".yml", ".sql"
}

def is_excluded_dir(dir_name):
    lower = dir_name.lower()
    if dir_name in EXCLUDED_DIRS or lower in EXCLUDED_DIRS or dir_name.endswith(".egg-info"):
        return True
    if dir_name.startswith(".") and dir_name != ".agents":
        return True
    if dir_name.startswith("__") or "__" in dir_name:
        return True
    if "worktree" in lower:
        return True
    return False

def read_file(file_path, rel_path):
    """Reads UTF-8 source byte-faithfully, rejects binary input, and raises on I/O errors."""
    try:
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
    except OSError as e:
        raise RuntimeError(f"Failed to read file {rel_path}: {e}")

    if b"\x00" in raw_bytes:
        print(f"[gen-llms] skipping binary file containing NUL bytes: {rel_path}")
        return None, raw_bytes

    try:
        return raw_bytes.decode("utf-8"), raw_bytes
    except UnicodeDecodeError:
        print(f"[gen-llms] skipping non-utf8 encoded file: {rel_path}")
        return None, raw_bytes

def is_excluded_file(file_name):
    lower = file_name.lower()
    if (
        file_name.endswith(".lock")
        or file_name.endswith("-lock.json")
        or file_name.endswith("-lock.yaml")
        or file_name.endswith("-lock.yml")
        or lower in {"cargo.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"}
    ):
        return True

    if file_name.startswith("._") or file_name.endswith(".pyc"):
        return True

    for sub in EXCLUDED_FILE_SUBSTRINGS:
        if sub in file_name:
            return True

    return False

def read_agents_dir_files():
    """Reads doctrine files from .agents/ surface (AGENTS.md and skills/*/SKILL.md)."""
    entries = []

    agents_md_path = os.path.join(AGENTS_DIR, "AGENTS.md")
    if os.path.exists(agents_md_path):
        rel_path = ".agents/AGENTS.md"
        content, _ = read_file(agents_md_path, rel_path)
        if content is not None:
            entries.append((rel_path, content))

    skills_dir = os.path.join(AGENTS_DIR, "skills")
    if os.path.exists(skills_dir):
        for root, dirs, files in os.walk(skills_dir):
            dirs[:] = [d for d in dirs if not is_excluded_dir(d)]
            for f in sorted(files):
                if f != "SKILL.md" or is_excluded_file(f):
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, ROOT_DIR)
                content, _ = read_file(full_path, rel_path)
                if content is not None:
                    entries.append((rel_path, content))

    return entries

def read_source_files():
    entries = read_agents_dir_files()
    agents_rel_paths = {rel for rel, _ in entries}

    for root, dirs, files in os.walk(ROOT_DIR):
        if root == ROOT_DIR:
            dirs[:] = [d for d in dirs if d != ".agents" and not is_excluded_dir(d)]
        else:
            dirs[:] = [d for d in dirs if not is_excluded_dir(d)]
            
        for f in files:
            ext = os.path.splitext(f)[1]
            if (ext in ALLOWED_EXTS or f in {"pyproject.toml", "LICENSE"}) and not is_excluded_file(f):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, ROOT_DIR)
                
                if rel_path in agents_rel_paths:
                    continue

                content, _ = read_file(full_path, rel_path)
                if content is not None:
                    entries.append((rel_path, content))
                    
    sorted_entries = sorted(entries, key=lambda x: x[0])
    return sorted_entries

def categorize_files(source_files):
    categories = {
        "Protocol Architecture, Doctrine & Governance": [],
        "Canonical Contract Schemas & Protocol Definitions": [],
        "Core Reference Implementation (iepe_core)": [],
        "Core Tools & Utilities": [],
        "Examples & Protocol Fixtures": [],
        "TestSuite & Verification Gates": [],
        "Operational Work Graph & Issues": [],
        "Verification & Execution Evidence": [],
        "Other Protocol Modules": []
    }
    for rel, src in source_files:
        line_count = len(src.splitlines())
        size_kib = round(len(src.encode('utf-8')) / 1024, 1)
        item = (rel, line_count, size_kib)

        if rel in {"AGENTS.md", "README.md", "ROADMAP.md", "LICENSE", "The-Project-Is-the-Benchmark.md", "pyproject.toml"} \
           or rel == ".agents/AGENTS.md" \
           or rel.startswith(".agents/skills/") \
           or rel.startswith("docs/"):
            categories["Protocol Architecture, Doctrine & Governance"].append(item)
        elif rel.startswith("schemas/"):
            categories["Canonical Contract Schemas & Protocol Definitions"].append(item)
        elif rel.startswith("iepe_core/"):
            categories["Core Reference Implementation (iepe_core)"].append(item)
        elif rel.startswith("tools/"):
            categories["Core Tools & Utilities"].append(item)
        elif rel.startswith("examples/") or rel.startswith("fixtures/"):
            categories["Examples & Protocol Fixtures"].append(item)
        elif rel.startswith("tests/"):
            categories["TestSuite & Verification Gates"].append(item)
        elif rel.startswith("work/"):
            categories["Operational Work Graph & Issues"].append(item)
        elif rel.startswith("evidence/"):
            categories["Verification & Execution Evidence"].append(item)
        else:
            categories["Other Protocol Modules"].append(item)
            
    return categories

def make_agent_rel_link(rel_path):
    if rel_path.startswith(".agents/"):
        return os.path.relpath(rel_path, ".agents")
    return "../" + rel_path

def main():
    os.makedirs(AGENTS_DIR, exist_ok=True)

    # Clean up stale/previous llms artifacts in .agents/
    for pattern in ["llms*.txt"]:
        for p in glob.glob(os.path.join(AGENTS_DIR, pattern)):
            try:
                os.remove(p)
            except Exception:
                pass

    ident_summary = get_repo_identity()
    source_files = read_source_files()
    categorized = categorize_files(source_files)

    total_lines = sum(len(src.splitlines()) for _, src in source_files)

    manifest_lines = [
        "# IEPE Protocol Master Index",
        f"> Protocol Root Version: v{VERSION} | Generated: {DATE} | Total Modules: {len(source_files)} files | Total Lines: {total_lines:,} lines",
        f"> Protocol Identity: {ident_summary}",
        "",
        "## Core Protocol Doctrine & Governance",
        f"- [AGENTS.md]({make_agent_rel_link('AGENTS.md')}): IEPE Master AI Agent Operating Contract",
        f"- [README.md]({make_agent_rel_link('README.md')}): IEPE Architecture Overview",
        f"- [ROADMAP.md]({make_agent_rel_link('ROADMAP.md')}): IEPE Development Roadmap",
        f"- [The-Project-Is-the-Benchmark.md]({make_agent_rel_link('The-Project-Is-the-Benchmark.md')}): Operational Doctrine",
        f"- [docs/PROTOCOL.md]({make_agent_rel_link('docs/PROTOCOL.md')}): IEPE Formal Specification",
        f"- [docs/INITIALIZATION.md]({make_agent_rel_link('docs/INITIALIZATION.md')}): Project Initialization Standard",
        f"- [docs/ADOPTION.md]({make_agent_rel_link('docs/ADOPTION.md')}): Adoption & Reconciliation Guide",
        "",
    ]

    for cat, items in categorized.items():
        if items:
            manifest_lines.append(f"## {cat} ({len(items)} files)")
            for rel, lcnt, size in items:
                link = make_agent_rel_link(rel)
                manifest_lines.append(f"- [{rel}]({link}) ({lcnt} lines, {size} KiB)")
            manifest_lines.append("")

    manifest_content = "\n".join(manifest_lines) + "\n"

    sep = "=" * 72
    def banner(title, info=""):
        extra = f" [{info}]" if info else ""
        return f"\n{sep}\n## {title}{extra}\n{sep}\n\n"

    full_parts = [
        f"# INTENT AND EVIDENCE PROJECT ENGINE (IEPE): CONSOLIDATED MASTER RESEARCH & CODEBASE CORPUS\n",
        f"Protocol Root Version: v{VERSION} ({DATE}) | Modules: {len(source_files)} | Total Lines: {total_lines:,}\n",
        f"Protocol Identity: {ident_summary}\n\n",
        f"TABLE OF CONTENTS & SUBSYSTEM SUMMARY:\n"
    ]

    for cat, items in categorized.items():
        if items:
            full_parts.append(f"  - {cat}: {len(items)} files\n")

    full_parts.append(f"\n{sep}\n\n")

    for cat, items in categorized.items():
        if items:
            full_parts.append(banner(f"SUBSYSTEM: {cat.upper()} ({len(items)} files)"))
            for rel, lcnt, size_kib in items:
                src = next(s for r, s in source_files if r == rel)
                full_parts.append(f"--- FILE: {rel} ({lcnt} lines, {size_kib} KiB) ---\n{src}\n\n")

    full_content = "".join(full_parts)
    
    corpus_sha256 = hashlib.sha256(full_content.encode("utf-8")).hexdigest()
    digest_header = f"> Corpus Payload SHA-256 (excluding this field): {corpus_sha256}\n"
    
    manifest_content = manifest_content.replace(f"> Protocol Identity: {ident_summary}\n", f"> Protocol Identity: {ident_summary}\n{digest_header}")
    full_content = full_content.replace(
        f"Protocol Identity: {ident_summary}\n\n",
        f"Protocol Identity: {ident_summary}\nCorpus Payload SHA-256 (excluding this field): {corpus_sha256}\n\n",
    )

    with open(os.path.join(AGENTS_DIR, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(manifest_content)
    with open(os.path.join(AGENTS_DIR, f"llms-{ABBR}-v{VERSION}.txt"), "w", encoding="utf-8") as f:
        f.write(manifest_content)

    with open(os.path.join(AGENTS_DIR, "llms-full.txt"), "w", encoding="utf-8") as f:
        f.write(full_content)
    with open(os.path.join(AGENTS_DIR, f"llms-full-{ABBR}-v{VERSION}.txt"), "w", encoding="utf-8") as f:
        f.write(full_content)

    full_kib = round(len(full_content.encode("utf-8")) / 1024)
    print(
        f"gen-llms: generated .agents/llms.txt, .agents/llms-{ABBR}-v{VERSION}.txt ({len(manifest_content)} bytes) and .agents/llms-full.txt, .agents/llms-full-{ABBR}-v{VERSION}.txt ({full_kib} KiB, {len(source_files)} source files included) [SHA256: {corpus_sha256[:16]}]"
    )

if __name__ == "__main__":
    main()
