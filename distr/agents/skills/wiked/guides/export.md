# PDF, DOCX, SVG, and PNG Export

Load this guide only for an explicitly requested query export. Output is neither wiki content nor evidence.

## Boundaries

- Derive content only from canonical Markdown allowed by `query.md`; permanent SVG is only complementary.
- Write the artifact in the configured instance language and preserve canonical terms.
- Never modify the wiki or place outputs or intermediates below it.
- Honor an explicit output path; otherwise use a descriptive filename at the consumer root.
- Interpret Word as DOCX; clarify before producing legacy DOC.
- Default a standalone diagram to SVG unless PNG is requested or required.

## Dependencies

Check executables with `command -v`; report, but never install, missing tools:

| Output | Required tools |
| --- | --- |
| DOCX | `pandoc`; `rsvg-convert` only for a needed compatibility fallback |
| PDF | `pandoc`, `weasyprint`; `rsvg-convert` when diagrams are present |
| Existing SVG | no renderer; copy the accepted derivative |
| New or adjusted SVG | `d2` and `d2.md` |
| PNG diagram | `rsvg-convert`; also `d2` for a new render |

## Workspace and Conversion

Resolve absolute repository and output paths. In one unique private temporary directory, materialize a complete Markdown input and copy referenced resources to the paths that input expects.

For PDF, convert copied D2 SVG resources to temporary PNG before Pandoc when installed WeasyPrint renders them incorrectly. Never alter accepted wiki assets for compatibility.

```bash
rsvg-convert --format=png --output="<temporary>.png" "<copied>.svg"
pandoc "document.md" --resource-path="<temp>:<repository>:<wiki>:<source-dirs>" \
  --pdf-engine=weasyprint -o "<absolute-output>.pdf"
pandoc "document.md" --resource-path="<temp>:<repository>:<wiki>:<source-dirs>" \
  -o "<absolute-output>.docx"
```

Copy an existing diagram's accepted SVG. For a new or adjusted diagram, follow `d2.md` using only a temporary D2 copy; render SVG or convert the temporary SVG to PNG with `rsvg-convert`.

## Validate and Clean Up

1. Confirm each final file exists outside the temporary directory and is non-empty.
2. Visually inspect PDF, SVG, and PNG for completeness and legibility. Check DOCX resource embedding and warnings.
3. Report final absolute paths, formats, consulted wiki pages, and limitations.
4. Remove the unique temporary directory even after failure and confirm it is absent.
