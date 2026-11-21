import io

import pytest

from turkmen_translit.cli import main


def run(argv, capsys, stdin=None, monkeypatch=None):
    if stdin is not None:
        monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
    rc = main(argv)
    out = capsys.readouterr().out
    return rc, out


def test_auto_cyrillic_to_latin(capsys):
    rc, out = run(["салам"], capsys)
    assert rc == 0
    assert out == "salam"


def test_auto_latin_to_cyrillic(capsys):
    _, out = run(["salam"], capsys)
    assert out == "салам"


def test_force_to_latin(capsys):
    _, out = run(["--to-latin", "Ашгабат"], capsys)
    assert out == "Aşgabat"


def test_detect(capsys):
    _, out = run(["--detect", "salam"], capsys)
    assert out.strip() == "latin"


def test_stdin(capsys, monkeypatch):
    _, out = run([], capsys, stdin="salam", monkeypatch=monkeypatch)
    assert out == "салам"


def test_files(tmp_path, capsys):
    src = tmp_path / "in.txt"
    dst = tmp_path / "out.txt"
    src.write_text("салам", encoding="utf-8")
    rc = main(["-i", str(src), "-o", str(dst)])
    assert rc == 0
    assert dst.read_text(encoding="utf-8") == "salam"


def test_version(capsys):
    with pytest.raises(SystemExit) as e:
        main(["--version"])
    assert e.value.code == 0
    assert "turkmen-translit" in capsys.readouterr().out
