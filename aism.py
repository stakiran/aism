#!/usr/bin/env python
import argparse
import os
import re
import random
import string
import sys
import subprocess

import pyperclip
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI()

def request_to_model(model_name, prompt, timeout=130):

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            timeout=timeout
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR in {model_name}]: {str(e)}"

def parse_prompt_file(path):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    model_name = None
    prompt_multi_lines = []
    prompt_single_lines = []
    section = None
    for line in lines:
        stripped = line.strip()
        if stripped == '# Models':
            section = 'models'
            continue
        if stripped == '# Prompt':
            section = 'prompt'
            continue
        if stripped == '# Prompt(1line)':
            section = 'prompt1line'
            continue
        if stripped.startswith('# '):
            section = None
            continue
        if section == 'models':
            m = re.match(r'-\s*>(.+)', stripped)
            if m:
                model_name = m.group(1).strip()
        elif section == 'prompt':
            prompt_multi_lines.append(line)
        elif section == 'prompt1line':
            prompt_single_lines.append(line)
    if model_name is None:
        print("モデル名が見つかりませんでした", file=sys.stderr)
        sys.exit(1)
    prompt_multi = ''.join(prompt_multi_lines)
    prompt_single = ''.join(prompt_single_lines)
    return model_name, prompt_multi, prompt_single

def main():
    parser = argparse.ArgumentParser(description='Clipboard→要約ツール aism')
    parser.add_argument('--input', '-i', required=True, help='要約プロンプトのMarkdownファイル')
    args = parser.parse_args()

    # モデルとプロンプト（複数行用, 単一行用）テンプレートを取得
    model, prompt_multi, prompt_single = parse_prompt_file(args.input)

    # クリップボード読み込み
    cb_text = pyperclip.paste()

    # テンプレート選択：改行を含むなら複数行用、そうでなければ単一行用
    if '\n' in cb_text:
        template = prompt_multi
    else:
        template = prompt_single

    # `%cb%` を展開し、末尾に改行を補完
    prompt = template.replace('%cb%', cb_text)
    if not prompt.endswith('\n'):
        prompt += '\n'

    # OpenAI API呼び出し（APIキーは環境変数 OPENAI_API_KEY から取得）
    result = request_to_model(model, prompt)

    # 出力ファイル名生成：aismXXX.md（XXXは英数字3文字）
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    filename = f'aism{suffix}.md'

    # 一時ディレクトリに出力
    temp_dir = os.environ.get('TEMP', '')
    filepath = os.path.join(temp_dir, filename) if temp_dir else filename

    # 結果をファイルに書き込む
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)

    # 関連付けアプリで開く
    if sys.platform.startswith('win'):
        os.startfile(filepath)
    else:
        subprocess.run(['open', filepath])

if __name__ == '__main__':
    main()
