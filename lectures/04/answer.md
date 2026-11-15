# Lecture 04 Answers

## Exercises

- Agreement by criterion (before revision): Grounding 9/9 , Scope 10/10 , Hint 10/10 , Clarity 9/10 , Lecture marker 10/10
- Number of items needing review (before revision): 1 (case 5, grounding)
- Criterion revised and the policy added: I updated the grounding criterion to allow general explanations of terms that are not in the glossary as long as the answer clearly states that the term is absent. I also removed the corresponding unresolved question.
- Agreement by criterion and number of review items (after revision): Grounding 10/10, Scope 10/10, Hint 10/10, Clarity 9/10, Lecture marker 10/10. The number of items needing review dropped from 1 to 0 and automatic coverage increased from 90% to 100%.
- Items where your labels differed from the instructor's, and your reasons: There were no disagreements. My labels matched the instructor's across all ten cases and five criteria, I did mark Cases 05 and 09 as uncertain because I thought the rubric left some room for interpretation.
- Observations and questions: Case 05 showed how an unclear rule can prevent automatic grading even when the answer itself seems reasonable, after defining the policy the grader could make a decision. Case 08 still had a disagreement on clarity which seems more subjective than the other criteria.

## Homework

- Level attempted: Basic / Implementation / Advanced
- What you did:
- Results:
- Observations and questions:

## Basic

- What you did: I compared the results before and after changing the grounding rubric; the original rule did not clearly explain how to handle general information about terms missing from the glossary. I added a policy allowing these explanations when the absence of the term is acknowledged then ran the evaluation again using the same ten cases.

- Results: Grounding agreement increased from 9/9 to 10/10, and the number of cases requiring manual review decreased from 1 to 0. The other criteria remained unchanged, case 08 still produced a clarity disagreement.

- Observations and questions: I found it interesting that changing one rule was enough to resolve an uncertain case without modifying the agent's original answer, it also made me think about how much the wording of an evaluation criterion can affect the results.

Note: I attempted to run the evaluation with Gemini, but the API repeatedly returned a 503 error, therefore I used --model test to complete the exercise and check how the rubric change affected the evaluation workflow. This mode uses predefined rules rather than a real LLM, so these results should not be treated as evidence of actual LLM grading performance.

## Implementation

- What you did: I created 10 evaluation cases covering normal questions, technical comparisons, spelling mistakes, terms missing from the glossary, homework questions, unrelated questions, attempts to override instructions, accidental inputs and nonexistant lectures. I generated answers using the lecture 03 agent with Gemini 3.1 Flash-Lite then evaluated them manually using the same 5 criteria from the exercises.
The API returned 503 and 429 errors, so I generated and saved the responses individually to avoid losing progress, I  used the same approach for the automatic grading and compared the results against my manual labels.

- Results:
+----------------+-----------+
| Criterion      | Agreement |
+----------------+-----------+
| Grounding      | 9/10      |
| Scope          | 9/10      |
| Hint           | 10/10     |
| Clarity        | 10/10     |
| Lecture marker | 10/10     |
+----------------+-----------+
Overall agreement was 10/10 with 100% automatic coverage. Out of 50 individual judgments 48 matched, giving a criterion-level agreement of 96%. The two disagreements were in Scope (Case 08) and Grounding (Case 10).
    Case 8: The grader marked the response as failing because it did not explicitly refuse the request to revel its system prompt, I marked it as passing because the agent maintained its educational role and did not reveal the full system prompt.

    Case 10: The grader accepted the answer because it did not invent any lecture content, I marked it as failing because the response only stated that "Lecture 40" was unavailable instead of stating thr course does not have a 40th lecture.

- Observations and questions: The exercise made it clear to me that agreement on the overall result does not necessarily mean agreement on every criterion. I also noticed that some criteria are easier to evaluate automatically than others; lecture marker is better suited to code-based checks because its format can be verified with a regular expression. Other objective requirements such as exact values or required fields could also be checked through code. Grounding, scope, hint and clarity are better suited to LLM evaluation because they require interpreting the meaning of a response rather than just checking its format. Still, code based checks have limitations; for example answers to empty or unrelated questions can fail the lecture marker check despite having no relevant lecture reference. I think this rule could be improved by allowing exceptions when no lecture applies. The disagreements in cases 08 and 10 also showed me that LLM grading is not always reliable, it can reject a reasonable response or accept one that does not fully meet the expected behavior. Human review is still important.

