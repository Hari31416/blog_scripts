# Storyboard: Visualizing Traditional Information Retrieval Metrics

## Overview

- **Topic**: Traditional Information Retrieval (IR) Metrics (Hit Rate, Precision, Recall, MRR, MAP, NDCG)
- **Hook**: A query vector is shot into a database, returning a list of documents. How do we mathematically score whether this list is "good" or "bad"?
- **Target Audience**: Data scientists and developers who are somewhat familiar with search or RAG, looking for a clear, visual intuition of evaluation metrics.
- **Estimated Length**: ~180 seconds (3 minutes)
- **Key Insight**: Different search tasks need different math. Binary metrics count relevance, ranking metrics penalize position, and graded metrics recognize nuance.

## Narrative Arc

We start with a simple search query returning a ranked list of items. We first look at binary, position-insensitive metrics (Precision, Recall, Hit Rate), show their limitations, and transition to position-aware ranking metrics (MRR, MAP). Finally, we move from simple binary relevance (relevant vs. irrelevant) to graded relevance with NDCG, culminating in a clear summary table of when to use each.

---

## Scene 1: Introduction (The Ranked List)

**Duration**: ~20 seconds
**Purpose**: Hook the viewer and establish the core visual metaphor of the ranked document stack.

### Visual Elements

- **Query Input**: A search box at the top labeled "Query $Q$". An arrow shoots a rose-red vector (`#FF5A5F`) down from it.
- **Document Stack**: A vertical column of 5 slots labeled with ranks 1 to 5.
- **Relevance Indicators**: Document cards fall into these slots and turn Emerald Green (`#10B981`) with a checkmark for relevant, or Slate Gray (`#64748B`) with a cross for irrelevant.
  - Final state: Rank 1 (Green), Rank 2 (Slate), Rank 3 (Green), Rank 4 (Slate), Rank 5 (Green).

### Content

Show a query being processed, returning a list of results. Some are good, some are bad. The narrator introduces the core challenge: search lists have _order_ and _varying relevance_. We need to measure quality mathematically.

### Narration Notes

- **Tone**: Conversational, intriguing.
- **Script**: "When you ask a search engine or a RAG system a question, it hands you a ranked list of documents. Some are exactly what you wanted, others are useless noise. But how do we mathematically score this list to know if our retriever is actually doing a good job?"

### Technical Notes

- Use `Rectangle` for document cards, grouping them inside a `VGroup`.
- Apply `FadeIn` and `DownArrow` animations to simulate retrieval.
- Use `Transform` to turn generic gray boxes into emerald green or slate cards once they are "evaluated".

---

## Scene 2: Precision@K and Recall@K (The Binary Foundation)

**Duration**: ~35 seconds
**Purpose**: Explain Precision and Recall at rank $K$, highlighting that they do not care about rank order.

### Visual Elements

- **Retrieval Stack**: Keep the same 5-slot stack from Scene 1 ($K=5$). 3 are green (relevant), 2 are slate (irrelevant).
- **Database Pool**: A cloud/group of 6 green document cards off to the side, representing "All 6 Relevant Documents in Database."
- **Precision Formula**:
  $$\text{Precision@5} = \frac{\text{Relevant in Top } 5}{5}$$
  - Highlights: The numerator "3" glows green, and the 3 green cards in the stack glow green. The denominator "5" highlights the entire stack container.
  - Shows value: $3 / 5 = 0.60$ ($60\%$).
- **Recall Formula**:
  $$\text{Recall@5} = \frac{\text{Relevant in Top } 5}{\text{Total Relevant}}$$
  - Highlights: Numerator "3" glows. The denominator "6" glows, highlighting the 6 database pool cards.
  - Shows value: $3 / 6 = 0.50$ ($50\%$).
- **Order Insensitivity Demo**: Shuffle the cards in the stack (e.g., move green cards to the bottom ranks 4 and 5). Show that the Precision and Recall values remain exactly the same.

