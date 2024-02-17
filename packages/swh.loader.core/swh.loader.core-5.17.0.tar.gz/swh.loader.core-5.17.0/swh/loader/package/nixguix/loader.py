# Copyright (C) 2020-2021  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import copy
import json
import logging
import re
from typing import Any, Dict, Iterator, List, Mapping, Optional, Set, Tuple

import attr

from swh.loader.package.loader import (
    BasePackageInfo,
    PackageLoader,
    PartialExtID,
    RawExtrinsicMetadataCore,
)
from swh.loader.package.utils import EMPTY_AUTHOR, cached_method, get_url_body
from swh.model import hashutil
from swh.model.model import (
    MetadataAuthority,
    MetadataAuthorityType,
    ObjectType,
    Release,
    Sha1Git,
)
from swh.model.swhids import CoreSWHID
from swh.storage.interface import StorageInterface

logger = logging.getLogger(__name__)

EXTID_TYPE = "subresource-integrity"
"""The ExtID is an ASCII string, as defined by
https://w3c.github.io/webappsec-subresource-integrity/"""

EXTID_VERSION = 0


@attr.s
class NixGuixPackageInfo(BasePackageInfo):
    raw_info = attr.ib(type=Dict[str, Any])

    integrity = attr.ib(type=str)
    """Hash of the archive, formatted as in the Subresource Integrity
    specification."""

    @classmethod
    def from_metadata(
        cls, metadata: Dict[str, Any], version: str
    ) -> "NixGuixPackageInfo":
        return cls(
            url=metadata["url"],
            filename=None,
            version=version,
            integrity=metadata["integrity"],
            raw_info=metadata,
        )

    def extid(self) -> PartialExtID:
        return (EXTID_TYPE, EXTID_VERSION, self.integrity.encode("ascii"))


class NixGuixLoader(PackageLoader[NixGuixPackageInfo]):
    """Load sources from a sources.json file. This loader is used to load
    sources used by functional package manager (eg. Nix and Guix).

    """

    visit_type = "nixguix"

    def __init__(
        self,
        storage: StorageInterface,
        url: str,
        unsupported_file_extensions: List[str] = [],
        **kwargs: Any,
    ):
        super().__init__(storage=storage, url=url, **kwargs)
        self.provider_url = url
        self.unsupported_file_extensions = unsupported_file_extensions

    # Note: this could be renamed get_artifacts in the PackageLoader
    # base class.
    @cached_method
    def raw_sources(self):
        return retrieve_sources(self.origin.url)

    @cached_method
    def supported_sources(self):
        raw_sources = self.raw_sources()
        return clean_sources(
            parse_sources(raw_sources), self.unsupported_file_extensions
        )

    @cached_method
    def integrity_by_url(self) -> Dict[str, str]:
        sources = self.supported_sources()
        return {s["urls"][0]: s["integrity"] for s in sources["sources"]}

    def get_versions(self) -> List[str]:
        """The first mirror of the mirror list is used as branch name in the
        snapshot.

        """
        return list(self.integrity_by_url().keys())

    def get_metadata_authority(self):
        return MetadataAuthority(
            type=MetadataAuthorityType.FORGE,
            url=self.origin.url,
            metadata={},
        )

    def get_extrinsic_snapshot_metadata(self):
        return [
            RawExtrinsicMetadataCore(
                format="nixguix-sources-json",
                metadata=self.raw_sources(),
            ),
        ]

    # Note: this could be renamed get_artifact_info in the PackageLoader
    # base class.
    def get_package_info(self, url) -> Iterator[Tuple[str, NixGuixPackageInfo]]:
        # TODO: try all mirrors and not only the first one. A source
        # can be fetched from several urls, called mirrors. We
        # currently only use the first one, but if the first one
        # fails, we should try the second one and so on.
        integrity = self.integrity_by_url()[url]
        p_info = NixGuixPackageInfo.from_metadata(
            {"url": url, "integrity": integrity}, version=url
        )
        yield url, p_info

    def select_extid_target(
        self, p_info: NixGuixPackageInfo, extid_targets: Set[CoreSWHID]
    ) -> Optional[CoreSWHID]:
        if extid_targets:
            # The archive URL is part of the release name. As that URL is not
            # intrinsic metadata, it means different releases may be created for
            # the same SRI so they have the same extid.
            # Therefore, we need to pick the one with the right URL.
            releases = self.storage.release_get(
                [target.object_id for target in extid_targets]
            )
            extid_targets = {
                release.swhid()
                for release in releases
                if release is not None and release.name == p_info.version.encode()
            }
        return super().select_extid_target(p_info, extid_targets)

    def extra_branches(self) -> Dict[bytes, Mapping[str, Any]]:
        """We add a branch to the snapshot called 'evaluation' pointing to the
        revision used to generate the sources.json file. This revision
        is specified in the sources.json file itself. For the nixpkgs
        origin, this revision is coming from the
        github.com/nixos/nixpkgs repository.

        Note this repository is not loaded explicitly. So, this
        pointer can target a nonexistent revision for a time. However,
        the github and gnu loaders are supposed to load this revision
        and should create the revision pointed by this branch.

        This branch can be used to identify the snapshot associated to
        a Nix/Guix evaluation.

        """
        # The revision used to create the sources.json file. For Nix,
        # this revision belongs to the github.com/nixos/nixpkgs
        # repository
        revision = self.supported_sources()["revision"]
        return {
            b"evaluation": {
                "target_type": "revision",
                "target": hashutil.hash_to_bytes(revision),
            }
        }

    def build_release(
        self, p_info: NixGuixPackageInfo, uncompressed_path: str, directory: Sha1Git
    ) -> Optional[Release]:
        return Release(
            name=p_info.version.encode(),
            message=None,
            author=EMPTY_AUTHOR,
            date=None,
            target=directory,
            target_type=ObjectType.DIRECTORY,
            synthetic=True,
        )


