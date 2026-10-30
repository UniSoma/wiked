"""Shared contract loading, page parsing, and link extraction for Wiked runtime scripts."""

from __future__ import annotations

import ipaddress
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from markdown_it import MarkdownIt

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
    if any("external_authority" in page_type for page_type in contract["page_types"].values()):
        if required_version < (1, 8, 0):
            relations.append(issue("contract.relation", "error", contract_label, "External authority requires methodology_version 1.8.0 or newer."))
        if "external_authority" not in contract["rules"]:
            relations.append(issue("contract.relation", "error", contract_label, "A page type with external authority requires rules.external_authority."))
    if "external_links" in contract["rules"] and required_version < (1, 8, 0):
        relations.append(issue("contract.relation", "error", contract_label, "External link checks require methodology_version 1.8.0 or newer."))
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


# The default parser silently drops links with schemes such as javascript: or file:;
# external-link checks must see every explicit destination to diagnose it.
PERMISSIVE_MARKDOWN = MarkdownIt()
PERMISSIVE_MARKDOWN.validateLink = lambda url: True
LINK_SCHEMES = {"http", "https", "mailto"}
IMAGE_SCHEMES = {"http", "https"}
HOST_LABEL = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)")
MAIL_ADDRESS = re.compile(r"[^@\s]+@[^@\s]+")


def external_links(text: str, line_offset: int = 0) -> list[tuple[str, int, bool]]:
    """Return explicit link, autolink, and image destinations that point outside the wiki."""
    links: list[tuple[str, int, bool]] = []
    for token in PERMISSIVE_MARKDOWN.parse(text):
        if token.type != "inline" or not token.map:
            continue
        line = token.map[0] + line_offset + 1
        for child in token.children or []:
            attribute = {"link_open": "href", "image": "src"}.get(child.type)
            target = dict(child.attrs or []).get(attribute) if attribute else None
            if target is None:
                continue
            try:
                parsed = urlsplit(target)
            except ValueError:
                links.append((target, line, child.type == "image"))
                continue
            # data: embeds content in the page; it does not point outside the wiki.
            if (parsed.scheme or parsed.netloc) and parsed.scheme.lower() != "data":
                links.append((target, line, child.type == "image"))
    return links


def valid_host(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        pass
    try:
        host = host.encode("idna").decode("ascii")
    except UnicodeError:
        return False
    labels = host.lower().removesuffix(".").split(".")
    return len(host) <= 253 and all(HOST_LABEL.fullmatch(label) for label in labels)


def external_link_problem(target: str, image: bool = False) -> tuple[str, str] | None:
    """Classify an external destination offline as (code, message), or None when acceptable."""
    try:
        parsed = urlsplit(target)
        # Markdown normalization percent-encodes the authority, including IPv6 brackets.
        authority = urlsplit(f"//{unquote(parsed.netloc)}")
        authority.port  # Raises for an invalid port.
    except ValueError:
        return "external-link.malformed", f"External link is malformed: {target}."
    scheme = parsed.scheme.lower()
    if scheme not in (IMAGE_SCHEMES if image else LINK_SCHEMES):
        kind = "image" if image else "link"
        return "external-link.scheme", f"External {kind} scheme is not allowed: {scheme or 'none'} in {target}."
    if scheme == "mailto":
        addresses = unquote(parsed.path).split(",")
        if not all(MAIL_ADDRESS.fullmatch(address.strip()) for address in addresses):
            return "external-link.malformed", f"External link is malformed: {target}."
        return None
    if not authority.hostname or not valid_host(authority.hostname):
        return "external-link.malformed", f"External link is malformed: {target}."
    return None