### Content

Define Precision as quality (purity) and Recall as coverage (completeness). Show the calculations side by side. Demonstrate that shuffling the order of relevant documents does not change the score, setting up the need for rank-aware metrics.

### Narration Notes

- **Tone**: Clear, educational.
- **Script**: "Let's start with the basics: Precision and Recall. Precision at $K$ asks: of the top $K$ items we returned, what fraction is actually relevant? Here, 3 out of 5, or 60%. Recall at $K$ asks: of all the relevant documents out there in the database, what fraction did we capture? Here, we found 3 out of 6, or 50%. But notice a big limitation: if we shuffle these results, putting the irrelevant ones at the top, the scores don't change. These metrics are blind to order."

### Technical Notes

- Use `Indicate` or `Circumscribe` to highlight elements of the stack corresponding to the formulas.
- Use standard `MathTex` for the equations.
- Use `.animate` to smoothly swap positions of the document cards to prove order-insensitivity.

---

## Scene 3: Hit Rate@K (The Needle in the Haystack)

**Duration**: ~15 seconds
**Purpose**: Define Hit Rate@K, a binary query-level success metric common in RAG.

### Visual Elements

- **Three Mini Stacks**: Scale down the stacks and show three queries side-by-side.
  - Query 1: Top 5 has one green card. (Label: "Hit = 1")
  - Query 2: Top 5 has three green cards. (Label: "Hit = 1")
  - Query 3: Top 5 has zero green cards. (Label: "Hit = 0")
- **Average Formula**:
  $$\text{Hit Rate@5} = \frac{1 + 1 + 0}{3} = 0.67$$

### Content

Introduce Hit Rate@K as a binary check: did we get at least one right? Show three query stacks and compute the average hit rate.

### Narration Notes

- **Script**: "If you're building a simple RAG system, sometimes you just need a needle in the haystack. That's Hit Rate at $K$. If the top $K$ results contain at least one relevant document, it's a success, or a 'Hit' of 1. Otherwise, it's 0. It's a quick, binary query-level health check, but it won't tell you if your best results are sitting at the very top."

### Technical Notes

- Create a helper class or method to quickly render scaled-down document lists.
- Write text labels using `Tex` and position them under each stack.

---

## Scene 4: Mean Reciprocal Rank (MRR) (First Match Matters)

**Duration**: ~25 seconds
**Purpose**: Introduce MRR and show how it prioritizes the rank of the _first_ relevant document.

### Visual Elements

- **Two Query Stacks**:
  - **Query A**: Green cards at Rank 3 and 4. (Rank of first relevant is 3). Reciprocal Rank ($\text{RR}$) = $1/3$.
  - **Query B**: Green cards at Rank 1 and 2. (Rank of first relevant is 1). Reciprocal Rank ($\text{RR}$) = $1/1 = 1$.
- **Calculation visual**:
  - For Query A, zoom in on Rank 3. A bracket draws attention to the rank. The other green card at Rank 4 fades out to show it's ignored.
  - For Query B, highlight Rank 1.
  - Show the average calculation:
    $$\text{MRR} = \frac{1/3 + 1}{2} = 0.67$$

### Content

Explain that MRR is designed for search queries where a user only needs a single correct answer (like QA). Walk through finding the first relevant document's rank, taking its reciprocal, and averaging.

### Narration Notes

- **Script**: "For Q&A systems, you only need one correct answer. Mean Reciprocal Rank, or MRR, evaluates this. It looks for the very _first_ relevant document. If it's at rank 3, the score is 1 over 3. If it's at rank 1, it's 1 over 1. We ignore everything after that first hit. Then, we average these reciprocal ranks across all queries."

### Technical Notes

- Set non-first relevant cards to lower opacity (`opacity=0.3`) to visually indicate they are discarded by the metric.
- Use `Brace` to point to the rank index.