def retrieve_sources(url: str) -> bytes:
    """Retrieve sources. Potentially raise NotFound error."""
    return get_url_body(url, allow_redirects=True)


def parse_sources(raw_sources: bytes) -> Dict[str, Any]:
    return json.loads(raw_sources.decode("utf-8"))


def make_pattern_unsupported_file_extension(
    unsupported_file_extensions: List[str],
):
    """Make a regexp pattern for unsupported file extension out of a list
    of unsupported archive extension list.

    """
    return re.compile(
        rf".*\.({'|'.join(map(re.escape, unsupported_file_extensions))})$", re.DOTALL
    )


def clean_sources(
    sources: Dict[str, Any], unsupported_file_extensions=[]
) -> Dict[str, Any]:
    """Validate and clean the sources structure. First, ensure all top level keys are
    present. Then, walk the sources list and remove sources that do not contain required
    keys.

    Filter out source entries whose:
    - required keys are missing
    - source type is not supported
    - urls attribute type is not a list
    - extension is known not to be supported by the loader

    Raises:
        ValueError if:
        - a required top level key is missing
        - top-level version is not 1

    Returns:
        source Dict cleaned up

    """
    pattern_unsupported_file = make_pattern_unsupported_file_extension(
        unsupported_file_extensions
    )
    # Required top level keys
    required_keys = ["version", "revision", "sources"]
    missing_keys = []
    for required_key in required_keys:
        if required_key not in sources:
            missing_keys.append(required_key)

    if missing_keys != []:
        raise ValueError(
            f"sources structure invalid, missing: {','.join(missing_keys)}"
        )

    # Only the version 1 is currently supported
    version = int(sources["version"])
    if version != 1:
        raise ValueError(
            f"The sources structure version '{sources['version']}' is not supported"
        )

    # If a source doesn't contain required attributes, this source is
    # skipped but others could still be archived.
    verified_sources = []
    for source in sources["sources"]:
        valid = True
        required_keys = ["urls", "integrity", "type"]
        for required_key in required_keys:
            if required_key not in source:
                logger.info(
                    f"Skip source '{source}' because key '{required_key}' is missing",
                )
                valid = False

        if valid and source["type"] != "url":
            logger.info(
                f"Skip source '{source}' because the type {source['type']} "
                "is not supported",
            )
            valid = False

        if valid and not isinstance(source["urls"], list):
            logger.info(
                f"Skip source {source} because the urls attribute is not a list"
            )
            valid = False

        if valid and len(source["urls"]) > 0:  # Filter out unsupported archives
            supported_sources: List[str] = []
            for source_url in source["urls"]:
                if pattern_unsupported_file.match(source_url):
                    logger.info(f"Skip unsupported artifact url {source_url}")
                    continue
                supported_sources.append(source_url)

            if len(supported_sources) == 0:
                logger.info(
                    f"Skip source {source} because urls only reference "
                    "unsupported artifacts. Unsupported "
                    f"artifacts so far: {pattern_unsupported_file}"
                )
                continue

            new_source = copy.deepcopy(source)
            new_source["urls"] = supported_sources
            verified_sources.append(new_source)

    sources["sources"] = verified_sources
    return sources
