# Visualizing Multi-Hop Retrieval (Parallel Query Decomposition vs. Sequential Chains)

## Overview
- **Topic**: Multi-Hop Retrieval (Query Decomposition vs. Sequential Dependency Resolution).
- **Hook**: How do RAG systems answer complex, multi-layered questions? We compare Parallel Query Decomposition (which fails on nested dependencies) with Sequential Multi-Hop (which resolves them step-by-step).
- **Target Audience**: Software engineers and AI practitioners.
- **Estimated Length**: 3 - 4 minutes.
- **Key Insight**: Independent sub-queries can be run in parallel, but nested dependencies require sequential execution where the output of one hop dynamically forms the query for the next.

## Narrative Arc
We begin with a nested question that paralyzes simple RAG. We then introduce Parallel Multi-Hop (Query Decomposition) using a comparative query, showing how it successfully splits independent tasks to run concurrently. However, we immediately show that this decomposition method fails when applied back to our nested question because of a hidden variable dependency. Finally, we introduce Sequential Multi-Hop as the solution that resolves the dependency layer-by-layer, and conclude with a speed-versus-reasoning tradeoff comparison.

---

## Scene 1: The Simple RAG Failure
**Duration**: ~45 seconds
**Purpose**: Show a complex nested query and demonstrate why standard single-hop retrieval fails.

### Visual Elements
- **Complex Query Box**: A styled glassmorphism text card:
  _"Compare the scientific contributions of Marie Curie and Albert Einstein"_
- **Standard RAG Flow**:
  - The entire sentence is embedded as a single vector.
  - A search is executed against a Vector Database (visualized as a scattered point cloud).
  - The database returns general biography articles for Marie Curie and Albert Einstein.
- **The Failure**:
  - The documents are highlighted with a red box showing missing critical data: _No detailed scientific breakthroughs are present in general biographies._
  - The Generator LLM outputs a warning icon: _"Error: Insufficient details to compare scientific contributions."_

### Content
We introduce a comparative query. Standard RAG searches for the whole phrase in one go, retrieving broad biographies instead of the specific details required to answer, resulting in failure due to lack of depth.

### Narration Notes
- **Tone**: Analytical, establishing the problem.
- **Key Points**:
  - "Standard RAG searches for everything at once, often missing critical details."
  - "When asked to compare contributions, general biographies lack the specific, deep scientific facts needed, resulting in failure."

### Technical Notes
- Highlight the query with a blue border.
- Use a `SurroundingRectangle` with a red border around the retrieved documents to show failure, and animate an exclamation mark.

---

## Scene 2: Parallel Multi-Hop (Query Decomposition)
**Duration**: ~60 seconds
**Purpose**: Introduce Parallel Multi-Hop (Query Decomposition) using a query that is natively independent.

### Visual Elements
- **New Query Card**:
  _"Compare the scientific contributions of Marie Curie and Albert Einstein."_
- **Decomposition Agent**: An agent icon (violet circle) splits this query into two independent paths:
  - **Sub-query 1**: _"Scientific contributions of Marie Curie"_
  - **Sub-query 2**: _"Scientific contributions of Albert Einstein"_
- **Parallel Retrieval**:
  - Both sub-queries are sent to the vector database concurrently.
  - Two parallel data return paths feed documents back to a **Composition Agent**.
- **Synthesis**: The Composition Agent merges the parallel context to output a clean comparative summary.

### Content
We introduce Parallel Multi-Hop. If a query is broad and comparative, we can decompose it into independent sub-queries. Since they do not rely on each other's outputs, we can run them at the same time, saving valuable round-trip latency.

### Narration Notes
- **Tone**: Informative, explaining a successful pattern.
- **Key Points**:
  - "Query Decomposition breaks a complex prompt into simpler, independent sub-queries."
  - "Because these queries don't depend on each other, they execute in parallel, keeping retrieval times low."

### Technical Notes
- Use `AnimationGroup` to trigger the two retrieval paths simultaneously, emphasizing the $O(1)$ concurrent time.
- Show the Composition Agent merging the streams into a single summary box.

---

## Scene 3: Where Query Decomposition Fails
**Duration**: ~45 seconds
**Purpose**: Show why parallel decomposition fails on the original nested GDP query.

### Visual Elements
- **Re-introducing the GDP Query**:
  _"Is the GDP of Marie Curie's birth country higher than that of Albert Einstein's?"_
- **Attempted Parallel Decomposition**:
  - The Decomposition Agent tries to split the query into:
    - **Sub-query 1**: _"What is the GDP of Marie Curie's birth country?"_
    - **Sub-query 2**: _"What is the GDP of Albert Einstein's birth country?"_
- **Database Failure**:
  - The database is searched for these exact phrases.
  - A red warning flash appears: database documents for GDP do not contain the name "Marie Curie," and biography documents do not contain GDP data.
  - The variables `[Curie's birth country]` and `[Einstein's birth country]` remain unresolved. Parallel execution hits a wall.

