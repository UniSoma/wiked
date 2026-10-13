"""Read distribution identity and release declarations from the installed tree."""

from pathlib import Path
import re

import yaml


SEMVER = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"


def version_tuple(version: str) -> tuple[int, ...]:
    if not isinstance(version, str) or not re.fullmatch(SEMVER, version):
        raise ValueError("Expected a stable SemVer version.")
    return tuple(int(part) for part in version.split("."))


def distribution_version(root: Path | None = None) -> str:
    root = root or Path(__file__).resolve().parents[3]
    manifest = yaml.safe_load((root / "wiked-manifest.yaml").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("namespace") != "wiked":
        raise ValueError("Invalid Wiked distribution manifest.")
    version = manifest.get("distribution_version")
    version_tuple(version)
    return version


def release_declarations(root: Path) -> dict[str, str]:
    """Validate declarations, not the maintainer's semantic impact classification."""
    version = distribution_version(root)
    text = (root / "skills/wiked/CHANGELOG.md").read_text(encoding="utf-8")
    sections = re.split(r"^## ", text, flags=re.MULTILINE)[1:]
    releases = {}
    for section in sections:
        heading, separator, body = section.partition("\n")
        parts = heading.split(" - ")
        if len(parts) != 2 or not separator or not body.strip():
            raise ValueError("Invalid changelog release declaration.")
        declared, impact = parts
        version_tuple(declared)
        if declared in releases or impact not in {"baseline", "review", "none"}:
            raise ValueError("Duplicate release or invalid changelog impact.")
        if impact == "review" and not all(marker in body for marker in ("### Review", "### Action")):
            raise ValueError("Methodological impacts need Review and Action sections.")
        releases[declared] = impact
    ordered = sorted(releases, key=version_tuple, reverse=True)
    if (not ordered or list(releases) != ordered or ordered[0] != version
            or releases[ordered[-1]] != "baseline"
            or sum(impact == "baseline" for impact in releases.values()) != 1):
        raise ValueError("Changelog must cover the current release through one oldest baseline, newest first.")
    return releases