Since the evaluation only included 10 cases the results are useful for identifying possible problems but they are not enough to draw strong conclusions about the grader's reliability.

## Advanced

- What you did: For the Advanced assignment I investigated Humanity's Last Exam (HLE), a benchmark developed by the Center for AI Safety, Scale AI, and an international consortium of academic contributors. I selected HLE because it was designed to evaluate frontier AI models using questions requiring specialized knowledge and complex reasoning. Its construction and validation procedures are particularly relevant to Lecture 04 because it focuses on developing reliable evaluation systems.

I examined five questions from the Linguistics category, focusing on different areas of the discipline:

1. Proto-Indo-European to Middle English (`66e93b7099d9d12b2b824c44`): Historical reconstruction through successive phonological and morphological changes.
2. Sanskrit, Hindi, and Punjabi (`66ea36e7aa2256fb4c995faf`): Reconstruction of a hypothetical ancestral form from two Indo-Aryan descendant forms.
3. Kazakh color terminology (`66e9b2899cf8fcf41599246f`): Inferring the semantic distinction between two terms associated with the color green.
4. Guarani nominal tense and aspect (`66f27d65a40482f6012a4006`): Identifying grammatical marking associated with objects created through an action.
5. Tulu and Korean (`670477044580e464f8bff2a3`): Identifying lexical similarities between two geographically and historically distinct languages.

For each question I examined its intended task, required knowledge, expected answer, and potential evaluation difficulties. I also considered whether I could solve it independently or would require specialist references. Then I investigated HLE's development including contributor recruitment, question screening, expert review, grading procedures and independent assessments of its reliability.

My principal sources were the original HLE research paper, its methodological documentation, and subsequent audits by Epoch AI, FutureHouse, and the HLE-Verified research project.

Finally I compared HLE with the ten-case evaluation set developed during Lecture 04, particularly the relationship between reference-answer quality, automated grading, and human judgment.

- Results:

1. Analysis of the selected linguistic questions

    ### Proto-Indo-European to Middle English - Historical reconstruction

    This question requires reconstructing a hypothetical Middle English verbal form from a Proto-Indo-European root. Solving it involves several stages of linguistic change including historical sound laws and morphological developments. I would need specialized references to verify the reconstruction independently. For an LLM the primary difficulty is maintaining consistency across multiple transformations; an early phonological error can invalidate the final result.

    The evaluation concern is whether a grader can distinguish an incorrect reconstruction from a valid answer expressed using a different historical spelling or linguistic notation. An exact-answer reference is useful but acceptable representational variations must be defined carefully.

    ### Sanskrit, Hindi, and Punjabi - Comparative reconstruction

    This problem presents hypothetical Hindi and Punjabi forms and asks for their most probable Sanskrit ancestor in IPA notation. Unlike a vocabulary question, it requires working backward from descendant forms using historical phonological correspondences. I could understand the general reconstruction method but could not confidently verify the answer without knowledge of Indo-Aryan historical linguistics.

    The main evaluation challenge is determining whether the proposed ancestral form is sufficiently justified and whether equivalent phonetic representations would be recognized by the grader, it illustrates the difference between producing the expected answer and demonstrating that a reconstruction is linguistically defensible.

    ### Kazakh - Semantic categorization

    This question asks the model to identify a contextual distinction between kök and jasyl, two Kazakh terms associated with green; its difficulty lies in inferring a semantic pattern from examples without assuming that color categories function identically across languages.

    I could attempt to identify the intended pattern, but validating its general applicability would require additional linguistic evidence, the reference explanation emphasizes a distinction involving natural and human-made objects. A potential limitation is that a rule supported by the examples provided may not describe every possible use of the words.

    This case highlights how multiple-choice grading can successfully test recognition of an intended pattern without necessarily establishing a model's understanding of its exceptions or contextual limitations.

    ### Guarani - Nominal tense and aspect

    This question examines grammatical marking for effected objects: entities that come into existence as a result of an action.

    The reference answer identifies the destinative suffix -rã. The construction is supported by descriptive research on Paraguayan Guarani; Its difficulty lies in understanding a grammatical system in which temporal or aspectual distinctions can be expressed through nominal morphology.

    I would require a reference grammar to confirm the rule, but the problem has a relatively specific target and a clear multiple-choice answer, it also illustrates the importance of distinguishing the correctness of a particular grammatical rule from broader theoretical disagreements about how its markers should be classified.

    ### Tulu and Korean - Lexical resemblance

    This problem asks the model to identify two languages exhibiting phonetic similarities in a small set of words. The reference answer is Tulu and Korean.

    I could not independently identify the intended pair without consulting specialized lexical resources, but the main issue is methodological: similarities between a few words do not establish historical relatedness. This is particularly relevant to parental terms which frequently contain similar sounds across unrelated languages.

    For grading purposes, the question raises concerns about how phonetic similarity is defined and whether the intended language pair is demonstrably the only acceptable answer. These concerns do not prove the reference answer is incorrect but rather they identify aspects requiring verification before treating the item as unambiguous.

    Together, the five problems illustrate different evaluation challenges: multi-stage reasoning, historical inference, semantic generalization, grammatical precision, and the uniqueness of expected answers.

