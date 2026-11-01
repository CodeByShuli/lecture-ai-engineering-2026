# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：I used Qwen/Qwen3.5-0.8B with LoRA (without quantization), 20 training epochs, a learning rate of 2e-4, lora_r = 16, lora_alpha = 32, and seed 42. The model was evaluated on 21 test questions.
- 自分で学習を実行したか（`executed_training_myself`）：はい（実行できた範囲：　）I ran the training on a T4 GPU in Google Colab and completed all 40 training steps.
- 学習前：`format_rate` =　9.52% (2/21) / `content_rate` =　0% (0/21)
- 学習後：`format_rate` =　100% (21/21) / `content_rate` =　90.48% (19/21)
- 退行した質問：None detected
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：Two questions still failed the content evaluation. When asked about when grades would be published, the model incorrectly used the assignment submission deadline. It also answered a question about whether office hours required a reservation by giving the office hours schedule instead. In both cases, it should have requested verification rather than giving an unsupported answer.
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：Before training, all four questions produced format errors. After training, the model correctly requested verification for the instructor's name and the next lecture topic. However, it incorrectly asserted a deadline for the final assignment. It correctly answered the regular assignment deadline, which was included in the FAQ.
- 学習で変わったこと・変わらなかったこと：LoRA training made a significant difference in how consistently the model followed the required JSON format. Content accuracy also improved considerably. However, the model still struggled with some questions that were not covered by the FAQ. I noticed that following the correct format doesn't necessarily mean the model understands when it lacks enough information to answer.

## 宿題

- 取り組んだレベル：発展, I decided to complete all three levels to explore how different training settings, custom datasets, and glossary-based fine-tuning affect model performance.
- 変えた設定やデータ：For Basic, I reduced the training epochs from 20 to 10. For Implementation, I created a custom FAQ dataset about a fictional Unity game. For Advanced, I generated 116 training examples from the course glossary, prepared a separate evaluation set, and compared the fine-tuned model with direct glossary retrieval.
- 結果（比較表や数字）：In Basic, both configurations achieved 100% format accuracy, while content accuracy was slightly higher with 20 epochs (90.48% vs. 85.71%). In Implementation, format accuracy improved from 38.10% to 100%, and content accuracy reached 90.48%. In Advanced, mean text similarity increased from 0.094 to 0.451, while the glossary retrieval system correctly handled all 12 lookup tests.
- ファインチューニングが向く場面・向かない場面についての考察：Across the three experiments, I found that fine-tuning was particularly effective for improving output consistency and adapting responses to specific datasets. However, it didn't completely prevent incorrect or unsupported answers. I think retrieval is more suitable when answers need to be grounded in a reliable source, while combining retrieval with fine-tuning could provide both consistency and factual support.

### Basic

- settings changed: reduced num_train_epochs from 20 to 10, keeping the other settings unchanged.

Results

| Metric                          | 20 Epochs | 10 Epochs |
| ------------------------------- | --------- | --------- |
| Training steps                  | 40        | 20        |
| Last recorded training loss     | 0.014008  | 0.099810  |
| Training time                   | 259 s     | 107 s     |
| Format accuracy before training | 9.52%     | 9.52%     |
| Format accuracy after training  | 100%      | 100%      |
| Content accuracy after training | 90.48%    | 85.71%    |
| Regressions                     | 0         | 0         |

The 20-epoch loss and training time were recorded during an earlier successful run with the same configuration.

What I found interesting was that both models reached 100% format accuracy, even though one was trained for half as many epochs. This suggests that 10 epochs were already enough for the model to learn the required JSON structure in this experiment. Content accuracy was slightly different. The model trained for 20 epochs answered 19 out of 21 questions correctly, while the model trained for 10 epochs answered 18. The shorter training also resulted in a higher training loss, although it took considerably less time. I also compared how both models handled questions that were not covered by the FAQ. Their classifications were the same: both correctly requested verification for the instructor's name and the next lecture topic, but incorrectly answered the final assignment deadline using information about a different deadline.

This showed me that learning to follow a specific output format is not necessarily the same as learning when an answer is supported by the available information.

I think fine-tuning is useful when we need a model to consistently follow a particular structure or response style. However, I wouldn't rely on fine-tuning alone for questions where factual accuracy is especially important or the information might change. In those cases, retrieving information from a reliable source and checking whether it supports the answer would be more appropriate. Reducing the training to 10 epochs saved time and preserved perfect format accuracy, but the 20-epoch model performed slightly better on content accuracy in this evaluation.


### Intermediate
#### 1. Level and changes made

