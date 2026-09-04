import argparse
import sys
from pathlib import Path

from .scanner import scan_paths


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
    args = parser.parse_args(argv)

    findings = scan_paths([Path(path) for path in args.paths])
    if findings:
        print("Disallowed shell usage detected:")
        print("\n".join(findings))
        return 1

    print("Shell usage check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
