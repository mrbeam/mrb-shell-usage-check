import argparse
import sys
from pathlib import Path

from .scanner import scan_paths


SUCCESS_MESSAGE = "Shell usage check passed."


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="mrb-shell-usage-check",
        description="Detect unsafe shell command construction in Python code.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="Regex for repo-relative Python paths to ignore. Repeatable.",
    )
    args = parser.parse_args(argv)

    findings = scan_paths(
        [Path(path) for path in args.paths],
        ignore_patterns=args.ignore,
    )
    if findings:
        print("Disallowed shell usage detected:")
        print("\n".join(findings))
        return 1

    print(SUCCESS_MESSAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
