# Lecture 05 Answers

## Exercises

## Exercises

- Answering model (`[model]` shown during execution): `gemini-3.1-flash-lite`

- Comparison question: "In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add?"

- Target materials (also record the difference in scope between full context and the other methods):

Full Context processes all available lecture documents simultaneously. The exercise materials describe a scope of 9 documents and 438 pages, while Vector Search, Tree, and Graph operate on the main materials from Lectures 01–03 (214 pages). This difference must be considered when comparing efficiency, since Full Context receives a substantially larger amount of information.

### Results by Method

| Method | Key points and correctness of the answer | Cited pages and evidence | Time (seconds) | Input/output tokens | Model responses | Estimated generation API cost (USD) |
|---|---|---|---:|---|---:|---:|
| Full context | Correct. LoRA freezes pretrained weights and trains low-rank matrices A and B. QLoRA adds 4-bit quantization. | Lecture 2, Japanese source p.52; translated PDF p.75; Lecture 2 Exercises p.21. | 3.31 | 95,823 / 270 | 1 | $0.024361 |
| Vector search | Correct. Accurately explained both LoRA and QLoRA. | Lecture 2, pp.51–52. Page 52 provides direct supporting evidence. | 3.40 | 2,756 / 236 | 2 | $0.001043 |
| Tree | Correct. Explained frozen weights, trainable matrices, and 4-bit quantization. | Lecture 2, p.52. Retrieved through hierarchical navigation. | 17.76 | 9,437 / 352 | 5 | $0.002887 |
| Graph | Correct. Explained LoRA and QLoRA accurately. | Lecture 2, p.52 appeared among the retrieved seeds, but the final answer did not explicitly cite a page number. | 18.32 | 5,186 / 313 | 2 | $0.001766 |

- Pages found by running search alone, and what their text confirmed:

Executed:

`uv run python -m app.retrieval "LoRA QLoRA difference"`

The independent retrieval test returned 11 pages, including five initial vector-search results and six additional pages from the adjacent-page expansion implemented during Homework.

The initial results included:

1. Lecture 2, p.52: Directly explains that LoRA freezes the original weights and trains small low-rank matrices A and B. QLoRA additionally compresses the base weights to 4 bits.
2. Lecture 2, p.51: Introduces Parameter-Efficient Fine-Tuning (PEFT) and explains the differences between full fine-tuning, LoRA, and QLoRA.
3. Lecture 2, p.60: Discusses a QLoRA exercise involving output-format compliance and evaluation.
4. Lecture 2, translated PDF p.79: Discusses the differences between retrieval and fine-tuning for acquiring knowledge.
5. Lecture 2, p.61: Contains exercise instructions with limited relevance to the comparison question.

The strongest evidence was concentrated on pages 51–52, especially page 52. The additional retrieved pages provided contextual information but were not necessary to answer this question. Because this independent search used the retrieval function modified during Homework, its 11-page output should be distinguished from the original five-result Vector Search baseline.

- Tool calls shown by `--trace` (names, arguments, counts, table-of-contents paths followed by Tree, etc.):

Full Context: No retrieval tools were called. The system supplied the complete lecture materials directly to the model. The input contained 369,490 characters, producing 95,823 input tokens.

Vector Search:

One `search_materials` call: `search_materials(query="LoRA freeze train QLoRA")`

The search retrieved the relevant Lecture 2 material, including page 52.

Tree:

Four `browse_tree` calls:

1. `browse_tree({})`
2. `browse_tree(node_id="lec02-main")`
3. `browse_tree(node_id="lec02-main-s045")`
4. `browse_tree(node_id="lec02-main-p052")`

Navigation path: `Course materials → Lecture 2 → When and how to adapt the selected model → Page 52`

The final call retrieved 1,238 characters of page text.

Graph:

One `search_graph` call:

`search_graph(query="Lecture 2 LoRA freeze train QLoRA")`

The search returned page `lec02-main-p052` among its initial seeds and explored related pages through the existing graph structure.

The original Graph mode was used, without enabling the Query-Aware modification developed during Homework.

- Examples where retrieved information was insufficient, or was retrieved but not used in the answer:

All four methods produced factually correct answers for the comparison question. No complete retrieval failure was observed in these executions.

However, several differences were identified:

1. Full Context: Received substantially more information than the question required. Most of the supplied material was unnecessary for answering.
2. Vector Search: Retrieved sufficient evidence efficiently, without requiring additional pages beyond the main explanation.
3. Tree: Successfully located the required page but needed multiple navigation steps and model responses.
4. Graph: Retrieved supporting evidence from Lecture 2, page 52, but the final answer did not explicitly cite that page.

