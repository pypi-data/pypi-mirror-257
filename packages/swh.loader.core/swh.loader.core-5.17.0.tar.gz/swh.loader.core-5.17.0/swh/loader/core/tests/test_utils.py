# Copyright (C) 2019 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from datetime import datetime
import os
import signal
from time import sleep
from unittest.mock import patch

import pytest

from swh.loader.core.utils import (
    CloneFailure,
    CloneTimeout,
    clean_dangling_folders,
    clone_with_timeout,
    compute_nar_hashes,
    parse_visit_date,
)


def prepare_arborescence_from(tmpdir, folder_names):
    """Prepare arborescence tree with folders

    Args:
        tmpdir (Either[LocalPath, str]): Root temporary directory
        folder_names (List[str]): List of folder names

    Returns:
        List of folders
    """
    dangling_folders = []
    for dname in folder_names:
        d = str(tmpdir / dname)
        os.mkdir(d)
        dangling_folders.append(d)
    return str(tmpdir), dangling_folders


def assert_dirs(actual_dirs, expected_dirs):
    """Assert that the directory actual and expected match"""
    for d in actual_dirs:
        assert d in expected_dirs
    assert len(actual_dirs) == len(expected_dirs)


def test_clean_dangling_folders_0(tmpdir):
    """Folder does not exist, do nothing"""
    r = clean_dangling_folders("/path/does/not/exist", "unused-pattern")
    assert r is None


@patch("swh.loader.core.utils.psutil.pid_exists", return_value=False)
def test_clean_dangling_folders_1(mock_pid_exists, tmpdir):
    """Folder which matches pattern with dead pid are cleaned up"""
    rootpath, dangling = prepare_arborescence_from(
        tmpdir,
        [
            "something",
            "swh.loader.svn-4321.noisynoise",
        ],
    )

    clean_dangling_folders(rootpath, "swh.loader.svn")

    actual_dirs = os.listdir(rootpath)
    mock_pid_exists.assert_called_once_with(4321)
    assert_dirs(actual_dirs, ["something"])


@patch("swh.loader.core.utils.psutil.pid_exists", return_value=True)
def test_clean_dangling_folders_2(mock_pid_exists, tmpdir):
    """Folder which matches pattern with live pid are skipped"""
    rootpath, dangling = prepare_arborescence_from(
        tmpdir,
        [
            "something",
            "swh.loader.hg-1234.noisynoise",
        ],
    )

    clean_dangling_folders(rootpath, "swh.loader.hg")

    actual_dirs = os.listdir(rootpath)
    mock_pid_exists.assert_called_once_with(1234)
    assert_dirs(
        actual_dirs,
        [
            "something",
            "swh.loader.hg-1234.noisynoise",
        ],
    )


@patch("swh.loader.core.utils.psutil.pid_exists", return_value=False)
@patch(
    "swh.loader.core.utils.shutil.rmtree",
    side_effect=ValueError("Could not remove for reasons"),
)
def test_clean_dangling_folders_3(mock_rmtree, mock_pid_exists, tmpdir):
    """Error in trying to clean dangling folders are skipped"""
    path1 = "thingy"
    path2 = "swh.loader.git-1468.noisy"
    rootpath, dangling = prepare_arborescence_from(
        tmpdir,
        [
            path1,
            path2,
        ],
    )

    clean_dangling_folders(rootpath, "swh.loader.git")

    actual_dirs = os.listdir(rootpath)
    mock_pid_exists.assert_called_once_with(1468)
    mock_rmtree.assert_called_once_with(os.path.join(rootpath, path2))
    assert_dirs(actual_dirs, [path2, path1])


def test_clone_with_timeout_no_error_no_timeout():
    def succeed():
        """This does nothing to simulate a successful clone"""

    clone_with_timeout("foo", "bar", succeed, timeout=0.5)


def test_clone_with_timeout_no_error_timeout():
    def slow():
        """This lasts for more than the timeout"""
        sleep(1)

    with pytest.raises(CloneTimeout):
        clone_with_timeout("foo", "bar", slow, timeout=0.5)


def test_clone_with_timeout_error():
    def raise_something():
        raise RuntimeError("panic!")

    with pytest.raises(CloneFailure):
        clone_with_timeout("foo", "bar", raise_something, timeout=0.5)


def test_clone_with_timeout_sigkill():
    """This also tests that the traceback is useful"""
    src = "https://www.mercurial-scm.org/repo/hello"
    dest = "/dev/null"
    timeout = 0.5
    sleepy_time = 100 * timeout
    assert sleepy_time > timeout

    def ignores_sigterm(*args, **kwargs):
        # ignore SIGTERM to force sigkill
        signal.signal(signal.SIGTERM, lambda signum, frame: None)
        sleep(sleepy_time)  # we make sure we exceed the timeout

    with pytest.raises(CloneTimeout) as e:
        clone_with_timeout(src, dest, ignores_sigterm, timeout)
    killed = True
    assert e.value.args == (src, timeout, killed)


VISIT_DATE_STR = "2021-02-17 15:50:04.518963"
VISIT_DATE = datetime(2021, 2, 17, 15, 50, 4, 518963)


@pytest.mark.parametrize(
    "input_visit_date,expected_date",
    [
        (None, None),
        (VISIT_DATE, VISIT_DATE),
        (VISIT_DATE_STR, VISIT_DATE),
    ],
)
def test_utils_parse_visit_date(input_visit_date, expected_date):
    assert parse_visit_date(input_visit_date) == expected_date


def test_utils_parse_visit_date_now():
    actual_date = parse_visit_date("now")
    assert isinstance(actual_date, datetime)


def test_utils_parse_visit_date_fails():
    with pytest.raises(ValueError, match="invalid"):
        parse_visit_date(10)  # not a string nor a date


def test_compute_nar_hashes_tarball(tarball_with_nar_hashes):
    tarball_path, nar_checksums = tarball_with_nar_hashes

    actual_checksums = compute_nar_hashes(tarball_path, nar_checksums.keys())

    assert actual_checksums == nar_checksums


def test_compute_nar_hashes_file(content_with_nar_hashes):
    content_path, nar_checksums = content_with_nar_hashes

    actual_checksums = compute_nar_hashes(
        content_path, nar_checksums.keys(), is_tarball=False
    )

    assert actual_checksums == nar_checksums
