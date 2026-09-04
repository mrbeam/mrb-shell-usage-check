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
        (3, "shell=True", "subprocess.run(f'echo {name}', shell=True)"),
        (
            3,
            "dynamic command construction",
            "subprocess.run(f'echo {name}', shell=True)",
        ),
    ]


def test_scan_file_flags_string_subprocess_commands(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        "import subprocess\nsubprocess.check_output('echo ok')\n",
        encoding="utf-8",
    )

    assert scan_file(sample) == [
        (2, "string command instead of argv", "subprocess.check_output('echo ok')")
    ]


def test_scan_file_flags_os_system_even_with_literal_command(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        "import os\nos.system('echo ok')\n",
        encoding="utf-8",
    )

    assert scan_file(sample) == [
        (2, "os.system is always shell-backed", "os.system('echo ok')")
    ]


def test_scan_paths_walks_directories(tmp_path):
    package = tmp_path / "pkg"
    package.mkdir()
    sample = package / "sample.py"
    sample.write_text(
        "import subprocess\nsubprocess.run([\"echo\", \"ok\"])\n",
        encoding="utf-8",
    )

    findings = scan_paths([tmp_path], base_dir=tmp_path)

    assert findings == []


def test_scan_paths_includes_relative_file_and_source_context(tmp_path):
    package = tmp_path / "pkg"
    package.mkdir()
    sample = package / "sample.py"
    sample.write_text(
        "import os\nos.system('echo ok')\n",
        encoding="utf-8",
    )

    findings = scan_paths([tmp_path], base_dir=tmp_path)

    assert findings == [
        "pkg/sample.py:2: os.system is always shell-backed\n    os.system('echo ok')"
    ]
