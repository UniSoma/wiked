---
id: wik-01m7at8mcfp3-d1k8n
ticket: wik-01m7at8mcfp3
title: 'Protótipo: Instance contract de referência para mapeamento consultivo'
type: other
created: '2026-11-13T16:11:23.320147006Z'
updated: '2026-11-13T16:11:23.320147006Z'
---

# Protótipo: Instance contract de referência para mapeamento consultivo (UC2)

PROTÓTIPO DESCARTÁVEL, ilustrativo. Gerado por `build.py` (anexo abaixo) numa mini-wiki sintética em inglês e validado com o Distributed validator v1.9.0 real e um rastreador Knot local de rascunho. Resultado: 19 arquivos, 0 erros, 0 avisos.

## Modelo

| Tronco | page_type | Seção estruturada (registros) | Campos |
|---|---|---|---|
| processes | process (roles knowledge+flow) | SIPOC (1); Activities (≥1) | Suppliers/Inputs/Outputs/Customers; Accountable (exatamente 1), Responsible (≥1), Consulted/Informed ("Nobody."), Data sources/Rules/Tools ("None.") |
| rules | business_rule | Rule (1) | Statement, Authority, Applies to, Uses data |
| data | data_source | Profile (1) | System, Owner (1), Steward ("Not assigned."), Refresh, Used by |
| tools | analytical_tool | Profile (1) | Purpose, Users, Data sources, Supports |
| stakeholders | role | — | texto livre |
| gaps | gap (open/addressed/accepted) | Gap (1) | Kind (dimensão DAMA), Affects, Impacts, Cause, Owner |
| sources | source | Source record / Grounded pages | proveniência padrão (entrevistas, workshops) |

As-is/to-be: página `current` com `## Proposed changes` → `[ticket] título`; página-par `state: proposed` com `change_ticket`. Pendências em `## Open questions` → `[ticket] título`. Diagramas D2 só para o papel `flow` (processos).

## O que o mecanismo atual já garante (verificado)

- Cardinalidade RACI: dois Accountable → `structured.cardinality` (erro).
- Vazio explícito obrigatório (sentinela) em vez de campo omitido.
- Pendência/proposta ligada a ticket Knot; ticket fechado → aviso `pendency.status`; ticket com a tag não citado → `pendency.inverse`.
- Proveniência bidirecional (fonte ↔ páginas fundamentadas).
- Diagrama exigido apenas nos tipos com papel `flow`.

## O que não garante (lacunas, para o ticket de consolidação)

1. **Tipo do destino em campo `page`**: `Rules` aceita link para um papel (stakeholder) sem diagnóstico. Falta restringir o tipo/tronco de destino.
2. **Vínculo inverso entre páginas**: regra diz "Applies to: Order intake", processo deixa de citar a regra → nada. Falta checagem de coerência bidirecional/cobertura (relacionado à checagem de cobertura já registrada como evolução).
3. **Par as-is/to-be**: nenhum vínculo tipado entre página `current` e `proposed`; o par é só convenção (link no corpo + mesmo ticket). Processo as-is sem to-be nem decisão "sem mudança" passa.
4. **Estado de proposta único**: `proposal_tracking` exige que *todo* tipo com o papel aceite `proposed` (o tipo `gap` precisou ganhá-lo).
5. **Aceitar A = R**: o RACI admite a mesma pessoa como Accountable e Responsible; `disjoint_with` não deve ser usado aí (erro de modelagem detectado no protótipo).

## Resposta à pergunta do ticket

O mecanismo atual (operação atual × propostas em tickets) basta para *registrar* as-is/to-be com governança; não basta para *comparar* nem para garantir *cobertura*. Isso confirma "disponível hoje" para o registro e "em evolução" para comparação lado a lado e checagens de tipo de destino e de vínculos.

## Anexo: build.py

