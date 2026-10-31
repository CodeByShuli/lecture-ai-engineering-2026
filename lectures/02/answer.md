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
