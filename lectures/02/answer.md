# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
- 自分で学習を実行したか（`executed_training_myself`）：はい / いいえ（実行できた範囲：　）
- 学習前：`format_rate` =　 / `content_rate` =　
- 学習後：`format_rate` =　 / `content_rate` =　
- 退行した質問：
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
- 学習で変わったこと・変わらなかったこと：

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- 変えた設定やデータ：
- 結果（比較表や数字）：
- ファインチューニングが向く場面・向かない場面についての考察：

### Basic
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

What I found interesting was that both models reached 100% format accuracy, even though one was trained for half as many epochs. This suggests that 10 epochs were already enough for the model to learn the required JSON structure in this experiment.

Content accuracy was slightly different. The model trained for 20 epochs answered 19 out of 21 questions correctly, while the model trained for 10 epochs answered 18. The shorter training also resulted in a higher training loss, although it took considerably less time.

I also compared how both models handled questions that were not covered by the FAQ. Their classifications were the same: both correctly requested verification for the instructor's name and the next lecture topic, but incorrectly answered the final assignment deadline using information about a different deadline.

This showed me that learning to follow a specific output format is not necessarily the same as learning when an answer is supported by the available information.

I think fine-tuning is useful when we need a model to consistently follow a particular structure or response style. However, I wouldn't rely on fine-tuning alone for questions where factual accuracy is especially important or the information might change. In those cases, retrieving information from a reliable source and checking whether it supports the answer would be more appropriate.

Reducing the training to 10 epochs saved time and preserved perfect format accuracy, but the 20-epoch model performed slightly better on content accuracy in this evaluation.