```python
# PROTOTYPE, throwaway: illustrative Instance contract + synthetic wiki for the consulting-mapping use case (UC2).
import sys, pathlib, yaml
root = pathlib.Path(sys.argv[1]); P, Q = (root / "ids.txt").read_text().split()
wiki = root / "wiki"
def rec(name, types, fields, lo=1, hi=None):
    return {"section": name, "page_types": types, "min_records": lo, "max_records": hi, "fields": fields}
def f(name, types=("page",), lo=1, hi=None, empty=None, disjoint=None):
    d = {"name": name, "value_types": list(types), "min_items": lo, "max_items": hi}
    if empty: d["empty_value"] = empty
    if disjoint: d["disjoint_with"] = disjoint
    return d
K = ["knowledge"]
def ptype(states, extra_opt=()):
    return {"roles": K, "states": states,
            "fields": {"required": ["type", "state"], "optional": ["reviewed_on", "change_ticket", *extra_opt], "date": ["reviewed_on"]},
            "sections": {"required": ["Sources"]}}
contract = {
  "contract_version": "1.0", "methodology_version": "1.9.0", "language": "en",
  "initial_content": {
    "title": "Client mapping knowledge base",
    "purpose": "Map processes, data sources, business rules, analytical tools and stakeholders, current and proposed.",
    "audience": "Consulting team, client sponsors and agents.",
    "scope": "Areas in the engagement scope.",
    "context_terms": [
      {"term": "Data source", "definition": "A business system, file or feed that holds data used by a process, rule or tool. Not a wiki Source."},
      {"term": "Gap", "definition": "A documented shortfall between the current state and what a use needs."}]},
  "topology": {"trunks": ["processes", "rules", "data", "tools", "stakeholders", "gaps", "sources"],
               "required_trunks": ["sources"], "sources_trunk": "sources", "max_depth": 1, "assets_directory": "assets"},
  "naming": {"pattern": "^[a-z][a-z0-9-]*$"},
  "navigation": {"root_index": "index.md", "trunk_index": "index.md", "context_file": "CONTEXT.md"},
  "frontmatter": {"marker": "---", "exceptions": ["index.md", "CONTEXT.md"]},
  "page_types": {
    "process": {**ptype(["current", "proposed"]), "roles": ["knowledge", "flow"]},
    "business_rule": ptype(["current", "proposed"]),
    "data_source": ptype(["current", "proposed"]),
    "analytical_tool": ptype(["current", "proposed"]),
    "role": ptype(["current", "proposed"]),
    "gap": ptype(["open", "addressed", "accepted", "proposed"]),
    "source": {"roles": ["evidence"], "states": ["indexed", "empty"],
               "fields": {"required": ["type", "state", "indexed_on"], "optional": [], "date": ["indexed_on"]},
               "sections": {"required": ["Source record", "Grounded pages"]}}},
  "states": ["current", "proposed", "open", "addressed", "accepted", "indexed", "empty"],
  "sections": {"source_record": "Source record", "grounded_pages": "Grounded pages", "content_sources": "Sources", "no_content": "None."},
  "structured_sections": [
    rec("SIPOC", ["process"], [f("Suppliers", ("text", "page")), f("Inputs", ("text", "page")),
        f("Outputs", ("text", "page")), f("Customers", ("text", "page"))], 1, 1),
    rec("Activities", ["process"], [
        f("Accountable", lo=1, hi=1), f("Responsible"),
        f("Consulted", lo=0, empty="Nobody."), f("Informed", lo=0, empty="Nobody."),
        f("Data sources", lo=0, empty="None."), f("Rules", lo=0, empty="None."), f("Tools", lo=0, empty="None.")]),
    rec("Rule", ["business_rule"], [f("Statement", ("text",), 1, 1), f("Authority", ("text", "page"), 1, 1),
        f("Applies to"), f("Uses data", lo=0, empty="None.")], 1, 1),
    rec("Profile", ["data_source"], [f("System", ("text",), 1, 1), f("Owner", lo=1, hi=1), f("Steward", lo=0, empty="Not assigned."),
        f("Refresh", ("text",), 1, 1), f("Used by")], 1, 1),
    rec("Profile", ["analytical_tool"], [f("Purpose", ("text",), 1, 1), f("Users"), f("Data sources"), f("Supports", lo=0, empty="None.")], 1, 1),
    rec("Gap", ["gap"], [f("Kind", ("text",), 1, 1), f("Affects"), f("Impacts"), f("Cause", ("text",), 1, 1),
        f("Owner", lo=1, hi=1)], 1, 1)],
  "assets": {"allowed_extensions": ["svg", "png"], "forbidden_files": ["index.md"], "allow_subdirectories": False},
  "diagrams": {"required_extensions": ["md", "d2", "svg"], "source_extension": "d2", "visualization_extension": "svg", "applies_to_roles": ["flow"]},
  "provenance": {"source_role": "evidence", "content_roles": K,
     "record_fields": ["Kind", "Origin", "Scope", "Published", "Consulted", "Indexed"],
     "publication_date_field": "Published", "publication_unknown": "unknown", "date_fields": ["Consulted", "Indexed"],
     "indexed_field": "indexed_on", "indexed_record_field": "Indexed", "no_content_states": ["empty"]},
  "pendency_tracking": {"roles": K, "section": "Open questions", "id_pattern": "^cli-01[0-9a-z]+$", "tag": "pendency",
     "valid_statuses": ["open", "in_progress"], "warning_statuses": ["closed"]},
  "proposal_tracking": {"roles": K, "section": "Proposed changes", "id_pattern": "^cli-01[0-9a-z]+$", "tag": "proposal",
     "valid_statuses": ["open", "in_progress"], "warning_statuses": ["closed"], "frontmatter_field": "change_ticket", "proposal_state": "proposed"},
  "rules": {n: {"severity": "warning" if n in {"pendency_status", "proposal_status"} else "error"} for n in (
     "contract", "topology", "navigation", "frontmatter", "h1", "reference", "assets", "diagrams", "provenance",
     "contextual_citation", "pendency_location", "pendency_association", "pendency_status", "pendency_inverse",
     "proposal_location", "proposal_association", "proposal_status", "proposal_inverse", "structured_sections", "heading_fragments")},
}
pages = {}
def page(path, ptype, state, title, body, extra=""):
    pages[path] = f"---\ntype: {ptype}\nstate: {state}\n{extra}---\n# {title}\n\n{body.strip()}\n\n## Sources\n\n- [Interview with the sales desk](../sources/interview-sales-desk.md)\n"
L = lambda t, p: f"[{t}](../{p}.md)"
SD, CA, FM = L("Sales desk", "stakeholders/sales-desk"), L("Credit analyst", "stakeholders/credit-analyst"), L("Finance manager", "stakeholders/finance-manager")
ERP, CLR, DASH = L("Customer master", "data/customer-master"), L("Credit limit check", "rules/credit-limit-check"), L("Sales dashboard", "tools/sales-dashboard")
page("processes/order-intake.md", "process", "current", "Order intake", f"""
How customer orders are received and released today.\n\n![Order intake flow](./order-intake.svg)

## SIPOC

### Order intake scope

- **Suppliers:** Customers
- **Inputs:** Purchase order
- **Outputs:** Released order
- **Customers:** {L("Finance manager", "stakeholders/finance-manager")}

## Activities

### Register the order

- **Accountable:** {SD}
- **Responsible:** {SD}
- **Consulted:** Nobody.
- **Informed:** Nobody.
- **Data sources:** {ERP}
- **Rules:** None.
- **Tools:** None.

### Check credit

- **Accountable:** {FM}
- **Responsible:** {CA}
- **Consulted:** {SD}
- **Informed:** Nobody.
- **Data sources:** {ERP}
- **Rules:** {CLR}
- **Tools:** {DASH}

## Open questions

- [{P}] Confirm who approves credit exceptions

## Proposed changes

- [{Q}] Automate credit analysis at order intake
""")
page("processes/order-intake-proposed.md", "process", "proposed", "Order intake (proposed)", f"""
Proposed future state: credit is checked automatically at registration; replaces [Order intake](./order-intake.md).\n\n![Proposed order intake flow](./order-intake-proposed.svg)

## SIPOC

### Order intake scope

- **Suppliers:** Customers
- **Inputs:** Purchase order
- **Outputs:** Released order
- **Customers:** {FM}

## Activities

### Register and check the order

- **Accountable:** {SD}
- **Responsible:** {CA}
- **Consulted:** Nobody.
- **Informed:** {FM}
- **Data sources:** {ERP}
- **Rules:** {CLR}
- **Tools:** None.

## Proposed changes

- [{Q}] Automate credit analysis at order intake
""", f"change_ticket: {Q}\n")
page("rules/credit-limit-check.md", "business_rule", "current", "Credit limit check", f"""
## Rule

### Credit limit

- **Statement:** An order is held when the customer's open balance plus the order exceeds the credit limit.
- **Authority:** Credit policy (interview)
- **Applies to:** {L("Order intake", "processes/order-intake")}
- **Uses data:** {ERP}
""")
page("data/customer-master.md", "data_source", "current", "Customer master", f"""
## Profile

### Customer master

- **System:** ERP customer table
- **Owner:** {FM}
- **Steward:** Not assigned.
- **Refresh:** Real time
- **Used by:**
  - {L("Order intake", "processes/order-intake")}
  - {CLR}
  - {DASH}
""")
page("tools/sales-dashboard.md", "analytical_tool", "current", "Sales dashboard", f"""
## Profile

### Sales dashboard

- **Purpose:** Monitor held orders and credit exposure.
- **Users:** {CA}
- **Data sources:** {ERP}
- **Supports:** {L("Order intake", "processes/order-intake")}
""")
for slug, title, text in [("sales-desk", "Sales desk", "Registers customer orders."),
                          ("credit-analyst", "Credit analyst", "Reviews held orders."),
                          ("finance-manager", "Finance manager", "Owns credit policy and customer data.")]:
    page(f"stakeholders/{slug}.md", "role", "current", title, text)
page("gaps/missing-credit-history.md", "gap", "open", "Missing credit history", f"""
## Gap

### Missing credit history

- **Kind:** Completeness
- **Affects:** {ERP}
- **Impacts:**
  - {CLR}
  - {DASH}
- **Cause:** Payment history is kept in spreadsheets outside the ERP.
- **Owner:** {FM}
""")
grounded = "\n".join(f"- [{t}](../{p})" for p, t in sorted(
    (p, c.split("\n# ", 1)[1].split("\n", 1)[0]) for p, c in pages.items()))
pages["sources/interview-sales-desk.md"] = ("---\ntype: source\nstate: indexed\nindexed_on: 2026-11-12\n---\n# Interview with the sales desk\n\n"
  "## Source record\n\n- **Kind:** interview notes.\n- **Origin:** workshop held with the sales desk.\n- **Scope:** order intake and credit.\n"
  "- **Published:** unknown.\n- **Consulted:** 2026-11-12.\n- **Indexed:** 2026-11-12.\n\n## Grounded pages\n\n" + grounded + "\n")
trunks = {"processes": "Processes", "rules": "Business rules", "data": "Data sources", "tools": "Analytical tools",
          "stakeholders": "Stakeholders", "gaps": "Gaps", "sources": "Sources"}
for t, title in trunks.items():
    items = sorted((c.split("\n# ", 1)[1].split("\n", 1)[0], p) for p, c in pages.items() if p.startswith(t + "/"))
    pages[f"{t}/index.md"] = f"# {title}\n\n" + "".join(f"- [{n}](./{p.split('/', 1)[1]})\n" for n, p in items)
ic = contract["initial_content"]
pages["index.md"] = f"# {ic['title']}\n\n{ic['purpose']}\n\n{ic['audience']}\n\n{ic['scope']}\n\n- [Context](./CONTEXT.md)\n" + \
    "".join(f"- [{title}](./{t}/index.md)\n" for t, title in trunks.items())
pages["CONTEXT.md"] = "# Context\n\n" + "".join(f"## {x['term']}\n\n{x['definition']}\n\n" for x in ic["context_terms"])
for p, c in pages.items():
    (wiki / p).parent.mkdir(parents=True, exist_ok=True); (wiki / p).write_text(c, encoding="utf-8")
(wiki / "assets").mkdir(exist_ok=True)
for stem in ("order-intake", "order-intake-proposed"):
    (wiki / "processes" / f"{stem}.d2").write_text("sales -> credit\n"); (wiki / "processes" / f"{stem}.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'/>\n")
(wiki / "wiki-structure.yaml").write_text(yaml.safe_dump(contract, sort_keys=False, allow_unicode=True), encoding="utf-8")
```

