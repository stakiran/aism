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

def request_to_model(model_name, prompt, timeout=130):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            request_timeout=timeout
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"[ERROR in {model_name}]: {str(e)}"

def parse_prompt_file(path):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    model_name = None
    prompt_lines = []
    section = None
    for line in lines:
        stripped = line.strip()
        if stripped == '# Models':
            section = 'models'
            continue
        if stripped == '# Prompt':
            section = 'prompt'
            continue
        if stripped.startswith('# '):
            section = None
            continue
        if section == 'models':
            # look for line starting with '-' and '>' prefix
            m = re.match(r'-\s*>(.+)', stripped)
            if m:
                model_name = m.group(1).strip()
        elif section == 'prompt':
            prompt_lines.append(line)
    if model_name is None:
        print("モデル名が見つかりませんでした", file=sys.stderr)
        sys.exit(1)
    prompt = ''.join(prompt_lines)
    return model_name, prompt

def main():
    parser = argparse.ArgumentParser(description='Clipboard→要約ツール aism')
    parser.add_argument('--input', '-i', required=True, help='要約プロンプトのMarkdownファイル')
    args = parser.parse_args()

    # モデルとプロンプトを取得
    model, prompt_template = parse_prompt_file(args.input)

    # クリップボード読み込みと展開
    cb_text = pyperclip.paste()
    prompt = prompt_template.replace('%cb%', cb_text)
    prompt += '\n'

    # OpenAI APIキーは環境変数 OPENAI_API_KEY から読み込まれる
    result = request_to_model(model, prompt)

    # 出力ファイル名生成
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    filename = f'aism{suffix}.md'
    # 出力パスを一時ディレクトリに設定
    temp_dir = os.environ.get('TEMP')
    filepath = os.path.join(temp_dir, filename)

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