For the Implementation level, I decided to create my own FAQ dataset based on a fictional video game development project. I chose this topic because I'm interested in game development, and I wanted to see how the model would handle questions about a project with a limited amount of information.

I replaced the original course FAQ with five entries:

- Game engine: Unity 6
- Genre: 2D puzzle-adventure
- Platform: Windows
- Player mode: Single-player
- Demo completion date: December 1, 2026

I modified the `FAQ`, `GROUNDED`, and `UNGROUNDED` variables, along with the additional evaluation questions and I kept the original JSON output format with the `answer` and `needs_review` fields. For the grounded questions, I wrote several different ways of asking about the same information. For example, I included questions like "Which game engine is being used?" and "What engine is the project built with?" to test if the model could recognize different phrasings.

For the ungrounded questions, I deliberately chose information that wasn't mentioned anywhere in the FAQ, such as the game's price, soundtrack composer, voice acting, and system requirements. I also added separate test questions about things like console support, gamepad compatibility, and demo duration. I wanted to check whether the model could recognize when information was missing instead of guessing an answer based on something related.

The final dataset contained 14 training examples, 7 validation examples, and 21 test questions. The training and test questions used different phrasings to avoid evaluating the model on the exact same questions it had seen during training.

#### 2. Training and results

I used Qwen3.5-0.8B with LoRA and kept the original training configuration:

- Training epochs: 20
- Learning rate: `2e-4`
- LoRA rank (`lora_r`): 16
- LoRA alpha (`lora_alpha`): 32
- Seed: 42

The training completed 40 steps in 170 seconds, and the final recorded training loss was 0.016268.

Comparison before and after training:

| Metric | Before training | After training |
|---|---|---|
| Format accuracy | 38.10% | 100% |
| Content accuracy | 0% | 90.48% |
| Both format and content correct | 0% | 90.48% |
| Fully correct responses | 0/21 | 19/21 |
| Regressions | — | 0 |

The improvement was pretty noticeable. Before training, the model frequently returned incomplete JSON responses or forgot to include `needs_review`. After training, all 21 responses followed the required format. Content accuracy also improved significantly, although two questions still failed. The first was "Is the project made with Unity or Unreal Engine?" The model requested verification even though the FAQ clearly stated that Unity 6 was being used. The second was "How long does it take to finish the demo?" Instead of recognizing that the FAQ didn't mention the demo's playtime, the model answered with its scheduled completion date. I found this second mistake particularly interesting because the model produced a perfectly formatted JSON response but confused two different pieces of information.

#### 3. Additional knowledge questions

I also tested four additional questions that weren't part of the original evaluation set. Three asked about information missing from the FAQ: the game's age rating, cloud save support, and character portrait illustrator. The fourth asked about the known demo completion date. Before training, all four responses failed the format check. After training, the model correctly requested verification for the three unknown questions and answered the demo completion date correctly. All four classifications were correct. This was an improvement, but the errors from the previous evaluation showed that the model still couldn't reliably distinguish known and unknown information in every situation.

#### 4. When Fine Tuning is useful and when it isn't

Based on these results, I think fine-tuning is especially useful when we want a model to follow a specific output structure or consistently respond in a particular way. In my experiment, format accuracy increased from 38.10% to 100%, which showed that LoRA worked well for teaching the model the required JSON structure, even with a relatively small dataset.

However, I don't think fine-tuning alone is the best approach when factual accuracy is especially important or when information changes frequently. For example, when the model confused the demo's completion date with its playtime, it showed that it could still provide an unsupported answer even after training. For situations like that, I think a retrieval-based approach would be more appropriate. Instead of depending entirely on information learned during training, the model could look up the relevant information and check whether the source actually supports its answer.

Overall,  teaching a model how to respond and teaching it when it has enough information to respond are two different challenges. Fine-tuning improved both format and content accuracy in my tests, but it didn't eliminate every error.

### Advanced — Fine Tuning with the course glossary

#### 1. Level and changes made

For the Advanced level, I used the course glossary to create a new training dataset instead of working with the fictional FAQ from the previous exercises. I generated the dataset using `scripts/make_sft_dataset.py` in GitHub Codespaces. The script converted the 58 glossary terms into 116 question-answer examples in JSONL format, using the `messages` structure required by `SFTTrainer`, then I uploaded the dataset to Google Colab and modified the notebook to train Qwen3.5-0.8B directly on these examples. I separated the dataset by glossary term, keeping both question variations for each term in the same split. This gave me 92 training examples and 24 validation examples.

I also created 12 evaluation questions divided into four categories:

