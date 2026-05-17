# HNSW Part 1: How HNSW Builds the Index

## Overview

- **Topic**: HNSW Index Construction (Node Insertion)
- **Hook**: _"Every nearest-neighbor search you've ever done secretly relies on a graph that was built in a surprisingly clever way. Let's watch it happen."_
- **Visual Metaphor**: A 3D stacked structure where new nodes find their layers and carve out optimized connection pathways.
- **Estimated Length**: ~85 seconds
- **Key Insight**: Layer assignment is random and logarithmic, while connection establishment uses a diversity-promoting heuristic — not simple proximity — to keep the graph navigable.

## Narrative Arc

We start by showing _why_ HNSW needs a multi-layer structure (the hook), then witness a single new node being born: it is randomly assigned a layer, navigates downward to find its neighborhood, and establishes connections using a diversity heuristic. The "aha moment" lands in Scene 4, when a naive connection is rejected in favor of a less-obvious but far more useful one.

---

## Scene 1: Introduction to Stacked Layers

**Duration**: ~10 seconds
**Purpose**: Ground the viewer — establish the multi-layer world before anything moves.

### Visual Elements

- A 3D perspective showing three semi-transparent rectangular planes stacked vertically:
  - **Layer 2 (Top)**: Very sparse, dark purple tint.
  - **Layer 1 (Middle)**: Coarse, dark indigo tint.
  - **Layer 0 (Bottom)**: Dense base layer, deep slate tint.
- A few existing points and edges shown on each layer, with vertical dashed lines connecting duplicate nodes across layers (e.g. node "E" exists on L2, L1, L0).
- Layer labels ("L2 — Sparse", "L1 — Medium", "L0 — Dense") fade in one at a time.

### Content

Establish that HNSW maintains a multi-layer index. Higher layers are sparse "expressways"; the bottom layer contains all elements.

### Narration Notes

> _"HNSW organizes its data into layers. Think of them as maps at different scales — a highway map at the top, a street map at the bottom. Every element lives on Layer 0, but only a lucky few reach higher layers."_

Tone: calm, orienting. Let the visuals breathe — don't rush through the layer labels.

---

## Scene 2: Layer Selection via Exponential Decay

**Duration**: ~12 seconds
**Purpose**: Animate the random level assignment formula — make the "logarithmic sparsity" feel inevitable.

### Visual Elements

- A new glowing gold node **"N"** appears above the stack.
- Formula displayed on the left, built term by term:
  $$L_{\max} = \left\lfloor -\ln(\text{uniform}(0,1)) \cdot m_L \right\rfloor$$
- A side probability bar animates along an exponential decay curve; most of the area is near zero.
- The bar stops at **Layer 1**. Node **N** gets labeled "Max Layer = 1" and descends to hover above Layer 1.

### Content

HNSW uses an exponential decay function to assign the maximum layer for a new node. Most nodes land on Layer 0; exponentially fewer reach higher layers. This keeps search logarithmic.

### Narration Notes

> _"When a new element arrives, HNSW rolls the dice — but it's a loaded die. The exponential decay formula means most elements stay on Layer 0. Our node N is lucky: it makes it to Layer 1."_

Pause briefly after the bar stops to let the "loaded die" metaphor settle.

---

## Scene 3: Greedy Traversal Down to Max Layer

**Duration**: ~12 seconds
**Purpose**: Show the top-down routing that finds the insertion entry point — fast and purposeful.

### Visual Elements

- Searcher starts at the entry point on Layer 2, performs a quick greedy walk (2–3 hops, probes shown briefly as thin lines).
- Lands on the local minimum on Layer 2.
- A vertical dashed line projects downward; the searcher "dives" and lands on the corresponding node on Layer 1 — now glowing as the entry point.

### Content

To insert N, we start from the very top layer and greedily walk toward N's location. The local minimum becomes the entry point for the actual insertion below.

### Narration Notes

> _"Before we can connect our node, we need to find where it belongs. Starting at the top, we greedily walk toward N — not to find its neighbors yet, just to get close. Once we hit a dead end, we drop to Layer 1 and begin the real work."_

Keep this scene brisk — the greedy walk is not the insight, it's the setup.

---

## Scene 4: Connection & Heuristic on Layer 1

**Duration**: ~25 seconds
**Purpose**: The core "aha moment" — why naive proximity fails and diversity wins.

### Visual Elements

