# Diagram Conventions (Mermaid → PNG → A4)

Rendering: `scripts/render_diagrams.sh <dir>` runs `mmdc -w 1600 -s 2 -b white` with the pinned Chrome. Widths above ~1600 px produce small text on A4; for tall diagrams pass width 1400.

## Layout
- Left-to-right (`flowchart LR`) for request paths and pipelines (≤ 7 boxes wide).
- Top-down (`flowchart TD`) for component diagrams and trees.
- To stack two panels vertically (e.g. a side-by-side scheme comparison), put each in a `subgraph` with `direction LR`, use `flowchart TD` at the top, and add an invisible link between the subgraphs: `W ~~~ D`. Without it Mermaid places them side by side and the text shrinks.
- Keep node labels to ≤ 3 short lines using `<br/>`.

## Styling (consistent across the family)
```
classDef store fill:#eef3f8,stroke:#3b5b7a,color:#1b2a3a     %% databases, caches, logs
classDef idx   fill:#e3f0e3,stroke:#3a7d44,color:#123a1a     %% index/serving partitions, terminal nodes
classDef agg   fill:#fff7e0,stroke:#c99a2e,color:#3a2e0c     %% aggregators, notes/annotations
```
Cylinders `[( )]` for stores; circles `(( ))` for tree nodes; dotted edges `-.->` for cache-miss / replenish / annotation links.

## What to draw (minimum per guide)
1. Main architecture (read path).
2. Build / write pipeline when it differs from the read path.
3. One structural illustration of the core idea: a trie with cached top-k lists; word- vs. document-sharding query execution; geohash grid with the boundary problem; fan-out on write vs. read.

Reference PNGs from the markdown as `![caption](diagrams/name.png)` and follow each with an italic one-line caption explaining any legend (e.g. "✱ = terminal node with frequency").

## QA
View each PNG once after rendering. Common fixes: swap TB→TD with `~~~` spacers when subgraphs go sideways; shorten labels that wrap into four lines; reduce width for tall trees.
