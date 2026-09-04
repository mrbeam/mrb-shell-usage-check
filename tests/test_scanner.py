from mrb_shell_usage_check.scanner import scan_file, scan_paths


def test_scan_file_flags_shell_true_and_dynamic_commands(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        "\n".join(
            [
                "import subprocess",
                "name = 'world'",
                "subprocess.run(f'echo {name}', shell=True)",
            ]
        ),
        encoding="utf-8",
    )

    assert scan_file(sample) == [
        (3, "shell=True"),
        (3, "dynamic command construction"),
    ]


def test_scan_paths_walks_directories(tmp_path):
    package = tmp_path / "pkg"
    package.mkdir()
    sample = package / "sample.py"
    sample.write_text(
        "import subprocess\nsubprocess.run([\"echo\", \"ok\"])\n",
        encoding="utf-8",
    )

    findings = scan_paths([tmp_path])

    assert findings == []
