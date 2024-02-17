# Copyright (C) 2019-2024  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import copy
import functools
import itertools
import logging
import os
import re
from typing import Callable, Dict, Optional, Tuple, TypeVar
from urllib.parse import unquote, urlparse, urlsplit
from urllib.request import urlopen

import requests
from tenacity.before_sleep import before_sleep_log

from swh.core.retry import http_retry
from swh.loader.exception import NotFound
from swh.loader.package import DEFAULT_PARAMS
from swh.model.hashutil import HASH_BLOCK_SIZE, MultiHash
from swh.model.model import Person

logger = logging.getLogger(__name__)


DOWNLOAD_HASHES = set(["sha1", "sha256", "length"])


EMPTY_AUTHOR = Person.from_fullname(b"")


def _content_disposition_filename(header: str) -> Optional[str]:
    fname = None
    fnames = re.findall(r"filename[\*]?=([^;]+)", header)
    if fnames and "utf-8''" in fnames[0].lower():
        #  RFC 5987
        fname = re.sub("utf-8''", "", fnames[0], flags=re.IGNORECASE)
        fname = unquote(fname)
    elif fnames:
        fname = fnames[0]
    if fname:
        fname = os.path.basename(fname.strip().strip('"'))
    return fname


@http_retry(
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def download(
    url: str,
    dest: str,
    hashes: Dict = {},
    filename: Optional[str] = None,
    auth: Optional[Tuple[str, str]] = None,
    extra_request_headers: Optional[Dict[str, str]] = None,
) -> Tuple[str, Dict]:
    """Download a remote file from url, and compute swh hashes on it.

    Args:
        url: Artifact uri to fetch and hash
        dest: Directory to write the archive to
        hashes: Dict of expected hashes (key is the hash algo) for the artifact
            to download (those hashes are expected to be hex string). The supported
            algorithms are defined in the :data:`swh.model.hashutil.ALGORITHMS` set.
        auth: Optional tuple of login/password (for http authentication
            service, e.g. deposit)

    Raises:
        ValueError in case of any error when fetching/computing (length,
        checksums mismatched...)

    Returns:
        Tuple of local (filepath, hashes of filepath)

    """
    params = copy.deepcopy(DEFAULT_PARAMS)
    if auth is not None:
        params["auth"] = auth
    if extra_request_headers is not None:
        params["headers"].update(extra_request_headers)
    # so the connection does not hang indefinitely (read/connection timeout)
    timeout = params.get("timeout", 60)

    parsed_url = urlparse(url)
    if parsed_url.scheme == "ftp":
        response = urlopen(url, timeout=timeout)
        chunks = (response.read(HASH_BLOCK_SIZE) for _ in itertools.count())
    elif parsed_url.scheme == "file":
        response = open(parsed_url.path, "rb")
        chunks = (response.read(HASH_BLOCK_SIZE) for _ in itertools.count())
    else:
        # request artifact raw bytes without extra compression as requests set
        # Accept-Encoding header to "gzip, deflate" by default
        params["headers"]["Accept-Encoding"] = "identity"
        response = requests.get(url, **params, timeout=timeout, stream=True)
        response.raise_for_status()
        # update URL to response one as requests follow redirection by default
        # on GET requests
        url = response.url
        # try to extract filename from content-disposition header if available
        if filename is None and "content-disposition" in response.headers:
            filename = _content_disposition_filename(
                response.headers["content-disposition"]
            )
        content_type = response.headers.get("content-type")
        content_encoding = response.headers.get("content-encoding", "")
        if (
            content_type
            in {"application/x-gzip", "application/gzip", "application/x-gunzip"}
            and "gzip" in content_encoding
        ):
            # prevent automatic deflate of response bytes by requests
            chunks = response.raw.stream(HASH_BLOCK_SIZE, decode_content=False)
        else:
            chunks = response.iter_content(chunk_size=HASH_BLOCK_SIZE)

    response_data = itertools.takewhile(bool, chunks)

    filename = filename if filename else os.path.basename(urlsplit(url).path)

    logger.debug("filename: %s", filename)
    filepath = os.path.join(dest, filename)
    logger.debug("filepath: %s", filepath)

    h = MultiHash(hash_names=DOWNLOAD_HASHES | set(hashes.keys()))
    with open(filepath, "wb") as f:
        for chunk in response_data:
            h.update(chunk)
            f.write(chunk)

    response.close()

    # Also check the expected hashes if provided
    if hashes:
        actual_hashes = h.hexdigest()
        for algo_hash in hashes.keys():
            actual_digest = actual_hashes[algo_hash]
            expected_digest = hashes[algo_hash]
            if actual_digest != expected_digest:
                raise ValueError(
                    "Failure when fetching %s. "
                    "Checksum mismatched: %s != %s"
                    % (url, expected_digest, actual_digest)
                )

    computed_hashes = h.hexdigest()
    length = computed_hashes.pop("length")
    extrinsic_metadata = {
        "length": length,
        "filename": filename,
        "checksums": computed_hashes,
        "url": url,
    }

    logger.debug("extrinsic_metadata: %s", extrinsic_metadata)

    return filepath, extrinsic_metadata


@http_retry(
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def get_url_body(url: str, **extra_params) -> bytes:
    """Basic HTTP client to retrieve information on software package,
    typically JSON metadata from a REST API.

    Args:
        url (str): An HTTP URL

    Raises:
        NotFound in case of query failures (for some reasons: 404, ...)

    Returns:
        The associated response's information

    """
    logger.debug("Fetching %s", url)
    response = requests.get(url, **{**DEFAULT_PARAMS, **extra_params})
    if response.status_code == 404:
        raise NotFound(f"Fail to query '{url}'. Reason: {response.status_code}")
    response.raise_for_status()
    return response.content


def release_name(version: str, filename: Optional[str] = None) -> str:
    if filename:
        return "releases/%s/%s" % (version, filename)
    return "releases/%s" % version


TReturn = TypeVar("TReturn")
TSelf = TypeVar("TSelf")

_UNDEFINED = object()


def cached_method(f: Callable[[TSelf], TReturn]) -> Callable[[TSelf], TReturn]:
    cache_name = f"_cached_{f.__name__}"

    @functools.wraps(f)
    def newf(self):
        value = getattr(self, cache_name, _UNDEFINED)
        if value is _UNDEFINED:
            value = f(self)
            setattr(self, cache_name, value)
        return value

    return newf
