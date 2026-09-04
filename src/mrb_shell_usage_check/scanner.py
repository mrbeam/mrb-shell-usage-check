import ast
from pathlib import Path

DISALLOWED_CALLEES = {
    ("subprocess", "run"),
    ("subprocess", "call"),
    ("subprocess", "check_call"),
    ("subprocess", "check_output"),
    ("subprocess", "Popen"),
    ("os", "system"),
    ("os", "popen"),
}
OS_SHELL_CALLEES = {
    ("os", "system"),
    ("os", "popen"),
}
SUBPROCESS_CALLEES = DISALLOWED_CALLEES - OS_SHELL_CALLEES
IGNORED_DIR_NAMES = {".git", ".venv", "venv", "node_modules", "build", "dist"}


def _callee_name(node):
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        return node.value.id, node.attr
    return None


def _is_shell_true(keyword):
    return (
        keyword.arg == "shell"
        and isinstance(keyword.value, ast.Constant)
        and keyword.value.value is True
    )


def _is_dynamic_command(arg):
    return isinstance(
        arg, (ast.JoinedStr, ast.BinOp, ast.Call, ast.Subscript, ast.Attribute)
    )


def _is_string_command(arg):
    return isinstance(arg, ast.Constant) and isinstance(arg.value, str)


def _iter_python_files(path):
    if path.is_file():
        if path.suffix == ".py":
            yield path
        return

    if not path.exists():
        return

    for candidate in sorted(path.rglob("*.py")):
        if any(part in IGNORED_DIR_NAMES for part in candidate.parts):
            continue
        yield candidate


def scan_file(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        callee = _callee_name(node.func)
        if callee not in DISALLOWED_CALLEES:
            continue

        if callee in OS_SHELL_CALLEES:
            findings.append((node.lineno, f"{callee[0]}.{callee[1]} is always shell-backed"))

        if any(_is_shell_true(keyword) for keyword in node.keywords):
            findings.append((node.lineno, "shell=True"))

        if node.args and callee in SUBPROCESS_CALLEES and _is_string_command(node.args[0]):
            findings.append((node.lineno, "string command instead of argv"))

        if node.args and _is_dynamic_command(node.args[0]):
            findings.append((node.lineno, "dynamic command construction"))
    return findings


def scan_paths(paths):
    files = []
    for path in paths:
        files.extend(_iter_python_files(path.resolve()))

    findings = []
    seen = set()
    for path in files:
        if path in seen:
            continue
        seen.add(path)
        for lineno, message in scan_file(path):
            findings.append(f"{path}:{lineno}: {message}")
    return findings
