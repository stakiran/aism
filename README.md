# aism
クリップボードにコピーされた内容の要約（複数行のとき）または概要（一行のとき）をつくる CLI ツール。

## 前提条件
- Windows
- Python 3.12 以上
- 環境変数 `OPENAI_API_KEY` に OpenAI API キーを設定すること

## インストール
```bash
git clone https://github.com/stakiran_sub/aism.git
cd aism
pip install pyperclip openai
```

requirements 参考:

```
$ pip freeze | grep -i openai
openai==1.95.0

$ pip freeze | grep -i pyperclip
pyperclip==1.9.0
```

## 使い方

### 1: 要約プロンプトファイルをつくります
詳細は .clinerules/01-specification.md を見てください

### 2: クリップボードに要約対象をコピー

### 3: aism 実行

```bash
python aism.py --input (要約プロンプトファイル名).md
```

すると、一時ディレクトリ（`%TEMP%`）に `aismXXX.md`（XXXは英数字3文字）が生成され、自動的に関連付けアプリで開かれます。

## 開発者向け
- Cline を使っています
- .clinerules/01-specification.md に仕様を書いた後、Cline に読ませてコードをつくってもらいます

## ライセンス
MIT
