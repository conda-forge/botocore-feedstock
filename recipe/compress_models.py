"""Match PyPI's model compression with gzip; botocore reads gzip transparently in memory."""

import gzip
from pathlib import Path


# Only these supporting files may stay uncompressed, matching upstream wheels.
uncompressed_names = {
    "_retry.json",
    "endpoints.json",
    "examples-1.json",
    "paginators-1.json",
    "paginators-1.sdk-extras.json",
    "partitions.json",
    "sdk-default-configuration.json",
    "service-2.sdk-extras.json",
    "waiters-2.json",
}
models = [
    model
    for model in Path("botocore/data").rglob("*")
    if model.is_file() and model.name not in uncompressed_names
]
names = {model.name for model in models}
if names != {"service-2.json", "endpoint-rule-set-1.json"}:
    raise RuntimeError(
        f"Upstream model filenames changed; review compression in build's 'compress_models.py': {sorted(names)}"
    )

for model in models:
    compressed = gzip.compress(model.read_bytes(), compresslevel=9, mtime=0)
    model.with_suffix(".json.gz").write_bytes(compressed)
    model.unlink()
