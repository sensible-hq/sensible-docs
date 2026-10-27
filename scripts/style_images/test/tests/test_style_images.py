import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import style_images  # noqa: E402

FAKE_CONVERT = """#!/usr/bin/env python3
import sys
src, dst = sys.argv[1], sys.argv[-1]
open(dst, "wb").write(b"styled:" + open(src, "rb").read())
"""


@pytest.fixture
def repo(tmp_path):
    (tmp_path / style_images.SCREENSHOTS).mkdir(parents=True)
    (tmp_path / style_images.FINAL).mkdir(parents=True)
    fake = tmp_path / "fake_convert"
    fake.write_text(FAKE_CONVERT)
    fake.chmod(0o755)
    return tmp_path, str(fake)


def shot(root, name, data):
    (root / style_images.SCREENSHOTS / name).write_bytes(data)


def final(root, name):
    return root / style_images.FINAL / name


def mapping(root):
    return json.loads((root / style_images.MAPPING).read_text())


def test_first_run_styles_everything_and_writes_mapping(repo):
    root, convert = repo
    shot(root, "a.png", b"A")
    shot(root, "b.png", b"B")
    styled, deleted = style_images.sync(root, convert=convert)
    assert (styled, deleted) == (["a.png", "b.png"], [])
    assert final(root, "a.png").read_bytes() == b"styled:A"
    assert set(mapping(root)) == {"a.png", "b.png"}


def test_unchanged_screenshots_are_not_restyled(repo):
    root, convert = repo
    shot(root, "a.png", b"A")
    style_images.sync(root, convert=convert)
    before = (root / style_images.MAPPING).read_text()
    assert style_images.sync(root, convert=convert) == ([], [])
    assert (root / style_images.MAPPING).read_text() == before


def test_only_changed_screenshot_is_restyled(repo):
    root, convert = repo
    shot(root, "a.png", b"A")
    shot(root, "b.png", b"B")
    style_images.sync(root, convert=convert)
    shot(root, "b.png", b"B2")
    assert style_images.sync(root, convert=convert) == (["b.png"], [])
    assert final(root, "b.png").read_bytes() == b"styled:B2"


def test_missing_final_is_restyled(repo):
    root, convert = repo
    shot(root, "a.png", b"A")
    style_images.sync(root, convert=convert)
    final(root, "a.png").unlink()
    assert style_images.sync(root, convert=convert) == (["a.png"], [])


def test_deleted_screenshot_deletes_its_final_and_entry(repo):
    root, convert = repo
    shot(root, "a.png", b"A")
    shot(root, "gone.png", b"G")
    style_images.sync(root, convert=convert)
    (root / style_images.SCREENSHOTS / "gone.png").unlink()
    assert style_images.sync(root, convert=convert) == ([], ["gone.png"])
    assert not final(root, "gone.png").exists()
    assert set(mapping(root)) == {"a.png"}


def test_final_without_a_screenshot_is_never_deleted(repo):
    root, convert = repo
    final(root, "hand_placed.png").write_bytes(b"H")
    shot(root, "a.png", b"A")
    style_images.sync(root, convert=convert)
    assert final(root, "hand_placed.png").read_bytes() == b"H"
    assert "hand_placed.png" not in mapping(root)


def test_only_top_level_pngs_are_sources(repo):
    root, convert = repo
    shot(root, "a.png", b"A")
    shot(root, "anim.gif", b"G")
    shot(root, "notes.txt", b"T")
    (root / style_images.SCREENSHOTS / "archived").mkdir()
    (root / style_images.SCREENSHOTS / "archived" / "old.png").write_bytes(b"O")
    styled, _ = style_images.sync(root, convert=convert)
    assert styled == ["a.png"]


def test_dry_run_writes_nothing(repo):
    root, convert = repo
    shot(root, "a.png", b"A")
    assert style_images.sync(root, dry_run=True, convert=convert) == (["a.png"], [])
    assert not final(root, "a.png").exists()
    assert not (root / style_images.MAPPING).exists()


def test_malformed_mapping_fails_loudly(repo):
    root, convert = repo
    shot(root, "a.png", b"A")
    (root / style_images.MAPPING).write_text("{not json")
    with pytest.raises(SystemExit):
        style_images.sync(root, convert=convert)


@pytest.mark.skipif(shutil.which("convert") is None, reason="ImageMagick not installed")
def test_real_styling_is_deterministic(tmp_path):
    src = tmp_path / "in.png"
    subprocess.run(["convert", "-size", "40x30", "xc:#3366cc", str(src)], check=True)
    a, b = tmp_path / "a.png", tmp_path / "b.png"
    style_images.style("convert", src, a)
    time.sleep(1.2)  # without the timestamp-free flags, a second later gives different bytes
    style_images.style("convert", src, b)
    assert a.read_bytes() == b.read_bytes()
