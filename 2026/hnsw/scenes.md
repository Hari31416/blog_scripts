# HNSW: Hierarchical Navigable Small Worlds (2D Zooming Version)

## Overview
- **Topic**: HNSW Vector Search
- **Visual Metaphor**: A multi-scale map where we zoom into denser and denser regions to find a specific target.
- **Key Insight**: Hierarchical search turns an exhaustive 2D search into a multi-layered navigation problem, optimized by jumping between scales.

## Narrative Arc
The animation uses a 2D "world" that contains all layers. We start at a bird's-eye view with a sparse graph. As we find local optima, the camera "dives" into the map, revealing more detailed layers of data points until we hit the base layer and find the exact nearest neighbor.

---

## Scene 1: The Sparse Top Layer (L2)
**Duration**: 8 seconds
**Purpose**: Introduce the entry point.

### Visual Elements
- A sparse graph (L2) with few nodes and long edges.
- A bright red "Query Point" as the target.
- A "Searcher" cursor starting at an entry point.

### Content
Perform a greedy search. Show neighbor checks with color-coded lines (Green for closer, Red for further). The searcher moves to the best node in this coarse resolution.

---

## Scene 2: The First Dive (Zoom to L1)
**Duration**: 6 seconds
**Purpose**: Show the refinement process.

### Visual Elements
- The camera zooms in on the current best node.
- **Transition**: L2 graph fades out as the denser L1 graph fades in.
- The dots and lines maintain their visual weight (vector-style zoom).

### Content
"Zooming to Layer 1..." status appears. The searcher is now at the exact same location in a much denser neighborhood.

---

## Scene 3: Refinement on Layer 1
**Duration**: 8 seconds
**Purpose**: Medium-scale optimization.

### Visual Elements
- The searcher checks neighbors in the L1 graph.
- More steps are taken as the density is higher.

---

## Scene 4: The Final Dive (Zoom to L0)
**Duration**: 10 seconds
**Purpose**: Reaching the base data.

### Visual Elements
- Another dramatic zoom-in.
- L1 fades out, L0 (the complete dataset) fades in.
- The space is now very dense with points.

### Content
"Final Zoom: Layer 0 (Dense)" status. The searcher performs the final greedy steps to land on the absolute nearest neighbor.

---

## Scene 5: Conclusion
**Duration**: 5 seconds
**Purpose**: Highlight complexity.

### Visual Elements
- The final nearest neighbor glows and scales up.
- The complexity text appears: "O(log N) Search Complexity".

---

## UI Components (Fixed in Viewport)
- **Status Bar**: A top bar that updates with the current phase (e.g., "Searching Layer 2", "Zooming to Layer 1").
- **Labels**: Complexity label in the bottom corner.

## Design Aesthetic
- **Points**: White dots on a deep black background.
- **Zooming**: Smooth camera transitions using `MovingCameraScene`.
- **Closeness Logic**: Dynamic line colors during greedy search to show distance metrics.