- Node **N** is placed on Layer 1 at its coordinates.
- Probe lines radiate from the entry point; a candidate list of size $ef_{\text{construction}}$ appears on the side.
- **Split-screen comparison** (left vs. right, or sequential highlight):
  - **Left — Naive Proximity**: Connects to the $M$ closest nodes. Three clustered edges drawn, all pointing into a tight group. Label: _"All edges point the same direction"_.
  - **Right — Heuristic Selection**: Iterates candidates. One close candidate is shown being rejected (edge turns red, fades) because it is nearer to an already-connected neighbor than to N. A slightly farther candidate is then _accepted_ (edge glows emerald) because it opens a new direction.
- The accepted edges solidify in Emerald Green.

### Content

The diversity heuristic is what separates HNSW from a simple k-NN graph. Redundant neighbors clustered in one direction are skipped; diverse neighbors that bridge different regions are preferred.

### Narration Notes

> _"Here's the clever part. The obvious approach is to just connect to the M closest nodes — but watch what happens. All the edges point in the same direction, creating a dead-end cluster. Instead, HNSW asks: does this candidate add something new? If it's closer to a node we've already connected than to N itself, we skip it. The result is a graph that actually lets you navigate the space."_

This scene carries the most explanatory weight. **Slow down at the rejection moment** — pause ~0.5s after the red fade so the viewer registers _why_ that candidate was skipped.

### Technical Notes

- Use a `SurroundingRectangle` or a subtle background color split to delineate naive vs. heuristic visually.
- The rejection animation: draw the dashed edge, flash it red, then use `FadeOut` — don't just skip it.
- The acceptance animation: draw solid edge with `GrowFromPoint`, then `set_color` to emerald with a brief `Flash`.
- Candidate queue on the side: a simple `VGroup` of labeled dots with a highlighted "top" element works well.

---

## Scene 5: Connection on Layer 0 & Edge Pruning

**Duration**: ~15 seconds
**Purpose**: Complete the insertion, and show that pruning is the same heuristic applied in reverse.

### Visual Elements

- Searcher projects down to Layer 0 (brief vertical dive animation).
- Candidate search runs — faster than Scene 4, implying the algorithm is now routine.
- Connections made to $M_0$ nodes in emerald.
- One existing neighbor now shows $M+1$ connections (highlight it in amber).
- **Pruning**: one of its redundant edges turns red, cracks/breaks, and fades.
- The full stack of layers glows for a moment — all layers, all connections, unified.

### Content

Layer 0 follows the same process but with a larger $M_0$. When an existing node exceeds its edge budget, the same diversity heuristic prunes the weakest link — maintaining navigability as the graph grows.

### Narration Notes

> _"We drop to the base layer and repeat. More neighbors, same heuristic. But here's one last detail: if any existing node now has too many connections, HNSW prunes the least useful one using the exact same diversity logic. The graph stays bounded and navigable — no matter how many elements we insert."_

End on the unified glow — let the viewer feel the completeness of the structure.

---

## Transitions & Flow

- **Scene 1 → 2**: Node N materializes above the already-lit stack — continuity preserved.
- **Scene 2 → 3**: N descends toward Layer 1; the searcher appears at the top layer simultaneously, bridging the cut.
- **Scene 3 → 4**: The "dive" lands the searcher at Layer 1 and N drops into place — same moment, no cut needed.
- **Scene 4 → 5**: Fade the Layer 1 candidate queue out; the dive downward mirrors Scene 3's dive for visual rhythm.
- **Recurring motif**: The vertical dashed "projection line" used in Scenes 3 and 5 reinforces that layers are the same space at different scales.

---

## Design Aesthetic

- **Background**: `#05070D` (Deep Dark Blue)
- **Planes**: Semi-transparent Slate/Indigo (`#1E293B` / `#312E81`) with white borders.
- **New Node N**: `#FBBF24` (Golden Amber) — the protagonist; always distinct.
- **Searcher/Entry Point**: `#A78BFA` (Violet) — separate identity from N.
- **Accepted Edges**: `#10B981` (Emerald) — positive outcome.
- **Rejected/Pruned Edges**: `#EF4444` (Rose Red) — negative outcome.
- **Existing Graph**: White nodes, grey edges — neutral background actors.
- **Candidate Queue**: Amber-tinted panel on the right viewport edge.

## Implementation Order

1. **Scene 1** — Static; build the layer geometry first. All other scenes depend on this layout.
2. **Scene 2** — Self-contained; implement the exponential bar independently.
3. **Scene 3** — Requires the greedy walk logic (reusable in Scene 4).
4. **Scene 4** — Core scene; implement last so the greedy walk and heuristic rejection logic are polished.
5. **Scene 5** — Reuses Scene 4 logic; add the pruning animation as the only new element.
