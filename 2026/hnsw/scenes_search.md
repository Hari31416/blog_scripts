# HNSW Part 2: How HNSW Searches

## Overview

- **Topic**: HNSW Vector Search (Hierarchical Greedy Search)
- **Hook**: _"Searching a million points sounds like it should take a million steps. HNSW does it in a handful — by navigating a series of progressively detailed maps."_
- **Visual Metaphor**: A multi-scale map where the camera zooms into denser and denser regions to find a specific target.
- **Estimated Length**: ~80 seconds
- **Key Insight**: Hierarchical search turns a flat O(N) scan into a multi-layer navigation problem — each layer narrows the search space so that the final dense-layer walk is tiny.

## Narrative Arc

We begin zoomed out on a sparse world, chasing a query point using nothing but greedy local decisions. Each time we hit a dead end, we don't give up — we zoom in and find the world has more detail. By the time we reach the base layer, we're already so close that the final walk is just a few steps. The payoff is not just that we found the answer, but _how few steps it took_.

---

## Scene 1: The Sparse Top Layer (L2)

**Duration**: ~12 seconds
**Purpose**: Introduce the greedy walk and build intuition for what "local minimum" means before the layers complicate things.

### Visual Elements

- Camera starts zoomed out, displaying a sparse graph (Layer 2) with few nodes and long-range edges.
- A bright Rose Red **"Query Point"** Q pulses at a fixed location.
- A glowing Violet **"Searcher"** cursor starts at node **"A"** (entry point), labeled "Entry Point".
- Probe lines shoot from the searcher to its neighbors:
  - **Emerald Green** for nodes closer to Q than the current position.
  - **Rose Red** for nodes farther from Q.
- Searcher steps: **A → D → E**. At **"E"**, all probes turn Red — no neighbor is closer. Label: _"Local Minimum on L2"_.

### Content

Search begins at the top layer. We greedily walk: check all neighbors, step to the closest one to the query. Repeat until stuck. This is fast because Layer 2 is sparse — we only check a handful of nodes total.

### Narration Notes

> _"Search starts at the top, where the graph is sparse. From our entry point, we check neighbors and always step toward the query. Within just a few hops, we're stuck — no neighbor is closer. On a normal graph, this would be where we give up. But HNSW has a trick."_

Keep the probe animation crisp and quick — this scene should feel fast, almost effortless, to contrast with what a full linear scan would look like.

---

## Scene 2: The First Dive (Zoom to L1)

**Duration**: ~10 seconds
**Purpose**: The signature visual of this video — the camera zoom that reveals a hidden, denser world.

### Visual Elements

- Searcher settles on node **"E"**. A subtle "lock-on" ring appears around it.
- A glassmorphic status bar at top updates: `"Diving to Layer 1..."`.
- The camera performs a smooth, exponential zoom-in centered on node **"E"**.
- As the camera zooms: Layer 2 graph fades out, Layer 1 graph fades in. Node **"E"** stays anchored at the same screen position throughout.
- After the zoom settles, **"E"** is surrounded by new neighbors and edges that weren't visible before.

### Content

Hitting a local minimum on a higher layer is not a failure — it's the signal to zoom in. Layer 1 is the same space but with more detail, and node **"E"** is our refined starting point.

### Narration Notes

> _"Instead of stopping, we dive. The camera zooms in — and suddenly the world has more detail. Layer 1 is denser. More connections. And our local minimum E is now surrounded by nodes we couldn't see before."_

The zoom should feel dramatic — like pulling focus on a camera. Let it breathe for ~0.5s after settling before the searcher starts moving again.

### Technical Notes

- The zoom is the most visually critical animation in the video. Use `self.camera.frame.animate.scale(0.35).move_to(node_E.get_center())` for a smooth exponential feel.
- Layer transition: use `FadeOut(layer2_group, run_time=1.5)` and `FadeIn(layer1_group, run_time=1.5)` synchronized with the zoom, not after.
- Node **"E"** must exist in both `layer2_group` and `layer1_group` at the same coordinates — keep it visible throughout (do not include it in the fade groups).
- Scale all stroke widths and dot radii inversely to the camera zoom so visual weight remains consistent.

---

## Scene 3: Refinement on Layer 1

**Duration**: ~10 seconds
**Purpose**: Show that the greedy walk is identical — the only difference is more nodes, shorter steps.

### Visual Elements

- Status bar updates: `"Searching Layer 1"`.
- Searcher checks neighbors of **"E"** on Layer 1 (more probes than Scene 1, tighter spacing).
- Greedy steps: **E → H → I → K**. Node **"K"** identified as the new local minimum. Label: _"Local Minimum on L1"_.

### Content

The algorithm is exactly the same as Scene 1. The denser graph means shorter steps and a much more precise position — we end up significantly closer to the query than we were on Layer 2.

### Narration Notes

> _"Same algorithm, denser map. We walk again — and this time, with more nodes to step through, we get much closer. K is our new best guess. And we're not done yet."_

This scene should be fast — it's the middle beat. Reuse the same probe animation rhythm from Scene 1 to reinforce that the algorithm hasn't changed.

---