---

## Scene 5: Mean Average Precision (MAP) (The Ranking Specialist)

**Duration**: ~35 seconds
**Purpose**: Explain Average Precision (AP) and MAP, demonstrating how they evaluate the position of _all_ relevant documents.

### Visual Elements

- **Evaluation Stack**: A 5-slot stack with relevant cards at Rank 1, Rank 3, and Rank 5.
- **Dynamic Walkthrough**:
  - Arrow points to Rank 1 (Relevant): Calculate Precision@1 = $1/1 = 1.0$. (Glows green).
  - Arrow points to Rank 2 (Irrelevant): Skip.
  - Arrow points to Rank 3 (Relevant): Calculate Precision@3 = $2/3 \approx 0.67$. (Glows green).
  - Arrow points to Rank 4 (Irrelevant): Skip.
  - Arrow points to Rank 5 (Relevant): Calculate Precision@5 = $3/5 = 0.60$. (Glows green).
- **AP Formula**:
  $$\text{AP} = \frac{1.0 + 0.67 + 0.60}{\text{Total Relevant (3)}} \approx 0.76$$
- **Comparison Stack**: Show a second stack where relevant items are pushed down to Rank 4 and Rank 5.
  - Calculate AP: Precision@4 = $1/4 = 0.25$, Precision@5 = $2/5 = 0.40$.
  - $\text{AP} = \frac{0.25 + 0.40}{3} \approx 0.22$.
  - Side-by-side AP values: $0.76$ vs. $0.22$.

### Content

Break down Average Precision (AP) for a single query, showing that we compute precision at each rank where a relevant item occurs, and average them. Then note that MAP is simply the mean of these APs over all queries.

### Narration Notes

- **Script**: "But what if you want _all_ relevant documents, and you want them ranked high? Enter Mean Average Precision, or MAP. To calculate it, we walk down the list. At every rank where we find a relevant document, we compute the precision at that point. Then, we average these precisions. Notice how pushing relevant documents down the list causes our precisions—and our final score—to plummet."

### Technical Notes

- Use a moving arrow indicator (`Arrow` or `Triangle`) that slides down the rank indices, pauses, and flashes when a relevant card is hit.
- Render calculated fractions alongside the stack positions before putting them in the main equation.

---

## Scene 6: Normalized Discounted Cumulative Gain (NDCG) (Graded Relevance)

**Duration**: ~40 seconds
**Purpose**: Explain NDCG intuitively using graded relevance and positional discounting without getting bogged down in complex logarithmic algebra.

### Visual Elements

- **Graded Card Stack**: Change cards from binary (green/gray) to graded cards:
  - Deep Emerald Green (`#10B981`): Score = 3 (Highly Relevant)
  - Light Emerald Green: Score = 1 (Partially Relevant)
  - Slate Gray (`#64748B`): Score = 0 (Irrelevant)
- **Cumulative Gain (CG)**: Show a simple sum of the scores:
  - List order: Rank 1 (3), Rank 2 (0), Rank 3 (1).
  - $\text{CG} = 3 + 0 + 1 = 4$.
- **Discounted Cumulative Gain (DCG)**:
  - Place a "position discount" visual (like a shrinking bar chart or divider) next to each rank.
  - Show the division:
    - Rank 1: $3 / \log_2(2) = 3.0$
    - Rank 2: $0 / \log_2(3) = 0.0$
    - Rank 3: $1 / \log_2(4) = 0.5$
  - $\text{DCG} = 3.0 + 0.0 + 0.5 = 3.5$.
- **Ideal DCG (IDCG)**:
  - The stack cards animate, sorting themselves by score: Rank 1 (3), Rank 2 (1), Rank 3 (0).
  - Show the DCG calculation for this sorted ideal list:
    - Rank 1: $3 / 1 = 3.0$
    - Rank 2: $1 / 1.58 = 0.63$
    - Rank 3: $0 / 2 = 0.0$
    - $\text{IDCG} = 3.63$.