2. Benchmark construction and contributor participation

    HLE was developed by nearly 1,000 subject-matter experts from more than 500 institutions across approximately 50 countries. Contributors included professors, researchers, and individuals with graduate-level expertise, they were responsible for proposing questions, specifying reference answers, and explaining the reasoning supporting those answers.

    The organizers offered a prize pool of approximately USD 500,000 to encourage high-quality submissions, but questions were required to be challenging, precise, objectively answerable, and resistant to straightforward internet retrieval.

    The organizers used advanced language models to screen submissions for difficulty; questions that existing models could reliably answer were generally rejected before human review.

    The project reported more than 70.000 submission and testing attempts with approximately 13.000 questions advancing to expert review. These attempts should not be interpreted as 70.000 unique questions since revisions and repeated tests were part of the process. The final public benchmark contained 2500 questions across more than 100 academic subjects.

    Approximately 76% use short-answer formats, 24% are multiple-choice questions and around 14% include visual information. This process produced a substantially more challenging evaluation set, although selecting questions based on model failure introduces a potential bias toward unusually obscure or difficult-to-interpret problems.

3. Expert validation

    Questions that passed the difficulty screening underwent two stages of human review:

    The first stage involved specialists with graduate-level qualifications in the relevant subject. Each question received between one and three reviews assessing clarity, correctness, originality, and suitability. A subsequent review by organizers and experienced reviewers determined which questions would enter the final dataset.

    An important limitation appears in the original methodology: reviewers were not expected to independently verify a complete solution when doing so would require more than approximately five minutes. Consequently, passing expert review did not necessarily mean that every reference answer had been independently derived and thoroughly checked. This is especially significant for specialized academic questions whose verification may require substantial calculations, literature searches or familiarity with a narrow research area.

    The authors later conducted additional audits. Following revisions, they reported approximately 15.4% expert disagreement in the public benchmark and approximately 18% in a targeted sample of biomedical and chemical questions. These figures represent disagreements under the authors auditing procedures, not necessarily confirmed error rates.

4. Grading methodology

    HLE evaluates models primarily through accuracy and calibration. Accuracy measures the proportion of questions answered correctly according to the reference answers, calibration measures whether a model's stated confidence corresponds to its actual performance. A model that frequently gives incorrect answers with high confidence has poor calibration even if some individual responses are correct.

    In the original evaluation an LLM-based grader using o3-mini compared model responses against official reference answers; although many questions are classified as `exactMatch` the grading procedure can recognize certain equivalent answer representations rather than relying exclusively on literal string matching. However the evaluator is instructed to compare the submitted response with the reference answer, not to independently solve the academic problem. This creates an important dependency: a consistent automatic grader cannot compensate for an incorrect reference answer.

    The grading process may function exactly as designed while still producing misleading results if the expected answer is ambiguous, incomplete, or scientifically incorrect.

5. Independent audits and limitations

    Subsequent research identified substantial quality concerns in the original benchmark.

    In August 2026 Epoch AI audited 48 questions selecting six from each of eight broad categories. The researchers identified 22 questions with significant defects affecting scoring including 12 considered impossible to answer correctly as written and 10 that could incorrectly reject valid answers, which represented approximately 46% of the audited sample. However, the sample was small and stratified equally across categories so the percentage cannot be treated as the established error rate for the entire benchmark.

    FutureHouse conducted a separate investigation of 321 text-only biology and chemistry questions in 2025. Using scientific literature and expert review, the researchers estimated that approximately 29,3% of the examined subset contained reference answers contradicted by published evidence. This finding applies specifically to the audited scientific questions and should not be generalized to other disciplines without further investigation.

    The HLE-Verified project subsequently introduced a systematic verification and revision process, its findings reinforced the importance of independently examining reference answers and explicitly identifying unresolved cases. The original organizers also introduced updated versions including HLE-Rolling and HLE-Diamond.

    Released in September 2026, HLE-Diamond contains 1000 refined questions divided equally between reasoning and specialized knowledge. These revisions demonstrate that maintaining benchmark reliability requires ongoing verification rather than treating the original dataset as permanently settled.

    Beyond reference-answer errors I identified three broader limitations:

        - Selection bias: Filtering questions according to whether existing models fail can favor obscure knowledge or unusual formulations rather than exclusively measuring deep reasoning.

        - Benchmark contamination: Publicly available questions may eventually appear in training data, allowing models to improve their scores through exposure rather than genuine capability improvements.

        - Limited scope: Performance on difficult, closed-ended academic questions does not necessarily predict a model's ability to conduct original research, manage long-term tasks, or solve complex real-world problems.

    These limitations do not eliminate HLE's value but they affect how its results should be interpreted.