## Scene 4: The Final Dive (Zoom to L0)

**Duration**: ~15 seconds
**Purpose**: The climactic zoom — the base layer, the densest world, and the final greedy walk to the true nearest neighbor.

### Visual Elements

- Status bar updates: `"Final Dive: Layer 0 (Dense)"`.
- Another dramatic zoom-in centered on node **"K"** — more extreme than Scene 2's zoom.
- Layer 1 fades out; an extremely dense Layer 0 fades in.
- The searcher performs the final walk: **K → R → P**.
- At node **"P"**: all probes turn Red. A lock-on ring expands from **"P"**. Label: _"True Nearest Neighbor"_.
- A faint distance line draws from **"P"** to **Q** (the query point) — shortest of all.

### Content

The final dive reaches Layer 0 — the complete dataset. Starting from K, which is already very close, the walk to the true nearest neighbor is just two steps. This is the payoff of all the hierarchical work above.

### Narration Notes

> _"One more dive — the deepest one. Now we're in the full dataset. But because we spent the earlier layers getting close, we only need two more steps to find the true nearest neighbor. P is it."_

Pause on the lock-on ring for ~0.8s. This is the visual resolution — let the viewer feel it before moving to the conclusion.

---

## Scene 5: Conclusion — The Path Replay

**Duration**: ~10 seconds
**Purpose**: Zoom back out and show the full search path as a unified story, then land the complexity claim.

### Visual Elements

- Camera smoothly zooms back out to the original full-stack view (all three layers visible).
- A traced path overlays all three layers: the hops on L2, the hops on L1, and the hops on L0, each in a distinct color (e.g., purple, indigo, white).
- Total hop count displayed: e.g., _"3 + 4 + 2 = 9 hops"_.
- Contrast label appears: _"Linear scan: 1,000,000 comparisons"_.
- Bottom-right label pulses in: `"O(log N) complexity"`.

### Content

We found the true nearest neighbor in just 9 hops across all layers. A brute-force linear scan of the same dataset would require millions of comparisons. That's the power of hierarchical navigation.

### Narration Notes

> _"Zoom back out. Here's everything we did — a handful of steps on each layer. Nine total hops to search a million points. That's not a trick; that's the geometry of a well-built graph working exactly as intended."_

The contrast label is the emotional punchline. Fade it in slowly after the hop count — don't show both at the same time.

### Technical Notes

- The zoom-out should mirror the zoom-in rhythm from Scenes 2 and 4 (same easing, reversed) to give the video visual symmetry.
- Use `TracedPath` or manually drawn `Line` objects for the path replay — color-coded per layer helps viewers track which hops happened at which scale.
- The hop count display: animate each term (`3 +`, `4 +`, `2 =`, `9 hops`) writing in sequence using `Write` or `AddTextLetterByLetter`.

---

## Transitions & Flow

- **Scene 1 → 2**: The lock-on ring on **"E"** triggers the zoom — the visual cause-and-effect is clear.
- **Scene 2 → 3**: Zoom settles, then the searcher immediately activates. No hard cut — motion is continuous.
- **Scene 3 → 4**: Mirrors Scene 1 → 2 exactly (lock-on on K → zoom) — the repetition teaches the pattern.
- **Scene 4 → 5**: Lock-on on **"P"**, then camera reverses out. The reversal feels earned precisely because the viewer has seen two zooms in.
- **Recurring motif**: The zoom-in/out is the visual heartbeat of this video. Each zoom should use the same easing curve for consistency.

---

## UI Components (Fixed in Viewport)

- **Status Bar**: Top glassmorphic panel — updates at the start of each scene. Keeps viewers oriented across layer transitions.
- **Complexity Label**: Bottom-right panel — appears only in Scene 5, so it feels like a reveal.

---

## Design Aesthetic

- **Background**: `#05070D` (Deep Dark Blue)
- **Query Point Q**: `#FF5A5F` (Rose Red) with a pulsing aura — the destination, always visible.
- **Searcher**: `#A78BFA` (Violet) ring and core — the agent navigating the layers.
- **Path Trace**: Violet trail left behind the searcher.
- **Probe Lines**: `#22C55E` (Emerald Green) for closer, `#EF4444` (Rose Red) for farther.
- **Layer 2 Graph**: `#C7D2FE` nodes, `#6B7280` edges — lightest, most distant.
- **Layer 1 Graph**: `#E5E7EB` nodes, `#64748B` edges — medium weight.
- **Layer 0 Graph**: `#FFFFFF` nodes, `#475569` edges — sharpest, most present.
- **Path Replay Colors**: Purple (L2 hops), Indigo (L1 hops), White (L0 hops).

## Implementation Order

1. **Scene 1** — Implement the greedy walk logic first; it is reused in Scenes 3 and 4.
2. **Scene 3** — Same as Scene 1, different graph density. Reuse directly.
3. **Scene 4** — Same again; add the lock-on ring and final labeling.
4. **Scene 2** — Implement the zoom transition after the walk logic is stable; it's the riskiest animation.
5. **Scene 5** — Implement last; depends on having correct hop counts and the path trace positions from all prior scenes.