### Content
We demonstrate the limit of query decomposition. If we try to split the GDP query immediately, we run into a blocker: we cannot search for the GDP of a country if we don't know the country yet. The sub-queries are not independent; they are nested.

### Narration Notes
- **Tone**: Warning, pointing out the architectural limit.
- **Key Points**:
  - "But what happens if we apply query decomposition back to our original GDP question?"
  - "It fails. We cannot search for a country's GDP until we resolve which country we are looking for."
  - "This is a nested dependency, and parallel decomposition cannot bridge this gap."

### Technical Notes
- Use flashing red question marks over the unresolved country variables in the sub-queries.
- Animate a barrier or "Stop" sign between the decomposition stage and the database.

---

## Scene 4: Sequential Multi-Hop to the Rescue
**Duration**: ~60 seconds
**Purpose**: Introduce Sequential Multi-Hop and show how it resolves nested dependencies step-by-step.

### Visual Elements
- **Sequential Multi-Hop Execution**:
  - **Hop 1: Entity Resolution**
    - The system runs the first queries: _"Marie Curie birth country"_ and _"Albert Einstein birth country"_.
    - The database returns `Poland` and `Germany`.
  - **Context Propagation**:
    - The output values `Poland` and `Germany` are injected directly into the next query templates.
    - The query text morphs on screen:
      - _"GDP of [Country 1]"_ $\rightarrow$ _"GDP of Poland"_
      - _"GDP of [Country 2]"_ $\rightarrow$ _"GDP of Germany"_
  - **Hop 2: Attribute Retrieval**
    - The system runs these resolved queries: _"GDP of Poland"_ and _"GDP of Germany"_.
    - The database returns `$800B` and `$4.5T`.
  - **Synthesis**: The final LLM compares the numbers and returns the correct answer: _"No (Germany's GDP is higher)."_

### Content
Introduce Sequential Multi-Hop. We execute the first hop to resolve the unknown variables (Poland and Germany), feed those values back into our state context, and use them to construct the final queries for the second hop.

### Narration Notes
- **Tone**: Triumphant, explaining the solution.
- **Key Points**:
  - "To solve nested dependencies, we use Sequential Multi-Hop."
  - "First, we resolve the hidden variables: Curie's birth country is Poland, and Einstein's is Germany."
  - "Then, we use those answers to fetch the GDP figures. Step-by-step, the dependency chain is resolved."

### Technical Notes
- Use `ReplacementTransform` to morph the text labels (e.g. `[Country 1]` smoothly transitioning to `Poland`).
- Show the two distinct hops executing in sequence, separated by a brief pause to emphasize the dependency handoff.

---

## Scene 5: Tradeoffs (Speed vs. Reasoning)
**Duration**: ~45 seconds
**Purpose**: Compare the two paradigms to help developers make architectural decisions.

### Visual Elements
- **Tradeoff Grid**:
  - Columns: **Metric**, **Parallel Decomposition**, **Sequential Chain**
  - Row 1: **Latency** $\rightarrow$ Low ($O(1)$ round-trips) vs. High ($O(N)$ sequential steps)
  - Row 2: **Dependency Handling** $\rightarrow$ Poor (Requires independent facts) vs. Excellent (Resolves nested variables)
  - Row 3: **Best Used For** $\rightarrow$ Comparative / Multi-faceted queries vs. Nested / Chain-of-thought retrieval
- **Latency Bars**: Visual bar chart showing Sequential taking twice as long as Parallel, but with a green checkmark on Sequential for "Dependency Resolution."

### Content
Summarize the tradeoff: Parallel is fast but struggles with nested dependencies. Sequential is slower because of the multiple round-trips, but it is necessary for complex, multi-layered reasoning.

### Narration Notes
- **Tone**: Authoritative, concluding.
- **Key Points**:
  - "Parallel decomposition gives you speed, but requires independent questions."
  - "Sequential chains give you deep reasoning, but at the cost of higher latency."
  - "Choosing the right flow is a direct tradeoff between response speed and reasoning depth."

### Technical Notes
- Render the table cleanly.
- Draw horizontal comparison bars that grow, highlighting the $O(1)$ vs $O(N)$ latency difference.

---

## Transitions & Flow
- We transition between scenes using slide transitions or zoom-outs.
- When query decomposition fails in Scene 3, we transition to Scene 4 by drawing a vertical timeline showing the "hops" executing one after another.

## Color Palette
- **Background**: `#0F172A` (Slate Dark Blue)
- **Sequential / Wait Paths**: `#F43F5E` (Rose Red)
- **Parallel / Fast Paths**: `#10B981` (Emerald Green)
- **Text / Labels**: `#F8FAFC` (Off-white)
- **Highlights**: `#3B82F6` (Electric Blue)