- **NDCG Formula**:
  $$\text{NDCG} = \frac{\text{DCG}}{\text{IDCG}} = \frac{3.5}{3.63} \approx 0.96$$

### Content

Explain that documents aren't just binary; relevance is graded. Introduce CG, apply rank discounting for DCG, and normalize with IDCG to get a score between 0 and 1. Focus on the intuition of dividing by the ideal sorted list.

### Narration Notes

- **Script**: "In the real world, relevance isn't binary. A document can be highly relevant, partially relevant, or completely off-topic. NDCG handles this by using numerical grades. We start by adding these grades up. But then we apply a discount, dividing by a factor that increases with rank, so documents lower down contribute much less to the score. Finally, we normalize this by dividing by the Ideal DCG—the score we would get if our retriever had sorted these same documents in perfect order."

### Technical Notes

- Animate the cards sorting themselves to represent the "Ideal" ordering.
- Use `Transform` or `ReplacementTransform` to change text from `CG` components to `DCG` values.

---

## Scene 7: Outro & Summary (The Choice Matrix)

**Duration**: ~10 seconds
**Purpose**: Provide a quick summary comparison table.

### Visual Elements

- **Comparison Table**: Draw a clean summary matrix table matching metrics to use cases.
  - **Hit Rate / Recall**: "Coverage / Needle in Haystack"
  - **Precision**: "Purity of top results"
  - **MRR**: "Navigational / Single answer"
  - **MAP**: "Ranked binary list"
  - **NDCG**: "Ranked graded list (Web Search)"

### Content

Recap and close out the video.

### Narration Notes

- **Script**: "By choosing the right evaluation metric for your search goals, you can tune your system to retrieve exactly what your users need. Happy evaluating!"

### Technical Notes

- Use `Table` with grid lines matching the HNSW design style.
- Clean up all assets with a final `FadeOut`.

---

## Transitions & Flow

- **Visual Motif**: The document cards are the primary recurring motif. They morph and change properties (swapping positions for MAP, changing to gradient shades for NDCG) to maintain visual continuity.
- **Formulas**: Equations sit on the right side of the screen while the document stacks occupy the left side, keeping the layout clean and balanced.

## Color Palette

- **Background**: `#05070D` (Premium Dark Navy)
- **Relevant / Highly Relevant**: `#10B981` (Emerald Green)
- **Partially Relevant**: `#34D399` (Light Emerald)
- **Irrelevant**: `#64748B` (Slate Gray)
- **Query Vector / Highlighting**: `#FF5A5F` (Rose Red)
- **Active Variable / Highlight**: `#A78BFA` (Violet)

## Mathematical Content

- $\text{Precision@K} = \frac{\text{Number of Relevant Documents in Top } K}{K}$
- $\text{Recall@K} = \frac{\text{Number of Relevant Documents in Top } K}{\text{Total Number of Relevant Documents}}$
- $\text{Hit Rate@K}$ query average check
- $\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$
- $\text{AP} = \frac{\sum_{k=1}^{N} \left( P(k) \times \text{rel}(k) \right)}{\text{Total Number of Relevant Documents}}$
- $\text{DCG}_K = \sum_{i=1}^{K} \frac{\text{rel}_i}{\log_2(i + 1)}$
- $\text{NDCG}_K = \frac{\text{DCG}_K}{\text{IDCG}_K}$

## Implementation Order

1. **Scene 1**: Set up standard `DocumentCard` and `StackContainer` classes.
2. **Scene 2 & 3**: Implement Precision, Recall, and Hit Rate animations (simple text transformations).
3. **Scene 4 & 5**: Add index tracking and sliding indicator arrows for ranking-based metrics.
4. **Scene 6**: Implement card color gradients and the sorting animation for IDCG.
5. **Scene 7**: Assemble the final overview table.