## Anexo: página de exemplo (processes/order-intake.md)

```markdown
---
type: process
state: current
---
# Order intake

How customer orders are received and released today.

![Order intake flow](./order-intake.svg)

## SIPOC

### Order intake scope

- **Suppliers:** Customers
- **Inputs:** Purchase order
- **Outputs:** Released order
- **Customers:** [Finance manager](../stakeholders/finance-manager.md)

## Activities

### Register the order

- **Accountable:** [Sales desk](../stakeholders/sales-desk.md)
- **Responsible:** [Sales desk](../stakeholders/sales-desk.md)
- **Consulted:** Nobody.
- **Informed:** Nobody.
- **Data sources:** [Customer master](../data/customer-master.md)
- **Rules:** None.
- **Tools:** None.

### Check credit

- **Accountable:** [Finance manager](../stakeholders/finance-manager.md)
- **Responsible:** [Credit analyst](../stakeholders/credit-analyst.md)
- **Consulted:** [Sales desk](../stakeholders/sales-desk.md)
- **Informed:** Nobody.
- **Data sources:** [Customer master](../data/customer-master.md)
- **Rules:** [Credit limit check](../rules/credit-limit-check.md)
- **Tools:** [Sales dashboard](../tools/sales-dashboard.md)

## Open questions

- [cli-01m7atr184sx] Confirm who approves credit exceptions

## Proposed changes

- [cli-01m7atr1bqt5] Automate credit analysis at order intake

## Sources

- [Interview with the sales desk](../sources/interview-sales-desk.md)
```
