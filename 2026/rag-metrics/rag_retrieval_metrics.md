# Evaluating RAG Retrieval: A Comprehensive Guide to Retrieval Metrics

A Retrieval-Augmented Generation (RAG) pipeline relies on two core components: **Retrieval** (finding the relevant context) and **Generation** (synthesizing the answer using that context). If the retriever fetches low-quality, incomplete, or noisy documents, the generator will inevitably produce subpar, hallucinated, or irrelevant answers—a classic case of "garbage in, garbage out."

Evaluating the retrieval component is therefore critical to optimize chunking strategies, embedding models, indexing configurations, and reranking pipelines.

Retrieval metrics are divided into two main categories:
1. **Traditional Information Retrieval (IR) Metrics**: Historically used in search engines, requiring a rigid ground-truth dataset (labeled queries and relevant documents).
2. **RAG-Specific Context Metrics**: Often utilizing "LLM-as-a-judge" to evaluate the quality, sufficiency, and relevance of the retrieved context without requiring extensive manual annotation.

---

## 1. Traditional Information Retrieval (IR) Metrics

These metrics evaluate the ranking quality and relevance of the retrieved documents against a known set of ground-truth relevant documents.

### Precision@K
* **Definition**: The proportion of retrieved documents in the top $K$ results that are actually relevant to the query.
* **Equation**:
  $$\text{Precision@K} = \frac{\text{Number of Relevant Documents in Top } K}{K}$$
* **Characteristics**:
  * Simple to compute and understand.
  * Disregards the order of the relevant documents within the top $K$.
  * Ignores the total number of relevant documents available in the dataset.

### Recall@K
* **Definition**: The proportion of all existing relevant documents that were successfully retrieved in the top $K$ results.
* **Equation**:
  $$\text{Recall@K} = \frac{\text{Number of Relevant Documents in Top } K}{\text{Total Number of Relevant Documents in Dataset}}$$
* **Characteristics**:
  * Focuses on the "completeness" of the search.
  * Disregards the order of the documents within the top $K$.
  * High recall can sometimes come at the cost of precision (introducing noise).

### Mean Reciprocal Rank (MRR)
* **Definition**: Evaluates ranking performance based on the position of the *first* relevant document.
* **Equation**:
  $$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$
  *Where $|Q|$ is the total number of queries, and $\text{rank}_i$ is the rank position of the first relevant document for the $i$-th query. If no relevant document is found, the reciprocal rank is $0$.*
* **Characteristics**:
  * Crucial for systems where the user only needs one correct result (e.g., QA systems, navigational queries).
  * Ignores any relevant documents retrieved *after* the first one.

### Mean Average Precision (MAP)
* **Definition**: The average of the Average Precision (AP) scores across a set of queries. Average Precision accounts for the precision at every rank where a relevant document is retrieved.
* **Equation**:
  $$\text{AP} = \frac{\sum_{k=1}^{N} \left( P(k) \times \text{rel}(k) \right)}{\text{Total Number of Relevant Documents}}$$
  $$\text{MAP} = \frac{1}{|Q|} \sum_{q \in Q} \text{AP}(q)$$
  *Where $N$ is the total number of retrieved documents, $P(k)$ is the precision at rank $k$, and $\text{rel}(k)$ is an indicator function (1 if the document at rank $k$ is relevant, 0 otherwise).*
* **Characteristics**:
  * Highly sensitive to the rank order of all relevant documents.
  * Penalizes systems that return relevant documents lower in the list.

### Normalized Discounted Cumulative Gain (NDCG)
* **Definition**: Evaluates the ranking quality by accounting for graded relevance (e.g., highly relevant, partially relevant, irrelevant) and penalizing relevant documents ranked lower in the list.
* **Equation**:
  * **Cumulative Gain (CG)** at $K$:
    $$\text{CG}_K = \sum_{i=1}^{K} \text{rel}_i$$
  * **Discounted Cumulative Gain (DCG)** at $K$ (Standard):
    $$\text{DCG}_K = \sum_{i=1}^{K} \frac{\text{rel}_i}{\log_2(i + 1)}$$
    *(Alternative formulation emphasizing highly relevant documents: $\text{DCG}_K = \sum_{i=1}^{K} \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}$)*
  * **Normalized DCG (NDCG)** at $K$:
    $$\text{NDCG}_K = \frac{\text{DCG}_K}{\text{IDCG}_K}$$
    *Where $\text{IDCG}_K$ is the Ideal DCG at $K$, achieved by sorting the documents by their ground-truth relevance in descending order.*
* **Characteristics**:
  * The gold standard for evaluating modern web search and recommendation systems.
  * Properly rewards systems that put the most relevant items at the absolute top.