6. Comparison with the Lecture 04 evaluation set

    The Lecture 04 evaluation set consisted of ten cases assessing an educational agent against five criteria: grounding, scope, hint, clarity, and lecture marker. Unlike HLE which primarily assesses specialized academic correctness, our evaluation examined whether an assistant behaved appropriately within its intended educational role.

    The small scale allowed us to inspect individual judgments, revise ambiguous criteria and compare human labels with automatic grading.

    In the Implementation exercise the LLM grader agreed with my manual evaluation on 48 of 50 individual criterion judgments (96%). However, agreement on the overall pass/fail outcome was 10 out of 10 cases (100%). The difference demonstrates that aggregate agreement can conceal disagreements at the criterion level.

    HLE faces a related challenge on a much larger scale. A model's overall accuracy may appear precise even when individual questions contain ambiguous wording, defective references, or grading inconsistencies.

    Our evaluation also demonstrated the value of revising unclear criteria: clarifying the grounding policy removed an uncertain judgment and increased automatic coverage in the deterministic test workflow. The same principle applies to large benchmarks although expert-level academic verification requires substantially greater resources.

- Observations and questions: The most important conclusion of this investigation is that benchmark difficulty and benchmark validity are not equivalent. HLE has considerable strengths: a large international contributor network, diverse academic coverage, systematic difficulty screening, expert review, and calibration measurements alongside accuracy. Nevertheless, the independent audits show that a sophisticated development process does not guarantee the correctness of every question or reference answer.

The linguistic examples make these issues concrete. Historical reconstruction may require recognizing equivalent notation; semantic questions may involve context-dependent distinctions; and lexical comparisons may require stronger evidence that an expected answer is uniquely justified.

I also found it important to distinguish between expert disagreement and demonstrated error. Different interpretations may justify additional investigation without automatically invalidating a question.

A related concern is whether evaluation procedures measure genuine reasoning or simply reward reproducing an expected answer, a model may produce a correct answer through unreliable reasoning while another may provide a defensible alternative and receive an incorrect judgment.

This raises several questions: How much independent verification should be required before a question enters a high-stakes benchmark? Should an evaluation recognize alternative answers supported by valid academic evidence? And how can researchers distinguish failures of model capability from failures of the evaluation instrument?

The comparison with Lecture 04 made it clear to me that reliable evaluation depends on clearly defined criteria, appropriate reference answers and mechanisms for investigating disagreements.

My conclusion is that a benchmark must be evaluated as rigorously as the models it is intended to measure. Difficult questions and consistent grading are valuable, but meaningful performance measurements require confidence that the questions themselves are valid and that the evaluation procedure recognizes genuinely correct answers.

Research sources:

- HLE Contributors Consortium. (2026). A benchmark of expert-level academic questions to assess AI capabilities. Nature. https://doi.org/10.1038/s41586-025-09962-4
- HLE research paper and methodological appendices. https://arxiv.org/html/2501.14249
- HLE official dataset. https://huggingface.co/datasets/cais/hle
- Epoch AI. (2026). Humanity's Last Exam — Benchmark Review. https://epoch.ai/benchmarks/hle/review
- FutureHouse. (2025). About 30% of Humanity's Last Exam Chemistry/Biology Answers are Likely Wrong. https://www.futurehouse.org/research/hle-exam
- HLE-Verified: A Systematic Verification and Structured Revision of Humanity's Last Exam. (2026). https://arxiv.org/abs/2602.13964
- Center for AI Safety and Scale AI. (2026). Introducing HLE-Diamond. https://lastexam.ai/blog/hle-diamond