- 3 rephrased questions: Definitions of terms included in training, but asked using different wording.
- 3 alias questions: Terms referred to by alternative names, such as ADK, token, and Coding Agent.
- 2 held-out terms: Guardrails and Fine-Tuning, which were included in the glossary but excluded from the training set.
- 4 outside-glossary terms: DBSCAN, Kalman Filter, Finite Element Method, and Monte Carlo Tree Search.

For the eight questions about glossary terms, I used their original definitions as reference answers. For the other four, I marked them as absent from the glossary.

#### 2. Training and results

I trained the model using LoRA for 5 epochs, keeping the learning rate at `2e-4`, `lora_r = 16`, and `lora_alpha = 32`. I reduced the number of epochs compared with the previous exercises because this dataset was considerably larger. The training completed 60 steps in 143.3 seconds, the average training loss was approximately 1.4503, while the last logged loss was 0.4582. To compare the model before and after training, I used the same 12 evaluation questions and measured textual similarity against the original glossary definitions.

| Metric | Before Training | After Training |
|---|---|---|
| Evaluation questions | 12 | 12 |
| Mean text similarity | 0.094 | 0.451 |
| Evaluation time | 56.4 s | 37.7 s |

The similarity scores were calculated using the eight questions with reference definitions. The four outside-glossary questions were examined separately. Overall, the model's responses became much closer to the original definitions after training.

Two particularly clear examples were Epoch and Learning Rate. Before training, the model gave longer explanations that didn't properly match the course definitions. After training, it reproduced both definitions exactly, giving them a similarity score of 1.000. However, the improvement wasn't consistent across all categories. The alias questions showed some improvement, but the answers still contained inaccuracies. For example, the model confused ADK with an Amazon-related cloud tool instead of correctly explaining Google's Agent Development Kit. The two held-out terms, Guardrails and Fine-Tuning, also had relatively low similarity scores after training. This was interesting because it suggested that the model had learned some of the specific definitions it encountered during training but didn't necessarily generalize equally well to concepts it hadn't trained on.

For concepts outside the glossary, the model still generated answers rather than indicating that the information wasn't available in the course material. Some of those answers were incorrect or mixed unrelated concepts. This showed me that improved similarity to training definitions doesn't necessarily mean that a model has become consistently reliable.

#### 3. Comparison with glossary retrieval

I also created a simple retrieval-based system to compare with the fine-tuned model. Instead of training, this system searched the original `glossary.json` file for the requested term or one of its aliases. If the term existed, it returned the original definition. Otherwise, it returned "Not in the glossary." The retrieval system correctly handled all 12 evaluation questions.

| Question Category | Correct Lookups |
|---|---|
| Rephrased questions | 3/3 |
| Aliases | 3/3 |
| Held-out terms | 2/2 |
| Outside-glossary terms | 4/4 |
| Total | 12/12 |

I found this comparison especially useful because the retrieval system didn't need to learn or memorize any definitions. It simply accessed the original source. It also correctly identified the four terms that weren't included in the glossary, while the fine-tuned model still attempted to explain them.

However, this wasn't a completely equivalent comparison. The retrieval system had access to the full glossary, including terms excluded from the model's training data. It also relied on exact matching of term names and aliases, which made the evaluation easier for this particular search method. The model's similarity scores and the retrieval system's lookup accuracy measure different things, so they shouldn't be directly compared as percentages of factual accuracy.

#### 4. When Fine Tuning is useful and when it isn't

After completing all three homework levels, I think I have a better understanding of the difference between adapting a model's behavior and giving it reliable access to information. Fine-tuning seems particularly useful when a model needs to consistently follow a specific format, writing style, or task-specific behavior. It can also help the model produce familiar definitions or responses without searching an external dataset every time. Still, fine-tuning requires training resources, and the information learned by the model may become outdated. More importantly, even when the training loss decreases and evaluation scores improve, the model can still produce incorrect information.

In this experiment, the fine-tuned model performed very well on some familiar definitions but struggled with aliases, held-out concepts, and questions outside the glossary. Retrieval seems more appropriate when answers need to stay grounded in a specific source or when the information changes frequently. It can return the original definition directly, and updating the information doesn't require retraining the model.

On the other hand, a simple keyword-based retrieval system depends on finding a matching term. It may struggle with questions that don't explicitly mention the correct terminology. A more advanced retrieval system would be needed to handle those cases. I think a combination of both approaches could be useful: fine-tuning to improve how the model responds, and retrieval to provide reliable, up-to-date information.

Overall, this experiment showed me that memorizing definitions and being able to reliably answer questions about them are not the same thing. LoRA improved the model's responses, but accessing the glossary directly was more dependable for this particular evaluation.