### Hit Rate@K (or Success Rate@K)
* **Definition**: The fraction of queries for which at least one relevant document is returned in the top $K$ results.
* **Equation**:
  $$\text{Hit Rate@K} = \frac{1}{|Q|} \sum_{q \in Q} \mathbb{I}(\text{at least one relevant document is in top } K)$$
  *Where $\mathbb{I}(\cdot)$ is the indicator function.*
* **Characteristics**:
  * Simple, binary query-level metric.
  * Very common in initial RAG prototyping to determine if the retriever is finding the "needle in the haystack."

---

## 2. RAG-Specific Context Metrics

Traditional IR metrics require hard ground-truth labels for *which* chunks are relevant. In many production RAG applications, such labels do not exist or are difficult to maintain. Modern RAG evaluation frameworks (such as **Ragas**, **TruLens**, and **DeepEval**) address this using "LLM-as-a-judge" to evaluate the retrieved context relative to the query and/or reference answers.

### Context Recall
* **Definition**: Evaluates whether the retrieved context contains all the necessary information required to answer the query.
* **How it is evaluated (LLM-as-a-judge)**:
  The reference (ground-truth) answer is decomposed into individual factual statements or claims. The LLM then analyzes the retrieved context to verify whether each statement can be attributed to or derived from the context.
* **Equation**:
  $$\text{Context Recall} = \frac{\text{Number of statements in Reference Answer supported by Context}}{\text{Total number of statements in Reference Answer}}$$
* **Characteristics**:
  * Focuses on *sufficiency*. Low context recall leads to generation gaps and hallucinated details as the generator attempts to answer without the facts.

### Context Precision
* **Definition**: Evaluates whether the relevant chunks in the retrieved context are ranked higher than the irrelevant chunks.
* **How it is evaluated (LLM-as-a-judge)**:
  The LLM evaluates each chunk in the retrieved context and decides whether it is relevant to answering the user query. The metric then computes a ranking-weighted precision score.
* **Equation**:
  $$\text{Context Precision@K} = \frac{\sum_{k=1}^{K} \left( P(k) \times \text{rel}(k) \right)}{\text{Total number of relevant chunks in top } K}$$
  *Where $\text{rel}(k)$ is 1 if chunk $k$ is deemed relevant by the LLM, and 0 otherwise. $P(k)$ is the precision at rank $k$.*
* **Characteristics**:
  * Evaluates the ranking performance of your retriever/reranker.
  * Important because LLMs can suffer from "lost in the middle" phenomena, where they ignore relevant context if it is buried in the middle of a large prompt.

### Context Relevancy (or Relevance)
* **Definition**: Measures the proportion of the retrieved context that is actually relevant to the user query, serving as a signal-to-noise ratio.
* **How it is evaluated (LLM-as-a-judge)**:
  The LLM parses the retrieved context, identifies sentences that are useful to address the user query, and penalizes the inclusion of redundant or off-topic text.
* **Equation**:
  $$\text{Context Relevancy} = \frac{\text{Number of sentences in Context relevant to Query}}{\text{Total number of sentences in Context}}$$
* **Characteristics**:
  * Evaluates *conciseness* and *focus*.
  * High context relevancy helps prevent the generator from being distracted by irrelevant information or exceeding token limits.

### Context Density / Noise Ratio
* **Definition**: A quantitative measure of the density of key information relative to filler words/sentences in the retrieved context. 
* **Characteristics**:
  * Similar to context relevancy, but sometimes calculated programmatically using information extraction algorithms or specific prompts to count useful tokens versus total tokens.

---

## Summary Comparison: Traditional vs. RAG-Specific Metrics

| Metric | Category | Primary Focus | Requires Labeled Chunks? | Sensitivity to Rank Order |
| :--- | :--- | :--- | :--- | :--- |
| **Precision@K** | Traditional | Accuracy / Quality of top results | Yes | No |
| **Recall@K** | Traditional | Coverage / Completeness | Yes | No |
| **MRR** | Traditional | Finding the single best result first | Yes | Yes (First match only) |
| **MAP** | Traditional | Overall ranking quality | Yes | Yes (Highly sensitive) |
| **NDCG** | Traditional | Graded relevance and ranking quality | Yes | Yes (Highly sensitive) |
| **Hit Rate** | Traditional | Basic success (binary) | Yes | No |
| **Context Recall** | RAG-Specific | Sufficiency of facts to answer query | No (Requires reference answer) | No |
| **Context Precision** | RAG-Specific | Ranking order of relevant chunks | No | Yes |
| **Context Relevancy** | RAG-Specific | Signal-to-noise ratio (reducing noise) | No (Query & Context only) | No |
