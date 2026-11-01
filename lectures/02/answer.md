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

- 取り組んだレベル：基礎 / 実装 / 発展
- 変えた設定やデータ：
- 結果（比較表や数字）：
- ファインチューニングが向く場面・向かない場面についての考察：

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
#### 1. Level and Changes Made

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

#### 2. Training and Results

I used Qwen3.5-0.8B with LoRA and kept the original training configuration:

- Training epochs: 20
- Learning rate: `2e-4`
- LoRA rank (`lora_r`): 16
- LoRA alpha (`lora_alpha`): 32
- Seed: 42

The training completed 40 steps in 170 seconds, and the final recorded training loss was 0.016268.

Comparison before and after training:

| Metric | Before Training | After Training |
|---|---|---|
| Format accuracy | 38.10% | 100% |
| Content accuracy | 0% | 90.48% |
| Both format and content correct | 0% | 90.48% |
| Fully correct responses | 0/21 | 19/21 |
| Regressions | — | 0 |

The improvement was pretty noticeable. Before training, the model frequently returned incomplete JSON responses or forgot to include `needs_review`. After training, all 21 responses followed the required format. Content accuracy also improved significantly, although two questions still failed. The first was "Is the project made with Unity or Unreal Engine?" The model requested verification even though the FAQ clearly stated that Unity 6 was being used. The second was "How long does it take to finish the demo?" Instead of recognizing that the FAQ didn't mention the demo's playtime, the model answered with its scheduled completion date. I found this second mistake particularly interesting because the model produced a perfectly formatted JSON response but confused two different pieces of information.

#### 3. Additional Knowledge Questions

I also tested four additional questions that weren't part of the original evaluation set. Three asked about information missing from the FAQ: the game's age rating, cloud save support, and character portrait illustrator. The fourth asked about the known demo completion date. Before training, all four responses failed the format check. After training, the model correctly requested verification for the three unknown questions and answered the demo completion date correctly. All four classifications were correct. This was an improvement, but the errors from the previous evaluation showed that the model still couldn't reliably distinguish known and unknown information in every situation.

#### 4. When Fine Tuning is useful and when it isn't

Based on these results, I think fine-tuning is especially useful when we want a model to follow a specific output structure or consistently respond in a particular way. In my experiment, format accuracy increased from 38.10% to 100%, which showed that LoRA worked well for teaching the model the required JSON structure, even with a relatively small dataset.

However, I don't think fine-tuning alone is the best approach when factual accuracy is especially important or when information changes frequently. For example, when the model confused the demo's completion date with its playtime, it showed that it could still provide an unsupported answer even after training. For situations like that, I think a retrieval-based approach would be more appropriate. Instead of depending entirely on information learned during training, the model could look up the relevant information and check whether the source actually supports its answer.

Overall,  teaching a model how to respond and teaching it when it has enough information to respond are two different challenges. Fine-tuning improved both format and content accuracy in my tests, but it didn't eliminate every error.