The independent retrieval test also returned several pages discussing exercises and general fine-tuning concepts that were not essential to the requested explanation. These observations distinguish successful evidence retrieval from efficient evidence selection and proper citation.

- Method you would adopt for this use case, your reasons, and limitations of the comparison conditions:

I would adopt Vector Search for this type of factual, single-page question. It produced a correct answer with the lowest measured generation API cost ($0.001043) and the fewest input tokens (2,756). Full Context also answered correctly and was fast in this execution, but its estimated generation cost was approximately 23 times higher than Vector Search. Tree provided a clear and interpretable retrieval path, but required four tool calls and five model responses. Graph retrieved relevant evidence but offered no demonstrated accuracy advantage for this question, while consuming more tokens than Vector Search.

The comparison has several limitations:

- Full Context covers more documents than the retrieval-based methods.
- Only one successful execution per method was recorded.
- The agent generated different search queries across methods.
- Response times may fluctuate because of model and API conditions.
- Generation API costs exclude query embedding and index construction.
- This comparison focused on a single-page factual question rather than evaluating a broad range of question types.

Therefore, these results support choosing Vector Search for this specific use case, but do not establish that it is universally superior.

- Observations and questions:

The experiment demonstrated that more context does not necessarily produce a better answer. All four methods answered correctly, despite substantial differences in context size, retrieval strategy, and computational cost. Full Context showed that a model can process a large amount of material successfully, although doing so may be unnecessarily expensive. Vector Search demonstrated the value of selecting only the most relevant evidence. Tree made the retrieval process interpretable by following the course structure. Graph provided a mechanism for discovering related information, but additional context did not improve correctness in this particular experiment.

For simple factual questions, selective retrieval appears preferable to supplying all available information. For questions requiring explanations across multiple sections, Tree or Graph may offer additional advantages.

Future experiments should evaluate:

1. Multi-page and cross-chapter questions requiring distributed evidence.
2. Unanswerable questions to test whether the model recognizes missing information.
3. Repeated executions to estimate variability in accuracy, latency, and cost.
4. Citation accuracy independently of answer correctness.
5. The relationship between retrieval size and evidence coverage.

The main conclusion is that retrieval methods should be selected according to the question, the required evidence, and measured performance rather than assuming that larger contexts or more complex search methods are inherently better.


## Homework

<!-- Completing any one of Basic, Implementation, or Advanced is sufficient. -->

- Level attempted: Basic / Implementation / Advanced
- What you did (files, settings, or processing changed, or retrieval method designed):
- Comparison question and conditions held fixed (model, target materials, etc.):
- Results (answers and evidence before/after, `--trace` output, time, token counts, estimated generation API cost, etc.):
- Examples of improvements and remaining failures or limitations:
- Observations and questions:

### Basic
What you did: Modified `RAG_TOP_K` in `app/config.py`, reducing the maximum number of retrieved pages from 5 to 2. The objective was to evaluate whether limiting retrieved context could reduce token consumption and generation API cost while preserving answer correctness and supporting evidence.

Comparison question and conditions held fixed: "In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add?"

Both experiments used:
- Model: `gemini-3.1-flash-lite`
- Retrieval method: Vector search (`search_materials`)
- Target materials: Lectures 01–03
- Identical question and answer requirements
- Execution with `--trace`

Results:

| Metric | Baseline (k=5) | Modified (k=2) |
|---|---:|---:|
| Response time | 3.40 s | 4.23 s |
| Input tokens | 2,756 | 1,628 |
| Output tokens | 236 | 265 |
| Model responses | 2 | 2 |
| Estimated generation API cost | $0.001043 | $0.000804 |
| Pages referenced | Lecture 2, pp. 51–52 | Lecture 2, p. 52 |
| Answer correctness | Correct | Correct |

Tool calls and supporting evidence:

Both executions called `search_materials`

- Baseline query: `"LoRA freeze train QLoRA"`
- Modified query: `"In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add?"`

Both answers correctly explained that LoRA freezes pretrained model weights while training additional low-rank matrices. QLoRA additionally quantizes the base model to 4 bits, reducing memory requirements. The modified execution retrieved Lecture 2, page 52, which directly supports the requested explanation.

Examples of improvements and remaining failures or limitations: Reducing `RAG_TOP_K` decreased input-token consumption by approximately 41% and estimated generation API cost by 23%, without compromising answer correctness in this experiment. However, response time increased by 0.83 seconds. Fewer retrieved pages did not translate into faster execution. Only one successful run per configuration was recorded. Additionally, the agent generated different search queries, introducing another variable into the comparison. These limitations prevent attributing every observed difference exclusively to the retrieval limit.

