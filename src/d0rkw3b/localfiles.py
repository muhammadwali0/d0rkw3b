"""Bounded local file inspection, with no uploads or subprocesses."""
import hashlib
import mimetypes
import os
import re
import stat
import struct
from datetime import datetime, timezone
from pathlib import Path

from .core.errors import EvidenceError

SAMPLE_LIMIT = 1_048_576


def open_regular(path):
    path = Path(path).expanduser().resolve(strict=True)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0))
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise EvidenceError('only regular local files can be inspected')
        return path, os.fdopen(descriptor, 'rb')
    except BaseException:
        os.close(descriptor)
        raise


def inspect_stream(stream, filename, *, copy_to=None):
    before = os.fstat(stream.fileno())
    digest, size, sample = hashlib.sha256(), 0, bytearray()
    while block := stream.read(SAMPLE_LIMIT):
        size += len(block)
        digest.update(block)
        if len(sample) < SAMPLE_LIMIT:
            sample.extend(block[:SAMPLE_LIMIT - len(sample)])
        if copy_to is not None:
            copy_to.write(block)
    after = os.fstat(stream.fileno())
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise EvidenceError('file changed during acquisition; retry from a stable copy')
    sample = bytes(sample)
    mime, _ = mimetypes.guess_type(str(filename))
    metadata = {'original_filename': Path(filename).name, 'size': size,
                'sha256': digest.hexdigest(), 'mime_type': mime or 'application/octet-stream',
                'mime_basis': 'filename extension (not authoritative)',
                'filesystem_modified_at': datetime.fromtimestamp(before.st_mtime, timezone.utc).isoformat(),
                'filesystem_ctime': datetime.fromtimestamp(before.st_ctime, timezone.utc).isoformat(),
                'sample_bytes': len(sample)}
    if sample.startswith(b'\x89PNG\r\n\x1a\n') and len(sample) >= 24 and sample[12:16] == b'IHDR':
        metadata.update(mime_type='image/png', mime_basis='PNG signature', dimensions=list(struct.unpack('>II', sample[16:24])))
    elif sample[:6] in (b'GIF87a', b'GIF89a') and len(sample) >= 10:
        metadata.update(mime_type='image/gif', mime_basis='GIF signature', dimensions=list(struct.unpack('<HH', sample[6:10])))
    elif sample.startswith(b'%PDF-'):
        metadata.update(mime_type='application/pdf', mime_basis='PDF signature')
    elif sample.startswith(b'\xff\xd8'):
        metadata.update(mime_type='image/jpeg', mime_basis='JPEG signature')
        offset = 2
        while offset + 4 <= len(sample):
            if sample[offset] != 0xff:
                break
            marker = sample[offset + 1]
            if marker in (0xd9, 0xda):
                break
            length = int.from_bytes(sample[offset + 2:offset + 4], 'big')
            if length < 2 or offset + 2 + length > len(sample):
                break
            if marker in (0xc0, 0xc1, 0xc2, 0xc3) and length >= 7:
                height, width = struct.unpack('>HH', sample[offset + 5:offset + 9])
                metadata['dimensions'] = [width, height]
                break
            offset += length + 2
    if b'\x00' not in sample:
        try:
            text = sample.decode('utf-8')
        except UnicodeDecodeError:
            pass
        else:
            # Extraction is a bounded list of textual references, not attribution.
            metadata['references'] = {
                'urls': sorted(set(re.findall(r'https?://[^\s<>"\x00-\x1f]{1,2048}', text)))[:100],
                'emails': sorted(set(re.findall(r'[\w.+-]{1,64}@[\w.-]{1,253}\.[A-Za-z]{2,63}', text)))[:100],
            }
            metadata['references_scope'] = 'first 1 MiB of UTF-8 text; candidates, not verified entities'
    return metadata


def inspect_file(path):
    resolved, stream = open_regular(path)
    with stream:
        result = inspect_stream(stream, resolved)
    return {'path': str(resolved), **result}
