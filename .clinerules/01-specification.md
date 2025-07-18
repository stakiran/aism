# aism

## 概要
- aism とは、クリップボードにコピーされた文字列を読み取って要約するツールです

## コマンドライン

```
python aism.py --input summarization-prompt.md
```

## 動作
- 1: クリップボードにコピーされた文字列を取得する
- 2: 1の文字列に「要約プロンプト」を付加した後、OpenAI API を呼び出し、その応答を取得する
- 3: ランダムなファイル名をつくり、2の応答を記入して保存し、このファイルを関連付けで開く

## 使用言語
- Python

# 実装

## クリップボードからの取得
- pyperclip を使ってください

## 要約プロンプトファイル
- `--input` 引数で与えられます
- Markdown ファイルです

以下にファイルの例を示します。

```markdown
# Models
- gpt-4o
- >gpt-4.1
- gpt-4.5-preview
- o1
- o3-mini
- o4-mini

# Prompt
%cb%

- 1行で要約して
- 3行で要約して
- 10行で要約して

# Prompt(1line)
%cb%

概要をレポートした後、以下の要約もつくって。

- 1行で要約
- 3行で前提知識の無い中学生向けにわかりやすく要約
- 3行で専門家向けに要約
- この内容と関連する概念とその概要を最大3つまで列挙、フォーマットは `(概念名) (一言で解説)`
```

Models については、使用するモデルが `>` で記されているので、その行のモデル名を取り出してください。この場合は `gpt-4.1` が正解です。

Prompt については、このセクションの内容がそのままプロンプトになります。ただし `%cb%` はクリップボード内容を示す変数であり、クリップボード内容に展開してください。また、末尾に空行がない場合は追加してください。

なお、クリップボード内容が単一行だった場合は Prompt(1line) の方を使ってください。クリップボード内容が複数行だった場合は Prompt を使ってください。

## OpenAI API の呼び出し
下記で構いません。

```python
def request_to_model(model_name, prompt, timeout=130):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {'role': 'user', 'content': prompt},
            ],
            request_timeout=timeout
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"[ERROR in {model_name}]: {str(e)}"
```

なお openai.ChatCompletion.create に失敗した場合は、出力ファイルにはそのエラー情報を記してください。

## 出力ファイル名
- `aismXXX.md` としてください。
    - `XXX` は `[a-zA-Z0-9]` から成るランダム文字列にしてください
    - また文字数は 3 文字固定です
- このファイルは `%temp%` に出力してください