Observations and questions: A smaller retrieval budget appears effective when the required evidence is concentrated on a single page. It can reduce unnecessary context while maintaining factual accuracy. However, reducing the number of retrieved pages may compromise evidence coverage for questions requiring information distributed across multiple sections. Further experiments should evaluate multi-page questions and repeated executions to determine whether these efficiency gains remain consistent.

### Implementation
What you did: Modified `search()` in `app/retrieval.py` to extend vector-search results with the immediately preceding and following pages. The implementation uses `(document_id, page)` to identify neighboring pages, prevents retrieval across document boundaries, and removes duplicates using `page_id`.

The original vector-search results are preserved, while additional pages are labeled with `retrieval_type: adjacent` and their corresponding source page.

Comparison question and conditions held fixed:

"In Lecture 3, how does compaction differ from cross-session memory? Do all daily notes become long-term memory?"

Both executions used:
- Model: `gemini-3.1-flash-lite`
- Retrieval method: Vector search, with and without adjacent-page expansion
- Target materials: Lectures 01–03
- `RAG_TOP_K = 5`
- Identical question and lecture materials
- Execution with `--trace`

Results:

| Metric | Original RAG | Adjacent-Page RAG |
|---|---:|---:|
| Response time | 15.40 s | 22.10 s |
| Input tokens | 2,293 | 4,230 |
| Output tokens | 476 | 345 |
| Model responses | 2 | 2 |
| Estimated generation API cost | $0.001287 | $0.001575 |
| Answer correctness | Correct | Correct |
| Retrieval strategy | Top 5 vector results | Top 5 + adjacent pages |

Tool calls and retrieval verification: Both executions called `search_materials` using the query:

`"compaction cross-session memory daily notes long-term memory"`

The modified retrieval function was also tested independently.

Original vector-search pages:
- Lecture 3: 13, 38, 39, 40, 65

Additional adjacent pages:
- Lecture 3: 12, 14, 37, 41, 64, 66

Verification results:
- Total retrieved pages: 11
- Unique pages: 11
- Duplicate pages: 0
- Document boundary violations: 0 in the tested results

All retrieved pages belonged to `lec03-main`, confirming that neighboring pages were added without crossing document boundaries.

Examples of improvements and remaining failures or limitations:

The modification successfully expanded evidence coverage from 5 to 11 pages, providing additional context around the original search results.

Both methods correctly distinguished compaction, which manages context within a session, from cross-session memory, which preserves selected information across sessions. Both also correctly explained that not all daily notes become long-term memory.

However, the expanded retrieval did not demonstrate an accuracy improvement for this question.

Input-token consumption increased by approximately 84.5%, estimated generation API cost increased by 22.4%, and response time increased by 6.70 seconds.

Pages adjacent to relevant results may provide useful context, but they may also introduce unrelated information. The inclusion of additional pages does not guarantee better evidence or stronger answers.

Only one end-to-end execution per configuration was measured. Additional questions and repeated runs would be necessary to establish consistent performance differences.

### Advanced
What you did: Designed and implemented Query-Aware Graph Retrieval, an improved graph-based retrieval method that prioritizes question-relevant evidence while limiting unnecessary context expansion.

The implementation modifies `search_graph()` in `app/retrieval.py` and introduces two improvements:

    1. Query-aware candidate ranking based on weighted keyword overlap between the question and retrieved pages.

    2. Selective expansion using document filtering, minimum relevance requirements, and a restricted context budget.

The improved method is activated through `AIE_GRAPH_MODE=query_aware`, allowing comparisons with the original Graph implementation without changing the source code between runs.

Data structure, storage, and retrieval design:

The system retains the existing retrieval infrastructure:

- `data/rag_data/lectures.json`: lecture materials organized into page-level chunks
- `data/rag_data/index.sqlite3`: vector search index
- `data/rag_data/graph.json`: graph connections between pages and terms
- `app/retrieval.py`: graph traversal and candidate-selection logic

The retrieval process follows these steps:

    1. Retrieve three initial vector-search results.
    2. Explore graph connections using the existing traversal mechanism.
    3. Extract significant terms from the question, page titles, and page contents.
    4. Filter candidates by the requested lecture, when specified.
    5. Require at least two distinct matching query terms.
    6. Rank eligible candidates using a relevance score.
    7. Return at most three additional pages, preserving the initial vector-search results.

The relevance score is:

`Score(page, query) = 3 × TitleMatches + ContentMatches`

Title matches receive greater weight because page titles often identify the principal subject of a slide. The algorithm uses distinct matching terms, reducing the influence of repeated words within long passages. The implementation preserves the original graph structure and changes only how additional candidates are selected.

Design rationale: The original Graph method can retrieve related but unnecessary pages, increasing input-token consumption without necessarily improving answer quality. The proposed method prioritizes evidence related to the actual question while restricting expansion to a smaller number of relevant pages. This design aims to balance evidence coverage, retrieval flexibility, and generation cost.

