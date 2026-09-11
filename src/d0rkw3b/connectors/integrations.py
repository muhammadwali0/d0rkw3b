"""Optional installed-tool detection and the tested ExifTool adapter."""

import shutil

from ..core.errors import ConnectorUnavailableError
from ..localfiles import open_regular
from .builtin import observation
from .models import Capabilities, Collection, Manifest
from .process import run_json

EXIFTOOL = Manifest(
    "exiftool",
    "ExifTool local metadata",
    ("file",),
    (),
    Capabilities(filesystem_read=True, subprocess=True),
    "Read image/document EXIF, GPS, dimensions, author and time tags through installed ExifTool. Never write or upload.",
    "One regular local file; fixed read-only options, 2 MiB output cap, no user ExifTool config.",
    15,
)

TOOLS = {
    "sherlock": "sherlock",
    "maigret": "maigret",
    "exiftool": "exiftool",
    "theharvester": "theHarvester",
    "amass": "amass",
}


def integrations():
    return [
        {
            "id": key,
            "executable": shutil.which(binary),
            "installed": shutil.which(binary) is not None,
            "adapter": "available" if key == "exiftool" else "detection-only",
        }
        for key, binary in TOOLS.items()
    ]


def exiftool(entity, *, timeout=15):
    executable = shutil.which("exiftool")
    if executable is None:
        raise ConnectorUnavailableError(
            "ExifTool is not installed; install it separately to enable this optional adapter"
        )
    path, stream = open_regular(entity.normalized_value)
    stream.close()
    tags = [
        "-FileType",
        "-MIMEType",
        "-ImageWidth",
        "-ImageHeight",
        "-Make",
        "-Model",
        "-DateTimeOriginal",
        "-CreateDate",
        "-ModifyDate",
        "-GPSLatitude",
        "-GPSLongitude",
        "-GPSAltitude",
        "-Author",
        "-Title",
        "-Creator",
        "-Producer",
        "-PageCount",
    ]
    rows = run_json(
        [executable, "-config", "", "-j", "-G1", "-n", "-s", *tags, "--", str(path)],
        timeout=timeout,
    )
    if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict):
        raise ConnectorUnavailableError("ExifTool returned an unexpected JSON shape")
    if any(key.split(":")[-1] == "Error" for key in rows[0]):
        raise ConnectorUnavailableError("ExifTool could not read metadata")
    item = observation(entity, "exiftool", "read-only installed ExifTool JSON", rows[0])
    return Collection(entity, [entity], [], [item])
