# HNSW Part 3: How Hyperparameters Change Everything

## Overview

- **Topic**: HNSW Hyperparameters ($M$, $ef_{\text{construction}}$, $ef_{\text{search}}$)
- **Hook**: _"You could run HNSW right out of the box — but the defaults are just a starting point. Two numbers control everything: how the graph is wired, and how aggressively it searches. Change them, and you get a completely different algorithm."_
- **Visual Metaphor**: Two side-by-side arenas where changing a single dial visibly rewires the graph and reshapes the search path.
- **Estimated Length**: ~85 seconds
- **Key Insight**: $M$ shapes the physical highway grid (recall vs. memory); $ef$ expands the search beam (recall vs. speed), allowing the algorithm to escape local minima it would otherwise get stuck in.

## Narrative Arc

We start with a quick "dashboard" framing to name the controls, then run two back-to-back experiments. First: the same dataset, same query, two graphs wired with different $M$ — the sparse one gets trapped, the dense one flies. Second: the same crescent-barrier problem, two search modes — $ef=1$ hits a wall and stops dead, $ef=4$ holds its nerve, backtracks through the queue, and slips around the obstacle. The summary table then lets those lessons crystallize.

---

## Scene 1: Parameter Overview (The Dashboard)

**Duration**: ~10 seconds
**Purpose**: Name the controls before touching them — give the viewer a mental model of what's adjustable.

### Visual Elements

- A minimal "control panel" layout: two clearly labeled dials or sliders.
  1. **$M$ (Max Connections per Node)**: slider showing range 2–64, resting at `M = 4`.
  2. **$ef$ (Candidate Queue Size)**: two sub-labels (`efConstruction` for build, `efSearch` for query), slider resting at `ef = 10`.
- Brief single-line definitions appear next to each dial as they highlight:
  - _"M → how many edges each node can have"_
  - _"ef → how wide the search beam is"_

### Content

HNSW's behavior is governed by two parameters. $M$ controls how densely connected the graph is when it's built. $ef$ controls how much effort the search spends exploring candidates. Tune them, and you trade memory, build time, and search latency against recall accuracy.

### Narration Notes

> _"HNSW has two primary tuning knobs. M controls how many connections each node can make — it determines the shape of the graph. ef controls how wide a net the search casts — it determines how thoroughly we explore. Let's see what happens when we pull each one."_

Keep this scene tight and visual — the definitions should be shown, not read out in full. The sliders are a visual promise: "we're going to move these."

---

## Scene 2: The $M$ Parameter — Edge Density & Shortcuts

**Duration**: ~20 seconds
**Purpose**: Make the cost of sparsity _visible_ — a trapped searcher is far more memorable than a definition.

### Visual Elements

- Split-screen layout (left/right, separated by a thin divider):
  - **Left**: labeled `"Low M  (M = 2)"` — sparse graph, at most 2 connections per node.
  - **Right**: labeled `"High M  (M = 6)"` — dense graph, many triangles and long-range edges.
- Both screens display the **same 15 data points**, same coordinates, same Rose Red query point Q.
- Search runs simultaneously on both screens, starting from the same entry node:
  - **Left (M = 2)**: Searcher winds along a long chain, 6 hops, ends stuck at a local minimum far from Q. A red dotted warning ring pulses. Label: _"Trapped — Recall Failure"_.
  - **Right (M = 6)**: Searcher jumps a long-range edge in a single hop, 2 steps total, lands on the true nearest neighbor. A green lock-on ring. Label: _"Success — 2 steps"_.
- After both searches complete, the two paths remain visible side-by-side for comparison.
- A brief annotation: _"Same data. Same query. Different graph."_

### Content

$M$ defines how many connections each node can form. A sparse graph (low $M$) uses less memory but creates isolated neighborhoods — the searcher can get trapped. A dense graph (high $M$) builds long-range shortcuts that let the searcher leap directly toward the target at the cost of more memory and slower edge checks.

### Narration Notes

