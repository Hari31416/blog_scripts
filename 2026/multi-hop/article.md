# Visualizing Multi-Hop Retrieval: Sequential vs. Parallel Flows

Standard Retrieval-Augmented Generation (RAG) works great for straightforward questions. If you ask for a simple fact, the system searches a vector database, pulls the most relevant document chunk, and uses it to answer.

But what happens when you throw a complex, multi-faceted question at it? Consider this:

> *"Compare the scientific contributions of Marie Curie and Albert Einstein."*

If you pass this entire sentence into a standard RAG pipeline, it creates a single search query. It looks for documents matching the whole phrase, which usually just returns broad biography articles about Curie and Einstein. Because these biographies are generic, they often lack specific details about their scientific breakthroughs, causing the comparison to fail. This is especially true in systems, where we usually set top_k to a small specified value to optimise for speed and cost, making it difficult to retrieve all the necessary information in one go.

<!-- ANIMATION_PLACEHOLDER: Scene 1 - Standard RAG Failure -->
*Figure 1: Standard RAG retrieves high-level biographies but fails because specific breakthrough details are missing from the retrieved context.*

---

## What is Multi-Hop Retrieval?

Multi-hop retrieval solves this problem by breaking a complex query down into multiple, distinct search steps (or "hops"). Instead of executing one broad, cluttered search, the system schedules multiple search steps.

How these searches are scheduled in production typically follows one of two paradigms: **Parallel Query Decomposition** or **Sequential Chains**.


## Paradigm 1: Parallel Multi-Hop (Query Decomposition)

If a query is broad and comparative, we can decompose it into independent sub-queries. Since they do not rely on each other's outputs, we can run them at the same time, saving valuable round-trip latency.

For our comparative question:
1. **Decompilation:** The system breaks the main query into two independent parts: *"Scientific contributions of Marie Curie"* and *"Scientific contributions of Albert Einstein"*.
2. **Parallel Retrieval:** Both sub-queries are launched concurrently against the vector database.
3. **Compilation:** A compiler agent receives the detailed retrieved contexts from both streams and merges them into a clean summary.

<!-- ANIMATION_PLACEHOLDER: Scene 2 - Parallel Query Decomposition -->
*Figure 2: Parallel Query Decomposition splits a comparative query into independent sub-queries, running them concurrently to minimize round-trip latency.*

---

## Where Query Decomposition Fails

But what happens if we apply query decomposition back to a nested question containing hidden variables? Consider this:

> *"Is the GDP of Marie Curie's birth country higher than that of Albert Einstein's?"*

If a decompiler agent attempts to split this query immediately, it creates two sub-queries: one asking for the GDP of Marie Curie's birth country, and another asking for the GDP of Albert Einstein's birth country.

This hits a wall. The database cannot search for these phrases because GDP documents do not contain the names of scientists, and biography documents do not contain GDP data. The variables `[Curie's birth country]` and `[Einstein's birth country]` remain unresolved. We cannot search for a country's GDP until we resolve which country we are looking for.

<!-- ANIMATION_PLACEHOLDER: Scene 3 - Decomposition Failure -->
*Figure 3: Immediate decomposition fails on nested queries because it cannot query attributes of unresolved variables.*

---

## Paradigm 2: Sequential Multi-Hop

To solve nested dependencies, we must execute a step-by-step chain of thought. The output of one hop dynamically forms the query for the next.

For our GDP comparison question, sequential retrieval operates in four distinct stages:

1. **Hop 1 (Entity Resolution):** The system first queries the birth countries. The query *"Marie Curie birth country"* returns `Poland`, and *"Albert Einstein birth country"* returns `Germany`.
2. **Context Propagation:** The system propagates these resolved variables. The next query templates *"GDP of [Country 1]"* and *"GDP of [Country 2]"* are dynamically rewritten as *"GDP of Poland"* and *"GDP of Germany"*.
3. **Hop 2 (Attribute Retrieval):** The resolved queries are executed. The query *"GDP of Poland"* returns `$800B`, and *"GDP of Germany"* returns `$4.5T`.
4. **Final Synthesis:** The LLM compares these figures and outputs the final answer: *"No (Germany's GDP is higher)."*

<!-- ANIMATION_PLACEHOLDER: Scene 4 - Sequential Multi-Hop -->
*Figure 4: Sequential Multi-Hop resolves nested queries step-by-step, using entity resolution (Hop 1) to propagate variables and rewrite the queries for Hop 2.*

---

## Summary of Trade-offs

Choosing the right pattern depends entirely on your data structure and user requirements:

* **Query Latency:** Parallel decomposition has low latency, executing in a single $O(1)$ round-trip. Sequential chains have high latency, requiring $O(N)$ sequential database round-trips.
* **Dependencies:** Parallel decomposition performs poorly with nested dependencies since it requires independent facts. Sequential chains excel at resolving nested variables step-by-step.
* **Best Used For:** Parallel decomposition is ideal for comparative or multi-faceted queries. Sequential chains are designed for nested or chain-of-thought retrieval.

<!-- ANIMATION_PLACEHOLDER: Scene 5 - Tradeoffs Comparison -->
*Figure 5: High-level metric tradeoffs and round-trip time latency compared between Parallel and Sequential paradigms.*

Choosing between these flows is a direct trade-off between response speed and reasoning depth. Use parallel query decomposition for flat, comparative queries to keep retrieval times low; use sequential chains for nested, multi-hop reasoning.