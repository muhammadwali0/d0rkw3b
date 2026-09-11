"""Validate built archives and produce SHA-256 checksums plus an SPDX runtime SBOM."""

import base64
import csv
import hashlib
import io
import json
import sys
import tarfile
import uuid
import zipfile
from datetime import datetime, timezone
from email.parser import BytesParser
from pathlib import Path, PurePosixPath


def inspect_wheel(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("duplicate wheel archive member")
        for name in names:
            if (
                PurePosixPath(name).is_absolute()
                or ".." in PurePosixPath(name).parts
                or name.endswith(".pyc")
            ):
                raise ValueError("unsafe or generated wheel member: " + name)
        metadata_names = [n for n in names if n.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise ValueError(
                "wheel must contain exactly one distribution metadata file"
            )
        metadata = BytesParser().parsebytes(archive.read(metadata_names[0]))
        if metadata["Name"].lower() != "d0rkw3b":
            raise ValueError("unexpected package name")
        for requirement in metadata.get_all("Requires-Dist", []):
            if "extra ==" not in requirement:
                raise ValueError("unexpected base runtime dependency: " + requirement)
        for category in ("providers", "recipes"):
            if not any(
                f"d0rkw3b/{category}/" in n and n.endswith(".json") for n in names
            ):
                raise ValueError("missing bundled data: " + category)
        record = metadata_names[0].replace("METADATA", "RECORD")
        for name, checksum, size in csv.reader(
            io.StringIO(archive.read(record).decode())
        ):
            data = archive.read(name)
            if name == record:
                continue
            expected = (
                "sha256="
                + base64.urlsafe_b64encode(hashlib.sha256(data).digest())
                .rstrip(b"=")
                .decode()
            )
            if checksum != expected or int(size) != len(data):
                raise ValueError("wheel RECORD verification failed for " + name)
        return metadata["Version"]


def build_manifest(directory):
    directory = Path(directory)
    archives = sorted([*directory.glob("*.whl"), *directory.glob("*.tar.gz")])
    if len([p for p in archives if p.suffix == ".whl"]) != 1 or len(archives) != 2:
        raise ValueError(
            "use a clean directory with exactly one wheel and one source distribution"
        )
    version = inspect_wheel(next(p for p in archives if p.suffix == ".whl"))
    source = next(p for p in archives if p.name.endswith(".tar.gz"))
    with tarfile.open(source) as archive:
        for member in archive.getmembers():
            if (
                PurePosixPath(member.name).is_absolute()
                or ".." in PurePosixPath(member.name).parts
                or member.issym()
                or member.islnk()
            ):
                raise ValueError("unsafe source archive member")
    packages = []
    for index, path in enumerate(archives):
        packages.append(
            {
                "SPDXID": f"SPDXRef-Distribution-{index}",
                "name": "d0rkw3b",
                "versionInfo": version,
                "packageFileName": path.name,
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "MIT",
                "copyrightText": "NOASSERTION",
                "checksums": [
                    {
                        "algorithm": "SHA256",
                        "checksumValue": hashlib.sha256(path.read_bytes()).hexdigest(),
                    }
                ],
            }
        )
    sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "D0RKW3B distribution runtime SBOM",
        "documentNamespace": "https://spdx.org/spdxdocs/d0rkw3b-" + str(uuid.uuid4()),
        "creationInfo": {
            "creators": ["Tool: D0RKW3B release_manifest.py"],
            "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "documentDescribes": [p["SPDXID"] for p in packages],
        "packages": packages,
    }
    path = directory / "d0rkw3b.spdx.json"
    path.write_text(json.dumps(sbom, indent=2) + "\n", encoding="utf-8")
    (directory / "SHA256SUMS").write_text(
        "".join(
            hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n"
            for p in [*archives, path]
        ),
        encoding="ascii",
    )
    print(
        f"Verified wheel RECORD and source members; generated checksums and SPDX SBOM for {version}."
    )


if __name__ == "__main__":
    build_manifest(sys.argv[1] if len(sys.argv) > 1 else "dist")