Comparison questions and conditions held fixed:

Question 1: Multi-page reasoning:

"In Lecture 3, how does compaction differ from cross-session memory? Do all daily notes become long-term memory?"

Expected evidence: Lecture 3, pp. 13, 39, and 40.

Question 2: Single-page explanation:

"In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add?"

Expected evidence: Lecture 2, p. 52.

Experimental conditions:

- Model: `gemini-3.1-flash-lite`
- Target materials: Lectures 01–03
- Same question wording across methods
- Same underlying lecture materials and search index
- `RAG_TOP_K = 5`
- `GRAPH_START_K = 3`
- `GRAPH_HOPS = 2`
- `GRAPH_MAX_RESULTS = 10`
- Graph improvement activated through `AIE_GRAPH_MODE=query_aware`

Basic RAG, original Graph, and Query-Aware Graph were compared using previously recorded executions.

Results:

Question 1: Compaction and Cross-Session Memory

| Metric | Basic RAG | Original Graph | Query-Aware Graph |
|---|---:|---:|---:|
| Response time | 15.40 s | 14.67 s | 3.45 s |
| Input tokens | 2,293 | 4,878 | 2,581 |
| Output tokens | 476 | 390 | 371 |
| Model responses | 2 | 2 | 2 |
| Estimated API cost | $0.001287 | $0.001804 | $0.001202 |
| Answer correctness | Correct | Correct | Correct |

Question 2: LoRA and QLoRA

| Metric | Basic RAG | Original Graph | Query-Aware Graph |
|---|---:|---:|---:|
| Response time | 3.40 s | 18.32 s | 3.87 s |
| Input tokens | 2,756 | 5,186 | 3,481 |
| Output tokens | 236 | 313 | 269 |
| Model responses | 2 | 2 | 2 |
| Estimated API cost | $0.001043 | $0.001766 | $0.001274 |
| Answer correctness | Correct | Correct | Correct |

The improved Graph reduced input tokens relative to the original Graph by approximately:

- 47.1% for the memory question.
- 32.9% for the LoRA question.

Estimated generation cost decreased by approximately 33.4% and 27.9%, respectively.

Both questions remained correctly answered.

However, Basic RAG still consumed fewer input tokens than the improved Graph in both cases. For the LoRA question, Basic RAG also achieved a lower estimated cost.

Tool calls and retrieval verification:

All Graph experiments used `search_graph` with `--trace`.

The original implementation returned excessive contextual information relative to the evidence needed for these questions. The first Query-Aware implementation also retrieved unrelated pages from other lectures, revealing a weakness in keyword-based relevance scoring. The algorithm was subsequently refined with lecture filtering and a minimum threshold of two distinct query-term matches.

Independent retrieval tests using fixed vector-search seeds produced the following results:

| Verification | Memory | LoRA |
|---|---:|---:|
| Initial vector results | 3 | 3 |
| Expanded graph results | 3 | 3 |
| Total retrieved pages | 6 | 6 |
| Duplicate pages | 0 | 0 |
| Pages outside requested lecture | 0 | 0 |

For the memory question, the test retained Lecture 3 pages 38, 39, and 65 as seeds and selected pages 40, 58, and 71 as additional candidates. For the LoRA question, the test retained Lecture 2 pages 51, 52, and 60 as seeds and selected pages 54, 58, and 59 as additional candidates. These deterministic tests verified candidate filtering and duplicate prevention. The end-to-end experiments separately evaluated the model's final answers.

Examples of improvements and remaining failures or limitations:

The final Query-Aware Graph correctly explained that compaction summarizes history within a session, while cross-session memory preserves selected information across sessions. It also correctly explained that daily notes undergo selective review and do not automatically become long-term memory. The final answer cited Lecture 3, pp. 38, 39, 40, and 65.

For the LoRA question, the system correctly identified frozen base weights, trainable low-rank matrices, and QLoRA's 4-bit quantization. The retrieval trace included Lecture 2, p. 52, although the final answer did not provide an explicit page citation.

The improvements were accompanied by several limitations:

- Keyword overlap does not fully capture semantic relevance or synonyms.
- Restricting expansion to the requested lecture may exclude useful cross-lecture relationships.
- The three-page expansion budget may omit important evidence for complex questions.
- The memory test did not retrieve every page in the predefined evidence set, although the available pages were sufficient to answer correctly.
- Correct answers do not guarantee complete evidence coverage or citation quality.
- One end-to-end execution per configuration is insufficient to establish consistent latency or accuracy improvements.
- Agent-generated search queries differed between some executions, limiting strict experimental control.