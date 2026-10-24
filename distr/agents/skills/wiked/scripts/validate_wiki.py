#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jsonschema>=4.23,<5",
#   "markdown-it-py>=3,<4",
#   "PyYAML>=6,<7",
# ]
# ///
"""Validate the portable structural core of a Wiked instance."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from markdown_it import MarkdownIt

# Validation must not create bytecode inside the installed, hashed distribution.
sys.dont_write_bytecode = True
from distribution import distribution_version


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    path: str
    line: int | None
    message: str


def issue(code: str, severity: str, path: Path | str, message: str, line: int | None = None) -> Diagnostic:
    return Diagnostic(code, severity, Path(path).as_posix(), line, message)


def issue_key(item: Diagnostic) -> tuple[Any, ...]:
    return (item.path, item.line is None, item.line or 0, item.code, item.message)


def load_data(path: Path, display_path: str) -> tuple[Any, Diagnostic | None]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, issue("contract.missing", "error", display_path, "Contract file not found.")
    except (OSError, UnicodeError) as exc:
        return None, issue("contract.read", "error", display_path, f"Could not read contract: {exc}")
    except yaml.MarkedYAMLError as exc:
        line = exc.problem_mark.line + 1 if exc.problem_mark else None
        return None, issue("contract.yaml", "error", display_path, f"Invalid contract YAML: {exc.problem or exc}", line)
    except yaml.YAMLError as exc:
        return None, issue("contract.yaml", "error", display_path, f"Invalid contract YAML: {exc}")


def json_path(error: Any) -> str:
    return ".".join(str(part) for part in error.absolute_path) or "contract"


def validate_contract(contract_path: Path, schema_path: Path) -> tuple[dict[str, Any] | None, list[Diagnostic]]:
    contract_label = "wiki/wiki-structure.yaml"
    schema_label = "contracts/wiki-structure.schema.json"
    contract, load_issue = load_data(contract_path, contract_label)
    if load_issue:
        return None, [load_issue]
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except FileNotFoundError:
        return None, [issue("runtime.schema-missing", "error", schema_label, "Bundled contract schema not found.")]
    except (OSError, UnicodeError, json.JSONDecodeError, SchemaError) as exc:
        return None, [issue("runtime.schema", "error", schema_label, f"Could not load bundled contract schema: {exc}")]

    validator = Draft202012Validator(schema)
    problems = [
        issue("contract.schema", "error", contract_label, f"{json_path(error)}: {error.message}; received {error.instance!r}")
        for error in sorted(validator.iter_errors(contract), key=lambda item: (list(item.absolute_path), item.message))
    ]
    if problems:
        return None, problems

    assert isinstance(contract, dict)
    relations: list[Diagnostic] = []
    try:
        methodology_version = distribution_version()
    except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as exc:
        return None, [issue("runtime.version", "error", "wiked-manifest.yaml", f"Could not load distribution version: {exc}")]
    required_version = tuple(int(part) for part in contract["methodology_version"].split("."))
    installed_version = tuple(int(part) for part in methodology_version.split("."))
    if required_version[0] != installed_version[0] or required_version > installed_version:
        relations.append(issue("contract.relation", "error", contract_label, f"Methodology version {contract['methodology_version']!r} is incompatible with installed version {methodology_version!r}."))
    try:
        re.compile(contract["naming"]["pattern"])
    except re.error as exc:
        relations.append(issue("contract.relation", "error", contract_label, f"Invalid naming pattern: {exc}"))
    topology = contract["topology"]
    trunks = set(topology["trunks"])
    required = set(topology["required_trunks"])
    sources = topology["sources_trunk"]
    if not required <= trunks:
        relations.append(issue("contract.relation", "error", contract_label, "Every required trunk must be declared in topology.trunks."))
    if sources not in required:
        relations.append(issue("contract.relation", "error", contract_label, "The sources trunk must be a required trunk."))
    if topology["assets_directory"] in trunks:
        relations.append(issue("contract.relation", "error", contract_label, "The assets directory cannot also be a trunk."))
    navigation = contract["navigation"]
    intent_map = navigation.get("intent_map")
    if intent_map is not None:
        if required_version < (1, 5, 0):
            relations.append(issue("contract.relation", "error", contract_label, "An intent map requires methodology_version 1.5.0 or newer."))
        if intent_map in {navigation["root_index"], navigation["trunk_index"], navigation["context_file"], navigation.get("authoring_file")}:
            relations.append(issue("contract.relation", "error", contract_label, "The intent map must be distinct from configured index, context, and authoring files."))
    authoring_file = navigation.get("authoring_file")
    if authoring_file is not None and authoring_file in {
        navigation["root_index"], navigation["trunk_index"], navigation["context_file"]
    }:
        relations.append(issue("contract.relation", "error", contract_label, "The authoring file must be distinct from configured index and context files."))
    states = set(contract["states"])
    page_types = set(contract["page_types"])
    roles: set[str] = set()
    for name, page_type in contract["page_types"].items():
        roles.update(page_type["roles"])
        fields = page_type["fields"]
        allowed_fields = set(fields["required"]) | set(fields["optional"])
        if not {"type", "state"} <= set(fields["required"]):
            relations.append(issue("contract.relation", "error", contract_label, f"Page type {name!r} must require the type and state fields."))
        if not set(page_type["states"]) <= states:
            relations.append(issue("contract.relation", "error", contract_label, f"Page type {name!r} uses a state not declared in states."))
        if set(fields["required"]) & set(fields["optional"]):
            relations.append(issue("contract.relation", "error", contract_label, f"Page type {name!r} declares a field as both required and optional."))
        if not set(fields["date"]) <= allowed_fields:
            relations.append(issue("contract.relation", "error", contract_label, f"Page type {name!r} has a date field that is not allowed."))
    for collection in contract.get("structured_sections", []):
        configured_types = set(collection["page_types"])
        if not configured_types <= page_types:
            relations.append(issue("contract.relation", "error", contract_label, f"Structured section {collection['section']!r} uses an unknown page type."))
        maximum = collection["max_records"]
        if maximum is not None and maximum < collection["min_records"]:
            relations.append(issue("contract.relation", "error", contract_label, f"Structured section {collection['section']!r} has a maximum record count below its minimum."))
        names = [field["name"] for field in collection["fields"]]
        if len(names) != len(set(names)):
            relations.append(issue("contract.relation", "error", contract_label, f"Structured section {collection['section']!r} repeats a field name."))
        for field in collection["fields"]:
            maximum = field["max_items"]
            if maximum is not None and maximum < field["min_items"]:
                relations.append(issue("contract.relation", "error", contract_label, f"Structured field {field['name']!r} has a maximum item count below its minimum."))
            if "empty_value" in field and field["min_items"] != 0:
                relations.append(issue("contract.relation", "error", contract_label, f"Structured field {field['name']!r} has an empty value but requires items."))
            if not set(field.get("disjoint_with", [])) <= set(names) - {field["name"]}:
                relations.append(issue("contract.relation", "error", contract_label, f"Structured field {field['name']!r} has an unknown disjoint field."))
            if field.get("disjoint_with") and "page" not in field["value_types"]:
                relations.append(issue("contract.relation", "error", contract_label, f"Structured field {field['name']!r} uses disjoint fields without accepting page values."))
    diagram_roles = set(contract["diagrams"]["applies_to_roles"])
    if not diagram_roles <= roles:
        relations.append(issue("contract.relation", "error", contract_label, "Every diagram role must be declared by a page type."))
    diagrams = contract["diagrams"]
    extensions = set(diagrams["required_extensions"])
    if diagrams["source_extension"] not in extensions or diagrams["visualization_extension"] not in extensions:
        relations.append(issue("contract.relation", "error", contract_label, "Diagram source and visualization extensions must be required extensions."))
    provenance = contract["provenance"]
    if provenance["source_role"] not in roles:
        relations.append(issue("contract.relation", "error", contract_label, "The provenance source role must be declared by a page type."))
    if not set(provenance["content_roles"]) <= roles:
        relations.append(issue("contract.relation", "error", contract_label, "Every provenance content role must be declared by a page type."))
    if provenance["source_role"] in provenance["content_roles"]:
        relations.append(issue("contract.relation", "error", contract_label, "The provenance source role cannot also be a content role."))
    if provenance["publication_date_field"] not in provenance["record_fields"]:
        relations.append(issue("contract.relation", "error", contract_label, "The publication date field must be declared in provenance.record_fields."))
    if not set(provenance["date_fields"]) <= set(provenance["record_fields"]):
        relations.append(issue("contract.relation", "error", contract_label, "Every provenance date field must be declared in provenance.record_fields."))
    if provenance["indexed_record_field"] not in provenance["date_fields"]:
        relations.append(issue("contract.relation", "error", contract_label, "The indexed record field must be declared in provenance.date_fields."))
    for name, page_type in contract["page_types"].items():
        if provenance["source_role"] not in page_type["roles"]:
            continue
        fields = page_type["fields"]
        allowed_fields = set(fields["required"]) | set(fields["optional"])
        if provenance["indexed_field"] not in allowed_fields:
            relations.append(issue("contract.relation", "error", contract_label, f"Source page type {name!r} must allow the indexed field {provenance['indexed_field']!r}."))
        elif provenance["indexed_field"] not in fields["date"]:
            relations.append(issue("contract.relation", "error", contract_label, f"Source page type {name!r} must classify the indexed field {provenance['indexed_field']!r} as a date."))
        if not set(provenance["no_content_states"]) <= set(page_type["states"]):
            relations.append(issue("contract.relation", "error", contract_label, f"Every no-content state must be allowed by source page type {name!r}."))
    for kind in ("pendency", "proposal"):
        tracking = contract[f"{kind}_tracking"]
        if not set(tracking["roles"]) <= roles:
            relations.append(issue("contract.relation", "error", contract_label, f"Every {kind} tracking role must be declared by a page type."))
        if set(tracking["valid_statuses"]) & set(tracking["warning_statuses"]):
            relations.append(issue("contract.relation", "error", contract_label, f"{kind.title()} valid and warning statuses must not overlap."))
        try:
            re.compile(tracking["id_pattern"])
        except re.error as exc:
            relations.append(issue("contract.relation", "error", contract_label, f"Invalid {kind} ticket ID pattern: {exc}"))
    proposal = contract["proposal_tracking"]
    for name, page_type in contract["page_types"].items():
        if not set(page_type["roles"]) & set(proposal["roles"]):
            continue
        if proposal["proposal_state"] not in page_type["states"]:
            relations.append(issue("contract.relation", "error", contract_label, f"Proposal page type {name!r} must allow the proposal state {proposal['proposal_state']!r}."))
        field = proposal["frontmatter_field"]
        if field not in set(page_type["fields"]["required"]) | set(page_type["fields"]["optional"]):
            relations.append(issue("contract.relation", "error", contract_label, f"Proposal page type {name!r} must allow the configured frontmatter field {field!r}."))
    return (contract if not relations else None), relations


def severity(contract: dict[str, Any], rule: str) -> str:
    return contract["rules"][rule]["severity"]


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def markdown_links(text: str, line_offset: int = 0) -> list[tuple[str, int, bool]]:
    links: list[tuple[str, int, bool]] = []
    for token in MarkdownIt().parse(text):
        if token.type != "inline" or not token.map:
            continue
        line = token.map[0] + line_offset + 1
        for child in token.children or []:
            if child.type == "link_open":
                target = dict(child.attrs or []).get("href")
                if target is not None:
                    links.append((target, line, False))
            elif child.type == "image":
                target = dict(child.attrs or []).get("src")
                if target is not None:
                    links.append((target, line, True))
    return links


def split_page(path: Path, marker: str) -> tuple[dict[str, Any] | None, str, int, Diagnostic | None]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != marker:
        return {}, "".join(lines), 0, None
    closing = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == marker), None)
    if closing is None:
        return None, "", 0, issue("frontmatter.syntax", "error", path, "Frontmatter closing marker is missing.", 1)
    try:
        value = yaml.safe_load("".join(lines[1:closing]))
    except yaml.MarkedYAMLError as exc:
        line = exc.problem_mark.line + 2 if exc.problem_mark else 2
        return None, "", 0, issue("frontmatter.syntax", "error", path, f"Invalid frontmatter YAML: {exc.problem or exc}", line)
    if not isinstance(value, dict):
        return None, "", 0, issue("frontmatter.syntax", "error", path, "Frontmatter must be a YAML mapping.", 2)
    return value, "".join(lines[closing + 1 :]), closing + 1, None


def explicit_anchors(body: str, offset: int) -> list[tuple[str, int]]:
    """Collect portable <a id="..."> targets, excluding code and comments."""
    anchors: list[tuple[str, int]] = []

    class AnchorParser(HTMLParser):
        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            identifier = dict(attrs).get("id")
            if tag == "a" and identifier and not re.search(r"\s", identifier):
                anchors.append((identifier, base_line + self.getpos()[0] - 1))

        handle_startendtag = handle_starttag

    for token in MarkdownIt("commonmark", {"html": True}).parse(body):
        base_line = (token.map[0] if token.map else 0) + offset + 1
        html = [token] if token.type == "html_block" else [
            child for child in token.children or [] if child.type == "html_inline"
        ]
        for fragment in html:
            AnchorParser().feed(fragment.content)
    return anchors


def heading_data(body: str, offset: int, *, include_explicit: bool = True) -> tuple[list[int], set[str], set[str]]:
    h1_lines: list[int] = []
    headings: set[str] = set()
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    tokens = MarkdownIt().parse(body)
    for index, token in enumerate(tokens):
        if token.type != "heading_open" or not token.map:
            continue
        title = tokens[index + 1].content if index + 1 < len(tokens) and tokens[index + 1].type == "inline" else ""
        headings.add(title)
        if token.tag == "h1":
            h1_lines.append(token.map[0] + offset + 1)
        slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
        slug = re.sub(r"[^a-z0-9 -]", "", slug)
        slug = re.sub(r"[ -]+", "-", slug).strip("-") or "section"
        count = counts.get(slug, 0)
        anchors.add(f"{slug}-{count}" if count else slug)
        counts[slug] = count + 1
    if include_explicit:
        anchors.update(identifier for identifier, _ in explicit_anchors(body, offset))
    return h1_lines, headings, anchors


def iso_date(value: Any) -> bool:
    if isinstance(value, datetime):
        return False
    if isinstance(value, date):
        return True
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_page(path: Path, wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    rel = relative(path, wiki_root)
    if rel == contract["navigation"].get("intent_map"):
        # This auxiliary is validated separately and can never acquire a page role.
        return []
    frontmatter, body, offset, parse_issue = split_page(path, contract["frontmatter"]["marker"])
    if parse_issue:
        return [Diagnostic(parse_issue.code, severity(contract, "frontmatter"), rel, parse_issue.line, parse_issue.message)]
    h1_lines, headings, _ = heading_data(body, offset)
    problems: list[Diagnostic] = []
    if len(h1_lines) != 1:
        problems.append(issue("h1.count", severity(contract, "h1"), rel, "Page must contain exactly one H1 heading.", h1_lines[0] if h1_lines else None))
    if path.name in contract["frontmatter"]["exceptions"] or rel == contract["navigation"].get("authoring_file"):
        return problems
    if not frontmatter:
        problems.append(issue("frontmatter.missing", severity(contract, "frontmatter"), rel, "Frontmatter is required."))
        return problems
    page_type = frontmatter.get("type")
    if page_type not in contract["page_types"]:
        problems.append(issue("frontmatter.type", severity(contract, "frontmatter"), rel, f"Unknown page type: {page_type!r}.", 1))
        return problems
    config = contract["page_types"][page_type]
    if frontmatter.get("state") not in config["states"]:
        problems.append(issue("frontmatter.state", severity(contract, "frontmatter"), rel, f"State is not allowed for page type {page_type!r}: {frontmatter.get('state')!r}.", 1))
    required = set(config["fields"]["required"])
    optional = set(config["fields"]["optional"])
    for field in sorted(required - set(frontmatter)):
        problems.append(issue("frontmatter.required", severity(contract, "frontmatter"), rel, f"Required frontmatter field is missing: {field}.", 1))
    for field in sorted(set(frontmatter) - required - optional):
        problems.append(issue("frontmatter.unknown", severity(contract, "frontmatter"), rel, f"Undeclared frontmatter field: {field}.", 1))
    for field in config["fields"]["date"]:
        if field in frontmatter and not iso_date(frontmatter[field]):
            problems.append(issue("frontmatter.date", severity(contract, "frontmatter"), rel, f"Invalid ISO date in field {field}: {frontmatter[field]!r}.", 1))
    for heading in config["sections"]["required"]:
        if heading not in headings:
            problems.append(issue("frontmatter.section", severity(contract, "frontmatter"), rel, f"Required heading is missing: {heading}."))
    return problems


def validate_initial_content(wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    """Check the human-approved minimum content created by Wiked setup."""
    initial = contract["initial_content"]
    navigation = contract["navigation"]
    checks = (
        (wiki_root / navigation["root_index"], "root index", ("title", "purpose", "audience", "scope")),
        (wiki_root / navigation["context_file"], "context file", ("context_terms",)),
    )
    problems: list[Diagnostic] = []
    for path, label, fields in checks:
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        required = (
            [initial[field] for field in fields]
            if fields != ("context_terms",)
            else [value for item in initial["context_terms"] for value in (item["term"], item["definition"])]
        )
        for value in required:
            if value not in content:
                problems.append(issue("setup.initial-content", severity(contract, "contract"), relative(path, wiki_root), f"Configured {label} value is missing: {value!r}."))
    return problems


def local_target(path: Path, wiki_root: Path, target: str) -> Path | None:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    resolved = (path.parent / unquote(parsed.path)).resolve()
    try:
        resolved.relative_to(wiki_root.resolve())
    except ValueError:
        return Path()
    return resolved


def validate_references(path: Path, wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    rel = relative(path, wiki_root)
    frontmatter, body, offset, parse_issue = split_page(path, contract["frontmatter"]["marker"])
    if parse_issue:
        return []
    problems: list[Diagnostic] = []
    _, _, own_anchors = heading_data(body, offset, include_explicit=False)
    for identifier, line in explicit_anchors(body, offset):
        if identifier in own_anchors:
            problems.append(issue("reference.anchor", severity(contract, "reference"), rel, f"Explicit anchor is duplicated or collides with a heading: {identifier}.", line))
        own_anchors.add(identifier)
    for target, line, _ in markdown_links(body, offset):
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        if target.startswith("#"):
            if unquote(parsed.fragment) not in own_anchors:
                problems.append(issue("reference.fragment", severity(contract, "reference"), rel, f"Local fragment does not exist: {parsed.fragment}.", line))
            continue
        destination = local_target(path, wiki_root, target)
        if destination == Path():
            problems.append(issue("reference.boundary", severity(contract, "reference"), rel, "Reference leaves the wiki boundary.", line))
            continue
        if destination is None:
            continue
        if not destination.is_file():
            problems.append(issue("reference.missing", severity(contract, "reference"), rel, f"Local reference does not exist: {parsed.path}.", line))
            continue
        if parsed.fragment and destination.suffix == ".md":
            _, target_body, target_offset, target_issue = split_page(destination, contract["frontmatter"]["marker"])
            if not target_issue and unquote(parsed.fragment) not in heading_data(target_body, target_offset)[2]:
                problems.append(issue("reference.fragment", severity(contract, "reference"), rel, f"Target fragment does not exist: {parsed.fragment}.", line))
        params = parse_qs(parsed.fragment, keep_blank_values=True) if destination.suffix == ".svg" else {}
        if "wiked-node" in params:
            node = params.get("wiked-node", [])
            section = params.get("section", [])
            if (set(params) != {"wiked-node", "section"} or len(node) != 1 or len(section) != 1
                    or not re.fullmatch(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*", node[0])
                    or not re.fullmatch(r"[a-z][a-z0-9_]*", section[0])):
                problems.append(issue("reference.diagram", severity(contract, "reference"), rel, "Malformed optional diagram return link.", line))
            elif section[0] not in own_anchors:
                problems.append(issue("reference.fragment", severity(contract, "reference"), rel, f"Diagram description anchor does not exist: {section[0]}.", line))
    return problems


def validate_topology(wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    topology = contract["topology"]
    navigation = contract["navigation"]
    trunks = set(topology["trunks"])
    assets = topology["assets_directory"]
    name_pattern = re.compile(contract["naming"]["pattern"])
    problems: list[Diagnostic] = []
    for required in topology["required_trunks"]:
        if not (wiki_root / required).is_dir():
            problems.append(issue("topology.required-trunk", severity(contract, "topology"), required, f"Required trunk is missing: {required}."))
    required_files = [navigation["root_index"], navigation["context_file"]]
    if "authoring_file" in navigation:
        required_files.append(navigation["authoring_file"])
    if "intent_map" in navigation:
        required_files.append(navigation["intent_map"])
    for required_file in required_files:
        if not (wiki_root / required_file).is_file():
            problems.append(issue("topology.required-file", severity(contract, "topology"), required_file, f"Required wiki file is missing: {required_file}."))
    if not (wiki_root / assets).is_dir():
        problems.append(issue("topology.required-assets", severity(contract, "topology"), assets, "Required assets directory is missing."))
    for item in sorted(wiki_root.iterdir(), key=lambda value: value.name):
        if item.is_dir() and item.name not in trunks and item.name != assets:
            problems.append(issue("topology.unknown-directory", severity(contract, "topology"), item.name, "Top-level directory is not declared by the contract."))
        reserved_files = {navigation["root_index"], navigation["context_file"], "wiki-structure.yaml"}
        if "authoring_file" in navigation:
            reserved_files.add(navigation["authoring_file"])
        if "intent_map" in navigation:
            reserved_files.add(navigation["intent_map"])
        if item.is_file() and item.name not in reserved_files:
            problems.append(issue("topology.root-file", severity(contract, "topology"), item.name, "File is not allowed at the wiki root."))
        if item.name not in reserved_files and not name_pattern.fullmatch(item.stem if item.is_file() else item.name):
            problems.append(issue("topology.name", severity(contract, "topology"), item.name, "Path name does not match the configured pattern."))
    for trunk_name in sorted(trunks):
        trunk = wiki_root / trunk_name
        if not trunk.is_dir():
            continue
        directories = [trunk, *(item for item in trunk.rglob("*") if item.is_dir())]
        for directory in sorted(directories, key=lambda value: relative(value, wiki_root)):
            depth = len(directory.relative_to(wiki_root).parts)
            if depth > topology["max_depth"]:
                problems.append(issue("topology.depth", severity(contract, "topology"), relative(directory, wiki_root), f"Trunk exceeds configured maximum depth {topology['max_depth']}."))
                continue
            index = directory / navigation["trunk_index"]
            if not index.is_file():
                problems.append(issue("topology.trunk-index", severity(contract, "topology"), relative(index, wiki_root), "Directory index is missing."))
        for item in trunk.rglob("*"):
            if item.is_file() and item.suffix not in {".md", *(f".{extension}" for extension in contract["diagrams"]["required_extensions"])}:
                problems.append(issue("topology.unknown-file", severity(contract, "topology"), relative(item, wiki_root), "File extension is not allowed inside a trunk."))
            if item.name != navigation["trunk_index"] and not name_pattern.fullmatch(item.stem if item.is_file() else item.name):
                problems.append(issue("topology.name", severity(contract, "topology"), relative(item, wiki_root), "Path name does not match the configured pattern."))
    return problems


def internal_markdown_targets(index: Path, wiki_root: Path) -> list[tuple[Path, int]]:
    targets: list[tuple[Path, int]] = []
    for target, line, image in markdown_links(index.read_text(encoding="utf-8")):
        parsed = urlsplit(target)
        if image or parsed.scheme or parsed.netloc or not parsed.path:
            continue
        resolved = local_target(index, wiki_root, target)
        if resolved is not None and resolved != Path() and resolved.suffix == ".md":
            targets.append((resolved, line))
    return targets


def validate_navigation(wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    navigation = contract["navigation"]
    trunks = [wiki_root / name for name in contract["topology"]["trunks"] if (wiki_root / name).is_dir()]
    root_index = wiki_root / navigation["root_index"]
    problems: list[Diagnostic] = []
    if root_index.is_file():
        targets = internal_markdown_targets(root_index, wiki_root)
        allowed = {wiki_root / navigation["context_file"]} | {trunk / navigation["trunk_index"] for trunk in trunks}
        if "authoring_file" in navigation:
            allowed.add(wiki_root / navigation["authoring_file"])
        if "intent_map" in navigation:
            allowed.add(wiki_root / navigation["intent_map"])
        for target, line in targets:
            if target not in allowed:
                problems.append(issue("navigation.root-target", severity(contract, "navigation"), navigation["root_index"], "Root index may link only to configured root references and trunk indexes.", line))
        for target in sorted(allowed, key=lambda value: relative(value, wiki_root)):
            count = sum(item == target for item, _ in targets)
            if count != 1:
                problems.append(issue("navigation.root-count", severity(contract, "navigation"), navigation["root_index"], f"Root index must link exactly once to {relative(target, wiki_root)}; found {count}."))
    for trunk in trunks:
        directories = [trunk, *(path for path in trunk.rglob("*") if path.is_dir())]
        for directory in directories:
            if len(directory.relative_to(wiki_root).parts) > contract["topology"]["max_depth"]:
                continue
            index = directory / navigation["trunk_index"]
            if not index.is_file():
                continue
            targets = internal_markdown_targets(index, wiki_root)
            pages = {path for path in directory.glob("*.md") if path != index}
            child_indexes = {path / navigation["trunk_index"] for path in directory.iterdir() if path.is_dir()}
            allowed = pages | child_indexes
            for target, line in targets:
                if target not in allowed:
                    problems.append(issue("navigation.trunk-target", severity(contract, "navigation"), relative(index, wiki_root), "Directory index may link only to immediate pages or child indexes.", line))
            for page in sorted(allowed, key=lambda value: relative(value, wiki_root)):
                count = sum(item == page for item, _ in targets)
                if count != 1:
                    problems.append(issue("navigation.trunk-count", severity(contract, "navigation"), relative(index, wiki_root), f"Directory index must link exactly once to {relative(page, wiki_root)}; found {count}."))
    return problems


def validate_intent_map(wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    """Validate navigation form and canonical destinations, never editorial meaning."""
    name = contract["navigation"].get("intent_map")
    if name is None or not (wiki_root / name).is_file():
        return []  # Topology reports a declared but missing map.
    path = wiki_root / name
    text = path.read_text(encoding="utf-8")
    rule = severity(contract, "navigation")
    problems: list[Diagnostic] = []

    def report(code: str, message: str, line: int | None = None) -> None:
        problems.append(issue(f"intent-map.{code}", rule, name, message, line))

    if text.splitlines() and text.splitlines()[0].strip() == contract["frontmatter"]["marker"]:
        report("frontmatter", "The intent map must not contain frontmatter or an operational page role.", 1)
        return problems
    tokens = MarkdownIt().parse(text)
    h1_lines, _, _ = heading_data(text, 0)
    if len(h1_lines) != 1:
        report("title", "The intent map must contain exactly one H1 title.")
    route_line: int | None = None
    destinations: set[Path] = set()
    entries = 0
    routes = 0
    index = 0
    while index < len(tokens):
        token = tokens[index]
        line = token.map[0] + 1 if token.map else None
        if token.type == "heading_open" and token.level == 0 and token.tag in {"h1", "h2"}:
            title = tokens[index + 1].content.strip()
            if token.tag == "h1":
                if routes or index != 0 or not title:
                    report("title", "Use a nonempty H1 title before the introduction and routes.", line)
            else:
                if route_line is not None and entries == 0:
                    report("destinations", "Each intent must have at least one destination with guidance.", route_line)
                if not title:
                    report("intent", "Each H2 must express a nonempty intent.", line)
                routes += 1
                route_line, entries, destinations = line, 0, set()
            index += 3
            continue
        if token.type == "paragraph_open" and token.level == 0 and not routes:
            index += 3  # Optional human-readable coverage introduction.
            continue
        if token.type == "bullet_list_open" and token.level == 0 and route_line is not None:
            index += 1
            while index < len(tokens) and tokens[index].type != "bullet_list_close":
                item = tokens[index]
                item_line = item.map[0] + 1 if item.map else line
                end = index + 1
                while end < len(tokens) and not (tokens[end].type == "list_item_close" and tokens[end].level == item.level):
                    end += 1
                record = tokens[index:end + 1]
                if [part.type for part in record] != ["list_item_open", "paragraph_open", "inline", "paragraph_close", "list_item_close"]:
                    report("entry", "Use a direct bullet item: [Canonical title](relative.md) - Guidance.", item_line)
                else:
                    inline = record[2]
                    match = re.fullmatch(r"\[([^\]\n]+)\]\(([^\s)]+)\) - (\S[\s\S]*)", inline.content.strip())
                    children = inline.children or []
                    if not match or sum(child.type == "link_open" for child in children) != 1 or any(child.type == "image" for child in children):
                        report("entry", "Each destination needs one canonical link followed by ' - ' and nonempty guidance.", item_line)
                    else:
                        entries += 1
                        label, target, _ = match.groups()
                        parsed = urlsplit(target)
                        destination = local_target(path, wiki_root, target)
                        if parsed.scheme or parsed.netloc or parsed.query or not parsed.path or Path(unquote(parsed.path)).is_absolute() or destination in {None, Path()} or destination.suffix != ".md" or not destination.is_file():
                            report("destination", "Destination must be an existing relative canonical Markdown page or index inside the wiki.", item_line)
                        else:
                            rel = destination.relative_to(wiki_root.resolve())
                            navigation = contract["navigation"]
                            in_trunk = len(rel.parts) > 1 and rel.parts[0] in contract["topology"]["trunks"]
                            is_index = rel.as_posix() == navigation["root_index"] or (in_trunk and destination.name == navigation["trunk_index"])
                            frontmatter, body, _, failure = split_page(destination, contract["frontmatter"]["marker"])
                            roles = page_roles(frontmatter or {}, contract)
                            is_content = (
                                in_trunk
                                and rel.parts[0] != contract["topology"]["sources_trunk"]
                                and contract["provenance"]["source_role"] not in roles
                                and bool(roles & set(contract["provenance"]["content_roles"]))
                            )
                            if failure or not (is_index or is_content):
                                report("destination", "Destination is not a canonical operational page or index; auxiliary, source, configuration, and governance material are excluded.", item_line)
                            elif h1_title(body) != label:
                                report("label", "Destination label must exactly match its canonical H1 title.", item_line)
                            if destination in destinations:
                                report("duplicate", "A destination may repeat between intents, but not within one intent (including different fragments).", item_line)
                            destinations.add(destination)
                index = end + 1
            index += 1
            continue
        report("structure", "Use an H1, optional introduction, and H2 intents containing direct destination bullet items.", line)
        # Skip a whole unsupported block; nested headings are not real routes.
        if token.nesting == 1:
            index += 1
            while index < len(tokens) and not (tokens[index].nesting == -1 and tokens[index].level == token.level):
                index += 1
        index += 1
    if not routes:
        report("intent", "The intent map must contain at least one H2 intent.")
    elif entries == 0:
        report("destinations", "Each intent must have at least one destination with guidance.", route_line)
    return problems


def validate_assets_and_diagrams(wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    """Validate configured visual assets and complete diagram sets by shared stem."""
    topology = contract["topology"]
    assets_root = wiki_root / topology["assets_directory"]
    name_pattern = re.compile(contract["naming"]["pattern"])
    allowed_extensions = {f".{extension.lower()}" for extension in contract["assets"]["allowed_extensions"]}
    asset_rule = severity(contract, "assets")
    problems: list[Diagnostic] = []
    referenced_assets: set[Path] = set()

    for path in sorted((candidate for candidate in wiki_root.rglob("*.md") if candidate.is_file()), key=lambda candidate: relative(candidate, wiki_root)):
        _, body, offset, parse_issue = split_page(path, contract["frontmatter"]["marker"])
        if parse_issue:
            continue
        for target, _, image in markdown_links(body, offset):
            if not image:
                continue
            destination = local_target(path, wiki_root, target)
            if destination not in {None, Path()} and assets_root.resolve() in destination.resolve().parents:
                referenced_assets.add(destination.resolve())

    if assets_root.is_dir():
        for item in sorted(assets_root.rglob("*"), key=lambda candidate: relative(candidate, wiki_root)):
            rel = relative(item, wiki_root)
            if item.is_dir():
                if not contract["assets"]["allow_subdirectories"]:
                    problems.append(issue("assets.subdirectory", asset_rule, rel, "Asset subdirectories are not allowed."))
                if not name_pattern.fullmatch(item.name):
                    problems.append(issue("topology.name", severity(contract, "topology"), rel, "Path name does not match the configured pattern."))
                continue
            if item.name in contract["assets"]["forbidden_files"]:
                problems.append(issue("assets.forbidden", asset_rule, rel, "Asset file is forbidden by the contract."))
            if item.suffix.lower() not in allowed_extensions:
                problems.append(issue("assets.extension", asset_rule, rel, "Asset file extension is not allowed."))
            if not name_pattern.fullmatch(item.stem):
                problems.append(issue("topology.name", severity(contract, "topology"), rel, "Path name does not match the configured pattern."))
            if item.resolve() not in referenced_assets:
                problems.append(issue("assets.orphan", asset_rule, rel, "Visual asset is not referenced by a Markdown page."))

    diagram_config = contract["diagrams"]
    diagram_extensions = {f".{extension}" for extension in diagram_config["required_extensions"]}
    required_extensions = diagram_extensions
    source_extension = f".{diagram_config['source_extension']}"
    visualization_extension = f".{diagram_config['visualization_extension']}"
    diagram_rule = severity(contract, "diagrams")
    diagram_roles = set(diagram_config["applies_to_roles"])
    components: dict[Path, set[str]] = {}
    for trunk_name in topology["trunks"]:
        trunk = wiki_root / trunk_name
        if not trunk.is_dir():
            continue
        for item in trunk.rglob("*"):
            if item.is_file() and item.suffix in diagram_extensions - {".md"}:
                components.setdefault(item.with_suffix(""), set()).add(item.suffix)
    for markdown in sorted(wiki_root.rglob("*.md"), key=lambda candidate: relative(candidate, wiki_root)):
        if relative(markdown, wiki_root) == contract["navigation"].get("intent_map"):
            continue
        frontmatter, _, _, parse_issue = split_page(markdown, contract["frontmatter"]["marker"])
        if not parse_issue and frontmatter and page_roles(frontmatter, contract) & diagram_roles:
            components.setdefault(markdown.with_suffix(""), set()).add(".md")
    for stem, found in sorted(components.items(), key=lambda pair: relative(pair[0], wiki_root)):
        markdown = stem.with_suffix(".md")
        if markdown.is_file():
            found.add(".md")
        missing = required_extensions - found
        if not markdown.is_file():
            problems.append(issue("diagrams.markdown", diagram_rule, relative(stem, wiki_root), "Diagram source must have a Markdown page with the same stem."))
            continue
        frontmatter, body, offset, parse_issue = split_page(markdown, contract["frontmatter"]["marker"])
        if parse_issue or not frontmatter or not page_roles(frontmatter, contract) & diagram_roles:
            problems.append(issue("diagrams.application", diagram_rule, relative(markdown, wiki_root), "Diagram source is not attached to a page with an applicable role."))
            continue
        if missing:
            problems.append(issue("diagrams.incomplete", diagram_rule, relative(stem, wiki_root), f"Diagram set is incomplete; missing: {', '.join(sorted(missing))}."))
            continue
        visualization = stem.with_suffix(visualization_extension)
        visualizations = [target for target, _, image in markdown_links(body, offset) if image and local_target(markdown, wiki_root, target) == visualization.resolve()]
        if len(visualizations) != 1:
            problems.append(issue("diagrams.visualization", diagram_rule, relative(markdown, wiki_root), "Diagram Markdown must embed its visualization exactly once."))
        if any(local_target(markdown, wiki_root, target) == stem.with_suffix(source_extension).resolve() for target, _, _ in markdown_links(body, offset)):
            problems.append(issue("diagrams.source-embedded", diagram_rule, relative(markdown, wiki_root), "Diagram Markdown must not embed its source file."))
    return problems


def section_occurrences(body: str, offset: int) -> list[tuple[str, tuple[int, int, str]]]:
    tokens = MarkdownIt().parse(body)
    headings: list[tuple[str, int, int]] = []
    for index, token in enumerate(tokens):
        if token.type != "heading_open" or not token.map:
            continue
        title = tokens[index + 1].content if index + 1 < len(tokens) and tokens[index + 1].type == "inline" else ""
        headings.append((title, token.map[0], token.map[1]))
    lines = body.splitlines()
    result: list[tuple[str, tuple[int, int, str]]] = []
    for index, (title, start, content_start) in enumerate(headings):
        end = headings[index + 1][1] if index + 1 < len(headings) else len(lines)
        result.append((title, (start + offset + 1, end + offset + 1, "\n".join(lines[content_start:end]))))
    return result


def page_sections(body: str, offset: int) -> dict[str, tuple[int, int, str]]:
    return {title: section for title, section in section_occurrences(body, offset)}


def section_links(path: Path, wiki_root: Path, section: tuple[int, int, str] | None) -> set[Path]:
    if section is None:
        return set()
    result: set[Path] = set()
    for target, _, image in markdown_links(section[2]):
        if image:
            continue
        destination = local_target(path, wiki_root, target)
        if destination not in {None, Path()} and destination.suffix == ".md" and destination.is_file():
            result.add(destination.resolve())
    return result


def source_record(section: tuple[int, int, str]) -> dict[str, str]:
    record: dict[str, str] = {}
    for line in section[2].splitlines():
        match = re.match(r"\s*-\s+\*\*(.+?):\*\*\s*(.*?)\s*$", line)
        if match:
            record[match.group(1)] = match.group(2).rstrip(".").strip()
    return record


def page_roles(frontmatter: dict[str, Any], contract: dict[str, Any]) -> set[str]:
    config = contract["page_types"].get(frontmatter.get("type"), {})
    return set(config.get("roles", [])) if isinstance(config, dict) else set()


def structured_pages(
    wiki_root: Path, contract: dict[str, Any]
) -> dict[Path, tuple[Path, dict[str, Any], str, int, dict[str, tuple[int, int, str]]]]:
    pages = {}
    exceptions = set(contract["frontmatter"]["exceptions"])
    for path in sorted(wiki_root.rglob("*.md"), key=lambda item: relative(item, wiki_root)):
        if path.name in exceptions or relative(path, wiki_root) == contract["navigation"].get("intent_map"):
            continue
        frontmatter, body, offset, parse_issue = split_page(path, contract["frontmatter"]["marker"])
        if parse_issue or not frontmatter or frontmatter.get("type") not in contract["page_types"]:
            continue
        pages[path.resolve()] = (path, frontmatter, body, offset, page_sections(body, offset))
    return pages


def validate_provenance(wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    config = contract["provenance"]
    sections = contract["sections"]
    pages = structured_pages(wiki_root, contract)
    source_role = config["source_role"]
    content_roles = set(config["content_roles"])
    source_pages = {key: value for key, value in pages.items() if source_role in page_roles(value[1], contract)}
    content_pages = {key: value for key, value in pages.items() if page_roles(value[1], contract) & content_roles}
    source_root = (wiki_root / contract["topology"]["sources_trunk"]).resolve()
    rule = severity(contract, "provenance")
    problems: list[Diagnostic] = []

    for resolved, (path, frontmatter, _, _, found_sections) in source_pages.items():
        rel = relative(path, wiki_root)
        if source_root not in resolved.parents:
            problems.append(issue("provenance.source-location", rule, rel, f"Source-role pages must be inside {contract['topology']['sources_trunk']}/."))
        record_section = found_sections.get(sections["source_record"])
        if record_section is None:
            problems.append(issue("provenance.record", rule, rel, f"Required source record section is missing: {sections['source_record']}."))
        else:
            record = source_record(record_section)
            for label in sorted(set(config["record_fields"]) - set(record)):
                problems.append(issue("provenance.record", rule, rel, f"Source record field is missing: {label}.", record_section[0]))
            publication = config["publication_date_field"]
            if publication in record and record[publication] != config["publication_unknown"] and not iso_date(record[publication]):
                problems.append(issue("provenance.record", rule, rel, f"Source record field {publication!r} must be an ISO date or the configured unknown value.", record_section[0]))
            for label in config["date_fields"]:
                if label in record and not iso_date(record[label]):
                    problems.append(issue("provenance.record", rule, rel, f"Source record field {label!r} must be a real ISO date.", record_section[0]))
            indexed = frontmatter.get(config["indexed_field"])
            indexed_record = record.get(config["indexed_record_field"])
            if indexed_record is not None and iso_date(indexed) and str(indexed) != indexed_record:
                problems.append(issue("provenance.record", rule, rel, f"Source record field {config['indexed_record_field']!r} must match frontmatter field {config['indexed_field']!r}.", record_section[0]))

        grounded = found_sections.get(sections["grounded_pages"])
        links = section_links(path, wiki_root, grounded)
        if frontmatter.get("state") in config["no_content_states"]:
            if grounded is None or grounded[2].strip() != sections["no_content"]:
                problems.append(issue("provenance.grounded", rule, rel, f"A no-content source must contain exactly {sections['no_content']!r} in {sections['grounded_pages']!r}.", grounded[0] if grounded else None))
            if links:
                problems.append(issue("provenance.grounded", rule, rel, "A no-content source cannot link to grounded content pages.", grounded[0] if grounded else None))
            continue
        if grounded is None:
            problems.append(issue("provenance.grounded", rule, rel, f"Required grounded-pages section is missing: {sections['grounded_pages']}."))
            continue
        invalid = links - content_pages.keys()
        if invalid:
            problems.append(issue("provenance.grounded", rule, rel, "The grounded-pages section may link only to pages with a configured content role.", grounded[0]))
        expected = links & content_pages.keys()
        backlinks = {
            page
            for page, (content_path, _, _, _, content_sections) in content_pages.items()
            if resolved in section_links(content_path, wiki_root, content_sections.get(sections["content_sources"]))
        }
        if expected != backlinks:
            problems.append(issue("provenance.backlinks", rule, rel, "Grounded-page links and content-page source backlinks must be identical.", grounded[0]))

    for resolved, (path, _, _, _, found_sections) in content_pages.items():
        if source_root in resolved.parents:
            problems.append(issue("provenance.source-location", rule, relative(path, wiki_root), "The sources trunk may contain only source-role pages."))
        source_section = found_sections.get(sections["content_sources"])
        for linked in section_links(path, wiki_root, source_section):
            if linked not in source_pages:
                problems.append(issue("provenance.sources", rule, relative(path, wiki_root), "The configured content-sources section may link only to source-role pages.", source_section[0] if source_section else None))
                continue
            grounded = source_pages[linked][4].get(sections["grounded_pages"])
            if resolved not in section_links(source_pages[linked][0], wiki_root, grounded):
                problems.append(issue("provenance.backlinks", rule, relative(path, wiki_root), "Source page does not contain the matching grounded-page backlink.", source_section[0] if source_section else None))
    return problems


def validate_contextual_citations(wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    config = contract["provenance"]
    labels = contract["sections"]
    pages = structured_pages(wiki_root, contract)
    sources = {key for key, value in pages.items() if config["source_role"] in page_roles(value[1], contract)}
    problems: list[Diagnostic] = []
    rule = severity(contract, "contextual_citation")
    for resolved, (path, frontmatter, body, offset, sections) in pages.items():
        if resolved in sources or not page_roles(frontmatter, contract) & set(config["content_roles"]):
            continue
        source_section = sections.get(labels["content_sources"])
        listed = section_links(path, wiki_root, source_section) & sources
        grounded = sections.get(labels["grounded_pages"])
        for target, line, image in markdown_links(body, offset):
            if image or (source_section and source_section[0] <= line < source_section[1]) or (grounded and grounded[0] <= line < grounded[1]):
                continue
            destination = local_target(path, wiki_root, target)
            if destination in {None, Path()} or destination.resolve() not in sources or destination.resolve() in listed:
                continue
            problems.append(issue("contextual-citation.missing", rule, relative(path, wiki_root), f"Contextual source citation is not listed in {labels['content_sources']!r}: {relative(destination.resolve(), wiki_root)}.", line))
    return problems


def direct_list_items(section: tuple[int, int, str]) -> tuple[list[Any], bool]:
    tokens = MarkdownIt().parse(section[2])
    containers = {"bullet_list_open", "bullet_list_close", "ordered_list_open", "ordered_list_close"}
    items = [token for token in tokens if token.type == "list_item_open" and token.level == 1 and token.map]
    extra = any(
        (token.type in containers and token.level != 0)
        or (token.type == "list_item_open" and token.level != 1)
        or (token.level == 0 and token.type not in containers)
        for token in tokens
    )
    return items, extra


HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FIELD = re.compile(r"^\s*-\s+\*\*(.+?):\*\*\s*(.*?)\s*$")
NESTED_ITEM = re.compile(r"^\s{2,}[-+*]\s+(.+?)\s*$")
PAGE_VALUE = re.compile(r"^\[([^\]]+)]\(([^)\s]+)\)$")


def structured_records(body: str, offset: int, section_name: str) -> tuple[list[tuple[str, int, list[tuple[str, str, list[tuple[str, int]], int]]]], list[tuple[int, str]]]:
    """Return immediate heading records and grammar failures for one named section."""
    lines = body.splitlines()
    headings = [(index, len(match.group(1)), match.group(2).strip()) for index, line in enumerate(lines) if (match := HEADING.match(line))]
    records: list[tuple[str, int, list[tuple[str, str, list[tuple[str, int]], int]]]] = []
    failures: list[tuple[int, str]] = []
    matches = [(line, level) for line, level, title in headings if title == section_name]
    if len(matches) > 1:
        return [], [(matches[1][0] + offset + 1, "Structured section must not be repeated.")]
    for position, (start, level, title) in enumerate(headings):
        if title != section_name:
            continue
        end = next((line for line, next_level, _ in headings[position + 1 :] if next_level <= level), len(lines))
        children = [(line, child_title) for line, child_level, child_title in headings[position + 1 :] if line < end and child_level == level + 1]
        if not children:
            failures.append((start + offset + 1, "Structured section must contain immediate heading records."))
            continue
        child_starts = {line for line, _ in children}
        for line in range(start + 1, end):
            if not lines[line].strip() or line in child_starts or any(child_start < line for child_start in child_starts):
                continue
            if HEADING.match(lines[line]):
                failures.append((line + offset + 1, "Structured section may contain only immediate heading records."))
                break
            failures.append((line + offset + 1, "Structured section may not contain content outside records."))
            break
        for child_index, (record_start, record_name) in enumerate(children):
            record_end = children[child_index + 1][0] if child_index + 1 < len(children) else end
            fields: list[tuple[str, str, list[tuple[str, int]], int]] = []
            current: tuple[str, str, list[tuple[str, int]], int] | None = None
            for line in range(record_start + 1, record_end):
                content = lines[line]
                if not content.strip():
                    continue
                field = FIELD.match(content)
                if field:
                    current = (field.group(1), field.group(2), [], line + offset + 1)
                    fields.append(current)
                    continue
                item = NESTED_ITEM.match(content)
                if item and current is not None and not current[1]:
                    current[2].append((item.group(1), line + offset + 1))
                    continue
                failures.append((line + offset + 1, "Structured record must contain only declared field items and nested value items."))
            records.append((record_name, record_start + offset + 1, fields))
    return records, failures


def h1_title(body: str) -> str | None:
    tokens = MarkdownIt().parse(body)
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag == "h1":
            return tokens[index + 1].content if index + 1 < len(tokens) and tokens[index + 1].type == "inline" else None
    return None


def validate_structured_sections(wiki_root: Path, contract: dict[str, Any]) -> list[Diagnostic]:
    collections = contract.get("structured_sections", [])
    if not collections:
        return []
    rule_severity = severity(contract, "structured_sections")
    problems: list[Diagnostic] = []
    for path in sorted(wiki_root.rglob("*.md"), key=lambda item: relative(item, wiki_root)):
        if relative(path, wiki_root) == contract["navigation"].get("intent_map"):
            continue
        frontmatter, body, offset, parse_issue = split_page(path, contract["frontmatter"]["marker"])
        if parse_issue or not frontmatter or frontmatter.get("type") not in contract["page_types"]:
            continue
        rel = relative(path, wiki_root)
        for collection in collections:
            if frontmatter["type"] not in collection["page_types"]:
                continue
            records, failures = structured_records(body, offset, collection["section"])
            if not records and not failures:
                problems.append(issue("structured.section", rule_severity, rel, f"Structured section is missing: {collection['section']}."))
                continue
            for line, message in failures:
                problems.append(issue("structured.syntax", rule_severity, rel, message, line))
            if len(records) < collection["min_records"] or (collection["max_records"] is not None and len(records) > collection["max_records"]):
                problems.append(issue("structured.cardinality", rule_severity, rel, f"Structured section {collection['section']!r} has {len(records)} records outside its configured cardinality."))
            fields_by_name = {field["name"]: field for field in collection["fields"]}
            for _, record_line, fields in records:
                seen: dict[str, list[tuple[str, int]]] = {}
                for name, scalar, nested, field_line in fields:
                    if name not in fields_by_name:
                        problems.append(issue("structured.field", rule_severity, rel, f"Unknown structured field: {name}.", field_line))
                        continue
                    if name in seen:
                        problems.append(issue("structured.field", rule_severity, rel, f"Structured field is repeated: {name}.", field_line))
                        continue
                    if scalar and nested:
                        problems.append(issue("structured.syntax", rule_severity, rel, f"Structured field {name!r} cannot combine a scalar and nested values.", field_line))
                    seen[name] = [(scalar, field_line)] if scalar else nested
                page_targets: dict[str, set[Path]] = {}
                for name, config in fields_by_name.items():
                    values = seen.get(name, [])
                    if not values and (config["min_items"] > 0 or "empty_value" in config):
                        problems.append(issue("structured.field", rule_severity, rel, f"Required structured field is missing: {name}.", record_line))
                        continue
                    empty = config.get("empty_value")
                    if empty is not None and len(values) == 1 and values[0][0] == empty:
                        continue
                    if empty is not None and any(value == empty for value, _ in values):
                        problems.append(issue("structured.empty", rule_severity, rel, f"Empty value for {name!r} must be its only scalar value.", values[0][1]))
                        continue
                    if len(values) < config["min_items"] or (config["max_items"] is not None and len(values) > config["max_items"]):
                        problems.append(issue("structured.cardinality", rule_severity, rel, f"Structured field {name!r} has {len(values)} values outside its configured cardinality.", record_line))
                    for value, line in values:
                        page = PAGE_VALUE.fullmatch(value)
                        if page:
                            target = local_target(path, wiki_root, page.group(2))
                            if target is None or target == Path() or target.suffix != ".md" or not target.is_file() or urlsplit(page.group(2)).fragment:
                                problems.append(issue("structured.page", rule_severity, rel, f"Page value for {name!r} must link to an existing local Markdown page.", line))
                                continue
                            _, target_body, _, target_issue = split_page(target, contract["frontmatter"]["marker"])
                            if target_issue or page.group(1) != h1_title(target_body):
                                problems.append(issue("structured.page", rule_severity, rel, f"Page value label for {name!r} must match the destination H1.", line))
                                continue
                            page_targets.setdefault(name, set()).add(target.resolve())
                        elif "text" not in config["value_types"]:
                            problems.append(issue("structured.value", rule_severity, rel, f"Structured field {name!r} requires page values.", line))
                        elif not value.strip():
                            problems.append(issue("structured.value", rule_severity, rel, f"Structured field {name!r} has an empty text value.", line))
                    if "page" not in config["value_types"] and any(PAGE_VALUE.fullmatch(value) for value, _ in values):
                        problems.append(issue("structured.value", rule_severity, rel, f"Structured field {name!r} does not accept page values.", record_line))
                for name, config in fields_by_name.items():
                    for other in config.get("disjoint_with", []):
                        overlap = page_targets.get(name, set()) & page_targets.get(other, set())
                        if overlap:
                            problems.append(issue("structured.disjoint", rule_severity, rel, f"Structured fields {name!r} and {other!r} share a page value.", record_line))
    return problems


def tracking_ticket_id(content: str, pattern: str) -> str | None:
    candidates = [value for value in re.findall(r"\[([^\]\r\n]*)\]", content) if re.fullmatch(pattern, value)]
    if len(candidates) != 1 or re.fullmatch(rf"\[{re.escape(candidates[0])}\]\s+\S.*", content) is None:
        return None
    return candidates[0]


def run_knot(arguments: list[str], repository_root: Path) -> tuple[Any | None, str | None, str | None]:
    try:
        result = subprocess.run(["knot", *arguments, "--json"], cwd=repository_root, text=True, capture_output=True, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, "runtime", f"Knot CLI failed: {exc}"
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None, "runtime", f"Knot CLI returned invalid JSON: {result.stderr.strip() or result.stdout.strip() or 'empty output'}"
    error = payload.get("error", {}) if isinstance(payload, dict) else {}
    if result.returncode != 0 or not isinstance(payload, dict) or payload.get("ok") is not True:
        code = error.get("code") if isinstance(error, dict) else None
        detail = error.get("message") if isinstance(error, dict) else None
        kind = "association" if code in {"not_found", "ambiguous_id"} else "runtime"
        return None, kind, detail or result.stderr.strip() or "Knot CLI rejected the request."
    return payload.get("data"), None, None


def knot_ticket(ticket_id: str, repository_root: Path, cache: dict[str, tuple[str | None, set[str], str | None, str | None]]) -> tuple[str | None, set[str], str | None, str | None]:
    if ticket_id in cache:
        return cache[ticket_id]
    data, kind, message = run_knot(["show", ticket_id], repository_root)
    if kind:
        result = (None, set(), kind, message)
    elif not isinstance(data, dict) or not isinstance(data.get("status"), str) or not isinstance(data.get("tags"), list) or not all(isinstance(tag, str) for tag in data["tags"]):
        result = (None, set(), "runtime", "Knot CLI returned a ticket without a valid status and tag list.")
    else:
        result = (data["status"], set(data["tags"]), None, None)
    cache[ticket_id] = result
    return result


def knot_tagged_tickets(tag: str, repository_root: Path) -> tuple[list[str], str | None]:
    ticket_ids: list[str] = []
    for command in ("list", "closed"):
        data, kind, message = run_knot([command, "--tag", tag], repository_root)
        if kind:
            return [], f"Knot CLI failed while listing tagged tickets: {message}"
        if not isinstance(data, list) or any(not isinstance(item, dict) or not isinstance(item.get("id"), str) for item in data):
            return [], "Knot CLI returned an invalid ticket list."
        ticket_ids.extend(item["id"] for item in data)
    return list(dict.fromkeys(ticket_ids)), None


def validate_tracking_ticket(ticket_id: str, tracking: dict[str, Any], kind: str, path: str, line: int | None, contract: dict[str, Any], repository_root: Path, cache: dict[str, tuple[str | None, set[str], str | None, str | None]]) -> list[Diagnostic]:
    association_code = f"{kind}.association"
    if re.fullmatch(tracking["id_pattern"], ticket_id) is None:
        return [issue(association_code, severity(contract, f"{kind}_association"), path, f"Invalid configured Knot ticket ID: {ticket_id}.", line)]
    status, tags, failure, message = knot_ticket(ticket_id, repository_root, cache)
    if failure == "runtime":
        return [issue("runtime.knot", "error", path, f"Knot CLI failed: {message}", line)]
    if failure:
        return [issue(association_code, severity(contract, f"{kind}_association"), path, f"Knot ticket could not be resolved: {message}", line)]
    if tracking["tag"] not in tags:
        return [issue(association_code, severity(contract, f"{kind}_association"), path, f"Knot ticket {ticket_id} does not have configured tag {tracking['tag']!r}.", line)]
    if status in tracking["valid_statuses"]:
        return []
    if status in tracking["warning_statuses"]:
        return [issue(f"{kind}.status", severity(contract, f"{kind}_status"), path, f"Knot ticket {ticket_id} is in historical terminal status {status!r}.", line)]
    return [issue(association_code, severity(contract, f"{kind}_association"), path, f"Knot ticket {ticket_id} has disallowed status {status!r}.", line)]


def validate_tracking(wiki_root: Path, contract: dict[str, Any], repository_root: Path, kind: str) -> list[Diagnostic]:
    tracking = contract[f"{kind}_tracking"]
    pages = structured_pages(wiki_root, contract)
    citations: dict[str, tuple[str, int | None]] = {}
    cache: dict[str, tuple[str | None, set[str], str | None, str | None]] = {}
    validated_tickets: set[str] = set()
    terminal_warning_ids: set[str] = set()
    problems: list[Diagnostic] = []
    location_code = f"{kind}.location"
    association_code = f"{kind}.association"
    location_rule = f"{kind}_location"
    association_rule = f"{kind}_association"

    for _, (path, frontmatter, body, offset, _) in pages.items():
        if not page_roles(frontmatter, contract) & set(tracking["roles"]):
            continue
        rel = relative(path, wiki_root)
        matching = [section for title, section in section_occurrences(body, offset) if title == tracking["section"]]
        if len(matching) > 1:
            problems.append(issue(location_code, severity(contract, location_rule), rel, f"Tracking section {tracking['section']!r} must not be repeated.", matching[1][0]))
        for section in matching:
            items, extra = direct_list_items(section)
            if not items or extra:
                problems.append(issue(location_code, severity(contract, location_rule), rel, f"Tracking section {tracking['section']!r} must contain only non-empty direct list items.", section[0]))
                continue
            lines = section[2].splitlines()
            for item in items:
                first_line = lines[item.map[0]] if item.map and item.map[0] < len(lines) else ""
                match = re.match(r"^\s*(?:[-+*]|\d+[.)])(?:\s+(.*))?$", first_line)
                content = ((match.group(1) if match else "") or "").strip()
                line = section[0] + item.map[0] + 1
                ticket_id = tracking_ticket_id(content, tracking["id_pattern"]) if content else None
                if ticket_id is None:
                    problems.append(issue(association_code, severity(contract, association_rule), rel, "Tracking item must use `[complete configured Knot ID] Title`.", line))
                    continue
                citations[ticket_id] = (rel, line)
                if ticket_id not in validated_tickets:
                    ticket_problems = validate_tracking_ticket(ticket_id, tracking, kind, rel, line, contract, repository_root, cache)
                    problems.extend(ticket_problems)
                    validated_tickets.add(ticket_id)
                    if any(problem.code == f"{kind}.status" for problem in ticket_problems):
                        terminal_warning_ids.add(ticket_id)

        if kind != "proposal":
            continue
        field = tracking["frontmatter_field"]
        state = tracking["proposal_state"]
        frontmatter_lines = path.read_text(encoding="utf-8").splitlines()[1:]
        closing = next((index for index, value in enumerate(frontmatter_lines) if value.strip() == contract["frontmatter"]["marker"]), len(frontmatter_lines))
        occurrences = sum(bool(re.match(rf"^\s*{re.escape(field)}\s*:", value)) for value in frontmatter_lines[:closing])
        if occurrences > 1:
            problems.append(issue(association_code, severity(contract, association_rule), rel, f"Frontmatter must contain exactly one {field!r} field.", 1))
        elif frontmatter.get("state") == state:
            value = frontmatter.get(field)
            if not isinstance(value, str) or not value.strip():
                problems.append(issue(association_code, severity(contract, association_rule), rel, f"A page in state {state!r} must contain exactly one {field!r} field.", 1))
            else:
                ticket_id = value.strip()
                citations[ticket_id] = (rel, 1)
                if ticket_id not in validated_tickets:
                    ticket_problems = validate_tracking_ticket(ticket_id, tracking, kind, rel, 1, contract, repository_root, cache)
                    problems.extend(ticket_problems)
                    validated_tickets.add(ticket_id)
                    if any(problem.code == f"{kind}.status" for problem in ticket_problems):
                        terminal_warning_ids.add(ticket_id)
        elif field in frontmatter:
            problems.append(issue(location_code, severity(contract, location_rule), rel, f"Frontmatter field {field!r} is allowed only in state {state!r}.", 1))

    ticket_ids, list_error = knot_tagged_tickets(tracking["tag"], repository_root)
    if list_error:
        problems.append(issue("runtime.knot", "error", "wiki", list_error))
        return problems
    for ticket_id in ticket_ids:
        status, _, failure, message = knot_ticket(ticket_id, repository_root, cache)
        if failure:
            code = "runtime.knot" if failure == "runtime" else f"{kind}.inverse"
            problems.append(issue(code, "error" if failure == "runtime" else severity(contract, f"{kind}_inverse"), "wiki", message or "Knot ticket could not be resolved."))
        elif status in tracking["warning_statuses"]:
            if ticket_id not in terminal_warning_ids:
                path, line = citations.get(ticket_id, ("wiki", None))
                problems.append(issue(f"{kind}.status", severity(contract, f"{kind}_status"), path, f"Knot ticket {ticket_id} is in historical terminal status {status!r}.", line))
        elif status in tracking["valid_statuses"] and ticket_id not in citations:
            problems.append(issue(f"{kind}.inverse", severity(contract, f"{kind}_inverse"), "wiki", f"Knot ticket {ticket_id} with configured tag {tracking['tag']!r} is not cited in section {tracking['section']!r}."))
    return problems


def validate(repository_root: Path, schema_path: Path) -> tuple[list[Diagnostic], int, bool]:
    wiki_root = repository_root / "wiki"
    contract_path = wiki_root / "wiki-structure.yaml"
    if not wiki_root.is_dir():
        return [issue("runtime.wiki-missing", "error", "wiki", "Wiki directory not found.")], 0, True
    contract, problems = validate_contract(contract_path, schema_path)
    if contract is None:
        return sorted(problems, key=issue_key), 0, True
    markdown = sorted((path for path in wiki_root.rglob("*.md") if path.is_file()), key=lambda path: relative(path, wiki_root))
    for path in markdown:
        try:
            path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            problems.append(issue("runtime.page-read", "error", relative(path, wiki_root), f"Could not read Markdown file: {exc}"))
    if any(item.code.startswith("runtime.") for item in problems):
        return sorted(problems, key=issue_key), 0, True
    problems.extend(validate_topology(wiki_root, contract))
    problems.extend(validate_initial_content(wiki_root, contract))
    for path in markdown:
        problems.extend(validate_page(path, wiki_root, contract))
        problems.extend(validate_references(path, wiki_root, contract))
    problems.extend(validate_navigation(wiki_root, contract))
    problems.extend(validate_intent_map(wiki_root, contract))
    problems.extend(validate_assets_and_diagrams(wiki_root, contract))
    problems.extend(validate_provenance(wiki_root, contract))
    problems.extend(validate_contextual_citations(wiki_root, contract))
    problems.extend(validate_structured_sections(wiki_root, contract))
    problems.extend(validate_tracking(wiki_root, contract, repository_root, "pendency"))
    problems.extend(validate_tracking(wiki_root, contract, repository_root, "proposal"))
    runtime_failure = any(item.code.startswith("runtime.") for item in problems)
    return sorted(problems, key=issue_key), len(markdown), runtime_failure


def render(problems: list[Diagnostic], files_checked: int, output_format: str) -> str:
    errors = sum(item.severity == "error" for item in problems)
    warnings = sum(item.severity == "warning" for item in problems)
    summary = {"files_checked": files_checked, "errors": errors, "warnings": warnings}
    if output_format == "json":
        return json.dumps({"ok": errors == 0, "summary": summary, "diagnostics": [asdict(item) for item in problems]}, indent=2) + "\n"
    lines = [f"Files checked: {files_checked}", f"Errors: {errors}", f"Warnings: {warnings}"]
    for item in problems:
        location = f"{item.path}:{item.line}" if item.line is not None else item.path
        lines.append(f"{location}: {item.severity} [{item.code}] {item.message}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--contract-only", action="store_true", help="Validate only the instance contract; do not read pages or access Knot.")
    args = parser.parse_args(argv)
    repository_root = args.repository_root.resolve()
    schema_path = Path(__file__).resolve().parent.parent / "contracts" / "wiki-structure.schema.json"
    try:
        if args.contract_only:
            contract, problems = validate_contract(repository_root / "wiki/wiki-structure.yaml", schema_path)
            problems = sorted(problems, key=issue_key)
            files_checked = 0
            preflight_failure = contract is None
        else:
            problems, files_checked, preflight_failure = validate(repository_root, schema_path)
    except (OSError, UnicodeError, ValueError) as exc:
        problems = [issue("runtime.failure", "error", repository_root, f"Could not traverse the repository: {exc}")]
        files_checked = 0
        preflight_failure = True
    print(render(problems, files_checked, args.format), end="")
    if preflight_failure:
        return 2
    return 1 if any(item.severity == "error" for item in problems) else 0


if __name__ == "__main__":
    sys.exit(main())
