USER_CHAT_TEMPLATE = "<start_of_turn>ユーザー\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>モデル\n"

# standard prompt
standard_prompt = USER_CHAT_TEMPLATE.format(
    prompt="次の数学の問題に答えてください。最終的な答えを数値のみで入力し、それ以外の文字は含めないでください。\n"
) + "{question}\n答え: " + MODEL_CHAT_TEMPLATE

# cot prompt
cot_prompt = USER_CHAT_TEMPLATE.format(
    prompt="次の数学の問題に答えてください。"
           "ステップごとに考え、その思考過程を下に書いてください。"
           "最後の行は「答えは xxx」の形式で、xxx は数値とします。\n"
) + "問題: {question}\nステップごとの答え:\n" + MODEL_CHAT_TEMPLATE

# propose_prompt
propose_prompt = USER_CHAT_TEMPLATE.format(
    prompt="あなたは {lang} を話す {n} 人の独立した数学者で構成されており、"
           "それぞれが多段階の数学問題を解決するための独自の視点を持っていると想像してください。\n\n"
           "各数学者は、問題を解決するための具体的なステップを提案します。"
           "このステップには以下が含まれる必要があります：\n"
           "- **簡潔な説明**：このステップがなぜ必要なのか、そしてどのように問題の解決に役立つのか。\n"
           "- **明確な方程式** または 計算：このステップを実行するためのもの。\n"
           "- 次に取るべき論理的なステップについての簡単な説明。\n\n"
           "各数学者は、回答を '考え i: ' で始める必要があります。ここで 'i' は 1, 2, ... {n} です。\n\n"
           "回答は **1 行で** 以下のフォーマットで記述してください：\n\n"
           "数学的な表現は計算された値で終わる必要があります。\n\n"
           "'考え i: 提案。方程式: [数学的表現]。次のステップ: 次のアクション。'\n\n"
           "各数学者は、異なる方法やアプローチを考慮しながら、独立して問題を解決する必要があります。\n\n"
           "もしこれが最初のステップである場合、各数学者は独立して最適な開始方法を決定します。\n"
           "もし事前のコンテキストが存在する場合は、現在の思考プロセスを基に進行し、解決に向けた前進を確実にします。\n\n"
           "このプロセスは、最終的な答えが得られるまで続き、各ステップで解法が洗練されていきます。\n\n"
) + "---\n" \
    "質問: {question}\n\n" \
    "コンテキスト（これまでの思考プロセス、ある場合）:\n{current_thought_process}\n\n" \
    "3 人の数学者が提案した具体的なステップ:\n" \
    + MODEL_CHAT_TEMPLATE

# value_prompt
value_prompt = USER_CHAT_TEMPLATE.format(
    prompt="与えられた推論のステップが、問題の解決に意味のある貢献をしているかどうかを評価してください。"
           "回答は『評価: 確実』『評価: 可能性あり』『評価: 不可能』のいずれかにしてください。"
           "説明や追加のテキストを含めないでください。\n\n"
           "以下のいずれかの評価を選択してください:\n"
           "- 確実: ステップは正しく、解決に向けた論理的な進展である。\n"
           "- 可能性あり: ステップは妥当だが、さらなる洗練が必要か、重要な詳細が不足している可能性がある。\n"
           "- 不可能: ステップは間違っている、関連性がない、または既知の事実と矛盾している。\n\n"
           "---\n"
           "問題: 列車が A 駅から 50 人の乗客を乗せて出発しました。次の駅で 15 人が降り、"
           "30 人が新たに乗車しました。現在、列車には何人の乗客がいますか？\n\n"
           "提案された次のステップ: 正味の変化を計算する：-15 + 30。\n評価: 確実\n\n"
           "提案された次のステップ: 状況を方程式として表す：50 - 15 + 30 = x。\n評価: 確実\n\n"
           "提案された次のステップ: 次の駅で 20 人が降りたと仮定し、合計が一致するか確認する。\n評価: 不可能\n\n"
           "提案された次のステップ: この関係をパーセンテージとして表す：(50 - 15) / 50。\n評価: 不可能\n\n"
           "提案された次のステップ: 各駅ごとに乗客数を 2 倍にすることを考慮する。\n評価: 不可能\n\n"
           "提案された次のステップ: 最終的な乗客数が x であると仮定し、逆算する。\n評価: 確実\n\n"
           "---\n"
           "問題: サーバールームには 9 台のコンピュータがありました。月曜日から木曜日まで、毎日 5 台ずつ設置されました。"
           "現在、サーバールームには何台のコンピュータがありますか？\n\n"
           "提案された次のステップ: 追加されたコンピュータの合計を計算する：5 × 4。\n評価: 確実\n\n"
           "提案された次のステップ: 変化を算術数列として表す：9 + (5 × n) （ここで n は日数）。\n評価: 確実\n\n"
           "提案された次のステップ: コンピュータが追加されたのではなく、削除されたと仮定する：9 - (5 × 4)。\n評価: 不可能\n\n"
           "提案された次のステップ: 問題を比率に変換する：(9 / 5) × 4。\n評価: 不可能\n\n"
           "提案された次のステップ: 線形加算ではなく、指数関数的な増加を仮定する。\n評価: 不可能\n\n"
           "提案された次のステップ: 逆計算をしても、元の 9 台のコンピュータになるかを確認する。\n評価: 確実\n\n"
) + "---\n" \
    "{question}\n\n" \
    "提案された次のステップ: {curr_candidate}\n\n" \
    "評価:" \
    + MODEL_CHAT_TEMPLATE

# Force output prompt
force_output_prompt = USER_CHAT_TEMPLATE.format(
    prompt="以下のコンテキストを考慮し、問題の最終的な答えを導き出してください。\n\n"
           "次のルールを厳守してください:\n"
           "- 方程式をステップごとに書き、各計算を論理的に説明する。\n"
           "- 提供されたコンテキストを活用し、各ステップが論理的に繋がるようにする。\n"
           "- コンテキストにすでにあるステップは繰り返さない。\n"
           "- 最後の行には、最終的な答えの数値のみを記入し、追加のテキストを含めない。\n\n"
           "コンテキスト（以前の思考過程、ある場合）:\n"
           "{context}\n\n"
) + "---\n" \
    "問題: {question}\n\n" \
    "解答:\n" \
    "ステップ 1: " \
    + MODEL_CHAT_TEMPLATE

# Choose final answer
final_judge_prompt = USER_CHAT_TEMPLATE.format(
    prompt="あなたは数学の判定者として、問題の最終的な答えを決定する役割を担っています。\n\n"
           "まず、問題文を注意深く分析してください。その後、以下の候補となる解答を厳密に検討します。\n"
           "各候補の論理的な思考過程を比較し、最も正確な最終結果を決定してください。\n\n"
           "次のルールに従ってください:\n"
           "- 決定を下す前に、論理的に問題を検討する。\n"
           "- 正しい解答が複数ある場合は、最も適切なものを選ぶ。\n"
           "- 候補の解答に矛盾や欠落がある場合は、それを考慮しない。\n"
           "- 最終出力は、単一の正しい数値のみで、説明や追加のテキストを含めない。\n\n"
           "---\n"
           "問題文:\n"
           "{question}\n\n"
           "候補となる解答:\n"
           "{candidate_answers}\n\n"
           "---\n"
           "最終的な答え: "
) + MODEL_CHAT_TEMPLATE