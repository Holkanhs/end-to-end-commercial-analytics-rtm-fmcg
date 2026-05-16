# Diagrams

PNG exports of the project's architecture diagrams. The source `.mmd` files are kept alongside the rendered PNGs so the diagrams are reproducible.

| Diagram | Source | Rendered |
|---|---|---|
| Medallion architecture (Bronze → Silver → Gold) | [`medallion_architecture.mmd`](medallion_architecture.mmd) | ![medallion](medallion_architecture.png) |
| End-to-end ELT flow (Snowflake → dbt → Power BI) | [`elt_flow.mmd`](elt_flow.mmd) | ![elt](elt_flow.png) |
| Power BI star schema (ER diagram) | [`star_schema.mmd`](star_schema.mmd) | ![star](star_schema.png) |

## Re-render

Requires Node.js (any recent version). No global install — `npx` downloads the renderer on demand.

```bash
# from this folder:
npx --yes -p @mermaid-js/mermaid-cli mmdc \
    -i medallion_architecture.mmd -o medallion_architecture.png \
    -b white -w 1600 -p puppeteer-config.json

npx --yes -p @mermaid-js/mermaid-cli mmdc \
    -i elt_flow.mmd -o elt_flow.png \
    -b white -w 1800 -p puppeteer-config.json

npx --yes -p @mermaid-js/mermaid-cli mmdc \
    -i star_schema.mmd -o star_schema.png \
    -b white -w 1600 -p puppeteer-config.json
```

The `puppeteer-config.json` in this folder disables the Chromium sandbox so the renderer works in restricted environments.

## Why both `.mmd` and `.png`?

- **`.mmd`** = diagrams-as-code. Edit once, re-render anywhere. GitHub renders these natively in Markdown.
- **`.png`** = portable. LinkedIn previews, slide decks, and any non-GitHub markdown viewer need a raster image.

GitHub's Markdown renderer also supports Mermaid blocks inline — see the architecture sections in the root `README.md` and `02_dbt/README.md` for the inline versions.
