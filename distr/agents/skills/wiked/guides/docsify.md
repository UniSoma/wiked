# Optional Docsify Diagram Navigation

Load only to propose, enable, or review interactive process diagrams in a consumer
using Docsify. Docsify and clickable diagrams are optional; static diagrams remain
valid under [the diagram protocol](d2.md#step-correspondence-and-navigation).
This guide is not a general Docsify installation, theme, search, or publishing guide.

## Authority and Adoption

- Read the instance contract. For review, complete `authoring-context.md`; no grill
  is needed unless objective qualification is requested. Before changing content
  or viewer configuration, satisfy `grill.md`, including qualification and explicit
  scope confirmation. For diagram changes, also load `d2.md`.
- During post-installation maintenance, inspect the existing viewer configuration
  to identify Docsify. Propose this integration and report compatibility or
  deployment gaps. Installing Wiked does not activate it or authorize viewer edits.
- Wiked owns the distributed [HTML example](../viewers/index.html), including its
  inline diagram adapter. Authorized adoption copies/adapts it into the consumer
  repository; that viewer, its embedded code, configuration, deployment, assets,
  and operational Markdown are consumer-owned. Never edit the installed example
  or install tools while operating a wiki. Humans install tools and arrange
  deployment. Never serve or reference `.agents/`, installed skill files, or the
  Wiked source repository as viewer dependencies.
- The adopted viewer must remain navigable after removing or updating the skill.
  Record the integration's adopted source version in the HTML, independently of
  the installed skill version. Future integration updates require an explicit
  proposal, authorized scope, preservation of local configuration, and browser
  acceptance; never synchronize or overwrite the viewer during skill updates.

Adoption offers readers clickable diagram steps leading to their canonical
sections, return links back to the exact node, and a link to each original SVG.
It requires a consumer already using or choosing Docsify, a governed change copying
the example into a consumer-owned viewer, explicit anchors and return links in
affected pages, browser acceptance, and consumer ownership of that viewer's
configuration, deployment, and future updates. Static diagrams remain conformant
without it.

## Integration Contract

The reference target is Docsify **4.13.1**, hash routing, same-origin HTTP(S) SVGs,
and D2 SVGs with source-node identities encoded as base64 CSS classes. This
metadata was checked with D2 **0.7.1**. Padded and unpadded class encodings are
accepted. Treat other versions, history routing, Markdown renderer overrides,
and plugins that replace images or intercept links as compatibility checks, not
assumed support. Perform the browser acceptance below before declaring adoption
functional, including on the reference versions.
When using Wiked to author or validate this integration, use 1.6.0 or newer:
older validators do not recognize its explicit description anchors. Include any
required instance compatibility update in the approved adoption scope. Reading
and navigating the adopted wiki does not require Wiked or its validator.

Keep the ordinary Markdown image. Its title marker opts that diagram into enhancement;
unmarked images remain static. A return link declares a node/description
association once; the adapter uses it to make that node clickable in the other
direction. No custom `<div>`, D2 `link` property, added icon, SVG edit, or new
instance-contract field is needed.

Use stable ASCII `snake_case` identifiers for diagrams and description anchors.
Node identifiers are the actual D2 source keys, not labels; qualify nested keys
with dots, such as `review.receive`. Do not change identities when labels change.
Diagram identifiers must be unique within the entry. Each SVG is embedded once.

### Markdown

For a `process.md`, `process.d2`, `process.svg` component set:

```markdown
# Process

![Process flow](process.svg "wiked-diagram=process")

<a id="step_receive"></a>

## Receive request

Register the request and check the supplied information.

[Back to step in diagram](process.svg#wiked-node=receive&section=step_receive)

<a id="step_validate"></a>

## Validate request

Check the requirements and decide whether the request can proceed.

[Back to step in diagram](process.svg#wiked-node=validate&section=step_validate)
```

Keep headings and node labels equal. Write content, image descriptions, and
return-link text in the instance language. Each portable `<a id="...">` is the
stable target of its immediately following section; do not use heading-derived
slugs or Docsify-only heading syntax as substitutes for these targets.

The image and its return links must use the same authored relative SVG path,
without a leading `./` (for example, `process.svg` or `../assets/process.svg`).
This avoids Docsify's special rewriting of ignored `./` links and makes nested
entries independent of the viewer document's URL. Do not turn these local
references into hardcoded deployment URLs. A return link names an SVG node and
a section in the **current entry**; cross-entry associations are not supported
by this adapter. Ordinary wiki page links remain ordinary Markdown links.
Keep the image URL free of fragments: Docsify 4.13.1 can discard its filename
while resolving a relative image URL containing `#`. The title marker avoids
that behavior while retaining normal static Markdown image rendering.

### D2

```d2
direction: down

receive: Receive request
validate: Validate request

receive -> validate
```

Keep the accepted layout, shapes, styles, and connections. The adapter locates
each source key using D2's encoded class metadata and makes its existing group
interactive; it does not infer identity from text or incidental SVG IDs. D2's
`link` attribute can introduce link icons or rendering changes, so do not add it
for this integration. An existing linked node requires separate review; the
adapter rejects a mapped node already inside a link rather than replacing its
behavior silently. It never hides existing link/tooltip decorations.

Repeated steps may share a canonical description. Give each occurrence its own
source key and add a separate return link for each, with meaningful occurrence
context. For one return, use the localized equivalent of "Back to step in diagram".
For multiple returns, use "Back to step in diagram: <node title>"; when titles
repeat, append " - <occurrence context>", including diagram context when needed.
Do not rename nodes merely to disambiguate return links. Multiple diagrams use
different image identifiers and asset paths; each can contain the same node key.

## Viewer Configuration

Use the complete [index.html example](../viewers/index.html) as the adoption
source, not as a runtime URL. It includes the mount element, a pinned Docsify
stylesheet and script, configuration, and the diagram adapter inline in
`<script id="wiked-docsify-diagrams">`. There is no separate adapter JS to deploy.

For a new viewer, copy/adapt the example to a consumer-owned file outside the
governed `wiki/` tree, such as `viewer/index.html`. Keep that HTML in the wiki
repository alongside its content. For an existing viewer, merge the inline
adapter and required configuration into its HTML; do not replace local navigation,
plugins, styles, or configuration with the example. Adapt language, title,
`basePath`, homepage, and navigation to the actual deployment. The example's
`/wiki/` content URL is illustrative, not a required hosting topology.

The deployed HTML contains the integration code itself. Do not load that code
from the skill installation, symlink to it, fetch it from Wiked, or require the
skill to be present at build or serving time. Wiked supplies an adoption example,
not a service or an operational wiki dependency. Docsify remains the chosen viewer
dependency, independently of Wiked.

The inline adapter must execute **after configuration but before Docsify**.
Preserve existing
`noCompileLinks` entries and add the SVG pattern: SVG return URLs must not become
Docsify entry routes. If a content-security policy disallows inline scripts,
arrange an approved hash/nonce for the adopted HTML or report a deployment gap;
do not weaken the policy or silently introduce an installed-skill dependency.
If the policy or offline deployment disallows the illustrated CDN, the human must
supply the approved pinned Docsify assets locally, including the stylesheet.
Do not weaken the policy. Verify `basePath` and image `data-origin`
attributes in the actual deployment, especially for nested entries.

The adapter enhances opted-in images after each rendered entry, intercepts the
corresponding return links, scrolls to and focuses the actual node or section,
and leaves the current entry route unchanged. It does not promise browser-history
entries or shareable direct node URLs. Enter activates a focused node. SVG styles
and renderer IDs are isolated in a shadow root, so multiple diagrams do not leak
styles or collide. It does not modify diagram files, labels, geometry, or layout.

Each successfully enhanced diagram also exposes a native "Open original diagram"
link to its validated SVG URL, without forcing a new tab. Adapt this label in the
inline adapter to the instance language during adoption. The link shares the
diagram's original visibility and is removed with it when rebuilding the entry.
It opens the static original, not the interactive node/description navigation;
users can choose the browser's open-in-new-tab actions and available zoom controls.
Browser zoom support varies; this is not an embedded zoom feature or a universal
zoom guarantee. Failed or stale enhancements must not leave generated links.

## Trust, Failure, and Validation

Only use reviewed, locally generated SVGs from the same origin as the viewer.
The adapter refuses cross-origin loads, redirects, oversized SVG text, active
content, foreign HTML, event attributes, and unsupported external resources.
Renderer styles are isolated; these checks are conservative rejection, **not a
general-purpose sanitizer for hostile SVG**. Do not point it at uploads or
untrusted sources. Bundled raster images and embedded font resources are allowed;
unsupported SVG features must be reported, not made to work by weakening checks.
Opening the original requests the raw asset again; the inline checks do not
sanitize that document or guarantee that a later response has identical bytes.

On a failed enhancement the image remains visible, a diagnostic is logged to
the browser console, and `data-wiked-error` identifies the affected image. Outside
the integration, Markdown and diagrams remain readable; return links may open the
static SVG and do not promise node-level navigation. Report that limitation rather
than claiming interactive adoption succeeded. Leaving/reopening an entry aborts
stale requests and rebuilds its associations.

Run the distributed validator. It recognizes portable explicit anchor targets,
reports duplicate/colliding anchors, and checks the optional return-link syntax
and description anchor. It still checks ordinary heading links and the required
single Markdown visualization embedding. It does **not** establish node existence
in rendered SVG, title equality, semantic correspondence, or browser behavior.

### Browser Acceptance

In the actual viewer, verify:

1. Each mapped action, decision, and subprocess is clickable to its exact section;
   every return reaches the intended occurrence, not only the diagram container.
2. Multiple diagrams, nested entry paths, repeated steps, and same-title
   occurrences remain distinct. Confirm no unintended entry navigation.
3. Links work after leaving/reopening and reloading the entry; delayed or failed
   SVG requests cannot alter a different entry. Failed loads preserve the image.
4. Keyboard focus and Enter activation work. Compare with the accepted diagram:
   labels, shapes, styles, connections, layout, and decorations remain unchanged.
5. Renaming a heading without changing its explicit anchor preserves navigation.
   Read-only/static presentation remains useful without the adapter.
6. Serve only the consumer-owned HTML, content, and approved viewer assets with
    the Wiked installation unavailable. Verify entry navigation and both diagram
    directions after reload, with no requests or build inputs from the skill.
7. Each enhanced diagram's original-file link reaches its own SVG, including from
   nested entries, is reachable by Tab and activated by Enter, and does not force
   a new tab. Check user-chosen independent opening and the browser's available
   zoom controls. Originally hidden images must not expose a visible link. Repeat
   navigation after returning and reloading; links must not duplicate or survive
   failed/stale enhancements.

Record viewer/renderer versions, results, unsupported behavior, and any untested
cases. A successful installation or validator run is not browser acceptance.
Maintenance may recommend adoption and track follow-ups without activating it;
unadopted interactivity is not a generic Wiked defect.
