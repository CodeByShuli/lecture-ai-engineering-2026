# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers: The bare LLM explained that it did not have access to the specific homework information for this course and asked for additional course details. In contrast, the agent searched the course glossary and correctly identified the three homework levels including the requirement to complete only one of them.

- Tool calls shown by `--trace` (tool names and arguments): When asked about the three homework levels, the agent called search_glossary with {'query': 'homework'}. The tool returned the relevant glossary entry, which the agent used to construct its answer.

- Number of LLM calls for one question (`requests`): The trace showed 2 model requests and 1 tool call for the question about the three homework levels.

- Tool added and the description in its docstring: I added make_quiz(lecture: int), which selects a random glossary term for the requested lecture and returns a review question with its answer. The docstring describes its putpose as creating review questions from the glossary and specifies that it should be used when a learner asks for a review question or quiz from a particular lecture. I verified that the agent called make_quiz with {'lecture': 2}, and all 11 automated tests passed.

## Homework

### Basic

- What you did: I ran two experiments using the same question ("What is the difference between LoRA and   QLoRA?"). In the first experiment, I removed the instruction requiring the agent to always check the glossary, then I restored it before the second experiment where I changed the search_glossary docstring to allow multiple related terms in a single query.

- Results:
    · Original: 2 tool calls (LoRA and QLoRA separately) and 2 model requests
    · Experiments:
        1st- 2 tool calls and 2 model requests: removing the instructions did not change the tool usage in this run.
        2nd- 1 tool call (query='LoRA and QLoRA') and 2 model requests.
    Also, calling search_glossary directly with the combined query and confirmed that it returned both definitions.

- Observations: The first experiment showed that removing an instruction does not necessarily prevent the agent from using a tool, especially when the tool's own description still encourages its use. The second experiment showed that changing a docstring can influence how the model constructs tool arguments, the combined search worked for these two terms even though I had not modified the search implementation.

This suggests that tool descriptions can affect behaviour, but fewer tool calls dont automatically guarantee better retrieval

### Implementation

- What you did: I added a save_learning_log tool that saves learning records as JSON files inside the learning_log directory: each recod contains a topic, notes and a timestamp. I registered the tool using requires_approval=True and modified the CLI to handle DeferredToolRequests and DeferredToolResults allowing the user to approve or reject saving.

- Results: I tested both approval scenarios using the same request about LoRA.
            Rejected (n): The agent reported that the tool call was denied, I verified that the learning_log directory had not been created.
            Approved (y): The agent successfully saved a JSON file, I checked the directory and opened the file to confirm that the topic, notes and timestamp were correct.
        The existing automated test suite passed all 11 tests before the manual approval tests.

- Ovservations: The exercise helped me understand how human in the loop approval works, clearly registering a tool with requires_approval=True is not enough by itself: the application also needs to handle the pending request and return the users decision.

### Advanced

- What you did: I rebuilt the learning support agent using Google's Agent Development Kit, keeping the same instructions and the three tools from the original exercise: search_glossary, get_lecture_sumary and make_quiz. I created adk_agent/glossary_agent/agent.py and __init__.py, then ran the agent using the ADK CLI.

- Results: The main difference I noticed with Pydantic AI was how the agents are configured: in Pydantic AI I registered the tools individually using agent.tool_plain(). With Google ADK I passed the tools directly as a list when creating the agent. I tested both agents with the same two questions:
        · "What is the difference between LoRA and QLoRA?"
        · "Give me one review question from lecture 02"
Both agents explained LoRA and QLoRA correctly and identified lecture 02 as the relevant session. For the review question Pydantic generated a question about overfitting while Google ADK generated one about Rank(LoRA r). Both provided hints to help the learner think about the answer.

- Observations: I found Google's ADK's agent setup relatively straightforward because I could reuse the existing Python tools without rewriting their implementations. Both frameworks produced useful answers, the differences in wording and selected quiz topics were not significant enough to conclude that one performed better. Unlike the Pydantic AI CLI used in the exercise, the standard ADK CLI output did not display the individual tool calls so I could not directly compare their tool usage from these runs.