> _"Same data. Same query. Different M. Watch carefully. Low M — the searcher inches along, then gets stuck. It never finds the closest point. High M — one long jump, and it's done. Those long-range edges are the shortcuts that make HNSW fast."_

The "Same data. Same query. Different graph." annotation is the scene's punchline — fade it in _after_ both searches finish, not during. Pause ~0.8s on it before transitioning.

---

## Scene 3: The $ef$ Parameter — Greedy vs. Beam Search

**Duration**: ~25 seconds
**Purpose**: The most nuanced scene — show concretely how a priority queue escapes a local minimum that a greedy search cannot.

### Visual Elements

- Split-screen layout (same format as Scene 2):
  - **Left**: `"Greedy Search  (efSearch = 1)"`
  - **Right**: `"Beam Search  (efSearch = 4)"`
- Both graphs are **identical**: a crescent arc of nodes forms a concave "barrier" between the entry point and the true nearest neighbor Q (which sits in the cavity behind the arc).
- **Left (ef = 1)**:
  - Searcher advances toward the crescent, probing neighbors.
  - Hits the center of the arc: all probes turn Red (every neighbor is farther from Q).
  - Search halts immediately. Red pulsing warning ring. Label: _"Stuck — Local Minimum"_.
- **Right (ef = 4)**:
  - A live **Candidate Queue** panel appears on the right edge of the right window:
    ```
    Queue (sorted by dist to Q):
    ▶ [A: 1.1]  [B: 1.4]  [C: 1.8]  [D: 2.1]
    ```
  - As the searcher moves, nodes are pushed onto the queue (animate items sliding in).
  - Searcher also hits the crescent wall — but the queue still has candidates.
  - The algorithm pops **B** (next best). An alternate branch shoots from B, bypasses the crescent edge, and steps to the true nearest neighbor.
  - Queue updates: Q's node appears at the top, turns Emerald. Label: _"True Nearest Neighbor Found"_.

### Content

$ef$ controls the size of the candidate priority queue during search. With $ef=1$, the search is strictly greedy: one candidate at a time, stops the moment it hits a dead end. With $ef=4$, the algorithm maintains a live sorted list of candidates — when it hits a wall, it backtracks to the next-best unexplored node and tries a different path. This is the difference between getting stuck and finding the truth.

### Narration Notes

> _"Now the harder one. Both graphs are identical — but one searches greedily, one uses a priority queue. The greedy searcher hits the crescent wall and gives up. The beam searcher? It hits the same wall — but it still has other candidates queued up. It backtracks, tries a different branch, and slips around the obstacle to find the real answer."_

The critical visual moment is the **backtrack** — when the right-side searcher pops from the queue and takes the alternate branch. Slow this animation down (1.5–2s) and highlight the queue item being popped so the viewer can follow the logic.

### Technical Notes

- The queue UI panel: use a `VGroup` of `RoundedRectangle` + `Text` items. On each step, animate `items.shift()` (pop from top) and `items.append()` (push new candidate) using `Transform` and `FadeIn` — the queue should feel live, not static.
- Color-code queue items by distance: closest = Emerald tint, middle = neutral, furthest = faint grey.
- The "crescent barrier" graph: arrange ~5–6 nodes in a concave arc. The true nearest neighbor Q should be visually inside the concavity, clearly "behind" the wall when viewed from the entry side.
- Run both sides in parallel using `AnimationGroup` or careful `add_sound`-style timing so the comparison lands at the same visual beat.
- The branch that escapes the crescent: draw it with `GrowFromPoint` starting from the popped queue node — make it feel like a new decision being made, not a pre-drawn path.

---

## Scene 4: Conclusion — The Trade-off Table

**Duration**: ~12 seconds
**Purpose**: Let the lessons from Scenes 2 and 3 crystallize into a reference the viewer can remember.

### Visual Elements

- The split-screen dissolves; a full-width glassmorphic summary table fades in:

| Parameter                      | Increase ↑                                                | Decrease ↓                                                  |
| :----------------------------- | :-------------------------------------------------------- | :---------------------------------------------------------- |
| **$M$**                        | ✓ Higher Recall, Faster Search &nbsp;&nbsp; ✗ More Memory | ✓ Less Memory &nbsp;&nbsp; ✗ Lower Recall, Trapped Searches |
| **$ef_{\text{construction}}$** | ✓ Better Graph Quality &nbsp;&nbsp; ✗ Slower Build Time   | ✓ Faster Indexing &nbsp;&nbsp; ✗ Weaker Graph Structure     |
| **$ef_{\text{search}}$**       | ✓ Higher Recall &nbsp;&nbsp; ✗ Higher Latency             | ✓ Faster Latency &nbsp;&nbsp; ✗ Lower Recall, Local Minima  |

- Each row highlights sequentially (the row glows as the narration covers it), not all at once.
- After the table is fully shown, a final text fades in at the bottom:
  _"HNSW's genius is that these trade-offs are tunable — not fixed."_

### Content

Three parameters, three trade-off axes: recall vs. memory ($M$), graph quality vs. build speed ($ef_{\text{construction}}$), and recall vs. search latency ($ef_{\text{search}}$). Together they make HNSW configurable for any workload — from a low-latency cache to a high-precision retrieval engine.

### Narration Notes

> _"Three numbers. Three trade-offs. M gives you the graph's skeleton. efConstruction determines how carefully it was built. efSearch determines how hard it tries when you query it. Tune them together, and HNSW can be anything from a near-instant approximation engine to a high-precision retrieval system."_

Highlight each table row as it's named in narration — the sequential glow prevents the viewer from reading ahead. The closing line is the video's true ending: let it sit on screen for ~1.5s before fade-out.

---

## Transitions & Flow

- **Scene 1 → 2**: The dashboard sliders animate — the $M$ slider moves to `M=2` on the left and `M=6` on the right simultaneously, then the split-screen unfolds. The slider motion is the visual trigger.
- **Scene 2 → 3**: The "Same data. Same query. Different graph." annotation fades out; the $ef$ slider on the dashboard briefly flashes as the new split-screen fades in — consistent with Scene 1→2.
- **Scene 3 → 4**: Both split-screen windows shrink toward center and dissolve into the summary table, which expands to fill the frame. The motion gives a sense of "collapsing the comparison into a rule."
- **Recurring motif**: The split-screen divider is the visual anchor for this video. Appearing in Scenes 2 and 3, it signals "we're comparing" — its disappearance in Scene 4 signals "we're concluding."

---

## Design Aesthetic

- **Background**: `#05070D` (Deep Dark Blue)
- **Query Point Q**: `#FF5A5F` (Rose Red) with pulsing aura — consistent with Parts 1 & 2.
- **Searcher**: `#A78BFA` (Violet) — consistent with Part 2.
- **Success Highlight**: `#10B981` (Emerald Green) glow and lock-on ring.
- **Failure Highlight**: `#EF4444` (Rose Red) dotted warning ring.
- **Crescent Barrier Nodes**: `#64748B` (Slate Grey) — visually "blocking."
- **Queue UI Panel**: Semi-transparent `#0F172A` background, white border, items color-coded Emerald (close) → Grey (far).
- **Split-Screen Divider**: Thin `#334155` vertical line with a subtle glow.
- **Summary Table**: Glassmorphic `#1E293B` background, `#10B981` for ✓ items, `#EF4444` for ✗ items.

## Implementation Order

1. **Scene 2** — Implement the split-screen greedy walk first; it's structurally simpler and establishes the comparison layout all scenes use.
2. **Scene 3** — Implement the queue UI next; this is the most complex element. Build and test it in isolation before integrating into the split-screen.
3. **Scene 1** — Implement the dashboard last among the "content" scenes; it needs to know what the sliders animate _toward_ (Scenes 2 and 3 values).
4. **Scene 4** — Implement the table after all content scenes; row-highlight timing depends on knowing the final narration pacing.
